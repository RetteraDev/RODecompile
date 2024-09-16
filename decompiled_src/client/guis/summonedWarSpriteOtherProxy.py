#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteOtherProxy.o
import BigWorld
import gameglobal
import events
import gametypes
import uiConst
import utils
import formula
import skillDataInfo
import const
import gamelog
import tipUtils
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from cdata import summon_sprite_bonus_skill_data as SSBSD
from cdata import game_msg_def_data as GMDD
DATA_2_ATTRS = ((0, 15, 25),
 (4, 12, 22),
 (3, 16, 26),
 (2, 14, 24),
 (1, 13, 23))
QUALITY_2_COLOR = {0: 'white',
 1: 'green_1',
 2: 'blue_2',
 3: 'purple_3',
 4: 'golden_4'}
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
BONUS_POINT_NUM_ONE = 1
BONUS_POINT_NUM_TWO = 2
BONUS_POINT_TYPE0 = 0
BONUS_POINT_TYPE1 = 1
BONUS_POINT_TYPE2 = 2
MAX_TALENT_NUM = 4
SPRITE_SKILL_SIGN_ID = 100
MAX_BONUS_NUM = 2
SKILL_SLOT_NUM = 8
SPRITE_SKILL_LEVEL = 1

class SummonedWarSpriteOtherProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteOtherProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_OTHER, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_OTHER:
            self.widget = widget
            self.itemMc = None
            self.initUI()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
        warSpritesMc = self.widget.warSpritesMc
        warSpritesMc.spriteList.itemHeight = 65
        warSpritesMc.spriteList.itemRenderer = 'SummonedWarSpriteOther_SummonedWarSprite_Item'
        warSpritesMc.spriteList.barAlwaysVisible = True
        warSpritesMc.spriteList.dataArray = []
        warSpritesMc.spriteList.lableFunction = self.lableFunction
        warSpritesMc.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.onSelect, False, 0, True)
        self.typeToSort = SCD.data.get('spriteMajorAbility', [])
        typeList = []
        for i, value in enumerate(self.typeToSort):
            typeInfo = {}
            typeInfo['label'] = gameStrings.SUMMONED_WAR_SPRITE_TXT1 + '<font color=\"#de5900\">' + value + '</font>' + gameStrings.SUMMONED_WAR_SPRITE_TXT2
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(warSpritesMc.spriteTypeDropdown, typeList)
        warSpritesMc.spriteTypeDropdown.menuRowCount = min(len(typeList), 5)
        warSpritesMc.spriteTypeDropdown.selectedIndex = 0
        spriteNumLimit = SCD.data.get('spriteNumLimit', 20)
        warSpritesMc.holdSpritesText.text = '%d/%d' % (len(self.data), spriteNumLimit)
        self.updateWarSpritesMc()

    def updateWarSpritesMc(self):
        spriteItemList = []
        index = self.widget.warSpritesMc.spriteTypeDropdown.selectedIndex
        self.sortedData = gameglobal.rds.ui.summonedWarSpriteMine.sortOtherSpriteList(self.data, index)
        for index, spriteInfo in enumerate(self.sortedData):
            itemInfo = {}
            itemInfo['numberId'] = index
            itemInfo['index'] = spriteInfo.get('index', 0)
            itemInfo['spriteId'] = spriteInfo.get(1, 0)
            itemInfo['name'] = spriteInfo.get(2, '')
            itemInfo['lv'] = spriteInfo.get(3, 0)
            spriteItemList.append(itemInfo)

        self.widget.warSpritesMc.spriteList.dataArray = spriteItemList
        self.widget.warSpritesMc.spriteList.validateNow()

    def onSelect(self, *args):
        self.itemMc.selected = False
        self.itemMc = None
        self.updateWarSpritesMc()

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.addEventListener(events.BUTTON_CLICK, self.onClickWarSprite, False, 0, True)
        itemMc.szName = itemData.name
        itemMc.numberId = itemData.numberId
        itemMc.szLv = 'lv %d' % itemData.lv
        itemMc.labels = [itemMc.szName, itemMc.szLv]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        slot = itemMc.itemSlot.slot
        slot.setItemSlotData({'iconPath': iconPath})
        ASUtils.setHitTestDisable(slot, True)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        slot.validateNow()
        itemMc.dieIcon.visible = False
        itemMc.spriteState.visible = False
        if not self.itemMc:
            itemMc.selected = True
            self.itemMc = itemMc
            self.update()

    def onClickWarSprite(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if itemMc.numberId != self.itemMc.numberId:
            itemMc.selected = True
            self.itemMc.selected = False
            self.itemMc = itemMc
            self.update()

    def update(self):
        self.updateAttributeMc()
        self.updateSkillMc()

    def updateAttributeMc(self):
        data = self.sortedData[self.itemMc.numberId]
        attributeMc = self.widget.attributeMc
        attributeMc.warSpriteName.text = data[2]
        attributeMc.power.text = data[4]
        props = {}
        props['oriAptitudeAgi'] = data[17]
        props['oriAptitudeInt'] = data[18]
        props['oriAptitudePhy'] = data[19]
        props['oriAptitudePw'] = data[20]
        props['oriAptitudeSpr'] = data[21]
        props['aptitudeAgi'] = data[22]
        props['aptitudeInt'] = data[23]
        props['aptitudePhy'] = data[24]
        props['aptitudePw'] = data[25]
        props['aptitudeSpr'] = data[26]
        props['name'] = data[2]
        props['baseGrowthRatio'] = data[33]
        title = utils.getSpriteScoreInfo(data[1], props)[2]
        attributeMc.ratingTitle.htmlText = title
        attributeMc.growthRate.htmlText = str('%.3f' % data[33]) + '<font color=\"#559423\">' + '+' + str('%.3f' % (data[28] - data[33])) + '</font>'
        star = utils.getSpriteGrowthRatioStar(data[1], data[28])
        attributeMc.ratingNum.text = '%d/%d' % (data[29], SSID.data.get(data[1], {}).get('spriteBoneTimes', 0))
        attributeMc.cleverMC.visible = data[30]
        iconId = SSID.data.get(data[1], {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        slot = attributeMc.itemSlot.slot
        slot.setItemSlotData({'iconPath': iconPath})
        ASUtils.setHitTestDisable(slot, True)
        attributeMc.bind.text = SCD.data.get('spriteBindTypeDesc')[data[5]]
        attributeMc.lv.text = data[3]
        attributeMc.intimacyLv.htmlText = str(data[8] - data[27]) + '<font color=\"#559423\">' + '+' + str(data[27]) + '</font>'
        attributeMc.race.text = SSID.data.get(data[1], {}).get('spriteRace', '')
        upgradeStage = data[const.SPRITE_DICT_INDEX_upgradeStage] if const.SPRITE_DICT_INDEX_upgradeStage in data else 0
        for i in range(len(DATA_2_ATTRS)):
            starMc = getattr(attributeMc, 'star%s' % i)
            starMc.visible = star >= i
            baseAttr = getattr(attributeMc, 'baseAttr%d' % i)
            baseAttr.text = '%d + %d' % (data[11][DATA_2_ATTRS[i][0]], data[DATA_2_ATTRS[i][1]] - data[11][DATA_2_ATTRS[i][0]])
            baseAptitude = getattr(attributeMc, 'baseAptitude%d' % i)
            aptitudeName = utils.APTITUDE_NAME_LIST[i]
            aptitudeOriginMax = utils.getAptitudeMax(data[1], aptitudeName)
            aptitudeMax = formula.getSpriteAptitudeVal(aptitudeOriginMax, data[30], data[9], data[1], upgradeStage)
            baseAptitude.text = '%d/%d' % (data[DATA_2_ATTRS[i][2]], aptitudeMax)
            aptitudeBar = getattr(attributeMc, 'aptitudeBar%d' % i)
            aptitudeBar.maxValue = aptitudeMax
            aptitudeBar.currentValues = [data[DATA_2_ATTRS[i][2]], 0, 0]
            fightAttr = getattr(attributeMc, 'fightAttr%d' % i)
            fightAttr.text = data[31][i]

    def updateSkillMc(self):
        data = self.sortedData[self.itemMc.numberId]
        self.updateAbilitySkill(self.widget.skillMc.passiveSkillSlot, data, 'trait', 34)
        self.updateAbilitySkill(self.widget.skillMc.activeSkillSlot, data, 'awake', 10, data[7])
        self.updateTalentSkill(data)
        self.updateLearnedSkill(data[32])

    def updateLearnedSkill(self, info):
        skillMc = self.widget.skillMc
        for i in xrange(SKILL_SLOT_NUM):
            slotMc = getattr(skillMc, 'learnedSkill%d' % i)
            slotMc.lockMC.visible = not info[i][1]
            skillId = SSSD.data.get(info[i][0], {}).get('virtualSkill', 0) if info[i][0] else 0
            slot = slotMc.slot
            if skillId:
                skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
                iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                slot.fitSize = True
                slot.dragable = False
                slot.setItemSlotData({'iconPath': iconPath})
                ASUtils.setHitTestDisable(slot, False)
                slot.validateNow()
                TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': SPRITE_SKILL_LEVEL}, False, 'upLeft')
            else:
                slot.setItemSlotData(None)
                ASUtils.setHitTestDisable(slot, True)

    def updateTalentSkill(self, data):
        skillMc = self.widget.skillMc
        talentSkill0, talentSkill1 = self.getBonusToSKillIds(data[7])
        for i in range(MAX_TALENT_NUM):
            skillIcon = skillMc.getChildByName('overview_skill%d' % i)
            cornerPic = skillMc.getChildByName('cornerPic%d' % i)
            bonusPoint = skillMc.getChildByName('bonusPoint%d' % i)
            talentName = skillMc.getChildByName('talentName%d' % i)
            skillIcon.lockMC.visible = False
            ASUtils.setHitTestDisable(bonusPoint, True)
            if i < len(data[6]):
                skillIcon.alpha = 1
                skillType = data[6][i]
                skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
                universalLabel = SSSD.data.get(skillType, {}).get('universalLabel', 0)
                ASUtils.setHitTestDisable(skillIcon.slot, False)
                if skillId:
                    self.setSkillSlot(skillIcon.slot, talentName, data[8], skillId, 'naturals')
                cornerPic.visible = True
                talentName.visible = True
                signId = universalLabel if universalLabel else SPRITE_SKILL_SIGN_ID
                cornerPic.gotoAndStop('sign_%d' % signId)
                if skillType in talentSkill0 and skillType in talentSkill1:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE2)
                elif skillType in talentSkill0:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE0)
                elif skillType in talentSkill1:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE1)
                else:
                    bonusPoint.visible = False
            else:
                skillIcon.alpha = 0.45
                cornerPic.visible = False
                talentName.visible = False
                bonusPoint.visible = False
                skillIcon.slot.setItemSlotData(None)
                ASUtils.setHitTestDisable(skillIcon.slot, True)

        if data[7]:
            skillMc.bonusMc.visible = True
            for i in range(MAX_BONUS_NUM):
                skillText = skillMc.bonusMc.getChildByName('bonusDesc%d' % i)
                bonusBg = skillMc.bonusMc.getChildByName('bonusBg%d' % i)
                if i < len(data[7]):
                    skillText.visible = True
                    bonusBg.visible = True
                    skillText.htmlText = SSSD.data.get(data[7][i], {}).get('bonusName', '')
                    tip = SSSD.data.get(data[7][i], {}).get('bonusDesc', '')
                    TipManager.addTip(skillText, tip)
                else:
                    skillText.visible = False
                    bonusBg.visible = False

        else:
            skillMc.bonusMc.visible = False

    def getBonusToSKillIds(self, bonus):
        if len(bonus) == BONUS_POINT_NUM_ONE:
            bonusId0 = bonus[0]
            bonusId1 = 0
        elif len(bonus) == BONUS_POINT_NUM_TWO:
            bonusId0 = bonus[0]
            bonusId1 = bonus[1]
        else:
            bonusId0 = 0
            bonusId1 = 0
        return (SSBSD.data.get(bonusId0, {}).get('talentCombo', ()), SSBSD.data.get(bonusId1, {}).get('talentCombo', ()))

    def updateAbilitySkill(self, skillSlot, data, szType, index, bonus = []):
        typeId = data[index]
        sssdData = SSSD.data.get(typeId, {})
        skillId = sssdData.get('virtualSkill', 0)
        skillAddId, skillLvAdd = sssdData.get('skillAddVirtualLv', (0, 0))
        addVirtualLv = skillLvAdd if skillAddId in bonus else 0
        if skillId:
            self.setSkillSlot(skillSlot.slotS, skillSlot.nameS, data[8], skillId, szType, addVirtualLv)
            skillSlot.lockS.visible = False
            skillSlot.blackBg.visible = False
            if szType == 'awake' and not data[9]:
                skillSlot.lockS.visible = True
                skillSlot.blackBg.visible = True
                ASUtils.setHitTestDisable(skillSlot.blackBg, True)

    def setSkillSlot(self, slot, nameText, famiEfflv, skillId, szType, addVirtualLv = 0):
        effLv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, szType, const.DEFAULT_SKILL_LV_SPRITE)
        lv = min(effLv + addVirtualLv, const.MAX_SKILL_LEVEL)
        try:
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
            iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            slot.fitSize = True
            slot.dragable = False
            slot.setItemSlotData({'iconPath': iconPath})
            slot.validateNow()
            TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
             'lv': lv}, False, 'upLeft')
            nameText.text = skillInfo.getSkillData('sname', '')
        except Exception as e:
            gamelog.error(e)

    def onClickCloseBtn(self, *args):
        self.hide()

    def show(self, data):
        if not data or len(data) == 0:
            BigWorld.player().showGameMsg(GMDD.data.NO_SUMMONED_SPRITE_DATA, ())
            return
        else:
            self.data = data
            for index, item in self.data.items():
                item['index'] = index

            if self.widget:
                self.itemMc = None
                self.initUI()
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_OTHER)
            return

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_OTHER)
