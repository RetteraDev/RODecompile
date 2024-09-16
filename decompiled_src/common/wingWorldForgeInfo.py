#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldForgeInfo.o
import BigWorld
import const
from wingWorldForge import WingWorldForge

class WingWorldForgeInfo(object):

    def createObjFromDict(self, dict):
        obj = WingWorldForge()
        data = dict['data']
        if not data:
            data = {}
        obj.carryRes = data.get('carryRes', {})
        obj.genItems = data.get('genItems', [])
        if type(obj.genItems) != list:
            obj.genItems = []
        obj.clientItems = data.get('clientItems', [])
        obj.level = data.get('level', 0)
        obj.state = data.get('state', 0)
        obj.genTimesWeekly = data.get('genTimesWeekly', 0)
        obj.lastStartTime = data.get('lastStartTime', 0)
        obj.round = data.get('round', 0)
        obj.round = data.get('round', 0)
        obj.count = data.get('count', 0)
        if obj.state == const.WINGWORLD_FORGE_STATE_START:
            obj.maxCount = len(obj.genItems)
            obj.maxRound = (obj.maxCount + const.WINGWORlD_FORGE_ROUND_NUM - 1) / const.WINGWORlD_FORGE_ROUND_NUM
        else:
            obj.maxRound = 0
            obj.maxCount = 0
        return obj

    def getDictFromObj(self, obj):
        data = {}
        data['carryRes'] = obj.carryRes
        data['genItems'] = obj.genItems
        data['clientItems'] = obj.clientItems
        data['level'] = obj.level
        data['state'] = obj.state
        data['genTimesWeekly'] = obj.genTimesWeekly
        data['lastStartTime'] = obj.lastStartTime
        data['round'] = obj.round
        data['count'] = obj.count
        dict = {'data': data}
        return dict

    def isSameType(self, obj):
        return type(obj) is WingWorldForge


instance = WingWorldForgeInfo()
