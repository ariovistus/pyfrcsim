from gazebo.transport.msgs import theBool
from gazebo.transport import Bool
from main_node import subscribe


class SimDigitalInput:
    def __init__(self, topic: str):
        self.value = False

        def callback(msg: Bool):
            self.value = msg.getData()

        subscribe(topic, theBool(), callback)

    def get(self):
        return self.value

