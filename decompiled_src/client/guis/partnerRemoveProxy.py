#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/partnerRemoveProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import utils
import commQuest
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor

class PartnerRemoveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PartnerRemoveProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PARTNER_REMOVE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PARTNER_REMOVE:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PARTNER_REMOVE)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PARTNER_REMOVE)
        self.widget = None
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.partnerArr = []
        self.curSelectedItem = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            p = BigWorld.player()
            self.partnerArr = []
            for gbId, info in p.partner.iteritems():
                if gbId not in p.members:
                    info['gbId'] = gbId
                    self.partnerArr.append(info)

            for x in xrange(0, const.PARTNER_MAX_NUM - 1):
                nameItem = getattr(self.widget, 'name' + str(x), None)
                nameItem.index = x
                if nameItem:
                    if x < len(self.partnerArr):
                        nameItem.visible = True
                        nameItem.label = gameStrings.PARTNER_REMOVE_NAME_ITEM % (self.partnerArr[x]['level'], self.partnerArr[x]['roleName'])
                    else:
                        nameItem.visible = False
                nameItem.addEventListener(events.BUTTON_CLICK, self.handleClickNameBtn, False, 0, True)

            self.setSelected(0)

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def handleClickNameBtn(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        self.setSelected(t.index)

    def setSelected(self, index):
        if self.curSelectedItem:
            self.curSelectedItem.selected = False
        nameItem = getattr(self.widget, 'name' + str(index), None)
        self.curSelectedItem = nameItem
        self.curSelectedItem.selected = True

    def getCurSelectedIndex(self):
        if self.curSelectedItem:
            return self.curSelectedItem.index
        else:
            return None

    def _onConfirmBtnClick(self, e):
        index = self.getCurSelectedIndex()
        if index != None and self.partnerArr and index < len(self.partnerArr):
            gbId = self.partnerArr[index].get('gbId', 0)
            if gbId:
                p = BigWorld.player()
                p.cell.comfirmChooseKickoutPartner(gbId)
