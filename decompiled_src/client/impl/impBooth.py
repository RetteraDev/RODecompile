#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impBooth.o
import const
import gameglobal

class ImpBooth(object):

    def isBooth(self):
        return False

    def set_boothName(self, old):
        self.topLogo.setBoothName(self.boothName)
        if gameglobal.rds.ui.booth.otherBoothInfo:
            if gameglobal.rds.ui.booth.otherBoothInfo[0] == self.id:
                gameglobal.rds.ui.booth.setBoothName(self.boothName)

    def set_boothStat(self, old):
        if self.boothStat == const.BOOTH_STAT_OPEN:
            self.topLogo.setBoothVisible(True)
        elif self.boothStat == const.BOOTH_STAT_CLOSE:
            self.topLogo.setBoothVisible(False)
        self.switchBoothAspect()
        if old == const.BOOTH_STAT_OPEN and self.boothStat == const.BOOTH_STAT_CLOSE and gameglobal.rds.ui.booth.otherBoothInfo:
            if gameglobal.rds.ui.booth.otherBoothInfo[0] == self.id:
                gameglobal.rds.ui.booth.hide()

    def set_boothAspect(self, old):
        pass

    def boothSetup(self, info):
        pass

    def boothShutup(self):
        pass

    def boothOpen(self, b):
        pass

    def boothSemiData(self, ownerID, serial, itemInfo, buyItemsInfo):
        pass

    def boothFullData(self, ownerID, page, pos, item):
        pass

    def boothLog(self, log):
        pass

    def boothLogs(self, ownerID, info):
        pass

    def boothWord(self, ownerID, info):
        pass

    def boothWordIntervalShort(self, ownerID):
        pass

    def boothWordAndLogs(self, ownerID, info):
        pass

    def boothBuyItemCleared(self):
        pass

    def inBoothing(self):
        return self.boothStat == const.BOOTH_STAT_OPEN

    def onBoothSkinExTimeChange(self, boothSkinExTime, oldBoothSkinExTime):
        self.boothSkinExTime = boothSkinExTime
        gameglobal.rds.ui.booth.setOldBoothSkinExTime(oldBoothSkinExTime)

    def switchBoothAspect(self):
        if self.inBoothing():
            self.modelServer.enterBooth()
        else:
            self.modelServer.leaveBooth()
