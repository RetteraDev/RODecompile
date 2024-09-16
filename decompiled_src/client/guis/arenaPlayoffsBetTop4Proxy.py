#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetTop4Proxy.o
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
import uiUtils
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
MAX_RIGHT_ITEM_NUM = 4
INVALID_HOT_TEAM_RANK = 99999

def sort_team(a, b):
    if a['hotTeamRank'] < b['hotTeamRank']:
        return -1
    if a['hotTeamRank'] > b['hotTeamRank']:
        return 1
    if a['hostId'] < b['hostId']:
        return -1
    if a['hostId'] > b['hostId']:
        return 1
    if int(a['tId']) < int(b['tId']):
        return -1
    if int(a['tId']) > int(b['tId']):
        return 1
    return 0


class ArenaPlayoffsBetTop4Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetTop4Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.lvKey = ''
        self.betId = 0
        self.selectedTeamItemIdx = -1
        self.selectedRightItemIdx = -1
        self.teamList = []
        self.rightIdList = [-1] * MAX_RIGHT_ITEM_NUM
        self.history = {}
        self.fisrtShow = {}
        self.lastConfirmHistory = {}
        self.betTimeData = {}

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
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
        elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS
        else:
            if not gameglobal.rds.configData.get('enableArenaPlayoffs', False):
                return False
            lvKeys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
        key = (gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, 1)
        crontab = []
        tBetEnd = []
        tBetTimeDesc = []
        tBetStart = []
        for lvKeyIndex, lvKey in enumerate(lvKeys):
            calcCrontab = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'crontab', lvKey)
            calcBetEnd = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'tBetEnd', lvKey)
            calcBetStart = duelUtils.genArenaPlayoffsBetCrontabStr(currentSeason, lvKeyIndex, key[0], key[1], 'tBetStart', lvKey)
            try:
                crontab.append(calcCrontab)
                tBetEnd.append(calcBetEnd)
                tBetStart.append(calcBetStart)
                startDesc = time.strftime('%m/%d %H:%M', time.localtime(utils.getDisposableCronTabTimeStamp(calcBetStart)))
                endDesc = time.strftime('%m/%d %H:%M', time.localtime(utils.getDisposableCronTabTimeStamp(calcBetEnd)))
                descText = '%s-%s' % (startDesc, endDesc)
                tBetTimeDesc.append(descText)
            except Exception as e:
                logInfo = '%s|%s|%s|%s|%s|' % (calcCrontab,
                 calcBetEnd,
                 calcBetStart,
                 str(gameglobal.rds.configData.get('enableArenaPlayoffsBet', False)),
                 str(lvKeys))
                msg = 'Exception in arenaPlayoffsBet initBetTime, info:%s, error:%s' % (logInfo, e.message)
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})
                return

        self.betTimeData['crontab'] = crontab
        self.betTimeData['tBetTimeDesc'] = tBetTimeDesc
        self.betTimeData['tBetStart'] = tBetStart
        self.betTimeData['tBetEnd'] = tBetEnd

    def initUI(self):
        self.widget.mainMc.helpIcon.helpKey = 301
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
                if lvKey == gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE:
                    continue
                betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, 0)
                betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, betId)
                apbtData = APBTD.data.get(betKey, {})
                if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                    apbtData = AP5BTD.data.get(betKey, {})
                    if self.betTimeData.has_key('tBetEnd') and utils.getDisposableCronTabTimeStamp(self.betTimeData['tBetEnd'][index]) > now:
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
        self.widget.mainMc.scrollWndList.itemRenderer = 'ArenaPlayoffsBetTop4_ScrollWndItem'
        self.widget.mainMc.scrollWndList.lableFunction = self.itemFunction
        self.widget.mainMc.scrollWndList.itemHeight = 34
        for i in xrange(MAX_RIGHT_ITEM_NUM):
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % i, None)
            if not itemMc:
                continue
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickRightItem, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverRightItem, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutRightItem, False, 0, True)
            itemMc.delBtn.addEventListener(events.MOUSE_CLICK, self.handleClickDelBtn, False, 0, True)

        self.widget.mainMc.rightDescIcon1.bonusType = 'wudao'
        self.widget.mainMc.rightDescIcon2.bonusType = 'wudao'
        self.widget.mainMc.costAmountIcon.bonusType = 'wudao'
        self.widget.mainMc.totalAmountIcon.bonusType = 'wudao'
        self.widget.mainMc.numStepper.enableMouseWheel = False
        self.widget.mainMc.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        self.widget.mainMc.chooseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickChooseBtn, False, 0, True)
        self.widget.mainMc.removeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRemoveBtn, False, 0, True)
        self.widget.mainMc.resetBtn.addEventListener(events.MOUSE_CLICK, self.handleClickResetBtn, False, 0, True)
        self.widget.mainMc.randomBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRandomBtn, False, 0, True)
        self.widget.mainMc.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET_START)

    def hanldleLvKeyChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.lvKey = itemMc.dataProvider[itemMc.selectedIndex].lvKey
        self.queryInfo()
        self.refreshInfo()

    def queryInfo(self):
        p = BigWorld.player()
        version = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('version', 0)
        p.cell.queryArenaPlayoffsBetIdDict(version, self.lvKey)
        version = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(self.lvKey, {}).get('version', 0)
        p.cell.queryArenaPlayoffsTeamsOfLvKey(version, self.lvKey)
        self.betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, 0)
        betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, self.betId)
        version = self.uiAdapter.arenaPlayoffsBet.betResultDict.get(self.lvKey, {}).get(betKey, {}).get('betDuelInfo', {}).get('version', 0)
        p.cell.queryArenaPlayoffsDuelBetResult(version, self.lvKey, gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, self.betId)
        version = self.uiAdapter.arenaPlayoffsBet.betFailedCashDict.get('version', 0)
        p.cell.queryArenaPlayoffsBetCalcInfo(version)
        self.uiAdapter.arenaPlayoffs.fetchFinalResult(self.lvKey)

    def refreshBetInfo(self, lvKey = ''):
        if not self.widget:
            return
        if lvKey != '' and lvKey != self.lvKey:
            return
        self.betId = self.uiAdapter.arenaPlayoffsBet.betIdDict.get(self.lvKey, {}).get('data', {}).get(gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, 0)
        betKey = (gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, self.betId)
        apbtData = APBTD.data.get(betKey, {})
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            apbtData = AP5BTD.data.get(betKey, {})
        self.widget.mainMc.rightTitle1.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_216
        rightDesc1 = apbtData.get('cashOfsys', 0) + self.uiAdapter.arenaPlayoffsBet.betResultDict.get(self.lvKey, {}).get(betKey, {}).get('lastSeasonRestCash', 0) + self.uiAdapter.arenaPlayoffsBet.betFailedCashDict.get('lastDuelRestCashDict', {}).get((self.lvKey, gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL, self.betId), {}).get('data', 0)
        self.widget.mainMc.rightDesc1.htmlText = format(rightDesc1, ',')
        ASUtils.autoSizeWithFont(self.widget.mainMc.rightDesc1, 20, 144, 8)
        self.widget.mainMc.rightDesc1.y = 65 + (20 - int(self.widget.mainMc.rightDesc1.getTextFormat().size))
        self.widget.mainMc.rightDescFlag1.x = self.widget.mainMc.rightDesc1.x + self.widget.mainMc.rightDesc1.textWidth + 5
        self.widget.mainMc.rightTitle2.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_226
        rightDesc2 = DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1) * DCD.data.get('ARENA_PLAYOFFS_BET_REWARD_CASH_MAX_RATIO', 1)
        ASUtils.textFieldAutoSize(self.widget.mainMc.rightDesc2, format(rightDesc2, ','))
        TipManager.addTip(self.widget.mainMc.rightDesc2, DCD.data.get('ARENA_PLAYOFFS_BET_TOP4_SIMPLE_TIP', ''))

    def refreshTotalAmountInfo(self):
        self.widget.mainMc.totalAmount.text = format(BigWorld.player().getFame(const.ARENA_PLAYOFFS_BET_FAME_ID), ',')

    @ui.callInCD(0.5)
    def refreshInfoInCD(self, lvKey = ''):
        self.refreshInfo(lvKey)

    def refreshInfo(self, lvKey = ''):
        if not self.widget:
            return
        elif lvKey != '' and lvKey != self.lvKey:
            return
        else:
            self.refreshBetInfo(lvKey)
            if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                index = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS.index(self.lvKey)
            elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
                index = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS.index(self.lvKey)
            else:
                index = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS.index(self.lvKey)
            self.widget.mainMc.rightTitle3.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_275
            if self.betTimeData.has_key('tBetTimeDesc'):
                self.widget.mainMc.rightDesc3.text = self.betTimeData['tBetTimeDesc'][index]
            else:
                self.widget.mainMc.rightDesc3.text = ''
            self.widget.mainMc.rightTitle4.text = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_281
            if self.betTimeData.has_key('crontab'):
                crontab = utils.getDisposableCronTabTimeStamp(self.betTimeData['crontab'][index])
                self.widget.mainMc.rightDesc4.text = time.strftime('%m/%d %H:%M', time.localtime(crontab))
            else:
                self.widget.mainMc.rightDesc4.text = ''
            self.widget.mainMc.rightDesc5.htmlText = gameStrings.TEXT_ARENAPLAYOFFSBETDAYNEWPROXY_288 % (DCD.data.get('ARENA_PLAYOFFS_BET_CNT_LIMIT', 0), DCD.data.get('ARENA_PLAYOFFS_BET_MULTIPLE_LIMIT', 0))
            self.widget.mainMc.numStepper.count = 1
            self.widget.mainMc.numStepper.maxCount = DCD.data.get('ARENA_PLAYOFFS_BET_MULTIPLE_LIMIT', 0)
            self.widget.mainMc.numStepper.enableMouseWheel = False
            self.widget.mainMc.costAmount.text = format(DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1), ',')
            self.selectedTeamItemIdx = -1
            self.selectedRightItemIdx = -1
            teamsInfo = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(self.lvKey, {}).get('info', {})
            finalDuelResult = self.uiAdapter.arenaPlayoffsBet.finalDuelResultDict.get(self.lvKey, [])
            hotTeamList = []
            for tId, tValue in teamsInfo.iteritems():
                if finalDuelResult and tId not in finalDuelResult:
                    continue
                hotTeamList.append((tId, tValue.get('teamArenaScore', 0)))

            hotTeamList.sort(key=lambda x: x[1], reverse=True)
            hotTeamNum = DCD.data.get('ARENA_PLAYOFFS_BET_HOT_TEAM_NUM', 6)
            if len(hotTeamList) > hotTeamNum:
                hotTeamList = hotTeamList[0:hotTeamNum]
            hotTeamDict = {}
            for i, value in enumerate(hotTeamList):
                hotTeamDict[value[0]] = i

            self.teamList = []
            for tId, tValue in teamsInfo.iteritems():
                if finalDuelResult and tId not in finalDuelResult:
                    continue
                teamInfo = {}
                teamInfo['tId'] = str(tId)
                teamInfo['teamName'] = tValue.get('teamName', '')
                teamInfo['hotTeamRank'] = hotTeamDict.get(tId, INVALID_HOT_TEAM_RANK)
                teamInfo['hostId'] = tValue.get('hostId', 0)
                teamInfo['serverName'] = '[%s]' % utils.getServerName(teamInfo['hostId'])
                self.teamList.append(teamInfo)

            self.teamList.sort(cmp=sort_team)
            for i in xrange(len(self.teamList)):
                self.teamList[i]['idx'] = i

            self.widget.mainMc.scrollWndList.dataArray = self.teamList
            if self.fisrtShow.get((self.lvKey, self.betId), True) or not self.history.has_key((self.lvKey, self.betId)):
                self.rightIdList = copy.deepcopy(self.lastConfirmHistory.get((self.lvKey, self.betId), [-1] * MAX_RIGHT_ITEM_NUM))
            else:
                self.rightIdList = copy.deepcopy(self.history.get((self.lvKey, self.betId), [-1] * MAX_RIGHT_ITEM_NUM))
            self.fisrtShow[self.lvKey, self.betId] = False
            for i in xrange(MAX_RIGHT_ITEM_NUM):
                itemMc = getattr(self.widget.mainMc, 'rightItem%d' % i, None)
                if not itemMc:
                    continue
                itemInfo = {}
                itemInfo['idx'] = i
                itemInfo['tId'] = str(self.rightIdList[i])
                itemInfo['teamName'] = teamsInfo.get(self.rightIdList[i], {}).get('teamName', '')
                ASUtils.setMcData(itemMc, 'data', itemInfo)

            self.refreshTotalAmountInfo()
            self.selectNextItem()
            self.updateTeamList()
            self.updateRightList()
            self.updateChooseBtn()
            return

    def updateChooseBtn(self):
        if self.selectedTeamItemIdx != -1 and self.selectedRightItemIdx != -1:
            if self.rightIdList[self.selectedRightItemIdx] == -1:
                self.widget.mainMc.chooseBtn.enabled = True
                self.widget.mainMc.removeBtn.enabled = False
            else:
                self.widget.mainMc.chooseBtn.enabled = False
                self.widget.mainMc.removeBtn.enabled = True
        else:
            self.widget.mainMc.chooseBtn.enabled = False
            self.widget.mainMc.removeBtn.enabled = False
        if self.selectedTeamItemIdx >= len(self.teamList):
            self.widget.mainMc.chooseBtn.enabled = False
        if len(self.teamList):
            self.widget.mainMc.resetBtn.enabled = True
            self.widget.mainMc.randomBtn.enabled = True
        else:
            self.widget.mainMc.resetBtn.enabled = False
            self.widget.mainMc.randomBtn.enabled = False
        for i in xrange(MAX_RIGHT_ITEM_NUM):
            if self.rightIdList[i] == -1:
                self.widget.mainMc.confirmBtn.enabled = False
                break
        else:
            self.widget.mainMc.confirmBtn.enabled = True

    def updateTeamItem(self, itemMc):
        if not itemMc:
            return
        if int(itemMc.data.tId) in self.rightIdList:
            color = '#B2B2B2'
            itemMc.overMc.visible = False
            itemMc.selectedMc.visible = False
        elif int(itemMc.data.idx) == self.selectedTeamItemIdx:
            color = '#FFFFE5'
            itemMc.overMc.visible = False
            itemMc.selectedMc.visible = True
        else:
            color = '#FFFFE5'
            itemMc.overMc.visible = False
            itemMc.selectedMc.visible = False
        itemMc.teamName.htmlText = uiUtils.toHtml(itemMc.data.teamName, color=color)
        itemMc.teamName.width = itemMc.teamName.textWidth + 5
        tipText = ''
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            tipText = gameStrings.ARENA_PLAYOFFS_5V5_BET_HOT_TEAM_TIPS
        else:
            tipText = DCD.data.get('ARENA_PLAYOFFS_BET_HOT_TEAM_TIPS', '')
        if int(itemMc.data.hotTeamRank) != INVALID_HOT_TEAM_RANK:
            itemMc.hotFlag.visible = True
            itemMc.hotFlag.x = itemMc.teamName.x + itemMc.teamName.textWidth
            TipManager.addTip(itemMc.hotFlag, tipText)
        else:
            itemMc.hotFlag.visible = False
        itemMc.serverName.htmlText = uiUtils.toHtml(itemMc.data.serverName, color=color)

    def updateTeamList(self):
        wndListItems = self.widget.mainMc.scrollWndList.items
        wndListLen = len(wndListItems)
        for i in xrange(wndListLen):
            self.updateTeamItem(wndListItems[i])

    def updateRightItem(self, itemMc):
        if not itemMc:
            return
        if int(itemMc.data.tId) != -1:
            itemMc.fullMc.visible = True
            itemMc.delBtn.visible = True
        else:
            itemMc.fullMc.visible = False
            itemMc.delBtn.visible = False
        if int(itemMc.data.idx) == self.selectedRightItemIdx:
            itemMc.overMc.visible = True
        else:
            itemMc.overMc.visible = False
        itemMc.teamName.text = itemMc.data.teamName

    def updateRightList(self):
        for i in xrange(MAX_RIGHT_ITEM_NUM):
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % i, None)
            self.updateRightItem(itemMc)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        ASUtils.setMcData(itemMc, 'data', itemData)
        self.updateTeamItem(itemMc)
        itemMc.x = 11
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickTeamItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverTeamItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutTeamItem, False, 0, True)
        menuParam = {'tId': int(itemData.tId),
         'hostId': int(itemData.hostId),
         'lvKey': self.lvKey}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_ARENA_PLAYOFFS_BET, menuParam)

    def handleClickTeamItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.tId) in self.rightIdList:
            return
        if int(itemMc.data.idx) == self.selectedTeamItemIdx:
            return
        self.selectedTeamItemIdx = int(itemMc.data.idx)
        self.updateTeamList()

    def handleOverTeamItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.tId) in self.rightIdList:
            return
        if int(itemMc.data.idx) == self.selectedTeamItemIdx:
            return
        itemMc.overMc.visible = True

    def handleOutTeamItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.tId) in self.rightIdList:
            return
        if int(itemMc.data.idx) == self.selectedTeamItemIdx:
            return
        itemMc.overMc.visible = False

    def selectNextItem(self):
        firstItemIdx = -1
        nextItemIdx = -1
        for teamInfo in self.teamList:
            if firstItemIdx == -1 and int(teamInfo['tId']) not in self.rightIdList:
                firstItemIdx = teamInfo['idx']
            if nextItemIdx == -1 and teamInfo['idx'] == self.selectedTeamItemIdx:
                nextItemIdx = -2
            elif nextItemIdx == -2 and int(teamInfo['tId']) not in self.rightIdList:
                nextItemIdx = teamInfo['idx']

        if nextItemIdx >= 0:
            self.selectedTeamItemIdx = nextItemIdx
        else:
            self.selectedTeamItemIdx = firstItemIdx
        firstItemIdx = -1
        nextItemIdx = -1
        for i in xrange(MAX_RIGHT_ITEM_NUM):
            if firstItemIdx == -1 and self.rightIdList[i] == -1:
                firstItemIdx = i
            if nextItemIdx == -1 and i == self.selectedRightItemIdx:
                nextItemIdx = -2
            elif nextItemIdx == -2 and self.rightIdList[i] == -1:
                nextItemIdx = i

        if nextItemIdx >= 0:
            self.selectedRightItemIdx = nextItemIdx
        else:
            self.selectedRightItemIdx = firstItemIdx

    def handleClickChooseBtn(self, *args):
        if self.selectedTeamItemIdx == -1 or self.selectedRightItemIdx == -1:
            return
        else:
            teamInfo = self.teamList[self.selectedTeamItemIdx]
            self.rightIdList[self.selectedRightItemIdx] = int(teamInfo['tId'])
            self.updateHistory()
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % self.selectedRightItemIdx, None)
            data = itemMc.data
            data.tId = teamInfo['tId']
            data.teamName = teamInfo['teamName']
            itemMc.data = data
            self.selectNextItem()
            self.updateTeamList()
            self.updateRightList()
            self.updateChooseBtn()
            return

    def handleClickRemoveBtn(self, *args):
        if self.selectedRightItemIdx == -1:
            return
        else:
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % self.selectedRightItemIdx, None)
            data = itemMc.data
            data.tId = -1
            data.teamName = ''
            itemMc.data = data
            self.rightIdList[self.selectedRightItemIdx] = -1
            self.updateHistory()
            self.updateTeamList()
            self.updateRightList()
            self.updateChooseBtn()
            return

    def handleClickResetBtn(self, *args):
        self.selectedTeamItemIdx = 0
        self.selectedRightItemIdx = 0
        for i in xrange(MAX_RIGHT_ITEM_NUM):
            self.rightIdList[i] = -1
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % i, None)
            data = itemMc.data
            data.tId = -1
            data.teamName = ''
            itemMc.data = data

        self.updateTeamList()
        self.updateRightList()
        self.updateChooseBtn()

    def handleClickRandomBtn(self, *args):
        self.selectedTeamItemIdx = -1
        self.selectedRightItemIdx = -1
        randomList = random.sample(self.teamList, min(len(self.teamList), MAX_RIGHT_ITEM_NUM))
        for i in xrange(len(randomList)):
            teamInfo = randomList[i]
            self.rightIdList[i] = int(teamInfo['tId'])
            itemMc = getattr(self.widget.mainMc, 'rightItem%d' % i, None)
            data = itemMc.data
            data.tId = teamInfo['tId']
            data.teamName = teamInfo['teamName']
            itemMc.data = data

        self.updateHistory()
        self.selectNextItem()
        self.updateTeamList()
        self.updateRightList()
        self.updateChooseBtn()

    def handleClickConfirmBtn(self, *args):
        info = {}
        info['lvKey'] = self.lvKey
        info['bType'] = gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL
        info['betId'] = self.betId
        info['multiple'] = self.widget.mainMc.numStepper.count
        info['costAmount'] = info['multiple'] * DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1)
        info['teamNUIDs'] = self.rightIdList
        info['isArena5v5'] = gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5
        info['isArenaScore'] = gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore
        self.updateLastConfirmHistory()
        self.uiAdapter.arenaPlayoffsBetConfirm.show(info)

    def handleClickRightItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.idx) == self.selectedRightItemIdx:
            return
        self.selectedRightItemIdx = int(itemMc.data.idx)
        self.updateRightList()
        self.updateChooseBtn()

    def handleOverRightItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.idx) == self.selectedRightItemIdx:
            return
        itemMc.overMc.visible = True

    def handleOutRightItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if int(itemMc.data.idx) == self.selectedRightItemIdx:
            return
        itemMc.overMc.visible = False

    def handleClickDelBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        data = itemMc.data
        data.tId = -1
        data.teamName = ''
        itemMc.data = data
        self.selectedRightItemIdx = int(itemMc.data.idx)
        self.rightIdList[self.selectedRightItemIdx] = -1
        self.updateHistory()
        self.updateTeamList()
        self.updateRightList()
        self.updateChooseBtn()

    def handleCountChange(self, *args):
        costAmount = self.widget.mainMc.numStepper.count * DCD.data.get('ARENA_PLAYOFFS_MIN_CASH_LIMIT', 1)
        self.widget.mainMc.costAmount.text = format(costAmount, ',')

    def checkBetStart(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
            keys = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEYS
        elif gameglobal.rds.ui.arenaPlayoffsBet.isArenaScore:
            keys = gametypes.CROSS_ARENA_PLAYOFFS_SCORE_LV_KEYS
        else:
            if not gameglobal.rds.configData.get('enableArenaPlayoffs', False):
                return False
            keys = gametypes.CROSS_ARENA_PLAYOFFS_COMMON_LV_KEYS
        for index, lvKey in enumerate(keys):
            if not self.betTimeData:
                self.initBetTime()
            if utils.inCrontabRange(self.betTimeData['tBetStart'][index], self.betTimeData['tBetEnd'][index]):
                return True

        return False

    def updateHistory(self):
        self.history[self.lvKey, self.betId] = copy.deepcopy(self.rightIdList)

    def updateLastConfirmHistory(self):
        self.lastConfirmHistory[self.lvKey, self.betId] = copy.deepcopy(self.rightIdList)
