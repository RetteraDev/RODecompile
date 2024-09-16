#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMapGame.o
import const
import gametypes
import utils
import gameglobal
import gamelog
import BigWorld
from helpers import tintalt as TA
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import map_game_config_data as MGCD
from data import sys_config_data as SCD
from helpers.mapGrid import MapGrid, MapGridVal

class ImpMapGame(object):

    def _initMapGameGrid(self):
        self.grids = MapGrid()
        self.bossBuff = set()
        self.playerBuff = set()
        self.spriteBuff = set()

    def onSyncMapGameGraveState(self, state):
        gamelog.debug('yedawang### onSyncMapGameGraveState state', state)
        gameglobal.rds.ui.mapGameMapV2.setBossState(state)
        entityList = []
        for entity in BigWorld.entities.values():
            entityCls = entity.__class__.__name__
            if entityCls in ('Npc', 'Dawdler') or entityCls in ('Monster', 'AvatarMonster') and not BigWorld.player().isEnemy(entity):
                if hasattr(entity, '_isMarkerNpc') and entity._isMarkerNpc():
                    continue
                if hasattr(entity, 'getOpacityValue'):
                    opacityValue = entity.getOpacityValue()
                    if opacityValue[0] == gameglobal.OPACITY_FULL:
                        entityList.append(entity)
                else:
                    entityList.append(entity)

        if state:
            msg = MGCD.data.get('MAP_GAME_DEFEAT_FINISH', '')
            self.graveScenarioPlay(msg)
            for entity in entityList:
                ghostTint = SCD.data.get('ghostmatte', 'refaction002')
                TA.ta_reset(entity.allModels)
                TA.ta_add(entity.allModels, ghostTint, tintType=TA.NPC_LINGSHI)

        else:
            for entity in entityList:
                TA.ta_reset(entity.allModels)

    def onUpdateMapGameBasicInfo(self, dto, extra):
        gamelog.debug('yedawang### onUpdateMapGameBasicInfo', dto)
        if not hasattr(self, 'grids'):
            self._initMapGameGrid()
        self.grids.fromClientDTO(dto)
        if gameglobal.rds.configData.get('enableMapGameV2'):
            gameglobal.rds.ui.mapGameMapV2.setRankData(extra['enterCntRank'], extra['callAttackRank'])
            gameglobal.rds.ui.mapGameEvent.setFinishedEvent(extra['finishedEvent'])
            gameglobal.rds.ui.mapGameMapV2.refreshInfo()
        if gameglobal.rds.configData.get('enableMapGame'):
            gameglobal.rds.ui.mapGameMap.refreshInfo()

    def onUpdateMapGameDetailInfo(self, gridId, dto):
        gamelog.debug('yedawang### onUpdateMapGameDetailInfo', gridId, dto)
        if dto is None:
            return
        else:
            if not hasattr(self, 'grids'):
                self._initMapGameGrid()
            if not self.grids.has_key(gridId):
                self.grids[gridId] = MapGridVal(gridId)
            self.grids[gridId].fromClientDTO(dto, simple=False)
            if gridId == MGCD.data.get('mapGameBossGridIdList', {}).get('fakeBoss', 20):
                gameglobal.rds.ui.mapGameMapV2.refreshFakeBoss()
            gridContentId = MGGPD.data.get(gridId, {}).get('contentId')
            gridType = MGGD.data.get(gridContentId).get('type')
            gameglobal.rds.ui.mapGameMap.refreshGrid(gridId)
            if gridType == gametypes.MAP_GAME_GRID_TYPE_BOSS:
                gameglobal.rds.ui.mapGameBoss.refreshInfo()
            elif gridType in gametypes.FIGHT_MAP_LIST:
                gameglobal.rds.ui.mapGameFight.refreshInfo()
            elif gridType in gametypes.DONATE_MAP_LIST:
                gameglobal.rds.ui.mapGameDonate.refreshInfo()
            elif gridType == gametypes.MAP_GAME_GRID_TYPE_BUFF:
                gameglobal.rds.ui.mapGameBuff.refreshInfo()
            return

    def onUpdateMapGameBuff(self, bossBuff, playerBuff, spriteBuff):
        if not hasattr(self, 'grids'):
            self._initMapGameGrid()
        self.bossBuff.clear()
        self.playerBuff.clear()
        self.spriteBuff.clear()
        self.bossBuff.update(bossBuff)
        self.playerBuff.update(playerBuff)
        self.spriteBuff.update(spriteBuff)
        gameglobal.rds.ui.mapGameBoss.refreshBuffList()
        gameglobal.rds.ui.mapGameMap.refreshDetailMc()

    def onMapGameBossKilled(self, gridId, bossName):
        gamelog.debug('yedawang### onMapGameBossKilled', gridId, bossName)
        msg = MGCD.data.get('MAP_GAME_BOSS_FINISH', '')
        gameglobal.rds.ui.mapGameFinish.show(True, msg)

    def set_mapGameClientGmState(self, old):
        if gameglobal.rds.configData.get('enableMapGameV2'):
            gameglobal.rds.ui.mapGameMapV2.showGMInfo(isShow=bool(self.mapGameClientGmState))

    def onGetMapGameEventReward(self, eventId):
        if gameglobal.rds.configData.get('enableMapGameV2'):
            gameglobal.rds.ui.mapGameEvent.refreshInfo()
