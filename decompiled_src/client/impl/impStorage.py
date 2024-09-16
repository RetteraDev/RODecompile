#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impStorage.o
from gamestrings import gameStrings
import BigWorld
import const
import gameglobal
import gametypes
import npcConst
import utils
from guis import uiConst
from data import npc_data as ND
from cdata import game_msg_def_data as GMDD

class ImpStorage(object):

    def openStorage(self, id):
        if utils.isAbilityOn() and not self.getAbilityData(gametypes.ABILITY_STORAGE_ON):
            self.showGameMsg(GMDD.data.ABILITY_LACK_MSG, (gameStrings.TEXT_NPCFUNCMAPPINGS_1852,))
            return
        elif not BigWorld.entities.get(id):
            return
        else:
            npcId = BigWorld.entities.get(id).npcId
            npcData = ND.data.get(npcId, None)
            if npcData == None:
                return
            openType = npcData.get('full', 0)
            gameglobal.rds.ui.inventory.hide()
            if openType:
                gameglobal.rds.ui.funcNpc.openDirectly(self.id, npcId, npcConst.NPC_FUNC_STORAGE)
                gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)
            else:
                gameglobal.rds.ui.inventory.show(False)
            gameglobal.rds.ui.storage.show(id)
            return

    def storagePackSlotEnlarge(self, slotCnt):
        if self.storage.enabledPackSlotCnt < slotCnt:
            gameglobal.rds.ui.storage.enablePackSlot(self.storage.enabledPackSlotCnt)
        self.storage.enabledPackSlotCnt = slotCnt

    def setStoragePosCount(self, posCountDict):
        self.storage.posCountDict = posCountDict
        for i in range(0, const.STORAGE_PAGE_NUM):
            posCount = self.storage.posCountDict.get(i, 0)
            if posCount == 0:
                gameglobal.rds.ui.storage.setBagTabAble(i, False)
                if gameglobal.rds.ui.storage.page == i:
                    gameglobal.rds.ui.storage.setFirstTab()
            else:
                gameglobal.rds.ui.storage.setBagTabAble(i, True)
                if gameglobal.rds.ui.storage.page == i:
                    gameglobal.rds.ui.storage.setSlotCount(posCount)

    def removeAllStorageItem(self):
        for page in self.storage.posCountDict:
            for pos in self.storage.getPosTuple(page):
                if self.storage.getQuickVal(page, pos):
                    gameglobal.rds.ui.storage.removeItem(page, pos)
                    self.storage.removeObj(page, pos)
