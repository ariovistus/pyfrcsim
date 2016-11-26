import logging

from ..main_node import advertise
from ..gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)

class SimRelay:

    def __init__(self, channel, relay_dict):
        
        self.relay_dict = relay_dict
        self.publisher = advertise('simulator/relay/%s' % channel, Float64)
        
        logger.info("Registered relay device on channel %s", channel)
        relay_dict.register('fwd', self.on_value_changed, notify=True)
        relay_dict.register('rev', self.on_value_changed, notify=True)


    def on_value_changed(self, key, value):
        
        value = 0.0
        if self.relay_dict['fwd']:
            value += 1.0
        if self.relay_dict['rev']:
            value += -1.0
        
        msg = Float64()
        msg.data = value
        self.publisher.publish(msg)

