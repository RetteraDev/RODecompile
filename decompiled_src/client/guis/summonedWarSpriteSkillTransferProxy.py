#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSkillTransferProxy.o
import BigWorld
import const
import uiConst
import events
import skillDataInfo
import tipUtils
import ui
import uiUtils
import gameglobal
import utils
import formula
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from data import formula_client_data as FCD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SKILL_SLOT_NUM = 8
SPRITE_SKILL_LEVEL = 1
SPRITE_INIT_SLOT_NUM = 2

class SummonedWarSpriteSkillTransferProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteSkillTransferProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = 0
        self.turnInSpriteIdx = 0
        self.canTransfer = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_SKILL_TRANSFER, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_SKILL_TRANSFER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_SKILL_TRANSFER)

    def reset(self):
        self.spriteIndex = 0
        self.turnInSpriteIdx = 0
        self.canTransfer = False

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_SKILL_TRANSFER)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteSkillTransfer_LeftItem'
        self.widget.spriteList.barAlwaysVisible = True
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.lableFunction = self.itemFunction
        self.widget.frontBtn.selected = True
        self.widget.afterBtn.selected = False

    def refreshInfo(self):
        if not self.widget:
            return
        dataList = self.filterSprite()
        self.widget.noSpriteDesc.visible = not dataList
        self.widget.spriteList.dataArray = dataList
        self.updateTurnOutSprite()
        self.updateTurnInSprite()
        self.updateTransferBtnState()

    @ui.checkInventoryLock()
    def realCover(self):
        p = BigWorld.player()
        p.base.transferSpriteLearnSkills(self.spriteIndex, self.turnInSpriteIdx, p.cipherOfPerson)

    def _onTransferBtnClick(self, e):
        if not self.spriteIndex or not self.turnInSpriteIdx:
            return
        trunOutInfo = self.getSpriteInformation(self.spriteIndex)
        trunInInfo = self.getSpriteInformation(self.turnInSpriteIdx)
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_SKILL_TRANSFER_SURE, '%s(%s,%d)-%s(%s,%d)') % (trunOutInfo[0],
         trunOutInfo[1],
         trunOutInfo[2],
         trunInInfo[0],
         trunInInfo[1],
         trunInInfo[2])
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.realCover)

    def getSpriteInformation(self, spriteIndex):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        name = spriteInfo.get('name', 0)
        lv = spriteInfo.get('props', {}).get('lv', 0)
        nameOriginal = SSID.data.get(spriteId, {}).get('name', '')
        return [name, nameOriginal, lv]

    def _onCancelBtnClick(self, e):
        self.hide()

    def _onFrontBtnClick(self, e):
        self.widget.frontBtn.selected = True
        self.widget.afterBtn.selected = False
        self.updateSkill()

    def _onAfterBtnClick(self, e):
        if not self.turnInSpriteIdx:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SPRITE_SKILL_TRANSFER_NONE_SELECTED, ())
            return
        self.widget.frontBtn.selected = False
        self.widget.afterBtn.selected = True
        self.updateSkill()

    def handleSelSpriteDown(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected:
            return
        target.selected = True
        self.turnInSpriteIdx = target.spriteIndex
        self.updateTurnInSprite()
        self.updateTransferBtnState()

    def updateTransferBtnState(self):
        skillTransferDisabledTips = SCD.data.get('skillTransferDisabledTips', ['noselect', 'itemsless'])
        if not self.turnInSpriteIdx:
            self.widget.transferBtn.disabled = True
            TipManager.addTip(self.widget.transferBtn, skillTransferDisabledTips[0])
        elif not self.canTransfer:
            self.widget.transferBtn.disabled = True
            TipManager.addTip(self.widget.transferBtn, skillTransferDisabledTips[1])
        else:
            self.widget.transferBtn.disabled = False
            TipManager.removeTip(self.widget.transferBtn)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.spriteIndex
        itemMc.spriteId = itemData.spriteId
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteSkillTransfer%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown, False, 0, True)
        spriteName = itemData.name
        szLv = 'lv %d' % itemData.lv
        itemMc.labels = [spriteName, szLv]
        if utils.getSpriteBattleState(itemMc.spriteIndex) and utils.getSpriteAccessoryState(itemMc.spriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhanAndfu')
        elif utils.getSpriteBattleState(itemMc.spriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhan')
        elif utils.getSpriteAccessoryState(itemMc.spriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('fu')
        else:
            itemMc.spriteState.visible = False
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.itemSlot.slot.dragable = False
        itemMc.selected = self.turnInSpriteIdx == itemData.spriteIndex
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')

    def filterSprite(self):
        p = BigWorld.player()
        spriteOutInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteOutLockedNum = self.getSkillLockedSlotNum(spriteOutInfo)
        spriteList = []
        for spriteInfo in p.summonSpriteList.values():
            if spriteInfo['index'] == self.spriteIndex:
                continue
            lockedNum = self.getSkillLockedSlotNum(spriteInfo)
            if lockedNum > spriteOutLockedNum:
                continue
            props = spriteInfo.get('props', {})
            itemInfo = {}
            itemInfo['spriteIndex'] = spriteInfo.get('index', -1)
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['lv'] = props.get('lv', 0)
            spriteList.append(itemInfo)

        return sorted(spriteList, key=lambda d: d['lv'], reverse=True)

    def getSkillLockedSlotNum(self, spriteInfo):
        learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
        lockedNum = 0
        for i in xrange(SKILL_SLOT_NUM):
            info = learnedSkillInfos.get(i, None)
            if info:
                slotState = info.get('slot', 0)
                if slotState != const.SSPRITE_SKILL_SLOT_FORBIDDEN:
                    lockedNum += 1

        return lockedNum

    def updateTurnOutSprite(self):
        self.updateSpriteItem(self.widget.turnOutSpriteItem, self.spriteIndex)
        self.updateSkill()

    def updateTurnInSprite(self):
        if not self.turnInSpriteIdx:
            self.widget.desc0.visible = True
            self.widget.trunInSpriteItem.visible = False
        else:
            self.widget.desc0.visible = False
            self.widget.trunInSpriteItem.visible = True
            self.updateSpriteItem(self.widget.trunInSpriteItem, self.turnInSpriteIdx)
            self.updateSkill()
        self.updateConsumeItem()

    def updateSpriteItem(self, itemMc, index):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList[index]
        spriteId = spriteInfo.get('spriteId', 0)
        ssidData = SSID.data.get(spriteId, {})
        iconId = ssidData.get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.itemSlot.slot.dragable = False
        spriteName = spriteInfo.get('name', '')
        lv = spriteInfo.get('props', {}).get('lv', 1)
        szLv = 'lv %d' % lv
        itemMc.labels = [spriteName, szLv]
        if utils.getSpriteBattleState(index) and utils.getSpriteAccessoryState(index):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhanAndfu')
        elif utils.getSpriteBattleState(index):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhan')
        elif utils.getSpriteAccessoryState(index):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('fu')
        else:
            itemMc.spriteState.visible = False
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (index,), False, 'upLeft')

    def updateSkill(self):
        if self.widget.frontBtn.selected:
            self.updateTurnForntSkill(self.spriteIndex, 'Out')
            self.updateTurnForntSkill(self.turnInSpriteIdx, 'In')
        else:
            self.updateTurnOutAfterSkill()
            self.updateTurnInAfterSkill()

    def updateTurnForntSkill(self, spriteIndex, typeStr):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
        for i in xrange(SKILL_SLOT_NUM):
            itemSlot = self.widget.transferMc.getChildByName('turn%sSlot%d' % (typeStr, i))
            info = learnedSkillInfos.get(i, None)
            if info:
                slotState = info.get('slot', 0)
                spriteSkillId = info.get('id', 0)
                stateLocked = slotState == const.SSPRITE_SKILL_SLOT_FORBIDDEN
                itemSlot.lock.visible = stateLocked
                ASUtils.setHitTestDisable(itemSlot.lock, stateLocked)
                skillId = SSSD.data.get(spriteSkillId, {}).get('virtualSkill', 0)
                if skillId:
                    skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
                    iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                    itemSlot.slot.fitSize = True
                    itemSlot.slot.dragable = False
                    itemSlot.slot.setItemSlotData({'iconPath': iconPath})
                    itemSlot.slot.validateNow()
                    TipManager.addTipByType(itemSlot.slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                     'lv': SPRITE_SKILL_LEVEL}, False, 'upLeft')
                else:
                    itemSlot.slot.setItemSlotData(None)
            else:
                itemSlot.slot.setItemSlotData(None)
                itemSlot.lock.visible = True

        desc = self.widget.transferMc.getChildByName('turn%sDesc' % typeStr)
        itemNum = self.getSpriteConsumeItemNum(spriteInfo)
        desc.text = gameStrings.SPRITE_SKILL_TRANSFER_CONSUME_DESC % itemNum

    def getSpriteConsumeItemNum(self, spriteInfo):
        spriteConsumesDict = SCD.data.get('spriteSkillConsumes', {})
        logSrc = spriteConsumesDict.get('logSrc', 505)
        itemId = spriteConsumesDict.get('itemId', 785012)
        _consumesDict = spriteInfo.get('_consumesDict', {})
        itemNum = _consumesDict.get(logSrc, {}).get(itemId, 0)
        return itemNum

    def updateTurnOutAfterSkill(self):
        for i in xrange(SKILL_SLOT_NUM):
            itemSlot = self.widget.transferMc.getChildByName('turnOutSlot%d' % i)
            itemSlot.slot.setItemSlotData(None)
            itemSlot.lock.visible = not i < SPRITE_INIT_SLOT_NUM

        desc = self.widget.transferMc.turnOutDesc
        desc.text = gameStrings.SPRITE_SKILL_TRANSFER_CONSUME_DESC % 0

    def updateTurnInAfterSkill(self):
        p = BigWorld.player()
        trunOutSpriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        turnInSpriteInfo = p.summonSpriteList.get(self.turnInSpriteIdx, {})
        learnedSkillInfos = self.getLearnedSkillInfo(trunOutSpriteInfo)
        disableSkills = self.getDisableSkillInfo(turnInSpriteInfo)
        for i in xrange(SKILL_SLOT_NUM):
            itemSlot = self.widget.transferMc.getChildByName('turnInSlot%d' % i)
            info = learnedSkillInfos.get(i, None)
            if info:
                slotState = info.get('slot', 0)
                spriteSkillId = info.get('id', 0)
                if spriteSkillId in disableSkills and disableSkills[spriteSkillId]:
                    spriteSkillId = disableSkills[spriteSkillId]
                stateLocked = slotState == const.SSPRITE_SKILL_SLOT_FORBIDDEN
                itemSlot.lock.visible = stateLocked
                ASUtils.setHitTestDisable(itemSlot.lock, stateLocked)
                skillId = SSSD.data.get(spriteSkillId, {}).get('virtualSkill', 0)
                if skillId:
                    skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
                    iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                    itemSlot.slot.fitSize = True
                    itemSlot.slot.dragable = False
                    itemSlot.slot.setItemSlotData({'iconPath': iconPath})
                    itemSlot.slot.validateNow()
                    TipManager.addTipByType(itemSlot.slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                     'lv': SPRITE_SKILL_LEVEL}, False, 'upLeft')
                else:
                    itemSlot.slot.setItemSlotData(None)
            else:
                itemSlot.slot.setItemSlotData(None)
                itemSlot.lock.visible = True

        outRareLv = trunOutSpriteInfo.get('rareLv', 0)
        InRareLv = turnInSpriteInfo.get('rareLv', 0)
        srcNum = self.getSpriteConsumeItemNum(trunOutSpriteInfo)
        dstNum = self.getSpriteConsumeItemNum(turnInSpriteInfo)
        params = {'srcScore': srcNum,
         'srcRare': outRareLv,
         'dstScore': dstNum,
         'dstRare': InRareLv}
        spriteId = trunOutSpriteInfo.get('spriteId', 0)
        freeItemId = SCD.data.get('spriteIdToTransferSkillItem', {}).get(spriteId, 0)
        if freeItemId:
            ownNumFree = p.inv.countItemInPages(uiUtils.getParentId(freeItemId), enableParentCheck=True)
        if outRareLv >= InRareLv:
            formulaId = SCD.data.get('qizhiNumConsumedFormulaId', 90179)
        elif freeItemId and ownNumFree:
            formulaId = SCD.data.get('qizhiNumConsumedFormulaId2', 90187)
        else:
            formulaId = SCD.data.get('qizhiNumConsumedFormulaId3', 90189)
        itemNum = formula.calcFormulaById(formulaId, params)
        desc = self.widget.transferMc.turnInDesc
        desc.text = gameStrings.SPRITE_SKILL_TRANSFER_CONSUME_DESC % itemNum

    def getLearnedSkillInfo(self, spriteInfo):
        infos = {}
        learnedSkills = spriteInfo.get('skills', {}).get('learns', [])
        if learnedSkills:
            for info in learnedSkills:
                infos[info.get('part', None)] = info

        return infos

    def checkHasFreeItem(self, spriteInfo):
        p = BigWorld.player()
        spriteId = spriteInfo.get('spriteId', 0)
        freeItemId = SCD.data.get('spriteIdToTransferSkillItem', {}).get(spriteId, 0)
        if not freeItemId:
            return False
        needNum = 1
        ownNum = p.inv.countItemInPages(uiUtils.getParentId(freeItemId), enableParentCheck=True)
        if ownNum < needNum:
            return False
        return True

    def getDisableSkillInfo(self, turnInSpriteInfo):
        turnInSkillInfo = self.getLearnedSkillInfo(turnInSpriteInfo)
        disableSkills = {}
        for i, part in enumerate(turnInSkillInfo):
            info = turnInSkillInfo[part]
            spriteSkillId = info.get('id', 0)
            if spriteSkillId:
                disableLearnSkillRefIds = SSSD.data.get(spriteSkillId, {}).get('disableLearnSkillRefIds', ())
                disableSkillRefId = disableLearnSkillRefIds[0] if disableLearnSkillRefIds else 0
                if disableSkillRefId:
                    disableSkills[disableSkillRefId] = spriteSkillId

        return disableSkills

    def updateConsumeItem(self):
        p = BigWorld.player()
        spriteId = p.summonSpriteList.get(self.spriteIndex, {}).get('spriteId', 0)
        freeItemId = SCD.data.get('spriteIdToTransferSkillItem', {}).get(spriteId, 0)
        if freeItemId:
            needNumFree = 1
            ownNumFree = p.inv.countItemInPages(uiUtils.getParentId(freeItemId), enableParentCheck=True)
        trunOutSpriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        turnInSpriteInfo = p.summonSpriteList.get(self.turnInSpriteIdx, {})
        outRareLv = trunOutSpriteInfo.get('rareLv', 0)
        InRareLv = turnInSpriteInfo.get('rareLv', 0)
        srcNum = self.getSpriteConsumeItemNum(trunOutSpriteInfo)
        dstNum = self.getSpriteConsumeItemNum(turnInSpriteInfo)
        params = {'srcScore': srcNum,
         'srcRare': outRareLv,
         'dstScore': dstNum,
         'dstRare': InRareLv}
        if freeItemId and ownNumFree:
            if outRareLv >= InRareLv:
                self.widget.consumeSlot0.visible = False
                self.widget.consumeSlot1.visible = False
                self.widget.consumeSlot2.visible = True
                self.updateItemSlot(self.widget.consumeSlot2, freeItemId, ownNumFree, needNumFree)
                self.canTransfer = ownNumFree >= needNumFree
            else:
                self.widget.consumeSlot0.visible = True
                self.widget.consumeSlot1.visible = True
                self.widget.consumeSlot2.visible = False
                self.updateItemSlot(self.widget.consumeSlot0, freeItemId, ownNumFree, needNumFree)
                qizhiItemId = 785012
                ownNum1 = p.inv.countItemInPages(uiUtils.getParentId(qizhiItemId), enableParentCheck=True)
                formulaId = SCD.data.get('qizhiNumNeedFormulaId2', 90186)
                needNum1 = formula.calcFormulaById(formulaId, params)
                self.updateItemSlot(self.widget.consumeSlot1, qizhiItemId, ownNum1, needNum1)
                self.canTransfer = ownNumFree >= needNumFree and ownNum1 >= needNum1
        else:
            self.widget.consumeSlot0.visible = True
            self.widget.consumeSlot1.visible = True
            self.widget.consumeSlot2.visible = False
            transferItemId = SCD.data.get('CommonTransferSpriteSkillItem', 787521)
            ownNum0 = p.inv.countItemInPages(uiUtils.getParentId(transferItemId), enableParentCheck=True)
            needNum0 = 1
            self.updateItemSlot(self.widget.consumeSlot0, transferItemId, ownNum0, needNum0)
            qizhiItemId = 785012
            ownNum1 = p.inv.countItemInPages(uiUtils.getParentId(qizhiItemId), enableParentCheck=True)
            if outRareLv >= InRareLv:
                formulaId = SCD.data.get('qizhiNumNeedFormulaId', 90178)
            else:
                formulaId = SCD.data.get('qizhiNumNeedFormulaId3', 90188)
            needNum1 = formula.calcFormulaById(formulaId, params)
            self.updateItemSlot(self.widget.consumeSlot1, qizhiItemId, ownNum1, needNum1)
            self.canTransfer = ownNum0 >= needNum0 and ownNum1 >= needNum1

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
        itemSlot.lock.visible = False
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemSlot.slot.setItemSlotData(itemInfo)
        itemSlot.slot.validateNow()
        ASUtils.setHitTestDisable(itemSlot.slotNum, True)
        itemSlot.slotNum.htmlText = count

    def transferSpriteSkillSuccess(self, sourceSpriteIndex):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_SKILL_TRANSFER_SUCCESS, ())
        if not self.widget:
            return
        if self.spriteIndex != sourceSpriteIndex:
            return
        self.turnInSpriteIdx = 0
        self.widget.frontBtn.selected = True
        self.widget.afterBtn.selected = False
        self.refreshInfo()
