#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chargeRewardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import clientUtils
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import coin_charge_reward_data as CCRD
from Scaleform import GfxValue
from ui import gbk2unicode
import gamelog
TIANQUAN_ITEM_ID = 3
AD_ICON_TEMPLATE = 'advertisement/%s.dds'

class ChargeRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChargeRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRewardInfo': self.onGetRewardInfo,
         'closeChargeReward': self.onCloseChargeReward,
         'openChargeWindow': self.onOpenChargeWindow,
         'getTitleInfo': self.onGetTitleInfo,
         'openChooseRewardWindow': self.onOpenChooseRewardWindow}
        self.widgetId = uiConst.WIDGET_CHARGE_REWARD
        self.mediator = None
        self.pushFlag = False
        self.pushId = 0
        self.rewardTitle = None
        uiAdapter.registerEscFunc(self.widgetId, self.hide)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator

    def show(self):
        if not self.showChargeReward():
            return
        gameglobal.rds.ui.loadWidget(self.widgetId, True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None

    def showChargeReward(self):
        crId, crData = self.chargeRewardInfo()
        if not crId:
            return False
        return gameglobal.rds.configData.get('enableChargeReward', True)

    def genChargeRewardItemInfo(self, myRewardInfo, index, rewardInfo, chooseReward):
        ret = {}
        rewardList = []
        if rewardInfo[2] > 0:
            rewardList.append(uiUtils.getGfxItemById(TIANQUAN_ITEM_ID, rewardInfo[2]))
        bonusId = rewardInfo[3]
        if bonusId:
            bonusItems = clientUtils.genItemBonus(bonusId, True)
            for itemId, count in bonusItems:
                rewardList.append(uiUtils.getGfxItemById(itemId, count))

        if myRewardInfo:
            ret['sendFlag'] = index in myRewardInfo[3]
            if len(myRewardInfo) >= 5:
                ret['choosedRewardFlag'] = index in myRewardInfo[4]
            else:
                ret['choosedRewardFlag'] = False
        else:
            ret['sendFlag'] = False
            ret['choosedRewardFlag'] = False
        if ret['sendFlag']:
            ret['sendTips'] = gameStrings.TEXT_CHARGEREWARDPROXY_89
        else:
            tips = ''
            if rewardInfo[0] > 0:
                tips += gameStrings.TEXT_CHARGEREWARDPROXY_94 + str(rewardInfo[0]) + gameStrings.TEXT_CHARGEREWARDPROXY_94_1
            if rewardInfo[1] > 0:
                tips += gameStrings.TEXT_CHARGEREWARDPROXY_97 + str(rewardInfo[1]) + gameStrings.TEXT_CHARGEREWARDPROXY_94_1
            ret['sendTips'] = tips
        ret['chargeValue'] = rewardInfo[0]
        ret['costValue'] = rewardInfo[1]
        ret['checkRewardTxt'] = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_154
        ret['chooseRewardTxt'] = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_151
        ret['sentRewardTxt'] = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
        if len(chooseReward) > index:
            if len(chooseReward[index]) > 0 and chooseReward[index][1] > 0:
                ret['rewardBtnVisible'] = True
            else:
                ret['rewardBtnVisible'] = False
        else:
            ret['rewardBtnVisible'] = False
        ret['index'] = index
        ret['rewardList'] = rewardList
        return ret

    def chargeRewardInfo(self):
        now = utils.getNow()
        for key, val in CCRD.data.iteritems():
            beginTime = utils.getTimeSecondFromStr(val.get('beginTime', ''))
            endTime = utils.getTimeSecondFromStr(val.get('endTime', ''))
            rewardTitle = val.get('chargeRewardName', gameStrings.TEXT_CHARGEREWARDPROXY_94)
            whiteList = val.get('whiteList', None)
            if whiteList and utils.getHostId() not in whiteList:
                continue
            if now >= beginTime and now <= endTime:
                self.rewardTitle = rewardTitle
                return (key, val)

        return (0, {})

    def refreshRewardInfo(self):
        if not self.mediator:
            return
        self.mediator.Invoke('refreshRewardInfo')

    def onSendRewardInfo(self):
        self.refreshRewardInfo()
        if not gameglobal.rds.ui.tianyuMall.showMallConfig():
            return
        if not self.pushFlag:
            self.pushChargeRewardInfo()

    def clearAll(self):
        self.pushFlag = False

    def pushChargeRewardInfo(self):
        if gameglobal.rds.configData.get('enableChargeRewardLoop', False):
            return
        elif not self.showChargeReward():
            return
        else:
            crId, crData = self.chargeRewardInfo()
            if not crId:
                return
            myRewardInfo = None
            for info in BigWorld.player().chargeRewardInfo:
                if info[0] == crId:
                    myRewardInfo = info
                    break

            hasReward = False
            if not myRewardInfo:
                hasReward = True
            else:
                for index, rewardInfo in enumerate(crData.get('chargeCoins', [])):
                    if index not in myRewardInfo[3]:
                        hasReward = True
                        break

            if not hasReward:
                return
            self.pushFlag = True
            self.pushId = crData.get('pushId', 11203)
            gameglobal.rds.ui.pushMessage.addPushMsg(self.pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(self.pushId, {'click': self.onPushClick})
            return

    def onPushClick(self):
        self.show()
        gameglobal.rds.ui.pushMessage.removePushMsg(self.pushId)

    def onGetRewardInfo(self, *arg):
        ret = {}
        crId, crData = self.chargeRewardInfo()
        ret['adIcon'] = AD_ICON_TEMPLATE % crData.get('pic', 0)
        beginTimeStr = crData.get('beginTime', '1.1')
        endTimeStr = crData.get('endTime', '1.1')
        sBegin = beginTimeStr.split('.')
        sEnd = endTimeStr.split('.')
        if len(sBegin) != 6 or len(sEnd) != 6:
            ret['periodTips'] = gameStrings.TEXT_CHARGEREWARDPROXY_212
        else:
            beginTips = ''
            endTips = ''
            for i in range(3):
                beginTips += str(sBegin[i])
                endTips += str(sEnd[i])
                if i != 2:
                    beginTips += '.'
                    endTips += '.'

            ret['periodTips'] = gameStrings.TEXT_CHARGEREWARDPROXY_225 % (beginTips, endTips)
        ret['chargeValue'] = 0
        ret['costValue'] = 0
        myRewardInfo = None
        for info in BigWorld.player().chargeRewardInfo:
            if info[0] == crId:
                ret['chargeValue'] = info[1]
                ret['costValue'] = info[2]
                myRewardInfo = info
                break

        rewardList = []
        for index, rewardInfo in enumerate(crData.get('chargeCoins', [])):
            chooseReward = crData.get('rewardsForChoose', [])
            rewardList.append(self.genChargeRewardItemInfo(myRewardInfo, index, rewardInfo, chooseReward))

        ret['rewardList'] = rewardList
        return uiUtils.dict2GfxDict(ret, True)

    def onCloseChargeReward(self, *arg):
        self.hide()

    def onOpenChargeWindow(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onOpenChooseRewardWindow(self, *arg):
        index = int(arg[3][0].GetNumber())
        isChooseReward = bool(arg[3][1].GetBool())
        gameglobal.rds.ui.chooseReward.show(index, isChooseReward)

    def getTitleInfo(self):
        self.chargeRewardInfo()
        return self.rewardTitle

    def onGetTitleInfo(self, *arg):
        ret = self.rewardTitle
        return GfxValue(gbk2unicode(ret))
