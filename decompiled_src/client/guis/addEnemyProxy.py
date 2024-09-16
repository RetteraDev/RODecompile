#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/addEnemyProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class AddEnemyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AddEnemyProxy, self).__init__(uiAdapter)
        self.modelMap = {'getEnemyInfo': self.onGetEnemyInfo,
         'ignoreAll': self.onIgnoreAll,
         'closePanel': self.onClosePanel,
         'addEnemy': self.onAddEnemy}
        self.mediator = None
        self.enemyInfo = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ADD_ENEMY:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ADD_ENEMY)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ADD_ENEMY)
        self.mediator = None

    def reset(self):
        self.enemyInfo = None

    def _getRemainTime(self, val):
        return int(60 - (BigWorld.player().getServerTime() - val))

    def pushEnemyMessage(self, gbId, roleName, lv):
        startTime = BigWorld.player().getServerTime()
        self.enemyInfo = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ADD_ENEMY)
        if self._getEnemyData(gbId):
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ADD_ENEMY, {'startTime': startTime,
         'totalTime': const.TIME_INTERVAL_DAY,
         'data': [gbk2unicode(roleName),
                  str(lv),
                  60,
                  str(gbId)]})

    def _getEnemyData(self, gbId):
        for item in self.enemyInfo:
            if long(item['data'][3]) == gbId:
                return item

    def refresh(self):
        self.enemyInfo = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ADD_ENEMY)
        data = [len(self.enemyInfo), []]
        for item in self.enemyInfo:
            item['data'][2] = self._getRemainTime(item['startTime'])
            data[1].append(item['data'])

        if len(self.enemyInfo) > 0:
            if self.mediator != None:
                self.mediator.Invoke('setEnemyInfo', uiUtils.array2GfxAarry(data))
        else:
            self.hide()

    def onGetEnemyInfo(self, *arg):
        self.enemyInfo = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ADD_ENEMY)
        data = [len(self.enemyInfo), []]
        for item in self.enemyInfo:
            item['data'][2] = self._getRemainTime(item['startTime'])
            data[1].append(item['data'])

        ar = uiUtils.array2GfxAarry(data)
        return ar

    def onIgnoreAll(self, *arg):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ADD_ENEMY)
        self.clearWidget()

    def onClosePanel(self, *arg):
        self.clearWidget()

    def onAddEnemy(self, *arg):
        gbId = long(arg[3][0].GetString())
        p = BigWorld.player()
        if p.friend.isFriend(gbId):
            fVal = p.friend.get(gbId)
            msg = uiUtils.getTextFromGMD(GMDD.data.ADD_FRIEND_TO_ENEMY, gameStrings.TEXT_ADDENEMYPROXY_95) % fVal.name
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onAddEnemyAccept, gbId))
        else:
            self.onAddEnemyAccept(gbId)

    def onAddEnemyAccept(self, gbId):
        p = BigWorld.player()
        p.base.addContactByGbId(gbId, gametypes.FRIEND_GROUP_ENEMY, 0)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_ADD_ENEMY, self._getEnemyData(gbId))
        self.clearWidget()
