#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResidentHiredProxy.o
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
SORT_TYPE_NAME = 1
SORT_TYPE_LEVEL = 2
SORT_TYPE_LOCATION = 3
SORT_TYPE_STATUS = 4
SORT_TYPE_PROPTYPE = 5

def sort_by_name(a, b):
    return b['residentInfo']['quality'] - a['residentInfo']['quality']


def sort_by_level(a, b):
    return b['level'] - a['level']


def sort_by_location(a, b):
    return a['jobId'] - b['jobId']


def sort_by_status(a, b):
    return b['statusTypeIdx'] - a['statusTypeIdx']


def sort_by_propType(a, b):
    return a['propTypeIdx'] - b['propTypeIdx']


SORT_MAP = {SORT_TYPE_NAME: (sort_by_name, True),
 SORT_TYPE_LEVEL: (sort_by_level, True),
 SORT_TYPE_LOCATION: (sort_by_location, False),
 SORT_TYPE_STATUS: (sort_by_status, True),
 SORT_TYPE_PROPTYPE: (sort_by_propType, False)}

class GuildResidentHiredProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildResidentHiredProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'setSort': self.onSetSort,
         'view': self.onView,
         'dispatch': self.onDispatch,
         'rest': self.onRest}
        self.mediator = None
        self.sortType = SORT_TYPE_STATUS
        self.ascendSorted = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESIDENT_HIRED, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RESIDENT_HIRED:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RESIDENT_HIRED)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RESIDENT_HIRED)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.sortType = SORT_TYPE_STATUS
        self.ascendSorted = False

    def onGetInfo(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            residentList = []
            for key in guild.hiredResident:
                resident = guild.hiredResident[key]
                itemInfo = {}
                itemInfo['residentName'] = resident.name
                itemInfo['level'] = resident.level
                itemInfo['residentInfo'] = guildUtils.createResidentInfo(guild, resident.nuid)
                itemInfo['shortStatus'] = guildUtils.getStatusField(resident.statusType, resident.statusStype, True)
                itemInfo['statusTypeIdx'] = resident.statusType * 1000 + resident.statusStype
                jobData = GJD.data.get(resident.jobId, {})
                if resident.jobId:
                    itemInfo['location'] = '%s-%s' % (commGuild.getBuildNameByJobId(guild, resident.jobId), jobData.get('name', ''))
                else:
                    itemInfo['location'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_102
                itemInfo['jobId'] = resident.jobId
                itemInfo['propTypeIdx'] = resident.getPropType()
                itemInfo['propType'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % gametypes.GUILD_RESIDENT_PROP_NAME.get(itemInfo['propTypeIdx'], '')
                itemInfo['canLvUp'] = resident.canLvUp()
                residentList.append(itemInfo)

            residentList.sort(cmp=SORT_MAP[self.sortType][0], reverse=SORT_MAP[self.sortType][1] if self.ascendSorted else not SORT_MAP[self.sortType][1])
            info['residentList'] = residentList
            info['sortType'] = self.sortType
            info['ascendSorted'] = self.ascendSorted
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onSetSort(self, *arg):
        if self.sortType == int(arg[3][0].GetString()) and self.ascendSorted == arg[3][1].GetBool():
            return
        self.sortType = int(arg[3][0].GetString())
        self.ascendSorted = arg[3][1].GetBool()
        self.refreshInfo()

    def onView(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, residentNUID=residentNUID)

    def onDispatch(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildDispatch.show(residentNUID)

    def onRest(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        guildUtils.stopWorkCheck(residentNUID)
