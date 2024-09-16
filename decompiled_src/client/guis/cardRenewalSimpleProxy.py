#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardRenewalSimpleProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from gamestrings import gameStrings
RIGHT_SCALE_RATIO = 1.3
CUR_CANVAS_POS_OFFSET = (10, 6)
OTHER_CANVAS_POS_OFFSET = (2, -3)

class CardRenewalSimpleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardRenewalSimpleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_RENEWAL_SIMPLE, self.hide)

    def reset(self):
        super(CardRenewalSimpleProxy, self).reset()
        self.curCardId = 0
        self.durationDay = 0
        self.itemIds = 0
        self.itemNums = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_RENEWAL_SIMPLE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_RENEWAL_SIMPLE)

    def show(self, cardId, durationDay, itemIds, itemNums):
        if not self.widget:
            self.curCardId = cardId
            self.durationDay = durationDay
            self.itemIds = itemIds
            self.itemNums = itemNums
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_RENEWAL_SIMPLE, True)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.delayTxt.text = gameStrings.CARD_RENEWAL_TIME_TXT % (self.durationDay,)
        self.setCardCanvas(self.curCardId, self.widget.cardCanvas, (13, 3), RIGHT_SCALE_RATIO)

    def refreshInfo(self):
        if not self.widget:
            return

    def setCardCanvas(self, cardId, canvas, pos, scale):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        self.widget.removeAllInst(canvas)
        cardMc = self.widget.getInstByClsName('CardSystem_CardContainer')
        cardMc.x, cardMc.y = pos
        cardMc.scaleX = scale
        cardMc.scaleY = scale
        cardObj = p.getCard(cardId)
        if cardMc and cardObj:
            self.uiAdapter.cardRenewalDetail.setCard(cardMc, cardObj, False)
            canvas.addChild(cardMc)

    def _onConfirmBtnClick(self, e):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        p.base.renewalCardWithItem(self.curCardId, self.itemIds, self.itemNums, [])
        self.hide()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
