#Embedded file name: /WORKSPACE/data/entities/client/helpers/action.o
import random
import gametypes
from data import avatar_action_data as AAD
UNKNOWN_ACTION = 0
ATTACK_ACTION = 1
BEHIT_ACTION = 2
SITDOWN_ACTION = 3
STANDUP_ACTION = 4
SPELL_ACTION = 5
CAST_ACTION = 6
DEAD_ACTION = 7
IDLE_ACTION = 8
CASTSTOP_ACTION = 9
USE_ACTION = 10
JUMP_ACTION = 11
FALL_ACTION = 12
ATTACK_PREPARE = 13
FAINT_ACTION = 16
THROW_ACTION = 17
PROGRESS_ACTION = 18
RIDE_JUMP_ACTION = 19
BORED_ACTION = 20
SHOW_WEAPON_ACTION = 21
HANG_WEAPON_ACTION = 22
MOVING_ACTION = 26
MOVINGSTOP_ACTION = 27
AFTERMOVE_ACTION = 28
AFTERMOVESTOP_ACTION = 29
ROLL_ACTION = 30
ROLLSTOP_ACTION = 31
STARTSPELL_ACTION = 32
GUARD_ACTION = 33
ALERT_ACTION = 34
FALLEND_ACTION = 35
DYING_ACTION = 36
GUIDE_ACTION = 37
GUIDESTOP_ACTION = 38
HITFLY_ACTION = 39
HITFLY_STOP_ACTION = 40
EMOTE_ACTION = 41
DASH_START_ACTION = 42
PICK_ITEM_ACTION = 43
CHARGE_START_ACTION = 44
CHARGE_ACTION = 45
HITBACK_ACTION = 46
FAST_DOWN_ACTION = 47
STARTPRESPELL_ACTION = 48
PRESPELLING_ACTION = 49
CHAT_ACTION = 50
INCOMBAT_START_ACTION = 51
FUKONG_START_ACTION = 52
FUKONG_LOOP_ACTION = 53
FUKONG_STOP_ACTION = 54
TIAOGAO_START_ACTION = 55
TIAOGAO_LOOP_ACTION = 56
TIAOGAO_STOP_ACTION = 57
JIDAO_START_ACTION = 58
JIDAO_LOOP_ACTION = 59
JIDAO_STOP_ACTION = 60
FAINT_START_ACTION = 61
FAINT_LOOP_ACTION = 62
FAINT_STOP_ACTION = 63
HORSE_DASH_STOP_ACTION = 64
NPC_COLLIDE_ACTION = 65
FISHING_ACTION = 66
CAST_MOVING_ACTION = 67
FISHING_READY_ACTION = 69
FISHING_HOLD_ACTION = 70
HIT_DIEFLY_ACTION = 71
PICK_END_ACTION = 72
BORN_IDLE_ACTION = 73
LEAVE_BORN_ACTION = 74
LEAVE_HORSE_ACTION = 75
LEAVE_HORSE_END_ACTION = 76
DA_ZUO_ACTION = 77
WING_TAKE_OFF_ACTION = 78
WING_LAND_ACTION = 79
MAN_DOWN_START_ACTION = 80
MAN_DOWN_STOP_ACTION = 81
DASH_STOP_ACTION = 83
SOCIAL_ACTION = 84
HORSE_WHISTLE_ACTION = 85
WING_LAND_END_ACTION = 86
WING_FLY_DOWN_ACTION = 87
WING_FLY_UP_ACTION = 88
COUPLE_EMOTE_START_ACTION = 89
COUPLE_EMOTE_BE_START_ACTION = 90
RUN_TO_IDEL_ACTION = 91
START_TO_RUN_ACTION = 92
ZAIJU_ON_ACTION = 93
PROGRESS_SPELL_ACTION = 94
SHOW_WEAR_ACTION = 95
OPEN_WEAR_ACTION = 96
RUSH_DOWN_ACTION = 97
NORMAL_READY_ACTION = 98
CLOSE_WEAR_ACTION = 99
APPRENTICE_TRAIN_ACTION = 100
APPRENTICE_TRAIN_END_ACTION = 101
LIFE_ACTION = 102
SHUANGXIU_ACTION = 103
SHUANGXIU_END_ACTION = 104
TELEPORT_SPELL_ACTION = 105
PHOTO_ACTION = 107
PET_ACTION = 108
INTERACTIVE_ENTER_ACTION = 109
WA_BAO_ACTION = 110
COUPLE_EMOTE_NORMAL_ACTION = 111
COUPLE_EMOTE_SHAXING_DESTROY_ACTION = 112
WING_LAND_TO_FLY_ACTION = 113
INTERACTIVE_ACTION = 114
TURN_ACTION = 115
SUMMON_SPRITE_TRANSFORM_ACTION = 116
SUMMON_SPRITE_LINGER = 117
HOLDING_SKILL_ACTION = [SPELL_ACTION,
 GUIDE_ACTION,
 CAST_ACTION,
 CHARGE_ACTION,
 STARTSPELL_ACTION,
 CHARGE_START_ACTION,
 STARTPRESPELL_ACTION,
 PRESPELLING_ACTION]
S_SLIDE = 0
S_BLEND = 1
S_BREAK = 2
S_DEFAULT = 0
S_SPELLING = 1
S_PRESPELLING = 2
S_SPELLCHARGE = 3
S_SPELLING_CAN_MOVE = 4
UNKNOWN_STATE = 0
FAINT_STATE = 1
JIDAO_STATE = 2
TIAOGAO_STATE = 2
FUKONG_STATE = 3
FREEZETIME_STATE = 4
EXCLUDE_ACTION_SET = frozenset(['prefixStateActions'])

class AdaptiveAction(object):

    def __init__(self, actionList, caps):
        super(AdaptiveAction, self).__init__()
        data = AAD.data.get(caps, {})
        if not data:
            data = AAD.data.get((1, 10), {})
        self._actions = {}
        for key, value in data.iteritems():
            self._actions[key] = []
            for act in value:
                if actionList and self.isActInList(act, actionList) or key in EXCLUDE_ACTION_SET:
                    self._actions[key].append(act)

    def isActInList(self, act, actionList):
        for realAct in actionList:
            actName = realAct.split('_')[-1]
            if actName == act:
                return True

        return False

    def getAction(self, actionName):
        try:
            act = self._actions[actionName]
        except:
            return

        if act == None or len(act) == 0:
            return
        return random.choice(act)


_ACTION_GROUP_NAMES = ['bodyTurnActions',
 'rideTurnActions',
 'attackActions',
 'showWeaponActions',
 'hangWeaponActions',
 'beHitActions',
 'forceBeHitActions',
 'dieActions',
 'deadActions',
 'jumpRunStartActions',
 'jumpRunActions',
 'jumpRunUpActions',
 'fallRunFlyActions',
 'fallRunDownActions',
 'fallRunEndIdleActions',
 'fallRunBackEndActions',
 'fallRunEndRunActions',
 'jumpDashStartActions',
 'jumpDashActions',
 'jumpDashUpActions',
 'fallDashFlyActions',
 'fallDashDownActions',
 'fallDashEndIdleActions',
 'fallDashEndDashActions',
 'jumpRunTwiceStart1Actions',
 'jumpRunTwice1Actions',
 'jumpRunTwiceUp1Actions',
 'fallRunTwiceFly1Actions',
 'fallRunTwiceDown1Actions',
 'fallRunTwiceEndIdle1Actions',
 'fallRunTwiceEndRun1Actions',
 'jumpRunTwiceStart2Actions',
 'jumpRunTwice2Actions',
 'jumpRunTwiceUp2Actions',
 'fallRunTwiceFly2Actions',
 'fallRunTwiceDown2Actions',
 'fallRunTwiceEndIdle2Actions',
 'fallRunTwiceEndRun2Actions',
 'jumpRunTwiceStart3Actions',
 'jumpRunTwice3Actions',
 'jumpRunTwiceUp3Actions',
 'fallRunTwiceFly3Actions',
 'fallRunTwiceDown3Actions',
 'fallRunTwiceEndIdle3Actions',
 'fallRunTwiceEndRun3Actions',
 'jumpDashTwiceStart1Actions',
 'jumpDashTwice1Actions',
 'jumpDashTwiceUp1Actions',
 'fallDashTwiceFly1Actions',
 'fallDashTwiceDown1Actions',
 'fallDashTwiceEndIdle1Actions',
 'fallDashTwiceEndDash1Actions',
 'jumpDashTwiceStart2Actions',
 'jumpDash2Actions',
 'jumpDashUp2Actions',
 'fallDashFly2Actions',
 'fallDashDown2Actions',
 'fallDashTwiceEndIdle2Actions',
 'fallDashTwiceEndDash2Actions',
 'summonActions',
 'sliderDashStartActions',
 'sliderDashActions',
 'fastFallDownActions',
 'slowFallDownActions',
 'rushStartActions',
 'rushActions',
 'rushStartWeaponInHandActions',
 'rushWeaponInHandActions',
 'hitBackActions',
 'boredActions',
 'horseJumpRunStartActions',
 'horseJumpRunStartActions',
 'horseJumpRunActions',
 'horseJumpRunUpActions',
 'horseFallRunFlyActions',
 'horseFallRunDownActions',
 'horseFallRunEndIdleActions',
 'horseFallRunBackEndActions',
 'horseFallRunEndRunActions',
 'horseJumpDashStartActions',
 'horseJumpDashActions',
 'horseJumpDashUpActions',
 'horseFallDashFlyActions',
 'horseFallDashDownActions',
 'horseFallDashEndIdleActions',
 'horseRoarJumpActions',
 'horseSprintStopActions',
 'horseBoredActions',
 'wingFlyRushStartActions',
 'wingNoFlyRushStartActionswingFlyRushActions',
 'wingFlyRushEndActions',
 'wingFlyUpStartActions',
 'wingNoFlyUpStartActionswingFlyDownStartActions',
 'wingFlyDownActions',
 'wingFlyUpActions',
 'wingFlyUpEndActions',
 'wingFlyDownEndActions',
 'fishingStartActions',
 'fishingLoopActions',
 'fishingEndActions',
 'fishingBoredActions',
 'fishingEndLoopActions',
 'faintActionswingFlyStopActionswingFlyNormalUpActions',
 'wingFlyNormalDownActions',
 'wingFlyFastDownActions',
 'wingFlyFastDownEndActions',
 'wingFlyBackStartActions',
 'wingFlyBackActions',
 'wingFlyLeftStartActions',
 'wingFlyLeftActions',
 'wingFlyRightStartActions',
 'wingFlyRightActions',
 'startToRunLeftActions',
 'startToRunRightActions',
 'runToIdleActions',
 'fallLeftRunEndRunActions',
 'fallRightRunEndRunActions']
_ACTION_DICT = dict()
_ACTION_DICT['bodyTurnActions'] = ('11021', '11031')
_ACTION_DICT['rideTurnActions'] = ('14021', '14031')
_ACTION_DICT['boredActions'] = (('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'),
 ('1102', '1103'))
_ACTION_DICT['horseBoredActions'] = (('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'),
 ('11102', '11103'))
_ACTION_DICT['attackActions'] = (('1502', '1502', '1502'),
 ('2502', '2502', '2502'),
 ('3502', '3502', '3502'),
 ('4502', '4502', '4502'),
 ('5502', '5502', '5502'),
 ('6502', '6502', '6502'),
 ('7502', '7502', '7502'),
 ('8502', '8502', '8502'),
 ('9502', '9502', '9502'))
_ACTION_DICT['hitBackActions'] = (('1101',),
 ('2501',),
 ('3501',),
 ('4501',),
 ('5501',),
 ('6501',),
 ('7501',),
 ('8501',),
 ('9501',))
_ACTION_DICT['faintHitActions'] = (('1815',),
 ('2815',),
 ('3815',),
 ('4815',),
 ('5815',),
 ('6815',),
 ('7815',),
 ('8815',),
 ('9815',))
_ACTION_DICT['faintActions'] = (('1808',),
 ('2808',),
 ('3808',),
 ('4808',),
 ('5808',),
 ('6808',),
 ('7808',),
 ('8808',),
 ('9808',))
_ACTION_DICT['showWeaponActions'] = (('1704',),
 ('2704',),
 ('3704',),
 ('4704',),
 ('5704',),
 ('6704',),
 ('7704',),
 ('8704',),
 ('9704',))
_ACTION_DICT['hangWeaponActions'] = (('1705',),
 ('2705',),
 ('3705',),
 ('4705',),
 ('5705',),
 ('6705',),
 ('7705',),
 ('8705',),
 ('9705',))
_ACTION_DICT['beHitActions'] = (('1509',),
 ('2509',),
 ('3509',),
 ('4509',),
 ('5509',),
 ('6509',),
 ('7509',),
 ('8509',),
 ('9509',))
_ACTION_DICT['forceBeHitActions'] = (('1831', '1832'),
 ('2831', '2832'),
 ('3831', '3832'),
 ('4831', '4832'),
 ('5831', '5832'),
 ('6831', '6832'),
 ('7831', '7832'),
 ('8831', '8832'),
 ('9831', '9832'))
_ACTION_DICT['frontHitActions'] = (('1801',),
 ('2801',),
 ('3801',),
 ('4801',),
 ('5801',),
 ('6801',),
 ('7801',),
 ('8801',),
 ('9801',))
_ACTION_DICT['frontCriticalHitActions'] = (('1803',),
 ('2803',),
 ('3803',),
 ('4803',),
 ('5803',),
 ('6803',),
 ('7803',),
 ('8803',),
 ('9803',))
_ACTION_DICT['backHitActions'] = (('1804',),
 ('2804',),
 ('3804',),
 ('4804',),
 ('5804',),
 ('6804',),
 ('7804',),
 ('8804',),
 ('9804',))
_ACTION_DICT['backCriticalHitActions'] = (('1805',),
 ('2805',),
 ('3805',),
 ('4805',),
 ('5805',),
 ('6805',),
 ('7805',),
 ('8805',),
 ('9805',))
_ACTION_DICT['lieHitActions'] = (('1816',),
 ('2816',),
 ('3816',),
 ('4816',),
 ('5816',),
 ('6816',),
 ('7816',),
 ('8816',),
 ('9816',))
_ACTION_DICT['lieHit1Actions'] = (('1817',),
 ('2817',),
 ('3817',),
 ('4817',),
 ('5817',),
 ('6817',),
 ('7817',),
 ('8817',),
 ('9817',))
_ACTION_DICT['lieCriticalHitActions'] = (('1806',),
 ('2806',),
 ('3806',),
 ('4806',),
 ('5806',),
 ('6806',),
 ('7806',),
 ('8806',),
 ('9806',))
_ACTION_DICT['dieActions'] = (('1520',),
 ('1520',),
 ('1520',),
 ('1520',),
 ('1520',),
 ('1520',),
 ('1520',),
 ('1520',),
 ('1520',))
_ACTION_DICT['deadActions'] = (('1521',),
 ('1521',),
 ('1521',),
 ('1521',),
 ('1521',),
 ('1521',),
 ('1521',),
 ('1521',),
 ('1521',))
_ACTION_DICT['die1Actions'] = (('1524',),
 ('1524',),
 ('1524',),
 ('1524',),
 ('1524',),
 ('1524',),
 ('1524',),
 ('1524',),
 ('1524',))
_ACTION_DICT['dead1Actions'] = (('1525',),
 ('1525',),
 ('1525',),
 ('1525',),
 ('1525',),
 ('1525',),
 ('1525',),
 ('1525',),
 ('1525',))
_ACTION_DICT['summonActions'] = (('1522',),
 ('2522',),
 ('3522',),
 ('4522',),
 ('5522',),
 ('6522',),
 ('7522',),
 ('8522',),
 ('9522',))
_ACTION_DICT['pickItemActions'] = (('1606',),
 ('2606',),
 ('3606',),
 ('4606',),
 ('5606',),
 ('6606',),
 ('7606',),
 ('8606',),
 ('9606',))
_ACTION_DICT['rollLeftStartActions'] = (('1127',),
 ('2127',),
 ('3127',),
 ('4127',),
 ('5127',),
 ('6127',),
 ('7127',),
 ('8127',),
 ('9127',))
_ACTION_DICT['rollRightStartActions'] = (('1129',),
 ('2129',),
 ('3129',),
 ('4129',),
 ('5129',),
 ('6129',),
 ('7129',),
 ('8129',),
 ('9129',))
_ACTION_DICT['rollBackStartActions'] = (('1131',),
 ('2131',),
 ('3131',),
 ('4131',),
 ('5131',),
 ('6131',),
 ('7131',),
 ('8131',),
 ('9131',))
_ACTION_DICT['rollFollowStartActions'] = (('1133',),
 ('2133',),
 ('3133',),
 ('4133',),
 ('5133',),
 ('6133',),
 ('7133',),
 ('8133',),
 ('9133',))
_ACTION_DICT['rollLeftStopActions'] = (('1128',),
 ('2128',),
 ('3128',),
 ('4128',),
 ('5128',),
 ('6128',),
 ('7128',),
 ('8128',),
 ('9128',))
_ACTION_DICT['rollRightStopActions'] = (('1130',),
 ('2130',),
 ('3130',),
 ('4130',),
 ('5130',),
 ('6130',),
 ('7130',),
 ('8130',),
 ('9130',))
_ACTION_DICT['rollBackStopActions'] = (('1132',),
 ('2132',),
 ('3132',),
 ('4132',),
 ('5132',),
 ('6132',),
 ('7132',),
 ('8132',),
 ('9132',))
_ACTION_DICT['rollFollowStopActions'] = (('1134',),
 ('2134',),
 ('3134',),
 ('4134',),
 ('5134',),
 ('6134',),
 ('7134',),
 ('8134',),
 ('9134',))
_ACTION_DICT['wingFlyStopActions'] = (('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',))
_ACTION_DICT['wingFlyNormalUpActions'] = (('21111',),
 ('21111',),
 ('21111',),
 ('21111',),
 ('21111',),
 ('21111',),
 ('21111',),
 ('21111',))
_ACTION_DICT['wingFlyNormalDownActions'] = (('21112',),
 ('21112',),
 ('21112',),
 ('21112',),
 ('21112',),
 ('21112',),
 ('21112',),
 ('21112',))
_ACTION_DICT['sliderDashStartActions'] = (('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',))
_ACTION_DICT['sliderDashActions'] = (('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',))
_ACTION_DICT['jumpRunStartActions'] = (('1119',),
 ('2119',),
 ('3119',),
 ('4119',),
 ('5119',),
 ('6119',),
 ('7119',),
 ('8119',),
 ('9119',))
_ACTION_DICT['jumpRunActions'] = (('1120',),
 ('2120',),
 ('3120',),
 ('4120',),
 ('5120',),
 ('6120',),
 ('7120',),
 ('8120',),
 ('9120',))
_ACTION_DICT['jumpRunUpActions'] = (('1121',),
 ('2121',),
 ('3121',),
 ('4121',),
 ('5121',),
 ('6121',),
 ('7121',),
 ('8121',),
 ('9121',))
_ACTION_DICT['fallRunFlyActions'] = (('1122',),
 ('2122',),
 ('3122',),
 ('4122',),
 ('5122',),
 ('6122',),
 ('7122',),
 ('8122',),
 ('9122',))
_ACTION_DICT['fallRunDownActions'] = (('1123',),
 ('2123',),
 ('3123',),
 ('4123',),
 ('5123',),
 ('6123',),
 ('7123',),
 ('8123',),
 ('9123',))
_ACTION_DICT['fallRunEndIdleActions'] = (('1124',),
 ('2124',),
 ('3124',),
 ('4124',),
 ('5124',),
 ('6124',),
 ('7124',),
 ('8124',),
 ('9124',))
_ACTION_DICT['fallRunBackEndActions'] = (('1125',),
 ('2125',),
 ('3125',),
 ('4125',),
 ('5125',),
 ('6125',),
 ('7125',),
 ('8125',),
 ('9125',))
_ACTION_DICT['fallRunEndRunActions'] = (('1126',),
 ('2126',),
 ('3126',),
 ('4126',),
 ('5126',),
 ('6126',),
 ('7126',),
 ('8126',),
 ('9126',))
_ACTION_DICT['fallLeftRunEndRunActions'] = (('1140',),
 ('2140',),
 ('3140',),
 ('4140',),
 ('5140',),
 ('6140',),
 ('7140',),
 ('8140',),
 ('9140',))
_ACTION_DICT['fallRightRunEndRunActions'] = (('1141',),
 ('2141',),
 ('3141',),
 ('4141',),
 ('5141',),
 ('6141',),
 ('7141',),
 ('8141',),
 ('9141',))
_ACTION_DICT['dashStartActions'] = (('1201',),
 ('1201',),
 ('1201',),
 ('1201',),
 ('1201',),
 ('1201',),
 ('1201',),
 ('1201',),
 ('1201',))
_ACTION_DICT['dashStopActions'] = (('1203',),
 ('1203',),
 ('1203',),
 ('1203',),
 ('1203',),
 ('1203',),
 ('1203',),
 ('1203',),
 ('1203',))
_ACTION_DICT['jumpDashStartActions'] = (('1208',),
 ('1208',),
 ('1208',),
 ('1208',),
 ('1208',),
 ('1208',),
 ('1208',),
 ('1208',),
 ('1208',))
_ACTION_DICT['jumpDashActions'] = (('1209',),
 ('1209',),
 ('1209',),
 ('1209',),
 ('1209',),
 ('1209',),
 ('1209',),
 ('1209',),
 ('1209',))
_ACTION_DICT['jumpDashUpActions'] = (('1210',),
 ('1210',),
 ('1210',),
 ('1210',),
 ('1210',),
 ('1210',),
 ('1210',),
 ('1210',),
 '1210')
_ACTION_DICT['fallDashFlyActions'] = (('1211',),
 ('1211',),
 ('1211',),
 ('1211',),
 ('1211',),
 ('1211',),
 ('1211',),
 ('1211',),
 ('1211',))
_ACTION_DICT['fallDashDownActions'] = (('1212',),
 ('1212',),
 ('1212',),
 ('1212',),
 ('1212',),
 ('1212',),
 ('1212',),
 ('1212',),
 ('1212',))
_ACTION_DICT['fallDashEndIdleActions'] = (('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',))
_ACTION_DICT['jumpDashStart1Actions'] = (('1214',),
 ('1214',),
 ('1214',),
 ('1214',),
 ('1214',),
 ('1214',),
 ('1214',),
 ('1214',),
 ('1214',))
_ACTION_DICT['jumpDash1Actions'] = (('1215',),
 ('1215',),
 ('1215',),
 ('1215',),
 ('1215',),
 ('1215',),
 ('1215',),
 ('1215',),
 ('1215',))
_ACTION_DICT['jumpDashUp1Actions'] = (('1216',),
 ('1216',),
 ('1216',),
 ('1216',),
 ('1216',),
 ('1216',),
 ('1216',),
 ('1216',),
 '1216')
_ACTION_DICT['fallDashFly1Actions'] = (('1217',),
 ('1217',),
 ('1217',),
 ('1217',),
 ('1217',),
 ('1217',),
 ('1217',),
 ('1217',),
 ('1217',))
_ACTION_DICT['fallDashDown1Actions'] = (('1218',),
 ('1218',),
 ('1218',),
 ('1218',),
 ('1218',),
 ('1218',),
 ('1218',),
 ('1218',),
 ('1218',))
_ACTION_DICT['fallDashEndIdle1Actions'] = (('1219',),
 ('1219',),
 ('1219',),
 ('1219',),
 ('1219',),
 ('1219',),
 ('1219',),
 ('1219',),
 ('1219',))
_ACTION_DICT['fallDashEndDashActions'] = (('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',))
_ACTION_DICT['jumpRunTwiceStart1Actions'] = (('1204',),
 ('1204',),
 ('1204',),
 ('1204',),
 ('1204',),
 ('1204',),
 ('1204',),
 ('1204',),
 ('1204',))
_ACTION_DICT['jumpRunTwice1Actions'] = (('1205',),
 ('1205',),
 ('1205',),
 ('1205',),
 ('1205',),
 ('1205',),
 ('1205',),
 ('1205',),
 ('1205',))
_ACTION_DICT['jumpRunTwiceUp1Actions'] = (('1206',),
 ('1206',),
 ('1206',),
 ('1206',),
 ('1206',),
 ('1206',),
 ('1206',),
 ('1206',),
 ('1206',))
_ACTION_DICT['fallRunTwiceFly1Actions'] = (('1207',),
 ('1207',),
 ('1207',),
 ('1207',),
 ('1207',),
 ('1207',),
 ('1207',),
 ('1207',),
 ('1207',))
_ACTION_DICT['fallRunTwiceDown1Actions'] = (('1123',),
 ('1123',),
 ('1123',),
 ('1123',),
 ('1123',),
 ('1123',),
 ('1123',),
 ('1123',),
 ('1123',))
_ACTION_DICT['fallRunTwiceEndIdle1Actions'] = (('1124',),
 ('1124',),
 ('1124',),
 ('1124',),
 ('1124',),
 ('1124',),
 ('1124',),
 ('1124',),
 ('1124',))
_ACTION_DICT['fallRunTwiceEndRun1Actions'] = (('1126',),
 ('1126',),
 ('1126',),
 ('1126',),
 ('1126',),
 ('1126',),
 ('1126',),
 ('1126',),
 ('1126',))
_ACTION_DICT['jumpRunTwiceStart2Actions'] = (('1220',),
 ('2119',),
 ('3119',),
 ('4119',),
 ('5119',),
 ('6119',),
 ('7119',),
 ('8119',),
 ('9119',))
_ACTION_DICT['jumpRunTwice2Actions'] = (('1221',),
 ('2120',),
 ('3120',),
 ('4120',),
 ('5120',),
 ('6120',),
 ('7120',),
 ('8120',),
 ('9120',))
_ACTION_DICT['jumpRunTwiceUp2Actions'] = (('1222',),
 ('2121',),
 ('3121',),
 ('4121',),
 ('5121',),
 ('6121',),
 ('7121',),
 ('8121',),
 ('9121',))
_ACTION_DICT['fallRunTwiceFly2Actions'] = (('1223',),
 ('2122',),
 ('3122',),
 ('4122',),
 ('5122',),
 ('6122',),
 ('7122',),
 ('8122',),
 ('9122',))
_ACTION_DICT['fallRunTwiceDown2Actions'] = (('1224',),
 ('2123',),
 ('3123',),
 ('4123',),
 ('5123',),
 ('6123',),
 ('7123',),
 ('8123',),
 ('9123',))
_ACTION_DICT['fallRunTwiceEndIdle2Actions'] = (('1124',),
 ('2124',),
 ('3124',),
 ('4124',),
 ('5124',),
 ('6124',),
 ('7124',),
 ('8124',),
 ('9124',))
_ACTION_DICT['fallRunTwiceEndRun2Actions'] = (('1126',),
 ('2126',),
 ('3126',),
 ('4126',),
 ('5126',),
 ('6126',),
 ('7126',),
 ('8126',),
 ('9126',))
_ACTION_DICT['jumpRunTwiceStart3Actions'] = (('1226',),
 ('2119',),
 ('3119',),
 ('4119',),
 ('5119',),
 ('6119',),
 ('7119',),
 ('8119',),
 ('9119',))
_ACTION_DICT['jumpRunTwice3Actions'] = (('1227',),
 ('2120',),
 ('3120',),
 ('4120',),
 ('5120',),
 ('6120',),
 ('7120',),
 ('8120',),
 ('9120',))
_ACTION_DICT['jumpRunTwiceUp3Actions'] = (('1228',),
 ('2121',),
 ('3121',),
 ('4121',),
 ('5121',),
 ('6121',),
 ('7121',),
 ('8121',),
 ('9121',))
_ACTION_DICT['fallRunTwiceFly3Actions'] = (('1229',),
 ('2122',),
 ('3122',),
 ('4122',),
 ('5122',),
 ('6122',),
 ('7122',),
 ('8122',),
 ('9122',))
_ACTION_DICT['fallRunTwiceDown3Actions'] = (('1230',),
 ('2123',),
 ('3123',),
 ('4123',),
 ('5123',),
 ('6123',),
 ('7123',),
 ('8123',),
 ('9123',))
_ACTION_DICT['fallRunTwiceEndIdle3Actions'] = (('1124',),
 ('2124',),
 ('3124',),
 ('4124',),
 ('5124',),
 ('6124',),
 ('7124',),
 ('8124',),
 ('9124',))
_ACTION_DICT['fallRunTwiceEndRun3Actions'] = (('1126',),
 ('2126',),
 ('3126',),
 ('4126',),
 ('5126',),
 ('6126',),
 ('7126',),
 ('8126',),
 ('9126',))
_ACTION_DICT['jumpDashTwiceStart1Actions'] = (('1220',),
 ('1220',),
 ('1220',),
 ('1220',),
 ('1220',),
 ('1220',),
 ('1220',),
 ('1220',),
 ('1220',))
_ACTION_DICT['jumpDashTwice1Actions'] = (('1221',),
 ('1221',),
 ('1221',),
 ('1221',),
 ('1221',),
 ('1221',),
 ('1221',),
 ('1221',),
 ('1221',))
_ACTION_DICT['jumpDashTwiceUp1Actions'] = (('1222',),
 ('1222',),
 ('1222',),
 ('1222',),
 ('1222',),
 ('1222',),
 ('1222',),
 ('1222',))
_ACTION_DICT['fallDashTwiceFly1Actions'] = (('1223',),
 ('1223',),
 ('1223',),
 ('1223',),
 ('1223',),
 ('1223',),
 ('1223',),
 ('1223',),
 ('1223',))
_ACTION_DICT['fallDashTwiceDown1Actions'] = (('1224',),
 ('1224',),
 ('1224',),
 ('1224',),
 ('1224',),
 ('1224',),
 ('1224',),
 ('1224',),
 ('1224',))
_ACTION_DICT['fallDashTwiceEndIdle1Actions'] = (('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',))
_ACTION_DICT['fallDashTwiceEndDash1Actions'] = (('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',))
_ACTION_DICT['jumpDashTwiceStart2Actions'] = (('1226',),
 ('1226',),
 ('1226',),
 ('1226',),
 ('1226',),
 ('1226',),
 ('1226',),
 ('1226',))
_ACTION_DICT['jumpDashTwice2Actions'] = (('1227',),
 ('1227',),
 ('1227',),
 ('1227',),
 ('1227',),
 ('1227',),
 ('1227',),
 ('1227',),
 ('1227',))
_ACTION_DICT['jumpDashTwiceUp2Actions'] = (('1228',),
 ('1228',),
 ('1228',),
 ('1228',),
 ('1228',),
 ('1228',),
 ('1228',),
 ('1228',),
 ('1228',))
_ACTION_DICT['fallDashTwiceFly2Actions'] = (('1229',),
 ('1229',),
 ('1229',),
 ('1229',),
 ('1229',),
 ('1229',),
 ('1229',),
 ('1229',),
 ('1229',))
_ACTION_DICT['fallDashTwiceDown2Actions'] = (('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',))
_ACTION_DICT['fallDashTwiceEndIdle2Actions'] = (('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',),
 ('1213',))
_ACTION_DICT['fallDashTwiceEndDash2Actions'] = (('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',),
 ('1232',))
_ACTION_DICT['slowFallDownActions'] = (('1225',),
 ('1225',),
 ('1225',),
 ('1225',),
 ('1225',),
 ('1225',),
 ('1225',),
 ('1225',))
_ACTION_DICT['fastFallDownActions'] = (('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',),
 ('1230',))
_ACTION_DICT['rushStart0Actions'] = (('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',))
_ACTION_DICT['rush0Actions'] = (('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',))
_ACTION_DICT['rushEnd0Actions'] = (('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',))
_ACTION_DICT['rushEndDown0Actions'] = (('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',))
_ACTION_DICT['rushStart1Actions'] = (('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',))
_ACTION_DICT['rush1Actions'] = (('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',))
_ACTION_DICT['rushEnd1Actions'] = (('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',))
_ACTION_DICT['rushEndDown1Actions'] = (('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',))
_ACTION_DICT['rushStart2Actions'] = (('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',),
 ('1233',))
_ACTION_DICT['rush2Actions'] = (('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',),
 ('1234',))
_ACTION_DICT['rushEnd2Actions'] = (('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',),
 ('1235',))
_ACTION_DICT['rushEndDown2Actions'] = (('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',),
 ('1236',))
_ACTION_DICT['rushStartWeaponInHandActions'] = (('1233',),
 ('2233',),
 ('3233',),
 ('4233',),
 ('5233',),
 ('6233',),
 ('7233',),
 ('8233',),
 ('9233',))
_ACTION_DICT['rushWeaponInHandActions'] = (('1234',),
 ('2234',),
 ('3234',),
 ('4234',),
 ('5234',),
 ('6234',),
 ('7234',),
 ('8234',),
 ('9234',))
_ACTION_DICT['rushEndWeaponInHandActions'] = (('1235',),
 ('2235',),
 ('3235',),
 ('4235',),
 ('5235',),
 ('6235',),
 ('7235',),
 ('8235',),
 ('9235',))
_ACTION_DICT['rushEndDownWeaponInHandActions'] = (('1236',),
 ('2236',),
 ('3236',),
 ('4236',),
 ('5236',),
 ('6236',),
 ('7236',),
 ('8236',),
 ('9236',))
_ACTION_DICT['horseWhistleActions'] = (('11100',),
 ('11100',),
 ('11100',),
 ('11100',),
 ('11100',),
 ('11100',),
 ('11100',),
 ('11100',))
_ACTION_DICT['horseJumpRunStartActions'] = [('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119'),
 ('11119', '31119')]
_ACTION_DICT['horseJumpRunActions'] = [('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120'),
 ('11120', '31120')]
_ACTION_DICT['horseJumpRunUpActions'] = [('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121'),
 ('11121', '31121')]
_ACTION_DICT['horseFallRunFlyActions'] = [('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122'),
 ('11122', '31122')]
_ACTION_DICT['horseFallRunDownActions'] = [('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212')]
_ACTION_DICT['horseFallRunEndIdleActions'] = [('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124'),
 ('11124', '31124')]
_ACTION_DICT['horseFallRunBackEndActions'] = [('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125'),
 ('11125', '31125')]
_ACTION_DICT['horseFallRunEndRunActions'] = [('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126'),
 ('11126', '31126')]
_ACTION_DICT['horseJumpDashStartActions'] = [('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208'),
 ('11208', '31208')]
_ACTION_DICT['horseJumpDashActions'] = [('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209'),
 ('11209', '31209')]
_ACTION_DICT['horseJumpDashUpActions'] = [('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210'),
 ('11210', '31210')]
_ACTION_DICT['horseFallDashFlyActions'] = [('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211'),
 ('11211', '31211')]
_ACTION_DICT['horseFallDashDownActions'] = [('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212'),
 ('11212', '31212')]
_ACTION_DICT['horseFallDashEndIdleActions'] = [('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213'),
 ('11213', '31213')]
_ACTION_DICT['horseRoarJumpActions'] = [('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104'),
 ('11104', '31104')]
_ACTION_DICT['horseSprintStopActions'] = [('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203'),
 ('11203', '31203')]
_ACTION_DICT['enterHorseActions'] = (('11214',),
 ('11214',),
 ('11214',),
 ('11214',),
 ('11214',),
 ('11214',),
 ('11214',),
 ('11214',))
_ACTION_DICT['leaveHorseActions'] = (('11215',),
 ('11215',),
 ('11215',),
 ('11215',),
 ('11215',),
 ('11215',),
 ('11215',),
 ('11215',))
_ACTION_DICT['leaveHorseEndActions'] = (('11216',),
 ('11216',),
 ('11216',),
 ('11216',),
 ('11216',),
 ('11216',),
 ('11216',),
 ('11216',))
_ACTION_DICT['wingNoFlyRushStartActions'] = (('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',))
_ACTION_DICT['wingFlyRushStartActions'] = (('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',),
 ('21107',))
_ACTION_DICT['wingFlyRushActions'] = (('21108',),
 ('21108',),
 ('21108',),
 ('21108',),
 ('21108',),
 ('21108',),
 ('21108',),
 ('21108',))
_ACTION_DICT['wingFlyRushEndActions'] = (('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',),
 ('21110',))
_ACTION_DICT['wingFlyUpStartActions'] = (('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',))
_ACTION_DICT['wingNoFlyUpStartActions'] = (('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',),
 ('21115',))
_ACTION_DICT['wingFlyUpActions'] = (('21116',),
 ('21116',),
 ('21116',),
 ('21116',),
 ('21116',),
 ('21116',),
 ('21116',),
 ('21116',))
_ACTION_DICT['wingFlyUpEndActions'] = (('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',))
_ACTION_DICT['wingFlyDownStartActions'] = (('21117',),
 ('21117',),
 ('21117',),
 ('21117',),
 ('21117',),
 ('21117',),
 ('21117',),
 ('21117',))
_ACTION_DICT['wingFlyDownActions'] = (('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',),
 ('21118',))
_ACTION_DICT['wingFlyDownEndActions'] = (('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',))
_ACTION_DICT['wingFlyLeftStartActions'] = (('21119',),
 ('21119',),
 ('21119',),
 ('21119',),
 ('21119',),
 ('21119',),
 ('21119',),
 ('21119',))
_ACTION_DICT['wingFlyLeftActions'] = (('21120',),
 ('21120',),
 ('21120',),
 ('21120',),
 ('21120',),
 ('21120',),
 ('21120',),
 ('21120',))
_ACTION_DICT['wingFlyRightStartActions'] = (('21121',),
 ('21121',),
 ('21121',),
 ('21121',),
 ('21121',),
 ('21121',),
 ('21121',),
 ('21121',))
_ACTION_DICT['wingFlyRightActions'] = (('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',),
 ('21122',))
_ACTION_DICT['wingFlyBackStartActions'] = (('21123',),
 ('21123',),
 ('21123',),
 ('21123',),
 ('21123',),
 ('21123',),
 ('21123',),
 ('21123',))
_ACTION_DICT['wingFlyBackActions'] = (('21124',),
 ('21124',),
 ('21124',),
 ('21124',),
 ('21124',),
 ('21124',),
 ('21124',),
 ('21124',))
_ACTION_DICT['wingFlyFastDownActions'] = (('21130',),
 ('21130',),
 ('21130',),
 ('21130',),
 ('21130',),
 ('21130',),
 ('21130',),
 ('21130',))
_ACTION_DICT['wingFlyFastDownEndActions'] = (('21131',),
 ('21131',),
 ('21131',),
 ('21131',),
 ('21131',),
 ('21131',),
 ('21131',),
 ('21131',))
_ACTION_DICT['wingFlyStartReadyActions'] = (('21127',),
 ('21127',),
 ('21127',),
 ('21127',),
 ('21127',),
 ('21127',),
 ('21127',),
 ('21127',))
_ACTION_DICT['wingFlyStartActions'] = (('21128',),
 ('21128',),
 ('21128',),
 ('21128',),
 ('21128',),
 ('21128',),
 ('21128',),
 ('21128',))
_ACTION_DICT['wingFlyStartToIdleActions'] = (('21129',),
 ('21129',),
 ('21129',),
 ('21129',),
 ('21129',),
 ('21129',),
 ('21129',),
 ('21129',))
_ACTION_DICT['fishingStartActions'] = (('51010',),
 ('51010',),
 ('51010',),
 ('51010',),
 ('51010',),
 ('51010',),
 ('51010',),
 ('51010',))
_ACTION_DICT['fishingPullActions'] = (('51023',),
 ('51023',),
 ('51023',),
 ('51023',),
 ('51023',),
 ('51023',),
 ('51023',),
 ('51023',))
_ACTION_DICT['fishingPullLoopActions'] = (('51024',),
 ('51024',),
 ('51024',),
 ('51024',),
 ('51024',),
 ('51024',),
 ('51024',),
 ('51024',))
_ACTION_DICT['fishingPullEndActions'] = (('51011',),
 ('51011',),
 ('51011',),
 ('51011',),
 ('51011',),
 ('51011',),
 ('51011',),
 ('51011',))
_ACTION_DICT['fishingBoredActions'] = (('51001',),
 ('51001',),
 ('51001',),
 ('51001',),
 ('51001',),
 ('51001',),
 ('51001',),
 ('51001',))
_ACTION_DICT['fishingReadyActions'] = (('51009',),
 ('51009',),
 ('51009',),
 ('51009',),
 ('51009',),
 ('51009',),
 ('51009',),
 ('51009',))
_ACTION_DICT['fishingHoldActions'] = (('51008',),
 ('51008',),
 ('51008',),
 ('51008',),
 ('51008',),
 ('51008',),
 ('51008',),
 ('51008',))
_ACTION_DICT['daZuoStartActions'] = (('1710',),
 ('1710',),
 ('1710',),
 ('1710',),
 ('1710',),
 ('1710',),
 ('1710',),
 ('1710',))
_ACTION_DICT['daZuoLoopActions'] = (('1711',),
 ('1711',),
 ('1711',),
 ('1711',),
 ('1711',),
 ('1711',),
 ('1711',),
 ('1711',))
_ACTION_DICT['daZuoStopActions'] = (('1712',),
 ('1712',),
 ('1712',),
 ('1712',),
 ('1712',),
 ('1712',),
 ('1712',),
 ('1712',))
_ACTION_DICT['manDownStartActions'] = (('1820',),
 ('2820',),
 ('3820',),
 ('4820',),
 ('5820',),
 ('6820',),
 ('7820',),
 ('8820',))
_ACTION_DICT['manDownStopActions'] = (('1821',),
 ('2821',),
 ('3821',),
 ('4821',),
 ('5821',),
 ('6821',),
 ('7821',),
 ('8821',))
_ACTION_DICT['chairIdleActions'] = (('31101',),
 ('31101',),
 ('31101',),
 ('31101',),
 ('31101',),
 ('31101',),
 ('31101',),
 ('31101',))
_ACTION_DICT['runForwardActions'] = (('1112',),
 ('2112',),
 ('3112',),
 ('4112',),
 ('5112',),
 ('6112',),
 ('7112',),
 ('8112',),
 ('9112',))
_ACTION_DICT['runBackActions'] = (('1113',),
 ('2113',),
 ('3113',),
 ('4113',),
 ('5113',),
 ('6113',),
 ('7113',),
 ('8113',),
 ('9113',))
_ACTION_DICT['runLeftActions'] = (('1114',),
 ('2114',),
 ('3114',),
 ('4114',),
 ('5114',),
 ('6114',),
 ('7114',),
 ('8114',),
 ('9114',))
_ACTION_DICT['runRightActions'] = (('1115',),
 ('2115',),
 ('3115',),
 ('4115',),
 ('5115',),
 ('6115',),
 ('7115',),
 ('8115',),
 ('9115',))
_ACTION_DICT['coupleEmoteStartActions'] = (('71941',),
 ('71941',),
 ('71941',),
 ('71941',),
 ('71941',),
 ('71941',),
 ('71941',),
 ('71941',),
 ('71941',))
_ACTION_DICT['coupleEmoteBeStartActions'] = (('72941',),
 ('72941',),
 ('72941',),
 ('72941',),
 ('72941',),
 ('72941',),
 ('72941',),
 ('72941',),
 ('72941',))
_ACTION_DICT['startToRunLeftActions'] = (('1117',),
 ('2117',),
 ('3117',),
 ('4117',),
 ('5117',),
 ('6117',),
 ('7117',),
 ('8117',),
 ('9117',))
_ACTION_DICT['startToRunRightActions'] = (('1116',),
 ('2116',),
 ('3116',),
 ('4116',),
 ('5116',),
 ('6116',),
 ('7116',),
 ('8116',),
 ('9116',))
_ACTION_DICT['runToIdleActions'] = (('1118',),
 ('2118',),
 ('3118',),
 ('4118',),
 ('5118',),
 ('6118',),
 ('7118',),
 ('8118',),
 ('9118',))

class ActionGroupMeta(type):

    def __init__(cls, name, bases, dic):
        super(ActionGroupMeta, cls).__init__(name, bases, dic)
        data = AAD.data.get((1, 10), {}).keys()
        for actionName in data:
            _funcName = 'get' + actionName[0].upper() + actionName[1:-1]

            def getFunction(self, fashion, name = actionName):
                actName = self.getActionByCaps(fashion).getAction(name)
                return fashion.getHorseWingActionKey(actName)

            setattr(cls, _funcName, getFunction)


class ActionGroup(object):
    __metaclass__ = ActionGroupMeta

    def __init__(self):
        super(ActionGroup, self).__init__()
        self.actionList = None
        self._cache = {}

    def getActionByCaps(self, fashion):
        caps = fashion.getCaps()
        if caps not in self._cache:
            self._cache[caps] = AdaptiveAction(self.actionList, caps)
        return self._cache[caps]


actionMap = {}

def getActionGroup(modelID):
    global actionMap
    if not actionMap.has_key(modelID):
        actionMap[modelID] = ActionGroup()
    return actionMap[modelID]


QINGGONG_ACTION_DICT = {'normalActions': ('runForwardActions', 'runBackActions', 'runLeftActions', 'runRightActions'),
 gametypes.QINGGONG_FLAG_ROLL: ('rollLeftStartActions', 'rollRightStartActions', 'rollBackStartActions', 'rollFollowStartActions', 'rollLeftStopActions', 'rollRightStopActions', 'rollBackStopActions', 'rollFollowStopActions'),
 gametypes.QINGGONG_FLAG_RUN_TWICE_JUMP: ('jumpRunTwiceStart1Actions', 'jumpRunTwice1Actions', 'jumpRunTwiceUp1Actions', 'fallRunTwiceFly1Actions', 'fallRunTwiceDown1Actions', 'fallRunTwiceEndIdle1Actions', 'fallRunTwiceEndRun1Actions', 'jumpRunTwiceStart2Actions', 'jumpRunTwice2Actions', 'jumpRunTwiceUp2Actions', 'fallRunTwiceFly2Actions', 'fallRunTwiceDown2Actions', 'fallRunTwiceEndIdle2Actions', 'fallRunTwiceEndRun2Actions', 'jumpRunTwiceStart3Actions', 'jumpRunTwice3Actions', 'jumpRunTwiceUp3Actions', 'fallRunTwiceFly3Actions', 'fallRunTwiceDown3Actions', 'fallRunTwiceEndIdle3Actions', 'fallRunTwiceEndRun3Actions'),
 gametypes.QINGGONG_FLAG_DASH_JUMP: ('jumpDashStartActions', 'jumpDashActions', 'jumpDashUpActions', 'fallDashFlyActions', 'fallDashDownActions', 'fallDashEndIdleActions', 'fallDashEndDashActions', 'jumpDashStart1Actions', 'jumpDash1Actions', 'jumpDashUp1Actions', 'fallDashFly1Actions', 'fallDashDown1Actions', 'fallDashEndIdle1Actions', 'fallDashEndDashActions'),
 gametypes.QINGGONG_FLAG_DASH_TWICE_JUMP: ('jumpDashTwiceStart1Actions', 'jumpDashTwice1Actions', 'jumpDashTwiceUp1Actions', 'fallDashTwiceFly1Actions', 'fallDashTwiceDown1Actions', 'fallDashTwiceEndIdle1Actions', 'fallDashTwiceEndDash1Actions', 'jumpDashTwiceStart2Actions', 'jumpDashTwice2Actions', 'jumpDashTwiceUp2Actions', 'fallDashTwiceFly2Actions', 'fallDashTwiceDown2Actions', 'fallDashTwiceEndIdle2Actions', 'fallDashTwiceEndDash2Actions'),
 gametypes.QINGGONG_FLAG_RIDE: ('horseJumpRunStartActions', 'horseJumpRunActions', 'horseJumpRunUpActions', 'horseFallRunFlyActions', 'horseFallRunDownActions', 'horseFallRunEndIdleActions', 'horseFallRunBackEndActions', 'horseFallRunEndRunActions', 'horseWhistleActions'),
 gametypes.QINGGONG_FLAG_RIDE_DASH_JUMP: ('horseJumpDashStartActions', 'horseJumpDashActions', 'horseJumpDashUpActions', 'horseFallDashFlyActions', 'horseFallDashDownActions', 'horseFallDashEndIdleActions'),
 gametypes.QINGGONG_FLAG_SLIDE_DASH: ('rushStart0Actions', 'rush0Actions', 'rushEnd0Actions', 'rushEndDown0Actions', 'rushStartWeaponInHandActions', 'rushWeaponInHandActions', 'rushEndWeaponInHandActions', 'rushEndDownWeaponInHandActions'),
 gametypes.QINGGONG_FLAG_WINGFLY_UP: ('wingFlyDownActions', 'wingFlyDownEndActions'),
 gametypes.QINGGONG_FLAG_WINGFLY_DASH: ('wingNoFlyRushStartActions', 'wingFlyRushStartActions', 'wingFlyRushActions', 'wingFlyRushEndActions'),
 gametypes.QINGGONG_FLAG_DASH: ('dashStartActions', 'dashStopActions')}

def getActionFromFlag(qingGongFlag, action, capIndexSet):
    qingGongActions = []
    if qingGongFlag in QINGGONG_ACTION_DICT.iterkeys():
        actNames = QINGGONG_ACTION_DICT[qingGongFlag]
        for actName in actNames:
            if qingGongFlag in (gametypes.QINGGONG_FLAG_ROLL, gametypes.QINGGONG_FLAG_SLIDE_DASH):
                for i in capIndexSet:
                    if i < len(_ACTION_DICT[actName]):
                        qingGongActions.extend(list(_ACTION_DICT[actName][i]))

            else:
                qingGongActions.extend(list(_ACTION_DICT[actName][0]))

    return qingGongActions
