#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousRecordProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import utils
import clientUtils
from uiProxy import UIProxy
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import ui_help_data as UHD
from data import famous_general_config_data as FGCD
from cdata import famous_general_reacord_data as FGRD
RECORD_NUM = 12

class FamousRecordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousRecordProxy, self).__init__(uiAdapter)
        self.widget = None
        self.recordInfo = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_RECORD, self.hidePanel)

    def hidePanel(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.recordInfo = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_RECORD)

    def show(self):
        if self.widget:
            self.refreshPanel()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_RECORD)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.refreshPanel()

    def refreshPanel(self):
        if not self.widget:
            return
        data = FGRD.data
        for i in xrange(self.recordInfo['currentRound'], RECORD_NUM):
            num = i + 1
            item = self.widget.getChildByName('item%d' % i)
            item.gotoAndStop('hui')
            item.state.gotoAndStop('not')
            item.getIntro.visible = False
            item.lastWeek.visible = False
            item.redBg.visible = False
            item.notGet.visible = False
            item.getBtn.visible = False
            currentProgress = 0
            item.check.enabled = False
            item.currentProgress.text = gameStrings.FAMOUS_RECORD_CURRENT_PROGRESS % (currentProgress, FGRD.data.get(num, {}).get('topNum', 0))

        for i in xrange(0, RECORD_NUM):
            num = i + 1
            itemData = data[num]
            item = self.widget.getChildByName('item%d' % i)
            item.title.text = itemData.get('recordName', '')
            itemBonus = clientUtils.genItemBonus(itemData.get('bonusId', 0))
            itemInfo = uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])
            item.icon.setItemSlotData(itemInfo)
            isReach = self.isCurrentNumReach(num)
            item.check.data = {'num': num,
             'isReach': isReach}
            item.check.addEventListener(events.MOUSE_CLICK, self.handleClickCheck)
            item.require.text = itemData.get('ruleTxt', '')

        for i in xrange(0, self.recordInfo['currentRound']):
            if i == RECORD_NUM:
                break
            num = i + 1
            item = self.widget.getChildByName('item%d' % i)
            item.gotoAndStop('normal')
            currentProgress = self.recordInfo.get('rankNumDict', {}).get(num, 0)
            item.currentProgress.text = gameStrings.FAMOUS_RECORD_CURRENT_PROGRESS % (currentProgress, FGRD.data.get(num, {}).get('topNum', 0))
            isReach = self.isCurrentNumReach(num)
            if num != self.recordInfo['currentRound']:
                item.state.gotoAndStop('end')
            else:
                item.state.gotoAndStop('in')
            if num in self.recordInfo.get('canApplyRewardList', []):
                item.getBtn.visible = True
                item.getBtn.data = num
                item.notGet.visible = False
                item.lastWeek.visible = False
                item.redBg.visible = False
                item.getIntro.visible = False
                item.getBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGet)
            elif num in self.recordInfo.get('alreadyApplyRewardList', []):
                item.getBtn.visible = False
                item.getIntro.visible = False
                item.lastWeek.visible = False
                item.redBg.visible = False
                item.notGet.visible = True
                item.notGet.text = gameStrings.FAMOUS_RECORD_HAS_APPLYED
            else:
                item.getBtn.visible = False
                item.getIntro.visible = False
                item.lastWeek.visible = False
                item.redBg.visible = False
                item.notGet.visible = True
                item.notGet.text = gameStrings.FAMOUS_RECORD_NOT_GET
            if num == self.recordInfo['currentRound']:
                item.notGet.visible = False
                item.getIntro.visible = True
                item.lastWeek.visible = True
                item.redBg.visible = True
                item.getBtn.visible = False
                item.lastWeek.text = gameStrings.FAMOUS_RECORD_LAST_WEEK % self.getLastDays(self.recordInfo.get('currentWeek', 0), num, isReach)

        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        self.widget.question.addEventListener(events.MOUSE_CLICK, self.handleClickQuestion)

    def isCurrentNumReach(self, num):
        isReach = False
        currentProgress = self.recordInfo.get('rankNumDict', {}).get(num, 0)
        if currentProgress == FGRD.data.get(num, {}).get('topNum', 0):
            isReach = True
        return isReach

    def getLastDays(self, currentWeek, num, isReach):
        now = utils.getNow()
        currentWeekDay = utils.localtimeEx(now).tm_wday
        currentHours = utils.localtimeEx(now).tm_hour
        lastWeek = FGRD.data.get(num, {}).get('lastWeek', 0) - currentWeek
        if isReach:
            lastWeek = 1
        if currentWeekDay <= 1:
            if currentWeekDay == 1 and currentHours >= 12:
                days = lastWeek * 7 - currentWeekDay + 1
            else:
                days = lastWeek * 7 - currentWeekDay - 6
        else:
            days = lastWeek * 7 - currentWeekDay + 1
        return days

    def handleClickCheck(self, *args):
        target = ASObject(args[3][0]).currentTarget
        gameglobal.rds.ui.famousRecordCommList.show(int(target.data['num']), isReach=int(target.data['isReach']))

    def handleClickGet(self, *args):
        target = ASObject(args[3][0]).currentTarget
        BigWorld.player().cell.applyFamousGeneralReward(int(target.data))

    def handleHidePanel(self, *args):
        self.clearWidget()

    def handleClickQuestion(self, *args):
        famousRecordHelpId = FGCD.data.get('famousRecordHelpId', 0)
        keyword = UHD.data.get(famousRecordHelpId, {}).get('keyword', '')
        gameglobal.rds.ui.help.show(keyword)
