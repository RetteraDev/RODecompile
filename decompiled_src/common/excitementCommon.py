#Embedded file name: I:/bag/tmp/tw2/res/entities\common/excitementCommon.o
import sys
import BigWorld
import gametypes
import commcalc
if BigWorld.component == 'client':
    import gameglobal
if BigWorld.component in ('base', 'cell'):
    import gameconfig
from data import excitement_data as ECD
from cdata import excitement_feature_data as ECFD
from cdata import game_msg_def_data as GMDD
from data import avatar_lv_data as ALD

class ImpExcitementCommon(object):

    def checkLvUpperCondition(self, id):
        eData = ECD.data.get(id, {})
        lvMin, lvMax = eData.get('displayLv')
        upExp = ALD.data.get(self.lv, {}).get('upExp', sys.maxint)
        sExp = getattr(self, 'exp', 0)
        if self.lv == lvMax and sExp >= upExp or self.lv > lvMax:
            return True
        return False

    def checkAllCondition(self, id, isNeedTip = True):
        if BigWorld.component == 'base':
            return False
        if self.checkLvUpperCondition(id):
            return True
        eData = ECD.data.get(id, {})
        if self.lv < eData.get('openlv'):
            if not isNeedTip:
                return False
            if BigWorld.component == 'cell':
                p = self.client
            elif BigWorld.component == 'client':
                p = self
            p.showGameMsg(GMDD.data.EXCITEMENT_LV_NOT_ENOUGH, ())
            return False
        for keyNum in xrange(gametypes.EXCITEMENT_CONDITION_MAX):
            keyStr = 'condition%s' % str(keyNum if keyNum else '')
            if keyStr not in eData:
                continue
            conType, conPara = eData.get(keyStr)
            if conType == gametypes.EXCITEMENT_CONDITION_TYPE:
                if not self.getQuestFlag(conPara):
                    if not isNeedTip:
                        return False
                    if BigWorld.component == 'cell':
                        p = self.client
                    elif BigWorld.component == 'client':
                        p = self
                    p.showGameMsg(GMDD.data.EXCITEMENT_QUEST_UNDONE, ())
                    return False

        return True

    def isExcitementDone(self, id):
        return commcalc.getBit(self.excitementDoneList, id)

    def checkExcitementFeature(self, featureId):
        if BigWorld.component == 'client':
            if not gameglobal.rds.configData.get('enableExcitementFeatureCheck', False):
                return True
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableExcitementFeatureCheck():
                return True
        exData = ECFD.data.get(featureId, {})
        excitementId = exData.get('type')
        if excitementId and self.checkAllCondition(excitementId, False):
            return True
        return False

    def excitementLvUpTigger(self):
        if BigWorld.component == 'client':
            if not gameglobal.rds.configData.get('enableExcitementFeatureCheck', False):
                return
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableExcitementFeatureCheck():
                return
        doneList = []
        for id, data in ECD.data.iteritems():
            if not self.isExcitementDone(id) and self.checkLvUpperCondition(id):
                doneList.append(id)

        if BigWorld.component == 'client':
            self.cell.applyExciteReward(doneList, False)
        elif BigWorld.component == 'cell':
            self._applyExciteReward(doneList, False)

    def getExcitementByLv(self, isExcludeDone = True):
        result = []
        for id, data in ECD.data.iteritems():
            lvMin, lvMax = ECD.data.get(id, {}).get('displayLv')
            if lvMin <= self.lv <= lvMax:
                if isExcludeDone:
                    if not self.isExcitementDone(id):
                        result.append(id)
                else:
                    result.append(id)

        return result

    def getExcitementDoneList(self):
        result = []
        for id in ECD.data.iterkeys():
            if self.isExcitementDone(id):
                result.append(id)

        return result
