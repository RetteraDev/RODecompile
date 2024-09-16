#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryPacketListProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_package_data as MPD
from data import marriage_config_data as MCD

class MarryPacketListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryPacketListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_PACKET_LIST, self.hide)

    def reset(self):
        self.marriageInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_PACKET_LIST:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_PACKET_LIST)

    def show(self, marriageInfo):
        self.marriageInfo = marriageInfo
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_PACKET_LIST)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.marriageList.itemRenderer = 'MarryPacketList_ListItem'
        self.widget.marriageList.lableFunction = self.listItemFunction
        self.widget.marriageList.itemHeight = 23
        self.widget.marriageList.itemWidth = 305
        self.widget.marriageList.dataArray = self.getListData()
        coin, count = self.getTotalCoinAndCount()
        self.widget.listTitleTxt.htmlText = gameStrings.MARRIAGE_PACKET_LIST_TITLE % (count,)
        self.widget.tianbiTxt.text = coin

    def refreshInfo(self):
        if not self.hasBaseData():
            return

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def listItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.roleNameTxt.text = info.roleName
            itemMc.numTxt.text = info.coin

    def getListData(self):
        dataArray = []
        for i, lData in enumerate(self.marriageInfo):
            roleName = lData.get('roleName', '')
            coin = lData.get('money', 0)
            info = {'roleName': roleName,
             'coin': coin}
            dataArray.append(info)

        return dataArray

    def getTotalCoinAndCount(self):
        p = BigWorld.player()
        totalCoin = 0
        totalCount = 0
        for i, lData in enumerate(self.marriageInfo):
            coin = lData.get('money', 0)
            moneyUnit = MCD.data.get('redPacketMoneyUnit', 0)
            count = coin / moneyUnit
            totalCount += count
            totalCoin += coin

        return (totalCoin, totalCount)
