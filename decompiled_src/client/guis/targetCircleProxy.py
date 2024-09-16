#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/targetCircleProxy.o
import gamelog
from uiProxy import UIProxy

class TargetCircleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TargetCircleProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerTargetCircle': self.onRegisterTargetCircle}
        self.circleArr = {}
        self.circleShow = [1, 1, 1]
        self.circleInfo = {}
        self.isLoaded = False

    def onRegisterTargetCircle(self, *arg):
        mc = arg[3][0]
        index = int(arg[3][1].GetNumber())
        gamelog.debug('onRegisterTargetCircle', index)
        self.circleArr[index] = mc
        mc.SetVisible(False)
        if index in self.circleInfo.keys():
            index, x, y = self.circleInfo[index]
            if self.circleShow[index] == 0:
                mc.GotoAndPlay('nonactivated')
            else:
                mc.GotoAndPlay('Activated')
            self.showMc(mc, x, y)

    def showNoActive(self, index, x1, y1):
        mc = self.circleArr.get(index)
        if mc:
            if self.circleShow[index] == 1:
                self.circleShow[index] = 0
                mc.GotoAndPlay('nonactivated')
            self.showMc(mc, x1, y1)
        else:
            self.circleInfo[index] = (index, x1, y1)
            if self.circleShow[index] == 1:
                self.circleShow[index] = 0
            if not self.isLoaded:
                self.isLoaded = True
                self.uiAdapter.uiObj.Invoke('loadTargetCircle')

    def show(self, x, y, index = 0):
        mc = self.circleArr.get(index)
        if mc:
            if self.circleShow[index] == 0:
                self.circleShow[index] = 1
                mc.GotoAndPlay('Activated')
            self.showMc(mc, x, y)
        else:
            self.circleInfo[index] = (index, x, y)
            if self.circleShow[index] == 0:
                self.circleShow[index] = 1
            if not self.isLoaded:
                self.isLoaded = True
                self.uiAdapter.uiObj.Invoke('loadTargetCircle')

    def showMc(self, mc, x, y):
        mc.SetVisible(True)
        mc.SetX(x)
        mc.SetY(y)

    def hide(self, index = 0):
        if self.circleArr.has_key(index):
            circle = self.circleArr.get(index)
            if circle != None:
                circle.SetVisible(False)
            if self.circleInfo.has_key(index):
                self.circleInfo.pop(index)

    def hideAll(self):
        for circle in self.circleArr.values():
            circle.SetVisible(False)

        self.circleInfo = {}
