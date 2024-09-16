#Embedded file name: I:/bag/tmp/tw2/res/entities\common/summonSpriteBiographyInfo.o
from userInfo import UserInfo
from summonSpriteBiography import SummonSpriteBiographyTarget, SummonSpriteBiographyTargets, SummonSpriteBiography, SummonSpriteBiographies

class SummonSpriteBiographyTargetsInfo(UserInfo):
    FIELD_TARGET_ID = 1
    FIELD_DONE = 2
    FIELD_DATE = 3

    def createObjFromDict(self, dict):
        bioTargets = SummonSpriteBiographyTargets()
        if dict and dict.has_key('summonSpriteBiographyTargets') and dict['summonSpriteBiographyTargets']:
            for achTargetVal in dict['summonSpriteBiographyTargets']:
                bioTarget = SummonSpriteBiographyTarget(achTargetVal[self.FIELD_TARGET_ID])
                bioTarget.done = True if achTargetVal[self.FIELD_DONE] > 0 else False
                bioTarget.date = achTargetVal[self.FIELD_DATE]
                bioTargets[bioTarget.achieveTargetId] = bioTarget

        return bioTargets

    def getDictFromObj(self, obj):
        aVals = []
        for bioTarget in obj.itervalues():
            aVals.append({self.FIELD_TARGET_ID: bioTarget.achieveTargetId,
             self.FIELD_DONE: 1 if bioTarget.done else 0,
             self.FIELD_DATE: bioTarget.date})

        return {'summonSpriteBiographyTargets': aVals}

    def isSameType(self, obj):
        return type(obj) is SummonSpriteBiographyTargets


summonSpriteTargetsInstance = SummonSpriteBiographyTargetsInfo()

class SummonSpriteBiographiesInfo(UserInfo):
    FIELD_SPRITE_ID = 1
    FIELD_BIO_ID = 2
    FIELD_ACHIEVE_ID = 3
    FIELD_ISFINISH = 4
    FIELD_FINISH_DATE = 5
    FIELD_ISUNLOCK = 6
    FIELD_UNLOCK_DATE = 7

    def createObjFromDict(self, dict):
        summonSpriteBio = SummonSpriteBiographies()
        if dict and dict.has_key('summonSpriteBiographies') and dict['summonSpriteBiographies']:
            for biographyVal in dict['summonSpriteBiographies']:
                spriteId = biographyVal[self.FIELD_SPRITE_ID]
                bioId = biographyVal[self.FIELD_BIO_ID]
                bio = SummonSpriteBiography(biographyVal[self.FIELD_ACHIEVE_ID])
                bio.isDone = biographyVal[self.FIELD_ISFINISH]
                bio.doneDate = biographyVal[self.FIELD_FINISH_DATE]
                bio.isUnlock = biographyVal[self.FIELD_ISUNLOCK]
                bio.unlockDate = biographyVal[self.FIELD_UNLOCK_DATE]
                if not summonSpriteBio.has_key(spriteId):
                    summonSpriteBio[spriteId] = {}
                summonSpriteBio[spriteId][bioId] = bio

        return summonSpriteBio

    def getDictFromObj(self, obj):
        aVals = []
        for spriteId, data in obj.iteritems():
            for bioId, biography in data.iteritems():
                aVals.append({self.FIELD_SPRITE_ID: spriteId,
                 self.FIELD_BIO_ID: bioId,
                 self.FIELD_ACHIEVE_ID: biography.achieveId,
                 self.FIELD_ISFINISH: biography.isDone,
                 self.FIELD_FINISH_DATE: biography.doneDate,
                 self.FIELD_ISUNLOCK: biography.isUnlock,
                 self.FIELD_UNLOCK_DATE: biography.unlockDate})

        return {'summonSpriteBiographies': aVals}

    def isSameType(self, obj):
        return type(obj) is SummonSpriteBiographies


summonSpriteBiographiesInstance = SummonSpriteBiographiesInfo()
