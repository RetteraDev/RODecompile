#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankingAwardCommonProxy.o
import BigWorld
import gameglobal
import gamelog
import uiConst
import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import uiUtils

class RankingAwardCommonProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankingAwardCommonProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.selectItem = None
        self.awardData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANKINGAWARD_COMMON, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANKINGAWARD_COMMON:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.selectItem = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANKINGAWARD_COMMON)
        self.awardData = {}

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANKINGAWARD_COMMON)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshData()

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def showAwardCommon(self, data):
        gamelog.debug('ypc@showAwardCommon data = ', data)
        self.awardData = data
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKINGAWARD_COMMON)
        else:
            self.refreshData()

    def refreshData(self):
        if not self.widget or not self.awardData:
            return
        self.widget.title.text = self.awardData['title']
        self.widget.rule.text = self.awardData['rule']
        self.widget.list.itemRenderer = 'RankAward_ListItem'
        self.widget.list.lableFunction = self.lableFunction
        self.widget.list.dataArray = self.awardData['list']

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.indexlbl.lbl.text = str(itemMc.index + 1)
        itemMc.rank.text = itemData.rank
        itemMc.title.text = itemData.title
        itemMc.titleEmpty.visible = itemData.title == ''
        itemMc.x = -5
        for i in range(0, 3):
            itemId = getattr(itemData, 'item%d' % i)
            itemNum = getattr(itemData, 'itemNum%d' % i)
            icon = itemMc.getChildByName('item%d' % i)
            icon.slot.dragable = False
            emptytxt = itemMc.getChildByName('empty%d' % i)
            if itemId == -1:
                emptytxt.visible = True
                icon.visible = False
            else:
                itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
                icon.slot.setItemSlotData(itemInfo)
                icon.visible = True
                emptytxt.visible = False

        itemMc.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)

    def onItemClick(self, *args):
        if not self.widget:
            return
        else:
            e = ASObject(args[3][0])
            if self.selectItem:
                self.selectItem.gotoAndStop('up')
            if e and e.gotoAndStop:
                self.selectItem = e
                self.selectItem.gotoAndStop('down')
            else:
                self.selectItem = None
            return
