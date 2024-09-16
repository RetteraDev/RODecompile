#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/ymf_desc_data.o
data = {1: {'desc': '· Убийство вражеского игрока – 1 очко;'},
 2: {'desc': '· Убийство дозорного – 1 очко;'},
 3: {'desc': '· Сбор Вечноснежных кристаллов –  5 очков;'},
 4: {'desc': '· Убийство элитного монстра –  3 очка;'},
 5: {'desc': '· Убийство босса – 10 очков.'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
