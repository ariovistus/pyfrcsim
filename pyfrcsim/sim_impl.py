import logger
from gazebo.gz_msgs.bool_pb2 import Bool
from gazebo.gz_msgs.float64_pb2 import Float64
from gazebo.msgs.gz_string_pb2 import GzString
from main_node import (
    subscribe,
    advertise,
)

logger = logging.getLogger(__name__)


class SimDigitalInput:
    def __init__(self, topic: str):
        self.value = False

        def callback(msg: Bool):
            self.value = msg.getData()

        subscribe(topic, Bool, callback)

    def get(self):
        return self.value


class SimEncoder:
    def __init__(self, topic: str):
        self.position = 0.0
        self.velocity = 0.0
        self.command_publisher = advertise("%s/control" % (topic,), GzString)

        def pos_callback(msg: Float64):
            self.position = msg.getData()

        subscribe("%s/position" % (topic,), Float64, pos_callback)

        def vel_callback(msg: Float64):
            self.velocity = msg.getData()

        subscribe("%s/velocity" % (topic,), Float64, vel_callback)

        # source code uses thread.interrupt. we just let the exception kill the thread?
        if self.command_publisher.wait_for_connection(5000):
            logger.info("Initialied: %s" % (topic,))
        else:
            logger.error("Failed to initialize %s: does the encoder exist?" % (topic,))

    def reset(self):
        _send_command(self.command_publisher, "reset")

    def start(self):
        _send_command(self.command_publisher, "start")

    def stop(self):
        _send_command(self.command_publisher, "stop")


class SimFloatInput:
    def __init__(self, topic: str):
        self.value = float("NaN")

        def callback(msg: Float64):
            self.value = msg.getData()

        subscribe(topic, Float64, callback)

    def get(self):
        return self.value


class SimGyro:
    def __init__(self, topic: str):
        self.position = float('NaN')
        self.velocity = float('NaN')
        self.command_publisher = advertise("%s/control" % (topic,), GzString)
        self.command_publisher.latching = True

        def pos_callback(msg: Float64):
            self.position = msg.getData()

        subscribe("%s/position" % (topic,), Float64, pos_callback)

        def vel_callback(msg: Float64):
            self.velocity = msg.getData()

        subscribe("%s/velocity" % (topic,), Float64, vel_callback)

    def reset(self):
        _send_command(self.command_publisher, "reset")

    def getAngle(self):
        return self.position

    def getVelocity(self):
        return self.velocity


class SimSpeedController:
    def __init__(self, topic: str):
        self.value = 0.0

        self.pub = advertise(topic, Float64)

    def get(self) -> float:
        return self.value

    def set(self, value: float):
        msg = Float64()
        msg.data = float(value)
        self.pub.publish(msg)

    def disable(self):
        self.set(0.0)

    def pidWrite(output: float):
        self.set(output)


def _send_command(pub: Publisher, cmd: str): 
    msg = GzString()
    msg.data = cmd
    publisher.publish(msg)
