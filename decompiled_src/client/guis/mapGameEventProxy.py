#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameEventProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
import events
import clientUtils
import uiUtils
import mapGameCommon
from uiTabProxy import UIProxy
from asObject import ASObject
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
from data import map_game_event_data as MGED
MAX_TAB_NUM = 5
MAX_BONUS_NUM = 4

class MapGameEventProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameEventProxy, self).__init__(uiAdapter)
        self.eventList = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_EVENT, self.hide)

    def reset(self):
        super(MapGameEventProxy, self).reset()
        self.widget = None
        self.selectTab = 0
        self.stage = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_EVENT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        super(MapGameEventProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_EVENT)

    def show(self):
        if mapGameCommon.checkVersion() != uiConst.MAP_GAME_VERSION_2:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_EVENT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        posX = 29
        eventContent = MGCD.data.get('eventContent', {})
        eventTabList = eventContent.keys()
        eventTabNameList = MGCD.data.get('eventTabNameList', [])
        self.stage = gameglobal.rds.ui.mapGameMapV2.getStage()
        tabNum = min(MAX_TAB_NUM, len(eventTabNameList))
        if MGCD.data.get('isSecondBossMode', False):
            tabNum = self.stage + 1
        for i in xrange(MAX_TAB_NUM):
            btn = self.widget.getChildByName('tab%d' % i)
            btn.visible = False
            if i in eventTabList:
                btn.x = posX
                posX += 69
                btn.index = i
                btn.label = eventTabNameList[i]
                btn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
                btn.visible = i < tabNum

        self.widget.eventList.lableFunction = self.itemFunction
        self.widget.eventList.itemRenderer = 'MapGameEvent_eventItem'
        self.widget.eventList.dataArray = []

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.swapPanelToFront()
        for i in xrange(MAX_TAB_NUM):
            tabBtn = self.widget.getChildByName('tab%d' % i)
            tabBtn.selected = i == self.selectTab

        self.refreshEventList()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if not itemData:
            itemMc.visible = False
            return
        itemMc.title.text = itemData.title
        itemMc.desc.text = itemData.desc
        if MGCD.data.get('isCampMode', False):
            itemMc.camp1.visible = True
            itemMc.camp2.visible = True
            itemMc.camp1.title.text = itemData.campName1
            itemMc.camp1.flag.gotoAndStop(itemData.campState1)
            itemMc.camp2.title.text = itemData.campName2
            itemMc.camp2.flag.gotoAndStop(itemData.campState2)
        else:
            itemMc.camp1.visible = False
            itemMc.camp2.visible = False
        bonusList = itemData.bonusList
        for i in xrange(MAX_BONUS_NUM):
            bonusMc = itemMc.getChildByName('slot%d' % i)
            if i < len(bonusList):
                bonusMc.visible = True
                bonusMc.setItemSlotData(uiUtils.getGfxItemById(bonusList[i][0], bonusList[i][1]))
                bonusMc.dragable = False
            else:
                bonusMc.visible = False

        rewardId = itemData.rewardId
        eventInfo = MGED.data.get(rewardId, 0)
        eventsIds = eventInfo.get('eventList', ())
        receivedEvents = BigWorld.player().mapGameEventReward if BigWorld.player().mapGameEventReward else []
        isFinished = not [ False for id in eventsIds if id not in self.eventList ]
        if isFinished:
            itemMc.receiveState.visible = True
            if rewardId not in receivedEvents:
                itemMc.receiveState.gotoAndStop('canReceive')
                itemMc.receiveState.btn.eventId = rewardId
                itemMc.receiveState.btn.addEventListener(events.BUTTON_CLICK, self.handleReceiveBtnClick, False, 0, True)
            else:
                itemMc.receiveState.gotoAndStop('received')
        else:
            itemMc.receiveState.visible = True
            itemMc.receiveState.gotoAndStop('noReceive')

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.selectTab = e.currentTarget.index
        self.refreshInfo()

    def handleReceiveBtnClick(self, *args):
        e = ASObject(args[3][0])
        eventId = int(e.currentTarget.eventId)
        BigWorld.player().cell.getMapGameEventReward(eventId)

    def refreshEventList(self):
        if not self.widget:
            return
        configData = MGCD.data
        eventContent = configData.get('eventContent', {})
        itemList = eventContent.get(self.selectTab, [])
        campNameDict = configData.get('campNameDict', {})
        eventArray = []
        for itemId in itemList:
            eventInfo = {}
            data = MGED.data.get(itemId, {})
            eventInfo['rewardId'] = itemId
            eventInfo['title'] = data.get('title', '')
            eventInfo['desc'] = data.get('desc', '')
            if MGCD.data.get('isCampMode', False):
                eventInfo['campName1'] = campNameDict.get(1, '')
                eventInfo['campName2'] = campNameDict.get(2, '')
                eventList = data.get('eventList', [0, 0])
                if eventList[0] in self.eventList:
                    eventInfo['campState1'] = 'success'
                else:
                    eventInfo['campState1'] = 'fail'
                if eventList[1] in self.eventList:
                    eventInfo['campState2'] = 'success'
                else:
                    eventInfo['campState2'] = 'fail'
            eventInfo['bonusList'] = clientUtils.genItemBonus(data.get('bonusId', 0))
            eventArray.append(eventInfo)

        self.widget.eventList.dataArray = eventArray
        self.widget.eventList.validateNow()

    def setFinishedEvent(self, eventList):
        self.eventList = eventList
        self.refreshInfo()
