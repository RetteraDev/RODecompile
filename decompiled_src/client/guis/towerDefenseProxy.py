#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/towerDefenseProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiConst

class TowerDefenseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TowerDefenseProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCountDownTime': self.onGetCountDownTime,
         'getCurrentWave': self.onGetCurrentWave,
         'getChallengeResult': self.onGetChallengeResult,
         'getPlayerInfo': self.onGetPlayerInfo,
         'showWave': self.onShowWave,
         'isShowCurWave': self.onIsShowCurWave}
        self.curWave = 0
        self.result = None
        self.info = None
        self.time = 10
        self.schoolMap = {3: 'shengtang',
         4: 'yuxu',
         5: 'guangren',
         6: 'yuxu',
         7: 'yuxu',
         8: 'yuxu'}
        self.isShowCurWave = True

    def onGetCountDownTime(self, *arg):
        return GfxValue(self.time)

    def onGetCurrentWave(self, *arg):
        ret = GfxValue(self.curWave)
        return ret

    def onGetChallengeResult(self, *arg):
        if self.result:
            return GfxValue('successful')
        return GfxValue('fail')

    def onGetPlayerInfo(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        self.info.sort(key=lambda k: k['scores'])
        self.info.reverse()
        for i, item in enumerate(self.info):
            arr = self.movie.CreateArray()
            arr.SetElement(0, GfxValue(self.schoolMap[p.school]))
            arr.SetElement(1, GfxValue(gbk2unicode(item['name'])))
            arr.SetElement(2, GfxValue(i + 1))
            arr.SetElement(3, GfxValue(item['boss']))
            arr.SetElement(4, GfxValue(item['monster']))
            arr.SetElement(5, GfxValue(item['cuipian']))
            arr.SetElement(6, GfxValue(item['hun']))
            arr.SetElement(7, GfxValue(item['die']))
            arr.SetElement(8, GfxValue(item['scores']))
            ret.SetElement(i, arr)

        return ret

    def showCountDown(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TD_COUNTDOWN)

    def showTdResult(self):
        self.curWave = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TD_COUNTDOWN)

    def hideCountDown(self):
        self.curWave = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TD_COUNTDOWN)

    def clearWidget(self):
        self.hideCountDown()

    def reset(self):
        self.curWave = 0
        self.result = None
        self.info = None
        self.time = 10
        self.isShowCurWave = True

    def onShowWave(self, *arg):
        gameglobal.rds.ui.playTips.show(gameStrings.TEXT_TOWERDEFENSEPROXY_89 % self.curWave, 3)

    def setTime(self, time):
        self.time = time

    def setShowCurWave(self, show):
        self.isShowCurWave = show

    def onIsShowCurWave(self, *arg):
        return GfxValue(self.isShowCurWave)
