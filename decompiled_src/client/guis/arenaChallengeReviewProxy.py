#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaChallengeReviewProxy.o
import BigWorld
import math
import gametypes
import uiConst
import utils
import events
import gamelog
import const
import gameglobal
from uiTabProxy import UITabProxy
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from random import choice
from cdata import game_msg_def_data as GMDD
from data import duel_config_data as DCD
from data import arena_mode_data as AMD
TAB_REVIEWPANEL0_INDEX = 0
TAB_REVIEWPANEL1_INDEX = 1
TAB_LIST = [{'tabIdx': TAB_REVIEWPANEL0_INDEX,
  'tabName': 'tabBtn0',
  'view': 'ArenaChallengeReview_ReViewPanelMc0',
  'pos': (28, 85)}, {'tabIdx': TAB_REVIEWPANEL1_INDEX,
  'tabName': 'tabBtn1',
  'view': 'ArenaChallengeReview_ReViewPanelMc1',
  'pos': (28, 85)}]
DEF_SELIDX = -1
MIN_PAGE = 1
MAX_ITEM_PERPAGE = 6
MAX_PLAYER_SIDE = 5
MAX_PLAYER_NUM = 10
ARENA_STAGE = [gametypes.CROSS_ARENA_CHALLENGE_STAGE_RUNNING, gametypes.CROSS_ARENA_CHALLENGE_STAGE_END]
HOTDEGREE_STAGE = DCD.data.get('hotDegreeStageNumber', (1, 2))
INFO_P1P2_KEY_IDX = 0
INFO_DATA_VALUE_IDX = 1

class ArenaChallengeReviewProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(ArenaChallengeReviewProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.reset()
        self.versions = [0, 0]
        self.curInfo = []
        self.playingInfo = []
        self.reviewInfo = []
        self.localPlayingInfo = []
        self.localReviewInfo = []
        self.infos = [self.playingInfo, self.reviewInfo]
        self.localServerInfos = [self.localPlayingInfo, self.localReviewInfo]
        self.selItemKey = [self.selPlayingItemKey, self.selEndItemKey]
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENACHALLENGE_REVIEW, self.hide)

    def reset(self):
        super(ArenaChallengeReviewProxy, self).reset()
        self.curPage = MIN_PAGE
        self.maxPage = MIN_PAGE
        self.isLocalServerOnly = False
        self.tabData = None
        self.selPlayingItemKey = None
        self.selEndItemKey = None
        self.lastSelIdx = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENACHALLENGE_REVIEW:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(ArenaChallengeReviewProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENACHALLENGE_REVIEW)

    def _getTabList(self):
        return TAB_LIST

    def show(self, showTabIndex = -1, gbIdSrc = 0, gbIdTgt = 0, tStart = 0):
        if not gameglobal.rds.configData.get('enableArenaChallenge', False):
            BigWorld.player().showGameMsgEx(GMDD.data.ARENA_CHALLENGE_NOT_OPEN, ())
            return
        if gbIdSrc and gbIdTgt:
            self.selItemKey[showTabIndex] = (gbIdSrc, gbIdTgt, tStart)
        if not self.widget:
            self.showTabIndex = showTabIndex
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENACHALLENGE_REVIEW)
        else:
            self.refreshInfo(showTabIndex)

    def refreshInfo(self, showTabIndex):
        if showTabIndex == -1:
            return
        if self.currentTabIndex == showTabIndex:
            self.refreshTab()
        else:
            self.widget.setTabIndex(showTabIndex)

    def initUI(self):
        self.itemMcNames = [ 'matchItem%d' % n for n in xrange(MAX_ITEM_PERPAGE) ]
        self.playerMcName = [ 'p%d' % n for n in xrange(MAX_PLAYER_NUM) ]
        self.widget.localServerOnlyCheckBox.selected = self.isLocalServerOnly
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.pageInput.textField.restrict = '0-9'
        self.widget.pageInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleEnterInput, False, 0, True)
        self.widget.pageInput.addEventListener(events.EVENT_CHANGE, self.handlePageInputChange, False, 0, True)
        self.widget.localServerOnlyCheckBox.addEventListener(events.EVENT_SELECT, self.handleCheckBoxSelected, False, 0, True)
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_REVIEWPANEL0_INDEX)
        else:
            self.widget.setTabIndex(self.showTabIndex)

    def refreshSelIdx(self, newSelIdx):
        if self.lastSelIdx == newSelIdx:
            return
        if self.lastSelIdx != -1:
            itemMc = getattr(self.currentView, self.itemMcNames[self.lastSelIdx])
            itemMc.selectMc.visible = False
            itemMc.overMc.visible = False
        if 0 <= newSelIdx < MAX_ITEM_PERPAGE:
            itemMc = getattr(self.currentView, self.itemMcNames[newSelIdx])
            itemMc.selectMc.visible = True
            itemMc.overMc.visible = True
        self.lastSelIdx = newSelIdx

    def handleClickMatchItem(self, *args):
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.name[-1:])
        self.refreshSelIdx(idx)
        self.selItemKey[self.currentTabIndex] = None

    def handleShareBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemPageIdx = int(e.currentTarget.parent.name[-1])
        itemTrueIdx = (self.curPage - 1) * MAX_ITEM_PERPAGE + itemPageIdx
        if len(self.curInfo) <= itemTrueIdx:
            gamelog.error('handleEnterReviewBtnClick idx >= len(curInfo)')
        else:
            linkParams = [self.currentTabIndex]
            if self.currentTabIndex == TAB_REVIEWPANEL0_INDEX:
                linkParams.extend(self.getPlayingLinkParams(itemTrueIdx))
                msg = DCD.data.get('sharePlayingLinkText', '%d %d %d %d %s %s %s') % tuple(linkParams)
            else:
                linkParams.extend(self.getEndLinkParams(itemTrueIdx))
                msg = DCD.data.get('shareEndLinkText', '%d %d %d %d %s %s %d %d %s') % tuple(linkParams)
            self.uiAdapter.sendLink(msg)

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        if self.lastSelIdx != int(e.currentTarget.name[-1]):
            e.currentTarget.overMc.visible = False

    def handleCheckBoxSelected(self, *args):
        e = ASObject(args[3][0])
        self.isLocalServerOnly = e.currentTarget.selected
        self.refreshTab()

    def handlePageInputChange(self, *args):
        e = ASObject(args[3][0])
        inputPage = e.currentTarget.text
        if not inputPage:
            return
        maxPage = int(self.widget.pageText.text[1:])
        if int(inputPage) > maxPage:
            e.currentTarget.text = maxPage

    def handleEnterReviewBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemPageIdx = int(e.currentTarget.parent.name[-1])
        itemTrueIdx = (self.curPage - 1) * MAX_ITEM_PERPAGE + itemPageIdx
        if len(self.curInfo) <= itemTrueIdx:
            gamelog.error('handleEnterReviewBtnClick idx >= len(curInfo)')
        else:
            gbIdList = self.curInfo[itemTrueIdx][INFO_P1P2_KEY_IDX]
            p = BigWorld.player()
            if p.gbId in gbIdList and p.arenaChallengeStatus in [gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC, gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY_SUCC]:
                p.showGameMsg(GMDD.data.ARENA_CHALLENGE_CANNOT_REVIEW, ())
            else:
                BigWorld.player().cell.enterArenaChallengeWithLive(choice(gbIdList))

    def handleEnterInput(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            newPage = int(e.currentTarget.text) if e.currentTarget.text else MIN_PAGE
            self.gotoPageByUser(newPage)

    def _onHeadBtnClick(self, e):
        self.gotoPageByUser(MIN_PAGE)

    def _onPrevBtnClick(self, e):
        self.gotoPageByUser(self.curPage - 1)

    def _onNextBtnClick(self, e):
        self.gotoPageByUser(self.curPage + 1)

    def _onTailBtnClick(self, e):
        self.gotoPageByUser(self.maxPage)

    def gotoPageByUser(self, newPage):
        self.selItemKey[self.currentTabIndex] = None
        self.gotoPage(newPage)

    def onTabChanged(self, *args):
        super(ArenaChallengeReviewProxy, self).onTabChanged(*args)
        self.queryArenaChallengeInfo()
        self.resetTabUI()
        self.refreshTab()

    def resetTabUI(self):
        for itemMcName in self.itemMcNames:
            itemMc = getattr(self.currentView, itemMcName)
            itemMc.overMc.visible = False
            itemMc.selectMc.visible = False
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickMatchItem, False, 0, True)
            itemMc.addEventListener(events.MOUSE_OVER, self.handleMouseOver, False, 0, True)
            itemMc.addEventListener(events.MOUSE_OUT, self.handleMouseOut, False, 0, True)
            itemMc.shareBtn.addEventListener(events.MOUSE_CLICK, self.handleShareBtnClick, False, 0, True)
            if itemMc.reviewBtn:
                itemMc.reviewBtn.addEventListener(events.MOUSE_CLICK, self.handleEnterReviewBtnClick, False, 0, True)

    def refreshTab(self):
        if not self.widget:
            return
        if not self.currentView:
            return
        self.curInfo = self.localServerInfos[self.currentTabIndex] if self.isLocalServerOnly else self.infos[self.currentTabIndex]
        self.initPageInfo()
        selPage, selIdx = self.getSelItemPos(self.selItemKey[self.currentTabIndex])
        self.gotoPage(selPage, selIdx)

    def onArenaChallengeInfoQuery(self, qType, version, info):
        if ARENA_STAGE[self.currentTabIndex] != qType:
            return
        self.versions[self.currentTabIndex] = version
        self.infos[self.currentTabIndex] = self.processData(info)
        self.localServerInfos[self.currentTabIndex] = self.getLocalServerInfo()
        self.refreshTab()

    def processData(self, info):
        dataList = [ [k, item] for k, v in info.iteritems() for item in v ]
        sortedData = sorted(dataList, key=lambda d: d[1].get('tStart'), reverse=True)
        return sortedData

    def getLocalServerInfo(self):
        return [ item for item in self.infos[self.currentTabIndex] if utils.getHostId() in [ team.get('hostId') for team in item[1].get('teamPair', {}) ] ]

    def queryArenaChallengeInfo(self):
        if self.currentTabIndex == TAB_REVIEWPANEL0_INDEX:
            BigWorld.player().cell.queryRunningArenaChallengeInfo(self.versions[self.currentTabIndex])
        elif self.currentTabIndex == TAB_REVIEWPANEL1_INDEX:
            BigWorld.player().cell.queryEndArenaChallengeInfo(self.versions[self.currentTabIndex])

    def initPageInfo(self):
        maxDataPage = int(math.ceil(float(len(self.curInfo)) / MAX_ITEM_PERPAGE))
        self.maxPage = max(maxDataPage, MIN_PAGE)
        pageInfoVisible = self.maxPage > MIN_PAGE
        self.widget.pageInput.visible = pageInfoVisible
        self.widget.pageText.visible = pageInfoVisible
        self.widget.prevBtn.visible = pageInfoVisible
        self.widget.headBtn.visible = pageInfoVisible
        self.widget.nextBtn.visible = pageInfoVisible
        self.widget.tailBtn.visible = pageInfoVisible
        if pageInfoVisible:
            self.widget.pageText.text = '/%d' % self.maxPage

    def refreshPageBottomInfo(self):
        self.widget.pageInput.text = self.curPage
        self.widget.prevBtn.enabled = self.curPage > MIN_PAGE
        self.widget.headBtn.enabled = self.curPage > MIN_PAGE
        self.widget.nextBtn.enabled = self.curPage < self.maxPage
        self.widget.tailBtn.enabled = self.curPage < self.maxPage

    def getSelItemPos(self, selItemKey):
        selPage = MIN_PAGE
        curPageSelIdx = DEF_SELIDX
        if selItemKey:
            if self.currentTabIndex == TAB_REVIEWPANEL0_INDEX:
                selIdx = [ idx for idx, item in enumerate(self.curInfo) if self.isTab0SelItem(item, selItemKey) ]
            elif self.currentTabIndex == TAB_REVIEWPANEL1_INDEX:
                selIdx = [ idx for idx, item in enumerate(self.curInfo) if self.isTab1SelItem(item, selItemKey) ]
            else:
                selIdx = []
            if selIdx:
                selPage = selIdx[0] / MAX_ITEM_PERPAGE + 1
                curPageSelIdx = selIdx[0] % MAX_ITEM_PERPAGE
        return (selPage, curPageSelIdx)

    def isTab0SelItem(self, item, selItemKey):
        return item[INFO_P1P2_KEY_IDX] == selItemKey[:2]

    def isTab1SelItem(self, item, selItemKey):
        return item[INFO_DATA_VALUE_IDX].get('tStart') == selItemKey[2] and item[INFO_P1P2_KEY_IDX] == selItemKey[:2]

    def gotoPage(self, newPage, selIdx = DEF_SELIDX):
        newPage = min(max(newPage, MIN_PAGE), self.maxPage)
        self.curPage = newPage
        self.refreshPanel(newPage)
        self.refreshSelIdx(selIdx)
        self.refreshPageBottomInfo()

    def refreshPanel(self, pageIdx):
        refreshItemFunc = None
        if self.currentTabIndex == TAB_REVIEWPANEL0_INDEX:
            refreshItemFunc = self.refreshPlayingItem
        elif self:
            refreshItemFunc = self.refreshReviewItem
        self.earlyItemCnt = len(self.curInfo) - (pageIdx - 1) * MAX_ITEM_PERPAGE
        curPageItemCnt = MAX_ITEM_PERPAGE if self.earlyItemCnt > MAX_ITEM_PERPAGE else self.earlyItemCnt
        for i in xrange(MAX_ITEM_PERPAGE):
            itemMc = getattr(self.currentView, self.itemMcNames[i], None)
            if i < curPageItemCnt:
                itemMc.visible = True
                itemDataIdx = (pageIdx - 1) * MAX_ITEM_PERPAGE + i
                refreshItemFunc(itemMc, itemDataIdx)
            else:
                itemMc.visible = False

    def refreshPlayingItem(self, itemMc, i):
        if i >= len(self.curInfo):
            return
        itemData = self.curInfo[i]
        self.refreshCommonInfo(itemMc, itemData)

    def refreshReviewItem(self, itemMc, i):
        if i >= len(self.curInfo):
            return
        itemData = self.curInfo[i]
        teamsData = itemData[INFO_DATA_VALUE_IDX].get('teamPair')
        score = (teamsData[0].get('winCnt', 0), teamsData[1].get('winCnt', 0))
        itemMc.matchResultText.text = '%d : %d' % score
        itemMc.matchResultMc.gotoAndPlay(self.getResultFrameName(score))
        self.refreshCommonInfo(itemMc, itemData)

    def refreshCommonInfo(self, itemMc, itemData):
        teamsData = itemData[INFO_DATA_VALUE_IDX].get('teamPair')
        mainPlayersGbId = itemData[INFO_P1P2_KEY_IDX]
        self.refreshTeamData(itemMc, teamsData, mainPlayersGbId, 0)
        self.refreshTeamData(itemMc, teamsData, mainPlayersGbId, 1)
        frameName = self.getHotDegreeFrameName(itemData[INFO_DATA_VALUE_IDX].get('liveCnt', 0))
        itemMc.hotDegreeIcon.gotoAndStop(frameName)

    def refreshTeamData(self, itemMc, teamsData, mainPlayersGbId, teamIdx):
        team = teamsData[teamIdx]
        serverName = utils.getServerName(team.get('hostId'))
        idx = teamIdx * MAX_PLAYER_SIDE - 1
        teamNameMc = getattr(itemMc, 'teamText%d' % teamIdx, None)
        for gbId, pInfo in team.get('members', {}).iteritems():
            idx += 1
            playerMc = getattr(itemMc, self.playerMcName[idx], None)
            school = const.SCHOOL_DICT.get(pInfo.get('school'))
            lv = pInfo.get('lv')
            roleName = pInfo.get('roleName')
            tipString = gameStrings.ARENA_CHALLENGE_REVIEW_TIPSTRING % (roleName,
             lv,
             school,
             serverName)
            TipManager.addTip(playerMc, tipString)
            playerMc.visible = True
            schoolFrameName = uiConst.SCHOOL_FRAME_DESC.get(pInfo.get('school'))
            playerMc.school.gotoAndStop(schoolFrameName)
            if gbId in mainPlayersGbId:
                teamNameMc.text = gameStrings.ARENA_CHALLENGE_REVIEW_TEAMNAME % roleName
                playerMc.leaderIcon.visible = True
            else:
                playerMc.leaderIcon.visible = False

        curPageLastItemIdx = (teamIdx + 1) * MAX_PLAYER_SIDE - 1
        for i in xrange(idx, curPageLastItemIdx):
            idx += 1
            playerMc = getattr(itemMc, self.playerMcName[idx], None)
            playerMc.visible = False

    def getPlayingLinkParams(self, itemTrueIdx):
        gbIdSrc, gbIdTgt = self.curInfo[itemTrueIdx][INFO_P1P2_KEY_IDX]
        info = self.curInfo[itemTrueIdx][INFO_DATA_VALUE_IDX]
        tStart = info.get('tStart')
        teamData = info.get('teamPair', ({}, {}))
        srcRoleName = teamData[0].get('members', {}).get(gbIdSrc).get('roleName')
        tgtRoleName = teamData[1].get('members', {}).get(gbIdTgt).get('roleName')
        modeName = AMD.data.get(info.get('arenaMode')).get('modeName')
        return (gbIdSrc,
         gbIdTgt,
         tStart,
         modeName,
         srcRoleName,
         tgtRoleName)

    def getEndLinkParams(self, itemTrueIdx):
        gbIdSrc, gbIdTgt = self.curInfo[itemTrueIdx][INFO_P1P2_KEY_IDX]
        info = self.curInfo[itemTrueIdx][INFO_DATA_VALUE_IDX]
        tStart = info.get('tStart')
        teamData = info.get('teamPair', ({}, {}))
        score0 = teamData[0].get('winCnt', 0)
        score1 = teamData[1].get('winCnt', 0)
        srcRoleName = teamData[0].get('members', {}).get(gbIdSrc).get('roleName')
        tgtRoleName = teamData[1].get('members', {}).get(gbIdTgt).get('roleName')
        modeName = AMD.data.get(info.get('arenaMode')).get('modeName')
        return (gbIdSrc,
         gbIdTgt,
         tStart,
         modeName,
         srcRoleName,
         score0,
         score1,
         tgtRoleName)

    def getResultFrameName(self, score):
        if score[0] > score[1]:
            return 'shengli'
        elif score[0] < score[1]:
            return 'fu'
        else:
            return 'ping'

    def getHotDegreeFrameName(self, liveCnt):
        if liveCnt < HOTDEGREE_STAGE[0]:
            return 'wu'
        elif HOTDEGREE_STAGE[0] <= liveCnt < HOTDEGREE_STAGE[1]:
            return 'renao'
        elif HOTDEGREE_STAGE[1] <= liveCnt < const.CROSS_ARENA_CHALLENGE_MAX_LIVE_NUM:
            return 'huobao'
        else:
            return 'yongji'
