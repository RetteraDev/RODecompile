#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impYabiao.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
from sfx import sfx
from guis import uiConst
from data import yabiao_data as YBD
from data import yabiao_config_data as YCD

class ImpYabiao(object):

    def acceptYabiao(self, ybId, res):
        gamelog.info('@szh acceptYabiao', ybId, res)
        if res:
            gameglobal.rds.ui.yaBiao.onAcceptYaBiao(ybId, res)
            if self.yabiaoData[gametypes.YABIAO_MARKER_SEQ] > 0:
                msg = YCD.data['adviceAbandonMsg'] % self.yabiaoData[gametypes.YABIAO_MARKER_SEQ]
                self.yabiaoUIID = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesBtnText=gameStrings.TEXT_IMPYABIAO_24, noCallback=lambda : self.quitGroup(), noBtnText=gameStrings.TEXT_IMPYABIAO_26)

    def acceptYabiaoMateConfirm(self, ybId, nuid, roleName, isWhole):
        gamelog.info('@szh acceptYabiaoMateConfirm', ybId, nuid, roleName, isWhole)
        self.yabiaoConfirmCB = BigWorld.callback(10, lambda : self.dismissYabiaoMsgBox())
        ybd = YBD.data[ybId]
        msg = ybd['yabiaoConfirmMsg']
        self.yabiaoUIID = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.onAcceptYabiaoMateConfirm(ybId, nuid, roleName, isWhole, True), noCallback=lambda : self.onAcceptYabiaoMateConfirm(ybId, nuid, roleName, isWhole, False))

    def dismissYabiaoMsgBox(self):
        if hasattr(self, 'yabiaoUIID'):
            gameglobal.rds.ui.messageBox.dismiss(self.yabiaoUIID)
            self.yabiaoUIID = 0

    def onAcceptYabiaoMateConfirm(self, ybId, nuid, roleName, isWhole, isConfirm):
        gamelog.info('@szh onAcceptYabiaoMateConfirm', self.yabiaoUIID, ybId, nuid, roleName, isWhole, isConfirm)
        if not self.inWorld:
            return
        if hasattr(self, 'yabiaoConfirmCB'):
            BigWorld.cancelCallback(self.yabiaoConfirmCB)
            self.yabiaoConfirmCB = 0
        self.cell.onAcceptYabiaoMateConfirm(ybId, nuid, roleName, isWhole, isConfirm)

    def abandonYabiao(self, ybId):
        gamelog.info('@szh abandonYabiao', ybId)
        gameglobal.rds.ui.yaBiao.hide()

    def triggerYabiao(self, npcId, res):
        gamelog.info('@szh triggerYabiao', npcId, res)
        gameglobal.rds.ui.yaBiao.onTriggerYabiao(res)

    def completeYabiao(self, ybId, res):
        gamelog.info('@szh completeYabiao', ybId, res)
        gameglobal.rds.ui.yaBiao.onCompleteYabiao(res, False)

    def completeFailedYabiao(self, ybId, res):
        gamelog.info('@szh completeFailedYabiao', ybId, res)
        gameglobal.rds.ui.yaBiao.onCompleteYabiao(res, True)

    def syncYabiaoZaiju(self, mhp, hp, position):
        gamelog.info('@szh syncYabiaoZaiju', mhp, hp, position)
        if self.yabiaoZaijuInfo != (hp, mhp):
            self.yabiaoZaijuInfo = (hp, mhp)
            gameglobal.rds.ui.yaBiao.refreshYabiaoZaijuBar()
        gameglobal.rds.ui.littleMap.addYabiaoZaiju(position)
        gameglobal.rds.ui.map.refreshYaBiaoIcon(position)

    def onYabiaoTimeOut(self):
        gamelog.info('@szh onYabiaoTimeOut')
        msg = YCD.data['timeoutMsg']
        self.yabiaoUIID = gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def hasYabiaoFailItem(self):
        if self.yabiaoData:
            ybId = self.yabiaoData[gametypes.YABIAO_ID]
            failItemId = YBD.data.get(ybId, {}).get('failItemId', 0)
            if failItemId:
                return self.inv.hasItemInPages(failItemId)
        return False

    def isYabiaoWhole(self):
        if self.yabiaoData:
            return self.yabiaoData.get(gametypes.YABIAO_WHOLE, False)
        return False

    def set_ybStatus(self, old):
        self.refreshYabiaoEffect()

    def refreshYabiaoEffect(self):
        if self.ybStatus:
            effectId = uiConst.YABIAO_EFFECT_DIFF_TEAM
            if self.groupNUID and self.groupNUID == BigWorld.player().groupNUID and not self._getZaijuNo():
                effectId = uiConst.YABIAO_EFFECT_SAME_TEAM
            self.addYabiaoEffect(effectId)
        else:
            self.addYabiaoEffect(None)

    def addYabiaoEffect(self, effectId):
        if not self.firstFetchFinished:
            return
        else:
            if hasattr(self, 'yabiaoEffect') and self.yabiaoEffect:
                if self.yabiaoEffect[0] == effectId:
                    return
                for fx in self.yabiaoEffect[1]:
                    fx.stop()

                self.yabiaoEffect = None
            if effectId:
                effectFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 effectId,
                 sfx.EFFECT_UNLIMIT,
                 sfx.KEEPEFFECTTIME))
                if effectFx:
                    self.yabiaoEffect = [effectId, effectFx]
            return

    def upgradeYabiao(self, res, oldZaijuNo, newZaijuNo):
        gamelog.info('@szh upgradeYabiao', res, oldZaijuNo, newZaijuNo)
        gameglobal.rds.ui.yaBiao.onUpgradeYabiao(res, oldZaijuNo, newZaijuNo)

    def hasYabiaoGuideEffect(self):
        minLv = const.MAX_LEVEL
        maxLv = 0
        guideMaxLv = YCD.data.get('guideMaxLv', 69)
        hasGuideMember = False
        for teamVal in self._getMembers().itervalues():
            if not teamVal.get('isOn'):
                continue
            teamValLv = teamVal.get('level', 0)
            if minLv > teamValLv:
                minLv = teamValLv
            if maxLv < teamValLv:
                maxLv = teamValLv
            if teamValLv <= guideMaxLv:
                hasGuideMember = True

        if maxLv - minLv > YCD.data.get('guideMarginLv', 9) and hasGuideMember:
            return True
        else:
            return False

    def onTeleportToYabiao(self, res, opNUID, position):
        gameglobal.rds.ui.yaBiao.onTeleportToYabiao(res)
