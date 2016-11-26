import logging
from ..main_node import advertise
from ..gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)


class SimPWM:

    def __init__(self, channel, pwm_dict):
        
        self.publisher = advertise('simulator/pwm/%s' % channel, Float64)
        
        logger.info("Registered PWM device on channel %s", channel)
        pwm_dict.register('value', self.on_value_changed, notify=True)
        

    def on_value_changed(self, key, value):
        msg = Float64()
        msg.data = value
        self.publisher.publish(msg)

