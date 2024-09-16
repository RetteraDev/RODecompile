#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/multiCarrierNodeSelectProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from asObject import ASUtils
from asObject import ASObject
from gamestrings import gameStrings
from data import multi_carrier_data as MCD
NODE_POSITION_X = 9
NODE_POSITION_Y = 43
HEIGHT_OFFSET = 29

class MultiCarrierNodeSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MultiCarrierNodeSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MULTI_CARRIER_NODE_SELECT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MULTI_CARRIER_NODE_SELECT:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MULTI_CARRIER_NODE_SELECT)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MULTI_CARRIER_NODE_SELECT)
        self.widget = None

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            p = BigWorld.player()
            carrierInfo = p.carrier
            if p.id in carrierInfo:
                self.hide()
                return
            self.widget.removeAllInst(self.widget.canvas)
            cData = MCD.data.get(p.carrier.carrierNo, {})
            seatName = cData.get('seatName', [])
            seatInfo = {}
            for k, v in carrierInfo.iteritems():
                seatInfo[v] = k

            for i, name in enumerate(seatName):
                item = self.widget.getInstByClsName('MultiCarrierNodeSelect_LocationBtn')
                if item:
                    if seatInfo.get(i + 1, None):
                        item.enabled = False
                    else:
                        item.enabled = True
                    item.label = name
                    item.y = i * HEIGHT_OFFSET
                    item.nodeIdx = i
                    self.widget.canvas.addChild(item)
                    item.addEventListener(events.BUTTON_CLICK, self.handleClickSelectNode, False, 0, True)
                self.widget.bg.height = NODE_POSITION_Y + (i + 1) * HEIGHT_OFFSET

        else:
            self.hide()

    def handleClickSelectNode(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        gamelog.debug('@zq handleClickSelectNode', t.nodeIdx)
        BigWorld.player().cell.applyEnterCarrierByIdx(t.nodeIdx + 1)

    def hasBaseData(self):
        p = BigWorld.player()
        if self.widget and p.carrier.carrierState in (gametypes.MULTI_CARRIER_STATE_RUNNING,):
            return True
        else:
            return False
