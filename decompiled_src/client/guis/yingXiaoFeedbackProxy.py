#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yingXiaoFeedbackProxy.o
import BigWorld
import gameglobal
import clientcom
import clientUtils
from Scaleform import GfxValue
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import ying_xiao_feedback_data as YXFD

class YingXiaoFeedbackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YingXiaoFeedbackProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeClick': self.onCloseClick,
         'feedbackClick': self.onFeedbackClick,
         'getFeedbackInfo': self.onGetFeedbackInfo,
         'loginOnDisable': self.onLoginOnDisable,
         'getLoginOnDisable': self.onGetLoginOnDisable}
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK, {'click': self.clickPushIcon})
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        pass

    def reset(self):
        self.isShow = False
        self.loginOnDisable = False

    def clearWidget(self):
        self.closeFeedbackWidget()

    def onCloseClick(self, *arg):
        feedbackId = int(arg[3][0].GetNumber())
        comId = int(arg[3][1].GetNumber())
        self.closeFeedbackWidget()
        self.removePushMsg(feedbackId=feedbackId, comId=comId)

    def onLoginOnDisable(self, *arg):
        self.loginOnDisable = arg[3][0].GetBool()

    def onGetLoginOnDisable(self, *arg):
        return GfxValue(self.loginOnDisable)

    def clickPushIcon(self):
        self.showFeedbackWidget()

    def onFeedbackClick(self, *arg):
        feedbackId = int(arg[3][0].GetNumber())
        comId = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        url = YXFD.data[feedbackId]['url'] + '?uid=' + str(p.gbId) + '?urs=' + gameglobal.rds.loginUserName
        clientcom.openFeedbackUrl(url)
        self.closeFeedbackWidget()
        self.removePushMsg(feedbackId=feedbackId, comId=comId)
        bonusId = YXFD.data.get(feedbackId, {}).get('bonusId', 0)
        if bonusId:
            p.onFeedbackReward(comId)
            p.cell.feedbackReward(feedbackId, bonusId, comId)

    def removePushMsg(self, isForce = False, feedbackId = 0, comId = 0):
        if isForce or self.loginOnDisable:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK)
        else:
            dataList = tuple(gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK))
            for item in dataList:
                if item['data'][0] == feedbackId and item['data'][1] == comId:
                    gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK, {'data': (feedbackId, comId)})

    def onGetFeedbackInfo(self, *arg):
        feedbackData = YXFD.data
        if not feedbackData.has_key(self.feedbackId):
            return uiUtils.array2GfxAarry({})
        bonusId = feedbackData[self.feedbackId].get('bonusId', 0)
        itemBonus = clientUtils.genItemBonus(bonusId)
        feedbackInfo = {}
        feedbackInfo['title'] = feedbackData[self.feedbackId].get('title', '')
        feedbackInfo['desc'] = feedbackData[self.feedbackId].get('desc', '')
        icons = []
        for itemId, itemNum in itemBonus:
            iconPath = uiUtils.getItemIconFile40(itemId)
            icons.append({'iconPath': iconPath,
             'itemId': itemId,
             'count': itemNum})

        feedbackInfo['icons'] = icons
        feedbackInfo['feedbackId'] = self.feedbackId
        feedbackInfo['comId'] = self.comId
        return uiUtils.dict2GfxDict(feedbackInfo, True)

    def showPushMessage(self, feedbackId, comId):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK, {'data': (feedbackId, comId)})

    def showFeedbackWidget(self):
        if not self.isShow:
            self.feedbackId, self.comId = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK).get('data', (0, 0))
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YING_XIAO_FEEDBACK)

    def closeFeedbackWidget(self):
        self.isShow = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YING_XIAO_FEEDBACK)
