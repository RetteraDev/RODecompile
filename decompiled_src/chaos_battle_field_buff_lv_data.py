#Embedded file name: /WORKSPACE/data/entities/common/cdata/chaos_battle_field_buff_lv_data.o
data = {(1, 1): {'buffCnt': 1,
          'prop': 6000,
          'name': '����ף��'},
 (1, 2): {'buffCnt': 1,
          'prop': 6000,
          'name': 'Ǭ��ף��'},
 (2, 1): {'buffCnt': 2,
          'prop': 3000,
          'name': '����ף��'},
 (2, 2): {'buffCnt': 2,
          'prop': 3000,
          'name': 'Ǭ��ף��'},
 (3, 1): {'buffCnt': 5,
          'prop': 960,
          'name': '����ף��'},
 (3, 2): {'buffCnt': 5,
          'prop': 960,
          'name': 'Ǭ��ף��'},
 (4, 1): {'buffCnt': 10,
          'prop': 40,
          'name': '����ף��'},
 (4, 2): {'buffCnt': 10,
          'prop': 40,
          'name': 'Ǭ��ף��'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')