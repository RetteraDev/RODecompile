#Embedded file name: I:/bag/tmp/tw2/res/entities\common\cdata/wing_world_army_roles_data.o
data = {1: {'name': '帝国统帅'},
 2: {'name': '大将'},
 3: {'name': '大臣'},
 4: {'name': '将军'},
 5: {'name': '士兵'},
 11: {'name': '领导层 （包含1、2）'},
 12: {'name': '中层 （包含3、4）'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
