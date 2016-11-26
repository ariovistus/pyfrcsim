from gazebo.transport.msgs import theFloat
from gazebo.transport import Float64
from main_node import subscribe


class SimFloatInput:
    def __init__(self, topic: str):
        self.value = float("NaN")

        def callback(msg: Float64):
            self.value = msg.getData()

        subscribe(topic, theFloat(), callback)

    def get(self):
        return self.value

