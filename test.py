# instructions: start gazebo. then run this.
# then watch for exceptions.
from pyfrcsim.main_node import (
    open_gazebo_connection,
    advertise,
    subscribe,
)
from pyfrcsim.gazebo.msgs.gz_string_pb2 import GzString

import logging

logging.basicConfig(level=logging.DEBUG)

open_gazebo_connection()
advertise("tacos", GzString)

def callback(_more_tacos):
    pass

subscribe("/gazebo/default/GearsBot/leftFinger/leftFingerContact/contacts", GzString, callback)
print ("tacos!")
