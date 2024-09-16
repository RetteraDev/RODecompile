#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteLunhuiProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import uiConst
import events
import utils
import skillDataInfo
import tipUtils
import gamelog
import ui
import gameglobal
from guis import uiUtils
from uiProxy import UIProxy
from asObject import ASUtils
from callbackHelper import Functor
from gameStrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from cdata import item_coin_dikou_cost_data as ICDCD
from cdata import game_msg_def_data as GMDD
SPRITE_SKILL_SIGN_ID = 100
BONUS_POINT_TYPE0 = 0
BONUS_POINT_TYPE1 = 1
BONUS_POINT_TYPE2 = 2
MAX_TALENT_NUM = 4
MAX_BONUS_NUM = 2

class SummonedWarSpriteLunhuiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteLunhuiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.dropDownBonusList = []
        self.isBonus = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI)
        self.uiAdapter.summonedWarSpriteLunhuiItems.hide()

    def reset(self):
        self.spriteIndex = None
        self.dropDownBonusList = []
        self.isBonus = False

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteLunhuiHelpKey', 0)
        self.widget.checkBox.selected = True
        self.widget.checkBox.addEventListener(events.MOUSE_CLICK, self.handleSelectCheckBox, False, 0, True)
        self.widget.dropDownBonus.addEventListener(events.INDEX_CHANGE, self.handleDropDwonBonus, False, 0, True)
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        ssidData = SSID.data.get(spriteId, {})
        prayBonusIds = list(ssidData.get('prayBonusIds', ()))
        prayBonusIds.insert(0, 0)
        self.dropDownBonusList = []
        for i, bonusId in enumerate(prayBonusIds):
            bonusName = SSSD.data.get(bonusId, {}).get('bonusName', gameStrings.TEXT_SUMMONEDWARSPRITELUNHUIPROXY_87)
            typeInfo = {}
            typeInfo['label'] = bonusName
            typeInfo['typeIndex'] = i
            typeInfo['bonusId'] = bonusId
            self.dropDownBonusList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.dropDownBonus, self.dropDownBonusList)
        self.widget.dropDownBonus.menuRowCount = len(self.dropDownBonusList)
        if self.widget.dropDownBonus.selectedIndex == -1:
            self.widget.dropDownBonus.selectedIndex = 0
        tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_LUNHUI_LUCKY_BAR_TIP, '')
        TipManager.addTip(self.widget.luckyBar, tip)
        TipManager.addTip(self.widget.luckyValT, tip)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateSpriteLunhui(self.spriteIndex)

    def handleSelectCheckBox(self, *args):
        self.updateLunhuiBtnState()

    @ui.checkInventoryLock()
    def _onSaveBtnClick(self, e):
        if not self.spriteIndex:
            return
        gameglobal.rds.ui.summonedWarSpriteLunhuiMsg.show(self.spriteIndex)

    def _onLunhuiBtnClick(self, e):
        if not self.spriteIndex:
            return
        else:
            p = BigWorld.player()
            isDiKouItem = self.widget.checkBox.selected
            selectedIndex = self.widget.dropDownBonus.selectedIndex
            spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
            rareLv = spriteInfo.get('rareLv', 0)
            bonusOccurrences = spriteInfo.get('bonusOccurrences', 0)
            limit = SCD.data.get('spriteLunhuiBonusOccurrencesLimit', {}).get(rareLv, 30)
            if selectedIndex and bonusOccurrences >= limit:
                bonusId = self.dropDownBonusList[selectedIndex]['bonusId']
                lunhuiBtn = e.target
                needItems = lunhuiBtn.needItems
                hadItems = lunhuiBtn.hadItems
                consumeType = self.getConsumeType(needItems, hadItems, isDiKouItem)
                gameglobal.rds.ui.summonedWarSpriteLunhuiSure.show(self.spriteIndex, consumeType, isDiKouItem, None, bonusId)
                return
            if not gameglobal.rds.ui.summonedWarSpriteLunhuiSure.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_LUNHUI):
                lunhuiBtn = e.target
                needItems = lunhuiBtn.needItems
                hadItems = lunhuiBtn.hadItems
                consumeType = self.getConsumeType(needItems, hadItems, isDiKouItem)
                gameglobal.rds.ui.summonedWarSpriteLunhuiSure.show(self.spriteIndex, consumeType, isDiKouItem, uiConst.CHECK_ONCE_TYPE_SPRITE_LUNHUI)
            else:
                p = BigWorld.player()
                spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
                propsLunhui = spriteInfo.get('propsLunhui', {})
                bonus = propsLunhui.get('bonus', [])
                if len(bonus) > 0:
                    msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_LUNHUI_CONTINUE_MSG, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realLunhui, isDiKouItem), yesBtnText=gameStrings.SPRITE_LUNHUI_MES_BOX_YES, noBtnText=gameStrings.SPRITE_LUNHUI_MES_BOX_NO)
                else:
                    self.realLunhui(isDiKouItem)
            return

    @ui.checkInventoryLock()
    def realLunhui(self, isDiKouItem):
        p = BigWorld.player()
        p.base.applyLunhuiSprite(self.spriteIndex, isDiKouItem, p.cipherOfPerson)

    def _onGetBtnClick(self, e):
        gameglobal.rds.ui.summonedWarSpriteLunhuiItems.show(self.spriteIndex)

    def handleDropDwonBonus(self, *args):
        pass

    def getConsumeType(self, needItems, hadItems, isDiKouItem):
        if not isDiKouItem:
            return uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE0
        elif hadItems >= needItems:
            return uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE0
        elif hadItems > 0:
            return uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE2
        else:
            return uiConst.SUMMONED_LUNHUI_COUNSUME_TYPE1

    def updateLunhuiBtnState(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        self.updateConsumeItemMC(spriteInfo)

    def updateSpriteLunhui(self, index):
        if not self.widget:
            return
        if index != self.spriteIndex:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        propsLunhui = spriteInfo.get('propsLunhui', {})
        props = spriteInfo.get('props', {})
        spriteName = spriteInfo.get('name', '')
        self.widget.spriteNameT.text = spriteName
        if not propsLunhui:
            self.hideAfterLunhuiDesc()
        else:
            self.updateAfterLunhuiSkillMc(propsLunhui, props)
        self.updateFrontLunhuiSkillMc(spriteInfo, props)
        self.updateConsumeItemMC(spriteInfo)
        self.updateMyCash()

    def hideAfterLunhuiDesc(self):
        if not self.widget:
            return
        self.widget.afterSkillMc.visible = False
        self.widget.saveBtn.enabled = False
        desc = SCD.data.get('spriteLunhuiDesc', '')
        self.widget.desc0.visible = True
        self.widget.desc0.htmlText = desc

    def updateAfterLunhuiSkillMc(self, propsLunhui, props):
        self.widget.afterSkillMc.visible = True
        self.widget.saveBtn.enabled = True
        self.widget.desc0.visible = False
        naturals = propsLunhui.get('naturals', [])
        bonus = propsLunhui.get('bonus', [])
        self.updateSkillMc(self.widget.afterSkillMc, naturals, bonus, props)

    def updateFrontLunhuiSkillMc(self, spriteInfo, props):
        naturals = spriteInfo.get('skills', {}).get('naturals', []) if spriteInfo else []
        bonus = spriteInfo.get('skills', {}).get('bonus', [])
        self.updateSkillMc(self.widget.frontSkillMc, naturals, bonus, props)

    def updateSkillMc(self, itemMc, naturals, bonus, props):
        talentSkill0, talentSkill1 = self.uiAdapter.summonedWarSpriteMine.getBonusToSKillIds(bonus)
        for i in range(MAX_TALENT_NUM):
            skillMc = itemMc.getChildByName('skillMc%d' % i)
            skillType = naturals[i] if i < len(naturals) else None
            self.setSkillItemData(skillMc, skillType, props.get('famiEffLv', 1))
            ASUtils.setHitTestDisable(skillMc.bonusPoint, True)
            if skillType in talentSkill0 and skillType in talentSkill1:
                skillMc.bonusPoint.visible = True
                skillMc.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE2)
            elif skillType in talentSkill0:
                skillMc.bonusPoint.visible = True
                skillMc.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE0)
            elif skillType in talentSkill1:
                skillMc.bonusPoint.visible = True
                skillMc.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE1)
            else:
                skillMc.bonusPoint.visible = False

        itemMc.bonusMc.visible = bool(bonus)
        if bonus:
            for i in range(MAX_BONUS_NUM):
                skillText = itemMc.bonusMc.getChildByName('bonusDesc%d' % i)
                bonusBg = itemMc.bonusMc.getChildByName('bonusBg%d' % i)
                if i < len(bonus):
                    skillText.visible = True
                    bonusBg.visible = True
                    skillText.htmlText = SSSD.data.get(bonus[i], {}).get('bonusName', '')
                    tip = SSSD.data.get(bonus[i], {}).get('bonusDesc', '')
                    TipManager.addTip(skillText, tip)
                else:
                    skillText.visible = False
                    bonusBg.visible = False

    def setSkillItemData(self, skillIcon, skillType, famiLv):
        skillIcon.lockMC.visible = False
        skillIcon.cornerPic.visible = skillType
        if skillType:
            skillIcon.alpha = 1
            skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
            universalLabel = SSSD.data.get(skillType, {}).get('universalLabel', 0)
            signId = universalLabel if universalLabel else SPRITE_SKILL_SIGN_ID
            skillIcon.cornerPic.gotoAndStop('sign_%d' % signId)
            ASUtils.setHitTestDisable(skillIcon.slot, False)
            if skillId:
                lv = utils.getEffLvBySpriteFamiEffLv(famiLv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
                self.updateSkillSlotIcon(skillIcon.slot, getattr(skillIcon, 'nameText', None), skillId, lv)
        else:
            skillIcon.alpha = 0.45
            skillIcon.slot.setItemSlotData(None)
            ASUtils.setHitTestDisable(skillIcon.slot, True)

    def updateSkillSlotIcon(self, slot, nameText, skillId, lv):
        try:
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
            iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            slot.fitSize = True
            slot.dragable = False
            slot.setItemSlotData({'iconPath': iconPath})
            slot.validateNow()
            TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
             'lv': lv}, False, 'upLeft')
            if nameText:
                nameText.text = skillInfo.getSkillData('sname', '')
        except Exception as e:
            gamelog.error(e)

    def updateConsumeItemMC(self, spriteInfo):
        if not self.widget:
            return
        else:
            spriteId = spriteInfo.get('spriteId', 0)
            naturals = spriteInfo.get('skills', {}).get('naturals', [])
            ssidData = SSID.data.get(spriteId, {})
            lunhuiCostItems = ssidData.get('lunhuiCostItems', (0, 0))
            itemId = lunhuiCostItems[0]
            itemNum = lunhuiCostItems[1]
            self.widget.itemSlot.dragable = False
            count = BigWorld.player().inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
            itemInfo = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(count, itemNum))
            self.widget.itemSlot.setItemSlotData(itemInfo)
            itemCoinData = ICDCD.data.get(itemId, [0, 0])
            diKouCost = itemCoinData[1]
            itemNumDiff = max(0, itemNum - count)
            needDikouConst = itemNumDiff * diKouCost
            self.widget.tianBiDikouT.text = needDikouConst
            p = BigWorld.player()
            lunhuiCostCash = ssidData.get('lunhuiCostCash', 0)
            self.widget.bindCashT.htmlText = uiUtils.convertNumStr(p.cash, lunhuiCostCash, False, enoughColor=None)
            lunhuiTimes = p.spriteExtraDict.get('weeklyData', {}).get('lunhuiTimes', 0)
            spriteLunhuiLimitWeekly = SCD.data.get('spriteLunhuiLimitWeekly', 0)
            leftTimes = max(0, spriteLunhuiLimitWeekly - lunhuiTimes)
            self.widget.leftNumT.text = SCD.data.get('spriteLunhuiLimitWeekDesc', '%d') % leftTimes
            self.widget.lunhuiBtn.needItems = itemNum
            self.widget.lunhuiBtn.hadItems = count
            self.widget.lunhuiBtn.disabled = False
            TipManager.removeTip(self.widget.lunhuiBtn)
            if len(naturals) < const.SSPRITE_NATURAM_SKILL_NUM_LIMIT:
                self.widget.lunhuiBtn.disabled = True
                tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_NATURAM_SKILL_NUM_LIMIT_LUNHUI_2, '')
                TipManager.addTip(self.widget.lunhuiBtn, tip)
            elif lunhuiTimes >= spriteLunhuiLimitWeekly:
                self.widget.lunhuiBtn.disabled = True
                TipManager.addTip(self.widget.lunhuiBtn, SCD.data.get('spriteLunhuiTimesLessTip', gameStrings.TEXT_SUMMONEDWARSPRITELUNHUIPROXY_342))
            elif p.cash < lunhuiCostCash:
                self.widget.lunhuiBtn.disabled = True
                TipManager.addTip(self.widget.lunhuiBtn, SCD.data.get('spriteLunhuiCashLessTip', gameStrings.TEXT_GUILDGROWTHPROXY_819_1))
            else:
                myTianbi = p.unbindCoin + p.bindCoin + p.freeCoin
                isDiKouItem = self.widget.checkBox.selected
                if isDiKouItem:
                    if myTianbi < needDikouConst:
                        self.widget.lunhuiBtn.disabled = True
                        TipManager.addTip(self.widget.lunhuiBtn, SCD.data.get('spriteLunhuiTianbiLessTip', gameStrings.TEXT_SUMMONEDWARSPRITELUNHUIPROXY_352))
                elif count < itemNum:
                    self.widget.lunhuiBtn.disabled = True
                    TipManager.addTip(self.widget.lunhuiBtn, SCD.data.get('spriteLunhuiItemsLessTip', gameStrings.TEXT_SUMMONEDWARSPRITELUNHUIPROXY_356))
            spriteConsumesDict = SCD.data.get('spriteLunhuiConsumes', {})
            logSrc = spriteConsumesDict.get('logSrc', 550)
            itemId = spriteConsumesDict.get('itemId', 670004)
            _consumesDict = spriteInfo.get('_consumesDict', {})
            itemNum = _consumesDict.get(logSrc, {}).get(itemId, 0)
            self.widget.consumesT.text = itemNum
            self.updateLuckyBar(spriteInfo)
            return

    def updateLuckyBar(self, spriteInfo):
        p = BigWorld.player()
        rareLv = spriteInfo.get('rareLv', 0)
        maxLucky = SCD.data.get('spriteLunhuiNoBonusPseudoThreshold', {}).get(rareLv, 1)
        curLucky = p.summonSpriteList[self.spriteIndex]['_lunhuiPseudoCntN1']
        self.widget.luckyBar.currentValue = curLucky
        self.widget.luckyBar.maxValue = maxLucky
        self.widget.luckyValT.text = '%d/%d' % (curLucky, maxLucky)
        if curLucky == maxLucky:
            self.widget.luckyBar.fullEffect.visible = True
            self.widget.luckyBar.fullEffect.gotoAndPlay(1)
        else:
            self.widget.luckyBar.fullEffect.visible = False
        if not self.isBonus:
            self.widget.luckyBar.bonusEffect.visible = False
        bonusOccurrences = p.summonSpriteList[self.spriteIndex]['bonusOccurrences']
        self.widget.bonusNumT.text = gameStrings.SPRITE_LUNHUI_BONUS_NUM % bonusOccurrences
        limit = SCD.data.get('spriteLunhuiBonusOccurrencesLimit', {}).get(rareLv, 30)
        if bonusOccurrences < limit:
            self.widget.dropDownBonus.selectedIndex = 0
            self.widget.dropDownBonus.disabled = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_LUNHUI_DROPDOWN_DISABLED_TIP, '%d') % limit
            TipManager.addTip(self.widget.dropDownBonus, tip)
        else:
            self.widget.dropDownBonus.disabled = False
            TipManager.removeTip(self.widget.dropDownBonus)

    def updateMyCash(self):
        p = BigWorld.player()
        self.widget.bindCashTMy.text = p.cash
        self.widget.tianBiTMy.text = p.unbindCoin + p.bindCoin + p.freeCoin

    def appearBonusPlayEffect(self, index, isBonus):
        self.isBonus = isBonus
        if isBonus:
            self.widget.luckyBar.bonusEffect.visible = True
            self.widget.luckyBar.bonusEffect.gotoAndPlay('play')
            ASUtils.callbackAtFrame(self.widget.luckyBar.bonusEffect, 21, self.setEffectVisible)

    def setEffectVisible(self, *args):
        self.widget.luckyBar.bonusEffect.visible = False
        self.isBonus = False
