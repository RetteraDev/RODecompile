#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationLeaveBookProxy.o
import BigWorld
import gameglobal
import gamelog
import utils
import uiConst
import events
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
import clientUtils
from cdata import assassination_config_data as ACD
ASSASSINATION_LEAVE_CONTENT_COLUMN = 3
ASSASSINATION_LEAVE_CONTENT_MAX_NUMS = 1000

class AssassinationLeaveBookProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationLeaveBookProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ASSASSINATION_LEAVE_BOOK, self.hide)

    def reset(self):
        self.assName = ''
        self.assContentId = 1
        self.assContent = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_LEAVE_BOOK:
            self.widget = widget
            self.refreshData()
            self.refreshUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_LEAVE_BOOK)

    def show(self, assName, assContentId):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_LEAVE_BOOK)
            self.assName = assName
            self.assContentId = assContentId

    def refreshData(self):
        self.assContent = ACD.data.get('assassinationMsgDict', {}).get(self.assContentId, '')

    def refreshUI(self):
        if not self.widget:
            return
        else:
            self.widget.hit.addEventListener(events.MOUSE_CLICK, self.handleCloseBtnClick, False, 0, True)
            allContent = self.gbk2Unicode(self.assContent)
            curContent = ''
            for idx in xrange(ASSASSINATION_LEAVE_CONTENT_COLUMN):
                if len(allContent) > ASSASSINATION_LEAVE_CONTENT_MAX_NUMS:
                    curContent = allContent[0:ASSASSINATION_LEAVE_CONTENT_MAX_NUMS]
                    allContent = allContent[ASSASSINATION_LEAVE_CONTENT_MAX_NUMS:]
                else:
                    curContent = allContent
                    allContent = ''
                contentMc = getattr(self.widget, 'content%d' % idx, None)
                if contentMc:
                    contentMc.text = self.unicode2gbk(curContent)

            self.widget.assassinationName.text = self.assName
            return

    def handleCloseBtnClick(self, *args):
        if self.widget:
            self.hide()

    def gbk2Unicode(self, str, default = ''):
        try:
            return str.decode(utils.defaultEncoding())
        except:
            gamelog.error('AssassinationLeaveBoolProxy gbk2unicode error', str)
            return default

    def unicode2gbk(self, str, default = ''):
        try:
            return str.encode(utils.defaultEncoding())
        except:
            gamelog.error('AssassinationLeaveBoolProxy unicode2utf error', str)
            return default
