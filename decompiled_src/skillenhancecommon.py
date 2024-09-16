#Embedded file name: /WORKSPACE/data/entities/common/skillenhancecommon.o
import BigWorld
import formula
import const
import utils
import gamelog
from userSoleType import UserSoleType
from data import skill_enhance_data as SED
from cdata import game_msg_def_data as GMDD

class CSkillEnhanceVal(UserSoleType):

    def __init__(self, state = const.SKILL_ENHANCE_STATE_UNUSABLE, enhancePoint = 0, enhanceTime = 0):
        self.state = state
        self.enhancePoint = enhancePoint
        self.enhanceTime = enhanceTime

    def getDictFromObj(self):
        d = {'state': self.state,
         'enhancePoint': self.enhancePoint,
         'enhanceTime': self.enhanceTime}
        return d


class SkillEnhanceCommon(object):

    def getPrePart(self, part):
        row, col = part / 10, part % 10
        prePart = row - 1
        if prePart > 0:
            return prePart * 10 + col
        return 0

    def getNextPart(self, part):
        row, col = part / 10, part % 10
        nextPart = row + 1
        if nextPart <= const.SKILL_ENHANCE_ROW_MAX:
            return nextPart * 10 + col
        return 0

    def hasEnhanced(self, part):
        if not self.enhanceData.has_key(part):
            return False
        eVal = self.enhanceData[part]
        if eVal.state == const.SKILL_ENHANCE_STATE_UNUSABLE:
            return False
        return True

    def hasActivated(self, part):
        if not self.hasEnhanced(part):
            return False
        eVal = self.enhanceData[part]
        return eVal.state == const.SKILL_ENHANCE_STATE_ACTIVE

    def hasLearned(self, part):
        return self.enhanceData.has_key(part)

    def canAddEnhancePoint(self, owner, part, val = 1, skillEnhancePoint = 0, jingJie = 0, totalPoint = 0, bMsg = False):
        if BigWorld.component in ('cell',):
            channel = owner.client
        elif BigWorld.component in ('client',):
            channel = owner
        if not SED.data.has_key((self.skillId, part)):
            return False
        enhData = SED.data[self.skillId, part]
        if not self.hasLearned(part):
            if enhData.get('initLearn', 0) and utils.checkLearnSkillEnhForQumoJunJie(self.skillId, part, owner):
                self.enhanceData[part] = CSkillEnhanceVal(const.SKILL_ENHANCE_STATE_INACTIVE)
            else:
                gamelog.debug('cannot enhance skill: hasLearned', self.enhanceData, part)
                return False
        enhanceType = formula.getSkillEnhanceType(part)
        totalPoint = totalPoint or sum([ data.enhancePoint for pt, data in self.enhanceData.iteritems() if pt % 10 in enhanceType ])
        skillEnhancePoint = skillEnhancePoint or owner.skillEnhancePoint
        if skillEnhancePoint < val:
            gamelog.debug('cannot enhance skill: skillEnhancePoint', owner.skillEnhancePoint)
            bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_POINT_LESS, ())
            return False
        if val > 0 and self.enhanceData[part].enhancePoint >= len(enhData['pskills']) or self.enhanceData[part].enhancePoint + val > len(enhData['pskills']):
            bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_REACH_MAX_POINT, ())
            return False
        if enhData.has_key('needSkillLv') and self.level < enhData['needSkillLv'][self.enhanceData[part].enhancePoint + val - 1]:
            gamelog.debug('cannot enhance skill: skillLv', self.skillId, part, self.level, enhData['needSkillLv'])
            bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_SKILL_LV_LESS, ())
            return False
        if enhData.has_key('totalPoint') and totalPoint < enhData['totalPoint']:
            gamelog.debug('cannot enhance skill: totalPoint', totalPoint, enhData['totalPoint'])
            bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_TOTAL_POINT_LESS, ())
            return False
        if enhData.has_key('prePoint'):
            prePart = self.getPrePart(part)
            if not prePart or not self.hasLearned(prePart):
                gamelog.debug('cannot enhance skill: prePoint1', prePart, self.hasLearned(prePart))
                return False
            preVal = self.enhanceData[prePart]
            if preVal.enhancePoint < enhData['prePoint']:
                gamelog.debug('cannot enhance skill: prePoint2', preVal.enhancePoint, enhData['prePoint'])
                bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_PRE_POINT_LESS, ())
                return False
        jingJie = jingJie or owner.jingJie
        if utils.isJingJieOn() and enhData.has_key('needJingjie') and jingJie < enhData['needJingjie']:
            gamelog.debug('cannot enhance skill: jingjie', jingJie, enhData['needJingjie'])
            bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_NEED_JINGJIE, ())
            return False
        return True

    def canReduceEnhancePoint(self, owner, part, val = 1, bMsg = False):
        if BigWorld.component in ('cell',):
            channel = owner.client
        elif BigWorld.component in ('client',):
            channel = owner
        if not self.hasLearned(part):
            return False
        if self.enhanceData[part].enhancePoint - val < 0:
            return False
        nextPart = self.getNextPart(part)
        if nextPart and self.enhanceData.has_key(nextPart) and self.enhanceData[nextPart].enhancePoint > 0:
            enhData = SED.data[self.skillId, nextPart]
            if enhData.get('prePoint', -1) > self.enhanceData[part].enhancePoint - val:
                bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_REDUCE_FAIL_NEXT_PART, ())
                return False
        enhanceType = formula.getSkillEnhanceType(part)
        for pt, data in self.enhanceData.iteritems():
            if pt % 10 not in enhanceType:
                continue
            if pt / 10 > part / 10 and self.enhanceData[pt].enhancePoint > 0:
                bMsg and channel.showGameMsg(GMDD.data.ENHANCE_SKILL_REDUCE_FAIL_TOTAL_POINT, ())
                return False

        return True

    def countActiveSkillEnhancement(self):
        count = 0
        for part, eVal in self.enhanceData.items():
            if eVal.state == const.SKILL_ENHANCE_STATE_ACTIVE:
                count += 1

        return count
