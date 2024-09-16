#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impOfflineIncome.o
import gameglobal
from commOfflineIncome import OfflineIncomeVal

class ImpOfflineIncome(object):

    def notifyOfflineIncomes(self, dtos):
        vals = []
        for dto in dtos:
            val = OfflineIncomeVal().fromDTO(dto)
            vals.append(val)

        gameglobal.rds.ui.offlineIncome.incomes = vals
        gameglobal.rds.ui.offlineIncome.notifyUIPushMsg()

    def notifyOfflineIncome(self, dto):
        val = OfflineIncomeVal().fromDTO(dto)
        gameglobal.rds.ui.offlineIncome.incomes.append(val)
        gameglobal.rds.ui.offlineIncome.notifyUIPushMsg()

    def onFetchOfflineIncome(self, dbID):
        for data in gameglobal.rds.ui.offlineIncome.incomes:
            if dbID == data.dbID:
                gameglobal.rds.ui.offlineIncome.incomes.remove(data)
                break

        gameglobal.rds.ui.offlineIncome.notifyUIPushMsg()

    def onFetchOfflineIncomeFailed(self, dbID):
        gameglobal.rds.ui.offlineIncome.notifyUIPushMsg()
