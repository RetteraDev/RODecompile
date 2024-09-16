#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentDiffProxy.o
import uiConst
import gameglobal
from uiTabProxy import UITabProxy
from data import achievement_data as AD
from data import achievement_class_data as ACD
from data import achieve_target_data as ATD
TAB_OVERVIEW_IDX = 0
TAB_DETAIL_IDX = 1
TAB_TITLE_IDX = 2
TAB_AWARD_IDX = 3
NAME_IDX = 0
CLASS_IDX = 1
MY_ACHIEVE_CNT_IDX = 0
TOTAL_CNT_IDX = 1

class AchvmentDiffProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(AchvmentDiffProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACHVMENTDIFFBG, self.hide)

    def reset(self):
        self.otherName = ''
        self.myAchieves = {}
        self.myAchieveTargets = {}
        self.myAchievePoint = 0
        self.otherAchieves = {}
        self.otherAchieveTargets = {}
        self.otherAchievePoint = 0
        self.achieveFilterData = {}
        self.maxPoint = 0
        self.classProgress = {}
        self.subClassInfo = {}
        super(AchvmentDiffProxy, self).reset()
        self.uiAdapter.achvmentDiffOverview.reset()
        self.uiAdapter.achvmentDiffDetail.reset()

    def clearAll(self):
        self.uiAdapter.achvmentDiffDetail.clearAll()
        self.uiAdapter.achvmentDiffOverview.clearAll()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACHVMENTDIFFBG:
            self.widget = widget
            self.initData()
            self.initUI()

    def clearWidget(self):
        super(AchvmentDiffProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACHVMENTDIFFBG)

    def _getTabList(self):
        return [{'tabIdx': TAB_OVERVIEW_IDX,
          'tabName': 'overviewTabBtn',
          'view': 'AchvmentDiffOverviewPanelWidget',
          'proxy': 'achvmentDiffOverview'}, {'tabIdx': TAB_DETAIL_IDX,
          'tabName': 'detailTabBtn',
          'view': 'AchvmentDiffDetailPanelWidget',
          'proxy': 'achvmentDiffDetail'}]

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACHVMENTDIFFBG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_OVERVIEW_IDX)

    def initData(self):
        self.myAchieves = gameglobal.rds.ui.achvment.achieves
        self.myAchieveTargets = gameglobal.rds.ui.achvment.achieveTargets
        self.myAchievePoint, self.otherAchievePoint, self.maxPoint = self.getAchievementPoint()
        self.achieveFilterData = self.genAchieveFilterData()
        self.subClassInfo = self.genSubClassInfo()
        self.classProgress = self.genClassProgress()

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
            ret[classId][MY_ACHIEVE_CNT_IDX] += int(achieveId in self.otherAchieves)
            ret[classId][TOTAL_CNT_IDX] += 1

        return ret

    def isHideAchieve(self, achieveId):
        isHide = AD.data.get(achieveId, {}).get('hideUI', 0)
        isInMyAchieves = achieveId in self.myAchieves
        isInOtherAchieves = achieveId in self.otherAchieves
        if isHide == uiConst.ACHIEVE_HIDE_ALL:
            return True
        if isHide == uiConst.ACHIEVE_HIDE_NOTDONE and not isInMyAchieves and not isInOtherAchieves:
            return True
        if isHide == uiConst.ACHIEVE_HIDE_NOTDONE_EX and (not isInMyAchieves or not isInOtherAchieves):
            return True
        return False

    def getAchievementPoint(self):
        myVal = gameglobal.rds.ui.achvment.achievePoint
        otherVal = 0
        maxVal = 0
        for k, v in AD.data.iteritems():
            if self.isHideAchieve(k):
                continue
            val = v.get('rewardPoint', 0)
            maxVal += val
            otherVal += val * int(k in self.otherAchieves)

        return (myVal, otherVal, maxVal)

    def getAchieveProgress(self, achieveId, isSelf):
        tgtAchieves = self.myAchieves if isSelf else self.otherAchieves
        tgtAchieveTargets = self.myAchieveTargets if isSelf else self.otherAchieveTargets
        achieveTargets = AD.data.get(achieveId, {}).get('achieveTargets', ())
        achieveCnt = 0
        totalCnt = 0
        if achieveTargets:
            targetId = achieveTargets[0]
            totalCnt = ATD.data.get(targetId, {}).get('varMax', 1)
            if achieveId in tgtAchieves:
                achieveCnt = totalCnt
            elif targetId in tgtAchieveTargets:
                var = ATD.data.get(targetId, {}).get('var', '')
                achieveCnt = min(totalCnt, tgtAchieveTargets[targetId].get(var, 0))
            else:
                achieveCnt = 0
        return (achieveCnt, totalCnt)
