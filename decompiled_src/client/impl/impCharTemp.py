#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCharTemp.o
import gameglobal
from cdata import game_msg_def_data as GMDD
from cdata import char_temp_white_list_data as CTWLD

class ImpCharTemp(object):

    def onGetCharTempData(self, data):
        pass

    def isUsingTemp(self):
        return hasattr(self, 'charTempId') and self.charTempId != 0

    def onGetCharTempHierogramInfo(self, tempId, lv, hieroEquip, hieroCrystals, effectsDict):
        gameglobal.rds.ui.hierogramShare.hide()
        self.sharedHierogramInfo = {'hieroEquip': hieroEquip,
         'hieroCrystals': hieroCrystals,
         'effectsDict': effectsDict,
         'lv': lv}
        pSkills, totalEffects = self._calcHieroArousePSkills(self.sharedHierogramInfo)
        self.sharedHierogramInfo['pSkills'] = pSkills
        self.sharedHierogramInfo['totalEffects'] = totalEffects
        gameglobal.rds.ui.hierogramShare.show()

    def onGetSkillData(self, data):
        if gameglobal.rds.ui.skillShareBG.widget:
            gameglobal.rds.ui.skillShareBG.hide()
        if data.has_key('tempId'):
            data.pop('tempId')
        data.get('wsSkill')['mws'] = self.mws
        data.get('wsSkill')['selectType1'] = gameglobal.rds.ui.skill.equipSkills[0]
        data.get('wsSkill')['selectType2'] = gameglobal.rds.ui.skill.equipSkills[1]
        self.sharedSkillData = data
        gameglobal.rds.ui.skillShareBG.show()

    def useCharTempSuccess(self, charTempId, extraInfo):
        self.showGameMsg(GMDD.data.ARENA_TEMPLATE_SET_SUCC, ())
        self.templateName = extraInfo.get('roleName', '')
        gameglobal.rds.ui.balanceArenaTemplate.useCharTempSuccess(charTempId)
        gameglobal.rds.ui.balanceArenaPreview.useCharTempSuccess(charTempId)
        self.closeTemplateRelatedWnd()

    def closeTemplateRelatedWnd(self):
        gameglobal.rds.ui.skill.hide()
        gameglobal.rds.ui.summonedWarSprite.hide()
        gameglobal.rds.ui.summonedWarSprite.recordSpriteNumber = 0
        gameglobal.rds.ui.summonedWarSprite.recordSpriteIndex = 0
        gameglobal.rds.ui.equipSoul.hide()
        gameglobal.rds.ui.roleInfo.hide()
        gameglobal.rds.ui.cardSystem.hide()

    def canChangeTemplate(self):
        return gameglobal.rds.configData.get('enableChangeCharTemp', False)

    def zanCharTempSuccess(self, gbID, roleName):
        self.showGameMsg(GMDD.data.ARENA_TEMPLATE_SUPPORT_SUCC, ())

    def inBalanceTemplateWhiteList(self):
        if not hasattr(self, 'roleURS'):
            return False
        return self.roleURS in CTWLD.data.keys()
