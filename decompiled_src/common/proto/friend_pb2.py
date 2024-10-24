#Embedded file name: I:/bag/tmp/tw2/res/entities\common\proto/friend_pb2.o
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
import common_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='friend.proto', package='gt.frnd', serialized_pb='\nfriend.protogt.frndcommon.proto\"\nPlayerId\ngbId (\"J\n\nPlayerInfo\ngbId (\nserver (\nroleName (\ndata (\"4\nPlayerInfoList\"\ninfos (2.gt.frnd.PlayerInfo\"e\nMoveLocalFriendToRemote&\n	srcPlayer (2.gt.frnd.PlayerInfo\"\ninfos (2.gt.frnd.PlayerInfo\"\\\nPlayerRelation$\n	srcPlayer (2.gt.frnd.PlayerId$\n	tgtPlayer (2.gt.frnd.PlayerId\"v\nUpdatePlayerRelationDetail$\n	srcPlayer (2.gt.frnd.PlayerId$\n	tgtPlayer (2.gt.frnd.PlayerId\ndata (\"\nRegHostInfo\nserver (\"?\n\nFriendInfo\ngbId (\ndata (\nonline (:false\"F\nPlayerRelationList\ngbId (\"\ninfos (2.gt.frnd.FriendInfo\"W\nPlayerInfoUpdated\nwho (2.gt.frnd.PlayerId\"\nfriends (2.gt.frnd.PlayerId\"L\nPlayerInfoOnlineStateUpdated,\nrelation (2.gt.frnd.PlayerInfoUpdated\"A\nPlayerInfoRemoved,\nrelation (2.gt.frnd.PlayerInfoUpdated\"i\nPlayerInfoUpdatedBasic,\nrelation (2.gt.frnd.PlayerInfoUpdated!\ninfo (2.gt.frnd.PlayerInfo\"-\n\rRemoteMessage\nserver (\ndata (\"-\nOnRemoteMessage\nhost (\ndata (\"E\nBatchPlayerInfoRequest\nids (2.gt.frnd.PlayerId\ntag (\"J\nBatchPlayerInfoReply%\ndata (2.gt.frnd.PlayerInfoList\ntag (\"Q\nAddFriendReply\ngbId (!\ninfo (2.gt.frnd.PlayerInfo\nonline (\"D\nRemoveFriendReply\ngbId (!\ninfo (2.gt.frnd.PlayerInfo*)\nGender\nMALE \n\nFEMALE	\nOTHER2�\n\rServerService)\nregHost.gt.frnd.RegHostInfo.gt.Void1\nreqAddPlayerInfo.gt.frnd.PlayerInfo.gt.Void4\nreqUpdatePlayerInfo.gt.frnd.PlayerInfo.gt.Void2\nreqRemovePlayerInfo.gt.frnd.PlayerId.gt.Void7\nreqAddPlayerFriend.gt.frnd.PlayerRelation.gt.Void:\nreqRemovePlayerFriend.gt.frnd.PlayerRelation.gt.VoidF\nreqUpdatePlayerFriend#.gt.frnd.UpdatePlayerRelationDetail.gt.Void2\nreqGetPlayerFriends.gt.frnd.PlayerId.gt.Void.\nreqPlayerOnline.gt.frnd.PlayerId.gt.Void/\nreqPlayerOffline.gt.frnd.PlayerId.gt.Void1\n\rreqCallMethod.gt.frnd.RemoteMessage.gt.Void>\nreqGetPlayersInfo.gt.frnd.BatchPlayerInfoRequest.gt.VoidG\nreqMoveLocalFriendToRmote .gt.frnd.MoveLocalFriendToRemote.gt.Void2�\n\rClientService>\nrepGetPlayerRelations.gt.frnd.PlayerRelationList.gt.VoidB\nrepPlayerOnline%.gt.frnd.PlayerInfoOnlineStateUpdated.gt.VoidC\nrepPlayerOffline%.gt.frnd.PlayerInfoOnlineStateUpdated.gt.VoidA\nrepPlayerInfoUpdated.gt.frnd.PlayerInfoUpdatedBasic.gt.Void5\nrepCallMethodFail.gt.frnd.RemoteMessage.gt.Void5\nrepOnCallMethod.gt.frnd.OnRemoteMessage.gt.Void<\nrepGetPlayersInfo.gt.frnd.BatchPlayerInfoReply.gt.Void3\nrepOnAddFriend.gt.frnd.AddFriendReply.gt.Void9\nrepOnRemoveFriend.gt.frnd.RemoveFriendReply.gt.Void;\nrepRemovePlayerInfo.gt.frnd.PlayerInfoRemoved.gt.VoidB��')
_GENDER = _descriptor.EnumDescriptor(name='Gender', full_name='gt.frnd.Gender', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='MALE', index=0, number=0, options=None, type=None), _descriptor.EnumValueDescriptor(name='FEMALE', index=1, number=1, options=None, type=None), _descriptor.EnumValueDescriptor(name='OTHER', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=1415, serialized_end=1456)
Gender = enum_type_wrapper.EnumTypeWrapper(_GENDER)
MALE = 0
FEMALE = 1
OTHER = 2
_PLAYERID = _descriptor.Descriptor(name='PlayerId', full_name='gt.frnd.PlayerId', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.PlayerId.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=39, serialized_end=63)
_PLAYERINFO = _descriptor.Descriptor(name='PlayerInfo', full_name='gt.frnd.PlayerInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.PlayerInfo.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='server', full_name='gt.frnd.PlayerInfo.server', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='roleName', full_name='gt.frnd.PlayerInfo.roleName', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='data', full_name='gt.frnd.PlayerInfo.data', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=65, serialized_end=139)
_PLAYERINFOLIST = _descriptor.Descriptor(name='PlayerInfoList', full_name='gt.frnd.PlayerInfoList', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='infos', full_name='gt.frnd.PlayerInfoList.infos', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=141, serialized_end=193)
_MOVELOCALFRIENDTOREMOTE = _descriptor.Descriptor(name='MoveLocalFriendToRemote', full_name='gt.frnd.MoveLocalFriendToRemote', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='srcPlayer', full_name='gt.frnd.MoveLocalFriendToRemote.srcPlayer', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='infos', full_name='gt.frnd.MoveLocalFriendToRemote.infos', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=195, serialized_end=296)
_PLAYERRELATION = _descriptor.Descriptor(name='PlayerRelation', full_name='gt.frnd.PlayerRelation', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='srcPlayer', full_name='gt.frnd.PlayerRelation.srcPlayer', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tgtPlayer', full_name='gt.frnd.PlayerRelation.tgtPlayer', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=298, serialized_end=390)
_UPDATEPLAYERRELATIONDETAIL = _descriptor.Descriptor(name='UpdatePlayerRelationDetail', full_name='gt.frnd.UpdatePlayerRelationDetail', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='srcPlayer', full_name='gt.frnd.UpdatePlayerRelationDetail.srcPlayer', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tgtPlayer', full_name='gt.frnd.UpdatePlayerRelationDetail.tgtPlayer', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='data', full_name='gt.frnd.UpdatePlayerRelationDetail.data', index=2, number=3, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=392, serialized_end=510)
_REGHOSTINFO = _descriptor.Descriptor(name='RegHostInfo', full_name='gt.frnd.RegHostInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.frnd.RegHostInfo.server', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=512, serialized_end=541)
_FRIENDINFO = _descriptor.Descriptor(name='FriendInfo', full_name='gt.frnd.FriendInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.FriendInfo.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='data', full_name='gt.frnd.FriendInfo.data', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='online', full_name='gt.frnd.FriendInfo.online', index=2, number=3, type=8, cpp_type=7, label=2, has_default_value=True, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=543, serialized_end=606)
_PLAYERRELATIONLIST = _descriptor.Descriptor(name='PlayerRelationList', full_name='gt.frnd.PlayerRelationList', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.PlayerRelationList.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='infos', full_name='gt.frnd.PlayerRelationList.infos', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=608, serialized_end=678)
_PLAYERINFOUPDATED = _descriptor.Descriptor(name='PlayerInfoUpdated', full_name='gt.frnd.PlayerInfoUpdated', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='who', full_name='gt.frnd.PlayerInfoUpdated.who', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='friends', full_name='gt.frnd.PlayerInfoUpdated.friends', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=680, serialized_end=767)
_PLAYERINFOONLINESTATEUPDATED = _descriptor.Descriptor(name='PlayerInfoOnlineStateUpdated', full_name='gt.frnd.PlayerInfoOnlineStateUpdated', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='relation', full_name='gt.frnd.PlayerInfoOnlineStateUpdated.relation', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=769, serialized_end=845)
_PLAYERINFOREMOVED = _descriptor.Descriptor(name='PlayerInfoRemoved', full_name='gt.frnd.PlayerInfoRemoved', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='relation', full_name='gt.frnd.PlayerInfoRemoved.relation', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=847, serialized_end=912)
_PLAYERINFOUPDATEDBASIC = _descriptor.Descriptor(name='PlayerInfoUpdatedBasic', full_name='gt.frnd.PlayerInfoUpdatedBasic', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='relation', full_name='gt.frnd.PlayerInfoUpdatedBasic.relation', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='info', full_name='gt.frnd.PlayerInfoUpdatedBasic.info', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=914, serialized_end=1019)
_REMOTEMESSAGE = _descriptor.Descriptor(name='RemoteMessage', full_name='gt.frnd.RemoteMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='server', full_name='gt.frnd.RemoteMessage.server', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='data', full_name='gt.frnd.RemoteMessage.data', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1021, serialized_end=1066)
_ONREMOTEMESSAGE = _descriptor.Descriptor(name='OnRemoteMessage', full_name='gt.frnd.OnRemoteMessage', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='host', full_name='gt.frnd.OnRemoteMessage.host', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='data', full_name='gt.frnd.OnRemoteMessage.data', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1068, serialized_end=1113)
_BATCHPLAYERINFOREQUEST = _descriptor.Descriptor(name='BatchPlayerInfoRequest', full_name='gt.frnd.BatchPlayerInfoRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='ids', full_name='gt.frnd.BatchPlayerInfoRequest.ids', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tag', full_name='gt.frnd.BatchPlayerInfoRequest.tag', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1115, serialized_end=1184)
_BATCHPLAYERINFOREPLY = _descriptor.Descriptor(name='BatchPlayerInfoReply', full_name='gt.frnd.BatchPlayerInfoReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='data', full_name='gt.frnd.BatchPlayerInfoReply.data', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='tag', full_name='gt.frnd.BatchPlayerInfoReply.tag', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1186, serialized_end=1260)
_ADDFRIENDREPLY = _descriptor.Descriptor(name='AddFriendReply', full_name='gt.frnd.AddFriendReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.AddFriendReply.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='info', full_name='gt.frnd.AddFriendReply.info', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='online', full_name='gt.frnd.AddFriendReply.online', index=2, number=3, type=8, cpp_type=7, label=2, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1262, serialized_end=1343)
_REMOVEFRIENDREPLY = _descriptor.Descriptor(name='RemoveFriendReply', full_name='gt.frnd.RemoveFriendReply', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='gbId', full_name='gt.frnd.RemoveFriendReply.gbId', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None), _descriptor.FieldDescriptor(name='info', full_name='gt.frnd.RemoveFriendReply.info', index=1, number=2, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=1345, serialized_end=1413)
_PLAYERINFOLIST.fields_by_name['infos'].message_type = _PLAYERINFO
_MOVELOCALFRIENDTOREMOTE.fields_by_name['srcPlayer'].message_type = _PLAYERINFO
_MOVELOCALFRIENDTOREMOTE.fields_by_name['infos'].message_type = _PLAYERINFO
_PLAYERRELATION.fields_by_name['srcPlayer'].message_type = _PLAYERID
_PLAYERRELATION.fields_by_name['tgtPlayer'].message_type = _PLAYERID
_UPDATEPLAYERRELATIONDETAIL.fields_by_name['srcPlayer'].message_type = _PLAYERID
_UPDATEPLAYERRELATIONDETAIL.fields_by_name['tgtPlayer'].message_type = _PLAYERID
_PLAYERRELATIONLIST.fields_by_name['infos'].message_type = _FRIENDINFO
_PLAYERINFOUPDATED.fields_by_name['who'].message_type = _PLAYERID
_PLAYERINFOUPDATED.fields_by_name['friends'].message_type = _PLAYERID
_PLAYERINFOONLINESTATEUPDATED.fields_by_name['relation'].message_type = _PLAYERINFOUPDATED
_PLAYERINFOREMOVED.fields_by_name['relation'].message_type = _PLAYERINFOUPDATED
_PLAYERINFOUPDATEDBASIC.fields_by_name['relation'].message_type = _PLAYERINFOUPDATED
_PLAYERINFOUPDATEDBASIC.fields_by_name['info'].message_type = _PLAYERINFO
_BATCHPLAYERINFOREQUEST.fields_by_name['ids'].message_type = _PLAYERID
_BATCHPLAYERINFOREPLY.fields_by_name['data'].message_type = _PLAYERINFOLIST
_ADDFRIENDREPLY.fields_by_name['info'].message_type = _PLAYERINFO
_REMOVEFRIENDREPLY.fields_by_name['info'].message_type = _PLAYERINFO
DESCRIPTOR.message_types_by_name['PlayerId'] = _PLAYERID
DESCRIPTOR.message_types_by_name['PlayerInfo'] = _PLAYERINFO
DESCRIPTOR.message_types_by_name['PlayerInfoList'] = _PLAYERINFOLIST
DESCRIPTOR.message_types_by_name['MoveLocalFriendToRemote'] = _MOVELOCALFRIENDTOREMOTE
DESCRIPTOR.message_types_by_name['PlayerRelation'] = _PLAYERRELATION
DESCRIPTOR.message_types_by_name['UpdatePlayerRelationDetail'] = _UPDATEPLAYERRELATIONDETAIL
DESCRIPTOR.message_types_by_name['RegHostInfo'] = _REGHOSTINFO
DESCRIPTOR.message_types_by_name['FriendInfo'] = _FRIENDINFO
DESCRIPTOR.message_types_by_name['PlayerRelationList'] = _PLAYERRELATIONLIST
DESCRIPTOR.message_types_by_name['PlayerInfoUpdated'] = _PLAYERINFOUPDATED
DESCRIPTOR.message_types_by_name['PlayerInfoOnlineStateUpdated'] = _PLAYERINFOONLINESTATEUPDATED
DESCRIPTOR.message_types_by_name['PlayerInfoRemoved'] = _PLAYERINFOREMOVED
DESCRIPTOR.message_types_by_name['PlayerInfoUpdatedBasic'] = _PLAYERINFOUPDATEDBASIC
DESCRIPTOR.message_types_by_name['RemoteMessage'] = _REMOTEMESSAGE
DESCRIPTOR.message_types_by_name['OnRemoteMessage'] = _ONREMOTEMESSAGE
DESCRIPTOR.message_types_by_name['BatchPlayerInfoRequest'] = _BATCHPLAYERINFOREQUEST
DESCRIPTOR.message_types_by_name['BatchPlayerInfoReply'] = _BATCHPLAYERINFOREPLY
DESCRIPTOR.message_types_by_name['AddFriendReply'] = _ADDFRIENDREPLY
DESCRIPTOR.message_types_by_name['RemoveFriendReply'] = _REMOVEFRIENDREPLY

class PlayerId(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERID


class PlayerInfo(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFO


class PlayerInfoList(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFOLIST


class MoveLocalFriendToRemote(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MOVELOCALFRIENDTOREMOTE


class PlayerRelation(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERRELATION


class UpdatePlayerRelationDetail(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _UPDATEPLAYERRELATIONDETAIL


class RegHostInfo(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REGHOSTINFO


class FriendInfo(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _FRIENDINFO


class PlayerRelationList(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERRELATIONLIST


class PlayerInfoUpdated(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFOUPDATED


class PlayerInfoOnlineStateUpdated(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFOONLINESTATEUPDATED


class PlayerInfoRemoved(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFOREMOVED


class PlayerInfoUpdatedBasic(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PLAYERINFOUPDATEDBASIC


class RemoteMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REMOTEMESSAGE


class OnRemoteMessage(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ONREMOTEMESSAGE


class BatchPlayerInfoRequest(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _BATCHPLAYERINFOREQUEST


class BatchPlayerInfoReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _BATCHPLAYERINFOREPLY


class AddFriendReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ADDFRIENDREPLY


class RemoveFriendReply(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _REMOVEFRIENDREPLY


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '��')
_SERVERSERVICE = _descriptor.ServiceDescriptor(name='ServerService', full_name='gt.frnd.ServerService', file=DESCRIPTOR, index=0, options=None, serialized_start=1459, serialized_end=2200, methods=[_descriptor.MethodDescriptor(name='regHost', full_name='gt.frnd.ServerService.regHost', index=0, containing_service=None, input_type=_REGHOSTINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqAddPlayerInfo', full_name='gt.frnd.ServerService.reqAddPlayerInfo', index=1, containing_service=None, input_type=_PLAYERINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqUpdatePlayerInfo', full_name='gt.frnd.ServerService.reqUpdatePlayerInfo', index=2, containing_service=None, input_type=_PLAYERINFO, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqRemovePlayerInfo', full_name='gt.frnd.ServerService.reqRemovePlayerInfo', index=3, containing_service=None, input_type=_PLAYERID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqAddPlayerFriend', full_name='gt.frnd.ServerService.reqAddPlayerFriend', index=4, containing_service=None, input_type=_PLAYERRELATION, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqRemovePlayerFriend', full_name='gt.frnd.ServerService.reqRemovePlayerFriend', index=5, containing_service=None, input_type=_PLAYERRELATION, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqUpdatePlayerFriend', full_name='gt.frnd.ServerService.reqUpdatePlayerFriend', index=6, containing_service=None, input_type=_UPDATEPLAYERRELATIONDETAIL, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqGetPlayerFriends', full_name='gt.frnd.ServerService.reqGetPlayerFriends', index=7, containing_service=None, input_type=_PLAYERID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqPlayerOnline', full_name='gt.frnd.ServerService.reqPlayerOnline', index=8, containing_service=None, input_type=_PLAYERID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqPlayerOffline', full_name='gt.frnd.ServerService.reqPlayerOffline', index=9, containing_service=None, input_type=_PLAYERID, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqCallMethod', full_name='gt.frnd.ServerService.reqCallMethod', index=10, containing_service=None, input_type=_REMOTEMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqGetPlayersInfo', full_name='gt.frnd.ServerService.reqGetPlayersInfo', index=11, containing_service=None, input_type=_BATCHPLAYERINFOREQUEST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='reqMoveLocalFriendToRmote', full_name='gt.frnd.ServerService.reqMoveLocalFriendToRmote', index=12, containing_service=None, input_type=_MOVELOCALFRIENDTOREMOTE, output_type=common_pb2._VOID, options=None)])

class ServerService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _SERVERSERVICE


class ServerService_Stub(ServerService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _SERVERSERVICE


_CLIENTSERVICE = _descriptor.ServiceDescriptor(name='ClientService', full_name='gt.frnd.ClientService', file=DESCRIPTOR, index=1, options=None, serialized_start=2203, serialized_end=2831, methods=[_descriptor.MethodDescriptor(name='repGetPlayerRelations', full_name='gt.frnd.ClientService.repGetPlayerRelations', index=0, containing_service=None, input_type=_PLAYERRELATIONLIST, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repPlayerOnline', full_name='gt.frnd.ClientService.repPlayerOnline', index=1, containing_service=None, input_type=_PLAYERINFOONLINESTATEUPDATED, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repPlayerOffline', full_name='gt.frnd.ClientService.repPlayerOffline', index=2, containing_service=None, input_type=_PLAYERINFOONLINESTATEUPDATED, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repPlayerInfoUpdated', full_name='gt.frnd.ClientService.repPlayerInfoUpdated', index=3, containing_service=None, input_type=_PLAYERINFOUPDATEDBASIC, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repCallMethodFail', full_name='gt.frnd.ClientService.repCallMethodFail', index=4, containing_service=None, input_type=_REMOTEMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repOnCallMethod', full_name='gt.frnd.ClientService.repOnCallMethod', index=5, containing_service=None, input_type=_ONREMOTEMESSAGE, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repGetPlayersInfo', full_name='gt.frnd.ClientService.repGetPlayersInfo', index=6, containing_service=None, input_type=_BATCHPLAYERINFOREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repOnAddFriend', full_name='gt.frnd.ClientService.repOnAddFriend', index=7, containing_service=None, input_type=_ADDFRIENDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repOnRemoveFriend', full_name='gt.frnd.ClientService.repOnRemoveFriend', index=8, containing_service=None, input_type=_REMOVEFRIENDREPLY, output_type=common_pb2._VOID, options=None),
 _descriptor.MethodDescriptor(name='repRemovePlayerInfo', full_name='gt.frnd.ClientService.repRemovePlayerInfo', index=9, containing_service=None, input_type=_PLAYERINFOREMOVED, output_type=common_pb2._VOID, options=None)])

class ClientService(_service.Service):
    __metaclass__ = service_reflection.GeneratedServiceType
    DESCRIPTOR = _CLIENTSERVICE


class ClientService_Stub(ClientService):
    __metaclass__ = service_reflection.GeneratedServiceStubType
    DESCRIPTOR = _CLIENTSERVICE
