#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerAbility.o
import gameglobal
import utils
import cPickle
import zlib
from data import social_lv_data as SLD
from data import life_skill_data as LSD

class ImpPlayerAbility(object):

    def enableAbilityNode(self, anNo, star):
        gameglobal.rds.ui.lifeSkillNew.setTreeNodeData(anNo, self.abilityTree[anNo])
        gameglobal.rds.ui.lifeSkillNew.showTreeNodeEffect(anNo)
        gameglobal.rds.ui.lifeSkillNew.refreshAllData()

    def syncAbilityIds(self, abilityIds):
        self.abilityIds = cPickle.loads(zlib.decompress(abilityIds))

    def getAbilityData(self, key1, key2 = None, default = 0):
        if not self.hasAbilityData(key1, key2):
            return default
        key = utils.getAbilityKey(key1, key2)
        return self.abilityData[key]

    def set_abilityTree(self, old):
        justAdd = True
        for anNo in old:
            if not self.abilityTree.get(anNo) or len(old.get(anNo, [])) > len(self.abilityTree.get(anNo, [])):
                justAdd = False
                break

        if justAdd == False:
            gameglobal.rds.ui.lifeSkillNew.refreshPanel(0, True)

    def hasAbilityData(self, key1, key2 = None):
        key = utils.getAbilityKey(key1, key2)
        if not self.abilityData.has_key(key):
            return False
        else:
            return True

    def getCurXueShiVal(self):
        res = 0
        res += SLD.data.get(self.socLv, {}).get('xueShiVal', 0)
        for skId, sVal in self.lifeSkill.items():
            res += LSD.data.get((skId, sVal['level']), {}).get('xueShiVal', 0)

        return res - self.usedXueShi

    def getCurYueLiVal(self, socLv = None):
        if socLv:
            calcSocLv = socLv
        else:
            calcSocLv = self.socLv
        res = 0
        res += SLD.data.get(calcSocLv, {}).get('yueLiVal', 0)
        for skId, sVal in self.lifeSkill.items():
            res += LSD.data.get((skId, sVal['level']), {}).get('yueLiVal', 0)

        return res
