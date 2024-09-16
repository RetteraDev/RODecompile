#Embedded file name: I:/bag/tmp/tw2/res/entities\common/deepLearningDataApplyInfo.o
from userInfo import UserInfo
from deepLearningDataApply import *

class deepLearningDataApplyInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = DeepLearningDataApplyInfo()
        for child in dict['data']:
            gbId = child['gbId']
            firstPush = child['firstPush']
            beginTime = child['beginTime']
            item = DeepLearningDataApplyItemInfo()
            for info in child['item']:
                item[info['itemId']] = DeepLearningDataApplyItemVal(info['itemId'], info['buyCount'])

            obj[gbId] = DeepLearningDataApplyVal(gbId, firstPush, beginTime, item)

        return obj

    def getDictFromObj(self, obj):
        data = []
        for info in obj.itervalues():
            itemInfo = []
            for item in info.item.itervalues():
                itemInfo.append({'itemId': item.itemId,
                 'buyCount': item.buyCount})

            data.append({'gbId': info.gbId,
             'firstPush': info.firstPush,
             'beginTime': info.beginTime,
             'item': itemInfo})

        return {'data': data}

    def isSameType(self, obj):
        return type(obj) is DeepLearningDataApplyInfo


instance = deepLearningDataApplyInfo()
