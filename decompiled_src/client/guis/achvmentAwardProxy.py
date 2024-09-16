#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentAwardProxy.o
import gameglobal
import clientUtils
from guis import events
from guis import uiUtils
from guis import uiConst
from gamestrings import gameStrings
from guis.asObject import ASObject
from uiProxy import UIProxy
from item import Item
from data import item_data as ID
from data import achieve_bonus_filter_data as ABFD
COLUMN_NUM = 8
ITEMID_IDX = 0
ACHIEVE_FLAG_IDX = 1
ITEM_NUM_IDX = 0
ITEM_ACHIEVEIDS_IDX = 1
KEYCODE_CTRL = 17

class AchvmentAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentAwardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.searchInfo = {}
        self.reset()

    def reset(self):
        self.achieves = {}
        self.itemIds = []
        self.itemAchieveInfo = {}
        self.itemUnAchieveInfo = {}

    def clearAll(self):
        self.searchInfo = {}

    def initPanel(self, widget):
        self.widget = widget.mainMc
        self.isCtrlPressed = False
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleKeyEvent, False, 0, True)
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyEvent, False, 0, True)
        self.initData()
        self.initListProp()
        self.refreshInfo()
        self.widget.searchTextInput.addEventListener(events.EVENT_CHANGE, self.onSearchChange)

    def unRegisterPanel(self):
        self.widget = None

    def initData(self):
        if not self.itemIds:
            self.achieves = gameglobal.rds.ui.achvment.achieves
            for achieveId, info in ABFD.data.iteritems():
                if self.uiAdapter.achvment.isHideAchieve(achieveId):
                    continue
                destlist = self.itemAchieveInfo if achieveId in self.achieves else self.itemUnAchieveInfo
                itemInfos = clientUtils.genItemBonus(info.get('bonusId', 0))
                for itemId, num in itemInfos:
                    itemNum, achieveIds = destlist.get(itemId, (0, []))
                    achieveIds.append(achieveId)
                    destlist[itemId] = (itemNum + num, achieveIds)

            itemIds1 = [ [itemId, True] for itemId in self.itemAchieveInfo ]
            itemIds1 = sorted(itemIds1, self.compare)
            itemIds2 = [ [itemId, False] for itemId in self.itemUnAchieveInfo ]
            itemIds2 = sorted(itemIds2, self.compare)
            self.itemIds = itemIds1
            self.itemIds.extend(itemIds2)
        if not self.searchInfo:
            self.searchInfo = {ID.data.get(listItem[0], {}).get('name', ''):listItem for listItem in self.itemIds}

    def compare(self, id1, id2):
        quality1 = ID.data.get(id1[ITEMID_IDX], {}).get('quality', 0)
        quality2 = ID.data.get(id2[ITEMID_IDX], {}).get('quality', 0)
        if quality1 == quality2:
            return cmp(id1[ITEMID_IDX], id2[ITEMID_IDX])
        return cmp(quality2, quality1)

    def initListProp(self):
        self.widget.listView.column = COLUMN_NUM
        self.widget.listView.itemWidth = 100
        self.widget.listView.itemHeight = 108
        self.widget.listView.itemRenderer = 'AchvmentAwardPanel_SlotItem'
        self.widget.listView.labelFunction = self.itemLabelFunc

    def refreshInfo(self):
        self.refreshCompleteness()
        if self.widget.searchTextInput.text:
            self.refreshSearchResult(self.widget.searchTextInput.text)
        else:
            self.refreshList(self.itemIds)

    def refreshSearchResult(self, searchText):
        retIds = [ self.searchInfo[name] for name in self.searchInfo if uiUtils.isContainString(name, searchText) ]
        if self.widget.listView.dataArray != retIds:
            self.refreshList(retIds)

    def refreshCompleteness(self):
        maxVal = len(self.itemAchieveInfo) + len(self.itemUnAchieveInfo)
        achieveVal = len(self.itemAchieveInfo)
        self.widget.completenessTf.text = gameStrings.ACHIEVE_ITEM_COMPLETE_TEXT % (achieveVal, maxVal)

    def refreshList(self, listData):
        self.widget.searchResultTf.visible = not listData
        self.widget.listView.dataArray = listData
        self.widget.listView.validateNow()

    def itemLabelFunc(self, *args):
        item = ASObject(args[3][1])
        itemInfo = ASObject(args[3][0])
        item.itemInfo = itemInfo
        itemId = itemInfo[ITEMID_IDX]
        flag = itemInfo[ACHIEVE_FLAG_IDX]
        state = uiConst.ITEM_NORMAL if flag else uiConst.ITEM_GRAY
        if ID.data.get(itemId, {}).get('achieveItemCntHide'):
            item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, appendInfo={'state': state,
             'srcType': 'achevment'}))
        else:
            destInfo = self.itemAchieveInfo if flag else self.itemUnAchieveInfo
            num = destInfo.get(itemId, (0, []))[ITEM_NUM_IDX]
            item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, num, appendInfo={'state': state,
             'srcType': 'achevment'}))
        item.slot.dragable = False
        item.itemNameTf.text = ID.data.get(itemId, {}).get('name', '')
        item.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)

    def onItemClick(self, *args):
        itemInfo = ASObject(args[3][0]).currentTarget.itemInfo
        itemId = itemInfo[ITEMID_IDX]
        if self.isCtrlPressed:
            item = Item(itemId)
            if item.isEquip():
                gameglobal.rds.ui.fittingRoom.addItem(item)
                return
        achieveIds = []
        if itemId in self.itemAchieveInfo:
            achieveIds.extend(self.itemAchieveInfo[itemId][ITEM_ACHIEVEIDS_IDX])
        if itemId in self.itemUnAchieveInfo:
            achieveIds.extend(self.itemUnAchieveInfo[itemId][ITEM_ACHIEVEIDS_IDX])
        gameglobal.rds.ui.achvment.link2AchvmentDetailView(linkData=achieveIds)

    def onSearchChange(self, *args):
        e = ASObject(args[3][0])
        if e.target != self.widget.searchTextInput:
            return
        text = e.currentTarget.text
        if text:
            self.refreshSearchResult(text)
        else:
            self.refreshList(self.itemIds)

    def handleKeyEvent(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == KEYCODE_CTRL:
            self.isCtrlPressed = e.type == events.KEYBOARD_EVENT_KEY_DOWN
