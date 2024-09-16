#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingAndMountProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import gametypes
import const
import utils
import itemToolTipUtils
from helpers import charRes
from helpers import capturePhoto
from helpers import cellCmd
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from asObject import ASObject
from asObject import TipManager
from gameStrings import gameStrings
from uiProxy import SlotDataProxy
from data import sys_config_data as SCD
from data import item_data as ID
from data import equip_data as ED
from cdata import font_config_data as FCD
from data import qing_gong_skill_data as QGSD
from cdata import horsewing_talent_level_data as HTLD
from cdata import game_msg_def_data as GMDD
from guis import events
STATE_DURA_DECAY = 0
STATE_DURA_HOLD = 1
STATE_TAIL = 2
STATE_SPEED_SWITCH = 3
STATE_SPEED_SHARE = 4
TAB_RIDE = 0
TAB_WING = 1
TAB_QINGONG = 2

class WingAndMountProxy(SlotDataProxy):
    DEFAULT_EXPAND_SLOT = 200

    def __init__(self, uiAdapter):
        super(WingAndMountProxy, self).__init__(uiAdapter)
        self.modelMap = {'selectTab': self.onSelectTab,
         'selectPos': self.onSelectPos,
         'refreshPanel': self.refreshPanel,
         'zoomFigure': self.zoomFigure,
         'rotateFigure': self.rotateFigure,
         'getStateDesc': self.getStateDesc,
         'equipItem': self.equipItem,
         'upgradeItem': self.upgradeItem,
         'genEveTip': self.genEveTip,
         'eveItem': self.doEveItem,
         'refreshQingGongSkill': self.refreshQingGongSkill,
         'setRandom': self.onSetRandom}
        self.type = 'wingAndMount'
        self.bindType = 'wingAndMount'
        self.mediator = None
        self.isShow = False
        self.headGen = None
        self.item = None
        self.selectIdx = -1
        self.selectedPos = -1
        self.currentContainer = None
        self.maxNum = None
        self.currentShowItemList = []
        self.isFirstTime = True
        self.isChangeRandom = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_WIN_AND_MOUNT, self.clearWidget)
        self.addEvent(events.EVENT_VIP_INFO_UPDATE, self.refreshVipRoleInfo, isGlobal=True)

    def refreshVipRoleInfo(self):
        BigWorld.player().refreshWingShare()
        BigWorld.player().refreshRideShare()

    def genEveTip(self, *args):
        if self.selectIdx == 1:
            targetData = SCD.data.get('WingEveNavigatorTarget', '')
        else:
            targetData = SCD.data.get('RideEveNavigatorTarget', '')
        if len(targetData):
            name = uiUtils.findNearestNpcName(targetData)
            desc = gameStrings.TEXT_WINGANDMOUNTPROXY_89 % name
            return GfxValue(gbk2unicode(desc))
        return GfxValue('')

    def doEveItem(self, *args):
        if self.selectIdx == 1:
            targetData = SCD.data.get('WingEveNavigatorTarget', '')
        else:
            targetData = SCD.data.get('RideEveNavigatorTarget', '')
        if len(targetData):
            uiUtils.findPosById(targetData)

    def zoomFigure(self, *args):
        index = args[3][0].GetNumber()
        deltaZoom = -0.02 * index
        if self.headGen:
            self.headGen.zoom(deltaZoom)

    def rotateFigure(self, *args):
        index = args[3][0].GetNumber()
        deltaYaw = -0.02 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        if self.headGen:
            self.headGen.endCapture()
        self.headGen = None
        self.item = None
        self.currentContainer = None
        self.maxNum = None
        self.currentShowItemList = []
        self.selectIdx = -1
        self.selectedPos = -1
        self.isFirstTime = True
        p = BigWorld.player()
        if self.isChangeRandom:
            p.sendOperation()
        self.isChangeRandom = False
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WIN_AND_MOUNT)

    def show(self, idx = -1):
        p = BigWorld.player()
        result0 = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_RIDE)
        result1 = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_WING)
        result2 = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_QINGGONG)
        if not result0 and not result1 and not result2:
            return
        if idx == TAB_QINGONG and not result2:
            return
        if idx == TAB_RIDE and not result0:
            return
        if idx == TAB_WING and not result1:
            return
        if idx == -1:
            if result0 or result1 or result2:
                if result2:
                    idx = TAB_QINGONG
                if result0:
                    idx = TAB_RIDE
                if result1:
                    idx = TAB_WING
            else:
                p.showGameMsg(GMDD.data.EXCITEMENT_FORBIDDEN_FUNC, ())
                return
        if not self.isShow:
            self.isShow = True
            self.selectIdx = idx
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WIN_AND_MOUNT)
        else:
            self.selectTab(idx)
        BigWorld.player().refreshWingTemp()
        BigWorld.player().refreshRideTemp()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WIN_AND_MOUNT:
            self.mediator = mediator
            self.initHeadGen()
            self.refreshTabBtn()

    def refreshPanel(self, *args):
        self.selectTab(self.selectIdx)

    def toggle(self):
        if self.isShow == False:
            self.show()
        else:
            self.clearWidget()

    def onItemChange(self, params):
        if params[0] != const.RES_KIND_EQUIP and params[0] != const.RES_KIND_RIDE_WING_BAG:
            return
        if params[0] == const.RES_KIND_EQUIP:
            if params[2] == gametypes.EQU_PART_WINGFLY and self.selectIdx == 1 or params[2] == gametypes.EQU_PART_RIDE and self.selectIdx == 0:
                self.addItem(params[3], self.selectIdx, 0)
        elif params[1] == self.selectIdx:
            self.addItem(params[3], self.selectIdx, params[2] + 1)

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.WingAndMountPhotoGen.getInstance('gui/taskmask.tga', 300)
        self.headGen.initFlashMesh()

    def takePhoto3D(self, item):
        if self.item == None or item == None or self.item.id != item.id:
            self.item = item
            if not self.headGen:
                self.headGen = capturePhoto.WingAndMountPhotoGen.getInstance('gui/taskmask.tga', 300)
                self.headGen.initFlashMesh()
            self.realShowItemPhoto(item)
        else:
            self.item = item

    def realShowItemPhoto(self, item):
        if item.isWingOrRide():
            res, aspect, showFashion = self.getMpr(item)
            extraInfo = {'aspect': aspect,
             'showFashion': showFashion}
            self.headGen.startCaptureEntAndRes(BigWorld.player(), res, False, extraInfo, True)
            return

    def getMpr(self, wingItem):
        p = BigWorld.player()
        mpr = charRes.MultiPartRes()
        isShowFashion = p.isShowFashion()
        mpr.queryByAttribute(p.realPhysique, p.realAspect, isShowFashion, p.avatarConfig)
        res = mpr.getPrerequisites()
        return (res, p.realAspect, isShowFashion)

    def onSelectTab(self, *args):
        tabIdx = int(args[3][0].GetNumber())
        self.selectTab(tabIdx)

    def onSelectPos(self, *args):
        pos = int(args[3][0].GetNumber())
        if pos == self.DEFAULT_EXPAND_SLOT:
            p = BigWorld.player()
            gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_RIDE_WING_BAG_EXPAND, p.rideWingBag.getEnlargeSlotIndex(self.selectIdx), {'page': self.selectIdx})
        else:
            self.selectPos(pos)

    def selectPos(self, pos, refresh = False):
        if not self.mediator:
            return
        else:
            if self.selectedPos != pos or refresh:
                if self.mediator:
                    self.mediator.Invoke('selectPos', GfxValue(pos))
                self.selectedPos = pos
                selectedItem = self.currentShowItemList[pos]
                data = self.getItemShowData(selectedItem)
                if selectedItem:
                    data['showUpGrade'] = not selectedItem.canAutoUpgradeStage()
                    if selectedItem.rideWingStage == selectedItem.maxRideWingStage:
                        data['showUpGrade'] = False
                    data['canUpGrade'] = selectedItem.canRideWingUpgradeConsumeInv()
                    canConfirm = False
                    nowKey = gameglobal.rds.ui.wingAndMountUpgrade.searchEveKey(selectedItem)
                    if nowKey:
                        canConfirm = True
                    self.mediator.Invoke('setEveVisible', GfxValue(canConfirm))
                else:
                    data['canUpGrade'] = False
                    data['showUpGrade'] = False
                    self.mediator.Invoke('setEveVisible', GfxValue(False))
                self.mediator.Invoke('showItemDesc', uiUtils.dict2GfxDict(data, True))
                if selectedItem:
                    self.isFirstTime = False
                    gamelog.debug('jinjj---selectPos', selectedItem.id)
                    self.mediator.Invoke('setItemView', GfxValue(True))
                    self.takePhoto3D(selectedItem)
                else:
                    if self.isFirstTime == True:
                        res, aspect, showFashion = self.getMpr(None)
                        extraInfo = {'aspect': aspect,
                         'showFashion': showFashion}
                        self.mediator.Invoke('setItemView', GfxValue(False))
                        self.headGen.startCaptureEntAndRes(BigWorld.player(), res, False, extraInfo, True)
                    else:
                        self.item = None
                        self.headGen.initFlashMesh()
                        self.headGen.refresh()
                        self.headGen.adaptor.attachment = None
                        if hasattr(self.headGen.adaptor, 'clear'):
                            self.headGen.adaptor.clear()
                    self.isFirstTime = False
            return

    def selectTab(self, idx):
        if self.mediator:
            self.mediator.Invoke('selectTab', GfxValue(idx))
        self.selectedPos = -1
        if idx in xrange(0, 2):
            self.currentContainer = BigWorld.player().rideWingBag
            self.maxNum = BigWorld.player().rideWingBag.getPosCount(idx)
            self.refreshIsRandom(idx)
        else:
            self.currentContainer = None
        self.selectIdx = idx
        self.refreshAll()
        self.selectPos(0, True)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def refreshIsRandom(self, idx):
        p = BigWorld.player()
        if idx == 1:
            page = gameglobal.RANDOM_WING
        else:
            page = gameglobal.RANDOM_RIDE
        value = p.operation.get(gameglobal.WING_MOUNT_RANDOM_PlUS, {}).get(page, 0)
        isSelected = False
        if value:
            isSelected = True
        if self.mediator:
            self.mediator.Invoke('setIsRandom', (GfxValue(isSelected), GfxValue(idx)))

    def onSetRandom(self, *args):
        selected = args[3][0].GetBool()
        value = 0
        if selected:
            value = 1
        if self.selectIdx == 1:
            page = gameglobal.RANDOM_WING
        else:
            page = gameglobal.RANDOM_RIDE
        p = BigWorld.player()
        p.operation.setdefault(gameglobal.WING_MOUNT_RANDOM_PlUS, {})[page] = value
        self.isChangeRandom = True

    def refreshAll(self, reSelect = False):
        if not self.mediator:
            return
        if self.selectIdx == 0:
            self.refreshWingView()
        elif self.selectIdx == 1:
            self.refreshMountView()
        else:
            self.refreshCommonPart()
        if reSelect == True:
            self.selectPos(self.selectedPos, True)

    def refreshWingView(self):
        self.refreshCommonPart()

    def getFirstPartItem(self):
        if self.selectIdx not in xrange(0, 2):
            return None
        else:
            if self.selectIdx == 1:
                part = gametypes.EQU_PART_WINGFLY
            else:
                part = gametypes.EQU_PART_RIDE
            item = BigWorld.player().equipment[part]
            return item

    def refreshCommonPart(self):
        if self.selectIdx == 1:
            page = const.RIDE_WING_BAG_PAGE_WING
        else:
            page = const.RIDE_WING_BAG_PAGE_RIDE
        self.currentShowItemList = []
        firstItem = self.getFirstPartItem()
        self.currentShowItemList.append(firstItem)
        p = BigWorld.player()
        count = p.rideWingBag.getPosCount(page)
        for pos in xrange(0, count):
            if not self.currentContainer:
                self.currentContainer = p.rideWingBag
            if self.currentContainer:
                item = self.currentContainer.getQuickVal(page, pos)
                self.currentShowItemList.append(item)

        inputList = []
        for i in xrange(len(self.currentShowItemList)):
            item = self.currentShowItemList[i]
            data = self.getItemData(item, i)
            inputList.append(data)

        if p.rideWingBag.canEnlargeSlot(page):
            inputList.append([self.DEFAULT_EXPAND_SLOT, None, 'nothing'])
        if self.mediator:
            self.mediator.Invoke('refreshItemList', uiUtils.array2GfxAarry(inputList, True))

    def refreshMountView(self):
        self.refreshCommonPart()

    def getItemData(self, item, pos):
        if item != const.CONT_EMPTY_VAL:
            iconPath = uiUtils.getItemIconFile64(item.id)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            huger = item.getHungerDuraFactor()
            stateType = uiConst.ITEM_NORMAL
            if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
                stateType = uiConst.EQUIP_EXPIRE_TIME
            data = [pos,
             {'iconPath': iconPath},
             color,
             item.cdura,
             item.initMaxDura,
             huger[0] - 1,
             stateType]
        else:
            data = [pos, None, 'nothing']
        return data

    def addItem(self, item, page, pos):
        if page == self.selectIdx:
            data = self.getItemData(item, pos)
            self.currentShowItemList[pos] = item
            if self.mediator:
                self.mediator.Invoke('addItem', uiUtils.array2GfxAarry(data, True))
            if self.selectIdx == page and self.selectedPos == pos:
                self.selectPos(pos, True)
        for keys in self.binding:
            self.binding[keys][0].Invoke('refreshTip')

    def getItemShowData(self, item):
        data = {}
        if item:
            name = uiUtils.getItemColorName(item.id)
            data['name'] = name
            if isinstance(item.starExp, int):
                data['starExp'] = item.starExp
            else:
                data['starExp'] = float('%0.1f' % item.starExp)
            data['maxStarExp'] = item.getRideWingMaxUpgradeExp()
            data['desc'] = ID.data.get(item.id, {}).get('historyDesc', '')
            stageArray = SCD.data.get('rideWingStageText', {})
            data['stage'] = item.rideWingStage
            data['maxStage'] = item.maxRideWingStage
            data['availableTalents'] = item.availableTalents()
            data['talents'] = getattr(item, 'talents', [])
            data['talentsLv'] = HTLD.data.get(item.getParentId())
            data['stageText'] = stageArray[item.rideWingStage]
            stateList = [None,
             None,
             None,
             None,
             None]
            if item.isRideWingDuraDecayState() or item.isRideWingDuraHoldState():
                if item.isRideWingDuraDecayState():
                    iconId = SCD.data.get('RideWingDuraDecayStateIcon', 0)
                    iconPath = self.getStateIcon(iconId)
                    stateList[STATE_DURA_DECAY] = iconPath
                if item.isRideWingDuraHoldState():
                    iconId = SCD.data.get('RideWingDuraHoldStateIcon', 0)
                    iconPath = self.getStateIcon(iconId)
                    stateList[STATE_DURA_DECAY] = iconPath
            if item.isRideWingExpBoostState():
                iconId = SCD.data.get('RideWingExpBoostStateIcon', 0)
                iconPath = self.getStateIcon(iconId)
                stateList[STATE_DURA_HOLD] = iconPath
            if item.isRideWingTailEffectState():
                iconId = SCD.data.get('RideWingTailEffectStateIcon', 0)
                iconPath = self.getStateIcon(iconId)
                stateList[STATE_TAIL] = iconPath
            if item.isSwitchSpeedSubId():
                if item.isWingEquip():
                    iconId = SCD.data.get('wingTempSpeedContent', (None, None))[0]
                else:
                    iconId = SCD.data.get('rideTempSpeedContent', (None, None))[0]
                iconPath = self.getStateIcon(iconId)
                stateList[STATE_SPEED_SWITCH] = iconPath
            iconId = None
            if item.isWingEquip():
                if BigWorld.player().hasSharedWingMaxSpeed():
                    iconId = SCD.data.get('wingShareSpeedContent', (None, None))[0]
            elif BigWorld.player().hasSharedRideMaxSpeed():
                iconId = SCD.data.get('rideShareSpeedContent', (None, None))[0]
            if iconId:
                iconPath = self.getStateIcon(iconId)
                stateList[STATE_SPEED_SHARE] = iconPath
            data['stateList'] = stateList
            gamelog.debug('jinjj---data[stateList]-', data['stateList'])
        return data

    def getStateIcon(self, iconID):
        return uiConst.ITEM_ICON_IMAGE_RES_64 + str(iconID) + '.dds'

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if self.currentShowItemList[pos]:
            return gameglobal.rds.ui.inventory.GfxToolTip(self.currentShowItemList[pos])
        else:
            return GfxValue('')

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[12:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'wingAndMount%d.slot%d' % (bar, slot)

    def getStateDesc(self, *args):
        stateId = int(args[3][0].GetNumber())
        desc = ''
        selectedItem = self.currentShowItemList[self.selectedPos]
        if not selectedItem:
            return desc
        else:
            if stateId == STATE_DURA_DECAY:
                if selectedItem:
                    if selectedItem.isRideWingDuraDecayState() or selectedItem.isRideWingDuraHoldState():
                        if selectedItem.isRideWingDuraDecayState():
                            factor = selectedItem.rideWingDuraDecayFactor()
                            result = factor * 100
                            et = selectedItem.rideWingStates['cduraDecayExpireTime']
                            leftTime = et - BigWorld.player().getServerTime()
                            timeText = utils.formatDurationShortVersion(leftTime)
                            desc = gameStrings.TEXT_WINGANDMOUNTPROXY_561 % (result, timeText)
                        else:
                            et = selectedItem.rideWingStates['cduraHoldExpireTime']
                            leftTime = et - BigWorld.player().getServerTime()
                            timeText = utils.formatDurationShortVersion(leftTime)
                            desc = gameStrings.TEXT_WINGANDMOUNTPROXY_566 % timeText
            elif stateId == STATE_DURA_HOLD:
                if selectedItem.isRideWingExpBoostState():
                    factor = selectedItem.rideWingExpBoostFactor()
                    result = factor * 100
                    et = selectedItem.rideWingStates['expBoostExpireTime']
                    leftTime = et - BigWorld.player().getServerTime()
                    timeText = utils.formatDurationShortVersion(leftTime)
                    desc = gameStrings.TEXT_WINGANDMOUNTPROXY_575 % (result, timeText)
            elif stateId == STATE_TAIL:
                if selectedItem.isRideWingTailEffectState():
                    et = selectedItem.rideWingStates['flyTailEffectExpireTime']
                    leftTime = et - BigWorld.player().getServerTime()
                    timeText = utils.formatDurationShortVersion(leftTime)
                    desc = gameStrings.TEXT_WINGANDMOUNTPROXY_582 % timeText
            elif stateId == STATE_SPEED_SWITCH:
                if selectedItem.isSwitchSpeedSubId():
                    itemType = 2
                    canFly = False
                    if selectedItem.isRideEquip():
                        itemType = 1
                        canFly = ED.data.get(selectedItem.id, {}).get('flyRide', 0)
                        desc = SCD.data.get('rideTempSpeedContent', (None, None))[1]
                    else:
                        itemType = 2
                        canFly = True
                        desc = SCD.data.get('wingTempSpeedContent', (None, None))[1]
                    switchNonCombatSpeedSubId = getattr(selectedItem, 'switchNonCombatSpeedSubId', None)
                    speedSwitchExpireTime = getattr(selectedItem, 'speedSwitchExpireTime', None)
                    leftTime = speedSwitchExpireTime - BigWorld.player().getServerTime()
                    timeText = utils.formatDurationShortVersion(leftTime)
                    if switchNonCombatSpeedSubId:
                        content = itemToolTipUtils.getSpeedContent(BigWorld.player(), switchNonCombatSpeedSubId, canFly, itemType, selectedItem.isSwimRide())
                        desc += ':'
                        for contentSub in content:
                            desc += '\n'
                            desc += contentSub

                    desc += gameStrings.TEXT_WINGANDMOUNTPROXY_606 % timeText
                else:
                    desc = ''
            elif stateId == STATE_SPEED_SHARE:
                desc = ''
                if selectedItem.isRideEquip():
                    nowNoCombatSpeedId = BigWorld.player().getCompoundRideSpeedSubId()
                    descTitle = SCD.data.get('rideShareSpeedContent', (None, None))[1]
                    hasTime = getattr(BigWorld.player(), 'rideShareSpeedExpireTime', None)
                    vipLeftTime = BigWorld.player().getVipPropLeftTime(gametypes.VIP_SERVICE_SHARE_RIDE_SPEED)
                else:
                    nowNoCombatSpeedId = BigWorld.player().getCompoundWingSpeedSubId()
                    descTitle = SCD.data.get('wingShareSpeedContent', (None, None))[1]
                    hasTime = getattr(BigWorld.player(), 'wingShareSpeedExpireTime', None)
                    vipLeftTime = BigWorld.player().getVipPropLeftTime(gametypes.VIP_SERVICE_SHARE_WING_SPEED)
                leftTime = hasTime - BigWorld.player().getServerTime()
                if vipLeftTime > leftTime:
                    leftTime = vipLeftTime
                timeText = utils.formatDurationShortVersion(leftTime)
                nowShareItem = None
                for i in xrange(len(self.currentShowItemList)):
                    item = self.currentShowItemList[i]
                    if item:
                        if item.getRideWingSpeedId() == nowNoCombatSpeedId and not item.isSwimRide():
                            if item.isExpireTTL():
                                continue
                            nowShareItem = item
                            break

                if nowShareItem:
                    desc = descTitle % uiUtils.getItemColorName(nowShareItem.id)
                desc += gameStrings.TEXT_WINGANDMOUNTPROXY_606 % timeText
            else:
                desc = ''
            return GfxValue(gbk2unicode(desc))

    def equipItem(self, *args):
        if self.selectedPos > 0:
            if self.selectIdx == 0:
                type = gametypes.EQU_PART_RIDE
            elif self.selectIdx == 1:
                type = gametypes.EQU_PART_WINGFLY
            cellCmd.equipRideWingBag(self.selectIdx, self.selectedPos - 1, type)

    def upgradeItem(self, *args):
        gamelog.debug('jinjj-----upgradeItem--')
        if self.selectedPos == 0:
            res = const.RES_KIND_EQUIP
            if self.selectIdx == 0:
                type = gametypes.EQU_PART_RIDE
                gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.RIDE_UPGRADE, res, 0, type)
            elif self.selectIdx == 1:
                type = gametypes.EQU_PART_WINGFLY
                gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.WING_UPGRADE, res, 0, type)
        else:
            res = const.RES_KIND_RIDE_WING_BAG
            if self.selectIdx == 0:
                gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.RIDE_UPGRADE, res, self.selectIdx, self.selectedPos - 1)
            else:
                gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.WING_UPGRADE, res, self.selectIdx, self.selectedPos - 1)

    def searchEmptyPos(self):
        for i in xrange(0, len(self.currentShowItemList)):
            if self.currentShowItemList[i] == None:
                return i

        return 0

    def moveItemFromBagIntoMine(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if not i:
            return
        if nPageDes == const.RIDE_WING_BAG_PAGE_RIDE:
            if i.isRideEquip():
                if nItemDes == 0:
                    p.useBagItem(nPageSrc, nItemSrc)
                else:
                    p.base.inv2rideWingBag(nPageSrc, nItemSrc, 1, nPageDes, nItemDes - 1)
        elif nPageDes == const.RIDE_WING_BAG_PAGE_WING:
            if i.isWingEquip():
                if nItemDes == 0:
                    p.useBagItem(nPageSrc, nItemSrc)
                else:
                    p.base.inv2rideWingBag(nPageSrc, nItemSrc, 1, nPageDes, nItemDes - 1)

    def onNotifySlotUse(self, *args):
        nPage, nItem = self.getSlotID(args[3][0].GetString())
        self.moveItemToBag(nPage, nItem)

    def moveItemToBag(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        nPageDes, nItemDes = p.inv.searchEmptyInPages()
        if nPageDes == const.CONT_NO_PAGE:
            p.showGameMsg(GMDD.data.BAG_FULL, ())
            return
        if nItemSrc == 0:
            if nPageSrc == 0 or nPageSrc == 1:
                if nPageSrc == 0:
                    type = gametypes.EQU_PART_RIDE
                else:
                    type = gametypes.EQU_PART_WINGFLY
                cellCmd.exchangeInvEqu(nPageDes, nItemDes, type)
        else:
            BigWorld.player().cell.rideWingBag2inv(nPageSrc, nItemSrc - 1, 1, nPageDes, nItemDes)

    def refreshQingGongSkill(self, *args):
        p = BigWorld.player()
        ret = {'ride': [],
         'qinggong': [],
         'wing': []}
        for key, value in QGSD.data.items():
            order = value.get('order', (-1, -1))
            if value['skillId'] == uiConst.QINGGONG_FLAG_BASIC:
                learned = True
                lv = 1
                icon = value.get('icon', 0)
            else:
                learned = p.qingGongSkills.has_key(key[0])
                if learned:
                    lv = p.qingGongSkills[key[0]].level
                    icon = QGSD.data.get((key[0], lv), {}).get('icon', 0)
                else:
                    lv = ''
                    icon = value.get('icon', 0)
            if icon:
                iconPath = 'misc/%d.dds' % icon
            else:
                iconPath = 'misc/notFound.dds'
            btnEnabled = QGSD.data.get((key[0], lv), {}).has_key('detailChangeDesc')
            if order[0] == uiConst.QINGGONG_TYPE_RIDE and value['lv'] == 1:
                ret['ride'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})
            elif order[0] == uiConst.QINGGONG_TYPE_QINGGONG and value['lv'] == 1:
                ret['qinggong'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})
            elif order[0] == uiConst.QINGGONG_TYPE_WING and value['lv'] == 1:
                ret['wing'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})

        for value in ret.values():
            value.sort(key=lambda k: k['order'])

        if self.mediator:
            self.mediator.Invoke('setQingGongContent', uiUtils.dict2GfxDict(ret, True))

    def refreshTabBtn(self):
        if self.mediator:
            sWidget = ASObject(self.mediator.Invoke('getWidget'))
            if sWidget:
                self.dealTabBtn(sWidget.tab0, gametypes.EXCITEMENT_FEATURE_RIDE)
                self.dealTabBtn(sWidget.tab1, gametypes.EXCITEMENT_FEATURE_WING)
                self.dealTabBtn(sWidget.tab2, gametypes.EXCITEMENT_FEATURE_QINGGONG)

    def dealTabBtn(self, mc, ctype):
        p = BigWorld.player()
        _enabled = p.checkExcitementFeature(ctype)
        mc.enabled = _enabled
        mc.mouseEnabled = True
        if not _enabled:
            TipManager.addTip(mc, gameStrings.EXCITEMENT_FORBIDDEN_TIPS)
        else:
            TipManager.removeTip(mc)
