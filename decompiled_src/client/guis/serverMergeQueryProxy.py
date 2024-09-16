#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/serverMergeQueryProxy.o
import BigWorld
import uiConst
import events
import gameglobal
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from cdata import region_server_name_data as RSND
from cdata import region_name_to_hostId as RNTH

class ServerMergeQueryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ServerMergeQueryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectZone = ''
        self.selectServerName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_SERVER_MERGE_QUERY, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SERVER_MERGE_QUERY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SERVER_MERGE_QUERY)

    def reset(self):
        self.selectZone = ''
        self.selectServerName = ''

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SERVER_MERGE_QUERY, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.regionDropdown.addEventListener(events.INDEX_CHANGE, self.handleRegionDropdwon, False, 0, True)
        self.widget.serverDropdown.addEventListener(events.INDEX_CHANGE, self.handleServerDropdwon, False, 0, True)
        self.widget.gotoGame.addEventListener(events.BUTTON_CLICK, self.handleGotoGameBtnClick, False, 0, True)
        self.widget.regionText.visible = True
        self.widget.serverText.visible = True
        ASUtils.setHitTestDisable(self.widget.regionText, True)
        ASUtils.setHitTestDisable(self.widget.serverText, True)
        self.updateGotoGameBtnState()

    def refreshInfo(self):
        if not self.widget:
            return
        allServerIds = []
        self.typeList = []
        for i, regionName in enumerate(RNTH.data):
            serverIds = RNTH.data.get(regionName, [])
            allServerIds += serverIds
            typeInfo = {}
            typeInfo['label'] = regionName
            typeInfo['serverIds'] = serverIds
            typeInfo['typeIndex'] = i
            self.typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.regionDropdown, self.typeList)
        self.widget.regionDropdown.menuRowCount = 4
        self.updateServerDropdown(allServerIds)

    def updateServerDropdown(self, serverIds):
        self.serverTypeList = []
        for serverId in serverIds:
            serverName = RSND.data.get(serverId, {}).get('serverName', '')
            serverTypeInfo = {}
            serverTypeInfo['label'] = serverName
            serverTypeInfo['serverId'] = serverId
            self.serverTypeList.append(serverTypeInfo)

        ASUtils.setDropdownMenuData(self.widget.serverDropdown, self.serverTypeList)
        self.widget.serverDropdown.menuRowCount = 4

    def handleRegionDropdwon(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.widget.regionText.visible = False
        self.widget.serverText.visible = True
        self.widget.serverDropdown.selectedIndex = -1
        self.selectServerName = ''
        itemInfo = self.typeList[itemMc.selectedIndex]
        serverIds = itemInfo.get('serverIds', [])
        self.updateServerDropdown(serverIds)
        self.updateGotoGameBtnState()
        self.widget.regionNameMc.textField.text = ''
        self.widget.serverNameMc.textField.text = ''

    def handleServerDropdwon(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.widget.regionText.visible = False
        self.widget.serverText.visible = False
        itemInfo = self.serverTypeList[itemMc.selectedIndex]
        serverId = itemInfo.get('serverId', 0)
        if self.widget.regionDropdown.selectedIndex == -1:
            regionTypeIndex = self.getRegionDropIndex(serverId)
            self.widget.regionDropdown.selectedIndex = regionTypeIndex
        self.updateCurRegionAndServer(serverId)

    def handleGotoGameBtnClick(self, *args):
        selZone = self.selectZone
        selIdx = self.getServerIdIndex()
        selServerIdx = self.getServerIdIndex()
        tmpVenderIdx = 0
        gameglobal.rds.ui.loginSelectServer.clickSelectServer(selZone, selIdx, selServerIdx, tmpVenderIdx)

    def getServerIdIndex(self):
        if not self.selectServerName:
            return -1
        srvDict = gameglobal.rds.loginManager.srvDict
        if srvDict:
            for i, key in enumerate(srvDict.keys):
                if key == self.selectZone:
                    for j, v in enumerate(srvDict.item.get(key)):
                        if v.name == self.selectServerName:
                            return j

        return 0

    def getRegionDropIndex(self, serverId):
        regionName = RSND.data.get(serverId, {}).get('regionName', '')
        for info in self.typeList:
            if info.get('label', '') == regionName:
                return info.get('typeIndex', 0)

        return 0

    def updateCurRegionAndServer(self, serverId = 0):
        currentHostId = RSND.data.get(serverId, {}).get('currentHostId', 0)
        serverName = RSND.data.get(currentHostId, {}).get('serverName', '')
        regionName = RSND.data.get(currentHostId, {}).get('regionName', '')
        self.selectServerName = serverName
        self.selectZone = regionName
        self.widget.regionNameMc.textField.text = regionName
        self.widget.serverNameMc.textField.text = serverName
        self.updateGotoGameBtnState()

    def updateGotoGameBtnState(self):
        if not self.widget:
            return
        self.widget.gotoGame.enabled = self.selectServerName and self.selectZone
