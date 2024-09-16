#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopDeclareProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from guis import uiUtils
from helpers import taboo
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD

class SchoolTopDeclareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopDeclareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_DECLARE, self.hide)

    def reset(self):
        pass

    @property
    def selfData(self):
        p = BigWorld.player()
        return p.getSelfCandidateData()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_DECLARE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_DECLARE)

    def show(self):
        if not self.selfData:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_DECLARE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.buyVip.addEventListener(events.BUTTON_CLICK, self.handleBuyVipClick, False, 0, True)
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.txtInput.addEventListener(events.EVENT_CHANGE, self.handleInputChange, False, 0, True)
        self.widget.broadcastLink.addEventListener(events.BUTTON_CLICK, self.handleBroadcastClick, False, 0, True)
        self.widget.txtInput.maxChars = 20

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.txtInput.text = self.selfData.get('declaration', '')

    def handleBuyVipClick(self, *args):
        self.uiAdapter.schoolTopVip.show()

    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        text = self.widget.txtInput.text
        result, text = taboo.checkDisbWord(text)
        if not result:
            p.showGameMsg(GMDD.data.SCHOOL_TOP_DECLARE_TABOO, ())
            return
        result, text = taboo.checkBWorld(text)
        if not result:
            p.showGameMsg(GMDD.data.SCHOOL_TOP_DECLARE_TABOO, ())
            return
        p.base.modifySchoolTopDeclaration(text)

    def handleInputChange(self, *args):
        self.widget.txtCnt.text = '%d/20' % self.widget.txtInput.textField.length

    def handleBroadcastClick(self, *args):
        msg = gameStrings.SCHOOL_TOP_DECLARE_VOTE_LINK % BigWorld.player().roleName
        color = '#ffe566'
        msg = "<font color= \'%s\'>[<a href = \'event:uiShow:schoolTopVote.show()\'><u>%s</u></a>]</font>" % (color, msg)
        gameglobal.rds.ui.sendLink(msg)
