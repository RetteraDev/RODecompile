#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldStrategyProxy.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import events
import const
import wingWorldUtils
import utils
from gamestrings import gameStrings
import gametypes
import gameconfigCommon
import gameglobal
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import wing_world_city_data as WWCD
from data import wing_world_config_data as WWCFGD
from data import region_server_config_data as RSCD
POST_ID_TO_FRAME_NAME_DIC = {1: 'shengjian',
 2: 'yanchui',
 3: 'shuangji'}
WING_WORLD_LEADER_POST_MAX_ID = 19
WING_WORLD_CAMP_LEADER_POST_MAX_ID = 23
CAMP_IMPAGE_PATH = 'wingWorld/wingWorldFlag/%s.dds'

class WingWorldStrategyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldStrategyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedCityKey = 0
        self.mapIconList = []
        self.widget = None
        self.lastSelectedWeek = None
        self.isExpand = True
        self.lastSelectedIcon = None

    def initPanel(self, widget):
        gamelog.info('jbx:initPanel')
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        p = BigWorld.player()
        if p.isWingWorldLeader():
            gamelog.info('jbx:queryWingWorldResume', p.wingWorld.state, p.wingWorld.country, p.wingWorld.cityVer, p.wingWorld.campVer)
            p.cell.queryWingWorldResume(p.wingWorld.state, p.wingWorld.briefVer, p.wingWorld.countryVer, p.wingWorld.cityVer, p.wingWorld.campVer)
        p.cell.queryWingWorldShiliHistory()

    def initUI(self):
        self.widget.funcBtn.addEventListener(events.BUTTON_CLICK, self.handleFuncBtnClick, False, 0, True)
        self.widget.map.mapIcon.fitSize = True
        self.widget.map.mapIcon.loadImage('wingWorld/%s.dds' % WWCFGD.data.get('wingWorldStrategyMap', ''))
        self.widget.txt2.visible = False
        self.widget.txt3.visible = False
        self.widget.iconCost0.visible = False
        self.widget.iconCost1.visible = False
        self.widget.iconCost2.visible = False
        self.widget.point1.visible = False
        self.widget.gatherBtn.visible = False
        self.widget.gatherBtn.addEventListener(events.BUTTON_CLICK, self.onGatherBtnClick, False, 0, True)
        self.widget.historyBtn.expandBtn.addEventListener(events.MOUSE_CLICK, self.handleHistoryBtnClick, False, 0, True)
        self.widget.historyBtn.expandMc.gotoAndPlay('open')
        if BigWorld.player().isWingWorldCampMode():
            self.widget.colorTitle.text = gameStrings.WING_WORLD_STRATEGY_CAMP
            camp = BigWorld.player().wingWorldCamp
            if camp == 1:
                selfColor, alpah = gametypes.WING_WORLD_WAR_CAMP_1_COLOR
            elif camp == 2:
                selfColor, alpah = gametypes.WING_WORLD_WAR_CAMP_2_COLOR
            else:
                self.widget.countryColor.visible = False
                self.widget.colorTitle.text = gameStrings.WING_WORLD_STRATEGY_NOCAMP
                selfColor, alpah = gametypes.WING_WORLD_WAR_CAMP_NO_COLOR
        else:
            self.widget.colorTitle.text = gameStrings.WING_WORLD_STRATEGY_COUNTRY
            selfColor, alpah = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldCountryColor', ('FFFFFF', 0.5))
        ASUtils.addColorMask(self.widget.countryColor, selfColor, alpah)

    def unRegisterPanel(self):
        gamelog.info('jbx:unRegisterPanel', self.widget)
        if self.widget and self.widget.map:
            for iconMc in self.mapIconList:
                self.widget.cities.removeChild(iconMc)

        self.reset()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshCityMap()
        self.refreshCityInfo()
        self.refreshWingWorldHistory()

    def canGather(self):
        p = BigWorld.player()
        return wingWorldUtils.isArmyFirstLeader(p.wingWorldPostId)

    def refreshCityInfo(self):
        p = BigWorld.player()
        wingWorld = p.wingWorld
        gamelog.info('jbx:refreshCityInfo', self.selectedCityKey)
        self.widget.funcBtn.visible = True
        self.widget.gatherBtn.visible = False
        if not self.selectedCityKey:
            self.widget.txtCityName.text = gameStrings.WING_WORLD_TAB_STRATEGY_NOT_SELECTED
            self.widget.txtLv.text = ''
            self.widget.txtCountryName.text = ''
            self.widget.txtLeaderName.text = ''
            self.widget.txt0.visible = False
            self.widget.txt1.visible = False
            self.widget.txtCost0.text = ''
            self.widget.txtCost1.text = ''
            self.widget.txtCost2.text = ''
            self.widget.txtState.text = gameStrings.WING_WORLD_TAB_STRATEGY_NOT_SELECTED_CITY
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
            self.widget.txtBeClareCnt.text = ''
            self.widget.txtBeClare.visible = False
            self.widget.txt3.visible = False
            self.widget.point0.visible = False
            self.widget.points.visible = False
            return
        self.widget.icon.visible = True
        self.widget.txt0.visible = True
        self.widget.txt1.visible = True
        self.widget.txt3.visible = True
        self.widget.point0.visible = True
        self.widget.points.visible = True
        cfgData = WWCD.data.get(self.selectedCityKey, {})
        self.widget.txtCityName.text = cfgData.get('name', '')
        cityLevel = cfgData.get('level', 1)
        self.widget.txtLv.text = WWCFGD.data.get('cityLevelDesc', {}).get(cityLevel, str(cityLevel))
        self.widget.txtCost0.text = ''
        self.widget.txtCost1.text = ''
        self.widget.txtCost2.text = ''
        self.refrshCountryInfo(self.selectedCityKey)
        if self.lastSelectedWeek:
            self.widget.txtCost0.text = ''
            self.widget.txtCost1.text = ''
            self.widget.txtCost2.text = ''
            self.widget.txtState.text = ''
            self.widget.funcBtn.visible = False
            self.widget.line1.visible = False
            self.widget.icon.visible = False
            self.widget.txtBeClareCnt.text = ''
            self.widget.txtBeClare.visible = False
            self.widget.txt2.visible = False
            self.widget.point0.visible = False
            return
        self.widget.line1.visible = True
        self.widget.point0.visible = True
        if p.isWingWorldCampMode():
            selfSide = wingWorld.country.getOwnCamp()
        else:
            selfSide = wingWorld.country.getOwn()
        ownCityIds = selfSide.ownedCityIds
        isDeclared = self.isDecleared(self.selectedCityKey)
        isCityLinkable = self.isCityLinkable(ownCityIds, self.selectedCityKey, p.getWingWorldGroupId())
        isLowerCityOccupyed = self.isLowerCityOccupyed(ownCityIds, self.selectedCityKey, p.getWingWorldGroupId())
        isLvOk = self.checkTargetCityLv(ownCityIds, self.selectedCityKey)
        isResourcesOk = self.checkResources(self.selectedCityKey)
        isCntFull = self.checkCntFull(self.selectedCityKey)
        isCntRealFull = self.checkCntRealFull(self.selectedCityKey)
        isSeasonStepOk, reason = self.checkSeasonStep(self.selectedCityKey)
        isInTime = self.checkDeclareTime()
        isLeader = p.isWingWorldLeader()
        isSwallowed = self.checkSwallowed(self.selectedCityKey)
        self.widget.funcBtn.label = gameStrings.WING_WORLD_ATTACK_DECLARE
        if not isSeasonStepOk:
            self.widget.icon.visible = False
            self.widget.funcBtn.enabled = False
            self.widget.txtState.text = WWCFGD.data.get('wingWorldSeasonStepTexts', {}).get(reason, '')
        if isLeader:
            self.widget.icon.visible = True
            if p.isWingWorldCampMode():
                self.widget.icon.visible = False
            else:
                self.widget.icon.gotoAndPlay(POST_ID_TO_FRAME_NAME_DIC[p.wingWorldPostId])
        else:
            self.widget.icon.visible = False
        if not wingWorldUtils.isCityOpen(p.getWingWorldGroupId(), self.selectedCityKey):
            self.widget.txtState.text = gameStrings.WING_WORLD_CITY_CANT_DECLARE_NOT_OPEN
            self.widget.funcBtn.enabled = False
        elif self.isSelfCity(self.selectedCityKey):
            self.widget.txtState.text = gameStrings.WING_WORLD_TAB_STRATEGY_CITY_SELF
            self.widget.funcBtn.enabled = False
            if gameglobal.rds.configData.get('enableWingWorldArmyGather', False):
                if not isSwallowed and self.canGather():
                    wingWorldState = BigWorld.player().wingWorld.state
                    if gametypes.WING_WORLD_STATE_DECLARE < wingWorldState < gametypes.WING_WORLD_STATE_SETTLEMENT:
                        self.widget.gatherBtn.visible = True
                        gatherCity = p.getWingGatherCityId()
                        if gatherCity and gatherCity == self.selectedCityKey:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_CANCEL_GATHER
                        elif gatherCity:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_GATHER
                        else:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_GATHER
        elif isDeclared:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARED
            self.widget.funcBtn.enabled = False
            declaredPostId = selfSide.getDeclaredCityPostId(self.selectedCityKey)
            if declaredPostId:
                self.widget.icon.visible = True
                if p.isWingWorldCampMode():
                    self.widget.icon.visible = False
                else:
                    frameName = POST_ID_TO_FRAME_NAME_DIC[declaredPostId] + 'disable'
                    self.widget.icon.gotoAndPlay(frameName)
            else:
                self.widget.icon.visible = False
                self.widget.txtState.text = gameStrings.WING_WORLD_DECLARED_OTHER_CITY
            if gameglobal.rds.configData.get('enableWingWorldArmyGather', False):
                if not isSwallowed and self.canGather():
                    wingWorldState = BigWorld.player().wingWorld.state
                    if gametypes.WING_WORLD_STATE_DECLARE < wingWorldState < gametypes.WING_WORLD_STATE_SETTLEMENT:
                        self.widget.gatherBtn.visible = True
                        gatherCity = p.getWingGatherCityId()
                        if gatherCity and gatherCity == self.selectedCityKey:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_CANCEL_GATHER
                        elif gatherCity:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_GATHER
                        else:
                            self.widget.gatherBtn.label = gameStrings.WING_WORLD_GATHER
        elif isSwallowed:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_SWALLOWED
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
        elif not p.isWingWorldLeader():
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_NOT_LEADER
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
        elif not isInTime:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_NOT_IN_TIME
            self.widget.funcBtn.enabled = False
        elif not isResourcesOk:
            self.widget.txtState.text = gameStrings.WING_WORLD_RESOURCES_NOT_ENOUGH
            self.widget.funcBtn.enabled = False
        elif isCntRealFull:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_CNT_FULL
            self.widget.funcBtn.enabled = False
        elif isCntFull:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_NOT_OPEN
            self.widget.funcBtn.enabled = False
        elif not p.isWingWorldCampMode() and self.selectedCityKey in selfSide.lostCityIdsLastWeek:
            self.widget.txtState.text = ''
            self.widget.funcBtn.enabled = True
            self.widget.icon.visible = True
            self.widget.funcBtn.label = gameStrings.WING_WORLD_COUNTER_ATTACK
        elif not isCityLinkable:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_NOT_CONNECTED
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
        elif not isLvOk:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_LOW_LV
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
        elif not isLowerCityOccupyed:
            self.widget.txtState.text = gameStrings.WING_WORLD_DECLARE_NEED_OCCUPY_LOWER
            self.widget.funcBtn.enabled = False
            self.widget.icon.visible = False
        else:
            self.widget.txtState.text = ''
            self.widget.funcBtn.enabled = True
        city = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, self.selectedCityKey)
        if not p.isWingWorldCampMode() and city.ownerHostId == p.getOriginHostId() and p.wingWorldPostId and p.wingWorldPostId <= 3 and gametypes.WING_WORLD_STATE_DECLARE <= p.wingWorld.state <= gametypes.WING_WORLD_STATE_OPEN:
            self.widget.txtBeClareCnt.text = gameStrings.WING_WORLD_BE_DECLAR % city.declaredNum if city.declaredNum else gameStrings.WING_WORLD_NOT_BE_DECLAR
            self.widget.txtBeClare.visible = True
            self.widget.point0.visible = True
        else:
            self.widget.txtBeClareCnt.text = ''
            self.widget.txtBeClare.visible = False
            self.widget.point0.visible = False
        if self.widget.txtState.visible:
            ASUtils.autoSizeWithFont(self.widget.txtState, 14, 221, 10)

    def refrshCountryInfo(self, cityId):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            self.widget.txt0.text = gameStrings.WING_WORLD_OCCUPY_CAMP
            self.widget.txt1.text = gameStrings.WING_WORLD_CAMP_LEADER
            if self.lastSelectedWeek:
                cityInfo = wingWorldUtils.getCityOwnerHostIdByWeek(cityId, self.lastSelectedWeek)
                kingName = cityInfo[3]
                self.widget.txtCountryName.text = cityInfo[1]
            else:
                if p.wingWorld.state in (gametypes.WING_WORLD_STATE_DECLARE_END, gametypes.WING_WORLD_STATE_OPEN, gametypes.WING_WORLD_STATE_SETTLEMENT) and p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId:
                    ownerCampId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId
                else:
                    ownerCampId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId).ownerHostId
                kingName = p.wingWorld.getCityKingName(ownerCampId) if ownerCampId else ''
                self.widget.txtCountryName.text = utils.getWingCampName(ownerCampId) if ownerCampId else gameStrings.WING_WORLD_NO_OWNER
            self.widget.txtLeaderName.text = kingName if kingName else gameStrings.WING_WORLD_NO_OWNER
        else:
            self.widget.txt0.text = gameStrings.WING_WORLD_OCCUPY_COUNTRY
            self.widget.txt1.text = gameStrings.WING_WORLD_COUNTRY_LEADER
            if self.lastSelectedWeek:
                cityInfo = wingWorldUtils.getCityOwnerHostIdByWeek(cityId, self.lastSelectedWeek)
                kingName = cityInfo[3]
                self.widget.txtCountryName.text = cityInfo[1]
            else:
                if p.wingWorld.state in (gametypes.WING_WORLD_STATE_DECLARE_END, gametypes.WING_WORLD_STATE_OPEN, gametypes.WING_WORLD_STATE_SETTLEMENT) and p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId:
                    ownerHostId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId
                else:
                    ownerHostId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId).ownerHostId
                kingName = p.wingWorld.getCityKingName(ownerHostId) if ownerHostId else ''
                self.widget.txtCountryName.text = RSCD.data.get(ownerHostId, {}).get('serverName', gameStrings.WING_WORLD_NO_OWNER)
            self.widget.txtLeaderName.text = kingName if kingName else gameStrings.WING_WORLD_NO_OWNER

    def isDecleared(self, cityId):
        p = BigWorld.player()
        wingWorld = p.wingWorld
        if self.isInShowDeclareStates():
            if p.isWingWorldCampMode():
                selfSide = wingWorld.country.getOwnCamp()
                return p.isWingWorldLeader() and selfSide.isDeclaredCity(cityId) or p.wingWorldPostId in selfSide.declaredCityId2PostId.values()
            else:
                selfSide = wingWorld.country.getOwn()
                return p.isWingWorldLeader() and selfSide.isDeclaredCity(cityId) or p.wingWorldPostId in selfSide.declaredCityId2PostId.values()
        return False

    def checkTargetCityLv(self, ownCityIds, cityId):
        if gameconfigCommon.enableWingWorldDeclareNewLink():
            return True
        maxLv = 0
        for ownCityId in ownCityIds:
            maxLv = max(WWCD.data.get(ownCityId, {}).get('level', 0), maxLv)

        maxLv += 1
        targetCityLv = WWCD.data.get(cityId, {}).get('level', 1)
        return maxLv >= targetCityLv

    def checkResources(self, cityId):
        return True

    def checkCntFull(self, cityId):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            return False
        ownCountry = p.wingWorld.country.getOwn()
        canDeclaeNum = ownCountry.getCanDeclareNum(p.getWingWorldGroupId())
        if canDeclaeNum == 1 and p.wingWorldPostId != wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID:
            return True
        else:
            return canDeclaeNum < 3 and len(ownCountry.declaredCityId2PostId) >= canDeclaeNum

    def checkSeasonStep(self, cityId):
        p = BigWorld.player()
        cityLv = WWCD.data.get(cityId, {}).get('level', 0)
        seasonStep = p.wingWorld.step
        if seasonStep == gametypes.WING_WORLD_SEASON_STEP_CLOSE:
            return (False, gametypes.WING_WORLD_SEASON_STEP_CLOSE)
        elif gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 <= seasonStep <= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_4:
            if p.isWingWorldCampMode():
                return (True, cityLv)
            return (seasonStep >= cityLv, cityLv)
        elif seasonStep == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
            return (False, gametypes.WING_WORLD_SEASON_STEP_CELEBRATION)
        else:
            return (False, gametypes.WING_WORLD_SEASON_STEP_ADJOURNING)

    def checkCntRealFull(self, cityId):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            return False
        ownCountry = p.wingWorld.country.getOwn()
        city = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId)
        cityDeclaredNum = city.declaredNum
        return len(ownCountry.declaredCityId2PostId) >= 3 or city.ownerHostId and cityDeclaredNum >= 2 or not city.ownerHostId and cityDeclaredNum >= 3

    def isSelfCity(self, cityId):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            isSelfCity = p.wingWorldCamp and wingWorldUtils.getCityOwnerHostId(cityId) == p.wingWorldCamp
        else:
            isSelfCity = wingWorldUtils.getCityOwnerHostId(cityId) == p.getOriginHostId()
        return isSelfCity

    def isInShowDeclareStates(self):
        p = BigWorld.player()
        return p.wingWorld.state in (gametypes.WING_WORLD_STATE_DECLARE,
         gametypes.WING_WORLD_STATE_DECLARE_END,
         gametypes.WING_WORLD_STATE_OPEN,
         gametypes.WING_WORLD_STATE_SETTLEMENT)

    def refreshCityMap(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            wingWorld = BigWorld.player().wingWorld
            for iconMc in self.mapIconList:
                self.widget.cities.removeChild(iconMc)

            self.mapIconList = []
            if not self.lastSelectedWeek and gametypes.WING_WORLD_STATE_DECLARE <= wingWorld.state <= gametypes.WING_WORLD_STATE_SETTLEMENT:
                attackCityIdList, defenedCityIdList = self.getAttackAndDefCityIdList()
            else:
                attackCityIdList, defenedCityIdList = [], []
            for cityId, cfgData in WWCD.data.iteritems():
                iconMc = None
                cityMc = self.widget.getChildByName('city%d' % cityId)
                cloudMc = self.widget.getChildByName('cloud%d' % cityId)
                ASUtils.setHitTestDisable(cityMc, True)
                cityDetail = ''
                if not self.lastSelectedWeek:
                    ownerId = wingWorldUtils.getCityOwnerHostId(cityId)
                    isSwallowed = wingWorldUtils.isCitySwallow(p.getWingWorldGroupId(), cityId)
                    nextSwallowTime = wingWorldUtils.getNextSwallowTime(p.getWingWorldGroupId(), cityId)
                else:
                    currentSeasonRecord = getattr(p, 'currentSeasonRecord', [None] * gametypes.WING_WORLD_BATTLE_MAX_CNT)
                    weekTime = currentSeasonRecord[self.lastSelectedWeek - 1][0]
                    ownerId = wingWorldUtils.getCityOwnerHostIdByWeek(cityId, self.lastSelectedWeek)[0]
                    isSwallowed = wingWorldUtils.isCitySwallowed(p.getWingWorldGroupId(), cityId, weekTime)
                    nextSwallowTime = -1
                if isSwallowed:
                    iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack7')
                    cityMc.visible = False
                    if iconMc.swallowMc:
                        iconMc.removeChild(iconMc.swallowMc)
                    if cloudMc:
                        ASUtils.setHitTestDisable(cloudMc, True)
                        cloudMc.visible = True
                        cloudMc.gotoAndPlay(0)
                    cityDetail = '(%s)' % gameStrings.WING_WORLD_CAMP_SWALLOWED
                else:
                    if cloudMc:
                        cloudMc.visible = False
                    if p.isWingWorldCampMode():
                        ownerCamp = ownerId
                        cityMc.visible = True
                        if ownerCamp == 1:
                            iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack2')
                            color, alpha = gametypes.WING_WORLD_WAR_CAMP_1_COLOR
                            ASUtils.addColorMask(cityMc, color, alpha)
                        elif ownerCamp == 2:
                            iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack5')
                            color, alpha = gametypes.WING_WORLD_WAR_CAMP_2_COLOR
                            ASUtils.addColorMask(cityMc, color, alpha)
                        else:
                            iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack7')
                            cityMc.visible = False
                    else:
                        cityMc.visible = True
                        if not self.lastSelectedWeek:
                            ownerHostId = wingWorldUtils.getCityOwnerHostId(cityId)
                        else:
                            ownerHostId = wingWorldUtils.getCityOwnerHostIdByWeek(cityId, self.lastSelectedWeek)[0]
                        if ownerHostId:
                            iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack%d' % RSCD.data.get(ownerHostId, {}).get('iconType', 1))
                            color, alpha = RSCD.data.get(ownerHostId, {}).get('wingWorldCountryColor', ('ffffff', 0.5))
                            ASUtils.addColorMask(cityMc, color, alpha)
                        else:
                            iconMc = self.widget.getInstByClsName('WingWorldStrateg_Attack7')
                            cityMc.visible = False
                if iconMc.swallowMc:
                    iconMc.removeChild(iconMc.swallowMc)
                if nextSwallowTime != -1 and not isSwallowed:
                    if nextSwallowTime - utils.getNow() < 7 * const.TIME_INTERVAL_DAY:
                        swallowMc = self.widget.getInstByClsName('WingWorldStrateg_SwallowIcon')
                        iconMc.addChild(swallowMc)
                        swallowMc.x = 51
                        swallowMc.y = 94
                        swallowMc.width = 30
                        swallowMc.height = 27
                        swallowMc.name = 'swallowMc'
                        TipManager.addTip(swallowMc, gameStrings.WING_WORLD_CAMP_WILL_SWALLOW)
                        cityDetail = '(%s)' % (gameStrings.WING_WORLD_CAMP_WILL_SWALLOW_THIS_WEEK % utils.formatDatetimeWithoutHour(nextSwallowTime))
                    elif nextSwallowTime - utils.getNow() < 14 * const.TIME_INTERVAL_DAY:
                        swallowMc = self.widget.getInstByClsName('WingWorldStrateg_SwallowIcon')
                        iconMc.addChild(swallowMc)
                        swallowMc.x = 55
                        swallowMc.y = 94
                        swallowMc.width = 20
                        swallowMc.height = 18
                        swallowMc.name = 'swallowMc'
                        TipManager.addTip(swallowMc, gameStrings.WING_WORLD_CAMP_WILL_SWALLOW2)
                        cityDetail = '(%s)' % (gameStrings.WING_WORLD_CAMP_WILL_SWALLOW_NEXT_WEEK % utils.formatDatetimeWithoutHour(nextSwallowTime))
                iconMc.iconarmy.visible = False
                if cityId in attackCityIdList:
                    iconMc.iconarmy.visible = True
                    if p.isWingWorldCampMode():
                        iconMc.iconarmy.gotoAndStop('camp')
                        iconMc.iconarmy.icon.fitSize = True
                        camp = getattr(p, 'wingWorldCamp', 0)
                        campIconName = WWCD.data.get('wingCampIcons', gameStrings.WING_WORLD_CAMP_ICONS).get(camp, '')
                        iconMc.iconarmy.icon.loadImage(CAMP_IMPAGE_PATH % campIconName)
                    else:
                        postId = wingWorld.country.getOwn().getDeclaredCityPostId(cityId)
                        iconMc.iconarmy.gotoAndStop(POST_ID_TO_FRAME_NAME_DIC.get(postId, ''))
                elif cityId in defenedCityIdList:
                    iconMc.iconarmy.visible = True
                    iconMc.iconarmy.gotoAndStop('defence')
                self.widget.cities.addChild(iconMc)
                iconMc.name = 'city%d' % cityId
                iconMc.data = cityId
                self.mapIconList.append(iconMc)
                pos = cfgData.get('pos', (619 / 15 * cityId - 90, 520 / 15 * cityId - 90))
                iconMc.x = pos[0]
                iconMc.y = pos[1]
                iconMc.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)
                TipManager.addTip(iconMc.icon, WWCD.data.get(cityId, {}).get('name', '') + cityDetail)

            return

    def refreshWingWorldHistory(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            currentSeasonRecord = getattr(p, 'currentSeasonRecord', [None] * gametypes.WING_WORLD_BATTLE_MAX_CNT)
            for i in xrange(gametypes.WING_WORLD_BATTLE_MAX_CNT):
                if i < gametypes.WING_WORLD_BATTLE_MAX_CNT / 2:
                    weekMc = self.widget.historyBtn.expandMc.progress.left.getChildByName('week%d' % (i + 1))
                else:
                    weekMc = self.widget.historyBtn.expandMc.progress.right.getChildByName('week%d' % (i + 1))
                weekMc.addEventListener(events.MOUSE_CLICK, self.handleWeekClick, False, 0, True)
                weekMc.week = i + 1
                if not currentSeasonRecord[i]:
                    weekMc.gotoAndStop('normal')
                    ASUtils.setHitTestDisable(weekMc, True)
                else:
                    ASUtils.setHitTestDisable(weekMc, False)
                    if self.lastSelectedWeek == i + 1:
                        weekMc.gotoAndStop('selected')
                        weekMc.txt0.text = gameStrings.WING_WORLD_WEEK_TIME % (i + 1)
                        weekMc.txt1.text = utils.formatDatetime(currentSeasonRecord[i][0])
                    else:
                        weekMc.gotoAndStop('pass')

            return

    def getAttackAndDefCityIdList(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            camp = p.wingWorld.country.getOwnCamp()
            declaredCityId2PostId = camp.declaredCityId2PostId
            allowAttackCityIds = camp.allowAttackCityIds[:]
            ownedCityIds = camp.ownedCityIds[:]
            hasPrivilege = p.wingWorldPostId and p.wingWorldPostId <= WING_WORLD_CAMP_LEADER_POST_MAX_ID
        else:
            country = p.wingWorld.country.getOwn()
            declaredCityId2PostId = country.declaredCityId2PostId
            allowAttackCityIds = country.allowAttackCityIds[:]
            ownedCityIds = country.ownedCityIds[:]
            hasPrivilege = p.wingWorldPostId and p.wingWorldPostId <= WING_WORLD_LEADER_POST_MAX_ID
        for declaredCityId, postId in declaredCityId2PostId.iteritems():
            if declaredCityId not in allowAttackCityIds and hasPrivilege:
                allowAttackCityIds.append(declaredCityId)

        ownedCityIds = [ cityId for cityId in ownedCityIds if not p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).isDirectSettlement and not self.checkSwallowed(cityId) ]
        return (allowAttackCityIds, ownedCityIds)

    def test1(self):
        p = BigWorld.player()
        wingWorld = p.wingWorld
        city = wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, 2)
        city.ownerHostId = 29032
        city.declaredNum = 1
        country = wingWorld.country.getCountry(city.ownerHostId)
        country.postInfo[wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID] = gameStrings.TEXT_WINGWORLDSTRATEGYPROXY_576
        selfCountry = wingWorld.country.getOwn()
        selfCountry.declaredCityId2PostId[2] = wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID
        selfCountry.postInfo[wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID] = p.roleName
        self.refreshInfo()

    def test2(self):
        p = BigWorld.player()
        cityList = [2, 3, 4]
        wingWorld = p.wingWorld
        for cityId in cityList:
            city = wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId)
            city.ownerHostId = 29032
            city.declaredNum = 1
            country = wingWorld.country.getCountry(city.ownerHostId)
            country.postInfo[wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID] = gameStrings.TEXT_WINGWORLDSTRATEGYPROXY_592 % cityId
            selfCountry = wingWorld.country.getOwn()
            selfCountry.declaredCityId2PostId[cityId] = wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID + (cityId - 2)
            selfCountry.postInfo[wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID + cityId - 2] = p.roleName

        self.refreshInfo()

    def isCityLinkable(self, ownCityIds, cityId, groupId):
        targetLv = WWCD.data.get(cityId, {}).get('level')
        if gameconfigCommon.enableWingWorldDeclareNewLink():
            return True
        if targetLv == 1:
            return True
        for selfCityId in ownCityIds:
            if wingWorldUtils.checkCityLinkable(selfCityId, cityId):
                return True

        return False

    def isLowerCityOccupyed(self, ownCityIds, cityId, groupId):
        if not gameconfigCommon.enableWingWorldDeclareNewLink():
            return True
        targetLv = WWCD.data.get(cityId, {}).get('level')
        if targetLv == 1:
            return True
        if targetLv <= wingWorldUtils.getMaxSwallowCityLevel(groupId) + 1:
            return True
        for selfCityId in ownCityIds:
            if abs(WWCD.data.get(selfCityId, {}).get('level', 0) - targetLv) <= 1:
                return True

        return False

    def checkDeclareTime(self):
        return BigWorld.player().wingWorld.state == gametypes.WING_WORLD_STATE_DECLARE

    def checkSwallowed(self, cityId):
        p = BigWorld.player()
        if gameconfigCommon.enableWingWorldSwallow():
            return wingWorldUtils.isCitySwallow(utils.getWingWorldGroupId(), cityId)
        else:
            return False

    def handleFuncBtnClick(self, *args):
        gamelog.info('jbx:handleFuncBtnClick')
        self.uiAdapter.wingWorldDeclareConfirm.show(self.selectedCityKey)

    def onGatherBtnClick(self, *args):
        p = BigWorld.player()
        gatherCity = p.getWingGatherCityId()
        if not self.selectedCityKey:
            return
        if gatherCity == self.selectedCityKey:
            p.cell.unApplyWingArmyGather()
        else:
            p.cell.applyWingArmyGather(self.selectedCityKey)

    def yesCallback(self):
        if not self.selectedCityKey:
            return
        BigWorld.player().cell.wingWorldDeclare(self.selectedCityKey)

    def handleIconClick(self, *args):
        e = ASObject(args[3][0])
        if self.lastSelectedIcon:
            self.lastSelectedIcon.icon.selected = False
        self.selectedCityKey = int(e.currentTarget.data)
        self.lastSelectedIcon = e.currentTarget
        self.lastSelectedIcon.icon.selected = True
        self.refreshCityInfo()

    def handleWeekClick(self, *args):
        e = ASObject(args[3][0])
        week = int(e.currentTarget.week)
        if week == self.lastSelectedWeek:
            return
        self.lastSelectedWeek = week
        self.refreshWingWorldHistory()
        self.selectedCityKey = 0
        self.refreshCityMap()
        self.refreshCityInfo()

    def handleHistoryBtnClick(self, *args):
        gamelog.info('jbx:handleHistoryBtnClick', self.widget.historyBtn.expandMc.currentFrameLabel)
        if self.isExpand:
            self.widget.historyBtn.expandMc.gotoAndPlay('back')
            self.isExpand = False
        else:
            self.widget.historyBtn.expandMc.gotoAndPlay('open')
            self.isExpand = True
        self.lastSelectedWeek = None
        self.selectedCityKey = None
        self.refreshCityMap()
        self.refreshCityInfo()
        self.refreshWingWorldHistory()

    def genTestLiShi(self, weekLen = 16):
        import utils
        hostIdList = [29031,
         10001,
         10108,
         10071,
         10031]
        startTime = utils.getNextCrontabTime('0 10 26 8 *')
        if utils.getYearInt(startTime) != utils.getYearInt(utils.getNow()):
            startTime = utils.getPreCrontabTime('0 10 26 8 *')
        weekList = []
        p = BigWorld.player()
        for i in xrange(weekLen):
            weekInfo = []
            for cityIdx in range(15):
                if cityIdx % 2 == 0:
                    hostId = hostIdList[cityIdx % 5]
                    weekInfo.append((cityIdx + 1,
                     hostId,
                     RSCD.data.get(hostId, {}).get('serverName', ''),
                     'guildName',
                     'leaderName'))

            weekList.append((startTime + 604800 * i, weekInfo))

        p.processHistoryRecords(weekList)
