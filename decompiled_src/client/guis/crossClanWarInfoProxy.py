#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossClanWarInfoProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gametypes
import gameglobal
import utils
from guis import uiUtils
from guis.asObject import MenuManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
import uiConst
import events
import gameconfigCommon
from gamestrings import gameStrings
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
RANK_UPDATE_INTERVAL = 6
from data import clan_war_fort_data as CWFD
from data import cross_clan_war_config_data as CCWCD

class CrossClanWarInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossClanWarInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_CLAN_WAR_INFO, self.hide)

    def reset(self):
        self.lastRankUpdateTime = 0
        self.isExpand = True
        self.isCross = False
        self.timer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_CLAN_WAR_INFO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.timer = self.timerFun()

    def clearWidget(self):
        self.widget = None
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_INFO)

    def show(self):
        if not gameglobal.rds.configData.get('enableCrossClanWar', False):
            return
        if BigWorld.player().mapID != const.SPACE_NO_BIG_WORLD:
            return
        self.isCross = BigWorld.player()._isSoul()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_INFO)

    def timerFun(self):
        if not self.widget:
            return
        self.refreshTime()
        if self.isExpand:
            self.refreshExpandMc()
        BigWorld.callback(1, self.timerFun)

    def getEndTime(self):
        endTime = 0
        for data in CWFD.data.itervalues():
            t = utils.getNextCrontabTime(data['endTime'])
            if not utils.isSameWeek(t, utils.getNow()):
                t = utils.getPreCrontabTime(data['endTime'])
            endTime = max(t, endTime)

        return endTime

    def refreshTime(self):
        endTime = self.getEndTime()
        leftTime = int(max(0, endTime - utils.getNow()))
        self.widget.txtLeftTime.text = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 1)

    def getGuildAndPlayerInfo(self):
        result = {}
        p = BigWorld.player()
        crossClanWarRealTimeInfo = getattr(p, 'crossClanWarRealTimeInfo', {})
        fortCnt = 0
        buildingCnt = 0
        fort = p.clanWar.fort
        for fortId, fortVal in fort.items():
            if fortVal.ownerGuildNUID == p.guildNUID:
                fortData = CWFD.data.get(fortId, '')
                if fortData and fortData.get('digongFort'):
                    continue
                if fortData:
                    if fortData.get('parentId'):
                        buildingCnt += 1
                    else:
                        fortCnt += 1

        result['ownFort'] = gameStrings.CROSS_CLAN_WAR_OCCUPY_FORT % fortCnt
        result['ownBuilding'] = gameStrings.CROSS_CLAN_WAR_OCCUPY_BUILDING % buildingCnt
        result['totalKill'] = crossClanWarRealTimeInfo.get('guildKillCnt', 0)
        result['personalKill'] = crossClanWarRealTimeInfo.get('killCnt', 0)
        result['personalDmg'] = crossClanWarRealTimeInfo.get('dmg', 0)
        result['personalCure'] = crossClanWarRealTimeInfo.get('cure', 0)
        result['score'] = crossClanWarRealTimeInfo.get('fameScore', 0)
        zhanchenNum = gameglobal.rds.ui.zhancheInfo.getzhancheNumber()
        result['zhancheNumber'] = '%d / %d' % (zhanchenNum[0], zhanchenNum[1])
        result['resultScore'] = crossClanWarRealTimeInfo.get('guildRecordScore', 0)
        if crossClanWarRealTimeInfo.get('guildRecordRank', None):
            result['resultRank'] = int(crossClanWarRealTimeInfo.get('guildRecordRank', 0))
        else:
            result['resultRank'] = gameStrings.RANK_NOT_IN_TEXT
        return result

    def refreshExpandMc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if utils.getNow() - self.lastRankUpdateTime >= RANK_UPDATE_INTERVAL:
            p.cell.getGuildZaijuUsedList(0)
            self.lastRankUpdateTime = utils.getNow()
        result = self.getGuildAndPlayerInfo()
        self.widget.resultScore.visible = gameconfigCommon.enableClanWarOptimizationRecord()
        self.widget.resultRank.visible = False
        self.widget.resultScoreTxt.visible = gameconfigCommon.enableClanWarOptimizationRecord()
        self.widget.resultRankTxt.visible = False
        self.widget.guildKill.text = result['totalKill']
        self.widget.ownFort.text = result['ownFort']
        self.widget.ownBuilding.text = result['ownBuilding']
        self.widget.personalKill.text = result['personalKill']
        self.widget.personalDmg.text = result['personalDmg']
        self.widget.personalCure.text = result['personalCure']
        if self.widget.personalPoint:
            self.widget.personalPoint.text = result['score']
        self.widget.txtVehicle.text = result['zhancheNumber']
        self.widget.resultScore.text = result['resultScore']
        self.widget.resultRank.text = result['resultRank']

    def initUI(self):
        pass

    def _checkInClanWar(self):
        if not BigWorld.player().clanWarStatus:
            BigWorld.player().showGameMsg(GMDD.data.DECLARE_WAR_NOT_IN_CLAN_WAR, ())
            return False
        return True

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.isExpand:
            self.widget.gotoAndStop('cross' if self.isCross else 'clanWar')
            self.widget.expandBtn.addEventListener(events.BUTTON_CLICK, self.handleExpandBtnClick, False, 0, True)
            self.refreshTime()
        else:
            self.widget.gotoAndStop('crossExpand' if self.isCross else 'clanWarExpand')
            self.refreshTime()
            self.refreshExpandMc()
            self.widget.shrinkBtn.addEventListener(events.BUTTON_CLICK, self.handleShrinkBtnClick, False, 0, True)
            self.widget.viewBtn.addEventListener(events.BUTTON_CLICK, self.handleViewBtnClick, False, 0, True)
            self.widget.zuLongBtn.addEventListener(events.BUTTON_CLICK, self.handleZuLongBtnClick, False, 0, True)
            self.widget.chuanSongBtn.addEventListener(events.BUTTON_CLICK, self.handleChuanSongBtnClick, False, 0, True)
            self.widget.zhanLingBtn.addEventListener(events.BUTTON_CLICK, self.handleZhanLingBtnClick, False, 0, True)
            if self.widget.yuanZhenBtn:
                self.widget.yuanZhenBtn.addEventListener(events.BUTTON_CLICK, self.handleCallMemberClick, False, 0, True)
            self.widget.infoBtn.addEventListener(events.BUTTON_CLICK, self.handleInfoBtnClick, False, 0, True)
            self.widget.declareBtn.addEventListener(events.BUTTON_CLICK, self.handleDeclareBtnClick, False, 0, True)
            self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.handleRankBtnClick, False, 0, True)
            self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)

    def handleInfoBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(2)

    def handleRankBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(1)

    def handleDeclareBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(3)

    def handleYuanZhenBtnClick(self, *args):
        seekId = CCWCD.data.get('yuanZhenSeekId', 0)
        uiUtils.findPosById(seekId)

    def handleRewardBtnClick(self, *args):
        self.uiAdapter.crossClanWarReward.show()

    def handleZhanLingBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(0)

    def handleCallMemberClick(self, *args):
        self.uiAdapter.guildCallMember.show()

    def handleChuanSongBtnClick(self, *args):
        if self._checkInClanWar():
            p = BigWorld.player()
            if not p.guild:
                p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, p.roleName)
                return
            nfort = len([ k for k, v in p.clanWar.fort.iteritems() if p.guildNUID and p.guildNUID == v.ownerGuildNUID ])
            if not nfort:
                p.showGameMsg(GMDD.data.CLAN_WAR_TELEPORT_NO_STONE, ())
                return
            if nfort > 1:
                self._confirmClanWarTeleport()
                return
            now = p.getServerTime()
            guildSkill = p.guildSkills.get(gametypes.GUILD_SKILL_TELEPORT)
            nextTime = guildSkill and guildSkill.nextTime or 0
            if nextTime < now:
                nextTime = 0
            msg = gameStrings.TEXT_CLANWARPROXY_240
            if not nextTime:
                msg = msg % gameStrings.TEXT_CLANWARPROXY_214
            else:
                msg = msg % (gameStrings.TEXT_CLANWARPROXY_216 % utils.formatTime(nextTime - now))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._confirmClanWarTeleport, yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def _confirmClanWarTeleport(self):
        BigWorld.player().cell.clanWarTeleport()

    def handleZuLongBtnClick(self, *args):
        if self._checkInClanWar():
            p = BigWorld.player()
            if not p.guild:
                p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (p.roleName,))
                return
            gameglobal.rds.ui.clanWarSkill.show()

    def _confirmClanWarStoneShield(self):
        BigWorld.player().cell.clanWarStoneShield()

    def handleViewBtnClick(self, *args):
        gameglobal.rds.ui.zhancheInfo.show()

    def handleShrinkBtnClick(self, *args):
        self.isExpand = False
        self.refreshInfo()

    def handleExpandBtnClick(self, *args):
        self.isExpand = True
        self.refreshInfo()

    def getMenuByTeleportData(self, menuData):
        menu = self.widget.getInstByClsName('menuCls')
        maxWidth = 0
        maxHeight = 0
        for i in xrange(len(menuData)):
            menuItem = self.widget.getInstByClsName('menubutton')
            menu.addChild(menuItem)
            menuItem.label = menuData[i][0]
            if menuItem.width > maxWidth:
                maxWidth = menuItem.width
            menuItem.x = 10
            menuItem.y = 7 + 19 * i
            maxHeight = menuItem.y + 7 + 19
            menuItem.data = menuData[i][1]
            menuItem.addEventListener(events.BUTTON_CLICK, self.onMenuClick, False, 0, True)

        menu.menubg.width = 10 + maxWidth + 10
        menu.menubg.height = maxHeight
        return menu

    def onMenuClick(self, *args):
        event = ASObject(args[3][0])
        fortId = event.currentTarget.data
        fortName = event.currentTarget.label
        p = BigWorld.player()
        now = p.getServerTime()
        guildSkill = p.guildSkills.get(gametypes.GUILD_SKILL_TELEPORT)
        nextTime = guildSkill and guildSkill.nextTime or 0
        if nextTime < now:
            nextTime = 0
        msg = gameStrings.TEXT_CLANWARPROXY_261
        if not nextTime:
            msg = msg % (fortName, gameStrings.TEXT_CLANWARPROXY_214)
        else:
            msg = msg % (fortName, gameStrings.TEXT_CLANWARPROXY_216 % utils.formatTime(nextTime - now))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda fortId = fortId: self._confirmClanWarTeleportToFort(fortId), yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def _confirmClanWarTeleportToFort(self, fortId):
        self._teleportToFort(fortId)

    def _teleportToFort(self, fortId):
        BigWorld.player().cell.clanWarTeleportToSelectedStone(fortId)

    def getClanWar(self):
        p = BigWorld.player()
        return p.clanWar

    def showSelectStoneToTeleport(self):
        if not self.widget:
            return
        p = BigWorld.player()
        forts = []
        for fortId, fort in self.getClanWar().fort.items():
            if fort.ownerGuildNUID == p.guildNUID:
                fortName = CWFD.data.get(fortId, {}).get('showName', '')
                forts.append((fortName, fortId))

        MenuManager.getInstance().hideMenuByTarget(self.widget.chuanSongBtn)
        menu = self.getMenuByTeleportData(forts)
        teleportBtn = self.widget.chuanSongBtn
        pos = ASUtils.local2Global(teleportBtn, teleportBtn.x - 60, teleportBtn.y - 250)
        if menu:
            MenuManager.getInstance().showMenu(self.widget.chuanSongBtn, menu, {'x': pos[0],
             'y': pos[1]})
