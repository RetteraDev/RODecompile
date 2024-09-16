#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendInviteActivity.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import events
import utils
from guis import uiUtils
from asObject import ASObject
from data import invitation_extra_reward_data as IERD
AD_ICON_TEMPLATE = 'advertisement/%s.dds'

class SummonFriendInviteActivity(object):

    def __init__(self, proxy):
        super(SummonFriendInviteActivity, self).__init__()
        self.parentProxy = proxy
        self.timer = None
        self.timedShopData = {}

    def getWidget(self):
        return self.parentProxy.widget

    def hideWidget(self):
        self.timer = None
        self.timedShopData = {}

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        activityMc = widget.invitePanel.activityMc
        activityMc.list.childItem = 'SummonFriendInviteV2_AcitivityItem'
        activityMc.list.childWidth = 229
        activityMc.list.pageItemFunc = self.activityItemFunc
        widget.pageRenderFunc = self.advertisementRendFunc
        self.refreshTimedShop()

    def refreshTimedShop(self):
        widget = self.getWidget()
        if not widget:
            return
        if not widget.invitePanel:
            return
        if not widget.invitePanel.activityMc:
            return
        adPageView = widget.invitePanel.activityMc.advertisement
        data = self.getTimedShopData()
        widget.invitePanel.activityMc.list.data = data['rewardInfo']
        if len(data['advertisements']) > 0:
            tmp = data['advertisements']
            adPageView.indicatorItemRenderName = 'SummonFriendInviteV2_Indicator'
            adPageView.data = tmp
        self.addTimer()

    def activityItemFunc(self, *args):
        item = ASObject(args[3][0])
        data = ASObject(args[3][1])
        item.itemName.mouseEnabled = True
        item.condition.mouseEnabled = False
        item.finishLabel.mouseEnabled = False
        item.restTime.mouseEnabled = False
        item.name = str(int(data.activityId))
        item.activityId = data.activityId
        item.itemName.htmlText = data.itemName
        item.condition.htmlText = data.condition
        if data.isFinished:
            item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_81
        else:
            item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_83
        item.restTime.visible = not data.isFinished
        item.restTime.htmlText = uiUtils.formatTime(data.restTime)
        item.itemSlot.setItemSlotData(data.itemData)
        item.itemSlot.dragable = False
        item.getRewardBtn.enabled = not data.hasReward and data.reachGoal
        item.getRewardBtn.label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187 if data.hasReward else gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_192
        item.getRewardBtn.addEventListener(events.MOUSE_CLICK, self.onGetActivityReward, False, 0, True)

    def onGetActivityReward(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        activityID = int(e.currentTarget.parent.name)
        p.cell.gainFriendInvitationSummaryReward(activityID)

    def advertisementRendFunc(self, *args):
        widget = self.getWidget()
        if not widget:
            return
        convertMc = ASObject(args[3][0])
        data = ASObject(args[3][1])
        if args[3][0].IsNull():
            convertMc = widget.getInstByClsName('SummonFriendInviteV2_AdIcon')
        adIcon = convertMc
        adIcon.adInfo = data
        adIcon.fitSize = True
        adIcon.loadImage(data.iconPath)
        adIcon.addEventListener(events.MOUSE_CLICK, self.onAdClick, False, 0, True)

    def onAdClick(self, *args):
        gameglobal.rds.ui.summonFriendBGV2.show()

    def getTimedShopData(self):
        ret = {}
        rewardData = IERD.data
        friendActivityData = getattr(BigWorld.player(), 'friendInvitationSummary', {})
        ret['advertisements'] = []
        ret['rewardInfo'] = []
        now = utils.getNow()
        for key, value in rewardData.items():
            startStamp = value.get('tStart', 1442455200)
            endStamp = value.get('tEnd', 1445472000)
            if now < startStamp:
                continue
            adItems = {}
            adItems['iconPath'] = AD_ICON_TEMPLATE % value.get('adName', '3')
            ret['advertisements'].append(adItems)
            item = {}
            rewardId = value.get('rewardId', 0)
            item['activityId'] = key
            item['condition'] = value.get('conditionDesc', gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_138)
            item['itemData'] = uiUtils.getGfxItemById(rewardId)
            item['itemName'] = uiUtils.getItemColorName(rewardId)
            item['isFinished'] = now > endStamp
            item['restTime'] = endStamp - now
            reqNum = value.get('num', 0)
            curNum = friendActivityData.get(key, [0, 0])[0]
            hasReward = friendActivityData.get(key, [0, 0])[1]
            item['reachGoal'] = reqNum <= curNum
            item['hasReward'] = hasReward
            ret['rewardInfo'].append(item)

        self.timedShopData = ret
        return ret

    def addTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
        self.updateTimer()

    def updateTimer(self):
        widget = self.getWidget()
        if not widget or not self.timedShopData:
            self.removeTimer()
            return
        activityMc = widget.invitePanel.activityMc
        arrLen = len(self.timedShopData['rewardInfo'])
        for i in range(arrLen):
            tempData = self.timedShopData['rewardInfo'][i]
            tempData['restTime'] -= 1
            item = activityMc.list.canvas.getChildByName(str(tempData['activityId']))
            if tempData['restTime'] > 0:
                if item:
                    item.restTime.htmlText = uiUtils.formatTime(tempData['restTime'])
            elif item:
                item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_81
                item.restTime.visible = False

        if self.timer:
            self.removeTimer()
        self.timer = BigWorld.callback(1, self.updateTimer)

    def removeTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
