#Embedded file name: I:/bag/tmp/tw2/res/entities\common/runeCommon.o
import const
from userSoleType import UserSoleType
from data import rune_effect_data as REFD
from const import RUNE_TYPE_TIANLUN, RUNE_TYPE_DILUN, RUNE_TYPE_BENYUAN, RUNE_EFFECT_TYPE_NUM

class RuneCommon(UserSoleType):

    def __init__(self):
        self.runeEquip = None
        self.runeEffectsDict = {}
        self.awakeDict = {}
        for runeType in const.ALL_RUNE_TYPE:
            self.awakeDict[runeType] = False
            self.runeEffectsDict[runeType] = [0] * const.RUNE_EFFECT_TYPE_NUM

        self.allRuneEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        self.pskillSet = {}

    def isEmptyRuneEquip(self):
        return self.runeEquip == None

    def getRuneEquip(self):
        return self.runeEquip

    def checkRuneEffectNeed(self, effectsData, effectsNeed):
        for i in range(RUNE_EFFECT_TYPE_NUM):
            if effectsData[i] < effectsNeed[i]:
                return False

        return True

    def getRuneEffects(self, runeSlotsType):
        return self.runeEffectsDict[runeSlotsType]

    def isAwake(self, runeSlotsType):
        return self.awakeDict[runeSlotsType]

    def calcAllRuneEffects(self):
        allRuneEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        for i in range(const.RUNE_EFFECT_TYPE_NUM):
            allRuneEffects[i] = self.runeEffectsDict[RUNE_TYPE_TIANLUN][i] + self.runeEffectsDict[RUNE_TYPE_DILUN][i]
            if self.isAwake(RUNE_TYPE_BENYUAN):
                allRuneEffects[i] += self.runeEffectsDict[RUNE_TYPE_BENYUAN][i]

        self.allRuneEffects = allRuneEffects

    def calcShenLiJiFaPSkill(self):
        self.pskillSet.clear()
        self.calcAllRuneEffects()
        for eId, pData in REFD.data.iteritems():
            length = len(pData)
            for idx in range(length - 1, -1, -1):
                effectsNeed = pData[idx].get('runeEffectsNeed', [])
                if not effectsNeed:
                    continue
                if self.checkRuneEffectNeed(self.allRuneEffects, effectsNeed):
                    pskId, pskLv = pData[idx].get('pskillId'), pData[idx].get('lv', 1)
                    if pskId:
                        self.pskillSet[eId] = (pskId, pskLv)
                        break

    def resetAll(self):
        self.runeEquip = None
        self.resetAllData()

    def resetAllData(self):
        self.runeEffectsDict = {}
        self.awakeDict = {}
        for runeType in const.ALL_RUNE_TYPE:
            self.awakeDict[runeType] = False
            self.runeEffectsDict[runeType] = [0] * const.RUNE_EFFECT_TYPE_NUM

        self.allRuneEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        self.pskillSet.clear()
