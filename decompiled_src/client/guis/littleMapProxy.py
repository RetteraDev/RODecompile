#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/littleMapProxy.o
from gamestrings import gameStrings
from collections import Iterable
import BigWorld
import gameglobal
import Math
import keys
import formula
import const
import gametypes
import Transport
import commQuest
import gameChunk
import gameconfigCommon
import utils
import copy
import gamelog
import wingWorldUtils
import pubgUtils
import math
from gamestrings import gameStrings
from Scaleform import GfxValue
from appSetting import Obj as AppSettings
from guis import uiConst
from guis import ui
from guis import cursor
from guis import uiUtils
from ui import gbk2unicode
from guis import events
from uiProxy import UIProxy
from callbackHelper import Functor
from helpers import navigator
import clientUtils
from guis import hotkey as HK
from guis.asObject import ASObject
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import areamap_data as AD
from data import npc_model_client_data as NCD
from data import quest_data as QD
from data import quest_loop_data as QLD
from data import seeker_data as SD
from data import map_func_config_data as MFD
from data import monster_data as MD
from cdata import transport_ref_data as TRD
from data import sys_config_data as SYSD
from data import chunk_mapping_data as CMD
from data import quest_goal_order_data as QGOR
from data import world_area_state_data as WASD
from data import world_area_data as WAD
from data import clan_war_marker_data as CWMD
from data import world_quest_data as WQD
from cdata import quest_loop_inverted_data as QLID
from data import battle_field_data as BFD
from data import battle_field_fort_data as BFFD
from data import play_recomm_activity_data as PRAD
from data import world_war_fort_data as WWFD
from data import world_war_relive_board_data as WWRBD
from data import world_war_config_data as WWCD
from data import zaiju_data as ZJD
from data import map_config_data as MCD
from cdata import quest_marker_group_data as QMGD
from cdata import quest_monster_group_data as QMOGD
from cdata import quest_npc_group_data as QNGD
from data import treasure_box_data as TBD
from data import isolated_creation_data as ICD
from data import fb_entity_data as FED
from data import duel_config_data as DCD
from data import fallen_red_guard_data as FRGD
from data import wing_city_building_data as WCBD
from data import wing_city_building_entity_data as WCBED
from data import chunk_reverse_data as CRD
from data import wing_soul_boss_data as WSBD
from data import wing_world_config_data as WWINGCD
from data import region_server_config_data as RSCD
from data import clan_courier_config_data as CCCD
from data import clan_courier_data as CCD
from data import npc_data as ND
from guis import worldBossHelper
PATH = 'littleMap/'
ICON_PATH = 'map/littleMapIcon/'
ICON_TYPE_PLAYER = 1
ICON_TYPE_NPC_FUNC = 2
ICON_TYPE_MONSTER = 4
ICON_TYPE_TEAMATE = 5
ICON_TYPE_POSITION = 6
ICON_TYPE_SEEK_TARGET = 7
ICON_TYPE_TRANSPORT_STONE = 8
ICON_TYPE_MAP_FUNC = 9
ICON_TYPE_FB_MONSTER = 10
ICON_TYPE_QUEST_ZHUXIAN = 11
ICON_TYPE_QUEST_ZHIXIAN = 12
ICON_TYPE_QUEST_LOOP = 13
ICON_TYPE_QUEST_SPECIAL = 14
ICON_TYPE_ENEMY = 15
ICON_TYPE_MAP_MARK = 16
ICON_TYPE_TRACK_TARGET = 17
ICON_TYPE_AREA_STATE = 18
ICON_TYPE_GUILD_BUILDING = 19
ICON_TYPE_WORLD_QUEST = 20
ICON_TYPE_BFFLAG_INFO = 21
ICON_TYPE_OTHER = 22
ICON_TYPE_HUNT_GIFT = 23
ICON_TYPE_HUNT_PROTECTER = 24
ICON_TYPE_HUNT_SPRITE = 25
ICON_TYPE_HUNT_TRAP = 26
ICON_TYPE_ROB_ZAIJU = 27
ICON_TYPE_ROB_ZAIJU_AREA = 28
ICON_TYPE_HEADER = 29
ICON_TYPE_ASSIST = 30
ICON_TYPE_JIEQI = 31
ICON_TYPE_ZHENCHUAN = 32
ICON_TYPE_PARTNER = 33
ICON_TYPE_DOTA_POSITION = 34
ICON_TYPE_MARRIAGE = 35
ICON_TYPE_WING_WORLD_GROUP_LEADER = 36
ICON_TYPE_WING_WORLD_TEAM_LEADER = 37
ICON_TYPE_WING_WORLD_BUILDING = 38
ICON_TYPE_WING_WORLD_ZAIJU = 39
ICON_TYPE_WING_WORLD_AIR_ZAIJU = 40
ICON_TYPE_WING_WORLD_EVENT_EFFECT = 41
ICON_TYPE_WING_WORLD_HOST_NAME = 42
ICON_TYPE_PUBG_TEAMMATE_MARK = 43
ICON_TYPE_WING_WORLD_BUILDING_DIC = {gametypes.WING_CITY_BUILDING_TYPE_STONE: 'LittleMap_WingWorldStone',
 gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD: 'LitttleMap_WingWorldReliveBoard',
 gametypes.WING_CITY_BUILDING_TYPE_AIR_STONE: 'Littlemap_WingWorldAirStone',
 gametypes.WING_CITY_BUILDING_TYPE_GATE: 'LittleMap_WingWorldGate',
 gametypes.WING_CITY_BUILDING_TYPE_WALL: 'LittleMap_WingWorldWall',
 gametypes.WING_CITY_BUILDING_TYPE_MAIN_HALL: 'LittleMap_WingWorldMainHall',
 gametypes.WING_CITY_BUILDING_TYPE_WAREHOUSE: 'LittleMap_WingWorldInventory'}
ICON_TYPE_WING_WORLD_DICT = {ICON_TYPE_WING_WORLD_GROUP_LEADER: 'LittleMap_WingWorldGroupLeader',
 ICON_TYPE_WING_WORLD_TEAM_LEADER: 'LittleMap_WingWorldTeamLeader',
 ICON_TYPE_WING_WORLD_ZAIJU: 'LittleMap_WingWorldZaiju',
 ICON_TYPE_WING_WORLD_AIR_ZAIJU: 'LittleMap_WingWorldAirZaiju'}
ICON_TYPE_HUNT_DICT = {ICON_TYPE_HUNT_GIFT: 'LittleMap_Gift',
 ICON_TYPE_HUNT_PROTECTER: 'LittleMap_Protecter',
 ICON_TYPE_HUNT_SPRITE: 'LittleMap_Sprite',
 ICON_TYPE_HUNT_TRAP: 'LittleMap_Trap'}
WORLD_MAP_ID = 9999
TRACK_TARGET_CLEAR_TIME = 5
completeResArr = SYSD.data.get('littmapQuest', {}).get('complete', ())
unfinishedResArr = SYSD.data.get('littmapQuest', {}).get('unfinished', ())
availableResArr = SYSD.data.get('littmapQuest', {}).get('available', ())
chatResArr = SYSD.data.get('littmapQuest', {}).get('chat', ['ltchatunfinished1'] * 9)
cltItemResArr = SYSD.data.get('littmapQuest', {}).get('cltItem', ['ltComCltItemunfinished1'] * 9)
monsterResArr = SYSD.data.get('littmapQuest', {}).get('monster', ['ltMonsterunfinished1'] * 9)
markNpcArr = SYSD.data.get('littmapQuest', {}).get('markNpc', ['ltMarkNpcunfinished1'] * 9)
ltNeedshowTypes = SYSD.data.get('ltNeedshowTypes', [])
farestAlpha = SYSD.data.get('ltFarestAlpha', 0.5)
colItemTypeRes = {1: cltItemResArr,
 2: monsterResArr}
defaultW = SYSD.data.get('defaultLtWidth', 250)
defaultH = SYSD.data.get('defaultLtHeight', 250)
ltShowIconOffset = SYSD.data.get('ltShowIconOffset', defaultW / 2)
NPC_POS_UNIT_NUM = 100
NPC_POS_UNIT_REFRESH_TIME = 0.05
NPC_POS_NO_REFRESH = -1
FB_ENTITY_TYPE_MONSTER = 'monster'
FB_ENTITY_TYPE_TREASURE_BOX = 'treasureBox'
FB_ENTITY_TYPE_ALONE_CREATION = 'iIsolatedCreation'
KEY_BTN_NAME_MAP = {HK.KEY_DOTA_MAP_MARK: 'markBtn',
 HK.KEY_DOTA_MAP_ATK: 'attackBtn',
 HK.KEY_DOTA_MAP_RETREAT: 'retreatBtn',
 HK.KEY_DOTA_MAP_GATHER: 'gatherBtn'}
CAN_OCCUPY_BUILDING_COLOR = ('#99ebff', '#99ff9e', '#fd99ff')

class LittleMapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LittleMapProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickIcon': self.onClickIcon,
         'getMapInfo': self.onGetMapInfo,
         'initDone': self.onInitDone,
         'startSendPos': self.onStartSendPos,
         'endSendPos': self.onEndSendPos,
         'sendPos': self.onSendPos,
         'mapIdChanged': self.onMapIdChanged,
         'getHeroMapId': self.onGetHeroMapId,
         'isPlayerInMap': self.onIsPlayerInMap,
         'cancelTrans': self.onCancelTrans,
         'transToStone': self.onTransToStone,
         'getBindCash': self.onGetBindCash,
         'saveInfo': self.onSaveInfo,
         'getInfo': self.onGetInfo,
         'getAreaStateInfo': self.onGetAreaStateInfo,
         'isBFHunt': self.onIsBFHunt,
         'bfDotaButtonClick': self.onBfDotaButtonClick,
         'isInBfDota': self.onIsInBfDota,
         'isInPUBG': self.onIsInPUBG,
         'getMapNameTip': self.onGetMapNameTip,
         'isInWingWorldCityWar': self.onIsInWingWorldCityWar,
         'transPos': self.onTransPos,
         'endSetMapLv': self.onEndSetMapLv}
        self.curMapNo = None
        self.curViewMapNo = None
        self.posData = None
        self.callbackHandler = None
        self.mapMed = None
        self.posInfoMed = None
        self.stoneId = 0
        self.destId = 0
        self.availableDest = []
        self.curMapLvl = None
        self.teamArr = []
        self.npcInfo = None
        self.refreshNpcCallBack = None
        self.addNpcCallBack = None
        self.confirmBoxId = None
        self.pathPoints = []
        self.monsterInCombat = {}
        self.trackTargetCallback = None
        self.npcDataInfo = {}
        self.transportStones = {}
        self.areaStateInfo = None
        self.lastChunkName = None
        self.npcPosUnit = None
        self.refUnitCallBack = None
        self.lastQuestInfo = {}
        self.clearPathCallBack = None
        self.gfxNpcDatas = {}
        self.refreshGfxNpcDataTypes = []
        self.blendEnable = False
        self.mapSpaceIdDict = {}
        self.oldHpInfo = {}
        self.otherItem = {}
        self.bfHuntIcons = {ICON_TYPE_HUNT_GIFT: {},
         ICON_TYPE_HUNT_PROTECTER: {},
         ICON_TYPE_HUNT_SPRITE: {},
         ICON_TYPE_HUNT_TRAP: {}}
        self.filterQuests = []
        self.filterLoopQuests = []
        self.seekGfxDatas = {}
        self.isSendPosState = False
        self.signalType = uiConst.SIGNAL_TYPE_NULL
        self.lastBfDotaBtnTime = 0
        self.bfDotaBtnTimer = 0
        self.wingWorldEventTimer = 0
        self.debugPosX = None
        self.debugPosY = None
        self.isLogPos = False
        self.pubgPoisonTimeRefreshHandleCB = None
        self.pubgPoisonRefreshHandleCB = None
        self.pubgAirlineHandleCB = None
        self.pubgAirPlanePath = None
        self.pubgAirlineRotation = None
        self.pubgAirlineWidth = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LITTLE_MAP:
            self.mapMed = mediator
            self.drawPathTrace(self.pathPoints, False)
            BigWorld.player().cell.fetchAreaStates()
            iconLayers = SYSD.data.get('littleMapIconLayers', ())
            if BigWorld.player().isInBfDota() and gameglobal.rds.configData.get('enableBfDotaMapMark', False):
                fun = Functor(self.showBfDotaBtns, 300, 20)
                BigWorld.callback(0, fun)
            return uiUtils.array2GfxAarry([ltNeedshowTypes,
             ltShowIconOffset,
             farestAlpha,
             iconLayers])

    def show(self, *args):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LITTLE_MAP)

    def _asWidgetClose(self, widgetId, multiID):
        self.hide()

    def reset(self):
        if self.callbackHandler:
            BigWorld.cancelCallback(self.callbackHandler)
        if self.refreshNpcCallBack:
            BigWorld.cancelCallback(self.refreshNpcCallBack)
        if self.trackTargetCallback:
            BigWorld.cancelCallback(self.trackTargetCallback)
        if self.clearPathCallBack:
            BigWorld.cancelCallback(self.clearPathCallBack)
        self.curMapNo = None
        self.curViewMapNo = None
        self.posData = None
        self.callbackHandler = None
        self.refreshNpcCallBack = None
        self.trackTargetCallback = None
        self.clearPathCallBack = None
        self.mapMed = None
        self.posInfoMed = None
        self.stoneId = 0
        self.destId = 0
        self.availableDest = []
        self.curMapLvl = None
        self.teamArr = []
        self.npcInfo = None
        self.confirmBoxId = None
        self.mapHeightRange = None
        self.monsterInCombat = {}
        self.transportStones = {}
        self.areaStateInfo = None
        self.lastChunkName = None
        self.refUnitCallBack = None
        self.npcPosUnit = None
        self.gfxNpcDatas = {}
        self._stopRefreshNpcPosUnit()
        self.blendEnable = True
        self.bfHuntIcons = {ICON_TYPE_HUNT_GIFT: {},
         ICON_TYPE_HUNT_PROTECTER: {},
         ICON_TYPE_HUNT_SPRITE: {},
         ICON_TYPE_HUNT_TRAP: {}}

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LITTLE_MAP)

    def changeToBfDotaMode(self, enable):
        if self.mapMed:
            self.mapMed.Invoke('setMapGreybgVisible', GfxValue(not enable))
            self.mapMed.Invoke('setBtnsCanShow', GfxValue(not enable))

    def setMapPosByMouse(self):
        if not self.mapMed:
            return
        med = ASObject(self.mapMed)
        self.debugPosX, self.debugPosY = med.iconCanvas.mouseX, med.iconCanvas.mouseY

    def onClickIcon(self, *arg):
        iconType = int(arg[3][0].GetMember('type').GetNumber())
        iconData = uiUtils.gfxArray2Array(arg[3][0].GetMember('data'))
        if BigWorld.player().isInBfDota() and self.isSendPosState:
            if iconType == ICON_TYPE_TEAMATE:
                self.signalType = uiConst.SIGNAL_TYPE_GATHER
            elif iconType == ICON_TYPE_ENEMY:
                self.signalType = uiConst.SIGNAL_TYPE_ATK
            elif iconType == ICON_TYPE_OTHER:
                if len(iconData) >= 2:
                    self.signalType = uiConst.SIGNAL_TYPE_GATHER if iconData[1].GetBool() else uiConst.SIGNAL_TYPE_ATK
            self.mapMed.Invoke('handleSendPos')
            return
        else:
            if iconType in (ICON_TYPE_NPC_FUNC,
             ICON_TYPE_QUEST_LOOP,
             ICON_TYPE_QUEST_SPECIAL,
             ICON_TYPE_QUEST_ZHIXIAN,
             ICON_TYPE_QUEST_ZHUXIAN) or iconType == ICON_TYPE_TRANSPORT_STONE and not self.stoneId:
                seekId = str(iconData[4].GetNumber())
                uiUtils.findPosById(seekId)
            elif iconType == ICON_TYPE_TRANSPORT_STONE and self.stoneId:
                self.destId = iconData[3].GetNumber()
                if self.destId in self.availableDest:
                    stone = BigWorld.entity(self.stoneId)
                    if stone:
                        stone.showConfirm(self.destId)
            elif iconType == ICON_TYPE_TEAMATE:
                pos = iconData[4]
                spaceNo = iconData[5].GetString()
                navigator.getNav().pathFinding((pos.GetElement(0).GetNumber(),
                 pos.GetElement(1).GetNumber(),
                 pos.GetElement(2).GetNumber(),
                 int(spaceNo)), None, None, True, 0.5)
            elif iconType == ICON_TYPE_WING_WORLD_BUILDING:
                if len(iconData) >= 3 and iconData[1]:
                    gamelog.info('jbx:cell.wingWorldWarTeleportToOwnerReliveBoard', int(iconData[2].GetNumber()))
                    BigWorld.player().cell.wingWorldWarTeleportToOwnerReliveBoard(int(iconData[2].GetNumber()))
            else:
                pos = arg[3][0].GetMember('pos')
                if pos:
                    BigWorld.player().pathFindingTo((pos.GetElement(0).GetNumber(), pos.GetElement(1).GetNumber(), pos.GetElement(2).GetNumber()), int(BigWorld.player().spaceNo))
            return

    def onGetMapInfo(self, *args):
        mapNo = int(args[3][0].GetString())
        mapPath, posData, mapNo, thirdLvScale = self.getMapInfo(mapNo)
        info = {}
        p = BigWorld.player()
        if posData:
            mapSize = AD.data.get(mapNo, {}).get('mapShowSize', None)
            info = {'posData': [mapPath,
                         posData,
                         mapNo,
                         thirdLvScale],
             'canDrag': not bool(mapSize)}
            if mapSize:
                info['mapSize'] = mapSize
            else:
                key = keys.SET_UI_INFO + '/littleMap/'
                info['mapSize'] = [AppSettings.get(key + 'width', defaultW), AppSettings.get(key + 'height', defaultH)]
            info['needShowEdageEffect'] = not formula.inBattleField(p.mapID)
        return uiUtils.dict2GfxDict(info, True)

    def onInitDone(self, *args):
        if not self.blendEnable:
            self.mapMed.Invoke('enableMapBlend', GfxValue(self.blendEnable))
            self.blendEnable = True
        self.setVisible(gameglobal.rds.ui.map.littleMapState)
        self.callbackHandler = BigWorld.callback(0.5, self.uiAdapter.refreshPlayerPos)
        self.refreshNpcPos()

    def littleMapStateChanged(self):
        chunkName = BigWorld.ChunkInfoAt(BigWorld.player().position)
        mapNo = self.getMapName(chunkName, BigWorld.player().spaceNo, BigWorld.player().position[1])
        if mapNo and gameglobal.rds.ui.map.littleMapState:
            self.setVisible(True)
        else:
            self.setVisible(False)

    def onStartSendPos(self, *args):
        self.isSendPosState = True
        if ui.get_cursor_state() == ui.NORMAL_STATE:
            ui.set_cursor_state(ui.LITTLE_MAP_SEND_POS)
            ui.set_cursor(cursor.littlemap_sendpos)
            ui.lock_cursor()

    def onEndSendPos(self, *args):
        self.isSendPosState = False
        if ui.get_cursor_state() == ui.LITTLE_MAP_SEND_POS:
            ui.reset_cursor()

    def onMapIdChanged(self, *args):
        self.curViewMapNo = args[3][0].GetNumber()
        self.npcDataInfo = None
        self.posData = AD.data.get(self.curViewMapNo, {}).get('posData')
        self.mapHeightRange = AD.data.get(self.curViewMapNo, {}).get('height', None)
        self.clearPathTrace()
        self._stopRefreshNpcPosUnit()
        self.refreshNpcPos(self.npcInfo)
        self.showTeamMate(self.teamArr)
        self.showEnemyPlayer({})
        self.showMapFuncBtns()
        self.showFBEntityIcon([])
        self.showMapMark()
        self.showGuildBuilding()
        self.showWorldQuest()
        self.showBfFlagInfo()
        self.showOtherItems()
        self.showBFHuntInfo()
        self.addWWBattleIcon()
        self.addWWReliveIcon()
        self.refreshMapRotation()
        self.addWWRBattleIcon()
        self.addRobZaiju()
        self.refreshGuildRobberNpcInfo()
        if formula.inDotaBattleField(BigWorld.player().mapID):
            self.onPlayerEnterDotaZaiju()
        self.refreshBattleFiledEntity()
        self.showWingWorldWarInfo()
        self.showBattleFortCrystalIcon()
        self.showBattleFortZaijuIcon()
        self.showBattleFortMonsterIcon()
        self.addBattleCqzzOtherIcons()
        p = BigWorld.player()
        p.base.getSoulBossStateInfoEx(p.getWingCityId())
        self.addClanWarYaBiao()
        self.refreshWorldBossIcon()
        self.refreshAllPUBGUI()

    def onGetHeroMapId(self, *args):
        return GfxValue(self.curMapNo if self.curMapNo else -1000)

    def onIsPlayerInMap(self, *args):
        return GfxValue(bool(BigWorld.player() and self.isTargetNeedShow(self.curMapNo, BigWorld.player().position[1])))

    def onCancelTrans(self, *args):
        self.unShowTransportDest()

    @ui.callFilter(1, False)
    def onTransToStone(self, *args):
        destId = args[3][0].GetNumber()
        BigWorld.player().cell.teleportToStone(destId)

    def onGetBindCash(self, *args):
        return GfxValue(BigWorld.player().bindCash + BigWorld.player().cash)

    def onSaveInfo(self, *args):
        hide = int(args[3][0].GetBool())
        width = int(args[3][1].GetNumber())
        height = int(args[3][2].GetNumber())
        key = keys.SET_UI_INFO + '/littleMap/'
        AppSettings[key + 'hide'] = hide
        AppSettings[key + 'width'] = width
        AppSettings[key + 'height'] = height

    def onGetInfo(self, *args):
        key = keys.SET_UI_INFO + '/littleMap/'
        info = {}
        info['hide'] = AppSettings.get(key + 'hide', 0)
        info['width'] = AppSettings.get(key + 'width', defaultW)
        info['height'] = AppSettings.get(key + 'height', defaultH)
        return uiUtils.dict2GfxDict(info)

    @ui.callFilter(5, False)
    def onGetAreaStateInfo(self, *args):
        BigWorld.player().cell.fetchAreaStates()

    def onIsBFHunt(self, *args):
        isBfHunt = formula.inHuntBattleField(BigWorld.player().mapID)
        return GfxValue(isBfHunt)

    def onSendPos(self, *args):
        posX = args[3][0].GetNumber()
        posZ = args[3][1].GetNumber()
        self.doSendPos(posX, posZ)

    def doSendPos(self, posX, posZ):
        p = BigWorld.player()
        if p.isInBfDota():
            gcd = DCD.data.get('bfDotaBtnGcd', 5)
            if utils.getNow() - self.lastBfDotaBtnTime < gcd:
                return
            self.lastBfDotaBtnTime = utils.getNow()
            p.cell.markDoneLittleMapInBFDota(self.signalType, (posX, 0, posZ))
        else:
            p.cell.sendPos(posX, posZ, self.curMapNo)
        self.onEndSendPos()
        if not p.isInBfDota() and not p.isInPUBG():
            self.showPosition((posX, 0, posZ))
        gameglobal.rds.sound.playSound(gameglobal.SD_409)

    def showMonsterPoint(self, x, y):
        if self.mapMed:
            self.mapMed.Invoke('showMonsterPoint', self.itemDataToGfx(MapItemData(ICON_TYPE_MONSTER, x, y, ['ltMonsterPoint'])))

    def setVisible(self, visible):
        if self.mapMed:
            self.mapMed.Invoke('setVisible', GfxValue(visible))
            if visible:
                self.refreshActive()

    def enableMapBlend(self, enable):
        if enable != self.blendEnable:
            self.blendEnable = enable
            if self.mapMed:
                self.mapMed.Invoke('enableMapBlend', GfxValue(enable))

    def getMapName(self, chunkName, spaceNo, posY):
        spaceId = uiUtils.getConfigSpaceNoCheckFbCopy(spaceNo)
        if not self.mapSpaceIdDict:
            for mapId, item in AD.data.items():
                mapSpaceId = item.get('spaceId')
                if mapSpaceId:
                    self.mapSpaceIdDict.setdefault(mapSpaceId, []).append(mapId)

        mapIds = self.mapSpaceIdDict.get(spaceId, [])
        if mapIds:
            for mapId in mapIds:
                item = AD.data.get(mapId, {})
                chunkList = item.get('chunkList')
                if chunkList == None:
                    continue
                if chunkName in chunkList and spaceId == item.get('spaceId'):
                    mapHeight = item.get('height', None)
                    if not mapHeight or mapHeight[0] <= posY and mapHeight[1] >= posY:
                        return mapId

    def getMapNoBySpaceNo(self, spaceNo, posY):
        spaceId = uiUtils.getConfigSpaceNoCheckFbCopy(spaceNo)
        for mapId, item in AD.data.items():
            if spaceId == item.get('spaceId'):
                mapHeight = item.get('height', None)
                if not mapHeight or mapHeight[0] <= posY and mapHeight[1] >= posY:
                    return mapId

    def getMapNameByNo(self, mapNo):
        if mapNo:
            data = AD.data.get(int(mapNo))
            if data == None:
                return
            return data.get('res')
        else:
            return

    def setPlayerPos(self, x, y, yaw):
        gameglobal.rds.ui.topBar.refreshPlayerMapInfo()
        if self.mapMed:
            p = BigWorld.player()
            if p.isInBfDota() and isinstance(BigWorld.camera(), BigWorld.TrackCamera):
                if self.isMapShow():
                    self.setVisible(False)
                return
            chunkName = BigWorld.ChunkInfoAt(BigWorld.player().position)
            if self.lastChunkName != chunkName and self.areaStateInfo:
                self.lastChunkName = chunkName
                self.showAreaInfo(self.areaStateInfo, True)
                self.showWorldQuest()
            mapNo = self.getMapName(chunkName, BigWorld.player().spaceNo, BigWorld.player().position[1])
            if mapNo == None and self.isMapShow():
                self.curMapNo = None
                self.curViewMapNo = None
                self.posData = None
                self.mapHeightRange = None
                self._stopRefreshNpcPosUnit()
                self.setVisible(False)
                if self.mapMed:
                    self.mapMed.Invoke('setMapNone')
                return
            if mapNo and not self.isMapShow():
                if not gameglobal.rds.ui.isHideAllUI() and gameglobal.rds.ui.map.littleMapState:
                    self.setVisible(True)
            if self.curMapNo != mapNo and mapNo != None:
                self.curMapNo = mapNo
                if self.curMapNo:
                    self.mapMed.Invoke('setMap', GfxValue(self.curMapNo))
        else:
            p = BigWorld.player()
            if utils.instanceof(p, 'PlayerAvatar') and p.isInBfDota() and not isinstance(BigWorld.camera(), BigWorld.TrackCamera):
                self.show()

    def getMapInfo(self, mapNo = -1):
        mapNo = int(mapNo)
        mapPath = ''
        posData = None
        thirdLvScale = []
        if mapNo == -1:
            mapNo = self.curMapNo
        mapData = AD.data.get(mapNo, None)
        if mapData:
            posData = mapData.get('posData')
            thirdLvScale = mapData.get('thirdLvScale', [])
            if not isinstance(thirdLvScale, tuple):
                thirdLvScale = tuple(thirdLvScale)
        mapName = self.getMapNameByNo(mapNo)
        if mapName:
            mapPath = PATH + mapName
        return (mapPath,
         posData,
         mapNo,
         thirdLvScale)

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
            if qld and len(qld['quests']) > 0:
                firstQuestId = qld['quests'][0]
                if isinstance(firstQuestId, tuple):
                    firstQuestId = firstQuestId[0]
        else:
            firstQuestId = quest
        return firstQuestId

    def isGoalComplete(self, seekId, info):
        return gameglobal.rds.ui.questTrack.isGoalComplete(seekId)

    def getSeekTitleName(self, iType, item):
        if iType.lower() == 'npc':
            npcId = item.get('npcId', 0)
            name, title = uiUtils.getNpcNameAndTitle(npcId)
        else:
            name = item.get('name', '')
            title = item.get('title', '')
        return (name, title)

    def checkSeekData(self, seekderData):
        serverConfigId = seekderData.get('serverConfigId')
        if serverConfigId and not uiUtils.needShowByServer(serverConfigId):
            return False
        npcId = seekderData.get('npcId', 0)
        if npcId and not ND.data.get(npcId, {}).get('enable', 1):
            return False
        return True

    def getSeekIds(self):
        p = BigWorld.player()
        spaceNo = p.mapID
        ret = []
        for key, item in CRD.data.iteritems():
            if key[0] == spaceNo:
                for info in item:
                    npcId = info.get('npcList', 0)
                    if SD.data.get(npcId, {}).get('isInMap', 0) or SD.data.get(npcId, {}).get('isInTransMap', 0):
                        ret.append(npcId)

        return ret

    def getNpcData(self, info = None, onlyAccepted = False):
        p = BigWorld.player()
        if not self.mapMed:
            return
        else:
            tmpCurViewMapNo = self.mapMed.Invoke('getCurrentMapId').GetNumber()
            if tmpCurViewMapNo == WORLD_MAP_ID:
                self.curViewMapNo = tmpCurViewMapNo
                return
            npcDataInfo = self.getQuestNpcInfo(info, onlyAccepted=onlyAccepted)
            if npcDataInfo == self.npcDataInfo and tmpCurViewMapNo == self.curViewMapNo:
                return NPC_POS_NO_REFRESH
            self.npcDataInfo = npcDataInfo
            self.curViewMapNo = tmpCurViewMapNo
            data = []
            dt = npcDataInfo.get('debateNpcTks', {})
            it = npcDataInfo.get('comCltItems', {})
            nt = npcDataInfo.get('needMonsters', {})
            bt = npcDataInfo.get('beatMonsters', {})
            mt = npcDataInfo.get('markNpcs', {})
            cltItemTypes = npcDataInfo.get('cltItemTypes', {})
            complete = npcDataInfo.get('complete', {})
            unfinished = npcDataInfo.get('unfinished')
            available = npcDataInfo.get('available')
            mapData = AD.data.get(self.curViewMapNo, {})
            if not mapData:
                return data
            seekIds = AD.data.get(self.curViewMapNo, {}).get('seekId', [])
            if not seekIds and not p.inWingCityOrBornIsland():
                return data
            allQuestSeekIds = dt.keys() + it.keys() + nt.keys() + bt.keys() + mt.keys()
            notifyList = BigWorld.player().clientPersistentNotifyList.get(gametypes.CLIENT_PERSISTENT_NOTIFY_MAP, [])
            for seekId in list(mapData.get('port', [])) + notifyList:
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z = item['xpos'], item['zpos']
                iType = item.get('type', '')
                if iType not in ('DiGongPort', 'FubenPort', 'transport'):
                    continue
                iconType = 'ltcommon'
                if iType == 'DiGongPort':
                    iconType = 'ltDiGongPort'
                elif iType == 'FubenPort':
                    iconType = 'ltFubenPort'
                else:
                    iconType = 'ltcommon'
                name, title = self.getSeekTitleName(iType, item)
                data.append(MapItemData(ICON_TYPE_NPC_FUNC, x, z, (iconType,
                 name,
                 title,
                 '',
                 seekId)))

            if p.inWingCityOrBornIsland():
                transStoneList = self.getSeekIds()
            else:
                transStoneList = mapData.get('transportStone', [])
            for seekId in list(transStoneList) + notifyList:
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                if iType not in ('transportStone',):
                    continue
                name, title = self.getSeekTitleName(iType, item)
                npcId = item.get('npcId', 0)
                iconType = 'ltTranstone' if Transport.isActiveStone(npcId) else 'ltUnActiveSend'
                data.append(MapItemData(ICON_TYPE_TRANSPORT_STONE, x, z, (iconType,
                 name,
                 title,
                 npcId,
                 seekId,
                 Transport.isActiveStone(npcId),
                 self.getTransCashBySeekId(seekId))))
                transId = TRD.data.get(npcId, {}).get('destId')
                if transId:
                    self.transportStones.setdefault(transId, []).append(seekId)

            for seekId in nt.keys():
                if seekId not in seekIds:
                    continue
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                name, title = self.getSeekTitleName(iType, item)
                trackIndex = gameglobal.rds.ui.map.getTrackIndex(nt[seekId][2])
                radii = QD.data.get(nt[seekId][2], {}).get('needMonsterRadii', 0)
                data.append(MapItemData(self.getIconByQuestType(nt[seekId][1]), x, z, (monsterResArr[nt[seekId][1] - 1],
                 name,
                 title,
                 nt[seekId][0],
                 seekId), trackIndex=trackIndex, radii=radii))

            for seekId in bt.keys():
                if seekId not in seekIds:
                    continue
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                name, title = self.getSeekTitleName(iType, item)
                trackIndex = gameglobal.rds.ui.map.getTrackIndex(bt[seekId][2])
                name, title = self.getSeekTitleName(iType, item)
                radii = QD.data.get(bt[seekId][2], {}).get('beatMonsterRadii', 0)
                data.append(MapItemData(self.getIconByQuestType(bt[seekId][1]), x, z, (monsterResArr[bt[seekId][1] - 1],
                 name,
                 title,
                 bt[seekId][0],
                 seekId), trackIndex=trackIndex, radii=radii))

            for seekId in it.keys():
                if seekId not in seekIds:
                    continue
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                radii = QD.data.get(it[seekId][2], {}).get('CltItemRadii', 0)
                trackIndex = gameglobal.rds.ui.map.getTrackIndex(it[seekId][2])
                iconRes = cltItemResArr
                if cltItemTypes.has_key(seekId):
                    iconRes = colItemTypeRes.get(cltItemTypes[seekId], iconRes)
                name, title = self.getSeekTitleName(iType, item)
                data.append(MapItemData(self.getIconByQuestType(it[seekId][1]), x, z, (iconRes[it[seekId][1] - 1],
                 name,
                 title,
                 it[seekId][0],
                 seekId), trackIndex=trackIndex, radii=radii))

            for seekId in dt.keys():
                if seekId not in seekIds:
                    continue
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                trackIndex = gameglobal.rds.ui.map.getTrackIndex(dt[seekId][2])
                name, title = self.getSeekTitleName(iType, item)
                data.append(MapItemData(self.getIconByQuestType(dt[seekId][1]), x, z, (chatResArr[dt[seekId][1] - 1],
                 name,
                 title,
                 dt[seekId][0],
                 seekId), trackIndex=trackIndex))

            for seekId in mt.keys():
                if seekId not in seekIds:
                    continue
                item = SD.data.get(seekId, {})
                if not self.checkSeekData(item):
                    continue
                x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                trackIndex = gameglobal.rds.ui.map.getTrackIndex(mt[seekId][2])
                name, title = self.getSeekTitleName(iType, item)
                data.append(MapItemData(self.getIconByQuestType(mt[seekId][1]), x, z, (markNpcArr[mt[seekId][1] - 1],
                 name,
                 title,
                 mt[seekId][0],
                 seekId), trackIndex=trackIndex))

            npcSeekDatas = mapData.get('npcSeekId', {})
            if npcSeekDatas:
                questInfo = ((complete, completeResArr), (available, availableResArr), (unfinished, unfinishedResArr))
                for questNpc, questRes in questInfo:
                    for npcId in questNpc:
                        npcSeekIds = npcSeekDatas.get(npcId, [])
                        allQuestSeekIds.extend(npcSeekIds)
                        for seekId in npcSeekIds:
                            if seekId not in seekIds:
                                continue
                            qType, questId = gameglobal.rds.ui.map.getIconByQuestTypes(questNpc.get(npcId))
                            if questNpc == unfinished and QD.data.get(questId, {}).get('hideUnfinishIcon', 1):
                                continue
                            item = SD.data.get(seekId, {})
                            if not self.checkSeekData(item):
                                continue
                            x, z, iType = item['xpos'], item['zpos'], item.get('type', '')
                            iconTtype = self.getIconByQuestType(qType)
                            npcType = questRes[int(qType) - 1]
                            trackIndex = gameglobal.rds.ui.map.getTrackIndex(questId)
                            name, title = self.getSeekTitleName(iType, item)
                            data.append(MapItemData(iconTtype, x, z, (npcType,
                             name,
                             title,
                             '',
                             seekId), trackIndex=trackIndex))

            enableWorldPlayActivity = gameglobal.rds.configData.get('enableWorldPlayActivity', False)
            if p.inWingCityOrBornIsland():
                npcList = self.getSeekIds()
            else:
                npcList = mapData.get('npc', [])
            for seekId in list(npcList) + notifyList:
                if seekId in allQuestSeekIds:
                    continue
                if self.seekGfxDatas.has_key(seekId):
                    data.insert(0, self.seekGfxDatas[seekId])
                    continue
                item = SD.data.get(seekId, {})
                iType = item.get('type', '')
                if not self.checkSeekData(item):
                    continue
                if iType.lower() not in ('npc', 'recommactivity'):
                    continue
                if iType.lower() == 'npc':
                    npcId = item.get('npcId', 0)
                    ndata = NCD.data.get(npcId)
                    if ndata == None:
                        continue
                    if ndata.get('isInRobOldSpace', 0):
                        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                            continue
                    x, z = item['xpos'], item['zpos']
                    icon = ndata.get('topIcon', 'common')
                    if uiUtils.checkTopIconValid(icon):
                        iconType = ICON_TYPE_NPC_FUNC
                        name, title = self.getSeekTitleName(iType, item)
                        gfxItemData = MapItemData(iconType, x, z, ('lt' + icon,
                         name,
                         title,
                         '',
                         seekId)).toGfxData()
                        data.insert(0, gfxItemData)
                        self.seekGfxDatas[seekId] = gfxItemData
                elif iType.lower() == 'recommactivity' and enableWorldPlayActivity:
                    activityId = item.get('npcId', 0)
                    activityData = PRAD.data.get(activityId, {})
                    if activityId:
                        mapIcon = activityData.get('mapIcon', '')
                        if mapIcon:
                            x, z = item['xpos'], item['zpos']
                            name = activityData.get('name', '')
                            iconPath = ICON_PATH + 'recommActivity/%s.dds' % mapIcon
                            gfxItemData = MapItemData(ICON_TYPE_NPC_FUNC, x, z, (iconPath,
                             name,
                             '',
                             '',
                             seekId)).toGfxData()
                            data.insert(0, gfxItemData)
                            self.seekGfxDatas[seekId] = gfxItemData

            return data

    def needQuestShowByLv(self, qData, questIgnoreLv):
        if not qData:
            return False
        playerLv = BigWorld.player().lv
        questMinShowLv, questMaxShowLv = qData.get('displayLv', [-1, -1])
        if questMinShowLv > 0 and questMaxShowLv > 0:
            if playerLv < questMinShowLv or playerLv > questMaxShowLv:
                return False
        elif playerLv - qData.get('recLv', 0) >= questIgnoreLv and not gameglobal.LOW_LV_QUEST_MAP:
            return False
        return True

    def getQuestNpcInfo(self, info = None, isMap = False, onlyAccepted = False):

        def addToDict(d, key, item):
            if d.has_key(key):
                d.get(key).append(item)
            else:
                d[key] = [item]

        dt = {}
        it = {}
        nt = {}
        bt = {}
        mt = {}
        cltItemTypes = {}
        available = {}
        complete = {}
        unfinished = {}
        npcInfo = {'debateNpcTks': dt,
         'comCltItems': it,
         'needMonsters': nt,
         'beatMonsters': bt,
         'markNpcs': mt,
         'available': available,
         'complete': complete,
         'unfinished': unfinished,
         'cltItemTypes': cltItemTypes}
        questIgnoreLv = SYSD.data.get('questIgnoreLvl', 100)
        playerLv = BigWorld.player().lv
        serverData = BigWorld.player().questInfoCache
        for aQuest in serverData.get('available_tasks', ()):
            if aQuest in self.filterQuests:
                continue
            aData = QD.data.get(aQuest, None)
            if aData != None:
                aNpc = aData.get('acNpc', None)
                if aNpc != None:
                    qType = aData.get('displayType', 0)
                    if not self.needQuestShowByLv(aData, questIgnoreLv):
                        self.filterQuests.append(aQuest)
                        continue
                    if not commQuest.isShowAvailableQuest(aQuest):
                        self.filterQuests.append(aQuest)
                        continue
                    addToDict(available, aNpc, [qType, aQuest])

        for aLoopQuest in serverData.get('available_taskLoops', ()):
            if aLoopQuest in self.filterLoopQuests:
                continue
            firstQuestId = self.getLoopNpc(aLoopQuest, True)
            aLoopData = QD.data.get(firstQuestId, None)
            if aLoopData:
                aLoopNpc = aLoopData.get('acNpc', None)
                qType = aLoopData.get('displayType', 0)
                if not self.needQuestShowByLv(aLoopData, questIgnoreLv):
                    self.filterLoopQuests.append(aLoopQuest)
                    continue
                if not commQuest.isShowAvailableQuest(firstQuestId):
                    self.filterLoopQuests.append(aLoopQuest)
                    continue
                if aLoopNpc:
                    qType = aLoopData.get('displayType', 0)
                    addToDict(available, aLoopNpc, [qType, firstQuestId])

        allQuest = serverData.get('unfinished_tasks', ()) + serverData.get('unfinished_taskLoops', ())
        for uQuest in allQuest:
            if uQuest in serverData.get('unfinished_taskLoops', ()):
                questId = self.getLoopNpc(uQuest, False)
                uData = QD.data.get(questId, None)
            else:
                questId = uQuest
                uData = QD.data.get(uQuest, None)
            if questId in self.filterQuests:
                continue
            if not commQuest.isShowExcludeAvailableMarkQuest(questId):
                self.filterQuests.append(questId)
                continue
            if uData != None:
                name = uData.get('name', '')
                uNpc = commQuest.getQuestCompNpc(BigWorld.player(), questId)
                qType = uData.get('displayType', 0)
                if uNpc != None:
                    addToDict(unfinished, uNpc, [qType, questId])
                debateNpcTk = uData.get('debateNpcTk', 0)
                needDialogTk = self.getNeedDialogTrackId(questId, uData)
                comCltItems = uData.get('comCltItemTk', ())
                needMonsters = self.getMonsterTrackId(questId, uData)
                beatMonsters = uData.get('beatMonsterTk', ())
                markNpcs = self.getMarkerNpcTrackId(questId, uData)
                cltItemTypesData = uData.get('cltItemTypes', ())
                if uData.get('showQuestGoalOrder'):
                    allTks = []
                    tmpTks = [(debateNpcTk,),
                     needDialogTk,
                     comCltItems,
                     needMonsters,
                     beatMonsters,
                     markNpcs]
                    questGoalOrder = uData.get('questGoalOrder', ())
                    for order in questGoalOrder:
                        orderName = QGOR.data.get(order, {}).get('tk')
                        if orderName:
                            if orderName == 'debateNpcTk':
                                tks = uData.get(orderName, 0)
                                tks = (tks,)
                            else:
                                tks = uData.get(orderName, ())
                            if tks:
                                allTks.append(tks)
                                tmpTks.remove(tks)

                    allTks += tmpTks
                    try:
                        for tks in allTks:
                            for tk in tks:
                                if not self.isGoalComplete(tk, info):
                                    if tk in (debateNpcTk,):
                                        debateNpcTk = tk
                                    else:
                                        debateNpcTk = 0
                                    if tk in needDialogTk:
                                        needDialogTk = [tk]
                                    else:
                                        needDialogTk = []
                                    if tk in comCltItems:
                                        comCltItems = [tk]
                                    else:
                                        comCltItems = []
                                    if tk in needMonsters:
                                        needMonsters = [tk]
                                    else:
                                        needMonsters = []
                                    if tk in beatMonsters:
                                        beatMonsters = [tk]
                                    else:
                                        beatMonsters = []
                                    if tk in markNpcs:
                                        markNpcs = [tk]
                                    else:
                                        markNpcs = []
                                    raise Exception()

                    except:
                        pass

                for needDialog in needDialogTk:
                    dt[needDialog] = (name, qType, questId)

                dt[debateNpcTk] = (name, qType, questId)
                for index, comCltItem in enumerate(comCltItems):
                    if not info or not self.isGoalComplete(comCltItem, info):
                        it[comCltItem] = (name, qType, questId)
                        if index < len(cltItemTypesData):
                            cltItemTypes[comCltItem] = cltItemTypesData[index]

                for needMonster in needMonsters:
                    if not info or not self.isGoalComplete(needMonster, info):
                        nt[needMonster] = (name, qType, questId)

                for beatMonster in beatMonsters:
                    if not info or not self.isGoalComplete(beatMonster, info):
                        bt[beatMonster] = (name, qType, questId)

                for markerNpc in markNpcs:
                    if not info or not self.isGoalComplete(markerNpc, info):
                        mt[markerNpc] = (name, qType, questId)

        for cQuest in serverData.get('complete_tasks', ()):
            if cQuest in self.filterQuests:
                continue
            if not commQuest.isShowExcludeAvailableMarkQuest(cQuest):
                self.filterLoopQuests.append(cQuest)
                continue
            cData = QD.data.get(cQuest, None)
            if cData != None:
                cNpc = commQuest.getQuestCompNpc(BigWorld.player(), cQuest)
                if cNpc != None:
                    qType = cData.get('displayType')
                    addToDict(complete, cNpc, [qType, cQuest])

        for cLoopQuest in serverData.get('complete_taskLoops', ()):
            if cLoopQuest in self.filterLoopQuests:
                continue
            questId = self.getLoopNpc(cLoopQuest, False)
            if not commQuest.isShowExcludeAvailableMarkQuest(questId):
                self.filterLoopQuests.append(cLoopQuest)
                continue
            cLoopData = QD.data.get(questId, None)
            if cLoopData != None:
                cLoopNpc = commQuest.getQuestCompNpc(BigWorld.player(), questId)
                qType = cLoopData.get('displayType')
                if cLoopNpc != None:
                    addToDict(complete, cLoopNpc, [qType, questId])

        return npcInfo

    def showTeamMate(self, arr):
        if not self.mapMed or not self.posData:
            return
        else:
            self.teamArr = arr
            p = BigWorld.player()
            if not self.teamArr == None:
                ar = []
                headerArr = []
                assistArr = []
                jieQiArr = []
                zhenChuanArr = []
                partnerArr = []
                marriageArr = []
                for item in self.teamArr:
                    if not item[0]:
                        continue
                    mGbId = item[1]
                    needShow = False
                    if self.curMapNo == self.curViewMapNo:
                        if item[3] == p.spaceNo:
                            needShow = True
                    elif self.isTargetNeedShow(self.getMapName(item[4], item[3], item[0][1]), item[0][1]):
                        needShow = True
                    if needShow and item[0]:
                        isHeader = item[6]
                        isAssist = item[7]
                        isJieQi = item[9]
                        isZhenChuan = item[10]
                        isPartner = item[11]
                        isMarriageTgt = item[12]
                        inDota = False
                        iconType = ICON_TYPE_TEAMATE
                        iconTweenInterval = 0
                        if isHeader:
                            iconType = ICON_TYPE_HEADER
                        elif isAssist:
                            iconType = ICON_TYPE_ASSIST
                        elif isJieQi:
                            iconType = ICON_TYPE_JIEQI
                        elif isZhenChuan:
                            iconType = ICON_TYPE_ZHENCHUAN
                        elif isPartner:
                            iconType = ICON_TYPE_PARTNER
                        elif isMarriageTgt:
                            iconType = ICON_TYPE_MARRIAGE
                        else:
                            iconType = ICON_TYPE_TEAMATE
                        teamIcon = 'ltTeamate' if item[8] else 'ltGroupMate'
                        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                            inDota = formula.inDotaBattleField(p.mapID)
                            if inDota:
                                if getattr(p, 'battleFieldTeam', None):
                                    isLife = p.battleFieldTeam.get(mGbId, {}).get('life', 0)
                                else:
                                    isLife = 0
                                if isLife == gametypes.LIFE_ALIVE:
                                    iconTweenInterval = utils.getRefreshAvatarInfoInterval(p)
                                else:
                                    continue
                                iconType = ICON_TYPE_TEAMATE
                                teamIcon = self._getDotaPlayerIcon(mGbId, gametypes.RELATION_FRIENDLY)
                                if not teamIcon:
                                    teamIcon = 'ltBattleTeamMate' if item[8] else 'ltBattleGroupMate'
                                mEntityId = item[5]
                                if mEntityId:
                                    mEntity = BigWorld.entities.get(mEntityId)
                                    if mEntity:
                                        item[0] = mEntity.position
                                        gameglobal.rds.littlemap.onEnter(iconType, mEntity)
                            elif p.isInPUBG():
                                teamIcon = 'ltTeamate' if item[8] else 'ltGroupMate'
                            else:
                                teamIcon = 'ltBattleTeamMate' if item[8] else 'ltBattleGroupMate'
                        if p.inWingWarCity():
                            mEntityId = item[5]
                            if mEntityId:
                                mEntity = BigWorld.entities.get(mEntityId)
                                if mEntity:
                                    item[0] = mEntity.position
                                    gameglobal.rds.littlemap.onLittleMapEnter(mEntity)
                                else:
                                    gameglobal.rds.littlemap.delEntity(mEntityId)
                        dataArr = [teamIcon,
                         item[2],
                         item[1],
                         item[5]]
                        gfxPos = list(item[0])
                        dataArr.append(gfxPos)
                        dataArr.append(str(item[3]))
                        dataArr.append(item[6])
                        dataArr.append(item[7])
                        dataArr.append(item[8])
                        dataArr.append(item[9])
                        dataArr.append(item[10])
                        dataArr.append(item[11])
                        dataArr.append(item[12])
                        dataArr.append(p.getTeammateNoInPUBG(mGbId))
                        gfxData = {'type': iconType,
                         'x': item[0][0],
                         'y': item[0][2],
                         'data': dataArr,
                         'entityId': item[5],
                         'tweenInterVal': iconTweenInterval}
                        if iconType == ICON_TYPE_HEADER:
                            headerArr.append(gfxData)
                        elif iconType == ICON_TYPE_ASSIST:
                            assistArr.append(gfxData)
                        elif iconType == ICON_TYPE_JIEQI:
                            jieQiArr.append(gfxData)
                        elif iconType == ICON_TYPE_ZHENCHUAN:
                            zhenChuanArr.append(gfxData)
                        elif iconType == ICON_TYPE_PARTNER:
                            partnerArr.append(gfxData)
                        elif iconType == ICON_TYPE_MARRIAGE:
                            marriageArr.append(gfxData)
                        else:
                            ar.append(gfxData)

                arrs = [ar,
                 headerArr,
                 assistArr,
                 jieQiArr,
                 zhenChuanArr,
                 partnerArr,
                 marriageArr]
                if self.mapMed:
                    self.mapMed.Invoke('showTeamMate', uiUtils.array2GfxAarry(arrs, True))
            return

    def showMapFuncBtns(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return
        ar = []
        for key, item in MFD.data.items():
            if item.get('mapNo') == self.curViewMapNo and item.get('type') == uiConst.MAP_FUNC_TYPE_FOR_LITTLE_MAP:
                ar.append(self.itemDataToGfx(MapItemData(ICON_TYPE_MAP_FUNC, item.get('posX'), item.get('posY'), ['ltMapExpansion', item.get('func'), item.get('param')])))

        gfxArr = uiUtils.array2GfxAarry(ar)
        if self.mapMed:
            self.mapMed.Invoke('showMapFuncs', gfxArr)

    def showSeekTarget(self, seekData):
        if self.isTargetNeedShow(seekData['areaNo'], seekData['ypos']):
            if self.mapMed:
                itemData = MapItemData(ICON_TYPE_SEEK_TARGET, int(seekData['xpos']), int(seekData['zpos']), ['ltSeekPos', seekData['xpos'], seekData['zpos']])
                self.mapMed.Invoke('showSeekTarget', self.itemDataToGfx(itemData))

    def hideSeekTarget(self):
        if self.mapMed:
            self.mapMed.Invoke('hideSeekTarget')

    def showPosition(self, pos, areaNo = None):
        if not areaNo:
            areaNo = self.curMapNo
        p = BigWorld.player()
        if self.isTargetNeedShow(areaNo, pos[1]):
            if self.mapMed:
                if p.isInBfDota():
                    self.signalType = uiConst.SIGNAL_TYPE_NULL
                    itemData = MapItemData(ICON_TYPE_DOTA_POSITION, int(pos[0]), int(pos[2]), ['ltMapDotaPos', pos[0], pos[2]])
                else:
                    itemData = MapItemData(ICON_TYPE_POSITION, int(pos[0]), int(pos[2]), ['ltMapPos', pos[0], pos[2]])
                self.mapMed.Invoke('showPosition', self.itemDataToGfx(itemData))

    def showFBEntityIcon(self, entityInfo):
        entityList = []
        if entityInfo and BigWorld.player().inFuben():
            for item in entityInfo:
                if item.get('entityType', '') == FB_ENTITY_TYPE_MONSTER:
                    self._addFbMonster(item, entityList)
                elif item.get('entityType', '') == FB_ENTITY_TYPE_TREASURE_BOX:
                    self._addFbTreasureBox(item, entityList)
                elif item.get('entityType', '') == FB_ENTITY_TYPE_ALONE_CREATION:
                    self._addFbAloneCreation(item, entityList)

        if self.mapMed:
            self.mapMed.Invoke('showFBEntityIcon', uiUtils.array2GfxAarry(entityList, True))

    def _addFbMonster(self, item, entityList):
        monster = MD.data.get(item['charType'])
        if monster:
            mEntityId = item.get('entityId')
            mapIcon = str(monster.get('mapIcon', ''))
            if mapIcon:
                monsterType = ''
                if item.has_key('campId'):
                    relation = formula.getTmpCampIdRelation(BigWorld.player().tCamp, item.get('campId'), formula.getFubenNo(BigWorld.player().spaceNo))
                    if mapIcon.startswith('lt'):
                        iconType = '%s_%s' % (mapIcon, relation)
                    else:
                        iconType = ICON_PATH + 'monster/%s_%s.dds' % (mapIcon, relation)
                elif mapIcon.startswith('lt'):
                    iconType = mapIcon
                else:
                    iconType = ICON_PATH + 'monster/%s.dds' % mapIcon
            else:
                if formula.inHuntBattleField(BigWorld.player().mapID):
                    iconType = ICON_TYPE_HUNT_DICT[ICON_TYPE_HUNT_GIFT]
                else:
                    iconType = 'ltBattleFieldMonster'
                if formula.tmpCampIdRelation(BigWorld.player().tCamp, item.get('campId'), formula.getFubenNo(BigWorld.player().spaceNo), gametypes.RELATION_ENEMY):
                    monsterType = 'EnemyType'
                else:
                    monsterType = 'Type'
            inCombat = item.get('inCombat', False)
            iconTip = monster.get('name', '')
            if monster.get('battleFieldMonsterType', 0):
                iconTip = uiConst.BATTLEFIELD_MONSTER_TYPES.get(monster.get('battleFieldMonsterType', 0), '')
                monsterType += str(monster.get('battleFieldMonsterType', 0))
            itemData = [iconType,
             iconTip,
             inCombat,
             monsterType]
            iconTweenInterval = 0
            if formula.inDotaBattleField(BigWorld.player().mapID):
                iconTweenInterval = const.SYNC_INFO_INTERVAL
            if monster.get('littleMapCombatEffect', True):
                if inCombat and not self.monsterInCombat.get(mEntityId, False):
                    if formula.inDotaBattleField(BigWorld.player().mapID):
                        gameglobal.rds.sound.playSound(5490)
                    else:
                        gameglobal.rds.sound.playSound(gameglobal.SD_511)
                self.monsterInCombat[mEntityId] = inCombat
            if mEntityId and formula.inDotaBattleField(BigWorld.player().mapID):
                mEntity = BigWorld.entities.get(mEntityId)
                if mEntity:
                    item['pos'] = mEntity.position
                    gameglobal.rds.littlemap.onEnter(ICON_TYPE_FB_MONSTER, mEntity)
            mapItem = MapItemData(ICON_TYPE_FB_MONSTER, item['pos'][0], item['pos'][2], itemData, mEntityId, needCombatEffect=True, tweenInterVal=iconTweenInterval)
            entityList.append(self.itemDataToGfx(mapItem))

    def _addFbTreasureBox(self, item, entityList):
        boxData = TBD.data.get(item['treasureBoxId'], {})
        if boxData:
            entityId = item.get('entityId')
            mapIcon = str(boxData.get('mapIcon', ''))
            iconTip = boxData.get('name', '')
            itemData = [mapIcon]
            mapItem = MapItemData(ICON_TYPE_FB_MONSTER, item['pos'][0], item['pos'][2], itemData, entityId, tips=iconTip)
            entityList.append(self.itemDataToGfx(mapItem))

    def _addFbAloneCreation(self, item, entityList):
        cidData = ICD.data.get(item['cid'], {})
        if cidData:
            entityId = item.get('entityId')
            mapIcon = str(cidData.get('mapIcon', ''))
            itemData = [mapIcon]
            mapItem = MapItemData(ICON_TYPE_FB_MONSTER, item['pos'][0], item['pos'][2], itemData, entityId)
            entityList.append(self.itemDataToGfx(mapItem))

    @ui.callAfterTime()
    def showMapMark(self):
        if self.mapMed:
            groupMapMark = BigWorld.player().groupMapMark
            markList = []
            for key, item in groupMapMark.items():
                if item.get('effectId'):
                    mapNo = self.getMapName(item['chunkName'], item['spaceNo'], item['pos'][1])
                    if self.isTargetNeedShow(mapNo, item['pos'][1]):
                        mapItem = MapItemData(ICON_TYPE_MAP_MARK, item['pos'][0], item['pos'][2], ['ltMapMark', gameStrings.TEXT_LITTLEMAPPROXY_1409 % key, key])
                        markList.append(self.itemDataToGfx(mapItem))

            self.mapMed.Invoke('showMapMark', uiUtils.array2GfxAarry(markList, True))

    def showEnemyPlayer(self, playersInfo, areaNo = 0):
        if not areaNo:
            areaNo = self.curMapNo
        if self.mapMed:
            p = BigWorld.player()
            playerList = []
            for gbId, info in playersInfo.iteritems():
                if not self.getOpacityValueByGbId(gbId):
                    continue
                roleName = info[gametypes.TEAM_SYNC_PROPERTY_ROLENAME]
                pos = info[gametypes.TEAM_SYNC_PROPERTY_POSITION]
                iconTweenInterval = 0
                if self.isTargetNeedShow(areaNo, pos[1]):
                    inDota = formula.inDotaBattleField(BigWorld.player().mapID)
                    mEntityId = None
                    if inDota:
                        if getattr(p, 'battleFieldTeam', None):
                            isLife = BigWorld.player().battleFieldTeam.get(gbId, {}).get('life', 0)
                        else:
                            isLife = 0
                        if isLife == gametypes.LIFE_ALIVE:
                            iconTweenInterval = utils.getRefreshAvatarInfoInterval(BigWorld.player())
                        else:
                            continue
                        mEntityId = BigWorld.player().battleFieldTeam.get(gbId, {}).get('id')
                        itemData = [self._getDotaPlayerIcon(gbId, gametypes.RELATION_ENEMY), roleName, str(gbId)]
                    elif formula.inHuntBattleField(BigWorld.player().mapID):
                        itemData = [ICON_TYPE_HUNT_DICT[uiConst.ICON_TYPE_HUNT_PROTECTER], roleName, str(gbId)]
                    else:
                        itemData = ['ltEnemy', roleName, str(gbId)]
                    mapItem = MapItemData(ICON_TYPE_ENEMY, pos[0], pos[2], itemData, entityId=mEntityId, tweenInterVal=iconTweenInterval)
                    playerList.append(self.itemDataToGfx(mapItem))
                    if inDota and mEntityId:
                        mEntity = BigWorld.entities.get(mEntityId)
                        if mEntity:
                            gameglobal.rds.littlemap.onEnter(ICON_TYPE_ENEMY, mEntity)

            self.mapMed.Invoke('showEnemyList', uiUtils.array2GfxAarry(playerList, True))

    def getOpacityValueByGbId(self, gbId):
        visible = True
        p = BigWorld.player()
        if formula.inDotaBattleField(p.mapID):
            entityId = p.battleFieldTeam.get(gbId, {}).get('id', 0)
            entity = BigWorld.entities.get(entityId, None)
            if entity:
                if getattr(entity, 'vehicleId', 0) == getattr(p, 'vehicleId', 0):
                    visible = True
                else:
                    value = entity.getOpacityValue()
                    if value[0] in (gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
                        visible = False
        return visible

    def showTrackTarget(self, seekId):
        if self.mapMed:
            if self.trackTargetCallback:
                BigWorld.cancelCallback(self.trackTargetCallback)
                self.trackTargetCallback = None
            if seekId:
                if BigWorld.player().isMoving:
                    BigWorld.player().showGameMsg(GMDD.data.CANNOT_SHOW_TARCK_TARGET, ())
                    return
                seekData = SD.data.get(seekId)
                if seekData:
                    xpos = seekData.get('xpos', 0)
                    zpos = seekData.get('zpos', 0)
                    ypos = seekData.get('ypos', 0)
                    spaceNo = seekData.get('spaceNo', 0)
                    if spaceNo != 1:
                        mapNo = self.getMapNoBySpaceNo(spaceNo, ypos)
                    else:
                        chunkName = uiUtils.getChunkName(xpos, zpos)
                        mapNo = self.getMapName(chunkName, spaceNo, ypos)
                    if mapNo and self.curViewMapNo != mapNo and isinstance(mapNo, int):
                        self.mapMed.Invoke('setMap', GfxValue(mapNo))
                    itemData = ['ltMapPos', xpos, zpos]
                    mapItem = MapItemData(ICON_TYPE_TRACK_TARGET, xpos, zpos, itemData)
                    self.mapMed.Invoke('showTrackTarget', uiUtils.array2GfxAarry([self.itemDataToGfx(mapItem)], True))
                    self.trackTargetCallback = BigWorld.callback(TRACK_TARGET_CLEAR_TIME, Functor(self.showTrackTarget, 0))
            else:
                self.mapMed.Invoke('showTrackTarget', uiUtils.array2GfxAarry([]))

    def isTargetNeedShow(self, areaNo, posY):
        if areaNo == WORLD_MAP_ID:
            return True
        elif not areaNo:
            return False
        else:
            targetPosData = None
            if type(areaNo) is int:
                areaNo = [areaNo]
            if self.posData:
                for tempNo in areaNo:
                    isInChildMap = not self.posData[-1] == self.curViewMapNo
                    areaInfo = AD.data.get(tempNo, None)
                    if areaInfo:
                        targetPosData = areaInfo.get('posData')
                    if targetPosData and self.posData and (isInChildMap and self.curViewMapNo == tempNo or not isInChildMap and targetPosData[-1] == self.posData[-1]) and (not self.mapHeightRange or self.mapHeightRange[0] <= posY and self.mapHeightRange[0] >= posY):
                        return True

            return

    def isWorldPositionNeedShow(self, pos):
        xpos, ypos, zpos = pos[0], pos[1], pos[2]
        chunkName = uiUtils.getChunkName(xpos, zpos)
        areaNo = self.getMapName(chunkName, 1, ypos)
        return self.isTargetNeedShow(areaNo, ypos)

    def refreshNpcPos(self, info = None):
        self.npcInfo = info
        if not self.refreshNpcCallBack and self.curMapNo:
            self.refreshNpcCallBack = BigWorld.callback(0.1, self._innerRefresNpcPos)

    def _innerRefresNpcPos(self):
        p = BigWorld.player()
        if self.mapMed and self.curMapNo and not p.inClanWar and not p.isInPUBG():
            self.transportStones = {}
            npcDatas = self.getNpcData(self.npcInfo, True)
            if npcDatas != NPC_POS_NO_REFRESH:
                for key in self.gfxNpcDatas.keys():
                    self.gfxNpcDatas[key] = []

                for item in npcDatas:
                    if isinstance(item, GfxValue):
                        self.gfxNpcDatas.setdefault(ICON_TYPE_NPC_FUNC, []).append(item)
                    else:
                        self.gfxNpcDatas.setdefault(item.data[0], []).append(self.itemDataToGfx(item))

                self.refreshGfxNpcDataTypes = self.gfxNpcDatas.keys()
                if self.addNpcCallBack:
                    BigWorld.cancelCallback(self.addNpcCallBack)
                self.addNpcCallBack = BigWorld.callback(0.1, self._refreshNpcIndicator)
        self.refreshNpcCallBack = None

    def _refreshNpcIndicator(self):
        if self.addNpcCallBack:
            BigWorld.cancelCallback(self.addNpcCallBack)
        self.addNpcCallBack = None
        if not len(self.refreshGfxNpcDataTypes):
            return
        else:
            iconType = self.refreshGfxNpcDataTypes.pop(0)
            items = self.gfxNpcDatas.get(iconType, [])
            if self.mapMed:
                self.mapMed.Invoke('showIndicator', uiUtils.array2GfxAarry([[iconType, items]]))
                if len(self.gfxNpcDatas):
                    self.addNpcCallBack = BigWorld.callback(0.1, self._refreshNpcIndicator)
            return

    def _refreshNpcPosUnit(self):
        if self.mapMed and self.curMapNo and self.npcPosUnit:
            if not self.npcPosUnit.isEmpty():
                npcDatas = self.getNpcData(self.npcInfo)
                gfxNpcDatas = []
                for item in npcDatas:
                    gfxNpcDatas.append(self.itemDataToGfx(item))

                self.npcPosUnit.addGfxItems(gfxNpcDatas)
                self.npcPosUnit.next()
                if not self.npcPosUnit.isEmpty():
                    self.refUnitCallBack = BigWorld.callback(NPC_POS_UNIT_REFRESH_TIME, self._refreshNpcPosUnit)
                else:
                    self.mapMed.Invoke('showIndicator', uiUtils.array2GfxAarry(self.npcPosUnit.gfxItems))

    def _stopRefreshNpcPosUnit(self):
        if self.npcPosUnit:
            self.npcPosUnit.clear()
        if self.refUnitCallBack:
            BigWorld.cancelCallback(self.refUnitCallBack)
            self.refUnitCallBack = None

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def itemDataToGfx(self, itemData):
        return itemData.toGfxData()

    def unShowTransportDest(self):
        self.stoneId = 0
        self.destId = 0
        self.availableDest = []

    def doTeleport(self):
        if self.stoneId and self.destId:
            p = BigWorld.player()
            p.cell.realUseTransportStone(self.stoneId, self.destId)
            self.unShowTransportDest()

    def refreshCurMapLvl(self):
        if self.mapMed:
            self.curMapLvl = self.mapMed.Invoke('getCurMapLvl').GetNumber()

    def showConfirm(self, destId = None):
        if self.confirmBoxId:
            return

    def getTransCashBySeekId(self, seekId):
        destId = SD.data.get(seekId, {}).get('npcId')
        return BigWorld.player().getTeleportCost(destId)

    def confirmOK(self):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_TELEPORT_BY_NPC):
            return
        else:
            self.confirmBoxId = None
            return

    def confirmCancel(self):
        self.confirmBoxId = None

    def isMapShow(self):
        if self.mapMed:
            return self.mapMed.Invoke('getVisible').GetBool()

    def drawPathTrace(self, pathPoints, append = True):
        if not self.pathPoints:
            self.clearPathTrace()
        if append:
            self.pathPoints.extend(pathPoints)
        else:
            self.pathPoints = pathPoints
        points = []
        for point in pathPoints:
            points.append((point.x, point.z))

        if self.mapMed:
            self.mapMed.Invoke('addPathTrace', (uiUtils.array2GfxAarry(points), GfxValue(append)))

    def endDrawPathTrace(self):
        self.pathPoints = []
        if self.clearPathCallBack:
            BigWorld.cancelCallback(self.clearPathCallBack)
        delay = SYSD.data.get('clearPathTime', 10)
        self.clearPathCallBack = BigWorld.callback(delay, self.clearPathTrace)

    def clearPathTrace(self):
        if self.clearPathCallBack:
            BigWorld.cancelCallback(self.clearPathCallBack)
        if self.mapMed:
            self.mapMed.Invoke('addPathTrace', (uiUtils.array2GfxAarry([]), GfxValue(False)))

    def getIconByQuestType(self, qType):
        if qType == gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN:
            return ICON_TYPE_QUEST_ZHUXIAN
        if qType == gametypes.QUEST_DISPLAY_TYPE_ZHIXIAN:
            return ICON_TYPE_QUEST_ZHIXIAN
        if qType == gametypes.QUEST_DISPLAY_TYPE_LOOP:
            return ICON_TYPE_QUEST_LOOP
        return ICON_TYPE_QUEST_SPECIAL

    def refreshActive(self):
        if self.mapMed:
            self.mapMed.Invoke('switchMapActive', GfxValue(not gameglobal.LITTLE_MAP_UNHIT_ABLE))

    def updateTransportStone(self, transId):
        if self.mapMed and self.transportStones.has_key(transId):
            iType = 'transportStone'
            for seekId in set(self.transportStones.get(transId, [])):
                seekData = SD.data.get(seekId)
                if seekData and seekData.get('isInTransMap', 0):
                    x, z = seekData['xpos'], seekData['zpos']
                    name, title = self.getSeekTitleName(iType, seekData)
                    npcId = seekData.get('npcId', 0)
                    iconType = 'ltTranstone' if Transport.isActiveStone(npcId) else 'ltUnActiveSend'
                    itemData = MapItemData(ICON_TYPE_TRANSPORT_STONE, x, z, (iconType,
                     name,
                     title,
                     npcId,
                     seekId,
                     Transport.isActiveStone(npcId),
                     self.getTransCashBySeekId(seekId)))
                    self.mapMed.Invoke('updateIcon', self.itemDataToGfx(itemData))

    def showAreaInfo(self, stateInfo, forceRefresh = False):
        p = BigWorld.player()
        if p.isInPUBG():
            return
        if not forceRefresh and self.areaStateInfo == stateInfo:
            return
        self.areaStateInfo = stateInfo
        if self.mapMed:
            dataArr = []
            for key, state in self.areaStateInfo.items():
                areaData = WAD.data.get(key, {})
                x, z = areaData.get('xpos', 0), areaData.get('zpos', 0)
                stateData = WASD.data.get(state, {})
                if self.lastChunkName in stateData.get('chunkList', ()):
                    itemData = MapItemData(ICON_TYPE_AREA_STATE, x, z, ('ltAreaState', stateData.get('tips', ''), key))
                    dataArr.append(self.itemDataToGfx(itemData))

            self.mapMed.Invoke('showAreaInfo', uiUtils.array2GfxAarry(dataArr, True))

    def showGuildBuilding(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return
        else:
            if self.mapMed:
                guildBuildings = []
                for key, value in CWMD.data.items():
                    if key not in BigWorld.player().clanWar.cmarker.keys():
                        pos = value.get('position', (0, 0, 0))
                        if value.get('buildingType') in (gametypes.CLAN_WAR_BUILDING_STONE, gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD) and self.isWorldPositionNeedShow(pos):
                            iconType = 'ltClanWarStoneUnactive' if value.get('buildingType') == gametypes.CLAN_WAR_BUILDING_STONE else 'ltClanWarReliveBoardUnactive'
                            tips = gameStrings.TEXT_LITTLEMAPPROXY_1733 if value.get('buildingType') == gametypes.CLAN_WAR_BUILDING_STONE else gameStrings.TEXT_LITTLEMAPPROXY_1733_1
                            itemData = MapItemData(ICON_TYPE_GUILD_BUILDING, pos[0], pos[2], (iconType, 0), tips=tips)
                            guildBuildings.append(self.itemDataToGfx(itemData))

                for nuid, buildingVla in BigWorld.player().clanWar.building.items():
                    if self.isWorldPositionNeedShow(buildingVla.pos):
                        iconType = None
                        if buildingVla.buildingType == gametypes.CLAN_WAR_BUILDING_STONE:
                            iconType = 'ltClanWarStone'
                            tips = gameStrings.TEXT_LITTLEMAPPROXY_1741
                        elif buildingVla.buildingType == gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD:
                            iconType = 'ltClanWarReliveBoard'
                            tips = gameStrings.TEXT_LITTLEMAPPROXY_1744
                        elif buildingVla.buildingType == gametypes.CLAN_WAR_BUILDING_ANTI_AIR_TOWER:
                            iconType = 'ltClanWarTower'
                            tips = gameStrings.TEXT_LITTLEMAPPROXY_1747
                        if iconType:
                            itemData = MapItemData(ICON_TYPE_GUILD_BUILDING, buildingVla.pos[0], buildingVla.pos[2], (iconType, buildingVla.buildingType), tips=tips)
                            guildBuildings.append(self.itemDataToGfx(itemData))

                self.mapMed.Invoke('showGuildBuilding', uiUtils.array2GfxAarry(guildBuildings, True))
            return

    def showWorldQuest(self):
        if not self.mapMed:
            return
        else:
            arg = []
            p = BigWorld.player()
            if p.isInPUBG():
                return
            for quest in getattr(p, 'worldQuests', None):
                data = WQD.data.get(quest)
                if data:
                    seekId = data.get('tkId', '')
                    seekData = SD.data.get(seekId, {})
                    y = seekData.get('ypos', 0)
                    areaNo = seekData.get('areaNo', 0)
                    if self.isTargetNeedShow(areaNo, y):
                        z = seekData.get('zpos', 0)
                        x = seekData.get('xpos', 0)
                        if CMD.data.get(BigWorld.ChunkInfoAt(p.position), {}).get('worldAreaId', 0) == data.get('areaId', 0):
                            tkType = data.get('tkType', 1)
                            rad = data.get('radioOffset', 0)
                            name = data.get('name', '')
                            itemData = MapItemData(ICON_TYPE_WORLD_QUEST, x, z, ('ltWorldQuest',
                             tkType,
                             rad,
                             name), radii=rad)
                            arg.append(self.itemDataToGfx(itemData))

            self.mapMed.Invoke('showWorldQuest', uiUtils.array2GfxAarry(arg, True))
            return

    def showBfFlagInfo(self):
        if not self.mapMed:
            return
        arg = []
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            spaceNo = formula.getFubenNo(p.spaceNo)
            flags = BFD.data.get(spaceNo, {}).get('flags', ())
            for flagId in flags:
                info = p.bfFlagInfo.get(flagId, {})
                if info:
                    x, _, z = info.get('pos', (0, 0, 0))
                    state = 0
                    camp = info.get('camp', 0)
                    status = info.get('status', 0)
                    if status == 0:
                        state = status
                    else:
                        state = '%s%s' % (int(p.tempCamp == camp), status)
                    itemData = MapItemData(ICON_TYPE_BFFLAG_INFO, x, z, ('ltBfFlag', info.get('littleMapIcon', 1), state))
                    arg.append(self.itemDataToGfx(itemData))

        self.mapMed.Invoke('showBfFlagInfo', uiUtils.array2GfxAarry(arg, True))

    def showBFHuntInfo(self):
        if not self.mapMed:
            return
        arg = []
        for type, dic in self.bfHuntIcons.iteritems():
            for id, info in dic.iteritems():
                itemData = MapItemData(type, info['pos'][0], info['pos'][1], (ICON_TYPE_HUNT_DICT[type], info['state']), tips=info['tips'])
                arg.append(self.itemDataToGfx(itemData))

        self.mapMed.Invoke('showBfHuntInfo', uiUtils.array2GfxAarry(arg, True))

    def showWingWorldWarInfo(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        if not p.inWingWarCity():
            return
        gamelog.info('jbx:showWingWorldWarInfo')
        wingWorldMiniMap = p.wingWorldMiniMap
        buildingArgs = []
        occupyBuildingList = []
        for building in wingWorldMiniMap.buildings:
            buildingType = WCBD.data.get(building.buildingId, {}).get('buildingType', 0)
            if not ICON_TYPE_WING_WORLD_BUILDING_DIC.has_key(buildingType):
                continue
            campIndex = wingWorldMiniMap.attendHost2ColorIdx.get(building.ownHostId, 0)
            if buildingType in gametypes.WING_CITY_WAR_SHOW_HP_TYPES or buildingType == gametypes.WING_CITY_BUILDING_TYPE_AIR_STONE:
                if building.hpPercent:
                    campIndex = 1
                else:
                    campIndex = 4
            insName = ICON_TYPE_WING_WORLD_BUILDING_DIC[buildingType] + 'Camp%d' % campIndex
            tips = WCBD.data.get(building.buildingId, {}).get('name', '')
            isReliveBoard = buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD
            itemData = MapItemData(ICON_TYPE_WING_WORLD_BUILDING, building.position[0], building.position[2], (insName, isReliveBoard, building.entNo), tips=tips)
            buildingArgs.append(self.itemDataToGfx(itemData))
            if wingWorldUtils.isBuildintEntityOccupyable(building.entNo) and campIndex:
                hostNameOffset = WWINGCD.data.get('LittleMapHostNameOffset', (12, -20))
                nameText = utils.getCountryName(building.ownHostId)
                nameText = nameText[:2] if nameText else ''
                text = uiUtils.toHtml(nameText, CAN_OCCUPY_BUILDING_COLOR[campIndex - 1])
                buildingItemData = MapItemData(ICON_TYPE_WING_WORLD_HOST_NAME, building.position[0] + hostNameOffset[0], building.position[2] + hostNameOffset[1], ('MAP_ICON_OCCUPY_BUILDING_NAME', text))
                occupyBuildingList.append(self.itemDataToGfx(buildingItemData))

        gamelog.info('jbx:wingWorldBuilding,len', len(buildingArgs))
        groupPosArg = []
        for wingWorldMinMapGroupPos in wingWorldMiniMap.hostMinMap.posData:
            posType = wingWorldMinMapGroupPos.type
            pos = wingWorldMinMapGroupPos.pos
            tips = ''
            iconType = 0
            if posType == gametypes.WING_MIN_MAP_POS_TYPE_GROUP:
                continue
            elif posType == gametypes.WING_MIN_MAP_POS_TYPE_CAPTAIN:
                continue
            elif posType == gametypes.WING_MIN_MAP_POS_TYPE_CARRIER:
                iconType = ICON_TYPE_WING_WORLD_ZAIJU
                tips = ZJD.data.get(wingWorldMinMapGroupPos.tempalteId, {}).get('name', '')
            itemData = MapItemData(iconType, pos[0], pos[2], (ICON_TYPE_WING_WORLD_DICT[iconType],), tips=tips, tweenInterVal=const.REFRESH_AVATAR_INFO_BATTLEFIELD_DOTA_INTERVAL)
            groupPosArg.append(self.itemDataToGfx(itemData))

        gamelog.info('jbx:groupPosInfo, len', len(groupPosArg))
        gamelog.info('jbx:occuplyList, len', len(occupyBuildingList))
        self.mapMed.Invoke('showWingWorldWarInfo', uiUtils.array2GfxAarry(buildingArgs + groupPosArg + occupyBuildingList, True))

    def showBattleFortCrystalIcon(self):
        p = BigWorld.player()
        if p.mapID not in const.FB_NO_BATTLE_FIELD_NEW_FLAG:
            if self.otherItem.has_key(uiConst.MAP_ICON_BATTLE_FORT_OCCUPY):
                self.delOtherItems((uiConst.MAP_ICON_BATTLE_FORT_OCCUPY,))
            return
        crystalList = []
        entities = BFD.data.get(p.mapID, {}).get('needLoadPos', (1, 2, 3))
        if not entities:
            return
        for enNo in entities:
            realNo = formula.getRealFbEntityNo(enNo, p.spaceNo)
            if realNo in p.battleFiedlOccupyInfo:
                occupyInfo = p.battleFiedlOccupyInfo[realNo]
                camp = occupyInfo.get('camp', 0)
            else:
                camp = 0
            otherCamp = 3 - p.tempCamp
            if camp == p.tempCamp:
                colorCamp = 2
            elif camp == otherCamp:
                colorCamp = 1
            else:
                colorCamp = 0
            val = FED.data.get(realNo, {})
            pos = val.get('pos', (0, 0, 0))
            fortId = val.get('entityNo', 0)
            fortName = BFFD.data.get(fortId, {}).get('fortName', '')
            if fortId in uiConst.BATTLE_MAIN_FIELD_FORT_IDS:
                mapIcon = 'ltBattleMainCrystal%d' % colorCamp
            elif fortId in uiConst.BATTLE_SECOND_FIELD_FORT_IDS:
                mapIcon = 'ltBattleSubCrystal%d' % colorCamp
            else:
                mapIcon = ''
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=fortName, data=(mapIcon,), areaNo=p.mapID)
            crystalList.append(item)

        gamelog.info('@yj:showBattleFortCrystalIcon, len(crystalList) =', len(crystalList))
        bornPoints = []
        campPos = BFD.data.get(p.mapID, {}).get('campPos', {'1': (0, 0, 0),
         '2': (0, 0, 0)})
        if not campPos:
            return
        for sideIndex, pos in campPos.iteritems():
            if int(sideIndex) == p.tempCamp:
                colorCamp = 2
            else:
                colorCamp = 1
            mapIcon = 'ltBattleFortSide%d' % colorCamp
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(mapIcon,), areaNo=p.mapID)
            bornPoints.append(item)

        gamelog.info('@yj:showBattleFortCrystalIcon, len(bornPoints) =', len(bornPoints))
        self.addOtherItems({uiConst.MAP_ICON_BATTLE_FORT_OCCUPY: crystalList + bornPoints})

    def showBattleFortZaijuIcon(self):
        p = BigWorld.player()
        gamelog.info('@yj:showBattleFortZaijuIcon, mapID, battleFieldZaijus =', p.mapID, p.battleFieldZaijus)
        if p.mapID not in const.FB_NO_BATTLE_FIELD_NEW_FLAG:
            return
        if self.otherItem.has_key(uiConst.MAP_ICON_BATTLE_FORT_ZAI_JU):
            self.delOtherItems((uiConst.MAP_ICON_BATTLE_FORT_ZAI_JU,))
        zaijuList = []
        for zaijuNUID, info in p.battleFieldZaijus.iteritems():
            camp = info.get('camp', 0)
            pos = info.get('pos', (0, 0, 0))
            otherCamp = 3 - p.tempCamp
            if camp == p.tempCamp:
                colorCamp = 2
            elif camp == otherCamp:
                colorCamp = 1
            else:
                colorCamp = 0
            mapIcon = 'ltBattleFortZaiju%d' % colorCamp
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(mapIcon,), areaNo=p.mapID)
            zaijuList.append(item)

        gamelog.info('@yj:showBattleFortZaijuIcon, len(zaijuList) =', len(zaijuList))
        self.addOtherItems({uiConst.MAP_ICON_BATTLE_FORT_ZAI_JU: zaijuList})

    def showBattleFortMonsterIcon(self):
        p = BigWorld.player()
        if p.mapID not in const.FB_NO_BATTLE_FIELD_NEW_FLAG:
            return
        if self.otherItem.has_key(uiConst.MAP_ICON_BATTLE_FORT_MONSTERS):
            self.delOtherItems((uiConst.MAP_ICON_BATTLE_FORT_MONSTERS,))
        monstersIcon = []
        for fbEntityNo, pos in p.battleFiedlMonstersPos.iteritems():
            mapIcon = 'ltBattleFortSoldier'
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(mapIcon,), areaNo=p.mapID)
            monstersIcon.append(item)

        gamelog.info('@yj:showBattleFortMonsterIcon, len(monstersIcon) =', len(monstersIcon))
        self.addOtherItems({uiConst.MAP_ICON_BATTLE_FORT_MONSTERS: monstersIcon})

    def showWingWorldWarEvent(self, entNo):
        if not self.mapMed:
            return
        if self.wingWorldEventTimer:
            BigWorld.cancelCallback(self.wingWorldEventTimer)
            self.wingWorldEventTimer = 0
        p = BigWorld.player()
        if not p.inWingWarCity():
            return
        pos = WCBED.data.get(entNo, {}).get('position', (0, 0, 0))
        self.setWingWorldWarEventEffectVisible(True)
        self.mapMed.Invoke('showWingWorldWarEvent', uiUtils.array2GfxAarry([pos[0], pos[2]], True))
        self.wingWorldEventTimer = BigWorld.callback(3, Functor(self.setWingWorldWarEventEffectVisible, False))

    def test(self):
        pos = BigWorld.player().position
        self.setWingWorldWarEventEffectVisible(True)
        self.mapMed.Invoke('showWingWorldWarEvent', uiUtils.array2GfxAarry([pos[0], pos[2]], True))
        self.wingWorldEventTimer = BigWorld.callback(3, Functor(self.setWingWorldWarEventEffectVisible, False))

    def setWingWorldWarEventEffectVisible(self, visible):
        self.wingWorldEventTimer = 0
        if not self.mapMed:
            return
        self.mapMed.Invoke('setWingWorldEventEffectVisible', GfxValue(visible))

    def showFallenRedGuard(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        arg = []
        flagList = getattr(BigWorld.player(), 'fallenRedGuardFlagList', [])
        if not clientUtils.checkFallendRedGuardTime():
            flagList = []
        for flagId, isDead in flagList:
            insName = 'LittleMap_FallenRedGaurd' if not isDead else 'LittleMap_FallenRedGaurdDead'
            posX = FRGD.data.get(flagId, {}).get('xpos', 0)
            posZ = FRGD.data.get(flagId, {}).get('zpos', 0)
            tips = gameStrings.FALLEN_RED_GUARD_ALIVE if not isDead else gameStrings.FALLEN_RED_GUARD_KILLED
            itemData = MapItemData(ICON_TYPE_OTHER, posX, posZ, [insName], tips=tips)
            arg.append(self.itemDataToGfx(itemData))

        self.mapMed.Invoke('showFallendRedGuardList', uiUtils.array2GfxAarry(arg, True))

    def setPlayIconVisible(self, visible):
        if self.mapMed:
            self.mapMed.Invoke('setPlayIconVisible', GfxValue(visible))

    def addBFHuntIcon(self, type, srcGbId, desGbId, pos, state, forceUpdate = True, tips = None):
        p = BigWorld.player()
        if not formula.inHuntBattleField(p.mapID):
            return
        else:
            typeDict = self.bfHuntIcons.get(type, None)
            if typeDict == None:
                return
            info = {}
            info['type'] = type
            info['pos'] = (pos[0], pos[2])
            info['state'] = state
            info['tips'] = tips
            for src, des in typeDict.keys():
                if src == srcGbId and des == None:
                    typeDict.pop((srcGbId, des))

            typeDict[srcGbId, desGbId] = info
            if forceUpdate:
                self.showBFHuntInfo()
            return

    def delBFHuntIcon(self, type, srcGbId, desGbId, forceUpdate = True):
        typeDict = self.bfHuntIcons.get(type, None)
        if typeDict == None:
            return
        else:
            if typeDict.has_key((srcGbId, desGbId)):
                typeDict.pop((srcGbId, desGbId))
            if forceUpdate:
                self.showBFHuntInfo()
            return

    def clearBFHuntIcons(self):
        self.bfHuntIcons = {ICON_TYPE_HUNT_GIFT: {},
         ICON_TYPE_HUNT_PROTECTER: {},
         ICON_TYPE_HUNT_SPRITE: {},
         ICON_TYPE_HUNT_TRAP: {}}
        self.showBFHuntInfo()

    def showBfFortInfo(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        if not hasattr(p, 'bfFortInfo'):
            return
        arg = []
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            spaceNo = formula.getFubenNo(p.spaceNo)
            forts = BFD.data.get(spaceNo, {}).get('forts', ())
            for fortId in forts:
                info = p.bfFortInfo.get(fortId, {})
                if info:
                    x, _, z = info.get('pos', (0, 0, 0))
                    state = 0
                    camp = info.get('camp', 0)
                    fortId = info.get('fortId', 0)
                    curValMap = info.get('curValMap', {})
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
                    icon = BFFD.data.get(fortId, {}).get('icon', 1)
                    if status == 0:
                        state = icon * 1000 + status
                    else:
                        state = icon * 1000 + int(occupType in (uiConst.BF_FORT_STATE_MY_FULL_HOLDED, uiConst.BF_FORT_STATE_MY_HALF_HOLDED)) * 10 + status
                    itemData = MapItemData(ICON_TYPE_BFFLAG_INFO, x, z, (ICON_PATH + 'battleFort/%s.dds' % state, 0, 0), fortId)
                    arg.append(self.itemDataToGfx(itemData))

            if hasattr(p, 'bfPlanePosInfo'):
                for info in p.bfPlanePosInfo:
                    x, _, z = info.get('pos', (0, 0, 0))
                    camp = info.get('camp', 0)
                    if camp == p.tempCamp:
                        iconPath = ICON_PATH + 'battlePlane/1.dds'
                    else:
                        iconPath = ICON_PATH + 'battlePlane/2.dds'
                    itemData = MapItemData(ICON_TYPE_BFFLAG_INFO, x, z, (iconPath, 0, 0))
                    arg.append(self.itemDataToGfx(itemData))

        self.mapMed.Invoke('showBfFlagInfo', uiUtils.array2GfxAarry(arg, True))

    @ui.callAfterTime()
    def showOtherItems(self):
        if not self.mapMed:
            return
        allItems = []
        for key, val in self.otherItem.iteritems():
            arr = []
            if isinstance(val, Iterable):
                for item in val:
                    if self.checkOtherItemsValid(key, item):
                        arr.append(self.itemDataToGfx(item))

            elif self.checkOtherItemsValid(key, val):
                arr.append(self.itemDataToGfx(val))
            allItems.append((key, arr))

        self.mapMed.Invoke('showOtherItems', uiUtils.array2GfxAarry(allItems, True))

    def checkOtherItemsValid(self, key, item):
        if item.areaNo and self.isTargetNeedShow(item.areaNo, item.y):
            return True
        else:
            return False

    def addOtherItems(self, itemDict):
        self.otherItem.update(itemDict)
        self.showOtherItems()

    def delOtherItems(self, keys):
        for key in keys:
            if self.otherItem.has_key(key):
                self.otherItem[key] = []

        self.showOtherItems()

    def acceptQuestDone(self, questId):
        if self.lastQuestInfo:
            qData = QLID.data.get(questId, '')
            if qData:
                qLoop = qData.get('questLoop', 0)
                if qLoop and qLoop in self.lastQuestInfo.get('available_taskLoops', []):
                    self.lastQuestInfo.get('available_taskLoops', []).remove(qLoop)
            elif questId and questId in self.lastQuestInfo.get('available_tasks', []):
                self.lastQuestInfo.get('available_tasks', []).remove(questId)

    def addYabiaoZaiju(self, pos):
        if pos:
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=gameStrings.TEXT_LITTLEMAPPROXY_2196, data=('ltguozhanbiaoche',), areaNo=uiConst.WW_AREA_NO)
            self.addOtherItems({uiConst.LITTLE_MAP_OTHER_BIAOCHE: item})

    def delYabiaoZaiju(self):
        self.delOtherItems((uiConst.LITTLE_MAP_OTHER_BIAOCHE,))

    def addWWRBattleIcon(self):
        otherItem = {}
        p = BigWorld.player()
        ww = p.worldWar
        for fortId, val in WWFD.data.items():
            if val.get('icon'):
                pos = val.get('position', (0, 0, 0))
                camp = 0
                if val.get('type', 0) == gametypes.WW_ROB_FORT_TYPE:
                    hostId = ww.getFortHostId(fortId)
                    if hostId:
                        camp = ww.getCountry(hostId).camp
                robAreaMapId = list(val.get('robAreaMapId', ()))
                if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False) and robAreaMapId:
                    robAreaMapId.append(gametypes.WW_ROB_OLD_MAP_ID)
                item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=val.get('name', ''), data=(ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp),), areaNo=robAreaMapId)
                otherItem['%s_%s' % (uiConst.LITTLE_MAP_OTHER_WW_ROB_FORT, fortId)] = item

        if not p.isWWRInRightState():
            self.delOtherItems(otherItem)
        else:
            self.addOtherItems(otherItem)

    def addWWBossIcon(self, bossInfos):
        p = BigWorld.player()
        if not bossInfos:
            return
        elif not self.mapMed:
            return
        elif not p.inWingPeaceCity():
            return
        else:
            liveIconPath = WWINGCD.data.get('liveIconPath', 'wingWorld/34213.dds')
            deathIconPath = WWINGCD.data.get('deathIconPath', 'wingWorld/34214.dds')
            tipsPrefix = gameStrings.WING_WORLD_ALLSOULS_ICON_TIP
            otherItem = {}
            for cfgId, state, killTime in bossInfos:
                if state not in (const.SOUL_BOSS_STATE_ALIVE, const.SOUL_BOSS_STATE_KILLED):
                    continue
                bossCfg = WSBD.data.get(cfgId, {})
                if not bossCfg:
                    continue
                bossPos = bossCfg.get('pos', None)
                bossName = MD.data.get(bossCfg.get('avatarId', 0), {}).get('name', '')
                bossIcon = liveIconPath if state == const.SOUL_BOSS_STATE_ALIVE else deathIconPath
                item = MapItemData(ICON_TYPE_OTHER, bossPos[0], bossPos[2], tips=tipsPrefix % bossName, data=(bossIcon,), areaNo=self.curMapNo)
                otherItem['%s_%s' % (uiConst.MAP_ICON_OTHER_WING_BOSS_FLAG, cfgId)] = item

            gamelog.debug('ypc@ littleMap addWWBossIcon! otherItem = ', otherItem)
            self.addOtherItems(otherItem)
            return

    def addClanWarYaBiao(self):
        if not self.mapMed or not gameconfigCommon.enableClanWarCourier():
            return
        elif not BigWorld.player().inClanCourier():
            return
        else:
            yabiaoStartIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoStartSmallIcon', '')
            yabiaoEndIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoEndSmallIcon', '')
            yabiaoMoveIcon = 'clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYabiaoMoveSmallIcon', '')
            startPos = [ value.get('pos', (0, 0, 0)) for value in CCD.data.itervalues() ]
            startPos = set(startPos)
            endPos = [ value.get('dstPos', (0, 0, 0)) for value in CCD.data.itervalues() ]
            endPos = set(endPos)
            clanCourierDic = getattr(BigWorld.player(), 'clanCourierDic', {})
            movePos = [ value.get('pos', (0, 0, 0)) for value in clanCourierDic.itervalues() if value.get('pos', None) and not value.get('isEnd', False) ]
            ret = []
            if CCCD.data.get('clanWarYabiaoStartSmallIcon', ''):
                for pos in startPos:
                    item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(yabiaoStartIcon,), areaNo=self.curMapNo)
                    ret.append(item)

            if CCCD.data.get('clanWarYabiaoEndSmallIcon', ''):
                for pos in endPos:
                    item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(yabiaoEndIcon,), areaNo=self.curMapNo)
                    ret.append(item)

            for pos in movePos:
                item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips='', data=(yabiaoMoveIcon,), areaNo=self.curMapNo)
                ret.append(item)

            self.addOtherItems({uiConst.MAP_ICON_OTHER_CLAN_WAR_YABIAO: ret})
            return

    def addBattleCqzzFlagIcon(self, pos, camp, state = 0):
        if not hasattr(self, 'cqzzFlagInfo'):
            self.cqzzFlagInfo = {}
        self.cqzzFlagInfo['%s_%s' % (uiConst.MAP_ICON_BATTLE_CQZZ_FLAG, camp)] = (pos, state)
        self.showCqzzFlagInfo()

    def showCqzzFlagInfo(self):
        arg = []
        if not hasattr(self, 'cqzzFlagInfo'):
            return
        tipText = gameStrings.BATTLE_CQZZ_FLAG_NAME
        for camp in [1, 2]:
            flagInfo = self.cqzzFlagInfo.get('%s_%s' % (uiConst.MAP_ICON_BATTLE_CQZZ_FLAG, camp), {})
            if flagInfo:
                pos, state = flagInfo
                flags = DCD.data.get('battleCqzzFlagIcons', {1: 'LittleMap_blueFlag',
                 2: 'LittleMap_redFlag'})
                item = MapItemData(ICON_TYPE_BFFLAG_INFO, pos[0], pos[2], tips=tipText, data=(flags.get(camp, ''), state), areaNo=self.curMapNo)
                arg.append(self.itemDataToGfx(item))

        if not self.mapMed:
            return
        self.mapMed.Invoke('showBfFlagInfo', uiUtils.array2GfxAarry(arg, True))

    def setInitCqzzFlag(self, camp, isInit = False):
        p = BigWorld.player()
        cqzzFlagPosGetState = getattr(p, 'cqzzFlagPosGetState', {})
        flagState = 0
        if isInit and cqzzFlagPosGetState.get(camp, 0):
            pos = cqzzFlagPosGetState.get(camp, (0, 0, 0))
            flagState = 1
        else:
            cqzzFlagPos = DCD.data.get('cqzzFlagPos', {})
            pos = cqzzFlagPos.get(camp, (0, 0, 0))
        self.addBattleCqzzFlagIcon(pos, camp, flagState)

    def addBattleCqzzOtherIcons(self):
        otherItem = {}
        self.cqzzFlagInfo = {}
        p = BigWorld.player()
        if not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_CQZZ):
            return
        spaceNo = formula.getFubenNo(p.spaceNo)
        campPos = BFD.data.get(spaceNo, {}).get('relivePos', {})
        if not campPos:
            campPos = BFD.data.get(spaceNo, {}).get('campPos', {})
        for camp in [1, 2]:
            pos = campPos.get(str(camp), (0, 0, 0))
            tipText = gameStrings.BATTLE_CQZZ_BASE_NAME
            bases = DCD.data.get('battleCqzzBaseIcons', {1: 'cqzz/bbase.dds',
             2: 'cqzz/rbase.dds'})
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=tipText, data=(bases.get(camp, ''),), areaNo=self.curMapNo)
            otherItem['%s_%d' % (uiConst.MAP_ICON_BATTLE_CQZZ_BASE, camp)] = item

        cqzzFlagPos = DCD.data.get('cqzzFlagPos', {})
        for camp in [1, 2]:
            pos = cqzzFlagPos.get(camp, (0, 0, 0))
            tipText = gameStrings.BATTLE_CQZZ_STICK_NAME
            sticks = DCD.data.get('battleCqzzStickIcons', {1: 'cqzz/bstick.dds',
             2: 'cqzz/rstick.dds'})
            item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=tipText, data=(sticks.get(camp, ''),), areaNo=self.curMapNo)
            otherItem['%s_%d' % (uiConst.MAP_ICON_BATTLE_CQZZ_STICK, camp)] = item

        self.addOtherItems(otherItem)
        for camp in [1, 2]:
            self.setInitCqzzFlag(camp, True)

    def addWWBattleIcon(self):
        p = BigWorld.player()
        if not formula.spaceInWorldWarBattle(p.spaceNo):
            return
        otherItem = {}
        ww = p.worldWar
        for fortId, val in WWFD.data.items():
            if val.get('icon'):
                pos = val.get('position', (0, 0, 0))
                camp = 0
                hostId = ww.getFortHostId(fortId)
                if hostId:
                    camp = ww.getCountry(hostId).camp
                areaMapIds = copy.deepcopy(list(val.get('wwMapId', [])))
                areaMapIds.append(val.get('areaMapId', 0))
                item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=val.get('name', ''), data=(ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp),), areaNo=areaMapIds)
                otherItem['%s_%s' % (uiConst.LITTLE_MAP_OTHER_WW_FORT, fortId)] = item

        self.addOtherItems(otherItem)

    def addWWReliveIcon(self):
        otherItem = {}
        p = BigWorld.player()
        if not (formula.spaceInWorldWarBattle(p.spaceNo) or formula.spaceInWorldWarRob(p.spaceNo)):
            return
        ww = p.worldWar
        for reliveId, val in WWRBD.data.items():
            if val.get('icon'):
                pos = val.get('position', (0, 0, 0))
                camp = 0
                hostId = ww.reliveBoard.get(reliveId, 0)
                if hostId:
                    camp = ww.getCountry(hostId).currCamp
                mapIds = list(val.get('wwMapIds', ()))
                mapIds.append(val.get('areaMapId', 0))
                item = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], tips=val.get('name', ''), data=(ICON_PATH + 'worldWarBattle/%s_%s.dds' % (val.get('icon'), camp),), areaNo=mapIds)
                otherItem['%s_%s' % (uiConst.LITTLE_MAP_OTHER_WW_RELIVEBOARD, reliveId)] = item

        self.addOtherItems(otherItem)

    def delWWBattleIcon(self):
        delItems = []
        for key in WWFD.data.keys():
            delItems.append('%s_%s' % (uiConst.LITTLE_MAP_OTHER_WW_FORT, key))

        self.delOtherItems(delItems)

    def delWWReliveIcon(self):
        delItems = []
        for key in WWRBD.data.keys():
            delItems.append('%s_%s' % (uiConst.LITTLE_MAP_OTHER_WW_RELIVEBOARD, key))

        self.delOtherItems(delItems)

    def addRobZaiju(self, force = False):
        if not self.mapMed:
            return
        p = BigWorld.player()
        ww = p.worldWar
        data = {}
        data['robZaijuItem'] = []
        pos = ww.robZaiju.position
        if ww.robState in gametypes.WW_ROB_STATE_NOT_OPEN or not pos or not p.isInRobSpace():
            data['visible'] = False
            data['robZaijuItem'] = []
        else:
            data['visible'] = True
            pos = ww.robZaiju.position
            level = ww.robZaiju.level
            radio = WWCD.data.get('robZaijuAuraRange', 0)
            arrZaiju = ['Little_Map_Rob_Zaiju', 'level%d' % level]
            if self.isTargetNeedShow(self.curMapNo, pos[1]):
                data['robZaijuItem'] = [self.itemDataToGfx(MapItemData(ICON_TYPE_ROB_ZAIJU, pos[0], pos[2], data=arrZaiju, areaNo=self.curMapNo, radii=radio))]
            else:
                data['robZaijuItem'] = []
        if not force:
            if not p.isWWRInRightState():
                data['visible'] = False
                data['robZaijuItem'] = []
        if ww.robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN:
            data['visible'] = False
            data['robZaijuItem'] = []
        self.mapMed.Invoke('showRobZaiju', uiUtils.dict2GfxDict(data, True))

    def refreshMapRotation(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        mapData = AD.data.get(self.curViewMapNo, {})
        rotation = mapData.get('rotation', 0)
        if rotation == 0:
            if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                bfRotation = mapData.get('bfRotation')
                if bfRotation:
                    rotation = bfRotation[p.bfSideIndex]
        self.mapMed.Invoke('setRotation', GfxValue(rotation))

    def onPlayerEnterDotaZaiju(self):
        if self.mapMed and formula.inDotaBattleField(BigWorld.player().mapID):
            iconPath = self._getDotaPlayerIcon(BigWorld.player().gbId, gametypes.RELATION_NEUTRAL)
            if iconPath:
                self.mapMed.Invoke('setPlayerIcon', GfxValue(iconPath))

    def resetPlayerIcon(self):
        if self.mapMed:
            self.mapMed.Invoke('setPlayerIcon')

    def _getDotaPlayerIcon(self, gbId, relation):
        iconPath = ''
        zaijuNo = BigWorld.player().bfDotaZaijuRecord.get(gbId, 0)
        zaijuInfo = ZJD.data.get(zaijuNo, {})
        if zaijuInfo and zaijuInfo.get('mapIcon'):
            iconPath = ICON_PATH + 'monster/%s_%s.dds' % (zaijuInfo.get('mapIcon'), relation)
        return iconPath

    def setHpInfo(self, hpInfo):
        if not self.mapMed:
            return
        combatNos = []
        p = BigWorld.player()
        deadIds = set(self.oldHpInfo) - set(hpInfo)
        for _, val in hpInfo.iteritems():
            campId = val.get('campId')
            key = val.get('fbEntityNo', 0)
            relation = formula.getTmpCampIdRelation(BigWorld.player().tCamp, campId, formula.getFubenNo(BigWorld.player().spaceNo))
            if relation != gametypes.RELATION_FRIENDLY:
                continue
            monster = MD.data.get(FED.data.get(key, {}).get('entityNo'), {})
            if monster.get('littleMapCombatEffect', True):
                inCombat = val.get('inCombat', False)
                if inCombat:
                    combatNos.append(key)
                    if not self.monsterInCombat.get(key, False):
                        if p.isInBfDota():
                            gameglobal.rds.sound.playSound(5490, interrupt=False)
                        else:
                            gameglobal.rds.sound.playSound(gameglobal.SD_511)
                self.monsterInCombat[key] = inCombat

        for id in deadIds:
            if p.isInBfDota() and not self.uiAdapter.isHideAllUI():
                campId = self.oldHpInfo[id]['campId']
                relation = formula.getTmpCampIdRelation(BigWorld.player().tCamp, campId, formula.getFubenNo(BigWorld.player().spaceNo))
                if relation == gametypes.RELATION_FRIENDLY:
                    gameglobal.rds.sound.playSound(5701)
                elif relation == gametypes.RELATION_ENEMY:
                    gameglobal.rds.sound.playSound(5700)

        self.oldHpInfo = hpInfo
        if p.isInBfDota() and hpInfo:
            self.mapMed.Invoke('setMonsterHp', (GfxValue(uiConst.MAP_ICON_OTHER_BATTLEFIELD_HP_ENTITIES), uiUtils.array2GfxAarry(hpInfo.values(), True), uiUtils.array2GfxAarry(combatNos)))

    def getMarkerNpcTrackId(self, questId, qd):
        markNpcs = list(qd.get('markerNpcsTk', ()))
        player = BigWorld.player()
        markerIndex = player.getQuestData(questId, const.QD_QUEST_MARKER_INDEX)
        if markerIndex:
            for groupId, index in markerIndex:
                qmgd = QMGD.data.get(groupId, {})
                markerTkList = qmgd.get('markerTkList', [])
                if index < len(markerTkList):
                    markNpcs.append(markerTkList[index])

        return tuple(markNpcs)

    def getMonsterTrackId(self, questId, qd):
        needMonsterTk = list(qd.get('needMonsterTk', ()))
        needMonstersGroup = qd.get('needMonstersGroup', 0)
        if needMonstersGroup:
            qmgd = QMOGD.data.get(needMonstersGroup, {})
            monsterTkList = qmgd.get('monsterTkList', [])
            player = BigWorld.player()
            randomMonstersGroup, randomIndex = player.getQuestData(questId, const.QD_GROUP_MONSTER_INFO, ({}, []))
            for i, index in enumerate(randomIndex):
                if index < len(monsterTkList):
                    trackId = monsterTkList[index]
                    needMonsterTk.append(trackId)

        return tuple(needMonsterTk)

    def getNeedDialogTrackId(self, questId, qd):
        needDialogTk = list(qd.get('needDialogTk', ()))
        dialogGroup, _ = qd.get('needDialogGroup', (0, 0))
        if dialogGroup:
            player = BigWorld.player()
            dialogIndex = player.getQuestData(questId, const.QD_QUEST_CHAT_INDEX)
            qngd = QNGD.data.get(dialogGroup, {})
            if dialogIndex:
                for index in dialogIndex:
                    npcTkList = qngd.get('npcTkList')
                    if index < len(npcTkList):
                        trackId = npcTkList[index]
                        needDialogTk.append(trackId)

        return tuple(needDialogTk)

    def refreshGuildRobberNpcInfo(self):
        p = BigWorld.player()
        if p.inGuildSpace() and hasattr(p, 'guildRobberNpcInfo'):
            items = []
            for info in p.guildRobberNpcInfo:
                items.append(MapItemData(ICON_TYPE_OTHER, info[0][0], info[0][2], ('ltGuildRobberNpc',), areaNo=self.curMapNo, pos=info[0]))

            self.addOtherItems({uiConst.MAP_ICON_OTHER_GUILD_ROBBER_NPC: items})
        elif self.otherItem.has_key(uiConst.MAP_ICON_OTHER_GUILD_ROBBER_NPC):
            self.delOtherItems((uiConst.MAP_ICON_OTHER_GUILD_ROBBER_NPC,))

    def refreshBattleFiledEntity(self):
        p = BigWorld.player()
        if formula.inDotaBattleField(p.mapID):
            items = self._getBattileFieldEntityData('needLoadPos')
            hpItems = self._getBattileFieldEntityData('needLoadPosTower')
            self.addOtherItems({uiConst.MAP_ICON_OTHER_BATTLEFIELD_ENTITIES: items,
             uiConst.MAP_ICON_OTHER_BATTLEFIELD_HP_ENTITIES: hpItems})
        else:
            if self.otherItem.has_key(uiConst.MAP_ICON_OTHER_BATTLEFIELD_ENTITIES):
                self.delOtherItems((uiConst.MAP_ICON_OTHER_BATTLEFIELD_ENTITIES,))
            if self.otherItem.has_key(uiConst.MAP_ICON_OTHER_BATTLEFIELD_HP_ENTITIES):
                self.delOtherItems((uiConst.MAP_ICON_OTHER_BATTLEFIELD_HP_ENTITIES,))

    def _getBattileFieldEntityData(self, key):
        p = BigWorld.player()
        items = []
        entities = BFD.data.get(p.mapID, {}).get(key)
        if entities:
            for enNo in entities:
                realNo = formula.getRealFbEntityNo(enNo, p.spaceNo)
                val = FED.data.get(realNo, {})
                monster = MD.data.get(val.get('entityNo'))
                if not monster:
                    continue
                pos = val.get('pos')
                camp = val.get('campId')
                mapIcon = str(monster.get('mapIcon', ''))
                isFriend = False
                if mapIcon:
                    relation = formula.getTmpCampIdRelation(p.tCamp, camp, p.mapID)
                    isFriend = relation == gametypes.RELATION_FRIENDLY
                    if mapIcon.startswith('lt'):
                        iconType = '%s_%s' % (mapIcon, relation)
                    else:
                        iconType = ICON_PATH + 'monster/%s_%s.dds' % (mapIcon, relation)
                items.append(MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], (iconType, isFriend), realNo, areaNo=p.mapID))

        return items

    @ui.uiEvent(uiConst.WIDGET_LITTLE_MAP, events.EVENT_ROLE_SET_LV)
    def resetFilterQuests(self):
        self.filterLoopQuests = []
        self.filterQuests = []

    def playBfDotaBtnsCoolDown(self):
        if self.bfDotaBtnTimer:
            BigWorld.cancelCallback(self.bfDotaBtnTimer)
            self.bfDotaBtnTimer = 0
        if self.mapMed:
            gcd = DCD.data.get('bfDotaBtnGcd', 5)
            self.mapMed.Invoke('playCooldown', (GfxValue(gcd * 1000), GfxValue(0)))
            self.bfDotaBtnTimer = BigWorld.callback(gcd, self.endBfDotaBtnsCoolDown)

    def endBfDotaBtnsCoolDown(self):
        self.bfDotaBtnTimer = 0
        if self.mapMed:
            self.mapMed.Invoke('stopCooldown')

    def showBfDotaBtns(self, x, y):
        if not self.mapMed:
            return
        keyDesArr = []
        keyDesArr.append(HK.HKM[HK.KEY_DOTA_MAP_MARK].getBrief())
        keyDesArr.append(HK.HKM[HK.KEY_DOTA_MAP_ATK].getBrief())
        keyDesArr.append(HK.HKM[HK.KEY_DOTA_MAP_RETREAT].getBrief())
        keyDesArr.append(HK.HKM[HK.KEY_DOTA_MAP_GATHER].getBrief())
        info = {}
        info['pos'] = [x, y]
        info['keyDes'] = keyDesArr
        self.mapMed.Invoke('showBfDotaButtons', uiUtils.dict2GfxDict(info, True))

    def hideBfDotaBtns(self):
        if not self.mapMed:
            return
        self.mapMed.Invoke('hideBfDotaButtons')

    def onBfDotaButtonClick(self, *args):
        name = args[3][0].GetString()
        if name == 'attackBtn':
            self.signalType = uiConst.SIGNAL_TYPE_ATK
        elif name == 'retreatBtn':
            self.signalType = uiConst.SIGNAL_TYPE_RETREAT
        else:
            self.signalType = uiConst.SIGNAL_TYPE_GATHER
        p = BigWorld.player()
        self.doSendPos(p.position[0], p.position[2])

    def InvokeProcessBfDotaClick(self, key):
        if not self.mapMed:
            return
        p = BigWorld.player()
        if not p.bianshen[1]:
            return
        gcd = DCD.data.get('bfDotaBtnGcd', 5)
        if utils.getNow() - self.lastBfDotaBtnTime < gcd:
            return
        if key in KEY_BTN_NAME_MAP:
            if key == HK.KEY_DOTA_MAP_MARK:
                if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE and not p.ap.showCursor:
                    p.ap._changeCursor(False)
            self.mapMed.Invoke('processBfDotaBtnClick', GfxValue(KEY_BTN_NAME_MAP[key]))

    def onIsInBfDota(self, *args):
        return GfxValue(BigWorld.player().isInBfDota())

    def onIsInWingWorldCityWar(self, *args):
        return GfxValue(BigWorld.player().inWingWarCity())

    def onTransPos(self, *args):
        return self.doTransPos(*args)

    def doTransPos(self, *args):
        x = args[3][0].GetNumber()
        y = args[3][1].GetNumber()
        posData = ASObject(args[3][2])
        mapRect = ASObject(args[3][3])
        newX = (x * posData[4] / posData[6] + posData[8] - posData[0]) * (mapRect[2] - mapRect[0]) / posData[2] + mapRect[0]
        newY = (posData[9] - y * posData[5] / posData[7] - posData[1]) * (mapRect[3] - mapRect[1]) / posData[3] + mapRect[1]
        if self.debugPosX != None:
            newX = self.debugPosX
            gamelog.info('jbx:littleMap formula X %f = ((%f/posData[6] + posData[8]) - %f)*%f + %f' % (newX,
             x * posData[4],
             posData[0],
             (mapRect[2] - mapRect[0]) / posData[2],
             mapRect[0]))
        if self.debugPosY != None:
            newY = self.debugPosY
            gamelog.info('jbx:littleMap formula Y %f = ((posData[9] - %f/posData[7]) - %f) * %f + %f' % (newY,
             y * posData[5],
             posData[1],
             (mapRect[3] - mapRect[1]) / posData[3],
             mapRect[1]))
        if self.isLogPos:
            gamelog.info('jbx:littleMap Pox', newX, newY)
        return uiUtils.array2GfxAarry([newX, newY])

    def refreshPlayerMapInfo(self):
        if BigWorld.player() and self.mapMed:
            color = 'yellow'
            chunckName = BigWorld.ChunkInfoAt(BigWorld.player().position)
            mapName = formula.whatLocationName(BigWorld.player().spaceNo, chunckName)
            if not BigWorld.player().inFuben():
                fortId = CMD.data.get(chunckName, {}).get('fortId')
                if fortId and self.isOwnerGuild(fortId):
                    mapName = gameStrings.TEXT_LITTLEMAPPROXY_2726 + '-' + mapName
                elif fortId:
                    mapName = gameStrings.TEXT_LITTLEMAPPROXY_2728 + '-' + mapName
            color = self.getAreaColor()
            if self.mapMed:
                self.mapMed.Invoke('refreshMapPosInfo', (GfxValue(round(BigWorld.player().position[0])),
                 GfxValue(round(BigWorld.player().position[2])),
                 GfxValue(round(BigWorld.player().position[1])),
                 GfxValue(gbk2unicode(mapName)),
                 GfxValue(color)))

    def getAreaColor(self):
        p = BigWorld.player()
        mapId = formula.getMapId(p.spaceNo)
        mData = MCD.data.get(mapId)
        limitPk = mData and mData.get('limitPk', 0)
        noPkPunish = mData and mData.get('noPkPunish', 0)
        inBigWorld = p.spaceNo == const.SPACE_NO_BIG_WORLD
        color = 'yellow'
        if gameChunk.resideInSafetyZone(p) or not inBigWorld and limitPk:
            color = 'green'
        elif gameChunk.resideInFreePk(p) or not inBigWorld and not limitPk and noPkPunish:
            color = 'red'
        return color

    def isOwnerGuild(self, fortId):
        p = BigWorld.player()
        fort = p.clanWar.fort.get(fortId, {})
        if p.guildNUID != 0 and fort and fort.ownerGuildNUID == p.guildNUID:
            return True
        return False

    def onGetMapNameTip(self, *arg):
        color = arg[3][0].GetString()
        if color == 'red':
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE2, {}).get('text', '')
        elif color == 'green':
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE1, {}).get('text', '')
        else:
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE3, {}).get('text', '')
        return GfxValue(gbk2unicode(ret))

    def onEndSetMapLv(self, *args):
        self.refreshAllPUBGUI()

    def getLittleMapNoByPos(self, positionY, spaceNo = None):
        spaceNo = BigWorld.player().spaceNo if not spaceNo else spaceNo
        chunkName = BigWorld.ChunkInfoAt(BigWorld.player().position)
        mapNo = self.getMapName(chunkName, spaceNo, positionY)
        return mapNo

    def refreshWorldBossIcon(self):
        if not self.mapMed:
            return
        if not worldBossHelper.getInstance().isInWorldBossActivity():
            self.addOtherItems({uiConst.MAP_ICON_WORLD_BOSS: []})
            return
        if not formula.inWorld(BigWorld.player().spaceNo):
            return
        ret = []
        bossDict = worldBossHelper.getInstance().getWorldBossInfos()
        for refId in bossDict:
            bossInfo = bossDict.get(refId, {})
            if not bossInfo:
                continue
            self.appendWorldBossInfo(bossInfo, ret)

        self.addOtherItems({uiConst.MAP_ICON_WORLD_BOSS: ret})

    def appendWorldBossInfo(self, bossInfo, ret):
        isLive = bossInfo.get('isLive', False)
        if not isLive:
            return
        else:
            pos = bossInfo.get('position', None)
            if not pos:
                return
            tipText = gameStrings.WORLD_BOSS_MAP_TIP % bossInfo.get('bossName', '')
            mapData = MapItemData(ICON_TYPE_OTHER, pos[0], pos[2], data=(bossInfo.get('mapLittleIcon', ''), 0, 0), tips=tipText, areaNo=self.curMapNo)
            ret.append(mapData)
            return

    def onIsInPUBG(self, *args):
        p = BigWorld.player()
        if p:
            return GfxValue(p.isInPUBG())
        else:
            return GfxValue(False)

    def refreshAllPUBGUI(self):
        self.refreshAllMarksIconInPUBG()
        self.refreshPoisonInPubg()
        self.setPlayerIconInPUBG()
        self.startSetAirPlaneLine()
        self.refreshDisasterIconInPUBG()
        self.refreshBossInPubg()
        self.refreshTreasureBoxInPubg()

    def refreshPoisonInPubg(self):
        self.pubgPoisonRefreshHandleCB and BigWorld.cancelCallback(self.pubgPoisonRefreshHandleCB)
        if not self.mapMed:
            return
        p = BigWorld.player()
        if p.isInPUBG() and p.curPoisonCircleData:
            self.pubgPoisonRefreshHandleCB = BigWorld.callback(pubgUtils.POISON_REFRESH_INTERVAL, self.refreshPoisonInPubg)
        self.setCurPoisonCircle()

    def setCurPoisonCircle(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        poisonData = dict()
        if p.isInPUBG() and p.curPoisonCircleData:
            nextCenterStage, nextCenterStamp, curCenterPos, nextCenterPos = p.curPoisonCircleData
            curPoisonAreaPos = p.getCurPoisonCirclePos(nextCenterStage, nextCenterStamp, curCenterPos, nextCenterPos)
            curPoisonAreaRadius = p.getCurPoisonCircleRadius(nextCenterStage, nextCenterStamp)
            curSafeAreaPos = list(nextCenterPos)
            curSafeAreaRadius = p.getNextSafeCircleRadius(nextCenterStage)
            poisonVisible = True
            poisonData['poisonCirclePos'] = curPoisonAreaPos
            poisonData['poisonCircleRadius'] = curPoisonAreaRadius
            poisonData['whiteCirclePos'] = curSafeAreaPos
            poisonData['whiteCircleRadius'] = curSafeAreaRadius
            poisonData['circleEdgeNums'] = DCD.data.get('pubgCircleEdgeNums', 32)
        else:
            poisonVisible = False
        self.mapMed.Invoke('refreshPubgPoisonCircle', (GfxValue(poisonVisible), uiUtils.dict2GfxDict(poisonData, True)))

    def setAirPlaneLinePath(self, planePath):
        self.pubgAirPlanePath = planePath
        if self.pubgAirPlanePath:
            airPlaneStartPos, airPlaneEndPos = self.pubgAirPlanePath
            self.pubgAirlineRotation = (Math.Vector3(airPlaneEndPos) - Math.Vector3(airPlaneStartPos)).yaw / math.pi * 180
            xOffset = abs(float(airPlaneStartPos[0] - airPlaneEndPos[0]))
            zOffset = abs(float(airPlaneStartPos[2] - airPlaneEndPos[2]))
            self.pubgAirlineWidth = math.sqrt(xOffset * xOffset + zOffset * zOffset)
        if not self.mapMed:
            return
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
        if not self.mapMed:
            return
        p = BigWorld.player()
        airlineData = dict()
        if p.isInPUBG() and isShow and self.pubgAirPlanePath:
            airPlaneStartPos, airPlaneEndPos = self.pubgAirPlanePath
            airPlanePos = BigWorld.player().getCurAirPlanePos()
            airlineData['airlineMain'] = [airPlaneStartPos[0],
             airPlaneStartPos[2],
             self.pubgAirlineRotation - 90,
             self.pubgAirlineWidth]
            airlineData['airlineStart'] = [airPlaneStartPos[0], airPlaneStartPos[2], self.pubgAirlineRotation]
            airlineData['airlineEnd'] = [airPlaneEndPos[0], airPlaneEndPos[2], self.pubgAirlineRotation]
            airlineData['airPlane'] = [airPlanePos[0], airPlanePos[2], self.pubgAirlineRotation]
        self.mapMed.Invoke('refreshPubgAirline', (GfxValue(isShow), uiUtils.dict2GfxDict(airlineData, True)))

    def setPUBGUIMc(self, isInPUBG = False):
        self.pubgPoisonTimeRefreshHandleCB and BigWorld.cancelCallback(self.pubgPoisonTimeRefreshHandleCB)
        p = BigWorld.player()
        if pubgUtils.PUBG_STATE_PROGRESS_PREPARE <= p.curPUBGStateProgress <= pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE_FORCE_DROP:
            isInPlane = True
        else:
            isInPlane = False
        info = dict()
        info['isInPUBG'] = isInPUBG
        if isInPUBG:
            info['isInPlane'] = isInPlane
            if isInPlane:
                if p.curPUBGStateProgress == pubgUtils.PUBG_STATE_PROGRESS_PREPARE:
                    numsInAirPlaneStr = DCD.data.get('pubgLittleMapUIPrepareNameTxt', gameStrings.TEXT_LITTLEMAPPROXY_2922)
                else:
                    numsInAirPlaneStr = DCD.data.get('pubgLittleMapUIPlaneNameTxt', gameStrings.TEXT_LITTLEMAPPROXY_2924)
                info['numsInAirPlane'] = gameStrings.PUBG_LITTLE_MAP_PREPARE_AND_PLANE_NUM % (numsInAirPlaneStr, p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IN_PLANE_IDX])
            elif p.curPoisonCircleData:
                info['nextTimeShrinkPoisonUIVisible'] = True
                poisonDataDict = p.getPoisonCircleData(p.curPoisonCircleData[0], p.curPoisonCircleData[1])
                poisonState = poisonDataDict['poisonState']
                info['leftTime'] = poisonDataDict['leftTime']
                info['allTime'] = poisonDataDict['allTime']
                info['leftTimeStr'] = poisonDataDict['leftTimeStr']
                if poisonState == pubgUtils.PUBG_POISON_STATE_HOLD:
                    self.pubgPoisonTimeRefreshHandleCB = BigWorld.callback(1, Functor(self.setPUBGUIMc, p.isInPUBG()))
                    info['nextTimeShrinkPoisonName'] = DCD.data.get('pubgLittleMapUIShrinkPoisonNameTxt1', '')
                elif poisonState == pubgUtils.PUBG_POISON_STATE_SHRINK:
                    self.pubgPoisonTimeRefreshHandleCB = BigWorld.callback(1, Functor(self.setPUBGUIMc, p.isInPUBG()))
                    info['nextTimeShrinkPoisonName'] = DCD.data.get('pubgLittleMapUIShrinkPoisonNameTxt2', '')
                elif poisonState == pubgUtils.PUBG_POISON_STATE_END:
                    info['nextTimeShrinkPoisonUIVisible'] = False
            else:
                info['nextTimeShrinkPoisonUIVisible'] = False
        info['leftNums'] = p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IDX]
        info['killNums'] = p.curPUBGNumsData[pubgUtils.PUBG_KILL_NUM_IDX]
        self.mapMed and self.mapMed.Invoke('showPubgUI', uiUtils.dict2GfxDict(info, True))

    def refreshAllMarksIconInPUBG(self):
        if not self.mapMed:
            return
        else:
            p = BigWorld.player()
            mapMarkData = []
            for gbId, teammateMarkData in p.allTeammateMapMark.iteritems():
                posInWorld = teammateMarkData.get('posInWorld', None)
                littleMapNo = teammateMarkData.get('littleMapNo', None)
                teammateNo = p.getTeammateNoInPUBG(gbId)
                if teammateNo and posInWorld and littleMapNo:
                    item = MapItemData(ICON_TYPE_PUBG_TEAMMATE_MARK, posInWorld[0], posInWorld[2], data=('LittleMap_PubgTeammateMark', teammateNo))
                    mapMarkData.append(self.itemDataToGfx(item))

            self.mapMed.Invoke('refreshPubgTeammateList', uiUtils.array2GfxAarry(mapMarkData, True))
            return

    def refreshDisasterIconInPUBG(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        mapDisasterData = list()
        if p.curDisasterDataInPUBG:
            posInWorld = p.curDisasterDataInPUBG['posInWorld']
            radius = DCD.data.get('pubgDestroyDisasterRadius', 0)
            item = MapItemData(ICON_TYPE_OTHER, posInWorld[0], posInWorld[2], data=('LittleMap_PubgDisaster',), radii=radius, areaNo=self.curMapNo)
            mapDisasterData.append(item)
        self.addOtherItems({uiConst.MAP_ICON_BATTLE_PUBG_DISASTER: mapDisasterData})

    def refreshBossInPubg(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        mapBossData = list()
        if p.curBossInPUBG:
            for bossPos in p.curBossInPUBG.itervalues():
                item = MapItemData(ICON_TYPE_OTHER, bossPos[0], bossPos[2], data=('LittleMap_PubgBoss',), areaNo=self.curMapNo)
                mapBossData.append(item)

        self.addOtherItems({uiConst.MAP_ICON_BATTLE_PUBG_BOSS: mapBossData})

    def refreshTreasureBoxInPubg(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        mapTreasureBoxData = list()
        treasureBoxPosInWorld = p.curTreasureBoxInPUBG.get('posInWorld', [])
        startStamp = p.curTreasureBoxInPUBG.get('startStamp', 0)
        if treasureBoxPosInWorld and startStamp:
            item = MapItemData(ICON_TYPE_OTHER, treasureBoxPosInWorld[0], treasureBoxPosInWorld[2], data=('LittleMap_PubgTreasureBox',), areaNo=self.curMapNo)
            mapTreasureBoxData.append(item)
        self.addOtherItems({uiConst.MAP_ICON_BATTLE_PUBG_TREASURE_BOX: mapTreasureBoxData})

    def setPlayerIconInPUBG(self):
        if not self.mapMed:
            return
        p = BigWorld.player()
        if p.isInPUBG():
            playerIconData = {'isInPUBG': True,
             'myTeammateNo': p.getMyTeammateNo()}
            self.mapMed.Invoke('setPlayerIcon', (GfxValue(''), uiUtils.dict2GfxDict(playerIconData, True)))


class MapItemData(object):

    def __init__(self, itemType, x, y, data = None, entityId = None, trackIndex = None, radii = None, tips = None, areaNo = None, pos = None, needCombatEffect = False, tweenInterVal = 0):
        self.itemType = itemType
        self.x = x
        self.y = y
        self.data = data
        self.entityId = entityId
        self.trackIndex = trackIndex
        self.radii = radii
        self.tips = tips
        self.areaNo = areaNo
        self.pos = pos
        self.needCombatEffect = needCombatEffect
        self.tweenInterVal = tweenInterVal

    def toGfxData(self):
        gfxData = {'type': self.itemType,
         'x': self.x,
         'y': self.y}
        if self.entityId:
            gfxData['entityId'] = self.entityId
        if self.data:
            gfxData['data'] = self.data
        if self.radii:
            gfxData['radii'] = self.radii
        if self.trackIndex:
            gfxData['trackIndex'] = self.trackIndex
        if self.tips:
            gfxData['tips'] = self.tips
        if self.pos:
            gfxData['pos'] = self.pos
        if self.needCombatEffect:
            gfxData['needCombatEffect'] = self.needCombatEffect
        if gameglobal.rds.configData.get('enableDotaHeroTweenPos', False):
            if self.tweenInterVal:
                gfxData['tweenInterVal'] = self.tweenInterVal
        return uiUtils.dict2GfxDict(gfxData, True)


class NpcPosUnits(object):

    def __init__(self, mapNo):
        self.mapNo = mapNo
        self.gfxItems = []
        self.seekerIds = []
        tmpIds = []
        for seekId in AD.data.get(mapNo, {}).get('seekId', []):
            tmpIds.append(seekId)
            if len(tmpIds) >= NPC_POS_UNIT_NUM:
                self.seekerIds.append(tmpIds)
                tmpIds = []

        if tmpIds:
            self.seekerIds.append(tmpIds)

    def getCurrent(self):
        if len(self.seekerIds):
            return self.seekerIds[0]

    def getCurrentNpcIds(self):
        seekIds = self.getCurrent()
        npcIds = []
        if seekIds:
            for seekId in seekIds:
                if SD.data.get(seekId, {}).get('type', '').lower() == 'npc':
                    npcId = SD.data.get(seekId, {}).get('npcId', 0)
                    if npcId:
                        npcIds.append(npcId)

        return npcIds

    def next(self):
        if len(self.seekerIds):
            self.seekerIds.pop(0)

    def isEmpty(self):
        return len(self.seekerIds) == 0

    def clear(self):
        self.seekerIds = []
        self.gfxItems = []

    def addGfxItems(self, items):
        self.gfxItems.extend(items)
