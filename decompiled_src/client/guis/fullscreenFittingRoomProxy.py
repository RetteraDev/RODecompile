#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fullscreenFittingRoomProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import tianyuMallProxy
from item import Item
import clientUtils
import utils
from Scaleform import GfxValue
from uiProxy import UIProxy
from ui import gbk2unicode
from data import bonus_set_data as BSD
from data import consumable_item_data as CID
from data import mall_config_data as MCFD
from data import mall_category_data as MCD
EQU_PART_RIDE_OR_WINGFLY = 1314
DEF_MALL_TAB_MAIN = 1
DEF_MALL_TAB_SUB = 1101

class FullscreenFittingRoomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FullscreenFittingRoomProxy, self).__init__(uiAdapter)
        self.modelMap = {'getAllTabsInfo': self.onGetAllTabsInfo,
         'getMallItemList': self.onGetMallItemList,
         'setPreviewInfo': self.onSetPreviewInfo,
         'cancelPreviewInfo': self.onCancelPreviewInfo,
         'cancelPartPreviewInfo': self.onCancelPartPreviewInfo,
         'openInventory': self.onOpenInventory,
         'searchFittingRoom': self.onSearchFittingRoom,
         'showBuyConfirm': self.onShowBuyConfirm,
         'closeBuyConfirm': self.onCloseBuyConfirm,
         'buyAllPreviewItems': self.onBuyAllPreviewItems,
         'changeColor': self.onChangeColor,
         'getColor': self.onGetColor,
         'reSetFigure': self.onReSetFigure,
         'updateFigure': self.onUpdateFigure,
         'getFashionDesc': self.onGetFashionDesc,
         'isEditModeOn': self.onIsEditModeOn,
         'openEditMode': self.onOpenEditMode,
         'saveCameraAndYaw': self.onSaveCameraAndYaw}
        self.mediator = None
        self.buyConfirmMediator = None
        self.fittingRoomWidgetId = uiConst.WIDGET_FULLSCREEN_FITTINGROOM
        self.buyConfirmWidgetId = uiConst.WIDGET_FULLSCREEN_FITTINGBUY
        uiAdapter.registerEscFunc(self.fittingRoomWidgetId, self.hide)
        uiAdapter.registerEscFunc(self.buyConfirmWidgetId, self.onCloseBuyConfirm)
        self.reset()

    @property
    def mallProxy(self):
        return gameglobal.rds.ui.tianyuMall

    def _registerMediator(self, widgetId, mediator):
        ret = {}
        if widgetId == self.fittingRoomWidgetId:
            self.mediator = mediator
            self.mallProxy.tabMgr.initTabs()
            ret['bagOpen'] = bool(gameglobal.rds.ui.inventory.mediator)
            return uiUtils.dict2GfxDict(ret, True)
        if widgetId == self.buyConfirmWidgetId:
            self.buyConfirmMediator = mediator
            self.genBuyConfirmItemInfo()
            ret['itemList'] = self.buyConfirmInfo
            ret['moneyInfo'] = self.mallProxy.getMyMoneyInfo()
            return uiUtils.dict2GfxDict(ret, True)

    def show(self):
        if not self.showFullscreenFittingRoomConfig():
            return
        try:
            self.mallTabInfo[0] = self.mallProxy.tabMgr.selChildId
            self.mallTabInfo[1] = self.mallProxy.tabMgr.getSelChild().selChildId
        except:
            self.mallTabInfo[0] = DEF_MALL_TAB_MAIN
            self.mallTabInfo[1] = DEF_MALL_TAB_SUB

        gameglobal.rds.ui.fittingRoom.enterFullScreenFitting(self.afterModelFinished)

    def onShowBuyConfirm(self, *arg):
        if not self.showFullscreenFittingRoomConfig():
            return
        gameglobal.rds.ui.loadWidget(self.buyConfirmWidgetId, True)

    def onCloseBuyConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.buyConfirmWidgetId)
        self.buyConfirmMediator = None
        self.buyConfirmInfo = []
        self.confirmBuyMallIds = []
        gameglobal.rds.ui.tianyuMall.confirmBuyType = ''

    @ui.uiEvent(uiConst.WIDGET_FULLSCREEN_FITTINGROOM, (events.EVENT_INVENTORY_CLOSE, events.EVENT_INVENTORY_OPEN))
    def onBagOpenStateChanged(self, event = None):
        if not event:
            return
        if not self.mediator:
            return
        if event.name == events.EVENT_INVENTORY_CLOSE:
            self.mediator.Invoke('inventoryStateChange', GfxValue(False))
        else:
            self.mediator.Invoke('inventoryStateChange', GfxValue(True))

    @ui.checkInventoryLock()
    def onBuyAllPreviewItems(self, *arg):
        if arg[3][0] is None:
            return
        else:
            mallIds = uiUtils.gfxArray2Array(arg[3][0])
            if not mallIds:
                return
            self.confirmBuyMallIds = []
            for i in xrange(len(mallIds)):
                self.confirmBuyMallIds.append(int(mallIds[i].GetNumber()))

            msg = gameStrings.TEXT_FULLSCREENFITTINGROOMPROXY_140
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmBuyAllPreviewItems)
            return

    @ui.checkInventoryLock()
    def confirmBuyAllPreviewItems(self):
        if not self.confirmBuyMallIds:
            return
        mallNums = []
        for i in xrange(len(self.confirmBuyMallIds)):
            mallNums.append(1)

        self.mallProxy.confirmBuyType = 'fsfrpv.0'
        p = BigWorld.player()
        dicountInfo = clientUtils.getMallItemDiscountInfo(self.confirmBuyMallIds)
        if not dicountInfo:
            return
        p.base.buyMallItems(self.confirmBuyMallIds, mallNums, p.cipherOfPerson, 2, dicountInfo)

    def onBuyAllPreviewItemsSucc(self, type, index):
        self.mallProxy.confirmBuyType = ''
        gameglobal.rds.ui.inventory.show(tempPanel='mall')
        if type == 'fsfrpv':
            if self.buyConfirmMediator:
                self.buyConfirmMediator.Invoke('previewItemsBuyDone', (GfxValue(type), GfxValue(index)))
            if self.mediator:
                self.mediator.Invoke('showBagNewItemEff', GfxValue(True))
        elif type == 'fsfr':
            if self.mediator:
                self.mediator.Invoke('confirmBuyDoneOneItem', (GfxValue(type), GfxValue(index)))
                self.mediator.Invoke('showBagNewItemEff', GfxValue(True))

    def afterModelFinished(self):
        self.uiAdapter.hideAllUI()
        gameglobal.rds.ui.loadWidget(self.fittingRoomWidgetId)

    def showFullscreenFittingRoomConfig(self):
        return gameglobal.rds.configData.get('enableFullScreenFittingRoom', False)

    def clearWidget(self):
        self.mallProxy.confirmBuyType = ''
        try:
            self.mallProxy.tabMgr.setSelectedChildId(self.mallTabInfo[0])
            self.mallProxy.tabMgr.getSelChild().setSelectedChildId(self.mallTabInfo[1])
        except:
            self.mallProxy.tabMgr.setSelectedChildId(DEF_MALL_TAB_MAIN)
            self.mallProxy.tabMgr.getSelChild().setSelectedChildId(DEF_MALL_TAB_SUB)

        self.uiAdapter.restoreUI()
        gameglobal.rds.ui.unLoadWidget(self.fittingRoomWidgetId)
        self.mediator = None
        gameglobal.rds.ui.fittingRoom.leaveFullScreenFitting()

    def reset(self):
        self.cacheItemsInfo = []
        self.previewItemInfo = {}
        self.buyConfirmInfo = []
        self.confirmBuyMallIds = []
        self.searchKeyWord = ''
        self.mallTabInfo = [DEF_MALL_TAB_MAIN, DEF_MALL_TAB_SUB]

    def onSendMoneyCallback(self):
        if self.mediator:
            self.mediator.Invoke('refreshMyMoney')
        if self.buyConfirmMediator:
            self.buyConfirmMediator.Invoke('refreshMyMoney')

    @ui.uiEvent(uiConst.WIDGET_FULLSCREEN_FITTINGROOM, events.EVENT_POINTS_CHANGE)
    def onEventPointsChange(self):
        if self.mediator:
            self.mediator.Invoke('refreshMyPointsInfo')

    def onGetAllTabsInfo(self, *arg):
        allMainTabs = self.mallProxy.tabMgr.getChildrenInfo()
        fsMainTabs = self.filterFullScreenPreviewTabs(allMainTabs, 'mainId')
        fsMainTabs = self.insertSubTabInfos(fsMainTabs)
        return uiUtils.array2GfxAarry(fsMainTabs, True)

    def onGetMallItemList(self, *arg):
        mainId = int(arg[3][0].GetNumber())
        subId = int(arg[3][1].GetNumber())
        if mainId == tianyuMallProxy.MAIN_TAB_FS_SEARCH:
            itemsInfo = self.getSearchItemList()
        else:
            itemsInfo = self.getTabItemList(mainId, subId)
        itemsInfo = self.mallProxy.appendLimitInfo(itemsInfo)
        itemsInfo.sort(key=lambda value: value.get('canBuy', True), reverse=True)
        self.cacheItemsInfo = itemsInfo
        preview = MCD.data.get((mainId, subId), {}).get('preview', tianyuMallProxy.PREVIEW_NONE)
        if preview == tianyuMallProxy.PREVIEW_SHOW_NO_MC:
            self.mediator.Invoke('setPreviewMcVisible', GfxValue(False))
        elif preview == tianyuMallProxy.PREVIEW_SHOW_MC:
            self.mediator.Invoke('setPreviewMcVisible', GfxValue(True))
        return uiUtils.array2GfxAarry(itemsInfo, True)

    def getSearchItemList(self):
        searchResult = self.mallProxy.tabMgr.searchByKeyWord(self.searchKeyWord, tianyuMallProxy.SEARCH_SCOPE_FITTING_ROOM)
        itemsInfo = searchResult['itemsInfo']
        return [ child for child in itemsInfo if child.get('validPeriod', 0) < 0 ]

    def getTabItemList(self, mainId, subId):
        self.mallProxy.tabMgr.setSelectedChildId(mainId)
        self.mallProxy.tabMgr.getSelChild().setSelectedChildId(subId)
        itemsInfo = self.mallProxy.tabMgr.getSelChild().getSelChild().getChildrenInfo()
        return [ child for child in itemsInfo if child.get('validPeriod', 0) < 0 ]

    def onSetPreviewInfo(self, *arg):
        btnIdx = int(arg[3][0].GetNumber())
        itemMallInfo = self.getItemInfoByIdx(btnIdx)
        if not itemMallInfo:
            return
        itemId = itemMallInfo['itemId']
        item = Item(itemId)
        self.addPreviewItemInfo(btnIdx, item, itemMallInfo)
        gameglobal.rds.ui.fittingRoom.addFullScreenItem(item)
        self.setWearBtnVisible()

    def setWearBtnVisible(self):
        value = gameglobal.rds.ui.fittingRoom.isWearBtnShow()
        if self.mediator:
            self.mediator.Invoke('setWearBtnVisible', GfxValue(value))

    def onCancelPreviewInfo(self, *arg):
        btnIdx = int(arg[3][0].GetNumber())
        itemMallInfo = self.getItemInfoByIdx(btnIdx)
        if not itemMallInfo:
            return
        itemId = itemMallInfo['itemId']
        item = Item(itemId)
        self.removePreviewItemInfo(btnIdx)
        gameglobal.rds.ui.fittingRoom.delFullScreenItem(item)
        self.setWearBtnVisible()

    def onCancelPartPreviewInfo(self, *arg):
        part = int(arg[3][0].GetNumber())
        if not self.previewItemInfo.has_key(part):
            return
        itemId = self.previewItemInfo[part]['itemId']
        item = Item(itemId)
        gameglobal.rds.ui.fittingRoom.delFullScreenItem(item)
        self.previewItemInfo.pop(part)
        self.refreshSelectState()

    def onOpenInventory(self, *arg):
        if arg[3][0].GetBool():
            gameglobal.rds.ui.inventory.show(tempPanel='mall')
        else:
            gameglobal.rds.ui.inventory.hide()

    def onSearchFittingRoom(self, *arg):
        self.searchKeyWord = ui.unicode2gbk(arg[3][0].GetString())
        self.mallProxy.tabMgr.setSelectedChildId(tianyuMallProxy.MAIN_TAB_FS_SEARCH)

    def addPreviewItemInfo(self, btnIdx, item, itemMallInfo):
        if not gameglobal.rds.ui.fittingRoom.checkItemPreview(item, False):
            return
        else:
            if self.checkBonusData(item):
                itemList = self.getBonusData(item)
                for bonusItem in itemList:
                    self.addPreviewItemInfo(btnIdx, bonusItem, itemMallInfo)

            else:
                mallInfo = {}
                if self.mallProxy.tabMgr.selChildId == tianyuMallProxy.MAIN_TAB_FS_SEARCH:
                    mallInfo['mainId'] = tianyuMallProxy.MAIN_TAB_FS_SEARCH
                    mallInfo['subId'] = 0
                else:
                    mallInfo['mainId'] = self.mallProxy.tabMgr.selChildId
                    mallInfo['subId'] = self.mallProxy.tabMgr.getSelChild().selChildId
                mallInfo['btnIdx'] = btnIdx
                mallInfo['mallId'] = itemMallInfo['mallId']
                parts = list(item.wherePreview())
                parts.extend(uiUtils.getAspectParts(item.id))
                if gametypes.EQU_PART_RIDE in parts or gametypes.EQU_PART_WINGFLY in parts:
                    parts.append(EQU_PART_RIDE_OR_WINGFLY)
                mainPart = parts[0] if len(parts) > 0 else None
                mallInfo = uiUtils.getGfxItem(item, uiConst.ICON_SIZE40, mallInfo)
                mallInfo['itemId'] = item.id
                mallInfo['parts'] = parts
                clearPartList = []
                for part, info in self.previewItemInfo.iteritems():
                    partSet = set(info['parts'])
                    mySet = set(parts)
                    if bool(partSet.intersection(mySet)):
                        clearPartList.append(part)

                for part in clearPartList:
                    self.previewItemInfo.pop(part)

                if mainPart is not None:
                    mallInfo['mainPart'] = mainPart
                    self.previewItemInfo[mainPart] = mallInfo
            self.refreshSelectState()
            return

    def removePreviewItemInfo(self, btnIdx):
        if self.mallProxy.tabMgr.selChildId == tianyuMallProxy.MAIN_TAB_FS_SEARCH:
            mainId = tianyuMallProxy.MAIN_TAB_FS_SEARCH
            subId = 0
        else:
            mainId = self.mallProxy.tabMgr.selChildId
            subId = self.mallProxy.tabMgr.getSelChild().selChildId
        for part in self.previewItemInfo.keys():
            mallInfo = self.previewItemInfo[part]
            if part == 'otherList':
                for i in range(len(mallInfo)):
                    info = mallInfo[i]
                    if info['btnIdx'] == btnIdx and info['mainId'] == mainId and info['subId'] == subId:
                        mallInfo.pop(i)

            elif mallInfo['btnIdx'] == btnIdx and mallInfo['mainId'] == mainId and mallInfo['subId'] == subId:
                self.previewItemInfo.pop(part)

        self.refreshSelectState()

    def genBuyConfirmItemInfo(self):
        self.buyConfirmInfo = []
        for part in self.previewItemInfo.keys():
            mallInfo = self.previewItemInfo[part]
            if part == 'otherList':
                for i in range(len(mallInfo)):
                    info = mallInfo[i]
                    self.buyConfirmInfo.append(info)

            else:
                self.buyConfirmInfo.append(mallInfo)

        for i in xrange(len(self.buyConfirmInfo)):
            info = self.buyConfirmInfo[i]
            self.buyConfirmInfo[i] = tianyuMallProxy.genMallItemInfo(info['mallId'])

        self.buyConfirmInfo = gameglobal.rds.ui.tianyuMall.appendLimitInfo(self.buyConfirmInfo)
        self.buyConfirmInfo = self.mallItemCanBuyCheck(self.buyConfirmInfo)

    def mallItemCanBuyCheck(self, itemList):
        for itemInfo in itemList:
            if not itemInfo['hasPermission']:
                itemInfo['canBuy'] = False
            elif itemInfo['limitType'] != tianyuMallProxy.LIMIT_TYPE_NONE:
                itemInfo['canBuy'] = itemInfo['leftNum'] > 0
            else:
                itemInfo['canBuy'] = True
            itemInfo['selected'] = itemInfo['canBuy']

        return itemList

    def refreshSelectState(self):
        if not self.mediator:
            return
        selectInfo = {}
        for part, mallInfo in self.previewItemInfo.iteritems():
            mainTabSelInfo = selectInfo.setdefault(mallInfo['mainId'], {})
            subTabSelInfo = mainTabSelInfo.setdefault(mallInfo['subId'], [])
            subTabSelInfo.append(mallInfo)

        self.mediator.Invoke('refreshSelectState', uiUtils.dict2GfxDict(selectInfo, True))

    def filterFullScreenPreviewTabs(self, orgTabs, matchKey):
        cursor = 0
        selectMatch = False
        selectTabId = orgTabs[-1]
        for i in range(len(orgTabs)):
            if cursor >= len(orgTabs) - 2:
                break
            tabInfo = orgTabs[cursor]
            if not tabInfo['fsPreview']:
                orgTabs.pop(cursor)
            else:
                cursor += 1
                if selectTabId == tabInfo[matchKey]:
                    selectMatch = True

        orgTabs[-2] = len(orgTabs) - 2
        if not selectMatch and orgTabs[-2] > 0:
            orgTabs[-1] = orgTabs[0][matchKey]
        return orgTabs

    def insertSubTabInfos(self, fsMainTabs):
        tabMgr = self.mallProxy.tabMgr
        for i in range(len(fsMainTabs) - 2):
            mainTabInfo = fsMainTabs[i]
            mainTab = tabMgr.getChild(mainTabInfo['mainId'])
            if not mainTab:
                continue
            allSubTabs = mainTab.getChildrenInfo()
            fsSubTabs = self.filterFullScreenPreviewTabs(allSubTabs, 'subId')
            mainTabInfo['subTabList'] = fsSubTabs

        return fsMainTabs

    def getItemInfoByIdx(self, idx):
        if idx < 0 or idx >= len(self.cacheItemsInfo):
            return {}
        return self.cacheItemsInfo[idx]

    def checkBonusData(self, item):
        return item.type == Item.BASETYPE_CONSUMABLE and CID.data.get(item.id, {}).has_key('itemSetInfo')

    def getBonusData(self, item):
        bonusSetId, _ = CID.data.get(item.id, {}).get('itemSetInfo', (0, 0))
        if not bonusSetId:
            return []
        bsd = BSD.data.get(bonusSetId, [])
        items = [ Item(data['bonusId']) for data in bsd if data.get('bonusType', 0) == gametypes.BONUS_TYPE_ITEM ]
        if bsd and bsd[0].get('calcType') in (0, 1):
            items = utils.filtItemByConfig(items, lambda e: e.id)
        return items

    @ui.callFilter(1, True)
    def onUpdateFigure(self, *arg):
        btnName = arg[3][0].GetString()
        if btnName == 'openWearBtn':
            self.uiAdapter.fittingRoom.updateModelFigure('open')
        elif btnName == 'showWearBtn':
            self.uiAdapter.fittingRoom.updateModelFigure('show')
        elif btnName == 'closeWearBtn':
            self.uiAdapter.fittingRoom.updateModelFigure('close')

    def onGetFashionDesc(self, *arg):
        desc = self.uiAdapter.fittingRoom.getFashionDesc()
        return GfxValue(gbk2unicode(desc))

    def onChangeColor(self, *arg):
        index = int(arg[3][0].GetNumber())
        descStr = 'prbDyeLists' if self.uiAdapter.fittingRoom.isPbrEquip() else 'dyeLists'
        dyeLists = MCFD.data.get(descStr, [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        if index < len(dyeLists):
            dyeList = dyeLists[index]
            self.uiAdapter.fittingRoom.setFullScreenModel(dyeList)

    def onGetColor(self, *arg):
        dyeLists = MCFD.data.get('dyeLists', [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        ret = []
        for dyeList in dyeLists:
            if not dyeList:
                ret.append(-1)
            else:
                color = dyeList[0]
                color = color.split(',')
                color = [ (int(item) if int(item) <= 255 else 255) for item in color ]
                ret.append((color[0] << 16) + (color[1] << 8) + color[2])

        return uiUtils.array2GfxAarry(ret)

    def onReSetFigure(self, *arg):
        btnName = arg[3][0].GetString()
        applyBare = False
        if btnName == 'nudeBtn':
            applyBare = True
        self.uiAdapter.fittingRoom.restoreModel(applyBare)
        self.previewItemInfo = {}
        self.refreshSelectState()

    def onIsEditModeOn(self, *arg):
        ret = not BigWorld.isPublishedVersion()
        return GfxValue(ret)

    def onOpenEditMode(self, *arg):
        gameglobal.rds.loginScene.setEditMode(1)

    def onSaveCameraAndYaw(self, *arg):
        gameglobal.rds.loginScene.saveCameraAndYaw()
