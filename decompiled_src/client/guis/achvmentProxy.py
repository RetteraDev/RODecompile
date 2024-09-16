#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentProxy.o
import BigWorld
import gameglobal
import uiConst
import clientUtils
from uiTabProxy import UITabProxy
from gamestrings import gameStrings
from cdata import font_config_data as FCD
from data import item_data as ID
from data import achievement_data as AD
from data import achievement_class_data as ACD
from data import title_data as TD
from data import achieve_target_data as ATD
TAB_OVERVIEW_IDX = 0
TAB_DETAIL_IDX = 1
TAB_TITLE_IDX = 2
TAB_AWARD_IDX = 3
NAME_IDX = 0
CLASS_IDX = 1
ACHIEVE_CNT_IDX = 0
TOTAL_CNT_IDX = 1

class AchvmentProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(AchvmentProxy, self).__init__(uiAdapter)
        self.achieves = {}
        self.achieveTargets = {}
        self.achievePoint = 0
        self.achieveFilterData = {}
        self.classProgress = {}
        self.subClassInfo = {}
        self.lastRequestIsCompare = False
        self.gainedAchieveIds = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACHVMENTBG, self.hide)

    def reset(self):
        self.linkAchieveId = 0
        super(AchvmentProxy, self).reset()
        self.uiAdapter.achvmentOverview.reset()
        self.uiAdapter.achvmentDetail.reset()
        self.uiAdapter.achvmentTitle.reset()
        self.uiAdapter.achvmentAward.reset()

    def clearAll(self):
        self.achieves = {}
        self.achieveTargets = {}
        self.achievePoint = 0
        self.achieveFilterData = {}
        self.classProgress = {}
        self.subClassInfo = {}
        self.gainedAchieveIds = []
        self.lastRequestIsCompare = False
        self.uiAdapter.achvmentOverview.clearAll()
        self.uiAdapter.achvmentDetail.clearAll()
        self.uiAdapter.achvmentTitle.clearAll()
        self.uiAdapter.achvmentAward.clearAll()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACHVMENTBG:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(AchvmentProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACHVMENTBG)

    def getAchieveData(self, isCompareRequest = False):
        self.lastRequestIsCompare = isCompareRequest
        BigWorld.player().base.getAchievement()

    def _getTabList(self):
        return [{'tabIdx': TAB_OVERVIEW_IDX,
          'tabName': 'overviewTabBtn',
          'view': 'AchvmentOverviewPanelWidget',
          'proxy': 'achvmentOverview'},
         {'tabIdx': TAB_DETAIL_IDX,
          'tabName': 'detailTabBtn',
          'view': 'AchvmentDetailPanelWidget',
          'proxy': 'achvmentDetail'},
         {'tabIdx': TAB_TITLE_IDX,
          'tabName': 'titleTabBtn',
          'view': 'AchvmentTitlePanelWidget',
          'proxy': 'achvmentTitle'},
         {'tabIdx': TAB_AWARD_IDX,
          'tabName': 'awardTabBtn',
          'view': 'AchvmentAwardPanelWidget',
          'proxy': 'achvmentAward'}]

    def show(self):
        if self.lastRequestIsCompare:
            self.lastRequestIsCompare = False
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ACHVEMENT_WEEK_AWARD)
        if self.widget:
            self.hide()
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACHVMENTBG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if not self.achieveFilterData:
            self.achieveFilterData = self.genAchieveFilterData()
        if not self.subClassInfo:
            self.subClassInfo = self.genSubClassInfo()
        self.classProgress = self.genClassProgress()
        self.initTabUI()
        if self.linkAchieveId:
            self.widget.setTabIndex(TAB_DETAIL_IDX)
            self.link2AchvmentDetailView(achieveId=self.linkAchieveId)
        elif self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_OVERVIEW_IDX)

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def genAchieveFilterData(self):
        return {achieveId:info for achieveId, info in AD.data.iteritems() if not self.isHideAchieve(achieveId)}

    def genSubClassInfo(self):
        subClassInfo = {}
        for classId, info in ACD.data.iteritems():
            for subClassId, name in info.get('newvalue', {}).iteritems():
                subClassInfo[subClassId] = (name, classId)

        return subClassInfo

    def genClassProgress(self):
        ret = {}
        for achieveId, info in self.achieveFilterData.iteritems():
            subClassId = info.get('class')
            classId = self.subClassInfo.get(subClassId, ('', 0))[CLASS_IDX]
            if classId not in ret:
                ret[classId] = [0, 0]
            ret[classId][ACHIEVE_CNT_IDX] += int(achieveId in self.achieves)
            ret[classId][TOTAL_CNT_IDX] += 1
            if subClassId not in ret:
                ret[subClassId] = [0, 0]
            ret[subClassId][ACHIEVE_CNT_IDX] += int(achieveId in self.achieves)
            ret[subClassId][TOTAL_CNT_IDX] += 1

        return ret

    def isHideAchieve(self, achieveId):
        isHide = AD.data.get(achieveId, {}).get('hideUI', 0)
        if isHide == uiConst.ACHIEVE_HIDE_ALL:
            return True
        if (isHide == uiConst.ACHIEVE_HIDE_NOTDONE or isHide == uiConst.ACHIEVE_HIDE_NOTDONE_EX) and achieveId not in self.achieves:
            return True
        return False

    def link2AchvmentDetailView(self, subClassId = 0, achieveId = 0, linkData = {}):
        if subClassId:
            self.uiAdapter.achvmentDetail.expandHistory = {}
            self.uiAdapter.achvmentDetail.selectedSubClassId = subClassId
        elif achieveId:
            subClassId = AD.data.get(achieveId, {}).get('class', -1)
            self.uiAdapter.achvmentDetail.expandHistory = {}
            self.uiAdapter.achvmentDetail.selectedSubClassId = subClassId
            self.uiAdapter.achvmentDetail.selectAchieveId = achieveId
        elif linkData:
            self.uiAdapter.achvmentDetail.expandHistory = {}
            self.uiAdapter.achvmentDetail.linkData = linkData
        if self.currentTabIndex != TAB_DETAIL_IDX:
            self.uiAdapter.achvmentDetail.resetSearchText()
            self.widget.setTabIndex(TAB_DETAIL_IDX)
        else:
            self.uiAdapter.achvmentDetail.refreshInfo()

    def getAchievementPoint(self):
        maxVal = 0
        for k, v in AD.data.iteritems():
            if self.isHideAchieve(k):
                continue
            val = v.get('rewardPoint', 0)
            maxVal += val

        return (self.achievePoint, maxVal)

    def getAwardString(self, titleId, bonusId):
        awardText = ''
        if titleId:
            awardText = gameStrings.ACHIEVE_DETAIL_AWARD_ITEM_FIELD_TEXT
            titleData = TD.data.get(titleId, {})
            color = FCD.data.get(('title', titleData.get('style', '')), {}).get('color', '#CCCCCC')
            awardText += gameStrings.ACHIEVE_DETAIL_AWARD_ITEM_TEXT % (color, titleData.get('name', ''))
        rewardItems = clientUtils.genItemBonus(bonusId)
        if rewardItems:
            awardText += gameStrings.ACHIEVE_DETAIL_AWARD_TITLE_FIELD_TEXT
            for itemId, itemNum in rewardItems:
                itemName = ID.data.get(itemId, {}).get('name', '')
                quality = ID.data.get(itemId, {}).get('quality', '')
                color = FCD.data.get(('item', quality), {}).get('color', '#CCCCCC')
                awardText += gameStrings.ACHIEVE_DETAIL_AWARD_TITLE_TEXT % (color, itemName, itemNum)

        return awardText

    def getAchieveProgress(self, achieveId):
        achieveTargets = AD.data.get(achieveId, {}).get('achieveTargets', ())
        achieveCnt = 0
        totalCnt = 0
        if achieveTargets:
            targetId = achieveTargets[0]
            totalCnt = ATD.data.get(targetId, {}).get('varMax', 1)
            if achieveId in self.achieves:
                achieveCnt = totalCnt
            elif targetId in self.achieveTargets:
                var = ATD.data.get(targetId, {}).get('var', '')
                achieveCnt = min(totalCnt, self.achieveTargets[targetId].get(var, 0))
            else:
                achieveCnt = 0
        return (achieveCnt, totalCnt)

    def checkAchieveFlag(self, acId):
        return acId in self.gainedAchieveIds
