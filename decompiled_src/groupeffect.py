#Embedded file name: /WORKSPACE/data/entities/client/sfx/groupeffect.o
import random
import math
import BigWorld
import Pixie
import Math
import gamelog
import sfx
import gameglobal
import clientUtils

class MultiCache(object):

    def __init__(self):
        self.map = {}

    def has_key(self, id):
        if self.map.has_key(id) and len(self.map[id]):
            return True
        else:
            return False

    def pop(self, id):
        if self.has_key(id):
            effect = self.map[id].pop(0)
            return effect
        else:
            return None

    def push(self, id, effect):
        if self.has_key(id):
            self.map[id].append(effect)
        else:
            self.map[id] = [effect]


multiCache = MultiCache()
noNeedCache = True

class GroupSfx(object):

    def __init__(self, fxId, fxLv, position, rotateAngle = None, rotateAxis = None, scale = None):
        global multiCache
        self.model = sfx.getDummyModel()
        self.position = position
        self.attached = False
        self.id = fxId
        self.rotateAngle = rotateAngle
        self.rotateAxis = rotateAxis
        self.scale = scale
        self.fx = None
        self.cache = multiCache
        if self.cache.has_key(fxId) and not noNeedCache:
            self.fx = self.cache.pop(fxId)
            self.fx.drawLevel(fxLv)
        else:
            try:
                self.fx = clientUtils.pixieFetch(sfx.getPath(fxId), fxLv)
                self.fx.drawLevel(fxLv)
            except:
                gamelog.error('can not find effect:', fxId)

    def __del__(self):
        if self.attached:
            self.detach()
        self.model = None
        self.fx = None

    def detach(self):
        if self.attached:
            self.model.root.detach(self.fx)
            if noNeedCache:
                self.fx.clear()
                self.fx.stop()
                self.fx = None
            else:
                self.cache.push(self.id, self.fx)
            sfx.giveBackDummyModel(self.model)
            self.attached = False

    def attach(self):
        if self.attached or not self.fx:
            return
        self.model.yaw = 0
        self.model.position = self.position
        self.triggered = True
        self.model.root.attach(self.fx)
        if self.rotateAngle != None:
            gamelog.debug('bgf:sfx', self.rotateAngle, self.rotateAxis, self.position)
            self.model.rotate(self.rotateAngle, self.rotateAxis)
        if self.scale:
            self.fx.scale(*self.scale)
        self.fx.force()
        self.attached = True


class GroupSfxBatch(object):

    def __init__(self, effectId, effectLv, positions, maxDelayTime, delay = 0, onComplete = None):
        self.delay = delay
        self.fxId = effectId
        self.fxLv = effectLv
        self.rotateMode = 0
        self.randScale = False
        self.randRotate = False
        self.dropPoint = False
        self.positions = positions[:]
        self.particals = []
        if maxDelayTime == -1:
            self.duration = gameglobal.EFFECT_LAST_TIME
        else:
            self.duration = maxDelayTime
        self.onComplete = onComplete

    def removeAll(self):
        gamelog.debug('done:', BigWorld.time())
        self.__detachAll()
        self.particals = []
        if self.onComplete is not None:
            self.onComplete()

    def addRotate(self, mode, angle, angleAxis):
        self.rotateMode = mode
        self.rotateAngle = angle
        self.angleAxis = angleAxis

    def addRandScale(self, param):
        self.randScale = True
        self.scaleParam = param

    def addRandRotate(self, param):
        self.randRotate = True
        self.randRotateParam = param

    def addDropPoint(self, flag):
        self.dropPoint = flag

    def start(self):
        gamelog.debug('start:', self.delay + self.duration)
        if self.delay > 0.01:
            BigWorld.callback(self.delay, self.__attachAll)
        else:
            self.__attachAll()
        BigWorld.callback(self.delay + self.duration, self.removeAll)

    def __attachAll(self):
        if len(self.particals) == 0:
            l = len(self.positions)
            if self.dropPoint:
                for p in xrange(l):
                    pos = BigWorld.findDropPoint(BigWorld.player().spaceID, Math.Vector3(self.positions[p][0], self.positions[p][1] + 10, self.positions[p][2]))
                    if pos:
                        self.positions[p] = (pos[0][0], pos[0][1], pos[0][2])

            if self.rotateMode == 1:
                deltaAngle = math.pi * 2 / l
                angle = 0
                for i in xrange(l):
                    self.particals.append(GroupSfx(self.fxId, self.fxLv, self.positions[i], angle, self.angleAxis))
                    angle -= deltaAngle

            elif self.rotateMode == 2:
                for i in xrange(l):
                    self.particals.append(GroupSfx(self.fxId, self.fxLv, self.positions[i], self.rotateAngle, self.angleAxis))

            else:
                for i in xrange(l):
                    self.particals.append(GroupSfx(self.fxId, self.fxLv, self.positions[i]))

        for p in self.particals:
            if self.randScale:
                scaleX = random.uniform(1 - self.scaleParam, 1 + self.scaleParam)
                scaleY = random.uniform(1 - self.scaleParam, 1 + self.scaleParam)
                scaleZ = random.uniform(1 - self.scaleParam, 1 + self.scaleParam)
                p.scale = (scaleX, scaleY, scaleZ)
            if self.randRotate:
                rad = random.uniform(-self.randRotateParam, self.randRotateParam)
                if p.rotateAngle != None:
                    p.rotateAngle += rad
                else:
                    p.rotateAngle = rad

        for p in self.particals:
            p.attach()

    def __detachAll(self):
        for p in self.particals:
            p.detach()


class GroupSfxSys(object):

    def __init__(self, effectId, effectLv, generatorF, args, dnd, randomSeed = 0):
        assert len(args) == len(dnd)
        self.batches = []
        self.nBatchesDone = 0
        self.startTime = BigWorld.time()
        self.stoped = False
        self.generatorF = generatorF
        self.args = args[:]
        self.effectId = effectId
        self.effectLv = effectLv
        self.delays, self.durations = zip(*dnd)
        self.rotateMode = 0
        self.dropPoint = False
        self.multiEffect = False
        self.randRotate = False
        self.randScale = False
        if effectId.__class__.__name__ in ('list', 'tuple'):
            self.multiEffect = True

    def start(self, startFrom = 0):
        gamelog.debug('start:', BigWorld.time())
        self.stop()
        delay = self.delays[0]
        startIdx = 0
        if startFrom > 0:
            for i in xrange(len(self.delays)):
                if self.delays[i] > startFrom:
                    delay = self.delays[i] - startFrom
                    startIdx = i
                    break

        self.delays = self.delays[startIdx:]
        args = self.args[startIdx:]
        durations = self.durations[startIdx:]
        for i in xrange(len(args)):
            poses = self.generatorF(*args[i])
            if self.dropPoint:
                l = len(poses)
                for p in xrange(l):
                    pos = BigWorld.findDropPoint(BigWorld.player().spaceID, Math.Vector3(poses[p][0], poses[p][1] + 5, poses[p][2]))
                    if pos:
                        poses[p] = (pos[0][0], pos[0][1], pos[0][2])

            if self.multiEffect:
                self.batches.append(GroupSfxBatch(self.effectId[i], self.effectLv, poses, durations[i], 0))
            else:
                self.batches.append(GroupSfxBatch(self.effectId, self.effectLv, poses, durations[i], 0))
            gamelog.debug('bgf:effect', self.rotateMode)
            if self.rotateMode != 0:
                self.batches[i].addRotate(self.rotateMode, self.rotateAngle, self.angleAxis)
            if self.randScale:
                self.batches[i].addRandScale(self.scaleParam)
            if self.randRotate:
                self.batches[i].addRandRotate(self.randRotateParam)

        self.startTime = BigWorld.time()
        self.stoped = False
        if delay > 0:
            BigWorld.callback(delay, self.nextBatch)
        else:
            self.nextBatch()

    def addRotate(self, mode, angle, angleAxis):
        self.rotateMode = mode
        self.rotateAngle = angle
        self.angleAxis = angleAxis

    def addDropPoint(self, flag):
        self.dropPoint = flag

    def addRandScale(self, param):
        self.randScale = True
        self.scaleParam = param

    def addRandRotate(self, param):
        self.randRotate = True
        self.randRotateParam = param

    def stop(self):
        gamelog.debug('stop:', BigWorld.time())
        self.stoped = True
        for undonebatch in self.batches[self.nBatchesDone + 1:]:
            undonebatch.removeAll()

        self.batches = []

    def nextBatch(self):
        if self.stoped:
            return
        idxBatchToStart = self.nBatchesDone
        self.batches[idxBatchToStart].start()
        if idxBatchToStart < len(self.batches) - 1:
            BigWorld.callback(self.delays[idxBatchToStart + 1] - self.delays[idxBatchToStart], self.nextBatch)
        self.nBatchesDone += 1

    def resume(self):
        pass


class PosGenerator(object):

    def __init__(self):
        pass

    @staticmethod
    def randomCircle(center, radius, n):
        res = []
        for i in xrange(n):
            r = random.random() * radius
            t = random.random() * 6.28318530717958
            x = center[0] + r * math.cos(t)
            y = center[1]
            z = center[2] + r * math.sin(t)
            res.append((x, y, z))

        return res

    @staticmethod
    def randomRectangle(center, length, width, n, yaw):
        res = []
        for i in xrange(n):
            x = length / 2 - random.random() * length
            z = width / 2 - random.random() * width
            x1 = x * math.cos(yaw) - z * math.sin(yaw)
            z1 = x * math.sin(yaw) + z * math.cos(yaw)
            res.append((center[0] + x1, center[1], center[2] + z1))

        return res

    @staticmethod
    def randomFan(center, radius, theta, n, yaw):
        res = []
        for i in xrange(n):
            r = random.random() * radius
            t = random.random() * theta - theta / 2 + yaw
            x = center[0] + r * math.cos(t)
            y = center[1]
            z = center[2] + r * math.sin(t)
            res.append((x, y, z))

        return res

    @staticmethod
    def line(startpos, length, n, direction):
        if n == 1:
            return [startpos]
        res = []
        dirlen = math.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
        n -= 1
        diff = (direction[0] * length / dirlen / n, direction[1] * length / dirlen / n, direction[2] * length / dirlen / n)
        n += 1
        pos = startpos
        for i in xrange(n):
            res.append(pos)
            pos = (pos[0] + diff[0], pos[1] + diff[1], pos[2] + diff[2])

        return res

    @staticmethod
    def randomLine(startpos, length, n, direction):
        res = []
        dirlen = math.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
        target = (startpos[0] + direction[0] * length / dirlen, startpos[1] + direction[1] * length / dirlen, startpos[2] + direction[2] * length / dirlen)
        for i in xrange(n):
            r = random.random()
            res.append((startpos[0] + r * (target[0] - startpos[0]), startpos[1] + r * (target[1] - startpos[1]), startpos[2] + r * (target[2] - startpos[2])))

        return res

    @staticmethod
    def randomSphere(center, radius, n):
        res = []
        for i in xrange(n):
            a = random.random() * 6.28318530717958
            b = random.random() * 6.28318530717958
            r = random.random() * radius
            x = center[0] + r * math.cos(a) * math.sin(b)
            y = center[1] + r * math.sin(a) * math.sin(b)
            z = center[2] + r * math.cos(b)
            res.append((x, y, z))

        return res

    @staticmethod
    def randomCyliner(center, radius, height, n, direction):
        res = []
        for i in xrange(n):
            a = random.random() * 6.28318530717958
            b = random.random() * height
            r = random.random() * radius
            res.append((center[0] + math.cos(a) * r, center[1] + height / 2 - b, center[2] + math.sin(a) * r))

        return res

    @staticmethod
    def randomBox(center, length, width, height, n, yaw):
        res = []
        for i in xrange(n):
            x = length / 2 - random.random() * length
            y = height / 2 - random.random() * height
            z = width / 2 - random.random() * width
            x1 = x * math.cos(yaw) - z * math.sin(yaw)
            z1 = x * math.sin(yaw) + z * math.cos(yaw)
            res.append((center[0] + x1, center[1] + y, center[2] + z1))

        return res

    @staticmethod
    def randomFanBox(center, radius, theta, height, n, yaw):
        res = []
        for i in xrange(n):
            r = random.random() * radius
            t = random.random() * theta - theta / 2 + yaw
            x = center[0] + r * math.cos(t)
            y = center[1] + height / 2 - random.random() * height
            z = center[2] + r * math.sin(t)
            res.append((x, y, z))

        return res

    @staticmethod
    def rangeInCircum(center, radius, delta, isAngle = False, angle = 0):
        gamelog.debug('bgf:effect', center, radius, delta, isAngle, angle)
        res = []
        i = 0.0
        if isAngle:
            deltaAngle = delta
        else:
            deltaAngle = float(delta / radius)
        while i < 2 * math.pi:
            x = radius * math.cos(i + angle) + center[0]
            y = center[1]
            z = radius * math.sin(i + angle) + center[2]
            i += deltaAngle
            res.append((x, y, z))

        return res


pb = None

def playEffect(effectId, effectLv, positions, duration, delay):
    global pb
    pb = GroupSfxBatch(effectId, effectLv, positions, duration, delay)
    pb.start()


fxId = 120761
fxLv = 1

def playCircle(effEctId, effectLv, targetPos, radius, fxNumber, maxDelayTime):
    pos = PosGenerator.randomCircle(targetPos, radius, fxNumber)
    playEffect(effEctId, effectLv, pos, maxDelayTime, 0)


def playCircum(effectId, effectLv, targetPos, step, numStep, delayTime, duration, delta, angle = 0):
    arg = []
    dnd = []
    for i in xrange(1, numStep + 1):
        arg.append((targetPos, step * i, delta))
        dnd.append((delayTime * (i - 1), duration))

    gss = GroupSfxSys(effectId, effectLv, PosGenerator.rangeInCircum, arg, dnd)
    gss.addRotate(1, None, Math.Vector3(0, 1, 0))
    gss.addDropPoint(True)
    gss.start()


def playLinear(effectId, effectLv, targetPos, yaw, length, numStep, delayTime, duration, delayStart = 0, needRandRotate = True):
    dir = (math.sin(yaw), 0, math.cos(yaw))
    tPos = Math.Vector3(targetPos)
    tPos[0] += dir[0] * 3.0
    tPos[2] += dir[2] * 3.0
    pointArray = PosGenerator.line(tPos, length, numStep, dir)
    gamelog.debug('bgf:sfx', yaw, pointArray)
    arg = []
    dnd = []
    for i in xrange(numStep):
        arg.append((pointArray[i],
         None,
         1,
         None))
        dnd.append((delayTime * (i + 1), duration))

    gss = GroupSfxSys(effectId, effectLv, PosGenerator.line, arg, dnd)
    gss.addDropPoint(True)
    gss.addRotate(2, yaw, Math.Vector3(0, 1, 0))
    if needRandRotate:
        gss.addRandRotate(math.pi)
    BigWorld.callback(delayStart, gss.start)


def playCircleEx(effectId, effectLv, targetPos, yaw, radius, num, numStep, delayTime, duration):
    arg = []
    dnd = []
    for i in xrange(numStep):
        arg.append((targetPos, radius, num))
        dnd.append((delayTime * (i + 1), duration))

    gss = GroupSfxSys(effectId, effectLv, PosGenerator.randomCircle, arg, dnd)
    gss.addRotate(2, yaw, Math.Vector3(0, 1, 0))
    gss.addDropPoint(True)
    gss.start()


def playMultiEffectInCircum(effectId, effectLv, targetPos, step, numStep, delayTime, duration, delta, isAngle, angle = 0):
    arg = []
    dnd = []
    for i in xrange(1, numStep + 1):
        arg.append((targetPos,
         0.7 + step * (i - 1),
         delta,
         isAngle,
         (i - 1) * angle))
        dnd.append((delayTime * (i - 1), duration))

    gss = GroupSfxSys(effectId, effectLv, PosGenerator.rangeInCircum, arg, dnd)
    gss.addRotate(1, None, Math.Vector3(0, 1, 0))
    gss.addDropPoint(True)
    gss.start()


def playFan():
    p = BigWorld.player()
    n = 50
    playEffect(fxId, fxLv, PosGenerator.randomFan(p.position, 5, 3.14159 / 4, n, p.yaw), 5, 0)


def playRectangle():
    p = BigWorld.player()
    n = 50
    playEffect(fxId, fxLv, PosGenerator.randomRectangle(p.position, 10, 10, n, p.yaw), 3, 0)


def playLine(effectId, effectLv, targetPos, yaw, length, numStep, delayTime, duration, delayStart = 0):
    global pb
    dir = (math.sin(yaw), 0, math.cos(yaw))
    tPos = Math.Vector3(targetPos)
    tPos[0] += dir[0] * 3.0
    tPos[2] += dir[2] * 3.0
    pointArray = PosGenerator.line(tPos, length, numStep, dir)
    pb = GroupSfxBatch(effectId, effectLv, pointArray, duration, delayStart)
    pb.addRotate(2, yaw, Math.Vector3(0, 1, 0))
    pb.addRandRotate(math.pi)
    pb.addDropPoint(True)
    pb.start()


def playRandomLine():
    p = BigWorld.player()
    n = 30
    playEffect(fxId, fxLv, PosGenerator.randomLine(p.position, 10, n, (0, 0, 1)), 3, 0)


def playSphere():
    p = BigWorld.player()
    n = 100
    playEffect(fxId, fxLv, PosGenerator.randomSphere(p.position + (0, 5, 0), 4, n), 5, 0)


def playBox():
    p = BigWorld.player()
    n = 100
    playEffect(fxId, fxLv, PosGenerator.randomBox(p.position + (0, 5, 0), 6, 6, 6, n, p.yaw), 3, 0)


def playCylinder():
    p = BigWorld.player()
    n = 100
    playEffect(fxId, fxLv, PosGenerator.randomCyliner(p.position + (0, 5, 0), 3, 5, n, None), 5, 0)


def playFanBox():
    p = BigWorld.player()
    n = 100
    playEffect(fxId, fxLv, PosGenerator.randomFanBox(p.position + (0, 5, 0), 3, 1.6, 5, n, 0), 5, 0)
