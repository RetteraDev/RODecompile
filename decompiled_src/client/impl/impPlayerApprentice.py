#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerApprentice.o
from gamestrings import gameStrings
import zlib
import cPickle
import BigWorld
import const
import gameglobal
import utils
import gametypes
from sMath import distance3D
from callbackHelper import Functor
from guis import ui
from guis import messageBoxProxy
from guis import uiConst
from guis import uiUtils
from guis import events
from cdata import game_msg_def_data as GMDD
from data import apprentice_new_config_data as ANCD

class ImpPlayerApprentice(object):

    def set_canbeMentor(self, old):
        if self.canbeMentor and not old:
            gameglobal.rds.ui.mentor.showCertification()

    def onApplyMentor(self, apprenticeName, apprenticeGbId, apprenticeSchool, apprenticeLv, apprenticeGuildName, apprenticeSignature, apprenticeSex):
        data = {'name': apprenticeName,
         'school': apprenticeSchool,
         'gbId': apprenticeGbId,
         'lv': apprenticeLv,
         'guild': apprenticeGuildName,
         'desc': apprenticeSignature,
         'sex': apprenticeSex}
        currentDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_BE_MENTOR)
        if currentDataList:
            for tmpData in currentDataList:
                if tmpData.get('data', {}).get('gbId') == apprenticeGbId:
                    return

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BE_MENTOR, {'data': data})

    def onApplyApprentice(self, mentorName, mentorGbId, mentorSchool, mentorLv, mentorGuildName, mentorSignature, mentorSex):
        data = {'name': mentorName,
         'school': mentorSchool,
         'gbId': mentorGbId,
         'lv': mentorLv,
         'guild': mentorGuildName,
         'desc': mentorSignature,
         'sex': mentorSex}
        currentDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_BE_APPRENTICE)
        if currentDataList:
            for tmpData in currentDataList:
                if tmpData.get('data', {}).get('gbId') == mentorGbId:
                    return

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BE_APPRENTICE, {'data': data})

    def kickMentor(self, mentorName, offTime, punish):
        msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT) % utils.getDisplayName(mentorName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cell.kickMentorAfterConfirmed)

    def kickApprentice(self, apprenticeName, apprenticeGbId, offTime, punish):
        msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT) % utils.getDisplayName(apprenticeName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickApprenticeAfterConfirmed, apprenticeGbId))

    def onAddApprenticeInfo(self, mentorGbId, matesGbIds, apprenticeGbIds):
        if mentorGbId:
            self.mentorGbId = mentorGbId
        if not hasattr(self, 'matesGbIds'):
            self.matesGbIds = []
        if not hasattr(self, 'apprenticeGbIds'):
            self.apprenticeGbIds = []
        if matesGbIds:
            for gbId, _ in matesGbIds:
                self.matesGbIds = filter(lambda x: x[0] != gbId, self.matesGbIds)

            self.matesGbIds = list(matesGbIds) + self.matesGbIds
        if apprenticeGbIds:
            for gbId, _ in apprenticeGbIds:
                self.apprenticeGbIds = filter(lambda x: x[0] != gbId, self.apprenticeGbIds)

            self.apprenticeGbIds = list(apprenticeGbIds) + self.apprenticeGbIds
        gameglobal.rds.ui.dispatchEvent(events.EVENT_ADD_APPRENTICE_IFNO)
        if self.apprenticeGbIds:
            graduateList = filter(lambda x: x[1], self.apprenticeGbIds)
            if len(graduateList) > 0 and hasattr(gameglobal.rds, 'tutorial'):
                gameglobal.rds.tutorial.onApprenticeGraduate()
        if self.inWorld:
            self.onQuestInfoModifiedAtClient(const.QD_APPRENTICE)

    def getApprenticeInfo(self, gbId):
        if hasattr(self, 'apprenticeGbIds'):
            for id, graduate in self.apprenticeGbIds:
                if gbId == id:
                    return (id, graduate)

    def onRemoveApprenticeInfo(self, mentorGbId, matesGbIds, apprenticeGbIds):
        if mentorGbId:
            if hasattr(self, 'mentorGbId') and self.mentorGbId == mentorGbId:
                self.mentorGbId = None
                self.matesGbIds = []
                self.setApprenticeGraduate(False)
        if matesGbIds:
            for gbId in matesGbIds:
                self.matesGbIds = filter(lambda x: x[0] != gbId, self.matesGbIds)

        if apprenticeGbIds:
            for gbId in apprenticeGbIds:
                self.apprenticeGbIds = filter(lambda x: x[0] != gbId, self.apprenticeGbIds)

        gameglobal.rds.ui.dispatchEvent(events.EVENT_REMOVE_APPRENTICE_IFNO)

    def onApplyTraining(self):
        mentorName = ''
        if self.mentorGbId:
            friendVal = self.friend.get(self.mentorGbId)
            if friendVal:
                mentorName = friendVal.name
        msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_CHUAN_GONG_MSG, gameStrings.TEXT_IMPPLAYERAPPRENTICE_115) % mentorName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.acceptTraining)

    def apprenticeGraduate(self):
        self.setApprenticeGraduate(True)
        gameglobal.rds.ui.mentor.showMentorLetter(uiConst.MENTOR_LETTER_CHUSHI)

    def setApprenticeGraduate(self, val):
        self.apprenticeGraduateFlag = val

    def set_apprenticeTrainInfo(self, old):
        super(self.__class__, self).set_apprenticeTrainInfo(old)

    def set_trainingVal(self, old):
        if old > self.trainingVal:
            self.showGameMsg(GMDD.data.APPRENTICE_TRAINING_VAL_CONSUME, (old - self.trainingVal,))
        gameglobal.rds.ui.topBar.setValueByName('trainingVal')

    def applyTraining(self, apprenticeID):
        if not self.stateMachine.checkStatus(const.CT_APPRENTICE_TRAIN):
            return
        if self.enableNewApprentice():
            self.cell.applyTrainingEx(apprenticeID)
        elif gameglobal.rds.ui.mentor.enableApprentice():
            self.cell.applyTraining(apprenticeID)

    def useTrainSkill(self):
        if not self.targetLocked or not self.targetLocked.IsAvatar or self.targetLocked == self:
            self.showGameMsg(GMDD.data.NO_TTRAIN_TARGET, ())
            return False
        self.applyTraining(self.targetLocked.id)

    def acceptTraining(self):
        if not self.stateMachine.checkStatus(const.CT_APPRENTICE_BE_TRAIN):
            return
        self.cell.acceptTraining()

    def cancelApprenticeTraining(self):
        if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
            self.cell.cancelApprenticeTraining()

    def applyTrainingConfirm(self, apprenticeID):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.cell.onApplyTrainingConfirmed, apprenticeID), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_LV_EXP_DECAY, gameStrings.TEXT_IMPPLAYERAPPRENTICE_162)
        gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPPLAYERAPPRENTICE_164, msg, buttons)

    def goonApplyTraining(self, apprenticeID):
        self.cell.onApplyTrainingConfirmed(apprenticeID)

    def hasMentor(self):
        return hasattr(self, 'mentorGbId') and self.mentorGbId

    def onApplyMentorEx(self, apprenticeName, apprenticeGbId, apprenticeSchool, apprenticeLv, apprenticeGuildName, apprenticeSignature, apprenticeSex):
        data = {'name': apprenticeName,
         'school': apprenticeSchool,
         'gbId': apprenticeGbId,
         'lv': apprenticeLv,
         'guild': apprenticeGuildName,
         'desc': apprenticeSignature,
         'sex': apprenticeSex}
        currentDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_BE_MENTOR)
        if currentDataList:
            for tmpData in currentDataList:
                if tmpData.get('data', {}).get('gbId') == apprenticeGbId:
                    return

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BE_MENTOR, {'data': data})

    def getMaxMentorApprenticeValEx(self):
        vals = [ self.apprenticeVal.get(gbId, 0) for gbId in self.apprenticeInfo.keys() ]
        if not vals:
            return 0
        return max(vals)

    def onAddApprenticeInfoEx(self, mentorInfo, matesGbIds, apprenticeGbIds):
        mentorGbId, mentorGraduate, mentorVal = mentorInfo
        if mentorGbId:
            if mentorGbId in self.apprenticeInfo.keys():
                val = self.apprenticeInfo.get(mentorGbId)
                matesGbIdsEx = val.get('mates')
            else:
                matesGbIdsEx = []
            self.apprenticeVal[mentorGbId] = mentorVal
            if matesGbIds:
                for gbId, _ in matesGbIds:
                    matesGbIdsEx = filter(lambda x: x[0] != gbId, matesGbIdsEx)

                matesGbIdsEx = matesGbIdsEx + list(matesGbIds)
            self.apprenticeInfo[mentorGbId] = {'mates': matesGbIdsEx,
             'graduate': mentorGraduate}
        if not hasattr(self, 'apprenticeGbIds'):
            self.apprenticeGbIds = []
        if apprenticeGbIds:
            tmpApprenticeGbIds = []
            for gbId, graduate, val in apprenticeGbIds:
                self.apprenticeGbIds = filter(lambda x: x[0] != gbId, self.apprenticeGbIds)
                self.apprenticeVal[gbId] = val
                tmpApprenticeGbIds.append((gbId, graduate))

            self.apprenticeGbIds = self.apprenticeGbIds + list(tmpApprenticeGbIds)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_ADD_APPRENTICE_IFNO)

    def onRemoveApprenticeInfoEx(self, mentorGbId, matesGbIds, apprenticeGbIds):
        if mentorGbId:
            if mentorGbId in self.apprenticeInfo.keys():
                self.apprenticeInfo.pop(mentorGbId)
        if apprenticeGbIds:
            for gbId in apprenticeGbIds:
                self.apprenticeGbIds = filter(lambda x: x[0] != gbId, self.apprenticeGbIds)

        if matesGbIds:
            for mentorId, gbId in matesGbIds:
                if mentorId in self.apprenticeInfo.keys():
                    mates = self.apprenticeInfo.get(mentorId, {}).get('mates', [])
                    self.apprenticeInfo[mentorId]['mates'] = filter(lambda x: x[0] != gbId, mates)

        gameglobal.rds.ui.dispatchEvent(events.EVENT_REMOVE_APPRENTICE_IFNO)

    def onApplyApprenticeEx(self, mentorName, mentorGbId, mentorSchool, mentorLv, mentorGuildName, mentorSignature, mentorSex):
        data = {'name': mentorName,
         'school': mentorSchool,
         'gbId': mentorGbId,
         'lv': mentorLv,
         'guild': mentorGuildName,
         'desc': mentorSignature,
         'sex': mentorSex}
        currentDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_BE_APPRENTICE)
        if currentDataList:
            for tmpData in currentDataList:
                if tmpData.get('data', {}).get('gbId') == mentorGbId:
                    return

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BE_APPRENTICE, {'data': data})

    def kickMentorEx(self, mentorName, mentorGbId, offTime, punish):
        if punish:
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT_PUNISH) % utils.getDisplayName(mentorName)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT) % utils.getDisplayName(mentorName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickMentorAfterConfirmedEx, mentorGbId, 1))

    def kickApprenticeEx(self, apprenticeName, apprenticeGbId, offTime, punish):
        if punish:
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT_PUNISH) % utils.getDisplayName(apprenticeName)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION_ALERT) % utils.getDisplayName(apprenticeName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickApprenticeAfterConfirmedEx, apprenticeGbId, 1))

    def apprenticeGraduateEx(self, mentorGbId):
        if self.apprenticeInfo.has_key(mentorGbId):
            val = self.apprenticeInfo[mentorGbId]
            val['graduate'] = True
            mates = []
            for gbId, graduate in val.get('mates', []):
                if self.gbId == gbId:
                    mates.append((gbId, True))
                else:
                    mates.append((gbId, graduate))

            val['mates'] = mates
        gameglobal.rds.ui.mentor.showMentorLetter(uiConst.MENTOR_LETTER_CHUSHI)
        gameglobal.rds.ui.mentorEx.refreshPanel()

    def onApplyGraduateEx(self, apprenticeGbId, apprenticeName, grade):
        gameglobal.rds.ui.mentorEx.onApplyGraduateEx(apprenticeGbId, apprenticeName)

    def enableNewApprentice(self):
        return gameglobal.rds.configData.get('enableNewApprentice', False)

    def sendApprenticeValEx(self, totalVal, weeklyVal, apprenticeVal, gbId, src):
        if gbId in self.apprenticeVal:
            self.apprenticeVal[gbId] = apprenticeVal
        self.apprenticeVal['totalVal'] = totalVal
        self.apprenticeVal['weeklyVal'] = weeklyVal

    def enableMentorQulificationEx(self):
        gameglobal.rds.ui.mentorEx.enableMentorQulificationEx()

    def enableApprenticeQulificationEx(self):
        gameglobal.rds.ui.mentorEx.enableApprenticeQulificationEx()

    def onApprenticeLogOnEx(self, apprenticeName, apprenticeGbId):
        pass

    def onMentorLogOnEx(self, mentorName, mentorGbId):
        pass

    def onSetBeMentorSloganEx(self, slogan):
        self.showGameMsg(GMDD.data.APPRENTICE_ON_SET_BE_MENTOR, ())
        gameglobal.rds.ui.mentorEx.onSetBeMentorSloganEx(slogan)

    def onSetBeApprenticeSloganEx(self, slogan):
        self.showGameMsg(GMDD.data.APPRENTICE_ON_SET_BE_APPRENTICE, ())
        gameglobal.rds.ui.mentorEx.onSetBeApprenticeSloganEx(slogan)

    def applyTrainingConfirmEx(self, apprenticeID):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.cell.onApplyTrainingConfirmedEx, apprenticeID), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_LV_EXP_DECAY, gameStrings.TEXT_IMPPLAYERAPPRENTICE_162)
        gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPPLAYERAPPRENTICE_164, msg, buttons)

    def onApplyTrainingEx(self, mentorGbId):
        mentorName = ''
        friendVal = self.friend.get(mentorGbId)
        if friendVal:
            mentorName = friendVal.name
        msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_CHUAN_GONG_MSG, gameStrings.TEXT_IMPPLAYERAPPRENTICE_115) % mentorName
        ents = [ ent for ent in BigWorld.entities.values() if getattr(ent, 'gbId', None) == mentorGbId ]
        if ents:
            mentor = ents[0]
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.acceptTrainingEx, mentor.id))

    def acceptTrainingEx(self, mentorId):
        if not self.stateMachine.checkStatus(const.CT_APPRENTICE_BE_TRAIN):
            return
        self.cell.acceptTrainingEx(mentorId)

    def set_apprenticeTrainInfoEx(self, old):
        super(self.__class__, self).set_apprenticeTrainInfoEx(old)

    def hasMentorEx(self):
        return bool(self.apprenticeInfo)

    def hasApprenticeEx(self):
        return bool(self.apprenticeGbIds)

    def onApplySoleMentorEx(self, apprenticeGbId, apprenticeName):
        gameglobal.rds.ui.mentorEx.onApplySoleMentorEx(apprenticeGbId, apprenticeName)

    def onApplySoleApprenticeEx(self, mentorGbId, mentorName):
        gameglobal.rds.ui.mentorEx.onApplySoleApprenticeEx(mentorGbId, mentorName)

    def onSetSoleApprenticeEx(self, gbId, roleType):
        if roleType == gametypes.APPRENTICE_ROLE_TYPE_SOLE_MENTOR:
            self.soleMentorGbId = gbId
        elif roleType == gametypes.APPRENTICE_ROLE_TYPE_SOLE_APPRENTICE:
            self.soleApprenticeGbId = gbId
        gameglobal.rds.ui.mentorEx.refreshPanel()

    def onApplySoleDismissEx(self, gbId, name):
        gameglobal.rds.ui.mentorEx.onApplySoleDismissEx(gbId, name)

    def onClearSoleApprenticeEx(self, gbId, roleType):
        if roleType == gametypes.APPRENTICE_ROLE_TYPE_MENTOR:
            self.soleMentorGbId = 0
        elif roleType == gametypes.APPRENTICE_ROLE_TYPE_APPRENTICE:
            self.soleApprenticeGbId = 0
        gameglobal.rds.ui.mentorEx.refreshPanel()

    def kickMentorCheckSoleEx(self, gbId):
        if self.soleMentorGbId == gbId:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.base.kickMentorEx, gbId), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_SOLE_MENTOR, gameStrings.TEXT_IMPPLAYERAPPRENTICE_370)
            gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPPLAYERAPPRENTICE_372, msg, buttons)
        else:
            self.base.kickMentorEx(gbId)

    def kickApprenticeCheckSoleEx(self, gbId):
        if self.soleApprenticeGbId == gbId:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.base.kickApprenticeEx, gbId), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_SOLE_APPRENTICE, gameStrings.TEXT_IMPPLAYERAPPRENTICE_381)
            gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPPLAYERAPPRENTICE_372, msg, buttons)
        else:
            self.base.kickApprenticeEx(gbId)

    def applyGraduateEx(self, mentorGbId, ret):
        gameglobal.rds.ui.mentorEx.onApprenticeGraduateEx(mentorGbId, ret)

    def onGetApprenticeInfoEx(self, gbId, ret):
        getExtraInfos = gameglobal.rds.ui.mentorEx.getExtraInfos
        oldVal = getExtraInfos.get(gbId, None)
        if oldVal == ret:
            return
        else:
            getExtraInfos[gbId] = ret
            gameglobal.rds.ui.mentorEx.refreshPanel()
            return

    def set_soleMentorNameEx(self, old):
        self.refreshToplogoTitle()

    def set_soleApprenticeNameEx(self, old):
        self.refreshToplogoTitle()

    def onSetApprenticeOptEx(self, mentorRejectOptEx, apprenticeRejectOptEx):
        self.mentorRejectOptEx = mentorRejectOptEx
        self.apprenticeRejectOptEx = apprenticeRejectOptEx

    def checkUngraduateTeamMentorEx(self):
        if not self.apprenticeInfo:
            return False
        for mentorGbId, info in self.apprenticeInfo.iteritems():
            if mentorGbId in self.members and not info.get('graduate', False):
                tgt = BigWorld.entities.get(self.members[mentorGbId].get('id', 0))
                if tgt and distance3D(self.position, tgt.position) <= 80:
                    return True

        return False

    def checkGraduateTeamMentorEx(self):
        if not self.apprenticeInfo:
            return False
        for mentorGbId, info in self.apprenticeInfo.iteritems():
            if mentorGbId in self.members and info.get('graduate', False):
                tgt = BigWorld.entities.get(self.members[mentorGbId].get('id', 0))
                if tgt and distance3D(self.position, tgt.position) <= 80:
                    return True

        return False

    def onGetGraduateRemarkByGbIdEx(self, gbId, res):
        info = cPickle.loads(zlib.decompress(res))
        gameglobal.rds.ui.mentorEx.onGetGraduateRemarkByGbIdEx(gbId, info)

    def getMaxApprenticeNum(self):
        totalApprenticeVal = self.apprenticeVal.get('totalVal', 0)
        maxApprenticeNumWithVal = ANCD.data.get('maxApprenticeNumWithApprenticeVal', ())
        maxApprenticeNum = ANCD.data.get('initMaxApprenticeNum', 3)
        for minVal, maxVal, maxNum in maxApprenticeNumWithVal:
            if minVal <= totalApprenticeVal <= maxVal or maxVal == -1 and minVal <= totalApprenticeVal:
                maxApprenticeNum = maxNum
                break

        return maxApprenticeNum

    def sendApprenticePreferenceInfo(self, mentorPreferenceInfo, apprenticePreferenceInfo):
        gameglobal.rds.ui.mentorEx.sendApprenticePreferenceInfo(mentorPreferenceInfo, apprenticePreferenceInfo)

    def onQueryApprenticeGrowthFeedBack(self, val, growthConsumeRewarded):
        msg = gameStrings.TEXT_IMPPLAYERAPPRENTICE_457 % val
        if growthConsumeRewarded:
            for name, cash, key in sorted(growthConsumeRewarded, key=lambda d: d[2]):
                if key == 'graduate':
                    tp = gameStrings.TEXT_IMPPLAYERAPPRENTICE_461
                else:
                    tp = gameStrings.TEXT_IMPPLAYERAPPRENTICE_463 % key
                msg += gameStrings.TEXT_IMPPLAYERAPPRENTICE_464 % (name, tp, cash)

        gameglobal.rds.ui.messageBox.showMsgBox(msg, textAlign='left')

    def onApplyLevelGrowthFeedback(self, apprenticeGbId, apprenticeVal, growthConsumeVal, growthConsumeCash):
        gameglobal.rds.ui.messageBox.dismiss(getattr(self, 'lastFeedbackId', 0))
        msg = gameStrings.TEXT_IMPPLAYERAPPRENTICE_470 % (apprenticeVal, growthConsumeVal, growthConsumeCash)
        self.lastFeedbackId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.comfirmApplyLevelGrowthFeedback, apprenticeGbId))

    def onGetLevelGrowthFeedback(self, mentorGbId, mentorName, apprenticeVal, growthConsumeVal, growthConsumeCash):
        gameglobal.rds.ui.messageBox.dismiss(getattr(self, 'lastFeedbackId', 0))
        msg = gameStrings.TEXT_IMPPLAYERAPPRENTICE_476 % (apprenticeVal,
         growthConsumeVal,
         mentorName,
         growthConsumeCash)
        self.lastFeedbackId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.comfirmGetLevelGrowthFeedback, mentorGbId, True), noCallback=Functor(self.comfirmGetLevelGrowthFeedback, mentorGbId, False))

    def onApplyGraduateGrowthFeedback(self, apprenticeGbId, apprenticeVal, growthConsumeVal, growthConsumeCash):
        gameglobal.rds.ui.messageBox.dismiss(getattr(self, 'lastFeedbackId', 0))
        msg = gameStrings.TEXT_IMPPLAYERAPPRENTICE_483 % (apprenticeVal, growthConsumeVal, growthConsumeCash)
        self.lastFeedbackId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.comfirmApplyGraduateGrowthFeedback, apprenticeGbId))

    def onGetGraduateGrowthFeedback(self, mentorGbId, mentorName, apprenticeVal, growthConsumeVal, growthConsumeCash):
        gameglobal.rds.ui.messageBox.dismiss(getattr(self, 'lastFeedbackId', 0))
        msg = gameStrings.TEXT_IMPPLAYERAPPRENTICE_476 % (apprenticeVal,
         growthConsumeVal,
         mentorName,
         growthConsumeCash)
        self.lastFeedbackId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.comfirmGetGraduateGrowthFeedback, mentorGbId, True), noCallback=Functor(self.comfirmGetGraduateGrowthFeedback, mentorGbId, False))

    @ui.checkInventoryLock()
    def comfirmApplyLevelGrowthFeedback(self, apprenticeGbId):
        self.cell.getLevelGrowthFeedback(apprenticeGbId, self.cipherOfPerson)

    @ui.checkInventoryLock()
    def comfirmGetLevelGrowthFeedback(self, mentorGbId, comfirm = True):
        self.cell.onGetLevelGrowthFeedbackConfirmed(mentorGbId, self.cipherOfPerson, comfirm)

    @ui.checkInventoryLock()
    def comfirmApplyGraduateGrowthFeedback(self, apprenticeGbId):
        self.cell.getGraduateGrowthFeedback(apprenticeGbId, self.cipherOfPerson)

    @ui.checkInventoryLock()
    def comfirmGetGraduateGrowthFeedback(self, mentorGbId, comfirm = True):
        self.cell.onGetGraduateGrowthFeedbackConfirmed(mentorGbId, self.cipherOfPerson, comfirm)
