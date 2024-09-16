#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyePlaneProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import utils
import gameglobal
import gametypes
import const
import clientcom
from guis import ui
from guis.uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from helpers import avatarMorpher as AM
from helpers import charRes
from helpers import tintalt as TA
from helpers import seqTask
from helpers import dyeMorpher
from callbackHelper import Functor
from item import Item
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import item_data as ID
from data import equip_data as ED
from cdata import material_dye_data as MAD
from cdata import game_msg_def_data as GMDD
from equipment import Equipment
DYE_ITEM_TYPE = (Item.EQUIP_FASHION_SUBTYPE_HEAD,
 Item.EQUIP_FASHION_SUBTYPE_BODY,
 Item.EQUIP_FASHION_SUBTYPE_HAND,
 Item.EQUIP_FASHION_SUBTYPE_LEG,
 Item.EQUIP_FASHION_SUBTYPE_SHOE,
 Item.EQUIP_FASHION_SUBTYPE_CAPE)

def cmp1(x1, x2):
    data1 = MAD.data.get(x1, {})
    data2 = MAD.data.get(x2, {})
    dyeType1 = data1.get('dyeType', 0)
    dyeType2 = data2.get('dyeType', 0)
    ret = cmp(dyeType1, dyeType2)
    if ret == 0:
        if data1.has_key('dyeQuality') and data2.has_key('dyeQuality'):
            dyeQuality1 = data1['dyeQuality']
            dyeQuality2 = data2['dyeQuality']
            ret = cmp(dyeQuality1, dyeQuality2)
            if ret == 0:
                return cmp(x1, x2)
            return ret
        return cmp(x1, x2)
    return ret


class DyePlaneProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(DyePlaneProxy, self).__init__(uiAdapter)
        self.bindType = 'dyePlane'
        self.type = 'dyePlane'
        self.modelMap = {'handleSliderChange': self.onHandleSliderChange,
         'handleTextureClick': self.onHandleClickTexture,
         'handleClickSlot': self.onHandleClickSlot,
         'handleOkClick': self.onHandleOkClick,
         'getInitData': self.onGetInitData,
         'unlockDualDye': self.unlockDualDye,
         'getUnlockData': self.onGetUnlockData,
         'clickUnlockClose': self.onClickUnlockClose,
         'clickUnlockConfirmBtn': self.onClickUnlockConfirmBtn,
         'setChannel': self.onSetChannel,
         'adjustColor': self.onAdjustColor,
         'handleColorClick': self.onHandleClickColor,
         'handleColorRareClick': self.onHandleColorRareClick,
         'handleAlphaSubClick': self.onHandleAlphaSubClick,
         'handleLightClick': self.onHandleLightClick,
         'handleLightSubClick': self.onHandleLightSubClick,
         'handleSelectSlot': self.onHandleSelectSlot,
         'handleClickRandom': self.onRandomDyeClick}
        self.colorNum = 0
        self.reset()
        self.med = None
        self.init()
        self.isShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_DYE_PLANE, self.close)
        self.model = None
        self.hairModel = None
        self.isSetEquip = False
        self.isHideAllUI = False
        self.modelUpdater = None
        self.dyeDisable = False
        self.isUpdating = False

    def init(self):
        items = MAD.data.keys()
        items.sort(cmp1)
        self.color_normal = []
        self.color_high = []
        self.color_rare = []
        self.color_random = []
        self.textureItems = []
        self.high_light = []
        for itemId in items:
            if MAD.data.get(itemId, {}).get('dyeType') == Item.CONSUME_DYE_NORMAL:
                if MAD.data.get(itemId, {}).get('dyeQuality') == 1:
                    self.color_normal.append(itemId)
                elif MAD.data.get(itemId, {}).get('dyeQuality') == 2:
                    self.color_high.append(itemId)
                elif MAD.data.get(itemId, {}).get('dyeQuality') == 3:
                    self.color_rare.append(itemId)
            elif MAD.data.get(itemId, {}).get('dyeType') == Item.CONSUME_DYE_RANDOM:
                self.color_random.append(itemId)
            elif MAD.data.get(itemId, {}).get('dyeType') == Item.CONSUME_DYE_TEXTURE:
                self.textureItems.append(itemId)
            elif MAD.data.get(itemId, {}).get('dyeType') == 7:
                self.high_light.append(itemId)

    def reset(self):
        self.resetData()
        self.dyeMap = {}
        self.isSetEquip = False
        self.fashionEffects = []

    def saveData(self, index = 0):
        if self.equipItem:
            map = {}
            self.dyeMap[index] = map
            map['equipPage'] = self.equipPage
            map['equipPos'] = self.equipPos
            map['equipItem'] = self.equipItem
            map['color'] = self.color
            map['dualColor'] = self.dualColor
            map['texture'] = self.texture
            map['textureSize'] = self.textureSize
            map['textureDensity'] = self.textureDensity
            map['textureDegree'] = self.textureDegree
            map['dyeNum'] = self.dyeNum
            map['dualDyeNum'] = self.dualDyeNum
            map['colorItemId'] = self.colorItemId
            map['textureItemId'] = self.textureItemId
            map['dualColorItemId'] = self.dualColorItemId
            map['dyeMethod'] = self.dyeMethod
            map['dualDyeMethod'] = self.dualDyeMethod
            map['channel'] = self.channel
            map['oldDyeList'] = self.oldDyeList
            map['resKind'] = self.resKind
            map['chooseColor0'] = self.chooseColor0
            map['chooseColor1'] = self.chooseColor1
            map['colorAlpha'] = self.colorAlpha
            map['colorAlpha'] = self.dualColorAlpha
            map['lightItemId'] = self.lightItemId
            map['dualLightItemId'] = self.dualLightItemId
            map['light'] = self.light
            map['dualLight'] = self.dualLight
            map['lightAlpha'] = self.lightAlpha
            map['dualLightAlpha'] = self.dualLightAlpha

    def reloadData(self, index = 0):
        if self.dyeMap:
            if not index:
                index = self.dyeMap.keys()[0]
            if self.dyeMap.has_key(index):
                map = self.dyeMap.pop(index)
                for key, value in map.iteritems():
                    setattr(self, key, value)

    def popData(self, index):
        if self.dyeMap.has_key(index):
            data = self.dyeMap.pop(index)
            page, pos, resKind = data.get('equipPage', 0), data.get('equipPos', 0), data.get('resKind', 0)
            self.setInvItem(page, pos, resKind)

    def resetCurrentData(self, item = None, index = 0):
        if not item:
            self.popData(index)
            if self.equipItem:
                oldIndex = getattr(self.equipItem, 'equipSType', 0)
                if oldIndex == index:
                    oldPage, oldPos, oldResKind = self.equipPage, self.equipPos, self.resKind
                    self.resetData()
                    self.reloadData()
                    self.setInvItem(oldPage, oldPos, oldResKind)
            self.setIcon(index, None)
        elif self.equipItem:
            oldIndex = getattr(self.equipItem, 'equipSType', 0)
            if oldIndex != index:
                self.saveData(oldIndex)
            else:
                oldPage, oldPos, oldResKind = self.equipPage, self.equipPos, self.resKind
                self.setInvItem(oldPage, oldPos, oldResKind)
            equipParts = list(item.wherePreview())
            equipParts.extend(uiUtils.getAspectParts(item.id))
            for key in self.dyeMap.keys():
                subItem = self.dyeMap[key].get('equipItem', None)
                if subItem:
                    subItemEquipParts = list(subItem.wherePreview())
                    subItemEquipParts.extend(uiUtils.getAspectParts(subItem.id))
                    for part in subItemEquipParts:
                        if part in equipParts:
                            self.popData(key)
                            self.setIcon(key, None)
                            break

            self.resetData()

    def resetData(self):
        self.equipPage = None
        self.equipPos = None
        self.equipItem = None
        self.color = None
        self.dualColor = None
        self.texture = 0
        self.textureSize = 5
        self.textureDensity = 0.3
        self.textureDegree = 1.5
        self.dyeNum = 0
        self.dualDyeNum = 0
        self.colorItemId = 0
        self.textureItemId = 0
        self.dualColorItemId = 0
        self.dyeMethod = const.DYE_COPY
        self.dualDyeMethod = const.DYE_COPY
        self.channel = const.DYE_CHANNEL_1
        self.oldDyeList = []
        self.npcEntId = 0
        self.resKind = 0
        self.chooseColor0 = None
        self.chooseColor1 = None
        self.colorAlpha = 0
        self.dualColorAlpha = 0
        self.lightItemId = 0
        self.dualLightItemId = 0
        self.light = ''
        self.dualLight = ''
        self.lightAlpha = 0
        self.dualLightAlpha = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYE_PLANE:
            self.med = mediator
            self.isShow = True

    def show(self, npcEntId = 0):
        self.npcEntId = npcEntId
        p = BigWorld.player()
        if not self.model:
            clientcom.fetchAvatarModel(p, gameglobal.getLoadThread(), self.afterModelFinished)
        else:
            self.afterModelFinished(self.model)

    def afterModelFinished(self, model):
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.realClose()
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
        rongGuang = charRes.RongGuangRes()
        mpr, aspect, isShowFashion = self.getEquipMpr()
        rongGuang.queryByAttribute(aspect, isShowFashion)
        rongGuang.apply(self.model)
        gameglobal.rds.loginScene.setPlayer(p, self.model)
        c = BigWorld.camera()
        if hasattr(c, 'boundRemain'):
            c.boundRemain = 1.0
        self.attachHairNode()
        self.fashionEffects = clientcom.attachFashionEffect(p, self.model)
        p.hideAllNearby()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self.isHideAllUI = True
        self.uiAdapter.hideAllUI()
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_DYE_PLANE, True)
        if not self.isShow:
            if gameglobal.rds.configData.get('enableWardrobe', False):
                self.uiAdapter.wardrobe.setDyeState()
                self.uiAdapter.wardrobe.show()
            else:
                self.uiAdapter.inventory.show()
                self.uiAdapter.inventory.setDyePlaneState()
                self.uiAdapter.fashionBag.askForShow()
                self.uiAdapter.fashionBag.setDyePlaneState()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYE_PLANE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if gameglobal.rds.ui.dyeColor.mediator:
            gameglobal.rds.ui.dyeColor.hide()
        self.onClickUnlockClose()
        self.isShow = False
        self.med = None
        if self.uiAdapter.wardrobe.widget:
            BigWorld.player().closeWardrobe()
        if self.uiAdapter.wardrobeDye.widget:
            self.uiAdapter.wardrobeDye.hide()
        if self.uiAdapter.inventory.mediator:
            self.uiAdapter.inventory.clearDyePlaneState()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.uiAdapter.fashionBag.clearDyePlaneState()
        p = BigWorld.player()
        p.restoreAllNearby()
        if self.model and self.model.inWorld:
            self.model.texturePriority = 0
            p.delModel(self.model)
            TA.ta_reset([self.model])
            self.model = None
            self.hairModel = None
        if self.modelUpdater:
            self.modelUpdater.release()
            self.modelUpdater = None
        if self.isHideAllUI:
            self.uiAdapter.restoreUI()
            self.isHideAllUI = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYE_PLANE)
        p.unlockKey(gameglobal.KEY_POS_UI)
        gameglobal.rds.loginScene.setPlayer(None, None)

    def getKey(self, index):
        return 'dyePlane.slot%d' % index

    def onHandleSliderChange(self, *arg):
        if not self.hasEquiped():
            return
        sliderName = arg[3][0].GetString()
        value = float(arg[3][1].GetNumber())
        if sliderName == 'texture_density':
            value = self.textureDensityValue(value)
            self.textureDensity = value
        elif sliderName == 'texture_size':
            if value >= 1 and value <= 20:
                value = self.textureSizeValue(value)
            self.textureSize = value
        elif sliderName == 'texture_degree':
            value = self.textureDegreeValue(value)
            self.textureDegree = value
        self.dyeModel()

    def textureDensityValue(self, value):
        return value * 0.01 * 0.4 + 0.2

    def revTextureDensityValue(self, value):
        return 2.5 * (value - 0.2) * 100

    def textureSizeValue(self, value):
        return 21 - value

    def revTextureSizeValue(self, value):
        return 21 - value

    def textureDegreeValue(self, value):
        return value * 0.01 * 0.6 + 1.2

    def revTextureDegreeValue(self, value):
        return (5 * value - 6) / 3.0 * 100

    def getOldDyeItemId(self, item, channel = const.DYE_CHANNEL_1):
        dyeMaterials = getattr(item, 'dyeMaterials', [])
        for oldChannel, itemId, _ in dyeMaterials:
            if channel == oldChannel:
                return itemId

    def close(self):
        if self.colorItemId == 0 and self.dualColorItemId == 0 and (self.textureItemId == 0 or self.textureSize == 0 or self.textureDensity == 0) or not self.equipItem:
            self.hide()
            return
        else:
            consumeItems = {}
            values = [self.__dict__] + self.dyeMap.values()
            for value in values:
                for i, (channel, itemStr) in enumerate(zip((const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_TEXTURE), ('colorItemId', 'dualColorItemId', 'textureItemId'))):
                    itemId = value.get(itemStr, 0)
                    if itemId:
                        dyeNum = value.get('dualDyeNum', 0) if i == 1 else value.get('dyeNum', 0)
                        oldDyeItemId = self.getOldDyeItemId(value.get('equipItem', None), channel)
                        if oldDyeItemId != itemId:
                            itemId = uiUtils.getParentId(itemId)
                            if itemId not in consumeItems:
                                consumeItems[itemId] = dyeNum
                            else:
                                consumeItems[itemId] += dyeNum

            msg = []
            lackMsg = []
            p = BigWorld.player()
            for key, value in consumeItems.iteritems():
                itemName = ID.data.get(key, {}).get('name', '')
                count = p.inv.countItemInPages(key, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                if count < value:
                    lackMsg.append('%sx%d' % (itemName, value - count))
                msg.append('%sx%d' % (itemName, value))

            if msg:
                if gameglobal.rds.configData.get('enableWardrobeMultiDyeScheme', False):
                    if self.isChooseEmptyScheme():
                        msg = gameStrings.DYELIST_SAVE_SCHEME % ','.join(msg)
                    else:
                        msg = gameStrings.DYELIST_COVER_SCHEME % ','.join(msg)
                else:
                    msg = gameStrings.TEXT_DYEPLANEPROXY_437 % ','.join(msg)
                if lackMsg:
                    lackMsg = gameStrings.TEXT_DYEPLANEPROXY_439 % ','.join(lackMsg)
                    msg += lackMsg
            else:
                msg = gameStrings.TEXT_DYEPLANEPROXY_442
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.checkItemCount, consumeItems), gameStrings.TEXT_DYEPLANEPROXY_444, self.hide, gameStrings.TEXT_IMPPLAYERTEAM_595)
            return

    def isChooseEmptyScheme(self):
        if self.equipItem:
            if self.equipItem.dyeMaterials:
                return False
        return True

    def checkItemCount(self, consumeItems):
        if gameglobal.rds.configData.get('enableWardrobeMultiDyeScheme', False):
            if self.equipItem.dyeCurrIdx == 1:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.DYELIST_CANT_DYE_INT)
                return
        p = BigWorld.player()
        for key, value in consumeItems.iteritems():
            count = p.inv.countItemInPages(key, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            if count < value:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_DYE, ())
                return

        self.saveAndClose()

    def saveAndClose(self):
        p = BigWorld.player()
        l = 0
        if self.colorItemId:
            l += 1
        if self.textureItemId:
            l += 1
        if self.dualColorItemId:
            l += 1
        consumeItemIds = []
        dyeMaterials = []
        for channel, itemId in zip((const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_TEXTURE), (self.colorItemId, self.dualColorItemId, self.textureItemId)):
            if itemId:
                if itemId == self.getOldDyeItemId(self.equipItem, channel):
                    consumeItemIds.append(itemId)
                    dyeMaterials.append((channel, itemId, self.dyeMethod))
                else:
                    dstPage, dstPos = p.inv.findItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
                    if not (dstPage == const.CONT_NO_PAGE and dstPos == const.CONT_NO_POS):
                        consumeItemIds.append(itemId)
                        dyeMaterials.append((channel, itemId, self.dyeMethod))

        sendSuccess = False
        if dyeMaterials and consumeItemIds and len(consumeItemIds) == l and len(dyeMaterials) == l:
            if self.npcEntId:
                npc = BigWorld.entity(self.npcEntId)
                if npc and npc.inWorld:
                    if self.resKind == const.RES_KIND_WARDROBE_BAG:
                        npc.cell.dyeEquip(self.equipPage, self.equipItem.uuid, consumeItemIds, self.equipItem.dyeList, self.resKind, dyeMaterials, False)
                    else:
                        npc.cell.dyeEquip(self.equipPage, str(self.equipPos), consumeItemIds, self.equipItem.dyeList, self.resKind, dyeMaterials, False)
                    sendSuccess = True
            else:
                if self.resKind == const.RES_KIND_WARDROBE_BAG:
                    p.cell.dyeEquip(self.equipPage, self.equipItem.uuid, consumeItemIds, self.equipItem.dyeList, self.resKind, dyeMaterials, False)
                else:
                    p.cell.dyeEquip(self.equipPage, str(self.equipPos), consumeItemIds, self.equipItem.dyeList, self.resKind, dyeMaterials, False)
                sendSuccess = True
        if not sendSuccess:
            self.hide()

    def dyeEquipCallback(self, success = True):
        if success and self.dyeMap:
            self.reloadData()
            self.saveAndClose()
        else:
            self.hide()

    def onHandleOkClick(self, *arg):
        self.close()

    def isInDyePlane(self, page, pos, resKind):
        if (page, pos, resKind) == (self.equipPage, self.equipPos, self.resKind):
            return True
        for value in self.dyeMap.itervalues():
            if (page, pos, resKind) == (value.get('equipPage', 0), value.get('equipPos', 0), value.get('resKind', 0)):
                return True

        return False

    def isWardrobeItemInDyePlane(self, uuid):
        if self.equipItem and uuid == self.equipItem.uuid:
            return True
        else:
            for value in self.dyeMap.itervalues():
                equipItem = value.get('equipItem', None)
                if equipItem and uuid == equipItem.uuid:
                    return True

            return False

    def setInvItem(self, page, pos, resKind):
        if resKind == const.RES_KIND_INV:
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)
        elif resKind == const.RES_KIND_FASHION_BAG:
            BigWorld.callback(0, Functor(gameglobal.rds.ui.fashionBag.updateSlotState, page, pos))

    def setIcon(self, index, item = None):
        key = self.getKey(index)
        if not item:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.setIconSelect(index, False)
        else:
            data = {}
            data['iconPath'] = uiUtils.getItemIconFile64(item.id)
            data['color'] = uiUtils.getItemColor(item.id)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            self.setIconSelect(index, True)
        self.setSuitVisible()

    def setIconSelect(self, index, isSelected):
        if self.med:
            self.med.Invoke('setIconSelect', (GfxValue(index), GfxValue(isSelected)))

    def setSuitVisible(self):
        if not self.med:
            return
        else:
            suitDic = {Item.EQUIP_FASHION_SUBTYPE_HEAD: 0,
             Item.EQUIP_FASHION_SUBTYPE_BODY: 0,
             Item.EQUIP_FASHION_SUBTYPE_HAND: 0,
             Item.EQUIP_FASHION_SUBTYPE_LEG: 0,
             Item.EQUIP_FASHION_SUBTYPE_SHOE: 0,
             Item.EQUIP_FASHION_SUBTYPE_CAPE: 0}
            partIndexMap = {'head': Item.EQUIP_FASHION_SUBTYPE_HEAD,
             'body': Item.EQUIP_FASHION_SUBTYPE_BODY,
             'hand': Item.EQUIP_FASHION_SUBTYPE_HAND,
             'leg': Item.EQUIP_FASHION_SUBTYPE_LEG,
             'shoe': Item.EQUIP_FASHION_SUBTYPE_SHOE,
             'cape': Item.EQUIP_FASHION_SUBTYPE_CAPE}
            values = [self.__dict__] + self.dyeMap.values()
            for value in values:
                item = value.get('equipItem', None)
                if not item:
                    continue
                ed = ED.data.get(item.id, {})
                slotParts = ed.get('slotParts', [])
                if slotParts:
                    suitDic[getattr(item, 'equipSType', 0)] = 1
                    for part in slotParts:
                        partIndex = partIndexMap.get(part, 0)
                        if partIndex in suitDic:
                            suitDic[partIndex] = 1

            self.med.Invoke('setSuitVisible', uiUtils.dict2GfxDict(suitDic))
            return

    def setEquip(self, page, pos, item, resKind, index = 0):
        p = BigWorld.player()
        if item and not item.isCanDye():
            p.showGameMsg(GMDD.data.EQUIP_CANNOT_DYE, ())
            return
        else:
            if item:
                index = getattr(item, 'equipSType', 0)
            if index not in DYE_ITEM_TYPE:
                return
            if item and not self._canShowEquip(item, True):
                return
            if item and gameglobal.rds.configData.get('enableWardrobe', False):
                if not item.isStorageByWardrobe():
                    p.showGameMsg(GMDD.data.WARDROBE_CANT_DYE_INV_ITEM, ())
                    return
            self.resetCurrentData(item, index)
            self.isSetEquip = True
            if item:
                self.equipPage = page
                self.equipPos = pos
                self.resKind = resKind
                self.setInvItem(page, pos, resKind)
                self.equipItem = copy.deepcopy(item)
                if hasattr(item, 'dyeList'):
                    self.oldDyeList = item.dyeList
                else:
                    self.oldDyeList = []
                self.dyeNum = ED.data.get(item.id).get('dyeNum', 1)
                self.dualDyeNum = ED.data.get(item.id).get('dualDyeNum', self.dyeNum)
                self.setIcon(index, item)
            mpr, aspect, showFashion = self.getEquipMpr()
            self.bodyPartUpdate(mpr, aspect, showFashion)
            self.updateLock()
            self.clearSelect()
            self.isSetEquip = False
            if self.equipItem:
                if item == None:
                    self.setEquipColor()
                    if self.colorItemId or self.dualColorItemId or self.textureItemId:
                        oldDyeList = getattr(self.equipItem, 'dyeList', [])
                        dyeMaterials = []
                        if self.colorItemId:
                            dyeMaterials.append((const.DYE_CHANNEL_1, self.colorItemId))
                        if self.dualColorItemId:
                            dyeMaterials.append((const.DYE_CHANNEL_2, self.dualColorItemId))
                        if self.textureItemId:
                            dyeMaterials.append((const.DYE_CHANNEL_TEXTURE, self.textureItemId))
                        retData = self.getDyePos(dyeMaterials, oldDyeList)
                        self.initDyeItem(retData)
                else:
                    dyeMaterials = getattr(self.equipItem, 'dyeMaterials', [])
                    if dyeMaterials:
                        retData = self.getDyePos(dyeMaterials, self.oldDyeList)
                        self.initDyeItem(retData)
            if self.equipItem:
                gameglobal.rds.ui.wardrobeDye.show(self.equipItem)
            else:
                gameglobal.rds.ui.wardrobeDye.hide()
            gameglobal.rds.ui.randomDye.hide()
            return

    def updateLock(self):
        if self.med:
            if self.equipItem:
                item = self.equipItem
                info = (GfxValue(item.isCanDye()),
                 GfxValue(item.isPermitDualDye()),
                 GfxValue(item.id),
                 GfxValue(self.isPbrEquip()),
                 GfxValue(item.isCanTexture()))
                self.med.Invoke('updateLock', info)
            else:
                info = (GfxValue(1),
                 GfxValue(0),
                 GfxValue(0),
                 GfxValue(True),
                 GfxValue(False))
                self.med.Invoke('updateLock', info)

    def clearSelect(self):
        if self.med:
            try:
                self.dyeDisable = True
                self.med.Invoke('clearSelect')
            finally:
                self.dyeDisable = False

    def onHandleClickSlot(self, *arg):
        index = int(arg[3][0].GetNumber())
        if self.hasEquiped():
            self.setEquip(None, None, None, None, index)

    def hasEquiped(self):
        return self.equipItem != None

    def onHandleClickColor(self, *arg):
        if not self.hasEquiped() or self.isSetEquip:
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        prefix = btnName[0:i]
        channel = int(arg[3][1].GetNumber())
        self.channel = channel
        if index < len(getattr(self, prefix, [])):
            itemId = getattr(self, prefix, [])[index]
            color_ = self.getData(itemId, 'color', [])
            if color_ == []:
                color_ = utils.genRandomDyeList()
            if prefix == 'color_rare':
                color_ = color_[0]
            if color_:
                if channel == const.DYE_CHANNEL_1:
                    self.colorItemId = itemId
                    self.color = color_
                    self.colorAlpha = 0
                    self.light = ''
                    self.lightAlpha = 0
                elif channel == const.DYE_CHANNEL_2:
                    self.dualColorItemId = itemId
                    self.dualColor = color_
                    self.dualColorAlpha = 0
                    self.dualLight = ''
                    self.dualLightAlpha = 0
            self.dyeModel()
            ret = {}
            if itemId != self.getOldDyeItemId(self.equipItem, channel):
                ret = self._getItemData(itemId, channel)
            mad = MAD.data.get(itemId, {})
            ret['channel'] = channel
            ret['highLightAlphaNum'] = mad.get('highLightAlphaNum', 0)
            ret['colorAlphaNum'] = len(mad.get('alpha', []))
            if prefix == 'color_rare':
                color = self.getData(itemId, 'color', [])
                ret['rareSubNum'] = len(color)
                ret['rareSubColor'] = []
                for item in color:
                    ret['rareSubColor'].append(self.colorStr2Int(item[0]))

            else:
                ret['rareSubNum'] = 0
                ret['rareSubColor'] = []
            return uiUtils.dict2GfxDict(ret)

    def onHandleColorRareClick(self, *arg):
        if not self.hasEquiped():
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        if self.channel == const.DYE_CHANNEL_1:
            if self.colorItemId:
                color_ = self.getData(self.colorItemId, 'color', [])
                if color_ and index < len(color_) and isinstance(color_[index], tuple):
                    self.color = color_[index]
        elif self.channel == const.DYE_CHANNEL_2:
            if self.dualColorItemId:
                color_ = self.getData(self.dualColorItemId, 'color', [])
                if color_ and index < len(color_) and isinstance(color_[index], tuple):
                    self.dualColor = color_[index]
        self.dyeModel()

    def onHandleAlphaSubClick(self, *arg):
        if not self.hasEquiped():
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        if self.channel == const.DYE_CHANNEL_1:
            if self.colorItemId:
                alpha = self.getData(self.colorItemId, 'alpha', [])
                if alpha and index < len(alpha):
                    self.colorAlpha = alpha[index]
        elif self.channel == const.DYE_CHANNEL_2:
            if self.dualColorItemId:
                alpha = self.getData(self.dualColorItemId, 'alpha', [])
                if alpha and index < len(alpha):
                    self.dualColorAlpha = alpha[index]
        self.dyeModel()

    def onHandleLightClick(self, *arg):
        if not self.hasEquiped():
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        prefix = btnName[0:i]
        channel = int(arg[3][1].GetNumber())
        self.channel = channel
        if index < len(getattr(self, prefix, [])):
            itemId = getattr(self, prefix, [])[index]
            light = self.getData(itemId, 'color', '')
            if channel == const.DYE_CHANNEL_1:
                self.lightItemId = itemId
                self.light = light
                self.lightAlpha = 0
            elif channel == const.DYE_CHANNEL_2:
                self.dualLightItemId = itemId
                self.dualLight = light
                self.dualLightAlpha = 0
            self.dyeModel()
            ret = self._getItemData(itemId, channel)
            ret['channel'] = channel
            return uiUtils.dict2GfxDict(ret)

    def onHandleLightSubClick(self, *arg):
        if not self.hasEquiped():
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        if self.channel == const.DYE_CHANNEL_1:
            if self.lightItemId:
                alpha = self.getRealAlpha(self.lightItemId, self.colorItemId)
                if alpha and index < len(alpha):
                    self.lightAlpha = alpha[index]
        elif self.channel == const.DYE_CHANNEL_2:
            if self.dualLightItemId:
                alpha = self.getRealAlpha(self.dualLightItemId, self.dualColorItemId)
                if alpha and index < len(alpha):
                    self.dualLightAlpha = alpha[index]
        self.dyeModel()

    def getRealAlpha(self, lightItemId, colorItemId):
        ret = self.getData(lightItemId, 'highLightAlpha', [])
        if self.getData(lightItemId, 'color', ''):
            return ret
        alpha = self.getData(colorItemId, 'highLightAlpha', [])
        if alpha:
            return alpha
        return ret

    def onHandleClickTexture(self, *arg):
        if not self.hasEquiped():
            return
        btnName = arg[3][0].GetString()
        i = btnName.rfind('_')
        index = int(btnName[i + 1:])
        if index < len(self.textureItems):
            self.textureItemId = self.textureItems[index]
            self.texture = MAD.data.get(self.textureItemId, {}).get('texture', 0)
        else:
            self.textureItemId = 0
            self.texture = 0
        self.dyeModel()
        ret = {}
        if self.textureItemId != self.getOldDyeItemId(self.equipItem, const.DYE_CHANNEL_TEXTURE):
            ret = self._getItemData(self.textureItemId, const.DYE_CHANNEL_TEXTURE)
        return uiUtils.dict2GfxDict(ret)

    def _getItemData(self, itemId, channel):
        p = BigWorld.player()
        if not itemId:
            return {}
        ret = {}
        ret['itemId'] = itemId
        dyeNum = self.dyeNum if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_TEXTURE) else self.dualDyeNum
        ret['iconPath'] = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, ID.data.get(itemId, {}).get('icon', 0))
        num = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        if num > dyeNum:
            num = dyeNum
        ret['num'] = '%d/%d' % (num, dyeNum)
        ret['color'] = uiUtils.getItemColor(itemId)
        return ret

    def canShowEquip(self):
        if not self.hasEquiped():
            return False
        return self._canShowEquip(self.equipItem, False)

    def _canShowEquip(self, item, showMsg = False):
        if not item:
            return False
        p = BigWorld.player()
        sex = p.realPhysique.sex
        sch = p.realPhysique.school
        bodyType = p.realPhysique.bodyType
        if not (item.type == Item.BASETYPE_EQUIP and item.equipType in (Item.EQUIP_BASETYPE_FASHION, Item.EQUIP_BASETYPE_ARMOR)):
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
        return True

    def getEquipMpr(self):
        p = BigWorld.player()
        if not self.canShowEquip():
            mpr = charRes.MultiPartRes()
            mpr.queryByAvatar(p)
            mpr.isAvatar = False
            return (mpr, p.realAspect, p.isShowFashion())
        else:
            self.setEquipColor()
            aspect = copy.deepcopy(p.realAspect)
            isShowFashion = self.createAspect(aspect, self.equipItem)
            for value in self.dyeMap.itervalues():
                item = value.get('equipItem', None)
                self.createAspect(aspect, item)

            mpr = charRes.MultiPartRes()
            mpr.queryByAttribute(p.realPhysique, aspect, isShowFashion, p.avatarConfig)
            return (mpr, aspect, isShowFashion)

    def getWearParts(self, itemId):
        ed = ED.data.get(itemId, {})
        slotParts = ed.get('slotParts', [])
        parts = ed.get('parts', [])
        autoParts = [ p for p in slotParts if p not in parts ]
        parts = []
        for p in autoParts:
            p = Equipment.FASHION_PARTS_MAP.get(p, None)
            if p is not None:
                parts.append(p)

        return parts

    def createAspect(self, aspect, item):
        if not item:
            return False
        isShowFashion = False
        if item.equipType == Item.EQUIP_BASETYPE_FASHION:
            isShowFashion = True
        parts = list(item.whereEquip())
        parts.extend(self.getWearParts(item.id))
        if isShowFashion:
            if getattr(item, 'equipSType', 0) in (Item.EQUIP_FASHION_SUBTYPE_NEIYI, Item.EQUIP_FASHION_SUBTYPE_NEIKU):
                for part in charRes.PARTS_ASPECT_FASHION_SUB:
                    setattr(aspect, part, 0)

            for part in charRes.PARTS_ASPECT_FASHION:
                equipId = getattr(aspect, part)
                if equipId:
                    equItem = Item(equipId)
                    equipParts = list(equItem.whereEquip())
                    equipParts.extend(uiUtils.getAspectParts(equItem.id))
                    for itemPart in parts:
                        if itemPart in equipParts:
                            setattr(aspect, part, 0)
                            break

        for part in parts:
            aspect.set(part, item.id, getattr(item, 'dyeList', []), getattr(item, 'enhLv', 0), getattr(item, 'rongGuang', []))

        return isShowFashion

    def getEquipRes(self):
        mpr, aspect, showFashion = self.getEquipMpr()
        res = None
        if mpr:
            res = mpr.getPrerequisites()
        return (res, aspect, showFashion)

    def dyeModel(self):
        if self.dyeDisable:
            return
        elif self.isUpdating:
            return
        else:
            model = None
            if self.canShowEquip():
                model = self.model
            else:
                self.showErrorMsg()
                return
            mpr, _, _ = self.getEquipMpr()
            self._dyeModel(mpr, model)
            return

    @ui.callFilter(0.5, False)
    def showErrorMsg(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_PREVIEW, ())

    def _dyeModel(self, mpr, model):
        player = BigWorld.player()
        if mpr and model:
            m = AM.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, cape=mpr.cape)
            m.readConfig(player.realAvatarConfig)
            m.applyDyeMorph(True)
            m.applyFaceMorph()
            if self.hairModel and mpr.dyesDict.get('head', []):
                dyeList = mpr.dyesDict.get('head', [])
                hairDyeMorpher = dyeMorpher.HairDyeMorpher(self.hairModel)
                hairDyeMorpher.read(dyeList)
                hairDyeMorpher.apply()

    def _getColor(self, colorStr):
        index = colorStr.rfind(',')
        return colorStr[0:index]

    def _getAlpha(self, colorStr):
        index = colorStr.rfind(',')
        return colorStr[index + 1:]

    def getDyePos(self, dyeMaterials, oldDyeList):
        retData = {}
        for item in dyeMaterials:
            ret = {}
            channel = item[0]
            dyeItemId = item[1]
            dyeList = oldDyeList[0:2]
            highLightIndex = const.DYES_INDEX_PBR_HIGH_LIGHT
            if channel == const.DYE_CHANNEL_2:
                dyeList = oldDyeList[5:7]
                highLightIndex = const.DYES_INDEX_PBR_DUAL_HIGH_LIGHT
            if not dyeList:
                continue
            color_ = self.getData(dyeItemId, 'color', [])
            if dyeItemId in self.color_rare:
                ret['color_rare'] = self.color_rare.index(dyeItemId)
                for i, color in enumerate(color_):
                    if self._getColor(color[0]) == self._getColor(dyeList[0]):
                        ret['color_rare_sub'] = i
                        break

            elif dyeItemId in self.color_high:
                ret['color_high'] = self.color_high.index(dyeItemId)
            elif dyeItemId in self.color_normal:
                ret['color_normal'] = self.color_normal.index(dyeItemId)
            elif dyeItemId in self.textureItems:
                ret['texture'] = self.textureItems.index(dyeItemId)
            if dyeItemId != self.getOldDyeItemId(self.equipItem, channel):
                ret['itemInfo'] = self._getItemData(dyeItemId, channel)
            if ret:
                if channel == const.DYE_CHANNEL_TEXTURE:
                    if len(oldDyeList) > const.DYES_INDEX_TEXTURE:
                        value = float(oldDyeList[const.DYES_INDEX_TEXTURE])
                        if value:
                            ret['texture_size'] = self.revTextureSizeValue(value)
                    if len(oldDyeList) > const.DYES_INDEX_TEXTURE + 1:
                        value = float(oldDyeList[const.DYES_INDEX_TEXTURE + 1])
                        if value:
                            ret['texture_density'] = self.revTextureDensityValue(value)
                    if len(oldDyeList) > const.DYES_INDEX_PBR_TEXTURE_DEGREE:
                        value = float(oldDyeList[const.DYES_INDEX_PBR_TEXTURE_DEGREE])
                        if value:
                            ret['texture_degree'] = self.revTextureDegreeValue(value)
                else:
                    alpha_ = self.getData(dyeItemId, 'alpha', [])
                    if int(self._getAlpha(dyeList[0])) in alpha_:
                        ret['color_alpha_sub'] = alpha_.index(int(self._getAlpha(dyeList[0])))
                    else:
                        ret['color_alpha_sub'] = 0
                    ret['high_light'] = 0
                    ret['high_light_sub'] = 0
                    for i, itemId in enumerate(self.high_light):
                        color_ = self.getData(itemId, 'color', '')
                        highLightAlpha = self.getRealAlpha(itemId, dyeItemId)
                        if not color_:
                            if len(oldDyeList) > highLightIndex:
                                hl = float(oldDyeList[highLightIndex])
                            else:
                                hl = int(self._getAlpha(dyeList[1]))
                            if hl in highLightAlpha:
                                ret['high_light_sub'] = highLightAlpha.index(hl)
                            else:
                                ret['high_light_sub'] = 0
                        if color_ and self._getColor(dyeList[1]) == self._getColor(color_):
                            ret['high_light'] = i
                            if len(oldDyeList) > highLightIndex:
                                hl = float(oldDyeList[highLightIndex])
                            else:
                                hl = int(self._getAlpha(dyeList[1]))
                            if hl in highLightAlpha:
                                ret['high_light_sub'] = highLightAlpha.index(hl)
                            else:
                                ret['high_light_sub'] = 0
                            break

            retData[channel] = ret

        return retData

    def initDyeItem(self, data):
        if self.med:
            try:
                self.dyeDisable = True
                self.med.Invoke('initDyeItem', uiUtils.dict2GfxDict(data))
            finally:
                self.dyeDisable = False

    def setEquipColor(self):
        if self.equipItem:
            self.equipItem.dyeList = self.oldDyeList
            if self.color:
                newColor = list(self.color)
                if self.colorAlpha:
                    newColor[0] = self.setAlpha(newColor[0], self.colorAlpha)
                if self.light:
                    newColor[1] = self.light
                if self.lightAlpha:
                    if self.isPbrEquip():
                        self.equipItem.setPbrHL(str(self.lightAlpha), const.DYE_CHANNEL_1)
                    else:
                        newColor[1] = self.setAlpha(newColor[1], self.lightAlpha)
                self.equipItem.setDye(newColor, self.dyeMethod)
            if self.dualColor:
                newColor = list(self.dualColor)
                if self.dualColorAlpha:
                    newColor[0] = self.setAlpha(newColor[0], self.dualColorAlpha)
                if self.dualLight:
                    newColor[1] = self.dualLight
                if self.dualLightAlpha:
                    if self.isPbrEquip():
                        self.equipItem.setPbrHL(str(self.dualLightAlpha), const.DYE_CHANNEL_2)
                    else:
                        newColor[1] = self.setAlpha(newColor[1], self.dualLightAlpha)
                self.equipItem.setDualDye(newColor, self.dualDyeMethod)
            texture = [str(self.textureSize), str(self.textureDensity), str(self.texture)]
            if self.texture:
                self.equipItem.setTexture(texture)
                if self.textureDegree:
                    self.equipItem.setPbrTextureG(str(self.textureDegree))

    def setAlpha(self, singleColor, alpha):
        singleColor = singleColor.split(',')
        singleColor[-1] = str(alpha)
        return ','.join(singleColor)

    def setDyeMethod(self, dyeMethod):
        if self.channel == const.DYE_CHANNEL_1:
            self.dyeMethod = dyeMethod
        else:
            self.dualDyeMethod = dyeMethod
        self.dyeModel()

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        key = int(key[-1])
        item = None
        if self.dyeMap.has_key(key):
            item = self.dyeMap[key].get('equipItem', None)
        elif self.equipItem:
            oldIndex = getattr(self.equipItem, 'equipSType', 0)
            if key == oldIndex:
                item = self.equipItem
        return self.uiAdapter.inventory.GfxToolTip(item)

    def onGetInitData(self, *arg):
        ret = {'color_normal': self.color_normal,
         'color_high': self.color_high,
         'color_rare': self.color_rare,
         'textureItem': self.textureItems,
         'color_random': self.color_random,
         'high_light': self.high_light}
        colorMap = {}
        for itemId in self.color_rare:
            data = MAD.data.get(itemId, {})
            if data.has_key('color'):
                color = data['color'][0][0]
                colorMap[itemId] = self.colorStr2Int(color)

        for itemId in self.high_light:
            data = MAD.data.get(itemId, {})
            if data.has_key('color'):
                color = data['color']
                colorMap[itemId] = self.colorStr2Int(color)

        for itemId in self.color_normal + self.color_high:
            data = MAD.data.get(itemId, {})
            if data.has_key('color'):
                color = data['color'][0]
                colorMap[itemId] = self.colorStr2Int(color)

        ret['colorMap'] = colorMap
        return uiUtils.dict2GfxDict(ret)

    def colorStr2Int(self, colorStr):
        if colorStr == '':
            return 0
        color = eval(colorStr)
        color = [ (value if value <= 255 else 255) for value in color ]
        return (color[0] << 16) + (color[1] << 8) + color[2]

    def unlockDualDye(self, *arg):
        if self.equipItem and self.equipItem.isCanDye() == gametypes.DYE_SINGLE and self.equipItem.isPermitDualDye():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_UNLOCK_DUAL_DYE, True)

    def onGetUnlockData(self, *arg):
        unlockInfo = SCD.data.get('unlockDualDye', (2000, (240000, 2)))
        if not unlockInfo:
            self.onClickUnlockClose()
            return
        cash = unlockInfo[0]
        unlockItem = unlockInfo[1][0]
        unLockItemNum = unlockInfo[1][1]
        ret = {}
        p = BigWorld.player()
        num = p.inv.countItemInPages(uiUtils.getParentId(unlockItem), enableParentCheck=True)
        if num > unLockItemNum:
            num = unLockItemNum
        ret['itemId'] = unlockItem
        ret['icon'] = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, ID.data.get(unlockItem, {}).get('icon'))
        ret['count'] = '%d/%d' % (num, unLockItemNum)
        ret['color'] = uiUtils.getItemColor(unlockItem)
        ret['cash'] = cash
        ret['itemName'] = ID.data.get(unlockItem, {}).get('name', '')
        return uiUtils.dict2GfxDict(ret, True)

    def onClickUnlockClose(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_UNLOCK_DUAL_DYE)

    def onClickUnlockConfirmBtn(self, *arg):
        p = BigWorld.player()
        unlockInfo = SCD.data.get('unlockDualDye', (2000, (240000, 2)))
        if unlockInfo:
            callback = Functor(p.cell.unlockDualDye, self.equipPage, self.equipPos, self.resKind)
            if uiUtils.checkBindCashEnough(unlockInfo[0], p.bindCash, p.cash, callback):
                callback()
        self.onClickUnlockClose()

    def onSetChannel(self, *arg):
        self.channel = int(arg[3][0].GetNumber())
        dyeMethod = self.dyeMethod
        if self.channel == const.DYE_CHANNEL_2:
            dyeMethod = self.dualDyeMethod
        self.uiAdapter.dyeColor.setDyeMethod(dyeMethod)

    def onAdjustColor(self, *arg):
        key = arg[3][0].GetString()
        channel = int(arg[3][1].GetNumber())
        r = int(arg[3][2].GetNumber())
        g = int(arg[3][3].GetNumber())
        b = int(arg[3][4].GetNumber())
        alpha = int(arg[3][5].GetNumber())
        if alpha == 0:
            alpha = 255
        if key == 'colorplane0':
            self.chooseColor0 = ['%d,%d,%d,%d' % (r,
              g,
              b,
              alpha)]
        else:
            self.chooseColor1 = ['%d,%d,%d,%d' % (r,
              g,
              b,
              alpha)]
        self.channel = channel
        itemId = self.color_random[-1]
        if MAD.data.get(itemId, {}).get('dyeType') == Item.CONSUME_DYE_SUPER:
            if self.chooseColor0 and self.chooseColor1:
                color_ = self.chooseColor0 + self.chooseColor1
                if channel == const.DYE_CHANNEL_1:
                    self.colorItemId = itemId
                    self.color = color_
                elif channel == const.DYE_CHANNEL_2:
                    self.dualColorItemId = itemId
                    self.dualColor = color_
            self.dyeModel()
            ret = self._getItemData(itemId, channel)
            ret['channel'] = channel
            return uiUtils.dict2GfxDict(ret)

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
            self.isUpdating = True
            self.modelUpdater.beginUpdate(resOld, res, None, None, tints)
            return

    def afterBodyPartUpdate(self, mpr, aspect, showFashion):
        self.isUpdating = False
        self.attachHairNode()
        self._dyeModel(mpr, self.model)
        rongGuang = charRes.RongGuangRes()
        mpr, aspect, isShowFashion = self.getEquipMpr()
        rongGuang.queryByAttribute(aspect, isShowFashion)
        rongGuang.apply(self.model)
        p = BigWorld.player()
        self.stopAllEffect()
        self.fashionEffects = clientcom.attachFashionEffect(p, self.model, aspect)

    def stopAllEffect(self):
        if self.fashionEffects:
            for fx in self.fashionEffects:
                fx.stop()

    def attachHairNode(self):
        if self.model:
            hairNode = self.model.node('biped Head')
            if hairNode:
                hairNode.attachments = []
            self.hairModel = clientcom.getHairNode(BigWorld.player(), self.model, True)

    def isPbrEquip(self):
        if self.equipItem:
            return clientcom.isPbrEquip(self.equipItem.id)
        return False

    def getData(self, itemId, key, default = None, subId = None):
        mad = MAD.data.get(itemId, {})
        if self.isPbrEquip() and key in ('color', 'alpha', 'highLightAlpha'):
            key = key[0].upper() + key[1:]
            data = mad.get('pbr' + key, default)
            if subId and key in ('alpha',):
                if data and subId < len(data) and (isinstance(data[subId], tuple) or isinstance(data[subId], list)):
                    data = data[subId]
            return data
        return mad.get(key, default)

    def onHandleSelectSlot(self, *arg):
        index = int(arg[3][0].GetNumber())
        if index not in DYE_ITEM_TYPE:
            return
        if not self.dyeMap.has_key(index):
            return
        oldIndex = 0
        if self.equipItem:
            oldIndex = getattr(self.equipItem, 'equipSType', 0)
        if oldIndex == index:
            return
        if oldIndex:
            self.saveData(oldIndex)
        self.reloadData(index)
        self.clearSelect()
        self.updateLock()
        self.setEquipColor()
        self.setIconSelect(index, True)
        gameglobal.rds.ui.wardrobeDye.show(self.equipItem)
        if self.colorItemId or self.dualColorItemId or self.textureItemId:
            oldDyeList = getattr(self.equipItem, 'dyeList', [])
            dyeMaterials = []
            if self.colorItemId:
                dyeMaterials.append((const.DYE_CHANNEL_1, self.colorItemId))
            if self.dualColorItemId:
                dyeMaterials.append((const.DYE_CHANNEL_2, self.dualColorItemId))
            if self.textureItemId:
                dyeMaterials.append((const.DYE_CHANNEL_TEXTURE, self.textureItemId))
            retData = self.getDyePos(dyeMaterials, oldDyeList)
            self.initDyeItem(retData)
        gameglobal.rds.ui.randomDye.hide()

    def onRandomDyeClick(self, *args):
        if not self.equipItem:
            BigWorld.player().showGameMsg(GMDD.data.NEED_EQUIP_ONE_CLOTH, ())
            return
        if self.equipItem:
            if self.equipItem.dyeCurrIdx == 1:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.DYELIST_CANT_DYE_INT)
                return
            gameglobal.rds.ui.randomDye.show(self.equipItem, self.resKind, self.equipPage, self.equipPos)
