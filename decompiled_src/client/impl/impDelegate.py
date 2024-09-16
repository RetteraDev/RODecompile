#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impDelegate.o
from gamestrings import gameStrings
import gameglobal
import const
import gamelog
import commcalc
from delegationRecordList import DelegationRecordListValue
from data import delegation_data as DD
from data import quest_loop_data as QLD
from cdata import game_msg_def_data as GMDD
from cdata import delegation_cash_ratio_data as DCRD
from cdata import delegation_exp_ratio_data as DERD

class ImpDelegate(object):

    def set_bookDgts(self, old):
        gameglobal.rds.ui.delegationBook.refreshBook()

    def set_stableDgts(self, old):
        gameglobal.rds.ui.delegationBook.refreshBook()

    def set_lastRefTime(self, old):
        gameglobal.rds.ui.delegationBook.refreshLeftTimeTxt()

    def set_compDgtCnt(self, old):
        gameglobal.rds.ui.delegationBook.refreshCompDgtCnt()

    def set_delegationRank(self, old):
        gameglobal.rds.ui.delegationBook.showRankUp()

    def set_dailyCompDgtCnt(self, old):
        for data in DCRD.data.values():
            if data.get('num', 0) == self.dailyCompDgtCnt:
                if data.get('rate', 0) == 0:
                    tip = gameStrings.TEXT_IMPDELEGATE_38 % self.dailyCompDgtCnt
                else:
                    tip = gameStrings.TEXT_IMPDELEGATE_40 % (self.dailyCompDgtCnt, data.get('rate', 0) * 100)
                gameglobal.rds.ui.messageBox.showAlertBox(tip)
                break

        for data in DERD.data.values():
            if data.get('num', 0) == self.dailyCompDgtCnt:
                if data.get('rate', 0) == 0:
                    tip = gameStrings.TEXT_IMPDELEGATE_47 % self.dailyCompDgtCnt
                else:
                    tip = gameStrings.TEXT_IMPDELEGATE_49 % (self.dailyCompDgtCnt, data.get('rate', 0) * 100)
                gameglobal.rds.ui.messageBox.showAlertBox(tip)
                break

    def initDelegations(self):
        self.delegationVer = 0
        self.allDelegations = {}

    def sendDelegationRecord(self, delegationRecord):
        self.delegationRecords = delegationRecord

    def appendDelegationRecord(self, rid, time):
        if not hasattr(self, 'delegationRecords'):
            self.delegationRecords = []
        cVal = DelegationRecordListValue(rid, time)
        self.delegationRecords.append(cVal)

    def fetchDelegations(self, union, ranks, forceRef = False):
        if hasattr(self, 'lastUnion'):
            if self.lastUnion != union:
                forceRef = True
        self.lastUnion = union
        self.delegationVer = 0 if forceRef else self.delegationVer
        self.cell.fetchDelegations(union, ranks, self.delegationVer)

    def onFetchDelegations(self, allDelegations, ver, isRefresh):
        self.delegationVer = ver
        if isRefresh:
            self.allDelegations = allDelegations
            gameglobal.rds.ui.noticeBoard.updataAllDelegtion()
        else:
            oldDelegations = self.allDelegations
            self.allDelegations = allDelegations
            delKeys = []
            for key in oldDelegations.keys():
                if not self.allDelegations.has_key(key):
                    delKeys.append(str(key))

            if len(delKeys):
                gameglobal.rds.ui.noticeBoard.delDgts(delKeys)

    def acceptDelegation(self, nuid, dId, src, isSucc):
        if not DD.data.has_key(dId):
            return
        if isSucc:
            gameglobal.rds.ui.noticeBoard.acceptDone(nuid, src, dId)
            gameglobal.rds.ui.delegationBook.acceptDone(nuid, src, dId)
            self.onQuestInfoModifiedAtClient(const.QD_DELEGATION)

    def completeDelegation(self, dId, status, isSucc):
        gamelog.debug('@szh completeDelegation', dId, status, isSucc)
        if not DD.data.has_key(dId):
            return
        dd = DD.data[dId]
        questLoopId = dd['quest']
        qld = QLD.data[questLoopId]
        name = qld['name']
        if isSucc:
            if status == const.DS_TYPE_EMPLOY:
                self.showGameMsg(GMDD.data.ENTRUST_COMPLETE_ME, (name,))
            elif status == const.DS_TYPE_EMPLOYED:
                self.showGameMsg(GMDD.data.ENTRUST_COMPLETE_HE, (name,))
            self.delegationVer = 0
            self.onQuestInfoModifiedAtClient(const.QD_DELEGATION)

    def abandonDelegation(self, dId, status, isSucc):
        if isSucc:
            self.delegationVer = 0
            self.onQuestInfoModifiedAtClient(const.QD_ABANDON)
            dd = DD.data[dId]
            questLoopId = dd['quest']
            qld = QLD.data[questLoopId]
            name = qld['name']
            if status == const.DS_TYPE_EMPLOYED:
                self.showGameMsg(GMDD.data.ENTRUST_GIVEUP_HE, (name,))
            elif status == const.DS_TYPE_EMPLOY:
                self.showGameMsg(GMDD.data.ENTRUST_GIVEUP_ME, (name,))
            gameglobal.rds.ui.delegationBook.abandonDlgSucc(dId)

    def getDelegationData(self, key1, key2, default = None):
        if not self.hasDelegationData(key1, key2):
            return default
        return self.delegationData[key1][key2]

    def hasDelegationData(self, key1, key2):
        if not self.delegationData.has_key(key1):
            return False
        if not self.delegationData[key1].has_key(key2):
            return False
        return True

    def getPreDgtFlag(self, dId):
        return commcalc.getBit(self.preDgtFlags, dId)

    def transmitDelegation(self, dId, isSucc):
        if not DD.data.has_key(dId):
            return
        if isSucc:
            self.delegationVer = 0
            self.onQuestInfoModifiedAtClient(const.QD_DELEGATION)

    def abandonAgentDelegation(self, dId, isSucc):
        if not DD.data.has_key(dId):
            return
        if isSucc:
            self.delegationVer = 0
            self.onQuestInfoModifiedAtClient(const.QD_ABANDON)
