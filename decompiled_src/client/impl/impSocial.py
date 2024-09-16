#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSocial.o
import BigWorld
import gameglobal
import skillDataInfo
from guis import uiUtils
from data import prop_data as PD
from cdata import game_msg_def_data as GMDD
from cdata import prop_def_data as PDD

class ImpSocial(object):

    def getSocPrimaryPropValue(self, propId):
        if propId not in PDD.data.SOCIAL_PRIMARY_PROPERTIES:
            return 0
        if propId == PDD.data.PROPERTY_STR:
            return self.socProp.str
        if propId == PDD.data.PROPERTY_DEX:
            return self.socProp.dex
        if propId == PDD.data.PROPERTY_KNOW:
            return self.socProp.know
        if propId == PDD.data.PROPERTY_SENSE:
            return self.socProp.sense
        if propId == PDD.data.PROPERTY_STUDY:
            return self.socProp.study
        if propId == PDD.data.PROPERTY_CHARM:
            return self.socProp.charm
        if propId == PDD.data.PROPERTY_LUCKY:
            return self.socProp.lucky

    def updateSocialSkillInfo(self, skillId, enable, lv):
        if self.skills.has_key(skillId):
            self.skills[skillId].level = lv
            self.skills[skillId].enable = enable
        else:
            self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            self.skills[skillId].enable = enable
            self.skills[skillId].isSocialSkill = True
        if lv == 0:
            self.skills.pop(skillId)
        gameglobal.rds.ui.roleInfo.updateSocialSkill()

    def updateCurSocSchoolInfo(self, socSchool, tTime):
        self.socSchools[socSchool] = tTime
        gameglobal.rds.ui.roleInfo.updateSocialPanel()
        gameglobal.rds.ui.roleInfo.updateSocialJob()

    def onPropNotEnough(self, propList, needList):
        strName = ''
        for i in xrange(len(propList)):
            name = PD.data.get(propList[i], {}).get('chName', '')
            need = needList[i]
            if strName:
                strName = strName + ','
            strName = strName + name + uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_SOC_PROP2) % need

        BigWorld.player().showGameMsg(GMDD.data.LIFE_SKILL_SOC_PROP, strName)
