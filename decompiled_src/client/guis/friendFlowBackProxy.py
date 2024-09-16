#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/friendFlowBackProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import gameglobal
from guis import uiUtils
from uiProxy import UIProxy

class FriendFlowBackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FriendFlowBackProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData,
         'send': self.onSendBonus}
        uiAdapter.registerEscFunc(uiConst.WIDGET_FRIEND_FLOW_BACK, self.hide)
        self.mediator = None
        self.friendList = []

    def show(self):
        if not self.mediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FRIEND_FLOW_BACK)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        if self.mediator:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_FRIEND_FLOW_BACK)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FRIEND_FLOW_BACK:
            self.mediator = mediator

    def onGetInitData(self, *args):
        flowBackList = []
        gameglobal.rds.ui.systemButton.showFriendShine(False)
        gameglobal.rds.ui.systemButton.setFriendFlowBack(0)
        for item in self.friendList:
            oneFlowBack = {}
            oneFlowBack['content'] = gameStrings.TEXT_FRIENDFLOWBACKPROXY_43 % (self.getDaysFromStamp(item[0]), item[2])
            oneFlowBack['date'] = self.formatDate(uiUtils._getTodayDate())
            oneFlowBack['gbId'] = item[1]
            flowBackList.append(oneFlowBack)

        return uiUtils.array2GfxAarry(flowBackList, True)

    def getNameFromgbId(self, gbId):
        if gbId and gbId != 1:
            for val in BigWorld.player().friend.values():
                if val.gbId == gbId:
                    return val.name

        return ''

    def getDaysFromStamp(self, stamp):
        date = str(stamp / 86400)
        return date

    def setFlowBackData(self, lastStamp, gbId):
        if not gameglobal.rds.configData.get('enableFriendFlowBack', False):
            return
        if self.hasGbId(gbId):
            gameglobal.rds.ui.systemButton.showFriendShine(True)
            gameglobal.rds.ui.systemButton.setFriendFlowBack(1)
            return
        self.friendList.append((lastStamp, gbId, self.getNameFromgbId(gbId)))
        self.friendList.sort(key=lambda k: k[0], reverse=True)
        if self.mediator:
            flowBackList = []
            for item in self.friendList:
                oneFlowBack = {}
                oneFlowBack['content'] = gameStrings.TEXT_FRIENDFLOWBACKPROXY_43 % (self.getDaysFromStamp(item[0]), item[2])
                oneFlowBack['date'] = self.formatDate(uiUtils._getTodayDate())
                oneFlowBack['gbId'] = item[1]
                flowBackList.append(oneFlowBack)

            self.mediator.Invoke('addFlowBackList', uiUtils.array2GfxAarry(flowBackList, True))
        else:
            gameglobal.rds.ui.systemButton.showFriendShine(True)
            gameglobal.rds.ui.systemButton.setFriendFlowBack(1)

    def hasGbId(self, gbId):
        for item in self.friendList:
            if item[1] == gbId:
                return True

        return False

    def formatDate(self, dateNum):
        dateNum = int(dateNum)
        dateStr = str(dateNum / 10000) + '.' + str(dateNum % 10000 / 100) + '.' + str(dateNum % 100)
        return dateStr

    def onSendBonus(self, *args):
        gbId = int(args[3][0].GetString())
        BigWorld.player().base.sendGiftToFlowbackFriend(gbId, self.getNameFromgbId(gbId))
        self.removeBygbId(gbId)

    def removeBygbId(self, gbId):
        for item in self.friendList:
            if item[1] == gbId:
                self.friendList.remove(item)
                if self.mediator != None:
                    self.mediator.Invoke('removeItem', ())
                break

        if len(self.friendList) == 0:
            self.hide()

    def clearData(self):
        self.friendList = []
