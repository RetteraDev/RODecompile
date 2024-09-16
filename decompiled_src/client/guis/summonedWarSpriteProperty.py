#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteProperty.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import events
import utils
import tipUtils
import formula
from asObject import ASObject
from callbackHelper import Functor
from guis import uiConst
from guis.asObject import MenuManager
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SYSCD
from guis import uiUtils
from guis.asObject import TipManager
PROPERTY_HEIGHT = 27
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
ATTR_NAME_LIST = [gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_28,
 gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_28_1,
 gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_28_2,
 gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_28_3,
 gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_28_4]

class SummonedWarSpriteMineProperty(object):

    def __init__(self, proxy):
        super(SummonedWarSpriteMineProperty, self).__init__()
        self.parentProxy = proxy
        self.addPointPanel = None
        self.mainPropInfo = uiUtils.getSpritePropsArray(uiConst.MAIN_PROPS)
        self.plusPropInfo = uiUtils.getSpritePropsArray(uiConst.PLUS_PROPS)

    def getWidget(self):
        return self.parentProxy.widget

    def getCurSelectSpriteInfo(self):
        idx = self.parentProxy.currSelectItemSpriteIndex
        return BigWorld.player().summonSpriteList.get(idx, {})

    def getManualPoint(self):
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        return currSelectWarSpriteInfo.get('props', {}).get('manualPoint', 0)

    def getAvailableManualPoint(self):
        addedPoint = 0
        manualPoint = self.getManualPoint()
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            ncMC = self.getAttrNSMC(POINT_ATTR_NAME_LIST[idx])
            if ncMC:
                realValue = int(currSelectWarSpriteInfo.get('props').get(POINT_ATTR_NAME_LIST[idx], 0))
                addedPoint = addedPoint + ncMC.value - realValue

        return int(manualPoint - addedPoint)

    def getAttrNSMC(self, name):
        mcName = name + 'NS'
        widget = self.getWidget()
        return getattr(widget.mineWarSpritePanel.attributeMc, mcName, None)

    def hideWidget(self):
        self.addPointPanel = None

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            spriteInfo = self.getCurSelectSpriteInfo()
            spriteId = spriteInfo.get('spriteId', 0)
            attributeMc = widget.mineWarSpritePanel.attributeMc
            attributeMc.attribute_planPointBtn.addEventListener(events.MOUSE_CLICK, self.handlePlanPoint, False, 1, True)
            attributeMc.attribute_washPointBtn.addEventListener(events.MOUSE_CLICK, self.handleWashPoint, False, 1, True)
            attributeMc.attribute_savePointBtn.addEventListener(events.MOUSE_CLICK, self.handleSavePoint, False, 1, True)
            attributeMc.washAptitudeBtn.addEventListener(events.MOUSE_CLICK, self.handleWashAptitudeBtn, False, 1, True)
            attributeMc.upBtn.addEventListener(events.MOUSE_CLICK, self.handleUpBtnClick, False, 1, True)
            manualPoint = self.getManualPoint()
            props = spriteInfo.get('props', {})
            for idx in xrange(len(POINT_ATTR_NAME_LIST)):
                ncMC = self.getAttrNSMC(POINT_ATTR_NAME_LIST[idx])
                if ncMC:
                    ncMC.nameTF.text = ATTR_NAME_LIST[idx]
                    value = props.get(POINT_ATTR_NAME_LIST[idx], 0)
                    addIdx = ADD_POINT_INDEX[POINT_ATTR_NAME_LIST[idx]]
                    oriProp = props.get('oriPrimaryProp', [0] * 5)[addIdx]
                    tip = SYSCD.data.get('spriteAttrDetailTips', {}).get(POINT_ATTR_NAME_LIST[idx], '%s, %s')
                    TipManager.addTip(ncMC.nameTF, tip % (oriProp, value - oriProp), tipUtils.TYPE_DEFAULT_BLACK)
                    value = int(value)
                    ncMC.minimum = value
                    ncMC.maximum = value + manualPoint
                    ncMC.value = value
                    ncMC.labelFunction = self.attrNSValueLabelFunction

            if self.addPointPanel == None:
                self.addPointPanel = widget.getInstByClsName('SummonedWarSpriteMine_AddPointPlan')
            attributeMc.cleverMC.visible = props.get('clever', 0)
            cleverTip = SYSCD.data.get('spriteCleverTips', gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_108)
            TipManager.addTip(attributeMc.cleverMC, cleverTip, tipUtils.TYPE_DEFAULT_BLACK)
            title = utils.getSpriteScoreInfo(spriteId, props)[2]
            attributeMc.attributeGradeText.htmlText = title
            TipManager.addTip(attributeMc.attributeGradeTitleTxt, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(attributeMc.attributeGradeText, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(attributeMc.growthRatioTxt, SYSCD.data.get('spriteGrowthRatioTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(attributeMc.growthRatioTF, SYSCD.data.get('spriteGrowthRatioTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
            self.resetGrowthStarInfo()
            self.resetAptitudeInfo()
            self.refreshSpriteMainProperty()
            self.refreshSpritePlusProperty()
            self.setTemplateState()
            return

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            widget = self.getWidget()
            attributeMc = widget.mineWarSpritePanel.attributeMc
            attributeMc.attribute_planPointBtn.visible = False
            attributeMc.attribute_washPointBtn.visible = False
            attributeMc.attribute_savePointBtn.visible = False
            attributeMc.upBtn.visible = False
            attributeMc.washAptitudeBtn.visible = False

    def handlePlanPoint(self, *args):
        e = ASObject(args[3][0])
        target = e.target
        self.setAddPointMCState(target)

    def setAddPointMCState(self, target):
        widget = self.getWidget()
        menuParent = widget.mineWarSpritePanel.attributeMc
        spriteInfo = self.getCurSelectSpriteInfo()
        summonLvUpManualAbilityPoint = SYSCD.data.get('summonLvUpManualAbilityPoint', 0)
        propManualPointScheme = spriteInfo.get('propManualPointScheme', [])
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            attrNSMC = getattr(self.addPointPanel, POINT_ATTR_NAME_LIST[idx] + 'NS', None)
            if attrNSMC:
                attrNSMC.nameTF.text = ATTR_NAME_LIST[idx]
                attrNSMC.maximum = summonLvUpManualAbilityPoint
                propIdx = ADD_POINT_INDEX[POINT_ATTR_NAME_LIST[idx]]
                attrNSMC.value = propManualPointScheme[propIdx] if propIdx < len(propManualPointScheme) else 0
                attrNSMC.labelFunction = self.addPointNSValueLabelFunction
                TipManager.addTip(attrNSMC.nameTF, SYSCD.data.get('spriteAttrTips', {}).get(POINT_ATTR_NAME_LIST[idx], idx), tipUtils.TYPE_DEFAULT_BLACK)

        self.addPointPanel.availableDescTF.text = gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_161 % summonLvUpManualAbilityPoint
        self.addPointPanel.saveAddPointBtn.addEventListener(events.MOUSE_CLICK, self.saveAddPointPlan, False, 1, True)
        self.addPointPanel.applicationBtn.addEventListener(events.MOUSE_CLICK, self.applyAddPointPlan, False, 1, True)
        self.addPointPanel.closeBtn.addEventListener(events.MOUSE_CLICK, self.closeAddPointPanel, False, 1, True)
        MenuManager.getInstance().showMenu(target, self.addPointPanel, {'x': target.x,
         'y': target.y + target.height}, False, menuParent)

    def resetGrowthStarInfo(self):
        widget = self.getWidget()
        spriteInfo = self.getCurSelectSpriteInfo()
        growthRatio = spriteInfo.get('props', {}).get('growthRatio', 0)
        widget.mineWarSpritePanel.attributeMc.growthRatioTF.text = str('%.3f' % growthRatio)
        star = utils.getSpriteGrowthRatioStar(spriteInfo.get('spriteId', 0), growthRatio)
        for i in xrange(const.SUMMON_SPRITE_MAX_STAR):
            starMc = getattr(widget.mineWarSpritePanel.attributeMc, 'star%s' % i)
            if starMc:
                starMc.visible = star >= i

    def resetAptitudeInfo(self):
        widget = self.getWidget()
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        upgradeStage = spriteInfo.get('upgradeStage', 0)
        props = spriteInfo.get('props')
        clever = props.get('clever', 0)
        juexing = props.get('juexing', 0)
        for idx in xrange(len(utils.APTITUDE_NAME_LIST)):
            aptitudeName = utils.APTITUDE_NAME_LIST[idx]
            oriName = utils.APTITUDE_NAME_MAP.get(aptitudeName)
            attrNSMC = getattr(widget.mineWarSpritePanel.attributeMc, aptitudeName + 'Bar', None)
            aptitude = int(props.get(aptitudeName, 0))
            aptitudeOrigin = int(props.get(oriName, 0))
            aptitudeOriginMax = utils.getAptitudeMax(spriteId, aptitudeName)
            aptitudeMax = formula.getSpriteAptitudeVal(aptitudeOriginMax, clever, juexing, spriteId, upgradeStage)
            if attrNSMC:
                attrNSMC.maxValue = aptitudeMax
                attrNSMC.currentValues = [aptitude, 0, 0]
            if clever:
                tip = SYSCD.data.get('spriteAptitudeCleverTips', {}).get(aptitudeName, '%d%d%d') % (aptitude, aptitudeOrigin, aptitude - aptitudeOrigin)
            else:
                tip = SYSCD.data.get('spriteAptitudeNormalTips', {}).get(aptitudeName, '%d') % (aptitude,)
            aptitudeTF = getattr(widget.mineWarSpritePanel.attributeMc, aptitudeName + 'TF', None)
            if aptitudeTF:
                aptitudeTF.text = str(aptitude) + '/' + str(aptitudeMax)
                TipManager.addTip(aptitudeTF, tip, tipUtils.TYPE_DEFAULT_BLACK)
            txt = getattr(widget.mineWarSpritePanel.attributeMc, aptitudeName + 'Txt', None)
            if txt:
                TipManager.addTip(txt, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def getAvailableAddedPoint(self):
        summonLvUpManualAbilityPoint = SYSCD.data.get('summonLvUpManualAbilityPoint', 0)
        sumValue = 0
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            attrNSMC = getattr(self.addPointPanel, POINT_ATTR_NAME_LIST[idx] + 'NS', None)
            if attrNSMC:
                sumValue = sumValue + attrNSMC.value

        return summonLvUpManualAbilityPoint - sumValue

    def resetAddPintNSEnable(self):
        availableAddedPoint = self.getAvailableAddedPoint()
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            attrNSMC = getattr(self.addPointPanel, POINT_ATTR_NAME_LIST[idx] + 'NS', None)
            if attrNSMC:
                value = attrNSMC.value
                attrNSMC.maximum = value + availableAddedPoint
                attrNSMC.nextBtn.enabled = False if availableAddedPoint <= 0 else True
                attrNSMC.prevBtn.enabled = False if value <= 0 else True
                attrNSMC.nextBtn.repeatInterval = attrNSMC.prevBtn.repeatInterval = 20

    def addPointNSValueLabelFunction(self, *args):
        value = int(args[3][0].GetNumber())
        self.resetAddPintNSEnable()
        return GfxValue(str(value))

    def closeAddPointPanel(self, *args):
        self.addPointPanel.visible = False

    def saveAddPointPlan(self, *args):
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        pow, intV, phy, spr, agi = self.getAddPointPlan()
        sumValue = pow + intV + phy + spr + agi
        summonLvUpManualAbilityPoint = SYSCD.data.get('summonLvUpManualAbilityPoint', 0)
        if sumValue > summonLvUpManualAbilityPoint or min((pow,
         intV,
         phy,
         spr,
         agi)) < 0:
            return
        gamelog.debug('m.l@SummonedWarSpriteMineProperty.saveAddPointPlan', selectedIndex, pow, intV, phy, spr, agi)
        BigWorld.player().base.saveSpriteManualPointScheme(selectedIndex, pow, intV, phy, spr, agi)
        self.addPointPanel.visible = False

    def applyAddPointPlan(self, *args):
        p = BigWorld.player()
        pow, intV, phy, spr, agi = self.getAddPointPlan()
        sumValue = pow + intV + phy + spr + agi
        availablePoints = self.getAvailableManualPoint()
        if availablePoints < sumValue:
            p.showGameMsg(GMDD.data.SUMMONED_SPRITE_NOENOUGH_POINT_TO_ADDED, ())
            return
        self.saveAddPointPlan()
        if sumValue <= 0:
            return
        cnt = int(availablePoints / sumValue)
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        BigWorld.player().base.onManualAddPorpPoint(selectedIndex, pow * cnt, intV * cnt, phy * cnt, spr * cnt, agi * cnt)
        p.showGameMsg(GMDD.data.SUMMONED_SPRITE_POINT_ADD_SUCC, ())

    def getAddPointPlan(self):
        pow = self.addPointPanel.attrPwNS.value
        intV = self.addPointPanel.attrIntNS.value
        phy = self.addPointPanel.attrPhyNS.value
        spr = self.addPointPanel.attrSprNS.value
        agi = self.addPointPanel.attrAgiNS.value
        return (pow,
         intV,
         phy,
         spr,
         agi)

    def handleWashPoint(self, *args):
        p = BigWorld.player()
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = currSelectWarSpriteInfo.get('index', -99)
        if currSelectWarSpriteInfo.get('resetPropPointCnt', 0) > 0:
            cost = SYSCD.data.get('costResetSpriteManualPoint', 20000)
            msg = uiUtils.getTextFromGMD(GMDD.data.SUMMONED_SPRITE_WASH_COST_MSG, '%d') % cost
        else:
            msg = SYSCD.data.get('summonedWarSpriteWashPointMsg', gameStrings.TEXT_SUMMONEDWARSPRITEPROPERTY_289)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.resetWashPointCallback, selectedIndex), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1, isModal=False, msgType='pushLoop', textAlign='center')

    def resetWashPointCallback(self, idx):
        gamelog.debug('m.l@SummonedWarSpriteMineProperty.resetWashPointCallback', idx)
        BigWorld.player().base.resetManuallyAddedPropPoint(idx)

    def handleSavePoint(self, *args):
        widget = self.getWidget()
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        props = currSelectWarSpriteInfo.get('props', {})
        pow = widget.mineWarSpritePanel.attributeMc.attrPwNS.value - props.get('attrPw', 0)
        int = widget.mineWarSpritePanel.attributeMc.attrIntNS.value - props.get('attrInt', 0)
        phy = widget.mineWarSpritePanel.attributeMc.attrPhyNS.value - props.get('attrPhy', 0)
        spr = widget.mineWarSpritePanel.attributeMc.attrSprNS.value - props.get('attrSpr', 0)
        agi = widget.mineWarSpritePanel.attributeMc.attrAgiNS.value - props.get('attrAgi', 0)
        if not pow and not int and not phy and not spr and not agi:
            return
        selectedIndex = currSelectWarSpriteInfo.get('index', -99)
        gamelog.debug('m.l@SummonedWarSpriteMineProperty.handleSavePoint', selectedIndex, pow, int, phy, spr, agi)
        BigWorld.player().base.onManualAddPorpPoint(selectedIndex, pow, int, phy, spr, agi)

    def handleWashAptitudeBtn(self, *args):
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        gameglobal.rds.ui.summonedWarSpriteReRandom.show(currSelectWarSpriteInfo)

    def handleUpBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteUp.show()

    def reset(self):
        pass

    def resetAttrNSEnable(self):
        widget = self.getWidget()
        availableManualPoint = self.getAvailableManualPoint()
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        for idx in xrange(len(POINT_ATTR_NAME_LIST)):
            ncMC = self.getAttrNSMC(POINT_ATTR_NAME_LIST[idx])
            if ncMC:
                value = ncMC.value
                ncMC.maximum = value + availableManualPoint
                realValue = int(currSelectWarSpriteInfo.get('props').get(POINT_ATTR_NAME_LIST[idx], 0))
                ncMC.nextBtn.enabled = False if availableManualPoint <= 0 else True
                ncMC.prevBtn.enabled = False if value <= realValue else True
                ncMC.nextBtn.visible = ncMC.prevBtn.visible = ncMC.nextBtn.enabled or ncMC.prevBtn.enabled
                ncMC.nextBtn.repeatInterval = ncMC.prevBtn.repeatInterval = 20

        widget.mineWarSpritePanel.attributeMc.manualPointTF.text = availableManualPoint
        summonLvUpManualAbilityPoint = SYSCD.data.get('summonLvUpManualAbilityPoint', 0)
        lv = currSelectWarSpriteInfo.get('props', {}).get('lv', 1)
        manualPoint = self.getManualPoint()
        washPointEnable = summonLvUpManualAbilityPoint * (lv - 1) > manualPoint
        widget.mineWarSpritePanel.attributeMc.attribute_washPointBtn.enabled = washPointEnable

    def attrNSValueLabelFunction(self, *args):
        value = int(args[3][0].GetNumber())
        e = ASObject(args[3][1])
        currSelectWarSpriteInfo = self.getCurSelectSpriteInfo()
        realValue = int(currSelectWarSpriteInfo.get('props').get(e.name[:-2], 0))
        retStr = "<font color=\'#D58115\'>%d</font> " % realValue
        if value - realValue > 0:
            retStr = retStr + "<font color=\'#40C133\'>+ %d</font>" % (value - realValue)
        self.resetAttrNSEnable()
        return GfxValue(retStr)

    def refreshSpriteMainProperty(self):
        widget = self.getWidget()
        fightMC = widget.mineWarSpritePanel.attributeMc.fightMC
        widget.removeAllInst(fightMC)
        spriteInfo = self.parentProxy.getCurSelectSpriteProp()
        mainInfo = uiUtils.createSpriteArr(spriteInfo, self.mainPropInfo, False)
        for i, info in enumerate(mainInfo):
            itemMc = widget.getInstByClsName('SummonedWarSpriteMine_FightPlus')
            itemMc.x = 133 if i % 2 else 0
            itemMc.y = PROPERTY_HEIGHT * int(i / 2)
            itemMc.nameTF.text = info[0]
            itemMc.valueTF.text = info[1]
            fightMC.addChild(itemMc)
            tip = uiUtils.getSpritePropsTooltip(spriteInfo, int(info[2]), int(info[3]))
            TipManager.addTip(itemMc.nameTF, tip, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(itemMc.valueTF, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def refreshSpritePlusProperty(self):
        widget = self.getWidget()
        fightPlusViewMC = widget.mineWarSpritePanel.attributeMc.fightPlusViewMC
        widget.removeAllInst(fightPlusViewMC.canvas)
        spriteInfo = self.parentProxy.getCurSelectSpriteProp()
        plusInfo = uiUtils.createSpriteArr(spriteInfo, self.plusPropInfo, False)
        for i, info in enumerate(plusInfo):
            itemMc = widget.getInstByClsName('SummonedWarSpriteMine_FightPlus')
            itemMc.x = 133 if i % 2 else 0
            itemMc.y = PROPERTY_HEIGHT * int(i / 2) + 23
            itemMc.nameTF.text = info[0]
            itemMc.valueTF.text = info[1]
            fightPlusViewMC.canvas.addChild(itemMc)
            tip = uiUtils.getSpritePropsTooltip(spriteInfo, int(info[2]), int(info[3]))
            TipManager.addTip(itemMc.nameTF, tip, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(itemMc.valueTF, tip, tipUtils.TYPE_DEFAULT_BLACK)

        fightPlusViewMC.refreshHeight(fightPlusViewMC.canvas.height + 31)

    def refreshSpritePropInfo(self, index):
        gamelog.debug('m.l@SummonedWarSpriteMineProperty.refreshSpritePropInfo', index, self.parentProxy.currSelectItemSpriteIndex)
        if index == self.parentProxy.currSelectItemSpriteIndex:
            self.refreshSpriteMainProperty()
            self.refreshSpritePlusProperty()
