#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldPreTaskTipProxy.o
import time
import BigWorld
import formula
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from data import wing_world_config_data as WWCD
QUERY_INTERVAL = 5
OFFSET_SECONDS = 60

class WingWorldPreTaskTipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldPreTaskTipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handle = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WINGWORLD_PRETASK_TIP, self.hide)

    def reset(self):
        self.damageVal = 0
        self.cureVal = 0
        self.donateVal = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WINGWORLD_PRETASK_TIP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.handle and BigWorld.cancelCallback(self.handle)
        self.handle = None
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WINGWORLD_PRETASK_TIP)

    def show(self, damageVal = 0, cureVal = 0):
        if damageVal or cureVal:
            self.updateVal(damageVal, cureVal)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WINGWORLD_PRETASK_TIP)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.startRefreshTimer()

    def startRefreshTimer(self):
        self.handle and BigWorld.cancelCallback(self.handle)
        curTime, _, destroyWWBossTime = self.getTimeInfo()
        if curTime < destroyWWBossTime + OFFSET_SECONDS:
            needQuery = int((destroyWWBossTime - curTime) % QUERY_INTERVAL) == 0
            needQuery and BigWorld.player().cell.queryWingWorldBossStats()
            self.refreshInfo()
            self.handle = BigWorld.callback(1, self.startRefreshTimer)
        else:
            self.refreshInfo()
            self.handle = None

    def refreshInfo(self):
        if not self.widget:
            return
        curTime, createWWBossTime, destroyWWBossTime = self.getTimeInfo()
        self.widget.tf_time.text = self.getTimeString(curTime, createWWBossTime, destroyWWBossTime)
        self.widget.tf_damage.text = self.damageVal
        self.widget.tf_cure.text = self.cureVal
        self.widget.tf_donate.text = self.donateVal

    def updateVal(self, damageVal, cureVal):
        calcDonateformulaId = WWCD.data.get('calcBossDonateFormulaId', 0)
        if not calcDonateformulaId:
            donateVal = 0
        else:
            donateVal = formula.calcFormulaById(calcDonateformulaId, {'damageVal': damageVal,
             'cureVal': cureVal})
        self.damageVal = damageVal
        self.cureVal = cureVal
        self.donateVal = int(donateVal)

    def getTimeString(self, curTime, createTime, destroyTime):
        if curTime < createTime:
            return ''
        elif curTime > destroyTime:
            return ''
        else:
            return time.strftime('%M:%S', time.localtime(destroyTime - curTime))

    def getTimeInfo(self):
        p = BigWorld.player()
        curTime = p.getServerTime()
        createWWBossTime = getattr(p, 'createWWBossTime', curTime)
        destroyWWBossTime = getattr(p, 'destroyWWBossTime', createWWBossTime + const.TIME_INTERVAL_HOUR)
        return (curTime, createWWBossTime, destroyWWBossTime)

    def _onRankBtnClick(self, e):
        gameglobal.rds.ui.bossDamageRank.show()
