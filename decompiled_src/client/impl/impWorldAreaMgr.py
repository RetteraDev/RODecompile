#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldAreaMgr.o
import BigWorld
import formula
import gameglobal
import utils
import const
import gamelog
from item import Item
from data import world_quest_data as WQD
from data import world_area_data as WAD
from data import sys_config_data as SCD
from data import monster_model_client_data as MMCD
from data import item_data as ID

class ImpWorldAreaMgr(object):

    def set_worldQuests(self, old):
        gameglobal.rds.ui.littleMap.showWorldQuest()

    def onEnterArea(self, areaId, stateNo):
        gamelog.info('@szh onEnterArea %d %d' % (areaId, stateNo))
        if not formula.validWorldArea(areaId):
            return
        self._modifySkyZonePriority(areaId, stateNo)
        gameglobal.rds.ui.regionQuest.areaId = areaId
        gameglobal.rds.ui.regionQuest.showState(stateNo)
        gameglobal.rds.ui.questTrack.refreshRegionList()

    def onLeaveArea(self, areaId):
        gamelog.info('@szh onLeaveArea %d' % areaId)
        if not formula.validWorldArea(areaId):
            return
        gameglobal.rds.ui.regionQuest.areaId = 0
        gameglobal.rds.ui.regionQuest.closeState()
        gameglobal.rds.ui.questTrack.refreshRegionList()

    def onAreaStateChanged(self, areaId, oldState, newState):
        gamelog.info('@szh onAreaStateChanged %d %d %d' % (areaId, oldState, newState))
        self._modifySkyZonePriority(areaId, newState)
        self.onWAQuestInfoModifiedAtClient(const.WAQD_STATE_CHANGED)
        gameglobal.rds.ui.regionQuest.stateId = newState
        if gameglobal.rds.ui.regionQuest.stateMed:
            gameglobal.rds.ui.regionQuest.refreshRegionStateInfo()
        else:
            gameglobal.rds.ui.regionQuest.showState(newState)

    def acceptWorldAreaQuest(self, questId, accState):
        gameglobal.rds.ui.questTrack.showRegionNotice(questId)
        self.onWAQuestInfoModifiedAtClient(const.WAQD_ACCEPT, {})
        self._addWQMonsterFx(questId)

    def completeWorldAreaQuest(self, completeId, compStatus):
        gameglobal.rds.ui.questTrack.completeId = completeId
        self.onWAQuestInfoModifiedAtClient(const.WAQD_COMP, {})
        self._removeWQMonsterFx(completeId)

    def _modifySkyZonePriority(self, areaId, stateNo):
        if not WAD.data.has_key(areaId):
            return
        wad = WAD.data[areaId]
        if not wad.has_key('skyZonePriority'):
            return
        skyZone = wad['skyZonePriority']
        if not skyZone.has_key(stateNo):
            return
        tgtZoneName = skyZone[stateNo]
        for _, zoneName in skyZone.iteritems():
            if zoneName == tgtZoneName:
                BigWorld.setZonePriority(zoneName, 100)
            else:
                BigWorld.setZonePriority(zoneName, 1)

    def onWAQuestInfoModifiedAtClient(self, questDataId, exData = {}):
        gameglobal.rds.ui.questTrack.refreshRegionList()
        gameglobal.rds.ui.regionQuest.refreshRegionQuestInfo()
        gameglobal.rds.ui.regionQuest.refreshRegionStateInfo()
        pickNearDist = SCD.data.get('pickNearQuestBoxLength', 6) * SCD.data.get('pickNearQuestBoxLength', 6)
        entities = BigWorld.entities.values()
        questBoxes = [ x for x in entities if utils.instanceof(x, 'QuestBox') ]
        questBoxTraps = []
        for questBox in questBoxes:
            questBox.updateBoxState()
            if (questBox.position - BigWorld.player().position).lengthSquared < pickNearDist:
                questBoxTraps.append(questBox)

        BigWorld.player().boxTrapCallback(questBoxTraps)

    def needWaQuestItems(self, items, questId):
        if questId not in self.worldQuests:
            return
        wqd = WQD.data.get(questId, {})
        needItemIds = [ x[0] for x in wqd.get('compItemCollect', ()) if x[0] in items ]
        for itemId in items:
            if ID.data.get(itemId, {}).get('holdMax'):
                if Item.isQuestItem(itemId):
                    num = self.questBag.countItemInPages(itemId, includeExpired=True, includeLatch=True)
                else:
                    num = self.inv.countItemInPages(itemId, includeExpired=True, includeLatch=True)
                if num >= ID.data[itemId]['holdMax']:
                    gamelog.debug('zt: item reach holdMax', itemId, ID.data[itemId]['holdMax'], num)
                    return False

        if len(items) == 0:
            return True
        if len(needItemIds) > 0:
            return True
        return False

    def getWorldQuestData(self, key1, key2, default = None):
        questTrack = gameglobal.rds.ui.questTrack
        if not self.hasWorldQuestData(key1, key2):
            return default
        return questTrack.cacheWorldQuestInfo[key1][key2]

    def hasWorldQuestData(self, key1, key2):
        questTrack = gameglobal.rds.ui.questTrack
        if not questTrack.cacheWorldQuestInfo.has_key(key1):
            return False
        if not questTrack.cacheWorldQuestInfo[key1].has_key(key2):
            return False
        return True

    def set_worldStateData(self, old):
        gameglobal.rds.ui.regionQuest.refreshRegionStateInfo()

    def set_worldQuestData(self, old):
        if not getattr(self, 'worldQuestData', None):
            return
        else:
            gameglobal.rds.ui.questTrack.cacheWorldQuestInfo.update(self.worldQuestData)
            return

    def onFetchAreaStates(self, stateInfo):
        gameglobal.rds.ui.map.setAreaState(stateInfo)
        gameglobal.rds.ui.littleMap.showAreaInfo(stateInfo)

    def _addWQMonsterFx(self, questId):
        data = WQD.data.get(questId, None)
        if data and data.has_key('markerMonsters'):
            markerMonsters = data['markerMonsters']
            self._realAddFx(markerMonsters, 'charType', MMCD.data)

    def _removeWQMonsterFx(self, questId):
        data = WQD.data.get(questId, None)
        if data and data.has_key('markerMonsters'):
            self._realRemoveFx(data['markerMonsters'], 'charType', MMCD.data)

    def modifySkyZonePriority(self, zoneName, skyPriority):
        BigWorld.setZonePriority(zoneName, skyPriority)
