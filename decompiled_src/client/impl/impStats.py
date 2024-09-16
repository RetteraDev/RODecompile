#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impStats.o
import gameglobal
from data import client_trigger_limit_data as CTLD

class ImpStats(object):

    def statsTriggerAtClient(self, triggerName, triggerArgs):
        if not CTLD.data.has_key((triggerName, triggerArgs)):
            return
        ctld = CTLD.data[triggerName, triggerArgs]
        if ctld.has_key('quests'):
            for questId in ctld['quests']:
                if questId in self.quests:
                    break
            else:
                return

        if ctld.has_key('minLv') and self.lv < ctld['minLv']:
            return
        if ctld.has_key('maxLv') and self.lv > ctld['maxLv']:
            return
        self.cell.statsTriggerFromClient(triggerName, triggerArgs)

    def triggerQRCode(self, qrCodeId, realTriggerCnt):
        gameglobal.rds.ui.qrCodeShareAchievement.pushShareIcon(qrCodeId, realTriggerCnt)

    def finishQRCode(self, qrCodeId):
        gameglobal.rds.ui.qrCodeAppScanShare.shareFeedBack(True)
