#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonOverviewProxy.o
import time
import BigWorld
import gameglobal
import gametypes
import uiConst
import utils
import gamelog
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis import events
from uiProxy import UIProxy
from data import duel_config_data as DCD
from gamestrings import gameStrings
ZHENGYING_NUM = 4
STATE_NUM = 4

class BalanceArena2PersonOverviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonOverviewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        self.requireVoteData()

    def requireVoteData(self):
        p = BigWorld.player()
        p.cell.dArenaSyncCampInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.startBtn.addEventListener(events.BUTTON_CLICK, self.onStartBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick, False, 0, True)
        self.widget.zhanBaoBtn.addEventListener(events.BUTTON_CLICK, self.onZhanBaoBtnClick, False, 0, True)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick, False, 0, True)
        self.widget.introText.htmlText = DCD.data.get('doubleArenaIntroduction', '')
        self.initZhenYing()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshMatchTime()
        self.refreshVoteInfo()
        if self.isInState16():
            if not gameglobal.rds.configData.get('enableDoubleArena16QiangZhanBao', True):
                self.widget.zhanBaoBtn.visible = False
            else:
                self.widget.zhanBaoBtn.visible = True
        elif not gameglobal.rds.configData.get('enableDoubleArenaZhanBao', False):
            self.widget.zhanBaoBtn.visible = False
        else:
            self.widget.zhanBaoBtn.visible = True

    def refreshVoteInfo(self):
        p = BigWorld.player()
        campInfo = getattr(p, 'doubleArenaCampInfo', {})
        for i in xrange(ZHENGYING_NUM):
            zhenyingMc = self.widget.getChildByName('zhenying%s' % str(i))
            zhenyingMc.voteMc.hotText.text = gameStrings.DOUBLEARENA_VOTESTR % str(campInfo.get(i + 1, 0))

    def getStartTimes(self):
        p = BigWorld.player()
        return getattr(p, 'stateStartTimes', [0,
         0,
         0,
         0])

    def getCurrentState(self):
        p = BigWorld.player()
        return getattr(p, 'doubleArenaState', gametypes.DOUBLE_ARENA_STATE_CLOSE)

    def refreshMatchTime(self):
        if not self.widget:
            return
        currentState = self.getCurrentState() - 1
        stateTimes = self.getStartTimes()
        for i in xrange(STATE_NUM):
            if i == currentState:
                self.widget.getChildByName('state%s' % str(i)).gotoAndStop('dangqian')
            else:
                self.widget.getChildByName('state%s' % str(i)).gotoAndStop('yihou')
            if i < currentState:
                self.widget.getChildByName('time%s' % str(i)).text = gameStrings.DOUBLEARENA_STATE_OVER
            else:
                stateTime = stateTimes[i]
                timeTuple = utils.getTimeTuple(stateTime)
                timeStr = time.strftime('%Y-%m-%d', timeTuple)
                self.widget.getChildByName('time%s' % str(i)).text = timeStr

    def initZhenYing(self):
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        for i in xrange(ZHENGYING_NUM):
            zhenyingMc = self.widget.getChildByName('zhenying%s' % str(i))
            zhenyingInfo = zhenyingInfos.get(i + 1, {})
            if zhenyingMc:
                zhenyingMc.icon.addEventListener(events.MOUSE_ROLL_OVER, self.showDetail, False, 0, True)
                zhenyingMc.icon.addEventListener(events.MOUSE_ROLL_OUT, self.hideDetail, False, 0, True)
                ASUtils.setHitTestDisable(zhenyingMc.world, True)
                zhenyingMc.voteMc.voteBtn.camp = i + 1
                zhenyingMc.voteMc.voteBtn.addEventListener(events.MOUSE_CLICK, self.onVoteBtnClick, False, 0, True)
                zhenyingMc.world.visible = False
                zhenyingMc.world.textField.htmlText = zhenyingInfo.get('detail', '.....')
                zhenyingMc.nameMc.textField.htmlText = zhenyingInfo.get('name', 'XXXX')
                zhenyingMc.icon.fitSize = True
                zhenyingMc.icon.loadImage(zhenyingInfo.get('photo', None))

    def onVoteBtnClick(self, *args):
        e = ASObject(args[3][0])
        camp = int(e.target.camp)
        gamelog.debug('dxk@balanceArena2PersonOverviewProxy vote for:', camp)
        p = BigWorld.player()
        p.cell.dArenaVoteForCamp(camp)

    def showDetail(self, *args):
        e = ASObject(args[3][0])
        e.target.parent.world.visible = True

    def hideDetail(self, *args):
        e = ASObject(args[3][0])
        e.target.parent.world.visible = False

    def isInState16(self):
        p = BigWorld.player()
        return p.isInDoubleArenaState16() or p.isInDoubleArenaStateEnd()

    def onStartBtnClick(self, *args):
        gameglobal.rds.ui.balanceArena2Person.selectSubTab(1)

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.balanceArena2PersonReward.show()

    def onZhanBaoBtnClick(self, *args):
        if not self.isInState16():
            gameglobal.rds.ui.balanceArena2PersonZhanBao.show()
        else:
            gameglobal.rds.ui.balanceArena2PersonInfo.show()

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_DOUBLE_ARENA_SCORE)
