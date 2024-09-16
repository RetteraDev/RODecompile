#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impHierogram.o
import const
import gameglobal
import gamelog
import gameconfigCommon
from data import item_data as ID
from data import sys_config_data as SCD
from data import rune_effect_data as RED
from data import rune_data as RD
from cdata import game_msg_def_data as GMDD

class ImpHierogram(object):

    def onClearAndTransitToRuneResult(self, isSuccess):
        gamelog.warning('onClearAndTransitToRuneResult isSuccess:{}'.format(isSuccess))
        if isSuccess:
            gameglobal.rds.ui.roleInfo.equipRuneEquip()
            gameglobal.rds.ui.roleInfo.refreshHieroNotify()
            gameglobal.rds.ui.systemButton.showRoleInfoNotify()
        else:
            self.showGameMsg(GMDD.data.CLEAR_TRANSIT_TO_HIEROGRAM_BAG_FULL, ())

    def updateHierogramData(self, hieroEquip, hieroCrystals, effectsDict):
        gamelog.debug('@zq updateHierogramData', hieroEquip, hieroCrystals, effectsDict)
        self.hierogramDict['hieroEquip'] = hieroEquip
        self.hierogramDict['hieroCrystals'] = hieroCrystals
        self.hierogramDict['effectsDict'] = effectsDict
        pSkills, totalEffects = self._calcHieroArousePSkills(self.hierogramDict)
        self.hierogramDict['pSkills'] = pSkills
        self.hierogramDict['totalEffects'] = totalEffects
        if gameglobal.rds.configData.get('enableHierogram', False):
            gameglobal.rds.ui.roleInformationHierogram.refreshInfo()
            gameglobal.rds.ui.runeView.updatePskill()
            gameglobal.rds.ui.roleInfo.refreshHieroNotify()
            gameglobal.rds.ui.systemButton.showRoleInfoNotify()

    def onCrystalLevelUp(self, newCrystalItem):
        gamelog.debug('@zq onCrystalLevelUp', newCrystalItem)
        if gameglobal.rds.ui.runeLvUp.mediator:
            gameglobal.rds.ui.runeLvUp.addNewRuneItem(newCrystalItem)
        gameglobal.rds.ui.equipChangeRuneLvUp.onRuneLvUpNotify(newCrystalItem)

    def _checkArouseEffectsNeed(self, effectsTotal, effectsNeed):
        for i in range(const.RUNE_EFFECT_TYPE_NUM):
            if effectsTotal[i] < effectsNeed[i]:
                return False

        return True

    def _calcHieroArousePSkills(self, hierogramDict = {}):
        pSkills = {}
        hieroTotalEffects = self._calcHieroTotalEffects(hierogramDict=hierogramDict)
        for eID, pData in RED.data.iteritems():
            length = len(pData)
            for idx in range(length - 1, -1, -1):
                effectsNeed = pData[idx].get('runeEffectsNeed', [])
                if not effectsNeed:
                    continue
                if self._checkArouseEffectsNeed(hieroTotalEffects, effectsNeed):
                    pSkillID = pData[idx].get('pskillId', 0)
                    pSkillLevel = pData[idx].get('lv', 1)
                    if pSkillID:
                        pSkills[eID] = (pSkillID, pSkillLevel)
                        break

        return (pSkills, hieroTotalEffects)

    def _calcHieroTotalEffects(self, types = (const.RUNE_TYPE_TIANLUN, const.RUNE_TYPE_DILUN, const.RUNE_TYPE_BENYUAN), hierogramDict = {}):
        hieroCrystals = hierogramDict.get('hieroCrystals', {})
        curEquipCrystalValidDataDict = self.getCurEquipCrystalItemValidData(hieroCrystals)
        runeEffectsDict = {}
        for hieroType in types:
            runeEffectsDict[hieroType] = [0] * const.RUNE_EFFECT_TYPE_NUM
            crystalItemTPs = self._getCrystalListByType(hieroType, hieroCrystals=hieroCrystals)
            for hieroType, part in crystalItemTPs:
                crystal = hieroCrystals.get((hieroType, part), None)
                if not crystal:
                    continue
                effectData = self.getRuneData(crystal.id, 'runeEffects', None)
                if not effectData or len(effectData) != const.RUNE_EFFECT_TYPE_NUM:
                    continue
                if not curEquipCrystalValidDataDict.get((hieroType, part), True):
                    continue
                for i, val in enumerate(effectData):
                    runeEffectsDict[hieroType][i] += val

        totalEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        for hieroType in types:
            for i, val in enumerate(runeEffectsDict[hieroType]):
                totalEffects[i] += val

        return totalEffects

    def _getCrystalListByType(self, hieroType, hieroCrystals):
        res = []
        if not hieroCrystals:
            return res
        for (tp, part), crystalItem in hieroCrystals.iteritems():
            if tp == hieroType:
                res.append((tp, part))

        return res

    def getCurEquipCrystalItemValidData(self, hieroCrystalsDict):
        curEquipCrystalValidDataDict = dict()
        if not hieroCrystalsDict:
            return curEquipCrystalValidDataDict
        curCrystalEquipTypeNumDict = self.getCurCrystalEquipTypeNumDict(hieroCrystalsDict)
        crystalEquipTypeNumLimitDict = SCD.data.get('RuneEquipNumberLimit', {})
        for (hType, hPart), itemData in hieroCrystalsDict.iteritems():
            curEquipCrystalValidDataDict[hType, hPart] = True
            crystalEquipType = ID.data.get(itemData.id, {}).get('RuneEquipType', 0)
            if gameconfigCommon.enableHierogramLimit() and curCrystalEquipTypeNumDict.get(crystalEquipType, 0) > crystalEquipTypeNumLimitDict.get(crystalEquipType, 0):
                curEquipCrystalValidDataDict[hType, hPart] = False

        return curEquipCrystalValidDataDict

    def getCurCrystalEquipTypeNumDict(self, hieroCrystalsDict):
        tempCrystalEquipTypeNumDict = dict()
        if not hieroCrystalsDict:
            return tempCrystalEquipTypeNumDict
        for (hType, hPart), itemData in hieroCrystalsDict.iteritems():
            crystalEquipType = ID.data.get(itemData.id, {}).get('RuneEquipType', 0)
            if crystalEquipType:
                if crystalEquipType in tempCrystalEquipTypeNumDict:
                    tempCrystalEquipTypeNumDict[crystalEquipType] += 1
                else:
                    tempCrystalEquipTypeNumDict[crystalEquipType] = 1

        return tempCrystalEquipTypeNumDict

    def isClearAndTransitToHierogram(self):
        return self.runeBoard.runeEquip == None

    def onTransferToNewHierogram(self, newItem):
        gameglobal.rds.ui.equipChangeRuneExchange.onTransferToNewHierogram(newItem)
        gameglobal.rds.ui.equipChangeRuneSuperExchange.onTransferToNewHierogram(newItem)

    def onTransferBackOldHierogram(self, newItem):
        gameglobal.rds.ui.equipChangeRuneReturnOld.onTransferBackOldHierogram(newItem)

    def onFeedHierogram(self, newItem, addValue, realAddValue):
        addValue = addValue * 1.0 / 10000
        gameglobal.rds.ui.equipChangeRuneFeed.onFeedHierogram(newItem, addValue)

    def onComposeNewHierogram(self, newItem):
        gameglobal.rds.ui.equipChangeRuneLvUp.onRuneLvUpNotify(newItem)

    def onExchangeHierogramSucc(self):
        gameglobal.rds.ui.equipChangeRuneToItem.onExchangeHierogramSucc()
