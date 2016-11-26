
from gazebo.msgs import (
    Publish,
)

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

    def __unicode__(self):
        return "%s (%s) %s:%s" % (self.topic, self.type, self.host, self.port)

    def connect(connection: Connection):
        # not implemented in origin for some reason
        raise Exception("Ha! Psych!")
