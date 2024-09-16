#Embedded file name: /WORKSPACE/data/entities/common/fbstatistics.o
import copy
import time
import BigWorld
import const
import gamelog
from userSoleType import UserSoleType
from userDictType import UserDictType
from sMath import distance3D
if BigWorld.component in ('cell', 'base'):
    from data import fb_eval_score_data as FESD
    import gameconfig
if BigWorld.component in ('client',):
    import gameglobal

class StatsDict(UserDictType):

    def _lateReload(self):
        super(StatsDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class FubenStats(UserSoleType):
    K_MAX_DPS = 1
    K_BOSS_KILLED_DURATION = 2
    K_DAMAGE = 3
    K_OFFLINE_CNT = 4
    K_CURE = 5
    K_DEATH_CNT = 7
    K_KILL_MONSTER_CNT = 8
    K_ACHIVEMENTS = 9
    K_SPECIAL = 10
    K_HIDDEN_STAGE = 11
    K_BEDAMAGE = 12
    K_KILL_AVATAR_CNT = 13
    K_MONSTER_FIRST_COMBAT_TIME = 14
    K_TOTAL_MONSTER_CNT = 15
    K_MONSTER_KILLED_TIME = 16
    K_BEKILLED_DURATION = 17
    K_PERIOD_SPILLAGE = 18
    K_TOTAL_SPILLAGE = 19
    K_DPS = 21
    K_BOSS_CNT = 23
    K_CONQUER_FB_DURATION = 24
    K_FB_COMP = 25
    K_DODGE = 26
    K_ASSIST_CNT = 27
    K_COMBO_KILL = 28
    K_USE_SKILL = 29
    K_MAX_COMBO_KILL = 30
    K_ENTER_TIME = 31
    K_LEAVE_TIME = 32
    K_KILL_MONSTERS = 33
    K_POTION_CURE = 34
    K_DMG_TO_BOSS = 35
    K_MONSTER_ENTER_COMBAT_TIME = 36
    K_MONSTER_LEAVE_COMBAT_TIME = 37
    K_BOSS_COMBAT_CNT = 38
    K_RELIVE_HERE_CNT = 39
    K_RELIVE_NEAR_CNT = 40
    K_RELIVE_BY_SKILL_CNT = 41
    K_AVATAR_ENTER_COMBAT_TIME = 42
    K_AVATAR_COMBAT_TIME = 43
    K_AVATAR_LEAVE_COMBAT_TIME = 44
    K_BOSS_COMBAT_DPS = 45
    K_FB_START_TIME = 46
    K_FB_SCORE = 47
    K_SKILL_DAMAGE = 48
    K_SKILL_HIT_COUNT = 49
    K_SKILL_BEDAMAGE = 50
    K_SKILL_CURE = 51
    K_SKILL_DPS = 52
    K_BOSS_COMBAT_SKILL_DPS = 53
    K_SKILL_BEHIT_COUNT = 54
    K_BOSS_COMBAT_TIME = 55
    K_BOSS_HATE = 56
    K_CLAN_WAR_BUILDING_CNT = 57
    K_CLAN_WAR_FORT_CNT = 58
    K_CLAN_WAR_DESTROY_BUILDING = 59
    K_CLAN_WAR_DESTROY_FORT = 60
    K_CLAN_WAR_OCCUPY_BUILDING = 61
    K_CLAN_WAR_OCCUPY_FORT = 62
    K_LAST_POS = 63
    K_CURRENT_POS = 64
    K_DISTANCE_SUM = 65
    K_DISTANCE_LAST_SUM = 66
    K_MONSTER_TOTAL_COMBAT_TIME = 67
    K_GROUP_GUIDES = 68
    K_CURRENT_EFFECTIVE_KILL = 69
    K_BOSS_CURRENT_SHISHENMODE = 70
    K_FB_OBSERVE = 71
    k_SHAXING_FB_RESULT = 72
    K_SHAXING_FB_MONSTER_LIFE = 73
    K_FB_SPACE_READY_TIME = 74
    K_FB_TRIGGER_PROGRESS_TIME = 75
    K_FB_BOSS_LIST = 76
    K_FB_CHICKEN_MEAL_FOOD_INFO = 77
    K_BF_DOTA_COMBAT_WITH_AVATAR_TIME = 78
    K_BF_DAMAGE_WITH_AVATAR = 79
    K_BF_BE_DAMAGE_WITH_AVATAR = 80
    K_BF_DOTA_DAMAGE_WITH_TOWER = 81
    K_COMBO_JIBAI = 82
    K_MAX_COMBO_JIBAI = 83
    K_JIBAI = 84
    K_LEGENDARY = 85
    K_BF_DAMAGE_WITH_MONSTER = 86
    K_BF_FORT_ENTER_FLY = 87
    K_BF_FORT_DAMAGE_WITH_FLY = 88
    K_BF_FORT_KILL_FLY = 89
    K_BF_RES_ENTER_SPECIAL_ZAIJU = 90
    K_BF_FIGHT_IN_TRAP_TIME = 91
    K_BF_FORT_DAMAGE_BETWEEN_FLY = 92
    K_BF_FORT_DAMAGE_BOSS_WITH_FLY = 93
    K_BF_RES_DAMAGE_WITH_SPECIAL_ZAIJU = 94
    K_BF_DOTA_COMBO_KILL = 95
    K_BF_DOTA_ACCUMULATE_KILL = 96
    K_BF_DOTA_MAX_COMBO_KILL = 97
    k_ENDLESS_FLOOR = 98
    K_ENDLESS_MAP_CONFIG_ID = 99
    K_ENDLESS_PROGRESS_FULL_TIME = 100
    K_ENDLESS_PROGRESS_POINT = 101
    K_BOSS_AFFIX = 102
    K_ENDLESS_WEEKLY_INTERVAL = 103
    K_ENDLESS_SPACE_FROM = 104
    K_ENDLESS_POSITION_FROM = 105
    K_ENDLESS_AFFIX_INFO = 106
    K_ENDLESS_BUFF_TOWER_INFO = 107
    K_ENDLESS_FINISH_FB_USE_TIME = 108
    K_RELIVE_PLAYER_CNT = 109
    K_SPRITE_DAMAGE = 110
    K_SPRITE_HEAL = 111
    K_SPRITE_BE_DAMAGE = 112
    K_SPRITE_DIE_NUM = 113
    K_SPRITE_KILL_MONSTER = 114
    K_SPRITE_DPS = 115
    K_SPRITE_MAX_DPS = 116
    K_SPRITE_ENTER_COMBAT_TIME = 117
    K_SPRITE_LEAVE_COMBAT_TIME = 118
    K_SPRITE_COMBAT_TIME = 119
    K_SPRITE_KILL_AVATAR_CNT = 120
    K_SPRITE_DIE_REASON = 121
    K_SPRITE_KILLER_SCHOOL_OR_SPRITEID = 122
    K_SPRITE_CURRENT_COMBAT_INFO = 123
    K_SPRITE_BOSS_COMBAT_DPS = 124
    K_SPRITE_SKILL_DAMAGE = 125
    K_SPRITE_SKILL_HIT_COUNT = 126
    K_SPRITE_SKILL_BEDAMAGE = 127
    K_SPRITE_SKILL_HEAL = 128
    K_SPRITE_SKILL_DPS = 129
    K_SPRITE_BOSS_COMBAT_SKILL_DPS = 130
    K_SPRITE_SKILL_BEHIT_COUNT = 131
    K_SKY_WING_DAMAGE_IN_LAST_BLOOD_STAGE = 132
    K_SPRITE_SKY_WING_DAMAGE_IN_LAST_BLOOD_STAGE = 133
    K_BF_DOTA_COMBO_DEATH_CNT = 134
    K_CLAN_WAR_FAME = 135
    K_COMBO_KILL_OR_ASSIT_CNT = 136
    K_KEEP_FOR_EXTRA_DATA = 137
    K_CLAN_WAR_GUILD_RECORD = 138
    K_RELIVE_ALL_CNT = 139
    K_RELIVE_DICT = 140
    K_CLAN_WAR_DEATH_CNT = 141
    K_TEAM_ENDLESS_FLOOR = 142
    K_TEAM_ENDLESS_COST_TIME = 143
    K_TEAM_ENDLESS_AFFIX = 144
    K_CLAN_WAR_VALID_ASSIST_CNT = 145
    K_SPRITE_CHALLENGE_FINISH_FB_USE_TIME = 146
    K_SPRITE_DIE_TIME = 147
    K_SPRITE_RECORD_IN_CHALLENGE = frozenset([K_SPRITE_DAMAGE,
     K_SPRITE_BE_DAMAGE,
     K_SPRITE_HEAL,
     K_SPRITE_DIE_TIME,
     K_SPRITE_ENTER_COMBAT_TIME])
    RECORD_TYPE_ADD = 1
    RECORD_TYPE_SET = 2
    RECORD_TYPE_APPEND = 3
    RECORD_TYPE_UPDATE = 4
    RECORD_TYPE_ADD_DICT = 5
    RECORD_TYPE_APPEND_CMP_LAST = 6
    statsConfig = {K_COMBO_JIBAI: (0, RECORD_TYPE_ADD),
     K_MAX_COMBO_JIBAI: (0, RECORD_TYPE_SET),
     K_JIBAI: (0, RECORD_TYPE_ADD),
     K_BF_DOTA_MAX_COMBO_KILL: (0, RECORD_TYPE_SET),
     K_LEGENDARY: (0, RECORD_TYPE_SET),
     K_BF_DAMAGE_WITH_MONSTER: (0, RECORD_TYPE_ADD),
     K_BF_FORT_ENTER_FLY: (0, RECORD_TYPE_ADD),
     K_BF_FORT_DAMAGE_WITH_FLY: (0, RECORD_TYPE_ADD),
     K_BF_FORT_KILL_FLY: (0, RECORD_TYPE_ADD),
     K_BF_RES_ENTER_SPECIAL_ZAIJU: (0, RECORD_TYPE_ADD),
     K_BF_FIGHT_IN_TRAP_TIME: (0, RECORD_TYPE_ADD),
     K_BF_FORT_DAMAGE_BETWEEN_FLY: (0, RECORD_TYPE_ADD),
     K_BF_FORT_DAMAGE_BOSS_WITH_FLY: (0, RECORD_TYPE_ADD),
     K_BF_RES_DAMAGE_WITH_SPECIAL_ZAIJU: (0, RECORD_TYPE_ADD),
     K_DAMAGE: (0, RECORD_TYPE_ADD),
     K_BEDAMAGE: (0, RECORD_TYPE_ADD),
     K_OFFLINE_CNT: (0, RECORD_TYPE_ADD),
     K_CURE: (0, RECORD_TYPE_ADD),
     K_DEATH_CNT: (0, RECORD_TYPE_ADD),
     K_KILL_MONSTER_CNT: (0, RECORD_TYPE_ADD),
     K_MAX_DPS: (0, RECORD_TYPE_SET),
     K_KILL_AVATAR_CNT: (0, RECORD_TYPE_ADD),
     K_PERIOD_SPILLAGE: (0, RECORD_TYPE_ADD),
     K_TOTAL_SPILLAGE: (0, RECORD_TYPE_ADD),
     K_TOTAL_MONSTER_CNT: (0, RECORD_TYPE_ADD),
     K_BOSS_CNT: (0, RECORD_TYPE_ADD),
     K_BEKILLED_DURATION: (0, RECORD_TYPE_SET),
     K_MONSTER_FIRST_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_MONSTER_KILLED_TIME: (0, RECORD_TYPE_SET),
     K_DPS: (0, RECORD_TYPE_SET),
     K_CONQUER_FB_DURATION: (0, RECORD_TYPE_SET),
     K_FB_COMP: (0, RECORD_TYPE_SET),
     K_DODGE: (0, RECORD_TYPE_SET),
     K_DMG_TO_BOSS: (0, RECORD_TYPE_ADD),
     K_BOSS_KILLED_DURATION: ([], RECORD_TYPE_APPEND),
     K_ACHIVEMENTS: ([], RECORD_TYPE_APPEND),
     K_SPECIAL: ([], RECORD_TYPE_APPEND),
     K_HIDDEN_STAGE: ([], RECORD_TYPE_APPEND),
     K_ASSIST_CNT: (0, RECORD_TYPE_ADD),
     K_USE_SKILL: ({}, RECORD_TYPE_ADD_DICT),
     K_COMBO_KILL: (0, RECORD_TYPE_ADD),
     K_MAX_COMBO_KILL: (0, RECORD_TYPE_SET),
     K_ENTER_TIME: (0, RECORD_TYPE_SET),
     K_LEAVE_TIME: (0, RECORD_TYPE_SET),
     K_KILL_MONSTERS: ({}, RECORD_TYPE_ADD_DICT),
     K_POTION_CURE: (0, RECORD_TYPE_ADD),
     K_MONSTER_ENTER_COMBAT_TIME: ({}, RECORD_TYPE_UPDATE),
     K_MONSTER_LEAVE_COMBAT_TIME: ({}, RECORD_TYPE_UPDATE),
     K_BOSS_COMBAT_CNT: ({}, RECORD_TYPE_ADD_DICT),
     K_RELIVE_HERE_CNT: (0, RECORD_TYPE_ADD),
     K_RELIVE_NEAR_CNT: (0, RECORD_TYPE_ADD),
     K_RELIVE_BY_SKILL_CNT: (0, RECORD_TYPE_ADD),
     K_AVATAR_ENTER_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_AVATAR_COMBAT_TIME: (0, RECORD_TYPE_ADD),
     K_AVATAR_LEAVE_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_BOSS_COMBAT_DPS: (0, RECORD_TYPE_SET),
     K_FB_START_TIME: (0, RECORD_TYPE_SET),
     K_FB_SCORE: (0, RECORD_TYPE_SET),
     K_SKILL_DAMAGE: ({}, RECORD_TYPE_ADD_DICT),
     K_SKILL_HIT_COUNT: ({}, RECORD_TYPE_ADD_DICT),
     K_SKILL_BEDAMAGE: ({}, RECORD_TYPE_ADD_DICT),
     K_SKILL_CURE: ({}, RECORD_TYPE_ADD_DICT),
     K_SKILL_DPS: ({}, RECORD_TYPE_UPDATE),
     K_BOSS_COMBAT_SKILL_DPS: ({}, RECORD_TYPE_UPDATE),
     K_SKILL_BEHIT_COUNT: ({}, RECORD_TYPE_ADD_DICT),
     K_BOSS_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_BOSS_HATE: ({}, RECORD_TYPE_ADD_DICT),
     K_CLAN_WAR_BUILDING_CNT: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_FORT_CNT: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_DESTROY_BUILDING: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_DESTROY_FORT: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_OCCUPY_BUILDING: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_OCCUPY_FORT: (0, RECORD_TYPE_ADD),
     K_LAST_POS: (0, RECORD_TYPE_SET),
     K_CURRENT_POS: (0, RECORD_TYPE_SET),
     K_DISTANCE_SUM: (0, RECORD_TYPE_ADD),
     K_DISTANCE_LAST_SUM: (0, RECORD_TYPE_SET),
     K_MONSTER_TOTAL_COMBAT_TIME: ({}, RECORD_TYPE_ADD_DICT),
     K_CURRENT_EFFECTIVE_KILL: ({}, RECORD_TYPE_UPDATE),
     K_GROUP_GUIDES: ([], RECORD_TYPE_SET),
     K_BOSS_CURRENT_SHISHENMODE: (0, RECORD_TYPE_SET),
     K_FB_OBSERVE: ([], RECORD_TYPE_APPEND),
     k_SHAXING_FB_RESULT: (2, RECORD_TYPE_SET),
     K_SHAXING_FB_MONSTER_LIFE: ([], RECORD_TYPE_APPEND),
     K_FB_SPACE_READY_TIME: (0, RECORD_TYPE_SET),
     K_FB_TRIGGER_PROGRESS_TIME: (0, RECORD_TYPE_SET),
     K_FB_BOSS_LIST: ([], RECORD_TYPE_APPEND),
     K_BF_DOTA_COMBAT_WITH_AVATAR_TIME: (0, RECORD_TYPE_ADD),
     K_BF_DAMAGE_WITH_AVATAR: (0, RECORD_TYPE_ADD),
     K_BF_BE_DAMAGE_WITH_AVATAR: (0, RECORD_TYPE_ADD),
     K_BF_DOTA_DAMAGE_WITH_TOWER: (0, RECORD_TYPE_ADD),
     K_FB_CHICKEN_MEAL_FOOD_INFO: ([], RECORD_TYPE_APPEND),
     K_BF_DOTA_COMBO_KILL: (0, RECORD_TYPE_SET),
     K_BF_DOTA_ACCUMULATE_KILL: (0, RECORD_TYPE_SET),
     k_ENDLESS_FLOOR: (0, RECORD_TYPE_SET),
     K_ENDLESS_MAP_CONFIG_ID: (0, RECORD_TYPE_SET),
     K_ENDLESS_PROGRESS_FULL_TIME: (0, RECORD_TYPE_SET),
     K_ENDLESS_PROGRESS_POINT: (0, RECORD_TYPE_SET),
     K_BOSS_AFFIX: ([], RECORD_TYPE_APPEND),
     K_ENDLESS_WEEKLY_INTERVAL: (0, RECORD_TYPE_SET),
     K_ENDLESS_SPACE_FROM: (0, RECORD_TYPE_SET),
     K_ENDLESS_POSITION_FROM: ([], RECORD_TYPE_SET),
     K_ENDLESS_AFFIX_INFO: ({}, RECORD_TYPE_ADD_DICT),
     K_ENDLESS_BUFF_TOWER_INFO: ({}, RECORD_TYPE_ADD_DICT),
     K_ENDLESS_FINISH_FB_USE_TIME: (0, RECORD_TYPE_SET),
     K_RELIVE_PLAYER_CNT: (0, RECORD_TYPE_ADD),
     K_TEAM_ENDLESS_FLOOR: (0, RECORD_TYPE_SET),
     K_TEAM_ENDLESS_COST_TIME: (0, RECORD_TYPE_SET),
     K_TEAM_ENDLESS_AFFIX: (0, RECORD_TYPE_SET),
     K_SPRITE_DAMAGE: (0, RECORD_TYPE_ADD),
     K_SPRITE_HEAL: (0, RECORD_TYPE_ADD),
     K_SPRITE_BE_DAMAGE: (0, RECORD_TYPE_ADD),
     K_SPRITE_DIE_NUM: (0, RECORD_TYPE_ADD),
     K_SPRITE_KILL_MONSTER: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_DPS: (0, RECORD_TYPE_SET),
     K_SPRITE_MAX_DPS: (0, RECORD_TYPE_SET),
     K_SPRITE_ENTER_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_SPRITE_LEAVE_COMBAT_TIME: (0, RECORD_TYPE_SET),
     K_SPRITE_COMBAT_TIME: (0, RECORD_TYPE_ADD),
     K_SPRITE_KILL_AVATAR_CNT: (0, RECORD_TYPE_ADD),
     K_SPRITE_DIE_REASON: ([], RECORD_TYPE_APPEND),
     K_SPRITE_KILLER_SCHOOL_OR_SPRITEID: ([], RECORD_TYPE_APPEND),
     K_SPRITE_CURRENT_COMBAT_INFO: ([], RECORD_TYPE_APPEND_CMP_LAST),
     K_SPRITE_BOSS_COMBAT_DPS: (0, RECORD_TYPE_SET),
     K_SPRITE_SKILL_DAMAGE: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_SKILL_HIT_COUNT: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_SKILL_BEDAMAGE: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_SKILL_HEAL: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_SKILL_DPS: ({}, RECORD_TYPE_UPDATE),
     K_SPRITE_BOSS_COMBAT_SKILL_DPS: ({}, RECORD_TYPE_UPDATE),
     K_SPRITE_SKILL_BEHIT_COUNT: ({}, RECORD_TYPE_ADD_DICT),
     K_SPRITE_DIE_TIME: (0, RECORD_TYPE_SET),
     K_SKY_WING_DAMAGE_IN_LAST_BLOOD_STAGE: (0, RECORD_TYPE_ADD),
     K_SPRITE_SKY_WING_DAMAGE_IN_LAST_BLOOD_STAGE: (0, RECORD_TYPE_ADD),
     K_BF_DOTA_COMBO_DEATH_CNT: (0, RECORD_TYPE_SET),
     K_CLAN_WAR_FAME: (0, RECORD_TYPE_ADD),
     K_COMBO_KILL_OR_ASSIT_CNT: (0, RECORD_TYPE_ADD),
     K_KEEP_FOR_EXTRA_DATA: ({}, RECORD_TYPE_ADD_DICT),
     K_CLAN_WAR_GUILD_RECORD: (0, RECORD_TYPE_ADD),
     K_RELIVE_ALL_CNT: (0, RECORD_TYPE_ADD),
     K_RELIVE_DICT: ({}, RECORD_TYPE_ADD_DICT),
     K_CLAN_WAR_DEATH_CNT: (0, RECORD_TYPE_ADD),
     K_CLAN_WAR_VALID_ASSIST_CNT: (0, RECORD_TYPE_ADD)}

    def __init__(self, stats = {}):
        super(FubenStats, self).__init__()
        if not stats:
            self.statsDict = {}
        else:
            self.statsDict = copy.deepcopy(stats)

    def reset(self, exlude = ()):
        if not exlude:
            self.statsDict.clear()
            return
        needRm = []
        for key in self.statsDict.keys():
            if key not in exlude:
                needRm.append(key)

        [ self.statsDict.pop(k) for k in needRm ]

    def delStats(self, key):
        self.statsDict.pop(key, None)

    def getStats(self, key):
        if self.statsDict.has_key(key):
            return self.statsDict[key]
        return copy.copy(self.statsConfig[key][0])

    def record(self, key, val, recordType = 0, fbNo = 0):
        default, rType = self.statsConfig[key]
        recordType = recordType if recordType else rType
        if not self.statsDict.has_key(key):
            self.statsDict[key] = copy.copy(default)
        if recordType == self.RECORD_TYPE_ADD:
            self.statsDict[key] = self.statsDict.get(key) + val
        elif recordType == self.RECORD_TYPE_SET:
            self.statsDict[key] = val
        elif recordType == self.RECORD_TYPE_APPEND:
            if hasattr(self.statsDict[key], 'append'):
                self.statsDict[key].append(val)
        elif recordType == self.RECORD_TYPE_UPDATE:
            if hasattr(self.statsDict[key], 'update'):
                self.statsDict[key].update(val)
        elif recordType == self.RECORD_TYPE_ADD_DICT:
            for k, v in val.iteritems():
                self.statsDict[key][k] = self.statsDict[key].get(k, 0) + v

        elif recordType == self.RECORD_TYPE_APPEND_CMP_LAST:
            if hasattr(self.statsDict[key], 'append'):
                if not self.statsDict[key]:
                    self.statsDict[key].append(val)
                else:
                    lastVal = self.statsDict[key][-1]
                    if lastVal != val:
                        self.statsDict[key].append(val)
        self._onRecord(key, val, recordType, fbNo)
        return self

    def isEmpty(self):
        return len(self.statsDict) == 0

    def calcDPS(self, statsAtReset = None):
        statsAtReset = statsAtReset or FubenStats()
        dmg = (self.getStats(self.K_DAMAGE) - statsAtReset.getStats(self.K_DAMAGE)) * 1.0
        enterCombatTime = self.getStats(self.K_AVATAR_ENTER_COMBAT_TIME)
        leaveCombatTime = self.getStats(self.K_AVATAR_LEAVE_COMBAT_TIME)
        combatTimeAtReset = statsAtReset.getStats(self.K_AVATAR_COMBAT_TIME)
        if enterCombatTime <= leaveCombatTime:
            combatTime = self.getStats(self.K_AVATAR_COMBAT_TIME) - combatTimeAtReset
        else:
            combatTime = self.getStats(self.K_AVATAR_COMBAT_TIME) + time.time() - enterCombatTime - combatTimeAtReset
        resultStats = FubenStats()
        dps = int(dmg / combatTime if combatTime > 0 else 0)
        for skillId, skillDmg in self.getStats(self.K_SKILL_DAMAGE).iteritems():
            skillDmgAtReset = statsAtReset.getStats(self.K_SKILL_DAMAGE).get(skillId, 0)
            skillDps = int((skillDmg - skillDmgAtReset) / combatTime if combatTime > 0 else 0)
            resultStats.record(self.K_SKILL_DPS, {skillId: skillDps})

        resultStats.record(self.K_DPS, dps)
        maxDps = self.getStats(self.K_MAX_DPS)
        if dps > maxDps:
            resultStats.record(self.K_MAX_DPS, dps)
        if BigWorld.component in ('cell', 'base') and gameconfig.enableSpriteCombatStats() or BigWorld.component in ('client',) and gameglobal.rds.configData.get('enableSpriteCombatStats', False):
            spriteDmg = (self.getStats(self.K_SPRITE_DAMAGE) - statsAtReset.getStats(self.K_SPRITE_DAMAGE)) * 1.0
            spriteEnterCombatTime = self.getStats(self.K_SPRITE_ENTER_COMBAT_TIME)
            spriteLeaveCombatTime = self.getStats(self.K_SPRITE_LEAVE_COMBAT_TIME)
            spriteCombatTimeAtReset = statsAtReset.getStats(self.K_SPRITE_COMBAT_TIME)
            if spriteEnterCombatTime <= spriteLeaveCombatTime:
                spriteCombatTime = self.getStats(self.K_SPRITE_COMBAT_TIME) - spriteCombatTimeAtReset
            else:
                spriteCombatTime = self.getStats(self.K_SPRITE_COMBAT_TIME) + time.time() - spriteEnterCombatTime - spriteCombatTimeAtReset
            spriteDps = int(spriteDmg / spriteCombatTime if spriteCombatTime > 0 else 0)
            for skillId, skillDmg in self.getStats(self.K_SPRITE_SKILL_DAMAGE).iteritems():
                skillDmgAtReset = statsAtReset.getStats(self.K_SPRITE_SKILL_DAMAGE).get(skillId, 0)
                skillDps = int((skillDmg - skillDmgAtReset) / spriteCombatTime if spriteCombatTime > 0 else 0)
                resultStats.record(self.K_SPRITE_SKILL_DPS, {skillId: skillDps})

            resultStats.record(self.K_SPRITE_DPS, spriteDps)
            spriteMaxDps = self.getStats(self.K_SPRITE_MAX_DPS)
            if spriteDps > spriteMaxDps:
                resultStats.record(self.K_SPRITE_MAX_DPS, spriteDps)
        return resultStats

    def _onRecord(self, key, val, recordType, fbNo):
        if key == self.K_DAMAGE:
            self.record(self.K_PERIOD_SPILLAGE, val)
            if getattr(self, 'lastRecordTime', 0) == 0:
                self.lastRecordTime = time.time()
            if getattr(self, 'lastDpsTime', 0) == 0:
                self.lastDpsTime = time.time()
            if time.time() - self.lastRecordTime >= const.DAMAGE_RECORD_PERIOD and BigWorld.component in ('cell', 'base'):
                standardVal = 0
                scoreData = FESD.data.get(fbNo, [])
                for sd in scoreData:
                    if sd.get('type', 0) == const.FB_EVAL_TYPE_ATTACK and sd.get('subType', 0) == const.ST_SPILLAGE:
                        standardVal = sd.get('numdep', 0)

                periodSpillage = self.getStats(self.K_PERIOD_SPILLAGE)
                if periodSpillage > standardVal:
                    self.record(self.K_TOTAL_SPILLAGE, periodSpillage - standardVal)
                self.record(self.K_PERIOD_SPILLAGE, 0, self.RECORD_TYPE_SET)
                self.lastRecordTime = time.time()
            self.lastDpsTime = time.time()

    def specialPatch(self, key, val):
        if key == self.K_MAX_DPS:
            if val > self.getStats(key):
                self.statsDict[key] = val
            return True
        if key == self.K_PERIOD_SPILLAGE:
            self.statsDict[key] = 0
            return True
        if key == self.K_CURRENT_POS:
            lastPos = self.getStats(self.K_LAST_POS)
            if lastPos:
                dist = distance3D(lastPos, val)
                self.record(self.K_DISTANCE_SUM, dist)
            self.record(self.K_LAST_POS, val)
            return True
        if key == self.K_MONSTER_LEAVE_COMBAT_TIME:
            enterCombatTime = self.getStats(self.K_MONSTER_ENTER_COMBAT_TIME)
            for k, v in val.items():
                if not enterCombatTime.has_key(k):
                    continue
                combatTime = v - enterCombatTime[k]
                self.record(self.K_MONSTER_TOTAL_COMBAT_TIME, {k: combatTime})

            return False
        return False

    def patchStats(self, stats, exlude = ()):
        if not stats:
            return
        for key, val in stats.statsDict.iteritems():
            default, recordType = self.statsConfig[key]
            if key in exlude:
                continue
            if self.specialPatch(key, val):
                continue
            if not self.statsDict.has_key(key):
                self.statsDict[key] = copy.copy(default)
            if recordType == self.RECORD_TYPE_ADD:
                self.statsDict[key] = self.statsDict.get(key) + val
            elif recordType == self.RECORD_TYPE_SET:
                self.statsDict[key] = val
            elif recordType == self.RECORD_TYPE_APPEND:
                self.statsDict[key].extend(val)
            elif recordType == self.RECORD_TYPE_UPDATE:
                if hasattr(self.statsDict[key], 'update'):
                    self.statsDict[key].update(val)
            elif recordType == self.RECORD_TYPE_ADD_DICT:
                for k, v in val.iteritems():
                    self.statsDict[key][k] = self.statsDict[key].get(k, 0) + v

            elif recordType == self.RECORD_TYPE_APPEND_CMP_LAST:
                for eVal in val:
                    if hasattr(self.statsDict[key], 'append'):
                        if not self.statsDict[key]:
                            self.statsDict[key].append(eVal)
                        else:
                            lastVal = self.statsDict[key][-1]
                            if lastVal != eVal:
                                self.statsDict[key].append(eVal)
