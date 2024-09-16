#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCareerGuideShare.o
import BigWorld
import cPickle
import zlib
import gameglobal
import gametypes
from gameclass import SkillInfo
from guis import uiConst
from skillDataInfo import ClientSkillInfo
from cdata import game_msg_def_data as GMDD

class ImpCareerGuideShare(object):

    def onQueryCareerGuideInfo(self, data):
        """
        \xe6\x96\xb0\xe6\x89\x8b\xe5\xbc\x95\xe5\xaf\xbc\xe7\x9a\x84\xe6\x8e\xa8\xe8\x8d\x90\xe6\x95\xb0\xe6\x8d\xae
        :param data:
        :return:
        """
        if not data:
            return
        decodeData = cPickle.loads(zlib.decompress(data))
        self.carrerGuideData = decodeData

    def getOtherSkillInfo(self, entId):
        """
        \xe6\x9f\xa5\xe7\x9c\x8b\xe4\xbb\x96\xe4\xba\xba\xe6\x8a\x80\xe8\x83\xbd\xe4\xbf\xa1\xe6\x81\xaf
        :param entId:
        :return:
        """
        tgt = BigWorld.entities.get(entId, None)
        if not tgt:
            return
        else:
            self.base.querySkillInfoByChat(tgt.roleName)
            return

    def getOtherHierogramInfo(self, entId):
        """
        \xe6\x9f\xa5\xe7\x9c\x8b\xe4\xbb\x96\xe4\xba\xba\xe7\xa5\x9e\xe6\xa0\xbc\xe4\xbf\xa1\xe6\x81\xaf
        :param entId:
        :return:
        """
        tgt = BigWorld.entities.get(entId, None)
        if not tgt:
            return
        else:
            self.base.queryHierogramInfoByChat(tgt.roleName)
            return

    def onGetOtherHierogramInfo(self, lv, hieroEquip, hieroCrystals, effectsDict):
        self.sharedHierogramInfo = {'hieroEquip': hieroEquip,
         'hieroCrystals': hieroCrystals,
         'effectsDict': effectsDict,
         'lv': lv}
        pSkills, totalEffects = self._calcHieroArousePSkills(self.sharedHierogramInfo)
        self.sharedHierogramInfo['pSkills'] = pSkills
        self.sharedHierogramInfo['totalEffects'] = totalEffects
        gameglobal.rds.ui.hierogramShare.show()

    def onApplyWuShuangGuideData(self, applyInfo):
        selectedList = applyInfo.get('selectedList', [])
        detailInfo = applyInfo.get('detailInfo', {})
        wsLeftOffset = 0
        wsRightOffset = 0
        for skillId in selectedList:
            skillInfo = SkillInfo(skillId, 1)
            wsType = skillInfo.getSkillData('wsType', 1)
            selectedWs = []
            wsVal = self.wushuang[wsType]
            currSchemeNo = gameglobal.rds.ui.actionbar.currSchemeNo
            if currSchemeNo == uiConst.SHORT_CUT_CASE_1:
                selectedWs = wsVal.selectedWs
            elif currSchemeNo == uiConst.SHORT_CUT_CASE_2:
                selectedWs = wsVal.selectedWs1
            elif currSchemeNo == uiConst.SHORT_CUT_CASE_3:
                selectedWs = wsVal.selectedWs2
            skillCnt = len(selectedWs)
            offset = 0
            direction = 0
            if wsType == 1:
                offset = wsLeftOffset
                wsLeftOffset += 1
                direction = uiConst.SKILL_PANEL_SPECIAL_LEFT
            else:
                offset = wsRightOffset
                wsRightOffset += 1
                direction = uiConst.SKILL_PANEL_SPECIAL_RIGHT
            equipSkillId = gameglobal.rds.ui.skill.equipSkills[wsType - 1][offset]
            if equipSkillId and equipSkillId not in selectedList:
                self.cell.removeWsSkill(equipSkillId)
            gameglobal.rds.ui.skill.equipSkills[wsType - 1][offset] = skillId
            gameglobal.rds.ui.skill.setItem(skillId, 2, skillCnt * (wsType - 1) + offset)
            self.cell.addWsSkill(skillId)
            info = detailInfo.get(skillId, [])
            if info:
                enable, level, slots, proficiency, daoHeng, lingli = info
                if not self.wsSkills.has_key(skillId):
                    self.setWSData(skillId, enable, level, slots, proficiency, daoHeng, lingli, wsType, True)
                    clientSkillInfo = ClientSkillInfo(skillId, level)
                    self.preloadEffect(skillDataInfo.getSkillEffect(clientSkillInfo))
                    self.preloadAction(skillDataInfo.getSkillAction(clientSkillInfo))
                else:
                    self.setWSData(skillId, enable, level, slots, proficiency, daoHeng, lingli, isInit=False)
                gameglobal.rds.ui.skill.checkWsProficiency(skillId, proficiency)

        gameglobal.rds.ui.skill.refreshSpecialSkill()
        gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()
        gameglobal.rds.ui.skill.refreshDetailInfo()
        self.showGameMsg(GMDD.data.SET_WU_SHUANG_RECOMM_DATA_SUCCESS, ())

    def querySkillInfoByChat(self, roleName):
        if self._isSoul():
            self.showGameMsg(GMDD.data.SKILL_SHARE_NOT_AVALIABLE_CROSS, ())
        elif roleName == self.roleName:
            gameglobal.rds.ui.skill.show()
        else:
            self.base.querySkillInfoByChat(roleName)

    def queryHierogramInfoByChat(self, roleName):
        if type(roleName) != str:
            msg = 'jbx:queryHierogramInfoByChat, typeError:%s' % roleName
            self.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})
            return
        if self._isSoul():
            self.showGameMsg(GMDD.data.HIEROGRAM_SHARE_NOT_AVALIABLE_CROSS, ())
        elif roleName == self.roleName:
            gameglobal.rds.ui.roleInfo.show(tabIdx=uiConst.ROLEINFO_TAB_RUNE)
        else:
            self.base.queryHierogramInfoByChat(roleName)

    def querySpriteInfoByChat(self, roleName):
        if self._isSoul():
            self.showGameMsg(GMDD.data.SPRITE_SHARE_NOT_AVALIABLE_CROSS, ())
        elif roleName == self.roleName:
            gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0)
        else:
            self.base.querySpriteInfoByChat(roleName)
