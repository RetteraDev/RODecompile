#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbLicenseProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
from uiProxy import UIProxy
from guis.asObject import ASUtils
from gamestrings import gameStrings
from guis import uiUtils
from guis import ui
from data import ftb_config_data as FCD

class FtbLicenseProxy(UIProxy):
    COLOR_DEFUALT = '#703921'

    def __init__(self, uiAdapter):
        super(FtbLicenseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_LICENSE, self.hide)

    def reset(self):
        self.ftbLicenseTextData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_LICENSE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_LICENSE)
        self.reset()

    def show(self):
        if not gameglobal.rds.configData.get('enableFTB', False):
            return
        if gameglobal.rds.ui.realNameCheck.isPlayerThirdParty():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_LICENSE)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.main.closeBtn
        self.widget.gotoAndPlay(0)
        ASUtils.callbackAtFrame(self.widget, 35, self.refreshInfo)
        self.widget.main.signBtn.addEventListener(events.BUTTON_CLICK, self._handleSignBtnClick, False, 0, True)
        self.widget.main.help.helpKey = FCD.data.get('licenseHelpKey', 0)
        p = BigWorld.player()
        if hasattr(p.base, 'queryFTBLicense'):
            p.base.queryFTBLicense()

    def refreshInfo(self):
        if not self.widget:
            return
        self._refreshAllTextUi()

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    @ui.callFilter(1, True)
    def _handleSignBtnClick(self, *args):
        p = BigWorld.player()
        if not self.isFtbAdrrCreated():
            self.widget.main.signBtn.enabled = False
            self.widget.main.license.htmlText = uiUtils.toHtml(gameStrings.FTB_TEXT_LICENSE_NOT_READY, self.COLOR_DEFUALT)
        elif hasattr(p.base, 'signFTBLicense'):
            p.base.signFTBLicense()

    def isFtbAdrrCreated(self):
        p = BigWorld.player()
        if not hasattr(p, 'ftbDataDetail'):
            return False
        return not not p.ftbDataDetail.ftbAddr

    @ui.uiEvent(uiConst.WIDGET_FTB_LICENSE, events.EVNET_FTB_LICENSEDATA_CHANGE)
    def onLicenseDataChange(self, event):
        self._refreshAllTextUi()

    def _refreshAllTextUi(self):
        if not self.widget or not self.widget.main:
            return
        p = BigWorld.player()
        if not hasattr(p, 'ftbDataDetail'):
            return
        roleName = p.roleName
        mineType = gameStrings.FTB_TEXT_MINE_TYPE_DEFAULT
        basePower = FCD.data.get('basePower', 0)
        guidePower = p.ftbDataDetail.guideDigPower
        hasSigned = p.ftbDataDetail.hasSigned
        licenseNo = p.ftbDataDetail.licenseNo
        ftbAddr = p.ftbDataDetail.ftbAddr
        addressSite = p.ftbDataDetail.ftbSite
        self.widget.main.roleName.htmlText = uiUtils.toHtml(roleName, self.COLOR_DEFUALT)
        self.widget.main.mineType.htmlText = uiUtils.toHtml(mineType, self.COLOR_DEFUALT)
        self.widget.main.miningAbility.htmlText = uiUtils.toHtml(gameStrings.FTB_TEXT_MINING_ABILITY_DEFAULT % basePower, self.COLOR_DEFUALT)
        self.widget.main.guideValue.htmlText = uiUtils.toHtml(gameStrings.FTB_TEXT_GUIDE_VALUE_DEFAULT % guidePower, self.COLOR_DEFUALT)
        self.widget.main.address.htmlText = uiUtils.toHtml(addressSite, self.COLOR_DEFUALT)
        self.widget.main.miningMothed.htmlText = uiUtils.toHtml(gameStrings.FTB_TEXT_MINING_MOTHED_DEFAULT, self.COLOR_DEFUALT)
        self.widget.main.period.htmlText = uiUtils.toHtml(gameStrings.FTB_TEXT_PERIOD_DEFAULT, self.COLOR_DEFUALT)
        self._refreshLicenseData(licenseNo, hasSigned, ftbAddr, addressSite)

    def _refreshLicenseData(self, licenseNo, hasSigned, ftbAddr, addressSite):
        self.widget.main.certificate.htmlText = uiUtils.toHtml(str(licenseNo)[0:12] if hasSigned else '', self.COLOR_DEFUALT)
        self.widget.main.license.htmlText = uiUtils.toHtml(ftbAddr if hasSigned else gameStrings.FTB_TEXT_LICENSE_DEFAULT, self.COLOR_DEFUALT)
        self.widget.main.signBtn.enabled = not hasSigned
        self.widget.main.address.htmlText = uiUtils.toHtml(addressSite, self.COLOR_DEFUALT) if hasSigned else ''

    def _genAddressSiteText(self, siteIdx):
        allAddrs = FCD.data.get('addressText', ())
        if siteIdx < 0 or siteIdx >= len(allAddrs):
            return ''
        return allAddrs[siteIdx]
