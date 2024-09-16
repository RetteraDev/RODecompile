#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorldYabiao.o
import BigWorld
import gameglobal
import gamelog
import gametypes
from guis import uiConst
from gamestrings import gameStrings
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from callbackHelper import Functor

class ImpWingWorldYabiao(object):

    def checkInWingWorldCarrierStateOnClient(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return False
        try:
            return self.id in self.wingWorldCarrier
        except:
            gamelog.error('cgy#checkInWingWorldCarrierStateOnClient: ', self.id, type(self.wingWorldCarrier))
            return False

    def onSyncWingWorldYabiaoToGuildMembers(self, wingWorldYabiaoData):
        gamelog.info('jbx:onSyncWingWorldYabiaoToGuildMembers', wingWorldYabiaoData)
        self.wingWorldYabiaoData = wingWorldYabiaoData
        if not wingWorldYabiaoData.isYabiaoRunning() or not self.inWingPeaceCityOrBornIsland():
            gameglobal.rds.ui.wingWorldYaBiao.hide()
            gameglobal.rds.ui.wingWorldYaBiao.delPushIcon()
            return
        if gameglobal.rds.ui.wingWorldYaBiao.widget or gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO):
            gameglobal.rds.ui.wingWorldYaBiao.refreshInfo()
        else:
            gameglobal.rds.ui.wingWorldYaBiao.addPushIcon()
            gameglobal.rds.ui.wingWorldYaBiao.show()

    def onQueryWingWorldGuildResourceForYabiao(self, resources):
        self.guildResourcesList = resources
        gamelog.info('jbx:onQueryWingWorldGuildResourceForYabiao', resources)
        gameglobal.rds.ui.guildResourceCheck.show()

    def onWingWorldYabiaoDriverTeleportOk(self, dstCityId):
        pass

    def onSetWingWorldYabiaoDstCity(self, wingWorldYabiaoData):
        gamelog.info('jbx:onSetWingWorldYabiaoDstCity', wingWorldYabiaoData.yabiaoDestination)
        self.wingWorldYabiaoData = wingWorldYabiaoData
        gameglobal.rds.ui.wingWorldYaBiao.refreshInfo()

    def onWingWorldYabiaoDaKaSucc(self, wingWorldYabiaoData):
        gamelog.info('jbx:onWingWorldYabiaoDaKaSucc', wingWorldYabiaoData)
        self.wingWorldYabiaoData = wingWorldYabiaoData
        gameglobal.rds.ui.wingWorldYaBiao.refreshInfo()

    def onUpdateWingWorldYabiaoPrivateGoods(self, carryType):
        gamelog.info('jbx:onUpdateWingWorldYabiaoPrivateGoods', carryType)
        if not self.guild:
            self.wingWorldYabiaoPrivateGoods = carryType
        else:
            self.guild.wingWorldYabiaoPrivateGoods = carryType
            self.showGameMsg(GMDD.data.CHOOSE_PRIVATE_GOODS_SUCC, ())

    def onSeekHelpWhenYabiaoBeAttack(self, guildName, guildNUID):
        text = GMD.data.get(GMDD.data.WING_WORLD_YABIAO_BE_ATTACK_AND_SEEK_HELP, {}).get('text', '%s') % guildName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, BigWorld.player().cell.applyTeleportToBeAttackYabiaoZaiju)

    def applyYabiao(self):
        p = BigWorld.player()
        if getattr(p, 'wingWorldForgeData', None):
            resObsidianNum = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_OBSIDIAN, 0)
            resCateyeNum = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_CATEYE, 0)
            resDiamondNum = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_DIAMOND, 0)
            if resObsidianNum > 0 or resCateyeNum > 0 or resDiamondNum > 0:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.WING_WORLD_YABIAO_CONFIRM, Functor(self._confirmYaBiao))
            else:
                p._confirmYaBiao()
        else:
            p._confirmYaBiao()

    def _confirmYaBiao(self):
        p = BigWorld.player()
        guildResourcesList = getattr(p, 'guildResourcesList', [])
        gamelog.info('jbx:applyWingWorldYabiao', guildResourcesList)
        p.cell.applyWingWorldYabiao(guildResourcesList)
        BigWorld.callback(0.1, gameglobal.rds.ui.wingWorld.hide)
