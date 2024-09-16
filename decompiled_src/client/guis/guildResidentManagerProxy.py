#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResidentManagerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import commGuild
import const
from uiProxy import UIProxy
from helpers import guild as guildUtils
from data import guild_job_data as GJD
from data import guild_building_data as GBD

class GuildResidentManagerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildResidentManagerProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickResident': self.onClickResident,
         'clickChange': self.onClickChange}
        self.mediator = None
        self.markerId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESIDENT_MANAGER, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RESIDENT_MANAGER:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, markerId, needHideAllGuildBuilding = False):
        if needHideAllGuildBuilding:
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
        self.markerId = markerId
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RESIDENT_MANAGER, layoutType=uiConst.LAYOUT_NPC_FUNC)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RESIDENT_MANAGER)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.markerId = 0

    def hideByMarkerId(self, markerId):
        if self.mediator and self.markerId == markerId:
            self.hide()

    def showOrHide(self, markerId):
        if self.markerId == markerId:
            if self.mediator:
                self.hide()
        else:
            self.show(markerId)

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            info = {}
            info['nameTitle'] = gameStrings.TEXT_GUILDFACTORYPROXY_102 % GBD.data.get(buildValue.buildingId, {}).get('name', '')
            jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_FUNC)
            info['hintText'] = GJD.data.get(jobId, {}).get('hintText', '')
            manager = marker.getManager(guild)
            if manager:
                residentManager = guildUtils.createResidentInfo(guild, manager.nuid, size=const.GUILD_RESIDENT_SIZE96)
                guildUtils.addManagerInfo(guild, manager.nuid, residentManager, jobId)
                info['residentManager'] = residentManager
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onClickResident(self, *arg):
        isEmpty = arg[3][0].GetBool()
        if isEmpty:
            difficulty = int(arg[3][1].GetNumber())
            jobId = commGuild.getJobIdFromGJRD(self.markerId, difficulty, gametypes.GUILD_JOB_TYPE_FUNC)
            gameglobal.rds.ui.guildDispatchInto.show(jobId)
        else:
            residentNUID = int(arg[3][1].GetString())
            gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, residentNUID)

    def onClickChange(self, *arg):
        jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_FUNC)
        gameglobal.rds.ui.guildDispatchInto.show(jobId)
