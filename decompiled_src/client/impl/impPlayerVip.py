#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerVip.o
import zlib
import cPickle
import utils
import gameglobal
import gametypes
import gamelog
from guis import events
from data import vip_service_data as VSD

class ImpPlayerVip(object):

    def onGetVipAward(self, serviceID, tExpire, tAward, isAll = False):
        for i in range(len(self.vipDailyBonus)):
            if serviceID == self.vipDailyBonus[i][0]:
                self.vipDailyBonus.insert(i, (serviceID, tExpire, tAward))
                del self.vipDailyBonus[i + 1]

        for i in range(len(self.vipWeeklyBonus)):
            if serviceID == self.vipWeeklyBonus[i][0]:
                self.vipWeeklyBonus.insert(i, (serviceID, tExpire, tAward))
                del self.vipWeeklyBonus[i + 1]

        if not isAll:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_INFO_UPDATE)

    def onGetAllVipAward(self, serviceInfo):
        for serviceID, tExpire, tAward in serviceInfo:
            self.onGetVipAward(serviceID, tExpire, tAward, isAll=True)

        gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_INFO_UPDATE)

    def sendVipInfo(self, res):
        info = cPickle.loads(zlib.decompress(res))
        self.vipWeeklyBonus = info.get('weeklyBonus', [])
        self.vipDailyBonus = info.get('dailyBonus', [])
        self.vipBasicPackage = info.get('basicPackage', {})
        self.vipAddedPackage = info.get('addedPackages', {})
        self.vipValidCnt = info.get('validCnt', [])
        self.vipCompensateCnt = info.get('availableCompensateCnt', 0)
        self.basicPackageBuyRecord = info.get('basicPackageBuyRecord', None)
        self.resetClientCheckService()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_INFO_UPDATE)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_PACKAGEINFO_UPDATE)
        gameglobal.rds.ui.diGongDetail.refreshDigongDetail()

    def updateVipCnt(self, serviceID, cnt):
        for x in xrange(0, len(self.vipValidCnt)):
            if serviceID == self.vipValidCnt[x][0]:
                self.vipValidCnt[x] = (serviceID, cnt)

    def resetClientCheckService(self):
        self.vipClientCheckServices = {}
        if self.vipBasicPackage:
            for serviceID, tExpire in self.vipBasicPackage.get('services'):
                propID = VSD.data.get(serviceID, {}).get('propID')
                if propID not in gametypes.VIP_SERVICE_CLIENT_COMPONENT:
                    continue
                self.vipClientCheckServices[serviceID] = max(self.vipClientCheckServices.get(serviceID, 0), tExpire)
                if propID not in self.vipClientCheckProps:
                    self.vipClientCheckProps[propID] = []
                if serviceID not in self.vipClientCheckProps[propID]:
                    self.vipClientCheckProps[propID].append(serviceID)

        if self.vipAddedPackage:
            for _, pVal in self.vipAddedPackage.iteritems():
                for serviceID, tExpire in pVal.get('services'):
                    propID = VSD.data.get(serviceID, {}).get('propID')
                    if propID not in gametypes.VIP_SERVICE_CLIENT_COMPONENT:
                        continue
                    self.vipClientCheckServices[serviceID] = max(self.vipClientCheckServices.get(serviceID, 0), tExpire)
                    if propID not in self.vipClientCheckProps:
                        self.vipClientCheckProps[propID] = []
                    if serviceID not in self.vipClientCheckProps[propID]:
                        self.vipClientCheckProps[propID].append(serviceID)

    def isValidService(self, serviceID, now):
        if serviceID not in VSD.data:
            return False
        if VSD.data[serviceID].get('invalid', False):
            return False
        return self.vipClientCheckServices[serviceID] > now

    def vipRevise(self, propID, val, getMax = True):
        if not self.vipClientCheckProps or propID not in self.vipClientCheckProps:
            return val
        now = utils.getNow()
        serviceIDs = self.vipClientCheckProps[propID]
        tmpVals = []
        for serviceID in serviceIDs:
            if serviceID not in self.vipClientCheckServices:
                continue
            if not self.isValidService(serviceID, now):
                continue
            vsd = VSD.data.get(serviceID)
            serviceType = vsd.get('serviceType')
            if serviceType != gametypes.VIP_SERVICE_TYPE_PROP_CALC:
                continue
            calcType = vsd.get('calcType')
            calcArg = vsd.get('calcArg')
            if calcType == gametypes.VIP_CALC_TYPE_ADD:
                tmpVals.append(val + calcArg)
            elif calcType == gametypes.VIP_CALC_TYPE_SUB:
                tmpVals.append(val - calcArg)
            elif calcType == gametypes.VIP_CALC_TYPE_SET:
                tmpVals.append(calcArg)
            elif calcType == gametypes.VIP_CALC_TYPE_MULTI:
                tmpVals.append(val * calcArg)

        if tmpVals:
            val = max(tmpVals) if getMax else min(tmpVals)
        return val

    def onBuyVipService(self, mIds, succ):
        if succ:
            gameglobal.rds.ui.tianyuMall.onVipPackageConfirmBuySuccess(mIds[0])

    def onGetVipCompensate(self, dayCnt, succ):
        print 'onGetVipCompensate', dayCnt, succ

    def refreshVipInfo(self, resetDailyServices, resetWeeklyServices, expiredServices):
        if resetDailyServices is None:
            resetDailyServices = []
        if resetWeeklyServices is None:
            resetWeeklyServices = []
        for i in range(len(self.vipDailyBonus)):
            serviceID = self.vipDailyBonus[i][0]
            tExpire = self.vipDailyBonus[i][1]
            if serviceID in resetDailyServices:
                self.vipDailyBonus.insert(i, (serviceID, tExpire, 0))
                del self.vipDailyBonus[i + 1]

        for i in range(len(self.vipWeeklyBonus)):
            serviceID = self.vipWeeklyBonus[i][0]
            tExpire = self.vipWeeklyBonus[i][1]
            if serviceID in resetWeeklyServices:
                self.vipWeeklyBonus.insert(i, (serviceID, tExpire, 0))
                del self.vipWeeklyBonus[i + 1]

        if not expiredServices:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_INFO_UPDATE)
            gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_PACKAGEINFO_UPDATE)
            return
        else:
            services = self.vipBasicPackage.get('services', [])
            leftServices = []
            svcLen = len(services)
            for i in range(svcLen):
                if services[i][0] not in expiredServices:
                    leftServices.append(services[i])

            self.vipBasicPackage['services'] = leftServices
            for key in self.vipAddedPackage:
                services = self.vipAddedPackage.get(key, {}).get('services', [])
                leftServices = []
                svcLen = len(services)
                for i in range(svcLen):
                    if services[i][0] not in expiredServices:
                        leftServices.append(services[i])

                self.vipAddedPackage[key]['services'] = leftServices

            gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_INFO_UPDATE)
            gameglobal.rds.ui.dispatchEvent(events.EVENT_VIP_PACKAGEINFO_UPDATE)
            return

    def isValidVipProp(self, propID):
        if not self.vipClientCheckProps or propID not in self.vipClientCheckProps:
            return False
        now = utils.getNow()
        serviceIDs = self.vipClientCheckProps[propID]
        for serviceID in serviceIDs:
            if serviceID not in self.vipClientCheckServices:
                continue
            if not self.isValidService(serviceID, now):
                continue
            return True

        return False

    def getVipPropLeftTime(self, propId):
        if not self.vipClientCheckProps or propId not in self.vipClientCheckProps:
            return 0
        now = utils.getNow()
        serviceTime = 0
        serviceIDs = self.vipClientCheckProps[propId]
        for serviceID in serviceIDs:
            if serviceID not in self.vipClientCheckServices:
                continue
            if not self.isValidService(serviceID, now):
                continue
            if serviceTime < self.vipClientCheckServices[serviceID]:
                serviceTime = self.vipClientCheckServices[serviceID]

        if serviceTime:
            return serviceTime - now
        else:
            return 0

    def isValidVip(self):
        return self.vipBasicPackage.get('tExpire', 0) - utils.getNow()

    def onQueryVipIsSameCompensate(self, isSame):
        gamelog.debug('@zhangkuo onQueryVipIsSameCompensate', isSame)
        self.vipSameCompensate = isSame

    def isVipSameCompensate(self):
        if hasattr(self, 'vipSameCompensate'):
            return self.vipSameCompensate
        return True
