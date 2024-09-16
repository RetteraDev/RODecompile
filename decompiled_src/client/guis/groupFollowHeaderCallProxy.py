#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupFollowHeaderCallProxy.o
import BigWorld
import gameglobal
import gamelog
import clientUtils
import gametypes
import clientcom
import formula
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from guis.asObject import TipManager
from gameStrings import gameStrings
from appSetting import Obj as AppSettings
from data import sys_config_data as SCD
from data import fb_data as FD
from cdata import game_msg_def_data as GMDD
COUNTDOWN_CHECK_TIME = 1
PROCESS_RATE = 10

class GroupFollowHeaderCallProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupFollowHeaderCallProxy, self).__init__(uiAdapter)
        self.widget = None
        self.countDown = 0
        self.countDownCallBack = None
        self.savePath = 'conf/ui/GroupFollowHeaderCall/isAutoAccept'
        self.isAutoAccept = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUPFOLLOWCALL, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUPFOLLOWCALL:
            self.widget = widget
            self.initUI()

    def show(self):
        if self.readConfigData():
            if self.checkOpenPhase():
                return
            p = BigWorld.player()
            p.cell.applyGroupFollow()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GROUPFOLLOWCALL)

    def clearWidget(self):
        if self.countDownCallBack:
            BigWorld.cancelCallback(self.countDownCallBack)
            self.countDownCallBack = None
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPFOLLOWCALL)

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        if self.isAutoAccept == None:
            self.isAutoAccept = self.readConfigData()
        self.countDown = 0

    def initState(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.mainMc.cancelBtn]
        self.widget.mainMc.okBtn.addEventListener(events.BUTTON_CLICK, self.handleClickOkBtn, False, 0, True)
        self.widget.mainMc.overtimeBox.visible = False
        self.widget.mainMc.overtimeBox.selected = False
        self.widget.mainMc.loading.isProcessing = False
        timeLimit = SCD.data.get('groupFollowAutoAcceptTime', 30)
        self.widget.mainMc.loading.maxValue = timeLimit * PROCESS_RATE
        self.widget.mainMc.loading.currentValue = timeLimit * PROCESS_RATE
        self.countDownFunc()
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            pass

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def countDownFunc(self):
        if self.hasBaseData():
            if self.countDownCallBack:
                BigWorld.cancelCallback(self.countDownCallBack)
                self.countDownCallBack = None
            self.countDown += 1
            timeLimit = SCD.data.get('groupFollowAutoAcceptTime', 30)
            curValue = (timeLimit - self.countDown) * PROCESS_RATE
            self.widget.mainMc.loading.currentValue = curValue
            if self.countDown > timeLimit:
                self.countDown = 0
                if self.widget.mainMc.overtimeBox.selected:
                    p = BigWorld.player()
                    p.cell.applyGroupFollow()
                self.hide()
                return
            self.countDownCallBack = BigWorld.callback(COUNTDOWN_CHECK_TIME, self.countDownFunc)

    def readConfigData(self):
        bAuto = AppSettings.get(self.savePath, 1)
        return bAuto

    def writeConfigData(self):
        if self.hasBaseData():
            self.isAutoAccept = int(self.widget.mainMc.overtimeBox.selected)
            AppSettings[self.savePath] = self.isAutoAccept

    def handleClickOkBtn(self, *arg):
        if self.countDownCallBack:
            BigWorld.cancelCallback(self.countDownCallBack)
            self.countDownCallBack = None
        if self.checkOpenPhase():
            return
        else:
            p = BigWorld.player()
            p.cell.applyGroupFollow()
            self.hide()
            return

    def checkOpenPhase(self):
        p = BigWorld.player()
        fbList = getattr(p, 'fbStatusList', [])
        fbList = self.uiAdapter.phaseFuben.filterFuben(fbList)
        hGbId = getattr(p, 'headerGbId', 0)
        headerSpaceNo = p.membersPos.get(hGbId, (0,))[0]
        fbNo = formula.getFubenNo(headerSpaceNo)
        name = formula.whatLocationName(headerSpaceNo, '', includeMLInfo=True)
        pFbNo = formula.getFubenNo(p.spaceNo)
        if hGbId and fbList and p.spaceNo != headerSpaceNo and not pFbNo:
            if fbNo:
                fbInfo = FD.data.get(fbNo, {})
                if fbInfo.get('isPushIcon', None):
                    self.uiAdapter.phaseFuben.openPhaseListByGroupFollow()
                    p.showGameMsg(GMDD.data.GROUPFOLLOW_ENTERFUBEN_MESSAGE, (name,))
                    self.hide()
                    return True
        return False
