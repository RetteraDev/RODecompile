#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guideGoalProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
import clientUtils
from uiProxy import UIProxy
from data import achievement_data as AD
from data import guide_goal_phase_data as GGPD
from data import guide_goal_column_data as GGCD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class GuideGoalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuideGoalProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTabInfo': self.onGetTabInfo,
         'getLeftTabInfo': self.onGetLeftTabInfo,
         'getDetailInfo': self.onGetDetailInfo,
         'confirm': self.onConfirm,
         'clickFly': self.onClickFly}
        self.mediator = None
        self.currentTabIndex = -1
        self.leftTabIndex = -1
        self.tabToPhase = {}
        self.awardInfo = {}
        self.achieveIdToOpenDay = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUIDE_GOAL, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUIDE_GOAL:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUIDE_GOAL)

    def reset(self):
        self.currentTabIndex = -1
        self.leftTabIndex = -1

    def clearData(self):
        self.awardInfo = {}

    def show(self):
        p = BigWorld.player()
        if p.lv < SCD.data.get('guideGoalMinLv', 0):
            p.showGameMsg(GMDD.data.REFUSE_GUIDE_GOAL, ())
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUIDE_GOAL)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUIDE_GOAL)

    def onGetTabInfo(self, *arg):
        self.refreshTabInfo()

    def refreshTabInfo(self):
        if self.mediator:
            p = BigWorld.player()
            tabList = []
            enterDayNum = utils.calcDaysAfterEnterWorld(p)
            for phaseId, value in GGPD.data.iteritems():
                tabInfo = {}
                tabInfo['phaseId'] = phaseId
                phaseAchievement = value.get('phaseAchievement', 0)
                openDayNum = value.get('openDayNum', 0)
                if enterDayNum >= openDayNum:
                    tabInfo['enabled'] = True
                    tabInfo['label'] = ''
                    tabInfo['finishFlag'] = gameglobal.rds.ui.achvment.checkAchieveFlag(phaseAchievement)
                else:
                    tabInfo['enabled'] = False
                    tabInfo['label'] = gameStrings.TEXT_GUIDEGOALPROXY_85 % openDayNum
                    tabInfo['finishFlag'] = False
                tabList.append(tabInfo)

            tabList.sort(key=lambda x: x['phaseId'])
            self.tabToPhase = {}
            for i in xrange(len(tabList)):
                self.tabToPhase[i] = tabList[i]['phaseId']

            self.mediator.Invoke('refreshTabInfo', uiUtils.array2GfxAarry(tabList, True))
            self.requestGetAwardedInfo()

    def onGetLeftTabInfo(self, *arg):
        self.currentTabIndex = int(arg[3][0].GetNumber())
        self.refreshLeftTabInfo(True)

    def refreshLeftTabInfo(self, useFirst):
        if not useFirst:
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
            gameglobal.rds.ui.welfare.refreshInfo()
        if self.mediator:
            self.leftTabIndex = -1
            info = {}
            info['useFirst'] = useFirst
            phaseId = self.tabToPhase[self.currentTabIndex]
            tabList = []
            ggpd = GGPD.data.get(phaseId, {})
            info['phaseName'] = ggpd.get('phaseName', '')
            columnList = ggpd.get('columnList', ())
            for columnId in columnList:
                ggcd = GGCD.data.get(columnId, {})
                tabInfo = {}
                tabInfo['label'] = ggcd.get('name', '')
                achievement = ggcd.get('achievement', 0)
                tabInfo['unGetFlag'] = gameglobal.rds.ui.achvment.checkAchieveFlag(achievement)
                tabInfo['finishFlag'] = False
                if tabInfo['unGetFlag'] and self.awardInfo.get(achievement):
                    tabInfo['unGetFlag'] = False
                    tabInfo['finishFlag'] = True
                tabList.append(tabInfo)

            info['tabList'] = tabList
            self.mediator.Invoke('refreshLeftTabInfo', uiUtils.dict2GfxDict(info, True))

    def onGetDetailInfo(self, *arg):
        leftTabIndex = int(arg[3][0].GetNumber())
        if self.leftTabIndex == leftTabIndex:
            return
        self.leftTabIndex = leftTabIndex
        self.refreshDetailInfo()

    def refreshDetailInfo(self):
        if self.mediator:
            info = {}
            phaseId = self.tabToPhase[self.currentTabIndex]
            ggpd = GGPD.data.get(phaseId, {})
            columnList = ggpd.get('columnList', ())
            columnId = columnList[self.leftTabIndex]
            ggcd = GGCD.data.get(columnId, {})
            info['columnId'] = columnId
            info['leftTitle'] = ggcd.get('name', '')
            info['leftDesc'] = ggcd.get('desc', '')
            info['leftSeekVisible'] = ggcd.get('seekId') != None
            info['leftSeekDesc'] = ggcd.get('seekDesc', '')
            achievement = ggcd.get('achievement', 0)
            info['leftAchieveId'] = achievement
            bonusId = AD.data.get(achievement, {}).get('bonusId', 0)
            itemBonus = clientUtils.genItemBonus(bonusId)
            leftItemList = []
            for i in xrange(len(itemBonus)):
                if i >= 2:
                    break
                leftItemList.append(uiUtils.getGfxItemById(itemBonus[i][0], itemBonus[i][1]))

            info['leftItemList'] = leftItemList
            if len(leftItemList) <= 0:
                leftConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                leftConfirmBtnEnabled = False
            elif self.awardInfo.get(achievement):
                leftConfirmBtnLabel = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                leftConfirmBtnEnabled = False
            elif gameglobal.rds.ui.achvment.checkAchieveFlag(achievement):
                leftConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                leftConfirmBtnEnabled = True
            else:
                leftConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                leftConfirmBtnEnabled = False
            info['leftConfirmBtnLabel'] = leftConfirmBtnLabel
            info['leftConfirmBtnEnabled'] = leftConfirmBtnEnabled
            gainedNum = 0
            for columnId in columnList:
                achievement = GGCD.data.get(columnId, {}).get('achievement', 0)
                if gameglobal.rds.ui.achvment.checkAchieveFlag(achievement):
                    gainedNum += 1

            info['phaseNum'] = '%d/%d' % (gainedNum, len(columnList))
            info['rightTitle'] = gameStrings.TEXT_GUIDEGOALPROXY_193 % ggpd.get('phaseName', '')
            info['rightDesc'] = ggpd.get('phaseDesc', '')
            achievement = ggpd.get('phaseAchievement', 0)
            info['rightAchieveId'] = achievement
            bonusId = AD.data.get(achievement, {}).get('bonusId', 0)
            itemBonus = clientUtils.genItemBonus(bonusId)
            rightItemList = []
            for i in xrange(len(itemBonus)):
                if i >= 2:
                    break
                rightItemList.append(uiUtils.getGfxItemById(itemBonus[i][0], itemBonus[i][1]))

            info['rightItemList'] = rightItemList
            if len(rightItemList) <= 0:
                rightConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                rightConfirmBtnEnabled = False
            elif self.awardInfo.get(achievement):
                rightConfirmBtnLabel = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                rightConfirmBtnEnabled = False
            elif gameglobal.rds.ui.achvment.checkAchieveFlag(achievement):
                rightConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                rightConfirmBtnEnabled = True
            else:
                rightConfirmBtnLabel = gameStrings.TEXT_FENGWUZHIPROXY_334
                rightConfirmBtnEnabled = False
            info['rightConfirmBtnLabel'] = rightConfirmBtnLabel
            info['rightConfirmBtnEnabled'] = rightConfirmBtnEnabled
            self.mediator.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        achieveId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.applyAchieveAward(achieveId)

    def onClickFly(self, *arg):
        columnId = int(arg[3][0].GetNumber())
        seekId = GGCD.data.get(columnId, {}).get('seekId', ())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def requestGetAwardedInfo(self):
        p = BigWorld.player()
        self.initAchieveIdToOpenDay()
        if not self.awardInfo:
            achieveIds = []
            for achieveId in self.achieveIdToOpenDay:
                achieveIds.append(achieveId)

            p.base.queryAchievesGetAwarded(achieveIds)

    def updateGetAwardedInfo(self, awardInfo):
        self.awardInfo.update(awardInfo)
        self.refreshLeftTabInfo(False)

    def checkPushMsg(self, achieveId):
        pass

    def initAchieveIdToOpenDay(self):
        if self.achieveIdToOpenDay:
            return
        for value in GGPD.data.itervalues():
            openDayNum = value.get('openDayNum', 0)
            phaseAchievement = value.get('phaseAchievement', 0)
            self.achieveIdToOpenDay[phaseAchievement] = openDayNum
            columnList = value.get('columnList', ())
            for columnId in columnList:
                achievement = GGCD.data.get(columnId, {}).get('achievement', 0)
                self.achieveIdToOpenDay[achievement] = openDayNum

    def canGainAward(self):
        p = BigWorld.player()
        self.requestGetAwardedInfo()
        enterDayNum = utils.calcDaysAfterEnterWorld(p)
        for achieveId, openDayNum in self.achieveIdToOpenDay.iteritems():
            if enterDayNum < openDayNum:
                continue
            if not gameglobal.rds.ui.achvment.checkAchieveFlag(achieveId):
                continue
            if not self.awardInfo.get(achieveId):
                return True

        return False

    def checkAllAwardGain(self):
        self.requestGetAwardedInfo()
        for achieveId in self.achieveIdToOpenDay.iterkeys():
            if not gameglobal.rds.ui.achvment.checkAchieveFlag(achieveId):
                return False
            if not self.awardInfo.get(achieveId, False):
                return False

        return True
