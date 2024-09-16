#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/questLogProxy.o
from gamestrings import gameStrings
import types
import re
import Math
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
from gamestrings import gameStrings
import const
import gamelog
import formula
import commQuest
import utils
from guis import ui
from guis import uiConst
from ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiUtils
from guis import tipUtils
from guis import events
from guis import messageBoxProxy
from callbackHelper import Functor
from item import Item
from cdata import guild_func_prop_def_data as GFNPDD
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import quest_data as QD
from data import quest_group_data as QGD
from data import seeker_data as SD
from cdata import font_config_data as FCD
from data import quest_loop_data as QLD
from cdata import quest_delegation_inverted_data as QDID
from data import delegation_data as DELD
from data import map_config_data as MCD
from data import fame_data as FD
from data import game_msg_data as GMD
from cdata import quest_loop_inverted_data as QLID
from data import sys_config_data as SCD
from data import job_action_data as JAD
from data import bonus_data as BD
from data import quest_type_show_data as QTSD
from data import nf_npc_data as NND
ALL_QUEST_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_LILIAN,
 gametypes.QUEST_DISPLAY_TYPE_ZHUXIAN,
 gametypes.QUEST_DISPLAY_TYPE_SPCIAL,
 gametypes.QUEST_DISPLAY_TYPE_SCHOOL_LUCK,
 gametypes.QUEST_DISPLAY_TYPE_SCHOOL_ONCE,
 gametypes.QUEST_DISPLAY_TYPE_ZHIXIAN,
 gametypes.QUEST_DISPLAY_TYPE_SHIMEN,
 gametypes.QUEST_DISPLAY_TYPE_LOOP,
 gametypes.QUEST_DISPLAY_TYPE_CLUE,
 gametypes.QUEST_DISPLAY_TYPE_ACTIVITY,
 gametypes.QUEST_DISPLAY_TYPE_QI_WEN,
 gametypes.QUEST_DISPLAY_TYPE_MING_YANG)
INTRODUCTION_QUEST_DISPLAY_TYPE = (gametypes.QUEST_DISPLAY_TYPE_SPCIAL_RECEIVED, gametypes.QUEST_DISPLAY_TYPE_SPCIAL_AVALIA)
MAX_REGION_NUM = 20
WARN_COLOR = '#cc2929'

class QuestLogProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(QuestLogProxy, self).__init__(uiAdapter)
        self.bindType = 'questLogProxy'
        self.modelMap = {'getQuestList': self.onGetQuestList,
         'getQuestDetail': self.onGetQuestDetail,
         'clickCloseBtn': self.onClickCloseBtn,
         'abandonQuest': self.onAbandonQuest,
         'retryQuest': self.onRetryQuest,
         'setCheck': self.onSetCheck,
         'autoFindPath': self.onAutoFindPath,
         'showPosition': self.onShowPosition,
         'changeTab': self.onChangeTab,
         'getTooltip': self.onGetTooltip,
         'setQuestFlag': self.onSetQuestFlag,
         'getQuestTypeIdx': self.onGetQuestTypeIdx,
         'shareQuest': self.onShareQuest,
         'sendQuest': self.onSendQuest,
         'gotoTrack': self.onGotoTrack,
         'guildHelp': self.onGuildHelp,
         'getCategoryState': self.onGetCategoryState,
         'setCategoryState': self.onSetCategoryState,
         'transDelegation': self.onTransDelegation,
         'getDelegationInfo': self.onGetDelegationInfo,
         'confirmTrans': self.onConfirmTrans,
         'cancelTrans': self.onCancelTrans,
         'getTransCost': self.onGetTransCost,
         'acceptQuest': self.onAcceptQuest,
         'clearQuestProgress': self.onClearQuestProgress,
         'completeQuest': self.onCompleteQuest,
         'openPlay': self.onOpenPlay,
         'getTrackListShow': self.onGetTrackListShow,
         'setTrackListShow': self.onSetTrackListShow,
         'getAvailable': self.onGetAvailable}
        self.taskList = None
        self.taskDetail = None
        self.mediator = None
        self.isShow = False
        self.curTaskIdx = [0, 0]
        self.checkList = []
        self.flags = []
        self.taskListIdx = 1
        self.isAvailable = False
        self.isIntroduct = False
        self.isJob = False
        self.availabelList = None
        self.quests = []
        self.curTaskInfo = None
        self.retryQuestId = 0
        self.categoryState = [[ True for i in xrange(len(ALL_QUEST_DISPLAY_TYPE)) ],
         [ True for i in xrange(len(ALL_QUEST_DISPLAY_TYPE)) ],
         [ True for i in xrange(len(INTRODUCTION_QUEST_DISPLAY_TYPE)) ],
         [ True for i in xrange(MAX_REGION_NUM) ]]
        self.currentDid = []
        self.questList = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_TASK_LOG, self.hide)
        self.addEvent(events.EVENT_QUEST_COMPLETE, self.onQuestRemoved, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_ACCEPT, self.onQuestAdded, isGlobal=True)
        self.addEvent(events.EVENT_QUEST_ABANDON, self.onQuestRemoved, isGlobal=True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TASK_LOG:
            self.mediator = mediator
            ret = {}
            ret['questLogRecommDesc'] = SCD.data.get('questLogRecommDesc', '')
            self.updateCate()
            ret['retryFailedQuest'] = True
            if BigWorld.player().lv >= SCD.data.get('minPlayRecommLv', 20):
                ret['extraTaskLogName'] = SCD.data.get('extraTaskLogName', '')
            else:
                ret['extraTaskLogName'] = ''
            return uiUtils.dict2GfxDict(ret, True)

    def _asWidgetClose(self, widgetId, multiID):
        self.hide()

    def _createQuestListItem(self, taskInfo, item, questId, displayType):
        p = BigWorld.player()
        lv = taskInfo.get('recLv', 0)
        showLv = taskInfo.get('recLv', 0)
        name = taskInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
        inCheckList = item in self.checkList
        if p.lv > lv + 3:
            val = 'green'
        elif p.lv < lv - 3:
            val = 'red'
        else:
            val = 'yellow'
        extraComplete = commQuest.completeQuestExtraCheck(p, questId)
        isFinish = commQuest.completeQuestCheck(p, questId)
        self.questList.append(questId)
        return [showLv,
         name,
         item,
         inCheckList,
         val,
         questId,
         displayType,
         extraComplete,
         isFinish,
         False]

    def _createTutorialQuestList(self):
        p = BigWorld.player()
        ret = []
        displayType = gametypes.QUEST_DISPLAY_TYPE_SPCIAL
        info, checkList = BigWorld.player().fetchAcQuestsList(displayType)
        self.checkList += checkList
        self.checkList = list(set(self.checkList))
        arr = []
        ret = []
        for item in info:
            questId = item
            taskInfo = QD.data.get(item, {})
            arr.append(self._createQuestListItem(taskInfo, item, questId, displayType))

        ret.append(arr)
        availableArr = []
        availableQuests = p.fetchAvailableQuestsByType(displayType)
        for item in availableQuests:
            questId = item.get('questId', 0)
            if not p.availabelTutorialCheck(questId):
                continue
            taskInfo = QD.data.get(questId, {})
            questInfo = self._createQuestListItem(taskInfo, item, questId, displayType)
            questInfo.append(taskInfo.get('autoAc', 0))
            availableArr.append(questInfo)

        ret.append(availableArr)
        ret.append(0)
        return uiUtils.array2GfxAarry(ret, True)

    def _createQuestList(self):
        p = BigWorld.player()
        ret = []
        self.questList = []
        for displayType in ALL_QUEST_DISPLAY_TYPE:
            i = ALL_QUEST_DISPLAY_TYPE.index(displayType)
            info, checkList = BigWorld.player().fetchAcQuestsList(displayType)
            if displayType in (gametypes.QUEST_DISPLAY_TYPE_LOOP, gametypes.QUEST_DISPLAY_TYPE_SHIMEN):
                if self._isCurrentQuest(self._getCurTaskIdx(), info):
                    self.categoryState[0][i] = True
            self.checkList += checkList
            self.checkList = list(set(self.checkList))
            arr = []
            for item in info:
                if displayType in gametypes.QUEST_LOOP_DISPLAY_TYPES:
                    questId = p.questLoopInfo[item].getCurrentQuest()
                    if not questId:
                        name = QLD.data.get(item, {}).get('name', '') + gameStrings.TEXT_QUESTLOGPROXY_225
                        arr.append([0,
                         name,
                         item,
                         False,
                         'green',
                         item,
                         displayType,
                         False,
                         False,
                         True])
                        continue
                    else:
                        taskInfo = QD.data.get(questId, {})
                        if taskInfo.get('displayType', 0) == gametypes.QUEST_DISPLAY_TYPE_JOB:
                            continue
                elif displayType in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
                    questId = p.questLoopInfo[item].getCurrentQuest()
                    taskInfo = QD.data.get(questId, {})
                    cateIdx = ALL_QUEST_DISPLAY_TYPE.index(gametypes.QUEST_DISPLAY_TYPE_LOOP)
                    ret[cateIdx].append(self._createQuestListItem(taskInfo, item, questId, displayType))
                    continue
                else:
                    questId = item
                    taskInfo = QD.data.get(item, {})
                if self.isIntroduct:
                    if displayType != gametypes.QUEST_DISPLAY_TYPE_SPCIAL:
                        continue
                elif displayType == gametypes.QUEST_DISPLAY_TYPE_SPCIAL:
                    continue
                hideInLog = self.needHideQuestInLog(questId)
                if not hideInLog:
                    arr.append(self._createQuestListItem(taskInfo, item, questId, displayType))

            ret.append(arr)

        for questCate in ret:
            questCate.sort(key=lambda k: k[0])

        ret.append(self.getQuestShowInLog())
        return uiUtils.array2GfxAarry(ret, True)

    def getQuestShowInLog(self):
        p = BigWorld.player()
        questNum = 0
        for questId in p.quests:
            if self.needHideQuestInLog(questId):
                continue
            if self.isExceptInQuestNum(questId):
                continue
            questNum += 1

        return questNum

    def isExceptInQuestNum(self, questId):
        return QD.data.get(questId, {}).get('ignoreCnt', 0)

    def needHideQuestInLog(self, questId):
        hideInLog = QD.data.get(questId, {}).get('showAcceptQuestTracker', -1)
        if hideInLog >= 0:
            return not hideInLog
        displayType = QD.data.get(questId, {}).get('displayType', 0)
        if displayType > 0:
            hideInLog = QTSD.data.get(displayType, {}).get('showAcceptQuestTracker', False)
            return not hideInLog
        return False

    def _createJobList(self):
        p = BigWorld.player()
        ret = []
        info = {}
        self.questList = []
        quests, checkList = BigWorld.player().fetchAcQuestsList(gametypes.QUEST_DISPLAY_TYPE_JOB)
        self.checkList += checkList
        self.checkList = list(set(self.checkList))
        for item in quests:
            questId = p.questLoopInfo[item].getCurrentQuest()
            qData = QD.data.get(questId, {})
            displayType = qData.get('displayType', 0)
            if displayType != gametypes.QUEST_DISPLAY_TYPE_JOB:
                continue
            region = qData.get('region', gameStrings.TEXT_GAME_1747)
            lv = qData.get('recLv', 0)
            name = qData.get('name', gameStrings.TEXT_CHATPROXY_2514)
            inCheckList = item in self.checkList
            if p.lv > lv + 3:
                val = 'green'
            elif p.lv < lv - 3:
                val = 'red'
            elif p.lv >= lv - 3 and p.lv <= lv + 3:
                val = 'yellow'
            extraComplete = commQuest.completeQuestExtraCheck(p, questId)
            isFinish = commQuest.completeQuestCheck(p, questId)
            if not info.has_key(region):
                info[region] = []
            info[region].append([lv,
             name,
             item,
             inCheckList,
             val,
             questId,
             displayType,
             extraComplete,
             isFinish,
             False])
            self.questList.append(questId)

        for index, (region, questInfo) in enumerate(info.items()):
            if self._isCurrentQuest(self._getCurTaskIdx(), quests):
                self.categoryState[2][index] = True
            isExpand = self.categoryState[2][index]
            if isExpand:
                ret.append([region, questInfo])
            else:
                ret.append([region, []])

        ret.append(len(p.quests))
        return uiUtils.array2GfxAarry(ret, True)

    def onGetQuestList(self, *arg):
        self.isAvailable = arg[3][0].GetBool()
        self.isIntroduct = arg[3][1].GetBool()
        self.isJob = arg[3][2].GetBool()
        if not self.isAvailable:
            if not self.isJob:
                if self.isIntroduct:
                    return self._createTutorialQuestList()
                return self._createQuestList()
            else:
                return self._createJobList()
        else:
            BigWorld.player().fetchAvailableQuests()

    def setQuestList(self, info, loopInfo):
        p = BigWorld.player()
        i = 0
        if self.isAvailable:
            self.availabelList = info + loopInfo
            tmpList = []
            for item in info:
                tmpList.append([item[0], False])

            for item in loopInfo:
                tmpList.append([item[0], True])

            info = tmpList
        else:
            info = self.sortTaskList(info)
        ret = []
        self.questList = []
        self.info = info
        for displayType in ALL_QUEST_DISPLAY_TYPE:
            i = ALL_QUEST_DISPLAY_TYPE.index(displayType)
            isExpand = True
            if isExpand:
                arr = []
                for item in info:
                    if type(item) in (tuple, list):
                        isLoop = item[1]
                        item = item[0]
                    if isLoop and displayType in gametypes.QUEST_LOOP_DISPLAY_TYPES:
                        delId = QDID.data.get(item, 0)
                        if self.isAvailable and displayType in (gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION,) and delId not in p.delegations:
                            continue
                        taskInfo = QLD.data.get(item, {})
                        if taskInfo == {}:
                            continue
                        tp = commQuest.getQuestLoopDisplayType(item)
                        if tp != displayType:
                            continue
                        questLoopInfo = BigWorld.player().questLoopInfo.get(item, None)
                        loopIndex = -1
                        if questLoopInfo:
                            if questLoopInfo.isLastStep():
                                groupNum = taskInfo.get('groupNum', 0)
                                loopIndex = groupNum
                            else:
                                loopIndex = questLoopInfo.getNextLoopIndex()
                        if loopIndex <= 0:
                            if self.isAvailable and self.questLoopNeedHide(item):
                                continue
                            minLv = taskInfo.get('recLv', 0)
                            name = taskInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
                            autoAc = taskInfo.get('autoAc', 0)
                        else:
                            loopIndex = questLoopInfo.getNextLoopIndex()
                            loopIndex = loopIndex - 1
                            quests = taskInfo.get('quests', [])
                            item = quests[loopIndex]
                            if self.isAvailable and self.questNeedHide(item):
                                continue
                            taskInfo = QD.data.get(item, {})
                            minLv = taskInfo.get('recLv', 0)
                            name = taskInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
                            autoAc = taskInfo.get('autoAc', 0)
                        inCheckList = item in self.checkList
                        extraComplete = commQuest.completeQuestExtraCheck(p, item)
                        isFinish = commQuest.completeQuestLoopCheck(p, item)
                        posInfo = (False, 0)
                        arr.append([minLv,
                         name,
                         item,
                         inCheckList,
                         self.getQuestColor(minLv),
                         item,
                         displayType,
                         extraComplete,
                         isFinish,
                         False,
                         autoAc,
                         posInfo])
                    elif isLoop and displayType in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
                        taskInfo = QLD.data.get(item, {})
                        if taskInfo == {}:
                            continue
                        tp = commQuest.getQuestLoopDisplayType(item)
                        if tp != displayType:
                            continue
                        if self.isAvailable and self.questLoopNeedHide(item):
                            continue
                        minLv = taskInfo.get('recLv', 0)
                        name = taskInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
                        autoAc = taskInfo.get('autoAc', 0)
                        posInfo = (False, 0)
                        inCheckList = item in self.checkList
                        extraComplete = commQuest.completeQuestExtraCheck(p, item)
                        isFinish = commQuest.completeQuestLoopCheck(p, item)
                        ret[1].append([minLv,
                         name,
                         item,
                         inCheckList,
                         self.getQuestColor(minLv),
                         item,
                         displayType,
                         extraComplete,
                         isFinish,
                         False,
                         autoAc,
                         posInfo])
                        continue
                    elif not isLoop:
                        taskInfo = QD.data.get(item, {})
                        if taskInfo == {} or taskInfo.get('displayType') != displayType:
                            continue
                        if self.isAvailable and self.questNeedHide(item):
                            continue
                        lv = taskInfo.get('recLv', 0)
                        name = taskInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
                        autoAc = taskInfo.get('autoAc', 0)
                        inCheckList = item in self.checkList
                        val = self.getQuestColor(lv)
                        extraComplete = commQuest.completeQuestExtraCheck(p, item)
                        isFinish = commQuest.completeQuestCheck(p, item)
                        posInfo = (False, 0)
                        if i == ALL_QUEST_DISPLAY_TYPE.index(gametypes.QUEST_DISPLAY_TYPE_ZHIXIAN):
                            gameStrings.TEXT_QUESTLOGPROXY_458
                            acNpcTk = taskInfo.get('acNpcTk', 0)
                            posInfo = self.getDistanceFromAcNpc(acNpcTk)
                        arr.append([lv,
                         name,
                         item,
                         inCheckList,
                         val,
                         item,
                         displayType,
                         extraComplete,
                         isFinish,
                         False,
                         autoAc,
                         posInfo])
                        self.questList.append(item)

                ret.append(arr)
            else:
                ret.append([])

        for k in xrange(0, len(ret)):
            questCate = ret[k]
            if k == ALL_QUEST_DISPLAY_TYPE.index(gametypes.QUEST_DISPLAY_TYPE_ZHIXIAN) and len(questCate) > 0:
                ret.remove(questCate)
                questCate.sort(self.zhixianSort)
                gameStrings.TEXT_QUESTLOGPROXY_472
                questCate = self.limitZhixian(questCate)
                ret.insert(k, questCate)
            else:
                questCate.sort(key=lambda k: k[0], reverse=True)

        ret.append(len(p.quests))
        if self.mediator != None:
            self.mediator.Invoke('setQuestList', uiUtils.array2GfxAarry(ret, True))

    def getQuestColor(self, lv):
        p = BigWorld.player()
        val = 'yellow'
        if p.lv > lv + 3:
            val = 'green'
        elif p.lv < lv - 3:
            val = 'red'
        elif p.lv >= lv - 3 and p.lv <= lv + 3:
            val = 'yellow'
        return val

    def limitZhixian(self, quests):
        limit = SCD.data.get('zhixianLimit', 5)
        start = len(quests)
        for i in range(0, len(quests)):
            qst = quests[i]
            if qst[10] == 0:
                start = i
                break

        gameStrings.TEXT_QUESTLOGPROXY_503
        limit += start
        if limit < len(quests):
            lose = quests[limit:]
            quests = quests[0:limit]
            for item in lose:
                self.questList.remove(item[2])

        return quests

    def getDistanceFromAcNpc(self, acNpcTk):
        if acNpcTk == 0:
            return (False, 0)
        gameStrings.TEXT_QUESTLOGPROXY_517
        if type(acNpcTk) == types.TupleType:
            pass
        elif type(acNpcTk) == int:
            acNpcTk = (acNpcTk,)
        else:
            return (False, 0)
        return self.fromNearestNpc(acNpcTk)

    def fromNearestNpc(self, acNpc):
        minDis = -1
        sdd = SD.data
        p = BigWorld.player()
        myPos = p.position
        mySpaceNo = p.spaceNo
        for npc in acNpc:
            sd = sdd.get(npc, None)
            if sd is None:
                continue
            npcPos = (sd.get('xpos'), sd.get('ypos'), sd.get('zpos'))
            spaceNo = sd.get('spaceNo')
            if mySpaceNo == spaceNo:
                dist = (npcPos - myPos).lengthSquared
                minDis = dist if minDis < 0 else minDis
                minDis = dist if dist < minDis else minDis

        if minDis < 0:
            return (False, 0)
        else:
            return (True, minDis)

    def zhixianSort(self, first, second):
        """aotoAc sort """
        autoAc = 10
        ret = first[autoAc] - second[autoAc]
        if ret != 0:
            return -ret
        pos = 11
        ret = first[pos][0] - second[pos][0]
        if ret != 0:
            return -ret
        ret = first[pos][1] - second[pos][1]
        if ret != 0:
            if ret > 0:
                return 1
            return -1
        lv = 0
        ret = first[lv] - second[lv]
        if ret != 0:
            return -ret
        return 0

    def questNeedHide(self, questId):
        questIdFilter = SCD.data.get('questIdFilter', ())
        for startId, endId in questIdFilter:
            if questId >= startId and questId <= endId:
                return True

        questNeedShow = QD.data.get(questId, {}).get('showCanAcceptQuestTracker', -1)
        if questNeedShow >= 0:
            return not questNeedShow
        else:
            displayType = QD.data.get(questId, {}).get('displayType', 0)
            questNeedShow = QTSD.data.get(displayType, {}).get('showCanAcceptQuestTracker', False)
            return not questNeedShow

    def questLoopNeedHide(self, questLoopId):
        questLoopIdFilter = SCD.data.get('questLoopIdFilter', ())
        for startId, endId in questLoopIdFilter:
            if questLoopId >= startId and questLoopId <= endId:
                return True

        questNeedShow = QLD.data.get(questLoopId, {}).get('showCanAcceptQuestTracker', -1)
        if questNeedShow >= 0:
            return not questNeedShow
        else:
            displayType = QLD.data.get(questLoopId, {}).get('displayType', 0)
            questNeedShow = QTSD.data.get(displayType, {}).get('showCanAcceptQuestTracker', False)
            return not questNeedShow

    def onGetQuestDetail(self, *arg):
        taskId = int(arg[3][0].GetString())
        self._updateCurTaskIdx(taskId)
        self.taskListIdx = QD.data.get(taskId, {}).get('displayType', int(arg[3][1].GetNumber()))
        if self.taskListIdx in gametypes.QUEST_LOOP_DISPLAY_TYPES or self.taskListIdx in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
            if taskId not in BigWorld.player().questLoopInfo.keys():
                taskId = QLID.data.get(taskId, {}).get('questLoop', taskId)
            BigWorld.player().fetchQuestLoopDetail(taskId)
        else:
            BigWorld.player().fetchQuestDetail(taskId)

    def onSetCheck(self, *arg):
        idx = int(arg[3][0].GetString())
        idxSel = arg[3][1].GetBool()
        self.taskListIdx = int(arg[3][2].GetString())
        if self.taskListIdx in gametypes.QUEST_LOOP_DISPLAY_TYPES:
            idx = self._isCurrentQuest(idx, BigWorld.player().fetchAcQuestsList(self.taskListIdx)[0])
        displayType = gametypes.QUEST_DISPLAY_TYPE_LOOP if self.taskListIdx in gametypes.QUEST_LOOP_DISPLAY_TYPES else self.taskListIdx
        return GfxValue(self.setQuestTracked(idx, displayType, idxSel))

    def setQuestTracked(self, questId, displayType, tracked):
        BigWorld.player().cell.setQuestTracked(questId, displayType, tracked)
        if not tracked and questId in self.checkList:
            self.checkList.remove(questId)
        gameglobal.rds.sound.playSound(gameglobal.SD_98)
        if tracked and commQuest.getTrackedQuestNum(BigWorld.player()) >= const.QUEST_TRACK_NUM:
            BigWorld.player().showGameMsg(GMDD.data.QUEST_TRACK_FULL, ())
            if questId in self.checkList:
                self.checkList.remove(questId)
            return False
        return True

    def onClickCloseBtn(self, *arg):
        self.clearWidget()

    def showTaskLog(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_QUEST):
            return
        if self.mediator:
            self.mediator.Invoke('refreshTasklist')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TASK_LOG)
            self.isShow = True

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TASK_LOG)
        self.isShow = False
        self.mediator = None
        self.checkList = []
        self.questList = []

    def setTaskDetail(self, info):
        self.curTaskInfo = info
        if self.mediator != None:
            displayType = QD.data.get(info.get('id', 0), {}).get('displayType', 0)
            if displayType in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
                questDetail = self.gfxClueQuestDetail(info, displayType)
            else:
                questDetail = self.gfxQuestDetail(info)
            self.mediator.Invoke('setTaskDetail', (questDetail, GfxValue(self.taskListIdx)))

    def createItemInfo(self, item, showNum = True):
        p = BigWorld.player()
        it = Item(item[0])
        itemInfo = {}
        itemInfo['id'] = item[0]
        itemInfo['name'] = 'item'
        itemInfo['iconPath'] = uiUtils.getItemIconFile40(it.id)
        if showNum:
            itemInfo['count'] = item[1]
        if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            itemInfo['state'] = uiConst.EQUIP_NOT_USE
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        quality = ID.data.get(item[0], {}).get('quality', 1)
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo['color'] = qualitycolor
        return itemInfo

    def onGetAvailable(self, *args):
        questId = int(args[3][0].GetString())
        questType = int(args[3][1].GetNumber())
        loopId = 0
        if questType in gametypes.QUEST_LOOP_DISPLAY_TYPES:
            loopId = BigWorld.player().getAcceptedLoopIdByQuestId(questId)
        return GfxValue(self.getAvailable(questId, loopId))

    def getAvailable(self, questId, loopId = 0):
        p = BigWorld.player()
        if self.isAvailable:
            return self.isAvailable
        elif questId in p.quests or loopId in p.questLoopInfo:
            return False
        else:
            return True

    def gfxQuestDetail(self, info):
        p = BigWorld.player()
        taskPlace = info.get('taskPlace', '')
        if taskPlace:
            taskPlace = gameStrings.TEXT_TIANYUMALLPROXY_1486 + taskPlace + gameStrings.TEXT_ITEMQUESTPROXY_85_1
        taskName = info.get('taskName', '')
        desc = info.get('taskDesc', '')
        qData = QD.data.get(info.get('id'), {})
        canReAcc = qData.get('canReAcc', 1)
        bonusFactor = BigWorld.player().getQuestData(info.get('id'), const.QD_BONUS_FACTOR, 1.0)
        shortDesc = qData.get('shortDesc', '')
        additionalDesc = qData.get('additionalDesc', '')
        if self.isAvailable and qData.get('autoAc', 0):
            additionalDesc += '\n' + GMD.data.get(GMDD.data.AVAILABLE_QUEST_ACCEPT_NOTICE, {}).get('text', '')
        goal = []
        for item in info.get('taskGoal', []):
            goal.append([self._genDesc(item.get(const.QUEST_GOAL_DESC, ''), item.get(const.QUEST_GOAL_TYPE, True)),
             item.get(const.QUEST_GOAL_STATE, ''),
             item.get(const.QUEST_GOAL_TRACK_ID, ''),
             item.get(const.QUEST_GOAL_TRACK, ''),
             self._genRate(item.get(const.QUEST_GOAL_DESC, '')),
             item.get(const.QUEST_GOAL_TRACK_TYPE, ''),
             self.getPosition(item.get(const.QUEST_GOAL_TRACK_ID, '')),
             self.getMapName(str(item.get(const.QUEST_GOAL_TRACK_ID, ''))) + '/' + self.getPosition(str(item.get(const.QUEST_GOAL_TRACK_ID, ''))),
             item.get(const.QUEST_GOAL_GUILD_HELP, 0)])

        deliveryNpc = info.get('taskDeliveryNPC', '')
        deliveryNpcTk = info.get('taskDeliveryNPCTk', '')
        deliveryNpcTkType = info.get('taskDeliveryNPCTkType', 0)
        deliveryNpcPos = self.getPosition(deliveryNpcTk)
        award = self._getAward(info, False, bonusFactor)
        isFailed = commQuest.questFailCheck(BigWorld.player(), info['id'])
        isCompleted = commQuest.completeQuestCheck(BigWorld.player(), info['id'])
        moneyUp = info.get('moneyUp', False)
        expUp = info.get('expUp', False)
        timeOut = info.get('timeOut', -1)
        orRelation = qData.get('condRelation', 0)
        questId = info.get('id', 0)
        isLoop = False
        loopId = info.get('loopId', -1)
        if loopId != -1:
            isLoop = True
        if isLoop:
            qld = QLD.data.get(loopId, {})
            if qld.get('isZhuXie', 0):
                canShare = False
            else:
                canShare = qld.get('teamQuest', 0)
        else:
            canShare = qData.get('shareQuest', 0)
        loopInfo = info.get('loopInfo', '')
        deliveryNpcPosition = self.getMapName(str(deliveryNpcTk)) + '/' + self.getPosition(str(deliveryNpcTk))
        showPlayBtn = qData.get('showPlayBtn', 0)
        progressLabel = qData.get('jobDesc', gameStrings.TEXT_JOBBOARDPROXY_257)
        needJobScore = qData.get('needJobScore', ())
        awardFactor = qData.get('awardFactor', ())
        if needJobScore:
            progressMaxValue = needJobScore[-1]
            jobScoreVar = qData.get('jobScoreVar', 'jobScoreVar%d' % questId)
            progressCurrentValue = BigWorld.player().questVars.get(jobScoreVar, 0)
            progressSeperator = [ score * 1.0 / progressMaxValue for score in needJobScore ]
            progressRatioTips = [ ratio for ratio in awardFactor ]
        else:
            progressMaxValue = 100
            progressCurrentValue = 0
            progressSeperator = []
            progressRatioTips = []
        progressActionTips = ''
        jobGroup = qData.get('jobGroup', 0)
        actions = JAD.data.get(jobGroup, {})
        jobIds = BigWorld.player().questData.get(questId, {}).get(const.QD_JOBS, [])
        for action in actions:
            if action.get('jobId', 0) in jobIds and action.get('visible', 0) == 1:
                progressActionTips += '%s    +%s\n' % (action.get('name', ''), action.get('jobScore', 0))

        arr = {'taskPlace': taskPlace,
         'taskName': taskName,
         'taskDesc': desc,
         'taskGoal': goal,
         'questId': questId,
         'loopId': loopId,
         'canShare': canShare,
         'taskDeliveryNPC': deliveryNpc,
         'taskDeliveryNPCTk': deliveryNpcTk,
         'deliveryNpcTkType': deliveryNpcTkType,
         'deliveryNpcPos': deliveryNpcPos,
         'taskAward': award,
         'isFailed': isFailed,
         'moneyUp': moneyUp,
         'expUp': expUp,
         'timeOut': timeOut,
         'orRelation': orRelation,
         'canAccept': 0,
         'canClear': 0,
         'additionalDesc': additionalDesc,
         'loopInfo': loopInfo,
         'deliveryNpcPosition': deliveryNpcPosition,
         'isCompleted': isCompleted,
         'canComplete': 0,
         'showPlayBtn': showPlayBtn,
         'shortDesc': shortDesc,
         'progressLabel': progressLabel,
         'progressMaxValue': progressMaxValue,
         'progressCurrentValue': progressCurrentValue,
         'progressSeperator': progressSeperator,
         'progressRatioTips': progressRatioTips,
         'progressActionTips': progressActionTips,
         'canReAcc': canReAcc}
        arr['canAccept'] = QD.data.get(info['id'], {}).get('autoAc', 0)
        arr['canClear'] = QLD.data.get(info['loopId'], {}).get('abProgressType', 0)
        arr['canComplete'] = QD.data.get(info['id'], {}).get('canComplete', 0) and isCompleted
        arr['isAccepted'] = not self.getAvailable(info['id'], info['loopId'])
        return uiUtils.dict2GfxDict(arr, True)

    def gfxClueQuestDetail(self, info, displayType = gametypes.QUEST_DISPLAY_TYPE_CLUE):
        p = BigWorld.player()
        taskPlace = info.get('taskPlace', '')
        if taskPlace:
            taskPlace = gameStrings.TEXT_TIANYUMALLPROXY_1486 + taskPlace + gameStrings.TEXT_ITEMQUESTPROXY_85_1
        taskName = info.get('taskName', '')
        desc = info.get('taskDesc', '')
        qData = QD.data.get(info.get('id'), {})
        shortDesc = QLD.data.get(info.get('loopId', 0), {}).get('desc', '')
        additionalDesc = qData.get('additionalDesc', '')
        if self.isAvailable and qData.get('autoAc', 0):
            additionalDesc += '\n' + GMD.data.get(GMDD.data.AVAILABLE_QUEST_ACCEPT_NOTICE, {}).get('text', '')
        goal = []
        loopInfo = BigWorld.player().questLoopInfo.get(info.get('loopId', 0), None)
        questInfo = loopInfo.questInfo if loopInfo else []
        for goalId, goalState in questInfo:
            if displayType == gametypes.QUEST_DISPLAY_TYPE_FENG_WU:
                goalDesc = QD.data.get(goalId, {}).get('markerNpcsMsg', '')
            else:
                goalDesc = QD.data.get(goalId, {}).get('shortDesc', '')
            trackId = -1
            canTrack = False
            rateDesc = ''
            canUseFly = False
            trackPos = ''
            trackMapName = ''
            goal.append([goalDesc,
             goalState,
             trackId,
             canTrack,
             rateDesc,
             canUseFly,
             trackPos,
             trackMapName])

        deliveryNpc = ''
        deliveryNpcTk = ''
        deliveryNpcTkType = 0
        deliveryNpcPos = ''
        lastQuestId = commQuest.getLastQuestInLoop(info.get('loopId', 0))
        exp, money, _, _ = commQuest.calcReward(p, lastQuestId, info.get('loopId', 0))
        items = commQuest.genQuestRewardItems(p, lastQuestId)
        itemList = []
        for item in items:
            itemList.append(self.createItemInfo(item))

        choiceList = []
        for item in info.get('rewardChoice', []):
            choiceList.append(self.createItemInfo(item))

        extraItemList = []
        for item in info.get('extraItems', []):
            extraItemList.append(self.createItemInfo(item))

        loopItems = []
        isLoop = False
        loopId = info.get('loopId', -1)
        curLoopCnt = self.getQuestLoopCnt(loopId)
        if loopId != -1:
            isLoop = True
            items = commQuest.getQuestLoopRewardItem(BigWorld.player(), info.get('loopId', -1))
            for item in items:
                loopItems.append(self.createItemInfo(item, False))

            if curLoopCnt <= 1:
                items = commQuest.getQuestFirstLoopRewardItem(BigWorld.player(), info.get('loopId', -1))
                for item in items:
                    loopItems.append(self.createItemInfo(item, False))

        award = self._getAward(info, True)
        isFailed = commQuest.questFailCheck(BigWorld.player(), info['id'])
        isCompleted = commQuest.completeQuestCheck(BigWorld.player(), info['id'])
        moneyUp = info.get('moneyUp', False)
        expUp = info.get('expUp', False)
        timeOut = info.get('timeOut', -1)
        orRelation = qData.get('condRelation', 0)
        questId = info.get('id', 0)
        canShare = QLD.data.get(info['loopId'], {}).get('teamQuest', 0) if isLoop else qData.get('shareQuest', 0)
        loopInfo = ''
        if isFailed:
            deliveryNpcTk = qData.get('acNpcTk', 0)
            deliveryNpcTkType = BigWorld.player()._filterCommitTrackType(qData, gametypes.TRACK_TYPE_NPC_AC)
        deliveryNpcPosition = self.getMapName(str(deliveryNpcTk)) + '/' + self.getPosition(str(deliveryNpcTk))
        showPlayBtn = qData.get('showPlayBtn', 0)
        arr = {'taskPlace': taskPlace,
         'taskName': taskName,
         'taskDesc': desc,
         'taskGoal': goal,
         'questId': questId,
         'loopId': loopId,
         'canShare': canShare,
         'taskDeliveryNPC': deliveryNpc,
         'taskDeliveryNPCTk': deliveryNpcTk,
         'deliveryNpcTkType': deliveryNpcTkType,
         'deliveryNpcPos': deliveryNpcPos,
         'taskAward': award,
         'isFailed': isFailed,
         'moneyUp': moneyUp,
         'expUp': expUp,
         'timeOut': timeOut,
         'orRelation': orRelation,
         'canAccept': 0,
         'canClear': 0,
         'additionalDesc': additionalDesc,
         'loopInfo': loopInfo,
         'deliveryNpcPosition': deliveryNpcPosition,
         'isCompleted': isCompleted,
         'canComplete': 0,
         'showPlayBtn': showPlayBtn,
         'shortDesc': shortDesc}
        arr['canAccept'] = QD.data.get(info['id'], {}).get('autoAc', 0)
        arr['canClear'] = QLD.data.get(info['loopId'], {}).get('abProgressType', 0)
        arr['canComplete'] = QD.data.get(info['id'], {}).get('canComplete', 0) and isCompleted
        arr['isAccepted'] = not self.getAvailable(info['id'], info['loopId'])
        return uiUtils.dict2GfxDict(arr, True)

    def _getGuildQuestRewardFactor(self, questId, gqrtype):
        guild = BigWorld.player().guild
        if not guild:
            return 1
        d = QLID.data.get(questId)
        if not d:
            return 1
        questLoopId = d.get('questLoop', 0)
        if not questLoopId:
            return 1
        return 1 + guild.getAbility(GFNPDD.data.QUEST_REWARD, (questLoopId, gqrtype)) + guild.getAbility(GFNPDD.data.QUEST_REWARD_ALL, questLoopId)

    def _getAward(self, info, isLoop = False, bonusFactor = 1):
        p = BigWorld.player()
        qData = QD.data.get(info.get('id'), {})
        rewardList = []
        questId = info.get('id', 0)
        exp, money, _, xiuwei = commQuest.calcReward(p, questId, info.get('loopId', 0))
        taskAward = info.get('taskAward', {})
        if not isLoop:
            money = taskAward.get('money', 0)
            exp = taskAward.get('exp', 0)
        if not money:
            money = 0
        if not exp:
            exp = 0
        cashRewardType = taskAward.get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
        money = int(money * self._getGuildQuestRewardFactor(info.get('id'), gametypes.GUILD_QUEST_REWARD_MONEY))
        exp = int(exp * self._getGuildQuestRewardFactor(info.get('id'), gametypes.GUILD_QUEST_REWARD_EXP))
        if money != 0:
            if cashRewardType == 1:
                rewardList.append(('cash', int(money * bonusFactor)))
            elif cashRewardType == 2:
                rewardList.append(('bindCash', int(money * bonusFactor)))
        if exp != 0:
            rewardList.append(('exp', exp))
        if xiuwei != 0:
            rewardList.append(('lingshi', xiuwei))
        fameList = qData.get('compFame', [])
        fameAwardFactor = commQuest.getQuestLoopAwardFactorByType(p, info.get('loopId', 0), gametypes.QUEST_REWARD_CREDIT)
        for fame in fameList:
            fameTip = FD.data.get(fame[0], {}).get('name') if len(fame) else ''
            fameName = SCD.data.get('fameIdToBonusDict', {}).get(fame[0], 'fame')
            if self.isAvailable and qData.get('displayType', 0) == gametypes.QUEST_DISPLAY_TYPE_LOOP:
                rewardList.append((fameName, taskAward.get('fame', {}).get(fame[0], 0), fameTip))
            else:
                rewardList.append((fameName, int(fame[1] * bonusFactor * fameAwardFactor), fameTip))

        for event in qData.get('comEvent', []):
            eventFun, eventArgs = event[0], event[1]
            if eventFun == 'addPFriendlyNF':
                for npcPId, rewardCnt in eventArgs[0]:
                    fameName = gameStrings.NPF_FAVOR % NND.data.get(npcPId, {}).get('name', '')
                    rewardList.append(('fame', rewardCnt, fameName))

        guildReward = qData.get('guildReward', 0)
        if guildReward != 0:
            rewardList.append(('guildReward', guildReward))
        guildBuildMarkerRewards = qData.get('guildBuildMarkerRewards', [])
        if len(guildBuildMarkerRewards) > 0:
            rewardList.append(('guildBuildMarkerRewards', guildBuildMarkerRewards[0][1]))
        guildAreaRewards = qData.get('guildAreaRewards', [])
        if len(guildAreaRewards) > 0:
            rewardList.append(('guildAreaRewards', guildAreaRewards[0][1]))
        guildDevMarkerRewards = qData.get('guildDevMarkerRewards', [])
        if len(guildDevMarkerRewards) > 0:
            rewardList.append(('guildDevMarkerRewards', guildDevMarkerRewards[0][1]))
        guildContribution = qData.get('guildContribution', 0)
        if guildContribution != 0:
            guildContribution = commQuest.calcQuestLoopGuildContri(p, questId, guildContribution)
            rewardList.append(('guildContribution', guildContribution))
        intimacyReward = qData.get('intimacyReward', 0)
        if intimacyReward != 0:
            rewardList.append(('qinmi', intimacyReward))
        extraRewardList = []
        extraMoney = info.get('taskAward', {}).get('extraMoney', 0)
        if extraMoney and extraMoney != 0:
            if cashRewardType == 1:
                extraRewardList.append(('cash', int(extraMoney * bonusFactor)))
            elif cashRewardType == 2:
                extraRewardList.append(('bindCash', int(extraMoney * bonusFactor)))
        extraExp = info.get('taskAward', {}).get('extraExp', 0)
        if extraExp and extraExp != 0:
            extraRewardList.append(('exp', extraExp))
        itemList = []
        if not qData.get('rewardItemsRate', 0):
            for item in info.get('taskAward', {}).get('icon', []):
                itemList.append(self.createItemInfo(item))

        choiceList = []
        for item in info.get('rewardChoice', []):
            choiceList.append(self.createItemInfo(item))

        extraItemList = []
        for item in info.get('extraItems', []):
            extraItemList.append(self.createItemInfo(item))

        groupHeaderItemList = []
        for item in info.get('groupHeaderItems', []):
            groupHeaderItemList.append(self.createItemInfo(item))

        if qData.get('triggerPartial', 0):
            progress, rewardId, prop = commQuest.getRewardByQuestProgress(p, questId)
            fixedBonus = BD.data.get(rewardId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus and type(fixedBonus) == tuple:
                for bType, bId, bNum in fixedBonus:
                    if bType == gametypes.BONUS_TYPE_GUILD_CONTRIBUTION:
                        rewardList.append(('guildContribution', bNum))
                    elif bType == gametypes.BONUS_TYPE_ITEM:
                        itemList.append(self.createItemInfo([bId, bNum], True))

        loopItems = []
        isLoop = False
        loopId = info.get('loopId', -1)
        curLoopCnt = self.getQuestLoopCnt(loopId)
        if loopId != -1:
            isLoop = True
            items = commQuest.getQuestLoopRewardItem(BigWorld.player(), info.get('loopId', -1))
            for item in items:
                loopItems.append(self.createItemInfo(item, False))

            if curLoopCnt <= 1:
                items = commQuest.getQuestFirstLoopRewardItem(BigWorld.player(), info.get('loopId', -1))
                for item in items:
                    loopItems.append(self.createItemInfo(item, False))

        award = {'rewardList': rewardList,
         'extraRewardList': extraRewardList,
         'icon': itemList,
         'choiceIcon': choiceList,
         'extraItems': extraItemList,
         'loopItems': loopItems,
         'groupHeaderItems': groupHeaderItemList}
        return award

    def getQuestLoopCnt(self, loopId):
        p = BigWorld.player()
        info = p.questLoopInfo.get(loopId, None)
        if info:
            if info.getCurrentQuest():
                curLoop = info.getCurrentStep() + 1
            else:
                curLoop = info.getCurrentStep()
            curLoopCnt = info.loopCnt + 1
        else:
            curLoop = 0
            curLoopCnt = 1
        return curLoopCnt

    @ui.callFilter(uiConst.SERVER_CALL_ABANDONTASK)
    def onRetryQuest(self, *arg):
        idx = int(arg[3][0].GetString())
        displayType = QD.data.get(idx, {}).get('displayType', 0)
        if displayType == gametypes.QUEST_DISPLAY_TYPE_LOOP:
            return
        self.retryQuestId = idx
        self.abandonQuest(BigWorld.player(), idx)

    @ui.callFilter(uiConst.SERVER_CALL_ABANDONTASK)
    def onAbandonQuest(self, *arg):
        idx = int(arg[3][0].GetString())
        p = BigWorld.player()
        if p.inCombat:
            p.showGameMsg(GMDD.data.ABABDON_QUEST_FAIL_IN_COMBAT, ())
            return
        elif utils.isInBusinessZaiju(p):
            p.showGameMsg(GMDD.data.ABABDON_QUEST_FAIL_IN_BUSINESS_ZAIJU, ())
            return
        else:
            displayType = QD.data.get(idx, {}).get('displayType', 0)
            if displayType in gametypes.QUEST_LOOP_DISPLAY_TYPES or displayType in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
                questId = idx
                idx = QLID.data.get(questId, {}).get('questLoop', questId)
                if questId == None:
                    return
                isteleport = p.checkTeleport(questId, 3)
                if displayType in (gametypes.QUEST_DISPLAY_TYPE_LOOP_DELEGATION,):
                    if idx:
                        delId = QDID.data.get(idx)
                    else:
                        delId = QDID.data.get(questId)
                    gamelog.debug('@zhp onAbandonDelegation', delId)
                    if delId and p.hasDelegationData(delId, const.DD_FAIL):
                        nextShowId = self._getNextShowId()
                        p.cell.abandonDelegation(delId)
                        self._updateCurTaskIdx(nextShowId)
                    else:
                        msg = gameStrings.TEXT_QUESTLOGPROXY_1116
                        if isteleport:
                            msg = gameStrings.TEXT_QUESTLOGPROXY_1118
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.abandonDelegation, p, int(questId if self.isAvailable else idx)))
                elif isteleport:
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.abandonQuestLoop, p, int(idx))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
                    gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_QUESTLOGPROXY_1123, buttons)
                else:
                    if self.abandonPunish(questId, idx):
                        return
                    nextShowId = self._getNextShowId()
                    p.cell.abandonQuestLoop(int(idx))
                    self.refreshTaskList()
                    self._updateCurTaskIdx(nextShowId)
            elif self.checkLastGroupQuest(idx):
                msg = GMD.data.get(GMDD.data.CONFIRM_ABANDON_LAST_QUEST, {}).get('text', gameStrings.TEXT_QUESTLOGPROXY_1133)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.abandonCommonQuest, p, idx))
            else:
                self.abandonCommonQuest(p, idx)
            return

    def checkLastGroupQuest(self, questId):
        questGroup = QD.data.get(questId, {}).get('questGroup', 0)
        if not questGroup:
            return False
        quests = QGD.data.get(questGroup, {}).get('quests', [])
        return len(quests) > 0 and questId == quests[-1]

    def abandonCommonQuest(self, p, idx):
        isteleport = p.checkTeleport(int(idx), 3)
        if isteleport:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.abandonQuest, p, int(idx))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_QUESTLOGPROXY_1123, buttons)
        else:
            isAuto = QD.data.get(int(idx), {}).get('autoAc', 0)
            if isAuto:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_QUESTLOGPROXY_1155, Functor(self.abandonQuest, p, int(idx)))
            else:
                nextShowId = self._getNextShowId()
                p.cell.abandonQuest(int(idx))
                self.refreshTaskList()
                self._updateCurTaskIdx(nextShowId)

    def _getNextShowId(self):
        nextShowId = 0
        if self._getCurTaskIdx() in self.questList:
            nextIndex = self.questList.index(self._getCurTaskIdx()) + 1
            if nextIndex < len(self.questList):
                nextShowId = self.questList[nextIndex]
        return nextShowId

    def refreshTaskList(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshTasklist', GfxValue(self.taskListIdx))

    def onShowPosition(self, *arg):
        id = arg[3][0].GetString()
        mapName = gbk2unicode(self.getMapName(id))
        position = self.getPosition(id)
        return GfxValue(mapName + '/' + position)

    def getPosition(self, id):
        if not id:
            return ''
        try:
            id = eval(id)
        except:
            return ''

        p = BigWorld.player()
        if type(id) == types.TupleType:
            idList = list(id)
            minDis = -1
            index = 0
            for item in idList:
                data = SD.data.get(item, None)
                if data:
                    pos = Math.Vector3(data.get('xpos', 0), data.get('ypos', 0), data.get('zpos', 0))
                    spaceNo = data['spaceNo']
                    if p.spaceNo == spaceNo:
                        tempDis = (p.position - pos).length
                        if minDis == -1 or minDis > tempDis:
                            minDis = tempDis
                            index = item

            id = index
            if id == 0 and len(idList) > 0:
                id = idList[0]
        if id == 0:
            return ''
        elif SD.data.has_key(id):
            sd = SD.data.get(id, {})
            return '%d , %d, %d' % (sd.get('xpos', 0), sd.get('zpos', 0), sd.get('ypos', 0))
        else:
            return ''

    def getMapName(self, id):
        if not id:
            return ''
        try:
            id = eval(id)
        except:
            return ''

        p = BigWorld.player()
        if type(id) == types.TupleType:
            idList = list(id)
            minDis = -1
            index = 0
            for item in idList:
                data = SD.data.get(item, None)
                if data:
                    pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                    spaceNo = data['spaceNo']
                    if p.spaceNo == spaceNo:
                        tempDis = (p.position - pos).length
                        if minDis == -1 or minDis > tempDis:
                            minDis = tempDis
                            index = item

            id = index
            if id == 0 and len(idList) > 0:
                id = idList[0]
        if id == 0:
            return ''
        elif SD.data.has_key(id):
            spaceNo = formula.getMapId(SD.data.get(id, {}).get('spaceNo', 0))
            return MCD.data.get(spaceNo, {}).get('name', '')
        else:
            return ''

    def onAutoFindPath(self, *arg):
        id = arg[3][0].GetString()
        uiUtils.findPosWithAlert(id)
        gameglobal.rds.sound.playSound(gameglobal.SD_98)

    def taskListCmp(self, item1, item2):
        if item1[1] == item2[1]:
            if item1[2] == item2[2]:
                if item1[3] < item2[3]:
                    return -1
                if item1[3] > item2[3]:
                    return 1
                return 0
            elif item1[2] < item2[2]:
                return -1
            elif item1[2] > item2[2]:
                return 1
            else:
                return 0
        else:
            if item1[1] < item2[1]:
                return -1
            if item1[1] > item2[1]:
                return 1
            return 0

    def sortTaskList(self, info):
        ret = []
        for item in info:
            questInfo = QD.data.get(item[0], {})
            recLv = questInfo.get('recLv', 0)
            acMinLv = questInfo.get('acMinLv', recLv)
            name = questInfo.get('name', gameStrings.TEXT_CHATPROXY_2514)
            ret.append([item,
             recLv,
             acMinLv,
             name])

        ret.sort(self.taskListCmp)
        res = []
        for item in ret:
            res.append(item[0])

        return res

    def getTaskBonus(self, taskId):
        exp, cash, socExp, _ = commQuest.calcReward(BigWorld.player(), taskId)
        if not exp:
            exp = 0
        if not cash:
            cash = 0
        return (exp, cash)

    def abandonDelegation(self, target, questLoopId):
        gamelog.debug('@zhp abandonDelegation', questLoopId)
        delId = QDID.data.get(questLoopId)
        if delId:
            nextShowId = self._getNextShowId()
            target.cell.abandonDelegation(delId)
            self._updateCurTaskIdx(nextShowId)

    def abandonQuestLoop(self, target, idNum):
        nextShowId = self._getNextShowId()
        target.cell.abandonQuestLoop(idNum)
        self.refreshTaskList()
        self._updateCurTaskIdx(nextShowId)

    def abandonQuest(self, target, idNum):
        nextShowId = self._getNextShowId()
        target.cell.abandonQuest(idNum)
        self.refreshTaskList()
        self._updateCurTaskIdx(nextShowId)

    def onChangeTab(self, *arg):
        self.isAvailable = arg[3][0].GetBool()
        self.isIntroduct = arg[3][1].GetBool()
        self.isJob = arg[3][2].GetBool()
        self.updateCate()

    def updateCate(self):
        if self.isAvailable:
            cateName = SCD.data.get('questCateName', (gameStrings.TEXT_QUESTLOGPROXY_1326,
             gameStrings.TEXT_QUESTLOGPROXY_1326_1,
             gameStrings.TEXT_QUESTLOGPROXY_1326_2,
             gameStrings.TEXT_QUESTLOGPROXY_1326_3,
             gameStrings.TEXT_QUESTLOGPROXY_1326_4,
             gameStrings.TEXT_QUESTLOGPROXY_1326_5))
            cateTypes = ALL_QUEST_DISPLAY_TYPE
        elif self.isIntroduct:
            cateName = SCD.data.get('tutorialQuestCateName', (gameStrings.TEXT_QUESTLOGPROXY_1330, gameStrings.TEXT_QUESTLOGPROXY_1330_1))
            cateTypes = INTRODUCTION_QUEST_DISPLAY_TYPE
        else:
            cateName = SCD.data.get('questCateName', (gameStrings.TEXT_QUESTLOGPROXY_1326,
             gameStrings.TEXT_QUESTLOGPROXY_1326_1,
             gameStrings.TEXT_QUESTLOGPROXY_1326_2,
             gameStrings.TEXT_QUESTLOGPROXY_1326_3,
             gameStrings.TEXT_QUESTLOGPROXY_1326_4,
             gameStrings.TEXT_QUESTLOGPROXY_1326_5))
            cateTypes = ALL_QUEST_DISPLAY_TYPE
        if self.mediator:
            self.mediator.Invoke('updateCate', (uiUtils.array2GfxAarry(cateName, True), uiUtils.array2GfxAarry(cateTypes, True)))

    def onGetTooltip(self, *arg):
        idx = int(arg[3][0].GetString())
        return tipUtils.getItemTipById(idx)

    def abandonPunish(self, questId, questLoopId = -1):
        if questLoopId == -1:
            return False
        qld = QLD.data.get(questLoopId, {})
        loopInfo = BigWorld.player().questLoopInfo.get(questLoopId, None)
        if not qld or not loopInfo:
            return False
        abandonCD = qld.get('abandonCD', -1)
        abandonItemRm = qld.get('abandonItemRm', [])
        abandonCashRm = qld.get('abandonCashRm', -1)
        abandonType = qld.get('abandonType', 1)
        step = len(loopInfo.questInfo)
        if step > 0 and loopInfo.questInfo[-1][1] == False:
            step -= 1
        avlAbandonCnt = max(0, loopInfo.avlAcCnt - qld.get('avlAcCnt', 0) + step)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.abandonQuestLoop, BigWorld.player(), int(questLoopId))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        title = ''
        if abandonCD != -1:
            title += gameStrings.TEXT_PUZZLEPROXY_465 % abandonCD
        if abandonItemRm != []:
            title += gameStrings.TEXT_PUZZLEPROXY_468 % (ID.data.get(abandonItemRm[0], {}).get('name', gameStrings.TEXT_GAME_1747), abandonItemRm[1])
        if abandonCashRm != -1:
            title += gameStrings.TEXT_PUZZLEPROXY_471 % abandonCashRm
        if abandonType != gametypes.QUEST_LOOP_ABANDON_TYPE_ONE:
            if abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_TWO:
                title += gameStrings.TEXT_PUZZLEPROXY_475 % max(avlAbandonCnt, 0)
            elif abandonType == gametypes.QUEST_LOOP_ABANDON_TYPE_THREE:
                title += gameStrings.TEXT_QUESTLOGPROXY_1378 + uiUtils.toHtml(gameStrings.TEXT_QUESTLOGPROXY_1378_1, WARN_COLOR) + gameStrings.TEXT_QUESTLOGPROXY_1378_2
        qd = QD.data.get(questId, {})
        if qd.has_key('businessLv'):
            title += uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_QUEST_GIVE_UP, '')
        if title:
            title = uiUtils.toHtml(gameStrings.TEXT_IMPQUEST_4705, WARN_COLOR) + title
            gameglobal.rds.ui.messageBox.show(True, '', title, buttons)
            return True
        else:
            return False

    def _genDesc(self, desc, isNormal):
        ret = re.sub(gameStrings.TEXT_QUESTTRACKPROXY_231, '', desc)
        if not isNormal:
            ret = gameStrings.TEXT_QUESTLOGPROXY_1393 + ret
        return ret

    def _genRate(self, desc):
        ret = re.findall(gameStrings.TEXT_QUESTTRACKPROXY_231, desc)
        if len(ret) > 0:
            ret = ret[0]
        else:
            ret = ''
        return ret

    def checkNewQuest(self):
        newQuests = set(BigWorld.player().quests) - set(self.quests)
        if not newQuests:
            return
        for item in newQuests:
            if commQuest.isQuestDisable(item):
                continue

    def onSetQuestFlag(self, *arg):
        pass

    def onGetQuestTypeIdx(self, *arg):
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(self.isAvailable))
        ret.SetElement(1, GfxValue(self.taskListIdx))
        taskIdx = self._getCurTaskIdx()
        ret.SetElement(2, GfxValue(taskIdx))
        ret.SetElement(3, GfxValue(self.isJob))
        ret.SetElement(4, GfxValue(self.isIntroduct))
        return ret

    def _getCurTaskIdx(self):
        taskIdx = 0
        if self.isAvailable:
            taskIdx = self.curTaskIdx[1]
        else:
            taskIdx = self.curTaskIdx[0]
        return taskIdx

    def _updateCurTaskIdx(self, idx):
        if self.isAvailable:
            self.curTaskIdx[1] = idx
        else:
            self.curTaskIdx[0] = idx

    def onShareQuest(self, *arg):
        idx = int(arg[3][0].GetNumber())
        isLoop = int(arg[3][1].GetBool())
        gamelog.debug('onShareQuest', idx)
        if not idx:
            return
        if isLoop:
            BigWorld.player().cell.shareQuestLoop(idx)
        else:
            BigWorld.player().cell.shareQuest(idx)

    def onSendQuest(self, *arg):
        idx = int(arg[3][0].GetString())
        if self.taskListIdx in gametypes.QUEST_LOOP_DISPLAY_TYPES:
            return
        qd = QD.data.get(idx, {})
        taskName = qd.get('name', gameStrings.TEXT_ITEMQUESTPROXY_87)
        color = FCD.data['quest', 0]['color']
        msg = "<font color=\'%s\'>[<a href = \'event:task%s\'><u>%s</u></a>]</font>" % (color, str(idx), str(taskName))
        gameglobal.rds.ui.sendLink(msg)

    def onGotoTrack(self, *arg):
        trackId = arg[3][1].GetString()
        trackId = uiUtils.findTrackId(trackId)
        uiUtils.gotoTrack(trackId)

    def onGuildHelp(self, *arg):
        questId = int(arg[3][0].GetString())
        BigWorld.player().cell.seekGuildHelpOnQuest(questId)

    def onGetCategoryState(self, *arg):
        if self.isAvailable:
            states = self.categoryState[1]
        elif self.isJob:
            states = self.categoryState[3]
        elif self.isIntroduct:
            states = self.categoryState[2]
        else:
            states = self.categoryState[0]
        return uiUtils.array2GfxAarry(states)

    def onSetCategoryState(self, *arg):
        arrSize = arg[3][0].GetArraySize()
        self.taskListIdx = int(arg[3][1].GetNumber())
        for i in xrange(arrSize):
            state = arg[3][0].GetElement(i).GetBool()
            if self.isAvailable:
                self.categoryState[1][i] = state
            elif self.isJob:
                self.categoryState[3][i] = state
            elif self.isIntroduct:
                self.categoryState[2][i] = state
            else:
                self.categoryState[0][i] = state

    def _isCurrentQuest(self, curQuestId, info):
        for item in info:
            if not BigWorld.player().questLoopInfo.has_key(item):
                continue
            questId = BigWorld.player().questLoopInfo[item].getCurrentQuest()
            if curQuestId == questId:
                return item

        return 0

    def onTransDelegation(self, *arg):
        self.currentDid = arg[3][0].GetNumber()

    def onGetDelegationInfo(self, *arg):
        dData = DELD.data.get(self.currentDid)
        result = [0,
         0,
         0,
         0]
        if dData:
            p = BigWorld.player()
            result = [self.currentDid,
             dData.get('rank'),
             p.cash,
             p.bindCash]
        return uiUtils.array2GfxAarry(result)

    @ui.callFilter(1)
    def onConfirmTrans(self, *arg):
        did = arg[3][0].GetNumber()
        agentDuration = arg[3][1].GetNumber()
        cash = arg[3][2].GetNumber()
        BigWorld.player().cell.transmitDelegation(did, agentDuration, cash)

    @ui.callFilter(1)
    def onCancelTrans(self, *arg):
        did = arg[3][0].GetNumber()
        BigWorld.player().cell.abandonAgentDelegation(did)

    def onGetTransCost(self, *arg):
        t = arg[3][0].GetNumber()
        did = arg[3][1].GetNumber()
        return GfxValue(commQuest.calcCommissionCash(BigWorld.player(), did, t))

    @ui.callFilter(1)
    def onAcceptQuest(self, *arg):
        idx = int(arg[3][0].GetString())
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_QUESTLOGPROXY_1550, Functor(self._acceptQuest, idx))

    def _acceptQuest(self, questId):
        BigWorld.player().cell.autoAcceptQuest(questId)
        self._updateCurTaskIdx(self._getNextShowId())

    @ui.callFilter(1)
    def onClearQuestProgress(self, *arg):
        questId = int(arg[3][0].GetString())
        if self.isAvailable:
            loopId = questId
        else:
            loopId = QLID.data.get(questId, {}).get('questLoop', 0)
        abProgressType = QLD.data.get(loopId, {}).get('abProgressType', gametypes.QUEST_LOOP_ABANDON_PROGRESS_ONE)
        msg = ''
        if abProgressType == gametypes.QUEST_LOOP_ABANDON_PROGRESS_TWO:
            msg = gameStrings.TEXT_QUESTLOGPROXY_1566
        elif abProgressType == gametypes.QUEST_LOOP_ABANDON_PROGRESS_THREE:
            msg = gameStrings.TEXT_QUESTLOGPROXY_1568
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.abandonQuestLoopProgress, loopId))

    def _getMsg(self, msgId, defaultMsg = ''):
        gmMsg = GMD.data.get(msgId, {})
        return gmMsg.get('text', defaultMsg)

    @ui.callFilter(1)
    def onCompleteQuest(self, *arg):
        questId = int(arg[3][0].GetString())
        rewardChoice = int(arg[3][1].GetNumber())
        if rewardChoice < 0:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)]
            msg = self._getMsg(GMDD.data.QUEST_REWARD_CHOICE_PROMPT, gameStrings.TEXT_QUESTLOGPROXY_1583)
            gameglobal.rds.ui.messageBox.show(False, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
            BigWorld.player().showGameMsg(GMDD.data.QUEST_NEED_SELECT_PRIZE, ())
            return
        questLoopId = QLID.data.get(questId, {}).get('questLoop', -1)
        if questLoopId > 0:
            BigWorld.player().cell.completeQuestLoopWithoutNpc(questLoopId, ['rewardChoice'], [rewardChoice])
        else:
            BigWorld.player().cell.completeQuestWithoutNpc(questId, ['rewardChoice'], [rewardChoice])

    @ui.callFilter(1)
    def onOpenPlay(self, *arg):
        gameglobal.rds.ui.playRecomm.show()

    def onQuestRemoved(self, event = None):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
            if questLoopId:
                displayType = commQuest.getQuestLoopDisplayType(questLoopId)
                if displayType == gametypes.QUEST_DISPLAY_TYPE_ACTIVITY:
                    pushDataList = self.uiAdapter.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST)
                    if pushDataList:
                        for data in pushDataList:
                            if data.get('data', 0) == questId:
                                self.uiAdapter.pushMessage.removeData(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST, data)
                                break

            self._updateCurTaskIdx(self._getNextShowId())
            if questId == self.retryQuestId:
                self._acceptQuest(questId)
                self.retryQuestId = 0
            if questId in SCD.data.get('lifeSkillQuestIds', ()):
                self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_LIFE_SKILL_LV_UP)
            return

    def onQuestAdded(self, event = None):
        if event is None:
            return
        else:
            questId = event.data.get('questId', 0)
            self.checkActivityQuesetAdded(questId)
            self.curTaskIdx[0] = questId
            return

    def checkActivityQuesetAdded(self, questId):
        questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
        if not questLoopId:
            return
        displayType = commQuest.getQuestLoopDisplayType(questLoopId)
        if displayType != gametypes.QUEST_DISPLAY_TYPE_ACTIVITY:
            return
        pushDataList = self.uiAdapter.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST)
        hasPushed = False
        if pushDataList:
            for data in pushDataList:
                if data.get('data', 0) == questId:
                    hasPushed = True

        if not hasPushed:
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST, {'data': questId})

    def checkActivityQuestAccepted(self):
        questLoopInfo = getattr(BigWorld.player(), 'questLoopInfo', None)
        if not questLoopInfo:
            return
        else:
            for questLoopVal in questLoopInfo.values():
                self.checkActivityQuesetAdded(questLoopVal.getCurrentQuest())

            return

    def onClickActivityQuestPush(self):
        data = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST)
        if not data:
            return
        self.uiAdapter.pushMessage.removeData(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST, data)
        self.taskListIdx = gametypes.QUEST_DISPLAY_TYPE_ACTIVITY
        self.isAvailable = False
        self.isJob = False
        self._updateCurTaskIdx(data.get('data', 0))
        self.showTaskLog()

    def resetData(self):
        self.curTaskIdx = [0, 0]

    def onGetTrackListShow(self, *arg):
        isTrackListShow = gameglobal.rds.ui.questTrack.isTrackListShow()
        return GfxValue(isTrackListShow)

    def onSetTrackListShow(self, *arg):
        needShow = bool(arg[3][0].GetBool())
        gameglobal.rds.ui.questTrack.hideTrackPanel(not needShow)

    def setTrackListShow(self, show):
        if not self.mediator:
            return
        self.mediator.Invoke('setTrackStatus', GfxValue(show))
