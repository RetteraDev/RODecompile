#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/personality_signature_data.o
data = {1: {'name': 'Фанаты'},
 2: {'name': 'Тупой товарищ по команде'},
 3: {'name': '17Ребенок'},
 4: {'isValid': 1,
     'name': 'Придурок'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
