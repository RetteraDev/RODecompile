#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildFactoryProxy.o
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
from callbackHelper import Functor
from data import guild_job_data as GJD
from data import guild_factory_product_data as GFPD
from data import guild_config_data as GCD
from data import guild_building_data as GBD
from data import guild_technology_data as GTD
from cdata import guild_factory_data as GFD

def sort_by_sortIdx(a, b):
    if a['sortIdx'] != b['sortIdx']:
        return a['sortIdx'] - b['sortIdx']
    return a['id'] - b['id']


def sort_by_tStart(a, b):
    return a['tStart'] - b['tStart']


def sort_resident(a, b):
    return a['isWorking'] - b['isWorking']


class GuildFactoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildFactoryProxy, self).__init__(uiAdapter)
        self.modelMap = {'getWorkInfo': self.onGetWorkInfo,
         'getResourceInfo': self.onGetResourceInfo,
         'fetch': self.onFetch,
         'product': self.onProduct,
         'cancelProduct': self.onCancelProduct,
         'cancelWaiting': self.onCancelWaiting,
         'donate': self.onDonate,
         'clickResident': self.onClickResident,
         'clickChange': self.onClickChange}
        self.mediator = None
        self.markerId = 0
        self.selectType = 0
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_FACTORY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_FACTORY:
            self.mediator = mediator

    def show(self, markerId):
        if not self.mediator:
            self.markerId = markerId
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_FACTORY)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_FACTORY)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.markerId = 0
        self.selectType = 0
        self.stopTimer()

    def refreshInfo(self):
        if self.selectType in gametypes.GUILD_FACTORY_TYPE:
            self.refreshWorkInfo(self.selectType)
        elif self.selectType == gametypes.GUILD_FACTORY_RESOURCE:
            self.refreshResourceInfo()

    def onGetWorkInfo(self, *arg):
        guild = BigWorld.player().guild
        marker = guild.marker.get(self.markerId)
        buildValue = guild.building.get(marker.buildingNUID)
        if buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
            self.selectType = gametypes.GUILD_FACTORY_PRODUCT_MACHINE
        elif buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
            self.selectType = gametypes.GUILD_FACTORY_PRODUCT_FACILITY
        else:
            return
        self.refreshWorkInfo(self.selectType)

    def refreshWorkInfo(self, selectType):
        if self.mediator and self.selectType == selectType:
            guild = BigWorld.player().guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            info = {}
            info['nameTitle'] = GBD.data.get(buildValue.buildingId, {}).get('name', '')
            buildLv = buildValue.level if buildValue else 0
            info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % buildLv
            info['managerField'] = gameStrings.TEXT_GUILDFACTORYPROXY_102 % info['nameTitle']
            info['authorization'] = gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_FACTORY)
            factory = guild._getFactory(selectType)
            factoryData = GFD.data.get(buildLv)
            reqList = []
            for productId, value in GFPD.data.iteritems():
                if value.get('type', 0) != selectType:
                    continue
                itemId = value.get('itemId', 0)
                if itemId == 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemInfo['productId'] = productId
                itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                ownNum = factory.product.get(productId, 0)
                itemInfo['itemNum'] = format(ownNum, ',')
                needLv = value.get('buildingLv', 0)
                itemInfo['lvReq'] = gameStrings.TEXT_GUILDFACTORYPROXY_122 % needLv if buildLv < needLv else ''
                techId = value.get('techId', 0)
                techVal = guild.technology.get(techId, None)
                if techVal and not techVal.isAvail():
                    itemInfo['techTips'] = gameStrings.TEXT_GUILDFACTORYPROXY_127 % GTD.data.get(techId, {}).get('name', '')
                else:
                    itemInfo['techTips'] = ''
                itemInfo['sortIdx'] = value.get('sortIdx', 0)
                reqList.append(itemInfo)

            reqList.sort(cmp=sort_by_sortIdx)
            info['reqList'] = reqList
            makingNum = 0
            makingList = []
            for taskVal in factory.task.itervalues():
                itemId = GFPD.data.get(taskVal.productId, {}).get('itemId', 0)
                if itemId == 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                info['itemInfo'] = itemInfo
                residentInfo = guildUtils.createResidentInfo(guild, taskVal.residentNUID)
                residentInfo['isWorking'] = False
                makinginfo = {}
                makinginfo['nuid'] = str(taskVal.nuid)
                makinginfo['itemInfo'] = itemInfo
                makinginfo['residentInfo'] = residentInfo
                makinginfo['tStart'] = taskVal.tStart
                makingNum += 1
                makingList.append(makinginfo)

            makingList.sort(cmp=sort_by_tStart)
            info['makingList'] = makingList
            info['makingNum'] = '%d/%d' % (makingNum, marker.getFuncWorkerCount(factoryData.get('jobIds')[selectType - 1]))
            waitingNum = 0
            waitingList = []
            for queueVal in factory.queue:
                itemId = GFPD.data.get(queueVal.productId, {}).get('itemId', 0)
                if itemId == 0:
                    continue
                itemInfo = {}
                itemInfo['itemId'] = itemId
                itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                itemInfo['nuid'] = str(queueVal.nuid)
                waitingNum += 1
                waitingList.append(itemInfo)

            info['waitingList'] = waitingList
            info['waitingNum'] = '%d/%d' % (waitingNum, factoryData.get('queueLen')[selectType - 1])
            jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_FUNC)
            info['hintText'] = GJD.data.get(jobId, {}).get('hintText', '')
            manager = marker.getManager(guild)
            if manager:
                residentManager = guildUtils.createResidentInfo(guild, manager.nuid, size=const.GUILD_RESIDENT_SIZE96)
                guildUtils.addManagerInfo(guild, manager.nuid, residentManager, jobId)
                info['residentManager'] = residentManager
            normalList = []
            normalWorkers = marker.getFuncWorkers()
            for residentNUID in normalWorkers:
                residentInfo = guildUtils.createResidentInfo(guild, residentNUID)
                normalList.append(residentInfo)

            normalList.sort(cmp=sort_resident)
            info['normalList'] = normalList
            info['normalLimit'] = marker.getFuncWorkerLimit(guild, gametypes.GUILD_JOB_DIFFICULTY_NORMAL)
            self.mediator.Invoke('refreshWorkInfo', uiUtils.dict2GfxDict(info, True))
            self.startTimer()

    def onGetResourceInfo(self, *arg):
        self.selectType = gametypes.GUILD_FACTORY_RESOURCE
        self.refreshResourceInfo()

    def refreshResourceInfo(self):
        if self.mediator and self.selectType == gametypes.GUILD_FACTORY_RESOURCE:
            guild = BigWorld.player().guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            info = {}
            info['nameTitle'] = GBD.data.get(buildValue.buildingId, {}).get('name', '')
            info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % (buildValue.level if buildValue else 0)
            info['titleField'] = gameStrings.TEXT_GUILDFACTORYPROXY_215 % info['nameTitle']
            otherRes = []
            maxOtherRes = guild._getMaxOtherRes()
            if buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
                otherResList = GCD.data.get('otherResMachineList', None)
            elif buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
                otherResList = GCD.data.get('otherResFacilityList', None)
            else:
                otherResList = None
            if otherResList:
                for itemId in otherResList:
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                    ownNum = guild.otherRes.get(itemId, 0)
                    itemInfo['itemNum'] = format(ownNum, ',')
                    itemInfo['numTips'] = '%s/%s' % (format(ownNum, ','), format(maxOtherRes, ','))
                    otherRes.append(itemInfo)

            info['otherRes'] = otherRes
            self.mediator.Invoke('refreshResourceInfo', uiUtils.dict2GfxDict(info, True))

    def onFetch(self, *arg):
        productId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildExtract.show(productId)

    def onProduct(self, *arg):
        productId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildProduce.show(self.markerId, productId)

    def onCancelProduct(self, *arg):
        taskNUID = int(arg[3][0].GetString())
        p = BigWorld.player()
        guild = p.guild
        factory = guild._getFactory(self.selectType)
        taskVal = factory.task.get(taskNUID)
        if not taskVal:
            return
        mojing, xirang, wood, bindCash, consumeItems = guild._unpackRes(taskVal.res)
        if bindCash + guild.bindCash > guild._getMaxBindCash() or mojing + guild.mojing > guild._getMaxMojing() or xirang + guild.xirang > guild._getMaxXirang() or wood + guild.wood > guild._getMaxWood():
            msg = gameStrings.TEXT_GUILDFACTORYPROXY_259
        else:
            msg = gameStrings.TEXT_GUILDFACTORYPROXY_261
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.cancelGuildFactoryTask, self.selectType, taskNUID))

    def onCancelWaiting(self, *arg):
        taskNUID = int(arg[3][0].GetString())
        p = BigWorld.player()
        guild = p.guild
        factory = guild._getFactory(self.selectType)
        taskVal = None
        for queueVal in factory.queue:
            if queueVal.nuid == taskNUID:
                taskVal = queueVal

        if not taskVal:
            return
        else:
            mojing, xirang, wood, bindCash, consumeItems = guild._unpackRes(taskVal.res)
            if bindCash + guild.bindCash > guild._getMaxBindCash() or mojing + guild.mojing > guild._getMaxMojing() or xirang + guild.xirang > guild._getMaxXirang() or wood + guild.wood > guild._getMaxWood():
                msg = gameStrings.TEXT_GUILDFACTORYPROXY_282
            else:
                msg = gameStrings.TEXT_GUILDFACTORYPROXY_284
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.cancelGuildFactoryQueue, self.selectType, taskNUID))
            return

    def onDonate(self, *arg):
        gameglobal.rds.ui.guildDonate.show()

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

    def startTimer(self):
        self.stopTimer()
        self.sendTimerInfo()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def sendTimerInfo(self):
        p = BigWorld.player()
        factory = p.guild._getFactory(self.selectType)
        if not factory or len(factory.task) == 0:
            return
        exist = False
        info = []
        for taskVal in factory.task.itervalues():
            leftTime = int(taskVal.tEnd - p.getServerTime())
            if leftTime <= 0:
                continue
            totalTime = taskVal.tEnd - taskVal.tStart
            currentValue = 100.0 * (totalTime - leftTime) / totalTime
            itemInfo = {}
            itemInfo['nuid'] = str(taskVal.nuid)
            itemInfo['currentValue'] = currentValue
            itemInfo['leftTimeText'] = uiUtils.formatTime(leftTime)
            info.append(itemInfo)
            exist = True

        if self.mediator and exist:
            self.mediator.Invoke('refreshTimerInfo', uiUtils.array2GfxAarry(info, True))
            self.timer = BigWorld.callback(1, self.sendTimerInfo)
