import logging

from .types.driverstation import DriverStationControl
from .types.analog_input import SimAnalogInput
from .types.digital_input import SimDigitalInput
from .types.pwm import SimPWM
from .types.relay import SimRelay
from .types.solenoid import SimSolenoid
from .types.timer import Timer
from .main_node import (
    open_gazebo_connection,
    close_gazebo_connection,
)

from .hal_hooks import GazeboSimHooks

from hal_impl import data, functions

class FrcSimMain:
    '''
        Connects robot code to gazebo simulator
    '''
    
    def __init__(self, parser):
        parser.add_argument('--host', default='127.0.0.1',
                            help='Hostname of gazebo')
        parser.add_argument('--port', default=11345,
                            help='Port to connect to')
        parser.add_argument('--log', default='ERROR', choices=logging._nameToLevel.keys(),
                            help='set loglevel')
        
        # cache of various devices
        self.devices = {}
    
    def _create_cb(self, typename, i, d, thing_cls):
        # typename: name of object
        # i: channel of object
        # d: dictionary
        # thing_cls: class to create when initialized
        
        self.devices.setdefault(typename, {})
        
        def _cb(k, v):
            # don't initialize the device twice
            # -> TODO: destroy device when freed
            if v and i not in self.devices[typename]:
                self.devices[typename][i] = thing_cls(i, d)
        
        return _cb
    
    def run(self, options, robot_class, **static_options):
        logging.basicConfig(level=getattr(logging, options.log.upper(), logging.ERROR))

        # Connect to the simulator
        open_gazebo_connection(options.host, options.port)
        
        try:
        
            # setup the HAL hooks
            
            # setup various control objects
            self.ds = DriverStationControl()
            self.tm = Timer()
            
            # HAL Hooks
            self.hal_hooks = GazeboSimHooks(self.tm)
            functions.hooks = self.hal_hooks
            data.reset_hal_data(functions.hooks)
            
            # Analog
            for i, d in enumerate(data.hal_data['analog_in']):
                d.register('initialized', self._create_cb('analog', i, d, SimAnalogInput))
            
            # Digital
            for i, d in enumerate(data.hal_data['dio']):
                d.register('initialized', self._create_cb('dio', i, d, SimDigitalInput))
            
            
            # Encoders
            
            # Gyro
            
            # PWM
            for i, d in enumerate(data.hal_data['pwm']):
                d.register('initialized', self._create_cb('pwm', i, d, SimPWM))
            
            # Relay
            for i, d in enumerate(data.hal_data['relay']):
                d.register('initialized', self._create_cb('relay', i, d, SimRelay))
            
            # Solenoid
            for i, d in enumerate(data.hal_data['solenoid']):
                d.register('initialized', self._create_cb('solenoid', i, d, SimSolenoid))
            
            return robot_class.main(robot_class)
            
        finally:
            close_gazebo_connection()
