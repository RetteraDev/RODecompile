#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wardrobeDyeProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import utils
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD

class WardrobeDyeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WardrobeDyeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.item = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WARDROBE_DYE, self.close)
        self.addEvent(events.EVENT_ITEM_DYE_SCHEME_CHANGED, self.refreshDyeScheme, isGlobal=True)

    def close(self):
        if gameglobal.rds.ui.dyePlane.isShow:
            gameglobal.rds.ui.dyePlane.close()
            return
        self.hide()

    def reset(self):
        self.item = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WARDROBE_DYE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WARDROBE_DYE)

    def show(self, item = None):
        if not gameglobal.rds.configData.get('enableWardrobeMultiDyeScheme', False):
            return
        if item:
            if not item.isCanDye():
                return
        else:
            return
        self.item = item
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WARDROBE_DYE, True)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WARDROBE_DYE)
        else:
            self.refreshInfo()

    def onCloseBtnClick(self, *args):
        self.close()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick, False, 0, True)
        self.widget.dyeList.itemRenderer = 'WardrobeDye_dyeItem'
        self.widget.dyeList.labelFunction = self.dyeListLabelFunc

    def refreshDyeScheme(self, param):
        item = param.data
        if item.uuid == self.item.uuid:
            self.item = item
            if not self.widget:
                self.show(item)
            else:
                self.refreshInfo()
            gameglobal.rds.ui.dyePlane.setEquip(0, 0, item, const.RES_KIND_WARDROBE_BAG)

    def dyeListLabelFunc(self, *args):
        dyeData = ASObject(args[3][0])
        dyeMc = ASObject(args[3][1])
        dyeMc.bgBtn.selected = self.item.dyeCurrIdx == dyeData.idx
        if dyeData.idx == -1:
            dyeMc.expandIdx = dyeData.expandIdx
            dyeMc.bgBtn.label = ''
            dyeMc.rongGuangTxt.visible = True
            dyeMc.rongGuangTxt.text = dyeData.label
            dyeMc.addMc.visible = True
        else:
            dyeMc.bgBtn.label = dyeData.label
            dyeMc.rongGuangTxt.visible = False
            dyeMc.addMc.visible = False
        dyeMc.idx = dyeData.idx
        dyeMc.addEventListener(events.MOUSE_CLICK, self.onDyeListItemClick, False, 0, True)

    def onDyeListItemClick(self, *args):
        e = ASObject(args[3][0])
        schemeIdx = e.currentTarget.idx
        p = BigWorld.player()
        if schemeIdx == -1:
            expandIdx = e.currentTarget.expandIdx
            self.openExpandWnd(expandIdx)
            return
        wearPart = p.getWardrobeItemWearPart(self.item.uuid)
        if wearPart == -1:
            p.base.requireSwitchItemDyeScheme(const.RES_KIND_WARDROBE_BAG, 0, self.item.uuid, schemeIdx)
        else:
            p.base.requireSwitchItemDyeScheme(const.RES_KIND_EQUIP, 0, str(wearPart), schemeIdx)

    def openExpandWnd(self, idx):
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_WARDROBE_DYE_EXPAND, idx, {'uuid': self.item.uuid})

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.dyeList.dataArray = gameglobal.rds.ui.dyeList.getSchemInfoArray(self.item, True)
        rongGuangTxt = self.getRongGuangTxt(self.item)
        if not rongGuangTxt:
            self.widget.rongGuangTxt.visible = False
        else:
            self.widget.rongGuangTxt.visible = True
            self.widget.rongGuangTxt.text = rongGuangTxt

    def getRongGuangTxt(self, i):
        dyeTTLExpireTime = ''
        now = utils.getNow()
        if hasattr(i, 'rongGuangExpireTime') and i.rongGuangExpireTime and now < i.rongGuangExpireTime:
            if dyeTTLExpireTime:
                dyeTTLExpireTime += '\n'
            str = utils.formatDuration(i.rongGuangExpireTime - now)
            dyeTTLExpireTime += gameStrings.DYELIST_RONGGUANG + str
        return dyeTTLExpireTime
