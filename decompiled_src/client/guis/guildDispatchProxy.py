#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildDispatchProxy.o
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
from data import guild_status_stype_data as GSSD
SORT_TYPE_RATE = 1

def sort_by_rate(a, b):
    if a['rate'] == b['rate']:
        return a['jobId'] - b['jobId']
    return b['rate'] - a['rate']


SORT_MAP = {SORT_TYPE_RATE: (sort_by_rate, True)}

class GuildDispatchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildDispatchProxy, self).__init__(uiAdapter)
        self.modelMap = {'getNormalInfo': self.onGetNormalInfo,
         'getAdvancedInfo': self.onGetAdvancedInfo,
         'dispatch': self.onDispatch,
         'setSort': self.onSetSort}
        self.mediator = None
        self.residentNUID = 0
        self.workType = gametypes.GUILD_JOB_DIFFICULTY_NORMAL
        self.sortType = SORT_TYPE_RATE
        self.ascendSorted = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_DISPATCH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_DISPATCH:
            self.mediator = mediator

    def show(self, residentNUID):
        self.residentNUID = residentNUID
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_DISPATCH)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_DISPATCH)

    def reset(self):
        self.residentNUID = 0
        self.workType = gametypes.GUILD_JOB_DIFFICULTY_NORMAL
        self.sortType = SORT_TYPE_RATE
        self.ascendSorted = False

    def hideByNUID(self, residentNUID):
        if self.residentNUID == residentNUID:
            self.hide()

    def refreshInfo(self, residentNUID = 0):
        if residentNUID and self.residentNUID != residentNUID:
            return
        if self.workType == gametypes.GUILD_JOB_DIFFICULTY_NORMAL:
            self.refreshNormalInfo()
        elif self.workType == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
            self.refreshAdvancedInfo()

    def onGetNormalInfo(self, *arg):
        self.refreshNormalInfo()

    def refreshNormalInfo(self):
        if self.mediator:
            self.workType = gametypes.GUILD_JOB_DIFFICULTY_NORMAL
            guild = BigWorld.player().guild
            resident = guild.hiredResident.get(self.residentNUID)
            if not resident:
                self.hide()
                return
            normalWork = []
            jobList = guild.getAvailJobList()
            for jobInfo in jobList:
                data = GJD.data.get(jobInfo[0], {})
                if data.get('difficulty', gametypes.GUILD_JOB_DIFFICULTY_NORMAL) != self.workType:
                    continue
                workInfo = {}
                workInfo['jobId'] = jobInfo[0]
                workInfo['content'] = data.get('name', '')
                workInfo['location'] = commGuild.getBuildNameByJobId(guild, jobInfo[0])
                propType = data.get('propType', 0)
                workInfo['propType'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % gametypes.GUILD_RESIDENT_PROP_NAME.get(propType, '')
                funcType = commGuild.getJobFuncType(guild, jobInfo[0])
                workInfo['rate'] = int(resident.getWorkEffect(propType, funcType) * 100)
                guildUtils.addSkillInfo(guild, resident.nuid, workInfo, jobInfo[0])
                workInfo['workNum'] = '%d/%d' % (jobInfo[2], jobInfo[1])
                normalWork.append(workInfo)

            normalWork.sort(cmp=SORT_MAP[self.sortType][0], reverse=SORT_MAP[self.sortType][1] if self.ascendSorted else not SORT_MAP[self.sortType][1])
            info = {}
            info['residentNUID'] = resident.nuid
            info['normalWork'] = normalWork
            info['sortType'] = self.sortType
            info['ascendSorted'] = self.ascendSorted
            self.mediator.Invoke('refreshNormalInfo', uiUtils.dict2GfxDict(info, True))

    def onGetAdvancedInfo(self, *arg):
        self.refreshAdvancedInfo()

    def refreshAdvancedInfo(self):
        if self.mediator:
            self.workType = gametypes.GUILD_JOB_DIFFICULTY_ADVANCED
            guild = BigWorld.player().guild
            resident = guild.hiredResident.get(self.residentNUID)
            if not resident:
                self.hide()
                return
            advancedWork = []
            jobList = guild.getAvailJobList()
            for jobInfo in jobList:
                data = GJD.data.get(jobInfo[0], {})
                if data.get('difficulty', gametypes.GUILD_JOB_DIFFICULTY_NORMAL) != self.workType:
                    continue
                workInfo = {}
                workInfo['jobId'] = jobInfo[0]
                workInfo['content'] = data.get('name', '')
                workInfo['location'] = commGuild.getBuildNameByJobId(guild, jobInfo[0])
                workInfo['propType'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % gametypes.GUILD_RESIDENT_PROP_NAME.get(data.get('propType', 0), '')
                guildUtils.addSkillInfo(guild, resident.nuid, workInfo, jobInfo[0])
                identity = ''
                statusStype = data.get('statusStype', ())
                for i in statusStype:
                    if identity != '':
                        identity += gameStrings.TEXT_ACTIVITYFACTORY_280
                    identity += GSSD.data.get(i, {}).get('name', '')

                workInfo['identity'] = identity if identity != '' else gameStrings.TEXT_BATTLEFIELDPROXY_1605
                workInfo['workNum'] = '%d/%d' % (jobInfo[2], jobInfo[1])
                advancedWork.append(workInfo)

            info = {}
            info['residentNUID'] = resident.nuid
            info['advancedWork'] = advancedWork
            self.mediator.Invoke('refreshAdvancedInfo', uiUtils.dict2GfxDict(info, True))

    def onDispatch(self, *arg):
        jobId = int(arg[3][0].GetNumber())
        guildUtils.dispatchCheck(self.residentNUID, jobId)

    def onSetSort(self, *arg):
        sortType = int(arg[3][0].GetString())
        ascendSorted = arg[3][1].GetBool()
        if self.sortType == sortType and self.ascendSorted == ascendSorted:
            return
        self.sortType = sortType
        self.ascendSorted = ascendSorted
        self.refreshNormalInfo()
