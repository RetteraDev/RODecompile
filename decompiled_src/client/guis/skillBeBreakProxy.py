#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillBeBreakProxy.o
import BigWorld
import clientcom
import Math
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import Tweener
from data import sys_config_data as SCD

class SkillBeBreakProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillBeBreakProxy, self).__init__(uiAdapter)
        self.widgetMap = {}
        self.entityMap = {}
        self.dyingWidgetMap = {}
        self.timer = None
        self.unloadTimer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SKILL_BE_BREAK:
            self.widgetMap[int(widget.multiID)] = widget
            self.initUI(widget)
            self.refreshInfo(widget)

    def clearWidget(self):
        for multiID, widget in self.widgetMap.iteritems():
            Tweener.removeTweens(widget)
            self.uiAdapter.unLoadWidget(multiID)

        self.widgetMap = {}

    def reset(self):
        self.entityMap = {}
        self.dyingWidgetMap = {}
        self.stopTimer()
        self.stopUnloadTimer()

    def initUI(self, widget):
        ASUtils.setHitTestDisable(widget, True)
        widget.beBreak.visible = False
        widget.callback = 0

    def refreshInfo(self, widget):
        entityId = 0
        multiID = int(widget.multiID)
        for key, entityVal in self.entityMap.iteritems():
            if entityVal.get('multiID') == multiID:
                entityId = key
                break

        if entityId == 0:
            return
        if widget.callback:
            ASUtils.cancelCallBack(widget.callback)
        widget.callback = ASUtils.callbackAtFrame(widget.beBreak, widget.beBreak.totalFrames, self.startFadeOut, entityId)
        widget.beBreak.visible = True
        widget.beBreak.gotoAndPlay(1)
        self.stopTimer()
        self.updateTime()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def stopUnloadTimer(self):
        if self.unloadTimer:
            BigWorld.cancelCallback(self.unloadTimer)
            self.unloadTimer = None

    def updateTime(self):
        needUpdate = False
        skillCountDownY = SCD.data.get('skillBeBreakY', 4)
        for entityId, entityVal in self.entityMap.iteritems():
            multiID = entityVal.get('multiID', 0)
            if multiID in self.dyingWidgetMap:
                continue
            widget = self.widgetMap.get(multiID)
            if not widget:
                continue
            ent = BigWorld.entity(entityId)
            if not ent or not ent.inWorld:
                widget.visible = False
                continue
            needUpdate = True
            widget.visible = True
            pos = Math.Vector3(ent.position)
            pos.y += skillCountDownY
            x, y = clientcom.worldPointToScreen(pos)
            widget.x = x - 110
            widget.y = y - 90

        if needUpdate:
            self.timer = BigWorld.callback(0.02, self.updateTime)

    def updateUnloadTime(self):
        needUpdate = False
        now = BigWorld.player().getServerTime()
        for multiID in self.dyingWidgetMap.keys():
            if now - self.dyingWidgetMap[multiID] > 90:
                self.dyingWidgetMap.pop(multiID, None)
                widget = self.widgetMap.pop(multiID, None)
                if widget:
                    Tweener.removeTweens(widget)
                self.uiAdapter.unLoadWidget(multiID)
            else:
                needUpdate = True

        if needUpdate:
            self.unloadTimer = BigWorld.callback(100, self.updateUnloadTime)

    def test(self, fadeOutTime = 10):
        ent = BigWorld.player().targetLocked
        self.show(ent.id, fadeOutTime)

    def show(self, entityId, fadeOutTime):
        ent = BigWorld.entity(entityId)
        if not ent or not ent.inWorld:
            return
        else:
            if entityId in self.entityMap:
                multiID = self.entityMap.get(entityId, {}).get('multiID', 0)
            else:
                multiID = 0
            if multiID in self.widgetMap:
                self.dyingWidgetMap.pop(multiID, None)
                widget = self.widgetMap.get(multiID)
                if widget:
                    widget.alpha = 1.0
                    Tweener.removeTweens(widget)
            else:
                widget = None
                multiID = self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_BE_BREAK)
            self.entityMap[entityId] = {'fadeOutTime': fadeOutTime,
             'multiID': multiID}
            if widget:
                self.refreshInfo(widget)
            return

    def startFadeOut(self, *args):
        entityId = int(ASObject(args[3][0])[0])
        if entityId not in self.entityMap:
            return
        entityVal = self.entityMap.get(entityId, {})
        multiID = entityVal.get('multiID', 0)
        widget = self.widgetMap.get(multiID)
        if not widget:
            return
        widget.alpha = 1.0
        tweenData = {'time': entityVal.get('fadeOutTime', 0),
         'alpha': 0,
         'onComplete': self.fadeTweenComplete,
         'onCompleteParams': (multiID,)}
        Tweener.addTween(widget, tweenData)

    def fadeTweenComplete(self, *args):
        multiID = int(args[3][0].GetNumber())
        self.dyingWidgetMap[multiID] = BigWorld.player().getServerTime()
        self.stopUnloadTimer()
        self.updateUnloadTime()
