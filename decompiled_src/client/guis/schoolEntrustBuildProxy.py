#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolEntrustBuildProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import commQuest
from guis.uiProxy import UIProxy
from guis import uiConst
from gameStrings import gameStrings
from callbackHelper import Functor
from data import quest_loop_data as QLD
from data import quest_data as QD
from data import fame_data as FD
from data import sys_config_data as SCD

class SchoolEntrustBuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolEntrustBuildProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_ENTRUST_BUILD, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_ENTRUST_BUILD:
            self.widget = widget
            self.initUI()

    def show(self, qId, eId, eLv):
        if not qId or not eId or not eLv:
            return
        self.qId = qId
        self.eId = eId
        self.eLv = eLv
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SCHOOL_ENTRUST_BUILD, True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SCHOOL_ENTRUST_BUILD)
        self.entrustInfo = {}
        self.widget = None

    def reset(self):
        self.qId = None
        self.eId = None
        self.eLv = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            p = BigWorld.player()
            qData = QLD.data.get(self.qId, {})
            qDetail = p.genQuestLoopDetail(self.qId)
            self.widget.titleTxt.htmlText = qData.get('name', '')
            self.widget.DescTxt.htmlText = qData.get('desc', '')
            fameList = []
            self.widget.removeAllInst(self.widget.rewardList)
            taskAward = qDetail.get('taskAward', {})
            cashRewardType = taskAward.get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
            quests = qData.get('quests', (0,))
            fqId = quests[-1]
            exp, money, socExp, xiuwei = commQuest.calcReward(p, fqId)
            fameData = QD.data.get(fqId, {}).get('compFame', [])
            fameAwardFactor = commQuest.getQuestLoopAwardFactorByType(p, qDetail.get('loopId', 0), gametypes.QUEST_REWARD_CREDIT)
            for fame in fameData:
                fameTip = FD.data.get(fame[0], {}).get('name') if len(fame) else ''
                fameName = SCD.data.get('fameIdToBonusDict', {}).get(fame[0], 'fame')
                fameList.append((fameName, int(fame[1] * fameAwardFactor), fameTip))

            height = 0
            if money:
                item = self.widget.getInstByClsName('SchoolEntrustBuild_RewardMc')
                self.widget.rewardList.addChild(item)
                if cashRewardType == gametypes.QUEST_CASHREWARD_FREE:
                    item.icon.bonusType = 'cash'
                elif gametypes.QUEST_CASHREWARD_BIND:
                    item.icon.bonusType = 'bindCash'
                item.rewardTxt.text = money
                item.y = height
                height += item.height + 5
            if exp:
                item = self.widget.getInstByClsName('SchoolEntrustBuild_RewardMc')
                self.widget.rewardList.addChild(item)
                item.icon.bonusType = 'exp'
                item.rewardTxt.text = exp
                item.y = height
                height += item.height + 5
            if fameList:
                for fame in fameList:
                    item = self.widget.getInstByClsName('SchoolEntrustBuild_RewardMc')
                    self.widget.rewardList.addChild(item)
                    item.icon.bonusType = 'fame'
                    item.rewardTxt.text = fame[1]
                    item.icon.tip = fame[2]
                    item.y = height
                    height += item.height + 5

    def cancelCallBack(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def _onAcceptBtnClick(self, e):
        gamelog.debug('@zq _onAcceptBtnClick')
        p = BigWorld.player()
        msg = gameStrings.SCHOOL_ENTRUST_ACCEPT_CONFIRM

        def closeFunc():
            self.hide()

        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.acceptSchoolEntrustQuestLoop, int(self.eId), self.eLv, self.qId), noCallback=closeFunc)
