#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/wing_world_season_event_data.o
data = {1: {'msg': "<font color=\'#A8F000\'>%s</font> захватывает собственность <font color=\'#A8F000\'>%s</font>: город <font color=\'#27a5d9\'>%s</font>"},
 2: {'msg': "Сила страны <font color=\'#A8F000\'>%s</font> достигает <font color=\'#A8F000\'>%d ур.</font>"},
 3: {'msg': "<font color=\'#A8F000\'>%s</font> владеет городом <font color=\'#27a5d9\'>%s</font> и становится <font color=\'#A8F000\'>%s</font>"},
 4: {'msg': "<font color=\'#A8F000\'>%s</font> присоединяется к: <font color=\'#A8F000\'>%s</font>",
     'priority': 1},
 5: {'msg': "Из-за взаимодействия серверов <font color=\'#27a5d9\'>%s</font> теряет статус захвата"}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
