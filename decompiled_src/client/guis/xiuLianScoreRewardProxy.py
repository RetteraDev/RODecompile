#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/xiuLianScoreRewardProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import clientUtils
from gameStrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject, RedPotManager
from data import guild_growth_volumn_data as GGVD
from cdata import guild_growth_score_award_data as GGSAD
MAX_TAB_BTN_NUM = 5

class XiuLianScoreRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(XiuLianScoreRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectBtn = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_XIU_LAIN_SCORE_REWARD, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_XIU_LAIN_SCORE_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_XIU_LAIN_SCORE_REWARD)

    def reset(self):
        self.selectBtn = None

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildGrowthScoreReward', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_XIU_LAIN_SCORE_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.rewardList.itemRenderer = 'XiuLianScoreReward_item'
        self.widget.rewardList.labelFunction = self.itemLableFunction
        self.widget.rewardList.column = 3
        self.widget.rewardList.dataArray = []

    def refreshTabs(self):
        itemList = []
        for key, value in GGSAD.data.iteritems():
            itemInfo = {}
            itemInfo['volumnId'] = key
            itemInfo['awardMargins'] = value.get('awardMargins', ())
            itemInfo['awardBonusIds'] = value.get('awardBonusIds', ())
            itemInfo['name'] = GGVD.data.get(key, {}).get('name', '')
            itemList.append(itemInfo)

        for i in xrange(MAX_TAB_BTN_NUM):
            btn = self.widget.getChildByName('tabBtn%d' % i)
            if i < len(itemList):
                btn.visible = True
                info = itemList[i]
                btn.label = info.get('name')
                btn.xiuLianData = info
                btn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
                if self.getXiuLianScoreTabRedPot(info['volumnId']):
                    RedPotManager.showSimpleRedPot(btn, (btn.width - 9, -3))
                else:
                    RedPotManager.removeRedPot(btn)
                if not self.selectBtn:
                    self.selectBtn = btn
            else:
                RedPotManager.removeRedPot(btn)
                btn.visible = False

        if self.selectBtn:
            self.selectBtn.selected = True

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTabs()
        self.updateReward()

    def handleBtnClick(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        if self.selectBtn:
            self.selectBtn.selected = False
            self.selectBtn = None
        self.selectBtn = targetBtn
        self.selectBtn.selected = True
        self.updateReward()

    def handleGetRewardBtnClick(self, *args):
        rewardBtn = ASObject(args[3][0]).currentTarget
        p = BigWorld.player()
        p.cell.receiveGuildGrowthScoreReward(int(rewardBtn.volumnId), int(rewardBtn.score))

    def itemLableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.item.gotoAndStop(itemData.state)
        itemMc.item.awardDesc.text = itemData.titleDesc
        rewardItems = clientUtils.genItemBonus(itemData.bonusId)
        for i in xrange(len(rewardItems)):
            slot = itemMc.item.getChildByName('icon%d' % i)
            if slot:
                itemId, itemNum = rewardItems[i]
                itemInfo = uiUtils.getGfxItemById(itemId, count=itemNum)
                slot.fitSize = True
                slot.dragable = False
                slot.setItemSlotData(itemInfo)

        if itemData.state == 'kelingqu':
            itemMc.item.lingQuBtn.volumnId = itemData.volumnId
            itemMc.item.lingQuBtn.score = itemData.score
            itemMc.item.lingQuBtn.addEventListener(events.BUTTON_CLICK, self.handleGetRewardBtnClick, False, 0, True)

    def updateReward(self):
        if not self.selectBtn:
            return
        p = BigWorld.player()
        xiuLianData = self.selectBtn.xiuLianData
        volumnId = xiuLianData.get('volumnId', 0)
        awardMargins = xiuLianData.get('awardMargins', ())
        awardBonusIds = xiuLianData.get('awardBonusIds', ())
        name = xiuLianData.get('name', '')
        myScore = p.guildGrowth.getVolumn(volumnId).score
        rewardList = []
        for i in xrange(len(awardBonusIds)):
            score = awardMargins[i]
            titleDesc = gameStrings.XIU_LIAN_REWARD_SOCRE_DESC % (name, score)
            if score in p.guildGrowthVolumnRewardInfo.get(volumnId, []):
                state = 'yilingqu'
            elif myScore < score:
                state = 'weidacheng'
            else:
                state = 'kelingqu'
            rewardList.append({'volumnId': volumnId,
             'score': score,
             'bonusId': awardBonusIds[i],
             'titleDesc': titleDesc,
             'state': state})

        self.widget.rewardList.dataArray = rewardList
        self.widget.rewardList.validateNow()

    def getXiuLianScoreTabRedPot(self, volumnId):
        if not gameglobal.rds.configData.get('enableGuildGrowthScoreReward', False):
            return False
        p = BigWorld.player()
        hasRedPot = False
        value = GGSAD.data.get(volumnId, {})
        awardMargins = value.get('awardMargins', ())
        myScore = p.guildGrowth.getVolumn(volumnId).score
        for score in awardMargins:
            if score not in p.guildGrowthVolumnRewardInfo.get(volumnId, []) and myScore >= score:
                hasRedPot = True
                break

        return hasRedPot

    def getXiuLianScoreRewardRedPot(self):
        if not gameglobal.rds.configData.get('enableGuildGrowthScoreReward', False):
            return False
        p = BigWorld.player()
        hasRedPot = False
        for key, value in GGSAD.data.iteritems():
            volumnId = key
            awardMargins = value.get('awardMargins', ())
            myScore = p.guildGrowth.getVolumn(volumnId).score
            for score in awardMargins:
                if score not in p.guildGrowthVolumnRewardInfo.get(volumnId, []) and myScore >= score:
                    hasRedPot = True
                    break

        return hasRedPot
