#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newGuiderOperaProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import tutorial_config_data as TCD
from data import sys_config_data as SCD
OPERATION_KEYS = [0, 1, 2]

class NewGuiderOperaProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewGuiderOperaProxy, self).__init__(uiAdapter)
        self.modelMap = {'handleCloseBtn': self.onHandleCloseBtn,
         'handleConfirmBtn': self.onHandleConfirmBtn,
         'handleOperaBtn': self.onHandleOperaBtn,
         'getRecom': self.onGetRecom,
         'getDesc': self.onGetDesc}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_GUIDER_OPERATION, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEW_GUIDER_OPERATION:
            self.mediator = mediator
            initData = self.getGuideData()
            if initData:
                return uiUtils.dict2GfxDict(initData, True)

    def getGuideData(self):
        if not gameglobal.rds.configData.get('enableCareerGuilde', False):
            return {}
        p = BigWorld.player()
        if hasattr(p, 'carrerGuideData'):
            schoolName = const.SCHOOL_DICT[p.school]
            operationInfo = p.carrerGuideData.get('operationInfo', {})
            operationGuide = {}
            for k in OPERATION_KEYS:
                v = operationInfo.get(k, 0)
                guideTxt = gameStrings.OPERATION_GUIDE_TIP % (v * 100, schoolName)
                operationGuide[k] = guideTxt

            return operationGuide
        return {}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GUIDER_OPERATION)

    def onHandleConfirmBtn(self, *arg):
        mode = int(arg[3][0].GetString())
        uiUtils.setAvatarPhysics(mode)
        gameglobal.rds.ui.actionbar.setFirstTimeOperation(mode, 1)
        if hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onMouseLeftBtnUp(['newGuiderOperaCloseBtn', 'None'])
            if mode == gameglobal.KEYBOARD_MODE:
                gameglobal.rds.tutorial.onOperaSelectTrigger(30)
            elif mode == gameglobal.MOUSE_MODE:
                gameglobal.rds.tutorial.onOperaSelectTrigger(28)
            elif mode == gameglobal.ACTION_MODE:
                gameglobal.rds.tutorial.onOperaSelectTrigger(29)
        self.hide()
        gameglobal.rds.ui.topBar.shineActionBtn()
        gameglobal.rds.ui.newGuiderOperationHint.playEffect()

    def onHandleCloseBtn(self, *arg):
        self.hide()
        gameglobal.rds.ui.topBar.shineActionBtn()

    def onHandleOperaBtn(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_CONTROL)

    def onGetRecom(self, *arg):
        info = {}
        p = BigWorld.player()
        operaRecomDict = TCD.data['operaRecomDict']
        info['recOp'] = operaRecomDict.get(BigWorld.player().school, 0)
        info['curOp'] = p.getOperationMode()
        return uiUtils.dict2GfxDict(info)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GUIDER_OPERATION)

    def close(self):
        self.hide()

    def onGetDesc(self, *arg):
        operaRecom = int(arg[3][0].GetNumber())
        operaRecomDict = TCD.data.get('operaRecomDict')
        if operaRecom == -1:
            operaRecom = operaRecomDict[BigWorld.player().school]
        info = {}
        guiderDesc = SCD.data.get('guiderDesc', {})
        info['modeDesc'] = guiderDesc[operaRecom]['modeDesc']
        info['desc'] = guiderDesc[operaRecom]['desc']
        info['recomDesc'] = guiderDesc[operaRecom]['recomDesc']
        info['recomSchoolDesc'] = guiderDesc[operaRecom]['recomSchoolDesc']
        return uiUtils.dict2GfxDict(info, True)
