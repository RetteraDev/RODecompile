#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFaceEmote.o
import BigWorld
import gameglobal
import clientcom
import const
from helpers import tintalt as TA
from sfx import sfx
from helpers import charRes
from helpers import vertexMorpher
from callbackHelper import Functor
from data import emote_data as ED

class ImpFaceEmote(object):
    FaceEmotePrefix = 'char/%d/config/emotion/%s.xml'

    def setFaceEmoteId(self):
        if self.curFaceEmoteId:
            self.startFaceEmoteById(self.curFaceEmoteId)
        else:
            self.endFaceEmote()

    def startFaceEmoteById(self, emoteId):
        xmlName = ED.data.get(emoteId, {}).get('res', None)
        if not xmlName:
            return
        else:
            modelId = charRes.transDummyBodyType(self.realPhysique.sex, self.realPhysique.bodyType, True)
            xmlPath = self.FaceEmotePrefix % (modelId, xmlName)
            clientcom.Cache.fetchConfig(xmlPath, Functor(self.startFaceEmote, xmlName))
            return

    def realStartFaceEmote(self, xmlName, model, realPhysique):
        if not gameglobal.rds.configData.get('enableFaceEmote', False):
            return {}
        if not model or not model.inWorld:
            return {}
        modelId = charRes.transDummyBodyType(realPhysique.sex, realPhysique.bodyType, True)
        resModelId = charRes.transBodyType(realPhysique.sex, realPhysique.bodyType)
        xmlName = self.FaceEmotePrefix % (modelId, xmlName)
        xml = clientcom.Cache.getConfig(xmlName)
        if not xml:
            return {}
        faceTexName = xml.readString('faceTex', '')
        eyeTexName = xml.readString('eyeTex', '')
        eyeRotate = xml.readFloat('eyeRotate', 0)
        actionName = xml.readString('action', '')
        morphName = xml.readString('morph', '')
        sfxSection = xml.openSections('effect')
        idleSfxSection = xml.openSections('idleEffect')
        idleSfxProb = xml.readInt('idleEffectProb', 0)
        blockInfo = {}
        for key in const.FACE_EMOTE_BLOCK_KEYS:
            value = xml.readInt(key, 0)
            if value:
                blockInfo[key] = value

        self.setFaceBoneAndMorph(model, blockInfo, 1)
        sfxList = []
        if sfxSection:
            sfxList = [ sec.asInt for sec in sfxSection ]
        idleSfxList = []
        if idleSfxSection:
            idleSfxList = [ sec.asInt for sec in idleSfxSection ]
        if actionName:
            try:
                action = model.action(actionName)
                action.enableAlpha(True)
                action()
            except:
                pass

        if morphName:
            model.setMorph(1, morphName, 1)
            model.applyMorph(1)
        emotionFxs = []
        for effectId in sfxList:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getBasicEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_UNLIMIT))
            if fx:
                emotionFxs.extend(fx)

        emotionIdleFxs = []
        for effectId in idleSfxList:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getBasicEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_UNLIMIT))
            if fx:
                emotionIdleFxs.extend(fx)

        if faceTexName:
            TA.ta_add([model], 'emotionHead%s' % realPhysique.sex, ['char/%d/%s' % (resModelId, faceTexName)], 0, 'head', False, True, tintType=TA.AVATARTINT)
        faceEmoteXmlInfo = {}
        if eyeTexName:
            self.eyeTintToEmotion(model, 'char/%d/%s' % (resModelId, eyeTexName), eyeRotate, faceEmoteXmlInfo)
        if faceTexName or eyeTexName:
            TA.ta_apply([model])
        if hasattr(model, 'enableAlphaAll'):
            model.enableAlphaAll(True)
        faceEmoteXmlInfo['faceEmotionAction'] = actionName
        faceEmoteXmlInfo['faceEmotionFxs'] = emotionFxs
        faceEmoteXmlInfo['faceEmotionMorph'] = morphName
        faceEmoteXmlInfo['faceTexName'] = faceTexName
        faceEmoteXmlInfo['eyeTexName'] = eyeTexName
        faceEmoteXmlInfo['faceIdleFxs'] = emotionIdleFxs
        faceEmoteXmlInfo['faceIdleFxIds'] = idleSfxList
        faceEmoteXmlInfo['faceIdleFxProb'] = idleSfxProb
        faceEmoteXmlInfo['faceBlockInfo'] = blockInfo
        return faceEmoteXmlInfo

    def setFaceBoneAndMorph(self, model, blockInfo, value = 1):
        boneSuspends = []
        morphDisables = []
        for key in blockInfo.iterkeys():
            info = const.FACE_EMOTE_BLOCK.get(key, {})
            boneSuspends.extend(info.get('bone', []))
            morphDisables.extend(info.get('morph', []))

        if morphDisables:
            morpher = vertexMorpher.AvatarFaceMorpher(None, None)
            morpher.createConfig(self.realAvatarConfig)
            needApply = False
            for morphName in morphDisables:
                if morpher.hasMorph(morphName):
                    needApply = True
                    if value:
                        model.setMorph(1, morphName, 0)
                    else:
                        model.setMorph(1, morphName, morpher.transformMap[morphName])

            if needApply:
                model.applyMorph(1)

    def realEndFaceEmote(self, model, realPhysique, faceEmoteXmlInfo):
        if not model or not model.inWorld:
            return
        else:
            faceEmotionAction = faceEmoteXmlInfo.get('faceEmotionAction', None)
            if faceEmotionAction:
                try:
                    model.action(faceEmotionAction).stop()
                except:
                    pass

            faceEmotionFxs = faceEmoteXmlInfo.get('faceEmotionFxs', [])
            if faceEmotionFxs:
                for fx in faceEmotionFxs:
                    fx.stop()

            faceIdleFxs = faceEmoteXmlInfo.get('faceIdleFxs', [])
            if faceIdleFxs:
                for fx in faceIdleFxs:
                    fx.stop()

            faceEmotionMorph = faceEmoteXmlInfo.get('faceEmotionMorph', None)
            if faceEmotionMorph:
                model.setMorph(1, faceEmotionMorph, 0)
                model.applyMorph(1)
            faceTexName = faceEmoteXmlInfo.get('faceTexName', None)
            if faceTexName:
                TA.ta_del([model], 'emotionHead%s' % realPhysique.sex, 'head', False, True)
            eyeTexName = faceEmoteXmlInfo.get('eyeTexName', None)
            if eyeTexName:
                self.eyeTintBackAvatar(model, faceEmoteXmlInfo)
            if faceTexName or eyeTexName:
                TA.ta_apply([model])
            BigWorld.callback(0.1, Functor(self.setEnableAlphaAll, model, False))
            blockInfo = faceEmoteXmlInfo.get('faceBlockInfo', {})
            if blockInfo:
                self.setFaceBoneAndMorph(model, blockInfo, 0)
            return

    def setEnableAlphaAll(self, model, value):
        if model and model.inWorld and hasattr(model, 'enableAlphaAll'):
            model.enableAlphaAll(value)

    def startFaceEmote(self, xmlName, xmlData = None):
        if not gameglobal.rds.configData.get('enableFaceEmote', False):
            return
        if not self.inWorld or not self.isRealModel:
            return
        if self.faceEmoteXmlInfo:
            self.endFaceEmote()
        model = self.modelServer.bodyModel
        self.faceEmoteXmlInfo = self.realStartFaceEmote(xmlName, model, self.realPhysique)

    def endFaceEmote(self):
        if not self.inWorld or not self.isRealModel:
            return
        model = self.modelServer.bodyModel
        if self.faceEmoteXmlInfo:
            self.realEndFaceEmote(model, self.realPhysique, self.faceEmoteXmlInfo)
            self.faceEmoteXmlInfo = {}

    def isInFaceEmotionState(self):
        return self.curFaceEmoteId != 0

    def eyeTintToEmotion(self, model, eyeTexName, eyeRotate, faceEmoteXmlInfo):
        serialId = model.serialId
        params = TA._MODEL_STATE_MAP.get(serialId, {}).get('eye', {}).get('tas', {}).get('avatarEye', None)
        if params:
            faceEmoteXmlInfo['oldFaceEmoteEyeTex'] = params[0]
            TA.ta_del([model], 'avatarEye', 'eye', applyLater=True)
            params[0] = eyeTexName
            params.append(eyeRotate)
            TA.ta_add([model], 'emotionEye', params, 0, 'eye', applyLater=True, tintType=TA.AVATARTINT)

    def eyeTintBackAvatar(self, model, faceEmoteXmlInfo):
        serialId = model.serialId
        params = TA._MODEL_STATE_MAP.get(serialId, {}).get('eye', {}).get('tas', {}).get('emotionEye', None)
        if params:
            TA.ta_del([model], 'emotionEye', 'eye', applyLater=True)
            oldFaceEmoteEyeTex = faceEmoteXmlInfo.get('oldFaceEmoteEyeTex', '')
            if oldFaceEmoteEyeTex:
                params[0] = oldFaceEmoteEyeTex
                params.pop()
                TA.ta_add([model], 'avatarEye', params, 0, 'eye', applyLater=True, tintType=TA.AVATARTINT)

    def getFaceIdleFxIds(self):
        return self.faceEmoteXmlInfo.get('faceIdleFxIds', [])

    def getFaceIdleFxProb(self):
        return self.faceEmoteXmlInfo.get('faceIdleFxProb', 0)

    def playFaceIdleFxs(self):
        idleSfxList = self.faceEmoteXmlInfo.get('faceIdleFxIds', [])
        if not idleSfxList:
            return
        faceIdleFxs = self.faceEmoteXmlInfo.get('faceIdleFxs', [])
        if faceIdleFxs:
            for fx in faceIdleFxs:
                fx.stop()

        model = self.modelServer.bodyModel
        emotionIdleFxs = []
        for effectId in idleSfxList:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getBasicEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_UNLIMIT))
            if fx:
                emotionIdleFxs.extend(fx)

        self.faceEmoteXmlInfo['faceIdleFxs'] = emotionIdleFxs

    def faceEmoteTimeOut(self):
        if not self.inWorld:
            return
        self.setFaceEmoteId()
