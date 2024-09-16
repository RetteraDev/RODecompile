#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCC.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import gamelog
import keys
from appSetting import Obj as AppSettings
from callbackHelper import Functor
from helpers import cc
from helpers import ccControl
from guis import uiUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
ROOM_TYPE_TMP = 0
ROOM_TYPE_GUILD = 1
ROOM_TYPE_SYS = 2
enterRoomInfo = []

class RoomInfo:

    def __init__(self):
        self.cid = None
        self.tag = None


class ImpCC(object):

    def getTeamCCInvite(self, playerName):
        msg = const.CC_INVITE_TEAM % playerName
        if hasattr(self, 'currentJoinTag'):
            if cc.getTeamTag() != self.currentJoinTag:
                if hasattr(self, 'nowShowId') and self.nowShowId:
                    if cc.getTeamTag() in self.nowShowId:
                        return
                else:
                    self.nowShowId = []
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doJoinTeamChannel), noCallback=Functor(self.rejectJoinInvitedChannel, playerName, '0'))
                self.nowShowId.append(cc.getTeamTag())
            else:
                self.cell.existCCInvite(playerName, '0')
        else:
            if hasattr(self, 'nowShowId') and self.nowShowId:
                if cc.getTeamTag() in self.nowShowId:
                    return
            else:
                self.nowShowId = []
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doJoinTeamChannel), noCallback=Functor(self.rejectJoinInvitedChannel, playerName, '0'))
            self.nowShowId.append(cc.getTeamTag())

    def _keepRoomInfo(self):
        count = len(self.enterCCRoomInfo)
        if count > 0:
            self.needKeepCCRoomInfo = self.enterCCRoomInfo[count - 1]

    def getLastRoomInfo(self):
        count = len(self.enterCCRoomInfo)
        if count > 0:
            return self.enterCCRoomInfo[count - 1]

    def doJoinTeamChannel(self):
        gamelog.debug('jinjj!@!@!@--------doJoinTeamChannel')
        lastRoomInfo = self.getLastRoomInfo()
        self.nowShowId = []
        if lastRoomInfo:
            if lastRoomInfo.tag != None:
                if lastRoomInfo.tag == cc.getTeamTag():
                    self.showInRoomMsg()
                    return
        self._keepRoomInfo()
        cc.joinTeamRoom('TEAM', self._doJoinTeamRoomSuccess)

    def showInRoomMsg(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.CC_RESPONSE_PLAYER_EXIST, p.realRoleName)

    def doJoinAuthorityChannel(self):
        roomid = SCD.data.get('cc_public_channel', const.CC_PUBLIC_CHANNEL)
        lastRoomInfo = self.getLastRoomInfo()
        self.currentJoinTagTemp = None
        if lastRoomInfo:
            if lastRoomInfo.cid != None:
                if lastRoomInfo.cid == str(roomid):
                    self.showInRoomMsg()
                    return
        self.currentJoinIdTemp = roomid
        self._keepRoomInfo()
        gamelog.debug('jinjj!@!@!@--------doJoinAuthorityChannel', roomid)
        cc.joinRoom(str(roomid), '', self._doJoinRoomSuccess)

    def _doJoinTeamRoomSuccess(self, cid):
        self.currentJoinTag = cc.getTeamTag()
        gamelog.debug('jinjj----_doJoinTeamRoomSuccess-', self.currentJoinTag, cid)
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.CC_ENTER_SUCCESS, ())
        roomInfo = RoomInfo()
        roomInfo.cid = cc.getCurrentCid()
        roomInfo.tag = cc.getTeamTag()
        self._doPushRoomInfo(roomInfo)
        gameglobal.rds.ui.cCControl.refreshPanel()

    def getOtherCCInvite(self, playerName, roomId, roomType, password):
        if roomType == ROOM_TYPE_TMP:
            msg = const.CC_INVITE_OTHER % playerName
            if hasattr(self, 'currentJoinTag'):
                if roomId == self.currentJoinTag:
                    self.cell.existCCInvite(playerName, '0')
                    return
        elif roomType == ROOM_TYPE_GUILD:
            msg = const.CC_INVITE_GUILD % playerName
            if str(cc.getCurrentCid()) == roomId:
                return
        else:
            msg = const.CC_INVITE_SYS % playerName
            if str(cc.getCurrentCid()) == roomId:
                return
        if hasattr(self, 'nowShowId') and self.nowShowId:
            if roomId in self.nowShowId:
                return
        else:
            self.nowShowId = []
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doJoinInvitedChannel, playerName, roomId, password, roomType), noCallback=Functor(self.rejectJoinInvitedChannel, playerName, roomId))
        self.nowShowId.append(roomId)

    def doJoinGuildCCChannel(self, pwd = ''):
        p = BigWorld.player()
        if not hasattr(p, 'guild'):
            return
        else:
            roomId = p.guild.roomId
            gamelog.debug('jinjj------------------roomId', roomId)
            if not roomId:
                p.cell.applyCCRoom()
            else:
                lastRoomInfo = self.getLastRoomInfo()
                if lastRoomInfo:
                    if lastRoomInfo.cid != None:
                        if lastRoomInfo.cid == roomId:
                            self.showInRoomMsg()
                            return
                self.currentJoinTagTemp = None
                self._keepRoomInfo()
                self.currentJoinIdTemp = roomId
                cc.joinRoom(roomId, pwd, self._doJoinRoomSuccess)
            return

    def doInviteOtherCCGuild(self, playerName):
        p = BigWorld.player()
        if not hasattr(p, 'guild'):
            return
        roomId = p.guild.roomId
        if not roomId:
            return
        p.cell.doOtherCCInvite([playerName], roomId, 1, '')

    def enterCCRoomByPassWord(self, passWord):
        if hasattr(self, 'currentJoinIdTemp'):
            self._keepRoomInfo()
            cc.joinRoom(self.currentJoinIdTemp, passWord, self._doJoinRoomSuccess)

    def doJoinInvitedChannel(self, playerName, roomId, password, roomType):
        self.cell.acceptCCInvite(playerName, roomId)
        lastRoomInfo = self.getLastRoomInfo()
        self.nowShowId = []
        if roomType == ROOM_TYPE_TMP:
            if lastRoomInfo:
                if lastRoomInfo.tag != None:
                    if lastRoomInfo.tag == roomId:
                        self.showInRoomMsg()
                        return
            self.currentJoinTagTemp = roomId
            self._keepRoomInfo()
            cc.joinRoomTag(roomId, 'Single', self._doJoinRoomSuccess)
        else:
            if lastRoomInfo:
                if lastRoomInfo.cid != None:
                    if lastRoomInfo.cid == roomId:
                        self.showInRoomMsg()
                        return
            self.currentJoinTagTemp = None
            self._keepRoomInfo()
            cc.joinRoom(roomId, password, self._doJoinRoomSuccess)

    def rejectJoinInvitedChannel(self, playerName, roomId):
        self.cell.rejectCCInvite(playerName, roomId)
        self.nowShowId = []

    def doSendLink(self, fromWho, roomId, isTmp = True, style = 0, msg = None):
        if not msg:
            content = const.CC_CLICK_INTO_ROOM % fromWho
        else:
            content = msg
        msg = uiUtils.getCCHyperLink(roomId, isTmp, style, content)
        gameglobal.rds.ui.sendLink(msg)

    def doSendNoticeInstall(self):
        BigWorld.player().showGameMsg(GMDD.data.CC_IS_INSTALL_NOTICE, ())

    def doAnalysisLink(self, role):
        if role.find('rtcd') != -1:
            roomId = role[4:]
            self.currentJoinTagTemp = roomId
            self.currentJoinTagTemp = None
            self._keepRoomInfo()
            cc.joinRoomTag(roomId, 'Single', self._doJoinRoomSuccess)
        else:
            roomId = role[3:]
            cc.joinRoom(roomId, '', self._doJoinRoomSuccess)

    def _doJoinRoomSuccess(self, cid):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.CC_ENTER_SUCCESS, ())
        gamelog.debug('jinjj join~~', cid)
        roomInfo = RoomInfo()
        roomInfo.cid = cc.getCurrentCid()
        if hasattr(self, 'currentJoinTagTemp'):
            roomInfo.tag = self.currentJoinTagTemp
            self.currentJoinTag = self.currentJoinTagTemp
            self._doPushRoomInfo(roomInfo)
            gameglobal.rds.ui.cCControl.refreshPanel()

    def _doPushRoomInfo(self, info):
        count = len(self.enterCCRoomInfo)
        self.needKeepCCRoomInfo = None
        for item in self.enterCCRoomInfo:
            if item.cid == info.cid:
                return

        if count > 0:
            if self.enterCCRoomInfo[count - 1].cid != info.cid:
                self.enterCCRoomInfo.append(info)
        else:
            self.enterCCRoomInfo.append(info)

    def doCreateRoom(self, nameList):
        name_tag = cc.getPlayerTag()
        lastRoomInfo = self.getLastRoomInfo()
        if lastRoomInfo:
            if lastRoomInfo.tag != None:
                if lastRoomInfo.tag == name_tag:
                    self._doCreatRoomSuccess(nameList, 0)
                    return
        self.currentJoinTagTemp = name_tag
        cc.joinRoomTag(name_tag, 'Single', Functor(self._doCreatRoomSuccess, nameList))

    def _doCreatRoomSuccess(self, nameList, cid):
        if not hasattr(self, 'currentJoinTagTemp'):
            return
        else:
            self.currentJoinTag = self.currentJoinTagTemp
            roomInfo = RoomInfo()
            roomInfo.cid = cc.getCurrentCid()
            roomInfo.tag = self.currentJoinTagTemp
            self._doPushRoomInfo(roomInfo)
            gamelog.debug('jinjj----doRoomCreateSuccess-', nameList)
            p = BigWorld.player()
            if self.currentJoinTag != None:
                p.cell.doOtherCCInvite(nameList, self.currentJoinTag, 0, '')
            return

    def doShareCurrentCid(self):
        p = BigWorld.player()
        if hasattr(self, 'currentJoinTag'):
            if self.currentJoinTag != None:
                self.doSendLink(p.realRoleName, self.currentJoinTag)
            else:
                self.doSendLink(p.realRoleName, cc.getCurrentCid(), False)
        else:
            self.doSendLink(p.realRoleName, cc.getCurrentCid(), False)

    def doCreateTeamRoom(self):
        lastRoomInfo = self.getLastRoomInfo()
        if lastRoomInfo:
            if lastRoomInfo.tag != None:
                if lastRoomInfo.tag == cc.getTeamTag():
                    p = BigWorld.player()
                    p.cell.doTeamCCInvite()
                    return
        self._keepRoomInfo()
        gamelog.debug('jinjj------doCreateTeamRoom---------')
        cc.joinTeamRoom('TEAM', self._doCreatTeamSuccess)

    def _doCreatTeamSuccess(self, cid):
        gamelog.debug('jinjj----', cid)
        p = BigWorld.player()
        p.cell.doTeamCCInvite()
        self.currentJoinTag = cc.getTeamTag()
        roomInfo = RoomInfo()
        roomInfo.cid = cc.getCurrentCid()
        roomInfo.tag = cc.getTeamTag()
        self._doPushRoomInfo(roomInfo)
        gameglobal.rds.ui.cCControl.refreshPanel()

    def doClear(self):
        self.currentJoinTag = None
        self.currentJoinTagTemp = None
        self.enterCCRoomInfo = []
        gamelog.debug('jinjj leave cc')
        gameglobal.rds.ui.cCControl.refreshPanel(True)

    def doPopCC(self, cid):
        gamelog.debug('jinjj leave room', self.enterCCRoomInfo, self.needKeepCCRoomInfo)
        count = len(self.enterCCRoomInfo)
        if count > 0:
            if self.needKeepCCRoomInfo == None:
                self.enterCCRoomInfo.pop()
                self.currentJoinTag = None
                self.currentJoinTagTemp = None
                count = len(self.enterCCRoomInfo)
                if count > 0:
                    roominfo = self.enterCCRoomInfo[count - 1]
                    if roominfo.tag != None:
                        gamelog.debug('jinjj doPopCC', roominfo.tag)
                        cc.joinRoomTag(roominfo.tag, 'Back', self._doJoinRoomSuccess)
                    else:
                        gamelog.debug('jinjj doPopCC2', roominfo.cid)
                        cc.joinRoom(str(roominfo.cid), '', self._doJoinRoomSuccess)
        gameglobal.rds.ui.cCControl.refreshPanel()

    def doInviteTeam(self):
        p = BigWorld.player()
        if p.isTeamLeader():
            self.doCreateTeamRoom()
        else:
            self.doJoinTeamChannel()

    def doEnterInGuildRoom(self):
        pass

    def onPlayerAcceptCC(self, playerName, roomId):
        self.showGameMsg(GMDD.data.CC_RESPONSE_PLAYER_ACCEPT, (playerName,))

    def onPlayerRejectCC(self, playerName, roomId):
        self.showGameMsg(GMDD.data.CC_RESPONSE_PLAYER_REJECT, (playerName,))

    def onPlayerExistCC(self, playerName, roomId):
        self.showGameMsg(GMDD.data.CC_RESPONSE_PLAYER_EXIST, (playerName,))

    def getCurrentTag(self):
        return self.currentJoinTag

    def doChangeTeamInCC(self, old, new):
        if hasattr(self, 'currentJoinTag'):
            if cc.getTeamTagById(old) == self.currentJoinTag:
                cc.joinTeamRoom('TEAM', self._doJoinTeamRoomSuccess)

    def inviteOtherToCC(self, name):
        lastRoomInfo = self.getLastRoomInfo()
        p = BigWorld.player()
        sysRoomId = str(SCD.data.get('cc_public_channel', const.CC_PUBLIC_CHANNEL))
        if lastRoomInfo:
            if lastRoomInfo.tag != None:
                p.cell.doOtherCCInvite([name], lastRoomInfo.tag, 0, '')
            elif lastRoomInfo.cid != None:
                if lastRoomInfo.cid != sysRoomId:
                    p.cell.doOtherCCInvite([name], lastRoomInfo.cid, 1, '')
                else:
                    p.cell.doOtherCCInvite([name], lastRoomInfo.cid, 2, '')
        else:
            self.doCreateRoom([name])

    def tryLoginCCBox(self):
        if self == BigWorld.player():
            self.base.tryLoginCCBox()

    def returnCCBoxInfo(self, rc, content):
        if rc == 0:
            extra = {}
            extra['role_id'] = str(self.gbId)
            extra['client_type'] = const.CCBOX_CLIENT_TYPE
            extra['client_key'] = const.CCBOX_KEY
            ccControl.initCCBoxInfo(content, extra)
            if self.groupNUID > 0:
                ccControl.joinTeam(str(self.groupNUID))
            if self.bfSideNUID:
                ccControl.joinTeam(str(self.bfSideNUID), const.CC_GROUP_TYPE_ZHANCHANG)
            ccControl.enableQuitConfirm(not AppSettings.get(keys.SET_CC_QUIT_CONFIRM, 0))
            ccControl.expandMaintool(not AppSettings.get(keys.SET_CC_MINI_SHOW, 0))
        else:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_IMPCC_424)
            ccControl.closeCC()

    def returnCCToken(self, rc, content):
        if rc == 0:
            gameglobal.rds.ccToken = content.split(' ')[1]
        else:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_ACCOUNT_644)
