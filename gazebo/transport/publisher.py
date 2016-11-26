import logging
from google.protobuf.message import (
    Message
)

logger = logging.getLogger(__name__)


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
