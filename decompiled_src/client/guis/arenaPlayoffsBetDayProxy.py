#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetDayProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import events
import uiConst
import random
import utils
import time
import ui
import const
import copy
import datetime
import duelUtils
import formula
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import MenuManager
from data import duel_config_data as DCD
from data import arena_playoffs_bet_time_data as APBTD
from data import arena_playoffs_5v5_bet_time_data as AP5BTD
from gamestrings import gameStrings
GROUP_MATCH_END_ROUND = 4

class ArenaPlayoffsBetDayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetDayProxy, self).__init__(uiAdapter)
        self.widget = None
        self.lvKey = ''
        self.betId = 0
        self.teamList = []
        self.ansList = []
        self.history = {}
        self.fisrtShow = {}
        self.lastConfirmHistory = {}
        self.betTimeDatas = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initBetTime()
        self.initUI()
        self.queryInfo()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def reset(self):
        self.history = {}
        self.fisrtShow = {}

    def clearAll(self):
        self.lastConfirmHistory = {}

    def initBetTime(self):
        currentSeason = formula.getPlayoffsSeason()
        self.betTimeDatas = {}
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            betSchedule = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_5V5
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
        elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            betSchedule = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_BALANCE
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS
        else:
            if not gameglobal.rds.configData.get('enableArenaPlayoffs', False):
                return
            betSchedule = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
        for key in betSchedule.keys():
            if key[0] != gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL:
                continue
            betTimeData = {}
            crontab = []
            tBetEnd = []
            tBetTimeDesc = []
            tBetStart = []
            for lvKeyIndex, lvKey in enumerate(lvKeys):
                calcCrontab = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'crontab', lvKey)
                calcBetEnd = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'tBetEnd', lvKey)
                calcBetStart = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'tBetStart', lvKey)
                crontab.append(calcCrontab)
                tBetEnd.append(calcBetEnd)
                tBetStart.append(calcBetStart)
                startDesc = time.strftime('%m/%d %H:%M', time.localtime(utils.getDisposableCronTabTimeStamp(calcBetStart)))
                endDesc = time.strftime('%m/%d %H:%M', time.localtime(utils.getDisposableCronTabTimeStamp(calcBetEnd)))
                descText = '%s-%s' % (startDesc, endDesc)
                tBetTimeDesc.append(descText)

            betTimeData['crontab'] = crontab
            betTimeData['tBetTimeDesc'] = tBetTimeDesc
            betTimeData['tBetEnd'] = tBetEnd
            betTimeData['tBetStart'] = tBetStart
            self.betTimeDatas[key] = betTimeData

    def initUI(self):
        self.widget.mainMc.helpIcon.helpKey = 302
        self.widget.mainMc.lvDropdown.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.hanldleLvKeyChange, False, 0, True)
        now = utils.getNow()
        p = BigWorld.player()
        if gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            self.lvKey = gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE
            self.widget.mainMc.lvDropdown.visible = False
        else:
            self.widget.mainMc.lvDropdown.visible = True
            firstSelectedIndex = -1
            bestLvSelectedIndex = -1
            lvList = []
            if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                keys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
            else:
                keys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
            for index, lvKey in enumerate(keys):
                betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, 0)
                betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, betId)
                apbtData = APBTD.data.get(betKey, {})
                if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                    apbtData = AP5BTD.data.get(betKey, {})
                if self.betTimeDatas.has_key('tBetEnd') and utils.getDisposableCronTabTimeStamp(self.betTimeDatas['tBetEnd'][index]) > now:
                    if firstSelectedIndex == -1:
                        firstSelectedIndex = index
                    lvKeyDatas = lvKey.split('_')
                    minLv, maxLv = lvKeyDatas[-2], lvKeyDatas[-1]
                    if p.lv >= int(minLv) and p.lv <= int(maxLv):
                        bestLvSelectedIndex = index
                elif apbtData.has_key('tBetEnd') and utils.getDisposableCronTabTimeStamp(apbtData['tBetEnd'][index]) > now:
                    if firstSelectedIndex == -1:
                        firstSelectedIndex = index
                    lvKeyDatas = lvKey.split('_')
                    minLv, maxLv = lvKeyDatas[-2], lvKeyDatas[-1]
                    if p.lv >= int(minLv) and p.lv <= int(maxLv):
                        bestLvSelectedIndex = index
                lvInfo = {}
                lvInfo['label'] = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_144 % lvKey.replace('_', '-')
                lvInfo['lvKey'] = lvKey
                lvList.append(lvInfo)

            ASUtils.setDropdownMenuData(self.widget.mainMc.lvDropdown, lvList)
            self.widget.mainMc.lvDropdown.menuRowCount = min(len(lvList), 5)
            if self.widget.mainMc.lvDropdown.selectedIndex == -1:
                if bestLvSelectedIndex != -1:
                    self.widget.mainMc.lvDropdown.selectedIndex = bestLvSelectedIndex
                elif firstSelectedIndex != -1:
                    self.widget.mainMc.lvDropdown.selectedIndex = firstSelectedIndex
                elif len(lvList) > 0:
                    self.widget.mainMc.lvDropdown.selectedIndex = 0
            elif self.widget.mainMc.lvDropdown.selectedIndex >= len(lvList):
                self.widget.mainMc.lvDropdown.selectedIndex = max(0, len(lvList) - 1)
            self.lvKey = self.widget.mainMc.lvDropdown.dataProvider[self.widget.mainMc.lvDropdown.selectedIndex].lvKey
        self.widget.mainMc.scrollWndList.itemRenderer = 'ArenaPlayoffsBetDay_ScrollWndItem'
        self.widget.mainMc.scrollWndList.lableFunction = self.itemFunction
        self.widget.mainMc.scrollWndList.itemHeight = 34
        self.widget.mainMc.rightDescIcon1.bonusType = 'wudao'
        self.widget.mainMc.rightDescIcon2.bonusType = 'wudao'
        self.widget.mainMc.costAmountIcon.bonusType = 'wudao'
        self.widget.mainMc.totalAmountIcon.bonusType = 'wudao'
        self.widget.mainMc.numStepper.enableMouseWheel = False
        self.widget.mainMc.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        self.widget.mainMc.resetBtn.addEventListener(events.MOUSE_CLICK, self.handleClickResetBtn, False, 0, True)
        self.widget.mainMc.randomBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRandomBtn, False, 0, True)
        self.widget.mainMc.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.mainMc.refreshBtn.addEventListener(events.MOUSE_CLICK, self.hanldleRefreshBtnClick, False, 0, True)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET_START)

    def hanldleLvKeyChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.lvKey = itemMc.dataProvider[itemMc.selectedIndex].lvKey
        self.queryInfo()
        self.refreshInfo()

    def hanldleRefreshBtnClick(self, *args):
        self.queryInfo()
        self.refreshInfo()

    def queryInfo(self):
        p = BigWorld.player()
        version = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('version', 0)
        p.cell.queryArenaPlayoffsBetIdDict(version, self.lvKey)
        version = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(self.lvKey, {}).get('version', 0)
        p.cell.queryArenaPlayoffsTeamsOfLvKey(version, self.lvKey)
        self.betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, 0)
        betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId)
        version = self.uiAdapter.arenaPlayoffsBet.betResultDict.get(self.lvKey, {}).get(betKey, {}).get('betDuelInfo', {}).get('version', 0)
        p.cell.queryArenaPlayoffsDuelBetResult(version, self.lvKey, gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId)
        version = self.uiAdapter.arenaPlayoffsBet.candidateDict.get(self.lvKey, {}).get(betKey, {}).get('version', 0)
        p.cell.queryArenaPlayoffsBetCandidate(version, self.lvKey, gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId)
        version = self.uiAdapter.arenaPlayoffsBet.betFailedCashDict.get('version', 0)
        p.cell.queryArenaPlayoffsBetCalcInfo(version)

    def refreshBetInfo(self, lvKey = ''):
        if not self.widget:
            return
        if lvKey != '' and lvKey != self.lvKey:
            return
        self.betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, 0)
        betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId)
        apbtData = APBTD.data.get(betKey, {})
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            apbtData = AP5BTD.data.get(betKey, {})
        self.widget.mainMc.rightTitle1.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_216
        rightDesc1 = apbtData.get('cashOfsys', 0) + self.uiAdapter.arenaPlayoffsBet.betResultDict.get(self.lvKey, {}).get(betKey, {}).get('lastSeasonRestCash', 0) + self.uiAdapter.arenaPlayoffsBet.betFailedCashDict.get('lastDuelRestCashDict', {}).get((self.lvKey, gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId), {}).get('data', 0)
        self.widget.mainMc.rightDesc1.htmlText = format(rightDesc1, ',')
        ASUtils.autoSizeWithFont(self.widget.mainMc.rightDesc1, 20, 144, 8)
        self.widget.mainMc.rightDesc1.y = 65 + (20 - int(self.widget.mainMc.rightDesc1.getTextFormat().size))
        self.widget.mainMc.rightDescFlag1.x = self.widget.mainMc.rightDesc1.x + self.widget.mainMc.rightDesc1.textWidth + 5
        self.widget.mainMc.rightTitle2.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_226
        if apbtData.get('hasLimit', 0):
            rightDesc2 = DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1) * DCD.data.get('ARENA_PLAYOFFS_BET_REWARD_CASH_MAX_RATIO', 1)
            ASUtils.textFieldAutoSize(self.widget.mainMc.rightDesc2, format(rightDesc2, ','))
            TipManager.addTip(self.widget.mainMc.rightDesc2, DCD.data.get('ARENA_PLAYOFFS_BET_DAY_SIMPLE_TIP', ''))
        else:
            ASUtils.textFieldAutoSize(self.widget.mainMc.rightDesc2, gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_232)
            TipManager.addTip(self.widget.mainMc.rightDesc2, DCD.data.get('ARENA_PLAYOFFS_BET_DAY_NO_LIMIT_SIMPLE_TIP', ''))

    def refreshTotalAmountInfo(self):
        self.widget.mainMc.totalAmount.text = format(BigWorld.player().getFame(const.ARENA_PLAYOFFS_BET_FAME_ID), ',')

    @ui.callInCD(0.5)
    def refreshInfoInCD(self, lvKey = ''):
        self.refreshInfo(lvKey)

    def refreshInfo(self, lvKey = ''):
        if not self.widget:
            return
        if lvKey != '' and lvKey != self.lvKey:
            return
        self.betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, 0)
        betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, self.betId)
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            index = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS.index(self.lvKey)
        elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            index = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS.index(self.lvKey)
        else:
            index = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS.index(self.lvKey)
        apbtTimeData = self.betTimeDatas.get(betKey, {})
        self.refreshBetInfo(lvKey)
        self.widget.mainMc.rightTitle3.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_275
        if apbtTimeData.has_key('tBetTimeDesc'):
            self.widget.mainMc.rightDesc3.text = apbtTimeData['tBetTimeDesc'][index]
        else:
            self.widget.mainMc.rightDesc3.text = ''
        self.widget.mainMc.rightTitle4.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_281
        if apbtTimeData.has_key('crontab'):
            crontab = utils.getDisposableCronTabTimeStamp(apbtTimeData['crontab'][index])
            self.widget.mainMc.rightDesc4.text = time.strftime('%m/%d %H:%M', time.localtime(crontab))
        else:
            self.widget.mainMc.rightDesc4.text = ''
        self.widget.mainMc.rightDesc5.htmlText = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_288 % (DCD.data.get('ARENA_PLAYOFFS_BET_CNT_LIMIT', 0), DCD.data.get('ARENA_PLAYOFFS_BET_MULTIPLE_LIMIT', 0))
        self.widget.mainMc.numStepper.count = 1
        self.widget.mainMc.numStepper.maxCount = DCD.data.get('ARENA_PLAYOFFS_BET_MULTIPLE_LIMIT', 0)
        self.widget.mainMc.numStepper.enableMouseWheel = False
        self.widget.mainMc.costAmount.text = format(DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1), ',')
        teamsInfo = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(self.lvKey, {}).get('info', {})
        candidateList = self.uiAdapter.arenaPlayoffsBet.candidateDict.get(self.lvKey, {}).get(betKey, {}).get('data', [])
        self.teamList = []
        for i in xrange(len(candidateList)):
            cId = candidateList[i]
            teamInfo = {}
            teamInfo['idx'] = i
            teamInfo['cId'] = cId
            teamInfo['teamName0'] = teamsInfo.get(cId[0], {}).get('teamName', '')
            teamInfo['teamName1'] = teamsInfo.get(cId[1], {}).get('teamName', '')
            teamInfo['hostId'] = (teamsInfo.get(cId[0], {}).get('hostId', 0), teamsInfo.get(cId[1], {}).get('hostId', 0))
            teamInfo['serverName0'] = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_304 % utils.getServerName(teamInfo['hostId'][0])
            teamInfo['serverName1'] = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_304 % utils.getServerName(teamInfo['hostId'][1])
            teamInfo['hotFlag0Visible'] = teamsInfo.get(cId[0], {}).get('teamArenaScore', 0) >= teamsInfo.get(cId[1], {}).get('teamArenaScore', 0)
            self.teamList.append(teamInfo)

        self.widget.mainMc.scrollWndList.dataArray = self.teamList
        if self.fisrtShow.get((self.lvKey, self.betId), True) or not self.history.has_key((self.lvKey, self.betId)):
            self.ansList = copy.deepcopy(self.lastConfirmHistory.get((self.lvKey, self.betId), [-1] * len(self.teamList)))
        else:
            self.ansList = copy.deepcopy(self.history.get((self.lvKey, self.betId), [-1] * len(self.teamList)))
        self.fisrtShow[self.lvKey, self.betId] = False
        self.refreshTotalAmountInfo()
        self.updateChooseBtn()

    def updateChooseBtn(self):
        if len(self.teamList):
            self.widget.mainMc.resetBtn.enabled = True
            self.widget.mainMc.randomBtn.enabled = True
        else:
            self.widget.mainMc.resetBtn.enabled = False
            self.widget.mainMc.randomBtn.enabled = False
        for ansIdx in self.ansList:
            if ansIdx == -1:
                self.widget.mainMc.confirmBtn.enabled = False
                break
        else:
            self.widget.mainMc.confirmBtn.enabled = len(self.ansList) > 0

    def updateTeamItem(self, itemMc):
        if not itemMc:
            return
        itemMc.teamName0.htmlText = itemMc.data.teamName0
        itemMc.teamName0.width = itemMc.teamName0.textWidth + 5
        TipManager.addTip(itemMc.teamName0, itemMc.data.serverName0)
        itemMc.teamName1.htmlText = itemMc.data.teamName1
        itemMc.teamName1.width = itemMc.teamName1.textWidth + 5
        TipManager.addTip(itemMc.teamName1, itemMc.data.serverName1)
        tipText = ''
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            tipText = gameStrings.ARENA_PLAYOFFS_5V5_BET_HOT_TEAM_TIPS
        else:
            tipText = DCD.data.get('ARENA_PLAYOFFS_BET_HOT_TEAM_TIPS', '')
        if itemMc.data.hotFlag0Visible:
            itemMc.hotFlag0.visible = True
            itemMc.hotFlag0.x = itemMc.teamName0.x + itemMc.teamName0.textWidth
            TipManager.addTip(itemMc.hotFlag0, tipText)
            itemMc.hotFlag1.visible = False
        else:
            itemMc.hotFlag0.visible = False
            itemMc.hotFlag1.visible = True
            itemMc.hotFlag1.x = itemMc.teamName1.x + itemMc.teamName1.textWidth
            TipManager.addTip(itemMc.hotFlag1, tipText)
        checkIdx = self.ansList[int(itemMc.data.idx)]
        if checkIdx == -1:
            itemMc.checkBox0.selected = False
            itemMc.checkBox1.selected = False
        elif checkIdx == 0:
            itemMc.checkBox0.selected = True
            itemMc.checkBox1.selected = False
        elif checkIdx == 1:
            itemMc.checkBox0.selected = False
            itemMc.checkBox1.selected = True
        itemMc.checkBox0.validateNow()
        itemMc.checkBox1.validateNow()

    def updateTeamList(self):
        wndListItems = self.widget.mainMc.scrollWndList.items
        wndListLen = len(wndListItems)
        for i in xrange(wndListLen):
            self.updateTeamItem(wndListItems[i])

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        ASUtils.setMcData(itemMc, 'data', itemData)
        itemMc.checkBox0.data = 0
        itemMc.checkBox0.addEventListener(events.MOUSE_CLICK, self.handleClickCheckBox, False, 0, True)
        itemMc.checkBox1.data = 1
        itemMc.checkBox1.addEventListener(events.MOUSE_CLICK, self.handleClickCheckBox, False, 0, True)
        self.updateTeamItem(itemMc)
        itemMc.x = 21
        menuParam = {'tId': int(itemData.cId[0]),
         'hostId': int(itemData.hostId[0]),
         'lvKey': self.lvKey}
        MenuManager.getInstance().registerMenuById(itemMc.teamName0, uiConst.MENU_ARENA_PLAYOFFS_BET, menuParam)
        menuParam = {'tId': int(itemData.cId[1]),
         'hostId': int(itemData.hostId[1]),
         'lvKey': self.lvKey}
        MenuManager.getInstance().registerMenuById(itemMc.teamName1, uiConst.MENU_ARENA_PLAYOFFS_BET, menuParam)

    def handleClickCheckBox(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.ansList[int(itemMc.parent.data.idx)] = int(itemMc.data)
        self.updateHistory()
        self.updateChooseBtn()

    def handleClickResetBtn(self, *args):
        self.ansList = [-1] * len(self.teamList)
        self.updateTeamList()
        self.updateChooseBtn()

    def handleClickRandomBtn(self, *args):
        betScoreLen = len(uiConst.ARENA_PLAYOFFS_BET_DAY_SCORE_LIST)
        for i in xrange(len(self.ansList)):
            self.ansList[i] = random.randint(0, betScoreLen - 1)

        self.updateHistory()
        self.updateTeamList()
        self.updateChooseBtn()

    def handleClickConfirmBtn(self, *args):
        info = {}
        info['lvKey'] = self.lvKey
        info['bType'] = gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL
        info['betId'] = self.betId
        info['multiple'] = self.widget.mainMc.numStepper.count
        info['costAmount'] = info['multiple'] * DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1)
        info['team1NUIDs'] = [ teamInfo['cId'][0] for teamInfo in self.teamList ]
        info['team2NUIDs'] = [ teamInfo['cId'][1] for teamInfo in self.teamList ]
        betScoreList = uiConst.ARENA_PLAYOFFS_BET_DAY_SCORE_LIST
        info['scoreList1'] = [ betScoreList[ansIdx][0] for ansIdx in self.ansList ]
        info['scoreList2'] = [ betScoreList[ansIdx][1] for ansIdx in self.ansList ]
        info['isArena5v5'] = gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5
        info['isArenaScore'] = gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore
        self.updateLastConfirmHistory()
        self.uiAdapter.arenaPlayoffsBetConfirm.show(info)

    def handleCountChange(self, *args):
        costAmount = self.widget.mainMc.numStepper.count * DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1)
        self.widget.mainMc.costAmount.text = format(costAmount, ',')

    def checkBetStart(self):
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            keys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
        elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            keys = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS
        else:
            if not gameglobal.rds.configData.get('enableArenaPlayoffs', False):
                return False
            keys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
        for index, lvKey in enumerate(keys):
            betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, 0)
            betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL, betId)
            if not self.betTimeDatas:
                self.initBetTime()
            apbtTimeData = self.betTimeDatas.get(betKey, {})
            if apbtTimeData and utils.inCrontabRange(apbtTimeData['tBetStart'][index], apbtTimeData['tBetEnd'][index]):
                return True

        return False

    def updateHistory(self):
        self.history[self.lvKey, self.betId] = copy.deepcopy(self.ansList)

    def updateLastConfirmHistory(self):
        self.lastConfirmHistory[self.lvKey, self.betId] = copy.deepcopy(self.ansList)
