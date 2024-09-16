#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRune.o
from gamestrings import gameStrings
import BigWorld
import const
import gametypes
import gameglobal
import gamelog
from guis import uiConst
from gameclass import PSkillInfo
from data import rune_qifu_effect_data as RQED
from data import rune_equip_xilian_effect_data as REXED
from data import rune_data as RD
from data import new_rune_data as NRD
from data import rune_prop_pskill_map_data as RPPMD
from cdata import game_msg_def_data as GMDD
from cdata import pskill_data as PD

class ImpRune(object):

    def onClearAndTransitToHierogramResult(self, isSuccess):
        if isSuccess:
            self.runeBoard.resetAll()
            gameglobal.rds.ui.roleInformationHierogram.refreshInfo()
            gameglobal.rds.ui.roleInfo.refreshHieroNotify()
            gameglobal.rds.ui.systemButton.showRoleInfoNotify()
        else:
            self.showGameMsg(GMDD.data.CLEAR_TRANSIT_TO_HIEROGRAM_BAG_FULL, ())
        gamelog.warning('onClearAndTransitToHierogramResult isSuccess: {}'.format(isSuccess))

    def clearRuneBoard(self):
        self.runeBoard.resetAll()
        gameglobal.rds.ui.runeView.removeItem(uiConst.RUNE_TYPE_EQUIP, 0)
        gameglobal.rds.ui.roleInfo.unEquipRuneEquip()
        gameglobal.rds.ui.roleInfo.updateRuneAwake()
        gameglobal.rds.ui.runeView.updatePskill()
        BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)

    def _recalcAllRuneSysData(self, runeEquip, runeEffects, awakeDict):
        """if self.runeBoard.runeEquip:
            oldRuneData = self.runeBoard.runeEquip.runeData
        else:
            oldRuneData = []
        
        oldDilunNum = 0
        oldTianlunNum = 0
        for runeDataVal in oldRuneData:
            if runeDataVal.runeSlotsType == const.RUNE_TYPE_DILUN:
                oldDilunNum = oldDilunNum + 1
            elif runeDataVal.runeSlotsType == const.RUNE_TYPE_TIANLUN:
                oldTianlunNum = oldTianlunNum + 1
        
        newRuneData = runeEquip.runeData
        newDilunNum = 0
        newTianlunNum = 0
        for runeDataVal in newRuneData:
            if runeDataVal.runeSlotsType == const.RUNE_TYPE_DILUN:
                newDilunNum = newDilunNum + 1
            elif runeDataVal.runeSlotsType == const.RUNE_TYPE_TIANLUN:
                newTianlunNum = newTianlunNum + 1
        if newTianlunNum > oldTianlunNum:
            gameglobal.rds.ui.roleInfo.playLunEffect(const.RUNE_TYPE_TIANLUN)
            pass
        if newDilunNum > oldDilunNum:
            gameglobal.rds.ui.roleInfo.playLunEffect(const.RUNE_TYPE_DILUN)
            pass  """
        self.runeBoard.resetAll()
        self.runeBoard.runeEquip = runeEquip
        self.runeBoard.runeEffectsDict = runeEffects
        self.runeBoard.awakeDict = awakeDict
        self.runeBoard.calcAllRuneEffects()
        self.runeBoard.calcShenLiJiFaPSkill()
        gameglobal.rds.ui.roleInfo.equipRuneEquip()
        gameglobal.rds.ui.runeView.updatePskill()
        BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
        if gameglobal.rds.ui.runeForging.mediator and gameglobal.rds.ui.runeForging.source == uiConst.RUNE_SOURCE_ROLE:
            for runeDataVal in self.runeBoard.runeEquip.runeData:
                if runeDataVal.runeSlotsType == gameglobal.rds.ui.runeForging.runePage and runeDataVal.part == gameglobal.rds.ui.runeForging.runePart:
                    it = runeDataVal.item
                    gameglobal.rds.ui.runeForging.addItem(it, uiConst.RUNE_REFORGING_EQUIP, 0)
                    break

        if gameglobal.rds.ui.runeReforging.mediator and gameglobal.rds.ui.runeReforging.source == uiConst.RUNE_SOURCE_ROLE:
            for runeDataVal in self.runeBoard.runeEquip.runeData:
                if runeDataVal.runeSlotsType == gameglobal.rds.ui.runeReforging.runePage and runeDataVal.part == gameglobal.rds.ui.runeReforging.runePart:
                    it = runeDataVal.item
                    gameglobal.rds.ui.runeReforging.addItem(it, uiConst.RUNE_REFORGING_EQUIP, 0)
                    break

        if gameglobal.rds.ui.runeChongXi.mediator and gameglobal.rds.ui.runeChongXi.runeSlotsType != None:
            gameglobal.rds.ui.runeChongXi.addXiLianSlot()

    def updateRuneSysData(self, runeEquip, runeEffects, awakeDict):
        gamelog.debug('@zq updateRuneSysData', runeEquip, runeEffects, awakeDict)
        self._recalcAllRuneSysData(runeEquip, runeEffects, awakeDict)

    def onRuneLvUp(self, rune):
        if gameglobal.rds.ui.runeLvUp.mediator:
            gameglobal.rds.ui.runeLvUp.addNewRuneItem(rune)
        gameglobal.rds.ui.equipChangeRuneLvUp.onRuneLvUpNotify(rune)
        gameglobal.rds.ui.equipChangeGemLvUp.onGemLvUpNotify(rune)
        gameglobal.rds.ui.equipChangeGemLvUpV2.onGemLvUpNotify(rune)

    def chongXiRunePreview(self, newXiLianId, xrData):
        if gameglobal.rds.ui.runeChongXi.mediator:
            msg = gameStrings.TEXT_IMPRUNE_108
            for skillId in xrData:
                skillLv = xrData[skillId]
                msg += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv)

            for effect in REXED.data[newXiLianId].get('effects', []):
                if effect[0] == gametypes.RUNE_EQUIP_XILIAN_EFFECT_TYPE_SHENLI:
                    msg += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2])

            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.comfirmChongXiRune, gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, self.cancelChongXiRune, gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def comfirmChongXiRune(self):
        if gameglobal.rds.ui.runeChongXi.mediator and gameglobal.rds.ui.runeChongXi.runeSlotsType != None:
            self.cell.comfirmChongXiRune(gameglobal.rds.ui.runeChongXi.runeSlotsType, gameglobal.rds.ui.runeChongXi.part)

    def cancelChongXiRune(self):
        if gameglobal.rds.ui.runeChongXi.mediator and gameglobal.rds.ui.runeChongXi.runeSlotsType != None:
            self.cell.cancelChongXiRune(gameglobal.rds.ui.runeChongXi.runeSlotsType, gameglobal.rds.ui.runeChongXi.part)

    def reforgingRunePreview(self, qiFuLv, qiFuId, qData):
        if gameglobal.rds.ui.runeReforging.mediator:
            msg = gameStrings.TEXT_IMPRUNE_129
            if qiFuLv == uiConst.RUNE_FORGING_LHIGH_LV:
                msg += gameStrings.TEXT_IMPRUNE_131
            else:
                msg += gameStrings.TEXT_IMPRUNE_133
            for skillId in qData:
                skillLv = qData[skillId]
                msg += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv)

            effects = RQED.data.get(qiFuId).get('effects', [])
            for effect in effects:
                if effect[0] == gametypes.RUNE_QIFU_EFFECT_TYPE_SHENLI:
                    msg += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2])

            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.comfirmReforgingRune, gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, self.cancelReforgingRune, gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def comfirmReforgingRune(self):
        npc = BigWorld.entities.get(gameglobal.rds.ui.runeReforging.npcId)
        if npc:
            if gameglobal.rds.ui.runeReforging.mediator:
                if gameglobal.rds.ui.runeReforging.source == uiConst.RUNE_SOURCE_INV:
                    npc.cell.comfirmInvReforgingRune(gameglobal.rds.ui.runeReforging.invPage, gameglobal.rds.ui.runeReforging.invPos)
                else:
                    npc.cell.comfirmRoleReforgingRune(gameglobal.rds.ui.runeReforging.runePage, gameglobal.rds.ui.runeReforging.runePart)

    def cancelReforgingRune(self):
        npc = BigWorld.entities.get(gameglobal.rds.ui.runeReforging.npcId)
        if npc:
            if gameglobal.rds.ui.runeReforging.mediator:
                if gameglobal.rds.ui.runeReforging.source == uiConst.RUNE_SOURCE_INV:
                    npc.cell.cancelInvReforgingRune(gameglobal.rds.ui.runeReforging.invPage, gameglobal.rds.ui.runeReforging.invPos)
                else:
                    npc.cell.cancelRoleReforgingRune(gameglobal.rds.ui.runeReforging.runePage, gameglobal.rds.ui.runeReforging.runePart)

    def isClearAndTransitToRune(self):
        ret = {}
        gameglobal.rds.ui.roleInformationHierogram.appendEquipData(ret, self.hierogramDict)
        if ret.get('itemInfos', {}).get('hieroEquipItem', None):
            return False
        elif ret.get('itemInfos', {}).get('benyuanItem', None):
            return False
        elif len(ret.get('itemInfos', {}).get('dilunItems', [])):
            return False
        elif len(ret.get('itemInfos', {}).get('tianlunItems', [])):
            return False
        else:
            return True

    def getRuneData(self, id, propName, defValue = None):
        if RD.data.has_key(id) and RD.data[id].has_key(propName):
            return RD.data[id][propName]
        if NRD.data.has_key(id) and NRD.data[id].has_key(propName):
            return NRD.data[id][propName]
        return defValue

    def genPropToNameMap(self):
        if hasattr(self, 'runeTypeMap'):
            return
        self.runeTypeMap = {}
        self.runeType2PropDic = {}
        for key, value in RPPMD.data.iteritems():
            for pSkillId in value.get('skills', []):
                self.runeTypeMap.setdefault((uiConst.RUNE_EFFECT_TYPE_SKILL, pSkillId), []).append(key)

            for propId in value.get('props', []):
                self.runeTypeMap.setdefault((uiConst.RUNE_EFFECT_TYPE_PROP, propId), []).append(key)

            typeName = value.get('typeName', '')
            newType = (value.get('runeEffectType', 1000), value.get('benyuanType', 1000), key)
            self.runeType2PropDic.setdefault(typeName, []).append(newType)

        for typeList in self.runeType2PropDic.values():
            typeList.sort()

    def getRuneOwnProp(self, itemId):
        if RD.data.has_key(itemId):
            pskillList = RD.data.get(itemId, {}).get('pskillList', ())
            if not pskillList:
                return ''
            skillId, lv = pskillList[0]
            return PD.data.get((skillId, lv), {}).get('desc', '')
        return NRD.data.get(itemId, {}).get('propDesc', '')

    def getRuneAddPercent(self, item):
        baseAdd = item.subSysProps.get(item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, {}).get('baseAdd', 0)
        feedAdd = item.subSysProps.get(item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, {}).get('feedAdd', 0)
        return (baseAdd + feedAdd) * 1.0 / 10000
