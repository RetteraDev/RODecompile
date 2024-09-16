#Embedded file name: /WORKSPACE/data/entities/common/chatconfig.o
import const
import BigWorld
if BigWorld.component in ('base', 'cell'):
    import gameconfig
from userSoleType import UserSoleType
from data import chat_channel_data as CCD

class ChatConfig(UserSoleType):
    CHANNEL_GROUP_MULTIPLE = 1
    CHANNEL_GROUP_SINGLE = 2
    CHANNEL_GROUP_COMBAT = 3
    CHANNEL_GROUP_SYSTEM = 4
    CHANNEL_GROUP_CUSTOM1 = 5
    CHANNEL_GROUP_CUSTOM2 = 6
    CHANNEL_GROUP_JJC = 7
    CHANNEL_GROUP_GROUP = 8
    supportedChannels = (const.CHAT_CHANNEL_SYSTEM,
     const.CHAT_CHANNEL_ARENA,
     const.CHAT_CHANNEL_WORLD,
     const.CHAT_CHANNEL_WORLD_EX,
     const.CHAT_CHANNEL_VIEW,
     const.CHAT_CHANNEL_SINGLE,
     const.CHAT_CHANNEL_TEAM,
     const.CHAT_CHANNEL_GROUP,
     const.CHAT_CHANNEL_BATTLE_FIELD,
     const.CHAT_CHANNEL_SPACE,
     const.CHAT_CHANNEL_SCHOOL,
     const.CHAT_CHANNEL_COMBAT,
     const.CHAT_CHANNEL_NPC,
     const.CHAT_CHANNEL_SHOUT,
     const.CHAT_CHANNEL_DEBUG,
     const.CHAT_CHANNEL_NOTICE,
     const.CHAT_CHANNEL_GUILD,
     const.CHAT_CHANNEL_INFO,
     const.CHAT_CHANNEL_ACTIVITY,
     const.CHAT_CHANNEL_NEW_PLAYER,
     const.CHAT_CHANNEL_DIGONG_LINE,
     const.CHAT_CHANNEL_CLAN,
     const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
     const.CHAT_CHANNEL_WORLD_WAR,
     const.CHAT_CHANNEL_OB,
     const.CHAT_CHANNEL_GROUP_INFO,
     const.CHAT_CHANNEL_SECRET,
     const.CHAT_CHANNEL_PARTNER,
     const.CHAT_CHANNEL_MARRIAGE_HALL,
     const.CHAT_CHANNEL_WING_WORLD_WAR,
     const.CHAT_CHANNEL_CROSS_CLAN_WAR,
     const.CHAT_CHANNEL_WING_WORLD_CAMP,
     const.CHAT_CHANNEL_MAP_GAME,
     const.CHAT_CHANNEL_ANONYMITY)
    editableGroups = (CHANNEL_GROUP_CUSTOM1, CHANNEL_GROUP_CUSTOM2)

    def __init__(self):
        self.channelConfig = {ChatConfig.CHANNEL_GROUP_MULTIPLE: dict(),
         ChatConfig.CHANNEL_GROUP_SINGLE: dict(),
         ChatConfig.CHANNEL_GROUP_COMBAT: dict(),
         ChatConfig.CHANNEL_GROUP_SYSTEM: dict(),
         ChatConfig.CHANNEL_GROUP_GROUP: dict()}
        self.groupName = {}
        self.groupPos = {}
        for channel, channelInfo in CCD.data.iteritems():
            groups = channelInfo.get('groups', ())
            for gp in groups:
                self.channelConfig[gp][channel] = True

    def __checkConfig(self, channel, group, modify = False):
        if group not in self.channelConfig.keys():
            return False
        if channel not in ChatConfig.supportedChannels:
            return False
        return True

    def appendChannelToGroup(self, channel, group):
        if not self.__checkConfig(channel, group, True):
            return False
        self.channelConfig[group][channel] = True
        return True

    def removeChannelFromGroup(self, channel, group):
        if not self.__checkConfig(channel, group, True):
            return False
        if self.channelConfig[group].get(channel, False):
            self.channelConfig[group][channel] = False
            return True
        self.channelConfig[group][channel] = False
        return False

    def removeGroup(self, group):
        if group not in ChatConfig.editableGroups:
            return False
        self.channelConfig.has_key(group) and self.channelConfig.pop(group)
        self.groupName.has_key(group) and self.groupName.pop(group)
        self.groupPos.has_key(group) and self.groupPos.pop(group)
        return True

    def createGroup(self, group, name, pos):
        if group not in ChatConfig.editableGroups:
            return False
        self.channelConfig[group] = dict()
        self.groupName[group] = name
        self.groupPos[group] = pos
        return True

    def setGroupPos(self, group, pos):
        if group not in ChatConfig.editableGroups:
            return False
        self.groupPos[group] = pos
        return True

    def setGroupName(self, group, name):
        if group not in ChatConfig.editableGroups:
            return False
        self.groupName[group] = name
        return True

    def hasGroup(self, group):
        return self.channelConfig.has_key(group) or self.groupName.has_key(group)

    def displayedInGroup(self, channel, group):
        if not self.__checkConfig(channel, group):
            return False
        return self.channelConfig[group].get(channel, False)

    def getDisplayedGroup(self, channel):
        for group, channels in self.channelConfig.iteritems():
            if channels.get(channel, False):
                return group

    def transfer(self, owner):
        owner.client.resChatConfig(self)

    def initChannel(self, owner):
        if not owner.getCellPrivateMiscProperty('secretChannelClosed', False):
            channelData = CCD.data.get(const.CHAT_CHANNEL_SECRET, {})
            groups = channelData.get('groups', ())
            for gp in groups:
                if gp in self.channelConfig and const.CHAT_CHANNEL_SECRET not in self.channelConfig[gp]:
                    self.channelConfig[gp][const.CHAT_CHANNEL_SECRET] = True

        for channel in self.supportedChannels:
            channelData = CCD.data.get(channel, {})
            configurable = channelData.get('config', 0)
            displayedGroup = self.getDisplayedGroup(channel)
            if configurable and displayedGroup == None:
                owner.switchChannel(owner.id, channel, const.CHAT_SWITCH_CLOSE)
            else:
                owner.switchChannel(owner.id, channel, const.CHAT_SWITCH_OPEN)
            if not configurable and displayedGroup == None:
                groups = channelData.get('groups', ())
                for gp in groups:
                    self.channelConfig[gp][channel] = True
