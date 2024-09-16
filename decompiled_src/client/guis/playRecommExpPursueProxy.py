#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommExpPursueProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gameglobal
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import events
from data import item_data as ID
from data import sys_config_data as SCD
from data import exp_pursue_guide_data as EPGD
TYPE1_ITEMNUM = 2

class PlayRecommExpPursueProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommExpPursueProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showList = []

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        self.requestData()

    def requestData(self):
        p = BigWorld.player()
        p.cell.getExpPursueGuide()

    def onGetExpPursueData(self, showList):
        self.showList = showList
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.mallItemsMc.itemList.itemRenderer = 'PlayRecommExpPursue_mallItem'
        self.widget.mallItemsMc.itemList.labelFunction = self.mallItemLabelFunction
        self.widget.contentList.itemRenderer = 'PlayRecommExpPursue_contentItem'
        self.widget.contentList.labelFunction = self.contentLabelFunction
        self.widget.contentList.itemHeightFunction = self.contentHeightFunction

    def mallItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemId = itemData.itemId
        self.setItemMcInfo(itemMc, itemId)

    def contentHeightFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemHeight = 158
        if itemData.type == 1:
            itemHeight = 210
        elif itemData.type == 0:
            itemHeight = 158
        return GfxValue(itemHeight)

    def getIconPath(self, iconId):
        return 'item/icon64/' + str(iconId) + '.dds'

    def contentLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.type == 1:
            itemMc.gotoAndStop('type1')
            itemMc.title.text = itemData.name
            itemMc.desc.htmlText = itemData.desc
            itemList = itemData.itemList
            if not itemList:
                itemList = []
            for i in xrange(TYPE1_ITEMNUM):
                itemItemMc = itemMc.getChildByName('item%d' % i)
                if i < len(itemList):
                    itemItemMc.visible = True
                    self.setItemMcInfo(itemItemMc, itemList[i])
                else:
                    itemItemMc.visible = False

            if itemData.seekId:
                itemMc.goBtn.visible = True
                itemMc.goBtn.seekId = itemData.seekId
                itemMc.goBtn.addEventListener(events.BUTTON_CLICK, self.onGoBtnItemClick)
            else:
                itemMc.goBtn.visible = False
            itemMc.icon.fitSize = True
            itemMc.icon.loadImage(self.getIconPath(itemData.iconId))
        elif itemData.type == 0:
            itemMc.gotoAndStop('type2')
            itemMc.title.text = itemData.name
            itemMc.desc.htmlText = itemData.desc
            if itemData.seekId:
                itemMc.goBtn.visible = True
                itemMc.goBtn.seekId = itemData.seekId
                itemMc.goBtn.addEventListener(events.BUTTON_CLICK, self.onGoBtnItemClick)
            else:
                itemMc.goBtn.visible = False
            itemMc.icon.fitSize = True
            itemMc.icon.loadImage(self.getIconPath(itemData.iconId))

    def onGoBtnItemClick(self, *args):
        e = ASObject(args[3][0])
        seekId = e.currentTarget.seekId
        uiUtils.findPosWithAlert(seekId)

    def setItemMcInfo(self, mc, itemId):
        itemInfo = uiUtils.getGfxItemById(itemId, 1)
        mc.slot.setItemSlotData(itemInfo)
        itemName = ID.data.get(itemId, '').get('name', '')
        mc.itemName.text = itemName
        mc.buyBtn.itemName = itemName
        mc.buyBtn.addEventListener(events.BUTTON_CLICK, self.onBuyBtnClick)

    def onBuyBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemName = e.currentTarget.itemName
        gameglobal.rds.ui.tianyuMall.showMallTab(0, 0, itemName)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshExpInfo()
        self.refreshBuyItems()
        self.refreshContent()

    def refreshExpInfo(self):
        p = BigWorld.player()
        self.widget.expMc.expPoint.text = getattr(p, 'xiuweiLevel', 0)
        expAddParamBuffVal = getattr(p, 'expAddParamBuffVal', 0)
        if gameglobal.rds.configData.get('enableServerExpAddNew', True):
            serverExpAddParam = expAddParamBuffVal - 100
        else:
            serverExpAddParam = expAddParamBuffVal
        self.widget.expMc.expRate.text = '%d%%' % serverExpAddParam

    def refreshContent(self):
        contents = []
        for contentIdx in self.showList:
            contents.append(EPGD.data.get(contentIdx, {}))

        contents.sort(cmp=self.conentCmp)
        self.widget.contentList.dataArray = contents

    def conentCmp(self, a, b):
        return a.get('order', 0) - b.get('order', 0)

    def refreshBuyItems(self):
        mallItems = SCD.data.get('expPursueGuideItems', [])
        items = []
        for itemId in mallItems:
            items.append({'itemId': itemId})

        self.widget.mallItemsMc.itemList.dataArray = items
