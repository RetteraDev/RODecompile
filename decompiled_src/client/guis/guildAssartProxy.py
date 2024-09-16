#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAssartProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import commGuild
import gametypes
import const
from callbackHelper import Functor
from uiProxy import UIProxy
from helpers import guild as guildUtils
from data import guild_job_data as GJD
from data import guild_building_marker_data as GBMD
from cdata import game_msg_def_data as GMDD

class GuildAssartProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAssartProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'beginAssart': self.onBeginAssart,
         'cancelAssart': self.onCancelAssart,
         'clickResident': self.onClickResident,
         'clickChange': self.onClickChange}
        self.mediator = None
        self.markerId = 0
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ASSART, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ASSART:
            self.mediator = mediator
            self.setInitData()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ASSART)

    def show(self, markerId = 0, npcId = 0):
        self.markerId = markerId
        self.npcId = npcId
        if self.mediator:
            self.setInitData()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ASSART)

    def onClose(self, *arg):
        self.hide()

    def clearNpcId(self):
        self.npcId = 0

    def _getEntity(self):
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
            return e
        else:
            return BigWorld.player()

    def onBeginAssart(self, *arg):
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_BUILDING):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        e = self._getEntity()
        if e:
            e.cell.startGuildDev(self.markerId)

    def onCancelAssart(self, *arg):
        self.cancelAssarting(self.markerId)

    def cancelAssarting(self, markerId):
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_BUILDING):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        msg = gameStrings.TEXT_GUILDASSARTPROXY_80
        e = self._getEntity()
        if e:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(e.cell.cancelGuildDev, markerId))

    def setInitData(self):
        if self.mediator:
            p = BigWorld.player()
            baseData = GBMD.data.get(self.markerId, {})
            info = {}
            info['iconNow'] = 'guildBuildUpgrade/%d.dds' % baseData.get('iconNoDev', 100)
            info['iconNext'] = 'guildBuildUpgrade/%d.dds' % baseData.get('icon', 100)
            info['nameNext'] = baseData.get('name', '')
            info['descNext'] = baseData.get('desc', '')
            self.mediator.Invoke('setInitData', uiUtils.dict2GfxDict(info, True))
            marker = p.guild.marker.get(self.markerId)
            if marker and marker.inDev():
                self.setAssartProgress(self.markerId)
            else:
                self.setConditionData()

    def setConditionData(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            baseData = GBMD.data.get(self.markerId, {})
            info = {}
            enabledState = True
            level = GBMD.data.get(self.markerId, {}).get('glevel', 0)
            info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % level
            info['levelHave'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % guild.level
            if level > guild.level:
                info['levelHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['levelHaveColor'] = '0xFFFFE7'
            info['assartPoint'] = baseData.get('progress', 0)
            info['assartTitleTips'] = gameStrings.TEXT_GUILDASSARTPROXY_122
            info['enabledState'] = enabledState
            self.mediator.Invoke('setConditionData', uiUtils.dict2GfxDict(info, True))

    def setAssartProgress(self, markerId):
        if self.mediator and self.markerId == markerId:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            baseData = GBMD.data.get(self.markerId, {})
            info = {}
            progressMax = baseData.get('progress', 0)
            currentValue = 100.0
            if progressMax >= marker.progress:
                currentValue = currentValue * marker.progress / progressMax
                info['assartText'] = '%s/%s' % (format(marker.progress, ','), format(progressMax, ','))
            else:
                info['assartText'] = '%s/%s' % (format(progressMax, ','), format(progressMax, ','))
            info['currentValue'] = currentValue
            info['workLoad'] = gameStrings.TEXT_GUILDASSARTPROXY_145 % marker.getWorkload(guild, ignoreTime=True)
            jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_DEV)
            info['hintText'] = GJD.data.get(jobId, {}).get('hintText', '')
            manager = marker.getManager(guild, type=gametypes.GUILD_JOB_TYPE_DEV)
            if manager:
                residentManager = guildUtils.createResidentInfo(guild, manager.nuid, size=const.GUILD_RESIDENT_SIZE96)
                guildUtils.addManagerInfo(guild, manager.nuid, residentManager, jobId)
                info['residentManager'] = residentManager
            normalList = []
            for residentNUID in marker.workers:
                residentInfo = guildUtils.createResidentInfo(guild, residentNUID)
                normalList.append(residentInfo)

            info['normalList'] = normalList
            info['normalLimit'] = marker.getDevWorkerLimit()
            self.mediator.Invoke('setAssartProgress', uiUtils.dict2GfxDict(info, True))

    def assartFinish(self, markerId):
        if self.mediator and self.markerId == markerId:
            self.hide()

    def onClickResident(self, *arg):
        isEmpty = arg[3][0].GetBool()
        if isEmpty:
            difficulty = int(arg[3][1].GetNumber())
            jobId = commGuild.getJobIdFromGJRD(self.markerId, difficulty, gametypes.GUILD_JOB_TYPE_DEV)
            gameglobal.rds.ui.guildDispatchInto.show(jobId)
        else:
            residentNUID = int(arg[3][1].GetString())
            gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, residentNUID)

    def onClickChange(self, *arg):
        jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_DEV)
        gameglobal.rds.ui.guildDispatchInto.show(jobId)
