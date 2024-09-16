#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/guild_challenge_data.o
data = {4401: {'campPos': {'1': [(139.040329, 9.498602, 190.528763), (294.904175, 8.082396, 239.810608), (-163.355316, 0.350307, 3.040008)],
                    '2': [(7.084632, 2.096841, -152.008209), (191.140884, 4.503555, -99.53318), (478.019684, 15.764138, -84.934525)]},
        'durationTime': 1800,
        'initScore': 500,
        'name': 'Остров отчаяния %s',
        'numLimit': 100,
        'readyTime': 300},
 4402: {'campPos': {'1': [(139.040329, 9.498602, 190.528763), (294.904175, 8.082396, 239.810608), (-163.355316, 0.350307, 3.040008)],
                    '2': [(7.084632, 2.096841, -152.008209), (191.140884, 4.503555, -99.53318), (478.019684, 15.764138, -84.934525)]},
        'durationTime': 1800,
        'initScore': 300,
        'name': 'Остров отчаяния %s',
        'numLimit': 60,
        'readyTime': 300}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
