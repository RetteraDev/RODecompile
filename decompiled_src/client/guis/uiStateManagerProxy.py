#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiStateManagerProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import formula
import gamelog
from uiProxy import UIProxy
from data import ui_state_manager_data as USMD

class UiStateManagerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UiStateManagerProxy, self).__init__(uiAdapter)
        self.hideWidgets = []
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onMapChagne, 0, True)
        self.addEvent(events.EVENT_WIDGET_LOAD_COMPLETE, self.onWidgetLoadedComplete, 0, True)

    def onWidgetLoadedComplete(self, event):
        p = BigWorld.player()
        mapID = getattr(p, 'mapID', 0)
        if event.data in USMD.data.get(mapID, {}).get('hideWidgets', ()):
            self.uiAdapter.setWidgetVisible(event.data, False)
            self.hideWidgets.append(event.data)

    def onMapChagne(self, event):
        oldMapId = formula.getMapId(event.data)
        newMapId = getattr(BigWorld.player(), 'mapID', 0)
        if newMapId and oldMapId != newMapId:
            self.recoverHideWidgets()
            self.hideWidgetsByMapID(newMapId)

    def testMapChagne(self, mapID):
        self.dispatchEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, mapID)

    def hideWidgetsByMapID(self, mapId):
        for widgetId in USMD.data.get(mapId, {}).get('hideWidgets', ()):
            self.uiAdapter.setWidgetVisible(widgetId, False)
            self.hideWidgets.append(widgetId)

    def recoverHideWidgets(self):
        for widgetId in set(self.hideWidgets):
            self.uiAdapter.setWidgetVisible(widgetId, True)

        self.hideWidgets = []
