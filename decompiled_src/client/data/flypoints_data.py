#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/flypoints_data.o
data = {1: {'ports': {10001: (5669.4941, -1.1527, -2259.9292),
               10002: (5671.5166, -1.4414, -2250.6274),
               10003: (5680.1655, -1.3622, -2176.1897),
               10004: (5684.2598, -1.3622, -2082.9856),
               10005: (5691.7686, -1.385, -1976.874),
               10006: (5662.2598, -1.2923, -1779.0394),
               10007: (5661.3262, -1.3776, -1658.6456),
               10008: (5649.873, -1.1578, -1657.932)},
     'exclude_ports': (10002, 10003, 10004, 10005, 10006, 10007),
     'airlines': {(10001, 10008): ((5669.4941, -1.1527, -2259.9292),
                                   (5671.5166, -1.4414, -2250.6274),
                                   (5680.1655, -1.3622, -2176.1897),
                                   (5684.2598, -1.3622, -2082.9856),
                                   (5691.7686, -1.385, -1976.874),
                                   (5662.2598, -1.2923, -1779.0394),
                                   (5661.3262, -1.3776, -1658.6456),
                                   (5649.873, -1.1578, -1657.932))},
     'paths': {(10001, 10008): (10001, 10008)}},
 125: {'ports': {1250001: (248.51, 136.33, 215.3),
                 1250002: (297.06, 155.91, 235.19),
                 1250003: (302.08, 161.14, 239.84),
                 1250004: (303.61, 166.79, 249.46),
                 1250005: (302.07, 171.75, 257.04),
                 1250006: (289.36, 180.55, 291.4),
                 1250007: (284.94, 180.4986, 307.16)},
       'exclude_ports': (1250002, 1250003, 1250004, 1250005, 1250006),
       'airlines': {(1250001, 1250007): ((248.51, 136.33, 215.3),
                                         (297.06, 155.91, 235.19),
                                         (302.08, 161.14, 239.84),
                                         (303.61, 166.79, 249.46),
                                         (302.07, 171.75, 257.04),
                                         (289.36, 180.55, 291.4),
                                         (284.94, 180.4986, 307.16))},
       'paths': {(1250001, 1250007): (1250001, 1250007)}},
 121: {'ports': {1210017: (-76.3218, 101.6061, 45.3895),
                 1210019: (-113.7525, 81.1489, 72.0084),
                 1210021: (-163.8039, 73.1897, 83.6674),
                 1210023: (-205.5623, 75.4049, 78.8208),
                 1210024: (-218.9363, 76.5963, 67.5988),
                 1210025: (-223.807, 81.1526, 20.366),
                 1210026: (-226.7795, 75.0766, -3.2855),
                 1210027: (-237.2645, 49.4098, -42.9423),
                 1210001: (-235.139, 49.4877, -53.7978),
                 1210007: (-174.5208, 118.5217, -40.9963),
                 1210013: (-69.3091, 121.2137, -23.2133),
                 1210014: (-126.3884, 129.0232, -49.3063),
                 1210015: (-66.0309, 105.6951, 31.2651)},
       'exclude_ports': (1210017, 1210019, 1210021, 1210023, 1210024, 1210025, 1210026, 1210007, 1210013, 1210014, 1210015),
       'airlines': {(1210001, 1210027): ((-235.139, 52.4877, -53.7978),
                                         (-174.5208, 118.5217, -40.9963),
                                         (-126.3884, 129.0232, -49.3063),
                                         (-69.3091, 121.2137, -23.2133),
                                         (-66.0309, 105.6951, 31.2651),
                                         (-76.3218, 101.6061, 45.3895),
                                         (-113.7525, 81.1489, 72.0084),
                                         (-163.8039, 73.1897, 83.6674),
                                         (-205.5623, 75.4049, 78.8208),
                                         (-218.9363, 76.5963, 67.5988),
                                         (-223.807, 81.1526, 20.366),
                                         (-226.7795, 75.0766, -3.2855),
                                         (-237.2645, 49.4098, -42.9423))},
       'paths': {(1210001, 1210027): (1210001, 1210027)}}}
from utils import convertToConst
data = convertToConst(data, name=__name__.split('.')[-1], ktype='int', vtype='dict')