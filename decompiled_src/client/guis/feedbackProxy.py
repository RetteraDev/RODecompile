#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/feedbackProxy.o
import BigWorld
import gameglobal
import clientcom
from Scaleform import GfxValue
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from data import feedback_data as FD

class FeedbackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FeedbackProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeClick': self.onCloseClick,
         'feedbackClick': self.onFeedbackClick,
         'getFeedbackInfo': self.onGetFeedbackInfo,
         'feedbackIconClick': self.onFeedbackIconClick,
         'loginOnDisable': self.onLoginOnDisable,
         'getLoginOnDisable': self.onGetLoginOnDisable}
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FEEDBACK, {'click': self.clickPushIcon})
        self.callbackId = None
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FEEDBACK_ICON:
            self.mediator = mediator
            self.mediator.Invoke('setVisible', GfxValue(False))

    def reset(self):
        self.isShow = False
        self.isIconShow = False
        self.loginOnDisable = False
        self.callbackDone = False
        if self.callbackId:
            BigWorld.cancelCallback(self.callbackId)
            self.callbackId = None
        self.strIndex = 0

    def onCloseClick(self, *arg):
        self.closeFeedbackWidget()
        if self.loginOnDisable:
            self.closeIcon()
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FEEDBACK)

    def onLoginOnDisable(self, *arg):
        self.loginOnDisable = arg[3][0].GetBool()

    def onGetLoginOnDisable(self, *arg):
        return GfxValue(self.loginOnDisable)

    def clickPushIcon(self):
        self.showFeedbackWidget()

    def onFeedbackClick(self, *arg):
        p = BigWorld.player()
        triggerLvs = FD.data.keys()
        url = FD.data[triggerLvs[self.strIndex]]['url'] + '?uid=' + str(p.gbId) + '?urs=' + gameglobal.rds.loginUserName
        clientcom.openFeedbackUrl(url)
        minIndex = 0
        for index, lv in enumerate(triggerLvs):
            if p.lv < lv:
                minIndex = index - 1
                break

        lv = triggerLvs[minIndex]
        p.cell.setLvTriggerFlag(lv, True)
        self.closeIcon()
        self.closeFeedbackWidget()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FEEDBACK)

    def onGetFeedbackInfo(self, *arg):
        p = BigWorld.player()
        triggerLvs = FD.data.keys()
        self.strIndex = 0
        isFound = False
        for index, lv in enumerate(triggerLvs):
            if lv == p.lv:
                self.strIndex = index
                isFound = True
                break
            elif lv > p.lv:
                self.strIndex = index - 1
                isFound = True
                break

        if not isFound:
            self.strIndex = len(triggerLvs) - 1
        id = triggerLvs[self.strIndex]
        ret = self.movie.CreateObject()
        ret.SetMember('title', GfxValue(gbk2unicode(FD.data[id].get('title', ''))))
        ret.SetMember('desc', GfxValue(gbk2unicode(FD.data[id].get('desc', ''))))
        return ret

    def showFeedback(self):
        p = BigWorld.player()
        self.showPushMessage()
        if self.loginOnDisable:
            return
        if p.inFuben():
            return
        self.showFeedbackWidget()
        self.showIcon()

    def showPushMessage(self):
        self.callbackDone = True
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_FEEDBACK)

    def showFeedbackWidget(self):
        pass

    def closeFeedbackWidget(self):
        self.isShow = False

    def showIcon(self):
        if self.isIconShow:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FEEDBACK_ICON)
        self.isIconShow = True

    def closeIcon(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FEEDBACK_ICON)
        self.isIconShow = False

    def onFeedbackIconClick(self, *arg):
        self.showFeedbackWidget()

    def startCallBack(self):
        if self.callbackId:
            BigWorld.cancelCallback(self.callbackId)
        if self.callbackDone:
            return
        self.callbackId = BigWorld.callback(60, self.showPushMessage)
