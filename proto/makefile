# v 2.5.0 is no good, 3.0.0 seems ok
PROTOC = ~/Downloads/bin/protoc
ODIR1=../pyfrcsim/gazebo/gz_msgs
ODIR2=../pyfrcsim/gazebo/msgs
# these seem to have come from frcsim
OUTPUTS1=bool_pb2.py driver_station_pb2.py float64_pb2.py frc_joystick_pb2.py 
# these seem to have come from gazebo
OUTPUTS2=packet_pb2.py publish_pb2.py publishers_pb2.py subscribe_pb2.py time_pb2.py gz_string_pb2.py gz_string_v_pb2.py time_pb2.py

# prepent output dir to each output file
OUTPUTS=$(OUTPUTS1:%=$(ODIR1)/%) $(OUTPUTS2:%=$(ODIR2)/%)

all: $(OUTPUTS) 
	

clean:
	$(foreach ous, $(OUTPUTS), rm -f $(ous))

$(ODIR1):
	mkdir -p $@

$(ODIR2):
	mkdir -p $@

$(ODIR1)/bool_pb2.py: $(ODIR1)
	$(PROTOC) --python_out=$(ODIR1) bool.proto


$(ODIR1)/driver_station_pb2.py: $(ODIR1)
	$(PROTOC) --python_out=$(ODIR1) driver-station.proto

$(ODIR1)/float64_pb2.py: $(ODIR1)
	$(PROTOC) --python_out=$(ODIR1) float64.proto

$(ODIR1)/frc_joystick_pb2.py: $(ODIR1)
	$(PROTOC) --python_out=$(ODIR1) frc_joystick.proto

$(ODIR2)/packet_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) packet.proto -I.
	# stinking protobuf doesn't have an option to change this for python
	# todo: revisit this with protobuf3
	sed -i 's/time_pb2/pyfrcsim.gazebo.msgs.time_pb2/' $@

$(ODIR2)/publish_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) publish.proto

$(ODIR2)/publishers_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) publishers.proto
	sed -i 's/publish_pb2/pyfrcsim.gazebo.msgs.publish_pb2/' $@

$(ODIR2)/subscribe_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) subscribe.proto

$(ODIR2)/time_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) time.proto

$(ODIR2)/gz_string_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) gz_string.proto

$(ODIR2)/gz_string_v_pb2.py: $(ODIR2)
	$(PROTOC) --python_out=$(ODIR2) gz_string_v.proto
