#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chatToFriendProxy.o
from gamestrings import gameStrings
import re
import math
import BigWorld
import keys
import const
import utils
import gameglobal
import clientcom
import gametypes
import gamelog
from Scaleform import GfxValue
from item import Item
from helpers import taboo
from appSetting import Obj as AppSettings
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk, callFilter
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from guis import events
from guis import richTextUtils
from guis import hotkeyProxy
from guis.asObject import ASObject
from callbackHelper import Functor
from guis import menuManager
from cdata import game_msg_def_data as GMDD
PROSECUTE_MSG_NUM = 5
MING_PAI_WIDTH = 18
MING_PAI_HEIGHT = 18

class ChatToFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChatToFriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFriendInfo': self.onGetFriendInfo,
         'sendMsgToFriend': self.onSendMsgToFriend,
         'getFriendHistory': self.onGetFriendHistory,
         'getHistoryOpen': self.onGetHistoryOpen,
         'getInputColor': self.onGetInputColor,
         'saveInputColor': self.onSaveInputColor,
         'linkLeftClick': self.onLinkLeftClick,
         'minimizeChat': self.onMinimizeChat,
         'closeHistory': self.onCloseHistory,
         'prosecute': self.onProsecute,
         'isShowYixin': self.isShowYixin,
         'getGroupInfo': self.onGetGroupInfo,
         'getoffsetIndex': self.onGetOffsetIndex,
         'startSoundRecord': self.onStartSoundRecord,
         'endSoundRecord': self.onEndSoundRecord,
         'getSounndRecordHotkey': self.onGetSounndRecordHotkey,
         'enableSoundRecord': self.onEnableSoundRecord,
         'mergePlayerChat': self.onMergePlayerChat,
         'enableGroupChat': self.onEnableGroupChat,
         'findNpc': self.onFindNpc,
         'npcWait': self.onNpcWait}
        self.reset()
        self.chatToGroupStamp = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHAT_TO_FRIEND, self.closePanel, True)
        self.addEvent(events.EVENT_RENAME_GROUP, self.refreshGroupName, isGlobal=True)

    def reset(self):
        self.friends = []
        self.friendMeds = {}
        self.initMsgs = {}
        self.isOpenHistory = {}
        self.chatMsgs = {}
        self.chatAllMsg = {}
        self.historyMsgNum = 0
        self.groupMeds = {}
        self.groups = []
        self.sendId = None

    def isShowYixin(self, *arg):
        isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
        return GfxValue(isShowYixin)

    def replaceFriend(self, data):
        fid = str(data['id'])
        find = False
        for i in xrange(0, len(self.friends)):
            if fid == self.friends[i]['id']:
                self.friends[i] = data
                find = True

        if find == False:
            if self.friendMeds.has_key(fid):
                self.friends.append(data)

    def show(self, initMsg = None, friendData = {}, isOpenHistory = False, addGroupChat = False):
        friendId = str(friendData['id'])
        gbId = int(friendId)
        if BigWorld.player().friend.get(gbId):
            if BigWorld.player().friend.get(gbId).temp:
                BigWorld.player().base.queryTempFriendIsOn(gbId)
        if addGroupChat and gameglobal.rds.configData.get('enableChatGroup', False):
            gameglobal.rds.ui.groupChat.addPlayerChatItem(friendData, initMsg)
            return
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHAT_TO_FRIEND)
            if friendData.get('npcId') and self.friendMeds.get(str(friendId), None):
                med = ASObject(self.friendMeds[str(friendId)])
                med.swapPanelToFront()
                if initMsg:
                    for msg in initMsg:
                        self.receiveMsg(friendId, msg, False)

                return
            self.friends.append(friendData)
            self.isOpenHistory[friendId] = isOpenHistory
            tempInitMsg = self.chatMsgs.get(friendId, [])
            if initMsg:
                tempInitMsg.extend(initMsg)
            self.initMsgs[friendId] = tempInitMsg
            return

    def onGetInputColor(self, *args):
        color = AppSettings.get(keys.SET_UI_INFO + '/chatToFriend/color', '')
        return GfxValue(color)

    def onSaveInputColor(self, *args):
        color = args[3][0].GetString()
        AppSettings[keys.SET_UI_INFO + '/chatToFriend/color'] = color
        AppSettings.save()

    def onMinimizeChat(self, *arg):
        fid = int(arg[3][0].GetString())
        p = BigWorld.player()
        if fid != const.XINYI_MANAGER_ID:
            fVal = p.getFValByGbId(fid)
            if fVal:
                self.uiAdapter.friend.addMinChat([fid, fVal.name])
        elif p.xinYiManager:
            name = p.xinYiManager['name'] + gameStrings.TEXT_AVATAR_2461
            self.uiAdapter.friend.addMinChat([fid,
             name,
             '',
             p.getXinYiMsgPhoto(),
             False])

    def onCloseHistory(self, *arg):
        self.historyMsgNum = 0

    def closePanel(self, widgetId, multiID):
        for groupId in self.groupMeds.keys():
            if groupId in self.groups:
                mediator = self.groupMeds.get(groupId, {}).get('mediator', None)
                if mediator and mediator.Invoke('getMultiID').GetNumber() == multiID:
                    self.groups.remove(groupId)
                    callbackHandler = self.groupMeds.get(groupId, {}).get('callbackHandler', None)
                    if callbackHandler:
                        BigWorld.cancelCallback(callbackHandler)
                    del self.groupMeds[groupId]
                    self.uiAdapter.unLoadWidget(multiID)
                    return

        closeFid = None
        for fid in self.friendMeds.keys():
            if self.friendMeds[fid].Invoke('getMultiID').GetNumber() == multiID:
                closeFid = fid
                break

        if closeFid:
            self.friendMeds.pop(closeFid)
            friend = self.getFriendByFid(closeFid)
            self.friends.remove(friend)
            if self.isOpenHistory.has_key(closeFid):
                self.isOpenHistory.pop(closeFid)
            if int(closeFid) not in gameglobal.rds.ui.friend.minChatArr and self.chatMsgs.has_key(closeFid):
                self.chatMsgs.pop(closeFid)
            if len(self.chatMsgs) + len(self.friends) + len(self.groups) + len(self.groupMeds) == 0:
                self.hide(self.destroyOnHide)
            if closeFid in self.chatAllMsg:
                self.chatAllMsg.pop(closeFid)
        self.uiAdapter.unLoadWidget(multiID)
        if closeFid:
            gameglobal.rds.ui.groupChat.removeGroupInChat(int(closeFid))

    def updateStatus(self, fid, data):
        self.replaceFriend(data)
        friend = self.getFriendByFid(fid)
        if friend or fid != const.XINYI_MANAGER_ID:
            med = self.getMeidatorByFid(fid)
            if med:
                med.Invoke('updateFriend', ())

    def closeChatByFid(self, fid):
        med = self.getMeidatorByFid(fid)
        if med:
            med.Invoke('close', ())

    def _asWidgetClose(self, widgetId, multiID):
        self.closePanel(widgetId, multiID)

    def clearWidget(self):
        for med in self.friendMeds.values():
            self.uiAdapter.unLoadWidget(med.Invoke('getMultiID').GetNumber())

    def onGetFriendInfo(self, *args):
        mediator = args[3][0]
        for item in reversed(self.friends):
            if not self.friendMeds.has_key(item['id']):
                self.friendMeds[item['id']] = mediator
                if self.initMsgs.has_key(item['id']):
                    for msg in self.initMsgs[item['id']]:
                        self.receiveMsg(item['id'], msg, False)

                    self.initMsgs.pop(item['id'])
                return self.friendToGfxValue(item)

        for key in self.friendMeds:
            if str(key) == mediator.Invoke('getFriendGbId').GetString():
                for item in self.friends:
                    if item['id'] == key:
                        return self.friendToGfxValue(item)

                break

        if len(self.friends):
            return self.friendToGfxValue(self.friends[0])
        else:
            return self.friendToGfxValue(None)

    def onGetHistoryOpen(self, *args):
        fid = args[3][0].GetString()
        return GfxValue(bool(self.isOpenHistory.has_key(fid) and self.isOpenHistory[fid]))

    def delFont(self, matchobj):
        return matchobj.group(1)

    def onSendMsgToFriend(self, *args):
        id = int(args[3][0].GetString())
        msg = unicode2gbk(args[3][1].GetString())
        self._sendAsMsgToFriend(id, msg)

    def _sendAsMsgToFriend(self, id, msg, autoInput = False):
        msg = uiUtils.parseMsg(msg)
        reFormat = re.compile('<FONT COLOR=\"#FFFFE6\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        if richTextUtils.isSysRichTxt(msg) and not autoInput:
            BigWorld.player().showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        if BigWorld.player().friend.isValidGroup(id):
            self._sendMsgToGroup(id, msg)
        else:
            self._sendMsgToFid(id, msg)

    def onGetFriendHistory(self, *args):
        fid = int(args[3][0].GetString())
        npcPid = int(args[3][1].GetNumber())
        pageNum = args[3][2].GetNumber()
        self._getHistoryByFid(fid, npcPid, pageNum)

    def hasChatToFriend(self):
        return len(self.friendMeds.values()) > 0

    def appenInputMsg(self, msg):
        med = self.getTopMediator()
        if med:
            med.Invoke('appendInputMsg', GfxValue(gbk2unicode(msg)))

    def receiveMsg(self, fid, msg, recordMsg = True):
        fid = str(fid)
        if recordMsg:
            if not self.chatMsgs.has_key(fid):
                self.chatMsgs[fid] = []
            self.chatMsgs.get(fid).append(msg)
        self.chatAllMsg.setdefault(fid, []).append(msg)
        mediator = self.getMeidatorByFid(fid)
        mediator.Invoke('addMsg', self.msgToGfxVlaue(msg, fid))

    def appendHistoryMsg(self, fid, msgs, total, offset, limit):
        self.historyMsgNum = total
        totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
        currentPage = totalPage - math.ceil(offset / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
        med = self.getMeidatorByFid(fid)
        if med:
            gfxMsg = []
            for msg in msgs:
                gfxMsg.append(self.msgToGfxVlaue(msg, None))

            med.Invoke('appendHistoryMsgs', (uiUtils.array2GfxAarry(gfxMsg), GfxValue(totalPage), GfxValue(currentPage)))
        else:
            gameglobal.rds.ui.groupChatHistoryMsg.show(fid, msgs, totalPage, currentPage)

    def openHistory(self, fid, isOpen = True):
        med = self.getMeidatorByFid(fid)
        if med:
            med.Invoke('openHistory', GfxValue(isOpen))

    def friendToGfxValue(self, friend):
        gfxFriend = self.movie.CreateObject()
        if not friend:
            return gfxFriend
        else:
            gfxFriend.SetMember('name', GfxValue(gbk2unicode(friend['name'])))
            fullName = friend.get('fullName', friend['name'])
            photo = friend['photo']
            if uiUtils.isDownloadImage(photo):
                imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                if not clientcom.isFileExist(imagePath):
                    BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
                else:
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            gfxFriend.SetMember('photo', GfxValue(photo))
            gfxFriend.SetMember('signature', GfxValue(gbk2unicode(friend['signature'])))
            gfxFriend.SetMember('id', GfxValue(friend['id']))
            gfxFriend.SetMember('school', GfxValue(uiConst.SCHOOL_FRAME_DESC.get(friend.get('school', 0), 'all')))
            gfxFriend.SetMember('level', GfxValue(friend.get('level', 0)))
            gfxFriend.SetMember('photoBorderIcon', GfxValue(friend.get('photoBorderIcon', '')))
            if BigWorld.player()._isSoul():
                gfxFriend.SetMember('stateDesc', GfxValue(gbk2unicode(const.FRIEND_STATE_DESC[gametypes.FRIEND_STATE_ONLINE])))
            else:
                gfxFriend.SetMember('stateDesc', GfxValue(gbk2unicode(const.FRIEND_STATE_DESC[friend['state']])))
            gfxFriend.SetMember('isBindYixin', GfxValue(friend['yixinOpenId']))
            fVal = BigWorld.player().getFValByGbId(int(friend['id']))
            if fVal:
                gfxFriend.SetMember('groupId', GfxValue(fVal.group))
                fullName = uiUtils.getNameWithMingPain(fullName, fVal.mingpaiId)
            gfxFriend.SetMember('fullName', GfxValue(gbk2unicode(fullName)))
            gfxFriend.SetMember('isGlobalFriend', GfxValue(BigWorld.player().isGobalFirendGbId(int(friend['id']))))
            npcId = friend.get('npcId', 0)
            if friend['id'] == '-1' and not npcId:
                gfxFriend.SetMember('isKefuFriend', GfxValue(True))
            else:
                gfxFriend.SetMember('isKefuFriend', GfxValue(False))
            gfxFriend.SetMember('npcId', GfxValue(npcId))
            if npcId and BigWorld.player().needPushNpcQuest(npcId):
                BigWorld.player().needNpcPush = 0
                gfxFriend.SetMember('needNpcPush', GfxValue(True))
            else:
                gfxFriend.SetMember('needNpcPush', GfxValue(False))
            return gfxFriend

    def msgToGfxVlaue(self, msg, fid = None):
        gfxMsg = self.movie.CreateObject()
        gfxMsg.SetMember('isMe', GfxValue(msg['isMe']))
        gfxMsg.SetMember('time', GfxValue(msg['time']))
        gfxMsg.SetMember('msg', GfxValue(gbk2unicode(msg['msg'])))
        gfxMsg.SetMember('isRedPacket', GfxValue(utils.isRedPacket(msg['msg'])))
        if fid == '-1':
            gfxMsg.SetMember('isKefu', GfxValue(True))
        p = BigWorld.player()
        photo = msg['photo']
        if uiUtils.isDownloadImage(photo):
            imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            if not clientcom.isFileExist(imagePath):
                BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
            else:
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        gfxMsg.SetMember('photo', GfxValue(gbk2unicode(photo)))
        gfxMsg.SetMember('photoBorderIcon', GfxValue(gbk2unicode(msg.get('photoBorderIcon', ''))))
        mpId = 0
        if msg['isMe']:
            mpId = p.selectedMPId
        elif fid:
            fVal = p.getFValByGbId(int(fid))
            if fVal:
                mpId = fVal.mingpaiId
        name = uiUtils.getNameWithMingPain(msg['name'], mpId)
        gfxMsg.SetMember('name', GfxValue(gbk2unicode(name)))
        return gfxMsg

    def getFriendByFid(self, fid):
        fid = str(fid)
        for friend in self.friends:
            if fid == friend['id']:
                return friend

    def getMeidatorByFid(self, fid):
        if fid > 0:
            for med in self.friendMeds.values():
                if med.Invoke('getFriendGbId').GetString() == str(fid):
                    return med

        fid = str(fid)
        friend = self.getFriendByFid(fid)
        if friend or fid == const.XINYI_MANAGER_ID:
            if friend:
                return self.friendMeds.get(friend.get('id'))
            else:
                return self.friendMeds.get(fid)
        else:
            return None

    def getMediatorByMultiID(self, multiID):
        for fid in self.friendMeds.keys():
            if self.friendMeds[fid].Invoke('getMultiID').GetNumber() == multiID:
                return self.friendMeds[fid]

    def getTopMediator(self):
        if len(self.friendMeds.values()) > 0:
            med = self.friendMeds.values()[0]
            topMid = med.Invoke('getTopChatPanelMid').GetNumber()
            if topMid > 0:
                return self.getMediatorByMultiID(topMid)

    def _sendMsgToFid(self, fid, msg):
        if fid == const.FRIEND_SYSTEM_ID:
            return
        p = BigWorld.player()
        rawMsg = re.sub('</?FONT.*?>', '', msg, 0, re.DOTALL)
        if utils.isEmpty(rawMsg):
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_EMPTY, ())
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if fid != const.XINYI_MANAGER_ID:
            fVal = p.getFValByGbId(fid)
            if not isNormal:
                p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
                if fVal:
                    gameglobal.rds.ui.chat._reportFontlibMonitor(const.CHAT_FRIEND, fVal.name, msg, const.FONT_LIB_MONITOR_MASK_SINGLE)
                    p.addRecentFriend(fid)
                return
        ret = False
        mediator = self.getTopMediator()
        if fid != const.XINYI_MANAGER_ID:
            if mediator:
                ret = mediator.Invoke('isSendMsgToYixin', ()).GetBool()
                if ret and not richTextUtils.isSoundRecord(msg):
                    msg = msg + ':toyixin'
            if p.isGobalFirendGbId(fid):
                p.base.chatToRemote(int(fid), msg)
            else:
                p.cell.chatToFriend(int(fid), fVal and fVal.name or '', msg)
        elif p.xinYiManager:
            self.sendMsgToXinyiManager(msg)

    @callFilter(3)
    def sendMsgToXinyiManager(self, msg):
        p = BigWorld.player()
        p.base.talkToXinyiManager(msg)

    def _getHistoryByFid(self, fid, npcPid, pageNum):
        p = BigWorld.player()
        if pageNum and self.historyMsgNum:
            totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
            offSet = (totalPage - pageNum) * uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM
            limit = min(uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM, self.historyMsgNum - offSet)
        else:
            offSet = 0
            limit = uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM
        return p.fetchChatHistory(int(fid), int(offSet), int(limit), npcPid)

    def _getSlefInfo(self):
        p = BigWorld.player()
        return {'name': p.realRoleName,
         'id': str(p.gbId),
         'photo': p._getFriendPhoto(p),
         'signature': p.friend.signature}

    def isShowed(self, fid):
        return self.getFriendByFid(fid) != None

    def isOpened(self, fid):
        fid = str(fid)
        med = self.friendMeds.get(fid, None)
        if med:
            if med.Invoke('getFriendGbId').GetString() != fid:
                med.Invoke('close', ())
                if fid in self.friendMeds.keys():
                    self.friendMeds.pop(fid)
                return False
            else:
                return True
        return False

    def onLinkLeftClick(self, *arg):
        fid = arg[3][0].GetString()
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][1].GetString())
        if roleName[:3] == 'ret':
            retCode = int(roleName[3:])
            p.base.chatToItem(retCode, fid)
        elif roleName[:4] == 'item':
            pos = roleName.find(':')
            if pos == -1:
                itemId = roleName[4:]
                it = Item(int(itemId), 1, False)
            else:
                itemId = roleName[4:pos]
                it = Item(int(itemId), 1, False)
                itdata = roleName[pos + 1:].split(':')
                for i in xrange(0, len(itdata), 2):
                    attrv = itdata[i + 1]
                    if attrv.isdigit():
                        attrv = int(attrv)
                    setattr(it, itdata[i], attrv)

            self.showTooltip(const.CHAT_TIPS_ITEM, fid, gameglobal.rds.ui.inventory.GfxToolTip(it))
        elif roleName[:4] == 'task':
            self.showTooltip(const.CHAT_TIPS_TASK, fid, gameglobal.rds.ui.chat.taskToolTip(int(roleName[4:])))
        elif roleName[:4] == 'achv':
            self.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, fid, gameglobal.rds.ui.chat.achieveToolTip(roleName[4:]))
        elif roleName.startswith('sprite'):
            p.base.chatToSprite(int(roleName[len('sprite'):]), fid)

    def showTooltip(self, tipsType, fid, gfxTipData):
        mediator = self.getMeidatorByFid(fid)
        if mediator:
            mediator.Invoke('showTooltip', (GfxValue(tipsType), GfxValue(fid), gfxTipData))

    def onProsecute(self, *arg):
        name = unicode2gbk(arg[3][0].GetString().strip())
        fid = arg[3][1].GetString()
        msg = self.chatAllMsg.get(fid, [])
        pMsg = ''
        if msg:
            msg = [ item['msg'] for item in msg ]
            if len(msg) > PROSECUTE_MSG_NUM:
                pMsg = ';'.join(msg[0:PROSECUTE_MSG_NUM])
            else:
                pMsg = ';'.join(msg)
        gameglobal.rds.ui.prosecute.show(name, uiConst.MENU_FRIEND, msg=pMsg)
        gameglobal.rds.ui.prosecute.channel = const.CHAT_FRIEND

    def onDownloadPhoto(self, status, callbackArgs):
        pass

    def showChatGroup(self, groupId):
        if groupId in self.groups:
            return
        self.groups.append(groupId)
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHAT_TO_FRIEND)

    def onGetGroupInfo(self, *args):
        ret = {}
        mediator = args[3][0]
        for groupId in self.groups:
            if not self.groupMeds.has_key(groupId):
                self.groupMeds[groupId] = {}
                callbackHandler = None
                if utils.getNow() - self.chatToGroupStamp > const.CHAR_TO_GROUP_COOLDOWN:
                    ret['sendEnable'] = True
                else:
                    ret['sendEnable'] = False
                    callbackHandler = BigWorld.callback(self.chatToGroupStamp + const.CHAR_TO_GROUP_COOLDOWN - utils.getNow(), Functor(self.setSendBtnEnable, mediator, True))
                self.groupMeds[groupId]['callbackHandler'] = callbackHandler
                self.groupMeds[groupId]['mediator'] = mediator
                ret['isChatToGroup'] = True
                ret['groupId'] = groupId
                ret['groupName'] = BigWorld.player().friend.getNameByGroupId(groupId)
                return uiUtils.dict2GfxDict(ret, True)

        ret['isChatToGroup'] = False
        ret['groupId'] = 0
        return uiUtils.dict2GfxDict(ret, True)

    def onGetOffsetIndex(self, *args):
        maxOffset = 0
        for med in self.friendMeds.values():
            if med:
                offset = med.Invoke('getOffsetIndex').GetNumber()
                if maxOffset < offset:
                    maxOffset = offset

        return GfxValue(maxOffset + 1)

    def groupReceiveMsg(self, groupId, msg, stamp):
        self.chatToGroupStamp = stamp
        mediator = self.groupMeds.get(groupId, {}).get('mediator', None)
        if mediator:
            mediator.Invoke('addMsg', self.msgToGfxVlaue(msg, None))
            mediator.Invoke('cleatTxt')
        for groupId in self.groups:
            mediator = self.groupMeds.get(groupId, {}).get('mediator', None)
            if mediator:
                self.setSendBtnEnable(mediator, False)
                callbackHandler = BigWorld.callback(const.CHAR_TO_GROUP_COOLDOWN, Functor(self.setSendBtnEnable, mediator, True))
                self.groupMeds[groupId]['callbackHandler'] = callbackHandler

    def _sendMsgToGroup(self, groupId, msg):
        p = BigWorld.player()
        if utils.getNow() - self.chatToGroupStamp <= const.CHAR_TO_GROUP_COOLDOWN:
            p.showGameMsg(GMDD.data.FRIEND_GROUP_CHAT_MSG_COOLDOWN, ())
            return
        rawMsg = re.sub('</?FONT.*?>', '', msg, 0, re.DOTALL)
        if len(rawMsg) > const.FRIEND_CHAT_MSG_MAX_LEN:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TOO_LONG, ())
            return
        if utils.isEmpty(rawMsg):
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_EMPTY, ())
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if isNormal:
            p.base.chatToGroupFriend(groupId, msg)

    def setSendBtnEnable(self, mediator, isEnable):
        if mediator:
            mediator.Invoke('setSendBtnEnable', GfxValue(isEnable))

    def isGroupOpened(self, groupId):
        if groupId in self.groups and self.groupMeds.get(groupId, {}).get('mediator', None):
            return True
        else:
            return False

    def friendGroupDeleted(self, groupId):
        if self.isGroupOpened(groupId):
            mediator = self.groupMeds.get(groupId, {}).get('mediator', None)
            multiID = mediator.Invoke('getMultiID').GetNumber()
            self.groups.remove(groupId)
            callbackHandler = self.groupMeds.get(groupId, {}).get('callbackHandler', None)
            if callbackHandler:
                BigWorld.cancelCallback(callbackHandler)
            del self.groupMeds[groupId]
            self.uiAdapter.unLoadWidget(multiID)

    def refreshGroupName(self, event):
        groupId = event.data.get('groupId')
        if self.isGroupOpened(groupId):
            mediator = self.groupMeds.get(groupId, {}).get('mediator', None)
            mediator.Invoke('refreshGroupName', GfxValue(gbk2unicode(event.data.get('groupName'))))

    def onStartSoundRecord(self, *arg):
        p = BigWorld.player()
        p.recordUploadTranslateSound(self.submitSoundRecord)

    def onEndSoundRecord(self, *arg):
        med = self.getTopMediator()
        for gbId, value in self.friendMeds.iteritems():
            if value == med:
                self.sendId = int(gbId)

        p = BigWorld.player()
        p.endSoundRecord()
        p.addSoundRecordNum(False, True)

    def onGetSounndRecordHotkey(self, *arg):
        _, _, desc = hotkeyProxy.getChatToFriendSoundRecordKey()
        return GfxValue(gbk2unicode(desc))

    def onEnableSoundRecord(self, *arg):
        val = BigWorld.player().enableSoundRecord()
        return GfxValue(val)

    def submitSoundRecord(self, duration, key, content):
        content = unicode2gbk(content)
        content = utils.soundRecordRichText(key, duration) + content
        if self.sendId:
            self._sendAsMsgToFriend(self.sendId, content, autoInput=True)

    def swapPanelToFront(self, fid):
        med = self.getMeidatorByFid(fid)
        if med:
            med.Invoke('swapPanelToFront')

    def onMergePlayerChat(self, *args):
        id = int(args[3][0].GetString())
        menuManager.getInstance().menuTarget.apply(gbId=id, extraInfo={'groupNUID': 0})
        menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_GROUP_CHAT_MERGE)
        gameglobal.rds.ui.chat.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def surePlayerMergeChat(self, gbId):
        p = BigWorld.player()
        if gbId != const.XINYI_MANAGER_ID:
            fVal = p.getFValByGbId(gbId)
            if fVal:
                multiID = self.friendMeds[str(gbId)].Invoke('getMultiID').GetNumber()
                self.closePanel(uiConst.WIDGET_CHAT_TO_FRIEND, multiID)
                msg = self.chatAllMsg.get(str(gbId), [])
                gameglobal.rds.ui.groupChat.addPlayerChatItem(p._createFriendData(fVal), msg)
        else:
            multiID = self.friendMeds[str(gbId)].Invoke('getMultiID').GetNumber()
            self.closePanel(uiConst.WIDGET_CHAT_TO_FRIEND, multiID)
            msg = self.chatAllMsg.get(str(gbId), [])
            gameglobal.rds.ui.groupChat.addPlayerChatItem(gameglobal.rds.ui.friend.createXinYiManagerData(), msg)

    def onEnableGroupChat(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableChatGroup', False))

    def onFindNpc(self, *args):
        npcId = int(args[3][0].GetNumber())
        npcInfo = self.uiAdapter.friend.getNpcInfo(npcId, False)
        uiUtils.findPosById(npcInfo.get('seekId', 0))
        BigWorld.player().base.acceptQuestNF()

    def onNpcWait(self, *args):
        npcId = int(args[3][0].GetNumber())
        self.hide()
