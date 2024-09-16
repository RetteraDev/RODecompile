#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/daFuWengProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import formula
import const
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from ui import unicode2gbk
from data import chess_box_data as CBD
from data import digong_floor_data as DD
from data import dfw_random_event_data as DRED
CLOCK_START = 1

class DaFuWengProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DaFuWengProxy, self).__init__(uiAdapter)
        self.modelMap = {'startDice': self.onStartDice,
         'backToChessBox': self.onBackToChessBox,
         'initDone': self.onInitDone,
         'getDfwSlot': self.onGetDfwSlot,
         'backToStart': self.onBackToStart,
         'showVideo': self.onShowVideo}
        self.videoRoomId = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WDIGET_DFW_ROOM_VIDEO_DESC, self.hideVideoDesc)

    def reset(self):
        self.med = None
        self.roomMed = None
        self.slotMed = None
        self.canDice = True
        self.expandOnOpen = True
        self.slotTips = {}
        self.performance = gametypes.DAFUWENG_FLOOR_PERFORMANCE_INIT

    def show(self, *args):
        if args and isinstance(args[0], dict):
            self.expandOnOpen = args[0].get('expandOnOpen', True)
        if not self.med:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DA_FU_WENG)
        else:
            self.med.Invoke('refreshView', self.getChessBoxData())
        if self.inRoom():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DA_FU_WENG_ROOM_INFO)
        else:
            self.roomMed = None
            self.performance = gametypes.DAFUWENG_FLOOR_PERFORMANCE_INIT
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DA_FU_WENG_ROOM_INFO)
        p = BigWorld.player()
        if not (hasattr(p, 'chessBoxStatus') and p.chessBoxStatus & 2):
            self.hideSlot()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DA_FU_WENG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DA_FU_WENG_ROOM_INFO)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DA_FU_WENG_SLOTS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WDIGET_DFW_ROOM_VIDEO_DESC)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DA_FU_WENG:
            self.med = mediator
            return self.getChessBoxData()
        if widgetId == uiConst.WIDGET_DA_FU_WENG_ROOM_INFO:
            self.roomMed = mediator
            return self.getRoomeInfo()
        if widgetId == uiConst.WIDGET_DA_FU_WENG_SLOTS:
            self.slotMed = mediator
            gameglobal.rds.sound.playSound(469)
            return self.getRandEventDatas()
        if widgetId == uiConst.WDIGET_DFW_ROOM_VIDEO_DESC:
            roomData = DD.data.get(self.videoRoomId, {})
            initData = {'bg': 'dafuweng/room/%s.dds' % roomData.get('descImg', 1000),
             'videoPath': roomData.get('videoPath', '')}
            return uiUtils.dict2GfxDict(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_DA_FU_WENG_SLOTS:
            self.hideSlot()
        elif widgetId == uiConst.WDIGET_DFW_ROOM_VIDEO_DESC:
            self.hideVideoDesc()

    def showVideoDesc(self, mlgNo):
        self.uiAdapter.unLoadWidget(uiConst.WDIGET_DFW_ROOM_VIDEO_DESC)
        self.videoRoomId = mlgNo
        roomData = DD.data.get(self.videoRoomId, {})
        if roomData:
            self.uiAdapter.loadWidget(uiConst.WDIGET_DFW_ROOM_VIDEO_DESC)

    def hideSlot(self):
        self.slotMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DA_FU_WENG_SLOTS)

    def hideVideoDesc(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WDIGET_DFW_ROOM_VIDEO_DESC)

    def onStartDice(self, *args):
        BigWorld.player().cell.chessBoxDice()

    def onInitDone(self, *args):
        self.updateChessBoxNo()
        if not self.canDice:
            self.med.Invoke('setDiceEnable', GfxValue(self.canDice))

    @ui.callFilter(1)
    def onBackToChessBox(self, *args):
        BigWorld.player().cell.backToBasicFloor()

    @ui.callFilter(1)
    def onGetDfwSlot(self, *args):
        gameglobal.rds.sound.stopSound(469)
        BigWorld.player().cell.getSlotsRandomVal()

    @ui.callFilter(1)
    def onBackToStart(self, *args):
        BigWorld.player().cell.backToSrcChessBox()

    def onShowVideo(self, *args):
        path = unicode2gbk(args[3][0].GetString())
        if path:
            self.uiAdapter.flash.show(path)

    def refreshLine(self):
        if self.med:
            p = BigWorld.player()
            if not self.inRoom() and not p.chessBoxNo[2]:
                lineVisible = True
            else:
                lineVisible = False
            self.med.Invoke('showLine', GfxValue(lineVisible))

    def updateChessBoxNo(self):
        if self.med:
            self.med.Invoke('setChessBoxNo', uiUtils.array2GfxAarry(BigWorld.player().chessBoxNo))
            self.refreshLine()

    def getChessBoxData(self):
        boxData = {'boxData': uiUtils.dict2GfxDict(CBD.data, True),
         'inRoom': self.inRoom() or not self.expandOnOpen}
        if not self.slotTips:
            for slotId in CBD.data.keys():
                floorNo = CBD.data.get(slotId, {}).get('floorNo', 0)
                if floorNo:
                    self.slotTips[slotId] = DD.data.get(floorNo + const.ML_SPACE_NO_DAFUWENG_FLOOR1, {}).get('name', '')

        boxData['slotTips'] = self.slotTips
        return uiUtils.dict2GfxDict(boxData, True)

    def getRoomeInfo(self):
        infoData = {}
        mlNo = formula.getMLNo(BigWorld.player().spaceNo)
        mlData = DD.data.get(mlNo, {})
        infoData['roomName'] = mlData.get('name', '')
        infoData['succDesc'] = mlData.get('succDesc', '')
        infoData['failDesc'] = mlData.get('failDesc', '')
        infoData['helpKey'] = mlData.get('helpKey', 0)
        infoData['desc'] = mlData.get('tgts', '')
        if self.performance in (gametypes.DAFUWENG_FLOOR_PERFORMANCE_FAIL, gametypes.DAFUWENG_FLOOR_PERFORMANCE_SUCC):
            infoData['succ'] = self.performance == gametypes.DAFUWENG_FLOOR_PERFORMANCE_SUCC
        return uiUtils.dict2GfxDict(infoData, True)

    def getRandEventDatas(self):
        eventData = {}
        events = CBD.data.get(BigWorld.player().chessBoxNo[1], {}).get('slots', [])
        for key in events:
            item = DRED.data.get(key, {})
            eventData[events.index(key) + 1] = {'name': item.get('name', ''),
             'desc': item.get('desc', ''),
             'icon': 'dafuweng/%s.dds' % item.get('icon', 0)}

        return uiUtils.dict2GfxDict(eventData, True)

    def updateFloorPerformance(self, performance):
        self.performance = performance
        if performance in (gametypes.DAFUWENG_FLOOR_PERFORMANCE_FAIL, gametypes.DAFUWENG_FLOOR_PERFORMANCE_SUCC):
            if self.roomMed:
                self.roomMed.Invoke('setResult', GfxValue(performance == gametypes.DAFUWENG_FLOOR_PERFORMANCE_SUCC))

    def updateChessBoxStatus(self, canDice, canSlots):
        self.canDice = canDice
        if self.med:
            self.med.Invoke('setDiceEnable', GfxValue(self.canDice))
        if canSlots:
            if self.slotMed:
                self.hideSlot()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DA_FU_WENG_SLOTS)

    def setSlotsVal(self, index):
        if self.slotMed:
            events = CBD.data.get(BigWorld.player().chessBoxNo[1], {}).get('slots', [])
            if index in events:
                uiIndex = events.index(index) + 1
            else:
                uiIndex = 1
            self.slotMed.Invoke('setSlotVal', GfxValue(uiIndex))

    def inRoom(self):
        spaceNo = BigWorld.player().spaceNo
        return formula.getMLGNo(spaceNo) == const.ML_SPACE_NO_DAFUWENG and formula.getMLFloorNo(spaceNo) > 0

    def showDiceResult(self, nums):
        if self.med:
            self.med.Invoke('setDiceResult', uiUtils.array2GfxAarry(nums))

    def showClockAni(self, time):
        gameglobal.rds.ui.arena.openArenaMsg()
        BigWorld.player().addTimerCount(CLOCK_START, time)

    def closeClockAni(self, time):
        gameglobal.rds.ui.arena.closeArenaCountDown()
