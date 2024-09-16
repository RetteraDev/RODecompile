#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenQuestProxy.o
import gameglobal
import uiUtils
import uiConst
from guis.uiProxy import UIProxy
from data import challenge_guide_data as CGD

class FubenQuestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenQuestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData}
        self.reset()
        self.questId = None

    def show(self, questId):
        self.questId = questId
        self.uiAdapter.loadWidget(uiConst.WIDGET_FUBEN_QUEST)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_QUEST)
        gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_FUBEN_QUEST, False)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def onGetInitData(self, *args):
        desc = CGD.data.get(self.questId, {}).get('desc', '')
        goal = CGD.data.get(self.questId, {}).get('goal', '')
        ret = {'desc': desc,
         'target': goal}
        return uiUtils.dict2GfxDict(ret, True)
