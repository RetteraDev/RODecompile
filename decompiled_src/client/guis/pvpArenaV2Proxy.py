#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpArenaV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import math
import gameglobal
import utils
import time
import gametypes
import uiUtils
import uiConst
import formula
import events
import const
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis import ui
from gamestrings import gameStrings
from data import arena_mode_data as AMD
from data import sys_config_data as SCD
from data import arena_score_desc_data as ASDD
from data import bonus_data as BD
from data import item_data as ID
from data import duel_config_data as DCD
from data import arena_season_data as ASD
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
from cdata import arena_level_data as ALD
PLAY_METHODS = 1
BTN5_X = 696
MATCH_BTN_TAB = 1
RANK_BTN_TAB = 0
ARENA_PANEL_STAGE_INIT = 1
ARENA_PANEL_STAGE_WAITING_TEAM = 2
ARENA_PANEL_STAGE_MATCHING = 3
ARENA_PANEL_STAGE_IN_GAME = 4
ARENA_PANEL_STAGE_MATCHED = 5
ARENA_MODE_ITEM_CLS = 'PvpArenaV2_wanfatiaomu'
PLAY_METHOD_SHOW = [1, 0, 0]
defaultLimit = (0, 20, 30, 40, 50)
defaultLimit2 = (0, 20000, 30000, 40000, 50000)
radius = [12,
 25,
 40,
 57,
 75]

class PvpArenaV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpArenaV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.severRank = ''
        self.raderData = {}
        self.lastSelectItem = None
        self.lastTimeStamp = 0
        self.arenaSortedModeData = []

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        if hasattr(self, 'myArenaId'):
            delattr(self, 'myArenaId')
        self.initPlayMethod()
        self.widget.data = self.onGetArenaData()
        self.initAreaInfo(self.widget.data)
        self.widget.btn1.addEventListener(events.MOUSE_CLICK, self.handleSeeRewardClick, False, 0, True)
        self.widget.btn2.addEventListener(events.MOUSE_CLICK, self.handleGetArenaRewardClick, False, 0, True)
        self.widget.btn5.addEventListener(events.MOUSE_CLICK, self.handleSeeRankClick, False, 0, True)
        self.addEvent(events.EVENT_CHANGE_GROUP_STATE, self.onGroupStateChanged)
        self.addEvent(events.EVENT_CHANGE_ARENA_STATE, self.refreshArenaStage)
        self.queryMode()

    def initPlayMethod(self):
        self.widget.playMethod.itemRenderer = ARENA_MODE_ITEM_CLS
        self.widget.playMethod.itemHeight = 74
        self.widget.playMethod.lableFunction = self.arenaModeLableFunc
        self.arenaSortedModeData = self.genArenaSortedModeData()

    def setMatchData(self):
        arenaInfos = self.arenaData['arenaBattleInfoList']
        dataArr = []
        for i, arenaInfo in enumerate(arenaInfos):
            arenaType = arenaInfo.get('arenaType', 0)
            if arenaType == 2:
                dataArr.append({'index': i,
                 'arenaInfo': arenaInfo})

        self.widget.playMethod.dataArray = dataArr
        self.widget.playMethod.validateNow()

    def setRankData(self):
        arenaInfos = self.arenaData['arenaBattleInfoList']
        dataArr = []
        for i, arenaInfo in enumerate(arenaInfos):
            arenaType = arenaInfo.get('arenaType', 0)
            if arenaType == 1:
                dataArr.append({'index': i,
                 'arenaInfo': arenaInfo})

        self.widget.playMethod.dataArray = dataArr
        self.widget.playMethod.validateNow()

    def arenaModeLableFunc(self, *args):
        data = ASObject(args[3][0])
        arenaInfo = data.arenaInfo
        index = data.index
        item = ASObject(args[3][1])
        item.tag = index
        item.arenaInfo = arenaInfo
        labels = []
        labels.append(arenaInfo.get('title', gameStrings.TEXT_PVPARENAV2PROXY_118))
        labels.append(arenaInfo.get('name', ''))
        item.labels = labels
        iconName = arenaInfo.get('iconName', '')
        if iconName:
            item.iconName = iconName
        else:
            item.iconName = '../pvpPanel/2001'
        item.addEventListener(events.BUTTON_CLICK, self.onPlayMethodItemClick)

    def onPlayMethodItemClick(self, *args):
        e = ASObject(args[3][0])
        index = e.target.tag
        self.selectMothodItem(e.target)
        arenaInfo = e.target.arenaInfo
        mode = arenaInfo.mode
        self.myArenaId = index
        self.trySelectArenaItem(index, mode)

    def selectMothodItem(self, item):
        if self.lastSelectItem:
            self.lastSelectItem.selected = False
        self.lastSelectItem = item
        item.selected = True

    def queryMode(self):
        p = BigWorld.player()
        p.base.queryArenaHistoryInfo()

    def transformData(self, arenaInfo):
        self.raderData = arenaInfo
        self.setRaderInfo()

    def setRaderInfo(self):
        if not self.widget:
            return
        for i in xrange(5):
            raderDesc = self.widget.getChildByName('desc%d' % i)
            raderDesc.text = gameStrings.RADER_DESCS[i]

        dataInfo = self.arenaData['arenaBattleInfoList'][self.myArenaId]
        raderData = self.raderData.get(dataInfo['mode'], {})
        mc = self.widget.socialRadar.inner
        limit = []
        limit.append(list(DCD.data.get('arenaAveKillCntLimit', defaultLimit)))
        limit.append(list(DCD.data.get('arenaAveAssistCntLmit', defaultLimit)))
        limit.append(list(DCD.data.get('arenaAveDamageLimit', defaultLimit2)))
        limit.append(list(DCD.data.get('arenaAveBedamageLimit', defaultLimit2)))
        limit.append(list(DCD.data.get('arenaAveCureValLmit', defaultLimit2)))
        data = [raderData.get('killCnt', 0),
         raderData.get('assistCnt', 0),
         raderData.get('damageVal', 0),
         raderData.get('beDamageVal', 0),
         raderData.get('cureVal', 0)]
        if raderData.get('finishCnt'):
            for i, element in enumerate(data):
                data[i] = math.ceil(float(data[i]) / raderData.get('finishCnt'))

        for i in xrange(len(data)):
            radertext = self.widget.getChildByName('radar%d' % i)
            radertext.text = data[i]

        centerPointX = mc.width / 2 + 0.5
        centerPointY = mc.height / 2 + 4
        mc.graphics.clear()
        mc.graphics.moveTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
        angle = 360 / len(data)
        mc.graphics.beginFill(26316, 0.6)
        for i, element in enumerate(data):
            if not i:
                continue
            pointX, pointY = self.getVertex(centerPointX, centerPointY, 90 - angle * i, self.getRadius(limit[i], data[i], radius))
            mc.graphics.lineTo(pointX, pointY)

        mc.graphics.lineTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
        mc.graphics.endFill()

    def getRadius(self, limit, data, radius):
        for i in xrange(1, len(limit)):
            if limit[i - 1] <= data < limit[i]:
                return radius[i - 1]

        return radius[len(radius) - 1]

    def getVertex(self, centerPointX, centerPointY, angle, radius):
        dx = radius * math.cos(math.pi * angle / 180)
        dy = radius * math.sin(math.pi * angle / 180)
        return (centerPointX + dx, centerPointY - dy)

    def setArenaInfo(self, data):
        self.arenaData = data
        self.widget.rankLv.text = data['arenaScore']
        self.widget.arenaScore.gotoAndPlay(data['curFrame'])
        self.widget.arenaScoreLbl.gotoAndPlay(data['curFrame'])
        self.widget.joinTimesDesc.htmlText = data['countWeek']
        self.widget.btn1.visible = data['showDuanWeiAward']
        TipManager.addTipByFunc(self.widget.arenaScore, self.makeSmallTips1, data, False)
        TipManager.addTipByFunc(self.widget.rankLv, self.makeSmallTips2, data, False)
        self.widget.btn5.x = self.widget.btn1.x if not self.widget.btn1.visible else BTN5_X
        if self.isBalanceArenaSelect():
            self.widget.severRankTitle.visible = False
            self.widget.severRank.visible = False
        else:
            self.widget.severRankTitle.visible = True
            self.widget.severRank.visible = True
            self.widget.severRank.text = self.severRank
        self.widget.combatScore.text = data['combatScore']
        self.widget.belongGroup.text = data['belongGroup']
        self.widget.notComplete.text = data['notComplete']
        self.widget.sessionText.text = data['sessionText']
        self.widget.sessionTime.text = data['sessionTime']

    def initAreaInfo(self, data):
        self.setArenaInfo(data)
        self.widget.matchBtn.addEventListener(events.MOUSE_CLICK, self.onMatchBtnClick, False, 0, True)
        self.widget.rankBtn.addEventListener(events.MOUSE_CLICK, self.onRankBtnClick, False, 0, True)
        self.onRankBtnClick()
        self.widget.btn3.addEventListener(events.MOUSE_CLICK, self.handleArenaApplyOfPersonBtnClick, False, 0, True)
        self.widget.extBtn.addEventListener(events.MOUSE_CLICK, self.handleArenaFuncClick, False, 0, True)
        self.widget.doubleBtn.addEventListener(events.MOUSE_CLICK, self.handleArenaFuncClick, False, 0, True)

    def makeSmallTips1(self, *args):
        self.makeSmallTips(self.widget.arenaScore, *args)

    def makeSmallTips2(self, *args):
        self.makeSmallTips(self.widget.rankLv, *args)

    def makeSmallTips(self, _mc, *args):
        data = ASObject(args[3][0])
        curData = data.scoreData.cur
        mc = self.getMcForTip(curData, False)
        if data.hasNext:
            self.tipsMc = self.widget.getInstByClsName('flash.display.MovieClip')
            nextData = data.scoreData.next
            nMc = self.getMcForTip(nextData, True)
            self.tipsMc.addChild(mc)
            self.tipsMc.addChild(nMc)
            nMc.y = mc.y + mc.height
            TipManager.showImediateTip(_mc, self.tipsMc)
            return None
        else:
            TipManager.showImediateTip(_mc, mc)
            return None

    def getMcForTip(self, data, isNext):
        if not isNext:
            mc = self.widget.getInstByClsName('PvPPanelNew_Arena_Fame_Tips')
        else:
            mc = self.widget.getInstByClsName('PvPPanelNew_Arena_Fame_Tips_02')
        mc.rankRange.text = data.rankRange
        if not isNext:
            mc.curName.text = data.name + gameStrings.TEXT_PVPARENAV2PROXY_263
        else:
            mc.curName.text = data.name + gameStrings.TEXT_PVPARENAV2PROXY_265
        mc.rankFrame.gotoAndPlay(data.curFrame)
        mc.curDesc1.text = data.desc1
        mc.curDesc2.text = data.desc2
        mc.curDesc3.text = data.desc3
        text1 = ''
        text2 = ''
        for i in xrange(len(data.bonus)):
            if i < 2:
                if text1 == '':
                    text1 = data.bonus[i]
                else:
                    text1 = text1 + '  ' + data.bonus[i]
            elif text2 == '':
                text2 = data.bonus[i]
            else:
                text2 = text2 + '  ' + data.bonus[i]

        mc.award0.htmlText = text1
        mc.award1.htmlText = text2
        return mc

    def handleSeeRankClick(self, *args):
        arenaMode = 0
        if not hasattr(self, 'myArenaId') or not self.arenaData:
            arenaMode = 0
        else:
            arenaMode = self.arenaData['arenaBattleInfoList'][self.myArenaId]['mode']
        if self.isBalanceArenaMode(arenaMode):
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_ARENA_SCORES_BALANCE)
        else:
            gameglobal.rds.ui.arenaRankList.show(arenaMode)

    def handleGetArenaRewardClick(self, *args):
        self.getArenaReward()

    def isBalanceArenaSelect(self):
        if not hasattr(self, 'myArenaId') or not self.arenaData:
            return False
        data = self.arenaData['arenaBattleInfoList'][self.myArenaId]
        return formula.isBalanceArenaMode(data['mode'])

    def isBalanceArenaMode(self, mode):
        return formula.isBalanceArenaMode(mode)

    @ui.callFilter(1)
    def getArenaReward(self):
        p = BigWorld.player()
        if self.isBalanceArenaSelect():
            p.cell.exchangeArenaFame(const.ARENA_MODE_TYPE_BALANCE)
        else:
            p.cell.exchangeArenaFame(const.ARENA_MODE_TYPE_NORMAL)

    def handleSeeRewardClick(self, *args):
        if not hasattr(self, 'myArenaId') or not self.arenaData:
            gameglobal.rds.ui.arenaRankAward.show()
            return
        data = self.arenaData['arenaBattleInfoList'][self.myArenaId]
        gameglobal.rds.ui.arenaRankAward.show(data['mode'])

    def handleArenaFuncClick(self, *args):
        e = ASObject(args[3][0])
        data = self.arenaData['arenaBattleInfoList'][self.myArenaId]
        if formula.isBalanceArenaMode(data['mode']):
            if e.target == self.widget.doubleBtn:
                p = BigWorld.player()
                if formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
                    p.arenaMode = data['mode']
                    p.applyArena()
                else:
                    arenaMode = data['mode']
                    minLv, maxLv = formula.getArenaLvByMode(arenaMode)
                    if p.lv < minLv or p.lv > maxLv:
                        p.showGameMsg(GMDD.data.ARENA_APPLY_FAILED_LV, (minLv, maxLv))
                        return
                    p.cell.applyEnterBalanceReadyRoom(arenaMode)
                return
        self.clickArenaFuncBtn(self.myArenaStage, data['mode'])

    def handleArenaApplyOfPersonBtnClick(self, *args):
        data = self.arenaData['arenaBattleInfoList'][self.myArenaId]
        if formula.isBalanceArenaMode(data['mode']):
            gameglobal.rds.ui.balanceArenaTemplate.show()
            return
        self.applyOfPersonClick(data['mode'])

    def applyOfPersonClick(self, arenaMode):
        p = BigWorld.player()
        if p.isInTeam():
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_IN_TEAM, ())
            return
        p.arenaMode = arenaMode
        p.applyArena()

    def clickArenaFuncBtn(self, stage, arenaMode):
        p = BigWorld.player()
        if stage == uiConst.ARENA_PANEL_START:
            if not p.isInTeam():
                p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_IN_TEAM, ())
                return
            p.arenaMode = arenaMode
            p.applyArena()
        elif stage == uiConst.ARENA_PANEL_WAITING_TEAM:
            pass
        elif stage == uiConst.ARENA_PANEL_MATCHING:
            p.cancelApplyArena()
        elif stage == uiConst.ARENA_PANEL_IN_GAME:
            p.abortArena()

    def onMatchBtnClick(self, *args):
        self.widget.matchBtn.selected = True
        self.widget.rankBtn.selected = False
        self.setMatchData()
        item = self.widget.playMethod.canvas.getChildAt(0)
        if item:
            index = item.tag
            self.selectMothodItem(item)
            arenaInfo = item.arenaInfo
            mode = arenaInfo.mode
            self.myArenaId = index
            self.trySelectArenaItem(index, mode)

    def onRankBtnClick(self, *args):
        self.widget.rankBtn.selected = True
        self.widget.matchBtn.selected = False
        self.setRankData()
        item = self.widget.playMethod.canvas.getChildAt(0)
        if item:
            index = item.tag
            self.selectMothodItem(item)
            arenaInfo = item.arenaInfo
            mode = arenaInfo.mode
            self.myArenaId = index
            self.trySelectArenaItem(index, mode)

    def onGroupStateChanged(self):
        if self.widget and hasattr(self, 'myArenaId') and self.isBalanceArenaSelect():
            self.refreshArenaPanel(self.myArenaId)

    def refreshArenaPanel(self, idx):
        self.myArenaId = idx
        self.widget.data = self.onGetArenaData()
        self.setArenaInfo(self.widget.data)
        data = self.arenaData['arenaBattleInfoList'][idx]
        self.widget.winTimes.text = self.getWinMatch(data['mode'])
        self.widget.allTimes.text = self.getAllMatchNum(data['mode'])
        self.widget.descPanel.canvas.text.htmlText = gameStrings.TEXT_PVPARENAV2PROXY_415 + data['timeDesc'] + gameStrings.TEXT_PVPARENAV2PROXY_415_1 + data['playDesc']
        self.widget.btn3.enabled = data['playerBtn']
        self.widget.doubleBtn.enabled = data['teamBtn'] if data['teamBtnName'] != 'Группа' else False
        self.widget.doubleBtn.label = data['teamBtnName']
        self.widget.btn3.label = gameStrings.TEXT_BALANCEARENAHOVERPROXY_145
        self.setRaderInfo()
        self.widget.belongGroupTitle.visible = True
        self.widget.belongGroup.visible = True
        if formula.isBalanceArenaMode(data['mode']):
            self.widget.btn3.label = gameStrings.TEXT_PVPARENAV2PROXY_425
            self.widget.belongGroupTitle.visible = False
            self.widget.belongGroup.visible = False
            p = BigWorld.player()
            if formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)) and data['mode'] == getattr(p, 'arenaModeCache', 0):
                if not p.isInTeam():
                    self.widget.doubleBtn.label = gameStrings.TEXT_PVPARENAV2PROXY_431
                else:
                    self.widget.doubleBtn.label = gameStrings.TEXT_BALANCEARENAHOVERPROXY_143
        if gameglobal.rds.configData.get('enableArenaWeeklyAwardBalance', False) and formula.isBalanceArenaMode(data['mode']) or gameglobal.rds.configData.get('enableArenaWeeklyAward', False) and not formula.isBalanceArenaMode(data['mode']):
            self.widget.joinTimesDesc.visible = True
            self.widget.btn2.visible = True
            self.widget.fameBg.visible = True
        else:
            self.widget.joinTimesDesc.visible = False
            self.widget.btn2.visible = False
            self.widget.fameBg.visible = False
        self.refreshArenaStage()

    def refreshArenaStage(self):
        p = BigWorld.player()
        stage = getattr(p, 'arenaStage', 1)
        if self.widget:
            self.setArenaStage(stage, self.getCount())

    def setArenaStage(self, stage, timeCount):
        self.myArenaStage = stage
        if self.myArenaStage == ARENA_PANEL_STAGE_INIT:
            self.widget.btn3.visible = True
            self.widget.doubleBtn.visible = True
            self.widget.extBtn.visible = False
            self.widget.descPanel.visible = True
        elif self.myArenaStage == ARENA_PANEL_STAGE_WAITING_TEAM:
            self.widget.extBtn.label = gameStrings.TEXT_ARENAPROXY_235
            self.widget.btn3.visible = False
            self.widget.extBtn.visible = True
            self.widget.doubleBtn.visible = False
            self.widget.descPanel.visible = False
        elif self.myArenaStage == ARENA_PANEL_STAGE_MATCHING:
            self.widget.extBtn.label = gameStrings.TEXT_ARENAPROXY_235
            self.widget.btn3.visible = False
            self.widget.extBtn.visible = True
            self.widget.doubleBtn.visible = False
            self.widget.descPanel.visible = False
        elif self.myArenaStage == ARENA_PANEL_STAGE_IN_GAME:
            self.widget.btn3.visible = False
            self.widget.extBtn.label = gameStrings.TEXT_ARENAPROXY_239
            self.widget.extBtn.visible = True
            self.widget.doubleBtn.visible = False
            self.widget.descPanel.visible = False
        elif self.myArenaStage == ARENA_PANEL_STAGE_MATCHED:
            self.widget.btn3.visible = False
            self.widget.extBtn.visible = False
            self.widget.doubleBtn.visible = False
            self.widget.descPanel.visible = False

    def getCount(self):
        p = BigWorld.player()
        stage = getattr(p, 'arenaStage', 1)
        if stage == uiConst.ARENA_PANEL_MATCHING:
            interval = p.getServerTime() - self.lastTimeStamp
            return int(interval)
        return 0

    def trySelectArenaItem(self, selIdx, mode):
        p = BigWorld.player()
        stage = getattr(p, 'arenaStage', 1)
        arenaMode = getattr(p, 'arenaMode', 0)
        if self.widget:
            self.refreshArenaPanel(selIdx)

    def onGetArenaData(self):
        curFrame, nextFame, hasNext, scoreData = self._genScoreDesc()
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        enableDuanWeiAward = gameglobal.rds.configData.get('enableDuanWeiAward', False)
        if self.isBalanceArenaSelect():
            arenaInfo = p.arenaInfoEx
            enableDuanWeiAward = gameglobal.rds.configData.get('enableDuanWeiAwardBalance', False)
        arenaScore = arenaInfo.arenaScore
        data = {}
        data['scoreData'] = scoreData
        data['curFrame'] = curFrame
        data['nextFame'] = nextFame
        data['hasNext'] = hasNext
        data['arenaScore'] = arenaScore
        data['showDuanWeiAward'] = enableDuanWeiAward
        minLv = ALD.data.get(arenaInfo.curLevel, {}).get('minLv', 1)
        maxLv = ALD.data.get(arenaInfo.curLevel, {}).get('maxLv', 1)
        data['belongGroup'] = '%d-%d' % (minLv, maxLv)
        data['notComplete'] = gameStrings.TEXT_PVPARENAV2PROXY_528 % DCD.data.get('arenaWeekPlaySubScore', 10)
        data['combatScore'] = utils.calcArenaCombatPower(arenaInfo)
        timeText = time.localtime().tm_year
        data['sessionText'] = gameStrings.TEXT_PVPARENAV2PROXY_531 % timeText + ASD.data.get(arenaInfo.curSeason, {}).get('SessionName', gameStrings.TEXT_ARENARANKAWARDPROXY_73_1)
        data['sessionTime'] = ASD.data.get(arenaInfo.curSeason, {}).get('SessionTimeText', '')
        data['countWeek'] = self.onGetCountWeek()
        data['arenaBattleInfoList'] = self.arenaSortedModeData
        lvKey = self.getPlayerTopRankKey()
        p = BigWorld.player()
        data['severRank'] = ''
        data['allSeverRank'] = ''
        p.base.getTopArenaScoreTimer(gameglobal.rds.ui.arenaRankList.arenaInfo.get(lvKey, [0, [], 0])[0], lvKey)
        if gameglobal.rds.configData.get('enableCrossServerArena', False):
            p.base.getGlboalTopArenaScore(gameglobal.rds.ui.arenaRankList.crossArenaInfo.get(lvKey, [0, [], 0])[0], lvKey)
        return data

    def getPlayerTopRankKey(self):
        p = BigWorld.player()
        return self.getPlayerLvKey() % str(p.school)

    def needToDisable(self, key):
        if key in const.CROSS_DOUBLE_ARENA or key in const.CROSS_BALANCE_ARENA_SCORE:
            return True
        return False

    def genArenaSortedModeData(self):
        ret = []
        p = BigWorld.player()
        inArenaNo = getattr(p, 'arenaMode', 0)
        sel = False
        for key, item in AMD.data.items():
            enable = item.get('isEnableUIApply', 0)
            if gameglobal.rds.configData.get('enableCrossServerArena', False):
                if formula.isCrossServerArena(key):
                    enable = enable and utils.crossServerArenaEnabled(key, p.lv)
                else:
                    enable = enable and not utils.crossServerArenaEnabled(key, p.lv)
            elif formula.isCrossServerArena(key):
                enable = False
            if formula.isBalanceArenaMode(key):
                enable = gameglobal.rds.configData.get('enableBalanceArena', False) and enable
                if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)) or formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
                    enable = True and item.get('isEnableUIApply', 0)
            if self.needToDisable(key):
                enable = False
            if enable:
                itemData = {}
                itemData['name'] = item.get('name', gameStrings.TEXT_ARENAPROXY_1034)
                itemData['mode'] = key
                itemData['playerBtn'] = item.get('playerBtn', 0)
                itemData['teamBtnName'] = item.get('teamBtnName', gameStrings.TEXT_BALANCEARENAHOVERPROXY_143)
                itemData['teamBtn'] = item.get('teamBtn', 0)
                itemData['ord'] = item.get('ord', 999)
                itemData['title'] = item.get('title', '')
                itemData['arenaType'] = item.get('arenaType', 0)
                itemData['iconName'] = item.get('iconName', '')
                itemData['timeDesc'] = item.get('timeDesc', '11:00~24:00')
                itemData['playDesc'] = self.getDescByLv(item.get('lvDescDict', {}), p.lv, item.get('desc', ''))
                if key == inArenaNo:
                    itemData['sel'] = True
                    sel = True
                else:
                    itemData['sel'] = False
                ret.append(itemData)

        ret = sorted(ret, key=lambda d: d['ord'], reverse=False)
        if sel == False and ret:
            ret[0]['sel'] = True
        return ret

    def setSeverRank(self, arenaInfo):
        if self.widget:
            txt = self.getRank(arenaInfo)
            self.severRank = txt
            self.widget.severRank.text = txt

    def getRank(self, rank):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaSelect():
            arenaInfo = p.arenaInfoEx
        weeklyNum = p._getArenaWeekPlayerCnt(const.ARENA_MODE_TYPE_BALANCE if self.isBalanceArenaSelect() and const.ARENA_MODE_TYPE_BALANCE else const.ARENA_MODE_TYPE_NORMAL)
        if rank == -1:
            if weeklyNum == 0:
                return uiUtils.getTextFromGMD(GMDD.data.ARENA_RANK_NO_PLAY, gameStrings.TEXT_PVPARENAV2PROXY_613)
            else:
                return gameStrings.TEXT_PVPARENAV2PROXY_615
        else:
            return '%d' % (rank + 1)

    def getPlayerLvKey(self):
        lvKey = uiUtils.getPlayerTopRankKey()
        return lvKey + '_%s'

    def getDescByLv(self, descDict, lv, default = ''):
        for lvTuple, desc in descDict.iteritems():
            if lvTuple[0] <= lv <= lvTuple[1]:
                return desc

        return default

    def getAllMatchNum(self, mode):
        return self.getWinMatch(mode) + self.getLoseMatch(mode) + self.getDuelMatch(mode)

    def getLoseMatch(self, mode):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaMode(mode):
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(mode, None)
        if details:
            return details.loseMatch
        else:
            return 0

    def getDuelMatch(self, mode):
        p = BigWorld.player()
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaMode(mode):
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(mode, None)
        if details:
            return details.duelMatch
        else:
            return 0

    def getWinMatch(self, mode):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaSelect():
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(mode, None)
        if details:
            return details.winMatch
        else:
            return 0

    def onGetCountWeek(self):
        p = BigWorld.player()
        total = DCD.data.get('arenaWeekPlayCntLimit', 10)
        arenaInfo = p.arenaInfo
        curNum = p._getArenaWeekPlayerCnt(const.ARENA_MODE_TYPE_BALANCE if self.isBalanceArenaSelect() else const.ARENA_MODE_TYPE_NORMAL)
        return gameStrings.TEXT_PVPARENAV2PROXY_671 % (curNum, total)

    def _genScoreDesc(self):
        p = BigWorld.player()
        curFrame = 'orange1'
        tmpASDD = ASDD.data.keys()
        tmpASDD.sort()
        data = {}
        data['cur'] = {}
        data['next'] = {}
        index = 0
        curIndex = 0
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaSelect():
            arenaInfo = p.arenaInfoEx
        for minS, maxS in tmpASDD:
            if arenaInfo.arenaScore >= minS and arenaInfo.arenaScore <= maxS:
                curFrame = ASDD.data[minS, maxS].get('frameName', 'orange1')
                data['cur'] = self.getScoreDesc((minS, maxS))
                curIndex = index
                break
            index += 1

        hasNext = True
        if index == len(ASDD.data.keys()):
            key = tmpASDD[index - 1]
            if index - 1 == curIndex:
                hasNext = False
        elif index == len(ASDD.data.keys()) - 1:
            key = tmpASDD[index]
            if index == curIndex:
                hasNext = False
        else:
            key = tmpASDD[index + 1]
        if hasNext == True:
            data['next'] = self.getScoreDesc(key)
        nextFame = ASDD.data[key].get('frameName', 'orange1')
        return (curFrame,
         nextFame,
         hasNext,
         data)

    def getScoreDesc(self, key):
        data = {}
        ad = ASDD.data[key]
        curFrame = ad.get('frameName', 'orange1')
        data['curFrame'] = curFrame
        data['name'] = ad.get('desc', gameStrings.TEXT_ARENAPROXY_321)
        data['rankRange'] = gameStrings.TEXT_ARENARANKAWARDPROXY_192 % (key[0], key[1])
        data['desc1'] = gameStrings.TEXT_PVPARENAV2PROXY_718 % (ad.get('duanWeiAwardZhanXun', 0), ad.get('duanWeiAwardZhanXun', 0))
        data['desc2'] = gameStrings.TEXT_PVPARENAV2PROXY_719 % (ad.get('lianXiAwardZhanXun', 0), ad.get('lianXiAwardJunZi', 0))
        data['desc3'] = gameStrings.TEXT_PVPARENAV2PROXY_720 % data['name']
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if self.isBalanceArenaSelect():
            arenaInfo = p.arenaInfoEx
        weeklyAwardName = ALD.data.get(p.arenaInfoEx.curLevel, {}).get('weeklyAwardName', '')
        awardId = ad.get(weeklyAwardName)
        fixedBonus = BD.data.get(awardId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        bonusItemName = []
        for i in xrange(0, len(fixedBonus)):
            bonusType, bonusItemId, bonusNum = fixedBonus[i]
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                name = uiUtils.getItemColorName(bonusItemId)
                name = ID.data.get(bonusItemId, {}).get('name', '')
                quality = ID.data.get(bonusItemId, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('color', '0xFFFFE7')
                trueName = gameStrings.TEXT_PVPARENAV2PROXY_739 % (color, name, bonusNum)
                bonusItemName.append(trueName)
            else:
                nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
                 gametypes.BONUS_TYPE_FAME: gameStrings.TEXT_CHALLENGEPROXY_199_1,
                 gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
                 gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
                 gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663}
                name = nameMap[bonusType]
                name = name + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(bonusNum)
                bonusItemName.append(name)

        data['bonus'] = bonusItemName
        return data
