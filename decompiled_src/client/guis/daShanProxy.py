#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/daShanProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from data import school_data as SD
from data import personal_zone_touch_data as PZTD

class DaShanProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DaShanProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDaShanList': self.onGetDaShanList,
         'clearDaShan': self.onClearDaShan,
         'chatToFriend': self.onChatToFriend,
         'addFriend': self.onAddFriend,
         'discardDaShan': self.onDiscardDaShan}
        self.data = []
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DASHAN, self.hide)
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DASHAN, {'click': self.show})

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DASHAN:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DASHAN)
        gameglobal.rds.ui.systemButton.showFriendShine(False)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DASHAN)

    def refreshDaShan(self):
        if self.mediator != None:
            ar = uiUtils.array2GfxAarry(self.data)
            self.mediator.Invoke('refresh', ar)

    def onGetDaShanList(self, *args):
        for item in self.data:
            item['time'] = uiUtils.formatTimeShort(utils.getNow() - item['eWhen']) + gameStrings.TEXT_DASHANPROXY_46
            item['isFriend'] = BigWorld.player().friend.isFriend(item['srcGbId'])
            item['gbId'] = str(item['srcGbId'])
            item['desc'] = PZTD.data.get(item['msgType'], {}).get('cdesc', '')

        self.data.sort(key=lambda k: k['eWhen'], reverse=True)
        ar = uiUtils.array2GfxAarry(self.data, True)
        return ar

    def onClearDaShan(self, *args):
        self.data = []
        self.hide()
        BigWorld.player().base.removeAllAppMsg()
        gameglobal.rds.uiLog.addClickLog(uiConst.MESSAGE_TYPE_DASHAN * 100 + 3)

    def checkShine(self):
        if len(self.data) == 0:
            gameglobal.rds.ui.systemButton.showFriendShine(False)

    def onChatToFriend(self, *args):
        gbId = int(args[3][0].GetString())
        dbId = int(args[3][1].GetNumber())
        gameglobal.rds.ui.friend.beginChat(gbId)
        self.removeFromData(dbId)
        BigWorld.player().base.removeAppMsgByDbId(dbId, gametypes.APP_MSG_OP_TALK)
        gameglobal.rds.uiLog.addClickLog(uiConst.MESSAGE_TYPE_DASHAN * 100 + 2)

    def onAddFriend(self, *args):
        gbId = int(args[3][0].GetString())
        dbId = int(args[3][1].GetNumber())
        hostId = int(args[3][2].GetNumber())
        self.removeFromData(dbId)
        BigWorld.player().base.addFriendOfApp(dbId, hostId, gbId)
        gameglobal.rds.uiLog.addClickLog(uiConst.MESSAGE_TYPE_DASHAN * 100 + 1)

    def onDiscardDaShan(self, *args):
        self.hide()
        gameglobal.rds.uiLog.addClickLog(uiConst.MESSAGE_TYPE_DASHAN * 100 + 4)

    def removeFromData(self, dbId):
        for item in self.data:
            if item['dbId'] == dbId:
                self.data.remove(item)

    def getItemDataByInfo(self, info):
        info['school'] = SD.data.get(info['srcSchool'], {}).get('name')
        info['serverName'] = utils.getServerName(info['srcServerId'])
        info['time'] = uiUtils.formatTimeShort(utils.getNow() - info['eWhen']) + gameStrings.TEXT_DASHANPROXY_46
        return info

    def setDaShanList(self, info):
        data = []
        for key, item in info.items():
            newItem = self.getItemDataByInfo(item)
            newItem['dbId'] = key
            data.append(newItem)

        self.data = data
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DASHAN, {'data': []})
        gameglobal.rds.ui.systemButton.showFriendShine(True)

    def addDaShanList(self, info):
        self.data.append(self.getItemDataByInfo(info))
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DASHAN, {'data': []})
        gameglobal.rds.ui.systemButton.showFriendShine(True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DASHAN)
