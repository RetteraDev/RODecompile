#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/barrageProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import random
import formula
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import qiren_barrage_data as QBD
from data import qiren_barrage_chat_data as QBCD
from data import qiren_barrage_group_data as QBGD

class BarrageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BarrageProxy, self).__init__(uiAdapter)
        self.modelMap = {'getConfig': self.onGetConfig}
        self.mediator = None
        self.checkCallBack = None
        self.testCallBack = None

    def clearWidget(self):
        if self.checkCallBack:
            BigWorld.cancelCallback(self.checkCallBack)
            self.checkCallBack = None
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BARRAGE)

    def onGetConfig(self, *args):
        configData = SCD.data.get('bulletConfig', {'maxLine': 10,
         'normalTime': 8,
         'rocketTime': 0.5,
         'speedStepNum': 0.5,
         'speedSteps': 4,
         'rocketPer': 20,
         'centerPer': 20,
         'centerTime': 10})
        return uiUtils.dict2GfxDict(configData, True)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BARRAGE)

    def closeBullet(self):
        if self.mediator:
            self.mediator.Invoke('closeBullet', ())

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BARRAGE:
            self.mediator = mediator
            self.checkCallBack = BigWorld.callback(2, self.onTimer)

    def onTimer(self):
        if not self.mediator:
            self.checkCallBack = None
            return
        else:
            self.mediator.Invoke('checkArray', ())
            self.checkCallBack = BigWorld.callback(2, self.onTimer)
            return

    def addBarrageMsg(self, msg, isMy, type = 'chat'):
        if not gameglobal.rds.configData.get('enableBarrage', False):
            return
        if not gameglobal.rds.ui.chat.openBarrage:
            return
        if self.mediator:
            info = {}
            info['msg'] = msg
            info['isMy'] = isMy
            info['type'] = type
            self.mediator.Invoke('addBullet', uiUtils.dict2GfxDict(info, True))
            if isMy:
                self.startQiRenBarrage()

    def startQiRenBarrage(self):
        p = BigWorld.player()
        mapId = formula.getMapId(p.spaceNo)
        if mapId not in QBCD.data.keys():
            return
        randomNum = SCD.data.get('qirenChatBarrageRandomNum', (4, 5, 6))
        randomNum = random.choice(randomNum)
        idList = QBCD.data.get(mapId, {}).get('idList', ())
        randomNum = min(randomNum, len(idList))
        idList = random.sample(idList, randomNum)
        for cid in idList:
            msg = QBD.data.get(cid, {}).get('msg', '')
            if msg != '':
                self.addBarrageMsg(msg, False)

    def startQiRenBarrageByGroupId(self, groupId):
        randomNum = SCD.data.get('qirenChatBarrageRandomNum', (4, 5, 6))
        randomNum = random.choice(randomNum)
        idList = QBGD.data.get(groupId, {}).get('idList', ())
        if not idList:
            return
        randomNum = min(randomNum, len(idList))
        idList = random.sample(idList, randomNum)
        for cid in idList:
            msg = QBD.data.get(cid, {}).get('msg', '')
            if msg != '':
                self.addBarrageMsg(msg, False)
