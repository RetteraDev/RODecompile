#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAchievement.o
import gameglobal
import BigWorld
import gametypes
from guis import uiConst
from helpers import loadingProgress
from data import achievement_data as AD
from cdata import game_msg_def_data as GMDD

class ImpAchievement(object):

    def resSetAchievement(self, achieveTargets, achieves, achievePoint):
        gameglobal.rds.ui.achvment.achievePoint = achievePoint
        gameglobal.rds.ui.achvment.achieveTargets = achieveTargets
        gameglobal.rds.ui.achvment.achieves = {achieveId:date for achieveId, date, _ in achieves}
        gameglobal.rds.ui.achvment.show()

    def resSetOtherAchievement(self, achieveTargets, achieves):
        gameglobal.rds.ui.achvmentDiff.otherAchieveTargets = achieveTargets
        gameglobal.rds.ui.achvmentDiff.otherAchieves = {achieveId:date for achieveId, date, _ in achieves}
        gameglobal.rds.ui.achvmentDiff.show()

    def resAchievementDone(self, achieveId):
        gameglobal.rds.ui.achvment.gainedAchieveIds.append(achieveId)
        gameglobal.rds.ui.guideGoal.refreshTabInfo()
        gameglobal.rds.ui.guideGoal.refreshLeftTabInfo(False)
        if loadingProgress.instance().inLoading:
            self.afterLoadShowAchievement = True
        data = AD.data.get(achieveId)
        if data and data.has_key('bonusId'):
            msgType = data.get('msgType', 0)
            if msgType == gametypes.ACHIEVE_MSG_FUBEN:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_SPECIAL_AWD, data.get('bonusId'))})
                if hasattr(self, 'specialAwardAchieves'):
                    self.specialAwardAchieves.append(achieveId)
            elif msgType == gametypes.ACHIEVE_MSG_COMMON:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD, {'data': achieveId})
            elif msgType == gametypes.ACHIEVE_MSG_NOT_PUSH:
                gameglobal.rds.ui.guideGoal.checkPushMsg(achieveId)

    def onGetFinalAchieveAward(self):
        pass

    def onGetAchieveAward(self, achieveId):
        if achieveId == gameglobal.rds.ui.achievePush.achieveId:
            gameglobal.rds.ui.achievePush.hide()
        if achieveId in AD.data and AD.data[achieveId].get('msgType', 0) == gametypes.ACHIEVE_MSG_COMMON:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD, {'data': achieveId})
        gameglobal.rds.ui.guideGoal.updateGetAwardedInfo({achieveId: True})

    def onQueryAwardAchieves(self, awardAchieves, specialAwardAchieves):
        self.specialAwardAchieves = specialAwardAchieves
        for achieveId in awardAchieves:
            data = AD.data.get(achieveId)
            if not data:
                continue
            msgType = data.get('msgType', 0)
            if msgType == gametypes.ACHIEVE_MSG_COMMON:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD, {'data': achieveId})
            elif msgType == gametypes.ACHIEVE_MSG_NOT_PUSH:
                gameglobal.rds.ui.guideGoal.checkPushMsg(achieveId)

        for achieveId in specialAwardAchieves:
            data = AD.data.get(achieveId)
            if not data:
                continue
            msgType = data.get('msgType', 0)
            if msgType == gametypes.ACHIEVE_MSG_FUBEN and data.get('bonusId', 0):
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_SPECIAL_AWD, data.get('bonusId'))})
            elif msgType == gametypes.ACHIEVE_MSG_NOT_PUSH:
                gameglobal.rds.ui.guideGoal.checkPushMsg(achieveId)

    def _hasSpecialAwardAchieve(self, specialAwardId):
        if not hasattr(self, 'specialAwardAchieves'):
            return False
        for achieveId in self.specialAwardAchieves:
            ad = AD.data.get(achieveId)
            if ad and ad.get('bonusId') == specialAwardId:
                return True

        return False

    def onSendAchieveScore(self, data):
        self.achieveScores = data

    def onGainAchieveScore(self, achieveId):
        self.achieveScores.append(achieveId)
        gameglobal.rds.ui.achievementScore.updateAchieveStatus(achieveId)

    def onUpdateAchieveScoreAward(self, aid, value):
        self.achieveScoreAward[aid] = value
        gameglobal.rds.ui.achievementScore.updateAwardStatus(aid)

    def onNoviceBoostAchieveUpdated(self, d):
        gameglobal.rds.ui.newbieGuideExam.setInfo(d)
        gameglobal.rds.ui.newbieGuideExam.refreshInfo()
        gameglobal.rds.ui.newbieGuide.refreshView()

    def onSendDoneAchieveIds(self, achieveIds):
        gameglobal.rds.ui.achvment.gainedAchieveIds = achieveIds
        gameglobal.rds.ui.guideGoal.refreshTabInfo()
        gameglobal.rds.ui.guideGoal.refreshLeftTabInfo(False)

    def onGetOtherPlayerNoviceBoostSucc(self, gbId, info, level):
        print '[@zqc ImpAchievement.onGetOtherPlayerNoviceBoostSucc:103] ', locals()
        gameglobal.rds.ui.newbieGuideExam.showOther(info, level)

    def onGetOtherPlayerNoviceBoostFail(self, gbId):
        print '[@zqc ImpAchievement.onGetOtherPlayerNoviceBoostFail:106] ', locals()
        BigWorld.player().showGameMsg(GMDD.data.TARGET_OFFLINE, ())

    def onQueryAchievesGetAwarded(self, awardInfo):
        gameglobal.rds.ui.guideGoal.updateGetAwardedInfo(awardInfo)
