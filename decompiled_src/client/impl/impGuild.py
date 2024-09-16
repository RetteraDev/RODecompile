#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuild.o
from gamestrings import gameStrings
import os
import cPickle
import zlib
import BigWorld
import Math
import const
import gameglobal
import gametypes
import gamelog
import guildShopInvCommon
import commGuild
import utils
import formula
import commGSXY
from sfx import screenEffect
import logicInfo
from guis import events
from guis import uiConst
from guis import uiUtils
from gameStrings import gameStrings
from callbackHelper import Functor
from helpers.eventDispatcher import Event as UIEvent
from helpers.guild import Guild, Event, Member, Building, GuildPSkillVal, GuildSkill, GuildGroupVal, GuildResidentVal, GuildAreaVal, GuildBuildingMarkerVal, GuildFactoryVal, GuildTechnologyVal, GuildPayVal, GuildPayrollVal, GuildPayGroupVal, GuildWSPracticeVal, GuildNoviceBoostVal
from helpers.storageGuild import StorageGuild
from commGuild import GuildFactoryTaskVal, GuildResidentPSkillVal, GuildTutorialStepVal, GuildActivityVal, GuildMemberActionStatsVal
from helpers import navigator
from data import guild_building_data as GBD
from data import guild_static_entity_data as GSED
from data import guild_resident_template_data as GRTD
from data import npc_data as ND
from data import guild_area_data as GARD
from data import guild_factory_product_data as GFPD
from data import guild_building_marker_data as GBMD
from data import guild_technology_data as GTD
from data import guild_config_data as GCD
from data import guild_pskill_data as GPD
from data import guild_job_data as GJD
from data import guild_activity_data as GATD
from cdata import game_msg_def_data as GMDD
from data import quest_loop_data as QLD
from data import guild_resident_pskill_data as GRPD
from data import guild_run_man_route_data as GRMRD
from data import achievement_data as AD
from data import guild_skill_data as GSD
from cdata import guild_func_prop_def_data as GFNPDD

class ImpGuild(object):

    def onLoadGuild(self, gdata, appliedGuilds, isInCross):
        if isInCross:
            self.onLoadGuildInCross()
            return None
        data = cPickle.loads(zlib.decompress(gdata))
        dbID, nuid, name, spaceNo, roomId, yixinTeamId, state, tBuild, level, announcement, menifest, leaderRole, leaderGbId, creatorRole, creatorGbId, maxMember, hasSpace, donateWeekly, tLastDonate, res, merit, prosperity, scale, clanWarScore, stability, tMaintainDestroy, vitality, lastActiveNum, member, event, building, shop, buyRecord, skills, pskill, growth, matchItemId, match, privileges, group, clanWarFlagMorpher, storagePosCountDict, recommendedResident, hiredResident, marker, area, factory, technology, otherRes, cancelRes, tutorialStep, activity, reserveRes, payments, payrollGroup, businessMan, options, declareWarGuild, challengeInfo, pkEnemy, kindness, leaderAutoResignEndTime, chickenMealScore, fishActivityScore, monsterClanWarScore, bonfireDTO, guildYMFScore, guildNewFlagScore, signInNum, prestige, redPacketDTO, availRedPacketNum, guildMergerValDTO, tGuildMergerActivityStart, ignoreRecommendGuildMerger, guildNameFromMerger, isWingWorldYabiaoDoneWeekly, clanWarTgtHostId, clanWarCrossHostId, zhanhun, clanWarChallengeResult, skillcds, wingWorldCamp, wingWorldCampState, wwCampGuildList, wwCampMemberList, wingWorldCampFriendName, wingWorldCampEnemyName, wingWorldCampPower, yanwuQL, yanwuBH = data
        guild = Guild()
        guild.dbID = dbID
        guild.nuid = nuid
        guild.name = name
        guild.spaceNo = spaceNo
        guild.roomId = roomId
        guild.yixinTeamId = yixinTeamId
        guild.state = state
        guild.tBuild = tBuild
        guild.level = level
        guild.announcement = announcement
        guild.menifest = menifest
        guild.leaderRole = leaderRole
        guild.leaderGbId = leaderGbId
        guild.creatorRole = creatorRole
        guild.creatorGbId = creatorGbId
        guild.maxMember = maxMember
        guild.hasSpace = hasSpace
        guild.donateWeekly = donateWeekly
        guild.tLastDonate = tLastDonate
        bindCash, mojing, xirang, wood = res
        guild.bindCash = bindCash
        guild.mojing = mojing
        guild.xirang = xirang
        guild.wood = wood
        guild.clanWarScore = clanWarScore
        guild.stability = stability
        guild.tMaintainDestroy = tMaintainDestroy
        guild.vitality = vitality
        guild.lastActiveNum = lastActiveNum
        guild.merit = merit
        guild.prosperity = prosperity
        guild.scale = scale
        guild.privileges = privileges
        guild.clanWarFlagMorpher = clanWarFlagMorpher
        guild.otherRes = otherRes
        guild.cancelRes = cancelRes
        guild.updateReserveRes(reserveRes)
        enemyGuildNUIDs, enemyClanNUIDs = pkEnemy
        guild.enemyGuildNUIDs = set(enemyGuildNUIDs)
        guild.enemyClanNUIDs = set(enemyClanNUIDs)
        guild.businessMan = businessMan
        guild.options = options
        guild.setFlag()
        guild.kindness = kindness
        guild.chickenMealScore = chickenMealScore
        guild.fishActivityScore = fishActivityScore
        guild.monsterClanWarScore = monsterClanWarScore
        guild.guildYMFScore = guildYMFScore
        guild.guildNewFlagScore = guildNewFlagScore
        guild.signInNum = signInNum
        guild.prestige = prestige
        guild.guildMergerVal.fromDTO(guildMergerValDTO)
        guild.wingWorldCamp = wingWorldCamp
        guild.wingWorldCampState = wingWorldCampState
        guild.wwCampGuildList = wwCampGuildList
        guild.wwCampMemberList = wwCampMemberList
        guild.wingWorldCampFriend = wingWorldCampFriendName
        guild.wingWorldCampEnemy = wingWorldCampEnemyName
        guild.wingWorldCampPower = wingWorldCampPower
        if declareWarGuild:
            self.declareWarGuild = set(declareWarGuild)
        for mdto in member:
            member = Member().fromDTO(mdto)
            gbId = member.gbId
            guild.member[gbId] = member
            if gbId == self.gbId:
                guild.memberMe = guild.member[gbId]
                guild.memberMe.inMatch = False
                guild.memberMe.hasMatchItem = matchItemId > 0
                guild.memberMe.matchItemId = matchItemId
                guild.memberMe.matched = False
                guild.memberMe.matchGbId = 0
                guild.memberMe.payments = {}

        for edto in event:
            guild.event.append(Event().fromDTO(edto))

        guild.sortEvent()
        for buildingNUID, buildingId, level, tEnd, tStart, progress, markerId in building:
            guild.building[buildingNUID] = Building(nuid=buildingNUID, buildingId=buildingId, level=level, tEnd=tEnd, tStart=tStart, progress=progress, markerId=markerId)

        guild.storage = StorageGuild()
        guild.storage.posCountDict = storagePosCountDict
        guild.storage.version = 0
        guild.shop = []
        for shopType in gametypes.GUILD_SHOP_TYPE:
            gshop = guildShopInvCommon.GuildShopInvCommon()
            guild.shop.append(gshop)
            gshop.shopType = shopType
            gshop.tNextRefresh = 0
            for i in range(len(gshop.stamp)):
                gshop.stamp[i] = 0

            gshop.buyRecord = {}

        for shopData in shop:
            if shopData:
                guild.updateShop(shopData)

        guild.getShop(gametypes.GUILD_SHOP_TYPE_TREASURE).buyRecord = buyRecord
        for skillId, nextTime, duration in skills:
            guild.skills[skillId] = GuildSkill(skillId=skillId, nextTime=nextTime, duration=duration)

        for skillId, level, tStart, tEnd in pskill:
            guild.pskill[skillId] = GuildPSkillVal(skillId=skillId, level=level, tEnd=tEnd, tStart=tStart)

        for skillId, level in GPD.data.iterkeys():
            if not guild.pskill.has_key(skillId):
                guild.pskill[skillId] = GuildPSkillVal(skillId=skillId)

        guild.growth.fromDTO(growth)
        if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            for groupId, (name, _, _) in gametypes.GUILD_TOURNAMENT_GUILD_FAKE_GROUP.iteritems():
                guild.group[groupId] = GuildGroupVal(groupId=groupId, name=name)

        for groupId, name, tWhen, leaderGbId in group:
            guild.group[groupId] = GuildGroupVal(groupId=groupId, name=name, tWhen=tWhen, leaderGbId=leaderGbId)

        if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            if guild.group.has_key(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH):
                guild.group[gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH].name = gameStrings.TEXT_IMPGUILD_202
        else:
            guild.group.pop(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2, None)
        tMatchStart, tMatchEnd, matchRound, tMatchRoundEnd, matchScore, matches = match
        guild.tMatchStart = tMatchStart
        guild.tMatchEnd = tMatchEnd
        guild.matchRound = matchRound
        guild.tMatchRoundEnd = tMatchRoundEnd
        guild.matchScore = matchScore
        guild.matches = matches
        for dto in recommendedResident:
            resident = GuildResidentVal().fromDTO(dto)
            guild.recommendedResident[resident.nuid] = resident

        for dto in hiredResident:
            resident = GuildResidentVal().fromDTO(dto)
            guild.hiredResident[resident.nuid] = resident

        for dto in marker:
            m = GuildBuildingMarkerVal().fromDTO(dto)
            guild.marker[m.markerId] = m

        for dto in area:
            a = GuildAreaVal().fromDTO(dto)
            guild.area[a.areaId] = a

        for dto in factory:
            f = GuildFactoryVal().fromDTO(dto)
            guild.factory[f.type] = f

        for dto in technology:
            t = GuildTechnologyVal().fromDTO(dto)
            guild.technology[t.techId] = t

        for dto in tutorialStep:
            step = GuildTutorialStepVal().fromDTO(dto)
            guild.tutorialStep[step.stepId] = step

        for dto in activity:
            a = GuildActivityVal().fromDTO(dto)
            guild.activity[a.aid] = a

        for mtype in gametypes.GUILD_PAY_TYPE:
            payroll = GuildPayrollVal(mtype=mtype)
            guild.payroll[mtype] = payroll

        for mtype, dto in payrollGroup:
            payroll = guild.payroll.get(mtype)
            for gdto in dto:
                pgroup = GuildPayGroupVal().fromDTO(gdto)
                payroll.group[pgroup.serialNUID] = pgroup

        if hasattr(self, 'guildTutorialStep'):
            guild.tutorialStep.update(getattr(self, 'guildTutorialStep'))
            delattr(self, 'guildTutorialStep')
        self.appliedGuilds = appliedGuilds
        self.guild = guild
        commGuild.initWorkers(guild)
        self.onGuildPayments(guild.nuid, payments)
        for markerId in GBMD.data.iterkeys():
            if not guild.marker.has_key(markerId):
                marker = GuildBuildingMarkerVal(markerId=markerId)
                guild.marker[markerId] = marker

        for areaId in GARD.data.iterkeys():
            if not guild.area.has_key(areaId):
                area = GuildAreaVal(areaId=areaId)
                guild.area[areaId] = area

        for techId in GTD.data.iterkeys():
            if not guild.technology.has_key(techId):
                guild.technology[techId] = GuildTechnologyVal(techId=techId)

        for tech in guild.technology.itervalues():
            if tech.isAvail():
                tech.applyAbility(self.guild)

        for activity in guild.activity.itervalues():
            self._notifyGuildActivity(activity.aid)

        guild.bonfire.fromDTO(bonfireDTO)
        guild.redPacket.fromDTO(redPacketDTO)
        self.guild._applyBuildingAbilities()
        self.cell.getGuildOtherProperties()
        if guild.matchRound:
            self.onGuildMatchRoundStart(guild.matchRound, guild.tMatchRoundEnd, guild.matches, guild.memberMe.hasMatchItem)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        if self.isGuildLeader() and self.guild.state == gametypes.GUILD_STATE_ACTIVE and hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onActiveGuild()
        if guild.hasSpace and hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onHasGuildSpace()
        if self.guild and self.guild.clanWarFlagMorpher:
            try:
                clanWarFlagMorpher = eval(self.guild.clanWarFlagMorpher)
                if utils.isDownloadImage(clanWarFlagMorpher[2]):
                    self.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, clanWarFlagMorpher[2], gametypes.NOS_FILE_PICTURE, self.onGuildFlagIconDownloadNOSFile, ())
            except Exception as e:
                gamelog.error('@hjx onLoadGuild:', e)

        guild.challengeInfo = challengeInfo
        gameglobal.rds.ui.guild.checkChallengePushMsg()
        gameglobal.rds.ui.guildRename.checkRenamePushMsg()
        if len(gameglobal.rds.ui.offlineIncome.incomes):
            gameglobal.rds.ui.offlineIncome.notifyUIPushMsg()
        shop = guild.getShop(gametypes.GUILD_SHOP_TYPE_TREASURE)
        if shop and shop.tNextRefresh:
            self.cell.checkGuildShopRefresh(shop.shopType, shop.tNextRefresh)
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.cell.onGuildRobberInfoUpdate()
        self.cell.requireGuildFubenData(const.FB_NO_GUILD_FUBEN_ELITE)
        self._afterLoadGuild()
        if leaderAutoResignEndTime:
            self.onUpdateLeaderAutoResignTime(leaderAutoResignEndTime)
        if availRedPacketNum:
            self.notifyAvailGuildRedPacketNum(availRedPacketNum)
        self.guildMergeActivityStartTime = tGuildMergerActivityStart
        self.ignoreRecommendGuildMerger = ignoreRecommendGuildMerger
        self.isWingWorldYabiaoDoneWeekly = isWingWorldYabiaoDoneWeekly
        p = BigWorld.player()
        if getattr(p, 'wingWorldYabiaoPrivateGoods', None):
            self.wingWorldYabiaoPrivateGoods = p.wingWorldYabiaoPrivateGoods
            p.wingWorldYabiaoPrivateGoods = None
        gameglobal.rds.crossGuild = guild
        p.clanWarCrossHostId = clanWarCrossHostId
        p.crossClanWarTgtHostId = clanWarTgtHostId
        self.sendGuildSkill(skillcds)
        self.zhanHun = zhanhun
        self.yanwuQL = yanwuQL
        self.yanwuBH = yanwuBH
        return None

    def onLoadGuildInCross(self):
        if hasattr(gameglobal.rds, 'crossGuild'):
            self.guild = gameglobal.rds.crossGuild
        self._afterLoadGuild()

    def _afterLoadGuild(self):
        gameglobal.rds.ui.guildPuzzle.show()
        gameglobal.rds.ui.ymfScoreV2.refreshInfo()
        self.checkGuildBonfire()

    def updateGuildName(self, guildName):
        if not self.guild:
            return
        self.guild.name = guildName

    def onGuildResetWeekly(self):
        if not self.guild:
            return
        self.guild.matchScore = 0

    def isGuildIconDownloaded(self):
        myDir = const.IMAGES_DOWNLOAD_DIR
        if not os.path.exists(myDir):
            return False
        else:
            filePath = myDir + '\\' + self.guildIcon + '.dds'
            if os.path.isfile(filePath):
                return True
            return False

    def needDownloadGuildIcon(self):
        if self.guildIcon == '':
            return False
        if self.isGuildIconDownloaded():
            return False
        return True

    def isGuildIconUsed(self):
        if self.guildIcon == '':
            return False
        elif self.guildFlag == '':
            return False
        guildIcon, _ = uiUtils.getGuildFlag(self.guildFlag)
        if self.guildIcon == guildIcon:
            return True
        else:
            return False

    def onOpenCreateGuild(self, npcId):
        gameglobal.rds.ui.createGuild.show(npcId)

    def onOpenGuildList(self, npcId):
        gameglobal.rds.ui.applyGuild.getGuildData(npcId)

    def onChallengeQuery(self, score, memberNum, enemyMemberNum):
        if self != BigWorld.player():
            return
        self.guild.challengeScore = score
        self.guild.challengeInfo['memberNum'] = memberNum
        self.guild.challengeInfo['enemyMemberNum'] = enemyMemberNum
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)
        gameglobal.rds.ui.guildChallengeField.refreshInfo()

    def onUpdateChallengeScore(self, score):
        gamelog.debug('@hjx challenge#onUpdateChallengeScore:', self.roleName, score)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        self.guild.challengeScore = score
        gameglobal.rds.ui.guildChallengeField.refreshInfo()

    def onUpdateChallengeStatus(self, status):
        gamelog.debug('@hjx challenge#onUpdateChallengeStatus:', self.roleName, status)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['status'] = status
        gameglobal.rds.ui.guild.refreshChallengeInfo(True)

    def onUpdateChallengeMemberNum(self, memberNum):
        gamelog.debug('@hjx challenge#onUpdateChallengeMemberNum:', self.roleName, memberNum)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['memberNum'] = memberNum
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)

    def onUpdateChallengeEnemyMemberNum(self, enemyMemberNum):
        gamelog.debug('@hjx challenge#onUpdateChallengeEnemyMemberNum:', self.roleName, enemyMemberNum)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['enemyMemberNum'] = enemyMemberNum
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)

    def onUpdateChallengeNum(self, memberNum, enemyMemberNum):
        gamelog.debug('@hjx challenge#onUpdateChallengeNum:', self.roleName, memberNum, enemyMemberNum)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['memberNum'] = memberNum
        guild.challengeInfo['enemyMemberNum'] = enemyMemberNum
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)

    def onUpdateGuildAnnouncement(self, guildNUID, announcement):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.announcement = announcement
        gameglobal.rds.ui.guild.updateAnnouncement()
        if announcement:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GUILD, gameStrings.TEXT_IMPGUILD_500 + uiUtils.htmlToText(announcement), '')

    def onUpdateGuildMenifest(self, guildNUID, menifest):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.menifest = menifest
        gameglobal.rds.ui.guildMenifest.hide()
        gameglobal.rds.ui.guild.updateMenifest()
        if menifest:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GUILD, gameStrings.TEXT_IMPGUILD_509 + menifest, '')

    def onUpdateGuild(self, data):
        guild = BigWorld.player().guild
        if guild:
            for k, v in data.iteritems():
                setattr(guild, k, v)

    def onUpdateGuildRoom(self, guildNUID, roomId, password):
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.roomId = roomId

    def onUpdateGuildYixinTeam(self, guildNUID, yixinTeamId):
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.yixinTeamId = yixinTeamId

    def onQueryGuildList(self, state, totalPages, page, sortBy, reverse, data):
        guildData = []
        gameglobal.rds.ui.applyGuild.dbID2nuid.clear()
        for item in data:
            gameglobal.rds.ui.applyGuild.dbID2nuid[item[1]] = item[0]
            guildItem = list(item[1:])
            guildItem[0] = str(guildItem[0])
            guildItem[9] = gameStrings.TEXT_IMPGUILD_538 if guildItem[9] < 50 else str(guildItem[9])
            guildItem.append(gameStrings.TEXT_IMPGUILD_539 if guildItem[6] >= guildItem[7] else gameStrings.TEXT_IMPGUILD_539_1)
            guildData.append(guildItem)

        if gameglobal.rds.ui.applyGuild.mediator:
            gameglobal.rds.ui.applyGuild.refreshInfo(state, totalPages, page, guildData, sortBy, reverse)
        else:
            gameglobal.rds.ui.applyGuild.show(state, totalPages, page, guildData, sortBy, reverse)

    def onQueryGuild(self, data):
        pass

    def onSearchPlayerForGuild(self, infoList):
        infoList = cPickle.loads(zlib.decompress(infoList))

    def refreshApplyList(self):
        gameglobal.rds.ui.guildMember.getGuildApplyList()

    def onGetApplyList(self, guildNUID, totalPages, page, applyList):
        data = []
        for member in applyList:
            gbId, role, level, school, _ = member
            data.append([str(gbId),
             uiUtils.toMenuName(role, gbId),
             level,
             const.SCHOOL_DICT[school]])

        gameglobal.rds.ui.guildMember.show(data)

    def onInviteGuildMember(self, fRole, guildNUID, guildName):
        if self.guild:
            gamelog.debug('already joined, ingore any invite')
            return
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPGUILD_571 % (fRole, guildName), Functor(self.cell.acceptGuildInvite, guildNUID), gameStrings.TEXT_IMPFRIEND_2211, Functor(self.cell.rejectGuildInvite, guildNUID), gameStrings.TEXT_IMPFRIEND_963, False)

    def onGuildApply(self, fGbId, fRole):
        if not gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GUILD_APPLY):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_APPLY, {'data': 'data'})

    def onGuildApplied(self, guildNUID, guildName):
        if guildNUID not in self.appliedGuilds:
            self.appliedGuilds.append(guildNUID)
        self.showGameMsg(GMDD.data.GUILD_APPLY_JOIN_OK, (guildName,))

    def onGuildApplyRejected(self, guildNUID, guildName):
        if guildNUID in self.appliedGuilds:
            self.appliedGuilds.remove(guildNUID)
            self.showGameMsg(GMDD.data.GUILD_APPLY_REJECTED, (guildName,))

    def onGuildsApplyRejected(self, guildNUIDs):
        for nuid in guildNUIDs:
            if nuid in self.appliedGuilds:
                self.appliedGuilds.remove(nuid)

    def onGuildApplyCancelled(self, guildNUID, guildName):
        if guildNUID in self.appliedGuilds:
            self.appliedGuilds.remove(guildNUID)
            self.showGameMsg(GMDD.data.GUILD_APPLY_CANCELLED, (guildName,))

    def onGuildApplyAccpeted(self, guildNUID, guildName):
        self.appliedGuilds = []
        self.showGameMsg(GMDD.data.GUILD_APPLY_ACCEPTED, (guildName,))

    def onGuildEvent(self, guildNUID, event):
        event = Event().fromDTO(event)
        skipEventId = GCD.data.get('skipEventMsgIds', ())
        if event.msgId not in skipEventId:
            self.showGameMsg(event.msgId, event.args)
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.addEvent(event)
        self.guild.sortEvent()
        gameglobal.rds.ui.guild.addEvent(event)

    def onGuildAcceptInvite(self, guildNUID, guildName):
        self.appliedGuilds = []
        self.showGameMsg(GMDD.data.GUILD_ACCEPT_INVITE, (guildName,))

    def onGuildRejectInvite(self, guildNUID, guildName):
        if guildNUID in self.appliedGuilds:
            self.appliedGuilds.remove(guildNUID)
            self.showGameMsg(GMDD.data.GUILD_REJECT_INVITE, (guildName,))

    def onGuildAddMember(self, guildNUID, gbId, member):
        if self.guild:
            self.guild.addMember(gbId, Member().fromDTO(member))
        gameglobal.rds.ui.guild.refreshMemberInfo()
        gameglobal.rds.ui.guildBonfire.refreshInfo()
        gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()

    def onGuildAddMembers(self, newMembers):
        if self.guild:
            for gbId, member in newMembers:
                self.guild.addMember(gbId, Member().fromDTO(member))

        gameglobal.rds.ui.guild.refreshMemberInfo()
        gameglobal.rds.ui.guildBonfire.refreshInfo()
        gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()

    def onGuildDelMember(self, guildNUID, gbId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.delMember(gbId)
        gameglobal.rds.ui.guild.refreshMemberInfo()
        gameglobal.rds.ui.guildBonfire.refreshInfo()
        gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()

    def clearGuildApplies(self):
        self.appliedGuilds = []

    def onLeaveGuild(self, guildNUID, guildName):
        self.guild = None
        self.showGameMsg(GMDD.data.GUILD_LEAVE, (guildName,))
        self.hideGuildUI()
        self.clanWar.reliveBoard.clear()
        gameglobal.rds.ui.cCControl.refreshPanel()
        self.clearDeclareWar()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        gameglobal.rds.ui.actionbar.clearGuildSkillShortCut()
        gameglobal.rds.ui.ycwzRankList.setClanWarAttendInfo((0, 0))
        gameglobal.rds.ui.guildPuzzle.hide()
        gameglobal.rds.ui.guildBonfire.hide()
        gameglobal.rds.ui.bFGuildTournamentLive.clearAllPanel()

    def onGuildKickedout(self, guildNUID, guildName):
        self.guild = None
        self.showGameMsg(GMDD.data.GUILD_KICKEDOUT, (guildName,))
        self.hideGuildUI()
        self.clanWar.reliveBoard.clear()
        self.clearDeclareWar()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        gameglobal.rds.ui.actionbar.clearGuildSkillShortCut()
        gameglobal.rds.ui.ycwzRankList.setClanWarAttendInfo((0, 0))
        gameglobal.rds.ui.guildPuzzle.hide()

    def onGuildResign(self, guildNUID, leaderGbId, leaderRole):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        oldLeaderGbId = self.guild.leaderGbId
        self.guild.leaderGbId = leaderGbId
        self.guild.leaderRole = leaderRole
        oldLeader = self.guild.member.get(oldLeaderGbId)
        leader = self.guild.member.get(leaderGbId)
        if oldLeader:
            oldLeader.roleId = gametypes.GUILD_ROLE_NORMAL
        if leader:
            leader.roleId = gametypes.GUILD_ROLE_LEADER
        if oldLeaderGbId == self.gbId:
            gameglobal.rds.ui.guild.updateAuthorization()
            gameglobal.rds.ui.guildAuthorization.updateRoleID()
            self.guild.resetPayrollCache()
        elif leaderGbId == self.gbId:
            gameglobal.rds.ui.guild.updateAuthorization()
            gameglobal.rds.ui.guildAuthorization.updateRoleID()
            self.guild.resetPayrollCache()
        gameglobal.rds.ui.guild.updateMember(oldLeaderGbId)
        gameglobal.rds.ui.guild.updateMember(leaderGbId)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        if self.isGuildLeader() and self.guild.state == gametypes.GUILD_STATE_ACTIVE and hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onActiveGuild()

    def onGuildAppoint(self, guildNUID, gbId, roleId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.roleId = roleId
            gameglobal.rds.ui.guild.updateMember(gbId)
        if self.gbId == gbId:
            gameglobal.rds.ui.guild.updateAuthorization()
            gameglobal.rds.ui.guildAuthorization.updateRoleID()
            gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)

    def onGuildDonateMe(self, guildNUID, contrib, contribTotal):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.memberMe.contrib = contrib
        self.guild.memberMe.contribTotal = contribTotal

    def onGuildDonate(self, guildNUID, donateWeekly, tLastDonate, res, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.donateWeekly = donateWeekly
        self.guild.tLastDonate = tLastDonate
        self.guild.otherRes.update(otherRes)
        self.guild.updateRes(res)

    def onGuildUpdateBindCash(self, guildNUID, bindCash):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.updateRes((bindCash,
         self.guild.mojing,
         self.guild.xirang,
         self.guild.wood))

    def onGuildUpdateReserveRes(self, guildNUID, reserveRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.updateReserveRes(reserveRes)
        gameglobal.rds.ui.guildSalaryAssign.refreshView()

    def onGuildUpdateRes(self, guildNUID, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.updateRes(res)

    def onGuildUpdateOtherRes(self, guildNUID, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if not otherRes:
            return
        self.guild.otherRes.update(otherRes)
        self.guild.refreshRes()

    def onGuildUpdateAllRes(self, guildNUID, res, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.otherRes.update(otherRes)
        self.guild.updateRes(res)

    def onGuildUpdateContrib(self, guildNUID, gbId, contrib, contribTotal):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.contrib = contrib
        member.contribTotal = contribTotal

    def onGuildMemberCombatScoreUpdate(self, guildNUID, gbId, combatScore):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.combatScore = combatScore
        gameglobal.rds.ui.guildMembersFbRank.refreshInfo()

    def onGuildMemberWWContriUpdate(self, guildNUID, gbId, contri):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.wingWorldContri = contri
        gameglobal.rds.ui.wingCampGuildList.refreshInfo()

    def onGuildMemberActivityDictUpdate(self, guildNUID, gbId, activityDict):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.activityDict = activityDict

    def onGuildUpdateLuxury(self, guildNUID, gbId, luxury):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.luxury = luxury

    def onGuildUpgrade(self, guildNUID, guildLevel, guildBindCash):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.level = guildLevel
        self.guild.bindCash = guildBindCash
        self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guildPuzzle.hide()

    def onGuildDismiss(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            self.guild = None
            self.showGameMsg(GMDD.data.GUILD_DISMISS, ())
            self.hideGuildUI()
            self.clanWar.reliveBoard.clear()
            self.clearDeclareWar()
            gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
            gameglobal.rds.ui.actionbar.clearGuildSkillShortCut()
            gameglobal.rds.ui.ycwzRankList.setClanWarAttendInfo((0, 0))
            gameglobal.rds.ui.guildPuzzle.hide()
            gameglobal.rds.ui.guildBonfire.hide()
            return

    def onGuildMemberOnline(self, guildNUID, gbId, level, spaceNo, areaId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.online = True
            member.level = level
            member.spaceNo = spaceNo
            member.areaId = areaId
            gameglobal.rds.ui.guild.refreshMemberInfo()
            gameglobal.rds.ui.guildBonfire.refreshInfo()
            gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()
            self.showGameMsg(GMDD.data.GUILD_MEMBER_ONLINE_NOTIFY, (gametypes.GUILD_ROLE_DICT.get(member.roleId), member.role))

    def onGuildMemberOffline(self, guildNUID, gbId, tLastOnline):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.online = False
            member.tLastOnline = tLastOnline
            gameglobal.rds.ui.guild.refreshMemberInfo()
            gameglobal.rds.ui.guildBonfire.refreshInfo()
            gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()

    def onGuildMemberLevelUpdate(self, guildNUID, gbId, level):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.level = level

    def onGuildMemberSpaceNoUpdate(self, guildNUID, gbId, spaceNo):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.spaceNo = spaceNo
            gameglobal.rds.ui.guildBonfire.refreshInfo()

    def onGuildMemberAreaIdUpdate(self, guildNUID, gbId, spaceNo, areaId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.spaceNo = spaceNo
            member.areaId = areaId

    def onGuildMemberSchoolUpdate(self, guildNUID, gbId, school):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if member:
            member.school = school

    def onGuildActive(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.state = gametypes.GUILD_STATE_ACTIVE
        self.guild.tMaintainDestroy = 0
        if self.isGuildLeader() and hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onActiveGuild()

    def onGuildMemberRename(self, guildNUID, gbId, name):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.member[gbId].role = name
        if self.guild.leaderGbId == gbId:
            self.guild.leaderRole = name
        if self.guild.creatorGbId == gbId:
            self.guild.creatorRole = name

    def hideGuildUI(self):
        if gameglobal.rds.ui.guild.mediator:
            gameglobal.rds.ui.guild.hide()
        if gameglobal.rds.ui.guildAnnouncement.mediator:
            gameglobal.rds.ui.guildAnnouncement.hide()
        if gameglobal.rds.ui.guildMember.mediator:
            gameglobal.rds.ui.guildMember.hide()
        if gameglobal.rds.ui.guildMemberAssgin.mediator:
            gameglobal.rds.ui.guildMemberAssgin.hide()
        if gameglobal.rds.ui.guildPost.mediator:
            gameglobal.rds.ui.guildPost.hide()
        if gameglobal.rds.ui.guildAuthorization.mediator:
            gameglobal.rds.ui.guildAuthorization.hide()
        if gameglobal.rds.ui.guildBuildSelect.mediator:
            gameglobal.rds.ui.guildBuildSelect.hide()
        if gameglobal.rds.ui.guildBuildUpgrade.mediator:
            gameglobal.rds.ui.guildBuildUpgrade.hide()
        if gameglobal.rds.ui.guildAssart.mediator:
            gameglobal.rds.ui.guildAssart.hide()
        if gameglobal.rds.ui.guildBuildSelectRemove.mediator:
            gameglobal.rds.ui.guildBuildSelectRemove.hide()
        if gameglobal.rds.ui.guildBuildRemove.mediator:
            gameglobal.rds.ui.guildBuildRemove.hide()
        if gameglobal.rds.ui.guildDonate.mediator:
            gameglobal.rds.ui.guildDonate.hide()
        if gameglobal.rds.ui.guildDonateReserve.mediator:
            gameglobal.rds.ui.guildDonateReserve.hide()
        if gameglobal.rds.ui.guildInherit.widget:
            gameglobal.rds.ui.guildInherit.hide()
        if gameglobal.rds.ui.guildAuction.widget:
            gameglobal.rds.ui.guildAuction.hide()
        gameglobal.rds.ui.guildRedPacket.hideRelateUI()
        gameglobal.rds.ui.guildAuctionGuild.clearAll()
        gameglobal.rds.ui.guildAuctionGuild.updateOpenPushMsg()
        gameglobal.rds.ui.guild.hideAllGuildBuilding()
        gameglobal.rds.ui.guildRobberActivityPush.activityEnd(False, 0)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_CHALLENGE)

    def set_guildNUID(self, old):
        if self.inClanWar and old != self.guildNUID:
            if BigWorld.player() == self:
                self._updateClanWarTopLogo()
            else:
                BigWorld.player()._updateClanWarTopLogoByEntId(self.id)
        if BigWorld.player() == self:
            gameglobal.rds.ui.chat.updatePadChannels()
        if BigWorld.player() == self and gameglobal.gHidePlayerGuild or BigWorld.player() != self and gameglobal.gHideAvatarGuild:
            return
        if self.topLogo:
            if self.guildNUID:
                self.topLogo.addGuildIcon(self.guildFlag)
                gameglobal.rds.ui.guild.updateFlag()
            else:
                self.topLogo.removeGuildIcon()
        if BigWorld.player().clanWarStatus and BigWorld.player().targetLocked == self:
            BigWorld.player().refreshTargetLocked()
        if BigWorld.player() == self and old > 0 and self.guildNUID == 0:
            gameglobal.rds.ui.zhanQi.morpherFactory.reset()

    def set_guildFlag(self, old):
        if BigWorld.player() == self and gameglobal.gHidePlayerGuild or BigWorld.player() != self and gameglobal.gHideAvatarGuild:
            return
        if self.topLogo:
            if self.guildNUID:
                self.topLogo.addGuildIcon(self.guildFlag)
                if BigWorld.player() == self:
                    gameglobal.rds.ui.guild.updateFlag()
            else:
                self.topLogo.removeGuildIcon()

    def set_guildIcon(self, old):
        gamelog.info('@hjx set_guildIcon:', old, self.guildIcon)
        if self == BigWorld.player() and self.guildIcon:
            p = BigWorld.player()
            if p.guildIconStatus == gametypes.NOS_FILE_STATUS_PENDING:
                p.downloadNOSFileDirectly(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.guildIcon, gametypes.NOS_FILE_PICTURE, p.onGuildIconDownloadNOSFileDirectly, (None,))

    def set_guildIconStatus(self, old):
        if self == BigWorld.player():
            gameglobal.rds.ui.zhanQi.refreshUserDefineInfo()

    def set_guildActivityIcon(self, old):
        if not self.topLogo:
            return
        if self.guildActivityIcon > 0:
            self.topLogo.setFindLogo(self.guildActivityIcon)
        else:
            self.topLogo.removeFindLogo()

    def set_guildContrib(self, old):
        delta = self.guildContrib - old
        if delta > 0:
            self.showGameMsg(GMDD.data.GUILD_CONTRIB_ADD, (delta,))
        elif delta < 0:
            self.showGameMsg(GMDD.data.GUILD_CONTRIB_DEC, (-delta,))
        gameglobal.rds.ui.topBar.setValueByName('guildContrib')

    def isGuildLeader(self):
        return self.guild and self.guild.leaderGbId == self.gbId

    def isGuildLeaders(self):
        return self.isGuildLeader() or self.guildRole in gametypes.GUILD_ROLE_LEADERS

    def updateClanWarFlag(self, newMorpher):
        if not self.guildNUID:
            return
        mVal = self.guild.member.get(self.gbId)
        if not mVal:
            return
        if mVal.roleId not in gametypes.GUILD_ROLE_LEADERS:
            self.showGameMsg(GMDD.data.UPDATE_CLANWAR_FLAG_FAIL_DENY, ())
            return
        newMorpherDict = eval(newMorpher)
        try:
            flag = str(newMorpherDict[2]) + const.SYMBOL_GUILD_FLAG_SPLIT + str(newMorpherDict[5])
        except:
            flag = ''
            gamelog.error('error in updateClanWarFlag!')
            return

        self.cell.updateClanWarFlag(newMorpher, flag)

    def onUpdateClanWarFlag(self, newMorpher):
        if not self.guildNUID or not self.guild:
            return
        self.guild.clanWarFlagMorpher = newMorpher
        self.guild.setFlag()
        gameglobal.rds.ui.guild.updateFlag()
        if gameglobal.rds.ui.createGuild.headGen:
            gameglobal.rds.ui.zhanQi.applyTint(gameglobal.rds.ui.createGuild.headGen)
        if gameglobal.rds.ui.guild.flagGen:
            gameglobal.rds.ui.zhanQi.applyTint(gameglobal.rds.ui.guild.flagGen)
        self.showGameMsg(GMDD.data.ZHAN_QI_SAVE_SUCC, ())

    def onQueryGuildFlag(self, guildNUID, morpher):
        gameglobal.rds.ui.applyGuild.updateFlag(guildNUID, morpher)

    def getGuildIconStatus(self):
        if hasattr(self, 'guildIconStatus'):
            return self.guildIconStatus
        else:
            return gametypes.NOS_FILE_STATUS_PENDING

    def onGuildUpdatePrivileges(self, guildNUID, rolePrivileges):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        for roleId, privileges in rolePrivileges.iteritems():
            self.guild.privileges[roleId] = privileges

        gameglobal.rds.ui.guild.updateAuthorization()

    def onGuildUpdateClanWarScore(self, guildNUID, clanWarScore):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.clanWarScore = clanWarScore

    def onGuildGetOtherProperties(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        prosperity, = data
        self.guild.prosperity = prosperity
        gameglobal.rds.ui.guild.refreshProsperityInfo()

    def onGuildGetKindness(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        kindness, = data
        self.guild.kindness = kindness

    def onGuildGetChickenMealScore(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        chickenMealScore, = data
        self.guild.chickenMealScore = chickenMealScore

    def onGuildGetFishActivityScore(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        fishActivityScore, = data
        self.guild.fishActivityScore = fishActivityScore

    def onGuildGetMonsterClanWarScore(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        monsterClanWarScore, = data
        self.guild.monsterClanWarScore = monsterClanWarScore

    def onGuildGetYMFScore(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        guildYMFScore, = data
        self.guild.guildYMFScore = guildYMFScore
        gameglobal.rds.ui.ymfScoreV2.refreshInfo()

    def onGuildBuildingUpgradeStart(self, guildNUID, buildingNUID, buildingId, tStart, markerId, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if not self.guild.building.has_key(buildingNUID):
            self.guild.building[buildingNUID] = Building(nuid=buildingNUID, buildingId=buildingId, tStart=tStart, markerId=markerId)
            self.guild.marker[markerId].buildingNUID = buildingNUID
        self.guild.building.get(buildingNUID).tStart = tStart
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_BUILDING_UPGRADE_START, (GBD.data.get(buildingId).get('name'),))
        self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guild.refreshSingleBuildInfo(markerId)
        gameglobal.rds.ui.guildBuildUpgrade.setInitData()

    def onGuildBuildingUpgradeFinish(self, guildNUID, r):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            for buildingNUID, level in r:
                building = self.guild.building.get(buildingNUID, None)
                if not building:
                    continue
                building.level = level
                building.stopUpgrading(self.guild)
                if building.buildingId == gametypes.GUILD_BUILDING_MASTER_ID:
                    self.guild.level = level
                    self.guild.maxMember = self.guild._getMaxMember()
                elif building.buildingId == gametypes.GUILD_BUILDING_HOUSE_ID:
                    self.guild.maxMember = self.guild._getMaxMember()
                self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_BUILDING, building.markerId)
                gameglobal.rds.ui.guild.refreshSingleBuildInfo(building.markerId)
                gameglobal.rds.ui.guildBuildUpgrade.upgradeFinish(building.nuid)
                gameglobal.rds.ui.guildBuildRemove.hideByMarkerId(building.markerId)

            self.onQuestInfoModifiedAtClient(const.QD_GUILD)
            gameglobal.rds.ui.guild.refreshAllResidentProxy()
            gameglobal.rds.ui.guildBuildSelectRemove.refreshInfo()
            return

    def onGuildBuildingUpgradeCancel(self, guildNUID, buildingNUID, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        building = self.guild.building.get(buildingNUID)
        building.tStart = 0
        building.stopUpgrading(self.guild)
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_BUILDING_UPGRADE_CANCEL, (GBD.data.get(building.buildingId).get('name'),))
        if building.level == 0:
            self.guild.building.pop(buildingNUID)
            self.guild.marker[building.markerId].buildingNUID = 0
        self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_BUILDING, building.markerId)
        self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guild.refreshSingleBuildInfo(building.markerId)
        gameglobal.rds.ui.guildBuildUpgrade.setInitData()
        gameglobal.rds.ui.guild.refreshAllResidentProxy()

    def onGuildRemoveBuilding(self, guildNUID, buildingNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        building = self.guild.building.get(buildingNUID)
        building.tStart = 0
        self.guild.marker[building.markerId].buildingNUID = 0
        self.guild.building.pop(buildingNUID)
        if building.buildingId == gametypes.GUILD_BUILDING_HOUSE_ID:
            self.guild.maxMember = self.guild._getMaxMember()
        gameglobal.rds.ui.guild.refreshSingleBuildInfo(building.markerId)
        gameglobal.rds.ui.guildBuildUpgrade.setInitData()
        gameglobal.rds.ui.guildBuildRemove.hideByMarkerId(building.markerId)
        gameglobal.rds.ui.guildBuildSelectRemove.refreshInfo()

    def onGuildAstrology(self, idx, astrologyId):
        gameglobal.rds.ui.guildFindStar.beginFindStar(idx)

    def onGuildAstrologyFailed(self):
        gameglobal.rds.ui.guildFindStar.astrologyFailed()

    def sendGuildGrowth(self, dto):
        self.guildGrowth.fromDTO(dto)

    def onGuildPSkillUpgradeStart(self, guildNUID, pskillId, tEnd, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        pskill = self.guild.getPSkill(pskillId)
        pskill.tStart = utils.getNow()
        pskill.tEnd = tEnd
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_PSKILL_UPGRADE_START, (pskill.level + 1, commGuild.getPSkillName(pskillId)))
        gameglobal.rds.ui.guildGrowth.updateResearchPSkillNode(pskillId)

    def onGuildPSkillUpgradeFinish(self, guildNUID, r):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        for pskillId, level in r:
            pskill = self.guild.getPSkill(pskillId)
            pskill.level = level
            pskill.tStart = 0
            pskill.tEnd = 0
            self.showGameMsg(GMDD.data.GUILD_PSKILL_UPGRADE_FINISH, (pskill.level, commGuild.getPSkillName(pskillId)))
            self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_PSKILL, pskillId)
            gameglobal.rds.ui.guildGrowth.updateResearchPSkillNode(pskillId)

    def onGuildPSkillUpgradeCancel(self, guildNUID, pskillId, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        pskill = self.guild.getPSkill(pskillId)
        pskill.tStart = 0
        pskill.tEnd = 0
        pskill.stop()
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_BUILDING_UPGRADE_CANCEL, (commGuild.getPSkillName(pskillId),))
        self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_PSKILL, pskillId)
        gameglobal.rds.ui.guildGrowth.updateResearchPSkillNode(pskillId)

    def onGuildGrowthUpgrade(self, guildNUID, volumnId, propertyId, level, res, propName):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        volumn = self.guild.getGrowthVolumn(volumnId)
        growth = volumn.getGrowth(propertyId)
        growth.level = level
        growth.active = True
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_GROWTH_ACTIVATED, (propName,))
        gameglobal.rds.ui.guildGrowth.updateLearnGrowthTree(volumnId, propertyId)
        gameglobal.rds.ui.guildGrowth.updateActivateGrowthTree(volumnId, propertyId)

    def onGuildGrowthDeactivated(self, guildNUID, volumnId, propertyId, level, propName):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        volumn = self.guild.getGrowthVolumn(volumnId)
        growth = volumn.getGrowth(propertyId)
        growth.level = level
        growth.active = False
        self.showGameMsg(GMDD.data.GUILD_GROWTH_DEACTIVATED, (propName,))
        gameglobal.rds.ui.guildGrowth.updateLearnGrowthTree(volumnId, propertyId)
        gameglobal.rds.ui.guildGrowth.updateActivateGrowthTree(volumnId, propertyId)

    def onLearnGuildGrowth(self, guildNUID, volumnId, propertyId, level, score, propName):
        if guildNUID and (not self.guild or guildNUID != self.guild.nuid):
            return
        volumn = self.guildGrowth.getVolumn(volumnId)
        volumn.score = score
        growth = volumn.getGrowth(propertyId)
        growth.level = level
        self.showGameMsg(GMDD.data.GUILD_LEARN_GROWTH, (level, propName))
        gameglobal.rds.ui.guildGrowth.updateLearnGrowthTree(volumnId, propertyId)
        gameglobal.rds.ui.guildGrowth.updateRewardBtnRedPot()

    def sendGuildSkill(self, data):
        bwTime = BigWorld.time()
        serverTime = self.getServerTime()
        for skillInfo in data:
            if len(skillInfo) == 3:
                skillId, nextTime, duration = skillInfo
            else:
                skillId, nextTime = skillInfo
                duration = GSD.data.get(skillId, {}).get('stateTime', 0)
            self.guildSkills[skillId] = GuildSkill(skillId=skillId, nextTime=nextTime, duration=duration)
            if nextTime > serverTime:
                skillcd = GSD.data.get(skillId, {}).get('cd', 0)
                end = nextTime - serverTime + bwTime
                logicInfo.cooldownClanWarSkill[skillId] = (end, skillcd)

        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.clanWarSkill.updateSlots()

    def onUpdateGuildSkill(self, guildNUID, bPlayer, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        serverTime = self.getServerTime()
        bwTime = BigWorld.time()
        skillId, nextTime, duration = data
        if bPlayer:
            if self.guildSkills.has_key(skillId):
                self.guildSkills[skillId].nextTime = nextTime
            else:
                self.guildSkills[skillId] = GuildSkill(skillId=skillId, nextTime=nextTime, duration=duration)
        elif self.guild.skills.has_key(skillId):
            self.guild.skills[skillId].nextTime = nextTime
        else:
            self.guild.skills[skillId] = GuildSkill(skillId=skillId, nextTime=nextTime, duration=duration)
        if nextTime > serverTime:
            skillcd = GSD.data.get(skillId, {}).get('cd', 0)
            end = nextTime - serverTime + bwTime
            logicInfo.cooldownClanWarSkill[skillId] = (end, skillcd)
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.clanWarSkill.updateSlots()

    def onUpdateGuildSkillCDAll(self, data):
        """
        :param data: [(skillId, nextTime), ...]
        :return:
        """
        gamelog.info('jbx:onUpdateGuildSkillCDAll', data)
        self.sendGuildSkill(data)

    def onGuildMatchStart(self, tMatchStart, tMatchEnd, matchRound, tMatchRoundEnd, matches, res, stability):
        if not self.guild:
            return
        self.guild.updateRes(res)
        self.guild.stability = stability
        self.guild.tMatchStart = tMatchStart
        self.guild.tMatchEnd = tMatchEnd
        self.guild.matchRound = matchRound
        self.guild.matches = matches
        self.showGameMsg(GMDD.data.GUILD_MATCH_START, ())
        self.onGuildMatchRoundStart(matchRound, tMatchRoundEnd, matches)

    def onGuildMatchEnd(self):
        if not self.guild:
            return
        self.guild.matchRound = 0
        self.guild.matches.clear()
        self.showGameMsg(GMDD.data.GUILD_MATCH_END, ())
        gameglobal.rds.ui.guildActivity.refreshState()
        if gameglobal.rds.ui.guildActivityTime.mediator:
            gameglobal.rds.ui.guildActivityTime.hide()
        self._hideGuildMatchItemPushMessage()
        self.clearAllGuildConnector()

    def onGuildMatchRoundStart(self, matchRound, tMatchRoundEnd, matches, hasMatchItem = True):
        if not self.guild:
            return
        if gameglobal.rds.ui.guildActivityTime.mediator:
            gameglobal.rds.ui.guildActivityTime.hide()
        self.guild.matchRound = matchRound
        self.guild.tMatchRoundEnd = tMatchRoundEnd
        self.guild.matches = matches
        self.guild.memberMe.inMatch = False
        self.guild.memberMe.hasMatchItem = False
        self.guild.memberMe.matchItemId = 0
        self.guild.memberMe.matched = False
        self.guild.memberMe.matchGbId = 0
        for gbIdPair in matches.keys():
            if self.gbId in gbIdPair:
                self.guild.memberMe.inMatch = True
                self.guild.memberMe.matched = matches[gbIdPair]
                for tGbId in gbIdPair:
                    if self.gbId != tGbId:
                        self.guild.memberMe.matchGbId = tGbId
                        break

                self._setGuildHasMatchItem(hasMatchItem)
                if hasMatchItem:
                    if matches.has_key((self.gbId, 0)):
                        self.guild.memberMe.matchItemId = const.GUILD_MATCH_INSTANT_ITEM_ID
                    else:
                        self.guild.memberMe.matchItemId = const.GUILD_MATCH_ITEM_ID
                break

        self.showGameMsg(GMDD.data.GUILD_MATCH_ROUND_START, (matchRound,))
        gameglobal.rds.ui.guildActivity.refreshState()
        gameglobal.rds.ui.guildActivity.refreshList()
        self.clearAllGuildConnector()

    def onGuildMatchOK(self, fGbId, toGbId, matchScore):
        if not self.guild:
            return
        self.guild.matchScore = matchScore
        self.guild.matches[fGbId, toGbId] = utils.getNow()
        self.guild.memberMe.matched = True
        gameglobal.rds.ui.guildActivity.refreshList()
        gameglobal.rds.ui.guildActivityTime.show()

    def onGuildMatchEffect(self, fEntId, toEntId):
        e = BigWorld.entities.get(fEntId)
        if e:
            e.playGuildConnectEffect(toEntId, const.GUILD_MATCH_EFFECT_DURATION)

    def resetGuildMatchItem(self):
        if not self.guild:
            return
        self._setGuildHasMatchItem(False)

    def _setGuildHasMatchItem(self, v):
        self.guild.memberMe.hasMatchItem = v
        if v:
            self._showGuildMatchPushMessage()
        else:
            self._hideGuildMatchItemPushMessage()
            gameglobal.rds.ui.guildActivityTime.show()

    def _showGuildMatchPushMessage(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM)

    def _hideGuildMatchItemPushMessage(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM)
        gameglobal.rds.ui.guildActivity.hideMatchItem()

    def onGuildActivityStart(self, guildNUID, activityDTO, res, stability):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.updateRes(res)
        self.guild.stability = stability
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        gameglobal.rds.ui.guildActivity.refreshActivityState(activityId)
        self._notifyGuildActivity(activityId)

    def onGuildActivityUpdate(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        gameglobal.rds.ui.guildActivity.refreshActivityState(activityId)

    def _notifyGuildActivity(self, activityId):
        activity = self.guild._getActivity(activityId)
        if not activity or activity.getState() != gametypes.GUILD_ACTIVITY_GOING:
            return
        data = GATD.data.get(activityId)
        if not data.get('notifyMsgId'):
            return
        cnt = data.get('notifyCnt', 3)
        self.showSysNotification(data.get('notifyMsgId'), (data.get('name', ''),), 1, data.get('notifyInterval', 10), finishCallback=lambda activityId = activityId, cnt = cnt: self._afterNotifyGuildActivity(activityId, cnt))

    def _afterNotifyGuildActivity(self, activityId, cnt):
        if not self.inWorld or not self.guild:
            return
        cnt -= 1
        if cnt <= 0:
            return
        activity = self.guild._getActivity(activityId)
        if activity.getState() != gametypes.GUILD_ACTIVITY_GOING:
            return
        data = GATD.data.get(activityId)
        self.showSysNotification(data.get('notifyMsgId'), (data.get('name', ''),), 1, data.get('notifyInterval', 10), finishCallback=lambda activityId = activityId, cnt = cnt: self._afterNotifyGuildActivity(activityId, cnt))

    def clearDeclareWar(self):
        if self.declareWarGuild:
            if self.clanWarStatus:
                for en in BigWorld.entities.values():
                    if en.inWorld and (en.IsAvatar and en.guildNUID in self.declareWarGuild or getattr(en, 'guildNUID', 0) in self.declareWarGuild) and en.topLogo:
                        en.topLogo.updateRoleName(en.topLogo.name)

            self.declareWarGuild.clear()
            self.refreshTargetLocked()

    def showItemIconNearGuildBuildingMarker(self, entId, itemId):
        gameglobal.rds.ui.pressKeyF.isGuildBuildingMarker = True
        gameglobal.rds.ui.pressKeyF.guildBuildingMarkerId = entId
        gameglobal.rds.ui.pressKeyF.setType(const.F_GUILDBUILDINGMARKER)

    def hideItemIconNearGuildBuildingMarker(self, entId):
        if gameglobal.rds.ui.pressKeyF.guildBuildingMarkerId == entId:
            gameglobal.rds.ui.pressKeyF.guildBuildingMarkerId = None
        if gameglobal.rds.ui.pressKeyF.isGuildBuildingMarker == True:
            gameglobal.rds.ui.pressKeyF.isGuildBuildingMarker = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_GUILDBUILDINGMARKER)

    def createGuildBuilding(self, entId):
        marker = BigWorld.entities.get(entId)
        if marker:
            if marker.devState == gametypes.GUILD_DEV_STATE_FINISHED:
                gameglobal.rds.ui.guildBuildSelect.show(marker.markerId, npcId=entId)
            else:
                gameglobal.rds.ui.guildAssart.show(marker.markerId, npcId=entId)

    def onGuildSpaceBought(self, guildNUID, res, hiredResident):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.hasSpace = True
        self.guild.updateRes(res)
        self.guild.hiredResident.clear()
        for dto in hiredResident:
            resident = GuildResidentVal().fromDTO(dto)
            self.guild.hiredResident[resident.nuid] = resident

        gameglobal.rds.ui.guild.refreshBuildInfo()
        gameglobal.rds.tutorial.onHasGuildSpace()

    def onGuildGroupRenamed(self, guildNUID, groupId, name):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        group = self.guild.group.get(groupId)
        if not group:
            return
        group.name = name
        gameglobal.rds.ui.guild.updateGroupInfo()
        gameglobal.rds.ui.guildGroup.refreshGroupInfo()

    def onGuildAddGroup(self, guildNUID, groupId, name):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.group[groupId] = GuildGroupVal(groupId=groupId, name=name, tWhen=utils.getNow())
        gameglobal.rds.ui.guild.updateGroupInfo()
        gameglobal.rds.ui.guildGroup.refreshGroupInfo()

    def onGuildRemoveGroup(self, guildNUID, groupId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            self.guild.group.pop(groupId, None)
            for member in self.guild.member.itervalues():
                if member.groupId == groupId:
                    member.groupId = 0

            gameglobal.rds.ui.guild.updateGroupInfo()
            gameglobal.rds.ui.guildGroup.refreshGroupInfo()
            return

    def onGuildMemberGroupUpdated(self, guildNUID, gbId, groupId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        member = self.guild.member.get(gbId)
        if not member:
            return
        member.groupId = groupId
        self.guild.checkGroupLeaderConsistant(gbId)
        gameglobal.rds.ui.guild.updateMember(gbId)

    def onGuildGroupOpFailed(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildGroup.refreshGroupInfo()

    def onGuildStabilityUpdate(self, guildNUID, stability):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.stability = stability
        gameglobal.rds.ui.guild.refreshResourceInfo()
        gameglobal.rds.ui.guildStorage.refreshResourceInfo()
        gameglobal.rds.ui.topBar.setValueByName('guildStability')

    def onOpenGuildResident(self, guildNUID, npcEntId, residentTemplateId, bNeedTreat):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        npc = BigWorld.entities.get(npcEntId)
        if not npc:
            return
        gameglobal.rds.ui.guild.residentNpcId = npcEntId
        gameglobal.rds.ui.guild.residentTemplateId = residentTemplateId
        gameglobal.rds.ui.guild.bNeedTreat = bNeedTreat
        if bNeedTreat:
            uichat = GRTD.data.get(residentTemplateId, {}).get('Uichat', ND.data.get(npc.npcId, {}).get('Uichat'))
        else:
            uichat = ND.data.get(npc.npcId, {}).get('Uichat')
        gameglobal.rds.ui.guildResident.hide()
        gameglobal.rds.ui.funcNpc.open(npcEntId, npc.npcId, uichat)

    def onQueryGuildFreeResident(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = GuildResidentVal().fromDTO(dto)
        gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_NEW, resident=resident)

    def onGuildAddRecommendedResident(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = GuildResidentVal().fromDTO(dto)
        self.guild.recommendedResident[resident.nuid] = resident
        gameglobal.rds.ui.guildResidentRec.refreshInfo()

    def onGuildHireResient(self, guildNUID, residentNUID, data, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            resident = self.guild.recommendedResident.pop(residentNUID, None)
            if not resident:
                return
            statusType, statusStype = data
            resident.statusType = statusType
            resident.statusStype = statusStype
            resident.tHire = utils.getNow()
            self.guild.hiredResident[resident.nuid] = resident
            self.guild.updateRes(res)
            gameglobal.rds.ui.guildResident.hideByNUID(residentNUID)
            gameglobal.rds.ui.guildResidentRec.refreshInfo()
            gameglobal.rds.ui.guildResidentHired.refreshInfo()
            return

    def onGuildRejectResient(self, guildNUID, residentNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            resident = self.guild.recommendedResident.pop(residentNUID, None)
            if not resident:
                return
            gameglobal.rds.ui.guildResident.hideByNUID(residentNUID)
            gameglobal.rds.ui.guildResidentRec.refreshInfo()
            return

    def _getGuildEntity(self, staticEntityId):
        entID = BigWorld.player().guildEntities.get(staticEntityId)
        ent = None
        if entID:
            ent = BigWorld.entities.get(entID)
        return ent

    def onLoadGuildStaticEntities(self, guildNUID, spaceNo, staticEntities, closedAreaIds):
        if self.spaceNo != spaceNo:
            return
        for staticEntityId in staticEntities:
            self._createGuildStaticEntity(staticEntityId, guildNUID)

        self.onRefreshGuildArea(guildNUID, spaceNo, closedAreaIds)

    def _createGuildStaticEntity(self, staticEntityId, guildNUID):
        data = GSED.data.get(staticEntityId)
        attrs = {'geId': staticEntityId,
         'guildNUID': guildNUID}
        try:
            entID = BigWorld.createEntity('ClientGuildEntity', self.spaceID, 0, data.get('position'), data.get('direction'), {'attrs': attrs})
            self.guildEntities[staticEntityId] = entID
        except:
            gamelog.debug('@CF:onLoadGuildStaticEntities, ERROR', self.spaceID, self.id, data.get('position'), data.get('direction'), {'attrs': attrs})

    def onUnloadGuildStaticEntities(self, guildNUID, spaceNo, staticEntities):
        if self.spaceNo != spaceNo:
            return
        else:
            for staticEntityId in staticEntities:
                entId = self.guildEntities.get(staticEntityId)
                ent = BigWorld.entities.get(entId)
                if ent:
                    ent.leaveWorld()
                    BigWorld.destroyEntity(entId)
                self.guildEntities.pop(entId, None)

            return

    def onGuildUpdatePendingMarkerIds(self, markerIds):
        for markerId in markerIds:
            self.pendingGuildMarkerIds.append(markerId)

    def onRefreshGuildArea(self, guildNUID, spaceNo, closedAreaIds):
        if self.spaceNo != spaceNo:
            return
        for areaId in closedAreaIds:
            adata = GARD.data.get(areaId)
            for fogId in adata.get('fog', ()):
                data = GSED.data.get(fogId)
                attrs = {'geId': fogId,
                 'guildNUID': guildNUID,
                 'scale': data.get('scale') or (1.0, 1.0, 1.0)}
                try:
                    entID = BigWorld.createEntity('ClientGuildFog', self.spaceID, 0, data.get('position'), data.get('direction'), {'attrs': attrs})
                    self.guildEntities[fogId] = entID
                except:
                    gamelog.debug('@CF:onRefreshGuildArea, ERROR', self.spaceID, self.id, data.get('position'), data.get('direction'), {'attrs': attrs})

    def onOpenGuildArea(self, guildNUID, spaceNo, areaId):
        if self.spaceNo != spaceNo:
            return
        else:
            data = GARD.data.get(areaId)
            for fogId in data.get('fog', ()):
                entId = self.guildEntities.get(fogId)
                if entId:
                    ent = BigWorld.entities.get(entId)
                    if ent:
                        ent.leaveWorld()
                        BigWorld.destroyEntity(entId)
                self.guildEntities.pop(fogId, None)

            return

    def onGuildUpdateAreaExt(self, guildNUID, areaId, ext):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        area = self.guild.area.get(areaId)
        if not area:
            area = GuildAreaVal(areaId=areaId)
            self.guild.area[areaId] = area
        area.ext = ext
        if ext == 0:
            area.state = gametypes.GUILD_AREA_STATE_CLOSE
        if area.isExtFinished():
            self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guildExploreState.refreshInfo()
        gameglobal.rds.ui.guild.refreshExploreStateInfo()

    def showGuildEntityItemIcon(self, entId, tp = 0):
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        data = GSED.data.get(ent.geId)
        tp = tp or data.get('type')
        if tp == gametypes.GUILD_STATIC_ENTITY_CHAIR:
            if self.isGuildSitInChair():
                return
            gameglobal.rds.ui.pressKeyF.isGuildEntity = True
            gameglobal.rds.ui.pressKeyF.guildEntityId = entId
            gameglobal.rds.ui.pressKeyF.setType(const.F_GUILDSIT)

    def showGuildTreatItemIcon(self, entId):
        if not self.isGuildSitInChair():
            return
        gameglobal.rds.ui.pressKeyF.isGuildEntity = True
        gameglobal.rds.ui.pressKeyF.guildEntityId = entId
        gameglobal.rds.ui.pressKeyF.setType(const.F_GUILDTREAT)

    def hideGuildEntityItemIcon(self, entId, tp = 0):
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        else:
            if gameglobal.rds.ui.pressKeyF.guildEntityId == entId:
                gameglobal.rds.ui.pressKeyF.guildEntityId = None
                if gameglobal.rds.ui.pressKeyF.isGuildEntity == True:
                    data = GSED.data.get(ent.geId)
                    tp = tp or data.get('type')
                    gameglobal.rds.ui.pressKeyF.isGuildEntity = False
                    if tp == gametypes.GUILD_STATIC_ENTITY_CHAIR:
                        gameglobal.rds.ui.pressKeyF.removeType(const.F_GUILDSIT)
                        gameglobal.rds.ui.pressKeyF.removeType(const.F_GUILDTREAT)
            return

    def seekToGuildChair(self, entId):
        if not entId:
            return
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        gameglobal.rds.ui.pressKeyF.isGuildEntity = False
        gameglobal.rds.ui.pressKeyF.removeType(const.F_GUILDSIT)
        destPos = Math.Vector3(*self.guild._getResidentSitPosition(ent.geId, 1))
        self.ap.seekPath(destPos, callback=lambda success, entId = entId: self._onSeekToGuildChair(success, entId))

    def _onSeekToGuildChair(self, success, entId):
        self.ap.forwardMagnitude = 0
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        if success == -1:
            return
        self.ap.setYaw(ent.yaw)
        self.reqGuildSitInChair(entId)

    def reqGuildSitInChair(self, entId):
        if not entId:
            return
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        self.cell.guildSitInChair(ent.geId, entId)

    def onGuildSitInChair(self, chairId, chairEntId, bNeedTreat):
        ent = BigWorld.entities.get(chairEntId)
        if not ent:
            return
        if ent.geId != chairId:
            return
        self.doGuildSitInChair(chairId)
        if bNeedTreat:
            self.showGuildTreatItemIcon(chairEntId)

    def doGuildSitInChair(self, chairId):
        chairEnt = self._getGuildEntity(chairId)
        if not chairEnt or not chairEnt.ownerModels:
            return
        else:
            self.chairEntId = chairEnt.id
            self.modelServer.sitInChair(chairEnt.ownerModels[0])
            self.fashion.playActionSequence(self.modelServer.bodyModel, const.GUILD_RESTAURANT_SIT_ACTIONS, None, keep=1)
            chairEnt.sitAvatarId = self.id
            chairEnt.refreshInteractEffects()
            return

    def isGuildSitInChair(self):
        return getattr(self, 'chairEntId', 0) != 0

    def guildLeaveChair(self):
        chairEntId = getattr(self, 'chairEntId', 0)
        if BigWorld.player() and self.id == BigWorld.player().id:
            ent = BigWorld.entities.get(chairEntId)
            if ent:
                self.hideGuildEntityItemIcon(chairEntId)
                chairId = ent.geId
                self.cell.guildLeaveChair(chairId)
        if chairEntId:
            self.chairEntId = 0
            ent = BigWorld.entities.get(chairEntId)
            if ent:
                self.modelServer.leaveChair(ent.ownerModels[0])
                ent.sitAvatarId = None
                ent.refreshInteractEffects()

    def doGuildLeaveChair(self):
        chairEntId = getattr(self, 'chairEntId', 0)
        if chairEntId:
            self.chairEntId = 0
            ent = BigWorld.entities.get(chairEntId)
            if ent:
                self.modelServer.leaveChair(ent.ownerModels[0])

    def onGuildLeaveChair(self, chairId):
        if gameglobal.rds.ui.serveFood.mediator:
            gameglobal.rds.ui.serveFood.hide()

    def reqGuildTreatResident(self, entId):
        if not entId:
            return
        ent = BigWorld.entities.get(entId)
        if not ent:
            return
        gameglobal.rds.ui.serveFood.show(entId)

    def onGuildFireResient(self, guildNUID, residentNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.stopWork(self.guild)
        self.guild.hiredResident.pop(residentNUID)
        gameglobal.rds.ui.guildResident.hideByNUID(residentNUID)
        gameglobal.rds.ui.guildDispatch.hideByNUID(residentNUID)
        gameglobal.rds.ui.guild.refreshAllResidentProxy()

    def onGuildRenameResident(self, guildNUID, residentNUID, name):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            resident = self.guild.hiredResident.get(residentNUID, None)
            if not resident:
                return
            resident.name = name
            gameglobal.rds.ui.guildResidentHired.refreshInfo()
            gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
            return

    def onGuildUpgradeResident(self, guildNUID, residentNUID, r):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            resident = self.guild.hiredResident.get(residentNUID, None)
            if not resident:
                return
            cpow, cagi, cint, cspr, pskills = r
            resident.cpow = cpow
            resident.cagi = cagi
            resident.cint = cint
            resident.cspr = cspr
            resident.lvUp()
            if pskills:
                for pskillId, lv in pskills:
                    if resident.pskills.has_key(pskillId):
                        resident.pskillLevelUp(pskillId, lv)
                    else:
                        resident.learnPSkill(pskillId, lv)

            gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
            gameglobal.rds.ui.guildDispatch.refreshInfo(residentNUID)
            gameglobal.rds.ui.guildResidentHired.refreshInfo()
            if pskills:
                for pskillId, lv in pskills:
                    self.showGameMsg(GMDD.data.GUILD_RESIDENT_UPGRADE_PSKILL, (gametypes.GUILD_RESIDENT_STATUS_NAME.get(resident.statusType),
                     resident.name,
                     GRPD.data.get((pskillId, lv), {}).get('name'),
                     lv))

            return

    def onGuildResidentPropUpdate(self, guildNUID, residentNUID, cpow, cagi, cint, cspr):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.cpow = cpow
        resident.cagi = cagi
        resident.cint = cint
        resident.cspr = cspr
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
        gameglobal.rds.ui.guildDispatch.refreshInfo(residentNUID)

    def onGuildResidentQpropUpdate(self, guildNUID, residentNUID, qpow, qagi, qint, qspr):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.qpow = qpow
        resident.qagi = qagi
        resident.qint = qint
        resident.qspr = qspr
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
        gameglobal.rds.ui.guildDispatch.refreshInfo(residentNUID)

    def onGuildResidentUpdateLv(self, guildNUID, residentNUID, lv):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.level = lv
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)

    def onGuildResidentUpdateExp(self, guildNUID, residentNUID, exp):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.exp = exp
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
        gameglobal.rds.ui.guildResidentHired.refreshInfo()

    def onGuildResidentUpdateStatus(self, guildNUID, residentNUID, stype):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.onInsightToStatus(stype)
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)

    def onGuildResidentUpdateTired(self, guildNUID, residentNUID, tired):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.tired = tired
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)

    def onGuildResidentUpdateTemplate(self, guildNUID, residentNUID, templateId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.templateId = templateId
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)

    def onGuildResidentUpdate(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = GuildResidentVal().fromDTO(dto)
        self.guild.hiredResident[resident.nuid] = resident
        gameglobal.rds.ui.guildResident.refreshInfo(resident.nuid)

    def onGuildBuildingProgressUpdated(self, guildNUID, buildingNUID, val):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            building = self.guild.building.get(buildingNUID, None)
            if not building:
                return
            building.addProgress(val)
            if building.checkFinishUpgrading():
                building.stopUpgrading(self.guild)
                self.onQuestInfoModifiedAtClient(const.QD_GUILD)
            return

    def onGuildDevProgressUpdated(self, guildNUID, markerId, progress):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        marker = self.guild.marker.get(markerId)
        marker.progress = progress
        if marker.isDevFinished():
            marker.stopDev(self.guild, False)
            for childMarkerId in GBMD.data.get(markerId).get('children', ()):
                cmarker = self.guild.marker.get(childMarkerId)
                cmarker.tDev = marker.tDev
                cmarker.progress = marker.progress

            self.onQuestInfoModifiedAtClient(const.QD_GUILD)
            gameglobal.rds.ui.guildAssart.assartFinish(marker.markerId)
            gameglobal.rds.ui.guild.refreshSingleBuildInfo(markerId)
            gameglobal.rds.ui.guild.refreshAllResidentProxy()
        else:
            gameglobal.rds.ui.guildAssart.setInitData()
            gameglobal.rds.ui.guild.refreshCurBuildInfo()

    def onGuildDevStart(self, guildNUID, markerId, tDev):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        marker = self.guild.marker.get(markerId)
        marker.tDev = tDev
        marker.state = gametypes.GUILD_DEV_STATE_START
        self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guild.refreshSingleBuildInfo(markerId)
        gameglobal.rds.ui.guildAssart.setInitData()

    def onGuildDevCancel(self, guildNUID, markerId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        marker = self.guild.marker.get(markerId)
        marker.stopDev(self.guild)
        for childMarkerId in GBMD.data.get(markerId).get('children', ()):
            cmarker = self.guild.marker.get(childMarkerId)
            cmarker.tDev = marker.tDev
            cmarker.progress = marker.progress
            cmarker.state = marker.state

        self.onQuestInfoModifiedAtClient(const.QD_GUILD)
        gameglobal.rds.ui.guild.refreshSingleBuildInfo(markerId)
        gameglobal.rds.ui.guildAssart.setInitData()
        gameglobal.rds.ui.guild.refreshAllResidentProxy()

    def onGuildAssignJob(self, guildNUID, residentNUID, jobId, tJob):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        jdata = GJD.data.get(jobId)
        if jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
            marker = commGuild.whereJob(self.guild, jobId)
            if marker:
                r = marker.stopFuncWorker(self.guild, jobId)
                if r:
                    gameglobal.rds.ui.guildResident.hideByNUID(r.nuid)
                    gameglobal.rds.ui.guildDispatch.hideByNUID(r.nuid)
                    gameglobal.rds.ui.guild.refreshAllResidentProxy(r.nuid)
        resident = self.guild.hiredResident.get(residentNUID)
        if resident:
            resident.stopWork(self.guild)
            resident.onAssignJob(self.guild, jobId, tJob)
            gameglobal.rds.ui.guildResident.hideByNUID(residentNUID)
            gameglobal.rds.ui.guildDispatch.hideByNUID(residentNUID)
            gameglobal.rds.ui.guild.refreshAllResidentProxy(residentNUID)

    def onGuildStopWork(self, guildNUID, residentNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if not resident:
            return
        resident.stopWork(self.guild)
        gameglobal.rds.ui.guildResident.hideByNUID(residentNUID)
        gameglobal.rds.ui.guild.refreshAllResidentProxy(residentNUID)

    def onGuildCheckPoint(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        stability, res = data
        self.guild.stability = stability
        self.guild.doCheckPoint()
        self.guild.updateRes(res)

    def onGuildUpgradeScale(self, guildNUID, scale, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.scale = scale
        self.onGuildUpdateOtherRes(guildNUID, otherRes)
        gameglobal.rds.ui.guild.refreshProsperityInfo()

    def onMockGuildBuildings(self, data):
        if self.spaceNo != const.GUILD_STATIC_SPACE_NO:
            return
        markerBaseId = 1000000
        buildingBaseId = 2000000
        tp = data[0]
        if tp == 0:
            self.buildingProxy.clearAll()
            step = data[1]
            for markerId, position, direction in data[2]:
                mdata = GBMD.data.get(markerId)
                stepModels = mdata.get('stepModels')
                if stepModels and step >= len(stepModels):
                    continue
                properties = {'cls': 'GuildBuildingMarker',
                 'pos': position,
                 'dir': direction,
                 'extra': {'markerId': markerId,
                           'step': step,
                           'hasBuilding': False}}
                self.buildingProxy.sightEnter(self.spaceID, markerBaseId + markerId, properties)

        else:
            level = data[1]
            for markerId, buildingId, position, direction in data[2]:
                properties = {'cls': 'GuildBuilding',
                 'pos': position,
                 'dir': direction,
                 'extra': {'buildingNUID': markerId,
                           'buildingId': buildingId,
                           'buildingLevel': min(level, GBD.data.get(buildingId).get('maxLevel', 1)),
                           'tStart': 0,
                           'markerId': markerId}}
                self.buildingProxy.sightEnter(self.spaceID, buildingBaseId + markerId, properties)

    def onExitGuildScene(self):
        self.clearGuildEntities()

    def clearGuildEntities(self):
        for entId in self.guildEntities.itervalues():
            if entId:
                ent = BigWorld.entities.get(entId)
                if ent:
                    try:
                        ent.leaveWorld()
                        BigWorld.destroyEntity(entId)
                    except:
                        pass

        self.guildEntities.clear()

    def onGuildAddFactoryQueue(self, guildNUID, taskDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        task = GuildFactoryTaskVal().fromDTO(taskDTO)
        ftype = GFPD.data.get(task.productId).get('type')
        factory = self.guild._getFactory(ftype)
        factory.queue.append(task)
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)

    def onGuildAddFactoryTask(self, guildNUID, taskDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        task = GuildFactoryTaskVal().fromDTO(taskDTO)
        pdata = GFPD.data.get(task.productId)
        if not pdata:
            return
        ftype = pdata.get('type')
        factory = self.guild._getFactory(ftype)
        factory.cancelQueue(self.guild, task.nuid)
        factory.task[task.nuid] = task
        task.onStart(self.guild, factory)
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)
        gameglobal.rds.ui.guildProduce.refreshInfo()

    def onGuildTaskFinished(self, guildNUID, ftype, taskNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            factory = self.guild._getFactory(ftype)
            task = factory.task.pop(taskNUID, None)
            if task:
                task.onFinish(self.guild, factory)
            gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)
            gameglobal.rds.ui.guildProduce.refreshInfo()
            return

    def onGuildFactoryDecProduct(self, guildNUID, productId, amount):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        ftype = GFPD.data.get(productId).get('type')
        factory = self.guild._getFactory(ftype)
        factory.decProduct(productId, amount)
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)

    def onGuildFactoryUpdateProduct(self, guildNUID, productId, amount):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        ftype = GFPD.data.get(productId).get('type')
        factory = self.guild._getFactory(ftype)
        factory.product[productId] = amount
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)

    def onGuildCancelFactoryQueue(self, guildNUID, ftype, taskNUID, res, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        factory = self.guild._getFactory(ftype)
        factory.cancelQueue(self.guild, taskNUID)
        self.onGuildUpdateAllRes(guildNUID, res, otherRes)
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)

    def onGuildCancelFactoryTask(self, guildNUID, ftype, taskNUID, res, otherRes):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        factory = self.guild._getFactory(ftype)
        factory.cancelTask(self.guild, taskNUID)
        self.onGuildUpdateAllRes(guildNUID, res, otherRes)
        gameglobal.rds.ui.guildFactory.refreshWorkInfo(ftype)
        gameglobal.rds.ui.guildProduce.refreshInfo()

    def onGuildDaily(self, guildNUID, r, vitality, lastActiveNum):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.vitality = vitality
        self.guild.lastActiveNum = lastActiveNum
        for member in self.guild.member.itervalues():
            member.donateWeekly = 0

        for residentNUID, d in r.iteritems():
            stype, learnedPSkillIds = d
            resident = self.guild.hiredResident[residentNUID]
            if learnedPSkillIds:
                for pskillId in learnedPSkillIds:
                    resident.pskills[pskillId] = GuildResidentPSkillVal(skillId=pskillId, level=1)

            resident.onInsightToStatus(stype)

        self.guild.getShop(gametypes.GUILD_SHOP_TYPE_TREASURE).buyRecord.clear()
        for activity in self.guild.activity.itervalues():
            activity.cnt = 0

        self.guild.signInNum = 0
        self.guild.redPacket.signInRedPacket.clear()
        self.guild.redPacket.clear()
        gameglobal.rds.ui.guild.refreshGuildInfo()

    def onGuildResidentPSkillUpdate(self, guildNUID, residentNUID, pskillId, lv):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        resident = self.guild.hiredResident.get(residentNUID)
        if resident.pskills.has_key(pskillId):
            resident.pskills[pskillId].level = lv
        else:
            resident.pskills[pskillId] = GuildResidentPSkillVal(skillId=pskillId, level=lv)

    def onGuildResearchTechnologyStart(self, guildNUID, techId, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.technology[techId] = GuildTechnologyVal(techId=techId, state=gametypes.GUILD_TECHNOLOGY_STATE_START)
        self.guild.updateRes(res)
        self.showGameMsg(GMDD.data.GUILD_RESEARCH_TECHNOLOGY_START, (GTD.data.get(techId).get('name'),))
        gameglobal.rds.ui.guildTechResearch.refreshInfo(techId)
        gameglobal.rds.ui.guild.refreshSingleTechnologyInfo(techId, False)

    def onGuildResearchTechnologyCancel(self, guildNUID, techId, res):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            techVal = self.guild.technology.get(techId, None)
            if techVal:
                techVal.cancelResearching()
            self.guild.updateRes(res)
            self.showGameMsg(GMDD.data.GUILD_RESEARCH_TECHNOLOGY_CANCEL, (GTD.data.get(techId).get('name'),))
            self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_TECH, techId)
            gameglobal.rds.ui.guildTechResearch.refreshInfo(techId)
            gameglobal.rds.ui.guild.refreshSingleTechnologyInfo(techId, False)
            return

    def onGuildResearchTechnologyFinish(self, guildNUID, techId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        technology = self.guild.technology.get(techId)
        technology.state = gametypes.GUILD_TECHNOLOGY_STATE_FINISH
        technology.progress = GTD.data.get(techId).get('progress')
        technology.applyAbility(self.guild)
        self.guild._popCancelRes(gametypes.GUILD_CANCEL_TYPE_TECH, techId)
        self.guild.maxMember = self.guild._getMaxMember()
        gameglobal.rds.ui.guildTechResearch.hideByTechId(techId)
        gameglobal.rds.ui.guild.refreshSingleTechnologyInfo(techId, True)

    def onGuildTechnologyUpdateProgress(self, guildNUID, techId, progress):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        technology = self.guild.technology.get(techId)
        technology.addProgress(progress - technology.progress)

    def onUploadGuildIconCheck(self, resType, guildIcon):
        guildIconUpLoadInterval = GCD.data.get('guildIconUpLoadInterval', 0)
        if resType == gametypes.GUILD_ICON_UPDATE_APPROVE:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPGUILD_2390 % utils.formatDuration(guildIconUpLoadInterval), lambda guildIcon = guildIcon: gameglobal.rds.ui.zhanQi._realUpload(guildIcon), noCallback=lambda : gameglobal.rds.ui.zhanQi._cancelUpload())
        elif resType == gametypes.GUILD_ICON_UPDATE_AUTH_FAIL:
            self.showGameMsg(GMDD.data.GUILD_ICON_UPDATE_AUTH_FAIL, ())
        elif resType == gametypes.GUILD_ICON_UPDATE_CD_FAIL:
            now = utils.getNow()
            if now - self.updateGuildIconTime < guildIconUpLoadInterval:
                delta = guildIconUpLoadInterval - (now - self.updateGuildIconTime)
                self.showGameMsg(GMDD.data.USE_DEFINE_FILE_TIME_LIMIT, (utils.formatDuration(delta),))

    def onGuildContainerKeep(self, guildNUID, buildingId, page, stamp):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if buildingId == gametypes.GUILD_BUILDING_STORAGE_ID:
            self.guild.storage.stamp[page] = stamp
            gameglobal.rds.ui.guildStorage.setGuildStorageItem(page)

    def onGuildContainerUpdate(self, guildNUID, buildingId, page, stamp, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if buildingId == gametypes.GUILD_BUILDING_STORAGE_ID:
            storage = self.guild.storage
            storage.stamp[page] = stamp
            data = cPickle.loads(zlib.decompress(data))
            for ps in range(storage.getPosCount(page)):
                storage.setQuickVal(const.CONT_EMPTY_VAL, page, ps)

            for ps, it in data:
                storage.setQuickVal(it, page, ps)

            gameglobal.rds.ui.guildStorage.setGuildStorageItem(page)

    def onGuildTutorialStepUpdate(self, guildNUID, stepId, progress):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        step = self.guild.tutorialStep.get(stepId)
        if step:
            step.progress = progress
            gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)

    def onGuildTutorialStepFinish(self, guildNUID, stepId, nextStepIds):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            self.guild.tutorialStep.pop(stepId, None)
            for nextStepId in nextStepIds:
                self.guild.tutorialStep[nextStepId] = GuildTutorialStepVal(stepId=nextStepId)

            gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
            return

    def onAddGuildTutorialStep(self, guildNUID, stepId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.tutorialStep[stepId] = GuildTutorialStepVal(stepId=stepId)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)

    def onResetGuildTutorialStep(self, guildNUID, stepId):
        self.guild.tutorialStep.clear()
        self.onAddGuildTutorialStep(guildNUID, stepId)

    def sendGuildTutorialStep(self, steps):
        if not self.guild:
            self.guildTutorialStep = {}
            guildTutorialStep = self.guildTutorialStep
        else:
            guildTutorialStep = self.guild.tutorialStep
        for dto in steps:
            step = GuildTutorialStepVal().fromDTO(dto)
            guildTutorialStep[step.stepId] = step

        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)

    def onGuildRename(self, guildNUID, name):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.name = name
        if gameglobal.rds.ui.guildRename.mediator:
            gameglobal.rds.ui.guildRename.hide()

    def onGuildQueryPkEnemy(self, guildNUID, guildEnemy, clanEnemy, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.pkEnemyVer = ver
        self.guild.guildEnemy = dict(guildEnemy)
        self.guild.clanEnemy = dict(clanEnemy)
        gameglobal.rds.ui.guild.refreshEnemyInfo()

    def onGuildUpdatePkEnemySuccess(self, guildNUID, guildEnemy, clanEnemy, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.pkEnemyVer = ver
        self.guild.guildEnemy = dict(guildEnemy)
        self.guild.clanEnemy = dict(clanEnemy)
        gameglobal.rds.ui.guild.refreshEnemyInfo()

    def onGuildUpdatePkEnemyFailed(self, data):
        if not self.guild or not self.guildNUID:
            return
        gameglobal.rds.ui.guild.refreshEnemyInfo()

    def onGuildUpdatePkEnemy(self, guildNUID, enemyGuildNUIDs, enemyClanNUIDs):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        enemyGuildNUIDs = set(enemyGuildNUIDs)
        enemyClanNUIDs = set(enemyClanNUIDs)
        diffGuildNUIDs = enemyGuildNUIDs.symmetric_difference(self.guild.enemyGuildNUIDs)
        diffClanNUIDs = enemyClanNUIDs.symmetric_difference(self.guild.enemyClanNUIDs)
        self.guild.enemyGuildNUIDs = enemyGuildNUIDs
        self.guild.enemyClanNUIDs = enemyClanNUIDs
        if diffGuildNUIDs or diffClanNUIDs:
            for en in BigWorld.entities.values():
                if en.inWorld and en.IsAvatar and en.topLogo:
                    gnuid = en.guildNUID
                    cnuid = en.clanNUID
                    if gnuid and gnuid in diffGuildNUIDs or cnuid and cnuid in diffClanNUIDs:
                        en.topLogo.updateRoleName(en.topLogo.name)

    def onApplyGuildChallengeSucc(self, challengeTimestamp, enemyName):
        gamelog.debug('@hjx challenge#onApplyGuildChallengeSucc:', challengeTimestamp)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['challengeTimestamp'] = challengeTimestamp
        guild.challengeInfo['enemyName'] = enemyName
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)

    def onApplyByGuildChallenge(self, srcGuildName, srcGuildNUID, srcGuildLv, srcChallengeTimestamp):
        gamelog.debug('@hjx challenge#onApplyByGuildChallenge:', srcGuildName, srcChallengeTimestamp)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['enemyName'] = srcGuildName
        guild.challengeInfo['srcChallengeTimestamp'] = srcChallengeTimestamp
        guild.challengeInfo['enemyGuildNUID'] = srcGuildNUID
        guild.challengeInfo['enemyGuildLv'] = srcGuildLv
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)
        gameglobal.rds.ui.guild.checkChallengePushMsg()

    def setGuildChallengeTimestamp(self, challengeTimestamp):
        gamelog.debug('@hjx challenge#setGuildChallengeTimestamp:', challengeTimestamp)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['challengeTimestamp'] = challengeTimestamp
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)

    def onRejectGuildChallenge(self, challengeTimestamp):
        gamelog.debug('@hjx challenge#onRejectGuildChallenge:', challengeTimestamp)
        gameglobal.rds.ui.guild.checkChallengePushMsg()

    def onGuildChallengeOccupy(self, tOccupy, fbNo):
        gamelog.debug('@hjx challenge#onGuildChallengeOccupy:', tOccupy, fbNo)
        if self != BigWorld.player():
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        guild.challengeInfo['tOccupy'] = tOccupy
        guild.challengeInfo['fbNo'] = fbNo
        guild.challengeInfo['memberNum'] = 0
        guild.challengeInfo['enemyMemberNum'] = 0
        gameglobal.rds.ui.guild.refreshChallengeInfo(False)
        gameglobal.rds.ui.guild.checkChallengePushMsg()

    def onQueryGuildStats(self, guildNUID, intervalType, ver, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        data = cPickle.loads(zlib.decompress(data))
        self.guild.stats[intervalType] = {}
        for gbId, contrib, bindCash, action in data:
            self.guild.stats[intervalType][gbId] = GuildMemberActionStatsVal(contrib=contrib, bindCash=bindCash, action=action)

        self.guild.statsVer[intervalType] = ver
        gameglobal.rds.ui.guild.refreshStatisticsInfo(intervalType)

    def onQueryGuildStatsKeep(self, guildNUID, intervalType, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guild.refreshStatisticsInfo(intervalType)

    def onGuildDonateReserveOK(self):
        gameglobal.rds.ui.guildStorage.refreshResourceInfo()
        if gameglobal.rds.ui.guildDonateReserve.mediator:
            gameglobal.rds.ui.guildDonateReserve.hide()

    def onGuildPayments(self, guildNUID, payments, amountTotal = 0, expireType = 0):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        mtype = 0
        for dto in payments:
            pval = GuildPayVal().fromDTO(dto)
            self.guild.memberMe.payments[pval.nuid] = pval
            mtype = pval.mtype

        self._notifyGuildPayment()
        if amountTotal and mtype:
            if mtype == gametypes.GUILD_PAY_TYPE_CASH:
                self.showGameMsg(GMDD.data.GUILD_PAY_MEMBERS_CASH, (self.guild.leaderRole, amountTotal, utils.formatDuration(gametypes.GUILD_PAY_EXPIRE[expireType])))
            elif mtype == gametypes.GUILD_PAY_TYPE_COIN:
                self.showGameMsg(GMDD.data.GUILD_PAY_MEMBERS_COIN, (self.guild.leaderRole, amountTotal, utils.formatDuration(gametypes.GUILD_PAY_EXPIRE[expireType])))
            elif mtype == gametypes.GUILD_PAY_TYPE_BIND_CASH:
                self.showGameMsg(GMDD.data.GUILD_PAY_MEMBERS_BIND_CASH, (self.guild.leaderRole, amountTotal, utils.formatDuration(gametypes.GUILD_PAY_EXPIRE[expireType])))

    def _notifyGuildPayment(self):
        payments = self.guild.memberMe.payments
        gameglobal.rds.ui.guildSalaryReceive.updateView()
        if not payments:
            return
        payments = self.guild.memberMe.payments.values()
        payments.sort(key=lambda x: x.tWhen)
        payment = payments.pop(0)
        now = utils.getNow()
        totalTime = payment.tExpire - now
        if totalTime > 0:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_SALARY_RECEIVE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_SALARY_RECEIVE, {'click': self.clickSalaryReceivePush})

    def onGuildGetPaymentFailed(self, guildNUID, nuid):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            self.guild.memberMe.payments.pop(nuid, None)
            self._notifyGuildPayment()
            return

    def onGuildGetPayment(self, guildNUID, nuid):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            self.guild.memberMe.payments.pop(nuid, None)
            self._notifyGuildPayment()
            return

    def onQueryGuildPayrollSettings(self, guildNUID, mtype, settings, groupSettings, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        payroll = self.guild.payroll.get(mtype)
        payroll.ver = ver
        payroll.settings = settings
        payroll.groupSettings = groupSettings
        gameglobal.rds.ui.guildSalaryAssign.refreshRate(mtype, settings, ver)

    def onQueryGuildPayrollSettingKeep(self, guildNUID, mtype):
        if not self.guild or guildNUID != self.guild.nuid:
            return

    def clickSalaryReceivePush(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_SALARY_RECEIVE)

    def onGuildAddPayGroup(self, guildNUID, mtype, serialNUID, tWhen, tExpire):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        payroll = self.guild.payroll.get(mtype)
        if not payroll.group.get(serialNUID):
            if len(payroll.group) >= const.GUILD_MAX_PAY_GROUP_NUM:
                dg = payroll.getEarliestGroup()
                payroll.group.pop(dg.serialNUID)
        group = GuildPayGroupVal(serialNUID=serialNUID, tWhen=tWhen, tExpire=tExpire)
        payroll.group[serialNUID] = group

    def onQueryGuildPayrollGroups(self, guildNUID, mtype, gdata, groupVer):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        payroll = self.guild.payroll.get(mtype)
        newSerialNUIDs = set()
        for dto in gdata:
            group = GuildPayGroupVal().fromDTO(dto)
            if not payroll.group.has_key(group.serialNUID):
                payroll.group[group.serialNUID] = group
            newSerialNUIDs.add(group.serialNUID)

        for serialNUID in payroll.group.keys():
            if serialNUID not in newSerialNUIDs:
                payroll.group.pop(serialNUID)

        payroll.groupVer = groupVer

    def onQueryGuildPayrollGroupsKeep(self, guildNUID, mtype):
        if not self.guild or guildNUID != self.guild.nuid:
            return

    def queryGuildPayroll(self, mtype, serialNUID):
        if not self.guild:
            return
        else:
            payroll = self.guild.payroll.get(mtype)
            group = payroll.group.get(serialNUID)
            if not group:
                return
            if group.payments != None:
                return
            group.payments = []
            self.cell.queryGuildPayroll(mtype, serialNUID)
            return

    def onQueryGuildPayroll(self, data):
        guildNUID, mtype, bDetail, serialNUID, pdata = cPickle.loads(zlib.decompress(data))
        if not self.guild or guildNUID != self.guild.nuid:
            return
        else:
            payroll = self.guild.payroll.get(mtype)
            group = payroll.group.get(serialNUID)
            if group.payments == None or group.payments:
                group.payments = []
            if bDetail:
                for gbId, amount, salaryType, tWhen, tPaid in pdata:
                    group.payments.append(GuildPayVal(gbId=gbId, amount=amount, tWhen=tWhen, tPaid=tPaid, salaryType=salaryType))

            else:
                for gbId, amount, salaryType, tWhen in pdata:
                    group.payments.append(GuildPayVal(gbId=gbId, amount=amount, tWhen=tWhen, salaryType=salaryType))

            gameglobal.rds.ui.guildSalaryHistory.updateSalaryDetailHistory()
            return

    def onQueryGuildMemberPayments(self, data):
        guildNUID, gbId, mdata = data
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRewardSalaryHistory.updateData(data)

    def onGuildMemberGetPayment(self, guildNUID, gbId, mtype, serialNUID, tPaid):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        payroll = self.guild.payroll.get(mtype)
        group = payroll.group.get(serialNUID)
        if group and group.payments:
            for pval in group.payments:
                if pval.gbId == gbId:
                    pval.tPaid = tPaid
                    break

    def onGuildWSPracticeStart(self, dto):
        wsp = GuildWSPracticeVal().fromDTO(dto)
        self.guildWSPractice[wsp.idx] = wsp
        gameglobal.rds.ui.guildWuShuang.refreshXinDeInfo()

    def onGuildWSPracticeFinished(self, idx):
        if idx >= len(self.guildWSPractice):
            return
        wsp = self.guildWSPractice[idx]
        if not wsp:
            return
        wsp.stop(self)
        gameglobal.rds.ui.guildWuShuang.refreshXinDeInfo()

    def onGuildWSPracticeUpdated(self, dto):
        wsp = GuildWSPracticeVal().fromDTO(dto)
        if wsp.idx >= len(self.guildWSPractice):
            return
        self.guildWSPractice[wsp.idx] = wsp
        gameglobal.rds.ui.guildWuShuang.refreshXinDeInfo()

    def onGuildWSPracticeInterval(self, idx):
        if idx >= len(self.guildWSPractice):
            return
        wsp = self.guildWSPractice[idx]
        if not wsp:
            return
        wsp.onInterval()
        gameglobal.rds.ui.guildWuShuang.refreshXinDeInfo()

    def sendClientGuildWSPractice(self, data):
        self.guildWSPractice = [None] * 4
        for dto in data:
            wsp = GuildWSPracticeVal().fromDTO(dto)
            self.guildWSPractice[wsp.idx] = wsp

        gameglobal.rds.ui.guildWuShuang.refreshXinDeInfo()

    def onGuildWSDaohengStart(self, dto):
        wsp = GuildWSPracticeVal().fromDTO(dto)
        self.guildWSDaoheng[wsp.idx] = wsp
        gameglobal.rds.ui.guildWuShuang.refreshDaoHengInfo()

    def onGuildWSDaohengFinished(self, idx):
        if idx >= len(self.guildWSDaoheng):
            return
        wsp = self.guildWSDaoheng[idx]
        if not wsp:
            return
        wsp.stop(self)
        gameglobal.rds.ui.guildWuShuang.refreshDaoHengInfo()

    def onGuildWSDaohengUpdated(self, dto):
        wsp = GuildWSPracticeVal().fromDTO(dto)
        if wsp.idx >= len(self.guildWSDaoheng):
            return
        self.guildWSDaoheng[wsp.idx] = wsp
        gameglobal.rds.ui.guildWuShuang.refreshDaoHengInfo()

    def onGuildWSDaohengInterval(self, idx):
        if idx >= len(self.guildWSDaoheng):
            return
        wsp = self.guildWSDaoheng[idx]
        if not wsp:
            return
        wsp.onInterval()
        gameglobal.rds.ui.guildWuShuang.refreshDaoHengInfo()

    def sendClientGuildWSDaoheng(self, data):
        self.guildWSDaoheng = [None] * 4
        for dto in data:
            wsp = GuildWSPracticeVal().fromDTO(dto)
            self.guildWSDaoheng[wsp.idx] = wsp

        gameglobal.rds.ui.guildWuShuang.refreshDaoHengInfo()

    def onGuildAddBusinessMan(self, guildNUID, gbId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if gbId not in self.guild.businessMan:
            self.guild.businessMan.append(gbId)
        gameglobal.rds.ui.guild.updateMember(gbId)

    def onGuildRemoveBusinessMan(self, guildNUID, gbIds):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        for gbId in gbIds:
            if gbId in self.guild.businessMan:
                self.guild.businessMan.remove(gbId)

        gameglobal.rds.ui.guild.updateMember(gbId)

    def onGuildOptionUpdate(self, guildNUID, options):
        if not self.guild:
            return
        self.guild.options.update(options)
        gameglobal.rds.ui.guildMember.refreshInfo()
        gameglobal.rds.ui.guildRename.checkRenamePushMsg()

    def onGuildGatherNotify(self, guildNUID, fromGbId, tEnd):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildCallMember.hideCallMemberPushMsg()
        gameglobal.rds.ui.guildCallMember.showCallMemberPushMsg(fromGbId)

    def onGuildGatherSuccess(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildCallMember.hideCallMemberPushMsg()

    def onGuildGatherRejected(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildCallMember.hideCallMemberPushMsg()

    def onGuildGatherFailed(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildCallMember.hideCallMemberPushMsg()

    def onQueryGuildNoviceBoostKeep(self):
        pass

    def onQueryGuildNoviceBoost(self, noviceBoosting, noviceBoosted, ver):
        if not self.guild:
            return
        self.guild.noviceBoosting = noviceBoosting
        self.guild.noviceBoosted = {}
        for dto in noviceBoosted:
            v = GuildNoviceBoostVal().fromDTO(dto)
            self.guild.noviceBoosted[v.gbId, v.actId] = v

        self.guild.noviceBoostVer = ver

    def onApplyNoviceBoostRewardOK(self, guildNUID, gbId, actId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        v = self.guild.noviceBoosted.get((gbId, actId))
        if v:
            v.state = gametypes.GUILD_NOVICE_BOOST_REWARD_DONE

    def displayGuildQuestBoard(self, count, page):
        self.cell.displayGuildQuestBoard(count, page)

    def onDisplayGuildQuestBoardFail(self):
        self.showGameMsg(GMDD.data.NO_AVALIABLE_GUILD_JOB, ())

    def onDisplayGuildQuestBoard(self, questLoopsInfo):
        gameglobal.rds.ui.guildJob.updateGuildJobBoard(questLoopsInfo)

    def acceptGuildQuestLoop(self, questLoopId):
        if QLD.data.has_key(questLoopId):
            self.cell.acceptGuildQuestLoop(questLoopId)

    def sendGuildRunMan(self, dto):
        self.runMan.clear()
        self.runMan.fromDTO(dto)

    def onGuildRunManStartNext(self, runManType, currNum):
        route = self.runMan.getRoute(runManType)
        route.state = gametypes.GUILD_RUN_MAN_STATE_OPEN
        route.currNum = currNum
        gameglobal.rds.ui.guildRunner.setType(runManType)
        gameglobal.rds.ui.guildRunner.setTime(utils.getNow())
        if currNum == 1:
            gameglobal.rds.ui.guildRunner.show()
            gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        else:
            gameglobal.rds.ui.guildRunner.refreshView()
        markerNpcId = GRMRD.data.get((runManType, currNum), {}).get('markerNpcId')
        for e in BigWorld.entities.values():
            if e.__class__.__name__ == 'Npc' and e.npcId == markerNpcId:
                e.refreshOpacityState()

    def onGuildRunManPassMarker(self, runManType, currNum, passNum):
        route = self.runMan.getRoute(runManType)
        mVal = route.getMarker(currNum)
        mVal.passed = True
        mVal.passNum = passNum

    def onGuildRunMainFail(self, runManType):
        route = self.runMan.getRoute(runManType)
        route._close()
        self.showGameMsg(GMDD.data.GUILD_RUN_MAN_TIMEOUT, ())
        gameglobal.rds.ui.guildRunner.setType(0)
        gameglobal.rds.ui.guildRunner.setTime(0)
        gameglobal.rds.ui.guildRunner.hide()
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()

    def onGuildRunManComplete(self, runManType):
        route = self.runMan.getRoute(runManType)
        route._close()
        self.showGameMsg(GMDD.data.GUILD_RUN_MAN_COMPLETE, ())
        gameglobal.rds.ui.guildRunner.setType(0)
        gameglobal.rds.ui.guildRunner.setTime(0)
        gameglobal.rds.ui.guildRunner.hide()
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)

    def _getGuildRunManRewardFactor(self, runManType):
        if not self.guild:
            return 1
        else:
            return 1 + self.guild.getAbility(GFNPDD.data.RUN_MAN_REWARD_ALL, runManType)

    def onGuildRobberOpen(self, guildNUID, beginTime, endTime, allRobbers, killedRobbers):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRobberActivityPush.activityOpen(beginTime, endTime, allRobbers, killedRobbers)

    def onGuildRobberUpdate(self, guildNUID, allRobbers, killedRobbers):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRobberActivityPush.updateInfo(allRobbers, killedRobbers)

    def onGuildRobberEnd(self, guildNUID, result, useTime):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRobberActivityPush.activityEnd(result, useTime)

    def onGuildRobberBigBoxStatus(self, guildNUID, boxStatus):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRobberActivityPush.updateBoxStatus(boxStatus)

    def onSyncGuildRobberNpcInfo(self, robberNpcInfo):
        self.guildRobberNpcInfo = robberNpcInfo
        gameglobal.rds.ui.littleMap.refreshGuildRobberNpcInfo()
        gameglobal.rds.ui.map.refreshGuildRobberNpcInfo()

    def onGetClanWarAttendance(self, attendInfo):
        gameglobal.rds.ui.ycwzRankList.setClanWarAttendInfo(attendInfo)

    def onSetGuildGroupLeader(self, guildNUID, groupId, gbId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        oldLeaderGbId = self.guild.getGroupLeaderGbId(groupId)
        oldGroupId = self.guild.getGroupIdOfLeader(gbId)
        if oldGroupId:
            if oldLeaderGbId and gbId:
                oldLeader = self.guild.member.get(oldLeaderGbId)
                if oldLeader:
                    self.guild.setGroupLeader(oldGroupId, oldLeaderGbId)
                    oldLeader.groupId = oldGroupId
                    if oldLeaderGbId == self.gbId:
                        self.showGameMsg(GMDD.data.GUILD_GROUP_SET_LEADER, self.guild.group[oldGroupId].name)
                    self.onGuildMemberGroupUpdated(guildNUID, oldLeaderGbId, oldGroupId)
            else:
                self.guild.setGroupLeader(oldGroupId, 0)
                if oldLeaderGbId:
                    self.onGuildMemberGroupUpdated(guildNUID, oldLeaderGbId, 0)
        self.guild.setGroupLeader(groupId, gbId)
        member = self.guild.member.get(gbId)
        if not member:
            return
        if groupId:
            member.groupId = groupId
        if gbId == self.gbId:
            self.showGameMsg(GMDD.data.GUILD_GROUP_SET_LEADER, self.guild.group[groupId].name)
        elif oldLeaderGbId == self.gbId:
            self.showGameMsg(GMDD.data.GUILD_GROUP_UNSET_LEADER, self.guild.group[groupId].name)
        self.guild.checkGroupLeaderConsistant(gbId)
        self.onGuildMemberGroupUpdated(guildNUID, gbId, groupId)
        if oldLeaderGbId:
            oldLeader = self.guild.member.get(oldLeaderGbId)
            if oldLeader:
                self.onGuildMemberGroupUpdated(guildNUID, oldLeaderGbId, oldLeader.groupId)

    def onGuildPuzzlePrepare(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        if self.guild.getPuzzleRoundNum() > 1:
            gameglobal.rds.ui.guildPuzzle.refreshInfo()
        else:
            gameglobal.rds.ui.guildPuzzle.show()

    def onGuildPuzzleStart(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        gameglobal.rds.ui.guildPuzzle.refreshInfo()
        gameglobal.rds.ui.guildBonfire.refreshInfo()

    def onGuildPuzzleResult(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        gameglobal.rds.ui.guildPuzzle.refreshInfo()

    def onGuildPuzzleReward(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        gameglobal.rds.ui.guildPuzzle.refreshInfo()

    def onGuildPuzzleEnd(self, guildNUID, activityDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        activityId = activityDTO[0]
        activity = self.guild._getActivity(activityId)
        activity.fromDTO(activityDTO)
        self.guild.puzzleJoined = False
        gameglobal.rds.ui.guildPuzzle.hide()

    def onJoinGuildPuzzle(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.puzzleJoined = True

    def onGuildPuzzleNormalReward(self, gbIdsData):
        if not self.guild:
            return
        winGbIds = cPickle.loads(zlib.decompress(gbIdsData))
        for gbId in winGbIds:
            mVal = self.guild.member.get(gbId)
            if mVal:
                self.showGameMsg(GMDD.data.GUILD_PUZZLE_WIN_MEMBER, (mVal.role,))

    def onLeaveGuildSpace(self):
        if hasattr(self, 'guildRobberNpcInfo'):
            self.guildRobberNpcInfo = []
            gameglobal.rds.ui.littleMap.refreshGuildRobberNpcInfo()
            gameglobal.rds.ui.map.refreshGuildRobberNpcInfo()

    def onGetPlayerPositionInGuildScene(self, spaceNo, position):
        targetSpaceNo = int(spaceNo)
        if formula.spaceInGuild(self.spaceNo):
            if not formula.spaceInGuild(targetSpaceNo):
                self.showGameMsg(GMDD.data.GUILD_PLAYER_NOT_IN_GUILD_SCENE, ())
            else:
                navigator.getNav().pathFinding((float(position[0]),
                 float(position[1]),
                 float(position[2]),
                 int(targetSpaceNo)), None, None, True, 0.5)
        else:
            p = BigWorld.player()
            haveSkill = p.guildMemberSkills.has_key(uiConst.GUILD_SKILL_DZG)
            canUse = logicInfo.isUseableGuildMemberSkill(gametypes.GUILD_PSKILL_DZG)
            canResetCd = self.canResetCD(gametypes.GUILD_PSKILL_DZG)
            if haveSkill and (canUse or canResetCd):
                if formula.spaceInGuild(targetSpaceNo):
                    gameglobal.rds.ui.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG, (str(position[0]), str(position[1]), str(position[2])))
                else:
                    msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_COMFIRM_TELEPORT_TO_GUILD_SPACE, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(gameglobal.rds.ui.skill.useGuildSkill, uiConst.GUILD_SKILL_DZG))
            elif formula.spaceInGuild(targetSpaceNo):
                navigator.getNav().pathFinding((float(position[0]),
                 float(position[1]),
                 float(position[2]),
                 int(targetSpaceNo)), None, None, True, 0.5)
            elif self.guild.spaceNo:
                defaultPosition = (165.550003, 64.726288, -90.260002)
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_COMFIRM_NAVIGATOR_TO_GUILD_SPACE, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self._comfirmNavigatorToGuildSpace, defaultPosition, self.guild.spaceNo))
            else:
                self.showGameMsg(GMDD.data.GUILD_PLAYER_NOT_IN_GUILD_SCENE, ())

    def _comfirmNavigatorToGuildSpace(self, position, spaceNo):
        navigator.getNav().pathFinding((float(position[0]),
         float(position[1]),
         float(position[2]),
         int(spaceNo)), None, None, True, 0.5)

    def onUpdateLeaderAutoResignTime(self, leaderAutoResignTime):
        self.guild.leaderAutoResignTime = leaderAutoResignTime
        gameglobal.rds.ui.guild.refreshResourceInfo()

    def onMassAstrologySucc(self, randomBuffList, selectIdx, selectBuffId, currBuffIds):
        gameglobal.rds.ui.guildIdentifyStar.beginIdentifyStar(randomBuffList, selectIdx, selectBuffId, currBuffIds)

    def onGetMassAstrologyInfo(self, currState, dailyCnt):
        gameglobal.rds.ui.guildIdentifyStar.setTimeInfo(currState, dailyCnt)

    def onGetMassAstrologyBuffTypes(self, dailyRefreshCnt, buffTypes):
        gameglobal.rds.ui.guildIdentifyStar.setBuffTypes(dailyRefreshCnt, buffTypes)

    def set_xiuweiLevel(self, old):
        gameglobal.rds.ui.roleInfo.refreshExpXiuWei()
        gameglobal.rds.ui.guildInherit.refreshInfoInCD()

    def setTodayGiveInheritCnt(self, todayGiveInheritCnt):
        self.todayGiveInheritCnt = todayGiveInheritCnt
        gameglobal.rds.ui.guildInherit.refreshInviteInfoInCD()

    def setTodayRecvInheritCnt(self, todayRecvInheritCnt):
        self.todayRecvInheritCnt = todayRecvInheritCnt
        gameglobal.rds.ui.guildInherit.refreshApplyInfoInCD()

    def guildInheritGiverInfoList(self, giverInfoList):
        gameglobal.rds.ui.guildInherit.updateApplyListInfo(giverInfoList)

    def guildInheritGiverInfo(self, giverInfo):
        pass

    def guildInheritReceiverInfoList(self, receiverInfoList):
        gameglobal.rds.ui.guildInherit.updateInviteListInfo(receiverInfoList)

    def guildInheritReceiverInfo(self, receiverInfo):
        pass

    def guildInheritNewRequest(self, gbId, role):
        gameglobal.rds.ui.guildInherit.updateGuildInheritPushMsg(uiConst.MESSAGE_TYPE_GUILD_INHERIT_APPLY, {'gbId': gbId,
         'roleName': role})

    def guildInheritNewInvite(self, gbId, role):
        gameglobal.rds.ui.guildInherit.updateGuildInheritPushMsg(uiConst.MESSAGE_TYPE_GUILD_INHERIT_INVITE, {'gbId': gbId,
         'roleName': role})

    def guildInheritApplyRequestSuccess(self, gbId):
        gameglobal.rds.ui.guildInherit.dissMissMsgBox(uiConst.MESSAGE_TYPE_GUILD_INHERIT_APPLY, gbId)

    def guildInheritApplyInviteSuccess(self, gbId):
        gameglobal.rds.ui.guildInherit.dissMissMsgBox(uiConst.MESSAGE_TYPE_GUILD_INHERIT_INVITE, gbId)

    def guildInheritInviteSuccessed(self, gbId):
        self.showGameMsg(GMDD.data.GUILD_INHERIT_INVITE_SUCCESSED, ())
        gameglobal.rds.ui.guildInherit.refreshCurrentViewList()

    def guildInheritRequestSuccessed(self, gbId):
        self.showGameMsg(GMDD.data.GUILD_INHERIT_REQUEST_SUCCESSED, ())
        gameglobal.rds.ui.guildInherit.refreshCurrentViewList()

    def onGuildActivityTopRankRewardMsg(self, guildNUID, rankType, rank, topThreeNames):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        if rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_CHICKEN:
            self.showGameMsg(GMDD.data.GUILD_CHICKEN_MEAL_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))
        elif rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_FISH:
            self.showGameMsg(GMDD.data.GUILD_FISH_ACTIVITY_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))
        elif rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_MONSTER:
            self.showGameMsg(GMDD.data.GUILD_MONSTER_CLAN_WAR_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))
        elif rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_YMF:
            self.showGameMsg(GMDD.data.GUILD_YMF_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))
        elif rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_SXY:
            self.showGameMsg(GMDD.data.GUILD_SXY_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))
        elif rankType == gametypes.GUILD_ACTIVITY_TOP_RANK_TYPE_NEWFLAG:
            self.showGameMsg(GMDD.data.GUILD_NEWFLAG_REWARD_MSG, (rank,
             topThreeNames[0],
             topThreeNames[1],
             topThreeNames[2]))

    def onGuildBonfireStart(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.bonfire.fromDTO(dto)
        self.checkGuildBonfire()
        if not self.inGuildSpace():
            gameglobal.rds.ui.guildBonfire.addPushMsg()

    def checkGuildBonfire(self):
        if not getattr(self, 'guild', None):
            gameglobal.rds.ui.guildBonfire.hide()
            return
        else:
            if self.guild.bonfire.isOpening() and self.inGuildSpace() and gameglobal.rds.configData.get('enableGuildBonfire', False):
                gameglobal.rds.ui.guildBonfire.show()
            else:
                gameglobal.rds.ui.guildBonfire.hide()
            return

    def onGuildBonfireFinish(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.bonfire.finish()
        gameglobal.rds.ui.guildBonfire.hide()
        gameglobal.rds.ui.guildBonfire.delPushMsg()
        gameglobal.rds.ui.guildMergeBonfire.hide(False)

    def onLightGuildTorchSucc(self, guildNUID, idx, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        name, = data
        self.guild.bonfire.torch[idx] = name
        gameglobal.rds.ui.guildBonfire.lightBonfireSucc(idx)
        gameglobal.rds.ui.guildBonfire.refreshInfo()

    def onGuildBonfireRefreshTreasureBox(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid or not self.inGuildSpace():
            return
        uiShowTime = GCD.data.get('bonfireEffs', {}).get('UIBoxShowTime', 3)
        soundId = GCD.data.get('bonfireEffs', {}).get('uiSound', 0)
        uiShowTime and gameglobal.rds.ui.guildBonfireBox.show(uiShowTime)
        soundId and gameglobal.rds.sound.playSound(soundId)

    def onGuildUpdateSignInNum(self, guildNUID, signInNum):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.signInNum = signInNum
        gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()

    def onGuildUpdatePrestige(self, guildNUID, prestige):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.prestige = prestige
        gameglobal.rds.ui.guild.refreshResourceInfo()

    def receiveGuildRedPacket(self, sn):
        if not self.guild:
            return
        self.cell.receiveGuildRedPacket(sn)

    def queryGuildRedPacket(self, sn):
        if not self.guild:
            return
        self.cell.queryGuildRedPacket(sn)

    def onGuildRedPacketStart(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.redPacket.fromDTO(dto)

    def onGuildRedPacketFinish(self, guildNUID, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.redPacket.fromDTO(dto)

    def onReceiveGuildRedPacketOK(self, guildNUID, sn, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        state, num = data
        v = self.guild.getRedPacket(sn)
        v.state = state
        v.received = num
        gameglobal.rds.ui.guildRedPacketRec.show(sn)
        gameglobal.rds.ui.guildRedPacketHistory.queryInfoInCD(True)

    def onReceiveGuildRedPacketFailed(self, guildNUID, sn, errMsgId, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.showGameMsg(errMsgId, ())
        if errMsgId == GMDD.data.GUILD_RED_PACKET_NOT_EXIST:
            gameglobal.rds.ui.guildRedPacketRec.closeBySn(sn)
        elif errMsgId == GMDD.data.GUILD_RED_PACKET_ALREADY_DONE:
            state, = data
            v = self.guild.getRedPacket(sn)
            v.state = state
            gameglobal.rds.ui.guildRedPacketRec.show(sn)
        elif errMsgId == GMDD.data.GUILD_RED_PACKET_ALREADY_RECV:
            state, num = data
            v = self.guild.getRedPacket(sn)
            v.state = state
            v.received = num
            gameglobal.rds.ui.guildRedPacketRec.show(sn)
        gameglobal.rds.ui.guildRedPacketHistory.queryInfoInCD(True)

    def onQueryAllGuildRedPacket(self, guildNUID, data, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        for dto in data:
            v = self.guild.getRedPacket(dto[0])
            v.fromSimpleDTO(dto)

        self.guild.redPacket.ver = ver
        gameglobal.rds.ui.guildRedPacketHistory.updateHistoryListInfo(data)

    def onQueryAllGuildRedPacketKeep(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return

    def onQueryGuildRedPacket(self, guildNUID, sn, dto):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        v = self.guild.getRedPacket(sn)
        v.fromDTO(dto)
        gameglobal.rds.ui.redPacket.onQueryGuildRedPacket(sn)

    def onGuildRedPacketSent(self, guildNUID, idx, richText):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.redPacket.markSent(idx)
        self.showGameMsg(GMDD.data.GUILD_COMMON_MSG, (richText,))
        gameglobal.rds.ui.guildRedPacket.refreshInfoInCD()
        gameglobal.rds.ui.guildRedPacketHistory.queryInfoInCD(False)
        gameglobal.rds.ui.guildRedPacketHistory.showGuildRedPacketPushMsg()

    def onQueryGuildAchieveRedPacketPool(self, guildNUID, dto, ver):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.redPacket.poolVer = ver
        self.guild.redPacket.fromPoolDTO(dto)
        gameglobal.rds.ui.guildRedPacketPool.refreshInfoInCD()

    def onQueryGuildAchieveRedPacketPoolKeep(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return

    def onSendGuildAchieveRedPacket(self, guildNUID, achieveId):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        self.guild.redPacket.removeFromPool(self.gbId, achieveId)
        gameglobal.rds.ui.guildRedPacketPool.refreshInfoInCD()
        gameglobal.rds.ui.guildRedPacketHistory.showGuildRedPacketPushMsg()

    def onSendGuildMergerRedPacket(self, guildNUID):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gameglobal.rds.ui.guildRedPacketPool.refreshInfoInCD()
        gameglobal.rds.ui.guildRedPacketHistory.showGuildRedPacketPushMsg()

    def getGuildMemberCnt(self):
        if not getattr(self, 'guild', None):
            return 0
        else:
            cnt = 0
            p = BigWorld.player()
            for member in self.guild.member.values():
                spaceNo = member.spaceNo if p.gbId != member.gbId else p.spaceNo
                if member.online and formula.spaceInGuild(spaceNo):
                    cnt += 1

            return cnt

    def notifyAvailGuildRedPacketNum(self, num):
        gameglobal.rds.ui.guildRedPacketHistory.showGuildRedPacketPushMsg()

    def updateFallenRedGuardChunkInfo(self, fallenRedGuardFlag, isSafe, deathTime):
        gamelog.info('jbx:updateFallenRedGuardChunkInfo', fallenRedGuardFlag, isSafe, deathTime)
        gameglobal.rds.ui.killFallenRedGuardRank.setFlagIsSafe(fallenRedGuardFlag, isSafe, deathTime)

    def updateFallenRedGuardDamageInfo(self, cfgId, entityId, firstAttackerInfo, killerInfo, guildsDamageList):
        joined = entityId and self.targetFallenRedGuards.get(cfgId) == entityId
        gamelog.info('jbx:updateFallenRedGuardDamageInfo', firstAttackerInfo, killerInfo, guildsDamageList)
        gameglobal.rds.ui.killFallenRedGuardRank.updateInfo(firstAttackerInfo, killerInfo, guildsDamageList, joined)

    def updateFallenRedGuardAlive(self, sdata):
        data = [ (cfgId, not alive) for cfgId, (_, alive, tKilled) in sdata.iteritems() if alive or tKilled ]
        data.sort(key=lambda x: x[1])
        self.fallenRedGuardFlagList = data
        gameglobal.rds.ui.littleMap.showFallenRedGuard()
        gameglobal.rds.ui.map.refreshFallenRedGuard()
        gameglobal.rds.ui.killFallenRedGuardRank.flagSafeRecord.clear()
        gameglobal.rds.ui.killFallenRedGuardRank.flagDeathTimeDic.clear()
        for cfgId, (_, alive, tKilled) in sdata.iteritems():
            gameglobal.rds.ui.killFallenRedGuardRank.flagSafeRecord[cfgId] = not (alive or tKilled)
            gameglobal.rds.ui.killFallenRedGuardRank.flagDeathTimeDic[cfgId] = tKilled

    def updateWingWorldSoulBossState(self, info):
        gamelog.debug('ypc@ updateWingWorldSoulBossState info = ', info)

    def updateWingWorldSoulBossStateEx(self, info):
        gamelog.debug('ypc@ updateWingWorldSoulBossStateEx info = ', info)
        gameglobal.rds.ui.littleMap.addWWBossIcon(info)
        if gameglobal.rds.ui.map.mapWidget:
            gameglobal.rds.ui.map.addWingWorldBossIcon(info)

    def updateWingWorldSoulBossSpecialDamage(self, cfgId, info):
        gamelog.debug('ypc@ updateWingWorldSoulBossSpecialDamage cfgId, info = ', cfgId, info)
        gameglobal.rds.ui.wingWorldAllSoulsRank.refreshBossStateInfo(info)

    def updateSoulBossGuildInfo(self, cfgId, info):
        gamelog.debug('ypc@ updateSoulBossGuild cfgId, info = ', cfgId, info)
        gameglobal.rds.ui.wingWorldAllSoulsRank.refreshGuildPanel(cfgId, info)

    def updateSoulBossMemberInfo(self, cfgId, info):
        gamelog.debug('ypc@ updateSoulBossMemberInfo cfgId, info = ', cfgId, info)
        gameglobal.rds.ui.wingWorldAllSoulsRank.refreshPersonPanel(cfgId, info)

    def onEnterSoulBossTrap(self, cfgId, monsterId):
        gamelog.debug('ypc@ onEnterSoulBossTrap, ', cfgId, monsterId)
        if not gameglobal.rds.ui.wingWorldAllSoulsRank.widget:
            gameglobal.rds.ui.wingWorldAllSoulsRank.show(cfgId)

    def onLeaveSoulBossTrap(self, cfgId, monsterId):
        gamelog.debug('ypc@ onLeaveSoulBossTrap, ', cfgId, monsterId)
        gameglobal.rds.ui.wingWorldAllSoulsRank.closeRank()

    def onSoulBossSpecialStateChange(self, specialTp, cfgId, monsterId):
        gamelog.debug('ypc@onSoulBossSpecialStateChange', specialTp, cfgId, monsterId)
        if const.SOUL_BOSS_ATK_TYPE_KILL == specialTp:
            p = BigWorld.player()
            p.base.getSoulBossStateInfoEx(p.getWingCityId())
        if gameglobal.rds.ui.wingWorldAllSoulsRank.widget:
            self.base.getSoulBossSpecialDamageInfo(cfgId)

    def onGetNpcMonumentArgs(self, npcId, args):
        gameglobal.rds.ui.wingWorldEpigraph.showEpigraph(npcId, args)

    def onGuildFubenMemberListUpdate(self, fbNo, gbIds):
        gamelog.debug('@yj .. onGuildFubenMemberListUpdate', fbNo, gbIds, fbNo in self.guildMembersFbData)
        if fbNo in self.guildMembersFbData:
            self.guildMembersFbData[fbNo]['memberlist'] = gbIds
        else:
            self.guildMembersFbData[fbNo] = {}
            self.guildMembersFbData[fbNo]['memberlist'] = gbIds
        gameglobal.rds.ui.guildMembersFbRank.updateFbEliteMembersList(gbIds)

    def onUpdateGuildFubenMemberList(self, fbNo, mType):
        pass

    def syncGuildFubenStage(self, fbNo, state):
        pass

    def syncGuildFubenRoundNum(self, fbNo, roundNum):
        gamelog.debug('@yj .. syncGuildFubenRoundNum', fbNo, roundNum)
        self.guildFubenRoundNum[fbNo] = roundNum

    def onRequireGuildFubenData(self, data):
        self.guildMembersFbData = data
        gameglobal.rds.ui.guildMembersFbRank.refreshInfo()

    def onGetGuildFubenRank(self, fbNo, rank):
        gameglobal.rds.ui.guildMembersFbResult.updateMyFbRank(rank)

    def onGetGuildFubenMaxMember(self, fbNo, data):
        pass

    def onInvitedEnterGuildFuben(self, fbNo):
        p = BigWorld.player()
        myFbNo = formula.getFubenNo(p.spaceNo)
        if formula.isGuildFuben(myFbNo):
            return
        gameglobal.rds.ui.guildMembersFbRank.hide()
        p = BigWorld.player()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.INVITED_ENTER_GUILD_FUBEN_DESC, yesCallback=Functor(p.cell.applyEnterGuildFuben, fbNo), yesBtnText=gameStrings.TEXT_IMPFRIEND_2211, noBtnText=gameStrings.TEXT_IMPFRIEND_963)

    def onGuildGetNewFlagScore(self, guildNUID, data):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        guildNewFlagScore, = data
        self.guild.guildNewFlagScore = guildNewFlagScore
        gamelog.debug('@zhangkuo onGuildGetNewFlagScore', guildNUID, guildNewFlagScore)

    def onReceiveGuildGrowthScoreReward(self, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe4\xba\xba\xe7\x89\xa9\xe4\xbf\xae\xe7\x82\xbc\xe8\xaf\x84\xe5\x88\x86\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        gamelog.info('@zmm onReceiveGuildGrowthScoreReward', ret)
        if ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_BY_MAIL_WHILE_INV_FULL, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.SHOP_BAG_LOCKED, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_ALREADY_RECEIVED:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_FAILED_BY_ALREADY_RECEIVED, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_VOLUMN_INVALID:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_FAILED_BY_VOLUMN_INVALID, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_FAILED, ())
        elif ret == gametypes.GUILD_GROWTH_SCORE_REWARD_SUC:
            self.showGameMsg(GMDD.data.GUILD_GROWTH_SCORE_REWARD_SUCCESS, ())
        if ret in (gametypes.GUILD_GROWTH_SCORE_REWARD_FAIL_BY_INV_FULL, gametypes.GUILD_GROWTH_SCORE_REWARD_SUC):
            gameglobal.rds.ui.xiuLianScoreReward.refreshInfo()
            gameglobal.rds.ui.guildGrowth.updateRewardBtnRedPot()

    def onUpdateGuildZhanxun(self, zhanHun):
        """
        :param zhanhun: \xe5\xbd\x93\xe5\x89\x8d\xe6\x88\x98\xe5\x8b\x8b\xe5\x80\xbc\xef\xbc\x8c\xe5\xae\x9e\xe6\x97\xb6\xe5\x90\x8c\xe6\xad\xa5
        :return:
        """
        self.zhanHun = zhanHun
        gameglobal.rds.ui.clanWarSkill.refreshZhanHunPoint()

    def confirmGuildGrowthRegress(self, typeStr, typeNum, volumnId, propertyId):
        """
        \xe5\x85\x83\xe7\xa5\x9e\xe6\x88\x96\xe5\x85\xac\xe4\xbc\x9a\xe8\xb4\xa1\xe7\x8c\xae\xe8\xb6\x85\xe8\xbf\x87\xe4\xb8\x8a\xe9\x99\x90\xef\xbc\x8c\xe5\xbc\xb9\xe5\x87\xba\xe5\xa4\x8d\xe9\x80\x89\xe6\xa1\x86\xef\xbc\x8c\xe8\xae\xa9\xe7\x94\xa8\xe6\x88\xb7\xe9\x80\x89\xe6\x8b\xa9\xe6\x98\xaf\xe5\x90\xa6\xe2\x80\x9c\xe7\xa1\xae\xe8\xae\xa4\xe2\x80\x9d\xe5\x9b\x9e\xe9\x80\x80
        :param typeStr: \xe2\x80\x9c\xe5\x85\x83\xe7\xa5\x9e\xe2\x80\x9d \xe6\x88\x96 \xe2\x80\x9c\xe5\x85\xac\xe4\xbc\x9a\xe8\xb4\xa1\xe7\x8c\xae\xe2\x80\x9d
        :param typeNum: \xe5\x85\xb7\xe4\xbd\x93\xe8\x8e\xb7\xe5\xbe\x97\xe7\x9a\x84\xe7\x82\xb9\xe6\x95\xb0
        :param volumnId: \xe5\x8d\xb7\xe8\xbd\xb4id
        :param propertyId: \xe5\x8d\xb7\xe8\xbd\xb4\xe4\xb8\x8b\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7id
        :return:
        """
        gamelog.info('@zq confirmGuildGrowthRegress', typeStr, typeNum, volumnId, propertyId)
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_GROWTH_REGRESS_FAILED_MSG, '%d-%s') % (typeNum, typeStr)
        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_GUILD_GROWTH_REGRESS):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.doConfirmGuildGrowthRegress, volumnId, propertyId), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_GUILD_GROWTH_REGRESS, noCallback=self._doCancelGuildGrowthRegress)
        else:
            self.cell.doConfirmGuildGrowthRegress(volumnId, propertyId)

    def _doCancelGuildGrowthRegress(self):
        gamelog.info('@zq _doCancelGuildGrowthRegress')

    def onGuildGrowthRegress(self, guildNUID, volumnId, propertyId, level, score, propName):
        """
        \xe4\xba\xba\xe7\x89\xa9\xe4\xbf\xae\xe7\x82\xbc\xe5\x9b\x9e\xe9\x80\x80\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe5\x88\xb7\xe6\x96\xb0\xe4\xba\xba\xe7\x89\xa9\xe4\xbf\xae\xe7\x82\xbc\xe5\xb1\x9e\xe6\x80\xa7\xe4\xbf\xa1\xe6\x81\xaf
        :param guildNUID: \xe5\x85\xac\xe4\xbc\x9anuid
        :param volumnId: \xe5\x8d\xb7\xe8\xbd\xb4id
        :param propertyId: \xe5\x8d\xb7\xe8\xbd\xb4\xe4\xb8\x8b\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7id
        :param level: \xe5\x8d\xb7\xe8\xbd\xb4\xe4\xb8\x8b\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7id\xe5\x9b\x9e\xe9\x80\x80\xe5\x90\x8e\xe7\x9a\x84\xe7\xad\x89\xe7\xba\xa7
        :param score: \xe4\xba\xba\xe7\x89\xa9\xe4\xbf\xae\xe7\x82\xbc\xe8\xaf\x84\xe5\x88\x86\xe5\x88\x86\xe6\x95\xb0
        :param propName: \xe5\x9b\x9e\xe9\x80\x80\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7\xe5\x90\x8d\xe7\xa7\xb0
        :return:
        """
        gamelog.info(gameStrings.TEXT_IMPGUILD_3697, guildNUID, volumnId, propertyId, level, score, propName)
        if guildNUID and (not self.guild or guildNUID != self.guild.nuid):
            return
        volumn = self.guildGrowth.getVolumn(volumnId)
        volumn.score = score
        growth = volumn.getGrowth(propertyId)
        growth.level = level
        gameglobal.rds.ui.guildGrowth.updateLearnGrowthTree(volumnId, propertyId)
        gameglobal.rds.ui.guildGrowth.updateRewardBtnRedPot()

    def onGetGuildWingWorldCamp(self, camp):
        if self.guild:
            self.guild.wingWorldCamp = camp

    def onQueryWingWorldCampGuildInfo(self, wingWorldCamp, wingWorldCampState, wwCampGuildList, wwCampMemberList, wingWorldCampPower):
        if self.guild:
            self.guild.wingWorldCamp = wingWorldCamp
            self.guild.wingWorldCampState = wingWorldCampState
            self.guild.wwCampGuildList = wwCampGuildList
            self.guild.wwCampMemberList = wwCampMemberList
            self.guild.wingWorldCampPower = wingWorldCampPower
            gameglobal.rds.ui.wingWorldCamp.refreshInfo()

    def onQueryWingWorldCampGuildRelation(self, wingWorldCampFriendName, wingWorldCampEnemyName):
        if self.guild:
            self.guild.wingWorldCampFriendName = wingWorldCampFriendName
            self.guild.wingWorldCampEnemyName = wingWorldCampEnemyName
            gameglobal.rds.ui.wingCampGuildRelation.refreshInfo()

    def onUpdateWWCampList(self, wwCampGuildList, wwCampMemberList):
        if self.guild:
            self.guild.wwCampGuildList = wwCampGuildList
            self.guild.wwCampMemberList = wwCampMemberList
            gameglobal.rds.ui.wingCampGuildList.refreshInfo()

    def onUpdateWWCampGuildSignUpState(self, state):
        if self.guild:
            self.guild.wingWorldCampState = state
            gameglobal.rds.ui.wingWorldCamp.refreshSignIn()
            self.addWWCampAutoFollowGuildPush()

    def addWWCampAutoFollowGuildPush(self):
        if self.lv >= 69 and self.wwcAutoFollow and self.guild and self.guild.wingWorldCampState == gametypes.WW_CAMP_GUILD_STATE_SIGNED:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_GUILD_SIGN, {'click': self.onNotifyWWCampAutoFollowClick})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_GUILD_SIGN)
        else:
            self.removeWWCampGuildStatePush()

    def onNotifyWWCampAutoFollowClick(self):
        self.removeWWCampGuildStatePush()
        from data import game_msg_data as GMD
        from cdata import game_msg_def_data as GMDD
        msg = GMD.data.get(GMDD.data.WING_CAMP_ADD_GUILD_SIGN_LIST, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onNotifyWWCampGuildStateClick, yesBtnText=gameStrings.TEXT_IMPGUILD_3755, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def removeWWCampGuildStatePush(self):
        if uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_GUILD_SIGN in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_GUILD_SIGN)

    def onNotifyWWCampGuildStateClick(self):
        self.removeWWCampGuildStatePush()
        if self.isWingWorldCamp():
            gameglobal.rds.ui.wingWorld.show(uiConst.WING_WORLD_TAB_CAMP)
            gameglobal.rds.ui.wingCampGuildList.show()

    def onAddGuildMemberGSXY(self):
        """
        \xe8\xa2\xab\xe6\xb7\xbb\xe5\x8a\xa0\xe8\xa1\x80\xe6\x88\x98\xe6\x88\x90\xe5\x91\x98
        :return:
        """
        gamelog.info('jbx:onAddGuildMemberGSXY')
        gameglobal.rds.ui.crossServerSXYSet.updateMembers()

    def onRemoveGuildMemberGSXY(self):
        """
        \xe8\xa2\xab\xe5\x88\xa0\xe9\x99\xa4\xe8\xa1\x80\xe6\x88\x98\xe6\x88\x90\xe5\x91\x98
        :return:
        """
        gamelog.info('jbx:onRemoveGuildMemberGSXY')
        gameglobal.rds.ui.crossServerSXYSet.updateMembers()

    def onUpdateGuildMemberGSXY(self, gbIds):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe8\xa1\x80\xe6\x88\x98\xe6\x88\x90\xe5\x91\x98
        :param gbIds: set
        :return:
        """
        gamelog.info('jbx:onUpdateGuildMemberGSXY', gbIds)
        self.crossServerSXYGbIds = list(gbIds)
        gameglobal.rds.ui.crossServerSXYSet.updateFbEliteMembersList(self.crossServerSXYGbIds)

    def onQueryGuildDonateWeeklyNum(self, guildDonateWeeklyNum):
        p = BigWorld.player()
        if p.guild:
            p.guild.guildDonateWeeklyNum = guildDonateWeeklyNum
        gameglobal.rds.ui.guildDonate.refreshInfo()
        gamelog.info('@lyh onQueryGuildDonateWeeklyNum================', guildDonateWeeklyNum)

    def onSyncMLStageGSXY(self, stage):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe5\x88\x86\xe7\xba\xbf\xe9\x98\xb6\xe6\xae\xb5
        :param stage: \xe5\x8f\x82\xe8\x80\x83 commGSXY
        :return:
        """
        needRefreshTopLogo = getattr(self, 'gsxyMLStage', 0) != stage and stage == commGSXY.GLOBAL_SXY_ML_STAGE_COMBAT
        self.gsxyMLStage = stage
        if needRefreshTopLogo:
            for en in BigWorld.entities.values():
                if not en.__class__.__name__ == 'Avatar':
                    continue
                en.topLogo.updateAvatarBloodColor(en)
                if not BigWorld.player().isEnemy(en):
                    en.topLogo.updateAvatarBloodColor(en)
                else:
                    en.topLogo.setColor('red')
                    en.topLogo.setBloodColor('red')

    def onUpdateGuildYanwuQL(self, yanwuQL):
        self.yanwuQL = yanwuQL
        gameglobal.rds.ui.clanWarSkill.refreshYanwuPoint()

    def onUpdateGuildYanwuBH(self, yanwuBH):
        self.yanwuBH = yanwuBH
        gameglobal.rds.ui.clanWarSkill.refreshYanwuPoint()
