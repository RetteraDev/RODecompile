#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tabAuctionCrossServerRegionProxy.o
import copy
import sys
import time
import BigWorld
import gameglobal
import gamelog
import events
from ui import gbk2unicode
from ui import unicode2gbk
from asObject import ASObject
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from gameStrings import gameStrings
from guis.asObject import ASUtils
from data import region_server_config_data as RSCD
from cdata import coin_consign_config_Data as CCCD
SERVERSTATES = ['kongxian',
 'lianghao',
 'fanmang',
 'baoman',
 'weihu']
WEIHU_FLAG = 4
CONST_POS_Y = 59
PER_ROW_NUM = 4
REGION_OFFSET_X = 92
REGION_OFFSET_Y = 25

class TabAuctionCrossServerRegionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TabAuctionCrossServerRegionProxy, self).__init__(uiAdapter)
        self.widget = None
        self.serverRegionId = None
        self.allServerRegionInfo = {}
        self.xConsignRegionIds = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_AUCTION_REGION, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TAB_AUCTION_REGION:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_AUCTION_REGION)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_AUCTION_REGION)

    def reset(self):
        self.serverRegionId = None
        self.allServerRegionInfo = {}
        self.xConsignRegionIds = []

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.genServerInfo()

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.selfRadioBtn.groupName = 'myRadio'
        self.widget.selfRadioBtn.tagStr = 'self'
        self.widget.selfRadioBtn.addEventListener(events.EVENT_SELECT, self.handleRadioBtnSelect, False, 0, True)
        self.widget.serverList.itemRenderer = 'TabAuctionCrossServerRegion_ServerItem'
        self.widget.serverList.barAlwaysVisible = True
        self.widget.serverList.column = 2
        self.widget.serverList.itemHeight = 45
        self.widget.serverList.itemWidth = 178
        self.widget.serverList.dataArray = []
        self.widget.serverList.lableFunction = self.itemFunction
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            allHeight = 0
            allHeight += self.widget.title.y + 52
            self.widget.removeAllInst(self.widget.serverList.canvas)
            nameDict = self.getNameDict()
            if self.serverRegionId and nameDict.get(self.serverRegionId, ''):
                self.widget.selfRadioBtn.visible = True
                self.widget.selfRadioBtn.label = gameStrings.AUCTION_CROSS_SERVER_REGION % nameDict.get(self.serverRegionId, '')
                allHeight += self.widget.selfRadioBtn.height
            else:
                self.widget.selfRadioBtn.visible = False
            if not self.widget.selfRadioBtn.visible:
                self.widget.regionMc.y = allHeight
            self.widget.removeAllInst(self.widget.regionMc)
            for i, rId in enumerate(self.xConsignRegionIds):
                radioBtn = self.widget.getInstByClsName('M12_DefaultRadioButton')
                radioBtn.x = i % PER_ROW_NUM * REGION_OFFSET_X
                radioBtn.y = int(i / PER_ROW_NUM) * REGION_OFFSET_Y
                radioBtn.name = 'radioBtn' + str(i)
                radioBtn.width = 116
                radioBtn.visible = True
                self.widget.regionMc.addChild(radioBtn)

            allHeight += self.widget.regionMc.height + 5
            for i in xrange(sys.maxint):
                radioBtn = self.widget.regionMc.getChildByName('radioBtn' + str(i))
                if radioBtn == None:
                    break
                if i < len(self.xConsignRegionIds):
                    radioBtn.label = nameDict.get(self.xConsignRegionIds[i], '')
                else:
                    radioBtn.visible = False
                self.widget.selfRadioBtn.group.addButton(radioBtn)
                radioBtn.tagStr = 'other'
                radioBtn.idx = i
                radioBtn.addEventListener(events.EVENT_SELECT, self.handleRadioBtnSelect, False, 0, True)

            self.widget.serverList.y = allHeight
            self.widget.innerBg.y = allHeight
            allHeight += self.widget.serverList.height + 30
            self.widget.BG.height = allHeight
            self.setInitSelected()

    def hasBaseData(self):
        if self.widget:
            return True
        return False

    def setInitSelected(self):
        if self.serverRegionId:
            self.widget.selfRadioBtn.selected = True
        else:
            radioBtn = self.widget.regionMc.getChildByName('radioBtn0')
            radioBtn.selected = True

    def getNameDict(self):
        return CCCD.data.get('crossConsignRegionName', {})

    def handleRadioBtnSelect(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.tagStr == 'self':
            self.widget.serverList.dataArray = copy.deepcopy(self.allServerRegionInfo.get(self.serverRegionId, []))
        elif target.tagStr == 'other':
            if int(target.idx) < len(self.xConsignRegionIds):
                self.widget.serverList.dataArray = copy.deepcopy(self.allServerRegionInfo.get(self.xConsignRegionIds[int(target.idx)], []))

    def genServerInfo(self):
        self.allServerRegionInfo = {}
        self.xConsignRegionIds = []
        rData = RSCD.data
        for k, v in rData.iteritems():
            xConsignRegionId = v.get('xConsignRegionId', 0)
            nameDict = self.getNameDict()
            if xConsignRegionId and nameDict.get(xConsignRegionId, ''):
                if k == int(gameglobal.rds.g_serverid):
                    self.serverRegionId = xConsignRegionId
                    if xConsignRegionId in self.xConsignRegionIds:
                        self.xConsignRegionIds.remove(xConsignRegionId)
                elif xConsignRegionId not in self.xConsignRegionIds and xConsignRegionId != self.serverRegionId:
                    self.xConsignRegionIds.append(xConsignRegionId)
                self.allServerRegionInfo.setdefault(xConsignRegionId, [])
                serverName = v.get('serverName', '')
                busy = self.getServerBusyState(serverName)
                self.allServerRegionInfo[xConsignRegionId].append((k, serverName, busy))

        self.xConsignRegionIds.sort()

    def getServerBusyState(self, serverName):
        for k, v in gameglobal.rds.loginManager.srvDict.item.iteritems():
            for item in v:
                if item.title == serverName:
                    return item.busy

    def itemFunction(self, *args):
        data = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        serverId = data[0]
        serverName = data[1]
        busy = data[2] if data[2] != None else 0
        flag = min(max(int(busy) - 1, 0), len(SERVERSTATES) - 1)
        if flag == WEIHU_FLAG:
            itemMc.stateIcon.gotoAndStop('weihu')
            serverName = uiUtils.toHtml(serverName, '#808080')
        else:
            itemMc.stateIcon.gotoAndStop(SERVERSTATES[flag])
            serverName = uiUtils.toHtml(serverName, '#FFFFE5')
        itemMc.nameTxt.htmlText = serverName
