#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/scoreInfoProxy.o
import BigWorld
import uiUtils
import uiConst
import events
import const
from uiProxy import UIProxy
from guis.asObject import ASObject
from cdata import game_msg_def_data as GMDD
RESULT_TIE = 0
RESULT_PROTECT_WIN = 1
RESULT_SPRITE_WIN = 2
RESULT_NOT_END = 3

class ScoreInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ScoreInfoProxy, self).__init__(uiAdapter)
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.spriteList = []
        self.protecterList = []
        self.spriteTotalScore = 0
        self.protecterTotalScore = 0
        self.result = None
        self.maxSideNum = 0

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_SCORE_INFO)

    def clearWidget(self):
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCORE_INFO)

    def _getFrameInfo(self):
        p = BigWorld.player()
        if not hasattr(p, 'bfSideIndex') or not hasattr(p, 'bfSideNUID'):
            return
        if not getattr(p, 'bfResultInfo'):
            self.result = RESULT_NOT_END
        elif p.bfResult == const.TIE:
            self.result = RESULT_TIE
        elif p.bfResult == const.LOSE:
            if p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
                self.result = RESULT_SPRITE_WIN
            else:
                self.result = RESULT_PROTECT_WIN
        elif p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            self.result = RESULT_PROTECT_WIN
        else:
            self.result = RESULT_SPRITE_WIN
        self.protecterList = []
        self.spriteList = []
        selfSideNUID = p.bfSideNUID
        if p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            selfSideList = self.protecterList
            anotherSideList = self.spriteList
        else:
            selfSideList = self.spriteList
            anotherSideList = self.protecterList
        for gbId, mInfo in p.battleFieldTeam.iteritems():
            memberInfo = {}
            memberInfo['name'] = mInfo['roleName']
            memberInfo['score'] = getattr(p, 'bfScoreList', {}).get(gbId, 0)
            if mInfo['sideNUID'] == selfSideNUID:
                selfSideList.append(memberInfo)
                continue
            anotherSideList.append(memberInfo)

        self.spriteTotalScore = 0
        self.protecterTotalScore = 0
        self.spriteList.sort(lambda x, y: cmp(y['score'], x['score']))
        self.protecterList.sort(lambda x, y: cmp(y['score'], x['score']))
        len0 = len(self.spriteList)
        len1 = len(self.protecterList)
        self.maxSideNum = max(len0, len1)
        self.protecterTotalScore, self.spriteTotalScore = self.uiAdapter.littleScoreInfo.getTotalScore()

    def labelFunc(self, *args):
        i = int(args[3][0].GetNumber())
        memberMc = ASObject(args[3][1])
        memberMc.lName.multiline = False
        memberMc.rName.multiline = False
        if i < len(self.protecterList):
            memberMc.lName.text = self.protecterList[i]['name']
            memberMc.lScore.text = str(self.protecterList[i]['score'])
        else:
            memberMc.lName.text = ''
            memberMc.lScore.text = ''
        if i < len(self.spriteList):
            memberMc.rName.text = self.spriteList[i]['name']
            memberMc.rScore.text = str(self.spriteList[i]['score'])
            memberMc.rScore.text = str(self.spriteList[i]['score'])
        else:
            memberMc.rName.text = ''
            memberMc.rScore.text = ''

    def refreshFrame(self):
        if not self.widget:
            return None
        else:
            self._getFrameInfo()
            self.widget.mainFrame.playerList.dataArray = range(self.maxSideNum)
            if self.result == RESULT_NOT_END:
                self.widget.mainFrame.sprite.gotoAndStop('not end')
                self.widget.mainFrame.protecter.gotoAndStop('not end')
            elif self.result == RESULT_TIE:
                self.widget.mainFrame.sprite.gotoAndStop('tie')
                self.widget.mainFrame.protecter.gotoAndStop('tie')
            elif self.result == RESULT_PROTECT_WIN:
                self.widget.mainFrame.protecter.gotoAndStop('win')
                self.widget.mainFrame.sprite.gotoAndStop('lose')
            else:
                self.widget.mainFrame.sprite.gotoAndStop('win')
                self.widget.mainFrame.protecter.gotoAndStop('lose')
            self.widget.mainFrame.sprite.frame.score.text = str(self.spriteTotalScore)
            self.widget.mainFrame.protecter.frame.score.text = str(self.protecterTotalScore)
            return None

    def _initUI(self):
        self.widget.removeAllInst(self.widget.mainFrame.playerList.canvas, True)
        self.widget.mainFrame.playerList.itemHeight = 31
        self.widget.mainFrame.playerList.itemRenderer = 'ScoreInfo_SinglePlayer'
        self.widget.mainFrame.playerList.lableFunction = self.labelFunc
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick, False, 0, True)
        self.widget.leaveBtn.addEventListener(events.MOUSE_CLICK, self.onLeaveClick, False, 0, True)

    def onCloseClick(self, *args):
        self.hide()

    def onLeaveClick(self, *args):
        p = BigWorld.player()
        if self.uiAdapter.topBar.isQuitBF:
            p.cell.quitBattleField()
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_BATTLE_FIELD_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitBattleField)
        self.hide()
