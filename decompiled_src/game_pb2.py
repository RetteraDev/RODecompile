#Embedded file name: /WORKSPACE/data/entities/common/proto/game_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='game.proto', package='gt.login', serialized_pb="\n\ngame.protogt.logincommon.proto\"-\n\nRegRequest\nserver (\nhostnum (\"\nRegReply\nmgr_uuid (\"A\n\rUrsmapRequest\nserver (\naccount (\nusernum (\"M\nGameRandKey\nserver (\naccount (\nuuid (\nrandkey (\"?\nUrsInfoRequest\nserver (\naccount (\nuuid (\"¿\nUrsInfoReply\naccount (\n	auth_data (\nopt_data (\nppc_data (\nqrcode (\ncookie (\n\rrealname_flag (\nsecu_info_idnum (\nrecharge_sum	 (:0\"0\nKickAccountReq\naccount (\r\ncheck (\":\nClearAccountExceptionReq\naccount (\r\ncheck (\"\nLockRequest\nurs (\",\nLockResponse\nurs (\nprotect (\"0\nRoleRequest\naccount (\nrolename (\"&\nRoleProtectRequest\nrolename (\"#\nOnProtectRequest\naccount (\"C\nSetUserBitmapRequest\naccount (\nkey (\r\r\nvalue (\r\"5\nSetUserBitmapReply\naccount (\nbitmap (\r\"\'\nGetUserBitmapRequest\naccount (\"5\nGetUserBitmapReply\naccount (\nbitmap (\r\"!\nKickConnectionReq\nuuid (\":\nSetUsermapFieldBlobMessage\r\nfield (\r\nvalue (\"9\nSetUsermapFieldIntMessage\r\nfield (\r\nvalue (\"£\nSetUsermapFieldRequest\nurs (\ntag (7\n	str_field (2$.gt.login.SetUsermapFieldBlobMessage6\n	int_field (2#.gt.login.SetUsermapFieldIntMessage\"0\nSetUsermapFieldReply\nurs (\ntag (\"7\nSetUserRechargeRequest\nurs (\nrecharge (\r\"7\nUpdateRealnameFlagRequest\nuuid (\nflag (\"^\nFlowbackBonusSingle\n\nsn (\r\nurs (\nitem_id (\r\nnum (\r\nt_expire (\r\"]\nFlowbackBonusReply\n\nsn (\r\r\nn_del (\r,\nbonus (2.gt.login.FlowbackBonusSingle\"D\nDelFlowbackBonusRequest\n\nsn (\r\nurs (\nitem_ids (\"2\nEnableRealNameCheckRequest\nenable_check (\"\'\nEnableOneAvatarRequest\r\nvalue (\"5\nKickAccountReply\naccount (\nrolename (\"?\nRegRealNameReply\naccount (\nstatus (\n\nid (\":\n\"EnablePlatformRealNameCheckRequest\nenable_check (2¿\n\nGameService+\n	RegServer.gt.login.RegRequest.gt.Void1\nUpdateUrsmap.gt.login.UrsmapRequest.gt.Void1\nGameKeyToLogin.gt.login.GameRandKey.gt.Void2\nFetchUrsInfo.gt.login.UrsInfoRequest.gt.Void3\n\rGmKickAccount.gt.login.KickAccountReq.gt.VoidE\nClearAccountException\".gt.login.ClearAccountExceptionReq.gt.Void,\n	QueryLock.gt.login.LockRequest.gt.Void0\n\rAddOnlineRole.gt.login.RoleRequest.gt.Void0\n\rDelOnlineRole.gt.login.RoleRequest.gt.Void8\nOnSetRoleProtect.gt.login.OnProtectRequest.gt.Void<\nReqSetUserBitmap.gt.login.SetUserBitmapRequest.gt.Void<\nReqGetUserBitmap.gt.login.GetUserBitmapRequest.gt.Void7\nKickConnection.gt.login.KickConnectionReq.gt.Void@\nReqSetUsermapField .gt.login.SetUsermapFieldRequest.gt.Void@\nReqSetUserRecharge .gt.login.SetUserRechargeRequest.gt.VoidC\nUpdateRealnameFlag#.gt.login.UpdateRealnameFlagRequest.gt.VoidE\nEnableRealNameCheck$.gt.login.EnableRealNameCheckRequest.gt.Void=\nEnableOneAvatar .gt.login.EnableOneAvatarRequest.gt.VoidA\nReqAssignFlowbackBonus.gt.login.FlowbackBonusSingle.gt.VoidB\nReqDelFlowbackBonus!.gt.login.DelFlowbackBonusRequest.gt.Void?\nReqListFlowbackBonus.gt.login.FlowbackBonusSingle.gt.VoidU\nEnablePlatformRealNameCheck,.gt.login.EnablePlatformRealNameCheckRequest.gt.Void2…\n\nGameClient.\n\nRcvUrsInfo.gt.login.UrsInfoReply.gt.Void+\nOnRegServer.gt.login.RegReply.gt.Void/\nOnQueryLock.gt.login.LockResponse.gt.Void8\nSetRoleProtect.gt.login.RoleProtectRequest.gt.Void:\nRepSetUserBitmap.gt.login.SetUserBitmapReply.gt.Void:\nRepGetUserBitmap.gt.login.GetUserBitmapReply.gt.Void>\nRepSetUsermapField.gt.login.SetUsermapFieldReply.gt.Void<\nReplyFlowbackBonus.gt.login.FlowbackBonusReply.gt.Void9\nKickServerAccount.gt.login.KickAccountReply.gt.VoidB€")
_REGREQUEST = _descriptor.Descriptor(name='RegRequest', full_name='gt.login.RegRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.RegRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='hostnum', full_name='gt.login.RegRequest.hostnum', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=38, serialized_end=83)
_REGREPLY = _descriptor.Descriptor(name='RegReply', full_name='gt.login.RegReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mgr_uuid', full_name='gt.login.RegReply.mgr_uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=85, serialized_end=113)
_URSMAPREQUEST = _descriptor.Descriptor(name='UrsmapRequest', full_name='gt.login.UrsmapRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.UrsmapRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='account', full_name='gt.login.UrsmapRequest.account', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='usernum', full_name='gt.login.UrsmapRequest.usernum', index=2, number=3, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=115, serialized_end=180)
_GAMERANDKEY = _descriptor.Descriptor(name='GameRandKey', full_name='gt.login.GameRandKey', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.GameRandKey.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='account', full_name='gt.login.GameRandKey.account', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uuid', full_name='gt.login.GameRandKey.uuid', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='randkey', full_name='gt.login.GameRandKey.randkey', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=182, serialized_end=259)
_URSINFOREQUEST = _descriptor.Descriptor(name='UrsInfoRequest', full_name='gt.login.UrsInfoRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.login.UrsInfoRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='account', full_name='gt.login.UrsInfoRequest.account', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='uuid', full_name='gt.login.UrsInfoRequest.uuid', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=261, serialized_end=324)
_URSINFOREPLY = _descriptor.Descriptor(name='UrsInfoReply', full_name='gt.login.UrsInfoReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.UrsInfoReply.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='auth_data', full_name='gt.login.UrsInfoReply.auth_data', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='opt_data', full_name='gt.login.UrsInfoReply.opt_data', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='ppc_data', full_name='gt.login.UrsInfoReply.ppc_data', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='qrcode', full_name='gt.login.UrsInfoReply.qrcode', index=4, number=5, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cookie', full_name='gt.login.UrsInfoReply.cookie', index=5, number=6, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='realname_flag', full_name='gt.login.UrsInfoReply.realname_flag', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='secu_info_idnum', full_name='gt.login.UrsInfoReply.secu_info_idnum', index=7, number=8, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='recharge_sum', full_name='gt.login.UrsInfoReply.recharge_sum', index=8, number=9, type=5, cpp_type=1, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=327, serialized_end=518)
_KICKACCOUNTREQ = _descriptor.Descriptor(name='KickAccountReq', full_name='gt.login.KickAccountReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.KickAccountReq.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='check', full_name='gt.login.KickAccountReq.check', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=520, serialized_end=568)
_CLEARACCOUNTEXCEPTIONREQ = _descriptor.Descriptor(name='ClearAccountExceptionReq', full_name='gt.login.ClearAccountExceptionReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.ClearAccountExceptionReq.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='check', full_name='gt.login.ClearAccountExceptionReq.check', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=570, serialized_end=628)
_LOCKREQUEST = _descriptor.Descriptor(name='LockRequest', full_name='gt.login.LockRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.login.LockRequest.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=630, serialized_end=656)
_LOCKRESPONSE = _descriptor.Descriptor(name='LockResponse', full_name='gt.login.LockResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.login.LockResponse.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='protect', full_name='gt.login.LockResponse.protect', index=1, number=2, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=658, serialized_end=702)
_ROLEREQUEST = _descriptor.Descriptor(name='RoleRequest', full_name='gt.login.RoleRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.RoleRequest.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='rolename', full_name='gt.login.RoleRequest.rolename', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=704, serialized_end=752)
_ROLEPROTECTREQUEST = _descriptor.Descriptor(name='RoleProtectRequest', full_name='gt.login.RoleProtectRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='rolename', full_name='gt.login.RoleProtectRequest.rolename', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=754, serialized_end=792)
_ONPROTECTREQUEST = _descriptor.Descriptor(name='OnProtectRequest', full_name='gt.login.OnProtectRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.OnProtectRequest.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=794, serialized_end=829)
_SETUSERBITMAPREQUEST = _descriptor.Descriptor(name='SetUserBitmapRequest', full_name='gt.login.SetUserBitmapRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.SetUserBitmapRequest.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='key', full_name='gt.login.SetUserBitmapRequest.key', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='value', full_name='gt.login.SetUserBitmapRequest.value', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=831, serialized_end=898)
_SETUSERBITMAPREPLY = _descriptor.Descriptor(name='SetUserBitmapReply', full_name='gt.login.SetUserBitmapReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.SetUserBitmapReply.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='bitmap', full_name='gt.login.SetUserBitmapReply.bitmap', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=900, serialized_end=953)
_GETUSERBITMAPREQUEST = _descriptor.Descriptor(name='GetUserBitmapRequest', full_name='gt.login.GetUserBitmapRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.GetUserBitmapRequest.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=955, serialized_end=994)
_GETUSERBITMAPREPLY = _descriptor.Descriptor(name='GetUserBitmapReply', full_name='gt.login.GetUserBitmapReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.GetUserBitmapReply.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='bitmap', full_name='gt.login.GetUserBitmapReply.bitmap', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=996, serialized_end=1049)
_KICKCONNECTIONREQ = _descriptor.Descriptor(name='KickConnectionReq', full_name='gt.login.KickConnectionReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.login.KickConnectionReq.uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1051, serialized_end=1084)
_SETUSERMAPFIELDBLOBMESSAGE = _descriptor.Descriptor(name='SetUsermapFieldBlobMessage', full_name='gt.login.SetUsermapFieldBlobMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='field', full_name='gt.login.SetUsermapFieldBlobMessage.field', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='value', full_name='gt.login.SetUsermapFieldBlobMessage.value', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1086, serialized_end=1144)
_SETUSERMAPFIELDINTMESSAGE = _descriptor.Descriptor(name='SetUsermapFieldIntMessage', full_name='gt.login.SetUsermapFieldIntMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='field', full_name='gt.login.SetUsermapFieldIntMessage.field', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='value', full_name='gt.login.SetUsermapFieldIntMessage.value', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1146, serialized_end=1203)
_SETUSERMAPFIELDREQUEST = _descriptor.Descriptor(name='SetUsermapFieldRequest', full_name='gt.login.SetUsermapFieldRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.login.SetUsermapFieldRequest.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='tag', full_name='gt.login.SetUsermapFieldRequest.tag', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='str_field', full_name='gt.login.SetUsermapFieldRequest.str_field', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='int_field', full_name='gt.login.SetUsermapFieldRequest.int_field', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1206, serialized_end=1369)
_SETUSERMAPFIELDREPLY = _descriptor.Descriptor(name='SetUsermapFieldReply', full_name='gt.login.SetUsermapFieldReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.login.SetUsermapFieldReply.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tag', full_name='gt.login.SetUsermapFieldReply.tag', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1371, serialized_end=1419)
_SETUSERRECHARGEREQUEST = _descriptor.Descriptor(name='SetUserRechargeRequest', full_name='gt.login.SetUserRechargeRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='urs', full_name='gt.login.SetUserRechargeRequest.urs', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='recharge', full_name='gt.login.SetUserRechargeRequest.recharge', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1421, serialized_end=1476)
_UPDATEREALNAMEFLAGREQUEST = _descriptor.Descriptor(name='UpdateRealnameFlagRequest', full_name='gt.login.UpdateRealnameFlagRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.login.UpdateRealnameFlagRequest.uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='flag', full_name='gt.login.UpdateRealnameFlagRequest.flag', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1478, serialized_end=1533)
_FLOWBACKBONUSSINGLE = _descriptor.Descriptor(name='FlowbackBonusSingle', full_name='gt.login.FlowbackBonusSingle', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='sn', full_name='gt.login.FlowbackBonusSingle.sn', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='urs', full_name='gt.login.FlowbackBonusSingle.urs', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='item_id', full_name='gt.login.FlowbackBonusSingle.item_id', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='num', full_name='gt.login.FlowbackBonusSingle.num', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='t_expire', full_name='gt.login.FlowbackBonusSingle.t_expire', index=4, number=5, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1535, serialized_end=1629)
_FLOWBACKBONUSREPLY = _descriptor.Descriptor(name='FlowbackBonusReply', full_name='gt.login.FlowbackBonusReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='sn', full_name='gt.login.FlowbackBonusReply.sn', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='n_del', full_name='gt.login.FlowbackBonusReply.n_del', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='bonus', full_name='gt.login.FlowbackBonusReply.bonus', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1631, serialized_end=1724)
_DELFLOWBACKBONUSREQUEST = _descriptor.Descriptor(name='DelFlowbackBonusRequest', full_name='gt.login.DelFlowbackBonusRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='sn', full_name='gt.login.DelFlowbackBonusRequest.sn', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='urs', full_name='gt.login.DelFlowbackBonusRequest.urs', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='item_ids', full_name='gt.login.DelFlowbackBonusRequest.item_ids', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1726, serialized_end=1794)
_ENABLEREALNAMECHECKREQUEST = _descriptor.Descriptor(name='EnableRealNameCheckRequest', full_name='gt.login.EnableRealNameCheckRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='enable_check', full_name='gt.login.EnableRealNameCheckRequest.enable_check', index=0, number=1, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1796, serialized_end=1846)
_ENABLEONEAVATARREQUEST = _descriptor.Descriptor(name='EnableOneAvatarRequest', full_name='gt.login.EnableOneAvatarRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='value', full_name='gt.login.EnableOneAvatarRequest.value', index=0, number=1, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1848, serialized_end=1887)
_KICKACCOUNTREPLY = _descriptor.Descriptor(name='KickAccountReply', full_name='gt.login.KickAccountReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.KickAccountReply.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='rolename', full_name='gt.login.KickAccountReply.rolename', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1889, serialized_end=1942)
_REGREALNAMEREPLY = _descriptor.Descriptor(name='RegRealNameReply', full_name='gt.login.RegRealNameReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='account', full_name='gt.login.RegRealNameReply.account', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='status', full_name='gt.login.RegRealNameReply.status', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='id', full_name='gt.login.RegRealNameReply.id', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1944, serialized_end=2007)
_ENABLEPLATFORMREALNAMECHECKREQUEST = _descriptor.Descriptor(name='EnablePlatformRealNameCheckRequest', full_name='gt.login.EnablePlatformRealNameCheckRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='enable_check', full_name='gt.login.EnablePlatformRealNameCheckRequest.enable_check', index=0, number=1, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2009, serialized_end=2067)
_SETUSERMAPFIELDREQUEST.fields_by_name['str_field'].message_type = _SETUSERMAPFIELDBLOBMESSAGE
_SETUSERMAPFIELDREQUEST.fields_by_name['int_field'].message_type = _SETUSERMAPFIELDINTMESSAGE
_FLOWBACKBONUSREPLY.fields_by_name['bonus'].message_type = _FLOWBACKBONUSSINGLE
DESCRIPTOR.message_types_by_name['RegRequest'] = _REGREQUEST
DESCRIPTOR.message_types_by_name['RegReply'] = _REGREPLY
DESCRIPTOR.message_types_by_name['UrsmapRequest'] = _URSMAPREQUEST
DESCRIPTOR.message_types_by_name['GameRandKey'] = _GAMERANDKEY
DESCRIPTOR.message_types_by_name['UrsInfoRequest'] = _URSINFOREQUEST
DESCRIPTOR.message_types_by_name['UrsInfoReply'] = _URSINFOREPLY
DESCRIPTOR.message_types_by_name['KickAccountReq'] = _KICKACCOUNTREQ
DESCRIPTOR.message_types_by_name['ClearAccountExceptionReq'] = _CLEARACCOUNTEXCEPTIONREQ
DESCRIPTOR.message_types_by_name['LockRequest'] = _LOCKREQUEST
DESCRIPTOR.message_types_by_name['LockResponse'] = _LOCKRESPONSE
DESCRIPTOR.message_types_by_name['RoleRequest'] = _ROLEREQUEST
DESCRIPTOR.message_types_by_name['RoleProtectRequest'] = _ROLEPROTECTREQUEST
DESCRIPTOR.message_types_by_name['OnProtectRequest'] = _ONPROTECTREQUEST
DESCRIPTOR.message_types_by_name['SetUserBitmapRequest'] = _SETUSERBITMAPREQUEST
DESCRIPTOR.message_types_by_name['SetUserBitmapReply'] = _SETUSERBITMAPREPLY
DESCRIPTOR.message_types_by_name['GetUserBitmapRequest'] = _GETUSERBITMAPREQUEST
DESCRIPTOR.message_types_by_name['GetUserBitmapReply'] = _GETUSERBITMAPREPLY
DESCRIPTOR.message_types_by_name['KickConnectionReq'] = _KICKCONNECTIONREQ
DESCRIPTOR.message_types_by_name['SetUsermapFieldBlobMessage'] = _SETUSERMAPFIELDBLOBMESSAGE
DESCRIPTOR.message_types_by_name['SetUsermapFieldIntMessage'] = _SETUSERMAPFIELDINTMESSAGE
DESCRIPTOR.message_types_by_name['SetUsermapFieldRequest'] = _SETUSERMAPFIELDREQUEST
DESCRIPTOR.message_types_by_name['SetUsermapFieldReply'] = _SETUSERMAPFIELDREPLY
DESCRIPTOR.message_types_by_name['SetUserRechargeRequest'] = _SETUSERRECHARGEREQUEST
DESCRIPTOR.message_types_by_name['UpdateRealnameFlagRequest'] = _UPDATEREALNAMEFLAGREQUEST
DESCRIPTOR.message_types_by_name['FlowbackBonusSingle'] = _FLOWBACKBONUSSINGLE
DESCRIPTOR.message_types_by_name['FlowbackBonusReply'] = _FLOWBACKBONUSREPLY
DESCRIPTOR.message_types_by_name['DelFlowbackBonusRequest'] = _DELFLOWBACKBONUSREQUEST
DESCRIPTOR.message_types_by_name['EnableRealNameCheckRequest'] = _ENABLEREALNAMECHECKREQUEST
DESCRIPTOR.message_types_by_name['EnableOneAvatarRequest'] = _ENABLEONEAVATARREQUEST
DESCRIPTOR.message_types_by_name['KickAccountReply'] = _KICKACCOUNTREPLY
DESCRIPTOR.message_types_by_name['RegRealNameReply'] = _REGREALNAMEREPLY
DESCRIPTOR.message_types_by_name['EnablePlatformRealNameCheckRequest'] = _ENABLEPLATFORMREALNAMECHECKREQUEST

class RegRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGREQUEST


class RegReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGREPLY


class UrsmapRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _URSMAPREQUEST


class GameRandKey(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMERANDKEY


class UrsInfoRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _URSINFOREQUEST


class UrsInfoReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _URSINFOREPLY


class KickAccountReq(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _KICKACCOUNTREQ


class ClearAccountExceptionReq(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CLEARACCOUNTEXCEPTIONREQ


class LockRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOCKREQUEST


class LockResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOCKRESPONSE


class RoleRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROLEREQUEST


class RoleProtectRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROLEPROTECTREQUEST


class OnProtectRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ONPROTECTREQUEST


class SetUserBitmapRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERBITMAPREQUEST


class SetUserBitmapReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERBITMAPREPLY


class GetUserBitmapRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETUSERBITMAPREQUEST


class GetUserBitmapReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETUSERBITMAPREPLY


class KickConnectionReq(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _KICKCONNECTIONREQ


class SetUsermapFieldBlobMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERMAPFIELDBLOBMESSAGE


class SetUsermapFieldIntMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERMAPFIELDINTMESSAGE


class SetUsermapFieldRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERMAPFIELDREQUEST


class SetUsermapFieldReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERMAPFIELDREPLY


class SetUserRechargeRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETUSERRECHARGEREQUEST


class UpdateRealnameFlagRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UPDATEREALNAMEFLAGREQUEST


class FlowbackBonusSingle(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FLOWBACKBONUSSINGLE


class FlowbackBonusReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FLOWBACKBONUSREPLY


class DelFlowbackBonusRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DELFLOWBACKBONUSREQUEST


class EnableRealNameCheckRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ENABLEREALNAMECHECKREQUEST


class EnableOneAvatarRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ENABLEONEAVATARREQUEST


class KickAccountReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _KICKACCOUNTREPLY


class RegRealNameReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGREALNAMEREPLY


class EnablePlatformRealNameCheckRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ENABLEPLATFORMREALNAMECHECKREQUEST


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '€')
_GAMESERVICE = _descriptor.ServiceDescriptor(name='GameService', full_name='gt.login.GameService', file=DESCRIPTOR, index=0, options=None, serialized_start=2070, serialized_end=3413, methods=[_descriptor.MethodDescriptor(name='RegServer', full_name='gt.login.GameService.RegServer', index=0, containing_service=None, input_type=_REGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='UpdateUrsmap', full_name='gt.login.GameService.UpdateUrsmap', index=1, containing_service=None, input_type=_URSMAPREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GameKeyToLogin', full_name='gt.login.GameService.GameKeyToLogin', index=2, containing_service=None, input_type=_GAMERANDKEY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='FetchUrsInfo', full_name='gt.login.GameService.FetchUrsInfo', index=3, containing_service=None, input_type=_URSINFOREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GmKickAccount', full_name='gt.login.GameService.GmKickAccount', index=4, containing_service=None, input_type=_KICKACCOUNTREQ, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ClearAccountException', full_name='gt.login.GameService.ClearAccountException', index=5, containing_service=None, input_type=_CLEARACCOUNTEXCEPTIONREQ, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='QueryLock', full_name='gt.login.GameService.QueryLock', index=6, containing_service=None, input_type=_LOCKREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='AddOnlineRole', full_name='gt.login.GameService.AddOnlineRole', index=7, containing_service=None, input_type=_ROLEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='DelOnlineRole', full_name='gt.login.GameService.DelOnlineRole', index=8, containing_service=None, input_type=_ROLEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnSetRoleProtect', full_name='gt.login.GameService.OnSetRoleProtect', index=9, containing_service=None, input_type=_ONPROTECTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqSetUserBitmap', full_name='gt.login.GameService.ReqSetUserBitmap', index=10, containing_service=None, input_type=_SETUSERBITMAPREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetUserBitmap', full_name='gt.login.GameService.ReqGetUserBitmap', index=11, containing_service=None, input_type=_GETUSERBITMAPREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='KickConnection', full_name='gt.login.GameService.KickConnection', index=12, containing_service=None, input_type=_KICKCONNECTIONREQ, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqSetUsermapField', full_name='gt.login.GameService.ReqSetUsermapField', index=13, containing_service=None, input_type=_SETUSERMAPFIELDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqSetUserRecharge', full_name='gt.login.GameService.ReqSetUserRecharge', index=14, containing_service=None, input_type=_SETUSERRECHARGEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='UpdateRealnameFlag', full_name='gt.login.GameService.UpdateRealnameFlag', index=15, containing_service=None, input_type=_UPDATEREALNAMEFLAGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='EnableRealNameCheck', full_name='gt.login.GameService.EnableRealNameCheck', index=16, containing_service=None, input_type=_ENABLEREALNAMECHECKREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='EnableOneAvatar', full_name='gt.login.GameService.EnableOneAvatar', index=17, containing_service=None, input_type=_ENABLEONEAVATARREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqAssignFlowbackBonus', full_name='gt.login.GameService.ReqAssignFlowbackBonus', index=18, containing_service=None, input_type=_FLOWBACKBONUSSINGLE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqDelFlowbackBonus', full_name='gt.login.GameService.ReqDelFlowbackBonus', index=19, containing_service=None, input_type=_DELFLOWBACKBONUSREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqListFlowbackBonus', full_name='gt.login.GameService.ReqListFlowbackBonus', index=20, containing_service=None, input_type=_FLOWBACKBONUSSINGLE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='EnablePlatformRealNameCheck', full_name='gt.login.GameService.EnablePlatformRealNameCheck', index=21, containing_service=None, input_type=_ENABLEPLATFORMREALNAMECHECKREQUEST, output_type=common_pb2._VOID, options=None)])

class GameService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _GAMESERVICE


class GameService_Stub(GameService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _GAMESERVICE


_GAMECLIENT = _descriptor.ServiceDescriptor(name='GameClient', full_name='gt.login.GameClient', file=DESCRIPTOR, index=1, options=None, serialized_start=3416, serialized_end=3933, methods=[_descriptor.MethodDescriptor(name='RcvUrsInfo', full_name='gt.login.GameClient.RcvUrsInfo', index=0, containing_service=None, input_type=_URSINFOREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnRegServer', full_name='gt.login.GameClient.OnRegServer', index=1, containing_service=None, input_type=_REGREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnQueryLock', full_name='gt.login.GameClient.OnQueryLock', index=2, containing_service=None, input_type=_LOCKRESPONSE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='SetRoleProtect', full_name='gt.login.GameClient.SetRoleProtect', index=3, containing_service=None, input_type=_ROLEPROTECTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepSetUserBitmap', full_name='gt.login.GameClient.RepSetUserBitmap', index=4, containing_service=None, input_type=_SETUSERBITMAPREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetUserBitmap', full_name='gt.login.GameClient.RepGetUserBitmap', index=5, containing_service=None, input_type=_GETUSERBITMAPREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepSetUsermapField', full_name='gt.login.GameClient.RepSetUsermapField', index=6, containing_service=None, input_type=_SETUSERMAPFIELDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReplyFlowbackBonus', full_name='gt.login.GameClient.ReplyFlowbackBonus', index=7, containing_service=None, input_type=_FLOWBACKBONUSREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='KickServerAccount', full_name='gt.login.GameClient.KickServerAccount', index=8, containing_service=None, input_type=_KICKACCOUNTREPLY, output_type=common_pb2._VOID, options=None)])

class GameClient(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _GAMECLIENT


class GameClient_Stub(GameClient):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _GAMECLIENT
