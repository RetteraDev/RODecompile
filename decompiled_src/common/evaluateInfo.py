#Embedded file name: I:/bag/tmp/tw2/res/entities\common/evaluateInfo.o
from userInfo import UserInfo
from evaluate import *

class EvaluateInfo(UserInfo):

    def createObjFromDict(self, dict):
        if dict.has_key('syncAppearanceItemCollect'):
            syncAppearanceItemCollect = dict['syncAppearanceItemCollect']
        else:
            syncAppearanceItemCollect = False
        if dict.has_key('appearanceItemCollectSet'):
            appearanceItemCollectSet = dict['appearanceItemCollectSet']
        else:
            appearanceItemCollectSet = set()
        if not dict.has_key('appearanceItemCollectNewSet') or not dict['appearanceItemCollectNewSet']:
            appearanceItemCollectNewSet = set()
        else:
            appearanceItemCollectNewSet = dict['appearanceItemCollectNewSet']
        if dict.has_key('appearanceItemCollectEvaluateInfo'):
            appearanceItemCollectEvaluateInfo = dict['appearanceItemCollectEvaluateInfo']
        else:
            appearanceItemCollectEvaluateInfo = {}
        if None == appearanceItemCollectSet:
            appearanceItemCollectSet = set()
        if None == appearanceItemCollectEvaluateInfo:
            appearanceItemCollectEvaluateInfo = {}
        evaluate = Evaluate(syncAppearanceItemCollect, appearanceItemCollectSet, appearanceItemCollectNewSet, appearanceItemCollectEvaluateInfo)
        for info in dict['evaluateData']:
            tmpVal = EvaluateVal(info['evaluateId'], info['finishCount'], info['evaluated'])
            evaluate[info['evaluateId']] = tmpVal

        return evaluate

    def getDictFromObj(self, obj):
        evaluate = []
        for info in obj.itervalues():
            tmp = {'evaluateId': info.evaluateId,
             'finishCount': info.finishCount,
             'evaluated': info.evaluated}
            evaluate.append(tmp)

        return {'evaluateData': evaluate,
         'syncAppearanceItemCollect': obj.syncAppearanceItemCollect,
         'appearanceItemCollectSet': obj.appearanceItemCollectSet,
         'appearanceItemCollectNewSet': obj.appearanceItemCollectNewSet,
         'appearanceItemCollectEvaluateInfo': obj.appearanceItemCollectEvaluateInfo}

    def isSameType(self, obj):
        return type(obj) is Evaluate


instance = EvaluateInfo()
