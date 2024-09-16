#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldQueueProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from callbackHelper import Functor
from uiProxy import UIProxy
from data import wing_world_config_data as WWCD
from data import wing_world_city_data as WWCTD
from gamestrings import gameStrings
from commonWingWorld import WWArmyPostVal
from guis import wingWorldStrategyProxy
import wingWorldUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from callbackHelper import Functor
QUEUE_TYPE_DEFAULT = 0
QUEUE_TYPE_V2_SIGN = 1
QUEUE_TYPE_V2_QUEUE = 2
QUEUE_V2_TYPES = (QUEUE_TYPE_V2_SIGN, QUEUE_TYPE_V2_QUEUE)

class WingWorldQueueProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldQueueProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.cityId = 0
        self.queueCnt = 0
        self.queueType = 0

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_QUEUE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_QUEUE)

    def show(self, cityId, queueCnt, queueType = QUEUE_TYPE_DEFAULT, isOpen = True):
        if queueType in QUEUE_V2_TYPES:
            if not gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
                return
        elif gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
            return
        self.cityId = cityId
        self.queueCnt = queueCnt if queueCnt >= 0 else self.queueCnt
        self.queueType = queueType
        if not self.widget and isOpen:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_QUEUE)
        else:
            self.refreshInfo()

    def setQueueNumCallBack(self, queueNum):
        if not self.widget:
            return
        else:
            self.queueCnt = queueNum if queueNum >= 0 else self.queueCnt
            self.refreshInfo()
            self.queueSetCallBack = None
            return

    def isQueueV2Type(self):
        return self.queueType in QUEUE_V2_TYPES

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        cityName = WWCTD.data.get(self.cityId, {}).get('name', '')
        if self.queueType == QUEUE_TYPE_DEFAULT:
            self.widget.mainContent.text = WWCD.data.get('wingWorldQueue', '%s') % cityName
            self.widget.counterTxt.text = WWCD.data.get('wingWorldWaitCnt', '%s') % (self.queueCnt if self.queueCnt > 0 else '-')
            self.widget.cancelBtn.label = gameStrings.WING_WORLD_QUIT_QUEUE
            self.widget.title.textField.text = gameStrings.WING_WORLD_QUEUE_TITLE
        elif self.queueType == QUEUE_TYPE_V2_SIGN:
            self.widget.mainContent.text = WWCD.data.get('wingWorldSignWaitText', gameStrings.WING_WORLD_SING_QUEUE) % cityName
            self.widget.counterTxt.text = WWCD.data.get('wingWorldSignWaitCntText', '%s') % ''
            self.widget.cancelBtn.label = gameStrings.WING_WORLD_QUIT_SIGN
            self.widget.title.textField.text = gameStrings.WING_WORLD_SIGN_TITLE
        else:
            p = BigWorld.player()
            self.widget.mainContent.text = WWCD.data.get('wingWorldV2QueueWaitText', gameStrings.WING_WORLD_SING_QUEUE) % cityName
            if getattr(p, 'wingWorldPostId', 0) and p.wingWorldPostId <= wingWorldStrategyProxy.WING_WORLD_CAMP_LEADER_POST_MAX_ID:
                self.widget.counterTxt.text = WWCD.data.get('wingWorldV2QueueGeneralWaitCntText', '')
            else:
                self.widget.counterTxt.text = WWCD.data.get('wingWorldV2QueueWaitCntText', WWCD.data.get('wingWorldWaitCnt', '%s')) % (self.queueCnt if self.queueCnt > 0 else '-')
            self.widget.cancelBtn.label = gameStrings.WING_WORLD_QUIT_QUEUE
            self.widget.title.textField.text = gameStrings.WING_WORLD_QUEUE_TITLE

    def onWingWorldWarCitySyncQueueInfo(self, queueCnt):
        if self.queueType == QUEUE_TYPE_DEFAULT:
            self.queueCnt = queueCnt
            self.refreshInfo()

    def handleCloseBtnClick(self, *args):
        self.hide()
        self.addPushMsg()

    def addPushMsg(self):
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_QUEUE)
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_QUEUE, {'click': self.onPushMsgClick})

    def onPushMsgClick(self):
        self.show(self.cityId, self.queueCnt, self.queueType)

    def removePushMsg(self):
        self.timer = None
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_QUEUE)

    def handleCancelBtnClick(self, *args):
        if not self.cityId:
            return
        if self.queueType in QUEUE_V2_TYPES:
            BigWorld.player().showConfirmQuitWingWorldQueueV2()
        else:
            self.hide()
            self.removePushMsg()
            BigWorld.player().cell.cancelTeleportToWingWarCityQueue(self.cityId)
        print 'jbx:self.hide'
