#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteRareTransferProxy.o
import BigWorld
import uiConst
import tipUtils
import gametypes
import math
import utils
import gameglobal
import ui
import const
import formula
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import summon_sprite_info_data as SSID
from data import sys_config_data as SCD
from data import formula_client_data as FCD
from data import summon_sprite_familiar_data as SSFD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SPRITE_RERANDOM_ITEMID_LOW = 785009
SPRITE_RERANDOM_ITEMID_HIGH = 785010

class SummonedWarSpriteRareTransferProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteRareTransferProxy, self).__init__(uiAdapter)
        self.widget = None
        self.originalIndex = 0
        self.targetSpriteId = 0
        self.selectSpriteMc = None
        self.canTransfer = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RARE_TRANSFER, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_RARE_TRANSFER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RARE_TRANSFER)

    def reset(self):
        self.originalIndex = 0
        self.targetSpriteId = 0
        self.selectSpriteMc = None
        self.canTransfer = False

    def show(self, spriteIndex):
        self.originalIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_RARE_TRANSFER)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.consumeIcon.bonusType = 'yunChui'
        self.widget.checkBox0.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox0, False, 0, True)
        self.widget.checkBox1.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox1, False, 0, True)
        self.widget.checkBox2.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox2, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateOriginalSprite()
        self.updateTargetSprite()
        self.updateTransferSprite()

    def _onRuleBtnClick(self, e):
        target = e.target
        descTipList = SCD.data.get('rareSpriteTransferRuleList', [])
        if not descTipList:
            return
        ruleTipPanel = self.widget.getInstByClsName('SummonedWarSpriteRareTransfer_ruleTip')
        for i, desc in enumerate(descTipList):
            ruleItem = ruleTipPanel.ruleListMc.getChildByName('rule%d' % i)
            ruleItem.ruleDesc.text = desc

        MenuManager.getInstance().showMenu(target, ruleTipPanel, {'x': target.x + target.width,
         'y': target.y - ruleTipPanel.height}, True, self.widget)

    @ui.checkInventoryLock()
    def realTransfer(self):
        p = BigWorld.player()
        skillTransferFlag = self.widget.checkBox0.selected
        familiarTransferFlag = self.widget.checkBox1.selected
        rerandTranserFlag = self.widget.checkBox2.selected
        p.base.spriteRareTransfer(self.originalIndex, self.targetSpriteId, skillTransferFlag, familiarTransferFlag, rerandTranserFlag, p.cipherOfPerson)

    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        originalName = spriteInfo.get('name', 0)
        targetName = SSID.data.get(self.targetSpriteId, {}).get('name', '')
        transferDesc0 = gameStrings.SPRITE_RARE_TRANSFER_SURE_DESC if self.widget.checkBox0.selected else gameStrings.SPRITE_RARE_TRANSFER_NO_DESC
        transferDesc1 = gameStrings.SPRITE_RARE_TRANSFER_SURE_DESC if self.widget.checkBox1.selected else gameStrings.SPRITE_RARE_TRANSFER_NO_DESC
        transferDesc2 = gameStrings.SPRITE_RARE_TRANSFER_SURE_DESC if self.widget.checkBox2.selected else gameStrings.SPRITE_RARE_TRANSFER_NO_DESC
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_SURE, '%s-%s-%s-%s-%s') % (originalName,
         targetName,
         transferDesc0,
         transferDesc1,
         transferDesc2)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.realTransfer)

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleSelectCheckBox0(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.updateTargetSprite()

    def handleSelectCheckBox1(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.updateTargetSprite()

    def handleSelectCheckBox2(self, *args):
        e = ASObject(args[3][0])
        self.updateTargetSprite()

    def handleSelSpriteClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.selectIcon.visible:
            return
        if self.selectSpriteMc and self.selectSpriteMc.selectIcon.visible:
            self.selectSpriteMc.selectIcon.visible = False
        target.selectIcon.visible = True
        self.targetSpriteId = target.targetSpriteId
        self.selectSpriteMc = target
        self.canTransfer = self.canTransfer and self.targetSpriteId
        self.updateTargetSprite()

    def getRareSprite(self):
        p = BigWorld.player()
        originalSpriteId = p.summonSpriteList.get(self.originalIndex, {}).get('spriteId', 0)
        blackList = SCD.data.get('spriteRareTransferBlackList', ())
        spriteIdList = []
        for i, spriteId in enumerate(SSID.data):
            spriteData = SSID.data.get(spriteId, {})
            spriteManual = spriteData.get('spriteManual', 0)
            if not spriteManual:
                continue
            isRare = spriteData.get('isRare', 0)
            if isRare != gametypes.SPRITE_RARE_TYPE_SPECIAL:
                continue
            if originalSpriteId == spriteId:
                continue
            if spriteId in blackList:
                continue
            spriteIdList.append(spriteId)

        return spriteIdList

    def updateOriginalSprite(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        self.widget.originalSlot.slot.setItemSlotData({'iconPath': uiUtils.getSummonSpriteIconPath(spriteId)})
        self.widget.originalSlot.slot.dragable = False
        self.widget.originalSlot.selectIcon.visible = False
        self.widget.originalSlot.slot.validateNow()
        TipManager.addTipByType(self.widget.originalSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (self.originalIndex,), False, 'upLeft')

    def updateTargetSprite(self):
        turnFamiOutStr, _ = utils.getSpriteFamiTransferPercentStr(self.originalIndex)
        self.widget.checkBox1.label = gameStrings.SUMMONED_WAR_SPRITE_RARE_TRANSFER_FAMI_HINT % turnFamiOutStr
        if not self.targetSpriteId:
            self.widget.noSelectDesc.visible = True
            self.widget.targetSlot.visible = False
            self.widget.checkBox0.selected = True
            self.widget.checkBox0.enabled = False
            self.widget.checkBox1.selected = True
            self.widget.checkBox1.enabled = False
            self.widget.checkBox2.selected = True
            self.widget.checkBox2.enabled = False
        else:
            self.widget.noSelectDesc.visible = False
            self.widget.targetSlot.visible = True
            self.widget.checkBox0.enabled = True
            self.widget.checkBox1.enabled = True
            self.widget.checkBox2.enabled = True
            self.widget.targetSlot.slot.setItemSlotData({'iconPath': uiUtils.getSummonSpriteIconPath(self.targetSpriteId)})
            self.widget.targetSlot.slot.dragable = False
            self.widget.targetSlot.selectIcon.visible = False
        self.updateOption()
        self.updateConsumeResource()
        self.updateSureBtnState()

    def updateSureBtnState(self):
        if self.canTransfer:
            self.widget.sureBtn.disabled = False
            TipManager.removeTip(self.widget.sureBtn)
        else:
            self.widget.sureBtn.disabled = True
            TipManager.addTip(self.widget.sureBtn, gameStrings.SPRITE_RARE_TRANSFER_CONDITION_LESS)

    def updateTransferSprite(self):
        rareSpritesIdList = self.getRareSprite()
        numChildren = self.widget.afterTransferMc.numChildren
        for i in xrange(0, numChildren):
            itemSlot = self.widget.afterTransferMc.getChildByName('itemSlot%d' % i)
            if i < len(rareSpritesIdList):
                itemSlot.visible = True
                spriteId = rareSpritesIdList[i]
                itemSlot.slot.setItemSlotData({'iconPath': uiUtils.getSummonSpriteIconPath(spriteId)})
                itemSlot.slot.dragable = False
                itemSlot.selectIcon.visible = False
                itemSlot.targetSpriteId = spriteId
                itemSlot.addEventListener(events.MOUSE_CLICK, self.handleSelSpriteClick, False, 0, True)
            else:
                itemSlot.visible = False

    def updateOption(self):
        if not self.widget.checkBox0.enabled:
            self.widget.desc0.visible = False
        else:
            self.widget.desc0.visible = True
            if not self.widget.checkBox0.selected:
                desc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_NO_SELECT_SKILL_DESC, '')
                self.widget.desc0.text = desc
            else:
                desc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_SELECT_SKILL_DESC, '')
                self.widget.desc0.text = desc
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        props = spriteInfo.get('props', {})
        famiEffLv = props.get('famiEffLv', 1)
        familiar = props.get('familiar', 1)
        famiEffAdd = props.get('famiEffAdd', 0)
        famiExp = props.get('famiExp', 0)
        totalFamiExp = utils.getSpriteAllFamiExp(familiar, famiExp)
        yunchuiCost = utils.getSpriteCoverCost(totalFamiExp)
        yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
        if not self.widget.checkBox1.enabled:
            self.widget.desc1.visible = False
            self.widget.famiMc.visible = False
            self.widget.consumeValT.htmlText = uiUtils.convertNumStr(yunchuiOwn, yunchuiCost, False, enoughColor=None)
            self.canTransfer = yunchuiOwn >= yunchuiCost and self.canTransfer
        elif not self.widget.checkBox1.selected:
            self.widget.famiMc.visible = False
            self.widget.desc1.visible = True
            self.widget.consumeIcon.visible = False
            self.widget.consumeValT.visible = False
            noSelFamiDesc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_NO_SELECT_FAMILIAR_DESC, '')
            self.widget.desc1.text = noSelFamiDesc
            self.canTransfer = True
        else:
            self.widget.famiMc.visible = True
            self.widget.desc1.visible = False
            self.widget.consumeIcon.visible = True
            self.widget.consumeValT.visible = True
            getTurnFami = utils.getSpriteFamiTransferV2(totalFamiExp) if gameglobal.rds.configData.get('enableSpriteFamiV2', False) else utils.getSpriteFamiTransfer(totalFamiExp)
            familiarLv = utils.getSpriteTotalFamiExpToLv(getTurnFami)
            self.widget.famiMc.valT0.text = '%d+%d' % (familiar, famiEffAdd)
            self.widget.famiMc.valT1.text = '%d+%d' % (familiarLv, 0)
            self.widget.famiMc.valT0.x = self.widget.famiMc.famiIcon0.x + self.widget.famiMc.famiIcon0.width
            self.widget.famiMc.toPic.x = self.widget.famiMc.valT0.x + self.widget.famiMc.valT0.textWidth
            self.widget.famiMc.famiIcon1.x = self.widget.famiMc.toPic.x + self.widget.famiMc.toPic.width
            self.widget.famiMc.valT1.x = self.widget.famiMc.famiIcon1.x + self.widget.famiMc.famiIcon0.width
            gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(self.widget.famiMc.famiIcon0, familiar, famiEffAdd, famiEffLv)
            gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(self.widget.famiMc.famiIcon1, familiarLv, 0, familiarLv + 0)
            self.widget.consumeValT.htmlText = uiUtils.convertNumStr(yunchuiOwn, yunchuiCost, False, enoughColor=None)
            self.canTransfer = yunchuiOwn >= yunchuiCost
        if not self.widget.checkBox2.enabled:
            self.widget.desc2.visible = False
        else:
            self.widget.desc2.visible = True
            if not self.widget.checkBox2.selected:
                desc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_NO_RERANDOM_DESC, '')
                self.widget.desc2.text = desc
            else:
                desc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_RARE_TRANSFER_RERANDOM_DESC, '%s') % self.getPropertyRate()
                self.widget.desc2.text = desc

    def getPropertyRate(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        upgradeStage = spriteInfo.get('upgradeStage', 0)
        props = spriteInfo.get('props')
        clever = props.get('clever', 0)
        juexing = props.get('juexing', 0)
        aptitudeSum = 0
        aptitudeMaxSum = 0
        for idx in xrange(len(utils.APTITUDE_NAME_LIST)):
            aptitudeName = utils.APTITUDE_NAME_LIST[idx]
            aptitude = int(props.get(aptitudeName, 0))
            aptitudeOriginMax = utils.getAptitudeMax(spriteId, aptitudeName)
            aptitudeMax = formula.getSpriteAptitudeVal(aptitudeOriginMax, clever, juexing, spriteId, upgradeStage)
            aptitudeSum += aptitude
            aptitudeMaxSum += aptitudeMax

        rateStr = '%.1f%%' % (aptitudeSum * 100.0 / aptitudeMaxSum)
        return rateStr

    def updateConsumeResource(self):
        p = BigWorld.player()
        transferNeedShenPoItem = SCD.data.get('spriteRareTransferConsumeItem')
        shenPoItemId = transferNeedShenPoItem[0]
        shenPoNeedNum = transferNeedShenPoItem[1]
        shenPoOwnNum = p.inv.countItemInPages(uiUtils.getParentId(shenPoItemId), enableParentCheck=True)
        if not self.targetSpriteId or not self.widget.checkBox0.selected and not self.widget.checkBox2.selected:
            self.widget.consumeMc.gotoAndStop('type0')
            self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
            self.canTransfer = shenPoOwnNum >= shenPoNeedNum and self.targetSpriteId and self.canTransfer
        elif self.widget.checkBox0.selected and not self.widget.checkBox2.selected:
            self.widget.consumeMc.gotoAndStop('type2')
            self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
            mallItemId, mallOwnNum, mallNeedNum = self.getSkillTransferItem()
            self.updateItemSlot(self.widget.consumeMc.consumeSlot1, mallItemId, mallOwnNum, mallNeedNum)
            qizhiItemId, qizhiOwnNum, qizhiNeedNum = self.getQiZhiFuItem()
            self.updateItemSlot(self.widget.consumeMc.consumeSlot2, qizhiItemId, qizhiOwnNum, qizhiNeedNum)
            self.canTransfer = mallOwnNum >= mallNeedNum and qizhiOwnNum >= qizhiNeedNum and self.targetSpriteId and self.canTransfer
        elif not self.widget.checkBox0.selected and self.widget.checkBox2.selected:
            lowItemId, lowOwnNum, lowItemCnt, highItemId, hightOwnNum, highItemCnt = self.getBiAnHuaItem()
            if not highItemCnt:
                self.widget.consumeMc.gotoAndStop('type1')
                self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot1, lowItemId, lowOwnNum, lowItemCnt)
            else:
                self.widget.consumeMc.gotoAndStop('type2')
                self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot1, lowItemId, lowOwnNum, lowItemCnt)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot2, highItemId, hightOwnNum, highItemCnt)
            self.canTransfer = lowOwnNum >= lowItemCnt and highItemId >= hightOwnNum and self.targetSpriteId and self.canTransfer
        elif self.widget.checkBox0.selected and self.widget.checkBox2.selected:
            lowItemId, lowOwnNum, lowItemCnt, highItemId, hightOwnNum, highItemCnt = self.getBiAnHuaItem()
            if not highItemCnt:
                self.widget.consumeMc.gotoAndStop('type3')
                self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
                mallItemId, mallOwnNum, mallNeedNum = self.getSkillTransferItem()
                self.updateItemSlot(self.widget.consumeMc.consumeSlot1, mallItemId, mallOwnNum, mallNeedNum)
                qizhiItemId, qizhiOwnNum, qizhiNeedNum = self.getQiZhiFuItem()
                self.updateItemSlot(self.widget.consumeMc.consumeSlot2, qizhiItemId, qizhiOwnNum, qizhiNeedNum)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot3, lowItemId, lowOwnNum, lowItemCnt)
            else:
                self.widget.consumeMc.gotoAndStop('type4')
                self.updateItemSlot(self.widget.consumeMc.consumeSlot0, shenPoItemId, shenPoOwnNum, shenPoNeedNum)
                mallItemId, mallOwnNum, mallNeedNum = self.getSkillTransferItem()
                self.updateItemSlot(self.widget.consumeMc.consumeSlot1, mallItemId, mallOwnNum, mallNeedNum)
                qizhiItemId, qizhiOwnNum, qizhiNeedNum = self.getQiZhiFuItem()
                self.updateItemSlot(self.widget.consumeMc.consumeSlot2, qizhiItemId, qizhiOwnNum, qizhiNeedNum)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot3, lowItemId, lowOwnNum, lowItemCnt)
                self.updateItemSlot(self.widget.consumeMc.consumeSlot4, highItemId, hightOwnNum, highItemCnt)
            self.canTransfer = mallOwnNum >= mallNeedNum and qizhiOwnNum >= qizhiNeedNum and lowOwnNum >= lowItemCnt and highItemId >= hightOwnNum and self.targetSpriteId and self.canTransfer

    def getSkillTransferItem(self):
        p = BigWorld.player()
        skillTransferNeedMallItem = (SCD.data.get('CommonTransferSpriteSkillItem'), 1)
        mallItemId = skillTransferNeedMallItem[0]
        mallNeedNum = skillTransferNeedMallItem[1]
        mallOwnNum = p.inv.countItemInPages(uiUtils.getParentId(mallItemId), enableParentCheck=True)
        return (mallItemId, mallOwnNum, mallNeedNum)

    def getQiZhiFuItem(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        spriteConsumesDict = SCD.data.get('spriteSkillConsumes', {})
        logSrc = spriteConsumesDict.get('logSrc', 505)
        qizhiItemId = spriteConsumesDict.get('itemId', 785012)
        _consumesDict = spriteInfo.get('_consumesDict', {})
        formulaId = SCD.data.get('qizhiNumNeedFormulaId', 90178)
        func = FCD.data.get(formulaId, {}).get('formula')
        if func:
            srcNum = _consumesDict.get(logSrc, {}).get(qizhiItemId, 0)
            dstNum = 0
            srcRare = spriteInfo.get('rareLv', 0)
            dstRare = srcRare
            qizhiNeedNum = func({'srcScore': srcNum,
             'dstScore': dstNum,
             'srcRare': srcRare,
             'dstRare': dstRare})
            qizhiNeedNum = max(1, int(math.ceil(qizhiNeedNum)))
        qizhiOwnNum = p.inv.countItemInPages(uiUtils.getParentId(qizhiItemId), enableParentCheck=True)
        return (qizhiItemId, qizhiOwnNum, qizhiNeedNum)

    def getBiAnHuaItem(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.originalIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        props = spriteInfo.get('props', {})
        isClever = props.get('clever', 0)
        scoreLv = utils.getSpriteScoreInfo(spriteId, props)[1]
        rerandomCost = SCD.data.get('spriteRareTransferReRandomItemCost', {})
        lowItemCnt, highItemCnt = rerandomCost.get((isClever, scoreLv), (0, 0))
        lowOwnNum = p.inv.countItemInPages(uiUtils.getParentId(SPRITE_RERANDOM_ITEMID_LOW), enableParentCheck=True)
        hightOwnNum = p.inv.countItemInPages(uiUtils.getParentId(SPRITE_RERANDOM_ITEMID_HIGH), enableParentCheck=True)
        return (SPRITE_RERANDOM_ITEMID_LOW,
         lowOwnNum,
         lowItemCnt,
         SPRITE_RERANDOM_ITEMID_HIGH,
         hightOwnNum,
         highItemCnt)

    def updateItemSlot(self, itemSlot, itemId, ownNum, needNum):
        if ownNum < needNum:
            strNum = uiUtils.toHtml(ownNum, '#FF0000')
            itemSlot.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        else:
            strNum = uiUtils.toHtml(ownNum, '#FFFFE6')
            itemSlot.slot.setSlotState(uiConst.ITEM_NORMAL)
        count = str('%s/%d' % (strNum, needNum))
        itemSlot.slot.dragable = False
        itemSlot.slot.fitSize = True
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemSlot.slot.setItemSlotData(itemInfo)
        itemSlot.slot.validateNow()
        ASUtils.setHitTestDisable(itemSlot.valueAmount, True)
        itemSlot.valueAmount.htmlText = count

    def transferSuccess(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_RARE_TRANSFER_SUCCESS, ())
        self.canTransfer = False
        self.hide()
