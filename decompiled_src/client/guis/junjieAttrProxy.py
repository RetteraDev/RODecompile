#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/junjieAttrProxy.o
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import zhanxun_rank_data as ZRD

class JunjieAttrProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JunjieAttrProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_JUNJIE_ATTR, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_JUNJIE_ATTR:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JUNJIE_ATTR)

    def show(self):
        if self.mediator == None:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JUNJIE_ATTR)

    def onGetInitData(self, *arg):
        ret = []
        for key, val in ZRD.data.iteritems():
            info = {}
            info['sortIdx'] = key[0]
            info['rank'] = '%d~%d' % (key[0], key[1])
            info['value'] = val.get('rewardJunJie', 0)
            info['attr'] = val.get('desc', '')
            ret.append(info)

        ret.sort(key=lambda x: x['sortIdx'])
        return uiUtils.array2GfxAarry(ret, True)
