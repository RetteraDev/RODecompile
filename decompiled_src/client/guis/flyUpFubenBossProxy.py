#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/flyUpFubenBossProxy.o
import BigWorld
import utils
import copy
import time
import gameglobal
import uiConst
import random
from asObject import Tweener
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import monster_model_client_data as MMCD
from data import formula_client_data as FCD
import gamelog
BOSS_NUM = 5
RANDOM_NUM = 7
ROLL_TOTAL_TIME = 4
BASE_ROLL_TIME = 0.1
ROLL_FACTOR = 0.15
ICON_MC_HEIGHT = 156
ICON_NUM = 4
BOSS_IMG_PREFIX = 'bossCharTypePic/'

class FlyUpFubenBossProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FlyUpFubenBossProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentBossIdx = 0
        self.rollStartTime = 0
        self.fbInfo = {}
        self.randomList = []
        self.randomIndexList = []
        self.fullRandomList = []
        self.lastIndexLists = []
        self.currRollingY = 0
        self.randomPos = 0
        self.lastRollId = -1
        self.rollCallBack = None
        self.hideCallBack = None
        self.lastTickTime = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FLY_UP_FUBEN_BOSS, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FLY_UP_FUBEN_BOSS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.randomList = []
        self.fullRandomList = []
        self.lastIndexLists = []
        self.currRollingY = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FLY_UP_FUBEN_BOSS)
        self.cancelCallbacks()

    def cancelCallbacks(self):
        if self.rollCallBack:
            BigWorld.cancelCallback(self.rollCallBack)
        self.rollCallBack = None
        if self.hideCallBack:
            BigWorld.cancelCallback(self.hideCallBack)
        self.hideCallBack = None
        Tweener.removeTweens(self.widget)

    def setFbInfo(self, randomUIInfo):
        gamelog.debug('dxk@flyUpFubenBoss setFbInfo', randomUIInfo)
        self.fbInfo = randomUIInfo.get('BossRandomUIInfo', {})
        monsterList = copy.copy(self.fbInfo.get('killedBossList', []))
        chosenBossNo = self.fbInfo.get('chosenBossNo', 0)
        if chosenBossNo:
            monsterList.append(chosenBossNo)
            self.currentBossIdx = len(monsterList) - 1
        else:
            self.currentBossIdx = -1
        self.fbInfo['monsterList'] = monsterList

    def show(self):
        self.cancelCallbacks()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FLY_UP_FUBEN_BOSS)
        else:
            self.setInitInfo()
            self.playKillAnim()

    def getBossIconPath(self, bossId):
        iconId = MMCD.data.get(bossId, {}).get('modelPic', 0)
        return self.getIconPath(iconId)

    def getIconPath(self, iconId):
        return BOSS_IMG_PREFIX + str(iconId) + '.dds'

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.setInitInfo()
        ASUtils.callbackAtFrame(self.widget, 40, self.playKillAnim)

    def setInitInfo(self):
        self.widget.alpha = 1
        bossList = self.fbInfo.get('monsterList', [])
        for i in xrange(BOSS_NUM):
            bossMc = self.widget.getChildByName('boss%d' % i)
            bossMc.cacheAsBitmap = True
            if i < self.currentBossIdx - 1:
                bossMc.visible = True
                bossMc.gotoAndStop('stateKilled')
                bossMc.killedMc.icon.fitSize = True
                bossMc.killedMc.icon.loadImage(self.getBossIconPath(bossList[i]))
            elif i == self.currentBossIdx - 1:
                bossMc.visible = True
                bossMc.gotoAndStop('stateKill')
                bossMc.killMc.gotoAndStop(0)
                bossMc.killMc.icon.fitSize = True
                bossMc.killMc.icon.loadImage(self.getBossIconPath(bossList[i]))
            else:
                bossMc.visible = False

    def playKillAnim(self, *args):
        if self.currentBossIdx == 0:
            self.playOpenAnim()
        else:
            bossMc = self.widget.getChildByName('boss%d' % (self.currentBossIdx - 1))
            bossMc.gotoAndStop('stateKill')
            bossMc.killMc.gotoAndPlay(0)
            ASUtils.callbackAtFrame(bossMc.killMc, 55, self.playOpenAnim)

    def playOpenAnim(self, *args):
        bossList = self.fbInfo.get('monsterList', [])
        if self.currentBossIdx != 0:
            bossMc = self.widget.getChildByName('boss%d' % (self.currentBossIdx - 1))
            bossMc.gotoAndStop('stateKilled')
            bossMc.killedMc.icon.fitSize = True
            bossMc.killedMc.icon.loadImage(self.getBossIconPath(bossList[self.currentBossIdx - 1]))
        if self.currentBossIdx == -1:
            self.hideCallBack = BigWorld.callback(SCD.data.get('flyUpBossLastTime', 1), self.hide)
            return
        bossMc = self.widget.getChildByName('boss%d' % self.currentBossIdx)
        bossMc.gotoAndStop('stateShow')
        bossMc.visible = True
        bossMc.openMc.gotoAndPlay(0)
        ASUtils.callbackAtFrame(bossMc.openMc, 90, self.playRollingAnimEx)

    def playRollingAnimEx(self, *args):
        bossMc = self.widget.getChildByName('boss%d' % self.currentBossIdx)
        bossMc.gotoAndStop('stateOver')
        overMc = bossMc.overMc
        self.rollStartTime = time.time()
        self.lastTickTime = self.rollStartTime
        self.fullRandomList = self.getFullRandomBossList()
        self.currRollingY = 0
        self.lastIndexLists = []
        for i in xrange(ICON_NUM):
            iconMc = overMc.rollMc.getChildByName('icon%d' % i)
            iconMc.fitSize = True

        self.rollLoopEx()

    def rollLoopEx(self):
        if not self.widget:
            return
        bossMc = self.widget.getChildByName('boss%d' % self.currentBossIdx)
        overMc = bossMc.overMc
        doRoll = True
        if self.currRollingY >= (len(self.fullRandomList) - 1) * ICON_MC_HEIGHT:
            self.currRollingY = (len(self.fullRandomList) - 1) * ICON_MC_HEIGHT
            doRoll = False
        indexLists = self.getCurrShowIdxs(self.currRollingY)
        if self.lastIndexLists != indexLists:
            for i, index in enumerate(indexLists):
                iconMc = overMc.rollMc.getChildByName('icon%d' % (ICON_NUM - i - 1))
                randIdx = index % len(self.fullRandomList)
                bossId = self.fullRandomList[randIdx]
                iconPath = self.getBossIconPath(bossId)
                iconMc.loadImage(iconPath)

            self.lastIndexLists = indexLists
        rollY = self.getRollMcY(self.currRollingY)
        overMc.rollMc.y = -(ICON_NUM - 1) * ICON_MC_HEIGHT + rollY
        if doRoll:
            now = time.time()
            passTime = max(0, self.lastTickTime - self.rollStartTime)
            deltaTime = max(0, now - self.lastTickTime)
            rollSpeedFunc = FCD.data.get(SCD.data.get('flyUpRollSpeedFunc', 0), {}).get('formula', self.getRollSpeed)
            info = {'passTime': passTime}
            self.currRollingY += max(1, int(rollSpeedFunc(info) * ICON_MC_HEIGHT * deltaTime))
            self.lastTickTime = now
            self.rollCallBack = BigWorld.callback(0.03, self.rollLoopEx)
        else:
            self.hideCallBack = BigWorld.callback(SCD.data.get('flyUpBossLastTime', 1), self.fadeHide)

    def getRollSpeed(self, info):
        passTime = info.get('passTime', 0)
        return 0.3 + 10 / (passTime * 0.3 + 2)

    def getCurrShowIdxs(self, totalY):
        index = int(totalY / ICON_MC_HEIGHT)
        index -= index % (ICON_NUM - 1)
        indexs = [index]
        for i in xrange(1, ICON_NUM):
            indexs.append(index + i)

        return indexs

    def getRollMcY(self, totalY):
        return totalY % ((ICON_NUM - 1) * ICON_MC_HEIGHT)

    def playRollingAnim(self, *args):
        bossMc = self.widget.getChildByName('boss%d' % self.currentBossIdx)
        bossMc.gotoAndStop('stateOver')
        overMc = bossMc.overMc
        overMc.gotoAndStop(0)
        self.randomList = self.getRandomBossList()
        self.randomIndexList = []
        self.randomPos = 0
        for i in xrange(0, len(self.randomList)):
            iconMc = overMc.getChildByName('icon%d' % i)
            iconMc.fitSize = True
            iconMc.loadImage(self.getBossIconPath(self.randomList[i]))

        self.rollStartTime = utils.getNow()
        self.lastRollId = 0
        self.rollLoop()

    def rollLoop(self):
        if not self.widget:
            return
        now = utils.getNow()
        passTime = max(0, now - self.rollStartTime)
        bossMc = self.widget.getChildByName('boss%d' % self.currentBossIdx)
        overMc = bossMc.overMc
        gotoFrame = self.getNextRandIndex()
        self.lastRollId = gotoFrame
        if passTime < ROLL_TOTAL_TIME:
            overMc.gotoAndStop(gotoFrame)
            nextTime = BASE_ROLL_TIME + ROLL_FACTOR * passTime
            self.rollCallBack = BigWorld.callback(nextTime, self.rollLoop)
        else:
            overMc.gotoAndStop(len(self.randomList))
            self.hideCallBack = BigWorld.callback(SCD.data.get('flyUpBossLastTime', 1), self.fadeHide)

    def getNextRandIndex(self):
        if len(self.randomList) == 0:
            return 1
        if not self.randomIndexList:
            self.randomIndexList = range(1, len(self.randomList) + 1)
        elif self.randomPos >= len(self.randomIndexList):
            newIndexList = range(1, len(self.randomList) + 1)
            newIndexList.remove(self.randomIndexList[-1])
            self.randomIndexList = newIndexList
            self.randomPos = 0
        random.shuffle(self.randomIndexList)
        randIdx = self.randomIndexList[self.randomPos]
        self.randomPos += 1
        return randIdx

    def fadeHide(self):
        ASUtils.addTweener(self.widget, {'time': 1,
         'alpha': 0}, self.endFadeCallBack)

    def endFadeCallBack(self, *args):
        self.hide()

    def getFullRandomBossList(self):
        bossList = self.fbInfo.get('monsterList', [])
        allBossList = self.fbInfo.get('curSlotBossList', [])
        if bossList[self.currentBossIdx] in allBossList:
            allBossList.remove(bossList[self.currentBossIdx])
        flyUpBossRandomNum = SCD.data.get('flyUpBossRandomNum', 20)
        if len(allBossList) == 0:
            return [bossList[self.currentBossIdx]] * flyUpBossRandomNum
        fullRandomList = []
        fullRandomList.append(bossList[self.currentBossIdx])
        randomPool = copy.copy(allBossList)
        randomPool.append(bossList[self.currentBossIdx])
        tempRandomList = copy.copy(allBossList)
        tempIdx = 0
        random.shuffle(tempRandomList)
        while len(fullRandomList) - 1 < flyUpBossRandomNum:
            if tempIdx < len(tempRandomList):
                fullRandomList.append(tempRandomList[tempIdx])
                tempIdx += 1
            else:
                tempRandomList = copy.copy(randomPool)
                tempRandomList.remove(fullRandomList[-1])
                random.shuffle(tempRandomList)
                tempIdx = 0

        fullRandomList.reverse()
        return fullRandomList

    def getRandomBossList(self):
        bossList = self.fbInfo.get('monsterList', [])
        allBossList = self.fbInfo.get('curSlotBossList', [])
        if bossList[self.currentBossIdx] in allBossList:
            allBossList.remove(bossList[self.currentBossIdx])
        random.shuffle(allBossList)
        randomList = allBossList[:min(len(allBossList), RANDOM_NUM - 1)]
        randomList.append(bossList[self.currentBossIdx])
        return randomList

    def refreshInfo(self):
        if not self.widget:
            return
