#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjSpriteEnterProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import ui
import const
from uiProxy import UIProxy
from data import zmj_fuben_config_data as ZFCD

class ZmjSpriteEnterProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjSpriteEnterProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_SPRITE_ENTER, self.hide)

    def reset(self):
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_SPRITE_ENTER:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_SPRITE_ENTER)

    def show(self):
        if not gameglobal.rds.configData.get('enableZMJAssist', False):
            return
        p = BigWorld.player()
        if p.isFbAssister or not p.zmjData:
            return
        bossStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        assistMinStar = ZFCD.data.get('assistMinStar', 10)
        if bossStar < assistMinStar:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_SPRITE_ENTER)

    def initUI(self):
        self.widget.callBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCallBtn, False, 0, True)

    @ui.callInCD(2.5)
    def handleClickCallBtn(self, *args):
        gameglobal.rds.ui.zmjSpriteInvite.show()
