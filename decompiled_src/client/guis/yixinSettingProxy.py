#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yixinSettingProxy.o
import BigWorld
import gameglobal
import copy
from guis import uiConst
from guis.uiProxy import UIProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class YixinSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YixinSettingProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'getSettingData': self.getSettingData,
         'setting': self.setting,
         'howToConcern': self.howToConcern,
         'howToAddGroup': self.howToAddGroup}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YIXIN_SETTING, self.closeWidget)

    def reset(self):
        self.dismiss()

    def setting(self, *args):
        startTimeIndex = int(args[3][0].GetNumber()) - 1
        endTimeIndex = int(args[3][1].GetNumber()) - 1
        otherLoginSetting = args[3][2].GetBool()
        salesSetting = args[3][3].GetBool()
        if startTimeIndex == endTimeIndex and startTimeIndex != -1 or startTimeIndex == -1 and endTimeIndex >= 0 or endTimeIndex == -1 and startTimeIndex >= 0:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_SETTING_TIME_FAILED, ())
            return
        setting = copy.deepcopy(BigWorld.player().yixinSetting)
        if startTimeIndex == -1 or endTimeIndex == -1:
            setting['enableBlockNotify'] = 0
        else:
            setting['enableBlockNotify'] = 1
        if startTimeIndex == -1:
            startTimeIndex = 25
        if endTimeIndex == -1:
            endTimeIndex = 25
        setting['notifyBlockStartTime'] = startTimeIndex
        setting['notifyBlockEndTime'] = endTimeIndex
        if otherLoginSetting:
            setting['notifyRareLogin'] = 1
        else:
            setting['notifyRareLogin'] = 0
        if salesSetting:
            setting['notifyTrade'] = 1
        else:
            setting['notifyTrade'] = 0
        oldSetting = dict(BigWorld.player().yixinSetting)
        if setting != oldSetting:
            BigWorld.player().base.setYixinSettings(setting)
        self.closeWidget()

    def howToConcern(self, *args):
        url = SCD.data.get('yixinHowToConcernUrl', '')
        BigWorld.openUrl(url)

    def howToAddGroup(self, *args):
        url = SCD.data.get('yixinHowToAddGroupUrl', '')
        BigWorld.openUrl(url)

    def getSettingData(self, *args):
        data = {}
        setting = BigWorld.player().yixinSetting
        if setting['enableBlockNotify']:
            data['startTime'] = setting['notifyBlockStartTime']
            data['endTime'] = setting['notifyBlockEndTime']
        else:
            data['startTime'] = -1
            data['endTime'] = -1
        data['isOtherLoginSetting'] = setting['notifyRareLogin']
        data['isSalesSetting'] = setting['notifyTrade']
        return uiUtils.dict2GfxDict(data, True)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def dismiss(self, *arg):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_SETTING)
        self.isShow = False
        self.mediator = None

    def toggle(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_SETTING)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_SETTING)
        self.isShow = not self.isShow

    def show(self):
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_SETTING)
        self.isShow = True
