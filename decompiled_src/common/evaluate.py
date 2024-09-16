#Embedded file name: I:/bag/tmp/tw2/res/entities\common/evaluate.o
import gamelog
import copy
import gametypes
from userSoleType import UserSoleType
from userDictType import UserDictType

class EvaluateVal(UserSoleType):

    def __init__(self, evaluateId, finishCount, evaluated = 0):
        """
        \xcd\xe6\xb7\xa8&\xcd\xe2\xb9\xdb\xc6\xc0\xbc\xdb\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9
        :param evaluateId: \xc6\xc0\xbc\xdb\xb1\xed\xb5\xc4id
        :param finishCount: \xb5\xb1\xc7\xb0id\xd2\xd1\xbe\xad\xcd\xea\xb3\xc9\xb5\xc4\xb4\xce\xca\xfd
        :param evaluated: \xb5\xb1\xc7\xb0id\xc6\xc0\xbc\xdb\xd3\xeb\xb7\xf1\xb5\xc4\xd0\xc5\xcf\xa2(\xb6\xd4\xcd\xe6\xb7\xa8\xc6\xc0\xbc\xdb\xc0\xb4\xcb\xb53\xb1\xed\xca\xbe\xd2\xd1\xbe\xad\xc6\xc0\xbc\xdb\xb9\xfd\xa3\xac\xb6\xd4\xcd\xe2\xb9\xdb\xc6\xc0\xbc\xdb\xc0\xb4\xcb\xb51\xb1\xed\xca\xbe\xbb\xf1\xc8\xa1\xc7\xb0\xc6\xc0\xbc\xdb\xb9\xfd\xa3\xac2\xb1\xed\xca\xbe\xbb\xf1\xc8\xa1\xba\xf3\xc6\xc0\xbc\xdb\xb9\xfd\xa3\xac3\xb1\xed\xca\xbe\xc7\xb0\xba\xf3\xb6\xbc\xc6\xc0\xbc\xdb\xb9\xfd)
        """
        self.evaluateId = evaluateId
        self.finishCount = finishCount
        self.evaluated = evaluated


class Evaluate(UserDictType):

    def __init__(self, syncAppearanceItemCollect = False, appearanceItemCollectSet = set(), appearanceItemCollectNewSet = set(), appearanceItemCollectEvaluateInfo = {}):
        super(Evaluate, self).__init__()
        self.syncAppearanceItemCollect = syncAppearanceItemCollect
        self.appearanceItemCollectSet = copy.copy(appearanceItemCollectSet)
        self.appearanceItemCollectNewSet = copy.copy(appearanceItemCollectNewSet)
        self.appearanceItemCollectEvaluateInfo = copy.copy(appearanceItemCollectEvaluateInfo)

    def _lateReload(self):
        super(Evaluate, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def updatePlayEvaluateInfo(self, evaluateId, finishCount):
        """
        \xb8\xfc\xd0\xc2\xc6\xc0\xbc\xdb\xca\xfd\xbe\xdd
        :param evaluateId:
        :param finishCount:
        :return:
        """
        if self.has_key(evaluateId):
            self[evaluateId].finishCount += finishCount
            return
        self[evaluateId] = EvaluateVal(evaluateId, finishCount)

    def checkPlayEvaluateCount(self, evaluateId, needValue):
        """
        \xbc\xec\xb2\xe9\xc6\xc0\xbc\xdb\xd0\xe8\xd2\xaa\xcd\xea\xb3\xc9\xb5\xc4\xb4\xce\xca\xfd\xca\xc7\xb7\xf1\xb4\xef\xb5\xbd\xd2\xaa\xc7\xf3
        :param evaluateId:
        :param needValue:
        :return:
        """
        if not self.has_key(evaluateId):
            return False
        return self[evaluateId].finishCount >= needValue

    def checkPlayEvaluated(self, evaluatedId, evaluatedValue):
        """
        \xbc\xec\xb2\xe2\xcd\xe6\xb7\xa8\xcf\xe0\xb9\xd8\xca\xc7\xb7\xf1\xd2\xd1\xbe\xad\xc6\xc0\xbc\xdb
        :param evaluatedId:
        :param evaluatedValue:
        :return:
        """
        if not self.has_key(evaluatedId):
            return False
        return self[evaluatedId].evaluated == evaluatedValue

    def applyPlayEvaluate(self, evaluateId, evaluated):
        """
        \xc6\xc0\xbc\xdb\xb2\xd9\xd7\xf7\xa3\xac\xb8\xfc\xd0\xc2\xc6\xc0\xbc\xdb\xd6\xb5\xa3\xac
        :param evaluateId:
        :param evaluated:
        :return:
        """
        if not self.has_key(evaluateId):
            return
        self[evaluateId].evaluated = evaluated

    def checkItemCollectEvaluated(self, evaluateId, items):
        """
        \xbc\xec\xb2\xe9\xcd\xe2\xb9\xdb\xca\xc7\xb7\xf1\xd2\xd1\xbe\xad\xc6\xc0\xbc\xdb\xb9\xfd
        :param evaluateId:
        :param items:
        :return:
        """
        if not self.appearanceItemCollectEvaluateInfo.has_key(evaluateId):
            return False
        collect = self.checkAppearanceItemCollected(items)
        if self.appearanceItemCollectEvaluateInfo[evaluateId] == gametypes.EVALUATE_APPLY_BEFORE:
            if not collect:
                return True
            return False
        if self.appearanceItemCollectEvaluateInfo[evaluateId] in (gametypes.EVALUATE_APPLY_AFTER, gametypes.EVALUATE_APPLY_YES):
            return True
        return False

    def applyItemCollectEvaluate(self, evaluateId, evaluated):
        """
        \xb8\xfc\xd0\xc2\xcd\xe2\xb9\xdb\xc6\xc0\xbc\xdb\xd6\xb5
        :param evaluateId:
        :param evaluated:
        :return:
        """
        self.appearanceItemCollectEvaluateInfo[evaluateId] = evaluated

    def getItemCollectEvaluateValue(self, evaluateId):
        """
        \xc8\xa1\xb5\xc3\xcd\xe2\xb9\xdb\xc6\xc0\xbc\xdb\xd6\xb5
        :param evaluateId:
        :return:
        """
        if not self.appearanceItemCollectEvaluateInfo.has_key(evaluateId):
            return 0
        return self.appearanceItemCollectEvaluateInfo[evaluateId]

    def checkAppearanceItemCollected(self, items):
        """
        \xbc\xec\xb2\xe9\xca\xc7\xb7\xf1\xd2\xd1\xbe\xad\xca\xd5\xbc\xaf\xd6\xb8\xb6\xa8\xb5\xc4\xb5\xc0\xbe\xdf\xc1\xd0\xb1\xed
        :param items:
        :return:
        """
        for itemId in self.appearanceItemCollectSet:
            if itemId in items:
                return True

        return False
