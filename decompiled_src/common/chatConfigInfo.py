#Embedded file name: I:/bag/tmp/tw2/res/entities\common/chatConfigInfo.o
from userInfo import UserInfo
from chatConfig import ChatConfig

class chatConfigInfo(UserInfo):

    def createObjFromDict(self, dic):
        obj = ChatConfig()
        for group, channels in dic['channelConfig'].iteritems():
            tempDict = {}
            if isinstance(channels, dict):
                for ch in channels.keys():
                    if ch in ChatConfig.supportedChannels:
                        tempDict[ch] = channels[ch]

            else:
                for ch in channels:
                    if ch in ChatConfig.supportedChannels:
                        tempDict[ch] = True

            obj.channelConfig[group] = tempDict

        if dic['groupName']:
            obj.groupName.update(dic['groupName'])
        if dic['groupPos']:
            obj.groupPos.update(dic['groupPos'])
        return obj

    def getDictFromObj(self, obj):
        dict = {}
        channelConfig = {}
        for group, channels in obj.channelConfig.iteritems():
            channelConfig[group] = {}
            for ch in channels.keys():
                if ch in ChatConfig.supportedChannels:
                    channelConfig[group][ch] = channels[ch]

        dict['channelConfig'] = channelConfig
        dict['groupName'] = obj.groupName
        dict['groupPos'] = obj.groupPos
        return dict

    def isSameType(self, obj):
        return type(obj) is ChatConfig


instance = chatConfigInfo()
