#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wardrobe_suit_data.o
data = {(2, 2, 1002): {'icon': 621172,
                'suitItems': [(621172, 16347), (621687, 16350)],
                'suitName': 'Набор Жемчуг Дракона'},
 (3, 2, 1001): {'icon': 621173,
                'state': 3,
                'suitItems': [(621173, 16348), (621688, 16351)],
                'suitName': 'Рюкин',
                'tips': 'Длинные тени, колеблющиеся волны, шепот в золотом веке, красный макияж рано'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='tuple', vtype='dict')
