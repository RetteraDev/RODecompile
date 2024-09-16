#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbExcavateProxy.o
import urllib
import time
import BigWorld
import gameglobal
import uiConst
import events
import const
import utils
import gamelog
from uiProxy import UIProxy
from guis import ui
from guis import uiUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from helpers.ftbDataHelper import DigEventNode
from gamestrings import gameStrings
from data import ftb_config_data as FCD
from cdata import game_msg_def_data as GMDD
from guis import ftbWalletHelper

class FtbExcavateProxy(UIProxy):
    ICON_FRAME_FTB = 'fuxitongbao'
    ICON_FRAME_GUIBINQUAN = 'guibinquan'
    APPKEY = '91a3c4a911c30'

    def __init__(self, uiAdapter):
        super(FtbExcavateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_EXCAVATE, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_EXCAVATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_EXCAVATE)

    def show(self):
        if not gameglobal.rds.configData.get('enableFTB', False):
            return
        if gameglobal.rds.ui.realNameCheck.isPlayerThirdParty():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_EXCAVATE)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.miningBtn.addEventListener(events.BUTTON_CLICK, self._handleMiningBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self._handleRewardBtnClick, False, 0, True)
        self.widget.upgradeBtn.addEventListener(events.BUTTON_CLICK, self._handleUpgradeBtnClick, False, 0, True)
        self.widget.tradeBtn.addEventListener(events.BUTTON_CLICK, self._handleTradeBtnClick, False, 0, True)
        self.widget.licenseBtn.addEventListener(events.BUTTON_CLICK, self._handleLicenseBtnClick, False, 0, True)
        self.widget.walletBtn.addEventListener(events.BUTTON_CLICK, self._handleWalletBtnClick, False, 0, True)
        self.widget.blockwebBtn.addEventListener(events.BUTTON_CLICK, self._handleBlockwebBtnClick, False, 0, True)
        self.widget.autoDigHit.addEventListener(events.MOUSE_CLICK, self._handleAutoDigBtnClick, False, 0, True)
        self.widget.helpTop.helpKey = FCD.data.get('topHelpKey', 0)
        self.widget.help.helpKey = FCD.data.get('timeHelpKey', 0)
        self.widget.presentTime.text = gameStrings.FTB_TEXT_PRESENT_TIME % FCD.data.get('vipRewardTime', 2)
        self.widget.eventList.itemRenderer = 'FtbExcavate_ListItem'
        self.widget.eventList.labelFunction = self._eventListLabelFunction
        self.widget.eventList.dataArray = []
        self.widget.moneyIcon.bonusType = self.ICON_FRAME_FTB
        self.widget.totalNowEarning.icon.bonusType = self.ICON_FRAME_FTB
        self.widget.totalOutput.icon.bonusType = self.ICON_FRAME_FTB
        self.widget.dailyOutput.icon.bonusType = self.ICON_FRAME_FTB
        self.widget.yaojingTicket.icon.bonusType = self.ICON_FRAME_GUIBINQUAN
        self.widget.tradeBtn.disabled = True
        TipManager.addTip(self.widget.tradeBtn, gameStrings.COMMON_NOT_OPEN)
        if not gameglobal.rds.configData.get('enableFtbWallet', False):
            self.widget.walletBtn.disabled = True
            TipManager.addTip(self.widget.walletBtn, gameStrings.COMMON_NOT_OPEN)
        self.widget.reportWeb.htmlText = gameStrings.FTB_REPORT_TEXT
        self.widget.reportWeb.addEventListener(events.MOUSE_CLICK, self._handleReportWebClick, False, 0, True)
        self.widget.paimaiBtn.addEventListener(events.BUTTON_CLICK, self._handlePaimaiBtnClick, False, 0, True)
        self.widget.paimaiBtn.visible = False
        if gameglobal.rds.configData.get('enableFTBActivityClient', False):
            self.widget.paimaiBtn.visible = True
        p = BigWorld.player()
        if hasattr(p.base, 'queryDiggingPower'):
            p.base.queryDiggingPower()
        if hasattr(p.base, 'queryDigDetails'):
            p.base.queryDigDetails()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        totalEarning = p.ftbDataDetail.totalEarning
        totalNowEarning = p.ftbDataDetail.totalNowEarning
        yaojingTicket = p.ftbDataDetail.yaojingTicket
        guideDigPower = p.ftbDataDetail.guideDigPower
        baseDigPower = FCD.data.get('basePower', 30)
        digDuration = p.ftbDataDetail.digDuration
        leftDigingTime = p.ftbDataDetail.leftDigingTime
        weekTimeOfConsumed = p.ftbDataDetail.weekTimeOfConsumed
        hasVipRewardTaken = p.ftbDataDetail.hasVipRewardTaken
        digEventList = p.ftbDataDetail.digEventList
        totalOutput = p.ftbDataDetail.totalOutput
        dailyOutput = p.ftbDataDetail.dailyOutput
        isDigging = p.ftbDataDetail.isDigging
        isAutoDig = p.ftbDataDetail.isAutoDig
        ephemeralPower = p.ftbDataDetail.ephemeralPower
        self._refreshEarningData(totalEarning, totalNowEarning, yaojingTicket)
        self._refreshAbility(baseDigPower, guideDigPower, ephemeralPower)
        self._refreshDigDuration(digDuration)
        self._refreshLeftTime(weekTimeOfConsumed, leftDigingTime)
        self._refreshHasTaken(hasVipRewardTaken)
        self._refreshEventList(digEventList)
        self._refreshOuputData(totalOutput, dailyOutput)
        self._refreshDigingState(isDigging)
        self._refreshIsAutoDig(isAutoDig)

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    @ui.callFilter(1, True)
    def _handleMiningBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        p = BigWorld.player()
        if target.data.isDiging:
            self.__requestStopDig()
        elif not p.ftbDataDetail.digStateSwitch:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.FTB_WARNING_DIG_NOT_OPEN, self.__requestStartDig)
        else:
            self.__requestStartDig()

    @ui.callFilter(1, True)
    def _handleRewardBtnClick(self, *args):
        p = BigWorld.player()
        if hasattr(p.base, 'takeFTBVipRewardTime'):
            p.base.takeFTBVipRewardTime()

    def _handleUpgradeBtnClick(self, *args):
        gameglobal.rds.ui.ftbExcavateAbility.show()

    def _handleTradeBtnClick(self, *args):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.FTB_TRADE_WARNING, ())

    def _handleLicenseBtnClick(self, *args):
        gameglobal.rds.ui.ftbLicense.show()

    def _handleWalletBtnClick(self, *args):
        if gameglobal.rds.configData.get('enableFtbWallet', False):
            ftbWalletHelper.getInstance().openWallet()
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.FTB_WALLET_WARNING, ())

    def _handleBlockwebBtnClick(self, *args):
        blockUrl = FCD.data.get('blockWebUrl', '')
        if blockUrl:
            BigWorld.openUrl(blockUrl)
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.FTB_BLOCKWEB_WARNING, ())

    @ui.callFilter(0.5, True)
    def _handleAutoDigBtnClick(self, *args):
        p = BigWorld.player()
        p.base.setAutoDigState(not p.ftbDataDetail.isAutoDig)

    def _handleReportWebClick(self, *args):
        reportWeb = FCD.data.get('reportWeb', '')
        if reportWeb:
            BigWorld.openUrl(reportWeb)

    def _handlePaimaiBtnClick(self, *args):
        self.checkActivityInfo()

    @ui.checkInventoryLock()
    def checkActivityInfo(self):
        p = BigWorld.player()
        p.base.getFtbAuthCode()

    def onGetFtbAuthCode(self):
        self.openActivityWnd()

    def openActivityWnd(self):
        if not self.widget and not gameglobal.rds.ui.playRecomm.widget:
            return
        if hasattr(BigWorld.player(), 'ftbAuctionData') and BigWorld.player().ftbAuctionData:
            url = self.createActivityUrl()
            gameglobal.rds.ui.innerIE.show(url, 3, 900, 480, skinType=uiConst.IE_SKIN_TYPE_FIT_SIZE)

    def createActivityUrl(self):
        p = BigWorld.player()
        ftbAuctionData = BigWorld.player().ftbAuctionData
        urlBase = 'https://nbaas.8.163.com/web/lottery/home.html#/entry?'
        if gameglobal.rds.configData.get('enableFtbAuctionTestUrl', True):
            urlBase = 'http://nbaas.8.163.com/web/lottery/home.html#/entry?'
        params = {'accessId': ftbAuctionData.get('accessId'),
         'accessToken': ftbAuctionData.get('accessToken'),
         'appKey': self.APPKEY,
         'userGameId': p.gbId,
         'serverId': p.getOriginHostId(),
         'serverName': utils.getServerName(p.getOriginHostId),
         'nickName': unicode(p.roleName, 'gbk').encode('utf-8'),
         'serverTimestamp': ftbAuctionData.get('serverTimestamp'),
         'gameName': 'tianyu',
         'sign': ftbAuctionData.get('sign')}
        url = urlBase + urllib.urlencode(params)
        return url

    def openPaimaiWnd(self):
        if not self.widget:
            return
        if hasattr(BigWorld.player(), 'ftbAuctionData') and BigWorld.player().ftbAuctionData:
            url = self.createAuctionUrl()
            gamelog.debug('dxk@ftbExcavate open auction url', url)
            gameglobal.rds.ui.innerIE.show(url, 3, 1200, 600, skinType=uiConst.IE_SKIN_TYPE_FTB)

    def createAuctionUrl(self):
        ftbAuctionData = BigWorld.player().ftbAuctionData
        urlBase = 'https://nbaas.8.163.com/web/auction/#/auction?'
        if gameglobal.rds.configData.get('enableFtbAuctionTestUrl', True):
            urlBase = 'http://nbaas.8.163.com/web/auction/#/auction?'
        params = {'accessToken': ftbAuctionData.get('accessToken'),
         'accessId': ftbAuctionData.get('accessId'),
         'activityNumber': FCD.data.get('activityNumber', ''),
         'game': 'ty'}
        url = urlBase + urllib.urlencode(params)
        return url

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_EARNINGDATA_CHANGE)
    def onEarningDataChange(self, event):
        data = event.data
        total = data.get('totalEarning', 0.0)
        totalNow = data.get('totalNowEarning', 0.0)
        yaojing = data.get('yaojingTicket', 0.0)
        self._refreshEarningData(total, totalNow, yaojing)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_DIGINGSTATE_CHANGE)
    def onDigingStateChange(self, event):
        isDiging = event.data
        self._refreshDigingState(isDiging)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_DIGTIMEDURATION_CHANGE)
    def onDigDurationChange(self, event):
        duration = event.data
        self._refreshDigDuration(duration)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_HASVIPREWARDTAKEN_CHANGE)
    def onHasVipRewardTakenChange(self, event):
        hasTaken = event.data
        self._refreshHasTaken(hasTaken)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_EVENTLIST_CHANGE)
    def onEventListChange(self, event):
        evetList = event.data
        self._refreshEventList(evetList)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_OUTPUTDATA_CHANGE)
    def onOutputdataChange(self, event):
        data = event.data
        totalOutput = data.get('totalOutput', 0.0)
        dailyOutput = data.get('dailyOutput', 0.0)
        self._refreshOuputData(totalOutput, dailyOutput)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_DIGPOWER_CHANGE)
    def onDigPowerChange(self, event):
        baseDigPower = FCD.data.get('basePower', 30)
        p = BigWorld.player()
        self._refreshAbility(baseDigPower, p.ftbDataDetail.guideDigPower, p.ftbDataDetail.ephemeralPower)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_TIMEDATA_CHANGE)
    def onDigTimeDataChange(self, event):
        weekTimeOfConsumed = event.data.get('weekTimeOfConsumed', 0)
        leftDigingTime = event.data.get('leftDigingTime', 0)
        self._refreshLeftTime(weekTimeOfConsumed, leftDigingTime)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE, events.EVNET_FTB_AUTODIGSTATE_CHANGE)
    def onAutoDigStateChange(self, event):
        isAutoDig = event.data
        self._refreshIsAutoDig(isAutoDig)

    def _refreshEarningData(self, total, totalNow, yaojing):
        if not self.widget:
            return
        self.widget.totalEarning.text = '%.07f' % total
        self.widget.totalNowEarning.txt.text = '%.07f' % totalNow
        self.widget.yaojingTicket.txt.text = '%.02f' % yaojing
        TipManager.addTip(self.widget.totalNowEarning, gameStrings.FTB_TEXT_FUXITONGBAO)
        TipManager.addTip(self.widget.yaojingTicket, gameStrings.FTB_TEXT_YAOJINGTICKET)

    def _refreshDigingState(self, isDiging):
        if not self.widget:
            return
        self.widget.statePic.gotoAndStop('busy' if isDiging else 'free')
        self.widget.miningBtn.label = gameStrings.FTB_TEXT_START_DIGING if not isDiging else gameStrings.FTB_TEXT_STOP_DIGING
        self.widget.miningBtn.data = {'isDiging': isDiging}

    def _refreshAbility(self, baseAbility, guideAbility, ephemeralPower):
        if not self.widget:
            return
        self.widget.baseAbility.text = str(baseAbility)
        self.widget.guideAbility.text = str(guideAbility + ephemeralPower)
        self.widget.totalAbility.text = str(baseAbility + guideAbility + ephemeralPower)

    def _refreshDigDuration(self, duration):
        if not self.widget:
            return
        self.widget.digDuration.text = self._genDurationStr(duration)

    def _refreshLeftTime(self, weekTime, leftTime):
        if not self.widget:
            return
        self.widget.weekMiningTime.text = self._genLeftTimeStr(weekTime)
        self.widget.leftMiningTime.text = self._genLeftTimeStr(leftTime)

    def _refreshHasTaken(self, hasTaken):
        if not self.widget:
            return
        hasVip = uiUtils.hasVipBasicSimple()
        if hasVip:
            self.widget.redPoint.visible = not hasTaken
            self.widget.rewardBtn.enabled = not hasTaken
        else:
            self.widget.redPoint.visible = False
            self.widget.rewardBtn.enabled = False

    def _refreshEventList(self, eventList):
        if not self.widget:
            return
        self.widget.eventList.dataArray = eventList
        self.widget.eventList.scrollToEnd()

    def _refreshOuputData(self, totalOutput, dailyOutput):
        if not self.widget:
            return
        self.widget.totalOutput.txt.text = '%d' % int(totalOutput + 0.5)
        self.widget.dailyOutput.txt.text = '%d' % int(dailyOutput + 0.5)

    def _refreshIsAutoDig(self, isAutoDig):
        if not self.widget:
            return
        self.widget.autoDig.selected = isAutoDig

    def _genDurationStr(self, duration):
        t = duration
        hours = min(int(t / 3600), 99)
        t = t % 3600
        minutes = int(t / 60)
        t = t % 60
        seconds = int(t)
        return '%02d:%02d:%02d' % (hours, minutes, seconds)

    def _genDurationShortStr(self, duration):
        t = duration
        t = t % 3600
        minutes = int(t / 60)
        t = t % 60
        seconds = int(t)
        return '%02d:%02d' % (minutes, seconds)

    def _genLeftTimeStr(self, t):
        if t == 0:
            return '0' + gameStrings.COMMON_MINUTE
        tmp = t
        days = int(tmp / 86400)
        s = ''
        if days > 0:
            s += '%s' % days + gameStrings.COMMON_DAY
        tmp = tmp % 86400
        hours = int(tmp / 3600)
        tmp = tmp % 3600
        minutes = int(tmp / 60)
        if hours > 0:
            s += '%s' % hours + gameStrings.COMMON_HOUR
        if minutes > 0:
            s += '%s' % minutes + gameStrings.COMMON_MINUTE
        if not s:
            s = '0' + gameStrings.COMMON_MINUTE
        return s

    def _eventListLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.type == DigEventNode.START:
            itemMc.state.visible = True
            itemMc.state.text = gameStrings.FTB_TEXT_START_DIGING
            itemMc.earning.visible = False
        elif itemData.type == DigEventNode.STOP:
            itemMc.state.visible = True
            itemMc.state.text = gameStrings.FTB_TEXT_STOP_DIGING
            itemMc.earning.visible = False
        elif itemData.type == DigEventNode.EARNING:
            itemMc.state.visible = False
            itemMc.earning.visible = True
            itemMc.earning.txt.text = '%.07f' % itemData.value
            itemMc.earning.icon.bonusType = self.ICON_FRAME_FTB
        if itemData.time:
            itemMc.time.text = time.strftime('%H:%M', time.localtime(float(itemData.time)))
        else:
            itemMc.time.text = ''

    def __requestStartDig(self):
        p = BigWorld.player()
        if p.ftbDataDetail.availDigTime <= 0:
            BigWorld.player().showGameMsg(GMDD.data.FTB_TIME_WARNING, ())
            return
        if hasattr(p.base, 'startDig'):
            p.base.startDig()

    def __requestStopDig(self):
        p = BigWorld.player()
        if hasattr(p.base, 'stopDig'):
            p.base.stopDig(const.FTB_STOP_MANUAL)
