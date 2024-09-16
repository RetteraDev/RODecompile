#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/quickJoinProxy.o
import BigWorld
from Scaleform import GfxValue
from guis.ui import gbk2unicode
from uiProxy import UIProxy
import gameglobal
import uiConst
import uiUtils
import utils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
TOTAL_COUNT = 30

class QuickJoinProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuickJoinProxy, self).__init__(uiAdapter)
        self.modelMap = {'getJoinDesc': self.onGetJoinDesc,
         'clickJoin': self.onClickJoin,
         'getJoinInfo': self.onGetJointInfo,
         'joiningOverTime': self.onJoiningOverTime,
         'closeJoin': self.onCloseJoin}
        self.reset()

    def reset(self):
        self.joiningMediator = None
        self.joinClickMediator = None
        self.joinType = uiConst.QUICK_JOIN_GROUP_NO

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QUICK_JOINING:
            self.joiningMediator = mediator
        elif widgetId == uiConst.WIDGET_QUICK_JOIN_CLICK:
            self.joinClickMediator = mediator

    def onGetJoinDesc(self, *arg):
        applyQuickJoinDesc = SCD.data.get('applyQuickJoinDesc', {})
        desc = applyQuickJoinDesc.get(self.joinType, '')
        return GfxValue(gbk2unicode(desc))

    def onClickJoin(self, *arg):
        p = BigWorld.player()
        if self.joiningMediator:
            p.showGameMsg(GMDD.data.APPLY_GROUP_FAILED_ALREADY_IN_JOINING, ())
            return
        if self.joinType == uiConst.QUICK_JOIN_GROUP_NO:
            return
        quickJoinInterval = SCD.data.get('quickJoinInterval', 50)
        delta = quickJoinInterval - (utils.getNow() - p.quickJoinTimestamp)
        if delta > 0:
            p.showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED_LIMIT, (utils.formatDuration(delta),))
            return
        if self.joinType == uiConst.QUICK_JOIN_GROUP_DIGONG:
            p.cell.queryDiGongTeams(p.spaceNo)
        elif self.joinType == uiConst.QUICK_JOIN_GROUP_WORLD_WAR:
            p.cell.queryWorldWarTeams()

    def onGetJointInfo(self, *arg):
        info = {}
        p = BigWorld.player()
        info['curCnt'] = 0 if not p.quickJoinTimestamp else max(TOTAL_COUNT - int(p.getServerTime() - p.quickJoinTimestamp) - 2, 0)
        info['maxCnt'] = TOTAL_COUNT
        return uiUtils.dict2GfxDict(info)

    def setJoinType(self, joinType):
        self.joinType = joinType

    def showJoinClick(self):
        if self.joinClickMediator:
            return
        if self.joinType == uiConst.QUICK_JOIN_GROUP_NO:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QUICK_JOIN_CLICK)

    def closeJoinClick(self):
        self.joinClickMediator = None
        self.joinType = uiConst.QUICK_JOIN_GROUP_NO
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUICK_JOIN_CLICK)

    def onCloseJoin(self, *arg):
        self.closeJoinClick()

    def onJoiningOverTime(self, *arg):
        p = BigWorld.player()
        if p.groupNUID == 0:
            BigWorld.player().showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED, ())
        gameglobal.rds.ui.team.groupDetailFactory.resetApplyJoining()
        self.closeJoining()

    def showJoining(self):
        if not gameglobal.rds.ui.team.groupDetailFactory.isApplyJoining:
            return
        if self.joiningMediator:
            self.joiningMediator.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QUICK_JOINING)

    def closeJoining(self):
        self.joiningMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUICK_JOINING)

    def onJoinGroupSucc(self):
        self.closeJoinClick()
        self.closeJoining()
        gameglobal.rds.ui.team.groupDetailFactory.resetApplyJoining()
