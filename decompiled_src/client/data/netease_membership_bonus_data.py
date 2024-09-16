#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/netease_membership_bonus_data.o
data = {2: {'bonusId': 18745,
     'desc': 'Вы можете получить его после привязки к торговому центру участника.',
     'name': 'Церемония связывания'},
 3: {'bonusId': 18743,
     'desc': 'Вы можете получить его после привязки к торговому центру участника в течение 3 месяцев подряд.',
     'name': 'Подарок долгой любви'},
 4: {'bonusId': 18744,
     'desc': 'Вы можете получить его после привязки к торговому центру участника, и вы не можете привязать другие игры в этом месяце.',
     'name': 'Индивидуальный подарок'},
 5: {'bonusId': 18746,
     'desc': 'В течение срока действия членства одна учетная запись ограничена одним разом.',
     'name': 'Встретиться'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
