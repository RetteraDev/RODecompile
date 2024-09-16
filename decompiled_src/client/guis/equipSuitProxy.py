#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipSuitProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import const
from guis import uiUtils, uiConst
from item import Item
from Scaleform import GfxValue
from uiProxy import SlotDataProxy
from guis import ui
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import equip_suits_data as ESD
from cdata import equip_suit_show_data as ESSD
from cdata import equip_suit_activation_data as ESAD
from callbackHelper import Functor
EQUIPSUIT_ICON_PATH = 'equipSuit/'

class EquipSuitProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipSuitProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeSuitActivate': self.onCloseSuitActivate,
         'resetEquipSlot': self.onResetEquipSlot,
         'activateSuit': self.onActivateSuit,
         'getDesc': self.onGetDesc,
         'selectSuit': self.onSelectSuit}
        self.bindType = 'equipSuit'
        self.type = 'equipSuit'
        self.activateMediator = None
        self.currentIndex = 0
        self.currentSuitId = None
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        self.activateMediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self, *arg):
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.activateMediator = None
        self.activateItemId = None
        self.activateUUID = None
        self.currentIndex = 0
        self.currentSuitId = None

    def show(self):
        pass

    def onActivateSuccess(self):
        if self.activateMediator:
            self.activateMediator.Invoke('activeSuccess')
            it, page, pos = BigWorld.player().inv.findItemByUUID(self.activateUUID)
            key = self._getKey(0, 0)
            self.updateEquipSlot(it, key)
            self.showEquipDetail(self.currentIndex, self.currentSuitId)

    def onGetDesc(self, *args):
        step1 = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ACTIVATE_STEP1, gameStrings.TEXT_EQUIPSUITPROXY_71)
        step2 = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ACTIVATE_STEP2, gameStrings.TEXT_EQUIPSUITPROXY_72)
        step3 = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ACTIVATE_STEP3, gameStrings.TEXT_EQUIPSUITPROXY_73)
        self.desc = [step1, step2, step3]
        return uiUtils.array2GfxAarry(self.desc, True)

    def onActivateSuit(self, *args):
        if not self.activateUUID:
            return
        suitId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        it, _, _ = p.inv.findItemByUUID(self.activateUUID)
        if it:
            consumeItemId = ESAD.data.get(self.activateItemId, [])[self.currentIndex].get('itemId')
            bindCount = p.inv.countItemBind(consumeItemId, enableParentCheck=True)
            if not it.isForeverBind() and bindCount:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ACTIVE_BIND, gameStrings.TEXT_EQUIPSUITPROXY_87)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.activiateSuit, suitId))
            else:
                self.activiateSuit(suitId)

    def activiateSuit(self, suitId):
        p = BigWorld.player()
        it, page, pos = p.inv.findItemByUUID(self.activateUUID)
        if it:
            ownSuitId = getattr(it, 'suitId', None)
            if ownSuitId and ownSuitId != suitId:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ALREADY_ACTIVE, gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_453)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onRealActivate, suitId))
            elif ownSuitId and ownSuitId == suitId:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SAME_SUITACTIVE, gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_456)
                p.showTopMsg(msg)
            else:
                self.cellActiveSuit(page, pos, suitId)

    def onRealActivate(self, suitId):
        p = BigWorld.player()
        it, page, pos = p.inv.findItemByUUID(self.activateUUID)
        if it:
            self.cellActiveSuit(page, pos, suitId)

    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.EQIP_SUIT_ACTIVATE)
    def cellActiveSuit(self, page, pos, suitId):
        p = BigWorld.player()
        p.cell.addSuitEffectToItem(page, pos, suitId)

    def _getKey(self, bar, slot):
        return 'equipSuit%d.slot%d' % (bar, slot)

    def onResetEquipSlot(self, *args):
        key = self._getKey(0, 0)
        self.updateEquipSlot(None, key)
        if self.activateMediator:
            self.activateMediator.Invoke('resetEquipSlot')

    def onSelectSuit(self, *args):
        self.currentIndex = int(args[3][0].GetNumber())
        self.currentSuitId = int(args[3][1].GetNumber())
        self.showEquipDetail(self.currentIndex, self.currentSuitId)

    def onCloseSuitActivate(self, *args):
        self.hide()

    def updateEquipSlot(self, it, key):
        if not it:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        else:
            itemInfo = uiUtils.getGfxItem(it, location=const.ITEM_IN_BAG)
            self.activateMediator.Invoke('setEquipSlot', uiUtils.dict2GfxDict(itemInfo))

    def setItem(self, nPage, nItem, destBar, destSlot, it):
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        self.activateItemId = it.id
        self.activateUUID = it.uuid
        self.updateEquipSlot(it, key)
        ret = self.getSuitTypeInfo(it)
        if self.activateMediator:
            self.activateMediator.Invoke('showEquipSuitType', uiUtils.array2GfxAarry(ret, True))

    def getSuitTypeInfo(self, it):
        ret = []
        data = ESAD.data.get(it.id, [])
        for suitIndex, item in enumerate(data):
            suitId = item.get('suitId')
            schoolShowLimit = item.get('schoolShowLimit', ())
            if BigWorld.player().school not in schoolShowLimit:
                continue
            suitData = ESD.data.get(suitId, {})
            icon = ESSD.data.get(suitId, {}).get('icon', '')
            suitName = suitData.items()[0][1].get('name', gameStrings.TEXT_EQUIPSUITPROXY_165)
            iconPath = EQUIPSUIT_ICON_PATH + str(icon) + '.dds'
            ret.append((suitIndex,
             suitId,
             suitName,
             iconPath))

        return ret

    def getSuitCostInfo(self, index, suitId):
        ret = {}
        p = BigWorld.player()
        suitActiveData = ESAD.data
        data = suitActiveData.get(self.activateItemId, [])[index]
        itemNum = 1
        itemId = data.get('itemId')
        cashNum = data.get('cash', 0)
        it = Item(itemId)
        needCount = itemNum
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        countStr = str(ownCount) + '/' + str(needCount)
        costInfo = uiUtils.getGfxItem(it, appendInfo={'count': countStr,
         'itemId': itemId})
        ret['costItem'] = costInfo
        ret['costCash'] = cashNum
        ret['ownCash'] = p.cash
        return ret

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def isItemDisabled(self, kind, page, pos, item):
        if not self.activateMediator:
            return False
        if not item.isEquip():
            return True
        if item.isWingOrRide():
            return True
        suitDatas = ESAD.data.get(item.id, [])
        if not suitDatas:
            return True
        fitSchool = False
        for data in suitDatas:
            schoolShowLimit = data.get('schoolShowLimit', ())
            if BigWorld.player().school in schoolShowLimit:
                fitSchool = True

        if not fitSchool:
            return True
        schReq = ID.data.get(item.id, {}).get('schReq', ())
        if schReq and BigWorld.player().school not in schReq:
            return True
        return False

    def showEquipDetail(self, index, suitId):
        ret = {}
        it, page, pos = BigWorld.player().inv.findItemByUUID(self.activateUUID)
        if not it:
            return
        else:
            mySuitId = getattr(it, 'suitId')
            if mySuitId:
                ret['currentInfo'] = self.getSuitPreviewInfo(it.suitId)
            else:
                ret['currentInfo'] = None
            ret['previewInfo'] = self.getSuitPreviewInfo(suitId)
            ret['costInfo'] = self.getSuitCostInfo(index, suitId)
            if self.activateMediator:
                self.activateMediator.Invoke('showEquipSuitDetail', uiUtils.dict2GfxDict(ret, True))
            return

    def getSuitPreviewInfo(self, mySuitId):
        suitDict = {}
        suitName = ''
        suitGetSkill = ''
        suitNotGetSkill = ''
        suitList = []
        suitData = ESD.data.get(mySuitId, {})
        suitShowData = ESSD.data.get(mySuitId, {})
        if len(suitData.items()) <= 0:
            return suitDict
        suits = suitShowData.get('posName', [])
        if len(suits) <= 0:
            return suitDict
        suitName = suitData.items()[0][1].get('name', '')
        p = BigWorld.player()
        if p:
            suitMaxNum = len(suits)
            suitCurNum = p.suitsCache.get(mySuitId, 0)
            suitName = gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_372 % (suitName, suitCurNum, suitMaxNum)
            for suit in suits:
                if len(suit) == 2:
                    part = gametypes.EQUIP_SUIT_PART.get(suit[0], 0)
                    equip = p.equipment.get(part)
                    if equip:
                        equipSuitId = getattr(equip, 'suitId')
                        if equipSuitId == mySuitId:
                            suitList.append((1, suit[1]))
                        else:
                            suitList.append((0, suit[1]))
                    else:
                        suitList.append((0, suit[1]))

            suitData = sorted(suitData.iteritems(), key=lambda x: x[0])
            for item in suitData:
                if item[0] == 'suits':
                    continue
                desc = '[%s]%s<br>' % (str(item[0]), item[1].get('desc', ''))
                if item[0] <= suitCurNum:
                    suitGetSkill += uiUtils.toHtml(desc, '#73E539')
                else:
                    suitNotGetSkill += uiUtils.toHtml(desc, '#808080')

        suitDict = {'suitName': suitName,
         'suitList': suitList,
         'suitGetSkill': suitGetSkill,
         'suitNotGetSkill': suitNotGetSkill}
        return suitDict
