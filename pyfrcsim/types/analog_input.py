import logging

from ..main_node import subscribe
from ..gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)

class SimAnalogInput:

    def __init__(self, channel, analog_dict):
        self.analog_dict = analog_dict
        subscribe('simulator/analog/%s' % channel, Float64, self.on_message)
        analog_dict["has_source"] = True
        logger.info("Registered analog input device on channel %s", channel)

    def on_message(self, msg: Float64):
        self.analog_dict['voltage'] = msg.data
        self.analog_dict['avg_voltage'] = msg.data
        
        
