#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/modelFittingRoomProxy.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gameglobal
import gametypes
import const
import utils
import clientcom
from Scaleform import GfxValue
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from helpers import editorHelper
from uiProxy import UIProxy
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from cdata import model_fitting_catagory_group_data as MFCGD
from data import item_furniture_data as IFD
from data import item_data as ID
CATAGORY_NAME_COMMON_MODEL = gameStrings.TEXT_MODELFITTINGROOMPROXY_23
CATAGORY_NAME_CUSTOMIZE_MODEL = gameStrings.TEXT_MODELFITTINGROOMPROXY_24
CATAGORY_NAME_GROUP = gameStrings.TEXT_MODELFITTINGROOMPROXY_25
CATARGORY_TYPE_COMM = 1
CATARGORY_TYPE_CUSTOMIZE = 2
CATARGORY_TYPE_GROUP = 3

class ModelFittingRoomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ModelFittingRoomProxy, self).__init__(uiAdapter)
        self.modelMap = {'playAction': self.onPlayAction,
         'getRoleInfo': self.onGetRoleInfo,
         'changeFigure': self.onChangeFigure,
         'refreshModel': self.onRefreshModel,
         'openInventory': self.onOpenInventory,
         'removePart': self.onRemovePart,
         'closeFittingRoom': self.onCloseFittingRoom,
         'selectModel': self.onSelectModel}
        self.headGen = None
        self.mediator = None
        self.homeFurniture = None
        self.lastInfo = None
        self.firstInfo = None
        self.fittingRoomWidgetId = uiConst.WIDGET_MODEL_FITTING_ROOM
        uiAdapter.registerEscFunc(self.fittingRoomWidgetId, self.onCloseFittingRoom)

    def _registerMediator(self, widgetId, mediator):
        self.lastInfo = None
        ret = {}
        if widgetId == self.fittingRoomWidgetId:
            self.mediator = mediator
            self.openBag(True)
            if gameglobal.rds.ui.inventory.mediator:
                self.mediator.Invoke('inventoryStateChange', GfxValue(True))
            modelListInfo = self.getModelListInfo()
            expandedNodes = self.getExpandedNodes(modelListInfo, self.homeFurniture.id)
            ret = {'modelListInfo': modelListInfo,
             'expandedNodes': expandedNodes,
             'showActions': self.homeFurniture.getShowActions()}
            BigWorld.callback(0, self.refreshPartBoard)
            return uiUtils.dict2GfxDict(ret, True)
        else:
            return

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def setLastInfo(self, info, furnitureId):
        if self.lastInfo:
            self.lastInfo['nextFurnitureId'] = furnitureId
            info['lastFurnitureId'] = self.lastInfo.get('furnitureId', 0)
        elif not self.firstInfo:
            self.firstInfo = info
        self.lastInfo = info

    def getCatagoryInfo(self):
        furnitures = editorHelper.instance().getAllDressUpFurniture()
        commInfo = []
        customizeInfo = []
        groupInfo = []
        groupDict = {}
        cIdx = cmIdx = gIdx = totalIndex = 0
        lastInfo = None
        tempInfo = None
        for furniture in furnitures:
            if furniture:
                iData = IFD.data.get(furniture.furnitureId, {})
                catagory = iData.get('catagory', None)
                if catagory == CATARGORY_TYPE_COMM:
                    tempInfo = {'isNode': True,
                     'name': 'node0_' + str(cIdx),
                     'label': iData.get('name', ''),
                     'furnitureId': furniture.id,
                     'totalIndex': totalIndex}
                    commInfo.append(tempInfo)
                    self.setLastInfo(tempInfo, furniture.id)
                    cIdx = cIdx + 1
                    totalIndex = totalIndex + 1
                elif catagory == CATARGORY_TYPE_CUSTOMIZE:
                    tempInfo = {'isNode': True,
                     'name': 'node1_' + str(cmIdx),
                     'label': iData.get('name', ''),
                     'furnitureId': furniture.id,
                     'totalIndex': totalIndex}
                    customizeInfo.append(tempInfo)
                    self.setLastInfo(tempInfo, furniture.id)
                    cmIdx = cmIdx + 1
                    totalIndex = totalIndex + 1
                elif catagory == CATARGORY_TYPE_GROUP:
                    catagoryGroup = iData.get('catagoryGroup', None)
                    groupList = groupDict.setdefault(catagoryGroup, [])
                    groupList.append(furniture)

        for group, furnitures in groupDict.iteritems():
            idx = 0
            catagoryName = MFCGD.data.get(group, {}).get('name', '')
            dataInfo = []
            for furniture in furnitures:
                iData = IFD.data.get(furniture.furnitureId, {})
                tempInfo = {'isNode': True,
                 'name': 'node2_' + str(gIdx) + '_' + str(idx),
                 'label': iData.get('name', ''),
                 'furnitureId': furniture.id,
                 'totalIndex': totalIndex}
                dataInfo.append(tempInfo)
                self.setLastInfo(tempInfo, furniture.id)
                idx = idx + 1
                totalIndex = totalIndex + 1

            groupInfo.append({'isNode': False,
             'name': 'node2_' + str(gIdx),
             'label': catagoryName,
             'data': dataInfo,
             'totalIndex': totalIndex})
            gIdx = gIdx + 1
            totalIndex = totalIndex + 1

        if self.firstInfo:
            self.firstInfo['lastFurnitureId'] = self.lastInfo.get('furnitureId', 0)
        if self.lastInfo:
            self.lastInfo['nextFurnitureId'] = self.firstInfo.get('furnitureId', 0)
        return (commInfo, customizeInfo, groupInfo)

    def getExpandedNodes(self, modelListInfo, furnitureId):
        nodes = []
        for info in modelListInfo:
            self.getExpandedNode(info, nodes, furnitureId)
            if nodes:
                return nodes

        return nodes

    def clearNodes(self, nodes):
        for i in xrange(len(nodes)):
            nodes.pop()

    def getExpandedNode(self, info, nodes, furnitureId):
        nodes.append(info.get('name', ''))
        if info.has_key('furnitureId'):
            if info.get('furnitureId') == furnitureId:
                return
            else:
                nodes.pop()
                return
        else:
            if info.get('data', None):
                for inf in info.get('data'):
                    length = len(nodes)
                    self.getExpandedNode(inf, nodes, furnitureId)
                    if len(nodes) > length:
                        return

                nodes.pop()
                return
            nodes.pop()
            return

    def getModelListInfo(self):
        commInfo, customizeInfo, groupInfo = self.getCatagoryInfo()
        return [{'isNode': False,
          'name': 'node0',
          'label': CATAGORY_NAME_COMMON_MODEL,
          'data': commInfo}, {'isNode': False,
          'name': 'node1',
          'label': CATAGORY_NAME_CUSTOMIZE_MODEL,
          'data': customizeInfo}, {'isNode': False,
          'name': 'node2',
          'label': CATAGORY_NAME_GROUP,
          'data': groupInfo}]

    def onPlayAction(self, *arg):
        index = int(arg[3][0].GetNumber())
        furniture = self.homeFurniture
        actions = furniture.getShowActions()
        BigWorld.player().cell.setFittingRoomItemAction(furniture.ownerUUID, index)
        self.homeFurniture.actionId = index
        if len(actions) > index:
            act = actions[index]
            try:
                gameglobal.rds.ui.fittingRoom.fittingModel.action(act)()
                furniture.model.action(act)()
            except Exception as e:
                gamelog.debug('m.l@modelFittingRoomProxy.onPlayAction action error', e.message)

    def onRefreshModel(self, *arg):
        count = 0
        for equip in self.homeFurniture.equips:
            if equip:
                count = count + 1

        BigWorld.player().cell.removeAllFittingRoomItem(self.homeFurniture.ownerUUID, count)

    @ui.uiEvent(uiConst.WIDGET_MODEL_FITTING_ROOM, (events.EVENT_INVENTORY_CLOSE, events.EVENT_INVENTORY_OPEN))
    def onBagOpenStateChanged(self, event = None):
        if not event:
            return
        if not self.mediator:
            return
        if event.name == events.EVENT_INVENTORY_CLOSE:
            self.mediator.Invoke('inventoryStateChange', GfxValue(False))
        else:
            self.mediator.Invoke('inventoryStateChange', GfxValue(True))

    def onOpenInventory(self, *arg):
        open = int(arg[3][0].GetBool())
        self.openBag(open)

    def onChangeFigure(self, *arg):
        index = int(arg[3][0].GetNumber())
        furnitureId = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if not furnitureId:
            p.showGameMsg(GMDD.data.NO_FITTING_MODEL_TO_SHOW, ())
            return
        furniture = BigWorld.entities.get(furnitureId)
        if not furniture:
            return
        self.homeFurniture = furniture
        gameglobal.rds.ui.fittingRoom.refreshModelFitting(self.homeFurniture, self.afterModelChange)

    def afterModelChange(self):
        self.refreshPartBoard()
        self.refreshSelectecFurniture()

    def openBag(self, open = True):
        if open:
            if not gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.show()
            else:
                gameglobal.rds.ui.inventory.mediator.Invoke('setVisible', GfxValue(True))
            if BigWorld.player().getAbilityData(gametypes.ABILITY_FASHION_BAG_ON):
                if not gameglobal.rds.ui.fashionBag.mediator:
                    gameglobal.rds.ui.fashionBag.show()
        else:
            gameglobal.rds.ui.inventory.closeInventory()

    def getBestMainEquipPart(self, i):
        partList = i.whereEquip()
        dstPos = partList[0]
        if len(partList) > 1:
            for id in range(0, len(partList)):
                part = partList[id]
                if self.homeFurniture.equips.isEmpty(part):
                    dstPos = part
                    break
                elif dstPos != part:
                    dstPos = part

        return dstPos

    @ui.uiEvent(uiConst.WIDGET_MODEL_FITTING_ROOM, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        page = event.data['page']
        pos = event.data['pos']
        if i == None:
            return
        elif not self.checkItemEquip(i):
            return
        else:
            part = self.getBestMainEquipPart(i)
            BigWorld.player().cell.addFittingRoomItem(self.homeFurniture.ownerUUID, const.RES_KIND_INV, page, pos, part)
            return

    @ui.uiEvent(uiConst.WIDGET_MODEL_FITTING_ROOM, events.EVENT_FASHION_ITEM_CLICKED)
    def onFashionRightClick(self, event):
        event.stop()
        i = event.data['item']
        page = event.data['page']
        pos = event.data['pos']
        if i == None:
            return
        else:
            BigWorld.player().showGameMsg(GMDD.data.HOME_FASHION_NEED_TO_INVENTORY, ())
            return

    def checkItemEquip(self, i):
        if not i:
            return False
        p = BigWorld.player()
        if i.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return False
        sch = self.homeFurniture.physique.school
        sex = self.homeFurniture.physique.sex
        bodyType = self.homeFurniture.physique.bodyType
        data = ID.data.get(i.id, {})
        if data.has_key('sexReq'):
            if sex != data['sexReq']:
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SEX, data.get('name', ''))
                return False
        if data.has_key('schReq'):
            if sch not in data['schReq']:
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL, data.get('name', ''))
                return False
        if not utils.inAllowBodyType(i.id, bodyType, ID):
            p.showGameMsg(GMDD.data.ITEM_USE_BODYTYPE_ERROR, ())
            return False
        return True

    def onRemovePart(self, *arg):
        part = int(arg[3][0].GetNumber())
        BigWorld.player().cell.removeFittingRoomItem(self.homeFurniture.ownerUUID, part)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator:
            if item:
                if not item.isFashionEquip():
                    return True
        return False

    def onGetRoleInfo(self, *arg):
        ret = {}
        return uiUtils.dict2GfxDict(ret, True)

    def show(self, homeFurniture):
        self.homeFurniture = homeFurniture
        gameglobal.rds.ui.fittingRoom.enterFullScreenModelFitting(homeFurniture, self.showFittingRoom)

    def refreshModel(self, modelEntity = None):
        if not self.mediator:
            return
        gameglobal.rds.ui.fittingRoom.refreshSameModelFitting(self.homeFurniture, Functor(self.afterModelPartUpdate, modelEntity))

    def afterModelPartUpdate(self, modelEntity):
        self.afterModelChange()
        if modelEntity:
            clientcom.cloneEntityAllWeaponAttachments(modelEntity, gameglobal.rds.ui.fittingRoom.fittingModel, True)

    def showFittingRoom(self):
        self.uiAdapter.hideAllUI()
        if not self.mediator:
            self.uiAdapter.loadWidget(self.fittingRoomWidgetId)
        else:
            self.refreshPartBoard()
            self.refreshSelectecFurniture()

    def refreshSelectecFurniture(self):
        if not self.mediator:
            return
        modelListInfo = self.getModelListInfo()
        expandedNodes = self.getExpandedNodes(modelListInfo, self.homeFurniture.id)
        self.mediator.Invoke('expandNode', uiUtils.array2GfxAarry(expandedNodes))

    def onCloseFittingRoom(self, *arg):
        gameglobal.rds.ui.fittingRoom.leaveFullScreenModelFitting()
        self.uiAdapter.restoreUI()
        self.uiAdapter.unLoadWidget(self.fittingRoomWidgetId)
        self.homeFurniture = None
        self.mediator = None
        self.lastInfo = None
        BigWorld.player().restoreAllNearby()

    def onSelectModel(self, *arg):
        furnitureId = int(arg[3][0].GetNumber())
        furniture = BigWorld.entities.get(furnitureId)
        if not furniture:
            return
        self.homeFurniture = furniture
        gameglobal.rds.ui.fittingRoom.refreshModelFitting(self.homeFurniture, self.afterModelChange)

    def refreshModelState(self):
        self.refreshPartBoard()

    def refreshPartBoard(self):
        if not self.mediator:
            return
        info = {}
        for index in range(len(self.homeFurniture.equips)):
            equip = self.homeFurniture.equips[index]
            if equip:
                parts = list(equip.wherePreview())
                parts.extend(uiUtils.getAspectParts(equip.id))
                mainPart = index
                subInfo = uiUtils.getGfxItem(equip, uiConst.ICON_SIZE40)
                subInfo['mainPart'] = mainPart
                subInfo['parts'] = [mainPart]
                subInfo['itemId'] = equip.id
                info[mainPart] = subInfo

        self.mediator.Invoke('refreshPartBoard', uiUtils.dict2GfxDict(info, True))
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
