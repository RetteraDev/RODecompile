#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipRedemptionProxy.o
from gamestrings import gameStrings
import time
import BigWorld
import utils
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
from data import equip_prefix_prop_data as EPPD
from data import item_data as ID

class EquipRedemptionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipRedemptionProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'getCacheData': self.onGetCacheData,
         'payRedemption': self.onPayRedemption}
        self.mediator = None
        self.bindType = 'redemption'
        self.type = 'redemption'
        self.npcId = 0
        self.version = 0
        self.redemptions = []
        self.itemList = []
        self.items = []
        self.uuidDict = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_REDEMPTION:
            self.mediator = mediator

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[10:]), int(idItem[4:]))

    def _getKey(self, page, pos):
        return 'redemption%d.slot%d' % (page, pos)

    def show(self, npcId):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_REDEMPTION)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_REDEMPTION)

    def onGetCacheData(self, *arg):
        playerCash = BigWorld.player().cash
        for item in self.itemList:
            needCash = item['needCash']
            item['cash'] = uiUtils.convertNumStr(playerCash, needCash)

        return uiUtils.array2GfxAarry(self.itemList, True)

    def onPayRedemption(self, *arg):
        uuid = arg[3][0].GetString()
        if not self.uuidDict.has_key(uuid):
            return
        originUuid = self.uuidDict[uuid]
        ent = BigWorld.entities.get(self.npcId)
        if not ent:
            return
        ent.cell.payRedemption(originUuid)

    def requetsData(self):
        ent = BigWorld.entities.get(self.npcId)
        if not ent:
            return
        ent.cell.openRedemption(self.version)

    def refreshData(self, data, ver):
        self.redemptions = data
        self.version = ver
        self.updateData()

    def updateData(self):
        self.itemList = []
        self.items = []
        playerCash = BigWorld.player().cash
        for redemption in self.redemptions:
            if redemption.tDeliver > 0:
                continue
            itemObj = {}
            convertUuid = repr(redemption.item.uuid)
            itemObj['uuid'] = convertUuid
            self.uuidDict[convertUuid] = redemption.item.uuid
            itemObj['itemInfo'] = self.getItemInfo(redemption.item)
            itemObj['tStart'] = redemption.tStart
            itemObj['tDeliver'] = redemption.tDeliver
            if redemption.tDeliver <= 0:
                itemObj['tEnd'] = GMD.data.get(GMDD.data.ITEM_REDEMPTION_AUTO_TIME, {}).get('text', gameStrings.TEXT_EQUIPREDEMPTIONPROXY_109) % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(redemption.tEnd))
            else:
                itemObj['tEnd'] = GMD.data.get(GMDD.data.ITEM_IS_IN_REDEMPTION, {}).get('text', gameStrings.TEXT_EQUIPREDEMPTIONPROXY_111)
            itemObj['needCash'] = redemption.cash
            itemObj['cash'] = uiUtils.convertNumStr(playerCash, redemption.cash)
            itemObj['coin'] = redemption.coin
            itemObj['fromGbId'] = redemption.fromGbId
            itemObj['fromRole'] = redemption.fromRole
            itemObj['toGbId'] = redemption.toGbId
            itemObj['toRole'] = redemption.toRole
            itemObj['lock'] = redemption.lock
            self.itemList.append(itemObj)
            self.items.append(redemption.item)

        temp = sorted(self.itemList, key=lambda k: k['tEnd'])
        self.itemList = sorted(temp, key=lambda k: k['tDeliver'], reverse=True)
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.array2GfxAarry(self.itemList, True))

    def updateItemList(self, itemList):
        ret = []
        for item in itemList:
            itemObj = self.getItemInfo(item.id)
            ret.append(itemObj)

        return ret

    def getItemInfo(self, item):
        if item:
            itemInfo = {}
            itemInfo = ID.data.get(item.id, {})
            itemInfo['itemId'] = item.id
            qualityColor = FCD.data.get(('item', item.quality), {}).get('color', '#ffffff')
            itemInfo['itemName'] = uiUtils.toHtml(self.getItemName(item), qualityColor)
            icon = 'item/icon64/' + str(itemInfo.get('icon', 'notFound')) + '.dds'
            itemInfo['iconPath'] = icon
            color = FCD.data.get(('item', item.quality), {}).get('qualitycolor', 'nothing')
            itemInfo['color'] = color
            return itemInfo

    def getItemName(self, item):
        itemName = ''
        if hasattr(item, 'name'):
            itemName = item.name
            if hasattr(item, 'prefixInfo'):
                for prefixItem in EPPD.data.get(item.prefixInfo[0], []):
                    if prefixItem['id'] == item.prefixInfo[1]:
                        if utils.isInternationalVersion():
                            itemName = item.name + prefixItem['name'] + item.getNameSuffix()
                        else:
                            itemName = prefixItem['name'] + item.name + item.getNameSuffix()
                        break
                    else:
                        itemName = item.name + item.getNameSuffix()

            else:
                itemName = item.name + item.getNameSuffix()
        return itemName

    def onGetToolTip(self, key):
        page, pos = self.getSlotID(key)
        if pos < len(self.itemList):
            i = self.items[pos]
            if i == None:
                return
            return gameglobal.rds.ui.inventory.GfxToolTip(i)
        else:
            return

    def removeItem(self, uuid, ver):
        if ver != self.version:
            self.requetsData()
            return
        for redemption in self.redemptions:
            if redemption.item.uuid == uuid:
                self.redemptions.pop(redemption)

        self.updateData()

    def updateItem(self, newRedemption, ver):
        if ver != self.version:
            self.requetsData()
            return
        convertUuid = repr(newRedemption.item.uuid)
        for redemption in self.redemptions:
            if repr(redemption.item.uuid) == convertUuid:
                redemption.opNUID = newRedemption.opNUID
                redemption.item = newRedemption.item
                redemption.tStart = newRedemption.tStart
                redemption.tDeliver = newRedemption.tDeliver
                redemption.tEnd = newRedemption.tEnd
                redemption.cash = newRedemption.cash
                redemption.coin = newRedemption.coin
                redemption.fromGbId = newRedemption.fromGbId
                redemption.fromRole = newRedemption.fromRole
                redemption.toGbId = newRedemption.toGbId
                redemption.toRole = newRedemption.toRole
                redemption.lock = newRedemption.lock

        self.updateData()
