#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossClanWarRewardProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
from guis import uiUtils
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import sys_config_data as SCD
SLOT_MAX_CNT = 12
from data import cross_clan_war_config_data as CCWCD

class CrossClanWarRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossClanWarRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_CLAN_WAR_REWARD, self.hide)

    def reset(self):
        self.infoList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_CLAN_WAR_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_REWARD)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction
        self.widget.scrollWndList.itemRenderer = 'CrossClanWarReward_ItemRender'

    def labelFunction(self, *args):
        index = int(args[3][0].GetNumber())
        mc = ASObject(args[3][1])
        if index < len(self.infoList):
            title = self.infoList[index][0]
            mc.txtTitle.text = title
            itemList = self.infoList[index][1:]
            for i in xrange(SLOT_MAX_CNT):
                slotMc = getattr(mc, 'item%d' % i)
                if i < len(itemList):
                    slotMc.visible = True
                    slotMc.dragable = False
                    slotMc.setItemSlotData(uiUtils.getGfxItemById(*itemList[i]))
                else:
                    slotMc.visible = False

    def itemHeightFunction(self, *args):
        index = int(args[3][0].GetNumber())
        if index < len(self.infoList):
            if len(self.infoList[index][1:]) <= SLOT_MAX_CNT / 2:
                return GfxValue(87)
            else:
                return GfxValue(145)
        else:
            return GfxValue(145)

    def refreshInfo(self):
        if not self.widget:
            return
        self.infoList = CCWCD.data.get('crossClanWarReward', ())
        self.widget.scrollWndList.dataArray = range(len(self.infoList))
