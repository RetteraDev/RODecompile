#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tweenMcProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
from guis.asObject import ASObject
from guis.asObject import ASUtils
from uiProxy import UIProxy
from data import fame_data as FD
from data import tween_data as TD
CLS_NAME_FAME = 'TweenMc_FameTween'
TWEEN_TYPE_FAME = 1
TYPE_MEDIATOR = 1
TYPE_WIDGET = 2

class TweenMcProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TweenMcProxy, self).__init__(uiAdapter)
        self.widget = None
        self.index = 0
        self.reset()
        self.preShowDataList = []

    def reset(self):
        self.tweenRecord = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TWEEN_MC:
            self.widget = widget
            ASUtils.setHitTestDisable(self.widget, True)
            for tweenData in self.preShowDataList:
                self.startTween(tweenData)

            self.preShowDataList = []

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TWEEN_MC)

    def startTween(self, tweenData):
        if not self.widget:
            self.preShowDataList.append(tweenData)
            self.show()
            return
        elif self.widget.x == None:
            self.preShowDataList.append()
            self.show()
            return
        else:
            insMc = self.widget.getInstByClsName(tweenData['clsName'])
            insMc.scaleX = 1.0
            insMc.scaleY = 1.0
            self.widget.addChild(insMc)
            if not insMc:
                gamelog.error('@jbx: clsName not Exist', tweenData['clsName'])
            insMc.x = tweenData['startPos'][0]
            insMc.y = tweenData['startPos'][1]
            self.tweenRecord[self.index] = (insMc, tweenData)
            for frameNum, callBack in tweenData['timeLineInfo']:
                ASUtils.callbackAtFrame(insMc, frameNum, callBack, self.index)

            self.index += 1
            return

    def tweenEnd(self, *args):
        index = int(args[3].getNumber())
        mc = self.tweenRecord.pop(index, None)
        if mc:
            self.widget.removeToCache(mc)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TWEEN_MC)

    def tweenFame(self, fameId):
        if not gameglobal.rds.configData.get('enableHonorV2', False):
            return
        else:
            tweenData = {}
            tweenData['clsName'] = CLS_NAME_FAME
            td = TD.data.get(TWEEN_TYPE_FAME, {})
            tweenData['time'] = td.get('time', 1.5)
            tweenData['startPos'] = td.get('startPos', (0, 0))
            tweenData['endTarget'] = td.get('endTarget', None)
            timeLineInfoList = []
            tweenData['params'] = fameId
            timeLineInfoList.append((1, self.loadFameIcon))
            timeLineInfoList.append((8, self.loadFameIcon2))
            timeLineInfoList.append((11, self.setText))
            timeLineInfoList.append((60, self.moveFun))
            tweenData['timeLineInfo'] = timeLineInfoList
            self.startTween(tweenData)
            return

    def getTweenPos(self, ins, endTargetData):
        type, gfxValueName, propList, offset = endTargetData
        widget = None
        if type == TYPE_MEDIATOR:
            widget = ASObject(eval('self.uiAdapter.%s' % gfxValueName))
            if not widget or not widget.getWidget:
                return (0, 0)
            widget = widget.getWidget()
        else:
            widget = eval('self.uiAdapter.%s' % gfxValueName)
        if not widget:
            raise Exception('@jbx: widget not find', type, gfxValueName)
        mc = widget
        for prop in propList:
            mc = getattr(mc, prop, None)
            if mc == None:
                raise Exception('@jbx: prop not find', propList)

        posX = mc.x + offset[0]
        posY = mc.y + offset[1]
        globalPos = ASUtils.local2Global(mc, posX, posY)
        targetPosLocal = ASUtils.global2Local(ins, globalPos[0], globalPos[1])
        return (targetPosLocal[0], targetPosLocal[1])

    def loadFameIcon(self, *args):
        index = int(ASObject(args[3][0])[0])
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        if not ins or not tweenData or not ins.icon:
            return
        else:
            fameID = tweenData['params']
            value = FD.data.get(fameID, None)
            icon = 'fame/fame156/%s.dds' % value.get('icon', '')
            ins.icon.fitSize = True
            ins.icon.fameIcon.loadImage(icon)
            return

    def setText(self, *args):
        index = int(ASObject(args[3][0])[0])
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        if not ins or not tweenData or not ins.txtName:
            return
        else:
            fameID = tweenData['params']
            value = FD.data.get(fameID, None)
            ins.txtName.txt.text = value.get('name', '')
            return

    def loadFameIcon2(self, *args):
        index = int(ASObject(args[3][0])[0])
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        if not ins or not tweenData or not ins.icon2:
            return
        else:
            fameID = tweenData['params']
            value = FD.data.get(fameID, None)
            icon = 'fame/fame156/%s.dds' % value.get('icon', '')
            ins.icon2.fitSize = True
            ins.icon2.fameIcon.loadImage(icon)
            return

    def moveFun(self, *args):
        index = int(ASObject(args[3][0])[0])
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        if not ins or not tweenData:
            return None
        else:
            targetPos = self.getTweenPos(ins, tweenData['endTarget'])
            ASUtils.addTweener(ins, {'time': tweenData['time'],
             'x': targetPos[0],
             'y': targetPos[1],
             'onCompleteParams': (index,),
             'scaleX': 0.2,
             'scaleY': 0.2}, self.endTween)
            return None

    def getData(self, *args):
        index = int(ASObject(args[3][0])[0])
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        return (index, ins, tweenData)

    def endTween(self, *args):
        index = int(args[3][0].GetNumber())
        ins, tweenData = self.tweenRecord.get(index, (None, None))
        self.tweenRecord.pop(index, None)
        if ins and ins.x != None:
            self.widget.removeToCache(ins)
        if len(self.tweenRecord) == 0:
            self.hide()
