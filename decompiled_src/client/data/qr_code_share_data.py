#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/qr_code_share_data.o
data = {1: {'achievementName': 'Любит троицу II',
     'bgImgPath': 'MOBA',
     'playerInfo': '%s <font color=\"#FFCF40\"> Lv.%d %s</font>',
     'pushPriority': 0,
     'pushType': 1,
     'rewardId': 330419,
     'shareDesc': '«Кингс» убивает 3 человека подряд',
     'topNumberDesc': 'Это ваш первый раз в <font color = \"# E5BF73\"> %d </font>'},
 2: {'achievementName': 'Великолепная четверка II',
     'bgImgPath': 'MOBA',
     'playerInfo': '%s <font color=\"#FFCF40\"> Lv.%d %s</font>',
     'pushPriority': 1,
     'pushType': 1,
     'rewardId': 330409,
     'shareDesc': 'Кингс-шоуунд убивает 4 человека подряд',
     'topNumberDesc': 'Это ваше четвертое убийство <font color = \"# E5BF73\"> %d </font>'},
 3: {'achievementName': 'Пять из пяти II',
     'bgImgPath': 'MOBA',
     'playerInfo': '%s <font color=\"#FFCF40\"> Lv.%d %s</font>',
     'pushPriority': 2,
     'pushType': 1,
     'rewardId': 330410,
     'shareDesc': 'Победители королей убили 5 человек',
     'topNumberDesc': 'Это уже пятый раз, когда вы были убиты в <font color = \"# E5BF73\"> %d </font>'},
 10002: {'achievementName': 'Побеждает флаг',
         'bgImgPath': 'MOBA',
         'playerInfo': '%s <font color=\"#FFCF40\"> Lv.%d %s</font>',
         'rewardId': 331006,
         'shareDesc': 'Короли сражаются против первой победы'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')