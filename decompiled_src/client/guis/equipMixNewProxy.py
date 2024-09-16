#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipMixNewProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import utils
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from item import Item
from ui import gbk2unicode
from data import equip_synthesize_category_data as ESCD
from data import equip_synthesize_data as ESD
from data import item_data as ID
from cdata import item_synthesize_set_data as ISSD
from cdata import equip_synthesize_npc_function_data as ESNFD
from cdata import game_msg_def_data as GMDD
from data import equip_data as ED
from data import game_msg_data as GMD

class EquipMixNewProxy(SlotDataProxy):
    NEED_SHOW_LEN = 3
    EFFECT_TIME = 1

    def __init__(self, uiAdapter):
        super(EquipMixNewProxy, self).__init__(uiAdapter)
        self.modelMap = {'selectedFunc': self.onSelectedFunc,
         'selectedItem': self.onSelectedItem,
         'confirmMix': self.onConfirmMix,
         'setTabInfo': self.setTabInfo,
         'startShow': self.startShow,
         'refreshView': self.onRefreshView,
         'showFittingRoom': self.onShowFittingRoom}
        self.reset()
        self.category = {}
        for key, value in ESCD.data.items():
            self.category[key] = value.get('categoryName', '')

        self.type = 'EquipMixNew'
        self.bindType = 'EquipMixNew'
        self.hasBindMaterial = False
        self.tabList = []
        self.cateItemList = {}
        self.targetItemId = 0
        self.selectSynId = 0
        self.synFuncList = []
        self.hasEnh = False
        self.hasValuable = False
        self.valuabelItemName = ''
        self.mainMaterialId = 0
        self.nowCallBack = None
        self.skilRefresh = False
        self.selectMaterialPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_MIX_NEW, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_MIX_NEW:
            self.mediator = mediator
            if BigWorld.player():
                BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)

    def startShow(self, *args):
        self.hasEnh = False
        self.hasValuable = False
        self.mainMaterialId = 0
        self.setTitleAndTab()
        self.setTab(0)

    def reset(self):
        self.mediator = None
        self.entityId = None
        self.itemId = None
        self.mainMaterialId = 0
        self.idx = None
        self.filterId = None
        self.hasBindMaterial = False
        self.targetItemId = 0
        self.selectSynId = 0
        self.synFuncList = []
        self.hasEnh = False
        self.hasValuable = False
        self.valuabelItemName = ''

    def show(self, entId, filterId = 0):
        self.entityId = entId
        self.filterId = filterId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_MIX_NEW)

    def clearWidget(self):
        self.reset()
        if self.nowCallBack:
            BigWorld.cancelCallback(self.nowCallBack)
            self.nowCallBack = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_MIX_NEW)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onItemRemove(self, params):
        if self.skilRefresh:
            return
        self.refreshAll(params)

    def onItemChange(self, params):
        if self.skilRefresh:
            return
        self.refreshAll(params)

    def showEffect(self):
        if self.mediator:
            self.mediator.Invoke('showEffect', ())

    def refreshAll(self, params):
        if self.mediator:
            if params[0] != const.RES_KIND_INV:
                return
            self.onRefreshView(None)

    def refreshAllSuc(self):
        if self.mediator:
            self.onRefreshView(None)
            self.skilRefresh = False

    def onRefreshView(self, *args):
        self.doSelectItem(self.targetItemId, True)
        self.setSelectedSynList(self.targetItemId, self.selectSynId)

    def onShowFittingRoom(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        item = Item(itemId)
        gameglobal.rds.ui.fittingRoom.addItem(item)

    def setTitleAndTab(self):
        if not self.filterId:
            return
        synDatas = ESNFD.data.get(int(self.filterId), {}).get('syncthesizeId', ())
        p = BigWorld.player()
        cateList = []
        self.cateItemList = {}
        for itemId, synMethod in synDatas:
            _, value = synMethod, ESD.data.get((itemId, synMethod))
            if value:
                schoolLimit = value.get('schoolShowLimit', [])
                if not schoolLimit or p.realSchool in schoolLimit:
                    nowCate = value.get('category', 0)
                    item = [nowCate, self.category.get(nowCate)]
                    if item not in cateList:
                        cateList.append(item)
                    if not self.cateItemList.get(nowCate):
                        self.cateItemList[nowCate] = []
                    self.cateItemList[nowCate].append([itemId, synMethod])

        cateList.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        self.tabList = cateList
        if self.mediator:
            self.mediator.Invoke('setTabList', uiUtils.array2GfxAarry(cateList, True))
        shopName = ESNFD.data.get(self.filterId, {}).get('shopName', ())
        name = ''
        if shopName:
            name = shopName
        elif len(cateList) > 0:
            name = ''
            if cateList[0][0] < 3:
                name = gameStrings.TEXT_EQUIPMIXNEWPROXY_183
            elif cateList[0][0] >= 3 and cateList[0][0] < 8:
                name = gameStrings.TEXT_EQUIPMIXNEWPROXY_185
            elif cateList[0][0] in (8, 9, 10, 13):
                name = gameStrings.TEXT_EQUIPMIXNEWPROXY_187
            elif cateList[0][0] == 11:
                name = gameStrings.TEXT_EQUIPMIXNEWPROXY_189
            elif cateList[0][0] == 12:
                name = gameStrings.TEXT_TIANYUMALLPROXY_3415
            name = name + gameStrings.TEXT_GAMECONST_1211
        self.mediator.Invoke('setShopName', GfxValue(gbk2unicode(name)))

    def setTab(self, idx):
        self.mediator.Invoke('setTab', GfxValue(idx))

    def setTabInfo(self, *args):
        cate = int(args[3][0].GetNumber())
        showList = ESNFD.data.get(self.filterId, {}).get('showList', {}).get(cate)
        if showList:
            self.setSynItemList(showList)
        else:
            cateItemList = self.cateItemList.get(cate, [])
            i = 0
            retList = []
            for subItem in cateItemList:
                if i % 8 == 0:
                    retList.append([])
                retList[i / 8].append(subItem[0])
                i = i + 1

            self.setSynItemList(retList)

    def setSynItemList(self, itemSynList):
        ret = []
        i = 0
        firstItem = 0
        for itemList in itemSynList:
            forList = []
            for itemId in itemList:
                itemData = uiUtils.getItemData(itemId)
                itemData['pos'] = i
                if len(self.getItemFuncInSchoolLimit(itemId)) > 0:
                    if i == 0:
                        firstItem = itemId
                    i = i + 1
                    forList.append(itemData)

            if forList:
                ret.append(forList)

        if len(ret) < self.NEED_SHOW_LEN:
            for i in xrange(self.NEED_SHOW_LEN - len(ret)):
                ret.append([])

        self.mediator.Invoke('setItemList', uiUtils.array2GfxAarry(ret))
        if firstItem:
            self.doSelectItem(firstItem)
            if self.mediator:
                self.mediator.Invoke('selectItemShow', GfxValue(0))

    def onSelectedItem(self, *args):
        itemId = int(args[3][0].GetNumber())
        self.doSelectItem(itemId)

    def getItemFuncInSchoolLimit(self, itemId):
        synDatas = ESNFD.data.get(self.filterId, {}).get('syncthesizeId', ())
        synFuncList = []
        p = BigWorld.player()
        for value in synDatas:
            if value[0] == itemId:
                esdValue = ESD.data.get((itemId, value[1]))
                if esdValue:
                    schoolLimit = esdValue.get('schoolShowLimit', [])
                    if not schoolLimit or p.realSchool in schoolLimit:
                        synFuncList.append(value)

        return synFuncList

    def doSelectItem(self, itemId, refresh = False):
        self.synFuncList = []
        self.targetItemId = itemId
        name = uiUtils.getItemColorName(itemId)
        if self.mediator:
            self.mediator.Invoke('setTargetItemName', GfxValue(gbk2unicode(name)))
        self.synFuncList = self.getItemFuncInSchoolLimit(itemId)
        self.setSynFuncList(self.synFuncList)
        if not refresh:
            if self.mediator:
                self.mediator.Invoke('selectedFunc', GfxValue(0))

    def getInhertArr(self, esdValue):
        strArr = []
        if esdValue:
            synType = esdValue.get('type', uiConst.FORMULA_TYPE_MIX)
            if synType == uiConst.FORMULA_TYPE_LV_UP:
                if esdValue.get('inheritStarExp', 0):
                    strArr.append(gameStrings.TEXT_IMPL_IMPITEM_7617)
                if esdValue.get('inheritPrefixProp', 0):
                    strArr.append(gameStrings.TEXT_ITEMRECALLPROXY_332)
                if esdValue.get('inheritRandProp', 0):
                    strArr.append(gameStrings.TEXT_EQUIPMIXNEWPROXY_291)
                if esdValue.get('inheritExhanceLv', 0):
                    strArr.append(gameStrings.TEXT_EQUIPMIXNEWPROXY_293)
                if esdValue.get('inheritExhanceJuexing', 0):
                    strArr.append(gameStrings.TEXT_EQUIPMIXNEWPROXY_295)
                if esdValue.get('inheritStarLv', 0):
                    strArr.append(gameStrings.TEXT_EQUIPMIXNEWPROXY_297)
                if esdValue.get('inheritYinYangSlots', 0):
                    strArr.append(gameStrings.TEXT_EQUIPMIXNEWPROXY_299)
        return strArr

    def setSynFuncList(self, synFuncList):
        checkList = []
        for synFunc in synFuncList:
            ret = self.getSynFuncMaterialItem(synFunc[0], synFunc[1])
            esdValue = ESD.data.get((synFunc[0], synFunc[1]))
            strArr = []
            if esdValue:
                strArr = self.getInhertArr(esdValue)
            if ret.get('material'):
                if len(ret.get('material')):
                    ret['inheritProp'] = strArr
                    checkList.append(ret)

        self.mediator.Invoke('setSynFuncList', uiUtils.array2GfxAarry(checkList, True))

    def getSynFuncMaterialItem(self, itemId, synId, needFullCount = False, needCheckMainMaterial = False):
        eData = ESD.data.get((itemId, synId))
        p = BigWorld.player()
        if eData:
            items = eData.get('materialNeed', ())
            itemGroup = eData.get('materialSetNeed', ())
            funcName = eData.get('funcName', '')
            synType = eData.get('type', uiConst.FORMULA_TYPE_MIX)
            groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
            items += tuple(groupItems)
            material = []
            hasBindMaterial = False
            materialEnough = True
            mainMaterialPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
            self.hasEnh = False
            self.hasValuable = False
            srcId = items[0][1]
            for itemSearchType, itemIdM, itemNum in items:
                itemData = uiUtils.getItemData(itemIdM)
                enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                maxNum = p.inv.countItemInPages(itemIdM, enableParentCheck=enableParentCheck, filterFunc=lambda it: len(it.getAllGuanYinPskill()) == 0)
                if p.inv.countItemInPages(itemIdM, enableParentCheck=enableParentCheck, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY):
                    hasBindMaterial = True
                if needCheckMainMaterial:
                    if srcId == itemIdM:
                        hasEnh = False
                    else:
                        hasEnh = p.inv.getItemHasEnhLv(itemIdM, itemNum)
                    if hasEnh:
                        self.hasEnh = True
                hasValuable = p.inv.getItemHasValuableTradeItem(itemIdM, itemNum)
                if hasValuable:
                    self.hasValuable = p.inv.getItemHasValuableTradeItem(itemIdM, itemNum)
                    self.valuabelItemName = uiUtils.getItemColorName(itemIdM)
                itemData['maxNum'] = maxNum
                itemData['needNum'] = itemNum
                if not needFullCount:
                    if maxNum >= itemNum:
                        numStr = uiUtils.toHtml('%d' % itemNum, '#FFFFE7')
                    else:
                        numStr = uiUtils.toHtml('%d' % itemNum, '#F43804')
                        materialEnough = False
                else:
                    if maxNum < itemNum:
                        materialEnough = False
                    numStr = uiUtils.convertNumStr(itemData['maxNum'], itemData['needNum'])
                if len(material) == 0 and itemData['maxNum'] == itemData['needNum']:
                    page, pos = p.inv.findItemInPages(itemIdM)
                    mainMaterialPos = [page, pos]
                if len(material) == 0 and synType == uiConst.FORMULA_TYPE_LV_UP and itemData['maxNum'] > itemData['needNum'] and needCheckMainMaterial:
                    if not needFullCount:
                        numStr = uiUtils.toHtml('%d' % itemNum, '#F43804')
                    else:
                        numStr = uiUtils.convertNumStr(0, itemData['needNum'])
                    itemData['count'] = numStr
                    itemData['srcType'] = 'equipMixNew_mainMaterial'
                else:
                    itemData['srcType'] = 'equipMixNew_material'
                    itemData['count'] = numStr
                material.append(itemData)

            ret = {'material': material,
             'hasBindMaterial': hasBindMaterial,
             'targetId': itemId,
             'synId': synId,
             'materialEnough': materialEnough,
             'synType': synType,
             'mainMaterialPos': mainMaterialPos,
             'funcName': funcName}
            return ret
        else:
            return {}

    def onSelectedFunc(self, *args):
        targetItemId = int(args[3][0].GetNumber())
        synId = int(args[3][1].GetNumber())
        self.setSelectedSynList(targetItemId, synId)

    def setSelectedSynList(self, targetItemId, synId):
        self.mainMaterialId = 0
        self.selectMaterialPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        material = self.getSynFuncMaterialItem(targetItemId, synId, True, True)
        if material:
            targetItem = uiUtils.getItemData(targetItemId)
            targetItem['srcType'] = 'equipMixNew_target'
            ret = {'material': material.get('material'),
             'targetItem': targetItem,
             'synType': material.get('synType')}
            if self.mediator:
                self.mediator.Invoke('setSelectedSynList', uiUtils.dict2GfxDict(ret))
            ret2 = self._cashInfo(targetItemId, synId)
            if self.mediator:
                self.mediator.Invoke('setCash', (GfxValue(ret2[0]), GfxValue(ret2[1])))
            self.hasBindMaterial = material.get('hasBindMaterial')
            canConfirm = True
            self.targetItemId = targetItemId
            self.selectSynId = synId
            if not material['materialEnough'] or not ret2[1]:
                canConfirm = False
            if self.mediator:
                if material['synType'] == uiConst.FORMULA_TYPE_LV_UP:
                    self.mainMaterialId = material['material'][0]['itemId']
                    if gameglobal.rds.ui.inventory.mediator:
                        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
                    if material['material'][0]['maxNum'] > material['material'][0]['needNum']:
                        self.mediator.Invoke('setHintVisible', GfxValue(True))
                        self.mediator.Invoke('setConfirmEnable', GfxValue(False))
                        if not gameglobal.rds.ui.inventory.mediator:
                            gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)
                        return
                    if material['material'][0]['maxNum'] == material['material'][0]['needNum']:
                        if material['mainMaterialPos'] != const.CONT_NO_PAGE:
                            self.selectMaterialPos = material['mainMaterialPos']
                self.mediator.Invoke('setConfirmEnable', GfxValue(canConfirm))
                self.mediator.Invoke('setHintVisible', GfxValue(False))
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def isEnableParentCheck(self):
        eData = ESD.data.get((self.targetItemId, self.selectSynId))
        if eData:
            items = eData.get('materialNeed', ())
            if items:
                if len(items[0]) == 3:
                    itemSearchType = items[0][0]
                    enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                    return enableParentCheck
        return False

    def checkItemCanUse(self, item):
        if item == None:
            return False
        elif self.mainMaterialId == item.id:
            return True
        else:
            if self.isEnableParentCheck():
                if item.getParentId() == self.mainMaterialId:
                    return True
            return False

    def setNeedItem(self, page, pos):
        eData = ESD.data.get((self.targetItemId, self.selectSynId))
        p = BigWorld.player()
        if eData:
            isRight = False
            items = eData.get('materialNeed', ())
            if items:
                if len(items[0]) == 3:
                    itemSearchType = items[0][0]
                    itemIdM = items[0][1]
                    itemNum = items[0][2]
                    enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                    item = p.inv.getQuickVal(page, pos)
                    if enableParentCheck:
                        if item.id == itemIdM or item.getParentId() == itemIdM:
                            self.selectMaterialPos = [page, pos]
                            isRight = True
                    elif item.id == itemIdM:
                        self.selectMaterialPos = [page, pos]
                        isRight = True
                    if isRight:
                        self.mediator.Invoke('setHintVisible', GfxValue(False))
                        itemData = uiUtils.getItemData(itemIdM)
                        needFullCount = True
                        if not needFullCount:
                            numStr = uiUtils.toHtml('%d' % itemNum, '#FFFFE7')
                        else:
                            numStr = uiUtils.convertNumStr(1, itemNum)
                        itemData['count'] = numStr
                        itemData['srcType'] = 'equipMixNew_mainMaterial'
                        self.mediator.Invoke('setMainMaterial', uiUtils.dict2GfxDict(itemData))
                        self.mediator.Invoke('setHintVisible', GfxValue(False))
                        material = self.getSynFuncMaterialItem(self.targetItemId, self.selectSynId)
                        cashInfo = self._cashInfo(self.targetItemId, self.selectSynId)
                        canConfirm = True
                        if not material['materialEnough'] or not cashInfo[1]:
                            canConfirm = False
                        self.mediator.Invoke('setConfirmEnable', GfxValue(canConfirm))
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def _cashInfo(self, itemId, idx):
        p = BigWorld.player()
        fData = ESD.data.get((itemId, idx), [])
        cash = 0
        if fData:
            cash = fData.get('cashNeed', 0)
        enough = True
        if cash > p.bindCash + p.cash:
            enough = False
        ret = [cash, enough]
        return ret

    def isBindCashEnough(self, itemId, idx):
        p = BigWorld.player()
        fData = ESD.data.get((itemId, idx), [])
        cash = 0
        if fData:
            cash = fData.get('cashNeed', 0)
        enough = True
        if cash > p.bindCash:
            enough = False
        return enough

    @ui.callFilter(1)
    def onConfirmMix(self, *args):
        self.checkCashEnough(self.doMix)

    def doMix(self):
        itemId = self.targetItemId
        idx = self.selectSynId
        data = ESD.data.get((itemId, idx))
        if data:
            synType = data.get('type', uiConst.FORMULA_TYPE_MIX)
            if synType == uiConst.FORMULA_TYPE_MIX:
                name = uiUtils.getItemColorName(itemId)
                msg = uiUtils.getTextFromGMD(GMDD.data.MIX_ITEM_CONFIRM_TEXT, gameStrings.TEXT_EQUIPMIXNEWPROXY_539) % name
                targetBind = ID.data.get(itemId, {}).get('bindType', 0) == gametypes.ITEM_BIND_TYPE_FOREVER
                if self.hasBindMaterial or targetBind:
                    bindHint = uiUtils.getTextFromGMD(GMDD.data.MIX_ITEM_BINDHINT_TEXT)
                    if not bindHint:
                        bindHint = gameStrings.TEXT_EQUIPMIXNEWPROXY_544
                    msg += bindHint
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onTrueCommit, itemId, idx))
            elif synType == uiConst.FORMULA_TYPE_LV_UP:
                srcEquip = BigWorld.player().inv.getQuickVal(self.selectMaterialPos[0], self.selectMaterialPos[1])
                if any([ slot.gem != None for slot in getattr(srcEquip, 'yangSlots', ()) ]) or any([ slot.gem != None for slot in getattr(srcEquip, 'yinSlots', ()) ]):
                    BigWorld.player().showGameMsg(GMDD.data.UPGRADE_EQUIP_FAIL_HAS_GEM, ())
                    return
                srcEquip = BigWorld.player().inv.getQuickVal(self.selectMaterialPos[0], self.selectMaterialPos[1])
                if not utils.checkValuableTradeItem(srcEquip):
                    self.hasValuable = True
                    self.valuabelItemName = uiUtils.getItemColorName(srcEquip.id)
                if self.hasValuable:
                    BigWorld.player().showGameMsg(GMDD.data.VALUABLE_ITEM_LATCH, self.valuabelItemName)
                    return
                descStr = uiUtils.getTextFromGMD(GMDD.data.LV_UP_ITEM_WILL_GET, gameStrings.TEXT_EQUIPMIXNEWPROXY_561)
                strArr = self.getInhertArr(data)
                if len(strArr) > 0 and len(self.synFuncList) == 1:
                    for i in xrange(0, len(strArr)):
                        descStr += strArr[i]
                        if i == 3:
                            descStr += '\n'
                        if i != len(strArr) - 1:
                            descStr += '  '

                    descStr += '</font>'
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.doTrueCommitLvUpStep1, itemId, idx))
                else:
                    self.doTrueCommitLvUpStep1(itemId, idx)

    def doTrueCommitLvUpStep1(self, itemId, idx):
        if self.hasEnh:
            descStr = uiUtils.getTextFromGMD(GMDD.data.EQUIP_LV_UP_CONFIRM, gameStrings.TEXT_EQUIPMIXNEWPROXY_581)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.doTrueCommitLvUpStep2, itemId, idx))
        else:
            self.doTrueCommitLvUpStep2(itemId, idx)

    def doTrueCommitLvUpStep2(self, itemId, idx):
        ed = ED.data.get(itemId, {})
        item = Item(itemId)
        if self.selectMaterialPos[0] == const.CONT_NO_PAGE:
            return
        maxEnhlv = item.getMaxEnhLv(BigWorld.player())
        srcEquip = BigWorld.player().inv.getQuickVal(self.selectMaterialPos[0], self.selectMaterialPos[1])
        if getattr(srcEquip, 'enhLv', -1) > maxEnhlv:
            descStr = gameStrings.TEXT_EQUIPMIXNEWPROXY_593
            descStr = GMD.data.get(GMDD.data.EQUIP_UPGRADE_ENHLV, {}).get('text', descStr)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self._doUpgradeEquipItem, self.selectMaterialPos[0], self.selectMaterialPos[1], itemId, idx))
        else:
            self._doUpgradeEquipItem(self.selectMaterialPos[0], self.selectMaterialPos[1], itemId, idx)

    def _doUpgradeEquipItem(self, srcItPage, srcItPos, itemId, idx):
        self.showEffect()
        if self.nowCallBack:
            BigWorld.cancelCallback(self.nowCallBack)
        self.nowCallBack = BigWorld.callback(self.EFFECT_TIME, Functor(self._doTrueUpgradeEquipItem, srcItPage, srcItPos, itemId, idx))

    def _doTrueUpgradeEquipItem(self, srcItPage, srcItPos, itemId, idx):
        if not self.entityId:
            return
        else:
            npcEnt = BigWorld.entities.get(self.entityId)
            self.skilRefresh = True
            npcEnt and npcEnt.cell.upgradeEquipItem(srcItPage, srcItPos, itemId, idx)
            self.nowCallBack = None
            return

    def onTrueCommit(self, itemId, idx):
        self.showEffect()
        if self.nowCallBack:
            BigWorld.cancelCallback(self.nowCallBack)
        self.nowCallBack = BigWorld.callback(self.EFFECT_TIME, Functor(self._onTrueCommit, itemId, idx))

    def _onTrueCommit(self, itemId, idx):
        if not self.entityId:
            return
        else:
            npcEnt = BigWorld.entities.get(self.entityId)
            npcEnt and npcEnt.cell.mixEquipItem(itemId, idx)
            self.skilRefresh = True
            self.nowCallBack = None
            return

    def checkCashEnough(self, callback):
        isEnough = self.isBindCashEnough(self.targetItemId, self.selectSynId)
        if isEnough:
            callback()
        else:
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_USE_CASH, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_USE_CASH')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, callback, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_EQUIP_MIX_NEW)

    def getTargetToolTip(self):
        item = Item(self.targetItemId)
        if self.hasBindMaterial:
            item.bindType = gametypes.ITEM_BIND_TYPE_FOREVER
        return gameglobal.rds.ui.inventory.GfxToolTip(item, const.ITEM_IN_NONE)

    def getMainMaterialToolTip(self, itemId):
        inv = BigWorld.player().inv
        if self.selectMaterialPos[0] != const.CONT_NO_PAGE:
            it = inv.getQuickVal(self.selectMaterialPos[0], self.selectMaterialPos[1])
            return gameglobal.rds.ui.inventory.GfxToolTip(it)
        else:
            return self.getMaterialToolTip(itemId)

    def getMaterialToolTip(self, itemId):
        inv = BigWorld.player().inv
        bindCnt = inv.countItemChild(itemId)
        it = Item(itemId)
        if bindCnt[0]:
            page, pos = inv.findItemInPages(bindCnt[1][0])
            if page != const.CONT_NO_PAGE:
                it = inv.getQuickVal(page, pos)
        else:
            page, pos = inv.findItemInPages(itemId)
            if page != const.CONT_NO_PAGE:
                it = inv.getQuickVal(page, pos)
        return gameglobal.rds.ui.inventory.GfxToolTip(it)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if not self.checkItemCanUse(item):
                return True
            if self.selectMaterialPos == [page, pos]:
                return True
            return False
        else:
            return False
