#Embedded file name: /WORKSPACE/data/entities/common/item.o
import time
import math
import copy
import sys
import random
import zlib
import json
from cPickle import dumps, loads
from collections import defaultdict
from crontab import CronTab
import BigWorld
from sMath import limit
import utils
import const
import uuid
import gametypes
import commcalc
import gamelog
import commonDecorator
import gameconfigCommon
import flyUpUtils
import wingWorldUtils
from userSoleType import UserSoleType
from formula import calcFormulaById
from formula import calcValueByFormulaData
from equipment import Equipment
from formula import calcCombatScoreType
from data import item_data as ID
from data import item_disass_data as IDD
from data import prop_ref_data as PRD
from data import equip_data as ED
from cdata import font_config_data as FCD
from data import consumable_item_data as CID
from data import special_life_skill_equip_data as SLSED
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import equip_wear_repair_data as EWRD
from data import prop_data as PPD
from cdata import rune_equip_exp_data as REED
from data import equip_prefix_prop_data as EPFPD
from cdata import equip_star_feed_data as ESFD
from cdata import equip_star_lv_up_data as ESLUD
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_enhance_prop_data as EEPD
from data import rune_data as RD
from data import new_rune_data as NRD
from cdata import equip_special_props_data as ESPD
from cdata import equip_order_factor_data as EOFD
from data import fame_data as FD
from data import life_skill_data as LSD
from data import social_school_data as SSD
from data import state_data as SD
from data import equip_enhance_refining_data as EERD
from data import horsewing_data as HWD
from data import horsewing_upgrade_data as HWUD
from data import equip_gem_data as EGD
from cdata import horsewing_talent_data as HWTD
from cdata import equip_fully_repair_cost_data as EFRCD
from data import life_skill_equip_data as LSED
from cdata import equip_quality_factor_data as EQFD
from cdata import guild_donate_item_data as GDID
from cdata import item_convert_bind_map_data as ICBD
from cdata import item_parentId_data as IPD
from cdata import bind_convert_item_types_data as BCITD
from cdata import yaopei_lv_data as YLD
from cdata import yaopei_lv_exp_data as YLED
from cdata import material_dye_data as MAD
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD
from data import lottery_data as LD
from data import manual_equip_props_data as MEPD
from data import extended_equip_prop_data as XEPD
from data import manual_equip_star_prop_data as MESTARPD
from cdata import manual_equip_result_reverse_data as MERRD
from cdata import equip_suit_show_data as ESSD
from cdata import equip_suit_activation_data as ESAD
from cdata import school_transfer_prop_enhance_data as STPED
from cdata import school_transfer_prop_rand_data as STPRD
from cdata import equip_gem_score_data as EGSD
from data import composite_shop_data as CSD
from cdata import equip_gem_inverted_data as EGID
from cdata import manual_equip_base_score_coeff_data as MEBSCD
from data import equip_enhance_item_config_data as EEICD
from cdata import fly_up_config_data as FUCD
from cdata import material_dye_data as MDD
from cdata import equip_gem_desc_reverse_data as EGDRD
if BigWorld.component in ('base', 'cell'):
    from random import choice, uniform, randint, sample
    import gameengine
    import Netease
    import logconst
    import gameconfig
    import gameconst
    import serverlog
    from cdata import mail_template_def_data as MTDD
if BigWorld.component == 'client':
    import gameglobal
else:
    from data import equip_random_property_data as ERPD
    from data import equip_property_pool_data as EPPD
    from data import formula_server_data as FSD
    from data import rune_equip_data as RED
    from cdata import hiero_equip_data as HED
    from data import equip_init_starlv_data as EISD
    from data import log_src_def_data as LSDD
    from cdata import yaopei_prop_data as YPD
    from data import yaopei_extra_prop_data as YEPD
    from data import manual_equip_special_prop_data as MESPD
    from data import equip_pre_type_reverse_data as EPTRD

class Item(UserSoleType):
    """
    \xb1\xbe\xc0\xe0\xd6\xd0starExp\xba\xcd cdura\xbe\xdf\xd3\xd0\xc1\xbd\xb2\xe3\xba\xac\xd2\xe5\xa3\xba
    1. \xc6\xd5\xcd\xa8\xd7\xb0\xb1\xb8\xb5\xc4\xc8\xda\xba\xcf\xb6\xc8\xba\xcd\xc4\xcd\xbe\xc3
    2. \xd7\xf8\xc6\xef\xb3\xe1\xb0\xf2\xb5\xc4\xc8\xda\xba\xcf\xb6\xc8\xba\xcd\xb1\xa5\xca\xb3\xb6\xc8(\xc4\xdc\xc1\xbf\xd6\xb5)
    
    \xd4\xda\xd0\xde\xb8\xc4\xd5\xe2\xd0\xa9\xb1\xe4\xc1\xbf\xd6\xb5\xca\xb1\xc7\xeb\xce\xf1\xb1\xd8\xc7\xf8\xb7\xd6\xca\xc7\xc6\xd5\xcd\xa8\xd7\xb0\xb1\xb8\xbb\xf2\xb3\xe1\xb0\xf2
    """
    BASETYPE_MONEY = 0
    BASETYPE_EQUIP = 1
    BASETYPE_CONSUMABLE = 2
    BASETYPE_MATERIAL = 6
    BASETYPE_RUNE_EQUIP = 8
    BASETYPE_RUNE = 9
    BASETYPE_MISC = 11
    BASETYPE_ENHANCE = 13
    BASETYPE_PACK = 14
    BASETYPE_LIFE_SKILL = 15
    BASETYPE_FUBEN = 16
    BASETYPE_LIFE_EQUIP = 17
    BASETYPE_EQUIP_GEM = 18
    BASETYPE_UNIDENTIFIED = 19
    BASETYPE_DEED = 20
    BASETYPE_UNIDENTIFIED_EQUIP = 21
    BASETYPE_FURNITURE = 22
    BASETYPE_HIEROGRAM_EQUIP = 23
    BASETYPE_HIEROGRAM_CRYSTAL = 24
    BASETYPE_PACK_EX = 25
    EQUIP_BASETYPE_WEAPON = 1
    EQUIP_BASETYPE_ARMOR = 2
    EQUIP_BASETYPE_JEWELRY = 3
    EQUIP_BASETYPE_FASHION = 4
    EQUIP_BASETYPE_FASHION_WEAPON = 5
    EQUIP_BASETYPE_ARMOR_RUBBING = 6
    EQUIP_BASETYPE_WEAPON_RUBBING = 7
    BASETYPE_FASHION = 12
    BASE_TYPE_USE_COMMON = frozenset([BASETYPE_CONSUMABLE])
    BASETYPE_ITEM_ACTION_BAR = frozenset([BASETYPE_EQUIP, BASETYPE_CONSUMABLE])
    BASETYPE_RUNES = (BASETYPE_RUNE, BASETYPE_HIEROGRAM_CRYSTAL)
    MAKE_TYPE_1 = 0
    MAKE_TYPE_2 = 1
    MAKE_TYPE_3 = 2
    SUBTYPE_2_POTION = 1
    SUBTYPE_2_RESET_ALL_ABILITY = 2
    SUBTYPE_2_SKILL_BOOK = 4
    SUBTYPE_2_ITEM_BOX = 6
    SUBTYPE_2_QUEST_MARKER = 7
    SUBTYPE_2_USE_SKILL = 8
    SUBTYPE_2_TELEPORT = 9
    SUBTYPE_2_RELIVE = 10
    SUBTYPE_2_FAME = 12
    SUBTYPE_2_QINGGONG_BOOK = 13
    SUBTYPE_2_FISHING_BAIT = 14
    SUBTYPE_2_ABILITY_BOOK = 15
    SUBTYPE_2_MIXITEM = 16
    SUBTYPE_2_ROD_ENHANCE = 17
    SUBTYPE_2_BUOY_ENHANCE = 18
    SUBTYPE_2_HOOK_ENHANCE = 19
    SUBTYPE_2_WSSKILL_ENHANCE = 20
    SUBTYPE_2_WSSKILL_ADD_SLOT = 21
    SUBTYPE_2_WSSKILL_LOSS_FREE = 22
    SUBTYPE_2_MULTI_TELEPORT = 23
    SUBTYPE_2_REWARD_TITLE = 24
    SUBTYPE_2_REWARD_POINT_RESET = 25
    SUBTYPE_2_QUEST_TRACK = 26
    SUBTYPE_2_CHAT = 27
    SUBTYPE_2_SKILL_ENHANCE = 28
    SUBTYPE_2_DYE = 29
    SUBTYPE_2_QUEST_MONSTER = 30
    SUBTYPE_2_BOSS_HISTORY = 31
    SUBTYPE_2_MODIFY_YAOLI = 32
    SUBTYPE_2_EXPLORE_SCROLL = 33
    SUBTYPE_2_QUEST_ITEM = 34
    SUBTYPE_2_RESET_PVP_TEMP_CAMP = 35
    SUBTYPE_2_GEN_MONSTER = 36
    SUBTYPE_2_CLAN_WAR_STONE = 37
    SUBTYPE_2_CLAN_WAR_RELIVE_BOARD = 38
    SUBTYPE_2_CLAN_WAR_ARROW_TOWER = 39
    SUBTYPE_2_CLAN_WAR_ANTI_AIR_TOWER = 40
    SUBTYPE_2_CLAN_WAR_GATE = 41
    SUBTYPE_2_CLAN_WAR_STONE_CORE = 42
    SUBTYPE_2_ZAIJU = 43
    SUBTYPE_2_LIFE_SKILL_BOOK = 44
    SUBTYPE_2_MONSTER_EVENT = 45
    SUBTYPE_2_MOJING = 46
    SUBTYPE_2_XIRANG = 47
    SUBTYPE_2_LIFE_SKILL_RECIPE = 48
    SUBTYPE_2_RESET_BODYTYPE = 49
    SUBTYPE_2_RESET_ROLENAME = 50
    SUBTYPE_2_RESET_AVATARCONFIG = 51
    SUBTYPE_2_GUILD_MONEY = 52
    SUBTYPE_2_CLAN_WAR_STONE_2 = 53
    SUBTYPE_2_HUAZHUANG = 54
    SUBTYPE_2_DYEBAG = 55
    SUBTYPE_2_RESET_GUILD_TELEPORT_CD = 56
    SUBTYPE_2_GUILD_MATCH = 57
    SUBTYPE_2_GUILD_MATCH_INSTANT = 58
    SUBTYPE_2_ACHIEVE_SCORE = 59
    SUBTYPE_2_AIR_SKILL_BOOK = 60
    SUBTYPE_2_AIR_PSKILL_BOOK = 61
    SUBTYPE_2_TELEPORT_ITEM = 62
    SUBTYPE_2_JUN_JIE = 63
    SUBTYPE_2_SIGN_ITEM = 64
    SUBTYPE_2_APPEARANCE_RENEWAL = 65
    SUBTYPE_2_YUE_KA = 66
    SUBTYPE_2_RESET_ONE_PROP = 67
    SUBTYPE_2_WOOD = 68
    SUBTYPE_2_RONGGUANG = 69
    SUBTYPE_2_COLOR_CARD = 70
    SUBTYPE_2_ITEM_RENEWAL = 71
    SUBTYPE_2_RESET_SKILLPOINT = 72
    SUBTYPE_2_RELIVE_CW = 73
    SUBTYPE_2_ENABLE_PROP_SCHEME = 74
    SUBTYPE_2_RESET_PROP_SCHEME = 75
    SUBTYPE_2_EQUIP_STAR_LVUP = 76
    SUBTYPE_2_FUBEN_MIDAS = 77
    SUBTYPE_2_SYSTEM = 78
    SUBTYPE_2_OCCUPY_EQUIP_GEM = 79
    SUBTYPE_2_RIDE_DURA_DECAY = 80
    SUBTYPE_2_RIDE_DURA_ADD = 81
    SUBTYPE_2_RIDE_EXP_BOOST = 82
    SUBTYPE_2_RIDE_EXP_ADD = 83
    SUBTYPE_2_JING_JIE = 84
    SUBTYPE_2_UNLOCK_MORPHER = 85
    SUBTYPE_2_RIDE_DURA_HOLD = 86
    SUBTYPE_2_RIDE_DRAG_TAIL_EFFECT = 87
    SUBTYPE_2_LIFE_SKILL_ITEM_IDENTIFY = 88
    SUBTYPE_2_QUERY_PLAYER_POSITION = 89
    SUBTYPE_2_LIFE_PROP = 90
    SUBTYPE_2_QUERY_PLAYER_POSITION_NPC = 91
    SUBTYPE_2_DO_EMOTE = 92
    SUBTYPE_2_ADD_EXP_BONUS = 93
    SUBTYPE_2_FIREWORKS = 94
    SUBTYPE_2_VP_STORAGE = 95
    SUBTYPE_2_GUILD_SPECIAL_RES = 96
    SUBTYPE_2_GUILD_MACHINE_RES = 97
    SUBTYPE_2_GUILD_FACILITY_RES = 98
    SUBTYPE_2_FAME_COLLECT = 99
    SUBTYPE_2_GUILD_OPEN_ROUND_TABLE = 100
    SUBTYPE_2_ML_WMD_SCORE = 101
    SUBTYPE_2_RESET_SEX = 102
    SUBTYPE_2_ADD_RIDE_WING_SHARE_SPEED_STATE = 103
    SUBTYPE_2_ADD_RIDE_WING_TEMP_SPEED = 104
    SUBTYPE_2_RESET_ONE_ABILITY = 105
    SUBTYPE_2_RESET_ONE_ABILITY_NODE = 106
    SUBTYPE_2_OPEN_MATERIAL_BAG = 107
    SUBTYPE_2_ADD_CHAT_WORLD_EX_TIME = 108
    SUBTYPE_2_GUILD_RESERVE_CASH = 109
    SUBTYPE_2_REVERT_SKILL_ENHANCEPOINT = 110
    SUBTYPE_2_GUILD_CONTRIB = 111
    SUBTYPE_2_GUILD_BIND_CASH = 112
    SUBTYPE_2_JUN_JIE_VAL = 113
    SUBTYPE_2_QUMO_VAL = 114
    SUBTYPE_2_REDUCE_FB_HISTORY = 115
    SUBTYPE_2_GUILD_RESIDENT_TIRED = 116
    SUBTYPE_2_STORY_EDIT = 117
    SUBTYPE_2_VIP_SERVICE = 118
    SUBTYPE_2_GUILD_BUSINESS_FIND_PATH = 119
    SUBTYPE_2_RUBBING_CLEAN = 120
    SUBTYPE_2_QUMO_DOUBLE = 121
    SUBTYPE_2_QUMO_EXP_DOUBLE = 122
    SUBTYPE_2_FAME_COLLECT_AND_EVENTS = 123
    SUBTYPE_2_EXP_XIUWEI_POOL = 124
    SUBTYPE_2_SET_LAST_PK_TIME = 125
    SUBTYPE_2_INTIMACY_ADD = 126
    SUBTYPE_2_KEJU_PUZZLE_PASS = 127
    SUBTYPE_2_ADD_BOOTH_EXTRA_EX_TIME = 128
    SUBTYPE_2_RESTORE_FASHION_PROP = 129
    SUBTYPE_2_FIREWORKS_LA_BA = 130
    SUBTYPE_2_YAOPEI_MIX_MATERIAL = 131
    SUBTYPE_2_SWITCH_FASHION = 132
    SUBTYPE_2_JUE_WEI = 133
    SUBTYPE_2_ADD_MINGPAI = 134
    SUBTYPE_2_YABIAO_ITEM = 135
    SUBTYPE_2_GUANYIN_NORMAL_SKILL_BOOK = 136
    SUBTYPE_2_GUANYIN_SUPER_SKILL_BOOK = 137
    SUBTYPE_2_QUEST_EMOTE = 138
    SUBTYPE_2_MALL_CASH = 139
    SUBTYPE_2_RAFFLE = 140
    SUBTYPE_2_LOTTERY = 141
    SUBTYPE_2_RED_PACKET = 142
    SUBTYPE_2_INTIMACY_SKILL_BOOK = 143
    SUBTYPE_2_UNLOCK_FACE_EMOTE = 144
    SUBTYPE_2_SUMMON_PET = 145
    SUBTYPE_2_GET_EFFECT_TITLE = 146
    SUBTYPE_2_INTERACTIVE_OBJECT = 147
    SUBTYPE_2_APPRENICE_VAL = 148
    SUBTYPE_2_EQUIP_IDENTIFY = 149
    SUBTYPE_2_CBT = 150
    SUBTYPE_2_MULTY_FAME = 151
    SUBTYPE_2_MALL_DISCOUNT = 152
    SUBTYPE_2_EMOTE_ENABLE = 153
    SUBTYPE_2_PRE_DEFINED_LABA = 154
    SUBTYPE_2_PRE_DEFINED_CROSS_LABA = 155
    SUBTYPE_2_ADD_EQUIP_STAR_EXP = 156
    SUBTYPE_2_ACTIVATION = 157
    SUBTYPE_2_ZHUANGSHI = 158
    SUBTYPE_2_ZHUANGSHI_CLEAN = 159
    SUBTYPE_2_YUANSHENDAN = 160
    SUBTYPE_2_NEW_AVATAR_STRAIGHT_UP = 161
    SUBTYPE_2_EQUIP_SOUL_STAR = 162
    SUBTYPE_2_SPRITE_EGG = 163
    SUBTYPE_2_SPRITE_SELLABLE_EGG = 164
    SUBTYPE_2_FUBEN_OPEN_ROUND_TABLE = 165
    SUBTYPE_2_TIHUCHA = 166
    SUBTYPE_2_XINSHOU_SEVEN_DAY = 167
    SUBTYPE_2_SIGN_CLEAN = 168
    SUBTYPE_2_QUEST_LOOP_CHAIN_GET_BACK_EXP_FREE_CNT = 169
    SUBTYPE_2_SPRITE_FOOD = 171
    SUBTYPE_2_SPRITE_TEXTBOOK = 172
    SUBTYPE_2_ENABLE_SOCIAL_EMOTE = 173
    SUBTYPE_2_BF_DOTA_ROLE = 174
    SUBTYPE_2_BF_DOTA_TALENT_SKILL = 175
    SUBTYPE_2_BF_DOTA_KING_FAME_MULTI_CARD = 176
    SUBTYPE_2_SPRITE_LEARN_UNLOCK = 177
    SUBTYPE_2_SPRITE_RERANDOM = 178
    SUBTYPE_2_SPRITE_ACCESSORY_TEMPLATE = 179
    SUBTYPE_2_PERSONAL_ZONE_SKIN = 180
    SUBTYPE_2_RANDOM_ZAIJU = 181
    SUBTYPE_2_HP_POOL = 182
    SUBTYPE_2_MP_POOL = 183
    SUBTYPE_2_SPRITE_SKIN = 184
    SUBTYPE_2_SPRITE_DUST = 185
    SUBTYPE_2_SPRITE_JUEXING_FOR_TEST = 186
    SUBTYPE_2_SPRITE_BONE = 187
    SUBTYPE_2_MARRIAGE_SUBSCRIBE = 188
    SUBTYPE_2_SPRITE_SPECIAL = 189
    SUBTYPE_2_ENGAGE = 190
    SUBTYPE_2_MARRIAGE_RED_PACKET = 191
    SUBTYPE_2_SPRITE_LUNHUI = 192
    SUBTYPE_2_CARD = 193
    SUBTYPE_2_GUILD_RED_PACKET = 194
    SUBTYPE_2_INVITE_POINT = 195
    SUBTYPE_2_RANDOM_LOTTERY = 196
    SUBTYPE_2_AVOID_DOING_ACTIVITY = 197
    SUBTYPE_2_QUIZZES_REVIVE_CARD = 198
    SUBTYPE_2_SPRITE_SET_CLEVER_AND_APTI_FOR_TEST = 199
    SUBTYPE_2_TIAN_YU_CAN_JING = 200
    SUBTYPE_2_CARD_FRAGMENT = 201
    SUBTYPE_2_GET_SELECT_ITEM = 202
    SUBTYPE_2_CARD_WASH_POINT = 203
    SUBTYPE_2_FIGHT_FOR_LOVE_FIREWORKS = 204
    SUBTYPE_2_FIGHT_FOR_LOVE_QYZH = 205
    SUBTYPE_2_TURN_OVER_CARD = 206
    SUBTYPE_2_ENABLE_SKILL_APPEARANCE = 208
    SUBTYPE_2_BALANCE_ARENA_UPLOAD_TEMP = 209
    SUBTYPE_2_QEUIP_ENHANCE_ITEM = 210
    SUBTYPE_2_CARD_SPECIAL_WASH = 211
    SUBTYPE_2_SPRITE_XIU_LIAN_ITEM = 212
    SUBTYPE_2_SPRITE_STATE = 213
    SUBTYPE_2_EQUIP_STAR_EXP = 214
    SUBTYPE_2_CHALLENGE_PASSPORT_CHARGE = 215
    SUBTYPE_2_CHALLENGE_PASSPORT_LV = 216
    SUBTYPE_2_CARD_ADD_DURATION = 217
    SUBTYPE_2_ARENA_PLAYOFFS_VOTE = 218
    SUBTYPE_2_SERVER_DONATE = 219
    SUBTYPE_2_CHALLENGE_PASSPORT_EXP = 220
    SUBTYPE_2_GET_ITEMS_REGULAR_BY_MAIL = 221
    SUBTYPE_2_START_GUILD_CONSIGN = 222
    SUBTYPE_2_FINISH_MAIN_QUEST = 223
    SUBTYPE_2_SELECT_TO_OPEN_BOX = 224
    SUBTYPE_2_PHOTO_BORDER = 225
    SUBTYPE_2_FINISH_QUESTION = 226
    SUBTYPE_2_FB_AVOID_DIE = 227
    SUBTYPE_2_GUILD_INHERIT = 228
    SUBTYPE_2_EXP_BUFF = 229
    SUBTYPE_2_OPTIONAL_BONUS = 230
    SUBTYPE_2_RANDOM_CARD_DRAW = 231
    SUBTYPE_2_AID_TITLE = 232
    SUBTYPE_2_ARENA_PLAYOFFS_AID = 233
    SUBTYPE_2_ASSASSINATION_TELEPORT = 234
    SUBTYPE_2_ASSASSINATION_KILL = 235
    SUBTYPE_2_ACT_APPEARANCE = 236
    SUBTYPE_2_ASSASSINATION_TARGET_NOTIFY = 237
    SUBTYPE_2_RANDOM_TREASURE_BAG_CONSUME = 238
    SUBTYPE_2_CARRIER_FUEL = 239
    SUBTYPE_2_PUBG_SKILL_BOOK_LEARN = 240
    SUBTYPE_2_PUBG_SKILL_BOOK_UNLOCK = 241
    SUBTYPE_2_NT_ITEM_PURCHASE = 242
    SUBTYPE_2_VT_PLANT = 243
    SUBTYPE_2_VT_SEEK_MY_TREE = 244
    SUBTYPE_2_FEED_ALL_HIEROGRAM = 245
    ITEM_SUBTYPES_CAN_USE_CROSS = frozenset([SUBTYPE_2_POTION,
     SUBTYPE_2_QUEST_ITEM,
     SUBTYPE_2_FAME,
     SUBTYPE_2_MULTY_FAME,
     SUBTYPE_2_CLAN_WAR_STONE,
     SUBTYPE_2_CLAN_WAR_RELIVE_BOARD,
     SUBTYPE_2_CLAN_WAR_ANTI_AIR_TOWER,
     SUBTYPE_2_CLAN_WAR_GATE,
     SUBTYPE_2_CLAN_WAR_STONE_CORE,
     SUBTYPE_2_ZAIJU,
     SUBTYPE_2_CLAN_WAR_STONE_2,
     SUBTYPE_2_PUBG_SKILL_BOOK_UNLOCK,
     SUBTYPE_2_PUBG_SKILL_BOOK_LEARN,
     SUBTYPE_2_USE_SKILL])
    ITEM_SUBTYPES_CAN_USE_MUILIPLE = frozenset([SUBTYPE_2_POTION,
     SUBTYPE_2_FAME,
     SUBTYPE_2_MULTY_FAME,
     SUBTYPE_2_ITEM_BOX,
     SUBTYPE_2_SPRITE_LUNHUI,
     SUBTYPE_2_GUILD_CONTRIB,
     SUBTYPE_2_CARD_FRAGMENT,
     SUBTYPE_2_CARD_WASH_POINT,
     SUBTYPE_2_SELECT_TO_OPEN_BOX,
     SUBTYPE_2_OPTIONAL_BONUS])
    SCORE_TYPE_ATTACK = 1
    SCORE_TYPE_DEFENSE = 2
    PROPERTY_CHART = {'name': '',
     'type': 0,
     'stype': 0,
     'sPrice': 0,
     'bPrice': 0,
     'mwrap': 1,
     'category': 0,
     'subcategory': 0}
    EQUIP_ARMOR_SUBTYPE_GUANYIN = 6
    EQUIP_JEWELRY_SUBTYPE_NECKLACE = 1
    EQUIP_JEWELRY_SUBTYPE_RING = 2
    EQUIP_JEWELRY_SUBTYPE_EARRING = 3
    EQUIP_JEWELRY_SUBTYPE_YAOPEI = 4
    EQUIP_FASHION_SUBTYPE_HEAD = 1
    EQUIP_FASHION_SUBTYPE_BODY = 2
    EQUIP_FASHION_SUBTYPE_HAND = 3
    EQUIP_FASHION_SUBTYPE_LEG = 4
    EQUIP_FASHION_SUBTYPE_SHOE = 5
    EQUIP_FASHION_SUBTYPE_NEIYI = 15
    EQUIP_FASHION_SUBTYPE_NEIKU = 16
    EQUIP_FASHION_SUBTYPE_CAPE = 17
    EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE = 6
    EQUIP_FASHION_SUBTYPE_FACEWEAR = 7
    EQUIP_FASHION_SUBTYPE_WAISTWEAR = 8
    EQUIP_FASHION_SUBTYPE_BACKWEAR = 9
    EQUIP_FASHION_SUBTYPE_TAILWEAR = 10
    EQUIP_FASHION_SUBTYPE_CHESTWEAR = 11
    EQUIP_FASHION_SUBTYPE_EARWEAR = 12
    EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT = 13
    EQUIP_FASHION_SUBTYPE_HEADWEAR_LR = 14
    EQUIP_FASHION_SUBTYPE_FOOT_DUST = 18
    EQUIP_FASHION_SUBTYPE_YUANLING = 19
    EQUIP_FASHION_WEAR = frozenset([EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE,
     EQUIP_FASHION_SUBTYPE_FACEWEAR,
     EQUIP_FASHION_SUBTYPE_WAISTWEAR,
     EQUIP_FASHION_SUBTYPE_BACKWEAR,
     EQUIP_FASHION_SUBTYPE_TAILWEAR,
     EQUIP_FASHION_SUBTYPE_CHESTWEAR,
     EQUIP_FASHION_SUBTYPE_EARWEAR,
     EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT,
     EQUIP_FASHION_SUBTYPE_HEADWEAR_LR,
     EQUIP_FASHION_SUBTYPE_YUANLING])
    CONSUME_DYE_NORMAL = 1
    CONSUME_DYE_RANDOM = 2
    CONSUME_DYE_MAGIC = 3
    CONSUME_DYE_SUPER = 4
    CONSUME_DYE_CLEAN = 5
    CONSUME_DYE_TEXTURE = 6
    CONSUME_RONGGUANG_UNKNOW = 0
    CONSUME_RONGGUANG_CLEAN = 1
    FASHION_BAG_FASHION = [EQUIP_BASETYPE_FASHION,
     EQUIP_FASHION_SUBTYPE_HEAD,
     EQUIP_FASHION_SUBTYPE_BODY,
     EQUIP_FASHION_SUBTYPE_HAND,
     EQUIP_FASHION_SUBTYPE_LEG,
     EQUIP_FASHION_SUBTYPE_SHOE,
     EQUIP_FASHION_SUBTYPE_NEIYI,
     EQUIP_FASHION_SUBTYPE_NEIKU]
    FASHION_BAG_JEWELRY = [EQUIP_BASETYPE_FASHION,
     EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE,
     EQUIP_FASHION_SUBTYPE_FACEWEAR,
     EQUIP_FASHION_SUBTYPE_EARWEAR,
     EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT,
     EQUIP_FASHION_SUBTYPE_HEADWEAR_LR,
     EQUIP_FASHION_SUBTYPE_FOOT_DUST,
     EQUIP_FASHION_SUBTYPE_YUANLING]
    FASHION_BAG_PENDANT = [EQUIP_BASETYPE_FASHION,
     EQUIP_FASHION_SUBTYPE_WAISTWEAR,
     EQUIP_FASHION_SUBTYPE_BACKWEAR,
     EQUIP_FASHION_SUBTYPE_TAILWEAR,
     EQUIP_FASHION_SUBTYPE_CHESTWEAR,
     EQUIP_FASHION_SUBTYPE_CAPE]
    FASHION_BAG_WEAPON = [EQUIP_BASETYPE_FASHION_WEAPON,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16]
    FASHION_BAG_ALL = {EQUIP_BASETYPE_FASHION: [EQUIP_FASHION_SUBTYPE_HEAD,
                              EQUIP_FASHION_SUBTYPE_BODY,
                              EQUIP_FASHION_SUBTYPE_HAND,
                              EQUIP_FASHION_SUBTYPE_LEG,
                              EQUIP_FASHION_SUBTYPE_SHOE,
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE,
                              EQUIP_FASHION_SUBTYPE_FACEWEAR,
                              EQUIP_FASHION_SUBTYPE_WAISTWEAR,
                              EQUIP_FASHION_SUBTYPE_BACKWEAR,
                              EQUIP_FASHION_SUBTYPE_TAILWEAR,
                              EQUIP_FASHION_SUBTYPE_CHESTWEAR,
                              EQUIP_FASHION_SUBTYPE_EARWEAR,
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT,
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_LR,
                              EQUIP_FASHION_SUBTYPE_NEIYI,
                              EQUIP_FASHION_SUBTYPE_NEIKU,
                              EQUIP_FASHION_SUBTYPE_FOOT_DUST,
                              EQUIP_FASHION_SUBTYPE_YUANLING,
                              EQUIP_FASHION_SUBTYPE_CAPE],
     EQUIP_BASETYPE_FASHION_WEAPON: FASHION_BAG_WEAPON[1:]}
    EQUIP_PART_TABLE = {EQUIP_BASETYPE_WEAPON: {1: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             2: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             3: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             4: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             5: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             6: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             7: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             8: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             9: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             10: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             11: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             12: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             13: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             14: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             15: (gametypes.EQU_PART_WEAPON_ZHUSHOU,),
                             16: (gametypes.EQU_PART_WEAPON_FUSHOU,),
                             51: (gametypes.EQU_PART_WEAPON_ZHUSHOU,)},
     EQUIP_BASETYPE_FASHION_WEAPON: {1: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     2: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     3: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     4: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     5: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     6: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     7: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     8: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     9: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     10: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     11: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     12: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     13: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     14: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,),
                                     15: (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU,),
                                     16: (gametypes.EQU_PART_FASHION_WEAPON_FUSHOU,)},
     EQUIP_BASETYPE_ARMOR: {1: (gametypes.EQU_PART_HEAD,),
                            2: (gametypes.EQU_PART_BODY,),
                            3: (gametypes.EQU_PART_HAND,),
                            4: (gametypes.EQU_PART_LEG,),
                            5: (gametypes.EQU_PART_SHOE,),
                            6: (gametypes.EQU_PART_CAPE,),
                            7: (gametypes.EQU_PART_RIDE,),
                            8: (gametypes.EQU_PART_WINGFLY,),
                            9: (gametypes.EQU_PART_BELT,)},
     EQUIP_BASETYPE_JEWELRY: {EQUIP_JEWELRY_SUBTYPE_NECKLACE: (gametypes.EQU_PART_NECKLACE,),
                              EQUIP_JEWELRY_SUBTYPE_RING: (gametypes.EQU_PART_RING1, gametypes.EQU_PART_RING2),
                              EQUIP_JEWELRY_SUBTYPE_EARRING: (gametypes.EQU_PART_EARRING1, gametypes.EQU_PART_EARRING2),
                              EQUIP_JEWELRY_SUBTYPE_YAOPEI: (gametypes.EQU_PART_YAOPEI,)},
     EQUIP_BASETYPE_FASHION: {EQUIP_FASHION_SUBTYPE_HEAD: (gametypes.EQU_PART_FASHION_HEAD,),
                              EQUIP_FASHION_SUBTYPE_BODY: (gametypes.EQU_PART_FASHION_BODY,),
                              EQUIP_FASHION_SUBTYPE_HAND: (gametypes.EQU_PART_FASHION_HAND,),
                              EQUIP_FASHION_SUBTYPE_LEG: (gametypes.EQU_PART_FASHION_LEG,),
                              EQUIP_FASHION_SUBTYPE_SHOE: (gametypes.EQU_PART_FASHION_SHOE,),
                              EQUIP_FASHION_SUBTYPE_CAPE: (gametypes.EQU_PART_FASHION_CAPE,),
                              EQUIP_FASHION_SUBTYPE_NEIYI: (gametypes.EQU_PART_FASHION_NEIYI,),
                              EQUIP_FASHION_SUBTYPE_NEIKU: (gametypes.EQU_PART_FASHION_NEIKU,),
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE: (gametypes.EQU_PART_HEADWEAR,),
                              EQUIP_FASHION_SUBTYPE_FACEWEAR: (gametypes.EQU_PART_FACEWEAR,),
                              EQUIP_FASHION_SUBTYPE_WAISTWEAR: (gametypes.EQU_PART_WAISTWEAR,),
                              EQUIP_FASHION_SUBTYPE_BACKWEAR: (gametypes.EQU_PART_BACKWEAR,),
                              EQUIP_FASHION_SUBTYPE_TAILWEAR: (gametypes.EQU_PART_TAILWEAR,),
                              EQUIP_FASHION_SUBTYPE_CHESTWEAR: (gametypes.EQU_PART_CHESTWEAR,),
                              EQUIP_FASHION_SUBTYPE_EARWEAR: (gametypes.EQU_PART_EARWEAR,),
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT: (gametypes.EQU_PART_HEADWEAR,),
                              EQUIP_FASHION_SUBTYPE_HEADWEAR_LR: (gametypes.EQU_PART_HEADWEAR_RIGHT, gametypes.EQU_PART_HEADWEAR_LFET),
                              EQUIP_FASHION_SUBTYPE_FOOT_DUST: (gametypes.EQU_PART_FOOT_DUST,),
                              EQUIP_FASHION_SUBTYPE_YUANLING: (gametypes.EQU_PART_YUANLING,)},
     EQUIP_BASETYPE_ARMOR_RUBBING: {1: (gametypes.EQU_PART_NONE,),
                                    2: (gametypes.EQU_PART_NONE,),
                                    3: (gametypes.EQU_PART_NONE,),
                                    4: (gametypes.EQU_PART_NONE,),
                                    5: (gametypes.EQU_PART_NONE,),
                                    6: (gametypes.EQU_PART_NONE,),
                                    7: (gametypes.EQU_PART_NONE,),
                                    8: (gametypes.EQU_PART_NONE,),
                                    9: (gametypes.EQU_PART_NONE,)},
     EQUIP_BASETYPE_WEAPON_RUBBING: {1: (gametypes.EQU_PART_NONE,),
                                     2: (gametypes.EQU_PART_NONE,),
                                     3: (gametypes.EQU_PART_NONE,),
                                     4: (gametypes.EQU_PART_NONE,),
                                     5: (gametypes.EQU_PART_NONE,),
                                     6: (gametypes.EQU_PART_NONE,),
                                     7: (gametypes.EQU_PART_NONE,),
                                     8: (gametypes.EQU_PART_NONE,),
                                     9: (gametypes.EQU_PART_NONE,),
                                     10: (gametypes.EQU_PART_NONE,),
                                     11: (gametypes.EQU_PART_NONE,),
                                     12: (gametypes.EQU_PART_NONE,),
                                     13: (gametypes.EQU_PART_NONE,),
                                     14: (gametypes.EQU_PART_NONE,),
                                     15: (gametypes.EQU_PART_NONE,),
                                     16: (gametypes.EQU_PART_NONE,)}}
    FISHING_EQUIP_PART_TABLE = {gametypes.FISHING_EQU_TYPE_ROD: gametypes.FISHING_EQUIP_ROD,
     gametypes.FISHING_EQU_TYPE_HOOK: gametypes.FISHING_EQUIP_HOOK,
     gametypes.FISHING_EQU_TYPE_BUOY: gametypes.FISHING_EQUIP_BUOY,
     SUBTYPE_2_FISHING_BAIT: gametypes.FISHING_EQUIP_BAIT}
    FISHING_EQUIP = (gametypes.FISHING_EQUIP_ROD, gametypes.FISHING_EQUIP_HOOK, gametypes.FISHING_EQUIP_BUOY)
    EQUIP_CONSIST_PROPERTIES = frozenset(['equipType', 'itemLv', 'initMaxDura'])
    EQUIP_INIT_PROPERTIES = frozenset(['quality',
     'dyeList',
     'canDye',
     'permitDualDye',
     'rongGuang',
     'canRubbing'])
    FASHION_FILTERS = {1: FASHION_BAG_FASHION,
     2: FASHION_BAG_JEWELRY,
     3: FASHION_BAG_PENDANT,
     4: FASHION_BAG_WEAPON}
    CONSUM_INIT_PROPERTIES = frozenset(['timeLimit'])
    ITEM_PROPERTY_MUTABLE = frozenset(['quality', 'bindType'])
    ITEM_PROPERTY_NO_FIX = frozenset(PROPERTY_CHART.keys()) | ITEM_PROPERTY_MUTABLE
    PROPERTY_USELESS = frozenset([])
    BASE_TYPE_FIXED = frozenset([BASETYPE_EQUIP])
    EQUIPABLE = 0
    WRONG_PLACE = 1
    WRONG_LEVEL = 2
    WRONG_SCHOOL = 3
    WRONG_SEX = 4
    WRONG_CDUR = 5
    WRONG_XIUWEI = 6
    WRONG_OUT = 7
    WRONG_FISHING_LV = 8
    WRONG_EXPLORE_LV = 9
    WRONG_XIANGYAO_EXP_LESS = 10
    WRONG_XUNBAO_EXP_LESS = 11
    WRONG_ZHUIZONG_EXP_LESS = 12
    WRONG_EXTRA_CHECK = 13
    WRONG_JINGJIE_LESS = 14
    WRONG_BODYTYPE = 15
    WRONG_AC_EXCITEMENT = 16
    WRONG_FLY_UP_LV = 17
    EQUIP_PART_INFO = {WRONG_PLACE: '部位不符',
     WRONG_LEVEL: '级别不符',
     WRONG_SCHOOL: '门派不符',
     WRONG_SEX: '性别不符',
     WRONG_CDUR: '耐久度不够',
     WRONG_XIUWEI: '修为不够',
     WRONG_OUT: '物品过期',
     WRONG_BODYTYPE: '体型不符',
     WRONG_AC_EXCITEMENT: '功能未开放',
     WRONG_FLY_UP_LV: '飞升等级不符'}
    TIMESTAMPID = 2147483647
    IDTIMESTAMP = ID.data[TIMESTAMPID]['timestamp']
    EDTIMESTAMP = ED.data[TIMESTAMPID]['timestamp']
    LEDTIMESTAMP = LSED.data[TIMESTAMPID]['timestamp']
    CIDTIMESTAMP = CID.data[TIMESTAMPID]['timestamp']
    SPLEDTIMESTAMP = SLSED.data[TIMESTAMPID]['timestamp']
    EQUIP_STAR_LV_UP_TIMESTAMP = ESLUD.data.get(TIMESTAMPID, {}).get('timestamp', 0)
    TIMESTAMP = max(IDTIMESTAMP, EDTIMESTAMP, LEDTIMESTAMP, CIDTIMESTAMP, SPLEDTIMESTAMP, EQUIP_STAR_LV_UP_TIMESTAMP)
    EQUIP_NOT_DECIDED = 0
    EQUIP_NOT_RARITY_MIRACLE = 1
    EQUIP_IS_RARITY = 2
    EQUIP_IS_MIRACLE = 3
    EQUIP_PROP_FIX_BASE = 1
    EQUIP_PROP_FIX_PREFIX = 2
    EQUIP_PROP_FIX_STARLV = 3
    EQUIP_SE_BASE = 1
    EQUIP_SE_PREFIX = 2
    EQUIP_SE_STARLV = 3
    EQUIP_SE_MANUAL = 4
    SES_PROPS_MAKER = 'maker'
    SES_PROPS_WENYINENH = 'wenYinEnh'
    GEM_SLOT_MAX_CNT = 3
    GEM_SLOT_EMPTY = 1
    GEM_SLOT_FILLED = 2
    GEM_SLOT_LOCKED = 3
    GEM_TYPE_YANG = 1
    GEM_TYPE_YIN = 2
    ITEM_WITHOUT_SES = 0
    ITEM_WITH_OWNER = 1
    ITEM_WITH_OTHERSES = 2
    ITEM_SUB_SYSTEM_PROPS_HIEROGRAM = 1
    ITEM_SUB_SYSTEM_INDEX = (ITEM_SUB_SYSTEM_PROPS_HIEROGRAM,)
    ITEM_SUB_SYSTEM_PROPS_NAME = {ITEM_SUB_SYSTEM_PROPS_HIEROGRAM: {'feedCount': 0,
                                       'baseAdd': 0,
                                       'feedAdd': 0}}
    ITEM_CATEGORY_CONSUME = 8
    ITEM_CATEGORY_MATERIAL = 7
    ITEM_SUBCATEGORY_DYE = 11
    ITEM_SUBCATEGORY_BEAUTY = 15
    ITEM_SUBCATEGORY_POLISH_MATERIAL = 3
    REFINE_MANUAL_RANDOM_PROP = 1
    REFINE_MANUAL_SPECIAL_PROP = 2
    REFINE_MANUAL_REMOVE_ITEM = 3
    REFINE_MANUAL_REFINE_CNT = 4
    REFINE_MANUAL_UNREFINE_CNT = 5
    REFINE_MANUAL_GBID_FLAG = 6
    REFINE_MANUAL_ROLENAME = 7
    REFINE_MANUAL_SPECIAL_PROP_BASE_CNT = 8
    REFINE_MANUAL_UNREFINE_SPECIAL_FLAG = 9

    @staticmethod
    def updateTimestamp():
        Item.IDTIMESTAMP = ID.data[Item.TIMESTAMPID]['timestamp']
        Item.EDTIMESTAMP = ED.data[Item.TIMESTAMPID]['timestamp']
        Item.LEDTIMESTAMP = LSED.data[Item.TIMESTAMPID]['timestamp']
        Item.CIDTIMESTAMP = CID.data[Item.TIMESTAMPID]['timestamp']
        Item.SPLEDTIMESTAMP = SLSED.data[Item.TIMESTAMPID]['timestamp']
        Item.EQUIP_STAR_LV_UP_TIMESTAMP = ESLUD.data.get(Item.TIMESTAMPID, {}).get('timestamp', 0)
        Item.TIMESTAMP = max(Item.IDTIMESTAMP, Item.EDTIMESTAMP, Item.LEDTIMESTAMP, Item.CIDTIMESTAMP, Item.SPLEDTIMESTAMP, Item.EQUIP_STAR_LV_UP_TIMESTAMP)

    @staticmethod
    def convertFilterSetToDict(userSelectList):
        selectList = []
        for selectPoint in userSelectList:
            selectList.append(Item.FASHION_FILTERS[selectPoint])

        filterDict = {}
        for list in selectList:
            equipSubType = list[1:]
            if list[0] in filterDict:
                filterDict[list[0]] += equipSubType
            else:
                filterDict[list[0]] = equipSubType

        return filterDict

    @staticmethod
    def isBindItem(itemId):
        return ID.data.get(itemId, {}).get('bindType', None) == gametypes.ITEM_BIND_TYPE_FOREVER

    def getSpecialEffectType(self):
        if not hasattr(self, 'ses') and not hasattr(self, 'ownerGbId'):
            return self.ITEM_WITHOUT_SES
        elif hasattr(self, 'ownerGbId'):
            return self.ITEM_WITH_OWNER
        else:
            return self.ITEM_WITHOUT_SES

    def dummySet(self, v):
        raise ValueError('attr can not be set')

    def dummyDel(self, v):
        raise ValueError('attr can not be del')

    def getName(self):
        try:
            name = ID.data.get(self.id, {})['name']
            return name
        except:
            return Item.PROPERTY_CHART['name']

    name = property(getName, dummySet, dummyDel, 'The name of the Item')

    def getMwrap(self):
        try:
            mwrap = ID.data.get(self.id, {})['mwrap']
            return mwrap
        except:
            return Item.PROPERTY_CHART['mwrap']

    mwrap = property(getMwrap, dummySet, dummyDel, 'The max wrap of the Item')

    def getType(self):
        try:
            tp = ID.data.get(self.id, {})['type']
            return tp
        except:
            return Item.PROPERTY_CHART['type']

    type = property(getType, dummySet, dummyDel, 'The type of the Item')

    def getStype(self):
        try:
            stp = ID.data.get(self.id, {})['stype']
            return stp
        except:
            return Item.PROPERTY_CHART['stype']

    stype = property(getStype, dummySet, dummyDel, 'The sub type of the Item')

    def isRuneHasRuneData(self):
        return self.isRuneEquip() and hasattr(self, 'runeData') and len(self.runeData) > 0

    def getSPrice(self):
        try:
            pr = ID.data.get(self.id, {})['sPrice']
            return pr
        except:
            return Item.PROPERTY_CHART['sPrice']

    sPrice = property(getSPrice, dummySet, dummyDel, 'The sub type of the Item')

    def getBPrice(self):
        try:
            pr = ID.data.get(self.id, {})['bPrice']
            return pr
        except:
            return Item.PROPERTY_CHART['bPrice']

    bPrice = property(getBPrice, dummySet, dummyDel, 'The sub type of the Item')

    def getCategory(self):
        try:
            pr = ID.data.get(self.id, {})['category']
            return pr
        except:
            return Item.PROPERTY_CHART['category']

    category = property(getCategory, dummySet, dummyDel, 'The category of the Item')

    def getSubcategory(self):
        try:
            pr = ID.data.get(self.id, {})['subcategory']
            return pr
        except:
            return Item.PROPERTY_CHART['subcategory']

    subcategory = property(getSubcategory, dummySet, dummyDel, 'The subcategory of the Item')

    def getDyeListFromMultiScheme(self):
        self.tryConvertToMultiDyeScheme()
        return self.dyeListScheme[self.dyeCurrIdx]

    def setDyeListViaMultiScheme(self, newDyeList):
        self.tryConvertToMultiDyeScheme()
        self.dyeListScheme[self.dyeCurrIdx] = newDyeList

    dyeList = property(getDyeListFromMultiScheme, setDyeListViaMultiScheme, dummyDel, 'dyeList getter when enable dye multi scheme')

    def getDyeMaterialsFromMultiScheme(self):
        self.tryConvertToMultiDyeScheme()
        return self.dyeMaterialsScheme[self.dyeCurrIdx]

    def setDyeMaterialsViaMultiScheme(self, newMaterials):
        self.tryConvertToMultiDyeScheme()
        self.dyeMaterialsScheme[self.dyeCurrIdx] = newMaterials

    dyeMaterials = property(getDyeMaterialsFromMultiScheme, setDyeMaterialsViaMultiScheme, dummyDel, 'dyeMaterials getter when enable dye multi scheme')

    def getPassiveUse(self):
        try:
            pr = CID.data.get(self.id, {})['passiveUse']
            return pr
        except:
            return 0

    def getPassiveUsePriority(self):
        try:
            pr = CID.data.get(self.id, {})['usePriority']
            return pr
        except:
            return 0

    def getFishingLvReq(self):
        try:
            if self.type == self.BASETYPE_LIFE_SKILL:
                part = self.whereEquipFishing()
                if part in self.FISHING_EQUIP:
                    return SLSED.data.get(self.id, {})['fishingLvReq']
            pr = CID.data.get(self.id, {})['fishingLvReq']
            return pr
        except:
            return 0

    def getMaxRange(self):
        try:
            pr = SLSED.data.get(self.id, {})['maxRange']
            return pr
        except:
            return 0

    def getControllability(self):
        try:
            pr = SLSED.data.get(self.id, {})['controllability']
            return pr
        except:
            return 0

    def getSensitivity(self):
        try:
            pr = SLSED.data.get(self.id, {})['sensitivity']
            return pr
        except:
            return 0.0

    def getHookAbility(self):
        try:
            pr = SLSED.data.get(self.id, {})['hookAbility']
            return pr
        except:
            return 0.0

    def guid(self, readable = True):
        if readable:
            return '%s-%s' % (str(self.serverId) if hasattr(self, 'serverId') else 0, str(uuid.UUID(bytes=self.uuid)))
        return self.uuid

    @property
    def addedOrder(self):
        border = ED.data.get(self.id, {}).get('order', 0)
        if not hasattr(self, 'seCache') or not self.seCache.has_key('order'):
            return border
        else:
            return int(max(0, border + self.seCache['order']))

    @property
    def order(self):
        return ED.data.get(self.id, {}).get('order', 0)

    @property
    def lvReq(self):
        bLvReq = ID.data.get(self.id, {}).get('lvReq', 0)
        if not hasattr(self, 'seCache') or not self.seCache.has_key('lvReq'):
            pass
        else:
            bLvReq = int(max(0, bLvReq + self.seCache['lvReq']))
        if self.isYaoPei():
            return bLvReq + YLD.data.get(self.getYaoPeiLv(), {}).get('lvReqUp', 0)
        else:
            return bLvReq

    @property
    def originLvReq(self):
        bLvReq = ID.data.get(self.id, {}).get('lvReq', 0)
        if self.isYaoPei():
            return bLvReq + YLD.data.get(self.getYaoPeiLv(), {}).get('lvReqUp', 0)
        else:
            return bLvReq

    @property
    def maxEnhlv(self):
        maxEhvLv = ED.data.get(self.id, {}).get('maxEnhlv', 0)
        if not hasattr(self, 'seCache') or not self.seCache.has_key('maxEnhlv'):
            return maxEhvLv
        else:
            return int(max(0, maxEhvLv + self.seCache['maxEnhlv']))

    def getMaxEnhLv(self, owner = None):
        if flyUpUtils.enableFlyUp() and owner and getattr(owner, 'flyUpLv', 0):
            maxEnhLv = ED.data.get(self.id, {}).get('maxEnhlvFlyUp', 0)
            if not maxEnhLv:
                maxEnhLv = ED.data.get(self.id, {}).get('maxEnhlv', 0)
            return getattr(self, 'seCache', {}).get('maxEnhlv', 0) + maxEnhLv
        else:
            return self.maxEnhlv

    @property
    def originMaxEnhlv(self):
        return ED.data.get(self.id, {}).get('maxEnhlv', 0)

    @property
    def realEnhlv(self):
        return min(getattr(self, 'enhLv', 0), self.maxEnhlv)

    def getRealEnhlv(self, owner = None):
        if flyUpUtils.enableFlyUp() and owner and getattr(owner, 'flyUpLv', 0):
            return min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner))
        else:
            return self.realEnhlv

    @property
    def addedStarLv(self):
        starLv = getattr(self, 'starLv', 0)
        if not hasattr(self, 'seCache') or not self.seCache.has_key('addStarLv'):
            return starLv
        else:
            return int(max(0, starLv + self.seCache['addStarLv']))

    @property
    def seExtraStarLv(self):
        extrStarLv = 0
        if hasattr(self, 'seCache') and self.seCache.has_key('addStarLv'):
            extrStarLv = self.seCache['addStarLv']
        return extrStarLv

    @property
    def originStarLv(self):
        return getattr(self, 'starLv', 0)

    @property
    def titleArgs(self):
        return getattr(self, '_titleArgs', None)

    @titleArgs.setter
    def titleArgs(self, val):
        setattr(self, '_titleArgs', val)

    @property
    def gemProps(self):
        props = []
        for gemSlot in getattr(self, 'yangSlots', ()):
            props.extend(gemSlot.gemProps)

        for gemSlot in getattr(self, 'yinSlots', ()):
            props.extend(gemSlot.gemProps)

        return props

    @property
    def virtualItem(self):
        return getattr(self, '_virtualItem', False)

    @virtualItem.setter
    def virtualItem(self, val):
        setattr(self, '_virtualItem', val)

    @property
    def subSysProps(self):
        return getattr(self, 'subSysPropsDict', {})

    @subSysProps.setter
    def subSysProps(self, val):
        setattr(self, 'subSysPropsDict', val)

    def getHieroSysProps(self, propName):
        if not self.isNewHieroCrystal():
            return 0
        return self.getSubSysProps(Item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, propName)

    def setHieroSysProps(self, propName, val):
        if not self.isNewHieroCrystal():
            gameengine.reportCritical('@xjw setHieroSysProps, not NewHieroCrystal %d, %s, %d' % (self.id, propName, val))
            return False
        return self.setSubSysProps(Item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, propName, val)

    def getSubSysProps(self, sysType, propName):
        if sysType not in Item.ITEM_SUB_SYSTEM_INDEX:
            raise AttributeError('access unknow subSysProps sysType!')
        if propName not in Item.ITEM_SUB_SYSTEM_PROPS_NAME[sysType].iterkeys():
            raise AttributeError('access unknow subSysProps propName!')
        if not self.subSysProps:
            self.subSysProps = {}
        if not self.subSysProps.has_key(sysType):
            self.subSysProps[sysType] = {}
        if self.subSysProps[sysType].has_key(propName):
            return self.subSysProps[sysType][propName]
        else:
            return Item.ITEM_SUB_SYSTEM_PROPS_NAME[sysType].get(propName)

    def setSubSysProps(self, sysType, propName, propVal):
        if sysType not in Item.ITEM_SUB_SYSTEM_INDEX:
            raise AttributeError('set unknow subSysProps sysType!')
        if propName not in Item.ITEM_SUB_SYSTEM_PROPS_NAME[sysType].iterkeys():
            raise AttributeError('set unknow subSysProps propName!')
        if not self.subSysProps:
            self.subSysProps = {}
        if not self.subSysProps.has_key(sysType):
            self.subSysProps[sysType] = {}
        self.subSysProps[sysType][propName] = propVal

    def _getGemRebalanceProps(self, owner, gemSlot, maxLv):
        if gemSlot.gem and gemSlot.state == Item.GEM_SLOT_FILLED:
            gemData = utils.getEquipGemData(gemSlot.gem.id)
            gemLv, gemType, gemSubType = gemData.get('lv'), gemData.get('type'), gemData.get('subType')
            if not gemLv or not gemType or not gemSubType:
                return []
            gemLv = min(gemLv, maxLv)
            newGemId = EGID.data.get((gemLv, gemType, gemSubType))
            newgemData = utils.getEquipGemData(newGemId)
            if newgemData:
                return newgemData.get('gemProps', [])
        return []

    def _getGemRebalancePropsWY(self, owner, gemType, gemSlot, maxLv):
        part = self.whereEquip()
        part = part[0] if isinstance(part, tuple) and len(part) >= 1 else gametypes.EQU_PART_NONE
        wySlot = owner.wenYin.getGemSlot(part, gemType, gemSlot.pos)
        if wySlot.isFilled() and gemSlot.isEmpty():
            gemData = utils.getEquipGemData(wySlot.gem.id)
            gemLv, gemType, gemSubType = gemData.get('lv'), gemData.get('type'), gemData.get('subType')
            if not gemLv or not gemType or not gemSubType:
                return []
            gemLv = min(gemLv, maxLv)
            newGemId = EGID.data.get((gemLv, gemType, gemSubType))
            newGemData = utils.getEquipGemData(newGemId)
            if not newGemData:
                return []
            if self.addedOrder >= newGemData.get('orderLimit', 0):
                return newGemData.get('gemProps', [])
            if gameconfigCommon.enableLessLvWenYin():
                lessGemId = utils.getLessLvWenYinGemId(self.addedOrder, newGemData)
                if lessGemId:
                    return EGD.data.get(lessGemId, {}).get('gemProps', [])
        return []

    def getGemProps(self, owner = None):
        if gameconfigCommon.enableSplitWenYinFromEquip():
            return self._getGemPropsWY(owner)
        else:
            return self._getGemProps(owner)

    def _getGemProps(self, owner):
        props = []
        rebalanceFlag = False
        if owner and BigWorld.component in ('base', 'cell') and gameconfig.enableRebalance() and owner.rebalancing:
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_WY, owner.rebalanceMode)
            if methodID:
                rebalanceFlag = True
                for gemSlot in getattr(self, 'yangSlots', ()):
                    props.extend(self._getGemRebalanceProps(owner, gemSlot, factor))

                for gemSlot in getattr(self, 'yinSlots', ()):
                    props.extend(self._getGemRebalanceProps(owner, gemSlot, factor))

        if not rebalanceFlag:
            for gemSlot in getattr(self, 'yangSlots', ()):
                props.extend(gemSlot.gemProps)

            for gemSlot in getattr(self, 'yinSlots', ()):
                props.extend(gemSlot.gemProps)

        return props

    def _getGemPropsWY(self, owner):
        props = []
        rebalanceFlag = False
        if owner and BigWorld.component in ('base', 'cell') and gameconfig.enableRebalance() and owner.rebalancing:
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_WY, owner.rebalanceMode)
            if methodID:
                rebalanceFlag = True
                for gemSlot in getattr(self, 'yangSlots', ()):
                    props.extend(self._getGemRebalancePropsWY(owner, Item.GEM_TYPE_YANG, gemSlot, factor))

                for gemSlot in getattr(self, 'yinSlots', ()):
                    props.extend(self._getGemRebalancePropsWY(owner, Item.GEM_TYPE_YIN, gemSlot, factor))

        if not rebalanceFlag and hasattr(owner, 'wenYin'):
            part = self.whereEquip()
            part = part[0] if isinstance(part, tuple) and len(part) >= 1 else gametypes.EQU_PART_NONE
            wySlots = owner.wenYin.getWYSlots(part)
            if wySlots:
                for equipGemSlot in getattr(self, 'yangSlots', ()):
                    wyGemSlot = wySlots.yangSlots[equipGemSlot.pos]
                    if not wyGemSlot.isFilled():
                        continue
                    if not equipGemSlot.isEmpty():
                        if not owner.charTempId:
                            gamelog.warning('xjw _getGemPropsWY, equip yangSlots not empty', owner.gbId, equipGemSlot.pos)
                            continue
                    gemData = utils.getEquipGemData(wyGemSlot.gem.id)
                    if not gemData:
                        continue
                    if gameconfigCommon.enableLessLvWenYin():
                        if self.addedOrder < gemData.get('orderLimit', 0):
                            lessGemId = utils.getLessLvWenYinGemId(self.addedOrder, gemData)
                            if lessGemId and EGD.data.has_key(lessGemId):
                                props.extend(EGD.data.get(lessGemId, {}).get('gemProps', []))
                            continue
                    elif self.addedOrder < gemData.get('orderLimit', 0):
                        continue
                    props.extend(wyGemSlot.gemProps)

                for equipGemSlot in getattr(self, 'yinSlots', ()):
                    wyGemSlot = wySlots.yinSlots[equipGemSlot.pos]
                    if not wyGemSlot.isFilled():
                        continue
                    if not equipGemSlot.isEmpty():
                        if not owner.charTempId:
                            gamelog.warning('xjw _getGemPropsWY, equip yinSlots not empty', owner.gbId, equipGemSlot.pos)
                            continue
                    gemData = utils.getEquipGemData(wyGemSlot.gem.id)
                    if not gemData:
                        continue
                    if gameconfigCommon.enableLessLvWenYin():
                        if self.addedOrder < gemData.get('orderLimit', 0):
                            lessGemId = utils.getLessLvWenYinGemId(self.addedOrder, gemData)
                            if lessGemId and EGD.data.has_key(lessGemId):
                                props.extend(EGD.data.get(lessGemId, {}).get('gemProps', []))
                            continue
                    elif self.addedOrder < gemData.get('orderLimit', 0):
                        continue
                    props.extend(wyGemSlot.gemProps)

        return props

    def isSpriteMaterial(self):
        if self.type == Item.BASETYPE_CONSUMABLE:
            spriteMaterialSet = SCD.data.get('spriteMaterialSet')
            if spriteMaterialSet and self.cstype in spriteMaterialSet:
                return True
        flag = self.intoInvFlag
        if flag:
            intoInvFlagSet = SCD.data.get('spritematerialIntoInvFlagSet')
            if intoInvFlagSet and flag in intoInvFlagSet:
                return True
        return False

    @property
    def suitId(self):
        asId = getattr(self, 'addedSuitId', None)
        if asId:
            return asId[0]
        if hasattr(self, 'fashionTransProp') and not self.hasFashionTransPropExpire():
            srcItemId = self.fashionTransProp[0]
            return ED.data.get(srcItemId, {}).get('suitId', 0)
        return ED.data.get(self.id, {}).get('suitId', 0)

    def getSkillVal(self):
        if self.isYaoPei():
            data = YLD.data.get(self.getYaoPeiLv(), {})
            skId = getattr(self, 'yaoPeiSkillId', 0)
            skLv = data.get('skillLv', 0)
            if skId == 0 or skLv <= 0:
                return None
            return (skId, skLv, getattr(self, 'skillNst', 0))
        else:
            data = ED.data.get(self.id, {})
            if not data.get('skillId'):
                return None
            return (data['skillId'], data.get('skillLv', 1), getattr(self, 'skillNst', 0))

    @property
    def intoInvFlag(self):
        return ID.data.get(self.id, {}).get('intoInvFlag', 0)

    def __init__(self, id = 0, cwrap = 1, genRandProp = True, isNew = True):
        super(Item, self).__init__()
        self.id = id
        self.cwrap = cwrap
        self.version = 0
        if id == 0:
            return
        if not ID.data.has_key(self.id):
            gamelog.error('ERROR: init non-exist item, return!!', self.id)
            return
        if isNew:
            self.uuid = utils.getUUID()
            self.uutime = utils.getNow()
            itemData = ID.data.get(self.id, {})
            if BigWorld.component in ('base', 'cell'):
                self.serverId = int(gameconfig.getHostId())
            else:
                self.serverId = 0
            for k, v in ID.data.get(self.id, {}).iteritems():
                if k in Item.ITEM_PROPERTY_MUTABLE:
                    setattr(self, k, v)
                elif k == 'commonExpireTime':
                    nextCrontabTime = CronTab(v).next(self.uutime)
                    expTime = nextCrontabTime + self.uutime if nextCrontabTime != None else self.uutime
                    self.commonExpireTime = int(expTime)

            if itemData.has_key('ttl'):
                self.expireTime = utils.getNow() + itemData['ttl']
                if itemData.get('canRenewal', 0):
                    self.ownershipPercent = itemData.get('ownership', const.ITEM_OWNERSHIP_MAX)
            if self.canRenewalCommon():
                self.commonExpireTime = const.COMMON_DEFAULT_EXPIRE_TIME
            if BigWorld.component != 'client':
                self.initEquipData(Item.EQUIP_CONSIST_PROPERTIES | Item.EQUIP_INIT_PROPERTIES, True, genRandProp)
                self.__initConsumableData(True)
                self.__initFishingEquipData(True)
                self.__initRuneData()
                self.__initRuneEquipData()
                self.__initHieroEquipData()
                self.__initExploreEquipData(True)
                self.__initConsumeDyeList()
                self.__initHieroPropData()
            else:
                self.initEquipData(Item.EQUIP_CONSIST_PROPERTIES | Item.EQUIP_INIT_PROPERTIES, True, False)
                self.__initFishingEquipData(True)
                self.__initConsumableData(False)
                self.__initShiChuanState()
            self.__initLifeEquipData(True)
            self.version = Item.TIMESTAMP
            if self.id in [gametypes.CASH_ITEM, gametypes.BIND_CASH_ITEM]:
                self.cwrap = 0
            else:
                self.cwrap = min(self.cwrap, self.mwrap)
            if itemData.has_key('freezeUseTime'):
                self.freezeUseTime = utils.getNow() + itemData['freezeUseTime'] * 60

    def setLotteryNo(self, owner):
        if BigWorld.component in ('base', 'cell') and not gameconfig.enableLottery():
            return
        itemData = ID.data.get(self.id, {})
        lotteryId = itemData.get('lotteryId')
        if not lotteryId:
            return
        if getattr(self, 'lotteryNo', None):
            return
        ld = LD.data.get(lotteryId)
        if not ld:
            return
        lotteryTime = ld.get('lotteryTime')
        if not lotteryTime:
            return
        lotteryInterval = ld.get('lotteryInterval')
        if not lotteryInterval:
            return
        now = utils.getNow()
        lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
        if now < lotteryTime - SCD.data.get('lotteryLockTime', 300):
            issueTime = lotteryTime
        else:
            issueTime = int(math.ceil(float(now - lotteryTime + SCD.data.get('lotteryLockTime', 300)) / lotteryInterval)) * lotteryInterval + lotteryTime
        lotteryEndTime = ld.get('lotteryEndTime')
        if lotteryEndTime and utils.getTimeSecondFromStr(lotteryEndTime) <= issueTime:
            return
        nuid = Netease.getNUID()
        self.lotteryNo = utils.encodeLottery(lotteryId, issueTime, nuid)
        if BigWorld.component == 'base':
            gameengine.getGlobalBase('LotteryStub').addNewLottery(lotteryId, issueTime, [nuid], owner.gbID)
        elif BigWorld.component == 'cell':
            gameengine.getGlobalBase('LotteryStub').addNewLottery(lotteryId, issueTime, [nuid], owner.gbId)

    def setSchoolTransferInfo(self, tSchool, oldSchool, tTime):
        self.schoolTransferInfo = (tSchool, oldSchool, tTime)

    def clearSchoolTransferInfo(self):
        self.schoolTransferInfo = None

    def canSchoolTransfer(self, school, tSchool):
        schReq = ID.data.get(self.id, {}).get('schReq', ())
        if schReq and school not in schReq:
            return False
        if self.isYaoPei() or self.isGuanYin():
            return False
        if self.isEquip() and not self.isFashionEquip() and not self.isWingOrRide() and not self.isForeverBind():
            return False
        transferKey = const.SCHOOL_TRANSFER_DATA_PREFIX + '%s' % tSchool
        tItemId = ED.data.get(self.id, {}).get(transferKey, None)
        if not tItemId or tItemId == self.id:
            return False
        return True

    def needPreTransferSuit(self, school, tSchool):
        addedSuit = getattr(self, 'addedSuitId', None)
        if not addedSuit:
            return
        schReq = ID.data.get(self.id, {}).get('schReq', ())
        if schReq and (school not in schReq or tSchool not in schReq):
            return False
        return True

    def getSchoolTransferId(self):
        if not self.schoolTransferInfo:
            return 0
        transferKey = const.SCHOOL_TRANSFER_DATA_PREFIX + '%s' % self.schoolTransferInfo[0]
        tId = ED.data.get(self.id, {}).get(transferKey, None)
        if tId == self.id:
            return 0
        return tId

    def getSchoolTransferBindType(self):
        if not self.schoolTransferInfo:
            return -1
        transferKey = const.SCHOOL_TRANSFER_DATA_PREFIX + '%s' % self.schoolTransferInfo[0]
        tId = ED.data.get(self.id, {}).get(transferKey, 0)
        return ID.data.get(tId, {}).get('bindType', -1)

    def _equipSchoolTransferAddedSuitId(self, res, transferKey, tItemId):
        addedSuit = getattr(self, 'addedSuitId', None)
        if addedSuit:
            addedSuitId = self.suitId
            tAddedSuitId = ESSD.data.get(addedSuitId, {}).get(transferKey, None)
            if tAddedSuitId and tAddedSuitId != addedSuitId:
                suitActivationData = ESAD.data.get(tItemId, {})
                for sad in suitActivationData:
                    if sad.get('suitId', 0) == tAddedSuitId:
                        tConsumeItemId = sad.get('itemId', 0)
                        if tConsumeItemId:
                            res.append(('addedSuitId', (tAddedSuitId, tConsumeItemId)))
                        break

    def transferAddedSuitIdPre(self, transferKey):
        addedSuit = getattr(self, 'addedSuitId', None)
        if addedSuit:
            addedSuitId = self.suitId
            tAddedSuitId = ESSD.data.get(addedSuitId, {}).get(transferKey, None)
            if tAddedSuitId and tAddedSuitId != addedSuitId:
                suitActivationData = ESAD.data.get(self.id, {})
                for sad in suitActivationData:
                    if sad.get('suitId', 0) == tAddedSuitId:
                        tConsumeItemId = sad.get('itemId', 0)
                        if tConsumeItemId:
                            self.addEquipSuit(tAddedSuitId, tConsumeItemId)
                            return True

        return False

    def _equipSchoolTransferEnhJuexingData(self, res, transferKey):
        enhJuexingData = getattr(self, 'enhJuexingData', None)
        tempJXStrength = getattr(self, 'tempJXStrength', None)
        tTempJXStrength = {}
        if enhJuexingData:
            enhLvs = enhJuexingData.keys()
            for enhLv in enhLvs:
                enhData = enhJuexingData[enhLv]
                tEnhData = []
                for propRefId, propType, val in enhData:
                    tPropRefId = STPED.data.get((self.equipType,
                     self.equipSType,
                     self.enhanceType,
                     propRefId), {}).get(transferKey, 0)
                    if tPropRefId and tPropRefId != propRefId:
                        tScore = PRD.data.get(tPropRefId, {}).get('juexingScore', None)
                        score = PRD.data.get(propRefId, {}).get('juexingScore', None)
                        if tScore and score and tScore[1] > 0:
                            tVal = float(val * score[1]) / tScore[1]
                            tEnhData.append((tPropRefId, propType, tVal))

                if tEnhData:
                    res.append(('enhJuexingData', (enhLv, tEnhData)))
                if tempJXStrength and enhLv in tempJXStrength:
                    if tEnhData:
                        tTempJXStrength[enhLv] = tEnhData
                    else:
                        tTempJXStrength[enhLv] = enhData

        if tempJXStrength:
            enhLvs = enhJuexingData.keys()
            for enhLv in enhLvs:
                if enhLv < SCD.data.get('enhJuexingStrengthEnhLvLimit', const.EQUIP_ENH_JUEXING_STRENGTH_LV_LIMIT):
                    continue
                if enhLv not in tempJXStrength:
                    continue
                enhData = tempJXStrength[enhLv]
                tEnhData = self._equipSchoolTransferJXDataCommon(enhData, transferKey)
                if tEnhData:
                    tTempJXStrength[enhLv] = tEnhData

            gamelog.debug('@hqx_enh_tempJXStrength', tTempJXStrength)
            res.append(('tempJXStrength', tTempJXStrength))

    def _equipSchoolTransferJXDataCommon(self, enhData, transferKey):
        tEnhData = []
        for propRefId, propType, val in enhData:
            tPropRefId = STPED.data.get((self.equipType,
             self.equipSType,
             self.enhanceType,
             propRefId), {}).get(transferKey, 0)
            if tPropRefId and tPropRefId != propRefId:
                tScore = PRD.data.get(tPropRefId, {}).get('juexingScore', None)
                score = PRD.data.get(propRefId, {}).get('juexingScore', None)
                if tScore and score and tScore[1] > 0:
                    tVal = float(val * score[1]) / tScore[1]
                    tEnhData.append((tPropRefId, propType, tVal))
                else:
                    tEnhData.append((propRefId, propType, val))
            else:
                tEnhData.append((propRefId, propType, val))

        return tEnhData

    def _equipSchoolTransferTempJXAlldata(self, res, transferKey):
        tempJXAlldata = getattr(self, 'tempJXAlldata', None)
        if tempJXAlldata:
            tTempJXAlldata = []
            for enhLv, enhData in tempJXAlldata:
                tEnhData = self._equipSchoolTransferJXDataCommon(enhData, transferKey)
                tTempJXAlldata.append((enhLv, tEnhData))

            res.append(('tempJXAlldata', tTempJXAlldata))

    def _equipSchoolTransferRProp(self, res, transferKey):
        rprops = getattr(self, 'rprops', None)
        transferMode = ED.data.get(self.id, {}).get('transferMode', None)
        transferModeExtra = ED.data.get(self.id, {}).get('transferModeExtra', None)
        modeIdx = ED.data.get(self.id, {}).get('transferModeExtraIdx', 0)
        if rprops and transferMode:
            trprops = []
            for idx, rprop in enumerate(rprops):
                aId, aType, val = rprop
                if transferModeExtra and idx >= modeIdx:
                    transferMode = transferModeExtra
                tAId = STPRD.data.get((self.equipType,
                 self.equipSType,
                 self.enhanceType,
                 transferMode,
                 aId), {}).get(transferKey, 0)
                if tAId and tAId != aId:
                    tScoreCoeffNum = PRD.data.get(tAId, {}).get('scoreCoeffNum', 0)
                    scoreCoeffNum = PRD.data.get(aId, {}).get('scoreCoeffNum', 0)
                    tVal = float(val * scoreCoeffNum) / tScoreCoeffNum
                    trprops.append((tAId, aType, tVal))
                else:
                    trprops.append((aId, aType, val))

            res.append(('rprops', trprops))
        rses = getattr(self, 'ses', {}).get(self.EQUIP_SE_BASE, [])
        if rses:
            tses = []
            for sEffect in rses:
                tEffect = ESPD.data.get(sEffect, {}).get(transferKey, 0)
                if tEffect and tEffect != sEffect:
                    tses.append(tEffect)
                else:
                    tses.append(sEffect)

            if not hasattr(self, 'ses'):
                self.ses = {}
            res.append(('ses', (self.EQUIP_SE_BASE, tses)))

    def _equipSchoolTransferPrefix(self, res, transferKey):
        prefixInfo = getattr(self, 'prefixInfo', None)
        if prefixInfo:
            preGroupId, prefixId = prefixInfo
            prefixData = EPFPD.data.get(preGroupId)
            if not prefixData:
                return
            data = {}
            for pd in prefixData:
                if pd['id'] == prefixId:
                    data = pd
                    break

            if not data:
                return
            tPreGroupId, tPrefixId = data.get(transferKey, (0, 0))
            if tPrefixId and tPrefixId != prefixId:
                tPrefixData = EPFPD.data.get(tPreGroupId)
                data = {}
                for pd in tPrefixData:
                    if pd['id'] == tPrefixId:
                        data = pd
                        break

                if data:
                    if data.has_key('props'):
                        preprops = []
                        for pid, pType, pVal in data['props']:
                            preprops.append((pid, pType, pVal))

                        res.append(('preprops', preprops))
                    if data.has_key('sEffect'):
                        if not hasattr(self, 'ses'):
                            self.ses = {}
                        if self.EQUIP_SE_PREFIX in self.ses:
                            res.append(('ses', (self.EQUIP_SE_PREFIX, [data['sEffect']])))
                    if data.has_key('propFix'):
                        if not hasattr(self, 'propFix'):
                            self.propFix = {}
                        if self.EQUIP_PROP_FIX_PREFIX in getattr(self, 'propFix', {}):
                            res.append(('propFix', (self.EQUIP_PROP_FIX_PREFIX, [data['propFix']])))
                    res.append(('prefixInfo', (tPreGroupId, tPrefixId)))
        newPrefixInfo = getattr(self, 'newPrefixInfo', None)
        if newPrefixInfo:
            preGroupId, prefixId, opNUID = newPrefixInfo
            prefixData = EPFPD.data.get(preGroupId)
            if not prefixData:
                return
            data = {}
            for pd in prefixData:
                if pd['id'] == prefixId:
                    data = pd
                    break

            if not data:
                return
            tPreGroupId, tPrefixId = data.get(transferKey, (0, 0))
            if tPrefixId and tPrefixId != prefixId:
                res.append(('newPrefixInfo', (tPreGroupId, tPrefixId, opNUID)))
        if getattr(self, 'preGroupList', None):
            if self.isManualEquip():
                mepd = MEPD.data.get(self.id, {})
                preGroupList = mepd.get('preGroupList', ())
            elif self.isExtendedEquip():
                xepd = XEPD.data.get(self.id, {})
                preGroupList = xepd.get('preGroupList', ())
            else:
                ed = ED.data.get(self.id, {})
                preGroupList = ed.get('preGroupList', ())
            res.append(('preGroupList', preGroupList))

    def _equipSchoolTransferProps(self, res, transferKey, tId):
        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            tProps = []
            if isManual:
                epd = MEPD.data.get(self.id, {})
                tepd = MEPD.data.get(tId, {})
                basicePropsData = self._getDataByMaketype(epd.get('basicProps', []))
                tBasicePropsData = self._getDataByMaketype(tepd.get('basicProps', []))
            else:
                epd = XEPD.data.get(self.id, {})
                tepd = XEPD.data.get(tId, {})
                basicePropsData = epd.get('basicProps', [])
                tBasicePropsData = tepd.get('basicProps', [])
            if basicePropsData and tBasicePropsData:
                basiceProps = [ ent[0] for ent in basicePropsData ]
                tBasiceProps = [ ent[0] for ent in tBasicePropsData ]
                for pid, pType, val in self.props:
                    idx = basiceProps.index(pid)
                    tPid = tBasiceProps[idx]
                    data = basicePropsData[idx]
                    tData = tBasicePropsData[idx]
                    if data[3] == data[2]:
                        tVal = tData[2]
                    else:
                        tVal = tData[2] + float(tData[3] - tData[2]) * (val - data[2]) / (data[3] - data[2])
                    tProps.append((tPid, pType, tVal))

            if hasattr(self, 'props') and tProps:
                res.append(('props', tProps))
        else:
            data = ED.data.get(tId, {})
            props = data.get('props')
            if props:
                tProps = []
                for aid, atype, aval in props:
                    tProps.append((aid, atype, aval))

                if hasattr(self, 'props') and tProps:
                    res.append(('props', tProps))

    def _equipSchoolTransferStarLv(self, res, transferKey):
        tId = ED.data.get(self.id, {}).get(transferKey, None)
        if not tId or tId == self.id:
            return
        data = {}
        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            starRandId, starEffDataId = getattr(self, 'manualEquipStarInfo', (-1, -1))
            for d in MESTARPD.data.get(starRandId, []):
                if d['id'] == starEffDataId:
                    data = d

            tStarRandId, tStarEffDataId = data.get(transferKey, (-1, -1))
            if starEffDataId == tStarEffDataId:
                return
            for d in MESTARPD.data.get(tStarRandId, []):
                if d['id'] == tStarEffDataId:
                    data = d

            if hasattr(self, 'manualEquipStarInfo'):
                res.append(('manualEquipStarInfo', (tStarRandId, tStarEffDataId)))
            tStarPropFix = data.get('propFix')
        else:
            data = ED.data.get(tId, {})
            tStarPropFix = data.get('starPropFix')
        if hasattr(self, 'propFix') and tStarPropFix and self.EQUIP_PROP_FIX_STARLV in self.propFix:
            res.append(('propFix', (self.EQUIP_PROP_FIX_STARLV, [tStarPropFix])))
        tStarSEffect = data.get('starSEffect', 0)
        if not hasattr(self, 'ses'):
            self.ses = {}
        tStarSEffect = data.get('starSEffect', 0)
        tses = []
        if tStarSEffect:
            tses = [tStarSEffect]
        if self.EQUIP_SE_STARLV in self.ses and tses:
            res.append(('ses', (self.EQUIP_SE_STARLV, tses)))

    def _equipSchoolTransferManualSes(self, res, transferKey):
        ses = getattr(self, 'ses', None)
        if ses:
            if self.EQUIP_SE_MANUAL in ses:
                rses = getattr(self, 'ses', {}).get(self.EQUIP_SE_MANUAL, [])
                if rses:
                    tses = []
                    for sEffect in rses:
                        tEffect = ESPD.data.get(sEffect, {}).get(transferKey, 0)
                        if tEffect and tEffect != sEffect:
                            tses.append(tEffect)
                        else:
                            tses.append(sEffect)

                    if not hasattr(self, 'ses'):
                        self.ses = {}
                    if self.EQUIP_SE_MANUAL in self.ses and tses:
                        res.append(('ses', (self.EQUIP_SE_MANUAL, tses)))

    def _equipSchoolTransferRawData(self, tId):
        tData = ED.data.get(tId, {})
        if tData:
            extraProps = tData.get('extraProps')
            self.extraProps = []
            if extraProps:
                for aid, atype, aval in extraProps:
                    self.extraProps.append((aid, atype, aval))

            etp = tData.get('equipType')
            if etp in (self.EQUIP_BASETYPE_WEAPON, self.EQUIP_BASETYPE_FASHION_WEAPON, self.EQUIP_BASETYPE_WEAPON_RUBBING):
                self.equipSType = tData.get('weaponSType')
            elif etp in (self.EQUIP_BASETYPE_ARMOR, self.EQUIP_BASETYPE_ARMOR_RUBBING):
                self.equipSType = tData.get('armorSType')
            elif etp == self.EQUIP_BASETYPE_JEWELRY:
                self.equipSType = tData.get('jewelSType')
            elif etp == self.EQUIP_BASETYPE_FASHION:
                self.equipSType = tData.get('fashionSType')
            else:
                raise Exception('equipment sub type not defintData. %d' % (self.id, tId))
            for k, v in tData.iteritems():
                if k in ('canRubbing', 'equipType', 'itemLv', 'unbindTimes'):
                    setattr(self, k, v)

    def _equipSchoolTransferDataClean(self):
        if getattr(self, 'rubbing', 0):
            self.rubbing = 0
        if getattr(self, 'rubbingTTLExpireTime', 0):
            self.rubbingTTLExpireTime = 0

    def _loadAllPropFromRes(self, res):
        for key, val in res:
            if key == 'addedSuitId':
                self.addEquipSuit(*val)
            elif key in ('tempJXAlldata', 'rprops', 'preprops', 'prefixInfo', 'newPrefixInfo', 'preGroupList', 'props', 'manualEquipStarInfo', 'tempJXStrength'):
                setattr(self, key, val)
            else:
                prop = getattr(self, key, None)
                if not prop:
                    prop = {}
                prop.update({val[0]: val[1]})

    def _rPropEquipSchoolTransferByGM(self, transferKey, owner):
        res = []
        rprops = getattr(self, 'rprops', None)
        transferMode = 1
        if rprops and transferMode:
            trprops = []
            if self.id in (140104, 140204, 140304, 140404, 140504, 140604):
                equipType, equipSType, enhanceType = (1, 13, 1)
            elif self.id in (141104, 141204, 141304, 141404, 141504, 141604):
                equipType, equipSType, enhanceType = (1, 14, 1)
            else:
                return False
            for aId, aType, val in rprops:
                tAId = STPRD.data.get((equipType,
                 equipSType,
                 enhanceType,
                 transferMode,
                 aId), {}).get(transferKey, 0)
                if tAId and tAId != aId:
                    tScoreCoeffNum = PRD.data.get(tAId, {}).get('scoreCoeffNum', 0)
                    scoreCoeffNum = PRD.data.get(aId, {}).get('scoreCoeffNum', 0)
                    tVal = float(val * scoreCoeffNum) / tScoreCoeffNum
                    trprops.append((tAId, aType, tVal))
                else:
                    trprops.append((aId, aType, val))

            res.append(('rprops', trprops))
        self._loadAllPropFromRes(res)
        self.refreshSeCache()
        self.refreshPropsFix()
        self.calcScores(extra={'owner': owner})
        return True

    def _equipSchoolTransferByKey(self, transferKey, tItemId, extra = None):
        res = []
        self._equipSchoolTransferAddedSuitId(res, transferKey, tItemId)
        self._equipSchoolTransferEnhJuexingData(res, transferKey)
        self._equipSchoolTransferTempJXAlldata(res, transferKey)
        self._equipSchoolTransferRProp(res, transferKey)
        self._equipSchoolTransferPrefix(res, transferKey)
        self._equipSchoolTransferProps(res, transferKey, tItemId)
        self._equipSchoolTransferStarLv(res, transferKey)
        self._equipSchoolTransferManualSes(res, transferKey)
        self._loadAllPropFromRes(res)
        self._equipSchoolTransferRawData(tItemId)
        self._equipSchoolTransferDataClean()
        self.id = tItemId
        self.refreshSeCache()
        self.refreshPropsFix()
        self.calcScores(extra=extra)

    def doEquipSchoolTransfer(self, extra = None):
        transferKey = const.SCHOOL_TRANSFER_DATA_PREFIX + '%s' % self.schoolTransferInfo[0]
        tItemId = self.getSchoolTransferId()
        if not tItemId:
            return
        if self.isFashionEquip() or self.isWingOrRide():
            self.id = tItemId
        else:
            self._equipSchoolTransferByKey(transferKey, tItemId, extra)
            if hasattr(self, 'dumpAfterIdentify'):
                it = self.getItemAfterIdentify()
                it._equipSchoolTransferByKey(transferKey, tItemId, extra)
                self.popProp('dumpAfterIdentify', None)
                self.dumpAfterIdentify = zlib.compress(dumps(utils.getItemSaveData(it)))
        self.clearSchoolTransferInfo()
        return True

    def __initFishingEquipData(self, isNew = False):
        if self.type == self.BASETYPE_LIFE_SKILL:
            part = self.whereEquipFishing()
            consumableParts = (gametypes.FISHING_EQUIP_BAIT,
             gametypes.FISHING_EQUIP_ENHANCE_ROD,
             gametypes.FISHING_EQUIP_ENHANCE_BUOY,
             gametypes.FISHING_EQUIP_ENHANCE_HOOK)
            if part in consumableParts:
                cid = CID.data.get(self.id)
                if not cid:
                    gamelog.error('data not configured in consumable equipment data!! %d' % self.id)
                    return
                self.fishingEquipType = cid.get('fishingEquipType', 1)
            elif part in self.FISHING_EQUIP:
                fed = SLSED.data.get(self.id)
                if not fed:
                    gamelog.error('data not configured in fishing equipment data!! %d' % self.id)
                    return
                if isNew:
                    self.fishingEquipType = fed.get('fishingEquipType')
                    self.initMaxDura = fed.get('mdura', 0)
                    self.mdura = self.initMaxDura
                    self.cdura = self.initMaxDura
                    self.itemLv = fed.get('fishingLvReq', 1)
                elif not hasattr(self, 'itemLv'):
                    self.initMaxDura = fed.get('mdura', 0)
                    self.mdura = self.initMaxDura
                    self.cdura = self.initMaxDura
                    self.itemLv = fed.get('fishingLvReq', 1)

    def __initExploreEquipData(self, isNew = False):
        if self.type == self.BASETYPE_LIFE_SKILL:
            part = self.whereEquipExplore()
            if part == gametypes.EXPLORE_EQUIP_COMPASS:
                eed = SLSED.data.get(self.id, {})
                if isNew:
                    self.regenTime = 0
                    self.sensePower = eed.get('sensePower', 0)
                    self.initMaxDura = eed.get('mdura', 0)
                    self.mdura = self.initMaxDura
                    self.cdura = self.initMaxDura
                    self.itemLv = eed.get('exploreLvReq', 1)
                elif not hasattr(self, 'itemLv'):
                    self.initMaxDura = eed.get('mdura', 0)
                    self.mdura = self.initMaxDura
                    self.cdura = self.initMaxDura
                    self.itemLv = eed.get('exploreLvReq', 1)
                if hasattr(self, 'initMaxDura') and self.initMaxDura > eed.get('mdura', 0) or hasattr(self, 'mdura') and self.mdura > eed.get('mdura', 0):
                    self.initMaxDura = eed.get('mdura', 0)
                    self.mdura = self.initMaxDura
        if getattr(self, 'cstype', 0) == Item.SUBTYPE_2_EXPLORE_SCROLL:
            self.exploreInfo = None

    def __initConsumableData(self, init):
        if self.type == self.BASETYPE_CONSUMABLE:
            cd = CID.data.get(self.id)
            if not cd:
                gamelog.error('data not configured in consumable data!! %d' % self.id)
                self.cstype = Item.PROPERTY_CHART['stype']
                return
            cstype = cd.get('sType')
            self.cstype = cstype
            if init:
                for t in self.CONSUM_INIT_PROPERTIES:
                    if cd.has_key(t):
                        setattr(self, t, cd.get(t))

    def initEquipData(self, properties, isNew, genRandProp = False):
        if self.type == self.BASETYPE_EQUIP:
            ed = ED.data.get(self.id)
            if not ed:
                gamelog.error('data not configured in equipment data!! %d' % self.id)
                return
            etp = ed.get('equipType')
            if etp in (self.EQUIP_BASETYPE_WEAPON, self.EQUIP_BASETYPE_FASHION_WEAPON, self.EQUIP_BASETYPE_WEAPON_RUBBING):
                self.equipSType = ed.get('weaponSType')
            elif etp in (self.EQUIP_BASETYPE_ARMOR, self.EQUIP_BASETYPE_ARMOR_RUBBING):
                self.equipSType = ed.get('armorSType')
            elif etp == self.EQUIP_BASETYPE_JEWELRY:
                self.equipSType = ed.get('jewelSType')
            elif etp == self.EQUIP_BASETYPE_FASHION:
                self.equipSType = ed.get('fashionSType')
            else:
                raise Exception('equipment sub type not defined! %d' % self.id)
            for k, v in ed.iteritems():
                if k in properties:
                    setattr(self, k, v)

            if not self.isManualEquip() and not self.isExtendedEquip():
                self.props = []
                if self.isFashionEquip() and hasattr(self, 'fashionTransProp') and not self.hasFashionTransPropExpire():
                    srcItemId, srcSuitId, expireTime = self.fashionTransProp
                    props = ED.data.get(srcItemId, {}).get('props')
                else:
                    props = ed.get('props')
                if props:
                    for aid, atype, aval in props:
                        self.props.append((aid, atype, aval))

                self.preGroupList = []
                preGroupList = ed.get('preGroupList')
                if preGroupList:
                    self.preGroupList = preGroupList
                self.extraProps = []
                extraProps = ed.get('extraProps')
                if extraProps:
                    for aid, atype, aval in extraProps:
                        self.extraProps.append((aid, atype, aval))

            self.refreshPropsFix()
            if isNew:
                self.inactiveStarLv = 0
                self.activeStarLv = 0
                self.starLv = 0
                self.maxStarLv = 0
                self.starExp = 0
                self.mdura = self.initMaxDura
                if self._checkEquipDuraValid():
                    self.cdura = self.initMaxDura
                else:
                    self.cdura = const.EQUIP_DURA_DEFAULT_VAL
                dyeMaterials = ed.get('dyeMaterials', [])
                canDye = ed.get('canDye')
                if canDye and not hasattr(self, 'dyeList') and not dyeMaterials:
                    self.resetDyeList()
                self.__initEquipGemSlots(ed)
                if self.isWingOrRide():
                    self.rideWingStage = ED.data.get(self.id, {}).get('initStage', 0)
                    self.rideWingStates = {}
                    self.talents = []
                    self.recalcWingRideTalents()
                if BigWorld.component in ('base', 'cell') and self.isGuanYin():
                    self.__initGuanYin()
            if genRandProp:
                self._randomQuality(ed)
                self.randomProperties(ed.get('randPropId'))
                preGroupId, prefixId = self.genPrefix()
                self.addPrefixProps(preGroupId, prefixId)
                self._randomInitStarLv(ed)
                if isNew and self.isExtendedEquip():
                    if not XEPD.data.has_key(self.id):
                        return
                    xepd = XEPD.data[self.id]
                    self._calcRandEquip(False, xepd)
                    self.calcScores(calcRarityMiracle=True)
                    self.popProp('dumpAfterIdentify', None)
                    self.dumpAfterIdentify = zlib.compress(dumps(utils.getItemSaveData(self)))
                else:
                    self.calcScores(calcRarityMiracle=True)
            if isNew and BigWorld.component in ('base', 'cell') and self.isYaoPei():
                self.__initYaoPei()

    def __initLifeEquipData(self, isNew = False):
        if self.type != Item.BASETYPE_LIFE_EQUIP:
            return
        if not LSED.data.has_key(self.id):
            gamelog.error('@hjx __initLifeEquipData, LSED has not item:%d' % self.id)
            return
        try:
            lData = LSED.data.get(self.id, {})
            self.subType = lData['subType']
            self.part = lData['partId']
            self.itemLv = lData['itemLv']
            if isNew:
                self.initMaxDura = lData['mdura']
                self.mdura = self.initMaxDura
                self.cdura = self.initMaxDura
        except:
            gamelog.error('@hjx __initLifeEquipData, item:%d, init failed!' % self.id)

    def __initEquipGemSlots(self, data):
        if data.has_key('yinSlots') or data.has_key('yangSlots') or data.has_key('lockedYinSlots') or data.has_key('lockedYangSlots'):
            if not hasattr(self, 'yangSlots'):
                self.yangSlots = []
            if not hasattr(self, 'yinSlots'):
                self.yinSlots = []
            for i in range(data.get('yangSlots', 0)):
                self.yangSlots.insert(0, GemSlot(self.GEM_SLOT_EMPTY))

            for i in range(data.get('lockedYangSlots', 0)):
                self.yangSlots.append(GemSlot(self.GEM_SLOT_LOCKED))

            for i in range(data.get('yinSlots', 0)):
                self.yinSlots.insert(0, GemSlot(self.GEM_SLOT_EMPTY))

            for i in range(data.get('lockedYinSlots', 0)):
                self.yinSlots.append(GemSlot(self.GEM_SLOT_LOCKED))

            for pos, sVal in enumerate(self.yangSlots):
                sVal.pos = pos

            for pos, sVal in enumerate(self.yinSlots):
                sVal.pos = pos

    def addEquipGemSlot(self, gemType, slotVal):
        if gemType == Item.GEM_TYPE_YANG:
            self.__dict__.setdefault('yangSlots', []).append(slotVal)
        elif gemType == Item.GEM_TYPE_YIN:
            self.__dict__.setdefault('yinSlots', []).append(slotVal)

    def refreshPropsFix(self):
        self.fixedProps = []
        if not hasattr(self, 'propFix') or not self.propFix:
            return
        if not self.props:
            return
        propFixCache = {}
        for fixProps in self.propFix.itervalues():
            for prop, value in fixProps:
                propFixCache.setdefault(prop, 0)
                propFixCache[prop] += value

        if not propFixCache:
            return
        for aid, atype, aval in self.props:
            if aid in propFixCache:
                self.fixedProps.append((aid, atype, aval * propFixCache[aid]))

    def getPrefixScore(self):
        prefixScore = 0
        if hasattr(self, 'prefixInfo'):
            preGroupId, prefixId = self.prefixInfo
            preGroupData = EPFPD.data.get(preGroupId, [])
            for prefixData in preGroupData:
                if prefixData.get('id') == prefixId:
                    prefixScore = prefixData.get('prefixScore', 0)
                    break

        return prefixScore

    def removePrefixProps(self):
        self.delProp(('preprops', 'prefixInfo'))
        if getattr(self, 'ses', {}).has_key(self.EQUIP_SE_PREFIX):
            self.loseEquipSpecialEffect(self.EQUIP_SE_PREFIX, 0)
        if getattr(self, 'propFix', {}).has_key(self.EQUIP_PROP_FIX_PREFIX):
            self.propFix[self.EQUIP_PROP_FIX_PREFIX] = []

    def genPrefix(self):
        prefix = (0, 0)
        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            if isManual:
                epd = MEPD.data.get(self.id, {})
            else:
                epd = XEPD.data.get(self.id, {})
            preGroupList = epd.get('preGroupList', ())
        else:
            ed = ED.data.get(self.id, {})
            preGroupList = ed.get('preGroupList', ())
        if not preGroupList:
            return prefix
        groupId = commcalc.weightingChoice([ groupId for groupId, _ in preGroupList ], [ prob for _, prob in preGroupList ])
        return self.genPrefixByGroupId(groupId, defaultPrefix=prefix)

    def genPrefixByGroupId(self, groupId, defaultPrefix = (0, 0)):
        prefix = defaultPrefix
        prefixData = EPFPD.data.get(groupId, None)
        if not prefixData:
            return prefix
        propDataList = []
        propWeightList = []
        for pd in prefixData:
            if pd['lvStart'] > self.itemLv or pd['lvEnd'] < self.itemLv:
                continue
            propDataList.append({'groupId': groupId,
             'data': pd})
            propWeightList.append(pd['prob'])

        if propDataList:
            propData = commcalc.weightingChoice(propDataList, propWeightList)
            prefix = (propData['groupId'], propData['data']['id'])
        return prefix

    def addPrefixProps(self, preGroupId, prefixId, extra = None):
        prefixData = EPFPD.data.get(preGroupId)
        if not prefixData:
            return
        data = {}
        for pd in prefixData:
            if pd['id'] == prefixId:
                data = pd
                break

        if not data:
            gamelog.error('invalid prefixId', self.id, preGroupId, prefixId)
            return
        self.preprops = []
        self.prefixInfo = (preGroupId, prefixId)
        if data.has_key('props'):
            for pid, pType, pVal in data['props']:
                self.preprops.append((pid, pType, pVal))

        if data.has_key('sEffect'):
            if not hasattr(self, 'ses'):
                self.ses = {}
            if self.ses.has_key(self.EQUIP_SE_PREFIX):
                self.loseEquipSpecialEffect(self.EQUIP_SE_PREFIX, 0)
            self.gainEquipSpecialEffect(self.EQUIP_SE_PREFIX, data['sEffect'])
        if data.has_key('propFix'):
            if not hasattr(self, 'propFix'):
                self.propFix = {}
            self.propFix[self.EQUIP_PROP_FIX_PREFIX] = [data['propFix']]
            self.refreshPropsFix()
        self.calcScores(extra=extra)

    def _getMatchPrefixIdByOldId(self, groupId, prefId):
        prefixData = EPFPD.data.get(groupId, None)
        preTypeId = 0
        newId = prefId
        if prefixData:
            for pd in prefixData:
                if pd['id'] == prefId:
                    if pd.has_key('preTypeId'):
                        preTypeId = pd['preTypeId']
                    break

        if preTypeId:
            for i, startEndList in EPTRD.data.get(preTypeId, {}).iteritems():
                if startEndList[0] <= self.itemLv <= startEndList[1]:
                    newId = i
                    break

        return newId

    def _inheritPrefix(self, fromEquip, allowPreAdjust = False):
        self.removePrefixProps()
        if not hasattr(fromEquip, 'prefixInfo'):
            return
        self.prefixInfo = fromEquip.prefixInfo
        self.preprops = copy.deepcopy(fromEquip.preprops)
        groupId, did = self.prefixInfo
        prefixData = EPFPD.data.get(groupId, None)
        if not prefixData:
            return
        if allowPreAdjust:
            oldDid = did
            did = self._getMatchPrefixIdByOldId(groupId, oldDid)
            if did != oldDid:
                prefixData = EPFPD.data[groupId]
                self.prefixInfo = (groupId, did)
                self.preprops = []
                for pd in prefixData:
                    if pd['id'] == did:
                        if pd.has_key('props'):
                            for pid, pType, pVal in pd['props']:
                                self.preprops.append((pid, pType, pVal))

                        break

        for pd in prefixData:
            if pd['id'] == did:
                if pd.has_key('sEffect'):
                    self.gainEquipSpecialEffect(self.EQUIP_SE_PREFIX, pd['sEffect'])
                if pd.has_key('propFix'):
                    if not hasattr(self, 'propFix'):
                        self.propFix = {}
                    self.propFix[self.EQUIP_PROP_FIX_PREFIX] = [pd['propFix']]
                    self.refreshPropsFix()
                break

    def _inheritRProps(self, fromEquip):
        if hasattr(fromEquip, 'rprops'):
            self.rprops = copy.deepcopy(fromEquip.rprops)
        if getattr(fromEquip, 'ses', {}).has_key(self.EQUIP_SE_BASE):
            self.loseEquipSpecialEffect(self.EQUIP_SE_BASE, 0)
            for seid in fromEquip.ses.get(self.EQUIP_SE_BASE, []):
                self.gainEquipSpecialEffect(self.EQUIP_SE_BASE, seid)

        if getattr(fromEquip, 'propFix', {}).has_key(self.EQUIP_PROP_FIX_BASE):
            self.propFix = {}
            self.propFix[self.EQUIP_PROP_FIX_BASE] = copy.deepcopy(fromEquip.propFix.get(self.EQUIP_PROP_FIX_BASE))

    def _checkFeed(self, owner, otherEquipIt, bMsg = True):
        if self.type != self.BASETYPE_EQUIP:
            return False
        if otherEquipIt.type != self.BASETYPE_EQUIP:
            return False
        if self.uuid == otherEquipIt.uuid:
            return False
        otherEquipData = ED.data.get(otherEquipIt.id)
        equipData = ED.data.get(self.id)
        if not otherEquipData or not equipData:
            gamelog.error('data not configured in equipment data!! %d' % self.id)
            return False
        if self.starLv >= self.maxStarLv:
            bMsg and owner.client.showGameMsg(GMDD.data.EQUIP_STAR_FEED_FAIL_MAX_LV, ())
            gamelog.error('reach max starLv', self.id, self.maxStarLv)
            return False
        etp = otherEquipData.get('equipType')
        if not otherEquipData.has_key('equipType') or not ESFD.data.has_key((self.quality, etp, otherEquipIt.equipSType)):
            bMsg and owner.client.showGameMsg(GMDD.data.EQUIP_STAR_FEED_FAIL_WRONG_ITEM, (otherEquipIt.name,))
            gamelog.debug('zt: feed equip wrong item', self.quality, etp, otherEquipIt.equipSType)
            return False
        expFormula = ESFD.data[self.quality, etp, otherEquipIt.equipSType].get('exp')
        if not expFormula:
            gamelog.error('zt: empty exp formula', expFormula)
            return False
        formulaId, formulaParams = expFormula[0], expFormula[1:]
        fd = FSD.data.get(formulaId)
        formula = fd.get('formula')
        if not formula:
            gamelog.error('zt: empty formula', expFormula)
            return False
        return True

    def feedEquip(self, owner, otherEquipIt):
        return False
        if not self._checkFeed(owner, otherEquipIt):
            return False
        otherEquipData = ED.data[otherEquipIt.id]
        etp = otherEquipData['equipType']
        expFormula = ESFD.data[self.quality, etp, otherEquipIt.equipSType]['exp']
        formulaId, formulaParams = expFormula[0], expFormula[1:]
        expAdd = otherEquipIt.evalValue(formulaId, formulaParams, {'totalStarExp': otherEquipIt.calcTotalStarExp()})
        expAdd *= otherEquipData.get('equipFeedFactor', 1.0)
        self.incStarExp(owner, expAdd)
        oldEquipIt = self.deepcopy()
        if otherEquipIt.isForeverBind():
            self.bindItem()
            if BigWorld.component in ('base', 'cell'):
                opNUID = Netease.getNUID()
                serverlog.genItemLog(owner, oldEquipIt, 0, opNUID, LSDD.data.LOG_SRC_EQUIP_ITEM, detail=logconst.ITEM_EQUIP_FEED_BIND)
        gamelog.debug('zt: equip feed', self.id, self.quality, otherEquipIt.id, etp, otherEquipIt.equipSType, expAdd, otherEquipData.get('equipFeedFactor', 1.0), formulaId, formulaParams)
        return True

    def _getEquipStarUpExpByStarLv(self, starLv):
        starExpData = ESLUD.data.get(starLv, {})
        lvUpFormula = starExpData.get('upExp')
        if not lvUpFormula:
            gamelog.error('jjh@_getEquipStarUpExp error, empty lvUpFormula')
            return 0
        needExp = self.evalValue(lvUpFormula[0], lvUpFormula[1:])
        return int(needExp)

    def _getEquipStarUpExp(self):
        return self._getEquipStarUpExpByStarLv(self.starLv)

    def _getEquipStarExpCeil(self):
        if self.isWingOrRide():
            return sys.maxint
        ceil = 30 * self._getEquipStarUpExp()
        ceilMaxStarLv = 0
        starLv = getattr(self, 'starLv', 0)
        while starLv <= getattr(self, 'maxStarLv', 0):
            ceilMaxStarLv += self._getEquipStarUpExpByStarLv(starLv)
            starLv += 1

        ceil = min(ceil, ceilMaxStarLv)
        return int(ceil)

    def _manualStarLvUp(self, owner, lvupStarExp):
        gamelog.debug('jjh@_manualStarLvUp ', owner.id, self.id, self.starExp, lvupStarExp, self.starLv, self.activeStarLv)
        effect_equip = const.CONT_EMPTY_VAL
        pos = const.CONT_NO_POS
        sub_pos = const.CONT_NO_POS
        sub_equip, sub_page, sub_pos = owner.subEquipment.findItemByUUID(self.uuid)
        if sub_equip == const.CONT_EMPTY_VAL:
            effect_equip, pos = owner.equipment.findEquipByUUID(self.uuid)
        else:
            pos = gametypes.subEquipToEquipPartMap.get(sub_pos, gametypes.EQU_PART_NONE)
            if pos != gametypes.EQU_PART_NONE:
                effect_equip = owner.equipment.get(pos)
        if effect_equip != const.CONT_EMPTY_VAL:
            Equipment.unApplyEquip(owner, effect_equip)
        self.starExp = self.starExp - lvupStarExp
        self.starLv += 1
        self.activeStarLv = max(self.starLv, self.activeStarLv)
        if self.starExp < self._getEquipStarUpExp():
            if not hasattr(self, 'propFix'):
                self.propFix = {}
            elif self.propFix.pop(self.EQUIP_PROP_FIX_STARLV, None):
                self.refreshPropsFix()
        if effect_equip != const.CONT_EMPTY_VAL:
            Equipment.applyEquip(owner, effect_equip)
        if self.starExp < self._getEquipStarUpExp():
            loseSes = self.loseEquipSpecialEffect(self.EQUIP_SE_STARLV, 0)
            if loseSes:
                for seId in loseSes:
                    seInfo = ESPD.data.get(seId, {})
                    for pskillId, pskillLv in seInfo.get('pskillDict', {}).iteritems():
                        owner.removePSkill(pskillId, const.PSKILL_SOURCE_EQUIP_SPECIAL_EFFECT, self.uuid)

        self.calcScores(extra={'owner': owner})

    def needPushLvUpMsg(self, oldExp, nowExp):
        if oldExp >= nowExp:
            return False
        starLv = getattr(self, 'starLv', 0)
        maxStarLv = getattr(self, 'maxStarLv', 0)
        starLvupExp = 0
        while starLv <= maxStarLv:
            starLvupExp += self._getEquipStarUpExpByStarLv(starLv)
            if nowExp < starLvupExp:
                return False
            if oldExp < starLvupExp:
                return True
            starLv += 1
            continue

        return False

    def _getRandomEquipStarPropData(self):
        starRandId, starEffDataId = getattr(self, 'manualEquipStarInfo', (-1, -1))
        for data in MESTARPD.data.get(starRandId, []):
            if data['id'] == starEffDataId:
                return data

        return {}

    def _getStarEffetInfo(self):
        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            data = self._getRandomEquipStarPropData()
            return (data.get('starSEffect'), data.get('propFix'))
        ed = ED.data.get(self.id, {})
        return (ed.get('starSEffect'), ed.get('starPropFix'))

    def _randomInitStarLv(self, ed = None):
        ed = ed or ED.data.get(self.id, {})
        starRandMode = ed.get('starRandMode', -1)
        if EISD.data.has_key((starRandMode, self.quality)):
            starLvData = EISD.data[starRandMode, self.quality].get('starLvs', None)
            if starLvData:
                lvr = commcalc.weightingChoice([ (slv, alv) for slv, alv, _ in starLvData ], [ prob for _, _, prob in starLvData ])
                self.maxStarLv, self.inactiveStarLv = lvr

    def incStarExp(self, owner, val):
        lvupStarExp = self._getEquipStarUpExp()
        if lvupStarExp <= 0:
            return (0, False)
        oldStarExp = self.starExp
        self.starExp = min(self.starExp + val, self._getEquipStarExpCeil())
        delta = self.starExp - oldStarExp
        if delta <= 0:
            return (0, False)
        self._autoCheckStarLvUp(owner, lvupStarExp)
        oldLvUpStarExp = lvupStarExp
        propChanged = False
        if oldStarExp < oldLvUpStarExp and self.starExp >= lvupStarExp:
            ed = ED.data.get(self.id)
            starEffect, starPropFix = self._getStarEffetInfo()
            if starEffect:
                if self.gainEquipSpecialEffect(self.EQUIP_SE_STARLV, starEffect) and owner:
                    part = owner.equipment.findItemByAttr({'uuid': self.uuid})
                    if part != const.CONT_NO_POS:
                        seId = self.ses[self.EQUIP_SE_STARLV][-1]
                        seInfo = ESPD.data.get(seId, {})
                        for pskillId, pskillLv in seInfo.get('pskillDict', {}).iteritems():
                            owner.addPSkill(pskillId, pskillLv, const.PSKILL_SOURCE_EQUIP_SPECIAL_EFFECT, self.uuid, calc=False)

            if starPropFix:
                if not hasattr(self, 'propFix'):
                    self.propFix = {}
                self.propFix[self.EQUIP_PROP_FIX_STARLV] = [starPropFix]
                self.refreshPropsFix()
            propChanged = True
            self.calcScores(extra={'owner': owner})
        if self.needPushLvUpMsg(oldStarExp, self.starExp):
            if BigWorld.component != 'client' and owner:
                _, part = owner.equipment.findEquipByUUID(self.uuid)
                if part != const.CONT_NO_POS:
                    owner.client.pushStarLvUpMsg(part)
        return (delta, propChanged)

    def _autoCheckStarLvUp(self, owner, lvupStarExp):
        if self.starExp >= lvupStarExp and self.starLv < self.activeStarLv:
            gamelog.debug('zt: star lv up', owner.id, self.id, self.starExp, lvupStarExp)
            extraExp = self.starExp - lvupStarExp
            self.starExp = 0
            self.starLv += 1
            self.incStarExp(owner, extraExp)
            self.calcScores(extra={'owner': owner})

    def calcTotalStarExp(self):
        if not hasattr(self, 'starLv') or not hasattr(self, 'starExp'):
            return 0
        totalExp = 0
        for slv in xrange(0, self.starLv):
            starExpData = ESLUD.data.get(slv, {})
            lvUpFormula = starExpData.get('upExp')
            if not lvUpFormula:
                break
            expAdd = self.evalValue(lvUpFormula[0], lvUpFormula[1:])
            totalExp += expAdd

        return int(totalExp + self.starExp)

    def decStarExp(self, owner, val):
        oldStarExp = self.starExp
        oldLvUpStarExp = self._getEquipStarUpExp()
        self.starExp -= val
        self.checkStarLvDown(owner)
        propChanged = False
        if oldStarExp >= oldLvUpStarExp and self.starExp < self._getEquipStarUpExp():
            ed = ED.data.get(self.id)
            if self.loseEquipSpecialEffect(self.EQUIP_SE_STARLV, 0):
                starEffect, starPropFix = self._getStarEffetInfo()
                if starEffect:
                    seInfo = ESPD.data.get(starEffect, {})
                    for pskillId, pskillLv in seInfo.get('pskillDict', {}).iteritems():
                        owner and owner.removePSkill(pskillId, const.PSKILL_SOURCE_EQUIP_SPECIAL_EFFECT, self.uuid)

            if not hasattr(self, 'propFix'):
                self.propFix = {}
            elif self.propFix.pop(self.EQUIP_PROP_FIX_STARLV, None):
                self.refreshPropsFix()
            propChanged = True
        return (val, propChanged)

    def checkStarLvDown(self, owner):
        needCalcScores = self.starExp < 0
        while self.starExp < 0:
            if self.starLv > 0:
                self.starLv -= 1
                maxStarExp = self._getEquipStarUpExp()
                if maxStarExp > 0:
                    self.starExp = self.starExp + maxStarExp
                else:
                    self.starExp = 0
            else:
                self.starExp = 0

        if needCalcScores:
            self.calcScores(extra={'owner': owner})

    def inheritStarLv(self, fromEquip):
        maxStarLv, inactiveStarLv = getattr(fromEquip, 'maxStarLv', 0), getattr(fromEquip, 'inactiveStarLv', 0)
        if maxStarLv == 0 and inactiveStarLv == 0:
            return
        ed = ED.data.get(self.id, {})
        starRandMode = ed.get('starRandMode', -1)
        starLvData = EISD.data[starRandMode, self.quality].get('starLvs', None)
        if not starLvData:
            return
        starLvs = sorted([ (slv if slv >= 0 else 0, alv if alv >= 0 else 0) for slv, alv, _ in starLvData ])
        if not starLvs:
            return
        minStarLvSum = starLvs[0][0] + starLvs[0][1]
        maxStarLvSum = starLvs[-1][0] + starLvs[-1][1]
        if maxStarLv + inactiveStarLv >= maxStarLvSum:
            self.maxStarLv = min(maxStarLv, maxStarLvSum)
            self.inactiveStarLv = maxStarLvSum - self.maxStarLv
        elif maxStarLv + inactiveStarLv <= minStarLvSum:
            self.maxStarLv = max(maxStarLv, starLvs[0][0])
            self.inactiveStarLv = minStarLvSum - self.maxStarLv
        else:
            self.maxStarLv, self.inactiveStarLv = maxStarLv, inactiveStarLv

    def inheritStarLvArbitrary(self, fromEquip):
        maxStarLv, inactiveStarLv = getattr(fromEquip, 'maxStarLv', 0), getattr(fromEquip, 'inactiveStarLv', 0)
        if maxStarLv == 0 and inactiveStarLv == 0:
            return
        fromTotalStarLv = maxStarLv + inactiveStarLv
        selfTotalStarLv = self.maxStarLv + self.inactiveStarLv
        if fromTotalStarLv >= selfTotalStarLv:
            self.maxStarLv = min(maxStarLv, selfTotalStarLv)
            self.inactiveStarLv = selfTotalStarLv - self.maxStarLv
        else:
            self.maxStarLv = max(maxStarLv, self.maxStarLv)
            self.inactiveStarLv = selfTotalStarLv - self.maxStarLv

    def _reportCritical(self):
        if BigWorld.component in ('base', 'cell'):
            gameengine.reportCritical('Verify in Item:%d(%s,%s),%d(%d)' % (self.id,
             self.name,
             self.guid(),
             self.cwrap,
             self.mwrap))

    def isWrap(self):
        if self.cwrap > 1:
            return True
        return False

    def beMax(self):
        return self.cwrap == self.mwrap

    def overMax(self, amount):
        if amount > self.mwrap:
            return True
        return False

    def overCurr(self, amount):
        if amount > self.cwrap:
            return True
        return False

    def underCurr(self, amount):
        if amount < self.cwrap:
            return True
        return False

    def eqCurr(self, amount):
        if amount == self.cwrap:
            return True
        return False

    def overBear(self, amount):
        if not self.canWrap():
            return True
        if self.cwrap + amount > self.mwrap:
            return True
        return False

    def incWrap(self, amount):
        self.cwrap = min(self.cwrap + amount, self.mwrap)
        return self

    def decWrap(self, amount):
        self.cwrap = max(self.cwrap - amount, 0)
        return self

    def setWrap(self, amount):
        if not hasattr(self, 'canOverMax'):
            self.cwrap = min(amount, self.mwrap)
        else:
            self.cwrap = amount
        return self

    def isOneDotaBattleField(self):
        return self.isDotaBattleFieldItem(self.id)

    def isOneQuest(self):
        return self.isQuestItem(self.id)

    def isOneBusiness(self):
        return self.isBusinessItem(self.id)

    def isOneUse(self):
        return hasattr(self, 'need_target')

    def isOneMall(self):
        return getattr(self, '_mallType', const.MALL_TYPE_NONE) != const.MALL_TYPE_NONE

    def hasOutdate(self):
        now = utils.getNow()
        mallExpireTime = getattr(self, '_mallExpireTime', now)
        if mallExpireTime <= 0:
            return False
        return now > mallExpireTime

    def updateProp(self, dict):
        self.__dict__.update(dict)
        return self

    def dumpProp(self):
        return dumps(self.__dict__, -1)

    def delProp(self, props):
        for p in props:
            self.__dict__.pop(p, None)

        return self

    def popProp(self, prop, default = None):
        return self.__dict__.pop(prop, default)

    def copyDict(self):
        return copy.deepcopy(self.__dict__)

    @staticmethod
    def maxWrap(id):
        it = ID.data.get(id)
        if it and it.has_key('mwrap'):
            return it['mwrap']
        else:
            return Item.PROPERTY_CHART['mwrap']

    @staticmethod
    def isQuestItem(id):
        iData = ID.data.get(id)
        if iData and iData.has_key('questItem'):
            return iData['questItem']
        else:
            return False

    @staticmethod
    def isDotaBattleFieldItem(id):
        return ID.data.get(id, {}).get('isDotaBattleField', 0)

    @staticmethod
    def isMaterialItem(id):
        iData = ID.data.get(id)
        if iData and iData.has_key('type') and iData['type'] == Item.BASETYPE_MATERIAL:
            return iData['type']
        else:
            return False

    @staticmethod
    def isBusinessItem(id):
        iData = ID.data.get(id)
        if iData and iData.has_key('businessItem'):
            return iData['businessItem']
        else:
            return False

    @staticmethod
    def isHierogramItem(id):
        iData = ID.data.get(id)
        if iData and iData.has_key('type') and iData['type'] in Item.BASETYPE_RUNES:
            return True
        else:
            return False

    @staticmethod
    def hierogramLv(id):
        return NRD.data.get(id, {}).get('lv', 0)

    @staticmethod
    def parentId(itemId):
        if ID.data.get(itemId, {}).has_key('parentId'):
            return ID.data[itemId]['parentId']
        return itemId

    @staticmethod
    def canTakeToCrossServer(itemId):
        if ID.data.get(itemId, {}).has_key('canTakeToCrossServer'):
            return ID.data[itemId]['canTakeToCrossServer']
        return False

    def consistent(self):
        if not ID.data.has_key(self.id):
            gamelog.error('Error:item id', self.name, self.id)
            if BigWorld.component in ('cell', 'base'):
                gameengine.reportCritical('item id not found in item_data %s %d' % (self.name, self.id))
            return
        if hasattr(self, 'compositeShopInfo') and time.time() - self.compositeShopInfo[0] > SCD.data.get('timeToReturnShop', 600):
            delattr(self, 'compositeShopInfo')
        data = ID.data[self.id]
        if data.get('bindType', 0) == gametypes.ITEM_BIND_TYPE_FOREVER and not self.isForeverBind():
            self.bindItem()
        if not data.has_key('ttl') and hasattr(self, 'expireTime') and self.id == 201158:
            self.delProp(('expireTime',))
        if BigWorld.component in ('base', 'cell') and gameconfig.useItemVersion():
            if not hasattr(self, 'version'):
                return
            currVer = Item.TIMESTAMP
            if self.version == currVer:
                return
        if BigWorld.component != 'client':
            if self.version < Item.EDTIMESTAMP:
                if hasattr(self, 'propFix') and type(self.propFix) != dict:
                    self.delProp(('propFix',))
                if hasattr(self, 'ses') and type(self.ses) != dict:
                    self.delProp(('ses',))
                self.initEquipData(Item.EQUIP_CONSIST_PROPERTIES, False)
            if self.version < Item.CIDTIMESTAMP:
                self.__initConsumableData(False)
            if self.version < Item.LEDTIMESTAMP:
                self.__initLifeEquipData(False)
            if self.version < Item.SPLEDTIMESTAMP:
                self.__initFishingEquipData()
                self.__initExploreEquipData()
        if self.cwrap > self.mwrap:
            gamelog.error('Error:item cwrap over mwrap', self.name, self.id, self.mwrap, self.cwrap, self.guid())
        if self.cwrap == 0 and self.id != 1 and self.id != 2:
            gamelog.error('Error:item cwrap equal zero', self.name, self.id, self.mwrap, self.cwrap, self.guid())
        if self.isRuneEquip():
            self.consistentRuneEquipData()
        if self.isRune():
            self.consistentRuneData()
        if self.isHieroEquip():
            pass
        if self.isEquip() and not self.isWingOrRide() and BigWorld.component != 'client' and self.version < Item.TIMESTAMP:
            hasStarProp = hasattr(self, 'propFix') and bool(self.propFix.get(self.EQUIP_PROP_FIX_STARLV, []))
            hasStarEff = hasattr(self, 'ses') and bool(self.ses.get(self.EQUIP_SE_STARLV, []))
            changed = False
            if not hasStarProp and not hasStarEff:
                if self.starExp >= self._getEquipStarUpExp():
                    oldStarExp = self.starExp
                    self.decStarExp(None, oldStarExp)
                    self.incStarExp(None, oldStarExp)
                    self.refreshPropsFix()
                    changed = True
            elif hasStarProp:
                if self.starExp >= self._getEquipStarUpExp():
                    self.propFix[self.EQUIP_PROP_FIX_STARLV] = self.propFix[self.EQUIP_PROP_FIX_STARLV][:1]
                else:
                    self.propFix.pop(self.EQUIP_PROP_FIX_STARLV, None)
                    changed = True
                if changed:
                    self.refreshPropsFix()
            if self.starExp >= self._getEquipStarExpCeil():
                self.starExp = self._getEquipStarExpCeil()
                changed = True
            self.calcScores(calcRarityMiracle=True)
        self.updateQuality()
        self.updateOwnershipPercent()
        if self.isGuanYin():
            self.consistentGuanYinData()
        if BigWorld.component in ('base', 'cell') and gameconfig.useItemVersion():
            self.version = currVer

    def updateOwnershipPercent(self):
        itemData = ID.data.get(self.id)
        if not itemData:
            return
        if hasattr(self, 'ownershipPercent'):
            return
        if itemData.has_key('ttl') and itemData.get('canRenewal', 0) and 'ownership' in itemData:
            self.ownershipPercent = itemData.get('ownership')

    def updateQuality(self):
        fixedQuality = ID.data.get(self.id, {}).get('fixedQuality', 0)
        if not fixedQuality:
            return
        if not hasattr(self, 'quality'):
            return
        if self.category != gametypes.ITEM_CATEGORY_FASHION:
            return
        quality = ID.data.get(self.id, {}).get('quality', 0)
        if quality > 0:
            self.quality = quality

    def loadProp(self, bytes):
        self.__dict__.update(loads(bytes))
        self.consistent()
        return self

    def deepcopy(self, regen = False, fromGuid = False):
        new = copy.deepcopy(self)
        if regen:
            new.uuid = utils.getUUID()
            new.uutime = utils.getNow()
            if fromGuid:
                new.fromGuid = [self.guid()]
        return new

    def regen(self):
        self.uuid = utils.getUUID()
        self.uutime = utils.getNow()

    def pickleItemEx(self, cwrap):
        itemDict = dict(self.__dict__)
        itemDict['cwrap'] = cwrap
        return dumps(itemDict, -1)

    def canWrap(self):
        if getattr(self, 'bWrap', True) == False:
            return False
        if self.mwrap > 1 and not self.hasLatch():
            return True
        return False

    def hasHoldMax(self):
        if self.id in ID.data and ID.data.get(self.id, {}).has_key('holdMax'):
            return (True, ID.data.get(self.id, {})['holdMax'])
        else:
            return (False, 0)

    def canDiscard(self):
        if self.isRuneEquip() and len(self.runeData) > 0:
            return False
        return utils.getItemNoDrop(ID.data.get(self.id, {})) == 0

    def selfcheck(self, strong = False):
        if self.cwrap > self.mwrap and not hasattr(self, 'canOverMax') or self.cwrap <= 0:
            self._reportCritical()
            return True
        if strong:
            if self.isExpireTTL():
                return True
        return False

    def isRunOrderUp(self):
        return True

    def isRunChongXi(self):
        return True

    def isRunForging(self):
        return True

    def isRunReforging(self):
        return True

    def isDye(self):
        if not hasattr(self, 'cstype'):
            return False
        if self.cstype == Item.SUBTYPE_2_DYE:
            return True
        return False

    def isRubbing(self):
        if self.isEquip() and self.equipType in (Item.EQUIP_BASETYPE_ARMOR_RUBBING, Item.EQUIP_BASETYPE_WEAPON_RUBBING):
            return True
        return False

    def isRongGuang(self):
        if not hasattr(self, 'cstype'):
            return False
        if self.cstype == Item.SUBTYPE_2_RONGGUANG:
            return True
        return False

    def isWear(self):
        if self.equipType == Item.EQUIP_BASETYPE_FASHION:
            if self.equipSType >= Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE and self.equipSType <= Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR:
                return True
        return False

    def isNeedHyperlink(self):
        if self.type in (Item.BASETYPE_EQUIP,
         Item.BASETYPE_RUNE_EQUIP,
         Item.BASETYPE_HIEROGRAM_EQUIP,
         Item.BASETYPE_RUNE,
         Item.BASETYPE_HIEROGRAM_CRYSTAL,
         Item.BASETYPE_EQUIP_GEM):
            return True
        if self.isAddStarExpItem():
            return True
        return False

    def isEquip(self):
        if self.type == Item.BASETYPE_EQUIP:
            return True
        return False

    def isWeaponOrArmor(self):
        if not self.isEquip():
            return False
        elif self.isRubbing():
            return False
        elif self.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_JEWELRY):
            return True
        elif self.equipType == Item.EQUIP_BASETYPE_ARMOR:
            we = self.whereEquip()
            return we and we[0] not in (gametypes.EQU_PART_RIDE, gametypes.EQU_PART_WINGFLY)
        else:
            return False

    def hasRuneEquipExp(self):
        iData = ID.data.get(self.id)
        if not iData:
            return False
        runeEquipExp = iData.get('runeEquipExp', 0)
        if runeEquipExp == 0:
            return False
        return True

    def isCanPutIntoFashionBag(self):
        iData = ID.data.get(self.id)
        if not iData:
            return False
        return iData.get('canPutFashionBag', False)

    @staticmethod
    def getDyeMaterialsScore(itId, mdd = None):
        if mdd is None:
            mdd = {}
            for mId, mVal in MDD.data.iteritems():
                pItemId = ID.data.get(mId, {}).get('parentId', mId)
                mdd[pItemId] = mVal

        iData = mdd.get(itId)
        if not iData:
            return 0
        return iData.get('randomDyeScore', 0)

    def fashionEquipDyeMaterialsNum(self):
        if not self.isCanDye():
            return 0
        equipData = ED.data.get(self.id, {})
        dyeNum = equipData.get('dyeNum', 1)
        dualDyeNum = equipData.get('dualDyeNum', dyeNum)
        canDye = self.isCanDye()
        materialsNum = dyeNum + dualDyeNum
        if canDye == gametypes.DYE_SINGLE:
            materialsNum = dyeNum
        return materialsNum

    def isCanDye(self):
        if self.isEquip() and hasattr(self, 'canDye'):
            return self.canDye
        return 0

    def isCanRubbing(self):
        equipData = ED.data.get(self.id, {})
        if self.isEquip() and equipData.get('canRubbing', 0):
            return True
        return False

    def isCanRongGuang(self):
        equipData = ED.data.get(self.id, {})
        if self.isEquip() and equipData.get('canRongGuang', 0):
            return True
        return False

    def isPermitDualDye(self):
        equipData = ED.data.get(self.id, {})
        if self.isEquip() and equipData.get('permitDualDye', 0):
            return True
        return False

    def isCanTexture(self):
        equipData = ED.data.get(self.id, {})
        if self.isEquip() and equipData.get('canTexture', 0):
            return True
        return False

    def isCanSign(self):
        equipData = ED.data.get(self.id, {})
        if self.isEquip() and equipData.get('canSign', 1):
            return True
        return False

    def whereEquip(self):
        return Item.EQUIP_PART_TABLE[self.equipType][self.equipSType]

    def wherePreview(self):
        equipType = Item.EQUIP_BASETYPE_ARMOR if self.equipType == Item.EQUIP_BASETYPE_ARMOR_RUBBING else self.equipType
        return Item.EQUIP_PART_TABLE[equipType][self.equipSType]

    def ctrlPreviewEffect(self):
        iData = ID.data.get(self.id)
        return iData.get('ctrl', 0) and iData.get('ctrlPreviewEffect', 0)

    def checkLockedSlot(self):
        for i in xrange(Item.GEM_SLOT_MAX_CNT):
            yinSlotData = self.getEquipGemSlot(Item.GEM_TYPE_YIN, i)
            if yinSlotData != None and yinSlotData.state == Item.GEM_SLOT_LOCKED:
                return True

        for i in xrange(Item.GEM_SLOT_MAX_CNT):
            yangSlotData = self.getEquipGemSlot(Item.GEM_TYPE_YANG, i)
            if yangSlotData != None and yangSlotData.state == Item.GEM_SLOT_LOCKED:
                return True

        return False

    def canInlayGem(self):
        slotsCnt = len(getattr(self, 'yangSlots', [])) + len(getattr(self, 'yinSlots', []))
        if slotsCnt == 0:
            return False
        return True

    def isFishingEquip(self):
        if self.type == Item.BASETYPE_LIFE_SKILL:
            itemData = SLSED.data.get(self.id, {})
            if itemData.get('fishingEquipType', 0) in gametypes.FISHING_EQUIP:
                return True
        return False

    def whereEquipFishing(self):
        if self.type == Item.BASETYPE_LIFE_SKILL:
            fed = SLSED.data.get(self.id)
            if not fed:
                gamelog.error('data not configured in fishing equipment data!! %d' % self.id)
                return -1
            fishingEquipType = fed.get('fishingEquipType')
            return Item.FISHING_EQUIP_PART_TABLE.get(fishingEquipType, -1)
        if self.type == Item.BASETYPE_CONSUMABLE:
            return Item.FISHING_EQUIP_PART_TABLE.get(self.cstype, -1)
        return -1

    def isExploreEquip(self):
        if self.type == Item.BASETYPE_LIFE_SKILL:
            itemData = SLSED.data.get(self.id, {})
            if itemData.get('fishingEquipType', 0) == gametypes.EXPLORE_EQU_TYPE_COMPASS:
                return True
        if self.type == Item.BASETYPE_CONSUMABLE and getattr(self, 'cstype', 0) == Item.SUBTYPE_2_EXPLORE_SCROLL:
            return True
        return False

    def whereEquipExplore(self):
        equipData = SLSED.data.get(self.id, {})
        if self.type == Item.BASETYPE_LIFE_SKILL:
            if equipData.get('fishingEquipType', 0) == gametypes.EXPLORE_EQU_TYPE_COMPASS:
                return gametypes.EXPLORE_EQUIP_COMPASS
        elif self.type == Item.BASETYPE_CONSUMABLE:
            if equipData.get('fishingEquipType', 0) == gametypes.EXPLORE_EQU_TYPE_SCROLL:
                return gametypes.EXPLORE_EQUIP_SCROLL
        return -1

    def getCondition(self, type):
        res = {}
        conditionsList = ID.data.get(self.id, {}).get('conditionsList', {})
        for condition in conditionsList:
            if condition[0] == type:
                op = condition[2]
                limitVal = condition[3]
                if op == const.CON_EQUAL:
                    res['eq'] = limitVal
                elif op == const.CON_GREATER:
                    res['gt'] = limitVal
                elif op == const.CON_SMALLER:
                    res['lt'] = limitVal
                elif op == const.CON_GREATER_EQUAL:
                    res['gte'] = limitVal
                elif op == const.CON_SMALLER_EQUAL:
                    res['lte'] = limitVal

        return res

    def extraCheck(self, owner, showMsg = True, messageBuf = None):
        conditionsList = ID.data.get(self.id, {}).get('conditionsList', [])
        for condition in conditionsList:
            if condition[0] == const.CON_FAME:
                fameId = condition[1]
                value = owner.fame.getFame(fameId, owner.school)
                msgId = GMDD.data.CON_FAME_FAILED_LV
                fameName = FD.data[fameId].get('name', '声望')
                data = (self.name, fameName)
            elif condition[0] == const.CON_SOCIAL_LV:
                value = owner.socLv
                msgId = GMDD.data.CON_SOCLV_FAILED
                data = (self.name,)
            elif condition[0] == const.CON_SOCIAL_SCHOOL:
                value = owner.curSocSchool
                msgId = GMDD.data.CON_SOCSCHOOL_FAILED
                schoolName = SSD.data[condition[3]].get('job', '')
                data = (self.name, schoolName)
            elif condition[0] == const.CON_LIFE_SKILL:
                skillId = condition[1]
                if skillId not in owner.lifeSkills:
                    value = None
                else:
                    value = owner.lifeSkills[skillId].level
                msgId = GMDD.data.CON_LIFE_SKILL_FAILED_LV
                key = (skillId, value)
                if key in LSD.data:
                    skillName = LSD.data[key].get('name', '')
                else:
                    return False
                data = (self.name, skillName)
            elif condition[0] == const.CON_PROP:
                propId = condition[1]
                value = commcalc.getAvatarPropValueById(owner, propId)
                msgId = GMDD.data.CON_PROP_FAILED
                propName = PPD.data[propId].get('chName', '人物属性')
                data = (self.name, propName)
            elif condition[0] == const.CON_BUFF:
                stateId = condition[3]
                if not owner.statesServerAndOwn.has_key(stateId):
                    stateName = SD.data[stateId].get('name', '')
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(GMDD.data.CON_BUFF_FAILED, (self.name, stateName))
                        if messageBuf is not None:
                            messageBuf[GMDD.data.CON_BUFF_FAILED] = (self.name, stateName)
                    return False
                continue
            elif condition[0] == const.CON_SKILL_ENHANC_POINT:
                value = utils.getTotalSkillEnhancePoint(owner)
                data = (self.name,)
                msgId = GMDD.data.CON_ENHANCE_POINT_FAILED
            elif condition[0] == const.CON_NO_BUFF:
                stateId = condition[3]
                if owner.statesServerAndOwn.has_key(stateId):
                    stateName = SD.data[stateId].get('name', '')
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(GMDD.data.CON_NO_BUFF_FAILED, (self.name, stateName))
                        if messageBuf is not None:
                            messageBuf[GMDD.data.CON_NO_BUFF_FAILED] = (self.name, stateName)
                    return False
                continue
            elif condition[0] == const.CON_QUEST:
                questId = condition[1]
                if questId not in owner.quests:
                    from data import quest_data as QD
                    questName = QD.data.get(questId, {}).get('name', '')
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(GMDD.data.CON_QUEST_FAILED, (self.name, questName))
                        if messageBuf is not None:
                            messageBuf[GMDD.data.CON_QUEST_FAILED] = (self.name, questName)
                    return False
                continue
            elif condition[0] == const.CON_XIU_WEI_LEVEL:
                value = owner.xiuweiLevel
                data = (self.name,)
                msgId = GMDD.data.CON_XIU_WEI_LEVEL_FAILED
            else:
                return False
            if value is None:
                return False
            op = condition[2]
            limitVal = condition[3]
            if op == const.CON_EQUAL:
                if value != limitVal:
                    if condition[0] != const.CON_SOCIAL_SCHOOL:
                        data = data + ('等于', limitVal)
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(msgId, data)
                        if messageBuf is not None:
                            messageBuf[msgId] = data
                    return False
            elif op == const.CON_GREATER:
                if value <= limitVal:
                    data = data + ('大于', limitVal)
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(msgId, data)
                        if messageBuf is not None:
                            messageBuf[msgId] = data
                    return False
            elif op == const.CON_SMALLER:
                if value >= limitVal:
                    data = data + ('小于', limitVal)
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(msgId, data)
                        if messageBuf is not None:
                            messageBuf[msgId] = data
                    return False
            elif op == const.CON_GREATER_EQUAL:
                if value < limitVal:
                    data = data + ('不小于', limitVal)
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(msgId, data)
                        if messageBuf is not None:
                            messageBuf[msgId] = data
                    return False
            elif op == const.CON_SMALLER_EQUAL:
                if value > limitVal:
                    data = data + ('不大于', limitVal)
                    if owner != None:
                        showMsg and hasattr(owner, 'client') and owner.client and owner.client.showGameMsg(msgId, data)
                        if messageBuf is not None:
                            messageBuf[msgId] = data
                    return False
            else:
                return False

        return True

    def canUseCommon(self, sex, sch, lv, owner, showMsg = True, messageBuf = None):
        if self.selfcheck():
            return False
        if self.type not in Item.BASE_TYPE_USE_COMMON:
            return False
        if self.isExpireTTL():
            showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (self.name,))
            if messageBuf is not None:
                messageBuf[GMDD.data.ITEM_TTL_EXPIRE] = (self.name,)
            return False
        acExcitement = ID.data.get(self.id, {}).get('acExcitement')
        if acExcitement:
            if not owner.checkExcitementFeature(acExcitement):
                return False
        sexReq = ID.data.get(self.id, {}).get('sexReq', 0)
        if sexReq > 0 and sexReq != sex:
            if owner != None:
                showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SEX, (self.name,))
                if messageBuf is not None:
                    messageBuf[GMDD.data.ITEM_FORBIDDEN_WRONG_SEX] = (self.name,)
            return False
        if sch not in ID.data.get(self.id, {}).get('schReq', (sch,)):
            if owner != None:
                showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL, (self.name,))
                if messageBuf is not None:
                    messageBuf[GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL] = (self.name,)
            return False
        lvReq = self.lvReq
        maxLvReq = ID.data.get(self.id, {}).get('maxLvReq', 0)
        if flyUpUtils.enableFlyUp() and owner.flyUpLv:
            lvReq -= ID.data.get(self.id, {}).get('flyUpReduceReqLv', 0)
            maxLvReq += ID.data.get(self.id, {}).get('flyUpAddReqLv', 0)
        if lvReq > lv:
            if owner != None:
                showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LEVEL_LOWER, (self.name, lvReq))
                if messageBuf is not None:
                    messageBuf[GMDD.data.ITEM_FORBIDDEN_LEVEL_LOWER] = (self.name, lvReq)
            return False
        if maxLvReq and maxLvReq < lv:
            if owner != None:
                showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LEVEL_UPPER, (self.name, maxLvReq))
                if messageBuf is not None:
                    messageBuf[GMDD.data.ITEM_FORBIDDEN_LEVEL_UPPER] = (self.name, maxLvReq)
            return False
        combatReq = ID.data.get(self.id, {}).get('combatReq', 0)
        if combatReq == gametypes.ITEM_REQ_IN_COMBAT and not owner.inCombat:
            showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_SPECIAL_PERIOD, (self.name, '战斗'))
            if messageBuf is not None:
                messageBuf[GMDD.data.ITEM_FORBIDDEN_SPECIAL_PERIOD] = (self.name, '战斗')
            return False
        if combatReq == gametypes.ITEM_REQ_NOT_IN_COMBAT and owner.inCombat:
            showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_IN_COMBAT, ())
            if messageBuf is not None:
                messageBuf[GMDD.data.ITEM_FORBIDDEN_IN_COMBAT] = ()
            return False
        openServerDayLimit = SCD.data.get('openServerDayLimit', 0)
        if openServerDayLimit and utils.getServerOpenDays() > openServerDayLimit:
            lastWeekActivationReq = ID.data.get(self.id, {}).get('lastWeekActivationReq', 0)
            if lastWeekActivationReq:
                if owner is None:
                    return False
                if owner.lastWeekActivation < lastWeekActivationReq:
                    showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LAST_WEEK_ACTIVATION_LOWER, (self.name, lastWeekActivationReq / 1000))
                    if messageBuf is not None:
                        messageBuf[GMDD.data.ITEM_FORBIDDEN_LAST_WEEK_ACTIVATION_LOWER] = (self.name, lastWeekActivationReq / 1000)
                    return False
            maxLastWeekActivationReq = ID.data.get(self.id, {}).get('maxLastWeekActivationReq', 0)
            if maxLastWeekActivationReq:
                if owner is None:
                    return False
                if owner.lastWeekActivation > maxLastWeekActivationReq:
                    showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LAST_WEEK_ACTIVATION_UPPER, (self.name, maxLastWeekActivationReq / 1000))
                    if messageBuf is not None:
                        messageBuf[GMDD.data.ITEM_FORBIDDEN_LAST_WEEK_ACTIVATION_UPPER] = (self.name, maxLastWeekActivationReq / 1000)
                    return False
        zaijuReq = ID.data.get(self.id, {}).get('zaijuReq', 0)
        if zaijuReq and owner._isOnZaijuOrBianyao():
            owner.client and owner.client.chatToEventEx('载具上无法使用本物品', const.CHANNEL_COLOR_RED)
            if messageBuf is not None:
                messageBuf[GMDD.data.USE_ITEM_FORBIDDEN_ZAIJU] = ()
            return False
        fishingLvReq = self.getFishingLvReq()
        if fishingLvReq and owner.fishingLv < fishingLvReq:
            showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_FISHINGLV, ())
            if messageBuf is not None:
                messageBuf[GMDD.data.ITEM_FORBIDDEN_WRONG_FISHINGLV] = ()
            return False
        checkFameId = CID.data.get(self.id, {}).get('checkFameId')
        if checkFameId:
            fameCost = self._getFameConstNum(owner)
            if not owner.enoughFame([(checkFameId, fameCost)]):
                fameName = FD.data.get(checkFameId, {}).get('name', '')
                showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_USE_FAME_CHECK_FAILED, (self.name,
                 fameName,
                 fameCost,
                 fameName))
                if messageBuf is not None:
                    messageBuf[GMDD.data.ITEM_USE_FAME_CHECK_FAILED] = (self.name,
                     fameName,
                     fameCost,
                     fameName)
                return False
        if owner != None:
            if not self.extraCheck(owner, showMsg, messageBuf):
                return False
        if getattr(self, 'freezeUseTime', 0) > utils.getNow():
            showMsg and owner.client and owner.client.showGameMsg(GMDD.data.ITEM_FORBIDDEN_FREEZE_USE_TIME, ())
            return False
        return True

    def _getFameConstNum(self, owner):
        cdata = CID.data.get(self.id, {})
        checkFameNum = cdata.get('checkFameNum')
        checkFameRatio = cdata.get('checkFameRatio')
        checkFamePeriod = cdata.get('checkFamePeriod')
        group = cdata['useLimitGroup'] if cdata.has_key('useLimitGroup') else 0
        key = (gametypes.ITEM_USE_CHECK_GROUP, group) if group > 0 else (gametypes.ITEM_USE_CHECK_SINGLE, self.id)
        history = owner.itemUseHistory.get(key, {})
        if checkFamePeriod == gametypes.ITEM_USE_LIMIT_TYPE_FOREVER:
            curNum = history.get(checkFamePeriod, 0)
        else:
            t = utils.getDaySecond() if checkFamePeriod == gametypes.ITEM_USE_LIMIT_TYPE_DAY else utils.getWeekSecond()
            data = history.get(checkFamePeriod, (t, 0))
            if data[0] == t:
                curNum = data[1]
            else:
                curNum = 0
        if not checkFameRatio:
            ratio = 1
        else:
            ratio = 999999
            for num, r in checkFameRatio:
                if curNum < num:
                    ratio = r
                    break

        return int(checkFameNum * ratio)

    def gainEquipSpecialEffect(self, src, seId):
        if not hasattr(self, 'ses'):
            self.ses = {}
        if not self.ses.has_key(src):
            self.ses[src] = []
        if seId in self.ses[src]:
            return False
        self.ses[src].append(seId)
        self.refreshSeCache()
        seInfo = ESPD.data.get(seId, {})
        if seInfo.get('pskillDict', None):
            return True
        else:
            return False

    def loseEquipSpecialEffect(self, src, seId):
        if not hasattr(self, 'ses'):
            self.ses = {}
        if not self.ses.has_key(src):
            self.ses[src] = []
        loseSes = []
        if seId in self.ses[src]:
            self.ses[src].remove(seId)
            self.refreshSeCache()
            loseSes = [seId]
        elif not seId:
            loseSes = self.ses[src]
            self.ses[src] = []
            self.refreshSeCache()
        return loseSes

    def refreshSeCache(self):
        if not hasattr(self, 'ses') or not self.ses:
            return
        self.seCache = {}
        for seList in self.ses.itervalues():
            for seId in seList:
                seInfo = ESPD.data.get(seId, {}).get('ses')
                if not seInfo:
                    continue
                for key, type, value in seInfo:
                    self.seCache.setdefault(key, 0)
                    if type == 1:
                        self.seCache[key] -= value
                    else:
                        self.seCache[key] += value

        gamelog.debug('refreshSeCache', self.seCache)

    def isCombatEquReq(self):
        return ID.data.get(self.id, {}).get('combatEquReq', 0)

    def canUseNow(self, sex, sch, bodyType, lv, owner, isInBag = True, extraDict = None):
        if self.selfcheck():
            return False
        if isInBag and self.isExpireTTL():
            return False
        if not self.checkPlayerCondition(sex, sch, bodyType, lv, needLvCheck=True, extraDict=extraDict):
            return False
        return True

    def checkPlayerCondition(self, sex, sch, bodyType, lv, needLvCheck = True, extraDict = None):
        if self.id not in ID.data:
            return False
        sexReq = ID.data.get(self.id, {}).get('sexReq', 0)
        if sexReq > 0 and sexReq != sex:
            return False
        schReq = ID.data.get(self.id, {}).get('schReq', ())
        if schReq and sch not in schReq:
            return False
        if not utils.inAllowBodyType(self.id, bodyType, ID):
            return False
        if needLvCheck:
            reduceReqLv = addReqLv = 0
            if flyUpUtils.enableFlyUp() and extraDict and extraDict.get('flyUpLv', 0):
                reduceReqLv = ID.data.get(self.id, {}).get('flyUpReduceReqLv', 0)
                addReqLv = ID.data.get(self.id, {}).get('flyUpAddReqLv', 0)
            if self.lvReq - reduceReqLv > lv:
                return False
            maxLvReq = ID.data.get(self.id, {}).get('maxLvReq', 0)
            if maxLvReq and maxLvReq + addReqLv < lv:
                return False
        if flyUpUtils.enableFlyUp() and extraDict and extraDict.get('flyUpLv', 0) < ID.data.get(self.id, {}).get('flyUpLvLimit', 0):
            return False
        return True

    def canEquip(self, owner, where = None):
        sex = owner.physique.sex
        sch = owner.physique.school
        bodyType = owner.physique.bodyType
        lv = owner.lv
        jingJie = owner.jingJie
        if not self.isEquip():
            return Item.WRONG_PLACE
        part = self.whereEquip()
        if part == gametypes.EQU_PART_NONE:
            return Item.WRONG_PLACE
        if where is not None and where not in part:
            return Item.WRONG_PLACE
        acExcitement = ID.data.get(self.id, {}).get('acExcitement')
        if acExcitement:
            if not owner.checkExcitementFeature(acExcitement):
                return Item.WRONG_AC_EXCITEMENT
        lvReq = self.lvReq
        if flyUpUtils.enableFlyUp() and owner.flyUpLv:
            lvReq -= ID.data.get(self.id, {}).get('flyUpReduceReqLv', 0)
        if lvReq and lv < lvReq:
            return Item.WRONG_LEVEL
        if ID.data.get(self.id, {}).has_key('maxLvReq'):
            maxLvReq = ID.data.get(self.id, {})['maxLvReq']
            if flyUpUtils.enableFlyUp() and owner.flyUpLv:
                maxLvReq += ID.data.get(self.id, {}).get('flyUpAddReqLv', 0)
            if lv > maxLvReq:
                return Item.WRONG_LEVEL
        if ID.data.get(self.id, {}).has_key('sexReq'):
            if sex != ID.data.get(self.id, {})['sexReq']:
                return Item.WRONG_SEX
        if not utils.inAllowBodyType(self.id, bodyType, ID):
            return Item.WRONG_BODYTYPE
        if ID.data.get(self.id, {}).has_key('schReq'):
            if sch not in ID.data.get(self.id, {})['schReq']:
                return Item.WRONG_SCHOOL
        if utils.isJingJieOn() and ID.data.get(self.id, {}).has_key('needJingJie'):
            if jingJie < ID.data.get(self.id, {})['needJingJie']:
                return Item.WRONG_JINGJIE_LESS
        if self.isExpireTTL():
            return Item.WRONG_OUT
        if hasattr(self, 'cdura') and self.cdura == 0:
            return Item.WRONG_CDUR
        if flyUpUtils.enableFlyUp() and BigWorld.component != 'client' and owner.flyUpLv < ID.data.get(self.id, {}).get('flyUpLvLimit', 0):
            return Item.WRONG_FLY_UP_LV
        if not self.extraCheck(owner):
            return Item.WRONG_EXTRA_CHECK
        return Item.EQUIPABLE

    def canEquipFishing(self, lv, where):
        if where != self.whereEquipFishing():
            return Item.WRONG_PLACE
        fishingLvReq = self.getFishingLvReq()
        if fishingLvReq:
            if lv < fishingLvReq:
                return Item.WRONG_FISHING_LV
        return Item.EQUIPABLE

    def canEquipExplore(self, owner, where):
        if where != self.whereEquipExplore():
            return Item.WRONG_PLACE
        scrollData = SLSED.data.get(self.id, {})
        if scrollData.get('xiangyaoExpNeed', 0) > owner.xiangyaoExp:
            return Item.WRONG_XIANGYAO_EXP_LESS
        if scrollData.get('xunbaoExpNeed', 0) > owner.xunbaoExp:
            return Item.WRONG_XUNBAO_EXP_LESS
        if scrollData.get('zhuizongExpNeed', 0) > owner.zhuizongExp:
            return Item.WRONG_ZHUIZONG_EXP_LESS
        if scrollData.get('exploreLvReq', 0) > owner.exploreLv:
            return Item.WRONG_EXPLORE_LV
        return Item.EQUIPABLE

    def canSplit(self, many):
        if self.cwrap < many:
            return False
        if self.cwrap == many:
            return True
        if self.hasLatch():
            return False
        if getattr(self, 'bWrap', True) == False:
            return False
        return True

    def getParentId(self):
        return self.parentId(self.id)

    def getAcExcitement(self):
        return ID.data.get(self.id, {}).get('acExcitement', 0)

    @property
    def enhanceType(self):
        enhType = ED.data.get(self.id, {}).get('enhanceType', 1)
        return enhType

    def canDisass(self):
        if not hasattr(self, 'quality'):
            return False
        parentId = self.getParentId()
        if (0,
         self.category,
         self.subcategory,
         self.quality) in IDD.data or (parentId,
         0,
         0,
         0) in IDD.data:
            return True
        return False

    def canDisassemble(self):
        if self.type != Item.BASETYPE_EQUIP:
            return False
        ed = ED.data.get(self.id, {})
        if not ed.get('canPeel', 0):
            return False
        canPeel = False
        if getattr(self, 'starExp', 0) > 0 or getattr(self, 'starLv') > 0:
            canPeel = True
        if getattr(self, 'maxStarLv', 0) > ed.get('peelStar', 0):
            canPeel = True
        curYangSlotNum = len([ sVal for sVal in getattr(self, 'yangSlots', []) if not sVal.isLocked() ])
        if curYangSlotNum > ed.get('peelYangSlot', 0):
            canPeel = True
        curYinSlotNum = len([ sVal for sVal in getattr(self, 'yinSlots', []) if not sVal.isLocked() ])
        if curYinSlotNum > ed.get('peelYinSlot', 0):
            canPeel = True
        if getattr(self, 'addedSuitId', None):
            canPeel = True
        return canPeel

    @staticmethod
    def canMerge(srcIt, dstIt):
        if srcIt.id != dstIt.id:
            return False
        if not srcIt.canWrap() or not dstIt.canWrap():
            return False
        if srcIt.bindType != dstIt.bindType:
            return False
        if srcIt.getTTLExpireTime() != dstIt.getTTLExpireTime():
            return False
        if getattr(srcIt, 'ownerGbId', 0) != getattr(dstIt, 'ownerGbId', 0):
            return False
        if getattr(srcIt, 'autoTakeToCrossServer', False) != getattr(dstIt, 'autoTakeToCrossServer', False):
            return False
        if getattr(srcIt, 'fromIntimacyGbId', 0) != getattr(dstIt, 'fromIntimacyGbId', 0):
            return False
        if getattr(srcIt, 'tCoinMail', 0) != getattr(dstIt, 'tCoinMail', 0):
            return False
        return True

    def hasMutableAttr(self):
        if self.getTTLExpireTime():
            return True
        if self.isEquip() or self.isLifeEquip() or self.isUnidentifiedEquip():
            return True
        if self.isRune() and self.mwrap == 1:
            return True
        if self.isHieroEquip():
            return True
        if self.isRuneEquip():
            return True
        if ID.data.get(self.id, {}).get('bindType') != getattr(self, 'bindType', -1):
            return True
        mutableAttrs = ('ownerGbId', 'cdura', 'ownershipPercent', 'timeLimit')
        for attr in mutableAttrs:
            if hasattr(self, attr):
                return True

        return False

    def _getRandPropsByIdAndQuality(self, randPropId, quality, extra = None):
        gamelog.debug('jorsef: _getRandPropsByIdAndQuality', self.id, randPropId, self.props)
        isRefine = extra.get('isRefine', False) if extra else False
        poolData = ERPD.data.get((randPropId, quality))
        if not poolData:
            return ({}, {})
        d = {}
        weight, data = [], []
        for pd in poolData:
            try:
                weight.append(pd['tableProb'])
                data.append(pd)
            except:
                continue

        if not data or not weight or len(data) != len(weight):
            return ({}, {})
        poolInfo = commcalc.weightingChoice(data, weight)
        result = []
        gamelog.debug('jorsef: get pool: ', poolInfo)
        for poolId, attrNum, way in poolInfo.get('pool', []):
            poolData = EPPD.data.get(poolId)
            if not poolData:
                gamelog.error('jorsef: ERROR, pool data not configured!!! %d %d' % (poolId, randPropId))
                continue
            poolData = [ d for d in poolData ]
            if len(poolData) == 0:
                gamelog.error('jorsef: ERROR: no value for pool data %d %d' % (poolId, randPropId))
                continue
            if way == gametypes.ITEM_ASSIGN_REPEAT:
                result.extend(self.randPool(poolData, attrNum, False, alreadyHave=[ propRef for propRef, _1, _2 in result ], extra=extra))
            else:
                result.extend(self.randPool(poolData, attrNum, True, alreadyHave=[ propRef for propRef, _1, _2 in result ], extra=extra))

        if poolInfo.has_key('propFix') and not isRefine:
            if not hasattr(self, 'propFix'):
                self.propFix = {}
            self.propFix.setdefault(self.EQUIP_PROP_FIX_BASE, []).append(poolInfo['propFix'])
            self.refreshPropsFix()
            gamelog.debug('add propFix', poolInfo['propFix'])
        if poolInfo.has_key('sEffectList') and not isRefine:
            sEffectList = poolInfo['sEffectList']
            effect = sample(sEffectList, 1)
            if effect and len(effect) > 0:
                self.gainEquipSpecialEffect(self.EQUIP_SE_BASE, effect[0])
                gamelog.debug('gain special effect', effect)
        return (result, poolInfo)

    def _randomQuality(self, ed = None):
        ed = ed or ED.data.get(self.id, {})
        if self.quality == 0:
            qualityProb = ed.get('qualityProb')
            if not qualityProb:
                return
            self.quality = commcalc.weightingChoice([ quality for quality, _ in qualityProb ], [ prop for _, prop in qualityProb ])

    def randomProperties(self, randPropId):
        if not randPropId:
            return
        result, randPropsDict = self._getRandPropsByIdAndQuality(randPropId, self.quality)
        self.inactiveStarLv += randPropsDict.get('inactiveStarLv', 0)
        self.rprops = []
        for res in result:
            self.rprops.append(res)

        self.__initEquipGemSlots(randPropsDict)

    def _refreshRefineSesEffect(self, newSesIds):
        self.ses[self.EQUIP_SE_MANUAL] = []
        self.refreshSeCache()
        for sesId in newSesIds:
            self.gainEquipSpecialEffect(self.EQUIP_SE_MANUAL, sesId)

    def recordRefineManual(self, owner, removedItems):
        if not hasattr(self, 'refineManual'):
            self.refineManual = {self.REFINE_MANUAL_RANDOM_PROP: copy.deepcopy(self.rprops),
             self.REFINE_MANUAL_REMOVE_ITEM: {},
             self.REFINE_MANUAL_REFINE_CNT: 0,
             self.REFINE_MANUAL_UNREFINE_CNT: 0,
             self.REFINE_MANUAL_GBID_FLAG: 0,
             self.REFINE_MANUAL_ROLENAME: '',
             self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT: 0}
            if hasattr(self, 'ses'):
                self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP] = copy.deepcopy(self.ses.get(self.EQUIP_SE_MANUAL, []))
        for _, _, item in removedItems:
            self.refineManual[self.REFINE_MANUAL_REMOVE_ITEM].setdefault(item.id, 0)
            self.refineManual[self.REFINE_MANUAL_REMOVE_ITEM][item.id] += item.cwrap

        self.refineManual[self.REFINE_MANUAL_REFINE_CNT] += 1
        cnt = self.refineManual[self.REFINE_MANUAL_REFINE_CNT]
        refineName = SCD.data.get('refineManualNameCnt', 100)
        if cnt >= refineName:
            self.refineManual[self.REFINE_MANUAL_GBID_FLAG] = owner.gbId
            self.refineManual[self.REFINE_MANUAL_ROLENAME] = owner.roleName
        refineCycle = SCD.data.get('refineManualCntCycle', {}).get(self.makeType, 150)
        specialCnt = self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT]
        if specialCnt >= refineCycle:
            self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT] = 1
            return True
        self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT] += 1
        return False

    def refineRandomProperties(self):
        mepd = MEPD.data.get(self.id, {})
        rPropId = self._getDataByMaketype(mepd['extraPools'])
        result, _ = self._getRandPropsByIdAndQuality(rPropId, self.quality, {'isRefine': True})
        idx = random.randint(0, len(self.rprops) - 1)
        tmpRes = copy.deepcopy(self.rprops)
        tmpRes[idx] = result[idx]
        self.rprops = copy.deepcopy(tmpRes)
        gamelog.debug('@hqx_refine_refineRandomProperties', rPropId, idx, result, self.rprops)
        return idx

    def replaceSpecialProperties(self, owner):
        sPropPools, sPropProbs = self._getRefineSpecialData()
        if not sPropPools:
            return
        res = []
        for sp in sPropProbs:
            if not sp[0]:
                continue
            res.append(sp)

        sPropIds = commcalc.weightingChoice(res, [ sp[1] for sp in res ])[0]
        self._replaceRefineSpecialProperties(owner, sPropIds)

    def refineSpecialProperties(self, owner):
        sPropPools, sPropProbs = self._getRefineSpecialData()
        if not sPropPools:
            return
        sPropIds = commcalc.weightingChoice(sPropProbs, [ sp[1] for sp in sPropProbs ])[0]
        gamelog.debug('@hqx_refine_refineSpecialProperties', sPropIds)
        if sPropIds:
            self.refineManual[Item.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT] = 1
        self._replaceRefineSpecialProperties(owner, sPropIds)

    def _getRefineSeList(self, poolId, sPropIds):
        sPropPools = self._getDataByMaketype(MEPD.data.get(self.id, {})['refineSpecialPools'])
        nowSes = getattr(self, 'ses', {}).get(self.EQUIP_SE_MANUAL, [])
        seList = MESPD.data.get(poolId, [])
        nameFlagList = []
        res = []
        if not nowSes:
            return [ se for se in seList ]
        if len(sPropIds) == len(nowSes) == 1:
            for sesId in nowSes:
                nameFlag = ESPD.data.get(sesId, {}).get('nameFlag', 0)
                if nameFlag:
                    nameFlagList.append(nameFlag)

        else:
            idx = sPropPools.index(poolId)
            if len(nowSes) > idx:
                sesId = nowSes[idx]
                nameFlag = ESPD.data.get(sesId, {}).get('nameFlag', 0)
                if nameFlag:
                    nameFlagList.append(nameFlag)
        for se in seList:
            specialEffect = se.get('specialEffect', 0)
            if ESPD.data.get(specialEffect, {}).get('nameFlag', 0) in nameFlagList:
                continue
            res.append(se)

        if not res:
            gameengine.reportCritical('@hqx_refine_getRefineSeList empty res %s %s %d' % (str(nowSes), str(nameFlagList), poolId))
        gamelog.debug('@hqx_refine_getRefineSeList', nowSes, nameFlagList, poolId, res)
        return res

    def _getRefineSpecialData(self):
        mepd = MEPD.data.get(self.id, {})
        sPropPools = self._getDataByMaketype(mepd['refineSpecialPools'])
        sPropProbs = self._getDataByMaketype(mepd['refineSpecialProbs'])
        if pow(2, len(sPropPools)) != len(sPropProbs) or len(sPropPools) > 2:
            gameengine.reportCritical('@hqx_refine_getRefineSpecialData data wrong !')
        return (sPropPools, sPropProbs)

    def _replaceRefineSpecialProperties(self, owner, sPropIds):
        if not sPropIds:
            return
        sPropPools = self._getDataByMaketype(MEPD.data.get(self.id, {})['refineSpecialPools'])
        propList = []
        for poolId in sPropIds:
            seList = self._getRefineSeList(poolId, sPropIds)
            if not seList:
                continue
            propData = commcalc.weightingChoice(seList, [ se['prob'] for se in seList ])
            propList.append(propData.get('specialEffect', 0))

        self.refineManual[self.REFINE_MANUAL_GBID_FLAG] = owner.gbId
        self.refineManual[self.REFINE_MANUAL_ROLENAME] = owner.roleName
        if not hasattr(self, 'ses'):
            self.ses = {}
        seManual = copy.deepcopy(self.ses.get(self.EQUIP_SE_MANUAL, []))
        gamelog.debug('@hqx_refine_replaceRefineSpecialProperties', owner.gbId, sPropIds, propList, seManual)
        if len(propList) >= len(seManual):
            self._refreshRefineSesEffect(propList)
        else:
            for idx, propId in enumerate(propList):
                if propId in seManual:
                    gameengine.reportCritical('@hqx_refine_replaceRefineSpecialProperties propId duplicated')
                    continue
                seIdx = sPropPools.index(sPropIds[idx])
                seManual[seIdx] = propId

            self._refreshRefineSesEffect(seManual)

    def unrefineManualProperties(self):
        if not hasattr(self, 'ses'):
            self.ses = {}
        oldR, oldS = copy.deepcopy(self.rprops), copy.deepcopy(self.ses.get(self.EQUIP_SE_MANUAL, []))
        gamelog.debug('@hqx_refine_unrefineManualProperties', self.rprops, self.ses, self.refineManual)
        self.rprops = copy.deepcopy(self.refineManual[self.REFINE_MANUAL_RANDOM_PROP])
        recordSes = self.refineManual.get(self.REFINE_MANUAL_SPECIAL_PROP, [])
        self._refreshRefineSesEffect(recordSes)
        return (oldR, oldS)

    def unrefineManualPropertiesGM(self, owner, unType):
        if not hasattr(self, 'ses'):
            self.ses = {}
        oldR, oldS = copy.deepcopy(self.rprops), copy.deepcopy(self.ses.get(self.EQUIP_SE_MANUAL, []))
        rProps = self.refineManual[self.REFINE_MANUAL_RANDOM_PROP]
        self.rprops = copy.deepcopy(rProps)
        recordSes = self.refineManual.get(self.REFINE_MANUAL_SPECIAL_PROP, [])
        self._refreshRefineSesEffect(recordSes)
        serverlog.genRefineManualEquipmentLog(owner, self, gameconst.REFINE_MANUAL_EQUIPMENT_OP_UNREFINE_GM, oldR, oldS)
        if unType == gametypes.GM_UNREFINE_TYPE_DEFAULT_RETURN:
            del self.refineManual
        elif unType == gametypes.GM_UNREFINE_TYPE_SPECIAL_RETURN:
            self.refineManual[Item.REFINE_MANUAL_REMOVE_ITEM] = {}
            unrefineCnt = self.refineManual.get(Item.REFINE_MANUAL_UNREFINE_CNT, 0)
            self.refineManual[Item.REFINE_MANUAL_REFINE_CNT] = unrefineCnt * SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
            self.refineManual[Item.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT] = 0
            if self.refineManual[Item.REFINE_MANUAL_REFINE_CNT] >= SCD.data.get('refineManualNameCnt', 100):
                self.refineManual[self.REFINE_MANUAL_GBID_FLAG] = owner.gbId
                self.refineManual[self.REFINE_MANUAL_ROLENAME] = owner.roleName
            else:
                self.refineManual[self.REFINE_MANUAL_GBID_FLAG] = 0
                self.refineManual[self.REFINE_MANUAL_ROLENAME] = ''
        elif unType == gametypes.GM_UNREFINE_TYPE_ALL_RETURN:
            backItem = self.refineManual.get(self.REFINE_MANUAL_REMOVE_ITEM, {})
            self.refineManualReturnMaterial(owner, backItem, SCD.data.get('gmManualEquipmentBackRate', 1), MTDD.data.GM_REFINE_MANUAL_EQUIPMENT_BACK_ITEM)
            del self.refineManual
        self.rarityMiracle = Item.EQUIP_NOT_DECIDED
        self.calcScores(calcRarityMiracle=True, extra={'owner': owner})
        gamelog.debug('@hqx_refine_unrefineManualPropertiesGM', self.rprops, self.ses, getattr(self, 'refineManual', None))

    def unbindRefineManual(self, refineManual, owner):
        self.refineManual = copy.deepcopy(refineManual)
        backItem = self.refineManual.get(self.REFINE_MANUAL_REMOVE_ITEM, {})
        unRefineCnt = self.refineManual.get(self.REFINE_MANUAL_UNREFINE_CNT, 0)
        specialFlag = self.refineManual.get(self.REFINE_MANUAL_UNREFINE_SPECIAL_FLAG, False)
        backId = SCD.data.get('refineManualEquipmentBindItemId', {}).get(self.makeType, 0)
        unrefineBase = SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
        refineItemCnt = MEPD.data.get(self.id, {}).get('refineItemCnt', 0)
        if specialFlag:
            backNum = sum(backItem.values()) - unRefineCnt * refineItemCnt * unrefineBase
        else:
            backNum = sum(backItem.values()) - (unRefineCnt + 1) * refineItemCnt * unrefineBase
        oldR, oldS = self.unrefineManualProperties()
        self.refineManualReturnMaterial(owner, {backId: backNum}, SCD.data.get('unbindManualEquipmentBackRate', 0.5), MTDD.data.UNBIND_REFINE_MANUAL_EQUIPMENT_BACK_ITEM)
        self.rarityMiracle = Item.EQUIP_NOT_DECIDED
        self.calcScores(calcRarityMiracle=True, extra={'owner': owner})
        serverlog.genRefineManualEquipmentLog(owner, self, gameconst.REFINE_MANUAL_EQUIPMENT_OP_UNBIND, oldR, oldS)
        del self.refineManual

    def disassembleRefineManual(self, owner):
        if not hasattr(self, 'refineManual'):
            return
        if not hasattr(self, 'ses'):
            self.ses = {}
        oldR, oldS = copy.deepcopy(self.rprops), copy.deepcopy(self.ses.get(self.EQUIP_SE_MANUAL, []))
        backItem = self.refineManual.get(self.REFINE_MANUAL_REMOVE_ITEM, {})
        backId = SCD.data.get('refineManualEquipmentBindItemId', {}).get(self.makeType, 0)
        unRefineCnt = self.refineManual.get(self.REFINE_MANUAL_UNREFINE_CNT, 0)
        unrefineBase = SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
        backSum = sum(backItem.values()) - unRefineCnt * MEPD.data.get(self.id, {}).get('refineItemCnt', 0) * unrefineBase
        returnItem = {backId: backSum} if self.isForeverBind() else backItem
        self.refineManualReturnMaterial(owner, returnItem, SCD.data.get('disassembleManualEquipmentBackRate', 0.5), MTDD.data.DISASSEMBLE_REFINE_MANUAL_EQUIPMENT_BACK_ITEM)
        serverlog.genRefineManualEquipmentLog(owner, self, gameconst.REFINE_MANUAL_EQUIPMENT_OP_DISASSEMBLE, oldR, oldS)

    def refineManualReturnMaterial(self, owner, backItem, backRate, mtdd):
        if len(backItem) > 1:
            gameengine.reportCritical('@hqx_refine_refineManualReturnMaterial_return_item > 1 %d %s' % (self.id, str(backItem)))
        import mail
        mailItem = []
        for itemId, itemNum in backItem.iteritems():
            if itemNum <= 0:
                continue
            itemNum = int(itemNum * backRate)
            mwrap = ID.data.get(itemId, {}).get('mwrap', 1)
            while itemNum > mwrap:
                mailItem.append((itemId, mwrap))
                itemNum -= mwrap

            if itemNum > 0:
                mailItem.append((itemId, itemNum))

        if mailItem:
            mail.sendSysMailEx(owner.gbId, owner.roleName, mtdd, itemBonus=mailItem, logSrc=LSDD.data.LOG_SRC_REFINE_MANUAL_EQUIPMENT)

    def createUpgradeEquip(self, coreEquip, upgradeData = {}):
        self.bindItem()
        if hasattr(coreEquip, 'makeType'):
            self.makeType = getattr(coreEquip, 'makeType', 0)
        if hasattr(coreEquip, '_consignVendor'):
            self._consignVendor = getattr(coreEquip, '_consignVendor', '')
        if hasattr(coreEquip, 'makerRole'):
            self.makerRole = getattr(coreEquip, 'makerRole', '')
        if hasattr(coreEquip, 'makerGbId'):
            self.makerGbId = getattr(coreEquip, 'makerGbId', 0)
        if hasattr(coreEquip, 'signCode'):
            self.signCode = getattr(coreEquip, 'signCode', 0)
        if hasattr(coreEquip, 'signName'):
            self.signName = getattr(coreEquip, 'signName', '')
        if hasattr(coreEquip, 'yangSlots'):
            self.yangSlots = coreEquip.yangSlots
        if hasattr(coreEquip, 'yinSlots'):
            self.yinSlots = coreEquip.yinSlots
        self.starLv = 0
        self.activeStarLv = 0
        self.inactiveStarLv = getattr(coreEquip, 'inactiveStarLv', 0)
        self.starExp = 0
        if hasattr(coreEquip, 'maxStarLv'):
            self.maxStarLv = getattr(coreEquip, 'maxStarLv', 0)
        if hasattr(coreEquip, 'enhLv'):
            self.enhLv = getattr(coreEquip, 'enhLv', 0)
        if hasattr(coreEquip, 'starpropFix'):
            self.starpropFix = getattr(coreEquip, 'starpropFix', {})
        if hasattr(coreEquip, 'seCache'):
            self.seCache = getattr(coreEquip, 'seCache', {})
        if hasattr(coreEquip, 'enhanceRefining'):
            self.enhanceRefining = getattr(coreEquip, 'enhanceRefining', {})
        if hasattr(coreEquip, 'dyeListScheme'):
            self.dyeListScheme = getattr(coreEquip, 'dyeListScheme', {})
        if hasattr(coreEquip, 'enhJuexingData'):
            self.enhJuexingData = getattr(coreEquip, 'enhJuexingData', {})
        if hasattr(coreEquip, 'quality'):
            self.quality = getattr(coreEquip, 'quality', 0)
        if hasattr(coreEquip, 'dyeCurrIdx'):
            self.dyeCurrIdx = getattr(coreEquip, 'dyeCurrIdx', 0)
        if hasattr(coreEquip, 'cdura'):
            self.cdura = getattr(coreEquip, 'cdura', 0)
        if hasattr(coreEquip, 'dyeMaterialsScheme'):
            self.dyeMaterialsScheme = getattr(coreEquip, 'dyeMaterialsScheme', {})
        if hasattr(coreEquip, 'tempJXAlldata'):
            self.tempJXAlldata = coreEquip.tempJXAlldata
        if hasattr(coreEquip, 'tempJXStrength'):
            self.tempJXStrength = coreEquip.tempJXStrength
        if hasattr(coreEquip, 'ses'):
            self.ses = {}
            for key, val in getattr(coreEquip, 'ses', {}).iteritems():
                if key == self.EQUIP_SE_STARLV:
                    continue
                if key == self.EQUIP_SE_MANUAL:
                    self.ses[key] = []
                    for i in val:
                        self.ses[key].append(ESPD.data.get(i, {}).get('upgradeManualIndex', 0) or i)

                    continue
                self.ses[key] = val

        if hasattr(coreEquip, 'refineManual'):
            self.refineManual = {}
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_RANDOM_PROP):
                oldProps = []
                for val in coreEquip.refineManual[self.REFINE_MANUAL_RANDOM_PROP]:
                    oldProps.append((val[0], val[1], val[2] * (upgradeData.get('extraPropRatio', 0.06) + 1)))

                self.refineManual[self.REFINE_MANUAL_RANDOM_PROP] = oldProps
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_SPECIAL_PROP):
                self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP] = coreEquip.refineManual[self.REFINE_MANUAL_SPECIAL_PROP]
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_REFINE_CNT):
                self.refineManual[self.REFINE_MANUAL_REFINE_CNT] = int((coreEquip.refineManual[self.REFINE_MANUAL_REFINE_CNT] - coreEquip.refineManual[self.REFINE_MANUAL_UNREFINE_CNT] * 100) * MEPD.data.get(coreEquip.id).get('refineItemCnt', 0) / MEPD.data.get(self.id).get('refineItemCnt', 0))
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_REMOVE_ITEM):
                self.refineManual[self.REFINE_MANUAL_REMOVE_ITEM] = coreEquip.refineManual[self.REFINE_MANUAL_REMOVE_ITEM]
            self.refineManual[self.REFINE_MANUAL_UNREFINE_CNT] = 0
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_GBID_FLAG):
                self.refineManual[self.REFINE_MANUAL_GBID_FLAG] = coreEquip.refineManual[self.REFINE_MANUAL_GBID_FLAG]
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_ROLENAME):
                self.refineManual[self.REFINE_MANUAL_ROLENAME] = coreEquip.refineManual[self.REFINE_MANUAL_ROLENAME]
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT):
                self.refineManual[self.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT] = 0
            if coreEquip.refineManual.has_key(self.REFINE_MANUAL_UNREFINE_SPECIAL_FLAG):
                self.refineManual[self.REFINE_MANUAL_UNREFINE_SPECIAL_FLAG] = coreEquip.refineManual[self.REFINE_MANUAL_UNREFINE_SPECIAL_FLAG]
        if getattr(coreEquip, 'prefixInfo', ()):
            dataInfo = EPFPD.data.get(coreEquip.prefixInfo[0])
            for dataValue in dataInfo:
                if dataValue.get('id', 0) == coreEquip.prefixInfo[1]:
                    self.prefixInfo = dataValue.get('upgradeManualIndex', coreEquip.prefixInfo)
                    break

        if getattr(coreEquip, 'newPrefixInfo', ()):
            dataInfo = EPFPD.data.get(coreEquip.newPrefixInfo[0])
            for dataValue in dataInfo:
                if dataValue.get('id', 0) == coreEquip.newPrefixInfo[1]:
                    newPrefixInfo = dataValue.get('upgradeManualIndex', 0)
                    if not newPrefixInfo:
                        newPrefixInfo = coreEquip.newPrefixInfo
                    else:
                        newPrefixInfo = list(newPrefixInfo)
                        newPrefixInfo.append(coreEquip.newPrefixInfo[2])
                        newPrefixInfo = tuple(newPrefixInfo)
                    self.newPrefixInfo = newPrefixInfo
                    break

        if getattr(coreEquip, 'preprops', ()):
            dataInfo = EPFPD.data.get(self.prefixInfo[0])
            for dataValue in dataInfo:
                if dataValue.get('id', 0) == self.prefixInfo[1]:
                    self.preprops = dataValue.get('props', coreEquip.preprops)
                    break

        gamelog.debug('@lyh creatUpgradeEquip self.preprops', self.preprops)
        if getattr(coreEquip, 'manualEquipStarInfo', {}):
            dataInfo = MESTARPD.data.get(coreEquip.manualEquipStarInfo[0])
            for dataValue in dataInfo:
                if dataValue['id'] == coreEquip.manualEquipStarInfo[1]:
                    self.manualEquipStarInfo = dataValue.get('upgradeManualIndex', coreEquip.manualEquipStarInfo)
                    break

        self.unbindTimes = ED.data.get(self.id, {}).get('unbindTimes', 3)
        props = []
        for val in coreEquip.props:
            props.append((val[0], val[1], math.floor(val[2] * (upgradeData.get('basePropRatio', 0.18) + 1))))

        self.props = props
        rprops = []
        for val in coreEquip.rprops:
            rprops.append((val[0], val[1], val[2] * (upgradeData.get('extraPropRatio', 0.06) + 1)))

        self.rprops = rprops
        self.extraProps = getattr(coreEquip, 'extraProps', [])
        self.calcYapPeiScore()
        self.calcScores()
        self.manaulEquip = True
        self._mailItemId = getattr(coreEquip, '_mailItemId', [])
        data = self._getRandomEquipStarPropData()
        starPropFixScore = data.get('starPropFixScore', 0)
        allStarSEffectScore = starPropFixScore + ESPD.data.get(data.get('starSEffect', 0), {}).get('equipScore', 0)
        initScoreWithAllStar = self.initScore + allStarSEffectScore
        self.rarityMiracle = self.calcRarityMiracleEquip(initScoreWithAllStar)
        self.dumpAfterIdentify = zlib.compress(dumps(utils.getItemSaveData(self)))
        return self

    def _expandDict(self, d1, d2):
        for key, value in d2.items():
            if d1.has_key(key):
                d1[key] += value
            else:
                d1[key] = value

        return d1

    def _genRefineRandPropVal(self, amin, amax, refineValRate):
        weight, data = [], []
        for idx, val in enumerate(refineValRate):
            weight.append(val)
            data.append(idx)

        finalIdx = commcalc.weightingChoice(data, weight)
        totalLen = len(refineValRate)
        delta = float(amax - amin) / totalLen
        amin += finalIdx * delta
        amax -= (totalLen - finalIdx - 1) * delta
        finalVal = uniform(amin, amax)
        return finalVal

    def _getRandPropFromPoolData(self, obj, refineValRate, extra = None):
        aid, atype, transType, amax, amin, pmin, pmax = obj
        isRefine = extra.get('isRefine', False) if extra else False
        if transType != gametypes.PROPERTY_RAND_ABS:
            fd = FSD.data.get(transType)
            if not fd:
                return None
            formula = fd.get('formula')
            if not formula:
                gamelog.error('jorsef: ERROR!!! formula not specified, %d' % transType)
                return None
            amin = self.evalValue(transType, pmin)
            amax = self.evalValue(transType, pmax)
        num = uniform(amin, amax) if not isRefine else self._genRefineRandPropVal(amin, amax, refineValRate)
        return (aid, atype, num)

    def _genRefineRandPropValRange(self, poolData):
        weight, data = [], []
        for pd in poolData:
            weight.append(pd['refineProb'])
            data.append(pd)

        poolInfo = commcalc.weightingChoice(data, weight)
        return poolInfo

    def randPool(self, poolData, attrNum, delSelected, alreadyHave, extra = None):
        result = []
        isRefine = extra.get('isRefine', False) if extra else False
        for i in range(attrNum):
            if not poolData or len(poolData) == 0:
                break
            choiceData = choice(poolData) if not isRefine else self._genRefineRandPropValRange(poolData)
            obj = choiceData['value']
            rProp = self._getRandPropFromPoolData(obj, choiceData.get('refineValRate', (10, 10, 25, 55)), extra=extra)
            if rProp is None:
                return []
            if alreadyHave and ED.data.get(self.id, {}).has_key('rarePropsRerandomType'):
                if rProp[0] in SCD.data.get('equipRarePropsList', ()):
                    cnt = len([ propRef for propRef in alreadyHave if propRef == rProp[0] ]) + 1
                    reRandprob = ED.data[self.id]['rarePropsRerandomType'].get(cnt, 0)
                    if reRandprob > 0:
                        r = random.randint(*const.RANDOM_RATE_BASE_10K)
                        if reRandprob > r / 10000.0:
                            gamelog.debug('@smj randPool reRandom', rProp[0], i, r, cnt)
                            choiceData = choice(poolData) if not isRefine else self._genRefineRandPropValRange(poolData)
                            obj = choiceData['value']
                            rProp = self._getRandPropFromPoolData(obj, choiceData.get('refineValRate', (10, 10, 25, 55)), extra=extra)
                            if rProp is None:
                                return []
            result.append(rProp)
            alreadyHave.append(rProp[0])
            if delSelected:
                poolData.remove(choiceData)

        gamelog.debug('jorsef: randPool result: ', result)
        return result

    def getIcon(self):
        iconId = ID.data.get(self.id, {})['icon']
        return iconId

    def evalValue(self, formulaId, params, extra = None, postExtra = None):
        vars = {}
        extra and vars.update(extra)
        vars['itemLv'] = getattr(self, 'itemLv', 1)
        vars['quality'] = getattr(self, 'quality', 1)
        vars['starLv'] = getattr(self, 'starLv', 0)
        vars['maxStarLv'] = getattr(self, 'maxStarLv', 0)
        for i in range(len(params)):
            param = params[i]
            vars['p%d' % (i + 1,)] = param

        postExtra and vars.update(postExtra)
        return calcFormulaById(formulaId, vars)

    def enhanceItem(self, owner, enhanProb):
        if not hasattr(self, 'enhLv'):
            self.enhLv = 0
        if not hasattr(self, 'enhJuexingData'):
            self.enhJuexingData = {}
        if not hasattr(self, 'enhanceRefining'):
            self.enhanceRefining = {}
        if self.enhLv >= self.getMaxEnhLv(owner):
            return 0
        oldLv = self.enhLv
        self.enhLv = limit(self.enhLv + 1, 0, self.getMaxEnhLv(owner))
        if self.enhLv not in getattr(self, 'enhJuexingData', {}):
            self._enhanceJuexing(owner, self.enhLv)
        self._setEquipRefining(owner, enhanProb, self.enhLv)
        if commcalc.enableEquipChangeJuexingStrength() and self.enhLv == SCD.data.get('enhJuexingStrengthEnhLvLimit', const.EQUIP_ENH_JUEXING_STRENGTH_LV_LIMIT) and flyUpUtils.enableFlyUp() and owner.flyUpLv >= FUCD.data.get('flyUpEnhanceJuexingStrengthLv', 0):
            self._enhanceJuexingStrength(owner, self.enhLv)
        return self.enhLv - oldLv

    def _inheritSign(self, fromEquip):
        if not self.isCanSign():
            return
        if hasattr(fromEquip, 'signCode') and hasattr(fromEquip, 'signName'):
            self.signCode = fromEquip.signCode
            self.signName = fromEquip.signName

    def _inheritEnhance(self, fromEquip, inheritJuexing = False):
        if not self.canEnhance():
            return
        if not hasattr(fromEquip, 'enhLv'):
            return
        self.enhLv = fromEquip.enhLv
        if hasattr(fromEquip, 'enhanceRefining'):
            self.enhanceRefining = {}
            for enhLv in xrange(1, self.enhLv + 1):
                if fromEquip.enhanceRefining.has_key(enhLv):
                    self.enhanceRefining[enhLv] = fromEquip.enhanceRefining[enhLv]

        if inheritJuexing and hasattr(fromEquip, 'enhJuexingData'):
            self.enhJuexingData = {}
            for enhLv in xrange(1, self.enhLv + 1):
                if fromEquip.enhJuexingData.has_key(enhLv):
                    self.enhJuexingData[enhLv] = fromEquip.enhJuexingData[enhLv]

    def canEnhance(self):
        if not hasattr(self, 'maxEnhlv'):
            return False
        return self.maxEnhlv != 0

    def _calcEquipRefining(self, enhProb, probInfo):
        fId = probInfo[0]
        params = probInfo[1:]
        vars = {}
        for i in range(len(params)):
            param = params[i]
            vars['p%d' % (i + 1,)] = param

        vars['prob'] = enhProb
        return calcFormulaById(fId, vars)

    def _setEquipRefining(self, owner, enhProb, enhLv, reEnhance = False):
        rd = EERD.data.get(enhLv)
        if not rd:
            return 0
        refiningEffects = rd.get('enhEffects', ())
        if not refiningEffects:
            return 0
        if not hasattr(self, 'enhanceRefining'):
            self.enhanceRefining = {}
        refiningList = []
        totalProb = 0
        for refining, probInfo in refiningEffects:
            prob = self._calcEquipRefining(enhProb, probInfo)
            refiningList.append((refining, prob))
            totalProb += prob

        r = uniform(0, totalProb)
        curProb = 0
        tRefining = 0
        for refining, prob in refiningList:
            curProb += prob
            if r < curProb:
                if reEnhance:
                    res = max(self.enhanceRefining.get(enhLv, 0), refining)
                else:
                    res = refining
                self.enhanceRefining[enhLv] = res
                tRefining = refining
                break

        return tRefining

    def getEnhaceJuexingDataWithItem(self, idx, enhLv, itemId):
        juexingDataList = utils.getEquipEnhJuexingData(self.equipType, self.equipSType, enhLv, self.enhanceType)
        if not juexingDataList:
            return []
        itemData = EEICD.data.get(itemId, {})
        enhLvWhiteList = itemData.get('whiteList', [])
        if not enhLvWhiteList:
            return
        whiteList = enhLvWhiteList[idx]
        jdData = []
        jdProbability = []
        for jd in juexingDataList:
            if jd['id'] in whiteList:
                jdData.append(jd)
                jdProbability.append(jd['probability'])

        juexingData = commcalc.weightingChoice(jdData, jdProbability)
        enhLvRate = itemData.get('prop', [])
        if not enhLvRate:
            return
        propRate = enhLvRate[idx]
        res = []
        for propRefId, propType, minVal, maxVal, steps in juexingData.get('enhanceJuexingProps', ()):
            if minVal > maxVal:
                continue
            idx = commcalc.weightingChoiceIndex(propRate)
            val = minVal + (maxVal - minVal) * idx / float(len(propRate) - 1)
            res.append((propRefId, propType, val))

        return res

    def getEnhaceJuexingData(self, enhLv):
        juexingDataList = utils.getEquipEnhJuexingData(self.equipType, self.equipSType, enhLv, self.enhanceType)
        if not juexingDataList:
            return []
        juexingData = commcalc.weightingChoice(juexingDataList, [ jd['probability'] for jd in juexingDataList ])
        res = []
        for propRefId, propType, minVal, maxVal, steps in juexingData.get('enhanceJuexingProps', ()):
            if minVal > maxVal:
                continue
            if enhLv >= SCD.data.get('enhJuexingStrengthEnhLvLimit', const.EQUIP_ENH_JUEXING_STRENGTH_LV_LIMIT):
                enhJuexingSpecialRate = SCD.data.get('enhJuexingSpecialRate', ())
                r = randint(*const.RANDOM_RATE_BASE_10K)
                curRate = 0
                for idx, enhRate in enumerate(enhJuexingSpecialRate):
                    curRate += enhRate
                    if curRate > r:
                        val = minVal + (maxVal - minVal) * idx / (len(enhJuexingSpecialRate) - 1)
                        res.append((propRefId, propType, val))
                        break

                continue
            val = minVal + (maxVal - minVal) * randint(0, steps) / float(steps)
            res.append((propRefId, propType, val))

        return res

    def _enhanceJuexing(self, owner, enhLv):
        if not hasattr(self, 'enhJuexingData'):
            self.enhJuexingData = {}
        if self.isJuexing() and enhLv in self.enhJuexingData:
            gamelog.error('@zs: equip juexing', owner.id, owner.gbId, self.id, self.enhJuexingData, enhLv)
            return False
        self.enhJuexingData[enhLv] = self.getEnhaceJuexingData(enhLv)
        return True

    def _enhanceJuexingStrength(self, owner, enhLv):
        if not hasattr(self, 'enhJuexingAddRatio'):
            self.enhJuexingAddRatio = {}
        strengthLvLimit = SCD.data.get('enhJuexingStrengthEnhLvLimit', const.EQUIP_ENH_JUEXING_STRENGTH_LV_LIMIT)
        minRatio, maxRatio = SCD.data.get('enhJuexingStrengthRange', (5, 25))
        for enhLv, val in self.enhJuexingData.iteritems():
            if not val:
                continue
            if enhLv >= strengthLvLimit:
                continue
            ratio = random.randint(minRatio, maxRatio)
            self.enhJuexingAddRatio[enhLv] = round(ratio / 100.0, 2)

        gamelog.debug('@hqx_enh _enhanceJuexingStrength', self.enhJuexingAddRatio)

    def getEquipRefiningStar(self):
        if not self.isEquip():
            return 0
        return 1

    def _resetEnhanceJuexing(self, owner, juexingEnhLv):
        if not self.isJuexing() or self.getJuexingLv(juexingEnhLv) < 0:
            return False
        return not not self.enhJuexingData.pop(juexingEnhLv, [])

    def isJuexing(self):
        return hasattr(self, 'enhJuexingData') and len(self.enhJuexingData)

    def getJuexingLv(self, juexingEnhLv):
        if not self.isJuexing() or juexingEnhLv not in self.enhJuexingData:
            return -1
        juexingEnhLvs = sorted(self.enhJuexingData.keys())
        return juexingEnhLvs.index(juexingEnhLv) + 1

    def hyperlink(self, stamp = None):
        if not stamp:
            stamp = Netease.getNUID()
        gameengine.getGlobalBase('ItemStub').generateKey(stamp, self.deepcopy())
        codes = utils.uint64ToStr(stamp)
        color = FCD.data['item', self.quality]['color']
        itemName = self.name
        if hasattr(self, 'prefixInfo'):
            for prefixItem in EPFPD.data.get(self.prefixInfo[0], []):
                if prefixItem['id'] == self.prefixInfo[1]:
                    if utils.isInternationalVersion():
                        itemName = self.name + prefixItem['name']
                    else:
                        itemName = prefixItem['name'] + self.name
                    break

        link = '#[' + codes + ']' + color + '[' + itemName + ']#n#[0]'
        return link

    def getNameSuffix(self):
        s = ''
        if hasattr(self, '_shihunRole'):
            s += '[%s]' % self._shihunRole
        return s

    def getExtraLinkInfo(self):
        s = ''
        if hasattr(self, '_shihunRole'):
            s += ':_shihunRole:' + self._shihunRole + ':_shihunEquip:' + str(self._shihunEquip)
        return s

    def _checkEquipDuraValid(self):
        if not hasattr(self, 'initMaxDura') or self.initMaxDura == const.EQUIP_DURA_NONE or not self.initMaxDura:
            return False
        return True

    def reduceDurability(self, many):
        if not self._checkEquipDuraValid():
            return
        if hasattr(self, 'seCache') and self.seCache.has_key('durabilityParam'):
            many = max(0, many * (1 - self.seCache['durabilityParam']))
        self.cdura = limit(self.cdura - many, 0.0, self.initMaxDura)

    def reduceLifeEquipDurability(self, many):
        if not self._checkEquipDuraValid():
            return False
        self.cdura = limit(self.cdura - many, 0.0, self.initMaxDura)
        return True

    def repair(self):
        if not self._checkEquipDuraValid():
            return
        self.cdura = self.initMaxDura

    def repairLifeEquip(self, initMaxDura):
        if not self._checkEquipDuraValid():
            return False
        self.cdura = initMaxDura
        return True

    def repairCost(self, school, lv):
        eqData = EWRD.data.get((self.equipType, self.equipSType))
        if not gameconfigCommon.enableNewDurability():
            repairArg = eqData.get('repairArg', 1)
            arg = 2
            if repairArg > arg:
                repairArg = 0.2
            cost = (self._duraCalcValue(self.initMaxDura) - self._duraCalcValue(self.cdura)) * self.itemLv * self.quality * repairArg * max(0.05, min((lv - 35) * 0.2, 1))
        else:
            repairArg = eqData.get('repairArg', 1)
            if BigWorld.component == 'client':
                from data import formula_client_data as FCDD
                costFormula = FCDD.data.get(repairArg, {}).get('formula', None)
            else:
                costFormula = FSD.data.get(repairArg, {}).get('formula', None)
            if not costFormula:
                gameengine.reportCritical('czf formula_server_data not {} formula'.format(repairArg))
                cost = 0
            else:
                arg = costFormula({'itemLv': int(self.itemLv)})
                cost = (self._duraCalcValue(self.initMaxDura) - self._duraCalcValue(self.cdura)) * self.itemLv * self.quality * arg * max(0.05, min((lv - 35) * 0.2, 1))
        if cost > 0:
            cost = max(1, int(round(cost)))
        else:
            cost = 0
        return cost

    def canRepair(self):
        if self.isExpireTTL():
            return False
        if not hasattr(self, 'cdura'):
            return False
        if not hasattr(self, 'initMaxDura'):
            return False
        if not self._checkEquipDuraValid():
            return False
        return utils.getItemNoRepair(ID.data.get(self.id, {})) == 0

    def canBooth(self):
        itemData = ID.data.get(self.id, {})
        if itemData.get('ttl', 0):
            return False
        return utils.getItemNoBooth(ID.data.get(self.id, {})) == 0

    def canBoothBuy(self):
        return self.canBooth() and utils.getItemNoBoothBuy(ID.data.get(self.id, {})) == 0

    def canBuyBack(self, shopType):
        data = ID.data.get(self.id, {})
        noBuyBack = data.get('noBuyBack', 0)
        if not noBuyBack:
            return True
        if shopType == const.SHOP_TYPE_COMMON:
            return noBuyBack not in (const.ITEM_BUY_BACK_FORBIDDEN_ALL, const.ITEM_BUY_BACK_FORBIDDEN_PRICE)
        if shopType == const.SHOP_TYPE_COMPOSITE:
            if data.get('famePrice'):
                return noBuyBack not in (const.ITEM_BUY_BACK_FORBIDDEN_ALL, const.ITEM_BUY_BACK_FORBIDDEN_FAME_PRICE)
            else:
                return noBuyBack not in (const.ITEM_BUY_BACK_FORBIDDEN_ALL, const.ITEM_BUY_BACK_FORBIDDEN_PRICE)
        else:
            return False

    def canReturnToShop(self):
        return hasattr(self, 'compositeShopInfo') and time.time() - self.compositeShopInfo[0] < SCD.data.get('timeToReturnShop', 600)

    def delCompositeShopInfo(self, owner, resKind, page, pos, bGroupTrade = True):
        if hasattr(self, 'compositeShopInfo'):
            delattr(self, 'compositeShopInfo')
            owner.client.delCompositeShopInfo(resKind, page, pos)
        if bGroupTrade:
            self.setGroupTrade(False)

    def delCompositeShopInfoOnly(self):
        if hasattr(self, 'compositeShopInfo'):
            delattr(self, 'compositeShopInfo')

    def canSell(self, shopType = 0, compositeShopId = 0):
        if self.isRuneHasRuneData():
            return False
        data = ID.data.get(self.id, {})
        if shopType == const.SHOP_TYPE_COMMON:
            return not utils.getItemNoSellForPrice(data)
        if shopType == const.SHOP_TYPE_COMPOSITE:
            if compositeShopId and self.canSellNormalToCompositeShop(compositeShopId):
                return True
            elif data.get('famePrice'):
                return not utils.getItemNoSellForFamePrice(data)
            else:
                return not utils.getItemNoSellForPrice(data)
        else:
            return not utils.getItemNoSell(data)

    def canSellToCompositeShop(self):
        return ID.data.get(self.id, {}).has_key('famePrice')

    def canSellToCompositeShopId(self, compositeShopId):
        famePriceDict = ID.data.get(self.id, {}).get('famePrice', {})
        for shopIdTuple in famePriceDict:
            if compositeShopId in shopIdTuple:
                return (True, famePriceDict[shopIdTuple])

        return (False, ())

    def canSellNormalToCompositeShop(self, compositeShopId):
        if not utils.isSellNormalToCompositeShopOn():
            return False
        if not CSD.data.has_key(compositeShopId):
            return False
        if not CSD.data[compositeShopId].get('canBuyNormalItem', 0):
            return False
        if utils.getItemNoSellForPrice(ID.data.get(self.id, {})):
            return False
        return True

    def canSellToPurchaseShop(self):
        data = ID.data.get(self.id, {})
        return data.has_key('famePrice') or data.has_key('buybackFamePrice')

    def canSellToPurchaseShopId(self, compositeShopId):
        data = ID.data.get(self.id, {})
        famePriceDict = data.get('buybackFamePrice', {}) or data.get('famePrice', {})
        for shopIdTuple in famePriceDict:
            if compositeShopId in shopIdTuple:
                return (True, famePriceDict[shopIdTuple])

        return (False, ())

    def sellWithConfirm(self):
        data = ID.data.get(self.id, {})
        return not data.get('noSellConfirm', 0)

    def _duraCalcValue(self, value):
        return int(math.ceil(value))

    def needRepair(self):
        if not self._checkEquipDuraValid():
            return False
        return self._duraCalcValue(self.cdura) < self._duraCalcValue(self.initMaxDura)

    def updateAttribute(self, props, newAttr = True):
        for name, newVal in props.iteritems():
            if newVal == None:
                try:
                    delattr(self, name)
                except AttributeError:
                    pass

            elif hasattr(self, name) or newAttr:
                setattr(self, name, newVal)

    def calcScores(self, calcRarityMiracle = False, extra = None):
        if utils.getCommonGameConfig('enableStatsCombatScoreType'):
            self._calcScoresWithType(calcRarityMiracle, extra)
        else:
            self._calcScores(calcRarityMiracle, extra)

    def _calcScores(self, calcRarityMiracle = False, extra = None):
        if self.isYaoPei():
            return
        owner = extra.get('owner', None) if extra else None
        initScore = 0
        rprop = self.rprops if hasattr(self, 'rprops') else []
        orderFactor = EOFD.data.get(self.order, {}).get('factor', 1.0)
        refiningFactor = 0
        for eLv, v in getattr(self, 'enhanceRefining', {}).iteritems():
            if eLv <= min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner)):
                refiningFactor += v

        enhanceScore = 0
        juexingScore = 0
        enhanceData = EEPD.data.get((self.equipType, self.equipSType, self.enhanceType), {})
        if enhanceData.has_key('enhScore'):
            fVars = {'enhanceRefining': refiningFactor,
             'orderFactor': orderFactor,
             'enhanceLv': min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner))}
            enhanceScore = calcValueByFormulaData(enhanceData['enhScore'], fVars)
        try:
            enhJuexingAddRatio = getattr(self, 'enhJuexingAddRatio', {})
            for eLv, juexingPropList in getattr(self, 'enhJuexingData', {}).iteritems():
                if eLv > min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner)):
                    continue
                addRatio = enhJuexingAddRatio.get(eLv, 0)
                juexingDataList = utils.getEquipEnhJuexingPropData(self.equipType, self.equipSType, eLv, self.enhanceType)
                for pid, ptp, value in juexingPropList:
                    if pid not in juexingDataList:
                        continue
                    data = PRD.data.get(pid)
                    if not data:
                        continue
                    juexingScoreFormula = data.get('juexingScore')
                    if not juexingScoreFormula:
                        continue
                    formulaId, formulaParams = juexingScoreFormula[0], juexingScoreFormula[1:]
                    value *= 1 + addRatio
                    juexingPropScore = self.evalValue(formulaId, formulaParams, {'val': value,
                     'enhLv': eLv})
                    juexingScore += juexingPropScore

        except Exception as e:
            gamelog.error('calc juexing score error!', self.id, e.message)

        seScore = 0
        for seType, seList in getattr(self, 'ses', {}).iteritems():
            seScoreVal = sum([ ESPD.data.get(seId, {}).get('equipScore', 0) for seId in seList ])
            seScore += seScoreVal
            if seType != self.EQUIP_SE_STARLV:
                initScore += seScoreVal

        starFactor = ESFCD.data.get(getattr(self, 'starLv', -1), {}).get('factor', 1.0)
        qualityFactor = EQFD.data.get(self.quality, {}).get('factor', 1.0)
        prefixScore = 0
        if hasattr(self, 'prefixInfo'):
            preGroupId, prefixId = self.prefixInfo
            preGroupData = EPFPD.data.get(preGroupId, [])
            for prefixData in preGroupData:
                if prefixData.get('id') == prefixId:
                    prefixScore = prefixData.get('prefixScore', 0)
                    break

        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            if isManual:
                epd = MEPD.data.get(self.id, {})
            else:
                epd = XEPD.data.get(self.id, {})
            preGroupList = epd.get('preGroupList', ())
        else:
            ed = ED.data.get(self.id, {})
            preGroupList = ed.get('preGroupList', ())
        minPreFixScore = 0
        for gid, _ in preGroupList:
            pgData = EPFPD.data.get(gid, [])
            for pfData in pgData:
                if pfData['lvStart'] > self.itemLv or pfData['lvEnd'] < self.itemLv:
                    continue
                if pfData.has_key('prefixScore'):
                    minPreFixScore = min(minPreFixScore, pfData['prefixScore']) if minPreFixScore else pfData['prefixScore']

        initScore += minPreFixScore * qualityFactor
        prefixScore *= starFactor * qualityFactor
        d = defaultdict(lambda : 0)
        for pid, ptp, value in rprop:
            d[pid, ptp] += value

        rPropScore = 0
        for key, value in d.iteritems():
            pid, ptp = key
            data = PRD.data.get(pid)
            if not data:
                continue
            if ptp == gametypes.DATA_TYPE_NUM:
                coeff = data.get('scoreCoeffNum', 0)
            else:
                coeff = data.get('scoreCoeffPercent', 0)
            gamelog.debug('jorsef: score temp: ', pid, ptp, value, coeff)
            rPropScore += value * coeff

        initScore += rPropScore * qualityFactor
        rPropScore *= starFactor * qualityFactor
        ed = ED.data.get(self.id, {})
        if isManual or isExtended:
            propsDict = {}
            equipTypeFactor = SCD.data.get('manualEquipTypeFactor', {}).get((self.equipType, self.equipSType, self.enhanceType), 1)
            for pid, ptp, value in getattr(self, 'props', []):
                propsDict[pid, ptp] = propsDict.get((pid, ptp), 0) + value

            baseExtraScore = 0
            for key, value in propsDict.iteritems():
                pid, ptp = key
                data = PRD.data.get(pid)
                if not data:
                    continue
                if ptp == gametypes.DATA_TYPE_NUM:
                    coeff = data.get('scoreCoeffNum', 0)
                else:
                    coeff = data.get('scoreCoeffPercent', 0)
                if isManual:
                    basicPropFactor = MEBSCD.data.get((pid,
                     self.equipType,
                     self.equipSType,
                     self.enhanceType), {}).get('basicPropFactor', 1.0)
                else:
                    basicPropFactor = 1.0
                baseExtraScore += value * coeff * basicPropFactor

            initScore += baseExtraScore * qualityFactor * equipTypeFactor
            baseExtraScore *= starFactor * qualityFactor * equipTypeFactor
        else:
            initScore += ed.get('extraPoint', 0) * qualityFactor
            baseExtraScore = ed.get('extraPoint', 0) * starFactor * qualityFactor
        gemScore = sum([ gemSlot.score for gemSlot in getattr(self, 'yangSlots', ()) ])
        gemScore += sum([ gemSlot.score for gemSlot in getattr(self, 'yinSlots', ()) ])
        propFixScore = 0
        if hasattr(self, 'propFix'):
            randPropFixScore = 0
            try:
                for pid, value in self.propFix.get(self.EQUIP_PROP_FIX_BASE, []):
                    data = PRD.data.get(pid)
                    if not data:
                        continue
                    randPropFixScoreFormula = data.get('randPropFixScoreFormula')
                    if not randPropFixScoreFormula:
                        continue
                    formulaId, formulaParams = randPropFixScoreFormula[0], randPropFixScoreFormula[1:]
                    randPropFixScore += self.evalValue(formulaId, formulaParams, {'starFactor': starFactor,
                     'qualityFactor': qualityFactor,
                     'propVal': value})

                initScore += randPropFixScore * 1.0 / starFactor if starFactor else randPropFixScore
            except Exception as e:
                gamelog.error('calc rand prop score error!', self.id, e.message)

            if isManual or isExtended:
                data = self._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
            else:
                starPropFixScore = ed.get('starPropFixScore', 0)
            if self.propFix.get(self.EQUIP_PROP_FIX_STARLV):
                propFixScore = starPropFixScore + randPropFixScore
        guanYinScore = self.calcGuanYinPSkillScore(extra)
        self.score = int(rPropScore + baseExtraScore + seScore + propFixScore + prefixScore + enhanceScore + juexingScore + gemScore + guanYinScore)
        self.initScore = int(initScore)
        if utils.enableCalcRarityMiracle() and calcRarityMiracle and not getattr(self, 'rarityMiracle', Item.EQUIP_NOT_DECIDED) and (ed.has_key('rarityCondition') or ed.has_key('miracleCondition')):
            if isManual or isExtended:
                data = self._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
                allStarSEffectScore = starPropFixScore + ESPD.data.get(data.get('starSEffect', 0), {}).get('equipScore', 0)
            else:
                starPropFixScore = ed.get('starPropFixScore', 0)
                allStarSEffectScore = starPropFixScore + ESPD.data.get(ed.get('starSEffect', 0), {}).get('equipScore', 0)
            initScoreWithAllStar = initScore + allStarSEffectScore
            self.rarityMiracle = self.calcRarityMiracleEquip(initScoreWithAllStar)

    def _calcScoresWithType(self, calcRarityMiracle = False, extra = None):
        if self.isYaoPei():
            return
        owner = extra.get('owner', None) if extra else None
        initScore = 0
        rprop = self.rprops if hasattr(self, 'rprops') else []
        orderFactor = EOFD.data.get(self.order, {}).get('factor', 1.0)
        refiningFactor = 0
        for eLv, v in getattr(self, 'enhanceRefining', {}).iteritems():
            if eLv <= min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner)):
                refiningFactor += v

        enhanceScore = 0
        enhanceScoreType = [0,
         0,
         0,
         0]
        juexingScore = 0
        juexingScoreType = [0,
         0,
         0,
         0]
        enhanceData = EEPD.data.get((self.equipType, self.equipSType, self.enhanceType), {})
        if enhanceData.has_key('enhScore'):
            fVars = {'enhanceRefining': refiningFactor,
             'orderFactor': orderFactor,
             'enhanceLv': min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner))}
            enhanceScore = calcValueByFormulaData(enhanceData['enhScore'], fVars)
            enhanceScoreType = calcCombatScoreType(enhanceScoreType, enhanceData.get('enhScoreType', []), [], enhanceScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
        try:
            enhJuexingAddRatio = getattr(self, 'enhJuexingAddRatio', {})
            for eLv, juexingPropList in getattr(self, 'enhJuexingData', {}).iteritems():
                if eLv > min(getattr(self, 'enhLv', 0), self.getMaxEnhLv(owner)):
                    continue
                addRatio = enhJuexingAddRatio.get(eLv, 0)
                juexingDataList = utils.getEquipEnhJuexingPropData(self.equipType, self.equipSType, eLv, self.enhanceType)
                for pid, ptp, value in juexingPropList:
                    if pid not in juexingDataList:
                        continue
                    data = PRD.data.get(pid)
                    if not data:
                        continue
                    juexingScoreFormula = data.get('juexingScore')
                    if not juexingScoreFormula:
                        continue
                    formulaId, formulaParams = juexingScoreFormula[0], juexingScoreFormula[1:]
                    value *= 1 + addRatio
                    juexingPropScore = self.evalValue(formulaId, formulaParams, {'val': value,
                     'enhLv': eLv})
                    juexingScore += juexingPropScore
                    juexingScoreType = calcCombatScoreType(juexingScoreType, data.get('juexingScoreType', []), [], juexingPropScore, const.COMBAT_SCORE_TYPE_OP_COEFF)

        except Exception as e:
            gamelog.error('calc juexing score error!', self.id, e.message)

        seScore = 0
        seScoreType = [0,
         0,
         0,
         0]
        for seType, seList in getattr(self, 'ses', {}).iteritems():
            seScoreVal = sum([ ESPD.data.get(seId, {}).get('equipScore', 0) for seId in seList ])
            seScoreValType = [0,
             0,
             0,
             0]
            for seId in seList:
                equipScore = ESPD.data.get(seId, {}).get('equipScore', 0)
                equipScoreType = ESPD.data.get(seId, {}).get('equipScoreType', [])
                equipScoreTypeResult = calcCombatScoreType([], equipScoreType, [], equipScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
                seScoreValType = calcCombatScoreType(seScoreValType, [], [equipScoreTypeResult], 0, const.COMBAT_SCORE_TYPE_OP_ADD)

            seScore += seScoreVal
            seScoreType = calcCombatScoreType(seScoreType, [], [seScoreValType], 0, const.COMBAT_SCORE_TYPE_OP_ADD)
            if seType != self.EQUIP_SE_STARLV:
                initScore += seScoreVal

        starFactor = ESFCD.data.get(getattr(self, 'starLv', -1), {}).get('factor', 1.0)
        qualityFactor = EQFD.data.get(self.quality, {}).get('factor', 1.0)
        prefixScore = 0
        prefixScoreType = [0,
         0,
         0,
         0]
        if hasattr(self, 'prefixInfo'):
            preGroupId, prefixId = self.prefixInfo
            preGroupData = EPFPD.data.get(preGroupId, [])
            for prefixData in preGroupData:
                if prefixData.get('id') == prefixId:
                    prefixScore = prefixData.get('prefixScore', 0)
                    prefixScoreType = calcCombatScoreType(prefixScoreType, prefixData.get('prefixScoreType', []), [], prefixScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
                    break

        isManual = self.isManualEquip()
        isExtended = self.isExtendedEquip()
        if isManual or isExtended:
            if isManual:
                epd = MEPD.data.get(self.id, {})
            else:
                epd = XEPD.data.get(self.id, {})
            preGroupList = epd.get('preGroupList', ())
        else:
            ed = ED.data.get(self.id, {})
            preGroupList = ed.get('preGroupList', ())
        minPreFixScore = 0
        for gid, _ in preGroupList:
            pgData = EPFPD.data.get(gid, [])
            for pfData in pgData:
                if pfData['lvStart'] > self.itemLv or pfData['lvEnd'] < self.itemLv:
                    continue
                if pfData.has_key('prefixScore'):
                    minPreFixScore = min(minPreFixScore, pfData['prefixScore']) if minPreFixScore else pfData['prefixScore']

        initScore += minPreFixScore * qualityFactor
        prefixScore *= starFactor * qualityFactor
        prefixScoreType = calcCombatScoreType(prefixScoreType, [], [], starFactor * qualityFactor, const.COMBAT_SCORE_TYPE_OP_MUL)
        d = defaultdict(lambda : 0)
        for pid, ptp, value in rprop:
            d[pid, ptp] += value

        rPropScore = 0
        rPropScoreType = [0,
         0,
         0,
         0]
        for key, value in d.iteritems():
            pid, ptp = key
            data = PRD.data.get(pid)
            if not data:
                continue
            if ptp == gametypes.DATA_TYPE_NUM:
                coeff = data.get('scoreCoeffNum', 0)
                coeffType = data.get('scoreCoeffNumType', [])
            else:
                coeff = data.get('scoreCoeffPercent', 0)
                coeffType = data.get('scoreCoeffPercentType', [])
            gamelog.debug('jorsef: score temp: ', pid, ptp, value, coeff)
            rPropScore += value * coeff
            rPropScoreType = calcCombatScoreType(rPropScoreType, coeffType, [], value * coeff, const.COMBAT_SCORE_TYPE_OP_COEFF)

        initScore += rPropScore * qualityFactor
        rPropScore *= starFactor * qualityFactor
        rPropScoreType = calcCombatScoreType(rPropScoreType, [], [], starFactor * qualityFactor, const.COMBAT_SCORE_TYPE_OP_MUL)
        baseExtraScoreType = [0,
         0,
         0,
         0]
        ed = ED.data.get(self.id, {})
        if isManual or isExtended:
            propsDict = {}
            equipTypeFactor = SCD.data.get('manualEquipTypeFactor', {}).get((self.equipType, self.equipSType, self.enhanceType), 1)
            for pid, ptp, value in getattr(self, 'props', []):
                propsDict[pid, ptp] = propsDict.get((pid, ptp), 0) + value

            baseExtraScore = 0
            for key, value in propsDict.iteritems():
                pid, ptp = key
                data = PRD.data.get(pid)
                if not data:
                    continue
                if ptp == gametypes.DATA_TYPE_NUM:
                    coeff = data.get('scoreCoeffNum', 0)
                    coeffType = data.get('scoreCoeffNumType', [])
                else:
                    coeff = data.get('scoreCoeffPercent', 0)
                    coeffType = data.get('scoreCoeffPercentType', [])
                if isManual:
                    basicPropFactor = MEBSCD.data.get((pid,
                     self.equipType,
                     self.equipSType,
                     self.enhanceType), {}).get('basicPropFactor', 1.0)
                else:
                    basicPropFactor = 1.0
                baseExtraScore += value * coeff * basicPropFactor
                baseExtraScoreType = calcCombatScoreType(baseExtraScoreType, coeffType, [], value * coeff * basicPropFactor, const.COMBAT_SCORE_TYPE_OP_COEFF)

            initScore += baseExtraScore * qualityFactor * equipTypeFactor
            baseExtraScore *= starFactor * qualityFactor * equipTypeFactor
            baseExtraScoreType = calcCombatScoreType(baseExtraScoreType, [], [], starFactor * qualityFactor * equipTypeFactor, const.COMBAT_SCORE_TYPE_OP_MUL)
        else:
            initScore += ed.get('extraPoint', 0) * qualityFactor
            baseExtraScore = ed.get('extraPoint', 0) * starFactor * qualityFactor
            baseExtraScoreType = calcCombatScoreType(baseExtraScoreType, ed.get('extraPointType', []), [], baseExtraScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
        gemScore = sum([ gemSlot.score for gemSlot in getattr(self, 'yangSlots', ()) ])
        gemScore += sum([ gemSlot.score for gemSlot in getattr(self, 'yinSlots', ()) ])
        gemScoreType = calcCombatScoreType([], [], [ gemSlot.scoreType for gemSlot in getattr(self, 'yangSlots', ()) ], 0, const.COMBAT_SCORE_TYPE_OP_ADD)
        gemScoreType = calcCombatScoreType(gemScoreType, [], [ gemSlot.scoreType for gemSlot in getattr(self, 'yinSlots', ()) ], 0, const.COMBAT_SCORE_TYPE_OP_ADD)
        propFixScore = 0
        propFixScoreType = [0,
         0,
         0,
         0]
        if hasattr(self, 'propFix'):
            randPropFixScore = 0
            randPropFixScoreType = [0,
             0,
             0,
             0]
            try:
                for pid, value in self.propFix.get(self.EQUIP_PROP_FIX_BASE, []):
                    data = PRD.data.get(pid)
                    if not data:
                        continue
                    randPropFixScoreFormula = data.get('randPropFixScoreFormula')
                    if not randPropFixScoreFormula:
                        continue
                    formulaId, formulaParams = randPropFixScoreFormula[0], randPropFixScoreFormula[1:]
                    randPropFixScoreVal = self.evalValue(formulaId, formulaParams, {'starFactor': starFactor,
                     'qualityFactor': qualityFactor,
                     'propVal': value})
                    randPropFixScore += randPropFixScoreVal
                    randPropFixScoreType = calcCombatScoreType(randPropFixScoreType, data.get('randPropFixScoreFormulaType', []), [], randPropFixScoreVal, const.COMBAT_SCORE_TYPE_OP_COEFF)

                initScore += randPropFixScore * 1.0 / starFactor if starFactor else randPropFixScore
            except Exception as e:
                gamelog.error('calc rand prop score error!', self.id, e.message)

            if isManual or isExtended:
                data = self._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
                starPropFixScoreType = calcCombatScoreType([], data.get('starPropFixScoreType', []), [], starPropFixScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
            else:
                starPropFixScore = ed.get('starPropFixScore', 0)
                starPropFixScoreType = calcCombatScoreType([], ed.get('starPropFixScoreType', []), [], starPropFixScore, const.COMBAT_SCORE_TYPE_OP_COEFF)
            if self.propFix.get(self.EQUIP_PROP_FIX_STARLV):
                propFixScore = starPropFixScore + randPropFixScore
                propFixScoreType = calcCombatScoreType([], [], [randPropFixScoreType, starPropFixScoreType], 0, const.COMBAT_SCORE_TYPE_OP_ADD)
        guanYinScore = self.calcGuanYinPSkillScore(extra)
        guanYinScoreType = self.calcGuanYinPSkillScoreType()
        self.score = int(rPropScore + baseExtraScore + seScore + propFixScore + prefixScore + enhanceScore + juexingScore + gemScore + guanYinScore)
        self.initScore = int(initScore)
        addScoreTypes = [rPropScoreType,
         baseExtraScoreType,
         seScoreType,
         propFixScoreType,
         prefixScoreType,
         enhanceScoreType,
         juexingScoreType,
         gemScoreType,
         guanYinScoreType]
        self.scoreType = calcCombatScoreType([], [], addScoreTypes, 0, const.COMBAT_SCORE_TYPE_OP_ADD)
        if utils.enableCalcRarityMiracle() and calcRarityMiracle and not getattr(self, 'rarityMiracle', Item.EQUIP_NOT_DECIDED) and (ed.has_key('rarityCondition') or ed.has_key('miracleCondition')):
            if isManual or isExtended:
                data = self._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
                allStarSEffectScore = starPropFixScore + ESPD.data.get(data.get('starSEffect', 0), {}).get('equipScore', 0)
            else:
                starPropFixScore = ed.get('starPropFixScore', 0)
                allStarSEffectScore = starPropFixScore + ESPD.data.get(ed.get('starSEffect', 0), {}).get('equipScore', 0)
            initScoreWithAllStar = initScore + allStarSEffectScore
            self.rarityMiracle = self.calcRarityMiracleEquip(initScoreWithAllStar)

    def calcRarityMiracleEquip(self, initScoreWithAllStar):
        ed = ED.data.get(self.id, {})
        rarityConds = ed.get('rarityCondition', None)
        miracleConds = ed.get('miracleCondition', None)
        if miracleConds and self._checkRarityOrMiracleCond(initScoreWithAllStar, miracleConds):
            return Item.EQUIP_IS_MIRACLE
        elif rarityConds and self._checkRarityOrMiracleCond(initScoreWithAllStar, rarityConds):
            return Item.EQUIP_IS_RARITY
        else:
            return Item.EQUIP_NOT_RARITY_MIRACLE

    def isRarityMiracle(self):
        res = getattr(self, 'rarityMiracle', Item.EQUIP_NOT_DECIDED)
        return res == Item.EQUIP_IS_RARITY or res == Item.EQUIP_IS_MIRACLE

    def _checkRarityOrMiracleCond(self, initScoreWithAllStar, conds):
        """
        conds (  (\xb3\xf5\xca\xbc\xc6\xc0\xb7\xd6\xa3\xac\xb6\xee\xcd\xe2\xca\xf4\xd0\xd4\xd2\xaa\xc7\xf3\xa3\xac[\xca\xf4\xd0\xd4\xb2\xce\xca\xfd\xc0\xe0\xd0\xcd\xa3\xac\xe3\xd0\xd6\xb5\xb2\xce\xca\xfd]),  ... )
        \xb6\xee\xcd\xe2\xca\xf4\xd0\xd4\xd2\xaa\xc7\xf3 cond[1] propTp : 1 \xb3\xc8\xd7\xd6 2 \xb0\xd7\xd7\xd6 3 \xc0\xb6\xd7\xd6 4 \xc0\xb6\xb0\xd7
        \xca\xf4\xd0\xd4\xb2\xce\xca\xfd\xc0\xe0\xd0\xcd cond[2] condTp : 1 \xb4\xef\xb5\xbd\xb0\xd9\xb7\xd6\xb1\xc8\xb5\xc4\xca\xf4\xd0\xd4\xd7\xdc\xca\xfd 2 \xcd\xac\xd2\xbb\xca\xf4\xd0\xd4\xb5\xc4\xb4\xef\xb5\xbd\xb0\xd9\xb7\xd6\xb1\xc8\xb5\xc4\xd7\xee\xb4\xf3\xd6\xb5
        \xe3\xd0\xd6\xb5\xb2\xce\xca\xfd cond[3] : \xca\xfd\xc1\xbf\xd2\xaa\xc7\xf3 \xbb\xf2 (\xb0\xd9\xb7\xd6\xb1\xc8\xa3\xac\xca\xfd\xc1\xbf\xd2\xaa\xc7\xf3)
        """
        for cond in conds:
            if len(cond) not in (2, 4):
                continue
            if initScoreWithAllStar <= cond[0]:
                continue
            if cond[1]:
                if cond[2] == 0:
                    if cond[1] == 1:
                        num = len(getattr(self, 'ses', {}).get(self.EQUIP_SE_MANUAL, []))
                    elif cond[1] == 2:
                        num = len(getattr(self, 'props', []))
                    elif cond[1] == 3:
                        num = len(getattr(self, 'rprops', []))
                    else:
                        num = len(getattr(self, 'props', [])) + len(getattr(self, 'rprops', []))
                    if num >= cond[3]:
                        return True
                    continue
                elif cond[1] in (2, 3, 4) and cond[2] in (1, 2) and len(cond[3]) == 2:
                    res = self._checkPropPercentageNum(cond[1], cond[2], cond[3][0], cond[3][1])
                    if res:
                        return True
            else:
                return True

        return False

    def _checkPropPercentageNum(self, propTp, condTp, percentage, num):
        isManual = MEPD.data.has_key(self.id)
        if not isManual:
            if not XEPD.data.has_key(self.id):
                gamelog.error('@smj _checkPropPercentageNum not has id')
                return False
        propIDs = []
        propVals = []
        rPropIDs = []
        rPropVals = []
        numStat = {}
        if propTp != 2:
            for pid, ptp, value in getattr(self, 'rprops', []):
                rPropIDs.append(pid)
                rPropVals.append(value)

        if propTp != 3:
            for pid, ptp, value in getattr(self, 'props', []):
                propIDs.append(pid)
                propVals.append(value)

        if isManual:
            epData = MEPD.data[self.id]
        else:
            epData = XEPD.data[self.id]
        if epData.has_key('extraPools') and len(rPropIDs) > 0:
            if isManual:
                randPropId = epData['extraPools'][0]
            else:
                randPropId = epData['extraPools']
            poolData = ERPD.data.get((randPropId, self.quality))
            if not poolData:
                gamelog.debug('@smj _checkPropPercentageNum not poolData')
                return False
            poolList = []
            for pd in poolData:
                for pool in pd.get('pool', []):
                    for i in xrange(pool[1]):
                        poolList.append(EPPD.data.get(pool[0], []))

            if len(poolList) != len(rPropIDs):
                gamelog.debug('@smj _checkPropPercentageNum len not match')
                return False
            pi = 0
            for propID in rPropIDs:
                eppd = poolList[pi]
                for ei in eppd:
                    val = ei.get('value')
                    if not val:
                        continue
                    if val[0] == propID:
                        aid, atype, transType, amax, amin, pmin, pmax = val
                        if transType != gametypes.PROPERTY_RAND_ABS:
                            fd = FSD.data.get(transType)
                            formula = fd.get('formula')
                            if not formula:
                                continue
                            amin = self.evalValue(transType, pmin)
                            amax = self.evalValue(transType, pmax)
                        if percentage * (amax - amin) + amin < rPropVals[pi]:
                            numStat[propID] = numStat.get(propID, 0) + 1
                            break

                pi += 1

        if epData.has_key('basicProps') and len(propIDs) > 0:
            if isManual:
                basiceProps = epData['basicProps'][0]
            else:
                basiceProps = epData['basicProps']
            pi = 0
            for propID in propIDs:
                for pid, pType, valMin, valMax, weights in basiceProps:
                    if not weights:
                        continue
                    if propID != pid:
                        continue
                    if percentage * (valMax - valMin) + valMin < propVals[pi]:
                        numStat[propID] = numStat.get(propID, 0) + 1
                        break

                pi += 1

        if condTp == 1:
            ttn = sum(numStat.values())
            return ttn >= num
        if condTp == 2:
            temp = [0]
            temp.extend(numStat.values())
            ttn = max(temp)
            return ttn >= num
        return False

    def isPropCondMatch(self, scoreLimit, rarityMiracle, rpropConds, yaopeiPropConds, yaopeiSkillConds, seManualProps):
        if not self.isEquip():
            return False
        if rarityMiracle and not self.isRarityMiracle():
            return False
        if seManualProps:
            ses = getattr(self, 'ses', None)
            if ses:
                if self.EQUIP_SE_MANUAL in ses:
                    rses = getattr(self, 'ses', {}).get(self.EQUIP_SE_MANUAL, [])
                    if not set(rses) & set(seManualProps):
                        return False
                else:
                    return False
            else:
                return False
        if yaopeiPropConds:
            if self.isYaoPei():
                counts = copy.copy(yaopeiPropConds)
                for pId, pType, pVal, minVal, maxVal, lv in self.yaoPeiExtraProps:
                    if pId in counts:
                        counts[pId] = max(counts[pId] - 1, 0)

                if sum(counts.values()) > 0:
                    return False
            else:
                return False
        if yaopeiSkillConds:
            if self.isYaoPei():
                if len(yaopeiSkillConds) != 1 or yaopeiSkillConds.get(self.yaoPeiSkillId, 0) != 1:
                    return False
            else:
                return False
        if rpropConds:
            counts = copy.copy(rpropConds)
            rprop = self.rprops if hasattr(self, 'rprops') else []
            for pid, ptp, value in rprop:
                if pid in counts:
                    counts[pid] = max(counts[pid] - 1, 0)

            if sum(counts.values()) > 0:
                return False
        if scoreLimit > self.score:
            return False
        return True

    def isExpireTTL(self):
        ttlExpireTime = self.getTTLExpireTime()
        if ttlExpireTime != 0:
            return utils.getNow() >= ttlExpireTime
        return False

    def isExpireTTLEC(self):
        ttlExpireTime = self.getTTLExpireTimeForItem()
        if ttlExpireTime != 0:
            return utils.getNow() >= ttlExpireTime
        return False

    def hasGrayJuexingData(self):
        enhLv = getattr(self, 'enhLv', 0)
        maxEnhlv = getattr(self, 'maxEnhlv', 0)
        enhJuexingData = getattr(self, 'enhJuexingData', {})
        if enhJuexingData:
            enhJueXingList = [ [key, val] for key, val in enhJuexingData.items() ]
            for key in enhJueXingList:
                if key[1]:
                    juexingDataList = key[1]
                    dataForEj = utils.getEquipEnhJuexingPropData(self.equipType, self.equipSType, key[0], self.enhanceType)
                    hasNotIn = False
                    for j in juexingDataList:
                        if j[0] not in dataForEj:
                            hasNotIn = True

                    if key[0] > enhLv or hasNotIn or key[0] > maxEnhlv:
                        return True

        tempJXAlldata = getattr(self, 'tempJXAlldata', [])
        if tempJXAlldata:
            enhTempJXList = [ [key, val] for key, val in tempJXAlldata ]
            for key in enhTempJXList:
                if key[1]:
                    tmpJXDataList = key[1]
                    dataForEj = utils.getEquipEnhJuexingPropData(self.equipType, self.equipSType, key[0], self.enhanceType)
                    hasNotIn = False
                    for j in tmpJXDataList:
                        if j[0] not in dataForEj:
                            hasNotIn = True

                    if key[0] > enhLv or hasNotIn or key[0] > maxEnhlv:
                        return True

        return False

    def isEquipExpire(self):
        if self.isDyeExpire():
            return True
        if self.isHuanfuExpire():
            return True
        if self.isRongGuangExpire():
            return True
        if self.isDragTailExpire():
            return True
        if self.isRubbingExpire():
            return True
        return False

    def isDyeExpire(self):
        current = BigWorld.component in ('client',) and BigWorld.player().getServerTime() or utils.getNow()
        if hasattr(self, 'dyeTTLExpireTime') and self.dyeTTLExpireTime:
            return self.dyeTTLExpireTime < current
        return False

    def isHuanfuExpire(self):
        current = BigWorld.component in ('client',) and BigWorld.player().getServerTime() or utils.getNow()
        if hasattr(self, 'currentSkin') and self.currentSkin:
            dyeSkins = getattr(self, 'dyeSkins', {})
            if self.currentSkin not in dyeSkins:
                return True
            if dyeSkins[self.currentSkin] and dyeSkins[self.currentSkin] < current:
                return True
        return False

    def isRubbingExpire(self):
        current = BigWorld.component in ('client',) and BigWorld.player().getServerTime() or utils.getNow()
        if hasattr(self, 'rubbingTTLExpireTime') and self.rubbingTTLExpireTime:
            return self.rubbingTTLExpireTime < current
        return False

    def isRongGuangExpire(self):
        current = BigWorld.component in ('client',) and BigWorld.player().getServerTime() or utils.getNow()
        if hasattr(self, 'rongGuangExpireTime') and self.rongGuangExpireTime:
            return self.rongGuangExpireTime < current
        return False

    def isDragTailExpire(self):
        if not self.isWingOrRide():
            return False
        if not hasattr(self, 'rideWingStates'):
            return False
        current = BigWorld.component in ('client',) and BigWorld.player().getServerTime() or utils.getNow()
        return self.rideWingStates.get('flyTailEffectExpireTime', const.EXPIRE_TIME_INFINITE) < current

    def getNearstExpireTime(self):
        expireTime = min(getattr(self, 'rongGuangExpireTime', const.EXPIRE_TIME_INFINITE), getattr(self, 'dyeTTLExpireTime', const.EXPIRE_TIME_INFINITE))
        ttlExpire = self.getTTLExpireTime()
        if ttlExpire:
            expireTime = min(expireTime, ttlExpire)
        shihunTime = self.getShihunExpireTime()
        if shihunTime:
            expireTime = min(expireTime, shihunTime)
        expireTime = min(self.getDragTailEffectExpireTime(), expireTime)
        if expireTime == const.EXPIRE_TIME_INFINITE:
            return 0
        return expireTime

    def getTTLExpireTime(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!!', self.id)
            return 0
        if hasattr(self, 'ownershipPercent') and self.ownershipPercent >= const.ITEM_OWNERSHIP_MAX:
            return 0
        realExpireTime = max(getattr(self, 'expireTime', const.EXPIRE_TIME_NOT_SET), getattr(self, 'commonExpireTime', const.EXPIRE_TIME_NOT_SET), getattr(self, '_mallExpireTime', const.EXPIRE_TIME_NOT_SET))
        if realExpireTime != const.EXPIRE_TIME_NOT_SET:
            return realExpireTime
        if itemData.get('ttl', 0) and hasattr(self, 'uutime'):
            return self.uutime + itemData['ttl']
        return 0

    def getCommonExpireTime(self):
        return getattr(self, 'commonExpireTime', const.EXPIRE_TIME_NOT_SET)

    def getTTLExpireTimeForItem(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 0
        if hasattr(self, 'ownershipPercent') and self.ownershipPercent >= const.ITEM_OWNERSHIP_MAX:
            return 0
        realExpireTime = max(getattr(self, 'expireTime', const.EXPIRE_TIME_NOT_SET), getattr(self, '_mallExpireTime', const.EXPIRE_TIME_NOT_SET))
        if realExpireTime != const.EXPIRE_TIME_NOT_SET:
            return realExpireTime
        if itemData.get('ttl', 0) and hasattr(self, 'uutime'):
            return self.uutime + itemData['ttl']
        return 0

    def getOwnershipPercent(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 0
        return getattr(self, 'ownershipPercent', 0)

    def getTimeLimitExpireType(self):
        itemData = CID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 0
        if not hasattr(self, 'timeLimit'):
            return 0
        return itemData.get('timeLimitExpireType', const.ITEM_TIME_LIMIT_TYPE_REMOVE)

    def getTTLExpireType(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 0
        return itemData.get('ttlExpireType', const.TTL_EXPIRE_TYPE_NORMAL)

    def getTTLChangeId(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 0
        return itemData.get('ttlChangeId', 0)

    def getTTLChangeAmount(self):
        itemData = ID.data.get(self.id, None)
        if not itemData:
            gamelog.error('data not configured in item data!! %d' % self.id)
            return 1
        return itemData.get('ttlChangeAmount', 1)

    def getUseItemSound(self):
        itemData = ID.data.get(self.id, {})
        return itemData.get('useItemSound', 0)

    def getDragItemSound(self):
        itemData = ID.data.get(self.id, {})
        return itemData.get('dragItemSound', 0)

    def isItemNoTrade(self):
        if self.isForeverBind():
            return True
        if self.isRuneHasRuneData():
            return True
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemNoTrade(itemData)

    def isItemNoConsign(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemNoConsign(itemData)

    def isItemCoinConsign(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemCoinConsign(itemData)

    def isItemCrossConsign(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemCrossConsign(itemData)

    def isItemNoMail(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemNoMail(itemData)

    def canItemHandover(self, owner = None, msgId = 0):
        if hasattr(self, 'tCoinMail') and gameconfigCommon.enableCoinMailHandoverCheck():
            tEnd = self.tCoinMail + SCD.data.get('coinMailCDDays', 0) * const.TIME_INTERVAL_DAY
            now = utils.getNow()
            if now < tEnd:
                if owner:
                    msgId = msgId or GMDD.data.HANDOVER_CD
                    if BigWorld.component != 'client':
                        owner.client.showGameMsg(msgId, (self.name, utils.formatDuration(tEnd - now)))
                    else:
                        owner.showGameMsg(msgId, (self.name, utils.formatDuration(tEnd - now)))
                return False
        return True

    def isItemApprenticeOnly(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemApprenticeOnly(itemData)

    def isItemMentorOnly(self):
        itemData = ID.data.get(self.id)
        return itemData and utils.getItemMentorOnly(itemData)

    def isItemGuildDonate(self):
        cstype = GDID.data.get(self.id, 0)
        if not cstype:
            return False
        return cstype == self.SUBTYPE_2_MOJING or cstype == self.SUBTYPE_2_XIRANG or cstype == self.SUBTYPE_2_WOOD or cstype == self.SUBTYPE_2_GUILD_MONEY or cstype == self.SUBTYPE_2_GUILD_SPECIAL_RES or cstype == self.SUBTYPE_2_GUILD_MACHINE_RES or cstype == self.SUBTYPE_2_GUILD_FACILITY_RES or self.isWingWorldGuildMoney()

    def isMojing(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_MOJING

    def isXirang(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_XIRANG

    def isWood(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_WOOD

    def isGuildMoney(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_GUILD_MONEY

    def isTianyucanjing(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_TIAN_YU_CAN_JING

    def isGuildReserveCash(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_GUILD_RESERVE_CASH

    def isJingJie(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_JING_JIE

    def isServerDonate(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_SERVER_DONATE

    def isGuildOtherRes(self):
        cstype = GDID.data.get(self.id, 0)
        if not cstype:
            return False
        return cstype == self.SUBTYPE_2_GUILD_SPECIAL_RES or cstype == self.SUBTYPE_2_GUILD_MACHINE_RES or cstype == self.SUBTYPE_2_GUILD_FACILITY_RES

    def isForeverBind(self):
        return hasattr(self, 'bindType') and self.bindType == gametypes.ITEM_BIND_TYPE_FOREVER

    def isEquipBind(self):
        return hasattr(self, 'bindType') and self.bindType == gametypes.ITEM_BIND_TYPE_EQUIP

    def isUseBind(self):
        return hasattr(self, 'bindType') and self.bindType == gametypes.ITEM_BIND_TYPE_USE

    def bindItem(self):
        self.bindType = gametypes.ITEM_BIND_TYPE_FOREVER

    def unbindItem(self):
        self.bindType = gametypes.ITEM_BIND_TYPE_NONE

    def canMoveToStorage(self):
        itemData = ID.data.get(self.id, {})
        return not utils.getItemNoStorage(itemData)

    def hasLatch(self):
        return hasattr(self, 'latchOfTime') and self.latchOfTime > utils.getNow() or hasattr(self, 'latchOfCipher')

    def isLatchOfTime(self):
        return hasattr(self, 'latchOfTime') and self.latchOfTime > utils.getNow()

    def canLatch(self):
        return utils.getItemNoLatch(ID.data.get(self.id, {})) == 0

    def getSpecialPropList(self):
        if not gameconfigCommon.enableRefineManualEquipment():
            return []
        ses = getattr(self, 'ses', {})
        specialPropList = []
        for sess in ses.itervalues():
            for spId in sess:
                if ESPD.data.has_key(spId):
                    if spId in ses.get(Item.EQUIP_SE_MANUAL, []):
                        specialPropList.append(spId)

        return specialPropList

    def getSpecialPropLevel(self):
        if not gameconfigCommon.enableRefineManualEquipment():
            return 0
        specialPropList = self.getSpecialPropList()
        if len(specialPropList) >= 2:
            return 2
        if len(specialPropList) == 1 and getattr(self, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY:
            return 1
        if ID.data.get(self.id, {}).get('showRefiningEff', 0):
            return 1
        return 0

    def checkHasSesProp(self, equipSesPropsId, sesPropsName):
        if equipSesPropsId not in ESPD.data:
            return False
        sesDataList = ESPD.data.get(equipSesPropsId, {}).get('ses', [])
        for sesData in sesDataList:
            if sesData[0] == sesPropsName:
                return True

        return False

    @property
    def hasSesMakerProp(self):
        if not hasattr(self, 'seCache') or not self.seCache.has_key(Item.SES_PROPS_MAKER):
            return False
        else:
            return True

    def isSesMaker(self, gbId):
        if not hasattr(self, 'makerGbId') or not self.makerGbId:
            return 0
        makerGbId = self.makerGbId
        if makerGbId == gbId:
            if not self.hasSesMakerProp:
                return 0
            else:
                param = self.seCache.get(Item.SES_PROPS_MAKER, 0)
                return param
        return 0

    def isSesWenYinEnh(self):
        if not hasattr(self, 'seCache') or not self.seCache.has_key(Item.SES_PROPS_WENYINENH):
            return 0
        else:
            param = self.seCache.get(Item.SES_PROPS_WENYINENH, 0)
            return param

    def isShihun(self):
        if hasattr(self, 'shihun'):
            r = getattr(self, 'shihun', False) and getattr(self, 'shihunExpireTime', 0) > utils.getNow()
            if not r:
                setattr(self, 'shihun', False)
            return r
        else:
            return False

    def getShihunExpireTime(self):
        return getattr(self, 'shihunExpireTime', 0)

    def setShihun(self, v):
        if v:
            setattr(self, 'shihun', True)
            setattr(self, 'shihunExpireTime', utils.getNow() + SCD.data.get('shihunTTL', const.SHIHUN_TTL))
        else:
            delattr(self, 'shihun')
            delattr(self, 'shihunExpireTime')
            if hasattr(self, 'shihunItemUUID'):
                delattr(self, 'shihunItemUUID')

    def setRedemption(self, v):
        if v:
            self.redemption = True
            self.valuableLatchOfTime = utils.getNow() + SCD.data.get('redemptionLatchTime', const.REDEMPTION_LATCH_TIME) + 2 * SCD.data.get('redemptionDeliverTime', const.REDEMPTION_DELIVER_TIME)
        elif hasattr(self, 'redemption'):
            delattr(self, 'redemption')
            delattr(self, 'valuableLatchOfTime')

    def setGroupTrade(self, v, assignList = None):
        if v:
            self.tGroupTrade = utils.getNow()
            if assignList:
                self.tradeAssignList = copy.deepcopy(assignList)
        elif hasattr(self, 'tGroupTrade'):
            delattr(self, 'tGroupTrade')
            if hasattr(self, 'tradeAssignList'):
                delattr(self, 'tradeAssignList')

    def isGroupTrade(self):
        return hasattr(self, 'tGroupTrade')

    def canGroupTrade(self):
        return self.isGroupTrade() and self.tGroupTrade + SCD.data.get('groupTradeTime', const.GROUP_TRADE_TIME) > utils.getNow()

    def getGroupTradeTime(self):
        if self.canGroupTrade():
            groupTradeTime = self.tGroupTrade + SCD.data.get('groupTradeTime', const.GROUP_TRADE_TIME) - utils.getNow()
            if groupTradeTime >= 0:
                return groupTradeTime
            else:
                return None
        else:
            return None

    def getGroupTradeEndStamp(self):
        if self.canGroupTrade():
            return self.tGroupTrade + SCD.data.get('groupTradeTime', const.GROUP_TRADE_TIME)
        else:
            return None

    def isItemCanRebuild(self):
        juexingDataList = getattr(self, 'enhJuexingData', {})
        if not juexingDataList:
            return False
        find = False
        for key in juexingDataList:
            juexingDataListOnLv = juexingDataList[key]
            for juexingData in juexingDataListOnLv:
                if juexingData:
                    find = True
                    break

        return find

    def _lateReload(self):
        super(Item, self)._lateReload()
        if self.isRuneEquip():
            if hasattr(self, 'runeData'):
                for rVal in self.runeData:
                    rVal.reloadScript()

        if self.isEquip():
            for gVal in getattr(self, 'yinSlots', []):
                gVal.reloadScript()

            for gVal in getattr(self, 'yangSlots', []):
                gVal.reloadScript()

    def consistentRuneEquipData(self):
        if BigWorld.component == 'client':
            return
        if not hasattr(self, 'runeData'):
            self.runeData = []
        if not hasattr(self, 'pskillData'):
            self.pskillData = {}
        if not hasattr(self, 'runeEquipLv'):
            self.runeEquipLv = 1
        if not hasattr(self, 'runeEquipExp'):
            self.runeEquipExp = 0
        rData = RED.data.get(self.id, {})
        if not hasattr(self, 'runeEquipOrder'):
            self.runeEquipOrder = rData.get('order', 1)
        if not hasattr(self, 'runeEquipAptitude'):
            self.runeEquipAptitude = rData.get('aptitude', 0)
        if not hasattr(self, 'runeEquipXiLianData') or self.runeEquipXiLianData == []:
            self.runeEquipXiLianData = {}

    def consistentHieroEquipData(self):
        if BigWorld.component == 'client':
            return
        if not hasattr(self, 'pskillData'):
            self.pskillData = {}
        rData = HED.data.get(self.id, {})
        if not hasattr(self, 'hieroEquipOrder'):
            self.hieroEquipOrder = rData.get('order', 1)
        if not hasattr(self, 'hieroEquipAptitude'):
            self.hieroEquipAptitude = rData.get('aptitude', 0)

    def __initRuneEquipData(self):
        if not self.isRuneEquip():
            return
        rData = RED.data.get(self.id)
        if not rData:
            gamelog.error('zs: ERROR!!! can not find rune equip data: %d' % self.id)
            return
        self.runeData = []
        self.pskillData = {}
        self.runeEquipLv = 1
        self.runeEquipExp = 0
        self.runeEquipOrder = rData.get('order', 1)
        self.runeEquipAptitude = rData.get('aptitude', 0)
        self.runeEquipXiLianData = {}

    def __initHieroEquipData(self):
        if not self.isHieroEquip():
            return
        rData = HED.data.get(self.id)
        if not rData:
            gamelog.error('smj: ERROR!!! can not find hierogram equip data: %d' % self.id)
            return
        self.pskillData = {}
        self.hieroEquipOrder = rData.get('order', 1)
        self.hieroEquipAptitude = rData.get('aptitude', 0)

    def getRuneEquipXiLianData(self, runeType):
        res = {}
        for key, val in self.runeEquipXiLianData.iteritems():
            runeSlotsType, part = key
            if runeSlotsType == runeType:
                res[part] = val

        return res

    def updateRuneEquipXiLianData(self, data):
        self.runeEquipXiLianData = {}
        for key, val in data.items():
            self.runeEquipXiLianData[key] = val

    def updateSingleSlotXiLianData(self, runeType, part, newXiLianId, newPskData):
        self.runeEquipXiLianData[runeType, part] = (newXiLianId, newPskData)

    def clearRuneEquipXiLianData(self):
        if not self.isRuneEquip():
            return
        self.runeEquipXiLianData = {}

    def getRuneEquipSlotNum(self, runeType):
        if not self.isRuneEquip():
            return 0
        return const.RUNE_EQUIP_SLOTS_MAP.get((self.runeEquipOrder, runeType), 0)

    def addRuneEquipExp(self, amount):
        if not self.isRuneEquip():
            return
        amount = int(amount)
        if amount <= 0:
            return
        self.runeEquipExp += amount
        self._runeEquipLvUp()

    def _runeEquipLvUp(self):
        if self.runeEquipLv >= const.RUNE_EQUIP_MAX_LV:
            return
        eData = REED.data.get((self.runeEquipLv, self.runeEquipOrder))
        if not eData:
            return
        upExp = eData['upExp']
        if self.runeEquipExp < upExp:
            return
        while True:
            self.runeEquipExp -= upExp
            self.runeEquipLv += 1
            if self.runeEquipLv >= const.RUNE_EQUIP_MAX_LV:
                break
            eData = REED.data.get((self.runeEquipLv, self.runeEquipOrder))
            if not eData:
                break
            upExp = eData['upExp']
            if self.runeEquipExp < upExp:
                break

    def getAllRuneEquipAwakePSkills(self):
        res = []
        res.extend(self.getRuneEquipAwakePSkillsByRuneType(const.RUNE_TYPE_TIANLUN))
        res.extend(self.getRuneEquipAwakePSkillsByRuneType(const.RUNE_TYPE_DILUN))
        return res

    def getRuneEquipAwakePSkillsByRuneType(self, runeType):
        if not self.isRuneEquip():
            return []
        rData = RED.data.get(self.id)
        if not rData:
            return []
        if runeType == const.RUNE_TYPE_TIANLUN:
            return rData.get('tianLunPSkillList', [])
        if runeType == const.RUNE_TYPE_DILUN:
            return rData.get('diLunPSkillList', [])
        return []

    def setRuneEquipAptitude(self, amount):
        if not self.isRuneEquip():
            return
        if amount < 0:
            return
        self.runeEquipAptitude = int(amount)

    def consistentRuneData(self):
        if BigWorld.component == 'client':
            return
        rData = Item.getRuneCfgData(self.id)
        if not hasattr(self, 'pskillData'):
            self.pskillData = {}
        if not hasattr(self, 'runeLv'):
            self.runeLv = rData.get('lv', 1)
        if not hasattr(self, 'runeQiFuData') or self.runeQiFuData == []:
            self.runeQiFuData = {}

    def __initConsumeDyeList(self):
        if self.getDyeType() in (Item.CONSUME_DYE_RANDOM, Item.CONSUME_DYE_MAGIC):
            self.genConsumeDyeList()

    def genConsumeDyeList(self):
        self.consumeDyeList = utils.genRandomDyeList()

    def __initShiChuanState(self):
        self.isShiChuan = False

    def setShiChuanState(self, isShiChuan):
        self.isShiChuan = isShiChuan

    def isShiChuanItem(self):
        return getattr(self, 'isShiChuan', False)

    def __initHieroPropData(self):
        if not self.isNewHieroCrystal():
            return
        if BigWorld.component not in ('base', 'cell'):
            return
        try:
            from cdata import hierogram_trans_rate_reverse_data as HTRRD
            from data import new_rune_property_data as NRPD
            runeLv = NRD.data.get(self.id).get('lv', 1)
            totalId = HTRRD.data.get(runeLv, {}).get('totalId', [])
            totalWeight = HTRRD.data.get(runeLv, {}).get('totalWeight', [])
            randVal = random.randint(0, totalWeight[-1] - 1)
            cfgId = 0
            for index in xrange(0, len(totalWeight)):
                if randVal < totalWeight[index]:
                    cfgId = totalId[index]
                    break

            cfgData = NRPD.data.get(cfgId)
            baseAdd = random.randint(int(cfgData['minVal'] * const.HIEROGRAM_PROP_SCALE), int(cfgData['maxVal'] * const.HIEROGRAM_PROP_SCALE))
            baseAdd -= const.HIEROGRAM_PROP_SCALE
            self.setHieroSysProps('baseAdd', baseAdd)
        except Exception as e:
            self.setHieroSysProps('baseAdd', 0)
            gameengine.reportCritical('xjw## __initHieroPropData except %s' % (e.message,))

    @staticmethod
    def getRuneCfgData(runeId):
        if Item.newHieroCrystal(runeId):
            return NRD.data.get(runeId)
        if Item.oldHieroCrystal(runeId):
            return RD.data.get(runeId)
        return {}

    def __initRuneData(self):
        if not self.isRune():
            return
        rData = Item.getRuneCfgData(self.id)
        if not rData:
            gamelog.error('zs: ERROR!!! can not find rune data: %d' % self.id)
            return
        self.pskillData = {}
        self.runeLv = rData.get('lv', 1)
        self.runeQiFuData = {}

    def setQiFuData(self, qiFuLv, qiFuId, qData):
        self.runeQiFuData[qiFuLv] = (qiFuId, qData)

    def getQiFuData(self):
        if not self.isRune():
            return {}
        return self.runeQiFuData

    def runeLvUp(self):
        if not self.isRune():
            return
        self.runeLv += 1

    def isRuneEquip(self):
        return self.type == self.BASETYPE_RUNE_EQUIP

    def isRune(self):
        return self.type in self.BASETYPE_RUNES

    def isOldRune(self):
        return RD.data.has_key(self.id)

    def isHieroEquip(self):
        return self.type == self.BASETYPE_HIEROGRAM_EQUIP

    def isHieroCrystal(self):
        return self.type in self.BASETYPE_RUNES

    @staticmethod
    def newHieroCrystal(id):
        rData = ID.data.get(id, {})
        return rData.get('type', 0) == Item.BASETYPE_HIEROGRAM_CRYSTAL

    @staticmethod
    def oldHieroCrystal(id):
        rData = ID.data.get(id, {})
        return rData.get('type', 0) == Item.BASETYPE_RUNE

    def isNewHieroCrystal(self):
        return self.type == self.BASETYPE_HIEROGRAM_CRYSTAL

    def isOldHieroCrystal(self):
        return self.type == self.BASETYPE_RUNE

    def getHierogramPropAdd(self):
        if not self.isNewHieroCrystal():
            return 0
        else:
            return self.getHieroSysProps('baseAdd') + self.getHieroSysProps('feedAdd')

    def isPrecious(self):
        return ID.data.get(self.id, {}).get('precious', 0) == 1

    def isValuable(self):
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableValuableTrade():
                return False
        return self.mwrap == 1 and ID.data.get(self.id, {}).get('valuable', 0) == 1

    def canRuneQiFu(self):
        if not self.isRune():
            return False
        rData = Item.getRuneCfgData(self.id)
        if not rData:
            return False
        for qiFuLv in rData.get('qiFuLvList', []):
            if qiFuLv not in self.runeQiFuData:
                return True

        return False

    def getCanRuneQiFuLv(self):
        canRuneQiFuLv = []
        if self.isRune():
            rData = Item.getRuneCfgData(self.id)
            if rData:
                for qiFuLv in rData.get('qiFuLvList', []):
                    if qiFuLv not in self.runeQiFuData:
                        canRuneQiFuLv.append(qiFuLv)

        return canRuneQiFuLv

    def canRuneReforging(self):
        if not self.isRune():
            return False
        rData = Item.getRuneCfgData(self.id)
        if not rData:
            return False
        for qiFuLv in rData.get('qiFuLvList', []):
            if qiFuLv in self.runeQiFuData:
                return True

        return False

    def getCanRuneReforgingLv(self):
        canRuneReforgingLv = []
        if self.isRune():
            rData = Item.getRuneCfgData(self.id)
            if rData:
                for qiFuLv in rData.get('qiFuLvList', []):
                    if qiFuLv in self.runeQiFuData:
                        canRuneReforgingLv.append(qiFuLv)

        return canRuneReforgingLv

    def isEmptyRunePos(self, runeSlotsType, part):
        if not self.isRuneEquip():
            return False
        for rVal in self.runeData:
            if rVal.runeSlotsType == runeSlotsType and rVal.part == part:
                return False

        return True

    def getRunePos(self, runeSlotsType, part):
        if not self.isRuneEquip():
            return None
        for rVal in self.runeData:
            if rVal.runeSlotsType == runeSlotsType and rVal.part == part:
                return rVal.item

    def validRunePos(self, runeSlotsType, part):
        return part >= 0 and part < self.getRuneEquipSlotNum(runeSlotsType)

    def addRuneItem(self, runeSlotsType, part, item):
        if not self.isRuneEquip():
            return
        if not item.isRune():
            return
        if not self.validRunePos(runeSlotsType, part):
            return
        if not self.isEmptyRunePos(runeSlotsType, part):
            return
        rVal = runeDataVal(runeSlotsType, part, item)
        self.runeData.append(rVal)

    def getRuneData(self):
        if not self.isRuneEquip():
            return []
        if not hasattr(self, 'runeData'):
            return []
        return self.runeData

    def removeRuneItem(self, runeSlotsType, part):
        if not self.isRuneEquip():
            return None
        pos = -1
        for i, rVal in enumerate(self.runeData):
            if rVal.runeSlotsType == runeSlotsType and rVal.part == part:
                pos = i
                break

        if pos == -1:
            return None
        sVal = self.runeData.pop(pos)
        return sVal.item

    @staticmethod
    def _isIntPropRef(aid):
        propId = PRD.data.get(aid, {}).get('property', 0)
        numtype = PPD.data.get(propId, {}).get('numtype', 'I')
        return numtype == 'I'

    def isLifeEquip(self):
        return self.type == Item.BASETYPE_LIFE_EQUIP

    def getDyeType(self):
        if self.type == Item.BASETYPE_CONSUMABLE and self.cstype == Item.SUBTYPE_2_DYE:
            cid = CID.data.get(self.id, {})
            return cid.get('dyeType', Item.CONSUME_DYE_NORMAL)
        return 0

    def getDyeTtl(self):
        if self.type == Item.BASETYPE_CONSUMABLE and self.cstype == Item.SUBTYPE_2_DYE:
            cid = CID.data.get(self.id, {})
            return cid.get('dyeTtl', 0)
        return 0

    def getRongGuangTtl(self):
        if self.type == Item.BASETYPE_CONSUMABLE and self.cstype == Item.SUBTYPE_2_RONGGUANG:
            cid = CID.data.get(self.id, {})
            return cid.get('rongGuangTtl', 0)
        return 0

    def getRongGuangType(self):
        if self.type == Item.BASETYPE_CONSUMABLE and self.cstype == Item.SUBTYPE_2_RONGGUANG:
            cid = CID.data.get(self.id, {})
            return cid.get('rongGuangType', Item.CONSUME_RONGGUANG_UNKNOW)
        return 0

    def _dyeColor(self, color0, color1, dyeType = const.DYE_COPY):
        if not isinstance(color0, list):
            color0 = list(color0)
        if not isinstance(color1, list):
            color1 = list(color1)
        if dyeType == const.DYE_COPY:
            if color1 and len(color1) == 2:
                return color1
            return color0
        dyeList = []
        if color0 and len(color0) == 2 and color1 and len(color1) == 2:
            for i in xrange(0, 2):
                r, g, b, a = color0[i].split(',')
                w, x, y, z = color1[i].split(',')
                r = float(r) + float(w)
                g = float(g) + float(x)
                b = float(b) + float(y)
                a = float(a) + float(z)
                dyeList.append('%d,%d,%d,%d' % (r * 0.5,
                 g * 0.5,
                 b * 0.5,
                 a * 0.5))

            return dyeList
        if color1 and len(color1) == 2:
            return color1
        return color0

    def setDye(self, dye = None, dyeType = const.DYE_COPY, channel = const.DYE_CHANNEL_1):
        if not dye or len(dye) != 2:
            return
        dyeList = []
        if hasattr(self, 'dyeList'):
            dyeList = list(self.dyeList)
        index = const.DYES_INDEX_DUAL_COLOR if channel == const.DYE_CHANNEL_2 else const.DYES_INDEX_COLOR
        self.dyeList = utils.addDyeLists(dyeList, index, dye)

    def setTexture(self, texture = None):
        if not texture or len(texture) != 3:
            return
        dyeList = []
        if hasattr(self, 'dyeList'):
            dyeList = list(self.dyeList)
        self.dyeList = utils.addDyeLists(dyeList, const.DYES_INDEX_TEXTURE, texture)

    def setDualDye(self, dye = None, dyeType = const.DYE_COPY):
        self.setDye(dye, dyeType, const.DYE_CHANNEL_2)

    def setPbrTextureG(self, textureG = None):
        if not textureG:
            return
        dyeList = []
        if hasattr(self, 'dyeList'):
            dyeList = list(self.dyeList)
        self.dyeList = utils.addDyeLists(dyeList, const.DYES_INDEX_PBR_TEXTURE_DEGREE, textureG)

    def setPbrHL(self, hl, channel = const.DYE_CHANNEL_1):
        if not hl:
            return
        dyeList = []
        if hasattr(self, 'dyeList'):
            dyeList = list(self.dyeList)
        index = const.DYES_INDEX_PBR_DUAL_HIGH_LIGHT if channel == const.DYE_CHANNEL_2 else const.DYES_INDEX_PBR_HIGH_LIGHT
        self.dyeList = utils.addDyeLists(dyeList, index, hl)

    def canRenewalIndependent(self):
        itemData = ID.data.get(self.id)
        if itemData and itemData.has_key('renewalType') and itemData.has_key('ttl'):
            if getattr(self, 'ownershipPercent', 0) < const.ITEM_OWNERSHIP_MAX:
                return True
        return False

    def canRenewalCommon(self):
        itemData = ID.data.get(self.id)
        if itemData:
            if itemData.has_key('commonRenewalType') and itemData.has_key('ttl'):
                return True
        return False

    def flyUpValidCheck(self, owner):
        if flyUpUtils.enableFlyUp() and BigWorld.component != 'client' and owner.flyUpLv < ID.data.get(self.id, {}).get('flyUpLvLimit', 0):
            return False
        return True

    def jingJieValidCheck(self, owner):
        itemData = ID.data.get(self.id)
        if itemData:
            if itemData.has_key('needJingJie') and owner.jingJie < itemData['needJingJie']:
                return False
            else:
                return True

    def isOwnershipPercentMax(self):
        return getattr(self, 'ownershipPercent', const.ITEM_OWNERSHIP_MAX) >= const.ITEM_OWNERSHIP_MAX

    def getRenewalType(self):
        return ID.data.get(self.id, {}).get('renewalType', 0)

    def getCommonRenewalType(self):
        return ID.data.get(self.id, {}).get('commonRenewalType', 0)

    def getEquipGemSlot(self, gemType, gemPos):
        if gemType == self.GEM_TYPE_YANG and hasattr(self, 'yangSlots') and gemPos < len(self.yangSlots):
            return self.yangSlots[gemPos]
        if gemType == self.GEM_TYPE_YIN and hasattr(self, 'yinSlots') and gemPos < len(self.yinSlots):
            return self.yinSlots[gemPos]

    def setSkillCD(self, cdTime):
        setattr(self, 'skillNst', time.time() + cdTime)

    def _canAddGem(self, owner, gemPos, gemItem, isReplace = False, bMsg = True):
        if BigWorld.component in 'cell':
            channel = owner.client
        elif BigWorld.component in 'client':
            channel = owner
        if not gemItem or gemItem.type != self.BASETYPE_EQUIP_GEM:
            return False
        if not EGD.data.has_key(gemItem.getParentId()):
            return False
        if not self.isEquip():
            return False
        if self.isYaoPei():
            return False
        if self.isGuanYin():
            return False
        if self.hasLatch():
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_LATCH, ())
            return False
        if gemItem.hasLatch():
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_GEM_LATCH, ())
            return False
        if not hasattr(self, 'yangSlots') and not hasattr(self, 'yinSlots'):
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_NO_SLOTS, ())
            return False
        gemData = utils.getEquipGemData(gemItem.id)
        gemSlot = self.getEquipGemSlot(gemData.get('type'), gemPos)
        if not gemSlot or not isReplace and not gemSlot.isEmpty():
            return False
        ed = ED.data.get(self.id, {})
        order = self.addedOrder
        if gemData.has_key('orderLimit') and order < gemData['orderLimit']:
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_ORDER, ())
            return False
        gtp = ed.get('gemEquipType')
        if gemData.has_key('equipLimit') and gtp not in gemData['equipLimit']:
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_EQUIPTYPE, ())
            return False
        if not gemItem.ownedBy(owner.gbId):
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_OWNER, ())
            return False
        return True

    def hasGem(self):
        return any([ sVal.gem for sVal in getattr(self, 'yinSlots', ()) + getattr(self, 'yangSlots', ()) ])

    def getHungerDuraFactor(self):
        if not self._checkEquipDuraValid():
            return (const.RIDE_WING_DURA_NORMAL, '', 1)
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableRideWingDurability():
                return (const.RIDE_WING_DURA_NORMAL, '', 1)
        if BigWorld.component in 'client':
            if not gameglobal.rds.configData.get('enableRideWingDurability', False):
                return (const.RIDE_WING_DURA_NORMAL, '', 1)
        data = None
        if self.isWingEquip():
            data = SCD.data.get('WingHungerStates')
        if not data:
            data = SCD.data.get('hungerStates')
        for state, (text, start, end, velocityFactor) in zip([const.RIDE_WING_DURA_HUNGRY,
         const.RIDE_WING_DURA_TIRED,
         const.RIDE_WING_DURA_NORMAL,
         const.RIDE_WING_DURA_FULL], data):
            if start <= int(self.cdura * 1.0 / self.initMaxDura * 100) <= end:
                return (state, text, velocityFactor)

        return (const.RIDE_WING_DURA_NORMAL, '未知', 1)

    def getVelocityDuraFactor(self):
        return self.getHungerDuraFactor()[2]

    def getVelocityFactorByVip(self, owner):
        if self.isWingEquip():
            return owner.vipRevise(gametypes.VIP_SERVICE_WING_SPEED_UP, 1, True)
        elif self.isRideEquip():
            return owner.vipRevise(gametypes.VIP_SERVICE_RIDE_SPEED_UP, 1, True)
        else:
            return 1

    def getCoupleEmoteVelocityFactor(self):
        factor = 1.0
        if hasattr(self, 'rideWingStage'):
            factor = HWUD.data.get((self.quality, self.getVehicleType(), self.rideWingStage), {}).get('coupleEmoteVelocityFactor', 1.0)
        return factor

    def isWingOrRide(self):
        return self.isWingEquip() or self.isRideEquip()

    def isWingEquip(self):
        return self.isEquip() and gametypes.EQU_PART_WINGFLY in self.whereEquip()

    def isRideEquip(self):
        return self.isEquip() and gametypes.EQU_PART_RIDE in self.whereEquip()

    def isSwimRide(self):
        if self.isRideEquip():
            return ED.data.get(self.id, {}).get('swimRide', False)
        return False

    def isFlyRide(self):
        if self.isRideEquip():
            return ED.data.get(self.id, {}).get('flyRide', False)
        return False

    def canSwim(self):
        if self.isSwimRide():
            return self.haveTalent(gametypes.RIDE_TALENT_SWIM)
        return False

    def canOnlySwim(self):
        if self.isSwimRide():
            return ED.data.get(self.id, {}).get('canOnlySwim', False)
        return False

    def haveTalent(self, talent):
        return talent in getattr(self, 'talents', [])

    def availableTalents(self):
        if not self.isWingOrRide():
            return []
        return ED.data.get(self.id, {}).get('talents', [])

    @property
    def maxAutoUpgradeStage(self):
        if not self.isWingOrRide():
            return 0
        return ED.data.get(self.id, {}).get('maxAutoUpgradeStage', 0)

    @property
    def maxRideWingStage(self):
        if not self.isWingOrRide():
            return 0
        return ED.data.get(self.id, {}).get('maxStage', 0)

    def canAutoUpgradeStage(self):
        return getattr(self, 'rideWingStage', 0) < self.maxAutoUpgradeStage

    def canRideWingUpgradeConsumeInv(self):
        if not self.isWingOrRide():
            return False
        if self.rideWingStage >= self.maxRideWingStage:
            return False
        if self.starExp < self.getRideWingMaxUpgradeExp():
            return False
        return True

    def recalcWingRideTalents(self, owner = None, needCalcProps = True):
        if not self.isWingOrRide():
            return
        if not hasattr(self, 'rideWingStage'):
            return
        if self.getHungerDuraFactor()[0] == const.RIDE_WING_DURA_HUNGRY:
            self.talents = []
            return
        hwtd = HWTD.data.get((self.id, self.rideWingStage), {})
        activeTalents = hwtd.get('talents', [])
        if not set(activeTalents).issubset(set(self.availableTalents())):
            gameengine and gameengine.reportCritical('@zqc 配表错误，升级到不匹配的天赋 itemId[%d], stage[%d]' % (self.id, self.rideWingStage))
        self.talents = copy.copy(list(activeTalents))
        if self.haveTalent(gametypes.RIDE_TALENT_DRAG_TAIL):
            if not hasattr(self, 'flyTailEffect') and hwtd.has_key('flyTailEffect'):
                self.flyTailEffect = hwtd['flyTailEffect']
        if owner and BigWorld.component == 'cell':
            if self in owner.realEquipment:
                part = self.getRideWingPart()
                if part:
                    it = owner.realEquipment.get(part)
                    if it:
                        Equipment.unApplyEquip(owner, it)
                    owner.updateExistRideWingEffect(part)
                    if it:
                        Equipment.applyEquip(owner, it)
                owner.recalcTopSpeed()
                if needCalcProps:
                    owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)

    def canRideWingUpgrade(self):
        if not self.isWingOrRide():
            return False
        if not hasattr(self, 'rideWingStage'):
            return
        return self.rideWingStage < self.maxRideWingStage

    def setRideWingDuraDecay(self, owner, factor, ttl, opNUID):
        self.rideWingStates['cduraDecayExpireTime'] = utils.getNow() + ttl
        self.rideWingStates['cduraDecay'] = factor
        owner.logItem(self, 0, opNUID, LSDD.data.LOG_SRC_RIDE_WING_BUF_CHANGE, fromGuid=[], toGuid=[], detail='%s %s' % ('duraDecay', self.rideWingStates), bagType=const.RES_KIND_EQUIP)
        owner.client.showGameMsg(GMDD.data.RIDE_WING_DURA_DECAY_FACTOR, (self.name, ttl / const.SECONDS_PER_DAY, int((1 - factor) * 100)))
        self.transRideWingPropToClient(owner)

    def addRideWingDura(self, owner, dura, opNUID):
        oldCdura = self.cdura
        self.cdura = min(self.cdura + dura, self.initMaxDura)
        owner.client.showGameMsg(GMDD.data.RIDE_WING_DURA_ADD, (self.name, const.DURA_TEXT[self.getVehicleType()], math.ceil(self.cdura - oldCdura)))
        self.recalcWingRideTalents(owner)
        self.transRideWingPropToClient(owner)

    def addRideWingExp(self, owner, exp, opNUID):
        if self.starExp >= self.getRideWingMaxUpgradeExp() and not self.canAutoUpgradeStage():
            return False
        realAddExp = self.incRideWingExp(owner, exp, opNUID, isRaw=True)
        owner.client.showGameMsg(GMDD.data.RIDE_WING_EXP_ADD, (self.name, math.ceil(realAddExp)))
        self.transRideWingPropToClient(owner)
        return True

    def setExpBoostState(self, owner, factor, ttl, opNUID):
        self.rideWingStates['expBoostExpireTime'] = utils.getNow() + ttl
        self.rideWingStates['expBoost'] = factor
        owner.logItem(self, 0, opNUID, LSDD.data.LOG_SRC_RIDE_WING_BUF_CHANGE, fromGuid=[], toGuid=[], detail='%s %s' % ('expBoost', self.rideWingStates), bagType=const.RES_KIND_EQUIP)
        owner.client.showGameMsg(GMDD.data.RIDE_WING_DURA_EXP_BOOST, (self.name, ttl / const.SECONDS_PER_DAY, int((factor - 1) * 100)))
        self.transRideWingPropToClient(owner)

    def setRideWingDuraHold(self, owner, ttl, opNUID):
        self.rideWingStates['cduraHoldExpireTime'] = utils.getNow() + ttl
        self.cdura = self.initMaxDura
        owner.logItem(self, 0, opNUID, LSDD.data.LOG_SRC_RIDE_WING_BUF_CHANGE, fromGuid=[], toGuid=[], detail='%s %s' % ('duraHold', self.rideWingStates), bagType=const.RES_KIND_EQUIP)
        owner.client.showGameMsg(GMDD.data.RIDE_WING_DURA_HOLD, (self.name, const.DURA_TEXT[self.getVehicleType()], ttl / const.SECONDS_PER_DAY))
        self.recalcWingRideTalents(owner)
        self.transRideWingPropToClient(owner)

    def getRideWingPart(self):
        if not self.isWingOrRide():
            return None
        elif self.isWingEquip():
            return gametypes.EQU_PART_WINGFLY
        else:
            return gametypes.EQU_PART_RIDE

    def setRideWingDragTailEffect(self, owner, effect, ttl, opNUID):
        self.rideWingStates['flyTailEffect'] = effect
        self.rideWingStates['flyTailEffectExpireTime'] = utils.getNow() + ttl
        owner.updateExistRideWingEffect(self.getRideWingPart())
        owner.logItem(self, 0, opNUID, LSDD.data.LOG_SRC_RIDE_WING_BUF_CHANGE, fromGuid=[], toGuid=[], detail='%s %s' % ('dragTailEffect', self.rideWingStates), bagType=const.RES_KIND_EQUIP)
        self.transRideWingPropToClient(owner)

    def getDragTailEffectExpireTime(self):
        if not hasattr(self, 'rideWingStates'):
            return const.EXPIRE_TIME_INFINITE
        return self.rideWingStates.get('flyTailEffectExpireTime', const.EXPIRE_TIME_INFINITE)

    def getRideWingFlyTailEffect(self):
        if not self.haveTalent(gametypes.RIDE_TALENT_DRAG_TAIL):
            return 0
        if self.rideWingStates.get('flyTailEffectExpireTime', 0) > utils.getNow():
            return self.rideWingStates.get('flyTailEffect', 0)
        return getattr(self, 'flyTailEffect', 0)

    def isRideWingDuraDecayState(self):
        return hasattr(self, 'rideWingStates') and self.rideWingStates.get('cduraDecayExpireTime', 0) > utils.getNow()

    def isRideWingExpBoostState(self):
        return hasattr(self, 'rideWingStates') and self.rideWingStates.get('expBoostExpireTime', 0) > utils.getNow()

    def isRideWingDuraHoldState(self):
        return hasattr(self, 'rideWingStates') and self.rideWingStates.get('cduraHoldExpireTime', 0) > utils.getNow()

    def isRideWingTailEffectState(self):
        return hasattr(self, 'rideWingStates') and self.rideWingStates.get('flyTailEffectExpireTime', 0) > utils.getNow()

    def rideWingDuraDecayFactor(self):
        if self.isRideWingDuraHoldState():
            return 0
        if self.isRideWingDuraDecayState():
            return self.rideWingStates.get('cduraDecay', 1)
        return 1

    def rideWingExpBoostFactor(self):
        if self.isRideWingExpBoostState():
            return self.rideWingStates.get('expBoost', 1)
        return 1

    def getVehicleType(self):
        if not self.isWingOrRide():
            return const.PLAYER_VEHICLE_FOOT
        elif self.isWingEquip():
            return const.PLAYER_VEHICLE_WING
        else:
            return const.PLAYER_VEHICLE_RIDE

    def getRideWingSpeedId(self, inCombat = False):
        if inCombat:
            keyName = 'combatSpeedId'
        else:
            keyName = 'speedId'
        if self.isSwitchSpeedSubId():
            if not inCombat and getattr(self, 'switchNonCombatSpeedSubId', None) is not None:
                return self.switchNonCombatSpeedSubId
            if inCombat and getattr(self, 'switchCombatSpeedSubId', None) is not None:
                return self.switchCombatSpeedSubId
        newSpeedId = 0
        if hasattr(self, 'rideWingStage'):
            newSpeedId = HWUD.data.get((self.quality, self.getVehicleType(), self.rideWingStage), {}).get(keyName)
        if newSpeedId:
            return newSpeedId
        subId = ED.data.get(self.id, {}).get('subId', [0])[0]
        subData = HWD.data.get(subId, {})
        if subData:
            return subData[0].get(keyName, None)
        else:
            return subId

    def getRideWingMaxUpgradeExp(self):
        if not hasattr(self, 'rideWingStage'):
            return 0
        return HWUD.data.get((self.quality, self.getVehicleType(), self.rideWingStage), {}).get('maxExp', 1)

    @commonDecorator.callonserver
    def incRideWingExp(self, owner, val, opNUID, isRaw = False):
        realAddStarExp = 0
        if not self.isWingOrRide():
            return 0
        if not hasattr(self, 'rideWingStage'):
            return 0
        oldStarExp = self.starExp
        if isRaw:
            self.starExp += val
        else:
            if val * self.rideWingExpBoostFactor() == 0:
                return
            self.starExp += val * self.rideWingExpBoostFactor()
        realAddStarExp = self.starExp - oldStarExp
        while True:
            curMaxExp = self.getRideWingMaxUpgradeExp()
            if self.starExp >= curMaxExp:
                if self.canAutoUpgradeStage():
                    _, part = owner.equipment.findEquipByUUID(self.uuid)
                    if part != const.CONT_NO_POS:
                        Equipment.unApplyEquip(owner, self)
                    self.rideWingStage += 1
                    if part != const.CONT_NO_POS:
                        Equipment.applyEquip(owner, self)
                    self.starExp -= curMaxExp
                    serverlog.markEquipStarExpLog(owner, self, oldStarExp, self.starExp, self.rideWingStage, logType=LSDD.data.LOG_SRC_RIDE_WING_UPGRADE)
                    oldStarExp = self.starExp
                    self.recalcWingRideTalents(owner)
                    if self.isWingEquip():
                        owner.base.syncWingSharedAttr()
                    else:
                        owner.base.syncRideSharedAttr()
                else:
                    self.starExp = curMaxExp
                    realAddStarExp -= self.starExp - curMaxExp
                    if oldStarExp != self.starExp and self.canRideWingUpgradeConsumeInv():
                        owner.client.showGameMsg(GMDD.data.RIDE_WING_CAN_UPGRADE, (self.name,))
                    break
            else:
                break

        return realAddStarExp

    @commonDecorator.callonserver
    def reduceRideWingDurability(self, owner, many, opNUID):
        if not self._checkEquipDuraValid():
            return
        if not self.isWingOrRide():
            return
        if BigWorld.component in ('base', 'cell') and not gameconfig.enableRideWingDurability():
            return
        subMany = many * self.rideWingDuraDecayFactor()
        if self.isWingEquip():
            subMany = owner.vipRevise(gametypes.VIP_SERVICE_WING_WEAR, subMany, False)
        elif self.isRideEquip():
            subMany = owner.vipRevise(gametypes.VIP_SERVICE_MOUNT_HUNGER, subMany, False)
        if subMany:
            prevDuraState = self.getHungerDuraFactor()[0]
            prevDura = self.cdura
            self.cdura = limit(self.cdura - subMany, 0.0, self.initMaxDura)
            if self.cdura == 0:
                self.cdura = const.RIDE_WING_MIN_DURA
            nowDuraState = self.getHungerDuraFactor()[0]
            if prevDuraState != nowDuraState:
                owner.logItem(self, 0, opNUID, LSDD.data.LOG_SRC_RIDE_WING_DURA_CHANGE, fromGuid=[], toGuid=[], detail='%d %d' % (prevDura, self.cdura), bagType=const.RES_KIND_EQUIP)
                self.recalcWingRideTalents(owner)
            return

    @commonDecorator.callonserver
    def transRideWingPropToClient(self, owner):
        part = None
        if not hasattr(self, 'rideWingStage'):
            return
        if self.isWingEquip():
            part = gametypes.EQU_PART_WINGFLY
        elif self.isRideEquip():
            part = gametypes.EQU_PART_RIDE
        else:
            return
        normalDict = {'talents': self.talents,
         'cdura': self.cdura,
         'starExp': self.starExp,
         'rideWingStage': self.rideWingStage,
         'rideWingStates': getattr(self, 'rideWingStates', {})}
        owner.client.rideWingPropChanged(part, normalDict)

    def getRideWingTotalExp(self):
        if not self.isWingOrRide():
            return 0
        totalExp = getattr(self, 'starExp', 0)
        stageCursor = getattr(self, 'rideWingStage', 0) - 1
        while stageCursor > 0:
            totalExp += HWUD.data.get((self.quality, self.getVehicleType(), stageCursor), {}).get('maxExp', 0)
            stageCursor -= 1

        return totalExp

    def isSwitchSpeedSubId(self):
        return getattr(self, 'speedSwitchExpireTime', 0) > utils.getNow()

    def setSwitchSpeedSubId(self, nonCombatSubId, combatSubId, expireTime):
        self.speedSwitchExpireTime = expireTime
        self.switchNonCombatSpeedSubId = nonCombatSubId
        self.switchCombatSpeedSubId = combatSubId

    def setIdentified(self, identifyId, quality):
        self.identifyId = identifyId
        self.identifyQuality = quality

    def isUndentifiedType(self):
        return self.type == self.BASETYPE_UNIDENTIFIED

    def canBeIdentified(self):
        if not self.isUndentifiedType():
            return
        return hasattr(self, 'identifyId') and hasattr(self, 'identifyQuality')

    def getIdentifyQuality(self):
        if hasattr(self, 'identifyQuality'):
            return self.identifyQuality
        else:
            return ID.data.get(self.id, {}).get('identifyQuality', 0)

    def getIdentifyTargetItem(self):
        if not self.canBeIdentified():
            return None
        return utils.getFinalLifeSkillByQuality(self.identifyId, self.identifyQuality)

    def getIdentifyType(self):
        if not self.canBeIdentified():
            return 0
        return ID.data.get(self.identifyId, {}).get('identifyType', 0)

    def getLifeEquToolProb(self):
        if not self.isLifeEquip():
            return 0
        return LSED.data.get(self.id, {}).get('identifyProb', 0)

    def getLifeEquToolQuality(self):
        if not self.isLifeEquip():
            return 0
        return LSED.data.get(self.id, {}).get('identifyQuality', 0)

    def getLifeEquSuccProb(self):
        if not self.isLifeEquip():
            return 0
        return LSED.data.get(self.id, {}).get('succProb', 0)

    def ownedBy(self, gbId):
        if not hasattr(self, 'ownerGbId'):
            return True
        if not self.ownerGbId or self.ownerGbId == gbId:
            return True
        return False

    def setOwner(self, gbId, ownerName):
        self.ownerGbId = gbId
        self.ownerRoleName = ownerName

    def setTwoSinger(self, signerOne, signerTwo):
        self.signerOne = signerOne
        self.signerTwo = signerTwo

    def addEquipGem(self, owner, gemPos, gemItem):
        if not self._canAddGem(owner, gemPos, gemItem):
            return False
        gemData = utils.getEquipGemData(gemItem.id)
        gemSlot = self.getEquipGemSlot(gemData.get('type'), gemPos)
        gemSlot.fillGem(gemItem)
        self.bindItem()
        gemItem.bindItem()
        self.calcScores(extra={'owner': owner})
        return True

    def _canRemoveGem(self, owner, gemType, gemPos):
        if not self.isEquip():
            return False
        if not hasattr(self, 'yangSlots') and not hasattr(self, 'yinSlots'):
            return False
        gemSlot = self.getEquipGemSlot(gemType, gemPos)
        if not gemSlot or not gemSlot.isFilled():
            gamelog.error('zt: cannot remove equip gem', owner.id, self.id, gemSlot)
            return False
        if not EGD.data.has_key(gemSlot.gem.getParentId()):
            gemSlot.removeGem()
            return False
        if self.hasLatch():
            return False
        return True

    def removeEquipGem(self, owner, gemType, gemPos):
        if not self._canRemoveGem(owner, gemType, gemPos):
            return None
        gemSlot = self.getEquipGemSlot(gemType, gemPos)
        if not gemSlot:
            return None
        gemItem = gemSlot.removeGem()
        self.calcScores(extra={'owner': owner})
        return gemItem

    def unlockGemSlot(self, owner, gemType, gemPos, needBind):
        gemSlot = self.getEquipGemSlot(gemType, gemPos)
        if not gemSlot or not gemSlot.isLocked():
            return False
        gemSlot.unlock()
        if needBind:
            self.bindItem()
        return True

    def inheritYinYangSlots(self, fromEquip):
        data = ED.data.get(self.id, {})
        if hasattr(fromEquip, 'yinSlots') and (data.has_key('yinSlots') or data.has_key('lockedYinSlots')):
            self.yinSlots = []
            nInitOpenSlot = data.get('yinSlots', 0)
            nInitLockedSlot = data.get('lockedYinSlots', 0)
            nOpenSlotSrc = len([ sVal for sVal in fromEquip.yinSlots if not sVal.isLocked() ])
            nOpenSlot = min(max(nOpenSlotSrc, nInitOpenSlot), nInitOpenSlot + nInitLockedSlot)
            nLockedSlot = nInitLockedSlot - (nOpenSlot - nInitOpenSlot)
            for i in range(nOpenSlot):
                self.yinSlots.insert(0, GemSlot(self.GEM_SLOT_EMPTY))

            for i in range(nLockedSlot):
                self.yinSlots.append(GemSlot(self.GEM_SLOT_LOCKED))

        if hasattr(fromEquip, 'yangSlots') and (data.has_key('yangSlots') or data.has_key('lockedYangSlots')):
            self.yangSlots = []
            nInitOpenSlot = data.get('yangSlots', 0)
            nInitLockedSlot = data.get('lockedYangSlots', 0)
            nOpenSlotSrc = len([ sVal for sVal in fromEquip.yangSlots if not sVal.isLocked() ])
            nOpenSlot = min(max(nOpenSlotSrc, nInitOpenSlot), nInitOpenSlot + nInitLockedSlot)
            nLockedSlot = nInitLockedSlot - (nOpenSlot - nInitOpenSlot)
            for i in range(nOpenSlot):
                self.yangSlots.insert(0, GemSlot(self.GEM_SLOT_EMPTY))

            for i in range(nLockedSlot):
                self.yangSlots.append(GemSlot(self.GEM_SLOT_LOCKED))

        for pos, sVal in enumerate(getattr(self, 'yinSlots', [])):
            sVal.pos = pos

        for pos, sVal in enumerate(getattr(self, 'yangSlots', [])):
            sVal.pos = pos

    def isMallFashionRenewable(self):
        itemData = ID.data.get(self.id)
        if not itemData:
            return False
        if self.isOwnershipPercentMax():
            return False
        if not itemData.get('canRenewal', False):
            return False
        if 'mallRenewal30Days' in itemData or 'mallRenewalForever' in itemData:
            return True
        return False

    def isFashionEquip(self):
        if not hasattr(self, 'equipType'):
            return False
        return self.equipType in Item.FASHION_BAG_ALL and self.equipSType in Item.FASHION_BAG_ALL[self.equipType]

    def isYaoPeiMixMaterial(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_YAOPEI_MIX_MATERIAL

    def isYaoPei(self):
        if not hasattr(self, 'equipType'):
            return False
        return self.equipType == Item.EQUIP_BASETYPE_JEWELRY and self.equipSType == Item.EQUIP_JEWELRY_SUBTYPE_YAOPEI

    def isAddStarExpItem(self):
        return hasattr(self, 'cstype') and (self.cstype == self.SUBTYPE_2_ADD_EQUIP_STAR_EXP or self.cstype == self.SUBTYPE_2_EQUIP_STAR_EXP)

    def isEquipStarExpItem(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_EQUIP_STAR_EXP

    def canUseAddStarExpItem(self):
        ed = ED.data.get(self.id)
        if not ed:
            return False
        etp = ed.get('equipType')
        if etp == self.EQUIP_BASETYPE_WEAPON:
            return True
        if etp == self.EQUIP_BASETYPE_ARMOR:
            armorSType = ed.get('armorSType')
            if armorSType in (self.EQUIP_FASHION_SUBTYPE_HEAD,
             self.EQUIP_FASHION_SUBTYPE_BODY,
             self.EQUIP_FASHION_SUBTYPE_HAND,
             self.EQUIP_FASHION_SUBTYPE_LEG,
             self.EQUIP_FASHION_SUBTYPE_SHOE):
                return True
        elif etp == self.EQUIP_BASETYPE_JEWELRY:
            jewelSType = ed.get('jewelSType')
            if jewelSType in (self.EQUIP_JEWELRY_SUBTYPE_NECKLACE, self.EQUIP_JEWELRY_SUBTYPE_RING, self.EQUIP_JEWELRY_SUBTYPE_EARRING):
                return True
        return False

    def isEquipGem(self):
        return self.type == Item.BASETYPE_EQUIP_GEM

    def getRaffleId(self):
        return CID.data.get(self.id, {}).get('raffleId', 0)

    def isRaffle(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_RAFFLE

    def getLotteryId(self):
        return ID.data.get(self.id, {}).get('lotteryId', 0)

    def isLottery(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_LOTTERY

    def isStorehouse(self):
        return CID.data.get(self.id, {}).get('sType', 0) == self.SUBTYPE_2_CBT

    def isGuildDonateItem(self):
        return self.isMojing() or self.isXirang() or self.isWood() or self.isGuildMoney() or self.isGuildOtherRes() or self.isWingWorldGuildMoney()

    def isWingWorldGuildMoney(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_TIAN_YU_CAN_JING and wingWorldUtils.isOpenWingWorld()

    def isMallDiscount(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_MALL_DISCOUNT

    def isEquipSoulStar(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_EQUIP_SOUL_STAR

    def isSkillAppearanceItem(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_ENABLE_SKILL_APPEARANCE

    def isActEffectAppearanceItem(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_ACT_APPEARANCE

    def hasFashionTransPropExpire(self):
        srcItemId, srcSuitId, expireTime = self.fashionTransProp
        if expireTime <= 0:
            return False
        if utils.getDaySecond(expireTime) + 86400 < utils.getNow():
            self.delProp(('fashionTransProp',))
            return True
        return False

    def hasRarePrefixProp(self):
        if not self.isEquip():
            return 0
        if not getattr(self, 'prefixInfo', None):
            return 0
        for prefixItem in EPFPD.data.get(self.prefixInfo[0], {}):
            if prefixItem.get('id') == self.prefixInfo[1]:
                return prefixItem.get('isRare', 0)

        return 0

    def checkCanConvertBind(self):
        """
        \xd7\xaa\xb0\xf3\xc7\xb0\xd6\xc3\xcc\xf5\xbc\xfe
        :return:
        """
        if self.getTTLExpireTime():
            return False
        if self.isOneMall():
            return False
        itemData = ID.data[self.id]
        if itemData.get('mallItem'):
            return False
        if self.isEquip() or self.isLifeEquip():
            return False
        mutableAttrs = ('ownerGbId', 'cdura', 'ownershipPercent', 'timeLimit')
        for attr in mutableAttrs:
            if hasattr(self, attr):
                return False

        key1 = (self.type, self.stype, getattr(self, 'cstype', 0))
        key2 = (self.type, self.stype, 0)
        key3 = (self.type, 0, 0)
        for key in [key1, key2, key3]:
            if key not in BCITD.data:
                continue
            bindData = BCITD.data.get(key)
            if bindData.get('convertible', False):
                return True
            return False

        return False

    def getBindConvertId(self):
        """
        \xd7\xaa\xbb\xbb\xb9\xe6\xd4\xf2\xa3\xba\xd1\xa1\xd4\xf1\xcd\xac\xb8\xb8ID\xd6\xd0\xcc\xec\xc9\xfa\xb0\xf3\xb6\xa8\xb5\xc4\xc4\xc7\xb8\xf6\xce\xef\xc6\xb7
        
        :return: 0 if cannot convert to bound else return the target item id
        """
        if not self.checkCanConvertBind():
            return 0
        if self.id in ICBD.data:
            return ICBD.data.get(self.id).get('bindItemId', 0)
        subIds = IPD.data.get(self.getParentId())
        if not subIds:
            return 0
        candSubIds = []
        for subId in subIds:
            itemData = ID.data.get(subId)
            if not itemData:
                return 0
            if itemData.get('mallItem'):
                continue
            if itemData.get('bindType') == gametypes.ITEM_BIND_TYPE_FOREVER:
                candSubIds.append(subId)

        if candSubIds:
            minSubId = min(candSubIds)
            if minSubId == self.id:
                return 0
            else:
                return minSubId
        return 0

    def addEquipSuit(self, suitId, consumedItemId):
        setattr(self, 'addedSuitId', (suitId, consumedItemId))

    def hasCbtInfo(self):
        if hasattr(self, 'cbtInfo'):
            return True
        else:
            return False

    def setCbtInfo(self, info):
        if BigWorld.component == 'client':
            return
        if self.hasCbtInfo():
            return
        setattr(self, 'cbtInfo', info)

    def setMarriageInfo(self, wifeRoleName, husbandRoleName):
        if BigWorld.component == 'client':
            return
        setattr(self, 'wifeRoleName', wifeRoleName)
        setattr(self, 'husbandRoleName', husbandRoleName)

    def setTargetInfo(self, tgtGbId, tgtName):
        if BigWorld.component == 'client':
            return
        setattr(self, 'targetGbId', tgtGbId)
        setattr(self, 'targetName', tgtName)

    def isPerfertRefined(self, owner):
        if self.getRealEnhlv(owner) != self.getMaxEnhLv(owner):
            return False
        if not hasattr(self, 'enhanceRefining'):
            return False
        for lv in xrange(1, self.getRealEnhlv(owner) + 1):
            enhEffects = EERD.data.get(lv, {}).get('enhEffects', [(0.02, (10017, 30, 20, 10))])
            if self.enhanceRefining.get(lv, 0) < enhEffects[-1][0]:
                return False

        return True

    def __initYaoPei(self):
        self.yaoPeiExp = 0
        self.maxYaoPeiExp = 0
        self.yaoPeiMaterialWeekly = 0
        self.lastAddYaoPeiExpTime = 0
        self.yaoPeiScore = 0
        self.yaoPeiProps = self.__initYaoPeiBaseProps()
        self.yaoPeiExtraProps = self.__initYaoPeiExtraProps()
        self.yaoPeiSkillId = self.__initYaoPeiSkill()
        self.calcYapPeiScore()
        self.initYaoPeiScore = self.yaoPeiScore
        commcalc.calcPursueYaoPeiData(self)

    def __initYaoPeiBaseProps(self):
        pd = YPD.data.get(self.id)
        if not pd:
            return []
        props = []
        for pId, pType, minVal, maxVal, rData in pd.get('basicProps', []):
            rVal = randint(0, sum(rData))
            idx = 0
            tSum = 0
            for i, v in enumerate(rData):
                tSum += v
                if rVal < tSum:
                    idx = i
                    break

            interval = (maxVal - minVal) / len(rData)
            rMinVal = minVal + idx * interval
            rMaxVal = rMinVal + interval
            rPropVal = uniform(rMinVal, rMaxVal)
            props.append((pId, pType, rPropVal))

        return props

    def __initYaoPeiExtraProps(self):
        pd = YPD.data.get(self.id)
        if not pd:
            return []
        extraProps = []
        for poolId, lv in pd.get('extraProps', []):
            ed = YEPD.data.get(poolId)
            if not ed:
                continue
            red = random.choice(ed)
            pId = red['aid']
            pType = red['atype']
            minVal = uniform(*red['minValue'])
            maxVal = uniform(*red['maxValue'])
            interval = red['interval']
            tt = randint(0, math.ceil((maxVal - minVal) / interval))
            pVal = min(minVal + tt * interval, maxVal)
            extraProps.append((pId,
             pType,
             round(pVal, 2),
             round(minVal, 2),
             round(maxVal, 2),
             lv))

        return extraProps

    def __initYaoPeiSkill(self):
        pd = YPD.data.get(self.id)
        if not pd:
            return 0
        r = randint(*const.RANDOM_RATE_BASE_10K)
        tSum = 0
        rSkId = 0
        for skId, _, prob in pd.get('randSkill', []):
            tSum += prob
            if r < tSum:
                rSkId = skId
                break

        return rSkId

    def calcYaoPeiLv(self):
        if not hasattr(self, 'yaoPeiExp'):
            return 1
        maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
        for lv in range(1, maxYaoPeiLv + 1):
            if self.yaoPeiExp < YLED.data.get((self.quality, lv), {}).get('exp', 0):
                return lv - 1

        return maxYaoPeiLv

    def getYaoPeiLv(self):
        return self.calcYaoPeiLv()

    def getYaoPaiLvUpExp(self):
        if not hasattr(self, 'yaoPeiExp'):
            return (0, 1)
        curLv = 1
        for lv in range(1, 21):
            if self.yaoPeiExp < YLED.data.get((self.quality, lv), {}).get('exp', 0):
                curLv = lv - 1
                break

        nextLv = curLv + 1
        curNeedExp = YLED.data.get((self.quality, curLv), {}).get('exp', 0)
        nextNeedExp = YLED.data.get((self.quality, nextLv), {}).get('exp', 1)
        needExp = nextNeedExp - curNeedExp
        hasExp = self.yaoPeiExp - curNeedExp
        return (hasExp, needExp)

    def setYaoPeiLv(self, lv):
        if not self.isYaoPei():
            return
        maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
        if lv < 0 or lv > maxYaoPeiLv:
            return
        self.yaoPeiExp = YLED.data.get((self.quality, lv), {}).get('exp', 0)

    def getYaoPeiMaterialWeekly(self):
        if not hasattr(self, 'yaoPeiMaterialWeekly') or not hasattr(self, 'lastAddYaoPeiExpTime'):
            return 0
        elif self.lastAddYaoPeiExpTime and not utils.isSameWeek(self.lastAddYaoPeiExpTime):
            return 0
        else:
            return self.yaoPeiMaterialWeekly

    def getYaoPeiPursueNum(self):
        if not hasattr(self, 'lastAddYaoPeiExpTime') or not self.lastAddYaoPeiExpTime or self.lastAddYaoPeiExpTime and not utils.isSameWeek(self.lastAddYaoPeiExpTime):
            commcalc.calcPursueYaoPeiData(self)
        curPursueNum = getattr(self, 'curPursueNum', 0)
        maxPursueNum = getattr(self, 'maxPursueNum', 0)
        return (curPursueNum, maxPursueNum)

    def getYaoPeiPropsAdd(self, lv):
        propsAdd = YLD.data.get(lv, {})
        basicAdd = propsAdd.get('basicAdd', 0)
        extraAdd = propsAdd.get('extraAdd', 0)
        skillLv = propsAdd.get('skillLv', 0)
        return (basicAdd, extraAdd, skillLv)

    def calcMaxYaoPeiLv(self):
        if not hasattr(self, 'maxYaoPeiExp'):
            return 1
        maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
        for lv in range(1, maxYaoPeiLv + 1):
            if self.maxYaoPeiExp < YLED.data.get((self.quality, lv), {}).get('exp', 0):
                return lv - 1

        return maxYaoPeiLv

    def getMaxYaoPeiLv(self):
        return self.calcMaxYaoPeiLv()

    def calcYapPeiScore(self):
        if not self.isYaoPei():
            return 0
        ypLv = self.getYaoPeiLv()
        basicAdd, extraAdd, skLv = self.getYaoPeiPropsAdd(ypLv)
        print '@zs calcScore1:', ypLv, basicAdd, extraAdd, skLv, self.yaoPeiProps, self.yaoPeiExtraProps
        baseScore = 0
        for pId, pType, pVal in self.yaoPeiProps:
            param = PRD.data.get(pId, {}).get('yaopeiBaseCoeff', 0)
            baseScore += pVal * basicAdd * param

        extraScore = 0
        for pId, pType, pVal, minVal, maxVal, lv in self.yaoPeiExtraProps:
            pd = PRD.data.get(pId, {})
            rangeParam = pd.get('yaopeiExtraRangeCoeff', (0, 0))
            valParam = pd.get('yaopeiExtraValueCoeff', 0)
            extraScore += minVal * extraAdd * rangeParam[0] + maxVal * extraAdd * rangeParam[1]
            if ypLv >= lv:
                extraScore += pVal * extraAdd * valParam

        skillScore = 0
        if self.yaoPeiSkillId:
            skLv = YLD.data.get(ypLv, {}).get('skillLv', 0)
            pd = YPD.data.get(self.id, {})
            for skId, param, _ in pd.get('randSkill', []):
                if skId == self.yaoPeiSkillId:
                    skillScore += param[0] + param[1] * skLv
                    break

        rprop = self.rprops if hasattr(self, 'rprops') else []
        d = defaultdict(lambda : 0)
        for pid, ptp, value in rprop:
            d[pid, ptp] += value

        rPropScore = 0
        for key, value in d.iteritems():
            pid, ptp = key
            data = PRD.data.get(pid)
            if not data:
                continue
            if ptp == gametypes.DATA_TYPE_NUM:
                coeff = data.get('scoreCoeffNum', 0)
            else:
                coeff = data.get('scoreCoeffPercent', 0)
            rPropScore += value * coeff

        factor = YLD.data.get(self.getYaoPeiLv(), {}).get('extraAdd', 1)
        rPropScore *= factor
        self.yaoPeiScore = int(baseScore + extraScore + skillScore + rPropScore)
        gamelog.debug('zs: calcYaoPei score ', self.id, self.yaoPeiScore, baseScore, extraScore, skillScore, rPropScore)
        self.score = self.yaoPeiScore

    def isSpriteTextBook(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_SPRITE_TEXTBOOK

    def isGuanYin(self):
        if not hasattr(self, 'equipType'):
            return False
        return self.equipType == Item.EQUIP_BASETYPE_ARMOR and self.equipSType == Item.EQUIP_ARMOR_SUBTYPE_GUANYIN

    def isGuanYinNormalSkillBook(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_GUANYIN_NORMAL_SKILL_BOOK

    def isGuanYinSuperSkillBook(self):
        return hasattr(self, 'cstype') and self.cstype == self.SUBTYPE_2_GUANYIN_SUPER_SKILL_BOOK

    def consistentGuanYinData(self):
        if not hasattr(self, 'guanYinExtraInfo'):
            self.guanYinExtraInfo = []
            for pg in xrange(self.guanYinSlotNum):
                self.guanYinExtraInfo.append([{}, {}, {}])

    def __initGuanYin(self):
        gd = GD.data.get(self.id)
        self.guanYinSlotNum = gd.get('pskillNum', 0)
        self.guanYinInfo = []
        for pg in xrange(self.guanYinSlotNum):
            self.guanYinInfo.append([None, None, None])

        self.guanYinExtraInfo = []
        for pg in xrange(self.guanYinSlotNum):
            self.guanYinExtraInfo.append([{}, {}, {}])

        self.guanYinStat = [None] * self.guanYinSlotNum
        self.guanYinSuperBookId = 0
        self.guanYinSuperPskillExpire = 0

    def validGuanYinPos(self, slot, part):
        if not self.isGuanYin():
            return False
        if not hasattr(self, 'guanYinSlotNum'):
            return False
        if slot < 0 or slot >= self.guanYinSlotNum:
            return False
        if part < 0 or part >= const.MAX_GUANYIN_PER_SLOT_PSKILL_NUM:
            return False
        return True

    def checkGuanYinPskillTimeOut(self, slot, part):
        if not self.isGuanYin():
            return False
        if not self.validGuanYinPos(slot, part):
            return False
        now = utils.getNow()
        extra = self.guanYinExtraInfo[slot][part]
        if extra.has_key('expireTime') and now > extra['expireTime']:
            return True
        if extra.has_key('commonExpireTime') and now > extra['commonExpireTime']:
            return True
        return False

    def getActiveGuanYinPskill(self):
        if not self.isGuanYin():
            return []
        res = []
        now = utils.getNow()
        for slot, info in enumerate(self.guanYinInfo):
            if self.guanYinStat[slot] == None:
                continue
            part = self.guanYinStat[slot]
            if info[part] == None:
                continue
            extra = self.guanYinExtraInfo[slot][part]
            if extra.has_key('expireTime') and now > extra['expireTime']:
                continue
            if extra.has_key('commonExpireTime') and now > extra['commonExpireTime']:
                continue
            bookId = info[part]
            bd = GBD.data.get(bookId)
            if not bd:
                continue
            pskIds = bd.get('pskillId', [])
            for pskId in pskIds:
                res.append((pskId, bd.get('lv', 1), slot))

        if hasattr(self, 'guanYinSuperBookId') and self.guanYinSuperBookId > 0 and now < self.guanYinSuperPskillExpire:
            res.extend(self.getGuanYinSurperPskill())
        return res

    def getGuanYinSurperPskill(self):
        if BigWorld.component in ('base', 'cell') and not gameconfig.enableGuanYinSuperSkill():
            return []
        guanYinSuperBookId = getattr(self, 'guanYinSuperBookId', 0)
        if guanYinSuperBookId <= 0:
            return []
        res = []
        bd = GBD.data.get(self.guanYinSuperBookId)
        if bd:
            pskIds = bd.get('pskillId', [])
            for pskId in pskIds:
                res.append((pskId, bd.get('lv', 1), -1))

        return res

    def calcGuanYinPSkillScore(self, extra):
        if not self.isGuanYin():
            return 0
        if gameconfigCommon.enableGuanYinThirdPhase():
            return extra and extra.get('guanYinScore', 0) or 0
        score = 0
        for info in self.guanYinInfo:
            tmax = 0
            for bookId in info:
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                tmax = max(bd.get('score', 0), tmax)

            score += tmax

        return score

    def calcGuanYinPSkillScoreType(self):
        if not self.isGuanYin():
            return [0,
             0,
             0,
             0]
        scoreType = [0,
         0,
         0,
         0]
        for info in self.guanYinInfo:
            tmax = 0
            tmaxType = [0,
             0,
             0,
             0]
            for bookId in info:
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                if bd.get('score', 0) > tmax:
                    tmax = bd.get('score', 0)
                    tmaxType = bd.get('scoreType', [])

            scoreType = calcCombatScoreType(scoreType, tmaxType, [], tmax, const.COMBAT_SCORE_TYPE_OP_COEFF)

        return scoreType

    def getAllGuanYinPskill(self):
        if not self.isGuanYin():
            return []
        res = []
        for info in self.guanYinInfo:
            for bookId in info:
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                pskIds = bd.get('pskillId', [])
                for pskId in pskIds:
                    res.append(pskId)

        if hasattr(self, 'guanYinSuperBookId') and self.guanYinSuperBookId > 0 and utils.getNow() < self.guanYinSuperPskillExpire:
            bd = GBD.data.get(self.guanYinSuperBookId)
            if bd:
                pskIds = bd.get('pskillId', [])
                for pskId in pskIds:
                    res.append(pskId)

        return res

    def checkGuanYinSuperSkill(self):
        if not self.isGuanYin():
            return False
        if hasattr(self, 'guanYinSuperBookId') and self.guanYinSuperBookId > 0 and utils.getNow() < self.guanYinSuperPskillExpire:
            return True
        return False

    def resetMultiDyeList(self):
        if not self.isEquip():
            return
        if self.isWingOrRide():
            self.dyeList = []
            return
        if not self.isFashionEquip():
            return
        self._initMultiDyeScheme()
        ed = ED.data.get(self.id, {})
        dyeList = ed.get('dyeList', [])
        self.dyeCurrIdx = gametypes.DYE_SCHEME_INIT
        for idx in self.dyeMaterialsScheme.keys():
            self.dyeListScheme[idx] = dyeList
            self.dyeMaterialsScheme[idx] = []

    def resetDyeList(self):
        if not self.isEquip():
            return
        if self.isWingOrRide():
            self.dyeList = []
            return
        if not self.isFashionEquip():
            return
        ed = ED.data.get(self.id, {})
        dyeList = ed.get('dyeList', [])
        if dyeList:
            self.dyeList = dyeList
            self.dyeMaterials = []
        else:
            canDye = ed.get('canDye', 0)
            if not canDye:
                return
            dyeMaterials = ed.get('dyeMaterials', [])
            if canDye == gametypes.DYE_SINGLE:
                dyeMaterials = [utils.genRandomNormalDyeMaterial()]
            elif canDye == gametypes.DYE_DUAL:
                dyeMaterials = [utils.genRandomNormalDyeMaterial(), utils.genRandomNormalDyeMaterial()]
            self.dyeList = utils.calcDyeListFromMaterial(dyeMaterials)
            self.dyeMaterials = []
            for i, itemId in enumerate(dyeMaterials):
                self.dyeMaterials.append((i + 1, itemId, const.DYE_COPY))

    def _initMultiDyeScheme(self):
        if hasattr(self, 'dyeMaterialsScheme'):
            return
        ed = ED.data.get(self.id, {})
        dyeList = ed.get('dyeList', [])
        self.dyeCurrIdx = gametypes.DYE_SCHEME_INIT
        self.dyeListScheme = {gametypes.DYE_SCHEME_INIT: dyeList,
         gametypes.DYE_SCHEME_DEFAULT_ON: dyeList}
        self.dyeMaterialsScheme = {gametypes.DYE_SCHEME_INIT: [],
         gametypes.DYE_SCHEME_DEFAULT_ON: []}

    def tryConvertToMultiDyeScheme(self):
        self._initMultiDyeScheme()
        if self.__dict__.get('dyeList'):
            ed = ED.data.get(self.id, {})
            dyeList = ed.get('dyeList', [])
            if self.__dict__.get('dyeMaterials'):
                self.dyeListScheme[gametypes.DYE_SCHEME_INIT] = dyeList
                self.dyeMaterialsScheme[gametypes.DYE_SCHEME_INIT] = []
                self.dyeListScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = self.__dict__['dyeList']
                self.dyeMaterialsScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = self.__dict__['dyeMaterials']
                self.dyeCurrIdx = gametypes.DYE_SCHEME_DEFAULT_ON
            else:
                self.dyeListScheme[gametypes.DYE_SCHEME_INIT] = dyeList
                self.dyeMaterialsScheme[gametypes.DYE_SCHEME_INIT] = []
                self.dyeListScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = dyeList
                self.dyeMaterialsScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = []
                self.dyeCurrIdx = gametypes.DYE_SCHEME_INIT
            self.__dict__.pop('dyeList', None)
            self.__dict__.pop('dyeMaterials', None)
        elif len(self.dyeMaterialsScheme[gametypes.DYE_SCHEME_INIT]):
            gamelog.info('cgy#tryConvertToMultiDyeScheme fix scheme:', self.dyeMaterialsScheme, self.dyeListScheme)
            ed = ED.data.get(self.id, {})
            dyeList = ed.get('dyeList', [])
            self.dyeListScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = self.dyeListScheme[gametypes.DYE_SCHEME_INIT]
            self.dyeMaterialsScheme[gametypes.DYE_SCHEME_DEFAULT_ON] = self.dyeMaterialsScheme[gametypes.DYE_SCHEME_INIT]
            self.dyeCurrIdx = gametypes.DYE_SCHEME_DEFAULT_ON
            self.dyeListScheme[gametypes.DYE_SCHEME_INIT] = dyeList
            self.dyeMaterialsScheme[gametypes.DYE_SCHEME_INIT] = []
        if BigWorld.component in ('base', 'cell') and not gameconfig.enableWardrobe():
            if len(self.dyeMaterialsScheme.get(gametypes.DYE_SCHEME_DEFAULT_ON)):
                self.dyeCurrIdx = gametypes.DYE_SCHEME_DEFAULT_ON

    def switchDyeScheme(self, targetIdx):
        self._initMultiDyeScheme()
        if targetIdx not in self.dyeListScheme:
            return False
        self.dyeCurrIdx = targetIdx
        return True

    def openNewDyeScheme(self):
        self._initMultiDyeScheme()
        gamelog.info('cgy#openNewDyeScheme:', self.id)
        ed = ED.data.get(self.id, {})
        dyeList = ed.get('dyeList', [])
        allSchemes = list(gametypes.DYE_MULTI_SCHEMES)
        allSchemes.sort()
        for idx in allSchemes:
            if idx not in self.dyeListScheme:
                self.dyeListScheme[idx] = dyeList
                self.dyeMaterialsScheme[idx] = []
                return idx

        return False

    def openDyeSchemeViaNum(self, openNum):
        gamelog.info('cgy#openDyeSchemeViaNum:', self.id, openNum)
        if openNum > len(gametypes.DYE_MULTI_SCHEMES) or openNum <= 0:
            return
        ed = ED.data.get(self.id, {})
        dyeList = ed.get('dyeList', [])
        allSchemes = list(gametypes.DYE_MULTI_SCHEMES)
        allSchemes.sort()
        curOpenNum = 0
        for idx in allSchemes:
            if curOpenNum >= openNum:
                return
            curOpenNum += 1
            if idx not in self.dyeListScheme:
                self.dyeListScheme[idx] = dyeList
                self.dyeMaterialsScheme[idx] = []

    def getNextDyeSchemeIdx(self):
        allSchemes = list(gametypes.DYE_MULTI_SCHEMES)
        allSchemes.sort()
        for idx in allSchemes:
            if idx not in self.dyeListScheme:
                return idx

        return 0

    def prettyPrintDyeScheme(self):
        prettyDyeList = json.dumps(self.dyeListScheme, sort_keys=True, indent=4)
        prettyDyeMaterials = json.dumps(self.dyeMaterialsScheme, sort_keys=True, indent=4)
        gamelog.info('cgy@item#prettyPrintDyeScheme:', self.dyeCurrIdx)
        gamelog.info('cgy@item#prettyPrintDyeScheme:', prettyDyeList)
        gamelog.info('cgy@item#prettyPrintDyeScheme:', prettyDyeMaterials)

    def resetHuanfu(self):
        if not self.isEquip():
            return
        if self.isWingOrRide():
            self.realDyeId = self.id
            self.currentSkin = None
            return

    @staticmethod
    def checkDyeMaterialsValid(equipId, owner, dyeList, dyeMaterials, needModify = False):
        if BigWorld.component in ('base', 'cell') and not gameconfig.enableCheckFashionDyeMaterials():
            return True
        if not dyeMaterials:
            return True
        allChannel = [const.DYE_CHANNEL_1, const.DYE_CHANNEL_2]
        ret = 0
        checkNum = 0
        for channel, itemId, _ in dyeMaterials:
            if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2):
                if channel in allChannel:
                    allChannel.remove(channel)
                isValid = 0
                checkNum += 1
                dyeArray = []
                mad = MAD.data.get(itemId, {})
                if not mad:
                    isValid = 1
                    ret += isValid
                    continue
                index = const.DYES_INDEX_COLOR if channel == const.DYE_CHANNEL_1 else const.DYES_INDEX_DUAL_COLOR
                if index < len(dyeList):
                    dye = dyeList[index]
                    dyeType = mad.get('dyeType', 0)
                    if dyeType == Item.CONSUME_DYE_NORMAL:
                        color = mad.get('pbrColor', [])
                        alpha = mad.get('pbrAlpha', [0])[-1]
                        if color:
                            if type(color[0]) is str:
                                dyeArray.append(color)
                            else:
                                dyeArray.extend(color)
                    for value in dyeArray:
                        if _checkValidDye(dye, alpha, value[0]):
                            isValid = 1
                            break

                    if not isValid and needModify:
                        if type(dyeList) is list:
                            dyeList[index] = dyeArray[-1][0]
                            if index + 1 < len(dyeList):
                                dyeList[index + 1] = dyeArray[-1][1]
                            lightIndex = const.DYES_INDEX_PBR_HIGH_LIGHT if channel == const.DYE_CHANNEL_1 else const.DYES_INDEX_PBR_DUAL_HIGH_LIGHT
                            if lightIndex < len(dyeList):
                                dyeList[lightIndex] = str(mad.get('pbrHighLightAlpha', [15])[0])
                else:
                    isValid = 1
                ret += isValid

        if allChannel:
            ed = ED.data.get(equipId)
            canDye = ed.get('canDye', 0)
            originalDyeList = ed.get('dyeList', [])
            if originalDyeList:
                for channel in allChannel:
                    index = const.DYES_INDEX_COLOR if channel == const.DYE_CHANNEL_1 else const.DYES_INDEX_DUAL_COLOR
                    if index == const.DYES_INDEX_DUAL_COLOR and canDye == gametypes.DYE_SINGLE:
                        continue
                    dye = []
                    originalDye = []
                    if index + 1 < len(dyeList):
                        dye = dyeList[index:index + 2]
                    if index + 1 < len(originalDyeList):
                        originalDye = originalDyeList[index:index + 2]
                    if list(originalDye) != list(dye):
                        ret += 1
                        if needModify:
                            if dye:
                                if originalDye:
                                    dyeList[index:index + 2] = originalDye
                                else:
                                    dyeList[index:index + 2] = const.DEFAULT_DYES[index:index + 2]
                            lightIndex = const.DYES_INDEX_PBR_HIGH_LIGHT if channel == const.DYE_CHANNEL_1 else const.DYES_INDEX_PBR_DUAL_HIGH_LIGHT
                            if lightIndex < len(dyeList) and lightIndex < len(originalDyeList):
                                dyeList[lightIndex] = originalDyeList[lightIndex]

        return ret == checkNum

    def checkDyeMaterialsValidSelf(self, owner):
        if hasattr(self, 'dyeMaterials') and hasattr(self, 'dyeList') and self.isFashionEquip():
            self.checkDyeMaterialsValid(self.id, owner, self.dyeList, self.dyeMaterials, True)

    def isDeed(self):
        return self.type == Item.BASETYPE_DEED

    def isManualEquip(self):
        return getattr(self, 'manaulEquip', False) or MEPD.data.has_key(self.id)

    def isExtendedEquip(self):
        return XEPD.data.has_key(self.id)

    def _getDataByMaketype(self, dataList):
        if self.makeType < len(dataList):
            return dataList[self.makeType]
        return dataList[-1]

    def unidentify(self):
        attrList = [('props', []), ('rprops', []), ('extraProps', [])]
        self.updateAttribute(dict(attrList), newAttr=False)
        self.delProp(['yangSlots', 'yinSlots'])
        self.removePrefixProps()
        self.loseEquipSpecialEffect(self.EQUIP_SE_BASE, 0)
        if hasattr(self, 'propFix') and self.propFix.pop(self.EQUIP_PROP_FIX_BASE, None):
            self.refreshPropsFix()

    def unidentifiedEquipItemInit(self, owner, makeType):
        self.makeType = makeType
        self.makerRole = owner.roleName
        self.makerGbId = owner.gbId
        return self

    def isUnidentifiedEquip(self):
        if self.type == Item.BASETYPE_UNIDENTIFIED_EQUIP:
            return True
        return False

    def manualEquipInit(self, unidentifiedItem):
        self.unidentify()
        self.manaulEquip = True
        self.makeType = unidentifiedItem.makeType
        self.makerRole = unidentifiedItem.makerRole
        self.makerGbId = unidentifiedItem.makerGbId
        self._randomQuality()
        self.score = 0
        return self

    def _calcRandEquip(self, isManual, epData):
        """
        \xca\xd6\xb9\xa4\xd7\xb0\xb1\xb8\xca\xfd\xbe\xdd\xc5\xe4\xd6\xc3\xb1\xed\xd4\xda MEPD
        \xc0\xa9\xd5\xb9\xcb\xe6\xbb\xfa\xd7\xb0\xb1\xb8\xc5\xe4\xd6\xc3\xb1\xed\xd4\xda XEPD
        \xd5\xe2\xc1\xbd\xb8\xf6\xb1\xed\xc2\xd4\xce\xa2\xc7\xf8\xb1\xf0\xd4\xda\xd3\xda\xa3\xba\xb6\xd4\xd3\xda\xd2\xbb\xd0\xa9\xcb\xe6\xbb\xfa\xca\xf4\xd0\xd4\xa3\xac\xca\xd6\xb9\xa4\xd7\xb0\xd2\xaa\xb8\xf9\xbe\xdd\xb4\xf2\xd4\xec\xc0\xe0\xd0\xcd(makeType)\xc0\xb4\xd1\xa1\xd4\xf1\xa3\xac\xb6\xf8\xba\xf3\xd5\xdf\xb2\xbb\xd3\xc3\xa3\xbb\xca\xd6\xb9\xa4\xd7\xb0\xd3\xc9\xb4\xf2\xd4\xec\xd5\xdf\xd0\xc5\xcf\xa2\xa3\xac\xb6\xf8\xba\xf3\xd5\xdf\xb2\xbb\xd3\xc3\xa1\xa3
        isManual \xce\xaa True \xca\xb1\xb1\xed\xca\xbe\xca\xd6\xb9\xa4\xd7\xb0\xbc\xf8\xb6\xa8\xa3\xac\xce\xaa False \xca\xb1\xb1\xed\xca\xbe\xca\xf4\xd0\xd4\xc0\xa9\xd5\xb9\xd7\xb0\xb1\xb8\xb5\xc4\xcb\xe6\xbb\xfa\xca\xf4\xd0\xd4\xc9\xfa\xb3\xc9
        """
        self.delProp(('yinSlots', 'yangSlots'))
        self.__initEquipGemSlots(ED.data[self.id])
        self._randomInitStarLv()
        self.props = []
        if epData.has_key('basicProps'):
            if isManual:
                basicProps = self._getDataByMaketype(epData['basicProps'])
            else:
                basicProps = epData['basicProps']
            for pid, pType, valMin, valMax, weights in basicProps:
                if not weights:
                    continue
                idx = commcalc.weightingChoiceIndex(weights)
                interval = (valMax - valMin) / len(weights)
                pVal = valMin + interval * (idx + random.random())
                self.props.append((pid, pType, pVal))

        self.extraProps = []
        self.rprops = []
        self.loseEquipSpecialEffect(self.EQUIP_SE_BASE, 0)
        if hasattr(self, 'propFix') and self.propFix.pop(self.EQUIP_PROP_FIX_BASE, None):
            self.refreshPropsFix()
        if epData.has_key('extraPools'):
            if isManual:
                randPropId = self._getDataByMaketype(epData['extraPools'])
            else:
                randPropId = epData['extraPools']
            self.randomProperties(randPropId)
        self.removePrefixProps()
        if epData.has_key('initPrefix'):
            initPrefixConf = epData['initPrefix']
            if isinstance(initPrefixConf, tuple):
                preGroupId, prefixId = epData['initPrefix']
                self.addPrefixProps(preGroupId, prefixId)
            elif isinstance(initPrefixConf, list):
                preGroupId = commcalc.weightingChoice([ groupId for groupId, _ in initPrefixConf ], [ prob for _, prob in initPrefixConf ])
                preGroupId, prefixId = self.genPrefixByGroupId(preGroupId)
                self.addPrefixProps(preGroupId, prefixId)
        self.loseEquipSpecialEffect(self.EQUIP_SE_MANUAL, 0)
        if epData.has_key('specialPools'):
            if isManual:
                specialEffPools = self._getDataByMaketype(epData['specialPools'])
            else:
                specialEffPools = epData['specialPools']
            for poolId, prob in specialEffPools:
                if random.randint(*const.RANDOM_RATE_BASE_10K) < prob:
                    seList = MESPD.data.get(poolId, [])
                    propData = commcalc.weightingChoice(seList, [ se['prob'] for se in seList ])
                    if propData.has_key('specialEffect'):
                        self.gainEquipSpecialEffect(self.EQUIP_SE_MANUAL, propData['specialEffect'])

        self.decStarExp(None, self.calcTotalStarExp())
        if epData.has_key('starPools'):
            if isManual:
                starRandId = self._getDataByMaketype(epData['starPools'])
            else:
                starRandId = epData['starPools']
            starEffPool = MESTARPD.data.get(starRandId, [])
            if starEffPool:
                starEffData = commcalc.weightingChoice(starEffPool, [ p['prob'] for p in starEffPool ])
                self.manualEquipStarInfo = (starRandId, starEffData['id'])

    def identify(self, owner = None):
        if not MEPD.data.has_key(self.id):
            return
        if not ED.data.has_key(self.id):
            return
        mepd = MEPD.data[self.id]
        self._calcRandEquip(True, mepd)
        self.calcScores(calcRarityMiracle=True, extra={'owner': owner})
        self.popProp('dumpAfterIdentify', None)
        self.dumpAfterIdentify = zlib.compress(dumps(utils.getItemSaveData(self)))

    def unbindRandomEquip(self, owner):
        it = self.getItemAfterIdentify()
        if not it:
            return None
        rarityMiracle = getattr(self, 'rarityMiracle', Item.EQUIP_NOT_DECIDED)
        refineManual = getattr(self, 'refineManual', {})
        it.unbindTimes = getattr(it, 'unbindTimes', 0) + 1
        self.__dict__ = it.__dict__
        self.dumpAfterIdentify = zlib.compress(dumps(utils.getItemSaveData(self)))
        if rarityMiracle != Item.EQUIP_NOT_DECIDED:
            self.rarityMiracle = rarityMiracle
        if gameconfigCommon.enableRefineManualEquipment() and refineManual:
            self.unbindRefineManual(refineManual, owner)
        return self

    def getItemAfterIdentify(self):
        if not (self.isManualEquip() or self.isExtendedEquip()):
            return None
        dumpAfterIdentify = self.dumpAfterIdentify
        itemProps = loads(zlib.decompress(dumpAfterIdentify))
        it = utils.createItemObjFromDict(itemProps)
        it.consistent()
        return it

    def isUnidentifiedManualEquip(self):
        return MERRD.data.has_key(self.id)

    def cmpGemEquipType(self, tgtId):
        srcGtp = ED.data.get(self.id, {}).get('gemEquipType')
        if not srcGtp:
            return False
        tgtGtp = ED.data.get(tgtId, {}).get('gemEquipType')
        if not srcGtp:
            return False
        if tgtGtp != srcGtp:
            return False
        return True

    def getStorageContainer(self):
        return getattr(self, 'storageRes', -1)

    def isStorageByWardrobe(self):
        if BigWorld.component == 'client':
            if not gameglobal.rds.configData.get('enableWardrobe', False):
                return False
        elif not gameconfig.enableWardrobe():
            return False
        return getattr(self, 'storageRes', -1) == const.RES_KIND_WARDROBE_BAG

    def setStorageContainer(self, resKind):
        if resKind == -1 and hasattr(self, 'storageRes'):
            delattr(self, 'storageRes')
            return
        self.storageRes = resKind

    def checkSchool(self, school):
        schoolReq = ID.data.get(self.id, {}).get('schReq')
        if not schoolReq:
            return True
        return school in schoolReq


def _checkValidDye(dye, alpha, validDye):
    if alpha:
        index1 = dye.rfind(',')
        index2 = validDye.rfind(',')
        if index1 != index2:
            return False
        if dye[0:index1] != validDye[0:index2]:
            return False
        if int(dye[index1 + 1:]) > alpha:
            return False
    elif dye != validDye:
        return False
    return True


class runeDataVal(UserSoleType):

    def __init__(self, runeSlotsType, part, item):
        self.runeSlotsType = runeSlotsType
        self.part = part
        self.item = item

    def _lateReload(self):
        if self.item:
            self.item.reloadScript()


class GemSlot(UserSoleType):

    def __init__(self, state = Item.GEM_SLOT_EMPTY, gem = const.CONT_EMPTY_VAL, gemProps = [], pos = 0):
        self.state = state
        self.gem = gem
        self.pos = pos
        self.gemProps = copy.copy(gemProps)

    def fillGem(self, gemItem):
        self.gem = gemItem
        self.state = Item.GEM_SLOT_FILLED
        gemData = utils.getEquipGemData(gemItem.id)
        for aid, atype, aval in gemData.get('gemProps', ()):
            self.gemProps.append((aid, atype, aval))

    def removeGem(self):
        gemItem = self.gem
        self.gem = const.CONT_EMPTY_VAL
        self.state = Item.GEM_SLOT_EMPTY
        self.gemProps = []
        return gemItem

    def isLocked(self):
        return self.state == Item.GEM_SLOT_LOCKED

    def isEmpty(self):
        return self.state == Item.GEM_SLOT_EMPTY

    def isFilled(self):
        return self.state == Item.GEM_SLOT_FILLED

    def unlock(self):
        self.state = Item.GEM_SLOT_EMPTY

    @property
    def score(self):
        if not self.gem:
            return 0
        gemData = utils.getEquipGemData(self.gem.id)
        if not gemData:
            return 0
        gemLv = gemData.get('lv', 0)
        gemType = gemData.get('type', 0)
        gemSubType = gemData.get('subType', 0)
        return EGSD.data.get((gemLv, gemType, gemSubType), {}).get('gPoint', 0)

    @property
    def scoreType(self):
        if not self.gem:
            return [0,
             0,
             0,
             0]
        gemData = utils.getEquipGemData(self.gem.id)
        if not gemData:
            return [0,
             0,
             0,
             0]
        gemLv = gemData.get('lv', 0)
        gemType = gemData.get('type', 0)
        gemSubType = gemData.get('subType', 0)
        gPoint = EGSD.data.get((gemLv, gemType, gemSubType), {}).get('gPoint', 0)
        gPointType = EGSD.data.get((gemLv, gemType, gemSubType), {}).get('gPointType', [])
        return calcCombatScoreType([], gPointType, [], gPoint, const.COMBAT_SCORE_TYPE_OP_COEFF)

    def getGemData(self, slotType):
        slotDict = {'gem': utils.getItemSaveData(self.gem),
         'state': self.state,
         'gemProps': self.gemProps,
         'slotType': slotType,
         'pos': self.pos}
        return slotDict

    @staticmethod
    def slotWithSavedData(data):
        slot = GemSlot()
        gemData = data['gem'] if data.has_key('gem') else {}
        slot.gem = utils.doCreateItemObjFromDict(gemData) if gemData else const.CONT_EMPTY_VAL
        slot.state = data['state']
        slot.pos = data['pos']
        slot.gemProps = []
        if slot.gem:
            try:
                gemProps = utils.getEquipGemData(slot.gem.id).get('gemProps', ())
                for aid, atype, aval in gemProps:
                    slot.gemProps.append((aid, atype, aval))

            except Exception as e:
                gamelog.error('fail to create slot', getattr(slot.gem, 'id', -1), getattr(e, 'message', ''))

        return slot

    def _lateReload(self):
        if self.gem:
            self.gem.reloadScript()
