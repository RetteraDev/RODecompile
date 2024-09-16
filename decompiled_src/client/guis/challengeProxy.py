#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/challengeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import time
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import achievement_data as ACD
from data import fame_data as FD
from data import state_data as SD
from data import school_data as SCD
from data import world_challenge_data as WCD
from data import world_challenge_npc_data as WCND
from data import world_challenge_group_data as WCGD
COLOR_GREEN = '#327423'
COLOR_RED = '#a60202'

class ChallengeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChallengeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getChallengeInfo': self.onGetChallengeInfo,
         'closeChallenge': self.onCloseChallenge,
         'joinChallenge': self.onJoinChallenge}
        self.widgetId = uiConst.WIDGET_WORLD_CHALLENGE
        self.mediator = None
        uiAdapter.registerEscFunc(self.widgetId, self.onCloseChallenge)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator

    def show(self, entId, funcId):
        if not self.showChallengeConfig():
            return
        self.entId = entId
        self.funcId = funcId
        gameglobal.rds.ui.loadWidget(self.widgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None

    def showChallengeConfig(self):
        return gameglobal.rds.configData.get('enableWorldChallenge', False)

    def genChallengeItem(self, chId):
        wcdd = WCD.data.get(chId, {})
        showStars = True
        ret = {}
        ret['chId'] = chId
        ret['title'] = wcdd.get('title', gameStrings.TEXT_CHALLENGEPROXY_152 + str(chId))
        ret['firstBonus'] = wcdd.get('firstBonusDesc', gameStrings.TEXT_CHALLENGEPROXY_65)
        ret['commonBonus'] = wcdd.get('commonBonusDesc', gameStrings.TEXT_CHALLENGEPROXY_66)
        ret['commBonusId'] = wcdd.get('commonBonusItemId', 0)
        if self.checkChallengeComplete(chId):
            logTime = self.getChallengeScoreTime(chId)
            ret['topLog'] = gameStrings.TEXT_CHALLENGEPROXY_71 % time.strftime('%Y.%m.%d', time.localtime(logTime))
            ret['enableJoin'] = True
            ret['btnLabel'] = gameStrings.TEXT_CHALLENGEPROXY_73
            ret['gotoLabel'] = ''
            ret['joinTips'] = ''
            ret['starNum'] = min(self.getChallengeScore(chId), 5)
            ret['completeFlag'] = True
            ret['showStars'] = True
            if wcdd.get('onlyOnce'):
                ret['showStars'] = False
                ret['enableJoin'] = False
                ret['firstBonus'] = gameStrings.TEXT_CHALLENGEPROXY_83
                ret['commonBonus'] = ''
            if logTime == 0:
                ret['topLog'] = ''
                ret['showStars'] = False
        else:
            joinable, tips = self.checkChallengeJoinable(chId)
            if joinable:
                ret['enableJoin'] = True
                ret['gotoLabel'] = ''
                ret['joinTips'] = ''
            else:
                ret['enableJoin'] = False
                ret['gotoLabel'] = gameStrings.TEXT_CHALLENGEPROXY_99
                ret['joinTips'] = tips
            ret['topLog'] = ''
            ret['btnLabel'] = gameStrings.TEXT_CHALLENGEPROXY_103
            ret['starNum'] = 0
            ret['completeFlag'] = False
            ret['showStars'] = False
        return ret

    def reset(self):
        self.entId = 0
        self.funcId = 0

    def checkChallengeJoinable(self, challengeId):
        data = WCD.data.get(challengeId, None)
        if not data:
            return (False, '')
        else:
            tipStr = gameStrings.TEXT_CHALLENGEPROXY_119
            joinable = True
            p = BigWorld.player()
            minLv = data.get('minLv', 0)
            if minLv:
                flag = p.lv >= minLv
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_128
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_130 % minLv, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_132 % minLv, COLOR_RED)
            acheivementId = data.get('acheivementId', 0)
            if acheivementId:
                flag = gameglobal.rds.ui.achvment.checkAchieveFlag(acheivementId)
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_139
                acName = ACD.data.get(acheivementId, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_140 + str(acheivementId))
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_142 % acName, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_144 % acName, COLOR_RED)
            preChallengeId = data.get('preId', 0)
            if preChallengeId:
                flag = self.checkChallengeComplete(preChallengeId)
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_151
                wcName = WCD.data.get(preChallengeId, {}).get('title', gameStrings.TEXT_CHALLENGEPROXY_152 + str(preChallengeId))
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_142 % wcName, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_144 % wcName, COLOR_RED)
            recommendScore = data.get('recommendScore', 0)
            if recommendScore:
                flag = p.combatScoreList[const.COMBAT_SCORE] >= recommendScore
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_163
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_142 % recommendScore, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_144 % recommendScore, COLOR_RED)
            buffId = data.get('buffId', 0)
            if buffId:
                flag = buffId in p.statesServerAndOwn.keys()
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_174
                sName = SD.data.get(buffId, {}).get('name', gameStrings.TEXT_GAMECONST_1430 + str(buffId))
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_142 % sName, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_144 % sName, COLOR_RED)
            school = data.get('school', 0)
            if school:
                flag = p.school == school
                joinable = joinable and flag
                tipStr += gameStrings.TEXT_CHALLENGEPROXY_186
                scName = SCD.data.get(school, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_187 + str(school))
                if flag:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_142 % scName, COLOR_GREEN)
                else:
                    tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_144 % scName, COLOR_RED)
            if data.has_key('fame'):
                fameId, fameVal = data.get('fame', (0, 0))
                if fameId and fameVal:
                    flag = p.fame.get(fameId) >= fameVal
                    joinable = joinable and flag
                    tipStr += gameStrings.TEXT_CHALLENGEPROXY_199 % FD.data.get(fameId, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1 + str(fameId))
                    if flag:
                        tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_201 % fameVal, COLOR_GREEN)
                    else:
                        tipStr += uiUtils.toHtml(gameStrings.TEXT_CHALLENGEPROXY_203 % fameVal, COLOR_RED)
            return (joinable, tipStr)

    def getChallengeInfo(self, challengeId):
        p = BigWorld.player()
        if not hasattr(p, 'worldChallengeInfo'):
            return None
        elif not hasattr(p.worldChallengeInfo, 'acceptChallenges'):
            return None
        else:
            return p.worldChallengeInfo.acceptChallenges.get(challengeId, None)

    def checkChallengeComplete(self, challengeId):
        chInfo = self.getChallengeInfo(challengeId)
        if not chInfo:
            return False
        return chInfo.bComplete

    def getChallengeScore(self, challengeId):
        chInfo = self.getChallengeInfo(challengeId)
        if not chInfo:
            return False
        return chInfo.highestScore

    def getChallengeScoreTime(self, challengeId):
        chInfo = self.getChallengeInfo(challengeId)
        if not chInfo:
            return False
        return chInfo.highestScoreTime

    def getChallengeGroupComleteTimes(self, groupId):
        p = BigWorld.player()
        if not hasattr(p, 'worldChallengeInfo'):
            return 0
        if not hasattr(p.worldChallengeInfo, 'groupCompleteTimes'):
            return 0
        return p.worldChallengeInfo.groupCompleteTimes.get(groupId, 0)

    def onApplyChallengeSucc(self):
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        self.hide()

    def onGetChallengeInfo(self, *arg):
        ret = {}
        groupData = WCND.data.get(self.funcId, {})
        groupId = groupData.get('groupId', 0)
        chList = []
        challengeIds = groupData.get('challengeIds', [])
        for chId in challengeIds:
            chList.append(self.genChallengeItem(chId))

        ret['npcName'] = groupData.get('npcName', 'Npc')
        ret['npcHello'] = groupData.get('npcHello', gameStrings.TEXT_CHALLENGEPROXY_268)
        ret['chList'] = chList
        comlteTips = ''
        chGroupData = WCGD.data.get(groupId, {})
        completeTimes = self.getChallengeGroupComleteTimes(groupId)
        allTimes = chGroupData.get('rewardTimes', 0)
        cdType = chGroupData.get('cdType', 0)
        if cdType == 1:
            comlteTips += gameStrings.TEXT_IMPITEM_2351
        elif cdType == 2:
            comlteTips += gameStrings.TEXT_IMPITEM_2350
        elif cdType == 3:
            comlteTips += gameStrings.TEXT_CHALLENGEPROXY_282
        comlteTips += gameStrings.TEXT_CHALLENGEPROXY_284 % (max(allTimes - completeTimes, 0), allTimes)
        ret['completeTips'] = comlteTips
        return uiUtils.dict2GfxDict(ret, True)

    def onCloseChallenge(self, *arg):
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.hide()

    def onJoinChallenge(self, *arg):
        if not self.entId:
            return
        npc = BigWorld.entities.get(self.entId)
        if not npc:
            return
        chId = int(arg[3][0].GetNumber())
        npc.cell.applyWorldChallenge(chId)
