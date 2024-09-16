#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildChallengeFieldProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import const
from uiProxy import UIProxy
from data import guild_challenge_data as GCHD

class GuildChallengeFieldProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildChallengeFieldProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.fbNo = 0
        self.timer = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CHALLENGE_FIELD:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CHALLENGE_FIELD)

    def reset(self):
        self.fbNo = 0
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_GUILD_CHALLENGE):
            if self.mediator:
                self.refreshInfo()
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CHALLENGE_FIELD)
            if gameglobal.rds.ui.guild.mediator:
                gameglobal.rds.ui.guild.hide()

    def enterChallengeBefore(self, fbNo):
        self.fbNo = fbNo
        self.show()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            info = {}
            maxScore = GCHD.data.get(self.fbNo, {}).get('initScore', 0)
            for key in guild.challengeScore:
                score = guild.challengeScore[key]
                if score < 0:
                    score = 0
                if key == p.guildNUID:
                    info['selfNum'] = gameStrings.TEXT_GUILDCHALLENGEFIELDPROXY_66 % score
                    selfCurrentValue = 100.0
                    if score < maxScore:
                        selfCurrentValue = selfCurrentValue * score / maxScore
                    info['selfCurrentValue'] = selfCurrentValue
                else:
                    info['enemyNum'] = gameStrings.TEXT_GUILDCHALLENGEFIELDPROXY_72 % score
                    enemyCurrentValue = 100.0
                    if score < maxScore:
                        enemyCurrentValue = enemyCurrentValue * score / maxScore
                    info['enemyCurrentValue'] = enemyCurrentValue

            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.guild:
                return
            challengeInfo = p.guild.challengeInfo
            fbValue = GCHD.data.get(self.fbNo, {})
            leftTime = int(challengeInfo.get('tOccupy', 0) + fbValue.get('readyTime', 0) + fbValue.get('durationTime', 0) - p.getServerTime())
            if leftTime < 0:
                return
            info = {}
            info['leftTime'] = leftTime
            info['useH'] = leftTime >= 3600
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            self.timer = BigWorld.callback(1, self.updateTime)
