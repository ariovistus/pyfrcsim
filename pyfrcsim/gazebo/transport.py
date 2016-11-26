import os
import time
import logging
import socketserver
import socket
import threading
from google.protobuf.message import (
    Message
)
from .msgs.packet_pb2 import Packet
from .msgs.publish_pb2 import Publish
from .msgs.publishers_pb2 import Publishers
from .msgs.subscribe_pb2 import Subscribe
from .msgs.time_pb2 import Time
from .msgs.gz_string_pb2 import GzString
from .msgs.gz_string_v_pb2 import GzString_V
from .gz_msgs.bool_pb2 import Bool
from .gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)


class Connection:
    HEADER_SIZE = 8
    def __init__(self):
        self.socket = None
        self.server = None

    def connect(self, host: str, port: int):
        logger.info("raw connect %s:%s", host, port)
        self.host = host
        self.port = port
        self.socket = socket.create_connection((host, port))
        local_host, local_port = self.socket.getsockname()
        remote_host, remote_port = self.socket.getpeername()
        logger.info("   connect %s:%s -> %s:%s", local_host, local_port, remote_host, remote_port)
        self._make_streams()

    def connect_and_wait(self, host: str, port: int):
        self.host = host
        self.port = port
        while True:
            try:
                self.socket = socket.create_connection((host, port))
                break
            except socket.timeout as ex:
                logger.warning("Cannot connect, retrying in five seconds.", exc_info=1)
        self._make_streams()

    def _make_streams(self):
        self.rfile = self.socket.makefile('b')
        self.wfile = self.socket.makefile('wb')

    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        if self.server is not None:
            self.server.shutdown()
            self.server = None

    def serve(self, callback):
        class Handler(socketserver.StreamRequestHandler):
            def __init__(hself):
                hself.callback = callback

            def handle(self):
                conn = Connection()
                conn.rfile = hself.rfile
                conn.wfile = hself.wfile
                hself.callback(conn)

        def _serve():
            self.server = socketserver.TCPServer(("", 0), Handler) 
            x = self.host, self.port = self.server.server_address
            logger.debug("listening on %s:%s" % x)
            self.server.serve_forever()
        thread = threading.Thread(target=_serve)
        thread.start()
        
    def raw_read(self) -> bytes:
        buff = self.rfile.read(Connection.HEADER_SIZE)
        if len(buff) != 8:
            logger.error("Only read %d bytes instead of 8 for header." % (len(buff),))
            return None
        size = int(buff, 16)
        data = self.rfile.read(size)
        return data

    def read(self) -> Packet:
        a = self.raw_read()
        if a is None:
            return None
        p = Packet()
        p.ParseFromString(a)
        return p
        
    def write(self, message: Message):
        _bytes = message.SerializeToString()
        self.wfile.write(_bytes)

    def write_packet(self, name: str, message: Message):
        ms = current_time_millis()
        pack = Packet()
        pack.stamp.sec = ms // 1000
        pack.stamp.nsec = (ms % 1000) * 1000
        pack.type = name
        pack.serialized_data = message.SerializeToString()
        self.write(pack)


def get_type_name(message: Message) -> str:
        return message.DESCRIPTOR.full_name


class Publisher(Message):
    def __init__(self, topic, msg_type, host, port):
        self.topic = topic
        self.msg_type = msg_type
        self.host = host
        self.port = port
        self.listeners = []
        self.latching = False
        self.last_msg = None

    def publish(self, msg: Message):
        self.last_msg = msg
        to_remove = []
        for listener in self.listeners:
            try:
                listener.write(msg)
            except Exception:
                # todo: refine exception type
                to_remove.append(listener)

        for listener in to_remove:
            logger.info("Removing listener from topic %s" % (self.topic,))
            try:
                listener.close()
            except Exception:
                # todo: refine exception type
                # boo hoo
                pass
            self.listeners.remove(listener)

    def connect(self, conn: Connection):
        logger.info("Handling subscriber connection for topic: %s" % (self.topic,))
        if self.latching and self.last_msg is not None:
            try:
                conn.write(self.last_msg)
            except Exception:
                # todo: refine exception type
                logger.warning("Writing latched message failed on topic %s" % (self.topic,))
                try:
                    conn.close()
                except Exception:
                    # todo: refine exception type
                    # boo hoo
                    pass
            return

        self.listeners.append(conn)
        self.notify_all()

    def wait_for_connection(timeout_millis: int) -> bool:
        start = current_time_millis()
        while not self.listeners:
            remain = timeout_millis - (current_time_millis() - start)
            if remain <= 0:
                break
            this.wait(remain)

        return bool(self.listeners)
        

def current_time_millis(): 
    return int(round(time.time() * 1000))


class RemotePublisherRecord:
    def __init__(self, pub: Publish):
        self.pub  = pub

    @property
    def topic(self) -> str:
        return self.pub.topic

    @property
    def host(self) -> str:
        return self.pub.host

    @property
    def port(self) -> int:
        return self.pub.port

    @property
    def msg_type(self) -> int:
        return self.pub.msg_type

    def __str__(self):
        return "%s (%s) %s:%s" % (self.topic, self.msg_type, self.host, self.port)

    def connect(connection: Connection):
        # not implemented in origin for some reason
        raise Exception("Ha! Psych!")


class Subscriber(Message):
    def __init__(self, topic, msg_type, callback, message_class, host, port):
        self.topic = topic
        self.msg_type = msg_type
        self.host = host
        self.port = port
        self.callback = callback
        self.message_class = message_class
        self.connections = []

    def connect(self, pub):
        def _run():
            self.handle_connect(pub)
        thread = threading.Thread(target=_run)
        thread.start()

    def handle_connect(self, pub):
        logger.info("CONN for %s from %s:%s", self.topic, self.host, self.port)
        conn = Connection()
        try:
            conn.connect(pub.host, pub.port)
            self.connections.append(conn)
            sub = Subscribe()
            sub.topic = self.topic
            sub.msg_type = self.msg_type
            sub.host = self.host
            sub.port = self.port
            sub.latching = False
            conn.write_packet("sub", sub)

            while True:
                data = conn.raw_read()
                if data is None:
                    self.connections.remove(conn)
                    return
                import pdb
                pdb.set_trace()
                msg = self.message_class()
                msg.ParseFromString(data)
                self.callback(msg)
        except Exception:
            # todo: refine exception type
            try:
                conn.close()
            except Exception:
                # todo: refine exception type
                pass
            logger.exception("exception in handle_connect")


class Node:
    def __init__(self, name):
        self.name = name
        self.server = Connection()
        self.master = Connection()
        self.publishers = {}
        self.subscriptions = {}
        self.namespaces = []

    def wait_for_connection(self, host: str, port: int):
        def _handle(conn: Connection):
            self.handle(conn)

        self.server.serve(_handle)
        self.master.connect_and_wait(host, port)
        self.initialize_connection()
        def _run():
            self.run()
        thread = threading.Thread(target=_run)
        thread.start()

    def advertise(self, topic: str, message_class: Message) -> Publisher:
        topic = self._fix_topic(topic)
        logger.info("ADV %s" % (topic,))
        msg_type = get_type_name(message_class)
        pub = Publisher(topic, msg_type, self.server.host, self.server.port)
        self.publishers[topic] = pub
        
        # todo: find publish.proto, figure out the real way to construct one
        req = Publish()
        req.topic = topic
        req.msg_type = msg_type
        req.host = self.server.host
        req.port = self.server.port

        try:
            self.master.write_packet("advertise", req)
        except Exception as ex:
            # todo: refine exception type
            # todo todo: wait for original authors to think of something more
            logger.exception("something bad")
        return pub

    def subscribe(self, topic: str, message_class: Message, callback: "(Message) -> None"):
        topic = self._fix_topic(topic)
        logger.info("SUB %s", topic)
        if topic in self.subscriptions:
            raise Exception("Multiple subscriptions for %s" % (topic,))

        msg_type = get_type_name(message_class)

        req = Subscribe()
        req.topic = topic 
        req.msg_type = msg_type
        req.host = self.server.host
        req.port = self.server.port
        req.latching = False

        try:
            self.master.write_packet("subscribe", req)
        except Exception as ex:
            # todo: refine exception type
            # todo todo: wait for original authors to think of something more
            logger.exception("something bad")

        sub = Subscriber(topic, msg_type, callback, message_class, self.server.host, self.server.port)
        self.subscriptions[topic] = sub
        # waaat? the topic is the dict's key, why would you iterate through everything?
        # unless its possible for the topic to change after its been added to the dict..
        for pub in self.publishers.values():
            if pub.topic == topic:
                sub.connect(pub)
        return sub

    def run(self): 
        try:
            while True:
                packet = self.master.read()
                if packet is None:
                    logger.critical("Received null packet, shutting down connection to master.")
                    self.master.close()
                    return
                self.process_packet(packet)
        except Exception:
            # todo: refine exception type
            logger.exception("I/O Error (?)")

    def initialize_connection(self):
        init_data = self.master.read()
        if init_data.type != "version_init":
            raise Exception("Expected 'version_init' packet, got '%s'." % (init_data.type,))
        # todo: figure out the actual api for 
        version = GzString()
        version.ParseFromString(init_data.serialized_data)
        logger.info("Version: %s", version.data)

        namespace_data = self.master.read()
        ns = GzString_V()
        ns.ParseFromString(namespace_data.serialized_data)
        self.namespaces.extend(ns.data)
        logger.info(str(self.namespaces))

        publisher_data = self.master.read()
        if publisher_data.type == "publishers_init":
            pubs = Publishers()
            pubs.ParseFromString(publisher_data.serialized_data)
            for pub in pubs.publisher:
                record = RemotePublisherRecord(pub)
                self.publishers[record.topic] = record
            for pub in self.publishers:
                logger.info(self.publishers[pub])
        else:
            logger.error("No publisher data received.")

    def process_packet(self, packet):
        if packet.type == "publisher_add": 
            pub1 = Publish()
            pub1.ParseFromString(packet.serialized_data)
            pub = RemotePublisherRecord(pub1)
            
            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("ACK %s", pub.topic)
                return

            logger.info("New Publisher: %s", pub.topic)
            logger.info("Publisher: %s", pub1)
            self.publishers[pub.topic] = pub
        elif packet.type in ["publisher_subscribe", "publisher_advertise"]:
            pub1 = Publish()
            pub1.ParseFromString(packet.serialized_data)
            pub = RemotePublisherRecord(pub1)

            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("Ignoring subscription request on (local) %s", pub.topic)
                return
            
            logger.info("PUBSUB found for: %s", pub.topic)
            logger.info("Publisher: %s", pub1)
            self.subscriptions[pub.topic].connect(pub)
        elif packet.type == "topic_namespace_add":
            ns = GzString()
            ns.ParseFromString(packet.serialized_data)
            self.namespaces.append(ns.data)
            logger.info("New Namespace: %s", pub.topic)
        elif packet.type == "unsubscribe":
            sub = Subscribe()
            sub.ParseFromString(packet.serialized_data)
            logger.warning("Ignoring unsubscribe: %s", sub);
        else:
            logger.warning("Can't handle %s", packet.type)

    def handle(self, conn: Connection):
        import pdb
        pdb.set_trace()
        logger.info("Handling new connection")
        msg = conn.read()
        if msg is None:
            logger.warning("Didst read null messaged.")
            return

        if msg.type == "sub":
            sub = Subscribe()
            sub.ParseFromString(msg.serialized_data)
            if sub.topic not in self.publishers:
                logger.error("Subscription for unknown topic %s", sub.topic)
                return

            logger.info("New connection for topic %s", sub.topic)

            pub = self.publishers[sub.topic]

            if pub.msg_type != sub.msg_type:
                logger.error("Message type mismatch requested=%d publishing=%s", pub.msg_type, sub.msg_type)
                return


            logger.info("CONN %s", sub.topic)

            pub.connect(conn)
        else:
            logger.warning("Unknown message type: %s", msg.type)


    def _fix_topic(self, topic: str):
        return "/gazebo/%s/%s" % (self.name, topic)


