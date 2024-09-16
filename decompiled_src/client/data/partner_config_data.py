#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/partner_config_data.o
data = {'PARTNER_NONE_TIPS': "Чтобы создать семью, соберите своих друзей и поговорите с <font color=\'#29b1cc\'><a href = \'event:seek:110160436\'>нотариусом</a></font>.",
 'activationLimit': 60000,
 'activationRewards': ((180000, 15511), (300000, 15512), (480000, 15513)),
 'partTitleNumStyle': {1: ('', '', '3', '4', '5'),
                       2: ('', '', '-', '-', '-'),
                       3: ('', '', '-', '-', '-'),
                       4: ('', '', '\xe2\x91\xa2', '\xe2\x91\xa3', '\xe2\x91\xa4'),
                       5: ('', '', 'III', 'IV', 'V')},
 'partnerRiteCarrierNos': {3: 1007,
                           4: 1008,
                           5: 1009},
 'partnerTitleId': 31131}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
