#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/jobBoardProxy.o
from gamestrings import gameStrings
import BigWorld
import math
import gameglobal
import const
import formula
import commQuest
import utils
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from callbackHelper import Functor
from data import job_data as JD
from data import quest_loop_data as QLD
from data import fame_data as FD
from data import sys_config_data as SCD
from data import item_data as ID
from data import quest_data as QD
from data import job_action_data as JAD
from cdata import game_msg_def_data as GMDD
from data import npc_data as ND
from cdata import quest_reward_data as QRD

class JobBoardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JobBoardProxy, self).__init__(uiAdapter)
        self.modelMap = {'getJobBoardInfo': self.onGetJobBoardInfo,
         'readJobDetail': self.onReadJobDetail,
         'closeBoard': self.onCloseBoard,
         'getJobDetailInfo': self.onGetJobDetailInfo,
         'acceptJob': self.onAcceptJob,
         'closeDetail': self.onCloseDetail,
         'giveupJob': self.onGiveupJob}
        self.mediator = None
        self.detailMed = None
        self.version = 0
        self.jobRefId = None
        self.index = None
        self.jobList = None
        self.jobTimeInfo = None
        self.entityId = None
        self.curJobId = None
        self.pollingCallback = None
        self.isBigPanel = False
        self.bonusFactor = 0
        self.isOpenByQuest = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_JOB_DETAIL, self.closeDetail)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_JOB_BOARD or widgetId == uiConst.WIDGET_BIG_JOB_BOARD:
            self.mediator = mediator
            self.startPolling()
        elif widgetId == uiConst.WIDGET_JOB_DETAIL:
            self.detailMed = mediator

    def reset(self):
        if self.pollingCallback:
            BigWorld.cancelCallback(self.pollingCallback)

    def checkCanOpen(self, jobId):
        p = BigWorld.player()
        if p.lv < SCD.data.get('openJobBoardLv', 100):
            p.showGameMsg(GMDD.data.FORBIDDEN_OPEN_JOB_BOARD, ())
            return False
        questLoopId = JD.data.get(jobId, {}).get('questLoopId', 0)
        questId = QLD.data.get(questLoopId, {}).get('quests', [0])[0]
        if questId in p.quests:
            p.showTopMsg(gameStrings.TEXT_JOBBOARDPROXY_82)
            return
        return True

    def show(self, jobRefId, index, version, jobList, jobTimeInfo, boardType, bonusFactor):
        self.jobRefId = jobRefId
        self.index = index
        self.version = version
        self.jobList = jobList
        self.jobTimeInfo = jobTimeInfo
        self.bonusFactor = bonusFactor
        ent = BigWorld.entities.get(self.entityId)
        if ent:
            ent.index = index
            ent.version = version
            ent.jobList = jobList
            ent.jobTimeInfo = jobTimeInfo
            ent.bonusFactor = bonusFactor
        self.isBigPanel = boardType != 1
        if boardType == 1:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JOB_BOARD)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BIG_JOB_BOARD)

    def clearWidget(self):
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        if self.isBigPanel:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIG_JOB_BOARD)
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JOB_BOARD)
        self.closeDetail()

    def showDetail(self, jobId):
        self.curJobId = jobId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JOB_DETAIL)

    def closeDetail(self):
        self.detailMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JOB_DETAIL)

    def _getFameLv(self, fameId, fameVal):
        fd = FD.data.get(fameId)
        ret = 1
        lvArray = fd.get('lvUpNeed', {}).items()
        lvArray.sort(key=lambda k: k[1], reverse=True)
        for key, val in lvArray:
            if fameVal >= val:
                ret = key + 1
                break

        return ret

    def _getFameReq(self, fameInfo):
        fd = FD.data.get(fameInfo[0])
        if not fd:
            return ''
        fameName = fd['name']
        return '%s' % fameName

    def _getFameDetail(self, fameInfo):
        fd = FD.data.get(fameInfo[0])
        if not fd:
            return ''
        fameLv = self._getFameLv(fameInfo[0], fameInfo[1])
        fameLvName = SCD.data.get('fameLvNameModify', {}).get(fameLv, '')
        return '%s' % fameLvName

    def createJobBoardInfo(self):
        ent = BigWorld.entities.get(self.entityId)
        if not ent:
            boardName = ''
        else:
            boardName = ent.roleName
        if self.jobTimeInfo[0][1]:
            endTime = uiUtils.convertToXingJiWord(uiUtils.getXingJiWordIdx(self.jobTimeInfo[0][1]))
        else:
            endTime = ''
        if self.jobTimeInfo[1][0]:
            nextTime = uiUtils.convertToXingJiWord(uiUtils.getXingJiWordIdx(self.jobTimeInfo[1][0]))
        else:
            nextTime = ''
        jobs = []
        for jobVal in self.jobList:
            data = JD.data.get(jobVal.jobId, {})
            title = data.get('name', '')
            questLoopId = data.get('questLoopId', 0)
            lv = QLD.data.get(questLoopId, {}).get('acMinLv', 1)
            moneyReq = commQuest.getJobCashNeed(BigWorld.player(), jobVal.jobId)
            fameReq = self._getFameReq(data.get('needFame', (0, 0)))
            fameDetail = self._getFameDetail(data.get('needFame', (0, 0)))
            totalNum = jobVal.count
            availableNum = jobVal.rest
            standardCount = data.get('count', 0)
            countUp = data.get('count', 0) < totalNum
            jobs.append({'lv': lv,
             'title': title,
             'fameReq': fameReq,
             'moneyReq': moneyReq,
             'totalNum': totalNum,
             'availableNum': availableNum,
             'jobId': jobVal.jobId,
             'countUp': countUp,
             'fameDetail': fameDetail,
             'standardCount': standardCount})

        ret = {'boardName': boardName,
         'endTime': endTime,
         'leftTime': 0,
         'nextTime': nextTime,
         'jobs': jobs,
         'bonusFactor': self.bonusFactor}
        return uiUtils.dict2GfxDict(ret, True)

    def setJobBoardInfo(self):
        if self.mediator:
            self.mediator.Invoke('setJobBoardInfo', self.createJobBoardInfo())

    def _isJobRunOut(self, jobId):
        for jobVal in self.jobList:
            if jobVal.jobId == jobId and jobVal.rest == 0:
                return True

        return False

    def createJobDetailInfo(self):
        if self.curJobId == None:
            return
        else:
            ret = {}
            data = JD.data.get(self.curJobId, {})
            questLoopId = data.get('questLoopId', 0)
            questId = QLD.data.get(questLoopId, {}).get('quests', [0])[0]
            qData = QD.data.get(questId, {})
            p = BigWorld.player()
            if self.jobList == None:
                self.jobList = p.getQuestData(questId, const.QD_JOBS)
            if self.jobTimeInfo == None:
                jobTimeInfo = p.getQuestData(questId, const.QD_JOB_TIME)
                if jobTimeInfo:
                    start = math.ceil(formula.getXingJiTime(formula.getFloatDayTime(math.ceil(jobTimeInfo[0]))))
                    end = math.ceil(formula.getXingJiTime(formula.getFloatDayTime(math.ceil(jobTimeInfo[1]))))
                    self.jobTimeInfo = [(start, end)]
            if self.bonusFactor == None:
                self.bonusFactor = p.getQuestData(questId, const.QD_BONUS_FACTOR)
            isFail = p.getQuestData(questId, const.QD_FAIL)
            if not isFail and not self.isOpenByQuest:
                canAccept = not self._isJobRunOut(self.curJobId)
            else:
                canAccept = False
            if questId in BigWorld.player().quests:
                isAccepted = True
            else:
                isAccepted = False
            title = QLD.data.get(questLoopId, {}).get('name', '')
            if self.jobTimeInfo:
                endTime = uiUtils.convertToXingJiWord(uiUtils.getXingJiWordIdx(int(self.jobTimeInfo[0][1])))
            else:
                endTime = ''
            desc = QLD.data.get(questLoopId, {}).get('desc', '')
            req = ''
            moneyReq = commQuest.getJobCashNeed(BigWorld.player(), self.curJobId)
            if moneyReq:
                req += gameStrings.TEXT_JOBBOARDPROXY_249 % moneyReq
            fameReq = ''
            fameReq = self._getFameReq(data.get('needFame', (0, 0)))
            fameReq += self._getFameDetail(data.get('needFame', (0, 0)))
            if fameReq:
                fameReq = gameStrings.TEXT_JOBBOARDPROXY_255 % fameReq
            label = qData.get('jobDesc', gameStrings.TEXT_JOBBOARDPROXY_257)
            needJobScore = qData.get('needJobScore', ())
            awardFactor = qData.get('awardFactor', ())
            if needJobScore:
                maxValue = needJobScore[-1]
                jobScoreVar = qData.get('jobScoreVar', 'jobScoreVar%d' % questId)
                currentValue = BigWorld.player().questVars.get(jobScoreVar, 0)
                seperator = [ score * 1.0 / maxValue for score in needJobScore ]
                ratioTips = [ ratio for ratio in awardFactor ]
            else:
                maxValue = 100
                currentValue = 0
                seperator = []
                ratioTips = []
            award = []
            rewardMode = qData.get('reward', 0)
            rewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', 1)
            rewardStr = ''
            if rewardType == 1:
                rewardStr = gameStrings.TEXT_GUILDJOBPROXY_161
            else:
                rewardStr = gameStrings.TEXT_GUILDJOBPROXY_163
            exp, money, socExp, _ = commQuest.calcReward(BigWorld.player(), questId)
            money = int(money * self.bonusFactor) if money else 0
            if money > 0:
                award.append({'type': 'money',
                 'value': money,
                 'tip': rewardStr})
            exp = int(exp * self.bonusFactor) if exp else 0
            if exp > 0:
                award.append({'type': 'exp',
                 'value': exp,
                 'tip': gameStrings.TEXT_GUILDJOBPROXY_174})
            fames = qData.get('compFame', [])
            fameVal = 0
            fameTip = ''
            for fame in fames:
                fameVal = int(fame[1] * self.bonusFactor)
                fameTip = FD.data.get(fame[0], {}).get('name') if len(fame) else ''
                if fameVal > 0:
                    award.append({'type': 'fame',
                     'value': fameVal,
                     'tip': fameTip})

            actionTips = ''
            jobGroup = qData.get('jobGroup', 0)
            actions = JAD.data.get(jobGroup, {})
            jobIds = BigWorld.player().questData.get(questId, {}).get(const.QD_JOBS, [])
            for action in actions:
                if action.get('jobId', 0) in jobIds and action.get('visible', 0) == 1:
                    actionTips += '%s    +%s\n' % (action.get('name', ''), action.get('jobScore', 0))

            items = commQuest.genQuestRewardItems(BigWorld.player(), questId)
            item = []
            for itemId, itemAmount in items:
                path = uiUtils.getItemIconFile40(itemId)
                quality = ID.data.get(itemId, {}).get('quality', 1)
                item.append({'path': path,
                 'quality': quality,
                 'count': itemAmount,
                 'id': itemId})

            ret = {'canAccept': canAccept,
             'isAccepted': isAccepted,
             'title': title,
             'endTime': endTime,
             'desc': desc,
             'isFailed': isFail,
             'req': req,
             'maxValue': maxValue,
             'currentValue': currentValue,
             'label': label,
             'seperator': seperator,
             'award': award,
             'item': item,
             'jobId': self.curJobId,
             'ratioTips': ratioTips,
             'actionTips': actionTips,
             'fameReq': fameReq}
            return uiUtils.dict2GfxDict(ret, True)

    def setJobDetailInfo(self):
        if self.detailMed:
            self.detailMed.Invoke('setJobDetailInfo', self.createJobDetailInfo())

    def getAvailableJobs(self, entityId):
        self.entityId = entityId
        ent = BigWorld.entities.get(self.entityId)
        if not ent:
            return
        else:
            npcID = ent.npcId
            boardType = ND.data.get(npcID, {}).get('boardType', 2)
            if self.mediator == None and getattr(ent, 'jobTimeInfo', None):
                self.show(ent.jobRefId, ent.index, ent.version, ent.jobList, ent.jobTimeInfo, boardType, ent.bonusFactor)
            ent.cell.getAvailableJobs(getattr(ent, 'version', 0))
            return

    def startPolling(self):
        self.getAvailableJobs(self.entityId)
        if self.mediator:
            if self.pollingCallback:
                BigWorld.cancelCallback(self.pollingCallback)
            self.pollingCallback = BigWorld.callback(5, self.startPolling)

    def refreshJobBoardInfo(self, jobRefId, index, version, jobList, jobTimeInfo, bonusFactor):
        self.jobRefId = jobRefId
        self.index = index
        self.version = version
        self.jobList = jobList
        self.jobTimeInfo = jobTimeInfo
        self.bonusFactor = bonusFactor
        ent = BigWorld.entities.get(self.entityId)
        if ent:
            ent.index = index
            ent.version = version
            ent.jobList = jobList
            ent.jobTimeInfo = jobTimeInfo
            ent.bonusFactor = bonusFactor
        self.setJobBoardInfo()

    def onGetJobBoardInfo(self, *arg):
        ret = self.createJobBoardInfo()
        return ret

    def onReadJobDetail(self, *arg):
        jobId = int(arg[3][0].GetString())
        if not self.checkCanOpen(jobId):
            return
        self.isOpenByQuest = False
        questLoopId = JD.data.get(jobId, {}).get('questLoopId', 0)
        questId = QLD.data.get(questLoopId, {}).get('quests', [0])[0]
        if BigWorld.player().questData.has_key(questId):
            self.showDetail(jobId)
        else:
            ent = BigWorld.entities.get(self.entityId)
            if not ent:
                return
            ent.cell.getJobDetail(jobId)

    def openJobDetail(self, id):
        self.isOpenByQuest = True
        jobId = commQuest.getJobIdByQuest(id)
        questLoopId = JD.data.get(jobId, {}).get('questLoopId', 0)
        questId = QLD.data.get(questLoopId, {}).get('quests', [0])[0]
        if BigWorld.player().questData.has_key(questId):
            self.showDetail(jobId)
        else:
            BigWorld.player().cell.getJobDetail(0, jobId)

    def onCloseBoard(self, *arg):
        self.hide()

    def onGetJobDetailInfo(self, *arg):
        ret = self.createJobDetailInfo()
        return ret

    def onAcceptJob(self, *arg):
        jobId = int(arg[3][0].GetString())
        p = BigWorld.player()
        ent = BigWorld.entities.get(self.entityId)
        if not ent:
            return
        questLoopId = JD.data.get(jobId, {}).get('questLoopId', 0)
        questLoop = p.questLoopInfo.get(questLoopId)
        moneyReq = commQuest.getJobCashNeed(p, jobId)
        if questLoop and questLoop.questInfo:
            p.showGameMsg(GMDD.data.JOB_ACCEPTED, ())
            self.closeDetail()
            return
        if uiUtils.checkBindCashEnough(moneyReq, p.bindCash, p.cash, Functor(ent.cell.acceptJob, jobId)):
            ent.cell.acceptJob(jobId)

    def onGiveupJob(self, *arg):
        jobId = int(arg[3][0].GetString())
        questLoopId = JD.data.get(jobId, {}).get('questLoopId', 0)
        questId = QLD.data.get(questLoopId, {}).get('quests', [0])[0]
        p = BigWorld.player()
        if questId in p.quests:
            tStart, tEnd = p.getQuestData(questId, const.QD_JOB_TIME, (0, 0))
            if tStart < utils.getNow() < tEnd:
                msg = uiUtils.getTextFromGMD(GMDD.data.ABANDON_JOB_PUNISH_CONFIRM, gameStrings.TEXT_JOBBOARDPROXY_431)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % int(SCD.data.get('abandonJobPunishTime', 300) / 60), Functor(self.abandonQuest, int(questLoopId)))
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_JOBBOARDPROXY_434, Functor(self.abandonQuest, int(questLoopId)))

    def abandonQuest(self, questLoopId):
        BigWorld.player().cell.abandonQuestLoop(int(questLoopId))
        self.onCloseDetail()

    def onCloseDetail(self, *arg):
        self.closeDetail()
