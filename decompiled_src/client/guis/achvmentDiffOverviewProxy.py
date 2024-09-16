#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentDiffOverviewProxy.o
import BigWorld
import gameglobal
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import achievement_point_lv_data as APLD
MAIN_STAGE_TYPE = 0
TITLE_ICON_PATH = 'achvment/110/%d.dds'

class AchvmentDiffOverviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentDiffOverviewProxy, self).__init__(uiAdapter)
        self.reset()

    def reset(self):
        self.widget = None
        self.otherName = ''
        self.myAchievePoint = 0
        self.otherAchievePoint = 0
        self.maxPoint = 0
        self.myStage = 0
        self.otherStage = 0
        self.achieveFilterData = {}
        self.myAchieves = {}
        self.otherAchieves = {}

    def clearAll(self):
        pass

    def initPanel(self, widget):
        self.widget = widget.mainMc
        self.initData()
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initData(self):
        self.achieveFilterData = gameglobal.rds.ui.achvmentDiff.achieveFilterData
        self.myAchieves = gameglobal.rds.ui.achvmentDiff.myAchieves
        self.otherAchieves = gameglobal.rds.ui.achvmentDiff.otherAchieves
        self.otherName = gameglobal.rds.ui.achvmentDiff.otherName
        self.myAchievePoint = gameglobal.rds.ui.achvmentDiff.myAchievePoint
        self.otherAchievePoint = gameglobal.rds.ui.achvmentDiff.otherAchievePoint
        self.maxPoint = gameglobal.rds.ui.achvmentDiff.maxPoint
        self.myStage, self.otherStage = self.getCurrentPointStage(self.myAchievePoint, self.otherAchievePoint)

    def initUI(self):
        myAchieveCnt = len(self.myAchieves)
        otherAchieveCnt = len(self.otherAchieves)
        maxAchieveCnt = len(self.achieveFilterData)
        myNextStageFloor = APLD.data.get((MAIN_STAGE_TYPE, self.myStage + 1), {}).get('achievePointRange', '1')
        otherNextStageFloor = APLD.data.get((MAIN_STAGE_TYPE, self.otherStage + 1), {}).get('achievePointRange', '1')
        myMc = self.widget.myMc
        myMc.nameTf.text = BigWorld.player().roleName
        myMc.achvmentTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_TEXT % myAchieveCnt
        myMc.achvmentProgressTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_PROGRESS_TEXT % (100.0 * myAchieveCnt / maxAchieveCnt)
        myMc.achievePointTf.text = '%d/%s' % (self.myAchievePoint, myNextStageFloor)
        myMc.progressMc.progressbar.currentValue = self.myAchievePoint * 100.0 / int(myNextStageFloor)
        myMc.progressMc.icon.fitSize = True
        iconId = APLD.data.get((MAIN_STAGE_TYPE, self.myStage), {}).get('rewardTitleIcon', 1001)
        myMc.progressMc.icon.loadImage(TITLE_ICON_PATH % iconId)
        myMc.stageMc.gotoAndStop('a%d' % self.myStage)
        otherMc = self.widget.otherMc
        otherMc.nameTf.text = self.otherName
        otherMc.achvmentTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_TEXT % otherAchieveCnt
        otherMc.achvmentProgressTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_PROGRESS_TEXT % (100.0 * otherAchieveCnt / maxAchieveCnt)
        otherMc.achievePointTf.text = '%d/%s' % (self.otherAchievePoint, otherNextStageFloor)
        otherMc.progressMc.progressbar.currentValue = self.otherAchievePoint * 100.0 / int(otherNextStageFloor)
        iconId = APLD.data.get((MAIN_STAGE_TYPE, self.otherStage), {}).get('rewardTitleIcon', 1001)
        otherMc.progressMc.icon.loadImage(TITLE_ICON_PATH % iconId)
        otherMc.stageMc.gotoAndStop('a%d' % self.otherStage)

    def getCurrentPointStage(self, myPoint, otherPoint):
        mainStages = {k[1]:v.get('achievePointRange', 0) for k, v in APLD.data.iteritems() if k[0] == MAIN_STAGE_TYPE}
        sortedData = sorted(mainStages.iteritems(), key=lambda d: int(d[1]), reverse=True)
        myStage = 0
        otherStage = 0
        for stageIdx, stageFloor in sortedData:
            if myPoint >= int(stageFloor) and myStage == 0:
                myStage = stageIdx
            if otherPoint >= int(stageFloor) and otherStage == 0:
                otherStage = stageIdx

        return (myStage, otherStage)
