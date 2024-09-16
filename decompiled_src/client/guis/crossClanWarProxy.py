#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossClanWarProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import uiUtils
from guis import ui
from gamestrings import gameStrings
import utils
import const
import uiConst
import events
from uiProxy import UIProxy
from data import clan_war_fort_data as CWFD
from data import wing_world_config_data as WWCD
from data import cross_clan_war_config_data as CCWCD
from cdata import cross_clan_war_region_data as CCWRD
from data import game_msg_data as GMD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import item_coin_dikou_cost_data as ICDCD
TAB_CLAN_WAR = 1
TAB_CROSS_CLAN_WAR = 2

class CrossClanWarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossClanWarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedTab = TAB_CLAN_WAR
        self.currentTabMc = None
        self.hostList = []
        self.showClanWarResult = False
        self.localSelectedHostId = None

    def initPanel(self, widget):
        self.widget = ASObject(widget)
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.clanWarBtn.addEventListener(events.BUTTON_CLICK, self.handleClanWarBtnClick, False, 0, True)
        self.widget.crossClanWar.addEventListener(events.BUTTON_CLICK, self.handleCrossClanWarBtnClick, False, 0, True)
        p = BigWorld.player()
        p.cell.getClanWarOpenInfo(utils.getHostId())
        isWingWorldOpen = gameglobal.rds.configData.get('enableWingWorld', False) and p.checkServerProgress(WWCD.data.get('finishMileStoneId', 19008), False)
        inGlobalClanWar = p.inGlobalClanWarTime() and utils.inCrontabRange(CCWCD.data.get('globalStartApplyTime', ''), CCWCD.data.get('globalEndTime', ''))
        if isWingWorldOpen or inGlobalClanWar:
            self.widget.crossClanWar.disabled = False
            TipManager.removeTip(self.widget.crossClanWar)
        else:
            self.widget.crossClanWar.disabled = True
            TipManager.addTip(self.widget.crossClanWar, CCWCD.data.get('wingWorldOpenTips', 'CCWCD.data.wingWorldOpenTips'))

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.clanWarBtn.selected = self.selectedTab == TAB_CLAN_WAR
        self.widget.clanWarTab.visible = self.selectedTab == TAB_CLAN_WAR
        self.widget.crossClanWar.selected = self.selectedTab == TAB_CROSS_CLAN_WAR
        self.widget.crossClanWarTab.visible = self.selectedTab == TAB_CROSS_CLAN_WAR
        if self.selectedTab == TAB_CLAN_WAR:
            self.currentTabMc = self.widget.clanWarTab
            self.refreshClanWar()
        else:
            self.currentTabMc = self.widget.crossClanWarTab
            self.refreshCrossClanWar()

    def handleClanWarBtnClick(self, *args):
        self.selectedTab = TAB_CLAN_WAR
        BigWorld.player().cell.getClanWarOpenInfo(utils.getHostId())
        self.refreshInfo()

    def getCroccClanWarTagHostId(self):
        crossHostId = getattr(BigWorld.player(), 'crossClanWarTgtHostId', 0)
        if not crossHostId:
            crossHostId = getattr(BigWorld.player(), 'clanWarCrossHostId', utils.getHostId())
        return crossHostId

    def handleCrossClanWarBtnClick(self, *args):
        self.selectedTab = TAB_CROSS_CLAN_WAR
        BigWorld.player().cell.getClanWarOpenInfo(self.getCroccClanWarTagHostId())
        self.refreshInfo()

    def refreshClanWar(self):
        if not self.widget or not self.currentTabMc:
            return
        p = BigWorld.player()
        self.currentTabMc.rankBtn.addEventListener(events.BUTTON_CLICK, self.handleShowRankBtnClick, False, 0, True)
        showClanWarResult = self.uiAdapter.topBar.showClanWarResult or BigWorld.player().clanWarStatus
        self.currentTabMc.rankBtn.enabled = not showClanWarResult
        self.currentTabMc.clanInfoBtn.enabled = showClanWarResult
        self.currentTabMc.killEnemyInfoBtn.enabled = showClanWarResult
        self.currentTabMc.declareWarInfoBtn.enabled = showClanWarResult
        self.currentTabMc.worldBossCardBtn.visible = gameglobal.rds.configData.get('enableWorldBoss', False)
        self.currentTabMc.historyBtn.addEventListener(events.BUTTON_CLICK, self.handleHistoryBtnClick, False, 0, True)
        self.currentTabMc.clanInfoBtn.addEventListener(events.BUTTON_CLICK, self.handleClanInfoBtnClick, False, 0, True)
        self.currentTabMc.killEnemyInfoBtn.addEventListener(events.BUTTON_CLICK, self.handleKillEnemyInfoBtnClick, False, 0, True)
        self.currentTabMc.declareWarInfoBtn.addEventListener(events.BUTTON_CLICK, self.handleDeclareWarInfoBtnClick, False, 0, True)
        self.currentTabMc.worldBossCardBtn.addEventListener(events.BUTTON_CLICK, self.handleWorldBossClick, False, 0, True)
        self.refreshFortInfo()
        self.currentTabMc.tipsContent.visible = not showClanWarResult
        self.currentTabMc.resultBtn.enabled = not p.clanWarStatus
        self.currentTabMc.resultBtn.addEventListener(events.BUTTON_CLICK, self.handleResultBntClick, False, 0, True)
        self.refreshCommonInfo()
        if gameglobal.rds.configData.get('enableClanWarOptimizationEvent', False):
            self.currentTabMc.timeDesc.visible = True
            self.currentTabMc.incidentBtn.visible = True
            self.currentTabMc.tips.visible = False
            self.currentTabMc.tips.tipDesc.text = CCWCD.data.get('clanWarIncidentTips', '')
            eventSeasonStartCrontab = CCWCD.data.get('eventSeasonStartCrontab')
            starTime = utils.formatDate(utils.getPreCrontabTime(eventSeasonStartCrontab))
            endTime = utils.formatDate(utils.getNextCrontabTime(eventSeasonStartCrontab) - 1)
            self.currentTabMc.timeDesc.text = gameStrings.CLAN_WAR_INCIDENT_TIME_DESC % (starTime, endTime)
            self.currentTabMc.incidentBtn.addEventListener(events.BUTTON_CLICK, self.handleIncidentBntClick, False, 0, True)
        else:
            self.currentTabMc.timeDesc.visible = False
            self.currentTabMc.incidentBtn.visible = False
            self.currentTabMc.tips.visible = False

    def testCrossClanWarHistoryData(self):
        fortCnt = 2
        buildingCnt = 3
        rank = 3
        memberCnt = 100
        guildKillCnt = 200
        fameScore = 10000
        killCnt = 20
        dmg = 1000000
        cure = 1000000
        BigWorld.player().clanWarHistoryData = (fortCnt,
         buildingCnt,
         rank,
         memberCnt,
         guildKillCnt,
         fameScore,
         killCnt,
         dmg,
         cure)
        self.refreshInfo()

    def getGuildAndPlayerInfo(self):
        result = {}
        p = BigWorld.player()
        if self.selectedTab == TAB_CLAN_WAR:
            clanWarHistoryData = getattr(p, 'clanWarHistoryData', [0] * 9)
        else:
            clanWarHistoryData = getattr(p, 'crossClanWarHistoryData', [0] * 9)
        fortCnt, buildingCnt, rank, memberCnt, guildKillCnt, fameScore, killCnt, dmg, cure = clanWarHistoryData
        result['ownFort'] = gameStrings.CROSS_CLAN_WAR_OCCUPY_FORT % fortCnt
        result['ownBuilding'] = gameStrings.CROSS_CLAN_WAR_OCCUPY_BUILDING % buildingCnt
        result['txtFortBuilding'] = '%s %s' % (result['ownFort'], result['ownBuilding'])
        result['guildRank'] = rank
        result['memerCnt'] = memberCnt
        result['totalKill'] = guildKillCnt
        result['personalKill'] = killCnt
        result['personalDmg'] = dmg
        result['personalCure'] = cure
        result['score'] = fameScore
        zhanchenNum = gameglobal.rds.ui.zhancheInfo.getzhancheNumber()
        result['zhancheNumber'] = '%d / %d' % (zhanchenNum[0], zhanchenNum[1])
        return result

    def refreshCommonInfo(self):
        if not self.widget or not self.currentTabMc:
            return None
        else:
            p = BigWorld.player()
            icon, color = uiUtils.getGuildFlag(p.guildFlag)
            if utils.isDownloadImage(icon) and not p.isDownloadNOSFileCompleted(icon):
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
            icon = uiUtils.getGuildIconPath(icon)
            self.currentTabMc.guildIcon.icon.fitSize = True
            self.currentTabMc.guildIcon.icon.loadImage(icon)
            if color:
                self.currentTabMc.guildIcon.color = color
            result = self.getGuildAndPlayerInfo()
            self.currentTabMc.txtFortBuilding.text = result['txtFortBuilding']
            self.currentTabMc.txtRank.text = result['guildRank']
            self.currentTabMc.txtMemberCnt.text = result['memerCnt']
            self.currentTabMc.killEnemy.text = result['totalKill']
            self.currentTabMc.personalKill.text = result['personalKill']
            self.currentTabMc.personalDmg.text = result['personalDmg']
            self.currentTabMc.personalCure.text = result['personalCure']
            if self.currentTabMc.personalPoint:
                self.currentTabMc.personalPoint.text = result['score']
            return None

    def getGuildPathAndClolor(self, flag):
        icon, color = uiUtils.getGuildFlag(flag)
        return (uiUtils.getGuildIconPath(icon), color)

    def getFortInfoList(self):
        fort = BigWorld.player().clanWar.fort
        fortGfxInfo = {}
        p = BigWorld.player()
        for fortId, fortVal in fort.iteritems():
            fortData = CWFD.data.get(fortId, '')
            if not fortData or fortData.get('digongFort'):
                continue
            if not fortData.get('parentId'):
                data = fortGfxInfo.get(fortId)
                if fortVal.ownerGuildName:
                    guildIcon, color = uiUtils.getGuildFlag(fortVal.ownerGuildFlag)
                    if uiUtils.isDownloadImage(guildIcon) and not p.isDownloadNOSFileCompleted(guildIcon):
                        if fortVal.fromHostId != utils.getHostId():
                            p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, fortVal.fromHostId, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                        else:
                            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                    icon, color = self.getGuildPathAndClolor(fortVal.ownerGuildFlag)
                else:
                    icon = uiConst.FORT_ICON_64 + '%s.dds' % fortId
                    color = 0
                if not data:
                    fortGfxInfo[fortId] = {'name': fortData.get('showName', ''),
                     'ownerGuildName': fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.CROSS_CLAN_WAR_NOT_OCCUPY,
                     'buildings': [],
                     'icon': icon,
                     'color': color}
                else:
                    data['name'] = fortData.get('showName', '')
                    data['ownerGuildName'] = fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.CROSS_CLAN_WAR_NOT_OCCUPY
                    data['icon'] = icon
                    data['color'] = color
            else:
                parentId = fortData.get('parentId')
                data = fortGfxInfo.get(parentId)
                if not data:
                    data = {'buildings': []}
                    fortGfxInfo[parentId] = data
                if fortVal.ownerGuildName:
                    icon, color = self.getGuildPathAndClolor(fortVal.ownerGuildFlag)
                else:
                    icon = uiConst.FORT_ICON_32 + '%s.dds' % fortId
                    color = 0
                data['buildings'].append({'name': fortData.get('showName', ''),
                 'ownerGuildName': fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.CROSS_CLAN_WAR_NOT_OCCUPY,
                 'icon': icon,
                 'color': color})

        return fortGfxInfo.values()

    def onDownloadGuildIcon(self, *args):
        pass

    def refreshFortInfo(self):
        if not self.widget or not self.currentTabMc:
            return
        else:
            info = self.getFortInfoList()
            arr = [self.currentTabMc.fort0, self.currentTabMc.fort1, self.currentTabMc.fort2]
            for i, mc in enumerate(arr):
                mc.title.text = info[i]['name'] + gameStrings.CROSS_CLAN_WAR_OCCUPY
                mc.fortName.text = info[i]['name']
                mc.fortIcon.fitSize = True
                mc.fortIcon.loadImage(info[i]['icon'])
                if info[i].get('color', None):
                    mc.fortIcon.color = info[i]['color']
                mc.guildName.text = info[i]['ownerGuildName']
                for j in xrange(4):
                    buildingMc = mc.getChildByName('building%d' % j)
                    if j < len(info[i]['buildings']):
                        buildingMc.fortName.text = info[i]['buildings'][j].get('name', '')
                        buildingMc.guildName.text = info[i]['buildings'][j].get('ownerGuildName', '')
                        buildingMc.fortIcon.fitSize = True
                        buildingMc.fortIcon.loadImage(info[i]['buildings'][j]['icon'])
                        buildingMc.visible = True
                        if info[i]['buildings'][j].get('color', None):
                            buildingMc.fortIcon.color = info[i]['buildings'][j]['color']
                    else:
                        buildingMc.visible = False

            return

    def getGlobalHostId(self):
        globalRegionServerId = CCWCD.data.get('globalRegionServerId', {})
        selfHostId = utils.getHostId()
        for regionHost, hostInfo in globalRegionServerId.iteritems():
            if selfHostId in hostInfo:
                return regionHost

    def getCrossClanWarInfo(self):
        p = BigWorld.player()
        crossResult = {}
        crossResult['selectedHostId'] = getattr(p, 'crossClanWarTgtHostId', 0)
        p = BigWorld.player()
        selfHostId = p.getOriginHostId()
        hostList = []
        crossClanApllyList = getattr(p, 'crossClanApllyList', [])
        if p.inGlobalClanWarTime():
            hostList.append(self.getGlobalHostId())
        else:
            for hostInfo in CCWRD.data.itervalues():
                for hosts in hostInfo.values():
                    if selfHostId in hosts:
                        hostList = [ hostId for hostId in hosts if hostId != selfHostId and hostId in crossClanApllyList ]
                        break

        crossResult['hostList'] = hostList
        crossResult['point'] = self.getGuildAndPlayerInfo()['score']
        crossResult['maxPoint'] = CCWCD.data.get('maxFameScore', 1000)
        return crossResult

    def refreshCrossClanWar(self):
        if not self.widget or not self.currentTabMc:
            return
        p = BigWorld.player()
        self.refreshCommonInfo()
        crossClanWarRuleTips = CCWCD.data.get('crossClanWarRuleTips', ('rule0', 'rule1', 'rule2', 'rule3'))
        for i in xrange(4):
            textMc = self.currentTabMc.getChildByName('tips%d' % i)
            textMc.text = crossClanWarRuleTips[i] if i < len(crossClanWarRuleTips) else ''

        crossResult = self.getCrossClanWarInfo()
        self.hostList = crossResult['hostList']
        self.currentTabMc.chooseHost.text = self.getServerName(crossResult['selectedHostId']) if crossResult.get('selectedHostId', 0) else ''
        self.currentTabMc.showResultBtn.addEventListener(events.BUTTON_CLICK, self.handleShowResultBtnClick, False, 0, True)
        self.currentTabMc.showResultBtn.visible = bool(crossResult['selectedHostId'])
        self.currentTabMc.historyBtn.addEventListener(events.BUTTON_CLICK, self.handleHistoryBtnClick, False, 0, True)
        if not p.inGlobalClanWarTime():
            isInTime = utils.inCrontabRange(CCWCD.data.get('startApplyTime', ''), CCWCD.data.get('endApplyTime', ''))
        else:
            isInTime = utils.inCrontabRange(CCWCD.data.get('globalStartApplyTime', ''), CCWCD.data.get('globalEndApplyTime', ''))
        self.currentTabMc.startBtn.enabled = isInTime and not crossResult['selectedHostId']
        ASUtils.setDropdownMenuData(self.currentTabMc.dropDown, crossResult['hostList'])
        self.currentTabMc.dropDown.addEventListener(events.EVENT_CHANGE, self.handleEventChange, False, 0, True)
        if crossResult['selectedHostId']:
            self.currentTabMc.dropDown.defaultText = self.getServerName(crossResult['selectedHostId'])
            self.currentTabMc.dropDown.selectedIndex = self.hostList.index(crossResult['selectedHostId'])
            self.currentTabMc.dropDown.enabled = False
        else:
            self.currentTabMc.dropDown.defaultText = gameStrings.CROSS_CLAN_WAR_NOT_SELECTED
            self.currentTabMc.dropDown.enabled = True
            self.currentTabMc.dropDown.enabled = True
        self.currentTabMc.dropDown.labelFunction = self.dropDownLabelFunction
        self.currentTabMc.startBtn.label = gameStrings.CROSS_CLAN_WAR_READY if crossResult['selectedHostId'] else gameStrings.CROSS_CLAN_WAR_START
        guildLevelLimit = CCWCD.data.get('guildLevelLimit', 8) if not p.inGlobalClanWarTime() else CCWCD.data.get('globalGuildLevelLimit', 6)
        TipManager.removeTip(self.currentTabMc.startBtn)
        if p.guild.level < guildLevelLimit:
            tipsContent = GMD.data.get(GMDD.data.CROSS_CLAN_WAR_APPLY_FAIL_GUILD_LEVEL_LIMIT, {}).get('text', '') % guildLevelLimit
            self.currentTabMc.startBtn.disabled = True
            TipManager.addTip(self.currentTabMc.startBtn, tipsContent)
        elif p.guild.memberMe.roleId not in gametypes.GUILD_ROLE_LEADERS:
            self.currentTabMc.startBtn.disabled = True
            tipsContent = GMD.data.get(GMDD.data.CROSS_CLAN_WAR_APPLY_FAIL_GUILD_LEADERS, {}).get('text', 'CROSS_CLAN_WAR_APPLY_FAIL_GUILD_LEADERS')
            TipManager.addTip(self.currentTabMc.startBtn, tipsContent)
        else:
            self.currentTabMc.startBtn.addEventListener(events.BUTTON_CLICK, self.handleStartBtnClick, False, 0, True)
        self.currentTabMc.txtPoint.text = str(crossResult['point'])
        TipManager.addTip(self.currentTabMc.point, CCWCD.data.get('pointTips', 'pointTips'))
        self.currentTabMc.openShop.addEventListener(events.BUTTON_CLICK, self.handleOpenShopBtnClick, False, 0, True)
        TipManager.addTip(self.currentTabMc.openShop, CCWCD.data.get('shopTips', 'shopTips'))
        self.currentTabMc.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoBtnClick, False, 0, True)
        self.currentTabMc.gotoBtn.label = gameStrings.CROSS_CLAN_WAR_RETURN if p.isInCrossClanWarStatus() else gameStrings.CROSS_CLAN_WAR_ENTER

    def handleEventChange(self, *args):
        index = int(self.currentTabMc.dropDown.selectedIndex)
        if index >= len(self.hostList) or index < 0:
            return
        self.localSelectedHostId = self.hostList[index]
        self.currentTabMc.showResultBtn.visible = True

    def handleGotoBtnClick(self, *args):
        p = BigWorld.player()
        if not p.isInCrossClanWarStatus():
            seekId = CCWCD.data.get('crossClanWarNpcSeekId', 10018142)
            uiUtils.findPosById(seekId)
        else:
            text = GMD.data.get(GMDD.data.CROSS_ClAN_WAR_RETURN, {}).get('text', 'CROSS_CLAN_WAR_RETURN')
            self.uiAdapter.messageBox.showYesNoMsgBox(text, p.cell.leaveClanWar)

    def handleOpenShopBtnClick(self, *args):
        seekId = CCWCD.data.get('crossClanWarShopSeekId', 10018142)
        uiUtils.findPosById(seekId)

    def handleStartBtnClick(self, *args):
        itemId = CCWCD.data.get('applyItemId', 999)
        if not ICDCD.data.has_key(itemId) and ID.data.get(itemId, {}).get('parentId', 0):
            itemId = ID.data.get(itemId, {}).get('parentId', 0)
        p = BigWorld.player()
        itemFameData = {}
        itemFameData['itemId'] = itemId
        itemFameData['deltaNum'] = 1 - p.inv.countItemInPages(itemId, enableParentCheck=True)
        itemFameData['type'] = 'tianbi'
        itemData = uiUtils.getGfxItemById(itemId)
        if self.currentTabMc.dropDown.selectedIndex < 0:
            p.showGameMsg(GMDD.data.CROSS_CLAN_WAR_APPLY_FAIL_NOT_SELECT_HOST, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.CROSS_CLAN_WAR_START_CONFIM, 'GMDD.data.CROSS_CLAN_WAR_START_CONFIM')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.startCallback, itemFameData=itemFameData, itemData=itemData)

    @ui.checkInventoryLock()
    def startCallback(self):
        itemId = CCWCD.data.get('applyItemId', 999)
        p = BigWorld.player()
        enableDiKou = p.inv.countItemInPages(itemId, enableParentCheck=True) < 1
        if not self.currentTabMc or not self.currentTabMc.dropDown:
            return
        index = int(self.currentTabMc.dropDown.selectedIndex)
        if index >= len(self.hostList):
            return
        p.cell.applyClanWar(self.hostList[index], enableDiKou, p.cipherOfPerson)

    def getServerName(self, hostId):
        if hostId == self.getGlobalHostId():
            return CCWCD.data.get('globalServerName', 'globalServerName')
        return utils.getServerName(hostId)

    def dropDownLabelFunction(self, *args):
        hostId = int(args[3][0].GetNumber())
        return GfxValue(ui.gbk2unicode(self.getServerName(hostId)))

    def handleShowRankBtnClick(self, *args):
        self.uiAdapter.crossClanWarRank.show(utils.getHostId())

    def handleHistoryBtnClick(self, *args):
        gameglobal.rds.ui.crossClanWarHistory.show(uiConst.CROSS_CLAN_WAR_HISTORY_FILTER_TYPE_SELF if self.selectedTab == TAB_CLAN_WAR else uiConst.CROSS_CLAN_WAR_HISTORY_FILTER_TYPE_OTHERS)

    def handleClanInfoBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(2)

    def handleKillEnemyInfoBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(1)

    def handleDeclareWarInfoBtnClick(self, *args):
        self.uiAdapter.clanWar.showRankList(3)

    def handleResultBntClick(self, *args):
        self.uiAdapter.clanWar.showClanWarResult()

    def handleShowResultBtnClick(self, *args):
        self.showClanWarResult = True
        crossClanWarTgtHostId = self.localSelectedHostId
        crossClanWarTgtHostId and BigWorld.player().cell.getClanWarOccupyInfo(crossClanWarTgtHostId)

    def handleIncidentBntClick(self, *args):
        self.uiAdapter.clanWarIncident.show()

    def handleWorldBossClick(self, *args):
        gameglobal.rds.ui.worldBossCard.show()
