#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorld.o
from gamestrings import gameStrings
import BigWorld
import Pixie
import formula
import gameglobal
from sfx import sfx
import gamelog
import const
import utils
import cPickle
import keys
import zlib
import gametypes
import appSetting
import wingWorldUtils
import clientUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from commonWorldWar import WWArmyCandidateVal, WWArmyPostVal, WWArmySkillVal
import logicInfo
from guis import uiUtils
from guis import uiConst
from helpers.sceneInfo import AreaInfo
from helpers.wingWorld import WingWorldCityMinMap, WingWorldCityWorldMap, WingHostResourcePointMap, WingWorld, pathFinding
from data import wing_world_config_data as WWCD
from data import wing_world_city_data as WWCTD
from data import game_msg_data as GMD
from data import region_server_config_data as RSCD
from data import wing_world_celebration_reward_data as WWCRD
from cdata import game_msg_def_data as GMDD
from data import skill_general_data as SGD
SOUL_BOSS_PUSHMSG_TYPE_START = 11531
SOUL_BOSS_PUSHMSG_TYPE_END = 11538

class ImpWingWorld(object):

    def inWingCity(self):
        return formula.spaceInWingCity(self.spaceNo)

    def inWingBornIsland(self):
        return formula.spaceInWingBornIsland(self.spaceNo)

    def inWingPeaceCity(self):
        return formula.spaceInWingPeaceCity(self.spaceNo)

    def inWingCityOrBornIsland(self):
        return self.inWingBornIsland() or self.inWingCity()

    def inWingPeaceCityOrBornIsland(self):
        return self.inWingPeaceCity() or self.inWingBornIsland()

    def onQueryWingWOpenInfo(self, openStage, isOpen, openDonate, openDonateLimit):
        """
        
        Args:
            openStage: \xe9\x98\xb6\xe6\xae\xb5 1 - 12
            isOpen: \xe9\x98\xb6\xe6\xae\xb5\xe5\xb0\x81\xe5\x8d\xb0\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xbe\xe7\x8e\xb0 bool
            openDonate:  \xe5\xbd\x93\xe5\x89\x8d\xe7\xa0\xb4\xe5\xb0\x81\xe5\x80\xbc
            openDonateLimit: \xe5\xbd\x93\xe5\x89\x8d\xe7\xa0\xb4\xe5\xb0\x81\xe4\xb8\x8a\xe9\x99\x90
        
        Returns:
        
        """
        if not hasattr(self, 'wingWorldOpenedStage') or self.wingWorldOpenedStage != openStage - 1:
            self.wingWorldOpenedStage = openStage - 1
            AreaInfo.getInstance().modifySkyBox()
            self.setDynamicSkybox(formula.getMapId(self.spaceNo))
        gameglobal.rds.ui.wingWorldRemoveSeal.onQueryInfo(openStage, isOpen, openDonate, openDonateLimit)
        gameglobal.rds.ui.wingWorld.onGetWingWorldOpenProgress(openStage, isOpen, openDonate, openDonateLimit)

    def onQueryWingWorldStats(self, damageVal, cureVal):
        """
        
        Args:
            damageVal:  \xe5\x9c\xa8\xe6\x89\x93Boss\xe4\xb8\xad\xe7\x9a\x84\xe4\xbc\xa4\xe5\xae\xb3\xe5\x80\xbc
            cureVal:   \xe5\x9c\xa8\xe6\x89\x93Boss\xe4\xb8\xad\xe7\x9a\x84\xe6\xb2\xbb\xe7\x96\x97\xe9\x87\x8f
        
        Returns:
        
        """
        gameglobal.rds.ui.wingWorldPreTaskTip.show(damageVal, cureVal)

    def onQueryWingWorldBossInfo(self, createWWBossTime, mlgNo):
        """
        
        Args:
            createWWBossTime: \xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\x96\xe7\x95\x8cboss\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4
            mlgNo: \xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\x96\xe7\x95\x8cBoss\xe7\x9a\x84\xe5\x9c\xb0\xe5\xae\xab\xe7\xbb\x84
        
        Returns:
        
        """
        self.wwBossMlgNo = mlgNo
        self.createWWBossTime = createWWBossTime
        self.destroyWWBossTime = createWWBossTime + const.TIME_INTERVAL_HOUR
        gameglobal.rds.ui.pushActivity.addWingWorldBossPush(self.createWWBossTime, self.destroyWWBossTime)
        if createWWBossTime - utils.getNow() > const.WINGWORLD_BOSS_SHOWMSG_REMAIN_TIME:
            self.showGameMsg(GMDD.data.WINGWORLD_BOSS_SECOND_SHOWGAMEMSG, ())

    def onQueryWingWorldDiGongTime(self, destroyDiGongTime, mlgNo):
        """
        
        Args:
            destroyDiGongTime: \xe9\x94\x80\xe6\xaf\x81\xe5\x9c\xb0\xe5\xae\xab\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4
        
        Returns:
        
        """
        self.wwBossMlgNo = mlgNo
        self.createWWBossTime = getattr(self, 'createWWBossTime', self.getServerTime())
        self.destroyWWBossTime = self.getServerTime()
        self.destroyDiGongTime = destroyDiGongTime
        gameglobal.rds.ui.pushActivity.updateWingWorldBossPush(self.createWWBossTime, self.destroyWWBossTime, destroyDiGongTime)
        self.cell.queryWingWorldOpenStageInfo()

    def notifyWingWorldBossDie(self, destroyDiGongTime):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe5\xbc\x80\xe9\x97\xa8\xe5\xbc\x82\xe4\xb8\x96\xe7\x95\x8cBoss\xe5\xb7\xb2\xe7\xbb\x8f\xe6\xad\xbb\xe4\xba\xa1
        Returns:
        
        """
        self.showGameMsg(GMDD.data.WINGWORLD_BOSS_DIE, ())
        self.createWWBossTime = getattr(self, 'createWWBossTime', self.getServerTime())
        self.destroyWWBossTime = self.getServerTime()
        self.destroyDiGongTime = destroyDiGongTime
        gameglobal.rds.ui.pushActivity.updateWingWorldBossPush(self.createWWBossTime, self.destroyWWBossTime, destroyDiGongTime)
        self.cell.queryWingWorldOpenStageInfo()

    def onWingWorldSubmitOk(self, openDonate):
        """
        \xe7\xa2\x8e\xe7\x89\x87\xe6\x8f\x90\xe4\xba\xa4\xe6\x88\x90\xe5\x8a\x9f
        """
        gameglobal.rds.ui.wingWorldRemoveSeal.onDonateSuccess(openDonate)

    def onInitWingWorld(self, dto, briefVer, countryVer, cityVer, campVer, countryData, peaceCityData, warCityData, campData, otherData):
        gamelog.debug('onInitWingWorld', dto, countryData, peaceCityData, warCityData)
        self.wingWorld.state, self.wingWorld.step, self.wingWorld.opennessLevel, self.wingWorld.trendId = dto
        self.wingWorld.briefVer = briefVer
        self.wingWorld.countryVer = countryVer
        self.wingWorld.campVer = campVer
        self.wingWorld.cityVer = cityVer
        self.wingWorld.city.fromDTO(peaceCityData)
        self.wingWorld.city.fromDTO(warCityData)
        self.wingWorld.country.fromDTO(countryData)
        self.wingWorld.camp.fromDTO(campData)
        gameglobal.rds.ui.wingWorldPush.checkState()
        self.checkWingWorldContinuePathFinding()
        gameglobal.rds.ui.wingCombatPush.onWingWorldStepChange()

    def checkWingWorldContinuePathFinding(self):
        gamelog.debug('@navigator checkWingWorldContinuePathFinding 1', self.wingWorld.pendingSeekPoint, len(self.wingWorld.city.cityVals[const.WING_CITY_TYPE_PEACE]))
        if not hasattr(self, 'lastTeleportPos'):
            return
            gamelog.debug('@navigator checkWingWorldContinuePathFinding 2', self.wingWorld.pendingSeekPoint, len(self.wingWorld.city.cityVals[const.WING_CITY_TYPE_PEACE]))
        if not self.wingWorld.city.cityVals[const.WING_CITY_TYPE_PEACE]:
            gamelog.debug('@navigator checkWingWorldContinuePathFinding 3', self.wingWorld.pendingSeekPoint, len(self.wingWorld.city.cityVals[const.WING_CITY_TYPE_PEACE]))
            return
        else:
            if self.wingWorld.pendingSeekPoint:
                gamelog.debug('@navigator checkWingWorldContinuePathFinding 4', self.wingWorld.pendingSeekPoint, len(self.wingWorld.city.cityVals[const.WING_CITY_TYPE_PEACE]))
                seekPoint = self.wingWorld.pendingSeekPoint
                self.wingWorld.pendingSeekPoint = None
                pathFinding(seekPoint, bDelayed=True)
            return

    def onWingWorldContinuePathFinding(self, seekPoint):
        gamelog.debug('@navigator onWingWorldContinuePathFinding', seekPoint)
        self.wingWorld.pendingSeekPoint = seekPoint
        self.checkWingWorldContinuePathFinding()

    def onWingWorldSeasonCombatLevel(self, step, level):
        gamelog.debug('onWingWorldSeasonCombatLevel', step, self.wingWorld.step, level)
        self.wingWorld.step = step
        self.onWingWorldStepChange(step)

    def onWingWorldSeasonCelebration(self, step):
        gamelog.debug('onWingWorldSeasonCelebration', step, self.wingWorld.step)
        self.wingWorld.step = step
        self.onWingWorldStepChange(step)

    def onWingWorldSeasonAdjourning(self, step):
        gamelog.debug('onWingWorldSeasonAdjourning', step, self.wingWorld.step)
        self.wingWorld = WingWorld()
        self.wingWorld.step = step
        self.onWingWorldStepChange(step)

    def onWingWorldStepChange(self, step):
        gamelog.info('jbx:onWingWorldStepChange', step)
        self.notifyWingWorldStep = 0
        msgId, picId, soundId = WWCD.data.get('wingWorldStepChangeMsgs', {}).get(step, (0, 0, 0))
        picId and gameglobal.rds.ui.showPicTip(picId)
        msgId and self.showGameMsg(msgId, ())
        soundId and gameglobal.rds.sound.playSound(soundId)
        gameglobal.rds.ui.wingCombatPush.onWingWorldStepChange()

    def onWingWorldStartDeclare(self, state):
        gamelog.debug('onWingWorldStartDeclare', state, self.wingWorld.state)
        self.wingWorld.state = state
        gameglobal.rds.ui.wingWorldStrategy.refreshInfo()
        gameglobal.rds.ui.wingWorldPush.checkState()

    def onWingWorldEndDeclare(self, state):
        gamelog.debug('onWingWorldEndDeclare', state, self.wingWorld.state)
        self.wingWorld.state = state
        gameglobal.rds.ui.wingWorldPush.checkState()

    def onWingWorldOpen(self, state):
        gamelog.debug('onWingWorldOpen', state, self.wingWorld.state)
        self.wingWorld.state = state
        gameglobal.rds.ui.wingWorldPush.checkState()

    def onWingWorldSettlement(self, state):
        gamelog.debug('onWingWorldSettlement', state, self.wingWorld.state)
        self.wingWorld.state = state
        if state == gametypes.WING_WORLD_STATE_FINISH and not getattr(self, 'hadWWResultShow', False):
            gameglobal.rds.ui.wingWorldDetailInfo.show()
            self.hadWWResultShow = True

    def onWingWorldFinished(self, state):
        gamelog.debug('onWingWorldFinished', state, self.wingWorld.state)
        self.wingWorld.state = state
        if state == gametypes.WING_WORLD_STATE_FINISH and not getattr(self, 'hadWWResultShow', False):
            gameglobal.rds.ui.wingWorldDetailInfo.show()
            self.hadWWResultShow = True

    def onWingWorldReset(self, state):
        gamelog.debug('onWingWorldReset', state, self.wingWorld.state)
        self.wingWorld.state = state

    def onWingWorldDeclareCity(self, cityId, cityDTO, countryDTO, isCamp):
        gamelog.debug('onWingWorldDeclareCity', cityId, isCamp)
        city = self.wingWorld.city.getCity(cityDTO[0], cityDTO[1])
        city.fromDTO(cityDTO)
        country = self.wingWorld.country.getCountry(countryDTO[0])
        country.fromDTO(countryDTO)
        gameglobal.rds.ui.wingWorldStrategy.refreshInfo()

    def onWingWorldOpenAttackCity(self, hostId, cityId):
        gamelog.debug('jbx:onWingWorldOpenAttackCity', self.spaceNo, hostId, cityId, gameglobal.rds.ui.wingWorldTransport.gotoCityId)
        if self.isWingWorldCampMode():
            camp = self.wingWorld.country.getCamp(hostId)
            camp.openAttack(cityId)
        else:
            country = self.wingWorld.country.getCountry(hostId)
            country.openAttack(cityId)
        city = self.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId)
        city.openAttack(hostId)
        gameglobal.rds.ui.wingWorldPush.checkState()
        if not self.isWingWorldCampMode() or hostId == self.wingWorldCamp:
            cityName = WWCTD.data.get(cityId, {}).get('name', str(cityId))
            self.showGameMsg(GMDD.data.WING_WORLD_ATTACK_CONFIRM, (cityName,))
            if gameglobal.rds.ui.wingWorldTransport.gotoCityId:
                self.teleportToWingWarCity(gameglobal.rds.ui.wingWorldTransport.gotoCityId)
                gameglobal.rds.ui.wingWorldTransport.gotoCityId = 0
                return

    def onWingWorldCityOpennessLevelUpgrade(self, isFromWingWorld, hostId, opennessLevel):
        gamelog.debug('@hxm onWingWorldCityOpennessLevelUpgrade>>>', isFromWingWorld, hostId, opennessLevel, self.spaceNo)
        if not isFromWingWorld and formula.spaceInWingCity(self.spaceNo):
            return
        gamelog.debug('@hxm onWingWorldCityOpennessLevelUpgrade client show>>>')

    def onWingWorldSetCountryFlag(self, hostId, flagId):
        gamelog.debug('@hxm onWingWorldSetCountryFlag>>>', hostId, flagId)
        country = self.wingWorld.country.getCountry(hostId)
        country.setFlagId(flagId)
        gameglobal.rds.ui.wingWorldWarFlag.refreshInfo()
        gameglobal.rds.ui.wingWorldOverView.updateCountryIcon()

    def onQueryWingWorldResume(self, dto, briefVer, countryVer, cityVer, countryDTO, peaceCityDTO, warCityDTO, campDTO):
        gamelog.debug('@hxm onQueryWingWorldResume>>>', dto, briefVer, countryVer, cityVer)
        if dto:
            self.wingWorld.state, self.wingWorld.step, self.wingWorld.opennessLevel, self.wingWorld.trendId = dto
        self.wingWorld.briefVer = briefVer
        self.wingWorld.countryVer = countryVer
        self.wingWorld.cityVer = cityVer
        if countryDTO:
            self.wingWorld.country.fromDTO(countryDTO)
        if peaceCityDTO:
            self.wingWorld.city.fromDTO(peaceCityDTO)
        if warCityDTO:
            self.wingWorld.city.fromDTO(warCityDTO)
        if campDTO:
            self.wingWorld.camp.fromDTO(campDTO)
        gameglobal.rds.ui.wingWorldStrategy.refreshInfo()
        gameglobal.rds.ui.wingWorldPush.checkState()
        gameglobal.rds.ui.wingWorldWarFlag.refreshInfo()
        gameglobal.rds.ui.wingWorldOverView.refreshInfo()
        gameglobal.rds.ui.wingWorldMap.refreshInfo()
        gameglobal.rds.ui.wingWorldCamp.refreshCityMc()
        self.checkWingWorldContinuePathFinding()

    def onQueryWingSeasonAndWorldEvents(self, seasonBlob, hostId, worldBlob):
        gamelog.debug('@hxm onQueryWingSeasonAndWorldEvent', hostId)
        if seasonBlob:
            self.wingWorld.events = cPickle.loads(zlib.decompress(seasonBlob))
        else:
            self.wingWorld.events = []
        gamelog.info('jbx:events', self.wingWorld.events, self.wingWorld.country.getCountry(hostId).events)
        self.wingWorld.country.getCountry(hostId).updateEvents(worldBlob)
        gameglobal.rds.ui.wingWorldOverView.refreshEvents()

    def onQueryWingWorldShiliHistory(self, blob):
        historyRecords = []
        if blob:
            historyRecords = cPickle.loads(zlib.decompress(blob))
        gamelog.debug('@hxm onQueryWingWorldShiliHistory', historyRecords)
        self.processHistoryRecords(historyRecords)

    def processHistoryRecords(self, historyRecords):
        self.currentSeasonRecord = [None] * gametypes.WING_WORLD_BATTLE_MAX_CNT
        startTime = wingWorldUtils.getCurrentSeasonStartTime()
        for time, battleInfo in historyRecords:
            weekIdx = utils.getIntervalWeek(time, startTime) - 1
            if weekIdx < 0 or weekIdx >= gametypes.WING_WORLD_BATTLE_MAX_CNT:
                gamelog.error('jbx: onQueryWingWorldShiliHistory info out time', time, battleInfo)
                continue
            weekInfo = {}
            for cityInfo in battleInfo:
                cityId, hostId, hostName, guildName, leaderName = cityInfo
                weekInfo[cityId] = (hostId,
                 hostName,
                 guildName,
                 leaderName)

            self.currentSeasonRecord[weekIdx] = (time, weekInfo)

        gameglobal.rds.ui.wingWorldStrategy.refreshWingWorldHistory()

    def onQueryWingWorldSeasonHistoryBook(self, blob):
        historyBook = []
        if blob:
            historyBook = cPickle.loads(zlib.decompress(blob))
        gamelog.debug('@hxm onQueryWingWorldSeasonHistoryBook', historyBook)
        self.historyBook = historyBook
        gameglobal.rds.ui.wingWorldHistoryBook.refreshInfo()

    def onQueryWingWorldFullCityDTO(self, dto):
        gamelog.debug('@hxm onQueryWingWorldFullCityDTO', dto)
        self.wingWorld.city.fromDTO([dto])
        cityId = dto[1]
        gameglobal.rds.ui.map.refreshWingWorldOrePoint(cityId)
        gameglobal.rds.ui.wingWorldBuilding.refreshCityInfo()

    def onQueryWingWorldContributeTop(self, isSyncFinish, topVersion, hostId, cityId, topType, topBlob):
        gamelog.debug('@hxm onQueryWingWorldContributeTop', isSyncFinish, topVersion, hostId, cityId, topType)
        if not isSyncFinish:
            return
        if topVersion == 0:
            return
        topData = []
        if topBlob:
            topData = cPickle.loads(zlib.decompress(topBlob))
        gamelog.debug('@hxm topdata:', topData)

    def onWingWorldTriggerTrend(self, hostIds, trendId):
        gamelog.debug('@hxm onWingWorldTriggerTrend', hostIds, trendId)
        if self.wingWorldCamp in hostIds:
            campVal = self.wingWorld.country.getOwnCamp()
            campVal.triggerTrend(trendId)
        elif self.getOriginHostId() in hostIds:
            countryVal = self.wingWorld.country.getOwn()
            countryVal.triggerTrend(trendId)

    def onCheckTeleportToPeaceCityFail(self, cityId):
        gamelog.debug('@hxm onCheckTeleportToPeaceCityFail cityId:', cityId)
        cityName = WWCTD.data.get(cityId, {}).get('name', '')
        self.showGameMsg(GMDD.data.TELEPORT_TO_PEACE_FAIL, cityName)

    def onMarkWingWorldMinMapPoint(self, ret, points):
        gamelog.debug('@hxm onMarkMinMapPoint>>>', ret, points)
        self.wingWorldMapMarkPoints = points
        gameglobal.rds.ui.map.refreshWingWorldMarks()

    def onDelWingWorldMinMapPoint(self, ret, points):
        gamelog.debug('@hxm onDelMinMapPoint>>>', ret, points)
        self.wingWorldMapMarkPoints = points
        gameglobal.rds.ui.map.refreshWingWorldMarks()

    def onSyncWingWorldBattleInfo(self, hostId, cityId, blob, events):
        scoreDTO, minMapDTO = cPickle.loads(zlib.decompress(blob))
        gamelog.debug('@hxm onSyncWingWorldBattleInfo>>>', scoreDTO, minMapDTO)
        self.wingWorldMiniMap.fromDTO(minMapDTO)
        scoreData = {}
        for hostId, dto in scoreDTO.iteritems():
            scoreData[hostId] = {'totalScore': dto[0],
             'buildings': dto[1],
             'destroyScore': sum(dto[3].itervalues()),
             'robResDict': dto[3]}

        self.wingWorldCityWarScore = scoreData
        self.wingWorldBattleCityId = cityId
        if events:
            for eventArgs in events:
                self.onWingWarCityHappenEvent(*eventArgs)

        gameglobal.rds.ui.wingWorldInfo.refreshInfo()
        gameglobal.rds.ui.wingWorldDetailInfo.refreshInfo()
        gameglobal.rds.ui.littleMap.showWingWorldWarInfo()
        if self.wingWorldMiniMap.airStoneEnergy > 0:
            self.addAirDefenceEffect()
        else:
            self.delAirDefenceEffect()
        self.wingWorldMapMarkPoints = self.wingWorldMiniMap.hostMinMap.points
        gameglobal.rds.ui.map.refreshWingWorldMarks()

    def onWingWarCityHappenEvent(self, cityId, eventId, args):
        gamelog.debug('@hxm onWingWarCityHappenEvent>>>', cityId, eventId, args)
        if cityId != self.getWingWarCityId():
            return
        gameglobal.rds.ui.wingWorldEvent.addWingWorldEvents(cityId, eventId, args)

    def onWingWorldReliveToFail(self, cityId, minMapDTO):
        gamelog.debug('@hxm onWingWorldReliveToFail>>>', minMapDTO)
        self.wingWorldMiniMap.fromDTO(minMapDTO)
        gameglobal.rds.ui.wingWorldInfo.refreshInfo()
        gameglobal.rds.ui.wingWorldDetailInfo.refreshInfo()
        gameglobal.rds.ui.littleMap.showWingWorldWarInfo()
        if self.wingWorldMiniMap.airStoneEnergy > 0:
            self.addAirDefenceEffect()
        else:
            self.delAirDefenceEffect()
        self.wingWorldMapMarkPoints = self.wingWorldMiniMap.hostMinMap.points
        gameglobal.rds.ui.map.refreshWingWorldMarks()

    def onWingWorldTeleportToOwnerReliveBoardFail(self, cityId, minMapDTO):
        gamelog.debug('@hxm onWingWorldTeleportToOwnerReliveBoardFail>>>', minMapDTO)
        minMap = WingWorldCityMinMap()
        minMap.fromDTO(minMapDTO)

    def onStartWingWorldWarRelive(self, reliveInterval):
        gamelog.debug('@hxm onStartWingWorldWarRelive', reliveInterval)
        gameglobal.rds.ui.player.onStartBattleFieldRelive(reliveInterval)
        gameglobal.rds.ui.deadAndRelive.hide()

    def onWorldMapWarCityBlob(self, cityId, blob):
        if blob:
            dto = cPickle.loads(zlib.decompress(blob))
            gamelog.debug('@hxm onWorldMapWarCityBlob', cityId, dto)
            cityMap = WingWorldCityWorldMap()
            cityMap.fromDTO(dto)
            self.wingWorld.setWorldMapCache(cityId, cityMap)
        else:
            self.wingWorld.setWorldMapCache(cityId, None)
        gameglobal.rds.ui.map.refreshWingWorldIcons()

    def onQueryWingWorldResource(self, resList, points, records):
        gamelog.debug('@hxm onQueryWingGuildResource>>>', resList, points, records)
        try:
            self.wingWorld.country.getOwn().resourcePointMap = WingHostResourcePointMap(points)
        except:
            gamelog.debug('ypc@ hostid not in config error!')

        panel = gameglobal.rds.ui.wingWorldResource.countryPanel
        if panel:
            panel.refreshWorldInfo(resList, records)
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.updateWindWorldResCollect()
        gameglobal.rds.ui.map.refreshWingWorldOrePoint()

    def onQueryWingGuildResource(self, resList):
        gamelog.debug('@hxm onQueryWingGuildResource>>>', resList)
        panel = gameglobal.rds.ui.wingWorldResource.countryPanel
        if panel:
            panel.refreshGuildInfo(resList)

    def onWingWarStartPrompt(self, normals, defenseOccupy, attackOccupy):
        gamelog.debug('@hxm onWingWarStartPrompt normals:', normals, 'defenseOccupy:', defenseOccupy, 'attackOccupy:', attackOccupy)
        if self.lv < WWCD.data.get('enterWingWorldMapMinLevel', 69):
            return
        if normals:
            citysName = wingWorldUtils.getWingCitysName(normals)
            self.showGameMsg(GMDD.data.WING_WORLD_CITY_DEFENCE, (citysName,))
        if defenseOccupy:
            citysName = wingWorldUtils.getWingCitysName(defenseOccupy)
            self.showGameMsg(GMDD.data.WING_WORLD_CITY_SAFE, (citysName,))
        if attackOccupy:
            citysName = wingWorldUtils.getWingCitysName(attackOccupy)
            self.showGameMsg(GMDD.data.WING_WORLD_CITY_OCCUPY, (citysName,))

    def onWingWarFinishPrompt(self, attackSucc, attackFail, defenseSucc, defenseFail, topPlayers):
        gamelog.debug('@hxm onWingWarFinishPrompt', 'attackSucc:', attackSucc, 'attackFail:', attackFail, 'defenseSucc:', defenseSucc, 'defenseFail:', defenseFail, 'topPlayers:', topPlayers)
        if self.lv < WWCD.data.get('enterWingWorldMapMinLevel', 69):
            return
        if attackSucc:
            citysName, guildsName = self.getCitysNameAndGuildNams(attackSucc)
            if not guildsName:
                self.showGameMsg(GMDD.data.WING_WORLD_ATTACK_SUCC_NO_GUILD, citysName)
            else:
                self.showGameMsg(GMDD.data.WING_WORLD_ATTACK_SUCC, (citysName, guildsName))
        if attackFail:
            citysName = wingWorldUtils.getWingCitysName(attackFail)
            self.showGameMsg(GMDD.data.WING_WORLD_ATTACK_FAIL, citysName)
        if defenseSucc:
            citysName, guildsName = self.getCitysNameAndGuildNams(defenseSucc)
            if not guildsName:
                self.showGameMsg(GMDD.data.WING_WORLD_DEFENCE_SUCC_NO_GUILD, citysName)
            else:
                self.showGameMsg(GMDD.data.WING_WORLD_DEFENCE_SUCC, (citysName, guildsName))
        if defenseFail:
            citysName = wingWorldUtils.getWingCitysName(defenseFail)
            self.showGameMsg(GMDD.data.WING_WORLD_DEFENCE_FAIL, citysName)
        if topPlayers:
            roleNames = ''
            for name in topPlayers:
                if roleNames:
                    roleNames += ',%s' % name
                else:
                    roleNames += name

            self.showGameMsg(GMDD.data.WING_WORLD_TOP_PLAYERS, roleNames)

    def getCitysNameAndGuildNams(self, argList):
        cityList = []
        guildList = []
        for cityId, guildName in argList:
            cityList.append(cityId)
            guildList.append(guildName)

        citysName = wingWorldUtils.getWingCitysName(cityList)
        guildNames = guildList[0]
        for name in guildList[1:]:
            guildNames += ',%s' % name

        return (citysName, guildNames)

    def getWingWorldGroupId(self):
        return RSCD.data.get(self.getOriginHostId(), {}).get('wingWorldGroupId', 1)

    def onWingWarAdminGuildPrompt(self, cityId, guild2RankDict):
        gamelog.debug('@hxm onWingWarAdminGuildPrompt', cityId, guild2RankDict)
        if self.lv < WWCD.data.get('enterWingWorldMapMinLevel', 69):
            return
        rank = guild2RankDict.get(self.guildNUID, 0)
        if not rank:
            return
        if rank > 20:
            return
        level = wingWorldUtils.calcCityAdminLevel(rank)
        if level:
            cityName = wingWorldUtils.getCityName(cityId)
            levelName = gameStrings.WING_WORLD_MANAGER_GUILDS[level - 1]
            self.showGameMsg(GMDD.data.WING_WORLD_BECOM_ADMIN_GUILD, (cityName, levelName))
        else:
            self.showGameMsg(GMDD.data.WING_WORLD_GUILD_RANK, (rank,))

    def onUpdateArmyPostData(self, postDatas, armyVer):
        for postData in postDatas:
            gameglobal.rds.ui.wingWorldVote.updateArmyPostData(postData, armyVer)

    def onAppointWingWorldArmyPostOK(self, gbId, dto, armyVer):
        gameglobal.rds.ui.wingWorldAppoint.onAppointWingWorldArmyPostOK(gbId, dto, armyVer)

    def onWingWorldArmyMarkNotify(self):
        if self.isWingWorldCampMode():
            return
        gameglobal.rds.ui.wingWorldOverView.addPushMsg()

    def onQueryWingWorldArmyMark(self, armyMark, armyMarkVer):
        gamelog.info('jbx:onQueryWingWorldArmyMark', armyMark, armyMarkVer)
        self.wingWorldArmyMarkScore = (armyMark, armyMarkVer)
        gameglobal.rds.ui.wingWorldOverView.refreshArmyMark()

    def onQueryWingWorldArmy(self, dtos, armyVer, armyOnlineVer, armyState, extraCanVoteGbIds):
        gamelog.info('jbx:onQueryWingWorldArmy', dtos, armyVer, armyOnlineVer, armyState, extraCanVoteGbIds)
        self.wingWorld.getArmyFromDTO(dtos)
        self.wingWorld.armyVer = armyVer
        self.wingWorld.amryOnlineVer = armyOnlineVer
        self.wingWorld.armyState = armyState
        self.wingWorld.buildArmyIndex()
        self.wingWorld.extraCanVoteGbIds = extraCanVoteGbIds
        gameglobal.rds.ui.wingWorldOverView.refreshInfo()
        gameglobal.rds.ui.wingWorldVote.refreshInfo()
        gameglobal.rds.ui.wingWorldVote2nd.refreshInfo()

    def onComfirmArmyCategoryNotify(self):
        gameglobal.rds.ui.wingWorldVote2nd.show()

    def onWingWorldArmyCallNotify(self, srcPostId, srcRoleName):
        postName = wingWorldUtils.getWingArmyData().get(srcPostId, {}).get('name', '')
        msg = uiUtils.getTextFromGMD(GMDD.data.WW_ARMY_CALL_NOTIFY, '%s_%s') % (postName, srcRoleName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cell.acceptWingWorldArmyCall, yesBtnText=gameStrings.TEXT_IMPSHUANGXIU_24, noCallback=self.cell.rejectWingWorldArmyCall, noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)

    def sendWingWorldArmySkill(self, data, bRefresh = False):
        if self.isWingWorldCampArmy():
            bwTime = BigWorld.time()
            serverTime = self.getServerTime()
            logicInfo.cooldownWWArmySkill = {}
            self.wingWorld.armySkills.clear()
            for skillId, level, nextTime in data:
                self.wingWorld.armySkills[skillId] = WWArmySkillVal(skillId=skillId, level=level, nextTime=nextTime)
                if nextTime > serverTime:
                    skillcd = SGD.data.get((skillId, 1)).get('cd')
                    end = nextTime - serverTime + bwTime
                    logicInfo.cooldownWWArmySkill[skillId] = (end, skillcd)

            if bRefresh:
                gameglobal.rds.ui.actionbar.updateSlots()

    def onCastWingWorldArmySkill(self, skillId, nextTime, mpUsed, mp):
        if self.isWingWorldCampArmy():
            sk = self.wingWorld.armySkills.get(skillId, None)
            if not sk:
                sk = WWArmySkillVal(skillId=skillId, level=1, nextTime=nextTime)
                self.wingWorld.armySkills[skillId] = sk
            else:
                sk.nextTime = nextTime
            self.wingWorld.mp = mp
            post = self.wingWorld.getArmyByPostId(self.wingWorldPostId)
            if post:
                post.mpUsed = mpUsed
            bwTime = BigWorld.time()
            serverTime = self.getServerTime()
            if nextTime > serverTime:
                skillcd = SGD.data.get((skillId, 1)).get('cd')
                end = nextTime - serverTime + bwTime
                logicInfo.cooldownWWArmySkill[skillId] = (end, skillcd)
            gameglobal.rds.ui.actionbar.updateSlots()

    def onQueryRecommendSoldierInGuild(self, info):
        appointingList1 = []
        appointingList2 = []
        for player in info:
            playerInfo = {'gbId': player[0],
             'photo': player[1],
             'combatScore': player[2],
             'name': player[4],
             'school': player[5],
             'sex': player[6]}
            if player[3]:
                appointingList1.append(playerInfo)
            else:
                appointingList2.append(playerInfo)

        appointingList1 = sorted(appointingList1, key=lambda x: x['combatScore'], reverse=True)
        appointingList2 = sorted(appointingList2, key=lambda x: x['combatScore'], reverse=True)
        gameglobal.rds.ui.wingWorldAppoint.appointingList = appointingList1 + appointingList2
        gameglobal.rds.ui.wingWorldAppoint.refreshAppointingPanel()

    def onQueryWingWorldVolatile(self, volatileDTO, ver):
        mp, mpUsedDTO = volatileDTO
        self.wingWorld.volatileVer = ver
        if self.isWingWorldCampArmy():
            camp = self.wingWorld.country.getOwnCamp()
            camp.mp = mp
        else:
            hostId = utils.getHostId()
            c = self.wingWorld.country.getCountry(hostId)
            c.mp = mp
        self.wingWorld.clearMpUsed()
        for postId, mpUsed in mpUsedDTO:
            post = self.wingWorld.getArmyByPostId(postId)
            if post:
                post.mpUsed = mpUsed

        gameglobal.rds.ui.wingWorldArmySkill.refreshInfo()

    def onWingWorldCrossSeasonStep(self, step):
        gamelog.debug('@hxm onWingWorldCrossSeasonStep>>>', step)
        self.notifyWingWorldStep = step

    def onGetWingWorldWarCarrierConstruct(self, constructingInfo, constructStartTime, constructEndTime, waitingInfo, doneInfo, bornPointEntNo, resCore, resLoader, version, reason):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe8\xbd\xbd\xe5\x85\xb7\xe5\xbb\xba\xe9\x80\xa0\xe4\xbf\xa1\xe6\x81\xaf\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x88\xe5\xa6\x82\xe6\x9e\x9c\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7\xe7\x9b\xb8\xe7\xad\x89\xef\xbc\x8c\xe5\xb0\x86\xe6\xb2\xa1\xe6\x9c\x89\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x89
        \xe5\x9b\x9e\xe8\xb0\x83\xe6\x97\xb6\xe6\x9c\xba\xef\xbc\x9a
        1.\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe4\xb8\xbb\xe5\x8a\xa8\xe6\x9f\xa5\xe8\xaf\xa2\xe5\xbb\xba\xe9\x80\xa0\xe4\xbf\xa1\xe6\x81\xaf\xe6\x97\xb6
        2.\xe5\xbb\xba\xe9\x80\xa0/\xe5\x8f\x96\xe6\xb6\x88\xe5\xbb\xba\xe9\x80\xa0/\xe5\x8f\x98\xe6\x9b\xb4\xe9\x9b\x86\xe7\xbb\x93\xe7\x82\xb9 \xe6\x97\xb6\xef\xbc\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\x8f\x91\xe7\x8e\xb0\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7\xe8\xbf\x87\xe6\x97\xa7\xe6\x97\xb6\xef\xbc\x88\xe5\xbb\xba\xe8\xae\xae\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x9c\xa8\xe6\x89\x93\xe5\xbc\x80\xe9\x9d\xa2\xe6\x9d\xbf\xe6\x97\xb6\xe8\xaf\xb7\xe6\xb1\x82\xe4\xb8\x80\xe6\xac\xa1\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x8c\xe9\x9d\xa2\xe6\x9d\xbf\xe5\xbc\x80\xe6\x97\xb6\xe6\xaf\x8fN\xe7\xa7\x92\xe8\xaf\xb7\xe6\xb1\x82\xe4\xb8\x80\xe6\xac\xa1\xe6\x95\xb0\xe6\x8d\xae limitcall 1\xef\xbc\x89
        
        :param constructingInfo: \xe6\xad\xa3\xe5\x9c\xa8\xe5\xbb\xba\xe9\x80\xa0\xe7\x9a\x84\xe8\xbd\xbd\xe5\x85\xb7\xe4\xbf\xa1\xe6\x81\xaf (carrierType, enhanceDict)\xef\xbc\x8c\xe5\x89\x8d\xe8\x80\x85\xe4\xb8\xba\xe3\x80\x8a\xe7\xbf\xbc\xe4\xb8\x96\xe7\x95\x8c\xe8\xbd\xbd\xe5\x85\xb7\xe5\xbb\xba\xe9\x80\xa0\xe8\xa1\xa8\xe3\x80\x8b\xe7\x9a\x84id\xef\xbc\x8c\xe5\x90\x8e\xe8\x80\x85\xe4\xb8\xba\xe6\x94\xb9\xe9\x80\xa0\xe5\xad\x97\xe5\x85\xb8
        :param constructStartTime: \xe6\xad\xa3\xe5\x9c\xa8\xe5\xbb\xba\xe9\x80\xa0\xe7\x9a\x84\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        :param constructEndTime: \xe6\xad\xa3\xe5\x9c\xa8\xe5\xbb\xba\xe9\x80\xa0\xe7\x9a\x84\xe5\xae\x8c\xe6\x88\x90\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        :param waitingInfo: \xe7\xad\x89\xe5\xbe\x85\xe9\x98\x9f\xe5\x88\x97 [(carrierType,enhanceDict), ...] \xe6\x8c\x89\xe6\x97\xb6\xe9\x97\xb4\xe9\xa1\xba\xe5\xba\x8f
        :param doneInfo: \xe5\xae\x8c\xe6\x88\x90\xe9\x98\x9f\xe5\x88\x97 [(carrierType, enhanceDict), ...] \xe6\x8c\x89\xe6\x97\xb6\xe9\x97\xb4\xe9\x80\x86\xe5\xba\x8f
        :param bornPointEntNo: \xe8\xbd\xbd\xe5\x85\xb7\xe5\x87\xba\xe7\x94\x9f\xe9\x9b\x86\xe7\xbb\x93\xe7\x82\xb9\xef\xbc\x88\xe5\xa4\x8d\xe6\xb4\xbb\xe7\x82\xb9entityNo\xef\xbc\x89
        :param resCore: \xe5\x89\xa9\xe4\xbd\x99\xe6\xa0\xb8\xe5\xbf\x83\xe6\x95\xb0
        :param resLoader: \xe5\x89\xa9\xe4\xbd\x99\xe8\xb4\x9f\xe8\xbd\xbd\xe6\x95\xb0
        :param version: \xe5\xbd\x93\xe5\x89\x8d\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        :param reason: \xe5\x88\xb7\xe6\x96\xb0\xe7\xb1\xbb\xe5\x9e\x8b
        """
        gamelog.debug('@xzh onGetWingWorldWarCarrierConstruct', constructingInfo, constructStartTime, constructEndTime, waitingInfo, doneInfo, bornPointEntNo, resCore, resLoader, version, reason)
        gameglobal.rds.ui.wingWorldCarrierNarrow.updateCarrierInfo(constructingInfo, constructStartTime, constructEndTime, waitingInfo, doneInfo, bornPointEntNo, resCore, resLoader, version)
        gameglobal.rds.ui.wingWorldCarrierConstruct.updateResStateBuildSuc()

    def onGetWingWorldWarBuildingEntDict(self, spaceNo, entIdSet):
        self.wingWorldWarBuildingEntIdSet = entIdSet

    def onLoadWingCityStaticBuildings(self, spaceNo, data):
        self.wingWorld.pendingStaticBuildings[spaceNo] = data

    def doLoadWingCityStaticBuildings(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        for cityEntityNo, entityId, extra in self.wingWorld.pendingStaticBuildings.pop(self.spaceNo, ()):
            self.wingWorld.createClientEntity(self, entityId, cityEntityNo, extra=extra)

    def onKillAvatarInWingWarCity(self, avatarName, hostId, time):
        self.wingWorldWarKillCnt = getattr(self, 'wingWorldWarKillCnt', 0) + 1
        gameglobal.rds.ui.battleField.showKillInWingWorld(self.wingWorldWarKillCnt)

    def onDestoryWingWorldCarrier(self, carrierNo, hostId, time):
        self.wingWorldWarKillCnt = getattr(self, 'wingWorldWarKillCnt', 0) + 1
        gameglobal.rds.ui.battleField.showKillInWingWorld(self.wingWorldWarKillCnt)

    def isWingWorldLeader(self):
        wingWorldPostId = self.wingWorldPostId
        return wingWorldPostId in wingWorldUtils.wingPostIdData.ARMY_SUPER_MGR_POST_IDS

    def inWingWarCity(self):
        return formula.spaceInWingWarCity(self.spaceNo)

    def onEnterWingWarCity(self):
        gamelog.info('jbx:enterWingWarCity')
        appSetting.VideoQualitySettingObj.setScale = 1.0
        self.wingWorldWarKillCnt = 0
        self.operation['commonSetting'][17] = gameglobal.WING_WORLD_ARMER_SETTING
        if getattr(self, 'topLogo', None):
            self.topLogo.updateBorderIconAndOtherIcon()
        BigWorld.callback(2, self.enterWingWorldWarOpenUI)

    def onEnterWingPeaceCity(self):
        gamelog.info('ypc@ onEnterWingPeaceCity')
        gameglobal.rds.ui.wingWorldAllSoulsRank.clearPushMsg()
        self.operation['commonSetting'][17] = gameglobal.WING_WORLD_ARMER_SETTING
        self.addPropBalancePush()

    def onLeaveWingPeaceCity(self):
        gamelog.info('ypc@ onLeaveWingPeaceCity')
        self.wingWorldWarKillCnt = 0
        gameglobal.rds.ui.wingWorldAllSoulsRank.clearPushMsg()
        self.delPropBalancePush()

    def canOpenWingWorldUI(self):
        if formula.spaceInWingCity(self.spaceNo) or formula.spaceInWingBornIsland(self.spaceNo):
            return True
        return gameglobal.rds.configData.get('enableWingWorld', False) and self.lv >= WWCD.data.get('enterWingWorldMapMinLevel', 69) and self.checkServerProgress(WWCD.data.get('finishMileStoneId', 19008), False)

    def enterWingWorldWarOpenUI(self):
        gameglobal.rds.ui.wingWorldInfo.show()
        gameglobal.rds.ui.wingWorldPush.hide()
        gameglobal.rds.ui.wingWorldEvent.show()
        gameglobal.rds.ui.chat.goToWingWorldWar()
        fixedPrivileges = wingWorldUtils.getWingArmyData().get(self.wingWorldPostId, {}).get('fixedPrivileges', ())
        if gametypes.WING_WORLD_PRIVILEGE_WAR_CARRIER_CONSTRUCT in fixedPrivileges:
            gameglobal.rds.ui.wingWorldCarrierNarrow.show()
        if not self.operation['commonSetting'][17]:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.ARMOR_MODE_TEXT, uiUtils.enabledClanWarArmorMode, isModal=False)
        self.addPropBalancePush()

    def onLeaveWingWarCity(self):
        gamelog.info('jbx:leaveWingWarCity')
        gameglobal.rds.ui.wingWorldInfo.hide()
        gameglobal.rds.ui.wingWorldDetailInfo.hide()
        gameglobal.rds.ui.wingWorldCarrierNarrow.hide()
        gameglobal.rds.ui.wingWorldEvent.show()
        gameglobal.rds.ui.wingWorldPush.checkState()
        gameglobal.rds.ui.chat.goToWorld()
        gameglobal.rds.ui.wingWorldCarrierConstruct.hide()
        gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_PLAYER_UF, True)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_PLAYER_UF, True)
        self.delAirDefenceEffect(True)
        self.delPropBalancePush()
        if getattr(self, 'topLogo', None):
            self.topLogo.updateBorderIconAndOtherIcon()

    def getWingWarCityId(self, spaceNo = 0):
        if not spaceNo:
            spaceNo = self.spaceNo
        if formula.spaceInWingWarCity(spaceNo):
            groupId, cityType, cityIds = formula.getWingCityInfo(spaceNo)
            if len(cityIds) > 0:
                return cityIds[0]
        return 0

    def getWingCityId(self, spaceNo = 0):
        if not spaceNo:
            spaceNo = self.spaceNo
        if formula.spaceInWingCity(spaceNo):
            chunkName = BigWorld.ChunkInfoAt(self.position)
            return formula.getWingCityId(self.spaceNo, chunkName)
        return 0

    def addAirDefenceEffect(self):
        cityId = self.getWingWarCityId()
        if not cityId:
            return
        else:
            if not getattr(self, 'airDefenceSfx', None):
                self.airDefenceSfx = clientUtils.pixieFetch(sfx.getPath(WWCTD.data.get(cityId, {}).get('noAirEffect', 900008)), 2)
            if not getattr(self, 'airDefenceMode', None):
                self.airDefenceMode = sfx.getDummyModel(True)
                self.airDefenceMode.position = WWCTD.data.get(cityId, {}).get('noAirEffectPos', (0, 0, 0))
            if self.airDefenceSfx not in self.airDefenceMode.root.attachments:
                self.airDefenceMode.root.attach(self.airDefenceSfx)
                self.airDefenceSfx.scale(*WWCTD.data.get(cityId, {}).get('noAirEffectScale', (1, 1, 1)))
                self.airDefenceSfx.force()
            return

    def delAirDefenceEffect(self, removeCache = False):
        if not getattr(self, 'airDefenceSfx', None):
            return
        elif not getattr(self, 'airDefenceMode', None):
            return
        else:
            if self.airDefenceSfx in self.airDefenceMode.root.attachments:
                self.airDefenceMode.root.detach(self.airDefenceSfx)
            if removeCache:
                self.airDefenceMode = None
                self.airDefenceSfx = None
            return

    def addYabiaoAttackerEffect(self):
        if getattr(self, 'attackerEffectTimer', 0):
            BigWorld.cancelCallback(self.attackerEffectTimer)
        self.attackerEffectTimer = BigWorld.callback(self.bWingWorldYabiaoAttacker - utils.getNow(), self.delYaBiaoAttackerEffect)
        if not self.firstFetchFinished:
            return
        else:
            p = BigWorld.player()
            if p.getOriginHostId() == self.getOriginHostId():
                return
            if getattr(self, 'yabiaoAttackSfx', None):
                return
            self.yabiaoAttackSfx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
             p.getEquipEffectPriority(),
             self.model,
             WWCD.data.get('yabiaoAttackerEffect', 3002),
             sfx.EFFECT_LIMIT_MISC))
            gamelog.info('jbx:addYabiaoAttackerEffect')
            return

    def delYaBiaoAttackerEffect(self):
        gamelog.info('jbx:delYaBiaoAttackerEffect')
        self.attackerEffectTimer = 0
        if not self.inWorld:
            return
        elif not self.firstFetchFinished:
            return
        elif not getattr(self, 'yabiaoAttackSfx', None):
            return
        else:
            sfx.detachEffect(self.model, WWCD.data.get('yabiaoAttackerEffect', 3002), self.yabiaoAttackSfx)
            self.yabiaoAttackSfx = None
            return

    def enterToWingBornIslandBySkill(self, showYesOrNo = True, msgId = 0):
        if utils.getNow() < wingWorldUtils.getEnterBornIslandSkillCD() + self.wingWorldEnterSkillLastUseTime:
            self.showGameMsg(GMDD.data.SKILL_NOT_READY, ())
            return
        if formula.spaceInWingBornIsland(self.spaceNo):
            return
        if showYesOrNo:
            msg = GMD.data.get(GMDD.data.TELEPORT_TO_BORN_ISLAND if not msgId else msgId, {}).get('text', 'TELEPORT_TO_BORN_ISLAND')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cell.enterToWingBornIslandBySkill)
        else:
            self.cell.enterToWingBornIslandBySkill()

    def onQueryCelebrationActivityData(self, expireTime, totalCnt, personalCnt, topGuild):
        gamelog.info('jbx:onQueryCelebrationActivityData', expireTime, totalCnt, personalCnt)
        self.celebrationActivityData = (expireTime, totalCnt, personalCnt)
        gameglobal.rds.ui.wingWorldCelebration.refreshInfo()
        if not topGuild:
            return
        gameglobal.rds.ui.wingWorldCelebration.addPushMsg()

    def canPathFindingWingWorld(self, toSpaceNo, includeSameSpace = False):
        toSpaceNo = self.getRealWingCitySpaceNo(toSpaceNo)
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return False
        if self.spaceNo == toSpaceNo:
            if self.spaceNo in const.MULTI_CITY_SPACE_NO and self.spaceNo in const.MULTI_CITY_SPACE_NO:
                return True
            else:
                return includeSameSpace
        if self.spaceNo == const.SPACE_NO_BIG_WORLD:
            return formula.spaceInWingBornIsland(toSpaceNo) or formula.spaceInWingPeaceCity(toSpaceNo)
        elif self.inWingBornIsland() or self.inWingPeaceCity():
            return formula.spaceInWingBornIsland(toSpaceNo) or formula.spaceInWingPeaceCity(toSpaceNo) or toSpaceNo == const.SPACE_NO_BIG_WORLD
        else:
            return False

    def getRealWingCitySpaceNo(self, spaceNo):
        if not formula.spaceInWingCity(spaceNo):
            return spaceNo
        g1 = formula.getWingCityGroupId(spaceNo)
        g2 = self.getWingWorldGroupId()
        if g1 != g2:
            return spaceNo + (g2 - g1) * const.WING_CITY_MAX_ID
        else:
            return spaceNo

    def wingWorldCommitItem(self):
        selfSideId = self.wingWorldCamp if self.isWingWorldCampMode() else self.getOriginHostId()
        if not self.isWingWorldCampMode():
            if not self.inWingBornIsland() and not self.inWingPeaceCity() or self.inWingPeaceCity() and self.wingWorld.city.getCity(0, self.getWingCityId()).ownerHostId != selfSideId and selfSideId:
                self.showGameMsg(GMDD.data.WING_WORLD_CELE_IN_OWN_CITY, ())
                return
        titleLevel = self.wingWorld.country.getOwn().titleLevel
        commitItems = WWCRD.data.get(titleLevel, {}).get('commitItems')
        itemIds = []
        itemCnts = []
        strs = []
        for itemId, cnt in commitItems:
            itemIds.append(itemId)
            itemCnts.append(cnt)
            strs.append(uiUtils.getItemColorNameWithClickTips(itemId, cnt))

        msgStr = GMD.data.get(GMDD.data.COMMIT_ITEMS_CONFIRM, {}).get('text', '%s') % ','.join(strs)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgStr, self.doCommitItems)

    def doCommitItems(self):
        titleLevel = self.wingWorld.country.getOwn().titleLevel
        commitItems = WWCRD.data.get(titleLevel, {}).get('commitItems')
        itemIds = []
        itemCnts = []
        for itemId, cnt in commitItems:
            needCnt = self.inv.countItemInPages(itemId) if not self._isSoul() else self.crossInv.countItemInPages(itemId)
            if needCnt < cnt:
                self.showGameMsg(GMDD.data.NO_LOSS_FREE_ITEM, ())
                return
            itemIds.append(itemId)
            itemCnts.append(cnt)

        gamelog.info('jbx:requireCommitWingCelebrationItem', itemIds, itemCnts)
        self.cell.requireCommitWingCelebrationItem(itemIds, itemCnts)

    def requireStartWingWorldCelebration(self):
        selfSideId = self.wingWorldCamp if self.isWingWorldCampMode() else self.getOriginHostId()
        if not self.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
            self.showGameMsg(GMDD.data.WING_WORLD_NOT_IN_CELEBRATION_SEASPN, ())
            return
        postId = self.wingWorldPostId
        if postId not in wingWorldUtils.wingPostIdData.START_CELEBRATION_POST_IDS:
            self.showGameMsg(GMDD.data.WING_WORLD_NOT_IN_CELEBRATION_POST_IDS, ())
            return
        if not self.inWingBornIsland() and not self.inWingPeaceCity() or self.inWingPeaceCity() and self.wingWorld.city.getCity(0, self.getWingCityId()).ownerHostId != selfSideId and selfSideId:
            self.showGameMsg(GMDD.data.WING_WORLD_CELE_IN_OWN_CITY, ())
            return
        gamelog.info('jbx:requireStartWingWorldCelebration')
        self.cell.requireStartWingWorldCelebration()

    def addPropBalancePush(self):
        lastTime = appSetting.Obj.get(keys.SET_WING_WORLD_PUSH, 0)
        if lastTime and utils.isSameWeek(lastTime, utils.getNow()):
            return
        appSetting.Obj[keys.SET_WING_WORLD_PUSH] = utils.getNow()
        appSetting.Obj.save()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_PROP)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_PROP, {'click': Functor(gameglobal.rds.ui.fengyinShow.show, self.mapID)})

    def delPropBalancePush(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_PROP)

    def getWingGroupId(self):
        return RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)

    def teleportToWingWarCity(self, cityId):
        if (gameglobal.rds.ui.wingWorldQueue.widget or gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_WING_WORLD_QUEUE)) and gameglobal.rds.ui.wingWorldQueue.cityId != cityId:
            msg = GMD.data.get(GMDD.data.ABORT_WING_WORLD_QUEUE_CONFIRM, {}).get('text', 'GMDD.data.ABORT_WING_WORLD_QUEUE_CONFIRM')
            if gameglobal.rds.ui.wingWorldQueue.isQueueV2Type():
                self.base.signWingWorldWarQueue(cityId)
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmAbortWingWorldQueue, cityId))
        elif gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False):
            self.base.signWingWorldWarQueue(cityId)
        else:
            self.cell.teleportToWingWarCity(cityId)

    def showConfirmQuitWingWorldQueueV2(self):
        msg = GMD.data.get(GMDD.data.ABORT_WING_WORLD_QUEUE_CONFIRM_V2, {}).get('text', 'GMDD.data.ABORT_WING_WORLD_QUEUE_CONFIRM_V2')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().base.unsignWingWorldWarQueue)

    def confirmAbortWingWorldQueue(self, cityId):
        self.cell.cancelTeleportToWingWarCityQueue(gameglobal.rds.ui.wingWorldQueue.cityId)
        self.cell.teleportToWingWarCity(cityId)

    def confirmAbortWingWorldQueueV2(self, cityId):
        self.base.unsignWingWorldWarQueue(self.wwSignAndQueueCityId)

    def onWingWorldWarCityAddInQueue(self, cityId, queueCnt):
        """
        \xe5\x8a\xa0\xe5\x85\xa5\xe9\x98\x9f\xe5\x88\x97
        :param cityId:
        :param queueCnt:
        :return:
        """
        gamelog.info('jbx:onWingWorldWarCityAddInQueue', cityId, queueCnt)
        gameglobal.rds.ui.wingWorldQueue.show(cityId, queueCnt)

    def onWingWorldWarCityQueueReady(self, cityId, countDown):
        """
        \xe9\x98\x9f\xe5\x88\x97\xe6\x8e\x92\xe5\x88\xb0
        :param cityId:
        :param countDown:
        :return:
        """
        gameglobal.rds.ui.wingWorldQueue.cityId = 0
        gameglobal.rds.ui.wingWorldQueue.queueCnt = 0
        cityName = WWCTD.data.get(cityId, {}).get('name', '')
        msg = GMD.data.get(GMDD.data.WING_WORLD_QUEUE_ENTER, {}).get('text', 'GMMDD.data.WING_WORLD_QUEUE_ENTER%s') % cityName
        gameglobal.rds.ui.wingWorldQueue.removePushMsg()
        gameglobal.rds.ui.wingWorldQueue.hide()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.teleportToWingWarCity, cityId), repeat=countDown, repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, noCallback=Functor(self.cell.rejectTeleportToWingWarCityQueue, cityId), countDownFunctor=Functor(self.cell.rejectTeleportToWingWarCityQueue, cityId))

    def onWingWorldWarCitySyncQueueInfo(self, queueCnt):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe9\x98\x9f\xe5\x88\x97\xe4\xba\xba\xe6\x95\xb0
        :param queueCnt:
        :return:
        """
        gamelog.info('jbx:onWingWorldWarCitySyncQueueInfo', queueCnt)
        gameglobal.rds.ui.wingWorldQueue.onWingWorldWarCitySyncQueueInfo(queueCnt)

    def onCancelTeleportToWingWarCityQueue(self, cityId):
        """
        \xe5\x8f\x96\xe6\xb6\x88\xe6\x8e\x92\xe9\x98\x9f\xe5\x9b\x9e\xe8\xb0\x83
        :param cityId:
        :return:
        """
        gamelog.info('jbx:onCancelTeleportToWingWarCityQueue', cityId)
        gameglobal.rds.ui.wingWorldQueue.hide()
        gameglobal.rds.ui.wingWorldQueue.cityId = 0
        gameglobal.rds.ui.wingWorldQueue.removePushMsg()

    def updateWingWorldWarQueueState(self, state):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe6\x8a\xa5\xe5\x90\x8d&\xe6\x8e\x92\xe9\x98\x9f\xe7\x8a\xb6\xe6\x80\x81
        :param state:
        :return:
        """
        self.wingWorldQueueState = state
        if state not in gametypes.WING_WORLD_SIGN_AND_QUEUE_STATES:
            return

    def onNotifyWWSignResult(self, cityId, succ):
        """
        \xe6\x8a\xa5\xe5\x90\x8d\xe7\xbb\x93\xe6\x9e\x9c
        :param cityId:
        :param succ: True: \xe9\x80\x89\xe4\xb8\xad\xef\xbc\x8c False:\xe6\x9c\xaa\xe9\x80\x89\xe4\xb8\xad
        :return:
        """
        if not succ:
            self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.WING_WORLD_PULL_FAILED,))
            gameglobal.rds.ui.wingWorldQueue.removePushMsg()
            gameglobal.rds.ui.wingWorldQueue.hide()

    def onPullWWSignMember(self, cityId):
        """
        \xe6\x8a\xa5\xe5\x90\x8d\xe9\x80\x89\xe4\xb8\xad\xef\xbc\x8c\xe6\x9d\xa5\xe6\x8b\x89\xe4\xba\xba\xe4\xba\x86
        :param cityId:
        :return:
        """
        gameglobal.rds.ui.wingWorldQueue.removePushMsg()
        gameglobal.rds.ui.wingWorldQueue.hide()
        cityName = WWCTD.data.get(cityId, {}).get('name', '')
        msg = GMD.data.get(GMDD.data.WING_WORLD_QUEUE_ENTER, {}).get('text', 'GMMDD.data.WING_WORLD_QUEUE_ENTER%s') % cityName
        countDown = 60
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.confirmEnterOnWingWorldWarQueue, cityId), repeat=countDown, repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, noCallback=self.base.unsignWingWorldWarQueue, countDownFunctor=Functor(self.cell.confirmEnterOnWingWorldWarQueue, cityId), needDissMissCallBack=False, canEsc=False)

    def onEnterWingWorldWarQueue(self, cityId, isQueue, canEnter, queueNum, myIndex, emptyPos):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe6\x8e\x92\xe9\x98\x9f\xe7\x8a\xb6\xe6\x80\x81
        :param cityId:
        :param isQueue: \xe6\x98\xaf\xe5\x90\xa6\xe9\x9c\x80\xe8\xa6\x81\xe6\x8e\x92\xe9\x98\x9f\xef\xbc\x8cFalse\xe8\xa1\xa8\xe7\xa4\xba\xe5\x9f\x8e\xe6\x88\x98\xe5\x9c\xb0\xe5\x9b\xbe\xe6\x9c\x89\xe7\xa9\xba\xe4\xbd\x8d\xef\xbc\x8c\xe4\xb8\x8d\xe7\x94\xa8\xe6\x8e\x92\xe9\x98\x9f\xe7\x9b\xb4\xe6\x8e\xa5\xe8\xbf\x9b\xe3\x80\x82
        :param canEnter: \xe5\xbd\x93\xe5\x89\x8d\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xbf\x9b\xef\xbc\x8c True\xe8\xa1\xa8\xe7\xa4\xba\xe6\x8e\x92\xe9\x98\x9f\xe8\xbd\xae\xe5\x88\xb0\xe4\xba\x86
        :param queueNum: \xe9\x98\x9f\xe4\xbc\x8d\xe9\x95\xbf\xe5\xba\xa6
        :param myIndex: \xe6\x88\x91\xe7\x9a\x84\xe4\xbd\x8d\xe7\xbd\xae
        :param emptyPos: \xe7\xa9\xba\xe4\xbd\x8d
        :return:
        """
        gamelog.debug('dxk@onEnterWingWorldWarQueue', cityId, isQueue, canEnter, queueNum, myIndex, emptyPos)
        if not isQueue and canEnter:
            gameglobal.rds.ui.wingWorldQueue.removePushMsg()
            gameglobal.rds.ui.wingWorldQueue.hide()
            self.cell.confirmEnterOnWingWorldWarQueue(cityId)
            return
        elif canEnter:
            gameglobal.rds.ui.wingWorldQueue.removePushMsg()
            gameglobal.rds.ui.wingWorldQueue.hide()
            cityName = WWCTD.data.get(cityId, {}).get('name', '')
            msg = GMD.data.get(GMDD.data.WING_WORLD_QUEUE_ENTER, {}).get('text', 'GMMDD.data.WING_WORLD_QUEUE_ENTER%s') % cityName
            countDown = 60
            self.cancelWingWorldQueueCounterCallBack()
            self.wingWorldQueueCountDownCallBack = BigWorld.callback(countDown, Functor(self.wingWorldQueueCounterCallBack, cityId))
            self.wingWorldQueueCountDownStart = utils.getNow()
            self.showWingWorldQueueMessage(countDown, cityId)
            return
        else:
            if isQueue:
                queueStartTime = getattr(self, 'wingWorldQueueStartTime', 0)
                if getattr(self, 'wingWorldQueueNumSetCallback', None):
                    BigWorld.cancelCallback(self.wingWorldQueueNumSetCallback)
                self.wingWorldQueueNumSetCallback = None
                if queueStartTime and utils.getNow() - queueStartTime < 5:
                    self.wingWorldQueueNumSetCallback = BigWorld.callback(5, Functor(self.updateWorldQueueNumCallBack, cityId, myIndex))
                    return
                gameglobal.rds.ui.wingWorldQueue.show(cityId, myIndex, 2, isOpen=False)
            return

    def updateWorldQueueNumCallBack(self, cityId, myIndex):
        if gameglobal.rds.ui.wingWorldQueue.cityId != cityId or gameglobal.rds.ui.wingWorldQueue.queueCnt >= myIndex:
            return
        else:
            gameglobal.rds.ui.wingWorldQueue.show(cityId, myIndex, 2, isOpen=False)
            self.wingWorldQueueNumSetCallback = None
            return

    def wingWorldQueueMsgMinCallBack(self):
        if uiConst.MESSAGE_TYPE_START_QUEUE_OVER not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_START_QUEUE_OVER)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_START_QUEUE_OVER, {'click': self.onClickWingWorldQueueMsgPush})

    def showWingWorldQueueMessage(self, count, cityId):
        if getattr(self, 'wingWorldQueuePushMsgId', 0):
            gameglobal.rds.ui.messageBox.dismiss(self.wingWorldQueuePushMsgId, needDissMissCallBack=False)
        cityName = WWCTD.data.get(cityId, {}).get('name', '')
        msg = GMD.data.get(GMDD.data.WING_WORLD_QUEUE_ENTER, {}).get('text', 'GMMDD.data.WING_WORLD_QUEUE_ENTER%s') % cityName
        self.wingWorldQueuePushMsgId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.clientConfirmEnterOnWingWorldWarQueue, cityId), repeat=count, repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, noCallback=self.base.unsignWingWorldWarQueue, countDownFunctor=Functor(self.cell.confirmEnterOnWingWorldWarQueue, cityId), minCallback=self.wingWorldQueueMsgMinCallBack, needDissMissCallBack=False, canEsc=False)

    def clientConfirmEnterOnWingWorldWarQueue(self, cityId):
        if not formula.spaceInBornIslandOrWingCity(self.spaceNo):
            self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.WING_WORLD_NOT_IN_BORN_CITY,))
            self.wingWorldQueueMsgMinCallBack()
        else:
            self.cancelWingWorldQueueCounterCallBack()
            self.cell.confirmEnterOnWingWorldWarQueue(cityId)

    def wingWorldQueueCounterCallBack(self, cityId):
        self.wingWorldQueueCountDownCallBack = None
        self.cell.confirmEnterOnWingWorldWarQueue(cityId)
        self.removeWingWorldQueuePush()

    def cancelWingWorldQueueCounterCallBack(self):
        if getattr(self, 'wingWorldQueueCountDownCallBack', None):
            BigWorld.cancelCallback(self.wingWorldQueueCountDownCallBack)
            self.wingWorldQueueCountDownCallBack = None

    def onClickWingWorldQueueMsgPush(self):
        cityId = self.wwSignAndQueueCityId
        countStart = getattr(self, 'wingWorldQueueCountDownStart', 0)
        countDown = countStart - utils.getNow() + 60
        if countDown < 0:
            self.removeWingWorldQueuePush()
            return
        self.showWingWorldQueueMessage(countDown, cityId)

    def removeWingWorldQueuePush(self):
        if uiConst.MESSAGE_TYPE_START_QUEUE_OVER not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_START_QUEUE_OVER)

    def refreshWingWorldQueueInfo(self):
        if self.inWingWorldQueueState():
            self.wingWorldQueueStartTime = utils.getNow()
            if self.wwSignAndQueueState in (gametypes.WING_WORLD_PLAYER_SIGN_STATE_SIGN_SUCC, gametypes.WING_WORLD_PLAYER_SIGN_STATE_IN_SIGN):
                gameglobal.rds.ui.wingWorldQueue.show(self.wwSignAndQueueCityId, 0, 1)
            else:
                gameglobal.rds.ui.wingWorldQueue.show(self.wwSignAndQueueCityId, 0, 2)
        else:
            self.wingWorldQueueStartTime = 0
            self.cancelWingWorldQueueCounterCallBack()
            gameglobal.rds.ui.wingWorldQueue.removePushMsg()
            gameglobal.rds.ui.wingWorldQueue.hide()
        gameglobal.rds.ui.wingWorldTransport.refreshBoxState()

    def inWingWorldQueueState(self):
        return self.wwSignAndQueueCityId and self.wwSignAndQueueState in gametypes.WING_WORLD_PLAYER_QUEUE_STATES

    def set_wwSignAndQueueCityId(self, oldVal):
        self.refreshWingWorldQueueInfo()

    def set_wwSignAndQueueState(self, oldVal):
        self.refreshWingWorldQueueInfo()

    def updateArmyGather(self, armyGather):
        """
        \xe5\x88\xb7\xe6\x96\xb0\xe9\x9b\x86\xe7\xbb\x93\xe5\x9f\x8e\xe5\xb8\x82
        :param armyGather:
        :return:
        """
        self.wingWorldGatherInfo = armyGather
        gameglobal.rds.ui.map.addWingWorldGatherIcon()
        gameglobal.rds.ui.wingWorldStrategy.refreshInfo()
        if gameglobal.rds.configData.get('enableWingWorldArmyGather', False):
            self.refreshWingGatherPush()

    def refreshWingGatherPush(self):
        wingWorldState = BigWorld.player().wingWorld.state
        if gametypes.WING_WORLD_STATE_DECLARE < wingWorldState < gametypes.WING_WORLD_STATE_FINISH:
            gatherCity = self.getWingGatherCityId()
            if gatherCity:
                if uiConst.MESSAGE_TYPE_START_GATHER not in gameglobal.rds.ui.pushMessage.msgs:
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_START_GATHER)
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_START_GATHER, {'click': self.onWingGatherPushClick})
                return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_START_GATHER)

    def onWingGatherPushClick(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_START_GATHER)
        gatherCity = self.getWingGatherCityId()
        if gatherCity:
            cityName = WWCTD.data.get(gatherCity, {}).get('name', '')
            msg = gameStrings.WING_WORLD_GATHER_CONFIRM % cityName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.confirmWingGather, gatherCity))

    def confirmWingGather(self, gatherCity):
        if not self.wwSignAndQueueCityId or self.wwSignAndQueueCityId != gatherCity:
            self.teleportToWingWarCity(gatherCity)

    def isWingGatherCity(self, cityId):
        gatherCityId = self.getWingGatherCityId()
        if gatherCityId:
            return gatherCityId == cityId
        return False

    def getWingGatherCityId(self):
        gatherInfo = getattr(self, 'wingWorldGatherInfo', {})
        return gatherInfo.get(self.wingWorldCamp, 0)
