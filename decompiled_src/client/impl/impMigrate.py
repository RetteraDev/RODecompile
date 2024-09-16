#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMigrate.o
from gamestrings import gameStrings
import gameglobal
import gamelog
import const
from guis import uiUtils
from callbackHelper import Functor
from cdata import migrate_config_data as MCD
from cdata import migrate_server_data as MSD

class ImpMigrate(object):

    def onGenMigrateCondClient(self, migrateCondition, cItemNum):
        gameglobal.rds.ui.funcNpc.onFuncState()
        gameglobal.rds.ui.migrateServer.condition = migrateCondition
        gameglobal.rds.ui.migrateServer.show()

    def onApplyMigrate(self, migrateCondition, cItemNum):
        gameglobal.rds.ui.migrateServer.condition = migrateCondition
        selfId = int(gameglobal.rds.g_serverid)
        freeMigrate = MSD.data.get(selfId, {}).get('freeMigrate', 0)
        itemId = MCD.data.get('consumeItemId', 0)
        itemName = uiUtils.getItemColorName(itemId)
        if not freeMigrate:
            desc = MCD.data.get('migrateTip', gameStrings.TEXT_IMPMIGRATE_24) % (itemName, cItemNum)
        else:
            desc = MCD.data.get('freeMigrateTip', gameStrings.TEXT_IMPMIGRATE_26)
        gameglobal.rds.ui.doubleCheckWithInput.show(desc, 'YES', title=gameStrings.TEXT_GROUPPROXY_192, confirmCallback=Functor(self.confirmMigrateServer))

    def confirmMigrateServer(self):
        serverId = gameglobal.rds.ui.migrateServer.serverId
        migrateCondition = gameglobal.rds.ui.migrateServer.condition
        if migrateCondition.get(const.MIGRATE_COND_ISOLATE_BAIL, True):
            self._confirmMigrateIsolateBail()
        else:
            desc = MCD.data.get('migrateisolateBailTip', gameStrings.TEXT_IMPMIGRATE_37)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(desc, self._confirmMigrateIsolateBail)

    def _confirmMigrateIsolateBail(self):
        serverId = gameglobal.rds.ui.migrateServer.serverId
        migrateCondition = gameglobal.rds.ui.migrateServer.condition
        if migrateCondition.get(const.MIGRATE_COND_UNBIND_TIMES, True):
            self._confirmMigrateResetUnbindItemTimes()
        else:
            desc = MCD.data.get('migrateResetUnbindItemTimes', gameStrings.TEXT_IMPMIGRATE_49)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(desc, self._confirmMigrateResetUnbindItemTimes)

    def _confirmMigrateResetUnbindItemTimes(self):
        serverId = gameglobal.rds.ui.migrateServer.serverId
        self.cell.beginMigrate(serverId)

    def onQueryOpenMigrateServer(self, hostIds):
        gameStrings.TEXT_IMPMIGRATE_60
        gamelog.debug('@zhangkuo onQueryOpenMigrateServer [hostIds]', hostIds)
        gameglobal.rds.ui.migrateServer.visibleHostIds = hostIds
        gameglobal.rds.ui.migrateServer.realShowChooseServer()
