#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wenQuanDetailProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import gamelog
import const
import keys
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from data import sys_config_data as SCD

class WenQuanDetailProxy(UIProxy):
    JIU_BUFFS = (39029, 39040, 39041, 39046, 39047, 39318, 39319, 39320, 39321, 39322, 39410, 39412, 39883)
    SHAO_KAO_BUFFS = (39231, 39232, 39233, 39323, 39324, 39325, 39411, 39413)

    def __init__(self, uiAdapter):
        super(WenQuanDetailProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickAutoPopoCkBox': self.onClickAutoPopoCkBox}
        self.mediator = None
        self.isShow = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WENQUAN_DETAIL:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self.getWenQuanDetailData(), True)

    def shouldUpdate(self):
        if not self.mediator:
            return False
        if not hasattr(BigWorld.player(), 'mapID') or BigWorld.player().mapID != const.ML_SPACE_NO_WENQUAN_FLOOR1:
            return False
        return True

    def updateState(self, oldState):
        if not self.shouldUpdate():
            return
        p = BigWorld.player()
        statesKey = p.getStates().keys()
        oldStateKey = oldState.keys()
        jiuBuffs = SCD.data.get('wenQuanJiuBuffs', WenQuanDetailProxy.JIU_BUFFS)
        shaoKaoBuffs = SCD.data.get('shaoKaoBuffs', WenQuanDetailProxy.SHAO_KAO_BUFFS)
        checkBuffs = jiuBuffs + shaoKaoBuffs
        updateFlag = False
        for buff in checkBuffs:
            if buff not in statesKey and buff in oldStateKey:
                updateFlag = True
                break
            if buff in statesKey and buff not in oldStateKey:
                updateFlag = True
                break

        if updateFlag:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self.getWenQuanDetailData(), True))

    def updateValue(self):
        if not self.shouldUpdate():
            return
        self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self.getWenQuanDetailData(), True))

    def getWenQuanDetailData(self):
        p = BigWorld.player()
        ret = {}
        ret['jiuLi'] = p.fame.get(gametypes.RECOMMEND_WENQUAN_JIULI, 0)
        ret['shiLiang'] = p.fame.get(gametypes.RECOMMEND_WENQUAN_SHILIANG, 0)
        ret['exp'] = p.dailyWenquanExp
        ret['socExp'] = p.dailyWenquanSocExp
        jiuBuffs = set(SCD.data.get('wenQuanJiuBuffs', WenQuanDetailProxy.JIU_BUFFS))
        shaoKaoBuffs = set(SCD.data.get('shaoKaoBuffs', WenQuanDetailProxy.SHAO_KAO_BUFFS))
        statesKey = set(p.getStates().keys())
        jiuAch = False
        jiuStr = gameStrings.TEXT_WENQUANDETAILPROXY_87
        if statesKey & jiuBuffs:
            jiuAch = True
            jiuStr = gameStrings.TEXT_WENQUANDETAILPROXY_90
        shaoKaoAch = False
        shaoKaoStr = gameStrings.TEXT_WENQUANDETAILPROXY_93
        if statesKey & shaoKaoBuffs:
            shaoKaoAch = True
            shaoKaoStr = gameStrings.TEXT_WENQUANDETAILPROXY_96
        ret['jiuName'] = gameStrings.TEXT_WENQUANDETAILPROXY_98
        ret['jiuAch'] = jiuAch
        ret['jiuStr'] = jiuStr
        ret['shaoKaoName'] = gameStrings.TEXT_WENQUANDETAILPROXY_101
        ret['shaoKaoAch'] = shaoKaoAch
        ret['shaoKaoStr'] = shaoKaoStr
        autoOpen = AppSettings.get(keys.SET_UI_AUTO_OPEN_WENQUAN_DETAIL, 1)
        ret['isAutoOpen'] = autoOpen
        ret['autoOpenLabel'] = gameStrings.TEXT_WENQUANDETAILPROXY_108
        gamelog.debug('jjh@wenquan getWenQuanDetailData', ret)
        return ret

    def show(self):
        if not gameglobal.rds.configData.get('enableWenQuanDetail', False):
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WENQUAN_DETAIL)
        self.isShow = True

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WENQUAN_DETAIL)

    def reset(self):
        self.mediator = None

    def onClickAutoPopoCkBox(self, *arg):
        isSelected = arg[3][0].GetBool()
        flag = AppSettings.get(keys.SET_UI_AUTO_OPEN_WENQUAN_DETAIL, 1)
        if isSelected and flag != 0:
            AppSettings[keys.SET_UI_AUTO_OPEN_WENQUAN_DETAIL] = 0
            AppSettings.save()
        elif not isSelected and flag != 1:
            AppSettings[keys.SET_UI_AUTO_OPEN_WENQUAN_DETAIL] = 1
            AppSettings.save()
