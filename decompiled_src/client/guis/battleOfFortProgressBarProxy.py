#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleOfFortProgressBarProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import sMath
import utils
import const
from uiProxy import UIProxy
from guis import uiUtils
from data import battle_field_data as BFD
from data import battle_field_fort_data as BFFD
from data import duel_config_data as DCD
MAX_PROGRESS_WIDTH = 348
FORT_OCCUP_BAR_WIDTH = 173
MAX_OCCUPY_POINT = 3
TYPE_MAIN_FRAME = 0
TYPE_SECOND_FRAME = 1
TYPE_ZAIJU_FRAME = 2

class BattleOfFortProgressBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleOfFortProgressBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.durationTime = 0
        self.timeTick = None
        self.towerId = -1
        self.occupyInfo = {}
        self.zaijuInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BATTLE_OF_FORT_PROGRESS_BAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def reset(self):
        self.durationTime = 0
        self.timeTick = None
        self.towerId = -1
        self.occupyInfo = {}
        self.zaijuInfo = {}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_OF_FORT_PROGRESS_BAR)
        self.widget = None

    def initUI(self):
        self.widget.statistBtn.addEventListener(events.MOUSE_CLICK, self.handleStatistBtnClick, False, 0, True)
        self.setFortInfo()
        self.setSideName()
        self.initBFTime()
        self.updateNewFlagDonate(0, 0)
        self.updateNewFlagOccupyPoint({})

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_OF_FORT_PROGRESS_BAR)

    def refreshInfo(self):
        if not self.widget:
            return
        self.startTimer()
        self.refreshStatsInfo()

    def initBFTime(self):
        p = BigWorld.player()
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        self.widget.flagTimer.text = utils.formatTimeStr(totalTime, 'm:s', zeroShow=True, sNum=2, mNum=2)

    def setSideName(self):
        if not self.widget:
            return
        p = BigWorld.player()
        otherCamp = 3 - p.tempCamp
        sideNames = DCD.data.get('battleOfFortSideNames', {1: gameStrings.TEXT_BATTLEOFFORTPROGRESSBARPROXY_89,
         2: gameStrings.TEXT_BATTLEOFFORTPROGRESSBARPROXY_89_1})
        self.widget.selfTitleName.text = sideNames.get(p.tempCamp, '')
        self.widget.enemyTitleName.text = sideNames.get(otherCamp, '')

    def startTimer(self):
        self.durationTime, color = self.getDurationTime()
        if self.timeTick:
            BigWorld.cancelCallback(self.timeTick)
        self.widget.flagTimer.htmlText = uiUtils.toHtml(utils.formatTimeStr(self.durationTime, 'm:s', zeroShow=True, sNum=2, mNum=2), color)
        self.timeTick = BigWorld.callback(1, self.handleTimer)

    def getDurationTime(self):
        p = BigWorld.player()
        if not p.bfTimeRec:
            return (0, '#FFFFFF')
        if not p.bfTimeRec.has_key('tReady'):
            return (0, '#FFFFFF')
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        if p.getServerTime() - p.bfTimeRec['tReady'] >= 0:
            color = '#FFFFFF'
            countTime = totalTime - int(p.getServerTime() - p.bfTimeRec['tReady'])
        else:
            color = '#FF0000'
            countTime = abs(int(p.getServerTime() - p.bfTimeRec['tReady']))
        return (int(countTime), color)

    def handleTimer(self):
        self.durationTime, color = self.getDurationTime()
        if self.durationTime < 0:
            if self.timeTick:
                BigWorld.cancelCallback(self.timeTick)
            return
        self.timeTick = BigWorld.callback(1, self.handleTimer)
        if self.widget:
            self.widget.flagTimer.htmlText = uiUtils.toHtml(utils.formatTimeStr(self.durationTime, 'm:s', zeroShow=True, sNum=2, mNum=2), color)

    def refreshStatsInfo(self):
        p = BigWorld.player()
        enemyMaxRes = myMaxRes = BFD.data.get(p.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        myCurRes = p.getMyRes()
        enemyCurRes = p.getEnemyRes()
        self.widget.selfNum.htmlText = myCurRes
        self.widget.selfStats.currentValue = myCurRes
        self.widget.selfStats.maxValue = myMaxRes
        self.widget.enemyNum.htmlText = enemyCurRes
        self.widget.enemyStats.currentValue = enemyCurRes
        self.widget.enemyStats.maxValue = enemyMaxRes

    def setFortInfo(self, ret = None):
        if not self.widget:
            return
        else:
            if ret == None:
                self.widget.fortOccupNum.visible = False
            else:
                value, maxValue = DCD.data.get('fortOccupBarValues', [50, 100])
                self.widget.fortOccupNum.bar.width = value * FORT_OCCUP_BAR_WIDTH / maxValue
                self.widget.fortOccupNum.bar1.width = value * FORT_OCCUP_BAR_WIDTH / maxValue
                self.widget.fortOccupNum.visible = True
                self.widget.fortOccupNum.thumb.x = MAX_PROGRESS_WIDTH * (0.5 - ret['fortVal'] / (ret['values'][1] * 1.0) * 0.5)
                self.widget.fortOccupNum.thumb.x = sMath.clamp(self.widget.fortOccupNum.thumb.x, 0, MAX_PROGRESS_WIDTH)
            return

    def handleStatistBtnClick(self, *args):
        gameglobal.rds.ui.battleField.onOpenStatsClick()

    def enterNewFlagTowerTrap(self, towerId, curValMap):
        if not self.widget:
            return
        self.towerId = towerId
        p = BigWorld.player()
        fortData = BFFD.data.get(towerId, {})
        fortInfo = {'values': (fortData.get('limitVal', 50), fortData.get('maxVal', 100))}
        fortVal = curValMap.get(p.tempCamp, 0)
        if fortVal <= 0:
            otherCamp = 3 - p.tempCamp
            fortVal = -curValMap.get(otherCamp, 0)
        fortInfo['fortVal'] = fortVal
        self.setFortInfo(fortInfo)

    def leaveNewFlagTowerTrap(self, towerId):
        if not self.widget:
            return
        else:
            if self.towerId == towerId:
                self.towerId = None
                self.setFortInfo()
            return

    def updateNewFlagTowerTrap(self, occupyInfo):
        if not self.widget:
            return
        if not self.towerId:
            return
        pointInfo = self.getOccupyPointInfo(occupyInfo)
        if not pointInfo:
            return
        p = BigWorld.player()
        fortData = BFFD.data.get(self.towerId, {})
        fortInfo = {'values': (fortData.get('limitVal', 50), fortData.get('maxVal', 100))}
        curValMap = pointInfo.get('curValMap', {})
        fortVal = curValMap.get(p.tempCamp, 0)
        if fortVal <= 0:
            otherCamp = 3 - p.tempCamp
            fortVal = -curValMap.get(otherCamp, 0)
        fortInfo['fortVal'] = fortVal
        self.setFortInfo(fortInfo)

    def getOccupyPointInfo(self, occupyInfo):
        for i, pointId in enumerate(occupyInfo):
            pointInfo = occupyInfo[pointId]
            fortId = pointInfo.get('fortId', 0)
            if self.towerId == fortId:
                return pointInfo

        return {}

    def updateNewFlagOccupyPoint(self, occupyInfo):
        if not self.widget:
            return
        self.occupyInfo = occupyInfo
        self.updateOccupyPoint()

    def enterNewFlagZaiju(self, NUID, camp, gbId):
        if not self.widget:
            return
        if NUID not in self.zaijuInfo:
            self.zaijuInfo[NUID] = {'camp': camp,
             'gbId': gbId}
        self.updateOccupyPoint()

    def leaveNewFlagZaiju(self, NUID, camp, gbId):
        if not self.widget:
            return
        if NUID in self.zaijuInfo:
            self.zaijuInfo[NUID] = {}
        self.updateOccupyPoint()

    def updateOccupyPoint(self):
        if not self.widget:
            return
        p = BigWorld.player()
        myCamp = p.tempCamp
        otherCamp = 3 - p.tempCamp
        myPoint = []
        otherPoint = []
        for i, pointId in enumerate(self.occupyInfo):
            pointInfo = self.occupyInfo[pointId]
            camp = pointInfo.get('camp', 0)
            fortId = pointInfo.get('fortId', 0)
            if camp == myCamp:
                if fortId in uiConst.BATTLE_MAIN_FIELD_FORT_IDS:
                    myPoint.append({'type': TYPE_MAIN_FRAME})
                elif fortId in uiConst.BATTLE_SECOND_FIELD_FORT_IDS:
                    myPoint.append({'type': TYPE_SECOND_FRAME})
            elif camp == otherCamp:
                if fortId in uiConst.BATTLE_MAIN_FIELD_FORT_IDS:
                    otherPoint.append({'type': TYPE_MAIN_FRAME})
                elif fortId in uiConst.BATTLE_SECOND_FIELD_FORT_IDS:
                    otherPoint.append({'type': TYPE_SECOND_FRAME})

        for i, NUID in enumerate(self.zaijuInfo):
            info = self.zaijuInfo[NUID]
            camp = info.get('camp', 0)
            if camp == myCamp:
                myPoint.append({'type': TYPE_ZAIJU_FRAME})
            elif camp == otherCamp:
                otherPoint.append({'type': TYPE_ZAIJU_FRAME})

        for i in xrange(MAX_OCCUPY_POINT):
            myPointMc = self.widget.selfPoint.getChildByName('point%d' % i)
            if i < len(myPoint):
                type = myPoint[i].get('type', 0)
                myPointMc.gotoAndStop('type%d' % type)
                myPointMc.visible = True
            else:
                myPointMc.visible = False
            otherPointMc = self.widget.enemyPoint.getChildByName('point%d' % i)
            if i < len(otherPoint):
                type = otherPoint[i].get('type', 0)
                otherPointMc.gotoAndStop('type%d' % type)
                otherPointMc.visible = True
            else:
                otherPointMc.visible = False

    def updateNewFlagDonate(self, point, rank):
        if not self.widget:
            return
        self.widget.contributionText.text = point
        self.widget.rankText.text = rank

    def checkBattleFortNewFlag(self):
        p = BigWorld.player()
        return gameglobal.rds.configData.get('enableNewFlagBF', False) and p.inFubenType(const.FB_TYPE_BATTLE_FIELD_NEW_FLAG)

    def getAvatarCampName(self, en):
        sideNames = DCD.data.get('battleOfFortSideNames', {1: gameStrings.TEXT_BATTLEOFFORTPROGRESSBARPROXY_89,
         2: gameStrings.TEXT_BATTLEOFFORTPROGRESSBARPROXY_89_1})
        targetCamp = getattr(en, 'tempCamp', 0)
        campName = sideNames.get(targetCamp, '')
        return campName
