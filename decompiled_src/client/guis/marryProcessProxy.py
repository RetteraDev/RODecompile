#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryProcessProxy.o
import BigWorld
from Scaleform import GfxValue
import utils
import uiUtils
import gametypes
import gameglobal
import uiConst
import datetime
import time
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from helpers import navigator
from asObject import ASObject
from asObject import ASUtils
from data import marriage_config_data as MCD
NODE_NUM_MAX = 5
PROCESS_DATA = {gametypes.MARRIAGE_STAGE_PREPARE: (4, 1),
 gametypes.MARRIAGE_STAGE_START: (28, 2),
 gametypes.MARRIAGE_STAGE_ENTER_HALL: (50, 3),
 gametypes.MARRIAGE_STAGE_PARADE: (74, 4),
 gametypes.MARRIAGE_STAGE_ENTER_RES: (96, 5)}
NORMAL_NAVIGATE_FIND_POS = 1
FING_LEADER_BY_SCHOOL = 2

class MarryProcessProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryProcessProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.timer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_PROCESS:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_PROCESS)
        p = BigWorld.player()
        if p and p.marriageStage in (gametypes.MARRIAGE_STAGE_PREPARE,
         gametypes.MARRIAGE_STAGE_START,
         gametypes.MARRIAGE_STAGE_ENTER_HALL,
         gametypes.MARRIAGE_STAGE_PARADE,
         gametypes.MARRIAGE_STAGE_ENTER_RES):
            p.addMarriageProgressMessage()

    def show(self):
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_PROCESS)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.updateTime()

    def cancelTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.hasBaseData():
            self.updateTimeInfo()
            self.cancelTimer()
            self.timer = BigWorld.callback(1, self.updateTime)

    def updateTimeInfo(self):
        p = BigWorld.player()
        now = utils.getNow()
        if p.marriageBegineTimestamp:
            if now < self.getFakeBeginTime():
                self.widget.countDownBeginMc.visible = True
                self.widget.processTime.visible = False
                self.widget.desc.visible = False
                self.widget.processMc.visible = False
                self.widget.gotoBtn.visible = False
                t = self.getFakeBeginTime() - now
                t = max(0, t)
                minute = t / 60
                second = t % 60
                formatTime = '%02d:%02d' % (minute, second)
                self.widget.countDownBeginMc.beginTime.text = formatTime
            else:
                self.widget.countDownBeginMc.visible = False
                self.widget.processTime.visible = True
                self.widget.desc.visible = True
                self.widget.processMc.visible = True
                self.widget.gotoBtn.visible = True
                hourNum = 1
                if p.marriageType == gametypes.MARRIAGE_TYPE_PACKAGE:
                    hourNum = 1
                elif p.marriageType == gametypes.MARRIAGE_TYPE_GREAT:
                    hourNum = 2
                t = self.getFakeBeginTime() + const.TIME_INTERVAL_HOUR * hourNum + const.TIME_INTERVAL_MINUTE * 5 - now
                t = max(0, t)
                minute = t / 60
                second = t % 60
                formatTime = '%02d:%02d' % (minute, second)
                self.widget.processTime.htmlText = gameStrings.MARRIAGE_OVER_COUNT_DOWN % (formatTime,)
                curValue, nodeNum = PROCESS_DATA.get(p.marriageStage, (0, 0))
                self.widget.processMc.currentValue = curValue
                for i in xrange(0, NODE_NUM_MAX):
                    nodeMc = getattr(self.widget.processMc, 'nodeMc' + str(i))
                    if nodeMc:
                        if i < nodeNum:
                            nodeMc.node.visible = True
                        else:
                            nodeMc.node.visible = False

                marriageStageData = MCD.data.get('marriageStageData', {})
                desc, stageType, stageData = marriageStageData.get(p.marriageStage, ('', 0, 0))
                self.widget.desc.htmlText = desc
                if stageType:
                    self.widget.gotoBtn.visible = True
                else:
                    self.widget.gotoBtn.visible = False
                if t == 0:
                    self.hide()

    def getFakeBeginTime(self):
        p = BigWorld.player()
        return p.marriageBegineTimestamp - const.TIME_INTERVAL_MINUTE * 5

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def _onGotoBtnClick(self, e):
        if self.hasBaseData():
            t = e.target
            p = BigWorld.player()
            marriageStageData = MCD.data.get('marriageStageData', {})
            desc, stageType, stageData = marriageStageData.get(p.marriageStage, ('', 0, 0))
            if stageType == NORMAL_NAVIGATE_FIND_POS:
                if stageData:
                    x, y, z, mapId = stageData
                    navigator.getNav().pathFinding((x,
                     y,
                     z,
                     mapId))
            elif stageType == FING_LEADER_BY_SCHOOL:
                p.cell.queryMarriageWifeSchool()
