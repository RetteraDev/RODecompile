#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFameCollect.o
import commcalc
import const
import gameglobal
from data import fame_collect_content_data as FCCD
from data import fame_data as FD
from cdata import fame_collect_data as FCD

class ImpFameCollect(object):

    def onFinishFameCollect(self, fameCollectId):
        fccd = FCCD.data.get(fameCollectId)
        gameglobal.rds.ui.fameCollect.showTip(fccd)

    def _getFameCollect(self, fameId, keys):
        result = {}
        fcd = FCD.data.get(fameId, None)
        allCount = 0
        getCount = 0
        if fcd:
            for key in keys:
                fameCollects = fcd.get(key, [])
                keyResult = {}
                for fameCollect in fameCollects:
                    tmpResult = {}
                    allCount += 1
                    tmpResult['id'] = fameCollect
                    tmpResult['hasGet'] = commcalc.getBit(self.fameCollectInfo, fameCollect)
                    if tmpResult['hasGet']:
                        getCount += 1
                        fccd = FCCD.data.get(fameCollect)
                        if fccd:
                            tmpResult['name'] = fccd.get('name', '')
                            tmpResult['desc'] = fccd.get('desc', '')
                    else:
                        tmpResult['name'] = '??????'
                        tmpResult['desc'] = '??????'
                    keyResult[fameCollect] = tmpResult

                result[key] = keyResult

        result['count'] = (getCount, allCount)
        return result

    def isFameWithCollect(self, fameId):
        fame = FD.data.get(fameId)
        if fame and fame.get('withCollect', 0):
            return True
        return False

    def getHistoryFameCollect(self, fameId):
        return self._getFameCollect(fameId, const.SHI_FAME_COLLECT_TYPES)

    def getInterestFameCollect(self, fameId):
        return self._getFameCollect(fameId, const.QI_FAME_COLLECT_TYPES)

    def getAllFameCollect(self, fameId):
        return self._getFameCollect(fameId, const.SHI_FAME_COLLECT_TYPES + const.QI_FAME_COLLECT_TYPES)

    def _getFameCollectCount(self, fameId, keys):
        fcd = FCD.data.get(fameId, None)
        allCount = 0
        getCount = 0
        if fcd:
            for key in keys:
                fameCollects = fcd.get(key, [])
                for fameCollect in fameCollects:
                    allCount += 1
                    if commcalc.getBit(self.fameCollectInfo, fameCollect):
                        getCount += 1

        return (getCount, allCount)

    def getHistoryFameCollectCount(self, fameId):
        return self._getFameCollectCount(fameId, const.SHI_FAME_COLLECT_TYPES)

    def getInterestFameCollectCount(self, fameId):
        return self._getFameCollectCount(fameId, const.QI_FAME_COLLECT_TYPES)
