#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaVoteProxy.o
import BigWorld
import uiConst
import events
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from Queue import Queue
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import dota_battle_field_report_data as DBFRD

class BfDotaVoteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaVoteProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.voteQueue = Queue()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_DOTA_VOTE, self.hide)

    def reset(self):
        self.widget = None
        self.curInfo = {}
        self.voteTime = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_VOTE:
            self.widget = widget
            self.widget.visible = False
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_VOTE)

    def show(self):
        p = BigWorld.player()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_VOTE)
        else:
            self.initUI()

    def initUI(self):
        self.widget.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.mainMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.voteQueue.empty():
            self.widget.visible = False
            return
        info = self.voteQueue.get()
        if not info:
            self.widget.visible = False
            return
        self.curInfo = info
        if info['isTeamMate']:
            team = gameStrings.BF_DOTA_VOTE_TEAM_MATE
        else:
            team = gameStrings.BF_DOTA_VOTE_TEAM_ENERMY
        self.widget.mainMc.msg.htmlText = SCD.data.get('BF_DOTA_VOTE_MSG', gameStrings.BF_DOTA_VOTE_MSG) % (team, info.get('roleName'), info.get('voteTypeDesc'))
        self.widget.visible = True
        self.voteTime = DBFRD.data.get('voteTime', 20)
        self.countdown()

    def handleConfirmBtnClick(self, *args):
        BigWorld.player().cell.commitDotaBFVoteResult(self.curInfo['gbId'], True, self.curInfo['voteType'])
        self.hideWidget()

    def handleCancelBtnClick(self, *args):
        BigWorld.player().cell.commitDotaBFVoteResult(self.curInfo['gbId'], False, self.curInfo['voteType'])
        self.hideWidget()

    def addVoteInfo(self, gbId, roleName, voteType):
        info = {}
        info['gbId'] = gbId
        info['roleName'] = roleName
        voteTypeDesc = DBFRD.data.get('voteTypeDesc')
        info['voteType'] = voteType
        info['voteTypeDesc'] = ''
        if voteTypeDesc:
            info['voteTypeDesc'] = voteTypeDesc.get(voteType, '')
        info['isTeamMate'] = self.isTeamMate(gbId)
        self.voteQueue.put(info)
        if self.widget and not self.widget.visible:
            self.refreshInfo()

    def hideWidget(self):
        self.widget.visible = False
        self.refreshInfo()

    def countdown(self):
        if not self.widget or not self.widget.visible:
            self.voteTime = 0
            return
        if self.voteTime > 0:
            self.widget.mainMc.countdown.text = self.voteTime
            self.voteTime -= 1
            BigWorld.callback(1, self.countdown)
        else:
            self.hideWidget()

    def isTeamMate(self, gbId):
        idList = self.getTeammateGbIdList()
        if gbId in idList:
            return True
        return False

    def getTeammateGbIdList(self):
        idList = []
        p = BigWorld.player()
        for gbId, mInfo in p.battleFieldTeam.iteritems():
            if mInfo['sideNUID'] == p.bfSideNUID:
                idList.append(gbId)

        return idList
