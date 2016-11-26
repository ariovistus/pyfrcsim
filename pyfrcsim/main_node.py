from google.protobuf.message import (
    Message,
)
from .gazebo.transport import (
    Node,
    Publisher,
    Subscriber,
)

_main_node = None


def _check_main_node():
    global _main_node
    if _main_node is None:
        raise Exception("MainNode.openGazeboConnection() should have already been "
        + "called by RobotBase.main()!")


def open_gazebo_connection(host: str, port: int):
    global _main_node
    _main_node = Node("frc")
    _main_node.wait_for_connection(host, port);


def close_gazebo_connection():
    global _main_node
    _check_main_node()
    _main_node.server.close()


def advertise(topic: str, message_class: Message) -> Publisher:
    global _main_node
    _check_main_node()
    return _main_node.advertise(topic, message_class)
    

def subscribe(topic: str, message_class: Message, callback: "(Message) -> None") -> Subscriber:
    global _main_node
    _check_main_node()
    return _main_node.subscribe(topic, message_class, callback)
    
