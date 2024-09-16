#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFGuildTournamentLiveProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import uiConst
import formula
import events
import utils
import const
from uiProxy import UIProxy
from asObject import ASObject
from gameStrings import gameStrings
from guis import uiUtils
from guis.asObject import TipManager
from callbackHelper import Functor
from data import battle_field_data as BFD
from data import guild_config_data as GCD
from data import battle_field_flag_data as BFFD
from data import state_data as SD
from data import battle_field_fort_data as BFFTD
from cdata import game_msg_def_data as GMDD
BH1_GROUPID = 0
BH2_GROUPID = 1
QL1_GROUPID = 0
QL2_GROUPID = 1
QL1_STATE = 0
QL2_STATE = 1
BH1_STATE = 2
BH2_STATE = 3
STATES = (QL1_STATE,
 QL2_STATE,
 BH1_STATE,
 BH2_STATE)
MAX_EFFECT_LV = 3
MAX_PLANE_NUM = 5

class BFGuildTournamentLiveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFGuildTournamentLiveProxy, self).__init__(uiAdapter)
        self.currentRefreshType = QL1_STATE
        self.currentRefreshWidget = None
        self.inspirePraiseData = {}
        self.hpInfo = None
        self.planeInfo = None
        self.monsterInfo = None
        self.monsterNUID = {}
        self.isQL1PanelNeedShow = False
        self.isQL2PanelNeedShow = False
        self.isBH1PanelNeedShow = False
        self.isBH2PanelNeedShow = False
        self.widget = {QL1_STATE: None,
         QL2_STATE: None,
         BH1_STATE: None,
         BH2_STATE: None}
        self.isNeedShow = {QL1_STATE: False,
         QL2_STATE: None,
         BH1_STATE: False,
         BH2_STATE: False}
        self.timeTick = {QL1_STATE: 0,
         QL2_STATE: 0,
         BH1_STATE: 0,
         BH2_STATE: 0}
        self.countTime = {QL1_STATE: 0,
         QL2_STATE: 0,
         BH1_STATE: 0,
         BH2_STATE: 0}
        self.subGroupIdx = {QL1_STATE: 0,
         QL2_STATE: 0,
         BH1_STATE: 0,
         BH2_STATE: 0}
        self.gbIdList = []
        self.coolDownReady = 0
        self.coolDownTimeTick = None
        self.isEncourageEnabled = True
        self.statisticFbNo = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL1, Functor(self.clearWidget, QL1_STATE))
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL2, Functor(self.clearWidget, QL2_STATE))
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH1, Functor(self.clearWidget, BH1_STATE))
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH2, Functor(self.clearWidget, BH2_STATE))

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL1:
            self.widget[QL1_STATE] = widget
            self.currentRefreshType = QL1_STATE
        elif widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL2:
            self.widget[QL2_STATE] = widget
            self.currentRefreshType = QL2_STATE
        elif widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH1:
            self.widget[BH1_STATE] = widget
            self.currentRefreshType = BH1_STATE
        else:
            self.widget[BH2_STATE] = widget
            self.currentRefreshType = BH2_STATE
        self.initUI()

    def _asWidgetClose(self, widgetId, multiID):
        super(self.__class__, self).clearWidget()
        if widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL1:
            self.widget[QL1_STATE] = None
        elif widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL2:
            self.widget[QL2_STATE] = None
        elif widgetId == uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH1:
            self.widget[BH1_STATE] = None
        else:
            self.widget[BH2_STATE] = None
        self.uiAdapter.unLoadWidget(widgetId)

    def clearAllWidget(self):
        self.clearWidget(QL1_STATE)
        self.clearWidget(QL2_STATE)
        self.clearWidget(BH1_STATE)
        self.clearWidget(BH2_STATE)

    def clearWidget(self, state = None):
        if not state:
            state = self.currentRefreshType
        if state == QL1_STATE:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL1)
            self.widget[QL1_STATE] = None
        elif state == QL2_STATE:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL2)
            self.widget[QL2_STATE] = None
        elif state == BH1_STATE:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH1)
            self.widget[BH1_STATE] = None
        else:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH2)
            self.widget[BH2_STATE] = None
        if state == self.currentRefreshType:
            self.currentRefreshWidget = None

    def clearMessage(self, state = None):
        if not state:
            state = self.currentRefreshType
        self.removeMessage(state)

    def clearAllPanel(self):
        self.currentRefreshWidget = QL1_STATE
        self.clearCurrentPanel()
        self.currentRefreshWidget = QL2_STATE
        self.clearCurrentPanel()
        self.currentRefreshWidget = BH1_STATE
        self.clearCurrentPanel()
        self.currentRefreshWidget = BH2_STATE
        self.clearCurrentPanel()

    def clearCurrentPanel(self):
        self.clearWidget()
        self.clearMessage()
        self.clearData()

    def clearPanel(self, groupId, subGroupIds):
        subGroupId = self.getSubGroupId(groupId, subGroupIds[1], subGroupIds[0])
        self.setCurrentRefreshType(groupId, subGroupId)
        self.setCurrentWidget()
        self.clearCurrentPanel()

    def clearData(self, state = None):
        if not state:
            state = self.currentRefreshType
        self.inspirePraiseData[state] = {}
        self.countTime[state] = 0
        BigWorld.cancelCallback(self.timeTick[state])
        if state in (QL1_STATE, QL2_STATE):
            self.planeInfo = None

    def initUI(self):
        self.setCurrentWidget()
        self.currentRefreshWidget.defaultCloseBtn = self.currentRefreshWidget.closeBtn
        self.refreshInspirePraiseData()
        self.currentRefreshWidget.encourageBtn.btn.data = self.currentRefreshType
        self.currentRefreshWidget.encourageBtn.btn.addEventListener(events.MOUSE_CLICK, self.handleClickEncourage)
        self.currentRefreshWidget.praiseBtn.data = self.currentRefreshType
        self.currentRefreshWidget.praiseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPraise)
        self.currentRefreshWidget.shareBtn.data = self.currentRefreshType
        self.currentRefreshWidget.shareBtn.addEventListener(events.MOUSE_CLICK, self.handleClickShare)
        self.currentRefreshWidget.witnessBtn.data = self.currentRefreshType
        self.currentRefreshWidget.witnessBtn.addEventListener(events.MOUSE_CLICK, self.handleClikWitness)
        self.currentRefreshWidget.panel.infoArea.foldBtn.data = self.currentRefreshType
        self.currentRefreshWidget.panel.infoArea.foldBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFold)
        self.currentRefreshWidget.statistic.data = self.currentRefreshType
        self.currentRefreshWidget.statistic.addEventListener(events.MOUSE_CLICK, self.handleClickStatistic)
        if self.currentRefreshType in (QL1_STATE, QL2_STATE):
            self.initQLPanel()
        else:
            self.initBHPanel()
        self.refreshCoolDown()
        self.setEvent()
        self.setEncourageBtnTip()

    def initQLPanel(self):
        self.refreshHpInfo()
        p = BigWorld.player()
        isTournamentApplyed = False
        guildTournament = p.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        if gameglobal.rds.ui.guild.isWWTournamentApplyedByGroupId(guildTournament):
            isTournamentApplyed = True
        self.hideAllPlane(isTournamentApplyed)
        if not isTournamentApplyed:
            self.initResInfo()
        self.refreshAllPlaneInfo()
        self.setCurrentTime()

    def initBHPanel(self):
        self.initResInfo()
        self.hideAllPlane()
        self.setCurrentTime()

    def initResInfo(self):
        self.currentRefreshWidget.selfStats.currentValue = 0
        self.currentRefreshWidget.selfStats.maxValue = 100
        self.currentRefreshWidget.selfNum.htmlText = 0
        self.currentRefreshWidget.enemyStats.currentValue = 0
        self.currentRefreshWidget.enemyStats.maxValue = 100
        self.currentRefreshWidget.enemyNum.htmlText = 0

    def setEncourageBtnTip(self):
        if not self.inspirePraiseData.get(self.currentRefreshType):
            return
        if not self.currentRefreshWidget:
            return
        gtInspireMorales = self.inspirePraiseData[self.currentRefreshType].get('gtInspireMorales', [0, 0])
        guildNUIDs = self.inspirePraiseData[self.currentRefreshType]['guildNUIDs']
        selfGtInspireMorale, enemyGtInspireMorale = self.getMorales(guildNUIDs, gtInspireMorales)
        self.setMoraleTip(selfGtInspireMorale, self.currentRefreshWidget.guildInfoSelf.bg)
        self.setMoraleTip(enemyGtInspireMorale, self.currentRefreshWidget.guildInfoEnemy.bg)

    def setMoraleTip(self, moralesNum, mc):
        moraleLv = self.getMoralesLv(moralesNum)
        if not moraleLv:
            desc = ''
        else:
            inspireGuildTournamentBuffs = GCD.data.get('inspireGuildTournamentBuffs', {})
            buffKeys = sorted(inspireGuildTournamentBuffs.keys())
            buffId = inspireGuildTournamentBuffs[buffKeys[moraleLv - 1]]
            desc = SD.data.get(buffId, {}).get('desc', '')
        TipManager.addTip(mc, desc)

    def refreshCoolDown(self):
        if self.widget.get(QL1_STATE, None):
            self.refreshCoolDownWithMc(self.widget[QL1_STATE].encourageBtn)
        if self.widget.get(QL2_STATE, None):
            self.refreshCoolDownWithMc(self.widget[QL2_STATE].encourageBtn)
        if self.widget.get(BH1_STATE, None):
            self.refreshCoolDownWithMc(self.widget[BH1_STATE].encourageBtn)
        if self.widget.get(BH2_STATE, None):
            self.refreshCoolDownWithMc(self.widget[BH2_STATE].encourageBtn)

    def refreshCoolDownWithMc(self, mc):
        if self.isEncourageEnabled:
            mc.effect.visible = True
            mc.progress.visible = False
            mc.btn.enabled = True
            mc.bgEffect.visible = True
        else:
            countTime = self.getCoolDownDurationTime()
            totalTime = GCD.data.get('inspireGuildTournamentCd', 0)
            mc.effect.visible = False
            mc.progress.visible = True
            totalFrames = mc.progress.coolDown.totalFrames
            mc.progress.coolDown.gotoAndStop(int((totalTime - countTime) / (totalTime * 1.0) * totalFrames))
            mc.bgEffect.visible = False
            mc.btn.enabled = False

    def setCoolDown(self, coolDownReady):
        self.coolDownReady = coolDownReady
        if self.coolDownTimeTick:
            BigWorld.cancelCallback(self.coolDownTimeTick)
        self.coolDownTimeTick = BigWorld.callback(1, self.handleCoolDown)

    def getCoolDownDurationTime(self):
        countTime = int(self.coolDownReady - utils.getNow())
        return countTime

    def handleCoolDown(self):
        countTime = self.getCoolDownDurationTime()
        if countTime <= 0:
            self.isEncourageEnabled = True
            BigWorld.cancelCallback(self.coolDownTimeTick)
        else:
            self.isEncourageEnabled = False
            self.coolDownTimeTick = BigWorld.callback(1, self.handleCoolDown)
        self.refreshCoolDown()

    def show(self, widgetType):
        if widgetType == QL1_STATE:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL1)
        elif widgetType == QL2_STATE:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_QL2)
        elif widgetType == BH1_STATE:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH1)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_GUILD_TOURNAMENT_LIVE_BH2)

    def pushLiveMessage(self, guildNUIDs, subGroupIds, groupId):
        subGroupId = self.getSubGroupId(groupId, subGroupIds, guildNUIDs)
        self.setCurrentRefreshType(groupId, subGroupId)
        self.queryForGuildTournament()
        if self.currentRefreshType == QL1_STATE:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL1)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL1, {'click': self.onClickShowQL1Panel})
        elif self.currentRefreshType == QL2_STATE:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL2)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL2, {'click': self.onClickShowQL2Panel})
        elif self.currentRefreshType == BH1_STATE:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH1)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH1, {'click': self.onClickShowBH1Panel})
        else:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH2)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH2, {'click': self.onClickShowBH2Panel})

    def getCurrentTournamentGroupId(self):
        if self.currentRefreshType in (QL1_STATE, QL2_STATE):
            return gametypes.GUILD_TOURNAMENT_GROUP_QL
        else:
            return gametypes.GUILD_TOURNAMENT_GROUP_BH

    def isInGuildWWTournamentInMatch(self, tournamentGroupId):
        p = BigWorld.player()
        state = p.guildTournament.get(tournamentGroupId).state
        trainState = p.guildTournament.get(tournamentGroupId).trainingState
        if state in gametypes.GUILD_TOURNAMENT_BTN_ENTER_STATES or trainState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_MATCH:
            return True
        else:
            return False

    def queryForGuildTournamentState(self):
        p = BigWorld.player()
        p.queryGuildTournamentSimple()

    def isInBattleField(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if formula.whatFubenType(fbNo) in const.FB_TYPE_BATTLE_FIELD:
            return True
        return False

    def onClickShowQL1Panel(self):
        if self.isInBattleField():
            return
        self.queryForGuildTournamentState()
        self.isQL1PanelNeedShow = True
        self.showQL1Panel()

    def onClickShowQL2Panel(self):
        if self.isInBattleField():
            return
        self.queryForGuildTournamentState()
        self.isQL2PanelNeedShow = True
        self.showQL2Panel()

    def showQL1Panel(self):
        if not self.isInGuildWWTournamentInMatch(gametypes.GUILD_TOURNAMENT_GROUP_QL):
            return
        self.show(QL1_STATE)
        self.isQL1PanelNeedShow = False

    def showQL2Panel(self):
        if not self.isInGuildWWTournamentInMatch(gametypes.GUILD_TOURNAMENT_GROUP_QL):
            return
        self.show(QL2_STATE)
        self.isQL2PanelNeedShow = False

    def onClickShowBH1Panel(self):
        if self.isInBattleField():
            return
        self.queryForGuildTournamentState()
        self.isBH1PanelNeedShow = True
        self.showBH1Panel()

    def showBH1Panel(self):
        if not self.isInGuildWWTournamentInMatch(gametypes.GUILD_TOURNAMENT_GROUP_BH):
            return
        self.show(BH1_STATE)
        self.isBH1PanelNeedShow = False

    def onClickShowBH2Panel(self):
        if self.isInBattleField():
            return
        self.queryForGuildTournamentState()
        self.isBH2PanelNeedShow = True
        self.showBH2Panel()

    def showBH2Panel(self):
        if not self.isInGuildWWTournamentInMatch(gametypes.GUILD_TOURNAMENT_GROUP_BH):
            return
        self.isBH2PanelNeedShow = False
        self.show(BH2_STATE)

    def removeMessage(self, state):
        if state == QL1_STATE:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL1)
        elif state == QL2_STATE:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_QL2)
        elif state == BH1_STATE:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH1)
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_LIVE_BH2)

    def showPanel(self):
        if self.isQL1PanelNeedShow:
            self.showQL1Panel()
        if self.isQL2PanelNeedShow:
            self.showQL2Panel()
        if self.isBH1PanelNeedShow:
            self.showBH1Panel()
        if self.isBH2PanelNeedShow:
            self.showBH2Panel()

    def setInspirePraiseData(self, fbNo, guildNUIDs, subGroupIds, gtInspireMorales, praisesNum, livesNum, tReady, groupId, groupNames):
        subGroupId = self.getSubGroupId(groupId, subGroupIds, guildNUIDs)
        self.setCurrentRefreshType(groupId, subGroupId)
        self.setSubGroupIdx(groupId, subGroupIds, guildNUIDs)
        if not self.inspirePraiseData.get(self.currentRefreshType, None):
            self.inspirePraiseData[self.currentRefreshType] = {}
        self.inspirePraiseData[self.currentRefreshType]['subGroupId'] = subGroupId
        self.inspirePraiseData[self.currentRefreshType]['guildNUIDs'] = guildNUIDs
        self.inspirePraiseData[self.currentRefreshType]['gtInspireMorales'] = gtInspireMorales
        self.inspirePraiseData[self.currentRefreshType]['praisesNum'] = praisesNum
        self.inspirePraiseData[self.currentRefreshType]['livesNum'] = livesNum
        self.inspirePraiseData[self.currentRefreshType]['fbNo'] = fbNo
        self.inspirePraiseData[self.currentRefreshType]['groupId'] = groupId
        self.inspirePraiseData[self.currentRefreshType]['guildNames'] = groupNames
        if self.inspirePraiseData[self.currentRefreshType].get('tReady', 0) != tReady:
            self.inspirePraiseData[self.currentRefreshType]['tReady'] = tReady
            self.refreshTime()
        self.setCurrentWidget()
        self.refreshInspirePraiseData()
        self.setEncourageBtnTip()

    def setInspirePraiseEventData(self, fbNo, subGroupIds, eventType, eventArgs, groupId):
        subGroupId = self.getSubGroupId(groupId, subGroupIds[1], subGroupIds[0])
        self.setCurrentRefreshType(groupId, subGroupId)
        if not self.inspirePraiseData.get(self.currentRefreshType, {}):
            self.inspirePraiseData[self.currentRefreshType] = {}
        if not self.inspirePraiseData[self.currentRefreshType].get('events', []):
            self.inspirePraiseData[self.currentRefreshType]['events'] = []
        eventData = {}
        eventData['eventType'] = eventType
        eventData['eventArgs'] = eventArgs
        self.inspirePraiseData[self.currentRefreshType]['events'].insert(0, eventData)
        self.setEvent()

    def setCurrentRefreshType(self, groupId, subGroupId):
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            if subGroupId == QL1_GROUPID:
                self.currentRefreshType = QL1_STATE
            else:
                self.currentRefreshType = QL2_STATE
        elif subGroupId == BH1_GROUPID:
            self.currentRefreshType = BH1_STATE
        else:
            self.currentRefreshType = BH2_STATE

    def setCurrentWidget(self, state = None):
        if state:
            self.currentRefreshType = state
        self.currentRefreshWidget = self.widget[self.currentRefreshType]

    def setSubGroupIdx(self, groupId, subGroupIds, guildNUIDs):
        p = BigWorld.player()
        if guildNUIDs[0] == guildNUIDs[1]:
            self.subGroupIdx[self.currentRefreshType] = 0
            return
        for i in xrange(0, len(guildNUIDs)):
            if p.guildNUID == guildNUIDs[i]:
                self.subGroupIdx[self.currentRefreshType] = i

    def getSubGroupId(self, groupId, subGroupIds, guildNUIDs = None):
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            if not guildNUIDs:
                if subGroupIds[self.subGroupIdx[QL1_STATE]] == QL1_GROUPID:
                    return QL1_GROUPID
                else:
                    return QL2_GROUPID
            p = BigWorld.player()
            if guildNUIDs[0] == guildNUIDs[1]:
                return QL1_GROUPID
            for i in xrange(0, len(guildNUIDs)):
                if p.guildNUID == guildNUIDs[i]:
                    return subGroupIds[i]

            return QL1_GROUPID
        else:
            if not guildNUIDs:
                if subGroupIds[self.subGroupIdx[QL1_STATE]] == BH1_GROUPID:
                    return BH1_GROUPID
                else:
                    return BH2_GROUPID
            p = BigWorld.player()
            if guildNUIDs[0] == guildNUIDs[1]:
                return BH1_GROUPID
            for i in xrange(0, len(guildNUIDs)):
                if p.guildNUID == guildNUIDs[i]:
                    return subGroupIds[i]

            return BH1_GROUPID

    def queryForGuildTournament(self):
        p = BigWorld.player()
        groupId = self.getCurrentTournamentGroupId()
        tournamentResult = p.worldWar.tournamentResult
        p.cell.queryWWTournament(groupId, tournamentResult.groupVer[groupId], tournamentResult.guildVer)

    def setCurrentTime(self):
        countTime = 0
        if self.currentRefreshType == QL1_STATE:
            countTime = self.countTime[QL1_STATE]
        elif self.currentRefreshType == QL2_STATE:
            countTime = self.countTime[QL2_STATE]
        elif self.currentRefreshType == BH1_STATE:
            countTime = self.countTime[BH1_STATE]
        else:
            countTime = self.countTime[BH2_STATE]
        self.currentRefreshWidget.flagTimer.text = countTime

    def refreshTime(self):
        tReady = self.inspirePraiseData[self.currentRefreshType]['tReady']
        BigWorld.cancelCallback(self.timeTick[self.currentRefreshType])
        self.timeTick[self.currentRefreshType] = BigWorld.callback(1, Functor(self.handleTimer, self.currentRefreshType))
        if self.currentRefreshWidget and self.currentRefreshWidget.flagTimer:
            countTime = self.getDurationTime(self.inspirePraiseData[self.currentRefreshType]['fbNo'], tReady)
            self.currentRefreshWidget.flagTimer.text = utils.formatTimeStr(countTime, 'm:s')

    def getDurationTime(self, fbNo, tReady):
        totalTime = BFD.data.get(fbNo, {}).get('durationTime', 1800)
        countTime = totalTime - int(utils.getNow() - tReady)
        return countTime

    def handleTimer(self, state):
        self.countTime[state] = self.getDurationTime(self.inspirePraiseData[state]['fbNo'], self.inspirePraiseData[state]['tReady'])
        if self.countTime[state] >= 0:
            self.timeTick[state] = BigWorld.callback(1, Functor(self.handleTimer, state))
            if not self.widget[state]:
                return
            self.widget[state].flagTimer.text = utils.formatTimeStr(self.countTime[state], 'm:s')
        else:
            BigWorld.cancelCallback(self.timeTick[state])

    def refreshAllInspirePraiseData(self):
        for state in STATES:
            self.currentRefreshType = state
            self.setCurrentWidget()
            self.refreshInspirePraiseData()

    def refreshInspirePraiseData(self):
        if not self.currentRefreshWidget:
            return
        elif not self.inspirePraiseData or not self.inspirePraiseData.get(self.currentRefreshType, None):
            return
        else:
            p = BigWorld.player()
            inspirePraiseData = self.inspirePraiseData[self.currentRefreshType]
            self.currentRefreshWidget.praiseNumArea.txt.text = inspirePraiseData.get('praisesNum', 0)
            self.currentRefreshWidget.witnessNumArea.txt.text = inspirePraiseData.get('livesNum', 0)
            selfGuildIdx = 0 if inspirePraiseData.get('guildNUIDs', [0, 0])[0] == p.guildNUID else 1
            enemyGuildIdx = 0 if selfGuildIdx == 1 else 1
            selfGuildName = self.getTournamentGuildName(selfGuildIdx)
            enemyGuildName = self.getTournamentGuildName(enemyGuildIdx)
            self.currentRefreshWidget.guildInfoSelf.guildName.text = selfGuildName
            self.currentRefreshWidget.guildInfoEnemy.guildName.text = enemyGuildName
            self.refreshMoraleIcon()
            return

    def getGuildNameByNuid(self, guildNUID):
        inspirePraiseData = self.inspirePraiseData.get(self.currentRefreshType, {})
        guildIdx = 0 if inspirePraiseData.get('guildNUIDs', [0, 0])[0] == guildNUID else 1
        return self.getTournamentGuildName(guildIdx)

    def getTournamentGuildName(self, guildIdx):
        inspirePraiseData = self.inspirePraiseData[self.currentRefreshType]
        return inspirePraiseData.get('guildNames', ['', ''])[guildIdx]

    def getMoralesLv(self, gtInspireMorales):
        inspireGuildTournamentBuffs = GCD.data.get('inspireGuildTournamentBuffs', {}).keys()
        inspireGuildTournamentBuffs = sorted(inspireGuildTournamentBuffs)
        for i in xrange(0, len(inspireGuildTournamentBuffs)):
            if gtInspireMorales < inspireGuildTournamentBuffs[i]:
                return i

        return len(inspireGuildTournamentBuffs)

    def refreshMoraleIcon(self):
        gtInspireMorales = self.inspirePraiseData[self.currentRefreshType].get('gtInspireMorales', [0, 0])
        guildNUIDs = self.inspirePraiseData[self.currentRefreshType]['guildNUIDs']
        selfGtInspireMorale, enemyGtInspireMorale = self.getMorales(guildNUIDs, gtInspireMorales)
        selfLv = self.getMoralesLv(selfGtInspireMorale)
        enemyLv = self.getMoralesLv(enemyGtInspireMorale)
        self.setMoraleLv(self.currentRefreshWidget.guildInfoSelf, selfLv)
        self.setMoraleLv(self.currentRefreshWidget.guildInfoEnemy, enemyLv)

    def getMorales(self, guildNUIDs, gtInspireMorales):
        p = BigWorld.player()
        selfGtInspireMorale = -1
        enemyGtInspireMorale = -1
        for i in xrange(0, len(guildNUIDs)):
            if p.guildNUID == guildNUIDs[i]:
                selfGtInspireMorale = gtInspireMorales[i]
            else:
                enemyGtInspireMorale = gtInspireMorales[i]

        if enemyGtInspireMorale < 0:
            enemyGtInspireMorale = selfGtInspireMorale
        return (selfGtInspireMorale, enemyGtInspireMorale)

    def setMoraleLv(self, mc, lv):
        if not lv:
            mc.lvNum.visible = False
        else:
            mc.lvNum.visible = True
            mc.lvNum.gotoAndStop('lv%d' % lv)
        for i in xrange(0, MAX_EFFECT_LV):
            mc.getChildByName('lv%d' % (i + 1)).visible = True
            if lv > MAX_EFFECT_LV:
                if i != MAX_EFFECT_LV - 1:
                    mc.getChildByName('lv%d' % (i + 1)).visible = False
            elif i + 1 != lv:
                mc.getChildByName('lv%d' % (i + 1)).visible = False

    def getHpInfoFromMonsterInfo(self, monsterInfo, monsterNUID):
        if not monsterInfo:
            return
        elif not self.inspirePraiseData.get(self.currentRefreshType, None):
            return
        elif not self.inspirePraiseData.get(self.currentRefreshType, None).get('fbNo', 0):
            return
        else:
            ret = {}
            p = BigWorld.player()
            myHpInfo = {}
            enemyHpInfo = {}
            for entityId, hpInfo in monsterInfo.iteritems():
                if monsterNUID.get(entityId, 0) == p.guildNUID:
                    myHpInfo['hp'] = monsterInfo.get(entityId, {}).get('hp', 0)
                    myHpInfo['mhp'] = monsterInfo.get(entityId, {}).get('mhp', 1)
                    fbEntityNo = monsterInfo.get(entityId, {}).get('fbEntityNo', 0)
                    myHpInfo['icon'] = 'battleFieldMonsterName/' + str(fbEntityNo) + '.dds'
                    ret['myHpInfo'] = myHpInfo
                else:
                    enemyHpInfo['hp'] = monsterInfo.get(entityId, {}).get('hp', 0)
                    enemyHpInfo['mhp'] = monsterInfo.get(entityId, {}).get('mhp', 1)
                    fbEntityNo = monsterInfo.get(entityId, {}).get('fbEntityNo', 0)
                    enemyHpInfo['icon'] = 'battleFieldMonsterName/' + str(fbEntityNo) + '.dds'
                    ret['enemyHpInfo'] = enemyHpInfo

            return ret

    def setEvent(self, state = None):
        if not state:
            state = self.currentRefreshType
        self.setCurrentWidget(state)
        if not self.currentRefreshWidget:
            return
        events = self.inspirePraiseData[state].get('events', [])
        if not self.currentRefreshWidget.panel.infoArea.detailArea:
            return
        self.currentRefreshWidget.panel.infoArea.detailArea.dataArray = events
        self.currentRefreshWidget.panel.infoArea.detailArea.lableFunction = self.eventsDetailFunction
        self.currentRefreshWidget.panel.infoArea.detailArea.itemHeight = 20
        self.currentRefreshWidget.panel.infoArea.detailArea.itemRenderer = 'BFGuildTournamentLive_Detail_Item'
        self.currentRefreshWidget.panel.infoArea.detailArea.itemHeightFunction = self.eventItemHeightFunction

    def getEventText(self, itemData):
        args = itemData.eventArgs
        eventType = int(itemData.eventType)
        guildNUID = args[0]
        guildName = self.getGuildNameByNuid(long(guildNUID))
        if eventType == gametypes.GUILD_TOURNAMENT_EVENT_AVATAR_COMBAT_KILL:
            roleName = args[1]
            killNum = args[2]
            resultText = GCD.data.get('guildTournamentAvatarKillEvent', '%s_%s_%d') % (guildName, roleName, long(killNum))
        elif eventType == gametypes.GUILD_TOURNAMENT_EVENT_OCCUPY_FORT:
            fortId = args[1]
            fortName = BFFTD.data.get(fortId, {}).get('fortName', '')
            resultText = GCD.data.get('guildTournamentOccupyFortEvent', '%s_%s') % (guildName, fortName)
        elif eventType == gametypes.GUILD_TOURNAMENT_EVENT_PLAYER_LANDING_PLANE:
            roleName = args[1]
            resultText = GCD.data.get('guildTournamentLandingPlaneEvent', '%s_%s') % (guildName, roleName)
        elif eventType == gametypes.GUILD_TOURNAMENT_EVENT_PLANE_DESTROY:
            resultText = GCD.data.get('guildTournamentPlaneDestoryEvent', '%s') % guildName
        elif eventType == gametypes.GUILD_TOURNAMENT_EVENT_FIRE_HURT:
            hurtNum = args[1]
            resultText = GCD.data.get('guildTournamentFireHurtEvent', '%s_%d') % (guildName, long(hurtNum))
        else:
            roleName = args[1]
            flagId = args[2]
            flagName = BFFD.data.get(flagId, {}).get('flagName', '')
            resultText = GCD.data.get('guildTournamentOccupyFlagEvent', '%s_%s_%s') % (guildName, roleName, flagName)
        return resultText

    def eventItemHeightFunction(self, *args):
        if not self.currentRefreshWidget:
            return GfxValue(0)
        info = ASObject(args[3][0])
        item = self.currentRefreshWidget.getInstByClsName('BFGuildTournamentLive_Detail_Item')
        item.txt.htmlText = self.getEventText(info)
        item.txt.wordWrap = True
        item.txt.height = item.txt.textHeight + 10
        return GfxValue(item.txt.height)

    def eventsDetailFunction(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.txt.wordWrap = True
        item.txt.htmlText = self.getEventText(itemData)
        item.txt.height = item.txt.textHeight + 10

    def setHpInfo(self, monsterInfo, monsterNUID, subGroupIds):
        subGroupId = self.getSubGroupId(gametypes.GUILD_TOURNAMENT_GROUP_QL, subGroupIds)
        self.setCurrentRefreshType(gametypes.GUILD_TOURNAMENT_GROUP_QL, subGroupId)
        self.setCurrentWidget()
        self.monsterInfo = monsterInfo
        self.monsterNUID = monsterNUID
        if not self.inspirePraiseData.get(self.currentRefreshType, {}):
            return
        self.hpInfo = self.getHpInfoFromMonsterInfo(monsterInfo, monsterNUID)
        if not self.currentRefreshWidget:
            return
        self.refreshHpInfo()

    def getMyScore(self, fbNo = 0):
        p = BigWorld.player()
        if not fbNo:
            fbNo = p.getBattleFieldFbNo()
        bfData = BFD.data.get(fbNo, {})
        planeTotalCnt = bfData.get('planeTotalCnt', 5)
        planeConsumeScore = bfData.get('planeConsumeScore', 100)
        maxScore = planeTotalCnt * planeConsumeScore
        myScore = 0
        if hasattr(p, 'bfScore'):
            for k, v in p.bfScore.iteritems():
                if p.guildNUID == k >> 1:
                    myScore = v

            if myScore >= maxScore:
                return maxScore
            return myScore
        else:
            return 0

    def getEnemyScore(self, fbNo = 0):
        p = BigWorld.player()
        if not fbNo:
            fbNo = p.getBattleFieldFbNo()
        bfData = BFD.data.get(fbNo, {})
        planeTotalCnt = bfData.get('planeTotalCnt', 5)
        planeConsumeScore = bfData.get('planeConsumeScore', 100)
        maxScore = planeTotalCnt * planeConsumeScore
        enemyScore = 0
        if hasattr(p, 'bfScore'):
            for k, v in p.bfScore.iteritems():
                if p.guildNUID != k >> 1:
                    enemyScore = v

            if enemyScore >= maxScore:
                return maxScore
            return enemyScore
        else:
            return 0

    def refreshAllPlane(self):
        fbNo = self.inspirePraiseData.get(QL1_STATE, {}).get('fbNo', 0)
        planeResUnit = BFD.data.get(fbNo, {}).get('planeConsumeScore', 100)
        myScore = self.getMyScore(fbNo)
        enemyScore = self.getEnemyScore(fbNo)
        planeInfo = ((int(myScore / planeResUnit), myScore % planeResUnit * 1.0 / planeResUnit), (int(enemyScore / planeResUnit), enemyScore % planeResUnit * 1.0 / planeResUnit))
        self.setAllPlaneInfo(planeInfo)

    def hideAllPlane(self, isShow = False):
        self.hidePlane('planeSelf', isShow)
        self.hidePlane('planeEnemy', isShow)

    def hidePlane(self, planeName, isShow = False):
        for i in xrange(0, MAX_PLANE_NUM):
            plane = self.currentRefreshWidget.getChildByName(planeName + str(i))
            plane.visible = isShow

    def setAllPlaneInfo(self, planeInfo):
        self.planeInfo = planeInfo
        if not self.widget[QL1_STATE]:
            return
        self.setCurrentWidget(QL1_STATE)
        self.refreshAllPlaneInfo()

    def refreshAllPlaneInfo(self):
        if not self.planeInfo:
            return
        self.setPlaneInfo('planeSelf', self.planeInfo[0])
        self.setPlaneInfo('planeEnemy', self.planeInfo[1])

    def setPlaneInfo(self, planeName, info):
        if not self.currentRefreshWidget:
            return
        for i in xrange(0, MAX_PLANE_NUM):
            plane = self.currentRefreshWidget.getChildByName(planeName + str(i))
            plane.maxValue = 1
            if i < info[0]:
                plane.currentValue = 1
            elif i == info[0]:
                plane.currentValue = info[1]
            else:
                plane.currentValue = 0

    def refreshHpInfo(self):
        self.hpInfo = self.getHpInfoFromMonsterInfo(self.monsterInfo, self.monsterNUID)
        if not self.hpInfo:
            return
        myInfo = self.hpInfo.get('myHpInfo', {})
        enemyInfo = self.hpInfo.get('enemyHpInfo', {})
        if myInfo:
            self.currentRefreshWidget.selfNum.htmlText = myInfo['hp']
            self.currentRefreshWidget.selfStats.currentValue = myInfo['hp']
            self.currentRefreshWidget.selfStats.maxValue = myInfo['mhp']
        if enemyInfo:
            self.currentRefreshWidget.enemyNum.htmlText = enemyInfo['hp']
            self.currentRefreshWidget.enemyStats.currentValue = enemyInfo['hp']
            self.currentRefreshWidget.enemyStats.maxValue = enemyInfo['mhp']

    def getStatsInfo(self, subGroupId):
        p = BigWorld.player()
        statsInfo = {}
        for k, v in p.bfRes.iteritems():
            guildNUID = k >> 1
            if guildNUID == p.guildNUID and k & 1 == subGroupId:
                statsInfo['myMaxRes'] = BFD.data.get(const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FLAG_1, {}).get('winResLimit', 100)
                statsInfo['myCurRes'] = v
            else:
                statsInfo['enemyMaxRes'] = BFD.data.get(const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FLAG_1, {}).get('winResLimit', 100)
                statsInfo['enemyCurRes'] = v

        return statsInfo

    def refreshBFStats(self, groupId, subGroupIds):
        subGroupId = self.getSubGroupId(groupId, subGroupIds[1], subGroupIds[0])
        self.setCurrentRefreshType(groupId, subGroupId)
        self.setCurrentWidget()
        if not self.currentRefreshWidget:
            return
        statsInfo = self.getStatsInfo(subGroupId)
        self.currentRefreshWidget.selfNum.htmlText = statsInfo['myCurRes']
        self.currentRefreshWidget.selfStats.currentValue = statsInfo['myCurRes']
        self.currentRefreshWidget.selfStats.maxValue = statsInfo['myMaxRes']
        self.currentRefreshWidget.enemyNum.htmlText = statsInfo['enemyCurRes']
        self.currentRefreshWidget.enemyStats.currentValue = statsInfo['enemyCurRes']
        self.currentRefreshWidget.enemyStats.maxValue = statsInfo['enemyMaxRes']

    def handleClickEncourage(self, *args):
        p = BigWorld.player()
        p.cell.requireInspireGuildTournamentMembers()

    def handleClickPraise(self, *args):
        p = BigWorld.player()
        targetBtn = ASObject(args[3][0]).currentTarget
        p.cell.requireAddPraiseForGTournament(self.getGroupIdFromState(targetBtn.data))

    def getGroupIdFromState(self, state):
        if state == QL1_STATE:
            return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL
        elif state == QL2_STATE:
            return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL_2
        elif state == BH1_STATE:
            return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH
        else:
            return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2

    def disablePraiseBtn(self, groupId, subGroupId):
        self.setCurrentRefreshType(groupId, subGroupId)
        self.setCurrentWidget()
        if not self.currentRefreshWidget:
            return
        self.currentRefreshWidget.praiseBtn.enabled = False

    def handleClickShare(self, *args):
        p = BigWorld.player()
        targetBtn = ASObject(args[3][0]).currentTarget
        data = self.inspirePraiseData.get(targetBtn.data, {})
        if not data:
            return
        groupId = self.getGroupIdFromState(targetBtn.data)
        guildNUIDs = data.get('guildNUIDs', [])
        pushTxt = uiUtils.getTextFromGMD(GMDD.data.GUILD_TOURNAMENT_WAR_HOT_PUSH_NOTIFY) % (self.getGuildNameByNuid(guildNUIDs[0]),
         self.getGuildNameByNuid(guildNUIDs[1]),
         p.guildNUID,
         groupId)
        gameglobal.rds.ui.sendLink(pushTxt)

    def handleClikWitness(self, *args):
        p = BigWorld.player()
        targetBtn = ASObject(args[3][0]).currentTarget
        groupId = self.getGroupIdFromState(targetBtn.data)
        p.cell.enterGuildTournamentWithLive(groupId, p.guildNUID)
        self.clearAllWidget()

    def handleClickFold(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        self.foldPanel(targetBtn.data)

    def foldPanel(self, state):
        self.widget[state].panel.gotoAndStop('fold')
        self.widget[state].panel.infoArea.extendBtn.data = state
        self.widget[state].panel.infoArea.extendBtn.addEventListener(events.MOUSE_CLICK, self.handleClickExtend)

    def handleClickExtend(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        self.extendPanel(targetBtn.data)
        self.setEvent(targetBtn.data)

    def extendPanel(self, state):
        self.widget[state].panel.gotoAndStop('extend')
        self.widget[state].panel.infoArea.foldBtn.data = state
        self.widget[state].panel.infoArea.foldBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFold)

    def handleClickStatistic(self, *args):
        p = BigWorld.player()
        targetBtn = ASObject(args[3][0]).currentTarget
        if targetBtn.data in (QL1_STATE, QL2_STATE):
            state = p.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_QL).state
            if state in gametypes.GUILD_TOURNAMENT_BTN_ENTER_STATES:
                self.statisticFbNo = const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FORT_1
            else:
                self.statisticFbNo = const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FLAG_1
        else:
            self.statisticFbNo = const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FLAG_1
        if targetBtn.data == QL1_STATE:
            p.queryAllGtBattleFieldDetails(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL)
        elif targetBtn.data == QL2_STATE:
            p.queryAllGtBattleFieldDetails(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL_2)
        elif targetBtn.data == BH1_STATE:
            p.queryAllGtBattleFieldDetails(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH)
        else:
            p.queryAllGtBattleFieldDetails(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2)
        gameglobal.rds.ui.battleField.openBFTmpResultWidget(self.statisticFbNo)
