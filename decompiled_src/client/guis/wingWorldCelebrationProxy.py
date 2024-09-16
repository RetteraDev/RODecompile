#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldCelebrationProxy.o
import BigWorld
import utils
import gametypes
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from data import wing_world_config_data as WWCD
from data import wing_world_celebration_reward_data as WWCRD
WING_WORLD_CAMP_CELEBRATE_ID = 99

class WingWorldCelebrationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCelebrationProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_CELEBRATION, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_CELEBRATION:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_CELEBRATION)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_CELEBRATION)
        BigWorld.player().cell.queryWingCelebrationActivityData()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            self.widget.gotoAndStop('camp')
            self.refreshCampInfo()
        else:
            self.widget.gotoAndStop('normal')
            self.refreshNormalInfo()

    def refreshNormalInfo(self):
        p = BigWorld.player()
        self.widget.helpIcon.visible = not p._isSoul()
        titleLevel = p.wingWorld.country.getOwn().titleLevel
        expireTime, totalCnt, personalCnt = getattr(p, 'celebrationActivityData', (0, 0, 0))
        consignRewardMarks = WWCRD.data.get(titleLevel, {}).get('consignRewardMarks', (100, 200, 300))
        consignRewardItems = WWCRD.data.get(titleLevel, {}).get('consignRewardItems', ((335264, 2), (335264, 3), (441757, 4)))
        self.widget.txtTotalProgerssvv.htmlText = gameStrings.WING_WORLD_CELE_DESC
        self.widget.txtCnt.htmlText = gameStrings.WING_WORLD_CELE_CURRENT_PROGRESS % personalCnt
        for i in xrange(3):
            itemMc = self.widget.getChildByName('item%d' % i)
            itemMc.dragable = False
            itemMc.setItemSlotData(uiUtils.getGfxItemById(*consignRewardItems[i]))
            progressMc = self.widget.getChildByName('progressBar%d' % i)
            minValue = consignRewardMarks[i - 1] if i - 1 >= 0 else 0
            maxValue = consignRewardMarks[i]
            progressMc.maxValue = maxValue - minValue
            progressMc.currentValue = max(0, totalCnt - minValue)
            stepMc = self.widget.getChildByName('step%d' % i)
            stepMc.visible = False

    def refreshCampInfo(self):
        p = BigWorld.player()
        self.widget.helpIcon.visible = False
        expireTime, totalCnt, personalCnt = getattr(p, 'celebrationActivityData', (0, 0, 0))
        consignRewardItems = WWCRD.data.get(WING_WORLD_CAMP_CELEBRATE_ID, {}).get('consignRewardItems', ((335264, 2), (335264, 3), (441757, 4)))
        consignRewardMarks = WWCRD.data.get(WING_WORLD_CAMP_CELEBRATE_ID, {}).get('consignRewardMarks', (100, 200, 300))
        self.widget.txtCnt.htmlText = gameStrings.WING_WORLD_CELE_CURRENT_CAMP_PROGRESS % personalCnt
        self.widget.txtTotalProgerss.htmlText = gameStrings.WING_WORLD_CELE_CAMP_DESC
        self.widget.item.dragable = False
        self.widget.item.setItemSlotData(uiUtils.getGfxItemById(*consignRewardItems[0]))
        self.widget.step.visible = False
        self.widget.progressBar.lableVisible = True
        self.widget.progressBar.maxValue = consignRewardMarks[0]
        self.widget.progressBar.currentValue = max(0, totalCnt)

    def addPushMsg(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableWingCelebrationActivity', False):
            return
        if p.lv < WWCD.data.get('enterWingWorldMapMinLevel', 69):
            return
        if p.wingWorld.step != gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
            return
        expireTime, totalCnt, personalCnt = getattr(p, 'celebrationActivityData', (0, 0, 0))
        if utils.getNow() > expireTime:
            return
        if uiConst.MESSAGE_TYPE_WING_WORLD_CELEBRATION in self.uiAdapter.pushMessage.msgs:
            return
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CELEBRATION)
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_CELEBRATION, {'click': self.show})
        self.timer = BigWorld.callback(expireTime - utils.getNow(), self.removePushMsg)

    def removePushMsg(self):
        self.timer = None
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CELEBRATION)
