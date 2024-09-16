#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/activityHallIconProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import uiUtils
from uiProxy import UIProxy
from data import activity_hall_data as AHD
from data import login_time_reward_data as LTRD

class ActivityHallIconProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityHallIconProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickActivityHall': self.onClickActivityHall,
         'clickGuideGoal': self.onClickGuideGoal,
         'clickFudan': self.onClickFudan}
        self.mediator = None
        self.timer = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVITY_HALL_ICON:
            self.mediator = mediator
            self.stopTimer()
            self.updateTime()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVITY_HALL_ICON)

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVITY_HALL_ICON)

    def updateTime(self):
        if self.mediator:
            self.updateBtnVisible()
            self.timer = BigWorld.callback(600, self.updateTime)

    def updateBtnVisible(self):
        if self.mediator:
            info = {}
            showNum = 0
            p = BigWorld.player()
            activityHallVisible = gameglobal.rds.configData.get('enableActivityHallIcon', False)
            if activityHallVisible:
                activityHallVisible = False
                for value in AHD.data.itervalues():
                    serverConfigId = value.get('serverConfigId')
                    if serverConfigId and not uiUtils.needShowByServer(serverConfigId):
                        continue
                    minLv = value.get('minLv', 0)
                    if p.lv < minLv:
                        continue
                    startShowTime = value.get('startShowTime', '2016.02.01.00.00.00')
                    startShowTime = utils.getTimeSecondFromStr(startShowTime)
                    endShowTime = value.get('endShowTime', '2016.02.21.00.00.00')
                    endShowTime = utils.getTimeSecondFromStr(endShowTime)
                    now = int(p.getServerTime())
                    if now >= startShowTime and now <= endShowTime:
                        activityHallVisible = True
                        break

            info['activityHallVisible'] = activityHallVisible
            if activityHallVisible:
                showNum += 1
            guideGoalVisible = gameglobal.rds.ui.topBar.checkGudeGoal()
            if gameglobal.rds.configData.get('enableRewardGiftActivityIcons', False):
                guideGoalVisible = False
            info['guideGoalVisible'] = guideGoalVisible
            if guideGoalVisible:
                showNum += 1
            fudanInfo = {}
            if gameglobal.rds.configData.get('enableLoginReward', False) and not gameglobal.rds.configData.get('enableRewardGiftActivityIcons', False):
                for key in p.fudanDict.keys():
                    fudanInfo[key] = {}
                    _time = 0
                    _level = p.calcFudanLevel(key, p.fudanDict[key][0], p.fudanDict[key][1])
                    if not p.fudanIsNeedDisplay(key, p.fudanDict[key][0], p.fudanDict[key][1], _level):
                        continue
                    if p.fudanDict.get(key, [0, False, 0])[2] - utils.getNow() < 0:
                        _time = 0
                    else:
                        _time = p.fudanDict.get(key, [0, False, 0])[2] - utils.getNow()
                    _icon = LTRD.data.get(key, {}).get('icon', 1)
                    fudanInfo[key]['time'] = _time
                    fudanInfo[key]['icon'] = _icon
                    showNum += 1

            info['fudanInfo'] = fudanInfo
            info['showNum'] = showNum
            self.mediator.Invoke('updateBtnVisible', uiUtils.dict2GfxDict(info, True))

    def onClickActivityHall(self, *arg):
        gameglobal.rds.ui.activityHall.show()

    def onClickGuideGoal(self, *arg):
        gameglobal.rds.ui.guideGoal.show()

    def onClickFudan(self, *args):
        if gameglobal.rds.configData.get('enableWelfare', False):
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_EVERYDAY_REWARD)
            return
        actId = int(args[3][0].GetNumber())
        if not gameglobal.rds.ui.dailySignIn.fudanIndex:
            gameglobal.rds.ui.dailySignIn.onGetConfigTab()
        gameglobal.rds.ui.dailySignIn.tabIndex = gameglobal.rds.ui.dailySignIn.fudanIndex.get(actId, 0)
        gameglobal.rds.ui.dailySignIn.show()
