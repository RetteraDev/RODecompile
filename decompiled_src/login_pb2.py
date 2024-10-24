#Embedded file name: /WORKSPACE/data/entities/common/proto/login_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='login.proto', package='gt.login', serialized_pb="\nlogin.protogt.logincommon.proto\"R\nLogonRequest\nusername (\npassword (\r\ncdkey (\nrandkey (\"V\nFeihuoLogonRequest\nusername (\ncookie (\r\ncdkey (\nrandkey (\"/\nYiyouLogonRequest\nuid (\r\ntoken (\"/\nTokenLogonRequest\nuid (\r\ntoken (\"�\n\nLogonReply;\ntype (2.gt.login.LogonReply.ReplyType:\rNEED_PASSWORD\nmessage (\r\nurs (: \n\nrecheckkey (: \"�\n	ReplyType\n\rNEED_PASSWORD \nWAITING\nPASSWORD_ERR\r\n	NEED_EKEY\nEKEY_ERR\nNEED_MIMAKA\n\nMIMAKA_ERR\nLOGINED\nMOBILE_MIMA_WARNING\nLOGIN_RESPONSE_HACK	\n\nCOOKIE_ERR\n\nCOOKIE_TIMEOUT\nFEIHUO_LOGINED\r\r\n	YIYOU_ERR\n\rYIYOU_LOGINED\nREAL_NAME_PASS\nREAL_NAME_WAIT\nREAL_NAME_NO\nREAL_NAME_FAIL\nPLATFORM_REAL_NAME_FAIL\"\nEkeyRequest\nkey (\"\n\rMimakaRequest\nkey (\" \nQueryRequest\nusername (\"�\nLogonQueryReply\nuuid (\nserver_uuid (1\nreply (2\".gt.login.LogonQueryReply.ReplyVal+\nReplyVal\nserver (\nusernum (\"/\nLogonRandKey\nserver (\nrandkey (\".\nFetchKeyResponse\nskey (\nrkey (\"\nFetchKeyRequest\nrkey (\"\"\nRegRoleRequest\nroleName (\"#\nUnregRoleRequest\nusrname (\"5\nQueryUrsRequest\nusername (\npassword (\"I\nQueryUrsResponse\nusername (#\nreply (2.gt.login.LogonReply\" \nQRCodeResponse\nqrcode (\" \n\rQRCodeRequest\nrandkey (\"\nFinishRealNameRequest2�\nLoginService)\nLogon.gt.login.LogonRequest.gt.Void\'\nEkey.gt.login.EkeyRequest.gt.Void+\nMimaka.gt.login.MimakaRequest.gt.Void-\n	QueryUser.gt.login.QueryRequest.gt.Void/\nFetchKey.gt.login.FetchKeyRequest.gt.Void-\nregRole.gt.login.RegRoleRequest.gt.Void1\n	unregRole.gt.login.UnregRoleRequest.gt.Void/\nQueryUrs.gt.login.QueryUrsRequest.gt.Void+\nQRCode.gt.login.QRCodeRequest.gt.Void\"\nQRCodeCancel.gt.Void.gt.Void5\nFeihuoLogon.gt.login.FeihuoLogonRequest.gt.Void3\n\nYiyouLogon.gt.login.YiyouLogonRequest.gt.Void7\nLogonByMRToken.gt.login.TokenLogonRequest.gt.Void7\nLogonByEUToken.gt.login.TokenLogonRequest.gt.Void;\nFinishRealName.gt.login.FinishRealNameRequest.gt.Void2�\nLoginClient\'\nReply.gt.login.LogonReply.gt.Void1\n\nQueryReply.gt.login.LogonQueryReply.gt.Void4\nLogonKeyToClient.gt.login.LogonRandKey.gt.Void2\n\nOnFetchKey.gt.login.FetchKeyResponse.gt.Void2\n\nOnQueryUrs.gt.login.QueryUrsResponse.gt.Void.\nOnQRCode.gt.login.QRCodeResponse.gt.VoidB��")
_LOGONREPLY_REPLYTYPE = _descriptor.EnumDescriptor(name='ReplyType', full_name='gt.login.LogonReply.ReplyType', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NEED_PASSWORD', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='WAITING', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PASSWORD_ERR', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NEED_EKEY', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='EKEY_ERR', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NEED_MIMAKA', index=5, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MIMAKA_ERR', index=6, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='LOGINED', index=7, number=7, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MOBILE_MIMA_WARNING', index=8, number=8, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='LOGIN_RESPONSE_HACK', index=9, number=9, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='COOKIE_ERR', index=10, number=10, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='COOKIE_TIMEOUT', index=11, number=11, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FEIHUO_LOGINED', index=12, number=13, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='YIYOU_ERR', index=13, number=14, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='YIYOU_LOGINED', index=14, number=15, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='REAL_NAME_PASS', index=15, number=16, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='REAL_NAME_WAIT', index=16, number=17, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='REAL_NAME_NO', index=17, number=18, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='REAL_NAME_FAIL', index=18, number=19, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PLATFORM_REAL_NAME_FAIL', index=19, number=20, options=None, type=None)], containing_type=None, options=None, serialized_start=440, serialized_end=823)
_LOGONREQUEST = _descriptor.Descriptor(name='LogonRequest', full_name='gt.login.LogonRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='username', full_name='gt.login.LogonRequest.username', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='password', full_name='gt.login.LogonRequest.password', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cdkey', full_name='gt.login.LogonRequest.cdkey', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='randkey', full_name='gt.login.LogonRequest.randkey', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=39, serialized_end=121)
_FEIHUOLOGONREQUEST = _descriptor.Descriptor(name='FeihuoLogonRequest', full_name='gt.login.FeihuoLogonRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='username', full_name='gt.login.FeihuoLogonRequest.username', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cookie', full_name='gt.login.FeihuoLogonRequest.cookie', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cdkey', full_name='gt.login.FeihuoLogonRequest.cdkey', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='randkey', full_name='gt.login.FeihuoLogonRequest.randkey', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=123, serialized_end=209)
_YIYOULOGONREQUEST = _descriptor.Descriptor(name='YiyouLogonRequest', full_name='gt.login.YiyouLogonRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uid', full_name='gt.login.YiyouLogonRequest.uid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='token', full_name='gt.login.YiyouLogonRequest.token', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=211, serialized_end=258)
_TOKENLOGONREQUEST = _descriptor.Descriptor(name='TokenLogonRequest', full_name='gt.login.TokenLogonRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uid', full_name='gt.login.TokenLogonRequest.uid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='token', full_name='gt.login.TokenLogonRequest.token', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=260, serialized_end=307)
_LOGONREPLY = _descriptor.Descriptor(name='LogonReply', full_name='gt.login.LogonReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='type', full_name='gt.login.LogonReply.type', index=0, number=1, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='message', full_name='gt.login.LogonReply.message', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='urs', full_name='gt.login.LogonReply.urs', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=True, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='recheckkey', full_name='gt.login.LogonReply.recheckkey', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=True, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_LOGONREPLY_REPLYTYPE], options=None, is_extendable=False, extension_ranges=[], serialized_start=310, serialized_end=823)
_EKEYREQUEST = _descriptor.Descriptor(name='EkeyRequest', full_name='gt.login.EkeyRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='key', full_name='gt.login.EkeyRequest.key', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=825, serialized_end=851)
_MIMAKAREQUEST = _descriptor.Descriptor(name='MimakaRequest', full_name='gt.login.MimakaRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='key', full_name='gt.login.MimakaRequest.key', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=853, serialized_end=881)
_QUERYREQUEST = _descriptor.Descriptor(name='QueryRequest', full_name='gt.login.QueryRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='username', full_name='gt.login.QueryRequest.username', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=883, serialized_end=915)
_LOGONQUERYREPLY_REPLYVAL = _descriptor.Descriptor(name='ReplyVal', full_name='gt.login.LogonQueryReply.ReplyVal', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.LogonQueryReply.ReplyVal.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='usernum', full_name='gt.login.LogonQueryReply.ReplyVal.usernum', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1023, serialized_end=1066)
_LOGONQUERYREPLY = _descriptor.Descriptor(name='LogonQueryReply', full_name='gt.login.LogonQueryReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.login.LogonQueryReply.uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='server_uuid', full_name='gt.login.LogonQueryReply.server_uuid', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reply', full_name='gt.login.LogonQueryReply.reply', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[_LOGONQUERYREPLY_REPLYVAL], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=918, serialized_end=1066)
_LOGONRANDKEY = _descriptor.Descriptor(name='LogonRandKey', full_name='gt.login.LogonRandKey', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.LogonRandKey.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='randkey', full_name='gt.login.LogonRandKey.randkey', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1068, serialized_end=1115)
_FETCHKEYRESPONSE = _descriptor.Descriptor(name='FetchKeyResponse', full_name='gt.login.FetchKeyResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='skey', full_name='gt.login.FetchKeyResponse.skey', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='rkey', full_name='gt.login.FetchKeyResponse.rkey', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1117, serialized_end=1163)
_FETCHKEYREQUEST = _descriptor.Descriptor(name='FetchKeyRequest', full_name='gt.login.FetchKeyRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='rkey', full_name='gt.login.FetchKeyRequest.rkey', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1165, serialized_end=1196)
_REGROLEREQUEST = _descriptor.Descriptor(name='RegRoleRequest', full_name='gt.login.RegRoleRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='roleName', full_name='gt.login.RegRoleRequest.roleName', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1198, serialized_end=1232)
_UNREGROLEREQUEST = _descriptor.Descriptor(name='UnregRoleRequest', full_name='gt.login.UnregRoleRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='usrname', full_name='gt.login.UnregRoleRequest.usrname', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1234, serialized_end=1269)
_QUERYURSREQUEST = _descriptor.Descriptor(name='QueryUrsRequest', full_name='gt.login.QueryUrsRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='username', full_name='gt.login.QueryUrsRequest.username', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='password', full_name='gt.login.QueryUrsRequest.password', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1271, serialized_end=1324)
_QUERYURSRESPONSE = _descriptor.Descriptor(name='QueryUrsResponse', full_name='gt.login.QueryUrsResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='username', full_name='gt.login.QueryUrsResponse.username', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reply', full_name='gt.login.QueryUrsResponse.reply', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1326, serialized_end=1399)
_QRCODERESPONSE = _descriptor.Descriptor(name='QRCodeResponse', full_name='gt.login.QRCodeResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='qrcode', full_name='gt.login.QRCodeResponse.qrcode', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1401, serialized_end=1433)
_QRCODEREQUEST = _descriptor.Descriptor(name='QRCodeRequest', full_name='gt.login.QRCodeRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='randkey', full_name='gt.login.QRCodeRequest.randkey', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1435, serialized_end=1467)
_FINISHREALNAMEREQUEST = _descriptor.Descriptor(name='FinishRealNameRequest', full_name='gt.login.FinishRealNameRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1469, serialized_end=1492)
_LOGONREPLY.fields_by_name['type'].enum_type = _LOGONREPLY_REPLYTYPE
_LOGONREPLY_REPLYTYPE.containing_type = _LOGONREPLY
_LOGONQUERYREPLY_REPLYVAL.containing_type = _LOGONQUERYREPLY
_LOGONQUERYREPLY.fields_by_name['reply'].message_type = _LOGONQUERYREPLY_REPLYVAL
_QUERYURSRESPONSE.fields_by_name['reply'].message_type = _LOGONREPLY
DESCRIPTOR.message_types_by_name['LogonRequest'] = _LOGONREQUEST
DESCRIPTOR.message_types_by_name['FeihuoLogonRequest'] = _FEIHUOLOGONREQUEST
DESCRIPTOR.message_types_by_name['YiyouLogonRequest'] = _YIYOULOGONREQUEST
DESCRIPTOR.message_types_by_name['TokenLogonRequest'] = _TOKENLOGONREQUEST
DESCRIPTOR.message_types_by_name['LogonReply'] = _LOGONREPLY
DESCRIPTOR.message_types_by_name['EkeyRequest'] = _EKEYREQUEST
DESCRIPTOR.message_types_by_name['MimakaRequest'] = _MIMAKAREQUEST
DESCRIPTOR.message_types_by_name['QueryRequest'] = _QUERYREQUEST
DESCRIPTOR.message_types_by_name['LogonQueryReply'] = _LOGONQUERYREPLY
DESCRIPTOR.message_types_by_name['LogonRandKey'] = _LOGONRANDKEY
DESCRIPTOR.message_types_by_name['FetchKeyResponse'] = _FETCHKEYRESPONSE
DESCRIPTOR.message_types_by_name['FetchKeyRequest'] = _FETCHKEYREQUEST
DESCRIPTOR.message_types_by_name['RegRoleRequest'] = _REGROLEREQUEST
DESCRIPTOR.message_types_by_name['UnregRoleRequest'] = _UNREGROLEREQUEST
DESCRIPTOR.message_types_by_name['QueryUrsRequest'] = _QUERYURSREQUEST
DESCRIPTOR.message_types_by_name['QueryUrsResponse'] = _QUERYURSRESPONSE
DESCRIPTOR.message_types_by_name['QRCodeResponse'] = _QRCODERESPONSE
DESCRIPTOR.message_types_by_name['QRCodeRequest'] = _QRCODEREQUEST
DESCRIPTOR.message_types_by_name['FinishRealNameRequest'] = _FINISHREALNAMEREQUEST

class LogonRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOGONREQUEST


class FeihuoLogonRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FEIHUOLOGONREQUEST


class YiyouLogonRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _YIYOULOGONREQUEST


class TokenLogonRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOKENLOGONREQUEST


class LogonReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOGONREPLY


class EkeyRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _EKEYREQUEST


class MimakaRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MIMAKAREQUEST


class QueryRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYREQUEST


class LogonQueryReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class ReplyVal(_message.Message):
        __metaclass__ = _reflection.GeneratedProtocolMessageType
        DESCRIPTOR = _LOGONQUERYREPLY_REPLYVAL

    DESCRIPTOR = _LOGONQUERYREPLY


class LogonRandKey(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOGONRANDKEY


class FetchKeyResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FETCHKEYRESPONSE


class FetchKeyRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FETCHKEYREQUEST


class RegRoleRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGROLEREQUEST


class UnregRoleRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNREGROLEREQUEST


class QueryUrsRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYURSREQUEST


class QueryUrsResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYURSRESPONSE


class QRCodeResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QRCODERESPONSE


class QRCodeRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QRCODEREQUEST


class FinishRealNameRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FINISHREALNAMEREQUEST


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '��')
_LOGINSERVICE = _descriptor.ServiceDescriptor(name='LoginService', full_name='gt.login.LoginService', file=DESCRIPTOR, index=0, options=None, serialized_start=1495, serialized_end=2245, methods=[_descriptor.MethodDescriptor(name='Logon', full_name='gt.login.LoginService.Logon', index=0, containing_service=None, input_type=_LOGONREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='Ekey', full_name='gt.login.LoginService.Ekey', index=1, containing_service=None, input_type=_EKEYREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='Mimaka', full_name='gt.login.LoginService.Mimaka', index=2, containing_service=None, input_type=_MIMAKAREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QueryUser', full_name='gt.login.LoginService.QueryUser', index=3, containing_service=None, input_type=_QUERYREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='FetchKey', full_name='gt.login.LoginService.FetchKey', index=4, containing_service=None, input_type=_FETCHKEYREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='regRole', full_name='gt.login.LoginService.regRole', index=5, containing_service=None, input_type=_REGROLEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='unregRole', full_name='gt.login.LoginService.unregRole', index=6, containing_service=None, input_type=_UNREGROLEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QueryUrs', full_name='gt.login.LoginService.QueryUrs', index=7, containing_service=None, input_type=_QUERYURSREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QRCode', full_name='gt.login.LoginService.QRCode', index=8, containing_service=None, input_type=_QRCODEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QRCodeCancel', full_name='gt.login.LoginService.QRCodeCancel', index=9, containing_service=None, input_type=common_pb2._VOID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='FeihuoLogon', full_name='gt.login.LoginService.FeihuoLogon', index=10, containing_service=None, input_type=_FEIHUOLOGONREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='YiyouLogon', full_name='gt.login.LoginService.YiyouLogon', index=11, containing_service=None, input_type=_YIYOULOGONREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='LogonByMRToken', full_name='gt.login.LoginService.LogonByMRToken', index=12, containing_service=None, input_type=_TOKENLOGONREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='LogonByEUToken', full_name='gt.login.LoginService.LogonByEUToken', index=13, containing_service=None, input_type=_TOKENLOGONREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='FinishRealName', full_name='gt.login.LoginService.FinishRealName', index=14, containing_service=None, input_type=_FINISHREALNAMEREQUEST, output_type=common_pb2._VOID, options=None)])

class LoginService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _LOGINSERVICE


class LoginService_Stub(LoginService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _LOGINSERVICE


_LOGINCLIENT = _descriptor.ServiceDescriptor(name='LoginClient', full_name='gt.login.LoginClient', file=DESCRIPTOR, index=1, options=None, serialized_start=2248, serialized_end=2559, methods=[_descriptor.MethodDescriptor(name='Reply', full_name='gt.login.LoginClient.Reply', index=0, containing_service=None, input_type=_LOGONREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QueryReply', full_name='gt.login.LoginClient.QueryReply', index=1, containing_service=None, input_type=_LOGONQUERYREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='LogonKeyToClient', full_name='gt.login.LoginClient.LogonKeyToClient', index=2, containing_service=None, input_type=_LOGONRANDKEY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnFetchKey', full_name='gt.login.LoginClient.OnFetchKey', index=3, containing_service=None, input_type=_FETCHKEYRESPONSE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnQueryUrs', full_name='gt.login.LoginClient.OnQueryUrs', index=4, containing_service=None, input_type=_QUERYURSRESPONSE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnQRCode', full_name='gt.login.LoginClient.OnQRCode', index=5, containing_service=None, input_type=_QRCODERESPONSE, output_type=common_pb2._VOID, options=None)])

class LoginClient(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _LOGINCLIENT


class LoginClient_Stub(LoginClient):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _LOGINCLIENT
