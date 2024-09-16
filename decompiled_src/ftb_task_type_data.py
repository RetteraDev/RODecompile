#Embedded file name: /WORKSPACE/data/entities/common/cdata/ftb_task_type_data.o
data = {1: {'duration': 7,
     'typeDesc': '每日登录游戏，可随机获得3-10羲鸟指引\n提升瑰宝值和战力，将有助于获得相对较高的羲鸟指引',
     'typeName': '每日登录'},
 2: {'duration': 7,
     'typeDesc': '完成每日必做推荐活动，达到指定活跃，可随机获得相应的羲鸟指引',
     'typeName': '每日活跃'},
 3: {'duration': 7,
     'typeDesc': '达成周俸领取条件，可随机获得相应的羲鸟指引\n提升军阶等级，将有助于获得相对较高的羲鸟指引',
     'typeName': '军阶'},
 4: {'duration': 7,
     'typeDesc': '达成周俸领取条件，可随机获得相应的羲鸟指引\n提升驱魔等级，将有助于获得相对较高的羲鸟指引',
     'typeName': '驱魔'},
 5: {'duration': 7,
     'typeDesc': '在每场公会联赛结算时，将统计获胜方战队的所有成员，并进行羲鸟指引加成',
     'typeName': '公会联赛'},
 6: {'duration': 7,
     'typeDesc': '击杀/复活1名玩家，可随机获得相应的羲鸟指引',
     'typeName': '领地战'},
 7: {'duration': -1,
     'typeDesc': '人择灵宝，宝亦择人，伏羲通宝蕴灵生瑞，象征着吉祥丰顺\n提升家园富贵值等级，将有助于获得更高的羲鸟指引',
     'typeName': '家园富贵值'}}
from utils import convertToConst
data = convertToConst(data, name='_'.join(__name__.split('.')), ktype='int', vtype='dict')
