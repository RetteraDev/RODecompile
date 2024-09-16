#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteAwakeProxy.o
import BigWorld
import uiConst
import gameglobal
import uiUtils
import skillDataInfo
import const
from asObject import TipManager
from uiProxy import UIProxy
from guis import tipUtils
from asObject import ASUtils
from gameStrings import gameStrings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from cdata import game_msg_def_data as GMDD
SPRITE_SKILL_LEVEL = 10

class SummonedWarSpriteAwakeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteAwakeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.isFirst = False
        self.awakeSkillRefId = None
        self.spriteId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_AWAKE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_AWAKE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_AWAKE)

    def reset(self):
        self.spriteIndex = None
        self.isFirst = False
        self.awakeSkillRefId = None
        self.spriteId = None

    def show(self, spriteIndex, isFirst, awakeSkillRefId):
        self.spriteIndex = spriteIndex
        self.isFirst = isFirst
        self.awakeSkillRefId = awakeSkillRefId
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_AWAKE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.help.helpKey = SCD.data.get('spriteAwakeSkillHelpKey', 0)
        self.updateAwakeCondition()
        self.updateAwakeReward()
        self.updateDesc()

    def updateAwakeCondition(self):
        if not self.widget:
            return
        spriteInfo = gameglobal.rds.ui.summonedWarSpriteMine.getCurSelectSpriteInfo()
        self.spriteId = spriteInfo.get('spriteId', 0)
        props = spriteInfo.get('props', {})
        familiar = int(props.get('familiar', 0))
        maxFamiliar = SSID.data.get(self.spriteId, {}).get('awakeNeedFamiliarLv', 0)
        conditionDesc0 = SCD.data.get('spriteSkillAwakeCondition0', '%d') % maxFamiliar
        bFinished0 = True if familiar >= maxFamiliar else False
        strValue0 = '(%d/%d)' % (familiar, maxFamiliar)
        value0 = strValue0 if not bFinished0 else ''
        self.updateConditionMc0(self.widget.conditionMc0, conditionDesc0, bFinished0, value0)
        p = BigWorld.player()
        conditionDesc1 = SCD.data.get('spriteSkillAwakeCondition1', '')
        bFinished1 = False
        if p.summonSpriteBio.has_key(self.spriteId) and p.summonSpriteBio[self.spriteId].has_key(const.SUMMON_SPRITE_JUEXING_NEED_BIO):
            spriteBio = p.summonSpriteBio[self.spriteId][const.SUMMON_SPRITE_JUEXING_NEED_BIO]
            if spriteBio.isDone and spriteBio.isUnlock:
                bFinished1 = True
        self.updateConditionMc1(self.widget.conditionMc1, conditionDesc1, bFinished1)
        if not bFinished0 or not bFinished1:
            self.widget.awakeBtn.disabled = True
            TipManager.addTip(self.widget.awakeBtn, gameStrings.SPRITE_AWAKE_CONDITION_TIP)
        else:
            self.widget.awakeBtn.disabled = False
            TipManager.removeTip(self.widget.awakeBtn)

    def updateConditionMc0(self, conditionMc, conditionDesc, bFinished, value):
        conditionMc.conditionText.htmlText = conditionDesc
        conditionMc.conditionFinish.visible = True if bFinished else False
        conditionMc.valueText.visible = True if not bFinished else False
        conditionMc.valueText.text = value

    def updateConditionMc1(self, conditionMc, conditionDesc, bFinished):
        conditionMc.conditionText.htmlText = conditionDesc
        conditionMc.valueText.visible = False
        conditionMc.conditionFinish.visible = bFinished
        conditionMc.linkBtn.visible = not bFinished

    def updateAwakeReward(self):
        if self.isFirst:
            firstRewardItems = SSID.data.get(self.spriteId, {}).get('firstAwakeExtraAwards', ())
            rewardItems = SSID.data.get(self.spriteId, {}).get('normalAwakeAwards', ())
        else:
            firstRewardItems = []
            rewardItems = SSID.data.get(self.spriteId, {}).get('normalAwakeAwards', ())
        rewardItemsMc = self.widget.rewardItemsMc
        self.widget.removeAllInst(rewardItemsMc)
        skillId = SSSD.data.get(self.awakeSkillRefId, {}).get('virtualSkill', 0)
        itemMc = self.widget.getInstByClsName('SummonedWarSpriteAwake_skillItem')
        skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
        iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
        itemMc.slot.fitSize = True
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.slot.validateNow()
        TipManager.addTipByType(itemMc.slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
         'lv': SPRITE_SKILL_LEVEL}, False, 'upLeft')
        itemMc.markPic.visible = False
        itemMc.x = 0
        rewardItemsMc.addChild(itemMc)
        for i, data in enumerate(firstRewardItems):
            itemId, itemNum = data
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteAwake_rewardItem')
            itemMc.slot.fitSize = True
            itemMc.slot.dragable = False
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemNum))
            itemMc.markPic.visible = True
            ASUtils.setHitTestDisable(itemMc.markPic, True)
            itemMc.x = (i + 1) * itemMc.width + 5
            rewardItemsMc.addChild(itemMc)

        for i, data in enumerate(rewardItems):
            itemId, itemNum = data
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteAwake_rewardItem')
            itemMc.slot.fitSize = True
            itemMc.slot.dragable = False
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemNum))
            itemMc.markPic.visible = False
            itemMc.x = (len(firstRewardItems) + 1 + i) * itemMc.width + 5
            rewardItemsMc.addChild(itemMc)

    def updateDesc(self):
        if not self.widget:
            return
        descDict = SCD.data.get('spriteAwakeDesc', {})
        if self.spriteId in descDict:
            descList = descDict[self.spriteId]
        else:
            descList = descDict[0]
        for i in xrange(3):
            desc = self.widget.getChildByName('desc%d' % i)
            if i < len(descList):
                desc.visible = True
                desc.textField.text = descList[i]
            else:
                desc.visible = False

    def _onAwakeBtnClick(self, e):
        p = BigWorld.player()
        if p.summonedSpriteInWorld and p.summonedSpriteInWorld.inCombat:
            p.showGameMsg(GMDD.data.SPRITE_INCOMBAT_CANNOT_AWAKE, ())
            return
        p.base.setSummonSpriteJuexing(self.spriteIndex)
        self.hide()

    def _onLinkBtnClick(self, e):
        gameglobal.rds.ui.summonedWarSpriteBiography.setBiographySelectSpriteIndex(self.spriteId, True, const.SUMMON_SPRITE_JUEXING_NEED_BIO)
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX4)
        self.hide()

    def checkRedPoint(self, spriteIndex):
        if not spriteIndex:
            return False
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        props = spriteInfo.get('props', {})
        juexing = props.get('juexing', False)
        if juexing:
            return False
        familiar = int(props.get('familiar', 0))
        maxFamiliar = SSID.data.get(spriteId, {}).get('awakeNeedFamiliarLv', 0)
        bFinished0 = True if familiar >= maxFamiliar else False
        bFinished1 = False
        if p.summonSpriteBio.has_key(spriteId) and p.summonSpriteBio[spriteId].has_key(const.SUMMON_SPRITE_JUEXING_NEED_BIO):
            spriteBio = p.summonSpriteBio[spriteId][const.SUMMON_SPRITE_JUEXING_NEED_BIO]
            if spriteBio.isDone and spriteBio.isUnlock:
                bFinished1 = True
        return bFinished0 and bFinished1
