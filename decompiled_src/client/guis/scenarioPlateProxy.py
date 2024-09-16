#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/scenarioPlateProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils

class ScenarioPlateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ScenarioPlateProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetConfig}
        self.dataInfo = None
        self.totalTime = None
        self.plateCallback = None

    def closeScenarioPlate(self, destroy = True):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCENARIO_PLATE)
        if self.plateCallback:
            BigWorld.cancelCallback(self.plateCallback)
            self.plateCallback = None
        if destroy:
            self.reset()

    def reset(self):
        self.dataInfo = None
        self.totalTime = None

    def onGetConfig(self, *arg):
        return self.dataInfo

    def initData(self, path, leftX, rightX, topY, bottomY, time, array, smallPath, smallLeftX, smallTopY):
        gamelog.debug('initData', path, (leftX, topY), (rightX, bottomY), time, array)
        self.dataInfo = self.movie.CreateObject()
        self.dataInfo.SetMember('leftX', GfxValue(leftX))
        self.dataInfo.SetMember('rightX', GfxValue(rightX))
        self.dataInfo.SetMember('topY', GfxValue(topY))
        self.dataInfo.SetMember('bottomY', GfxValue(bottomY))
        self.dataInfo.SetMember('path', GfxValue(path))
        w, h, _, _ = BigWorld.getScreenState()
        self.dataInfo.SetMember('width', GfxValue(w))
        self.dataInfo.SetMember('height', GfxValue(h))
        self.dataInfo.SetMember('smallPath', GfxValue(smallPath))
        self.dataInfo.SetMember('smallLeftX', GfxValue(smallLeftX))
        self.dataInfo.SetMember('smallTopY', GfxValue(smallTopY))
        self.totalTime = time
        self._pushTransform(array)

    def initSwfData(self, swfName, time):
        self.dataInfo = uiUtils.dict2GfxDict({'swf': 1,
         'swfName': swfName})
        self.totalTime = time

    def _pushTransform(self, array):
        transform = self.movie.CreateArray()
        for i, item in enumerate(array):
            obj = self.movie.CreateObject()
            obj.SetMember('x', GfxValue(item[0]))
            obj.SetMember('y', GfxValue(item[1]))
            obj.SetMember('scale', GfxValue(item[2]))
            obj.SetMember('time', GfxValue(item[3]))
            transform.SetElement(i, obj)

        self.dataInfo.SetMember('transform', transform)

    def show(self):
        self.closeScenarioPlate(False)
        self.uiAdapter.loadWidget(uiConst.WIDGET_SCENARIO_PLATE)
        BigWorld.callback(self.totalTime, self.closeScenarioPlate)
