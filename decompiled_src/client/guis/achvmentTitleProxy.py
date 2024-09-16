#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentTitleProxy.o
import time
import gameglobal
from guis import tipUtils
from guis import uiUtils
from guis import events
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from uiProxy import UIProxy
from cdata import font_config_data as FCD
from data import achievement_data as AD
from data import title_data as TD
from data import achieve_rewardTitle_filter_data as ARFD
COLUMN_NUM = 2
COLOR_GRAY = '#969696'

class AchvmentTitleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentTitleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.achieves = {}
        self.searchInfo = {}
        self.titleAchieveIds = []

    def clearAll(self):
        pass

    def initPanel(self, widget):
        self.widget = widget.mainMc
        self.initData()
        self.initListProp()
        self.refreshInfo()
        self.widget.searchTextInput.addEventListener(events.EVENT_CHANGE, self.onSearchChange)

    def unRegisterPanel(self):
        self.widget = None

    def initData(self):
        if not self.titleAchieveIds:
            self.achieves = gameglobal.rds.ui.achvment.achieves
            titleAchieveIds = [ achieveId for achieveId in ARFD.data.keys() if not self.uiAdapter.achvment.isHideAchieve(achieveId) ]
            self.titleAchieveIds = sorted(titleAchieveIds, self.compare)
        if not self.searchInfo:
            self.searchInfo = {TD.data.get(ARFD.data.get(key, {}).get('rewardTitle'), {}).get('name'):key for key in self.titleAchieveIds}

    def compare(self, id1, id2):
        if id1 in self.achieves and id2 not in self.achieves:
            return -1
        if id1 not in self.achieves and id2 in self.achieves:
            return 1
        return cmp(AD.data.get(id1, {}).get('rewardTitle'), AD.data.get(id2, {}).get('rewardTitle'))

    def initListProp(self):
        self.widget.listView.itemRenderer = 'AchvmentTitlePanel_TitleItem'
        self.widget.listView.column = COLUMN_NUM
        self.widget.listView.labelFunction = self.itemLabelFunc

    def refreshInfo(self):
        self.refreshCompleteness()
        if self.widget.searchTextInput.text:
            self.refreshSearchResult(self.widget.searchTextInput.text)
        else:
            self.refreshList(self.titleAchieveIds)

    def refreshCompleteness(self):
        maxTitleNum = len(self.titleAchieveIds)
        achieveTitleNum = len(list(set(self.titleAchieveIds) & set(self.achieves)))
        self.widget.completenessBar.maxValue = maxTitleNum
        self.widget.completenessBar.currentValue = achieveTitleNum

    def refreshList(self, listData):
        self.widget.searchResultTf.visible = not listData
        self.widget.listView.dataArray = listData
        self.widget.listView.validateNow()

    def refreshSearchResult(self, searchText):
        retIds = [ self.searchInfo[name] for name in self.searchInfo if uiUtils.isContainString(name, searchText) ]
        if retIds != self.widget.listView.dataArray:
            self.refreshList(retIds)

    def itemLabelFunc(self, *args):
        item = ASObject(args[3][1])
        achieveId = int(args[3][0].GetNumber())
        item.achieveId = achieveId
        achieveData = AD.data.get(achieveId, {})
        achieveName = achieveData.get('name')
        rewardTitleId = achieveData.get('rewardTitle')
        isAchieved = achieveId in self.achieves
        item.nameTf.htmlText = self.getTitleShowText(rewardTitleId, isAchieved)
        item.dateTf.text = self.getDateText(achieveId)
        item.addEventListener(events.MOUSE_CLICK, self.onItemClick)
        TipManager.addTip(item, gameStrings.ACHIEVEMENT_TITLE_DESC % achieveName, tipUtils.TYPE_DEFAULT_BLACK, 'over', 'mouse')
        item.disabled = not isAchieved
        item.mouseEnabled = True

    def getTitleShowText(self, titleId, isAchieved):
        titleData = TD.data.get(titleId, {})
        titleName = titleData.get('name', '')
        titleColor = COLOR_GRAY
        if isAchieved:
            titleColor = FCD.data.get(('title', titleData.get('style', '')), {}).get('color', '#CCCCCC')
        return uiUtils.toHtml(titleName, titleColor)

    def getDateText(self, achieveId):
        if achieveId in self.achieves:
            t = time.localtime(self.achieves[achieveId])
            return time.strftime('%d/%.2d/%.2d' % (t.tm_year, t.tm_mon, t.tm_mday))
        else:
            return ''

    def onItemClick(self, *args):
        achieveId = ASObject(args[3][0]).currentTarget.achieveId
        gameglobal.rds.ui.achvment.link2AchvmentDetailView(achieveId=achieveId)

    def onSearchChange(self, *args):
        e = ASObject(args[3][0])
        if e.target != self.widget.searchTextInput:
            return
        text = e.currentTarget.text
        if text:
            self.refreshSearchResult(text)
        else:
            self.refreshList(self.titleAchieveIds)
