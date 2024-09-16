#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFFortInfoV1Proxy.o
import BigWorld
import gameglobal
import uiConst
import events
import sMath
import utils
import formula
from uiProxy import UIProxy
from data import battle_field_data as BFD
MAX_PROGRESS_WIDTH = 262
MAX_PLANE_NUM = 5
MAX_EFFECT_LV = 3
HP_NUM = 2

class BFFortInfoV1Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFFortInfoV1Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.durationTime = 0
        self.timeTick = None
        self.inspirePraiseData = {}
        self.sideName = {}

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_FORT_INFO_V1)
        self.widget = None

    def initUI(self):
        p = BigWorld.player()
        self.planeMcs = [self.widget.selfPlane, self.widget.enemyPlane]
        bulletMax = BFD.data.get(p.getBattleFieldFbNo(), {}).get('maxBullet', 50)
        ret = {'myBullet': p.getMyBullet(),
         'enemyBullet': p.getEnemyBullet(),
         'myMaxBullet': bulletMax,
         'enemyMaxBullet': bulletMax}
        self.setFortInfo()
        self.setBulletInfo(ret)
        self.initBFTime()
        self.setObserve()
        self.refreshInspirePraiseData()
        self.startTimer()
        self.refreshSideName()
        self.widget.statsBtn.addEventListener(events.MOUSE_CLICK, self.handleClickStats)
        self.widget.goHomeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGoHome)

    def initBFTime(self):
        p = BigWorld.player()
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        self.widget.flagTimer.text = utils.formatTimeStr(totalTime, 'h:m:s')

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

    def refreshMoraleIcon(self):
        if not self.widget:
            return
        else:
            gtInspireMorales = self.inspirePraiseData.get('gtInspireMorales', None)
            if not gtInspireMorales:
                return
            guildNUIDs = self.inspirePraiseData['guildNUIDs']
            selfGtInspireMorale, enemyGtInspireMorale = gameglobal.rds.ui.bFGuildTournamentLive.getMorales(guildNUIDs, gtInspireMorales)
            selfLv = gameglobal.rds.ui.bFGuildTournamentLive.getMoralesLv(selfGtInspireMorale)
            enemyLv = gameglobal.rds.ui.bFGuildTournamentLive.getMoralesLv(enemyGtInspireMorale)
            self.setMoraleLv(self.widget.selfGuildInfo, selfLv)
            self.setMoraleLv(self.widget.enemyGuildInfo, enemyLv)
            return

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

    def setObserve(self):
        p = BigWorld.player()
        if p.inFightObserve():
            self.widget.statsBtn.visible = False
            self.widget.goHomeBtn.visible = False
            self.widget.fortOccupNum.visible = False
            self.widget.fortIcon.visible = False
            self.widget.myBulletScore.visible = False
            self.widget.enemyBulletScore.visible = False
            self.widget.bg.height = 60
            self.widget.praiseNumArea.x = 120
            self.widget.praiseNumArea.y = 81
            self.widget.witnessNumArea.x = 226
            self.widget.witnessNumArea.y = 81
        elif not formula.inGuildTournamentQL(p.mapID):
            self.widget.praiseNumArea.visible = False
            self.widget.witnessNumArea.visible = False
        else:
            self.widget.praiseNumArea.visible = True
            self.widget.witnessNumArea.visible = True

    def startTimer(self):
        self.durationTime = self.getDurationTime()
        if self.timeTick:
            BigWorld.cancelCallback(self.timeTick)
        self.widget.flagTimer.text = utils.formatTimeStr(self.durationTime, 'h:m:s')
        self.timeTick = BigWorld.callback(1, self.handleTimer)

    def getDurationTime(self):
        p = BigWorld.player()
        if not p or not p.bfTimeRec:
            return 0
        if p.__class__.__name__ == 'PlayerAccount':
            return 0
        if not p.bfTimeRec.has_key('tReady'):
            return 0
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        countTime = totalTime - int(p.getServerTime() - p.bfTimeRec['tReady'])
        return countTime

    def handleTimer(self):
        self.durationTime = self.getDurationTime()
        if self.durationTime <= 0:
            if self.timeTick:
                BigWorld.cancelCallback(self.timeTick)
            return
        self.timeTick = BigWorld.callback(1, self.handleTimer)
        if self.widget:
            self.widget.flagTimer.text = utils.formatTimeStr(self.durationTime, 'h:m:s')

    def setBulletInfo(self, ret):
        myBar = self.widget.myBulletScore.bar.bar
        enemyBar = self.widget.enemyBulletScore.bar.bar
        myBar.validateNow()
        enemyBar.validateNow()
        myBar.currentValue = ret['myBullet']
        myBar.maxValue = ret['myMaxBullet']
        self.widget.myBulletScore.barEffect.visible = ret['myBullet'] == ret['myMaxBullet']
        if ret['myBullet'] == ret['myMaxBullet']:
            self.widget.myBulletScore.gotoAndPlay(0)
            self.widget.myBulletScore.barEffect.gotoAndPlay(0)
        else:
            self.widget.myBulletScore.gotoAndStop(0)
        enemyBar.currentValue = ret['enemyBullet']
        enemyBar.maxValue = ret['enemyMaxBullet']
        self.widget.enemyBulletScore.barEffect.visible = ret['enemyBullet'] == ret['enemyMaxBullet']
        if ret['enemyBullet'] == ret['enemyMaxBullet']:
            self.widget.enemyBulletScore.gotoAndPlay(0)
            self.widget.enemyBulletScore.barEffect.gotoAndPlay(0)
        else:
            self.widget.enemyBulletScore.gotoAndStop(0)

    def setHpInfo(self, ret):
        if len(ret) != HP_NUM:
            return
        myInfo = ret[0]
        enemyInfo = ret[1]
        self.widget.selfNum.htmlText = myInfo['hp']
        self.widget.selfStats.currentValue = myInfo['hp']
        self.widget.selfStats.maxValue = myInfo['mhp']
        self.widget.enemyNum.htmlText = enemyInfo['hp']
        self.widget.enemyStats.currentValue = enemyInfo['hp']
        self.widget.enemyStats.maxValue = enemyInfo['mhp']

    def setFortInfo(self, ret = None):
        if ret == None:
            self.widget.fortIcon.visible = False
            self.widget.fortOccupNum.visible = False
        else:
            self.widget.fortIcon.visible = True
            self.widget.fortOccupNum.visible = True
            self.widget.fortIcon.gotoAndStop('type%d' % ret['fortType'])
            self.widget.fortIcon.icon.gotoAndStop('c%d' % ret['state'])
            self.widget.fortOccupNum.thumb.x = MAX_PROGRESS_WIDTH * (0.5 - ret['fortVal'] / (ret['values'][1] * 1.0) * 0.5)
            self.widget.fortOccupNum.thumb.x = sMath.clamp(self.widget.fortOccupNum.thumb.x, 0, MAX_PROGRESS_WIDTH)

    def setAllPlaneInfo(self, ret):
        for i in xrange(0, len(self.planeMcs)):
            self.setPlaneInfo(self.planeMcs[i], ret[i])

    def setPlaneInfo(self, planeMc, info):
        for i in xrange(0, MAX_PLANE_NUM):
            plane = planeMc.getChildByName('plane%d' % i)
            plane.maxValue = 1
            if i < info[0]:
                plane.currentValue = 1
            elif i == info[0]:
                plane.currentValue = info[1]
            else:
                plane.currentValue = 0

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

    def handleClickStats(self, *args):
        gameglobal.rds.ui.battleField.onOpenStatsClick()

    def handleClickGoHome(self, *args):
        BigWorld.player().bfGoHome()
