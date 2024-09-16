#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schemeSwitchProxy.o
import BigWorld
import uiConst
import uiUtils
import events
import utils
import time
from uiProxy import UIProxy
from asObject import ASObject
from gameStrings import gameStrings
from cdata import game_msg_def_data as GMDD
SCHEME_BASE = (0,)
SCHEME_APPRECIATION = (1, 2)
SCHEME_VIP = (3,)
MAX_SCHEME_NUM = 4
EQUIP_SOUL_SCHEMENO_OFFSET = 1

class SchemeSwitchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchemeSwitchProxy, self).__init__(uiAdapter)
        self.widget = None
        self.panelType = 0
        self.selectedSchemeNo = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHEME_SWITCH, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHEME_SWITCH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHEME_SWITCH)

    def reset(self):
        self.panelType = 0
        self.selectedSchemeNo = -1

    def show(self, panelType):
        if not self.widget:
            self.panelType = panelType
            p = BigWorld.player()
            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                self.selectedSchemeNo = p.getCurWSSchemeNo()
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                self.selectedSchemeNo = p.currEquipSoulSchemeNo - EQUIP_SOUL_SCHEMENO_OFFSET
            else:
                self.selectedSchemeNo = 0
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHEME_SWITCH)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.title.textField.text = gameStrings.SCHEME_SWITCH_TITLE.get(self.panelType, '')
        for i in xrange(MAX_SCHEME_NUM):
            itemMc = getattr(self.widget, 'scheme%d' % i, None)
            if not itemMc:
                continue
            itemMc.schemeNo = i
            if i in SCHEME_BASE:
                itemMc.detail.icon.gotoAndStop('base')
            elif i in SCHEME_APPRECIATION:
                itemMc.detail.icon.gotoAndStop('appreciation')
            elif i in SCHEME_VIP:
                itemMc.detail.icon.gotoAndStop('privilege')
            itemMc.buyBtn.visible = i not in SCHEME_BASE
            itemMc.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBuyBtn, False, 0, True)
            itemMc.detail.nameInput.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
            itemMc.detail.nameInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleInputKeyUp, False, 0, True)

        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            for i in xrange(MAX_SCHEME_NUM):
                itemMc = getattr(self.widget, 'scheme%d' % i, None)
                if not itemMc:
                    continue
                if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                    schemeName = p.getWSSchemeName(i)
                elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                    schemeName = p.getEquipSoulSchemeName(i + EQUIP_SOUL_SCHEMENO_OFFSET)
                else:
                    schemeName = uiUtils.getDefaultSchemeName(self.panelType, i)
                itemMc.detail.nameInput.text = schemeName
                buyBtnLabel = ''
                timeTextValidTitle = ''
                timeTextValidPeriod = ''
                canRename = True
                canClickDetail = True
                if i in SCHEME_APPRECIATION:
                    if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                        expireTime = p.getWSSchemeExpireTime(i)
                    elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                        expireTime = p.getEquipSoulSchemeExpireTime(i + EQUIP_SOUL_SCHEMENO_OFFSET)
                    else:
                        expireTime = 0
                    if expireTime != 0:
                        buyBtnLabel = gameStrings.SCHEME_SWITCH_RENEWAL
                        if expireTime > utils.getNow():
                            timeTextValidTitle = gameStrings.SCHEME_SWITCH_TIME_LIMIT
                            timeTextValidPeriod = time.strftime('%Y.%m.%d  %H:%M', time.localtime(expireTime))
                        else:
                            timeTextValidTitle = gameStrings.SCHEME_SWITCH_TIME_OUT
                            canRename = False
                    else:
                        buyBtnLabel = gameStrings.SCHEME_SWITCH_BUY
                        canRename = False
                        canClickDetail = False
                elif i in SCHEME_VIP:
                    if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                        expireTime = p.getWSSchemeExpireTime(i)
                    elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                        expireTime = p.getEquipSoulSchemeExpireTime(i + EQUIP_SOUL_SCHEMENO_OFFSET)
                    else:
                        expireTime = 0
                    if expireTime != 0:
                        buyBtnLabel = gameStrings.SCHEME_SWITCH_RENEWAL
                        if expireTime > utils.getNow():
                            timeTextValidTitle = gameStrings.SCHEME_SWITCH_TIME_LIMIT_SP
                            timeTextValidPeriod = time.strftime('%Y.%m.%d  %H:%M', time.localtime(expireTime))
                        else:
                            timeTextValidTitle = gameStrings.SCHEME_SWITCH_TIME_OUT
                            canRename = False
                    else:
                        buyBtnLabel = gameStrings.SCHEME_SWITCH_BUY_SP
                        canRename = False
                        canClickDetail = False
                itemMc.buyBtn.label = buyBtnLabel
                itemMc.detail.timeText.validTitle.htmlText = timeTextValidTitle
                itemMc.detail.timeText.validPeriod.htmlText = timeTextValidPeriod
                itemMc.detail.nameInput.enabled = canRename
                itemMc.detail.enabled = canClickDetail
                if canClickDetail:
                    itemMc.detail.validateNow()
                    itemMc.detail.mouseChildren = True
                    itemMc.detail.addEventListener(events.MOUSE_CLICK, self.handleClickDetail, False, 0, True)
                else:
                    itemMc.detail.removeEventListener(events.MOUSE_CLICK, self.handleClickDetail)

            self.refreshDetail()
            return

    def handleClickDetail(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selected:
            return
        self.selectedSchemeNo = e.currentTarget.parent.schemeNo
        self.refreshDetail()

    def refreshDetail(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            for i in xrange(MAX_SCHEME_NUM):
                itemMc = getattr(self.widget, 'scheme%d' % i, None)
                if not itemMc:
                    continue
                itemMc.detail.selected = self.selectedSchemeNo == i

            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                self.widget.confirmBtn.enabled = self.selectedSchemeNo != p.getCurWSSchemeNo()
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                self.widget.confirmBtn.enabled = self.selectedSchemeNo != p.currEquipSoulSchemeNo - EQUIP_SOUL_SCHEMENO_OFFSET
            else:
                self.widget.confirmBtn.enabled = False
            return

    def handleClickBuyBtn(self, *args):
        e = ASObject(args[3][0])
        schemeNo = e.currentTarget.parent.schemeNo
        if schemeNo in SCHEME_APPRECIATION:
            if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
                self.uiAdapter.schemeResume.show(self.panelType, schemeNo)
            elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
                self.uiAdapter.schemeResume.show(self.panelType, schemeNo + EQUIP_SOUL_SCHEMENO_OFFSET)
            else:
                self.uiAdapter.schemeResume.show(self.panelType, schemeNo)
        elif schemeNo in SCHEME_VIP:
            self.uiAdapter.tianyuMall.showMallTab(10001, 0)

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
            expireTime = p.getWSSchemeExpireTime(self.selectedSchemeNo)
        elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
            expireTime = p.getEquipSoulSchemeExpireTime(self.selectedSchemeNo + EQUIP_SOUL_SCHEMENO_OFFSET)
        else:
            expireTime = 0
        if expireTime != 0 and expireTime < utils.getNow():
            msg = uiUtils.getTextFromGMD(GMDD.data.SCHEME_SWITCH_OVERDUE, '')
            self.uiAdapter.messageBox.showMsgBox(msg)
            return
        if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
            p.saveWSShortcut(self.uiAdapter.actionbar.getClientShortCut())
            p.cell.saveAndSwitchWSScheme(p.getCurWSSchemeNo(), self.selectedSchemeNo)
        elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
            p.base.switchEquipSoulScheme(self.selectedSchemeNo + EQUIP_SOUL_SCHEMENO_OFFSET)
        self.hide()

    def handleInputFocusOut(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        if e.currentTarget == e.target:
            return
        schemeNo = e.currentTarget.parent.parent.schemeNo
        p = BigWorld.player()
        if self.panelType == uiConst.SCHEME_SWITCH_WUSHUANG:
            if p.getWSSchemeName(schemeNo) != e.currentTarget.text:
                p.base.setWSSchemeName(schemeNo, e.currentTarget.text)
        elif self.panelType == uiConst.SCHEME_SWITCH_EQUIP_SOUL:
            if p.getEquipSoulSchemeName(schemeNo + EQUIP_SOUL_SCHEMENO_OFFSET) != e.currentTarget.text:
                p.base.updateEquipSoulSchemeName(schemeNo + EQUIP_SOUL_SCHEMENO_OFFSET, e.currentTarget.text)

    def handleInputKeyUp(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            e.currentTarget.stage.focus = None
            e.stopImmediatePropagation()
