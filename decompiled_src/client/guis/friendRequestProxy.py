#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/friendRequestProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import const
import gametypes
from gamestrings import gameStrings
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import nf_npc_data as NND

class FriendRequestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FriendRequestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRequestList': self.onGetRequestList,
         'clearRequest': self.onClearRequest,
         'discardRequest': self.onDiscardRequest,
         'viewProfile': self.onViewProfile,
         'acceptRequest': self.onAcceptRequest}
        self.data = []
        self.dataForDel = []
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FREIND_REQUEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FREIND_REQUEST:
            self.mediator = mediator

    def reset(self):
        self.dataForDel = []

    def show(self):
        p = BigWorld.player()
        npcList = [ npcPId for npcPId in p.npcFavor.npcRequest if not p.friend.has_key(npcPId) ]
        if self.data or npcList:
            if not self.mediator:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FREIND_REQUEST)
                p = BigWorld.player()
                if p.friend:
                    p._checkBlink()
            else:
                self.mediator.Invoke('refreshData')

    def onGetRequestList(self, *args):
        return self.getGfxData()

    def getFriendRequestNum(self):
        p = BigWorld.player()
        if not p.friend:
            return 0
        tempMsgs = p.friend.tempMsgs
        gbIdSet = set()
        for gbId, type, msg, idx in p.friend.tempMsgs:
            if p.friend.isFriendAddMsg(type):
                gbIdSet.add(gbId)

        if self.data:
            delList = []
            for gbId, type, msg, idx in self.data:
                if p.friend and p.friend.isFriend(gbId):
                    delList.append(gbId)
                    continue
                gbIdSet.add(gbId)

            for gbId in delList:
                self.pop(gbId)

        return len(gbIdSet)

    def checkNewFriendRequest(self):
        p = BigWorld.player()
        if not p.friend:
            return False
        newRequest = []
        for item in p.friend.tempMsgs:
            if p.friend.isFriendAddMsg(item[1]):
                newRequest.append(item)

        if len(newRequest) == 0 and not self.data:
            return False
        for item in newRequest:
            gbId, type, msg, idx = item
            p.friend.tempMsgs.remove(item)
            for i, (_idx, _gbId, _) in enumerate(p.friend.tempMsgOther):
                if _idx == idx:
                    p.friend.tempMsgOther.pop(i)
                    break

            for i, (_gbId, _type, _msg, _idx) in enumerate(self.data):
                if _gbId == gbId and _type == type:
                    self.data[i] = (_gbId,
                     _type,
                     msg,
                     _idx)
                    break
            else:
                self.data.append(item)

        delList = []
        for _gbId, _type, _msg, _idx in self.data:
            if p.friend and p.friend.isFriend(_gbId):
                delList.append(_gbId)

        for _gbId in delList:
            self.pop(_gbId)

        if not self.data:
            return False
        return True

    def getGfxData(self):
        ret = []
        if self.data:
            p = BigWorld.player()
            for _gbId, _type, _msg, _idx in self.data:
                school = _msg.get('school', const.SCHOOL_DEFAULT)
                name = uiUtils.toHtml(_msg['roleName'], '#FFBF3F')
                serverName = _msg.get('serverName', '')
                schoolTxt = const.SCHOOL_DICT.get(school, gameStrings.TEXT_GAME_1747)
                srcId = _msg.get('srcId', 0)
                descTxt = gameStrings.TEXT_FRIENDREQUESTPROXY_129 % name
                sourceTxt = uiUtils.getFriendSrcDesc(srcId)
                if serverName:
                    descTxt = gameStrings.TEXT_FRIENDREQUESTPROXY_132 % (serverName, descTxt)
                    sourceTxt = gameStrings.TEXT_BATTLEFIELDPROXY_256
                sourceTxt = gameStrings.TEXT_FRIENDREQUESTPROXY_134 + sourceTxt
                isFriend = False
                if p.friend and p.friend.isFriend(_gbId):
                    isFriend = True
                ret.append({'desc': descTxt,
                 'school': schoolTxt,
                 'source': sourceTxt,
                 'gbId': _gbId,
                 'source': sourceTxt,
                 'isFriend': isFriend})

        p = BigWorld.player()
        for npcPId in p.npcFavor.npcRequest:
            if p.friend.has_key(npcPId):
                continue
            cfgData = NND.data.get(npcPId, {})
            descTxt = gameStrings.NPC_FRIEND_REQUEST % uiUtils.toHtml(cfgData.get('name', ''), '#FFBF3F')
            schoolTxt = ''
            sourceTxt = gameStrings.NPC_FRIEND_SOURCE
            ret.append({'desc': descTxt,
             'school': schoolTxt,
             'source': sourceTxt,
             'gbId': -npcPId,
             'source': sourceTxt,
             'isFriend': False})

        return uiUtils.array2GfxAarry(ret, True)

    def onClearRequest(self, *args):
        if self.data:
            p = BigWorld.player()
            for _gbId, _type, _msg, _idx in self.data:
                if _type == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
                    p.base.rmOfflineFriendInvite(_gbId)
                elif _type == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
                    hostId = _msg.get('hostId', 0)
                    p.base.denyRemoteAddFriendRequest(hostId, _gbId)

        self.data = []
        self.hide()
        gameglobal.rds.ui.recommendSearchFriend.updatefriendRequentListBtn()

    def onDiscardRequest(self, *args):
        self.hide()

    def pop(self, gbId):
        for i, (_gbId, _type, _msg, _idx) in enumerate(self.data):
            if _gbId == gbId:
                return self.data.pop(i)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FREIND_REQUEST)

    def onViewProfile(self, *arg):
        gbId = int(arg[3][0].GetString())
        p = BigWorld.player()
        for _gbId, _type, _msg, _idx in self.data + self.dataForDel:
            if gbId == _gbId:
                if _type == gametypes.FRIEND_MSG_TYPE_GLOBAL_SERVER_ADD:
                    p.showGameMsg(GMDD.data.GLOBAL_FRIEND_FORBID_PROFILE, ())
                else:
                    p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_FRIEND)
                    srcId = _msg.get('srcId', 0)
                    if srcId == const.FRIEND_SRC_RECOMMEND_FRIEND:
                        p.getPersonalSysProxy().friendSrcId = const.FRIEND_SRC_RECOMMEND_FRIEND_ACK
            break

    def onAcceptRequest(self, *arg):
        gbId = int(arg[3][0].GetString())
        if gbId < 0:
            BigWorld.player().base.addContactNF(-gbId)
            return
        info = self.pop(gbId)
        if info:
            self.dataForDel.append(info)
            _gbId, _type, _msg, _idx = info
            p = BigWorld.player()
            if _type == gametypes.FRIEND_MSG_TYPE_GLOBAL_SERVER_ADD:
                hostId = _msg.get('hostId', 0)
                p.base.acceptRemoteAddFriendRequest(hostId, gbId)
            else:
                srcId = _msg.get('srcId', 0)
                if srcId == const.FRIEND_SRC_RECOMMEND_FRIEND:
                    srcId = const.FRIEND_SRC_RECOMMEND_FRIEND_ACK
                else:
                    srcId = 0
                p.base.addContactByGbId(gbId, gametypes.FRIEND_GROUP_FRIEND, srcId)
                if _type == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
                    p.base.rmOfflineFriendInvite(gbId)
        gameglobal.rds.ui.recommendSearchFriend.updatefriendRequentListBtn()
