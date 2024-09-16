#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/pointGenProxy.o
import random
import csv
import BigWorld
from Scaleform import GfxValue
import gameglobal
import keys
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst
from helpers import navigator
from sMath import distance3D

class PointGenProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(PointGenProxy, self).__init__(uiAdapter)
        self.bindType = 'pointGen'
        self.modelMap = {'setConfig': self.onSetConfig}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_POINT_GEN:
            self.med = mediator

    def reset(self):
        self.pointNum = 0
        self.pointDist = 0
        self.pointArray = []
        self.callback = None
        self.waterHeight = -100000
        self.rightPos = False
        self.innerError = False
        self.med = None

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_POINT_GEN)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_POINT_GEN)

    def onSetConfig(self, *arg):
        spaceNo = int(arg[3][0].GetString())
        self.pointNum = int(arg[3][1].GetString())
        self.pointDist = float(arg[3][2].GetString())
        self.genPoint(spaceNo)

    def checkPosValid(self, newPos):
        if newPos == None:
            return False
        if newPos[1] <= self.waterHeight:
            return False
        for pos in self.pointArray:
            if distance3D(pos, newPos) < self.pointDist:
                return False

        return True

    def genPoint(self, spaceNo):
        if self.pointNum <= 0 or self.pointDist <= 0:
            return
        p = BigWorld.player()
        p.spaceNo = spaceNo
        if gameglobal.rds.isSinglePlayer:
            navigator.getNav().InitSeekNavsBySpaceNo(p.spaceNo)
            navigator.getNav().clearOtherNavs()
        else:
            p.cell.adminOnCell('$speed 10000')
        self.pointArray = []
        self.rightPos = True
        self.innerError = False
        BigWorld.callback(1, self._genPoint)

    def showResult(self):
        if self.med:
            if not self.innerError:
                output = '已经找到%s / %s个点' % (len(self.pointArray), self.pointNum)
                self.med.Invoke('showResult', GfxValue(gbk2unicode(output)))
            else:
                self.med.Invoke('showResult', GfxValue(gbk2unicode('如果是第一次出现，请重新点击确定')))

    def _genPoint(self):
        p = BigWorld.player()
        if len(self.pointArray) < self.pointNum and not self.innerError:
            if self.callback:
                BigWorld.cancelCallback(self.callback)
                self.callback = None
            self.callback = BigWorld.callback(0.5, self._genPoint)
            if BigWorld.spaceLoadStatus(50) < 1.0:
                return
            pos = p.position
            if keys.CAPS_SWIM in p.am.matchCaps:
                self.waterHeight = pos.y
                self.rightPos = False
                self.gotoNextPos(pos)
                return
            if self.rightPos:
                self.pointArray.append(pos.tuple())
                self.showResult()
                self.rightPos = False
                self.gotoNextPos(pos)
        else:
            if not self.rightPos:
                self.showResult()
            self.writeToFile()

    def writeToFile(self):
        csvfile = open('../res/universes/pointGen.csv', 'w')
        o = csv.writer(csvfile)
        out_data = ['路点编号', '坐标']
        o.writerow(out_data)
        for key, value in enumerate(self.pointArray):
            array = [key, '%f, %f, %f' % value]
            o.writerow(array)

        csvfile.close()

    def gotoNextPos(self, pos):
        nav = navigator.getNav()
        index = 0
        innerIndex = 0
        while True:
            newPos = nav.getRandomPos(pos, random.randint(self.pointDist * (index + 1), self.pointDist * (index + 2)))
            if self.checkPosValid(newPos):
                self.teleport(newPos.x, newPos.y, newPos.z)
                self.rightPos = True
                return
            index += 1
            if index == 10:
                index = 1
                innerIndex += 1
                newPos = random.choice(self.pointArray)
                self.teleport(newPos[0], newPos[1], newPos[2])
                if innerIndex == 5:
                    self.innerError = True
                    return

    def teleport(self, x, y, z):
        p = BigWorld.player()
        p.physics.teleport((x, y, z))
