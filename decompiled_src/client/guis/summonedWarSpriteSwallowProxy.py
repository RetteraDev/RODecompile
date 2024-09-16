#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSwallowProxy.o
import BigWorld
import const
import uiConst
import gameglobal
import gamelog
import ui
import events
import uiUtils
import utils
import skillDataInfo
import tipUtils
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from guis.asObject import TipManager
from callbackHelper import Functor
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from cdata import game_msg_def_data as GMDD
POINT_ATTR_NAME_LIST = ['attrPw',
 'attrAgi',
 'attrSpr',
 'attrPhy',
 'attrInt']
ADD_POINT_INDEX = {'attrPw': 0,
 'attrAgi': 4,
 'attrSpr': 3,
 'attrPhy': 2,
 'attrInt': 1}
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SPRITE_SKILL_SIGN_ID = 100
BONUS_POINT_NUM_ONE = 1
BONUS_POINT_NUM_TWO = 2
BONUS_POINT_TYPE0 = 0
BONUS_POINT_TYPE1 = 1
BONUS_POINT_TYPE2 = 2
MAX_BONUS_NUM = 2

class SummonedWarSpriteSwallowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteSwallowProxy, self).__init__(uiAdapter)
        self.widgetId = uiConst.WIDGET_SUMMONED_SPRITE_SWALLOW
        uiAdapter.registerEscFunc(self.widgetId, self.hide)
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == self.widgetId:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(self.widgetId)

    def show(self, spriteInfo):
        self.spriteInfo = spriteInfo
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(self.widgetId)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteSwallow_SpriteItem'
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.labelFunction = self.itemFunction
        self.refreshPlayerCashInfo()

    @ui.uiEvent(uiConst.WIDGET_SUMMONED_SPRITE_SWALLOW, events.EVENT_SUMMON_SPRITE_LIST_CHANGED)
    def refreshInfo(self):
        self.spriteInfo = BigWorld.player().summonSpriteList.get(self.spriteInfo['index'])
        self.updateCurSkills()
        spriteList = self.getSwallowSpriteList()
        self.widget.spriteList.dataArray = spriteList
        self.selSpriteInfo = spriteList[0] if spriteList else {}
        self.updateSelSkills()
        gamelog.debug('zhp@SummonedWarSpriteSwallowProxy.refreshInfo', len(spriteList))

    @ui.uiEvent(uiConst.WIDGET_SUMMONED_SPRITE_SWALLOW, events.EVENT_SUMMON_SPRITE_INFO_CHANGED)
    def updateCurSkills(self):
        self.updateSkills(self.spriteInfo, False)

    def updateSelSkills(self):
        self.updateSkills(self.selSpriteInfo, True)

    def updateSkills(self, info, isSwallowedSprite):
        itemName = 'newSkillMc%d' if isSwallowedSprite else 'skillMc%d'
        bonusMc = self.widget.newBonusMc if isSwallowedSprite else self.widget.bonusMc
        naturals = info.get('skills', {}).get('naturals', []) if info else []
        bonus = info.get('skills', {}).get('bonus', [])
        talentSkill0, talentSkill1 = self.uiAdapter.summonedWarSpriteMine.getBonusToSKillIds(bonus)
        for i in range(4):
            skillIcon = self.widget.getChildByName(itemName % i)
            skillType = naturals[i] if i < len(naturals) else None
            self.setSkillItemData(skillIcon, skillType, info.get('props', {}).get('famiEffLv', 1))
            ASUtils.setHitTestDisable(skillIcon.bonusPoint, True)
            if skillType in talentSkill0 and skillType in talentSkill1:
                skillIcon.bonusPoint.visible = True
                skillIcon.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE2)
            elif skillType in talentSkill0:
                skillIcon.bonusPoint.visible = True
                skillIcon.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE0)
            elif skillType in talentSkill1:
                skillIcon.bonusPoint.visible = True
                skillIcon.bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE1)
            else:
                skillIcon.bonusPoint.visible = False

        bonusMc.visible = bool(bonus)
        if bonus:
            for i in range(MAX_BONUS_NUM):
                skillText = bonusMc.getChildByName('bonusDesc%d' % i)
                bonusBg = bonusMc.getChildByName('bonusBg%d' % i)
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
                self.updateSkillSlotIcon(skillIcon.slot, None, skillId, lv)
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

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.index
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteSwallow%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.updateSelSprite, False, 0, True)
        itemMc.szName = itemData.name
        itemMc.szLv = 'lv %d' % itemData.props.lv
        itemMc.labels = [itemMc.szName, itemMc.szLv]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.selected = self.selSpriteInfo.get('index') == itemData.index
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.index,), False, 'upLeft')

    def updateSelSprite(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected:
            return
        self.selSpriteInfo = BigWorld.player().summonSpriteList.get(target.spriteIndex)
        target.selected = True
        self.updateSelSkills()

    @ui.uiEvent(uiConst.WIDGET_SUMMONED_SPRITE_SWALLOW, (events.EVENT_CASH_CHANGED, events.EVENT_BIND_CASH_CHANGED))
    def refreshPlayerCashInfo(self):
        p = BigWorld.player()
        self.widget.bindCash.text = p.bindCash
        self.widget.cash.text = p.cash
        SSIData = SSID.data.get(self.spriteInfo['spriteId'], {})
        cashNeed = SSIData.get('spriteSwallowCash', 0)
        self.widget.costCash.htmlText = uiUtils.convertNumStr(p.cash + p.bindCash, cashNeed, False, enoughColor=None)

    def reset(self):
        self.widget = None
        self.spriteInfo = None
        self.selSpriteInfo = None
        self.msgBoxId = None

    def _onConfirmBtnClick(self, e):
        gamelog.debug('zhp@SummonedWarSpriteSwallowProxy._onConfirmBtnClick')
        self.msgBoxId and self.uiAdapter.messageBox.dismiss(self.msgBoxId)
        if self.selSpriteInfo:
            index = self.spriteInfo['index']
            msg = None
            if utils.getSpriteBattleState(index):
                msg = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_IN_BATTLE_STATE)
            elif utils.getSpriteAccessoryState(index):
                msg = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_IN_ACCESSORY)
            if msg:
                self.msgBoxId = self.uiAdapter.messageBox.showAlertBox(msg)
            else:
                anotherIndex = self.selSpriteInfo['index']
                anotherSpriteId = self.selSpriteInfo['spriteId']
                anotherName = self.selSpriteInfo['name']
                anotherLv = self.selSpriteInfo['props']['lv']
                anotherOldName = SSID.data.get(anotherSpriteId, {}).get('name', '')
                primaryName = self.spriteInfo['name']
                primarySpriteId = self.spriteInfo['spriteId']
                primaryLv = self.spriteInfo['props']['lv']
                primaryOldName = SSID.data.get(primarySpriteId, {}).get('name', '')
                primaryValues = self.getOriPrimaryPropValues(self.spriteInfo['props'])
                swallowValues = self.getOriPrimaryPropValues(self.selSpriteInfo['props'])
                swallowCombine = self.getTalentAndBounsName(self.selSpriteInfo)
                msg = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_CONFIRM_MSG, '%s%s%d%s%d%d%d%d%d%d%d%d%d%d%s%s%d') % (primaryName,
                 primaryOldName,
                 primaryLv,
                 swallowCombine,
                 primaryValues[0],
                 swallowValues[0],
                 primaryValues[1],
                 swallowValues[1],
                 primaryValues[2],
                 swallowValues[2],
                 primaryValues[3],
                 swallowValues[3],
                 primaryValues[4],
                 swallowValues[4],
                 anotherName,
                 anotherOldName,
                 anotherLv)
                self.msgBoxId = self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.checkBindCash, index, anotherIndex), textAlign='left')
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_NO_SPRITE)
            self.msgBoxId = self.uiAdapter.messageBox.showAlertBox(msg)

    def getOriPrimaryPropValues(self, props):
        oriValues = []
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            addIdx = ADD_POINT_INDEX[POINT_ATTR_NAME_LIST[idx]]
            value = props.get('oriPrimaryProp', [0] * 5)[addIdx]
            oriValues.append(value)

        return oriValues

    def getTalentAndBounsName(self, info):
        combineName = ''
        naturals = info.get('skills', {}).get('naturals', [])
        famiLv = info.get('props', {}).get('famiEffLv', 1)
        for skillType in naturals:
            skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
            if skillId:
                lv = utils.getEffLvBySpriteFamiEffLv(famiLv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
                skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
                sname = skillInfo.getSkillData('sname', '')
                if combineName:
                    combineName = combineName + ',' + sname
                else:
                    combineName += sname

        bonus = info.get('skills', {}).get('bonus', [])
        for i in range(MAX_BONUS_NUM):
            if i < len(bonus):
                bonusName = SSSD.data.get(bonus[i], {}).get('bonusName', '')
                if combineName:
                    combineName = combineName + ',' + bonusName
                else:
                    combineName += bonusName

        return combineName

    def _onCancelBtnClick(self, e):
        self.hide()

    def checkBindCash(self, index, anotherIndex):
        p = BigWorld.player()
        SSIData = SSID.data.get(self.spriteInfo['spriteId'], {})
        cashNeed = SSIData.get('spriteSwallowCash', 0)
        if p.bindCash < cashNeed:
            msg = uiUtils.getTextFromGMD(GMDD.data.BINDCASH_IS_NOT_ENOUGH, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.applySwallow, index, anotherIndex), msgType='bindCash', isShowCheckBox=True)
        else:
            self.applySwallow(index, anotherIndex)

    @ui.checkInventoryLock()
    def applySwallow(self, index, anotherIndex):
        p = BigWorld.player()
        p.base.applySwallowAnotherSprite(index, anotherIndex, p.cipherOfPerson)

    def getSwallowSpriteList(self):
        spriteList = []
        if not self.spriteInfo:
            return []
        p = BigWorld.player()
        for sprite in p.summonSpriteList.values():
            if sprite['index'] == self.spriteInfo['index']:
                continue
            if sprite['spriteId'] != self.spriteInfo['spriteId']:
                continue
            if utils.getSpriteBattleState(sprite['index']):
                continue
            if utils.getSpriteAccessoryState(sprite['index']):
                continue
            spriteList.append(sprite)

        gamelog.debug('zhp@SummonedWarSpriteSwallowProxy.getSwallowSpriteList', len(p.summonSpriteList), len(spriteList))
        return sorted(spriteList, key=lambda d: d['props']['lv'], reverse=True)
