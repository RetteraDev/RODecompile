#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTransferHintProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import school_transfer_hint_data as STHD
from cdata import game_msg_def_data as GMDD
MODE_NORMAL = 1
MODE_LOW_LV_FREE = 2

class SchoolTransferHintProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTransferHintProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TRANSFER_HINT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TRANSFER_HINT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_HINT)

    def reset(self):
        self.selectedSchool = const.SCHOOL_DEFAULT
        self.isLowLvFree = False

    def hide(self, destroy = True):
        super(SchoolTransferHintProxy, self).hide(destroy)
        if self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.close()

    def show(self, selectedSchool, isLowLvFree):
        if not gameglobal.rds.configData.get('enableSchoolTransfer', False):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SCHOOL_TRANSFER_DISABLED, ())
            return
        if isLowLvFree and not gameglobal.rds.configData.get('enableLowLvFreeSchoolTransfer', False):
            return
        self.selectedSchool = selectedSchool
        self.isLowLvFree = isLowLvFree
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_HINT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.checkBox.addEventListener(events.EVENT_SELECT, self.handleSelect, False, 0, True)
        if BigWorld.player().hasInvPassword and gameglobal.rds.configData.get('enableInventoryLock', False):
            self.widget.passwordInputTitle.visible = True
            self.widget.passwordInput.visible = True
            ASUtils.setHitTestDisable(self.widget.passwordInputTitle, True)
            self.widget.passwordInput.textField.restrict = 'a-zA-Z0-9'
            self.widget.passwordInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
            self.widget.passwordInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
        else:
            self.widget.passwordInputTitle.visible = False
            self.widget.passwordInput.visible = False
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.confirmBtn.enabled = False

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.removeAllInst(self.widget.scrollWnd.canvas)
        itemList = []
        for key, value in STHD.data.iteritems():
            showMode = value.get('showMode', 0)
            if showMode == MODE_NORMAL and self.isLowLvFree:
                continue
            elif showMode == MODE_LOW_LV_FREE and not self.isLowLvFree:
                continue
            itemList.append({'sortIdx': key,
             'desc': value.get('desc', '')})

        itemList.sort(key=lambda x: x['sortIdx'])
        posY = 0
        for i, itemInfo in enumerate(itemList):
            itemMc = self.widget.getInstByClsName('SchoolTransferHint_Item')
            itemMc.desc.htmlText = itemInfo.get('desc', '')
            itemMc.desc.height = itemMc.desc.textHeight + 5
            itemMc.bg.gotoAndStop('light' if i % 2 else 'dark')
            itemMc.bg.height = itemMc.desc.height + 16
            itemMc.y = posY
            posY += itemMc.height
            self.widget.scrollWnd.canvas.addChild(itemMc)

        self.widget.scrollWnd.refreshHeight()

    def handleSelect(self, *args):
        self.widget.confirmBtn.enabled = self.widget.checkBox.selected

    def handleInputFocusIn(self, *args):
        if not self.widget:
            return
        self.widget.passwordInputTitle.visible = False

    def handleInputFocusOut(self, *args):
        if not self.widget:
            return
        self.widget.passwordInputTitle.visible = self.widget.passwordInput.text == ''

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().cell.beginSchoolTransfer(self.selectedSchool, self.widget.passwordInput.text)
