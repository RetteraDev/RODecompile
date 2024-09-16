#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/welfareNewServerProxy.o
import BigWorld
import gameglobal
import uiUtils
import utils
import const
from uiProxy import UIProxy
from data import open_server_bonus_data as OSBD
from data import sys_config_data as SCD
from cdata import open_server_bonus_vp_data as OSBVD
from data import vp_level_data as VLD

class WelfareNewServerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareNewServerProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'gainReward': self.onGainReward,
         'refreshFrame': self.onRefreshFrame}
        self.panelMC = None
        self.bonusTip = {}

    def onRegisterMc(self, *arg):
        self.panelMC = arg[3][0]
        self.refreshInfo()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def onRefreshFrame(self, *args):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.panelMC:
            return
        frameInfo = self.getFrameInfo()
        self.panelMC.Invoke('refreshFrame', uiUtils.dict2GfxDict(frameInfo, True))

    def getFrameInfo(self):
        p = BigWorld.player()
        serverData = p.openServerBonus if p.openServerBonus else {}
        frameInfo = {}
        serverOpendDay = utils.getServerOpenDays() + 1
        frameInfo['passedDay'] = SCD.data.get('openServerBonusDesc', '活动已进行到第%d天') % min(30, serverOpendDay)
        frameInfo['remainTime'] = utils.getServerOpenTime() + const.TIME_INTERVAL_MONTH - const.TIME_INTERVAL_DAY - utils.getNow()
        itemList = []
        hasReward = False
        for key, value in OSBD.data.iteritems():
            itemInfo = {}
            itemInfo['day'] = key
            tips = value.get('text', '奖励tips')
            self.bonusTip[key] = tips
            if serverData.has_key(key):
                state = serverData[key].state
                if state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                    itemInfo['state'] = 'wait'
                elif state == const.OPEN_SERVER_BONUS_STATE_READY:
                    itemInfo['state'] = 'ready'
                    hasReward = True
                else:
                    itemInfo['state'] = 'gained'
            else:
                itemInfo['state'] = 'wait'
            if key <= serverOpendDay:
                fixedItemId = self._getBonusItemId(key)
                tips = self._getNewServerBonusTip(key)
                tips = self._getNewServerBonusTip(key)
                itemInfo['tips'] = tips
                if fixedItemId != 0:
                    itemInfo['item'] = uiUtils.getGfxItemById(fixedItemId)
                else:
                    itemInfo['item'] = uiUtils.getGfxItemById(value.get('itemId', 0))
            else:
                itemInfo['item'] = uiUtils.getGfxItemById(value.get('itemId', 0))
                itemInfo['tips'] = tips
            itemList.append(itemInfo)

        frameInfo['itemList'] = itemList
        frameInfo['hasReward'] = hasReward
        return frameInfo

    def _getNewServerBonusTip(self, day):
        vpLv = self._getVpLv(day)
        itemInfo = self._getKnowItemInfo(day)
        tipStr = self.bonusTip[day]
        if itemInfo:
            hasVp = itemInfo[1]
            tip = itemInfo[0][2]
            vp = OSBVD.data.get((day, vpLv), {}).get('vp', 0)
            playerLv = BigWorld.player().lv
            vpDefaultLower = VLD.data.get(playerLv, {}).get('vpDefaultLower', 0)
            vpDefaultUpper = VLD.data.get(playerLv, {}).get('vpDefaultUpper', 0)
            exp = (vpDefaultLower + vpDefaultUpper) / 2 * vp
            tipStr = tip % exp if hasVp else tip
        return tipStr

    def _getBonusItemId(self, day):
        itemId = 0
        itemInfo = self._getKnowItemInfo(day)
        if itemInfo:
            itemId = itemInfo[0][1]
        return itemId

    def _getKnowItemInfo(self, day):
        knowItem = OSBD.data.get(day, {}).get('knownItem', [])
        if len(knowItem) > 0:
            vpLv = self._getVpLv(day)
            lv1 = knowItem[0][0]
            lv2 = knowItem[1][0]
            lv3 = knowItem[2][0]
            if vpLv <= lv1:
                return [knowItem[0], True]
            elif vpLv > lv1 and vpLv <= lv2:
                return [knowItem[1], True]
            elif vpLv > lv2 and vpLv <= lv3:
                return [knowItem[2], False]
            else:
                return None

    def _getVpLv(self, day):
        vpLv = 0
        openServerBonus = BigWorld.player().openServerBonus
        if openServerBonus and openServerBonus.has_key(day):
            bonusData = openServerBonus[day]
            vpLv = bonusData.vpLv
        return vpLv

    def onGainReward(self, *args):
        day = args[3][0].GetNumber()
        gameglobal.rds.ui.messageBox.showMsgBox(msg='将领取所有可领取的新服奖励', callback=self.gainRewardCallBack, showTitle='新服福利')

    def gainRewardCallBack(self):
        BigWorld.player().cell.gainOpenServerBonus()

    def isNewServerActivityEnd(self):
        p = BigWorld.player()
        serverData = p.openServerBonus if p.openServerBonus else {}
        if not serverData:
            return False
        for key, value in OSBD.data.iteritems():
            if serverData.has_key(key):
                state = serverData[key].state
                if state != const.OPEN_SERVER_BONUS_STATE_REWARDED:
                    return False
                    break
            else:
                return False

        return True

    def showTick(self):
        if not self.panelMC:
            return
        self.panelMC.Invoke('showTick')

    def canOpenTab(self):
        canOpenTab = False
        hasReward = False
        enableNewServerSignInPanel = gameglobal.rds.configData.get('enableNewServerSignInPanel', False)
        lv = BigWorld.player().lv
        if enableNewServerSignInPanel and not self.isNewServerActivityEnd() and lv >= 20:
            canOpenTab = True
        if canOpenTab:
            frameInfo = self.getFrameInfo()
            if frameInfo['hasReward']:
                hasReward = True
        return (canOpenTab, hasReward)
