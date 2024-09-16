#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldEventProxy.o
import BigWorld
import gameglobal
import gametypes
import const
import gamelog
import uiConst
from Queue import Queue
from guis.asObject import ASUtils
from uiProxy import UIProxy
from data import wing_city_building_data as WCBD

class WingWorldEventProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldEventProxy, self).__init__(uiAdapter)
        self.widget = None
        self.eventQueue = Queue()
        self.currentData = None
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_EVENT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_EVENT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_EVENT)

    def initUI(self):
        self.widget.mainMc.visible = False

    def setIcon(self, *args):
        campIndex = self.currentData[1]
        self.widget.mainMc.icon.gotoAndStop(uiConst.WING_WORLD_EVENT_TO_FRAME_NAME[self.currentData[0]][0])
        self.widget.mainMc.icon.content.gotoAndStop('camp%d' % campIndex)
        gamelog.info('jbx:setIcon', uiConst.WING_WORLD_EVENT_TO_FRAME_NAME[self.currentData[0]][0])

    def setTxtLabel(self, *args):
        self.widget.mainMc.txtLabel.gotoAndStop(uiConst.WING_WORLD_EVENT_TO_FRAME_NAME[self.currentData[0]][1])
        gamelog.info('jbx:setTxtLabel', uiConst.WING_WORLD_EVENT_TO_FRAME_NAME[self.currentData[0]][1])

    def refreshInfo(self):
        if not self.widget:
            return
        if self.eventQueue.qsize():
            self.widget.mainMc.visible = True
            self.currentData = self.eventQueue.get()
            gamelog.info('jbx:setCurrentData', self.currentData)
            self.widget.gotoAndPlay('win' if self.currentData[2] else 'fail')
            self.uiAdapter.littleMap.showWingWorldWarEvent(self.currentData[3])
            self.widget.mainMc.gotoAndPlay(1)
            ASUtils.callbackAtFrame(self.widget.mainMc, 11, self.setIcon)
            ASUtils.callbackAtFrame(self.widget.mainMc, 14, self.setTxtLabel)
            ASUtils.callbackAtFrame(self.widget.mainMc, self.widget.mainMc.totalFrames, self.endFrameCallback)
            BigWorld.callback(3, self.refreshInfo)
            gameglobal.rds.sound.playSound(6187)
        else:
            self.widget.mainMc.visible = False

    def endFrameCallback(self, *args):
        if self.widget:
            self.widget.mainMc.visible = False

    def addWingWorldEvents(self, cityId, eventId, args):
        gamelog.info('jbx:addWingWorldEvents', cityId, eventId, args)
        self.processEvent(cityId, eventId, args)
        if not self.widget or self.widget.mainMc.visible:
            return
        self.refreshInfo()

    def processEvent(self, cityId, eventId, args):
        p = BigWorld.player()
        selfHostId = p.wingWorldCamp if p.isWingWorldCampMode() else p.getOriginHostId()
        campIndex = 0
        cityOwnerHostId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId
        eventHostId = 0
        isWin = True
        entNo = 0
        if eventId == gametypes.WING_WORLD_WAR_EVENT_BUILDING_CHANGE_HANDS:
            entNo, buildingId, oldOwnerHostId, ownerHostId = args
            if oldOwnerHostId and not ownerHostId:
                if oldOwnerHostId != selfHostId:
                    return
            buildingType = WCBD.data.get(buildingId, {}).get('buildingType', 0)
            if not ownerHostId:
                campIndex = p.wingWorldMiniMap.attendHost2ColorIdx.get(oldOwnerHostId, 1)
                eventHostId = oldOwnerHostId
            else:
                campIndex = p.wingWorldMiniMap.attendHost2ColorIdx.get(ownerHostId, 1)
                eventHostId = ownerHostId
            if buildingType == gametypes.WING_CITY_BUILDING_TYPE_STONE:
                iscore = WCBD.data.get(buildingId, {}).get('core', 0)
                if iscore:
                    if not ownerHostId:
                        eventType = uiConst.WING_WORLD_EVENT_MAIN_STONE_LOST
                        isWin = False
                    else:
                        eventType = uiConst.WING_WORLD_EVENT_MAIN_STONE_OCCUPY
                        isWin = True
                elif not ownerHostId:
                    eventType = uiConst.WING_WORLD_EVENT_SECOND_STONE_LOST
                    isWin = False
                else:
                    eventType = uiConst.WING_WORLD_EVENT_SECOND_STONE_OCCUPY
                    isWin = True
            elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD:
                if not ownerHostId:
                    eventType = uiConst.WING_WORLD_EVENT_RELIVE_BOARD_LOST
                    isWin = False
                else:
                    eventType = uiConst.WING_WORLD_EVENT_RELIVE_BOARD_OCCUPY
                    isWin = True
            else:
                gamelog.error('jbx: unsupport buildType', buildingType)
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_AIR_STONE_ENABLE:
            campIndex = 1
            eventHostId = selfHostId
            eventType = uiConst.WING_WORLD_EVENT_AIR_STONE_RECOVER
            isWin = True
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_AIR_STONE_DISABLE:
            campIndex = 1
            eventHostId = selfHostId
            eventType = uiConst.WING_WORLD_EVENT_AIR_STONE_LOST
            isWin = False
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_AIR_DEFENSE_ENABLE:
            campIndex = 1
            eventHostId = selfHostId
            eventType = uiConst.WING_WORLD_EVENT_AIR_DEFENCE_ACTIVATE
            isWin = True
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_AIR_DEFENSE_DISABLE:
            campIndex = 1
            eventHostId = selfHostId
            eventType = uiConst.WING_WORLD_EVENT_AIR_DEFENCE_DISABLE
            isWin = False
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_GATE_DESTROY:
            entNo, attackerHostId = args
            if selfHostId == cityOwnerHostId:
                campIndex = 1
                eventHostId = selfHostId
                eventType = uiConst.WING_WORLD_EVENT_GATE_LOST
                isWin = False
            else:
                campIndex = p.wingWorldMiniMap.attendHost2ColorIdx.get(attackerHostId, 0)
                eventHostId = attackerHostId
                eventType = uiConst.WING_WORLD_EVENT_GATE_DESTROY
                isWin = True
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_HALL_DESTROY:
            entNo, attackerHostId = args
            if selfHostId == cityOwnerHostId:
                campIndex = 1
                eventHostId = selfHostId
                eventType = uiConst.WING_WORLD_EVENT_MAIN_HALL_LOST
                isWin = False
            else:
                campIndex = p.wingWorldMiniMap.attendHost2ColorIdx.get(attackerHostId, 0)
                eventHostId = attackerHostId
                eventType = uiConst.WING_WORLD_EVENT_MAIN_HALL_DESTROY
                isWin = True
        elif eventId == gametypes.WING_WORLD_WAR_EVENT_WAREHOUSE_DESTROY:
            entNo, attackerHostId = args
            if selfHostId == cityOwnerHostId:
                campIndex = 1
                eventHostId = selfHostId
                eventType = uiConst.WING_WORLD_EVENT_INVENTORY_LOST
                isWin = False
            else:
                campIndex = p.wingWorldMiniMap.attendHost2ColorIdx.get(attackerHostId, 0)
                eventHostId = attackerHostId
                eventType = uiConst.WING_WORLD_EVENT_INVENTORY_DESTROY
                isWin = True
        self.eventQueue.put((eventType,
         campIndex,
         isWin,
         entNo,
         eventHostId))

    def test(self):
        self.show()
        p = BigWorld.player()
        self.addWingWorldEvents(1, gametypes.WING_WORLD_WAR_EVENT_BUILDING_CHANGE_HANDS, (10001,
         1,
         p.getOriginHostId(),
         0))
        self.addWingWorldEvents(1, gametypes.WING_WORLD_WAR_EVENT_BUILDING_CHANGE_HANDS, (10001, 1, 29032, 0))
        self.addWingWorldEvents(1, gametypes.WING_WORLD_WAR_EVENT_AIR_STONE_ENABLE, (10001,
         1,
         1,
         p.getOriginHostId()))
        self.addWingWorldEvents(1, gametypes.WING_WORLD_WAR_EVENT_BUILDING_CHANGE_HANDS, (10002, 2, 0, 29031))
        self.addWingWorldEvents(1, gametypes.WING_WORLD_WAR_EVENT_BUILDING_CHANGE_HANDS, (10002, 2, 0, 29032))
