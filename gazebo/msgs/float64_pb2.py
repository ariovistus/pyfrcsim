# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: float64.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='float64.proto',
  package='gazebo.msgs',
  serialized_pb='\n\rfloat64.proto\x12\x0bgazebo.msgs\"\x17\n\x07\x46loat64\x12\x0c\n\x04\x64\x61ta\x18\x01 \x02(\x01\x42\x0b\x42\tGzFloat64')




_FLOAT64 = _descriptor.Descriptor(
  name='Float64',
  full_name='gazebo.msgs.Float64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='gazebo.msgs.Float64.data', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=30,
  serialized_end=53,
)

DESCRIPTOR.message_types_by_name['Float64'] = _FLOAT64

class Float64(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FLOAT64

  # @@protoc_insertion_point(class_scope:gazebo.msgs.Float64)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'B\tGzFloat64')
# @@protoc_insertion_point(module_scope)