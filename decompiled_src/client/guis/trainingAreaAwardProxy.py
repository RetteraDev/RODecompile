#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/trainingAreaAwardProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gametypes
import clientUtils
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from guis import uiUtils
from guis import tipUtils
from data import item_data as ID
from cdata import font_config_data as FCD
from data import stats_target_data as STD

class TrainingAreaAwardProxy(SlotDataProxy):
    MAX_PAGE_ITEM_NUM = 12

    def __init__(self, uiAdapter):
        super(TrainingAreaAwardProxy, self).__init__(uiAdapter)
        self.modelMap = {'changePage': self.onChangePage,
         'getPageCount': self.onGetPageCount,
         'getInitData': self.onGetInitData,
         'getDesc': self.onGetDesc}
        self.bindType = 'trainingAward'
        self.type = 'trainingAward'
        self.isShow = False
        self.mediator = None
        self.currPage = 0
        self.pageCount = 0
        self.pageDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_TRAINING_AREA_AWARD, self.hide)
        self.initData()

    def initData(self):
        items = []
        for value in STD.data.itervalues():
            bonusId = value.get('bonusId', 0)
            type = value.get('type', 0)
            if type == gametypes.STATS_SUBTYPE_TRAINING and bonusId:
                awardInfo = clientUtils.genItemBonus(bonusId)
                desc = value.get('desc', '')
                prop = value.get('property', None)
                for itemId, itemNum in awardInfo:
                    items.append((itemId,
                     desc,
                     prop,
                     itemNum))

        length = len(items)
        self.pageCount = length // self.MAX_PAGE_ITEM_NUM
        if length % self.MAX_PAGE_ITEM_NUM:
            self.pageCount += 1
        for i, item in enumerate(items):
            page = i // self.MAX_PAGE_ITEM_NUM
            if not self.pageDict.has_key(page):
                self.pageDict[page] = []
            self.pageDict[page].append(item)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TRAINING_AREA_AWARD:
            self.mediator = mediator
            self.isShow = True

    def getSlotID(self, key):
        return (self.currPage, int(key[18:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        itemId = self.pageDict[page][pos][0]
        return tipUtils.getItemTipById(itemId)

    def onGetPageCount(self, *arg):
        return GfxValue(self.pageCount)

    def getPageItem(self, page):
        itemPage = self.movie.CreateArray()
        pageInfo = self.pageDict[self.currPage]
        for pos in xrange(len(pageInfo)):
            itemId = pageInfo[pos][0]
            num = pageInfo[pos][3]
            obj = self.movie.CreateObject()
            data = ID.data.get(itemId, {})
            name = data.get('name', '')
            path = uiUtils.getItemIconFile40(itemId)
            obj.SetMember('name', GfxValue(gbk2unicode(name)))
            obj.SetMember('path', GfxValue(path))
            quality = data.get('quality', 1)
            qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            obj.SetMember('qualitycolor', GfxValue(qualitycolor))
            obj.SetMember('num', GfxValue(num))
            obj.SetMember('position', GfxValue(pos))
            itemPage.SetElement(pos, obj)

        return itemPage

    def onGetInitData(self, *arg):
        return self.getPageItem(0)

    def show(self):
        self.currPage = 0
        self.uiAdapter.loadWidget(uiConst.WIDGET_TRAINING_AREA_AWARD)

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRAINING_AREA_AWARD)

    def onChangePage(self, *arg):
        self.currPage = int(arg[3][0].GetNumber())
        itemPage = self.getPageItem(self.currPage)
        if self.mediator:
            self.mediator.Invoke('setPageItem', itemPage)

    def onGetDesc(self, *arg):
        pos = int(arg[3][0].GetNumber())
        itemInfo = self.pageDict[self.currPage][pos]
        prop = itemInfo[2]
        p = BigWorld.player()
        propNum = 0
        if hasattr(p, 'statsInfo') and p.statsInfo.has_key(prop):
            propNum = p.statsInfo[prop]
        desc = itemInfo[1] % propNum
        return GfxValue(gbk2unicode(desc))
