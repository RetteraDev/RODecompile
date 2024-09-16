#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/optionalRewardBoxProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis.asObject import ASObject
from data import optional_bonus_data as OBD
from data import consumable_item_data as CID

class OptionalRewardBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(OptionalRewardBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_OPTIONAL_REWARD_BOX, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_OPTIONAL_REWARD_BOX:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_OPTIONAL_REWARD_BOX)

    def reset(self):
        self.opNUID = 0
        self.optionId = 0
        self.selectItemMc = None
        self.nPage = 0
        self.nPos = 0
        self.maxNum = 1
        self.itemId = 0

    def showMulti(self, itemId, nPage = 0, nPos = 0):
        p = BigWorld.player()
        self.itemId = itemId
        boxItem = p.inv.getQuickVal(nPage, nPos)
        maxNum = boxItem.cwrap
        optionId = CID.data.get(itemId, {}).get('optionId', 0)
        self.show(0, optionId, nPage, nPos, maxNum)

    def show(self, opNUID, optionId, nPage = 0, nPos = 0, maxNum = 1):
        self.opNUID = opNUID
        self.optionId = optionId
        self.nPage = nPage
        self.nPos = nPos
        self.maxNum = maxNum
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_OPTIONAL_REWARD_BOX)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.getedRewardMc.visible = False
        self.widget.optionalMc.visible = True
        obdData = OBD.data.get(self.optionId, {})
        icons = obdData.get('iconId', [])
        self.widget.optionalMc.gotoAndStop('type%d' % len(icons))
        for i in xrange(len(icons)):
            itemMc = self.widget.optionalMc.rewardMc.getChildByName('item%d' % i)
            if self.opNUID:
                itemMc.item.gotoAndStop('normal')
            else:
                itemMc.item.gotoAndStop('multi')
                itemMc.item.counter.maxCount = self.maxNum
                itemMc.item.counter.minCount = 1
                itemMc.item.maxBtn.addEventListener(events.BUTTON_CLICK, self.onMaxBtnClick)
            rewards = icons[i]
            for j in xrange(6):
                slot = itemMc.item.getChildByName('slot%d' % j)
                if j < len(rewards):
                    slot.visible = True
                    itemId = rewards[j]
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    slot.fitSize = True
                    slot.dragable = False
                    slot.setItemSlotData(itemInfo)
                else:
                    slot.visible = False

            itemMc.item.selectBtn.rewardIndex = i
            itemMc.item.selectBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectBtnClick, False, 0, True)
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemMcClick, False, 0, True)
            itemMc.item.selectIcon.visible = False

    def onMaxBtnClick(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.parent.counter.count = self.maxNum

    def handleItemMcClick(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if self.selectItemMc:
            self.selectItemMc.item.selectIcon.visible = False
        itemMc.item.selectIcon.visible = True
        self.selectItemMc = itemMc

    def handleSelectBtnClick(self, *args):
        selectBtn = ASObject(args[3][0]).currentTarget
        p = BigWorld.player()
        if self.opNUID:
            p.base.genOptionalBonusItem(self.opNUID, selectBtn.rewardIndex)
        else:
            count = selectBtn.parent.counter.count
            p.cell.useCommonItemWithParamNew(self.nPage, self.nPos, count, 'index', selectBtn.rewardIndex)
            BigWorld.callback(0.1, self.hide)

    def handleQuitBtnClick(self, *args):
        self.hide()

    def getedOptionalRewards(self, rewardItems):
        if not self.widget:
            return
        self.widget.getedRewardMc.visible = True
        self.widget.optionalMc.visible = False
        items = {}
        for i in xrange(len(rewardItems)):
            itemId = rewardItems[i][1]
            itemNum = rewardItems[i][2]
            if items.has_key(itemId):
                items[itemId] += itemNum
            else:
                items[itemId] = itemNum

        self.widget.getedRewardMc.slotMc.gotoAndStop('type%d' % len(items))
        i = 0
        for itemId in items:
            slot = self.widget.getedRewardMc.slotMc.getChildByName('slot%d' % i)
            itemNum = items[itemId]
            itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
            slot.fitSize = True
            slot.dragable = False
            slot.setItemSlotData(itemInfo)
            i += 1

        self.widget.getedRewardMc.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)
