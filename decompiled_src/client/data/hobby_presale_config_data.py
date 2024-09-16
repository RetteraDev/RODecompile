#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/hobby_presale_config_data.o
data = {'alreadyFinished': 'С сожалением сообщаем вам, что все коды бронирования были выданы. Пожалуйста, дождитесь следующего раунда.',
 'alreadyGeted': 'Вы уже зарезервировали этот товар. Каждый аккаунт может сделать только одно бронирование.',
 'buyLink': 'https://gift.163.com/2017-tianyu.html',
 'deductDepositMailId': 1425,
 'deposit': 8000,
 'endTimeRrviewMsg': 'Бронирование закрыто. Пожалуйста, подождите следующую партию.',
 'lvLimit': 30,
 'nonReserve': 'Вы не зарезервировали ни одного товара. Зарезервируйте сначала перед запросом.',
 'nonReserveDeposit': 'Вы не зарезервировали эту подарочную коробку и не внесли депозит.',
 'presaleTimeCfg': {1: ('2017.05.18.19.30.00', '2017.05.18.22.00.00'),
                    2: ('2017.05.19.19.30.00', '2017.05.19.22.00.00'),
                    3: ('2017.05.22.19.30.00', '2017.05.22.22.00.00')},
 'queryLink': 'https://tianyu.163.com/2017/jinhe/',
 'refundDepositMailId': 1424,
 'refundMsgId': 11441,
 'remindMsgId': 11440,
 'reserveOvertime': 'Бронирование не удалось. Пожалуйста, попробуйте еще раз.',
 'subscribeMailId': 1423,
 'successGuide': "<a href = \'event: https: //gift.163.com/2017-tianyu.html\'><u><font color=’#008eac’>Нажмите, чтобы перейти</font></u></a> в магазин периферийных устройств, чтобы оплатить и завершить покупку.",
 'waitingRrviewMsg': 'Уведомления о бронировании будут выдаваться через системные уведомления. Не повторяйте процесс бронирования до их получения.'}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='string', vtype='int')
