import logger
from gazebo.transport.msgs import (
    theString,
    makeString,
    theFloat,
)
from gazebo.transport import Float64
from main_node import (
    subscribe,
    advertise,
)

logger = logging.getLogger(__name__)


class SimGyro:
    def __init__(self, topic: str):
        self.position = float('NaN')
        self.velocity = float('NaN')
        self.command_publisher = advertise("%s/control" % (topic,), theString())
        self.command_publisher.latching = True

        def pos_callback(msg: Float64):
            self.position = msg.getData()

        subscribe("%s/position" % (topic,), theFloat(), pos_callback)

        def vel_callback(msg: Float64):
            self.velocity = msg.getData()

        subscribe("%s/velocity" % (topic,), theFloat(), vel_callback)

    def _send_command(self, cmd: str): 
        self.command_publisher.publish(makeString(cmd))

    def reset(self):
        self._send_command("reset")

    def getAngle(self):
        return self.position

    def getVelocity(self):
        return self.velocity

