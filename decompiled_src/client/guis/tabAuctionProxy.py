#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tabAuctionProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
from Scaleform import GfxValue
from ui import unicode2gbk
import gamelog
from uiProxy import UIProxy
from data import region_server_config_data as RSCD
from cdata import coin_consign_config_Data as CCCD
TAB_IDX_PROXY = {0: 'tabAuctionConsign',
 1: 'tabAuctionConsign',
 2: 'tabAuctionCrossServer'}

class TabAuctionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TabAuctionProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'changeTabIndex': self.onChangeTabIndex,
         'initTabInfo': self.onInitTabInfo,
         'setInitData': self.onSetInitData}
        self.mediator = None
        self.tabIdx = uiConst.TABAUCTION_TAB_YUNBI
        self.subTabIdx = 0
        self.switchData = {}
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_AUCTION, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TAB_AUCTION:
            self.mediator = mediator
            self.resetSwitchData()
            return uiUtils.array2GfxAarry([self.tabIdx, self.subTabIdx])

    def clearWidget(self):
        self.resetSwitchData()
        self.mediator = None
        self.npcId = 0
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_AUCTION)

    def reset(self):
        self.tabIdx = uiConst.TABAUCTION_TAB_YUNBI
        self.subTabIdx = 0

    def show(self, tabIdx, subTabIdx = 0, npcId = 0, layoutType = uiConst.LAYOUT_DEFAULT):
        p = BigWorld.player()
        serverProgressMsId = CCCD.data.get('crossConsignServerProgressID', 0)
        if tabIdx == uiConst.TABAUCTION_TAB_CROSS_SERVER:
            if p._isSoul() or not gameglobal.rds.configData.get('enableCrossConsign', False) or not gameglobal.rds.configData.get('enableTabAuction', False) or not p.checkServerProgress(serverProgressMsId, False):
                tabIdx = uiConst.TABAUCTION_TAB_YUNBI
        if not self.mediator:
            self.tabIdx = tabIdx
            self.subTabIdx = subTabIdx
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_AUCTION, layoutType=layoutType)
        if gameglobal.rds.ui.mail.mediator:
            gameglobal.rds.ui.mail.hide()
        self.npcId = npcId

    def onClose(self, *arg):
        self.checkAndHide()

    def checkAndHide(self):
        self.hide()

    def onChangeTabIndex(self, *arg):
        tabIdx = int(arg[3][0].GetNumber())
        subTabIdx = int(arg[3][1].GetNumber())
        self.realSetTabIndex(tabIdx, subTabIdx)

    def realSetTabIndex(self, tabIdx, subTabIdx):
        if self.mediator:
            self.tabIdx = tabIdx
            self.subTabIdx = subTabIdx
            self.mediator.Invoke('realSetTabIndex', (GfxValue(self.tabIdx), GfxValue(self.subTabIdx)))

    def onInitTabInfo(self, *arg):
        ret = {}
        canCrossServer = True
        tips = ''
        rdata = RSCD.data.get(int(gameglobal.rds.g_serverid), {})
        if not gameglobal.rds.configData.get('enableCrossConsign', False):
            canCrossServer = False
            tips = CCCD.data.get('crossConsignForbiddenTips2', '')
        if not rdata.get('xConsignRegionId', None) or not rdata.get('xConsignCenterHostID', None):
            canCrossServer = False
            tips = CCCD.data.get('crossConsignForbiddenTips2', '')
        serverProgressMsId = CCCD.data.get('crossConsignServerProgressID', 0)
        p = BigWorld.player()
        if not p.checkServerProgress(serverProgressMsId, False):
            canCrossServer = False
            tips = CCCD.data.get('crossConsignForbiddenTips', '')
        ret['canCrossServer'] = canCrossServer
        ret['tips'] = tips
        return uiUtils.dict2GfxDict(ret, True)

    def setSwitchData(self, *arg):
        searchName = unicode2gbk(arg[3][0].GetString())
        selectedBtn = unicode2gbk(arg[3][1].GetString())
        availableCkBox = arg[3][2].GetBool()
        minLv = unicode2gbk(arg[3][3].GetString())
        maxLv = unicode2gbk(arg[3][4].GetString())
        gamelog.debug('@zq availableCkBox', availableCkBox)
        info = {'searchName': searchName,
         'selectedBtn': selectedBtn,
         'availableCkBox': availableCkBox,
         'minLv': minLv,
         'maxLv': maxLv}
        self.switchData = info

    def resetSwitchData(self):
        self.switchData = {'searchName': '',
         'selectedBtn': '',
         'availableCkBox': False,
         'minLv': '',
         'maxLv': ''}

    def onSetInitData(self, *arg):
        _proxyStr = TAB_IDX_PROXY.get(self.tabIdx, '')
        if _proxyStr and hasattr(gameglobal.rds.ui, _proxyStr):
            getattr(gameglobal.rds.ui, _proxyStr).setInitInfo(self.switchData)
        self.switchData = {}

    def getEntity(self):
        e = None
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
        else:
            e = BigWorld.player()
        return e
