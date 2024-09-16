#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillCountdownProxy.o
import BigWorld
import clientcom
import Math
import const
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import Tweener
from data import sys_config_data as SCD

class SkillCountdownProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillCountdownProxy, self).__init__(uiAdapter)
        self.widgetMap = {}
        self.entityMap = {}
        self.dyingWidgetMap = {}
        self.tweenDataMap = {}
        self.timer = None
        self.unloadTimer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SKILL_COUNTDOWN:
            multiID = int(widget.multiID)
            self.widgetMap[multiID] = widget
            self.initUI(widget)
            tweenData = self.tweenDataMap.pop(multiID, None)
            if tweenData:
                widget.alpha = 1.0
                Tweener.addTween(widget, tweenData)
            self.stopTimer()
            self.updateTime()

    def clearWidget(self):
        for multiID, widget in self.widgetMap.iteritems():
            Tweener.removeTweens(widget)
            self.uiAdapter.unLoadWidget(multiID)

        self.widgetMap = {}

    def reset(self):
        self.entityMap = {}
        self.dyingWidgetMap = {}
        self.tweenDataMap = {}
        self.stopTimer()
        self.stopUnloadTimer()

    def initUI(self, widget):
        ASUtils.setHitTestDisable(widget, True)
        widget.spell.progress.setAngle(0, 360)
        widget.spell.progress.clockWise = True
        widget.guide.visible = False

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
        skillCountDownY = SCD.data.get('skillCountDownY', 4)
        now = BigWorld.player().getServerTime()
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
            widget.x = x - 128
            widget.y = y - 90
            if entityVal.get('castType') == const.COUNTDOWN_CAST_TYPE_SPELL:
                widget.spell.visible = True
                widget.guide.visible = False
                widget.spell.title.text = entityVal.get('skillName', '')
                if entityVal.get('isFadeOut', False):
                    currentValue = entityVal.get('fadeOutValue', 0)
                else:
                    startTime = entityVal.get('startTime', 0)
                    duration = entityVal.get('duration', 0)
                    currentValue = 100.0
                    if now - startTime >= duration:
                        self.startFadeOut(entityId, now)
                    elif duration > 0:
                        currentValue = currentValue * (now - startTime) / duration
                widget.spell.progress.currentValue = currentValue
            else:
                widget.spell.visible = False
                widget.guide.visible = True
                if not entityVal.get('isFadeOut', False):
                    startTime = entityVal.get('startTime', 0)
                    duration = entityVal.get('duration', 0)
                    if now - startTime >= duration:
                        self.startFadeOut(entityId, now)
                widget.guide.title.text = entityVal.get('skillName', '')

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

    def test(self, castType = 1, duration = 3, fadeOutTime = 10):
        ent = BigWorld.player().targetLocked
        self.showCountdown(ent.id, 'Skill Name', castType, duration, fadeOutTime)

    def showCountdown(self, entityId, skillName, castType, duration, fadeOutTime):
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
                multiID = self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_COUNTDOWN)
            self.entityMap[entityId] = {'skillName': skillName,
             'startTime': BigWorld.player().getServerTime(),
             'castType': castType,
             'duration': duration,
             'isFadeOut': False,
             'fadeOutValue': 0,
             'fadeOutTime': fadeOutTime,
             'multiID': multiID}
            self.tweenDataMap.pop(multiID, None)
            self.stopTimer()
            self.updateTime()
            return

    def closeCountdown(self, entityId):
        ent = BigWorld.entity(entityId)
        if not ent or not ent.inWorld:
            return
        if entityId not in self.entityMap:
            return
        self.startFadeOut(entityId, BigWorld.player().getServerTime())

    def startFadeOut(self, entityId, now):
        if entityId not in self.entityMap:
            return
        entityVal = self.entityMap.get(entityId, {})
        if entityVal.get('isFadeOut', False):
            return
        entityVal['isFadeOut'] = True
        startTime = entityVal.get('startTime', 0)
        duration = entityVal.get('duration', 0)
        currentValue = 100.0
        if duration > 0 and now - startTime < duration:
            currentValue = currentValue * (now - startTime) / duration
        entityVal['fadeOutValue'] = currentValue
        multiID = entityVal.get('multiID', 0)
        tweenData = {'time': entityVal.get('fadeOutTime', 0),
         'alpha': 0,
         'onComplete': self.fadeTweenComplete,
         'onCompleteParams': (multiID,)}
        widget = self.widgetMap.get(multiID)
        if widget:
            widget.alpha = 1.0
            Tweener.addTween(widget, tweenData)
        else:
            self.tweenDataMap[multiID] = tweenData

    def fadeTweenComplete(self, *args):
        multiID = int(args[3][0].GetNumber())
        self.dyingWidgetMap[multiID] = BigWorld.player().getServerTime()
        self.stopUnloadTimer()
        self.updateUnloadTime()
