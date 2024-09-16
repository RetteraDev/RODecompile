#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipRefineSuitsPropProxy.o
import BigWorld
import const
import gametypes
from guis import uiConst
from guis.asObject import ASObject
from guis import uiUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import prop_ref_data as PRD
from data import enhance_suit_data as ESD
CAN_REFINE_PARTS = [gametypes.EQU_PART_HEAD,
 gametypes.EQU_PART_BODY,
 gametypes.EQU_PART_SHOE,
 gametypes.EQU_PART_HAND,
 gametypes.EQU_PART_LEG,
 gametypes.EQU_PART_NECKLACE,
 gametypes.EQU_PART_RING1,
 gametypes.EQU_PART_RING2,
 gametypes.EQU_PART_WEAPON_ZHUSHOU,
 gametypes.EQU_PART_WEAPON_FUSHOU,
 gametypes.EQU_PART_EARRING1,
 gametypes.EQU_PART_EARRING2]

class EquipRefineSuitsPropProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipRefineSuitsPropProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_REFINE_SUITS_PROP, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EQUIP_REFINE_SUITS_PROP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EQUIP_REFINE_SUITS_PROP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_EQUIP_REFINE_SUITS_PROP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def propListLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        BigWorld.player().itemData = itemData
        mc.txtPropName.htmlText = itemData.txtName
        mc.txtValue.htmlText = itemData.txtValue

    def getRefineTotal(self):
        total = 0
        for part in CAN_REFINE_PARTS:
            eqiupItem = self.getRefineItem(part)
            maxRefine = 0 if not eqiupItem else uiUtils.getEquipTotalRefining(eqiupItem)
            total += maxRefine

        return total

    def getRefineCnt(self, refineLv, maxTotal):
        p = BigWorld.player()
        cnt = 0
        for part in CAN_REFINE_PARTS:
            eqiupItem = self.getRefineItem(part)
            maxRefineLv = 0 if not eqiupItem else eqiupItem.getRealEnhlv()
            if maxRefineLv >= refineLv:
                cnt += 1

        return cnt

    def getInfoByLv(self, lv, isNext = False):
        info = {}
        cfgData = ESD.data.get((BigWorld.player().school, lv), {})
        if cfgData:
            info['txtLv'] = gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_LV % lv[0]
            info['txtTitle'] = gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_NEXT if isNext else gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_CURRENT
            propList = [ (propId, value) for propId, _, value in cfgData.get('prop', ()) ]
            propInfo = []
            for propId, value in propList:
                cfg = PRD.data.get(propId, {})
                propInfo.append({'txtName': cfg.get('chName'),
                 'txtValue': value})

            info['propList'] = propInfo
            needLv = lv[0]
            needTotal = lv[1] * 100
            needCnt = len(CAN_REFINE_PARTS)
            curCnt = self.getRefineCnt(*lv)
            currentTotal = self.getRefineTotal()
            info['needLv'] = gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_NEED_LV % needLv
            info['needCnt'] = '%d/%d' % (curCnt, needCnt)
            info['totalRefine'] = gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_NEED_TOTAL % (currentTotal, needTotal)
        return info

    def refreshSuitsMc(self, mc, data):
        mc.propList.itemRenderer = 'EquipRefineSuitsProp_ItemRender'
        mc.propList.labelFunction = self.propListLabelFunction
        mc.title.title.text = data.get('txtTitle')
        mc.title.txtLv.text = data.get('txtLv')
        mc.propList.dataArray = data.get('propList', [])
        mc.condition.txtCondition.htmlText = data.get('needLv', '')
        mc.condition.txtCnt.htmlText = data.get('needCnt', '')
        mc.condition.txtCnt.x = mc.condition.txtCondition.x + mc.condition.txtCondition.textWidth + 5
        mc.condition.txtTotal.htmlText = data.get('totalRefine', '')

    def getAddScore(self):
        currentLv, nextLv = self.getRefineLv()
        addScore = int(ESD.data.get((BigWorld.player().school, currentLv), {}).get('attnum', 0))
        return addScore

    def getRefineItem(self, part):
        p = BigWorld.player()
        item = p.equipment.get(part, None)
        sutItem = p.subEquipment.get(part, None)
        if not item and not sutItem:
            return
        elif item and not sutItem:
            return item
        elif sutItem and not item:
            return sutItem
        equipEnhanceLv = item.getRealEnhlv()
        subEquipEnhanceLv = sutItem.getRealEnhlv()
        if equipEnhanceLv != subEquipEnhanceLv:
            if equipEnhanceLv > subEquipEnhanceLv:
                return item
            return sutItem
        else:
            return item

    def getRefineLv(self):
        p = BigWorld.player()
        minLv = 100
        maxTotalRefine = 0
        for partIndex in CAN_REFINE_PARTS:
            item = self.getRefineItem(partIndex)
            if not item:
                equipEnhanceLv = 0
                equipEnhance = 0
            else:
                equipEnhanceLv = item.getRealEnhlv()
                equipEnhance = uiUtils.getEquipTotalRefining(item)
            maxTotalRefine += equipEnhance
            minLv = min(minLv, equipEnhanceLv)

        currentLv = None
        nextLv = None
        keys = ESD.data.keys()
        keys.sort()
        for index, (school, (enhancelv, enhanceTotal)) in enumerate(keys):
            if school != p.school:
                continue
            if enhancelv <= minLv and maxTotalRefine >= enhanceTotal * 100:
                currentLv = (enhancelv, enhanceTotal)
            else:
                nextLvIndex = index
                if nextLvIndex < len(keys):
                    nextKey = keys[nextLvIndex]
                    if nextKey[0] == p.school:
                        nextLv = nextKey[1]
                break

        return (currentLv, nextLv)

    def getInfo(self):
        result = {}
        p = BigWorld.player()
        currentLv, nextLv = self.getRefineLv()
        scoreLv = currentLv if currentLv else nextLv
        result['score'] = int(ESD.data.get((p.school, scoreLv), {}).get('attnum', ''))
        result['current'] = self.getInfoByLv(currentLv, False)
        result['next'] = self.getInfoByLv(nextLv, True)
        return result

    def refreshInfo(self):
        if not self.widget:
            return
        info = self.getInfo()
        currentInfo = info.get('current', {})
        nextInfo = info.get('next', {})
        isShowTwo = currentInfo and nextInfo
        self.widget.gotoAndStop('two' if isShowTwo else 'one')
        self.widget.txtScore.text = gameStrings.EQUIP_REFINE_SUITS_PROP_TXT_SCORE % info.get('score')
        if isShowTwo:
            currentMc = self.widget.curSuitsProp
            self.refreshSuitsMc(currentMc, currentInfo)
            nextMc = self.widget.nextSuitsProp
            self.refreshSuitsMc(nextMc, nextInfo)
        else:
            currentMc = self.widget.curSuitsProp
            self.refreshSuitsMc(currentMc, nextInfo if nextInfo else currentInfo)
