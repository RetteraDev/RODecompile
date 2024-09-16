#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopPushProxy.o
import BigWorld
import gametypes
import const
import formula
import utils
import gameglobal
import uiConst
import events
import gamelog
from uiProxy import UIProxy
from data import school_top_config_data as STCD
from cdata import game_msg_def_data as GMDD

class SchoolTopPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_PUSH, self.hide)

    def reset(self):
        pass

    def clearAll(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self.timer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_PUSH)

    def show(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self.timer = None
        if not gameglobal.rds.configData.get('enableSchoolTopMatch', False):
            return
        else:
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_PUSH)
            return

    def initUI(self):
        self.widget.button.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if getattr(p, 'schoolTopStage', {}).get(p.school, None) in (gametypes.SCHOOL_TOP_STAGE_CLOSED, gametypes.SCHOOL_TOP_STAGE_DPS):
                self.hide()
                return
            if utils.getNow() > self.getEndTime() and getattr(p, 'schoolTopStage', {}).get(p.school, None) not in (gametypes.SCHOOL_TOP_STAGE_CAMPAIGN, gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE, gametypes.SCHOOL_TOP_STAGE_MATCH_START):
                self.hide()
                return
            roleName0 = ''
            roleName1 = ''
            gbId0 = 0
            gbId1 = 0
            finalCandidates = getattr(p, 'finalCandidates', [])
            for candidate in finalCandidates:
                if candidate.get('isSchoolTop', False):
                    roleName1 = candidate.get('roleName', '')
                    gbId1 = candidate.get('gbId', 0)
                else:
                    roleName0 = candidate.get('roleName', '')
                    gbId0 = candidate.get('gbId', 0)

            if getattr(p, 'schoolTopStage', {}).get(p.school, None) in (gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE, gametypes.SCHOOL_TOP_STAGE_MATCH_START, gametypes.SCHOOL_TOP_STAGE_OVER):
                schoolTopEndInfo = getattr(p, 'schoolTopEndInfo', None)
                if schoolTopEndInfo:
                    winnerInfo, loserInfo, isLive = schoolTopEndInfo
                    if loserInfo.get('isGiveUp', False):
                        self.widget.detail.gotoAndStop('giveUpresult')
                        self.widget.detail.player0.gotoAndStop('win')
                        self.widget.detail.player1.gotoAndStop('giveUp')
                        roleName0 = winnerInfo.get('roleName', '')
                        roleName1 = loserInfo.get('roleName', '')
                    else:
                        self.widget.detail.gotoAndStop('result')
                        self.widget.detail.txtWinner.text = winnerInfo.get('roleName', '')
                else:
                    self.widget.detail.gotoAndStop('fighting')
                    schoolTopMatchScore = getattr(p, 'schoolTopMatchScore', [])
                    if not schoolTopMatchScore:
                        self.widget.detail.txtCnt0.text = ''
                        self.widget.detail.txtCnt1.text = ''
                    else:
                        scoreInfo = {}
                        for gbId, roleName in schoolTopMatchScore:
                            name, score = scoreInfo.get(gbId, (roleName, 0))
                            scoreInfo[gbId] = (roleName, score + 1)

                        self.widget.detail.txtCnt0.text = scoreInfo.get(gbId0, ('', 0))[1]
                        self.widget.detail.txtCnt1.text = scoreInfo.get(gbId1, ('', 0))[1]
            else:
                self.widget.detail.gotoAndStop('before')
                self.widget.detail.txtTime.text = utils.formatTimeStr(max(0, int(self.getStartTime() - utils.getNow())), 'm:s', True, 2, 2)
            if self.widget.detail.txtName0:
                self.widget.detail.txtName0.text = roleName0
            if self.widget.detail.txtName1:
                self.widget.detail.txtName1.text = roleName1
            BigWorld.callback(0.3, self.refreshInfo)
            return

    def getStartTime(self):
        battleStartTime = utils.getNextCrontabTime(STCD.data.get('matchStartTime', ''))
        if not utils.isSameWeek(battleStartTime, utils.getNow()):
            battleStartTime = utils.getPreCrontabTime(STCD.data.get('matchStartTime', ''))
        return battleStartTime

    def getEndTime(self):
        pushEndTime = utils.getNextCrontabTime(STCD.data.get('pushEndTime', ''))
        if not utils.isSameWeek(pushEndTime, utils.getNow()):
            pushEndTime = utils.getPreCrontabTime(STCD.data.get('pushEndTime', ''))
        return pushEndTime

    def getPreShowTime(self):
        return STCD.data.get('preShowTime', 60)

    def tryStartTimer(self):
        if not gameglobal.rds.configData.get('enableSchoolTopMatch', False):
            return
        else:
            p = BigWorld.player()
            startTime = self.getStartTime()
            now = utils.getNow()
            if startTime - self.getPreShowTime() < now < self.getEndTime():
                self.show()
            elif getattr(p, 'schoolTopStage', {}).get(p.school, None) in (gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE, gametypes.SCHOOL_TOP_STAGE_MATCH_START):
                self.show()
            elif utils.getNow() < startTime - self.getPreShowTime():
                if self.timer:
                    BigWorld.cancelCallback(self.timer)
                gamelog.info('jbx:schoolTop TryStartTimer', startTime - self.getPreShowTime() - utils.getNow())
                self.timer = BigWorld.callback(startTime - self.getPreShowTime() - utils.getNow(), self.show)
            return

    def handleBtnClick(self, *args):
        p = BigWorld.player()
        if getattr(p, 'schoolTopStage', {}).get(p.school, None) not in (gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE, gametypes.SCHOOL_TOP_STAGE_MATCH_START, gametypes.SCHOOL_TOP_STAGE_OVER):
            p.showGameMsg(GMDD.data.SCHOOL_TOP_MATCH_NOT_START, ())
            return
        else:
            gameglobal.rds.ui.schoolTopFight.show()
            return
