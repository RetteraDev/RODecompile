#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dynamicResultProxy.o
import BigWorld
import gameglobal
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from data import life_skill_event_notify_data as LSEND
from data import state_data as SD

class DynamicResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DynamicResultProxy, self).__init__(uiAdapter)
        self.modelMap = {'doHide': self.onHide}
        self.reset()

    def onHide(self, *args):
        self.clearWidget()

    def reset(self):
        self.med = None
        self.resultData = None

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYNAMIC_RESULT)
        self.med = None
        self.resultData = None

    def show(self, *args):
        BigWorld.callback(0.2, self.showReal)

    def showReal(self):
        if self.resultData:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYNAMIC_RESULT)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYNAMIC_RESULT:
            self.med = mediator
            if self.resultData:
                return self.getGfxResultData()

    def showResult(self, resultType, resultData):
        notifyData = LSEND.data.get((resultType, resultData), {})
        if not notifyData:
            return
        self.resultData = {'type': resultType,
         'tips': notifyData.get('tips', ''),
         'name': notifyData.get('name', ''),
         'showTime': 5}
        if resultType == uiConst.LIFE_SKILL_EVENT_BUFF:
            buffIconId = SD.data.get(resultData, {}).get('iconId', '')
            self.resultData['icon'] = 'state/40/%s.dds' % buffIconId
        elif resultType in (uiConst.LIFE_SKILL_EVENT_ITEM,
         uiConst.LIFE_SKILL_EVENT_FAME,
         uiConst.LIFE_SKILL_EVENT_PICKITEM,
         uiConst.LIFE_SKILL_EVENT_BOXITEM,
         uiConst.LIFE_SKILL_EVENT_GET_ABILITY):
            self.resultData['icon'] = uiUtils.getItemIconFile64(resultData)
            if resultType != uiConst.LIFE_SKILL_EVENT_FAME:
                name = uiUtils.getItemColorName(resultData)
                self.resultData['name'] = name
        if self.med:
            self.med.Invoke('setResult', self.getGfxResultData())
        else:
            self.show()

    def getGfxResultData(self):
        return uiUtils.dict2GfxDict(self.resultData, True)
