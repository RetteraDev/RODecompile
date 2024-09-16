#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/killFallenRedGuardRankProxy.o
import BigWorld
import gameglobal
import const
import uiConst
import events
from guis.asObject import ASObject
import gamelog
import utils
import gametypes
from helpers import navigator
from callbackHelper import Functor
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import TipManager
from data import fallen_red_guard_data as FRGD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class KillFallenRedGuardRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(KillFallenRedGuardRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.trunkNameToFlagDic = {}
        self.firstAttackerInfo = (0, '', 0, '')
        self.killerInfo = (0, '', 0, '')
        self.guildsDamageList = []
        self.lastTrunkName = ''
        self.flagSafeRecord = {}
        self.flagDeathTimeDic = {}
        self.monsterFlag = False
        self.callback = None
        self.currentCallbackFun = None
        self.continuePathFinding = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_RANK, self.hide)

    def reset(self):
        self.lastConfirmTime = 0
        self.lastApplyTime = 0
        self.timer = 0
        self.showTimer = 0
        self.isJointed = False
        self.attackerNum = 0

    def clearAll(self):
        self.trunkNameToFlagDic = {}
        self.firstAttackerInfo = (0, 0, 0, 0)
        self.killerInfo = (0, 0, 0, 0)
        self.guildsDamageList = []
        self.lastTrunkName = ''
        self.flagSafeRecord = {}
        self.callback = None
        self.continuePathFinding = False
        self.monsterFlag = False

    def getFlagByTrunkName(self, trunkName):
        if not self.trunkNameToFlagDic:
            for flag, value in FRGD.data.iteritems():
                name = value.get('trunkName', '')
                if name:
                    self.trunkNameToFlagDic[name] = flag

        return self.trunkNameToFlagDic.get(trunkName, 0)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_KILL_FALLEN_RED_GUARD_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def setFlagIsSafe(self, flag, isSafe, deathTime):
        if not gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
            return
        self.flagSafeRecord[flag] = isSafe
        self.flagDeathTimeDic[flag] = deathTime
        if self.callback:
            if not self.currentCallbackFun and not isSafe:
                self.currentCallbackFun = self.callback
                self.callback = None
                msg = GMD.data.get(GMDD.data.TELEPORT_FALLEN_RED_GUARD, {}).get('text', '')
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.yesCallback, noCallback=self.noCallback)
            else:
                self.callback()
                self.callback = None
                return
            return
        else:
            return

    def addPushIcon(self):
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_FALLEN_RED_GUARD):
            gamelog.info('jbx:addPushIcon')
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_FALLEN_RED_GUARD)
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FALLEN_RED_GUARD, {'click': self.show})

    def delPushIcon(self):
        if self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_FALLEN_RED_GUARD):
            gamelog.info('jbx:delPushIcon')
            self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FALLEN_RED_GUARD)

    def yesCallback(self):
        if self.currentCallbackFun:
            self.currentCallbackFun()
            self.currentCallbackFun = None
        nav = navigator.getNav()
        if self.continuePathFinding and getattr(nav, 'lastPathFindingArgs', None):
            fun, args = nav.lastPathFindingArgs
            continePathFun = Functor(fun, *args)
            BigWorld.callback(2, continePathFun)
        self.callback = None
        self.continuePathFinding = False
        nav.lastPathFindingArgs = None

    def noCallback(self):
        self.currentCallbackFun = None
        self.callback = None
        nav = navigator.getNav()
        nav.lastPathFindingArgs = None

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_RANK)
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = 0

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_KILL_FALLEN_RED_GUARD_RANK)
            if self.timer:
                BigWorld.cancelCallback(self.timer)
                self.timer = 0
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'KillFallenRedGuardRank_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        TipManager.addTip(self.widget.txtMonsterName, GCD.data.get('killFallenRedGuardTips', 'tips'))

    def updateInfo(self, firstAttackerInfo, killerInfo, guildsDamageList, isJoined):
        gamelog.info('jbx:updateInfo', firstAttackerInfo, killerInfo, guildsDamageList, self.monsterFlag)
        p = BigWorld.player()
        self.attackerNum = 0
        for guildNUID, guildName, percent, attackersNum in guildsDamageList:
            if p.guild and p.guild.nuid == guildNUID:
                self.attackerNum = attackersNum
                break

        if not firstAttackerInfo:
            firstAttackerInfo = (0, '', 0, '')
        if not killerInfo:
            killerInfo = (0, '', 0, '')
        self.firstAttackerInfo = firstAttackerInfo
        self.killerInfo = killerInfo
        self.guildsDamageList = guildsDamageList
        self.isJointed = isJoined
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.attackGuildName.text = self.firstAttackerInfo[1]
        self.widget.attackPlayerName.text = self.firstAttackerInfo[3]
        self.widget.killGuildName.text = self.killerInfo[1]
        self.widget.killPlayerName.text = self.killerInfo[3]
        self.guildsDamageList.sort(cmp=lambda x, y: cmp(x[2], y[2]), reverse=True)
        self.widget.scrollWndList.dataArray = range(len(self.guildsDamageList))
        self.widget.isJoined.visible = self.isJointed
        p = BigWorld.player()
        if p.guild and p.guild.nuid:
            self.widget.txtAttackerNum.text = gameStrings.KILL_FALLEN_ATTACKER_NUM % self.attackerNum
        else:
            self.widget.txtAttackerNum.text = ''
        self.widget.txtMonsterName.text = FRGD.data.get(self.monsterFlag, {}).get('titleName', '')

    def labelFunction(self, *args):
        index = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        guildNuid, guildName, percent, attackerNum = self.guildsDamageList[index]
        itemMc.txtRank.text = str(index + 1)
        if index < 3:
            itemMc.rankIcon.visible = True
            itemMc.rankIcon.gotoAndStop('rank%d' % (index + 1))
            itemMc.txtRank.visible = False
        else:
            itemMc.rankIcon.visible = False
            itemMc.txtRank.visible = True
        itemMc.txtGuildName.text = guildName
        itemMc.txtPercent.text = '%.2f%%' % percent

    def handleRewardBtnClick(self, *args):
        gamelog.info('jbx:handleRewardBtnClick')
        self.uiAdapter.killFallenRedGuardReward.show()

    def test(self):
        firstAttackerInfo = (0, 'guildName', 1, 'role1')
        fkillerInfo = (0, 'guildName2', 2, 'role2')
        rankList = []
        for i in xrange(10):
            info = (0,
             'guildName%d' % i,
             i,
             'role%d' % i)
            rankList.append(info)

        self.updateInfo(firstAttackerInfo, fkillerInfo, rankList)
        self.show()

    def checkTrunk(self, trunkName, force = False):
        if not gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
            return
        startTime = GCD.data.get('fallenRedGuardStartTime', [])
        endTime = GCD.data.get('fallenRedGuardEndTime', [])
        if not (startTime and endTime and utils.inTimeRange(startTime, endTime)):
            self.delPushIcon()
            return
        p = BigWorld.player()
        flag = self.getFlagByTrunkName(trunkName)
        isDeadOverTime = False
        if not flag:
            self.delPushIcon()
            if self.widget:
                self.hide()
            return
        if (flag, True) in getattr(p, 'fallenRedGuardFlagList', []) and self.flagDeathTimeDic.get(flag, 0) and self.flagDeathTimeDic[flag] + 60 < utils.getNow():
            isDeadOverTime = True
            self.delPushIcon()
            if self.widget:
                self.hide()
        elif not self.flagSafeRecord.get(flag, True):
            self.addPushIcon()
        if not isDeadOverTime and utils.getNow() - self.lastApplyTime > 3:
            if self.monsterFlag and flag:
                BigWorld.player().base.getFallenRedGuardDamageInfo(flag)
            self.lastApplyTime = utils.getNow()
            if gameglobal.rds.ui.killFallenRedGuardReward.isSpecial() and BigWorld.player().pkMode != const.PK_MODE_KILL:
                BigWorld.player().cell.checkForcePK(gametypes.IMP_PK_RESOURCE_FALLEN)
        if flag in self.flagSafeRecord and not self.flagSafeRecord.get(flag, True):
            if utils.getNow() - self.lastConfirmTime > 10:
                p.showGameMsg(GMDD.data.IN_FALLEN_RED_GUARD, ())
                self.lastConfirmTime = utils.getNow()
        if self.lastTrunkName == trunkName:
            if not force:
                return
        self.lastTrunkName = trunkName

    def enterMonster(self, flag):
        self.monsterFlag = flag
        self.checkTrunk(self.lastTrunkName, True)
        BigWorld.player().base.getFallenRedGuardDamageInfo(flag)
        self.showTimer = BigWorld.callback(1, self.show)
        gamelog.info('jbx:enterMonster', flag)
        BigWorld.player().cell.checkForcePK(gametypes.IMP_PK_RESOURCE_FALLEN)

    def leaveMonster(self, monster):
        gamelog.info('jbx:leaveMonster', monster.hp)
        BigWorld.player().base.getFallenRedGuardChunkInfo(self.monsterFlag)
        BigWorld.player().base.getFallenRedGuardDamageInfo(self.monsterFlag)
        if self.showTimer:
            BigWorld.cancelCallback(self.showTimer)
            self.showTimer = 0
        BigWorld.player().cell.checkForcePK(gametypes.IMP_PK_RESOURCE_FALLEN)
