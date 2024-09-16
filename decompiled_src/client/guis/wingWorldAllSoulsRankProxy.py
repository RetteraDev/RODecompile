#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldAllSoulsRankProxy.o
import BigWorld
import events
import uiConst
import gameglobal
import sys
import sMath
import formula
from gamestrings import gameStrings
from uiProxy import UIProxy
from asObject import ASObject
from asObject import TipManager
from helpers import tickManager
from data import region_server_config_data as RSCD
from data import wing_soul_boss_data as WSBD
from cdata import soul_boss_chartype_to_cfgid_data as SBCTCD
import gamelog
ALLSOULS_TAB_GUILD = 0
ALLSOULS_TAB_PERSON = 1
REQUEST_INTERVAL = 5
MAX_PUSH_MSG_COUNT = 3

class WingWorldAllSoulsRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldAllSoulsRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.selectedItem = None
        self.currentTab = ALLSOULS_TAB_GUILD
        self.timerId = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK, self.hide)
        self.allBossAvatarId = [ bdata.get('avatarId', 0) for bdata in WSBD.data.values() ]
        self.lastBossId = -1

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK)
        self.selectedItem = None
        if self.timerId != -1:
            tickManager.stopTick(self.timerId)
            self.timerId = -1
        bossId = self.lastBossId
        if bossId != -1:
            self.addPushMsg(bossId)

    def closeRank(self):
        self.clearWidget()

    def onMsgCallback1(self):
        msgData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_1)
        if msgData:
            self.realShow(msgData.get('data', -1))

    def onMsgCallback2(self):
        msgData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_2)
        if msgData:
            self.realShow(msgData.get('data', -1))

    def onMsgCallback3(self):
        msgData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_3)
        if msgData:
            self.realShow(msgData.get('data', -1))

    def realShow(self, bossId):
        p = BigWorld.player()
        if not p.inWingPeaceCity():
            return
        nearestId = bossId
        if nearestId == -1:
            return
        self.show(bossId)

    def show(self, bossId):
        if bossId == -1:
            return
        self.lastBossId = bossId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_ALLSOULS_RANK)
        else:
            self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.guildTab.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.personalTab.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        self.widget.guildPanel.list.itemRenderer = 'WingWorldAllSoulsRank_GuildListItem'
        self.widget.guildPanel.list.labelFunction = self.guildListFunction
        self.widget.guildPanel.list.dataArray = []
        self.widget.personalPanel.list.itemRenderer = 'WingWorldAllSoulsRank_PersonListItem'
        self.widget.personalPanel.list.labelFunction = self.personListFunction
        self.widget.personalPanel.list.dataArray = []
        self.widget.firstGuild.text = ''
        self.widget.finalGuild.text = ''
        self.widget.firstPlayer.text = ''
        self.widget.finalPlayer.text = ''
        self.clearPushMsg()
        if self.timerId != -1:
            tickManager.stopTick(self.timerId)
        self.timerId = tickManager.addTick(REQUEST_INTERVAL, self.requestTimer)
        self.onGuildPanelShow()
        if self.lastBossId != -1:
            p = BigWorld.player()
            p.base.getSoulBossSpecialDamageInfo(self.lastBossId)

    def refreshInfo(self):
        if not self.widget:
            return

    def requestTimer(self):
        bossId = self.lastBossId
        if bossId == -1:
            return
        if self.currentTab == ALLSOULS_TAB_GUILD:
            p = BigWorld.player()
            p.base.getSoulBossGuildDamageInfo(bossId)
        if self.currentTab == ALLSOULS_TAB_PERSON:
            p = BigWorld.player()
            p.base.getSoulBossMemberDamageInfo(bossId, p.camp)

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedItem:
            self.selectedItem.selected = False
        if e.target.name == 'guildTab':
            self.onGuildPanelShow()
        if e.target.name == 'personalTab':
            self.onPersonalPanelShow()

    def handleRewardBtnClick(self, *args):
        bossId = self.lastBossId
        if bossId == -1:
            return
        gameglobal.rds.ui.wingWorldAllSoulsRankReward.show(bossId)

    def onGuildPanelShow(self):
        self.widget.guildPanel.visible = True
        self.widget.personalPanel.visible = False
        self.currentTab = ALLSOULS_TAB_GUILD
        self.selectedItem = self.widget.guildTab
        self.widget.guildTab.selected = True
        bossId = self.lastBossId
        if bossId == -1:
            return
        p = BigWorld.player()
        p.base.getSoulBossGuildDamageInfo(bossId)

    def onPersonalPanelShow(self):
        self.widget.guildPanel.visible = False
        self.widget.personalPanel.visible = True
        self.currentTab = ALLSOULS_TAB_PERSON
        self.selectedItem = self.widget.personalTab
        self.widget.personalTab.selected = True
        bossId = self.lastBossId
        if bossId == -1:
            return
        p = BigWorld.player()
        p.base.getSoulBossMemberDamageInfo(bossId, p.camp)

    def refreshGuildPanel(self, bossId, data):
        gamelog.debug('ypc@ guild data = ', data)
        if not self.widget or self.currentTab != ALLSOULS_TAB_GUILD:
            return
        if not data:
            self.widget.guildPanel.list.dataArray = []
            return
        self.widget.guildPanel.list.dataArray = data

    def refreshPersonPanel(self, bossId, data):
        gamelog.debug('ypc@ person data = ', data)
        if not self.widget or self.currentTab != ALLSOULS_TAB_PERSON:
            return
        if not data:
            self.widget.personalPanel.list.dataArray = []
            return
        dataArray = [data.get('maxDmg', {}), data.get('maxCure', {}), data.get('maxHurted', {})]
        self.widget.personalPanel.list.dataArray = dataArray

    def refreshBossStateInfo(self, data):
        if not self.widget or not self.widget.firstPlayer:
            return
        firstAtkName = data.get('firstAttacker', {}).get('name', '')
        firstAtkGuild = data.get('firstAttacker', {}).get('guildName', '')
        killerName = data.get('killer', {}).get('name', '')
        killerGuild = data.get('killer', {}).get('guildName', '')
        self.widget.firstPlayer.text = firstAtkName
        self.widget.firstGuild.text = firstAtkGuild
        self.widget.finalPlayer.text = killerName
        self.widget.finalGuild.text = killerGuild

    def guildListFunction(self, *args):
        info = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.rank.text = str(itemMc.index + 1)
        itemMc.guildName.text = info.guildName
        itemMc.value.text = '%.2f%%' % (float(info.dmg) / 100)
        if info.hostId and info.hostId in RSCD.data:
            tipStr = gameStrings.WING_WORLD_ALLSOULS_HOSTNAME % RSCD.data[info.hostId].get('serverName', '')
            TipManager.addTip(itemMc.guildName, tipStr)

    def personListFunction(self, *args):
        info = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemMc.index == 0:
            itemMc.rankType.text = gameStrings.WING_WORLD_ALLSOULS_DMGTOP
            itemMc.value.text = str(info.value)
        if itemMc.index == 1:
            itemMc.rankType.text = gameStrings.WING_WORLD_ALLSOULS_CURETOP
            itemMc.value.text = str(info.value)
        if itemMc.index == 2:
            itemMc.rankType.text = gameStrings.WING_WORLD_ALLSOULS_HURTEDTOP
            itemMc.value.text = str(info.value)
        namelist = info.name.split('-')
        if len(namelist) > 1:
            serverName = namelist[-1]
            for sdata in RSCD.data.values():
                if serverName == sdata.get('serverName', ''):
                    break
            else:
                itemMc.guildName.text = info.name

            itemMc.guildName.text = info.name[0:info.name.rfind(serverName) - 1]
            if info.hostId and info.hostId in RSCD.data:
                tipStr = gameStrings.WING_WORLD_ALLSOULS_HOSTNAME % RSCD.data[info.hostId].get('serverName', '')
                TipManager.removeTip(itemMc.guildName)
                TipManager.addTip(itemMc.guildName, tipStr)
                gamelog.debug('ypc@ tipname = ', tipStr)
        else:
            itemMc.guildName.text = info.name

    def addPushMsg(self, bossId):
        p = BigWorld.player()
        if not p.inWingPeaceCity():
            return
        else:
            unUsedMsg = uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_1
            clickCallback = None
            if gameglobal.rds.ui.pushMessage.hasMsgType(unUsedMsg):
                return
            if unUsedMsg == uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_1:
                clickCallback = self.onMsgCallback1
            elif unUsedMsg == uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_2:
                clickCallback = self.onMsgCallback2
            elif unUsedMsg == uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_3:
                clickCallback = self.onMsgCallback3
            gamelog.debug('ypc@ addPushMsg unUsedMsg, clickCallback ', unUsedMsg, clickCallback)
            if unUsedMsg != -1 and clickCallback:
                gameglobal.rds.ui.pushMessage.addPushMsg(unUsedMsg, {'data': bossId})
                gameglobal.rds.ui.pushMessage.setCallBack(unUsedMsg, {'click': clickCallback})
            return

    def getUnUsedMsg(self):
        for msg in uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_LIST:
            if not gameglobal.rds.ui.pushMessage.hasMsgType(msg):
                return msg

        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_1)
        return uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_BOSS_1

    def clearPushMsg(self):
        for msg in uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_LIST:
            gameglobal.rds.ui.pushMessage.removePushMsg(msg)

    def isBossIdInMsg(self, bossId):
        for msg in uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_SOUL_LIST:
            msgData = gameglobal.rds.ui.pushMessage.getLastData(msg)
            if msgData and bossId != -1 and msgData.get('data', -1) == bossId:
                return True

        return False

    def getNearestBossId(self):
        entities = BigWorld.entities.items()
        bosslist = []
        for id, ent in entities:
            if getattr(ent, 'monsterInstance', False):
                monsterId = getattr(ent, 'charType', -1)
                if monsterId != -1 and monsterId in self.allBossAvatarId:
                    bosslist.append(ent)

        if not bosslist:
            return -1
        p = BigWorld.player()
        nearestId = -1
        d = sys.float_info.max
        for boss in bosslist:
            bossDistance = sMath.distance2D(boss.position, p.position)
            if bossDistance < d:
                nearestId = getattr(boss, 'charType', -1)
                d = bossDistance

        if nearestId != -1:
            return self.getBossId(formula.getWingCityGroupId(p.spaceNo), nearestId)
        return -1

    def getBossId(self, age, avatarId):
        if avatarId not in SBCTCD.data:
            return -1
        if age not in SBCTCD.data[avatarId]:
            return -1
        return SBCTCD.data[avatarId][age]

    def isWingSoulBoss(self, ent):
        if not ent:
            return False
        if getattr(ent, 'monsterInstance', False):
            monsterId = getattr(ent, 'charType', -1)
            if monsterId != -1 and monsterId in self.allBossAvatarId:
                return True
        return False
