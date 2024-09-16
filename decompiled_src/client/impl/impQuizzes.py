#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impQuizzes.o
from gamestrings import gameStrings
import gamelog
import gametypes
import gameglobal
import const
from cdata import game_msg_def_data as GMDD

class ImpQuizzes(object):
    """
    \xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe6\x9a\xb4\xe9\x9c\xb2\xe6\x8e\xa5\xe5\x8f\xa3\xef\xbc\x9a
    self.base.queryQuizzesJoinedInfo() \xe7\x82\xb9\xe5\xbc\x80\xe6\x8a\xa5\xe5\x90\x8d\xe9\x9d\xa2\xe6\x9d\xbf\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x8a\xa5\xe5\x90\x8d\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x9a\xe5\xb7\xb2\xe6\x8a\xa5\xe5\x90\x8d\xe4\xba\xba\xe6\x95\xb0\xef\xbc\x8c\xe8\x87\xaa\xe5\xb7\xb1\xe6\x98\xaf\xe5\x90\xa6\xe6\x8a\xa5\xe8\xbf\x87\xe5\x90\x8d
    self.base.queryQuizzesJoinedNum() \xe5\xae\x9a\xe6\x97\xb6\xe6\x9f\xa5\xe8\xaf\xa2\xe5\xb7\xb2\xe6\x8a\xa5\xe5\x90\x8d\xe4\xba\xba\xe6\x95\xb0
    self.base.joinQuizzes() \xe5\x8f\x82\xe5\x8a\xa0\xe6\x8a\xa5\xe5\x90\x8d
    self.base.commitQuizzesAnswer(curRound, answerId) \xe6\x8f\x90\xe4\xba\xa4\xe7\xad\x94\xe6\xa1\x88
    self.base.queryQuizzesRoundResult(curRound)  \xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe9\x80\x9a\xe7\x9f\xa5\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\x9c\xac\xe5\x9b\x9e\xe5\x90\x88\xe7\xad\x94\xe9\xa2\x98\xe5\x80\x92\xe8\xae\xa1\xe6\x97\xb6\xe7\xbb\x93\xe6\x9d\x9f, \xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\xa0\xb9\xe6\x8d\xae\xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c
    self.base.queryQuizzesInfo() \xe6\xb4\xbb\xe5\x8a\xa8\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad\xe7\x8e\xa9\xe5\xae\xb6\xe7\x82\xb9\xe5\xbc\x80\xe6\xb4\xbb\xe5\x8a\xa8\xe9\x9d\xa2\xe6\x9d\xbf\xef\xbc\x8c\xe6\x9f\xa5\xe8\xaf\xa2\xe5\xbd\x93\xe5\x89\x8d\xe7\xad\x94\xe9\xa2\x98\xe4\xbf\xa1\xe6\x81\xaf:\xe6\xb4\xbb\xe5\x8a\xa8\xe9\x98\xb6\xe6\xae\xb5\xe3\x80\x81\xe5\x89\xa9\xe4\xbd\x99\xe4\xba\xba\xe6\x95\xb0\xe3\x80\x81\xe5\xbd\x93\xe5\x89\x8d\xe5\x9b\x9e\xe5\x90\x88\xe6\x95\xb0\xe3\x80\x81\xe9\x97\xae\xe9\xa2\x98\xe6\x8f\x8f\xe8\xbf\xb0\xe3\x80\x81\xe9\x80\x89\xe9\xa1\xb9\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x8c
    \xe5\x90\x84\xe9\x80\x89\xe9\xa1\xb9\xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0\xe3\x80\x81\xe6\x9c\xac\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c\xe3\x80\x81\xe7\xad\x94\xe9\xa2\x98\xe7\x8a\xb6\xe6\x80\x81\xe3\x80\x81\xe7\x89\xb9\xe6\xae\x8a\xe9\xa2\x98\xe5\xa5\x96\xe5\x8a\xb1\xe3\x80\x81\xe6\x9c\x80\xe7\xbb\x88\xe6\xb7\x98\xe6\xb1\xb0\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0
    self.cell.chatToQuizzes(msg, channel) \xe5\x8f\x91\xe9\x80\x81\xe5\xbc\xb9\xe5\xb9\x95\xe6\xb6\x88\xe6\x81\xaf\xef\xbc\x9a\xe6\x99\xae\xe9\x80\x9a\xe3\x80\x81\xe4\xb8\x96\xe7\x95\x8c\xe3\x80\x81\xe5\x8f\xb7\xe8\xa7\x92
    self.base.queryQuizzesActivityId() \xe6\x9f\xa5\xe8\xaf\xa2\xe5\xbd\x93\xe5\x89\x8d\xe6\xb4\xbb\xe5\x8a\xa8ID
    self.base.queryQuizzesOverInfo() \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\x80\xe7\xbb\x88\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c
    """

    def onPushQuizzesStage(self, stage, nextStageTimestamp):
        """
        \xe6\x8e\xa8\xe9\x80\x81\xe5\xbd\x93\xe5\x89\x8d\xe7\x9a\x84\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81
        :param stage: \xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81
        :return:
        """
        gamelog.debug('@zhangkuo onPushQuizzesStage [stage]', stage)
        if stage == gametypes.QUIZZES_ACTIVITY_STAGE_OPEN:
            gameglobal.rds.ui.yunChuiQuizzesApply.pushApplyMessage()
        elif stage == gametypes.QUIZZES_ACTIVITY_STAGE_READY:
            gameglobal.rds.ui.yunChuiQuizzesApply.removeApplyPushMsg()
            if gameglobal.rds.ui.yunChuiQuizzesApply.widget:
                gameglobal.rds.ui.yunChuiQuizzesApply.hide()
        elif stage == gametypes.QUIZZES_ACTIVITY_STAGE_OVER:
            self.base.queryQuizzesOverInfo()
        elif stage == gametypes.QUIZZES_ACTIVITY_STAGE_NOT_OPEN:
            gameglobal.rds.ui.yunChuiQuizzes.afterQuizzesOver()
        gameglobal.rds.ui.yunChuiQuizzesPush.setActivityState(stage, nextStageTimestamp)
        gameglobal.rds.ui.yunChuiQuizzesApply.setActivityState(stage)

    def onQueryQuizzesJoinedInfo(self, isJoined, joinedNum, activityId):
        """
        \xe7\x82\xb9\xe5\x87\xbb\xe6\x8a\xa5\xe5\x90\x8d\xe9\x9d\xa2\xe6\x9d\xbf\xef\xbc\x8c\xe6\x98\xbe\xe7\xa4\xba\xe5\xb7\xb2\xe6\x8a\xa5\xe5\x90\x8d\xe4\xba\xba\xe6\x95\xb0\xef\xbc\x8c\xe8\x87\xaa\xe5\xb7\xb1\xe6\x98\xaf\xe5\x90\xa6\xe6\x8a\xa5\xe5\x90\x8d
        :param isJoined:
        :param joinedNum:
        :return:
        """
        gameglobal.rds.ui.yunChuiQuizzesApply.setInfo(isJoined, joinedNum, activityId)
        gameglobal.rds.ui.yunChuiQuizzesApply.show()
        gamelog.debug('@zhangkuo onQueryQuizzesJoinedInfo [isJoined] [joinedNum] [activityId]', isJoined, joinedNum, activityId)

    def onQueryQuizzesJoinedNum(self, joinedNum):
        """
        \xe5\xae\x9a\xe6\x97\xb6\xe6\x9f\xa5\xe8\xaf\xa2\xe5\xb7\xb2\xe6\x8a\xa5\xe5\x90\x8d\xe4\xba\xba\xe6\x95\xb0\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param joinedNum: \xe5\xb7\xb2\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0
        :return:
        """
        if gameglobal.rds.ui.yunChuiQuizzes.widget:
            gameglobal.rds.ui.yunChuiQuizzes.setApplyNum(joinedNum)
        gamelog.debug('@zhangkuo onQueryQuizzesJoinedNum [joinedNum]', joinedNum)

    def onQuizzesJoined(self):
        """
        \xe6\x8a\xa5\xe5\x90\x8d\xe6\x88\x90\xe5\x8a\x9f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :return:
        """
        gameglobal.rds.ui.yunChuiQuizzesApply.isJoined = True
        gameglobal.rds.ui.yunChuiQuizzesApply.refreshInfo()
        gamelog.debug(gameStrings.TEXT_IMPQUIZZES_81)

    def onQuizzesRoundStart(self, data):
        """
        \xe4\xb8\x80\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe5\xbc\x80\xe5\xa7\x8b\xe4\xb8\x8b\xe5\x8f\x91\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae
        :param data:
        :return:
        """
        gameglobal.rds.ui.yunChuiQuizzes.onQuizzesRoundStart(data)
        gamelog.debug('@zhangkuo onQuizzesRoundStart [curRound] [questionDesc]', data[0], data[1])
        for desc in data[2]:
            gamelog.debug('@zhangkuo optionDesc:', desc)

        curRound = data[0]
        gameglobal.rds.ui.yunChuiQuizzes.setCurRound(curRound)
        gameglobal.rds.ui.yunChuiQuizzesPush.setCurRound(curRound)

    def onQuizzesRoundOver(self):
        """
        \xe4\xb8\x80\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9d\x9f\xef\xbc\x8c\xe9\x80\x9a\xe7\x9f\xa5\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\x9f\xa5\xe8\xaf\xa2\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c
        :return:
        """
        gamelog.debug('@zhangkuo onQuizzesRoundOver')
        if gameglobal.rds.ui.yunChuiQuizzes.widget:
            curRound = gameglobal.rds.ui.yunChuiQuizzes.getCurRound()
            self.base.queryQuizzesRoundResult(curRound)

    def onQueryQuizzesRoundResult(self, answerResult, remainNum, selectedRatio, rightAnswerId, myAnswerId, nextStageStamp):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9c\xac\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param answerResult: \xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c \xe8\xaf\xa6\xe7\xbb\x86\xe8\xaf\xb4\xe6\x98\x8e\xe8\xa7\x81gametypes.py QUIZZES_ANSWER_RIGHT\xe7\x9b\xb8\xe5\x85\xb3
        :param remainNum: \xe5\x89\xa9\xe4\xbd\x99\xe4\xba\xba\xe6\x95\xb0
        :param selectedRatio: \xe5\x90\x84\xe9\x80\x89\xe9\xa1\xb9\xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0\xe7\x9a\x84\xe6\xaf\x94\xe4\xbe\x8b
        :return:
        """
        gameglobal.rds.ui.yunChuiQuizzes.onQueryQuizzesRoundResult(answerResult, remainNum, selectedRatio, rightAnswerId, myAnswerId, nextStageStamp)
        gamelog.debug('@zhangkuo onQuizzesRoundResult [answerResult] [remainNum] [selectedRatio] [rightAnswerId] [myAnswerId]', answerResult, remainNum, str(selectedRatio), rightAnswerId, myAnswerId)

    def onQueryQuizzesInfo(self, quizzesInfo):
        """
        \xe6\xb4\xbb\xe5\x8a\xa8\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad\xe7\x82\xb9\xe5\xbc\x80\xe6\xb4\xbb\xe5\x8a\xa8\xe9\x9d\xa2\xe6\x9d\xbf\xe6\x9f\xa5\xe7\x9c\x8b\xe5\xbd\x93\xe5\x89\x8d\xe6\xb4\xbb\xe5\x8a\xa8\xef\xbc\x8c\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param quizzesInfo:
        :return:
        """
        activityStage = quizzesInfo.get(gametypes.QUIZZES_INFO_ACTIVITY_STAGE)
        quizzesState = quizzesInfo.get(gametypes.QUIZZES_INFO_QUIZZES_STATE)
        activityId = quizzesInfo.get(gametypes.QUIZZES_INFO_ACTIVITY_ID)
        gameglobal.rds.ui.yunChuiQuizzes.setCurActivityId(activityId)
        gameglobal.rds.ui.yunChuiQuizzes.setQuizzesInfo(activityId, quizzesInfo)
        if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_NOT_OPEN or activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_OPEN:
            self.showGameMsg(GMDD.data.QUIZZES_NOT_READY, ())
            gamelog.debug('@zhangkuo onQueryQuizzesInfo:stage = ', quizzesInfo)
        else:
            gameglobal.rds.ui.yunChuiQuizzes.show()
            if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_OVER:
                answerResult = quizzesInfo.get(gametypes.QUIZZES_INFO_ANSWER_RESULT)
                succeedNum = quizzesInfo.get(gametypes.QUIZZES_INFO_REMAIN_NUM)
                failedNum = quizzesInfo.get(gametypes.QUIZZES_INFO_FAILED_NUM)
                specialReward = quizzesInfo.get(gametypes.QUIZZES_INFO_SPECIAL_REWARD)
                gameglobal.rds.ui.yunChuiQuizzesPush.successNum = succeedNum
                gamelog.debug('@zhangkuo onQueryQuizzesInfo:stage over [answerResult] [succeedNum] [failedNum] [specialReward]', answerResult, succeedNum, failedNum, str(specialReward))
            else:
                nextStageStamp = quizzesInfo.get(gametypes.QUIZZES_INFO_NEXT_STAGE_TIMESTAMP)
                remainNum = quizzesInfo.get(gametypes.QUIZZES_INFO_REMAIN_NUM)
                curRound = quizzesInfo.get(gametypes.QUIZZES_INFO_CUR_ROUND)
                questionDesc = quizzesInfo.get(gametypes.QUIZZES_INFO_QUESTION_DESC)
                optionDesc = quizzesInfo.get(gametypes.QUIZZES_INFO_OPTION_DESC)
                failedQuestionIndex = quizzesInfo.get(gametypes.QUIZZES_INFO_FAILED_QUESTION_INDEX)
                commitedAnswerId = quizzesInfo.get(gametypes.QUIZZES_INFO_COMMITED_ANSWER_ID)
                gamelog.debug('@zhangkuo onQueryQuizzesInfo:stage start [remain] [curRound] [questionDesc] [optionDesc] [failedQuestionIndex] [commitedAnswerId]', remainNum, curRound, questionDesc, str(optionDesc), failedQuestionIndex, commitedAnswerId)
                if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_ROUND_OVER:
                    optionSelectedNum = quizzesInfo.get(gametypes.QUIZZES_INFO_OPTION_SELECTED_NUM)
                    answerResult = quizzesInfo.get(gametypes.QUIZZES_INFO_ANSWER_RESULT)
                    rightAnswerId = quizzesInfo.get(gametypes.QUIZZES_INFO_RIGHT_ANSWER_ID)
                    gamelog.debug('@zhangkuo onQueryQuizzesInfo:stage round over [optionSelectedNum] [answerResult]', str(optionSelectedNum), answerResult)

    def onQuizzesOver(self, specialReward, succeedNum, failedNum, answerResult):
        """
        \xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe8\xbd\xae\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9d\x9f
        :param specialReward: \xe7\xad\x94\xe5\xaf\xb9\xe7\x9a\x84\xe7\x89\xb9\xe6\xae\x8a\xe9\xa2\x98\xe7\x9a\x84index\xe5\x92\x8c\xe5\xaf\xb9\xe5\xba\x94\xe5\xb9\xb3\xe5\x88\x86\xe7\x9a\x84\xe5\xa5\x96\xe5\x8a\xb1\xef\xbc\x8c\xe5\x9b\xba\xe5\xae\x9a\xe5\xa5\x96\xe5\x8a\xb1\xe6\xa0\xb9\xe6\x8d\xaeindex\xe6\x9f\xa5\xe8\xa1\xa8
        :param succeedNum: \xe9\x80\x9a\xe5\x85\xb3\xe4\xba\xba\xe6\x95\xb0
        :param failedNum: \xe6\x9c\xaa\xe9\x80\x9a\xe5\x85\xb3\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0
        :param answerResult: \xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe9\xa2\x98\xe7\x9a\x84\xe7\xad\x94\xe9\xa2\x98\xe7\xbb\x93\xe6\x9e\x9c
        :return:
        """
        result = [specialReward,
         succeedNum,
         failedNum,
         answerResult]
        gameglobal.rds.ui.yunChuiQuizzesPush.successNum = succeedNum
        gameglobal.rds.ui.yunChuiQuizzes.onQuizzesOver(specialReward, succeedNum, failedNum, answerResult)
        gamelog.debug('@zhangkuo [specialReward] [succeedNum] [failedNum] [answerResult]', specialReward, succeedNum, failedNum, answerResult)

    def onChatToQuizzes(self, channel, srcRole, msg, gbId):
        """
        \xe5\x8f\x91\xe9\x80\x81\xe7\x9a\x84\xe5\xbc\xb9\xe5\xb9\x95\xe6\xb6\x88\xe6\x81\xaf
        :param useType:\xe6\xb6\x88\xe6\x81\xaf\xe7\xb1\xbb\xe5\x9e\x8b, const.CHAT_CHANNEL_QUIZZES_HAOJIAO\xe7\x9b\xb8\xe5\x85\xb3
        :param msg: \xe6\xb6\x88\xe6\x81\xaf\xe5\x86\x85\xe5\xae\xb9
        :return:
        """
        if channel == const.CHAT_CHANNEL_QUIZZES_HAOJIAO:
            msg = srcRole + ':' + msg
        gameglobal.rds.ui.yunChuiQuizzes.onChatToQuizzes(channel, msg)
        gamelog.debug('@zhangkuo onChatToQuizzes [channel] [msg] [roleName]', channel, msg, srcRole)

    def onQueryQuizzesActivityId(self, activityId):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\xb4\xbb\xe5\x8a\xa8ID\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c \xe4\xb8\xba0\xe8\xa1\xa8\xe7\xa4\xba\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x9c\xaa\xe5\xbc\x80\xe6\x94\xbe
        :param activityId:
        :return:
        """
        gamelog.debug('@zhangkuo onQueryQuizzesActivityId [activityId]', activityId)
        gameglobal.rds.ui.yunChuiQuizzesPush.setCurActivityId(activityId)
