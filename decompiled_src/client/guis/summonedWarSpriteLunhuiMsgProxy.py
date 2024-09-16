#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteLunhuiMsgProxy.o
import BigWorld
import uiConst
import ui
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from data import summon_sprite_info_data as SSID

class SummonedWarSpriteLunhuiMsgProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteLunhuiMsgProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_MSG, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_MSG:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_MSG)

    def reset(self):
        self.spriteIndex = None

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_MSG, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spriteName = spriteInfo.get('name', '')
        propsLunhui = spriteInfo.get('propsLunhui', {})
        props = spriteInfo.get('props', {})
        lv = int(props.get('lv', 0))
        ssidData = SSID.data.get(spriteId, {})
        name = ssidData.get('name', '')
        self.widget.spriteNameT.text = gameStrings.SPRITE_LUNHUI_MSG_NAME % (spriteName, name, lv)
        self.updateLunhuiSkillMc(propsLunhui, props)

    @ui.checkInventoryLock()
    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        p.base.submitLunhuiResult(self.spriteIndex, p.cipherOfPerson)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def updateLunhuiSkillMc(self, propsLunhui, props):
        naturals = propsLunhui.get('naturals', [])
        bonus = propsLunhui.get('bonus', [])
        gameglobal.rds.ui.summonedWarSpriteLunhui.updateSkillMc(self.widget.talentSkillMc, naturals, bonus, props)
