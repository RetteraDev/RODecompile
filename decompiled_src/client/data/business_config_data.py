#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/business_config_data.o
data = {'blackPickInterval': 300,
 'businessFameId': 601,
 'buyStateTips': {1: 'Перепроизводство, цена снижается',
                  2: 'Недостаточный объем производства, цена повышается'},
 'delegationFeeRate': 0.03,
 'delegationMaxFee': 500000,
 'delegationMinFee': 5000,
 'dgtCntPersonPerday': 10,
 'saleReserveMargin': (0.2, 0.4, 0.6, 0.8, 1.0),
 'sellStateTips': 'Складские запасы: в каждой точке время от времени тратятся складские запасы. Чем больше товаров на складе, тем ниже цена продажи с этого местного склада после следующей корректировки цен'}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
