#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impExcitement.o
import gametypes
import gameglobal
import commcalc
import gamelog
from excitementCommon import ImpExcitementCommon

class ImpExcitement(ImpExcitementCommon):

    def onApplyExciteRewardSuccess(self, doneList, isLvTigger):
        gamelog.debug('@zq onApplyExciteRewardSuccess: ', doneList, isLvTigger)
        if doneList:
            gameglobal.rds.ui.excitementIcon.refreshInfo()
            gameglobal.rds.ui.excitementDetail.hide()
            if isLvTigger:
                gameglobal.rds.ui.excitementUnlockEffect.show(doneList[0])
            gameglobal.rds.ui.skill.refreshSkillBgBtn()
            gameglobal.rds.ui.wingAndMount.refreshTabBtn()
            gameglobal.rds.ui.systemButton.refreshSysBtn()
            if self.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM):
                gameglobal.rds.ui.roleInfo.openRune()
            if self.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_JINGJIE):
                gameglobal.rds.ui.roleInfo.openJingjie()
            gameglobal.rds.ui.skill.refreshSpecialSkill()
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
