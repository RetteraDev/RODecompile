#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapProxy.o
from gamestrings import gameStrings
import BigWorld
import GUI
import Math
import copy
from Scaleform import GfxValue
import gameconfigCommon
import gameglobal
import uiConst
import gametypes
import ui
import keys
import formula
import const
import utils
import gamelog
import wingWorldUtils
import clientUtils
import calendar
import datetime
import math
import pubgUtils
from guis import events
from guis.asObject import ASObject
from gamestrings import gameStrings
import commcalc
import commQuest
from guis import uiUtils
from guis import pinyinConvert
from uiProxy import UIProxy
from ui import gbk2unicode
from ui import unicode2gbk
from sfx import cameraEffect
from helpers import navigator
from callbackHelper import Functor
from guis import messageBoxProxy
from guis import cursor
from appSetting import Obj as AppSettings
from guis import asObject
from guis.asObject import ASUtils
from commonWingWorld import WWArmyPostVal
from guis import worldBossHelper
from data import clan_courier_data as CCD
from data import seeker_data as SD
from data import npc_model_client_data as NCD
from data import quest_data as QD
from data import quest_loop_data as QLD
from cdata import mapSearch_iii_data as MIII
from data import mapSearch_ii_data as MII
from data import map_sign_data as MSD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import map_func_config_data as MFCD
from cdata import transport_ref_data as TRD
from data import transport_data as TD
from data import sys_config_data as SYSD
from data import chunk_reverse_data as CRD
from data import clan_war_fort_data as CWFD
from data import map_guide_data as MGD
from data import world_area_state_data as WASD
from data import clan_war_marker_data as CWMD
from data import world_quest_data as WQD
from data import map_filter_config as MFC
from data import chunk_mapping_data as CMD
from data import guild_area_data as GAD
from data import guild_building_marker_data as GBMD
from data import guild_building_data as GBD
from data import guild_config_data as GCD
from data import battle_field_fort_data as BFFD
from data import battle_field_data as BFD
from data import play_recomm_activity_data as PRAD
from data import map_play_data as MPD
from data import world_war_fort_data as WWFD
from data import world_war_relive_board_data as WWRBD
from data import world_war_config_data as WWCD
from data import map_third_lv_data as MTLD
from data import fallen_red_guard_data as FRGD
from data import wing_world_country_flag_data as WWCFD
from data import wing_world_city_data as WWCITYD
from data import wing_city_building_data as WCBD
from data import wing_city_building_entity_data as WCBED
from data import wing_city_resource_data as WCRD
from data import wing_world_config_data as WWCFGD
from data import wing_world_city_data as WWCTD
from data import region_server_config_data as RSCD
from data import wing_world_config_data as WINGCD
from data import wing_soul_boss_data as WSBD
from data import monster_data as MD
from data import clan_war_fort_data as CWFD
from data import clan_war_event_limit_data as CWELD
from data import cross_clan_war_config_data as CCWCD
from data import clan_courier_config_data as CCCD
from data import duel_config_data as DCD
from data import map_config_data as MCD
from cdata import hunt_ghost_config_data as HGCD
completeResArr = SYSD.data.get('mapQuest', {}).get('complete', ())
unfinishedResArr = SYSD.data.get('mapQuest', {}).get('unfinished', ())
availableResArr = SYSD.data.get('mapQuest', {}).get('available', ())
chatResArr = SYSD.data.get('mapQuest', {}).get('chat', ['mapchatunfinished0'] * 9)
cltItemResArr = SYSD.data.get('mapQuest', {}).get('cltItem', ['mapComCltItemunfinished0'] * 9)
monsterResArr = SYSD.data.get('mapQuest', {}).get('monster', ['mapMonsterunfinished0'] * 9)
markNpcArr = SYSD.data.get('mapQuest', {}).get('markNpc', ['mapMarkNpcunfinished0'] * 9)
colItemTypeRes = {1: cltItemResArr,
 2: monsterResArr}
LEVEL_3_SIZE = (9600, 6400)
ICON_PATH = 'map/mapIcon/'
WING_WORLD_ICON_PATH = 'map/mapIcon/wingworld'
WING_WORLD_MARK_ICON_CNT = 4
MAP_LV_0 = 0
MAP_LV_1 = 1
MAP_LV_2 = 2
WORLD_MAP_NAME = 'ycdg'
PIC_UNIT_SIZE = (512, 512)
MARK_TYPE_TO_CURSOR_STATE = {0: ui.WING_WORLD_MARK0,
 1: ui.WING_WORLD_MARK1,
 2: ui.WING_WORLD_MARK2,
 3: ui.WING_WORLD_MARK3}
MARK_TYPE_TO_CURSOR_NAME = {0: cursor.cursor_wing_world_mark0,
 1: cursor.cursor_wing_world_mark1,
 2: cursor.cursor_wing_world_mark2,
 3: cursor.cursor_wing_world_mark3}
YELLOW_COLOR = '#e59545'
CAN_OCCUPY_BUILDING_COLOR = ('#99ebff', '#99ff9e', '#fd99ff')
BGMAP_CM_RELAYOUT_DATA = {'pubgPoisonMc': [True, 2],
 'airlineAllMc': [False, 1],
 'boundLineMc': [True, 1],
 'plantTreeAllAreaBoundMc': [False, 1],
 'huntGhostAllAreaBoundMc': [False, 1]}

class MapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeMap': self.onCloseMap,
         'registerMap': self.onRegisterMap,
         'getPlayerPos': self.onGetPlayerPos,
         'seekNpc': self.onSeekNpc,
         'seekPoint': self.onSeekPoint,
         'getCurrentMapInfo': self.onGetCurrentMapInfo,
         'getAreaInfo': self.onGetAreaInfo,
         'preLoadPic': self.onPreLoadPic,
         'getMapSign': self.onGetMapSign,
         'getTeamMate': self.onGetTeamMate,
         'refreshNpcInfo': self.onRefreshNpcInfo,
         'teleport': self.onTeleport,
         'getBindCash': self.onGetBindCash,
         'getStoneCost': self.onGetStoneCost,
         'transPos': self.onTransPos,
         'rTransPos': self.onRTransPos,
         'getSeekPoint': self.onGetSeekPoint,
         'getFortInfo': self.onGetFortInfo,
         'getSearchNpcNames': self.onGetSearchNpcNames,
         'getOptionVisible': self.onGetOptionVisible,
         'setLevel': self.onSetLevel,
         'clickReliveBoard': self.onClickReliveBoard,
         'modOptionVisible': self.onModOptionVisible,
         'getGuideData': self.onGetGuideData,
         'startMark': self.onStartMark,
         'addMapMark': self.onAddMapMark,
         'confirmMark': self.onConfirmMark,
         'closeMark': self.onCloseMark,
         'getMapMark': self.onGetMapMark,
         'editMark': self.onEditMark,
         'delMark': self.onDelMark,
         'getWorldQuest': self.onGetWorldQuest,
         'getNpcData': self.onGetNpcData,
         'getFogData': self.onGetFogData,
         'getBuildingData': self.onGetBuildingData,
         'broadCastSelf': self.onBroadCastSelf,
         'broadCastMark': self.onBroadCastMark,
         'updateTarget': self.updateTarget,
         'getPlayTipData': self.onGetPlayTipData,
         'refreshOtherIcon': self.onRefreshOtherIcon,
         'getPlayData': self.onGetPlayData,
         'setOptionMode': self.onSetOptionMode,
         'getOptionMode': self.onGetOptionMode,
         'getPlayVisible': self.onGetPlayVisible,
         'getCheckShow': self.onGetCheckShow,
         'setCheckShow': self.onSetCheckShow,
         'getRobZaijuInfo': self.onGetRobZaijuInfo,
         'showThirdLvMap': self.onShowThirdLvMap,
         'getThirdLvMapIcons': self.onGetThirdLvMapIcons,
         'scaleToSecLvMap': self.onScaleToSecLvMap,
         'scaleToThirdLvMap': self.onScaleToThirdLvMap,
         'getMapSize': self.onGetMapSize,
         'clickIcon': self.onClickIcon,
         'inWingWorldWarCity': self.onInWingWorldWarCity,
         'configUICallback': self.onConfigUICallback,
         'getEyeVisible': self.onGetEyeVisible,
         'getMapMaxLv': self.onGetMapMaxLv,
         'getThirdIconScale': self.onGetThirdIconScale,
         'setLevelCompleted': self.onSetLevelCompleted,
         'getBgMapChildMcRelayoutDataByLevel': self.onGetBgMapChildMcRelayoutDataByLevel,
         'getBgMapChildMcIdxData': self.onGetBgMapChildMcIdxData}
        self.mc = None
        self.curMapName = ''
        self.callbackHandler = None
        self.npcCallbackHandler = None
        self.isShow = False
        self.targetPos = None
        self.littleMapState = True
        self.mapSize = self.getMapSizeDict()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP, self.realClose)
        self.teamArr = {}
        self.npcInfo = None
        self.teleportId = None
        self.pathPoints = []
        self.seekPoint = []
        self.option = {0: {},
         1: {},
         2: {},
         10: {},
         11: {},
         12: {},
         20: {},
         21: {},
         22: {}}
        self.playFilter = {0: {},
         1: {},
         2: {},
         10: {},
         11: {},
         12: {},
         20: {},
         21: {},
         22: {}}
        self.getOptionByFilterData()
        self.getPlayByFilterData()
        self.getOptionSetting('option')
        self.getOptionSetting('playFilter')
        self.npcDataInfo = {}
        self.npcData = []
        self.spaceInfo = self.getSpaceSizeDic()
        self.markX = 0
        self.markY = 0
        self.curMark = 0
        self.markType = 1
        self.marks = {}
        self.isMarkState = False
        self.curMode = self.getOptionMode()
        self.checkShow = self.getCheckShow()
        self.thirdLvMapDict = self.getThirdLvMapDict()
        self.thirdLvMapSpaceNos = []
        self.mapInfo = MapInfo()
        self.mapWidget = None
        self.markType = -1
        self.currentCityId = 0
        self.debugPosX = None
        self.debugPosY = None
        self.isLogPos = False
        self.pubgPoisonRefreshHandleCB = None
        self.pubgAirPlanePath = None
        self.pubgAirlineHandleCB = None
        self.pubgAirPlaneStartInWidget = []
        self.pubgAirPlaneEndInWidget = []
        self.pubgAirlineRotation = None
        self.pubgAirlineWidth = None
        self.pubgBoundAreaDataInWidget = None
        self.ghostRefreshHandleCB = None

    def getOptionByFilterData(self):
        for key, val in MFC.data.items():
            self.option[0][key] = int(val.get('level1'))
            self.option[1][key] = int(val.get('level2'))
            self.option[2][key] = int(val.get('level3'))
            self.option[10][key] = key == 9
            self.option[11][key] = key == 9
            self.option[12][key] = key == 9
            self.option[20][key] = int(val.get('level1'))
            self.option[21][key] = int(val.get('level2'))
            self.option[22][key] = int(val.get('level3'))

    def getPlayByFilterData(self):
        for key, val in MPD.data.items():
            fType = int(val.get('type'))
            self.playFilter[0][fType] = 0
            self.playFilter[1][fType] = 0
            self.playFilter[2][fType] = 0
            self.playFilter[10][fType] = int(val.get('level1'))
            self.playFilter[11][fType] = int(val.get('level2'))
            self.playFilter[12][fType] = int(val.get('level3'))
            self.playFilter[20][fType] = int(val.get('level1'))
            self.playFilter[21][fType] = int(val.get('level2'))
            self.playFilter[22][fType] = int(val.get('level3'))

    def getOption(self, option, optionDword):
        return commcalc.getBitDword(optionDword, option)

    def setOption(self, option, checked, optionDword):
        return commcalc.calcBitDword(optionDword, option, checked)

    def getOptions(self, optionDword, filterKey):
        options = {}
        if filterKey == 'playFilter':
            for key, item in MPD.data.items():
                _type = int(item.get('type', 0))
                options[_type] = int(self.getOption(_type, optionDword))

        elif filterKey == 'option':
            for key in MFC.data.keys():
                options[key] = int(self.getOption(key, optionDword))

        return options

    def setOptions(self, options):
        ret = 0
        for key, val in options.items():
            ret = self.setOption(key, val, ret)

        return ret

    def getOptionSetting(self, key):
        for mode in xrange(3):
            for level in xrange(3):
                path = keys.SET_UI_MAP_OPTION + '/' + key + str(mode * 10 + level)
                newPath = keys.SET_UI_MAP_OPTION + '/' + key + str(mode * 10 + level)
                optionDword = 0
                oldOptionDword = AppSettings.get(path, -1)
                newOptionDword = AppSettings.get(newPath, -1)
                if newOptionDword != -1:
                    optionDword = newOptionDword
                elif oldOptionDword != -1 and key == 'option':
                    optionDword = oldOptionDword
                else:
                    continue
                getattr(self, key)[mode * 10 + level] = self.getOptions(optionDword, key)

    def getOptionMode(self):
        path = keys.SET_UI_MAP_OPTION + '/mode'
        mode = AppSettings.get(path, 0)
        return mode

    def setOptionMode(self, mode):
        path = keys.SET_UI_MAP_OPTION + '/mode'
        if int(AppSettings.get(path, 0)) != mode:
            AppSettings[path] = mode
            AppSettings.save()
        return mode

    def getCheckShow(self):
        path = keys.SET_UI_MAP_OPTION + '/checkShow'
        mode = AppSettings.get(path, 0)
        return mode

    def setCheckShow(self, mode):
        path = keys.SET_UI_MAP_OPTION + '/checkShow'
        if int(AppSettings.get(path, 0)) != mode:
            AppSettings[path] = mode
            AppSettings.save()
        return mode

    def onSetCheckShow(self, *args):
        checkShow = args[3][0].GetNumber()
        self.checkShow = checkShow
        self.setCheckShow(self.checkShow)
        self.refreshNpcPos()

    def onGetCheckShow(self, *args):
        return GfxValue(self.checkShow)

    def onSetOptionMode(self, *args):
        mode = int(args[3][0].GetNumber())
        self.curMode = mode
        self.setOptionMode(mode)
        self.setOptionSetting('option')
        self.setOptionSetting('playFilter')

    def onGetOptionMode(self, *args):
        return GfxValue(self.curMode)

    def setOptionSetting(self, key):
        needSave = False
        for mode in xrange(3):
            for level in xrange(3):
                path = keys.SET_UI_MAP_OPTION + '/' + key + str(mode * 10 + level)
                v = self.setOptions(getattr(self, key)[mode * 10 + level])
                if int(AppSettings.get(path, -1)) != v:
                    AppSettings[path] = v
                    needSave = True

        if needSave:
            AppSettings.save()

    def onGetNpcData(self, *arg):
        p = BigWorld.player()
        result = dict()
        if p.isInPUBG():
            pass
        else:
            result = MFC.data.items()
        return uiUtils.array2GfxAarry(result, True)

    def onGetPlayData(self, *arg):
        result = dict()
        p = BigWorld.player()
        if p.isInPUBG():
            pass
        else:
            result = MPD.data.items()
        return uiUtils.array2GfxAarry(result, True)

    def onGetGuideData(self, *arg):
        ret = []
        for item in MGD.data.values():
            ret.append(item['guideRun'])

        return uiUtils.array2GfxAarry(ret)

    def onGetBindCash(self, *arg):
        p = BigWorld.player()
        return GfxValue(getattr(p, 'cash', 0) + getattr(p, 'bindCash', 0))

    def onGetStoneCost(self, *arg):
        seekId = int(arg[3][0].GetString())
        destId = SD.data.get(seekId, {}).get('npcId')
        cost = BigWorld.player().getTeleportCost(destId)
        return GfxValue(cost)

    def onGetSearchNpcNames(self, *arg):
        text = unicode2gbk(arg[3][0].GetString())
        ret = []
        isPinyinAndHanzi = utils.isPinyinAndHanzi(text)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return uiUtils.array2GfxAarry(ret)
        text = text.lower()
        mapName = self.getCurrentMapName()
        searchTypes = ['digongport',
         'fubenport',
         'npc',
         'movablenpc',
         'transport',
         'transportstone']
        dt = self.npcDataInfo.get('debateNpcTks', {})
        it = self.npcDataInfo.get('comCltItems', {})
        nt = self.npcDataInfo.get('needMonsters', {})
        bt = self.npcDataInfo.get('beatMonsters', {})
        mt = self.npcDataInfo.get('markNpcs', {})
        complete = self.npcDataInfo.get('complete', {})
        unfinished = self.npcDataInfo.get('unfinished', {})
        available = self.npcDataInfo.get('available', {})
        for key, item in SD.data.items():
            spaceNo = item.get('spaceNo', 1)
            currSpaceNo = self.getCurrentSpaceNo()
            if currSpaceNo != spaceNo:
                if formula.spaceInGuild(currSpaceNo):
                    if formula.getMapId(currSpaceNo) != spaceNo:
                        continue
                else:
                    continue
            npcType = item.get('type', '').lower()
            if npcType not in searchTypes:
                continue
            visible = item.get('isInMap', 0)
            npcId = item.get('npcId')
            if not visible and key not in nt.keys() + bt.keys() + it.keys() + dt.keys() + mt.keys() and npcId not in complete and npcId not in available and npcId not in unfinished:
                continue
            name = ''
            if npcId and npcType in ('npc', 'movablenpc'):
                name = NCD.data.get(npcId, {}).get('name', '')
            else:
                name = item.get('name', '')
            if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
                name2 = pinyinConvert.strPinyinFirst(name)
                isFind = name2.find(text) != -1
            else:
                isFind = name.lower().find(text) != -1
            if isFind:
                x = item.get('xpos', 0)
                y = item.get('zpos', 0)
                newX, newY = self.transPos(x, y, mapName)
                if spaceNo == const.SPACE_NO_BIG_WORLD:
                    name = name + '[' + uiUtils.getChunkNameBySeekId(key) + ']'
                ret.append({'label': gbk2unicode(name),
                 'data': [newX, newY, key]})

        return uiUtils.array2GfxAarry(ret)

    def onRefreshNpcInfo(self, *arg):
        self.refreshNpcPos(self.npcInfo)

    def onCloseMap(self, *arg):
        self.openMap(False)

    def onGetOptionVisible(self, *arg):
        return uiUtils.dict2GfxDict(self.option[10 * self.curMode + self.mapInfo.mapLv])

    def onGetPlayVisible(self, *arg):
        return uiUtils.dict2GfxDict(self.playFilter[10 * self.curMode + self.mapInfo.mapLv])

    def onModOptionVisible(self, *arg):
        level = int(arg[3][0].GetNumber())
        key = int(arg[3][1].GetNumber())
        check = int(arg[3][2].GetNumber())
        optionKey = arg[3][3].GetString()
        option = getattr(self, optionKey)
        if option and option[10 * self.curMode + level].has_key(key):
            option[10 * self.curMode + level][key] = check

    def reset(self):
        if self.callbackHandler:
            BigWorld.cancelCallback(self.callbackHandler)

    def onRegisterMap(self, *arg):
        self.mapSize = self.getMapSizeDict()
        self.thirdLvMapDict = self.getThirdLvMapDict()
        self.mc = arg[3][0]
        self.mapWidget = asObject.ASObject(self.mc)
        self.mapInfo.mapLv = 1
        BigWorld.player().cell.fetchAreaStates()
        self.addMarks()
        self.updateMarks()
        initData = {'overColoumNum': SYSD.data.get('mapIconOverColoumNum', 5),
         'overWidth': SYSD.data.get('mapIconOverWidth', 20),
         'overHeight': SYSD.data.get('mapIconOverHeight', 20)}
        self.debugPosX = None
        self.debugPosY = None
        return uiUtils.dict2GfxDict(initData, True)

    def onConfigUICallback(self, *args):
        p = BigWorld.player()
        self.refreshFallenRedGuard()
        self.currentCityId = MTLD.data.get(self.mapInfo.mapId, {}).get('wingCityId', 0)
        nearbyWingCityIds = MTLD.data.get(self.mapInfo.mapId, {}).get('nearbyWingCityIds', ())
        isBornIsland = MTLD.data.get(self.mapInfo.mapId, {}).get('isBornIsland', 0)
        if p.inWingWarCity():
            for i in xrange(WING_WORLD_MARK_ICON_CNT):
                markMc = getattr(self.mapWidget.topMark, 'mark%d' % i)
                markMc.markType = i
                markMc.addEventListener(events.MOUSE_CLICK, self.handleMarkMcClick, False, 0, True)

            self.mapWidget.topMark.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearBtnClick, False, 0, True)
            if self.currentCityId:
                gamelog.info('jbx:querWingWorldWarCityWorldMap', self.currentCityId)
                p.cell.querWingWorldWarCityWorldMap(self.currentCityId)
            self.refreshWingWorldIcons()
            self.addWingWorldGatherIcon()
            self.refreshWingWorldMarks()
            self.mapWidget.topSearchArea.visible = not bool(self.currentCityId)
            if self.currentCityId and self.currentCityId == p.getWingWarCityId():
                if p.isWingWorldCampMode():
                    self.mapWidget.topMark.visible = False
                else:
                    self.mapWidget.topMark.visible = wingWorldUtils.isArmyLeader(p.wingWorldPostId)
            else:
                self.mapWidget.topMark.visible = False
        elif p.inWingPeaceCity():
            self.refreshWingWorldGuildFlag()
            self.addWingWorldWarFlagIcon()
            self.addWingWorldGatherIcon()
            if self.currentCityId and not isBornIsland:
                gamelog.info('@yj:querWingWorldWarCityWorldMap:inWingPeaceCity', self.currentCityId, nearbyWingCityIds)
                if nearbyWingCityIds and len(nearbyWingCityIds) == 2:
                    p.cell.queryWingWorldFullCityDTO(nearbyWingCityIds[0], nearbyWingCityIds[1])
                else:
                    p.cell.queryWingWorldFullCityDTO(self.currentCityId, 0)
                p.base.getSoulBossStateInfoEx(self.currentCityId)
            elif isBornIsland:
                p.cell.queryWingWorldResource(False)
            else:
                self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_ADD_RESOURCE_POINT, [])
                self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_OTHER_WING_BOSS_FLAG, [])
            self.mapWidget.topSearchArea.visible = True
            self.mapWidget.topMark.visible = False
        elif p.inWingBornIsland():
            self.refreshWingWorldGuildFlag()
            self.addWingWorldWarFlagIcon()
            self.addWingWorldGatherIcon()
            self.mapWidget.topMark.visible = False
            if not self.mapInfo.isThirdLvMap():
                self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_ADD_RESOURCE_POINT, [])
                self.currentCityId = 0
            elif self.currentCityId:
                gamelog.info('@yj:querWingWorldWarCityWorldMap:inWingBornIsland', self.currentCityId, nearbyWingCityIds)
                if nearbyWingCityIds and len(nearbyWingCityIds) == 2:
                    p.cell.queryWingWorldFullCityDTO(nearbyWingCityIds[0], nearbyWingCityIds[1])
                else:
                    p.cell.queryWingWorldFullCityDTO(self.currentCityId, 0)
            elif isBornIsland:
                p.cell.queryWingWorldResource(False)
        else:
            self.mapWidget.topMark.visible = False
            self.currentCityId = 0
            self.addOtherIns(uiConst.MAP_ICON_OTHER_WING_WAR_FLAG, [])
        self.addClanWarYaBiao()
        self.addWorldBossIcons()
        self.refreshAllPUBGUI()
        self.refreshDoublePlantTreeUI()
        self.refreshHuntGhostUI()

    def onGetEyeVisible(self, *args):
        visible = True
        p = BigWorld.player()
        if p.inWingCityOrBornIsland():
            if MTLD.data.has_key(self.mapInfo.mapId):
                wingCityId = p.getWingCityId()
                if wingCityId and self.currentCityId != wingCityId:
                    visible = False
                elif p.inWingBornIsland() and self.currentCityId:
                    visible = False
        return GfxValue(visible)

    def handleClearBtnClick(self, *args):
        gamelog.info('jbx:clearAllWingWorldMinMapPoint')
        BigWorld.player().cell.clearAllWingWorldMinMapPoint(self.currentCityId)

    def handleMarkMcClick(self, *args):
        e = asObject.ASObject(args[3][0])
        self.markType = int(e.currentTarget.markType)
        self.uiAdapter.clearState()
        dstState = MARK_TYPE_TO_CURSOR_STATE[self.markType]
        dstCursorName = MARK_TYPE_TO_CURSOR_NAME[self.markType]
        if ui.get_cursor_state() != dstState:
            ui.reset_cursor()
            ui.set_cursor_state(dstState)
            ui.set_cursor(dstCursorName)
            ui.lock_cursor()
            self.mapWidget.bgmap.addEventListener(events.MOUSE_CLICK, self.handleSendMarkClick, False, 1, True)

    def handleSendMarkClick(self, *args):
        gamelog.info('jbx:handleSendMarkClick')
        e = asObject.ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.delWingWorldMarkState()
            e.stopImmediatePropagation()
        elif e.buttonIdx == uiConst.LEFT_BUTTON:
            posX = self.mapWidget.bgmap.mouseX
            posY = self.mapWidget.bgmap.mouseY
            posX, posY = self.rTransPos(posX, posY, self.getCurrentMapName(), self.mapInfo.mapLv)
            gamelog.info('jbx:markWingWorldMinMapPoint', self.currentCityId, int(posX), int(posY), self.markType)
            BigWorld.player().cell.markWingWorldMinMapPoint(self.currentCityId, int(posX), int(posY), self.markType)
            self.delWingWorldMarkState()

    def delWingWorldMarkState(self):
        if not self.mapWidget:
            return
        if self.markType >= 0:
            dstState = MARK_TYPE_TO_CURSOR_STATE[self.markType]
            if ui.get_cursor_state() == dstState:
                ui.reset_cursor()
            self.markType = -1
        if self.mapWidget and self.mapWidget.bgmap:
            self.mapWidget.bgmap.removeEventListener(events.MOUSE_CLICK, self.handleSendMarkClick)

    def updateTarget(self, *args):
        if self.targetPos == None:
            return
        else:
            newX, newY = self.transPos(int(self.targetPos[0]), int(self.targetPos[2]), self.targetPos[3])
            self.mc.Invoke('setTargetPos', (GfxValue(int(newX)), GfxValue(int(newY)), GfxValue(gbk2unicode(self.targetPos[3]))))
            return

    def setAreaState(self, info):
        ret = []
        p = BigWorld.player()
        if p.isInPUBG():
            return
        for item in info.values():
            chunkName = BigWorld.ChunkInfoAt(BigWorld.player().position)
            data = WASD.data.get(item)
            if data and chunkName in data.get('chunkList', ()):
                name = data['tipsM']
                newPos = self.transPos(data['xposM'], data['zposM'], self.getCurrentMapName())
                ret.append([name, newPos])

        if self.mc:
            self.mc.Invoke('setAreaState', uiUtils.array2GfxAarry(ret, True))

    def setWorldQuest(self):
        if not self.mc:
            return
        arg = []
        p = BigWorld.player()
        if p.isInPUBG():
            return
        for quest in p.worldQuests:
            data = WQD.data.get(quest)
            if data:
                tkType = data.get('tkType', 1)
                rad = data.get('tkRadii', 0)
                name = data.get('name', '')
                seekId = data.get('tkId', '')
                if CMD.data.get(BigWorld.ChunkInfoAt(p.position), {}).get('worldAreaId', 0) == data.get('areaId', 0):
                    x = SD.data.get(seekId, {}).get('xpos', 0)
                    y = SD.data.get(seekId, {}).get('zpos', 0)
                    newX, newY = self.transPos(x, y, self.getCurrentMapName())
                    arg.append({'type': tkType,
                     'rad': rad,
                     'name': name,
                     'posX': newX,
                     'posY': newY})

        if self.mc:
            self.mc.Invoke('setWorldQuest', uiUtils.array2GfxAarry(arg, True))

    def onGetWorldQuest(self, *arg):
        self.setWorldQuest()

    def onGetAreaInfo(self, *arg):
        level = int(arg[3][0].GetNumber())
        mapId = int(arg[3][1].GetNumber())
        ret = self.movie.CreateArray()
        ret1 = self.movie.CreateArray()
        if level == 2:
            mapName = MII.data[mapId].get('mapName_ii')
            ret.SetElement(0, GfxValue(gbk2unicode(mapName)))
            mapPos = MII.data[mapId].get('mapPos')
            ret1.SetElement(0, GfxValue(mapPos[0]))
            ret1.SetElement(1, GfxValue(mapPos[2]))
            ret.SetElement(1, ret1)
            ret.SetElement(2, GfxValue(self.getMapNameByNo(mapId)))
            ret.SetElement(3, GfxValue(mapId))
        elif level == 3:
            mapName = MIII.data[mapId].get('mapName_iii')
            ret.SetElement(0, GfxValue(gbk2unicode(mapName)))
            mapPos = MIII.data[mapId].get('areaPos')
            ret1.SetElement(0, GfxValue(mapPos[0]))
            ret1.SetElement(1, GfxValue(mapPos[2]))
            ret.SetElement(1, ret1)
            ret.SetElement(2, GfxValue(mapId))
        return ret

    def onGetPlayerPos(self, *arg):
        self.curMapName = arg[3][0].GetString()

    def getPlayerPos(self):
        p = BigWorld.player()
        x, y = p.position[0], p.position[2]
        if not self.mapInfo.isThirdLvMap():
            if p.inWingCity():
                cityId = formula.getWingCityId(p.spaceNo, BigWorld.ChunkInfoAt(p.position))
                x, y = WWCTD.data.get(cityId, {}).get('mapPos', (p.position[0], p.position[2]))
            elif p.inWingBornIsland():
                x, y = WWCFGD.data.get('bornIslandPos', (p.position[0], p.position[2]))
        return (x, p.position[1], y)

    def setPlayerPos(self, x, y, yaw):
        if not self.mc:
            return
        p = BigWorld.player()
        if not self.mapInfo.isThirdLvMap():
            if p.inWingCity():
                chunkName = BigWorld.ChunkInfoAt(p.position)
                cityId = formula.getWingCityId(p.spaceNo, chunkName)
                x, y = WWCTD.data.get(cityId, {}).get('mapPos', (p.position[0], p.position[2]))
            elif p.inWingBornIsland():
                x, y = RSCD.data.get(p.getOriginHostId(), {}).get('bornIslandPos', (p.position[0], p.position[2]))
        spaceNo = self.getSpaceNo()
        mapName = self.getMapNameByNo(spaceNo, BigWorld.player().position)
        currentMapName = self.getCurrentMapName()
        if currentMapName == mapName or self.mapInfo.containsMap(mapName) or BigWorld.player().inWingCityOrBornIsland():
            newX, newY = self.transPos(x, y, currentMapName, showLog=True)
            mapIIName = self.mapInfo.getMapShowName()
            self.mc.Invoke('setPlayerPos', (GfxValue(newX),
             GfxValue(newY),
             GfxValue(yaw * 180 / 3.14),
             GfxValue(gbk2unicode(mapIIName))))
            self.setPlayerIcon()

    def setPlayerIcon(self):
        p = BigWorld.player()
        if not self.mapWidget:
            return
        if hasattr(p, 'isInPUBG') and p.isInPUBG():
            self.setPlayerIconInPUBG()
        else:
            self.mapWidget.eye.gotoAndStop('normal')

    def getSpaceInfo(self, mapName):
        if self.mapInfo.isThirdLvMap():
            spaceInfo = MTLD.data.get(self.mapInfo.mapId, {})
        else:
            spaceInfo = self.spaceInfo[mapName]
        return spaceInfo

    def transPos(self, x, y, mapName, mapLv = -1, showLog = False):
        if not self.spaceInfo.has_key(mapName):
            return (x, y)
        else:
            mapLv = mapLv if mapLv >= MAP_LV_0 else self.mapInfo.mapLv
            spaceInfo = self.getSpaceInfo(mapName)
            mapWidth = spaceInfo['mapWidth']
            spaceAllWidth = spaceInfo['spaceAllWidth']
            posInBg = spaceInfo['posInBg']
            spaceX = spaceInfo['spaceX']
            spaceY = spaceInfo['spaceY']
            spaceAllHeight = spaceInfo['spaceAllHeight']
            mapHeight = spaceInfo['mapHeight']
            spaceWidth = spaceInfo['spaceWidth']
            spaceHeight = spaceInfo['spaceHeight']
            zeroPosX = spaceInfo['zeroPosX']
            zeroPosZ = spaceInfo['zeroPosZ']
            stdWidth = spaceInfo['stdWidth']
            stdHeight = spaceInfo['stdHeight']
            newX = (x * (mapWidth * 1.0 / spaceAllWidth) + zeroPosX - spaceX) * ((posInBg[2] - posInBg[0]) * 1.0 / spaceWidth) + posInBg[0]
            newY = (zeroPosZ - y * (mapHeight * 1.0 / spaceAllHeight) - spaceY) * ((posInBg[3] - posInBg[1]) * 1.0 / spaceHeight) + posInBg[1]
            if showLog:
                if self.debugPosX != None:
                    newX = self.debugPosX
                    gamelog.info('jbx:map formula X %f = (%f*(%f/spaceAllWidth)+zeroPosX - %f)*%f+%f' % (newX,
                     x,
                     mapWidth,
                     spaceX,
                     (posInBg[2] - posInBg[0]) * 1.0 / spaceWidth,
                     posInBg[0]))
                if self.debugPosY != None:
                    newY = self.debugPosY
                    gamelog.info('jbx:map formula Y %f = (zeroPosZ - %f*(%f/spaceAllHeight) - %f)*%f + %f' % (newY,
                     y,
                     mapHeight,
                     spaceY,
                     (posInBg[3] - posInBg[1]) * 1.0 / spaceHeight,
                     posInBg[1]))
            if self.isLogPos:
                gamelog.info('jbx:mapPos', newX, newY)
            newX = newX * (self.mapSize[mapName][mapLv][0] * 1.0 / stdWidth)
            newY = newY * (self.mapSize[mapName][mapLv][1] * 1.0 / stdHeight)
            return (newX, newY)

    def rTransPos(self, x, y, mapName, mapLv = -1):
        if mapName == 'world':
            return
        spaceInfo = self.getSpaceInfo(mapName)
        mapWidth = spaceInfo['mapWidth']
        spaceAllWidth = spaceInfo['spaceAllWidth']
        posInBg = spaceInfo['posInBg']
        spaceX = spaceInfo['spaceX']
        spaceY = spaceInfo['spaceY']
        spaceAllHeight = spaceInfo['spaceAllHeight']
        mapHeight = spaceInfo['mapHeight']
        spaceWidth = spaceInfo['spaceWidth']
        spaceHeight = spaceInfo['spaceHeight']
        zeroPosX = spaceInfo['zeroPosX']
        zeroPosZ = spaceInfo['zeroPosZ']
        stdWidth = spaceInfo['stdWidth']
        stdHeight = spaceInfo['stdHeight']
        x = x * (stdWidth * 1.0 / self.mapSize[mapName][mapLv][0])
        y = y * (stdHeight * 1.0 / self.mapSize[mapName][mapLv][1])
        newX = ((x - posInBg[0]) / ((posInBg[2] - posInBg[0]) * 1.0 / spaceWidth) + spaceX - zeroPosX) / (mapWidth * 1.0 / spaceAllWidth)
        newY = (zeroPosZ - spaceY - (y - posInBg[1]) / ((posInBg[3] - posInBg[1]) * 1.0 / spaceHeight)) / (mapHeight * 1.0 / spaceAllHeight)
        return (newX, newY)

    def onSetLevel(self, *arg):
        level = int(arg[3][0].GetNumber())
        self.mapInfo.mapLv = level
        BigWorld.callback(0.3, self.refreshFallenRedGuard)

    def onTransPos(self, *arg):
        x = arg[3][0].GetNumber()
        y = arg[3][1].GetNumber()
        mapName = arg[3][2].GetString()
        transX, transY = self.transPos(x, y, mapName)
        ret = [transX, transY]
        return uiUtils.array2GfxAarry(ret)

    def onRTransPos(self, *arg):
        x = arg[3][0].GetNumber()
        y = arg[3][1].GetNumber()
        mapName = arg[3][2].GetString()
        transX, transY = self.rTransPos(x, y, mapName, self.mapInfo.mapLv)
        ret = [transX, transY]
        return uiUtils.array2GfxAarry(ret)

    def getSpaceSizeDic(self):
        dic = {}
        for key in MII.data.keys():
            mapName = self.getMapNameByNo(key)
            dic[mapName] = MII.data[key]

        for key, value in MTLD.data.iteritems():
            dic[value.get('mapPath')] = value

        return dic

    def getThirdLvMapDict(self):
        tmp = {}
        self.thirdLvMapSpaceNos = {}
        for key, value in MTLD.data.iteritems():
            chunkNames = value.get('chuckNames', [])
            spaceNo = value.get('spaceNo', 0)
            for chName in chunkNames:
                tmp[spaceNo, chName] = key

            self.thirdLvMapSpaceNos[value.get('spaceNo', 0)] = value.get('mapPath', '')

        return tmp

    def isThirdLvMap(self, spaceNo, chName):
        mapId = formula.getMapId(spaceNo)
        return self.thirdLvMapDict.has_key((mapId, chName))

    def openMap(self, show, type = 'normal', targetPos = None):
        p = BigWorld.player()
        if show:
            if p.inWingPeaceCityOrBornIsland():
                p.cell.statsTriggerFromClient('loadWidgetTrigger', (uiConst.FAKE_WIDGET_ID_WING_WORLD_MAP,))
            self.mapInfo.mapType = type
            if not gameglobal.rds.ui.enableUI:
                p.showUI(True)
            gameglobal.rds.ui.chat.hideView()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MAP)
            self.isShow = True
            self.targetPos = targetPos
            if ui.get_cursor_state() != ui.NORMAL_STATE:
                ui.reset_cursor()
            p.cell.getJobsCount()
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAP)
            self.targetPos = None
            if cameraEffect.mapCallback:
                BigWorld.cancelCallback(cameraEffect.mapCallback)
                cameraEffect.mapCallback = None
            gameglobal.rds.ui.chat.showView()
            BigWorld.camera(gameglobal.rds.cam.cc)
            BigWorld.worldDrawEnabled(True)
            if hasattr(BigWorld, 'bigMapEnabled'):
                BigWorld.bigMapEnabled(False)
            self.clearMarkState()
            self.delWingWorldMarkState()
            if self.mc:
                self.setOptionSetting('option')
                self.setOptionSetting('playFilter')
            self.mc = self.mapWidget = None
            self.isShow = False
            if hasattr(BigWorld, 'forceUpdateZoneParams'):
                BigWorld.forceUpdateZoneParams()
            self.mapInfo.clear()
            self.currentCityId = 0
            self.releasePUBGData()

    def showMap(self, isDown):
        BigWorld.player().showMap(isDown)

    def onPreLoadPic(self, *arg):
        name = arg[3][0].GetString()
        GUI.Simple('gui/' + name)

    def loadPic(self):
        if self.mc:
            self.mc.Invoke('init')

    def enableWorldDraw(self, needWorldDraw = True):
        if needWorldDraw:
            BigWorld.worldDrawEnabled(True)
        if hasattr(BigWorld, 'bigMapEnabled'):
            BigWorld.bigMapEnabled(False)

    def realClose(self, needWorldDraw = True):
        self.mc = self.mapWidget = None
        if cameraEffect.mapCallback:
            BigWorld.cancelCallback(cameraEffect.mapCallback)
            cameraEffect.mapCallback = None
        if gameglobal.MAP_PLAYING:
            gameglobal.MAP_PLAYING = False
        BigWorld.callback(1.5, Functor(self.enableWorldDraw, needWorldDraw))
        p = BigWorld.player()
        if p and utils.instanceof(p, 'PlayerAvatar') and self.isShow:
            p.unlockKey(gameglobal.KEY_POS_EFFECT)
            p.updateActionKeyState()
            p.excludeCam = False
        BigWorld.camera(gameglobal.rds.cam.cc)
        self.enableWorldDraw(needWorldDraw)
        self.clearMarkState()
        self.delWingWorldMarkState()
        gameglobal.rds.ui.chat.showView()
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAP)
            self.setOptionSetting('option')
            self.setOptionSetting('playFilter')
        self.isShow = False
        if hasattr(BigWorld, 'forceUpdateZoneParams'):
            BigWorld.forceUpdateZoneParams()
        self.mapInfo.clear()
        self.releasePUBGData()

    def close(self):
        self.realClose()

    def setPlayerVisible(self, bVisible):
        self.mc.Invoke('setPlayerVisible', GfxValue(bVisible))

    def getLoopNpc(self, loopId, isNext):
        firstQuestId = None
        info = BigWorld.player().questLoopInfo.get(loopId, None)
        quest = None
        if info:
            if isNext:
                quests = info.getNextQuests(BigWorld.player())
                if len(quests) > 0:
                    quest = quests[0]
                else:
                    quest = None
            else:
                quest = info.getCurrentQuest()
        if info is None or len(info.questInfo) == 0 or quest == None:
            qld = QLD.data.get(loopId)
            if len(qld['quests']) > 0:
                firstQuestId = qld['quests'][0]
                if isinstance(firstQuestId, tuple):
                    firstQuestId = firstQuestId[0]
        else:
            firstQuestId = quest
        return firstQuestId

    def getMapRange(self):
        if self.mapInfo.isThirdLvMap() and self.mapInfo.getCurrentMapSpaceNo() == const.SPACE_NO_BIG_WORLD:
            thirdMapName = self.mapInfo.getMapName()
            thirdMapSize = self.mapSize.get(thirdMapName)[self.mapInfo.mapLv]
            leftTop = self.rTransPos(0, 0, thirdMapName)
            rightBottom = self.rTransPos(thirdMapSize[0], thirdMapSize[1], thirdMapName)
            leftTop = self.transPos(leftTop[0], leftTop[1], WORLD_MAP_NAME, MAP_LV_2)
            rightBottom = self.transPos(rightBottom[0], rightBottom[1], WORLD_MAP_NAME, MAP_LV_2)
            w, h = PIC_UNIT_SIZE
            return [int(leftTop[0] / w),
             int(rightBottom[0] / w) + 1,
             int(leftTop[1] / h),
             int(rightBottom[1] / h) + 1]
        ret = self.mc.Invoke('getMapRange')
        xMin = int(ret.GetElement(0).GetNumber()) * 2 ** (2 - self.mapInfo.mapLv)
        xMax = int(ret.GetElement(1).GetNumber()) * 2 ** (2 - self.mapInfo.mapLv)
        yMin = int(ret.GetElement(2).GetNumber()) * 2 ** (2 - self.mapInfo.mapLv)
        yMax = int(ret.GetElement(3).GetNumber()) * 2 ** (2 - self.mapInfo.mapLv)
        return [xMin,
         xMax,
         yMin,
         yMax]

    def getAreaNpc(self):
        spaceNo = self.mapInfo.getCurrentMapSpaceNo()
        mapRange = self.getMapRange()
        ret = []
        if spaceNo == const.SPACE_NO_BIG_WORLD:
            for i in range(mapRange[0], mapRange[1] + 1):
                for j in range(mapRange[2], mapRange[3] + 1):
                    npcList = CRD.data.get((spaceNo, i, j), None)
                    if npcList:
                        ret.extend(npcList)

        else:
            for key, item in CRD.data.items():
                if key[0] == spaceNo:
                    ret.extend(item)

        return ret

    def getTrackIndex(self, questId):
        return gameglobal.rds.ui.questTrack.getTrackedIds(questId)

    def refreshYaBiaoIcon(self, pos):
        if self.mc:
            newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
            self.mc.Invoke('addYaBiaoIcon', uiUtils.array2GfxAarry(newPos))

    def refreshFallenRedGuard(self):
        if not self.mc:
            return
        p = BigWorld.player()
        flagList = getattr(BigWorld.player(), 'fallenRedGuardFlagList', [])
        if not clientUtils.checkFallendRedGuardTime():
            flagList = []
        ret = {}
        posArray = []
        areaArray = []
        for flagId, isDead in flagList:
            insName = 'Map_FallenRedGaurd' if not isDead else 'Map_FallenRedGaurdDead'
            tips = gameStrings.FALLEN_RED_GUARD_ALIVE if not isDead else gameStrings.FALLEN_RED_GUARD_KILLED
            posX = FRGD.data.get(flagId, {}).get('xpos', 0)
            posZ = FRGD.data.get(flagId, {}).get('zpos', 0)
            newPos = self.transPos(posX, posZ, self.getCurrentMapName())
            posArray.append((insName, newPos, tips))
            leftX = FRGD.data.get(flagId, {}).get('leftxpos', 0)
            leftY = FRGD.data.get(flagId, {}).get('leftypos', 0)
            mapLeftX, mapLeftY = self.transPos(leftX, leftY, self.getCurrentMapName())
            rightX = FRGD.data.get(flagId, {}).get('rightxpos', 0)
            rightY = FRGD.data.get(flagId, {}).get('rightypos', 0)
            mapRightX, mapRightY = self.transPos(rightX, rightY, self.getCurrentMapName())
            isSpecial = False
            if utils.getWeekInt() == const.WEEK_INT_FRI and FRGD.data.get(flagId, {}).get('order', 0) == 1:
                isSpecial = True
            areaArray.append((min(mapLeftX, mapRightX),
             min(mapLeftY, mapRightY),
             abs(mapRightX - mapLeftX),
             abs(mapRightY - mapLeftY),
             isSpecial))

        gamelog.info('jbx:refreshFallenRedGuard', len(posArray))
        ret['pos'] = posArray
        ret['area'] = areaArray
        self.mc.Invoke('addFallenRedGuardIcon', uiUtils.dict2GfxDict(ret, True))

    def getNpcData(self, info = None, mapName = None):
        data = []
        self.npcDataInfo = gameglobal.rds.ui.littleMap.getQuestNpcInfo(None, True)
        dt = self.npcDataInfo.get('debateNpcTks', {})
        it = self.npcDataInfo.get('comCltItems', {})
        nt = self.npcDataInfo.get('needMonsters', {})
        bt = self.npcDataInfo.get('beatMonsters', {})
        mt = self.npcDataInfo.get('markNpcs', {})
        cltItemTypes = self.npcDataInfo.get('cltItemTypes', {})
        complete = self.npcDataInfo.get('complete', {})
        unfinished = self.npcDataInfo.get('unfinished', {})
        available = self.npcDataInfo.get('available', {})
        npcList = self.getAreaNpc()
        seekIds = [ npcData.get('npcList', 0) for npcData in npcList ]
        notifyList = BigWorld.player().clientPersistentNotifyList.get(gametypes.CLIENT_PERSISTENT_NOTIFY_MAP, [])
        allList = seekIds + notifyList
        p = BigWorld.player()
        for seekId in allList:
            trackIndex = 0
            radii = 0
            item = SD.data.get(seekId)
            if not item:
                continue
            if not self.uiAdapter.littleMap.checkSeekData(item):
                continue
            if item.get('xpos') == None:
                continue
            visible = item.get('isInMap', 0) or seekId in notifyList
            npcId = item.get('npcId')
            if not visible and seekId not in nt.keys() + bt.keys() + it.keys() + dt.keys() + mt.keys() and npcId not in complete and npcId not in available and npcId not in unfinished:
                continue
            x, z = item['xpos'], item['zpos']
            iType = item.get('type', '')
            spaceNo = item.get('spaceNo', 1)
            npcId = item.get('npcId')
            if iType.lower() == 'npc':
                name, title = uiUtils.getNpcNameAndTitle(npcId)
            else:
                name = item.get('name', '')
                title = item.get('title', '')
            if self.mapInfo.isThirdLvMap():
                pos = Math.Vector3(item.get('xpos'), item.get('ypos'), item.get('zpos'))
            else:
                pos = None
            if self.getMapNameByNo(spaceNo, pos) != mapName and not formula.spaceInWingBornIslandOrPeaceCity(p.spaceNo):
                continue
            if seekId in nt.keys():
                trackIndex = self.getTrackIndex(nt[seekId][2])
                radii = QD.data.get(nt[seekId][2], {}).get('needMonsterRadii', 0)
                data.append([monsterResArr[nt[seekId][1] - 1],
                 x,
                 z,
                 name,
                 title,
                 nt[seekId][0],
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif seekId in bt.keys():
                radii = QD.data.get(bt[seekId][2], {}).get('beatMonsterRadii', 0)
                trackIndex = self.getTrackIndex(bt[seekId][2])
                data.append([monsterResArr[bt[seekId][1] - 1],
                 x,
                 z,
                 name,
                 title,
                 bt[seekId][0],
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif seekId in it.keys():
                iconRes = cltItemResArr
                if cltItemTypes.has_key(seekId):
                    iconRes = colItemTypeRes.get(cltItemTypes[seekId], iconRes)
                trackIndex = self.getTrackIndex(it[seekId][2])
                radii = QD.data.get(it[seekId][2], {}).get('CltItemRadii', 0)
                data.append([iconRes[it[seekId][1] - 1],
                 x,
                 z,
                 name,
                 title,
                 it[seekId],
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif seekId in dt.keys():
                trackIndex = self.getTrackIndex(dt[seekId][2])
                data.append([chatResArr[dt[seekId][1] - 1],
                 x,
                 z,
                 name,
                 title,
                 dt[seekId][0],
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif seekId in mt.keys():
                trackIndex = self.getTrackIndex(mt[seekId][2])
                data.append([markNpcArr[mt[seekId][1] - 1],
                 x,
                 z,
                 name,
                 title,
                 mt[seekId][0],
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            if npcId != None and iType != 'transportStone' and iType != 'recommActivity':
                ndata = NCD.data.get(npcId)
                if ndata == None:
                    continue
                if ndata.get('isInRobOldSpace', 0):
                    if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                        continue
                npcType = ''
                resArr = None
                qType = None
                questId = 0
                if npcId in complete:
                    qType, questId = self.getIconByQuestTypes(complete.get(npcId))
                    if not commQuest.isShowExcludeAvailableMarkQuest(questId):
                        continue
                    resArr = completeResArr
                elif npcId in available:
                    qType, questId = self.getIconByQuestTypes(available.get(npcId))
                    if not commQuest.isShowAvailableQuest(questId):
                        continue
                    resArr = availableResArr
                elif npcId in unfinished:
                    qType, questId = self.getIconByQuestTypes(unfinished.get(npcId))
                    if not commQuest.isShowExcludeAvailableMarkQuest(questId):
                        continue
                    if QD.data.get(questId, {}).get('hideUnfinishIcon', 0):
                        continue
                    resArr = unfinishedResArr
                if qType and resArr and int(qType) >= 1 and int(qType) <= len(resArr):
                    npcType = resArr[int(qType) - 1]
                if npcType and npcType != '':
                    trackIndex = self.getTrackIndex(questId)
                    data.append([npcType,
                     x,
                     z,
                     name,
                     title,
                     '',
                     x,
                     z,
                     seekId,
                     trackIndex,
                     radii])
                elif visible:
                    icon = ndata.get('topIcon', 'common')
                    if uiUtils.checkTopIconValid(icon):
                        data.insert(0, ['map' + icon,
                         x,
                         z,
                         name,
                         title,
                         '',
                         x,
                         z,
                         seekId,
                         trackIndex,
                         radii])
            enableWorldPlayActivity = gameglobal.rds.configData.get('enableWorldPlayActivity', False)
            if iType == 'transport' and visible:
                data.append(['mapcommon',
                 x,
                 z,
                 name,
                 title,
                 '',
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif iType == 'DiGongPort' and visible:
                data.append(['mapDiGongPort',
                 x,
                 z,
                 name,
                 title,
                 '',
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif iType == 'FubenPort' and visible:
                data.append(['mapFubenPort',
                 x,
                 z,
                 name,
                 title,
                 '',
                 x,
                 z,
                 seekId,
                 trackIndex,
                 radii])
                continue
            elif iType == 'transportStone' and visible:
                if self.isActiveTransStone(npcId):
                    data.append(['maptransStoneAct',
                     x,
                     z,
                     name,
                     title,
                     '',
                     x,
                     z,
                     seekId,
                     trackIndex,
                     radii])
                    continue
                else:
                    data.append(['maptransStoneDis',
                     x,
                     z,
                     name,
                     title,
                     '',
                     x,
                     z,
                     seekId,
                     trackIndex,
                     radii])
                    continue
            elif iType == 'recommActivity' and enableWorldPlayActivity and visible:
                activityId = item.get('npcId', 0)
                activityData = PRAD.data.get(activityId, {})
                if activityId:
                    if self.checkShow and not self.playCheckShow(activityId):
                        continue
                    if self.isInvalidWeek(activityId):
                        continue
                    mapIcon = activityData.get('mapIcon', '')
                    if mapIcon:
                        name = activityData.get('name', '')
                        iconPath = ICON_PATH + 'recommActivity/%s.dds' % mapIcon
                        commonData = [iconPath,
                         x,
                         z,
                         name,
                         title,
                         '',
                         x,
                         z,
                         seekId,
                         trackIndex,
                         radii]
                        extraData = self.getRecommExtraData(activityId)
                        if extraData:
                            commonData.append(extraData)
                        data.append(commonData)

        return data

    def checkTopIconValid(self, type):
        topIconList = ['WorkBoard']
        if type in topIconList:
            return False
        return True

    def getRecommExtraData(self, activityId):
        data = None
        activityData = PRAD.data.get(activityId, {})
        if activityId:
            activityType = activityData.get('type', 1)
            mapIcon = activityData.get('mapIcon', '')
            if activityType == uiConst.Map_PlayRecomm_ACTIVE and mapIcon:
                data = (activityType, self.getActiveLockFlag(activityId), self.inMonsterRefreshTime(activityId))
            elif activityType == uiConst.Map_PlayRecomm_JOB and mapIcon:
                data = (activityType, self.getJobState(activityId))
            elif activityType == uiConst.Map_PlayRecomm_MONSTER and mapIcon:
                data = (activityType, self.getMonsterRefreshTime(activityId))
            else:
                data = (activityType,)
        return data

    def getMonsterRefreshTime(self, activityId):
        showTime = SYSD.data.get('MAP_MONSTER_SHOW', 1800)
        endTime = SYSD.data.get('MAP_MONSTER_HIDE', 600)
        aData = PRAD.data.get(activityId, {})
        startTime = aData.get('refreshTimes', ())[0]
        leftTime = utils.getNextCrontabTime(startTime, utils.getNow()) - utils.getNow()
        if leftTime > showTime or abs(leftTime) < endTime:
            leftTime = 0
        return leftTime

    def getActiveLockFlag(self, activityId):
        ret = False
        aData = PRAD.data.get(activityId, {})
        weekSet = aData.get('weekSet', 0)
        startTimes = aData.get('startTimes', ())
        endTimes = aData.get('endTimes', ())
        if startTimes and endTimes:
            ret = not utils.inDateRange(startTimes[0], endTimes[0], weekSet=weekSet)
        else:
            ret = False
        return ret

    def isInvalidWeek(self, activityId):
        aData = PRAD.data.get(activityId, {})
        weekSet = aData.get('weekSet', 0)
        return utils.isInvalidWeek(weekSet)

    def inMonsterRefreshTime(self, activityId):
        aData = PRAD.data.get(activityId, {})
        weekSet = aData.get('weekSet', 0)
        refreshTime = aData.get('monsterRefreshTime', [])
        for rTime in refreshTime:
            if utils.inCrontabRange(rTime[0], rTime[1], weekSet=weekSet):
                return True

        return False

    def playCheckShow(self, activityId):
        time = False
        lv = False
        p = BigWorld.player()
        aData = PRAD.data.get(activityId, {})
        weekSet = aData.get('weekSet', 0)
        startTimes = aData.get('startTimes', ())
        endTimes = aData.get('endTimes', ())
        maxLv = aData.get('maxLv')
        minLv = aData.get('minLv')
        if maxLv and minLv:
            if minLv <= p.lv <= maxLv:
                lv = True
            else:
                lv = False
        else:
            lv = True
        if startTimes and endTimes:
            time = utils.inDateRange(startTimes[0], endTimes[0], weekSet=weekSet)
        else:
            time = True
        return lv and time

    def getJobState(self, activityId):
        p = BigWorld.player()
        aData = PRAD.data.get(activityId, {})
        jobId = aData.get('jobId', 0)
        if hasattr(p, 'jobsCount'):
            state = p.jobsCount.get(jobId, 0)
        else:
            state = 0
        return bool(state)

    def getIconByQuestTypes(self, qTypes):
        for qType in gametypes.ALL_QUEST_DISPLAY_TYPE:
            for sType in qTypes:
                if qType == sType[0]:
                    return (qType, sType[1])

        return (0, 0)

    def isActiveTransStone(self, seekId):
        transportId = TRD.data.get(seekId, {}).get('destId', 0)
        p = BigWorld.player()
        if transportId:
            if formula.spaceInWingBornIslandOrPeaceCity(p.spaceNo):
                return self.isTransportActiveInWingPeaceCity(transportId)
            if TD.data.get(transportId, {}).get('initActive', 0) or transportId in BigWorld.player().transportHistory:
                return True
        return False

    def isTransportActiveInWingPeaceCity(self, transportId):
        p = BigWorld.player()
        transData = TD.data.get(transportId, {})
        if transData.get('mustOwner', 0):
            cityId = transData.get('cityId')
            if p.isWingWorldCampMode():
                return cityId == RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldNeighborCityId', 0)
            return cityId in p.wingWorld.country.getOwn().ownedCityIds or cityId == RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldNeighborCityId', 0)
        else:
            return True

    def refreshNpcPos(self, info = None):
        if info != None:
            self.npcInfo = info
        if self.mc is None:
            return
        elif BigWorld.player().isInPUBG():
            return
        else:
            npcData = self.getNpcData(info, self.getCurrentMapName())
            self.setNpcPos(npcData)
            return

    def getSpaceNo(self):
        return formula.getMapId(BigWorld.player().spaceNo)

    def getCurrentMapName(self):
        ret = ''
        if self.mc:
            ret = self.mc.Invoke('getMapName')
            return ret.GetString()
        else:
            return ret

    def getCurrentSpaceNo(self):
        ret = 9999
        p = BigWorld.player()
        if p.inWingCityOrBornIsland() and self.mapInfo.isThirdLvMap():
            return MTLD.data.get(self.mapInfo.mapId, {}).get('spaceNo', 0)
        elif self.mc:
            ret = self.mc.Invoke('getSpaceNo')
            return int(ret.GetNumber())
        else:
            return ret

    def setNpcPos(self, data):
        for itemData in data:
            newX, newY = self.transPos(itemData[1], itemData[2], self.getCurrentMapName())
            if newX == None:
                continue
            itemData[1] = newX
            itemData[2] = newY

        if self.mc:
            self.mc.Invoke('setIndicatorPos', uiUtils.array2GfxAarry(data, True))

    def onGetFortInfo(self, *arg):
        p = BigWorld.player()
        areaPoint = []
        fortInfo = []
        building = []
        reliveBoard = []
        if self.getSpaceNo() != 1 or p.isInPUBG():
            ret = [areaPoint, fortInfo]
            return uiUtils.array2GfxAarry(ret, True)
        else:
            p = BigWorld.player()
            clanWar = p.clanWar
            try:
                for key, item in CWFD.data.items():
                    if item.get('digongFort'):
                        continue
                    lPoint = item.get('fortLTPoint')
                    rPoint = item.get('fortBRPoint')
                    iconPos = item.get('fortIconPos')
                    mapName = self.getCurrentMapName()
                    forVal = clanWar.fort.get(key)
                    if p.clanWarStatus and lPoint and rPoint:
                        newLPoint = self.transPos(lPoint[0], lPoint[2], mapName)
                        newRPoint = self.transPos(rPoint[0], rPoint[2], mapName)
                        areaPoint.append([newLPoint, newRPoint])
                    if iconPos:
                        newIconPos = self.transPos(iconPos[0], iconPos[2], mapName)
                        fortName = clanWar.fort[key].ownerGuildName
                        fortFlag = clanWar.fort[key].ownerGuildFlag
                        guildNUID = clanWar.fort[key].ownerGuildNUID
                        fortType = item.get('type', 1)
                        flag = ''
                        color = ''
                        if guildNUID > 0:
                            guildIcon, guildColor = uiUtils.getGuildFlag(fortFlag)
                            if uiUtils.isDownloadImage(guildIcon):
                                if forVal.fromHostId != utils.getHostId() and not p.isDownloadNOSFileCompleted(guildIcon):
                                    p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, forVal.fromHostId, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                                else:
                                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                            flag = uiUtils.getGuildIconPath(guildIcon)
                            color = guildColor
                        fortInfo.append({'fortName': fortName,
                         'type': fortType,
                         'flag': flag,
                         'pos': newIconPos,
                         'color': color})

            except:
                pass

            for key, val in CWMD.data.items():
                if clanWar.cmarker.get(key):
                    if val['buildingType'] == gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD:
                        continue
                    state = 1
                else:
                    state = 0
                newPosition = self.transPos(val['position'][0], val['position'][2], mapName)
                building.append({'type': val['buildingType'],
                 'pos': newPosition,
                 'state': state})

            for nuid, val in clanWar.reliveBoard.items():
                newPos = self.transPos(val.pos[0], val.pos[2], mapName)
                reliveBoard.append({'nuid': str(val.nuid),
                 'pos': newPos})

            ret = [areaPoint,
             fortInfo,
             reliveBoard,
             building]
            return uiUtils.array2GfxAarry(ret, True)

    def onDownloadGuildIcon(self, status, callbackArgs):
        pass

    def getMapNameByNo(self, spaceNo, pos = None):
        mapId = formula.getMapId(spaceNo)
        p = BigWorld.player()
        if pos:
            if not p.inWingCityOrBornIsland():
                chunkName = uiUtils.getChunkName(pos[0], pos[2])
                if self.isThirdLvMap(spaceNo, chunkName):
                    return MTLD.data.get(self.thirdLvMapDict.get((mapId, chunkName))).get('mapPath', '')
            elif self.thirdLvMapSpaceNos.has_key(spaceNo):
                return self.thirdLvMapSpaceNos[spaceNo]
        return MII.data.get(mapId, {}).get('mapPath', '')

    def getMapIdBySpaceNo(self, spaceNo, pos, mapType = uiConst.MAP_TYPE_NORMAL):
        mapId = formula.getMapId(spaceNo)
        p = BigWorld.player()
        if pos and (mapType == uiConst.MAP_TYPE_NORMAL or p.inWingCityOrBornIsland()):
            if p.inWingCityOrBornIsland():
                chunkName = BigWorld.ChunkInfoAt(p.position)
            else:
                chunkName = uiUtils.getChunkName(pos[0], pos[2])
            mapId = self.thirdLvMapDict.get((mapId, chunkName), mapId)
        if p.inWingCityOrBornIsland():
            if not MTLD.data.has_key(mapId):
                if p.inWingPeaceCityOrBornIsland():
                    mapId = WWCFGD.data.get('wingWorldGlobalMapID', (90001, 90002))[0]
                else:
                    mapId = WWCFGD.data.get('wingWorldGlobalMapID', (90001, 90002))[1]
        return mapId

    def onGetCurrentMapInfo(self, *arg):
        spaceNo = self.getSpaceNo()
        p = BigWorld.player()
        yaw = BigWorld.player().yaw
        if not self.mapInfo.hasMapInfo():
            self.mapInfo.mapId = self.getMapIdBySpaceNo(spaceNo, BigWorld.player().position, self.mapInfo.mapType)
            self.mapInfo.initMapLv(self.mapInfo.mapLv)
        playerPos = self.getPlayerPos()
        self.mapInfo.pos = playerPos
        mapName = self.mapInfo.getMapName()
        pos = self.mapInfo.pos
        x, y = self.transPos(pos[0], pos[2], mapName)
        playerPosX, playerPosY = self.transPos(playerPos[0], playerPos[2], mapName)
        showName = gbk2unicode(MII.data.get(spaceNo, {}).get('mapName_ii', gameStrings.TEXT_MAPPROXY_1559))
        info = {'x': x,
         'y': y,
         'yaw': yaw * 180 / 3.14,
         'mapName': mapName,
         'showName': showName,
         'spaceNo': spaceNo,
         'isThirdLvMap': self.mapInfo.isThirdLvMap(),
         'playerPos': {'x': playerPosX,
                       'y': playerPosY},
         'mapType': self.mapInfo.mapType,
         'mapLv': self.mapInfo.mapLv,
         'canScale': self.mapInfo.getCanScale(),
         'inWingWorld': p.inWingCityOrBornIsland(),
         'showOverIconTime': SYSD.data.get('showOverIconTime', 200)}
        return uiUtils.dict2GfxDict(info, True)

    def setNpcItem(self, data):
        ret = self.movie.CreateArray()
        for i, item in enumerate(data):
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(item[0])))
            ar.SetElement(1, GfxValue(item[1]))
            ar.SetElement(2, GfxValue(item[2]))
            ret.SetElement(i, ar)

        if self.mc != None:
            self.mc.Invoke('setNpcItem', ret)

    def onSeekNpc(self, *arg):
        posId = arg[3][0].GetString()
        uiUtils.findPosById(posId)

    def hideSeekPos(self):
        if self.mc:
            self.mc.Invoke('hideSeekPos')

    def onRefreshOtherIcon(self, *args):
        self.addBattleFortIcon()
        self.addBattlePlaneIcon()
        p = BigWorld.player()
        enableWorldWarBattle = gameglobal.rds.configData.get('enableWorldWarBattle', False)
        if enableWorldWarBattle:
            if p.inWorldWarBattle():
                self.addWWBattleIcon(True)
            elif p.inWorldWarEx():
                self.addWWBattleIcon()
            if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if formula.spaceInWorldWar(p.spaceNo):
                    self.addWWRBattleIcon()
        if formula.spaceInWorldWarRob(p.spaceNo):
            self.addWWRBattleIcon()
        if gameglobal.rds.configData.get('enableGuildRobber'):
            self.refreshGuildRobberNpcInfo()
        self.refreshClanWarIncidentIcon()
        playerPos = self.getPlayerPos()
        self.setPlayerPos(playerPos[0], playerPos[2], p.yaw)

    def addWingWorldWarFlagIcon(self):
        if not self.mc:
            return
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        p = BigWorld.player()
        if not hasattr(p, 'wingWorld'):
            return
        if not p.isWingWorldCampMode():
            usedFlags = p.wingWorld.country.getUsedFlags()
            if not usedFlags:
                return
        ret = []
        if self.mapInfo.isThirdLvMap():
            nearbyWingCityIds = MTLD.data.get(self.mapInfo.mapId, {}).get('nearbyWingCityIds', ())
            if nearbyWingCityIds:
                for neighborCityId in nearbyWingCityIds:
                    self.appendCityWarFlag(ret, neighborCityId)

            elif self.currentCityId:
                self.appendCityWarFlag(ret, self.currentCityId)
        self.addOtherIns(uiConst.MAP_ICON_OTHER_WING_WAR_FLAG, ret)

    def addWingWorldGatherIcon(self):
        if not self.mc:
            return
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        p = BigWorld.player()
        if not p.isWingWorldCampMode():
            return
        if not p.wingWorldCamp:
            return
        if not gameglobal.rds.configData.get('enableWingWorldArmyGather', False):
            return
        if p.inWingWarCity() or p.inWingBornIsland() or p.inWingPeaceCity():
            pass
        else:
            return
        ret = []
        gatherCityId = p.getWingGatherCityId()
        if not self.mapInfo.isThirdLvMap():
            if gatherCityId:
                self.appendGatherFlag(ret, gatherCityId)
        self.addOtherIns(uiConst.MAP_ICON_WING_GATHER, ret)

    def appendGatherFlag(self, ret, cityId):
        p = BigWorld.player()
        pos = WWCTD.data.get(cityId, {}).get('mapPos', (1000, 1000))
        newPos = self.transPos(pos[0], pos[1], self.getCurrentMapName())
        tips = gameStrings.WING_WORLD_GATHER_TIP
        iconId = 'gather%d' % p.wingWorldCamp
        ret.append({'x': newPos[0],
         'y': newPos[1],
         'iconPath': 'wingWorld/%s.png' % str(iconId),
         'tips': tips})

    def appendCityWarFlag(self, ret, cityId):
        cfgData = WWCITYD.data.get(cityId, {})
        p = BigWorld.player()
        wingWorldCityVal = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId)
        if wingWorldCityVal.ownerHostId:
            if wingWorldCityVal.ownerHostId in gametypes.WING_WORLD_CAMPS:
                flagId = WWCD.data.get('wingCampIcons', gameStrings.WING_WORLD_CAMP_ICONS).get(wingWorldCityVal.ownerHostId, '')
                tips = gameStrings.WING_WORLD_OWN_CAMP_NAME % utils.getWingCampName(wingWorldCityVal.ownerHostId)
            else:
                country = p.wingWorld.country.getCountry(wingWorldCityVal.ownerHostId)
                flagId = country.flagId
                tips = gameStrings.WING_WORLD_OWN_HOST_NAME % RSCD.data.get(wingWorldCityVal.ownerHostId, {}).get('serverName', '')
            if flagId:
                pos = cfgData.get('warFlagPosition', (1000, 1000))
                pos = self.rTransPos(pos[0], pos[1], self.getCurrentMapName(), MAP_LV_0)
                newPos = self.transPos(pos[0], pos[1], self.getCurrentMapName())
                iconId = flagId if wingWorldCityVal.ownerHostId in gametypes.WING_WORLD_CAMPS else WWCFD.data.get(flagId, {}).get('icon', 0)
                htmlText = uiUtils.toHtml(tips, YELLOW_COLOR, fontSize=14)
                ret.append({'x': newPos[0],
                 'y': newPos[1],
                 'iconPath': 'wingWorld/wingWorldFlag/%s.dds' % str(iconId),
                 'tips': tips,
                 'textInfo': htmlText})

    def addWingWorldBossIcon(self, bossInfos):
        if not bossInfos:
            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_WING_BOSS_FLAG, [])
            return
        elif not self.mapWidget or not self.mapInfo or not self.mapInfo.isThirdLvMap():
            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_WING_BOSS_FLAG, [])
            return
        else:
            liveIconPath = WINGCD.data.get('liveIconPath', 'wingWorld/34213.dds')
            deathIconPath = WINGCD.data.get('deathIconPath', 'wingWorld/34214.dds')
            tipsPrefix = gameStrings.WING_WORLD_ALLSOULS_ICON_TIP
            ret = []
            for cfgId, state, killTime in bossInfos:
                if state not in (const.SOUL_BOSS_STATE_ALIVE, const.SOUL_BOSS_STATE_KILLED):
                    continue
                bossCfg = WSBD.data.get(cfgId, {})
                if not bossCfg:
                    continue
                bossPos = bossCfg.get('pos', None)
                bossName = MD.data.get(bossCfg.get('avatarId', 0), {}).get('name', '')
                mapPos = self.transPos(bossPos[0], bossPos[2], self.getCurrentMapName())
                bossIcon = liveIconPath if state == const.SOUL_BOSS_STATE_ALIVE else deathIconPath
                gamelog.debug('ypc@ bossIcon = ', bossIcon)
                ret.append({'x': mapPos[0],
                 'y': mapPos[1],
                 'iconPath': bossIcon,
                 'tips': tipsPrefix % bossName})

            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_WING_BOSS_FLAG, ret)
            return

    def addClanWarYaBiao(self):
        if not self.mapWidget or not gameconfigCommon.enableClanWarCourier():
            return
        elif not BigWorld.player().inClanCourier():
            return
        else:
            yabiaoStartIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoStartIcon', '')
            yabiaoEndIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoEndIcon', '')
            yabiaoMoveIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoMoveIcon', '')
            startPos = [ value.get('pos', (0, 0, 0)) for value in CCD.data.itervalues() ]
            startPos = set(startPos)
            endPos = [ value.get('dstPos', (0, 0, 0)) for value in CCD.data.itervalues() ]
            endPos = set(endPos)
            clanCourierDic = getattr(BigWorld.player(), 'clanCourierDic', {})
            movePos = [ value.get('pos', (0, 0, 0)) for value in clanCourierDic.itervalues() if value.get('pos', None) if not value.get('isEnd', False) ]
            ret = []
            if CCCD.data.get('clanWarYabiaoStartIcon', ''):
                for pos in startPos:
                    mapPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                    ret.append({'x': mapPos[0],
                     'y': mapPos[1],
                     'iconPath': yabiaoStartIcon})

            if CCCD.data.get('clanWarYabiaoEndIcon', ''):
                for pos in endPos:
                    mapPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                    ret.append({'x': mapPos[0],
                     'y': mapPos[1],
                     'iconPath': yabiaoEndIcon})

            for pos in movePos:
                mapPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                ret.append({'x': mapPos[0],
                 'y': mapPos[1],
                 'iconPath': yabiaoMoveIcon})

            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_CLAN_WAR_YABIAO, ret)
            return

    def addWorldBossIcons(self):
        if not self.mapWidget:
            return
        if not worldBossHelper.getInstance().isInWorldBossActivity():
            self.addOtherIns(uiConst.MAP_ICON_WORLD_BOSS, [])
        p = BigWorld.player()
        if not formula.inWorld(p.spaceNo):
            return
        ret = []
        bossDict = worldBossHelper.getInstance().getWorldBossInfos()
        for refId in bossDict:
            bossInfo = bossDict[refId]
            self.appendWorldBossInfo(bossInfo, ret)

        self.addOtherIns(uiConst.MAP_ICON_WORLD_BOSS, ret)

    def appendWorldBossInfo(self, bossInfo, ret):
        isLive = bossInfo.get('isLive', False)
        if not isLive:
            return
        else:
            pos = bossInfo.get('position', None)
            if not pos:
                return
            newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
            areaSize = self.getRealRadiusInWidget(DCD.data.get('worldBossAreaWidth', 60)) * 2
            tips = gameStrings.WORLD_BOSS_MAP_TIP % bossInfo.get('bossName', '')
            iconPath = bossInfo.get('mapIcon', '')
            ret.append({'x': newPos[0],
             'y': newPos[1],
             'position': pos,
             'width': areaSize,
             'height': areaSize,
             'iconPath': iconPath,
             'tips': tips})
            return

    def addBattleFortIcon(self):
        if not self.mc:
            return
        p = BigWorld.player()
        if not hasattr(p, 'bfFortInfo'):
            return
        ret = []
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            spaceNo = formula.getFubenNo(p.spaceNo)
            forts = BFD.data.get(spaceNo, {}).get('forts', ())
            for fortId in forts:
                info = p.bfFortInfo.get(fortId, {})
                if info:
                    x, _, z = info.get('pos', (0, 0, 0))
                    newPos = self.transPos(x, z, self.getCurrentMapName())
                    state = 0
                    fortId = info.get('fortId', 1)
                    curValMap = info.get('curValMap', {})
                    icon = BFFD.data.get(fortId, {}).get('icon', 1)
                    if not curValMap:
                        status = 0
                    else:
                        fortVal = info.get('curValMap', {}).get(p.tempCamp, 0)
                        if fortVal <= 0:
                            otherCamp = 3 - p.tempCamp
                            fortVal = -curValMap.get(otherCamp, 0)
                        occupType = self.uiAdapter.battleField.getFortOccupType(fortId, fortVal)
                        if occupType in (uiConst.BF_FORT_STATE_MY_FULL_HOLDED, uiConst.BF_FORT_STATE_ENEMY_FULL_HOLDED):
                            status = gametypes.BATTLE_FIELD_FLAG_STATTUS_FULL_HOLDED
                        elif occupType in (uiConst.BF_FORT_STATE_MY_HALF_HOLDED, uiConst.BF_FORT_STATE_ENEMY_HALF_HOLDED):
                            status = gametypes.BATTLE_FIELD_FLAG_STATTUS_HALF_HOLDED
                        else:
                            status = gametypes.BATTLE_FIELD_FLAG_STATTUS_DEFAULT
                    if status == 0:
                        state = icon * 1000 + status
                    else:
                        state = icon * 1000 + int(occupType in (uiConst.BF_FORT_STATE_MY_FULL_HOLDED, uiConst.BF_FORT_STATE_MY_HALF_HOLDED)) * 10 + status
                    ret.append({'pos': newPos,
                     'flag': ICON_PATH + '/battleFort/%d.dds' % state})

        self.mc.Invoke('addBattleFortIcon', uiUtils.array2GfxAarry(ret))

    def addBattlePlaneIcon(self):
        if not self.mc:
            return
        ret = []
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            if hasattr(p, 'bfPlanePosInfo'):
                for info in p.bfPlanePosInfo:
                    x, _, z = info.get('pos', (0, 0, 0))
                    camp = info.get('camp', 0)
                    if camp == p.tempCamp:
                        iconPath = ICON_PATH + '/battlePlane/1.dds'
                    else:
                        iconPath = ICON_PATH + '/battlePlane/2.dds'
                    newPos = self.transPos(x, z, self.getCurrentMapName())
                    ret.append({'pos': newPos,
                     'flag': iconPath})

        self.mc.Invoke('addBattlePlaneIcon', uiUtils.array2GfxAarry(ret))

    def addTeamMate(self, arr):
        self.teamArr = arr
        if self.mc:
            gfxArr = self.onGetTeamMate()
            self.mc.Invoke('addTeamMate', gfxArr)

    def onGetTeamMate(self, *arg):
        arr = copy.deepcopy(self.teamArr)
        ar = []
        p = BigWorld.player()
        currentMapName = self.getCurrentMapName()
        selfCityId = p.getWingCityId()
        for item in arr:
            if p.spaceNo == item[3] and item[0]:
                mapName = self.getMapNameByNo(item[3], item[0])
                if currentMapName == mapName or self.mapInfo.containsMap(mapName) or p.inWingCity() and selfCityId == p.getWingCityId(item[3]) == self.currentCityId or MTLD.data.get(self.mapInfo.mapId, {}).get('isBornIsland', 0) and formula.spaceInWingBornIsland(item[3]):
                    x, z = self.transPos(int(item[0][0]), int(item[0][2]), self.getCurrentMapName())
                    ar.append([x,
                     z,
                     str(item[1]),
                     gbk2unicode(item[2]),
                     item[6],
                     item[7],
                     item[8],
                     item[9],
                     item[10],
                     item[11],
                     p.getTeammateNoInPUBG(item[1])])

        gfxArr = uiUtils.array2GfxAarry(ar)
        return gfxArr

    def onSeekPoint(self, *arg):
        gamelog.info('jbx:onSeekPoint')
        mapName = self.getCurrentMapName()
        if mapName == '':
            return
        else:
            x = arg[3][0].GetNumber()
            y = arg[3][1].GetNumber()
            self.newX, self.newY = self.rTransPos(x, y, mapName, self.mapInfo.mapLv)
            p = BigWorld.player()
            pos = None
            spaceNo = self.getCurrentSpaceNo()
            isAltDown = BigWorld.getKeyDownState(keys.KEY_RALT, 0) or BigWorld.getKeyDownState(keys.KEY_LALT, 0)
            if not BigWorld.isPublishedVersion() and isAltDown:
                if spaceNo == formula.getMapId(p.spaceNo):
                    navigator.getNav().getNearbyPoint(Math.Vector3(self.newX, 400, self.newY), spaceNo, self._onSeekPointCallback, (50, 450, 50), True)
                else:
                    self._onSeekPointCallback(-1, 0, None)
            else:
                if spaceNo == formula.getMapId(p.spaceNo):
                    heightArray = (400, 300, 200, 100, 75, 50, 25)
                    for h in heightArray:
                        pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(self.newX, h, self.newY))
                        if pos:
                            pos = pos[0]
                            break

                if not pos:
                    pos = Math.Vector3(self.newX, navigator.UNKNOWN_Y, self.newY)
                if p.life != gametypes.LIFE_DEAD:
                    if p.canPathFindingWingWorld(spaceNo, False):
                        from helpers import wingWorld
                        wingWorld.pathFinding((pos[0],
                         pos[1],
                         pos[2],
                         spaceNo), endDist=0.5, showMsg=False, fromGroupFollow=False)
                    else:
                        ret = navigator.getNav().pathFinding((pos[0],
                         pos[1],
                         pos[2],
                         spaceNo), None, None, True, 0.5, self.onArrive)
                        if ret == 1:
                            p.topLogo.setAutoPathingVisible(True)
                    if p.inWingCityOrBornIsland() and self.currentCityId != p.getWingCityId():
                        mapId = self.getMapIdBySpaceNo(p.mapID, p.position, self.mapInfo.mapType)
                        self.setCurrentMap(mapId, p.position, MAP_LV_0)
            return

    def _onSeekPointCallback(self, pointnum, dist, pos):
        if not pos:
            pos = Math.Vector3(self.newX, navigator.UNKNOWN_Y, self.newY)
        self.mapTeleportDebug(pos)

    def onGetSeekPoint(self, *arg):
        gamelog.info('jbx:onGetSeekPoint')
        if not self.seekPoint:
            return GfxValue(False)
        currentMapName = self.mapInfo.getMapName()
        if self.seekPoint[2] != currentMapName:
            thirdLvMapNames = []
            if self.mapInfo.isThirdLvMap():
                pass
            else:
                for id in MII.data.get(self.mapInfo.mapId, {}).get('thirdLvMaps', ()):
                    info = MTLD.data.get(id)
                    if info:
                        thirdLvMapNames.append(info.get('mapPath'))

                if self.seekPoint[2] not in thirdLvMapNames:
                    return GfxValue(False)
        self.drawPathTrace(self.pathPoints, False)
        newX, newZ = self.transPos(self.seekPoint[0], self.seekPoint[1], currentMapName)
        seekPoint = [newX, newZ, self.seekPoint[2]]
        if self.pathPoints:
            return uiUtils.array2GfxAarry(seekPoint)
        else:
            return GfxValue(False)

    def onClickReliveBoard(self, *arg):
        nuid = long(arg[3][0].GetString())
        ok, cancel = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        p = BigWorld.player()
        contrib = GCD.data.get('guildTeleportConsumeContrib', 0)
        if contrib and not p.clanWarStatus:
            if p and p.life == gametypes.LIFE_DEAD:
                content = GMD.data.get(GMDD.data.MAP_GUILD_RELIEVE_CONTRIB_TIP, {}).get('text', '') % contrib
            else:
                content = GMD.data.get(GMDD.data.MAP_GUILD_TRANS_CONTRIB_TIP, {}).get('text', '') % contrib
        elif p and p.life == gametypes.LIFE_DEAD:
            content = GMD.data.get(GMDD.data.MAP_GUILD_RELIEVE_TIP, {}).get('text', '')
        else:
            content = GMD.data.get(GMDD.data.MAP_GUILD_TRANS_TIP, {}).get('text', '')
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(ok, Functor(self.reliveBoardConfirmOK, nuid)), MBButton(cancel)]
        gameglobal.rds.ui.messageBox.show(True, '', content, buttons)

    def reliveBoardConfirmOK(self, nuid):
        BigWorld.player().cell.teleportToReliveBoard(nuid)

    def setSeekPos(self, seekPoint):
        x, y, z, spaceNo = seekPoint
        p = BigWorld.player()
        if p.inWingCityOrBornIsland():
            mapName = self.getCurrentMapName()
        else:
            mapName = self.getMapNameByNo(spaceNo, (x, y, z))
        if mapName:
            self.seekPoint = [x,
             z,
             mapName,
             0]

    def showSeekPos(self):
        if self.mc and self.seekPoint:
            newX, newZ = self.transPos(self.seekPoint[0], self.seekPoint[1], self.mapInfo.getMapName())
            seekPoint = [newX, newZ, self.mapInfo.getMapName()]
            self.mc.Invoke('setSeekPoint', uiUtils.array2GfxAarry(seekPoint))

    def mapTeleportDebug(self, pos):
        if gameglobal.rds.isSinglePlayer:
            BigWorld.player().physics.teleport(pos)
        else:
            BigWorld.player().cell.adminOnCell('$goto %s %s %s' % (pos[0], pos[1], pos[2]))

    def onArrive(self):
        self.hideSeekPos()

    @ui.callFilter(1, False)
    def onTeleport(self, *arg):
        destId = int(arg[3][0].GetString())
        btnIndx = int(arg[3][1].GetNumber())
        if btnIndx == uiConst.RIGHT_BUTTON:
            uiUtils.findPosById(destId)
        else:
            p = BigWorld.player()
            destId = SD.data.get(destId, {}).get('npcId')
            if p.life == gametypes.LIFE_DEAD and formula.spaceInWingBornIslandOrPeaceCity(p.spaceNo):
                msg = WINGCD.data.get('peaceCityReliveFrameConfirm', '') % wingWorldUtils.getExtraTeleportJunzi()
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.wingPeaceCityReliveToStone, destId), title=gameStrings.TEXT_DEADANDRELIVEPROXY_193)
            else:
                p.cell.teleportToStone(destId)

    def wingPeaceCityReliveToStone(self, destId):
        BigWorld.player().cell.wingPeaceCityReliveToStone(destId)

    def onGetMapSign(self, *arg):
        mapSignArr = []
        for item in MSD.data.values():
            for lvSize in item['lvSize']:
                if self.mapInfo.mapLv == lvSize[0] - 1 and self.getMapNameByNo(item['mapId']) == self.getCurrentMapName():
                    x, y = self.transPos(item['x'], item['z'], self.getCurrentMapName())
                    mapSignArr.append([gbk2unicode(item['isShow']),
                     lvSize[1],
                     item['showType'],
                     x,
                     y])

        gfxArr = uiUtils.array2GfxAarry(mapSignArr)
        return gfxArr

    def drawPathTrace(self, pathPoints, append = True):
        p = BigWorld.player()
        if append:
            self.pathPoints.extend(pathPoints)
        else:
            self.pathPoints = pathPoints
        if self.mc:
            points = []
            mapName = self.getCurrentMapName()
            for point in pathPoints:
                points.append(self.transPos(point.x, point.z, mapName))

            if p.inWingCityOrBornIsland():
                if MTLD.data.has_key(self.mapInfo.mapId):
                    wingCityId = p.getWingCityId()
                    if wingCityId and self.currentCityId != wingCityId or p.inWingBornIsland() and self.currentCityId:
                        return
            self.mc.Invoke('addPathTrace', (uiUtils.array2GfxAarry(points), GfxValue(append), GfxValue(mapName)))
            if self.pathPoints:
                self.showSeekPos()

    def endDrawPathTrace(self):
        self.pathPoints = []
        if self.mc:
            self.mc.Invoke('addPathTrace', (uiUtils.array2GfxAarry([]), GfxValue(False)))
        self.hideSeekPos()

    def findMe(self):
        if self.mc:
            self.mc.Invoke('findMe')

    def onStartMark(self, *arg):
        state = arg[3][0].GetBool()
        if state:
            self.setMarkState()
        else:
            self.clearMarkState()

    def onAddMapMark(self, *arg):
        x = int(arg[3][0].GetNumber())
        y = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if p.isInPUBG():
            xInWorld, yInWorld = self.rTransPos(x, y, self.getCurrentMapName(), self.mapInfo.mapLv)
            self.setMarksIconInPUBG(p.gbId, xInWorld, yInWorld)
        else:
            if p.spaceNo != const.SPACE_NO_BIG_WORLD:
                p.showGameMsg(GMDD.data.MAP_MARK_ISWORLDMAP, ())
                return
            if len(p.mapMarkers) >= 6:
                p.showGameMsg(GMDD.data.MAP_MARK_NUM_LIMIT, ())
                return
            self.markX = x
            self.markY = y
            self.markType = 1
            self.curMark = self.getAddMarkIndex()
            self.showMarkEdit()

    def getAddMarkIndex(self, *arg):
        for i in range(6):
            if not BigWorld.player().mapMarkers.get(i + 1):
                return i + 1

    def onGetMapMark(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['type'] = self.markType
        if p.mapMarkers.has_key(self.curMark):
            ret['title'] = p.mapMarkers[self.curMark].title
            ret['desc'] = p.mapMarkers[self.curMark].desc
        return uiUtils.dict2GfxDict(ret, True)

    def onGetFogData(self, *arg):
        guild = BigWorld.player().guild
        info = []
        if guild:
            for areaValue in guild.area.itervalues():
                if not areaValue.isExtFinished():
                    picId = GAD.data.get(areaValue.areaId, {}).get('picId')
                    pos = GAD.data.get(areaValue.areaId, {}).get('fogPos')
                    info.append((picId, pos))

        return uiUtils.array2GfxAarry(info)

    def onEditMark(self, *arg):
        self.markType = 2
        self.curMark = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        mark = p.mapMarkers.get(self.curMark, {})
        if mark:
            self.markX = mark.pos[0]
            self.markY = mark.pos[2]
            self.showMarkEdit()

    def onDelMark(self, *arg):
        index = int(arg[3][0].GetNumber())
        BigWorld.player().cell.delMapMarker(index)

    def addMarks(self, *arg):
        if not self.mc:
            return
        if BigWorld.player().spaceNo != const.SPACE_NO_BIG_WORLD and not formula.spaceInClanWarPhase(BigWorld.player().spaceNo):
            return
        for key, val in BigWorld.player().mapMarkers.items():
            self.mc.Invoke('setMark', (GfxValue(val.pos[0]),
             GfxValue(val.pos[2]),
             GfxValue(key),
             GfxValue(gbk2unicode(val.title)),
             GfxValue(val.desc)))

    def updateMarks(self):
        if BigWorld.player().spaceNo != const.SPACE_NO_BIG_WORLD and not formula.spaceInClanWarPhase(BigWorld.player().spaceNo):
            return
        if self.mc:
            p = BigWorld.player()
            marks = {}
            for index, mark in p.mapMarkers.items():
                marks[index] = [mark.title]

            self.mc.Invoke('updateMarks', uiUtils.dict2GfxDict(marks, True))

    def onConfirmMark(self, *arg):
        title = unicode2gbk(arg[3][0].GetString())
        if not title:
            BigWorld.player().showGameMsg(GMDD.data.MAP_MARK_TITLE_ISBLANK, ())
            return
        desc = unicode2gbk(arg[3][1].GetString())
        p = BigWorld.player()
        showX = self.markX
        showY = self.markY
        if p.mapMarkers.get(self.curMark):
            startX = self.markX
            startY = self.markY
            showX = self.markX * 2 ** (self.mapInfo.mapLv - 1)
            showY = self.markY * 2 ** (self.mapInfo.mapLv - 1)
            p.cell.modifyMapMarker(self.curMark, (startX, 0, startY), title, desc)
        else:
            startX = self.markX * 2 ** (1 - self.mapInfo.mapLv)
            startY = self.markY * 2 ** (1 - self.mapInfo.mapLv)
            p.cell.addMapMarker(self.curMark, (startX, 0, startY), title, desc)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAP_MARK)
        if self.mc:
            self.mc.Invoke('setMark', (GfxValue(showX),
             GfxValue(showY),
             GfxValue(self.curMark),
             GfxValue(gbk2unicode(title)),
             GfxValue(gbk2unicode(desc))))

    def onCloseMark(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAP_MARK)

    def showMarkEdit(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MAP_MARK)

    def setMarkState(self):
        self.uiAdapter.clearState()
        self.isMarkState = True
        if ui.get_cursor_state() != ui.MAPMARK_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.MAPMARK_STATE)
            ui.set_cursor(cursor.pickup)
            ui.lock_cursor()

    def clearMarkState(self):
        if self.isMarkState:
            self.isMarkState = False
            if ui.get_cursor_state() == ui.MAPMARK_STATE:
                ui.reset_cursor()

    def onBroadCastSelf(self, *args):
        gameglobal.rds.ui.chat.doSendMapLink(None)
        self.onCloseMap()

    def onBroadCastMark(self, *args):
        index = int(args[3][0].GetNumber())
        mapName = self.getCurrentMapName()
        value = BigWorld.player().mapMarkers.get(index)
        if not value:
            return
        posInfo0, posInfo2 = self.rTransPos(value.pos[0], value.pos[2], mapName, self.mapInfo.mapLv)
        gameglobal.rds.ui.chat.doSendPos(posInfo0, navigator.UNKNOWN_Y, posInfo2, mapName)
        self.onCloseMap()

    def onGetBuildingData(self, *args):
        ret = []
        guild = BigWorld.player().guild
        if guild:
            for markerId in guild.marker.iterkeys():
                markerData = GBMD.data.get(markerId, {})
                buildingNUID = guild.marker[markerId].buildingNUID
                buildValue = guild.building.get(buildingNUID) if buildingNUID else None
                if buildValue:
                    picList = GBD.data.get(buildValue.buildingId, {}).get('picId', [])
                    if picList:
                        name = GBD.data.get(buildValue.buildingId, {}).get('name', '')
                        level = buildValue.level
                        pic = picList[level]
                        mapPos = markerData.get('mapPos')
                        if mapPos:
                            ret.append({'name': name,
                             'lv': level,
                             'pic': pic,
                             'pos': mapPos})

        return uiUtils.array2GfxAarry(ret, True)

    def onGetPlayTipData(self, *args):
        seekId = args[3][0].GetNumber()
        playRecommId = SD.data.get(seekId, {}).get('npcId', 0)
        if not playRecommId:
            return uiUtils.dict2GfxDict({'isNone': True}, True)
        pradd = PRAD.data
        aData = pradd.get(playRecommId, {})
        displayType = aData.get('displayType', ())
        ret = gameglobal.rds.ui.playRecomm.genLvUpItemInfo(aData, displayType, playRecommId, True)
        return uiUtils.dict2GfxDict(ret, True)

    def addWWBattleIcon(self, isAddBattleFort = False):
        ret = []
        p = BigWorld.player()
        ww = p.worldWar
        if isAddBattleFort:
            for fortId, val in WWFD.data.items():
                if val.get('icon'):
                    areaMapIds = copy.deepcopy(list(val.get('wwMapId', [])))
                    areaMapIds.append(val.get('areaMapId', 0))
                    if gameglobal.rds.ui.littleMap.curViewMapNo not in areaMapIds:
                        continue
                    pos = val.get('position', (0, 0, 0))
                    camp = 0
                    hostId = ww.getFortHostId(fortId)
                    if hostId:
                        camp = ww.getCountry(hostId).camp
                    newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                    infoType = val.get('type', -1)
                    ret.append({'pos': newPos,
                     'flag': ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp),
                     'infoType': infoType})

        for reliveId, val in WWRBD.data.items():
            if val.get('icon'):
                pos = val.get('position', (0, 0, 0))
                hostId = ww.reliveBoard.get(reliveId, 0)
                camp = BigWorld.player().getWorldWarSideByHostId(hostId)
                newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                ret.append({'pos': newPos,
                 'flag': ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp)})

        if self.mc:
            self.mc.Invoke('addWWBattleIcon', uiUtils.array2GfxAarry(ret))

    def addWWRBattleIcon(self):
        ret = []
        p = BigWorld.player()
        ww = p.worldWar
        if not p.isWWRInRightState():
            return
        for fortId, val in WWFD.data.items():
            if val.get('icon'):
                if val.get('type', 0) in gametypes.WW_ROB_MAP_ICON_TYPES and val.get('robAreaMapId', ()):
                    pos = val.get('position', (0, 0, 0))
                    infoType = val.get('type', -1)
                    camp = 0
                    if infoType == gametypes.WW_ROB_FORT_TYPE:
                        hostId = ww.getFortHostId(fortId)
                        camp = BigWorld.player().getWorldWarSideByHostId(hostId)
                    newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                    ret.append({'pos': newPos,
                     'flag': ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp),
                     'infoType': infoType})

        if self.mc:
            self.mc.Invoke('addWWRBattleIcon', uiUtils.array2GfxAarry(ret))

    def onGetRobZaijuInfo(self, *args):
        p = BigWorld.player()
        ww = p.worldWar
        pos = ww.robZaiju.position
        ret = {}
        if not p.isWWRInRightState():
            ret['visible'] = False
            return uiUtils.dict2GfxDict(ret, True)
        elif ww.robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN:
            ret['visible'] = False
            return uiUtils.dict2GfxDict(ret, True)
        elif ww.robState in gametypes.WW_ROB_STATE_NOT_OPEN or not pos or not p.isInRobSpace():
            ret['visible'] = False
            return uiUtils.dict2GfxDict(ret, True)
        else:
            ret['visible'] = True
            ret['pos'] = self.transPos(pos[0], pos[2], self.getCurrentMapName())
            ret['radio'] = WWCD.data.get('robZaijuAuraRange', 0)
            ret['level'] = ww.robZaiju.level
            radio = WWCD.data.get('robZaijuAuraRange', 0)
            ret['lPos'] = self.transPos(pos[0] - radio, pos[2], self.getCurrentMapName())
            ret['rPos'] = self.transPos(pos[0] + radio, pos[2], self.getCurrentMapName())
            return uiUtils.dict2GfxDict(ret, True)

    def refreshRobZaiju(self):
        if self.mc:
            self.mc.Invoke('refreshRobZaiju')

    def onShowThirdLvMap(self, *args):
        info = asObject.ASObject(args[3][0])
        pos = asObject.ASObject(args[3][1])
        self.setCurrentMap(int(info.mapId), Math.Vector3(pos[0], 0, pos[1]), MAP_LV_0)

    def onGetThirdLvMapIcons(self, *args):
        icons = []
        p = BigWorld.player()
        if self.checkShowThirdLvMap():
            for id in MII.data.get(self.mapInfo.mapId, {}).get('thirdLvMaps', ()):
                info = MTLD.data.get(id)
                if info:
                    if info.get('isBornIsland', 0):
                        iconPosInMap = RSCD.data.get(p.getOriginHostId(), {}).get('iconPosInMap', (0, 0))
                    else:
                        iconPosInMap = info.get('iconPosInMap')
                    icons.append({'path': 'widgets/thirdLvMapSwf/%s.swf' % info.get('iconPath', ''),
                     'x': iconPosInMap[0],
                     'y': iconPosInMap[1],
                     'mapId': id})

        return uiUtils.array2GfxAarry(icons)

    def checkShowThirdLvMap(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        return True

    def setCurrentMap(self, mapId, pos, mapLv = MAP_LV_1):
        if mapId == self.mapInfo.mapId:
            return
        p = BigWorld.player()
        if p.inWingWarCity() and MTLD.data.has_key(mapId):
            spaceNo = MTLD.data.get(mapId, {}).get('spaceNo', 0)
            cityId = p.getWingWarCityId(spaceNo)
            attackCityIds, defCityIds = self.uiAdapter.wingWorldStrategy.getAttackAndDefCityIdList()
            if cityId not in attackCityIds and cityId not in defCityIds:
                p.showGameMsg(GMDD.data.CAN_NOT_OPEN_NOT_RELATIVE_CITY, ())
                return
        gamelog.info('jbx:setCurrentMap', mapId, pos, mapLv)
        self.mapInfo.mapId = mapId
        self.mapInfo.pos = pos
        self.mapInfo.mapLv = mapLv
        self.mc.Invoke('init')
        if BigWorld.player().inWingCityOrBornIsland():
            self.onConfigUICallback()

    def onScaleToSecLvMap(self, *args):
        p = BigWorld.player()
        map = asObject.ASObject(self.mc)
        pos = self.rTransPos(map.bgmap.mouseX, map.bgmap.mouseY, self.getCurrentMapName())
        self.setCurrentMap(self.getMapIdBySpaceNo(p.spaceNo, None), Math.Vector3(pos[0], 0, pos[1]), MAP_LV_0)

    def onGetMapMaxLv(self, *args):
        maxLv = 5 if BigWorld.player().inWingCityOrBornIsland() else 3
        return GfxValue(maxLv)

    def onGetThirdIconScale(self, *args):
        mapId = int(args[3][0].GetNumber())
        return GfxValue(MTLD.data.get(mapId, {}).get('thirdIconScale', 1))

    def onSetLevelCompleted(self, *args):
        p = BigWorld.player()
        if p.inWingWarCity():
            self.refreshWingWorldIcons()
            self.refreshWingWorldMarks()
        self.refreshClanWarIncidentIcon()
        self.refreshAllPUBGUI()
        self.refreshDoublePlantTreeUI()
        self.refreshHuntGhostUI()
        self.addWorldBossIcons()

    def onScaleToThirdLvMap(self, *args):
        if self.mapInfo.isThirdLvMap():
            return
        if not self.checkShowThirdLvMap():
            return
        p = BigWorld.player()
        mapId = 0
        if p.inWingCityOrBornIsland() and len(args[3]):
            mapId = int(args[3][0].GetNumber())
        map = asObject.ASObject(self.mc)
        pos = self.rTransPos(map.bgmap.mouseX, map.bgmap.mouseY, self.getCurrentMapName())
        worldPos = Math.Vector3(pos[0], 0, pos[1])
        if not mapId:
            mapId = self.getMapIdBySpaceNo(BigWorld.player().spaceNo, worldPos)
        self.setCurrentMap(mapId, worldPos, MAP_LV_0)

    def onGetBgMapChildMcRelayoutDataByLevel(self, *args):
        childRelayoutDataArr = []
        for childMcName, childMcData in BGMAP_CM_RELAYOUT_DATA.iteritems():
            childRelayoutData = list()
            childRelayoutData.append(childMcName)
            childRelayoutData.append(childMcData[0])
            childRelayoutDataArr.append(childRelayoutData)

        gfxArr = uiUtils.array2GfxAarry(childRelayoutDataArr)
        return gfxArr

    def onGetBgMapChildMcIdxData(self, *args):
        childIdxDataArr = []
        for childMcName, childMcData in BGMAP_CM_RELAYOUT_DATA.iteritems():
            childIdxData = list()
            childIdxData.append(childMcName)
            childIdxData.append(childMcData[1])
            childIdxDataArr.append(childIdxData)

        gfxArr = uiUtils.array2GfxAarry(childIdxDataArr)
        return gfxArr

    def onGetMapSize(self, *args):
        mapName = args[3][0].GetString()
        lv = int(args[3][1].GetNumber())
        return uiUtils.array2GfxAarry(self.mapSize.get(mapName, [19660800])[lv])

    def onClickIcon(self, *args):
        iconData = asObject.ASObject(args[3][0])
        p = BigWorld.player()
        gamelog.info('jbx:onClickIcon', iconData.pos)
        if iconData.pos:
            p.pathFindingTo(iconData.pos, p.spaceNo)
        if p.inWingWarCity():
            cityId, entNo, buildingId, buildingType = iconData.data
            entNo = int(entNo)
            if buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD:
                worldMapCache = BigWorld.player().wingWorld.worldMapCache
                if not worldMapCache.has_key(cityId):
                    return
                if not worldMapCache[cityId].buildDic.has_key(entNo):
                    return
                wingWorldCityBuildingMinMap = worldMapCache[cityId].buildDic[entNo]
                if p.isWingWorldCampMode():
                    if wingWorldCityBuildingMinMap.ownHostId != p.wingWorldCamp:
                        p.showGameMsg(GMDD.data.RELIVE_BOARD_NOT_FORBIDDEN, ())
                        return
                elif wingWorldCityBuildingMinMap.ownHostId != p.getOriginHostId():
                    p.showGameMsg(GMDD.data.RELIVE_BOARD_NOT_FORBIDDEN, ())
                    return
                if p.life == gametypes.LIFE_DEAD:
                    gamelog.info('jbx:cell.wingWorldWarReliveTo', entNo)
                    if MTLD.data.get(self.mapInfo.mapId, {}).get('wingCityId', 0) != p.getWingWarCityId():
                        p.showGameMsg(GMDD.data.CANT_OPEN_OTHER_CITY_MAP_IN_WAR, ())
                        return
                    p.cell.wingWorldWarReliveTo(entNo)
                else:
                    if not (self.mapInfo.mapType == uiConst.MAP_TYPE_TRANSPORT and self.uiAdapter.pressKeyF.wingWorldReliveBoardId):
                        p.showGameMsg(GMDD.data.NO_RELIVE_BOARD_NEARBY, ())
                        return
                    if cityId != p.getWingWarCityId():
                        msg = GMD.data.get(GMDD.data.CITY_TELEPORT_CONFIRM, {}).get('text', '%s') % WWCTD.data.get(int(cityId), {}).get('name', '')
                        self.openMap(False)
                        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.teleportToWingWarCity, int(cityId)))
                        return
                    gamelog.info('jbx:cell.wingWorldWarTeleportToOwnerReliveBoard', entNo)
                    p.cell.wingWorldWarTeleportToOwnerReliveBoard(entNo)
                self.openMap(False)

    def teleportToWingWarCity(self, cityId):
        BigWorld.player().teleportToWingWarCity(cityId)

    def onInWingWorldWarCity(self, *args):
        return GfxValue(BigWorld.player().inWingWarCity())

    def getMapSizeDict(self):
        sizeDict = {'ycdg': [(2400, 1600), (4800, 3200), (9600, 6400)],
         '00_xsc': [(2560, 2560), (2560, 2560), (2560, 2560)],
         'guild': [(1920, 1920), (1920, 1920), (1920, 1920)],
         'zc_wjzd': [(2560, 2560), (2560, 2560), (2560, 2560)],
         'dgbj': [(2048, 1280), (4096, 2560), (8192, 5120)],
         'wingWorld': [(2400, 1600), (4800, 3200), (9600, 6400)]}
        for value in MTLD.data.values():
            mapName = value.get('mapPath')
            if value.has_key('lvSizes'):
                sizeDict[mapName] = value['lvSizes']
            if not sizeDict.has_key(mapName):
                sizeDict[mapName] = [(value.get('spaceWidth', 0), value.get('spaceHeight', 0))] * 3

        return sizeDict

    def refreshWingWorldIcons(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        if not self.currentCityId:
            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_BATTLEFIELD_WING_WORLD, [])
            self.addOtherIns(uiConst.MAP_ICON_BUILDING_HP, [])
            self.addOtherIns(uiConst.MAP_ICON_OCCUPY_BUILDING_NAME, [])
            return
        buildingIconList = []
        occupyBuildingList = []
        hpIconList = []
        worldMapCache = BigWorld.player().wingWorld.worldMapCache
        if not worldMapCache.has_key(self.currentCityId):
            return
        originalHostId = p.getOriginHostId()
        for entNo, wingWorldCityBuildingMinMap in worldMapCache[self.currentCityId].buildDic.iteritems():
            ownHostId = wingWorldCityBuildingMinMap.ownHostId
            campIndex = worldMapCache[self.currentCityId].attendHost2ColorIdx.get(ownHostId, 0)
            cityId = self.currentCityId
            cfgData = WCBED.data.get(entNo, {})
            buildingId = cfgData.get('buildingId', 0)
            offsetPos = WCBED.data.get(entNo, {}).get('offsetPos', (0, 0))
            buildingType = WCBD.data.get(buildingId, {}).get('buildingType', gametypes.WING_CITY_BUILDING_TYPE_GATE)
            pos = cfgData.get('position', (0, 0, 0))
            newX, newY = self.transPos(pos[0] + offsetPos[0], pos[2] + offsetPos[1], self.getCurrentMapName())
            if buildingType in gametypes.WING_CITY_WAR_SHOW_HP_TYPES or buildingType == gametypes.WING_CITY_BUILDING_TYPE_AIR_STONE:
                if not wingWorldCityBuildingMinMap.hpPercent:
                    campIndex = 4
                else:
                    campIndex = 1
            iconPath = WING_WORLD_ICON_PATH + '/%s.dds' % (WCBD.data.get(buildingId, {}).get('buildingIcon', str(buildingId)) + '_' + str(campIndex))
            iconData = (cityId,
             entNo,
             buildingId,
             buildingType)
            iconInfo = {'x': newX,
             'y': newY,
             'iconPath': iconPath,
             'data': iconData,
             'tips': WCBD.data.get(buildingId, {}).get('tips', 'tips%d' % buildingId)}
            if p.isWingWorldCampMode():
                if self.currentCityId in p.wingWorld.country.getOwnCamp().ownedCityIds and buildingType in gametypes.WING_CITY_WAR_SHOW_HP_TYPES:
                    iconInfo['hp'] = wingWorldCityBuildingMinMap.hpPercent
                    hpIconList.append(iconInfo)
                else:
                    buildingIconList.append(iconInfo)
            elif self.currentCityId in p.wingWorld.country.getCountry(originalHostId).ownedCityIds and buildingType in gametypes.WING_CITY_WAR_SHOW_HP_TYPES:
                iconInfo['hp'] = wingWorldCityBuildingMinMap.hpPercent
                hpIconList.append(iconInfo)
            else:
                buildingIconList.append(iconInfo)
            if buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD:
                iconInfo['reliveBoardId'] = entNo
            if wingWorldUtils.isBuildintEntityOccupyable(entNo) and campIndex:
                hostNameOffset = WWCFGD.data.get('hostNameOffset', (12, -20))
                x, y = newX + hostNameOffset[0], newY + hostNameOffset[1]
                text = ''
                if p.isWingWorldCampMode():
                    if ownHostId in gametypes.WING_WORLD_CAMPS:
                        campNames = utils.getWingCampName(ownHostId)
                        text = uiUtils.toHtml(campNames[0:2], CAN_OCCUPY_BUILDING_COLOR[campIndex - 1])
                else:
                    text = uiUtils.toHtml(RSCD.data.get(ownHostId, {}).get('serverName', '')[0:2], CAN_OCCUPY_BUILDING_COLOR[campIndex - 1])
                occupyIconInfo = {'x': x,
                 'y': y,
                 'textInfo': text}
                occupyBuildingList.append(occupyIconInfo)

        gamelog.info('jbx:refreshWingWorldIcons', len(buildingIconList), len(hpIconList), len(occupyBuildingList))
        self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_BATTLEFIELD_WING_WORLD, buildingIconList)
        self.addOtherIns(uiConst.MAP_ICON_BUILDING_HP, hpIconList)
        self.addOtherIns(uiConst.MAP_ICON_OCCUPY_BUILDING_NAME, occupyBuildingList)

    def addOtherIns(self, type, data, useCache = True, insName = None):
        tmpIcons = getattr(self.mapWidget.otherIconsDict, type, None)
        insName = type if not insName else insName
        if tmpIcons == None:
            tmpIcons = []
        elif not useCache:
            while tmpIcons:
                removeIcon = tmpIcons.pop()
                self.mapWidget.removeToCache(removeIcon)

        for icon in tmpIcons:
            icon.visible = False

        for index, iconData in enumerate(data):
            icon = None
            if len(tmpIcons) > index and tmpIcons[index]:
                icon = tmpIcons[index]
            else:
                icon = self.mapWidget.getInstByClsName(insName)
                tmpIcons.append(icon)
            self.processIcon(type, icon, iconData)
            icon.iconType = type
            icon.visible = True
            if iconData.has_key('tips'):
                asObject.TipManager.addTip(icon, iconData['tips'])
            else:
                asObject.TipManager.removeTip(icon)
            icon.x = iconData['x'] - icon.width / 2
            iconHeight = iconData.get('iconHeight', icon.height)
            icon.y = iconData['y'] - iconHeight / 2
            icon.iconData = iconData
            icon.iconData.iconType = type
            self.mapWidget.otherIconCanvas.addChild(icon)

        setattr(self.mapWidget.otherIconsDict, type, tmpIcons)

    def processIcon(self, type, icon, iconData):
        if type == uiConst.MAP_ICON_OTHER_GUILD_FLAG:
            icon.icon.fitSize = True
            icon.icon.loadImage(iconData['iconPath'])
            icon.textMc.htmlText = iconData['textInfo']
        elif type == uiConst.MAP_ICON_BUILDING_HP:
            icon.icon.fitSize = True
            icon.icon.loadImage(iconData['iconPath'])
            icon.hp.currentValue = iconData['hp']
        elif type == uiConst.MAP_ICON_OTHER_WING_WAR_FLAG:
            icon.icon.fitSize = True
            icon.icon.loadImage(iconData['iconPath'])
            icon.textMc.htmlText = iconData['textInfo']
        elif type == uiConst.MAP_ICON_OCCUPY_BUILDING_NAME:
            icon.content.htmlText = iconData['textInfo']
        elif type == uiConst.MAP_ICON_BATTLE_PUBG_MARK:
            icon.gotoAndStop('mark%d' % int(iconData['teammateNo']))
        elif type == uiConst.MAP_ICON_BATTLE_PUBG_DISASTER:
            icon.width = icon.height = iconData['radius']
        elif type in [uiConst.MAP_ICON_BATTLE_PUBG_TREASURE_BOX, uiConst.MAP_ICON_HUNT_GHOST]:
            if iconData['leftTimeStr']:
                if icon.bg:
                    icon.bg.visible = True
            elif icon.bg:
                icon.bg.visible = False
            icon.leftTimeTxt.text = iconData['leftTimeStr']
        elif type == uiConst.MAP_ICON_WING_GATHER:
            icon.icon.fitSize = True
            icon.icon.loadImage(iconData['iconPath'])
        elif type == uiConst.MAP_ICON_WORLD_BOSS:
            icon.icon.fitSize = True
            icon.icon.loadImage(iconData['iconPath'])
            icon.area.width = iconData['width']
            icon.area.height = iconData['height']
            icon.icon.position = iconData['position']
            icon.icon.addEventListener(events.MOUSE_CLICK, self.onBossIconClick)
            icon.icon.x = max(0, (icon.area.width - icon.icon.width) / 2)
            icon.icon.y = max(0, (icon.area.height - icon.icon.height) / 2)
            if icon.icon.x == 0:
                icon.area.visible = False
            else:
                icon.area.visible = True

    def onBossIconClick(self, *args):
        from guis.asObject import ASObject
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.LEFT_BUTTON:
            return
        position = e.currentTarget.position
        if position:
            pos = Math.Vector3(position[0], position[1], position[2])
            uiUtils.findPosByPos(1, pos)

    def refreshWingWorldOrePoint(self, currentCityId = 0):
        if not self.mapWidget:
            return
        elif not wingWorldUtils.isResourcePointBossExistPeriod():
            self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_ADD_RESOURCE_POINT, [])
            return
        else:
            resPoints = wingWorldUtils.getResourcePointsByCityId(currentCityId)
            gamelog.info('@yj:refreshWingWorldOrePoint:resPoints', resPoints)
            if not resPoints:
                self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_ADD_RESOURCE_POINT, [])
                return
            p = BigWorld.player()
            isBornIsland = MTLD.data.get(self.mapInfo.mapId, {}).get('isBornIsland', 0)
            resourcePoints = {}
            if currentCityId:
                resourcePoints = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, currentCityId).resourcePoints
            elif isBornIsland:
                resourcePoints = p.wingWorld.country.getOwn().resourcePointMap
            gamelog.info('@yj:refreshWingWorldOrePoint:resourcePoints', resourcePoints)
            protectTime = WWCFGD.data.get('wingWolrdProtectTime', 1800)
            selfHostId = p.getOriginHostId()
            ret = []
            for pointId in resPoints:
                data = WCRD.data.get(pointId, {})
                resType = data.get('resType', 0)
                pos = data.get('position', (0, 0, 0))
                newPos = self.transPos(pos[0], pos[2], self.getCurrentMapName())
                insName = 'Wing_World_Ore_Point%d' % resType
                pointFrom = 'normal'
                resStateDesc = gameStrings.TEXT_CLANWARPROXY_111
                if pointId in resourcePoints:
                    if selfHostId == resourcePoints[pointId].ownerHostId:
                        pointFrom = 'mine'
                    else:
                        pointFrom = 'other'
                    occuyDesc = gameStrings.TEXT_MAPPROXY_2767 if resourcePoints[pointId].ownerHostId in gametypes.WING_WORLD_CAMPS else gameStrings.TEXT_MAPPROXY_2767_1
                    resStateDesc = occuyDesc % utils.getCountryName(resourcePoints[pointId].ownerHostId)
                pointState = 0
                pointVal = resourcePoints.get(pointId, None)
                if pointVal and pointVal.state == gametypes.WING_RESOURCE_POINT_STATE_NORMAL:
                    pointState = 0
                elif pointVal and pointVal.state == gametypes.WING_RESOURCE_POINT_STATE_FIGHTING:
                    pointState = 1
                if pointVal and hasattr(pointVal, 'occupyTime'):
                    occupyTime = resourcePoints[pointId].occupyTime
                    if occupyTime and utils.getNow() - occupyTime <= protectTime:
                        pointState = 2
                resName = data.get('name', '')
                tipDesc = '%s\n%s' % (resName, resStateDesc)
                iconInfo = {}
                iconInfo['insName'] = insName
                iconInfo['pos'] = newPos
                iconInfo['pointFrom'] = pointFrom
                iconInfo['pointState'] = pointState
                iconInfo['tipDesc'] = tipDesc
                ret.append(iconInfo)

            self.mapWidget.addWingWorldOrePointIcon(uiConst.MAP_ICON_ADD_RESOURCE_POINT, ret)
            return

    def refreshWingWorldGuildFlag(self):
        if not self.mapWidget:
            return
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            return
        iconList = []
        if self.mapInfo.isThirdLvMap():
            nearbyWingCityIds = MTLD.data.get(self.mapInfo.mapId, {}).get('nearbyWingCityIds', ())
            if nearbyWingCityIds:
                for id in nearbyWingCityIds:
                    self.appendGuildFlag(iconList, id)

            elif self.currentCityId:
                self.appendGuildFlag(iconList, self.currentCityId)
        self.addOtherIns(uiConst.MAP_ICON_OTHER_GUILD_FLAG, iconList, False)
        gamelog.info('jbx:refreshWingWorldGuildFlag', len(iconList))

    def appendGuildFlag(self, iconList, cityId):
        p = BigWorld.player()
        cfgData = WWCITYD.data.get(cityId, {})
        city = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId)
        rankCity = self.getFirstRankGuild(city.adminGuildMap)
        if rankCity:
            guildFlag = rankCity.guildFlag
            guildName = rankCity.guildName
            icon, color = uiUtils.getGuildFlag(guildFlag)
            tips = gameStrings.WING_WORLD_ADMIN_GUILD % guildName
            pos = cfgData.get('guildFlagPosition', (1000, 1050))
            if uiUtils.isDownloadImage(icon) and not p.isDownloadNOSFileCompleted(icon):
                p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, city.ownerHostId, gametypes.NOS_FILE_PICTURE, self.guildIconDownLoadCallback, ())
            iconPath = uiUtils.getGuildIconPath(icon)
            pos = self.rTransPos(pos[0], pos[1], self.getCurrentMapName(), MAP_LV_0)
            newX, newY = self.transPos(pos[0], pos[1], self.getCurrentMapName())
            iconInfo = {'x': newX,
             'y': newY,
             'iconPath': iconPath,
             'color': color,
             'tips': tips}
            htmlText = uiUtils.toHtml(guildName, YELLOW_COLOR, fontSize=14)
            iconInfo['textInfo'] = htmlText
            iconList.append(iconInfo)

    def guildIconDownLoadCallback(self, *args):
        gamelog.info('jbx:guildIconDownLoadCallback')
        self.refreshWingWorldGuildFlag()

    def getFirstRankGuild(self, adminGuildMap):
        for guldNuild, val in adminGuildMap.iteritems():
            if val.rank == 1:
                return val

    def refreshWingWorldMarks(self):
        if not self.mapWidget:
            return
        if not self.currentCityId:
            self.mapWidget.removeAllInst(self.mapWidget.wingWorldMarkCanvas)
            return
        wingWorldMarkPoints = getattr(BigWorld.player(), 'wingWorldMapMarkPoints', [])
        marks = []
        if self.currentCityId != BigWorld.player().getWingWarCityId():
            self.mapWidget.removeAllInst(self.mapWidget.wingWorldMarkCanvas)
            return
        for index, points in enumerate(wingWorldMarkPoints):
            if not points:
                continue
            marks.append((index,
             points[0],
             points[1],
             points[2]))

        self.mapWidget.removeAllInst(self.mapWidget.wingWorldMarkCanvas)
        self.mapWidget.bgmap.setChildIndex(self.mapWidget.wingWorldMarkCanvas, self.mapWidget.bgmap.numChildren - 1)
        for index, x, y, markType in marks:
            posX, posY = self.transPos(x, y, self.getCurrentMapName())
            markMc = self.mapWidget.getInstByClsName('Map_mark%d' % markType)
            self.mapWidget.wingWorldMarkCanvas.addChild(markMc)
            markMc.x = posX
            markMc.y = posY
            markMc.realPos = (x, y)
            markMc.markType = markType
            markMc.markIdx = index
            markMc.addEventListener(events.MOUSE_CLICK, self.handleMarkIconClick, False, 0, True)

    def handleMarkIconClick(self, *args):
        e = asObject.ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            markIcon = e.currentTarget
            if markIcon.markType != None:
                gamelog.info('jbx:delWingWorldMinMapPoint', self.currentCityId, markIcon.markIdx, markIcon.x, markIcon.y, markIcon.markType)
                BigWorld.player().cell.delWingWorldMinMapPoint(self.currentCityId, int(markIcon.markIdx), int(markIcon.realPos[0]), int(markIcon.realPos[1]), int(markIcon.markType))
                e.stopImmediatePropagation()

    def refreshGuildRobberNpcInfo(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        if p.inGuildSpace() and hasattr(p, 'guildRobberNpcInfo'):
            items = []
            for info in p.guildRobberNpcInfo:
                newX, newY = self.transPos(info[0][0], info[0][2], self.getCurrentMapName())
                items.append({'x': newX,
                 'y': newY,
                 'iconPath': ICON_PATH + 'common/guildRobberNpc.dds',
                 'pos': info[0]})

            self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_GUILD_ROBBER_NPC, items)

    def refreshClanWarIncidentIcon(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableClanWarOptimizationEvent', False):
            return
        if not self.isInNewClanWarTime():
            return
        if not self.mapWidget:
            return
        if p.isInPUBG():
            return
        items = []
        fortList = []
        eventSeasonStartCrontab = CCWCD.data.get('eventSeasonStartCrontab')
        eventSeasonStartTime = utils.getPreCrontabTime(eventSeasonStartCrontab)
        deltaDay = (calendar.SATURDAY - datetime.datetime.fromtimestamp(eventSeasonStartTime).weekday()) % 7
        firstEventStartTime = eventSeasonStartTime + const.TIME_INTERVAL_DAY * deltaDay
        nowWeekIndex = utils.getIntervalWeek(utils.getNow(), firstEventStartTime) + 1
        score = 0
        forId = 0
        for id, event in CWELD.data.iteritems():
            if id == nowWeekIndex:
                score = event.get('score', 0)
                forId = event.get('fortId', 0)
                break

        fortInfo = CWFD.data.get(forId, {})
        fortIconPos = fortInfo.get('fortIncidentIconPos', ())
        iconName = fortInfo.get('fortIncidentIconName', 'duanhaiji')
        x, y = self.transPos(fortIconPos[0], fortIconPos[2], self.getCurrentMapName())
        tips = gameStrings.CLAN_WAR_INCIDENT_MAP_ICON_TIP % score
        items.append({'x': x,
         'y': y,
         'iconPath': 'clanWarFlag/%s.dds' % iconName,
         'pos': fortIconPos,
         'tips': tips})
        self.mapWidget.addOtherIcons(uiConst.MAP_ICON_OTHER_CLAN_WAR_INCIDENT_FLAG, items)

    def isInNewClanWarTime(sel):
        if gameglobal.rds.configData.get('enableClanWarNoCheck', False):
            return True
        globalStartTime = CCWCD.data.get('globalStartTime')
        globalEndTime = CCWCD.data.get('globalEndTime')
        if globalStartTime and globalEndTime and utils.inCrontabRange(globalStartTime, globalEndTime):
            return False
        for fortId, data in CWFD.data.iteritems():
            startTime = data.get('newStartTime')
            endTime = data.get('newEndTime')
            if startTime and endTime and utils.inCrontabRange(startTime, endTime):
                return True

        return False

    def releasePUBGData(self):
        pass

    def refreshAllPUBGUI(self):
        self.setUIEnabledInPUBG()
        self.setCurPoisonCircle()
        self.setAirPlaneLinePath(self.pubgAirPlanePath)
        self.refreshAllMarksIconInPUBG()
        self.refreshDisasterIconInPUBG()
        self.refreshBossInPubg()
        self.refreshTreasureBoxInPubg()
        self.setBoundAreaInPubg(self.pubgBoundAreaDataInWidget)

    def setUIEnabledInPUBG(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        bgmap = self.mapWidget.bgmap
        if p.isInPUBG():
            self.mapWidget.mySigns.visible = False
            self.mapWidget.npcInfo.visible = False
            self.mapWidget.topSearchArea.visible = True
            self.mapWidget.topSearchArea.broadCastPostion.visible = False
            self.mapWidget.topSearchArea.findNpcBtn.visible = False

    def getRealRadiusInWidget(self, radiusInWorld):
        if radiusInWorld > 0:
            teampRadiusPosXInWidget, teampRadiusPosYInWidget = self.transPos(radiusInWorld, radiusInWorld, self.getCurrentMapName())
            teampZeroPosXInWidget, teampZeroPosYInWidget = self.transPos(0, 0, self.getCurrentMapName())
            if abs(teampRadiusPosXInWidget - teampZeroPosXInWidget) != 0 and abs(teampRadiusPosYInWidget - teampZeroPosYInWidget) != 0:
                curRadiusInWidget = abs(teampRadiusPosXInWidget - teampZeroPosXInWidget)
            else:
                curRadiusInWidget = 0
        else:
            curRadiusInWidget = 0
        return curRadiusInWidget

    def setCurPubgWhiteCircle(self, curSafeAreaPosXInWidget, curSafeAreaPosYInWidget, curSafeAreaRadiusInWidget):

        def pubgWhiteCircleMcDelegateFunc(pubgWhiteCircle):
            circleEdgeNums = DCD.data.get('pubgCircleEdgeNums', 32)
            pubgWhiteCircle.setCircleInfo(circleEdgeNums, 14536119, 0, 14536119, 1, curSafeAreaRadiusInWidget, 2)

        self.createAndSetPubgMc(self.mapWidget.bgmap, 'pubgWhiteCircle', 'com.scaleform.mmo.core.component.RegularPolygon', posX=curSafeAreaPosXInWidget, posY=curSafeAreaPosYInWidget, delegateFunc=pubgWhiteCircleMcDelegateFunc)

    def setCurPubgPoisonCricle(self, curPoisonAreaXInWidget, curPoisonAreaYInWidget, curPoisonAreaRadiusInWidget):
        bgmap = self.mapWidget.bgmap
        pubgPoisonMc = bgmap.getChildByName('pubgPoisonMc')
        if not pubgPoisonMc:
            pubgPoisonMc = self.mapWidget.getInstByClsName('PUBGPoison')
            pubgPoisonMc.name = 'pubgPoisonMc'
            pubgPoisonMc.visible = True
            pubgPoisonMc.blendMode = 'layer'
            pubgPoisonMc.mouseEnabled = False
            pubgPoisonMc.mouseChildren = False
            pubgPoisonMc.x = 0
            pubgPoisonMc.y = 0
            pubgPoisonMc.poisonArea.width = self.getSpaceInfo(self.getCurrentMapName())['spaceAllWidth']
            pubgPoisonMc.poisonArea.height = self.getSpaceInfo(self.getCurrentMapName())['spaceAllWidth']
            bgmap.addChild(pubgPoisonMc)

        def poisonCirclenMcDelegateFunc(poisonCircle):
            circleEdgeNums = DCD.data.get('pubgCircleEdgeNums', 32)
            poisonCircle.setCircleInfo(circleEdgeNums, 14474460, 1, 14474460, 1, curPoisonAreaRadiusInWidget, 1)
            poisonCircle.blendMode = 'erase'

        self.createAndSetPubgMc(pubgPoisonMc, 'poisonCircle', 'com.scaleform.mmo.core.component.RegularPolygon', posX=curPoisonAreaXInWidget, posY=curPoisonAreaYInWidget, width=curPoisonAreaRadiusInWidget * 2, height=curPoisonAreaRadiusInWidget * 2, delegateFunc=poisonCirclenMcDelegateFunc)

    def setCurPoisonCircle(self):
        self.pubgPoisonRefreshHandleCB and BigWorld.cancelCallback(self.pubgPoisonRefreshHandleCB)
        if not self.mapWidget:
            self.pubgPoisonRefreshHandleCB = None
            return
        else:
            self.refreshTreasureBoxInPubg()
            p = BigWorld.player()
            if p.isInPUBG() and p.curPoisonCircleData:
                self.pubgPoisonRefreshHandleCB = BigWorld.callback(pubgUtils.POISON_REFRESH_INTERVAL, self.setCurPoisonCircle)
                nextCenterStage, nextCenterStamp, curCenterPos, nextCenterPos = p.curPoisonCircleData
                curPoisonAreaPos = p.getCurPoisonCirclePos(nextCenterStage, nextCenterStamp, curCenterPos, nextCenterPos)
                curSafeAreaPos = nextCenterPos
                curPoisonAreaRadius = p.getCurPoisonCircleRadius(nextCenterStage, nextCenterStamp)
                curSafeAreaRadius = p.getNextSafeCircleRadius(nextCenterStage)
                curPoisonAreaRadiusInWidget = self.getRealRadiusInWidget(curPoisonAreaRadius)
                curSafeAreaRadiusInWidget = self.getRealRadiusInWidget(curSafeAreaRadius)
                curPoisonAreaXInWidget, curPoisonAreaYInWidget = self.transPos(curPoisonAreaPos[0], curPoisonAreaPos[2], self.getCurrentMapName())
                curSafeAreaPosXInWidget, curSafeAreaPosYInWidget = self.transPos(curSafeAreaPos[0], curSafeAreaPos[2], self.getCurrentMapName())
                self.setCurPubgPoisonCricle(curPoisonAreaXInWidget, curPoisonAreaYInWidget, curPoisonAreaRadiusInWidget)
                self.setCurPubgWhiteCircle(curSafeAreaPosXInWidget, curSafeAreaPosYInWidget, curSafeAreaRadiusInWidget)
            else:
                self.setPubgMcVisible(self.mapWidget.bgmap, 'pubgPoisonMc', False)
                self.setPubgMcVisible(self.mapWidget.bgmap, 'pubgWhiteCircle', False)
            return

    def setAirPlaneLinePath(self, planePath):
        self.pubgAirPlanePath = planePath
        if not self.mapWidget:
            return
        if not self.pubgAirPlanePath:
            if self.pubgAirPlaneStartInWidget:
                del self.pubgAirPlaneStartInWidget[:]
            if self.pubgAirPlaneEndInWidget:
                del self.pubgAirPlaneEndInWidget[:]
        else:
            airPlaneStartPos, airPlaneEndPos = self.pubgAirPlanePath
            self.pubgAirPlaneStartInWidget = list(self.transPos(airPlaneStartPos[0], airPlaneStartPos[2], self.getCurrentMapName()))
            self.pubgAirPlaneEndInWidget = list(self.transPos(airPlaneEndPos[0], airPlaneEndPos[2], self.getCurrentMapName()))
            self.pubgAirlineRotation = (Math.Vector3(airPlaneEndPos) - Math.Vector3(airPlaneStartPos)).yaw / math.pi * 180
            xOffset = abs(float(self.pubgAirPlaneStartInWidget[0] - self.pubgAirPlaneEndInWidget[0]))
            zOffset = abs(float(self.pubgAirPlaneStartInWidget[1] - self.pubgAirPlaneEndInWidget[1]))
            self.pubgAirlineWidth = math.sqrt(xOffset * xOffset + zOffset * zOffset)
        if BigWorld.player().isInPUBG() and self.pubgAirPlanePath:
            self.startSetAirPlaneLine()
        else:
            self.stopSetAirPlaneLine()

    def startSetAirPlaneLine(self):
        self.pubgAirlineHandleCB and BigWorld.cancelCallback(self.pubgAirlineHandleCB)
        self.pubgAirlineHandleCB = None
        if not self.pubgAirPlanePath or not BigWorld.player().isInPUBG():
            return
        else:
            self.setAirPlaneLine(True)
            self.pubgAirlineHandleCB = BigWorld.callback(pubgUtils.AIRPLANE_REFRESH_INTERVAL, self.startSetAirPlaneLine)
            return

    def stopSetAirPlaneLine(self):
        self.pubgAirlineHandleCB and BigWorld.cancelCallback(self.pubgAirlineHandleCB)
        self.pubgAirlineHandleCB = None
        self.setAirPlaneLine(False)

    def setAirPlaneLine(self, isShow):
        if not self.mapWidget:
            return
        bgmap = self.mapWidget.bgmap
        if isShow and self.pubgAirPlanePath:
            airlineAllMc = self.createAndSetPubgMc(bgmap, 'airlineAllMc', 'flash.display.MovieClip', posX=0, posY=0)

            def airlineMcDelegateFunc(airlineMc):
                if airlineMc and airlineMc.dashline:
                    airlineMc.dashline.width = self.pubgAirlineWidth - 10

            self.createAndSetPubgMc(airlineAllMc, 'airline', 'Map_Airline', posX=self.pubgAirPlaneStartInWidget[0], posY=self.pubgAirPlaneStartInWidget[1], rotation=self.pubgAirlineRotation - 90, delegateFunc=airlineMcDelegateFunc)
            self.createAndSetPubgMc(airlineAllMc, 'airlineStartPoint', 'Map_AirlineStartPoint', posX=self.pubgAirPlaneStartInWidget[0], posY=self.pubgAirPlaneStartInWidget[1], rotation=self.pubgAirlineRotation)
            self.createAndSetPubgMc(airlineAllMc, 'airlineEndPoint', 'Map_AirplineArrow', posX=self.pubgAirPlaneEndInWidget[0], posY=self.pubgAirPlaneEndInWidget[1], rotation=self.pubgAirlineRotation)
            airPlanePosInWorld = BigWorld.player().getCurAirPlanePos()
            airPlanePosInWidget = self.transPos(airPlanePosInWorld[0], airPlanePosInWorld[2], self.getCurrentMapName())
            self.createAndSetPubgMc(airlineAllMc, 'airlinePlane', 'Map_AirlinePlane', posX=airPlanePosInWidget[0], posY=airPlanePosInWidget[1], rotation=self.pubgAirlineRotation)
        else:
            self.setPubgMcVisible(bgmap, 'airlineAllMc', False)

    def createAndSetPubgMc(self, parentMc, childName, mcClassName, posX, posY, width = None, height = None, rotation = None, delegateFunc = None, isNewMc = False):
        if not parentMc or not childName:
            return
        else:
            child = parentMc.getChildByName(childName)
            if not child:
                child = self.mapWidget.getInstByClsName(mcClassName)
            elif isNewMc:
                parentMc.removeChild(child)
                child = self.mapWidget.getInstByClsName(mcClassName)
            else:
                self.mapWidget.addChild(child)
            child.visible = True
            child.name = childName
            child.x = posX
            child.y = posY
            if rotation != None:
                child.rotation = rotation
            if width != None:
                child.width = width
            if height != None:
                child.height = height
            delegateFunc and delegateFunc(child)
            parentMc.addChild(child)
            return child

    def setPubgMcVisible(self, parentMc, childName, enabled):
        if parentMc and childName:
            childMc = parentMc.getChildByName(childName)
            if childMc:
                childMc.visible = enabled

    def setPlayerIconInPUBG(self):
        myTeammateNo = BigWorld.player().getMyTeammateNo()
        if not self.mapWidget or not myTeammateNo:
            return
        self.mapWidget.eye.gotoAndStop('PUBGMe%d' % myTeammateNo)

    def setMarksIconInPUBG(self, gbId, xInWorld, zInWorld, spaceNo = None):
        p = BigWorld.player()
        spaceNo = p.spaceNo if not spaceNo else spaceNo
        littleMapNo = gameglobal.rds.ui.littleMap.getLittleMapNoByPos(0, spaceNo)
        p.cell.sendPos(xInWorld, zInWorld, littleMapNo)
        p.setTeammateMapMarkInPUBG(gbId, xInWorld, zInWorld, littleMapNo)

    def refreshAllMarksIconInPUBG(self):
        if not self.mapWidget:
            return
        else:
            p = BigWorld.player()
            mapMarAllkData = list()
            for gbId, teammateMarkData in p.allTeammateMapMark.iteritems():
                posInWorld = teammateMarkData.get('posInWorld', None)
                teammateNo = p.getTeammateNoInPUBG(gbId)
                if teammateNo and posInWorld:
                    xInWidget, yInWidet = self.transPos(posInWorld[0], posInWorld[2], self.getCurrentMapName())
                    mapMarAllkData.append({'x': xInWidget,
                     'y': yInWidet,
                     'teammateNo': teammateNo})

            self.addOtherIns(uiConst.MAP_ICON_BATTLE_PUBG_MARK, mapMarAllkData, True, 'Map_PubgMark')
            return

    def refreshDisasterIconInPUBG(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        mapDisasterData = list()
        if p.curDisasterDataInPUBG:
            xInWidget, yInWidet = self.transPos(p.curDisasterDataInPUBG['posInWorld'][0], p.curDisasterDataInPUBG['posInWorld'][2], self.getCurrentMapName())
            mapDisasterData.append({'x': xInWidget,
             'y': yInWidet,
             'radius': self.getRealRadiusInWidget(DCD.data.get('pubgDestroyDisasterRadius', 0))})
        self.addOtherIns(uiConst.MAP_ICON_BATTLE_PUBG_DISASTER, mapDisasterData, True, 'Map_PubgDisaster')

    def refreshBossInPubg(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        mapBossData = list()
        if p.curBossInPUBG:
            for bossPos in p.curBossInPUBG.itervalues():
                xInWidget, yInWidet = self.transPos(bossPos[0], bossPos[2], self.getCurrentMapName())
                mapBossData.append({'x': xInWidget,
                 'y': yInWidet,
                 'tips': DCD.data.get('pubgBossNameInMap', 'Boss')})

        self.addOtherIns(uiConst.MAP_ICON_BATTLE_PUBG_BOSS, mapBossData, True, 'Map_PubgBoss')

    def refreshTreasureBoxInPubg(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        mapTreasureBoxData = list()
        treasureBoxPosInWorld = p.curTreasureBoxInPUBG.get('posInWorld', [])
        startStamp = DCD.data.get('pubgCreateTreasureBoxInterval', 300) + p.curTreasureBoxInPUBG.get('startStamp', 0) - utils.getNow()
        if treasureBoxPosInWorld and startStamp > 0:
            xInWidget, yInWidet = self.transPos(treasureBoxPosInWorld[0], treasureBoxPosInWorld[2], self.getCurrentMapName())
            mapTreasureBoxData.append({'x': xInWidget,
             'y': yInWidet,
             'tips': DCD.data.get('pubgTreasureBoxNameInMap', gameStrings.TEXT_MAPPROXY_3367),
             'leftTimeStr': utils.formatTimeStr(startStamp, formatStr='m:s', zeroShow=True, sNum=2, mNum=2)})
        self.addOtherIns(uiConst.MAP_ICON_BATTLE_PUBG_TREASURE_BOX, mapTreasureBoxData, True, 'Map_PubgTreasureBox')

    def setBoundAreaInPubg(self, pubgBoundAreaDataInWidget):
        self.pubgBoundAreaDataInWidget = pubgBoundAreaDataInWidget
        if not self.mapWidget:
            return
        else:
            p = BigWorld.player()
            bgmap = self.mapWidget.bgmap
            if not p.isInPUBG():
                self.setPubgMcVisible(bgmap, 'boundLineMc', False)
                return
            mapBounds = MCD.data.get(self.mapInfo.mapId, {}).get('mapBounds', None)
            if mapBounds:
                centerX, centerZ, width, height = utils.getBoundCenterData(mapBounds)
                mapBoundCenterXInWidget, mapBoundCenterYInWidget = self.transPos(centerX, centerZ, self.getCurrentMapName())
                mapBoundWidthInWidget = self.getRealRadiusInWidget(width)
                mapBoundHeightInWidget = self.getRealRadiusInWidget(height)
                self.pubgBoundAreaDataInWidget = [mapBoundCenterXInWidget,
                 mapBoundCenterYInWidget,
                 mapBoundWidthInWidget,
                 mapBoundHeightInWidget]
            if self.pubgBoundAreaDataInWidget:
                boundLineMc = self.createAndSetPubgMc(bgmap, 'boundLineMc', 'flash.display.MovieClip', posX=0, posY=0)
                self.createAndSetPubgMc(boundLineMc, 'mapBound', 'Map_mapBound', posX=self.pubgBoundAreaDataInWidget[0], posY=self.pubgBoundAreaDataInWidget[1], width=self.pubgBoundAreaDataInWidget[2] + 192, height=self.pubgBoundAreaDataInWidget[3] + 192)
                self.createAndSetPubgMc(boundLineMc, 'mapBoundTxt', 'Map_mapBoundTxt', posX=self.pubgBoundAreaDataInWidget[0], posY=self.pubgBoundAreaDataInWidget[1] - self.pubgBoundAreaDataInWidget[3] / 2.0)
            return

    def refreshDoublePlantTreeUI(self):
        if not self.mapWidget:
            return
        p = BigWorld.player()
        bgmap = self.mapWidget.bgmap
        if not p.isInDoublePlantTree():
            self.setPubgMcVisible(bgmap, 'plantTreeAllAreaBoundMc', False)
            return
        areaBoundList = p.getDoublePlantTreeAreaBounds()
        for idx, areaBound in enumerate(areaBoundList):
            if areaBound:
                centerX, centerZ, width, height = utils.getBoundCenterData(areaBound)
                areaBoundCenterXInWidget, areaBoundCenterYInWidget = self.transPos(centerX, centerZ, self.getCurrentMapName())
                areaBoundWidthInWidget = self.getRealRadiusInWidget(width)
                areaBoundHeightInWidget = self.getRealRadiusInWidget(height)
                ptAreaBoundInWidget = [areaBoundCenterXInWidget,
                 areaBoundCenterYInWidget,
                 areaBoundWidthInWidget,
                 areaBoundHeightInWidget]
                if ptAreaBoundInWidget:
                    ptAllAreaBoundMc = self.createAndSetPubgMc(bgmap, 'plantTreeAllAreaBoundMc', 'flash.display.MovieClip', posX=0, posY=0)
                    ASUtils.setHitTestDisable(ptAllAreaBoundMc, True)
                    if self.mapInfo.mapLv == 2:
                        self.createAndSetPubgMc(ptAllAreaBoundMc, 'mapBound%d' % idx, 'Map_Double_Plant_Tree_Area', posX=ptAreaBoundInWidget[0], posY=ptAreaBoundInWidget[1], width=ptAreaBoundInWidget[2] + 50, height=ptAreaBoundInWidget[3] + 50, isNewMc=True)
                        self.createAndSetPubgMc(ptAllAreaBoundMc, 'mapBoundTxt%d' % idx, 'Map_Double_Plant_Tree_Title', posX=ptAreaBoundInWidget[0], posY=ptAreaBoundInWidget[1] - ptAreaBoundInWidget[3] / 2.0 - 5, width=120.0 * (self.mapInfo.mapLv + 1) / 3, height=30 * (self.mapInfo.mapLv + 1) / 3, isNewMc=True)
                    else:
                        self.createAndSetPubgMc(ptAllAreaBoundMc, 'mapBound%d' % idx, 'Map_Double_Plant_Tree_Area_No_Effect', posX=ptAreaBoundInWidget[0], posY=ptAreaBoundInWidget[1], width=ptAreaBoundInWidget[2], height=ptAreaBoundInWidget[3], isNewMc=True)
                        self.createAndSetPubgMc(ptAllAreaBoundMc, 'mapBoundTxt%d' % idx, 'flash.display.MovieClip', posX=0, posY=0, isNewMc=True)

    def refreshGhostMc(self):
        if not self.mapWidget:
            return
        ghostInfos = gameglobal.rds.ui.huntGhost.bigBoxInfo
        ghostData = list()
        for entId, boxInfo in ghostInfos.iteritems():
            bornTime, pos = boxInfo
            existTime = bornTime + HGCD.data.get('BigBoxExistTime', 120) - utils.getNow()
            xInWidget, yInWidet = self.transPos(pos[0], pos[2], self.getCurrentMapName())
            leftTimeStr = utils.formatTimeStr(existTime, formatStr='m:s', zeroShow=True, sNum=2, mNum=2) if existTime > 0 else ''
            ghostData.append({'x': xInWidget,
             'y': yInWidet,
             'tips': HGCD.data.get('ghostNameInMap', ''),
             'leftTimeStr': leftTimeStr,
             'iconHeight': 58})

        self.addOtherIns(uiConst.MAP_ICON_HUNT_GHOST, ghostData, True, 'map_ghost')
        self.ghostRefreshHandleCB = BigWorld.callback(1, self.refreshGhostMc)

    def refreshHuntGhostUI(self):
        self.ghostRefreshHandleCB and BigWorld.cancelCallback(self.ghostRefreshHandleCB)
        if not self.mapWidget:
            self.ghostRefreshHandleCB = None
            return
        else:
            p = BigWorld.player()
            bgmap = self.mapWidget.bgmap
            if not gameglobal.rds.ui.huntGhost.isOpen():
                self.setPubgMcVisible(bgmap, 'huntGhostAllAreaBoundMc', False)
                return
            areaBoundList = gameglobal.rds.ui.huntGhost.getHuntGhostAreaBounds()
            for idx, areaBound in enumerate(areaBoundList):
                if areaBound:
                    centerX, centerZ, width, height = utils.getBoundCenterDataReverse(areaBound)
                    areaBoundCenterXInWidget, areaBoundCenterYInWidget = self.transPos(centerX, centerZ, self.getCurrentMapName())
                    areaBoundWidthInWidget = self.getRealRadiusInWidget(width)
                    areaBoundHeightInWidget = self.getRealRadiusInWidget(height)
                    hgAreaBoundInWidget = [areaBoundCenterXInWidget,
                     areaBoundCenterYInWidget,
                     areaBoundWidthInWidget,
                     areaBoundHeightInWidget]
                    if hgAreaBoundInWidget:
                        hgAllAreaBoundMc = self.createAndSetPubgMc(bgmap, 'huntGhostAllAreaBoundMc', 'flash.display.MovieClip', posX=0, posY=0)
                        ASUtils.setHitTestDisable(hgAllAreaBoundMc, True)
                        self.createAndSetPubgMc(hgAllAreaBoundMc, 'mapBound%d' % idx, 'MapHuntGhost_Area', posX=hgAreaBoundInWidget[0], posY=hgAreaBoundInWidget[1], width=hgAreaBoundInWidget[2] + 50, height=hgAreaBoundInWidget[3] + 50, isNewMc=True)
                        self.createAndSetPubgMc(hgAllAreaBoundMc, 'mapBoundTxt%d' % idx, 'MapHuntGhost_Title', posX=hgAreaBoundInWidget[0], posY=hgAreaBoundInWidget[1] - hgAreaBoundInWidget[3] / 2.0 - 5, width=279.0 * (self.mapInfo.mapLv + 1) / 3, height=82 * (self.mapInfo.mapLv + 1) / 3, isNewMc=True)

            self.refreshGhostMc()
            return


class MapInfo(object):

    def __init__(self, mapId = 0, pos = None):
        self.mapId = mapId
        self.pos = pos
        self.mapLv = MAP_LV_1
        self.mapType = uiConst.MAP_TYPE_NORMAL

    def getMapName(self):
        if MII.data.has_key(self.mapId):
            return MII.data.get(self.mapId).get('mapPath')
        else:
            return MTLD.data.get(self.mapId, {}).get('mapPath', '')

    def getCanScale(self):
        if MII.data.has_key(self.mapId):
            return MII.data.get(self.mapId).get('canScale', False)
        else:
            return MTLD.data.get(self.mapId, {}).get('canScale', False)

    def isThirdLvMap(self):
        return MTLD.data.has_key(self.mapId)

    def hasMapInfo(self):
        return MII.data.has_key(self.mapId) or MTLD.data.has_key(self.mapId)

    def clear(self):
        self.mapId = 0
        self.pos = None
        self.mapLv = 1

    def getCurrentMapSpaceNo(self):
        return MTLD.data.get(self.mapId, {}).get('spaceNo', self.mapId)

    def initMapLv(self, mapLv):
        if self.mapType == uiConst.MAP_TYPE_TRANSPORT and not BigWorld.player().inWingCityOrBornIsland():
            self.mapLv = MAP_LV_0
        elif self.isThirdLvMap():
            self.mapLv = MAP_LV_0
        elif self.getMapName() == 'dgbj':
            self.mapLv = MAP_LV_0
        else:
            self.mapLv = mapLv

    def containsMap(self, thirdLvMapName):
        if not self.isThirdLvMap():
            thirdLvMaps = MII.data.get(self.mapId).get('thirdLvMaps', [])
            for id in thirdLvMaps:
                if thirdLvMapName == MTLD.data.get(id, {}).get('mapPath'):
                    return True

        return False

    def getMapShowName(self):
        if self.isThirdLvMap():
            return MTLD.data.get(self.mapId, {}).get('mapName_ii', '')
        else:
            return MII.data.get(self.mapId, {}).get('mapName_ii', '')
