#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/equipFashionChangeProxy.o
import cPickle
import BigWorld
import gameglobal
import const
import utils
from helpers import charRes
from helpers import avatarMorpher as AM
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils

class EquipFashionChangeProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(EquipFashionChangeProxy, self).__init__(uiAdapter)
        self.bindType = 'equipFashionChange'
        self.modelMap = {'confirm': self.onConfirm,
         'cancel': self.onCancel,
         'testColor': self.onTestColor}
        self.mediator = None
        self.resList = None
        self.dataDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_DEBUG_EQUIP_FASHION_CHANGE, self.clearWidget)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DEBUG_EQUIP_FASHION_CHANGE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DEBUG_EQUIP_FASHION_CHANGE:
            self.mediator = mediator

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.resList = None
        self.dataDict = {}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            self.resList = None
            self.dataDict = {}
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DEBUG_EQUIP_FASHION_CHANGE)

    def onConfirm(self, *arg):
        info = arg[3][0]
        dataArray = uiUtils.gfxArray2Array(info)
        dataDict = {}
        dataDict['sex'] = int(dataArray[0].GetNumber())
        dataDict['bodyType'] = int(dataArray[1].GetNumber())
        dataDict['hair'] = int(dataArray[2].GetNumber())
        dataDict['body'] = int(dataArray[3].GetNumber())
        dataDict['hand'] = int(dataArray[4].GetNumber())
        dataDict['leg'] = int(dataArray[5].GetNumber())
        dataDict['shoe'] = int(dataArray[6].GetNumber())
        dataDict['transModelId'] = False
        dataDict['multiPart'] = True
        if dataDict['sex'] == const.SEX_FEMALE and dataDict['bodyType'] == const.BODY_TYPE_5:
            dataDict['bodyType'] = const.BODY_TYPE_3
        self.showModel(dataDict)

    def showModel(self, dataDict):
        self.dataDict = dataDict
        mpr = charRes.convertToMultiPartRes(dataDict)
        mpr.isAvatar = False
        self.resList = mpr.getPrerequisites()
        BigWorld.player().modelServer.bodyUpdateOffLine(self.resList)

    def onCancel(self, *arg):
        self.hide()

    def onTestColor(self, *arg):
        btnName = arg[3][0].GetString()
        color = arg[3][1].GetString()
        gameglobal.APPLY_NEW_SKIN_MODEL = True
        if btnName == 'confirm1':
            color = color.split(';')
            dyeList = utils.addDyeLists([], const.DYES_INDEX_COLOR, color)
            dyeList = utils.addDyeLists(dyeList, const.DYES_INDEX_DUAL_COLOR, color)
            dyesDict = {}
            for part in charRes.PARTS_ASPECT:
                dyesDict[part] = dyeList

            self.dataDict['dyesDict'] = dyesDict
        else:
            map = {'faceMorphs': '68:0.55\n12:0.65\n26:0.40\n33:0.85\n70:0.80\n51:0.10\n20:0.25\n48:0.45\n59:0.65\n55:0.10\n71:0.30\n57:0.15\n35:0.70\n74:0.35\n24:0.40\n8:0.60\n46:0.15\n21:1.00\n10:0.15\n62:0.25\n18:0.25',
             'dyeMode': 1L,
             'eyeDyes': '205:1\n206:67,50,44,300\n207:240,240,240,400\n208:1.48\n237:67,50,44,300\n238:240,240,240,400\n239:1\n240:240,240,240,600',
             'headDyes': '209:1\n211:4\n212:68,68,68,255\n210:1.4\n213:3\n214:45,45,45,255\n215:1.26\n216:70,70,70,255\n217:0.55\n218:2.3\n219:13.55\n221:0.54\n222:164,72,31,255\n223:0.32\n224:0.93\n225:50.6\n227:5\n201:228,222,211,255\n202:0.18\n203:40.4\n226:4\n228:1\n229:0.0\n230:0.0\n231:0.04\n232:0.0\n233:230,200,242,255\n234:0.5\n235:200.0\n236:1',
             'bodyBones': '135:0.45\n148:0.45\n104:0.35\n142:0.50\n108:0.40\n119:0.80\n133:0.50\n110:0.20\n125:1.00\n111:0.05\n138:0.10\n118:0.15\n145:0.55\n116:0.50\n123:0.60\n114:0.05\n106:0.40\n101:0.50\n139:1.00\n122:0.30\n143:0.20',
             'faceBones': '28:0.05\n41:0.15\n15:0.35\n66:0.50\n2:0.45\n5:0.65\n44:0.15\n39:0.70\n38:0.25\n13:0.25\n30:0.10\n63:0.25\n4:0.05\n32:0.50',
             'fxType': 1L,
             'skinDyes': '201:228,222,211,255\n202:0.18\n203:40.4',
             'hairDyes': '204:40,30,30,300|55,45,45,250|72,45,15,250|18.00'}
            map['skinDyes'] = '\n'.join(('201:' + color, '202:0.2', '203:40'))
            avatarConfig = cPickle.dumps(map)
            self.dataDict['avatarConfig'] = avatarConfig
        data = self.dataDict
        m = AM.SimpleModelMorpher(BigWorld.player().model, data['sex'], const.SCHOOL_SHENTANG, data['bodyType'], 0, data['hair'], 0, data['body'], data['hand'], data['leg'], data['shoe'], data['transModelId'], charRes.HEAD_TYPE0, data.get('dyesDict', {}))
        m.readConfig(data.get('avatarConfig', ''))
        m.apply()
