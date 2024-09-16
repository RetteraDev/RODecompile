#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarActivity.o
from gamestrings import gameStrings
import BigWorld
import const
import gametypes
import utils
import uiUtils
import gameglobal
from data import ww_activity_basic_data as WWABD
from data import ww_juewei_activity_recommend_data as WWJARD
from data import world_war_config_data as WWCD
from cdata import game_msg_def_data as GMDD
REWARD_MAX_NUM = 3
REF_TYPE_QUEST_LOOP = 1
REF_TYPE_COMMIT_ITEM = 2
REF_TYPE_YABIAO = 3
REF_TYPE_KILL_BOSS = 4
REF_TYPE_WORLD_WAR = 5
RECOM_REF_TYPE_FAME = 1
RECOM_REF_TYPE_USE_ITEM = 2
RECOM_REF_TYPE_YABIAO = 3

def getActById(actId, weekDay):
    return WWActInfo(actId, weekDay)


def getActDetail(actId, weekDay):
    info = getActById(actId, weekDay)
    if info:
        return info.getDetail()
    return {}


def getActInfosByDay(weekDay):
    p = BigWorld.player()
    actInfos = []
    for actId in WWABD.data.keys():
        if not gameglobal.rds.configData.get('enableWorldWarRob'):
            if actId in gametypes.WW_ROB_QUEST_INFO_ID:
                continue
        info = getActById(actId, weekDay)
        if info:
            visibleCamp = info.getVisibleCamp()
            if visibleCamp and p.worldWar.getDayCamp(weekDay) != visibleCamp:
                continue
            startCron, endCron = info.getAvailableTime()
            sec = int(utils.getNow() + (weekDay - uiUtils.getWeekDay()) * const.TIME_INTERVAL_DAY)
            if not utils.inDateRange(startCron, endCron, sec):
                continue
            actInfos.append(info.getInfo())

    actInfos.sort(cmp=lambda x, y: cmp(x['priority'], y['priority']), reverse=True)
    return actInfos


def isAllWWActDone(weekDay):
    dayActInfos = getActInfosByDay(weekDay)
    for info in dayActInfos:
        if info['mark']:
            if not info['finished']:
                return False

    return True


def getRecommendActList():
    dailyContr = []
    weeklyContr = []
    dailyHonor = []
    weeklyHonor = []
    for actId, val in sorted(WWABD.data.iteritems(), key=lambda d: d[1]['priority'], reverse=True):
        info = WWRecommendActInfo(actId)
        val = info.getInfo()
        if info.isWeekly():
            if info.isContribition():
                weeklyContr.append(val)
            if info.isHonor():
                weeklyHonor.append(val)
        if info.isDaily():
            if info.isContribition():
                dailyContr.append(val)
            if info.isHonor():
                dailyHonor.append(val)

    return {'aList': [weeklyContr,
               dailyContr,
               weeklyHonor,
               dailyHonor]}


class WWActInfo(object):

    def __init__(self, actId, weekDay):
        self.id = actId
        self.data = WWABD.data.get(self.id, {})
        self.weekDay = weekDay

    def getName(self):
        return self.data.get('name', '')

    def getAvailableTime(self):
        return (self.data.get('startTimes') or utils.CRON_ANY, self.data.get('endTimes') or utils.CRON_ANY)

    def getBtnActionType(self):
        return self.data.get('btnActionType', 0)

    def getBtnActionName(self):
        if self.getBtnActionType() == gametypes.WW_ACTIVITY_ENTER_TYPE_WORLD_WAR_BATTLE:
            if not gameglobal.rds.ui.worldWar.enableWorldWarBattle():
                return None
            p = BigWorld.player()
            if p.worldWar.battleStateDict[gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG] == gametypes.WORLD_WAR_BATTLE_STATE_OPEN or p.worldWar.battleStateDict[gametypes.WORLD_WAR_TYPE_BATTLE] == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                if p.getWBHireState() != gametypes.WB_HIRE_OTHER_HOST:
                    minLv = WWCD.data.get('hireMinLv', const.WORLD_WAR_HIRE_MINLV)
                    if p.lv >= minLv:
                        return gameStrings.TEXT_WORLDWARACTIVITY_118
                    else:
                        return self.data.get('btnActionName2', None)
                else:
                    return None
            if p.worldWar.battleState == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                return self.data.get('btnActionName', None)
            else:
                return None
        if self.getBtnActionType() == gametypes.WW_ROB_BATTLE:
            if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                return None
            p = BigWorld.player()
            if self.weekDay % 2:
                if p.worldWar.getCamp() == p.worldWar.getCurrCamp():
                    return None
            elif p.worldWar.getCamp() != p.worldWar.getCurrCamp():
                return None
            if p.lv < const.WORLD_WAR_ARMY_MINLV:
                return None
            robStateOld = p.worldWar.robStateDict.get(gametypes.WORLD_WAR_TYPE_ROB, 0)
            robStateYoung = p.worldWar.robStateDict.get(gametypes.WORLD_WAR_TYPE_ROB_YOUNG, 0)
            if p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB_YOUNG) and p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                if robStateYoung == gametypes.WW_ROB_STATE_PREOPEN:
                    return self.data.get('btnActionName3', None)
            if p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB) and p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                if robStateOld == gametypes.WW_ROB_STATE_PREOPEN:
                    return self.data.get('btnActionName3', None)
            if robStateOld in gametypes.WW_ROB_STATE_APPLY_STATES and robStateYoung in gametypes.WW_ROB_STATE_APPLY_STATES:
                if not p.isHaveRobStartPrivilege():
                    return self.data.get('btnActionName', None)
                return None
            if robStateOld in gametypes.WW_ROB_STATE_APPLY_STATES and robStateYoung == gametypes.WW_ROB_STATE_CLOSED:
                if not p.isHaveRobStartPrivilege():
                    return self.data.get('btnActionName', None)
                return None
            if robStateYoung in gametypes.WW_ROB_STATE_APPLY_STATES and robStateOld == gametypes.WW_ROB_STATE_CLOSED:
                if not p.isHaveRobStartPrivilege():
                    return self.data.get('btnActionName', None)
                return None
            if robStateOld not in gametypes.WW_ROB_STATE_NOT_OPEN or robStateYoung not in gametypes.WW_ROB_STATE_NOT_OPEN:
                return self.data.get('btnActionName2', None)
            return None
        else:
            return self.data.get('btnActionName', None)

    def getMark(self):
        if self.isActCurrentDay():
            return self.data.get('mark', False)
        return False

    def getFullDesc(self):
        return self.data.get('fulldesc', '')

    def getVisibleCamp(self):
        return self.data.get('visibility', 0)

    def getCnt(self):
        if not self.isActCurrentDay():
            return 0
        else:
            refType = self.data.get('erefType', 0)
            refId = self.data.get('erefId', None)
            p = BigWorld.player()
            cnt = 0
            if refType == REF_TYPE_QUEST_LOOP:
                questStarLv, _ = p.worldWar.calcQuestStarLv(p.worldWar.getCountry().enemyHostId)
                loopQuestId = refId[max(questStarLv - 1, 0)]
                if p.questLoopInfo.has_key(loopQuestId):
                    if p.questLoopInfo[loopQuestId].loopCnt >= 1:
                        return self.getPeriodCnt()
                    cnt += p.questLoopInfo[loopQuestId].getCurrentStep()
            elif refType == REF_TYPE_COMMIT_ITEM:
                for npcId in refId:
                    cnt += p.itemCommitInfo.get(npcId, {}).get('dailyCnt', 0)

            elif refType == REF_TYPE_YABIAO:
                cnt = p.yabiaoCnt
            return cnt

    def getPeriodCnt(self):
        rectTimes = self.data.get('rectimes', 0)
        refType = self.data.get('erefType', 0)
        if refType == REF_TYPE_COMMIT_ITEM:
            weekCnt = 0
            for npcId in self.data.get('erefId', ()):
                weekCnt += BigWorld.player().itemCommitInfo.get(npcId, {}).get('weeklyCnt', 0)

            return max(0, min(rectTimes, self.data.get('weektimes', 0) - weekCnt + self.getCnt()))
        return rectTimes

    def getReward(self):
        reward = []
        for i in xrange(REWARD_MAX_NUM):
            fameId = self.data.get('bonus%d' % (i + 1), 0)
            cnt = self.data.get('bonusamount%d' % (i + 1), 0)
            if fameId:
                reward.append({'fameId': fameId,
                 'cnt': cnt})

        return reward

    def getAccNpc(self):
        return self.data.get('desc', '')

    def getSeekId(self):
        return self.data.get('seekid', '')

    def getPriority(self):
        return self.data.get('priority', 0)

    def isFinished(self):
        if not self.isActCurrentDay():
            return False
        refType = self.data.get('erefType', 0)
        dailyMax = self.data.get('daytimes', 0)
        p = BigWorld.player()
        if refType == REF_TYPE_COMMIT_ITEM:
            weeklyMax = self.data.get('weektimes', 0)
            refId = self.data.get('erefId', None)
            weeklyCnt = 0
            if refId:
                for npcId in refId:
                    weeklyCnt += p.itemCommitInfo.get(npcId, {}).get('weeklyCnt', 0)

            return weeklyCnt >= weeklyMax or self.getCnt() >= dailyMax
        else:
            return self.getCnt() >= dailyMax

    def isActCurrentDay(self):
        return self.weekDay == uiUtils.getWeekDay()

    def onBtnClick(self):
        p = BigWorld.player()
        if self.getBtnActionType() == gametypes.WW_ACTIVITY_ENTER_TYPE_WORLD_WAR_BATTLE:
            if p.wbApplyHireHostId:
                applyServerName = utils.getServerName(p.wbApplyHireHostId)
                msg = uiUtils.getTextFromGMD(GMDD.data.WW_CANCAEL_APPLY_HIRE_FOR_JOIN_COMFIRM, '%s') % applyServerName
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelHireAndEnterWWBattle)
                return
            if p._getWBHireHostId():
                p.showGameMsg(GMDD.data.WB_HIRE_APPLY_ALREADY_HIRED, ())
                return
            if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if p.recentEnterWWType:
                    p.cell.enterWorldWarEvent(p.recentEnterWWType)
                    return
                if p.lv > const.WORLD_WAR_ARMY_MINLV:
                    p.base.queryWWQLBHSelection(gametypes.WORLD_WAR_TYPE_BATTLE)
                else:
                    gameglobal.rds.ui.worldWarLvChoose.show(gametypes.WORLD_WAR_TYPE_BATTLE)
            else:
                p.cell.enterWorldWarEvent(gametypes.WORLD_WAR_TYPE_BATTLE)
        elif self.getBtnActionType() == gametypes.WW_ROB_BATTLE:
            p = BigWorld.player()
            robStateOld = p.worldWar.robStateDict.get(gametypes.WORLD_WAR_TYPE_ROB, 0)
            robStateYoung = p.worldWar.robStateDict.get(gametypes.WORLD_WAR_TYPE_ROB_YOUNG, 0)
            if p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB_YOUNG) and p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                if robStateYoung == gametypes.WW_ROB_STATE_PREOPEN:
                    gameglobal.rds.ui.worldWarRobOverview.onClickWWRStartMsg()
                    return
            if p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB) and p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                if robStateOld == gametypes.WW_ROB_STATE_PREOPEN:
                    gameglobal.rds.ui.worldWarRobOverview.onClickWWRStartMsg()
                    return
            if robStateOld not in gametypes.WW_ROB_STATE_NOT_OPEN or robStateOld in gametypes.WW_ROB_STATE_APPLY_STATES or robStateYoung not in gametypes.WW_ROB_STATE_NOT_OPEN or robStateYoung in gametypes.WW_ROB_STATE_APPLY_STATES:
                if p.recentEnterWWType:
                    p.cell.enterWorldWarEvent(p.recentEnterWWType)
                    return
                if p.lv > const.WORLD_WAR_ARMY_MINLV:
                    p.base.queryWWQLBHSelection(gametypes.WORLD_WAR_TYPE_ROB)
                else:
                    gameglobal.rds.ui.worldWarLvChoose.show(gametypes.WORLD_WAR_TYPE_ROB)

    def cancelHireAndEnterWWBattle(self):
        p = BigWorld.player()
        p.cell.worldWarCancelQueue(gametypes.WORLD_WAR_TYPE_BATTLE)
        p.cell.enterWorldWarEvent(gametypes.WORLD_WAR_TYPE_BATTLE)

    def formatStr(self, startCron, endCron, showDay = False, showHour = True):
        start = utils.parseCrontabPattern(startCron)
        end = utils.parseCrontabPattern(endCron)
        if [] in (start[utils.MINUTE],
         start[utils.HOUR],
         end[utils.MINUTE],
         end[utils.HOUR]):
            result = ''
            if showHour:
                if showDay:
                    return gameStrings.TEXT_WORLDWARACTIVITY_313 % (start[utils.MONTH][0],
                     start[utils.DAY][0],
                     end[utils.MONTH][0],
                     end[utils.DAY][0])
                else:
                    return '00:00-24:00'
            elif showDay:
                if [] in (start[utils.MINUTE], start[utils.HOUR]):
                    result = gameStrings.TEXT_WORLDWARACTIVITY_319 % (start[utils.MONTH][0], start[utils.DAY][0])
                else:
                    result = gameStrings.TEXT_WORLDWARACTIVITY_321 % (start[utils.MONTH][0],
                     start[utils.DAY][0],
                     start[utils.HOUR][0],
                     start[utils.MINUTE][0])
                if [] in (end[utils.MINUTE], end[utils.HOUR]):
                    result += gameStrings.TEXT_WORLDWARACTIVITY_324 % (end[utils.MONTH][0], end[utils.DAY][0])
                else:
                    result += gameStrings.TEXT_WORLDWARACTIVITY_326 % (end[utils.MONTH][0],
                     end[utils.DAY][0],
                     end[utils.HOUR][0],
                     end[utils.MINUTE][0])
            return result
        startMinute = start[utils.MINUTE][0]
        startHour = start[utils.HOUR][0]
        endMinute = end[utils.MINUTE][0]
        endHour = end[utils.HOUR][0]
        if showDay:
            return gameStrings.TEXT_WORLDWARACTIVITY_334 % (start[utils.MONTH][0],
             start[utils.DAY][0],
             startHour,
             startMinute,
             end[utils.MONTH][0],
             end[utils.DAY][0],
             endHour,
             endMinute)
        else:
            return '%02d:%02d-%02d:%02d' % (startHour,
             startMinute,
             endHour,
             endMinute)

    def getInfo(self):
        start, end = self.getAvailableTime()
        isDone = self.isFinished()
        return {'activityName': self.getName(),
         'time': self.formatStr(start, end),
         'actId': self.id,
         'timeValid': utils.inTimeRange(start, end),
         'mark': self.getMark(),
         'finished': isDone,
         'markTip': gameStrings.TEXT_WORLDWARACTIVITY_350 if isDone else gameStrings.TEXT_WORLDWARACTIVITY_350_1,
         'priority': self.getPriority()}

    def getExtraInfo(self):
        extraInfo = {}
        p = BigWorld.player()
        if not gameglobal.rds.ui.worldWar.enableWorldWarBattleHire():
            return extraInfo
        if self.getBtnActionType() == gametypes.WW_ACTIVITY_ENTER_TYPE_WORLD_WAR_BATTLE:
            if p.worldWar.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                if gameglobal.rds.configData.get('enableWorldWarBattleYoungHire', False):
                    minLv = WWCD.data.get('hireMinLvNew', const.WORLD_WAR_HIRE_MINLV_NEW)
                else:
                    minLv = WWCD.data.get('hireMinLv', const.WORLD_WAR_HIRE_MINLV)
                if p.lv >= minLv and not (p._getWBHireHostId() and p.worldWar.battleHireStopped):
                    state = p.getWBHireState()
                    if state == gametypes.WB_HIRE_UNHIRED:
                        extraInfo['mercenaryStr'] = gameStrings.TEXT_WORLDWARACTIVITY_368
                    elif state == gametypes.WB_HIRE_OTHER_HOST:
                        extraInfo['mercenaryStr'] = gameStrings.TEXT_WORLDWARACTIVITY_370 % utils.getServerName(p.wbHireHostId)
            elif p._getWBHireHostId() and not p.worldWar.battleHireStopped:
                extraInfo['mercenaryStr'] = gameStrings.TEXT_WORLDWARACTIVITY_370 % utils.getServerName(p.wbHireHostId)
        return extraInfo

    def getDetail(self):
        if self.getPeriodCnt() > 0 and self.isActCurrentDay():
            periodCnt = '%d/%d' % (self.getCnt(), self.getPeriodCnt())
        else:
            periodCnt = ''
        isDone = self.isFinished()
        val = {'desc': self.getFullDesc(),
         'activityName': self.getName(),
         'btnName': self.getBtnActionName(),
         'btnType': self.getBtnActionType(),
         'periodCnt': periodCnt,
         'reward': self.getReward(),
         'accNpc': self.getAccNpc(),
         'seekId': str(self.getSeekId()),
         'mark': self.getMark(),
         'finished': isDone,
         'markTip': gameStrings.TEXT_WORLDWARACTIVITY_350 if isDone else gameStrings.TEXT_WORLDWARACTIVITY_350_1,
         'extraInfo': self.getExtraInfo()}
        return val


class WWRecommendActInfo(object):

    def __init__(self, actId):
        self.id = actId
        self.data = WWJARD.data.get(self.id, {})

    def getCnt(self):
        refType = self.data.get('erefType')
        cnt = 0
        refNum = self.data.get('erefnum', 1)
        refId = self.data.get('erefId', 0)
        p = BigWorld.player()
        if refType == RECOM_REF_TYPE_FAME:
            cnt = p.fame.get(refId, 0)
        elif refType == RECOM_REF_TYPE_USE_ITEM:
            limitType = gametypes.ITEM_USE_LIMIT_TYPE_DAY
            if self.isWeekly():
                limitType = gametypes.ITEM_USE_LIMIT_TYPE_WEEK
            cnt = uiUtils.getItemUseNum(refId, limitType)
        elif refType == RECOM_REF_TYPE_YABIAO:
            cnt = p.yabiaoCnt
        return int(cnt * self.getPeriodCnt() / refNum)

    def getPeriodCnt(self):
        return self.data.get('limit', 0)

    def isWeekly(self):
        return self.data.get('weekly', 0)

    def isDaily(self):
        return self.data.get('daily', 0)

    def isHonor(self):
        return self.data.get('conhonor', 0)

    def isContribition(self):
        return self.data.get('contribution', 0)

    def isFinished(self):
        return self.getCnt() >= self.getPeriodCnt()

    def getInfo(self):
        return {'desc': self.data.get('fulldesc', ''),
         'rewardCnt': self.data.get('rewarddesc', ''),
         'cnt': '%s/%s' % (self.getCnt(), self.getPeriodCnt()),
         'done': self.isFinished()}
