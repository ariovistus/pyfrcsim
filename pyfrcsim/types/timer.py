import logging
import threading

from ..main_node import subscribe
from ..gazebo.gz_msgs.float64_pb2 import Float64

logger = logging.getLogger(__name__)

class Timer:

    def __init__(self):

        self.cond = threading.Condition()
        subscribe('time', Float64, self.on_time)

        # wait for time before returning
        logger.info("Waiting for first timestamp from gazebo")
        
        with self.cond:
            self.cond.wait()
            
        logger.info("Time acquired (simulation time is %s)", self.simTime)

    def on_time(self, msg: Float64):
        with self.cond:
            self.simTime = msg.data 
            self.cond.notify_all()

    def wait(self, seconds):

        start = self.simTime

        while self.simTime - start < seconds:
            with self.cond:
                self.cond.wait()

