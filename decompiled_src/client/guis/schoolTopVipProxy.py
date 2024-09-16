#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopVipProxy.o
import BigWorld
import utils
import const
import gameglobal
import uiConst
import events
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import school_top_config_data as STCD
from cdata import game_msg_def_data as GMDD

class SchoolTopVipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopVipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_VIP, self.hide)

    def reset(self):
        pass

    @property
    def selfData(self):
        p = BigWorld.player()
        return p.getSelfCandidateData()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_VIP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def getVipExpiredTime(self):
        serviceExpire = self.selfData.get('serviceExpire', 0)
        return max(utils.getNow(), serviceExpire)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_VIP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_VIP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.numPaper.maximum = self.getCanBuyMaxDays()
        self.widget.numPaper.addEventListener(events.INDEX_CHANGE, self.handleNumChange, False, 0, True)
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.coinIcon.bonusType = 'yunChui'

    def getCanBuyMaxDays(self):
        startDayInt = utils.getWeekInt(utils.getNow())
        if self.getVipExpiredTime() > utils.getNow():
            startDayInt = utils.getWeekInt(self.getVipExpiredTime())
        return 6 - startDayInt

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshDesc()

    def handleNumChange(self, *args):
        self.refreshDesc()

    def refreshDesc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        expiredTime = self.getVipExpiredTime()
        if not self.widget.numPaper.value:
            expiredTime = self.getVipExpiredTime() - 1
        elif expiredTime <= utils.getNow():
            expiredTime = utils.getNow() + (self.widget.numPaper.value - 1) * 24 * 60 * 60
        else:
            expiredTime = expiredTime - 1 + self.widget.numPaper.value * 24 * 60 * 60
        if expiredTime <= utils.getNow() and not bool(self.widget.numPaper.value):
            self.widget.txtDesc.text = gameStrings.SCHOOL_TOP_BUY_VIP_EXPIRED % self.getCanBuyMaxDays()
        else:
            hourInt = 24
            if utils.getWeekInt(expiredTime) == 5:
                hourInt = utils.getHourInt(utils.getNextCrontabTime(STCD.data.get('matchStartTime', '15 19 * * 5')))
            self.widget.txtDesc.text = gameStrings.SCHOOL_TOP_BUY_VIP % (self.getCanBuyMaxDays(),
             utils.getMonthInt(expiredTime),
             utils.getMonthDayInt(expiredTime),
             hourInt)
        broadcastPrice = STCD.data.get('broadcastPrice', 100)
        needFame = int(broadcastPrice * int(self.widget.numPaper.value))
        self.widget.txtCache.text = '%d/%d' % (needFame, p.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0))

    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        broadcastPrice = STCD.data.get('broadcastPrice', 100)
        needFame = int(broadcastPrice * int(self.widget.numPaper.value))
        totalFame = p.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0)
        if totalFame < needFame:
            p.showGameMsg(GMDD.data.NOT_ENOUGH_YUNCHUI_SCORE)
        p = BigWorld.player()
        p.cell.buySchoolTopBroadcastService(int(self.widget.numPaper.value))
