#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pushActivityProxy.o
import BigWorld
import const
import uiConst
import events
import gameglobal
import ui
from callbackHelper import Functor
from uiProxy import UIProxy
from guis.asObject import ASObject
ICON_OFFSET = 55
WING_WORLD_BOSS_TYPE = 'wingWorldBoss'

class PushActivityProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PushActivityProxy, self).__init__(uiAdapter)
        self.widget = None
        self.pushActivityData = {}
        self.timeoutHandles = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUSHACTIVITY, self.hide)

    def reset(self):
        for handles in self.timeoutHandles.itervalues():
            BigWorld.cancelCallback(handles)

        self.timeoutHandles = {}

    def clearAll(self):
        self.pushActivityData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUSHACTIVITY:
            self.widget = widget
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUSHACTIVITY)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUSHACTIVITY)
        else:
            self.refreshInfo()

    def addPushActivityIcon(self, activityType, data):
        curTime = BigWorld.player().getServerTime()
        endTime = data.get('endTime', curTime)
        if curTime >= endTime:
            return
        data['activityType'] = activityType
        self.pushActivityData[activityType] = data
        self.show()
        self.addTimeoutCallback(activityType)

    def removePushActivityIcon(self, activityType):
        if activityType in self.pushActivityData:
            del self.pushActivityData[activityType]
        if activityType in self.timeoutHandles:
            del self.timeoutHandles[activityType]
        if not self.widget:
            return
        icon = getattr(self.widget, 'icon%s' % activityType)
        self.widget.removeChild(icon)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.pushActivityData:
            self.hide()
            return
        if not self.widget:
            return
        showData = sorted(self.pushActivityData.itervalues(), key=lambda d: d.get('time1', 0))
        for idx, data in enumerate(showData):
            iconMc = getattr(self.widget, 'icon%s' % data['activityType'])
            if not iconMc:
                iconMc = self.widget.getInstByClsName('PushActivity_ActivityPushIcon')
                self.widget.addChild(iconMc)
            iconMc.x = ICON_OFFSET * (idx - 1)
            iconMc.y = 0
            iconMc.show(data)
            iconMc.addEventListener(events.MOUSE_CLICK, self.onPushIconClick, False, 0, True)

    def addTimeoutCallback(self, activityType):
        p = BigWorld.player()
        curTime = p.getServerTime()
        endTime = self.pushActivityData.get(activityType, {}).get('endTime', curTime)
        t = endTime - curTime
        activityType in self.timeoutHandles and BigWorld.cancelCallback(self.timeoutHandles[activityType])
        self.timeoutHandles[activityType] = BigWorld.callback(t, Functor(self.removePushActivityIcon, activityType))

    def onPushIconClick(self, *args):
        e = ASObject(args[3][0])
        acitivityType = e.currentTarget.activityType
        clickFunc = self.pushActivityData.get(acitivityType, {}).get('clickFunc')
        clickFunc and clickFunc()

    def addWingWorldBossPush(self, createWWBossTime, destroyWWBossTime):
        pushActivityData = {'clickFunc': self.clickWingWorldBossActivityPush,
         'stageText0': 'time',
         'stageText1': 'time',
         'time1': createWWBossTime,
         'time2': destroyWWBossTime,
         'endTime': destroyWWBossTime}
        self.addPushActivityIcon('wingWorldBoss', pushActivityData)

    def updateWingWorldBossPush(self, createWWBossTime, destroyBossTime, destroyLineTime):
        pushActivityData = {'clickFunc': self.clickWingWorldBossActivityPush,
         'stageText0': 'time',
         'stageText1': 'time',
         'stageText2': 'time',
         'time1': createWWBossTime,
         'time2': destroyBossTime,
         'time3': destroyLineTime,
         'endTime': destroyLineTime}
        self.addPushActivityIcon('wingWorldBoss', pushActivityData)

    @ui.callFilter(5)
    def clickWingWorldBossActivityPush(self):
        enterBaseMLNo = getattr(BigWorld.player(), 'wwBossMlgNo', 0)
        enterBaseMLNo and gameglobal.rds.ui.diGong.show(enterBaseMlNo=enterBaseMLNo)
