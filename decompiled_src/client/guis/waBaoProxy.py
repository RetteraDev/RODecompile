#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/waBaoProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import Sound
import appSetting
from uiProxy import UIProxy
from callbackHelper import Functor
from data import item_data as ID
from data import consumable_item_data as CID
from data import wabao_data as WD

class WaBaoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WaBaoProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.resItemId = 0
        self.resItemList = []
        self.jumpList = []
        self.intervalIdx = 0
        self.intervalList = []
        self.firstStep = True
        self.hasShowReslut = False
        self.timer = None
        self.resultTimer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WABAO, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WABAO:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WABAO)
        gameglobal.rds.sound.playSound(5)

    def reset(self):
        self.resItemId = 0
        self.resItemList = []
        self.jumpList = []
        self.intervalIdx = 0
        self.intervalList = []
        self.firstStep = True
        if not self.hasShowReslut:
            BigWorld.player().cell.wabaoTurnDone()
        self.hasShowReslut = False
        self.stopTimer()
        BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)
        Sound.enableMusic(appSetting.SoundSettingObj.isMusicEnable())
        gameglobal.rds.sound.stopSound(4673)
        gameglobal.rds.sound.stopSound(4675)

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
        if self.resultTimer:
            BigWorld.cancelCallback(self.resultTimer)
            self.resultTimer = None

    def show(self, resItemId, resItemList, jumpList):
        self.resItemId = resItemId
        self.resItemList = resItemList
        self.jumpList = jumpList
        if not self.mediator:
            multiId = gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WABAO, isModal=True)
            if multiId == None:
                BigWorld.player().cell.cancelWabaoTurn()
                return
        p = BigWorld.player()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        Sound.enableMusic(False)
        gameglobal.rds.sound.playSound(4673)
        gameglobal.rds.sound.playSound(4675)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            treasureId = CID.data.get(self.resItemId, {}).get('treasureId', 0)
            intervalTime = WD.data.get(treasureId, {}).get('jumpSet', ())
            self.intervalIdx = 0
            self.intervalList = []
            totalJumpNum = 0
            for i in xrange(len(self.jumpList)):
                self.intervalList.extend([intervalTime[i]] * self.jumpList[i])
                totalJumpNum += self.jumpList[i]

            resItemLen = len(self.resItemList)
            tempItemList = [(0, 0)] * resItemLen
            resultIdx = totalJumpNum % resItemLen
            tempItemList[resultIdx] = self.resItemList[0]
            tempItemList[(resultIdx - 1 + resItemLen) % resItemLen] = self.resItemList[1]
            tempItemList[(resultIdx + 1) % resItemLen] = self.resItemList[2]
            tempItemList[(resultIdx - 2 + resItemLen) % resItemLen] = self.resItemList[3]
            tempItemList[(resultIdx + 2) % resItemLen] = self.resItemList[4]
            tempIdx = 0
            for i in xrange(5, resItemLen):
                while tempItemList[tempIdx][0] != 0:
                    tempIdx += 1

                tempItemList[tempIdx] = self.resItemList[i]

            self.resItemList = tempItemList
            resTreasureLv = ID.data.get(self.resItemId, {}).get('treasureLv', 0)
            itemList = []
            for i in xrange(resItemLen):
                itemId, itemNum = self.resItemList[i]
                iddata = ID.data.get(itemId, {})
                itemInfo = {}
                itemInfo['itemId'] = itemId
                itemInfo['itemName'] = iddata.get('name', '')
                itemInfo['itemNum'] = itemNum if itemNum > 1 else ''
                itemInfo['iconPath'] = uiUtils.getItemIconFile150(itemId)
                itemInfo['isTreasure'] = iddata.get('treasureLv', 0) >= resTreasureLv
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def startTurn(self):
        if self.mediator:
            resItemLen = len(self.resItemList)
            intervalLen = len(self.intervalList)
            if self.intervalIdx >= intervalLen:
                info = {}
                info['lightIdx'] = self.intervalIdx % resItemLen
                info['darkIdx'] = (self.intervalIdx + resItemLen - 1) % resItemLen
                self.mediator.Invoke('showResult', uiUtils.dict2GfxDict(info, True))
                gameglobal.rds.sound.playSound(4674)
                itemId, itemNum = self.resItemList[info['lightIdx']]
                resTreasureLv = ID.data.get(self.resItemId, {}).get('treasureLv', 0)
                isTreasure = ID.data.get(itemId, {}).get('treasureLv', 0) >= resTreasureLv
                self.resultTimer = BigWorld.callback(1, Functor(self.showResult, itemId, itemNum, isTreasure))
                return
            nowInterval = self.intervalList[self.intervalIdx]
            info = {}
            info['lightIdx'] = self.intervalIdx % resItemLen
            if self.firstStep:
                info['darkIdx'] = -1
            else:
                info['darkIdx'] = (self.intervalIdx + resItemLen - 1) % resItemLen
            self.firstStep = False
            self.mediator.Invoke('startTurn', uiUtils.dict2GfxDict(info, True))
            gameglobal.rds.sound.playSound(4674)
            self.intervalIdx += 1
            self.timer = BigWorld.callback(nowInterval, self.startTurn)

    def onConfirm(self, *arg):
        gameglobal.rds.sound.playSound(2)
        self.stopTimer()
        self.firstStep = True
        self.startTurn()

    def showResult(self, itemId, itemNum, isTreasure):
        self.hasShowReslut = True
        gameglobal.rds.ui.waBaoResult.show(itemId, itemNum, isTreasure)
