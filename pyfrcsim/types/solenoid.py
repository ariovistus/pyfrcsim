import logging

from ..main_node import advertise
from ..gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)

class SimSolenoid:

    def __init__(self, channel, solenoid_dict):
        
        self.publisher = advertise(
            'simulator/pneumatic/%s/%s' % (0, channel), 
            Float64)
        
        logger.info("Registered solenoid device on channel %s", channel)
        solenoid_dict.register('value', self.on_value_changed, notify=True)

    def on_value_changed(self, key, value):
        
        msg = Float64()
        msg.data = 1.0 if value else -1.0
        self.publisher.publish(msg)

