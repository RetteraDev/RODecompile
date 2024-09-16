#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteRemarkProxy.o
import BigWorld
import uiConst
from helpers import taboo
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteRemarkProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteRemarkProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteName = ''
        self.spriteIndex = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_REMARK, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_REMARK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_REMARK)

    def reset(self):
        self.spriteName = ''
        self.spriteIndex = -1

    def show(self, spriteIndex, spriteName):
        self.spriteIndex = spriteIndex
        self.spriteName = spriteName
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_REMARK, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.fName.text = self.spriteName

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        name = self.widget.remark.text
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            self.widget.remark.text = ''
            p.showGameMsg(GMDD.data.SPRITE_REMARK_TABOO_WORD, ())
        else:
            p.base.renameSummonedSprite(self.spriteIndex, name)
            self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()
