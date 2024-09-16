#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildTechResearchProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
import commGuild
import const
from uiProxy import UIProxy
from helpers import guild as guildUtils
from callbackHelper import Functor
from data import guild_scale_data as GSCD
from data import guild_building_data as GBD
from data import guild_technology_data as GTD
from data import guild_resident_pskill_data as GRPD
from cdata import game_msg_def_data as GMDD

class GuildTechResearchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildTechResearchProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'clickResident': self.onClickResident,
         'clickChange': self.onClickChange,
         'beginResearch': self.onBeginResearch,
         'cancelResearch': self.onCancelResearch}
        self.mediator = None
        self.techId = 0
        self.buildingId = 0
        self.markerId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_TECH_RESEARCH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_TECH_RESEARCH:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_TECH_RESEARCH)

    def reset(self):
        self.techId = 0
        self.buildingId = 0
        self.markerId = 0

    def show(self, techId):
        if not techId or not BigWorld.player().guild.technology.get(techId, None):
            return
        else:
            self.techId = techId
            self.buildingId = GTD.data.get(techId, {}).get('buildingId', 0)
            self.markerId = commGuild.getMarkerIdByBuildingId(BigWorld.player().guild, self.buildingId)
            if self.markerId == 0:
                BigWorld.player().showGameMsg(GMDD.data.GUILD_BUILDING_NOT_EXIST, (GBD.data.get(self.buildingId, {}).get('name'),))
                return
            if self.mediator:
                self.refreshInfo()
                self.mediator.Invoke('swapPanelToFront')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_TECH_RESEARCH)
            return

    def hideByTechId(self, techId):
        if self.mediator and self.techId == techId:
            self.hide()

    def refreshInfo(self, techId = 0):
        if techId != 0 and self.techId != techId:
            return
        else:
            enableWingWorldGuildRoleOptimization = gameglobal.rds.configData.get('enableWingWorldGuildRoleOptimization', False)
            if self.mediator:
                guild = BigWorld.player().guild
                techData = GTD.data.get(self.techId, {})
                info = {}
                info['techId'] = self.techId
                info['techName'] = techData.get('name', '')
                info['techDesc'] = techData.get('desc' if not enableWingWorldGuildRoleOptimization else 'desc2', '')
                info['iconPath'] = 'guildTech/64/%d.dds' % techData.get('icon', 0)
                enabledState = True
                info['cash'] = techData.get('bindCash', 0)
                info['cashHave'] = guild.bindCash
                if info['cash'] > info['cashHave']:
                    info['cashHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['cashHaveColor'] = '0xFFFFE7'
                scale = techData.get('scale', 0)
                scaleHave = guild.scale
                info['scale'] = GSCD.data.get(scale, {}).get('name', '')
                info['scaleHave'] = GSCD.data.get(scaleHave, {}).get('name', '')
                if scale > scaleHave:
                    info['scaleHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['scaleHaveColor'] = '0xFFFFE7'
                reqBuildingId = techData.get('reqBuildingId', 0)
                reqBuildingLevel = techData.get('reqBuildingLevel', 0)
                buildName = GBD.data.get(reqBuildingId, {}).get('name', '')
                marker = guild.marker.get(commGuild.getMarkerIdByBuildingId(guild, reqBuildingId), None)
                buildValue = guild.building.get(marker.buildingNUID, None) if marker else None
                ownLevel = buildValue.level if buildValue else 0
                info['building'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_310 % (buildName, reqBuildingLevel)
                info['buildingHave'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_310 % (buildName, ownLevel)
                if reqBuildingLevel > ownLevel:
                    info['buildingHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['buildingHaveColor'] = '0xFFFFE7'
                info['locationName'] = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_115 % GBD.data.get(self.buildingId, {}).get('name', '')
                info['baseSpeed'] = techData.get('speed', 0)
                info['propType'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % gametypes.GUILD_RESIDENT_PROP_NAME.get(techData.get('propType', 0), '')
                techVal = guild.technology.get(self.techId, None)
                progressMax = techData.get('progress', 0)
                currentValue = 100.0
                if progressMax >= techVal.progress:
                    currentValue = currentValue * techVal.progress / progressMax
                    info['progressBarText'] = '%s/%s' % (format(techVal.progress, ','), format(progressMax, ','))
                else:
                    info['progressBarText'] = '%s/%s' % (format(progressMax, ','), format(progressMax, ','))
                info['currentValue'] = currentValue
                info['progressMax'] = progressMax
                info['inResearching'] = techVal.inResearching()
                pskillId = techData.get('pskillId', 0)
                skillName = GRPD.data.get((pskillId, 1), {}).get('name', '')
                marker = guild.marker.get(self.markerId, None)
                manager = marker.getManager(guild) if marker else None
                if manager:
                    residentManager = guildUtils.createResidentInfo(guild, manager.nuid, size=const.GUILD_RESIDENT_SIZE96)
                    info['residentManager'] = residentManager
                    info['techEffect'] = '%d%%' % int(manager.getTechWorkEffect(guild, self.techId) * 100)
                    info['techSpeed'] = manager.getTechWorkload(guild, self.techId, ignoreTime=True)
                    leftTime = 0
                    if info['progressMax'] >= techVal.progress and info['techSpeed'] != 0:
                        leftTime = 3600 * (info['progressMax'] - techVal.progress) / info['techSpeed']
                    info['remainTime'] = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_143 % uiUtils.formatTime(leftTime)
                    if skillName != '':
                        if pskillId not in manager.pskills:
                            info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_130 % skillName
                            info['reqSkillColor'] = '0xF43804'
                            enabledState = False
                            info['techSpeed'] = 0
                            info['remainTime'] = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_151
                        else:
                            info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_167 % skillName
                            info['reqSkillColor'] = '0xFFFFE7'
                        info['lockVisible'] = True
                    else:
                        info['reqSkill'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                        info['reqSkillColor'] = '0xFFFFE7'
                        info['lockVisible'] = False
                else:
                    info['techEffect'] = '0%'
                    info['techSpeed'] = 0
                    info['remainTime'] = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_151
                    if skillName != '':
                        info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_130 % skillName
                        info['reqSkillColor'] = '0xF43804'
                        enabledState = False
                        info['lockVisible'] = True
                    else:
                        info['reqSkill'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                        info['reqSkillColor'] = '0xFFFFE7'
                        info['lockVisible'] = False
                info['enabledState'] = enabledState
                self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            return

    def onClose(self, *arg):
        self.hide()

    def onBeginResearch(self, *arg):
        BigWorld.player().cell.researchGuildTechnology(self.techId)

    def onCancelResearch(self, *arg):
        p = BigWorld.player()
        guild = p.guild
        techData = GTD.data.get(self.techId, {})
        if techData.get('bindCash', 0) + guild.bindCash > guild._getMaxBindCash():
            msg = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_190
        else:
            msg = gameStrings.TEXT_GUILDTECHRESEARCHPROXY_192
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.cancelResearchGuildTechnology, self.techId))

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
