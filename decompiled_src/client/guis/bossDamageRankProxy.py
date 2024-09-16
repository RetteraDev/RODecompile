#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bossDamageRankProxy.o
import BigWorld
import gameglobal
import gametypes
import uiConst
import const
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import rankPanelUtils
from data import wing_world_config_data as WWCD
REFRESH_INTERVAL_TIME = 30
ICON_MAX_RANK = 3
DATA_GBID_INDEX = 0
DATA_NAME_INDEX = 1
DATA_SCHOOL_INDEX = 2
DATA_VAL_INDEX = 3
VAL_VAL_INDEX = 0
VAL_TIME_INDEX = 1
VAL_LV_INDEX = 2

class BossDamageRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BossDamageRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.schoolMenu = rankPanelUtils.SchoolMenuUtil()
        self.lvBtn = rankPanelUtils.LvButtonsUtil()
        self.refreshBtn = rankPanelUtils.RefreshBtnUtil()
        self.dataCache = {'version': 0,
         'data': {}}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOSSDAMAGE_RANK, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BOSSDAMAGE_RANK:
            self.widget = widget
            self.initUI()
            self.refreshList()
            self.queryInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOSSDAMAGE_RANK)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BOSSDAMAGE_RANK)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.schoolMenu.register(self.widget.schoolMenu, self.onSchoolMenuChange, selectIdx=self.getSchoolDefSel())
        self.lvBtn.register(self.widget, getattr(self.widget, self.getInitLvMcName()), self.getLvBtnInfoMap(), self.onLvBtnClick)
        self.refreshBtn.register(self.widget.refreshBtn, self.onRefreshBtnClick, REFRESH_INTERVAL_TIME)
        self.initText()
        self.initListProp()

    def initText(self):
        self.widget.title.textField.text = WWCD.data.get('bossDamageRankTitle')
        self.widget.awardText.text = WWCD.data.get('bossDamageRewardText')
        self.widget.rankText.text = WWCD.data.get('bossDamageRankText')

    def initListProp(self):
        self.widget.rankList.itemRenderer = 'BossDamageRank_ListItem'
        self.widget.rankList.labelFunction = self.rankItemLabelFunc

    def refreshList(self, needReset = False):
        listData = self.dataCache.get('data', {}).get(self.getKey(), ())
        self.widget.rankList.dataArray = listData
        needReset and self.widget.rankList.scrollToHead()

    def getSchoolDefSel(self):
        return const.SCHOOL_SET.index(BigWorld.player().school)

    def onGetTopWingWorldBoss(self, dataInfo):
        key = dataInfo[-1]
        version = dataInfo[0]
        data = dataInfo[1]
        data.sort(self.compare, key=lambda d: d[DATA_VAL_INDEX])
        self.dataCache['version'] = version
        self.dataCache['data'][key] = data
        self.widget and self.refreshList(True)

    def compare(self, d1, d2):
        if d1[VAL_VAL_INDEX] == d2[VAL_VAL_INDEX]:
            return cmp(d1[VAL_TIME_INDEX], d2[VAL_TIME_INDEX])
        return cmp(d2[VAL_VAL_INDEX], d1[VAL_VAL_INDEX])

    def rankItemLabelFunc(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        rank = item.index + 1
        if rank <= ICON_MAX_RANK:
            item.rankIcon.visible = True
            item.rankIcon.gotoAndStop('rank%d' % rank)
            item.tf_rank.visible = False
        else:
            item.rankIcon.visible = False
            item.tf_rank.visible = True
            item.tf_rank.text = str(rank)
        item.gbId = data[DATA_GBID_INDEX]
        item.tf_name.text = data[DATA_NAME_INDEX]
        item.tf_lv.text = data[DATA_VAL_INDEX][VAL_LV_INDEX]
        item.tf_rankData.text = int(data[DATA_VAL_INDEX][VAL_VAL_INDEX])
        item.bg.visible = bool(long(item.gbId) == BigWorld.player().gbId)

    def getInitLvMcName(self):
        lv = BigWorld.player().lv
        if 1 <= lv <= 59:
            return 'lv0'
        elif 60 <= lv <= 69:
            return 'lv1'
        else:
            return 'lv2'

    def getLvBtnInfoMap(self):
        return {'lv0': '1_59_',
         'lv1': '60_69_',
         'lv2': '70_79_'}

    def getKey(self):
        return self.lvBtn.currentData + str(self.schoolMenu.schoolId)

    def onSchoolMenuChange(self):
        self.queryInfo()
        self.widget and self.refreshList(True)

    def onLvBtnClick(self):
        self.queryInfo()
        self.widget and self.refreshList(True)

    def onRefreshBtnClick(self):
        self.queryInfo()

    def _onAwardBtnClick(self, e):
        gameglobal.rds.ui.ranking.openRewardPanel(const.PROXY_KEY_WING_WORLD_BOSS_DAMAGE, 0)

    def queryInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        version = self.dataCache.get('version', 0)
        p.base.getTopWingWorldBoss(version, self.getKey())
