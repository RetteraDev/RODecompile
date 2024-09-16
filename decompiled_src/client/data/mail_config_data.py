#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/mail_config_data.o
data = {'simpleKeepTime': 86400,
 'taxRate': 0.05,
 'paymentReadKeepTime': 2592000,
 'coinTaxRate': 0.05,
 'mallUnreadKeepTime': 43200000,
 'mallReadKeepTime': 43200000,
 'normalReadKeepTime': 86400}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
