# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bool.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bool.proto',
  package='gazebo.msgs',
  syntax='proto2',
  serialized_pb=_b('\n\nbool.proto\x12\x0bgazebo.msgs\"\x14\n\x04\x42ool\x12\x0c\n\x04\x64\x61ta\x18\x01 \x02(\x08\x42\x08\x42\x06GzBool')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BOOL = _descriptor.Descriptor(
  name='Bool',
  full_name='gazebo.msgs.Bool',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='gazebo.msgs.Bool.data', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=47,
)

DESCRIPTOR.message_types_by_name['Bool'] = _BOOL

Bool = _reflection.GeneratedProtocolMessageType('Bool', (_message.Message,), dict(
  DESCRIPTOR = _BOOL,
  __module__ = 'bool_pb2'
  # @@protoc_insertion_point(class_scope:gazebo.msgs.Bool)
  ))
_sym_db.RegisterMessage(Bool)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\006GzBool'))
# @@protoc_insertion_point(module_scope)
