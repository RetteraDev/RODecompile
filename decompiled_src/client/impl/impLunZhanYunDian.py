#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impLunZhanYunDian.o
import gamelog
import gameglobal
from guis import uiConst

class ImpLunZhanYunDian(object):

    def applyLunZhanYunDian(self):
        pass

    def syncLzydStage(self, stage):
        gamelog.info('yedawang### syncLzydStage', stage)
        gameglobal.rds.ui.LZYDPush.onChangeLZYDState(stage)

    def notifyAvatarMatch(self):
        gamelog.info('yedawang### notifyAvatarMatch')
        gameglobal.rds.ui.arenaCommonTips.show(uiConst.ARENA_MATCH_WAIT)

    def notifyAvatarApplySucc(self):
        gamelog.info('yedawang### notifyAvatarApplySucc')
        gameglobal.rds.ui.lunZhanYunDian.refreshInfo()

    def notifyAvatarMatchEnd(self):
        gamelog.info('yedawang### notifyAvatarMatchEnd')
        gameglobal.rds.ui.arenaCommonTips.hide()
