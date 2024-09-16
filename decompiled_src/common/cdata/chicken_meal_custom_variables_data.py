#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common\cdata/chicken_meal_custom_variables_data.o
data = {1: {'foodInfo': 'food_info1',
     'useSkillForFoodResult': 'skill_result1',
     'foodResult': 'food_result1'},
 2: {'foodInfo': 'food_info2',
     'useSkillForFoodResult': 'skill_result2',
     'foodResult': 'food_result2'},
 3: {'foodInfo': 'food_info3',
     'useSkillForFoodResult': 'skill_result3',
     'foodResult': 'food_result3'},
 4: {'foodInfo': 'food_info4',
     'useSkillForFoodResult': 'skill_result4',
     'foodResult': 'food_result4'},
 5: {'foodInfo': 'food_info5',
     'useSkillForFoodResult': 'skill_result5',
     'foodResult': 'food_result5'},
 6: {'foodInfo': 'food_info6',
     'useSkillForFoodResult': 'skill_result6',
     'foodResult': 'food_result6'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
