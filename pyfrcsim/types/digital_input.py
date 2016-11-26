import logging

from ..main_node import subscribe
from ..gazebo.gz_msgs.bool_pb2 import Bool

logger = logging.getLogger(__name__)

class SimDigitalInput:

    def __init__(self, channel, digital_dict):
        self.digital_dict = digital_dict
        subscribe('simulator/dio/%s' % channel, Bool, self.on_message)
        digital_dict["has_source"] = True
        logger.info("Registered digital input device on channel %s", channel)

    def on_message(self, msg: Bool):
        self.digital_dict['value'] = msg.data
