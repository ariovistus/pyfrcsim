import os
import logging
import socketserver
import socket
import threading
from google.protobuf.message import (
    Message
)
from gazebo.msgs.packet_pb2 import Packet
from gazebo.msgs.publish_pb2 import Publish
from gazebo.msgs.publishers_pb2 import Publishers
from gazebo.msgs.subscribe_pb2 import Subscribe
from gazebo.msgs.gz_string_pb2 import GzString
from gazebo.msgs.gz_string_v_pb2 import GzString_V
from gazebo.gz_msgs.bool_pb2 import Bool
from gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self):
        self.socket = None
        self.server = None

    def connect(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.create_connection((host, port))
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
        self.rfile = self.socket.makefile('r')
        self.wfile = self.socket.makefile('w')

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
            self.server.serve_forever()
        thread = threading.Thread(target=_serve)
        thread.start()
        
    def raw_read(self):
        # todo: determine api
        return None

    def read(self) -> Packet:
        # todo: determine api
        return None
        
    def write(self, message: Message):
        # todo: pull in protobuf
        pass

    def write_packet(self, message: Message):
        # todo: figure out where packet.proto is
        pass


class Node:
    def __init__(self, name):
        self.name = name
        self.server = Connection()
        self.master = Connection()
        self.publishers = {}
        self.subscriptions = {}
        self.namespaces = []

    def wait_for_connection(self):
        default_uri = "localhost:11345"
        user_defined_uri = os.environ.get("GAZEBO_MASTER_URI", default_uri)
        xs = user_defined_uri.split(":")
        if len(xs) != 2:
            logger.error("invalid GAZEBO_MASTER_URI %s. URI must be of the form HOSTNAME:PORT" % (user_defined_uri,))
            logger.warning("using default %s" % (default_uri,));
            xs = default_uri.split(":")
        host, port = xs
        port = int(port)

        def _handle(conn: Connection):
            self.handle(conn)

        self.server.serve(_handle)
        self.master.connect_and_wait(host, port)
        self.initialize_connection()
        def _run():
            self.run()
        thread = threading.Thread(target=_run)
        thread.start()

    def advertise(topic: str, defaultMessage: Message):
        topic = self._fix_topic(topic)
        logger.info("ADV %s" % (topic,))
        _type = get_type_name(defaultMessage)
        pub = Publisher(topic, _type, self.server.host, self.server.port)
        self.publishers[topic] = pub
        
        # todo: find publish.proto, figure out the real way to construct one
        req = Publish(topic, _type, self.server.host, self.server.port)

        try:
            self.master.write_packet("advertise", req)
        except Exception as ex:
            # todo: refine exception type
            # todo todo: wait for original authors to think of something more
            logger.exception("something bad")
        return pub

    def subscribe(self, topic: str, defaultMessage: Message, callback):
        topic = self._fix_topic(topic)
        logger.info("SUB %s" % (topic,))
        if topic in self.subscriptions:
            raise Exception("Multiple subscriptions for %s" % (topic,))

        _type = get_type_name(defaultMessage)

        # todo: find subscribe.proto, figure out the real way to construct one
        req = Subscribe(topic, _type, self.server.host, self.server.port, latching=False)

        try:
            self.master.write_packet("subscribe", req)
        except Exception as ex:
            # todo: refine exception type
            # todo todo: wait for original authors to think of something more
            logger.exception("something bad")

        sub = Subscriber(topic, _type, callback, defaultMessage, self.server.host, self.server.port)
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
        version = GzString.String.parseFrom(init_data.getSerializedData())
        log.info("Version: %s" % (version.getDate()))

        namespace_data = self.master.read()
        ns = String_V.parseFrom(namespace_data.getSerializedData())
        self.namespaces.extend(ns.getDataList())
        logger.info(str(namespaces))

        publisher_data = self.master.read()
        if publisher_data.type == "publisher_init":
            pubs = Publishers.parseFrom(publisher_data.getSerializedData())
            for pub in pubs.getPublisherList():
                record = RemotePublisherRecord(pub)
                self.publishers[record.topic] = record
            logger.info(str(self.publishers))
        else:
            logger.error("No publisher data received.")

    def process_packet(self, packet):
        if packet.type == "publisher_add": 
            pub = RemotePublisherRecord(Publish.parseFrom(packet.getSerializedData()))
            
            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("ACK %s" % (pub.topic,))
                return

            logger.info("New Publisher: %s" % (pub.topic,))
            logger.info("Publisher: %s" % (Publish.parseFrom(packet.getSerializedData())))
            self.publishers[pub.topic] = pub
        elif packet.type in ["publisher_subscribe", "publisher_advertise"]:
            pub = RemotePublisherRecord(Publish.parseFrom(packet.getSerializedData()))

            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("Ignoring subscription request on (local) %s" % (pub.topic,))
                return
            
            logger.info("PUBSUB found for: %s" % (pub.topic,))
            logger.info("Publisher: %s" % (Publish.parseFrom(packet.getSerializedData())))
            self.subscriptions[pub.topic].connect(pub)
        elif packet.type == "topic_namespace_add":
            self.namespaces.append(GzString.String.parseFrom(packet.getSerializedData()).getData())
            logger.info("New Namespace: %s" % (pub.topic,))
        elif packet.type == "unsubscribe":
            sub = Subscribe.parseFrom(packet.getSerializedData())
            logger.warning("Ignoring unsubscribe: %s" % (sub,));
        else:
            logger.warning("Can't handle %s" % (packet.type,))

    def handle(self, conn: Connection):
        log.info("Handling new connection")
        msg = conn.read()
        if msg is None:
            log.warning("Didst read null messaged.")
            return

        if msg.type == "sub":
            sub = Subscribe.parseFrom(msg.getSerializedData())
            if sub.topic not in self.publishers:
                logger.error("Subscription for unknown topic %s" % (sub.topic,))
                return

            logger.info("New connection for topic %s" % (sub.topic,))

            pub = self.publishers[sub.topic]

            if pub.type != sub.type:
                logger.error("Message type mismatch requested=%d publishing=%s" % (pub.type, sub.type))
                return


            logger.info("CONN %s" % (sub.topic,))

            pub.connect(conn)
        else:
            logger.warning("Unknown message type: %s" % (msg.type,))


    def _fix_topic(self, topic: str):
        return "/gazebo/%s/%" % (self.name, topic)


def get_type_name(message: Message) -> str:
        return message.DESCRIPTOR.full_name


def theBool():
    return Bool.getDefaultInstance()


def theString():
    return String.getDefaultInstance()


def makeString(s: str):
    return String.newBuilder().setData(s).build()


def theFloat():
    return Float64.getDefaultInstance()


def makeFloat(f: float):
    return Float64.newBuilder().setData(f).build()


class Publisher(Message):
    def __init__(self, topic, type, host, port):
        self.topic = topic
        self.type = type
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
        return self.pub.getTopic()

    @property
    def host(self) -> str:
        return self.pub.getHost()

    @property
    def port(self) -> int:
        return self.pub.getPort()

    @property
    def type(self) -> int:
        return self.pub.getMessageType()

    def __str__(self):
        return "%s (%s) %s:%s" % (self.topic, self.type, self.host, self.port)

    def connect(connection: Connection):
        # not implemented in origin for some reason
        raise Exception("Ha! Psych!")


class Subscriber(Message):
    def __init__(self, topic, type, callback):
        self.topic = topic
        self.type = type
        self.host = host
        self.port = port
        self.callback = callback
        # todo: figure out the real api
        self.deserializer = deserialier.getParserForType()
        self.connections = []

    def connect(self, pub):
        def _run():
            self.handle_connect(pub)
        thread = threading.Thread(target=_run)
        thread.start()

    def handle_connect(self, pub):
        logger.info("CONN for %s from %s:%s" % (self.topic, self.host, self.port))
        conn = Connection()
        try:
            conn.connect(pub.host, pub.port)
            self.connections.append(conn)
            # todo: figure out the real api
            sub = Subscribe(self.topic, self.type, self.host, self.port, latching=False)
            conn.write_packet("sub", sub)

            while True:
                data = conn.raw_read()
                if data is None:
                    self.connections.remove(conn)
                    return
                msg = deserializer.parseFrom(data)
                self.callback(msg)
        except Exception:
            # todo: refine exception type
            try:
                conn.close()
            except Exception:
                # todo: refine exception type
                pass
            logger.exception("exception in handle_connect")

