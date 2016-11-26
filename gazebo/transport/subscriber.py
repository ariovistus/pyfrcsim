import logging
from typing import (
    Callable
)
from google.protobuf.message import (
    Message
)

logger = logging.getLogger(__name__)


class Subscriber(Message):
    def __init__(self, topic, type, callback: Callable[[Message], None], deserializer: Message, host, port):
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

