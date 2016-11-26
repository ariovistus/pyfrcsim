ODIR=../gazebo/msgs
OUTPUTS1=bool_pb2.py driver_station_pb2.py float64_pb2.py frc_joystick_pb2.py

# prepent output dir to each output file
OUTPUTS=$(OUTPUTS1:%=$(ODIR)/%)

all: $(OUTPUTS) 
	

clean:
	$(foreach ous, $(OUTPUTS), rm -f $(ous))

$(ODIR):
	mkdir -p $@

$(ODIR)/bool_pb2.py: $(ODIR)
	protoc --python_out=$(ODIR) bool.proto

$(ODIR)/driver_station_pb2.py: $(ODIR)
	protoc --python_out=$(ODIR) driver-station.proto

$(ODIR)/float64_pb2.py: $(ODIR)
	protoc --python_out=$(ODIR) float64.proto

$(ODIR)/frc_joystick_pb2.py: $(ODIR)
	protoc --python_out=$(ODIR) frc_joystick.proto
