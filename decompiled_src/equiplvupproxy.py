#Embedded file name: /WORKSPACE/data/entities/client/guis/equiplvupproxy.o
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import gametypes
import npcConst
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from item import Item
from guis import ui
from callbackHelper import Functor
from ui import gbk2unicode
from data import equip_data as ED
from data import equip_synthesize_category_data as ESCD
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import equip_star_factor_data as ESFCD
from data import prop_ref_data as PRD
from cdata import equip_special_props_data as ESPD
from cdata import item_synthesize_set_data as ISSD
from cdata import equip_synthesize_npc_function_data as ESNFD
from data import equip_synthesize_data as ESD
from cdata import equip_quality_factor_data as EQFD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import equip_prefix_prop_data as EPFPD
import utils

def float2Int(num):
    return int(num)


class EquipLvUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipLvUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'getItemList': self.onGetItemList,
         'getItemFormula': self.onGetItemFormula,
         'getOtherInfo': self.onGetOtherInfo,
         'confirm': self.onConfirm,
         'close': self.onClose,
         'getFuncType': self.onGetFuncType,
         'gotoWeb': self.onGotoWeb,
         'getTips': self.onGetTips}
        self.reset()
        self.bindType = 'equipLvUp'
        self.type = 'equipLvUp'
        self.category = [ value.get('categoryName', '') for key, value in ESCD.data.items() ]
        self.npcFuncType = npcConst.NPC_FUNC_UPGRADE_EQUIP
        self.itemUUID = ''
        self.itemPos = -1
        self.itemPage = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_LV_UP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_LV_UP:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
            BigWorld.player().registerEvent(const.EVENT_ITEM_MOVE, self.onItemMove)
            BigWorld.player().registerEvent(const.EVENT_ITEM_SORT, self.onItemSort)

    def onItemSort(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        item = params[3]
        if kind != const.RES_KIND_INV:
            if item:
                if item.uuid:
                    if item.uuid == self.itemUUID:
                        self.clearUpdateItemPos()
            return
        if item:
            if item.uuid:
                if item.uuid == self.itemUUID:
                    self.setUpdateItemPos(page, pos)

    def onItemChange(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        if kind != const.RES_KIND_INV:
            return
        if page == self.itemPage and pos == self.itemPos:
            self.setUpdateItemPos(page, pos, True)
        else:
            return

    def onItemRemove(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        if kind != const.RES_KIND_INV:
            return
        if page == self.itemPage and pos == self.itemPos:
            self.clearUpdateItemPos()
        else:
            return

    def onItemMove(self, params):
        srcKind = params[0]
        srcPage = params[1]
        srcPos = params[2]
        dstKind = params[3]
        dstPage = params[4]
        dstPos = params[5]
        if srcKind != const.RES_KIND_INV and dstKind != const.RES_KIND_INV:
            return
        if srcKind == const.RES_KIND_INV:
            if srcPage == self.itemPage and srcPos == self.itemPos:
                if dstKind != const.RES_KIND_INV:
                    self.clearUpdateItemPos()
                    return
                else:
                    self.setUpdateItemPos(dstPage, dstPos)
                    return
        if dstKind == const.RES_KIND_INV:
            if dstPage == self.itemPage and dstPos == self.itemPos:
                if srcKind != const.RES_KIND_INV:
                    self.clearUpdateItemPos()
                    return
                else:
                    self.setUpdateItemPos(srcPage, srcPos)
                    return

    def reset(self):
        if getattr(self, 'mediator', None):
            p = BigWorld.player()
            if p:
                if p.__class__.__name__ == 'PlayerAvatar':
                    p.unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                    p.unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
                    p.unRegisterEvent(const.EVENT_ITEM_MOVE, self.onItemMove)
                    p.unRegisterEvent(const.EVENT_ITEM_SORT, self.onItemSort)
        self.mediator = None
        self.entityId = None
        self.itemId = None
        self.idx = None
        self.filterId = None

    def show(self, entId, filterId, npcType = npcConst.NPC_FUNC_UPGRADE_EQUIP):
        self.entityId = entId
        self.filterId = filterId
        self.npcFuncType = npcType
        if npcType == npcConst.NPC_FUNC_EQUIP_WASH:
            newItem, page, pos = self.checkNewPreProps()
            if newItem:
                self.showConfirmPanel(newItem, page, pos)
                return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_LV_UP)

    def checkNewPreProps(self):
        inv = BigWorld.player().inv
        for page in inv.posCountDict:
            for ps in xrange(inv.posCountDict[page]):
                it = inv.getQuickVal(page, ps)
                if it and it.type == Item.BASETYPE_EQUIP:
                    if hasattr(it, 'newPrefixInfo'):
                        return (it, page, ps)

        return (None, -1, -1)

    def showConfirmPanel(self, item, page, pos):
        item = BigWorld.player().inv.getQuickVal(page, pos)
        preGroupId, prefixId, opNUID = item.popProp('newPrefixInfo')
        newIt = item.deepcopy()
        newIt.removePrefixProps()
        newIt.preprops = []
        newIt.prefixInfo = (preGroupId, prefixId)
        prefixData = EPFPD.data.get(preGroupId)
        data = {}
        for pd in prefixData:
            if pd['id'] == prefixId:
                data = pd
                break

        if not data:
            return
        if data.has_key('props'):
            for pid, pType, pVal in data['props']:
                newIt.preprops.append((pid, pType, pVal))

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_LV_UP)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def _createItemList(self):
        p = BigWorld.player()
        ret = []
        for cateId, title in enumerate(self.category):
            content = []
            synDatas = ESNFD.data.get(self.filterId, {}).get('syncthesizeId', ())
            funcType = ESNFD.data.get(self.filterId, {}).get('funcType', 0)
            for itemId, synMethod in synDatas:
                idx, value = synMethod, ESD.data.get((itemId, synMethod))
                schoolLimit = value.get('schoolShowLimit', [])
                if schoolLimit and p.school not in schoolLimit or value['category'] != cateId + 1:
                    continue
                if funcType == uiConst.FORMULA_TYPE_LV_UP and value['type'] == uiConst.FORMULA_TYPE_LV_UP and self.npcFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP:
                    pass
                elif funcType == uiConst.FORMULA_TYPE_PREFIX_WASH and value['type'] == uiConst.FORMULA_TYPE_PREFIX_WASH and self.npcFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
                    pass
                else:
                    continue
                iData = ID.data.get(itemId, {})
                iconPath = uiUtils.getItemIconFile64(itemId)
                name = iData.get('name', '')
                triggerIdx = synDatas.index((itemId, synMethod), 0)
                content.append({'iconPath': iconPath,
                 'name': name,
                 'itemId': itemId,
                 'idx': idx,
                 'triggerIdx': triggerIdx})
                content.sort(key=lambda k: k['triggerIdx'])

            if len(content) > 0:
                ret.append({'title': title,
                 'content': content})

        return ret

    def setUpdateItemPos(self, page, pos, needReset = False):
        if not self.itemId:
            return
        p = BigWorld.player()
        dItem = p.inv.getQuickVal(page, pos)
        if not dItem:
            return
        eData = ESD.data.get((self.itemId, self.idx), [])
        srcId = eData.get('materialNeed', (0,))[0][1]
        if srcId != dItem.id:
            if needReset:
                self.clearUpdateItemPos()
            return
        self.itemPos = pos
        self.itemPage = page
        self.itemUUID = dItem.uuid
        ret = self._createFormula(False)
        if len(ret) <= 0:
            return
        self.mediator.Invoke('setItemFormula', uiUtils.dict2GfxDict(ret, True))

    def clearUpdateItemPos(self):
        self.itemPos = -1
        self.itemPage = -1
        self.itemUUID = ''
        ret = self._createFormula(True)
        if len(ret) <= 0:
            return
        self.mediator.Invoke('setItemFormula', uiUtils.dict2GfxDict(ret, True))

    def _createFormula(self, needCheckNum = True):
        targetItemId = self.itemId
        idx = self.idx
        p = BigWorld.player()
        ret = {}
        eData = ESD.data.get((targetItemId, idx), [])
        if eData:
            items = eData.get('materialNeed', ())
            itemGroup = eData.get('materialSetNeed', ())
            material = []
            if not items:
                items = ()
            groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
            items += tuple(groupItems)
            self.hasEnh = False
            srcId = eData.get('materialNeed', (0,))[0][1]
            for itemSearchType, itemId, itemNum in items:
                iData = ID.data.get(itemId, {})
                iconPath = uiUtils.getItemIconFile64(itemId)
                quality = iData.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                maxNum = p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck, filterFunc=lambda it: utils.lvUpRideWingFilter(it, eData))
                if srcId == itemId:
                    hasEnh = False
                else:
                    hasEnh = p.inv.getItemHasEnhLv(itemId, itemNum)
                if hasEnh:
                    self.hasEnh = True
                material.append({'iconPath': iconPath,
                 'quality': color,
                 'maxNum': maxNum,
                 'needNum': itemNum,
                 'itemId': itemId})

            tData = ID.data.get(srcId, {})
            iconPath = uiUtils.getItemIconFile64(srcId)
            quality = tData.get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            maxNum = p.inv.countItemInPages(srcId, enableParentCheck=True, filterFunc=lambda it: utils.lvUpRideWingFilter(it, eData))
            needShowTip = False
            srcPage, srcPos = p.inv.findItemInPages(srcId)
            if maxNum == 1:
                self.itemPos = srcPos
                self.itemPage = srcPage
            if needCheckNum:
                if maxNum > 1:
                    maxNum = 0
                    needShowTip = True
                    self.itemPos = -1
                    self.itemPage = -1
                    self.itemUUID = ''
            elif maxNum > 1:
                maxNum = 1
            srcItem = {'iconPath': iconPath,
             'quality': color,
             'itemId': srcId,
             'needNum': 1,
             'maxNum': maxNum,
             'needShowTip': needShowTip,
             'srcPos': self.itemPos,
             'srcPage': self.itemPage}
            srcIt = None
            if self.itemPage != -1 and self.itemPos != -1:
                srcIt = p.inv.getQuickVal(self.itemPage, self.itemPos)
            if not srcIt:
                srcIt = Item(srcId)
            tData = ID.data.get(targetItemId, {})
            iconPath = 'item/icon64/%s.dds' % str(tData.get('icon', 'notFound'))
            quality = tData.get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            dstItem = {'iconPath': iconPath,
             'quality': color,
             'itemId': targetItemId}
            dstIt = Item(targetItemId)
            if self.npcFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
                srcProps = "<font color= \'#79C725\'>" + uiUtils.getItemPreprops(srcIt) + '</font>'
                dstProps = "<font color= \'#79C725\'>前缀属性随机</font>"
            else:
                srcProps = self._createPropsString(srcIt)
                dstProps = self._createPropsString(dstIt)
            ret = {'material': material,
             'srcItem': srcItem,
             'dstItem': dstItem,
             'srcProps': srcProps,
             'dstProps': dstProps}
        return ret

    def _createPropsString(self, i):
        ret = ''
        if hasattr(i, 'starLv'):
            starLv = i.starLv
        else:
            starLv = 0
        nextStarLv = starLv + 1 if starLv != -1 else -1
        starFactor = ESFCD.data.get(starLv, {}).get('factor', 1.0)
        nextStarFactor = ESFCD.data.get(nextStarLv, {}).get('factor', 1.0)
        quality = getattr(i, 'quality', 1)
        if not quality:
            quality = 1
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        basic = []
        if hasattr(i, 'props'):
            for pid, pType, pVal in i.props:
                if pType == gametypes.DATA_TYPE_NUM and i._isIntPropRef(pid):
                    basic.append((pid,
                     pType,
                     float2Int(pVal * starFactor * qualityFactor),
                     float2Int(pVal * (nextStarFactor - starFactor) * qualityFactor)))
                else:
                    basic.append((pid,
                     pType,
                     pVal * starFactor * qualityFactor,
                     pVal * (nextStarFactor - starFactor) * qualityFactor))

        basicProp = ''
        if basic:
            if ED.data[i.id]['equipType'] == 1:
                newBasic = []
                for item in basic:
                    if item[0] == 118:
                        basicProp += '物理攻击力  ' + str(item[2]) + '-'
                    elif item[0] == 119:
                        basicProp += str(item[2]) + '\n'
                    else:
                        newBasic.append(item)

                basic = newBasic
                newBasic = []
                for item in basic:
                    if item[0] == 120:
                        basicProp += '法术攻击力  ' + str(item[2]) + '-'
                    elif item[0] == 121:
                        basicProp += str(item[2]) + '\n'
                    else:
                        newBasic.append(item)

                basic = newBasic
            for item in basic:
                info = PRD.data[item[0]]
                basicProp += info['name'] + '  '
                if info['showType'] == 0:
                    basicProp += str(int(item[2]))
                elif info['showType'] == 2:
                    basicProp += str(round(item[2], 1))
                else:
                    basicProp += str(round(item[2] * 100, 1)) + '%'
                basicProp += '\n'

            ret += basicProp + '\n'
        prefixProp = ''
        if hasattr(i, 'preprops'):
            preprops = i.preprops
            preprops = [ tuple(list(pp) + [PRD.data[pp[0]]['priorityLevel'], PRD.data[pp[0]]['showColor'], pp[2] * (nextStarFactor - starFactor) * qualityFactor]) for pp in preprops ]
            preprops.sort(key=lambda k: k[3])
            for item in preprops:
                info = PRD.data[item[0]]
                prefixProp += "<font color = \'#73E539\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    prefixProp += "<font color = \'#BBFF99\'>+"
                elif info['type'] == 1:
                    prefixProp += "<font color = \'#BBFF99\'>-"
                if info['showType'] == 0:
                    prefixProp += str(float2Int(item[2] * starFactor * qualityFactor)) + '</font>'
                elif info['showType'] == 2:
                    prefixProp += str(round(item[2] * starFactor * qualityFactor, 1)) + '</font>'
                else:
                    prefixProp += str(round(item[2] * 100 * starFactor * qualityFactor, 1)) + '%</font>'
                prefixProp += '\n'

            ret += prefixProp + '\n'
        if not hasattr(i, 'preprops') and hasattr(i, 'preGroupList') and len(i.preGroupList) > 0:
            proGroupList = "<font color = \'#73E539\'>"
            proGroupList += '前缀属性随机'
            proGroupList += '</font>'
            proGroupList += '\n'
            ret += proGroupList + '\n'
        fixedProp = ''
        if hasattr(i, 'extraProps'):
            fixed = i.extraProps
            fixed = [ tuple(list(f) + [PRD.data[f[0]]['priorityLevel'], PRD.data[f[0]]['showColor'], f[2] * (nextStarFactor - starFactor) * qualityFactor]) for f in fixed ]
            fixed.sort(key=lambda k: k[3])
            for item in fixed:
                info = PRD.data[item[0]]
                fixedProp += "<font color = \'#2491FF\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    fixedProp += "<font color = \'#99CCFF\'>+"
                elif info['type'] == 1:
                    fixedProp += "<font color = \'#99CCFF\'>-"
                if info['showType'] == 0:
                    fixedProp += str(float2Int(item[2] * starFactor * qualityFactor)) + '</font>'
                elif info['showType'] == 2:
                    fixedProp += str(round(item[2] * starFactor * qualityFactor, 1)) + '</font>'
                else:
                    fixedProp += str(round(item[2] * 100 * starFactor * qualityFactor, 1)) + '%</font>'
                fixedProp += '\n'

            ret += fixedProp
        rand = []
        if hasattr(i, 'rprops'):
            for pid, pType, pVal in i.rprops:
                if pType == gametypes.DATA_TYPE_NUM and i._isIntPropRef(pid):
                    rand.append((pid,
                     pType,
                     float2Int(pVal * starFactor * qualityFactor),
                     float2Int(pVal * (nextStarFactor - starFactor) * qualityFactor)))
                else:
                    rand.append((pid,
                     pType,
                     pVal * starFactor * qualityFactor,
                     pVal * (nextStarFactor - starFactor) * qualityFactor))

            rand = [ tuple(list(r) + [PRD.data[r[0]]['priorityLevel'], PRD.data[r[0]]['showColor']]) for r in rand ]
            rand.sort(key=lambda k: k[4])
        if hasattr(i, 'randPropId') and len(rand) <= 0:
            randPropId = '\n'
            randPropId += "<font color = \'#2491FF\'>"
            randPropId += '额外属性随机'
            randPropId += '</font>'
            ret += randPropId + '\n'
        randProp = ''
        if rand:
            for item in rand:
                info = PRD.data[item[0]]
                randProp += "<font color = \'#2491FF\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    randProp += "<font color = \'#99CCFF\'>+"
                elif info['type'] == 1:
                    randProp += "<font color = \'#99CCFF\'>-"
                if info['showType'] == 0:
                    randProp += str(int(item[2])) + '</font>'
                elif info['showType'] == 2:
                    randProp += str(round(item[2], 1)) + '</font>'
                else:
                    randProp += str(round(item[2] * 100, 1)) + '%</font>'
                randProp += '\n'

            ret += randProp + '\n'
        extraSkill = ''
        ses = getattr(i, 'ses', None)
        if ses:
            for spId in ses:
                spData = ESPD.data.get(spId, {})
                extraSkill += '%s:%s\n' % (spData.get('name', ''), spData.get('desc', ''))

            ret += "\n<font color = \'#E89BFF\'>%s</font>" % extraSkill
        starPSkill = ''
        ed = ED.data.get(i.id, {})
        if ed.get('starSEffect', None):
            starLv = getattr(i, 'starLv', 0)
            if starLv < ed.get('starLvNeed', 0):
                pskill = ed['starSEffect']
                spData = ESPD.data.get(pskill, {})
                starPSkill += "<font color = \'#808080\'>%s:%s</font>\n" % (spData.get('name', ''), spData.get('desc', ''))
            ret += '\n%s' % starPSkill
        return ret

    def _cashInfo(self, itemId, idx):
        ret = {}
        p = BigWorld.player()
        fData = ESD.data.get((itemId, idx))
        if fData:
            cash = fData.get('cashNeed', 0)
        ret['needCash'] = str(cash)
        ret['bindCash'] = str(p.bindCash)
        ret['cash'] = str(p.cash)
        return ret

    def refresh(self):
        if self.mediator:
            ret = self._createFormula(False)
            if len(ret) <= 0:
                return
            self.mediator.Invoke('setItemFormula', uiUtils.dict2GfxDict(ret, True))
            if self.itemId is None or self.idx is None:
                return
            itemId = str(self.itemId)
            idx = str(self.idx)
            self.mediator.Invoke('updateCash', (GfxValue(itemId), GfxValue(idx)))

    def onGetItemList(self, *arg):
        ret = self._createItemList()
        return uiUtils.array2GfxAarry(ret, True)

    def onGetItemFormula(self, *arg):
        self.itemId = int(arg[3][0].GetString())
        self.idx = int(arg[3][1].GetString())
        self.itemPos = -1
        self.itemPage = -1
        self.itemUUID = ''
        ret = self._createFormula()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetOtherInfo(self, *arg):
        itemId = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        return uiUtils.dict2GfxDict(self._cashInfo(itemId, idx), True)

    @ui.callFilter(1)
    def onConfirm(self, *arg):
        itemId = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        triggerId = (self.itemId, idx)
        data = ESD.data.get(triggerId, [])
        if not data:
            return
        descStr = "进阶装备后将继承:<font color=\'#FF0000\'>"
        strArr = []
        if data.get('inheritStarExp', 0):
            strArr.append('升段经验')
        if data.get('inheritPrefixProp', 0):
            strArr.append('前缀属性')
        if data.get('inheritRandProp', 0):
            strArr.append('随机属性')
        if data.get('inheritExhanceLv', 0):
            strArr.append('精炼等级')
        if data.get('inheritExhanceJuexing', 0):
            strArr.append('精炼觉醒')
        if len(strArr) > 0 and self.npcFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP:
            for i in xrange(0, len(strArr)):
                descStr += strArr[i]
                if i != len(strArr) - 1:
                    descStr += '、'

            descStr += '</font>'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.doTrueCommitStep1, itemId, idx))
        else:
            self.doTrueCommitStep1(itemId, idx)

    def doTrueCommitStep1(self, itemId, idx):
        srcEquip = BigWorld.player().inv.getQuickVal(self.itemPage, self.itemPos)
        if self.npcFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP:
            self.doTrueCommitStep1_next(srcEquip, itemId, idx)
        elif self.npcFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
            self.doTrueCommitStep1_next2(srcEquip, itemId, idx)

    @ui.checkEquipCanReturn(1, GMDD.data.RETURN_BACK_EQUIP_LVUP)
    @ui.looseGroupTradeConfirm(1, GMDD.data.RETURN_BACK_EQUIP_LVUP)
    def doTrueCommitStep1_next(self, srcEquip, itemId, idx):
        if self.hasEnh:
            descStr = '进阶材料中有强化后的道具，\n是否确认进阶？\n如不想使用,请将该道具存入仓库'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.doTrueCommitStep2, itemId, idx))
        else:
            self.doTrueCommitStep2(itemId, idx)

    @ui.checkEquipCanReturn(1, GMDD.data.RETURN_BACK_EQUIP_WASH)
    @ui.looseGroupTradeConfirm(1, GMDD.data.RETURN_BACK_EQUIP_WASH)
    def doTrueCommitStep1_next2(self, srcEquip, itemId, idx):
        if self.hasEnh:
            descStr = '重铸材料中有强化后的道具，\n是否确认重铸？\n如不想使用,请将该道具存入仓库'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.doTrueCommitStep2, itemId, idx))
        else:
            self.doTrueCommitStep2(itemId, idx)

    def doTrueCommitStep2(self, itemId, idx):
        npcEnt = BigWorld.entities.get(self.entityId)
        ed = ED.data.get(self.itemId, {})
        if self.itemPage == const.CONT_NO_PAGE:
            return
        if self.npcFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP:
            maxEnhlv = ed.get('maxEnhlv', 0)
            srcEquip = BigWorld.player().inv.getQuickVal(self.itemPage, self.itemPos)
            if getattr(srcEquip, 'enhLv', -1) > maxEnhlv:
                descStr = '进化后的装备精炼等级上限低于当前装备的精炼等级，进化会导致装备的精炼等级下降，确认升阶吗？'
                descStr = GMD.data.get(GMDD.data.EQUIP_UPGRADE_ENHLV, {}).get('text', descStr)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self._doUpgradeEquipItem, self.itemPage, self.itemPos, itemId, idx))
            else:
                npcEnt and npcEnt.cell.upgradeEquipItem(self.itemPage, self.itemPos, itemId, idx)
        elif self.npcFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
            p = BigWorld.player()
            equipIt = p.inv.getQuickVal(self.itemPage, self.itemPos)
            if equipIt.isForeverBind():
                npcEnt and npcEnt.cell.resetEquipItem(self.itemPage, self.itemPos, itemId, idx)
            else:
                sData = ESD.data.get((itemId, idx))
                materialNeed, materialSetNeed = sData.get('materialNeed', ()), sData.get('materialSetNeed')
                removedItems = []
                bindPolicy, includeExpired, includeLatch, includeShihun = (gametypes.ITEM_REMOVE_POLICY_BIND_FIRST,
                 False,
                 False,
                 False)
                sd = ISSD.data.get(materialSetNeed, ())
                for d in sd:
                    itId = d.get('itemId', 0)
                    if itId == 0:
                        continue
                    attrId = d.get('attrId', None)
                    numRange = d.get('numRange', (0, 0))
                    itemSearchType = d.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT)
                    enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                    if attrId == None:
                        num = max(numRange)
                        rmItems = p.inv._searchItemCandidates(itId, num, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun)
                        for pg, ps in rmItems:
                            i = p.inv.getQuickVal(pg, ps)
                            removedItems.append(i)

                if any([ i.isForeverBind() for i in removedItems ]):
                    descStr = '重铸后装备将绑定，确认重铸吗？'
                    descStr = GMD.data.get(GMDD.data.RESET_EQUIP_PREFIX_BIND, {}).get('text', descStr)
                    npcEnt and gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(npcEnt.cell.resetEquipItem, self.itemPage, self.itemPos, itemId, idx))
                else:
                    npcEnt and npcEnt.cell.resetEquipItem(self.itemPage, self.itemPos, itemId, idx)

    def _doUpgradeEquipItem(self, srcItPage, srcItPos, itemId, idx):
        npcEnt = BigWorld.entities.get(self.entityId)
        npcEnt and npcEnt.cell.upgradeEquipItem(self.itemPage, self.itemPos, itemId, idx)

    def onClose(self, *arg):
        self.hide()

    def onGetFuncType(self, *arg):
        return GfxValue(self.npcFuncType)

    def onGotoWeb(self, *args):
        url = ''
        wupinId = args[3][0].GetNumber()
        if wupinId:
            url = SCD.data.get('WEB_WUPIN_SEARCH', uiConst.WEB_WUPIN_SEARCH)
            url = url % wupinId
        else:
            url = SCD.data.get('WEB_INDEX_SEARCH', uiConst.WEB_INDEX_SEARCH)
        BigWorld.openUrl(url)

    def onGetTips(self, *args):
        tips = GMD.data.get(GMDD.data.EQUIP_LV_UP_TIPS, {}).get('text', '可携带的前缀属性查询')
        self.gameOnOff()
        return GfxValue(gbk2unicode(tips))

    def gameOnOff(self):
        if gameglobal.rds.configData.get('enableEquipGotoWeb', False) and self.mediator:
            self.mediator.Invoke('gotoWebBtnVisible', GfxValue(True))
        else:
            self.mediator.Invoke('gotoWebBtnVisible', GfxValue(False))
