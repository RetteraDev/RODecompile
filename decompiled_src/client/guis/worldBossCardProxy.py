#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossCardProxy.o
import BigWorld
import gameglobal
import uiConst
from guis.asObject import ASUtils
from uiProxy import UIProxy
from guis import uiUtils
from guis import worldBossHelper
from gamestrings import gameStrings
from data import duel_config_data as DCD
SMALL_BOSS_NUM = 6
REWARD_ITEM_NUM = 4

class WorldBossCardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldBossCardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_CARD, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WORLD_CARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_CARD)

    def show(self):
        p = BigWorld.player()
        p.base.queryWorldBossCard()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_CARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def setCardInfo(self, mc, bossInfo, isBigCard = False):
        killNum = bossInfo.get('killNum', 0)
        if killNum == 0:
            ASUtils.setMcEffect(mc.bossIcon, 'gray')
        else:
            ASUtils.setMcEffect(mc.bossIcon, '')
        mc.bossName.text = bossInfo.get('bossName', '')
        mc.numMc.textField.text = gameStrings.WORLD_BOSS_KILL_NUM % killNum
        if isBigCard:
            mc.bossIcon.fitSize = True
            mc.bossIcon.loadImage(bossInfo.get('bossIcon', ''))
        else:
            mc.bossIcon.fitSize = True
            mc.bossIcon.loadImage(bossInfo.get('bossSmallIcon', ''))

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshCards()
        self.refreshReward()

    def refreshCards(self):
        cardInfo = worldBossHelper.getInstance().getWorldBossCardInfo()
        bossIds = worldBossHelper.getInstance().getNormalWorldBossIds()
        for i in xrange(SMALL_BOSS_NUM):
            cardMc = self.widget.getChildByName('subCard%d' % i)
            if i < len(bossIds):
                bossId = bossIds[i]
                bossInfo = worldBossHelper.getInstance().getBossBaseInfoByBossId(bossId)
                bossInfo['killNum'] = cardInfo.get(bossId, 0)
                self.setCardInfo(cardMc, bossInfo)
            else:
                self.setCardInfo(cardMc, {})

        rareBossId = worldBossHelper.getInstance().getRareWorldBossId()
        cardMc = self.widget.mainCard
        bossInfo = worldBossHelper.getInstance().getBossBaseInfoByBossId(rareBossId)
        bossInfo['killNum'] = cardInfo.get(rareBossId, 0)
        self.setCardInfo(cardMc, bossInfo, True)

    def refreshReward(self):
        rewardItemList = DCD.data.get('worldBossCardRewardList', [])
        for i in xrange(REWARD_ITEM_NUM):
            rewardSlot = self.widget.getChildByName('slot%d' % i)
            rewardSlot.dragable = False
            if i < len(rewardItemList):
                itemId, num = rewardItemList[i]
                rewardSlot.visible = True
                itemInfo = uiUtils.getGfxItemById(itemId, num)
                rewardSlot.setItemSlotData(itemInfo)
            else:
                rewardSlot.visible = False

        self.widget.tipText.text = DCD.data.get('worldBossCardRewardTip', '')
