#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceFinalGuideProxy.o
import BigWorld
import gameglobal
import events
import utils
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import guide_goal_phase_data as GGPD
from data import guide_goal_column_data as GGCD
from data import sys_config_data as SCD
from data import new_server_activity_data as NSAD

class NewServiceFinalGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceFinalGuideProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        if not self.widget:
            return
        p = BigWorld.player()
        mainMc = self.widget.mainMc
        isComplete = True
        enterDayNum = utils.calcDaysAfterEnterWorld(p)
        for phaseId, value in GGPD.data.iteritems():
            phaseMc = mainMc.getChildByName('phase%d' % phaseId)
            columnList = value.get('columnList', ())
            openDayNum = value.get('openDayNum', 0)
            if enterDayNum >= openDayNum:
                gainedNum = 0
                for columnId in columnList:
                    achievement = GGCD.data.get(columnId, {}).get('achievement', 0)
                    if gameglobal.rds.ui.achvment.checkAchieveFlag(achievement):
                        gainedNum += 1

                if gainedNum < len(columnList):
                    phaseMc.finishMc.visible = False
                    phaseMc.textField.visible = True
                    phaseMc.textField.text = '%d/%d' % (gainedNum, len(columnList))
                    isComplete = False
                else:
                    phaseMc.finishMc.visible = True
                    phaseMc.textField.visible = False
            else:
                phaseMc.finishMc.visible = False
                phaseMc.textField.visible = True
                phaseMc.textField.text = gameStrings.GUIDE_GOAL_OPEN_DAY_DESC % openDayNum
                isComplete = False

        mainMc.openGuideBtn.addEventListener(events.BUTTON_CLICK, self._onOpenGuideBtn, False, 0, True)
        if BigWorld.player().newServerActivityAchieveRewardFlag or not isComplete:
            mainMc.rewardBtn.enabled = False
        else:
            mainMc.rewardBtn.enabled = True
            mainMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self._onRewardBtn, False, 0, True)
        lastDays = NSAD.data.get('achievementOpenDay', 30)
        leftSec = utils.getLeftSecondByServerOpenDay(lastDays)
        if leftSec <= 0:
            leftDays = 0
            leftHours = 0
        else:
            leftDays = utils.formatDurationLeftDay(leftSec)
            leftHours = utils.formatDurationLeftHour(leftSec)
        strTime = gameStrings.LEFT_TIME_HEAD + str(leftDays) + gameStrings.COMMON_DAY + str(leftHours) + gameStrings.COMMON_HOUR
        mainMc.leftTimeTf.text = strTime

    def _onOpenGuideBtn(self, *args):
        gameglobal.rds.ui.guideGoal.show()

    def _onRewardBtn(self, *args):
        BigWorld.player().cell.applyFinalAchieveAward()
        self.widget.mainMc.rewardBtn.enabled = False

    def canOpenTab(self):
        visible = True
        p = BigWorld.player()
        if p.lv < SCD.data.get('guideGoalMinLv', 0):
            visible = False
        lastDays = NSAD.data.get('achievementOpenDay', 30)
        leftSec = utils.getLeftSecondByServerOpenDay(lastDays)
        if leftSec <= 0:
            visible = False
        return visible

    def isShowCompleteRedPoint(self):
        if BigWorld.player().newServerActivityAchieveRewardFlag:
            return False
        enterDayNum = utils.calcDaysAfterEnterWorld(BigWorld.player())
        for phaseId, value in GGPD.data.iteritems():
            columnList = value.get('columnList', ())
            openDayNum = value.get('openDayNum', 0)
            if enterDayNum < openDayNum:
                return False
            for columnId in columnList:
                achievement = GGCD.data.get(columnId, {}).get('achievement', 0)
                if not gameglobal.rds.ui.achvment.checkAchieveFlag(achievement):
                    return False

        return True
