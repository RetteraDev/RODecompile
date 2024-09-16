#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/multiCarrierProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gamelog
import gameglobal
import gametypes
import events
import random
import utils
from asObject import ASObject
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import uiConst
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import MenuManager
from guis import uiUtils
from gameStrings import gameStrings
from data import multi_carrier_data as MCD
from data import wing_world_carrier_data as WWCD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
SPRITTE_HEIGHT = 21

class MultiCarrierProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MultiCarrierProxy, self).__init__(uiAdapter)
        self.widget = None
        self.multiCarrierNo = None
        self.showSetting = False
        self.seatMCList = []
        self.menuItemMCList = []
        self.reset()

    def getCarrierData(self):
        if self.carrierType == uiConst.MUTLI_CARRIER_WING_WORLD:
            return WWCD.data.get(self.multiCarrierNo, {})
        return MCD.data.get(self.multiCarrierNo, {})

    @property
    def carrier(self):
        p = BigWorld.player()
        if self.carrierType == uiConst.MUTLI_CARRIER_WING_WORLD:
            return p.wingWorldCarrier
        return p.carrier

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MULTI_CARRIER:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MULTI_CARRIER)
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_MULTI_CARRIER, False)
        self.reset()

    def show(self, multiCarrierNo, carrierType = uiConst.MULTI_CARRIER_NORMAL):
        self.reset()
        self.multiCarrierNo = multiCarrierNo
        self.carrierType = carrierType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MULTI_CARRIER)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.carrierSettingBtn.visible = False
        self.widget.listBottonMC.visible = False
        self.widget.seatMC.visible = False
        self.widget.carrierSettingBtn.focusable = False
        self.initSettingList()
        p = BigWorld.player()
        if p.isTeamLeader():
            self.showFunc1Btn(False)
            self.widget.carrierSettingBtn.visible = True
        carrierState = 2
        if self.carrierType == uiConst.MULTI_CARRIER_NORMAL:
            carrierState = self.carrier.carrierState
        self.resetIconState(carrierState)
        self.refreshSeat()

    def createSeatMC(self, count):
        if count > len(self.seatMCList):
            for i in xrange(count - len(self.seatMCList)):
                self.seatMCList.append(self.widget.getInstByClsName('MultiCarrier_Seat_Mounts'))

    def clearMenuMC(self):
        for menuItem in self.menuItemMCList:
            menuItem.visible = False
            ASUtils.setMcData(menuItem, 'data', {})
            self.widget.removeChild(menuItem)

        self.menuItemMCList = []

    def createMenuItem(self, count):
        if count > len(self.menuItemMCList):
            for i in xrange(count - len(self.menuItemMCList)):
                menuItem = self.widget.getInstByClsName('MultiCarrier_MenuItemtBtn')
                self.menuItemMCList.append(menuItem)
                self.widget.addChild(menuItem)

    def _onMenuItemBtnClick(self, e):
        gamelog.debug('-----m.l@MultiCarrierProxy._onMenuItemBtnClick', e.target.data)
        funcName = e.target.data.funcName
        func = getattr(self, funcName, None)
        if func:
            func(e.target.data)

    def refreshSeat(self):
        if not self.widget:
            return
        p = BigWorld.player()
        multiCarrierData = self.getCarrierData()
        self.clearSeatIcon()
        self.refreshBtnState()
        self.refreshSeatMCState(multiCarrierData)

    def refreshSeatMCState(self, multiCarrierData):
        count = multiCarrierData.get('maxPlaceNum', 0)
        posData = multiCarrierData.get('uiPos', {})
        seatName = multiCarrierData.get('seatName', [])
        p = BigWorld.player()
        self.createSeatMC(count)
        for i in xrange(count):
            itemData = {}
            mc = self.seatMCList[i]
            entityId = self.carrier.getEntIdByIdx(i + 1)
            itemData['entityId'] = entityId
            if not entityId:
                mc.gotoAndPlay('empty')
            elif entityId == p.id:
                mc.gotoAndPlay('self')
            else:
                mc.gotoAndPlay('other')
            mc.x = posData.get(i, (0, 0))[0]
            mc.y = posData.get(i, (0, 0))[1]
            ASUtils.setMcData(mc, 'data', itemData)
            carrierIndex = i + 1
            itemData['data'] = {'carrierIndex': carrierIndex,
             'entityId': entityId}
            if carrierIndex != self.carrier.get(p.id):
                MenuManager.getInstance().registerMenuById(mc, uiConst.MENU_MULTI_CARRIER_SEAT_NODE, itemData)
            self.addSeatTip(i, entityId, mc, seatName[i])
            self.widget.carrierMC.addChild(mc)

    def addSeatTip(self, idx, entityId, mc, seatName):
        if entityId:
            ent = BigWorld.entities.get(entityId, None)
            if ent and ent.inWorld:
                if ent != BigWorld.player():
                    tip = SCD.data.get('carrierSeatNameTip', '%s\n%s\nlv %d\n%s') % (seatName,
                     ent.roleName,
                     ent.lv,
                     const.SCHOOL_DICT[ent.school])
                else:
                    tip = '%s\n%s\nlv %d\n%s' % (seatName,
                     ent.roleName,
                     ent.lv,
                     const.SCHOOL_DICT[ent.school])
                TipManager.addTip(mc, tip)

    def refreshBtnState(self):
        p = BigWorld.player()
        if self.carrierType == uiConst.MULTI_CARRIER_NORMAL:
            if p.isTeamLeader():
                if self.carrier.isReadyState():
                    if self.carrier.isReachCreateNum():
                        self.widget.func1Btn.visible = True
                        self.widget.func1Btn.gotoAndPlay('kai')
                    else:
                        self.widget.func1Btn.visible = False
                    self.widget.func2Btn.gotoAndPlay('jie')
                    self.widget.carrierSettingBtn.visible = True
                elif self.carrier.isRunningState():
                    if self.carrier.get(p.id):
                        self.widget.func1Btn.visible = True
                        self.widget.func1Btn.gotoAndPlay('li')
                        self.widget.func2Btn.gotoAndPlay('jie')
                        self.widget.carrierSettingBtn.visible = True
                    else:
                        self.widget.func1Btn.visible = True
                        self.widget.func2Btn.visible = True
                        self.widget.func1Btn.gotoAndPlay('hui')
                        self.widget.func2Btn.gotoAndPlay('jie')
                        self.widget.carrierSettingBtn.visible = False
            elif self.carrier.carrierState in (gametypes.MULTI_CARRIER_STATE_CHECK_READY, gametypes.MULTI_CARRIER_STATE_RUNNING):
                self.widget.func1Btn.visible = False
                if self.carrier.get(p.id):
                    self.widget.func2Btn.gotoAndPlay('li')
                else:
                    self.widget.func2Btn.gotoAndPlay('hui')
        elif p.isOnWingWorldCarrier():
            if self.carrier.getCarrierHeaderEntId() == p.id:
                self.widget.func1Btn.visible = True
                self.widget.func2Btn.visible = True
                self.widget.func1Btn.gotoAndStop('li')
                self.widget.func2Btn.gotoAndPlay('jie')
                self.widget.carrierSettingBtn.visible = True
            else:
                self.widget.func1Btn.visible = False
                self.widget.func2Btn.visible = True
                self.widget.func2Btn.gotoAndStop('li')
                self.widget.carrierSettingBtn.visible = False

    def resetIconState(self, carrierState):
        if not self.widget:
            return
        multiCarrierData = self.getCarrierData()
        iconId = multiCarrierData.get('icon', '')
        iconPath = 'carrier/%s_%d.dds' % (iconId, carrierState)
        self.widget.carrierMC.carrierMainMC.icon.loadImage(iconPath)

    def initSettingList(self):
        self.widget.seatMC.seatListMC.itemRenderer = 'MultiCarrier_settingListItem'
        self.widget.seatMC.seatListMC.lableFunction = self.itemFunction
        self.widget.seatMC.seatListMC.itemHeight = SPRITTE_HEIGHT

    def clearSeatIcon(self):
        if not self.widget:
            return
        for mc in self.seatMCList:
            self.widget.carrierMC.removeChild(mc)

        self.seatMCList = []

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.roleNameTF.text = itemData.name
        itemMc.seatNameTF.text = itemData.seatName
        ASUtils.setMcData(itemMc, 'data', itemData)
        itemMc.jobIconMC.gotoAndPlay(uiUtils.getSchoolLabelString(itemData.school))
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleSettingSeatClick, False, 0, True)
        itemMc.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleItemStateChange, False, 0, True)
        itemMc.validateNow()
        carrierIndex = itemData.index
        p = BigWorld.player()
        if carrierIndex != self.carrier.get(p.id):
            param = {}
            param['entityId'] = itemData.entityId
            param['data'] = {'carrierIndex': itemData.index,
             'entityId': itemData.entityId}
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_MULTI_CARRIER_SEAT_NODE, param)

    def handleSettingSeatClick(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        gamelog.debug('m.l@MultiCarrierProxy.handleSettingSeatClick')

    def handleItemStateChange(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.roleNameTF.text = mc.data.name
        mc.seatNameTF.text = mc.data.seatName

    def refreshSeatSettingList(self):
        seatInfoList = []
        p = BigWorld.player()
        multiCarrierData = self.getCarrierData()
        maxPlaceNum = multiCarrierData.get('maxPlaceNum', 0)
        self.widget.seatMC.countTF.text = gameStrings.TEXT_MULTICARRIERPROXY_272 % (len(self.carrier), maxPlaceNum)
        for entId, index in self.carrier.iteritems():
            ent = BigWorld.entities.get(entId, None)
            name = ''
            school = 0
            if ent and ent.inWorld:
                name = utils.getRealRoleName(ent.roleName)
                school = ent.school
            spriteInfo = {}
            spriteInfo['entityId'] = entId
            spriteInfo['index'] = index
            spriteInfo['name'] = name
            spriteInfo['school'] = school
            spriteInfo['seatName'] = multiCarrierData.get('seatName', [])[index - 1]
            seatInfoList.append(spriteInfo)

        self.widget.seatMC.seatListMC.dataArray = seatInfoList

    def handleWheel(self, *args):
        e = ASObject(args[3][0])

    def reset(self):
        self.showSetting = False
        self.multiCarrierNo = None
        self.carrierType = uiConst.MULTI_CARRIER_NORMAL

    def resetSettingVisible(self):
        self.widget.listBottonMC.visible = self.showSetting
        self.widget.seatMC.visible = self.showSetting
        self.widget.carrierSettingBtn.selected = self.showSetting
        if self.carrierType == uiConst.MULTI_CARRIER_NORMAL:
            self.widget.seatMC.qualificationBtn.visible = False
        else:
            self.widget.seatMC.qualificationBtn.visible = True

    def _onReleaseCarrierBtnClick(self, e):
        multiCarrierReleaseConfirmMsg = SCD.data.get('multiCarrierReleaseConfirmMsg', gameStrings.TEXT_MULTICARRIERPROXY_308)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierReleaseConfirmMsg, self.realReleaseCarrierBtnClick)

    def realReleaseCarrierBtnClick(self):
        p = BigWorld.player()
        gamelog.debug('-----m.l@MultiCarrierProxy._onReleaseCarrierBtnClick', self.carrier)
        if self.carrierType == uiConst.MULTI_CARRIER_NORMAL:
            if self.carrier.isReadyState():
                p.cell.cancelCheckReadyStateByHeader()
            elif self.carrier.isRunningState():
                p.cell.disbandCarrierByHeader()
        else:
            p.cell.applyDisbandWingWorldCarrier()

    def _onStartCarrierBtnClick(self, e):
        gamelog.debug('-----m.l@MultiCarrierProxy._onStartCarrierBtnClick')
        BigWorld.player().cell.startCarrierByHeader()

    def _onLeaveCarrierBtnClick(self, e):
        p = BigWorld.player()
        gamelog.debug('-----m.l@MultiCarrierProxy._onLeaveCarrierBtnClick', self.carrier.get(p.id))
        if self.carrierType == uiConst.MULTI_CARRIER_NORMAL:
            if self.carrier.get(p.id) and self.carrier.isRunningState():
                p.cell.applyLeaveCarrier()
            else:
                p.cell.cancelSelfReadyState()
        else:
            dist = p.qinggongMgr.getDistanceFromGround()
            if dist != p.flyHeight and dist < WWCD.data.get('heightForLeaveCarrier', 5):
                p.cell.applyLeaveWingWorldCarrier()
            else:
                p.showGameMsg(GMDD.data.UNABLE_TO_LEAVE_CARRIER, ())

    def _onGoBackCarrierBtnClick(self, e):
        p = BigWorld.player()
        gamelog.debug('-----m.l@MultiCarrierProxy._onGoBackCarrierBtnClick', self.carrier.carrierState)
        if self.carrier.isReadyState():
            multiCarrierGoBackReadyConfirmMsg = SCD.data.get('multiCarrierGoBackReadyConfirmMsg', gameStrings.TEXT_MULTICARRIERPROXY_348)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierGoBackReadyConfirmMsg, p._comfirmInviteCheckCarrierReady)
        else:
            BigWorld.player().cell.applyEnterCarrier()

    def _onCarrierSettingBtnClick(self, e):
        gamelog.debug('-----m.l@MultiCarrierProxy._onCarrierSettingBtnClick', self.showSetting)
        self.showSetting = not self.showSetting
        self.resetSettingVisible()
        if self.showSetting:
            self.refreshSeatSettingList()

    def showFunc1Btn(self, show):
        self.widget.func1Btn.visible = show

    def _onQualificationBtnClick(self, e):
        if gameglobal.rds.ui.multiCarrierQualification.widget:
            gameglobal.rds.ui.multiCarrierQualification.hide()
        else:
            gameglobal.rds.ui.multiCarrierQualification.show()
