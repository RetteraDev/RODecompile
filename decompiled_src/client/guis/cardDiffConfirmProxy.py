#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardDiffConfirmProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
import events
import gametypes
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import conditional_prop_data as CPD
from data import prop_ref_data as PRD
from data import advance_card_data as ACD
from data import card_atlas_data as CAD
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import pskill_template_data as PTD
from cdata import pskill_data as PDD
TITLE_COLOR = '#B3915C'
CONTENT_COLOR = '#0088CC'
TITLE_OFFSET_Y = 30
CONTENT_OFFSET_Y = 8
CONTENT_OFFSET_X = 80
SLOT_WIDTH = 120
EXTRAMC_OFFSET_X = 160
BUTTON_OFFSET_X_1 = 136
BUTTON_OFFSET_X_2 = 245
BASE_HEIGHT = 125
DASHLINE_POS_X = 20
ITEM_CENTER_POS_X = 40

class CardDiffConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardDiffConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_DIFF_CONFIRM, self.hide)

    def reset(self):
        self.cardId = None
        self.diffType = None
        self.diffLv = 0
        self.callback = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_DIFF_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_DIFF_CONFIRM)

    def show(self, cardId, diffType, callback):
        self.cardId = cardId
        self.diffType = diffType
        p = BigWorld.player()
        if diffType == uiConst.CARD_DIFF_TYPE_UPGRADE:
            cardObj = p.getCard(self.cardId)
            if cardObj:
                if cardObj.actived:
                    self.diffLv = 1
                else:
                    self.diffLv = 0
        elif diffType == uiConst.CARD_DIFF_TYPE_DEGRADE:
            self.diffLv = -1
        self.callback = callback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_DIFF_CONFIRM)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.removeAllInst(self.widget.canvas)
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        cardGoalLv = cardObj.advanceLvEx + self.diffLv
        canvasHeight = 0
        lastPropItemY = 0
        titleItem = self.widget.getInstByClsName('CardDiffConfirm_ConfirmTitle')
        self.widget.canvas.addChild(titleItem)
        lastPropItemY = titleItem.y + titleItem.height
        activeProps, bShow = self.getDiffActiveProp()
        if bShow:
            pText = ''
            for propId, propVal in activeProps:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, separator='  ')

            if not pText:
                pText = gameStrings.CARD_DIFF_PROP_NONE
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_ACTIVE_PROP, pText, lastPropItemY)
            lastPropItemY = propertyItem.y + propertyItem.contentTxt.textHeight
        advanceProps, bShow = self.getDiffAdvanceProp()
        if bShow:
            pText = ''
            for propId, propVal in advanceProps:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, separator='  ')

            if not pText:
                pText = gameStrings.CARD_DIFF_PROP_NONE
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_ADVANCE_PROP, pText, lastPropItemY)
            lastPropItemY = propertyItem.y + propertyItem.contentTxt.textHeight
        atlasProp, bShow = self.getDiffAtlasProp()
        if bShow:
            pText = ''
            for propId, propVal in atlasProp:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, separator='\n')

            verId = cardObj.version
            conMax = self.uiAdapter.cardSystem.getAtlasConMax(verId)
            atlasData = CAD.data.get(verId, {})
            gameStrings.CARD_DIFF_ATLAS_PROP_ACTIVATE
            activedNum = self.uiAdapter.cardSystem.getAtlasActivedNumData(verId)
            goalActivedNum = activedNum + 1 if self.diffType == uiConst.CARD_DIFF_TYPE_UPGRADE else activedNum - 1
            goalActivedNum = min(conMax, goalActivedNum)
            numStr = uiUtils.convertNumStr(goalActivedNum, conMax, enoughColor='', notEnoughColor='')
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_ATLAS_PROP_ACTIVATE % (atlasData.get('version', ''),), numStr, lastPropItemY)
            lastPropItemY = contentItem.y + contentItem.contentTxt.textHeight
            if not pText:
                pText = gameStrings.CARD_DIFF_PROP_NONE
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_ATLAS_PROP % (atlasData.get('version', ''),), pText, lastPropItemY)
            lastPropItemY = propertyItem.y + propertyItem.contentTxt.textHeight
        pSkills, cSkills, bShow = self.getCardSkillProp()
        if bShow:
            pText = ''
            for skillId, lv in pSkills:
                pText += PDD.data.get((skillId, lv), {}).get('desc', '') + '\n'
                pText = pText.replace('<', '&lt;').replace('>', '&gt;')

            for skillId, propVal in cSkills:
                condData = CPD.data.get(skillId, {})
                formatType = int(condData.get('formatType', 0))
                desc = condData.get('desc', '')
                desc = desc.replace('<', '&lt;').replace('>', '&gt;')
                if formatType == const.COND_PROP_NUM_PERCENT:
                    desc = desc % (propVal * 100,)
                else:
                    desc = desc % (propVal,)
                pText += desc + '\n'

            if not pText:
                pText = gameStrings.CARD_DIFF_PROP_NONE
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_EQUIP_PSKILLS, pText, lastPropItemY)
            lastPropItemY = propertyItem.y + propertyItem.contentTxt.textHeight
        if self.diffType == uiConst.CARD_DIFF_TYPE_UPGRADE and cardGoalLv == const.CARD_BREAK_RANK:
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_OUTLINE_GOLD, '', lastPropItemY)
            lastPropItemY = contentItem.y + contentItem.contentTxt.textHeight
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_CHANGE_OPEN, '', lastPropItemY)
            lastPropItemY = contentItem.y + contentItem.contentTxt.textHeight
        elif self.diffType == uiConst.CARD_DIFF_TYPE_DEGRADE and cardGoalLv == const.CARD_BREAK_RANK - 1:
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_OUTLINE_NORMAL, '', lastPropItemY)
            lastPropItemY = contentItem.y + contentItem.contentTxt.textHeight
            contentItem, propertyItem = self.appendPropText(gameStrings.CARD_DIFF_CHANGE_CLOSE, '', lastPropItemY)
            lastPropItemY = contentItem.y + contentItem.contentTxt.textHeight
        extraItems = cardObj.getExtraItemsEx()
        if extraItems and self.diffType == uiConst.CARD_DIFF_TYPE_UPGRADE:
            dashLine0 = self.widget.getInstByClsName('M12_DefaultDashLine')
            self.widget.canvas.addChild(dashLine0)
            dashLine0.y = lastPropItemY + CONTENT_OFFSET_Y + 10
            lastPropItemY = dashLine0.y + dashLine0.height
            extraMc = self.widget.getInstByClsName('CardDiffConfirm_ExtraItem')
            self.widget.canvas.addChild(extraMc)
            extraMc.x = EXTRAMC_OFFSET_X
            extraMc.y = lastPropItemY + CONTENT_OFFSET_Y + 10
            self.widget.removeAllInst(extraMc.slotCanvas)
            itemNum = len(extraItems)
            for i, (itemIds, itemNum) in enumerate(extraItems):
                if itemIds:
                    itemId = itemIds[-1]
                    itemMc = self.widget.getInstByClsName('CardDiffConfirm_NameSlot')
                    extraMc.slotCanvas.addChild(itemMc)
                    halfNum = len(extraItems) / 2.0
                    itemMc.x = SLOT_WIDTH * i - SLOT_WIDTH * halfNum + ITEM_CENTER_POS_X
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    count = 0
                    for iId in itemIds:
                        count += p.inv.countItemInPages(iId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)

                    numStr = uiUtils.convertNumStr(count, itemNum)
                    itemInfo['count'] = numStr
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(itemInfo)
                    itemMc.nameTxt.text = ID.data.get(itemId, {}).get('name', '')

            lastPropItemY = extraMc.y + extraMc.height
            descTxt = ''
            if cardObj.isCurrentPeriod:
                descTxt += gameStrings.CARD_DIFF_PERIOD_BOSS
            if cardObj.isBreakRank:
                if descTxt:
                    descTxt += gameStrings.CARD_DIFF_UPGRADE_SEPARATOR
                    label = gameStrings.CARD_DIFF_BREAK_RANK
                    descTxt += label
                else:
                    label = gameStrings.CARD_DIFF_BREAK_RANK
                    descTxt += label
            descTxt += gameStrings.CARD_DIFF_UPGRADE_DESC
            extraMc.descTxt.text = descTxt
        dashLine1 = self.widget.getInstByClsName('M12_FenGeLine_LV2')
        self.widget.canvas.addChild(dashLine1)
        dashLine1.y = lastPropItemY + CONTENT_OFFSET_Y + 10
        dashLine1.x = DASHLINE_POS_X
        lastPropItemY = dashLine1.y + dashLine1.height
        confirmBtn = self.widget.getInstByClsName('M12_TongYongButton_1')
        self.widget.canvas.addChild(confirmBtn)
        confirmBtn.label = gameStrings.COMMON_CONFIRM
        confirmBtn.x = BUTTON_OFFSET_X_1
        confirmBtn.y = lastPropItemY + CONTENT_OFFSET_Y
        confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        cancelBtn = self.widget.getInstByClsName('M12_TongYongButton_1')
        self.widget.canvas.addChild(cancelBtn)
        cancelBtn.label = gameStrings.COMMON_CANCEL
        cancelBtn.x = BUTTON_OFFSET_X_2
        cancelBtn.y = lastPropItemY + CONTENT_OFFSET_Y
        cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.bg.height = BASE_HEIGHT + lastPropItemY

    def appendPropText(self, titleText, propText, y, retItem = None):
        contentItem = None
        if titleText:
            contentItem = self.widget.getInstByClsName('CardDiffConfirm_ContentItem')
            contentItem.contentTxt.htmlText = titleText
            contentItem.x = CONTENT_OFFSET_X
            contentItem.y = y + CONTENT_OFFSET_Y
            self.widget.canvas.addChild(contentItem)
            if not retItem:
                retItem = contentItem
        propertyItem = None
        if propText:
            propertyItem = self.widget.getInstByClsName('CardDiffConfirm_PropertyItem')
            propertyItem.contentTxt.htmlText = propText
            propertyItem.y = contentItem.y
            propertyItem.x = retItem.x + retItem.contentTxt.textWidth + 10
            self.widget.canvas.addChild(propertyItem)
        return (contentItem, propertyItem)

    def getDiffAdvanceProp(self):
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        if cardObj:
            curAdvance = ()
            if cardObj.actived:
                curAdvance = cardObj.advanceProps
            goalAdvance = ACD.data.get(cardObj.id * const.CARD_PRESERVED_RANK + cardObj.advanceLvEx + self.diffLv, {}).get('advanceProps', ())
            if set(curAdvance) != set(goalAdvance):
                return (goalAdvance, True)
        return ([], False)

    def getDiffActiveProp(self):
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        if cardObj:
            curActive = []
            if cardObj.actived:
                curActive = cardObj.activeProps
            goalActive = ACD.data.get(cardObj.id * const.CARD_PRESERVED_RANK + cardObj.advanceLvEx + self.diffLv, {}).get('activeProps', ())
            if set(curActive) != set(goalActive):
                return (goalActive, True)
        return ([], False)

    def getDiffAtlasProp(self):
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        if cardObj:
            goalAdvanceLv = cardObj.advanceLvEx + self.diffLv
            verId = cardObj.version
            activedNum = self.uiAdapter.cardSystem.getAtlasActivedNumData(verId)
            atlasData = CAD.data.get(verId, {})
            propArr = []
            if not cardObj.actived and self.diffType == uiConst.CARD_DIFF_TYPE_UPGRADE:
                bShow = False
                for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
                    cond = atlasData.get('cond' + str(num), 0)
                    if cond and cond <= activedNum + 1:
                        propArr += atlasData.get('prop' + str(num), ((0, 0),))
                    if cond and cond == activedNum + 1:
                        bShow = True

                if bShow:
                    return (propArr, bShow)
            if not cardObj.advanceLvEx and self.diffType == uiConst.CARD_DIFF_TYPE_DEGRADE:
                bShow = False
                for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
                    cond = atlasData.get('cond' + str(num), 0)
                    if cond and cond <= activedNum - 1:
                        propArr += atlasData.get('prop' + str(num), ((0, 0),))
                    if cond and cond == activedNum:
                        bShow = True

                if bShow:
                    return (propArr, bShow)
        return ([], False)

    def getPSkillProp(self):
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        if cardObj:
            curPskill = []
            if cardObj.actived:
                curPskill = cardObj.passivitySkills
            goalPskill = ACD.data.get(cardObj.id * const.CARD_PRESERVED_RANK + cardObj.advanceLvEx + self.diffLv, {}).get('passivity', ())
            if set(curPskill) != set(goalPskill):
                return (goalPskill, True)
        return ([], False)

    def getCardSkillProp(self):
        p = BigWorld.player()
        cardObj = p.getCard(self.cardId)
        if not cardObj:
            return ([], [], False)
        passivity, condSkill = self.uiAdapter.cardSystem.getCardSkillsOpenLv(cardObj)
        pSkill = []
        cardGoalLv = cardObj.advanceLvEx + self.diffLv
        for (skillId, lv), openLv in passivity.iteritems():
            if cardGoalLv == openLv:
                pSkill.append((skillId, lv))

        cSkill = []
        for (skillId, propVal), openLv in condSkill.iteritems():
            if cardGoalLv == openLv:
                cSkill.append((skillId, propVal))

        isShow = bool(pSkill) or bool(cSkill)
        return (pSkill, cSkill, isShow)

    def handleConfirmBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        if self.callback():
            self.callback()
        self.hide()

    def handleCancelBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
