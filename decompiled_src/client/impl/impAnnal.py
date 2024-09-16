#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAnnal.o
from gamestrings import gameStrings
import BigWorld
import utils
import formula
import game
import gamelog
import gameglobal
import gametypes
from callbackHelper import Functor
from helpers.annal import AnnalReplay
from helpers import annalUtils
from guis import uiConst

class ImpAnnal(object):

    def onStartAnnalReplay(self, host, port, uuid, index, hostId, live, fromStart):
        annalHostId = hostId or utils.getHostId()
        self.annalReplay = AnnalReplay(serverId=utils.getServerName(annalHostId), host=host, port=port, uuid=uuid, index=index, live=live, fromStart=fromStart)
        self._tryToStartAnnalReplay(bTimeout=False)

    def _tryToStartAnnalReplay(self, bTimeout = True):
        if not bTimeout and self.annalReplay.waitingTimerId:
            BigWorld.cancelCallback(self.annalReplay.waitingTimerId)
        self.annalReplay.waitingTimerId = 0
        if self.annalReplay.locked or not self.inWorld or not formula.spaceInAnnalReplay(self.spaceNo):
            gamelog.debug('_tryToStartAnnalReplay waiting for space ready')
            self.annalReplay.waitingTimerId = BigWorld.callback(2, Functor(self._tryToStartAnnalReplay))
            return
        self._clearAnnalEntities()
        self.annalReplay.startReplay()

    def onAnnalReplayFinished(self, stopByForce = False):
        if self.annalReplay.promptTimerId:
            BigWorld.cancelCallback(self.annalReplay.promptTimerId)
            self.annalReplay.promptTimerId = 0
        if stopByForce:
            self._stopAnnalReplay()
        else:
            self.annalReplay.promptTimerId = BigWorld.callback(10, Functor(self._showAnnalReplayFinishedPrompt))

    def _showAnnalReplayFinishedPrompt(self):
        self.annalReplay.messageBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPANNAL_46, Functor(self._stopAnnalReplay), noCallback=Functor(self._cancelStopAnnalReplay))

    def _stopAnnalReplay(self, bExit = False):
        if bExit:
            if annalUtils.stopPlay():
                return
        if self.annalReplay.messageBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.annalReplay.messageBoxId)
        self.annalReplay.locked = False
        self.annalReplay.messageBoxId = None
        self.annalReplay.promptTimerId = 0
        self.cell.stopAnnalReplay()
        self._clearAnnalEntities()

    def _cancelStopAnnalReplay(self):
        self.annalReplay.messageBoxId = None
        self.annalReplay.promptTimerId = 0

    def _clearAnnalEntities(self):
        if hasattr(BigWorld, 'clearServerAnnalEntities'):
            BigWorld.clearServerAnnalEntities()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FIGHT_OBSERVE_MONSTER_BLOOD)

    def onGetAnnalChatData(self, data):
        annalChatType, infoList = data
        if annalChatType == gametypes.ANNAL_CHAT_TYPE_WING_XINMO:
            for channel, msg, gbId, name, fromHostId in infoList:
                gameglobal.rds.ui.chat.addMessage(channel, msg, name)
