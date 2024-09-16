#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/cc.o
import os
import BigWorld
import formula
import gameglobal
import gametypes
import clientUtils
import gamelog
import const
import uuid
import utils
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
TYPE_NORMAL = 1
TYPE_TEMP = 2
status_close = 0
status_logging = 1
status_logined = 2

class iCC(object):

    def __init__(self):
        self.ccObj = BigWorld.PyCC()
        self.ccObj.script = self
        self.context = 0
        self.channel_id = None
        self.room_name = ''
        self.room_pwd = ''
        self.onlogin_cb = None
        self.create_channel_cb = None
        self.on_join_room_cb = None
        self.login_status = 0
        self.login_state_context = 0
        self.b_weibologin = False

    def setJoinRoomCb(self, cb):
        self.on_join_room_cb = cb

    def isStartCC(self):
        return self.ccObj.getIsStart()

    def setRoomInfo(self, name, pswd, callback, ch_callback = None):
        self.room_name = name
        self.room_pwd = pswd
        gamelog.debug('jinjj---setRoomInfo', self.room_pwd)
        self.onlogin_cb = callback
        self.create_channel_cb = ch_callback

    def setRoomTagInfo(self, functor):
        self.onlogin_cb = functor

    def preStart(self):
        return self.ccObj.prestart()

    def resetCc(self):
        self.ccObj.resetcc()

    def start(self, silent = 0):
        if not hasattr(gameglobal.rds, 'loginUserName'):
            luser = ''
        else:
            luser = gameglobal.rds.loginUserName
        gamelog.debug('jinjj-----cc start')
        self.ccObj.start(luser, silent)
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.CC_OPENING, ())

    def checkUpdate(self):
        if hasattr(self.ccObj, 'checkUpdate'):
            return self.ccObj.checkUpdate()
        return 0

    def isCCUpdating(self):
        if hasattr(self.ccObj, 'isCCUpdating'):
            return self.ccObj.isCCUpdating()
        return 0

    def getIsStart(self):
        return self.ccObj.getIsStart()

    def createTc(self):
        self.ccObj.createChannel(0, self.room_name, self.room_pwd, TYPE_TEMP)

    def openCcMall(self):
        self.ccObj.control(2)

    def getORooms(self):
        self.ccObj.getOwnRoom()

    def showRoomForm(self, bShow):
        self.ccObj.showRoom(bShow)

    def joinRoomTag(self, context, room_tag):
        self.ccObj.joinChannelByTag(context, str(room_tag))

    def joinTC(self):
        self.ccObj.joinChannel(0, self.room_name, self.room_pwd)

    def createNC(self):
        self.ccObj.createChannel(0, const.CC_NORMAL_TEST, '', TYPE_NORMAL)

    def joinChannel(self, channel_id, pwd = ''):
        self.ccObj.joinChannel(0, channel_id, pwd)

    def closeChannel(self):
        channel_id = self.ccObj.getChannelID()
        if channel_id != '0':
            self.ccObj.closeChannel(channel_id)

    def setNotloginCallback(self, callback):
        self.notlogin_callback = callback

    def setLoginCallback(self, callback):
        self.login_callback = callback

    def getLoginState(self):
        p = BigWorld.player()
        self.login_state_context += 1
        uid = str(uuid.UUID(bytes=p.playerUUID))
        return self.ccObj.getLoginStatus(self.login_state_context, gameglobal.rds.loginUserName, uid)

    def getChannelId(self):
        return self.ccObj.getChannelID()

    def close(self):
        self.ccObj.close()
        self.channel_id = None
        self.b_weibologin = False
        BigWorld.player().doClear()
        gameglobal.rds.ui.topBar.setCCStatus(0)

    def OnStartCC(self):
        gamelog.debug('jinjj-----cc OnStartCC')
        self.doLogin()
        gameglobal.rds.ui.cCControl.refreshPanel()

    def weiboLogin(self):
        p = BigWorld.player()
        uid = str(uuid.UUID(bytes=p.playerUUID))
        self.ccObj.weibologin(uid)

    def OnWeiboLogin(self, res):
        p = BigWorld.player()
        if res == 0:
            self.b_weibologin = True
        elif res == -1:
            p.showGameMsg(GMDD.data.CC_WEIBO_SEND_FAILED, ())
        elif res == -2:
            p.showGameMsg(GMDD.data.CC_WEIBO_UPDATE_WAIT, ())

    def doLogin(self):
        p = BigWorld.player()
        if p:
            uid = str(uuid.UUID(bytes=p.playerUUID))
            userName = gameglobal.rds.loginUserName
            passWord = gameglobal.rds.loginUserPassword
            if not passWord and hasattr(gameglobal.rds, 'ccToken'):
                userName = gameglobal.rds.ccToken + '@token#'
            if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                roleName = '排队中'
                schoolName = '未知'
                lv = 0
            else:
                roleName = p.realRoleName
                schoolName = formula.whatSchoolName(p.physique.school)
                lv = p.lv
            gamelog.debug('jinjj~~~~cc doLogin~', userName, uid, passWord, roleName, schoolName, lv)
            try:
                self.ccObj.login(userName, uid, passWord, roleName, schoolName, lv)
            except:
                clientUtils.reportEngineException('%s %s %s %s %s %d' % (userName,
                 uid,
                 passWord,
                 roleName,
                 schoolName,
                 lv))

            p.showGameMsg(GMDD.data.CC_LOGINING_WAITING, ())

    def clearCallback(self):
        try:
            self.onlogin_cb = None
            self.create_channel_cb = None
            self.on_join_room_cb = None
            if hasattr(self, 'login_callback'):
                del self.login_callback
            if hasattr(self, 'notlogin_callback'):
                del self.notlogin_callback
        except:
            pass

    def OnGetLoginStatus(self, context, status):
        if self.login_state_context != context:
            return
        self.login_status = status
        if status == status_logined:
            if hasattr(self, 'login_callback') and self.login_callback:
                self.login_callback()
        elif status == status_close:
            if hasattr(self, 'notlogin_callback') and self.notlogin_callback:
                self.notlogin_callback()

    def OnLoginCC(self, ok):
        gamelog.debug('jinjj ---OnLoginCC~~~~~~~~~', self.onlogin_cb)
        p = BigWorld.player()
        if not ok:
            if self.onlogin_cb:
                self.onlogin_cb()
            p.showGameMsg(GMDD.data.CC_LOGINING_SUCCESS, ())
        else:
            reason = {0: 'cc成功',
             1: '登录cc网关失败',
             2: 'cc账号被踢',
             3: 'cc本地网络连接中断',
             4: 'cc密码错误',
             5: 'cc帐号错误',
             6: 'cc本地初始化失败',
             7: 'cc短时间登录频繁urs禁止登录',
             8: 'cc黑名单不允许登录',
             9: 'cc游戏昵称设置出错',
             10: 'cc维护中'}
            if reason.get(ok) != None:
                gameglobal.rds.ui.messageBox.showMsgBox(reason[ok])
            else:
                gameglobal.rds.ui.messageBox.showMsgBox('意外的错误,错误代码:%d' % ok)
        gameglobal.rds.ui.cCControl.refreshPanel()
        if ok == 0:
            gameglobal.rds.ui.topBar.setCCStatus(1)

    def showWeibo(self, show):
        self.ccObj.weiboshow(show)

    def getWeibologin(self):
        return self.b_weibologin

    def closeWeibo(self):
        pass

    def OnWeiboShow(self, show):
        pass

    def OnWeiboRelationCreate(self, res):
        pass

    def ccStartError(self, rt_val):
        if rt_val < 0:
            gameglobal.rds.ui.messageBox.showMsgBox(const.CC_START_FAILED)
            self.close()
        elif rt_val == 0:
            self.clearCallback()
            self.setNotloginCallback(self.doLogin)

    def OnCreateCCChannel(self, context, strCid):
        self.channel_id = strCid
        if self.create_channel_cb:
            self.create_channel_cb(strCid)

    def OnJoinCCChannel(self, context, nRes):
        reson = {0: '成功',
         1: '房间号不存在',
         2: '密码错误',
         3: '房间黑名单不允许进入',
         4: '人数达到上限无法进入',
         5: '不在当前队伍中,不能进入',
         6: '已请求加入该房间,请耐心等待'}
        if nRes != 0:
            gamelog.debug('jinjj----------OnJoinCCChannel', self.room_pwd)
            if nRes != 2 or self.room_pwd != '':
                gameglobal.rds.ui.messageBox.showMsgBox(reson.get(nRes, '意外的错误'))
            else:
                gameglobal.rds.ui.inventoryPassword.show(0, 0, 0, True)
        else:
            self.channel_id = self.getChannelId()
            if self.on_join_room_cb:
                self.on_join_room_cb(context)
        gameglobal.rds.ui.cCControl.refreshPanel()
        if nRes == 0:
            gameglobal.rds.ui.topBar.setCCStatus(2)

    def OnCloseCCChannel(self, ctx, nRes):
        gamelog.debug('jinjj---OnCloseCCChannel')
        BigWorld.player().doPopCC(self.channel_id)
        self.channel_id = None
        self.b_weibologin = False
        gameglobal.rds.ui.topBar.setCCStatus(1)

    def OnCloseCC(self, nRes):
        gamelog.debug('jinjj---OnCloseCC')
        self.channel_id = None
        self.b_weibologin = False
        BigWorld.player().doClear()
        gameglobal.rds.ui.topBar.setCCStatus(0)

    def OnSetTempRoomOwner(self, context, nRes):
        pass

    def OnGetOwnRoomBySelf(self, rlist):
        pass

    def OnCheckRoomId(self, rsid, isexist):
        pass

    def OnGetGameUserList(self, ulist):
        pass

    def OnRoomMemberChange(self, reason, name):
        try:
            b = name.decode('utf8')
            a = b.encode(utils.defaultEncoding(), 'ignore')
            p = BigWorld.player()
            if reason == 1:
                p.showGameMsg(GMDD.data.CC_ENTER_ROOM, a)
            elif reason == 2:
                p.showGameMsg(GMDD.data.CC_LEAVE_ROOM, a)
        except:
            pass

    def checkCCInstall(self):
        if hasattr(self.ccObj, 'checkCCInstall'):
            if self.ccObj.checkCCInstall() == 0:
                return True
            return os.path.exists('.\\cc\\start.exe')
        else:
            return True


obj = iCC()

def launchCC():
    global obj
    obj.clearCallback()
    startCC()


def openCcMall():
    is_cc_started = obj.getIsStart()
    p = BigWorld.player()
    if is_cc_started < 1:
        p.showGameMsg(GMDD.data.CC_OPENCC_PLEASE, ())
    elif is_cc_started == 1:
        p.showGameMsg(GMDD.data.CC_OPENING, ())
    else:
        obj.openCcMall()


def startCC(silent = 0):
    p = BigWorld.player()
    if isCCUpdating():
        p.showGameMsg(GMDD.data.COMMON_MSG, ('cc\xd5\xfd\xd4\xda\xb8\xfc\xd0\xc2\xd6\xd0\xa3\xac\xc7\xeb\xc9\xd4\xba\xf3\xd4\xd9\xca\xd4',))
        return False
    else:
        is_cc_started = obj.getIsStart()
        if is_cc_started in (0, -1, 2):
            if not gameglobal.rds.loginUserPassword:
                BigWorld.player().base.createCCToken()
        if is_cc_started in (0, -1):
            obj.start(silent)
            return False
        if is_cc_started == 2:
            st = obj.getLoginState()
            if st == status_close:
                obj.doLogin()
                return False
            return True
        if is_cc_started == 1:
            p.showGameMsg(GMDD.data.CC_OPENING, ())
            return False
        p.showGameMsg(GMDD.data.CC_OPENING_FAILED, ())
        return False


def checkUpdate():
    ret = 0
    if obj:
        ret = obj.checkUpdate()
    return ret


def isCCUpdating():
    ret = 0
    if obj:
        ret = obj.isCCUpdating()
    return ret


def closeChannel():
    if obj:
        obj.closeChannel()


def closeCC():
    if obj:
        obj.close()


def resetCc():
    if obj:
        obj.resetCc()


def queryChannel():
    chid = obj.getChannelId()
    return chid


def closeWeibo():
    if obj:
        obj.closeWeibo()


def createRoom(rname, pswd, on_create_channel_cb = None):
    global room_tag_info
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    room_tag_info = None
    obj.clearCallback()
    obj.setRoomInfo(rname, pswd, obj.createTc, on_create_channel_cb)
    if startCC():
        obj.setLoginCallback(obj.createTc)


def joinRoom(rids, pswd, on_join_room_callback = None):
    global room_tag_info
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    room_tag_info = None
    obj.clearCallback()
    if on_join_room_callback == None:
        obj.setJoinRoomCb(None)
    else:
        obj.setJoinRoomCb(on_join_room_callback)
    obj.setRoomInfo(rids, pswd, obj.joinTC)
    if startCC():
        obj.setLoginCallback(obj.joinTC)


room_tag_info = None
room_tag_id = 10000

def getRoomTagId():
    global room_tag_id
    room_tag_id += 1
    return room_tag_id


player_tag_id = 10000

def getPlayerTagId():
    global player_tag_id
    player_tag_id += 1
    return player_tag_id


def joinPlayerRoom():
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    name_tag = getPlayerTag()
    joinRoomTag(name_tag, 'Single')


def getTeamTag():
    p = BigWorld.player()
    if p and p.groupNUID:
        return 'ty_' + str(gameglobal.rds.g_serverid) + '_t' + str(p.groupNUID)
    else:
        return None


def getTeamTagById(groupNUID):
    p = BigWorld.player()
    if p and groupNUID:
        return 'ty_' + str(gameglobal.rds.g_serverid) + '_t' + str(groupNUID)
    else:
        return None


def getPlayerTag():
    p = BigWorld.player()
    name_tag = 'ty_' + str(gameglobal.rds.g_serverid) + '_p' + str(p.id) + '_' + str(getPlayerTagId())
    return name_tag


def joinTeamRoom(tag = 'TEAM', callback = None):
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    name_tag = getTeamTag()
    if name_tag:
        if callback != None:
            gamelog.debug('jinjj--', callback)
            joinRoomTag(name_tag, tag, callback)
        else:
            joinRoomTag(name_tag, tag)
    else:
        p.showGameMsg(GMDD.data.CC_NOT_IN_TEAM, ())


def joinBattleRoom(tnuid):
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    if tnuid:
        joinRoomTag('ty_' + tnuid, 'TROOP')
    else:
        p.showGameMsg(GMDD.data.CC_NOT_IN_GROUP, ())


def joinRoomTag(room_tag, flag, on_join_room_callback = None):
    global room_tag_info
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    obj.clearCallback()
    context = getRoomTagId()
    room_tag_info = (room_tag, flag, context)
    if on_join_room_callback == None:
        obj.setJoinRoomCb(onJoinRoomOk)
    else:
        obj.setJoinRoomCb(on_join_room_callback)
    do_join_tr = Functor(obj.joinRoomTag, context, room_tag)
    obj.setRoomTagInfo(do_join_tr)
    if startCC():
        obj.setLoginCallback(do_join_tr)


def joinBlocRoom():
    p = BigWorld.player()
    if not obj.checkCCInstall():
        p.doSendNoticeInstall()
        return
    if p and p.blocNUID:
        name_tag = 'tx_' + str(gameglobal.rds.g_serverid) + '_' + str(p.blocNUID)
        joinRoomTag(name_tag, 'BLOC')
    else:
        p.showGameMsg(GMDD.data.CHAT_NOT_IN_BATTLEFIELD, ())


def onJoinRoomOk(context):
    if room_tag_info and context in room_tag_info:
        room_tag, flag, context = room_tag_info


def showRoomForm(bShow):
    obj.showRoomForm(bShow)


def testDmp():
    if obj:
        obj.closeWeibo()
        obj.resetCc()


def getCurrentCid():
    if obj:
        return obj.getChannelId()


def openCCRoomIntoFront():
    if obj:
        obj.showRoomForm(True)


def preStart():
    if obj:
        return obj.preStart()


def isStartCC():
    if obj:
        return obj.isStartCC()
