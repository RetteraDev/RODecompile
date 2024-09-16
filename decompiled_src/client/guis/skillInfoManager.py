#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillInfoManager.o
from gamestrings import gameStrings
import BigWorld
import utils
import const
import gamelog
import uiUtils
import gameglobal
import skillDataInfo
import weakref
from guis import uiConst
from gameclass import Singleton
from gameclass import SkillInfo
from gameclass import PSkillInfo
from Scaleform import GfxValue
from callbackHelper import Functor
from data import skill_panel_data as SPD
from data import skill_general_data as SGD
from data import skill_general_template_data as SGTD
from data import sys_config_data as SCFD
from cdata import pskill_data as PD
from cdata import pskill_template_data as PSTD
from cdata import skill_enhance_lv_data as SELD
from cdata import game_msg_def_data as GMDD
DATA_TYPE_SKILL = 1
DATA_TYPE_PSKILL = 2
SKILL_STATE_UNSTUDIED = 1
SKILL_STATE_TOP_LEVEL = 2
SKILL_STATE_CAN_NOT_STUDY_LV = 3
SKILL_STATE_CAN_NOT_STUDY_MONEY = 4
SKILL_STATE_CAN_STUDY = 5
SKILL_STATE_CAN_NOT_STUDY_SKILL_POINT = 6

class ISkillInfo(object):

    def __init__(self, owner):
        self.owner = weakref.ref(owner)
        self.sType = 0
        self.skillList = []
        self.skillLv = {}
        self.isEditMode = False

    def setEditMode(self, value):
        self.isEditMode = value

    def clear(self):
        self.skillLv = {}
        self.isEditMode = False

    def checkSkillState(self, skillInfo):
        p = BigWorld.player()
        extra = {}
        curLv = self.getSkillLvBySkillInfo(skillInfo)
        if curLv == const.MAX_SKILL_LEVEL:
            return (SKILL_STATE_TOP_LEVEL, extra)
        if skillInfo.hasSkillData('learnLv'):
            learnLv = skillInfo.getSkillData('learnLv')
            if p.arenaLv < learnLv:
                extra['learnLv'] = learnLv
                return (SKILL_STATE_CAN_NOT_STUDY_LV, extra)
        if not self.isEditMode:
            if skillInfo.hasSkillData('learnGold'):
                learnGold = skillInfo.getSkillData('learnGold')
                if p.cash + p.bindCash < learnGold:
                    extra['money'] = learnGold
                    return (SKILL_STATE_CAN_NOT_STUDY_MONEY, extra)
        if skillInfo.hasSkillData('learnPoint'):
            learnPoint = skillInfo.getSkillData('learnPoint')
            if self.owner().getRestSkillPoint() < learnPoint:
                extra['skillPoint'] = learnPoint
                return (SKILL_STATE_CAN_NOT_STUDY_SKILL_POINT, extra)
        return (SKILL_STATE_CAN_STUDY, extra)

    def calcAddEnable(self, skillLv, skillInfo):
        state, _ = self.checkSkillState(skillInfo)
        if state == SKILL_STATE_CAN_STUDY:
            btnEnabled = True
            if skillLv == const.MAX_SKILL_LEVEL:
                btnEnabled = False
        elif state == SKILL_STATE_CAN_NOT_STUDY_MONEY:
            btnEnabled = True
        else:
            btnEnabled = False
        if self.owner().getRestSkillPoint() < skillInfo.getSkillData('learnPoint'):
            btnEnabled = False
        return btnEnabled

    def getSkillInfo(self):
        pass

    def getSkillIconState(self, skillId):
        p = BigWorld.player()
        if self.sType == DATA_TYPE_SKILL:
            if p.isPubgCommSkillLock(skillId):
                return uiConst.SKILL_ICON_STAT_LOCK
            if p.skills.has_key(skillId):
                return uiConst.SKILL_ICON_STAT_USEABLE
            if p.wsSkills.has_key(skillId):
                return uiConst.SKILL_ICON_STAT_USEABLE
        elif self.sType == DATA_TYPE_PSKILL:
            if p.learnedPSkills.has_key(skillId):
                return uiConst.SKILL_ICON_STAT_USEABLE
        return uiConst.SKILL_ICON_STAT_GRAY


class UICommonSkillInfo(ISkillInfo):

    def __init__(self, owner):
        super(UICommonSkillInfo, self).__init__(owner)
        self.sType = DATA_TYPE_SKILL

    def _getSkillLvStr(self, skillId):
        skillLv = self.getSkillLv(skillId)
        if skillLv:
            skLvStr = str(skillLv) + '/' + str(SCFD.data.get('maxSkillLevel', 15))
        else:
            skLvStr = gameStrings.TEXT_SKILLINFOMANAGER_129 % SGD.data.get((skillId, 1), {}).get('learnLv', 1)
        return (skillLv, skLvStr)

    def getSkillLv(self, skillId):
        p = BigWorld.player()
        if self.skillLv.has_key(skillId):
            lv = self.skillLv[skillId]
        elif self.isEditMode:
            skillPointScheme = p.getSpecialSkillPoint()
            lv = skillPointScheme.get(skillId, {}).get('level', 1)
        elif p.skills.get(skillId, None):
            lv = p.skills[skillId].level
        elif p.pubgSkills.get(skillId, None):
            lv = p.pubgSkills[skillId].lv
        else:
            lv = 0
        return lv

    def getConsumePoint(self):
        cnt = 0
        p = BigWorld.player()
        skillPointScheme = None
        if self.isEditMode:
            skillPointScheme = p.getSpecialSkillPoint()
        for skillId, level in self.skillLv.iteritems():
            if self.isEditMode:
                baseLevel = skillPointScheme.get(skillId, {}).get('level', 1)
            else:
                if not p.skills.has_key(skillId):
                    continue
                baseLevel = p.skills[skillId].level
            if level > baseLevel:
                for curLevel in xrange(baseLevel, level):
                    skillInfo = self.getSkillInfoData(skillId, curLevel + 1)
                    cnt += skillInfo.getSkillData('learnPoint', 0)

            elif self.isEditMode:
                for curLevel in xrange(baseLevel, level, -1):
                    skillInfo = self.getSkillInfoData(skillId, curLevel)
                    cnt -= skillInfo.getSkillData('learnPoint', 0)

        return cnt

    def getSkillInfoData(self, skillId, skillLv):
        if skillLv > const.MAX_SKILL_LEVEL:
            skillLv = const.MAX_SKILL_LEVEL
        elif skillLv < 1:
            skillLv = 1
        return SkillInfo(skillId, skillLv)

    def getSkillLvBySkillInfo(self, skillInfo):
        p = BigWorld.player()
        curLv = 0
        if self.isEditMode:
            if self.skillLv.has_key(skillInfo.num):
                curLv = self.skillLv[skillInfo.num]
            else:
                skillPointScheme = p.getSpecialSkillPoint()
                if skillPointScheme.has_key(skillInfo.num):
                    curLv = skillPointScheme.get(skillInfo.num, {}).get('level', 0)
        elif not p.skills.has_key(skillInfo.num):
            curLv = 0
        else:
            sVal = p.skills[skillInfo.num]
            if sVal.level == const.MAX_SKILL_LEVEL:
                return const.MAX_SKILL_LEVEL
            curLv = sVal.level
        return curLv

    def getSubSkillItemInfo(self, subSkillId):
        sd = skillDataInfo.ClientSkillInfo(subSkillId)
        icon = sd.getSkillData('icon', None)
        p = BigWorld.player()
        skillLv, skLvStr = self._getSkillLvStr(subSkillId)
        name = SGTD.data.get(subSkillId, {}).get('name', '')
        item = {'icon': {'iconPath': 'skill/icon/' + str(icon) + '.dds'},
         'skillName': name,
         'skillLv': skillLv,
         'skLvStr': skLvStr,
         'learnedSkill': p.skills.has_key(subSkillId),
         'skillSlotState': self.getSkillIconState(subSkillId)}
        return item

    def getSkillItemInfo(self, skillId):
        p = BigWorld.player()
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        skillLv, skLvStr = self._getSkillLvStr(skillId)
        name = SGTD.data.get(skillId, {}).get('name', '')
        if p.skills.get(skillId, None) and not self.isEditMode:
            enableSubBtn = skillLv > p.skills[skillId].level
        else:
            enableSubBtn = skillLv > 1
        skillInfo = SkillInfo(skillId, min(skillLv + 1, const.MAX_SKILL_LEVEL))
        childId = skillInfo.getSkillData('childId', [])
        subSkillInfo = []
        if childId:
            for subSkillId in childId:
                subSkillInfo.append(self.getSubSkillItemInfo(subSkillId))

        enableAddBtn = self.calcAddEnable(skillLv, skillInfo)
        learnLv = skillInfo.getSkillData('learnLv', 1)
        item = {'icon': {'iconPath': 'skill/icon/' + str(icon) + '.dds'},
         'skillName': name,
         'learnedSkill': p.skills.has_key(skillId),
         'skillSlotState': self.getSkillIconState(skillId),
         'hasSkill': p.skills.get(skillId, None) != None,
         'enableAddBtn': enableAddBtn and (not p.isUsingTemp() or p.canChangeTemplate()),
         'skillLv': skillLv,
         'skLvStr': skLvStr,
         'enableSubBtn': enableSubBtn and (not p.isUsingTemp() or p.canChangeTemplate()),
         'subSkillInfo': subSkillInfo,
         'skillId': skillId,
         'learnLv': learnLv}
        return item

    def getSkillInfo(self):
        skillInfo = []
        p = BigWorld.player()
        self.skillList = SPD.data.get(p.school, {}).get('wsType1Skills', []) + SPD.data.get(p.school, {}).get('wsType2Skills', [])
        if not gameglobal.rds.ui.skill.isRemoveOldSchoolSkill():
            skillList = self.skillList
        else:
            skillList = gameglobal.rds.ui.skill.getSelectedSchoolSkillList()
        for skillId in skillList:
            item = self.getSkillItemInfo(skillId)
            skillInfo.append(item)

        gameglobal.rds.ui.skill.normalSkills = self.skillList
        return uiUtils.array2GfxAarry(skillInfo, True)

    def refreshSkillById(self, skillId):
        if skillId not in self.skillList:
            return
        commonSkillMc = gameglobal.rds.ui.skill.commonSkillMc
        if not commonSkillMc:
            return
        index = self.skillList.index(skillId)
        info = self.getSkillItemInfo(skillId)
        if commonSkillMc:
            commonSkillMc.Invoke('refreshNormalSkillLvByIndex', (GfxValue(index), uiUtils.dict2GfxDict(info, True)))
        gameglobal.rds.ui.skill.refreshSkillPoint()

    def addSkillPoint(self, skillId):
        p = BigWorld.player()
        if self.owner().getRestSkillPoint() <= 0:
            p.showGameMsg(GMDD.data.SKILL_LV_UP_LACK_SKILL_POINT, ())
            return
        else:
            if self.isEditMode:
                sk = p.getSpecialSkillPoint().get(skillId, {})
                if self.skillLv.has_key(skillId):
                    self.skillLv[skillId] = min(self.skillLv[skillId] + 1, const.MAX_SKILL_LEVEL)
                    if sk and self.skillLv[skillId] == sk['level']:
                        self.skillLv.pop(skillId, None)
                else:
                    lv = sk.get('level', 1)
                    self.skillLv[skillId] = lv + 1
            elif self.skillLv.has_key(skillId):
                self.skillLv[skillId] = min(self.skillLv[skillId] + 1, const.MAX_SKILL_LEVEL)
                sk = p.skills.get(skillId, None)
                if sk and self.skillLv[skillId] == sk.level:
                    self.skillLv.pop(skillId, None)
            else:
                sk = p.skills.get(skillId)
                if sk:
                    self.skillLv[skillId] = sk.level + 1
                else:
                    gamelog.error('@hjx skillId:%d not in skills!!!' % skillId)
            self.refreshSkillById(skillId)
            return

    def reduceSkillPoint(self, skillId):
        p = BigWorld.player()
        if self.isEditMode:
            sk = p.getSpecialSkillPoint().get(skillId, {})
            enhancePoint = 0
            if sk and sk.has_key('enhanceData'):
                for enhData in sk['enhanceData'].itervalues():
                    enhancePoint += enhData.get('enhancePoint', 0)

            if enhancePoint:
                gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_SKILLINFOMANAGER_340)
                return
            if self.skillLv.has_key(skillId):
                self.skillLv[skillId] = max(self.skillLv[skillId] - 1, 1)
                if sk and self.skillLv[skillId] == sk.get('level', 1):
                    self.skillLv.pop(skillId, None)
            else:
                lv = sk.get('level', 1)
                self.skillLv[skillId] = lv - 1
        elif self.skillLv.has_key(skillId):
            self.skillLv[skillId] = max(self.skillLv[skillId] - 1, 1)
            sk = p.skills.get(skillId, None)
            if sk and self.skillLv[skillId] == sk.level:
                self.skillLv.pop(skillId, None)
        else:
            sk = p.skills.get(skillId)
            if sk:
                self.skillLv[skillId] = sk.level - 1
            else:
                gamelog.error('@hjx skillId:%d not in skills!!!' % skillId)
        self.refreshSkillById(skillId)


class UIPSkillInfo(ISkillInfo):

    def __init__(self, owner):
        super(UIPSkillInfo, self).__init__(owner)
        self.sType = DATA_TYPE_PSKILL

    def _getSkillLvStr(self, skillId):
        skillLv = self.getSkillLv(skillId)
        p = BigWorld.player()
        pskillInfo = self.genPskillInfo(skillId, skillLv)
        learnEnhanceLv = pskillInfo.getSkillData('learnEnhanceLv', 0)
        enhanceLv = utils.getSkillEnhanceLv(p)
        if learnEnhanceLv and enhanceLv < learnEnhanceLv:
            skLvStr = gameStrings.TEXT_SKILLINFOMANAGER_380 % SELD.data.get(learnEnhanceLv, {}).get('name', '')
        elif skillLv == 0:
            skLvStr = gameStrings.TEXT_SKILLINFOMANAGER_129 % PD.data.get((skillId, 1), {}).get('learnLv', 1)
        else:
            skLvStr = gameStrings.TEXT_SKILLINFOMANAGER_384
        return (skillLv, skLvStr)

    def getSkillLv(self, skillId):
        p = BigWorld.player()
        if self.skillLv.has_key(skillId):
            lv = self.skillLv[skillId]
        elif p.learnedPSkills.get(skillId, None):
            lv = p.learnedPSkills[skillId].level
        else:
            lv = 0
        return lv

    def genPskillInfo(self, pskId, skillLv):
        if self.isAutoLvUp(pskId):
            return PSkillInfo(pskId, 1)
        else:
            return PSkillInfo(pskId, min(skillLv + 1, const.MAX_SKILL_LEVEL))

    def getConsumePoint(self):
        cnt = 0
        p = BigWorld.player()
        for skillId, level in self.skillLv.iteritems():
            if p.learnedPSkills.get(skillId, None):
                baseLevel = p.learnedPSkills[skillId].level
            else:
                baseLevel = 0
            if level > baseLevel:
                for curLevel in xrange(baseLevel, level):
                    skillInfo = self.getSkillInfoData(skillId, curLevel + 1)
                    cnt += skillInfo.getSkillData('learnPoint', 0)

        return cnt

    def getSkillInfoData(self, skillId, skillLv):
        if skillLv > const.MAX_SKILL_LEVEL:
            skillLv = const.MAX_SKILL_LEVEL
        elif skillLv < 1:
            skillLv = 1
        return PSkillInfo(skillId, skillLv)

    def getSkillLvBySkillInfo(self, skillInfo):
        p = BigWorld.player()
        if not p.learnedPSkills.has_key(skillInfo.num):
            curLv = 0
        else:
            sVal = p.learnedPSkills[skillInfo.num]
            if sVal.level == const.MAX_SKILL_LEVEL:
                return const.MAX_SKILL_LEVEL
            curLv = sVal.level
        return curLv

    def isAutoLvUp(self, pskId):
        pskInfo = PSkillInfo(pskId, 1)
        return pskInfo.getSkillData('autoLvUp', 0)

    def getSkillItemInfo(self, pskId):
        p = BigWorld.player()
        name = PSTD.data.get(pskId, {}).get('sname', '')
        skillLv, skLvStr = self._getSkillLvStr(pskId)
        pskInfo = self.genPskillInfo(pskId, skillLv)
        icon = pskInfo.getSkillData('icon', 'notFound')
        if p.learnedPSkills.get(pskId, None):
            enableSubBtn = skillLv > p.learnedPSkills[pskId].level
        else:
            enableSubBtn = skillLv > 1
        enableAddBtn = self.calcAddEnable(skillLv, pskInfo) and not self.isAutoLvUp(pskId)
        item = {'icon': {'iconPath': 'skill/icon64/' + str(icon) + '.dds'},
         'skillName': name,
         'enableAddBtn': enableAddBtn and (not p.isUsingTemp() or p.canChangeTemplate()),
         'enableSubBtn': enableSubBtn and (not p.isUsingTemp() or p.canChangeTemplate()),
         'skLvStr': skLvStr,
         'learnedSkill': p.learnedPSkills.has_key(pskId),
         'skillSlotState': self.getSkillIconState(pskId),
         'hasSkill': p.learnedPSkills.has_key(pskId),
         'skillLv': skillLv}
        return item

    def getSkillInfo(self):
        pskills = []
        p = BigWorld.player()
        self.skillList = SPD.data.get(p.school, {}).get('pskills', [])
        for pskId in self.skillList:
            item = self.getSkillItemInfo(pskId)
            pskills.append(item)

        gameglobal.rds.ui.skill.pskills = self.skillList
        return uiUtils.array2GfxAarry(pskills, True)

    def refreshSkillById(self, pskId):
        if pskId not in self.skillList:
            return
        commonSkillMc = gameglobal.rds.ui.skill.commonSkillMc
        if not commonSkillMc:
            return
        index = self.skillList.index(pskId)
        item = self.getSkillItemInfo(pskId)
        if commonSkillMc:
            commonSkillMc.Invoke('refreshPSkillLvByIndex', (GfxValue(index), uiUtils.dict2GfxDict(item, True)))
        gameglobal.rds.ui.skill.refreshSkillPoint()

    def addSkillPoint(self, skillId):
        p = BigWorld.player()
        if self.owner().getRestSkillPoint() <= 0:
            p.showGameMsg(GMDD.data.SKILL_LV_UP_LACK_SKILL_POINT, ())
            return
        else:
            if self.skillLv.has_key(skillId):
                self.skillLv[skillId] = min(self.skillLv[skillId] + 1, const.MAX_SKILL_LEVEL)
                sk = p.pskills.get(skillId, {}).get(skillId, None)
                if sk and self.skillLv[skillId] == sk.level:
                    self.skillLv.pop(skillId, None)
            else:
                sk = p.learnedPSkills.get(skillId, None)
                if sk:
                    self.skillLv[skillId] = sk.level + 1
                else:
                    self.skillLv[skillId] = 1
            self.refreshSkillById(skillId)
            return

    def reduceSkillPoint(self, skillId):
        p = BigWorld.player()
        if self.skillLv.has_key(skillId):
            self.skillLv[skillId] = max(self.skillLv[skillId] - 1, 0)
            sk = p.learnedPSkills.get(skillId, None)
            if sk and self.skillLv[skillId] == sk.level:
                self.skillLv.pop(skillId, None)
        else:
            sk = p.learnedPSkills.get(skillId, None)
            if sk:
                self.skillLv[skillId] = sk.level - 1
            else:
                self.skillLv[skillId] = 0
        self.refreshSkillById(skillId)


class SkillInfoManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.reset()
        self.__createIns()

    def __createIns(self):
        self.commonSkillIns = UICommonSkillInfo(self)
        self.pSkillIns = UIPSkillInfo(self)

    def reset(self):
        self.commonSkillIns = None
        self.pSkillIns = None
        self.isEditMode = False

    def clear(self):
        self.commonSkillIns.clear()
        self.pSkillIns.clear()
        self.isEditMode = False

    def setEditMode(self, value):
        self.isEditMode = value
        self.commonSkillIns.setEditMode(value)

    def saveSkillSchedule(self):
        p = BigWorld.player()
        if self.isEditMode:
            if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                self.saveWWSkillSchedule()
            elif gameglobal.rds.configData.get('enableCrossBFSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                self.saveCrossBFSchedule()
            else:
                self.saveArenaSkillSchedule()
            return
        if self.commonSkillIns.getConsumePoint() + self.pSkillIns.getConsumePoint() == 0:
            p.showGameMsg(GMDD.data.SKILL_LV_UP_FAILED_NOTHING, ())
            return
        if p.isUsingTemp():
            p.cell.upgradeSkills(self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values(), False)
            return
        cnt = p.skillPoint + self.commonSkillIns.getConsumePoint() + self.pSkillIns.getConsumePoint()
        if cnt > p.activeSkillPoint:
            gamelog.debug('@hjx skill#saveSkillSchedule:', self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())
            p.cell.upgradeSkills(self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values(), True)
        else:
            msg = gameStrings.TEXT_SKILLINFOMANAGER_598 % (const.CASH_DESC, const.BIND_CASH_DESC)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmUpgradeSkills, 0))

    def confirmUpgradeSkills(self, needCash):
        gamelog.debug('@hjx skill#confirmUpgradeSkills:', self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())
        p = BigWorld.player()
        if uiUtils.checkBindCashEnough(needCash, p.bindCash, p.cash, Functor(p.cell.upgradeSkills, self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values(), False)):
            p.cell.upgradeSkills(self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values(), False)

    def saveCrossBFSchedule(self):
        p = BigWorld.player()
        gamelog.info('jbx:saveCrossBFSchedule', self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())
        p.base.updateSkillSchemeEx(const.SKILL_SCHEME_CROSS_BF, self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())

    def saveArenaSkillSchedule(self):
        p = BigWorld.player()
        gamelog.info('jbx:saveArenaSkillSchedule', self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())
        p.base.updateSkillSchemeEx(const.SKILL_SCHEME_ARENA, self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())

    def saveWWSkillSchedule(self):
        p = BigWorld.player()
        gamelog.info('jbx:updateWingWorldSkillScheme', self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())
        p.base.updateSkillSchemeEx(const.SKILL_SCHEME_WINGWORLD, self.commonSkillIns.skillLv.keys(), self.commonSkillIns.skillLv.values(), self.pSkillIns.skillLv.keys(), self.pSkillIns.skillLv.values())

    def getRestSkillPoint(self):
        p = BigWorld.player()
        curMaxSkillPoints = 0
        skillPoint = 0
        if self.isEditMode:
            curMaxSkillPoints = 0
            if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                wwSkillScheme = utils.getWingWorldSkillSchemaData(p.getWingWorldGroupId())
                if wwSkillScheme:
                    curMaxSkillPoints = wwSkillScheme.get('wingSkillPoint', 0)
                skillPoint = p.wingWorldSkillPoint
            elif gameglobal.rds.configData.get('enableCrossBFSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                crossBfScheme = utils.getCrossBFSkillSchemaData(p.lv)
                if crossBfScheme:
                    curMaxSkillPoints = crossBfScheme.get('skillPoint', 0)
                skillPoint = p.crossBFSkillPoint
            else:
                arenaSkillScheme = utils.getArenaSkillSchemeData(p.realLv)
                if arenaSkillScheme:
                    curMaxSkillPoints = arenaSkillScheme.get('arenaSkillPoint', 0)
                skillPoint = p.arenaSkillPoint
        else:
            curMaxSkillPoints = utils.getCurSkillPoint(p.lv)
            skillPoint = p.skillPoint
        return curMaxSkillPoints - skillPoint - (self.commonSkillIns.getConsumePoint() + self.pSkillIns.getConsumePoint())


def getInstance():
    return SkillInfoManager.getInstance()
