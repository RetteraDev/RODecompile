#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResidentRecProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import commGuild
from uiProxy import UIProxy
from helpers import guild as guildUtils
from data import guild_resident_template_data as GRTD
SORT_TYPE_NAME = 1
SORT_TYPE_LEVEL = 2
SORT_TYPE_STATUS = 3
SORT_TYPE_SALARY = 4
SORT_TYPE_HIREFEE = 5

def sort_by_name(a, b):
    return b['quality'] - a['quality']


def sort_by_level(a, b):
    return b['level'] - a['level']


def sort_by_status(a, b):
    return b['statusTypeIdx'] - a['statusTypeIdx']


def sort_by_salary(a, b):
    return a['salary'] - b['salary']


def sort_by_hirefee(a, b):
    return a['hireFee'] - b['hireFee']


SORT_MAP = {SORT_TYPE_NAME: (sort_by_name, True),
 SORT_TYPE_LEVEL: (sort_by_level, True),
 SORT_TYPE_STATUS: (sort_by_status, True),
 SORT_TYPE_SALARY: (sort_by_salary, False),
 SORT_TYPE_HIREFEE: (sort_by_hirefee, False)}

class GuildResidentRecProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildResidentRecProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'setSort': self.onSetSort,
         'view': self.onView,
         'hire': self.onHire,
         'leave': self.onLeave}
        self.mediator = None
        self.sortType = SORT_TYPE_STATUS
        self.ascendSorted = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESIDENT_RECOMMEND, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RESIDENT_RECOMMEND:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RESIDENT_RECOMMEND)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RESIDENT_RECOMMEND)
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
            for key in guild.recommendedResident:
                resident = guild.recommendedResident[key]
                baseInfo = GRTD.data.get(resident.templateId, {})
                itemInfo = {}
                itemInfo['residentName'] = resident.name
                itemInfo['level'] = resident.level
                residentInfo = {}
                residentInfo['residentNUID'] = str(resident.nuid)
                residentInfo['iconPath'] = guildUtils.getPhotoPath40(baseInfo.get('icon', 0))
                residentInfo['statusStype'] = guildUtils.getStatusStypePath20(resident.statusStype)
                itemInfo['quality'], residentInfo['qualitycolor'] = guildUtils.getResidentQuality(resident.templateId)
                residentInfo['statusField'] = guildUtils.getStatusField(resident.statusType, resident.statusStype, False)
                residentInfo['tiredLv'] = 'lv%d' % commGuild.getTiredType(resident.tired)
                residentInfo['tiredValue'] = resident.tired
                residentInfo['isWorking'] = resident.subJobId != 0
                itemInfo['residentInfo'] = residentInfo
                itemInfo['shortStatus'] = guildUtils.getStatusField(resident.statusType, resident.statusStype, True)
                itemInfo['statusTypeIdx'] = resident.statusType * 1000 + resident.statusStype
                recommender = guild.member.get(resident.recommender)
                itemInfo['playerName'] = recommender.role if recommender else ''
                itemInfo['salary'] = resident.salary
                itemInfo['hireFee'] = baseInfo.get('employFee', 0)
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
        gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_RECOMMENDED, residentNUID=residentNUID)

    def onHire(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.hireGuildResident(residentNUID)

    def onLeave(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.rejectGuildResident(residentNUID)
