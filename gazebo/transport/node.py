import os
import logging
from typing import (
    Callable
)
from google.protobuf.message import (
    Message
)
from gazebo.msgs import (
    Publish,
    Subscribe,
    Packet,
    Publishers,
    GzString,
    String_V,
)

logger = logging.getLogger(__name__)


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

    def subscribe(self, topic: str, defaultMessage: Message, callback: Callable[[Message], None]):
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
            pub = RemotePublisherRecord(Publish.parseFrom(packet.getSerializedData())
            
            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("ACK %s" % (pub.topic,))
                return

            logger.info("New Publisher: %s" % (pub.topic,))
            logger.info("Publisher: %s" % (Publish.parseFrom(packet.getSerializedData()))
            self.publishers[pub.topic] = pub
        elif packet.type in ["publisher_subscribe", "publisher_advertise"]:
            pub = RemotePublisherRecord(Publish.parseFrom(packet.getSerializedData())

            if pub.host == self.server.host and pub.port == self.server.port:
                logger.info("Ignoring subscription request on (local) %s" % (pub.topic,))
                return
            
            logger.info("PUBSUB found for: %s" % (pub.topic,))
            logger.info("Publisher: %s" % (Publish.parseFrom(packet.getSerializedData()))
            self.subscriptions[pub.topic].connect(pub)
        elif packet.type == "topic_namespace_add":
            self.namespaces.append(GzString.String.parseFrom(packet.getSerializedData()).getData())
            logger.info("New Namespace: %s" % (pub.topic,))
        elif packet.type == "unsubscribe":
            sub = Subscribe.parseFrom(packet.getSerializedData());
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
