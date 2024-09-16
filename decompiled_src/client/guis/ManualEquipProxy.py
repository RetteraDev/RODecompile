#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ManualEquipProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import item
import events
import gametypes
import ui
import utils
from item import Item
from guis import uiConst
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from asObject import ASObject
from callbackHelper import Functor
from cdata import equip_special_props_data as ESPD
from cdata import equip_make_manual_dikou_data as EMMDD
from cdata import manual_equip_cost_data as MECD
from data import manual_equip_props_data as MEPD
from data import item_data as ID
from data import equip_data as ED
from cdata import item_synthesize_set_data as ISSD
from data import prop_ref_data as PRD
from data import sys_config_data as SCD
from data import equip_random_property_data as ERPD
from data import equip_property_pool_data as EPPD
from cdata import equip_quality_factor_data as EQFD
from data import formula_client_data as FCD
from cdata import game_msg_def_data as GMDD
MAIN_MATERIAL_TYPE_MAX_NUM = 3
BASIC_PROPS_DETAIL_SELECT_DEFAULT_HEIGHT = 50
BASIC_PROPS_DETAIL_LINE_HEIGHT = 22
RARE_PROPS_MAX_NUM = 3
RANDOM_RPOPS_MAX_NUM = 15
ALL_MAKE_TYPE_LIST = [Item.MAKE_TYPE_1, Item.MAKE_TYPE_2, Item.MAKE_TYPE_3]
OVERVIEW_INFO_PANEL = 'overviewInfo'
EQUIP_DETAIL_INFO_PANEL = 'equipDetailInfo'

class ManualEquipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ManualEquipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.lvRange = SCD.data.get('MANUAL_EQUIP_RANGE', ())
        self.showType = {1: gameStrings.TEXT_EQUIPMIXNEWPROXY_183,
         2: gameStrings.TEXT_EQUIPMIXNEWPROXY_185,
         3: gameStrings.TEXT_EQUIPMIXNEWPROXY_187}
        self.selectedEquipId = 0
        self.selectedEquipMc = None
        self.npcId = None
        self.curViewPanel = OVERVIEW_INFO_PANEL
        uiAdapter.registerEscFunc(uiConst.WIDGET_MANUAL_EQUIP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MANUAL_EQUIP:
            self.widget = widget
            self.initAllPanel()

    def show(self, npcId):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MANUAL_EQUIP)
        self.queryDiscountTime()

    def queryDiscountTime(self):
        if gameglobal.rds.configData.get('enableManualEquipMaterialDiscount', False):
            p = BigWorld.player()
            p.cell.syncMakeManualEquipDiscount()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MANUAL_EQUIP)

    def reset(self):
        self.widget = None
        self.selectedEquipId = 0
        self.selectedEquipMc = None
        self.npcId = None
        self.curViewPanel = OVERVIEW_INFO_PANEL

    @property
    def manualEquipRarePropHints(self):
        return SCD.data.get('ManualEquipRarePropsHints', ['',
         '',
         '',
         '',
         ''])

    def getLvRange(self, range):
        ret = []
        defaultLvIndex = 0
        p = BigWorld.player()
        index = 0
        for item in range:
            info = {'label': '%d-%d' % item,
             'data': item}
            ret.append(info)
            if item[0] <= p.lv <= item[1]:
                defaultLvIndex = index
            index = index + 1

        return (ret, defaultLvIndex)

    def getItemIcon(self, itemId):
        reqSchool = ID.data.get(itemId, {}).get('schReq', ())
        if BigWorld.player().school in reqSchool:
            state = uiConst.ITEM_NORMAL
        else:
            state = uiConst.EQUIP_BROKEN
        ret = uiUtils.getGfxItemById(itemId, appendInfo={'state': state})
        return ret

    def getEquipList(self, lvIndex, bMySchool):
        defaultSelectedEquipId = 0
        lvRange = self.lvRange[lvIndex]
        ret = []
        for showType, val in self.showType.items():
            node = {'name': val,
             'children': [],
             'equipType': showType}
            ret.append(node)

        for equip in MECD.data.iterkeys():
            equipType = ED.data.get(equip, {}).get('equipType', 0)
            reqLv = ID.data.get(equip, {}).get('lvReq', 0)
            reqSchool = ID.data.get(equip, {}).get('schReq', ())
            if bMySchool and BigWorld.player().school not in reqSchool:
                continue
            for nodeItem in ret:
                if nodeItem['equipType'] == equipType and lvRange[0] <= reqLv <= lvRange[1]:
                    nodeItem['children'].append(equip)
                    defaultSelectedEquipId = equip if not defaultSelectedEquipId else defaultSelectedEquipId

        for nodeItem in ret:
            nodeItem['children'].sort(key=lambda k: MECD.data.get(k, {}).get('priorityLevel', 0))

        return (ret, defaultSelectedEquipId)

    def getEquipItemDataById(self, equipId):
        manualEquipTypeMap = SCD.data.get('manualEquipTypeMap')
        manualEquipData = MECD.data.get(equipId, {})
        equipData = ED.data.get(equipId, {})
        itemData = ID.data.get(equipId, {})
        priorityLevel = manualEquipData.get('priorityLevel', 0)
        equipType = equipData.get('equipType', 0)
        name = itemData.get('name', '')
        reqLv = itemData.get('lvReq', 0)
        subcategory = itemData.get('subcategory', 0)
        icon = self.getItemIcon(equipId)
        subType = manualEquipTypeMap.get(equipType, {}).get(subcategory, '')
        equipItemData = {'name': name,
         'reqLv': reqLv,
         'icon': icon,
         'itemId': equipId,
         'equipType': equipType,
         'priorityLevel': priorityLevel,
         'subType': subType}
        return equipItemData

    def getEquipListDefaultExpandIdx(self, equipListTreeData):
        if not equipListTreeData:
            return None
        else:
            for idx, treeHead in enumerate(equipListTreeData):
                if len(treeHead.get('children', [])) > 0:
                    return idx

            return None

    def getMainMaterial(self, materialSetID, onlyBooks = False):
        p = BigWorld.player()
        sd = ISSD.data.get(materialSetID, None)
        material = []
        if sd != None:
            for d in sd:
                itemId = d.get('itemId', 0)
                if itemId == 0:
                    continue
                if onlyBooks and self.canTianBiDikou(itemId):
                    continue
                numRange = d.get('numRange', (0, 0))
                needCount = numRange[1]
                costInfo = self.getItemInfo(itemId, needCount)
                isEnough = self.isItemEnough(itemId, needCount)
                itemName = ID.data.get(itemId, {}).get('name', '')
                itemLv = str(ID.data.get(itemId, {}).get('lvReq', '')) + gameStrings.TEXT_MANUALEQUIPPROXY_171
                material.append((costInfo,
                 itemName,
                 itemLv,
                 isEnough))

        return material

    def canTianBiDikou(self, itemId):
        return bool(EMMDD.data.get(itemId, {}))

    def isItemEnough(self, itemId, needCount):
        p = BigWorld.player()
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        isEnough = True
        if needCount > ownCount:
            isEnough = False
        return isEnough

    def getItemInfo(self, itemId, needCount):
        p = BigWorld.player()
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if ownCount < needCount:
            countStr = "<font color=\'#ff0000\'>" + str(ownCount) + '/' + str(needCount) + '</font>'
        else:
            countStr = str(ownCount) + '/' + str(needCount)
        itemInfo = uiUtils.getGfxItemById(itemId, appendInfo={'count': countStr})
        return itemInfo

    def getTianBiDiKou(self, tianBiNeed):
        p = BigWorld.player()
        TianBi = p.unbindCoin + p.bindCoin + p.freeCoin
        if TianBi < tianBiNeed:
            countStr = uiUtils.toHtml(str(TianBi) + '/' + str(tianBiNeed), '#ff0000')
            self.isTianBiEnough = False
        else:
            countStr = str(TianBi) + '/' + str(tianBiNeed)
            self.isTianBiEnough = True
        return countStr

    def getOtherCost(self, extraCost, makeType):
        if extraCost:
            itemId, needCount = extraCost[makeType - 1]
            itemInfo = self.getItemInfo(itemId, needCount)
            itemName = ID.data.get(itemId, {}).get('name', '')
            isEnough = self.isItemEnough(itemId, needCount)
            return [itemInfo, itemName, isEnough]
        else:
            return []

    def getNeedStr(self, key, cashNeed):
        p = BigWorld.player()
        if getattr(p, key, 0) < cashNeed:
            cashStr = "<font color=\'#ff0000\'>" + str(cashNeed / 10.0) + '</font>'
        else:
            cashStr = str(cashNeed / 10.0)
        return cashStr

    def getCashStr(self, cashNeed):
        p = BigWorld.player()
        if getattr(p, 'cash', 0) < cashNeed:
            cashStr = "<font color=\'#ff0000\'>" + str(cashNeed) + '</font>'
        else:
            cashStr = str(cashNeed)
        return cashStr

    def getBasicProps(self, equipId):
        ret = {}
        basicProps = MEPD.data.get(equipId, {}).get('basicProps', ())
        quality = ID.data.get(equipId, {}).get('quality', 0)
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        for makeType, makeProps in enumerate(basicProps):
            for prop in makeProps:
                pId = prop[0]
                prd = PRD.data.get(pId, {})
                propName = prd.get('name', '')
                showType = prd.get('showType', 0)
                val1 = prop[2] * qualityFactor
                val2 = prop[3] * qualityFactor
                val1 = uiUtils.formatProp(val1, 0, showType)
                val2 = uiUtils.formatProp(val2, 0, showType)
                if pId not in ret:
                    ret[pId] = {'name': propName,
                     'makeTypePropData': {}}
                ret[pId]['makeTypePropData'][makeType] = (val1, val2)

        return ret

    def getExtraPools(self, equipId):
        extraPools = MEPD.data.get(equipId, {}).get('extraPools', [])
        quality = ID.data.get(equipId, {}).get('quality', 0)
        attrArrs = []
        for poolId in extraPools:
            attrNum = 0
            attrIds = []
            attrArr = []
            typeInfo = {}
            pools = ERPD.data.get((poolId, quality), [])[0].get('pool', [])
            for pool in pools:
                attrNum = attrNum + pool[1]
                attrDatas = EPPD.data.get(pool[0])
                for attrData in attrDatas:
                    attrId, attr = self.getAttrByData(equipId, attrData)
                    if attrId and attrId not in attrIds:
                        attrArr.append(attr)
                        attrIds.append(attrId)

            typeInfo['num'] = attrNum
            typeInfo['attrs'] = attrArr
            attrArrs.append(typeInfo)

        return attrArrs

    def getRareProps(self, equipId):
        rarePropResult = []
        rarePropIds = MECD.data.get(equipId, {}).get('rarePropIds', [])
        for rarePropId in rarePropIds:
            rarePropData = ESPD.data.get(rarePropId, {})
            if not rarePropData:
                continue
            rarePropResult.append([rarePropData.get('name', ''), rarePropData.get('desc', '')])

        return rarePropResult

    def getRareMaxExpProps(self, equipId):
        rareMaxExpPropResult = []
        rareMaxExpPropIds = MECD.data.get(equipId, {}).get('rareMaxExpPropIds', [])
        for rareMaxExpPropId in rareMaxExpPropIds:
            rareMaxExpPropData = ESPD.data.get(rareMaxExpPropId, {})
            if not rareMaxExpPropData:
                continue
            rareMaxExpPropResult.append([rareMaxExpPropData.get('name', ''), rareMaxExpPropData.get('desc', '')])

        return rareMaxExpPropResult

    def getEquipDetail(self, equipId, makeType):
        ret = {}
        materialSetNeed = MECD.data.get(equipId, {}).get('materialSetNeed', 0)
        remainDiscountTime = self.getMaterialDiscountTime()
        extraCostDiscount = MECD.data.get(equipId, {}).get('extraCostDiscount', [])
        if remainDiscountTime and extraCostDiscount:
            extraCost = MECD.data.get(equipId, {}).get('extraCostDiscount')
        else:
            extraCost = MECD.data.get(equipId, {}).get('extraCost')
        cashNeed = MECD.data.get(equipId, {}).get('cashNeed', 0)
        mentalNeed = MECD.data.get(equipId, {}).get('mentalNeed', 0)
        labourNeed = MECD.data.get(equipId, {}).get('labourNeed', 0)
        equipName = ID.data.get(equipId, {}).get('name', '')
        ret['mainCost'] = self.getMainMaterial(materialSetNeed)
        ret['TianBiNeed'] = self.getMainTianBiNeed(materialSetNeed)
        if makeType > 0:
            otherCost = self.getOtherCost(extraCost, makeType)
            if remainDiscountTime and extraCostDiscount and otherCost:
                otherCost[0]['cornerMark'] = 'cheap'
            ret['otherCost'] = otherCost
            ret['TianBiNeed'] += self.getOtherTianBiNeed(extraCost, makeType)
        else:
            ret['otherCost'] = []
        ret['cash'] = self.getCashStr(cashNeed)
        ret['mentalNeed'] = self.getNeedStr('mental', mentalNeed)
        ret['labourNeed'] = self.getNeedStr('labour', labourNeed)
        ret['equipName'] = equipName
        ret['basicProps'] = self.getBasicProps(equipId)
        ret['extraPools'] = self.getExtraPools(equipId)
        ret['iconPath'] = uiUtils.getItemIconPath(equipId)
        ret['discountInfo'] = self.getDiscountInfo(makeType) if extraCostDiscount else []
        ret['rareProps'] = self.getRareProps(equipId)
        ret['rareMaxExpProps'] = self.getRareMaxExpProps(equipId)
        ret['haveMakeBook'] = self.checkMakeBook(materialSetNeed)
        return ret

    def getDiscountInfo(self, makeType):
        if not gameglobal.rds.configData.get('enableManualEquipMaterialDiscount', False) or makeType <= 0:
            return []
        totalTime = SCD.data.get('makeManualEquipDiscountWeeklyCnt', 0)
        return [self.getMaterialDiscountTime(), totalTime]

    def getMaterialDiscountTime(self):
        if not gameglobal.rds.configData.get('enableManualEquipMaterialDiscount', False):
            return 0
        p = BigWorld.player()
        totalTime = SCD.data.get('makeManualEquipDiscountWeeklyCnt', 0)
        return max(0, totalTime - getattr(p, 'manualEquipDiscount', 0))

    def getOtherTianBiNeed(self, extraCost, makeType):
        if extraCost:
            itemId, needCount = extraCost[makeType - 1]
            p = BigWorld.player()
            ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if ownCount < needCount:
                return EMMDD.data.get(itemId, {}).get('coin', 0) * (needCount - ownCount)
        return 0

    def checkMakeBook(self, materialSetID):
        sum = 0
        sd = ISSD.data.get(materialSetID, None)
        if sd == None:
            return False
        itemId = sd[0].get('itemId', 0)
        if itemId == 0:
            return False
        numRange = sd[0].get('numRange', (0, 0))
        needCount = numRange[1]
        p = BigWorld.player()
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if ownCount < needCount:
            return False
        else:
            return True

    def getMainTianBiNeed(self, materialSetID):
        sum = 0
        sd = ISSD.data.get(materialSetID, None)
        if sd == None:
            return
        else:
            for d in sd:
                itemId = d.get('itemId', 0)
                if itemId == 0:
                    continue
                numRange = d.get('numRange', (0, 0))
                needCount = numRange[1]
                p = BigWorld.player()
                ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
                if ownCount < needCount:
                    sum += EMMDD.data.get(itemId, {}).get('coin', 0) * (needCount - ownCount)

            return sum

    def getAttrByData(self, equipId, attrData):
        it = item.Item(equipId)
        value = attrData.get('value', [])
        aid, atype, transType, amax, amin, pmin, pmax = value
        attrName = PRD.data.get(aid, {}).get('shortName', '')
        showType = PRD.data.get(aid, {}).get('showType', 0)
        quality = ID.data.get(equipId, {}).get('quality', 0)
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        if transType != gametypes.PROPERTY_RAND_ABS:
            fd = FCD.data.get(transType)
            if not fd:
                return (None, None)
            formula = fd.get('formula')
            if not formula:
                return (None, None)
            amin = it.evalValue(transType, pmin)
            amax = it.evalValue(transType, pmax)
        amin = amin * qualityFactor
        amax = amax * qualityFactor
        val1 = uiUtils.formatProp(amin, 0, showType)
        val2 = uiUtils.formatProp(amax, 0, showType)
        return [aid, [attrName, val1, val2]]

    def selectEquip(self, equipItemMc):
        if self.selectedEquipMc:
            self.selectedEquipMc.selected = False
        self.selectedEquipId = int(equipItemMc.equipId)
        self.selectedEquipMc = equipItemMc
        self.selectedEquipMc.selected = True
        self.refreshDetailInfo()

    def initAllPanel(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.makeType1.selected = True
        self.widget.makeType1.group.setSelectedButtonByIndex(Item.MAKE_TYPE_1, True)
        rangeData, defaultLvIndex = self.getLvRange(self.lvRange)
        ASUtils.setDropdownMenuData(self.widget.dropList, rangeData)
        self.widget.dropList.selectedIndex = defaultLvIndex
        self.widget.dropList.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleSelectLvRange, False, 0, True)
        self.widget.onlyMySchool.selected = True
        self.widget.onlyMySchool.addEventListener(events.EVENT_SELECT, self.handleSelectMySchool, False, 0, True)
        equipDataList, self.selectedEquipId = self.getEquipList(self.widget.dropList.selectedIndex, self.widget.onlyMySchool.selected)
        treeExpandIdx = self.getEquipListDefaultExpandIdx(equipDataList)
        self.widget.equipList.tree.itemRenderers = ['ManualEquip_FirstItem', 'ManualEquip_TreeItem']
        self.widget.equipList.tree.itemHeights = [26, 74]
        self.widget.equipList.tree.lvItemGap = 0
        self.widget.equipList.tree.labelFunction = self.setTreeItem
        self.widget.equipList.tree.onlyOneExpand = True
        self.widget.equipList.tree.dataArray = equipDataList
        self.widget.equipList.tree.selectData = equipDataList[treeExpandIdx].get('children')[0]
        self.widget.equipList.scrollToHead()
        self.widget.equipList.tree.validateNow()
        self.refreshDetailInfo()

    def refreshDetailInfo(self):
        if not self.widget:
            return
        curSelectedMakeType = int(self.widget.makeType1.group.selectedIndex)
        detailData = self.getEquipDetail(self.selectedEquipId, curSelectedMakeType)
        if self.curViewPanel == OVERVIEW_INFO_PANEL:
            self.widget.content.gotoAndStop(OVERVIEW_INFO_PANEL)
            self.setOverviewInfo(detailData)
        elif self.curViewPanel == EQUIP_DETAIL_INFO_PANEL:
            self.widget.content.gotoAndStop(EQUIP_DETAIL_INFO_PANEL)
            self.setEquipDetailInfo(detailData)
        self.setOtherInfo(detailData)

    def showSuccAni(self):
        self.widget.effect.gotoAndPlay('succ')
        self.widget.effect.guangmang.gotoAndPlay(1)

    def addChildMcByPosY(self, parentMc, childMc, posY, offset = 10):
        if not parentMc or not childMc:
            return 0
        parentMc.addChild(childMc)
        childMc.y = posY
        return childMc.y + childMc.height + offset

    def refreshEquipList(self):
        if self.selectedEquipMc:
            self.selectedEquipMc.selected = False
            self.selectedEquipMc = None
            self.selectedEquipId = 0
        equipDataList, self.selectedEquipId = self.getEquipList(self.widget.dropList.selectedIndex, self.widget.onlyMySchool.selected)
        treeExpandIdx = self.getEquipListDefaultExpandIdx(equipDataList)
        self.widget.equipList.tree.dataArray = equipDataList
        self.widget.equipList.tree.selectData = equipDataList[treeExpandIdx].get('children')[0]
        self.widget.equipList.scrollToHead()
        self.widget.equipList.tree.validateNow()

    def setTreeItem(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        if isFirst:
            itemMc.desc.label = ASObject(args[3][1]).name
        else:
            equipId = int(args[3][1].GetNumber())
            data = self.getEquipItemDataById(equipId)
            itemMc.itemName.text = data['name']
            itemMc.lvDesc.text = gameStrings.MANUAL_EQUIP_ITEM_LV_DESC % data['reqLv']
            itemMc.slot.setItemSlotData(data['icon'])
            itemMc.subType.text = data['subType']
            itemMc.slot.dragable = False
            itemMc.mouseChildren = True
            itemMc.equipId = data['itemId']
            itemMc.equipType = data['equipType']
            itemMc.validateNow()
            if self.selectedEquipId and self.selectedEquipId == data['itemId']:
                self.selectEquip(itemMc)
            itemMc.addEventListener(events.BUTTON_CLICK, self.clickEquip, False, 0, True)

    def setOtherInfo(self, detailData):
        self.widget.equipName.text = detailData.get('equipName', '')
        self.widget.effect.icon.loadImage(detailData.get('iconPath', ''))
        self.widget.upIcon.visible = self.checkCurIsNewLvSelectedIdx()
        TipManager.addTip(self.widget.upIcon, self.manualEquipRarePropHints[4])
        manualMakeTypeTxt = SCD.data.get('MANUAL_MAKE_TYPE', [])
        for idx, makeType in enumerate(ALL_MAKE_TYPE_LIST):
            self.widget.getChildByName('makeType%d' % (idx + 1)).label = manualMakeTypeTxt[makeType]
            self.widget.getChildByName('makeType%d' % (idx + 1)).addEventListener(events.EVENT_SELECT, self.handleSelectMakeType, False, 0, True)

    def checkCurIsNewLvSelectedIdx(self):
        if not self.widget:
            return False
        return self.widget.dropList.selectedIndex == len(self.lvRange) - 1

    def setEquipDetailInfo(self, detailData):
        curSelectedMakeType = int(self.widget.makeType1.group.selectedIndex)
        equipDetailPanelMc = self.widget.content.equipDetailPanel
        canvas = equipDetailPanelMc.equipDetailInfoScroll.canvas
        while canvas.numChildren > 0:
            canvas.removeChildAt(0)

        equipDetailPanelMc.returnBtn.addEventListener(events.BUTTON_CLICK, self.clickReturn, False, 0, True)
        curCanvasHeight = 0
        basicProps = detailData.get('basicProps', {})
        if len(basicProps) > 0:
            basicPropsMc = self.widget.getInstByClsName('ManualEquip_BasicPropsDetail')
            manualMakeTypeTxt = SCD.data.get('MANUAL_MAKE_TYPE', [])
            for idx, makeType in enumerate(ALL_MAKE_TYPE_LIST):
                basicPropsMc.detailMakeTypeAll.getChildByName('detailMakeType%d' % idx).textField.text = manualMakeTypeTxt[makeType]

            basicPropsDetailSelectMc = self.widget.getInstByClsName('ManualEquip_BasicPropsDetailSelect')
            self.addChildMcByPosY(basicPropsMc, basicPropsDetailSelectMc, 0, offset=0)
            basicPropsDetailSelectMc.height = BASIC_PROPS_DETAIL_SELECT_DEFAULT_HEIGHT + BASIC_PROPS_DETAIL_LINE_HEIGHT * len(basicProps)
            for makeType in xrange(len(ALL_MAKE_TYPE_LIST)):
                detailMakeTypeSelMc = basicPropsDetailSelectMc.getChildByName('detailMakeTypeSel%d' % makeType)
                if makeType == curSelectedMakeType:
                    detailMakeTypeSelMc.visible = True
                    detailMakeTypeSelMc.gotoAndPlay(0)
                else:
                    detailMakeTypeSelMc.visible = False

            propIdx = 0
            curDetailLineHeight = basicPropsMc.detailMakeTypeAll.y + basicPropsMc.detailMakeTypeAll.height
            for basicProp in basicProps.itervalues():
                if propIdx % 2 == 0:
                    detailLineMc = self.widget.getInstByClsName('ManualEquip_BasicPropsDetailLine')
                else:
                    detailLineMc = self.widget.getInstByClsName('ManualEquip_BasicPropsDetailLineWithBg')
                detailLineMc.attr.textField.text = basicProp.get('name', '')
                makeTypePropData = basicProp.get('makeTypePropData', {})
                for makeType, basicPropData in makeTypePropData.iteritems():
                    valMc = detailLineMc.getChildByName('val%d' % makeType)
                    if makeType != Item.MAKE_TYPE_1:
                        valMc.textField.htmlText = "<font color=\'#6de539\'>%s</font>~%s" % (basicPropData[0], basicPropData[1])
                    else:
                        valMc.textField.text = '%s~%s' % (basicPropData[0], basicPropData[1])

                propIdx += 1
                curDetailLineHeight = self.addChildMcByPosY(basicPropsMc, detailLineMc, curDetailLineHeight, offset=0)

            curCanvasHeight = self.addChildMcByPosY(canvas, basicPropsMc, curCanvasHeight)
        rareProps = detailData.get('rareProps', [])
        if len(rareProps) > 0 and curSelectedMakeType == Item.MAKE_TYPE_3:
            rareProps0Mc = self.setRarePropsInfo(rareProps, 'ManualEquip_RarePropsDetail', 'ManualEquip_RarePropsDetailLine', self.manualEquipRarePropHints[0], self.manualEquipRarePropHints[1], needShowVal=True, fontTxt="<font color=\'#ffc961\'>%s</font>")
            curCanvasHeight = self.addChildMcByPosY(canvas, rareProps0Mc, curCanvasHeight)
        rareMaxExpProps = detailData.get('rareMaxExpProps', [])
        if len(rareMaxExpProps) > 0 and curSelectedMakeType == Item.MAKE_TYPE_3:
            rareProps1Mc = self.setRarePropsInfo(rareMaxExpProps, 'ManualEquip_RarePropsDetail', 'ManualEquip_RarePropsDetailLine', self.manualEquipRarePropHints[2], self.manualEquipRarePropHints[3], needShowVal=True, fontTxt="<font color=\'#CA7FFF\'>%s</font>")
            curCanvasHeight = self.addChildMcByPosY(canvas, rareProps1Mc, curCanvasHeight)
        randomPropsMc = self.widget.getInstByClsName('ManualEquip_RandomPropsDetail')
        self.addChildMcByPosY(canvas, randomPropsMc, curCanvasHeight)
        randomAttrs = detailData.get('extraPools', [])[curSelectedMakeType].get('attrs', [])
        randomPropsMc.extraPropDesc.textField.htmlText = gameStrings.MANUAL_EQUIP_RANDOM_PROPS_HINT % detailData.get('extraPools', [])[curSelectedMakeType].get('num', [])
        for idx in xrange(RANDOM_RPOPS_MAX_NUM):
            randomAttrMc = randomPropsMc.getChildByName('randomAttr%d' % idx)
            randomVal = randomPropsMc.getChildByName('randomVal%d' % idx)
            if idx < len(randomAttrs):
                propData = randomAttrs[idx]
                randomAttrMc.visible = True
                randomVal.visible = True
                randomAttrMc.textField.text = propData[0]
                randomVal.textField.text = '%s~%s' % (propData[1], propData[2])
            else:
                randomAttrMc.visible = False
                randomVal.visible = False

        equipDetailPanelMc.equipDetailInfoScroll.validateNow()
        equipDetailPanelMc.equipDetailInfoScroll.refreshHeight()

    def setOverviewInfo(self, detailData):
        self.setEquipOverviewInfo(detailData)
        self.setMaterialOverviewInfo(detailData)

    def setEquipOverviewInfo(self, detailData):
        curSelectedMakeType = int(self.widget.makeType1.group.selectedIndex)
        equipOverviewPanelMc = self.widget.content.equipOverviewPanel
        canvas = equipOverviewPanelMc.equipOverviewInfoScroll.canvas
        while canvas.numChildren > 0:
            canvas.removeChildAt(0)

        equipOverviewPanelMc.detailBtn.addEventListener(events.BUTTON_CLICK, self.clickDetail, False, 0, True)
        curCanvasHeight = 0
        basicProps = detailData.get('basicProps', [])
        if len(basicProps) > 0:
            basicPropsMc = self.widget.getInstByClsName('ManualEquip_BasicProps')
            manualMakeTypeTxt = SCD.data.get('MANUAL_MAKE_TYPE', [])
            basicPropsMc.makeType.gotoAndStop('a%d' % curSelectedMakeType)
            basicPropsMc.makeType.textField.text = manualMakeTypeTxt[curSelectedMakeType]
            propIdx = 0
            curDetailLineHeight = basicPropsMc.makeType.y + basicPropsMc.makeType.height
            for basicProp in basicProps.itervalues():
                if propIdx % 2 == 0:
                    detailLineMc = self.widget.getInstByClsName('ManualEquip_BasicPropsLine')
                else:
                    detailLineMc = self.widget.getInstByClsName('ManualEquip_BasicPropsLineWithBg')
                detailLineMc.attr.textField.text = basicProp.get('name', '')
                basicPropData = basicProp.get('makeTypePropData', {}).get(curSelectedMakeType, (0, 0))
                if curSelectedMakeType != Item.MAKE_TYPE_1:
                    detailLineMc.val.textField.htmlText = "<font color=\'#6de539\'>%s</font>~%s" % (basicPropData[0], basicPropData[1])
                else:
                    detailLineMc.val.textField.text = '%s~%s' % (basicPropData[0], basicPropData[1])
                propIdx += 1
                curDetailLineHeight = self.addChildMcByPosY(basicPropsMc, detailLineMc, curDetailLineHeight, offset=0)

            curCanvasHeight = self.addChildMcByPosY(canvas, basicPropsMc, 0)
        rareProps = detailData.get('rareProps', [])
        if len(rareProps) > 0 and curSelectedMakeType == Item.MAKE_TYPE_3:
            rareProps0Mc = self.setRarePropsInfo(rareProps, 'ManualEquip_RareProps', 'ManualEquip_RarePropsLine', self.manualEquipRarePropHints[0], self.manualEquipRarePropHints[1], needShowVal=False, fontTxt="<font color=\'#ffc961\'>%s</font>")
            curCanvasHeight = self.addChildMcByPosY(canvas, rareProps0Mc, curCanvasHeight)
        rareMaxExpProps = detailData.get('rareMaxExpProps', [])
        if len(rareMaxExpProps) > 0 and curSelectedMakeType == Item.MAKE_TYPE_3:
            rareProps1Mc = self.setRarePropsInfo(rareMaxExpProps, 'ManualEquip_RareProps', 'ManualEquip_RarePropsLine', self.manualEquipRarePropHints[2], self.manualEquipRarePropHints[3], needShowVal=False, fontTxt="<font color=\'#CA7FFF\'>%s</font>")
            curCanvasHeight = self.addChildMcByPosY(canvas, rareProps1Mc, curCanvasHeight)
        randomPropsMc = self.widget.getInstByClsName('ManualEquip_RandomProps')
        self.addChildMcByPosY(canvas, randomPropsMc, curCanvasHeight)
        randomAttrs = detailData.get('extraPools', [])[curSelectedMakeType].get('attrs', [])
        randomPropsMc.extraPropDesc.textField.htmlText = gameStrings.MANUAL_EQUIP_RANDOM_PROPS_HINT % detailData.get('extraPools', [])[curSelectedMakeType].get('num', [])
        for idx in xrange(RANDOM_RPOPS_MAX_NUM):
            randomAttrMc = randomPropsMc.getChildByName('randomAttr%d' % idx)
            if idx < len(randomAttrs):
                propData = randomAttrs[idx]
                randomAttrMc.visible = True
                randomAttrMc.textField.text = propData[0]
            else:
                randomAttrMc.visible = False

        equipOverviewPanelMc.equipOverviewInfoScroll.validateNow()
        equipOverviewPanelMc.equipOverviewInfoScroll.refreshHeight()

    def setRarePropsInfo(self, rarePropsData, parentMcName, childMcName, hint0Txt, hint1Txt, needShowVal = False, fontTxt = '%d'):
        rarePropsMc = self.widget.getInstByClsName(parentMcName)
        rarePropsMc.hint0.htmlText = hint0Txt
        rarePropsMc.hint1.htmlText = hint1Txt
        rarePropsLineMcPosY = rarePropsMc.height
        rarePropsLineMc = None
        for idx, rarePropData in enumerate(rarePropsData):
            if idx % RARE_PROPS_MAX_NUM == 0:
                rarePropsLineMc = self.widget.getInstByClsName(childMcName)
                rarePropsLineMcPosY = self.addChildMcByPosY(rarePropsMc, rarePropsLineMc, rarePropsLineMcPosY, offset=0)
            propMcIdx = idx % RARE_PROPS_MAX_NUM
            attrMc = rarePropsLineMc.getChildByName('attr%d' % propMcIdx)
            attrMc.visible = True
            attrMc.textField.htmlText = fontTxt % rarePropData[0]
            if needShowVal and rarePropData[1]:
                valMc = rarePropsLineMc.getChildByName('val%d' % propMcIdx)
                valMc.visible = True
                valMc.textField.htmlText = fontTxt % uiUtils.getShortStr(rarePropData[1], valMc.textField.length - 1)
                if uiUtils.checkStrOverLen(rarePropData[1], valMc.textField.length):
                    TipManager.addTip(attrMc, rarePropData[1])
                    TipManager.addTip(valMc, rarePropData[1])

        return rarePropsMc

    def setMaterialOverviewInfo(self, detailData):
        materialPanelMc = self.widget.content.materialOverviewPanel
        curSelectedMakeType = int(self.widget.makeType1.group.selectedIndex)
        manualMakeTypeTxt = SCD.data.get('MANUAL_MAKE_TYPE', [])
        materialPanelMc.makeBtn.addEventListener(events.BUTTON_CLICK, self.clickMake, False, 0, True)
        materialPanelMc.makeBtn.label = manualMakeTypeTxt[curSelectedMakeType]
        mainMaterialCostData = detailData.get('mainCost', [])
        for idx in xrange(MAIN_MATERIAL_TYPE_MAX_NUM):
            mainMaterialMc = materialPanelMc.getChildByName('mainMaterial%d' % idx)
            if idx < len(mainMaterialCostData):
                mainMaterialMc.visible = True
                mainMaterialMc.slot.setItemSlotData(mainMaterialCostData[idx][0])
                mainMaterialMc.itemName.text = mainMaterialCostData[idx][1]
                if not mainMaterialCostData[idx][3]:
                    mainMaterialMc.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
                else:
                    mainMaterialMc.slot.setSlotState(uiConst.ITEM_NORMAL)
            else:
                mainMaterialMc.visible = False

        otherCost = detailData.get('otherCost', [])
        if len(otherCost) > 0:
            materialPanelMc.otherMaterial.setItemSlotData(otherCost[0])
            materialPanelMc.otherMaterialName.text = otherCost[1]
            if not otherCost[2]:
                materialPanelMc.otherMaterial.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            else:
                materialPanelMc.otherMaterial.setSlotState(uiConst.ITEM_NORMAL)
            discountInfo = detailData.get('discountInfo', [])
            if len(discountInfo) > 0:
                materialPanelMc.discountText.visible = True
                materialPanelMc.discountVal.text = '%d/%d' % (discountInfo[0], discountInfo[1])
            else:
                materialPanelMc.discountText.visible = False
                materialPanelMc.discountVal.text = ''
        else:
            materialPanelMc.discountText.visible = False
            materialPanelMc.discountVal.text = ''
        materialPanelMc.cash.htmlText = detailData.get('cash', '')
        materialPanelMc.mental.htmlText = detailData.get('mentalNeed', '')
        materialPanelMc.labour.htmlText = detailData.get('labourNeed', '')
        if curSelectedMakeType == Item.MAKE_TYPE_1:
            materialPanelMc.otherMaterial.visible = False
            materialPanelMc.otherMaterialName.visible = False
            materialPanelMc.otherMaterialLabel.visible = False
        else:
            materialPanelMc.otherMaterial.visible = True
            materialPanelMc.otherMaterialName.visible = True
            materialPanelMc.otherMaterialLabel.visible = True
        materialPanelMc.diKou.checkBox.selected = True
        materialPanelMc.diKou.tianBi.btn.addEventListener(events.BUTTON_CLICK, self.handlePay, False, 0, True)
        self.tianBiDiKou = self.getTianBiDiKou(detailData.get('TianBiNeed', 0))
        materialPanelMc.diKou.tianBi.value.htmlText = self.tianBiDiKou
        self.isHaveMakeBook = detailData.get('haveMakeBook', False)

    def handlePay(self, *args):
        BigWorld.player().openRechargeFunc()

    def handleSelectMySchool(self, *args):
        self.refreshEquipList()

    def handleSelectMakeType(self, *args):
        self.refreshDetailInfo()

    def handleSelectLvRange(self, *args):
        self.refreshEquipList()

    def clickEquip(self, *args):
        equipItemMc = ASObject(args[3][0]).currentTarget
        self.selectEquip(equipItemMc)
        self.refreshDetailInfo()

    def clickDetail(self, *args):
        self.curViewPanel = EQUIP_DETAIL_INFO_PANEL
        self.refreshDetailInfo()

    def clickReturn(self, *args):
        self.curViewPanel = OVERVIEW_INFO_PANEL
        self.refreshDetailInfo()

    def clickMake(self, *args):
        if self.npcId != None:
            curSelectedMakeType = int(self.widget.makeType1.group.selectedIndex)
            reqSchool = ID.data.get(self.selectedEquipId, {}).get('schReq', ())
            if BigWorld.player().school not in reqSchool:
                msg = uiUtils.getTextFromGMD(GMDD.data.MANUAL_EQUIP_NOT_SCHOOL, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realMakeEquip, self.selectedEquipId, curSelectedMakeType))
            else:
                self.realMakeEquip(self.selectedEquipId, curSelectedMakeType)

    def realMakeEquip(self, equipId, makeType):
        p = BigWorld.player()
        mentalNeed = MECD.data.get(equipId, {}).get('mentalNeed', 0)
        labourNeed = MECD.data.get(equipId, {}).get('labourNeed', 0)
        if labourNeed > getattr(p, 'labour', 0):
            p.showGameMsg(GMDD.data.MAKE_EQUIP_LABOUR_NOT_ENOUGH, ())
            return
        if mentalNeed > getattr(p, 'mental', 0):
            p.showGameMsg(GMDD.data.MAKE_EQUIP_MENTAL_NOT_ENOUGH, ())
            return
        materialSetNeed = MECD.data.get(equipId, {}).get('materialSetNeed', 0)
        mainCost = self.getMainMaterial(materialSetNeed, onlyBooks=True)
        for cost in mainCost:
            isEnough = cost[3]
            if not isEnough:
                p.showGameMsg(GMDD.data.MAKE_EQUIP_BOOK_NOT_ENOUGH, ())
                return

        p.makeManualEquip(self.npcId, equipId, makeType, self.isHaveMakeBook, self.widget.content.materialOverviewPanel.diKou.checkBox.selected, self.isTianBiEnough)
