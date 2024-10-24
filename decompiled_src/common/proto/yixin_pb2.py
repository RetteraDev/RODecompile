#Embedded file name: I:/bag/tmp/tw2/res/entities\common\proto/yixin_pb2.o
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='yixin.proto', package='gt.yixin', serialized_pb="\nyixin.protogt.yixincommon.proto\"*\nRegisterMsg\nserver (\nkey (\"\nPlayer\nuuid (\"b\nSenderInfos\nrolename (\nuuid (\ngender (\n\nprofession (\ncontent (\"#\nArgs\nname (\r\nvalue (\"c\nRegisterYixinRequest \nplayer (2.gt.yixin.Player\nmobile (\npwd (\nnick (\"�\nRegisterYixinReply \nplayer (2.gt.yixin.Player;\nerror (2\".gt.yixin.RegisterYixinReply.Error:NO_ERROR\"1\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\"W\nBindYixinUserRequest \nplayer (2.gt.yixin.Player\nmobile (\r\ndrill (\"�\nBindYixinUserReply \nplayer (2.gt.yixin.Player;\nerror (2\".gt.yixin.BindYixinUserReply.Error:NO_ERROR\r\ndrill (\nmobile (\nopenid (\ncooldown (\"�\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\n\nBAD_MOBILE\nDOUBLE_YIXIN_BIND\nDOUBLE_USER_BIND\nCOOLING_DOWN\"O\nUnBindYixinUserRequest\nhandle_name ( \nplayer (2.gt.yixin.Player\"�\nUnBindYixinUserReply\nhandle_name ( \nplayer (2.gt.yixin.Player=\nerror (2$.gt.yixin.UnBindYixinUserReply.Error:NO_ERROR\"1\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\"D\nSignRequest\nhandle_name ( \nplayer (2.gt.yixin.Player\"S\n	SignReply\nhandle_name ( \nplayer (2.gt.yixin.Player\nmessage (\"\nClan\nuuid (\"?\nCreateClanRequest\nclan (2.gt.yixin.Clan\nname (\"�\nCreateClanReply\nclan (2.gt.yixin.Clan8\nerror (2.gt.yixin.CreateClanReply.Error:NO_ERROR\ntid (\"h\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nBAD_DATABASE_REPLY\nBAD_NAME\nDOUBLE_BIND\"?\nRenameClanRequest\nclan (2.gt.yixin.Clan\nname (\"�\nRenameClanReply\nclan (2.gt.yixin.Clan8\nerror (2.gt.yixin.RenameClanReply.Error:NO_ERROR\"?\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nBAD_CLAN\"d\nAddClanMemberRequest\nclan (2.gt.yixin.Clan \nmember (2.gt.yixin.Player\nnick (\"�\nAddClanMemberReply\nclan (2.gt.yixin.Clan \nmember (2.gt.yixin.Player;\nerror (2\".gt.yixin.AddClanMemberReply.Error:NO_ERROR\"U\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nPLAYER_NOT_EXIST\nBAD_CLAN\"Y\nRemoveClanMemberRequest\nclan (2.gt.yixin.Clan \nmember (2.gt.yixin.Player\"�\nRemoveClanMemberReply\nclan (2.gt.yixin.Clan \nmember (2.gt.yixin.Player>\nerror (2%.gt.yixin.RemoveClanMemberReply.Error:NO_ERROR\"1\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\"g\nRenameClanMemberRequest\nclan (2.gt.yixin.Clan \nmember (2.gt.yixin.Player\nnick (\"`\n\rChatToClanMsg\nclan (2.gt.yixin.Clan \ntalker (2.gt.yixin.Player\ncontent (\"t\n\rClanChatToMsg\nclan (2.gt.yixin.Clan \ntalker (2.gt.yixin.Player\n\ntalkerNick (\ncontent (\"Y\nCountYixinFriendRequest \nplayer (2.gt.yixin.Player\nargs (2.gt.yixin.Args\"�\nCountYixinFriendReply \nplayer (2.gt.yixin.Player\r\ncount (\r>\nerror (2%.gt.yixin.CountYixinFriendReply.Error:NO_ERROR\nargs (2.gt.yixin.Args\"1\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\"<\nFollowPublicYixinRequest \nplayer (2.gt.yixin.Player\"�\nFollowPublicYixinReply \nplayer (2.gt.yixin.Player?\nerror (2&.gt.yixin.FollowPublicYixinReply.Error:NO_ERROR\">\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nALREADY\"B\nGameSideUnBindYixinUserRequest \nplayer (2.gt.yixin.Player\"�\nGameSideUnBindYixinUserReply \nplayer (2.gt.yixin.PlayerE\nerror (2,.gt.yixin.GameSideUnBindYixinUserReply.Error:NO_ERROR\"#\nError\nNO_ERROR \nUNEXISTS\"\"\nResetCooldownMsg\nmobile (\"J\nRejoinClanRequest\nhandle_name ( \nplayer (2.gt.yixin.Player\"Y\nRejoinClanReply\nhandle_name ( \nplayer (2.gt.yixin.Player\nmessage (\"e\nImageToClanMsg\nclan (2.gt.yixin.Clan\"\nuploader (2.gt.yixin.Player\n	image_url (\"I\nQueryYixinUserRequest \nplayer (2.gt.yixin.Player\nmobile (\"�\nQueryYixinUserReply \nplayer (2.gt.yixin.Player<\nerror (2#.gt.yixin.QueryYixinUserReply.Error:NO_ERROR\nmobile (\nserver (\nopenid (\"^\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\r\n	NO_PLAYER\r\n	NO_OPENID\r\n	NOT_MATCH\"0\nQueryClanRequest\nclan (2.gt.yixin.Clan\"�\nQueryClanReply\nclan (2.gt.yixin.Clan7\nerror (2.gt.yixin.QueryClanReply.Error:NO_ERROR\ntid (\"\"\nError\nNO_ERROR \nNO_TEAM\"P\nGetPlayerGeneralRequest\nhandle_name ( \nplayer (2.gt.yixin.Player\"q\nGetPlayerGeneralReply\nhandle_name ( \nplayer (2.gt.yixin.Player\n	errorcode (\nresult (\"\'\nOpenIDs\nuuid (\nopenid (\"\\\nOneChatToMsg \nplayer (2.gt.yixin.Player*\nsenderinfos (2.gt.yixin.SenderInfos\"e\nChatToOneMsg \ntalker (2.gt.yixin.Player\"\nlistener (2.gt.yixin.Player\ncontent (\"-\nGameSideUnBindMobileRequest\nmobile (\"�\nGameSideUnBindMobileReply\nmobile (B\nerror (2).gt.yixin.GameSideUnBindMobileReply.Error:NO_ERROR\"O\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\n\nBAD_MOBILE\nUNEXISTS\"$\nQueryMobileRequest\nmobile (\"�\nQueryMobileReply\nmobile (9\nerror (2 .gt.yixin.QueryMobileReply.Error:NO_ERROR\nopenid ( \nplayer (2.gt.yixin.Player\nserver (\"M\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\r\n	NO_OPENID\nNO_BIND\"J\nSetPlayerRewardRequest \nplayer (2.gt.yixin.Player\nreward (\r\"�\nSetPlayerRewardReply \nplayer (2.gt.yixin.Player=\nerror (2$.gt.yixin.SetPlayerRewardReply.Error:NO_ERROR\nreward (\r\"O\nError\nNO_ERROR \nPLAYER_NOT_EXIST\nALREADY_SET\n\rTYPE_OVERFLOW\"L\nUnsetPlayerRewardRequest \nplayer (2.gt.yixin.Player\nreward (\r\"�\nUnsetPlayerRewardReply \nplayer (2.gt.yixin.Player?\nerror (2&.gt.yixin.UnsetPlayerRewardReply.Error:NO_ERROR\nreward (\r\"K\nError\nNO_ERROR \nPLAYER_NOT_EXIST\nNOT_SET\n\rTYPE_OVERFLOW\"<\nQueryPlayerRewardRequest \nplayer (2.gt.yixin.Player\"�\nQueryPlayerRewardReply \nplayer (2.gt.yixin.Player\nreward (5\nerror (2&.gt.yixin.QueryPlayerRewardReply.Error\"+\nError\nNO_ERROR \nPLAYER_NOT_EXIST\"]\nQueryPlayerHeadImageRequest \nplayer (2.gt.yixin.Player\nargs (2.gt.yixin.Args\"�\nQueryPlayerHeadImageReply \nplayer (2.gt.yixin.Player\n\nheadimgurl (8\nerror (2).gt.yixin.QueryPlayerHeadImageReply.Error\nargs (2.gt.yixin.Args\"G\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nPLAYER_NOT_EXIST\"c\nAddFriendRequest \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player\nmsg (\"�\nAddFriendReply \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player-\nerror (2.gt.yixin.AddFriendReply.Error\nmsg (\"�\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\n\rSRC_NOT_EXIST\n\rTGT_NOT_EXIST\nMAX_FRIEND_LIMIT\n\rIN_BLACK_LIST\nALREADY_FRIEND\nMAX_ADD_FRIEND_FREQUENT\nAUTO_ADD_FRIEND\"Y\nAcceptFriendRequest \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player\"�\nAcceptFriendReply \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player0\nerror (2!.gt.yixin.AcceptFriendReply.Error\"m\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\n\rSRC_NOT_EXIST\n\rTGT_NOT_EXIST\nMAX_FRIEND_LIMIT\":\nYixinFriendListRequest \nplayer (2.gt.yixin.Player\"�\nYixinFriendListReply \nplayer (2.gt.yixin.Player\nopenids (3\nerror (2$.gt.yixin.YixinFriendListReply.Error\"G\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\nPLAYER_NOT_EXIST\"m\nUpdateFriendAliasRequest \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player\r\nalias (\"�\nUpdateFriendAliasReply \nsource (2.gt.yixin.Player \ntarget (2.gt.yixin.Player5\nerror (2&.gt.yixin.UpdateFriendAliasReply.Error\"W\nError\nNO_ERROR \nBAD_YIXIN_SERVER_REPLY\n\rSRC_NOT_EXIST\n\rTGT_NOT_EXIST\"K\nPublicSendP2PTextRequest!\nplayers (2.gt.yixin.Player\ntext (2�\nYixinServer+\nRegister.gt.yixin.RegisterMsg.gt.Void<\nReqRegisterYixin.gt.yixin.RegisterYixinRequest.gt.Void<\nReqBindYixinUser.gt.yixin.BindYixinUserRequest.gt.Void>\nRepUnBindYixinUser.gt.yixin.UnBindYixinUserReply.gt.Void(\nRepSign.gt.yixin.SignReply.gt.Void6\n\rReqCreateClan.gt.yixin.CreateClanRequest.gt.Void6\n\rReqRenameClan.gt.yixin.RenameClanRequest.gt.Void*\nReqDisbandClan.gt.yixin.Clan.gt.Void<\nReqAddClanMember.gt.yixin.AddClanMemberRequest.gt.VoidB\nReqRenameClanMember!.gt.yixin.RenameClanMemberRequest.gt.VoidB\nReqRemoveClanMember!.gt.yixin.RemoveClanMemberRequest.gt.Void/\n\nClanChatTo.gt.yixin.ClanChatToMsg.gt.VoidB\nReqCountYixinFriend!.gt.yixin.CountYixinFriendRequest.gt.VoidD\nReqFollowPublicYixin\".gt.yixin.FollowPublicYixinRequest.gt.VoidG\nReqGameSideUnBind(.gt.yixin.GameSideUnBindYixinUserRequest.gt.Void5\n\rResetCooldown.gt.yixin.ResetCooldownMsg.gt.Void4\n\rRepRejoinClan.gt.yixin.RejoinClanReply.gt.Void>\nReqQueryYixinUser.gt.yixin.QueryYixinUserRequest.gt.Void4\nReqQueryClan.gt.yixin.QueryClanRequest.gt.Void@\nRepGetPlayerFriends.gt.yixin.GetPlayerGeneralReply.gt.Void=\nRepGetPlayerClan.gt.yixin.GetPlayerGeneralReply.gt.Void?\nRepGetPlayerStatus.gt.yixin.GetPlayerGeneralReply.gt.Void=\nRepGetPlayerInfo.gt.yixin.GetPlayerGeneralReply.gt.Void,\nReqPushOpenIDs.gt.yixin.Player.gt.Void(\n\nBindRoleID.gt.yixin.Player.gt.Void-\n	OneChatTo.gt.yixin.OneChatToMsg.gt.VoidJ\nReqGameSideUnBindMobile%.gt.yixin.GameSideUnBindMobileRequest.gt.Void8\nReqQueryMobile.gt.yixin.QueryMobileRequest.gt.VoidD\nReqQueryPlayerReward\".gt.yixin.QueryPlayerRewardRequest.gt.Void@\nReqSetPlayerReward .gt.yixin.SetPlayerRewardRequest.gt.VoidJ\nReqQueryPlayerHeadImage%.gt.yixin.QueryPlayerHeadImageRequest.gt.Void4\nReqAddFriend.gt.yixin.AddFriendRequest.gt.Void:\nReqAcceptFriend.gt.yixin.AcceptFriendRequest.gt.Void@\nReqYixinFriendList .gt.yixin.YixinFriendListRequest.gt.VoidD\nReqUpdateFriendAlias\".gt.yixin.UpdateFriendAliasRequest.gt.VoidD\nReqPublicSendP2PText\".gt.yixin.PublicSendP2PTextRequest.gt.VoidD\nReqUnsetPlayerReward\".gt.yixin.UnsetPlayerRewardRequest.gt.Void2�\nYixinClient:\nRepRegisterYixin.gt.yixin.RegisterYixinReply.gt.Void:\nRepBindYixinUser.gt.yixin.BindYixinUserReply.gt.Void@\nReqUnBindYixinUser .gt.yixin.UnBindYixinUserRequest.gt.Void*\nReqSign.gt.yixin.SignRequest.gt.Void4\n\rRepCreateClan.gt.yixin.CreateClanReply.gt.Void4\n\rRepRenameClan.gt.yixin.RenameClanReply.gt.Void:\nRepAddClanMember.gt.yixin.AddClanMemberReply.gt.Void@\nRepRemoveClanMember.gt.yixin.RemoveClanMemberReply.gt.Void/\n\nChatToClan.gt.yixin.ChatToClanMsg.gt.Void@\nRepCountYixinFriend.gt.yixin.CountYixinFriendReply.gt.VoidB\nRepFollowPublicYixin .gt.yixin.FollowPublicYixinReply.gt.VoidE\nRepGameSideUnBind&.gt.yixin.GameSideUnBindYixinUserReply.gt.Void6\n\rReqRejoinClan.gt.yixin.RejoinClanRequest.gt.Void1\nImageToClan.gt.yixin.ImageToClanMsg.gt.Void<\nRepQueryYixinUser.gt.yixin.QueryYixinUserReply.gt.Void2\nRepQueryClan.gt.yixin.QueryClanReply.gt.VoidB\nReqGetPlayerFriends!.gt.yixin.GetPlayerGeneralRequest.gt.Void?\nReqGetPlayerClan!.gt.yixin.GetPlayerGeneralRequest.gt.VoidA\nReqGetPlayerStatus!.gt.yixin.GetPlayerGeneralRequest.gt.Void?\nReqGetPlayerInfo!.gt.yixin.GetPlayerGeneralRequest.gt.Void-\nRepPushOpenIDs.gt.yixin.OpenIDs.gt.Void-\n	ChatToOne.gt.yixin.ChatToOneMsg.gt.VoidH\nRepGameSideUnBindMobile#.gt.yixin.GameSideUnBindMobileReply.gt.Void6\nRepQueryMobile.gt.yixin.QueryMobileReply.gt.VoidB\nRepQueryPlayerReward .gt.yixin.QueryPlayerRewardReply.gt.Void>\nRepSetPlayerReward.gt.yixin.SetPlayerRewardReply.gt.VoidH\nRepQueryPlayerHeadImage#.gt.yixin.QueryPlayerHeadImageReply.gt.Void2\nRepAddFriend.gt.yixin.AddFriendReply.gt.Void8\nRepAcceptFriend.gt.yixin.AcceptFriendReply.gt.Void>\nRepYixinFriendList.gt.yixin.YixinFriendListReply.gt.VoidB\nRepUpdateFriendAlias .gt.yixin.UpdateFriendAliasReply.gt.VoidB\nRepUnsetPlayerReward .gt.yixin.UnsetPlayerRewardReply.gt.VoidB��")
_REGISTERYIXINREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.RegisterYixinReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=463, serialized_end=512)
_BINDYIXINUSERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.BindYixinUserReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_MOBILE', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DOUBLE_YIXIN_BIND', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DOUBLE_USER_BIND', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='COOLING_DOWN', index=5, number=5, options=None, type=None)], containing_type=None, options=None, serialized_start=787, serialized_end=915)
_UNBINDYIXINUSERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.UnBindYixinUserReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=463, serialized_end=512)
_CREATECLANREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.CreateClanReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_DATABASE_REPLY', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_NAME', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DOUBLE_BIND', index=4, number=4, options=None, type=None)], containing_type=None, options=None, serialized_start=1555, serialized_end=1659)
_RENAMECLANREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.RenameClanReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_CLAN', index=2, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=1834, serialized_end=1897)
_ADDCLANMEMBERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.AddClanMemberReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_CLAN', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=2149, serialized_end=2234)
_REMOVECLANMEMBERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.RemoveClanMemberReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=463, serialized_end=512)
_COUNTYIXINFRIENDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.CountYixinFriendReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=463, serialized_end=512)
_FOLLOWPUBLICYIXINREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.FollowPublicYixinReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='ALREADY', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=3352, serialized_end=3414)
_GAMESIDEUNBINDYIXINUSERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.GameSideUnBindYixinUserReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='UNEXISTS', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=3622, serialized_end=3657)
_QUERYYIXINUSERREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.QueryYixinUserReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NO_PLAYER', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NO_OPENID', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NOT_MATCH', index=4, number=4, options=None, type=None)], containing_type=None, options=None, serialized_start=4208, serialized_end=4302)
_QUERYCLANREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.QueryClanReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='NO_TEAM', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=4473, serialized_end=4507)
_GAMESIDEUNBINDMOBILEREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.GameSideUnBindMobileReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_MOBILE', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='UNEXISTS', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=5105, serialized_end=5184)
_QUERYMOBILEREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.QueryMobileReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NO_OPENID', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NO_BIND', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=5386, serialized_end=5463)
_SETPLAYERREWARDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.SetPlayerRewardReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=1, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='ALREADY_SET', index=2, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TYPE_OVERFLOW', index=3, number=4, options=None, type=None)], containing_type=None, options=None, serialized_start=5679, serialized_end=5758)
_UNSETPLAYERREWARDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.UnsetPlayerRewardReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=1, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NOT_SET', index=2, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TYPE_OVERFLOW', index=3, number=4, options=None, type=None)], containing_type=None, options=None, serialized_start=5980, serialized_end=6055)
_QUERYPLAYERREWARDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.QueryPlayerRewardReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=1, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=5679, serialized_end=5722)
_QUERYPLAYERHEADIMAGEREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.QueryPlayerHeadImageReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=2149, serialized_end=2220)
_ADDFRIENDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.AddFriendReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SRC_NOT_EXIST', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TGT_NOT_EXIST', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MAX_FRIEND_LIMIT', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='IN_BLACK_LIST', index=5, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='ALREADY_FRIEND', index=6, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MAX_ADD_FRIEND_FREQUENT', index=7, number=7, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='AUTO_ADD_FRIEND', index=8, number=8, options=None, type=None)], containing_type=None, options=None, serialized_start=6885, serialized_end=7083)
_ACCEPTFRIENDREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.AcceptFriendReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SRC_NOT_EXIST', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TGT_NOT_EXIST', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MAX_FRIEND_LIMIT', index=4, number=4, options=None, type=None)], containing_type=None, options=None, serialized_start=6885, serialized_end=6994)
_YIXINFRIENDLISTREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.YixinFriendListReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='PLAYER_NOT_EXIST', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=2149, serialized_end=2220)
_UPDATEFRIENDALIASREPLY_ERROR = _descriptor.EnumDescriptor(name='Error', full_name='gt.yixin.UpdateFriendAliasReply.Error', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='NO_ERROR', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BAD_YIXIN_SERVER_REPLY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SRC_NOT_EXIST', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TGT_NOT_EXIST', index=3, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=6885, serialized_end=6972)
_REGISTERMSG = _descriptor.Descriptor(name='RegisterMsg', full_name='gt.yixin.RegisterMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.yixin.RegisterMsg.server', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='key', full_name='gt.yixin.RegisterMsg.key', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=39, serialized_end=81)
_PLAYER = _descriptor.Descriptor(name='Player', full_name='gt.yixin.Player', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.yixin.Player.uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=83, serialized_end=105)
_SENDERINFOS = _descriptor.Descriptor(name='SenderInfos', full_name='gt.yixin.SenderInfos', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='rolename', full_name='gt.yixin.SenderInfos.rolename', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='uuid', full_name='gt.yixin.SenderInfos.uuid', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='gender', full_name='gt.yixin.SenderInfos.gender', index=2, number=3, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='profession', full_name='gt.yixin.SenderInfos.profession', index=3, number=4, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='content', full_name='gt.yixin.SenderInfos.content', index=4, number=5, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=107, serialized_end=205)
_ARGS = _descriptor.Descriptor(name='Args', full_name='gt.yixin.Args', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='name', full_name='gt.yixin.Args.name', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='value', full_name='gt.yixin.Args.value', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=207, serialized_end=242)
_REGISTERYIXINREQUEST = _descriptor.Descriptor(name='RegisterYixinRequest', full_name='gt.yixin.RegisterYixinRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.RegisterYixinRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.RegisterYixinRequest.mobile', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='pwd', full_name='gt.yixin.RegisterYixinRequest.pwd', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='nick', full_name='gt.yixin.RegisterYixinRequest.nick', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=244, serialized_end=343)
_REGISTERYIXINREPLY = _descriptor.Descriptor(name='RegisterYixinReply', full_name='gt.yixin.RegisterYixinReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.RegisterYixinReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.RegisterYixinReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_REGISTERYIXINREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=346, serialized_end=512)
_BINDYIXINUSERREQUEST = _descriptor.Descriptor(name='BindYixinUserRequest', full_name='gt.yixin.BindYixinUserRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.BindYixinUserRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.BindYixinUserRequest.mobile', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='drill', full_name='gt.yixin.BindYixinUserRequest.drill', index=2, number=3, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=514, serialized_end=601)
_BINDYIXINUSERREPLY = _descriptor.Descriptor(name='BindYixinUserReply', full_name='gt.yixin.BindYixinUserReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.BindYixinUserReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.BindYixinUserReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='drill', full_name='gt.yixin.BindYixinUserReply.drill', index=2, number=3, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.BindYixinUserReply.mobile', index=3, number=4, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='openid', full_name='gt.yixin.BindYixinUserReply.openid', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cooldown', full_name='gt.yixin.BindYixinUserReply.cooldown', index=5, number=6, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_BINDYIXINUSERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=604, serialized_end=915)
_UNBINDYIXINUSERREQUEST = _descriptor.Descriptor(name='UnBindYixinUserRequest', full_name='gt.yixin.UnBindYixinUserRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.UnBindYixinUserRequest.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.UnBindYixinUserRequest.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=917, serialized_end=996)
_UNBINDYIXINUSERREPLY = _descriptor.Descriptor(name='UnBindYixinUserReply', full_name='gt.yixin.UnBindYixinUserReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.UnBindYixinUserReply.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.UnBindYixinUserReply.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.UnBindYixinUserReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_UNBINDYIXINUSERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=999, serialized_end=1190)
_SIGNREQUEST = _descriptor.Descriptor(name='SignRequest', full_name='gt.yixin.SignRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.SignRequest.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.SignRequest.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1192, serialized_end=1260)
_SIGNREPLY = _descriptor.Descriptor(name='SignReply', full_name='gt.yixin.SignReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.SignReply.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.SignReply.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='message', full_name='gt.yixin.SignReply.message', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1262, serialized_end=1345)
_CLAN = _descriptor.Descriptor(name='Clan', full_name='gt.yixin.Clan', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.yixin.Clan.uuid', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1347, serialized_end=1367)
_CREATECLANREQUEST = _descriptor.Descriptor(name='CreateClanRequest', full_name='gt.yixin.CreateClanRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.CreateClanRequest.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='name', full_name='gt.yixin.CreateClanRequest.name', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1369, serialized_end=1432)
_CREATECLANREPLY = _descriptor.Descriptor(name='CreateClanReply', full_name='gt.yixin.CreateClanReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.CreateClanReply.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.CreateClanReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tid', full_name='gt.yixin.CreateClanReply.tid', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_CREATECLANREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=1435, serialized_end=1659)
_RENAMECLANREQUEST = _descriptor.Descriptor(name='RenameClanRequest', full_name='gt.yixin.RenameClanRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.RenameClanRequest.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='name', full_name='gt.yixin.RenameClanRequest.name', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1661, serialized_end=1724)
_RENAMECLANREPLY = _descriptor.Descriptor(name='RenameClanReply', full_name='gt.yixin.RenameClanReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.RenameClanReply.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.RenameClanReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_RENAMECLANREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=1727, serialized_end=1897)
_ADDCLANMEMBERREQUEST = _descriptor.Descriptor(name='AddClanMemberRequest', full_name='gt.yixin.AddClanMemberRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.AddClanMemberRequest.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='member', full_name='gt.yixin.AddClanMemberRequest.member', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='nick', full_name='gt.yixin.AddClanMemberRequest.nick', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1899, serialized_end=1999)
_ADDCLANMEMBERREPLY = _descriptor.Descriptor(name='AddClanMemberReply', full_name='gt.yixin.AddClanMemberReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.AddClanMemberReply.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='member', full_name='gt.yixin.AddClanMemberReply.member', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.AddClanMemberReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_ADDCLANMEMBERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=2002, serialized_end=2234)
_REMOVECLANMEMBERREQUEST = _descriptor.Descriptor(name='RemoveClanMemberRequest', full_name='gt.yixin.RemoveClanMemberRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.RemoveClanMemberRequest.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='member', full_name='gt.yixin.RemoveClanMemberRequest.member', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2236, serialized_end=2325)
_REMOVECLANMEMBERREPLY = _descriptor.Descriptor(name='RemoveClanMemberReply', full_name='gt.yixin.RemoveClanMemberReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.RemoveClanMemberReply.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='member', full_name='gt.yixin.RemoveClanMemberReply.member', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.RemoveClanMemberReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_REMOVECLANMEMBERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=2328, serialized_end=2530)
_RENAMECLANMEMBERREQUEST = _descriptor.Descriptor(name='RenameClanMemberRequest', full_name='gt.yixin.RenameClanMemberRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.RenameClanMemberRequest.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='member', full_name='gt.yixin.RenameClanMemberRequest.member', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='nick', full_name='gt.yixin.RenameClanMemberRequest.nick', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2532, serialized_end=2635)
_CHATTOCLANMSG = _descriptor.Descriptor(name='ChatToClanMsg', full_name='gt.yixin.ChatToClanMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.ChatToClanMsg.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='talker', full_name='gt.yixin.ChatToClanMsg.talker', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='content', full_name='gt.yixin.ChatToClanMsg.content', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2637, serialized_end=2733)
_CLANCHATTOMSG = _descriptor.Descriptor(name='ClanChatToMsg', full_name='gt.yixin.ClanChatToMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.ClanChatToMsg.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='talker', full_name='gt.yixin.ClanChatToMsg.talker', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='talkerNick', full_name='gt.yixin.ClanChatToMsg.talkerNick', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='content', full_name='gt.yixin.ClanChatToMsg.content', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2735, serialized_end=2851)
_COUNTYIXINFRIENDREQUEST = _descriptor.Descriptor(name='CountYixinFriendRequest', full_name='gt.yixin.CountYixinFriendRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.CountYixinFriendRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='args', full_name='gt.yixin.CountYixinFriendRequest.args', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=2853, serialized_end=2942)
_COUNTYIXINFRIENDREPLY = _descriptor.Descriptor(name='CountYixinFriendReply', full_name='gt.yixin.CountYixinFriendReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.CountYixinFriendReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='count', full_name='gt.yixin.CountYixinFriendReply.count', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.CountYixinFriendReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='args', full_name='gt.yixin.CountYixinFriendReply.args', index=3, number=4, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_COUNTYIXINFRIENDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=2945, serialized_end=3162)
_FOLLOWPUBLICYIXINREQUEST = _descriptor.Descriptor(name='FollowPublicYixinRequest', full_name='gt.yixin.FollowPublicYixinRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.FollowPublicYixinRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3164, serialized_end=3224)
_FOLLOWPUBLICYIXINREPLY = _descriptor.Descriptor(name='FollowPublicYixinReply', full_name='gt.yixin.FollowPublicYixinReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.FollowPublicYixinReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.FollowPublicYixinReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_FOLLOWPUBLICYIXINREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=3227, serialized_end=3414)
_GAMESIDEUNBINDYIXINUSERREQUEST = _descriptor.Descriptor(name='GameSideUnBindYixinUserRequest', full_name='gt.yixin.GameSideUnBindYixinUserRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.GameSideUnBindYixinUserRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3416, serialized_end=3482)
_GAMESIDEUNBINDYIXINUSERREPLY = _descriptor.Descriptor(name='GameSideUnBindYixinUserReply', full_name='gt.yixin.GameSideUnBindYixinUserReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.GameSideUnBindYixinUserReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.GameSideUnBindYixinUserReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_GAMESIDEUNBINDYIXINUSERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=3485, serialized_end=3657)
_RESETCOOLDOWNMSG = _descriptor.Descriptor(name='ResetCooldownMsg', full_name='gt.yixin.ResetCooldownMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.ResetCooldownMsg.mobile', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3659, serialized_end=3693)
_REJOINCLANREQUEST = _descriptor.Descriptor(name='RejoinClanRequest', full_name='gt.yixin.RejoinClanRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.RejoinClanRequest.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.RejoinClanRequest.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3695, serialized_end=3769)
_REJOINCLANREPLY = _descriptor.Descriptor(name='RejoinClanReply', full_name='gt.yixin.RejoinClanReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.RejoinClanReply.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.RejoinClanReply.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='message', full_name='gt.yixin.RejoinClanReply.message', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3771, serialized_end=3860)
_IMAGETOCLANMSG = _descriptor.Descriptor(name='ImageToClanMsg', full_name='gt.yixin.ImageToClanMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.ImageToClanMsg.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='uploader', full_name='gt.yixin.ImageToClanMsg.uploader', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='image_url', full_name='gt.yixin.ImageToClanMsg.image_url', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3862, serialized_end=3963)
_QUERYYIXINUSERREQUEST = _descriptor.Descriptor(name='QueryYixinUserRequest', full_name='gt.yixin.QueryYixinUserRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryYixinUserRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.QueryYixinUserRequest.mobile', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=3965, serialized_end=4038)
_QUERYYIXINUSERREPLY = _descriptor.Descriptor(name='QueryYixinUserReply', full_name='gt.yixin.QueryYixinUserReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryYixinUserReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.QueryYixinUserReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.QueryYixinUserReply.mobile', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='server', full_name='gt.yixin.QueryYixinUserReply.server', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='openid', full_name='gt.yixin.QueryYixinUserReply.openid', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_QUERYYIXINUSERREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=4041, serialized_end=4302)
_QUERYCLANREQUEST = _descriptor.Descriptor(name='QueryClanRequest', full_name='gt.yixin.QueryClanRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.QueryClanRequest.clan', index=0, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4304, serialized_end=4352)
_QUERYCLANREPLY = _descriptor.Descriptor(name='QueryClanReply', full_name='gt.yixin.QueryClanReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='clan', full_name='gt.yixin.QueryClanReply.clan', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.QueryClanReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tid', full_name='gt.yixin.QueryClanReply.tid', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_QUERYCLANREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=4355, serialized_end=4507)
_GETPLAYERGENERALREQUEST = _descriptor.Descriptor(name='GetPlayerGeneralRequest', full_name='gt.yixin.GetPlayerGeneralRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.GetPlayerGeneralRequest.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.GetPlayerGeneralRequest.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4509, serialized_end=4589)
_GETPLAYERGENERALREPLY = _descriptor.Descriptor(name='GetPlayerGeneralReply', full_name='gt.yixin.GetPlayerGeneralReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='handle_name', full_name='gt.yixin.GetPlayerGeneralReply.handle_name', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.GetPlayerGeneralReply.player', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='errorcode', full_name='gt.yixin.GetPlayerGeneralReply.errorcode', index=2, number=3, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='result', full_name='gt.yixin.GetPlayerGeneralReply.result', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4591, serialized_end=4704)
_OPENIDS = _descriptor.Descriptor(name='OpenIDs', full_name='gt.yixin.OpenIDs', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='uuid', full_name='gt.yixin.OpenIDs.uuid', index=0, number=1, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='openid', full_name='gt.yixin.OpenIDs.openid', index=1, number=2, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4706, serialized_end=4745)
_ONECHATTOMSG = _descriptor.Descriptor(name='OneChatToMsg', full_name='gt.yixin.OneChatToMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.OneChatToMsg.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='senderinfos', full_name='gt.yixin.OneChatToMsg.senderinfos', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4747, serialized_end=4839)
_CHATTOONEMSG = _descriptor.Descriptor(name='ChatToOneMsg', full_name='gt.yixin.ChatToOneMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='talker', full_name='gt.yixin.ChatToOneMsg.talker', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='listener', full_name='gt.yixin.ChatToOneMsg.listener', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='content', full_name='gt.yixin.ChatToOneMsg.content', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4841, serialized_end=4942)
_GAMESIDEUNBINDMOBILEREQUEST = _descriptor.Descriptor(name='GameSideUnBindMobileRequest', full_name='gt.yixin.GameSideUnBindMobileRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.GameSideUnBindMobileRequest.mobile', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=4944, serialized_end=4989)
_GAMESIDEUNBINDMOBILEREPLY = _descriptor.Descriptor(name='GameSideUnBindMobileReply', full_name='gt.yixin.GameSideUnBindMobileReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.GameSideUnBindMobileReply.mobile', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.GameSideUnBindMobileReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_GAMESIDEUNBINDMOBILEREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=4992, serialized_end=5184)
_QUERYMOBILEREQUEST = _descriptor.Descriptor(name='QueryMobileRequest', full_name='gt.yixin.QueryMobileRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.QueryMobileRequest.mobile', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=5186, serialized_end=5222)
_QUERYMOBILEREPLY = _descriptor.Descriptor(name='QueryMobileReply', full_name='gt.yixin.QueryMobileReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='mobile', full_name='gt.yixin.QueryMobileReply.mobile', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.QueryMobileReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='openid', full_name='gt.yixin.QueryMobileReply.openid', index=2, number=3, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryMobileReply.player', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='server', full_name='gt.yixin.QueryMobileReply.server', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_QUERYMOBILEREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=5225, serialized_end=5463)
_SETPLAYERREWARDREQUEST = _descriptor.Descriptor(name='SetPlayerRewardRequest', full_name='gt.yixin.SetPlayerRewardRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.SetPlayerRewardRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reward', full_name='gt.yixin.SetPlayerRewardRequest.reward', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=5465, serialized_end=5539)
_SETPLAYERREWARDREPLY = _descriptor.Descriptor(name='SetPlayerRewardReply', full_name='gt.yixin.SetPlayerRewardReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.SetPlayerRewardReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.SetPlayerRewardReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reward', full_name='gt.yixin.SetPlayerRewardReply.reward', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_SETPLAYERREWARDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=5542, serialized_end=5758)
_UNSETPLAYERREWARDREQUEST = _descriptor.Descriptor(name='UnsetPlayerRewardRequest', full_name='gt.yixin.UnsetPlayerRewardRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.UnsetPlayerRewardRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reward', full_name='gt.yixin.UnsetPlayerRewardRequest.reward', index=1, number=2, type=13, cpp_type=3, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=5760, serialized_end=5836)
_UNSETPLAYERREWARDREPLY = _descriptor.Descriptor(name='UnsetPlayerRewardReply', full_name='gt.yixin.UnsetPlayerRewardReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.UnsetPlayerRewardReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.UnsetPlayerRewardReply.error', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reward', full_name='gt.yixin.UnsetPlayerRewardReply.reward', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_UNSETPLAYERREWARDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=5839, serialized_end=6055)
_QUERYPLAYERREWARDREQUEST = _descriptor.Descriptor(name='QueryPlayerRewardRequest', full_name='gt.yixin.QueryPlayerRewardRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryPlayerRewardRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=6057, serialized_end=6117)
_QUERYPLAYERREWARDREPLY = _descriptor.Descriptor(name='QueryPlayerRewardReply', full_name='gt.yixin.QueryPlayerRewardReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryPlayerRewardReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='reward', full_name='gt.yixin.QueryPlayerRewardReply.reward', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.QueryPlayerRewardReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_QUERYPLAYERREWARDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=6120, serialized_end=6294)
_QUERYPLAYERHEADIMAGEREQUEST = _descriptor.Descriptor(name='QueryPlayerHeadImageRequest', full_name='gt.yixin.QueryPlayerHeadImageRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryPlayerHeadImageRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='args', full_name='gt.yixin.QueryPlayerHeadImageRequest.args', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=6296, serialized_end=6389)
_QUERYPLAYERHEADIMAGEREPLY = _descriptor.Descriptor(name='QueryPlayerHeadImageReply', full_name='gt.yixin.QueryPlayerHeadImageReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.QueryPlayerHeadImageReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='headimgurl', full_name='gt.yixin.QueryPlayerHeadImageReply.headimgurl', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.QueryPlayerHeadImageReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='args', full_name='gt.yixin.QueryPlayerHeadImageReply.args', index=3, number=4, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_QUERYPLAYERHEADIMAGEREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=6392, serialized_end=6634)
_ADDFRIENDREQUEST = _descriptor.Descriptor(name='AddFriendRequest', full_name='gt.yixin.AddFriendRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.AddFriendRequest.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.AddFriendRequest.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='msg', full_name='gt.yixin.AddFriendRequest.msg', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=6636, serialized_end=6735)
_ADDFRIENDREPLY = _descriptor.Descriptor(name='AddFriendReply', full_name='gt.yixin.AddFriendReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.AddFriendReply.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.AddFriendReply.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.AddFriendReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='msg', full_name='gt.yixin.AddFriendReply.msg', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_ADDFRIENDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=6738, serialized_end=7083)
_ACCEPTFRIENDREQUEST = _descriptor.Descriptor(name='AcceptFriendRequest', full_name='gt.yixin.AcceptFriendRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.AcceptFriendRequest.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.AcceptFriendRequest.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=7085, serialized_end=7174)
_ACCEPTFRIENDREPLY = _descriptor.Descriptor(name='AcceptFriendReply', full_name='gt.yixin.AcceptFriendReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.AcceptFriendReply.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.AcceptFriendReply.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.AcceptFriendReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_ACCEPTFRIENDREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=7177, serialized_end=7425)
_YIXINFRIENDLISTREQUEST = _descriptor.Descriptor(name='YixinFriendListRequest', full_name='gt.yixin.YixinFriendListRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.YixinFriendListRequest.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=7427, serialized_end=7485)
_YIXINFRIENDLISTREPLY = _descriptor.Descriptor(name='YixinFriendListReply', full_name='gt.yixin.YixinFriendListReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='player', full_name='gt.yixin.YixinFriendListReply.player', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='openids', full_name='gt.yixin.YixinFriendListReply.openids', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.YixinFriendListReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_YIXINFRIENDLISTREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=7488, serialized_end=7687)
_UPDATEFRIENDALIASREQUEST = _descriptor.Descriptor(name='UpdateFriendAliasRequest', full_name='gt.yixin.UpdateFriendAliasRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.UpdateFriendAliasRequest.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.UpdateFriendAliasRequest.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='alias', full_name='gt.yixin.UpdateFriendAliasRequest.alias', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=7689, serialized_end=7798)
_UPDATEFRIENDALIASREPLY = _descriptor.Descriptor(name='UpdateFriendAliasReply', full_name='gt.yixin.UpdateFriendAliasReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='source', full_name='gt.yixin.UpdateFriendAliasReply.source', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='target', full_name='gt.yixin.UpdateFriendAliasReply.target', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='error', full_name='gt.yixin.UpdateFriendAliasReply.error', index=2, number=3, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[_UPDATEFRIENDALIASREPLY_ERROR], options=None, is_extendable=False, extension_ranges=[], serialized_start=7801, serialized_end=8037)
_PUBLICSENDP2PTEXTREQUEST = _descriptor.Descriptor(name='PublicSendP2PTextRequest', full_name='gt.yixin.PublicSendP2PTextRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='players', full_name='gt.yixin.PublicSendP2PTextRequest.players', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='text', full_name='gt.yixin.PublicSendP2PTextRequest.text', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=8039, serialized_end=8114)
_REGISTERYIXINREQUEST.fields_by_name['player'].message_type = _PLAYER
_REGISTERYIXINREPLY.fields_by_name['player'].message_type = _PLAYER
_REGISTERYIXINREPLY.fields_by_name['error'].enum_type = _REGISTERYIXINREPLY_ERROR
_REGISTERYIXINREPLY_ERROR.containing_type = _REGISTERYIXINREPLY
_BINDYIXINUSERREQUEST.fields_by_name['player'].message_type = _PLAYER
_BINDYIXINUSERREPLY.fields_by_name['player'].message_type = _PLAYER
_BINDYIXINUSERREPLY.fields_by_name['error'].enum_type = _BINDYIXINUSERREPLY_ERROR
_BINDYIXINUSERREPLY_ERROR.containing_type = _BINDYIXINUSERREPLY
_UNBINDYIXINUSERREQUEST.fields_by_name['player'].message_type = _PLAYER
_UNBINDYIXINUSERREPLY.fields_by_name['player'].message_type = _PLAYER
_UNBINDYIXINUSERREPLY.fields_by_name['error'].enum_type = _UNBINDYIXINUSERREPLY_ERROR
_UNBINDYIXINUSERREPLY_ERROR.containing_type = _UNBINDYIXINUSERREPLY
_SIGNREQUEST.fields_by_name['player'].message_type = _PLAYER
_SIGNREPLY.fields_by_name['player'].message_type = _PLAYER
_CREATECLANREQUEST.fields_by_name['clan'].message_type = _CLAN
_CREATECLANREPLY.fields_by_name['clan'].message_type = _CLAN
_CREATECLANREPLY.fields_by_name['error'].enum_type = _CREATECLANREPLY_ERROR
_CREATECLANREPLY_ERROR.containing_type = _CREATECLANREPLY
_RENAMECLANREQUEST.fields_by_name['clan'].message_type = _CLAN
_RENAMECLANREPLY.fields_by_name['clan'].message_type = _CLAN
_RENAMECLANREPLY.fields_by_name['error'].enum_type = _RENAMECLANREPLY_ERROR
_RENAMECLANREPLY_ERROR.containing_type = _RENAMECLANREPLY
_ADDCLANMEMBERREQUEST.fields_by_name['clan'].message_type = _CLAN
_ADDCLANMEMBERREQUEST.fields_by_name['member'].message_type = _PLAYER
_ADDCLANMEMBERREPLY.fields_by_name['clan'].message_type = _CLAN
_ADDCLANMEMBERREPLY.fields_by_name['member'].message_type = _PLAYER
_ADDCLANMEMBERREPLY.fields_by_name['error'].enum_type = _ADDCLANMEMBERREPLY_ERROR
_ADDCLANMEMBERREPLY_ERROR.containing_type = _ADDCLANMEMBERREPLY
_REMOVECLANMEMBERREQUEST.fields_by_name['clan'].message_type = _CLAN
_REMOVECLANMEMBERREQUEST.fields_by_name['member'].message_type = _PLAYER
_REMOVECLANMEMBERREPLY.fields_by_name['clan'].message_type = _CLAN
_REMOVECLANMEMBERREPLY.fields_by_name['member'].message_type = _PLAYER
_REMOVECLANMEMBERREPLY.fields_by_name['error'].enum_type = _REMOVECLANMEMBERREPLY_ERROR
_REMOVECLANMEMBERREPLY_ERROR.containing_type = _REMOVECLANMEMBERREPLY
_RENAMECLANMEMBERREQUEST.fields_by_name['clan'].message_type = _CLAN
_RENAMECLANMEMBERREQUEST.fields_by_name['member'].message_type = _PLAYER
_CHATTOCLANMSG.fields_by_name['clan'].message_type = _CLAN
_CHATTOCLANMSG.fields_by_name['talker'].message_type = _PLAYER
_CLANCHATTOMSG.fields_by_name['clan'].message_type = _CLAN
_CLANCHATTOMSG.fields_by_name['talker'].message_type = _PLAYER
_COUNTYIXINFRIENDREQUEST.fields_by_name['player'].message_type = _PLAYER
_COUNTYIXINFRIENDREQUEST.fields_by_name['args'].message_type = _ARGS
_COUNTYIXINFRIENDREPLY.fields_by_name['player'].message_type = _PLAYER
_COUNTYIXINFRIENDREPLY.fields_by_name['error'].enum_type = _COUNTYIXINFRIENDREPLY_ERROR
_COUNTYIXINFRIENDREPLY.fields_by_name['args'].message_type = _ARGS
_COUNTYIXINFRIENDREPLY_ERROR.containing_type = _COUNTYIXINFRIENDREPLY
_FOLLOWPUBLICYIXINREQUEST.fields_by_name['player'].message_type = _PLAYER
_FOLLOWPUBLICYIXINREPLY.fields_by_name['player'].message_type = _PLAYER
_FOLLOWPUBLICYIXINREPLY.fields_by_name['error'].enum_type = _FOLLOWPUBLICYIXINREPLY_ERROR
_FOLLOWPUBLICYIXINREPLY_ERROR.containing_type = _FOLLOWPUBLICYIXINREPLY
_GAMESIDEUNBINDYIXINUSERREQUEST.fields_by_name['player'].message_type = _PLAYER
_GAMESIDEUNBINDYIXINUSERREPLY.fields_by_name['player'].message_type = _PLAYER
_GAMESIDEUNBINDYIXINUSERREPLY.fields_by_name['error'].enum_type = _GAMESIDEUNBINDYIXINUSERREPLY_ERROR
_GAMESIDEUNBINDYIXINUSERREPLY_ERROR.containing_type = _GAMESIDEUNBINDYIXINUSERREPLY
_REJOINCLANREQUEST.fields_by_name['player'].message_type = _PLAYER
_REJOINCLANREPLY.fields_by_name['player'].message_type = _PLAYER
_IMAGETOCLANMSG.fields_by_name['clan'].message_type = _CLAN
_IMAGETOCLANMSG.fields_by_name['uploader'].message_type = _PLAYER
_QUERYYIXINUSERREQUEST.fields_by_name['player'].message_type = _PLAYER
_QUERYYIXINUSERREPLY.fields_by_name['player'].message_type = _PLAYER
_QUERYYIXINUSERREPLY.fields_by_name['error'].enum_type = _QUERYYIXINUSERREPLY_ERROR
_QUERYYIXINUSERREPLY_ERROR.containing_type = _QUERYYIXINUSERREPLY
_QUERYCLANREQUEST.fields_by_name['clan'].message_type = _CLAN
_QUERYCLANREPLY.fields_by_name['clan'].message_type = _CLAN
_QUERYCLANREPLY.fields_by_name['error'].enum_type = _QUERYCLANREPLY_ERROR
_QUERYCLANREPLY_ERROR.containing_type = _QUERYCLANREPLY
_GETPLAYERGENERALREQUEST.fields_by_name['player'].message_type = _PLAYER
_GETPLAYERGENERALREPLY.fields_by_name['player'].message_type = _PLAYER
_ONECHATTOMSG.fields_by_name['player'].message_type = _PLAYER
_ONECHATTOMSG.fields_by_name['senderinfos'].message_type = _SENDERINFOS
_CHATTOONEMSG.fields_by_name['talker'].message_type = _PLAYER
_CHATTOONEMSG.fields_by_name['listener'].message_type = _PLAYER
_GAMESIDEUNBINDMOBILEREPLY.fields_by_name['error'].enum_type = _GAMESIDEUNBINDMOBILEREPLY_ERROR
_GAMESIDEUNBINDMOBILEREPLY_ERROR.containing_type = _GAMESIDEUNBINDMOBILEREPLY
_QUERYMOBILEREPLY.fields_by_name['error'].enum_type = _QUERYMOBILEREPLY_ERROR
_QUERYMOBILEREPLY.fields_by_name['player'].message_type = _PLAYER
_QUERYMOBILEREPLY_ERROR.containing_type = _QUERYMOBILEREPLY
_SETPLAYERREWARDREQUEST.fields_by_name['player'].message_type = _PLAYER
_SETPLAYERREWARDREPLY.fields_by_name['player'].message_type = _PLAYER
_SETPLAYERREWARDREPLY.fields_by_name['error'].enum_type = _SETPLAYERREWARDREPLY_ERROR
_SETPLAYERREWARDREPLY_ERROR.containing_type = _SETPLAYERREWARDREPLY
_UNSETPLAYERREWARDREQUEST.fields_by_name['player'].message_type = _PLAYER
_UNSETPLAYERREWARDREPLY.fields_by_name['player'].message_type = _PLAYER
_UNSETPLAYERREWARDREPLY.fields_by_name['error'].enum_type = _UNSETPLAYERREWARDREPLY_ERROR
_UNSETPLAYERREWARDREPLY_ERROR.containing_type = _UNSETPLAYERREWARDREPLY
_QUERYPLAYERREWARDREQUEST.fields_by_name['player'].message_type = _PLAYER
_QUERYPLAYERREWARDREPLY.fields_by_name['player'].message_type = _PLAYER
_QUERYPLAYERREWARDREPLY.fields_by_name['error'].enum_type = _QUERYPLAYERREWARDREPLY_ERROR
_QUERYPLAYERREWARDREPLY_ERROR.containing_type = _QUERYPLAYERREWARDREPLY
_QUERYPLAYERHEADIMAGEREQUEST.fields_by_name['player'].message_type = _PLAYER
_QUERYPLAYERHEADIMAGEREQUEST.fields_by_name['args'].message_type = _ARGS
_QUERYPLAYERHEADIMAGEREPLY.fields_by_name['player'].message_type = _PLAYER
_QUERYPLAYERHEADIMAGEREPLY.fields_by_name['error'].enum_type = _QUERYPLAYERHEADIMAGEREPLY_ERROR
_QUERYPLAYERHEADIMAGEREPLY.fields_by_name['args'].message_type = _ARGS
_QUERYPLAYERHEADIMAGEREPLY_ERROR.containing_type = _QUERYPLAYERHEADIMAGEREPLY
_ADDFRIENDREQUEST.fields_by_name['source'].message_type = _PLAYER
_ADDFRIENDREQUEST.fields_by_name['target'].message_type = _PLAYER
_ADDFRIENDREPLY.fields_by_name['source'].message_type = _PLAYER
_ADDFRIENDREPLY.fields_by_name['target'].message_type = _PLAYER
_ADDFRIENDREPLY.fields_by_name['error'].enum_type = _ADDFRIENDREPLY_ERROR
_ADDFRIENDREPLY_ERROR.containing_type = _ADDFRIENDREPLY
_ACCEPTFRIENDREQUEST.fields_by_name['source'].message_type = _PLAYER
_ACCEPTFRIENDREQUEST.fields_by_name['target'].message_type = _PLAYER
_ACCEPTFRIENDREPLY.fields_by_name['source'].message_type = _PLAYER
_ACCEPTFRIENDREPLY.fields_by_name['target'].message_type = _PLAYER
_ACCEPTFRIENDREPLY.fields_by_name['error'].enum_type = _ACCEPTFRIENDREPLY_ERROR
_ACCEPTFRIENDREPLY_ERROR.containing_type = _ACCEPTFRIENDREPLY
_YIXINFRIENDLISTREQUEST.fields_by_name['player'].message_type = _PLAYER
_YIXINFRIENDLISTREPLY.fields_by_name['player'].message_type = _PLAYER
_YIXINFRIENDLISTREPLY.fields_by_name['error'].enum_type = _YIXINFRIENDLISTREPLY_ERROR
_YIXINFRIENDLISTREPLY_ERROR.containing_type = _YIXINFRIENDLISTREPLY
_UPDATEFRIENDALIASREQUEST.fields_by_name['source'].message_type = _PLAYER
_UPDATEFRIENDALIASREQUEST.fields_by_name['target'].message_type = _PLAYER
_UPDATEFRIENDALIASREPLY.fields_by_name['source'].message_type = _PLAYER
_UPDATEFRIENDALIASREPLY.fields_by_name['target'].message_type = _PLAYER
_UPDATEFRIENDALIASREPLY.fields_by_name['error'].enum_type = _UPDATEFRIENDALIASREPLY_ERROR
_UPDATEFRIENDALIASREPLY_ERROR.containing_type = _UPDATEFRIENDALIASREPLY
_PUBLICSENDP2PTEXTREQUEST.fields_by_name['players'].message_type = _PLAYER
DESCRIPTOR.message_types_by_name['RegisterMsg'] = _REGISTERMSG
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['SenderInfos'] = _SENDERINFOS
DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['RegisterYixinRequest'] = _REGISTERYIXINREQUEST
DESCRIPTOR.message_types_by_name['RegisterYixinReply'] = _REGISTERYIXINREPLY
DESCRIPTOR.message_types_by_name['BindYixinUserRequest'] = _BINDYIXINUSERREQUEST
DESCRIPTOR.message_types_by_name['BindYixinUserReply'] = _BINDYIXINUSERREPLY
DESCRIPTOR.message_types_by_name['UnBindYixinUserRequest'] = _UNBINDYIXINUSERREQUEST
DESCRIPTOR.message_types_by_name['UnBindYixinUserReply'] = _UNBINDYIXINUSERREPLY
DESCRIPTOR.message_types_by_name['SignRequest'] = _SIGNREQUEST
DESCRIPTOR.message_types_by_name['SignReply'] = _SIGNREPLY
DESCRIPTOR.message_types_by_name['Clan'] = _CLAN
DESCRIPTOR.message_types_by_name['CreateClanRequest'] = _CREATECLANREQUEST
DESCRIPTOR.message_types_by_name['CreateClanReply'] = _CREATECLANREPLY
DESCRIPTOR.message_types_by_name['RenameClanRequest'] = _RENAMECLANREQUEST
DESCRIPTOR.message_types_by_name['RenameClanReply'] = _RENAMECLANREPLY
DESCRIPTOR.message_types_by_name['AddClanMemberRequest'] = _ADDCLANMEMBERREQUEST
DESCRIPTOR.message_types_by_name['AddClanMemberReply'] = _ADDCLANMEMBERREPLY
DESCRIPTOR.message_types_by_name['RemoveClanMemberRequest'] = _REMOVECLANMEMBERREQUEST
DESCRIPTOR.message_types_by_name['RemoveClanMemberReply'] = _REMOVECLANMEMBERREPLY
DESCRIPTOR.message_types_by_name['RenameClanMemberRequest'] = _RENAMECLANMEMBERREQUEST
DESCRIPTOR.message_types_by_name['ChatToClanMsg'] = _CHATTOCLANMSG
DESCRIPTOR.message_types_by_name['ClanChatToMsg'] = _CLANCHATTOMSG
DESCRIPTOR.message_types_by_name['CountYixinFriendRequest'] = _COUNTYIXINFRIENDREQUEST
DESCRIPTOR.message_types_by_name['CountYixinFriendReply'] = _COUNTYIXINFRIENDREPLY
DESCRIPTOR.message_types_by_name['FollowPublicYixinRequest'] = _FOLLOWPUBLICYIXINREQUEST
DESCRIPTOR.message_types_by_name['FollowPublicYixinReply'] = _FOLLOWPUBLICYIXINREPLY
DESCRIPTOR.message_types_by_name['GameSideUnBindYixinUserRequest'] = _GAMESIDEUNBINDYIXINUSERREQUEST
DESCRIPTOR.message_types_by_name['GameSideUnBindYixinUserReply'] = _GAMESIDEUNBINDYIXINUSERREPLY
DESCRIPTOR.message_types_by_name['ResetCooldownMsg'] = _RESETCOOLDOWNMSG
DESCRIPTOR.message_types_by_name['RejoinClanRequest'] = _REJOINCLANREQUEST
DESCRIPTOR.message_types_by_name['RejoinClanReply'] = _REJOINCLANREPLY
DESCRIPTOR.message_types_by_name['ImageToClanMsg'] = _IMAGETOCLANMSG
DESCRIPTOR.message_types_by_name['QueryYixinUserRequest'] = _QUERYYIXINUSERREQUEST
DESCRIPTOR.message_types_by_name['QueryYixinUserReply'] = _QUERYYIXINUSERREPLY
DESCRIPTOR.message_types_by_name['QueryClanRequest'] = _QUERYCLANREQUEST
DESCRIPTOR.message_types_by_name['QueryClanReply'] = _QUERYCLANREPLY
DESCRIPTOR.message_types_by_name['GetPlayerGeneralRequest'] = _GETPLAYERGENERALREQUEST
DESCRIPTOR.message_types_by_name['GetPlayerGeneralReply'] = _GETPLAYERGENERALREPLY
DESCRIPTOR.message_types_by_name['OpenIDs'] = _OPENIDS
DESCRIPTOR.message_types_by_name['OneChatToMsg'] = _ONECHATTOMSG
DESCRIPTOR.message_types_by_name['ChatToOneMsg'] = _CHATTOONEMSG
DESCRIPTOR.message_types_by_name['GameSideUnBindMobileRequest'] = _GAMESIDEUNBINDMOBILEREQUEST
DESCRIPTOR.message_types_by_name['GameSideUnBindMobileReply'] = _GAMESIDEUNBINDMOBILEREPLY
DESCRIPTOR.message_types_by_name['QueryMobileRequest'] = _QUERYMOBILEREQUEST
DESCRIPTOR.message_types_by_name['QueryMobileReply'] = _QUERYMOBILEREPLY
DESCRIPTOR.message_types_by_name['SetPlayerRewardRequest'] = _SETPLAYERREWARDREQUEST
DESCRIPTOR.message_types_by_name['SetPlayerRewardReply'] = _SETPLAYERREWARDREPLY
DESCRIPTOR.message_types_by_name['UnsetPlayerRewardRequest'] = _UNSETPLAYERREWARDREQUEST
DESCRIPTOR.message_types_by_name['UnsetPlayerRewardReply'] = _UNSETPLAYERREWARDREPLY
DESCRIPTOR.message_types_by_name['QueryPlayerRewardRequest'] = _QUERYPLAYERREWARDREQUEST
DESCRIPTOR.message_types_by_name['QueryPlayerRewardReply'] = _QUERYPLAYERREWARDREPLY
DESCRIPTOR.message_types_by_name['QueryPlayerHeadImageRequest'] = _QUERYPLAYERHEADIMAGEREQUEST
DESCRIPTOR.message_types_by_name['QueryPlayerHeadImageReply'] = _QUERYPLAYERHEADIMAGEREPLY
DESCRIPTOR.message_types_by_name['AddFriendRequest'] = _ADDFRIENDREQUEST
DESCRIPTOR.message_types_by_name['AddFriendReply'] = _ADDFRIENDREPLY
DESCRIPTOR.message_types_by_name['AcceptFriendRequest'] = _ACCEPTFRIENDREQUEST
DESCRIPTOR.message_types_by_name['AcceptFriendReply'] = _ACCEPTFRIENDREPLY
DESCRIPTOR.message_types_by_name['YixinFriendListRequest'] = _YIXINFRIENDLISTREQUEST
DESCRIPTOR.message_types_by_name['YixinFriendListReply'] = _YIXINFRIENDLISTREPLY
DESCRIPTOR.message_types_by_name['UpdateFriendAliasRequest'] = _UPDATEFRIENDALIASREQUEST
DESCRIPTOR.message_types_by_name['UpdateFriendAliasReply'] = _UPDATEFRIENDALIASREPLY
DESCRIPTOR.message_types_by_name['PublicSendP2PTextRequest'] = _PUBLICSENDP2PTEXTREQUEST

class RegisterMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGISTERMSG


class Player(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYER


class SenderInfos(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SENDERINFOS


class Args(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ARGS


class RegisterYixinRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGISTERYIXINREQUEST


class RegisterYixinReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGISTERYIXINREPLY


class BindYixinUserRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _BINDYIXINUSERREQUEST


class BindYixinUserReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _BINDYIXINUSERREPLY


class UnBindYixinUserRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNBINDYIXINUSERREQUEST


class UnBindYixinUserReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNBINDYIXINUSERREPLY


class SignRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SIGNREQUEST


class SignReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SIGNREPLY


class Clan(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CLAN


class CreateClanRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CREATECLANREQUEST


class CreateClanReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CREATECLANREPLY


class RenameClanRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RENAMECLANREQUEST


class RenameClanReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RENAMECLANREPLY


class AddClanMemberRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ADDCLANMEMBERREQUEST


class AddClanMemberReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ADDCLANMEMBERREPLY


class RemoveClanMemberRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REMOVECLANMEMBERREQUEST


class RemoveClanMemberReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REMOVECLANMEMBERREPLY


class RenameClanMemberRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RENAMECLANMEMBERREQUEST


class ChatToClanMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CHATTOCLANMSG


class ClanChatToMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CLANCHATTOMSG


class CountYixinFriendRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _COUNTYIXINFRIENDREQUEST


class CountYixinFriendReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _COUNTYIXINFRIENDREPLY


class FollowPublicYixinRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FOLLOWPUBLICYIXINREQUEST


class FollowPublicYixinReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FOLLOWPUBLICYIXINREPLY


class GameSideUnBindYixinUserRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDEUNBINDYIXINUSERREQUEST


class GameSideUnBindYixinUserReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDEUNBINDYIXINUSERREPLY


class ResetCooldownMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RESETCOOLDOWNMSG


class RejoinClanRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REJOINCLANREQUEST


class RejoinClanReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REJOINCLANREPLY


class ImageToClanMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _IMAGETOCLANMSG


class QueryYixinUserRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYYIXINUSERREQUEST


class QueryYixinUserReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYYIXINUSERREPLY


class QueryClanRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYCLANREQUEST


class QueryClanReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYCLANREPLY


class GetPlayerGeneralRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETPLAYERGENERALREQUEST


class GetPlayerGeneralReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GETPLAYERGENERALREPLY


class OpenIDs(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _OPENIDS


class OneChatToMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ONECHATTOMSG


class ChatToOneMsg(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CHATTOONEMSG


class GameSideUnBindMobileRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDEUNBINDMOBILEREQUEST


class GameSideUnBindMobileReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _GAMESIDEUNBINDMOBILEREPLY


class QueryMobileRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYMOBILEREQUEST


class QueryMobileReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYMOBILEREPLY


class SetPlayerRewardRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETPLAYERREWARDREQUEST


class SetPlayerRewardReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SETPLAYERREWARDREPLY


class UnsetPlayerRewardRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNSETPLAYERREWARDREQUEST


class UnsetPlayerRewardReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UNSETPLAYERREWARDREPLY


class QueryPlayerRewardRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYPLAYERREWARDREQUEST


class QueryPlayerRewardReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYPLAYERREWARDREPLY


class QueryPlayerHeadImageRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYPLAYERHEADIMAGEREQUEST


class QueryPlayerHeadImageReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _QUERYPLAYERHEADIMAGEREPLY


class AddFriendRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ADDFRIENDREQUEST


class AddFriendReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ADDFRIENDREPLY


class AcceptFriendRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ACCEPTFRIENDREQUEST


class AcceptFriendReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ACCEPTFRIENDREPLY


class YixinFriendListRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _YIXINFRIENDLISTREQUEST


class YixinFriendListReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _YIXINFRIENDLISTREPLY


class UpdateFriendAliasRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UPDATEFRIENDALIASREQUEST


class UpdateFriendAliasReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UPDATEFRIENDALIASREPLY


class PublicSendP2PTextRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PUBLICSENDP2PTEXTREQUEST


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '��')
_YIXINSERVER = _descriptor.ServiceDescriptor(name='YixinServer', full_name='gt.yixin.YixinServer', file=DESCRIPTOR, index=0, options=None, serialized_start=8117, serialized_end=10374, methods=[_descriptor.MethodDescriptor(name='Register', full_name='gt.yixin.YixinServer.Register', index=0, containing_service=None, input_type=_REGISTERMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqRegisterYixin', full_name='gt.yixin.YixinServer.ReqRegisterYixin', index=1, containing_service=None, input_type=_REGISTERYIXINREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqBindYixinUser', full_name='gt.yixin.YixinServer.ReqBindYixinUser', index=2, containing_service=None, input_type=_BINDYIXINUSERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepUnBindYixinUser', full_name='gt.yixin.YixinServer.RepUnBindYixinUser', index=3, containing_service=None, input_type=_UNBINDYIXINUSERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepSign', full_name='gt.yixin.YixinServer.RepSign', index=4, containing_service=None, input_type=_SIGNREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqCreateClan', full_name='gt.yixin.YixinServer.ReqCreateClan', index=5, containing_service=None, input_type=_CREATECLANREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqRenameClan', full_name='gt.yixin.YixinServer.ReqRenameClan', index=6, containing_service=None, input_type=_RENAMECLANREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqDisbandClan', full_name='gt.yixin.YixinServer.ReqDisbandClan', index=7, containing_service=None, input_type=_CLAN, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqAddClanMember', full_name='gt.yixin.YixinServer.ReqAddClanMember', index=8, containing_service=None, input_type=_ADDCLANMEMBERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqRenameClanMember', full_name='gt.yixin.YixinServer.ReqRenameClanMember', index=9, containing_service=None, input_type=_RENAMECLANMEMBERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqRemoveClanMember', full_name='gt.yixin.YixinServer.ReqRemoveClanMember', index=10, containing_service=None, input_type=_REMOVECLANMEMBERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ClanChatTo', full_name='gt.yixin.YixinServer.ClanChatTo', index=11, containing_service=None, input_type=_CLANCHATTOMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqCountYixinFriend', full_name='gt.yixin.YixinServer.ReqCountYixinFriend', index=12, containing_service=None, input_type=_COUNTYIXINFRIENDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqFollowPublicYixin', full_name='gt.yixin.YixinServer.ReqFollowPublicYixin', index=13, containing_service=None, input_type=_FOLLOWPUBLICYIXINREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGameSideUnBind', full_name='gt.yixin.YixinServer.ReqGameSideUnBind', index=14, containing_service=None, input_type=_GAMESIDEUNBINDYIXINUSERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ResetCooldown', full_name='gt.yixin.YixinServer.ResetCooldown', index=15, containing_service=None, input_type=_RESETCOOLDOWNMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepRejoinClan', full_name='gt.yixin.YixinServer.RepRejoinClan', index=16, containing_service=None, input_type=_REJOINCLANREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqQueryYixinUser', full_name='gt.yixin.YixinServer.ReqQueryYixinUser', index=17, containing_service=None, input_type=_QUERYYIXINUSERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqQueryClan', full_name='gt.yixin.YixinServer.ReqQueryClan', index=18, containing_service=None, input_type=_QUERYCLANREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetPlayerFriends', full_name='gt.yixin.YixinServer.RepGetPlayerFriends', index=19, containing_service=None, input_type=_GETPLAYERGENERALREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetPlayerClan', full_name='gt.yixin.YixinServer.RepGetPlayerClan', index=20, containing_service=None, input_type=_GETPLAYERGENERALREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetPlayerStatus', full_name='gt.yixin.YixinServer.RepGetPlayerStatus', index=21, containing_service=None, input_type=_GETPLAYERGENERALREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGetPlayerInfo', full_name='gt.yixin.YixinServer.RepGetPlayerInfo', index=22, containing_service=None, input_type=_GETPLAYERGENERALREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqPushOpenIDs', full_name='gt.yixin.YixinServer.ReqPushOpenIDs', index=23, containing_service=None, input_type=_PLAYER, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='BindRoleID', full_name='gt.yixin.YixinServer.BindRoleID', index=24, containing_service=None, input_type=_PLAYER, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='OneChatTo', full_name='gt.yixin.YixinServer.OneChatTo', index=25, containing_service=None, input_type=_ONECHATTOMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGameSideUnBindMobile', full_name='gt.yixin.YixinServer.ReqGameSideUnBindMobile', index=26, containing_service=None, input_type=_GAMESIDEUNBINDMOBILEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqQueryMobile', full_name='gt.yixin.YixinServer.ReqQueryMobile', index=27, containing_service=None, input_type=_QUERYMOBILEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqQueryPlayerReward', full_name='gt.yixin.YixinServer.ReqQueryPlayerReward', index=28, containing_service=None, input_type=_QUERYPLAYERREWARDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqSetPlayerReward', full_name='gt.yixin.YixinServer.ReqSetPlayerReward', index=29, containing_service=None, input_type=_SETPLAYERREWARDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqQueryPlayerHeadImage', full_name='gt.yixin.YixinServer.ReqQueryPlayerHeadImage', index=30, containing_service=None, input_type=_QUERYPLAYERHEADIMAGEREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqAddFriend', full_name='gt.yixin.YixinServer.ReqAddFriend', index=31, containing_service=None, input_type=_ADDFRIENDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqAcceptFriend', full_name='gt.yixin.YixinServer.ReqAcceptFriend', index=32, containing_service=None, input_type=_ACCEPTFRIENDREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqYixinFriendList', full_name='gt.yixin.YixinServer.ReqYixinFriendList', index=33, containing_service=None, input_type=_YIXINFRIENDLISTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqUpdateFriendAlias', full_name='gt.yixin.YixinServer.ReqUpdateFriendAlias', index=34, containing_service=None, input_type=_UPDATEFRIENDALIASREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqPublicSendP2PText', full_name='gt.yixin.YixinServer.ReqPublicSendP2PText', index=35, containing_service=None, input_type=_PUBLICSENDP2PTEXTREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqUnsetPlayerReward', full_name='gt.yixin.YixinServer.ReqUnsetPlayerReward', index=36, containing_service=None, input_type=_UNSETPLAYERREWARDREQUEST, output_type=common_pb2._VOID, options=None)])

class YixinServer(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _YIXINSERVER


class YixinServer_Stub(YixinServer):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _YIXINSERVER


_YIXINCLIENT = _descriptor.ServiceDescriptor(name='YixinClient', full_name='gt.yixin.YixinClient', file=DESCRIPTOR, index=1, options=None, serialized_start=10377, serialized_end=12334, methods=[_descriptor.MethodDescriptor(name='RepRegisterYixin', full_name='gt.yixin.YixinClient.RepRegisterYixin', index=0, containing_service=None, input_type=_REGISTERYIXINREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepBindYixinUser', full_name='gt.yixin.YixinClient.RepBindYixinUser', index=1, containing_service=None, input_type=_BINDYIXINUSERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqUnBindYixinUser', full_name='gt.yixin.YixinClient.ReqUnBindYixinUser', index=2, containing_service=None, input_type=_UNBINDYIXINUSERREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqSign', full_name='gt.yixin.YixinClient.ReqSign', index=3, containing_service=None, input_type=_SIGNREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepCreateClan', full_name='gt.yixin.YixinClient.RepCreateClan', index=4, containing_service=None, input_type=_CREATECLANREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepRenameClan', full_name='gt.yixin.YixinClient.RepRenameClan', index=5, containing_service=None, input_type=_RENAMECLANREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepAddClanMember', full_name='gt.yixin.YixinClient.RepAddClanMember', index=6, containing_service=None, input_type=_ADDCLANMEMBERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepRemoveClanMember', full_name='gt.yixin.YixinClient.RepRemoveClanMember', index=7, containing_service=None, input_type=_REMOVECLANMEMBERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ChatToClan', full_name='gt.yixin.YixinClient.ChatToClan', index=8, containing_service=None, input_type=_CHATTOCLANMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepCountYixinFriend', full_name='gt.yixin.YixinClient.RepCountYixinFriend', index=9, containing_service=None, input_type=_COUNTYIXINFRIENDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepFollowPublicYixin', full_name='gt.yixin.YixinClient.RepFollowPublicYixin', index=10, containing_service=None, input_type=_FOLLOWPUBLICYIXINREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGameSideUnBind', full_name='gt.yixin.YixinClient.RepGameSideUnBind', index=11, containing_service=None, input_type=_GAMESIDEUNBINDYIXINUSERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqRejoinClan', full_name='gt.yixin.YixinClient.ReqRejoinClan', index=12, containing_service=None, input_type=_REJOINCLANREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ImageToClan', full_name='gt.yixin.YixinClient.ImageToClan', index=13, containing_service=None, input_type=_IMAGETOCLANMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepQueryYixinUser', full_name='gt.yixin.YixinClient.RepQueryYixinUser', index=14, containing_service=None, input_type=_QUERYYIXINUSERREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepQueryClan', full_name='gt.yixin.YixinClient.RepQueryClan', index=15, containing_service=None, input_type=_QUERYCLANREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetPlayerFriends', full_name='gt.yixin.YixinClient.ReqGetPlayerFriends', index=16, containing_service=None, input_type=_GETPLAYERGENERALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetPlayerClan', full_name='gt.yixin.YixinClient.ReqGetPlayerClan', index=17, containing_service=None, input_type=_GETPLAYERGENERALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetPlayerStatus', full_name='gt.yixin.YixinClient.ReqGetPlayerStatus', index=18, containing_service=None, input_type=_GETPLAYERGENERALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ReqGetPlayerInfo', full_name='gt.yixin.YixinClient.ReqGetPlayerInfo', index=19, containing_service=None, input_type=_GETPLAYERGENERALREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepPushOpenIDs', full_name='gt.yixin.YixinClient.RepPushOpenIDs', index=20, containing_service=None, input_type=_OPENIDS, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='ChatToOne', full_name='gt.yixin.YixinClient.ChatToOne', index=21, containing_service=None, input_type=_CHATTOONEMSG, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepGameSideUnBindMobile', full_name='gt.yixin.YixinClient.RepGameSideUnBindMobile', index=22, containing_service=None, input_type=_GAMESIDEUNBINDMOBILEREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepQueryMobile', full_name='gt.yixin.YixinClient.RepQueryMobile', index=23, containing_service=None, input_type=_QUERYMOBILEREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepQueryPlayerReward', full_name='gt.yixin.YixinClient.RepQueryPlayerReward', index=24, containing_service=None, input_type=_QUERYPLAYERREWARDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepSetPlayerReward', full_name='gt.yixin.YixinClient.RepSetPlayerReward', index=25, containing_service=None, input_type=_SETPLAYERREWARDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepQueryPlayerHeadImage', full_name='gt.yixin.YixinClient.RepQueryPlayerHeadImage', index=26, containing_service=None, input_type=_QUERYPLAYERHEADIMAGEREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepAddFriend', full_name='gt.yixin.YixinClient.RepAddFriend', index=27, containing_service=None, input_type=_ADDFRIENDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepAcceptFriend', full_name='gt.yixin.YixinClient.RepAcceptFriend', index=28, containing_service=None, input_type=_ACCEPTFRIENDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepYixinFriendList', full_name='gt.yixin.YixinClient.RepYixinFriendList', index=29, containing_service=None, input_type=_YIXINFRIENDLISTREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepUpdateFriendAlias', full_name='gt.yixin.YixinClient.RepUpdateFriendAlias', index=30, containing_service=None, input_type=_UPDATEFRIENDALIASREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='RepUnsetPlayerReward', full_name='gt.yixin.YixinClient.RepUnsetPlayerReward', index=31, containing_service=None, input_type=_UNSETPLAYERREWARDREPLY, output_type=common_pb2._VOID, options=None)])

class YixinClient(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _YIXINCLIENT


class YixinClient_Stub(YixinClient):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _YIXINCLIENT
