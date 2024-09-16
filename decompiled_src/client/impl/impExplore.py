#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impExplore.o
import BigWorld
import gametypes
import gameglobal
import gamelog
import formula
from data import special_life_skill_equip_data as SLSED
from data import explore_data as ED
from cdata import game_msg_def_data as GMDD

class ImpExplore(object):

    def exploreFinished(self, result, args):
        gameglobal.rds.ui.explore.exploreResult(result, args)
        if result == gametypes.EXPLORE_RES_OTHER_SPACE:
            self.showGameMsg(GMDD.data.TANMI_1, formula.whatSpaceName(args[0], True))
        elif result == gametypes.EXPLORE_RES_FARAWARY:
            scroll = self.exploreEquip.get(gametypes.EXPLORE_EQUIP_SCROLL)
            if scroll:
                exploreId = SLSED.data.get(scroll.id, {}).get('exploreId', 0)
                msg = ED.data.get(exploreId, {}).get('distMsg')
                if msg:
                    self.showGameMsg(msg, ())

    def onExploreTargetLose(self, scrollId):
        self.showGameMsg(GMDD.data.EXPLORE_TARGET_LOSE, ())

    def checkExploreEquip(self):
        equipNeed = (gametypes.EXPLORE_EQUIP_COMPASS,)
        errorMsg = (GMDD.data.EXPLORE_EQUIP_COMPASS,)
        for idx, part in enumerate(equipNeed):
            if self.exploreEquip.isEmpty(part):
                self.showGameMsg(errorMsg[idx], ())
                return False

        return True

    def onPrepareExplore(self, power):
        gamelog.debug('zt: sense power', power)
        gameglobal.rds.ui.explore.setPowerInfo(power)

    def useExploreItem(self, item, page, index):
        eData = SLSED.data.get(item.id, {})
        if eData.get('fishingEquipType') == gametypes.EXPLORE_EQU_TYPE_COMPASS:
            BigWorld.player().cell.exchangeInvExploreEqu(page, index, gametypes.EXPLORE_EQUIP_COMPASS)
        elif eData.get('fishingEquipType') == gametypes.EXPLORE_EQU_TYPE_SCROLL:
            if self.exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS):
                BigWorld.player().cell.equipScroll(0 if item.isOneQuest() else page, index, bool(item.isOneQuest()))
                gameglobal.rds.ui.explore.show()
            else:
                self.showGameMsg(GMDD.data.EXPLORE_EQUIP_COMPASS, ())

    def onExploreSucc(self):
        gameglobal.rds.ui.explore.showExploreSuc()

    def onGetExploreItem(self, items, isQuestItem):
        pass
