#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mysteryAnimalProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import ASObject
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class MysteryAnimalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MysteryAnimalProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MYSTERY_ANIMAL, self.hide)

    def reset(self):
        self.itemData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MYSTERY_ANIMAL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MYSTERY_ANIMAL)

    def show(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableExchangeMysteryAnimal', False):
            p.showGameMsg(GMDD.data.MYSTERY_ANIMAL_NOT_OPEN, ())
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MYSTERY_ANIMAL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if not gameglobal.rds.configData.get('enableExchangeMysteryBox', False):
            self.setTab(2)
            self.widget.tab1.visible = False
            self.widget.tab2.visible = False
            self.widget.tab2.x = self.widget.tab1.x
        else:
            self.setTab(1)
            self.widget.tab1.visible = True
            self.widget.tab2.x = 265
        self.widget.boxNode.numNode.count = 1
        self.widget.boxNode.numNode.minCount = 0
        self.widget.boxNode.numNode.maxCount = 50
        self.widget.helpBtn.visible = False
        self.widget.boxNode.numNode.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange, False, 0, True)
        self.widget.tab1.addEventListener(events.MOUSE_CLICK, self.handleTabClick, False, 0, True)
        self.widget.tab2.addEventListener(events.MOUSE_CLICK, self.handleTabClick, False, 0, True)
        self.widget.boxNode.okBtn.addEventListener(events.MOUSE_CLICK, self.handleOkClick1, False, 0, True)
        self.widget.animalNode.okBtn.addEventListener(events.MOUSE_CLICK, self.handleOkClick2, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleTabClick(self, *args):
        e = ASObject(args[3][0])
        name = e.currentTarget.name
        self.setTab(int(name[-1]))

    def handleOkClick1(self, *args):
        if not gameglobal.rds.configData.get('enableExchangeMysteryBox', False):
            return
        p = BigWorld.player()
        itemId, rewardId, consumeNum = self.getItemAndRewardByIndex(1)
        if itemId == 0:
            return
        count = p.inv.countItemInPages(itemId, enableParentCheck=True, includeLatch=True)
        num = int(self.widget.boxNode.numNode.count)
        if num == -1:
            num = 1
        if count < consumeNum * num:
            p.showGameMsg(GMDD.data.MYSTERY_BOX_FRAG_NOT_ENOUGH, ())
        else:
            p.cell.exchangeMysteryAnimal(rewardId, num)

    def handleOkClick2(self, *args):
        if not gameglobal.rds.configData.get('enableExchangeMysteryAnimal', False):
            return
        p = BigWorld.player()
        itemId, rewardId, consumeNum = self.getItemAndRewardByIndex(2)
        if itemId == 0:
            return
        unBindCount = p.inv.countItemInPages(itemId, gametypes.ITEM_REMOVE_POLICY_UNBIND_ONLY, enableParentCheck=True)
        allCount = p.inv.countItemInPages(itemId, enableParentCheck=True, includeLatch=True)
        if unBindCount < consumeNum and allCount >= consumeNum:
            msg = gameStrings.MYSTERY_ANIMAL_UNBIND_ITEM_LESS
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realExchange, rewardId))
        elif allCount < consumeNum:
            p.showGameMsg(GMDD.data.MYSTERY_ANIMAL_FRAG_NOT_ENOUGH, ())
        else:
            self.realExchange(rewardId)

    def realExchange(self, rewardId):
        p = BigWorld.player()
        p.cell.exchangeMysteryAnimal(rewardId, 1)

    def setTab(self, index):
        if index == 1:
            self.widget.tab1.selected = True
            self.widget.tab2.selected = False
            self.widget.boxNode.visible = True
            self.widget.animalNode.visible = False
        elif index == 2:
            self.widget.tab1.selected = False
            self.widget.tab2.selected = True
            self.widget.boxNode.visible = False
            self.widget.animalNode.visible = True
        self.initPanel(index)

    def initPanel(self, index):
        self.index = index
        image1 = getattr(self.widget, 'image1')
        image2 = getattr(self.widget, 'image2')
        p = BigWorld.player()
        itemId, rewardId, consumeNum = self.getItemAndRewardByIndex(index)
        count = p.inv.countItemInPages(itemId, enableParentCheck=True, includeLatch=True)
        if index == 1:
            image1.visible = True
            image2.visible = False
            num = int(self.widget.boxNode.numNode.count)
            if num == -1:
                num = 1
            if count < consumeNum * num or count == 0:
                color = '#E51717'
            else:
                color = '#CEDDE1'
            info = uiUtils.getGfxItemById(itemId, uiUtils.toHtml(str(count) + '/' + str(consumeNum * num), color))
            self.widget.boxNode.fragItem.setItemSlotData(info)
            self.widget.boxNode.fragItem.validateNow()
            self.widget.boxNode.fragItem.dragable = False
            itemLen = len(SCD.data.get('mysteryAnimalRewardList'))
            for i in range(4):
                itemNode = getattr(self.widget.boxNode, 'item' + str(i + 1))
                itemNode.dragable = False
                if i + 1 <= itemLen:
                    itemNode.visible = True
                    itemNode.setItemSlotData(uiUtils.getGfxItemById(SCD.data.get('mysteryAnimalRewardList')[i]))
                else:
                    itemNode.visible = False

        elif index == 2:
            image1.visible = False
            image2.visible = True
            if count < consumeNum or count == 0:
                color = '#E51717'
            else:
                color = '#CEDDE1'
            self.widget.animalNode.fragItem.setItemSlotData(uiUtils.getGfxItemById(itemId, uiUtils.toHtml(str(count) + '/' + str(consumeNum), color)))
            self.widget.animalNode.fragItem.validateNow()
            self.widget.animalNode.fragItem.dragable = False

    def handleCounterChange(self, *args):
        self.initPanel(1)

    def getItemAndRewardByIndex(self, index):
        itemsForExchangeMysteryAnimal = SCD.data.get('itemsForExchangeMysteryAnimal', [])
        if not itemsForExchangeMysteryAnimal:
            return (0, 0, 0)
        itemId = itemsForExchangeMysteryAnimal[index - 1][1]['itemId']
        consumeNum = itemsForExchangeMysteryAnimal[index - 1][1]['itemNum']
        rewardId = itemsForExchangeMysteryAnimal[index - 1][0]
        return (itemId, rewardId, consumeNum)

    def refreshPanel(self):
        self.initPanel(self.index or 1)
