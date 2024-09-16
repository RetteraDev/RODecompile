#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteLunhuiSureProxy.o
import BigWorld
import uiConst
import ui
import events
import skillDataInfo
import utils
import const
import tipUtils
from guis import uiUtils
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from cdata import item_coin_dikou_cost_data as ICDCD
from cdata import summon_sprite_bonus_skill_data as SSBSD
MAX_ALL_CONSUME_TYPE = 3
SPRITE_SKILL_SIGN_ID = 100

class SummonedWarSpriteLunhuiSureProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteLunhuiSureProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.consumeType = 0
        self.isDiKouItem = True
        self.checkOnceMap = {}
        self.checkOnceType = None
        self.bonusId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_SURE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_SURE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_SURE)

    def reset(self):
        self.spriteIndex = None
        self.consumeType = 0
        self.isDiKouItem = True
        self.bonusId = 0

    def show(self, spriteIndex, consumeType, isDiKouItem, checkOnceType = None, bonusId = 0):
        self.spriteIndex = spriteIndex
        self.consumeType = consumeType
        self.isDiKouItem = isDiKouItem
        self.checkOnceType = checkOnceType
        self.bonusId = bonusId
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_SURE, True)

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        rareLv = spriteInfo.get('rareLv', 0)
        ssidData = SSID.data.get(spriteId, {})
        lunhuiCostCash = ssidData.get('lunhuiCostCash', 0)
        lunhuiCostItems = ssidData.get('lunhuiCostItems', (0, 0))
        itemId = lunhuiCostItems[0]
        needItemNum = lunhuiCostItems[1]
        hadItemNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        itemCoinData = ICDCD.data.get(itemId, [0, 0])
        diKouCost = itemCoinData[1]
        itemNumDiff = max(0, needItemNum - hadItemNum)
        needDikouConst = itemNumDiff * diKouCost
        if self.bonusId:
            self.widget.hasBonusPanel.visible = True
            self.widget.noneBonusPanel.visible = False
            self.updateSkillSlot(self.widget.hasBonusPanel, spriteInfo)
            self.updateConsumeMc(self.widget.hasBonusPanel, itemId, needItemNum, hadItemNum, lunhuiCostCash, needDikouConst)
            limit = SCD.data.get('spriteLunhuiBonusOccurrencesLimit', {}).get(rareLv, 30)
            self.widget.hasBonusPanel.bonusDesc.text = gameStrings.SPRITE_LUNHUI_BONUS_SUB_DESC % limit
        else:
            self.widget.hasBonusPanel.visible = False
            self.widget.noneBonusPanel.visible = True
            self.widget.noneBonusPanel.checkBox.addEventListener(events.EVENT_SELECT, self.onCheckBox, False, 0, True)
            self.updateConsumeMc(self.widget.noneBonusPanel, itemId, needItemNum, hadItemNum, lunhuiCostCash, needDikouConst)

    def updateSkillSlot(self, bonusPanel, spriteInfo):
        talentCombo = SSBSD.data.get(self.bonusId, {}).get('talentCombo', ())
        famiLv = spriteInfo.get('props', {}).get('famiEffLv', 1)
        for i in xrange(len(talentCombo)):
            skillSlot = bonusPanel.getChildByName('skillSlot%d' % i)
            skillType = talentCombo[i]
            skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
            if skillId:
                universalLabel = SSSD.data.get(skillType, {}).get('universalLabel', 0)
                signId = universalLabel if universalLabel else SPRITE_SKILL_SIGN_ID
                skillSlot.cornerPic.gotoAndStop('sign_%d' % signId)
                lv = utils.getEffLvBySpriteFamiEffLv(famiLv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
                skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
                iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                skillSlot.slot.fitSize = True
                skillSlot.slot.dragable = False
                skillSlot.slot.setItemSlotData({'iconPath': iconPath})
                skillSlot.slot.validateNow()
                TipManager.addTipByType(skillSlot.slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': lv}, False, 'upLeft')

        bonusName = SSSD.data.get(self.bonusId, {}).get('bonusName', '')
        bonusPanel.bonusIcon.bonusDesc1.text = bonusName

    def updateConsumeMc(self, bonusPanel, itemId, needItemNum, hadItemNum, lunhuiCostCash, needDikouConst):
        bonusPanel.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        bonusPanel.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        bonusPanel.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        bonusPanel.help.helpKey = SCD.data.get('spriteLunhuiSureHelpKey', 0)
        for i in range(MAX_ALL_CONSUME_TYPE):
            consumeMc = bonusPanel.getChildByName('consumeMc%d' % i)
            consumeMc.visible = i == self.consumeType

        consumeMc = bonusPanel.getChildByName('consumeMc%d' % self.consumeType)
        if self.consumeType == uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE2:
            self.updateConsumeMcType2(consumeMc, itemId, needItemNum, hadItemNum, lunhuiCostCash, needDikouConst)
        elif self.consumeType == uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE1:
            self.updateConsumeMcType1(consumeMc, lunhuiCostCash, needDikouConst)
        else:
            self.updateConsumeMcType0(consumeMc, itemId, needItemNum, hadItemNum, lunhuiCostCash)

    def getCheckOnceData(self, type):
        return self.checkOnceMap.get(type, False)

    def onCheckBox(self, *arg):
        checkBoxSelect = self.widget.noneBonusPanel.checkBox.selected
        if self.checkOnceType:
            self.checkOnceMap[self.checkOnceType] = checkBoxSelect

    @ui.checkInventoryLock()
    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        if self.bonusId:
            p.base.applySpritePrayLunhui(self.spriteIndex, self.bonusId, self.isDiKouItem, p.cipherOfPerson)
        else:
            p.base.applyLunhuiSprite(self.spriteIndex, self.isDiKouItem, p.cipherOfPerson)
        self.hide()

    def handleCloseBtnClick(self, *args):
        self.hide()

    def updateConsumeMcType2(self, consumeMc, itemId, needItemNum, hadItemNum, lunhuiCostCash, needDikouConst):
        consumeMc.itemSlot.dragable = False
        itemInfo = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(hadItemNum, needItemNum))
        consumeMc.itemSlot.setItemSlotData(itemInfo)
        consumeMc.cashT.text = lunhuiCostCash
        consumeMc.tianbiT.text = needDikouConst

    def updateConsumeMcType1(self, consumeMc, lunhuiCostCash, needDikouConst):
        consumeMc.cashT.text = lunhuiCostCash
        consumeMc.tianbiT.text = needDikouConst

    def updateConsumeMcType0(self, consumeMc, itemId, needItemNum, hadItemNum, lunhuiCostCash):
        consumeMc.itemSlot.dragable = False
        itemInfo = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(hadItemNum, needItemNum))
        consumeMc.itemSlot.setItemSlotData(itemInfo)
        consumeMc.cashT.text = lunhuiCostCash
