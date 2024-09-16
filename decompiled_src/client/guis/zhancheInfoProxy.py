#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhancheInfoProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASUtils
from asObject import ASObject
from data import guild_config_data as GCD
from data import zaiju_data as ZD

class ZhancheInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZhancheInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.infoList = []
        self.zhancheList = []
        self.useNumber = 0
        self.totalNumber = 0
        self.version = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHANCHE_LIST, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZHANCHE_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZHANCHE_LIST)

    def show(self):
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZHANCHE_LIST)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.zhancheMc.zhancheList.itemRenderer = 'ZhancheInfo_ZhancheItem'
        self.widget.zhancheMc.zhancheList.lableFunction = self.itemFunction
        self.widget.zhancheMc.zhancheList.itemHeight = 30

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        ASUtils.setMcData(itemMc, 'data', itemData)
        itemMc.zaijuNo.text = itemData.zaijuNo
        itemMc.descName.text = itemData.descName

    def updateItem(self, itemMc):
        if not itemMc:
            return
        itemMc.zaijuNo.text = 1
        itemMc.descName.text = 1

    def getItemInfo(self):
        p = BigWorld.player()
        if not self.version:
            self.version = 0
        p.cell.getGuildZaijuUsedList(self.version)

    def setItemInfo(self, data):
        version = data[0]
        if self.version != version:
            self.version = version
            self.zhancheList = data[1]
        self.getzhancheNumber()
        if not self.widget:
            return

    def refreshInfo(self):
        self.getItemInfo()
        self.infoList = []
        for i in xrange(len(self.zhancheList)):
            zhancheInfo = {}
            zaijuId = self.zhancheList[i][0]
            zhancheInfo['zaijuNo'] = ZD.data.get(zaijuId, {}).get('name', '')
            zhancheInfo['descName'] = self.zhancheList[i][1]
            self.infoList.append(zhancheInfo)

        self.getzhancheNumber()
        if not self.widget:
            return
        self.widget.zhancheMc.zhancheList.dataArray = self.infoList

    def getzhancheNumber(self):
        self.useNumber = len(self.zhancheList)
        self.totalNumber = GCD.data.get('GUILD_EMPTY_ZAIJU_USED_LIMIT', 0)
        gameglobal.rds.ui.clanWar.updateZhancheNum(self.useNumber, self.totalNumber)
        return (self.useNumber, self.totalNumber)
