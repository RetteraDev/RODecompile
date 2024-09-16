#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/questionnaireProxy.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import gameglobal
import clientUtils
import events
import uiConst
import uiUtils
import cefUIManager
import const
from helpers import CEFControl
from guis.uiProxy import UIProxy
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import consumable_item_data as CID
from data import question_data as QD
from data import mail_template_data as MTD
from cdata import game_msg_def_data as GMDD

class QuestionnaireProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuestionnaireProxy, self).__init__(uiAdapter)
        self.widget = None
        self.width = 720
        self.height = 400
        self.swfPath = 'gui/widgets/QuestionnaireWidget' + uiAdapter.getUIExt()
        self.insName = 'Questionnaire_unitWeb'
        self.oldX = 0
        self.oldY = 0
        self.url = ''
        self.curQuestionId = 0
        self.pussMessageInfo = []
        self.questionnairType = 0
        self.questionnairItem = 0
        self.isFinished = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QUESTIONNAIRE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, questionnairType = uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE, itemId = 0):
        if questionnairType == uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE:
            if not self.pussMessageInfo:
                return
        elif questionnairType == uiConst.QUESTIONNAIRE_TYPE_ITEM:
            if not itemId:
                return
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_QUESTIONNAIRE, closeFunc=self.hide):
            return
        self.questionnairType = questionnairType
        self.questionnaireItemId = itemId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_QUESTIONNAIRE)

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_QUESTIONNAIRE)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QUESTIONNAIRE)

    def clearAll(self):
        self.pussMessageInfo = []

    def reset(self):
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        self.url = ''
        self.curQuestionId = 0
        self.questionnairType = 0
        self.questionnaireItemId = 0

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.minimizeBtn
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCloseBtn, False, 0, True)
        self.widget.completeBtn.enabled = self.isFinished

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            p.lockKey(gameglobal.KEY_POS_UI, False)
            if self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE:
                questionId = self.pussMessageInfo[len(self.pussMessageInfo) - 1]
                self.curQuestionId = questionId
                qData = QD.data.get(questionId, {})
                tId = qData.get('templateId', ())
                self.url = ''.join((qData.get('questionLink', ''),
                 '?uid=',
                 str(p.gbId),
                 '?urs=',
                 str(p.roleURS)))
                bonusId = MTD.data.get(tId, {}).get('bonusId', 0)
                items = clientUtils.genItemBonus(bonusId)
                for x in xrange(0, 3):
                    item = getattr(self.widget, 'icon%d' % x, None)
                    if item:
                        item.visible = False

                for i, data in enumerate(items):
                    itemId, itemNum = data
                    icon = getattr(self.widget, 'icon%d' % i, None)
                    if icon:
                        path = uiUtils.getItemIconPath(itemId, uiConst.ICON_SIZE64)
                        icon.icon.fitSize = True
                        icon.icon.loadImage(path)
                        icon.scoreNum.text = str(itemNum)
                        TipManager.addItemTipById(icon, itemId)
                        icon.visible = True

                self.widget.completeBtn.visible = True
                self.widget.rewardTxt.visible = True
                self.widget.minimizeBtn.visible = True
                self.widget.titleTxt.text = gameStrings.QUESTIONNAIRE_TITLE_1
            elif self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_ITEM:
                cData = CID.data.get(self.questionnaireItemId, {})
                self.url = ''.join((cData.get('questionLink', ''),
                 '?uid=',
                 str(p.gbId),
                 '?urs=',
                 str(p.roleURS)))
                for x in xrange(0, 3):
                    item = getattr(self.widget, 'icon%d' % x, None)
                    if item:
                        item.visible = False

                self.widget.completeBtn.visible = False
                self.widget.rewardTxt.visible = False
                self.widget.minimizeBtn.visible = False
                self.widget.titleTxt.text = gameStrings.QUESTIONNAIRE_TITLE_2
            self.startPlay()
            return

    def startPlay(self):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX = int(self.widget.x + self.widget.picture.x)
        self.oldY = int(self.widget.y + self.widget.picture.y)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        CEFModule.loadURL(self.url)
        CEFModule.setEnableGoBack(True)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def onEnterFrame(self, *args):
        x = int(self.widget.x + self.widget.picture.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.picture.y * self.widget.scaleY)
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            CEFModule.setScale(self.widget.scaleX / scale, self.widget.scaleY / scale)

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.url)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def handleCEFRequest(self, request, requestLen):
        if request == self.url or request.find('tianyu.163.com/news/kuang') != -1:
            return
        p = BigWorld.player()
        if request.find('end.html') != -1:
            if self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE:
                self.finishedQuestion()
            elif self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_ITEM:
                pg, ps = p.inv.findItemInPages(self.questionnaireItemId)
                if pg != const.CONT_NO_PAGE and ps != const.CONT_NO_POS:
                    p.cell.useCommonItem(pg, ps, 1, const.RES_KIND_INV)

    def hasBaseData(self):
        if self.widget and (self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE and self.pussMessageInfo or self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_ITEM and self.questionnaireItemId):
            return True
        else:
            return False

    def handleClickCloseBtn(self, *args):
        p = BigWorld.player()
        if self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_PUSH_MESSAGE:
            if self.widget.completeBtn.enabled:
                p.base.finishedQuestion(self.curQuestionId)
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUESTIONNAIRE_CLOSE_SHOW_MSG, '')

                def _confirmCB():
                    p.base.cancelNotifyQuestion(self.curQuestionId)
                    self.removeQuestionMessage()
                    self.hide()
                    self.isFinished = False

                self.uiAdapter.messageBox.showYesNoMsgBox(msg, _confirmCB)
        elif self.questionnairType == uiConst.QUESTIONNAIRE_TYPE_ITEM:
            self.hide()

    def finishedQuestion(self):
        if self.widget:
            self.isFinished = True
            self.widget.completeBtn.enabled = self.isFinished

    def _onCompleteBtnClick(self, *args):
        BigWorld.player().base.finishedQuestion(self.curQuestionId)

    def addQuestionMessage(self, pushQuestionIdList):
        for newId in pushQuestionIdList:
            if newId not in self.pussMessageInfo:
                self.pussMessageInfo.insert(0, newId)

        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_QUESTIONNAIRE, {'click': self.show})
        for qId in self.pussMessageInfo:
            dList = self.uiAdapter.pushMessage.getDataList(uiConst.MESSAGE_TYPE_QUESTIONNAIRE)
            if not self.isHasData(dList, qId):
                self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_QUESTIONNAIRE, {'data': qId})

    def removeAllQuestionMessage(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_QUESTIONNAIRE)

    def removeQuestionMessage(self):
        if self.pussMessageInfo:
            questionId = self.pussMessageInfo.pop()
            self.uiAdapter.pushMessage.removeData(uiConst.MESSAGE_TYPE_QUESTIONNAIRE, {'data': questionId})

    def isHasData(self, dList, qId):
        for item in dList:
            if qId == item.get('data', None):
                return True

        return False
