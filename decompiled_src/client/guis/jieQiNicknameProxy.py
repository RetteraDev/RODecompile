#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/jieQiNicknameProxy.o
import BigWorld
import gameglobal
import events
import utils
from helpers import taboo
from guis import uiConst
from guis.asObject import ASObject
from guis.uiProxy import UIProxy
from gamestrings import gameStrings
from data import sys_config_data as SCD
MAX_WORD_NUM = 4

class JieQiNicknameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JieQiNicknameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.nickName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_JIEQI_NICKNAME, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_JIEQI_NICKNAME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_JIEQI_NICKNAME)

    def reset(self):
        self.nickName = ''

    def show(self):
        if not gameglobal.rds.configData.get('enableIntimacyTgtNickName', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_JIEQI_NICKNAME, isModal=True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.inputArea.addEventListener(events.EVENT_CHANGE, self.handleChangeWord, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.inputArea.text = self.nickName = p.intimacyTgtNickName or ''
        self.widget.inputArea.validateNow()
        num = MAX_WORD_NUM - self.widget.inputArea.textField.length
        self.updateWordNum(num)

    def handleChangeWord(self, *args):
        e = ASObject(args[3][0])
        nickName = e.currentTarget.text
        num = MAX_WORD_NUM - e.currentTarget.textField.length
        if num == 0:
            self.nickName = nickName
        if num < 0:
            num = 0
            self.widget.inputArea.text = self.nickName
        self.updateWordNum(num)

    def _onCommitBtnClick(self, e):
        p = BigWorld.player()
        tgtGbId = p.friend.intimacyTgt
        nickName = self.widget.inputArea.text
        result, _ = taboo.checkNameDisWord(nickName)
        if not result:
            self.widget.inputArea.text = ''
            self.widget.inputNums.htmlText = SCD.data.get('jieQiNicknameTabooWord', '')
        else:
            bFlag = utils.isChineseAndNumber(nickName)
            if bFlag:
                p.base.setIntimacyTgtNickName(tgtGbId, nickName)
                self.hide()
            else:
                self.widget.inputArea.text = ''
                self.widget.inputNums.htmlText = gameStrings.JIEQI_NICKNAME_AGAIN_INPUT

    def updateWordNum(self, num):
        color = "<font color = \'#6de539\'>"
        if num == 0:
            color = "<font color = \'#f43804\'>"
        showStr = gameStrings.JIEQI_NICKNAME_WORD_NUM % (color, num, MAX_WORD_NUM)
        self.widget.inputNums.htmlText = showStr
