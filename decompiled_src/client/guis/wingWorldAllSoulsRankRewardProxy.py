#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldAllSoulsRankRewardProxy.o
import BigWorld
import gameglobal
import uiConst
import wingWorldUtils
from uiProxy import UIProxy
from asObject import ASObject
from helpers import guild as guildUtils
from guis import uiUtils
from data import wing_soul_boss_data as WSBD
from data import guild_top_reward_data as GTRD
from data import bonus_data as BD
from data import wing_world_config_data as WWCD
import gamelog
FIRST_ATTACK_REWARD_COUNT = 3
KILL_ATTACK_REWARD_COUNT = 3
RANK_REWARD_COUNT = 3

class WingWorldAllSoulsRankRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldAllSoulsRankRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.currentBossId = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK_REWARD, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.currentBossId = -1
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK_REWARD)

    def show(self, bossId):
        self.currentBossId = bossId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK_REWARD)
        else:
            self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshFirstAttackReward()
        self.refreshKillAttackReward()
        self.refreshRankReward()

    def refreshFirstAttackReward(self):
        bossInfo = WSBD.data.get(self.currentBossId, {})
        if wingWorldUtils.isInWingCelebration():
            firstBonusIndex = bossInfo.get('qdshoudaobonusId', ())
        else:
            firstBonusIndex = bossInfo.get('shoudaobonusId', ())
        firstBonusIds, _ = guildUtils.getGuildTopRewardInfo(GTRD.data.get(firstBonusIndex, {}), 1)
        firstAtkItems = []
        for id in firstBonusIds:
            firstAtkItems.extend(BD.data.get(id, {}).get('displayItems', []))

        gamelog.debug('ypc@ firstAtkItems = ', firstAtkItems)
        for i in xrange(0, FIRST_ATTACK_REWARD_COUNT):
            item = self.widget.getChildByName('first%d' % i)
            if i < len(firstAtkItems):
                itemId, cnt = firstAtkItems[i]
                item.visible = True
                item.slot.dragable = False
                item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
            else:
                item.visible = False

    def refreshKillAttackReward(self):
        bossInfo = WSBD.data.get(self.currentBossId, {})
        if wingWorldUtils.isInWingCelebration():
            killBonusIndex = bossInfo.get('qdweidaobonusId', ())
        else:
            killBonusIndex = bossInfo.get('weidaobonusId', ())
        killBonusIds, _ = guildUtils.getGuildTopRewardInfo(GTRD.data.get(killBonusIndex, {}), 1)
        killAtkItems = []
        for id in killBonusIds:
            killAtkItems.extend(BD.data.get(id, {}).get('displayItems', []))

        gamelog.debug('ypc@ killAtkItems = ', killAtkItems)
        for i in xrange(0, KILL_ATTACK_REWARD_COUNT):
            item = self.widget.getChildByName('kill%d' % i)
            if i < len(killAtkItems):
                itemId, cnt = killAtkItems[i]
                item.visible = True
                item.slot.dragable = False
                item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
            else:
                item.visible = False

    def refreshRankReward(self):
        self.widget.rewardList.itemRenderer = 'WingWorldAllSoulsRankReward_ListItemRenderer'
        self.widget.rewardList.labelFunction = self.listRenderFunction
        self.widget.desc.text = WWCD.data.get('wingWorldAllSoulsRewardDesc', '')
        bossInfo = WSBD.data.get(self.currentBossId, {})
        if wingWorldUtils.isInWingCelebration():
            rankBonusIndex = bossInfo.get('qdjishabonusId', ())
        else:
            rankBonusIndex = bossInfo.get('jishabonusId', ())
        allRankReward = GTRD.data.get(rankBonusIndex, [])
        listArray = []
        for i in xrange(0, len(allRankReward)):
            rewards = []
            bonusIds, _ = guildUtils.getGuildTopRewardInfo(allRankReward, i + 1)
            desc = allRankReward[i].get('desc', '')
            for id in bonusIds:
                rewards.extend(BD.data.get(id, {}).get('displayItems', []))

            listArray.append({'rank': i + 1,
             'desc': desc,
             'rewards': rewards[0:RANK_REWARD_COUNT]})

        self.widget.rewardList.dataArray = listArray

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def listRenderFunction(self, *args):
        data = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.desc.text = data.desc
        itemMc.rank.num.text = str(data.rank)
        for i in xrange(0, RANK_REWARD_COUNT):
            slot = itemMc.getChildByName('reward%d' % i).slot
            if i < len(data.rewards):
                itemId, itemCount = data.rewards[i][0], data.rewards[i][1]
                slot.visible = True
                slot.dragable = False
                slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
            else:
                slot.visible = False
