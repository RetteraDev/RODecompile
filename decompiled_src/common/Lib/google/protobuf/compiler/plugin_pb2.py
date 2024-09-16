#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf\compiler/plugin_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
import google.protobuf.descriptor_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/compiler/plugin.proto', package='google.protobuf.compiler', serialized_pb='\n%google/protobuf/compiler/plugin.protogoogle.protobuf.compiler google/protobuf/descriptor.proto\"}\nCodeGeneratorRequest\nfile_to_generate (	\n	parameter (	8\n\nproto_file (2$.google.protobuf.FileDescriptorProto\"ª\nCodeGeneratorResponse\r\nerror (	B\nfile (24.google.protobuf.compiler.CodeGeneratorResponse.File>\nFile\nname (	\ninsertion_point (	\ncontent (	B,\ncom.google.protobuf.compilerBPluginProtos')
_CODEGENERATORREQUEST = _descriptor.Descriptor(name='CodeGeneratorRequest', full_name='google.protobuf.compiler.CodeGeneratorRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='file_to_generate', full_name='google.protobuf.compiler.CodeGeneratorRequest.file_to_generate', index=0, number=1, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='parameter', full_name='google.protobuf.compiler.CodeGeneratorRequest.parameter', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=unicode('', 'utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='proto_file', full_name='google.protobuf.compiler.CodeGeneratorRequest.proto_file', index=2, number=15, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=101, serialized_end=226)
_CODEGENERATORRESPONSE_FILE = _descriptor.Descriptor(name='File', full_name='google.protobuf.compiler.CodeGeneratorResponse.File', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='name', full_name='google.protobuf.compiler.CodeGeneratorResponse.File.name', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=unicode('', 'utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='insertion_point', full_name='google.protobuf.compiler.CodeGeneratorResponse.File.insertion_point', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=unicode('', 'utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='content', full_name='google.protobuf.compiler.CodeGeneratorResponse.File.content', index=2, number=15, type=9, cpp_type=9, label=1, has_default_value=False, default_value=unicode('', 'utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=337, serialized_end=399)
_CODEGENERATORRESPONSE = _descriptor.Descriptor(name='CodeGeneratorResponse', full_name='google.protobuf.compiler.CodeGeneratorResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='error', full_name='google.protobuf.compiler.CodeGeneratorResponse.error', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=unicode('', 'utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='file', full_name='google.protobuf.compiler.CodeGeneratorResponse.file', index=1, number=15, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[_CODEGENERATORRESPONSE_FILE], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=229, serialized_end=399)
_CODEGENERATORREQUEST.fields_by_name['proto_file'].message_type = google.protobuf.descriptor_pb2._FILEDESCRIPTORPROTO
_CODEGENERATORRESPONSE_FILE.containing_type = _CODEGENERATORRESPONSE
_CODEGENERATORRESPONSE.fields_by_name['file'].message_type = _CODEGENERATORRESPONSE_FILE
DESCRIPTOR.message_types_by_name['CodeGeneratorRequest'] = _CODEGENERATORREQUEST
DESCRIPTOR.message_types_by_name['CodeGeneratorResponse'] = _CODEGENERATORRESPONSE

class CodeGeneratorRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CODEGENERATORREQUEST


class CodeGeneratorResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class File(_message.Message):
        __metaclass__ = _reflection.GeneratedProtocolMessageType
        DESCRIPTOR = _CODEGENERATORRESPONSE_FILE

    DESCRIPTOR = _CODEGENERATORRESPONSE


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\ncom.google.protobuf.compilerBPluginProtos')
