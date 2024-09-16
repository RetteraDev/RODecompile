#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impChat.o
from gamestrings import gameStrings
import re
import types
import BigWorld
import const
import gameglobal
import gametypes
import gamemsg
import gamelog
import utils
import clientUtils
import formula
from guis import richTextUtils
from callbackHelper import Functor
from item import Item
from sfx import keyboardEffect
from guis import groupUtils
from guis import uiConst
from guis import uiUtils
from guis import menuManager
from data import game_msg_data as GMD
from data import chat_channel_data as CCD
from data import item_data as ID
from data import dialogs_data as DD
from data import sys_config_data as SCD
from data import game_server_msg_data as GSMD
from data import summon_sprite_personalized_chat_data as SSPCD
from cdata import game_msg_def_data as GMDD
from cdata import summon_sprite_talk_content_data as SSTCD
from cdata import summon_sprite_chat_reverse_data as SSCRD
from helpers import AnonymousNameManager

def ItemNameAdd(data):
    return data.group(2)


GROUP_MSG_MAP = {gametypes.GROUP_TYPE_TEAM_GROUP: {'<group1>': gameStrings.TEXT_GAMEGLOBAL_1371_3,
                                   '<group2>': gameStrings.TEXT_IMPCHAT_40},
 gametypes.GROUP_TYPE_RAID_GROUP: {'<group1>': gameStrings.TEXT_GAMEGLOBAL_1371,
                                   '<group2>': gameStrings.TEXT_IMPCHAT_41}}
CASH_STYLE_MSG = '<cash>'
LABOUR_STYLE_MSG = '<labour>'
LABOUR_DESC = gameStrings.TEXT_IMPCHAT_47
BRAIN_DESC = gameStrings.TEXT_IMPCHAT_48
DUPLICATED_SYS_MODES = (3, 8)
SHIELD_MSG_ID_IN_GM_MODE = frozenset([GMDD.data.GUILD_NOT_JOINED])

class ImpChat(object):

    def chatToSpace(self, srcRole, titleOption, msg, mingpaiId):
        channel = const.CHAT_CHANNEL_WING_WORLD_WAR if self.inWingWarCity() else const.CHAT_CHANNEL_SPACE
        gameglobal.rds.ui.chat.addMessage(channel, msg, srcRole, mingpaiId=mingpaiId)
        if BigWorld.player().roleName == srcRole:
            gameglobal.rds.ui.help.canAutoPush(msg)

    def chatToNovice(self, srcRole, msg, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_NEW_PLAYER, msg, srcRole, mingpaiId=mingpaiId)
        if BigWorld.player().roleName == srcRole:
            gameglobal.rds.ui.help.canAutoPush(msg)

    def chatToClan(self, srcRole, msg, srcgbId, fromGuildName, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_CLAN, msg, srcRole, fromGuild=fromGuildName, mingpaiId=mingpaiId)

    def chatToDiGongLine(self, srcRole, msg, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_DIGONG_LINE, msg, srcRole, mingpaiId=mingpaiId)

    def chatInScreen(self, msg, color):
        gameglobal.rds.ui.notify.showSysNotifyDirect(msg, color)

    def chatInScreenById(self, msgId, color):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        gameglobal.rds.ui.notify.showSysNotifyDirect(msg, color)

    def chatInSysBoard(self, msgId, duration):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        gameglobal.rds.ui.playTips.show(msg, duration)

    def chatToEvent(self, msgNo, color):
        msg = gamemsg.message[msgNo]
        self.chatToEventEx(msg, color)
        if msgNo == gamemsg.ITEM_MSG_OBSOLETE:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SYSTEM_MESSAGE_ITEM_OBSOLETE, ())

    def chatToEventEx(self, msg, color = None):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, msg, '')

    def chatToBoard(self, msg):
        pass

    def chatToSingle(self, srcRole, msg, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, msg, srcRole, mingpaiId=mingpaiId)

    def chatTextFromSprite(self, rangeID, spriteRole, spriteId, masterRole, masterGBID, contentID, personalizedText):
        contentDict = SSTCD.data.get(contentID, {})
        text = contentDict.get('text', '')
        textRange = contentDict.get('text_range', const.SSPRITE_TALK_RANGE_MASTER)
        needBubble = contentDict.get('text_bubble', False)
        soundId = contentDict.get('soundId', False)
        if personalizedText is not None:
            text = personalizedText
            needBubble = True
        if rangeID == const.SSPRITE_TALK_RANGE_MASTER:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, text, spriteRole, mingpaiId=0, msgProperties={'spriteId': spriteId})
        elif rangeID == const.SSPRITE_TALK_RANGE_MYTEAM:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GROUP, text, spriteRole, mingpaiId=0, msgProperties={'spriteId': spriteId})
        elif rangeID == const.SSPRITE_TALK_RANGE_NEARBY:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_VIEW, text, spriteRole, mingpaiId=0, msgProperties={'spriteId': spriteId})
        srcEntity = BigWorld.entities.get(spriteId)
        if srcEntity and needBubble:
            srcEntity.topLogo.setChatMsg(uiUtils.toHtml(text, '#FFFFE6'), 3, isFromSprite=True)
        if soundId and BigWorld.player().checkSpriteCanPlaySound(spriteId):
            gameglobal.rds.sound.playSound(soundId)

    def chatToWorld(self, srcRole, msg, useType = 0, gbId = 0, mingpaiId = 0):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WORLD, msg, srcRole, useType=useType, gbId=gbId, mingpaiId=mingpaiId)
        if BigWorld.player().roleName == srcRole:
            gameglobal.rds.ui.help.canAutoPush(msg)

    def chatToWorldForCompanion(self, srcRole, msgId, params, gbId, msg):
        if not msg:
            if params:
                msg = uiUtils.getTextFromGMD(msgId) % params + ':role'
            else:
                msg = uiUtils.getTextFromGMD(msgId) + ':role'
        else:
            msg = msg + ':role'
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WORLD, msg, srcRole, useType=0, gbId=gbId, icon=uiConst.NEWBIE_WORLD_CHAT_MSG_ICON)

    def chatToWorldEx(self, srcRole, msg, labaId, useType, gbId, mingpaiId):
        if useType in (const.CROSS_SERVER_NORMAL_CHAT_MSG, const.CROSS_SERVER_ANONYMOUS_CHAT_MSG):
            if gameglobal.rds.configData.get('enableCrossServerLaba', False) == False:
                return
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX, msg, srcRole, labaId=labaId, useType=useType, gbId=gbId, mingpaiId=mingpaiId)
        elif useType in (const.WORLD_WAR_NORMAL_CHAT_MSG, const.WORLD_WAR_ANONYMOUS_CHAT_MSG):
            if gameglobal.rds.configData.get('enableWorldWarLaba', False) == False:
                return
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WORLD_WAR, msg, srcRole, labaId=labaId, useType=useType, gbId=gbId, mingpaiId=mingpaiId)
        elif useType in (const.CROSS_CLAN_WAR_NORMAL_CHAT_MSG, const.CROSS_CLAN_WAR_ANONYMOUS_CHAT_MSG):
            labaId = uiConst.CROSS_CLAN_WAR_LABA_ID
            self.chatConfig.channelConfig[const.CHANNEL_TAB_MULTIPLE][const.CHAT_CHANNEL_CROSS_CLAN_WAR] = True
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_CROSS_CLAN_WAR, msg, srcRole, labaId=labaId, useType=useType, gbId=gbId, mingpaiId=mingpaiId)
        elif useType in (const.WING_WORLD_CAMP_NORMAL_CHAT_MSG, const.WING_WORLD_CAMP_ANONYMOUS_CHAT_MSG):
            self.chatConfig.channelConfig[const.CHANNEL_TAB_MULTIPLE][const.CHAT_CHANNEL_WING_WORLD_CAMP] = True
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WING_WORLD_CAMP, msg, srcRole, labaId=labaId, useType=useType, gbId=gbId, mingpaiId=mingpaiId)
        else:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WORLD_EX, msg, srcRole, labaId=labaId, useType=useType, gbId=gbId, mingpaiId=mingpaiId)

    def chatToSystem(self, msg):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, msg, '')

    def chatToSchool(self, srcRole, msg, mingpaiId, extra):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SCHOOL, msg, srcRole, mingpaiId=mingpaiId, extra=extra)
        if BigWorld.player().roleName == srcRole:
            gameglobal.rds.ui.help.canAutoPush(msg)

    def broadcastChatToSchool(self, srcRole, msgId, mingpaiId):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        self.chatToSchool(srcRole, msg, mingpaiId, {})

    def chatToSelectedSchool(self, srcRole, msgId, school):
        if self.school != school:
            return
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        self.chatToSchool(srcRole, msg, 0, {})

    def chatToNPC(self, srcRole, msg, srcID, duration):
        self.popupMsg(srcID, msg, duration)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_NPC, msg, srcRole)

    def chatToView(self, srcRole, msg, srcID, duration, isGm, mingpaiId):
        if gameglobal.rds.ui.chat.isBlock(srcRole):
            return
        else:
            srcEnt = BigWorld.entities.get(srcID, None)
            msgProperties, msg = utils.decodeMsgHeader(msg)
            if srcEnt:
                if getattr(srcEnt, 'jctSeq', 0) and BigWorld.player().inClanCourier():
                    srcRole = srcEnt.getJCTRoleName()
                if self.chatConfig.getDisplayedGroup(const.CHAT_CHANNEL_VIEW) or srcEnt == self:
                    if not isGm:
                        if BigWorld.player().roleName == srcRole:
                            duration = SCD.data.get('bubbleDurationSelf', 3)
                        else:
                            duration = SCD.data.get('bubbleDurationOther', 3)
                        self.popupMsg(srcID, msg, duration)
                    gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_VIEW, msg, srcRole, mingpaiId=mingpaiId, msgProperties=msgProperties)
                    if BigWorld.player().roleName == srcRole:
                        gameglobal.rds.ui.help.canAutoPush(msg)
            if self.checkNeedMsgFeedBack():
                ens = BigWorld.entities.values()
                for entity in ens:
                    if hasattr(entity, 'msgFeedBack'):
                        hasFeedBack = entity.msgFeedBack(msg)
                        if hasFeedBack:
                            break

            return

    def checkNeedMsgFeedBack(self):
        if not gameglobal.rds.configData.get('enableInteractiveHomeChat', False):
            return False
        if self.spaceInHomeOrLargeRoom():
            return True
        return False

    def beChatToPartner(self, srcRole, msg, srcgbId, mingpaiId):
        gamelog.debug('@hjx partner#beChatToPartner:', srcRole, msg, srcgbId, mingpaiId)

    def chatToTeamGroup(self, srcRole, msg, srcgbId, mingpaiId, isNeedBubble):
        if gameglobal.rds.ui.chat.isBlock(srcRole):
            return
        if self.groupNUID == 0:
            return
        msgProperties, msg = utils.decodeMsgHeader(msg)
        if self.groupType in [gametypes.GROUP_TYPE_TEAM_GROUP, gametypes.GROUP_TYPE_RAID_GROUP]:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_TEAM, msg, srcRole, mingpaiId=mingpaiId, msgProperties=msgProperties)
            if richTextUtils.isRedPacket(msg) or richTextUtils.isSoundRecord(msg):
                return
            if self.gbId != srcgbId and groupUtils.isInSameTeam(self.gbId, srcgbId) or self.gbId == srcgbId:
                srcEntity = BigWorld.entities.get(self.members.get(srcgbId, {}).get('id', 0))
                if srcEntity:
                    if BigWorld.player().roleName == srcRole:
                        duration = SCD.data.get('bubbleDurationSelf', 3)
                    else:
                        duration = SCD.data.get('bubbleDurationOther', 3)
                    if isNeedBubble:
                        srcEntity.topLogo.setChatMsg(uiUtils.toHtml(msg[:-5], '#8cc6ff'), duration)
        if self.isInTeam() or self.isInGroup() and self.gbId != srcgbId and groupUtils.isInSameTeam(self.gbId, srcgbId):
            if isNeedBubble:
                gameglobal.rds.ui.teamComm.setChatBubble(srcRole, msg[:-5])

    def chatToGroup(self, srcRole, msg, srcgbId, mingpaiId):
        if gameglobal.rds.ui.chat.isBlock(srcRole):
            return
        if self.groupNUID == 0:
            return
        if self.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            msgProperties, msg = utils.decodeMsgHeader(msg)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GROUP, msg, srcRole, mingpaiId=mingpaiId)
            if richTextUtils.isRedPacket(msg) or richTextUtils.isSoundRecord(msg):
                return
            if self.gbId != srcgbId and self.members and self.members.has_key(srcgbId) or self.gbId == srcgbId:
                srcEntity = BigWorld.entities.get(self.members.get(srcgbId, {}).get('id', 0))
                if srcEntity:
                    if BigWorld.player().roleName == srcRole:
                        duration = SCD.data.get('bubbleDurationSelf', 3)
                    else:
                        duration = SCD.data.get('bubbleDurationOther', 3)
                    srcEntity.topLogo.setChatMsg(uiUtils.toHtml(msg[:-5], '#8cc6ff'), duration)
            if self.gbId != srcgbId and groupUtils.isInSameTeam(self.gbId, srcgbId):
                gameglobal.rds.ui.teamComm.setChatBubble(srcRole, msg[:-5])

    def chatToArena(self, srcRole, msg, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_ARENA, msg, srcRole, mingpaiId=mingpaiId)

    def chatToBattleField(self, srcRole, msg, mingpaiId, chatToAll):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_BATTLE_FIELD, msg, srcRole, mingpaiId=mingpaiId, chatToAll=chatToAll)

    def chatToMarriageHall(self, srcRole, msg, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_MARRIAGE_HALL, msg, srcRole, mingpaiId=mingpaiId)

    def chatToAnonymity(self, srcRole, msg):
        if AnonymousNameManager.getInstance().checkCanRecvAnonyChanel():
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_ANONYMITY, msg, srcRole)

    def chatToTeam(self, srcRole, msg):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_TEAM, msg, srcRole)

    def chatToNotice(self, srcRole, msg):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_NOTICE, msg, srcRole)

    def chatToShout(self, srcRole, msg, srcID, duration, mingpaiId):
        srcEnt = BigWorld.entities.get(srcID, None)
        config = CCD.data.get(const.CHAT_CHANNEL_SHOUT, {}).get('config', 0)
        if srcEnt and (self.chatConfig.getDisplayedGroup(const.CHAT_CHANNEL_SHOUT) or config == 0):
            self.popupMsg(srcID, msg, duration)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SHOUT, msg, srcRole, mingpaiId=mingpaiId)

    def chatToItem(self, stamp, it, fid):
        gfxTipData = gameglobal.rds.ui.inventory.GfxToolTip(it)
        if fid == 'chatRoom':
            gameglobal.rds.ui.chatRoomWindow.showTooltip(const.CHAT_TIPS_ITEM, gfxTipData)
        elif fid == 'chat':
            gameglobal.rds.ui.chat.showTooltip(const.CHAT_TIPS_ITEM, gfxTipData)
        elif fid == 'booth':
            gameglobal.rds.ui.booth.showTooltip(const.CHAT_TIPS_ITEM, gfxTipData)
        elif fid == 'fitting':
            gameglobal.rds.ui.fittingRoom.addItem(it)
        elif fid == 'systemPush':
            gameglobal.rds.ui.systemPush.additem(it, 1)
        else:
            gameglobal.rds.ui.chatToFriend.showTooltip(const.CHAT_TIPS_ITEM, fid, gfxTipData)

    def chatToSprite(self, stamp, spriteInfoDict, fid):
        gameglobal.rds.ui.summonedWarSprite.showSpriteDetailTip(spriteInfoDict, fid)

    def chatToGM(self, msg):
        gameglobal.rds.ui.gmChat.sendMsgToGM(msg)

    def chatToGuild(self, srcRole, msg, srcgbId, mingpaiId):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GUILD, msg, srcRole, mingpaiId=mingpaiId)
        if BigWorld.player().roleName == srcRole:
            gameglobal.rds.ui.help.canAutoPush(msg)

    def popupMsg(self, entId, msg, duration = const.POPUP_MSG_SHOW_DURATION):
        en = BigWorld.entities.get(entId)
        if not en or not en.topLogo:
            return
        if msg.startswith('#BE:'):
            emotionId = int(msg.split(':')[1])
            if emotionId < len(uiConst.emoteMap):
                en.topLogo.showBigEmote(emotionId)
        else:
            en.topLogo.setChatMsg(msg, duration)

    def _processHelpCmd(self, msg):
        gamelog.debug('_processHelpCmd', msg)
        gameglobal.rds.gmMsg = msg
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GMWIDGET)

    def _processKindHelpCmd(self, msg):
        gamelog.debug('_processKindHelpCmd', msg)
        gameglobal.rds.gmGroupMsg = msg
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GMGROUPWIDGET)

    def _processCmd(self, msg):
        gamelog.debug('_processCmd', msg[0])
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GMPARAMETERWIDGET)
        gameglobal.rds.gmParameterMsg = msg
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GMPARAMETERWIDGET)

    def sendGmMsg(self, msg, methodName):
        if BigWorld.isPublishedVersion():
            return
        gamelog.debug('methodName', methodName)
        serverId = int(gameglobal.rds.g_serverid)
        if serverId < const.PUBLISH_SERVER_ID_BEGIN or serverId > const.PUBLISH_SERVER_ID_END:
            if methodName == 'help':
                msg.sort()
                self._processKindHelpCmd(msg)
            elif methodName == 'gmmatch':
                self._processCmd(msg)
            else:
                gamelog.error('the methodName is not correct:', methodName)

    def chatToGm(self, msg):
        msgs = msg.split('\n')
        for m in msgs:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, m, '')

    def showDebugMessge(self, msg):
        if not msg:
            return
        gameglobal.rds.ui.topMessage.showTopMsg(msg)

    def showBattlePromptMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        data = self.extractItemName(data, text)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.topMessage.showTopMsg(msg)

    def showSysBoardMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        color = msgData.get('color', 'white')
        time = msgData.get('time', 2)
        if not text or not color:
            return
        data = self.extractItemName(data, text)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.playTips.show(msg, time)

    def showSystemMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, msg, '')

    def showCombatMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        msg = '[%s] %s' % (utils.formatTimeEx(utils.getNow()), msg)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_COMBAT, msg, '')

    def showArenaMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_ARENA, msg, '')

    def showGangMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_BATTLE_FIELD, msg, '')

    def showGuildMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GUILD, msg, '')

    def showClanMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_CLAN, msg, '')

    def showTopRedMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.topMessage.showTopRedMsg(msg)

    def showTopBlueMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.topMessage.showTopBlueMsg(msg)

    def showSpriteMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        showTime = msgData.get('time', 3)
        msg = self.formatMsg(text, data)
        if msg:
            gameglobal.rds.ui.spriteAni.setPopMsg(msg, const.SPRITE_POPO_MSG_FANKUI, showTime)

    def showSystemNotify(self, msgId, data, msgData):
        if gameglobal.rds.configData.get('enableSystemMessage', False):
            p = BigWorld.player()
            p.chatFromSystemNotify(p.gbId, msgId, utils.getNow(), data)

    def showSystemSingleTip(self, msgId, data, msgData):
        gameglobal.rds.ui.systemSingleTip.showSysSingleMsg(msgId, data, msgData)

    def showActivityMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_ACTIVITY, msg, '')

    def showInfoMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_INFO, msg, '')

    def showSystemPush(self, msgId, data, msgData):
        p = BigWorld.player()
        if msgId == GMDD.data.QUEST_ACCEPTED:
            iconPath = SCD.data.get('systemPushQuestAccept', '')
            text = data[0]
            if data[1]:
                gameglobal.rds.ui.systemPush.setSystemInfo(iconPath, text)
        elif msgId == GMDD.data.QUEST_COMPLETED:
            iconPath = SCD.data.get('systemPushQuestCompleted', '')
            text = data[0]
            if data[1]:
                gameglobal.rds.ui.systemPush.setSystemInfo(iconPath, text)
        elif msgId in (GMDD.data.ITEM_GET_COMPLETE, GMDD.data.ITEM_GET_COMPLETE_ONE):
            if data[0].find('ret') != -1:
                itemId = data[2] if len(data) > 2 else -1
                if itemId != -1:
                    if ID.data.get(itemId, {}).get('mwrap', 0) > 1:
                        gameglobal.rds.ui.systemPush.additem(Item(itemId, 1, False), data[1])
                    else:
                        itemId = clientUtils.itemMsgParse(data[0])
                        p.base.chatToItem(itemId, 'systemPush')
            elif data[0].find('item') != -1:
                itemId = clientUtils.itemMsgParse(data[0])
                if itemId != -1:
                    gameglobal.rds.ui.systemPush.additem(Item(itemId, 1, False), data[1])
        elif msgId in (GMDD.data.QUEST_MONEY_GET, GMDD.data.ITEM_PICK_BIND_MONEY_COMPLETE):
            iconPath = SCD.data.get('systemPushBindMoney', '')
            if int(data[0]) == 0:
                return
            gameglobal.rds.ui.systemPush.setSystemInfo(iconPath, gameStrings.TEXT_INVENTORYPROXY_3297, True, -1, int(data[0]))
        elif msgId == GMDD.data.ITEM_PICK_MONEY_COMPLETE:
            iconPath = SCD.data.get('systemPushMoney', '')
            if int(data[0]) == 0:
                return
            gameglobal.rds.ui.systemPush.setSystemInfo(iconPath, gameStrings.TEXT_INVENTORYPROXY_3296, True, -2, int(data[0]))

    def showMsgBox(self, msgId, data, msgData):
        text = msgData.get('text', '')
        data = self.extractItemName(data, text)
        if text and data:
            text = self.formatMsg(text, data)
        gameglobal.rds.ui.showTips(text)

    def showSysMsgCurrentTab(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        color = msgData.get('color', None)
        if text and data:
            text = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addSystemMessage(text, color)

    def showPlayMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        time = msgData.get('time', 1)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.playTips.show(msg, time)

    def showSysPromptMsg(self, msgId, data, msgData):
        text = msgData.get('text', '')
        forceShow = msgData.get('forceShow', False)
        data = self.extractItemName(data, text)
        msg = self.formatMsg(text, data)
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA and not msgData.get('inScenario', 0):
            if msg not in self.msgCache:
                self.msgCache.append(msg)
            return
        gameglobal.rds.ui.systemTips.show(msg, forceShow)

    def showSysCacheMsg(self):
        if self.msgCache:
            for i, msg in enumerate(self.msgCache):
                BigWorld.callback(i * 0.2, Functor(gameglobal.rds.ui.systemTips.show, msg))

        self.msgCache = []

    def playUISound(self, msgId, data, msgData):
        if len(data) and type(data[-1]) == types.IntType:
            gameglobal.rds.sound.playSound(data[-1])

    def showNoticeMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_NOTICE, msg, '')

    def showTopMsg(self, msg):
        gameglobal.rds.ui.systemTips.show(msg)

    def showGameMsg(self, msgId, data = ()):
        if getattr(self, 'gmMode', False) and msgId in SHIELD_MSG_ID_IN_GM_MODE:
            return
        if gameglobal.rds.ui.activitySaleLottery.isLotterying == True:
            if msgId == GMDD.data.RANDOM_LOTTERY_DRAW_SUCCESS or msgId == GMDD.data.TEMP_BAG_GET_ONE_ITEM or msgId == GMDD.data.TEMP_BAG_GET_ITEM:
                gameglobal.rds.ui.activitySaleLottery.setLotteryMsg(msgId, data)
                return
        if gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult == True:
            if msgId == GMDD.data.RANDOM_CARD_DRAW_SUCCESS or msgId == GMDD.data.TEMP_BAG_GET_ONE_ITEM or msgId == GMDD.data.TEMP_BAG_GET_ITEM:
                gameglobal.rds.ui.activitySaleRandomCardDraw.setCardDrawMsg(msgId, data)
                return
        if gameglobal.rds.ui.randomTreasureBagMain.drawing:
            if msgId == GMDD.data.ITEM_GET_COMPLETE or msgId == GMDD.data.ITEM_GET_COMPLETE_ONE:
                gameglobal.rds.ui.randomTreasureBagMain.enQueueLotteryMsg(msgId, data)
                return
        if gameglobal.rds.ui.activitySaleLuckyLottery.drawing:
            if msgId == GMDD.data.TEMP_BAG_GET_ONE_ITEM or msgId == GMDD.data.TEMP_BAG_GET_ITEM:
                gameglobal.rds.ui.activitySaleLuckyLottery.enQueueLotteryMsg(msgId, data)
                return
        self.showGameMsgEx(msgId, data)

    def showMsgPicTip(self, data = ()):
        gameglobal.rds.ui.showPicTip(data)

    def showServerGameMsg(self, msgId, data):
        if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
            return
        else:
            msgData = GSMD.data.get(msgId, None)
            self._showGameMsgEx(msgId, msgData, data)
            return

    def showGMNotifyMsg(self, msgData):
        self._showGameMsgEx(0, msgData, {})

    def showOperatorPushMsg(self, data):
        icon, tip, sound, data = data
        gameglobal.rds.ui.help.addPushData(icon, data, tip, sound)

    def showDisposableNotifiyMsgs(self, data):
        gamelog.debug('@zqc [impChat.py:425]ImpChat.showDisposableNotifiyMsgs', data)
        for info in data:
            startTime, _, tips, title, msg, who, icon = info
            gameglobal.rds.ui.pushNotice.addPushNotice(icon, tips, title, msg, who, startTime)

    def showMapGameMsg(self, msgId, data, msgData):
        text = self.getLinkText(data, msgData)
        msg = self.formatMsg(text, data)
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_MAP_GAME, msg, '')

    def showGameMsgEx(self, msgId, data, needSound = True):
        if not msgId:
            return
        else:
            msgData = GMD.data.get(msgId, None)
            self._showGameMsgEx(msgId, msgData, data, needSound)
            if msgId == GMDD.data.GROUP_ALL_PREPARE_DONE:
                gameglobal.rds.ui.group.clearPrepareInfo()
            elif msgId == GMDD.data.FASHION_PROP_TRANS_SUCC:
                gameglobal.rds.ui.fashionPropTransfer.onTransSuccess()
            elif msgId == GMDD.data.LOTTERY_EXCHANGE_SUCC:
                gameglobal.rds.ui.freeLottery.openUrl()
            return

    def _showGameMsgEx(self, msgId, msgData, data, needSound = True):
        try:
            if msgData == None:
                if len(data):
                    msgData = {'text': data[0]}
                else:
                    return
            if msgData.has_key('minLv') and msgData.get('minLv', 0) > BigWorld.player().lv or msgData.has_key('maxLv') and msgData.get('maxLv', 0) < BigWorld.player().lv:
                return
            timeLimit = msgData.get('timeLimit', 0)
            if timeLimit and self.gameMsgCDDict.get(msgId, 0) >= timeLimit:
                return
            self.gameMsgCDDict[msgId] = self.gameMsgCDDict.get(msgId, 0) + 1
            displayModes = msgData.get('displayMode', (1,))
            showMsgFuncs = {1: 'showSysBoardMsg',
             2: 'showBattlePromptMsg',
             3: 'showSystemMsg',
             4: 'showMsgBox',
             5: 'showCombatMsg',
             6: 'showArenaMsg',
             7: 'showGangMsg',
             8: 'showSysMsgCurrentTab',
             9: 'showSysPromptMsg',
             10: 'playUISound',
             11: 'showNoticeMsg',
             12: 'showGuildMsg',
             13: 'showInfoMsg',
             14: 'showActivityMsg',
             15: 'showSystemPush',
             16: 'showClanMsg',
             17: 'showTopRedMsg',
             18: 'showTopBlueMsg',
             23: 'showSpriteMsg',
             25: 'showSystemNotify',
             26: 'showSystemSingleTip',
             55: 'showMapGameMsg'}
            if displayModes == DUPLICATED_SYS_MODES and gameglobal.rds.ui.chat.currentTab == const.CHANNEL_TAB_SYSTEM:
                displayModes = (DUPLICATED_SYS_MODES[0],)
            for mode in displayModes:
                modeFuncName = showMsgFuncs.get(mode, '')
                if modeFuncName:
                    func = getattr(self, modeFuncName, None)
                    func and func(msgId, data, msgData)
                else:
                    schoolChannelMap = {const.SCHOOL_SHENTANG: 17,
                     const.SCHOOL_YUXU: 18,
                     const.SCHOOL_GUANGREN: 19,
                     const.SCHOOL_YANTIAN: 20,
                     const.SCHOOL_LINGLONG: 21,
                     const.SCHOOL_LIUGUANG: 22}
                    schoolChannel = schoolChannelMap.get(BigWorld.player().school)
                    if mode == schoolChannel:
                        text = msgData.get('text', '')
                        msg = self.formatMsg(text, data)
                        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SCHOOL, msg, '')
                    else:
                        return

            if BigWorld.player().school == const.SCHOOL_YECHA and msgId == GMDD.data.SKILL_FORBIDDEN_NO_YUAN_LING:
                modelSound = {}
            else:
                modelSound = msgData.get('modelSound', {})
            if self.fashion.modelID in modelSound:
                soundId = modelSound[self.fashion.modelID]
            else:
                soundId = msgData.get('defaultSound', 0)
            if needSound:
                if soundId and gameglobal.ENABLE_ERROR_SOUND and not gameglobal.IN_ERROR_SOUND_CD:
                    gameglobal.IN_ERROR_SOUND_CD = True
                    gameglobal.rds.sound.playSound(soundId)
                    BigWorld.callback(SCD.data.get('soundPlayCD', 5), self.playSoundCooldown)
        except Exception as e:
            gamelog.debug('zt: showGameMsgError', msgId, data, e.message)

    def getLinkText(self, data, msgData):
        text = msgData.get('text', '')
        if not gameglobal.rds.configData.get('enableChatLink', False):
            return text
        p = BigWorld.player()
        type, linkText, nameIndex = msgData.get('linkText', (0, '', 0))
        if linkText and type:
            menuTarget = menuManager.getInstance().funcMenuTarget
            if type == uiConst.CHAT_LINK_FUNC_TYPE_ADDFRIEND:
                if isinstance(data, tuple):
                    data = data[nameIndex]
                menuTarget.apply(roleName=data)
                if menuTarget.canAddFriend(p):
                    linkText = linkText % data
                    text += linkText
            elif type == uiConst.CHAT_LINK_FUNC_TYPE_ENTERARENALIVE:
                linkText = linkText % data[nameIndex]
                text += linkText
        return text

    def playSoundCooldown(self):
        gameglobal.IN_ERROR_SOUND_CD = False

    def resConfigChannel(self, channel, group, displayed):
        gamelog.debug('zt: resConfigChannel', channel, group, displayed)
        if displayed:
            self.chatConfig.appendChannelToGroup(channel, group)
        else:
            self.chatConfig.removeChannelFromGroup(channel, group)

    def resChatConfig(self, config):
        gamelog.debug('yedawang###: resChatConfig channel', config.channelConfig)
        self.chatConfig = config
        if gameglobal.rds.configData.get('enableMapGame', False):
            channelConfig = self.chatConfig.channelConfig[const.CHANNEL_TAB_MULTIPLE]
            if not channelConfig.has_key(const.CHAT_CHANNEL_MAP_GAME):
                self.cell.configChannel(const.CHAT_CHANNEL_MAP_GAME, const.CHANNEL_TAB_MULTIPLE, True)
        gameglobal.rds.ui.chat.updateChannelTab()

    def resConfigGroup(self, group, name, pos):
        if not self.chatConfig.hasGroup(group):
            self.chatConfig.createGroup(group, name, pos)
        self.chatConfig.setGroupName(group, name)
        self.chatConfig.setGroupPos(group, pos)
        gameglobal.rds.ui.chat.updateChannelTab(False, True)
        gamelog.debug('zt: resConfigGroup', self.chatConfig.groupName, self.chatConfig.groupPos)

    def resRemoveGroup(self, group):
        self.chatConfig.removeGroup(group)
        gameglobal.rds.ui.chat.updateChannelTab(True, False)
        gamelog.debug('zt: resRemoveGroup', self.chatConfig.groupName, self.chatConfig.groupPos)

    def showApplyArenaChallenge(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast):
        gamelog.debug('@hjx arenachallenge#showApplyArenaChallenge:', srcHostId, srcRoleName, tgtHostId, challengeMode, tgtRoleName, msg)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_SHOW, declartionDict)
        if BigWorld.player().roleName == tgtRoleName and utils.getHostId() == tgtHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_APPLY, declartionDict)

    def showApplyByArenaChallenge(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast):
        gamelog.debug('@hjx arenachallenge#showApplyByArenaChallenge:', srcHostId, srcRoleName, tgtHostId, challengeMode, tgtRoleName, msg, needBroadcast)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_SHOW, declartionDict)
        if BigWorld.player().roleName == tgtRoleName and utils.getHostId() == tgtHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_APPLY, declartionDict)

    def rejectArenaChallengeApply(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast):
        gamelog.debug('@hjx arenachallenge#rejectArenaChallengeApply:', srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_REFUSE, declartionDict)
        if BigWorld.player().roleName == srcRoleName and utils.getHostId() == srcHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_REFUSE, declartionDict)

    def rejectByArenaChallengeApply(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast):
        gamelog.debug('@hjx arenachallenge#rejectByArenaChallengeApply:', srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_REFUSE, declartionDict)
        if BigWorld.player().roleName == srcRoleName and utils.getHostId() == srcHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_REFUSE, declartionDict)

    def acceptArenaChallengeApply(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast, extra):
        gamelog.debug('@hjx arenachallenge#acceptArenaChallengeApply:', srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast, extra)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_ACCEPT, declartionDict)
        gameglobal.rds.ui.arenaChallengeDeclartion.showMsgInChat(declartionDict, extra)
        if BigWorld.player().roleName == srcRoleName and utils.getHostId() == srcHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ACCEPT, declartionDict)

    def acceptByArenaChallengeApply(self, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast, extra):
        gamelog.debug('@hjx arenachallenge#acceptByArenaChallengeApply:', srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg, needBroadcast, extra)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if needBroadcast:
            gameglobal.rds.ui.arenaChallengeDeclartion.show(uiConst.ARENA_CHALLENGE_DECLARTION_ACCEPT, declartionDict)
        gameglobal.rds.ui.arenaChallengeDeclartion.showMsgInChat(declartionDict, extra)
        if BigWorld.player().roleName == srcRoleName and utils.getHostId() == srcHostId:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ACCEPT, declartionDict)

    def showSysNotification(self, notificationId, msgArgs, repeatCnt, interval, finishCallback = None):
        self.showGameMsg(notificationId, msgArgs)
        repeatCnt -= 1
        if repeatCnt > 0:
            BigWorld.callback(interval, Functor(self.showSysNotification, notificationId, msgArgs, repeatCnt, interval, finishCallback))
        elif finishCallback:
            BigWorld.callback(interval, finishCallback)

    def extractItemName(self, msgArr, text):
        if not isinstance(msgArr, tuple):
            return msgArr
        if text.find(CASH_STYLE_MSG) != -1 or text.find(LABOUR_STYLE_MSG) != -1:
            return msgArr
        data = []
        num = min(text.count('%'), len(msgArr))
        for i in xrange(0, num):
            msg = msgArr[i]
            if isinstance(msg, types.StringTypes):
                fontFormat = re.compile('<font color=(.+?)><u>(.+?)</u></a>]</font>', re.DOTALL)
                msg = fontFormat.sub(ItemNameAdd, msg)
            data.append(msg)

        return tuple(data)

    def _getCurGroupType(self):
        if self.groupType > 0:
            return self.groupType
        return gameglobal.rds.ui.team.groupType

    def _preProcessMsg(self, text, data):
        if text.find('<group1>') != -1:
            curGroupType = self._getCurGroupType()
            text = text.replace('<group1>', GROUP_MSG_MAP[curGroupType]['<group1>'])
        if text.find('<group2>') != -1:
            curGroupType = self._getCurGroupType()
            text = text.replace('<group2>', GROUP_MSG_MAP[curGroupType]['<group2>'])
        if text.find(CASH_STYLE_MSG) != -1:
            data = list(data)
            bindCash, cash = data[-2:]
            desc = ''
            if bindCash:
                desc += str(bindCash) + const.BIND_CASH_DESC
            if cash:
                if desc:
                    desc += ','
                desc += str(cash) + const.CASH_DESC
            text = text.replace(CASH_STYLE_MSG, desc)
        if text.find(LABOUR_STYLE_MSG) != -1:
            data = list(data)
            labour, brain = data[-2:]
            desc = ''
            if labour:
                desc += LABOUR_DESC % labour
            if brain:
                if desc:
                    desc += ','
                desc += BRAIN_DESC % brain
            text = text.replace(LABOUR_STYLE_MSG, desc)
        return text

    def formatMsg(self, text, data):
        text = self._preProcessMsg(text, data)
        if not isinstance(data, tuple):
            msg = text % data
        else:
            num = text.count('%')
            msg = text % data[0:num]
        msg = uiUtils.generateStr(msg)
        return richTextUtils.parseSysTxt(msg)

    def chatInChannel(self, channel, roleName, msgId, entId, duration = const.POPUP_MSG_SHOW_DURATION):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        if channel == 0:
            self.chatToWorld(roleName, msg)
        elif channel == 2:
            self.chatToShout(roleName, msg, entId, duration, 0)
        elif channel == 3:
            self.chatToNotice(roleName, msg)

    def resRoleInfo(self, roleName, lv, school):
        gameglobal.rds.ui.chat.showRightMenu(roleName, lv, school)

    def onGetChatBanInfo(self, chatValid, chatBlockFrequency, chatBlockStartTime, chatBlockLastTime):
        self.chatValid = chatValid
        self.chatBlockFrequency = chatBlockFrequency
        self.chatBlockStartTime = chatBlockStartTime
        self.chatBlockLastTime = chatBlockLastTime
        gameglobal.rds.ui.isolate.onGetChatBanInfo()

    def isBlockChat(self):
        if hasattr(self, 'chatValid'):
            if self.chatValid == const.AUTH_VALID_FORBID:
                return True
        if self.getChatBlockChatDelay() > 0:
            return True
        if hasattr(self, 'chatBlockStartTime') and self.chatBlockStartTime > 0:
            return True
        return False

    def getChatBlockChatDelay(self):
        if hasattr(self, 'chatBlockLastTime') and hasattr(self, 'chatBlockStartTime'):
            return max(0, self.chatBlockLastTime - utils.getNow() + self.chatBlockStartTime)
        return 0

    def spritePopMsg(self, msg, time):
        gameglobal.rds.ui.spriteAni.setPopMsg(msg, const.SPRITE_POPO_MSG_YUNYING, time)

    def useItemOfPreDefinedLaba(self, page, pos, labaId, useType):
        pass

    def beChated(self, srcRole, channel, msg):
        gameglobal.rds.ui.chat.addMessage(channel, msg, srcRole)

    def observerChat(self, srcRole, msg):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_OB, msg, srcRole)

    def showGroupMemberLeaveMsg(self, data):
        p = BigWorld.player()
        if not data:
            msgData = GMD.data.get(GMDD.data.LEAVE_FROM_TEAM_SELF, {})
            p.showGameMsg(GMDD.data.GROUP_QUIT_COMPLETE, ())
            for key, val in p.members.items():
                tgtGroupIndex = p.arrangeDict.get(key, 0)
                if p.id != val['id'] and utils.isSameTeam(self.groupIndex, tgtGroupIndex):
                    self._showGameMsgEx(GMDD.data.LEAVE_FROM_TEAM_SELF, msgData, val['roleName'])

        else:
            msgData = GMD.data.get(GMDD.data.LEAVE_FROM_TEAM_MATE, {})
            self._showGameMsgEx(GMDD.data.LEAVE_FROM_TEAM_MATE, msgData, data)

    def onGroupCCManagerSet(self, gbId):
        gamelog.debug('@zmm onGroupCCManagerSet', self.gbId, gbId)

    def onChangeCCMode(self, gbId, ccMode):
        gamelog.debug('@zmm onChangeCCMode', self.gbId, gbId, ccMode)
        gameglobal.rds.ui.teamComm.setOtherVoiceMode(gbId, ccMode)

    def onGetSecretChannelRole(self, publicRole):
        print 'onGetSecretChannelRole', publicRole

    def chatToSecret(self, srcRole, msg, gbId):
        print 'chatToSecret', srcRole, msg, gbId
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SECRET, msg, srcRole, gbId=gbId)

    def payBindCashNotify(self, needBindCash, failedMsgId, callFunction):
        if needBindCash > self.bindCash + self.cash:
            self.showGameMsgEx(failedMsgId, ())
        elif needBindCash > self.bindCash:
            msg = GMD.data.get(GMDD.data.BINDCASH_IS_NOT_ENOUGH, {}).get('text', '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=callFunction, msgType='bindCash', isShowCheckBox=True)
        else:
            callFunction()

    def showYesNoMsgBox(self, msgId, msgData, param):
        msg = GMD.data.get(msgId, {}).get('text')
        if not msg:
            return
        else:
            if not isinstance(msgData, tuple):
                msgString = msg % msgData
            else:
                num = msg.count('%')
                msgString = msg % msgData[0:num]
            yesCallback = param.pop('yesCallback', None)
            if yesCallback:
                if len(yesCallback) == 1:
                    param['yesCallback'] = getattr(self.cell, yesCallback[0])
                else:
                    param['yesCallback'] = Functor(getattr(self.cell, yesCallback[0]), *yesCallback[1:])
            noCallback = param.pop('noCallback', None)
            if noCallback:
                if len(noCallback) == 1:
                    param['noCallback'] = getattr(self.cell, noCallback[0])
                else:
                    param['noCallback'] = Functor(getattr(self.cell, noCallback[0]), *noCallback[1:])
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgString, **param)
            return

    def chatNpcInviteTeam(self, type):
        if type == const.CHAT_INVITE_TEAM_FOR_XUNLING and self.lv < 20:
            self.showGameMsg(GMDD.data.TEAM_INVITE_LEVEL_NOT_ENOUGH, ())
            return
        if self.isInTeamOrGroup():
            self.showGameMsg(GMDD.data.USE_TEAM_CHAT_FRAME_IN_TEAM, ())
            return
        from data import school_data as SD
        from guis import uiUtils
        msg = ''
        if type == const.CHAT_INVITE_TEAM_FOR_XUNLING:
            msg = uiUtils.getTextFromGMD(GMDD.data.NPC_FUNC_INVITE_TEAM) % (self.lv, SD.data[self.school]['name'], self.roleName)
        elif type == const.CHAT_INVITE_TEAM_FOR_YOULI:
            msg = uiUtils.getTextFromGMD(GMDD.data.NPC_FUNC_INVITE_TEAM_FOR_YOULI) % self.roleName
        if not msg:
            return
        msg += ':role'
        self.cell.chatToView(msg, const.POPUP_MSG_SHOW_DURATION)
        self.cell.chatToGroupInfo(msg)
        self.cell.chatToSpace(msg)
