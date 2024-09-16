#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceSkinSettingProxy.o
import BigWorld
import gameglobal
import utils
import events
import keys
from guis.uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from data import personal_zone_skin_data as PZSD
ITEM_NUM_PER_PAGE = 2

class SpaceSkinSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpaceSkinSettingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACE_SKIN_SETTING, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPACE_SKIN_SETTING:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACE_SKIN_SETTING)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACE_SKIN_SETTING)

    def reset(self):
        self.curPage = 0
        self.totalPage = 0
        self.pageData = []
        self.selectedItem = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        for k, v in PZSD.data.iteritems():
            v['id'] = k
            self.pageData.append(v)

        self.totalPage = self.getPageNum(len(self.pageData))

    def getPageNum(self, length):
        pageNum = length / ITEM_NUM_PER_PAGE
        pageNum = pageNum + 1 if length % ITEM_NUM_PER_PAGE else pageNum
        return pageNum

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setDropdownMenuData(self.widget.page, [ '%d/%d' % (x, self.totalPage) for x in xrange(1, self.totalPage + 1) ])
        self.widget.page.addEventListener(events.INDEX_CHANGE, self.onSelectedOption, False, 0, True)
        for i in xrange(0, ITEM_NUM_PER_PAGE):
            item = getattr(self.widget, 'item' + str(i), None)
            if item:
                item.addEventListener(events.BUTTON_CLICK, self.onItemClick, False, 0, True)

        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            self.selectedItem = None
            p = BigWorld.player()
            infoList = self.getCurPageItemInfo()
            for i in xrange(0, ITEM_NUM_PER_PAGE):
                item = getattr(self.widget, 'item' + str(i), None)
                info = {}
                if i < len(infoList):
                    info = infoList[i]
                if item:
                    if info:
                        item.visible = True
                        item.skinId = info.get('id', 0)
                        if self.getCurSelId() == item.skinId:
                            self.setSelectedItem(item)
                        else:
                            item.selected = False
                        gfxItem = uiUtils.getGfxItemById(info.get('itemId', 0))
                        item.icon.setItemSlotData(gfxItem)
                        item.useless.visible = False if item.skinId in p.personalZoneSkin else True
                        if item.useless.visible:
                            item.icon.setSlotState(2)
                            item.disabled = True
                        else:
                            item.icon.setSlotState(1)
                            item.disabled = False
                        skinId = info.get('id', 0)
                        skinVal = p.personalZoneSkin.get(skinId)
                        if skinVal:
                            if skinVal.expireTime:
                                vilidTime = utils.formatDatetime(skinVal.expireTime)
                                item.desc.htmlText = gameStrings.PERSONAL_ZONE_SKIN_VILIDDATE % vilidTime
                                item.desc.visible = True
                            else:
                                item.desc.visible = False
                        else:
                            item.desc.visible = False
                        item.newIcon.visible = info.get('isNew', 0)
                        item.nameText.htmlText = info.get('name', '')
                        TipManager.addItemTipById(item, info.get('itemId', 0))
                    else:
                        item.visible = False

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def onSelectedOption(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        if self.hasBaseData():
            self.refreshInfo()

    def getCurPageItemInfo(self):
        curPage = self.widget.page.selectedIndex
        infoList = self.pageData[curPage * ITEM_NUM_PER_PAGE:curPage * ITEM_NUM_PER_PAGE + ITEM_NUM_PER_PAGE]
        return infoList

    def onItemClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        if t.skinId:
            p = BigWorld.player()
            p.base.setPersonalZoneSkin(t.skinId)

    def setSelectedItem(self, selItem):
        if self.hasBaseData():
            if self.selectedItem:
                self.selectedItem.selected = False
            self.selectedItem = selItem
            self.selectedItem.selected = True

    def setSelectedItemBySkinId(self, sId):
        if self.hasBaseData():
            for i in xrange(0, ITEM_NUM_PER_PAGE):
                item = getattr(self.widget, 'item' + str(i), None)
                if item:
                    if self.getCurSelId() == item.skinId:
                        self.setSelectedItem(item)
                    else:
                        item.selected = False

    def getCurSelId(self):
        p = BigWorld.player()
        return p.personalZoneSkin.curUseSkinId or 1
