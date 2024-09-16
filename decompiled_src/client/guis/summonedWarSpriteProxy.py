#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import tipUtils
import formula
import const
import skillDataInfo
from guis import events
from guis import ui
from uiTabProxy import UITabProxy
from asObject import RedPotManager
from Scaleform import GfxValue
from guis import uiUtils
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.summonedWarSpriteProperty import POINT_ATTR_NAME_LIST
from guis.summonedWarSpriteProperty import ADD_POINT_INDEX
from data import summon_sprite_info_data as SSID
from data import sys_config_data as SCD
from data import summon_sprite_skill_data as SSSD
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
from cdata import sprite_growth_category_data as SGCD
TAB_BTN_MAX_CNT = 5

class SummonedWarSpriteProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE, self.hide)
        self.type = 'summonedWarSprite'
        self.recordSpriteNumber = 0
        self.recordSpriteIndex = 0
        self.spriteIndex = 0
        self.feedItemPanel = None
        self.tipMc = None
        self.tipParentMc = None
        self.qualityColorDic = {0: 'white',
         1: 'green_1',
         2: 'blue_2',
         3: 'purple_3',
         4: 'golden_4'}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)
            self.reflowTabBtns()
            self.setTemplateState()

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            self.widget.tabBtn1.enabled = False
            self.widget.tabBtn2.enabled = False
            self.widget.tabBtn3.enabled = False
            self.widget.tabBtn4.enabled = False

    def reflowTabBtns(self):
        if not self.widget:
            return
        tabLen = len(self.tabList)
        posY = 56
        for tabIdx in xrange(TAB_BTN_MAX_CNT):
            tabBtn = getattr(self.widget, 'tabBtn%d' % tabIdx)
            if tabIdx < tabLen:
                tabBtn.visible = self.tabList[tabIdx]['visible']
                if tabBtn.visible:
                    tabBtn.y = posY
                    posY += 83
            else:
                tabBtn.visible = False

        RedPotManager.addRedPot(self.widget.tabBtn0, uiConst.SUMMONED_WAR_SPRITE_TAB_0, (0, 0), self.visiblePotFunTab0)
        RedPotManager.addRedPot(self.widget.tabBtn4, uiConst.SUMMONED_WAR_SPRITE_TAB_2, (0, 0), self.visiblePotFunTab2)

    def clearWidget(self):
        super(SummonedWarSpriteProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE)
        self.uiAdapter.summonedWarSpriteMine.resetHeadGen()
        self.uiAdapter.summonedWarSpriteMine.headGen = None
        self.uiAdapter.summonedWarSpriteBiography.resetHeadGen()
        self.uiAdapter.summonedWarSpriteBiography.headGen = None
        self.hideSubPanel()

    def clearAll(self):
        self.recordSpriteNumber = 0
        self.recordSpriteIndex = 0

    def reset(self):
        self.spriteIndex = 0
        self.feedItemPanel = None
        super(SummonedWarSpriteProxy, self).reset()

    def appendTab(self, tabList, view, proxy, tabName = '', visible = True):
        tabLen = len(tabList)
        tabList.append({'tabIdx': tabLen,
         'tabName': 'tabBtn%d' % tabLen,
         'view': view,
         'proxy': proxy,
         'visible': visible})

    def _getTabList(self):
        tabList = []
        self.appendTab(tabList, 'SummonedWarSpriteMineWidget', 'summonedWarSpriteMine', '', True)
        self.appendTab(tabList, 'SummonedWarSpriteGuardWidget', 'summonedWarSpriteGuard', '', True)
        self.appendTab(tabList, 'SummonedWarSpriteExplorePlanWidget', 'summonedWarSpriteExplorePlan', '', self.checkExploreBtnVisible())
        self.appendTab(tabList, 'SummonedWarSpriteXiuLianWidget', 'summonedWarSpriteXiuLian', '', self.checkXiuLianBtnVisible())
        self.appendTab(tabList, 'SummonedWarSpriteBiographyWidget', 'summonedWarSpriteBiography', '', True)
        return tabList

    def checkExploreBtnVisible(self):
        return gameglobal.rds.configData.get('enableExploreSprite', False)

    def checkXiuLianBtnVisible(self):
        return gameglobal.rds.configData.get('enableSpriteGrowth', False)

    def show(self, showTabIndex, spriteIndex = 0, feedItemPanel = None, subTabIdx = None, isGotoAddPrivity = False):
        if not gameglobal.rds.configData.get('enableSummonedSprite', False):
            return
        p = BigWorld.player()
        if not p.summonSpriteList:
            p.showGameMsg(GMDD.data.NO_SUMMONED_SPRITE_TO_SHOW, ())
            return
        self.showTabIndex = showTabIndex
        self.spriteIndex = spriteIndex
        self.feedItemPanel = feedItemPanel
        if showTabIndex == uiConst.WAR_SPRITE_TAB_INDEX0:
            self.uiAdapter.summonedWarSpriteMine.isGotoAddPrivity = isGotoAddPrivity
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
            if feedItemPanel:
                self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE)
        if subTabIdx:
            tabProxy = getattr(self.uiAdapter, self._getTabList()[showTabIndex]['proxy'])
            hasattr(tabProxy, 'setSubTabIdx') and tabProxy.setSubTabIdx(subTabIdx)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        self.updateXiuLianBtn()

    def onTabChanged(self, *args):
        super(SummonedWarSpriteProxy, self).onTabChanged(*args)
        self.hideSubPanel()
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            self.updateSpriteTab0RedPot()
            proxy = self.getCurrentProxy()
            if proxy and hasattr(proxy, 'refreshInfo'):
                proxy.refreshInfo()
                if self.spriteIndex and hasattr(proxy, 'setSpriteSelected'):
                    proxy.setSpriteSelected(self.spriteIndex, 'overviewTabBtn')
                    self.spriteIndex = 0
                if self.feedItemPanel and hasattr(proxy, 'openSpriteFeedPanel'):
                    proxy.openSpriteFeedPanel(self.feedItemPanel)
                    self.feedItemPanel = None
            return

    @ui.uiEvent(uiConst.WIDGET_SUMMONED_WAR_SPRITE, events.EVENT_SPRITE_PROPS_CHANGED)
    def onSpritePropChange(self, event = None):
        proxy = self.getCurrentProxy()
        if event and proxy and hasattr(proxy, 'refreshSpriteProp'):
            index = event.data
            proxy.refreshSpriteProp(index)

    def saveSpriteIndex(self, number, index):
        self.recordSpriteNumber = number
        self.recordSpriteIndex = index

    def hideSubPanel(self):
        self.uiAdapter.summonedWarSpriteReRandom.hide()
        self.uiAdapter.summonedWarSpriteSwallow.hide()
        self.uiAdapter.summonedWarSpriteAwake.hide()
        self.uiAdapter.summonedWarSpriteUp.hide()
        self.uiAdapter.summonedWarSpriteLunhui.hide()
        self.uiAdapter.summonedWarSpriteFamiliar.hide()
        self.uiAdapter.summonedWarSpriteChat.hide()
        self.uiAdapter.summonedWarSpriteSkillTransfer.hide()
        self.uiAdapter.summonedWarSpriteUpGrade.hide()
        self.uiAdapter.summonedWarSpriteRareTransfer.hide()

    def visiblePotFunTab0(self, *args):
        p = BigWorld.player()
        for spriteInfo in p.summonSpriteList.values():
            spriteIndex = spriteInfo.get('index', 0)
            if spriteIndex and gameglobal.rds.ui.summonedWarSpriteMine.visibleItemRedPoint(spriteIndex):
                return GfxValue(True)

        return GfxValue(False)

    def updateSpriteTab0RedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_TAB_0)

    def visiblePotFunTab2(self, *args):
        isRedPot = gameglobal.rds.ui.summonedWarSpriteBiography.checkAllSpriteBioRedPoint()
        return GfxValue(isRedPot)

    def updateSpriteTab2RedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_TAB_2)

    def showSpriteDetailTip(self, spriteInfoDict, type, posX = -1, posY = -1):
        if not spriteInfoDict:
            return
        else:
            if self.tipParentMc is None:
                toolTipManager = ASObject(gameglobal.rds.ui.uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.utils.TooltipManager')).Invoke('getInstance'))
                self.tipParentMc = toolTipManager.getCanvas()
            stage = self.tipParentMc.stage
            if self.tipMc is None:
                self.tipMc = ASUtils.getClsByClsName('Tip_SpriteDetailTip')
                ASUtils.setHitTestDisable(self.tipMc, False)
                stage.addEventListener('showTooltip', self.handleShowToolTip, False, 0, False)
                stage.addEventListener(events.MOUSE_DOWN, self.handleHideSprite, True, 0, False)
            tipData = self.getSpriteDetailTipData(spriteInfoDict, False, rtype=type)
            self.tipMc.tipData = tipData
            x = stage.mouseX if posX < 0 else posX
            y = stage.mouseY if posY < 0 else posY
            if x + self.tipMc.width > stage.stageWidth:
                x -= self.tipMc.width
            if y + self.tipMc.height > stage.stageHeight:
                y = stage.stageHeight - self.tipMc.height
            self.tipMc.x = x
            self.tipMc.y = y
            self.tipParentMc.addChild(self.tipMc)
            self._setupSecondaryTip(tipData)
            TipManager.hideTip()
            return

    def _setupSecondaryTip(self, tipData):
        ASUtils.setHitTestDisable(self.tipMc.leftTipMC.headSlot, True)
        talentSkillCount = len(tipData['talentSkillInfos'])
        learnedSkillCount = len(tipData['learnedSkillInfos'])
        bonusCount = len(tipData['bonusInfos'])
        for i in range(8):
            if i < 2:
                abSkillSlot = self.tipMc.leftTipMC.__getattr__('abSkillSlot' + str(i))
                abSkillSlotCover = self.tipMc.leftTipMC.__getattr__('blackCover' + str(i))
                ASUtils.setHitTestDisable(abSkillSlotCover, True)
                abSkillSlot.validateNow()
                ASUtils.setHitTestDisable(abSkillSlot, False)
                TipManager.addTipByType(abSkillSlot, tipUtils.TYPE_SKILL, tipData['abSkillInfos'][i]['tipData'], False, 'upLeft')
                if i < bonusCount:
                    bonusDescTxt = self.tipMc.leftTipMC.talentMC.bonusMc.__getattr__('bonusDesc' + str(i))
                    TipManager.addTip(bonusDescTxt, tipData['bonusInfos'][i]['bonusTip'])
            if i < 4:
                talentMc = self.tipMc.leftTipMC.talentMC.__getattr__('skillMC' + str(i))
                ASUtils.setHitTestDisable(talentMc.bonusPoint, True)
                talentSlot = talentMc.slot
                if i < talentSkillCount:
                    talentSlot.validateNow()
                    ASUtils.setHitTestDisable(talentSlot, False)
                    TipManager.addTipByType(talentSlot, tipUtils.TYPE_SKILL, tipData['talentSkillInfos'][i]['tipData'], False, 'upLeft')
                else:
                    TipManager.removeTip(talentSlot)
            learnedSkillSlot = self.tipMc.leftTipMC.__getattr__('skillMC' + str(i)).slot
            if i < learnedSkillCount:
                learnedSkillSlot.validateNow()
                ASUtils.setHitTestDisable(learnedSkillSlot, False)
                TipManager.addTipByType(learnedSkillSlot, tipUtils.TYPE_SKILL, tipData['learnedSkillInfos'][i]['tipData'], False, 'upLeft')
            else:
                TipManager.removeTip(learnedSkillSlot)

    def handleShowToolTip(self, *args):
        if self.tipParentMc is None or self.tipMc is None or self.tipMc.parent != self.tipParentMc:
            return
        else:
            target = ASObject(args[3][0]).target
            isSubTipOfSpriteDetailTip = False
            for i in range(4):
                if target == self.tipMc.leftTipMC:
                    isSubTipOfSpriteDetailTip = True
                    break
                else:
                    target = target.parent

            if not isSubTipOfSpriteDetailTip:
                self.tipParentMc.removeChild(self.tipMc)
            return

    def handleHideSprite(self, *args):
        if self.tipParentMc and self.tipMc:
            self.tipParentMc.removeChild(self.tipMc)

    def getSpriteDetailTipData(self, spriteInfoDict, invokedByAS = True, rtype = ''):
        data = {}
        spriteId = spriteInfoDict[const.SPRITE_DICT_INDEX_spriteId]
        spriteConfig = SSID.data.get(spriteId, {})
        isAwake = spriteInfoDict[const.SPRITE_DICT_INDEX_juexing]
        bonusSkills = spriteInfoDict[const.SPRITE_DICT_INDEX_bonus]
        talentSkill0, talentSkill1 = gameglobal.rds.ui.summonedWarSpriteMine.getBonusToSKillIds(bonusSkills)
        famiEfflv = spriteInfoDict[const.SPRITE_DICT_INDEX_famiEffLv]
        talentSkills = spriteInfoDict[const.SPRITE_DICT_INDEX_naturals]
        upgradeStage = spriteInfoDict[const.SPRITE_DICT_INDEX_upgradeStage] if const.SPRITE_DICT_INDEX_upgradeStage in spriteInfoDict else 0
        data['qualityColor'] = self.qualityColorDic[len(talentSkills)]
        data['headIconPath'] = 'summonedSprite/icon/%s.dds' % spriteConfig.get('spriteIcon', '000')
        data['spriteName'] = spriteInfoDict[const.SPRITE_DICT_INDEX_name]
        data['combatValue'] = spriteInfoDict[const.SPRITE_DICT_INDEX_combatScore]
        data['abSkillInfos'] = [self.getSkillInfo(spriteInfoDict, 'trait'), self.getSkillInfo(spriteInfoDict, 'awake')]
        talentInfoList = data['talentSkillInfos'] = []
        for skillType in talentSkills:
            info = {}
            skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
            lv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
            info['iconPath'] = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            info['skillName'] = skillInfo.getSkillData('sname', '')
            signId = SSSD.data.get(skillType, {}).get('universalLabel', 100)
            info['typeFrame'] = 'sign_%d' % signId
            info['tipData'] = {'skillId': skillId,
             'lv': lv}
            if skillType in talentSkill0 and skillType in talentSkill1:
                info['pointFrame'] = 'point2'
            elif skillType in talentSkill0:
                info['pointFrame'] = 'point0'
            elif skillType in talentSkill1:
                info['pointFrame'] = 'point1'
            else:
                info['pointFrame'] = ''
            talentInfoList.append(info)

        bonusInfos = data['bonusInfos'] = []
        for bonusId in bonusSkills:
            info = {}
            info['bonusName'] = SSSD.data.get(bonusId, {}).get('bonusName', '')
            info['bonusTip'] = SSSD.data.get(bonusId, {}).get('bonusDesc', '')
            bonusInfos.append(info)

        learndSkillInfos = data['learnedSkillInfos'] = []
        for skillData in spriteInfoDict[const.SPRITE_DICT_INDEX_learns]:
            info = {}
            skillId = SSSD.data.get(skillData[0], {}).get('virtualSkill', 0)
            if skillId != 0:
                skillInfo = skillDataInfo.ClientSkillInfo(skillId)
                info['iconPath'] = iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                info['skillName'] = skillInfo.getSkillData('sname', '')
            info['locked'] = skillData[1] == 0
            info['tipData'] = {'skillId': skillId,
             'lv': 1}
            learndSkillInfos.append(info)

        familiar = max(spriteInfoDict[const.SPRITE_DICT_INDEX_famiEffLv] - spriteInfoDict[const.SPRITE_DICT_INDEX_famiEffAdd], 0)
        data['typeName'] = spriteConfig.get('spriteRace', '')
        spriteBindTypeDesc = SCD.data.get('spriteBindTypeDesc', ('', ''))
        data['bindType'] = spriteBindTypeDesc[1] if spriteInfoDict[const.SPRITE_DICT_INDEX_bindType] else spriteBindTypeDesc[0]
        data['lv'] = '%d' % spriteInfoDict[const.SPRITE_DICT_INDEX_lv]
        data['loveLv'] = '%d+<font color=\"#00FF00\">%d</font>' % (familiar, spriteInfoDict[const.SPRITE_DICT_INDEX_famiEffAdd])
        data['quality'] = self.getGrade(spriteInfoDict)
        data['isClever'] = spriteInfoDict[const.SPRITE_DICT_INDEX_clever]
        boneLv = spriteInfoDict[const.SPRITE_DICT_INDEX_boneLv]
        baseGrowthRatio = spriteInfoDict[const.SPRITE_DICT_INDEX_baseGrowthRatio]
        spriteBoneGrowth = spriteConfig.get('spriteBoneGrowth', 0)
        baseGrowthRatio, boneRatio = gameglobal.rds.ui.summonedWarSpriteUp.getSpriteGrowthRatio(baseGrowthRatio, isAwake, boneLv, spriteBoneGrowth)
        data['growthRatioText'] = '%.3f+<font color=\"#00FF00\">%.3f</font>' % (baseGrowthRatio, boneRatio)
        data['starCount'] = utils.getSpriteGrowthRatioStar(spriteId, spriteInfoDict[const.SPRITE_DICT_INDEX_growthRatio]) + 1
        maxBoneLv = spriteConfig.get('spriteBoneTimes', 0)
        data['growthCountText'] = '%d/%d' % (boneLv, maxBoneLv)
        baseAttrList = data['baseAttributes'] = []
        for i in range(5):
            attrName = POINT_ATTR_NAME_LIST[i]
            finalAttr = spriteInfoDict[getattr(const, 'SPRITE_DICT_INDEX_' + attrName)]
            index = ADD_POINT_INDEX[attrName]
            oriAttr = spriteInfoDict[const.SPRITE_DICT_INDEX_oriPrimaryProp][index]
            aptitudeName = utils.APTITUDE_NAME_LIST[i]
            aptitudeOriginMax = utils.getAptitudeMax(spriteId, aptitudeName)
            aptitudeMax = formula.getSpriteAptitudeVal(aptitudeOriginMax, data['isClever'], isAwake, spriteId, upgradeStage)
            aptitude = spriteInfoDict[getattr(const, 'SPRITE_DICT_INDEX_' + aptitudeName)]
            baseAttrList += [['%d+%d' % (oriAttr, finalAttr - oriAttr), aptitude, aptitudeMax]]

        data['mainAttributes'] = spriteInfoDict[const.SPRITE_DICT_INDEX_vPropCache]
        if rtype == 'zmjSprite':
            spriteDps = spriteInfoDict.get('spriteDps', 0)
            if spriteDps > uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD:
                spriteDps = gameStrings.ZMJ_DMG_SIMPLIFY_TXT % (spriteDps / uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD,)
            data['spriteDps'] = spriteDps
            data['showSpriteDps'] = True
        if invokedByAS:
            return uiUtils.dict2GfxDict(data, True)
        return data

    def getSkillInfo(self, spriteInfoDict, skillType):
        isAwake = spriteInfoDict[const.SPRITE_DICT_INDEX_juexing]
        bonusSkills = spriteInfoDict[const.SPRITE_DICT_INDEX_bonus]
        famiEfflv = spriteInfoDict[const.SPRITE_DICT_INDEX_famiEffLv]
        index = const.SPRITE_DICT_INDEX_awake if skillType == 'awake' else const.SPRITE_DICT_INDEX_trait
        sssdData = SSSD.data.get(spriteInfoDict[index], {})
        skillAddId, skillLvAdd = sssdData.get('skillAddVirtualLv', (0, 0))
        addVirtualLv = skillLvAdd if skillAddId in bonusSkills else 0
        effLv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, skillType, const.DEFAULT_SKILL_LV_SPRITE)
        lv = min(effLv + addVirtualLv, const.MAX_SKILL_LEVEL)
        skillId = sssdData.get('virtualSkill', 0)
        skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
        traitSkillInfo = {}
        traitSkillInfo['iconPath'] = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
        traitSkillInfo['skillName'] = skillInfo.getSkillData('sname', '')
        traitSkillInfo['locked'] = skillType == 'awake' and not isAwake
        traitSkillInfo['tipData'] = {'skillId': skillId,
         'lv': lv}
        return traitSkillInfo

    def getGrade(self, spriteInfoDict):
        props = {}
        props['baseGrowthRatio'] = spriteInfoDict[const.SPRITE_DICT_INDEX_baseGrowthRatio]
        props['growthRatio'] = spriteInfoDict[const.SPRITE_DICT_INDEX_growthRatio]
        propNameList = utils.APTITUDE_ORI_NAME_LIST + utils.APTITUDE_NAME_LIST
        for propName in propNameList:
            props[propName] = spriteInfoDict[getattr(const, 'SPRITE_DICT_INDEX_' + propName)]

        return utils.getSpriteScoreInfo(spriteInfoDict[const.SPRITE_DICT_INDEX_spriteId], props)[2]

    def updateXiuLianBtn(self):
        p = BigWorld.player()
        if self.checkXiuLianBtnVisible():
            parentIds = sorted(SGCD.data.keys())
            firstId = parentIds[0]
            lvLimit = SGCD.data.get(firstId, {}).get('lvLimit', 0)
            jingJieLimit = SGCD.data.get(firstId, {}).get('jingJieLimit', 0)
            if p.lv >= lvLimit and p.jingJie >= jingJieLimit:
                self.widget.tabBtn3.disabled = False
                TipManager.removeTip(self.widget.tabBtn3)
            else:
                self.widget.tabBtn3.disabled = True
                color1 = '#231d1b' if p.lv >= lvLimit else '#d34024'
                color2 = '#231d1b' if p.jingJie >= jingJieLimit else '#d34024'
                szJingjieName = gameStrings.SPRITE_XIU_LIAN_JINGJIE_TO_NAME.get(jingJieLimit, '')
                msgTip = gameStrings.SPRITE_XIU_LIAN_BTN_CONDITION_TIP % (uiUtils.toHtml(lvLimit, color1), uiUtils.toHtml(szJingjieName, color2))
                TipManager.addTip(self.widget.tabBtn3, msgTip)

    def checkXiuLianLvAndJinejie(self):
        if not self.checkXiuLianBtnVisible():
            return False
        p = BigWorld.player()
        parentIds = sorted(SGCD.data.keys())
        firstId = parentIds[0]
        lvLimit = SGCD.data.get(firstId, {}).get('lvLimit', 0)
        jingJieLimit = SGCD.data.get(firstId, {}).get('jingJieLimit', 0)
        if p.lv >= lvLimit and p.jingJie >= jingJieLimit:
            return True
        return False
