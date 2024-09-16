#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpPlayoffs5v5FudaiProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
from data import personal_zone_bonus_data as PZBD

class PvpPlayoffs5v5FudaiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpPlayoffs5v5FudaiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FUDAI, self.hide)

    def reset(self):
        self.prevVal = 0
        self.upLimit = PZBD.data.get(5, {}).get('maxNum', 999)
        self.lowerLimit = 0
        self.cashNeed = 0
        self.coinNeed = 0
        self.tag = 5
        self.fudaiNumber = 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_PLAYOFFS_5V5_FUDAI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FUDAI)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FUDAI)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.fuDaiNumberText.text = 1
        self.widget.helpBtn.helpKey = 413
        self.widget.nextBtn.addEventListener(events.MOUSE_CLICK, self.onAdd, False, 0, True)
        self.widget.prevBtn.addEventListener(events.MOUSE_CLICK, self.onMinus, False, 0, True)
        self.widget.giftBlue.addEventListener(events.MOUSE_CLICK, self.giftChange, False, 0, True)
        self.widget.giftPurple.addEventListener(events.MOUSE_CLICK, self.giftChange, False, 0, True)
        self.widget.giftGlod.addEventListener(events.MOUSE_CLICK, self.giftChange, False, 0, True)
        self.widget.okBtn.addEventListener(events.MOUSE_CLICK, self.setFudai, False, 0, True)
        TipManager.addTip(self.widget.giftBlue, PZBD.data.get(4, {}).get('tips', ''))
        TipManager.addTip(self.widget.giftPurple, PZBD.data.get(5, {}).get('tips', ''))
        TipManager.addTip(self.widget.giftGlod, PZBD.data.get(6, {}).get('tips', ''))
        self.widget.fuDaiNumberText.addEventListener(events.EVENT_CHANGE, self.onValChange, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.totlePayChange()
        self.btnChange()

    def giftChange(self, *args):
        e = ASObject(args[3][0])
        target = e.target
        if target == self.widget.giftBlue:
            self.tag = 4
            self.refreshTarget()
        elif target == self.widget.giftPurple:
            self.tag = 5
            self.refreshTarget()
        elif target == self.widget.giftGlod:
            self.tag = 6
            self.refreshTarget()
        self.totlePayChange()
        self.btnChange()

    def refreshTarget(self):
        self.upLimit = PZBD.data.get(self.tag, {}).get('maxNum', 999)
        self.cashNeed = PZBD.data.get(self.tag, {}).get('cashNeed', 0)
        self.coinNeed = PZBD.data.get(self.tag, {}).get('coinNeed', 0)

    def onAdd(self, *args):
        originalVal = 0
        if not self.widget.fuDaiNumberText.text == '':
            originalVal = int(self.widget.fuDaiNumberText.text)
        if originalVal >= self.upLimit - 1:
            self.widget.fuDaiNumberText.text = self.upLimit
            self.fudaiNumber = self.upLimit
        else:
            self.widget.fuDaiNumberText.text = originalVal + 1
            self.fudaiNumber = originalVal + 1
        self.totlePayChange()
        self.btnChange()

    def onMinus(self, *args):
        originalVal = int(self.widget.fuDaiNumberText.text)
        if originalVal <= self.lowerLimit + 1:
            self.widget.fuDaiNumberText.text = self.lowerLimit
            self.fudaiNumber = self.lowerLimit
        else:
            self.widget.fuDaiNumberText.text = originalVal - 1
            self.fudaiNumber = originalVal - 1
        self.totlePayChange()
        self.btnChange()

    def onValChange(self, *args):
        if self.widget.fuDaiNumberText.text.isdigit():
            self.prevVal = int(self.widget.fuDaiNumberText.text)
            self.fudaiNumber = self.prevVal
        elif self.widget.fuDaiNumberText.text == '':
            self.prevVal = ''
            self.fudaiNumber = 0
        self.widget.fuDaiNumberText.text = self.prevVal
        if self.prevVal != '' and self.prevVal >= self.upLimit:
            self.widget.fuDaiNumberText.text = self.upLimit
            self.fudaiNumber = self.upLimit
        self.totlePayChange()
        self.btnChange()

    def btnChange(self):
        self.widget.prevBtn.disabled = False
        self.widget.nextBtn.disabled = False
        self.widget.okBtn.disabled = False
        if self.widget.fuDaiNumberText.text.isdigit():
            fuDaiNumberVal = int(self.widget.fuDaiNumberText.text)
        else:
            fuDaiNumberVal = 0
        if fuDaiNumberVal >= self.upLimit:
            self.widget.nextBtn.disabled = True
        elif fuDaiNumberVal <= self.lowerLimit:
            self.widget.prevBtn.disabled = True
            self.widget.okBtn.disabled = True
        totlePay, owned = self.widget.totlePay.text.split('/')
        if int(totlePay) > int(owned):
            self.widget.okBtn.disabled = True

    def totlePayChange(self):
        p = BigWorld.player()
        itemPrice = max(PZBD.data.get(self.tag, {}).get('cashNeed', 0), PZBD.data.get(self.tag, {}).get('coinNeed', 0))
        owned = 0
        totlePay = 0
        if PZBD.data.get(self.tag, {}).get('coinNeed', 0) != 0:
            self.widget.coinIcon.gotoAndPlay('tianBi')
            owned = p.getTianBi()
        else:
            self.widget.coinIcon.gotoAndPlay('cash')
            owned = p.cash
        if self.widget.fuDaiNumberText.text.isdigit():
            totlePay = itemPrice * int(self.widget.fuDaiNumberText.text)
        self.widget.totlePay.text = str(totlePay) + '/' + str(owned)

    def setFudai(self, *args):
        if self.widget.okBtn.disabled == True:
            return
        if not self.widget.fuDaiNumberText.text.isdigit():
            return
        itemPrice = max(PZBD.data.get(self.tag, {}).get('cashNeed', 0), PZBD.data.get(self.tag, {}).get('coinNeed', 0))
        totalPay = itemPrice * int(self.widget.fuDaiNumberText.text)
        if self.tag == 6:
            msg = gameStrings.PVP_PLAYOFFS_5V5_FUDAI_CONFIRM % totalPay
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmBuyAllPreviewItems, self.tag, self.fudaiNumber))
        else:
            self.confirmBuyAllPreviewItems(self.tag, self.fudaiNumber)

    def confirmBuyAllPreviewItems(self, tag, number):
        p = BigWorld.player()
        p.cell.addArenaPlayoffsVoteLuckyBag(tag, number)

    def onSetFudaiSucess(self):
        gameglobal.rds.ui.pvpPlayoffs5v5Vote.refreshInfo()
        self.hide()
