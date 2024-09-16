#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/walkLineEditProxy.o
from Scaleform import GfxValue
import BigWorld
import ResMgr
import gameglobal
import gamelog
from helpers import walkLineEditor
from helpers import navigator
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst

class WalkLineEditProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(WalkLineEditProxy, self).__init__(uiAdapter)
        self.bindType = 'walkLineEdit'
        self.modelMap = {'chooseFile': self.onChooseFile,
         'choosePoint': self.onChoosePoint,
         'register': self.onRegister,
         'fileControl': self.onFileControl,
         'pointControl': self.onPointControl,
         'getFileName': self.sendFileName}
        self.mapFun = {'addPointBtn': self.addPoint,
         'delPointBtn': self.delPoint,
         'addConBtn': self.addConnection,
         'delConBtn': self.delConnection,
         'clearBtn': self.clearSpace,
         'jumpBtn': self.jumpTo,
         'exportBtn': self.export,
         'compileBtn': self.compile,
         'exportStoneWayBtn': self.exportStoneWay,
         'dropPointBtn': self.dropPoint,
         'exportFlyBtn': self.exportFlyBtn}
        self.editor = walkLineEditor.WalkLineEditor.getInstance()
        self.fileList = []
        self.mc = None

    def generateFileArray(self):
        self.fileList = []
        file = ResMgr.openSection(self.editor.SAVE_PATH)
        if file:
            for fileName in file.keys():
                if fileName.endswith('.xml'):
                    self.fileList.append(fileName)

        gamelog.debug('bgf:generateFileArray', self.fileList)

    def sendFileArray(self):
        ar = self.movie.CreateArray()
        for i, fileName in enumerate(self.fileList):
            value = GfxValue(gbk2unicode(fileName))
            ar.SetElement(i, value)

        return ar

    def getValue(self, key):
        if key == 'walkLineEdit.fileList':
            self.generateFileArray()
            return self.sendFileArray()

    def onChooseFile(self, *arg):
        fileName = arg[3][1].GetString()
        self.clearSpace()
        self.editor.readPoints(self.editor.SAVE_PATH + fileName)
        self.updateChoice(self.editor.getCurrentPoint(), self.editor.getLastPoint())
        self.updatePointData()

    def onChoosePoint(self, *arg):
        point = arg[3][1].GetString()
        index = int(point.split(':')[0])
        gamelog.debug('bgf:onChoosePoint', index, point)
        self.editor.setCurrent(index)
        self.updateChoice(self.editor.getCurrentPoint(), self.editor.getLastPoint())
        self.updatePointData()

    def onRegister(self, *arg):
        self.mc = arg[3][0]

    def onFileControl(self, *arg):
        gamelog.debug('bgf:onFileControl', arg[3][0].GetString())
        btnName = arg[3][0].GetString()
        if btnName == 'saveBtn':
            fileName = arg[3][1].GetString()
            if self.editor.savePoints(fileName):
                if fileName in self.fileList:
                    self.fileList.remove(fileName)
                self.fileList.append(fileName)
                return self.sendFileArray()
        elif btnName == 'saveSpaceNoBtn':
            spaceNo = int(arg[3][1].GetString())
            p = BigWorld.player()
            BigWorld.player().spaceNo = spaceNo
            if gameglobal.rds.isSinglePlayer:
                navigator.getNav().InitSeekNavsBySpaceNo(p.spaceNo)
                navigator.getNav().clearOtherNavs()
        elif btnName == 'exportCsvBtn':
            self.editor.savePointAsCSV('point.csv')

    def onPointControl(self, *arg):
        btnName = arg[3][0].GetString()
        self.mapFun[btnName]()

    def addPoint(self):
        self.editor.addPoint()
        self.updateChoice(self.editor.getCurrentPoint(), self.editor.getLastPoint())
        self.updatePointData()

    def delPoint(self):
        self.editor.delPoint()
        self.updateChoice(self.editor.getCurrentPoint(), self.editor.getLastPoint())
        self.updatePointData()

    def addConnection(self):
        self.editor.connectPoints()

    def delConnection(self):
        self.editor.dconnectPoints()

    def clearSpace(self):
        self.editor.clearCurSpace()
        self.updateChoice(self.editor.getCurrentPoint(), self.editor.getLastPoint())
        self.updatePointData()

    def jumpTo(self):
        self.editor.pfToSelect()

    def sendFileName(self, *arg):
        p = BigWorld.player()
        ret = 'space_' + str(p.spaceNo) + '.xml'
        return GfxValue(ret)

    def export(self, *arg):
        self.editor.exportPoints()

    def exportStoneWay(self, *arg):
        self.editor.starCalStone()

    def dropPoint(self, *arg):
        self.editor.dropPoint()

    def compile(self):
        self.editor.compilePoints()

    def showWalkLineEdit(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_WALKLINE)))

    def updateChoice(self, curPoint, lastPoint):
        curStr = 'None'
        lastStr = 'None'
        if curPoint:
            curStr = '%d:(%.2f, %.2f, %.2f)' % (curPoint.num,
             curPoint.pos[0],
             curPoint.pos[1],
             curPoint.pos[2])
        if lastPoint:
            lastStr = '%d:(%.2f, %.2f, %.2f)' % (lastPoint.num,
             lastPoint.pos[0],
             lastPoint.pos[1],
             lastPoint.pos[2])
        self.mc.Invoke('setChoicePoint', (GfxValue(curStr), GfxValue(lastStr)))

    def updatePointData(self):
        pointData = self.editor.getPoints()
        ar = self.movie.CreateArray()
        i = 0
        for index, value in sorted(pointData.items(), key=lambda d: d[0]):
            str = '%d:(%.2f, %.2f, %.2f)' % (value.num,
             value.pos[0],
             value.pos[1],
             value.pos[2])
            ar.SetElement(i, GfxValue(str))
            i = i + 1

        gamelog.debug('bgf:updatePointData', pointData, i)
        self.mc.Invoke('setPointData', ar)

    def exportFlyBtn(self, *arg):
        self.editor.exportFlyPoints()
