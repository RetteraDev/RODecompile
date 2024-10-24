#Embedded file name: I:/bag/tmp/tw2/res/entities\common\proto/admin_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
import admincommon_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='admin.proto', package='gt.admin', serialized_pb="\nadmin.protogt.admincommon.protoadmincommon.proto\";\n\nRegRequest\nserver (\nkey (\nserverId (\r\"<\nMessageHttpRequest\nwho (\nmsg (\nsucc (\"+\nToolMsgRequest\nuser (\nmsg (\"\n\nMsgRequest\nmsg (\"G\nChat2GmRequest\nuser (\nmsg (\nuuid (\nsucc (\"z\nChat2ChannelRequest\nserver (\nchannel (\ndesc (\nsrc (\ndst (\nmsg (\r\npos (: \"5\nCriticalRequest\n\rpython_server (\nmsg (\"5\nActivityRequest\n\rpython_server (\nmsg (\"4\nWarningRequest\n\rpython_server (\nmsg (\"@\nProgressRequest\n\rpython_server (\nprogress_value (\r\">\nUnderWriteRequest\n\rpython_server (\n\nwrite_info (\"_\nAvatarReportRequest\nserver (\ncaller (\nsender (\nmsg (\nuid (\"e\nMonitorReportRequest\nserver (\ntype (\ncaller (\nsender (\ncontent (\"m\nGmConnectRequest\nserver (\ncaller (\nsender (\nname (\nstatus (\nuid (\"P\nServerNotifyRequest\nserver (\ntalker (\nmsg (\nflag (\"O\nGetVipMsgRequest\nwho (\nvip_lv (\r\n\nlv (\r\n\nvip_msg_id (\r\"c\nGameSideSendVipMsgRequest\n	from_role (\n	from_gbid (\nmanager (\ncontent (\"R\nGameSideSendVipMsgReponse\nmanager (\ntarget_gbid (\ncontent (\"P\nGTSideSendVipMsgRequest\nmanager (\ntarget_gbid (\ncontent (\"b\nGTSideSendVipMsgResponse\nmanager (\n	from_role (\n	from_gbid (\ncontent (\"<\nGTSideManagerOnlineRequest\nmanager (\r\nstate (\r\" \nGetAllOnlineToolSerivceRequest\"S\n\nToolCmdMsg\r\ngroup (\nurs (\ncmd (\nuuid (\nreason (\"F\n\rToolGmChatMsg\r\ngroup (\nurs (\nrole (\nmsg (\"Z\nToolGmMonitorMsg\r\ngroup (\nurs (\nrole (\ntype (\nparams (\"L\nServerNotifyMsg\nserver (\ntalker (\nmsg (\nflag (\"\\\nPhoneAvatarMsg\r\ngroup (\nwho (\r\ntouid (\nsender (\ncontext (\"!\nVipMsg\n\nid (\r\nmsg (\"6\nVipMsgs\nwho (\nmsgs (2.gt.admin.VipMsg\"/\nToolServiceAccountsResponse\naccounts (2�	\nAdminService*\nRegister.gt.admin.RegRequest.gt.Void5\nMessageHttp.gt.admin.MessageHttpRequest.gt.Void1\nToolMessage.gt.admin.ToolMsgRequest.gt.Void1\n	GmConnect.gt.admin.GmConnectRequest.gt.Void7\nAvatarReport.gt.admin.AvatarReportRequest.gt.Void2\nDispatchToolMessage.gt.admin.Message.gt.Void-\nChat2Gm.gt.admin.Chat2GmRequest.gt.Void2\nChat2Channel.gt.admin.ChannelMessage.gt.Void5\nCriticalReport.gt.admin.CriticalRequest.gt.Void4\n\rCriticalClear.gt.admin.CriticalRequest.gt.Void3\n\rPrivateReport.gt.admin.ChannelMessage.gt.Void9\n\rMonitorReport.gt.admin.MonitorReportRequest.gt.Void5\nActivityReport.gt.admin.ActivityRequest.gt.Void3\n\rWarningReport.gt.admin.WarningRequest.gt.Void5\nProgressReport.gt.admin.ProgressRequest.gt.Void3\n\nUnderWrite.gt.admin.UnderWriteRequest.gt.Void7\nServerNotify.gt.admin.ServerNotifyRequest.gt.Void1\n	GetVipMsg.gt.admin.GetVipMsgRequest.gt.VoidC\nGameSideSendVipMsg#.gt.admin.GameSideSendVipMsgRequest.gt.VoidH\nGTSideSendVipMsgFeedback\".gt.admin.GTSideSendVipMsgResponse.gt.VoidP\nReqGetAllOnlineToolService(.gt.admin.GetAllOnlineToolSerivceRequest.gt.Void2�\nAdminClient-\nSendToolCmd.gt.admin.ToolCmdMsg.gt.Void4\nSendAdminGmChat.gt.admin.ToolGmChatMsg.gt.Void5\n\rSendGmMonitor.gt.admin.ToolGmMonitorMsg.gt.Void+\nSendMail.gt.admin.MailRequest.gt.Void5\nOnServerNotify.gt.admin.ServerNotifyMsg.gt.Void1\nPhoneAvatar.gt.admin.PhoneAvatarMsg.gt.Void\'\nOnVipMsg.gt.admin.VipMsgs.gt.Void?\nGTSideSendVipMsg!.gt.admin.GTSideSendVipMsgRequest.gt.VoidI\nXinYiManagerOnlineState$.gt.admin.GTSideManagerOnlineRequest.gt.VoidK\nGameSideSendVipMsgFeedBack#.gt.admin.GameSideSendVipMsgReponse.gt.VoidM\nRepGetAllOnlineToolService%.gt.admin.ToolServiceAccountsResponse.gt.VoidB��")
_REGREQUEST = _descriptor.Descriptor(name='RegRequest', full_name='gt.admin.RegRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.RegRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='key', full_name='gt.admin.RegRequest.key', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='serverId', full_name='gt.admin.RegRequest.serverId', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=58, serialized_end=117)
_MESSAGEHTTPREQUEST = _descriptor.Descriptor(name='MessageHttpRequest', full_name='gt.admin.MessageHttpRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='who', full_name='gt.admin.MessageHttpRequest.who', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.MessageHttpRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='succ', full_name='gt.admin.MessageHttpRequest.succ', index=2, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=119, serialized_end=179)
_TOOLMSGREQUEST = _descriptor.Descriptor(name='ToolMsgRequest', full_name='gt.admin.ToolMsgRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='user', full_name='gt.admin.ToolMsgRequest.user', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.ToolMsgRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=181, serialized_end=224)
_MSGREQUEST = _descriptor.Descriptor(name='MsgRequest', full_name='gt.admin.MsgRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='msg', full_name='gt.admin.MsgRequest.msg', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=226, serialized_end=251)
_CHAT2GMREQUEST = _descriptor.Descriptor(name='Chat2GmRequest', full_name='gt.admin.Chat2GmRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='user', full_name='gt.admin.Chat2GmRequest.user', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.Chat2GmRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uuid', full_name='gt.admin.Chat2GmRequest.uuid', index=2, number=3, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='succ', full_name='gt.admin.Chat2GmRequest.succ', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=253, serialized_end=324)
_CHAT2CHANNELREQUEST = _descriptor.Descriptor(name='Chat2ChannelRequest', full_name='gt.admin.Chat2ChannelRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.Chat2ChannelRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='channel', full_name='gt.admin.Chat2ChannelRequest.channel', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='desc', full_name='gt.admin.Chat2ChannelRequest.desc', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='src', full_name='gt.admin.Chat2ChannelRequest.src', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='dst', full_name='gt.admin.Chat2ChannelRequest.dst', index=4, number=5, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.Chat2ChannelRequest.msg', index=5, number=6, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='pos', full_name='gt.admin.Chat2ChannelRequest.pos', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=True, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=326, serialized_end=448)
_CRITICALREQUEST = _descriptor.Descriptor(name='CriticalRequest', full_name='gt.admin.CriticalRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='python_server', full_name='gt.admin.CriticalRequest.python_server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.CriticalRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=450, serialized_end=503)
_ACTIVITYREQUEST = _descriptor.Descriptor(name='ActivityRequest', full_name='gt.admin.ActivityRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='python_server', full_name='gt.admin.ActivityRequest.python_server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.ActivityRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=505, serialized_end=558)
_WARNINGREQUEST = _descriptor.Descriptor(name='WarningRequest', full_name='gt.admin.WarningRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='python_server', full_name='gt.admin.WarningRequest.python_server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.WarningRequest.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=560, serialized_end=612)
_PROGRESSREQUEST = _descriptor.Descriptor(name='ProgressRequest', full_name='gt.admin.ProgressRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='python_server', full_name='gt.admin.ProgressRequest.python_server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='progress_value', full_name='gt.admin.ProgressRequest.progress_value', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=614, serialized_end=678)
_UNDERWRITEREQUEST = _descriptor.Descriptor(name='UnderWriteRequest', full_name='gt.admin.UnderWriteRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='python_server', full_name='gt.admin.UnderWriteRequest.python_server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='write_info', full_name='gt.admin.UnderWriteRequest.write_info', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=680, serialized_end=742)
_AVATARREPORTREQUEST = _descriptor.Descriptor(name='AvatarReportRequest', full_name='gt.admin.AvatarReportRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.AvatarReportRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='caller', full_name='gt.admin.AvatarReportRequest.caller', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sender', full_name='gt.admin.AvatarReportRequest.sender', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.AvatarReportRequest.msg', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uid', full_name='gt.admin.AvatarReportRequest.uid', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=744, serialized_end=839)
_MONITORREPORTREQUEST = _descriptor.Descriptor(name='MonitorReportRequest', full_name='gt.admin.MonitorReportRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.MonitorReportRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='gt.admin.MonitorReportRequest.type', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='caller', full_name='gt.admin.MonitorReportRequest.caller', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sender', full_name='gt.admin.MonitorReportRequest.sender', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='content', full_name='gt.admin.MonitorReportRequest.content', index=4, number=5, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=841, serialized_end=942)
_GMCONNECTREQUEST = _descriptor.Descriptor(name='GmConnectRequest', full_name='gt.admin.GmConnectRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.GmConnectRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='caller', full_name='gt.admin.GmConnectRequest.caller', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sender', full_name='gt.admin.GmConnectRequest.sender', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='name', full_name='gt.admin.GmConnectRequest.name', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='status', full_name='gt.admin.GmConnectRequest.status', index=4, number=5, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uid', full_name='gt.admin.GmConnectRequest.uid', index=5, number=6, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=944, serialized_end=1053)
_SERVERNOTIFYREQUEST = _descriptor.Descriptor(name='ServerNotifyRequest', full_name='gt.admin.ServerNotifyRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.ServerNotifyRequest.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='talker', full_name='gt.admin.ServerNotifyRequest.talker', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.ServerNotifyRequest.msg', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='flag', full_name='gt.admin.ServerNotifyRequest.flag', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1055, serialized_end=1135)
_GETVIPMSGREQUEST = _descriptor.Descriptor(name='GetVipMsgRequest', full_name='gt.admin.GetVipMsgRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='who', full_name='gt.admin.GetVipMsgRequest.who', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='vip_lv', full_name='gt.admin.GetVipMsgRequest.vip_lv', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='lv', full_name='gt.admin.GetVipMsgRequest.lv', index=2, number=3, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='vip_msg_id', full_name='gt.admin.GetVipMsgRequest.vip_msg_id', index=3, number=4, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1137, serialized_end=1216)
_GAMESIDESENDVIPMSGREQUEST = _descriptor.Descriptor(name='GameSideSendVipMsgRequest', full_name='gt.admin.GameSideSendVipMsgRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='from_role', full_name='gt.admin.GameSideSendVipMsgRequest.from_role', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='from_gbid', full_name='gt.admin.GameSideSendVipMsgRequest.from_gbid', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='manager', full_name='gt.admin.GameSideSendVipMsgRequest.manager', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='content', full_name='gt.admin.GameSideSendVipMsgRequest.content', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1218, serialized_end=1317)
_GAMESIDESENDVIPMSGREPONSE = _descriptor.Descriptor(name='GameSideSendVipMsgReponse', full_name='gt.admin.GameSideSendVipMsgReponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='manager', full_name='gt.admin.GameSideSendVipMsgReponse.manager', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target_gbid', full_name='gt.admin.GameSideSendVipMsgReponse.target_gbid', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='content', full_name='gt.admin.GameSideSendVipMsgReponse.content', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1319, serialized_end=1401)
_GTSIDESENDVIPMSGREQUEST = _descriptor.Descriptor(name='GTSideSendVipMsgRequest', full_name='gt.admin.GTSideSendVipMsgRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='manager', full_name='gt.admin.GTSideSendVipMsgRequest.manager', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target_gbid', full_name='gt.admin.GTSideSendVipMsgRequest.target_gbid', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='content', full_name='gt.admin.GTSideSendVipMsgRequest.content', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1403, serialized_end=1483)
_GTSIDESENDVIPMSGRESPONSE = _descriptor.Descriptor(name='GTSideSendVipMsgResponse', full_name='gt.admin.GTSideSendVipMsgResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='manager', full_name='gt.admin.GTSideSendVipMsgResponse.manager', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='from_role', full_name='gt.admin.GTSideSendVipMsgResponse.from_role', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='from_gbid', full_name='gt.admin.GTSideSendVipMsgResponse.from_gbid', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='content', full_name='gt.admin.GTSideSendVipMsgResponse.content', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1485, serialized_end=1583)
_GTSIDEMANAGERONLINEREQUEST = _descriptor.Descriptor(name='GTSideManagerOnlineRequest', full_name='gt.admin.GTSideManagerOnlineRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='manager', full_name='gt.admin.GTSideManagerOnlineRequest.manager', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='state', full_name='gt.admin.GTSideManagerOnlineRequest.state', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1585, serialized_end=1645)
_GETALLONLINETOOLSERIVCEREQUEST = _descriptor.Descriptor(name='GetAllOnlineToolSerivceRequest', full_name='gt.admin.GetAllOnlineToolSerivceRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1647, serialized_end=1679)
_TOOLCMDMSG = _descriptor.Descriptor(name='ToolCmdMsg', full_name='gt.admin.ToolCmdMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='group', full_name='gt.admin.ToolCmdMsg.group', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='urs', full_name='gt.admin.ToolCmdMsg.urs', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cmd', full_name='gt.admin.ToolCmdMsg.cmd', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uuid', full_name='gt.admin.ToolCmdMsg.uuid', index=3, number=4, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='reason', full_name='gt.admin.ToolCmdMsg.reason', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1681, serialized_end=1764)
_TOOLGMCHATMSG = _descriptor.Descriptor(name='ToolGmChatMsg', full_name='gt.admin.ToolGmChatMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='group', full_name='gt.admin.ToolGmChatMsg.group', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='urs', full_name='gt.admin.ToolGmChatMsg.urs', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='role', full_name='gt.admin.ToolGmChatMsg.role', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.ToolGmChatMsg.msg', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1766, serialized_end=1836)
_TOOLGMMONITORMSG = _descriptor.Descriptor(name='ToolGmMonitorMsg', full_name='gt.admin.ToolGmMonitorMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='group', full_name='gt.admin.ToolGmMonitorMsg.group', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='urs', full_name='gt.admin.ToolGmMonitorMsg.urs', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='role', full_name='gt.admin.ToolGmMonitorMsg.role', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='gt.admin.ToolGmMonitorMsg.type', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='params', full_name='gt.admin.ToolGmMonitorMsg.params', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1838, serialized_end=1928)
_SERVERNOTIFYMSG = _descriptor.Descriptor(name='ServerNotifyMsg', full_name='gt.admin.ServerNotifyMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.admin.ServerNotifyMsg.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='talker', full_name='gt.admin.ServerNotifyMsg.talker', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.ServerNotifyMsg.msg', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='flag', full_name='gt.admin.ServerNotifyMsg.flag', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1930, serialized_end=2006)
_PHONEAVATARMSG = _descriptor.Descriptor(name='PhoneAvatarMsg', full_name='gt.admin.PhoneAvatarMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='group', full_name='gt.admin.PhoneAvatarMsg.group', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='who', full_name='gt.admin.PhoneAvatarMsg.who', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='touid', full_name='gt.admin.PhoneAvatarMsg.touid', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sender', full_name='gt.admin.PhoneAvatarMsg.sender', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='context', full_name='gt.admin.PhoneAvatarMsg.context', index=4, number=5, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2008, serialized_end=2100)
_VIPMSG = _descriptor.Descriptor(name='VipMsg', full_name='gt.admin.VipMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='id', full_name='gt.admin.VipMsg.id', index=0, number=1, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.admin.VipMsg.msg', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2102, serialized_end=2135)
_VIPMSGS = _descriptor.Descriptor(name='VipMsgs', full_name='gt.admin.VipMsgs', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='who', full_name='gt.admin.VipMsgs.who', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msgs', full_name='gt.admin.VipMsgs.msgs', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2137, serialized_end=2191)
_TOOLSERVICEACCOUNTSRESPONSE = _descriptor.Descriptor(name='ToolServiceAccountsResponse', full_name='gt.admin.ToolServiceAccountsResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='accounts', full_name='gt.admin.ToolServiceAccountsResponse.accounts', index=0, number=1, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2193, serialized_end=2240)
_VIPMSGS.fields_by_name['msgs'].message_type = _VIPMSG
DESCRIPTOR.message_types_by_name['RegRequest'] = _REGREQUEST
DESCRIPTOR.message_types_by_name['MessageHttpRequest'] = _MESSAGEHTTPREQUEST
DESCRIPTOR.message_types_by_name['ToolMsgRequest'] = _TOOLMSGREQUEST
DESCRIPTOR.message_types_by_name['MsgRequest'] = _MSGREQUEST
DESCRIPTOR.message_types_by_name['Chat2GmRequest'] = _CHAT2GMREQUEST
DESCRIPTOR.message_types_by_name['Chat2ChannelRequest'] = _CHAT2CHANNELREQUEST
DESCRIPTOR.message_types_by_name['CriticalRequest'] = _CRITICALREQUEST
DESCRIPTOR.message_types_by_name['ActivityRequest'] = _ACTIVITYREQUEST
DESCRIPTOR.message_types_by_name['WarningRequest'] = _WARNINGREQUEST
DESCRIPTOR.message_types_by_name['ProgressRequest'] = _PROGRESSREQUEST
DESCRIPTOR.message_types_by_name['UnderWriteRequest'] = _UNDERWRITEREQUEST
DESCRIPTOR.message_types_by_name['AvatarReportRequest'] = _AVATARREPORTREQUEST
DESCRIPTOR.message_types_by_name['MonitorReportRequest'] = _MONITORREPORTREQUEST
DESCRIPTOR.message_types_by_name['GmConnectRequest'] = _GMCONNECTREQUEST
DESCRIPTOR.message_types_by_name['ServerNotifyRequest'] = _SERVERNOTIFYREQUEST
DESCRIPTOR.message_types_by_name['GetVipMsgRequest'] = _GETVIPMSGREQUEST
DESCRIPTOR.message_types_by_name['GameSideSendVipMsgRequest'] = _GAMESIDESENDVIPMSGREQUEST
DESCRIPTOR.message_types_by_name['GameSideSendVipMsgReponse'] = _GAMESIDESENDVIPMSGREPONSE
DESCRIPTOR.message_types_by_name['GTSideSendVipMsgRequest'] = _GTSIDESENDVIPMSGREQUEST
DESCRIPTOR.message_types_by_name['GTSideSendVipMsgResponse'] = _GTSIDESENDVIPMSGRESPONSE
DESCRIPTOR.message_types_by_name['GTSideManagerOnlineRequest'] = _GTSIDEMANAGERONLINEREQUEST
DESCRIPTOR.message_types_by_name['GetAllOnlineToolSerivceRequest'] = _GETALLONLINETOOLSERIVCEREQUEST
DESCRIPTOR.message_types_by_name['ToolCmdMsg'] = _TOOLCMDMSG
DESCRIPTOR.message_types_by_name['ToolGmChatMsg'] = _TOOLGMCHATMSG
DESCRIPTOR.message_types_by_name['ToolGmMonitorMsg'] = _TOOLGMMONITORMSG
DESCRIPTOR.message_types_by_name['ServerNotifyMsg'] = _SERVERNOTIFYMSG
DESCRIPTOR.message_types_by_name['PhoneAvatarMsg'] = _PHONEAVATARMSG
DESCRIPTOR.message_types_by_name['VipMsg'] = _VIPMSG
DESCRIPTOR.message_types_by_name['VipMsgs'] = _VIPMSGS
DESCRIPTOR.message_types_by_name['ToolServiceAccountsResponse'] = _TOOLSERVICEACCOUNTSRESPONSE

class RegRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGREQUEST


class MessageHttpRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MESSAGEHTTPREQUEST


class ToolMsgRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOOLMSGREQUEST


class MsgRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MSGREQUEST


class Chat2GmRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CHAT2GMREQUEST


class Chat2ChannelRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CHAT2CHANNELREQUEST


class CriticalRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CRITICALREQUEST


class ActivityRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ACTIVITYREQUEST


class WarningRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _WARNINGREQUEST


class ProgressRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PROGRESSREQUEST


class UnderWriteRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNDERWRITEREQUEST


class AvatarReportRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _AVATARREPORTREQUEST


class MonitorReportRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MONITORREPORTREQUEST


class GmConnectRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GMCONNECTREQUEST


class ServerNotifyRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SERVERNOTIFYREQUEST


class GetVipMsgRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETVIPMSGREQUEST


class GameSideSendVipMsgRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDESENDVIPMSGREQUEST


class GameSideSendVipMsgReponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDESENDVIPMSGREPONSE


class GTSideSendVipMsgRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GTSIDESENDVIPMSGREQUEST


class GTSideSendVipMsgResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GTSIDESENDVIPMSGRESPONSE


class GTSideManagerOnlineRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GTSIDEMANAGERONLINEREQUEST


class GetAllOnlineToolSerivceRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETALLONLINETOOLSERIVCEREQUEST


class ToolCmdMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOOLCMDMSG


class ToolGmChatMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOOLGMCHATMSG


class ToolGmMonitorMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOOLGMMONITORMSG


class ServerNotifyMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SERVERNOTIFYMSG


class PhoneAvatarMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PHONEAVATARMSG


class VipMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _VIPMSG


class VipMsgs(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _VIPMSGS


class ToolServiceAccountsResponse(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _TOOLSERVICEACCOUNTSRESPONSE


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '��')
_ADMINSERVICE = _descriptor.ServiceDescriptor(name='AdminService', full_name='gt.admin.AdminService', file=DESCRIPTOR, index=0, options=None, serialized_start=2243, serialized_end=3436, methods=[_descriptor.MethodDescriptor(name='Register', full_name='gt.admin.AdminService.Register', index=0, containing_service=None, input_type=_REGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='MessageHttp', full_name='gt.admin.AdminService.MessageHttp', index=1, containing_service=None, input_type=_MESSAGEHTTPREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ToolMessage', full_name='gt.admin.AdminService.ToolMessage', index=2, containing_service=None, input_type=_TOOLMSGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GmConnect', full_name='gt.admin.AdminService.GmConnect', index=3, containing_service=None, input_type=_GMCONNECTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='AvatarReport', full_name='gt.admin.AdminService.AvatarReport', index=4, containing_service=None, input_type=_AVATARREPORTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='DispatchToolMessage', full_name='gt.admin.AdminService.DispatchToolMessage', index=5, containing_service=None, input_type=admincommon_pb2._MESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='Chat2Gm', full_name='gt.admin.AdminService.Chat2Gm', index=6, containing_service=None, input_type=_CHAT2GMREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='Chat2Channel', full_name='gt.admin.AdminService.Chat2Channel', index=7, containing_service=None, input_type=admincommon_pb2._CHANNELMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='CriticalReport', full_name='gt.admin.AdminService.CriticalReport', index=8, containing_service=None, input_type=_CRITICALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='CriticalClear', full_name='gt.admin.AdminService.CriticalClear', index=9, containing_service=None, input_type=_CRITICALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='PrivateReport', full_name='gt.admin.AdminService.PrivateReport', index=10, containing_service=None, input_type=admincommon_pb2._CHANNELMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='MonitorReport', full_name='gt.admin.AdminService.MonitorReport', index=11, containing_service=None, input_type=_MONITORREPORTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ActivityReport', full_name='gt.admin.AdminService.ActivityReport', index=12, containing_service=None, input_type=_ACTIVITYREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='WarningReport', full_name='gt.admin.AdminService.WarningReport', index=13, containing_service=None, input_type=_WARNINGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ProgressReport', full_name='gt.admin.AdminService.ProgressReport', index=14, containing_service=None, input_type=_PROGRESSREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='UnderWrite', full_name='gt.admin.AdminService.UnderWrite', index=15, containing_service=None, input_type=_UNDERWRITEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ServerNotify', full_name='gt.admin.AdminService.ServerNotify', index=16, containing_service=None, input_type=_SERVERNOTIFYREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GetVipMsg', full_name='gt.admin.AdminService.GetVipMsg', index=17, containing_service=None, input_type=_GETVIPMSGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GameSideSendVipMsg', full_name='gt.admin.AdminService.GameSideSendVipMsg', index=18, containing_service=None, input_type=_GAMESIDESENDVIPMSGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GTSideSendVipMsgFeedback', full_name='gt.admin.AdminService.GTSideSendVipMsgFeedback', index=19, containing_service=None, input_type=_GTSIDESENDVIPMSGRESPONSE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetAllOnlineToolService', full_name='gt.admin.AdminService.ReqGetAllOnlineToolService', index=20, containing_service=None, input_type=_GETALLONLINETOOLSERIVCEREQUEST, output_type=common_pb2._VOID, options=None)])

class AdminService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _ADMINSERVICE


class AdminService_Stub(AdminService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _ADMINSERVICE


_ADMINCLIENT = _descriptor.ServiceDescriptor(name='AdminClient', full_name='gt.admin.AdminClient', file=DESCRIPTOR, index=1, options=None, serialized_start=3439, serialized_end=4096, methods=[_descriptor.MethodDescriptor(name='SendToolCmd', full_name='gt.admin.AdminClient.SendToolCmd', index=0, containing_service=None, input_type=_TOOLCMDMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='SendAdminGmChat', full_name='gt.admin.AdminClient.SendAdminGmChat', index=1, containing_service=None, input_type=_TOOLGMCHATMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='SendGmMonitor', full_name='gt.admin.AdminClient.SendGmMonitor', index=2, containing_service=None, input_type=_TOOLGMMONITORMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='SendMail', full_name='gt.admin.AdminClient.SendMail', index=3, containing_service=None, input_type=admincommon_pb2._MAILREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnServerNotify', full_name='gt.admin.AdminClient.OnServerNotify', index=4, containing_service=None, input_type=_SERVERNOTIFYMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='PhoneAvatar', full_name='gt.admin.AdminClient.PhoneAvatar', index=5, containing_service=None, input_type=_PHONEAVATARMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OnVipMsg', full_name='gt.admin.AdminClient.OnVipMsg', index=6, containing_service=None, input_type=_VIPMSGS, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GTSideSendVipMsg', full_name='gt.admin.AdminClient.GTSideSendVipMsg', index=7, containing_service=None, input_type=_GTSIDESENDVIPMSGREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='XinYiManagerOnlineState', full_name='gt.admin.AdminClient.XinYiManagerOnlineState', index=8, containing_service=None, input_type=_GTSIDEMANAGERONLINEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='GameSideSendVipMsgFeedBack', full_name='gt.admin.AdminClient.GameSideSendVipMsgFeedBack', index=9, containing_service=None, input_type=_GAMESIDESENDVIPMSGREPONSE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetAllOnlineToolService', full_name='gt.admin.AdminClient.RepGetAllOnlineToolService', index=10, containing_service=None, input_type=_TOOLSERVICEACCOUNTSRESPONSE, output_type=common_pb2._VOID, options=None)])

class AdminClient(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _ADMINCLIENT


class AdminClient_Stub(AdminClient):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _ADMINCLIENT
