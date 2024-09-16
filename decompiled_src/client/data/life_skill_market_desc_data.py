#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/life_skill_market_desc_data.o
data = {1: {1: 'Руда',
     2: 'растения',
     3: 'Свиток идентификации'},
 2: {1: 'Расширение инвентаря',
     2: 'Сырье'},
 3: {1: 'Сырье',
     2: 'Материал'},
 4: {1: 'Ингредиенты',
     2: 'Целебные травы'},
 5: {1: 'Материал',
     2: 'Расширение инвентаря'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
