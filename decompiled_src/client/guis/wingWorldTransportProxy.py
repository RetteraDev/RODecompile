#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldTransportProxy.o
import BigWorld
from Scaleform import GfxValue
import const
import gametypes
import gameglobal
import uiConst
import events
import utils
import gamelog
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis import ui
from data import wing_world_city_data as WWCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class WingWorldTransportProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldTransportProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.gotoCityId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_TRANSPORT, self.hide)

    def reset(self):
        self.cityList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_TRANSPORT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_TRANSPORT)

    def show(self):
        p = BigWorld.player()
        if p.wingWorld.state >= gametypes.WING_WORLD_STATE_SETTLEMENT:
            return False
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_TRANSPORT)
            return True

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        self.widget.dropDown.labelFunction = self.labelFunction
        self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.onTargetCityChange)

    def labelFunction(self, *args):
        item = ASObject(args[3][0])
        return GfxValue(ui.gbk2unicode(item[0]))

    def onTargetCityChange(self, *args):
        self.refreshBoxState()

    def refreshBoxState(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
            return
        signStartCrontab, pullStartCrontab, signEndCrontab = gameglobal.rds.ui.wingWorldPush.getSignCrontab()
        selectedIdx = int(self.widget.dropDown.selectedIndex)
        if selectedIdx >= 0 and selectedIdx < len(self.cityList):
            _, cityId = self.cityList[selectedIdx]
            if p.isWingWorldCampMode():
                selfSide = p.wingWorld.country.getOwnCamp()
            else:
                selfSide = p.wingWorld.country.getOwn()
            if cityId in selfSide.ownedCityIds:
                if getattr(p, 'wingWorldQueueState', 0) == gametypes.WING_WORLD_SIGN_AND_QUEUE_STATE_SIGN:
                    if cityId == p.wwSignAndQueueCityId:
                        self.widget.yesBtn.label = gameStrings.WING_WORLD_QUIT_SIGN
                    else:
                        self.widget.yesBtn.label = gameStrings.FIGHT_FOR_LOVE_APPLY
                elif cityId == p.wwSignAndQueueCityId:
                    self.widget.yesBtn.label = gameStrings.WING_WORLD_QUIT_QUEUE
                else:
                    self.widget.yesBtn.label = gameStrings.WING_WORLD_ENTER
            elif getattr(p, 'wingWorldQueueState', 0) in gametypes.WING_WORLD_SIGN_AND_QUEUE_SIGN_STATES:
                if cityId == p.wwSignAndQueueCityId:
                    self.widget.yesBtn.label = gameStrings.WING_WORLD_QUIT_SIGN
                else:
                    self.widget.yesBtn.label = gameStrings.FIGHT_FOR_LOVE_APPLY
            elif cityId == p.wwSignAndQueueCityId:
                self.widget.yesBtn.label = gameStrings.WING_WORLD_QUIT_QUEUE
            else:
                self.widget.yesBtn.label = gameStrings.WING_WORLD_ENTER

    def getCityList(self):
        p = BigWorld.player()
        cityList = []
        if p.isWingWorldCampMode():
            selfSide = p.wingWorld.country.getOwnCamp()
            selfPostId = p.wingWorldPostId
        else:
            selfSide = p.wingWorld.country.getOwn()
            selfPostId = p.wingWorldPostId
        declaredCityId2PostId = selfSide.declaredCityId2PostId
        allowAttackCityIds = selfSide.allowAttackCityIds[:]
        ownedCityIds = selfSide.ownedCityIds[:]
        for declaredCityId, postId in declaredCityId2PostId.iteritems():
            if gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
                if declaredCityId not in allowAttackCityIds:
                    allowAttackCityIds.append(declaredCityId)
            elif declaredCityId not in allowAttackCityIds and selfPostId == postId:
                allowAttackCityIds.append(declaredCityId)

        for attackCityId in allowAttackCityIds:
            if p.isWingGatherCity(attackCityId):
                cityName = gameStrings.WING_WORLD_ATT_GATHER % WWCD.data.get(attackCityId, {}).get('name', '')
            else:
                cityName = gameStrings.WING_WORLD_ATTACK % WWCD.data.get(attackCityId, {}).get('name', '')
            cityList.append((cityName, attackCityId))

        for defendCityId in ownedCityIds:
            if p.isWingGatherCity(defendCityId):
                cityName = gameStrings.WING_WORLD_DEF_GATHER % WWCD.data.get(defendCityId, {}).get('name', '')
            else:
                cityName = gameStrings.WING_WORLD_DEFEND % WWCD.data.get(defendCityId, {}).get('name', '')
            cityList.append((cityName, defendCityId))

        cityList.sort(cmp=self.sortCityList)
        cityList = [ (cityName, cityId) for cityName, cityId in cityList if not p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).isDirectSettlement ]
        return cityList

    def sortCityList(self, item1, item2):
        p = BigWorld.player()
        if p.isWingGatherCity(item1[1]):
            return -1
        if p.isWingGatherCity(item2[1]):
            return 1
        return 0

    def refreshInfo(self):
        if not self.widget:
            return
        self.cityList = self.getCityList()
        ASUtils.setDropdownMenuData(self.widget.dropDown, self.cityList)
        self.widget.dropDown.selectedIndex = 0
        self.refreshBoxState()

    def handleYesBtnClick(self, *args):
        selectedIdx = int(self.widget.dropDown.selectedIndex)
        p = BigWorld.player()
        gamelog.info('jbx:handleYesBtnClick', selectedIdx, len(self.cityList))
        if selectedIdx >= 0 and selectedIdx < len(self.cityList):
            _, cityId = self.cityList[selectedIdx]
            if p.isWingWorldCampMode():
                selfSide = p.wingWorld.country.getOwnCamp()
            else:
                selfSide = p.wingWorld.country.getOwn()
            if gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
                if p.wwSignAndQueueCityId:
                    if cityId == p.wwSignAndQueueCityId:
                        p.showConfirmQuitWingWorldQueueV2()
                    else:
                        p.teleportToWingWarCity(cityId)
                else:
                    p.teleportToWingWarCity(cityId)
                    self.hide()
            elif cityId not in selfSide.allowAttackCityIds and cityId not in selfSide.ownedCityIds:
                msg = GMD.data.get(GMDD.data.WING_WORLD_OPEN_ATTACK_CONFIRM, {}).get('text', '')
                fun = Functor(self.confirmOpenAttack, cityId)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, fun)
            else:
                p.teleportToWingWarCity(cityId)
                self.hide()

    def confirmOpenAttack(self, cityId):
        self.gotoCityId = cityId
        BigWorld.player().cell.wingWorldOpenAttackCity()
        self.hide()

    def handleNoBtnClick(self, *args):
        gamelog.info('jbx:handleNoBtnClick')
        self.hide()
