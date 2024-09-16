#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/descriptionWithBuffProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import events
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import state_data as SD
BUFF_WIDTH = 61
BUFF_HEIGHT = 54
MAX_SLOT_NUM_PER_LINE = 6

class DescriptionWithBuffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DescriptionWithBuffProxy, self).__init__(uiAdapter)
        self.widget = None
        self.yesCallBack = None
        self.cancelCallBack = None
        self.title = ''
        self.msg = ''
        self.buffIds = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_DESCRIPT_BUFF, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DESCRIPT_BUFF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DESCRIPT_BUFF)

    def show(self, title, msg, buffIds, yesCallBack = None, cancelCallBack = None):
        self.title = title
        self.msg = msg
        self.buffIds = buffIds
        self.yesCallBack = yesCallBack
        self.cancelCallBack = cancelCallBack
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_DESCRIPT_BUFF)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.title.textField.text = self.title
        self.widget.main.tip.htmlText = self.msg
        self.widget.main.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)
        self.widget.main.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.removeAllChild(self.widget.main.slotArea)
        for index, buffId in enumerate(self.buffIds):
            itemMc = self.widget.getInstByClsName('DescriptionWithBuff_buffIcon')
            self.widget.main.slotArea.addChild(itemMc)
            rowNum = index / MAX_SLOT_NUM_PER_LINE
            colNum = index - rowNum * MAX_SLOT_NUM_PER_LINE
            itemMc.x = colNum * BUFF_WIDTH
            itemMc.y = rowNum * BUFF_HEIGHT
            self.setBuffIcon(itemMc, buffId)

    def setBuffIcon(self, slot, buffId):
        cfg = SD.data.get(buffId, {})
        iconId = cfg.get('iconId', 'notFound')
        iconPath = 'state/40/%s.dds' % iconId
        slot.fitSize = True
        slot.dragable = False
        slot.loadImage(iconPath)
        buffText = cfg.get('desc', '')
        TipManager.addTip(slot, buffText)

    def onConfirmBtnClick(self, *args):
        if self.yesCallBack:
            self.yesCallBack()
        self.hide()

    def onCancelBtnClick(self, *args):
        if self.cancelCallBack:
            self.cancelCallBack()
        self.hide()
