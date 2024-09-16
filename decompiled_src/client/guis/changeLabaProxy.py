#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/changeLabaProxy.o
from gamestrings import gameStrings
import copy
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import utils
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
from data import laba_config_data as LCD

class ChangeLabaProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChangeLabaProxy, self).__init__(uiAdapter)
        self.modelMap = {'getLabaInfo': self.onGetLabaInfo,
         'getLabaSize': self.onGetLabaSize,
         'getSelectLabaId': self.onGetSelectLabaId,
         'selectedPos': self.onSelectedPos,
         'getCurrentPage': self.onGetCurrentPage}
        self.mediator = None
        self.newIdList = []
        self.keyList = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHANGE_LABA, self.clearWidget)

    def clearWidget(self):
        p = BigWorld.player()
        if p and hasattr(p, 'sendOperation'):
            p.sendOperation()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHANGE_LABA)

    def show(self, newIdList = []):
        self.newIdList = newIdList
        self.checkCurLabaCanUse()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHANGE_LABA)

    def onGetCurrentPage(self, *args):
        if len(self.newIdList):
            self.newIdList.sort()
            for i in xrange(len(self.keyList)):
                if self.newIdList[0] == self.keyList[i]:
                    return GfxValue(i / 2)

            return GfxValue(0)
        else:
            return GfxValue(0)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHANGE_LABA:
            self.mediator = mediator

    def toggle(self):
        if self.mediator:
            self.clearWidget()
        else:
            self.show()

    def onGetLabaSize(self, *args):
        data = LCD.data
        self.keyList = []
        for item in data:
            if data[item]['type'] == gametypes.LABA_CROSS_SERVER or data[item]['type'] == gametypes.LABA_FIRE_WORK or data[item].get('isShow', 0) == 1 or not self.checkLabVisible(item):
                continue
            else:
                self.keyList.append(item)

        return GfxValue(len(self.keyList))

    def checkCurLabaCanUse(self):
        data = LCD.data
        p = BigWorld.player()
        curLabaId = p.operation.get('curLabaId', 0)
        if not data.get(curLabaId):
            p.operation['curLabaId'] = 0
            p.sendOperation()
            return
        labaInfo = data[curLabaId]
        labaType = labaInfo['type']
        if labaType == gametypes.LABA_ITEM_TYPE:
            endTime = BigWorld.player().chatWorldExTime.get(curLabaId, 0)
            if endTime < utils.getNow():
                p.operation['curLabaId'] = 0
                p.sendOperation()
                return
        elif labaType == gametypes.LABA_TIME_TYPE:
            configData = labaInfo.get('configData', {})
            if not configData:
                p.operation['curLabaId'] = 0
                p.sendOperation()
                return
            startCrons = configData['startTimes']
            endCrons = configData['endTimes']
            canUse = False
            for i in xrange(len(startCrons)):
                if utils.inCrontabRange(startCrons[i], endCrons[i]):
                    canUse = True
                else:
                    continue

            if canUse == False:
                p.operation['curLabaId'] = 0
                p.sendOperation()
                return

    def checkLabVisible(self, labaId):
        labaInfo = LCD.data.get(labaId, {})
        labaType = labaInfo['type']
        if labaInfo.get('isShow', 0) == 1:
            return False
        if labaType == gametypes.LABA_TIME_TYPE:
            configData = labaInfo.get('configData', {})
            if not configData:
                return False
        elif labaType == gametypes.LABA_CROSS_SERVER or labaType == gametypes.LABA_FIRE_WORK:
            return False
        return True

    def onGetLabaInfo(self, *args):
        page = int(args[3][0].GetNumber())
        info = []
        nowInfo = self.keyList[page * 2:page * 2 + 2]
        for labaId in nowInfo:
            labaInfo = copy.deepcopy(LCD.data[labaId])
            labaType = labaInfo['type']
            labaInfo['labaId'] = labaId
            if labaInfo.get('isShow', 0) == 1:
                continue
            if labaType == gametypes.LABA_ITEM_TYPE:
                endTime = BigWorld.player().chatWorldExTime.get(labaId, 0)
                if endTime > utils.getNow():
                    timeText = time.strftime('%Y.%m.%d  %H:%M', time.localtime(endTime))
                    labaInfo['desc'] = gameStrings.TEXT_BOOTHPROXY_168 % timeText
                    labaInfo['descMid'] = False
                else:
                    labaInfo['descMid'] = True
            elif labaType == gametypes.LABA_NORMAL_TYPE:
                labaInfo['descMid'] = False
            elif labaType == gametypes.LABA_TIME_TYPE:
                configData = labaInfo.get('configData', {})
                if not configData:
                    labaInfo['descMid'] = True
                    continue
                startCrons = configData['startTimes']
                endCrons = configData['endTimes']
                for i in xrange(len(startCrons)):
                    if utils.inCrontabRange(startCrons[i], endCrons[i]):
                        labaInfo['descMid'] = False
                    else:
                        continue

                if labaInfo.get('descMid') == None:
                    labaInfo['descMid'] = True
            elif labaType == gametypes.LABA_CROSS_SERVER or labaType == gametypes.LABA_FIRE_WORK:
                continue
            if labaId in self.newIdList:
                labaInfo['isNew'] = True
            info.append(labaInfo)

        info.sort(key=lambda item: item['labaId'])
        return uiUtils.array2GfxAarry(info, True)

    def onSelectedPos(self, *args):
        labaId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.operation['curLabaId'] = labaId

    def onGetSelectLabaId(self, *args):
        p = BigWorld.player()
        labaId = p.operation.get('curLabaId', 0)
        return GfxValue(labaId)
