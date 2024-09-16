#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemRecastProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
import const
import gametypes
import npcConst
from uiProxy import SlotDataProxy
from guis import uiUtils
from guis import ui
from guis import events
from ui import gbk2unicode
from gamestrings import gameStrings
from callbackHelper import Functor
from data import item_recast_data as IRD
from data import npc_data as ND
from data import item_data as ID
from cdata import item_recast_material_data as IRMD
from cdata import item_recast_npc_func_data as IRNFD
from cdata import game_msg_def_data as GMDD

class ItemRecastProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SlotDataProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmRecast': self.onConfirmRecast,
         'selectRuleChanged': self.onSelectRuleChanged,
         'rightClickItem': self.onRightClickItem,
         'selectRecastChanged': self.onSelectRecastChanged}
        self.bindType = 'itemRecast'
        self.type = 'itemRecast'
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_RECAST, self.hide)

    def reset(self):
        self.recastMed = None
        self.currentRecastIds = None
        self.matchRecastIds = None
        self.currentCanLoop = False
        self.recastItemMaxNum = 0
        self.canRecastItems = []
        self.npcEntity = None
        self.mixIdList = None
        self.bindingData = {}
        self.recastItemData = {}
        self.selectedCastId = None
        self.index = 0

    def show(self, *args):
        self.npcEntity = args[0]
        self.index = args[1]
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_RECAST)

    def clearWidget(self):
        self.clearAllRecastItem()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_RECAST)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ITEM_RECAST:
            self.recastMed = mediator
            if self.npcEntity:
                npcId = self.npcEntity.npcId
                functions = ND.data.get(npcId, {}).get('functions', [])
                for i in xrange(len(functions)):
                    funcId = functions[i]
                    if funcId[1] == npcConst.NPC_FUNC_RECAST_ITEM and self.index == i:
                        self.mixIdList = IRNFD.data.get(funcId[2], ()).get('mixIdList', ())

                ruleList = []
                initData = {'ruleList': ruleList}
                for value in self.mixIdList:
                    recastRules = value[1:]
                    data = {}
                    data['ruleName'] = IRD.data.get(recastRules[0], {}).get('name', '')
                    data['msg'] = IRD.data.get(recastRules[0], {}).get('emptyMsg', '')
                    data['recastItemNum'] = max((IRD.data.get(ruleId, {}).get('materialCnt') for ruleId in recastRules))
                    data['ruleGroups'] = value
                    ruleList.append(data)

                return uiUtils.dict2GfxDict(initData, True)

    @ui.checkItemIsLock([2, 3])
    def addItemToRecast(self, item, pageSrc, posSrc, desPage = -1, desPos = -1):
        gamelog.debug('@zhp addItemToRecast', pageSrc, posSrc, desPage, desPos)
        if not self.currentRecastIds:
            gamelog.debug('@zhp addItemToRecast, not currentRecastIds')
            return
        if self.recastItemMaxNum <= len(self.bindingData):
            gamelog.debug('@zhp position null, replace old')
            self.removeRecastItem(self.bindingData.keys()[-1])
        self.canRecastItems = []
        materialSetId = []
        itemNum = {}
        for recastId in self.matchRecastIds:
            mId = IRD.data.get(recastId, {}).get('materialSetId', 0)
            if mId and mId not in materialSetId:
                materialSetId.append(mId)

        for mId in materialSetId:
            for materialData in IRMD.data.get(mId, {}):
                self.canRecastItems.append(materialData.get('itemId'))
                itemNum[materialData.get('itemId')] = materialData.get('num', 1)

        if item.getParentId() not in self.canRecastItems:
            gamelog.debug('@zhp not recast items')
            BigWorld.player().showGameMsg(GMDD.data.ITEM_CAN_NOT_RECAST, (item.name,))
            return
        if desPos == -1:
            desPos = len(self.bindingData)
        bindKey = self.getBindKeyByPagePos(desPage, desPos)
        self.bindingData[bindKey] = item
        if self.binding.has_key(bindKey):
            cnt = min(item.cwrap, itemNum.get(item.getParentId(), 1))
            self.binding[bindKey][1].InvokeSelf(uiUtils.dict2GfxDict(uiUtils.getGfxItem(item, appendInfo={'count': cnt}, location=const.ITEM_IN_BAG)))
        self.recastItemData[bindKey] = (pageSrc, posSrc)
        gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)
        self.refreshMatchIds()

    def removeRecastItem(self, key):
        if self.bindingData.has_key(key):
            del self.bindingData[key]
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            pageSrc, posSrc = self.recastItemData[key]
            del self.recastItemData[key]
            gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)
            self.refreshMatchIds()

    @ui.uiEvent(uiConst.WIDGET_ITEM_RECAST, events.EVENT_INVENTORY_CLOSE)
    def clearAllRecastItem(self):
        data = GfxValue(0)
        data.SetNull()
        for key in self.binding.keys():
            self.binding[key][1].InvokeSelf(data)

        self.matchRecastIds = self.currentRecastIds
        self.bindingData = {}
        recastDatas = self.recastItemData.values()
        self.recastItemData = {}
        self.selectedCastId = None
        for pageSrc, posSrc in recastDatas:
            gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)

        if self.recastMed:
            self.recastMed.Invoke('setMaterialInfo', data)
            self.recastMed.Invoke('setItemBg', GfxValue('off'))

    def getSlotID(self, key):
        return (1, key[-1])

    def getBindKeyByPagePos(self, page, pos):
        return 'itemRecast.slot%s' % pos

    def refreshMatchIds(self):
        if not self.recastMed:
            return
        else:
            if len(self.bindingData) == 0:
                self.matchRecastIds = self.currentRecastIds
                data = GfxValue(0)
                data.SetNull()
                self.recastMed.Invoke('setMaterialInfo', data)
                self.recastMed.Invoke('setItemBg', GfxValue('off'))
            else:
                self.matchRecastIds = []
                materialSets = set([ IRD.data.get(recastId, {}).get('materialSetId', 0) for recastId in self.currentRecastIds ])
                materialSetsIdNum = {}
                for item in self.bindingData.values():
                    pId = item.getParentId()
                    for mSetId in materialSets:
                        for value in IRMD.data.get(mSetId, []):
                            if value.get('itemId') == pId and item.cwrap >= value.get('num', 0):
                                if not materialSetsIdNum.has_key(mSetId):
                                    materialSetsIdNum[mSetId] = 1
                                else:
                                    materialSetsIdNum[mSetId] = materialSetsIdNum[mSetId] + 1
                                break

                for recastId in self.currentRecastIds:
                    recastValue = IRD.data.get(recastId, {})
                    if materialSetsIdNum.has_key(recastValue.get('materialSetId', 0)) and materialSetsIdNum[recastValue.get('materialSetId', 0)] <= recastValue.get('materialCnt', 0):
                        self.matchRecastIds.append(recastId)

                if self.matchRecastIds:
                    materialArray = []
                    materialInfoData = {'materialArray': materialArray,
                     'msg': IRD.data.get(self.matchRecastIds[0], {}).get('selectMaterialMsg', '')}
                    p = BigWorld.player()
                    selectRecastData = None
                    for recastId in self.matchRecastIds:
                        recastData = IRD.data.get(recastId, {})
                        data = {}
                        moneyCost = recastData.get('moneyCost')
                        txt = '0'
                        color = None
                        red = '#ff0000'
                        if moneyCost:
                            txt = str(moneyCost[1])
                            cashType = moneyCost[0]
                            if cashType == gametypes.BIND_CASH_ITEM and not p._canPay(moneyCost[1]):
                                color = red
                            elif cashType == gametypes.CASH_ITEM and not p._canPayCash(moneyCost[1]):
                                color = red
                        data['cashTxt'] = uiUtils.toHtml(txt, color)
                        exp = recastData.get('expCost', 0)
                        data['expNum'] = exp
                        if exp > p.exp:
                            exp = uiUtils.toHtml(exp, red)
                        data['expTxt'] = exp
                        if recastData.has_key('fameCost'):
                            if p.enoughFame(recastData.get('fameCost')):
                                color = None
                            else:
                                color = red
                            txt = ''
                            for fameId, num in recastData.get('fameCost'):
                                if txt:
                                    txt = txt + ','
                                txt = txt + '%s:%s' % (ID.data.get(fameId, {}).get('name', ''), num)

                            data['fameTxt'] = uiUtils.toHtml(txt, color)
                        else:
                            data['fameTxt'] = ''
                        data['cashType'] = 'bindCash' if recastData.get('moneyCost', (0, 0))[0] == gametypes.BIND_CASH_ITEM else 'cash'
                        mList = []
                        enoughMaterial = True
                        for itemCost in recastData.get('itemCost', {}):
                            itemData = {'iconPath': uiUtils.getItemIconFile64(itemCost[0]),
                             'overIconPath': uiUtils.getItemIconFile64(itemCost[0]),
                             'itemId': itemCost[0]}
                            needCnt = itemCost[1]
                            hadCnt = BigWorld.player().inv.countItemInPages(itemCost[0], enableParentCheck=True)
                            if hadCnt >= needCnt:
                                itemData['countTxt'] = str(needCnt)
                            else:
                                enoughMaterial = False
                                itemData['countTxt'] = "<font color = \'#ff0000\'>%s</font>" % needCnt
                            mList.append(itemData)

                        data['enoughMaterial'] = enoughMaterial
                        data['materialList'] = mList
                        data['recastId'] = recastId
                        materialArray.append(data)
                        if self.selectedCastId == recastId:
                            selectRecastData = data

                    if selectRecastData and selectRecastData in materialArray:
                        materialInfoData['selectedCastIndex'] = materialArray.index(selectRecastData)
                    self.recastMed.Invoke('setMaterialInfo', uiUtils.dict2GfxDict(materialInfoData, True))
                    self.recastMed.Invoke('setItemBg', GfxValue('on'))
                else:
                    data = GfxValue(0)
                    data.SetNull()
                    self.recastMed.Invoke('setMaterialInfo', data)
                    self.recastMed.Invoke('setItemBg', GfxValue('off'))
            gamelog.debug('@zhp refreshMatchIds', self.matchRecastIds)
            return

    def onConfirmRecast(self, *args):
        gamelog.debug('@zhp onConfirmRecast', self.selectedCastId)
        if self.selectedCastId and self.recastItemData and self.npcEntity:
            pageList = []
            posList = []
            for recastData in self.recastItemData.values():
                pageList.append(recastData[0])
                posList.append(recastData[1])

            bindConfirm = IRD.data.get(self.selectedCastId, {}).get('bindConfirm', 0)
            if bindConfirm:
                txt = gameStrings.ITEM_RECAST_BIND_CONFIRM
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.realConfirmRecast, self.selectedCastId, pageList, posList))
            else:
                self.npcEntity.cell.recastItem(self.selectedCastId, pageList, posList)
        if not self.recastItemData and self.matchRecastIds:
            msg = IRD.data.get(self.matchRecastIds[0], {}).get('emptyMsg', '')
            gameglobal.rds.ui.messageBox.showAlertBox(msg)

    def realConfirmRecast(self, selectedCastId, pageList, posList):
        self.npcEntity.cell.recastItem(selectedCastId, pageList, posList)

    def onSelectRuleChanged(self, *args):
        index = int(args[3][0].GetNumber())
        gamelog.debug('@zhp onSelectRuleChanged, index:', index)
        if index >= 0:
            self.clearAllRecastItem()
            ruleGroup = self.mixIdList[index]
            self.currentCanLoop = ruleGroup[0]
            self.currentRecastIds = ruleGroup[1:]
            self.matchRecastIds = ruleGroup[1:]
            self.recastItemMaxNum = max((IRD.data.get(ruleId, {}).get('materialCnt') for ruleId in self.currentRecastIds))

    def onRightClickItem(self, *args):
        key = args[3][0].GetString()
        self.removeRecastItem(key)

    def onSelectRecastChanged(self, *args):
        self.selectedCastId = int(args[3][0].GetNumber())
        if self.recastMed:
            msg = IRD.data.get(self.selectedCastId, {}).get('selectMaterialMsg', '')
            self.recastMed.Invoke('updateMsg', GfxValue(gbk2unicode(msg)))

    def onRecastItemSucc(self, uuidList):
        oldSelectedCastId = self.selectedCastId
        self.clearAllRecastItem()
        if self.currentCanLoop:
            self.selectedCastId = oldSelectedCastId
            for uuid in uuidList:
                item, page, pos = BigWorld.player().inv.findItemByUUID(uuid)
                if item:
                    self.addItemToRecast(item, page, pos)

    def isItemDisabled(self, kind, page, pos, item):
        if kind == const.RES_KIND_INV:
            return self.recastMed and (page, pos) in self.recastItemData.values()
