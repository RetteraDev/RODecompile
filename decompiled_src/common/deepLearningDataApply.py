#Embedded file name: I:/bag/tmp/tw2/res/entities\common/deepLearningDataApply.o
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType

class DeepLearningDataApplyItemVal(UserSoleType):

    def __init__(self, itemId, buyCount):
        self.itemId = itemId
        self.buyCount = buyCount

    def _lateReload(self):
        super(DeepLearningDataApplyItemVal, self)._lateReload()


class DeepLearningDataApplyItemInfo(UserDictType):

    def __init__(self):
        super(DeepLearningDataApplyItemInfo, self).__init__()

    def _lateReload(self):
        super(DeepLearningDataApplyItemInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addItem(self, itemIds):
        for itemId in itemIds:
            self[itemId] = DeepLearningDataApplyItemVal(itemId, 0)

    def checkBuyItem(self, itemId, maxBuyLimit):
        if not self.has_key(itemId):
            return False
        return self[itemId].buyCount + 1 <= maxBuyLimit

    def buyItem(self, itemId):
        if not self.has_key(itemId):
            return False
        self[itemId].buyCount += 1
        return True

    def listItemInfo(self):
        itemInfo = {}
        for info in self.itervalues():
            itemInfo[info.itemId] = info.buyCount

        return itemInfo


class DeepLearningDataApplyVal(UserSoleType):

    def __init__(self, gbId, firstPush, beginTime, item = DeepLearningDataApplyItemInfo()):
        self.gbId = gbId
        self.firstPush = firstPush
        self.beginTime = beginTime
        self.item = copy.copy(item)

    def _lateReload(self):
        super(DeepLearningDataApplyVal, self)._lateReload()
        self.item.reloadScript()


class DeepLearningDataApplyInfo(UserDictType):

    def __init(self):
        super(DeepLearningDataApplyInfo, self).__init__()

    def _lateReload(self):
        super(DeepLearningDataApplyInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addOnPushInfo(self, gbId, firstPush, beginTime, itemIds):
        if self.has_key(gbId):
            return
        self[gbId] = DeepLearningDataApplyVal(gbId, firstPush, beginTime)
        self[gbId].item.addItem(itemIds)

    def resetOnPushInfo(self, gbIds):
        for gbId in gbIds:
            self.pop(gbId, None)

    def checkBuyItem(self, gbId, itemId, maxBuyLimit):
        if not self.has_key(gbId):
            return False
        return self[gbId].item.checkBuyItem(itemId, maxBuyLimit)

    def buyItem(self, gbId, itemId):
        if not self.has_key(gbId):
            return False
        return self[gbId].item.buyItem(itemId)

    def listItemInfo(self, gbId):
        if not self.has_key(gbId):
            return {}
        return self[gbId].item.listItemInfo()

    def getFirstPush(self, gbId):
        if not self.has_key(gbId):
            return 0
        return self[gbId].firstPush

    def setFirstPush(self, gbId, firstPush):
        if not self.has_key(gbId):
            return
        self[gbId].firstPush = firstPush
