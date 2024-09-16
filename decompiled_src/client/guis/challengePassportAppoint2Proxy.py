#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/challengePassportAppoint2Proxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from guis import events
from data import challenge_passport_config_data as CPCD
from cdata import challenge_passport_season_data as CPSD

class ChallengePassportAppoint2Proxy(UIProxy):
    TAB_POS_START_X = 0
    TAB_POS_START_Y = 766
    TAB_INTERVAL = 38

    def _setCurrentPage(self, value):
        if value != self.currentPage:
            self.currentPage = value
            self.setPageData(self.currentPage)

    CurrentPage = property(lambda self: self.currentPage, _setCurrentPage)

    def __init__(self, uiAdapter):
        super(ChallengePassportAppoint2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.numPage = 0
        self.currentPage = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT2)
        self.reset()

    def show(self):
        if not gameglobal.rds.configData.get('enableChallengePassport', False):
            return
        if not uiUtils.isInChallengePassport():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT2, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.main.returnBtn
        self.widget.gotoAndPlay(0)
        self.widget.main.prePageBtn.addEventListener(events.BUTTON_CLICK, self.handlePrePageClick, False, 0, True)
        self.widget.main.nextPageBtn.addEventListener(events.BUTTON_CLICK, self.handleNextPageClick, False, 0, True)
        self.initPages()
        self.setPageData(0)
        self.refreshPhoto()

    def refreshPhoto(self):
        season = uiUtils.getCurrentChallengePassportSeason()
        seasonData = CPSD.data.get(season, {})
        self.widget.photo.gotoAndStop(seasonData.get('clothName', ''))

    def refreshInfo(self):
        if not self.widget:
            return

    def initPages(self):
        self.numPage = len(CPCD.data.get('challengePassportOpenUiDesc', ()))
        for i in xrange(self.numPage):
            tabMc = self.widget.getInstByClsName('PassportAppoint2_Tab')
            tabMc.name = 'page%d' % i
            self.widget.main.addChild(tabMc)
            tabMc.x = self.TAB_POS_START_X + i * self.TAB_INTERVAL
            tabMc.y = self.TAB_POS_START_Y

        self.currentPage = 0

    def setPageData(self, page):
        for i in xrange(self.numPage):
            pageMc = self.widget.main.getChildByName('page%d' % i)
            if pageMc:
                pageMc.gotoAndStop('on' if i == page else 'off')

        if page in range(self.numPage):
            descTxt = CPCD.data.get('challengePassportOpenUiDesc', ())[page]
            titleTxt = CPCD.data.get('challengePassportOpenUiTitle', ())[page]
        else:
            descTxt = titleTxt = ''
        self.widget.main.desc.htmlText = descTxt
        self.widget.main.title.text = titleTxt
        self.widget.main.prePageBtn.enabled = page != 0
        self.widget.main.nextPageBtn.enabled = page != self.numPage - 1

    def handlePrePageClick(self, *args):
        self.CurrentPage = max(0, self.CurrentPage - 1)

    def handleNextPageClick(self, *args):
        self.CurrentPage = min(self.numPage - 1, self.CurrentPage + 1)
