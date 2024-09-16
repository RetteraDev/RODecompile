#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandBarProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import math
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import sys_config_data as SCD
COUNT_DOWN_SHOW = 60
PROGRESS_BAR_WIDTH = 248

class VoidDreamlandBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.flyEffect = None
        self.currTimePre = ''
        self.currSkilledPre = ''
        self.fubenData = {'totalTime': 0,
         'startTime': 0,
         'endTime': 0,
         'targetState': 0}
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_BAR, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_BAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_BAR)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_BAR)

    def reset(self):
        self.timer = None
        self.flyEffect = None
        self.currTimePre = ''
        self.currSkilledPre = ''
        self.fubenData = {'totalTime': 0,
         'startTime': 0,
         'endTime': 0,
         'targetState': 0}

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.countDown, True)
        ASUtils.setHitTestDisable(self.widget.millisecond, True)
        self.widget.goalOne.visible = True
        self.widget.goalTwo.visible = False
        self.widget.virtualText.visible = False

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateTargetState()
        self.updateProcessBar()
        self.updateCountDown()

    def updateProcessBar(self):
        self.widget.processBar.playSfx1.visible = False
        self.widget.processBar.playSfx2.visible = False
        ASUtils.setHitTestDisable(self.widget.processBar.bar.skilledLight, True)
        ASUtils.setHitTestDisable(self.widget.processBar.bar.timeLight, True)
        TipManager.addTipByFunc(self.widget.processBar.bar.skilledBar, self.tipSkilledBarFunction, self.widget.processBar.bar.skilledBar, False)
        TipManager.addTipByFunc(self.widget.processBar.bar.timeBar, self.tipTimeBarFunction, self.widget.processBar.bar.timeBar, False)
        TipManager.addTipByFunc(self.widget.processBar.bar.yellowCursor, self.tipSkilledBarFunction, self.widget.processBar.bar.yellowCursor, False)
        TipManager.addTipByFunc(self.widget.processBar.bar.purpleCursor, self.tipTimeBarFunction, self.widget.processBar.bar.purpleCursor, False)
        self.updateKilledValueBar(0, 0)

    def updateKilledValueBar(self, curKilledValue, totalKilledValue):
        if not self.widget:
            return
        totalBarValue = SCD.data.get('endlessProgressBar', 0)
        totalKilledValue = min(totalKilledValue, totalBarValue)
        if totalBarValue == 0:
            currBarW = 0
        else:
            currBarW = min(int(math.ceil(PROGRESS_BAR_WIDTH * totalKilledValue / totalBarValue)), PROGRESS_BAR_WIDTH)
        self.updateprocessBarInfo(self.widget.processBar.bar.skilledBarMask, self.widget.processBar.bar.skilledBar, self.widget.processBar.bar.skilledLight, self.widget.processBar.bar.yellowCursor, currBarW, currBarW > 0)
        if totalBarValue == 0:
            szPre = str(0)
        else:
            szPre = str(int(totalKilledValue * 1.0 / totalBarValue * 100))
        self.currSkilledPre = gameStrings.PROGRESS_BAR_PERCENT % (szPre, '%')
        if totalKilledValue == totalBarValue:
            self.widget.goalTwo.visible = True
            gameglobal.rds.sound.playSound(5634)

    def updateTimeCursor(self, bOver):
        if bOver:
            self.widget.processBar.bar.purpleCursor.gotoAndStop('special')
        else:
            self.widget.processBar.bar.purpleCursor.gotoAndStop('normal')

    def updateTimeValueBar(self, currTimeValue):
        totalBarValue = self.fubenData['totalTime']
        if not totalBarValue:
            currBarW = 0
        else:
            currBarW = min(int(math.ceil(PROGRESS_BAR_WIDTH * currTimeValue / totalBarValue)), PROGRESS_BAR_WIDTH)
        self.updateprocessBarInfo(self.widget.processBar.bar.timeBarMask, self.widget.processBar.bar.timeBar, self.widget.processBar.bar.timeLight, self.widget.processBar.bar.purpleCursor, currBarW, currBarW > 0)

    def updateprocessBarInfo(self, barMask, bar, light, cursor, currBarW, bShow):
        barMask.visible = bShow
        bar.visible = bShow
        light.visible = bShow
        cursor.visible = bShow
        if not bShow:
            return
        barMask.width = currBarW
        light.x = currBarW
        cursor.x = currBarW

    def updateCountDown(self):
        if not self.widget:
            self.stopTimer()
            return
        p = BigWorld.player()
        leftTimes = self.fubenData['endTime'] - p.getServerTime()
        second = int(math.floor(leftTimes))
        if second >= 0:
            if second <= COUNT_DOWN_SHOW:
                color = '#E53900'
                self.widget.millisecond.visible = True
                secondStr = str(math.modf(leftTimes)[0])
                secondStr = secondStr[2:4]
                self.widget.millisecond.text = secondStr
            else:
                color = '#ffcc30'
                self.widget.millisecond.visible = False
            self.widget.countDown.htmlText = uiUtils.toHtml(utils.formatTimeStr(second, 'm:s', True, 2, 2, 2), color)
            self.updateTimeCursor(False)
            self.timer = BigWorld.callback(0, self.updateCountDown)
        else:
            self.stopTimer()
            second = 0
            self.widget.millisecond.text = '00'
            self.updateTimeCursor(True)
        self.currTimePre = gameStrings.VOID_DREAMLAND_BAR_LEFT_TIME % utils.formatTimeStr(second, 'm:s', True, 2, 2, 2)
        self.updateTimeValueBar(p.getServerTime() - self.fubenData['startTime'])

    def updateTargetState(self):
        if not self.widget:
            return
        targetState = self.fubenData['targetState']
        if targetState == 0:
            self.updateGoalTextField(0, 'One', 'accept')
            self.updateGoalTextField(1, 'Two', 'accept')
            self.widget.bossMc.bossIcon.gotoAndStop('gray')
        elif targetState == 1:
            self.updateGoalTextField(0, 'One', 'complete')
            self.updateGoalTextField(1, 'Two', 'accept')
            self.widget.bossMc.bossIcon.gotoAndStop('appear')
        elif targetState == 2:
            self.updateGoalTextField(0, 'One', 'complete')
            self.updateGoalTextField(1, 'Two', 'complete')
            self.widget.bossMc.bossIcon.gotoAndStop('killed')

    def updateGoalTextField(self, nIndex, szStr, state):
        tLabel = SCD.data.get('endlessGoalsDescription', ())
        goal = self.widget.getChildByName('goal%s' % szStr)
        if tLabel and goal:
            self.widget.virtualText.text = tLabel[nIndex]
            numLines = self.widget.virtualText.numLines
            if numLines > 1:
                goal.gotoAndStop('duohang')
                goalAction = goal.multiLine
            else:
                goal.gotoAndStop('danhang')
                goalAction = goal.singleLine
            goalAction.gotoAndPlay(state)
            if state == 'complete':
                goalItem = goalAction.goalCompleteMc
            else:
                goalItem = goalAction.goalMc
            if nIndex == 0:
                goalItem.goalIcon.gotoAndStop('monster')
            else:
                goalItem.goalIcon.gotoAndStop('boss')
            goalItem.goalText.text = tLabel[nIndex]

    def tipSkilledBarFunction(self, *args):
        mc = ASObject(args[3][0])
        skilledStr = TipManager.getInstance().getDefaultTipMc(self.currSkilledPre)
        TipManager.showImediateTip(mc, skilledStr)

    def tipTimeBarFunction(self, *args):
        mc = ASObject(args[3][0])
        timeStr = TipManager.getInstance().getDefaultTipMc(self.currTimePre)
        TipManager.showImediateTip(mc, timeStr)

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateEndEndlessBarInfo(self):
        if not self.widget:
            return
        self.stopTimer()

    def playEffect(self):
        if not self.widget:
            return
        p = BigWorld.player()
        posX, posY = BigWorld.getWorldPosInScreen((p.position[0], p.position[1] + p.model.height, p.position[2]))
        posX -= self.widget.x
        posY -= self.widget.y
        bezierList = [{'x': posX - 50,
          'y': posY - 300}]
        tweenerInfo = {'x': 63,
         'y': 135,
         'time': 1.5,
         'transition': 'easeInCubic',
         '_bezier': bezierList}
        flyEffectMc = self.widget.getInstByClsName('VoidDreamlandBar_flyEffect')
        flyEffectMc.x = posX
        flyEffectMc.y = posY
        flyEffectMc.setTweener(tweenerInfo)
        self.widget.addChild(flyEffectMc)
        self.flyEffect = BigWorld.callback(1.5, self.udpatePlayEffect)

    def udpatePlayEffect(self):
        if not self.widget:
            return
        else:
            self.widget.processBar.playSfx1.visible = True
            self.widget.processBar.playSfx2.visible = True
            self.widget.processBar.playSfx1.gotoAndPlay(1)
            self.widget.processBar.playSfx2.gotoAndPlay(1)
            gameglobal.rds.sound.playSound(5633)
            if self.flyEffect:
                BigWorld.cancelCallback(self.flyEffect)
                self.flyEffect = None
            return

    def setFbInfo(self, info):
        if info.has_key('endless_target_state'):
            self.fubenData['targetState'] = info.get('endless_target_state')
            self.updateTargetState()
        if info.has_key('endless_time_info'):
            self.fubenData['totalTime'] = info.get('endless_time_info')[0]
            self.fubenData['startTime'] = info.get('endless_time_info')[1]
            self.fubenData['endTime'] = info.get('endless_time_info')[0] + info.get('endless_time_info')[1]
            self.show()
