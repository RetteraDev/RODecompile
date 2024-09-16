#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareRewardCatchUpProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import gamelog
import clientUtils
import math
import gametypes
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import reward_catch_up_data as RCUD
from data import fame_data as FD
from cdata import qumo_junjie_reward_catchup_data as QJRCD
from cdata import qumo_junjie_reward_catchup_price_data as QJRCPD
REWARD_ITEM_MAX_CNT = 6
REWARD_ICON_MAX_CNT = 4
EXP_ITEM_ID = 441002

class WelfareRewardCatchUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareRewardCatchUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.freeCnt = 0
        self.reset()

    def reset(self):
        self.isActivityMode = False
        self.expandDic = {}

    def initRewardCatchUp(self, widget):
        self.widget = ASObject(widget)
        self.initUI()
        self.refreshInfo()

    def initUI(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_REWARD_CATCH_UP)
        if not self.widget:
            return
        self.widget.helpIcon.helpKey = SCD.data.get('rewardCatchUpHelpKey', 0)
        self.widget.removeAllInst(self.widget.scrollWndList.canvas)
        self.widget.scrollWndList.itemRenderer = 'WelfareRewardCatchUp_ItemRender'
        self.widget.scrollWndList.lableFunction = self.labelFunction
        self.widget.scrollWndList.itemHeight = 117
        self.widget.banner.loadImage('welfare/%s.dds' % SCD.data.get('rewardCatchUpBannerName', 'zhuigan'))

    def unRegistRewardCatchUp(self):
        self.uiAdapter.catchUpDetail.hide()
        if self.widget:
            self.widget.scrollWndList.dataArray = []
            self.widget = None
        self.reset()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.validateNow()
        infoList = self.getInfoList()
        self.freeCnt = 0
        if not infoList:
            self.unRegistRewardCatchUp()
        else:
            self.widget.scrollWndList.dataArray = infoList
            self.widget.scrollWndList.validateNow()
        gameglobal.rds.ui.welfare.refreshInfo()

    def getInfoList(self):
        infoList = []
        p = BigWorld.player()
        for id, info in RCUD.data.iteritems():
            school = info.get('school', 0)
            if school and p.school != school:
                continue
            rewardCatchUpInfo = p.rewardCatchUpInfo.values()
            rewardInfo = ()
            if rewardCatchUpInfo:
                rewardInfo = rewardCatchUpInfo[0].get(id, ())
            if rewardInfo:
                if rewardInfo[0] + rewardInfo[1] <= 0:
                    continue
            else:
                continue
            lv = info.get('lv', 0)
            historyLv = rewardInfo[3]
            if lv and not lv[0] <= historyLv <= lv[1]:
                continue
            itemData = {}
            itemData['rewardCatchUpInfo'] = rewardInfo
            activityType = info.get('activityType', 0)
            itemData['rewardId'] = id
            itemData['title'] = info.get('ItemTitle', '')
            if activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_QU_MO, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_JUN_JIE]:
                qumoLv, junjieLv = rewardInfo[4:]
                extraLv = qumoLv if activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_QU_MO else junjieLv
                if not extraLv:
                    continue
                qjrgd = QJRCD.data.get((extraLv, activityType), {})
                bonusId = qjrgd.get('wingWorldbonusId', 0) if gameglobal.rds.configData.get('enableWingWorld', False) else qjrgd.get('bonusId', 0)
                itemDic = {}
                for itemId, cnt in clientUtils.genItemBonus(bonusId):
                    itemDic[itemId] = itemDic.get(itemId, 0) + cnt

                itemList = [ uiUtils.getGfxItemById(key, value) for key, value in itemDic.iteritems() ]
                consumeCoins = QJRCPD.data.get(bonusId, {}).get('coin', 0)
                if consumeCoins:
                    itemData['consumeCoins'] = consumeCoins
            else:
                canBackBonus = info.get('bonusIds', {})
                canBackBonusIds = []
                if canBackBonus:
                    for key in canBackBonus.keys():
                        if key[0] <= historyLv <= key[1]:
                            bonusId = canBackBonus.get(key, 0)
                            if bonusId:
                                canBackBonusIds.append(bonusId)

                itemDic = {}
                for bonusId in canBackBonusIds:
                    for itemId, cnt in clientUtils.genItemBonus(bonusId):
                        itemDic[itemId] = itemDic.get(itemId, 0) + cnt

                itemList = [ uiUtils.getGfxItemById(key, value) for key, value in itemDic.iteritems() ]
                consumeCoins = info.get('consumeCoins')
                if consumeCoins:
                    itemData['consumeCoins'] = consumeCoins({'lv': historyLv})
            itemData['iconList'] = []
            addExp = info.get('addExp')
            exp = 0
            if addExp:
                exp = addExp({'lv': historyLv})
            if exp:
                itemList.append(uiUtils.getGfxItemById(EXP_ITEM_ID, 1))
            itemData['itemList'] = itemList
            itemData['iconList'].append(('exp', exp))
            fameList = info.get('addFame', ())
            for fameId, fameVal in fameList:
                itemData['iconList'].append(('shenwang', fameVal, fameId))

            itemData['sortOrder'] = info.get('sortOrder', 0)
            infoList.append(itemData)
            infoList.sort(key=lambda x: x['sortOrder'])

        return infoList

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.itemData = itemData
        itemList = itemData.itemList
        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemSlot = itemMc.getChildByName('item%d' % i)
            if i >= len(itemList):
                itemSlot.visible = False
                continue
            itemSlot.visible = True
            itemSlot.dragable = False
            itemSlot.setItemSlotData(itemList[i])

        for i in xrange(REWARD_ICON_MAX_CNT):
            bonusIcon = itemMc.getChildByName('rewardIcon%d' % i)
            rewardTxt = itemMc.getChildByName('rewardTxt%d' % i)
            bonusIcon.visible = False
            rewardTxt.visible = False

        iconList = itemData.iconList
        index = 0
        for j in xrange(len(iconList)):
            if iconList[j][1] == 0:
                continue
            bonusIcon = itemMc.getChildByName('rewardIcon%d' % index)
            rewardTxt = itemMc.getChildByName('rewardTxt%d' % index)
            bonusIcon.visible = True
            rewardTxt.visible = True
            index = index + 1
            bonusIcon.bonusType = iconList[j][0]
            rewardTxt.text = str(int(iconList[j][1]))
            if iconList[j][0] == 'shenwang':
                TipManager.addTip(bonusIcon, FD.data.get(iconList[j][2], {}).get('name', ''))

        itemMc.costMc.visible = False
        itemMc.freeDesc.visible = False
        freeCnt, payCnt, discount = itemData.rewardCatchUpInfo[:3]
        itemMc.txtTitile.text = itemData.title % (freeCnt + payCnt)
        self.freeCnt += freeCnt
        discount = min(discount, 1)
        if freeCnt:
            itemMc.freeDesc.visible = True
            itemMc.costMc.visible = False
            itemMc.freeDesc.htmlText = gameStrings.TEXT_WELFAREREWARDCATCHUPPROXY_217 % freeCnt
        else:
            itemMc.costMc.visible = True
            itemMc.freeDesc.visible = False
            itemMc.costMc.priceMc.desc.text = gameStrings.TEXT_WELFAREREWARDCATCHUPPROXY_221
            if discount and discount < 1:
                itemMc.costMc.discountMc.visible = True
                itemMc.costMc.priceMc.costTxt0.text = int(math.ceil(int(itemData.consumeCoins) * discount))
                discountShow = discount * 10
                discountShow = int(discountShow) if discountShow == int(discountShow) else discountShow
                itemMc.costMc.discountMc.discount.htmlText = gameStrings.TEXT_WELFAREREWARDCATCHUPPROXY_228 % str(discountShow)
                itemMc.costMc.discountMc.costTxt1.gotoAndStop('yuanjia')
                itemMc.costMc.discountMc.costTxt1.delFlag.width = len(str(itemData.consumeCoins)) * 7.5
                itemMc.costMc.discountMc.costTxt1.costTxt1.text = int(itemData.consumeCoins)
            else:
                itemMc.costMc.discountMc.visible = False
                itemMc.costMc.priceMc.costTxt0.text = int(itemData.consumeCoins)
        itemMc.gainRewrdBtn.label = gameStrings.WELFARE_REWARD_CATCH_UP_RETRIEVE_BTN
        itemMc.gainRewrdBtn.addEventListener(events.BUTTON_CLICK, self.handleGainRewardBtnClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleIemOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleItemOut, False, 0, True)

    def handleIemOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.itemIcon.gotoAndStop('over')

    def handleItemOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.itemIcon.gotoAndStop('normal')

    def handleGainRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.parent.itemData
        gameglobal.rds.ui.catchUpDetail.show(itemData)

    def getRedFlagVisible(self):
        return self.freeCnt > 0

    def addPushIcon(self):
        if not gameglobal.rds.configData.get('enableRewardCatchUp', False):
            return
        if BigWorld.player().lv < SCD.data.get('welfareRewardCatchUpTabLv', 20):
            return
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_REWARD_CATCH_UP) and uiConst.MESSAGE_TYPE_REWARD_CATCH_UP not in self.uiAdapter.pushMessage.onceMessage:
            callBackDict = {'click': Functor(self.uiAdapter.welfare.show, uiConst.WELFARE_TAB_REWARD_CATCH_UP)}
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_REWARD_CATCH_UP, callBackDict)
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_REWARD_CATCH_UP)

    def isOpen(self):
        if gameglobal.rds.configData.get('enableRewardCatchUp', False):
            p = BigWorld.player()
            rewardCatchUpInfo = p.rewardCatchUpInfo.values()
            rewardInfoList = []
            if rewardCatchUpInfo:
                rewardInfoList = rewardCatchUpInfo[0].values()
            for rewardInfo in rewardInfoList:
                freeCnt, payCnt = rewardInfo[:2]
                if freeCnt > 0 or payCnt > 0:
                    return True

        return False

    def checkRedFlag(self):
        return False
