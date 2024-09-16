#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schemeResumeProxy.o
import BigWorld
import uiConst
import events
import uiUtils
import utils
import time
from uiProxy import UIProxy
from gameStrings import gameStrings
from data import sys_config_data as SCD
STEP_SELECT_TIME = 1
STEP_CONFIRM_ITEM = 2

class SchemeResumeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchemeResumeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.panelType = 0
        self.schemeNo = 0
        self.step = STEP_SELECT_TIME
        self.choice = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHEME_RESUME, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHEME_RESUME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHEME_RESUME)

    def reset(self):
        self.panelType = 0
        self.schemeNo = 0
        self.step = STEP_SELECT_TIME
        self.choice = 0

    def show(self, panelType, schemeNo):
        if not self.widget:
            self.panelType = panelType
            self.schemeNo = schemeNo
            self.step = STEP_SELECT_TIME
            self.choice = 1
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHEME_RESUME)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.detail1.visible = False
        self.widget.detail1.select0.tag = 0
        self.widget.detail1.select1.tag = 1
        self.widget.detail2.visible = False
        self.widget.detail2.itemSlot.dragable = False
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancelBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if self.step == STEP_SELECT_TIME:
            self.widget.detail1.visible = True
            self.widget.detail2.visible = False
            detail1 = self.widget.detail1
            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                expireTime = p.getWSSchemeExpireTime(self.schemeNo)
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                expireTime = p.getEquipSoulSchemeExpireTime(self.schemeNo)
            else:
                expireTime = 0
            itemData = self.getItemData()
            day1 = itemData.get(1)[1] / uiConst.ONE_DAT_TIME
            day2 = itemData.get(2)[1] / uiConst.ONE_DAT_TIME
            if expireTime > 0:
                detail1.title.text = gameStrings.SCHEME_RESUME_TITLE_RENEWAL
                detail1.select0.label = gameStrings.SCHEME_RESUME_TITLE_RENEWAL_DAY % day1
                detail1.select1.label = gameStrings.SCHEME_RESUME_TITLE_RENEWAL_DAY % day2
            else:
                detail1.title.text = gameStrings.SCHEME_RESUME_TITLE_BUY
                detail1.select0.label = gameStrings.SCHEME_RESUME_TITLE_BUY_DAY % day1
                detail1.select1.label = gameStrings.SCHEME_RESUME_TITLE_BUY_DAY % day2
            detail1.select0.selected = self.choice == 1
            detail1.select1.selected = self.choice == 2
            self.widget.confirmBtn.enabled = True
        elif self.step == STEP_CONFIRM_ITEM:
            self.widget.detail1.visible = False
            self.widget.detail2.visible = True
            detail2 = self.widget.detail2
            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                schemeName = p.getWSSchemeName(self.schemeNo)
                expireTime = p.getWSSchemeExpireTime(self.schemeNo)
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                schemeName = p.getEquipSoulSchemeName(self.schemeNo)
                expireTime = p.getEquipSoulSchemeExpireTime(self.schemeNo)
            else:
                schemeName = uiUtils.getDefaultSchemeName(self.panelType, self.schemeNo)
                expireTime = 0
            itemData = self.getItemData()
            addTime = itemData.get(self.choice)[1]
            day = addTime / uiConst.ONE_DAT_TIME
            now = utils.getNow()
            if expireTime > 0:
                detail2.costText.text = gameStrings.SCHEME_RESUME_TITLE_RENEWAL_COST % day
                if expireTime > now:
                    finalTime = expireTime + addTime
                else:
                    finalTime = now + addTime
            else:
                detail2.costText.text = gameStrings.SCHEME_RESUME_TITLE_BUY_COST % day
                finalTime = now + addTime
            detail2.timeText.htmlText = gameStrings.SCHEME_RESUME_DATE % (schemeName, time.strftime('%Y.%m.%d  %H:%M', time.localtime(finalTime)))
            needNum = 1
            itemId, ownNum = self.getCanShowItemId(itemData.get(self.choice)[0], needNum)
            itemInfo = uiUtils.getGfxItemById(itemId)
            if ownNum < needNum:
                itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
                self.widget.confirmBtn.enabled = False
            else:
                itemInfo['count'] = '%d/%d' % (ownNum, needNum)
                itemInfo['state'] = uiConst.ITEM_NORMAL
                self.widget.confirmBtn.enabled = True
            detail2.itemSlot.setItemSlotData(itemInfo)

    def getItemData(self):
        p = BigWorld.player()
        if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
            expireTime = p.getWSSchemeExpireTime(self.schemeNo)
            if expireTime > 0:
                return SCD.data.get('resetSkillSchemeExpireData', {})
            else:
                return SCD.data.get('enableSkillSchemeData', {})
        else:
            if self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                return SCD.data.get('enableEquipSoulSchemeData', {})
            return {}

    def getCanShowItemId(self, itemList, needNum):
        p = BigWorld.player()
        tempItemId = 0
        tempOwnNum = 0
        for itemId in itemList:
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if ownNum >= needNum:
                return (itemId, ownNum)
            if tempItemId == 0:
                tempItemId = itemId
                tempOwnNum = ownNum

        return (tempItemId, tempOwnNum)

    def handleClickConfirmBtn(self, *args):
        if self.step == STEP_SELECT_TIME:
            if self.widget.detail1.select0.selected:
                self.choice = 1
            elif self.widget.detail1.select1.selected:
                self.choice = 2
            else:
                return
            self.step = STEP_CONFIRM_ITEM
            self.refreshInfo()
        elif self.step == STEP_CONFIRM_ITEM:
            p = BigWorld.player()
            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                expireTime = p.getWSSchemeExpireTime(self.schemeNo)
                p.cell.enableWSSkillScheme(self.schemeNo, expireTime == 0, self.choice)
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                p.cell.enableEquipSoulScheme(self.schemeNo, self.choice)
            self.hide()

    def handleClickCancelBtn(self, *args):
        if self.step == STEP_SELECT_TIME:
            self.hide()
        elif self.step == STEP_CONFIRM_ITEM:
            self.step = STEP_SELECT_TIME
            self.refreshInfo()
