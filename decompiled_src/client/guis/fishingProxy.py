#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fishingProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gametypes
from uiProxy import SlotDataProxy
from guis import ui
from guis import uiUtils
from ui import gbk2unicode
from item import Item
from helpers import fishing
from callbackHelper import Functor
from data import item_data as ID
from cdata import font_config_data as FCD
from data import fish_data as FD
from data import special_life_skill_equip_data as SLSED
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import consumable_item_data as CID

class FishingProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FishingProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'manualFishing': self.onManualFishing,
         'autoFishing': self.onAutoFishing,
         'clickSlot': self.onClickSlot,
         'selectItem': self.onSelectItem,
         'unselectItem': self.onUnselectItem,
         'getFishingDistance': self.onGetFishingDistance,
         'getContorlVal': self.onGetContorlVal,
         'upRodBeforeBite': self.onUpRodBeforeBite,
         'throwRod': self.onThrowRod,
         'isAuto': self.onIsAuto,
         'autoUpRod': self.onAutoUpRod,
         'getResultData': self.onGetResultData,
         'cancelAutoFishing': self.onCancelAutoFishing,
         'pickFish': self.onPickFish,
         'discardFish': self.onDiscardFish,
         'closeEndPanel': self.onCloseEndPanel,
         'getFishingItem': self.onGetFishingItem,
         'chargeFinish': self.onChargeFinish,
         'getChargeVal': self.onGetChargeVal,
         'restart': self.onRestart,
         'getIllustrationInfo': self.onGetIllustrationInfo,
         'closeIllustration': self.onCloseIllustration,
         'getFishingIllustrationTips': self.onGetFishingIllustrationTips,
         'exitFishing': self.onExitFishing,
         'setChargeForDistState': self.onSetChargeForDistState,
         'checkCanFish': self.onCheckCanFish,
         'getChargingData': self.onGetChargingData,
         'inCharging': self.onInCharging,
         'inPull': self.onInPull,
         'getBaitInfo': self.onGetBaitInfo,
         'clickBaitSlot': self.onClickBaitSlot,
         'removeEquipBait': self.removeEquipBait,
         'getSeekNpcHttp': self.onGetSeekNpcHttp,
         'flyTrack': self.onFlyTrack}
        self.FishStartMediator = None
        self.FishMediator = None
        self.FishEndMediator = None
        self.IllustrationMediator = None
        self.bindType = 'fishing'
        self.type = 'fishing'
        self.isAuto = False
        self.fishingItem = [None] * 5
        self.fishingResult = [0, 0]
        self.isChargingForDist = False
        self.restartHandler = None
        self.restart = False
        self.labelCallback = None
        self.inCharging = False
        self.fishId = None
        self.inPull = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_FISHING_START, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FISHING, self.stopFishing)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FISHING_ILLUSTARTION, self.closeFishingIllustration)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FISHING_START:
            self.FishStartMediator = mediator
        elif widgetId == uiConst.WIDGET_FISHING:
            self.FishMediator = mediator
        elif widgetId == uiConst.WIDGET_FISHING_END:
            self.FishEndMediator = mediator
        elif widgetId == uiConst.WIDGET_FISHING_ILLUSTARTION:
            self.IllustrationMediator = mediator

    def show(self):
        p = BigWorld.player()
        if not p.checkFishEquip():
            return
        p.stopFish()
        self.closeFishing()
        if p.fishingMgr:
            p.fishingMgr.clearAutoTimer()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHING_START)

    def showFishingStart(self):
        p = BigWorld.player()
        if p.inFishingReady():
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHING_START)

    def showFishing(self):
        self.isChargingForDist = False
        self.inCharging = False
        self.inPull = False
        self.fishId = None
        if self.labelCallback:
            BigWorld.cancelCallback(self.labelCallback)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHING)

    def showFishingEnd(self):
        self.closeFishing()

    def showFishingIllustration(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHING_ILLUSTARTION)

    def clearWidget(self):
        self.closeFishingStart()
        self.closeFishing()
        self.closeFishingEnd()

    def reset(self):
        self.fishingItem = [None] * 5

    def closeFishingStart(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHING_START)
        self.FishStartMediator = None

    def closeFishing(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHING)
        self.FishMediator = None
        self.isChargingForDist = False
        self.inCharging = False
        self.fishId = None
        self.inPull = False
        gameglobal.rds.sound.stopSound(gameglobal.SD_411)
        if self.labelCallback:
            BigWorld.cancelCallback(self.labelCallback)
        if gameglobal.rds.ui.inventory.itemFilter == uiConst.FILTER_ITEM_BAIT:
            gameglobal.rds.ui.inventory.itemFilter = uiConst.FILTER_ITEM_ALL
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def closeFishingEnd(self):
        self.FishEndMediator = None

    def closeFishingIllustration(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHING_ILLUSTARTION)
        self.IllustrationMediator = None

    def getSlotID(self, key):
        _, idSlot = key.split('.')
        return (0, int(idSlot[4:]))

    def _getKey(self, bar, slot):
        return 'fishing.slot%d' % slot

    def equipBait(self, item, nPageSrc, nItemSrc, nPageDes, nItemDes):
        if item == const.CONT_EMPTY_VAL:
            return
        if getattr(item, 'cstype', 0) == Item.SUBTYPE_2_FISHING_BAIT:
            if item.canEquipFishing(BigWorld.player().fishingLv, gametypes.FISHING_EQUIP_BAIT) == Item.EQUIPABLE:
                BigWorld.player().cell.setConsumableFishingEquip(nItemDes + 3, item.id)

    def removeEquipBait(self, *arg):
        BigWorld.player().cell.setConsumableFishingEquip(gametypes.FISHING_EQUIP_BAIT, 0)

    def setItem(self, item, bar, slot):
        if not item:
            return
        self.fishingItem[slot] = item
        key = self._getKey(bar, slot)
        iconPath = uiUtils.getItemIconFile40(item.id)
        data = self.uiAdapter.movie.CreateObject()
        data.SetMember('iconPath', GfxValue(iconPath))
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        self.setSlotColor(slot, color)
        if self.binding.has_key(key):
            self.binding[key][1].InvokeSelf(data)

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.get(key, None):
            self.fishingItem[slot] = None
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.setSlotColor(slot, 'nothing')
            if self.FishStartMediator != None:
                self.FishStartMediator.Invoke('resetSlotState', GfxValue(slot))

    def setSlotColor(self, idSlot, color):
        if self.FishStartMediator != None:
            self.FishStartMediator.Invoke('setSlotColor', (GfxValue(idSlot), GfxValue(color)))

    def upFishingRod(self, rarity):
        if self.FishMediator != None:
            self.FishMediator.Invoke('upFishingRod', GfxValue(rarity))

    def showResult(self, res):
        if self.FishMediator != None:
            self.FishMediator.Invoke('showResult', GfxValue(res))
            if res == uiConst.FISHING_SUCCESS:
                gameglobal.rds.sound.playSound(gameglobal.SD_413)
                gameglobal.rds.sound.playSound(gameglobal.SD_412)
            else:
                gameglobal.rds.sound.playSound(gameglobal.SD_414)
                gameglobal.rds.sound.playSound(gameglobal.SD_450)
        if not self.isAuto:
            BigWorld.callback(1, self.restartFishing)

    def _genItemArr(self):
        p = BigWorld.player()
        slots = []
        posMap = {0: gametypes.FISHING_EQUIP_ROD,
         1: gametypes.FISHING_EQUIP_BUOY,
         2: gametypes.FISHING_EQUIP_HOOK}
        for idx, item in enumerate(p.fishingEquip[3:]):
            if item:
                iconPath = uiUtils.getItemIconFile40(item.id)
                cData = CID.data.get(item.id)
                desc = SCD.data.get('fishingSlotDesc', gameStrings.TEXT_FISHINGPROXY_244)
                colorName = desc % (uiUtils.getItemColorName(item.id), str(cData.get('attraction', 0)))
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                count = p.inv.countItemInPages(item.id)
                if idx == 0:
                    selected = False
                elif count == 0:
                    selected = False
                    BigWorld.player().cell.switchFishingEnhance(posMap[idx - 1], False)
                    BigWorld.player().fishingEquip.switchEnhance(self, posMap[idx - 1], False)
                else:
                    selected = p.fishingEquip.isEnhance[posMap[idx - 1]]
            else:
                iconPath = ''
                color = 'nothing'
                count = 0
                selected = False
                colorName = SCD.data.get('notInFinshStartItem', gameStrings.TEXT_FISHINGPROXY_266)
            slots.append([{'iconPath': iconPath,
              'count': count,
              'color': color},
             color,
             selected,
             colorName])

        return slots

    def refreshFishingPanel(self):
        slots = self._genItemArr()
        if self.FishStartMediator != None:
            self.FishStartMediator.Invoke('refreshFishingItem', uiUtils.array2GfxAarry(slots, True))

    def setFloatMove(self, type):
        if self.FishMediator != None:
            self.FishMediator.Invoke('setFloatMove', GfxValue(type))
            gameglobal.rds.sound.playSound(gameglobal.SD_411)
            if type == uiConst.FLOAT_MOVE_FAST:
                gameglobal.rds.ui.showFishLabel(0, uiConst.FISHING_BITE)

    def restartFishing(self):
        self.closeFishing()
        player = BigWorld.player()
        if player.inFishing() or player.inFishingReady():
            self.showFishing()

    def stopFishing(self):
        BigWorld.player().showGameMsg(GMDD.data.FISHING_BREAK, ())
        BigWorld.player().stopFish()
        self.hide()

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if slot == 4:
            i = Item(self.fishingResult[0])
        else:
            i = BigWorld.player().fishingEquip[slot + 3]
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def onClosePanel(self, *arg):
        self.closeFishingStart()

    def onManualFishing(self, *arg):
        p = BigWorld.player()
        p.readyFish()
        self.isAuto = False

    def onAutoFishing(self, *arg):
        p = BigWorld.player()
        p.readyFish(const.ST_HOLD_FISHING)
        self.isAuto = True

    def readyFish(self, step = const.ST_READY_FISHING):
        p = BigWorld.player()
        if p.checkCanFish():
            self.closeFishingStart()
            self.showFishing()

    def onClickSlot(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onSelectItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        posMap = {0: gametypes.FISHING_EQUIP_ROD,
         1: gametypes.FISHING_EQUIP_BUOY,
         2: gametypes.FISHING_EQUIP_HOOK}
        BigWorld.player().cell.switchFishingEnhance(posMap[slot - 1], True)
        BigWorld.player().fishingEquip.switchEnhance(self, posMap[slot - 1], True)

    def onUnselectItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        posMap = {0: gametypes.FISHING_EQUIP_ROD,
         1: gametypes.FISHING_EQUIP_BUOY,
         2: gametypes.FISHING_EQUIP_HOOK}
        BigWorld.player().cell.switchFishingEnhance(posMap[slot - 1], False)
        BigWorld.player().fishingEquip.switchEnhance(self, posMap[slot - 1], False)

    def onGetFishingDistance(self, *arg):
        p = BigWorld.player()
        if p.fishingEquip[0]:
            ret = [5, (5 + p.fishingEquip[0].getMaxRange() + p.rodEnhance) / 2, p.fishingEquip[0].getMaxRange() + p.rodEnhance]
        else:
            ret = [0, 0, 0]
        return uiUtils.array2GfxAarry(ret)

    def onGetContorlVal(self, *arg):
        ret = 1
        p = BigWorld.player()
        if p.fishingEquip[0]:
            ret = p.fishingEquip[0].getControllability()
        return GfxValue(ret)

    def onUpRodBeforeBite(self, *arg):
        BigWorld.player().pullFish()

    def onThrowRod(self, *arg):
        dist = float(arg[3][0].GetString())
        gameglobal.rds.ui.showFishLabel(dist, uiConst.FISHING_NUMBER)
        self.labelCallback = BigWorld.callback(2, Functor(gameglobal.rds.ui.showFishLabel, 0, uiConst.FISHING_WAITING_BITE))
        BigWorld.player().startFish(dist, self.isAuto)

    def onIsAuto(self, *arg):
        return GfxValue(self.isAuto)

    def onAutoUpRod(self, *arg):
        pass

    def onGetResultData(self, *arg):
        iconPath = uiUtils.getItemIconFile40(self.fishingResult[0])
        itemName = ID.data.get(self.fishingResult[0], {}).get('name', '')
        ret = [{'iconPath': iconPath,
          'count': self.fishingResult[1]}, gbk2unicode(itemName), str(self.fishingResult[0])]
        return uiUtils.array2GfxAarry(ret)

    def onCancelAutoFishing(self, *arg):
        pass

    def onPickFish(self, *arg):
        BigWorld.player().cell.getFishBonus()
        self.closeFishingEnd()
        self.showFishing()

    def onDiscardFish(self, *arg):
        BigWorld.player().cell.discardFishBonus()
        self.closeFishingEnd()
        self.showFishing()

    def onCloseEndPanel(self, *arg):
        self.closeFishingEnd()
        self.showFishing()

    def onGetFishingItem(self, *arg):
        slots = self._genItemArr()
        return uiUtils.array2GfxAarry(slots, True)

    @ui.callFilter(2)
    def onChargeFinish(self, *arg):
        BigWorld.player().pullFish()

    def onGetChargeVal(self, *arg):
        ret = 1
        p = BigWorld.player()
        if p.fishingEquip[0]:
            ret = p.fishingEquip[0].getControllability()
        return GfxValue(ret)

    @ui.callFilter(2, False)
    def onRestart(self, *arg):
        self.showResult(uiConst.FISHING_ESCAPE)
        BigWorld.player().cell.stopFishing(True)
        BigWorld.player().restarFishing()

    def onGetIllustrationInfo(self, *arg):
        lv = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        res = []
        for key, val in FD.data.items():
            if val['lv'] == lv:
                item = Item(key)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                res.append([key in p.fishHistory,
                 uiUtils.getItemIconFile64(key),
                 str(key),
                 color])

        return uiUtils.array2GfxAarry(res)

    def onCloseIllustration(self, *arg):
        self.closeFishingIllustration()

    def onGetFishingIllustrationTips(self, *arg):
        id = int(arg[3][0].GetString())
        fData = FD.data.get(id, {})
        ret = ''
        if fData:
            ret += fData['name'] + '\n'
            ret += fData.get('posDesc', '') + '\n'
            ret += fData.get('useDesc', '') + '\n'
        return GfxValue(gbk2unicode(ret))

    def onExitFishing(self, *arg):
        BigWorld.player().stopFish()
        self.hide()

    def onSetChargeForDistState(self, *arg):
        self.isChargingForDist = arg[3][0].GetBool()
        if not self.isAuto and self.isChargingForDist:
            p = BigWorld.player()
            p.readyFish(const.ST_HOLD_FISHING)

    def onCheckCanFish(self, *arg):
        dist = float(arg[3][0].GetString())
        if dist == 0:
            p = BigWorld.player()
            return GfxValue(p.checkCanFish())
        else:
            dstPos = fishing.checkWater(dist)
            if dstPos:
                return GfxValue(True)
            if self.isAuto:
                self.closeFishing()
            return GfxValue(False)

    def onGetChargingData(self, *arg):
        ret = {}
        p = BigWorld.player()
        rData = SLSED.data.get(p.fishingEquip[0].id, {})
        fData = FD.data.get(self.fishId, {})
        ret['perfect'] = rData.get('perfectNum', 0)
        ret['fail'] = rData.get('failNum', 0)
        ret['changeRate'] = fData.get('feedBack', (1, 1))
        ret['moveSpeed'] = fData.get('moveSpeed', (1, 1))
        ret['increaseSpeed'] = rData.get('chargeSpeed', 0)
        ret['decreaseSpeed'] = fData.get('chargeMinus', 0)
        ret['offsetPixel'] = rData.get('offsetPixel', 0)
        return uiUtils.dict2GfxDict(ret, True)

    def onInCharging(self, *arg):
        self.inCharging = True
        self.inPull = False

    def isCharging(self):
        return self.inCharging

    def onInPull(self, *arg):
        self.inPull = arg[3][0].GetBool()

    def _createBaitInfo(self):
        p = BigWorld.player()
        item = p.fishingEquip[3]
        if item:
            iconPath = uiUtils.getItemIconFile40(item.id)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            count = p.inv.countItemInPages(item.id)
            itemId = item.id
        else:
            iconPath = 'notFound'
            color = 'nothing'
            count = 0
            itemId = 0
        ret = {'iconPath': iconPath,
         'count': count,
         'qualityColor': color,
         'itemId': itemId}
        return ret

    def onGetBaitInfo(self, *arg):
        ret = self._createBaitInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onClickBaitSlot(self, *arg):
        gameglobal.rds.ui.inventory.itemFilter = uiConst.FILTER_ITEM_BAIT
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()
        else:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def refreshBaitSlot(self):
        if self.FishMediator:
            self.FishMediator.Invoke('setBaitInfo', uiUtils.dict2GfxDict(self._createBaitInfo(), True))
            if gameglobal.rds.ui.inventory.itemFilter == uiConst.FILTER_ITEM_BAIT:
                gameglobal.rds.ui.inventory.hide()

    def onGetSeekNpcHttp(self, *arg):
        ret = SCD.data.get('fishingStartSeekNpcHttp', gameStrings.TEXT_FISHINGPROXY_545)
        ret = ret % SCD.data.get('fishingStartSeekId', 11013916)
        return GfxValue(gbk2unicode(ret))

    def onFlyTrack(self, *arg):
        seekId = SCD.data.get('fishingStartSeekId', 11013916)
        uiUtils.gotoTrack(seekId)
