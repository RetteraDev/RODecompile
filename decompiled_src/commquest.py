#Embedded file name: /WORKSPACE/data/entities/common/commquest.o
import time
import random
import BigWorld
import const
import gametypes
import gamescript
import gamelog
import formula
import utils
import commNpcFavor
from item import Item
from sMath import distance3D
if BigWorld.component in ('cell', 'base'):
    import gameconfig
    import gameengine
    import serverProgress
elif BigWorld.component in 'client' and not getattr(BigWorld, 'isBot', False):
    import clientUtils
    import gameglobal
    from guis import groupUtils
from data import quest_data as QD
from data import state_data as SD
from data import quest_loop_data as QLD
from cdata import quest_reward_data as QRD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import quest_npc_relation as QNR
from data import consumable_item_data as CID
from data import quest_marker_data as QMD
from data import emotion_action_data as EAD
from data import quest_group_data as QGD
from data import quest_extra_data as QED
from data import delegation_data as DD
from data import delegation_upgrade_data as DUD
from data import job_data as JD
from cdata import quest_loop_inverted_data as QLID
from cdata import quest_delegation_inverted_data as QDID
from cdata import questloop_job_inverted_data as QJID
from cdata import delegation_rank_inverted_data as DRID
from data import world_quest_data as WQD
from data import monster_event_trigger_data as METD
from cdata import delegation_cash_ratio_data as DCRD
from cdata import delegation_exp_ratio_data as DERD
from cdata import quest_plus_data as QPD
from data import sys_config_data as SCD
from cdata import quest_abnormal_repair_data as QARD
from data import delegation_config_data as DCD
from data import isolate_config_data as ICD
from data import junjie_config_data as JCD
from data import title_data as TD
from data import rune_data as RD
from cdata import business_lv_config_data as BLCD
from cdata import business_quest_set_data as BQSD
from data import business_config_data as BCD
from data import fame_data as FD
from data import intimacy_data as IMD
from data import qiren_clue_data as QCD
from data import achievement_data as AD
from data import quest_type_show_data as QTSD
from data import world_quest_refresh_data as WQRD
from cdata import quest_item_group_data as QIGD
from cdata import server_progress_prop_def_data as SPPPD
MAX_AVL_QUEST = 50

def isQuestDisable(questId):
    if not QD.data.has_key(questId):
        return True
    hid = utils.getHostId()
    if BigWorld.component == 'client':
        publicServer = gameglobal.rds.configData.get('publicServer', False)
    else:
        publicServer = gameconfig.publicServer()
    enableHosts = {0: (hid,),
     1: (),
     2: (hid,) if publicServer else ()}
    qd = QD.data[questId]
    if hid not in enableHosts.get(qd.get('disable', 0), (hid,)):
        return True
    if qd.has_key('disableSwitch'):
        switch = qd['disableSwitch']
        if BigWorld.component in 'cell':
            if not hasattr(gameconfig, switch) or not getattr(gameconfig, switch)():
                return True
        elif BigWorld.component in 'client':
            if not gameglobal.rds.configData.get(switch, False):
                return True
    return False


def isQuestLoopDisable(questLoopId):
    qld = QLD.data.get(questLoopId, {})
    if not qld:
        return True
    if qld.get('disable', 0):
        return True
    if qld.has_key('disableSwitch'):
        switch = qld['disableSwitch']
        if BigWorld.component in 'cell':
            if not hasattr(gameconfig, switch) or not getattr(gameconfig, switch)():
                return True
        elif BigWorld.component in 'client':
            if gameglobal.rds.configData.get(switch, False):
                return True
    return False


def getQuestCompNpc(owner, questId):
    qd = QD.data[questId]
    compNpcType = qd.get('compNpcType', gametypes.QUEST_COMPNPC_DEFINE)
    if compNpcType in (gametypes.QUEST_COMPNPC_EXACT, gametypes.QUEST_COMPNPC_RANDOM_EXLUDE_ACNPC):
        return owner.getQuestData(questId, const.QD_COMPNPC)
    else:
        return qd.get('compNpc', None)


def getAcNpc(owner, questId):
    qd = QD.data[questId]
    if QLID.data.has_key(questId):
        questLoopId = QLID.data[questId]['questLoop']
        acNpcType = qd.get('acNpcType', gametypes.QUEST_ACNPC_RANDOM)
        if acNpcType == gametypes.QUEST_ACNPC_EXACT and owner.questLoopInfo.has_key(questLoopId):
            return owner.questLoopInfo[questLoopId].lastCompNpc
        else:
            return qd.get('acNpc', None)
    else:
        return qd.get('acNpc', None)


def _gainQuestPlusCheck(owner, questId, bMsg, channel):
    qpd = QPD.data.get(questId, None)
    if not qpd:
        return True
    minSocLv = qpd.get('minSocLv', 0)
    if owner.socLv < minSocLv:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOCIAL_LEVEL_LOWER, (minSocLv,))
        return False
    maxSocLv = qpd.get('maxSocLv', 0)
    if 0 < maxSocLv < owner.socLv:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOCIAL_LEVEL_UPPER, (maxSocLv,))
        return False
    reqSocExp = qpd.get('reqSocExp', 0)
    if 0 < reqSocExp < owner.socExp:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOCIAL_EXP_LOWER, (reqSocExp,))
        return False
    acLifeSkills = qpd.get('acLifeSkills', ())
    for reqSkill in acLifeSkills:
        skid, lv = reqSkill
        if BigWorld.component == 'cell':
            if skid not in owner.lifeSkills.keys() or owner.lifeSkills[skid].level < lv:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LIFESKILL_LEVEL_LOWER, (lv,))
                return False
        elif BigWorld.component == 'client':
            if skid not in owner.lifeSkill.keys() or owner.lifeSkill[skid]['level'] < lv:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LIFESKILL_LEVEL_LOWER, (lv,))
                return False

    acLifeSkillExp = qpd.get('acLifeSkillExp', ())
    for reqExp in acLifeSkillExp:
        skid, exp = reqExp
        if BigWorld.component == 'cell':
            if skid not in owner.lifeSkills.keys() or owner.lifeSkills[skid].exp < exp:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LIFESKILL_EXP_LOWER, ())
                return False
        elif BigWorld.component == 'client':
            if skid not in owner.lifeSkill.keys() or owner.lifeSkill[skid]['exp'] < exp:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LIFESKILL_EXP_LOWER, ())
                return False

    acFishingLv = qpd.get('acFishingLv', 0)
    if owner.fishingLv < acFishingLv:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_FISHING_LEVEL_LOWER, (acFishingLv,))
        return False
    acFishingExp = qpd.get('acFishingExp', 0)
    if owner.fishingExp < acFishingExp:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_FISHING_EXP_LOWER, ())
        return False
    acExploreLv = qpd.get('acExploreLv', 0)
    if owner.exploreLv < acExploreLv:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_EXPLORE_LEVEL_LOWER, (acExploreLv,))
        return False
    acExploreExp = qpd.get('acExploreExp', 0)
    allExp = owner.xiangyaoExp + owner.xunbaoExp + owner.zhuizongExp
    if allExp < acExploreExp:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_EXPLORE_EXP_LOWER, ())
        return False
    acSocProps = qpd.get('acSocProps', ())
    for prop in acSocProps:
        propId, value = prop
        if owner.getSocPrimaryPropValue(propId) < value:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOC_PROP_LOWER, ())
            return False

    ss = qpd.get('reqSocSchoolStatus', None)
    if ss:
        sid, status = ss
        if not utils.getSocSchoolStatus(owner, sid, status):
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOC_SCHOOL_MISMATCH, ())
            return False
    reqCash = qpd.get('reqCash', ())
    if reqCash and reqCash > owner.cash + owner.bindCash:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_MONEY_LOWER, (reqCash,))
        return False
    acTitleId = qpd.get('acTitleId', 0)
    if acTitleId and acTitleId in TD.data.keys():
        if acTitleId not in owner.currTitle:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TITLE, (TD.data[acTitleId].get('name', ''),))
            return False
    acAchieveId = qpd.get('acAchieve', 0)
    if acAchieveId and acAchieveId in AD.data.keys():
        if BigWorld.component == 'client':
            if acAchieveId not in gameglobal.rds.ui.achvment.gainedAchieveIds:
                return False
        elif BigWorld.component == 'cell':
            if not owner.getAchieveFlag(acAchieveId):
                return False
    return True


def gainQuestCheck(owner, questId, bMsg = True, bShare = False):
    backQuestId = questId
    td = QD.data.get(questId)
    if BigWorld.component in 'cell':
        channel = owner.client
    elif BigWorld.component in 'client':
        channel = owner
    if td is None or isQuestDisable(questId):
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_NEED_ABANDON, ())
        return False
    now = utils.getNow()
    if (now - utils.getServerOpenTime() + 3) / 3600 < td.get('timeInterval', 0):
        return False
    if owner.getQuestForbidFlag(questId):
        return False
    if td.get('autoAbandon'):
        return False
    if utils.getEnableCheckServerConfig():
        serverConfigId = td.get('serverConfigId', 0)
        if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
            return False
    if bShare and not td.get('shareQuest', 0):
        if bMsg:
            pass
        return False
    sex = td.get('acSex', 0)
    if sex > 0 and owner.physique.sex != sex:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SEX, ())
        return False
    if td.has_key('school'):
        school = td.get('school')
        if owner.physique.school != school:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SCHOOL, ())
            return False
    if td.has_key('schoolExclude'):
        schoolExclude = td.get('schoolExclude')
        if owner.physique.school in schoolExclude:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SCHOOL_EXCLUDE, ())
            return False
    if questId in owner.quests:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ALREADY_ACCEPT, ())
        return False
    if owner.getQuestFlag(questId):
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ALREADY_COMPLETE, ())
        return False
    if td.has_key('acMinLv'):
        if owner.lv < td['acMinLv']:
            if bMsg:
                minLv = str(td['acMinLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_LOWER, (minLv,))
            return False
    if td.has_key('acNpcFavorMinLv') and hasattr(channel, 'npcFavor'):
        npcId, minLv = td['acNpcFavorMinLv']
        pVal = channel.npcFavor.npcFavorValue.get(npcId, 0)
        lv = commNpcFavor.getPFriendlyLv(npcId, pVal, channel)
        if lv < minLv:
            return False
    if td.has_key('acMaxLv'):
        if owner.lv > td['acMaxLv']:
            if bMsg:
                maxLv = str(td['acMaxLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_UPPER, (maxLv,))
            return False
    if td.has_key('acPreQst') and owner.lv < td.get('acPreQstLvLimit', const.MAX_LEVEL):
        for quests in td['acPreQst']:
            enough = True
            if not isinstance(quests, tuple):
                quests = tuple([quests])
            isAll = False
            for qid in quests:
                if owner.getQuestFlag(qid):
                    isAll = True
                    break

            if isAll is False:
                enough = False
            if enough is False:
                questIds = []
                for quests in td['acPreQst']:
                    if not isinstance(quests, tuple):
                        questIds.append(quests)
                    else:
                        questIds.extend(list(quests))

                if bMsg:
                    for qid in questIds:
                        channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NEED_PRE_QUEST, (QD.data[qid]['name'],))

                return False

    if td.has_key('acNeedQsts'):
        for quests in td['acNeedQsts']:
            enough = True
            if not isinstance(quests, tuple):
                quests = tuple([quests])
            isAll = False
            for qid in quests:
                if qid in owner.quests:
                    isAll = True
                    break

            if isAll is False:
                enough = False
            if enough is False:
                if bMsg:
                    for qid in quests:
                        channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NEED_COND_QUEST, (QD.data[qid]['name'],))

                return False

    if td.has_key('acNotNeedQsts'):
        for qid in td['acNotNeedQsts']:
            if qid in owner.quests:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NOT_NEED_COND_QUEST, (QD.data[qid]['name'],))
                return False

    if td.has_key('notAcOrCompQsts'):
        questIds = td['notAcOrCompQsts']
        for checkQuestId in questIds:
            if checkQuestId in owner.quests or owner.getQuestFlag(checkQuestId):
                return False

    if td.has_key('acOrCompQsts'):
        for quests in td['acOrCompQsts']:
            enough = True
            if not isinstance(quests, tuple):
                quests = tuple([quests])
            isAll = False
            for qid in quests:
                if qid in owner.quests or owner.getQuestFlag(qid):
                    isAll = True
                    break

            if isAll is False:
                enough = False
            if enough is False:
                if bMsg:
                    for qid in quests:
                        channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NEED_COND_QUEST, (QD.data[qid]['name'],))

                return False

    if td.has_key('acMutexQst'):
        for quests in td['acMutexQst']:
            enough = False
            if not isinstance(quests, tuple):
                quests = tuple([quests])
            isAll = True
            for qid in quests:
                if not owner.getQuestFlag(qid) and qid not in owner.quests:
                    isAll = False
                    break

            if isAll:
                enough = True
            if enough is True:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_MUTEX, (QD.data[questId]['name'],))
                return False

    if td.has_key('needTempCamp'):
        if owner.pvpTempCamp != td['needTempCamp']:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WRONG_CAMP, ())
            return False
    clanCourierCamp = td.get('clanCourierCamp', 0)
    if clanCourierCamp == 1 and not owner.isJct:
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WRONG_CAMP, ())
        return False
    if clanCourierCamp == 2 and not owner.isClanCourierAvatar():
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WRONG_CAMP, ())
        return False
    if td.has_key('acFame'):
        acFame = td['acFame']
        if not owner.enoughFame(acFame):
            if BigWorld.component == 'cell' or not td.get('acFameSeen', 0):
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_ACFAME, (acFame[0][1],))
                return False
    if td.has_key('acMaxFame'):
        acMaxFame = td['acMaxFame']
        if owner.enoughFame(acMaxFame):
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_ACFAME, (acMaxFame[0][1],))
            return False
    if td.has_key('acFameCost'):
        acFameCost = td['acFameCost']
        if not owner.enoughFame(acFameCost):
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_ACFAMECOST, (acFameCost[0][1],))
            return False
    if td.has_key('acNeedGuild'):
        if td['acNeedGuild'] and not owner.guildNUID:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_GUILD, ())
            if not (BigWorld.component in 'client' and td.get('forceToDisplay', 0)):
                return False
    if td.has_key('guildJoinTimeLimit'):
        if owner.guildNUID == 0 or owner.guildTJoin + td['guildJoinTimeLimit'] >= now:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_GUILD_JOIN_TIME, ())
            return False
    if td.has_key('antiIndulgeStates'):
        indulgeState = owner.getIndulgeProfitState()
        if indulgeState in td['antiIndulgeStates']:
            if bMsg:
                channel.showGameMsg(GMDD.data.ANTIINDULGE_CANNOT_TAKE_QUEST, ())
            return False
    if td.has_key('serverProgressMsId'):
        msId = td['serverProgressMsId']
        if msId and not owner.checkServerProgress(msId, bMsg=bMsg):
            return False
    validInBianyao = td.get('validInBianyao', gametypes.FUNCTION_INVALID_FOR_YAO)
    if owner._isInBianyao() and validInBianyao == gametypes.FUNCTION_INVALID_FOR_YAO:
        return False
    if not owner._isInBianyao() and validInBianyao == gametypes.FUNCTION_VALID_ONLY_FOR_YAO:
        return False
    if td.has_key('businessLv'):
        if not owner.guildBusiness:
            return False
        businessQuestIds = BQSD.data[1]
        for businessQuestId in businessQuestIds:
            if businessQuestId in owner.quests:
                return False

    if td.has_key('needMental'):
        needMental = td['needMental']
        if owner.mental < needMental:
            return False
    if BigWorld.component == 'client':
        if td.has_key('acGuildLv'):
            if owner.guild is None or owner.guild.level < td['acGuildLv']:
                return False
        if td.has_key('acGuildBuildMarkers'):
            if owner.guild is None:
                return False
            for markerId, lv in td['acGuildBuildMarkers']:
                if owner.guild.isBuildingFinished(markerId):
                    continue
                if not owner.guild.marker[markerId].inBuilding(owner.guild):
                    continue
                marker = owner.guild.marker.get(markerId)
                building = marker.getBuilding(owner.guild)
                if building is None or building.level != lv:
                    continue
                break
            else:
                return False

        if td.has_key('acGuildBuildMarkersLv'):
            if owner.guild is None:
                return False
            for markerId, lv in td['acGuildBuildMarkersLv']:
                marker = owner.guild.marker.get(markerId)
                building = marker.getBuilding(owner.guild)
                if building is not None and building.level >= lv:
                    break
            else:
                return False

        if td.has_key('acGuildDevMarkers'):
            if owner.guild is None:
                return False
            for markerId, minProgress, maxProgress in td['acGuildDevMarkers']:
                if not owner.guild.marker or not owner.guild.marker.has_key(markerId):
                    return False
                if owner.guild.isDevFinished(markerId):
                    return False
                if not owner.guild.marker[markerId].inDev():
                    return False
                if owner.guild.marker[markerId].progress <= minProgress or owner.guild.marker[markerId].progress > maxProgress:
                    return False

        if td.has_key('acGuildAreas'):
            if owner.guild is None:
                return False
            for areaId in td['acGuildAreas']:
                if owner.guild.isAreaExtFinished(areaId):
                    return False

        if td.has_key('businessLv'):
            businessLv = td['businessLv']
            blcd = BLCD.data[businessLv]
            if not hasattr(owner.guild, 'bindCash') or owner.guild.bindCash < blcd['baseFame']:
                return False
            if owner.guild.getSelfContrib() < 0:
                return False
    if td.has_key('acQumoLv'):
        if owner.qumoLv != td['acQumoLv']:
            return False
    if td.has_key('acPreQumoLv'):
        if owner.preQumoLv != td['acPreQumoLv']:
            return False
    if td.has_key('needJunJieLv'):
        if owner.junJieLv < td['needJunJieLv']:
            return False
    if td.has_key('needJueWeiLv'):
        if owner.jueWeiLv < td['needJueWeiLv']:
            return False
    apprenticeType = td.get('gainReqApprenticeType', 0)
    if apprenticeType:
        if enableNewApprentice():
            flag = apprenticeTypeCheckEx(owner, apprenticeType)
        else:
            flag = apprenticeTypeCheck(owner, apprenticeType)
        if not flag:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_APPRENTICE_FAIL, ())
            if not (BigWorld.component in 'client' and td.get('forceToDisplay', 0)):
                return False
    gainReqGraduateApprentice = td.get('gainReqGraduateApprentice', 0)
    if gainReqGraduateApprentice:
        if enableNewApprentice():
            flag = apprenticeGraduateCheckEx(owner)
        else:
            flag = apprenticeGraduateCheck(owner)
        if not flag:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_APPRENTICE_NOT_GRAUDATE, ())
            if not (BigWorld.component in 'client' and td.get('forceToDisplay', 0)):
                return False
    if td.has_key('acTeamOnly'):
        if BigWorld.component == 'cell' and owner.groupType != gametypes.GROUP_TYPE_TEAM_GROUP:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TEAM_ONLY, ())
            return False
    if td.has_key('acTeamCnt'):
        teamCnt = td['acTeamCnt']
        if BigWorld.component == 'cell':
            if len(owner.team) != teamCnt:
                if td.get('isShowIgnoreTeamCnt', 0):
                    bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TEAM_CNT, (teamCnt,))
                return False
        elif BigWorld.component == 'client':
            if not td.get('isShowIgnoreTeamCnt', 0):
                cnt = len([ x for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ])
                if cnt != teamCnt:
                    return False
    if td.has_key('acTeamCntLarger'):
        teamCnt = td['acTeamCntLarger']
        if BigWorld.component == 'cell':
            if len(owner.team) <= teamCnt:
                if td.get('isShowIgnoreTeamCnt', 0):
                    bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TEAM_LARGER_CNT, (teamCnt,))
                return False
    if td.has_key('acTeamCntLess'):
        teamCnt = td['acTeamCntLess']
        if BigWorld.component == 'cell':
            if len(owner.team) >= teamCnt:
                if td.get('isShowIgnoreTeamCnt', 0):
                    bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TEAM_LESS_CNT, (teamCnt,))
                return False
        elif BigWorld.component == 'client':
            cnt = len([ x for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ])
            if cnt >= teamCnt:
                return False
    if td.has_key('acBoyCnt'):
        boyCnt = td['acBoyCnt']
        if BigWorld.component == 'cell':
            curBoyCnt = len([ x for x in owner.team.values() if x.sex == 1 ])
            if curBoyCnt != boyCnt:
                return False
        elif BigWorld.component == 'client':
            members = [ owner.members[x] for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ]
            curBoyCnt = len([ x for x in members if x['sex'] == 1 ])
            if curBoyCnt != boyCnt:
                return False
    if td.has_key('acGirlCnt'):
        girlCnt = td['acGirlCnt']
        if BigWorld.component == 'cell':
            curGirlCnt = len([ x for x in owner.team.values() if x.sex == 2 ])
            if curGirlCnt != girlCnt:
                return False
        elif BigWorld.component == 'client':
            members = [ owner.members[x] for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ]
            curGirlCnt = len([ x for x in members if x['sex'] == 2 ])
            if curGirlCnt != girlCnt:
                return False
    if td.has_key('acBuff'):
        if td['acBuff'] not in owner.statesServerAndOwn:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_BUFF_FAIL, ())
            return False
    if td.has_key('acStatesCheck'):
        states = td['acStatesCheck']
        for stateName in states:
            if BigWorld.component == 'cell':
                if not getattr(owner, '_check_' + stateName)():
                    return False
            elif BigWorld.component == 'client':
                if not getattr(owner.stateMachine, '_check_' + stateName)():
                    return False

    if td.has_key('needHeader') and owner.groupHeader != owner.id:
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_HEADER_FAIL, ())
        return False
    if td.has_key('checkFbNo') and formula.inExcludeFubenList(td['checkFbNo'], owner.fbStatusList):
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_CHECK_FB_FAIL, ())
        return False
    if td.has_key('hasItem'):
        if not checkHasEnoughItem(owner, td['hasItem'][0], td['hasItem'][1]):
            bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_CHECK_ENOUGH_ITEM_FAIL, (td['hasItem'][1], ID.data.get(td['hasItem'][0], {}).get('name', '')))
            return False
    if td.has_key('needQirenClues'):
        qcds = td.get('needQirenClues', ())
        for qcd in qcds:
            if not owner.getClueFlag(qcd):
                clueFailMsgId = QCD.data.get(qcd, {}).get('clueFailMsgId', 0)
                if clueFailMsgId and bMsg:
                    channel.showGameMsg(clueFailMsgId, ())
                return False

    if td.get('puzzleChoice', None):
        if not owner.getPuzzleChoiceFlag(questId):
            return False
    if td.has_key('wwTempCamp'):
        if owner.getWorldWarTempCamp() != td['wwTempCamp']:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WORLD_WAR_CAMP, ())
            return False
    if td.get('isCross') and not td.get('isBodyAcc') and not owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOUL, ())
        return False
    if not td.get('isCross') and owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOUL, ())
        return False
    if td.has_key('intimacytTgt'):
        intimacytTgtFlag = td['intimacytTgt']
        if BigWorld.component == 'cell':
            if gametypes.ACCEPT_QUEST_NEED_INTIMACY == intimacytTgtFlag and not owner.cellOfIntimacyTgt:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NEED_INTIMACYT, ())
                return False
            if gametypes.ACCEPT_QUEST_NOT_NEED_INTIMACY == intimacytTgtFlag and owner.cellOfIntimacyTgt:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT, ())
                return False
            if gametypes.ACCEPT_QUEST_NEED_INTIMACY_AND_SAME_TEAM == intimacytTgtFlag and (not owner.cellOfIntimacyTgt or owner.cellOfIntimacyTgt not in owner.team.keys()):
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT_AND_SAME_TEAM, ())
                return False
        elif BigWorld.component == 'client':
            if gametypes.ACCEPT_QUEST_NEED_INTIMACY == intimacytTgtFlag and not owner.friend.intimacyTgt:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NEED_INTIMACYT, ())
                return False
            if gametypes.ACCEPT_QUEST_NOT_NEED_INTIMACY == intimacytTgtFlag and owner.friend.intimacyTgt:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT, ())
                return False
            if gametypes.ACCEPT_QUEST_NEED_INTIMACY_AND_SAME_TEAM == intimacytTgtFlag and (not owner.friend.intimacyTgt or owner.friend.intimacyTgt not in owner.members.keys()):
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT_AND_SAME_TEAM, ())
                return False
    acExcitement = td.get('acExcitement')
    if acExcitement:
        if not owner.checkExcitementFeature(acExcitement):
            return False
    if BigWorld.component == 'cell' and td.get('hasHome'):
        if not owner.home.hasHome():
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NO_HOME, ())
            return False
    return _gainQuestPlusCheck(owner, backQuestId, bMsg, channel)


def gainQuestLoopSimpleCheck(owner, questLoopId, bMsg = True, npcNo = None, itemNo = None, acStep = -1):
    qld = QLD.data.get(questLoopId)
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if qld is None or isQuestLoopDisable(questLoopId):
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ALREADY_DELETE, ())
        return False
    if owner.questLoopInfo.has_key(questLoopId) and owner.questLoopInfo[questLoopId].getCurrentQuest() is not None:
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ALREADY_ACCEPT, ())
        return False
    if qld.get('autoAbandon'):
        return False
    if owner.getQuestLoopForbidFlag(questLoopId):
        return False
    if not owner.checkWorldRefreshQuestLoop(questLoopId):
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WORLD_REFRESH_CD, ())
        return False
    if qld.has_key('acPreQstLoop'):
        acPreQstLoops = qld.get('acPreQstLoop', ())
        for acPreQstLoopId in acPreQstLoops:
            if not owner.getQuestLoopFlag(acPreQstLoopId):
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NEED_PRE_QUEST_LOOP, (QLD.data.get(acPreQstLoopId, {}).get('name', ''),))
                return False

    if qld.has_key('acMinLv'):
        if owner.lv < qld['acMinLv']:
            if bMsg:
                minLv = str(qld['acMinLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_LOWER, (minLv,))
            return False
    if qld.has_key('acMaxLv'):
        if owner.lv > qld['acMaxLv']:
            if bMsg:
                maxLv = str(qld['acMaxLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_UPPER, (maxLv,))
            return False
    if qld.has_key('acStartTimes') and qld.has_key('acEndTimes'):
        actStartTime = qld['acStartTimes']
        actEndTime = qld['acEndTimes']
        if True not in [ utils.inTimeTupleRange(actStartTime[i], actEndTime[i], current) for i in xrange(len(actStartTime)) ]:
            return False
    if questLoopId in owner.questLoopInfo:
        questLoop = owner.questLoopInfo[questLoopId]
        if not questLoop.acQuestCheck(owner, acStep, bMsg):
            return False
    acQuestLoops = {}
    if npcNo:
        qnr = QNR.data.get(npcNo, {})
        if not qnr.has_key('acQuestGroups'):
            return False
        acQuestLoops.update(qnr['acQuestGroups'])
    if itemNo:
        itemData = CID.data.get(itemNo, {})
        if not itemData.has_key('questLoop'):
            return False
        acQuestLoops.update(itemData['questLoop'])
    if len(acQuestLoops) > 0:
        if questLoopId not in acQuestLoops:
            return False
        acQuests = acQuestLoops[questLoopId]
        if questLoopId in owner.questLoopInfo:
            questLoop = owner.questLoopInfo[questLoopId]
            questIds = questLoop.getNextQuests(owner)
        else:
            questIds = getAvaiNextQuestsInLoop(owner, questLoopId, 0)
        isValid = False
        for questId in questIds:
            if questId in acQuests:
                isValid = True

        if isValid is False:
            if bMsg:
                channel.chatToEventEx('无法接取任务组%d' % questLoopId, const.CHANNEL_COLOR_RED)
            return False
    return True


def gainQuestLoopCheck(owner, questLoopId, bMsg = True, npcNo = None, itemNo = None, bShare = False, acStep = -1):
    qld = QLD.data.get(questLoopId)
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if qld is None or isQuestLoopDisable(questLoopId):
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ALREADY_DELETE, ())
        return False
    if utils.getEnableCheckServerConfig():
        serverConfigId = qld.get('serverConfigId', 0)
        if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
            return False
    if owner.questLoopInfo.has_key(questLoopId) and owner.questLoopInfo[questLoopId].getCurrentQuest() is not None:
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ALREADY_ACCEPT, ())
        return False
    if qld.get('autoAbandon'):
        return False
    if owner.getQuestLoopForbidFlag(questLoopId):
        return False
    if not owner.checkWorldRefreshQuestLoop(questLoopId):
        bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WORLD_REFRESH_CD, ())
        return False
    if qld.has_key('acPreQstLoop'):
        acPreQstLoops = qld.get('acPreQstLoop', ())
        for acPreQstLoopId in acPreQstLoops:
            if not owner.getQuestLoopFlag(acPreQstLoopId):
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_NEED_PRE_QUEST_LOOP, (QLD.data.get(acPreQstLoopId, {}).get('name', ''),))
                return False

    if qld.has_key('acMinLv'):
        if owner.lv < qld['acMinLv']:
            if bMsg:
                minLv = str(qld['acMinLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_LOWER, (minLv,))
            return False
    if qld.has_key('acMaxLv'):
        if owner.lv > qld['acMaxLv']:
            if bMsg:
                maxLv = str(qld['acMaxLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_LEVEL_UPPER, (maxLv,))
            return False
    if qld.has_key('acWWStartLv'):
        if owner.getWorldWarQuestStarLv() != qld['acWWStartLv']:
            if bMsg:
                acWWStartLv = str(qld['acWWStartLv'])
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WORLD_WAR_LEVEL, (acWWStartLv,))
            return False
    if qld.get('isCross') and not qld.get('isBodyAcc') and not owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOUL, ())
        return False
    if not qld.get('isCross') and owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_SOUL, ())
        return False
    if qld.has_key('wwTempCamp'):
        if owner.getWorldWarTempCamp() != qld['wwTempCamp']:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_WORLD_WAR_CAMP, ())
            return False
    if qld.get('type', gametypes.QUEST_LOOP_TYPE_NORMAL) in (gametypes.QUEST_LOOP_TYPE_ONCE,):
        if owner.getQuestLoopFlag(questLoopId):
            return False
    if qld.has_key('acMutexQst'):
        for acQuestLoopId in qld['acMutexQst']:
            if owner.questLoopInfo.has_key(acQuestLoopId) and (len(owner.questLoopInfo[acQuestLoopId].questInfo) > 0 or owner.questLoopInfo[acQuestLoopId].loopCnt > 0):
                return False

    if qld.has_key('weekSet'):
        weekSet = qld.get('weekSet', 0)
        if utils.isInvalidWeek(weekSet):
            return False
    if qld.has_key('acStartTimes') and qld.has_key('acEndTimes'):
        actStartTime = qld['acStartTimes']
        actEndTime = qld['acEndTimes']
        if True not in [ utils.inTimeTupleRange(actStartTime[i], actEndTime[i], current) for i in xrange(len(actStartTime)) ]:
            return False
    if qld.has_key('acXingjiTimes'):
        acXingjiTimes = qld['acXingjiTimes']
        if not formula.isInXingJiTimeIntervals(acXingjiTimes):
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_XINGJITIME_INVALID, ())
            return False
    if qld.has_key('serverProgressMsId'):
        msId = qld['serverProgressMsId']
        if msId and not owner.checkServerProgress(msId, bMsg=bMsg):
            return False
    if questLoopId in owner.questLoopInfo:
        questLoop = owner.questLoopInfo[questLoopId]
        if not questLoop.acQuestCheck(owner, acStep, bMsg):
            return False
    if QDID.data.has_key(questLoopId):
        dId = QDID.data[questLoopId]
        if owner.getDelegationData(dId, const.DD_FAIL):
            return False
        if owner.getDelegationData(dId, const.DD_STATUS) in (const.DS_TYPE_AGENTED, const.DS_TYPE_EMPLOY):
            return False
    if qld.get('isolateFlag') > 0:
        if owner.isolateType == gametypes.ISOLATE_TYPE_NONE:
            return False
        if ICD.data['isolateQuestInterval'].has_key(owner.isolateType):
            current = utils.getNow()
            if current <= owner.isolateTime + ICD.data['isolateQuestInterval'][owner.isolateType]:
                return False
        if BigWorld.component == 'cell':
            expectLiberateCnt = getExpectLiberateCnt(owner)
            if owner.liberateCnt >= expectLiberateCnt:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_ISOLATE_LIBERATE, ())
                return False
    if qld.has_key('acTeamOnly'):
        if owner.groupType != gametypes.GROUP_TYPE_TEAM_GROUP:
            from data import quest_loop_chain_data as QLCD
            if gameconfig.enableQuestLoopChain() and owner.groupType == gametypes.GROUP_TYPE_NON_GROUP and QLCD.data.has_key((questLoopId, 1)):
                channel.chatNpcInviteTeam(const.CHAT_INVITE_TEAM_FOR_XUNLING)
            bMsg and owner.sendGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_TEAM_ONLY, ())
            return False
    acQuestLoops = {}
    if npcNo:
        qnr = QNR.data.get(npcNo, {})
        if not qnr.has_key('acQuestGroups'):
            return False
        acQuestLoops.update(qnr['acQuestGroups'])
    if itemNo:
        itemData = CID.data.get(itemNo, {})
        if not itemData.has_key('questLoop'):
            return False
        acQuestLoops.update(itemData['questLoop'])
    if len(acQuestLoops) > 0:
        if questLoopId not in acQuestLoops:
            return False
        bMsg = False
        if qld.get('accForce'):
            bMsg = True
        acQuests = acQuestLoops[questLoopId]
        if questLoopId in owner.questLoopInfo:
            questLoop = owner.questLoopInfo[questLoopId]
            questIds = questLoop.getNextQuests(owner, bMsg=bMsg)
        else:
            questIds = getAvaiNextQuestsInLoop(owner, questLoopId, 0, bMsg=bMsg)
        isValid = False
        for questId in questIds:
            if questId in acQuests:
                isValid = True

        if isValid is False:
            if bMsg and qld.get('name'):
                channel.chatToEventEx('无法接取任务：%s' % qld.get('name'), const.CHANNEL_COLOR_RED)
            return False
    if qld.has_key('serverProgressMsId'):
        msId = qld['serverProgressMsId']
        if msId and not owner.checkServerProgress(msId, bMsg=bMsg):
            return False
    if qld.has_key('intimacytTgt'):
        intimacytTgtFlag = qld['intimacytTgt']
        if BigWorld.component == 'cell':
            if not owner.cellOfIntimacyTgt and intimacytTgtFlag:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NEED_INTIMACYT, ())
                return False
            if owner.cellOfIntimacyTgt and not intimacytTgtFlag:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT, ())
                return False
        elif BigWorld.component == 'client':
            if not owner.friend.intimacyTgt and intimacytTgtFlag:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NEED_INTIMACYT, ())
                return False
            if owner.friend.intimacyTgt and not intimacytTgtFlag:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_ACCEPT_FAIL_NOT_NEED_INTIMACYT, ())
                return False
    return True


def _completeQuestPlusCheck(owner, questId, bMsg, channel):
    if not QPD.data.has_key(questId):
        return True
    qpd = QPD.data[questId]
    reqSocExp = qpd.get('reqSocExp', 0)
    if 0 < reqSocExp < owner.socExp:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_SOCIAL_EXP_LOWER, (reqSocExp,))
        return False
    reqCash = qpd.get('reqCash', ())
    if reqCash and reqCash > owner.cash + owner.bindCash:
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_MONEY_LOWER, (reqCash,))
        return False
    ss = qpd.get('reqSocSchoolStatus', None)
    if ss:
        sid, status = ss
        if not utils.getSocSchoolStatus(owner, sid, status):
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_SOC_SCHOOL_MISMATCH, ())
            return False
    return True


def completeQuestCheck(owner, questId, bMsg = False):
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if questId not in owner.quests:
        return False
    elif not QD.data.has_key(questId):
        channel.completeQuest(questId, False)
        return False
    qd = QD.data.get(questId)
    orRelation = qd.get('condRelation', 0)
    if qd is None or isQuestDisable(questId):
        return False
    elif owner.getQuestFlag(questId):
        return False
    elif owner.getQuestData(questId, const.QD_FAIL):
        return False
    if qd.has_key('school'):
        school = qd.get('school')
        if owner.physique.school != school:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SCHOOL, ())
            return False
    if qd.has_key('schoolExclude'):
        schoolExclude = qd.get('schoolExclude')
        if owner.physique.school in schoolExclude:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SCHOOL_EXCLUDE, ())
            return False
    if qd.has_key('comMinLv'):
        if owner.lv < qd['comMinLv']:
            if bMsg:
                minLv = qd['comMinLv']
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LEVEL_LOWER, (minLv,))
            return False
    if qd.has_key('comMaxLv'):
        if owner.lv > qd['comMaxLv']:
            if bMsg:
                maxLv = qd['comMaxLv']
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LEVEL_UPPER, (maxLv,))
            return False
    if qd.has_key('failBuff'):
        if qd['failBuff'] in owner.statesServerAndOwn:
            if bMsg:
                buffName = SD.data.get(qd['failBuff'], {}).get('name', '')
                channel.showGameMsg(GMDD.data.QUEST_COMP_REJECT_STATE, (buffName,))
            return False
    if qd.has_key('timeLimit'):
        limit = owner.getQuestData(questId, const.QD_BEGIN_TIME, default=0) + qd['timeLimit']
        if limit < current:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_FAILED_TIMEOUT, (qd['name'],))
            return False
    if qd.has_key('playerSafe') and qd['playerSafe'] > 0:
        playerSafe = owner.getQuestData(questId, const.QD_PLAYER_SAFE, True)
        if playerSafe is False:
            return False
    if qd.has_key('monsterSafe'):
        monsterSafe = owner.getQuestData(questId, const.QD_MONSTER_SAFE, {})
        for charType in qd['monsterSafe']:
            if charType in monsterSafe and monsterSafe[charType] is False:
                return False

    if qd.has_key('compNeedGuild'):
        if qd['compNeedGuild'] and not owner.guildNUID:
            bMsg and channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_GUILD, ())
            return False
    if qd.has_key('needBindEkey'):
        if qd['needBindEkey'] and owner.securityTypeOfCell not in const.SECURITY_TYPE_EKEY:
            return False
    if qd.has_key('vipBarRanks'):
        if owner.vipBarRank not in qd['vipBarRanks']:
            return False
    if qd.get('autoJingJieQuestTo', 0) and qd.get('isRealAutoBreak', 0):
        if utils.checkUpgradeJingJie(owner) and qd['autoJingJieQuestTo'] == owner.jingJie + 1:
            pass
        else:
            return False
    if qd.has_key('cmpReqApprenticeType'):
        if enableNewApprentice():
            flag = apprenticeTypeCheckEx(owner, qd.get('cmpReqApprenticeType', 0))
        else:
            flag = apprenticeTypeCheck(owner, qd.get('cmpReqApprenticeType', 0))
        if not flag:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_ACCEPT_APPRENTICE_FAIL, ())
            return False
    if qd.has_key('cmpReqApprenticeVal'):
        if enableNewApprentice():
            flag = apprenticeValCheckEx(owner, qd.get('cmpReqApprenticeVal', 0))
        else:
            flag = False
        if not flag:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMP_APPRENTICE_VAL_FAIL, ())
            return False
    if qd.has_key('cmpReqCombatScore'):
        if owner.combatScoreList[const.COMBAT_SCORE] < qd['cmpReqCombatScore']:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMP_COMBAT_SCORE_FAIL, (qd['cmpReqCombatScore'] - owner.combatScoreList[const.COMBAT_SCORE],))
            return False
    validInBianyao = qd.get('validInBianyao', gametypes.FUNCTION_INVALID_FOR_YAO)
    if owner._isInBianyao() and validInBianyao == gametypes.FUNCTION_INVALID_FOR_YAO:
        return False
    elif not owner._isInBianyao() and validInBianyao == gametypes.FUNCTION_VALID_ONLY_FOR_YAO:
        return False
    elif not _completeQuestPlusCheck(owner, questId, bMsg, channel):
        return False
    if not enableQuestMaterialBag(owner, qd):
        if qd.has_key('compItemCollect'):
            isSucc = isQuestItemCollectComplete(owner, questId)
            if not isSucc and not orRelation:
                if bMsg:
                    gamelog.info('@szh: quest %d has compItemCollect limit' % questId)
                    if qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT) == const.QUEST_COMPCOND_EXACT:
                        channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_NOT_EQUAL_ITEM, ())
                    else:
                        channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LESS_ITEM, ())
                return False
            if isSucc and orRelation:
                return True
        elif qd.has_key('compItemCollectMulti'):
            isSucc = isQuestItemCollectCompleteMulti(owner, questId)
            if not isSucc and not orRelation:
                if bMsg:
                    gamelog.info('@syk: quest %d has compItemCollectMulti limit' % questId)
                    channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LESS_ITEM, ())
                return False
            if isSucc and orRelation:
                return True
    elif BigWorld.component in 'client':
        isSucc = owner.isQuestMaterialItemCollectComplete(questId)
        if not isSucc and not orRelation:
            if bMsg:
                gamelog.info('@PGF: quest %d has compMaterialItemCollectAndConsume limit' % questId)
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LESS_ITEM, ())
            return False
        if isSucc and orRelation:
            return True
    if qd.has_key('comSmtItem'):
        isSucc = isQuestItemSubmitComplete(owner, questId)
        if not isSucc and not orRelation:
            return False
        if isSucc and orRelation:
            return True
    if qd.has_key('randomItemCommit'):
        isSuc = isQuestRandomItemCommitComplete(owner, questId)
        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('randomItemCommitEx'):
        if BigWorld.component in 'client':
            isSuc = owner.isQuestRandomItemCommitExComplete(questId)
            if not isSuc and not orRelation:
                return False
            if isSuc and orRelation:
                return True
    if qd.has_key('randomItemCommitMulti'):
        isSuc = isQuestRandomItemCommitMultiComplete(owner, questId)
        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.get('isCross') and not qd.get('isBodyCom') and not owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SOUL_NOT_CROSS, ())
        return False
    elif not qd.get('isCross') and owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SOUL_CROSS, ())
        return False
    if qd.has_key('comBuff'):
        if qd['comBuff'] not in owner.statesServerAndOwn:
            if not orRelation:
                if bMsg and qd.has_key('comBuffMsg'):
                    channel.showGameMsg(GMDD.data.QUEST_COMP_NEED_STATE, (qd['comBuffMsg'],))
                return False
        elif orRelation:
            return True
    if qd.has_key('comBuffEx'):
        comStateIds = qd['comBuffEx']
        if comStateIds[0] == 0:
            isMatched = True
            for comStateId in comStateIds[1:]:
                if BigWorld.component == 'client':
                    if comStateId not in owner.statesServerAndOwn and not owner._checkTempStateIdInQuestData(questId, comStateId):
                        isMatched = False
                        break
                elif comStateId not in owner.statesServerAndOwn:
                    isMatched = False
                    break

        elif comStateIds[0] == 1:
            isMatched = False
            for comStateId in comStateIds[1:]:
                if BigWorld.component == 'client':
                    if comStateId in owner.statesServerAndOwn or owner._checkTempStateIdInQuestData(questId, comStateId):
                        isMatched = True
                        break
                elif comStateId in owner.statesServerAndOwn:
                    isMatched = True
                    break

        if not isMatched:
            if not orRelation:
                if bMsg and qd.has_key('comBuffExMsg'):
                    channel.showGameMsg(GMDD.data.QUEST_COMP_NEED_STATE, (qd['comBuffExMsg'],))
                return False
        elif orRelation:
            return True
    if qd.has_key('needMonsters') or qd.has_key('needMonstersGroup'):
        isSucc = isQuestMonsterKillComplete(owner, questId)
        if not isSucc and not orRelation:
            return False
        if isSucc and orRelation:
            return True
    if qd.has_key('fishingScore'):
        score = owner.getQuestData(questId, const.QD_FISHING_SCORE, -1)
        if score == -1 or score < qd['fishingScore']:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('beatMonsterNo'):
        beatMonsterNo = qd['beatMonsterNo']
        if beatMonsterNo > 0:
            bmd = owner.getQuestData(questId, const.QD_MONSTER_BEAT)
            if not bmd.get('done', False):
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('needDialog') or qd.has_key('needDialogGroup'):
        npcs = owner.getQuestData(questId, const.QD_QUEST_CHAT, {})
        for npcId, count in npcs.iteritems():
            if count == 0:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('markerNpcs') or qd.has_key('markerNpcsGroup'):
        if not owner.hasQuestData(questId, const.QD_QUEST_MARKER):
            channel.completeQuest(questId, False)
            return False
        if not qd.get('triggerPartial', 0):
            markerInfo, _ = owner.getQuestData(questId, const.QD_QUEST_MARKER)
            for count in markerInfo.values():
                if count == 0:
                    if not orRelation:
                        return False
                elif orRelation:
                    return True

        else:
            markerInfo, _ = owner.getQuestData(questId, const.QD_QUEST_MARKER)
            if sum(markerInfo.values()) == 0:
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('questInteractive'):
        if not owner.hasQuestData(questId, const.QD_QUEST_INTERACTIVE):
            channel.completeQuest(questId, False)
            return False
        questInteractiveInfo = owner.getQuestData(questId, const.QD_QUEST_INTERACTIVE)
        if sum(questInteractiveInfo.values()) != 0:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('debateChatId'):
        flag = owner.getQuestData(questId, const.QD_QUEST_DEBATE)
        if flag is not True:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('puzzleId') and owner.hasQuestData(questId, const.QD_PUZZLE):
        puzzleType = qd.get('puzzleType', const.PUZZLE_ANSWER_RIGHT)
        puzzleInfo = owner.getQuestData(questId, const.QD_PUZZLE)
        puzzleMode = qd.get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE)
        if puzzleMode == gametypes.PUZZLE_MODE_SINGLE:
            answer = puzzleInfo.values()[0]
            if not (puzzleType == const.PUZZLE_ANSWER_RIGHT and answer == const.PUZZLE_RIGHE) and not (puzzleType == const.PUZZLE_ANSWER_ANY and answer != const.PUZZLE_EMPTY):
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif puzzleMode in gametypes.PUZZLE_MODE_RIGHT_CONTINUE:
            complete = True
            for answer in puzzleInfo.values():
                if answer != const.PUZZLE_RIGHE:
                    complete = False
                    break

            if not complete:
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif puzzleMode in gametypes.PUZZLE_MODE_FALSE_CONTINUE:
            complete = True
            for answer in puzzleInfo.values():
                if answer == const.PUZZLE_EMPTY:
                    complete = False
                    break

            if not complete:
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('kingRoad'):
        if not owner.getQuestData(questId, const.QD_KING_ROAD):
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('arenaWin'):
        cnt = owner.getQuestData(questId, const.QD_ARENA_WIN)
        if cnt < qd['arenaWin']:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('questEquip'):
        questEquipReq = qd['questEquip']
        questEquip = owner.getQuestData(questId, const.QD_EQUIPMENT)
        for itemId in questEquipReq:
            if itemId not in questEquip:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('timeRemain'):
        qstTimeRemain = qd['timeRemain']
        questBeginTime = owner.getQuestData(questId, const.QD_TIME_REMAIN, current)
        if current < questBeginTime + qstTimeRemain:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('needConvoy'):
        convoyCharType = owner.getQuestData(questId, const.QD_CONVOY, 0)
        if convoyCharType != qd['needConvoy']:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('pvpKill'):
        pvpKillInfo = owner.getQuestData(questId, const.QD_PVP_KILL, {})
        for camp, cnt in qd['pvpKill'].iteritems():
            if not pvpKillInfo.has_key(camp) or pvpKillInfo[camp] < cnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('questVars'):
        for var, cnt in qd['questVars']:
            if owner.questVars.get(var, 0) < cnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('questAchieve'):
        achieveIds = qd['questAchieve']
        questAchieveInfo = owner.getQuestData(questId, const.QD_ACHIEVE, {})
        if not isinstance(achieveIds, tuple):
            achieveIds = tuple([achieveIds])
        for achieveId in achieveIds:
            if not questAchieveInfo.get(achieveId, False):
                if not orRelation:
                    return False
                break
        else:
            if orRelation:
                return True

    if qd.has_key('questAchieveOr'):
        achieveIds = qd['questAchieveOr']
        questAchieveInfo = owner.getQuestData(questId, const.QD_ACHIEVE, {})
        for achieveId in achieveIds:
            if questAchieveInfo.get(achieveId, False):
                if orRelation:
                    return True
                break
        else:
            if not orRelation:
                return False

    if qd.has_key('needJobScore'):
        jobScoreVar = qd.get('jobScoreVar', 'jobScoreVar%d' % questId)
        jobScore = owner.questVars.get(jobScoreVar, 0)
        if not any([ jobScore >= minScore for minScore in qd['needJobScore'] ]):
            return False
        if orRelation:
            return True
    if qd.has_key('needLifeSkillCollection'):
        collectionData = owner.getQuestData(questId, const.QD_QUEST_LIFESKILL_COLLECTION, {})
        for itemId, itemCnt in qd['needLifeSkillCollection']:
            if collectionData.get(itemId, 0) < itemCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('needLifeSkillManufacture'):
        manufacturerData = owner.getQuestData(questId, const.QD_QUEST_LIFESKILL_MANUFACTURE, {})
        for itemId, itemCnt in qd['needLifeSkillManufacture']:
            if manufacturerData.get(itemId, 0) < itemCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True

    if qd.has_key('jingJieLimit'):
        jingJie = qd['jingJieLimit']
        if owner.jingJie < jingJie:
            if not orRelation:
                if bMsg:
                    channel.showGameMsg(GMDD.data.QUEST_COMP_JINGJIE_FAIL, (jingJie - owner.jingJie,))
                return False
        elif orRelation:
            return True
    if qd.has_key('skillEnhancePoint'):
        skillPoints = qd['skillEnhancePoint']
        if utils.getTotalSkillEnhancePoint(owner) < skillPoints:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('needSkillEnhance'):
        skillEnhanceInfo = qd['needSkillEnhance']
        for partLv, cnt in skillEnhanceInfo:
            if utils.getSkillEnhanceCntByPart(owner, partLv) < cnt:
                if not orRelation:
                    return False
        else:
            if orRelation:
                return True

    if qd.has_key('needSkillEnhancePartOr'):
        skillEnhancePartInfo = qd['needSkillEnhancePartOr']
        isSuc = False
        for skillId, part in skillEnhancePartInfo:
            if utils.isSkillEnhanced(owner, skillId, part):
                isSuc = True
                break

        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needSkillEnhancePartAnd'):
        skillEnhancePartInfo = qd['needSkillEnhancePartAnd']
        isSuc = True
        for skillId, part in skillEnhancePartInfo:
            if not utils.isSkillEnhanced(owner, skillId, part):
                isSuc = False
                break

        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needDaoheng'):
        isSuc = False
        if BigWorld.component in 'cell':
            for sVal in owner.wsSkills.itervalues():
                if sVal.daoHeng.sumDaoHeng() > 0 or len(sVal.slots) > 0:
                    isSuc = True
                    break

        elif BigWorld.component in 'client':
            for sVal in owner.wsSkills.itervalues():
                if hasattr(sVal, 'daoHeng') and (sum(sVal.daoHeng.values()) > 0 or len(sVal.slots) > 0):
                    isSuc = True
                    break

        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needShenli'):
        shenliCnt = qd['needShenli']
        isSuc = False
        if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableHierogramOrRune', False) or BigWorld.component != 'client' and not gameconfig.enableHierogramOrRune():
            isSuc = False
        elif BigWorld.component == 'client' and gameglobal.rds.configData.get('enableHierogram', False) or BigWorld.component != 'client' and gameconfig.enableHierogram():
            isSuc = hasattr(owner, 'hierogram') and len(owner.hierogram.hieroArousePSkillsByEID) >= shenliCnt
        else:
            isSuc = hasattr(owner, 'runeBoard') and len(owner.runeBoard.pskillSet) >= shenliCnt
        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needShenliPartOr'):
        shenliInfo = qd['needShenliPartOr']
        isSuc = False
        if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableHierogramOrRune', False) or BigWorld.component != 'client' and not gameconfig.enableHierogramOrRune():
            isSuc = False
        elif BigWorld.component == 'client' and gameglobal.rds.configData.get('enableHierogram', False) or BigWorld.component != 'client' and gameconfig.enableHierogram():
            for shenliId in shenliInfo:
                if hasattr(owner, 'hierogram') and shenliId in owner.hierogram.hieroArousePSkillsByEID:
                    isSuc = True
                    break

        else:
            for shenliId in shenliInfo:
                if hasattr(owner, 'runeBoard') and shenliId in owner.runeBoard.pskillSet:
                    isSuc = True
                    break

        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needShenliPartAnd'):
        shenliInfo = qd['needShenliPartAnd']
        isSuc = True
        if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableHierogramOrRune', False) or BigWorld.component != 'client' and not gameconfig.enableHierogramOrRune():
            isSuc = False
        elif BigWorld.component == 'client' and gameglobal.rds.configData.get('enableHierogram', False) or BigWorld.component != 'client' and gameconfig.enableHierogram():
            for shenliId in shenliInfo:
                if hasattr(owner, 'hierogram') and shenliId not in owner.hierogram.hieroArousePSkillsByEID:
                    isSuc = False
                    break

        else:
            for shenliId in shenliInfo:
                if hasattr(owner, 'runeBoard') and shenliId not in owner.runeBoard.pskillSet:
                    isSuc = False
                    break

        if not isSuc and not orRelation:
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('needRuneEquipLv'):
        runeEquipLv, runeEquipCnt = qd['needRuneEquipLv']
        if getRuneLvLarger(owner, runeEquipLv) < runeEquipCnt:
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('businessLv'):
        businessLv = qd['businessLv']
        blcd = BLCD.data[businessLv]
        fameId = BCD.data['businessFameId']
        maxFame = blcd['maxFame']
        if BigWorld.component == 'cell':
            if not owner.guildNUID or maxFame > owner.fame.getFame(fameId, owner.school):
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            if not owner.guildNUID or maxFame > owner.fame.get(fameId, 0):
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('comTeamCnt'):
        teamCnt = qd['comTeamCnt']
        if BigWorld.component == 'cell':
            if len(owner.team) != teamCnt:
                if not orRelation:
                    if qd.get('isShowIgnoreTeamCnt', 0):
                        channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_TEAM_CNT, (teamCnt,))
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            cnt = len([ x for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ])
            if cnt != teamCnt:
                if not orRelation:
                    if not qd.get('isShowIgnoreTeamCnt', 0):
                        return False
            elif orRelation:
                return True
    if qd.has_key('comTeamCntLarger'):
        teamCnt = qd['comTeamCntLarger']
        if BigWorld.component == 'cell':
            if len(owner.team) <= teamCnt:
                if not orRelation:
                    if qd.get('isShowIgnoreTeamCnt', 0):
                        channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_MORE_THAN_TEAM_CNT, (teamCnt,))
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            cnt = len([ x for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ])
            if cnt <= teamCnt:
                if not orRelation:
                    if not qd.get('isShowIgnoreTeamCnt', 0):
                        return False
            elif orRelation:
                return True
    if qd.has_key('comTeamCntLess'):
        teamCnt = qd['comTeamCntLess']
        if BigWorld.component == 'cell':
            if len(owner.team) >= teamCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            cnt = len([ x for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ])
            if cnt >= teamCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('comBoyCnt'):
        boyCnt = qd['comBoyCnt']
        if BigWorld.component == 'cell':
            curBoyCnt = len([ x for x in owner.team.values() if x.sex == 1 ])
            if curBoyCnt != boyCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            members = [ owner.members[x] for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ]
            curBoyCnt = len([ x for x in members if x['sex'] == 1 ])
            if curBoyCnt != boyCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('comGirlCnt'):
        girlCnt = qd['comGirlCnt']
        if BigWorld.component == 'cell':
            curGirlCnt = len([ x for x in owner.team.values() if x.sex == 2 ])
            if curGirlCnt != girlCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
        elif BigWorld.component == 'client':
            members = [ owner.members[x] for x in owner.members.keys() if groupUtils.isInSameTeam(x, owner.gbId) ]
            curGirlCnt = len([ x for x in members if x['sex'] == 2 ])
            if curGirlCnt != girlCnt:
                if not orRelation:
                    return False
            elif orRelation:
                return True
    if qd.has_key('comStatesCheck'):
        states = qd['comStatesCheck']
        for stateName in states:
            if BigWorld.component == 'cell':
                if not getattr(owner, '_check_' + stateName)():
                    if not orRelation:
                        return False
                elif orRelation:
                    return True
            elif BigWorld.component == 'client':
                if not getattr(owner.stateMachine, '_check' + stateName)():
                    if not orRelation:
                        return False
                elif orRelation:
                    return True

    if qd.has_key('fireworkVar'):
        if not owner.getQuestData(questId, const.QD_FIREWORK, False):
            if not orRelation:
                return False
        elif orRelation:
            return True
    if qd.has_key('needAllMembers') and owner.groupHeader == owner.id:
        isSuc = True
        if not owner.groupNUID:
            isSuc = False
        else:
            dist = SCD.data.get('teamAroundDist', 30)
            if BigWorld.component == 'cell':
                for _gbId, mVal in owner.team.iteritems():
                    if _gbId == owner.gbId:
                        continue
                    if not mVal.isOn or not mVal.box:
                        isSuc = False
                        break
                    memberEntity = BigWorld.entities.get(mVal.box.id)
                    if not memberEntity or distance3D(owner.position, memberEntity.position) > dist or memberEntity.life == gametypes.LIFE_DEAD:
                        isSuc = False
                        break

            elif BigWorld.component == 'client':
                for _gbId, mVal in owner.members.iteritems():
                    if _gbId == owner.gbId:
                        continue
                    if not mVal['isOn'] or not mVal['id']:
                        isSuc = False
                        break
                    memberEntity = BigWorld.entities.get(mVal['id'])
                    if not memberEntity or distance3D(owner.position, memberEntity.position) > dist or memberEntity.life == gametypes.LIFE_DEAD:
                        isSuc = False
                        break

        if not isSuc and not orRelation:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_TEAM_NOT_ALL_AROUND, ())
            return False
        if isSuc and orRelation:
            return True
    if qd.has_key('comTeamOnly') and BigWorld.component == 'cell':
        if owner.groupType != gametypes.GROUP_TYPE_TEAM_GROUP:
            if not orRelation:
                bMsg and channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_TEAM_ONLY, ())
                return False
            if orRelation:
                return True
    if orRelation:
        return False
    else:
        return True


def completeQuestExtraCheck(owner, questId, bMsg = False):
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if questId not in owner.quests:
        return False
    if not QED.data.has_key(questId):
        return False
    qed = QED.data[questId]
    qd = QD.data[questId]
    if qed is None or isQuestDisable(questId):
        if bMsg:
            gamelog.info('@szh: quest extra %d has been disable' % questId)
        return False
    if owner.getQuestFlag(questId):
        return False
    if owner.getQuestData(questId, const.QD_EXTRA_FAIL):
        if bMsg:
            gamelog.info('@szh: quest extra %d has failed' % questId)
        return False
    if qed.has_key('timeLimit'):
        limit = owner.getQuestData(questId, const.QD_BEGIN_TIME, default=0) + qed['timeLimit']
        if limit < current:
            if bMsg:
                gamelog.info('@szh: quest %d has time limit' % questId)
                channel.showGameMsg(GMDD.data.QUEST_FAILED_TIMEOUT, (qd['name'],))
            return False
    if qed.has_key('needMonsters'):
        kms = owner.getQuestData(questId, const.QD_EXTRA_MONSTER_KILL)
        if kms is None:
            return False
        for no, num in qed['needMonsters']:
            if kms.get(no, 0) < num:
                if bMsg:
                    gamelog.info('@szh: quest %d has monster limit' % questId)
                return False

    if qed.has_key('beatMonsterNo'):
        beatMonsterNo = qed['beatMonsterNo']
        if beatMonsterNo > 0:
            bmd = owner.getQuestData(questId, const.QD_EXTRA_MONSTER_BEAT)
            if not bmd.get('done', False):
                if bMsg:
                    gamelog.info('@szh: quest %d has beatMonsterNo limit' % questId)
                return False
    if qed.has_key('compItemCollect'):
        tmpQuestItems = {}
        tmpCommonItems = {}
        for itemId, many in qed['compItemCollect']:
            if Item.isQuestItem(itemId):
                tmpQuestItems[itemId] = many
            else:
                tmpCommonItems[itemId] = many

        if not owner.questBag.canRemoveItems(tmpQuestItems) or not owner.realInv.canRemoveItems(tmpCommonItems):
            if bMsg:
                gamelog.info('@szh: quest %d has compItemCollect limit' % questId)
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LESS_ITEM, ())
            return False
    elif qed.has_key('compItemCollectMulti'):
        if not isQuestItemCollectCompleteMulti(owner, questId):
            if bMsg:
                gamelog.info('@syk: quest %d has compItemCollectMulti limit' % questId)
                channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_LESS_ITEM, ())
            return False
    if qed.has_key('pvpKill'):
        pvpKillInfo = owner.getQuestData(questId, const.QD_EXTRA_PVP_KILL, {})
        for camp, cnt in qed['pvpKill'].iteritems():
            if not pvpKillInfo.has_key(camp) or pvpKillInfo[camp] < cnt:
                if bMsg:
                    gamelog.info('@szh: quest %d has pvpKill limit' % questId)
                return False

    if qed.has_key('comBuff'):
        if qed['comBuff'] not in owner.statesServerAndOwn:
            if bMsg:
                gamelog.info('@szh: quest %d has combuff limit' % questId)
            return False
    if qed.has_key('comBuffEx'):
        comStateIds = qed.get('comBuffEx', ())
        if comStateIds[0] == 0:
            isMatched = True
            for comStateId in comStateIds[1:]:
                if comStateId not in owner.statesServerAndOwn:
                    isMatched = False
                    break

        elif comStateIds[0] == 1:
            isMatched = False
            for comStateId in comStateIds[1:]:
                if comStateId in owner.statesServerAndOwn:
                    isMatched = True
                    break

        if not isMatched:
            if bMsg:
                gamelog.info('@szh: quest has combuff limit ', comStateIds)
            return False
    if qed.has_key('questVars'):
        for var, cnt in qed['questVars']:
            if owner.questVars.get(var, 0) < cnt:
                if bMsg:
                    gamelog.info('@szh: quest %d has extra questVars limit' % questId)
                return False

    if qed.has_key('needApprentice'):
        if enableNewApprentice():
            flag = apprenticeTeamCheckEx(owner)
        else:
            flag = apprenticeTeamCheck(owner)
        if not flag:
            if bMsg:
                gamelog.info('@szh: needApprentice relation limit' % questId)
            return False
    return True


def enableNewApprentice():
    if BigWorld.component in 'cell':
        return gameconfig.enableNewApprentice()
    if BigWorld.component in 'client':
        return gameglobal.rds.configData.get('enableNewApprentice', False)
    return False


def apprenticeGraduateCheck(owner):
    if BigWorld.component in 'cell':
        if owner.apprentice.graduate:
            return True
    elif BigWorld.component in 'client':
        if owner.apprenticeGraduateFlag:
            return True
    return False


def apprenticeGraduateCheckEx(owner):
    if BigWorld.component in 'cell':
        if owner.graduateMentorListEx:
            return True
    elif BigWorld.component in 'client':
        if owner.checkGraduateTeamMentorEx():
            return True
    return False


def apprenticeTypeCheck(owner, apprenticeType):
    flag = False
    if apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_MENTOR:
        if BigWorld.component in 'cell':
            if len(owner.apprentice) > 0:
                flag = True
        elif BigWorld.component in 'client':
            if owner.apprenticeGbIds:
                for _, graduate in owner.apprenticeGbIds:
                    if not graduate:
                        flag = True
                        break

    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_APPRENTICE:
        if BigWorld.component in 'cell':
            if owner.apprentice.mentorGbId and not owner.apprentice.graduate:
                flag = True
        elif BigWorld.component in 'client':
            if owner.mentorGbId and not owner.apprenticeGraduateFlag:
                flag = True
    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_MENTOR_OR_APPRENTICE:
        if BigWorld.component in 'cell':
            if owner.apprentice.mentorGbId and not owner.apprentice.graduate or len(owner.apprentice) > 0:
                flag = True
        elif BigWorld.component in 'client':
            if owner.mentorGbId and not owner.apprenticeGraduateFlag:
                flag = True
            if not flag and owner.apprenticeGbIds:
                for _, graduate in owner.apprenticeGbIds:
                    if not graduate:
                        flag = True
                        break

    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_TEAM:
        flag = apprenticeTeamCheck(owner)
    return flag


def apprenticeTeamCheck(owner):
    flag = False
    if BigWorld.component in 'cell':
        for gbId in owner.team.keys():
            tgt = None
            if gbId == owner.apprentice.mentorGbId and owner.apprentice.mentorBox and not owner.apprentice.graduate:
                tgt = BigWorld.entities.get(owner.apprentice.mentorBox.id)
            elif gbId in owner.apprentice and not owner.apprentice[gbId].graduate and owner.apprentice[gbId].box:
                tgt = BigWorld.entities.get(owner.apprentice[gbId].box.id)
            if tgt and distance3D(owner.position, tgt.position) <= 80:
                flag = True
                break

    elif BigWorld.component in 'client':
        if owner.mentorGbId and owner.mentorGbId in owner.members and not owner.apprenticeGraduateFlag:
            tgt = BigWorld.entities.get(owner.members[owner.mentorGbId].get('id', 0))
            if tgt and distance3D(owner.position, tgt.position) <= 80:
                flag = True
        else:
            for gbId, graduate in owner.apprenticeGbIds:
                if not graduate and gbId in owner.members:
                    tgt = BigWorld.entities.get(owner.members[gbId].get('id', 0))
                    if tgt and distance3D(owner.position, tgt.position) <= 80:
                        flag = True
                        break

    return flag


def apprenticeValCheckEx(owner, apprenticeVal):
    flag = False
    if BigWorld.component in 'cell':
        if owner.maxMentorVal >= apprenticeVal:
            flag = True
    elif BigWorld.component in 'client':
        if owner.getMaxMentorApprenticeValEx() >= apprenticeVal:
            flag = True
    return flag


def apprenticeTypeCheckEx(owner, apprenticeType):
    flag = False
    if apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_MENTOR:
        if BigWorld.component in 'cell':
            if len(owner.apprenticeListEx) > 0:
                flag = True
        elif BigWorld.component in 'client':
            if owner.apprenticeGbIds:
                for _, graduate in owner.apprenticeGbIds:
                    if not graduate:
                        flag = True
                        break

    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_APPRENTICE:
        if BigWorld.component in 'cell':
            if owner.mentorListEx:
                flag = True
        elif BigWorld.component in 'client':
            if owner.apprenticeInfo and any([ not ent.get('graduate', 0) for ent in owner.apprenticeInfo.values() ]):
                flag = True
    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_MENTOR_OR_APPRENTICE:
        if BigWorld.component in 'cell':
            if owner.mentorListEx or owner.apprenticeListEx:
                flag = True
        elif BigWorld.component in 'client':
            if owner.apprenticeInfo and any([ not ent.get('graduate', 0) for ent in owner.apprenticeInfo.values() ]):
                flag = True
            if not flag and owner.apprenticeGbIds:
                for _, graduate in owner.apprenticeGbIds:
                    if not graduate:
                        flag = True
                        break

    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_TEAM:
        flag = apprenticeTeamCheckEx(owner)
    elif apprenticeType == gametypes.APPRENTICE_QUEST_TYPE_APPRENTICE_NOT_GRADUATE_EVER:
        if BigWorld.component in 'cell':
            if owner.tGraduateEx == 0 and owner.mentorListEx:
                flag = True
        elif BigWorld.component in 'client':
            if owner.tGraduateEx == 0 and owner.apprenticeInfo:
                flag = True
    return flag


def apprenticeTeamCheckEx(owner):
    flag = False
    if BigWorld.component in 'cell':
        for gbId in owner.team.keys():
            if not owner.team[gbId].box:
                continue
            tgt = None
            if gbId in owner.apprenticeListEx or gbId in owner.mentorListEx:
                tgt = BigWorld.entities.get(owner.team[gbId].box.id)
            if tgt and distance3D(owner.position, tgt.position) <= 80:
                flag = True
                break

    elif BigWorld.component in 'client':
        if owner.checkUngraduateTeamMentorEx():
            flag = True
        else:
            for gbId, graduate in owner.apprenticeGbIds:
                if not graduate and gbId in owner.members:
                    tgt = BigWorld.entities.get(owner.members[gbId].get('id', 0))
                    if tgt and distance3D(owner.position, tgt.position) <= 80:
                        flag = True
                        break

    return flag


def completeQuestLoopSimpleCheck(owner, questLoopId, bMsg = False):
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if questLoopId not in owner.questLoopInfo:
        return False
    qld = QLD.data.get(questLoopId)
    if qld is None or isQuestLoopDisable(questLoopId):
        return False
    if not owner.checkWorldRefreshQuestLoop(questLoopId):
        return False
    if qld.has_key('comStartTimes') and qld.has_key('comEndTimes'):
        comtStartTime = qld['comStartTimes']
        comtEndTime = qld['comEndTimes']
        if True not in [ utils.inTimeTupleRange(comtStartTime[i], comtEndTime[i], current) for i in xrange(len(comtStartTime)) ]:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_LOOP_COMPTIME_INVALID, ())
            return False
    questLoop = owner.questLoopInfo[questLoopId]
    if not questLoop.completeQuestCheck():
        return False
    questId = questLoop.getCurrentQuest()
    if questId is None:
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if questId not in owner.quests:
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if owner.getQuestFlag(questId):
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if not completeQuestCheck(owner, questId, bMsg):
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    return True


def completeQuestLoopCheck(owner, questLoopId, bMsg = False):
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = BigWorld.player().getServerTime()
    if questLoopId not in owner.questLoopInfo:
        return False
    qld = QLD.data.get(questLoopId)
    if qld is None or isQuestLoopDisable(questLoopId):
        return False
    if not owner.checkWorldRefreshQuestLoop(questLoopId):
        return False
    if qld.has_key('weekSet'):
        weekSet = qld.get('weekSet', 0)
        if utils.isInvalidWeek(weekSet):
            bMsg and channel.showGameMsg(GMDD.data.QUEST_LOOP_COMPTIME_INVALID, ())
            return False
    if qld.has_key('comStartTimes') and qld.has_key('comEndTimes'):
        comtStartTime = qld['comStartTimes']
        comtEndTime = qld['comEndTimes']
        if True not in [ utils.inTimeTupleRange(comtStartTime[i], comtEndTime[i], current) for i in xrange(len(comtStartTime)) ]:
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_LOOP_COMPTIME_INVALID, ())
            return False
    if qld.has_key('comXingjiTimes'):
        comXingjiTimes = qld['comXingjiTimes']
        if not formula.isInXingJiTimeIntervals(comXingjiTimes):
            if bMsg:
                channel.showGameMsg(GMDD.data.QUEST_COMPLETE_XINGJITIME_INVALID, ())
                gamelog.info('@szh the acXingjiTimes fails! %d' % questLoopId)
            return False
    if qld.has_key('comWWStartLv'):
        if owner.getWorldWarQuestStarLv() != qld['comWWStartLv']:
            if bMsg:
                comWWStartLv = str(qld['comWWStartLv'])
                channel.showGameMsg(GMDD.data.QUEST_COMPLETE_FAIL_WORLD_WAR_LEVEL, (comWWStartLv,))
            return False
    if qld.get('isCross') and not qld.get('isBodyCom') and not owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SOUL_NOT_CROSS, ())
        return False
    if not qld.get('isCross') and owner._isSoul():
        if bMsg:
            channel.showGameMsg(GMDD.data.QUEST_COMP_FAIL_SOUL_CROSS, ())
        return False
    questLoop = owner.questLoopInfo[questLoopId]
    if not questLoop.completeQuestCheck():
        return False
    questId = questLoop.getCurrentQuest()
    if questId is None:
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if questId not in owner.quests:
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if QDID.data.has_key(questLoopId):
        dId = QDID.data[questLoopId]
        if owner.getDelegationData(dId, const.DD_FAIL):
            if bMsg:
                channel.completeQuest(questId, False)
            gamelog.debug('@szh the related delegation has failed', owner.id, dId, questLoopId)
            return False
        if owner.getDelegationData(dId, const.DD_STATUS) in (const.DS_TYPE_AGENTED, const.DS_TYPE_EMPLOY):
            if bMsg:
                channel.completeQuest(questId, False)
            gamelog.debug('@szh the related delegation has agented or employed', owner.id, dId, questLoopId)
            return False
    if owner.getQuestFlag(questId):
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    if not completeQuestCheck(owner, questId, bMsg):
        if bMsg:
            channel.completeQuest(questId, False)
        return False
    return True


def questFailCheck(owner, questId):
    if questId not in owner.quests:
        return False
    qd = QD.data.get(questId, {})
    if qd.has_key('timeLimit'):
        limit = owner.getQuestData(questId, const.QD_BEGIN_TIME, 0) + qd['timeLimit']
        if BigWorld.component in 'cell':
            current = time.time()
        elif BigWorld.component in 'client':
            current = BigWorld.player().getServerTime()
        if limit < current:
            return True
    if owner.getQuestData(questId, const.QD_FAIL):
        return True
    return False


def extraCheckAvailableTask(channel, questId, isQuestLoop):
    if isQuestLoop:
        qd = QLD.data.get(questId, {})
    else:
        qd = QD.data.get(questId, {})
    if BigWorld.component in 'client':
        if qd.has_key('acIntimacyMinLv'):
            if len(channel.members) < 2:
                return False
            intimacyLv = qd['acIntimacyMinLv']
            for _gbId, mVal in channel.members.iteritems():
                if _gbId != channel.gbId:
                    friend = channel.friend.get(_gbId, {})
                    if not friend or not friend.acknowledge:
                        continue
                    if qd.get('acNeedFullIntimacy', 0):
                        maxVal = IMD.data.get(friend.intimacyLv, {}).get('maxVal', const.MAX_INTIMACY_VALUE)
                        if maxVal != friend.intimacy:
                            continue
                    if friend.intimacyLv < intimacyLv:
                        continue
                    break
            else:
                return False

        if qd.has_key('acIntimacyMaxLv'):
            if len(channel.members) < 2:
                return False
            intimacyLv = qd['acIntimacyMaxLv']
            for _gbId, mVal in channel.members.iteritems():
                if _gbId != channel.gbId:
                    friend = channel.friend.get(_gbId, {})
                    if not friend or not friend.acknowledge:
                        continue
                    if qd.get('acNeedFullIntimacy', 0):
                        maxVal = IMD.data.get(friend.intimacyLv, {}).get('maxVal', const.MAX_INTIMACY_VALUE)
                        if maxVal != friend.intimacy:
                            continue
                    if friend.intimacyLv > intimacyLv:
                        continue
                    break
            else:
                return False

    elif BigWorld.component in 'cell':
        if qd.has_key('acIntimacyMinLv'):
            if len(channel.team) < 2:
                return False
            intimacyLv = qd['acIntimacyMinLv']
            for _gbId, mVal in channel.team.iteritems():
                if _gbId != channel.gbId:
                    if not mVal.pally:
                        continue
                    if qd.get('acNeedFullIntimacy', 0):
                        if not mVal.isFullIntimacy:
                            continue
                    if mVal.intimacyLv < intimacyLv:
                        continue
                    break
            else:
                return False

        if qd.has_key('acIntimacyMaxLv'):
            if len(channel.team) < 2:
                return False
            intimacyLv = qd['acIntimacyMaxLv']
            for _gbId, mVal in channel.team.iteritems():
                if _gbId != channel.gbId:
                    if not mVal.pally:
                        continue
                    if qd.get('acNeedFullIntimacy', 0):
                        if not mVal.isFullIntimacy:
                            continue
                    if mVal.intimacyLv > intimacyLv:
                        continue
                    break
            else:
                return False

    return True


def getQuestInfo(owner, acQuests, comQuests, acQuestLoops = {}, comQuestLoops = {}, npcNo = None):
    if not isinstance(acQuests, tuple) and not isinstance(acQuests, list):
        acQuests = tuple([acQuests])
    if not isinstance(comQuests, tuple) and not isinstance(comQuests, list):
        comQuests = tuple([comQuests])
    questInfo = {'available_tasks': [],
     'unfinished_tasks': [],
     'complete_tasks': [],
     'complete_extra_tasks': [],
     'available_taskLoops': [],
     'unfinished_taskLoops': [],
     'complete_taskLoops': [],
     'complete_extra_taskLoops': []}
    for acQuest in acQuests:
        qd = QD.data.get(acQuest, {})
        if isQuestDisable(acQuest):
            continue
        if qd.get('type') not in (gametypes.QUEST_TYPE_ZHUXIAN, gametypes.QUEST_TYPE_ZHIXIAN):
            continue
        if acQuest not in owner.quests and not owner.getQuestFlag(acQuest) and gainQuestCheck(owner, acQuest, False):
            if extraCheckAvailableTask(owner, acQuest, 0) and not QD.data[acQuest].get('goldType', 0):
                questInfo['available_tasks'].append(acQuest)

    for comQuest in comQuests:
        qd = QD.data.get(comQuest, {})
        if isQuestDisable(comQuest):
            continue
        if qd.get('type') != gametypes.QUEST_TYPE_ZHUXIAN and qd.get('type') != gametypes.QUEST_TYPE_ZHIXIAN:
            continue
        if comQuest in owner.quests:
            if npcNo and owner.getQuestData(comQuest, const.QD_COMPNPC, npcNo) != npcNo:
                continue
            if not completeQuestCheck(owner, comQuest, False):
                questInfo['unfinished_tasks'].append(comQuest)
            else:
                questInfo['complete_tasks'].append(comQuest)
                if completeQuestExtraCheck(owner, comQuest):
                    questInfo['complete_extra_tasks'].append(comQuest)

    for acQuestLoopId in acQuestLoops:
        if isQuestLoopDisable(acQuestLoopId):
            continue
        if gainQuestLoopCheck(owner, acQuestLoopId, False):
            if not extraCheckAvailableTask(owner, acQuestLoopId, 1):
                continue
            if acQuestLoopId in owner.questLoopInfo:
                avlQuestIds = owner.questLoopInfo[acQuestLoopId].getNextQuests(owner)
            else:
                avlQuestIds = getAvaiNextQuestsInLoop(owner, acQuestLoopId, 0)
            if len(acQuestLoops[acQuestLoopId]) > 0:
                avlQuestIds = [ x for x in avlQuestIds if x in acQuestLoops[acQuestLoopId] ]
            acQuests = []
            for questId in avlQuestIds:
                qd = QD.data[questId]
                if qd.get('acNpcType', gametypes.QUEST_ACNPC_RANDOM) == gametypes.QUEST_ACNPC_EXACT:
                    if owner.questLoopInfo.has_key(acQuestLoopId) and owner.questLoopInfo[acQuestLoopId].lastCompNpc == npcNo:
                        acQuests.append(questId)
                    elif not owner.questLoopInfo.has_key(acQuestLoopId):
                        acQuests.append(questId)
                else:
                    acQuests.append(questId)

            if len(acQuests) > 0:
                questInfo['available_taskLoops'].append(acQuestLoopId)

    for comQuestLoopId in comQuestLoops:
        if isQuestLoopDisable(comQuestLoopId):
            continue
        if comQuestLoopId in owner.questLoopInfo:
            if not completeQuestLoopCheck(owner, comQuestLoopId, False):
                comQuestId = owner.questLoopInfo[comQuestLoopId].getCurrentQuest()
                if npcNo and owner.getQuestData(comQuestId, const.QD_COMPNPC, npcNo) != npcNo:
                    continue
                if comQuestId is not None:
                    if len(comQuestLoops[comQuestLoopId]) == 0 or comQuestId in comQuestLoops[comQuestLoopId]:
                        questInfo['unfinished_taskLoops'].append(comQuestLoopId)

    for comQuestLoopId in comQuestLoops:
        if isQuestLoopDisable(comQuestLoopId):
            continue
        if comQuestLoopId in owner.questLoopInfo:
            if completeQuestLoopCheck(owner, comQuestLoopId, False):
                comQuestId = owner.questLoopInfo[comQuestLoopId].getCurrentQuest()
                if npcNo and owner.getQuestData(comQuestId, const.QD_COMPNPC, npcNo) != npcNo:
                    continue
                if comQuestId is not None:
                    if len(comQuestLoops[comQuestLoopId]) == 0 or comQuestId in comQuestLoops[comQuestLoopId]:
                        questInfo['complete_taskLoops'].append(comQuestLoopId)
                        if completeQuestExtraCheck(owner, comQuestId):
                            questInfo['complete_extra_taskLoops'].append(comQuestLoopId)

    return questInfo


def hasAcceptQuests(owner, acQuests, npcNo = None):
    if not isinstance(acQuests, tuple) and not isinstance(acQuests, list):
        acQuests = tuple([acQuests])
    for acQuest in acQuests:
        qd = QD.data.get(acQuest, {})
        if isQuestDisable(acQuest):
            continue
        if qd.get('type') not in (gametypes.QUEST_TYPE_ZHUXIAN, gametypes.QUEST_TYPE_ZHIXIAN):
            continue
        if acQuest not in owner.quests and not owner.getQuestFlag(acQuest) and gainQuestCheck(owner, acQuest, False):
            if extraCheckAvailableTask(owner, acQuest, 0):
                return True

    return False


def hasCompleteQuests(owner, comQuests, npcNo = None):
    if not isinstance(comQuests, tuple) and not isinstance(comQuests, list):
        comQuests = tuple([comQuests])
    for comQuest in comQuests:
        qd = QD.data.get(comQuest, {})
        if isQuestDisable(comQuest):
            continue
        if qd.get('type') != gametypes.QUEST_TYPE_ZHUXIAN and qd.get('type') != gametypes.QUEST_TYPE_ZHIXIAN:
            continue
        if comQuest in owner.quests:
            if npcNo and owner.getQuestData(comQuest, const.QD_COMPNPC, npcNo) != npcNo:
                continue
            if completeQuestCheck(owner, comQuest, False):
                return True

    return False


def hasUncompleteQuests(owner, comQuests, npcNo = None):
    if not isinstance(comQuests, tuple) and not isinstance(comQuests, list):
        comQuests = tuple([comQuests])
    for comQuest in comQuests:
        qd = QD.data.get(comQuest, {})
        if isQuestDisable(comQuest):
            continue
        if qd.get('type') != gametypes.QUEST_TYPE_ZHUXIAN and qd.get('type') != gametypes.QUEST_TYPE_ZHIXIAN:
            continue
        if comQuest in owner.quests:
            if npcNo and owner.getQuestData(comQuest, const.QD_COMPNPC, npcNo) != npcNo:
                continue
            if not completeQuestCheck(owner, comQuest, False):
                return True

    return False


def hasAcceptQuestLoops(owner, acQuestLoops = {}, npcNo = None):
    for acQuestLoopId in acQuestLoops:
        if isQuestLoopDisable(acQuestLoopId):
            continue
        if gainQuestLoopCheck(owner, acQuestLoopId, False):
            if not extraCheckAvailableTask(owner, acQuestLoopId, 1):
                continue
            if acQuestLoopId in owner.questLoopInfo:
                avlQuestIds = owner.questLoopInfo[acQuestLoopId].getNextQuests(owner)
            else:
                avlQuestIds = getAvaiNextQuestsInLoop(owner, acQuestLoopId, 0)
            if len(acQuestLoops[acQuestLoopId]) > 0:
                avlQuestIds = [ x for x in avlQuestIds if x in acQuestLoops[acQuestLoopId] ]
            acQuests = []
            for questId in avlQuestIds:
                qd = QD.data[questId]
                if qd.get('acNpcType', gametypes.QUEST_ACNPC_RANDOM) == gametypes.QUEST_ACNPC_EXACT:
                    if owner.questLoopInfo.has_key(acQuestLoopId) and owner.questLoopInfo[acQuestLoopId].lastCompNpc == npcNo:
                        acQuests.append(questId)
                else:
                    acQuests.append(questId)

            if len(acQuests) > 0:
                return True

    return False


def hasCompleteQuestLoops(owner, comQuestLoops = {}, npcNo = None):
    for comQuestLoopId in comQuestLoops:
        if isQuestLoopDisable(comQuestLoopId):
            continue
        if comQuestLoopId in owner.questLoopInfo:
            if completeQuestLoopCheck(owner, comQuestLoopId, False):
                comQuestId = owner.questLoopInfo[comQuestLoopId].getCurrentQuest()
                if npcNo and owner.getQuestData(comQuestId, const.QD_COMPNPC, npcNo) != npcNo:
                    continue
                if comQuestId is not None:
                    if len(comQuestLoops[comQuestLoopId]) == 0 or comQuestId in comQuestLoops[comQuestLoopId]:
                        return True

    return False


def hasUnCompleteQuestLoops(owner, comQuestLoops = {}, npcNo = None):
    for comQuestLoopId in comQuestLoops:
        if isQuestLoopDisable(comQuestLoopId):
            continue
        if comQuestLoopId in owner.questLoopInfo:
            if not completeQuestLoopCheck(owner, comQuestLoopId, False):
                comQuestId = owner.questLoopInfo[comQuestLoopId].getCurrentQuest()
                if comQuestId is not None:
                    if len(comQuestLoops[comQuestLoopId]) == 0 or comQuestId in comQuestLoops[comQuestLoopId]:
                        return True

    return False


def getAvaiNextQuestsInLoop(owner, questLoopId, circleStep, bMsg = False):
    if not QLD.data.has_key(questLoopId):
        return []
    qld = QLD.data[questLoopId]
    questIds = []
    if isQuestLoopDisable(questLoopId):
        return []
    if qld['ranType'] == gametypes.QUEST_LOOP_SELECT_SEQUENCE:
        if circleStep >= len(qld['quests']):
            questId = 0
        else:
            questId = qld['quests'][circleStep]
        if gainQuestCheck(owner, questId, bMsg):
            questIds.append(questId)
    elif qld['ranType'] == gametypes.QUEST_LOOP_SELECT_RANDOM:
        avaiQuestIds = qld['quests']
        for questId in avaiQuestIds:
            if gainQuestCheck(owner, questId, bMsg):
                questIds.append(questId)

    elif qld['ranType'] == gametypes.QUEST_LOOP_SELECT_PARTRANDOM:
        if circleStep >= len(qld['quests']):
            avaiQuestIds = []
        else:
            avaiQuestIds = qld['quests'][circleStep]
        for questId in avaiQuestIds:
            if gainQuestCheck(owner, questId, bMsg):
                questIds.append(questId)

    elif qld['ranType'] in (gametypes.QUEST_LOOP_SELECT_GLOBAL_RANDOM, gametypes.QUEST_LOOP_SELECT_GLOBAL_PARTRANDOM, gametypes.QUEST_LOOP_SELECT_GLOBAL_LVRANDOM):
        if owner.globalQuestLoopSeq.has_key(questLoopId):
            if circleStep < len(owner.globalQuestLoopSeq[questLoopId]):
                questId = owner.globalQuestLoopSeq[questLoopId][circleStep]
                if gainQuestCheck(owner, questId, bMsg):
                    questIds.append(questId)
    return questIds


def _evaluateRewardData(reward, rewardData, locals = {}):
    func = rewardData.get(reward, '')
    if func:
        try:
            return func(locals)
        except:
            gamelog.error('_evaluateRewardData wrong!')
            return 0

    else:
        return 0


def calcReward(owner, questId, questLoopId = 0):
    return _calcReward(owner, 'reward', questId, questLoopId)


def calcPuzzleReward(owner, questId, questLoopId = 0):
    return _calcReward(owner, 'puzzleReward', questId, questLoopId)


def calcWAReward(owner, questId):
    return _calcReward(owner, 'reward', questId, 0, 1)


def calcRewardByProgress(owner, questId, questLoopId = 0, perfect = True):
    return _calcReward(owner, 'reward', questId, questLoopId, 0, perfect)


def _calcReward(owner, rewardKey, questId, questLoopId = 0, questType = 0, perfect = True):
    if questType == 0:
        qd = QD.data.get(questId, {})
    else:
        qd = WQD.data.get(questId, {})
    rewardMode = qd.get(rewardKey, None)
    if BigWorld.component in ('cell', 'base'):
        if gameconfig.enableExpToYuanshen():
            if qd.get('needExpToYuanshen', 0) and serverProgress.getProgressStatus(SPPPD.data.EXP_TO_YUANSHEN):
                rewardMode = qd.get('yuanshenReward', None)
    if rewardMode == None:
        return (0, 0, 0, 0)
    rewardData = QRD.data.get(rewardMode, None)
    if rewardData == None:
        return (0, 0, 0, 0)
    lv = owner.getQuestLv(questId, qd)
    if owner.hasQuestData(questId, const.QD_QUEST_SOCLV):
        socLv = owner.getQuestData(questId, const.QD_QUEST_SOCLV)
    else:
        socLv = owner.socLv
    questStar = qd.get('hard', None)
    if questStar == None:
        return (0, 0, 0, 0)
    if BigWorld.component in 'cell':
        teams = [ x.box.id for x in owner.team.itervalues() if x.isOn and x.box ]
        grpCount = 0
        for memberId in teams:
            member = BigWorld.entities.get(memberId)
            if member is None:
                continue
            if distance3D(owner.position, member.position) > 80:
                continue
            grpCount += 1

    elif BigWorld.component in 'client':
        if hasattr(owner, 'members'):
            teams = [ x['id'] for x in owner.members.itervalues() if x['isOn'] ]
            grpCount = 0
            for memberId in teams:
                member = BigWorld.entities.get(memberId)
                if member is None:
                    continue
                if distance3D(owner.position, member.position) > 80:
                    continue
                grpCount += 1

        else:
            grpCount = 0
    progress, proBonus, _ = getRewardByQuestProgress(owner, questId, perfect)
    locals = {'flv': gamescript.FORMULA_FLV,
     'lv': lv,
     'slv': socLv,
     'questStar': questStar,
     'grpCount': grpCount,
     'progress': progress}
    socExpBONUS = _evaluateRewardData('socExpBonus', rewardData, locals)
    expBONUS = _evaluateRewardData('expBonus', rewardData, locals)
    grpCount = _evaluateRewardData('grpExpBonus', rewardData, locals)
    otherExpBonus = _evaluateRewardData('otherExpBonus', rewardData, locals)
    totalExp = expBONUS + grpCount + otherExpBonus
    expXiuWei = _evaluateRewardData('expXiuWei', rewardData, locals)
    grpExpXiuWei = _evaluateRewardData('grpExpXiuWei', rewardData, locals)
    totalXiuWei = expXiuWei + grpExpXiuWei
    cashBonus = _evaluateRewardData('cashBonus', rewardData, locals)
    if questLoopId != 0:
        return _calcQuestLoopReward(owner, questLoopId, totalExp, cashBonus, socExpBONUS, totalXiuWei)
    else:
        return (int(totalExp),
         int(cashBonus),
         int(socExpBONUS),
         int(totalXiuWei))


def calcExtraReward(owner, questId):
    if not QED.data.has_key(questId):
        return (0, 0, 0)
    qed = QED.data[questId]
    qd = QD.data.get(questId, {})
    rewardMode = qed.get('reward', None)
    if rewardMode == None:
        return (0, 0, 0)
    rewardData = QRD.data.get(rewardMode, None)
    if rewardData == None:
        return (0, 0, 0)
    lv = owner.getQuestLv(questId, qd)
    questStar = qd.get('hard', None)
    if questStar == None:
        return (0, 0, 0)
    if BigWorld.component in 'cell':
        grpCount = len(owner.team)
    elif BigWorld.component in 'client':
        if hasattr(owner, 'members'):
            grpCount = len(owner.members)
        else:
            grpCount = 0
    locals = {'flv': gamescript.FORMULA_FLV,
     'lv': lv,
     'questStar': questStar,
     'grpCount': grpCount}
    expBONUS = _evaluateRewardData('expBonus', rewardData, locals)
    grpCount = _evaluateRewardData('grpExpBonus', rewardData, locals)
    otherExpBonus = _evaluateRewardData('otherExpBonus', rewardData, locals)
    totalExp = expBONUS + grpCount + otherExpBonus
    cashBonus = _evaluateRewardData('cashBonus', rewardData, locals)
    return (totalExp, cashBonus, 0)


def getQuestLoopAwardFactorByType(owner, questLoopId, type):
    awardFactor = 1.0
    qld = QLD.data.get(questLoopId, None)
    qlVal = owner.questLoopInfo.get(questLoopId, None)
    if not qld or not qlVal:
        return awardFactor
    loopCnt = qlVal.loopCnt if qlVal else 0
    loopReward = qld.get('loopReward', {})
    if loopReward.has_key(type):
        ratio = _getRatio(loopReward[type], loopCnt)
        awardFactor *= ratio
    return awardFactor


def _calcQuestLoopReward(owner, questLoopId, totalExp, cashBonus, socExp = 0, expXiuWei = 0):
    qld = QLD.data.get(questLoopId, None)
    if qld == None:
        return (totalExp,
         cashBonus,
         socExp,
         expXiuWei)
    qlVal = owner.questLoopInfo.get(questLoopId, None)
    loopCnt = qlVal.loopCnt if qlVal else 0
    loopReward = qld.get('loopReward', {})
    if loopReward.has_key(gametypes.QUEST_REWARD_EXP):
        ratio = _getRatio(loopReward[gametypes.QUEST_REWARD_EXP], loopCnt)
        totalExp *= ratio
    if loopReward.has_key(gametypes.QUEST_REWARD_CASH):
        ratio = _getRatio(loopReward[gametypes.QUEST_REWARD_CASH], loopCnt)
        cashBonus *= ratio
    if loopReward.has_key(gametypes.QUEST_REWARD_SOCEXP):
        ratio = _getRatio(loopReward[gametypes.QUEST_REWARD_SOCEXP], loopCnt)
        socExp *= ratio
    if loopReward.has_key(gametypes.QUEST_REWARD_EXPXIUWEI):
        ratio = _getRatio(loopReward[gametypes.QUEST_REWARD_EXPXIUWEI], loopCnt)
        expXiuWei *= ratio
    step = qlVal.getCurrentStep() if qlVal else 0
    stepReward = qld.get('stepReward', {})
    if stepReward.has_key(gametypes.QUEST_REWARD_EXP):
        totalExp *= stepReward[gametypes.QUEST_REWARD_EXP][step]
    if stepReward.has_key(gametypes.QUEST_REWARD_CASH):
        cashBonus *= stepReward[gametypes.QUEST_REWARD_CASH][step]
    if stepReward.has_key(gametypes.QUEST_REWARD_SOCEXP):
        socExp *= stepReward[gametypes.QUEST_REWARD_SOCEXP][step]
    if stepReward.has_key(gametypes.QUEST_REWARD_EXPXIUWEI):
        expXiuWei *= stepReward[gametypes.QUEST_REWARD_EXPXIUWEI][step]
    return (int(totalExp),
     int(cashBonus),
     int(socExp),
     int(expXiuWei))


def _getRatio(loopRewardValue, loopCnt):
    ratio = 0
    length = len(loopRewardValue)
    for i in range(length):
        if loopCnt + 1 >= loopRewardValue[i][0] and loopCnt + 1 <= loopRewardValue[i][1]:
            ratio = loopRewardValue[i][2]
            break

    if i == length - 1 and ratio == 0 and loopRewardValue[i][1] == const.ENDLESS_LOOP_CNT:
        ratio = loopRewardValue[i][2]
    return ratio


def questTimeLeft(owner, questId):
    timeout = 1
    if BigWorld.component in 'cell':
        current = time.time()
    elif BigWorld.component in 'client':
        current = BigWorld.player().getServerTime()
    qd = QD.data[questId]
    if qd.has_key('timeLimit'):
        limit = qd['timeLimit']
        timeout = owner.getQuestData(questId, const.QD_BEGIN_TIME, 0) + limit - current
    elif qd.has_key('timeRemain'):
        duration = qd['timeRemain']
        timeout = owner.getQuestData(questId, const.QD_TIME_REMAIN) + duration - current
    if timeout > 0 and not owner.getQuestData(questId, const.QD_FAIL):
        return timeout
    else:
        return -1


def getTrackedQuestNum(owner):
    cnt = 0
    for questId in owner.quests:
        if owner.getQuestData(questId, const.QD_QUEST_TRACKED, False):
            cnt += 1

    return cnt


def genQuestRewardItems(owner, questId, isAvailable = False):
    qd = QD.data.get(questId, None)
    if qd == None:
        return []
    if not qd.has_key('situationType'):
        return _genQuestRewardNormalItems(owner, qd, questId, isAvailable)
    if gametypes.QUEST_REWARD_ITEM_SITUATION_TYPE == qd['situationType']:
        if not qd.get('situationParam', ()):
            return _genQuestRewardNormalItems(owner, qd, questId, isAvailable)
        completeQuest = False
        for param in qd['situationParam']:
            completeQuestTmp = True
            for questId in param:
                if not owner.getQuestFlag(questId):
                    completeQuestTmp = False
                    break

            if completeQuestTmp:
                completeQuest = True
                break

        if not completeQuest:
            return _genQuestRewardNormalItems(owner, qd, questId, isAvailable)
        rewardItemsBySituation = qd.get('rewardItemsBySituation', [])
        rewardItemsBySituation = utils.filtItemByConfig(rewardItemsBySituation, lambda e: e[0])
        return _popNoQuestItemReward(owner, rewardItemsBySituation)
    if gametypes.QUEST_REWARD_ITEM_EXTRA_SITUATION_TYPE == qd['situationType']:
        if not qd.get('situationParam', ()):
            return _genQuestRewardNormalItems(owner, qd, questId, isAvailable)
        completeQuest = False
        for param in qd.get('situationParam', ()):
            varList = {}
            statsType = param[0]
            gamelog.info('@lyh statsType', statsType)
            if statsType == gametypes.STATS_TYPE_ACHIEVE:
                varList = owner.busyStatsInfo
            elif statsType == gametypes.STATS_TYPE_STATS:
                varList = owner.busyStatsInfo
            elif statsType == gametypes.STATS_TYPE_QUEST:
                varList = owner.questVars
            elif statsType == gametypes.STATS_TYPE_JOB:
                varList = owner.questVars
            elif statsType == gametypes.STATS_TYPE_ACTION:
                varList = owner.busyStatsInfo
            elif statsType == gametypes.STATS_TYPE_SUMMON_SPRITE_BIO:
                varList = owner.busyStatsInfo
            if varList and varList.get(param[1], 0) >= param[2]:
                completeQuest = True
            else:
                completeQuest = False
                break

        if completeQuest:
            rewardItemsBySituation = qd.get('rewardItemsBySituation', [])
            rewardItemsBySituation = utils.filtItemByConfig(rewardItemsBySituation, lambda e: e[0])
            return _popNoQuestItemReward(owner, rewardItemsBySituation)
        return _genQuestRewardNormalItems(owner, qd, questId, isAvailable)


def _genQuestRewardNormalItems(owner, qd, questId, isAvailable):
    if isAvailable:
        rewardItems = qd.get('rewardItems', [])
        rewardItems = utils.filtItemByConfig(rewardItems, lambda e: e[0])
    elif isPuzzleReward(owner, questId):
        rewardItems = qd.get('puzzleRewardItems', [])
    else:
        rewardItems = qd.get('rewardItems', [])
        rewardItems = utils.filtItemByConfig(rewardItems, lambda e: e[0])
    return _popNoQuestItemReward(owner, rewardItems)


def _popNoQuestItemReward(owner, rewardItems):
    res = []
    for itemInfo in rewardItems:
        if not _checkQuestItemReward(owner, itemInfo):
            continue
        itemId = itemInfo[0]
        amount = itemInfo[1]
        res.append((itemId, amount))

    return res


def getQuestLoopRewardItem(owner, questLoopId):
    qld = QLD.data[questLoopId]
    bonusId = qld.get('bonusId', 0)
    return clientUtils.genItemBonus(bonusId)


def getQuestFirstLoopRewardItem(owner, questLoopId):
    qlVal = owner.questLoopInfo.get(questLoopId, None)
    loopCnt = qlVal.loopCnt if qlVal else 0
    if loopCnt == 0:
        qld = QLD.data[questLoopId]
        firstLoopBonusId = qld.get('firstLoopBonusId', 0)
    else:
        return []
    return clientUtils.genItemBonus(firstLoopBonusId)


def genQuestExtraRewardItems(owner, questId):
    qed = QED.data.get(questId, None)
    if qed == None:
        return []
    if not qed.has_key('rewardItems'):
        return []
    res = []
    for itemInfo in qed['rewardItems']:
        if not _checkQuestItemReward(owner, itemInfo):
            continue
        itemId = itemInfo[0]
        amount = itemInfo[1]
        res.append((itemId, amount))

    if owner.getQuestData(questId, const.QD_EXTRA_BONUS_NUID, 0) == owner.gbId and qed.has_key('rewardExtraItems'):
        for itemInfo in qed['rewardExtraItems']:
            if not _checkQuestItemReward(owner, itemInfo):
                continue
            itemId = itemInfo[0]
            amount = itemInfo[1]
            res.append((itemId, amount))

    return res


def genGroupHeaderRewardItems(owner, questId):
    qd = QD.data.get(questId, None)
    if qd == None:
        return []
    bonusId = qd.get('groupHeaderReward', 0)
    return clientUtils.genItemBonus(bonusId)


def genQuestRewardChoice(owner, questId):
    qd = QD.data.get(questId, None)
    if qd == None:
        return []
    if not qd.has_key('rewardChoice'):
        return []
    res = []
    rewardChoice = utils.filtItemByConfig(qd['rewardChoice'], lambda e: e[0])
    for itemInfo in rewardChoice:
        if not _checkQuestItemReward(owner, itemInfo):
            continue
        itemId = itemInfo[0]
        amount = itemInfo[1]
        res.append((itemId, amount))

    return res


def getRewardByQuestProgress(owner, questId, perfect = True):
    qd = QD.data.get(questId, None)
    if not (qd and qd.has_key('progressReward')):
        return (0, 0, 1)
    proRwds = qd['progressReward']
    if not (type(proRwds) == list and len(proRwds) > 0):
        return (0, 0, 1)
    if perfect and len(proRwds[-1]) == 3:
        return proRwds[-1]
    perform = 0
    progress, rewardId, prop = (0, 0, 1)
    if qd.has_key('triggerPartial') and qd.has_key('markerNpcs') and owner.hasQuestData(questId, const.QD_QUEST_MARKER):
        markerInfo, _ = owner.getQuestData(questId, const.QD_QUEST_MARKER)
        for count in markerInfo.values():
            if count > 0:
                perform += 1

    elif qd.has_key('puzzleId') and qd.get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE) in gametypes.PUZZLE_MODE_REWARD_BY_PROGRESS:
        puzzleInfo = owner.getQuestData(questId, const.QD_PUZZLE, {0: const.PUZZLE_WRONG})
        for result in puzzleInfo.values():
            if result == const.PUZZLE_RIGHE:
                perform += 1

    for proCnt, proRwdId, proProp in proRwds:
        if perform >= proCnt:
            progress, rewardId, prop = proCnt, proRwdId, proProp
        else:
            break

    return (progress, rewardId, prop)


def isPuzzleReward(owner, questId):
    flag = False
    qd = QD.data.get(questId, {})
    if qd.has_key('puzzleId') and qd.get('puzzleMode', gametypes.PUZZLE_MODE_SINGLE) == gametypes.PUZZLE_MODE_SINGLE:
        puzzleInfo = owner.getQuestData(questId, const.QD_PUZZLE, {0: const.PUZZLE_WRONG})
        if puzzleInfo.values()[0] == const.PUZZLE_WRONG:
            flag = True
    return flag


def genQuestExtraRewardChoice(owner, questId):
    qed = QED.data.get(questId, None)
    if qed == None:
        return []
    if not qed.has_key('rewardChoice'):
        return []
    res = []
    for itemInfo in qed['rewardChoice']:
        if not _checkQuestItemReward(owner, itemInfo):
            continue
        itemId = itemInfo[0]
        amount = itemInfo[1]
        res.append((itemId, amount))

    return res


def _checkQuestItemReward(owner, itemInfo):
    if len(itemInfo) == 2:
        return True
    if len(itemInfo) == 3:
        limitInfo = itemInfo[2]
        for key, value in limitInfo.iteritems():
            if key == 'sex':
                if owner.physique.sex != value:
                    return False
            elif key == 'bodyType':
                if owner.physique.bodyType != value:
                    return False
            else:
                if not hasattr(owner, key):
                    return False
                try:
                    if getattr(owner, key) != value:
                        return False
                except:
                    return False

    else:
        return False
    return True


def getEmotionIcon(markerId):
    if not QMD.data.has_key(markerId):
        return
    qmd = QMD.data[markerId]
    icon = None
    itemId = qmd.get('actionId', -1)
    if itemId != -1:
        icon = EAD.data.get(itemId, {}).get('emotionId', 0)
    return icon


def getPropIcon(markerId):
    itemId = getPropItemId(markerId)
    icon = ID.data[itemId]['icon']
    return icon


def getPropItemId(markerId):
    if not QMD.data.has_key(markerId):
        return None
    qmd = QMD.data[markerId]
    tmpItems = {}
    for itemId, amount in qmd['useItems']:
        tmpItems[itemId] = amount

    itemId = tmpItems.keys()[0]
    return itemId


def checkQuestAbnormalState(owner):
    limitLv = SCD.data.get('questAbnormalRepairLv', 0)
    if owner.lv > limitLv:
        return 0
    if formula.spaceInFuben(owner.spaceNo):
        return 0
    if owner.isolateType != gametypes.ISOLATE_TYPE_NONE:
        return 0
    realSpaceNo = formula.getRealSpaceNo(owner.spaceNo)
    for repairQuestId in QARD.data.keys():
        qard = QARD.data[repairQuestId]
        if qard.has_key('compSkip'):
            compQuestId = qard['compSkip']
            if owner.getQuestFlag(compQuestId):
                continue
        if qard.has_key('nonCompSkip'):
            nonCompQuestId = qard['nonCompSkip']
            if not owner.getQuestFlag(nonCompQuestId):
                continue
        if repairQuestId in owner.quests:
            if not qard.has_key('acSpaceNo'):
                continue
            matchSpaceNo = qard['acSpaceNo']
            destId = qard['acDest']
            gamelog.info('@szh repair ac_quest', repairQuestId, realSpaceNo, matchSpaceNo)
        elif owner.getQuestFlag(repairQuestId):
            if not qard.has_key('compSpaceNo'):
                continue
            matchSpaceNo = qard['compSpaceNo']
            destId = qard['compDest']
            gamelog.info('@szh repair comp_quest', repairQuestId, realSpaceNo, matchSpaceNo)
        else:
            if not qard.has_key('noAcSpaceNo'):
                continue
            matchSpaceNo = qard['noAcSpaceNo']
            destId = qard['noAcDest']
            gamelog.info('@szh repair non_ac_quest', repairQuestId, realSpaceNo, matchSpaceNo)
        if matchSpaceNo != realSpaceNo:
            return destId

    return 0


def isQuestGroupMatch(owner, questGroupId):
    if not QGD.data.has_key(questGroupId):
        return False
    qgd = QGD.data[questGroupId]
    mapId = formula.getMapId(owner.spaceNo)
    if mapId in qgd['mapIds']:
        return True
    else:
        return False


def getCompItemCollect(owner, data):
    if enableQuestMaterialBag(owner, data):
        return []
    items = []
    if data.has_key('compItemCollect'):
        items = list(data.get('compItemCollect', ()))
    elif data.has_key('compItemCollectMulti'):
        for item in data.get('compItemCollectMulti', ()):
            items.extend(item)

    return items


def enableQuestMaterialBag(owner, data):
    if BigWorld.component in ('client',):
        if gameglobal.rds.configData.get('enableQuestMaterialBag', False) and data.has_key('compMaterialItemCollectAndConsume'):
            return True
    elif gameconfig.enableQuestMaterialBag() and data.has_key('compMaterialItemCollectAndConsume'):
        return True
    return False


def isQuestItemCollectCompleteMulti(owner, questId):
    qd = QD.data[questId]
    if enableQuestMaterialBag(owner, qd):
        return False
    if not qd.has_key('compItemCollectMulti'):
        return False
    compItemCollectMulti = qd['compItemCollectMulti']
    costNum = None
    if utils.isYaojingqitanStartQuest(questId):
        if BigWorld.component in 'cell':
            costNum = owner.getYaojingqitanCostNum()
        elif BigWorld.component in 'client':
            costList = SCD.data.get('yaojingqitanCost', {})
            costType = getattr(BigWorld.player(), 'yaojingqitanCostType', 1)
            if costType in costList:
                costNum = costList[costType][0]
    isMatch = []
    for compItemCollect in compItemCollectMulti:
        itemOwn = 0
        itemNeed = 0
        for itemId, itemCnt in compItemCollect:
            if costNum:
                itemCnt = costNum
            if Item.isQuestItem(itemId):
                itemOwn += owner.questBag.countItemInPages(itemId)
            else:
                itemOwn += owner.realInv.countItemInPages(itemId)
            itemNeed = itemCnt

        isMatch.append(itemOwn >= itemNeed)

    for match in isMatch:
        if match == False:
            return False

    return True


def isQuestItemCollectComplete(owner, questId):
    qd = QD.data[questId]
    if enableQuestMaterialBag(owner, qd):
        return False
    if not qd.has_key('compItemCollect'):
        return False
    compItemCollect = qd['compItemCollect']
    compItemCollectType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
    tmpQuestItems = {}
    tmpCommonItems = {}
    for itemId, _ in compItemCollect:
        if Item.isQuestItem(itemId):
            tmpQuestItems[itemId] = owner.questBag.countItemInPages(itemId)
        else:
            tmpCommonItems[itemId] = owner.realInv.countItemInPages(itemId)

    if compItemCollectType == const.QUEST_COMPCOND_DISTINCT:
        isSucc = True
        for itemId, amount in compItemCollect:
            if Item.isQuestItem(itemId):
                if tmpQuestItems[itemId] < amount:
                    isSucc = False
                    break
            elif tmpCommonItems[itemId] < amount:
                isSucc = False
                break

    elif compItemCollectType == const.QUEST_COMPCOND_ALL:
        cnt = 0
        total = 0
        for itemId, amount in compItemCollect:
            if Item.isQuestItem(itemId):
                cnt += tmpQuestItems[itemId]
            else:
                cnt += tmpCommonItems[itemId]
            total = amount

        if cnt < total:
            isSucc = False
        else:
            isSucc = True
    elif compItemCollectType == const.QUEST_COMPCOND_ANY:
        isSucc = False
        for itemId, amount in compItemCollect:
            if Item.isQuestItem(itemId):
                if tmpQuestItems[itemId] >= amount:
                    isSucc = True
                    break
            elif tmpCommonItems[itemId] >= amount:
                isSucc = True
                break

    elif compItemCollectType == const.QUEST_COMPCOND_EXACT:
        isSucc = True
        for itemId, amount in compItemCollect:
            if Item.isQuestItem(itemId):
                if tmpQuestItems[itemId] != amount:
                    isSucc = False
                    break
            elif tmpCommonItems[itemId] != amount:
                isSucc = False
                break

    return isSucc


def isQuestMonsterKillComplete(owner, questId):
    qd = QD.data[questId]
    needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
    kms = owner.getQuestData(questId, const.QD_MONSTER_KILL)
    randomMonstersGroup, _ = owner.getQuestData(questId, const.QD_GROUP_MONSTER_INFO, ({}, []))
    if kms is None:
        return False
    if needMonstersType == const.QUEST_COMPCOND_DISTINCT:
        isSucc = True
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                if kms.get(no, 0) < num:
                    isSucc = False
                    break

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                if kms.get(no, 0) < num:
                    isSucc = False
                    break

    elif needMonstersType == const.QUEST_COMPCOND_ALL:
        isSucc = False
        cnt = 0
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                cnt += kms.get(no, 0)
                if cnt >= num:
                    isSucc = True
                    break

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                cnt += kms.get(no, 0)
                if cnt >= num:
                    isSucc = True
                    break

    elif needMonstersType == const.QUEST_COMPCOND_ANY:
        isSucc = False
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                if kms.get(no, 0) >= num:
                    isSucc = True
                    break

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                if kms.get(no, 0) >= num:
                    isSucc = True
                    break

    return isSucc


def isQuestItemSubmitComplete(owner, questId):
    qd = QD.data[questId]
    submitItemType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
    if not qd.has_key('submitItem'):
        return False
    compItemSubmit = qd['submitItem']
    tmpQuestItems = {}
    tmpCommonItems = {}
    for itemId, _ in compItemSubmit:
        if Item.isQuestItem(itemId):
            tmpQuestItems[itemId] = owner.questBag.countItemInPages(itemId)
        else:
            tmpCommonItems[itemId] = owner.realInv.countItemInPages(itemId)

    if submitItemType in (const.QUEST_COMPCOND_DISTINCT, const.QUEST_COMPCOND_EXACT):
        isSucc = True
        for itemId, amount in compItemSubmit:
            if Item.isQuestItem(itemId):
                if tmpQuestItems[itemId] < amount:
                    isSucc = False
                    break
            elif tmpCommonItems[itemId] < amount:
                isSucc = False
                break

    elif submitItemType == const.QUEST_COMPCOND_ALL:
        cnt = 0
        total = 0
        for itemId, amount in compItemSubmit:
            if Item.isQuestItem(itemId):
                cnt += tmpQuestItems[itemId]
            else:
                cnt += tmpCommonItems[itemId]
            total = amount

        if cnt < total:
            isSucc = False
        else:
            isSucc = True
    elif submitItemType == const.QUEST_COMPCOND_ANY:
        isSucc = False
        for itemId, amount in compItemSubmit:
            if Item.isQuestItem(itemId) and tmpQuestItems[itemId] >= amount:
                isSucc = True
                break
            elif tmpCommonItems[itemId] >= amount:
                isSucc = True
                break

    return isSucc


def isQuestRandomItemCommitComplete(owner, questId):
    qd = QD.data[questId]
    if not owner.hasQuestData(questId, const.QD_RANDOM_ITEM_COMMIT):
        return False
    randomIndex = owner.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT)
    itemId, amount = qd['randomItemCommit'][randomIndex]
    if Item.isQuestItem(itemId):
        if not owner.questBag.canRemoveItems({itemId: amount}):
            return False
    elif not owner.realInv.canRemoveItems({itemId: amount}):
        return False
    return True


def isQuestRandomItemCommitMultiComplete(owner, questId):
    qd = QD.data[questId]
    if enableQuestMaterialBag(owner, qd):
        return False
    if not owner.hasQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_MULTI):
        return False
    randomItemsMulti = owner.getQuestData(questId, const.QD_RANDOM_ITEM_COMMIT_MULTI)
    isMatch = []
    for itemGroupId, itemNeed in randomItemsMulti:
        itemOwn = 0
        itemList = QIGD.data.get(itemGroupId, {}).get('itemList', ())
        for itemId in itemList:
            if Item.isQuestItem(itemId):
                itemOwn += owner.questBag.countItemInPages(itemId, enableParentCheck=True)
            else:
                itemOwn += owner.realInv.countItemInPages(itemId, enableParentCheck=True)

        isMatch.append(itemOwn >= itemNeed)

    for match in isMatch:
        if match == False:
            return False

    return True


def getQuestLoopDisplayType(questLoopId):
    if QDID.data.has_key(questLoopId):
        return gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION
    qld = QLD.data.get(questLoopId, {})
    return qld.get('displayType', gametypes.QUEST_DISPLAY_TYPE_LOOP)


def getQuestLoopIdByQuestId(questId):
    return QLID.data.get(questId, {}).get('questLoop', 0)


def getLastQuestInLoop(questLoopId):
    if not QLD.data.has_key(questLoopId):
        return 0
    qld = QLD.data[questLoopId]
    quests = qld['quests']
    if type(quests[-1]) == int:
        return quests[-1]
    else:
        return quests[-1][-1]


def selectSubQuestsByRatio(questIds, ratios, cnt):
    questIds = [ x for x in questIds ]
    ratios = [ x for x in ratios ]
    if len(questIds) == 1:
        return questIds
    if len(ratios) == 0:
        ratios = [1] * len(questIds)
    if len(questIds) == 0 or len(questIds) != len(ratios) or len(questIds) < cnt:
        return []
    results = []
    for j in xrange(cnt):
        curRatio = random.random() * sum(ratios)
        for i in xrange(len(questIds)):
            if ratios[i] <= 0:
                continue
            curRatio -= ratios[i]
            if curRatio <= 0:
                questId = questIds.pop(i)
                ratios.pop(i)
                results.append(questId)
                break

    if const.QUEST_RATIO_MATCH_REPORT_CONFIG and len(results) < cnt:
        if BigWorld.component in ('cell', 'base'):
            gameengine.reportCritical('commQuest#selectSubQuestsByRatio cnt ratio not match: {} {}'.format(questIds, ratios))
    return results


def checkQuestEvents(questId, eventKey, eventNames):
    if not QD.data.has_key(questId):
        return False
    qd = QD.data[questId]
    if not qd.has_key(eventKey):
        return False
    events = qd[eventKey]
    for event in events:
        if event[0] in eventNames:
            return True

    return False


def calcQuestLoopGuildContri(owner, questId, guildContri):
    questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
    if questLoopId:
        qld = QLD.data.get(questLoopId, None)
        if qld is not None:
            qlVal = owner.questLoopInfo.get(questLoopId, None)
            loopCnt = qlVal.loopCnt if qlVal else 0
            loopReward = qld.get('loopReward', {})
            if loopReward.has_key(gametypes.QUEST_REWARD_GUILD_CONTRI):
                guildContri *= _getRatio(loopReward[gametypes.QUEST_REWARD_GUILD_CONTRI], loopCnt)
            step = qlVal.getCurrentStep() if qlVal else 0
            stepReward = qld.get('stepReward', {})
            if stepReward.has_key(gametypes.QUEST_REWARD_GUILD_CONTRI):
                guildContri *= stepReward[gametypes.QUEST_REWARD_GUILD_CONTRI][step]
    return guildContri


def isDelegation(questId):
    if not QLID.data.has_key(questId):
        return False
    if not QLID.data[questId].has_key('delegationId'):
        return False
    return True


def isUrgentDelegation(dgtData):
    if dgtData.has_key(const.DD_BONUS_TYPE) and dgtData[const.DD_BONUS_TYPE] != gametypes.DELEGATE_BONUS_NONE:
        return True
    else:
        return False


def checkDelegationType(owner, nuid, dId, src):
    if src == gametypes.DELEGATE_AC_SRC_STUB:
        return gametypes.DELEGATE_MARK_URGENT
    if src == gametypes.DELEGATE_AC_SRC_BENEFIT:
        return gametypes.DELEGATE_MARK_RECOMMEND
    if src == gametypes.DELEGATE_AC_SRC_BOOK:
        if owner.bookDgts.has_key(nuid):
            return owner.bookDgts[nuid].get(const.DD_MARK_TYPE, gametypes.DELEGATE_MARK_NORMAL)
    else:
        dd = DD.data[dId]
        if dd['type'] == gametypes.DELEGATE_TYPE_LIMIT:
            return gametypes.DELEGATE_MARK_LIMIT
    return gametypes.DELEGATE_MARK_NORMAL


def markDgtUrgent(dId):
    dd = DD.data[dId]
    if not dd.has_key('bonusType'):
        return (gametypes.DELEGATE_BONUS_NONE, 0)
    bonusType = random.choice(dd['bonusType'])
    bonusRate = random.choice(dd['bonusRate'])
    if bonusType == 'exp':
        return (gametypes.DELEGATE_BONUS_EXP, bonusRate)
    elif bonusType == 'money':
        return (gametypes.DELEGATE_BONUS_CASH, bonusRate)
    elif bonusType == 'item':
        return (gametypes.DELEGATE_BONUS_ITEM, bonusRate)
    else:
        return (gametypes.DELEGATE_BONUS_FAME, (bonusType, bonusRate))


def fetchPromotionDelegations(owner):
    if not DRID.data.has_key(gametypes.DELEGATE_PROMOTION_UNION):
        return []
    tmpCandidates = DRID.data[gametypes.DELEGATE_PROMOTION_UNION]
    if not tmpCandidates.has_key(owner.delegationRank):
        return []
    tmpCandidates = tmpCandidates[owner.delegationRank]
    candidates = []
    for dId in tmpCandidates:
        if not gainDelegationCheck(owner, dId):
            continue
        dud = DUD.data[dId]
        pFame = dud['fame']
        if not owner.enoughFame(pFame):
            continue
        pRank = dud['rank']
        if pRank != owner.delegationRank:
            continue
        candidates.append(dId)

    return candidates


def calcDelegationReward(owner, dId):
    dd = DD.data.get(dId, {})
    rewardMode = dd.get('reward', None)
    if rewardMode == None:
        return (0, 0)
    rewardData = QRD.data.get(rewardMode, None)
    if rewardData == None:
        return (0, 0)
    lv = owner.getDelegationData(dId, const.DD_LV)
    if not lv:
        lv = owner.lv
    dgtStar = dd.get('dgtStar', None)
    if dgtStar == None:
        return (0, 0)
    locals = {'flv': gamescript.FORMULA_FLV,
     'lv': lv,
     'dgtStar': dgtStar}
    expBONUS = _evaluateRewardData('expBonus', rewardData, locals)
    grpCount = _evaluateRewardData('grpExpBonus', rewardData, locals)
    otherExpBonus = _evaluateRewardData('otherExpBonus', rewardData, locals)
    totalExp = expBONUS + grpCount + otherExpBonus
    rateId = 0
    for expRateId in DERD.data.keys():
        num = DERD.data[expRateId]['num']
        if owner.dailyCompDgtCnt >= num and (rateId == 0 or DERD.data[rateId]['num'] < num):
            rateId = expRateId

    expRate = DERD.data.get(rateId, {}).get('rate', 1.0)
    if owner.getPreDgtFlag(dId):
        totalExp *= expRate
    cashBonus = _evaluateRewardData('cashBonus', rewardData, locals)
    rateId = 0
    for cashRateId in DCRD.data.keys():
        num = DCRD.data[cashRateId]['num']
        if owner.dailyCompDgtCnt >= num and (rateId == 0 or DCRD.data[rateId]['num'] < num):
            rateId = cashRateId

    cashRate = DCRD.data.get(rateId, {}).get('rate', 1.0)
    if owner.getPreDgtFlag(dId):
        cashBonus *= cashRate
    return (int(totalExp), int(cashBonus))


def calcCommissionCash(owner, dId, agentDuration):
    lv = DD.data.get(dId).get('rank', 0)
    return int(lv * agentDuration / 36)


def gainDelegationCheck(owner, dId, nuid = 0, src = gametypes.DELEGATE_AC_SRC_UNKNOWN, bMsg = False):
    if BigWorld.component in 'cell':
        channel = owner.client
        current = time.time()
    elif BigWorld.component in 'client':
        channel = owner
        current = owner.getServerTime()
    if dId in owner.delegations:
        bMsg and channel.showGameMsg(GMDD.data.DELEGATE_QUEST_ACC_ON, ())
        return False
    if not DD.data.has_key(dId):
        return False
    dd = DD.data[dId]
    dType = dd['type']
    rank = dd['rank']
    if rank > owner.delegationRank:
        if bMsg:
            channel.showGameMsg(GMDD.data.DELEGATE_ACC_FAIL_RANK, ())
        return False
    openQuestLv = SCD.data.get('openDelegationLv', 0)
    if owner.lv < openQuestLv:
        bMsg and channel.showGameMsg(GMDD.data.DELEGATION_BOOK_LV_LOW, ())
        return False
    if dType == gametypes.DELEGATE_TYPE_PROMOTION:
        dud = DUD.data[dId]
        pFame = dud['fame']
        if not owner.enoughFame(pFame):
            if bMsg:
                channel.showGameMsg(GMDD.data.DELEGATE_ACC_FAIL_FAME, ())
            return False
        pRank = dud['rank']
        if pRank != owner.delegationRank:
            if bMsg:
                channel.showGameMsg(GMDD.data.DELEGATE_ACC_FAIL_RANK, ())
            return False
    elif dType == gametypes.DELEGATE_TYPE_PRE:
        if owner.getPreDgtFlag(dId):
            if bMsg:
                channel.showGameMsg(GMDD.data.DELEGATE_ACC_FAIL_PRE_DONE, ())
            return False
    elif dd.has_key('preDgt') and not owner.getPreDgtFlag(dd['preDgt']):
        if bMsg:
            channel.showGameMsg(GMDD.data.DELEGATE_ACC_FAIL_PRE, ())
        return False
    if src in (gametypes.DELEGATE_AC_SRC_BOOK, gametypes.DELEGATE_AC_SRC_PRE):
        if src == gametypes.DELEGATE_AC_SRC_BOOK:
            dgtVals = owner.bookDgts
        elif src == gametypes.DELEGATE_AC_SRC_PRE:
            dgtVals = owner.stableDgts
        if not dgtVals.has_key(nuid):
            return False
        dgtVal = dgtVals[nuid]
        if isUrgentDelegation(dgtVal):
            beginTime = dgtVal[const.DD_BEGIN_TIME]
            duration = dd['duration']
            if current > duration + beginTime - 0.1:
                return False
    return True


def genDelegationRewardItems(owner, dId):
    dd = DD.data.get(dId, None)
    if dd == None:
        return []
    if not dd.has_key('rewardItems'):
        return []
    res = []
    for itemInfo in dd['rewardItems']:
        if not _checkQuestItemReward(owner, itemInfo):
            continue
        itemId = itemInfo[0]
        amount = itemInfo[1]
        res.append((itemId, amount))

    return res


def calcBookRefCost(owner, subType, rank):
    cost = []
    if BigWorld.component == 'cell':
        current = time.time()
    else:
        current = owner.getServerTime()
    if current - owner.lastRefTime <= DCD.data.get('BookRefreshInterval', 0):
        cost.append(int(DCD.data.get('BookRefreshInterval', 0) - current + owner.lastRefTime) / 60 * DCD.data.get('BookRefreshCashPerMinite', 0))
    else:
        cost.append(0)
    if subType > 0:
        cost.append(DCD.data.get('BookRefreshTypeDefinedCash', 0))
    else:
        cost.append(0)
    if rank > 0:
        cost.append(DCD.data.get('BookRefreshRankDefinedCash', 0))
    else:
        cost.append(0)
    cost.append(owner.compDgtCnt * DCD.data.get('CompDgtCompersateCash', 0))
    return cost


def getWARewardRate(owner, questId):
    wqd = WQD.data[questId]
    if not wqd.has_key('tgtVarRange') or not wqd.has_key('rewardRate'):
        return (1, 1)
    tgtVarRange = wqd['tgtVarRange']
    rewardRate = wqd['rewardRate']
    tgtVarValue = owner.getWorldQuestData(questId, const.WAQD_TGT_VAR, 0)
    amount = 0
    for i in xrange(len(tgtVarRange)):
        amount += tgtVarRange[i]
        if tgtVarValue < amount:
            if i == 0:
                return (i, 0)
            else:
                return (i, rewardRate[i - 1])

    return (i + 1, rewardRate[i])


def getJobCashNeed(owner, jobId):
    if BigWorld.component in ('cell',):
        from gamenumeric import calcFormulaById as calcFormula
    elif BigWorld.component in ('client',):
        from commcalc import _calcFormulaById as calcFormula
    jobData = JD.data.get(jobId)
    if not jobData:
        gamelog.error('invalid jobId', jobId)
        return 0
    questLoopId = jobData['questLoopId']
    questId = QLD.data.get(questLoopId, {}).get('quests', (0,))[0]
    accJobLv = owner.getQuestData(questId, const.QD_QUEST_LV, owner.lv)
    calcCashLocals = {'lv': accJobLv}
    cashNeed = int(calcFormula(jobData['cashFomulaId'], calcCashLocals))
    return cashNeed


def canAcceptJob(owner, jobId, bMsg = False):
    if BigWorld.component in ('cell',):
        channel = owner.client
    elif BigWorld.component in ('client',):
        channel = owner
    if len(getAcceptedJobs(owner)) >= SCD.data.get('maxAcceptJobs', 10):
        bMsg and channel.showGameMsg(GMDD.data.JOB_ACCEPT_MAX, (SCD.data.get('maxAcceptJobs', 10),))
        return False
    jobData = JD.data.get(jobId)
    if not jobData:
        gamelog.error('invalid jobId', jobId)
        return False
    needCash = getJobCashNeed(owner, jobId)
    if needCash and owner.inv.isRefuse():
        bMsg and channel.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        return
    if not owner._canPay(needCash):
        bMsg and channel.showGameMsg(GMDD.data.ACCEPT_JOB_FAIL_CASH, ())
        return False
    needFame = jobData.get('needFame')
    if needFame and not owner.enoughFame((needFame,)):
        fameId, fVal = needFame
        fameLv = 0
        fameData = FD.data.get(fameId, {})
        for lv, fameValue in fameData.get('lvUpNeed', {}).items():
            if fVal >= fameValue:
                fameLv = lv + 1

        fameName = fameData.get('name', '')
        fameLvName = SCD.data.get('fameLvNameModify', {}).get(fameLv, '')
        bMsg and channel.showGameMsg(GMDD.data.ACCEPT_JOB_FAIL_FAME, (fameName, fameLvName))
        return False
    return True


def getJobIdByQuestLoop(questLoopId):
    jobId = QJID.data.get(questLoopId, {}).get('jobId', 0)
    if not jobId:
        return 0
    return jobId


def getJobIdByQuest(questId):
    questLoopId = QLID.data.get(questId, {}).get('questLoop', 0)
    if not questLoopId:
        return 0
    return getJobIdByQuestLoop(questLoopId)


def getAcceptedJobQuests(owner):
    jobIds = [ (qid, getJobIdByQuest(qid)) for qid in owner.quests ]
    jobIds = [ qid for qid, jobId in jobIds if jobId ]
    return jobIds


def getAcceptedJobs(owner):
    jobIds = [ (qid, getJobIdByQuest(qid)) for qid in owner.quests ]
    jobIds = [ (qid, jobId) for qid, jobId in jobIds if jobId ]
    return jobIds


def reachMaxJobScore(owner, questId):
    needJobScore = QD.data[questId].get('needJobScore', (0,))
    jobScoreVar = QD.data[questId].get('jobScoreVar', 'jobScoreVar%d' % questId)
    jobScore = owner.questVars.get(jobScoreVar, 0)
    if jobScore >= needJobScore[-1]:
        return True
    return False


def reachExtraVarBonux(owner, questId):
    qd = QD.data[questId]
    if not QED.data.has_key(questId):
        return False
    qed = QED.data[questId]
    if not qd.has_key('shareExtraBonusRate') or not owner.getQuestData(questId, const.QD_EXTRA_BONUS_NUID):
        return False
    if not qed.has_key('questVars'):
        return False
    questVars = qed['questVars']
    for varName, value in questVars:
        if owner.questVars.get(varName, 0) < value:
            return False

    return True


def checkHasEnoughItem(player, itemId, itemNum):
    if Item.isQuestItem(itemId):
        if player.questBag.countItemInPages(itemId, enableParentCheck=True) < itemNum:
            return False
    elif player.realInv.countItemInPages(itemId, enableParentCheck=True) < itemNum:
        return False
    return True


def checkHasItem(player, itemId):
    if Item.isQuestItem(itemId):
        page, pos = player.questBag.findItemInPages(itemId, enableParentCheck=True)
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return False
    else:
        page, pos = player.realInv.findItemInPages(itemId, enableParentCheck=True)
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return False
    return True


def _checkTriggerEvent(player, monster, eventData):
    if BigWorld.component in 'cell':
        channel = player.client
    elif BigWorld.component in 'client':
        channel = player
    if utils.isOccupied(monster) and not utils.hasOccupiedRelation(player, monster):
        return False
    if eventData.get('teamMode') and player.groupType != gametypes.GROUP_TYPE_TEAM_GROUP:
        return False
    if eventData.has_key('xingJiTimeIntervals'):
        if not formula.isInXingJiTimeIntervals(eventData.get('xingJiTimeIntervals')):
            gamelog.debug('@PGF:canTriggerEvent not satisfy xingji time', formula.getXingJiTime(), eventData.get('xingJiTimeIntervals'))
            return False
    if eventData.get('hpPercent') and (monster.hp <= 0 or monster.hp * 1.0 / monster.mhp > eventData.get('hpPercent', 1)):
        gamelog.debug('@zqc cannot trigger event hp', monster.hp, monster.mhp, eventData.get('hpPercent', -1))
        return False
    if eventData.has_key('lv') and (player.lv < eventData['lv'][0] or player.lv > eventData['lv'][1]):
        gamelog.debug('zt: cannot trigger event lv', player.lv, eventData['lv'])
        return False
    if eventData.has_key('sex') and player.physique.sex != eventData['sex']:
        gamelog.debug('zt: cannot triiger event sex', player.physique.sex, eventData['sex'])
        return False
    for qid in eventData.get('notAcceptQuests', ()):
        if qid in player.quests:
            gamelog.debug('zt: cannot triiger event notAcceptQuests', qid, eventData['notAcceptQuests'])
            return False

    for qid in eventData.get('notCompleteQuests', ()):
        if player.getQuestFlag(qid):
            gamelog.debug('zt: cannot triiger event notCompleteQuests', qid, eventData['notCompleteQuests'])
            return False

    if eventData.has_key('radii') and distance3D(monster.position, player.position) > eventData['radii'] + 1:
        gamelog.debug('zt: cannot triiger event radii', eventData['radii'])
        return False
    if eventData.has_key('zaijuStatus') and player._isOnZaiju() and player._getZaijuNo() != eventData['zaijuStatus']:
        gamelog.debug('zt: cannot triiger event zaiju', eventData['zaijuStatus'], player._isOnZaiju(), player._getZaijuNo())
        return False
    if eventData.has_key('useItem'):
        if not checkHasItem(player, eventData['useItem']):
            return False
    if eventData.has_key('hasItem'):
        if not checkHasItem(player, eventData['hasItem']):
            channel.showGameMsg(eventData.get('hasItemMsgId', GMDD.data.QUEST_ACCEPT_CHECK_ITEM_FAIL), (ID.data.get(eventData['hasItem'], {}).get('name', ''),))
            return False
    if eventData.has_key('needAcceptQuests') and not any([ qid in player.quests for qid in eventData['needAcceptQuests'] ]):
        gamelog.debug('zt: cannot triiger event needAcceptQuests', eventData['needAcceptQuests'], player.quests)
        return False
    if eventData.has_key('needAcceptwaQuest') and not any([ qid in player.worldQuests for qid in eventData['needAcceptwaQuest'] ]):
        gamelog.debug('zt: cannot triiger event needAcceptQuests', eventData['needAcceptwaQuest'], player.worldQuests)
        return False
    if eventData.has_key('state') and not player.hasState(eventData['state']):
        gamelog.debug('zt: cannot triiger event state', eventData['state'])
        return False
    if eventData.has_key('notTriggerState') and player.hasState(eventData['notTriggerState']):
        gamelog.debug('syk: cannot trigger event notTriggerState', eventData['notTriggerState'])
        return False
    if eventData.has_key('zaijuStatus') and (not player._isOnZaiju() or player._getZaijuNo() != eventData['zaijuStatus']):
        gamelog.debug('zt: cannot triiger event zaiju', eventData['zaijuStatus'])
        return False
    if eventData.get('notInZaiju') and player._isOnZaiju():
        gamelog.debug('zt: cannot triiger event in zaiju', eventData['notInZaiju'])
        return False
    if eventData.has_key('notFailQuest') and any([ player.getQuestData(qid, const.QD_FAIL, False) for qid in eventData['notFailQuest'] ]):
        gamelog.debug('zt: cannot triiger event failQuest', eventData['notFailQuest'])
        return False
    if eventData.has_key('needHeader') and player.groupHeader != player.id:
        gamelog.debug('@PGF: cannot trigger event needHeader', player.groupHeader, player.id)
        channel.showGameMsg(eventData.get('needHeaderMsgId', GMDD.data.QUEST_ACCEPT_HEADER_FAIL), ())
        return False
    if eventData.has_key('checkFbNo') and formula.inExcludeFubenList(eventData['checkFbNo'], player.fbStatusList):
        gamelog.debug('@PGF: cannot trigger event checkFbNo', eventData['checkFbNo'], player.fbStatusList)
        channel.showGameMsg(eventData.get('checkFbNoMsgId', GMDD.data.QUEST_ACCEPT_CHECK_FB_FAIL), ())
        return False
    if eventData.has_key('clues') and not all([ player.getClueFlag(cid) for cid in eventData['clues'] ]):
        gamelog.debug('zt: cannot trigger event clues', eventData['clues'])
        return False
    if eventData.has_key('noClues') and any([ player.getClueFlag(cid) for cid in eventData['noClues'] ]):
        gamelog.debug('zt: cannot trigger event noClues', eventData['noClues'])
        return False
    return True


def canTriggerEvent(player, monster, eventIndex = None):
    eventDataList = METD.data.get(monster.charType, ())
    for i, eventData in enumerate(eventDataList):
        if eventIndex is not None and eventIndex != i:
            continue
        if _checkTriggerEvent(player, monster, eventData):
            return i

    return -1


def getAllTriggerEvent(player, monster):
    ret = []
    eventDataList = METD.data.get(monster.charType, ())
    for i, eventData in enumerate(eventDataList):
        if _checkTriggerEvent(player, monster, eventData):
            ret.append(i)

    return ret


def canTriggerEffect(player, monster):
    eventDataList = METD.data.get(monster.charType)
    if not eventDataList:
        return False
    for i, eventData in enumerate(eventDataList):
        if eventData.has_key('needAcceptQuests') and not any([ qid in player.quests for qid in eventData['needAcceptQuests'] ]):
            gamelog.debug('zt: cannot triiger event needAcceptQuests', eventData['needAcceptQuests'], player.quests)
            return False
        if eventData.has_key('needAcceptwaQuest') and not any([ qid in player.worldQuests for qid in eventData['needAcceptwaQuest'] ]):
            gamelog.debug('zt: cannot triiger event needAcceptQuests', eventData['needAcceptwaQuest'], player.worldQuests)
            return False
        if eventData.has_key('cd') and utils.getNow() < monster.nextTriggerEventTime.get(i, 0):
            return False

    return True


def getExpectLiberateCnt(owner):
    isolateMapInfo = ICD.data['isolateLimit']
    if not isolateMapInfo.has_key(owner.isolateType):
        return 0
    isolateInfo = isolateMapInfo[owner.isolateType]
    if owner.isolateInfo.get(owner.isolateType, 0) > max(isolateInfo.keys()):
        isolateCnt = max(isolateInfo.keys())
    else:
        isolateCnt = owner.isolateInfo.get(owner.isolateType, 0)
    return isolateInfo.get(isolateCnt, 0)


def getRuneLvLarger(owner, lv):
    cnt = 0
    if BigWorld.component == 'client' and gameglobal.rds.configData.get('enableHierogram', False) or BigWorld.component != 'client' and gameconfig.enableHierogram():
        if hasattr(owner, 'iterAllCrystalItems'):
            for crystal in owner.iterAllCrystalItems(ignoreSwitch=False):
                rData = Item.getRuneCfgData(crystal.id)
                if rData.get('lv', 0) >= lv:
                    cnt += 1

    elif hasattr(owner, 'runeBoard') and hasattr(owner.runeBoard.runeEquip, 'runeData'):
        for runeDataVal in owner.runeBoard.runeEquip.runeData:
            rData = Item.getRuneCfgData(runeDataVal.item.id)
            if rData.get('lv', 0) >= lv:
                cnt += 1

    return cnt


def getQuestMonsterKillNumCompAny(owner, questId):
    killNum = 0
    qd = QD.data[questId]
    needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
    kms = owner.getQuestData(questId, const.QD_MONSTER_KILL)
    randomMonstersGroup, _ = owner.getQuestData(questId, const.QD_GROUP_MONSTER_INFO, ({}, []))
    if kms is None:
        return 0
    if needMonstersType == const.QUEST_COMPCOND_ANY:
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                killNum = max(kms.get(no, 0), killNum)

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                killNum = max(kms.get(no, 0), killNum)

    return killNum


def getQuestMonsterKillNeedMonsterIdList(owner, questId):
    qd = QD.data.get(questId, {})
    needMonstersType = qd.get('compCondType', const.QUEST_COMPCOND_DISTINCT)
    kms = owner.getQuestData(questId, const.QD_MONSTER_KILL)
    randomMonstersGroup, _ = owner.getQuestData(questId, const.QD_GROUP_MONSTER_INFO, ({}, []))
    if kms is None:
        return []
    needMonsterIdList = []
    if needMonstersType == const.QUEST_COMPCOND_DISTINCT:
        isSucc = True
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                if kms.get(no, 0) < num:
                    needMonsterIdList.append(no)
                    isSucc = False

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                if kms.get(no, 0) < num:
                    needMonsterIdList.append(no)
                    isSucc = False

    elif needMonstersType == const.QUEST_COMPCOND_ALL:
        isSucc = False
        cnt = 0
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                cnt += kms.get(no, 0)
                if cnt >= num:
                    isSucc = True
                    break
                else:
                    needMonsterIdList.append(no)

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                cnt += kms.get(no, 0)
                if cnt >= num:
                    isSucc = True
                    break
                else:
                    needMonsterIdList.append(no)

    elif needMonstersType == const.QUEST_COMPCOND_ANY:
        isSucc = False
        if qd.has_key('needMonsters'):
            for no, num in qd['needMonsters']:
                if kms.get(no, 0) >= num:
                    isSucc = True
                    break
                else:
                    needMonsterIdList.append(no)

        elif qd.has_key('needMonstersGroup'):
            for no, num in randomMonstersGroup.iteritems():
                if kms.get(no, 0) >= num:
                    isSucc = True
                    break
                else:
                    needMonsterIdList.append(no)

    else:
        isSucc = True
    if isSucc:
        return []
    return needMonsterIdList


def isShowAvailableQuest(questId):
    showDisplayInLittleMap = QD.data.get(questId, {}).get('showMapCanAcceptQuestLogo', -1)
    if showDisplayInLittleMap >= 0:
        return showDisplayInLittleMap
    displayType = QD.data.get(questId, {}).get('displayType', 0)
    if displayType > 0:
        showDisplayInLittleMap = QTSD.data.get(displayType, {}).get('showMapCanAcceptQuestLogo', False)
        return showDisplayInLittleMap
    return showDisplayInLittleMap


def isShowExcludeAvailableMarkQuest(questId):
    showDisplayInLittleMap = QD.data.get(questId, {}).get('showMapExcludeCanAcceptQuestLogo', -1)
    if showDisplayInLittleMap >= 0:
        return showDisplayInLittleMap
    else:
        displayType = QD.data.get(questId, {}).get('displayType', 0)
        if displayType > 0:
            showDisplayInLittleMap = QTSD.data.get(displayType, {}).get('showMapExcludeCanAcceptQuestLogo', False)
            return showDisplayInLittleMap
        return showDisplayInLittleMap


def getWorldRefreshQuestGroup(refreshType = 0):
    res = {}
    for id, data in WQRD.data.iteritems():
        tp = data.get('type', 0)
        if refreshType and tp != refreshType:
            continue
        if tp not in res:
            res[tp] = []
        res[tp].append(id)

    return res


def getGroupActionMonsterEventIndex(num):
    eventDataList = METD.data.get(num)
    if not eventDataList:
        return -1
    for i, eventData in enumerate(eventDataList):
        if eventData.get('teamMode'):
            return i

    return -1


def getGroupGlobalActionMonsterEventIndex(num):
    eventDataList = METD.data.get(num)
    if not eventDataList:
        return -1
    for i, eventData in enumerate(eventDataList):
        if eventData.get('teamMode') and eventData.get('complexTrigger'):
            return i

    return -1


def checkMonsterEventItem(target, itemId):
    if target and getattr(target, 'IsMonster', False):
        if BigWorld.component == 'client':
            if hasattr(target, 'triggerEventIndex') and target.triggerEventIndex >= 0 and METD.data.has_key(target.charType):
                eventData = METD.data[target.charType][target.triggerEventIndex]
                if eventData.get('useItem') == itemId:
                    return True
        elif BigWorld.component == 'cell':
            if METD.data.has_key(target.charType) and len(METD.data[target.charType]) == 1:
                eventData = METD.data[target.charType][0]
                if eventData.get('useItem') == itemId:
                    return True
    return False
