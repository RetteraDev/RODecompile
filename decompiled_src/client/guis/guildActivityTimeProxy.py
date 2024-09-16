#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildActivityTimeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import commGuild
import gametypes
import const
from uiProxy import UIProxy

class GuildActivityTimeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildActivityTimeProxy, self).__init__(uiAdapter)
        self.modelMap = {'showActivity': self.onShowActivity}
        self.mediator = None
        self.timer = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ACTIVITY_TIME:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ACTIVITY_TIME)

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self):
        guild = BigWorld.player().guild
        if not guild or not guild.memberMe.inMatch:
            return
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ACTIVITY_TIME)

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild or not guild.memberMe.inMatch:
                return
            info = {}
            titleField = gameStrings.TEXT_GUILDACTIVITYTIMEPROXY_55
            headVisible = False
            if not guild.memberMe.matched:
                if guild.memberMe.matchGbId:
                    titleField = gameglobal.rds.ui.guildActivity.getMyMatchName()
                    headVisible = True
                else:
                    titleField = gameStrings.TEXT_GUILDACTIVITYPROXY_103
                    headVisible = False
            info['titleField'] = titleField
            info['headVisible'] = headVisible
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.guild:
                return
            nowRound = gameglobal.rds.ui.guildActivity.getActivitySate()
            if nowRound <= 0:
                return
            leftTime = p.guild.tMatchRoundEnd - int(p.getServerTime())
            if leftTime < 0:
                return
            if gameglobal.rds.configData.get('enableGuildMatchOptimize', False):
                totalRound = const.GUILD_MATCH_MAX_ROUND_OPTIMIZE
            else:
                totalRound = const.GUILD_MATCH_MAX_ROUND
            info = {'round': gameStrings.TEXT_GUILDACTIVITYTIMEPROXY_91 % (nowRound, totalRound),
             'leftTime': leftTime}
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            self.timer = BigWorld.callback(1, self.updateTime)

    def onShowActivity(self, *arg):
        gameglobal.rds.ui.guild.openGuildBuilding(commGuild.getMarkerIdByBuildingId(BigWorld.player().guild, gametypes.GUILD_BUILDING_ACTIVITY_ID))
