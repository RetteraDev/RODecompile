#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteXiuLianProxy.o
from gamestrings import gameStrings
import BigWorld
import events
import gameglobal
import const
import ui
import utils
from uiProxy import UIProxy
from guis import uiUtils
from guis import uiConst
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import sprite_growth_entry_data as SGED
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import sprite_growth_category_data as SGCD
from cdata import game_msg_def_data as GMDD
from cdata import sprite_growth_entry_limit_data as SGELD
ITEM1_HEIGHT = 58
ITEM2_HEIGHT = 44

class SummonedWarSpriteXiuLianProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteXiuLianProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedParentId = 0
        self.selectedChildId = 0
        self.expItems = ()
        self.itemReplaceMoney = ()
        self.diKouMoney = 0

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedParentId = 0
        self.selectedChildId = 0
        self.expItems = ()
        self.itemReplaceMoney = ()
        self.diKouMoney = 0

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.spriteList.tree.lvItemGap = 2
        self.widget.spriteList.tree.itemRenderers = ['SummonedWarSpriteXiuLian_spriteItem1', 'SummonedWarSpriteXiuLian_spriteItem2']
        self.widget.spriteList.tree.itemHeights = [ITEM1_HEIGHT, ITEM2_HEIGHT]
        self.widget.spriteList.tree.labelFunction = self.treeLabelFun
        self.widget.spriteList.tree.addEventListener(events.EVENT_SELECTED_DATA_CHANGED, self.handleSelectChange, False, 0, True)
        self.widget.spriteList.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleTreeItemGroupChange, False, 0, True)
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.lvBtn.addEventListener(events.BUTTON_CLICK, self.handleLvBtnClick, False, 0, True)
        self.widget.recoverBtn.addEventListener(events.BUTTON_CLICK, self.handleRecoverBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            treeData = []
            for i, parentId in enumerate(SGCD.data):
                entrys = SGCD.data.get(parentId, {}).get('entrys', (1, 2, 3, 4))
                entrys = [ '%d_%d' % (parentId, childId) for childId in entrys ]
                treeData.append({'parent': parentId,
                 'children': entrys})

            self.widget.spriteList.tree.selectData = None
            if not self.selectedChildId and treeData:
                strChildren = treeData[0]['children'][0]
                parentId, childId = strChildren.split('_')
                self.selectedParentId = int(parentId)
                self.selectedChildId = int(childId)
            self.widget.spriteList.tree.dataArray = treeData
            self.widget.spriteList.tree.validateNow()
            if self.selectedChildId:
                self.widget.spriteList.tree.selectData = '%d_%d' % (self.selectedParentId, self.selectedChildId)
            self.updateTotalScore()
            return

    def updateTotalScore(self):
        if not self.widget:
            return
        p = BigWorld.player()
        totalScore = 0
        for i, parentId in enumerate(p.spriteGrowthInfo):
            scores = p.spriteGrowthInfo.get(parentId, {}).get('scores', 0)
            totalScore += scores

        desc0 = gameStrings.SUMMONED_WAR_SPRITE_XIU_LIAN_SCORE % totalScore
        desc1 = gameStrings.SUMMONED_WAR_SPRITE_XIU_LIAN_COMBAT % p.combatScoreList[const.SPRITE_GROWTH_SCORE]
        self.widget.scoreT.htmlText = '%s   %s' % (desc0, desc1)

    def checkConsumeItemEnough(self):
        p = BigWorld.player()
        isEnough = True
        for item in self.expItems:
            itemId = item[0]
            needNum = item[1]
            ownNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
            if ownNum < needNum:
                isEnough = False

        return isEnough

    def handleSureBtnClick(self, *args):
        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_XIU_LIAN_SURE):
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_XIU_LIAN_SURE_DESC, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onSureCallBack, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SPRITE_XIU_LIAN_SURE)
        else:
            self.onSureCallBack()

    def onSureCallBack(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if self.checkConsumeItemEnough():
            self.onRealGrowthExp()
        elif self.diKouMoney and p.bindCash >= self.diKouMoney:
            self.onRealGrowthExp()
        elif p.cash + p.bindCash >= self.diKouMoney:
            msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_SKILL_CONSUME_COIN_NOTIFY, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onRealGrowthExp, msgType='bindCash', isShowCheckBox=True)

    @ui.checkInventoryLock()
    def onRealGrowthExp(self):
        p = BigWorld.player()
        p.base.spriteGrowthEntryLvUp(self.selectedParentId, self.selectedChildId, p.cipherOfPerson)

    def handleLvBtnClick(self, *args):
        p = BigWorld.player()
        entries = p.spriteGrowthInfo.get(self.selectedParentId, {}).get('entries', {})
        if not entries:
            return
        curLv = entries.get(self.selectedChildId, {}).get('lv', 0)
        lvUpLimit = entries.get(self.selectedChildId, {}).get('lvUpLimit', 0)
        lvDelta = utils.spriteGrowthUpLimitDelta(self.selectedChildId, lvUpLimit)
        if lvUpLimit + lvDelta > utils.getSpriteGrowthEntryLvLimit(self.selectedChildId):
            p.showGameMsg(GMDD.data.SPRITE_XIU_LIAN_NONE_GROWTH_LV, ())
            return
        exceedItem = SGED.data.get((self.selectedChildId, lvUpLimit + lvDelta), {}).get('exceedItem', ())
        itemId, itemNum = exceedItem[0] if exceedItem else (0, 0)
        itemData = uiUtils.getGfxItemById(itemId, itemNum)
        ownNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        itemData['count'] = uiUtils.convertNumStr(ownNum, itemNum)
        yesBtnEnable = lvUpLimit <= utils.getSpriteGrowthEntryLvLimit(self.selectedChildId) and ownNum >= itemNum
        entryName = SGED.data.get((self.selectedChildId, curLv), {}).get('name', '')
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_XIU_LIAN_GROWTH_UP_MSG, '') % (entryName, entryName, lvUpLimit + lvDelta)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realGrowth), yesBtnEnable=yesBtnEnable, itemData=itemData)

    def realGrowth(self):
        p = BigWorld.player()
        p.base.raiseGrowthEntryUpLimit(self.selectedParentId, self.selectedChildId)

    def handleRecoverBtnClick(self, *args):
        if gameglobal.rds.configData.get('enableFreeRecoverSpriteGrowth', False):
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_XIU_LIAN_FREE_RECOVER):
                msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_XIU_LIAN_FREE_RECOVER_MSG, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realRecover), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SPRITE_XIU_LIAN_FREE_RECOVER)
            else:
                self.realRecover()
            return
        else:
            p = BigWorld.player()
            entries = p.spriteGrowthInfo.get(self.selectedParentId, {}).get('entries', 0)
            curLv = entries.get(self.selectedChildId, {}).get('lv', 0)
            nextLv = min(curLv + 1, utils.getSpriteGrowthEntryLvLimit(self.selectedChildId))
            sgedNextData = SGED.data.get((self.selectedChildId, nextLv), {})
            xiuLianName = sgedNextData.get('name', '')
            entryInfo = entries.get(self.selectedChildId, {})
            lvUpLimit = entryInfo.get('lvUpLimit', 0)
            initUpLimit = utils.spriteGrowthUpLimitInit(self.selectedChildId)
            recoverNum1 = utils.getConsumedGrowthExpItems(self.selectedChildId, curLv)
            recoverNum2 = utils.getConsumedGrowthExceedItems(self.selectedChildId, lvUpLimit)
            recoverNum1.update(recoverNum2)
            recoverItemDesc = ''
            for itemId, num in recoverNum1.items():
                itemDesc = '%s*%d' % (uiUtils.getItemColorName(itemId), num)
                if recoverItemDesc:
                    recoverItemDesc += ',' + itemDesc
                else:
                    recoverItemDesc += itemDesc

            if lvUpLimit == initUpLimit:
                recoverCost = SGED.data.get((self.selectedChildId, curLv), {}).get('recoverCost', ())
            else:
                recoverCost = SGED.data.get((self.selectedChildId, lvUpLimit), {}).get('recoverCost', ())
            if recoverCost:
                consumeItemId, consumeItemNum = recoverCost[0] if recoverCost else (0, 0)
                itemData = uiUtils.getGfxItemById(consumeItemId, consumeItemNum)
                ownNum = p.inv.countItemInPages(uiUtils.getParentId(consumeItemId), enableParentCheck=True)
                itemData['count'] = uiUtils.convertNumStr(ownNum, consumeItemNum)
                yesBtnEnable = ownNum >= consumeItemNum
            else:
                itemData = None
                yesBtnEnable = True
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_XIU_LIAN_RECOVER_MSG, gameStrings.TEXT_SUMMONEDWARSPRITEXIULIANPROXY_215) % (xiuLianName, recoverItemDesc)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realRecover), yesBtnEnable=yesBtnEnable, itemData=itemData)
            return

    @ui.checkInventoryLock()
    def realRecover(self):
        p = BigWorld.player()
        p.base.recoverSpriteGrowthEntry(self.selectedParentId, self.selectedChildId, p.cipherOfPerson)

    def handleSelectChange(self, *args):
        e = ASObject(args[3][0])
        if not e.data or not e.data.selectData:
            return
        if e.data.selectItem.disabled:
            return
        parentId, childId = e.data.selectData.split('_')
        self.selectedParentId = int(parentId)
        self.selectedChildId = int(childId)
        self.updateXiuLianDetail()

    def handleTreeItemGroupChange(self, *args):
        e = ASObject(args[3][0])
        target = e.data.item
        self.widget.spriteList.refreshHeight(self.widget.spriteList.tree.height)
        target.selected = e.data.expand

    def treeLabelFun(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        itemMc.isFirst = isFirst
        if isFirst:
            itemData = ASObject(args[3][1])
            self.updateParent(itemMc, itemData)
        else:
            itemData = args[3][1].GetString()
            self.updateChildren(itemMc, itemData)

    def updateParent(self, itemMc, itemData):
        parentId = itemData.parent
        itemMc.itemData = itemData
        itemMc.parentId = parentId
        p = BigWorld.player()
        if parentId in p.spriteGrowthInfo.keys() and p.spriteGrowthInfo.get(parentId, {}).get('isAvailable', False):
            unlockType = 'up'
            self.widget.spriteList.tree.firstItemDisabled(itemMc, False)
        else:
            unlockType = 'lock'
        scores = p.spriteGrowthInfo.get(parentId, {}).get('scores', 0)
        sgcdData = SGCD.data.get(parentId, {})
        szName = sgcdData.get('name', '')
        lvLimit = sgcdData.get('lvLimit', 0)
        jingJieLimit = sgcdData.get('jingJieLimit', 0)
        scoreLimit = sgcdData.get('scoreLimit', ())
        if unlockType == 'lock':
            itemMc.disabled = True
            scoreDesc = ''
            for limit in scoreLimit:
                id = limit[0]
                score = limit[1]
                name = SGCD.data.get(id, {}).get('name', '')
                curScore = p.spriteGrowthInfo.get(id, {}).get('scores', 0)
                szSocre = self.getTipColor(score, curScore, score)
                scoreDesc += gameStrings.SPRITE_XIU_LIAN_PARENT_CONDITION_TIP1 % (name, szSocre)

            szLv = self.getTipColor(lvLimit, p.lv, lvLimit)
            szJingJie = self.getJingJieName(jingJieLimit, p.jingJie)
            msgTip = gameStrings.SPRITE_XIU_LIAN_PARENT_CONDITION_TIP0 % (szName,
             szLv,
             szJingJie,
             scoreDesc)
            TipManager.addTip(itemMc, msgTip)
        else:
            itemMc.disabled = False
            TipManager.removeTip(itemMc)
        itemMc.unlockIcon.gotoAndStop(unlockType)
        itemMc.labels = [szName, scores]

    def getJingJieName(self, jingJieLimit, myJineJie):
        szJingjieName = gameStrings.SPRITE_XIU_LIAN_JINGJIE_TO_NAME.get(jingJieLimit, '')
        color = '#231d1b' if myJineJie >= jingJieLimit else '#d34024'
        return uiUtils.toHtml(szJingjieName, color)

    def getTipColor(self, val, val1, val2):
        color = '#231d1b' if val1 >= val2 else '#d34024'
        return uiUtils.toHtml(val, color)

    def updateChildren(self, itemMc, itemData):
        pId, cId = itemData.split('_')
        parentId = int(pId)
        childId = int(cId)
        itemMc.itemData = itemData
        itemMc.parentId = parentId
        itemMc.childId = childId
        if self.selectedParentId == parentId and self.selectedChildId == childId:
            self.widget.spriteList.tree.selectData = '%d_%d' % (self.selectedParentId, self.selectedChildId)
        p = BigWorld.player()
        entries = p.spriteGrowthInfo.get(parentId, {}).get('entries', {})
        curLv = entries.get(childId, {}).get('lv', 0)
        sgedData = SGED.data.get((childId, max(curLv, 1)), {})
        szName = sgedData.get('name', '')
        lvLimit = sgedData.get('lvLimit', 0)
        jingJieLimit = sgedData.get('jingJieLimit', 0)
        szLv = '%d/%d' % (curLv, utils.getSpriteGrowthEntryLvLimit(childId))
        if p.lv >= lvLimit and p.jingJie >= jingJieLimit:
            itemMc.disabled = False
            TipManager.removeTip(itemMc)
        else:
            itemMc.disabled = True
            szLv = self.getTipColor(lvLimit, p.lv, lvLimit)
            jingJieLimit = self.getTipColor(jingJieLimit, p.jingJie, jingJieLimit)
            msgTip = gameStrings.SPRITE_XIU_LIAN_CHILD_CONDITION_TIP % (szName, szLv, jingJieLimit)
            TipManager.addTip(itemMc, msgTip)
        itemMc.labels = [szName, szLv]
        itemMc.lvBar.currentValue = curLv
        itemMc.lvBar.maxValue = utils.getSpriteGrowthEntryLvLimit(childId)

    def getLvLimitUpValue(self, lvUpLimit):
        for i in xrange(lvUpLimit + 1, 100):
            data = SGED.data.get((self.selectedChildId, i), {})
            if data.get('exceedItem'):
                return (data.get('lvLimit', 0), data.get('jingJieLimit', 0))

        return (0, 0)

    def updateXiuLianDetail(self):
        p = BigWorld.player()
        entries = p.spriteGrowthInfo.get(self.selectedParentId, {}).get('entries', {})
        entryInfo = entries.get(self.selectedChildId, {})
        curLv = entryInfo.get('lv', 0)
        lvUpLimit = entryInfo.get('lvUpLimit', 0)
        lvDelta = utils.spriteGrowthUpLimitDelta(self.selectedChildId, lvUpLimit)
        self.widget.lvDescT.text = gameStrings.SPRITE_XIU_LIAN_GROWTH_LV_LIMIT % lvUpLimit
        nextLvUpLimit, nextJingJieUpLimit = self.getLvLimitUpValue(lvUpLimit)
        if lvUpLimit + lvDelta > utils.getSpriteGrowthEntryLvLimit(self.selectedChildId) or not lvDelta and lvUpLimit == utils.getSpriteGrowthEntryLvLimit(self.selectedChildId):
            lvLimitTip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_XIU_LIAN_NONE_GROWTH_LV, '')
            self.widget.lvBtn.disabled = True
            TipManager.addTip(self.widget.lvBtn, lvLimitTip)
        elif p.lv >= nextLvUpLimit and p.jingJie >= nextJingJieUpLimit:
            self.widget.lvBtn.disabled = False
            TipManager.removeTip(self.widget.lvBtn)
        else:
            szNextLv = self.getTipColor(nextLvUpLimit, p.lv, nextLvUpLimit)
            szNextJingJie = self.getJingJieName(nextJingJieUpLimit, p.jingJie)
            upLvTip = gameStrings.SPRITE_XIU_LIAN_LV_LIMIT_UP_TIP % (szNextLv, szNextJingJie)
            self.widget.lvBtn.disabled = True
            TipManager.addTip(self.widget.lvBtn, upLvTip)
        sgedData = SGED.data.get((self.selectedChildId, curLv), {})
        propAddDesc = sgedData.get('propAddDesc', '+0')
        nextLv = min(curLv + 1, utils.getSpriteGrowthEntryLvLimit(self.selectedChildId))
        sgedNextData = SGED.data.get((self.selectedChildId, nextLv), {})
        nextPropAddDesc = sgedNextData.get('propAddDesc', 0)
        nextPropContentDesc = sgedNextData.get('propContentDesc', '')
        nextPropContentDesc1 = sgedNextData.get('propContentDesc1', '')
        nextPropConditionDesc = sgedNextData.get('propConditionDesc', '')
        nextLvLimit = sgedNextData.get('lvLimit', 0)
        nextJingJieLimit = sgedNextData.get('jingJieLimit', 0)
        self.widget.contentDesc.text = nextPropContentDesc
        self.widget.contentDesc1.text = nextPropContentDesc1
        self.widget.conditionDesc.text = nextPropConditionDesc
        self.widget.selectName.text = '%s Lv.%s' % (sgedNextData.get('name', ''), curLv)
        self.widget.effectDesc.visible = True if curLv else False
        extraAddLv = SCD.data.get('rareSpriteExtraGrowthLv', 5)
        self.widget.effectDesc.text = SCD.data.get('rareSpriteEffectLvDesc', '%d') % (curLv + extraAddLv)
        canRecover = SGELD.data.get(self.selectedChildId, {}).get('canRecover', 0)
        if gameglobal.rds.configData.get('enableRecoverSpriteGrowth', False) and canRecover:
            self.widget.recoverBtn.visible = True
            if lvUpLimit <= utils.spriteGrowthUpLimitInit(self.selectedChildId) and curLv <= 0 or curLv < 10:
                self.widget.recoverBtn.disabled = True
                TipManager.addTip(self.widget.recoverBtn, gameStrings.SPRITE_XIU_LIAN_RECOVER_DISABLE_TIP)
            else:
                self.widget.recoverBtn.disabled = False
                TipManager.removeTip(self.widget.recoverBtn)
        else:
            self.widget.recoverBtn.visible = False
        if curLv >= utils.getSpriteGrowthEntryLvLimit(self.selectedChildId) or curLv == lvUpLimit or p.lv < nextLvLimit or p.jingJie < nextJingJieLimit:
            self.widget.lvMc.visible = False
            self.widget.maxLvMc.visible = True
            self.widget.maxLvMc.curLvT.text = gameStrings.SPRITE_XIU_LIAN_CURRENT_LV % curLv
            self.widget.maxLvMc.curPreT.text = propAddDesc
        else:
            self.widget.lvMc.visible = True
            self.widget.maxLvMc.visible = False
            self.widget.lvMc.curLvT.text = gameStrings.SPRITE_XIU_LIAN_CURRENT_LV % curLv
            self.widget.lvMc.curPreT.text = propAddDesc
            self.widget.lvMc.nextLvT.text = gameStrings.SPRITE_XIU_LIAN_NEXT_LV % nextLv
            self.widget.lvMc.nextPreT.text = nextPropAddDesc
        TipManager.removeTip(self.widget.sureBtn)
        if curLv >= utils.getSpriteGrowthEntryLvLimit(self.selectedChildId):
            self.widget.consumeMc.visible = False
            self.widget.maxLvDesc.visible = True
            self.widget.sureBtn.disabled = True
            self.widget.maxLvDesc.htmlText = gameStrings.SPRITE_XIU_LIAN_TO_MAX_LV_DESC
        elif curLv == lvUpLimit:
            self.widget.consumeMc.visible = False
            self.widget.maxLvDesc.visible = True
            self.widget.sureBtn.disabled = True
            self.widget.maxLvDesc.htmlText = gameStrings.SPRITE_XIU_LIAN_TO_LIMIT_LV_LESS % (lvUpLimit + lvDelta)
        elif p.lv < nextLvLimit or p.jingJie < nextJingJieLimit:
            self.widget.consumeMc.visible = False
            self.widget.maxLvDesc.visible = True
            self.widget.sureBtn.disabled = True
            szJingjieName = gameStrings.SPRITE_XIU_LIAN_JINGJIE_TO_NAME.get(nextJingJieLimit, '')
            if p.lv >= nextLvLimit:
                conditionDesc = gameStrings.SPRITE_XIU_LIAN_TO_JINGJIE_LESS % szJingjieName
            elif p.jingJie >= nextJingJieLimit:
                conditionDesc = gameStrings.SPRITE_XIU_LIAN_TO_PLAYER_LV_LESS % nextLvLimit
            else:
                conditionDesc = gameStrings.SPRITE_XIU_LIAN_TO_PLAYER_LV_AND_JINEJIELESS % (nextLvLimit, szJingjieName)
            self.widget.maxLvDesc.htmlText = conditionDesc
        else:
            self.widget.consumeMc.visible = True
            self.widget.maxLvDesc.visible = False
            self.widget.sureBtn.disabled = False
            self.expItems = sgedNextData.get('expItems', ())
            self.itemReplaceMoney = sgedNextData.get('itemReplaceMoney', ())
            if len(self.expItems) == 1:
                self.widget.consumeMc.gotoAndStop('type1')
                itemId, itemNum = self.expItems[0]
                ownNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
                self.updateConsumeItem(self.widget.consumeMc.slot, self.widget.consumeMc.slotNum, self.widget.consumeMc.itemName, itemId, itemNum, ownNum)
                self.updateBtnAndText1(self.widget.consumeMc.desc, itemId, itemNum, ownNum)
            elif len(self.expItems) == 2:
                self.widget.consumeMc.gotoAndStop('type2')
                itemId0, itemNum0 = self.expItems[0]
                ownNum0 = p.inv.countItemInPages(uiUtils.getParentId(itemId0), enableParentCheck=True)
                self.updateConsumeItem(self.widget.consumeMc.slot0, self.widget.consumeMc.slotNum0, self.widget.consumeMc.itemName0, itemId0, itemNum0, ownNum0)
                itemId1, itemNum1 = self.expItems[1]
                ownNum1 = p.inv.countItemInPages(uiUtils.getParentId(itemId1), enableParentCheck=True)
                self.updateConsumeItem(self.widget.consumeMc.slot1, self.widget.consumeMc.slotNum1, self.widget.consumeMc.itemName1, itemId1, itemNum1, ownNum1)
                self.updateBtnAndText2(self.widget.consumeMc.desc0, self.widget.consumeMc.desc1, itemId0, itemNum0, ownNum0, itemId1, itemNum1, ownNum1)

    def updateConsumeItem(self, slot, slotNum, itemName, itemId, needNum, ownNum):
        p = BigWorld.player()
        itemInfo = uiUtils.getGfxItemById(itemId)
        slot.fitSize = True
        slot.dragable = False
        slot.setItemSlotData(itemInfo)
        if ownNum < needNum:
            strNum = uiUtils.toHtml(ownNum, '#FF0000')
            slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            slot.addEventListener(events.MOUSE_DOWN, self.handleSlotClick, False, 0, True)
        else:
            strNum = uiUtils.toHtml(ownNum, '#FFFFE6')
            slot.setSlotState(uiConst.ITEM_NORMAL)
            slot.removeEventListener(events.MOUSE_DOWN, self.handleSlotClick)
        count = str('%s/%d' % (strNum, needNum))
        ASUtils.setHitTestDisable(slotNum, True)
        slotNum.htmlText = count
        itemName.text = ID.data.get(itemId, {}).get('name', '')

    def handleSlotClick(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()

    def getReplaceMoney(self, itemId):
        replaceMoney = 0
        for itemReplaceId, money in self.itemReplaceMoney:
            if itemReplaceId == itemId:
                replaceMoney = money

        return replaceMoney

    def updateBtnAndText1(self, descText, itemId, needNum, ownNum):
        p = BigWorld.player()
        replaceMoney = self.getReplaceMoney(itemId)
        if not replaceMoney:
            descText.visible = False
            self.widget.sureBtn.disabled = ownNum < needNum
            return
        else:
            maxDiKouNum = ownNum + int((p.bindCash + p.cash) * 1.0 / replaceMoney)
            diKouNum = max(needNum - ownNum, 0)
            self.diKouMoney = diKouNum * replaceMoney
            if not maxDiKouNum:
                msgDesc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_LIU_LIAN_LACK_CASH_DESC, '')
                descText.htmlText = msgDesc
                descText.visible = True
                self.widget.sureBtn.disabled = True
            elif diKouNum:
                descText.htmlText = gameStrings.SPRITE_XIU_LIAN_LESS_ITEM_DESC % uiUtils.convertNumStr(p.cash + p.bindCash, self.diKouMoney, False, enoughColor=None)
                descText.visible = True
                if p.bindCash + p.cash >= self.diKouMoney:
                    self.widget.sureBtn.disabled = False
                else:
                    self.widget.sureBtn.disabled = True
                    TipManager.addTip(self.widget.sureBtn, gameStrings.SPRITE_XIU_LIAN_LESS_CAHS_OR_ITEM)
            else:
                descText.visible = False
                self.widget.sureBtn.disabled = False
            return

    def updateBtnAndText2(self, descText0, descText1, itemId0, needNum0, ownNum0, itemId1, needNum1, ownNum1):
        p = BigWorld.player()
        replaceMoney0 = self.getReplaceMoney(itemId0)
        replaceMoney1 = self.getReplaceMoney(itemId1)
        if not replaceMoney0 and not replaceMoney1:
            descText0.visible = False
            descText1.visible = False
            self.widget.sureBtn.disabled = not (ownNum0 >= needNum0 and ownNum1 >= needNum1)
            return
        maxOwnNum = 0
        maxNeedNum = needNum0 + needNum1
        if replaceMoney0:
            descText0.visible = True
            descText1.visible = False
            maxDiKouNum = ownNum0 + int((p.bindCash + p.cash) * 1.0 / replaceMoney0)
            diKouNum = max(needNum0 - ownNum0, 0)
            maxOwnNum = maxDiKouNum + ownNum1
            self.updateDiKouText(descText0, maxDiKouNum, diKouNum, replaceMoney0)
        elif replaceMoney1:
            descText0.visible = False
            descText1.visible = True
            maxDiKouNum = ownNum1 + int((p.bindCash + p.cash) * 1.0 / replaceMoney1)
            diKouNum = max(needNum1 - ownNum1, 0)
            maxOwnNum = maxDiKouNum + ownNum0
            self.updateDiKouText(descText1, maxDiKouNum, diKouNum, replaceMoney1)
        if not maxOwnNum:
            self.widget.sureBtn.disabled = True
        elif maxOwnNum >= maxNeedNum:
            self.widget.sureBtn.disabled = False
        else:
            self.widget.sureBtn.disabled = True
            TipManager.addTip(self.widget.sureBtn, gameStrings.SPRITE_XIU_LIAN_LESS_CAHS_OR_ITEM)

    def updateDiKouText(self, descText, maxDiKouNum, diKouNum, replaceMoney):
        p = BigWorld.player()
        self.diKouMoney = diKouNum * replaceMoney
        if not maxDiKouNum:
            msgDesc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_LIU_LIAN_LACK_CASH_DESC, '')
            descText.htmlText = msgDesc
            descText.visible = True
        elif diKouNum:
            descText.htmlText = gameStrings.SPRITE_XIU_LIAN_LESS_ITEM_DESC % uiUtils.convertNumStr(p.cash + p.bindCash, self.diKouMoney, False, enoughColor=None)
            descText.visible = True
        else:
            descText.visible = False

    def updateSpriteGrowthEntryLvUp(self):
        if not self.widget:
            return
        treeList = self.widget.spriteList.tree
        for i in xrange(0, treeList.numChildren):
            itemMc = treeList.getChildAt(i)
            if itemMc.isFirst:
                self.updateParent(itemMc, itemMc.itemData)
            else:
                self.updateChildren(itemMc, itemMc.itemData)

        self.updateTotalScore()
        self.updateXiuLianDetail()

    def spriteLvUpLimitSuccess(self, categoryId, entryId):
        if not self.widget:
            return
        if self.selectedParentId != categoryId or self.selectedChildId != entryId:
            return
        self.updateTotalScore()
        self.updateXiuLianDetail()
