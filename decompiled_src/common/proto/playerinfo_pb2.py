#Embedded file name: I:/bag/tmp/tw2/res/entities\common\proto/playerinfo_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='playerinfo.proto', package='gt', serialized_pb='\nplayerinfo.protogt\"™\n\nPlayerInfo\nurs (\n\nservername (\r\nlevel (\ncash (\nrolename (\nposition (\nspaceno (\nprocess (\nmd5	 (\nmac\n (\"V\nChatMessage\r\nctype (\nmsg (\nach_num (\ndate (\nname (BÄê')
_PLAYERINFO = _descriptor.Descriptor(name='PlayerInfo', full_name='gt.PlayerInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.PlayerInfo.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='servername', full_name='gt.PlayerInfo.servername', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='level', full_name='gt.PlayerInfo.level', index=2, number=3, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cash', full_name='gt.PlayerInfo.cash', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='rolename', full_name='gt.PlayerInfo.rolename', index=4, number=5, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='position', full_name='gt.PlayerInfo.position', index=5, number=6, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='spaceno', full_name='gt.PlayerInfo.spaceno', index=6, number=7, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='process', full_name='gt.PlayerInfo.process', index=7, number=8, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='md5', full_name='gt.PlayerInfo.md5', index=8, number=9, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mac', full_name='gt.PlayerInfo.mac', index=9, number=10, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=25, serialized_end=195)
_CHATMESSAGE = _descriptor.Descriptor(name='ChatMessage', full_name='gt.ChatMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='ctype', full_name='gt.ChatMessage.ctype', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.ChatMessage.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='ach_num', full_name='gt.ChatMessage.ach_num', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='date', full_name='gt.ChatMessage.date', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='name', full_name='gt.ChatMessage.name', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=197, serialized_end=283)
DESCRIPTOR.message_types_by_name['PlayerInfo'] = _PLAYERINFO
DESCRIPTOR.message_types_by_name['ChatMessage'] = _CHATMESSAGE

class PlayerInfo(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFO


class ChatMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CHATMESSAGE


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'Äê')
