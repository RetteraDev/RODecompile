#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldCarrierConstructProxy.o
import BigWorld
import uiConst
import gameglobal
import events
import wingWorldUtils
import uiUtils
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import TipManager
from data import wing_world_carrier_construct_data as WWCCD
from data import wing_world_carrier_enhance_prop_data as WWCEPD
from data import wing_world_carrier_index_data as WWCID
from data import wing_world_carrier_data as WWCD
from data import wing_world_config_data as WWSCD
ATTRIBUTE_NUM = 6
MAX_CHANGE_ATTRIBUTE = 2
MAX_RESOURCE = 3
ZAI_JU_IOCN_PATH = 'wingWorld/zaijuBig/%d.dds'
BONUS_TYPES = ['material', 'population', 'timeCost']

class WingWorldCarrierConstructProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCarrierConstructProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedCarrierTypeItem = None
        self.selectedCarrierTypeId = 0
        self.selectedZaijuItem = None
        self.selectedZaijuId = 0
        self.clickedAttribute = []
        self.changeAttCount = {}
        self.version = 0
        self.attributeDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CARRIER_CONSTRUCT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CARRIER_CONSTRUCT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CARRIER_CONSTRUCT)
        gameglobal.rds.ui.wingWorldCreatePoint.hide()

    def reset(self):
        self.selectedCarrierTypeItem = None
        self.selectedCarrierTypeId = 0
        self.selectedZaijuItem = None
        self.selectedZaijuId = 0
        self.clickedAttribute = []
        self.changeAttCount = {}
        self.version = 0
        self.attributeDict = {}

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CARRIER_CONSTRUCT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.carrierTypeList.barAlwaysVisible = True
        self.widget.carrierTypeList.itemRenderer = 'WingWorldCarrierConstruct_carrierTypeItem'
        self.widget.carrierTypeList.dataArray = []
        self.widget.carrierTypeList.lableFunction = self.itemFunction
        self.widget.carrierTypeList.validateNow()

    def refreshInfo(self):
        if not self.widget:
            return
        self.version = gameglobal.rds.ui.wingWorldCarrierNarrow.getCarrierVersion()
        carrierTypes = self.getCarrierTypeList()
        self.widget.carrierTypeList.dataArray = carrierTypes
        self.widget.carrierTypeList.validateNow()

    def _onBeginBtnClick(self, e):
        if not self.selectedZaijuId:
            return
        enhancePropIds = []
        enhanceCnts = []
        for attributeIdx in self.clickedAttribute:
            enhancePropIds.append(attributeIdx)
            enhanceCnts.append(self.changeAttCount[attributeIdx])

        p = BigWorld.player()
        p.cell.constructWingWorldWarCarrier(self.selectedZaijuId, enhancePropIds, enhanceCnts, self.version)

    def _onPointBtnClick(self, e):
        gameglobal.rds.ui.wingWorldCreatePoint.show()

    def handleItemMcDown(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedCarrierTypeId and self.selectedCarrierTypeId == itemMc.carrierTypeId:
            return
        if self.selectedCarrierTypeItem:
            self.selectedCarrierTypeItem.selected = False
        itemMc.selected = True
        self.selectedCarrierTypeItem = itemMc
        self.selectedCarrierTypeId = itemMc.carrierTypeId
        self.selectedZaijuId = 0
        self.updateZaiju()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.carrierTypeId = itemData.carrierTypeId
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleItemMcDown, False, 0, True)
        iconPath = ZAI_JU_IOCN_PATH % itemData.iconId
        itemMc.carrierTypeIcon.fitSize = True
        itemMc.carrierTypeIcon.loadImage(iconPath)
        itemMc.label = itemData.name
        itemMc.selected = False
        if not self.selectedCarrierTypeId:
            itemMc.selected = True
        elif self.selectedCarrierTypeId and self.selectedCarrierTypeId == itemData.carrierTypeId:
            itemMc.selected = True
        if itemMc.selected:
            self.selectedCarrierTypeItem = itemMc
            self.selectedCarrierTypeId = itemData.carrierTypeId
            self.updateZaiju()

    def getCarrierTypeList(self):
        itemList = []
        for key, data in WWCID.data.iteritems():
            itemInfo = {}
            itemInfo['carrierTypeId'] = key
            itemInfo['name'] = data.get('name', '')
            itemInfo['iconId'] = data.get('iconId', 0)
            itemList.append(itemInfo)

        return itemList

    def handleZaijuMcClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedZaijuId and self.selectedZaijuId == itemMc.zaijuId:
            return
        if self.selectedZaijuItem:
            self.selectedZaijuItem.parent.gotoAndStop('normal')
        itemMc.parent.gotoAndStop('selected')
        self.selectedZaijuItem = itemMc
        self.selectedZaijuId = itemMc.zaijuId
        self.clickedAttribute = []
        self.updateZaijuSelected()

    def updateZaiju(self):
        if not self.selectedCarrierTypeId:
            return
        else:
            zaijuIds = WWCID.data.get(self.selectedCarrierTypeId, {}).get('zaijuIds', ())
            self.widget.carrierTypes.gotoAndStop('type%d' % len(zaijuIds))
            for i in xrange(len(zaijuIds)):
                mcName = 'zaijuMc%d' % i
                zaijuMc = getattr(self.widget.carrierTypes, mcName, None)
                if zaijuMc:
                    zaijuId = zaijuIds[i]
                    zaijuMc.zaijuItem.zaijuId = zaijuId
                    zaijuIconId = WWCCD.data.get(zaijuId, {}).get('zaijuIconId', 0)
                    iconPath = ZAI_JU_IOCN_PATH % zaijuIconId
                    zaijuMc.zaijuItem.zaijuIcon.fitSize = True
                    zaijuMc.zaijuItem.zaijuIcon.loadImage(iconPath)
                    zaijuMc.zaijuItem.zaijuName.text = WWCD.data.get(zaijuId, {}).get('name', '')
                    zaijuMc.zaijuItem.addEventListener(events.MOUSE_CLICK, self.handleZaijuMcClick, False, 0, True)
                    zaijuMc.gotoAndStop('normal')
                    if not self.selectedZaijuId or self.selectedZaijuId == zaijuId:
                        zaijuMc.gotoAndStop('selected')
                        self.selectedZaijuItem = zaijuMc.zaijuItem
                        self.selectedZaijuId = zaijuId
                        self.updateZaijuSelected()

            return

    def handleSubBtnClick(self, *args):
        e = ASObject(args[3][0])
        sunBtn = e.currentTarget
        attributeMc = sunBtn.parent
        attributeMc.addBtn.visible = True
        sunBtn.visible = False
        self.changeAttCount[attributeMc.attributeIndex] = 0
        self.clickedAttribute.remove(attributeMc.attributeIndex)
        self.updateAttributeBtnState()
        self.updateAttributeBar(attributeMc.attributeIndex, False)
        self.updateResourceVal(attributeMc.attributeIndex, False)

    def handleAddBtnClick(self, *args):
        e = ASObject(args[3][0])
        addBtn = e.currentTarget
        attributeMc = addBtn.parent
        attributeMc.subBtn.visible = True
        addBtn.visible = False
        self.changeAttCount[attributeMc.attributeIndex] = 1
        self.clickedAttribute.append(attributeMc.attributeIndex)
        self.updateAttributeBtnState()
        self.updateAttributeBar(attributeMc.attributeIndex, True)
        self.updateResourceVal(attributeMc.attributeIndex, True)

    def updateAttributeBtnState(self):
        for i in range(1, ATTRIBUTE_NUM + 1):
            mcName = 'attribute%d' % i
            attributeMc = getattr(self.widget, mcName, None)
            if attributeMc:
                if not attributeMc.changeVal:
                    self.updateAttributeBtnEnabled(attributeMc, False)
                elif len(self.clickedAttribute) == MAX_CHANGE_ATTRIBUTE:
                    if i in self.clickedAttribute:
                        self.updateAttributeBtnEnabled(attributeMc, True)
                    else:
                        self.updateAttributeBtnEnabled(attributeMc, False)
                else:
                    self.updateAttributeBtnEnabled(attributeMc, True)

    def updateAttributeBtnEnabled(self, attributeMc, isEnable):
        if attributeMc.subBtn.visible:
            attributeMc.subBtn.enabled = isEnable
        elif attributeMc.addBtn.visible:
            attributeMc.addBtn.enabled = isEnable

    def updateAttributeBar(self, attributeIndex, isAdd):
        wwccdData = WWCCD.data.get(self.selectedZaijuId, {})
        initPoints = wwccdData.get('initPoints', {})
        maxPoints = wwccdData.get('maxPoints', {})
        pointsPerEnh = wwccdData.get('pointsPerEnh', {})
        for i in range(1, ATTRIBUTE_NUM + 1):
            mcName = 'attribute%d' % i
            attributeMc = getattr(self.widget, mcName, None)
            if attributeMc and i == attributeIndex:
                iniVal = initPoints[i]
                maxVal = maxPoints[i]
                changeVal = pointsPerEnh[i]
                if isAdd:
                    extraVal = iniVal + changeVal
                    szVal = '%s+%s' % (uiUtils.toHtml(iniVal, '#F3EBC7'), uiUtils.toHtml(changeVal, '#fff726'))
                else:
                    extraVal = iniVal
                    szVal = '%s' % uiUtils.toHtml(iniVal, '#F3EBC7')
                attributeMc.attributeBar.currentValues = [iniVal, extraVal]
                attributeMc.attributeBar.maxValue = maxVal
                attributeMc.attributeVal.htmlText = szVal
                break

    def initResourceVal(self):
        costeds = []
        totalCoreCost, totalLoaderCost, totalTimeCost = wingWorldUtils.getWingWorldWarCarrierConstructCost(self.selectedZaijuId, self.attributeDict)
        costeds.append(totalCoreCost)
        costeds.append(totalLoaderCost)
        costeds.append(totalTimeCost)
        self.widget.iconType0.bonusType = BONUS_TYPES[0]
        self.widget.iconType0.curResource = costeds[0]
        colorVal = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resCore, costeds[0])
        self.widget.valT0.htmlText = colorVal
        tipMaterial = WWSCD.data.get('constructMaterialTip', '')
        TipManager.addTip(self.widget.iconType0, tipMaterial)
        self.widget.iconType1.bonusType = BONUS_TYPES[1]
        self.widget.iconType1.curResource = costeds[1]
        colorVal = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader, costeds[1])
        self.widget.valT1.htmlText = colorVal
        tipPopulation = WWSCD.data.get('constructPopulationTip', '')
        TipManager.addTip(self.widget.iconType1, tipPopulation)
        self.widget.iconType2.bonusType = BONUS_TYPES[2]
        self.widget.iconType2.curResource = costeds[2]
        self.widget.valT2.htmlText = costeds[2]
        isMaterialLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resCore < costeds[0]
        isPopulationLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader < costeds[1]
        self.updateResourceLessDesc(isMaterialLess, isPopulationLess)

    def updateZaijuSelected(self):
        self.clickedAttribute = []
        self.changeAttCount = {}
        zaijuData = WWCD.data.get(self.selectedZaijuId, {})
        self.widget.zjName.text = zaijuData.get('name', '')
        self.widget.zjDesc.text = zaijuData.get('desc', '')
        self.attributeDict = gameglobal.rds.ui.wingWorldCarrierNarrow.getZaijuAttributeInfo(self.selectedZaijuId)
        self.initResourceVal()
        wwccdData = WWCCD.data.get(self.selectedZaijuId, {})
        initPoints = wwccdData.get('initPoints', {})
        maxPoints = wwccdData.get('maxPoints', {})
        pointsPerEnh = wwccdData.get('pointsPerEnh', {})
        for i in range(1, ATTRIBUTE_NUM + 1):
            mcName = 'attribute%d' % i
            attributeMc = getattr(self.widget, mcName, None)
            if attributeMc:
                attributeMc.attributeIndex = i
                attributeMc.attributeNameT.text = WWCEPD.data.get(i, {}).get('name', '')
                TipManager.addTip(attributeMc.attributeNameT, WWCEPD.data.get(i, {}).get('tipDesc', ''))
                maxVal = maxPoints.get(i, 0)
                iniVal = initPoints.get(i, 0)
                changeVal = pointsPerEnh.get(i, 0)
                if self.attributeDict and i in self.attributeDict and self.attributeDict[i]:
                    self.clickedAttribute.append(i)
                    self.changeAttCount[i] = self.attributeDict[i]
                    extraVal = iniVal + changeVal
                    attributeMc.addBtn.visible = False
                    attributeMc.subBtn.visible = True
                    szVal = '%s+%s' % (uiUtils.toHtml(iniVal, '#F3EBC7'), uiUtils.toHtml(changeVal, '#fff726'))
                else:
                    extraVal = 0
                    attributeMc.addBtn.visible = True
                    attributeMc.subBtn.visible = False
                    szVal = '%s' % uiUtils.toHtml(iniVal, '#F3EBC7')
                attributeMc.changeVal = changeVal
                attributeMc.attributeBar.currentValues = [iniVal, extraVal]
                attributeMc.attributeBar.maxValue = maxVal
                attributeMc.attributeVal.htmlText = szVal
                attributeMc.subBtn.addEventListener(events.MOUSE_CLICK, self.handleSubBtnClick, False, 0, True)
                attributeMc.addBtn.addEventListener(events.MOUSE_CLICK, self.handleAddBtnClick, False, 0, True)

        self.updateAttributeBtnState()

    def getColorVal(self, leftCost, needCost):
        if leftCost >= needCost:
            colorVal = uiUtils.toHtml(needCost, '#D9CFB6')
        else:
            colorVal = uiUtils.toHtml(needCost, '#CE4C45')
        return colorVal

    def updateResourceVal(self, attributeIndex, isAdd):
        wwccdData = WWCCD.data.get(self.selectedZaijuId, {})
        enhanceCost = wwccdData.get('enhanceCost', {})
        changeVal = enhanceCost.get(attributeIndex, 0)
        resources = []
        for i in xrange(MAX_RESOURCE):
            mcName0 = 'iconType%d' % i
            mcName1 = 'valT%d' % i
            iconType = getattr(self.widget, mcName0, None)
            valT = getattr(self.widget, mcName1, None)
            preVal = int(iconType.curResource)
            if isAdd:
                curResource = preVal + changeVal[i]
            else:
                curResource = preVal - changeVal[i]
            if i == 0:
                colorVal = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resCore, curResource)
            elif i == 1:
                colorVal = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader, curResource)
            elif i == 2:
                colorVal = curResource
            resources.append(curResource)
            iconType.curResource = curResource
            valT.htmlText = colorVal

        isMaterialLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resCore < resources[0]
        isPopulationLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader < resources[1]
        self.updateResourceLessDesc(isMaterialLess, isPopulationLess)

    def updateResourceLessDesc(self, isMaterialLess, isPopulationLess):
        self.widget.desc0.visible = True
        resourceLessDesc = WWSCD.data.get('resourceLessDesc', [])
        warCarrierConstructWaitingNumLimit = WWSCD.data.get('warCarrierConstructWaitingNumLimit', 8)
        waitingInfo = gameglobal.rds.ui.wingWorldCarrierNarrow.waitingInfo
        if isMaterialLess and isPopulationLess:
            self.widget.desc0.htmlText = resourceLessDesc[0]
            self.widget.beginBtn.enabled = False
        elif isMaterialLess:
            self.widget.desc0.htmlText = resourceLessDesc[1]
            self.widget.beginBtn.enabled = False
        elif isPopulationLess:
            self.widget.desc0.htmlText = resourceLessDesc[2]
            self.widget.beginBtn.enabled = False
        elif len(waitingInfo) >= warCarrierConstructWaitingNumLimit:
            self.widget.desc0.htmlText = resourceLessDesc[3]
            self.widget.beginBtn.enabled = False
        else:
            self.widget.beginBtn.enabled = True
            p = BigWorld.player()
            warCarrierAccelerateDesc = WWSCD.data.get('warCarrierAccelerateDesc', ['%d%d', '%d%d'])
            attackAccNum, defenceAccNum, createRate = WWSCD.data.get('warCarrierConstructAccelerateArgs', (0, 0, 1))
            country = p.wingWorld.country.getOwn()
            doneNum = len(gameglobal.rds.ui.wingWorldCarrierNarrow.doneInfo)
            if p.getWingWarCityId() in country.ownedCityIds:
                if doneNum < defenceAccNum:
                    self.widget.desc0.visible = True
                    self.widget.desc0.htmlText = warCarrierAccelerateDesc[1] % (defenceAccNum, createRate)
                else:
                    self.widget.desc0.visible = False
            elif doneNum < attackAccNum:
                self.widget.desc0.visible = True
                self.widget.desc0.htmlText = warCarrierAccelerateDesc[0] % (attackAccNum, createRate)
            else:
                self.widget.desc0.visible = False

    def updateResStateBuildSuc(self):
        if not self.widget:
            return
        val0 = self.widget.iconType0.curResource
        val1 = self.widget.iconType1.curResource
        self.widget.valT0.htmlText = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resCore, val0)
        self.widget.valT1.htmlText = self.getColorVal(gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader, val1)
        isMaterialLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resCore < val0
        isPopulationLess = gameglobal.rds.ui.wingWorldCarrierNarrow.resLoader < val1
        self.updateResourceLessDesc(isMaterialLess, isPopulationLess)
