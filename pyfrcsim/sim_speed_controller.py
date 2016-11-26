from gazebo.transport.msgs import (
    theFloat,
    makeFloat,
)
from gazebo.transport import Float64
from main_node import advertise


class SimSpeedController:
    def __init__(self, topic: str):
        self.value = 0.0

        self.pub = advertise(topic, theFloat())

    def get(self) -> float:
        return self.value

    def set(self, value: float):
        self.value = float(value)
        self.pub.publish(makeFloat)

    def disable(self):
        self.set(0.0)

    def pidWrite(output: float):
        self.set(output)

