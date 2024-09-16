#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/lifeLinkManager.o
import BigWorld
import Math
import gameglobal
import utils
import gamelog
from gameclass import Singleton
from sfx import sfx
from data import life_link_data as LLD

class LifeLinkInfo(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.linkEffect = None
        self.entId1 = 0
        self.entId2 = 0
        self.stateId = 0
        self.linkInfo = None
        self.isOk = False
        self.lastTriggerTime = 0
        self.linkId = 0
        self.interval = -1
        self.radius = 0
        self.isImpact = False
        self.isInTrigger = False
        self.oldPosition = None
        self.areaArg2 = 0
        self.areaArg3 = 0

    def init(self, key, linkInfo):
        self.entId1, self.entId2, self.stateId = key
        self.linkInfo = linkInfo
        self.linkId = linkInfo.get('linkId', None)
        lld = LLD.data.get(self.linkId, {})
        self.interval = lld.get('interval', -1)
        self.isImpact = lld.get('isImpact', False)
        self.radius = lld.get('areaArg', 0) * 0.5
        self.areaArg2 = lld.get('areaArg2', 0)
        self.areaArg3 = lld.get('areaArg3', 0)

    def start(self):
        if self.isOk:
            return
        if not self.linkId:
            return
        lld = LLD.data.get(self.linkId, {})
        effect = lld.get('effect', 2315)
        distance = lld.get('distance', 20)
        ent1 = BigWorld.entity(self.entId1)
        ent2 = BigWorld.entity(self.entId2)
        nodeName = lld.get('node', None)
        if not ent1 or not ent1.inWorld or not getattr(ent1, 'firstFetchFinished', False):
            return
        if not ent2 or not ent2.inWorld or not getattr(ent2, 'firstFetchFinished', False):
            return
        if nodeName:
            startNode = ent1.model.node(nodeName)
            endNode = ent2.model.node(nodeName)
        else:
            startNode = ent1.model.node('biped')
            endNode = ent2.model.node('biped')
        if effect:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (ent1.getSkillEffectLv(),
             startNode,
             effect,
             endNode,
             distance + 10,
             ent1.getSkillEffectPriority()))
            self.linkEffect = fx
            self.isOk = True

    def stop(self):
        if self.linkEffect:
            self.linkEffect.release()
        self.reset()

    def checkTrigger(self):
        now = utils.getNow()
        if not self.isImpact:
            return
        if not self.radius:
            return
        if not self.isOk:
            return
        ent1 = BigWorld.entity(self.entId1)
        ent2 = BigWorld.entity(self.entId2)
        if not ent1 or not ent1.inWorld:
            return
        if not ent2 or not ent2.inWorld:
            return
        player = BigWorld.player()
        if player == ent1 or player == ent2:
            return
        pos1 = Math.Vector2(ent1.position.x, ent1.position.z)
        pos2 = Math.Vector2(ent2.position.x, ent2.position.z)
        player = BigWorld.player()
        p = Math.Vector2(player.position.x, player.position.z)
        dir = pos2 - pos1
        rawDist = (p - (pos1 + pos2) * 0.5).length
        if rawDist > dir.length * 0.5 + self.radius:
            return
        dir.normalise()
        crossDir = Math.Vector2(-dir.y, dir.x)
        crossDir *= self.radius
        p0 = pos1 + crossDir
        p1 = pos1 - crossDir
        p2 = pos2 + crossDir
        p3 = pos2 - crossDir
        if utils.isInRectangle(p0, p2, p3, p1, p):
            if not self.isInTrigger and self.heightCheck(ent1.position, ent2.position, player.position, self.areaArg2, self.areaArg3):
                gamelog.debug('bgf@LifeLinkInfo checkTrigger', self.lastTriggerTime, now)
                self.isInTrigger = True
                self.lastTriggerTime = now
                ent1.cell.triggerLifeLinkCalc(player.id, ent2.id)
        elif not self.isInTrigger and self.oldPosition and utils.isLineSegmentJudge(pos1, pos2, p, self.oldPosition) and self.heightCheck(ent1.position, ent2.position, player.position, self.areaArg2, self.areaArg3):
            self.isInTrigger = False
            self.lastTriggerTime = now
            ent1.cell.triggerLifeLinkCalc(player.id, ent2.id)
        else:
            self.isInTrigger = False
        self.oldPosition = p

    def heightCheck(self, p0, p2, p, upHeight, downHeight):
        horizonP0 = Math.Vector2(p0.x, p0.z)
        horizonP2 = Math.Vector2(p2.x, p2.z)
        horizonP = Math.Vector2(p.x, p.z)
        diff20 = (horizonP2 - horizonP0).length
        diff = (horizonP - horizonP0).length
        if diff20 > 0.1:
            y = diff / diff20 * (p2.y - p0.y) + p0.y
        else:
            y = p0.y
        if p.y >= y + upHeight or p.y <= y - downHeight:
            return False
        return True


def getInstance():
    return LifeLinkManager.getInstance()


class LifeLinkManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.reset()

    def reset(self):
        self.lifeLink = {}
        self.callbackHandle = None
        self.interval = 0.1

    def release(self):
        self.stopCheckTrigger()
        for key in self.lifeLink.keys():
            lifeLink = self.lifeLink.pop(key)
            lifeLink.stop()

        self.reset()

    def removeEnt(self, entId):
        for key in self.lifeLink.keys():
            if entId == key[0] or entId == key[1]:
                lifeLink = self.lifeLink.pop(key, None)
                lifeLink.stop()

    def stopCheckTrigger(self):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
            self.callbackHandle = None

    def startCheckTrigger(self):
        self.stopCheckTrigger()
        if not self.lifeLink:
            return
        for value in self.lifeLink.itervalues():
            value.checkTrigger()

        self.callbackHandle = BigWorld.callback(0.1, self.startCheckTrigger)

    def update(self, entId, linkInfos):
        oldSet = set()
        for key in self.lifeLink.iterkeys():
            if entId == key[0] or entId == key[1]:
                oldSet.add(key)

        newSet = set()
        for stateId, linkInfo in linkInfos.iteritems():
            linkedEntIds = linkInfo.get('linkedEntIds', set())
            for linkedEntId in linkedEntIds:
                if entId != linkedEntId:
                    minEntId = min(entId, linkedEntId)
                    maxEntId = max(entId, linkedEntId)
                    newSet.add((minEntId, maxEntId, stateId))

        removeSet = oldSet - newSet
        for key in removeSet:
            lifeLinkInfo = self.lifeLink.pop(key, None)
            lifeLinkInfo.stop()

        addSet = newSet - oldSet
        for key in addSet:
            lifeLinkInfo = LifeLinkInfo()
            lifeLinkInfo.init(key, linkInfos.get(key[-1]))
            self.lifeLink[key] = lifeLinkInfo

        for stateId, linkInfo in self.lifeLink.iteritems():
            linkInfo.start()

        gamelog.debug('bgf@lifeLinkManager update', newSet, oldSet, self.lifeLink)
        if self.lifeLink:
            self.startCheckTrigger()
