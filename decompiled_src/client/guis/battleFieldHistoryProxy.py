#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleFieldHistoryProxy.o
import BigWorld
import copy
import gameglobal
import events
import const
from guis import uiConst
from guis.asObject import ASObject
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import battle_field_history_data as BFHD
OVERVIEW_BF_DATA = 0
NORMAL_ITEM_NAME = 'BattleFieldHistory_NormalItem'
NORMAL_ITEM_NUM = 6
NORMAL_ITEM_OFFSET = 3
MIN_VALUE_KEYS = (18,)
MAX_VALUE_KEYS = (17,)
TOTAL_CALC_TYPE_DEFAULT = 0
TOTAL_CALC_TYPE_MIN = 1
TOTAL_CALC_TYPE_MAX = 2

class BattleFieldHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleFieldHistoryProxy, self).__init__(uiAdapter)
        self.commonDataKey = []
        self.gloryDataKey = []
        self.isNeedShow = False
        self.reset()
        self.widget = None
        self.tabIdx = OVERVIEW_BF_DATA
        uiAdapter.registerEscFunc(uiConst.WIDGET_BATTLE_FIELD_HISTORY, self.clearWidget)

    def reset(self):
        self.tabData = {const.BATTLE_FIELD_MODE_RES: {},
         const.BATTLE_FIELD_MODE_FLAG: {},
         const.BATTLE_FIELD_MODE_FORT: {},
         OVERVIEW_BF_DATA: {},
         const.BATTLE_FIELD_MODE_NEW_FLAG: {},
         const.BATTLE_FIELD_MODE_CQZZ: {},
         const.BATTLE_FIELD_MODE_PUBG: {}}
        self.tabIndexs = [OVERVIEW_BF_DATA,
         const.BATTLE_FIELD_MODE_RES,
         const.BATTLE_FIELD_MODE_FLAG,
         const.BATTLE_FIELD_MODE_FORT,
         const.BATTLE_FIELD_MODE_NEW_FLAG,
         const.BATTLE_FIELD_MODE_CQZZ,
         const.BATTLE_FIELD_MODE_PUBG]

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.refreshUI()

    def refreshUI(self):
        self.buildHistoryItem()
        self.initData()
        self.initUI()

    def buildHistoryItem(self):
        self.gloryDataKey = []
        self.commonDataKey = []
        for id, item in BFHD.data.iteritems():
            if id in MIN_VALUE_KEYS:
                item['calcType'] = TOTAL_CALC_TYPE_MIN
            elif id in MAX_VALUE_KEYS:
                item['calcType'] = TOTAL_CALC_TYPE_MAX
            if item.get('isGloryData', []):
                self.gloryDataKey.append(item)
            else:
                self.commonDataKey.append(item)

    def normalizeTabData(self):
        for k, data in self.tabData.iteritems():
            for key, item in data.iteritems():
                if item < 0:
                    data[key] = 0

    def getValueList(self, key):
        p = BigWorld.player()
        valueList = [self.tabData[const.BATTLE_FIELD_MODE_RES].get(key, 0), self.tabData[const.BATTLE_FIELD_MODE_FLAG].get(key, 0), self.tabData[const.BATTLE_FIELD_MODE_FORT].get(key, 0)]
        if gameglobal.rds.configData.get('enableNewFlagBF', False):
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_NEW_FLAG].get(key, 0))
        if gameglobal.rds.configData.get('enableCqzzBf', False):
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_CQZZ].get(key, 0))
        if p.isCanJoinPUBG():
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_PUBG].get(key, 0))
        return valueList

    def initData(self):
        p = BigWorld.player()
        self.tabData[const.BATTLE_FIELD_MODE_RES] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldResHistory', {}))
        self.tabData[const.BATTLE_FIELD_MODE_FLAG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldFlagHistory', {}))
        self.tabData[const.BATTLE_FIELD_MODE_FORT] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldFortHistory', {}))
        self.tabData[const.BATTLE_FIELD_MODE_NEW_FLAG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldNewFlagHistory', {}))
        self.tabData[const.BATTLE_FIELD_MODE_CQZZ] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldCqzzHistory', {}))
        self.tabData[const.BATTLE_FIELD_MODE_PUBG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldPUBGHistory', {}))
        self.normalizeTabData()
        for item in self.gloryDataKey:
            key = item.get('key', 0)
            valueList = self.getValueList(key)
            calcType = item.get('calcType', TOTAL_CALC_TYPE_DEFAULT)
            if OVERVIEW_BF_DATA in item.get('isGloryData', []):
                if calcType == TOTAL_CALC_TYPE_MIN:
                    self.tabData[OVERVIEW_BF_DATA][key] = min(valueList)
                elif calcType == TOTAL_CALC_TYPE_MAX:
                    self.tabData[OVERVIEW_BF_DATA][key] = max(valueList)
                else:
                    self.tabData[OVERVIEW_BF_DATA][key] = sum(valueList)

        for item in self.commonDataKey:
            key = item.get('key', 0)
            valueList = self.getValueList(key)
            calcType = item.get('calcType', TOTAL_CALC_TYPE_DEFAULT)
            if OVERVIEW_BF_DATA in item.get('type', []):
                if calcType == TOTAL_CALC_TYPE_MIN:
                    self.tabData[OVERVIEW_BF_DATA][key] = min(valueList)
                elif calcType == TOTAL_CALC_TYPE_MAX:
                    self.tabData[OVERVIEW_BF_DATA][key] = max(valueList)
                else:
                    self.tabData[OVERVIEW_BF_DATA][key] = sum(valueList)

    def initUI(self):
        p = BigWorld.player()
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        for idx in xrange(0, len(self.tabIndexs)):
            btn = self.widget.getChildByName('btn%d' % idx)
            btn.data = self.tabIndexs[idx]
            btn.addEventListener(events.MOUSE_CLICK, self.handleClickTabBtn)
            btn.visible = True
            if not gameglobal.rds.configData.get('enableNewFlagBF', False) and self.tabIndexs[idx] == const.BATTLE_FIELD_MODE_NEW_FLAG:
                btn.visible = False
            if not gameglobal.rds.configData.get('enableCqzzBf', False) and self.tabIndexs[idx] == const.BATTLE_FIELD_MODE_CQZZ:
                btn.visible = False
            if self.tabIndexs[idx] == const.BATTLE_FIELD_MODE_PUBG:
                if not p.isCanJoinPUBG() or not gameglobal.rds.configData.get('enablePVPPUBGProxy', False):
                    btn.visible = False

        self.onTabIdxChanged()

    def onTabIdxChanged(self):
        for idx in xrange(0, len(self.tabIndexs)):
            btn = self.widget.getChildByName('btn%d' % idx)
            if btn.data == self.tabIdx:
                self.widget.getChildByName('btn%d' % idx).selected = True
            else:
                self.widget.getChildByName('btn%d' % idx).selected = False

        self.refreshPanel()

    def refreshPanel(self):
        self.refreshGloryPanel()
        self.refreshNormalPanel()

    def refreshGloryPanel(self):
        tabData = self.tabData.get(self.tabIdx, [])
        gloryMcIdx = 0
        for gloryData in self.gloryDataKey:
            showGloryList = gloryData.get('isGloryData', [])
            if self.tabIdx not in showGloryList:
                continue
            glory = self.widget.gloryArea.getChildByName('glory%d' % gloryMcIdx)
            gloryMcIdx += 1
            gloryFrameIdx = gloryData.get('gloryFrameIdx', 7)
            glory.icon.gotoAndStop('glory%d' % gloryFrameIdx)
            key = gloryData.get('key', '')
            if glory.icon.score:
                glory.scoreTxt.text = gloryData.get('name', '%s')
                glory.icon.score.text = str(int(tabData.get(key, 0)))
            elif gloryData.get('name', '%s').find('%s') != -1:
                glory.scoreTxt.text = gloryData.get('name', '%s') % str(tabData.get(key, 0))
            else:
                glory.scoreTxt.text = gloryData.get('name', '%s')

    def refreshNormalPanel(self):
        tabData = self.tabData.get(self.tabIdx, [])
        x = 0
        y = 0
        normalItemNum = 0
        for idx in xrange(0, len(self.commonDataKey)):
            showTypeList = self.commonDataKey[idx].get('type', [])
            if self.tabIdx not in showTypeList:
                continue
            key = self.commonDataKey[idx].get('key', '')
            if self.commonDataKey[idx].get('isAverage', 0):
                divide = self.commonDataKey[idx].get('divide', [])
                if not tabData.get(divide[1], 0):
                    tabData[key] = 0
                elif self.commonDataKey[idx].get('isPercentForm', 0):
                    tabData[key] = '%d%%' % int(tabData.get(divide[0], 0) * 1.0 / tabData.get(divide[1], 0) * 100)
                else:
                    tabData[key] = int(tabData.get(divide[0], 0) / tabData.get(divide[1], 0))
            normalItem = self.widget.normalScoreList.getChildByName('normalItem%d' % normalItemNum)
            if not normalItem:
                normalItem = self.widget.getInstByClsName(NORMAL_ITEM_NAME)
                normalItem.x = x
                normalItem.y = y
                normalItem.name = 'normalItem%d' % normalItemNum
                self.widget.normalScoreList.addChild(normalItem)
            if normalItemNum % NORMAL_ITEM_NUM == 5:
                y = y + normalItem.height + NORMAL_ITEM_OFFSET
                x = 0
            else:
                x = x + normalItem.width
            normalItemNum += 1
            normalItem.itemName.text = self.commonDataKey[idx].get('name', '')
            normalItem.score.text = self.convertNum(tabData.get(key, 0))

        while normalItemNum < self.widget.normalScoreList.numChildren:
            self.widget.normalScoreList.removeChildAt(self.widget.normalScoreList.numChildren - 1)

    def convertNum(self, num):
        if type(num) == str:
            return num
        elif num > 100000000:
            return gameStrings.BF_HISTORY_YI % ('%.2f' % (num / 100000000))
        elif num > 10000:
            return gameStrings.BF_HISTORY_WAN % int(num / 10000)
        else:
            return str(int(num))

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_HISTORY)
        self.commonDataKey = []
        self.gloryDataKey = []
        self.isNeedShow = False
        self.widget = None
        self.tabIdx = OVERVIEW_BF_DATA
        self.reset()

    def handleClickTabBtn(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        self.tabIdx = targetBtn.data
        self.onTabIdxChanged()

    def handleHidePanel(self, *args):
        self.clearWidget()

    def show(self):
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BATTLE_FIELD_HISTORY)
        else:
            self.refreshUI()
