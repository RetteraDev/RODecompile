#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tuZhuangProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import item
import const
import gamelog
import utils
import cPickle
from guis import ui
from guis.uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from guis import tianyuMallProxy
from helpers import tintalt as TA
from helpers import tuZhuangDyeMorpher
from callbackHelper import Functor
from item import Item
from gameStrings import gameStrings
from cdata import tuzhuang_material_data as TMD
from cdata import tuzhuang_equip_data as TED
from data import mall_item_data as MID
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import equip_skin_data as ESD
from cdata import huanfu_skin_data as HSD
firstArea = 'firstArea'
firstMaterial = 'firstMaterial'
secondArea = 'secondArea'
secondMaterial = 'secondMaterial'
textureArea = 'textureArea'
thirdArea = 'thirdArea'
thirdMaterial = 'thirdMaterial'
globalLight = 'globalLight'
TUZHUANG_DYE_ITEM_MAP = {const.DYE_CHANNEL_1: (firstArea, firstMaterial),
 const.DYE_CHANNEL_2: (secondArea, secondMaterial),
 const.DYE_CHANNEL_TEXTURE: (textureArea,),
 const.DYE_CHANNEL_3: (thirdArea, thirdMaterial),
 const.DYE_CHANNEL_LIGHT: (globalLight,)}
CHANNEL_U2P_MAP = {0: const.DYE_CHANNEL_1,
 1: const.DYE_CHANNEL_2,
 2: const.DYE_CHANNEL_3,
 'tietu': const.DYE_CHANNEL_TEXTURE,
 'light': const.DYE_CHANNEL_LIGHT}
UI_CHANNEL_ARRAY = ['yanse', 'caizhi', 'gaoguang']
UI_NO_CHANNEL_AYYAY = ['tietu', 'light']
UI_CHANNEL_ARRAY = ['yanse', 'caizhi', 'gaoguang']
UI_ARRAY = UI_NO_CHANNEL_AYYAY + UI_CHANNEL_ARRAY
UI_PART_MAP = dict(zip(UI_CHANNEL_ARRAY, [0, 1, 2]))
PY_PART_MAP = {firstArea: 0,
 secondArea: 0,
 thirdArea: 0,
 firstMaterial: 1,
 secondMaterial: 1,
 thirdMaterial: 1,
 textureArea: 0,
 globalLight: 0}
BAR_TYPE_RADIO = 1
BAR_TYPE_COLOR = 2
BAR_TYPE_SLIDER = 3
BAR_PART_MAP = dict(zip(UI_ARRAY, (None,
 None,
 BAR_TYPE_COLOR,
 BAR_TYPE_RADIO,
 BAR_TYPE_SLIDER)))

def getChannelFromUI(area, btnIndex):
    if area in UI_NO_CHANNEL_AYYAY:
        return (CHANNEL_U2P_MAP[area], btnIndex)
    if area in UI_CHANNEL_ARRAY:
        return (CHANNEL_U2P_MAP[btnIndex], UI_PART_MAP[area])


def getInfoFromTMD(itemId, key = 'color', default = None):
    return TMD.data.get(itemId, {}).get(key, default)


class TuZhuangProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(TuZhuangProxy, self).__init__(uiAdapter)
        self.bindType = 'tuzhuang'
        self.type = 'tuzhuang'
        self.modelMap = {'tuZhuangItem': self.onTuZhuangItem,
         'getMyPointsInfo': self.onGetMyPointsInfo,
         'getMyMoneyInfo': self.onGetMyMoneyInfo,
         'getAllTabsInfo': self.onGetAllTabsInfo,
         'getMallItemList': self.onGetMallItemList,
         'searchItem': self.onSearchItem,
         'chooseNextItem': self.onChooseNextItem,
         'clickColorBtn': self.onClickColorBtn,
         'clickAreaBtn': self.onClickAreaBtn,
         'changeSlider': self.onChangeSlider,
         'cancelPreviewInfo': self.onCancelPreviewInfo,
         'setPreviewInfo': self.onSetPreviewInfo,
         'saveColor': self.onSaveColor,
         'clickCaizhi': self.onClickCaizhi,
         'confirmBuy': self.onConfirmBuy,
         'openConfirmWindow': self.onOpenConfirmWindow,
         'closeBuyConfirm': self.onCloseBuyConfirm,
         'gotoBack': self.onGotoBack,
         'cancelTuZhuang': self.onCancelTuZhuang,
         'isShowDyeTest': self.isShowDyeTest,
         'selectHuanXingTTL': self.onSelectHuanXingTTL,
         'clickCancelColor': self.clickCancelColor,
         'getInvItemInfo': self.onGetInvItemInfo,
         'clickSkinBtn': self.onClickSkinBtn,
         'applyOldSkin': self.onApplyOldSkin,
         'switchHuanfuHuanxing': self.switchHuanfuHuanxing}
        self.reset()
        self.med = None
        self.buyConfirmMediator = None
        self.isShow = False
        self.dyeTestVis = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_TUZHUANG, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_TUZHUANG_CONFIRM, self.onCloseBuyConfirm)
        self.tabMgr = tianyuMallProxy.TuZhuangTabManager()
        self.huanXingItems = self.initHuanXingItem()

    def initHuanXingItem(self):
        ret = {}
        for key, value in TMD.data.iteritems():
            if value.has_key('ttlType'):
                ret[value['ttlType']] = key

        return ret

    def canShowTuZhuang(self):
        return gameglobal.rds.configData.get('enableTuzhuang', False)

    def getPartDyeListItem(self, channel, part):
        return self.dyeListItem.get(channel, {}).get(part, [])

    def getSelectedDyeListItem(self, channel, part):
        index = self.getPartClickIndex(channel, part)
        values = self.getPartDyeListItem(channel, part)
        if index != None and index >= 0 and index < len(values):
            return values[index]
        else:
            return

    def getPartDyeList(self, channel, part, defaultValue = None):
        value = defaultValue
        try:
            value = self.dyeList.get(channel, [])[part]
        except:
            pass

        return value

    def setPartDyeList(self, channel, part, value):
        utils.setPartTuZhuangDyeList(self.dyeList, channel, part, value)

    def getPartClickIndex(self, channel, part = 0):
        return self.dyeClickIndex.get(channel, {}).get(part, None)

    def setPartClickIndex(self, channel, part = 0, value = 0):
        self.dyeClickIndex.setdefault(channel, {})
        if value == -1:
            if self.dyeClickIndex[channel].has_key(part):
                self.dyeClickIndex[channel].pop(part)
        else:
            self.dyeClickIndex[channel][part] = value

    def onClickAreaBtn(self, *arg):
        if not self.item:
            return
        else:
            data0 = arg[3][0].GetString()
            data1 = int(arg[3][1].GetNumber())
            channel, part = getChannelFromUI(data0, data1)
            barShowType = BAR_PART_MAP[data0]
            gamelog.debug('onClickAreaBtn', channel, part, data0, data1, barShowType)
            if barShowType == BAR_TYPE_COLOR:
                dyeItems = self.getPartDyeListItem(channel, part)
                colorArray = []
                for dyeId in dyeItems:
                    hasSuffix = getInfoFromTMD(dyeId, 'needConsume', 0)
                    colorArray.append((self.transColorStr(getInfoFromTMD(dyeId, 'color'))[0], hasSuffix))

                self.showBar(colorArray, barShowType)
            elif barShowType == BAR_TYPE_RADIO:
                dyeItems = self.getPartDyeListItem(channel, part)
                value = self.getPartDyeList(channel, part, 0)
                valueName = self.getCaizhiName(channel, part, value)
                caizhiArray = []
                for dyeId in dyeItems:
                    caizhiArray.append(getInfoFromTMD(dyeId, 'materialName', ''))

                if value and valueName in caizhiArray:
                    valueIndex = caizhiArray.index(valueName)
                else:
                    valueIndex = -1
                self.showBar([valueIndex, caizhiArray], barShowType)
            elif barShowType == BAR_TYPE_SLIDER:
                dyeItems = self.getPartDyeListItem(channel, 0)
                index = self.getPartClickIndex(channel, 0)
                if index == None:
                    self.hideBar()
                    return
                dyeId = dyeItems[index]
                value = self.getPartDyeList(channel, part)
                range = getInfoFromTMD(dyeId, 'alphaRange')
                if value == None:
                    value = range[0]
                gaoGuangArray = [value, range[0], range[1]]
                self.showBar(gaoGuangArray, barShowType)
            elif data0 == 'tietu':
                part -= 1
                self.handleValueChange(data0, data1, channel, 0, part)
            return

    def onClickColorBtn(self, *arg):
        data0 = arg[3][0].GetString()
        data1 = int(arg[3][1].GetNumber())
        index = int(arg[3][2].GetNumber())
        channel, part = getChannelFromUI(data0, data1)
        gamelog.debug('onClickColorBtn', channel, part, index)
        self.handleValueChange(data0, data1, channel, part, index)

    def onClickCaizhi(self, *arg):
        data0 = arg[3][0].GetString()
        data1 = int(arg[3][1].GetNumber())
        channel, part = getChannelFromUI(data0, data1)
        index = int(arg[3][2].GetNumber())
        gamelog.debug('onClickCaizhi', channel, part, index)
        self.handleValueChange(data0, data1, channel, part, index)

    def onConfirmBuy(self, *arg):
        p = BigWorld.player()
        if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG:
            dyeArray = []
            hasTint = False
            if self.dyeClickIndex.has_key(const.DYE_CHANNEL_TEXTURE) and self.dyeClickIndex[const.DYE_CHANNEL_TEXTURE].has_key(0):
                tintId = self.getSelectedDyeListItem(const.DYE_CHANNEL_TEXTURE, 0)
                if tintId:
                    hasTint = True
                    dyeArray.append((const.DYE_CHANNEL_TEXTURE, [tintId]))
            if not hasTint:
                lightId = self.getSelectedDyeListItem(const.DYE_CHANNEL_LIGHT, 0)
                if lightId:
                    dyeArray.append((const.DYE_CHANNEL_LIGHT, [lightId]))
                for channel in self.dyeClickIndex:
                    if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
                        subArray = []
                        colorId = self.getSelectedDyeListItem(channel, 0)
                        if colorId:
                            subArray.append(colorId)
                        else:
                            subArray.append(0)
                        caizhiId = self.getSelectedDyeListItem(channel, 1)
                        if caizhiId:
                            subArray.append(caizhiId)
                        else:
                            subArray.append(0)
                        gaoguangValue = self.getPartClickIndex(channel, 2)
                        if gaoguangValue:
                            subArray.append(gaoguangValue)
                        else:
                            subArray.append(0)
                        dyeArray.append((channel, subArray))

            ttlType = 1
            if self.ttlType:
                ttlType = self.ttlType
            huanxingItem = self.huanXingItems[ttlType]
            hxPage, hxPos = p.inv.findItemInPages(huanxingItem, enableParentCheck=True)
            if hxPage == const.CONT_NO_PAGE and hxPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.TUZHUANG_NO_HUANXING, ())
                return
            if not dyeArray:
                p.showGameMsg(GMDD.data.TUZHUANG_NO_CHOOSE_DYE, ())
                return
            if self.mallId == -1:
                info = self.getItemInfoByIdx(self.index)
                page = info.get('page', 0)
                pos = info.get('pos', 0)
                resKind = info.get('resKind')
                p.cell.tuzhuangInvItem(page, pos, resKind, hxPage, hxPos, const.RES_KIND_INV, cPickle.dumps(dyeArray, -1))
            else:
                p.cell.tuzhuangMallItem(self.mallId, hxPage, hxPos, const.RES_KIND_INV, cPickle.dumps(dyeArray, -1))
        else:
            skinId = self.getUsingSkinId()
            if self.mallId == -1:
                info = self.getItemInfoByIdx(self.index)
                page = info.get('page', 0)
                pos = info.get('pos', 0)
                resKind = info.get('resKind', 0)
                self.realHuanfuInvItem(page, pos, resKind, skinId)
            else:
                self.realHuanfuMallItem(self.mallId, skinId)
        self.onCloseBuyConfirm()

    def onOpenConfirmWindow(self, *arg):
        if self.mallId != -1:
            if self.index < 0 or self.index >= len(self.cacheItemsInfo):
                return
            mid = MID.data.get(self.mallId, {})
            itemId = mid.get('itemId', 0)
            itemName = mid.get('itemName', '')
            for _, _, _, it in self.rideWingItems:
                if it.getParentId() == it.parentId(itemId):
                    msg = gameStrings.MSG_BUY_TUZHUANG % itemName
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.realOpenConfirmWindow)
                    break
            else:
                self.realOpenConfirmWindow()

        else:
            self.realOpenConfirmWindow()

    def realOpenConfirmWindow(self):
        if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG:
            if self.ttlType:
                self.uiAdapter.loadWidget(uiConst.WIDGET_TUZHUANG_CONFIRM)
            else:
                p = BigWorld.player()
                p.showGameMsg(GMDD.data.TUZHUANG_NO_CHOOSE_HUANXING, ())
        elif self.ttlType or not self.skinIndex and self.mallId != -1:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TUZHUANG_CONFIRM)
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.TUZHUANG_NO_CHOOSE_HUANXING, ())

    def onCloseBuyConfirm(self, *args):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TUZHUANG_CONFIRM)

    def onGotoBack(self, *arg):
        if self.med:
            self.med.Invoke('hideItemDetial')
        self.setPlayerModelActionRate(1)

    def onCancelTuZhuang(self, *arg):
        self.updateItemDetial()
        model = self.getRideModel() if self.getRideModel() else self.getWingModel()
        self._dyeModel(model)

    def getRideModel(self):
        return self.uiAdapter.fittingRoom.rideModel

    def getWingModel(self):
        return self.uiAdapter.fittingRoom.wingModel

    def onChangeSlider(self, *arg):
        data0 = arg[3][0].GetString()
        data1 = int(arg[3][1].GetNumber())
        channel, part = getChannelFromUI(data0, data1)
        value = int(arg[3][2].GetNumber())
        if data0 == 'light':
            value -= 1
        if channel == const.DYE_CHANNEL_LIGHT and value == -1:
            self.handleValueCancel(data0, data1, channel, part, value)
        else:
            self.handleValueChange(data0, data1, channel, part, value)

    def updateCostMc(self):
        if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG:
            dyeArray = self.createConsumeItem()
            price = self.getPriceVal(dyeArray, False)
            dyeInfoArray = []
            p = BigWorld.player()
            for dyeId in dyeArray:
                count = p.inv.countItemInPages(dyeId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                dyeInfoArray.append(uiUtils.getGfxItemById(dyeId, '%d/%d' % (count, self.getConsumeNum())))

            ret = {'priceVal': price,
             'priceType': 1,
             'item': dyeInfoArray}
            self.showCostMc(ret)

    def updateHuanfuCostMc(self):
        visible = True
        if self.mallId != -1 and self.skinIndex == 0:
            visible = False
        hasSkin = self.hasSkin()
        isUsingSkin = False
        currentSkin = getattr(self.item, 'currentSkin', 0)
        if self.skinIndex:
            skins = self.getItemSkins(self.item)
            subSkin = skins[self.skinIndex - 1]
            isUsingSkin = currentSkin in subSkin
        else:
            isUsingSkin = not currentSkin
        ret = {'hasSkin': hasSkin,
         'visible': visible,
         'isUsingSkin': isUsingSkin}
        self.showHuanfuCostMc(ret)

    def handleValueChange(self, data0, data1, channel, part, value):
        self.setPartClickIndex(channel, part, value)
        self.updateAllDisplay(data0, data1, channel, part, value)

    def handleValueCancel(self, data0, data1, channel, part, value):
        self.setPartClickIndex(channel, part, value)
        if channel == const.DYE_CHANNEL_LIGHT:
            self.dyeList[channel] = []
        else:
            self.setPartDyeList(channel, part, const.DEFAULT_TZ_PART_DYES[part])
        self.updateAllDisplay(data0, data1, channel, part, value)

    def updateAllDisplay(self, data0, data1, channel, part, value):
        model = self.getRideModel() if self.getRideModel() else self.getWingModel()
        self._dyeModel(model)
        self.updateCostMc()
        priceType = 1
        priceVal = 0
        if channel in (const.DYE_CHANNEL_TEXTURE, const.DYE_CHANNEL_LIGHT):
            dyeId = self.getSelectedDyeListItem(channel, part)
            if dyeId:
                priceVal = self.getPriceVal([dyeId])
        else:
            dyeArray = []
            for channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
                dyeId = self.getSelectedDyeListItem(channel, part)
                if dyeId:
                    dyeArray.append(dyeId)

            priceVal = self.getPriceVal(dyeArray)
        self.showItemPriceVal(data0, {'priceVal': priceVal,
         'priceType': priceType})

    def _dyeModel(self, model):
        if self.dyeClickIndex.has_key(const.DYE_CHANNEL_TEXTURE) and self.dyeClickIndex[const.DYE_CHANNEL_TEXTURE].has_key(0):
            tintId = self.getSelectedDyeListItem(const.DYE_CHANNEL_TEXTURE, 0)
            if tintId:
                tint = getInfoFromTMD(tintId, 'texture')
                TA.ta_del([model], 'tuzhuang2')
                TA.ta_set_static([model], tint)
                return
        dyeTint = TED.data.get(self.item.id, {}).get('dyeTint', 'Default')
        if model:
            m = tuZhuangDyeMorpher.TuZhuangDyeMorpher(model)
            m.read(self.createConfig(), dyeTint)
            m.apply()

    def createConfig(self):
        for channel in self.dyeClickIndex:
            if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
                colorId = self.getSelectedDyeListItem(channel, 0)
                if colorId:
                    color = getInfoFromTMD(colorId, 'color')
                    self.setPartDyeList(channel, 0, color)
                caizhiId = self.getSelectedDyeListItem(channel, 1)
                if caizhiId:
                    material = getInfoFromTMD(caizhiId, 'material')
                    self.setPartDyeList(channel, 1, material)
                gaoguangValue = self.getPartClickIndex(channel, 2)
                if gaoguangValue:
                    self.setPartDyeList(channel, 2, gaoguangValue)
            elif channel == const.DYE_CHANNEL_LIGHT:
                lightId = self.getSelectedDyeListItem(channel, 0)
                if lightId:
                    light = getInfoFromTMD(lightId, 'light')
                    self.setPartDyeList(channel, 0, light)

        ret = []
        for channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
            value = self.dyeList[channel]
            if len(value) < len(const.DEFAULT_TZ_PART_DYES):
                value = value + const.DEFAULT_TZ_PART_DYES[len(value):]
            ret += value

        if self.dyeList[const.DYE_CHANNEL_LIGHT] and self.dyeList[const.DYE_CHANNEL_LIGHT][0]:
            ret.append(self.dyeList[const.DYE_CHANNEL_LIGHT][0])
        return ret

    def createConsumeItem(self):
        dyeArray = []
        if self.dyeClickIndex.has_key(const.DYE_CHANNEL_TEXTURE) and self.dyeClickIndex[const.DYE_CHANNEL_TEXTURE].has_key(0):
            tintId = self.getSelectedDyeListItem(const.DYE_CHANNEL_TEXTURE, 0)
            if tintId:
                if getInfoFromTMD(tintId, 'needConsume', 0):
                    dyeArray.append(tintId)
                return dyeArray
        lightId = self.getSelectedDyeListItem(const.DYE_CHANNEL_LIGHT, 0)
        if lightId and getInfoFromTMD(lightId, 'needConsume', 0):
            dyeArray.append(lightId)
        for channel in self.dyeClickIndex:
            if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
                colorId = self.getSelectedDyeListItem(channel, 0)
                if colorId and getInfoFromTMD(colorId, 'needConsume', 0):
                    dyeArray.append(colorId)
                caizhiId = self.getSelectedDyeListItem(channel, 1)
                if caizhiId and getInfoFromTMD(caizhiId, 'needConsume', 0):
                    dyeArray.append(caizhiId)

        return dyeArray

    def getPriceVal(self, dyeArray, ignoreNum = True):
        priceVal = 0
        p = BigWorld.player()
        for dyeId in dyeArray:
            count = p.inv.countItemInPages(dyeId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            needNum = 1
            if not ignoreNum:
                needNum = self.getConsumeNum()
            if count < needNum:
                mallId = getInfoFromTMD(dyeId, 'mallId', 0)
                priceVal += MID.data.get(mallId, {}).get('priceVal', 0) * (needNum - count)

        return priceVal

    def getConsumeNum(self):
        ttlRate = SCD.data.get('tuzhuangTTLRate', {})
        ttlType = self.ttlType
        if not ttlRate.has_key(ttlType):
            ttlType = 1
        return ttlRate.get(ttlType, (1, 604800))[0]

    def onTuZhuangItem(self, *arg):
        self.mallId = int(arg[3][0].GetNumber())
        buyNum = int(arg[3][1].GetNumber())
        self.index = int(arg[3][2].GetString()[9:])
        itemInfo = self.getItemInfoByIdx(self.index)
        self.enterTuZhuang = True
        if self.item and self.item.id == itemInfo['itemId']:
            self.playerModelCallback()
        self.updateItemDetial()

    def freeModel(self, model):
        p = BigWorld.player()
        if model:
            if model.inWorld:
                p.delModel(model)
            TA.ta_reset([model])
            model.texturePriority = 0

    def updateItemDetial(self):
        itemInfo = self.getItemInfoByIdx(self.index)
        if not itemInfo:
            return
        else:
            if self.mallId == -1:
                self.item = self.usedRideWingItems[self.index][-1]
            else:
                self.item = item.Item(itemInfo['itemId'])
            oldItem = gameglobal.rds.ui.fittingRoom.item
            if not oldItem or oldItem.id != itemInfo['itemId']:
                item_ = Item(self.item.id)
                gameglobal.rds.ui.fittingRoom.addFullScreenItem(item_)
            if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG:
                self.dyeClickIndex = {}
                self.dyeListItem = self.getDyeListItem(self.item.id)
                self.dyeList = self.getDyeListInfo(None)
                self.ttlType = 0
                ret = {}
                ret['dyeList'] = self.getDyeDetail(self.item)
                ret['item'] = itemInfo
                self.showItemDetial(ret)
            else:
                ret = {}
                skinTextrue = self.getItemSkinsTexture(self.item)
                ret['texture'] = skinTextrue
                ret['item'] = itemInfo
                self.skinIndex, self.ttlType = skinTextrue[0]
                self.showItemSkins(ret)
                self.updateHuanfuCostMc()
            return

    def setPlayerModelActionRate(self, rate):
        models = [gameglobal.rds.ui.fittingRoom.model]
        if self.getWingModel():
            models.append(self.getWingModel())
        for model in models:
            if model and len(model.queue):
                act = model.queue[-1]
                model.action(act)(0, None, 0, rate)

    def playerModelCallback(self):
        if self.enterTuZhuang:
            self.enterTuZhuang = False
            BigWorld.callback(0.7, Functor(self.setPlayerModelActionRate, 0.3))

    def showItemDetial(self, info):
        if self.med:
            self.med.Invoke('showItemDetial', uiUtils.dict2GfxDict(info, True))

    def showBar(self, range, showType = BAR_TYPE_COLOR):
        if self.med:
            self.med.Invoke('showBar', (uiUtils.array2GfxAarry(range, True), GfxValue(showType)))

    def hideBar(self):
        if self.med:
            self.med.Invoke('hideBar')

    def showCostMc(self, data):
        if self.med:
            self.med.Invoke('showCostMc', uiUtils.dict2GfxDict(data, True))

    def showHuanfuCostMc(self, data):
        if self.med:
            self.med.Invoke('showHuanfuCostMc', uiUtils.dict2GfxDict(data, True))

    def showItemPriceVal(self, areaName, data):
        if self.med:
            self.med.Invoke('showItemPriceVal', (GfxValue(areaName), uiUtils.dict2GfxDict(data, True)))

    def getDyeDetail(self, item):
        ret = self.getDyeListInfo(item)
        texArray = [ret[const.DYE_CHANNEL_TEXTURE], [gameStrings.TEXT_TUZHUANGPROXY_631]]
        ret[const.DYE_CHANNEL_TEXTURE] = texArray
        for dyeId in self.dyeListItem[const.DYE_CHANNEL_TEXTURE][PY_PART_MAP[textureArea]]:
            textureIcon = getInfoFromTMD(dyeId, 'textureIcon', 0)
            hasSuffix = getInfoFromTMD(dyeId, 'needConsume', 0)
            texArray[1].append(('tuZhuang/%d.dds' % textureIcon, hasSuffix))

        lightIndex = len(self.dyeListItem[const.DYE_CHANNEL_LIGHT][PY_PART_MAP[globalLight]])
        lightArray = ret[const.DYE_CHANNEL_LIGHT]
        if not lightArray:
            lightArray.append(0)
        lightArray.append(0)
        lightArray.append(lightIndex)
        for channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
            dye = ret[channel]
            if len(dye) >= 1:
                dye[0] = self.transColorStr(dye[0])
            if len(dye) >= 2:
                dye[1] = self.getCaizhiName(channel, 1, dye[1])
            if len(dye) >= 3:
                dye[2] = float(dye[2])

        return ret

    def getDyeListInfo(self, item):
        dyeList = getattr(item, 'dyeList', [])
        return utils.getTuZhuangDyeListInfo(dyeList)

    def getDyeListItem(self, itemId):
        dyeListItem = {}
        ted = TED.data.get(itemId, {})
        for channel, keys in TUZHUANG_DYE_ITEM_MAP.iteritems():
            dyeListItem[channel] = {}
            for key in keys:
                dyeIds = ted.get(key, [])
                dyeListItem[channel][PY_PART_MAP[key]] = dyeIds

        return dyeListItem

    def getCaizhiName(self, channel, part, value):
        dyeIds = self.getPartDyeListItem(channel, part)
        for dyeId in dyeIds:
            if float(value) == getInfoFromTMD(dyeId, 'material'):
                return getInfoFromTMD(dyeId, 'materialName', '')

        return ''

    def transColorStr(self, color):
        if type(color) in (tuple, list):
            color = color[0]
        color = [ int(r) for r in color.split(',') ]
        for i in xrange(3):
            color[i] = min(color[i], 255)

        return ((color[0] << 16) + (color[1] << 8) + color[2], color[3])

    def retransColorStr(self, color, alpha):
        pass

    def onChooseNextItem(self, *arg):
        offset = int(arg[3][0].GetNumber())
        newIndex = self.index + offset
        itemInfo = self.getItemInfoByIdx(newIndex)
        if not itemInfo:
            return
        self.index = newIndex
        self.mallId = itemInfo['mallId']
        self.enterTuZhuang = True
        self.updateItemDetial()

    def onSearchItem(self, *arg):
        self.searchKeyWord = ui.unicode2gbk(arg[3][0].GetString())
        self.tabMgr.setSelectedChildId(tianyuMallProxy.MAIN_TAB_FS_SEARCH)

    def insertSubTabInfos(self, mainTabs):
        for i in xrange(len(mainTabs) - 2):
            mainTabInfo = mainTabs[i]
            mainTab = self.tabMgr.getChild(mainTabInfo['mainId'])
            if not mainTab:
                continue
            allSubTabs = mainTab.getChildrenInfo()
            mainTabInfo['subTabList'] = allSubTabs

        return mainTabs

    def onGetAllTabsInfo(self, *arg):
        allMainTabs = self.tabMgr.getChildrenInfo()
        allMainTabs[-1] = tianyuMallProxy.MAIN_TAB_TUZHUANG
        allMainTabs = self.insertSubTabInfos(allMainTabs)
        return uiUtils.array2GfxAarry(allMainTabs, True)

    def onGetMallItemList(self, *arg):
        mainId = int(arg[3][0].GetNumber())
        subId = int(arg[3][1].GetNumber())
        self.mainTab = mainId
        mallProxy = gameglobal.rds.ui.tianyuMall
        if mainId == tianyuMallProxy.MAIN_TAB_FS_SEARCH:
            itemsInfo = self.getSearchItemList()
        else:
            itemsInfo = self.getTabItemList(mainId, subId)
        itemsInfo = mallProxy.appendLimitInfo(itemsInfo)
        self.cacheItemsInfo = itemsInfo
        return uiUtils.array2GfxAarry(itemsInfo, True)

    def getSearchItemList(self):
        searchResult = self.tabMgr.searchByKeyWord(self.searchKeyWord)
        itemsInfo = searchResult['itemsInfo']
        return [ child for child in itemsInfo if child.get('validPeriod', 0) < 0 ]

    def getTabItemList(self, mainId, subId):
        self.tabMgr.setSelectedChildId(mainId)
        self.tabMgr.getSelChild().setSelectedChildId(subId)
        itemsInfo = self.tabMgr.getSelChild().getSelChild().getChildrenInfo()
        return [ child for child in itemsInfo if child.get('validPeriod', 0) < 0 or child.get('mallId') == -1 ]

    def onGetMyPointsInfo(self, *arg):
        pointsInfo = {}
        p = BigWorld.player()
        pointsInfo['account'] = getattr(p, 'roleURS', gameStrings.TEXT_RECHARGEPROXY_34)
        pointsInfo['commonPoints'] = p.commonPoints + p.specialPoints
        pointsInfo['standbyPoints'] = p.standbyPoints
        pointsInfo['allPoints'] = p.standbyPoints + p.commonPoints + p.specialPoints
        pointsInfo['rate'] = 1.0
        return uiUtils.dict2GfxDict(pointsInfo, True)

    def getMyMoneyInfo(self):
        attrValid = True
        p = BigWorld.player()
        ret = {'tianbi': 0,
         'tianquan': 0,
         'jifen': 0,
         'cash': 0,
         'unBindCoin': 0,
         'bindCoin': 0}
        attrValid &= hasattr(p, 'unbindCoin')
        attrValid &= hasattr(p, 'bindCoin')
        attrValid &= hasattr(p, 'freeCoin')
        attrValid &= hasattr(p, 'mallCash')
        attrValid &= hasattr(p, 'mallScore')
        attrValid &= hasattr(p, 'totalMallScore')
        if not attrValid:
            return ret
        ret['tianBi'] = p.unbindCoin + p.bindCoin + p.freeCoin
        ret['tianQuan'] = p.mallCash
        ret['jiFenBi'] = p.mallScore
        ret['totalJiFen'] = p.totalMallScore
        ret['cash'] = getattr(p, 'cash', 0)
        ret['unBindCoin'] = getattr(p, 'unbindCoin', 0)
        ret['bindCoin'] = getattr(p, 'bindCoin', 0) + getattr(p, 'freeCoin', 0)
        return ret

    def onGetMyMoneyInfo(self, *arg):
        return uiUtils.dict2GfxDict(self.getMyMoneyInfo(), True)

    def reset(self):
        self.cacheItemsInfo = None
        self.index = -1
        self.item = None
        self.mallId = -1
        self.dyeMap = {const.DYE_CHANNEL_1: ['255,255,255,255', '1', '1'],
         const.DYE_CHANNEL_2: ['255,255,255,255', '1', '1'],
         const.DYE_CHANNEL_3: ['255,255,255,255', '1', '1']}
        self.dyeTexture = ''
        self.dyeListItem = {}
        self.dyeList = {}
        self.dyeClickIndex = {}
        self.enterTuZhuang = False
        self.ttlType = 0
        self.rideWingItems = []
        self.usedRideWingItems = []
        self.mainTab = tianyuMallProxy.MAIN_TAB_TUZHUANG
        self.skinIndex = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TUZHUANG:
            self.med = mediator
            self.tabMgr.initTabs()
            self.isShow = True
            self.initInvItem()
        elif widgetId == uiConst.WIDGET_TUZHUANG_CONFIRM:
            self.buyConfirmMediator = mediator
            ret = {}
            ret['moneyInfo'] = self.getMyMoneyInfo()
            ret['itemInfo'] = self.getItemInfoByIdx(self.index)
            p = BigWorld.player()
            if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG:
                dyeArray = self.createConsumeItem()
                allPrice = ret['itemInfo']['priceVal']
                ret['moneyInfo']['allPrice'] = allPrice
                dyeArray.insert(0, self.huanXingItems[self.ttlType])
                itemList = []
                for i, dyeId in enumerate(dyeArray):
                    count = p.inv.countItemInPages(dyeId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                    numInfo = {'num': '%d/%d' % (count, 1 if i == 0 else self.getConsumeNum())}
                    dyeData = uiUtils.getGfxItemById(dyeId, appendInfo=numInfo)
                    dyeData['name'] = uiUtils.getItemColorName(dyeId)
                    itemList.append(dyeData)

                ret['itemList'] = itemList
            else:
                skinId = self.getUsingSkinId()
                count = 0
                if skinId:
                    count = p.inv.countItemInPages(skinId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                    numInfo = {'num': '%d/%d' % (count, 1)}
                    skinData = uiUtils.getGfxItemById(skinId, appendInfo=numInfo)
                    skinData['name'] = uiUtils.getItemColorName(skinId)
                    ret['itemList'] = [skinData]
                allPrice = ret['itemInfo']['priceVal']
                ret['moneyInfo']['allPrice'] = allPrice
                if not count:
                    hsd = HSD.data.get(skinId, {})
                    mallId = hsd.get('mallId', 0)
                    price = MID.data.get(mallId, {}).get('priceVal', 0)
                    ret['moneyInfo']['allPrice'] += price
            return uiUtils.dict2GfxDict(ret, True)

    def show(self, callback = None):
        if not self.canShowTuZhuang():
            return
        gameglobal.rds.ui.fittingRoom.enterFullScreenFitting(self.afterModelFinished, False)
        gameglobal.rds.ui.fittingRoom.setPlayerModelFinishCallback(self.playerModelCallback)

    def afterModelFinished(self):
        self.uiAdapter.hideAllUI()
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_TUZHUANG, True)
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TUZHUANG)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.restoreUI()
        self.isShow = False
        self.med = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TUZHUANG)
        gameglobal.rds.ui.fittingRoom.leaveFullScreenFitting()

    def getItemInfoByIdx(self, idx):
        if self.mallId != -1:
            if idx < 0 or idx >= len(self.cacheItemsInfo):
                return {}
            return self.cacheItemsInfo[idx]
        elif idx < 0 or idx >= len(self.usedRideWingItems):
            return {}
        else:
            page, pos, resKind, it = self.usedRideWingItems[idx]
            mallId = -1
            mallLabel = 0
            info = {'page': page,
             'pos': pos,
             'resKind': resKind,
             'mallId': mallId,
             'itemId': it.id,
             'label': mallLabel}
            tianyuMallProxy.appendBasicItemInfo(info)
            info['itemName'] = info['name']
            info['priceType'] = gametypes.MALL_PRICE_TYPE_COIN
            info['priceVal'] = 0
            return info

    def onSetPreviewInfo(self, *arg):
        btnIdx = int(arg[3][0].GetNumber())
        itemMallInfo = self.getItemInfoByIdx(btnIdx)
        self.index = btnIdx
        if not itemMallInfo:
            return
        itemId = itemMallInfo['itemId']
        item_ = item.Item(itemId)
        self.item = item_
        gameglobal.rds.ui.fittingRoom.addFullScreenItem(item_)

    def onCancelPreviewInfo(self, *arg):
        btnIdx = int(arg[3][0].GetNumber())
        itemMallInfo = self.getItemInfoByIdx(btnIdx)
        if not itemMallInfo:
            return
        else:
            itemId = itemMallInfo['itemId']
            item_ = item.Item(itemId)
            self.item = None
            gameglobal.rds.ui.fittingRoom.delFullScreenItem(item_)
            return

    def onSaveColor(self, *arg):
        channel = int(arg[3][0].GetNumber())
        color = arg[3][1].GetString()
        gloss = arg[3][2].GetString()
        sranseA = arg[3][3].GetString()
        texture = arg[3][4].GetString()
        if color:
            self.dyeMap[channel][0] = color
        if gloss:
            self.dyeMap[channel][1] = gloss
        if sranseA:
            self.dyeMap[channel][2] = sranseA
        self.dyeTexture = texture
        ret = []
        for channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
            ret += self.dyeMap[channel]

        if self.dyeTexture:
            ret.append(self.dyeTexture)
        if not self.item:
            return
        model = self.getRideModel() if self.getRideModel() else self.getWingModel()
        dyeTint = TED.data.get(self.item.id, {}).get('dyeTint', 'Default')
        if model:
            m = tuZhuangDyeMorpher.TuZhuangDyeMorpher(model)
            m.read(ret, dyeTint)
            m.apply()

    def isShowDyeTest(self, *arg):
        return GfxValue(not BigWorld.isPublishedVersion() and self.dyeTestVis)

    def onSelectHuanXingTTL(self, *arg):
        self.ttlType = int(arg[3][0].GetNumber()) + 1
        self.updateCostMc()

    def refreshMyMoney(self):
        if self.med:
            self.med.Invoke('refreshMyMoney')

    def clickCancelColor(self, *arg):
        data0 = arg[3][0].GetString()
        data1 = int(arg[3][1].GetNumber())
        channel, part = getChannelFromUI(data0, data1)
        gamelog.debug('clickCancelColor', channel, part)
        self.handleValueCancel(data0, data1, channel, part, -1)

    def onGetInvItemInfo(self, *arg):
        ret = []
        self.usedRideWingItems = self.getInvItemByMainTab()
        for i, (_, _, _, it) in enumerate(self.usedRideWingItems):
            data = uiUtils.getGfxItemById(it.id)
            data['index'] = i
            ret.append(data)

        return uiUtils.array2GfxAarry(ret)

    def initInvItem(self):
        wingItems = []
        rideItems = []
        p = BigWorld.player()
        for pg in p.inv.getPageTuple():
            for ps in p.inv.getPosTuple(pg):
                it = p.inv.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.isWingEquip():
                    wingItems.append((pg,
                     ps,
                     const.RES_KIND_INV,
                     it))
                elif it.isRideEquip():
                    rideItems.append((pg,
                     ps,
                     const.RES_KIND_INV,
                     it))

        if p.equipment[gametypes.EQU_PART_RIDE]:
            rideItems.append((0,
             gametypes.EQU_PART_RIDE,
             const.RES_KIND_EQUIP,
             p.equipment[gametypes.EQU_PART_RIDE]))
        if p.equipment[gametypes.EQU_PART_WINGFLY]:
            rideItems.append((0,
             gametypes.EQU_PART_WINGFLY,
             const.RES_KIND_EQUIP,
             p.equipment[gametypes.EQU_PART_WINGFLY]))
        self.rideWingItems = rideItems + wingItems

    def getItemSkins(self, item):
        esd = ESD.data.get(item.id, {})
        skinNumber = esd.get('skinNumber', 0)
        skin = esd.get('skin', [])
        return skin[:skinNumber]

    def getItemSkinsTexture(self, item):
        skin = self.getItemSkins(item)
        currentSkin = getattr(item, 'currentSkin', 0)
        dyeSkins = getattr(item, 'dyeSkins', {})
        index = (0, 0)
        for i, subSkin in enumerate(skin):
            if currentSkin in subSkin:
                index = (i, subSkin.index(currentSkin))
                break

        texArray = [(gameStrings.HUANXING_ORIGINAL_SKIN, 0)]
        ret = [index, texArray]
        for subSkin in skin:
            hasSkin = False
            for usedSkin, ttl in dyeSkins.iteritems():
                if usedSkin in subSkin and (ttl == 0 or utils.getNow() <= ttl):
                    hasSkin = True
                    break

            dyeId = subSkin[-1]
            hsd = HSD.data.get(dyeId, {})
            if hasSkin:
                textureIcon = hsd.get('textureIcon', 0)
            else:
                textureIcon = hsd.get('textureDisableIcon', 3)
            texArray.append(('tuZhuang/%d.dds' % textureIcon, False))

        return ret

    def showItemSkins(self, data):
        if self.med:
            self.med.Invoke('showItemSkins', uiUtils.dict2GfxDict(data, True))

    def onClickSkinBtn(self, *arg):
        index = arg[3][1].GetInt()
        self.skinIndex = index
        self.updateHuanfuCostMc()
        skinId = self.getUsingSkinId()
        hsd = HSD.data.get(skinId, {})
        realDyeId = hsd.get('realDyeId', 0)
        if realDyeId:
            item_ = Item(realDyeId)
        else:
            item_ = Item(self.item.id)
        gameglobal.rds.ui.fittingRoom.addFullScreenItem(item_)

    def getInvItemByMainTab(self):
        ret = []
        for item in self.rideWingItems:
            it = item[-1]
            if self.mainTab == tianyuMallProxy.MAIN_TAB_TUZHUANG and it.id in TED.data.iterkeys() or self.mainTab == tianyuMallProxy.MAIN_TAB_HUANFU and it.id in ESD.data.iterkeys():
                ret.append(item)

        return ret

    def showInvItem(self):
        if self.med:
            self.med.Invoke('initInv')

    def getUsingSkinId(self):
        if self.skinIndex:
            skins = self.getItemSkins(self.item)
            subSkin = skins[self.skinIndex - 1]
            if self.ttlType and 0 <= self.ttlType - 1 < len(subSkin):
                return subSkin[self.ttlType - 1]
            else:
                return subSkin[-1]
        return 0

    def onApplyOldSkin(self, *arg):
        oldSkin = 0
        if self.skinIndex:
            skins = self.getItemSkins(self.item)
            subSkin = skins[self.skinIndex - 1]
            dyeSkins = getattr(self.item, 'dyeSkins', {})
            for usedSkin, ttl in dyeSkins.iteritems():
                if usedSkin in subSkin and (ttl == 0 or utils.getNow() <= ttl):
                    oldSkin = usedSkin
                    break

        info = self.getItemInfoByIdx(self.index)
        page = info.get('page', 0)
        pos = info.get('pos', 0)
        resKind = info.get('resKind', 0)
        self.realHuanfuInvItem(page, pos, resKind, oldSkin)

    def hasSkin(self):
        if not self.skinIndex:
            return True
        skins = self.getItemSkins(self.item)
        subSkin = skins[self.skinIndex - 1]
        dyeSkins = getattr(self.item, 'dyeSkins', {})
        for usedSkin, ttl in dyeSkins.iteritems():
            if usedSkin in subSkin and (ttl == 0 or utils.getNow() <= ttl):
                return True

        return False

    def switchHuanfuHuanxing(self, *arg):
        self.mainTab = arg[3][0].GetInt()
        self.showInvItem()

    def realHuanfuInvItem(self, page, pos, resKind, skinId):
        p = BigWorld.player()
        it = uiUtils.getItemByKind(page, pos, resKind, p)
        if not it:
            return
        if it.id not in ESD.data.iterkeys():
            return
        p.cell.huanfuInvItem(page, pos, resKind, skinId)

    def realHuanfuMallItem(self, mallId, skinId):
        if self.mallId == -1:
            return
        mid = MID.data.get(mallId, {})
        itemId = mid.get('itemId', 0)
        if itemId not in ESD.data.iterkeys():
            return
        p = BigWorld.player()
        p.cell.huanfuMallItem(mallId, skinId)
