#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSchoolTop.o
from gamestrings import gameStrings
import gamelog
import gametypes
import utils
import gameglobal
from appSetting import Obj as AppSettings
from guis import uiConst
import keys
from data import school_top_config_data as STCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class ImpSchoolTop(object):
    """
    \xe9\x97\xa8\xe6\xb4\xbe\xe9\xa6\x96\xe5\xb8\xad\xe7\x8e\xa9\xe6\xb3\x95
    1. \xe6\x8a\x95\xe7\xa5\xa8\xef\xbc\x9ap.cell.schoolTopVotePlayer(dstGbId\xef\xbc\x9a\xe8\xa2\xab\xe6\x8a\x95\xe7\xa5\xa8\xe8\x80\x85gbId)
    2. \xe6\xb7\xbb\xe5\x8a\xa0\xe7\xa6\x8f\xe8\xa2\x8b\xef\xbc\x9ap.cell.addSchoolTopLuckyBag(bagType\xef\xbc\x9a\xe7\xa6\x8f\xe8\xa2\x8b\xe7\xb1\xbb\xe5\x9e\x8b, num\xef\xbc\x9a\xe6\x95\xb0\xe9\x87\x8f)
    3. \xe8\xb4\xad\xe4\xb9\xb0\xe5\xae\xa3\xe4\xbc\xa0\xe6\x9c\x8d\xe5\x8a\xa1\xef\xbc\x9ap.cell.buySchoolTopBroadcastService(num\xef\xbc\x9a\xe6\x95\xb0\xe9\x87\x8f)
    4. \xe7\x94\xb3\xe8\xaf\xb7\xe8\xbf\x9b\xe5\x85\xa5\xe6\x88\x96\xe8\xa7\x82\xe6\x88\x98\xe6\xaf\x94\xe6\xad\xa6\xef\xbc\x9ap.cell.applySchoolTopMatch()
    5. \xe7\xa6\xbb\xe5\xbc\x80\xe6\xaf\x94\xe6\xad\xa6\xe8\xb5\x9b\xe5\x9c\xba\xef\xbc\x9ap.cell.leaveSchoolTopMatch()
    6. \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe9\x97\xa8\xe6\xb4\xbe\xe7\xab\x9e\xe9\x80\x89\xe8\x80\x85\xe5\x90\x8d\xe5\x8d\x95\xef\xbc\x9ap.base.querySchoolTopCandidates()
    7. \xe4\xbf\xae\xe6\x94\xb9\xe7\xab\x9e\xe9\x80\x89\xe5\xae\xa3\xe8\xa8\x80\xef\xbc\x9ap.base.modifySchoolTopDeclaration(content:\xe5\xae\xa3\xe8\xa8\x80\xe5\x86\x85\xe5\xae\xb9)
    8. \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe9\x97\xa8\xe6\xb4\xbe\xe6\x9c\x80\xe7\xbb\x88\xe6\xaf\x94\xe8\xb5\x9b\xe4\xba\xba\xe5\x91\x98\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x9a$p.base.queryFinalCandidates()
    9. \xe5\xae\xa3\xe4\xbc\xa0\xe6\x9c\x8d\xe5\x8a\xa1\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe9\x87\x8f $p.schoolTopBroadcastServiceNum
    10. \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8f\x82\xe8\xb5\x9b\xe7\x8e\xa9\xe5\xae\xb6\xe5\xbd\xa2\xe8\xb1\xa1\xe6\x95\xb0\xe6\x8d\xae p.cell.querySchoolTopFullClientData()
    11. \xe6\x9f\xa5\xe8\xaf\xa2\xe6\xaf\x94\xe8\xb5\x9b\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbf\xa1\xe6\x81\xaf p.base.querySchoolTopDetails()
    """

    def onQueryCandidates(self, candidates):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe7\xab\x9e\xe9\x80\x89\xe5\x90\x8d\xe5\x8d\x95\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        {gbId\xef\xbc\x9a{roleName:str,guildName:str,rank:int,lv:int,
        ticketCnt:int,luckyBag:{\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x881,2,3\xef\xbc\x89:\xe6\x95\xb0\xe9\x87\x8f(int)},
        declaration:str,rank:int, school:int}
        """
        self.schoolTopCandidates = candidates
        gameglobal.rds.ui.schoolTopVote.refreshInfo()
        gamelog.debug('@zhangkuo onQueryCandidates [candidates]', str(candidates))

    def getSelfCandidateData(self):
        return getattr(self, 'schoolTopCandidates', {}).get(self.gbId, {})

    def onSchoolTopVotePlayer(self, dstGbId):
        """
        \xe6\x8a\x95\xe7\xa5\xa8\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param dstGbId: \xe6\x8a\x95\xe7\xa5\xa8\xe7\x9b\xae\xe6\xa0\x87
        """
        for gbId, info in getattr(self, 'schoolTopCandidates', {}).iteritems():
            if gbId == dstGbId:
                info['ticketCnt'] = info.get('ticketCnt', 0) + 1

        gameglobal.rds.ui.schoolTopVote.refreshInfo()
        self.base.querySchoolTopCandidates()
        gamelog.debug('@zhangkuo onSchoolTopVotePlayer', dstGbId)

    def onAddSchoolLuckyBag(self, bagType, num):
        """
        \xe6\xb7\xbb\xe5\x8a\xa0\xe7\xab\x9e\xe9\x80\x89\xe7\xa6\x8f\xe8\xa2\x8b\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param bagType: \xe7\xa6\x8f\xe8\xa2\x8b\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x8cgametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_1\xe7\x9b\xb8\xe5\x85\xb3
        :param num:\xe7\xa6\x8f\xe8\xa2\x8b\xe4\xb8\xaa\xe6\x95\xb0
        """
        self.showGameMsg(GMDD.data.SCHOOL_TOP_ADD_LUCK_BAG_SUCC, ())
        self.base.querySchoolTopCandidates()
        gameglobal.rds.ui.schoolTopSetGift.hide()
        gamelog.debug('@zhangkuo onAddSchoolTopLuckyBag [bagType][num]', bagType, num)

    def onBuySchoolTopBroadcastService(self, num, expire):
        """
        \xe8\xb4\xad\xe4\xb9\xb0\xe5\xae\xa3\xe4\xbc\xa0\xe6\x9c\x8d\xe5\x8a\xa1\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param num:\xe5\xae\xa3\xe4\xbc\xa0\xe6\x9c\x8d\xe5\x8a\xa1\xe6\x95\xb0\xe9\x87\x8f
        :param expire:\xe8\xbf\x87\xe6\x9c\x9f\xe6\x97\xb6\xe9\x97\xb4
        """
        gameglobal.rds.ui.schoolTopVip.hide()
        self.base.querySchoolTopCandidates()
        gamelog.debug('@zhangkuo onBuySchoolTopBroadcastService [num][expire]', num, expire)

    def onPushSchoolTopStage(self, stage):
        """
        \xe6\xb4\xbb\xe5\x8a\xa8\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96
        :param stage: \xe5\x90\x84\xe8\x81\x8c\xe4\xb8\x9a\xe7\x9a\x84\xe6\xb4\xbb\xe5\x8a\xa8\xe9\x98\xb6\xe6\xae\xb5{school:stage} gametypes.SCHOOL_TOP_STAGE_CLOSED \xe7\x9b\xb8\xe5\x85\xb3
        """
        self.schoolTopStage = stage
        gameglobal.rds.ui.schoolTopPush.tryStartTimer()
        if stage.get(self.school, None) in (gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE, gametypes.SCHOOL_TOP_STAGE_MATCH_START, gametypes.SCHOOL_TOP_STAGE_OVER) and not getattr(self, 'schoolTopFullClientData', None):
            self.base.queryFinalCandidates()
            self.cell.querySchoolTopFullClientData()
        gamelog.debug('@zhangkuo onPushSchoolTopStage', stage)

    def onModifyDeclaration(self):
        """\xe4\xbf\xae\xe6\x94\xb9\xe7\xab\x9e\xe9\x80\x89\xe5\xae\xa3\xe8\xa8\x80\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83"""
        self.showGameMsg(GMDD.data.MODIFY_DECLARATION_SUCC, ())
        gameglobal.rds.ui.schoolTopDeclare.hide()
        self.base.querySchoolTopCandidates()
        gamelog.debug('@zhangkuo onModifyDeclaration')

    def onQueryFinalCandidates(self, candidates):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe9\x97\xa8\xe6\xb4\xbe\xe6\x9c\x80\xe7\xbb\x88\xe6\xaf\x94\xe8\xb5\x9b\xe4\xba\xba\xe5\x91\x98\xe4\xbf\xa1\xe6\x81\xaf
        [{'gbId':int, 'isSchoolTop':bool, 'roleName':str}, ]
        """
        self.finalCandidates = candidates
        gamelog.debug('@zhangkuo onQueryFinalCandidates [candidates]', str(candidates))

    def onSchoolTopMatchStageChange(self, stage, nextTimestamp):
        """
        \xe9\x97\xa8\xe6\xb4\xbe\xe9\xa6\x96\xe5\xb8\xad\xe6\xaf\x94\xe6\xad\xa6\xe5\x89\xaf\xe6\x9c\xac\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\x98\xe5\x8c\x96
        :param stage: \xe5\xb0\x86gametypes.SCHOOL_TOP_MATCH_PHASE_PREPARE\xe7\x9b\xb8\xe5\x85\xb3
        :param nextTimestamp: \xe4\xb8\x8b\xe4\xb8\xaa\xe9\x98\xb6\xe6\xae\xb5\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        :return:
        """
        self.schoolTopMatchStage = stage
        self.schoolTopTimeStamp = nextTimestamp
        gameglobal.rds.ui.arena.showArenaStats()
        gamelog.debug('@zhangkuo onSchoolTopMatchStageChange [stage][nextTimestamp]', stage, nextTimestamp)

    def onSchoolTopMatchScoreChange(self, matchWinner):
        """
        \xe6\xaf\x94\xe6\xad\xa6\xe6\xaf\x94\xe5\x88\x86\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96
        :param matchWinner: [(\xe7\xac\xac\xe4\xb8\x80\xe5\xb1\x80\xe8\xb5\xa2\xe5\xae\xb6gbId, roleName)\xef\xbc\x8c(\xe7\xac\xac\xe4\xba\x8c\xe5\xb1\x80\xe8\xb5\xa2\xe5\xae\xb6gbId, roleName)...]
        :return:
        """
        self.schoolTopMatchScore = matchWinner
        gameglobal.rds.ui.arena.showArenaStats()
        gamelog.debug('@zhangkuo onSchoolTopMatchScoreChange [matchWinner]', str(matchWinner))

    def onSchoolTopMatchEnd(self, winnerInfo, loserInfo, isLive):
        """
        \xe6\xaf\x94\xe6\xad\xa6\xe7\xbb\x93\xe6\x9d\x9f
        :param winnerInfo: {'gbId':int, 'roleName':str, 'isGiveUp':bool, 'isSchoolTop':bool}
        :param loserInfo: {'gbId':int, 'roleName':str, 'isGiveUp':bool, 'isSchoolTop':bool}
        :param isLive: \xe6\x98\xaf\xe5\x90\xa6\xe5\xa4\x84\xe4\xba\x8e\xe6\x97\x81\xe8\xa7\x82
        :return:
        """
        self.schoolTopEndInfo = (winnerInfo, loserInfo, isLive)
        gamelog.debug('@zhangkuo onSchoolTopMatchEnd [winnerInfo][loserInfo][isLive]', str(winnerInfo), str(loserInfo), isLive)

    def onQuerySchoolTopFullClientData(self, data):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe9\x97\xa8\xe6\xb4\xbe\xe5\x8f\x82\xe8\xb5\x9b\xe7\x8e\xa9\xe5\xae\xb6\xe5\xbd\xa2\xe8\xb1\xa1\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param data: [{'name':str,'lv':int,'signal':int, 'avatarConfig':str, 'physique':str, 'aspect':str},{}]
        """
        self.schoolTopFullClientData = data
        gamelog.debug('@zhangkuo onQuerySchoolTopFullClientData [data]', str(data))

    def onQuerySchoolTopDetails(self, details):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\xaf\x94\xe8\xb5\x9b\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbf\xa1\xe6\x81\xaf
        :param details: \xe7\xbb\x93\xe6\x9e\x84\xe5\xa6\x82\xe4\xb8\x8b\xef\xbc\x9a
        {
        'iPhase':\xe6\xaf\x94\xe6\xad\xa6\xe9\x98\xb6\xe6\xae\xb5\xef\xbc\x88\xe8\xa7\x81 gametypes.SCHOOL_TOP_MATCH_PHASE_PREPARE\xef\xbc\x89
        'curRound': int \xe5\xbd\x93\xe5\x89\x8d\xe6\xaf\x94\xe6\xad\xa6\xe5\x9b\x9e\xe5\x90\x88
        'matchWinner': [(gbId, roleName)]
        'schoolTopGbId': int \xe9\xa6\x96\xe5\xb8\xad\xe5\xbc\x9f\xe5\xad\x90gbId
        \xe2\x80\x99member'\xef\xbc\x9a {gbId:rolename},
        'combatDetails':\xe6\x88\x98\xe6\x96\x97\xe7\xbb\x9f\xe8\xae\xa1\xe4\xbf\xa1\xe6\x81\xaf,
        'nextTimestamp': \xe4\xb8\x8b\xe4\xb8\xaa\xe9\x98\xb6\xe6\xae\xb5\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        }
        :return:
        """
        self.schoolTopMatchStage = details.get('iPhase', 0)
        self.schoolTopTimeStamp = details.get('nextTimestamp', 0)
        self.schoolTopMatchScore = details.get('matchWinner', [])
        gameglobal.rds.ui.arena.showArenaStats()
        gamelog.debug('@zhangkuo onQuerySchoolTopDetails', str(details))

    def notifyLeaveSchoolTop(self, roleName):
        self.showGameMsg(GMDD.data.ARENA_FORCE_QUIT, (roleName,))

    def testSchoolTopMatchEnd(self):
        info = []
        info.append({'gbId': 111111,
         'roleName': 'aaaaa',
         'level': 50,
         'school': 3,
         'killedNum': 3,
         'assitNum': 1,
         'deathNum': 1,
         'cureNum': 20000,
         'damageNum': 30000,
         'oldSchoolTop': True,
         'schoolTop': True})
        info.append({'gbId': 22222,
         'roleName': 'bbbbb',
         'level': 50,
         'school': 3,
         'killedNum': 3,
         'assitNum': 1,
         'deathNum': 1,
         'cureNum': 20000,
         'damageNum': 30000,
         'oldSchoolTop': False,
         'schoolTop': False})
        self.schoolTopMatchEnd(info)

    def testSchoolTopMatch(self):
        info = []
        info.append({'gbId': 111111,
         'roleName': 'aaaaa',
         'level': 50,
         'school': 3,
         'killedNum': 3,
         'assitNum': 1,
         'deathNum': 1,
         'cureNum': 20000,
         'damageNum': 30000,
         'oldSchoolTop': True,
         'schoolTop': True})
        info.append({'gbId': 22222,
         'roleName': 'bbbbb',
         'level': 50,
         'school': 3,
         'killedNum': 3,
         'assitNum': 1,
         'deathNum': 1,
         'cureNum': 20000,
         'damageNum': 30000,
         'oldSchoolTop': False,
         'schoolTop': False})
        self.onSyncSchoolTopCombatDetails(info)

    def schoolTopMatchEnd(self, info):
        """
        \xe6\xaf\x94\xe8\xb5\x9b\xe7\xbb\x93\xe6\x9d\x9f
        :param info: [{'gbId':int, 'roleName':str, 'level':int, 'school': int,
        'killedNum': int, 'assitNum':int, 'deathNum':int, 'cureNum':int, 'damageNum':int, oldSchoolTop':bool, 'schoolTop':bool,
        }]
        :return:
        """
        gamelog.debug('@zhangkuo schoolTopMatchEnd [info]', str(info))
        schoolTopdef = {}
        schoolTopAtk = {}
        for matchInfo in info:
            if matchInfo['oldSchoolTop']:
                schoolTopdef = {'campNum': matchInfo['gbId'] % 2,
                 'killedNum': matchInfo['killedNum'],
                 'assistAtkNum': matchInfo['assitNum'],
                 'level': matchInfo['level'],
                 'beKilledNum': matchInfo['deathNum'],
                 'cureNum': matchInfo['cureNum'],
                 'damageNum': matchInfo['damageNum'],
                 'school': matchInfo['school'],
                 'roleName': matchInfo['roleName'],
                 'id': 0,
                 'sideNUID': getattr(self, 'sideNUID', 0) + 1,
                 'fromHostName': '',
                 'oldSchoolTop': matchInfo['oldSchoolTop'],
                 'schoolTop': matchInfo['schoolTop']}
            else:
                schoolTopAtk = {'campNum': matchInfo['gbId'] % 2,
                 'killedNum': matchInfo['killedNum'],
                 'assistAtkNum': matchInfo['assitNum'],
                 'level': matchInfo['level'],
                 'beKilledNum': matchInfo['deathNum'],
                 'cureNum': matchInfo['cureNum'],
                 'damageNum': matchInfo['damageNum'],
                 'school': matchInfo['school'],
                 'roleName': matchInfo['roleName'],
                 'id': 0,
                 'sideNUID': getattr(self, 'sideNUID', 0),
                 'fromHostName': '',
                 'oldSchoolTop': matchInfo['oldSchoolTop'],
                 'schoolTop': matchInfo['schoolTop']}

        self.arenaStatistics = []
        schoolTopAtk and self.arenaStatistics.append(schoolTopAtk)
        schoolTopdef and self.arenaStatistics.append(schoolTopdef)
        gameglobal.rds.ui.arena.showSchoolTopFinalResult()

    def testAAA(self):
        self.arenaStatistics = [{'schoolTop': False,
          'fromHostName': '',
          'cureNum': 0,
          'sideNUID': 1L,
          'killedNum': 0,
          'id': 0,
          'campNum': 1L,
          'school': 3,
          'oldSchoolTop': True,
          'level': 69,
          'damageNum': 0,
          'assistAtkNum': 0,
          'beKilledNum': 0,
          'roleName': '×ó½¨Ò°'}, {'schoolTop': False,
          'fromHostName': '',
          'cureNum': 0,
          'sideNUID': 1L,
          'killedNum': 0,
          'id': 0,
          'campNum': 1L,
          'school': 3,
          'oldSchoolTop': False,
          'level': 69,
          'damageNum': 0,
          'assistAtkNum': 0,
          'beKilledNum': 0,
          'roleName': 'â×Ú¤'}]
        gameglobal.rds.ui.arena.showSchoolTopFinalResult()

    def onSyncSchoolTopCombatDetails(self, combatInfo):
        """
        \xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\x90\x8c\xe6\xad\xa5\xe6\x88\x98\xe6\x96\x97\xe7\xbb\x9f\xe8\xae\xa1\xe4\xbf\xa1\xe6\x81\xaf
        :param combatInfo: [{'gbId':int, 'roleName':str, 'level':int, 'school': int,
        'killedNum': int, 'assitNum':int, 'deathNum':int, 'cureNum':int, 'damageNum':int,
        }]
        :return:
        """
        self.arenaStatistics = []
        for matchInfo in combatInfo:
            self.arenaStatistics.append({'campNum': matchInfo['gbId'] % 2,
             'killedNum': matchInfo['killedNum'],
             'assistAtkNum': matchInfo['assitNum'],
             'level': matchInfo['level'],
             'beKilledNum': matchInfo['deathNum'],
             'cureNum': matchInfo['cureNum'],
             'damageNum': matchInfo['damageNum'],
             'school': matchInfo['school'],
             'roleName': matchInfo['roleName'],
             'id': 0,
             'sideNUID': matchInfo['gbId'] % 2,
             'fromHostName': '',
             'oldSchoolTop': matchInfo.get('oldSchoolTop', False),
             'schoolTop': matchInfo.get('schoolTop', False)})

        gamelog.debug('@zhangkuo onSyncSchoolTopCombatDetails [combatInfo]', str(combatInfo))

    def enterSchoolTopMatch(self):
        gameglobal.rds.ui.arena.isSchoolTop = True
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_STATS)
        gameglobal.rds.ui.schoolTopFight.hide()

    def leaveSchoolTopMatch(self):
        gameglobal.rds.ui.arena.hide()

    def testArena(self):
        self.schoolTopMatchStage = gametypes.SCHOOL_TOP_MATCH_PHASE_ROUND_1
        self.schoolTopTimeStamp = utils.getNow() + 300
        self.finalCandidates = []
        self.finalCandidates.append({'gbId': 0,
         'isSchoolTop': True,
         'roleName': gameStrings.TEXT_IMPSCHOOLTOP_249})
        self.finalCandidates.append({'gbId': 1,
         'isSchoolTop': False,
         'roleName': gameStrings.TEXT_IMPSCHOOLTOP_250})
        self.schoolTopMatchScore = []
        self.schoolTopMatchScore.append((1, ''))
        self.schoolTopMatchScore.append((1, ''))
        gameglobal.rds.ui.arena.isSchoolTop = True
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_STATS)
        gameglobal.rds.ui.arena.showArenaStats()

    def onSchoolTopDpsOver(self, rank, dps, lastDps):
        """
        \xe6\x9c\xa8\xe6\xa1\xa9\xe5\x89\xaf\xe6\x9c\xac\xe7\xbb\x93\xe7\xae\x97\xe4\xbf\xa1\xe6\x81\xaf
        :param dps: \xe6\x9c\xac\xe6\xac\xa1\xe7\xa7\x92\xe4\xbc\xa4
        :param lastDps: \xe4\xb8\x8a\xe6\xac\xa1\xe7\xa7\x92\xe4\xbc\xa4
        :param rank: \xe5\xbd\x93\xe5\x89\x8d\xe6\x8e\x92\xe5\x90\x8d
        :return:
        """
        gamelog.debug('@zhangkuo onSchoolTopDpsOver [dps][lastDps][rank]', dps, lastDps, rank)
        gameglobal.rds.ui.schoolTopFubenEval.show(rank, dps, lastDps)

    def onQuerySchoolTopGuessInfo(self, data):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe7\xab\x9e\xe7\x8c\x9c\xe4\xbf\xa1\xe6\x81\xaf
        :param data:
        {
            'schoolTop': school, # {'gbId':int, 'roleName':str, 'guessCnt':int}
            'other': other, # {'gbId':int, 'roleName':str, 'guessCnt':int}
            'choosedRole': choosedRole # \xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe8\xa7\x92\xe8\x89\xb2\xef\xbc\x8c0\xe8\xa1\xa8\xe7\xa4\xba\xe6\xb2\xa1\xe6\x9c\x89\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x87
        }
        :return:
        """
        self.schoolTopGuessData = data
        gamelog.debug('@zhangkuo onQuerySchoolTopGuessInfo', str(data))

    def onGuessSchoolTopWinner(self, data):
        """
        \xe9\x80\x89\xe6\x8b\xa9\xe7\xab\x9e\xe7\x8c\x9c\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param data:
        {
            'schoolTop': school, # {'gbId':int, 'roleName':str, 'guessCnt':int}
            'other': other, # {'gbId':int, 'roleName':str, 'guessCnt':int}
            'choosedRole': choosedRole # \xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe8\xa7\x92\xe8\x89\xb2\xef\xbc\x8c0\xe8\xa1\xa8\xe7\xa4\xba\xe6\xb2\xa1\xe6\x9c\x89\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x87
        }
        :return:
        """
        self.schoolTopGuessData = data
        gamelog.debug('@zhangkuo onGuessSchoolTopWinner', str(data))

    def onQuerySchoolTopDpsTimesWeekly(self, times):
        """\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe5\x91\xa8\xe6\x8c\x91\xe6\x88\x98\xe6\x9c\xa8\xe6\xa1\xa9\xe5\x89\xaf\xe6\x9c\xac\xe7\x9a\x84\xe6\xac\xa1\xe6\x95\xb0"""
        isNew = getattr(self, 'schoolTopDpsTimesWeekly', 0) != times
        self.schoolTopDpsTimesWeekly = times
        gamelog.debug('@zhangkuo onQuerySchoolTopDpsTimesWeekly [times]', times)
        if isNew:
            gameglobal.rds.ui.playRecommActivation.refreshRecomm(None, True)

    def addSchoolTopPush(self):
        if not gameglobal.rds.configData.get('enableSchoolTopTestFuben', False):
            return None
        else:
            if not self.schoolTopDpsTimesWeekly:
                key = keys.SET_SCHOOL_TOP_PUSH_DAILY % self.gbId
                if utils.isSameDay(utils.getNow(), AppSettings.get(key, 0)):
                    return None
                start, end = STCD.data.get('pushTimeRange', (None, None))
                AppSettings[key] = utils.getNow()
                AppSettings.save()
                if start and end and utils.inTimeRange(start, end):
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SCHOOL_TOP_TEST)
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SCHOOL_TOP_TEST, {'click': self.enterSchoolTopTest})
            return None

    def enterSchoolTopTest(self):
        text = GMD.data.get(GMDD.data.SCHOOL_TOP_TEST_CONFIRM, {}).get('text', '')
        gameglobal.rds.ui.funcNpc.uiAdapter.messageBox.showYesNoMsgBox(text, gameglobal.rds.ui.funcNpc.schoolTopTestConfirm)
