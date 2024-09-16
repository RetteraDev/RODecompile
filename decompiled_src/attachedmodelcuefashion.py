#Embedded file name: /WORKSPACE/data/entities/client/helpers/attachedmodelcuefashion.o
import inspect
import BigWorld
import const
import gameglobal
from callbackHelper import Functor
from sfx import sfx

class AttachedModelCueFashion(object):

    def _playSound(self, data):
        entity = BigWorld.entity(self.entityID)
        params = data.split(':')
        try:
            onlyPlayer = int(params[1])
        except:
            onlyPlayer = False

        soundPath = str(params[0])
        if onlyPlayer and not entity.fashion.isPlayer:
            return
        gameglobal.rds.sound.playFx(soundPath, entity.position, False, entity)
        if gameglobal.g_Print_SoundPath:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, soundPath, '')

    def _playEffect(self, data):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        params = data[1:].split(':')
        effects = params[0][1:-1].split(',')
        delayTime = 0.0
        if len(params) > 1:
            delayTime = float(params[1])
        onlyPlayer = bool(float(params[2])) if len(params) > 2 else False
        if onlyPlayer and entity != BigWorld.player():
            return
        for e in effects:
            tt = e.split('.xml-')
            if len(tt) == 2:
                effect = tt[0].split('/')
                if effect[len(effect) - 1].isdigit():
                    if getattr(entity, 'inCombat', 0):
                        effectLv = entity.getSkillEffectLv()
                        priority = entity.getSkillEffectPriority()
                    else:
                        effectLv = entity.getBasicEffectLv()
                        priority = entity.getBasicEffectPriority()
                    effId = int(effect[len(effect) - 1])
                    duration = float(tt[1]) / gameglobal.ACTION_FRAME
                    BigWorld.callback(delayTime, Functor(self._attachFx, effId, effectLv, priority, duration))

    def _attachFx(self, effId, effectLv, priority, duration):
        if not hasattr(self, 'cueFxDict'):
            self.cueFxDict = {}
        oldFxs = self.cueFxDict.get(effId, [])
        if oldFxs:
            for fx in oldFxs:
                fx.stop()

        newFxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
         priority,
         self.model,
         effId,
         sfx.EFFECT_LIMIT,
         duration))
        if newFxs:
            self.cueFxDict[effId] = newFxs

    def actionCueCallback(self, cueId, data, actionName):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        p = BigWorld.player()
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_END and (entity.position - p.position).lengthSquared > gameglobal.MAX_DISTANCE_ACTION_CUE * gameglobal.MAX_DISTANCE_ACTION_CUE:
            return
        if entity.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        if cueId == 1:
            self._playSound(data)
        elif cueId == 2 and data.startswith('s'):
            self._playEffect(data)

    def doAction(self, act):
        for item in self.models:
            model = item[0]
            try:
                model.action(act)()
            except:
                pass

    def stopAction(self):
        for item in self.models:
            modelItem = item[0]
            if not hasattr(modelItem, 'queue'):
                return
            actQueue = modelItem.queue
            if len(actQueue) == 0:
                return
            for i in actQueue:
                aq = modelItem.action(i)
                aq.stop()

    def doActions(self, acts):
        for item in self.models:
            model = item[0]
            try:
                l = len(acts)
                act = model.action(acts[0])
                for i in xrange(1, l):
                    act = getattr(act(0, None, 0), acts[i])

                act(0, None, 0)
            except:
                pass


class AttachedModelCueFashionMeta(type):

    def __init__(cls, name, bases, dic):
        super(AttachedModelCueFashionMeta, cls).__init__(name, bases, dic)
        inherits = (AttachedModelCueFashion,)
        for inherit in inherits:
            AttachedModelCueFashionMeta._moduleMixin(cls, name, inherit)

    def _moduleMixin(cls, name, module):
        for name, fun in inspect.getmembers(module, inspect.ismethod):
            setattr(cls, name, fun.im_func)

        for name, memb in inspect.getmembers(module):
            if name == '__module__':
                continue
            if memb.__class__.__name__ in const.BUILTIN_OBJS:
                setattr(cls, name, memb)


class HairNodeModelCue(object):
    __metaclass__ = AttachedModelCueFashionMeta

    def __init__(self, entityID):
        self.model = None
        self.entityID = entityID

    def setModel(self, model):
        self.model = model

    def release(self):
        self.model = None
        self.entityID = None

    @property
    def models(self):
        return ((self.model,),)
