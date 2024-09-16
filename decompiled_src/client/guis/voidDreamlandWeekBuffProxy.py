#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandWeekBuffProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from cdata import endless_challenge_weekly_buff_reverse_data as ECWBRD

class VoidDreamlandWeekBuffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandWeekBuffProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rank = None
        self.weeklyInterval = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_WEEK_BUFF, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_WEEK_BUFF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, rank, weeklyInterval):
        self.rank = rank
        self.weeklyInterval = weeklyInterval
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_WEEK_BUFF)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_WEEK_BUFF)

    def reset(self):
        self.rank = None
        self.weeklyInterval = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'VoidDreamlandWeekBuff_weekBuffItem'
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.lableFunction = self.itemFunction
        self.widget.scrollWndList.itemHeight = 35

    def _onSureBtnClick(self, e):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        indexPosY = 0
        itemList = []
        weekData = ECWBRD.data.get(self.rank, {})
        for idx, key in enumerate(sorted(weekData.keys())):
            weekDesc = weekData.get(key, {}).get('desc', '')
            weekText = weekData.get(key, {}).get('name', '')
            itemInfo = {}
            itemInfo['index'] = idx
            itemInfo['weekText'] = weekText
            itemInfo['weekDesc'] = weekDesc
            itemInfo['bright'] = False
            if key == self.weeklyInterval:
                itemInfo['bright'] = True
                indexPosY = idx
            itemList.append(itemInfo)

        self.widget.scrollWndList.dataArray = itemList
        self.widget.scrollWndList.validateNow()
        pos = self.widget.scrollWndList.getIndexPosY(indexPosY)
        self.widget.scrollWndList.scrollTo(pos)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.bright:
            itemMc.weekBuffBright.visible = True
            itemMc.weekBuffDark.visible = False
            weekBuffItem = itemMc.weekBuffBright
        else:
            itemMc.weekBuffBright.visible = False
            itemMc.weekBuffDark.visible = True
            weekBuffItem = itemMc.weekBuffDark
        weekBuffItem.weekText.text = itemData.weekText
        weekBuffItem.weekDesc.text = itemData.weekDesc
