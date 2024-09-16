#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/buffListenerIconSelectProxy.o
import cPickle
import zlib
import copy
import BigWorld
import const
import gameglobal
import uiConst
import events
from asObject import ASObject
from uiProxy import UIProxy
from data import conditional_prop_data as CPD
SLOT_NORMAL = 1
SLOT_SELECTED = 2

class BuffListenerIconSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BuffListenerIconSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BUFF_LISTENER_ICON_SELECT, self.hide)

    def reset(self):
        self.listenerType = 0
        self.listenerId = 0
        self.selectedIconId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BUFF_LISTENER_ICON_SELECT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BUFF_LISTENER_ICON_SELECT)

    def show(self, listenerType, listenerId):
        self.listenerType = listenerType
        self.listenerId = listenerId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BUFF_LISTENER_ICON_SELECT)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.iconList.column = 5
        self.widget.iconList.itemHeight = 50
        self.widget.iconList.itemWidth = 50
        self.widget.iconList.itemRenderer = 'BuffListenerIconSelect_Slot'
        self.widget.iconList.labelFunction = self.slotItemFunc
        self.widget.iconList.dataArray = []

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.iconList.dataArray = [ {'iconId': iconId} for iconId in uiConst.BUFF_LISTENER_ICON_IDS ]
        buffData = p.buffListenerConfig.get('buffConfig', {}).get(self.listenerType, {}).get(self.listenerId, {})
        if not self.selectedIconId:
            self.selectedIconId = buffData.get('icon', 0)
            if not self.selectedIconId:
                condPropData = CPD.data.get(self.listenerId, {})
                conPropType = condPropData.get('conPropType', 1)
                if conPropType == const.COND_PROP_TYPE_ATTACK:
                    self.selectedIconId = uiConst.BUFF_LISTENER_DEFAULT_ICON_1
                elif conPropType == const.COND_PROP_TYPE_DEFENSE:
                    self.selectedIconId = uiConst.BUFF_LISTENER_DEFAULT_ICON_2
            self.setSelectedIconId(self.selectedIconId)

    def slotItemFunc(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.iconId = info.iconId
            icon = info.iconId
            if not icon:
                if conPropType == const.COND_PROP_TYPE_ATTACK:
                    icon = uiConst.BUFF_LISTENER_DEFAULT_ICON_1
                elif conPropType == const.COND_PROP_TYPE_DEFENSE:
                    icon = uiConst.BUFF_LISTENER_DEFAULT_ICON_2
            iconPath = uiConst.MACRO_COMMON_ICON % icon
            itemData = {'iconPath': iconPath}
            itemMc.setItemSlotData(itemData)
            itemMc.dragable = False
            if self.selectedIconId == icon:
                itemMc.setSlotState(SLOT_SELECTED)
            else:
                itemMc.setSlotState(SLOT_NORMAL)
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleSlotItemClick, False, 0, True)

    def setSelectedIconId(self, iconId):
        if self.selectedIconId:
            selectedItem = self.getItemBySelectedIconId(self.selectedIconId)
            if selectedItem:
                selectedItem.setSlotState(SLOT_NORMAL)
            self.selectedIconId = None
        if iconId:
            self.selectedIconId = iconId
            selectedItem = self.getItemBySelectedIconId(self.selectedIconId)
            if selectedItem:
                selectedItem.setSlotState(SLOT_SELECTED)

    def getItemBySelectedIconId(self, iconId):
        items = self.widget.iconList.items
        for item in items:
            if item.iconId == iconId:
                return item

    def _onConfirmBtnClick(self, e):
        t = e.currentTarget
        p = BigWorld.player()
        buffListenerConfig = copy.deepcopy(p.buffListenerConfig)
        buffListenerConfig.setdefault('buffConfig', {})
        buffListenerConfig['buffConfig'].setdefault(self.listenerType, {})
        buffListenerConfig['buffConfig'][self.listenerType].setdefault(self.listenerId, {})
        buffListenerConfig['buffConfig'][self.listenerType][self.listenerId]['icon'] = self.selectedIconId
        serverData = self.packConfigData(buffListenerConfig)
        p.base.setStateMonitorClientConfig(serverData)
        self.hide()

    def packConfigData(self, data):
        return zlib.compress(cPickle.dumps(data))

    def handleSlotItemClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        iconId = t.iconId
        self.setSelectedIconId(iconId)
