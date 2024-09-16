#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/fittingModel.o
import copy
import weakref
import utils
import BigWorld
import gameglobal
import appearance
import physique
import HomeFurniture
import gametypes
from item import Item
from helpers import capturePhoto
from helpers import charRes
from data import item_data as ID
from data import consumable_item_data as CID

class FittingModel(object):

    def __init__(self, typeName, size, modelFinishCallback, proxy):
        super(FittingModel, self).__init__()
        self.typeName = typeName
        self.size = size
        self._modelFinishCallback = modelFinishCallback
        self.proxy = weakref.proxy(proxy)
        self.reset()

    def reset(self):
        self.headGen = None
        self.item = None
        self.figureInfo = None
        self.dyeList = ()
        self.itemList = ()
        self.originalAspect = None
        self.model = None
        self.showItems = []

    def afterModelFinishCallback(self):
        self.setLoadingMcVisible(False)
        if self._modelFinishCallback:
            self._modelFinishCallback()

    def setLoadingMcVisible(self, value):
        if self.proxy:
            self.proxy.setLoadingMcVisible(value)

    def initHeadGeen(self):
        if not self.headGen:
            self.headGen = getattr(capturePhoto, self.typeName).getInstance('gui/taskmask.tga', self.size)
            self.headGen.setFitingModel(self)
        self.headGen.initFlashMesh()
        self.headGen.setModelFinishCallback(self.afterModelFinishCallback)

    def showItem(self):
        res, aspect, showFashion = self.getMpr()
        self.takePhoto3D(res, True, {'aspect': aspect,
         'showFashion': showFashion,
         'physique': self.getPhysique() if self.figureInfo else None,
         'showAvatar': self.isShowAvatar()})

    def showMultiItem(self):
        res, aspect, showFashion = self.getMultiMpr()
        self.takePhoto3D(res, True, {'aspect': aspect,
         'showFashion': showFashion,
         'physique': self.getPhysique() if self.figureInfo else None,
         'showAvatar': self.isShowAvatar()})

    def addItem(self, item):
        if gameglobal.rds.ui.fittingRoom.checkItemPreview(item):
            self.item = item
            self.itemList = ()
            self.item.oldDyeList = getattr(self.item, 'dyeList', ())
            if self.dyeList and self.isCanDye():
                self.item.dyeList = self.dyeList
            self.showItem()

    def addItems(self, items):
        for item in items:
            if not gameglobal.rds.ui.fittingRoom.checkItemPreview(item):
                return

        self.showItems = items
        self.showMultiItem()

    def getMultiMpr(self):
        mpr, aspect, isShowFashion = self.getMultiEquipMpr()
        res = mpr.getPrerequisites()
        return (res, aspect, isShowFashion)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
        self.figureInfo = None
        self.dyeList = ()
        self.setLoadingMcVisible(False)

    def takePhoto3D(self, res, isFittingRoom = False, extraInfo = {}):
        if not self.headGen:
            self.headGen = getattr(capturePhoto, self.typeName).getInstance('gui/taskmask.tga', self.size)
        self.headGen.startCaptureEntAndRes(BigWorld.player(), res, isFittingRoom, extraInfo)
        self.setLoadingMcVisible(True)

    def getMultiEquipMpr(self):
        p = BigWorld.player()
        realPhysqiue = self.getPhysique()
        aspect = self.getAspect()
        avatarConfig = self.getAvatarConfig()
        mpr = charRes.MultiPartRes()
        isShowFashion = True
        for item in self.showItems:
            if item:
                if gameglobal.rds.ui.fittingRoom.checkBonusData(item):
                    items = gameglobal.rds.ui.fittingRoom.getBonusData(item)
                    for item in items:
                        if item.type == Item.BASETYPE_EQUIP:
                            if not item.isWingOrRide():
                                isShowFashion |= gameglobal.rds.ui.fittingRoom.createAspect(aspect, item)
                            if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                                isShowFashion = False

                elif gameglobal.rds.ui.fittingRoom.checkUunlockMorpher(item):
                    data = CID.data.get(item.id, {})
                    if data.has_key('faxing_style'):
                        if realPhysqiue == p.realPhysique:
                            realPhysqiue = copy.deepcopy(realPhysqiue)
                        realPhysqiue.hair = data['faxing_style']
                        aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
                    elif data.has_key('zhuangshi_style'):
                        avatarConfig = gameglobal.rds.ui.fittingRoom.createAvatarConfig(avatarConfig, data['zhuangshi_style'])
                elif gameglobal.rds.ui.fittingRoom.checkZhuangshiItem(item):
                    data = CID.data.get(item.id, {})
                    avatarConfig = gameglobal.rds.ui.fittingRoom.createAvatarConfig(avatarConfig, data.get('zhuangshi', 1))
                else:
                    if not item.isWingOrRide():
                        isShowFashion |= gameglobal.rds.ui.fittingRoom.createAspect(aspect, item)
                    if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                        isShowFashion = False

        mpr.queryByAttribute(realPhysqiue, aspect, isShowFashion, avatarConfig)
        return (mpr, aspect, isShowFashion)

    def getEquipMpr(self):
        p = BigWorld.player()
        realPhysqiue = self.getPhysique()
        aspect = self.getAspect()
        avatarConfig = self.getAvatarConfig()
        mpr = charRes.MultiPartRes()
        isShowFashion = gameglobal.rds.ui.fittingRoom.isShowFashion(aspect)
        if self.item:
            if gameglobal.rds.ui.fittingRoom.checkBonusData(self.item):
                items = gameglobal.rds.ui.fittingRoom.getBonusData(self.item)
                for item in items:
                    if item.type == Item.BASETYPE_EQUIP:
                        if not item.isWingOrRide():
                            isShowFashion |= gameglobal.rds.ui.fittingRoom.createAspect(aspect, item)
                        if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                            isShowFashion = False

            elif gameglobal.rds.ui.fittingRoom.checkUunlockMorpher(self.item):
                data = CID.data.get(self.item.id, {})
                if data.has_key('faxing_style'):
                    if realPhysqiue == p.realPhysique:
                        realPhysqiue = copy.deepcopy(realPhysqiue)
                    realPhysqiue.hair = data['faxing_style']
                    aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
                elif data.has_key('zhuangshi_style'):
                    avatarConfig = gameglobal.rds.ui.fittingRoom.createAvatarConfig(avatarConfig, data['zhuangshi_style'])
            elif gameglobal.rds.ui.fittingRoom.checkZhuangshiItem(self.item):
                data = CID.data.get(self.item.id, {})
                avatarConfig = gameglobal.rds.ui.fittingRoom.createAvatarConfig(avatarConfig, data.get('zhuangshi', 1))
            else:
                item = self.item
                if not item.isWingOrRide():
                    isShowFashion |= gameglobal.rds.ui.fittingRoom.createAspect(aspect, item)
                if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                    isShowFashion = False
        mpr.queryByAttribute(realPhysqiue, aspect, isShowFashion, avatarConfig)
        return (mpr, aspect, isShowFashion)

    def getMpr(self):
        if self.item and self.item.type == Item.BASETYPE_FURNITURE:
            res = HomeFurniture.getModelPath(self.item.id)
            aspect = None
            isShowFashion = False
            return (res, aspect, isShowFashion)
        mpr, aspect, isShowFashion = self.getEquipMpr()
        res = mpr.getPrerequisites()
        return (res, aspect, isShowFashion)

    def restorePhoto3D(self):
        self.item = None
        self.showItems = []
        p = BigWorld.player()
        self.originalAspect = copy.deepcopy(p.aspect)
        res, aspect, showFashion = self.getMpr()
        self.takePhoto3D(res, True, {'aspect': aspect,
         'showFashion': showFashion,
         'physique': self.getPhysique() if self.figureInfo else None,
         'showAvatar': self.isShowAvatar()})

    def getPhysique(self):
        p = BigWorld.player()
        if self.figureInfo:
            realPhysique = self.figureInfo.get('physique', physique.Physique({}))
        else:
            realPhysique = p.realPhysique
        return realPhysique

    def isShowAvatar(self):
        if self.item and self.item.type == Item.BASETYPE_FURNITURE:
            return False
        return True

    def getAspect(self):
        p = BigWorld.player()
        if self.originalAspect:
            return self.originalAspect
        if self.figureInfo:
            return appearance.Appearance({})
        return copy.deepcopy(p.realAspect)

    def getAvatarConfig(self):
        p = BigWorld.player()
        if self.figureInfo:
            return self.figureInfo.get('avatarConfig', '')
        return p.avatarConfig


class MarryPreviewFittingModel(FittingModel):

    def takePhoto3D(self, res, isFittingRoom = False, extraInfo = {}):
        if not self.headGen:
            self.headGen = getattr(capturePhoto, self.typeName).getInstance('gui/taskmask.tga', self.size)
        if self.figureInfo:
            physique = extraInfo.get('physique')
            if not physique:
                return
            sex = physique.sex
            bodyType = physique.bodyType
            modelId = charRes.transBodyType(sex, bodyType)
            aspect = extraInfo.get('aspect')
            if not aspect:
                return
            showFashion = extraInfo.get('showFashion')
            avatarConfig = self.getAvatarConfig()
            self.headGen.startCaptureRes(modelId, aspect, physique, avatarConfig, ('1101',), showFashion=showFashion)
        else:
            self.headGen.startCaptureEntAndRes(BigWorld.player(), res, isFittingRoom, extraInfo)
        self.setLoadingMcVisible(True)

    def getAspect(self):
        if self.figureInfo:
            aspect = self.figureInfo.get('aspect', appearance.Appearance({}))
            if aspect:
                return aspect
        return appearance.Appearance({})

    def addItem(self, item):
        if self.checkItemPreview(item):
            self.item = item
            self.itemList = ()
            self.item.oldDyeList = getattr(self.item, 'dyeList', ())
            if self.dyeList and self.isCanDye():
                self.item.dyeList = self.dyeList
            self.showItem()

    def addItems(self, items):
        for item in items:
            if not self.checkItemPreview(item):
                return

        self.showItems = items
        self.showMultiItem()

    def checkItemPreview(self, item, showMsg = True):
        if not item:
            return False
        p = BigWorld.player()
        physiqueVal = self.getPhysique()
        sex = physiqueVal.sex
        sch = physiqueVal.school
        bodyType = physiqueVal.bodyType
        if not (item.type == Item.BASETYPE_EQUIP or item.type == Item.BASETYPE_FURNITURE and gameglobal.rds.configData.get('enablePreviewHomeFurniture', False) or self.checkBonusData(item) or self.checkUunlockMorpher(item) or self.checkZhuangshiItem(item)):
            return False
        if not utils.inAllowBodyType(item.id, bodyType, ID):
            if showMsg:
                p.showGameMsg(GMDD.data.ITEM_USE_BODYTYPE_ERROR, ())
            return False
        return True

    def checkBonusData(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and CID.data.get(item.id, {}).has_key('itemSetInfo')

    def checkUunlockMorpher(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and getattr(item, 'cstype', 0) == Item.SUBTYPE_2_UNLOCK_MORPHER

    def checkZhuangshiItem(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and getattr(item, 'cstype', 0) == Item.SUBTYPE_2_ZHUANGSHI
