#Embedded file name: I:/bag/tmp/tw2/res/entities\common/flowbackInfo.o
from userInfo import UserInfo
from flowback import Flowback

class FlowbackInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = Flowback()
        obj.yaoliBonus.fromDTO(dict['yaoliBonus'])
        obj.jiuliBonus.fromDTO(dict['jiuliBonus'])
        obj.vpBonus.fromDTO(dict['vpBonus'])
        obj.lostType = dict['lostType']
        obj.startTime = dict['startTime']
        obj.itemBonusRefType = dict['itemBonusRefType']
        obj.lastLostTime = dict['lastLostTime']
        obj.thisLostTime = dict['thisLostTime']
        obj.lastWorldChatTime = dict['lastWorldChatTime']
        obj.worldChatCount = dict['worldChatCount']
        obj.lastTeleportTime = dict['lastTeleportTime']
        obj.teleportCount = dict['teleportCount']
        obj.guildGiftCount = dict['guildGiftCount']
        obj.friendGiftCount = dict['friendGiftCount']
        obj.giftSentFriends = dict['giftSentFriends']
        return obj

    def getDictFromObj(self, obj):
        d = {}
        d['yaoliBonus'] = obj.yaoliBonus.getDTO()
        d['jiuliBonus'] = obj.jiuliBonus.getDTO()
        d['vpBonus'] = obj.vpBonus.getDTO()
        d['lostType'] = obj.lostType
        d['startTime'] = obj.startTime
        d['itemBonusRefType'] = obj.itemBonusRefType
        d['lastLostTime'] = obj.lastLostTime
        d['thisLostTime'] = obj.thisLostTime
        d['lastWorldChatTime'] = obj.lastWorldChatTime
        d['worldChatCount'] = obj.worldChatCount
        d['lastTeleportTime'] = obj.lastTeleportTime
        d['teleportCount'] = obj.teleportCount
        d['guildGiftCount'] = obj.guildGiftCount
        d['friendGiftCount'] = obj.friendGiftCount
        d['giftSentFriends'] = obj.giftSentFriends
        return d

    def isSameType(self, obj):
        return type(obj) is Flowback


instance = FlowbackInfo()
