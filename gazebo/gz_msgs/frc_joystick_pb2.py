# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: frc_joystick.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='frc_joystick.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x12\x66rc_joystick.proto\x12\x0bgazebo.msgs\",\n\x0b\x46RCJoystick\x12\x0c\n\x04\x61xes\x18\x01 \x03(\x01\x12\x0f\n\x07\x62uttons\x18\x02 \x03(\x08\x42\x0f\x42\rGzFRCJoystick')




_FRCJOYSTICK = _descriptor.Descriptor(
  name='FRCJoystick',
  full_name='gazebo.msgs.FRCJoystick',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='axes', full_name='gazebo.msgs.FRCJoystick.axes', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buttons', full_name='gazebo.msgs.FRCJoystick.buttons', index=1,
      number=2, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=35,
  serialized_end=79,
)

DESCRIPTOR.message_types_by_name['FRCJoystick'] = _FRCJOYSTICK

class FRCJoystick(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FRCJOYSTICK

  # @@protoc_insertion_point(class_scope:gazebo.msgs.FRCJoystick)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'B\rGzFRCJoystick')
# @@protoc_insertion_point(module_scope)