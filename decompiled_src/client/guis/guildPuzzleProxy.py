#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildPuzzleProxy.o
import BigWorld
import const
import gameglobal
import gametypes
import uiConst
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class GuildPuzzleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildPuzzleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.iconPushed = False
        self.reset()

    def reset(self):
        self.stopTimer()

    def initPanel(self, widget):
        self.widget = widget
        self.widget.visible = False
        self.show()

    def clearWidget(self):
        if not self.widget:
            return
        self.widget.visible = False
        gameglobal.rds.ui.chat.updateLabaPos()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_PUZZLE)

    def show(self):
        if not self.widget or self.widget.visible or not self.checkWidgetAvailable():
            return
        if not gameglobal.rds.configData.get('enableGuildPuzzle', False) or not BigWorld.player().guild:
            self.hide()
            return
        puzzleState = BigWorld.player().guild.getPuzzleState()
        if puzzleState in gametypes.GUILD_ACTIVITY_ACTIVE_STATE:
            if not self.iconPushed:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_PUZZLE)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_PUZZLE, {'click': self.onPushClick})
                self.iconPushed = True
            self.widget.visible = True
            self.refreshInfo()
            self.countDownTimer()
            gameglobal.rds.ui.chat.updateLabaPos()

    def onPushClick(self):
        p = BigWorld.player()
        guildPuzzleMsg = SCD.data.get('guildPuzzlePushMsg', {})
        if p.guild.getPuzzleState() == gametypes.GUILD_ACTIVITY_PREPARE:
            msg = guildPuzzleMsg.get('prepare', '')
        else:
            msg = guildPuzzleMsg.get('going', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onClickJoin, yesBtnText=guildPuzzleMsg.get('yesBtn', ''), noBtnText=guildPuzzleMsg.get('noBtn', ''))

    def onClickJoin(self):
        gameglobal.rds.ui.chat.showView()
        gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_GUILD)
        gameglobal.rds.ui.chat.openInput()

    def refreshInfo(self):
        if not self.widget or not self.widget.visible or not self.checkWidgetAvailable():
            return
        p = BigWorld.player()
        puzzleState = p.guild.getPuzzleState()
        roundNum = p.guild.getPuzzleRoundNum()
        leftTime = p.guild.getPuzzleLeftTime()
        if roundNum and leftTime:
            guildPuzzleMsg = SCD.data.get('guildPuzzleMsg', {})
            if puzzleState == gametypes.GUILD_ACTIVITY_PREPARE:
                self.widget.puzzleInfoText.htmlText = guildPuzzleMsg.get('prepare', '%d') % roundNum
            elif puzzleState == gametypes.GUILD_ACTIVITY_GOING:
                puzzleDesc = p.guild.getPuzzleDesc()
                if puzzleDesc:
                    self.widget.puzzleInfoText.htmlText = guildPuzzleMsg.get('question', '%d%s') % (roundNum, puzzleDesc)
            elif puzzleState == gametypes.GUILD_ACTIVITY_RESULT:
                puzzleAnswer = p.guild.getPuzzleAnswer()
                if puzzleAnswer:
                    self.widget.puzzleInfoText.htmlText += guildPuzzleMsg.get('answer', '%s') % puzzleAnswer
            elif puzzleState == gametypes.GUILD_ACTIVITY_RESULT_MORE:
                puzzleTextTops = p.guild.getPuzzleTops(False)
                puzzleVoiceTops = p.guild.getPuzzleTops(True)
                winnerText = ''
                if puzzleVoiceTops:
                    winners = ','.join(puzzleVoiceTops)
                    winnerText += guildPuzzleMsg.get('voiceWinners', '%s') % winners
                    p.showGameMsg(GMDD.data.GUILD_PUZZLE_TOP_VOICE_WINNERS, (winners,))
                if puzzleTextTops:
                    winners = ','.join(puzzleTextTops)
                    winnerText += guildPuzzleMsg.get('textWinners', '%s') % winners
                    p.showGameMsg(GMDD.data.GUILD_PUZZLE_TOP_TEXT_WINNERS, (winners,))
                if not winnerText:
                    winnerText = guildPuzzleMsg.get('noWinners', '')
                self.widget.puzzleInfoText.htmlText = winnerText
            self.widget.progressBar.maxValue = leftTime

    def countDownTimer(self):
        self.stopTimer()
        if not self.widget or not self.widget.visible or not self.checkWidgetAvailable():
            return
        guild = BigWorld.player().guild
        if not guild:
            self.hide()
            return
        leftTime = guild.getPuzzleLeftTime()
        self.widget.progressBar.currentValue = leftTime
        self.widget.countDownText.text = '%ds ' % leftTime
        self.timer = BigWorld.callback(1, self.countDownTimer)

    def checkWidgetAvailable(self):
        if not self.uiAdapter.isWidgetLoaded(uiConst.WIDGET_CHAT_LOG):
            self.widget = None
            return False
        else:
            return True

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
