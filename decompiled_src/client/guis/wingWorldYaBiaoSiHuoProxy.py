#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldYaBiaoSiHuoProxy.o
import BigWorld
import gamelog
import uiConst
import events
import gametypes
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import wing_world_config_data as WWCFD
from data import wing_world_yabiao_private_goods_bonus as WWYPGB
RADIO_MAX_CTN = 4

class WingWorldYaBiaoSiHuoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldYaBiaoSiHuoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_YABIAO_SIHUO, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_YABIAO_SIHUO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_YABIAO_SIHUO)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_YABIAO_SIHUO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.txtTitile, True)
        self.widget.txtDesc.htmlText = WWCFD.data.get('yaBiaoSiHuoDesc', 'yaBiaoSiHuoDesc')
        self.widget.radio0.selected = False
        wingWorldYaBiaoDescs = WWCFD.data.get('yaBiaoSiHuoDescs', ['%d'] * 4)
        self.widget.radio0.label = wingWorldYaBiaoDescs[0] % WWYPGB.data.get(gametypes.WING_WORLD_YABIAO_PRIVATE_GOODS_ONE, {}).get('costCash', 100)
        self.widget.radio1.selected = False
        self.widget.radio1.label = wingWorldYaBiaoDescs[1] % WWYPGB.data.get(gametypes.WING_WORLD_YABIAO_PRIVATE_GOODS_TWO, {}).get('costCash', 200)
        self.widget.radio2.selected = False
        self.widget.radio2.label = wingWorldYaBiaoDescs[2] % WWYPGB.data.get(gametypes.WING_WORLD_YABIAO_PRIVATE_GOODS_THREE, {}).get('costCash', 300)
        self.widget.radio3.selected = False
        self.widget.radio3.label = wingWorldYaBiaoDescs[3] % WWYPGB.data.get(gametypes.WING_WORLD_YABIAO_PRIVATE_GOODS_FOUR, {}).get('coinCash', 400)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleConfirmBtnClick(self, *args):
        for i in xrange(RADIO_MAX_CTN):
            radio = getattr(self.widget, 'radio%d' % i)
            if radio.selected:
                p = BigWorld.player()
                gamelog.info('jbx:applyCarryWingWorldYabiaoPrivateGoods', p.wingWorldYabiaoData.yabiaoEntId, i + 1)
                BigWorld.player().cell.applyCarryWingWorldYabiaoPrivateGoods(p.wingWorldYabiaoData.yabiaoEntId, i + 1)
                self.hide()
                return
