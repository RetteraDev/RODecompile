#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/auraFx.o
import BigWorld
import gamelog
import gameglobal
import utils
import sfx
from data import skill_auras_data as SAD

class EffectMgr(object):

    def __init__(self, ownerId):
        self.ownerId = ownerId
        self.fxMap = {}
        self.startFxMap = {}
        self.effEndTimeDict = {}

    def release(self):
        owner = BigWorld.entity(self.ownerId)
        if owner and owner.inWorld:
            attachModel = owner.model
            for fxId in self.fxMap.keys():
                sfx.detachEffect(attachModel, fxId, self.fxMap[fxId])

        self.fxMap = {}
        self.startFxMap = {}
        self.effEndTimeDict = {}
        self.ownerId = 0

    def _getAuraDuration(self, auraId):
        auraData = SAD.data.get(auraId, None)
        if not auraData:
            gamelog.error('@fj auraId invalid %d', auraId)
            return 0
        duration = auraData.get('duration', 10)
        return duration

    def _realAddAuraFx(self, attachModel, hostId, auraId, effId, lastTime, effectLv, priority):
        if attachModel:
            attachModel.hostId = hostId
        ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
         priority,
         attachModel,
         effId,
         sfx.EFFECT_LIMIT,
         lastTime))
        if ef != None:
            self.fxMap[effId] = ef
            if not self.effEndTimeDict.has_key(effId):
                self.effEndTimeDict[effId] = {}
            self.effEndTimeDict[effId].update({auraId: utils.getNow() + self._getAuraDuration(auraId)})

    def getEffectEndTime(self, effectId):
        endTime = 0
        if self.effEndTimeDict.has_key(effectId):
            for key, value in self.effEndTimeDict[effectId].iteritems():
                if value > endTime:
                    endTime = value

        return endTime

    def addAura(self, auraId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        auraData = SAD.data.get(auraId, None)
        if not auraData:
            gamelog.error('@fj auraId invalid %d', auraId)
            return
        startFxList = auraData.get('startFx', [])
        fxList = auraData.get('fx', [])
        duration = auraData.get('duration', 10)
        attachModel = owner.model
        if attachModel:
            attachModel.hostId = self.ownerId
        now = utils.getNow()
        for i in fxList:
            if self.fxMap.has_key(i):
                if now + duration > self.getEffectEndTime(i):
                    sfx.detachEffect(attachModel, i, self.fxMap[i])
                    self.fxMap.pop(i)
                    self._realAddAuraFx(attachModel, self.ownerId, auraId, i, duration, gameglobal.EFFECT_MID, gameglobal.EFF_PLAYER_AURA_PRIORITY)
                else:
                    if not self.effEndTimeDict.has_key(i):
                        self.effEndTimeDict[i] = {}
                    self.effEndTimeDict[i].update({auraId: now + self._getAuraDuration(auraId)})
            else:
                self._realAddAuraFx(attachModel, self.ownerId, auraId, i, duration, gameglobal.EFFECT_MID, gameglobal.EFF_PLAYER_AURA_PRIORITY)

        for i in startFxList:
            if self.startFxMap.has_key(i):
                sfx.detachEffect(attachModel, i, self.startFxMap[i])
            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_MID,
             gameglobal.EFF_PLAYER_AURA_PRIORITY,
             attachModel,
             i,
             sfx.EFFECT_UNLIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if ef:
                self.startFxMap[i] = ef

    def removeAura(self, auraId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        auraData = SAD.data.get(auraId, None)
        if auraData == None:
            gamelog.error('@fj auraId invalid %d', auraId)
            return
        attachModel = owner.model
        now = utils.getNow()
        fxList = auraData.get('fx', [])
        for i in fxList:
            if self.fxMap.has_key(i):
                if self.effEndTimeDict.has_key(i) and auraId in self.effEndTimeDict[i].keys():
                    endTimePre = self.getEffectEndTime(i)
                    self.effEndTimeDict[i].pop(auraId)
                    endTimePost = self.getEffectEndTime(i)
                    if endTimePost < endTimePre:
                        sfx.detachEffect(attachModel, i, self.fxMap[i])
                        self.fxMap.pop(i)
                        if endTimePost > now:
                            self._realAddAuraFx(attachModel, self.ownerId, auraId, i, endTimePost - now, gameglobal.EFFECT_MID, gameglobal.EFF_PLAYER_AURA_PRIORITY)

        startFxList = auraData.get('startFx', [])
        for i in startFxList:
            if self.startFxMap.has_key(i):
                self.startFxMap.pop(i)

        self._addDelFx(auraData)

    def _addDelFx(self, auraData):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        attachModel = owner.model
        hostId = self.ownerId
        if attachModel:
            attachModel.hostId = hostId
        for i in auraData.get('delFx', []):
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_MID,
             gameglobal.EFF_PLAYER_AURA_PRIORITY,
             attachModel,
             i,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
