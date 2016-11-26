# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: subscribe.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='subscribe.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x0fsubscribe.proto\x12\x0bgazebo.msgs\"a\n\tSubscribe\x12\r\n\x05topic\x18\x01 \x02(\t\x12\x0c\n\x04host\x18\x02 \x02(\t\x12\x0c\n\x04port\x18\x03 \x02(\r\x12\x10\n\x08msg_type\x18\x04 \x02(\t\x12\x17\n\x08latching\x18\x05 \x01(\x08:\x05\x66\x61lse')




_SUBSCRIBE = _descriptor.Descriptor(
  name='Subscribe',
  full_name='gazebo.msgs.Subscribe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='gazebo.msgs.Subscribe.topic', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='host', full_name='gazebo.msgs.Subscribe.host', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='port', full_name='gazebo.msgs.Subscribe.port', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg_type', full_name='gazebo.msgs.Subscribe.msg_type', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latching', full_name='gazebo.msgs.Subscribe.latching', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=32,
  serialized_end=129,
)

DESCRIPTOR.message_types_by_name['Subscribe'] = _SUBSCRIBE

class Subscribe(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SUBSCRIBE

  # @@protoc_insertion_point(class_scope:gazebo.msgs.Subscribe)


# @@protoc_insertion_point(module_scope)
