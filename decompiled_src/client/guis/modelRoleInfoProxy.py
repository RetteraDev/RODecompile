#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/modelRoleInfoProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import utils
from helpers import editorHelper
from guis import uiConst
from guis import uiUtils
from helpers import capturePhoto
from helpers import charRes
from Scaleform import GfxValue
from uiProxy import SlotDataProxy
from cdata import font_config_data as FCD
from data import item_data as ID

class ModelRoleInfoProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ModelRoleInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'sendLink': self.onSendLink,
         'getRoleInfo': self.onGetRoleInfo,
         'oneKeyTryOn': self.onOneKeyTryOn,
         'rotateFigure': self.onRotateFigure,
         'closeRoleInfo': self.onCloseRoleInfo}
        self.binding = {}
        self.bindType = 'modelrole'
        self.type = 'modelroleslot'
        self.homeFurniture = None
        self.equip = None
        self.share = None
        self.school = None
        self.aspect = None
        self.physique = None
        self.avatarConfig = None
        self.roleName = None
        self.itemId = None
        self.uuid = None
        self.nuid = None
        self.headGen = None
        self.mediator = None
        self.roleInfoWidgetId = uiConst.WIDGET_MODEL_ROLE_INFO
        uiAdapter.registerEscFunc(self.roleInfoWidgetId, self.onCloseRoleInfo)

    def getFurnitureName(self):
        furnitureName = self.homeFurniture.getName() if self.homeFurniture else ''
        if not furnitureName:
            furnitureName = utils.getFurnitureName(self.itemId)
        return furnitureName

    def _registerMediator(self, widgetId, mediator):
        ret = {}
        if widgetId == self.roleInfoWidgetId:
            self.mediator = mediator
            self.initHeadGen()
            self.takePhoto3D()
            furnitureName = self.getFurnitureName()
            ret['title'] = self.getTile(furnitureName)
            ret['share'] = self.share
            return uiUtils.dict2GfxDict(ret, True)

    def getTile(self, furnitureName):
        return gameStrings.TEXT_MODELROLEINFOPROXY_66 % (self.roleName, furnitureName)

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.104 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onSendLink(self, *arg):
        if self.homeFurniture:
            uuid = self.homeFurniture.ownerUUID if self.homeFurniture else self.uuid
            BigWorld.player().cell.getFittingRoomItemLink(uuid)
        else:
            furnitureName = utils.getFurnitureName(self.itemId)
            msg = utils.getModelShareLinkMsg(self.roleName, str(self.nuid), furnitureName)
            gameglobal.rds.ui.sendLink(msg)

    def onOneKeyTryOn(self, *arg):
        if not self.equip:
            return
        BigWorld.player().tryOnModel(self.equip)

    def setSlotColor(self, idSlot, color):
        if self.mediator != None:
            self.mediator.Invoke('setSlotColor', (GfxValue(idSlot), GfxValue(color)))

    def setSlotState(self, idSlot, stat):
        if self.mediator != None:
            self.mediator.Invoke('setSlotState', (GfxValue(idSlot), GfxValue(stat)))

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[9:]), int(idItem[4:]))

    def getSlotValue(self, movie, idItem, idBar):
        item = self.equip.get(idItem)
        if item:
            data = self.uiAdapter.movie.CreateObject()
            icon = uiUtils.getItemIconFile64(item.id)
            iconPath = GfxValue(icon)
            data.SetMember('iconPath', iconPath)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            data.SetMember('color', GfxValue(color))
            self.setSlotColor(idItem, color)
            return data

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        i = self.equip.get(idNum)
        if i != None:
            return gameglobal.rds.ui.inventory.GfxToolTip(i, const.ITEM_IN_TARGET_ROLE)
        else:
            return

    def onGetItemTip(self, part):
        i = self.equip.get(part)
        if i != None:
            return gameglobal.rds.ui.inventory.GfxToolTip(i, const.ITEM_IN_TARGET_ROLE)
        else:
            return

    def _getKey(self, nSlot):
        return 'modelrole0.slot%d' % nSlot

    def _getItemData(self, itemId, part):
        p = BigWorld.player()
        if not itemId:
            return {}
        ret = {}
        ret['itemId'] = itemId
        ret['iconPath'] = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, ID.data.get(itemId, {}).get('icon', 0))
        num = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        ret['num'] = '%d/%d' % (1, 1)
        ret['color'] = uiUtils.getItemColor(itemId)
        ret['srcType'] = 'modelrole' + str(part)
        return ret

    def onGetRoleInfo(self, *arg):
        ret = {}
        equipLen = len(BigWorld.player().equipment)
        equips = [None] * equipLen
        for i in xrange(equipLen):
            if self.equip and len(self.equip) > i:
                equipItem = self.equip[i]
                if equipItem:
                    equips[i] = self._getItemData(self.equip[i].id, i)

        ret['equips'] = equips
        ret['share'] = self.share
        furnitureName = self.getFurnitureName()
        ret['title'] = self.getTile(furnitureName)
        return uiUtils.dict2GfxDict(ret, True)

    def showRoleInfo(self, homeFurniture, equip, school, aspect, physique, avatarConfig, share = False, roleName = '', itemId = None, uuid = None, nuid = None):
        self.homeFurniture = homeFurniture
        self.share = share
        self.equip = equip
        self.school = school
        self.aspect = aspect
        self.physique = physique
        self.avatarConfig = avatarConfig
        self.roleName = roleName if roleName else editorHelper.instance().ownerName
        self.itemId = itemId
        self.uuid = uuid
        self.nuid = nuid
        if self.mediator != None:
            self.refreshDataInfo()
            self.takePhoto3D()
        else:
            self.uiAdapter.loadWidget(self.roleInfoWidgetId)

    def refreshDataInfo(self):
        self.mediator.Invoke('refreshDataInfo')

    def onCloseRoleInfo(self, *arg):
        self.mediator = None
        self.uiAdapter.unLoadWidget(self.roleInfoWidgetId)

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.ModelRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 420)
        modelId = charRes.transBodyType(self.physique.sex, self.physique.bodyType)
        showFashion = True
        self.headGen.startCaptureRes(modelId, self.aspect, self.physique, self.avatarConfig, ('1101',), showFashion)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.ModelRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 420)
        self.headGen.initFlashMesh()

    def test(self):
        p = BigWorld.player()
        self.showRoleInfo(p.equipment, p.school, p.aspect, p.physique, p.avatarConfig)
