#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingAndMountUpgradeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import utils
import itemToolTipUtils
from helpers import charRes
from helpers import capturePhoto
from item import Item
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from data import equip_data as ED
from data import sys_config_data as SCD
from data import equip_synthesize_data as ESD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import horsewing_upgrade_data as HUD
from cdata import item_synthesize_set_data as ISSD
from cdata import horsewing_talent_data as HTD
from cdata import horsewing_manual_upgrade_data as HWMUD

class WingAndMountUpgradeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(WingAndMountUpgradeProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshPanel': self.refreshPanel,
         'confirm': self.onConfirm,
         'cancel': self.closeWidget,
         'showPreView': self.showPreView,
         'zoomFigure': self.zoomFigure,
         'rotateFigure': self.rotateFigure}
        self.type = 'WAMUpGrade'
        self.bindType = 'WAMUpGrade'
        self.mediator = None
        self.isShow = False
        self.headGen = None
        self.funcType = uiConst.WING_UPGRADE
        self.preViewItem = None
        self.isShowPre = False
        self.npcID = -1
        self.targetRes = [const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS]
        self.materialEnough = False
        self.eveMap = {}
        self.item = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE, self.clearWidget)

    def onConfirm(self, *args):
        if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
            if self.targetRes[0] == const.RES_KIND_EQUIP:
                BigWorld.player().cell.upgradeRideWingEquip(self.targetRes[2])
            else:
                BigWorld.player().base.upgradeRideWingEquip(self.targetRes[1], self.targetRes[2])
            self.clearWidget()
        else:
            item = self.getCurrentDealItem(self.targetRes)
            nowKey = self.searchEveKey(item)
            npcEnt = BigWorld.entities.get(self.npcID)
            if npcEnt:
                npcEnt.cell.upgradeEquipItem(self.targetRes[1], self.targetRes[2], nowKey[0], nowKey[1])
            self.clearWidget()

    def showPreView(self, *args):
        self.isShowPre = args[3][0].GetBool()
        if self.isShowPre:
            self.takePhoto3D(self.preViewItem)

    def zoomFigure(self, *args):
        if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
            return
        index = args[3][0].GetNumber()
        deltaZoom = -0.02 * index
        if self.headGen:
            self.headGen.zoom(deltaZoom)

    def rotateFigure(self, *args):
        if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
            return
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
        self.preViewItem = None
        self.isShowPre = False
        self.npcID = -1
        self.targetRes = [const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS]
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        self.bindingData = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def show(self, funcType = uiConst.WING_UPGRADE, itemResKind = const.RES_KIND_INV, itemResPage = const.CONT_NO_PAGE, itemResPos = const.CONT_NO_POS, npcID = -1):
        self.isShow = True
        self.funcType = funcType
        self.npcID = npcID
        self.targetRes = [itemResKind, itemResPage, itemResPos]
        if self.mediator:
            self.refreshPanel(None)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE:
            self.mediator = mediator
            if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
                self.initHeadGen()
                self.uiAdapter.tdHeadGen.startCapture()
                BigWorld.callback(0.5, lambda : self.mediator.Invoke('setPreViewPanelVisible', GfxValue(True)))
            else:
                self.initHeadGen()

    def toggle(self):
        if self.isShow == False:
            self.show()
        else:
            self.clearWidget()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.WingAndMountUpgradePhotoGen.getInstance('gui/taskmask.tga', 408)
        self.headGen.initFlashMesh()
        res, aspect, showFashion = self.getMpr(None)
        self.headGen.startCaptureEntAndRes(BigWorld.player(), res, False, {}, False, True)

    def takePhoto3D(self, item):
        self.item = item
        if not self.headGen:
            self.headGen = capturePhoto.WingAndMountUpgradePhotoGen.getInstance('gui/taskmask.tga', 408)
            self.headGen.initFlashMesh()
        self.realShowItemPhoto(item)

    def realShowItemPhoto(self, item):
        if not item:
            self.headGen.initFlashMesh()
            self.headGen.refresh()
            self.headGen.adaptor.attachment = None
            if hasattr(self.headGen.adaptor, 'clear'):
                self.headGen.adaptor.clear()
            return
        elif item.isWingOrRide():
            res, aspect, showFashion = self.getMpr(item)
            extraInfo = {'aspect': aspect,
             'showFashion': showFashion}
            self.headGen.startCaptureEntAndRes(BigWorld.player(), res, False, extraInfo, False, True)
            return
        else:
            return

    def getMpr(self, wingItem):
        p = BigWorld.player()
        mpr = charRes.MultiPartRes()
        isShowFashion = p.isShowFashion()
        mpr.queryByAttribute(p.realPhysique, p.realAspect, isShowFashion, p.avatarConfig)
        res = mpr.getPrerequisites()
        return (res, p.realAspect, isShowFashion)

    def refreshPanel(self, *args):
        gamelog.debug('jinjj--refreshPanel-wma')
        self.mediator.Invoke('setFuncType', GfxValue(self.funcType))
        self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))
        self.mediator.Invoke('setPreviewButton', GfxValue(False))
        item = self.getCurrentDealItem(self.targetRes)
        self.setDealItemShow(item)

    def refreshHint(self):
        if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
            if self.materialEnough == True:
                hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_201
            else:
                hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_203
        else:
            item = self.getCurrentDealItem(self.targetRes)
            if not item:
                if self.funcType == uiConst.WING_EVE:
                    hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_208
                else:
                    hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_210
            else:
                nowKey = self.searchEveKey(item)
                if nowKey:
                    info = ESD.data[nowKey]
                    if info.has_key('stageRequire'):
                        stageArray = SCD.data.get('rideWingStageText', {})
                        if getattr(item, 'rideWingStage', 0) < info.get('stageRequire'):
                            hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_219 % stageArray[info['stageRequire']]
                            self.mediator.Invoke('setHint', GfxValue(gbk2unicode(hint)))
                            return
                        if info.get('maxExpRequire', 0) and item.starExp < item.getRideWingMaxUpgradeExp():
                            hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_223
                            self.mediator.Invoke('setHint', GfxValue(gbk2unicode(hint)))
                            return
                        if self.materialEnough == False:
                            hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_227
                        else:
                            hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_229
                else:
                    hint = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_231
        self.mediator.Invoke('setHint', GfxValue(gbk2unicode(hint)))

    def getCurrentDealItem(self, targetRes):
        gamelog.debug('jinjj--getCurrentDealItem', targetRes)
        if targetRes[1] != const.CONT_NO_PAGE:
            p = BigWorld.player()
            if targetRes[0] == const.RES_KIND_INV:
                return p.inv.getQuickVal(targetRes[1], targetRes[2])
            elif targetRes[0] == const.RES_KIND_EQUIP:
                return p.equipment[targetRes[2]]
            elif targetRes[0] == const.RES_KIND_RIDE_WING_BAG:
                return p.rideWingBag.getQuickVal(targetRes[1], targetRes[2])
            else:
                return None
        else:
            return None

    def setItem(self, itemResKind = const.RES_KIND_INV, itemResPage = const.CONT_NO_PAGE, itemResPos = const.CONT_NO_POS):
        item = self.getCurrentDealItem([itemResKind, itemResPage, itemResPos])
        gamelog.debug('jinjj --setitem', item)
        if item:
            isItemRight = False
            if self.funcType == uiConst.WING_EVE or self.funcType == uiConst.WING_UPGRADE:
                if item.isWingEquip():
                    isItemRight = True
            elif item.isRideEquip():
                isItemRight = True
            if isItemRight:
                self.targetRes = [itemResKind, itemResPage, itemResPos]
                self.setDealItemShow(item)
            if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                self.mediator.Invoke('setPreviewButton', GfxValue(False))
                self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))
            else:
                self.mediator.Invoke('setPreviewButton', GfxValue(True))
                self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))
        else:
            self.targetRes = [0, -1, -1]
            self.setDealItemShow(None)
            self.mediator.Invoke('setPreviewButton', GfxValue(False))
            self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))

    def setItemInSlot(self, item, key):
        self.bindingData[key] = item
        iconPath = uiUtils.getItemIconFile64(item.id)
        data = {'iconPath': iconPath}
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        self.binding[key][0].Invoke('setSlotColor', GfxValue(color))

    def setDealItemShow(self, item):
        self.clearItem()
        self.materialEnough = False
        if item:
            key = self._getKey(0, 0)
            self.setItemInSlot(item, key)
            if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                self.mediator.Invoke('setPreviewButton', GfxValue(False))
                self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))
            else:
                self.mediator.Invoke('setPreviewButton', GfxValue(True))
                self.mediator.Invoke('setPreViewPanelVisible', GfxValue(False))
            upgradeInfo = self.getItemAllInfo(item)
            gamelog.debug('jinjj-upgradeInfo----', upgradeInfo)
            materialInfo = upgradeInfo.get('material', [])
            gamelog.debug('jinjj-materialInfo----', materialInfo)
            self.materialEnough = True
            if materialInfo:
                for i in xrange(0, len(materialInfo)):
                    itemId = materialInfo[i][0]
                    needNum = materialInfo[i][1]
                    materialItem = Item(itemId)
                    hadNum = BigWorld.player().inv.countItemInPages(materialItem.getParentId(), enableParentCheck=True)
                    result = BigWorld.player().inv.countItemChild(materialItem.getParentId())
                    if result[0] > 0:
                        materialItem = Item(result[1][0])
                    else:
                        materialItem = Item(materialItem.getParentId())
                    nowKey = self._getKey(0, i + 1)
                    self.setItemInSlot(materialItem, nowKey)
                    if hadNum < needNum:
                        self.materialEnough = False
                    if hadNum >= needNum:
                        numStr = '%d/%d' % (hadNum, needNum)
                    else:
                        numStr = "<font color=\'#FB0000\'>%d/%d</font>" % (hadNum, needNum)
                    self.mediator.Invoke('setSlotNum', (GfxValue(i), GfxValue(gbk2unicode(numStr))))

            content = []
            content.append(upgradeInfo.get('fromContent', []))
            content.append(upgradeInfo.get('toContent', []))
            canConfirm = False
            if self.materialEnough:
                if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                    canConfirm = item.canRideWingUpgradeConsumeInv()
                else:
                    nowKey = self.searchEveKey(item)
                    if nowKey:
                        info = ESD.data[nowKey]
                        canConfirm = utils.lvUpRideWingFilter(item, info)
            if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                label = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_348
            else:
                label = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_350
                fromName = upgradeInfo['fromName']
                toName = upgradeInfo['toName']
                self.mediator.Invoke('setItemTitle', (GfxValue(gbk2unicode(fromName)), GfxValue(gbk2unicode(toName))))
            self.mediator.Invoke('setConfirmEnable', (GfxValue(canConfirm), GfxValue(gbk2unicode(label))))
            writeList = []
            for i in xrange(2):
                writeText = ''
                for c in content[i]:
                    if writeText != '':
                        writeText += '\n'
                    writeText += c

                talentText = [const.RIDE_WING_TALENT_MULTI_TEXT,
                 const.RIDE_WING_TALENT_SWIM_TEXT,
                 const.RIDE_WING_TALENT_FLY_TEXT,
                 const.RIDE_WING_TALENT_DRAGTAIL_TEXT,
                 const.RIDE_WING_TALENT_MULTI_FLY_TEXT,
                 const.RIDE_TALENT_SHARE_TEXT]
                talent = upgradeInfo.get('talent', [None, None])
                if talent[i]:
                    if writeText != '':
                        writeText += '\n'
                    writeText += gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_369
                    if i == 0:
                        otherTalent = talent[1]
                    else:
                        otherTalent = talent[0]
                    for t in talent[i]:
                        if t not in otherTalent:
                            if i == 0:
                                writeText += "<font color =\'#FB0000\'>" + talentText[t - 1] + '</font>'
                            else:
                                writeText += "<font color =\'#79C725\'>" + talentText[t - 1] + '</font>'
                        else:
                            writeText += talentText[t - 1]
                        writeText += ' '

                writeList.append(writeText)

            self.mediator.Invoke('setContent', (GfxValue(gbk2unicode(writeList[0])), GfxValue(gbk2unicode(writeList[1]))))
        self.refreshHint()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearItem(self):
        key = self._getKey(0, 0)
        self.bindingData = {}
        self.bindingData[key] = None
        data = GfxValue(0)
        data.SetNull()
        self.binding[key][1].InvokeSelf(data)
        self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
        self.materialEnough = False
        mNum = 2
        if self.funcType != uiConst.WING_UPGRADE and self.funcType != uiConst.RIDE_UPGRADE:
            mNum = 3
        for i in xrange(0, mNum):
            mKey = self._getKey(0, i)
            self.bindingData[mKey] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[mKey][1].InvokeSelf(data)
            self.binding[mKey][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.mediator.Invoke('setSlotNum', (GfxValue(i), GfxValue(gbk2unicode(''))))

        self.mediator.Invoke('setContent', (GfxValue(gbk2unicode('')), GfxValue(gbk2unicode(''))))
        if self.funcType != uiConst.WING_UPGRADE and self.funcType != uiConst.RIDE_UPGRADE:
            self.mediator.Invoke('setItemTitle', (GfxValue(gbk2unicode('')), GfxValue(gbk2unicode(''))))
        if self.funcType == uiConst.WING_UPGRADE:
            label = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_415
        else:
            label = gameStrings.TEXT_WINGANDMOUNTUPGRADEPROXY_350
        self.mediator.Invoke('setPreviewButton', GfxValue(False))
        self.mediator.Invoke('setConfirmEnable', (GfxValue(False), GfxValue(gbk2unicode(label))))

    def getItemAllInfo(self, item):
        if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
            return self.getItemUpgradeInfo(item)
        else:
            return self.getItemEveInfo(item)

    def searchEveKey(self, item):
        if not self.eveMap:
            for key in ESD.data:
                itemNeed = ESD.data[key].get('materialNeed', ())
                itemNeedId = itemNeed[0][1]
                self.eveMap[Item(itemNeedId).getParentId()] = key

        return self.eveMap.get(item.getParentId(), None)

    def getItemEveInfo(self, item):
        infoData = {}
        nowKey = self.searchEveKey(item)
        p = BigWorld.player()
        if nowKey:
            info = ESD.data[nowKey]
            materialSet = info.get('materialSetNeed', 0)
            material = self.getMaterial(materialSet)
            infoData['material'] = material
            stage = item.rideWingStage
            eveItemId = nowKey[0]
            infoData['fromName'] = uiUtils.getItemColorName(item.id)
            infoData['toName'] = uiUtils.getItemColorName(eveItemId)
            self.preViewItem = Item(eveItemId)
            gamelog.debug('jinjj----self.isShowPre-------', self.isShowPre)
            if self.isShowPre:
                self.takePhoto3D(self.preViewItem)
            eveStage = ED.data.get(item.id, {}).get('initStage', 0)
            fromContent = itemToolTipUtils.getRideWingItemContent(p, item.id, stage)
            toContent = itemToolTipUtils.getRideWingItemContent(p, eveItemId, eveStage)
            for i in xrange(len(toContent)):
                if toContent[i] not in fromContent:
                    toContent[i] = "<font color=\'#79C725\'>" + toContent[i] + '</font>'

            infoData['fromContent'] = fromContent
            infoData['toContent'] = toContent
            currentTalent = HTD.data.get((item.id, stage), {}).get('talents', ())
            updateTalent = HTD.data.get((eveItemId, eveStage), {}).get('talents', ())
            talent = [currentTalent, updateTalent]
            infoData['talent'] = talent
        return infoData

    def _getRideWingUpgradeMaterialSet(self, itemId, quality, vehicleType, stage):
        setNeed = HWMUD.data.get((itemId, stage), {}).get('materialSet', 0)
        if not setNeed:
            setNeed = HUD.data.get((quality, vehicleType, stage), {}).get('materialSet', 0)
        return setNeed

    def getItemUpgradeInfo(self, item):
        infoData = {}
        p = BigWorld.player()
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        stage = item.rideWingStage
        if self.funcType == uiConst.WING_UPGRADE:
            type = 2
        else:
            type = 1
        hudKey2 = (quality, type, stage + 1)
        upgradeInfo = HUD.data.get(hudKey2, {})
        if not upgradeInfo:
            return infoData
        fromContent = itemToolTipUtils.getRideWingItemContent(p, item.id, stage)
        toContent = itemToolTipUtils.getRideWingItemContent(p, item.id, stage + 1)
        for i in xrange(len(toContent)):
            if toContent[i] not in fromContent:
                toContent[i] = "<font color=\'#79C725\'>" + toContent[i] + '</font>'

        infoData['fromContent'] = fromContent
        infoData['toContent'] = toContent
        setNeed = self._getRideWingUpgradeMaterialSet(item.id, quality, type, stage)
        material = self.getMaterial(setNeed)
        infoData['material'] = material
        currentTalent = HTD.data.get((item.id, stage), {}).get('talents', ())
        updateTalent = HTD.data.get((item.id, stage + 1), {}).get('talents', ())
        talent = [currentTalent, updateTalent]
        infoData['talent'] = talent
        return infoData

    def getMaterial(self, materialSetID):
        sd = ISSD.data.get(materialSetID, None)
        material = []
        if sd != None:
            for d in sd:
                itemId = d.get('itemId', 0)
                if itemId == 0:
                    continue
                numRange = d.get('numRange', (0, 0))
                needNum = numRange[1]
                material.append((itemId, needNum))

        return material

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[10:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'WAMUpGrade%d.slot%d' % (bar, slot)

    def onGetToolTip(self, *arg):
        gamelog.debug('jinjj--onGetToolTip-')
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onNotifySlotUse(self, *args):
        nPage, nItem = self.getSlotID(args[3][0].GetString())
        if nPage == 0 and nItem == 0 and self.funcType != uiConst.WING_UPGRADE and self.funcType != uiConst.RIDE_UPGRADE:
            gameglobal.rds.ui.wingAndMountUpgrade.setItem(const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS)

    def checkItemCanUse(self, item):
        canConfirm = False
        if item.isWingOrRide():
            if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                canConfirm = item.canRideWingUpgradeConsumeInv()
            else:
                nowKey = self.searchEveKey(item)
                if nowKey:
                    info = ESD.data[nowKey]
                    canConfirm = utils.lvUpRideWingFilter(item, info)
        return canConfirm

    def checkItemCanDrag(self, item):
        canConfirm = False
        if item.isWingOrRide():
            if self.funcType == uiConst.WING_UPGRADE or self.funcType == uiConst.RIDE_UPGRADE:
                canConfirm = False
            elif item.isWingEquip() and self.funcType == uiConst.WING_EVE or item.isRideEquip() and self.funcType == uiConst.RIDE_EVE:
                nowKey = self.searchEveKey(item)
                if nowKey:
                    canConfirm = True
        return canConfirm

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if not self.checkItemCanDrag(item):
                return True
            if self.targetRes[0] == const.RES_KIND_INV:
                if self.targetRes[1] == page and self.targetRes[2] == pos:
                    return True
        return False
