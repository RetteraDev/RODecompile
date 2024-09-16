#Embedded file name: /WORKSPACE/data/entities/client/helpers/skillappearancesutils.o
import BigWorld
import utils
import keys
import gameglobal
import gametypes
import const
import copy
from callbackHelper import Functor
from appSetting import Obj as AppSettings
from skillDataInfo import ClientSkillInfo
from skillDataInfo import AppearanceSkillInfo
from gamestrings import gameStrings
from helpers import tickManager
from data import skill_appearance_data as SAD
from data import skill_appearance_reverse_data as SARD
from data import creation_client_data as CCD
from data import creation_client_appearance_data as CCAD
from data import skill_appearance_config_data as SACD
from data import summoned_beast_appearance_data as SBAD
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD
import gamelog
DEFAULT_APPEARANCE_ID = 0
APPEARANCE_DEADLINE_FOREVER = 0
APPEARANCE_DEADLINE_NOT_ACTIVE = -1

def getPlayerAllSkillsWithAppearance():
    skillsWithAppearance = {}
    p = BigWorld.player()
    alldata = p.skillAppearancesDetail.allAppearanceData
    for sId, apperanceData in alldata.iteritems():
        if _isSubSkill(sId):
            continue
        skillsWithAppearance[sId] = {'skillId': sId}
        skillsWithAppearance[sId].update(apperanceData)
        if const.SKILL_APPEARANCE_KEY_INFO not in skillsWithAppearance[sId]:
            skillsWithAppearance[sId][const.SKILL_APPEARANCE_KEY_INFO] = {}
        skillsWithAppearance[sId][const.SKILL_APPEARANCE_KEY_INFO].update({DEFAULT_APPEARANCE_ID: APPEARANCE_DEADLINE_FOREVER})
        if const.SKILL_APPEARANCE_KEY_CURRENT not in skillsWithAppearance[sId]:
            skillsWithAppearance[sId][const.SKILL_APPEARANCE_KEY_CURRENT] = DEFAULT_APPEARANCE_ID

    allSkillIds = p.skills.keys() + p.wsSkills.keys()
    for sId in allSkillIds:
        if sId in SARD.data:
            if _isSubSkill(sId):
                continue
            appearanceIds = SARD.data[sId]
            if sId not in skillsWithAppearance:
                skillsWithAppearance[sId] = {'skillId': sId,
                 const.SKILL_APPEARANCE_KEY_INFO: {DEFAULT_APPEARANCE_ID: APPEARANCE_DEADLINE_FOREVER},
                 const.SKILL_APPEARANCE_KEY_CURRENT: DEFAULT_APPEARANCE_ID}
            for aid in appearanceIds:
                if aid not in skillsWithAppearance[sId][const.SKILL_APPEARANCE_KEY_INFO]:
                    skillsWithAppearance[sId][const.SKILL_APPEARANCE_KEY_INFO][aid] = APPEARANCE_DEADLINE_NOT_ACTIVE

    return skillsWithAppearance


def checkItemCanUse(item):
    if not item or not hasattr(item, 'isSkillAppearanceItem') or not item.isSkillAppearanceItem():
        return False
    aid = CID.data.get(item.id, {}).get('appearanceId', None)
    if aid is None:
        return False
    sid = SAD.data.get(aid, {}).get('skillId', (None,))[0]
    if sid is None:
        return False
    return sid in getPlayerAllSkillsWithAppearance()


def getAppearanceExpire(appearanceId):
    skillId = SAD.data.get(appearanceId, {}).get('skillId', (0,))[0]
    p = BigWorld.player()
    alldata = p.skillAppearancesDetail.allAppearanceData
    return alldata.get(skillId, {}).get(const.SKILL_APPEARANCE_KEY_INFO, {}).get(appearanceId, -1)


def _isSubSkill(skillId):
    for aid, data in SAD.data.iteritems():
        allSkill = data.get('skillId', ())
        try:
            index = allSkill.index(skillId)
        except:
            index = -1

        if index > 0:
            return True

    return False


class SkillAppearancesDetail(object):

    def __init__(self, owner):
        self.owner = owner
        self.updateData()
        self.trialing = -1
        self.endTrialTimer = -1
        self._tickId = -1
        if self.owner and self.owner == BigWorld.player():
            self.startAppearanceExpireTimer()

    def clear(self):
        self.stopTimer()

    def updateData(self):
        self.allAppearanceData = copy.deepcopy(self.owner.skillAppearances)
        self.updateDataExpire()

    def updateDataExpire(self):
        if self.allAppearanceData:
            for skillId, detail in self.allAppearanceData.iteritems():
                current = detail.get(const.SKILL_APPEARANCE_KEY_CURRENT, 0)
                if current != 0:
                    expire = detail.get(const.SKILL_APPEARANCE_KEY_INFO, {}).get(current, 0)
                    if expire == -1 or expire > 0 and expire < utils.getNow():
                        detail[const.SKILL_APPEARANCE_KEY_CURRENT] = 0
                        if self.owner and self.owner == BigWorld.player():
                            gameglobal.rds.ui.actionbar.refreshActionbar()
                            gameglobal.rds.ui.skillAppearance.refreshInfo()

    def startAppearanceExpireTimer(self):
        self.stopTimer()
        self._tickId = tickManager.addTick(5, self.__timer)

    def stopTimer(self):
        if self._tickId != -1:
            tickManager.stopTick(self._tickId)
            self._tickId = -1

    def __timer(self):
        self.updateDataExpire()

    def canShielded(self, appearanceId):
        return SAD.data.get(appearanceId, {}).get('noShield', False)

    def getCurrentAppearance(self, skillId):
        if not gameglobal.rds.configData.get('enableSkillAppearance', False):
            return -1
        if self.trialing in SARD.data.get(skillId, []):
            return self.trialing
        skillDetail = self.allAppearanceData.get(skillId, {})
        currentId = skillDetail.get(const.SKILL_APPEARANCE_KEY_CURRENT, 0)
        if currentId <= 0:
            return -1
        deadLine = skillDetail.get(const.SKILL_APPEARANCE_KEY_INFO, {}).get(currentId, -1)
        if not (utils.getNow() < deadLine or deadLine == 0):
            return -1
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableSkillAppearanceBlock', False):
            if bool(int(AppSettings.get(keys.SET_BLOCK_SKILL_APPEARANCE, 0))):
                if p.id != self.owner.id and self.canShielded(currentId):
                    return -1
        if hasattr(p, 'anonymNameMgr') and p.anonymNameMgr:
            anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=self.owner)
            if anonymousType != gametypes.AnonymousType_None:
                if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_SKILL_EFFECT_HIDE, False):
                    return -1
        return currentId

    def getGeneralAppearanceSkillInfo(self, skillId, skillLv):
        appearanceId = self.getCurrentAppearance(skillId)
        if appearanceId == -1:
            return ClientSkillInfo(skillId, skillLv)
        return AppearanceSkillInfo(skillId, appearanceId, AppearanceSkillInfo.SKILL_TYPE_GENERAL)

    def getCreationAppearanceData(self, cid):
        skillId = CCD.data.get(cid, {}).get('sid', -1)
        if skillId == -1:
            return CCD.data.get(cid, {})
        appearanceId = self.getCurrentAppearance(skillId)
        if appearanceId == -1:
            return CCD.data.get(cid, {})
        ainfo = CCAD.data.get((cid, appearanceId), {})
        if not ainfo:
            return CCD.data.get(cid, {})
        return ainfo

    def getSummonedBeastAppearanceData(self, summonedBeastId, skillId):
        if skillId == -1 or summonedBeastId == -1:
            return {}
        appearanceId = self.getCurrentAppearance(skillId)
        if appearanceId == -1:
            return {}
        return SBAD.data.get((summonedBeastId, appearanceId), {})

    def getCurrentStateSkillInfo(self, skillId, level, state):
        appearanceId = self.getCurrentAppearance(skillId)
        if appearanceId <= 0:
            return ClientSkillInfo(skillId, level, 3, state)
        return AppearanceSkillInfo(skillId, appearanceId, AppearanceSkillInfo.SKILL_TYPE_STATE, state)

    def trailAppearance(self, skillId, appearanceId):
        if self.owner.id != BigWorld.player().id:
            gamelog.debug('ypc@ trailAppearance failed! only player can trailAppearance')
            return
        if appearanceId not in SARD.data.get(skillId, []):
            gamelog.debug('ypc@ trailAppearance failed! error appearanceId')
            return
        self.endTrialAppearance()
        self.trialing = appearanceId
        trialTime = SACD.data.get('TrialTime', 10)
        self.endTrialTimer = BigWorld.callback(trialTime, Functor(self.endTrialAppearance, True))
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SKILL_APPEARANCE_TRIAL_WARNING % trialTime)
        gameglobal.rds.ui.actionbar.refreshActionbar()

    def endTrialAppearance(self, refreshActionbar = False):
        self.trialing = -1
        if self.endTrialTimer != -1:
            BigWorld.cancelCallback(self.endTrialTimer)
            self.endTrialTimer = -1
        if refreshActionbar:
            gameglobal.rds.ui.actionbar.refreshActionbar()
