import logging
import functools

from ..main_node import subscribe
from ..gazebo.gz_msgs.driver_station_pb2 import DriverStation
from ..gazebo.gz_msgs.joystick_pb2 import Joystick 

import hal
from hal_impl.data import hal_data
from hal_impl import mode_helpers

logger = logging.getLogger(__name__)

class DriverStationControl:

    def __init__(self):

        subscribe('ds/state', DriverStation, self.on_state)

        for i in range(6):
            subscribe('ds/joysticks/%s' % i,
                      Joystick,
                      functools.partial(self.on_joystick, i))

        self.state = None
        self.enabled = None
        hal_data["control"]['has_source'] = True

    def on_joystick(self, idx, msg: Joystick):
        
        logger.info("joystick! %s", msg)
        js = hal_data['joysticks'][idx]
        buttons = js['buttons']
        axes = js['axes']
        js['has_source'] = True
        
        # super inefficient, but could be worse..
        # -> probably will be bit by race conditions here 
        for i, (a, _) in enumerate(zip(msg.axes, axes)):
            axes[i] = a
            
        for i, (b, _) in enumerate(zip(msg.buttons, buttons)):
            buttons[i] = b

        mode_helpers.notify_new_ds_data()

    def on_state(self, msg: DriverStation):
        
        logger.info("on state: %s", msg)
        if self.state != msg.state or self.enabled != msg.enabled:
            
            if msg.state == DriverStation.TEST:
                mode_helpers.set_test_mode(msg.enabled)
            elif msg.state == DriverStation.AUTO:
                mode_helpers.set_autonomous(msg.enabled)
            elif msg.state == DriverStation.TELEOP:
                mode_helpers.set_teleop_mode(msg.enabled)
            
            self.state = msg.state
            self.enabled = msg.enabled
    
