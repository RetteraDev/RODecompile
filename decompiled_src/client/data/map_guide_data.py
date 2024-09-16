#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/map_guide_data.o
data = {1: {'guideRun': (100, 'guideAddMc', ['MapGuide_esc', 'guide_esc'])},
 2: {'guideRun': (500, 'guideAddMc', ['MapGuide_1', 'guide1'])},
 3: {'guideRun': (2000, 'guideDelMc', ['guide1'])},
 4: {'guideRun': (2000, 'guideAddMc', ['MapGuide_2', 'guide2'])},
 5: {'guideRun': (3000, 'guideDrag', [300, 300, 1])},
 6: {'guideRun': (5000, 'guideDelMc', ['guide2'])},
 7: {'guideRun': (5000, 'guideAddMc', ['MapGuide_3', 'guide3'])},
 8: {'guideRun': (6000, 'guideScale', [2, 100, 100])},
 9: {'guideRun': (7000, 'guideDelMc', ['guide3'])},
 10: {'guideRun': (7000, 'guideAddMc', ['MapGuide_4', 'guide4'])},
 11: {'guideRun': (8000, 'guideScale', [1, 100, 100])},
 12: {'guideRun': (9000, 'guideDelMc', ['guide4'])},
 13: {'guideRun': (10000, 'guideAddMc', ['MapGuide_5', 'guide5'])},
 14: {'guideRun': (12000, 'guideDelMc', ['guide5'])},
 15: {'guideRun': (12000, 'guideAddMc', ['MapGuide_6', 'guide6'])},
 16: {'guideRun': (16000, 'guideDelMc', ['guide6'])},
 17: {'guideRun': (16000, 'guideAddMc', ['MapGuide_7', 'guide7'])},
 18: {'guideRun': (22000, 'guideDelMc', ['guide7'])},
 19: {'guideRun': (22000, 'guideDelMc', ['guide_esc'])},
 20: {'guideRun': (23000, 'guideEnd', ['end'])}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
