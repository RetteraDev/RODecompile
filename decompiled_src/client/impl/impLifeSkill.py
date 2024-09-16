#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impLifeSkill.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import gamelog
import const
import utils
from guis import events
from guis import uiConst
from helpers.eventDispatcher import Event
from data import life_skill_subtype_data as LSSD
from data import life_skill_subtype_reverse_data as LSSRD
from data import life_skill_expertise_data as LSED
from data import life_skill_data as LSD
from data import life_skill_collection_data as LSCD
from data import life_skill_manufacture_data as LSMD
from data import life_skill_event_notify_data as LSEND

class ImpLifeSkill(object):

    def sendLifeSkillInfo(self, skills):
        gamelog.debug('@hjx lifeSkill#sendLifeSkillInfo:', skills)
        self.expertiseReverseInfo = {gametypes.LIFE_SKILL_TYPE_COLLECTION: [],
         gametypes.LIFE_SKILL_TYPE_MANUFACTURE: []}
        for skill in skills:
            skill = list(skill)
            if not LSD.data.has_key((skill[0], skill[1])):
                continue
            self.lifeSkill[skill[0]] = {'level': skill[1],
             'suSkills': skill[2],
             'expertise': skill[3],
             'exp': skill[4]}
            gameglobal.rds.ui.lifeSkillNew.addSkillLevelUpPushMsg(skill[0], skill[4], skill[1])
            if skill[3]:
                expertiseData = LSED.data[skill[3]]
                subTypeId = expertiseData['subType']
                subTypeData = LSSD.data[subTypeId]
                self.expertiseReverseInfo[subTypeData['type']].append(skill[3])

        for key in LSSRD.data.keys():
            for subKey in LSSRD.data[key].keys():
                if not self.lifeSkill.has_key(subKey):
                    self.lifeSkill[subKey] = {'level': 0,
                     'suSkills': 0,
                     'expertise': 0,
                     'exp': 0}

        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def getLiefSkillAttr(self, skillId, attr, default = 0):
        if not self.lifeSkill.has_key(skillId):
            return default
        if not self.lifeSkill[skillId].has_key(attr):
            return default
        return self.lifeSkill[skillId][attr]

    def updateLifeSkillInfo(self, skillId, level, exp, subSkills, expertise):
        gamelog.debug('@hjx lifeSkill#updateLifeSkillInfo:', skillId, level, exp, subSkills, expertise)
        p = BigWorld.player()
        oldYuLi = p.getCurYueLiVal()
        if not self.lifeSkill.has_key(skillId):
            return
        gameglobal.rds.ui.lifeSkillNew.addSkillLevelUpPushMsg(skillId, exp, level)
        self.lifeSkill[skillId]['level'] = level
        self.lifeSkill[skillId]['exp'] = exp
        self.lifeSkill[skillId]['subSkills'] = subSkills
        self.lifeSkill[skillId]['expertise'] = expertise
        newYuLi = p.getCurYueLiVal()
        p.checkLifeSkillBreak(oldYuLi, newYuLi)
        lvupEvent = Event(events.EVENT_LIFE_SKILL_UPDATE, {'skillId': skillId})
        gameglobal.rds.ui.dispatchEvent(lvupEvent)
        gameglobal.rds.ui.lifeSkill.onLifeSkillLevelUp()

    def onAddLifeSkillExp(self, skillId, exp, amount):
        gamelog.debug('@hjx lifeSkill#onAddLifeSkillExp:', skillId, exp, amount)
        if not self.lifeSkill.has_key(skillId):
            return
        self.lifeSkill[skillId]['exp'] = exp
        gameglobal.rds.ui.showLifeSkillLabel(uiConst.LIFE_SKILL_NUM_TYPE_EXP, amount)
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def onRepairLifeEquipmentFailed(self, subType, part, mType):
        pass

    def _getLifeSkillType(self, skillId):
        if not self.lifeSkill.has_key(skillId):
            return 0
        sData = LSD.data.get((skillId, 1))
        if not sData:
            return 0
        return sData['type']

    def _getSubSkillData(self, skType, subSkId):
        if skType == gametypes.LIFE_SKILL_TYPE_COLLECTION:
            return LSCD.data.get(subSkId)
        elif skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
            return LSMD.data.get(subSkId)
        else:
            return None

    def beginLifeSkill(self, skillId, subSkId, extra):
        skType = self._getLifeSkillType(skillId)
        self.curLifeSkillType = skType
        if skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
            self.manuSkillStartTimeStamp = utils.getNow()
            self.manuSpellTime = extra.get('spellTime', 15)
            self.manuId = subSkId
            gameglobal.rds.ui.lifeSkillNew.refreshPanel(gametypes.MANUFACTURE_STAGE_BEGIN)
        sData = self._getSubSkillData(skType, subSkId)
        soundId = sData.get('soundId', 0)
        if soundId > 0:
            gameglobal.rds.sound.playSound(soundId)

    def resetManu(self):
        self.manuId = 0
        self.manuSpellTime = 0
        self.manuSkillStartTimeStamp = 0

    def cancelLifeSkill(self, skillId, subSkId):
        skType = self._getLifeSkillType(skillId)
        if skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
            self.resetManu()
            gameglobal.rds.ui.lifeSkillNew.refreshPanel(gametypes.MANUFACTURE_STAGE_CANCEL)
        sData = self._getSubSkillData(skType, subSkId)
        soundId = sData.get('soundId', 0)
        if soundId > 0:
            gameglobal.rds.sound.stopSound(soundId)

    def finishLifeSkill(self, skillId, subSkId):
        skType = self._getLifeSkillType(skillId)
        if skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
            self.resetManu()
            gameglobal.rds.ui.lifeSkillNew.refreshPanel(gametypes.MANUFACTURE_STAGE_SUCC)
        else:
            gameglobal.rds.ui.lifeSkillNew.refreshPanel()
        gameglobal.rds.ui.roleInfo.updateSocialPanel()
        sData = self._getSubSkillData(skType, subSkId)
        soundId = sData.get('soundId', 0)
        if soundId > 0:
            gameglobal.rds.sound.stopSound(soundId)

    def onUseLifeSkillFailed(self, skillId, subSkId):
        gamelog.debug('@hjx lifeSkill#onUseLifeSkillFailed:', skillId, subSkId)
        skType = self._getLifeSkillType(skillId)
        if skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
            self.resetManu()
            gameglobal.rds.ui.lifeSkillNew.refreshPanel(gametypes.MANUFACTURE_STAGE_FAILED)

    def onLifeSkillEvent(self, gbId, eventType, eventData):
        gamelog.debug('zt: onLifeSkillEvent', gbId, eventType, eventData)
        if (eventType, eventData) in LSEND.data:
            gameglobal.rds.ui.dynamicResult.showResult(eventType, eventData)
        if eventType in (gametypes.GAME_EVENT_GET_BONUS, gametypes.GAME_EVENT_PICK_ITEM, gametypes.GAME_EVENT_PICK_TREASUREBOX_ITEM):
            gameglobal.rds.ui.showSpecialCurve([eventData])

    def onBuyFromMarket(self, errcode, mid, iid, count, adjustedPirce):
        gamelog.info('jjh@market onBuyFromMarket ', errcode, mid, iid, count, adjustedPirce)
        if not errcode:
            gameglobal.rds.ui.resourceMarket.onBuyFromMarket(mid, iid, count, adjustedPirce)
            return
        if errcode == const.MARKET_ERROR_CODE_COUNT_NOT_ENOUGH:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_179)
        elif errcode == const.MARKET_ERROR_CODE_PRICE_OVER_FLOW:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_181)
        elif errcode == const.MARKET_ERROR_CODE_MAX_TURN_OVER:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_183)
        elif errcode == const.MARKET_ERROR_CODE_PRICE_MISMATCH:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_185)

    def onSellToMarket(self, errcode, mid, iid, count, price):
        gamelog.info('jjh@market onSellToMarket ', errcode, mid, iid, count, price)
        if not errcode:
            gameglobal.rds.ui.resourceMarket.onSellToMarket(mid, iid, count, price)
            return
        if errcode == const.MARKET_ERROR_CODE_COUNT_NOT_ENOUGH:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_196)
        elif errcode == const.MARKET_ERROR_CODE_PRICE_OVER_FLOW:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_198)
        elif errcode == const.MARKET_ERROR_CODE_MAX_TURN_OVER:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_200)
        elif errcode == const.MARKET_ERROR_CODE_PRICE_MISMATCH:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPLIFESKILL_202)

    def onQueryMarketInfo(self, mid, marketInfo, timeStamp):
        gamelog.info('@hjx market#onQueryMarketInfo:', mid, marketInfo, timeStamp)
        gameglobal.rds.ui.resourceMarket.refreshResourceMarket(mid, marketInfo, timeStamp)

    def set_usedTanSuo(self, old, new, part = None):
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def set_usedWeiWang(self, old, new, part = None):
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()
