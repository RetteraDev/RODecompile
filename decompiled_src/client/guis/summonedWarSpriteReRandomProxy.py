#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteReRandomProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gamelog
import gameglobal
import utils
import events
import formula
import ui
from guis import tipUtils
from asObject import ASObject
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import uiConst
from guis.asObject import MenuManager
from guis.asObject import TipManager
from guis import uiUtils
from gameStrings import gameStrings
from data import consumable_item_data as CID
from data import sys_config_data as SYSCD
from data import summon_sprite_info_data as SSID
from cdata import game_msg_def_data as GMDD
from cdata import summon_sprite_rerandom_rule_data as SSRRD
SPRITE_MAX_LEVEL = 3

class SummonedWarSpriteReRandomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteReRandomProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RERANDOM, self.hide)
        self.widget = None
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_RERANDOM:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RERANDOM)
        self.reset()

    def show(self, spriteInfo):
        self.reset()
        self.spriteInfo = spriteInfo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RERANDOM)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        if not self.spriteInfo:
            return
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleCloseBtnClick, False, 1, True)
        self.widget.saveBtn.addEventListener(events.MOUSE_CLICK, self.handleSaveBtnClick, False, 1, True)
        self.widget.reRandomBtn.addEventListener(events.MOUSE_CLICK, self.handleReRandomBtnClick, False, 1, True)
        self.widget.consumesBtn.addEventListener(events.BUTTON_CLICK, self.handleConsumesBtnClick, False, 1, True)
        self.widget.spriteNameTF.text = self.spriteInfo.get('name', '')
        self.widget.cashCost.visible = False
        self.updateSpriteInfo(self.spriteInfo.get('index'))
        self.updateConsumeItemMC()

    def handleConsumesBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.addConsumesTip(e.target)

    def addConsumesTip(self, target):
        if not self.spriteInfo:
            return
        else:
            consumesTipPanel = self.widget.getInstByClsName('SummonedWarSpriteReRandom_consumesTip')
            spriteConsumesDict = SYSCD.data.get('spriteReRandomConsumes', {})
            logSrc = spriteConsumesDict.get('logSrc', 441)
            itemIds = spriteConsumesDict.get('itemId', [785009, 785010])
            _consumesDict = self.spriteInfo.get('_consumesDict', {})
            for i, itemId in enumerate(itemIds):
                itemMc = getattr(consumesTipPanel, 'itemNum%d' % i, None)
                if not itemMc:
                    continue
                consumeInfo = _consumesDict.get(logSrc, {})
                consumeNum = 0
                for consumeId in consumeInfo:
                    if itemId == uiUtils.getParentId(consumeId):
                        consumeNum += consumeInfo[consumeId]

                itemMc.text = consumeNum

            MenuManager.getInstance().showMenu(target, consumesTipPanel, None, False)
            return

    def updateSpriteInfo(self, index):
        if not self.widget:
            return
        if index != self.spriteInfo.get('index'):
            return
        propsReRand = self.spriteInfo.get('propsReRand', {})
        if not propsReRand:
            self.hideNewMC()
        else:
            self.updateNewSpriteInfo(propsReRand)
        self.updateNowSpriteInfo(self.spriteInfo.get('props', {}))
        self.updateConsumeItemMC()

    def updateConsumeItemMC(self):
        clever = self.isCurSpriteClever()
        spriteId = self.spriteInfo.get('spriteId', 0)
        itemMc = getattr(self.widget, 'reRandomItem0', None)
        rrd = SSRRD.data.get((spriteId, int(clever) + 1), {})
        itemId = rrd.get('reRandomItemId')
        itemNum = rrd.get('reRandomItemNumber')
        if itemMc:
            itemMc.dragable = False
            count = BigWorld.player().inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
            itemInfo = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(count, itemNum))
            itemMc.setItemSlotData(itemInfo)
            itemMc.count = count
            self.setConsumeItemSelected(itemMc)
        self.widget.selectDescTF.htmlText = SYSCD.data.get('spriteRerandomConsumeDescs', ('', ''))[int(clever)]

    def handleItemMcClick(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()

    def setConsumeItemSelected(self, itemMc):
        p = BigWorld.player()
        if self.selectedItemMC:
            self.selectedItemMC.setSlotState(uiConst.ITEM_NORMAL)
            self.selectedItemMC = None
        self.selectedItemMC = itemMc
        if self.selectedItemMC.count:
            self.selectedItemMC.setSlotState(uiConst.ITEM_SELECTED)
            self.selectedItemMC.removeEventListener(events.MOUSE_CLICK, self.handleItemMcClick)
        else:
            self.selectedItemMC.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            self.selectedItemMC.addEventListener(events.MOUSE_CLICK, self.handleItemMcClick, False, 0, True)
        self.widget.cashCost.visible = True
        _, cash = self.getConsumeInfo(self.selectedItemMC.data.itemId)
        self.widget.cashCost.costTxt.htmlText = uiUtils.convertNumStr(p.cash + p.bindCash, cash, False, enoughColor=None)

    def handleCloseBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.hide()

    def discardRadom(self):
        self.hide()
        gamelog.debug('m.l@SummonedWarSpriteReRandomProxy.discardRadom')

    def handleSaveBtnClick(self, *args):
        gamelog.debug('m.l@SummonedWarSpriteReRandomProxy.handleSaveBtnClick')
        propsReRand = self.spriteInfo.get('propsReRand', {})
        props = self.spriteInfo.get('props', {})
        msg = None
        if props['clever'] and not propsReRand['clever']:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RERANDOM_CLEVER_LOST_SAVE_MSG, 'SPRITE_RERANDOM_CLEVER_LOST_SAVE_MSG')
        elif self.getReRandSpriteLvResult() > 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RERANDOM_LV_DONW_SAVE_MSG, 'SPRITE_RERANDOM_LV_DONW_SAVE_MSG')
        if msg:
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.realSaveResult, gameStrings.SPRITE_RERANDOM_SAVE_CONFIRM, noBtnText=gameStrings.SPRITE_RERANDOM_SAVE_CANCEL)
        else:
            self.realSaveResult()

    @ui.checkInventoryLock()
    def realSaveResult(self):
        p = BigWorld.player()
        idx = self.spriteInfo.get('index', -99)
        BigWorld.player().base.submitSpriteReRandomResult(idx, p.cipherOfPerson)

    def handleReRandomBtnClick(self, *args):
        p = BigWorld.player()
        if not self.selectedItemMC:
            p.showGameMsg(GMDD.data.SPRITE_RERANDOM_NEED_SELECT_ITEM, ())
            return
        idx = self.spriteInfo.get('index', -99)
        itemId = self.selectedItemMC.data.itemId
        page, pos = p.inv.findItemInPages(itemId, enableParentCheck=True)
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            if self.isCurSpriteClever():
                p.showGameMsg(GMDD.data.SPRITE_RERANDOM_CLEVER_NO_ITEM, ())
            else:
                p.showGameMsg(GMDD.data.SPRITE_RERANDOM_NORMAL_NO_ITEM, ())
            return
        spriteReMode = CID.data.get(itemId, {}).get('spriteReMode', -1)
        gamelog.debug('m.l@SummonedWarSpriteReRandomProxy.handleReRandomBtnClick', idx, spriteReMode, itemId, page, pos)
        spriteId = self.spriteInfo.get('spriteId', 0)
        propsReRand = self.spriteInfo.get('propsReRand', {})
        _, scoreLv, title, _ = utils.getSpriteScoreInfo(spriteId, propsReRand)
        msg = ''
        if propsReRand.get('clever') and not self.isCurSpriteClever():
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RERANDOM_CLEVER_LOST_MSG, 'SPRITE_RERANDOM_CLEVER_LOST_MSG')
        elif scoreLv in SYSCD.data.get('spriteReRandomNeedAlertLvs', (2, 3)):
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RERANDOM_GET_RARE_LV, '%s') % title
        elif self.getReRandSpriteLvResult() < 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RERANDOM_LV_DONW_RERANDON_MSG, 'SPRITE_RERANDOM_LV_DONW_RERANDON_MSG')
        if msg:
            if self.reRandomMsgId:
                self.uiAdapter.messageBox.dismiss(self.reRandomMsgId)
            self.reRandomMsgId = self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.applyReRandom, idx, spriteReMode), gameStrings.SPRITE_RERANDOM_CONFIRM, noBtnText=gameStrings.SPRITE_RERANDOM_CANCEL)
        else:
            self.applyReRandom(idx, spriteReMode)

    @ui.checkInventoryLock()
    def applyReRandom(self, idx, spriteReMode):
        p = BigWorld.player()
        p.base.applyReRandomSummonSpriteProp(idx, spriteReMode, p.cipherOfPerson)

    def hideNewMC(self):
        if not self.widget:
            return
        self.widget.newAptitudeMC.visible = False
        self.widget.saveBtn.enabled = False
        clever = self.isCurSpriteClever()
        desc = SYSCD.data.get('spriteReRandomAptitudeDescs', ('', ''))[clever]
        self.widget.descTF.visible = True
        self.widget.descTF.htmlText = desc
        self.widget.reRandomBtn.label = gameStrings.TEXT_SUMMONEDWARSPRITERERANDOMPROXY_230

    def updateNewSpriteInfo(self, props):
        if not self.widget:
            return
        spriteId = self.spriteInfo.get('spriteId', 0)
        self.calcSpriteAttitude(spriteId, props)
        self.widget.newAptitudeMC.visible = True
        self.widget.saveBtn.enabled = True
        self.widget.descTF.visible = False
        self.widget.reRandomBtn.label = gameStrings.TEXT_SUMMONEDWARSPRITERERANDOMPROXY_240
        score, lv, title, _ = utils.getSpriteScoreInfo(spriteId, props)
        self.widget.newAptitudeMC.attributeGradeTF.htmlText = title
        TipManager.addTip(self.widget.newAptitudeMC.attributeGradeTxt, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(self.widget.newAptitudeMC.attributeGradeTF, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
        self.setGrowthStarInfo(self.widget.newAptitudeMC, props)
        self.setAptitudeInfo(self.widget.newAptitudeMC, props, True)
        self.updateConsumeItemMC()
        effect = self.widget.newAptitudeMC.cleverEffect
        effectVisible = lv == SPRITE_MAX_LEVEL
        self.widget.newAptitudeMC.attributeGradeTF.visible = not effectVisible
        effect.visible = effectVisible
        if effectVisible:
            effect.gotoAndPlay(0)
        star = utils.getSpriteGrowthRatioStar(spriteId, props.get('growthRatio', 0))
        self.refreshStar(star, self.widget.newAptitudeMC)

    def refreshStar(self, star, startContainer):
        for i in xrange(const.SUMMON_SPRITE_MAX_STAR):
            starMc = getattr(startContainer, 'star%s' % i)
            if starMc:
                starMc.visible = star >= i

    def updateNowSpriteInfo(self, props):
        if not self.widget:
            return
        spriteId = self.spriteInfo.get('spriteId', 0)
        score, _, title, _ = utils.getSpriteScoreInfo(spriteId, props)
        self.widget.nowAptitudeMC.attributeGradeTF.htmlText = title
        TipManager.addTip(self.widget.nowAptitudeMC.attributeGradeTxt, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(self.widget.nowAptitudeMC.attributeGradeTF, SYSCD.data.get('spriteGradeTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
        self.setGrowthStarInfo(self.widget.nowAptitudeMC, props)
        self.setAptitudeInfo(self.widget.nowAptitudeMC, props)
        star = utils.getSpriteGrowthRatioStar(spriteId, props.get('growthRatio', 0))
        self.refreshStar(star, self.widget.nowAptitudeMC)

    def setGrowthStarInfo(self, containMC, props):
        containMC.growthRatioTF.text = str('%.3f' % props.get('growthRatio', 0))
        TipManager.addTip(containMC.growthRatioTxt, SYSCD.data.get('spriteGrowthRatioTip', ''), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(containMC.growthRatioTF, SYSCD.data.get('spriteGrowthRatioTip', ''), tipUtils.TYPE_DEFAULT_BLACK)

    def setAptitudeInfo(self, containMC, props, withDiff = False):
        spriteId = self.spriteInfo.get('spriteId', 0)
        upgradeStage = self.spriteInfo.get('upgradeStage', 0)
        nowProps = self.spriteInfo.get('props', {})
        clever = props.get('clever', 0)
        juexing = props.get('juexing', 0)
        for idx in xrange(len(utils.APTITUDE_NAME_LIST)):
            aptitudeName = utils.APTITUDE_NAME_LIST[idx]
            attrNSMC = getattr(containMC, aptitudeName, None)
            aptitude = props.get(aptitudeName, 0)
            aptitudeOriginMax = utils.getAptitudeMax(spriteId, aptitudeName)
            aptitudeMax = formula.getSpriteAptitudeVal(aptitudeOriginMax, clever, juexing, spriteId, upgradeStage)
            nowAptitude = nowProps.get(aptitudeName)
            diffValue = aptitude - nowAptitude
            if attrNSMC:
                attrNSMC.maxValue = aptitudeMax
                if withDiff:
                    if diffValue > 0:
                        attrNSMC.currentValues = [nowAptitude, 0, aptitude]
                    else:
                        attrNSMC.currentValues = [aptitude, nowAptitude, 0]
                else:
                    attrNSMC.currentValues = [aptitude, 0, 0]
            aptitudeTF = getattr(containMC, aptitudeName + 'TF', None)
            tip = SYSCD.data.get('spriteAptitudeTips', {}).get(aptitudeName, aptitudeName)
            if aptitudeTF:
                if withDiff:
                    if diffValue >= 0:
                        aptitudeTF.htmlText = '<font color=\"#40C133\">+%d</font>' % diffValue
                    else:
                        aptitudeTF.htmlText = '<font color=\"#CD4032\">%d</font>' % diffValue
                else:
                    aptitudeTF.text = str(aptitude)
                TipManager.addTip(aptitudeTF, tip, tipUtils.TYPE_DEFAULT_BLACK)
            containMC.cleverIcon.visible = props.get('clever', 0)
            cleverTip = SYSCD.data.get('spriteCleverTips', '')
            TipManager.addTip(containMC.cleverIcon, cleverTip, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(getattr(containMC, aptitudeName + 'Txt', None), tip, tipUtils.TYPE_DEFAULT_BLACK)

    def setAptitudeDiff(self, containMC):
        pass

    def reset(self):
        self.spriteInfo = None
        self.closeHandle = None
        self.selectedItemMC = None
        self.reRandomMsgId = None

    def getConsumeInfo(self, itemId):
        spriteId = self.spriteInfo.get('spriteId', 0)
        reRandomMode = CID.data.get(itemId, {}).get('spriteReMode', -1)
        rrd = SSRRD.data.get((spriteId, reRandomMode), {})
        itemNum = rrd.get('reRandomItemNumber', 0)
        cashCost = rrd.get('reRandomCashCost', 0)
        return (itemNum, cashCost)

    def getReRandSpriteLvResult(self):
        spriteId = self.spriteInfo.get('spriteId', 0)
        curLv = utils.getSpriteScoreInfo(spriteId, self.spriteInfo.get('props', {}))[1]
        propsReRand = self.spriteInfo.get('propsReRand', {})
        self.calcSpriteAttitude(spriteId, propsReRand)
        newLv = utils.getSpriteScoreInfo(spriteId, propsReRand)[1] if propsReRand else 0
        return cmp(curLv, newLv)

    def calcSpriteAttitude(self, spriteId, props):
        clever = props.get('clever', 0)
        upgradeStage = self.spriteInfo.get('upgradeStage', 0)
        nowProps = self.spriteInfo.get('props', {})
        juexing = nowProps.get('juexing', 0)
        if props:
            for aptName in utils.APTITUDE_NAME_LIST:
                oriValue = props.get(utils.APTITUDE_NAME_MAP.get(aptName), 0)
                props[aptName] = formula.getSpriteAptitudeVal(oriValue, clever, juexing, spriteId, upgradeStage)

            props['growthRatio'] = utils.calcSpriteGrowthRatio(props.get('baseGrowthRatio', 0), juexing, nowProps.get('boneLv', 0), SSID.data.get(spriteId, {}).get('spriteBoneGrowth', 0))

    def isCurSpriteClever(self):
        return self.spriteInfo.get('props', {}).get('clever', 0)

    @ui.checkInventoryLock()
    def abandonSpriteClever(self):
        p = BigWorld.player()
        msg = uiUtils.getTextFromGMD(GMDD.data.ABANDON_SPRITE_CLEVER_MSG, 'ABANDON_SPRITE_CLEVER_MSG')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.base.abandonSpriteCleverForItem, self.spriteInfo.get('index', 0), p.cipherOfPerson))
