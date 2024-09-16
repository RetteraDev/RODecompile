#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteMsgProxy.o
import BigWorld
import uiConst
import const
import gameglobal
from guis import uiUtils
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID

class SummonedWarSpriteMsgProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteMsgProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedIndex = None
        self.learnsPart = None
        self.isLuckilyTry = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_MSG, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_MSG:
            self.widget = widget
            self.initUI()
            self.refreshAll()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_MSG)

    def reset(self):
        self.selectedIndex = None
        self.learnsPart = None

    def show(self, selectedIndex, learnsPart):
        self.selectedIndex = selectedIndex
        self.learnsPart = learnsPart
        self.isLuckilyTry = False
        if self.widget:
            self.refreshAll()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_MSG, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshAll(self):
        self.refreshRadioBtn()
        self.refreshMainInfo()

    def refreshRadioBtn(self):
        dirRBtn = self.widget.directLearnSkillRadioBtn
        luckyRBtn = self.widget.luckyLearnSkillRadioBtn
        dirRBtn.validateNow()
        luckyRBtn.validateNow()
        dirRBtn.groupName = 'summonedWarSpriteLearnSkillCheck'
        luckyRBtn.groupName = 'summonedWarSpriteLearnSkillCheck'
        dirRBtn.selected = not self.isLuckilyTry
        luckyRBtn.selected = self.isLuckilyTry
        dirRBtn.addEventListener(events.BUTTON_CLICK, self.handleRadioBtnCheckClick, False, 0, True)
        luckyRBtn.addEventListener(events.BUTTON_CLICK, self.handleRadioBtnCheckClick, False, 0, True)
        spriteSkillSlotLuckyUnlockEnabled = gameglobal.rds.configData.get('enableSpriteSkillLuckyUnlock', False)
        dirRBtn.visible = spriteSkillSlotLuckyUnlockEnabled
        luckyRBtn.visible = spriteSkillSlotLuckyUnlockEnabled
        self.widget.centerHintTxt.text = gameStrings.SUMMONED_WAR_SPRITE_SKILL_SLOT_UNLOCK_SELECT_HINT if spriteSkillSlotLuckyUnlockEnabled else gameStrings.SUMMONED_WAR_SPRITE_SKILL_SLOT_UNLOCK_HINT

    def handleRadioBtnCheckClick(self, *args):
        e = ASObject(args[3][0])
        radioBtnMc = e.currentTarget
        if str(radioBtnMc.name) == 'directLearnSkillRadioBtn':
            self.isLuckilyTry = False
            radioBtnMc.selected = not self.isLuckilyTry
        elif str(radioBtnMc.name) == 'luckyLearnSkillRadioBtn':
            self.isLuckilyTry = True
            radioBtnMc.selected = self.isLuckilyTry
        self.refreshMainInfo()

    def refreshMainInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.selectedIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        itemNeeds = SSID.data.get(spriteId, {}).get('learnsSkillConsumeItems', ())
        cashNeeds = SSID.data.get(spriteId, {}).get('learnsSkillSpendCash', ())
        if len(itemNeeds) != const.SSPRITE_LEARN_SKILL_LIMIT or len(cashNeeds) != const.SSPRITE_LEARN_SKILL_LIMIT:
            return
        itemId = itemNeeds[self.learnsPart][0]
        if self.isLuckilyTry:
            needNum = SCD.data.get('learnSpriteSkillSlotTryluckItemNum', 1)
            needValue = SCD.data.get('learnSkillTryluckCash', 500)
        else:
            needNum = itemNeeds[self.learnsPart][1]
            needValue = cashNeeds[self.learnsPart]
        ownNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        if ownNum < needNum:
            strNum = uiUtils.toHtml(ownNum, '#FF0000')
        else:
            strNum = uiUtils.toHtml(ownNum, '#FFFFE6')
        count = str('%s/%d' % (strNum, needNum))
        self.widget.itemMc.slot.dragable = False
        self.widget.itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, count=count))
        self.widget.spendIcon.bonusType = SCD.data.get('spendIconType', 'bindCash')
        self.widget.valueText.text = needValue
        if ownNum >= needNum and p.bindCash + p.cash >= needValue:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        p.base.freeForbiddenLearnSlot(self.selectedIndex, self.learnsPart, self.isLuckilyTry)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()
