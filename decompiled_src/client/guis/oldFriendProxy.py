#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/oldFriendProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from ui import unicode2gbk
from uiProxy import UIProxy
from guis import uiUtils
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import school_data as SD

class OldFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(OldFriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitInfo': self.onGetInitInfo,
         'getOldRoleNames': self.onGetOldRoleNames,
         'getOldFriendInfo': self.onGetOldFriendInfo,
         'addFriend': self.onAddFriend,
         'closePanel': self.onClosePanel}
        self.mediator = None
        self.npcId = None
        self.oldPlayerNames = None
        self.oldFriendActive = False
        self.playerName = None
        self.data = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_OLD_FRIEND, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_OLD_FRIEND:
            self.mediator = mediator

    def show(self, npcId, oldPlayerNames, oldFriendActive, data):
        self.npcId = npcId
        self.oldPlayerNames = oldPlayerNames
        self.oldFriendActive = oldFriendActive
        self.data = data
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_OLD_FRIEND)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_OLD_FRIEND)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.npcId = None
        self.oldPlayerNames = None
        self.oldFriendActive = False
        self.playerName = None
        self.data = None

    def _confirmInActivate(self, npc):
        if not npc:
            return
        npc.cell.inactivateOldFriend()

    def confirmInActivate(self, npc):
        if not npc:
            return
        msg = GMD.data.get(GMDD.data.CONFIRM_INACTIVATE_OLD_FRIEND, {}).get('text', gameStrings.TEXT_OLDFRIENDPROXY_70)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._confirmInActivate, npc))

    def createOldFriendInfo(self):
        for data in self.data:
            data[2] = SD.data.get(data[2], {}).get('name', gameStrings.TEXT_GAME_1747)

        ret = {'data': self.data}
        return uiUtils.dict2GfxDict(ret, True)

    def setOldFriendInfo(self, oldPlayerName, data):
        self.data = data
        ret = self.createOldFriendInfo()
        if self.mediator:
            self.mediator.Invoke('setOldFriendInfo', ret)

    def getOldFriendInfo(self):
        BigWorld.player().cell.getOldFriendList(self.playerName)

    def refreshOldFriendInfo(self, gbId):
        if self.mediator:
            for data in self.data:
                if data[0] == gbId:
                    data[5] = True
                    break

            ret = self.createOldFriendInfo()
            self.mediator.Invoke('setOldFriendInfo', ret)

    def onGetInitInfo(self, *arg):
        return self.createOldFriendInfo()

    def onGetOldRoleNames(self, *arg):
        ret = []
        for name in self.oldPlayerNames:
            ret.append({'label': name})

        return uiUtils.array2GfxAarry(ret, True)

    def onGetOldFriendInfo(self, *arg):
        self.playerName = unicode2gbk(arg[3][0].GetString())
        self.getOldFriendInfo()

    def onAddFriend(self, *arg):
        gbIds = arg[3][0].GetString().split(',')
        p = BigWorld.player()
        for gbId in gbIds:
            gbId = int(gbId)
            if p.friend.isEnemy(gbId):
                p.base.deleteEnemy(gbId, True)
            else:
                p.base.addContactByGbId(gbId, gametypes.FRIEND_GROUP_FRIEND, 0)

    def onClosePanel(self, *arg):
        self.hide()
