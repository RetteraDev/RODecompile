#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cheerProxy.o
import BigWorld
import gameglobal
import events
import uiConst
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from data import wing_world_config_data as WWCD

class CheerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CheerProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CHEER, self.hide)

    def reset(self):
        self.roundNo = 0
        self.matchNo = 0
        self.groupNUID = 0
        self.teamName = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CHEER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CHEER)

    def show(self, roundNo = 0, matchNo = 0, groupNUID = 0, teamName = ''):
        self.roundNo = roundNo
        self.matchNo = matchNo
        self.groupNUID = groupNUID
        self.teamName = teamName
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CHEER)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirm, False, 0, True)
        self.widget.confirmInfo.text = gameStrings.WING_WORLD_CHEER_TIP % self.teamName

    def onConfirm(self, *args):
        p = BigWorld.player()
        p.base.inspireWingWorldXinMoArena(self.roundNo, self.matchNo, self.groupNUID)
        self.clearWidget()

    def refreshInfo(self):
        if not self.widget:
            return
        awardItemId = WWCD.data.get('xinmoCheerAwardItemId', 0)
        self.widget.itemSlot.dragable = False
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(awardItemId))
