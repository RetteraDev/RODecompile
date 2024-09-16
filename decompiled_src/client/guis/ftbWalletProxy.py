#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import base64
import time
import gametypes
import utils
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis import tipUtils
from guis import events
from guis.asObject import ASUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import ftb_config_data as FCD
QUERY_SIZE = 30
GAMESLOT_NUM = 8

class FtbWalletProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbWalletProxy, self).__init__(uiAdapter)
        self.widget = None
        self.dealInfo = {}
        self.bindGames = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_WALLET, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_WALLET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_WALLET)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_WALLET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.eventList.labelFunction = self.dealItemLabelFunc
        self.widget.eventList.itemRenderer = 'FtbWallet_dealItem'
        self.widget.addressBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick)
        self.widget.privateKeyBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick)
        self.widget.bindCodeBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick)
        self.widget.configBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick)
        self.widget.coinIcon.bonusType = gametypes.ICON_FRAME_FTB
        self.resetPrivateInfo()
        self.queryBindGameInfo()
        self.queryDealList()

    def queryBindGameInfo(self):
        BigWorld.player().base.queryFtbBindGame()

    def queryDealList(self):
        BigWorld.player().base.queryFtbTransaction(QUERY_SIZE)

    def resetPrivateInfo(self):
        if not self.widget:
            return
        self.widget.privateKeyBtn.label = gameStrings.FTB_WALLET_VIEW_PRIVAEKEY_CODE
        self.widget.bindCodeBtn.label = gameStrings.FTB_WALLET_VIEW_BIND_CODE
        self.widget.privateKeyText.text = ''
        self.widget.privateKeyText.visible = False
        self.widget.privatekeyLock.visible = True
        self.widget.bindCodeMc.text = ''
        self.widget.bindCodeMc.defaultText = gameStrings.FTB_WALLET_VIEW_BINDCODE_TIP
        ASUtils.setHitTestDisable(self.widget.bindCodeMc, True)

    def dealItemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.data = itemData
        itemMc.desc.text = itemData.tradeDescription
        timeArray = time.localtime(int(itemData.operationTime) / 1000)
        itemMc.time.text = str(time.strftime(gameStrings.TEXT_FTBWALLETDETAILPROXY_53, timeArray))
        itemMc.earning.amount.text = '%.07f' % itemData.transactionValue
        itemMc.earning.icon.bonusType = gametypes.ICON_FRAME_FTB
        if itemData.onChain:
            itemMc.state.htmlText = gameStrings.FTB_WALLET_DEAL_STATE_OK
        else:
            itemMc.state.htmlText = gameStrings.FTB_WALLET_DEAL_STATE_CONFIRM
        itemMc.addEventListener(events.MOUSE_CLICK, self.onDealItemClick)

    def onDealItemClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.data
        gameglobal.rds.ui.ftbWalletDetail.show(itemData)

    def onButtonClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        if btnName == 'addressBtn':
            BigWorld.setClipBoardText(self.widget.adressText.text)
        elif btnName == 'privateKeyBtn':
            if self.widget.privateKeyText.text:
                BigWorld.setClipBoardText(self.widget.privateKeyText.text)
            else:
                gameglobal.rds.ui.ftbWalletSubWnd.showViewPrivateKeyWnd(self.showBindPrivateKey)
        elif btnName == 'bindCodeBtn':
            if self.widget.bindCodeMc.text:
                BigWorld.setClipBoardText(self.widget.bindCodeMc.text)
            else:
                gameglobal.rds.ui.ftbWalletSubWnd.showViewBindCodeWnd(self.showBindCode)
        elif btnName == 'configBtn':
            gameglobal.rds.ui.ftbWalletSubWnd.showResetPassWndState0()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        ftbWalletData = getattr(p, 'ftbWalletData', {})
        self.widget.moneyText.text = '%.07f' % ftbWalletData.get('balance', 0)
        self.widget.adressText.text = ftbWalletData.get('bcAddress', '')
        self.refreshDealList()
        self.refreshBindList()

    def onGetDealList(self, data):
        self.dealInfo = data
        self.refreshDealList()

    def onGetBindInfo(self, data):
        self.bindGames = data
        self.refreshBindList()

    def showBindPrivateKey(self):
        p = BigWorld.player()
        privateKey = getattr(p, 'ftbPrivateKey', {}).get('privateKey', '')
        self.widget.privateKeyText.text = base64.decodestring(privateKey)
        self.widget.privateKeyBtn.label = gameStrings.FTB_WALLET_COPY
        self.widget.privateKeyText.visible = True
        self.widget.privatekeyLock.visible = False

    def showBindCode(self):
        p = BigWorld.player()
        bindCode = getattr(p, 'ftbPrivateKey', {}).get('mnemonicList', '')
        self.widget.bindCodeMc.text = base64.decodestring(bindCode)
        self.widget.bindCodeBtn.label = gameStrings.FTB_WALLET_COPY
        ASUtils.setHitTestDisable(self.widget.bindCodeMc, False)

    def getIconPath(self, iconName):
        return 'appIcons/' + iconName + '.png'

    def refreshBindList(self):
        self.widget.bindAppText.text = gameStrings.FTB_WALLET_BIND_GAME_TXT % len(self.bindGames)
        appInfos = FCD.data.get('appIcons', {})
        gameKeys = appInfos.keys()
        for i in xrange(GAMESLOT_NUM):
            slotMc = self.widget.getChildByName('icon%d' % i)
            slotMc.bg.gotoAndPlay('lock')
            if i < len(gameKeys):
                appKey = gameKeys[i]
                appInfo = appInfos.get(appKey, ['', ''])
                name = appInfo[0]
                photo = appInfo[1]
                slotMc.icon.visible = True
                slotMc.icon.fitSize = True
                TipManager.addTip(slotMc, name, tipUtils.TYPE_DEFAULT_BLACK)
                slotMc.icon.loadImage(self.getIconPath(photo))
                if appKey in self.bindGames:
                    slotMc.bindMc.visible = False
                else:
                    slotMc.bindMc.visible = True
            else:
                slotMc.icon.visible = False
                slotMc.bindMc.visible = False

    def refreshDealList(self):
        self.widget.eventList.dataArray = self.dealInfo.get('transactionHist', [])
