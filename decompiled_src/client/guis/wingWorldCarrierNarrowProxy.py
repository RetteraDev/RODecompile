#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldCarrierNarrowProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import gameglobal
import utils
import wingWorldUtils
import events
import gametypes
from uiProxy import UIProxy
from asObject import ASObject
from callbackHelper import Functor
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import wing_world_carrier_construct_data as WWCCD
from data import wing_world_config_data as WWSCD
from data import wing_world_carrier_enhance_prop_data as WWCEPD
from data import wing_world_carrier_data as WWCD
from data import wing_city_building_entity_data as WCBED
from cdata import game_msg_def_data as GMDD
ZAI_JU_IOCN_PATH = 'wingWorld/zaijuSmall/%d.dds'
ZAI_JU_SHUO_SUO_NUM = 4
ZAI_JU_ZHAN_KAI_NUM = 8
ZAI_JU_CREATED_NUM = 4
DEALY_TIME = -2

class WingWorldCarrierNarrowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCarrierNarrowProxy, self).__init__(uiAdapter)
        self.widget = None
        self.isZhankai = False
        self.constructingInfo = ()
        self.constructEndTime = 0
        self.waitingInfo = []
        self.doneInfo = []
        self.bornPointEntNo = 0
        self.resCore = 0
        self.resLoader = 0
        self.version = 0
        self.totalTimeCost = 0
        self.callback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CARRIER_NARROW, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CARRIER_NARROW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CARRIER_NARROW)

    def reset(self):
        self.callback = None

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CARRIER_NARROW)

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
        if self.isZhankai:
            self.widget.constructMc.gotoAndStop('zhankai')
            self.updateZhankaiMc()
        else:
            self.widget.constructMc.gotoAndStop('shousuo')
            self.updateShuosuoMc()

    def updateCarrierInfo(self, constructingInfo, constructStartTime, constructEndTime, waitingInfo, doneInfo, bornPointEntNo, resCore, resLoader, version):
        self.constructingInfo = constructingInfo
        self.constructEndTime = constructEndTime
        self.waitingInfo = waitingInfo
        self.doneInfo = doneInfo
        self.bornPointEntNo = bornPointEntNo
        self.resCore = resCore
        self.resLoader = resLoader
        self.version = version
        self.totalTimeCost = max(0, constructEndTime - constructStartTime)
        self.refreshInfo()

    def handleSlotClick(self, *args):
        msg = WWSCD.data.get('cancelCreateZaijuDesc', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realCancel, True, 0))

    def handleWaitingSlotClick(self, *args):
        e = ASObject(args[3][0])
        slot = e.currentTarget
        waitingIndex = slot.waitingIndex
        msg = WWSCD.data.get('cancelCreateZaijuDesc', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realCancel, False, waitingIndex))

    def realCancel(self, isCurrent, waitingIndex):
        p = BigWorld.player()
        p.cell.cancelWingWorldWarCarrierConstruct(isCurrent, waitingIndex, self.version)

    def handleCreatedSlotClick(self, *args):
        e = ASObject(args[3][0])
        slot = e.currentTarget
        doneIndex = slot.doneIndex
        if doneIndex < len(self.doneInfo):
            carriers = self.doneInfo[doneIndex]
            carrierType = carriers[0]
            enhanceDict = carriers[1]
            enhancePropIds = tuple(enhanceDict.keys())
            enhanceCnts = tuple(enhanceDict.values())
            totalCoreCost, totalLoaderCost, totalTimeCost = wingWorldUtils.getWingWorldWarCarrierConstructCost(carrierType, enhanceDict)
            warCarrierConstructWaitingNumLimit = WWSCD.data.get('warCarrierConstructWaitingNumLimit', 8)
            p = BigWorld.player()
            if self.resCore < totalCoreCost and self.resLoader < totalLoaderCost:
                p.showGameMsg(GMDD.data.WING_WORLD_ZAIJU_RESOURCE_LESS_DESC0, ())
                return
            if self.resCore < totalCoreCost:
                p.showGameMsg(GMDD.data.WING_WORLD_ZAIJU_RESOURCE_LESS_DESC1, ())
                return
            if self.resLoader < totalLoaderCost:
                p.showGameMsg(GMDD.data.WING_WORLD_ZAIJU_RESOURCE_LESS_DESC2, ())
                return
            if len(self.waitingInfo) >= warCarrierConstructWaitingNumLimit:
                p.showGameMsg(GMDD.data.WING_WORLD_ZAIJU_RESOURCE_LESS_DESC3, ())
                return
            p.cell.constructWingWorldWarCarrier(carrierType, enhancePropIds, enhanceCnts, self.version)

    def _onCarriersBtnClick(self, e):
        gameglobal.rds.ui.wingWorldCarrierConstruct.show()

    def _onZhankaiBtnClick(self, e):
        self.isZhankai = True
        self.widget.constructMc.gotoAndStop('zhankai')
        self.updateZhankaiMc()

    def _onShuosuoBtnClick(self, e):
        self.isZhankai = False
        self.widget.constructMc.gotoAndStop('shousuo')
        self.updateShuosuoMc()

    def updateShuosuoMc(self):
        self.updateBar()
        self.updateCommonMc()

    def updateZhankaiMc(self):
        self.updateBar()
        self.updateCommonMc()
        self.updateZaijuSlot(ZAI_JU_ZHAN_KAI_NUM)
        self.updateZaijuCreated()

    def updateBar(self):
        if not self.widget:
            self.stopCallback()
            return
        nowTime = utils.getNow()
        leftTime = max(self.constructEndTime - nowTime, 0)
        costTime = max(self.totalTimeCost - leftTime, 0)
        if self.constructEndTime and self.constructEndTime - nowTime <= DEALY_TIME:
            self.widget.constructMc.carrierBar.currentValue = costTime
            self.widget.constructMc.carrierBar.maxValue = self.totalTimeCost
            self.widget.constructMc.carrierBar.validateNow()
            self.widget.constructMc.carrierBar.textField.text = gameStrings.WING_WORLD_POS_FULL_DESC
            self.stopCallback()
            return
        self.widget.constructMc.carrierBar.currentValue = costTime
        self.widget.constructMc.carrierBar.maxValue = self.totalTimeCost
        if not self.constructEndTime:
            self.stopCallback()
            return
        self.stopCallback()
        self.callback = BigWorld.callback(1, self.updateBar)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateCommonMc(self):
        constructMc = self.widget.constructMc
        constructMc.icon0.bonusType = 'material'
        constructMc.valT0.text = self.resCore
        tipMaterial = WWSCD.data.get('carrierMaterialTip', '')
        TipManager.addTip(constructMc.icon0, tipMaterial)
        maxPopulation = WWSCD.data.get('warCarrierConstructInitRes', (0, 0))[1]
        constructMc.icon1.bonusType = 'population'
        constructMc.valT1.text = '%d/%d' % (self.resLoader, maxPopulation)
        tipPopulation = WWSCD.data.get('carrierPopulationTip', '')
        TipManager.addTip(constructMc.icon1, tipPopulation)
        zaijuId = self.constructingInfo[0] if self.constructingInfo else 0
        ASUtils.setHitTestDisable(constructMc.carrierSlot.numT, True)
        if zaijuId:
            zaijuIconId = WWCCD.data.get(zaijuId, {}).get('zaijuIconId', 0)
            iconPath = ZAI_JU_IOCN_PATH % zaijuIconId
            constructMc.carrierSlot.slot.fitSize = True
            constructMc.carrierSlot.slot.dragable = False
            constructMc.carrierSlot.slot.setItemSlotData({'iconPath': iconPath})
            constructMc.carrierSlot.slot.validateNow()
            constructMc.carrierSlot.slot.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
            constructMc.carrierSlot.numT.visible = False
            zaijuName = WWCD.data.get(zaijuId, {}).get('name', '')
            attributeName = self.getCreatedAttributeName(self.constructingInfo[1])
            tipMsg = WWSCD.data.get('zaijuWaitingTip', '%s%s') % (zaijuName, attributeName)
            TipManager.addTip(constructMc.carrierSlot.slot, tipMsg)
        else:
            constructMc.carrierSlot.numT.visible = True
            constructMc.carrierSlot.numT.text = '1'
            constructMc.carrierSlot.slot.setItemSlotData(None)
            constructMc.carrierSlot.slot.removeEventListener(events.MOUSE_CLICK, self.handleSlotClick)
            TipManager.removeTip(constructMc.carrierSlot.slot)

    def updateZaijuSlot(self, slotNum):
        for i in xrange(slotNum):
            mcName = 'carrierSlot%d' % i
            carrierSlot = getattr(self.widget.constructMc, mcName, None)
            carrierSlot.slot.waitingIndex = i
            ASUtils.setHitTestDisable(carrierSlot.numT, True)
            if i < len(self.waitingInfo):
                carriers = self.waitingInfo[i]
                zaijuId = carriers[0]
                zaijuIconId = WWCCD.data.get(zaijuId, {}).get('zaijuIconId', 0)
                iconPath = ZAI_JU_IOCN_PATH % zaijuIconId
                carrierSlot.slot.fitSize = True
                carrierSlot.slot.dragable = False
                carrierSlot.slot.setItemSlotData({'iconPath': iconPath})
                carrierSlot.slot.validateNow()
                carrierSlot.slot.addEventListener(events.MOUSE_CLICK, self.handleWaitingSlotClick, False, 0, True)
                carrierSlot.numT.visible = False
                zaijuName = WWCD.data.get(zaijuId, {}).get('name', '')
                attributeName = self.getCreatedAttributeName(carriers[1])
                tipMsg = WWSCD.data.get('zaijuWaitingTip', '%s%s') % (zaijuName, attributeName)
                TipManager.addTip(carrierSlot.slot, tipMsg)
            else:
                carrierSlot.numT.visible = True
                carrierSlot.numT.text = i + 2
                carrierSlot.slot.setItemSlotData(None)
                carrierSlot.slot.removeEventListener(events.MOUSE_CLICK, self.handleWaitingSlotClick)
                TipManager.removeTip(carrierSlot.slot)

    def updateZaijuCreated(self):
        for i in xrange(ZAI_JU_CREATED_NUM):
            mcName = 'createdSlot%d' % i
            createdSlot = getattr(self.widget.constructMc, mcName, None)
            createdSlot.slot.doneIndex = i
            createdSlot.numT.visible = False
            if i < len(self.doneInfo):
                carriers = self.doneInfo[i]
                zaijuId = carriers[0]
                zaijuIconId = WWCCD.data.get(zaijuId, {}).get('zaijuIconId', 0)
                iconPath = ZAI_JU_IOCN_PATH % zaijuIconId
                createdSlot.slot.fitSize = True
                createdSlot.slot.dragable = False
                createdSlot.slot.setItemSlotData({'iconPath': iconPath})
                createdSlot.slot.validateNow()
                createdSlot.slot.addEventListener(events.MOUSE_CLICK, self.handleCreatedSlotClick, False, 0, True)
                createdSlot.numT.visible = False
                zaijuName = WWCD.data.get(zaijuId, {}).get('name', '')
                attributeName = self.getCreatedAttributeName(carriers[1])
                tipMsg = WWSCD.data.get('zaijuCreatedTip', '%s%s') % (zaijuName, attributeName)
                TipManager.addTip(createdSlot.slot, tipMsg)
            else:
                createdSlot.slot.setItemSlotData(None)
                createdSlot.slot.removeEventListener(events.MOUSE_CLICK, self.handleCreatedSlotClick)
                TipManager.removeTip(createdSlot.slot)

    def getCreatedAttributeName(self, enhanceDict):
        attributeName = ''
        for attributeIdx in enhanceDict:
            attName = WWCEPD.data.get(attributeIdx, {}).get('name', '')
            if attributeName:
                attributeName = attributeName + ',' + attName
            else:
                attributeName = attName

        if not attributeName:
            attributeName = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        return attributeName

    def getCarrierVersion(self):
        return self.version

    def getZaijuAttributeInfo(self, zaijuId):
        if self.constructingInfo:
            carrierType = self.constructingInfo[0]
            if carrierType == zaijuId:
                return self.constructingInfo[1]
        if self.waitingInfo:
            for waits in self.waitingInfo:
                if waits[0] == zaijuId:
                    return waits[1]

        if self.doneInfo:
            for dones in self.doneInfo:
                if dones[0] == zaijuId:
                    return dones[1]

        return {}

    def isShowWingWorldCarrierNarrow(self):
        p = BigWorld.player()
        if hasattr(p, 'inWingWarCity') and p.inWingWarCity():
            fixedPrivileges = wingWorldUtils.getWingArmyData().get(p.wingWorldPostId, {}).get('fixedPrivileges', ())
            if gametypes.WING_WORLD_PRIVILEGE_WAR_CARRIER_CONSTRUCT in fixedPrivileges:
                gameglobal.rds.ui.wingWorldCarrierNarrow.show()
