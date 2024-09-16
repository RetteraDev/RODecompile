#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteReleaseProxy.o
import BigWorld
import uiConst
import gameglobal
import const
from uiProxy import UIProxy
from guis import uiUtils
from data import summon_sprite_info_data as SSID
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteReleaseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteReleaseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RELEASE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_RELEASE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RELEASE)

    def reset(self):
        self.spriteIndex = None

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RELEASE, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.titleText.text = SCD.data.get('spriteReleaseTitleText', '')
        self.widget.help.helpKey = SCD.data.get('spriteReleaseHelpKey', 0)
        spriteInfo = gameglobal.rds.ui.summonedWarSpriteMine.getCurSelectSpriteInfo()
        skillInfo = spriteInfo.get('skills', {})
        naturals = skillInfo.get('naturals', [])
        if len(naturals) >= const.SSPRITE_NATURAM_SKILL_NUM_LIMIT:
            self.widget.releaseTip.visible = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SUMMONED_SPRITE_RELEASE_TIP, '')
            self.widget.releaseTip.text = tip
        else:
            self.widget.releaseTip.visible = False
            self.widget.releaseDesc1.y = 80
            self.widget.releaseDesc2.y = 135
            self.widget.icon.y = 138
        newName = spriteInfo.get('name', '')
        lv = int(spriteInfo.get('props', {}).get('lv', 0))
        spriteId = spriteInfo.get('spriteId', 0)
        oldName = SSID.data.get(spriteId, {}).get('name', '')
        desc1 = SCD.data.get('spritereleaseDesc1', '%s(%s,%d)') % (newName, oldName, lv)
        self.widget.releaseDesc1.htmlText = desc1
        self.widget.releaseDesc2.htmlText = SCD.data.get('spritereleaseDesc2', '')

    def _onReleaseBtnClick(self, e):
        spriteInfo = gameglobal.rds.ui.summonedWarSpriteMine.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        familiar = int(props.get('familiar', 0))
        famiExp = int(props.get('famiExp', 0))
        exp = int(props.get('exp', 0))
        lv = int(props.get('lv', 0))
        if familiar > 1 or famiExp > 0 or lv > 1 or exp > 0:
            gameglobal.rds.ui.doubleCheckWithInput.show(SCD.data.get('spriteSureDeleteDesc', ''), 'DELETE', title=SCD.data.get('spriteSureDeleteTitle', ''), confirmCallback=self.confirmBtnCallback, cancelCallback=self.hide)
        else:
            self.confirmBtnCallback()

    def _onCancelBtnClick(self, e):
        self.hide()

    def confirmBtnCallback(self):
        gameglobal.rds.ui.summonedWarSpriteMine.sureRemoveSprite(self.spriteIndex)
        self.hide()
