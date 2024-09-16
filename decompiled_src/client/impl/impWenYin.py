#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWenYin.o
import BigWorld
import gamelog
import utils
from item import Item
import gameglobal
import gameconfigCommon
from guis import uiConst
from gamestrings import gameStrings

class ImpWenYin(object):

    def onSendWenYinInfo(self, wenYin):
        """
        :param wenYin: WEN_YIN
        :return:
        """
        gamelog.info('jbx:onSendWenYinInfo', wenYin)
        setattr(self, 'wenYin', wenYin)
        self.fillGemToEquipments()

    def syncSubWenYin(self, subWenYin):
        gamelog.info('czf:syncSubWenYin', subWenYin)
        setattr(self, 'subWenYin', subWenYin)

    def fillGemToEquipments(self, refreshUI = True):
        if not gameconfigCommon.enableSplitWenYinFromEquip():
            return
        elif not getattr(self, 'wenYin', None):
            return
        else:
            wenYin = self.wenYin
            self.doFillGemToEquipments(self.equipment, wenYin)
            if refreshUI:
                gameglobal.rds.ui.roleInfo.refreshInfo()
                gameglobal.rds.ui.equipChangeInlayV2.refreshAll()
            return

    def doFillGemToEquipments(self, equipment, wenYin):
        for part, item in enumerate(equipment):
            for index, gemSlot in enumerate(getattr(item, 'yinSlots', [])):
                avatarGemSlot = wenYin.getGemSlot(part, uiConst.GEM_TYPE_YIN, index)
                if avatarGemSlot and avatarGemSlot.gem:
                    gemSlot.gem = avatarGemSlot.gem
                    gemSlot.gemProps = avatarGemSlot.gemProps
                    gemSlot.gem.isValidGem = wenYin.isPartValid(equipment, part, uiConst.GEM_TYPE_YIN, index)
                    if not gemSlot.gem.isValidGem:
                        if not wenYin.checkGemOrder(equipment, gemSlot.gem.id, part):
                            gemSlot.gem.unvalidStr = gameStrings.EQUIP_CHANGE_GEM_UNVALID_OVER_ORDER
                        else:
                            gemSlot.gem.unvalidStr = gameStrings.EQUIP_CHANGE_GEM_UNVALID_UNLOCK
                    else:
                        gemSlot.gem.unvalidStr = ''
                else:
                    gemSlot.gem = None

            for index, gemSlot in enumerate(getattr(item, 'yangSlots', [])):
                avatarGemSlot = wenYin.getGemSlot(part, uiConst.GEM_TYPE_YANG, index)
                if avatarGemSlot and avatarGemSlot.gem:
                    gemSlot.gem = avatarGemSlot.gem
                    gemSlot.gemProps = avatarGemSlot.gemProps
                    gemSlot.gem.isValidGem = wenYin.isPartValid(equipment, part, uiConst.GEM_TYPE_YANG, index)
                    if not gemSlot.gem.isValidGem:
                        if not wenYin.checkGemOrder(equipment, gemSlot.gem.id, part):
                            gemSlot.gem.unvalidStr = gameStrings.EQUIP_CHANGE_GEM_UNVALID_OVER_ORDER
                        else:
                            gemSlot.gem.unvalidStr = gameStrings.EQUIP_CHANGE_GEM_UNVALID_UNLOCK
                    else:
                        gemSlot.gem.unvalidStr = ''
                else:
                    gemSlot.gem = None

    def onAddSubWenYin(self, equipPos, slotPos, gemSlot):
        gamelog.info('jbx:onAddSubWenYin', equipPos, slotPos, gemSlot)
        gemId = gemSlot.gem.id
        gemData = utils.getEquipGemData(gemId)
        if gemData.get('type', 0) == Item.GEM_TYPE_YANG:
            gamelog.info('jbx:subWenYin yangSlots', equipPos, slotPos, gemSlot.gem.id)
            self.subWenYin[equipPos].yangSlots[slotPos] = gemSlot
        else:
            gamelog.info('jbx:subWenYin yinSlots', equipPos, slotPos, gemSlot.gem.id)
            self.subWenYin[equipPos].yinSlots[slotPos] = gemSlot
        gameglobal.rds.ui.equipChangeInlayV2.refreshAll()

    def onRemoveSubWenYin(self, equipPos, gemType, gemPos):
        gamelog.info('jbx:onRemoveSubWenYin', equipPos, gemType, gemPos)
        if gemType == Item.GEM_TYPE_YANG:
            self.subWenYin[equipPos].yangSlots[gemPos].removeGem()
        else:
            self.subWenYin[equipPos].yinSlots[gemPos].removeGem()
        gameglobal.rds.ui.equipChangeInlayV2.refreshAll()

    def onSwitchWenYinSucc(self, wenYin, subWenYin):
        gamelog.info('jbx:onSwitchWenYinSucc', wenYin, subWenYin)
        self.subWenYin = subWenYin
        self.wenYin = wenYin
        gameglobal.rds.ui.equipChangeInlayV2.isSubMode = False
        self.fillGemToEquipments(True)
        gameglobal.rds.ui.equipChangeInlayV2.refreshAll()
