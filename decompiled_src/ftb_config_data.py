#Embedded file name: /WORKSPACE/data/entities/common/cdata/ftb_config_data.o
data = {'mallScoreDigTime': {1000: 100,
                      10000: 500,
                      40000: 1500,
                      100000: 3000}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
