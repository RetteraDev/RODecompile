#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/avatarMorpherUtils.o
"""
Created on 2013-3-28

@author: bezy
"""
import random
SLIDER_MAX = 20.0
SLIDER_MIN = -20.0
SLIDER_DENSITY = 100.0
M2I_MAPPING = {}
I2M_MAPPING = {}

def genRandSliderValue():
    return random.uniform(SLIDER_MIN, SLIDER_MAX)


def genRandSliderDensityValue():
    return random.random()


def valueClip(x, a, b):
    a, b = min(a, b), max(a, b)
    if x < a:
        return a
    if x > b:
        return b
    return x


ZHUANGBAN_BTN = 1
BONE_VERTEX_SLIDER = 2
COLOR_TEST = 4
MOVIE_CLIP = 5
ZHUANGBAN_SLIDER = 6
COLOR_TEST_BTN = 7
FACE_U2M_MAPPING = {'eye_size': (1, 'eye_size_min', 'eye_size_max', 0),
 'eye_location1': (3, 'eye_location_up', 'eye_location_down', 0),
 'eye_spacing': (5, 'eye_spacing_min', 'eye_spacing_max', 0),
 'eye_width': (7, 'eye_width_min', 'eye_width_max', 1),
 'eye_canthus': (9, 'eye_canthus_up', 'eye_canthus_down', 1),
 'eye_shape': (11, 'eye_shape_1', 'eye_shape_2', 1),
 'eye_location2': (13, 'eye_location_front', 'eye_location_back', 0),
 'nose_location': (15, 'nose_location_up', 'nose_location_down', 0),
 'nose_width': (17, 'nose_width_min', 'nose_width_max', 1),
 'nose_bridge': (19, 'nose_bridge_lowest', 'nose_bridge_highest', 1),
 'nose_shape': (21, 'nose_shape_1', 'nose_shape_2', 1),
 'nose_angle': (23, 'nose_angle_up', 'nose_angle_down', 1),
 'nose_height': (25, 'nose_height_min', 'nose_height_max', 1),
 'mouth_location1': (27, 'mouth_location_up', 'mouth_location_down', 0),
 'mouth_location2': (29, 'mouth_location_front', 'mouth_location_back', 0),
 'mouth_width': (31, 'mouth_width_min', 'mouth_width_max', 0),
 'lip_upper': (33, 'lip_upper_thin', 'lip_upper_thick', 1),
 'lip_lower': (35, 'lip_lower_thin', 'lip_lower_thick', 1),
 'mouth_corner': (37, 'mouth_corner_up', 'mouth_corner_down', 0),
 'mouth_shape': (39, 'mouth_shape_1', 'mouth_shape_2', 0),
 'eyebrow_location1': (41, 'eyebrow_location_up', 'eyebrow_location_down', 0),
 'eyebrow_rotation': (43, 'eyebrow_rotation_min', 'eyebrow_rotation_max', 0),
 'eyebrow_location2': (45, 'eyebrow_location_front', 'eyebrow_location_back', 1),
 'cheekbones': (47, 'cheekbones_lowest', 'cheekbones_highest', 1),
 'faceWidth': (49, 'face_thin', 'face_thick', 0),
 'chin1': (51, 'chin_short', 'chin_long', 1),
 'chin2': (53, 'chin_thin', 'chin_thick', 1),
 'chin_shape': (55, 'chin_shape_1', 'chin_shape_2', 1),
 'chin_tip': (57, 'chin_tip_circular', 'chin_tip_sharp', 1),
 'chin_position': (59, 'chin_position_front', 'chin_position_back', 1),
 'chin_angle': (61, 'chin_angle_min', 'chin_angle_max', 1),
 'cheek': (63, 'cheek_thin', 'cheek_fat', 0),
 'eye_rotation': (65, 'eye_rotation_up', 'eye_rotation_down', 0),
 'eyelid_upper_shape': (67, 'eyelid_upper_shape_1', 'eyelid_upper_shape_2', 1),
 'eyelid_lower_shape': (69, 'eyelid_lower_shape_1', 'eyelid_lower_shape_2', 1),
 'lip_upper_width': (71, 'lip_upper_width_min', 'lip_upper_width_max', 1),
 'lip_lower_width': (73, 'lip_lower_width_min', 'lip_lower_width_max', 1),
 'eye_rotation1': (75, 'eye_rotation_min', 'eye_rotation_max', 0),
 'eyebrow_distance': (77, 'eyebrow_distance_min', 'eyebrow_distance_max', 0),
 'eye_rotation2': (79, 'eye_rotation_near', 'eye_rotation_far', 0)}
FACE_M2U_MAPPING = {}
FACE_MORPHER_DATA = []
BODY_U2M_MAPPING = {'tixing': (101, 'base_figure_thin', 'base_figure_thick', 0),
 'shengao': (103, 'base_height_min', 'base_height_max', 0),
 'tou': (105, 'head_size_min', 'head_size_max', 0),
 'bozi1': (107, 'neck_width_min', 'neck_width_max', 0),
 'bozi2': (109, 'neck_length_min', 'neck_length_max', 0),
 'xiongkuo': (111, 'chest_size_min', 'chest_size_max', 0),
 'jian1': (113, 'shoulder_width_min', 'shoulder_width_max', 0),
 'jian2': (115, 'shoulder_location_up', 'shoulder_location_down', 0),
 'jian3': (117, 'shoulder_size_min', 'shoulder_size_max', 0),
 'shoubi1': (119, 'arm_length_min', 'arm_length_max', 0),
 'shoubi2': (121, 'arm_size_min', 'arm_size_max', 0),
 'shou1': (123, 'hand_size_min', 'hand_size_max', 0),
 'shou2': (125, 'finger_length_min', 'finger_length_max', 0),
 'xiong1': (127, 'breast_size_min', 'breast_size_max', 0),
 'xiong2': (129, 'breast_angle_up', 'breast_angle_down', 0),
 'xiong3': (131, 'breast_angle_min', 'breast_angle_max', 0),
 'tun1': (133, 'pelvis_width_min', 'pelvis_width_max', 0),
 'tun2': (135, 'pelvis_thickness_min', 'pelvis_thickness_max', 0),
 'yao1': (137, 'waist_width_min', 'waist_width_max', 0),
 'yao2': (139, 'waist_length_min', 'waist_length_max', 0),
 'datui1': (141, 'thigh_length_min', 'thigh_length_max', 0),
 'datui2': (143, 'thigh_width_min', 'thigh_width_max', 0),
 'xiaotui1': (145, 'calf_length_min', 'calf_length_max', 0),
 'xiaotui2': (147, 'calf_size_min', 'calf_size_max', 0),
 'jiao': (149, 'foot_size_min', 'foot_size_max', 0)}
BODY_M2U_MAPPING = {}
DYE_U2M_MAPPING = {'pifu_color': (201,
                'skin_Color',
                ('head', 'skin'),
                1),
 'pifu_lightness': (202,
                    'skin_Specular',
                    ('head', 'skin'),
                    2),
 'pifu_gloss': (203,
                'skin_SpecularPower',
                ('head', 'skin'),
                2),
 'faxing_color': (204,
                  'hair_Color',
                  ('hair',),
                  1),
 'yanqiu_style': (205,
                  'diffuseTex',
                  ('eye',),
                  1),
 'yanqiu_color': (206,
                  'Pupil_Color',
                  ('eye',),
                  1),
 'yanbai_color': (207,
                  'Whites_Color',
                  ('eye',),
                  1),
 'yanqiu_size': (208,
                 'eyeSize',
                 ('eye',),
                 2),
 'meimao_style': (209,
                  'maskATex#1',
                  ('head',),
                  1),
 'meimao_density': (210,
                    'eyebrow_power',
                    ('head',),
                    2),
 'huxu_style': (211,
                'maskATex#2',
                ('head',),
                1),
 'meixu_color': (212,
                 'eyebrow_color',
                 ('head',),
                 1),
 'huazhuang_style': (213,
                     'maskBTex',
                     ('head',),
                     1),
 'yanxian_color': (214,
                   'eyeliner_color',
                   ('head',),
                   1),
 'yanxian_density': (215,
                     'eyeliner_power',
                     ('head',),
                     2),
 'yanying_color': (216,
                   'eyeshadow_color',
                   ('head',),
                   1),
 'yanying_density': (217,
                     'eyeshadow_power',
                     ('head',),
                     2),
 'yanying_lightness': (218,
                       'eyeshadow_Specular',
                       ('head',),
                       2),
 'yanying_gloss': (219,
                   'eyeshadow_SpecularPower',
                   ('head',),
                   2),
 'yanzhi_color': (220,
                  'blusher_color',
                  ('head',),
                  1),
 'yanzhi_density': (221,
                    'blusher_power',
                    ('head',),
                    2),
 'chungao_color': (222,
                   'lip_color',
                   ('head',),
                   1),
 'chungao_density': (223,
                     'lip_power',
                     ('head',),
                     2),
 'chungao_lightness': (224,
                       'lip_Specular',
                       ('head',),
                       2),
 'chungao_gloss': (225,
                   'lip_SpecularPower',
                   ('head',),
                   2),
 'zhuangshi_style': (226,
                     'maskCTex',
                     ('head',),
                     1),
 'xiaoxiang_style': (227,
                     'normalTex',
                     ('head',),
                     1),
 'zhouwen_style': (228,
                   'bumpTex',
                   ('head',),
                   1),
 'zhouwen_e_density': (229,
                       'Bump_R',
                       ('head',),
                       2),
 'zhouwen_yan_density': (230,
                         'Bump_G',
                         ('head',),
                         2),
 'zhouwen_zui_density': (231,
                         'Bump_B',
                         ('head',),
                         2),
 'zhouwen_lian_density': (232,
                          'Bump_A',
                          ('head',),
                          2),
 'zhuangshi_color': (233,
                     'facemask_color',
                     ('head',),
                     1),
 'zhuangshi_density': (234,
                       'facemask_power',
                       ('head',),
                       2),
 'xiaoxiang_style1': (236,
                      'diffuseTexHead',
                      ('head',),
                      1),
 'right_yanqiu_color': (237,
                        'Pupil_Color2',
                        ('eye',),
                        1),
 'right_yanbai_color': (238,
                        'Whites_Color2',
                        ('eye',),
                        1),
 'fanshe_style': (239,
                  'fansheTex',
                  ('eye',),
                  1),
 'fanshe_color': (240,
                  'Fanshe_Color',
                  ('eye',),
                  1),
 'female_meimao_style': (241,
                         'maskATex',
                         ('head',),
                         1),
 'jiemao_style': (242,
                  'diffuseTexJiemao',
                  ('eyelash',),
                  1)}
DYE_M2U_MAPPING = {}
DYE_MALE_ALIASES = {'huxu_density': 'yanzhi_density'}
DYE_MALE_DEALIASES = dict(zip(DYE_MALE_ALIASES.values(), DYE_MALE_ALIASES.keys()))
DYE_MORPH_BINDING = {'normalTex': 'diffuseTexHead',
 'diffuseTexHead': 'normalTex'}
DYE_MORPHER_COPY = {'Pupil_Color2': 'Pupil_Color',
 'Whites_Color2': 'Whites_Color'}
DYE_INDEX_COPY = {}

def __init():
    for k, v in FACE_U2M_MAPPING.iteritems():
        FACE_M2U_MAPPING[v[1]] = (k, 0)
        FACE_M2U_MAPPING[v[2]] = (k, 1)
        id1, id2 = str(v[0]), str(v[0] + 1)
        M2I_MAPPING[v[1]] = id1
        M2I_MAPPING[v[2]] = id2
        I2M_MAPPING[id1] = v[1]
        I2M_MAPPING[id2] = v[2]
        if v[3] == 1:
            FACE_MORPHER_DATA.append(v[1])
            FACE_MORPHER_DATA.append(v[2])

    for k, v in BODY_U2M_MAPPING.iteritems():
        BODY_M2U_MAPPING[v[1]] = (k, 0)
        BODY_M2U_MAPPING[v[2]] = (k, 1)
        id1, id2 = str(v[0]), str(v[0] + 1)
        M2I_MAPPING[v[1]] = id1
        M2I_MAPPING[v[2]] = id2
        I2M_MAPPING[id1] = v[1]
        I2M_MAPPING[id2] = v[2]

    for k, v in DYE_U2M_MAPPING.iteritems():
        DYE_M2U_MAPPING[v[1]] = (k, v[3])
        id1 = str(v[0])
        M2I_MAPPING[v[1]] = id1
        I2M_MAPPING[id1] = v[1]

    for k, v in DYE_MORPHER_COPY.iteritems():
        idk = M2I_MAPPING[k]
        idv = M2I_MAPPING[v]
        DYE_INDEX_COPY[idk] = idv


__init()

def getIdxByMorpher(morph):
    return M2I_MAPPING.get(morph, morph)


def getMorpherByIdx(idx):
    return I2M_MAPPING.get(idx, idx)


def _getMorpherScope(ui, resConfig):
    config = resConfig.get(ui) if resConfig else None
    if config and config[0] == 3:
        return (config[1][0], config[1][1])
    else:
        return (-1.0, 1.0)


def getFaceMorpherParamByUI(uiBtn, uiValue, resConfig = None):
    morph = FACE_U2M_MAPPING.get(uiBtn)
    if morph is None:
        return
    ratio = (uiValue - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN)
    minValue, maxValue = _getMorpherScope(uiBtn, resConfig)
    value = minValue + (maxValue - minValue) * ratio
    if value > 0:
        return (morph[3],
         morph[2],
         value,
         morph[1])
    else:
        return (morph[3],
         morph[1],
         -value,
         morph[2])


def getUIParamByFaceMorpher(morph, value, resConfig = None):
    ui = FACE_M2U_MAPPING.get(morph)
    if ui is None:
        return
    if ui[1] == 0:
        value = -value
    minValue, maxValue = _getMorpherScope(ui[0], resConfig)
    d = maxValue - minValue
    ratio = 0.0 if d == 0 else (value - minValue) / d
    uiValue = SLIDER_MIN + (SLIDER_MAX - SLIDER_MIN) * ratio
    return (ui[0], uiValue)


def getBodyMorpherParamByUI(uiBtn, uiValue, resConfig = None):
    morph = BODY_U2M_MAPPING.get(uiBtn)
    if morph is None:
        return
    ratio = (uiValue - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN)
    minValue, maxValue = _getMorpherScope(uiBtn, resConfig)
    value = minValue + (maxValue - minValue) * ratio
    if value > 0:
        return (morph[3],
         morph[2],
         value,
         morph[1])
    else:
        return (morph[3],
         morph[1],
         -value,
         morph[2])


def getUIParamByBodyMorpher(morph, value, resConfig = None):
    ui = BODY_M2U_MAPPING.get(morph)
    if ui is None:
        return
    if ui[1] == 0:
        value = -value
    minValue, maxValue = _getMorpherScope(ui[0], resConfig)
    d = maxValue - minValue
    ratio = 0.0 if d == 0 else (value - minValue) / d
    uiValue = SLIDER_MIN + (SLIDER_MAX - SLIDER_MIN) * ratio
    return (ui[0], uiValue)


def getDyeMorpherParamByUI(uiBtn, uiValue, isMale = False):
    if isMale:
        uiBtn = DYE_MALE_ALIASES.get(uiBtn, uiBtn)
    morph = DYE_U2M_MAPPING.get(uiBtn)
    if morph is None:
        return
    elif morph[3] == 1:
        return (morph[2], morph[1], int(uiValue))
    else:
        return (morph[2], morph[1], uiValue / SLIDER_DENSITY)


def getUIParamByDyeMorpher(morph, value, isMale = False):
    ui = DYE_M2U_MAPPING.get(morph)
    if ui is None:
        return
    else:
        uiBtn = isMale and DYE_MALE_DEALIASES.get(ui[0], ui[0]) or ui[0]
        if ui[1] == 1:
            return (uiBtn, int(value))
        return (uiBtn, value * SLIDER_DENSITY)
