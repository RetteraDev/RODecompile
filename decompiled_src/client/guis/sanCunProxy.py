#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/sanCunProxy.o
from gamestrings import gameStrings
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class SanCunProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SanCunProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetData}
        self.mediator = None
        self.fbInfo = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SANCUN:
            self.mediator = mediator

    def show(self):
        if self.fbInfo:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SANCUN)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SANCUN)

    def setFbInfo(self, info):
        self.fbInfo.update(info)
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SANCUN)
        else:
            self.mediator.Invoke('refreshData', uiUtils.dict2GfxDict(self.getFbData(), True))

    def getFbData(self):
        ret = {}
        plant_submit = self.fbInfo.get('plant_submit', 0)
        insect_submit = self.fbInfo.get('insect_submit', 0)
        horn_submit = self.fbInfo.get('horn_submit', 0)
        shell_submit = self.fbInfo.get('shell_submit', 0)
        poison_submit = self.fbInfo.get('poison_submit', 0)
        plant_tip = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_PLANT, {}).get('text', '')
        insect_tip = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_INSECT, {}).get('text', '')
        horn_tip = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_HORN, {}).get('text', '')
        shell_tip = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_SHELL, {}).get('text', '')
        poison_tip = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_POISON, {}).get('text', '')
        ret['subData'] = [plant_submit,
         insect_submit,
         horn_submit,
         shell_submit,
         poison_submit]
        ret['tips'] = [plant_tip,
         insect_tip,
         horn_tip,
         shell_tip,
         poison_tip]
        ret['total'] = self.fbInfo.get('sancun_submit', 0)
        ret['maxValue'] = self.fbInfo.get('sancun_need', 0)
        sancun_material = self.fbInfo.get('sancun_material', 0)
        sancun_total = self.fbInfo.get('sancun_total', 0)
        ret['totalTip'] = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_NEED, {}).get('text', '')
        ret['descTip'] = GMD.data.get(GMDD.data.FUBEN_SANCUN_TIPS_TOTAL, {}).get('text', '')
        ret['desc'] = gameStrings.TEXT_SANCUNPROXY_60 % (sancun_material, sancun_total)
        return ret

    def onGetData(self, *arg):
        return uiUtils.dict2GfxDict(self.getFbData(), True)
