#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/trainingFubenEvalProxy.o
import BigWorld
import gameglobal
import gamelog
from uiProxy import DataProxy
from guis import uiConst
from fubenEvalInfo import TrainingFubenEvalInfo
from guis.fubenEvalInfo import ChallengeFubenEvalInfo

class TrainingFubenEvalProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(TrainingFubenEvalProxy, self).__init__(uiAdapter)
        self.bindType = 'trainingFubenEval'
        self.modelMap = {'closeClick': self.onCloseClick,
         'getEvalInfo': self.onGetEvalInfo,
         'getAllStaticsInfo': self.onGetAllStaticsInfo}
        self.reset()

    def reset(self):
        self.evalInfo = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRAINING_FUBEN_EVAL)

    def onGetEvalInfo(self, *arg):
        gamelog.debug('@hjx TrainingFubenEvalProxy#onGetEvalInfo:')
        if self.evalInfo is None:
            gamelog.ERROR('@hjx TrainingFubenEvalProxy#onGetEvalInfo: evalInfo is None!')
            return
        else:
            ret = self.movie.CreateObject()
            ret.SetMember('combat', self.evalInfo.getCombatInfo())
            ret.SetMember('record', self.evalInfo.getRecordInfo())
            ret.SetMember('allStatics', self.evalInfo.getAllStatics())
            ret.SetMember('bossName', self.evalInfo.getBossName())
            ret.SetMember('evalName', self.evalInfo.getEvalLevel())
            return ret

    def onGetAllStaticsInfo(self, *arg):
        return self.evalInfo.getAllStaticsInfo()

    def showFubenEval(self, evalInfo):
        p = BigWorld.player()
        p.motionPin()
        self.evalInfo = TrainingFubenEvalInfo(evalInfo)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TRAINING_FUBEN_EVAL, True)

    def showChallangeFubenEval(self, evalInfo, missionId):
        self.evalInfo = ChallengeFubenEvalInfo(evalInfo, missionId)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TRAINING_FUBEN_EVAL)

    def onCloseClick(self, *arg):
        BigWorld.player().motionUnpin()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRAINING_FUBEN_EVAL)
