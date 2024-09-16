#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/trainingNpcProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import gamelog
from uiProxy import UIProxy
from data import training_npc_ai_data as TNAD
STAGE_SELECT_SCHOOL = 1
STAGE_SELECT_BOSS = 2

class TrainingNpcProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TrainingNpcProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPanelInfo': self.onGetPanelInfo,
         'clickSelectSchool': self.onClickSelectSchool,
         'clickSelectBoss': self.onClickSelectBoss,
         'getSelectedSchool': self.onGetSelectedSchool,
         'getSelectedBoss': self.onGetSelectedBoss}
        self.mediator = None
        self.selectedSchoolIndex = 0
        self.diedBoss = []
        self.diedBossId = 0
        self.passedBoss = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_NPC_TRAINING, self.close)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NPC_TRAINING:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        self.closeNpcTrainingWidget()

    def reset(self):
        self.stage = STAGE_SELECT_SCHOOL
        self.erefFunId = None
        self.selectedBossIndex = 0

    def close(self):
        gameglobal.rds.ui.trainingNpc.hide()
        gameglobal.rds.ui.funcNpc.close()

    def addDiedMonster(self, charType):
        self.diedBossId = charType
        self.diedBoss.append(charType)

    def _getSelectSchoolData(self):
        source = TNAD.data.get(self.erefFunId, {}).get('panel1', [])
        return uiUtils.array2GfxAarry(source)

    def _getSelectBossData(self):
        ar = self.movie.CreateArray()
        source = TNAD.data.get(self.erefFunId, {}).get('panel2', [])
        index = 0
        isHistory = TNAD.data.get(self.erefFunId, {}).get('isHistory', 0)
        for elem in source:
            if isHistory and elem[1] not in self.passedBoss:
                continue
            obj = self.movie.CreateObject()
            obj.SetMember('bossId', GfxValue(elem[0]))
            if elem[1] in self.diedBoss:
                obj.SetMember('isPassed', GfxValue(1))
            else:
                obj.SetMember('isPassed', GfxValue(0))
            ar.SetElement(index, obj)
            index += 1

        return ar

    def onGetPanelInfo(self, *arg):
        gamelog.debug('@hjx training#onGetPanelInfo0:', self.stage, self.erefFunId)
        if self.erefFunId is None:
            return
        else:
            obj = self.movie.CreateObject()
            obj.SetMember('stage', GfxValue(self.stage))
            if self.stage == STAGE_SELECT_SCHOOL:
                data = self._getSelectSchoolData()
            else:
                data = self._getSelectBossData()
            obj.SetMember('data', data)
            return obj

    def onClickSelectSchool(self, *arg):
        self.selectedSchoolIndex = int(arg[3][0].GetString())
        gamelog.debug('@hjx training#onClickSelectSchool:', self.selectedSchoolIndex)

    def onClickSelectBoss(self, *arg):
        self.selectedBossIndex = int(arg[3][0].GetString())
        gamelog.debug('@hjx training#onClickSelectBoss:', self.selectedBossIndex)

    def onSelectSchool(self):
        gamelog.debug('@hjx training#onSelectSchool:', self.erefFunId)
        self.stage = STAGE_SELECT_SCHOOL
        self.refreshTrainingPanel()

    def onSelectBoss(self, npcId):
        gamelog.debug('@hjx training#onSelectBoss:', self.erefFunId)
        self.stage = STAGE_SELECT_BOSS
        self.refreshTrainingPanel()
        npc = BigWorld.entities.get(npcId)
        if npc is not None:
            npc.cell.executeTrainingFbAI(self.selectedSchoolIndex + 1, uiConst.TRAINING_FUBEN_TYPE_PANEL_SCHOOL)

    def onGetSelectedSchool(self, *arg):
        return GfxValue(self.selectedSchoolIndex)

    def onGetSelectedBoss(self, *arg):
        return GfxValue(self.selectedBossIndex)

    def refreshTrainingPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NPC_TRAINING)

    def onOkBtnClick(self, npcId):
        npc = BigWorld.entities.get(npcId)
        gamelog.debug('@hjx training#onOkBtnClick:', npcId, npc)
        if npc is not None:
            npc.cell.executeTrainingFbAI(self.selectedBossIndex + 1, uiConst.TRAINING_FUBEN_TYPE_PANEL_BOSS)
        self.close()

    def closeNpcTrainingWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NPC_TRAINING)

    def initData(self, bossHistory):
        self.passedBoss = bossHistory
        self.selectedSchoolIndex = 0
        self.diedBoss = []
        self.diedBossId = 0
