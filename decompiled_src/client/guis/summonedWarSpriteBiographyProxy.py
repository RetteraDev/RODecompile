#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteBiographyProxy.o
import BigWorld
import utils
import events
import gameglobal
import tipUtils
import uiConst
import skillDataInfo
import const
import ui
from asObject import RedPotManager
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from helpers import capturePhoto
from gameStrings import gameStrings
from Scaleform import GfxValue
from callbackHelper import Functor
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_data as SSD
from data import summon_sprite_info_data as SSID
from data import monster_model_client_data as MMCD
from data import achievement_data as AD
from data import achieve_target_data as ATD
from data import summon_sprite_biography_data as SSBD
from data import summon_sprite_skill_data as SSSD
from data import skill_general_data as SGD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SPRITE_BIOGRAPHY_NUM = 8
MAX_BIOGRAPHY_UNLOCK_CONDITION_NUM = 3
UNLOCK_ITEM_HEIGHT = 22
UNLOCK_REWARD_ITEM_NUM = 4
TLAENT_SKILL_SLOT_NUM = 5
BIOGRAPHY_UNLOCK_SOUND_ID = 5747
SPRITE_SKILL_SIGN_ID = 100
MIN_SKILL_LV_SPRITE = 1
BIO_UNLOCK_NEED_HIDE_SOUND_BTN = 4
OTHER_BIO_INDEX = 5

class SummonedWarSpriteBiographyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteBiographyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.warSpriteDict = {}
        self.headGen = None
        self.currSelectItem = None
        self.currSelectItemSpriteId = None
        self.isBiography = False
        self.currSelectBioId = None
        self.currSelectBioItem = None
        self.currPlayBioSoundId = None
        self.contentTextMc = None

    def reset(self):
        self.warSpriteDict = {}
        self.currSelectItem = None
        self.currSelectItemSpriteId = None
        self.isBiography = False
        self.currSelectBioId = None
        self.currSelectBioItem = None
        self.contentTextMc = None
        self.stopCurrPlayBioSound()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.setTemplateStates()

    def setTemplateStates(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            self.widget.biographyPanel.biographyBtn.visible = False

    def initUI(self):
        self.widget.biographyPanel.commentBtn.visible = False
        self.widget.biographyPanel.manualBtn.addEventListener(events.BUTTON_CLICK, self.handleManualBtnClick, False, 0, True)
        self.widget.biographyPanel.biographyBtn.addEventListener(events.BUTTON_CLICK, self.handleBiographyBtnClick, False, 0, True)
        self.contentTextMc = self.widget.getInstByClsName('SummonedWarSpriteBiography_contentText')
        self.initLeftWarSpritesMc()
        RedPotManager.addRedPot(self.widget.biographyPanel.biographyBtn, uiConst.SUMMONED_WAR_SPRITE_BIOGRAPHY_RED_POT, (58, -3), self.visiblePotFun)

    def initLeftWarSpritesMc(self):
        warSpritesMc = self.widget.biographyPanel.warSpritesMc
        warSpritesMc.spriteList.column = 3
        warSpritesMc.spriteList.itemWidth = 75
        warSpritesMc.spriteList.itemHeight = 75
        warSpritesMc.spriteList.itemRenderer = 'SummonedWarSpriteBiography_spriteHeadIcon'
        warSpritesMc.spriteList.barAlwaysVisible = True
        warSpritesMc.spriteList.dataArray = []
        warSpritesMc.spriteList.lableFunction = self.itemFunction
        self.warSpriteDict = self.getShowWarSpriteDict()
        warSpritesMc.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
        typeToSort = SCD.data.get('spriteAtkTypeList', [])
        typeList = []
        for i, vlaue in enumerate(typeToSort):
            typeInfo = {}
            typeInfo['label'] = vlaue
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(warSpritesMc.spriteTypeDropdown, typeList)
        warSpritesMc.spriteTypeDropdown.menuRowCount = min(len(typeList), 5)
        if warSpritesMc.spriteTypeDropdown.selectedIndex == -1:
            warSpritesMc.spriteTypeDropdown.selectedIndex = 0

    def handleManualBtnClick(self, *args):
        self.isBiography = False
        self.updateManualOrBiography()

    def handleBiographyBtnClick(self, *args):
        self.isBiography = True
        self.updateManualOrBiography()

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex)

    def handleSpriteHeadIconClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.currSelectItemSpriteId and self.currSelectItemSpriteId == itemMc.spriteId:
            return
        if self.currSelectItem:
            self.currSelectItem.selectedHeadIcon.visible = False
        itemMc.selectedHeadIcon.visible = True
        self.currSelectItem = itemMc
        self.currSelectItemSpriteId = itemMc.spriteId
        self.updateSpritePhoto3D()
        self.updateSpriteOhterInfo()
        self.updateManualOrBiography()
        self.updateBiographyRedPot()

    def handleBiographyPictureClick(self, *args):
        e = ASObject(args[3][0])
        bioPicture = e.currentTarget
        if not bioPicture.isOpen:
            return
        if self.currSelectBioId and self.currSelectBioId == bioPicture.bioId:
            return
        if self.currSelectBioItem:
            self.currSelectBioItem.selectedP.visible = False
        bioPicture.selectedP.visible = True
        self.currSelectBioId = bioPicture.bioId
        self.currSelectBioItem = bioPicture
        self.updateSpriteBioMc(bioPicture)

    def handleUnlockBtnClick(self, *args):
        e = ASObject(args[3][0])
        unlockBtn = e.currentTarget
        if unlockBtn.spriteId and unlockBtn.bioId:
            p = BigWorld.player()
            p.base.unLockSummonSpriteBio(unlockBtn.spriteId, unlockBtn.bioId)

    def handleStopSoundBtnClick(self, *args):
        e = ASObject(args[3][0])
        stopBtn = e.currentTarget
        stopBtn.visible = False
        self.widget.biographyPanel.biographyMc.bioContentMc.playSoundBtn.visible = True
        if stopBtn.biographySoundId:
            gameglobal.rds.sound.stopSound(stopBtn.biographySoundId)

    def handlePlaySoundBtnClick(self, *args):
        e = ASObject(args[3][0])
        playBtn = e.currentTarget
        playBtn.visible = False
        self.widget.biographyPanel.biographyMc.bioContentMc.stopSoundBtn.visible = True
        if playBtn.biographySoundId:
            self.currPlayBioSoundId = playBtn.biographySoundId
            gameglobal.rds.sound.playSound(playBtn.biographySoundId)

    def handleMoreBtnClick(self, *args):
        helpKeyWord = SSID.data.get(self.currSelectItemSpriteId, {}).get('helpKeyWordMoreInfo', '')
        gameglobal.rds.ui.help.show(helpKeyWord)

    def handleGetBtnClick(self, *args):
        helpKeyWord = SSID.data.get(self.currSelectItemSpriteId, {}).get('helpKeyWordGainWay', '')
        gameglobal.rds.ui.help.show(helpKeyWord)

    def refreshInfo(self):
        if not self.widget:
            return
        warSpritesMc = self.widget.biographyPanel.warSpritesMc
        self.updateWarSpritesTypeList(warSpritesMc.spriteTypeDropdown.selectedIndex)

    def getShowWarSpriteDict(self):
        dict = {}
        for i, spritdId in enumerate(SSID.data):
            spriteData = SSID.data.get(spritdId, {})
            spriteData['spriteId'] = spritdId
            spriteManual = spriteData.get('spriteManual', 0)
            if spriteManual:
                dict[spritdId] = spriteData

        return dict

    def filterWarSpriteList(self, typeIndex):
        spriteList = []
        for spritdId in self.warSpriteDict:
            spriteData = SSID.data.get(spritdId, {})
            attackType = spriteData.get('atkType', 0)
            if attackType == typeIndex or not typeIndex:
                spriteList.append(spriteData)

        spriteList.sort(key=lambda d: d['spriteManual'])
        return spriteList

    def updateWarSpritesTypeList(self, typeIndex):
        warSpriteList = self.filterWarSpriteList(typeIndex)
        itemList = []
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            teamInfo = {}
            teamInfo['numberId'] = i
            teamInfo['spriteId'] = spriteInfo.get('spriteId', -1)
            teamInfo['name'] = spriteInfo.get('name', '')
            teamInfo['iconPath'] = gameglobal.rds.ui.summonedWarSpriteGuard.getSpriteIconPath(spriteInfo.get('spriteId', 0))
            teamInfo['isRedPoint'] = self.checkRedPoint(teamInfo['spriteId'])
            itemList.append(teamInfo)

        self.widget.biographyPanel.warSpritesMc.spriteList.dataArray = itemList
        self.widget.biographyPanel.warSpritesMc.spriteList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSpriteHeadIconClick, False, 0, True)
        itemMc.spriteId = itemData.spriteId
        itemMc.icon.clear()
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(itemData.iconPath)
        itemMc.selectedHeadIcon.visible = False
        itemMc.redIcon.visible = itemData.isRedPoint
        if self.currSelectItemSpriteId and self.currSelectItemSpriteId == itemData.spriteId:
            itemMc.selectedHeadIcon.visible = True
        elif not self.currSelectItemSpriteId and itemData.numberId == 0:
            itemMc.selectedHeadIcon.visible = True
        if itemMc.selectedHeadIcon.visible:
            self.currSelectItem = itemMc
            self.currSelectItemSpriteId = itemData.spriteId
            self.updateSpritePhoto3D()
            self.updateSpriteOhterInfo()
            self.updateManualOrBiography()
            self.updateBiographyRedPot()

    def updateSpritePhoto3D(self):
        self.initHeadGen()
        self.takePhoto3D()

    def takePhoto3D(self):
        charType = SSD.data.get(self.currSelectItemSpriteId, {}).get('charType', 0)
        modelId = MMCD.data.get(charType, {}).get('model', 0)
        if not self.headGen:
            self.headGen = capturePhoto.SummonedWarSpriteBiographyPhotoGen.getInstance('gui/taskmask.tga', 299)
        self.headGen.startCapture(modelId, None, None)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.SummonedWarSpriteBiographyPhotoGen.getInstance('gui/taskmask.tga', 299)
        self.headGen.initFlashMesh()

    def updateSpriteOhterInfo(self):
        spriteData = SSID.data.get(self.currSelectItemSpriteId, {})
        self.widget.biographyPanel.spriteName.htmlText = spriteData.get('name', '')
        self.widget.biographyPanel.spriteType.text = spriteData.get('spriteRace', '')
        self.widget.biographyPanel.spriteTypeDesc.text = spriteData.get('spriteTypeDesc', '')
        attackType = spriteData.get('atkType', 0)
        tipMsg = ''
        if attackType == 1:
            self.widget.biographyPanel.attackType.gotoAndStop('nearWar')
            tipMsg = SCD.data.get('spriteNearWarTip', '')
        elif attackType == 2:
            self.widget.biographyPanel.attackType.gotoAndStop('farWar')
            tipMsg = SCD.data.get('spriteFarWarTip', '')
        elif attackType == 3:
            self.widget.biographyPanel.attackType.gotoAndStop('magic')
            tipMsg = SCD.data.get('spriteMagicTip', '')
        elif attackType == 4:
            self.widget.biographyPanel.attackType.gotoAndStop('nearMagic')
            tipMsg = SCD.data.get('spriteNearMagicTip', '')
        TipManager.addTip(self.widget.biographyPanel.attackType, tipMsg)
        rareIcon = self.widget.biographyPanel.rareIcon
        rareIcon.visible = spriteData.get('isRare', False)
        if rareIcon.visible:
            rareIcon.gotoAndStop('type' + str(spriteData.get('isRare')))

    def updateManualMc(self):
        manualMc = self.widget.biographyPanel.manualMc
        self.updateSkillSlot(manualMc.skillSpeSlot, 'trait')
        self.updateSkillSlot(manualMc.skillActSlot, 'awake')
        self.updateTalentRange()
        self.updateAttributeRange()

    def updateSkillSlot(self, skillSlot, szType):
        typeId = self.warSpriteDict.get(self.currSelectItemSpriteId, {}).get(szType, 0)
        skillId = SSSD.data.get(typeId, {}).get('virtualSkill', 0)
        if skillId:
            self.updateSkillSlotIcon(skillSlot.slotS, skillSlot.nameS, skillId, szType)

    def updateSkillSlotIcon(self, slot, nameText, skillId, szType = ''):
        try:
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=MIN_SKILL_LV_SPRITE)
            iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            slot.icon.clear()
            slot.icon.fitSize = True
            slot.icon.loadImage(iconPath)
            TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
             'lv': MIN_SKILL_LV_SPRITE}, False, 'upLeft')
            if nameText:
                nameText.text = skillInfo.getSkillData('sname', '')
        except:
            pass

    def updateTalentRange(self):
        manualMc = self.widget.biographyPanel.manualMc
        manualMc.talentRangeText.text = SCD.data.get('talentRangeText', '')
        manualMc.moreBtn.addEventListener(events.BUTTON_CLICK, self.handleMoreBtnClick, False, 0, True)
        talentSkillList = SSID.data.get(self.currSelectItemSpriteId, {}).get('talentSkillList', [])
        for i in range(TLAENT_SKILL_SLOT_NUM):
            slot = manualMc.skillList.getChildByName('skillSlot%d' % i)
            if i < len(talentSkillList):
                skillId = talentSkillList[i]
                self.updateSkillSlotIcon(slot, None, skillId)
                signId = SGD.data.get((skillId, MIN_SKILL_LV_SPRITE), {}).get('spriteSkillSign', SPRITE_SKILL_SIGN_ID)
                slot.cornerPic.gotoAndStop('sign_%d' % signId)

    def updateAttributeRange(self):
        manualMc = self.widget.biographyPanel.manualMc
        manualMc.qualityRangeText.text = SCD.data.get('qualityRangeText', '')
        manualMc.getBtn.addEventListener(events.BUTTON_CLICK, self.handleGetBtnClick, False, 0, True)
        for idx in xrange(len(utils.APTITUDE_TALENT_RANGE_NAME_LIST)):
            aptitudeName = utils.APTITUDE_TALENT_RANGE_NAME_LIST[idx]
            aptitudeMax = utils.getAptitudeMax(self.currSelectItemSpriteId, aptitudeName)
            aptitudeMin = utils.getAptitudeMin(self.currSelectItemSpriteId, aptitudeName)
            valueText = manualMc.attributeMc.getChildByName(aptitudeName + 'Range')
            valueText.text = '%s-%s' % (str(aptitudeMin), str(aptitudeMax))
            txt = manualMc.attributeMc.getChildByName(aptitudeName + 'Txt')
            if aptitudeName == 'growthRatio':
                tip = SCD.data.get('spriteGrowthRatioTip', 'spriteGrowthRatioTip')
            else:
                tip = SCD.data.get('spriteAptitudeTips', {}).get(aptitudeName, aptitudeName)
            TipManager.addTip(txt, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def updateBiographyMc(self):
        p = BigWorld.player()
        biographyMc = self.widget.biographyPanel.biographyMc
        for bioId in range(1, SPRITE_BIOGRAPHY_NUM + 1):
            bioPicture = biographyMc.getChildByName('bioPicture%d' % bioId)
            bioPicture.addEventListener(events.MOUSE_CLICK, self.handleBiographyPictureClick, False, 0, True)
            bioPicture.bioId = bioId
            bioPicture.spriteId = self.currSelectItemSpriteId
            bioPicture.isUnlock = False
            bioPicture.isOtherBio = bioId >= OTHER_BIO_INDEX
            bioPicture.achieveId = SSBD.data.get((self.currSelectItemSpriteId, bioId), {}).get('achieveId', -1)
            bioPicture.isOpen = SSBD.data.get((self.currSelectItemSpriteId, bioId), {}).get('open', 0)
            bioPicture.lockP.gotoAndPlay('lock')
            TipManager.removeTip(bioPicture)
            if p.summonSpriteBio.has_key(self.currSelectItemSpriteId) and p.summonSpriteBio[self.currSelectItemSpriteId].has_key(bioId):
                isDone = p.summonSpriteBio[self.currSelectItemSpriteId][bioId].isDone
                isUnlock = p.summonSpriteBio[self.currSelectItemSpriteId][bioId].isUnlock
                bioPicture.unLockSfx.visible = isDone and not isUnlock
                bioPicture.lockP.visible = not isUnlock
                bioPicture.normalP.visible = isDone
                bioPicture.sealP.visible = False
                bioPicture.isUnlock = isUnlock
            elif bioPicture.isOpen:
                bioPicture.unLockSfx.visible = False
                bioPicture.lockP.visible = True
                bioPicture.normalP.visible = True
                bioPicture.sealP.visible = False
            else:
                bioPicture.unLockSfx.visible = False
                bioPicture.lockP.visible = True
                bioPicture.normalP.visible = False
                bioPicture.sealP.visible = True
                TipManager.addTip(bioPicture, gameStrings.SUMMONED_WAR_SPRITE_COMING_SOON)
            bioPicture.selectedP.visible = False
            if not self.currSelectBioId or self.currSelectBioId == bioId:
                bioPicture.selectedP.visible = True
                self.currSelectBioId = bioId
                self.currSelectBioItem = bioPicture
                self.updateSpriteBioMc(bioPicture)

    def visiblePotFun(self, *args):
        isRedPot = self.checkRedPoint(self.currSelectItemSpriteId)
        return GfxValue(isRedPot)

    def updateBiographyRedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_BIOGRAPHY_RED_POT)

    def checkRedPoint(self, spriteId):
        p = BigWorld.player()
        if not p.summonSpriteBio.has_key(spriteId):
            return False
        for bioId in range(1, SPRITE_BIOGRAPHY_NUM + 1):
            if p.summonSpriteBio[spriteId].has_key(bioId):
                if p.summonSpriteBio[spriteId][bioId].isDone and not p.summonSpriteBio[spriteId][bioId].isUnlock:
                    return True

        return False

    def checkAllSpriteBioRedPoint(self):
        warSpriteDict = self.getShowWarSpriteDict()
        if not warSpriteDict:
            return False
        for spriteId in warSpriteDict:
            spriteInfo = warSpriteDict[spriteId]
            spriteId = spriteInfo.get('spriteId', 0)
            isRed = self.checkRedPoint(spriteId)
            if isRed:
                return True

        return False

    def updateManualOrBiography(self):
        if not self.widget:
            return
        self.widget.biographyPanel.manualBtn.selected = not self.isBiography
        self.widget.biographyPanel.manualMc.visible = not self.isBiography
        self.widget.biographyPanel.biographyBtn.selected = self.isBiography
        self.widget.biographyPanel.biographyMc.visible = self.isBiography
        self.stopCurrPlayBioSound()
        if self.isBiography:
            self.updateBiographyMc()
        else:
            self.updateManualMc()

    def updateSpriteBioMc(self, bioPicture):
        if self.currSelectItemSpriteId != bioPicture.spriteId:
            return
        unlockContentMc = self.widget.biographyPanel.biographyMc.unlockContentMc
        bioContentMc = self.widget.biographyPanel.biographyMc.bioContentMc
        if bioPicture.isOtherBio:
            bioContentMc.visible = False
            unlockContentMc.visible = True
            unlockContentMc.title2.text = gameStrings.SPRITE_BIO_UNLOCK_TITLE2
            if bioPicture.isUnlock:
                unlockContentMc.unlockCondition.title1.text = gameStrings.SPRITE_OHTER_BIO_UNLOCK_TITLE1
                unlockContentMc.unlockBtn.visible = False
                unlockContentMc.consumeBtn.visible = False
                self.updateOtherBioUnlockDesc(bioPicture.spriteId, bioPicture.bioId)
                self.updateOtherBioRewardDesc(bioPicture.spriteId, bioPicture.bioId)
            else:
                unlockContentMc.unlockCondition.title1.text = gameStrings.SPRITE_BIO_UNLOCK_TITLE1
                self.updateBioUnlockConditionMc(bioPicture.achieveId)
                self.updateOtherBioRewardDesc(bioPicture.spriteId, bioPicture.bioId)
                self.updateBioUnlockBtn(unlockContentMc, bioPicture.spriteId, bioPicture.bioId)
        else:
            unlockContentMc.visible = not bioPicture.isUnlock
            bioContentMc.visible = bioPicture.isUnlock
            self.stopCurrPlayBioSound()
            if bioPicture.isUnlock:
                self.updateBioContentMc(bioPicture.spriteId, bioPicture.bioId)
            else:
                unlockContentMc.unlockCondition.title1.text = gameStrings.SPRITE_BIO_UNLOCK_TITLE1
                unlockContentMc.title2.text = gameStrings.SPRITE_BIO_UNLOCK_TITLE2
                self.updateBioUnlockConditionMc(bioPicture.achieveId)
                self.updateBioUnlockRewardItems(bioPicture.spriteId, bioPicture.bioId)

    def updateOtherBioUnlockDesc(self, spriteId, bioId):
        unlockContentMc = self.widget.biographyPanel.biographyMc.unlockContentMc
        otherBioDesc = SSBD.data.get((spriteId, bioId), {}).get('otherBioUnlockDesc', '')
        unlockContentMc.unlockCondition.otherUnlockDesc.visible = True
        unlockContentMc.unlockCondition.unlockItemListMc.visible = False
        unlockContentMc.unlockCondition.otherUnlockDesc.textField.htmlText = otherBioDesc

    def updateOtherBioRewardDesc(self, spriteId, bioId):
        unlockContentMc = self.widget.biographyPanel.biographyMc.unlockContentMc
        otherBioRewardDesc = SSBD.data.get((spriteId, bioId), {}).get('otherBioRewardDesc', '')
        unlockContentMc.otherRewardDesc.visible = True
        unlockContentMc.otherRewardDesc.textField.htmlText = otherBioRewardDesc
        for i in range(UNLOCK_REWARD_ITEM_NUM):
            rewardSlot = unlockContentMc.getChildByName('rewardSlot%d' % i)
            rewardSlot.visible = False

    def updateBioContentMc(self, spriteId, bioId):
        bioContentMc = self.widget.biographyPanel.biographyMc.bioContentMc
        bioContentMc.bioName.text = SSBD.data.get((spriteId, bioId), ()).get('biographyName', '')
        bioContentMc.stopSoundBtn.addEventListener(events.BUTTON_CLICK, self.handleStopSoundBtnClick, False, 0, True)
        bioContentMc.playSoundBtn.addEventListener(events.BUTTON_CLICK, self.handlePlaySoundBtnClick, False, 0, True)
        if bioId == BIO_UNLOCK_NEED_HIDE_SOUND_BTN:
            bioContentMc.stopSoundBtn.visible = False
            bioContentMc.playSoundBtn.visible = False
        else:
            bioContentMc.stopSoundBtn.visible = False
            bioContentMc.playSoundBtn.visible = True
            biographySoundId = SSBD.data.get((spriteId, bioId), ()).get('biographySoundId', 0)
            bioContentMc.stopSoundBtn.biographySoundId = biographySoundId
            bioContentMc.playSoundBtn.biographySoundId = biographySoundId
            if not biographySoundId:
                bioContentMc.playSoundBtn.disabled = True
                TipManager.addTip(bioContentMc.playSoundBtn, gameStrings.SUMMONED_WAR_SPRITE_COMING_SOON)
            else:
                bioContentMc.playSoundBtn.disabled = False
                TipManager.removeTip(bioContentMc.playSoundBtn)
        bioContentMc.contentMc.itemRenderer = 'SummonedWarSpriteBiography_contentText'
        bioContentMc.contentMc.dataArray = []
        bioContentMc.contentMc.lableFunction = self.itemTextFunction
        bioContentMc.contentMc.itemHeightFunction = self.itemHeightFunction
        contentList = []
        biographyDesc = SSBD.data.get((spriteId, bioId), {}).get('biographyDesc', '')
        contentList.append({'desc': biographyDesc})
        bioContentMc.contentMc.dataArray = contentList

    def itemTextFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.contentText.htmlText = itemData.desc

    def itemHeightFunction(self, *args):
        if not self.contentTextMc:
            return
        itemData = ASObject(args[3][0])
        self.contentTextMc.contentText.htmlText = itemData.desc
        return GfxValue(self.contentTextMc.contentText.textHeight + 5)

    def updateBioUnlockConditionMc(self, achieveId):
        unlockContentMc = self.widget.biographyPanel.biographyMc.unlockContentMc
        unlockContentMc.unlockCondition.otherUnlockDesc.visible = False
        conditionListMc = unlockContentMc.unlockCondition.unlockItemListMc
        conditionListMc.visible = True
        self.widget.removeAllInst(conditionListMc)
        if achieveId == -1:
            return
        p = BigWorld.player()
        ad = AD.data.get(achieveId, {})
        achieveTargets = ad.get('achieveTargets', [])
        for i, targetId in enumerate(achieveTargets):
            if not ATD.data.has_key(targetId):
                continue
            atd = ATD.data.get(targetId, {})
            name = atd.get('name', '')
            var = atd.get('var', '')
            varMax = atd.get('varMax', 0)
            if not varMax:
                topValue = 0
                varMax = 1
                if targetId in p.summonSpriteBioTargets and p.summonSpriteBioTargets[targetId].done:
                    topValue = 1
            else:
                topValue = p.summonSpriteBioStatsInfo.get(var, 0)
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteBiography_unlockItem')
            itemMc.conditionName.htmlText = name
            itemMc.conditionValue.text = '%s/%s' % (str(topValue), str(varMax))
            itemMc.y = UNLOCK_ITEM_HEIGHT * i
            conditionListMc.addChild(itemMc)

    def updateBioUnlockRewardItems(self, spriteId, bioId):
        unlockContentMc = self.widget.biographyPanel.biographyMc.unlockContentMc
        unlockContentMc.otherRewardDesc.visible = False
        rewardList = SSBD.data.get((spriteId, bioId), {}).get('unlockRewardItems', [])
        for i in range(UNLOCK_REWARD_ITEM_NUM):
            rewardSlot = unlockContentMc.getChildByName('rewardSlot%d' % i)
            rewardSlot.visible = True
            rewardSlot.alpha = 0.45
            itemInfo = None
            if i < len(rewardList):
                rewardSlot.alpha = 1
                itemInfo = uiUtils.getGfxItemById(rewardList[i])
            rewardSlot.slot.setItemSlotData(itemInfo)
            ASUtils.setHitTestDisable(rewardSlot.slot, True if not itemInfo else False)

        self.updateBioUnlockBtn(unlockContentMc, spriteId, bioId)

    def updateBioUnlockBtn(self, unlockContentMc, spriteId, bioId):
        p = BigWorld.player()
        unlockContentMc.unlockBtn.visible = True
        unlockContentMc.unlockBtn.enabled = False
        if p.summonSpriteBio.has_key(spriteId) and p.summonSpriteBio[spriteId].has_key(bioId):
            if p.summonSpriteBio[spriteId][bioId].isDone and not p.summonSpriteBio[self.currSelectItemSpriteId][bioId].isUnlock:
                unlockContentMc.unlockBtn.enabled = True
        unlockContentMc.unlockBtn.spriteId = spriteId
        unlockContentMc.unlockBtn.bioId = bioId
        unlockContentMc.unlockBtn.addEventListener(events.BUTTON_CLICK, self.handleUnlockBtnClick, False, 0, True)
        ssbdData = SSBD.data.get((spriteId, bioId), {})
        unlockContentMc.consumeBtn.visible = True
        if not gameglobal.rds.configData.get('enableUnlockSpriteBioInMoney', False):
            unlockContentMc.consumeBtn.label = gameStrings.SUMMON_WAR_SPRITE_BIO_ENABLED
            unlockContentMc.consumeBtn.disabled = True
            return
        canPayForUnlock = ssbdData.get('canPayForUnlock', 0)
        coinCost = ssbdData.get('unlockCost', 0)
        reqLvPayForUnlock = ssbdData.get('reqLvPayForUnlock', 1)
        TipManager.removeTip(unlockContentMc.consumeBtn)
        if not canPayForUnlock:
            unlockContentMc.consumeBtn.label = gameStrings.SUMMON_WAR_SPRITE_BIO_NO_TIANBI_LOCK
            unlockContentMc.consumeBtn.disabled = True
        elif p.lv < reqLvPayForUnlock:
            tipDesc = gameStrings.SUMMON_WAR_SPRITE_BIO_TIANBI_LV_TIP % reqLvPayForUnlock
            TipManager.addTip(unlockContentMc.consumeBtn, tipDesc)
            unlockContentMc.consumeBtn.label = gameStrings.SUMMON_WAR_SPRITE_BIO_LESS_TIANBI_LV
            unlockContentMc.consumeBtn.disabled = True
        else:
            unlockContentMc.consumeBtn.label = gameStrings.SUMMON_WAR_SPRITE_BIO_CONSUME_TIANBI % coinCost
            unlockContentMc.consumeBtn.disabled = False
        unlockContentMc.consumeBtn.spriteId = spriteId
        unlockContentMc.consumeBtn.bioId = bioId
        unlockContentMc.consumeBtn.coinCost = coinCost
        unlockContentMc.consumeBtn.addEventListener(events.BUTTON_CLICK, self.handleConsumeBtnClick, False, 0, True)

    @ui.checkInventoryLock()
    def handleConsumeBtnClick(self, *args):
        e = ASObject(args[3][0])
        consumeBtn = e.currentTarget
        if consumeBtn.spriteId and consumeBtn.bioId:
            msg = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_BIO_CONSUME_TIANBI_DESC, '%d') % consumeBtn.coinCost
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realConsumeTianbi, consumeBtn.spriteId, consumeBtn.bioId))

    def realConsumeTianbi(self, spriteId, bioId):
        p = BigWorld.player()
        p.base.unlockSummonSpriteBioInMoney(spriteId, bioId, p.cipherOfPerson)

    def updateBioUnlockInfo(self, effectList):
        if not self.widget:
            return
        self.updateBiographyRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab2RedPot()
        if not self.isBiography:
            return
        for v in effectList:
            if v[0] == self.currSelectItemSpriteId and v[1] == self.currSelectBioId:
                bioPicture = self.widget.biographyPanel.biographyMc.getChildByName('bioPicture%d' % self.currSelectBioId)
                self.updateSpriteBioMc(bioPicture)
                self.updateBioSpriteItemRed()

    def updateBioUnlockSucc(self, spriteId, bioId):
        if not self.widget:
            return
        self.updateBiographyRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab2RedPot()
        if not self.isBiography:
            return
        if self.currSelectItemSpriteId == spriteId and self.currSelectBioId == bioId:
            bioPicture = self.widget.biographyPanel.biographyMc.getChildByName('bioPicture%d' % self.currSelectBioId)
            bioPicture.normalP.visible = True
            bioPicture.sealP.visible = False
            bioPicture.unLockSfx.visible = False
            bioPicture.selectedP.visible = True
            bioPicture.lockP.gotoAndPlay('unlock')
            gameglobal.rds.sound.playSound(BIOGRAPHY_UNLOCK_SOUND_ID)
            bioPicture.isUnlock = True
            self.updateSpriteBioMc(bioPicture)
            self.updateBioSpriteItemRed()

    def updateBioSpriteItemRed(self):
        if not self.currSelectItem or not self.currSelectItemSpriteId:
            return
        self.currSelectItem.redIcon.visible = self.checkRedPoint(self.currSelectItemSpriteId)

    def stopCurrPlayBioSound(self):
        if self.currPlayBioSoundId:
            gameglobal.rds.sound.stopSound(self.currPlayBioSoundId)
            self.currPlayBioSoundId = None

    def setBiographySelectSpriteIndex(self, spriteId, visible = False, bioId = None):
        self.currSelectItemSpriteId = spriteId
        self.isBiography = visible
        self.currSelectBioId = bioId

    def checkSpritePreBioIdsUnlock(self, spriteId, bioId):
        preBioIds = SSBD.data.get((spriteId, bioId), {}).get('preBioIds', ())
        if bioId in preBioIds:
            preBioIds.remove(bioId)
        p = BigWorld.player()
        for preBioId in preBioIds:
            if not p.summonSpriteBio.has_key(spriteId) or not p.summonSpriteBio[spriteId].has_key(preBioId):
                return False
            if not p.summonSpriteBio[spriteId][preBioId].isUnlock:
                return False

        return True
