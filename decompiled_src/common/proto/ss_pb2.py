#Embedded file name: I:/bag/tmp/tw2/res/entities\common\proto/ss_pb2.o
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='ss.proto', package='gt.ss', serialized_pb="\nss.protogt.sscommon.proto\"L\nStubMsg\nfromHost (\ntoHost (\r\neName (\nfuncArgs (\"�\n	EntityMsg\nfromHost (\ntoHost (\nbox (\r\neName ($\neCom (2.gt.ss.Component:BASE\nfuncArgs (\"!\nHost\nname (\ncid (*+\n	Component\nBASE \nCELL\n\nCLIENT2�\n\rServerService!\nrecvHost.gt.ss.Host.gt.Void(\ntransStubMsg.gt.ss.StubMsg.gt.Void,\ntransEntityMsg.gt.ss.EntityMsg.gt.Void2e\n\rClientService\'\nrecvStubMsg.gt.ss.StubMsg.gt.Void+\n\rrecvEntityMsg.gt.ss.EntityMsg.gt.VoidB��")
_COMPONENT = _descriptor.EnumDescriptor(name='Component', full_name='gt.ss.Component', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='BASE', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='CELL', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='CLIENT', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=278, serialized_end=321)
Component = enum_type_wrapper.EnumTypeWrapper(_COMPONENT)
BASE = 0
CELL = 1
CLIENT = 2
_STUBMSG = _descriptor.Descriptor(name='StubMsg', full_name='gt.ss.StubMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='fromHost', full_name='gt.ss.StubMsg.fromHost', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='toHost', full_name='gt.ss.StubMsg.toHost', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='eName', full_name='gt.ss.StubMsg.eName', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='funcArgs', full_name='gt.ss.StubMsg.funcArgs', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=33, serialized_end=109)
_ENTITYMSG = _descriptor.Descriptor(name='EntityMsg', full_name='gt.ss.EntityMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='fromHost', full_name='gt.ss.EntityMsg.fromHost', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='toHost', full_name='gt.ss.EntityMsg.toHost', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='box', full_name='gt.ss.EntityMsg.box', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='eName', full_name='gt.ss.EntityMsg.eName', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='eCom', full_name='gt.ss.EntityMsg.eCom', index=4, number=5, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='funcArgs', full_name='gt.ss.EntityMsg.funcArgs', index=5, number=6, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=112, serialized_end=241)
_HOST = _descriptor.Descriptor(name='Host', full_name='gt.ss.Host', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='name', full_name='gt.ss.Host.name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='cid', full_name='gt.ss.Host.cid', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=243, serialized_end=276)
_ENTITYMSG.fields_by_name['eCom'].enum_type = _COMPONENT
DESCRIPTOR.message_types_by_name['StubMsg'] = _STUBMSG
DESCRIPTOR.message_types_by_name['EntityMsg'] = _ENTITYMSG
DESCRIPTOR.message_types_by_name['Host'] = _HOST

class StubMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STUBMSG


class EntityMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ENTITYMSG


class Host(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _HOST


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '��')
_SERVERSERVICE = _descriptor.ServiceDescriptor(name='ServerService', full_name='gt.ss.ServerService', file=DESCRIPTOR, index=0, options=None, serialized_start=324, serialized_end=462, methods=[_descriptor.MethodDescriptor(name='recvHost', full_name='gt.ss.ServerService.recvHost', index=0, containing_service=None, input_type=_HOST, output_type=common_pb2._VOID, options=None), _descriptor.MethodDescriptor(name='transStubMsg', full_name='gt.ss.ServerService.transStubMsg', index=1, containing_service=None, input_type=_STUBMSG, output_type=common_pb2._VOID, options=None), _descriptor.MethodDescriptor(name='transEntityMsg', full_name='gt.ss.ServerService.transEntityMsg', index=2, containing_service=None, input_type=_ENTITYMSG, output_type=common_pb2._VOID, options=None)])

class ServerService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _SERVERSERVICE


class ServerService_Stub(ServerService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _SERVERSERVICE


_CLIENTSERVICE = _descriptor.ServiceDescriptor(name='ClientService', full_name='gt.ss.ClientService', file=DESCRIPTOR, index=1, options=None, serialized_start=464, serialized_end=565, methods=[_descriptor.MethodDescriptor(name='recvStubMsg', full_name='gt.ss.ClientService.recvStubMsg', index=0, containing_service=None, input_type=_STUBMSG, output_type=common_pb2._VOID, options=None), _descriptor.MethodDescriptor(name='recvEntityMsg', full_name='gt.ss.ClientService.recvEntityMsg', index=1, containing_service=None, input_type=_ENTITYMSG, output_type=common_pb2._VOID, options=None)])

class ClientService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _CLIENTSERVICE


class ClientService_Stub(ClientService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _CLIENTSERVICE
