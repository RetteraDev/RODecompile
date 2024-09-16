#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/delegation_config_data.o
data = {'BookRefreshInterval': 3600,
 'CompDgtCompersateCash': 0,
 'BookRefreshRankDefinedCash': 3000,
 'BookRefreshTypeDefinedCash': 2000,
 'BookRefreshCashPerMinite': 90}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
