#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/qte_data.o
data = {1: {'correctKey': 'A',
     'interval': 1.0,
     'lockCameraAndDc': 1,
     'type': 1},
 2: {'correctKey': 'S',
     'interval': 1.0,
     'lockCameraAndDc': 1,
     'type': 1},
 3: {'correctKey': 'W',
     'interval': 1.0,
     'lockCameraAndDc': 0,
     'type': 1},
 4: {'correctKey': 'D',
     'delayTime': 2.0,
     'interval': 1.0,
     'lockCameraAndDc': 1,
     'type': 1},
 11: {'exactDev': 0.5,
      'exactTime': 2.0,
      'interval': 3.0,
      'lockCameraAndDc': 0,
      'type': 2},
 12: {'delayTime': 3.0,
      'exactDev': 0.5,
      'exactTime': 2.0,
      'interval': 3.0,
      'lockCameraAndDc': 0,
      'type': 2},
 21: {'accumulateKey': 'A',
      'accumulateSum': 5,
      'attenuateTime': 0.3,
      'interval': 5.0,
      'lockCameraAndDc': 0,
      'type': 3},
 22: {'accumulateKey': 'A',
      'accumulateSum': 5,
      'attenuateTime': 0.3,
      'delayTime': 3.0,
      'interval': 5.0,
      'lockCameraAndDc': 0,
      'type': 3},
 30: {'correctKey': 'SPACE',
      'faceToTgt': 1,
      'interval': 1.0,
      'lockCameraAndDc': 0,
      'opSucc': (4, ''),
      'type': 1},
 31: {'accumulateKey': 'A',
      'accumulateSum': 2,
      'attenuateTime': 0.5,
      'delayTime': 0.8,
      'desc': 'Быстро нажмите A',
      'faceToTgt': 1,
      'interval': 1.5,
      'lockCameraAndDc': 0,
      'opSucc': (2, ''),
      'type': 3},
 32: {'accumulateKey': 'D',
      'accumulateSum': 2,
      'attenuateTime': 0.5,
      'delayTime': 0.8,
      'desc': 'Быстро нажмите D',
      'faceToTgt': 1,
      'interval': 1.5,
      'lockCameraAndDc': 0,
      'opSucc': (3, ''),
      'type': 3}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')