#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famerRankHistoryProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import uiConst
import utils
import uiUtils
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import ASObject
from data import hall_of_fame_rules_desc_data as HOFRDD
from data import hall_of_fame_config_data as HOFCD
from guis import rankPanelUtils
from guis.asObject import ASUtils
import events
import gamelog

class FamerRankHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamerRankHistoryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemMc = None
        self.topType = 0
        self.dataCache = {}
        self.version = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMER_RANK_HISTORY, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FAMER_RANK_HISTORY:
            self.widget = widget
            self.initUI()
            self.reqeustData()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FAMER_RANK_HISTORY)

    def show(self, topType):
        if topType < 46 or topType > 52:
            return
        if self.widget:
            self.hide()
        self.topType = topType
        self.uiAdapter.loadWidget(uiConst.WIDGET_FAMER_RANK_HISTORY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.titleTxt.text = HOFCD.data.get('rankName', {}).get(self.topType, '')
        if self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING:
            self.widget.schoolDropdown.visible = True
            self.schoolMenu = rankPanelUtils.SchoolMenuUtil()
            self.schoolMenu.register(self.widget.schoolDropdown, self.handleInvalidateRankList, rankPanelUtils.getCompleteMenuData())
        else:
            self.widget.schoolDropdown.visible = False
        if self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING or self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI:
            self.widget.lvBtn0.addEventListener(events.EVENT_SELECT, self.handleInvalidateRankList, False, 0, False)
            self.widget.lvBtn1.addEventListener(events.EVENT_SELECT, self.handleInvalidateRankList, False, 0, False)
        else:
            self.widget.lvBtn0.visible = self.widget.lvBtn1.visible = False
        self.refreshSeasonMenu()
        self.refreshList()

    def handleInvalidateRankList(self, *args):
        self.refreshList()

    def refreshList(self):
        if not self.widget:
            return
        if self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING:
            schoolId = rankPanelUtils.getCompleteMenuData()[self.widget.schoolDropdown.selectedIndex]['schoolId']
            lvKeyStr = self.getLvKey() + '_' + str(schoolId)
        elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI:
            lvKeyStr = self.getLvKey() + '_0'
        else:
            lvKeyStr = '0'
        season = self.widget.seasonDropdown.selectedIndex + 1
        dataList = self.dataCache.get(season, {}).get(self.topType, {}).get(lvKeyStr, [])
        dataLen = len(dataList)
        for index in range(10):
            listItem = self.widget.__getattr__('item' + str(index))
            if index < dataLen:
                listItem.visible = True
                self.setupListItem(listItem, dataList[index])
            else:
                listItem.visible = False

    def onGetRankData(self, infoDic, curTopType, ver):
        gamelog.info('@ljh on receive famer rank histroy data: ', 'season count=', len(infoDic), 'rankType =', curTopType, 'version =', ver)
        if self.version == ver:
            return
        self.version = ver
        for season, seasonDataDict in infoDic.iteritems():
            for topType, rankDict in seasonDataDict.iteritems():
                for lvKey, dataArray in rankDict.iteritems():
                    cachedDataArray = self.dataCache.setdefault(season, {}).setdefault(topType, {}).setdefault(lvKey, [])
                    del cachedDataArray[:]
                    for data in dataArray:
                        roleName = utils.getRoleNameFromNameWithHostIdStr(data[1])
                        serverName = utils.getServerName(utils.getHostIdFromNameWithHostIdStr(data[1]))
                        cachedDataArray.append((data[3],
                         roleName,
                         serverName,
                         uiUtils.getSchoolNameById(data[2])))

                    cachedDataArray.sort(key=lambda v: v[0])

        if self.widget:
            self.refreshSeasonMenu()
            self.refreshList()

    def reqeustData(self):
        BigWorld.player().base.getTopHallOfFameHistory(self.topType, self.version)
        gamelog.info('@ljh request famer rank history data: topType =', self.topType, 'version =', self.version)

    def setupListItem(self, item, data):
        item.playerName.text = data[1]
        item.serverName.text = data[2]
        item.schoolName.text = data[3]
        rank = data[0]
        if rank <= 3:
            item.rank.visible = False
            item.top3Icon.visible = True
            item.top3Icon.gotoAndStop(rank * 5)
        else:
            item.rank.visible = True
            item.rank.text = str(rank)
            item.top3Icon.visible = False

    def refreshSeasonMenu(self):
        self.widget.seasonDropdown.removeEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleInvalidateRankList)
        seasonList = self.dataCache.keys()
        seasonList.sort()
        seasonMenuData = [ {'label': gameStrings.FAMER_RANK_HISTORY_SEASON % season} for season in seasonList ]
        ASUtils.setDropdownMenuData(self.widget.seasonDropdown, seasonMenuData)
        self.widget.seasonDropdown.selectedIndex = len(seasonList) - 1
        self.widget.seasonDropdown.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleInvalidateRankList, False, 0, True)

    def getLvKey(self):
        if self.widget.lvBtn0.selected:
            return '1_69'
        return '70_79'
