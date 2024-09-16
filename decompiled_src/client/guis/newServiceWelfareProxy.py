#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceWelfareProxy.o
from gamestrings import gameStrings
import BigWorld
import utils
import uiUtils
import const
import events
import tipUtils
import gameglobal
import commNewServerActivity
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import TipManager
from data import open_server_bonus_data as OSBD
from data import sys_config_data as SCD
from cdata import open_server_bonus_vp_data as OSBVD
from data import vp_level_data as VLD

class NewServiceWelfareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceWelfareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bonusTip = {}
        self.dayCnt = 0
        self.callback = None

    def reset(self):
        self.dayCnt = 0
        self.callback = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        if not self.widget:
            return
        self.widget.mainMC.leftTime.visible = False
        self.widget.mainMC.leftTimeTxt.visible = False
        self.widget.mainMC.now.visible = False
        scrollList = self.widget.mainMC.onlineRewardList
        scrollList.column = 1
        scrollList.itemRenderer = 'NewServiceWelfare_Item'
        scrollList.lableFunction = self.listLabelFunction

    def refreshInfo(self):
        if not self.widget:
            return
        frameInfo = self.getFrameInfo()
        self.widget.mainMC.onlineRewardList.dataArray = frameInfo.get('itemList', [])
        self.widget.mainMC.onlineRewardList.validateNow()
        self.updateTime()

    def updateTime(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        if p.openServerBonus and hasattr(p.openServerBonus, 'getMinLeftTime'):
            minTimeLeft, self.dayCnt = p.openServerBonus.getMinLeftTime(p)
        else:
            minTimeLeft, self.dayCnt = (-1, 0)
        if minTimeLeft == -1:
            self.stopCallback()
            return
        self.updateItemMc(minTimeLeft)
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.callback = BigWorld.callback(1, self.updateTime)

    def updateItemMc(self, minTimeLeft):
        listItems = self.widget.mainMC.onlineRewardList.items
        listItemsLen = len(listItems)
        for i in xrange(listItemsLen):
            itemMc = listItems[i]
            if itemMc.stateStr == 'wait' and itemMc.dayCnt == self.dayCnt:
                itemMc.state.text = utils.formatTimeStr(minTimeLeft)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def getFrameInfo(self):
        p = BigWorld.player()
        serverData = p.openServerBonus if p.openServerBonus else {}
        frameInfo = {}
        serverOpendDay = utils.getServerOpenDays() + 1
        frameInfo['passedDay'] = SCD.data.get('openServerBonusDesc', gameStrings.TEXT_NEWSERVICEWELFAREPROXY_103) % min(30, serverOpendDay)
        frameInfo['remainTime'] = utils.getServerOpenTime() + const.TIME_INTERVAL_MONTH - const.TIME_INTERVAL_DAY - utils.getNow()
        itemList = []
        hasReward = False
        if p.openServerBonus and hasattr(p.openServerBonus, 'getMinLeftTime'):
            minTimeLeft, self.dayCnt = p.openServerBonus.getMinLeftTime(p)
        else:
            minTimeLeft, self.dayCnt = (0, 0)
        for key, value in OSBD.data.iteritems():
            itemInfo = {}
            itemInfo['day'] = key
            tips = value.get('text', gameStrings.TEXT_NEWSERVICEWELFAREPROXY_116)
            self.bonusTip[key] = tips
            if serverData.has_key(key):
                state = serverData[key].state
                if state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                    itemInfo['state'] = 'wait'
                    if key > self.dayCnt:
                        leftTime = gameStrings.TEXT_NEWSERVICEWELFAREPROXY_123
                    elif self.dayCnt == key:
                        leftTime = utils.formatTimeStr(minTimeLeft)
                    else:
                        leftTime = ''
                    itemInfo['stateText'] = leftTime
                elif state == const.OPEN_SERVER_BONUS_STATE_READY:
                    itemInfo['state'] = 'ready'
                    hasReward = True
                    itemInfo['stateText'] = ''
                else:
                    itemInfo['state'] = 'gained'
                    itemInfo['stateText'] = ''
            else:
                itemInfo['state'] = 'notOpen'
                itemInfo['stateText'] = gameStrings.TEXT_NEWSERVICEWELFAREPROXY_139
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
                return [knowItem[0], False]
            elif vpLv > lv1 and vpLv <= lv2:
                return [knowItem[1], False]
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

    def listLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.stateStr = itemData.state
        itemMc.dayCnt = itemData.day
        itemMc.day.text = gameStrings.TEXT_NEWSERVICEWELFAREPROXY_211 % itemData.day
        slot = itemMc.icon.slot
        slot.setItemSlotData(itemData.item)
        slot.dragable = False
        itemMc.state.visible = itemData.state == 'wait' or itemData.state == 'notOpen'
        itemMc.gainBtn.enabled = itemData.state == 'ready'
        itemMc.state.text = itemData.stateText
        if itemData.state == 'gained':
            itemMc.gainBtn.label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
        else:
            itemMc.gainBtn.label = gameStrings.TEXT_NEWBIEGUIDEPROXY_344
        itemMc.gainBtn.itemData = itemData
        itemMc.gainBtn.addEventListener(events.MOUSE_CLICK, self.handleGainBtnClick, False, 0, True)
        slot.validateNow()
        TipManager.addTip(slot, itemData.tips, tipUtils.TYPE_DEFAULT_BLACK)

    def handleGainBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        day = target.itemData.day
        gameglobal.rds.ui.messageBox.showMsgBox(msg=gameStrings.TEXT_NEWSERVICEWELFAREPROXY_234, callback=self.gainRewardCallBack, showTitle=gameStrings.TEXT_NEWSERVICEWELFAREPROXY_234_1)

    def gainRewardCallBack(self):
        BigWorld.player().cell.gainOpenServerBonus()

    def canOpenTab(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_WELFARE):
            return False
        p = BigWorld.player()
        if not p._isOpenServerBonusEnabled():
            return False
        enableNewServerSignInPanel = gameglobal.rds.configData.get('enableNewServerSignInPanel', False)
        if enableNewServerSignInPanel and not self.isNewServerActivityEnd() and p.lv >= 20:
            return True
        return False

    def isShowWelfareRedPoint(self):
        hasReward = False
        if self.canOpenTab():
            frameInfo = self.getFrameInfo()
            if frameInfo['hasReward']:
                hasReward = True
        return hasReward

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

    def updateNewServiceWelfare(self):
        self.refreshInfo()
        gameglobal.rds.ui.newServiceActivities.updateActiviesTabWelfareRedPot()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
