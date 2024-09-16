#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceTouchProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from data import personal_zone_touch_data as PZTD
PERPAGE_ITEM_NUM_MAX = 12

class SpaceTouchProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(SpaceTouchProxy, self).__init__(uiAdapter)
        self.bindType = 'spaceTouch'
        self.modelMap = {'getInitInfo': self.onGetInitInfo,
         'sendTouch': self.onSendTouch}
        self.reset()
        self.lastName = ''
        self.lastTouchId = 0
        self.noZoneInfo = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACE_TOUCH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACE_TOUCH:
            self.mediator = mediator

    def onGetInitInfo(self, *arg):
        touchData = []
        for key, data in PZTD.data.iteritems():
            if data.get('hideIcon', 0):
                continue
            itemData = {}
            itemData['id'] = key
            itemData['cdesc'] = data.get('cdesc', '')
            itemData['name'] = data.get('name', '')
            itemData['iconPath'] = self.getIconPath(data.get('photo', 0))
            touchData.append(itemData)

        self.baseInfo['touchData'] = touchData
        return uiUtils.dict2GfxDict(self.baseInfo, True)

    def getIconPath(self, id):
        return 'gerenkongjian/%d.dds' % id

    def onSendTouch(self, *arg):
        touchId = int(arg[3][0].GetNumber())
        self.sendTouch(touchId)
        self.lastName = self.baseInfo.get('roleName', '')
        self.lastTouchId = touchId
        self.hide()

    def sendTouch(self, touchId):
        p = BigWorld.player()
        p.base.touchPersonalZone(self.ownerGbID, touchId, self.hostId)
        self.uiAdapter.addFriendPop.sendTouch(self.ownerGbID)

    def show(self, ownerGbID, ownerName, hostId = 0, noZoneInfo = False):
        self.ownerGbID = ownerGbID
        self.hostId = hostId
        self.baseInfo['roleName'] = ownerName
        self.noZoneInfo = noZoneInfo
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACE_TOUCH)
        else:
            self.refresh()

    def refresh(self):
        if self.mediator:
            self.mediator.Invoke('refreshRoleName', GfxValue(uiUtils.gbk2unicode(self.baseInfo['roleName'])))

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACE_TOUCH)

    def reset(self):
        self.baseInfo = {}
        self.hostId = 0
        self.mediator = None

    def sendTouchMsg(self):
        p = BigWorld.player()
        zone = p.getPersonalSysProxy()
        canChat = self.noZoneInfo or zone.isOnline() and not zone.isCrossServer()
        if canChat and self.lastName and self.lastTouchId:
            p = BigWorld.player()
            desc = PZTD.data.get(self.lastTouchId, {}).get('cdesc', '')
            desc = desc + ':role'
            p.cell.chatToOne(self.lastName, desc)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, desc, self.lastName, False, True)
