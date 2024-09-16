#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFScoreAwardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import utils
import formula
import const
import gamelog
from uiProxy import UIProxy
from data import bonus_data as BD
from data import battle_field_data as BFD
from cdata import guild_tournament_round_score_reward_data as GTRSRD
from cdata import cross_gtn_group_round_score_reward_data as CGGRSRD
from cdata import cross_gtn_playoff_round_score_reward_data as CGPRSRD
from cdata import game_msg_def_data as GMDD
from cdata import test_cross_gtn_group_round_score_reward_data as TCGGRSRD
from cdata import test_cross_gtn_playoff_round_score_reward_data as TCGPRSRD
from cdata import test_guild_tournament_round_score_reward_data as TGTRSRD

class BFScoreAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFScoreAwardProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.groupId = 0
        self.bFState = 0
        self.monsterInfo = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BF_SCORE_AWARD:
            self.mediator = mediator
            self.refreshInfo()

    def show(self):
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_SCORE_AWARD)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_SCORE_AWARD)

    def setBFInfo(self, groupId, bFState):
        self.groupId = groupId
        self.bFState = bFState

    def setHpInfo(self, monsterInfo):
        if self.monsterInfo != monsterInfo:
            self.monsterInfo = monsterInfo
            self.refreshHpInfo()

    def refreshInfo(self):
        if self.mediator:
            info = {}
            info['winHint'] = uiUtils.getTextFromGMD(GMDD.data.BF_SCORE_AWARD_WIN_HINT, '')
            info['loseHint'] = uiUtils.getTextFromGMD(GMDD.data.BF_SCORE_AWARD_LOSE_HINT, '')
            winList = []
            loseList = []
            if self.bFState == uiConst.BF_SCORE_AWARD_GUILD_TOURNAMENT:
                cfgData = GTRSRD.data
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    cfgData = TGTRSRD.data
                for value in cfgData.itervalues():
                    if value.get('groupId', 0) != self.groupId:
                        continue
                    if value.get('isWin', 0):
                        winList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])
                    else:
                        loseList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])

            elif self.bFState == uiConst.BF_SCORE_AWARD_CROSS_GTN_GROUP:
                cfgData = CGGRSRD.data
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    cfgData = TCGGRSRD.data
                for value in cfgData.itervalues():
                    if value.get('groupId', 0) != self.groupId:
                        continue
                    if value.get('isWin', 0):
                        winList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])
                    else:
                        loseList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])

            elif self.bFState == uiConst.BF_SCORE_AWARD_CROSS_GTN_PLAYOFF:
                cfgData = CGPRSRD.data
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    cfgData = TCGPRSRD.data
                for value in cfgData.itervalues():
                    if value.get('groupId', 0) != self.groupId:
                        continue
                    if value.get('isWin', 0):
                        winList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])
                    else:
                        loseList.append([value.get('score', (0, 0))[0], value.get('groupBonusId', 0)])

            winList.sort()
            loseList.sort()
            for i in xrange(len(winList)):
                fixedBonus = BD.data.get(winList[i][1], {}).get('fixedBonus', ())
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                if not fixedBonus:
                    continue
                info['winSlotInfo%d' % i] = uiUtils.getItemData(fixedBonus[0][1])

            for i in xrange(len(loseList)):
                fixedBonus = BD.data.get(loseList[i][1], {}).get('fixedBonus', ())
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                if not fixedBonus:
                    continue
                info['loseSlotInfo%d' % i] = uiUtils.getItemData(fixedBonus[0][1])

            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.refreshHpInfo()

    def refreshHpInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            bfdata = BFD.data.get(p.getBattleFieldFbNo(), {})
            fbNo = formula.getFubenNo(p.spaceNo)
            if formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FORT:
                maxHp = 0
                myHp = 0
                myMonsterOrder = bfdata.get('monsterOrder', {}).get(str(p.bfSideIndex + 1), [])
                myMonsterIdOrder = []
                for monsFbEntNo in myMonsterOrder:
                    isSucc = False
                    for val in self.monsterInfo.values():
                        if val.get('fbEntityNo', -1) == monsFbEntNo:
                            myMonsterIdOrder.append(val.get('entityId', 0))
                            isSucc = True
                            break

                    if not isSucc:
                        myMonsterIdOrder.append(0)

                for monster in myMonsterIdOrder:
                    myHp = max(myHp, self.monsterInfo.get(monster, {}).get('hp', 0))
                    maxHp = max(maxHp, self.monsterInfo.get(monster, {}).get('mhp', 0))

                enemyHp = 0
                enemyMonsterOrder = bfdata.get('monsterOrder', {}).get(str(2 - p.bfSideIndex), [])
                enemyMonsterIdOrder = []
                for monsFbEntNo in enemyMonsterOrder:
                    isSucc = False
                    for val in self.monsterInfo.values():
                        if val.get('fbEntityNo', -1) == monsFbEntNo:
                            enemyMonsterIdOrder.append(val.get('entityId', 0))
                            isSucc = True
                            break

                    if not isSucc:
                        enemyMonsterIdOrder.append(0)

                for monster in enemyMonsterIdOrder:
                    enemyHp = max(enemyHp, self.monsterInfo.get(monster, {}).get('hp', 0))
                    maxHp = max(maxHp, self.monsterInfo.get(monster, {}).get('mhp', 0))

                info['degree0'] = gameStrings.TEXT_BFSCOREAWARDPROXY_171 % int(maxHp * 2e-05)
                info['degree1'] = gameStrings.TEXT_BFSCOREAWARDPROXY_171 % int(maxHp * 4e-05)
                info['degree2'] = gameStrings.TEXT_BFSCOREAWARDPROXY_171 % int(maxHp * 6e-05)
                info['degree3'] = gameStrings.TEXT_BFSCOREAWARDPROXY_171 % int(maxHp * 8e-05)
                info['degree4'] = gameStrings.TEXT_BFSCOREAWARDPROXY_171 % int(maxHp * 0.0001)
                info['currentValue'] = 100.0 * (maxHp - max(myHp, enemyHp)) / maxHp if maxHp != 0 else 0
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FLAG:
                maxRes = BFD.data.get(p.getBattleFieldFbNo(), {}).get('winResLimit', 100)
                myRes = p.getMyRes()
                enemyRes = p.getEnemyRes()
                info['degree0'] = '%d' % int(maxRes * 0.2)
                info['degree1'] = '%d' % int(maxRes * 0.4)
                info['degree2'] = '%d' % int(maxRes * 0.6)
                info['degree3'] = '%d' % int(maxRes * 0.8)
                info['degree4'] = '%d' % int(maxRes)
                info['currentValue'] = 100.0 * min(myRes, enemyRes) / maxRes if maxRes != 0 else 0
            self.mediator.Invoke('refreshHpInfo', uiUtils.dict2GfxDict(info, True))
