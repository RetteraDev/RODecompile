#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/perFontTextProxy.o
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils

class PerFontTextProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PerFontTextProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTextData': self.onGetTextData}
        self.loadeds = {}
        self.loading = {}

    def checkNum(self):
        if len(self.loading) + len(self.loadeds) >= 2:
            ids = self.loadeds.keys() + self.loading.keys()
            minId = min(ids)
            if minId in self.loading:
                self.loading.pop(minId)
            else:
                self._asWidgetClose(uiConst.WIDGET_PERFONTTEXT, minId)

    def show(self, data):
        self.checkNum()
        multiID = self.uiAdapter.loadWidget(uiConst.WIDGET_PERFONTTEXT)
        self.loading[multiID] = data

    def onGetTextData(self, *arg):
        multiID = int(arg[3][0].GetString())
        if multiID in self.loading:
            msgInfo = self.loading.pop(multiID)
            self.loadeds[multiID] = msgInfo
            ret = {}
            ret['coord'] = msgInfo[0]
            ret['desc'] = msgInfo[1]
            ret['color'] = msgInfo[2]
            ret['duration'] = msgInfo[3]
            ret['size'] = msgInfo[4]
            ret['intervalFrame'] = msgInfo[5]
            ret['blackGround'] = msgInfo[6]
            ret['notMid'] = msgInfo[7]
            return uiUtils.dict2GfxDict(ret, True)

    def _asWidgetClose(self, widgetId, multiID):
        self.uiAdapter.unLoadWidget(multiID)
        if multiID in self.loadeds:
            self.loadeds.pop(multiID)

    def hide(self):
        for multiID in self.loadeds.keys():
            self.uiAdapter.unLoadWidget(multiID)

    def test(self):
        self.show([(0, 0),
         gameStrings.TEXT_PERFONTTEXTPROXY_62,
         16777215,
         60,
         20,
         0,
         0])
        self.show([(0, 0.04),
         'Come on boy, let me tell you how to dapao.',
         16777215,
         60,
         20,
         0,
         1])

    def test1(self):
        self.show([(0, 0.4),
         gameStrings.TEXT_PERFONTTEXTPROXY_62,
         16777215,
         5,
         20,
         0,
         0])
        self.show([(0, 0.44),
         'Come on boy, let me tell you how to dapao.',
         16777215,
         5,
         20,
         0,
         1])
