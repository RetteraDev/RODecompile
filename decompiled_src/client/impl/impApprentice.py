#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impApprentice.o
from gamestrings import gameStrings
import cPickle
import zlib
import BigWorld
import Math
import utils
import gameglobal
from guis import uiUtils
from guis import uiConst
from callbackHelper import Functor
from helpers import action
from data import apprentice_config_data as ACD
from data import apprentice_new_config_data as ANCD
from cdata import game_msg_def_data as GMDD
from data import item_data as ID

class ImpApprentice(object):

    def isInApprenticeTrain(self):
        if gameglobal.rds.configData.get('enableNewApprentice', False):
            if not self.apprenticeTrainInfoEx:
                return False
            if self.id == self.apprenticeTrainInfoEx[0]:
                return True
            return False
        elif not self.apprenticeTrainInfo:
            return False
        elif self.id == self.apprenticeTrainInfo[0]:
            return True
        else:
            return False

    def isInApprenticeBeTrain(self):
        if gameglobal.rds.configData.get('enableNewApprentice', False):
            if not self.apprenticeTrainInfoEx:
                return False
            if self.gbId == self.apprenticeTrainInfoEx[1]:
                return True
            return False
        elif not self.apprenticeTrainInfo:
            return False
        elif self.gbId == self.apprenticeTrainInfo[1]:
            return True
        else:
            return False

    def getTrainStartAction(self):
        if self.isInApprenticeTrain():
            return ACD.data.get('trainStartAction', '75501')
        else:
            return ACD.data.get('beTrainStartAction', '76501')

    def getTrainLoopAction(self):
        if self.isInApprenticeTrain():
            return ACD.data.get('trainLoopAction', '75502')
        else:
            return ACD.data.get('beTrainLoopAction', '76502')

    def getTrainEndAction(self):
        if self.isInApprenticeTrain():
            return ACD.data.get('trainEndAction', '75503')
        else:
            return ACD.data.get('beTrainEndAction', '76503')

    def getTrainLoopEffect(self):
        if self.isInApprenticeTrain():
            return ACD.data.get('trainLoopEffect', (30410,))
        else:
            return ACD.data.get('beTrainLoopEffect', (30411,))

    def playApprenticeTrainStart(self):
        trainStartAction = self.getTrainStartAction()
        trainLoopAction = self.getTrainLoopAction()
        trainLoopEffect = self.getTrainLoopEffect()
        blend = True
        keep = True
        playSeq = []
        playSeq.append((trainStartAction,
         None,
         action.APPRENTICE_TRAIN_ACTION,
         0,
         1.0,
         None))
        playSeq.append((trainLoopAction,
         trainLoopEffect,
         action.APPRENTICE_TRAIN_ACTION,
         0,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.APPRENTICE_TRAIN_ACTION, None, blend, None, keep, priority=self.getSkillEffectPriority())

    def playApprenticeTrainLoop(self):
        if self.inMoving():
            return
        else:
            self.fashion.stopAllActions()
            trainLoopAction = self.getTrainLoopAction()
            trainLoopEffect = self.getTrainLoopEffect()
            blend = True
            keep = True
            playSeq = []
            playSeq.append((trainLoopAction,
             trainLoopEffect,
             action.APPRENTICE_TRAIN_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.APPRENTICE_TRAIN_ACTION, None, blend, None, keep, priority=self.getSkillEffectPriority())
            return

    def playApprenticeTrainEnd(self):
        self.fashion.stopAllActions()
        trainEndAction = self.getTrainEndAction()
        if not self.inMoving():
            blend = True
            keep = True
            playSeq = []
            playSeq.append((trainEndAction,
             None,
             action.APPRENTICE_TRAIN_END_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.APPRENTICE_TRAIN_END_ACTION, None, blend, None, keep, priority=self.getSkillEffectPriority())

    def gotoRightPosition(self):
        if self == BigWorld.player():
            trainer = BigWorld.entities.get(self.apprenticeTrainInfo[0])
            if trainer:
                dist = ACD.data.get('relativeApprenticeDist', 1)
                destPos = Math.Vector3(utils.getRelativePosition(trainer.position, trainer.yaw, 0, dist))
                BigWorld.player().ap.seekPath(destPos, Functor(self.arriveRightPosition, trainer))

    def arriveRightPosition(self, trainer, suc):
        if not trainer or not trainer.inWorld:
            return
        dist = ACD.data.get('relativeApprenticeDist', 1)
        destPos = Math.Vector3(utils.getRelativePosition(trainer.position, trainer.yaw, 0, dist))
        BigWorld.player().ap.seekPath(destPos, Functor(self.arriveCallback, trainer))
        self.arriveCallback(trainer, True)

    def arriveCallback(self, trainer, ret):
        self.ap.forwardMagnitude = 0
        self.ap.updateMoveControl()
        BigWorld.callback(0.1, Functor(self.faceTrainer, trainer))

    def faceTrainer(self, trainer):
        self.faceTo(trainer)
        self.ap.restore()

    def set_apprenticeTrainInfo(self, old):
        if self.apprenticeTrainInfo:
            if self == BigWorld.player():
                if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
                    self.ap.stopMove()
                    self.ap.restore(False)
        if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
            self.playApprenticeTrainStart()
            if self.isInApprenticeBeTrain():
                self.gotoRightPosition()
        if old and (not self.isInApprenticeTrain() or not self.isInApprenticeBeTrain()):
            self.playApprenticeTrainEnd()
            if self == BigWorld.player():
                self.ap.reset()

    def checkMentorCondition(self, bMsg = False):
        if not gameglobal.rds.ui.mentor.enableApprentice():
            return False
        if self._isSoul():
            return
        p = BigWorld.player()
        if not self.canbeMentor:
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_NO_MENTOR_QULIFICATION, ())
            return False
        if self.lv < ACD.data.get('minMentorLv', 50):
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        return True

    def checkApprenticeCondition(self, bMsg = False):
        if not gameglobal.rds.ui.mentor.enableApprentice():
            return False
        if self._isSoul():
            return
        maxApprenticeLv = ACD.data.get('maxApprenticeLv', 0)
        minApprenticeLv = ACD.data.get('minApprenticeLv', 0)
        p = BigWorld.player()
        if maxApprenticeLv and self.lv > maxApprenticeLv:
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        if minApprenticeLv and self.lv < minApprenticeLv:
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        return True

    def checkApprenticeConditionEx(self, bMsg = False):
        p = BigWorld.player()
        if not p.enableNewApprentice():
            return False
        if self._isSoul():
            return
        maxApprenticeLv = ANCD.data.get('maxApprenticeLv', 0)
        minApprenticeLv = ANCD.data.get('minApprenticeLv', 0)
        if maxApprenticeLv and self.lv > maxApprenticeLv:
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        if minApprenticeLv and self.lv < minApprenticeLv:
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        return True

    def checkMentorConditionEx(self, bMsg = False):
        p = BigWorld.player()
        if not p.enableNewApprentice():
            return False
        if self._isSoul():
            return
        if self.lv < ANCD.data.get('minMentorLv', 50):
            bMsg and p.showGameMsg(GMDD.data.APPRENTICE_LV_CHECK_FAILED, ())
            return False
        return True

    def set_apprenticeTitleMentor(self, old):
        self.refreshToplogoTitle()

    def set_apprenticeTitleApprentice(self, old):
        self.refreshToplogoTitle()

    def applyTrainingConfirm(self, apprenticeID):
        pass

    def kickMentorGraduated(self):
        graduateDismissItem = ACD.data.get('graduateDismissItem', 0)
        if graduateDismissItem in ID.data:
            itemData = uiUtils.getGfxItemById(graduateDismissItem)
            itemName = ID.data[graduateDismissItem]['name']
        else:
            itemData = None
            itemName = ''
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_MENTOR_GRADUATED, gameStrings.TEXT_IMPAPPRENTICE_235) % itemName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cell.kickMentorGraduatedAfterConfirmed, itemData=itemData)

    def kickApprenticeGraduated(self, gbId, name):
        graduateDismissItem = ACD.data.get('graduateDismissItem', 0)
        if graduateDismissItem in ID.data:
            itemData = uiUtils.getGfxItemById(graduateDismissItem)
            itemName = ID.data[graduateDismissItem]['name']
        else:
            itemData = None
            itemName = ''
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_APPRENTICE_GRADUATED, gameStrings.TEXT_IMPAPPRENTICE_248) % (name, itemName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickApprenticeGraduatedAfterConfirmed, gbId), itemData=itemData)

    def onGetRecommendMentors(self, res):
        info = cPickle.loads(zlib.decompress(res))
        gameglobal.rds.ui.mentor.showRecommend(info, uiConst.RECOMMEND_MENTORS)

    def onGetRecommendApprentices(self, res):
        info = cPickle.loads(zlib.decompress(res))
        gameglobal.rds.ui.mentor.showRecommend(info, uiConst.RECOMMEND_APPRENTICES)

    def kickMentorGraduatedEx(self, gbId, name):
        graduateDismissItem = ANCD.data.get('graduateDismissItem', 0)
        if graduateDismissItem in ID.data:
            itemData = uiUtils.getGfxItemById(graduateDismissItem)
            itemName = ID.data[graduateDismissItem]['name']
        else:
            itemData = None
            itemName = ''
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_MENTOR_GRADUATED, gameStrings.TEXT_IMPAPPRENTICE_235) % itemName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickMentorGraduatedAfterConfirmedEx, gbId, 2), itemData=itemData)

    def kickApprenticeGraduatedEx(self, gbId, name):
        graduateDismissItem = ANCD.data.get('graduateDismissItem', 0)
        if graduateDismissItem in ID.data:
            itemData = uiUtils.getGfxItemById(graduateDismissItem)
            itemName = ID.data[graduateDismissItem]['name']
        else:
            itemData = None
            itemName = ''
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_KICK_APPRENTICE_GRADUATED, gameStrings.TEXT_IMPAPPRENTICE_248) % (name, itemName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.base.kickApprenticeGraduatedAfterConfirmedEx, gbId, 1), itemData=itemData)

    def onGetRecommendApprenticesEx(self, res, isMentor):
        gameglobal.rds.ui.mentorEx.onGetRecommendApprenticesEx(res, isMentor)

    def applyTrainingConfirmEx(self, apprenticeID):
        pass

    def set_apprenticeTrainInfoEx(self, old):
        if self.apprenticeTrainInfoEx:
            if self == BigWorld.player():
                if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
                    self.ap.stopMove()
                    self.ap.restore(False)
        if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
            self.playApprenticeTrainStart()
            if self.isInApprenticeBeTrain():
                if self == BigWorld.player():
                    trainer = BigWorld.entities.get(self.apprenticeTrainInfoEx[0])
                    if trainer:
                        dist = ANCD.data.get('relativeApprenticeDist', 1)
                        destPos = Math.Vector3(utils.getRelativePosition(trainer.position, trainer.yaw, 0, dist))
                        BigWorld.player().ap.seekPath(destPos, Functor(self.arriveRightPosition, trainer))
        if old and (not self.isInApprenticeTrain() or not self.isInApprenticeBeTrain()):
            self.playApprenticeTrainEnd()
            if self == BigWorld.player():
                self.ap.reset()

    def replayOtherApprenticeTrainEx(self):
        if self != BigWorld.player():
            self.playApprenticeTrainLoop()

    def onGetRecommendApprenticesFromUS(self, res, isMentor):
        gameglobal.rds.ui.mentorEx.onGetRecommendApprenticesEx(res, isMentor)

    def onAssignApprenticeTarget(self, gbId, apprenticeTargetId):
        if not hasattr(self, 'apprenticeTargets'):
            self.apprenticeTargets = {}
        if gbId in self.apprenticeTargets:
            targets, rewarded, assignTime = self.apprenticeTargets.get(gbId)
        else:
            targets, rewarded, assignTime = {}, 0, 0
        targets[apprenticeTargetId] = 0
        self.apprenticeTargets[gbId] = (targets, rewarded, utils.getNow())
        gameglobal.rds.ui.apprenticeTarget.refreshInfo()
        gameglobal.rds.ui.apprenticeTarget.refreshTargetsView()

    def sendApprenticeTargets(self, apprenticeTargetIds):
        if not hasattr(self, 'apprenticeTargets'):
            self.apprenticeTargets = apprenticeTargetIds
        else:
            self.apprenticeTargets.update(apprenticeTargetIds)
        gameglobal.rds.ui.apprenticeTarget.refreshInfo()
        gameglobal.rds.ui.apprenticeTarget.refreshTargetsView()

    def clearApprenticeTargetsInfo(self):
        self.apprenticeTargets = {}
        gameglobal.rds.ui.apprenticeTarget.refreshInfo()

    def onFinishApprenticeTarget(self, gbId, apprenticeTargetId):
        if gbId in self.apprenticeTargets:
            targets, rewarded, assignTime = self.apprenticeTargets.get(gbId)
            targets[apprenticeTargetId] = 1
            self.apprenticeTargets[gbId] = (targets, rewarded, assignTime)
            gameglobal.rds.ui.apprenticeTarget.refreshInfo()

    def sendApprenticeTargetPoolSeed(self, seed):
        self.apprenticeTargetPoolSeed = seed
        gameglobal.rds.ui.apprenticeTarget.refreshInfo()

    def isTeacher(self, gbId):
        if not hasattr(self, 'apprenticeInfo'):
            return False
        if gbId in self.apprenticeInfo.keys():
            return True

    def isApprentice(self, targetGbId):
        if not hasattr(self, 'apprenticeGbIds'):
            return False
        for gbId, _ in self.apprenticeGbIds:
            if targetGbId == gbId:
                return True

        return False
