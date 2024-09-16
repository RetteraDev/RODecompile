#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fittingRoomProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
import ResMgr
from Scaleform import GfxValue
import Pixie
import const
import gameglobal
import gametypes
import uiConst
import physique
import appearance
import clientcom
import utils
import clientUtils
from item import Item
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from callbackHelper import Functor
from guis import uiUtils
from helpers import capturePhoto
from helpers import charRes
from helpers import avatarMorpher as AM
from helpers import avatarMorpherUtils as AMU
from helpers import strmap
from helpers import attachedModel
from helpers import tintalt as TA
from helpers import seqTask
from helpers import cameraControl as CC
from helpers import blackEffectManager
from sfx import sfx
from HomeFurniture import HomeFurniture
from guis import tipUtils
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import consumable_item_data as CID
from data import bonus_set_data as BSD
from data import equip_data as ED
from data import wear_show_data as WSD
from data import mall_config_data as MCD
TYPE_MULTIITEM = 1

class FittingRoomProxy(SlotDataProxy):
    FX_INDEX_FASHION = 0
    FX_INDEX_RIDE = 1
    FX_INDEX_WING = 2

    def __init__(self, uiAdapter):
        super(FittingRoomProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'reSetFigure': self.onReSetFigure,
         'zoomFigure': self.onZoomFigure,
         'rotateFigure': self.onRotateFigure,
         'updateFigure': self.onUpdateFigure,
         'getFashionDesc': self.onGetFashionDesc}
        self.mediator = None
        self.headGen = None
        self.mallHeadGen = None
        self.item = None
        self.figureInfo = None
        self.dyeList = ()
        self.itemList = ()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FITTINGROOM, Functor(self.hide, None))
        self.lightEffectId = MCD.data.get('lightEffect', [10104, 10104, 10104])
        self.lightEffect = None
        self.lightEffectIndex = None
        self.lightDummyModel = None
        self.originalAspect = None
        self.model = None
        self.fittingModel = None
        self.rideModel = None
        self.wingModel = None
        self.hpNodeList = []
        self.modelUpdater = None
        self.fittingModelUpdater = None
        self.addedItemList = []
        self.addedItemDict = {}
        self.applyBare = False
        self.heightOffset = MCD.data.get('wingShowOffset', 0.4)
        self.playerModelFinishCallback = None
        self.showType = None
        self.showItems = []
        self.homeFurniture = None
        self.hideResetBtn = False

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FITTINGROOM)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FITTINGROOM:
            self.mediator = mediator
            self.showFitting()
            return uiUtils.dict2GfxDict({'hideResetBtn': self.hideResetBtn})

    def reset(self):
        super(self.__class__, self).reset()
        self.item = None
        self.fashionEffects = []

    def clearWidget(self):
        self.mediator = None
        self.resetHeadGen()
        self.originalAspect = None
        self.showType = None
        self.showItems = []
        self.hideResetBtn = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FITTINGROOM)

    def onClickClose(self, *arg):
        self.hide()

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onUpdateFigure(self, *arg):
        self.updateFigure()

    def onGetFashionDesc(self, *arg):
        desc = self.getFashionDesc()
        return GfxValue(gbk2unicode(desc))

    def onZoomFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        if self.headGen:
            self.headGen.zoom(deltaZoom)

    def onReSetFigure(self, *arg):
        if self.headGen:
            self.headGen.resetYaw()

    def addMallItem(self, item):
        if item and item.ctrlPreviewEffect():
            clientcom.previewEffect(BigWorld.player(), item.id)
            return
        if self.checkItemPreview(item):
            self.item = item
            self.itemList = ()
            self.item.oldDyeList = getattr(self.item, 'dyeList', ())
            if self.dyeList and self.isCanDye():
                self.item.dyeList = self.dyeList
            self.showMallItem()

    def showMallItem(self):
        res, aspect, showFashion = self.getMpr()
        self.takeMallPhoto3D(res, True, {'aspect': aspect,
         'showFashion': showFashion,
         'physique': self.getPhysique() if self.figureInfo else None,
         'showAvatar': self.isShowAvatar()})

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
        if self.checkBonusData(item):
            itemList = self.getBonusData(item)
            for item in itemList:
                if self.checkItemPreview(item):
                    break
            else:
                return False

        data = ID.data.get(item.id, {})
        if data.has_key('sexReq'):
            if sex != data['sexReq']:
                if showMsg:
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SEX, item.name)
                return False
        if data.has_key('schReq'):
            if sch not in data['schReq']:
                if showMsg:
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL, item.name)
                return False
        if not utils.inAllowBodyType(item.id, bodyType, ID):
            if showMsg:
                p.showGameMsg(GMDD.data.ITEM_USE_BODYTYPE_ERROR, ())
            return False
        if self.showType == TYPE_MULTIITEM and hasattr(item, 'equipType') and (item.equipType == Item.EQUIP_BASETYPE_JEWELRY or item.equipType == Item.EQUIP_BASETYPE_ARMOR and item.wherePreview()[0] == gametypes.EQU_PART_HEAD):
            if showMsg:
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_PREVIEW, ())
            return False
        return True

    def addItem(self, item):
        if item and item.ctrlPreviewEffect():
            clientcom.previewEffect(BigWorld.player(), item.id)
            return
        if self.checkItemPreview(item):
            self.item = copy.deepcopy(item)
            self.itemList = ()
            if not self.mediator:
                self.show()
            else:
                self.showFitting()

    def addItems(self, items):
        for item in items:
            if not self.checkItemPreview(item):
                return

        self.showItems = items
        self.showType = TYPE_MULTIITEM
        if not self.mediator:
            self.hideResetBtn = True
            self.show()
        else:
            self.showFitting()

    def createAspect(self, aspect, item):
        if item.equipType not in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON, Item.EQUIP_BASETYPE_WEAPON_RUBBING):
            isShowFashion = False
            if item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType not in Item.EQUIP_FASHION_WEAR and item.equipSType != Item.EQUIP_FASHION_SUBTYPE_HEAD:
                isShowFashion = True
            if item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in (Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE, Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT, Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR):
                headId = aspect.fashionHead
                if charRes.getHeadType(headId) == charRes.HEAD_TYPE1:
                    aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
            parts = list(item.wherePreview())
            parts.extend(uiUtils.getAspectParts(item.id))
            if isShowFashion:
                for part in charRes.PARTS_ASPECT_FASHION:
                    equipId = getattr(aspect, part)
                    if equipId:
                        equItem = Item(equipId)
                        equipParts = list(equItem.wherePreview())
                        equipParts.extend(uiUtils.getAspectParts(equItem.id))
                        for itemPart in parts:
                            if itemPart in equipParts:
                                setattr(aspect, part, 0)
                                break

            for part in parts:
                itemId = item.rubbing if getattr(item, 'rubbing', 0) else item.id
                aspect.set(part, itemId, getattr(item, 'dyeList', ()), getattr(item, 'enhLv', 0), getattr(item, 'rongGuang', []))

            return isShowFashion
        return False

    def isShowFashion(self, aspect):
        for partName in charRes.PARTS_ASPECT_FASHION:
            if partName != 'fashionHead' and getattr(aspect, partName, None):
                return True

        return False

    def getHomeFurnitureMpr(self, homeFurniture):
        realPhysqiue = homeFurniture.realPhysique
        aspect = copy.deepcopy(homeFurniture.realAspect)
        avatarConfig = homeFurniture.avatarConfig
        mpr = charRes.MultiPartRes()
        isShowFashion = True
        mpr.applyConfig = False
        mpr.queryByAttribute(realPhysqiue, aspect, isShowFashion, avatarConfig)
        return (mpr, aspect, isShowFashion)

    def getMultiEquipMpr(self):
        p = BigWorld.player()
        realPhysqiue = p.realPhysique
        aspect = copy.deepcopy(p.realAspect)
        avatarConfig = p.avatarConfig
        mpr = charRes.MultiPartRes()
        isShowFashion = True
        for item in self.showItems:
            if item:
                if self.checkBonusData(item):
                    items = self.getBonusData(item)
                    for item in items:
                        if item.type == Item.BASETYPE_EQUIP:
                            if not item.isWingOrRide():
                                isShowFashion |= self.createAspect(aspect, item)
                            if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                                isShowFashion = False

                elif self.checkUunlockMorpher(item):
                    data = CID.data.get(item.id, {})
                    if data.has_key('faxing_style'):
                        if realPhysqiue == p.realPhysique:
                            realPhysqiue = copy.deepcopy(realPhysqiue)
                        realPhysqiue.hair = data['faxing_style']
                        aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
                    elif data.has_key('zhuangshi_style'):
                        avatarConfig = self.createAvatarConfig(avatarConfig, data['zhuangshi_style'])
                elif self.checkZhuangshiItem(item):
                    data = CID.data.get(item.id, {})
                    avatarConfig = self.createAvatarConfig(avatarConfig, data.get('zhuangshi', 1))
                else:
                    if not item.isWingOrRide():
                        isShowFashion |= self.createAspect(aspect, item)
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
        isShowFashion = self.isShowFashion(aspect)
        if self.item:
            if self.checkBonusData(self.item):
                items = self.getBonusData(self.item)
                for item in items:
                    if item.type == Item.BASETYPE_EQUIP:
                        if not item.isWingOrRide():
                            isShowFashion |= self.createAspect(aspect, item)
                        if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                            isShowFashion = False

            elif self.checkUunlockMorpher(self.item):
                data = CID.data.get(self.item.id, {})
                if data.has_key('faxing_style'):
                    if realPhysqiue == p.realPhysique:
                        realPhysqiue = copy.deepcopy(realPhysqiue)
                    realPhysqiue.hair = data['faxing_style']
                    aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
                elif data.has_key('zhuangshi_style'):
                    avatarConfig = self.createAvatarConfig(avatarConfig, data['zhuangshi_style'])
            elif self.checkZhuangshiItem(self.item):
                data = CID.data.get(self.item.id, {})
                avatarConfig = self.createAvatarConfig(avatarConfig, data.get('zhuangshi', 1))
            else:
                item = self.item
                if not item.isWingOrRide():
                    isShowFashion |= self.createAspect(aspect, item)
                if item.equipType == Item.EQUIP_BASETYPE_ARMOR and not item.isWingOrRide() or item.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING:
                    isShowFashion = False
        mpr.queryByAttribute(realPhysqiue, aspect, isShowFashion, avatarConfig)
        return (mpr, aspect, isShowFashion)

    def createAvatarConfig(self, avatarConfig, zhuangshiStyle):
        config = strmap.strmap(avatarConfig)
        headDyes = config.get('headDyes')
        headDyes = headDyes.split('\n')
        for i, item in enumerate(headDyes):
            key, value = item.split(':')
            if key.isdigit():
                if int(key) == AMU.DYE_U2M_MAPPING['zhuangshi_style'][0]:
                    headDyes[i] = '%s:%d' % (key, zhuangshiStyle)
                if int(key) == AMU.DYE_U2M_MAPPING['zhuangshi_density'][0]:
                    headDyes[i] = '%s:%f' % (key, 1.0)

        headDyes = '\n'.join(headDyes)
        config.set('headDyes', headDyes)
        return str(config)

    def getMpr(self):
        if self.item and self.item.type == Item.BASETYPE_FURNITURE:
            res = HomeFurniture.getModelPath(self.item.id)
            aspect = None
            isShowFashion = False
            return (res, aspect, isShowFashion)
        else:
            mpr, aspect, isShowFashion = self.getEquipMpr()
            res = mpr.getPrerequisites()
            return (res, aspect, isShowFashion)

    def getMultiMpr(self):
        mpr, aspect, isShowFashion = self.getMultiEquipMpr()
        res = mpr.getPrerequisites()
        return (res, aspect, isShowFashion)

    def showFitting(self):
        if self.mediator:
            res = aspect = showFashion = None
            if self.showType == TYPE_MULTIITEM:
                res, aspect, showFashion = self.getMultiMpr()
            else:
                res, aspect, showFashion = self.getMpr()
            self.initHeadGen()
            self.takePhoto3D(res, True, {'aspect': aspect,
             'showFashion': showFashion,
             'showAvatar': self.isShowAvatar()})

    def takePhoto3D(self, res, isFittingRoom = False, extraInfo = {}):
        if not self.headGen:
            self.headGen = capturePhoto.FittingRoomPhotoGen.getInstance('gui/taskmask.tga', 542)
        self.headGen.startCaptureEntAndRes(BigWorld.player(), res, isFittingRoom, extraInfo)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.FittingRoomPhotoGen.getInstance('gui/taskmask.tga', 542)
        self.headGen.initFlashMesh()

    def takeMallPhoto3D(self, res, isFittingRoom = False, extraInfo = {}):
        if not self.mallHeadGen:
            self.mallHeadGen = capturePhoto.CombineMallPhotoGen.getInstance('gui/taskmask.tga', 460)
        self.mallHeadGen.startCaptureEntAndRes(BigWorld.player(), res, isFittingRoom, extraInfo)
        self.uiAdapter.tianyuMall.setLoadingMcVisible(True)

    def resetMallHeadGen(self):
        if self.mallHeadGen:
            self.mallHeadGen.endCapture()
        self.figureInfo = None
        self.dyeList = ()
        self.uiAdapter.tianyuMall.setLoadingMcVisible(False)

    def initMallHeadGen(self):
        if not self.mallHeadGen:
            self.mallHeadGen = capturePhoto.CombineMallPhotoGen.getInstance('gui/taskmask.tga', 460)
        self.mallHeadGen.initFlashMesh()
        self.mallHeadGen.setModelFinishCallback(self.afterPlayerModelFinished)

    def afterPlayerModelFinished(self):
        self.uiAdapter.tianyuMall.setLoadingMcVisible(False)

    def restorePhoto3D(self):
        self.item = None
        p = BigWorld.player()
        self.originalAspect = copy.deepcopy(p.aspect)
        res, aspect, showFashion = self.getMpr()
        self.takeMallPhoto3D(res, True, {'aspect': aspect,
         'showFashion': showFashion,
         'physique': self.getPhysique() if self.figureInfo else None,
         'showAvatar': self.isShowAvatar()})

    def getFashionDesc(self, item = None):
        if not item:
            item = self.item
        desc = gameStrings.TEXT_FITTINGROOMPROXY_447
        if item:
            if self.checkBonusData(item):
                items = self.getBonusData(item)
            else:
                items = [item]
            for item in items:
                if item.isWingOrRide():
                    desc = gameStrings.TEXT_FITTINGROOMPROXY_455
                elif ED.data.get(item.id, {}).get('attachedWear', 0) in attachedModel.WEAR_ATTACH_ACTION_TYPE:
                    desc = gameStrings.TEXT_FITTINGROOMPROXY_457

        return desc

    def isWearBtnShow(self):
        if self.item:
            if self.checkBonusData(self.item):
                items = self.getBonusData(self.item)
            else:
                items = [self.item]
            for item in items:
                if ED.data.get(item.id, {}).get('attachedWear', 0) in attachedModel.WEAR_ATTACH_ACTION_TYPE:
                    return True

        return False

    def updateFigure(self):
        if self.item:
            if self.checkBonusData(self.item):
                items = self.getBonusData(self.item)
            else:
                items = [self.item]
            for item in items:
                if item.isWingOrRide():
                    item.rideWingStage = item.maxRideWingStage
                    if self.mediator:
                        self.showFitting()
                    else:
                        self.showMallItem()
                    break
                elif ED.data.get(item.id, {}).get('attachedWear', 0) in attachedModel.WEAR_ATTACH_ACTION_TYPE:
                    attachedwearType = ED.data.get(item.id, {}).get('attachedWear', 0)
                    if self.mediator:
                        model = self.headGen.adaptor.attachment
                        self.attachWearItem(model, item, attachedwearType)
                    else:
                        model = self.mallHeadGen.adaptor.attachment
                        self.attachWearItem(model, item, attachedwearType)

    def checkBonusData(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and (CID.data.get(item.id, {}).has_key('itemSetInfo') or CID.data.get(item.id, {}).has_key('needReMapBonusId'))

    def checkUunlockMorpher(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and getattr(item, 'cstype', 0) == Item.SUBTYPE_2_UNLOCK_MORPHER

    def checkZhuangshiItem(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and getattr(item, 'cstype', 0) == Item.SUBTYPE_2_ZHUANGSHI

    def getBonusData(self, item):
        if self.checkBonusData(item):
            if not (self.item and self.item.id == item.id and self.itemList):
                if 'itemSetInfo' in CID.data.get(item.id, {}):
                    bonusSetId, _ = CID.data.get(item.id, {}).get('itemSetInfo', (0, 0))
                    if bonusSetId:
                        bsd = BSD.data.get(bonusSetId, [])
                        items = [ Item(data['bonusId']) for data in bsd if data.get('bonusType', 0) == gametypes.BONUS_TYPE_ITEM and data.get('bonusRate', 0) == 10000 ]
                        if bsd and bsd[0].get('calcType') in (0, 1):
                            items = utils.filtItemByConfig(items, lambda e: e.id)
                        self.itemList = items
                        for item in self.itemList:
                            item.oldDyeList = getattr(item, 'dyeList', ())

                elif 'needReMapBonusId' in CID.data.get(item.id, {}):
                    itemIdList = []
                    tipUtils._getItemBoxRewardList(CID.data.get(item.id, {}), item.id, itemIdList, [])
                    self.itemList = [ Item(itemInfo[0]) for itemInfo in itemIdList ]
                    for item in self.itemList:
                        item.oldDyeList = getattr(item, 'dyeList', ())

            for item in self.itemList:
                if self.dyeList and self.isCanDye():
                    item.dyeList = self.dyeList
                elif getattr(item, 'oldDyeList', ()):
                    item.dyeList = item.oldDyeList

            return self.itemList
        return []

    def needHideWeapon(self, item = None, originalAspect = None):
        if not originalAspect:
            originalAspect = self.originalAspect
        if originalAspect:
            if originalAspect.backwear or originalAspect.waistwear:
                return True
        if not item:
            item = self.item
        if not item:
            return False
        items = []
        if self.checkBonusData(item):
            items = self.getBonusData(item)
        else:
            items = [item]
        for item in items:
            if getattr(item, 'equipSType', 0) in (Item.EQUIP_FASHION_SUBTYPE_WAISTWEAR, Item.EQUIP_FASHION_SUBTYPE_BACKWEAR):
                return True

        return False

    def withFashionBack(self, showItems = None):
        if not showItems:
            showItems = self.showItems
        for item in showItems:
            if getattr(item, 'equipSType', 0) in (Item.EQUIP_FASHION_SUBTYPE_WAISTWEAR, Item.EQUIP_FASHION_SUBTYPE_BACKWEAR):
                return True

        return False

    def needHideHairWear(self, item = None):
        if not item:
            item = self.item
        if not item:
            return False
        items = []
        if self.checkBonusData(item):
            items = self.getBonusData(item)
        else:
            items = [item]
        for item in items:
            if getattr(item, 'equipSType', 0) in (Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE, Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT, Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR):
                return True
            if getattr(item, 'equipSType', 0) == Item.EQUIP_FASHION_SUBTYPE_HEAD:
                headType = charRes.getHeadType(item.id)
                if headType == charRes.HEAD_TYPE1:
                    return True

        return False

    def needHideFaceWear(self, item = None):
        if not item:
            item = self.item
        if not item:
            return False
        items = []
        if self.checkBonusData(item):
            items = self.getBonusData(item)
        else:
            items = [item]
        for item in items:
            if getattr(item, 'equipSType', 0) == Item.EQUIP_FASHION_SUBTYPE_HEAD and charRes.getHeadType(item.id) == charRes.HEAD_TYPE1:
                return True

        return False

    def isPbrEquip(self):
        if not self.item:
            return False
        items = []
        if self.checkBonusData(self.item):
            items = self.getBonusData(self.item)
        else:
            items = [self.item]
        for item in items:
            if clientcom.isPbrEquip(item.id):
                return True

        return False

    def setFigureInfo(self, xmlName):
        if xmlName:
            sect = ResMgr.openSection('config/avatar/char/%s.xml' % xmlName)
            self.figureInfo = clientcom._getAvatarConfigFromFile(sect)
        else:
            self.figureInfo = None
        if self.item:
            self.addMallItem(self.item)
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.NO_FASHION_PREVIEW, ())

    def getPhysique(self):
        p = BigWorld.player()
        if self.figureInfo:
            realPhysique = physique.Physique({})
            realPhysique.school = p.school
            realPhysique.sex = self.figureInfo['sex']
            realPhysique.bodyType = self.figureInfo['bodyType']
            realPhysique.hair = self.figureInfo['hair']
        else:
            realPhysique = p.realPhysique
        return realPhysique

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
            return self.figureInfo['avatarConfig']
        return p.avatarConfig

    def setDyeList(self, dyeList):
        if self.mallHeadGen:
            model = self.mallHeadGen.adaptor.attachment
            self.setModelDyeList(dyeList, model)

    def isCanDye(self):
        if not self.item:
            return False
        if self.checkBonusData(self.item):
            bonusSetId, _ = CID.data.get(self.item.id, {}).get('itemSetInfo', (0, 0))
            if bonusSetId:
                items = [ Item(data['bonusId']) for data in BSD.data.get(bonusSetId, []) if data.get('bonusType', 0) == gametypes.BONUS_TYPE_ITEM ]
                items = utils.filtItemByConfig(items, lambda e: e.id)
                for it in items:
                    if it.isCanDye():
                        return True

        else:
            return self.item.isCanDye()
        return False

    def enterFullScreenModelFitting(self, homeFurniture, callback = None):
        p = BigWorld.player()
        if not p.stateMachine.checkStatus(const.CT_OPEN_FULL_SCREEN_MODEL_FITTING_ROOM):
            return
        self.leaveFullScreenModelFitting()
        self.homeFurniture = homeFurniture
        if not self.fittingModel:
            clientcom.fetchAvatarModel(homeFurniture, gameglobal.getLoadThread(), Functor(self.afterFittingModelFinished, callback))
        else:
            self.afterFittingModelFinished(callback, self.model)

    def refreshModelFitting(self, homeFurniture, callback = None):
        p = BigWorld.player()
        if self.fittingModel:
            if self.fittingModel.inWorld:
                p.delModel(self.fittingModel)
            self.fittingModel.texturePriority = 0
            TA.ta_reset([self.fittingModel])
            self.fittingModel = None
        if self.fittingModelUpdater:
            self.fittingModelUpdater.release()
            self.fittingModelUpdater = None
        self.homeFurniture = homeFurniture
        clientcom.fetchAvatarModel(homeFurniture, gameglobal.getLoadThread(), Functor(self.afterRefreshFittingModelFinished, callback))

    def refreshSameModelFitting(self, homeFurniture, callback = None):
        if not self.fittingModel:
            return
        else:
            p = BigWorld.player()
            resOld = list(self.fittingModel.sources)
            tints = TA._get_matter_tint_data(self.fittingModel)
            mpr, aspect, isShowFashion = self.getHomeFurnitureMpr(homeFurniture)
            res = mpr.getPrerequisites()
            if not self.fittingModelUpdater:
                self.fittingModelUpdater = seqTask.SeqModelUpdater(self.fittingModel, gameglobal.getLoadThread(), Functor(self.afterModelFittingPartUpdate, mpr, callback))
            else:
                self.fittingModelUpdater.modelOkCallback = Functor(self.afterModelFittingPartUpdate, mpr, callback)
            if set(resOld) == set(res):
                self.fittingModelUpdater.modelOkCallback()
            else:
                self.fittingModelUpdater.beginUpdate(resOld, res, None, None, tints)
            return

    def afterModelFittingPartUpdate(self, mpr, callback):
        self._dyeModel(mpr, self.fittingModel, True)
        if callback:
            callback()

    def afterRefreshFittingModelFinished(self, callback, model):
        self.setFittingModelFinished(model)
        if callback:
            callback()

    def leaveFullScreenModelFitting(self):
        p = BigWorld.player()
        p.restoreAllNearby()
        self.homeFurniture = None
        if self.fittingModel:
            if self.fittingModel.inWorld:
                p.delModel(self.fittingModel)
            self.fittingModel.texturePriority = 0
            TA.ta_reset([self.fittingModel])
            self.fittingModel = None
        p.unlockKey(gameglobal.KEY_POS_UI)
        if self.fittingModelUpdater:
            self.fittingModelUpdater.release()
            self.fittingModelUpdater = None
        gameglobal.rds.loginScene.setPlayer(None, None)
        self.reset()
        self.removeFullScreenEffect()
        self.detachEffect()
        if self.lightDummyModel:
            sfx.giveBackDummyModel(self.lightDummyModel)
            self.lightDummyModel = None

    def setFittingModelFinished(self, model):
        if not self.fittingModel:
            self.fittingModel = model
        p = BigWorld.player()
        if not self.fittingModel.inWorld:
            p.addModel(self.fittingModel)
        self.fittingModel.texturePriority = 100
        self.fittingModel.position = p.position
        self.fittingModel.yaw = 0
        actionId = self.homeFurniture.getDefaultShowAction() if self.homeFurniture else '1101'
        try:
            self.fittingModel.action(actionId)()
        except:
            pass

        self.fittingModel.expandVisibilityBox(10)
        self.homeFurniture.clearCloneAttachment(model)
        clientcom.cloneEntityAllAttachments(self.homeFurniture, model, True)
        gameglobal.rds.loginScene.setPlayer(self.homeFurniture, self.fittingModel)

    def afterFittingModelFinished(self, callback, model):
        p = BigWorld.player()
        self.setFittingModelFinished(model)
        c = BigWorld.camera()
        if hasattr(c, 'boundRemain'):
            c.boundRemain = 0.6
        p.hideAllNearby()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self.addFullScreenEffect()
        self.fashionEffects = clientcom.attachFashionEffect(p, self.fittingModel)
        if callback:
            callback()

    def enterFullScreenFitting(self, callback = None, spaceLimit = True):
        p = BigWorld.player()
        if p.inSwim in (const.DEEPWATER, const.SHOALWATER):
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_FITTINGROOMPROXY_782)
            return
        if p.inCombat:
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_FITTINGROOMPROXY_785)
            return
        if spaceLimit and p.mapID != const.SPACE_NO_BIG_WORLD:
            p.showGameMsg(GMDD.data.USE_IN_BIG_WORLD, ())
            return
        if not p.stateMachine.checkStatus(const.CT_OPEN_FULL_SCREEN_FITTING_ROOM):
            return
        self.leaveFullScreenFitting()
        if not self.model:
            clientcom.fetchAvatarModel(p, gameglobal.getLoadThread(), Functor(self.afterModelFinished, callback))
        else:
            self.afterModelFinished(callback, self.model)

    def afterModelFinished(self, callback, model):
        if not self.model:
            self.model = model
        p = BigWorld.player()
        if not self.model.inWorld:
            p.addModel(self.model)
        self.model.texturePriority = 100
        self.model.position = p.position
        self.model.yaw = 0
        self.model.action('1101')()
        self.model.expandVisibilityBox(10)
        clientcom.cloneEntityAllAttachments(p, model, True)
        gameglobal.rds.loginScene.setPlayer(p, self.model)
        rongGuang = charRes.RongGuangRes()
        mpr, aspect, isShowFashion = self.getEquipMpr()
        rongGuang.queryByAvatar(p)
        rongGuang.apply(self.model)
        c = BigWorld.camera()
        if hasattr(c, 'boundRemain'):
            c.boundRemain = 0.6
        p.hideAllNearby()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self.addFullScreenEffect()
        self.fashionEffects = clientcom.attachFashionEffect(p, self.model)
        self.dyeList = ()
        if callback:
            callback()

    def addFullScreenEffect(self):
        p = BigWorld.player()
        p.setBlackScreenEff(blackEffectManager.SRC_FITTINGROOM, True)
        self.attachEffect(self.FX_INDEX_FASHION)

    def removeFullScreenEffect(self):
        p = BigWorld.player()
        if hasattr(BigWorld, 'fittingRoom'):
            if not gameglobal.rds.ui.wardrobe.widget:
                p.setBlackScreenEff(blackEffectManager.SRC_FITTINGROOM, False)

    def leaveFullScreenFitting(self):
        p = BigWorld.player()
        p.restoreAllNearby()
        if self.rideModel and self.rideModel.inWorld:
            self.rideModel.texturePriority = 0
            p.delModel(self.rideModel)
            TA.ta_reset([self.rideModel])
            self.rideModel = None
        if self.model:
            if self.model.inWorld:
                p.delModel(self.model)
            self.model.texturePriority = 0
            TA.ta_reset([self.model])
            self.model = None
        self.wingModel = None
        self.addedItemList = []
        self.addedItemDict = {}
        p.unlockKey(gameglobal.KEY_POS_UI)
        if self.modelUpdater:
            self.modelUpdater.release()
            self.modelUpdater = None
        gameglobal.rds.loginScene.setPlayer(None, None)
        self.reset()
        self.removeFullScreenEffect()
        self.applyBare = False
        self.hpNodeList = []
        self.detachEffect()
        self.originalAspect = None
        self.dyeList = ()
        if self.lightDummyModel:
            sfx.giveBackDummyModel(self.lightDummyModel)
            self.lightDummyModel = None
        self.playerModelFinishCallback = None

    def addFullScreenItem(self, item):
        if self.checkItemPreview(item):
            self.item = item
            self.itemList = ()
            self.item.oldDyeList = getattr(self.item, 'dyeList', ())
            if self.dyeList and self.isCanDye():
                self.item.dyeList = self.dyeList
            itemList = [item]
            if self.checkBonusData(item):
                itemList = self.getBonusData(item)
            if not self.originalAspect:
                if self.applyBare:
                    self.originalAspect = appearance.Appearance({})
                else:
                    p = BigWorld.player()
                    self.originalAspect = copy.deepcopy(p.aspect)
            for subItem in itemList:
                if subItem.wherePreview():
                    equipParts = list(subItem.wherePreview())
                    equipParts.extend(uiUtils.getAspectParts(subItem.id))
                    if gametypes.EQU_PART_RIDE in equipParts:
                        index = equipParts.index(gametypes.EQU_PART_RIDE)
                        equipParts[index] = gametypes.EQU_PART_WINGFLY
                    for equipPart in equipParts:
                        if self.addedItemDict.has_key(equipPart):
                            oldSubItem, oldItem = self.addedItemDict.pop(equipPart)
                            if oldItem:
                                self.addedItemList.remove(oldItem)

                    self.addedItemDict[equipParts[0]] = (subItem, item)

            self.addedItemList.append(item)
            mpr, aspect, isShowFashion = self.getEquipMpr()
            self.addItemAction()
            self.bodyPartUpdate(mpr, aspect, isShowFashion)

    def addItemAction(self):
        showAction = MCD.data.get('showAction', '1911')
        if self.model and showAction not in self.model.queue:
            p = BigWorld.player()
            p.fashion.playActionSequence(self.model, (showAction, '1101'), None)

    def delFullScreenItem(self, delItem):
        itemList = [delItem]
        if self.checkBonusData(delItem):
            itemList = self.getBonusData(delItem)
        for subItem in itemList:
            if subItem.wherePreview():
                equipPart = subItem.wherePreview()[0]
                if gametypes.EQU_PART_RIDE == equipPart:
                    equipPart = gametypes.EQU_PART_WINGFLY
                if self.addedItemDict.has_key(equipPart):
                    oldSubItem, oldItem = self.addedItemDict.pop(equipPart)
                    if oldItem:
                        self.addedItemList.remove(oldItem)

        p = BigWorld.player()
        if not self.addedItemList:
            self.restoreModel(self.applyBare)
        else:
            if self.model:
                self.model.action('1101')()
            if self.applyBare:
                self.originalAspect = appearance.Appearance({})
            else:
                self.originalAspect = copy.deepcopy(p.aspect)
            for i, item in enumerate(self.addedItemList):
                self.item = item
                self.itemList = ()
                self.item.oldDyeList = getattr(self.item, 'dyeList', ())
                if self.dyeList and self.isCanDye():
                    self.item.dyeList = self.dyeList
                mpr, aspect, isShowFashion = self.getEquipMpr()
                if i == len(self.addedItemList) - 1:
                    self.bodyPartUpdate(mpr, aspect, isShowFashion)

    def restoreModel(self, applyBare = False):
        self.item = None
        self.addedItemList = []
        self.addedItemDict = {}
        p = BigWorld.player()
        self.applyBare = applyBare
        if applyBare:
            self.originalAspect = appearance.Appearance({})
        else:
            self.originalAspect = copy.deepcopy(p.aspect)
        mpr, aspect, isShowFashion = self.getEquipMpr()
        self.bodyPartUpdate(mpr, aspect, isShowFashion)
        if self.model:
            self.model.action('1101')()

    def setFullScreenModel(self, dyeList):
        self.setModelDyeList(dyeList, self.model)

    def setModelDyeList(self, dyeList, model):
        self.dyeList = dyeList
        p = BigWorld.player()
        if self.item and model:
            if not self.isCanDye():
                p.showGameMsg(GMDD.data.EQUIP_CANNOT_DYE, ())
                return
            if self.dyeList:
                self.item.dyeList = self.dyeList
            elif getattr(self.item, 'oldDyeList', ()):
                self.item.dyeList = self.item.oldDyeList
            mpr, aspect, _ = self.getEquipMpr()
            physique = self.getPhysique()
            avatarConfig = self.getAvatarConfig()
            if mpr and model:
                m = AM.SimpleModelMorpher(model, physique.sex, physique.school, physique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, cape=mpr.cape)
                m.readConfig(avatarConfig)
                m.applyDyeMorph(True)
                if not self.needHideHairWear():
                    node = model.node('biped Head')
                    if node and node.attachments:
                        for hModel in node.attachments:
                            clientcom.setHairNodeDyeByAspect(aspect, hModel)

        else:
            p.showGameMsg(GMDD.data.NO_FASHION_PREVIEW, ())

    def bodyPartUpdate(self, mpr, aspect, showFashion):
        if not self.model:
            return
        else:
            if not self.modelUpdater:
                self.modelUpdater = seqTask.SeqModelUpdater(self.model, gameglobal.getLoadThread(), Functor(self.afterBodyPartUpdate, mpr, aspect, showFashion))
            else:
                self.modelUpdater.modelOkCallback = Functor(self.afterBodyPartUpdate, mpr, aspect, showFashion)
            resOld = list(self.model.sources)
            mpr.applyConfig = False
            res = mpr.getPrerequisites()
            tints = TA._get_matter_tint_data(self.model)
            if set(resOld) == set(res):
                self.modelUpdater.modelOkCallback()
            else:
                self.modelUpdater.beginUpdate(resOld, res, None, None, tints)
            return

    def detachEffect(self):
        if self.lightDummyModel:
            self.lightDummyModel.root.attachments = []
        self.lightEffect = None
        self.lightEffectIndex = None

    def attachEffect(self, fxIndex):
        if fxIndex == self.lightEffectIndex:
            return
        self.detachEffect()
        self.lightEffectIndex = fxIndex
        p = BigWorld.player()
        if not self.lightDummyModel:
            self.lightDummyModel = sfx.getDummyModel(True)
            self.lightDummyModel.position = p.position
        try:
            fxPath = sfx.getPath(self.lightEffectId[fxIndex])
            self.lightEffect = clientUtils.pixieFetch(fxPath, p.getEquipEffectLv())
            self.lightEffect.clear()
            self.lightEffect.force()
            self.lightDummyModel.root.attach(self.lightEffect)
        except:
            pass

    def afterBodyPartUpdate(self, mpr, aspect, showFashion):
        self._dyeModel(mpr, self.model)
        rongGuang = charRes.RongGuangRes()
        mpr, aspect, isShowFashion = self.getEquipMpr()
        rongGuang.queryByAttribute(aspect, isShowFashion)
        rongGuang.apply(self.model)
        p = BigWorld.player()
        if self.rideModel:
            self.rideModel.setHP('HP_ride', None)
            p.delModel(self.rideModel)
            self.rideModel = None
            p.addModel(self.model)
            self.model.position = p.position
            gameglobal.rds.loginScene.lookModel = self.model
            self.model.action('1101')()
            CC.initCC(False, 0.6)
            CC.TC.followMovementHalfLife = 0.1
            gameglobal.rds.loginScene.zoomTo(0)
        if self.wingModel:
            self.model.setHP('HP_back', None)
            self.wingModel = None
            self.model.action('1101')()
            CC.initCC(False, 1.0)
            gameglobal.rds.loginScene.zoomTo(0)
            self.model.position = p.position
        self.attachEffect(self.FX_INDEX_FASHION)
        self.detachAllModel()
        self.attachAllModel()
        self.addItemEffect()
        if self.fashionEffects:
            for fx in self.fashionEffects:
                fx.stop()

        p = BigWorld.player()
        self.fashionEffects = clientcom.attachFashionEffect(p, self.model, aspect)
        if self.playerModelFinishCallback:
            self.playerModelFinishCallback()

    def addItemEffect(self):
        if self.item:
            quality = self.item.quality
            qualityEffect = MCD.data.get('qualityEffect', [10101,
             10101,
             10102,
             10102,
             10103,
             10103,
             10103])
            p = BigWorld.player()
            if qualityEffect and quality < len(qualityEffect):
                effect = qualityEffect[quality]
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
                 p.getEquipEffectPriority(),
                 self.model,
                 effect,
                 sfx.EFFECT_LIMIT_MISC))

    def detachAllModel(self):
        if not self.hpNodeList:
            self.hpNodeList = [ node for node in self.model.nodeList() if node[0:2] == 'HP' ]
        try:
            for node in self.hpNodeList:
                self.model.setHP(node, None)

            hairNode = self.model.node('biped Head')
            if hairNode:
                hairNode.attachments = []
            hpRoot = self.model.node('HP_root')
            if hpRoot:
                hpRoot.attachments = []
        except:
            pass

    def attachAllModel(self):
        ent = BigWorld.player()
        physique = None
        if self.figureInfo:
            physique = self.getPhysique()
        if not self.needHideHairWear():
            clientcom.cloneEntityHairWearAttachments(ent, self.model, True)
        if not physique and not self.applyBare:
            if not self.needHideFaceWear():
                clientcom.cloneEntityFaceWearAttachments(ent, self.model, True)
            clientcom.cloneEntityOtherWearAttachments(ent, self.model, True)
            if not self.needHideWeapon():
                clientcom.cloneEntityAllWeaponAttachments(ent, self.model, True)
        if self.item:
            if self.originalAspect:
                originalAspect = self.originalAspect
                for part in gametypes.EQU_PART_WEARS:
                    partName = gametypes.ASPECT_PART_REV_DICT[part]
                    if getattr(originalAspect, partName, None) and getattr(ent.realAspect, partName, None) != getattr(originalAspect, partName, None):
                        itemNew = Item(getattr(originalAspect, partName))
                        self.setAttachMent(ent, self.model, itemNew, True, self.beforeSetAttachment, self.afterSetAttachment)

            item = self.item
            if self.checkBonusData(item):
                items = self.getBonusData(item)
                for item in items:
                    self.setAttachMent(ent, self.model, item, True, self.beforeSetAttachment, self.afterSetAttachment)

            else:
                self.setAttachMent(ent, self.model, item, True, self.beforeSetAttachment, self.afterSetAttachment)

    def beforeSetAttachment(self, ent, model, item, hangUp = True):
        p = BigWorld.player()
        if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
            if item.wherePreview()[0] == gametypes.EQU_PART_RIDE:
                p.delModel(model)

    def setCameraAndYaw(self, model):
        if not model:
            return
        path = model.sources[0]
        modelId = path.split('/')[-1].split('.')[0]
        cameraInfo, yaw = gameglobal.rds.loginScene.loadCameraAndYaw(modelId)
        if cameraInfo:
            if CC.TC and hasattr(CC.TC, 'cameraDHProvider'):
                targetMatrix = model.matrix
                CC.playCC(0.4, cameraInfo, targetMatrix)
            if yaw:
                model.yaw = yaw
            gameglobal.rds.loginScene.trackNo = 3
        else:
            gameglobal.rds.loginScene.zoomTo(3)

    def afterSetAttachment(self, ent, model, newModel, item, hangUp = True, scale = 0):
        p = BigWorld.player()
        if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
            if not newModel:
                return
            if item.wherePreview()[0] == gametypes.EQU_PART_RIDE:
                p.addModel(newModel)
                self.rideModel = newModel
                newModel.position = p.position
                gameglobal.rds.loginScene.lookModel = self.rideModel
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                if scale:
                    newModel.scale = (scale, scale, scale)
                self.setCameraAndYaw(newModel)
                ed = ED.data.get(item.id, {})
                rideActionList = []
                if self.rideModel:
                    rideActionList = self.rideModel.actionNameList()
                rideShowAction = MCD.data.get('rideShowAction', ['11220', '11219'])
                if not rideActionList or not set(rideShowAction).issubset(set(rideActionList)):
                    rideAction = ed.get('horseShowAction', None)
                    if rideAction:
                        rideShowAction = (rideAction,)
                charShowAction = ed.get('charShowAction', None)
                if not charShowAction:
                    charShowAction = self.searchIdleAction(self.rideModel)
                p.fashion.playActionSequence(self.rideModel, rideShowAction, None)
                p.fashion.playActionSequence(self.model, (charShowAction,), None)
                self.attachEffect(self.FX_INDEX_RIDE)
                equipModel = p.modelServer.rideAttached
                attachments = equipModel.getAttachments(item.id, None, getattr(item, 'rideWingStage', 0))
                if newModel and newModel.inWorld and attachments:
                    attachments = attachments[0]
                    for effect in attachments[4]:
                        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
                         p.getEquipEffectPriority(),
                         newModel,
                         effect,
                         sfx.EFFECT_LIMIT_MISC))

            elif item.wherePreview()[0] == gametypes.EQU_PART_WINGFLY:
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                self.wingModel = newModel
                wingShowAction = MCD.data.get('wingShowAction', ['21101'])
                p.fashion.playActionSequence(self.wingModel, wingShowAction, None)
                p.fashion.playActionSequence(self.model, wingShowAction[-1:], None)
                self.setCameraAndYaw(self.model)
                self.model.position = p.position + (0, self.heightOffset, 0)
                self.attachEffect(self.FX_INDEX_WING)
        elif item.equipType == Item.EQUIP_BASETYPE_FASHION:
            if ED.data.get(item.id, {}).get('attachedWear', 0) == attachedModel.WEAR_ATTACH_ACTION:
                self.updateModelFigure('open')

    def searchIdleAction(self, model):
        if not model:
            return None
        else:
            for item in model.actionNamePair():
                if item[1].find('idle_a') != -1:
                    return item[0]

            return None

    def updateModelFigure(self, op = 'open'):
        if self.item:
            if self.checkBonusData(self.item):
                items = self.getBonusData(self.item)
            else:
                items = [self.item]
            for item in items:
                if ED.data.get(item.id, {}).get('attachedWear', 0) in attachedModel.WEAR_ATTACH_ACTION_TYPE:
                    attachedwearType = ED.data.get(item.id, {}).get('attachedWear', 0)
                    if attachedwearType == attachedModel.WEAR_ATTACH_ACTION:
                        self.attachWearItem(self.model, item, attachedwearType, op)
                    elif op == 'open':
                        self.attachWearItem(self.model, item, attachedwearType, op)

    def attachWearItem(self, model, item, attachedwearType = 1, op = 'open'):
        ent = BigWorld.player()
        if item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.EQUIP_FASHION_WEAR:
            equipModel = None
            hairNode = None
            if item.equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE:
                equipModel = ent.modelServer.headdress
                if model and model.node('biped Head'):
                    if model.node('biped Head').attachments:
                        hairNode = model.node('biped Head').attachments[0]
                    else:
                        hairNode = clientcom.getHairNode(ent, model)
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_FACEWEAR:
                equipModel = ent.modelServer.facewear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_WAISTWEAR:
                equipModel = ent.modelServer.waistwear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_BACKWEAR:
                equipModel = ent.modelServer.backwear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_TAILWEAR:
                equipModel = ent.modelServer.tailwear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_CHESTWEAR:
                equipModel = ent.modelServer.chestwear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_EARWEAR:
                equipModel = ent.modelServer.earwear
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR:
                equipModel = ent.modelServer.headdressRight
                if model and model.node('biped Head'):
                    if model.node('biped Head').attachments:
                        hairNode = model.node('biped Head').attachments[0]
                    else:
                        hairNode = clientcom.getHairNode(ent, model)
            elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_YUANLING:
                equipModel = ent.modelServer.yuanLing
            if not equipModel:
                return
            attachments = equipModel.getAttachments(item.id)
            try:
                if attachments:
                    for i in attachments:
                        if i[2]:
                            model.setHP(i[2], None)
                        if i[3]:
                            model.setHP(i[3], None)

            except:
                pass

            showAction = gameglobal.IDLEACT1
            actionSeq = [gameglobal.IDLEACT1]
            ed = ED.data.get(item.id, {})
            if attachedwearType == attachedModel.WEAR_ATTACH_ACTION:
                showWearId = ed.get('showWearId', 0)
                wsd = WSD.data.get(showWearId, {})
                key = clientcom.getAvatarKey(ent)
                if op == 'open':
                    showAction = wsd.get(key + 'IdleAction', '56105')
                    actionSeq = [showAction]
                elif op == 'show':
                    skills = wsd.get(key + 'Skills', [])
                    if skills:
                        skillId, skillLv = skills[0]
                        clientSkillInfo = ent.getClientSkillInfo(skillId, skillLv)
                        showAction = clientSkillInfo.getSkillData('castAct', [0, '1101'])[1]
                        actionSeq = [showAction, wsd.get(key + 'IdleAction', '56105')]
            showEffect = ed.get('previewEffect', ())
            if op == 'close':
                clientcom.cloneEntityModelWearAttachment(ent, attachments, model, hairNode, True, True, showAction, showEffect)
            else:
                clientcom.cloneEntityModelWearAttachment(ent, attachments, model, hairNode, False, True, showAction, showEffect)
            if actionSeq:
                ent.fashion.playActionSequence(model, actionSeq, None, releaseFx=False)

    def setAttachMent(self, ent, model, item, hangUp = True, beforeAttachFun = None, afterAttachFun = None):
        if not item or not hasattr(item, 'equipType'):
            return
        else:
            returnModel = None
            scale = 0
            if beforeAttachFun:
                beforeAttachFun(ent, model, item, hangUp)
            if item.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON, Item.EQUIP_BASETYPE_WEAPON_RUBBING):
                equipModel = ent.modelServer.leftWeaponModel
                enhLv = getattr(item, 'enhLv', 0)
                itemId = item.rubbing if getattr(item, 'rubbing', 0) else item.id
                subIdList = ED.data.get(itemId, {}).get('subId', [])
                attachments = []
                for i in xrange(0, len(subIdList)):
                    attachments.extend(equipModel.getAttachments(itemId, i, enhLv))

                returnModel = clientcom.cloneEntityModelAttachment(ent, attachments, model, hangUp, True)
            elif item.equipType == Item.EQUIP_BASETYPE_ARMOR:
                if item.wherePreview()[0] == gametypes.EQU_PART_RIDE:
                    equipModel = ent.modelServer.rideAttached
                    equipId = item.id
                    if hasattr(item, 'realDyeId'):
                        equipId = item.realDyeId
                    attachments = equipModel.getAttachments(equipId, None, getattr(item, 'rideWingStage', 0))
                    rScale = 1.0
                    try:
                        riderScale = ED.data.get(item.id, {}).get('riderScale', None)
                        scale = attachments[0][3]
                        if riderScale and attachments:
                            rScale = riderScale / scale
                    except:
                        rScale = 1.0

                    rideModel = clientcom.cloneBasicAttachment(ent, attachments, model, True, True, equipId, rScale)
                    returnModel = rideModel
                elif item.wherePreview()[0] == gametypes.EQU_PART_WINGFLY:
                    equipModel = ent.modelServer.wingFlyModel
                    attachments = equipModel.getAttachments(item.id, None, getattr(item, 'rideWingStage', 0))
                    wingModel = clientcom.cloneBasicAttachment(ent, attachments, model, True, False)
                    returnModel = wingModel
                    if hasattr(wingModel, 'texturePriority'):
                        wingModel.texturePriority = 100
            elif item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.EQUIP_FASHION_WEAR:
                equipModel = None
                hairNode = None
                if item.equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE:
                    equipModel = ent.modelServer.headdress
                    if model and model.node('biped Head') and model.node('biped Head').attachments:
                        hairNode = model.node('biped Head').attachments[0]
                    else:
                        hairNode = clientcom.getHairNode(ent, model)
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_FACEWEAR:
                    equipModel = ent.modelServer.facewear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_WAISTWEAR:
                    equipModel = ent.modelServer.waistwear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_BACKWEAR:
                    equipModel = ent.modelServer.backwear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_TAILWEAR:
                    equipModel = ent.modelServer.tailwear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_CHESTWEAR:
                    equipModel = ent.modelServer.chestwear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_EARWEAR:
                    equipModel = ent.modelServer.earwear
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR:
                    equipModel = ent.modelServer.headdressRight
                    if model and model.node('biped Head') and model.node('biped Head').attachments:
                        hairNode = model.node('biped Head').attachments[0]
                    else:
                        hairNode = clientcom.getHairNode(ent, model)
                elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_YUANLING:
                    equipModel = ent.modelServer.yuanLing
                if equipModel:
                    attachments = equipModel.getAttachments(item.id)
                    photoAction = equipModel.getPhotoAction(item.id)
                    returnModel = clientcom.cloneEntityModelWearAttachment(ent, attachments, model, hairNode, hangUp, True, photoAction)
            if afterAttachFun:
                afterAttachFun(ent, model, returnModel, item, hangUp, scale)
            return

    def _dyeModel(self, mpr, model, modelFitting = False):
        player = BigWorld.player()
        if modelFitting:
            player = self.homeFurniture
        if mpr and model:
            m = AM.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, cape=mpr.cape)
            m.readConfig(player.realAvatarConfig)
            m.applyDyeMorph(True)
            m.applyFaceMorph()

    def setPlayerModelFinishCallback(self, func):
        self.playerModelFinishCallback = func

    def isShowAvatar(self):
        if self.item and self.item.type == Item.BASETYPE_FURNITURE:
            return False
        return True
