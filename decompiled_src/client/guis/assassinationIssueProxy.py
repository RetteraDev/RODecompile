#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationIssueProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from callbackHelper import Functor
import clientUtils
from cdata import assassination_config_data as ACD
from cdata import game_msg_def_data as GMDD
ASSASSINATION_MONEY_GRADE_NUMS = 3

class AssassinationIssueProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationIssueProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ASSASSINATION_ISSUE, self.hide)

    def reset(self):
        self.leaveContentTxtList = []
        self.curSelectedContentId = 1
        self.isAnonymous = False
        self.anonymityMoney = 0
        self.money = 0
        self.moneyUpperLimit = 999999
        self.moneyLowerLimit = 0
        self.ruleTipsStr = ''
        self.moneyGradeList = []
        self.enemyData = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_ISSUE:
            self.widget = widget
            self.reset()
            self.initData()
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_ISSUE)

    def show(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            BigWorld.player().base.refreshOtherFriends()
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_ISSUE)

    def initData(self):
        leaveContentTxtDict = ACD.data.get('assassinationMsgDict', {})
        for idx, text in leaveContentTxtDict.iteritems():
            self.leaveContentTxtList.append({'label': text,
             'id': idx})

        self.anonymityMoney = ACD.data.get('assassinationAnonymityCost', 0)
        self.moneyUpperLimit = ACD.data.get('rewardUpperLimit', 0)
        self.moneyLowerLimit = ACD.data.get('assassinationRewardLimit', 0)
        self.ruleTipsStr = ACD.data.get('ruleTipsStr', 0)
        self.moneyGradeList = ACD.data.get('assassinationAnonymityCostGradeList', [])
        self.money = self.moneyLowerLimit

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initLeaveContent()
        self.initAnonymityCheckBox()
        self.initMoneyInput()
        self.initSubmitBtn()
        self.initGrade()
        self.initPortrait()

    def initLeaveContent(self):
        self.widget.leaveContent.selectedIndex = 0
        ASUtils.setDropdownMenuData(self.widget.leaveContent, self.leaveContentTxtList)
        self.widget.leaveContent.addEventListener(events.INDEX_CHANGE, self.handleLeaveContentIndexChangeClick, False, 0, True)
        self.widget.leaveContent.menuRowCount = min(len(self.leaveContentTxtList), 5)
        self.widget.leaveContent.validateNow()

    def handleLeaveContentIndexChangeClick(self, *args):
        idx = self.widget.leaveContent.selectedIndex
        if idx < len(self.leaveContentTxtList):
            self.curSelectedContentId = self.leaveContentTxtList[idx].get('id', 1)

    def initAnonymityCheckBox(self):
        self.widget.anonymityCheckBox.selected = self.isAnonymous
        self.widget.anonymityCheckBox.addEventListener(events.BUTTON_CLICK, self.handleAnonymityCheckBoxClick, False, 0, True)
        self.updateAnonymityMoneyIconMc()

    def handleAnonymityCheckBoxClick(self, *args):
        e = ASObject(args[3][0])
        self.isAnonymous = e.currentTarget.selected
        self.updateAnonymityMoneyIconMc()

    def updateAnonymityMoneyIconMc(self):
        self.widget.anonymityMoney.text = self.anonymityMoney
        self.widget.anonymityMoneyIconMc.visible = self.isAnonymous
        self.widget.anonymityMoney.visible = self.isAnonymous

    def initMoneyInput(self):
        self.widget.moneyInput.text = self.moneyLowerLimit
        self.widget.moneyInput.maxNum = self.moneyUpperLimit
        self.widget.moneyInput.addEventListener(events.EVENT_CHANGE, self.handleoMoneyInputChange)
        self.widget.moneyInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleMoneyInputKeyEnterClick, False, 0, True)

    def handleoMoneyInputChange(self, *args):
        e = ASObject(args[3][0])
        textInputMc = e.currentTarget
        if textInputMc.text == '':
            self.money = 0
        else:
            self.money = int(textInputMc.text)
        self.refreshGrade()

    def handleMoneyInputKeyEnterClick(self, *args):
        searchInputMc = ASObject(args[3][0])
        if searchInputMc.keyCode == events.KEYBOARD_CODE_ENTER or searchInputMc.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            searchInputMc.currentTarget.stage.focus = None
            searchInputMc.stopImmediatePropagation()

    def initSubmitBtn(self):
        self.widget.submitBtn.addEventListener(events.BUTTON_CLICK, self.handSubmitBtnClick, False, 0, True)

    def handSubmitBtnClick(self, *args):
        if self.widget.moneyInput.text != '':
            self.money = int(self.widget.moneyInput.text)
        else:
            self.money = 0
        msg = ''
        if self.isAnonymous:
            msg = gameStrings.ASSASSINATION_SUBMIT_WIDTH_ANONYMITY_MSG % (self.money, self.anonymityMoney)
        else:
            msg = gameStrings.ASSASSINATION_SUBMIT_MSG % self.money
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.requestSubmit)

    def requestSubmit(self):
        check = gameglobal.rds.ui.assassinationMain.checkIssue() and self.realCheckIssue()
        if check:
            BigWorld.player().base.putAssassinationOnBoard(self.enemyData.get('gbId', 0), self.enemyData.get('name', ''), self.enemyData.get('school', ''), self.enemyData.get('sex', 0), self.enemyData.get('lv', 0), self.money, not self.isAnonymous, self.curSelectedContentId)
            self.hide()

    def initGrade(self):
        self.widget.ruleTip.htmlText = self.ruleTipsStr
        for idx in xrange(ASSASSINATION_MONEY_GRADE_NUMS):
            mgMc = getattr(self.widget, 'moneyGrade%d' % idx, None)
            mgMc.text = self.moneyGradeList[idx]['name']
            TipManager.addTip(mgMc, self.moneyGradeList[idx]['tip'])

        self.refreshGrade()

    def refreshGrade(self):
        gradeData = gameglobal.rds.ui.assassinationMain.checkMoneyGrade(self.money)
        if gradeData:
            self.widget.curMoneyGrade.text = gameStrings.ASSASSINATION_GRADE + gradeData['name']
        else:
            self.widget.curMoneyGrade.text = ''

    def initPortrait(self):
        self.widget.portrait.addEventListener(events.BUTTON_CLICK, self.handlePortraitClick, False, 0, True)
        self.refreshPortrait()

    def refreshPortrait(self):
        ptMc = self.widget.portrait
        if self.enemyData:
            ptMc.selected = True
            if self.enemyData.get('headIcon', ''):
                ptMc.headIcon.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
                ptMc.headIcon.headIcon.fitSize = True
                ptMc.headIcon.headIcon.serverId = int(gameglobal.rds.g_serverid)
                ptMc.headIcon.headIcon.url = self.enemyData.get('headIcon', '')
            else:
                ptMc.headIcon.headIcon.fitSize = True
                ptMc.headIcon.headIcon.loadImage(uiUtils.getHeadIconPath(self.enemyData.get('school', 0), self.enemyData.get('sex', 0)))
            ptMc.lvMc.htmlText = str(self.enemyData.get('lv', 0))
        else:
            ptMc.selected = False

    def handlePortraitClick(self, *args):
        gameglobal.rds.ui.assassinationEnemy.show()

    def confirmToSelectEmeny(self, enemyData):
        if not self.widget:
            return
        self.enemyData = enemyData
        self.enemyData['gbId'] = long(self.enemyData['gbId'])
        self.refreshPortrait()

    def realCheckIssue(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return False
        if not self.moneyLowerLimit <= self.money <= self.moneyUpperLimit:
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_MONEY_ERROR, (self.moneyLowerLimit, self.moneyUpperLimit))
            return False
        if not (self.enemyData and self.enemyData.get('gbId', 0) != 0):
            p.showGameMsg(GMDD.data.ASSASSINATION_ISSUE_NONE_TARGET_DATA, ())
            return False
        return True
