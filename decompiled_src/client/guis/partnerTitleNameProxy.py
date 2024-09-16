#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/partnerTitleNameProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import utils
import commQuest
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from gamestrings import gameStrings
from gamestrings import DEFAULT_LANGUAGE
from callbackHelper import Functor
from helpers import taboo
from data import partner_config_data as PCD
from data import title_data as TD
from cdata import game_msg_def_data as GMDD
MIDDLETYPE_NUM = 5

class PartnerTitleNameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PartnerTitleNameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PARTNER_TITLE_NAME, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PARTNER_TITLE_NAME:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PARTNER_TITLE_NAME)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PARTNER_TITLE_NAME)
        self.widget = None
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        self.widget.numType1.selected = True
        for x in xrange(0, 5):
            numType = getattr(self.widget, 'numType' + str(x + 1), None)
            if numType:
                numType.data = x
                numstr = ''
                if len(p.members) >= const.PARTNER_MIN_NUM and len(p.members) <= const.PARTNER_MAX_NUM:
                    numstr = p.getPartnerTitleNumStyle(x + 1, len(p.members))
                numType.label = numstr
                numType.addEventListener(events.EVENT_SELECT, self.handleSelectedNumType, False, 0, True)

        self.widget.prefix.maxChars = 5
        self.widget.postfix.maxChars = 3
        self.widget.prefix.addEventListener(events.EVENT_CHANGE, self.handleTextChange, False, 0, True)
        self.widget.postfix.addEventListener(events.EVENT_CHANGE, self.handleTextChange, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            self.updateTitlePreview()

    def handleSelectedNumType(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        t.group.selectedIndex
        self.updateTitlePreview()

    def handleTextChange(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        self.updateTitlePreview()

    def _getPrefixText(self):
        if self.hasBaseData():
            return self.widget.prefix.text.strip()
        return ''

    def _getPostfixText(self):
        if self.hasBaseData():
            return self.widget.postfix.text.strip()
        return ''

    def _getMidType(self):
        if self.hasBaseData():
            return self.widget.numType1.group.selectedIndex + 1

    def getTitleData(self):
        return (self._getPrefixText(), self._getPostfixText(), self._getMidType())

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def updateTitlePreview(self):
        p = BigWorld.player()
        prefix, postfix, midType = self.getTitleData()
        if prefix:
            titleStr = p.connectPartnerTitleName(prefix, postfix, midType, len(p.members))
            partnerTitleId = PCD.data.get('partnerTitleId', 0)
            tData = TD.data.get(partnerTitleId, {})
            titleStr = uiUtils.toHtml(titleStr, uiConst.TITLE_COLOR_DIC.get(tData.get('style', 0), ''))
            self.widget.titleShow.htmlText = titleStr
        else:
            self.widget.titleShow.htmlText = gameStrings.PARTNER_PLZ_INPUT

    def strLimit(self, strContent):
        try:
            strContent = strContent.strip()
            strContent = strContent.decode(utils.defaultEncoding())
        except:
            return False

        if utils.getGameLanuage() == DEFAULT_LANGUAGE:
            for s in strContent:
                if not self.is_chinese(s):
                    return False

            return True
        else:
            return True
        return True

    def is_chinese(self, uchar):
        if uchar >= '一' and uchar <= '龥':
            return True
        else:
            return False

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        if self._getPrefixText() == '':
            p.showGameMsg(GMDD.data.PARTNER_INPUT_NAME_INVALID, ())
            return
        prefix, postfix, midType = self.getTitleData()
        p._applyPartnerTeamName(prefix, postfix, midType)

    def tabooCheck(self, msg):
        isNormal1, msg = taboo.checkDisbWord(msg)
        isNormal2, msg = taboo.checkBSingle(msg)
        isNormal3, msg = taboo.checkNameDisWord(msg)
        return isNormal1 and isNormal2 and isNormal3
