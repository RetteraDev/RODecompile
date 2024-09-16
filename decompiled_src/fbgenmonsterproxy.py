#Embedded file name: /WORKSPACE/data/entities/client/debug/fbgenmonsterproxy.o
from Scaleform import GfxValue
import BigWorld
import GUI
import Math
import csv
import gameglobal
import clientUtils
from guis.ui import unicode2gbk
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import ui

class GenMonster:

    def __init__(self, id, modelId, scale, terrel, action, note):
        self.id = id
        self.modelId = modelId
        self.scale = scale
        self.terrel = terrel
        self.action = action
        self.note = note
        self.position = BigWorld.player().position
        if terrel:
            pos = BigWorld.findDropPoint(BigWorld.player().spaceID, self.position)
            if pos:
                self.position = pos[0]
        self.yaw = BigWorld.player().yaw
        self.placeMonster()

    def placeMonster(self):
        path = '%s%d/%d.model' % (gameglobal.charRes, self.modelId, self.modelId)
        self.model = clientUtils.model(path)
        BigWorld.player().addModel(self.model)
        self.model.position = self.position
        self.model.yaw = self.yaw
        try:
            self.model.scale = (self.scale, self.scale, self.scale)
            self.model.action(str(self.action))()
        except:
            pass

        self.i = GUI.WorldLabelGUI('', ui.font18)
        self.i.source = self.model.matrix
        self.i.biasPos = Math.Vector3(0, 3, 0)
        self.i.text = str(self.id)
        self.i.visible = True
        self.i.maxDistance = 200
        self.i.colour = Math.Vector4(0, 255, 0, 254)
        GUI.addRoot(self.i)


class FbGenMonsterProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(FbGenMonsterProxy, self).__init__(uiAdapter)
        self.bindType = 'fbGenMonster'
        self.modelMap = {'addMonster': self.onAddMonster,
         'delMonster': self.onDelMonster,
         'exportCsv': self.onExportCsv,
         'clickItem': self.onClickItem,
         'clearAll': self.onClearAll}
        self.monsterData = {}
        self.selectMonsterKey = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FB_GEN_MONSTER:
            self.mediator = mediator
        self.updateMonsterData()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_GEN_MONSTER)
        if self.mediator:
            self.mediator.Invoke('show')

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.item = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_GEN_MONSTER)

    def genMonsterKey(self):
        if not self.monsterData:
            return 1
        return max(self.monsterData.keys()) + 1

    def onAddMonster(self, *arg):
        note = unicode2gbk(arg[3][0].GetString())
        model = int(arg[3][1].GetString())
        scale = float(arg[3][2].GetString())
        terrel = int(arg[3][3].GetString())
        action = str(arg[3][4].GetString())
        key = self.genMonsterKey()
        self.monsterData[key] = GenMonster(key, model, scale, terrel, action, note)
        self.updateMonsterData()

    def onDelMonster(self, *arg):
        if self.selectMonsterKey:
            if self.monsterData.has_key(self.selectMonsterKey):
                genMonster = self.monsterData[self.selectMonsterKey]
                try:
                    BigWorld.player().delModel(genMonster.model)
                    GUI.delRoot(genMonster.i)
                except:
                    pass

                del self.monsterData[self.selectMonsterKey]
        self.updateMonsterData()

    def onExportCsv(self, *arg):
        self.doExportCsv('FBMonster.csv')

    def doExportCsv(self, fileName):
        csvfile = open('../res/' + fileName, 'wb')
        o = csv.writer(csvfile)
        rows = []
        rows.append(['编号',
         '备注',
         '坐标',
         '面向',
         '模型编号',
         '放缩倍率',
         '动作编号',
         '是否贴地'])
        if self.monsterData:
            for key, value in self.monsterData.iteritems():
                array = [key,
                 value.note,
                 self.getPosStr(value.position),
                 '0,0,%s' % round(value.yaw, 3),
                 value.modelId,
                 value.scale,
                 value.action,
                 value.terrel]
                rows.append(array)

        o.writerows(rows)
        csvfile.close()

    def getPosStr(self, position):
        return '%s, %s, %s' % (round(position[0], 3), round(position[1], 3), round(position[2], 3))

    def onClickItem(self, *arg):
        data = arg[3][1].GetString()
        key = int(data.split(':')[0])
        self.selectMonsterKey = key

    def onClearAll(self, *arg):
        if self.monsterData:
            for _k, v in self.monsterData.iteritems():
                if v.model:
                    BigWorld.player().delModel(v.model)
                    v.model = None

            self.monsterData = {}
        self.updateMonsterData()

    def showFbGenMonster(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_FB_GEN_MONSTER)))

    def updateMonsterData(self):
        ar = self.movie.CreateArray()
        i = 0
        for key in sorted(self.monsterData.keys()):
            data = self.monsterData.get(key)
            strData = '%d:(%d, %s, %s, )' % (key,
             data.modelId,
             self.getPosStr(data.position),
             data.yaw)
            ar.SetElement(i, GfxValue(strData))
            i = i + 1

        self.mediator.Invoke('setMonsterData', ar)
