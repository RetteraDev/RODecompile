#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impClanWar.o
from gamestrings import gameStrings
import math
import BigWorld
import const
import gamelog
import gameglobal
import gametypes
import utils
from item import Item
from guis import uiConst
from guis import uiUtils
from guis import generalPushMappings
from guis.clanChallengeProxy import TAB_IDX_CROSS_CLAN_CHALLENGE
from guis import events
from helpers import clanWar
from helpers.clanWar import ReliveBoardVal, BuildingVal
from callbackHelper import Functor
from gamestrings import gameStrings
from data import quest_marker_data as QMD
from data import item_data as ID
from data import chunk_mapping_data as CMD
from data import clan_war_fort_data as CWFD
from data import clan_war_marker_data as CWMD
from data import game_msg_data as GMD
from data import clan_war_challenge_config_data as CWCCD
from cdata import game_msg_def_data as GMDD
CW_START = 1
CW_END = 2
SHOW_COUNT = [300,
 60,
 30,
 20,
 15,
 10,
 9,
 8,
 7,
 6,
 5,
 4,
 3,
 2,
 1]
COUNT_DOWN_NUM = (5, 4, 3, 2, 1)
ANIMATION_SHOW_COUNT = [15, 10]
START_COUNT = 1
END_COUNT = 2

class ImpClanWar(object):

    def isInClanWar(self):
        return self.inClanWar

    def showItemIconNearClanWarCreation(self, entId, itemId):
        ent = BigWorld.entities.get(entId)
        if ent and utils.instanceof(ent, 'ClanWarReliveBoard'):
            self.showDestroyableItemIcon(entId)
            return
        if ent and utils.instanceof(ent, 'ClanWarMarker'):
            self.showItemIconNearClanWarMarker(entId, itemId)
            return
        icon = ID.data.get(itemId, {}).get('icon', '')
        path = 'item/icon/%d.dds' % icon
        gameglobal.rds.ui.npcSlot.hide()
        gameglobal.rds.ui.npcSlot.show(path, type=uiConst.SLOT_FROM_CLAN_WAR_CREATION, params=[entId, True, itemId])
        gameglobal.rds.ui.pressKeyF.isClanWarCreation = True
        gameglobal.rds.ui.pressKeyF.clanWarCreationId = entId
        gameglobal.rds.ui.pressKeyF.setType(const.F_CLANWARCREATION)

    def hideItemIconNearClanWarCreation(self, entId):
        ent = BigWorld.entities.get(entId)
        if ent and utils.instanceof(ent, 'ClanWarMarker'):
            self.hideItemIconNearClanWarMarker(entId)
            return
        elif ent and utils.instanceof(ent, 'ClanWarReliveBoard'):
            self.hideDestroyableItemIcon(entId)
            return
        else:
            if gameglobal.rds.ui.pressKeyF.clanWarCreationId == entId:
                gameglobal.rds.ui.npcSlot.hide()
                gameglobal.rds.ui.pressKeyF.clanWarCreationId = None
            if gameglobal.rds.ui.pressKeyF.isClanWarCreation == True:
                gameglobal.rds.ui.pressKeyF.isClanWarCreation = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_CLANWARCREATION)
            return

    def showItemIconNearClanWarMarker(self, entId, itemId):
        icon = ID.data.get(itemId, {}).get('icon', '')
        path = 'item/icon/%d.dds' % icon
        gameglobal.rds.ui.npcSlot.hide()
        gameglobal.rds.ui.npcSlot.show(path, type=uiConst.SLOT_FROM_CLAN_WAR_CREATION, params=[entId, True, itemId])
        gameglobal.rds.ui.pressKeyF.isClanWarMarker = True
        gameglobal.rds.ui.pressKeyF.clanWarCreationId = entId
        gameglobal.rds.ui.pressKeyF.setType(const.F_CLANWARMARKER)

    def hideItemIconNearClanWarMarker(self, entId):
        if gameglobal.rds.ui.pressKeyF.clanWarCreationId == entId:
            gameglobal.rds.ui.npcSlot.hide()
            gameglobal.rds.ui.pressKeyF.clanWarCreationId = None
        if gameglobal.rds.ui.pressKeyF.isClanWarMarker == True:
            gameglobal.rds.ui.pressKeyF.isClanWarMarker = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_CLANWARMARKER)

    def showDestroyableItemIcon(self, entId):
        if gameglobal.rds.ui.pressKeyF.clanWarCreationId:
            gameglobal.rds.ui.npcSlot.hide()
        gameglobal.rds.ui.pressKeyF.isDestroyable = True
        gameglobal.rds.ui.pressKeyF.clanWarCreationId = entId
        gameglobal.rds.ui.pressKeyF.setType(const.F_DESTROYABLE)

    def hideDestroyableItemIcon(self, entId):
        if gameglobal.rds.ui.pressKeyF.clanWarCreationId == entId:
            gameglobal.rds.ui.npcSlot.hide()
            gameglobal.rds.ui.pressKeyF.clanWarCreationId = None
        if gameglobal.rds.ui.pressKeyF.isDestroyable == True:
            gameglobal.rds.ui.pressKeyF.isDestroyable = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_DESTROYABLE)
        if getattr(self, 'destroyClanWarBuildingConfirmId', 0):
            gameglobal.rds.ui.messageBox.dismiss(self.destroyClanWarBuildingConfirmId)
            self.destroyClanWarBuildingConfirmId = 0

    @property
    def clanWar(self):
        if self._isSoul():
            return self.crossClanWar
        else:
            return self.localClanWar

    def useClanWarItem(self, entId):
        if not gameglobal.rds.ui.pressKeyF.clanWarCreationId:
            return
        ent = BigWorld.entities.get(gameglobal.rds.ui.pressKeyF.clanWarCreationId)
        if not ent:
            return
        if utils.instanceof(ent, 'Npc') or utils.instanceof(ent, 'MovableNpc') or utils.instanceof(ent, 'ClanWarMarker'):
            stype = QMD.data.get(ent.npcId, {}).get('filterBySubtype')
            if stype:
                if BigWorld.player()._isSoul():
                    gameglobal.rds.ui.crossServerBag.show()
                else:
                    gameglobal.rds.ui.inventory.show(True)
                    if stype == Item.SUBTYPE_2_CLAN_WAR_STONE:
                        p = BigWorld.player()
                        fortId = p.getCurrentFortId()
                        if fortId and CWFD.data.get(fortId, {}).get('type') == const.FORT_TYPE_JUDIAN:
                            stype = Item.SUBTYPE_2_CLAN_WAR_STONE_2
                    gameglobal.rds.ui.inventory.setFilterBySubtype(stype)
        elif utils.instanceof(ent, 'ClanWarCreation'):
            ent.chooseItem()

    def onGetFortOccupyInfo(self, data, hostId):
        gamelog.info('jbx:onGetFortOccupyInfo', hostId, data)
        if hostId and hostId != self.getOriginHostId():
            for d in data:
                fortId = d[0]
                if len(d) == 1:
                    self.crossClanWar.fort[fortId] = clanWar.FortVal(fortId)
                else:
                    fortId, guildNUID, guildName, guildFlag, clanNUID, fromHostId = d
                    self.crossClanWar.fort[fortId] = clanWar.FortVal(fortId, guildNUID, guildName, guildFlag, clanNUID, fromHostId)

        else:
            for d in data:
                fortId = d[0]
                if len(d) == 1:
                    self.clanWar.fort[fortId] = clanWar.FortVal(fortId)
                else:
                    fortId, guildNUID, guildName, guildFlag, clanNUID, fromHostId = d
                    self.clanWar.fort[fortId] = clanWar.FortVal(fortId, guildNUID, guildName, guildFlag, clanNUID, fromHostId)

            gameglobal.rds.ui.crossClanWar.refreshInfo()
        if gameglobal.rds.ui.crossClanWar.showClanWarResult:
            gameglobal.rds.ui.clanWar.showClanWarResult(True)
            gameglobal.rds.ui.crossClanWar.showClanWarResult = False

    def onUseClanWarItem(self):
        gameglobal.rds.ui.inventory.setFilterBySubtype(0)

    def onNotUseClanWarItem(self):
        gameglobal.rds.ui.inventory.setFilterBySubtype(0)

    def destroyClanWarBuilding(self, entId):
        if not entId:
            return
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        if getattr(self, 'destroyClanWarBuildingConfirmId', 0):
            return
        self.destroyClanWarBuildingConfirmId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPCLANWAR_182 % ent.roleName, yesCallback=lambda : self._confirmDestroyClanWarBuilding(entId), noCallback=self._cancelDestroyClanWarBuilding, isModal=True)

    def _confirmDestroyClanWarBuilding(self, entId):
        self.destroyClanWarBuildingConfirmId = 0
        self.cell.destroyClanWarBuilding(entId)

    def _cancelDestroyClanWarBuilding(self):
        self.destroyClanWarBuildingConfirmId = 0

    def onStartReliveByGuild(self, reliveInterval):
        gameglobal.rds.ui.deadAndRelive.hide()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()
        gameglobal.rds.ui.deadAndRelive.guildReliveCountDown(reliveInterval)

    def showClanWarTip(self, tipId):
        gameglobal.rds.ui.showPicTip(tipId)

    def reliveByGuild(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_GUILD, True)

    def onGetNpcAwardInfo(self, npcEntId, npcFuncType, awardInfo):
        npcEnt = BigWorld.entities.get(npcEntId)
        if not npcEnt:
            return
        npcEnt.awardInfo[npcFuncType] = awardInfo
        if gameglobal.rds.ui.funcNpc.lastFuncType == npcFuncType:
            gameglobal.rds.ui.funcNpc.openAwardPanel(npcFuncType, npcEntId)

    def clanWarCountDown(self, stage):
        if not hasattr(self, 'cwCountTimer'):
            return
        else:
            self._calcCurrentCWCount()
            if self.spaceNo != const.CLAN_WAR_SPACE_NO or self.clanWarStatus and stage == CW_START or not self.clanWarStatus and stage == CW_END:
                if getattr(self, 'cwCallback', None):
                    BigWorld.cancelCallback(self.cwCallback)
                    self.cwCallback = None
                    gameglobal.rds.ui.arena.closeArenaCountDown()
                return
            if self.cwCountTimer <= 0:
                gameglobal.rds.ui.arena.closeArenaCountDown()
                return
            if getattr(self, 'cwCallback', None):
                BigWorld.cancelCallback(self.cwCallback)
                self.cwCallback = None
            if self.cwCountTimer in SHOW_COUNT:
                msgId = None
                if stage == CW_START:
                    fortId = self.getCurrentFortId()
                    fort = self.clanWar.fort.get(fortId)
                    if fort and not fort.checkOwnerEx(self.guildNUID, self.clanNUID):
                        msgId = GMDD.data.CLAN_WAR_START_OTHER_COUNT_DOWN
                    else:
                        msgId = GMDD.data.CLAN_WAR_START_COUNT_DOWN
                else:
                    msgId = GMDD.data.CLAN_WAR_END_COUNT_DOWN
                leftTime = utils.formatTime(self.cwCountTimer)
                self.showGameMsg(msgId, (leftTime,))
            self.cwCallback = BigWorld.callback(1, Functor(self.clanWarCountDown, stage))
            return

    def _calcCurrentCWCount(self):
        self.cwCountTimer = int(math.ceil(max(0, self.cwStageTime - self.getServerTime())))

    def onClanWarStartTimeNotify(self, t):
        gameglobal.rds.ui.arena.openArenaMsg()
        self.cwStageTime = t
        self._calcCurrentCWCount()
        self.clanWarCountDown(CW_START)

    def onClanWarEndTimeNotify(self, t):
        self.cwStageTime = t
        self._calcCurrentCWCount()

    def getCurrentFortId(self):
        chunk = BigWorld.ChunkInfoAt(self.position)
        return CMD.data.get(chunk, {}).get('fortId', 0)

    def _updateClanWarTopLogo(self):
        entities = []
        for en in BigWorld.entities.values():
            if (en.__class__.__name__ == 'Avatar' or en.__class__.__name__ in gametypes.CLAN_WAR_CLASS) and en.topLogo:
                entities.append(en)

        for en in entities:
            en.topLogo.updateRoleName(en.topLogo.name)

        if self.targetLocked:
            target = self.targetLocked
            ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)

    def _updateClanWarTopLogoByEntId(self, entId):
        en = BigWorld.entities.get(entId)
        if not en or not en.IsAvatar or not en.topLogo:
            return
        en.topLogo.updateRoleName(en.topLogo.name)

    def onDeclareWarTo(self, guildNUID, guildName):
        self.declareWarGuild.add(guildNUID)
        for en in BigWorld.entities.values():
            if en.inWorld and (en.IsAvatar and en.guildNUID == guildNUID or getattr(en, 'guildNUID', 0) == guildNUID) and en.topLogo:
                en.topLogo.updateRoleName(en.topLogo.name)

        self.showGameMsg(GMDD.data.DECLARE_WAR_TO, (guildName,))
        gameglobal.rds.ui.clanWar.declareToSucc(guildNUID, guildName)
        self.refreshTargetLocked()

    def onDeclareWarFrom(self, guildNUID, guildName):
        self.declareWarGuild.add(guildNUID)
        for en in BigWorld.entities.values():
            if en.inWorld and (en.IsAvatar and en.guildNUID == guildNUID or getattr(en, 'guildNUID', 0) == guildNUID) and en.topLogo:
                en.topLogo.updateRoleName(en.topLogo.name)

        self.showGameMsg(GMDD.data.DECLARE_WAR_FROM, (guildName,))
        self.refreshTargetLocked()

    def cancelDeclareWarRequest(self, guildNUID, guildName):
        tip = gameStrings.TEXT_IMPCLANWAR_323 % guildName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(tip, Functor(self.confirmCancelWarRequest, guildNUID), noCallback=Functor(self.rejectWarRequest, guildNUID))

    def confirmCancelWarRequest(self, guildNUID):
        self.cell.confirmCancelDeclareWar(guildNUID)

    def rejectWarRequest(self, guildNUID):
        self.cell.rejectCancelDeclareWar(guildNUID)

    def onCancelDeclareWar(self, guildNUID, guildName):
        if guildNUID not in self.declareWarGuild:
            return
        self.declareWarGuild.remove(guildNUID)
        for en in BigWorld.entities.values():
            if en.inWorld and (en.IsAvatar and en.guildNUID == guildNUID or getattr(en, 'guildNUID', 0) == guildNUID) and en.topLogo:
                en.topLogo.updateRoleName(en.topLogo.name)

        gameglobal.rds.ui.clanWar.onCancelDeclareWar(guildNUID, guildName)
        self.refreshTargetLocked()

    def onQueryDeclareWar(self, ver, data):
        gameglobal.rds.ui.clanWar.setDeclareWarList(ver, data)

    def onLoadClanWarData(self, data):
        fortData, buildingData, scoreData, hostId = data
        gamelog.info('jbx:onLoadClanWarData:fortData, buildingData, scoreData, hostId', fortData, buildingData, scoreData, hostId)
        guildKillCnt, guildRecordScore, kill, dmg, cure, fame = scoreData
        self.crossClanWarRealTimeInfo = {'guildKillCnt': guildKillCnt,
         'killCnt': kill,
         'dmg': dmg,
         'cure': cure,
         'fameScore': fame,
         'guildRecordScore': guildRecordScore}
        self.onGetFortOccupyInfo(fortData, hostId)
        delta = 5
        marker = {}
        for k, v in CWMD.data.iteritems():
            buildingType = v.get('buildingType')
            bm = marker.get(buildingType)
            if not bm:
                bm = []
                marker[buildingType] = bm
            bm.append((k, v.get('position')))

        for nuid, buildingType, buildingId, pos in buildingData:
            cmarkerId = 0
            bm = marker.get(buildingType)
            if bm:
                for markerId, cpos in bm:
                    if abs(cpos[0] - pos[0]) < delta and abs(cpos[1] - pos[1]) < delta and abs(cpos[2] - cpos[2]) < delta:
                        cmarkerId = markerId
                        break

            self.onAddGuildClanWarBuilding(buildingType, (nuid,
             buildingId,
             pos,
             cmarkerId), False)

    def onAddGuildClanWarBuilding(self, buildingType, data, showTip = True):
        nuid, buildingId, pos, cmarkerId = data
        building = BuildingVal(nuid, buildingType, buildingId, cmarkerId, pos)
        self.clanWar.building[nuid] = building
        if cmarkerId:
            self.clanWar.cmarker[cmarkerId] = building
        if buildingType == gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD:
            self.clanWar.reliveBoard[nuid] = ReliveBoardVal(nuid, buildingId, pos)
            if showTip:
                self.showClanWarTip(gametypes.CLAN_WAR_TIP_RELIVE_BOARD_BUILT)
        gameglobal.rds.ui.littleMap.showGuildBuilding()

    def onDelGuildClanWarBuilding(self, nuid):
        building = self.clanWar.building.get(nuid)
        if building:
            self.clanWar.building.pop(nuid, None)
            self.clanWar.cmarker.pop(building.cmarkerId, None)
        self.clanWar.reliveBoard.pop(nuid, None)
        gameglobal.rds.ui.littleMap.showGuildBuilding()

    def showSelectStoneToTeleport(self):
        gameglobal.rds.ui.clanWar.showSelectStoneToTeleport()
        gameglobal.rds.ui.crossClanWarInfo.showSelectStoneToTeleport()

    def onFortOwnerGuildRename(self, guildNUID, name):
        for fort in self.clanWar.fort.itervalues():
            if fort.ownerGuildNUID == guildNUID:
                fort.ownerGuildName = name

    def useGuildSkill(self, skillId):
        if skillId == gametypes.GUILD_SKILL_TELEPORT:
            gameglobal.rds.ui.clanWar.onClanWarTeleport()
        elif skillId == gametypes.GUILD_SKILL_STONE_SHIELD:
            gameglobal.rds.ui.clanWar.onClanWarStoneShield()
        elif skillId == gametypes.GUILD_SKILL_GATHER:
            gameglobal.rds.ui.guildCallMember.show()
        elif skillId in gametypes.GUILD_CROSS_SKILLS:
            self.cell.useGuildSkillInCrossServer(skillId)
            return
        self.cell.useGuildSkill(skillId)

    def onQueryClanWarApplyHost(self, data):
        gamelog.info('jbx:onQueryClanWarApplyHost', data)
        self.crossClanApllyList = data
