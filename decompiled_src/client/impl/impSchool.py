#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSchool.o
import gameglobal
import gamelog
from cdata import game_msg_def_data as GMDD

class ImpSchool(object):

    def onGenSchoolTransferCondition(self, opType, condition):
        gameglobal.rds.ui.schoolTransferCondition.updateConditionDict(condition)

    def sendSchoolTransferInfo(self, res):
        gameglobal.rds.ui.schoolTransferSelect.updateTransferInfo(res)

    def onQueryEntrustInfo(self, info):
        gamelog.debug('@zq onQueryEntrustInfo', info)
        if not info.get('lastDailyRefreshTime'):
            self.showGameMsg(GMDD.data.SCHOOL_ENTRUST_CANNOT_OPEN, ())
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.onDefaultState()
            return
        gameglobal.rds.ui.schoolEntrust.show(info)

    def onGetSchoolEntrustRewardSuc(self):
        self.cell.querySchoolEntrustInfo()

    def onUpdateSchoolEntrustCountInfo(self, info):
        self.schoolEntrustCountInfo = info
