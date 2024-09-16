#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/killFallenRedGuardRewardProxy.o
import BigWorld
import uiConst
import events
import copy
import const
import gametypes
import utils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import uiUtils
from helpers import guild as guildUtils
from data import guild_top_reward_data as GTRD
from data import guild_config_data as GCD
from data import bonus_data as BD
from data import fallen_red_guard_data as FRGD
REWARD_ITEM_MAX_CNT = 3

class KillFallenRedGuardRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(KillFallenRedGuardRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_REWARD, self.hide)

    def reset(self):
        self.selectedKey = 0
        self.selectedMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_KILL_FALLEN_RED_GUARD_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_REWARD)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'KillFallenRedGuardReward_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.txtDesc.htmlText = GCD.data.get('KillFallenRedGuardRewardTips', '')

    def refreshInfo(self):
        if not self.widget:
            return
        rankId = gametypes.TOP_TYPE_FALLEN_RED_GUARD_FIRST_ATTACK_SPECIAL if self.isSpecial() else gametypes.TOP_TYPE_FALLEN_RED_GUARD_FIRST_ATTACK
        firstAtkBonusIds, _ = guildUtils.getGuildTopRewardInfo(GTRD.data.get((rankId, 0, 0)), 1)
        firstAtkBonusItems = []
        for firstAtkBonusId in firstAtkBonusIds:
            firstAtkBonusItems.extend(BD.data.get(firstAtkBonusId, {}).get('displayItems', []))

        killRankId = gametypes.TOP_TYPE_FALLEN_RED_GUARD_KILL_SPECIAL if self.isSpecial() else gametypes.TOP_TYPE_FALLEN_RED_GUARD_KILL
        killBonusIds, _ = guildUtils.getGuildTopRewardInfo(GTRD.data.get((killRankId, 0, 0)), 1)
        killBonusItems = []
        for killBonusId in killBonusIds:
            killBonusItems.extend(BD.data.get(killBonusId, {}).get('displayItems', []))

        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemMc = self.widget.getChildByName('firstAtkReward%d' % i)
            if i < len(firstAtkBonusItems):
                itemId, cnt = firstAtkBonusItems[i]
                itemMc.visible = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
            else:
                itemMc.visible = False

        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemMc = self.widget.getChildByName('killReward%d' % i)
            if i < len(killBonusItems):
                itemId, cnt = killBonusItems[i]
                itemMc.visible = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
            else:
                itemMc.visible = False

        rewardList = []
        dmgRankId = gametypes.TOP_TYPE_FALLEN_RED_GUARD_DAMAGE_SPECIAL if self.isSpecial() else gametypes.TOP_TYPE_FALLEN_RED_GUARD_DAMAGE
        rankIndex = 0
        while True:
            bonusIds = guildUtils.getGuildTopRewardInfo(GTRD.data.get((dmgRankId, 0, 0)), rankIndex + 1)[0]
            desc = gameStrings.KILL_FALLEN_RED_GUARD_RANK % (rankIndex + 1)
            if bonusIds:
                rewardList.append((rankIndex + 1, bonusIds, desc))
                rankIndex += 1
            else:
                break

        self.widget.scrollWndList.dataArray = rewardList

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        key = itemData[0]
        bonusIds = itemData[1]
        desc = itemData[2]
        itemMc.groupName = 'killFallenRedGuardReward'
        itemMc.key = key
        if key < 10:
            itemMc.rank.visible = True
            itemMc.rank.txtRank.text = key
        else:
            itemMc.rank.visible = False
        itemMc.txtRank.text = desc
        bonusItems = []
        for i in xrange(int(bonusIds.length)):
            bonusId = int(bonusIds[i])
            bonusItems.extend(BD.data.get(bonusId, {}).get('displayItems', ()))

        for i in xrange(REWARD_ITEM_MAX_CNT):
            item = itemMc.getChildByName('item%d' % i)
            if i < len(bonusItems):
                itemId, cnt = bonusItems[i]
                item.visible = True
                item.slot.dragable = False
                item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
            else:
                item.visible = False

        itemMc.addEventListener(events.MOUSE_OVER, self.handleItemRenderMouseOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_OUT, self.handleItemRenderMouseOut, False, 0, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemRenderMouseClick, False, 0, True)

    def isSpecial(self):
        p = BigWorld.player()
        if utils.getWeekInt() != const.WEEK_INT_FRI:
            return False
        chunkName = BigWorld.ChunkInfoAt(p.position)
        flag = self.uiAdapter.killFallenRedGuardRank.getFlagByTrunkName(chunkName)
        return FRGD.data.get(flag, {}).get('order', 0) == 1

    def handleItemRenderMouseOver(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.key == self.selectedKey:
            e.currentTarget.gotoAndStop('over')

    def handleItemRenderMouseOut(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.key == self.selectedKey:
            e.currentTarget.gotoAndStop('up')

    def handleItemRenderMouseClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedMc:
            if self.selectedMc.key == e.currentTarget.key:
                return
            self.selectedMc.gotoAndStop('up')
            self.selectedMc = None
            self.selectedKey = 0
        self.selectedKey = e.currentTarget.key
        self.selectedMc = e.currentTarget
        e.currentTarget.gotoAndStop('down')
