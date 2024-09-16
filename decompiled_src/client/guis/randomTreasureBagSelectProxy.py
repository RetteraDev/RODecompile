#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/randomTreasureBagSelectProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import sMath
import math
import utils
import const
import clientUtils
import ui
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis import uiUtils
from callbackHelper import Functor
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import random_treasure_bag_lottery_data as RTBLD
from data import random_treasure_bag_lottery_group_data as RTBLGD
GROUP_ITEM_NUMS = 7
ALL_ITEM_NUMS_LIMIT = 9
ITEM_SELECT_BG_Y = 24
ITEM_SELECT_BG_HEIGHT_OFFSET = 7
ITEM_SELECT_HEIGHT = 108
ITEM_SELECT_WIDTH = 80
ITEM_SELECT_LEFT_OFFSET = 9
ITEM_SELECT_UP_OFFSET = 9
ITEM_SELECT_DOWN_OFFSET = 10
ITEM_SELECT_WIDTH_OFFSET = 5
ITEM_SELECT_HEIGHT_OFFSET = 8

class RandomTreasureBagSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RandomTreasureBagSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.bagId = 1
        self.allSelectData = {}
        self.groupIdList = []
        self.bagStaticDataDict = {}
        self.bagServerDataDict = {}
        self.checkCanRefreshListType = True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANDOM_TREASURE_BAG_SELECT:
            self.widget = widget
            self.initAll()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANDOM_TREASURE_BAG_SELECT)

    def show(self, bagId):
        if not gameglobal.rds.configData.get('enableRandomTreasureBagMain', False):
            return
        self.bagId = bagId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANDOM_TREASURE_BAG_SELECT)
        else:
            self.initAll()

    def initAll(self):
        self.initData()
        self.initUI()
        self.refreshUI()

    def initData(self):
        self.bagStaticDataDict = gameglobal.rds.ui.randomTreasureBagMain.getBagDataById(self.bagId)
        self.bagServerDataDict = gameglobal.rds.ui.randomTreasureBagMain.getBagServerDataById(self.bagId)
        if 'randomLotteryItemsHistory' in self.bagServerDataDict and self.bagServerDataDict['randomLotteryItemsHistory']:
            self.allSelectData = self.processServerData(self.bagServerDataDict['randomLotteryItemsHistory'])
        else:
            self.allSelectData = self.processStaticData(self.bagStaticDataDict['presetGroupItemDataDict'])
        self.groupIdList = self.bagStaticDataDict['groupIdList']

    def initUI(self):
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmClick, False, 0, True)
        self.widget.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearClick, False, 0, True)

    def refreshUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshList()
        self.refreshBtn()

    def refreshBtn(self):
        self.widget.clearBtn.enabled = self.checkCanClear()

    def checkCanRefreshList(self):
        if self.checkCanRefreshListType:
            self.refreshList()

    def refreshList(self):
        self.checkCanRefreshListType = False
        self.removeUIAllChild(self.widget.mainList.canvas)
        posY = 0
        for groupId in self.groupIdList:
            groupData = self.getGroupData(int(groupId))
            itemIdsData = groupData.get('itemIds', {})
            titleMc = self.widget.getInstByClsName('RandomTreasureBagSelect_itemSelectTitle')
            self.widget.mainList.canvas.addChild(titleMc)
            titleMc.title.htmlText = gameStrings.RANDOM_TREASURE_BAG_SELECT_ITEM_TITLE % (groupData.get('desc', ''), self.getCurGroupReqSelectNums(groupId))
            titleMc.y = posY
            titleMc.x = 0
            itemSelectBgMc = self.widget.getInstByClsName('RandomTreasureBagSelect_itemSelectBg')
            self.widget.mainList.canvas.addChild(itemSelectBgMc)
            itemSelectBgMc.y = titleMc.y + ITEM_SELECT_BG_Y
            itemSelectBgMc.x = 0
            allItemNums = len(itemIdsData)
            itemLineNums = math.ceil(allItemNums * 1.0 / GROUP_ITEM_NUMS)
            itemSelectBgMc.height = itemLineNums * (ITEM_SELECT_HEIGHT + ITEM_SELECT_UP_OFFSET) + ITEM_SELECT_DOWN_OFFSET
            curItemMcIdx = 0
            curItemMcLine = 1
            for itemId, value in itemIdsData.iteritems():
                groupItemMc = self.widget.getInstByClsName('RandomTreasureBagSelect_itemSelect')
                self.widget.mainList.canvas.addChild(groupItemMc)
                curItemMcIdx = curItemMcIdx % GROUP_ITEM_NUMS
                groupItemMc.x = ITEM_SELECT_LEFT_OFFSET + curItemMcIdx * (ITEM_SELECT_WIDTH + ITEM_SELECT_WIDTH_OFFSET)
                groupItemMc.y = itemSelectBgMc.y + ITEM_SELECT_UP_OFFSET + (curItemMcLine - 1) * (ITEM_SELECT_HEIGHT + ITEM_SELECT_HEIGHT_OFFSET)
                curItemMcIdx += 1
                if curItemMcIdx == GROUP_ITEM_NUMS:
                    curItemMcLine += 1
                self.setItemSelectMc(groupItemMc, itemId, value, groupId)

            posY = itemSelectBgMc.y + itemSelectBgMc.height + ITEM_SELECT_BG_HEIGHT_OFFSET

        self.widget.mainList.validateNow()
        self.widget.mainList.refreshHeight(posY)
        self.checkCanRefreshListType = True

    def setItemSelectMc(self, itemMc, itemId, value, groupId):
        itemMc.visible = True
        isRare = gameglobal.rds.ui.randomTreasureBagMain.checkItemIsRare(itemId, value[0], bagId=self.bagId)
        gameglobal.rds.ui.randomTreasureBagMain.setRewardItemMc(itemMc.item, itemId, iconSize=uiConst.ICON_SIZE110, itemNums=value[0], isRare=isRare)
        itemMc.numStepper.enableMouseWheel = False
        itemMc.numStepper.maxCount = value[1]
        itemMc.numStepper.minCount = 0
        itemMc.numStepper.itemId = itemId
        itemMc.numStepper.groupId = groupId
        itemMc.numStepper.numInput.mouseChildren = False
        itemMc.numStepper.numInput.editable = False
        itemMc.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.itemCountChange, False, 0, True)
        if groupId in self.allSelectData and itemId in self.allSelectData[groupId]:
            itemMc.numStepper.count = self.allSelectData[groupId][itemId]
            itemMc.itemSelected.visible = True
            itemMc.itemSelectedBg.visible = True
        else:
            itemMc.numStepper.count = 0
            itemMc.itemSelected.visible = False
            itemMc.itemSelectedBg.visible = False
        if self.getCurSelectItemNums() == ALL_ITEM_NUMS_LIMIT:
            itemMc.numStepper.nextBtn.enabled = False
        if self.getCurGroupReqSelectNums(groupId) == self.getCurGroupSelectItemNums(groupId):
            itemMc.numStepper.nextBtn.enabled = False

    def itemCountChange(self, *args):
        numStepper = ASObject(args[3][0]).currentTarget
        itemId = int(numStepper.itemId)
        groupId = int(numStepper.groupId)
        count = int(numStepper.count)
        lastItemNums = self.getCurSelectItemNums()
        if groupId not in self.allSelectData:
            self.allSelectData[groupId] = {}
        if count > 0:
            self.allSelectData[groupId][itemId] = count
            numStepper.parent.itemSelected.visible = True
            numStepper.parent.itemSelectedBg.visible = True
        else:
            numStepper.parent.itemSelected.visible = False
            numStepper.parent.itemSelectedBg.visible = False
            if itemId in self.allSelectData[groupId]:
                self.allSelectData[groupId].pop(itemId)
            if not self.allSelectData[groupId]:
                self.allSelectData.pop(groupId)
        curItemNums = self.getCurSelectItemNums()
        if curItemNums == ALL_ITEM_NUMS_LIMIT or lastItemNums == ALL_ITEM_NUMS_LIMIT and curItemNums == ALL_ITEM_NUMS_LIMIT - 1:
            self.checkCanRefreshList()
            return
        if self.getCurGroupSelectItemNums(groupId) == self.getCurGroupReqSelectNums(groupId) or self.getCurGroupSelectItemNums(groupId) == self.getCurGroupReqSelectNums(groupId) - 1:
            self.checkCanRefreshList()

    def processServerData(self, serverDataDict):
        allGroupDataDict = dict()
        for groupId, valueList in serverDataDict.iteritems():
            itemDict = dict()
            for value in valueList:
                if value[0] in itemDict:
                    itemDict[value[0]] += 1
                else:
                    itemDict[value[0]] = 1

            allGroupDataDict[groupId] = itemDict

        return allGroupDataDict

    def processStaticData(self, staticDataDict):
        allGroupDataDict = dict()
        for groupId, valueList in staticDataDict.iteritems():
            itemDict = dict()
            for value in valueList:
                if value in itemDict:
                    itemDict[value] += 1
                else:
                    itemDict[value] = 1

            allGroupDataDict[groupId] = itemDict

        return allGroupDataDict

    def getGroupData(self, groupId):
        return RTBLGD.data.get(groupId, {})

    def getCurSelectItemNums(self):
        result = 0
        for itemDict in self.allSelectData.itervalues():
            for itemNums in itemDict.itervalues():
                result += itemNums

        return result

    def getCurGroupSelectItemNums(self, groupId):
        result = 0
        itemDict = self.allSelectData.get(groupId, {})
        for itemNums in itemDict.itervalues():
            result += itemNums

        return result

    def getCurGroupReqSelectNums(self, groupId):
        requireSelectNum = self.getGroupData(groupId).get('requireSelectNum', 0)
        return requireSelectNum

    def checkCanConfirm(self):
        p = BigWorld.player()
        if self.getCurSelectItemNums() != ALL_ITEM_NUMS_LIMIT:
            p.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_SELECT_CONFIRM_REQUIRE_FAIL, ())
            return False
        for groupId in self.groupIdList:
            requireSelectNum = self.getCurGroupReqSelectNums(groupId)
            curSelectNum = 0
            if groupId in self.allSelectData:
                curSelectNum = self.getCurGroupSelectItemNums(groupId)
            if curSelectNum < requireSelectNum:
                p.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_SELECT_CONFIRM_REQUIRE_FAIL, ())
                return False

        return True

    def checkCanClear(self):
        if not self.allSelectData:
            return False
        return True

    def handleConfirmClick(self, *args):
        if self.checkCanConfirm():
            gameglobal.rds.ui.randomTreasureBagMain.addGroupItemData(self.bagId, self.allSelectData)
            self.hide()

    def handleClearClick(self, *args):
        self.allSelectData.clear()
        self.checkCanRefreshList()

    def removeUIAllChild(self, itemMc):
        while itemMc.numChildren > 0:
            itemMc.removeChildAt(0)
