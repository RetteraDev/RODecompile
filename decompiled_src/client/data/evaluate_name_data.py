#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/evaluate_name_data.o
data = {1: {'rateName1': 'Веселье',
     'rateName2': 'Полный сюрпризов',
     'rateName3': 'Идеальное руководство',
     'rateName4': 'Эффекты дисплея',
     'rateNameTips1': 'Бла бла',
     'rateNameTips2': 'Бла бла',
     'rateNameTips3': 'Бла бла',
     'rateNameTips4': 'Бла бла'},
 2: {'rateName1': 'Стиль',
     'rateName2': 'Красота',
     'rateName3': 'Практичность',
     'rateName4': 'Итог',
     'rateNameTips1': 'Подходит ли этот внешний вид вашему вкусу или стилю?',
     'rateNameTips2': 'Как вы думаете, этот внешний вид достаточно крутой?',
     'rateNameTips3': 'Достаточно ли полезен этот внешний вид? Вы будете продолжать использовать это?',
     'rateNameTips4': 'Пожалуйста, оцените этот пункт.'},
 3: {'rateName1': 'Итог',
     'rateName2': 'КПД',
     'rateName3': 'Творческий подход',
     'rateName4': 'интуитивность',
     'rateNameTips1': 'Вы довольны этим?',
     'rateNameTips2': 'Сбалансирован ли режим игры? Вы получили то, что хотели из этого?',
     'rateNameTips3': 'Вы чувствовали, что действия были творческими и уникальными?',
     'rateNameTips4': 'Был ли режим игры легким для понимания и интуитивно понятным?'},
 4: {'rateName1': 'фигура',
     'rateName2': 'участок',
     'rateName3': 'Опыт',
     'rateName4': 'Итог',
     'rateNameTips1': 'Персонажи живые и впечатляющие?',
     'rateNameTips2': 'Сюжетное содержание интересно и компактно?',
     'rateNameTips3': 'Является ли опыт последовательным и бесспорным?',
     'rateNameTips4': 'В целом, вам нравится этот сюжет?'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
