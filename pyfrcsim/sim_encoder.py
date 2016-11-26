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


class SimEncoder:
    def __init__(self, topic: str):
        self.position = 0.0
        self.velocity = 0.0
        self.command_publisher = advertise("%s/control" % (topic,), theString())

        def pos_callback(msg: Float64):
            self.position = msg.getData()

        subscribe("%s/position" % (topic,), theFloat(), pos_callback)

        def vel_callback(msg: Float64):
            self.velocity = msg.getData()

        subscribe("%s/velocity" % (topic,), theFloat(), vel_callback)

        # source code uses thread.interrupt. we just let the exception kill the thread?
        if self.command_publisher.wait_for_connection(5000):
            logger.info("Initialied: %s" % (topic,))
        else:
            logger.error("Failed to initialize %s: does the encoder exist?" % (topic,))

    def _send_command(self, cmd: str): 
        self.command_publisher.publish(makeString(cmd))

    def reset(self):
        self._send_command("reset")

    def start(self):
        self._send_command("start")

    def stop(self):
        self._send_command("stop")
