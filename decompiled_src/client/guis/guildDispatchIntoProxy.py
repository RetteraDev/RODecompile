#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildDispatchIntoProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
import commGuild
from uiProxy import UIProxy
from helpers import guild as guildUtils
from data import guild_job_data as GJD

def sort_by_jobIdIdx(a, b):
    if a['jobIdIdx'] == b['jobIdIdx']:
        return b['rate'] - a['rate']
    return a['jobIdIdx'] - b['jobIdIdx']


class GuildDispatchIntoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildDispatchIntoProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'view': self.onView,
         'dispatchInto': self.onDispatchInto,
         'filter': self.onFilter,
         'changeOnlyFree': self.onChangeOnlyFree}
        self.mediator = None
        self.jobId = 0
        self.propTypeFlag = {gametypes.GUILD_RESIDENT_PROP_POW: True,
         gametypes.GUILD_RESIDENT_PROP_AGI: True,
         gametypes.GUILD_RESIDENT_PROP_INT: True,
         gametypes.GUILD_RESIDENT_PROP_SPR: True}
        self.onlyFreeFlag = True
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_DISPATCH_INTO, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_DISPATCH_INTO:
            self.mediator = mediator

    def show(self, jobId):
        if not GJD.data.has_key(jobId):
            return
        self.jobId = jobId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_DISPATCH_INTO)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_DISPATCH_INTO)

    def reset(self):
        self.jobId = 0
        self.propTypeFlag = {gametypes.GUILD_RESIDENT_PROP_POW: True,
         gametypes.GUILD_RESIDENT_PROP_AGI: True,
         gametypes.GUILD_RESIDENT_PROP_INT: True,
         gametypes.GUILD_RESIDENT_PROP_SPR: True}
        self.onlyFreeFlag = True
        gameglobal.rds.ui.guildResident.hideByPanelType(uiConst.GUILD_RESIDENT_PANEL_DISPATCH)

    def onGetInfo(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            jobInfo = GJD.data.get(self.jobId, {})
            info = {}
            info['locationField'] = '%s-%s' % (commGuild.getBuildNameByJobId(guild, self.jobId), jobInfo.get('name', ''))
            info['propTypeField'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % gametypes.GUILD_RESIDENT_PROP_NAME.get(jobInfo.get('propType', 0), '')
            residentList = []
            for key in guild.hiredResident:
                resident = guild.hiredResident[key]
                if self.onlyFreeFlag and resident.jobId:
                    continue
                if not self.propTypeFlag.get(resident.getPropType(), False):
                    continue
                itemInfo = {}
                itemInfo['residentName'] = resident.name
                itemInfo['level'] = resident.level
                itemInfo['residentInfo'] = guildUtils.createResidentInfo(guild, resident.nuid)
                itemInfo['shortStatus'] = guildUtils.getStatusField(resident.statusType, resident.statusStype, True)
                jobData = GJD.data.get(resident.jobId, {})
                if resident.jobId:
                    itemInfo['location'] = '%s-%s' % (commGuild.getBuildNameByJobId(guild, resident.jobId), jobData.get('name', ''))
                else:
                    itemInfo['location'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_102
                funcType = commGuild.getJobFuncType(guild, self.jobId)
                itemInfo['rate'] = int(resident.getWorkEffect(jobInfo.get('propType', 0), funcType) * 100)
                guildUtils.addSkillInfo(guild, resident.nuid, itemInfo, self.jobId)
                itemInfo['jobIdIdx'] = 1 if resident.jobId else 0
                residentList.append(itemInfo)

            residentList.sort(cmp=sort_by_jobIdIdx)
            info['residentList'] = residentList
            info['propTypeFlag'] = self.propTypeFlag
            needPropHint = False
            for i in gametypes.GUILD_RESIDENT_PROP:
                if self.propTypeFlag[i] == False:
                    needPropHint = True
                    break

            info['onlyFreeFlag'] = self.onlyFreeFlag
            if self.onlyFreeFlag:
                info['hint'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_127 % (gameStrings.TEXT_GUILDDISPATCHINTOPROXY_127_1 if needPropHint else '')
            else:
                info['hint'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_129 % (gameStrings.TEXT_GUILDDISPATCHINTOPROXY_127_1 if needPropHint else '')
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onView(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_DISPATCH, residentNUID=residentNUID)

    def onDispatchInto(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        guildUtils.dispatchCheck(residentNUID, self.jobId)

    def onFilter(self, *arg):
        propTypeIdx = int(arg[3][0].GetNumber())
        propTypeFlag = arg[3][1].GetBool()
        if self.propTypeFlag[propTypeIdx] == propTypeFlag:
            return
        self.propTypeFlag[propTypeIdx] = propTypeFlag
        self.refreshInfo()

    def onChangeOnlyFree(self, *arg):
        onlyFreeFlag = arg[3][0].GetBool()
        if self.onlyFreeFlag == onlyFreeFlag:
            return
        self.onlyFreeFlag = onlyFreeFlag
        self.refreshInfo()
