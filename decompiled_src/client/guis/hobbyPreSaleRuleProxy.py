#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hobbyPreSaleRuleProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
from uiProxy import UIProxy
from guis.asObject import ASUtils
from gameStrings import gameStrings
from data import hobby_presale_rule_data as HPRD
from data import hobby_presale_config_data as HPCD

class HobbyPreSaleRuleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HobbyPreSaleRuleProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOBBY_PRESALE_RULE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HOBBY_PRESALE_RULE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOBBY_PRESALE_RULE)

    def reset(self):
        pass

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_HOBBY_PRESALE_RULE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.checkBox.addEventListener(events.EVENT_SELECT, self.handleSelect, False, 0, True)
        if BigWorld.player().hasInvPassword and gameglobal.rds.configData.get('enableInventoryLock', False):
            ASUtils.setHitTestDisable(self.widget.passwordInputTitle, True)
            self.widget.passwordInputTitle.visible = True
            self.widget.passwordInput.visible = True
            self.widget.passwordInput.textField.restrict = 'a-zA-Z0-9'
            self.widget.passwordInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
            self.widget.passwordInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
        else:
            self.widget.passwordInputTitle.visible = False
            self.widget.passwordInput.visible = False
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.confirmBtn.enabled = False
        bFlag = False
        nowTime = utils.getNow()
        timeList = HPCD.data.get('presaleTimeCfg', {})
        for batch in timeList:
            beginTime = timeList[batch][0]
            endTime = timeList[batch][1]
            if nowTime >= utils.getTimeSecondFromStr(beginTime) and nowTime <= utils.getTimeSecondFromStr(endTime):
                bFlag = True
                break

        if bFlag:
            self.widget.confirmBtn.label = gameStrings.HOBBY_PRESALE_RULE_SURE
            self.widget.checkBox.enabled = True
        else:
            self.widget.confirmBtn.label = gameStrings.HOBBY_PRESALE_NOT_BEGIN
            self.widget.checkBox.enabled = False

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.removeAllInst(self.widget.scrollWnd.canvas)
        itemList = []
        for key, value in HPRD.data.iteritems():
            itemList.append({'sortIdx': key,
             'desc': value.get('desc', '')})

        itemList.sort(key=lambda x: x['sortIdx'])
        posY = 0
        for i, itemInfo in enumerate(itemList):
            itemMc = self.widget.getInstByClsName('HobbyPreSaleRule_Item')
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
        p = BigWorld.player()
        lvLimit = HPCD.data.get('lvLimit', 0)
        if p.lv < lvLimit:
            msg = gameStrings.HOBBY_PRESALE_LESS_LEVEL % lvLimit
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            self.hide()
        else:
            cipher = self.widget.passwordInput.text
            opType = 1
            p.base.queryExternalMallDataWithCipher(opType, cipher)
