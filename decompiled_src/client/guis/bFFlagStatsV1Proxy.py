#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFFlagStatsV1Proxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
import const
import formula
from uiProxy import UIProxy
from data import battle_field_data as BFD
MAX_EFFECT_LV = 3

class BFFlagStatsV1Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFFlagStatsV1Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.timeTick = None
        self.inspirePraiseData = {}
        self.sideName = {}

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_FLAG_STATS_V1)
        self.widget = None
        if self.timeTick:
            BigWorld.cancelCallback(self.timeTick)
            self.timeTick = 0

    def initUI(self):
        self.refreshStatsInfo()
        self.initBFTime()
        self.setObserve()
        self.startTimer()
        self.refreshSideName()
        self.refreshInspirePraiseData()
        self.widget.statsBtn.addEventListener(events.MOUSE_CLICK, self.handleClickStats)
        self.widget.goHomeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGoHome)

    def setSideName(self, sideName):
        self.sideName = sideName
        self.refreshSideName()

    def refreshSideName(self):
        if not self.widget:
            return
        if not self.sideName:
            self.widget.selfGuildInfo.visible = False
            self.widget.enemyGuildInfo.visible = False
            return
        p = BigWorld.player()
        if getattr(p, 'bfSideNUID'):
            for k, v in self.sideName.iteritems():
                if k == p.bfSideNUID:
                    self.widget.selfGuildInfo.selfGuildName.text = v
                else:
                    self.widget.enemyGuildInfo.enemyGuildName.text = v

        self.widget.selfGuildInfo.visible = True
        self.widget.enemyGuildInfo.visible = True

    def setObserve(self):
        p = BigWorld.player()
        if p.inFightObserve():
            self.widget.statsBtn.visible = False
            self.widget.goHomeBtn.visible = False
        elif formula.inGuildTournamentBH(p.mapID):
            self.widget.praiseNumArea.visible = True
            self.widget.witnessNumArea.visible = True
        else:
            self.widget.praiseNumArea.visible = False
            self.widget.witnessNumArea.visible = False

    def initBFTime(self):
        totalTime = self.getTotalTime()
        self.widget.flagTimer.text = utils.formatTimeStr(totalTime, 'h:m:s')

    def startTimer(self):
        p = BigWorld.player()
        if not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            return
        self.durationTime = self.getDurationTime()
        if self.timeTick:
            BigWorld.cancelCallback(self.timeTick)
        self.widget.flagTimer.text = utils.formatTimeStr(self.durationTime, 'h:m:s')
        self.timeTick = BigWorld.callback(1, self.handleTimer)

    def handleTimer(self):
        self.durationTime = self.getDurationTime()
        if self.durationTime <= 0 or not self.widget:
            if self.timeTick:
                BigWorld.cancelCallback(self.timeTick)
            return
        self.widget.flagTimer.text = utils.formatTimeStr(self.durationTime, 'h:m:s')
        self.timeTick = BigWorld.callback(1, self.handleTimer)

    def getTotalTime(self):
        p = BigWorld.player()
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        return totalTime

    def getDurationTime(self):
        p = BigWorld.player()
        if not p or not p.bfTimeRec.has_key('tReady'):
            return 0
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        countTime = totalTime - int(p.getServerTime() - p.bfTimeRec['tReady'])
        return countTime

    def refreshStatsInfo(self):
        statsInfo = self.getStatsInfo()
        self.widget.selfNum.text = statsInfo['myCurRes']
        self.widget.enemyNum.text = statsInfo['enemyCurRes']
        self.widget.selfStats.currentValue = int(statsInfo['myCurRes'] * 1.0 / statsInfo['myMaxRes'] * 100)
        self.widget.enemyStats.currentValue = int(statsInfo['enemyCurRes'] * 1.0 / statsInfo['enemyMaxRes'] * 100)

    def getStatsInfo(self):
        p = BigWorld.player()
        obj = {}
        enemyMaxRes = myMaxRes = BFD.data.get(p.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        obj['myMaxRes'] = myMaxRes
        obj['myCurRes'] = p.getMyRes()
        obj['enemyMaxRes'] = enemyMaxRes
        obj['enemyCurRes'] = p.getEnemyRes()
        obj['isResBattleField'] = p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES)
        obj['isHookBattleField'] = p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK)
        return obj

    def setInspirePraiseData(self, gtInspireMorales, guildNUIDs, praisesNum, livesNum):
        self.inspirePraiseData['gtInspireMorales'] = gtInspireMorales
        self.inspirePraiseData['guildNUIDs'] = guildNUIDs
        self.inspirePraiseData['praisesNum'] = praisesNum
        self.inspirePraiseData['livesNum'] = livesNum
        self.refreshInspirePraiseData()

    def refreshInspirePraiseData(self):
        if not self.widget:
            return
        if not self.inspirePraiseData:
            return
        self.widget.praiseNumArea.txt.text = self.inspirePraiseData['praisesNum']
        self.widget.witnessNumArea.txt.text = self.inspirePraiseData['livesNum']
        self.refreshMoraleIcon()
        self.setEncourageBtnTip()

    def setEncourageBtnTip(self):
        if not self.inspirePraiseData:
            return
        if not self.widget:
            return
        guildNUIDs = self.inspirePraiseData['guildNUIDs']
        gtInspireMorales = self.inspirePraiseData['gtInspireMorales']
        selfGtInspireMorale, enemyGtInspireMorale = gameglobal.rds.ui.bFGuildTournamentLive.getMorales(guildNUIDs, gtInspireMorales)
        gameglobal.rds.ui.bFGuildTournamentLive.setMoraleTip(selfGtInspireMorale, self.widget.selfGuildInfo.bg)
        gameglobal.rds.ui.bFGuildTournamentLive.setMoraleTip(enemyGtInspireMorale, self.widget.enemyGuildInfo.bg)

    def refreshMoraleIcon(self):
        gtInspireMorales = self.inspirePraiseData.get('gtInspireMorales', [0, 0])
        selfGtInspireMorale = -1
        enemyGtInspireMorale = -1
        guildNUIDs = self.inspirePraiseData['guildNUIDs']
        selfGtInspireMorale, enemyGtInspireMorale = gameglobal.rds.ui.bFGuildTournamentLive.getMorales(guildNUIDs, gtInspireMorales)
        selfLv = gameglobal.rds.ui.bFGuildTournamentLive.getMoralesLv(selfGtInspireMorale)
        enemyLv = gameglobal.rds.ui.bFGuildTournamentLive.getMoralesLv(enemyGtInspireMorale)
        self.setMoraleLv(self.widget.selfGuildInfo, selfLv)
        self.setMoraleLv(self.widget.enemyGuildInfo, enemyLv)

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

    def handleClickStats(self, *args):
        gameglobal.rds.ui.battleField.onOpenStatsClick()

    def handleClickGoHome(self, *args):
        BigWorld.player().bfGoHome()
