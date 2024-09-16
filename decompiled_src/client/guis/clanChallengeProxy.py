#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanChallengeProxy.o
import BigWorld
import math
import gamelog
import gametypes
import const
import events
import utils
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import clan_war_fort_data as CWFD
from data import game_msg_data as GMD
from data import item_data as ID
from data import region_server_config_data as RSCD
from data import clan_war_challenge_config_data as CWCCD
from cdata import game_msg_def_data as GMDD
TAB_IDX_GUILD_CHALLENGE = 0
TAB_IDX_CLAN_CHALLENGE = 1
TAB_IDX_CROSS_CLAN_CHALLENGE = 2
CLAN_STATE_NONE = 0
CLAN_STATE_MINE = 1
CLAN_STATE_ENEMY = 2
CLAN_STATE_ATK_APPLY = 3
CLAN_STATE_MINE_APPLY = 4
CLAN_STATE_ATK = 5
CLAN_STATE_MINE_DEF = 6
CLAN_STATE_DEF_SUCC = 7
CLAN_STAET_ATK_SUCC = 8
TEXT_COLOR_RED = '#FF471C'

class ClanChallengeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanChallengeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tabIdx = TAB_IDX_GUILD_CHALLENGE
        self.reset()

    def reset(self):
        self.selectedFortMc = None
        self.selectedFortId = 0
        self.jumpIdx = None

    def initPanel(self, widget):
        self.widget = ASObject(widget)
        if self.jumpIdx != None:
            self.tabIdx = self.jumpIdx
            self.jumpIdx = None
        else:
            self.tabIdx = TAB_IDX_GUILD_CHALLENGE
        self.initUI()
        if self.tabIdx in (TAB_IDX_CLAN_CHALLENGE, TAB_IDX_CROSS_CLAN_CHALLENGE):
            self.initClanChallenge()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.tab0.addEventListener(events.BUTTON_CLICK, self.handleTab0Click, False, 0, True)
        self.widget.tab1.addEventListener(events.BUTTON_CLICK, self.handleTab1Click, False, 0, True)
        p = BigWorld.player()
        self.widget.tab2.visible = bool(getattr(p, 'clanWarCrossHostId', 0))
        self.widget.tab2.addEventListener(events.BUTTON_CLICK, self.handleTab2Click, False, 0, True)
        self.timerCheck()

    def isInCombatState(self):
        p = BigWorld.player()
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', 0)
        isCombat = const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE <= clanWarChallengeState <= const.CLAN_WAR_CHALLENGE_STAGE_END
        return isCombat

    def initClanChallenge(self):
        for fortId, cfgData in CWFD.data.iteritems():
            if cfgData.get('digongFort'):
                continue
            fortMc = getattr(self.widget, 'fort%d' % fortId)
            fortMc.fortId = fortId
            fortMc.addEventListener(events.BUTTON_CLICK, self.handleFortMcClick, False, 0, True)

        self.widget.memberSettingBtn.addEventListener(events.BUTTON_CLICK, self.handleMemberSettingBtnClick, False, 0, True)
        self.widget.showResultBtn.addEventListener(events.BUTTON_CLICK, self.handleShowResultBtnClick, False, 0, True)
        self.widget.viewRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleViewRewardBtnClick, False, 0, True)
        self.widget.helpIcon.helpKey = CWCCD.data.get('helpKey', 201)
        p = BigWorld.player()
        hasattr(p.cell, 'queryClanWarChallengeBaseInfo') and p.cell.queryClanWarChallengeBaseInfo(p.getClanChallengeHostId())
        p.cell.queryClanWarChallengeAllMemberInfo(p.getClanChallengeHostId())
        p.cell.queryClanWarChallengeAllCombatInfo(p.getClanChallengeHostId())

    def enableMemberSetting(self, fortId = None):
        if fortId == None:
            fortId = self.selectedFortId
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(fortId, [])
        isMember = clanChallengeMemberInfo and p.gbId in clanChallengeMemberInfo[2]
        return bool((p.isClanChallengeCommander(fortId) or p.guild.memberMe.roleId in gametypes.GUILD_ROLE_LEADERS or isMember) and fortId in p.targetChallengeGuild)

    def refreshClanChallenge(self):
        if not self.widget or self.tabIdx not in (TAB_IDX_CLAN_CHALLENGE, TAB_IDX_CROSS_CLAN_CHALLENGE):
            return
        p = BigWorld.player()
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', 0)
        self.widget.memberSettingBtn.visible = const.CLAN_WAR_CHALLENGE_STAGE_END > clanWarChallengeState >= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE
        if self.selectedFortMc:
            fortState, args = self.selectedFortMc.stateData
            self.widget.memberSettingBtn.enabled = self.enableMemberSetting() and fortState != CLAN_STATE_ENEMY
        else:
            self.widget.memberSettingBtn.enabled = self.enableMemberSetting()
        self.widget.showResultBtn.visible = const.CLAN_WAR_CHALLENGE_STAGE_END >= clanWarChallengeState >= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1
        targetChallengeGuild = getattr(p, 'targetChallengeGuild', {})
        if not self.selectedFortId and targetChallengeGuild:
            self.selectedFortId = targetChallengeGuild.keys()[0]
        self.refreshClan()
        self.refreshTipsContent()
        self.refreshStartChallengeBtn()
        self.widget.rules.htmlText = CWCCD.data.get('ruleStageConfig', '')

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.tab0.selected = self.tabIdx == TAB_IDX_GUILD_CHALLENGE
        self.widget.tab1.selected = self.tabIdx == TAB_IDX_CLAN_CHALLENGE
        self.widget.tab2.selected = self.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE
        if self.tabIdx == TAB_IDX_GUILD_CHALLENGE:
            self.widget.gotoAndStop('guildChallenge')
            self.widget.guildChallenge.initChallenge()
        else:
            self.widget.gotoAndStop('clanChallenge')
            self.refreshClanChallenge()

    def isEnterCombat(self):
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, None)
        if not clanChallengeMemberInfo:
            return False
        else:
            isEnterCombat = False
            state = getattr(p, 'clanWarChallengeState', const.CLAN_WAR_CHALLENGE_STAGE_DEFAULT)
            if const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE <= state <= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND5:
                layout = clanChallengeMemberInfo[3]
                roundIdx = max(0, state - const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1)
                if len(layout) > roundIdx and p.gbId in layout[roundIdx]:
                    return True
            return isEnterCombat

    def refreshStartChallengeBtn(self):
        p = BigWorld.player()
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', 0)
        self.widget.startChallengeBtn.addEventListener(events.BUTTON_CLICK, self.handleStartChallengeBtnClick, False, 0, True)
        self.widget.startChallengeBtn.enabled = True
        if clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            self.widget.startChallengeBtn.enabled = False
        elif clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_PREPARE:
            targetChallengeGuild = getattr(p, 'targetChallengeGuild', {})
            if not targetChallengeGuild.has_key(self.selectedFortId):
                self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_APPLY_BTN_LABEL_APPLY
                self.widget.startChallengeBtn.data = 'applyChallenge'
            else:
                self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_APPLY_BTN_LABEL_CANCEL
                self.widget.startChallengeBtn.data = 'cancelChallenge'
            self.widget.startChallengeBtn.enabled = p.guild.memberMe.roleId in gametypes.GUILD_ROLE_LEADERS
        elif clanWarChallengeState in (const.CLAN_WAR_CHALLENGE_STAGE_PREPARE, const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE):
            self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_APPLY_BTN_LABEL_SETTING
            self.widget.startChallengeBtn.data = 'setChallenge'
            self.widget.startChallengeBtn.enabled = self.enableMemberSetting()
        elif clanWarChallengeState == const.CLAN_WAR_CHALLENGE_STAGE_END:
            self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_APPLY_BTN_LABEL_END
            self.widget.startChallengeBtn.enabled = False
        else:
            isEnter = self.isEnterCombat()
            isOb = not isEnter
            if isEnter:
                self.widget.startChallengeBtn.data = 'enterChallenge'
                self.setEnterChallengeLabel()
            elif isOb:
                self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_APPLY_BTN_LABEL_OB
                self.widget.startChallengeBtn.data = 'obChallenge'
            self.widget.startChallengeBtn.enabled = clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_END
        self.widget.memberSettingBtn.visible = const.CLAN_WAR_CHALLENGE_STAGE_END > clanWarChallengeState >= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE
        if self.selectedFortMc:
            fortState, args = self.selectedFortMc.stateData
            self.widget.memberSettingBtn.enabled = self.enableMemberSetting() and fortState != CLAN_STATE_ENEMY
        else:
            self.widget.memberSettingBtn.enabled = self.enableMemberSetting()

    def setEnterChallengeLabel(self):
        p = BigWorld.player()
        clanChallengeCombatResult = getattr(p, 'clanChallengeCombatResult', {}).get(self.selectedFortId, [])
        if not clanChallengeCombatResult:
            self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_WAR_CHALLENGE_BTN_LABEL_STARTED
        else:
            clanWarChallengeState = getattr(p, 'clanWarChallengeState', None)
            roundIdx = clanWarChallengeState - const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1
            tStart = clanChallengeCombatResult[-1][roundIdx] if len(clanChallengeCombatResult[-1]) > roundIdx else 0
            combatReadyTime = CWCCD.data.get('combatReadyTime', 180)
            if utils.getNow() < tStart + combatReadyTime:
                self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_WAR_CHALLENGE_BTN_LABEL_ENTER % (tStart + combatReadyTime - utils.getNow())
            else:
                self.widget.startChallengeBtn.label = gameStrings.CROSS_CLAN_WAR_CHALLENGE_BTN_LABEL_STARTED

    def timerCheck(self):
        if not self.widget or not self.widget.startChallengeBtn:
            return
        p = BigWorld.player()
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', 0)
        if self.widget.startChallengeBtn.data == 'enterChallenge' and const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1 <= clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_END:
            self.setEnterChallengeLabel()
        BigWorld.callback(1, self.timerCheck)

    def enterChallenge(self, *args):
        gamelog.info('jbx:enterChallenge')
        BigWorld.player().cell.enterClanWarChallenge(BigWorld.player().getClanChallengeHostId())

    def obChallenge(self, *args):
        gamelog.info('jbx:obChallenge')
        if not self.selectedFortId:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_CHALLENGE_SELECT_FORT, ())
            return
        BigWorld.player().cell.startObserveClanWarChallenge(self.selectedFortId, BigWorld.player().getClanChallengeHostId())

    def setChallenge(self, *args):
        gamelog.info('jbx:setChallenge')
        self.handleMemberSettingBtnClick()

    def cancelChallenge(self, *args):
        gamelog.info('jbx:cancelChallenge')
        if not self.selectedFortId:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_CHALLENGE_SELECT_FORT, ())
            return
        p = BigWorld.player()
        ownGuildName = p.clanWar.fort.get(self.selectedFortId).ownerGuildName
        fortName = CWFD.data.get(self.selectedFortId, {}).get('showName', '')
        msg = GMD.data.get(GMDD.data.CANCEL_CHALLENGE_FONFIRM, {}).get('text', 'GMDD.data.CANCEL_CHALLENGE_FONFIRM %s %s') % (ownGuildName, fortName)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.confirmCallback)

    def confirmCallback(self):
        gamelog.info('jbx:cancelApplyClanWarChallenge', self.selectedFortId)
        BigWorld.player().cell.cancelApplyClanWarChallenge(self.selectedFortId)

    def testCancelChallenge(self):
        p = BigWorld.player()
        clanWarChallengeBaseInfo = getattr(p, 'clanWarChallengeBaseInfo', {})
        info = clanWarChallengeBaseInfo[self.selectedFortId]
        for index, applyInfo in enumerate(info[-1]):
            if applyInfo[0] == p.guild.nuid:
                info[-1].pop(index)
                break

        p.onCancelApplyClanWarChallenge(info)

    def testApplyClanWarChallenge(self):
        p = BigWorld.player()
        clanWarChallengeBaseInfo = getattr(p, 'clanWarChallengeBaseInfo', {})
        info = clanWarChallengeBaseInfo[self.selectedFortId]
        info[-1].append((p.guild.nuid,
         p.guild.name,
         1,
         500))
        p.onApplyClanWarChallenge(info)

    def applyChallenge(self, *args):
        p = BigWorld.player()
        roleId = p.guild.memberMe.roleId
        if self.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            p.showGameMsg(GMDD.data.GUILD_CHALLENGE_CROSS_APPLY_ERROR, ())
            return
        if roleId not in gametypes.GUILD_ROLE_LEADERS:
            p.showGameMsg(GMDD.data.GUILD_CHALLENGE_NEED_LEADER_EX, ())
            return
        if not self.selectedFortId:
            p.showGameMsg(GMDD.data.GUILD_CHALLENGE_SELECT_FORT, ())
            return
        if len(getattr(p, 'targetChallengeGuild', {})) >= 2:
            p.showGameMsg(GMDD.data.GUILD_CHALLENGE_APPLY_OVER_TIMES, ())
            return
        itemId = CWCCD.data.get('applyItemId', 999)
        p = BigWorld.player()
        itemData = uiUtils.getGfxItemById(itemId)
        ownCnt = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if not ownCnt:
            itemData['count'] = '%s/1' % uiUtils.toHtml('0', TEXT_COLOR_RED)
        else:
            itemData['count'] = '%d/1' % min(1, ownCnt)
        ownGuildName = p.clanWar.fort.get(self.selectedFortId).ownerGuildName
        fortName = CWFD.data.get(self.selectedFortId, {}).get('showName', '')
        confirmMsg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_CONFIRM, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_CONFIRM %s %s') % (ownGuildName, fortName)
        checkText = gameStrings.CLAN_CHALLENGE_APPLY_CHECK_LABEL % ID.data.get(itemId, {}).get('name', '')
        self.uiAdapter.messageBox.showItemCheckMsgBox(confirmMsg, self.applyChallengeConfirmCallback, itemData=itemData, checkText=checkText)

    def testMsgBox(self):
        itemId = CWCCD.data.get('applyItemId', 999)
        p = BigWorld.player()
        itemData = uiUtils.getGfxItemById(itemId)
        ownCnt = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if not ownCnt:
            itemData['count'] = '%s/1' % uiUtils.toHtml('0', TEXT_COLOR_RED)
        else:
            itemData['count'] = '%d/1' % min(1, ownCnt)
        ownGuildName = 'SSSSS'
        fortName = CWFD.data.get(self.selectedFortId, {}).get('showName', '')
        confirmMsg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_CONFIRM, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_CONFIRM %s %s') % (ownGuildName, fortName)
        checkText = gameStrings.CLAN_CHALLENGE_APPLY_CHECK_LABEL % ID.data.get(itemId, {}).get('name', '')
        self.uiAdapter.messageBox.showItemCheckMsgBox(confirmMsg, self.applyChallengeConfirmCallback, itemData=itemData, checkText=checkText)

    @ui.checkInventoryLock()
    def applyChallengeConfirmCallback(self):
        p = BigWorld.player()
        itemId = CWCCD.data.get('applyItemId', 999)
        itemCnt = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if self.uiAdapter.messageBox.checkBoxSelected:
            if not itemCnt:
                p.showGameMsg(GMDD.data.CLAN_CHALLENGE_APPLY_ITEM_NEED, ())
                return
        else:
            itemCnt = 0
        gamelog.info('jbx:applyClanWarChallenge', self.selectedFortId, bool(itemCnt))
        p.cell.applyClanWarChallenge(self.selectedFortId, bool(itemCnt), p.cipherOfPerson)

    def handleStartChallengeBtnClick(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.data and hasattr(self, e.currentTarget.data) and getattr(self, e.currentTarget.data)()

    def refreshTipsContent(self):
        p = BigWorld.player()
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', 0)
        targetChallengeGuild = getattr(p, 'targetChallengeGuild', {})
        guildeNameList = set(targetChallengeGuild.values())
        if clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_APPLY_TIME', gameStrings.CLAN_CHALLENGE_APPLY_TIME)
        elif clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_PREPARE:
            if not guildeNameList:
                self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_APPLY_TIME', gameStrings.CLAN_CHALLENGE_APPLY_TIME)
            else:
                self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_APPLY_WAIT', gameStrings.CLAN_CHALLENGE_APPLY_WAIT) % ','.join(guildeNameList)
        elif clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_PREPARE:
            self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_PREPARE', gameStrings.CLAN_CHALLENGE_PREPARE)
        elif clanWarChallengeState < const.CLAN_WAR_CHALLENGE_STAGE_END:
            self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_COMBAT', 'CLAN_CHALLENGE_COMBAT')
        else:
            self.widget.tipsContent.text = CWCCD.data.get('CLAN_CHALLENGE_END', 'CLAN_CHALLENGE_END')
        self.widget.tipsIcon.x = self.widget.tipsContent.x - self.widget.tipsContent.textWidth / 2 + 230

    def testApply(self):
        import random
        p = BigWorld.player()
        p.clanWarChallengeState = const.CLAN_WAR_CHALLENGE_STAGE_APPLY
        clanWarChallengeBaseInfo = []
        for fortId, cfgData in CWFD.data.iteritems():
            if cfgData.get('digongFort'):
                continue
            ownerGuildNUID = p.guild.nuid if fortId % 3 == 0 else 1
            ownerGuildName = p.guild.name if fortId % 3 == 0 else str(fortId)
            ownerGuildFlag = ''
            ownerClanNUID = fortId
            applyList = []
            if fortId % 2:
                for i in xrange(5):
                    applyList.append((i,
                     'guild%d' % i,
                     i % 2,
                     random.randint(1, 100)))

            clanWarChallengeBaseInfo.append((fortId,
             ownerGuildNUID,
             ownerGuildName,
             ownerGuildFlag,
             ownerClanNUID,
             applyList))

        p.onQueryClanWarChallengeBaseInfo(clanWarChallengeBaseInfo)

    def testAtk(self):
        p = BigWorld.player()
        p.clanWarChallengeState = const.CLAN_WAR_CHALLENGE_STAGE_PREPARE
        clanWarChallengeBaseInfo = []
        for fortId, cfgData in CWFD.data.iteritems():
            if cfgData.get('digongFort'):
                continue
            ownerGuildNUID = p.guild.nuid if fortId % 3 == 0 else 1
            ownerGuildName = p.guild.name if fortId % 3 == 0 else str(fortId)
            ownerGuildFlag = ''
            ownerClanNUID = fortId
            clanWarChallengeBaseInfo.append((fortId,
             ownerGuildNUID,
             ownerGuildName,
             ownerGuildFlag,
             ownerClanNUID,
             fortId + 1,
             'challenge:%d' % fortId if fortId % 2 else ''))

        p.onQueryClanWarChallengeBaseInfo(clanWarChallengeBaseInfo)

    def getOwnerGuildName(self, name, hostId):
        if hostId and hostId != BigWorld.player().getOriginHostId():
            name = name + '-' + RSCD.data.get(hostId, {}).get('serverName', '')
        return name

    def refreshClan(self):
        p = BigWorld.player()
        clanWarChallengeBaseInfo = getattr(p, 'clanWarChallengeBaseInfo', {})
        clanWarChallengeState = getattr(p, 'clanWarChallengeState', const.CLAN_WAR_CHALLENGE_STAGE_DEFAULT)
        clanChallengeCombatResult = getattr(p, 'clanChallengeCombatResult', {})
        for fortId, cfgData in CWFD.data.iteritems():
            if cfgData.get('digongFort'):
                continue
            fortMc = getattr(self.widget, 'fort%d' % fortId)
            if fortId == self.selectedFortId:
                if self.selectedFortMc:
                    self.selectedFortMc.selected = False
                self.selectedFortMc = fortMc
                self.selectedFortMc.selected = True
            else:
                fortMc.selected = False
            fortVal = clanWarChallengeBaseInfo.get(fortId, None)
            args = []
            if not fortVal or len(fortVal) < 2 or not fortVal[2]:
                fortState = CLAN_STATE_NONE
            elif clanWarChallengeState == const.CLAN_WAR_CHALLENGE_STAGE_END and clanChallengeCombatResult.has_key(fortId):
                oldOwernHostId = fortVal[1]
                ownerGuildNUID = clanChallengeCombatResult[fortId][1]
                challengeGuildNuid = clanChallengeCombatResult[fortId][5]
                ownerWinCnt = clanChallengeCombatResult[fortId][9].count(ownerGuildNUID)
                challengeWinCnt = clanChallengeCombatResult[fortId][9].count(challengeGuildNuid)
                if challengeWinCnt > ownerWinCnt:
                    fortState = CLAN_STAET_ATK_SUCC
                    ownerGuildName = fortVal[6]
                else:
                    fortState = CLAN_STATE_DEF_SUCC
                    ownerGuildName = self.getOwnerGuildName(fortVal[3], oldOwernHostId)
                args = [ownerGuildName]
            elif clanWarChallengeState == const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
                fortId, hostId, ownerGuildNUID, ownerGuildName, ownerGuildFlag, ownerClanNUID, applyList = fortVal
                ownerGuildName = self.getOwnerGuildName(ownerGuildName, hostId)
                if applyList:
                    if ownerGuildNUID == p.guild.nuid:
                        fortState = CLAN_STATE_MINE_APPLY
                    else:
                        fortState = CLAN_STATE_ATK_APPLY
                    args = [ownerGuildName, applyList]
                elif ownerGuildNUID == p.guild.nuid:
                    fortState = CLAN_STATE_MINE
                    args = [ownerGuildName]
                else:
                    fortState = CLAN_STATE_ENEMY
                    args = [ownerGuildName]
            else:
                fortId, hostId, ownerGuildNUID, ownerGuildName, ownerGuildFlag, ownerClanNUID, challengeGuildName = fortVal
                ownerGuildName = self.getOwnerGuildName(ownerGuildName, hostId)
                if challengeGuildName:
                    if ownerGuildNUID == p.guild.nuid:
                        fortState = CLAN_STATE_MINE_DEF
                        args = [ownerGuildName, challengeGuildName]
                    else:
                        fortState = CLAN_STATE_ATK
                        args = [challengeGuildName, ownerGuildName]
                elif ownerGuildNUID == p.guild.nuid:
                    fortState = CLAN_STATE_MINE
                    args = [ownerGuildName]
                else:
                    fortState = CLAN_STATE_ENEMY
                    args = [ownerGuildName]
            self.refreshFortMc(fortId, fortMc, fortState, args)

    def refreshFortMc(self, fortId, fortMc, fortState, args):
        TipManager.removeTip(fortMc)
        fortName = CWFD.data.get(fortId, {}).get('showName', '')
        TipManager.addTip(fortMc, fortName)
        fortMc.stateData = (fortState, args)
        fortMc.msgId = 0
        p = BigWorld.player()
        if fortState == CLAN_STATE_NONE:
            fortMc.guild.icon.gotoAndStop('no')
            fortMc.guild.atkName.textField.text = ''
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = ''
            fortMc.canSelected = False
            fortMc.msgId = GMDD.data.CLAN_FORT_CAN_NOT_CLICK_NO_OWNER
        elif fortState == CLAN_STATE_MINE_DEF:
            fortMc.guild.icon.gotoAndStop('my')
            fortMc.guild.atkName.textField.text = args[1]
            fortMc.guild.atkIcon.visible = True
            fortMc.guild.defIcon.visible = True
            fortMc.guild.defName.textField.text = args[0]
            fortMc.canSelected = True
        elif fortState == CLAN_STATE_MINE:
            fortMc.guild.icon.gotoAndStop('my')
            fortMc.guild.atkName.textField.text = ''
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = args[0]
            fortMc.canSelected = False
            fortMc.msgId = GMDD.data.CLAN_FORT_CAN_NOT_CLICK_SELF_FORT
        elif fortState == CLAN_STAET_ATK_SUCC:
            if p.guildName == args[0]:
                fortMc.guild.icon.gotoAndStop('my' if p.guildName == args[0] else 'other')
            fortMc.guild.atkName.textField.text = args[0]
            fortMc.guild.atkIcon.visible = True
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = ''
        elif fortState == CLAN_STATE_DEF_SUCC:
            if p.guildName == args[0]:
                fortMc.guild.icon.gotoAndStop('my' if p.guildName == args[0] else 'other')
            fortMc.guild.atkName.textField.text = ''
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = True
            fortMc.guild.defName.textField.text = args[0]
        elif fortState == CLAN_STATE_ENEMY:
            fortMc.guild.icon.gotoAndStop('other')
            fortMc.guild.atkName.textField.text = ''
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = args[0]
            fortMc.canSelected = getattr(BigWorld.player(), 'clanWarChallengeState', 0) == const.CLAN_WAR_CHALLENGE_STAGE_APPLY
        elif fortState == CLAN_STATE_ATK_APPLY:
            fortMc.guild.icon.gotoAndStop('other')
            fortMc.guild.atkName.textField.text = gameStrings.CLAN_CHALLENGE_APPLY
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = args[0]
            fortMc.canSelected = True
            TipManager.addTip(fortMc, self.getFortApplyTips(fortName, args[1]))
        elif fortState == CLAN_STATE_MINE_APPLY:
            fortMc.guild.icon.gotoAndStop('my')
            fortMc.guild.atkName.textField.text = gameStrings.CLAN_CHALLENGE_APPLY
            fortMc.guild.atkIcon.visible = False
            fortMc.guild.defIcon.visible = False
            fortMc.guild.defName.textField.text = args[0]
            fortMc.canSelected = False
            TipManager.addTip(fortMc, self.getFortApplyTips(fortName, args[1]))
            fortMc.msgId = GMDD.data.CLAN_FORT_CAN_NOT_CLICK_SELF_FORT
        elif fortState == CLAN_STATE_ATK:
            fortMc.guild.icon.gotoAndStop('other')
            fortMc.guild.atkName.textField.text = args[0]
            fortMc.guild.atkIcon.visible = True
            fortMc.guild.defIcon.visible = True
            fortMc.guild.defName.textField.text = args[1]
            fortMc.canSelected = True
        if not fortMc.canSelected:
            fortMc.selected = False
            if fortMc == self.selectedFortMc:
                self.selectedFortId = 0
                self.selectedFortMc = None
        stage = getattr(p, 'clanWarChallengeState', 0)
        if const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1 <= stage <= const.CLAN_WAR_CHALLENGE_STAGE_END and fortState != CLAN_STATE_NONE:
            fortMc.canSelected = True
        ASUtils.autoSizeWithFont(fortMc.guild.defName.textField, 14, fortMc.guild.defName.textField.width, 9)
        ASUtils.autoSizeWithFont(fortMc.guild.atkName.textField, 14, fortMc.guild.atkName.textField.width, 9)

    def getApplyTips(self, applyInfo):
        guildName = applyInfo[1]
        nuidA, nameA, prestigeA, isReApplyA, isEnemyA, isUseItemA, tWhenA = applyInfo
        percent = BigWorld.player().getWeightedPrestige(applyInfo)
        percent = int(math.ceil(abs(percent - 1.0) * 100))
        if isEnemyA and not isReApplyA:
            return guildName + gameStrings.CLAN_CHALLENGE_ENEMY % percent
        if isEnemyA and isReApplyA:
            return guildName + gameStrings.CLAN_CHALLENGE_ENEMY_SECOND % percent
        if not isEnemyA and isReApplyA:
            return guildName + gameStrings.CLAN_CHALLENGE_SECOND % percent
        return guildName

    def getFortApplyTips(self, fortName, applyList):
        nameList = [ self.getApplyTips(applyInfo) for applyInfo in applyList ]
        nameStr = '\n'.join(nameList)
        return gameStrings.CLAN_CHALLENGE_APPLY_LIST % fortName + nameStr

    @ui.callFilter(1)
    def handleFortMcClick(self, *args):
        e = ASObject(args[3][0])
        fortId = int(e.currentTarget.fortId)
        if not e.currentTarget.canSelected:
            if e.currentTarget.msgId:
                msgId = int(e.currentTarget.msgId)
                BigWorld.player().showGameMsg(msgId, ())
            return
        e.currentTarget.selected = True
        if fortId != self.selectedFortId:
            if self.selectedFortMc:
                self.selectedFortMc.selected = False
            self.selectedFortMc = e.currentTarget
            self.selectedFortMc.selected = True
            self.selectedFortId = fortId
        self.refreshStartChallengeBtn()

    def handleMemberSettingBtnClick(self, *args):
        p = BigWorld.player()
        roleId = p.guild.memberMe.roleId
        if roleId not in gametypes.GUILD_ROLE_LEADERS and not p.isMemberInClanWarChallenge(p.gbId) and not p.isClanChallengeCommander(self.selectedFortId):
            p.showGameMsg(GMDD.data.CLAN_CHALLENGE_NOT_IN_COMBAT, ())
            return
        if not self.selectedFortId:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_CHALLENGE_SELECT_FORT, ())
            return
        self.uiAdapter.clanChallengeSet.show(self.selectedFortId)

    def handleShowResultBtnClick(self, *args):
        p = BigWorld.player()
        if self.selectedFortId <= 0:
            p.showGameMsg(GMDD.data.CLAN_CHALLENGE_NOT_SELECT_FORT, ())
            return
        baseInfo = p.clanWarChallengeBaseInfo.get(self.selectedFortId, {})
        if not baseInfo or not baseInfo[5]:
            p.showGameMsg(GMDD.data.CWC_QUERY_COMBAT_FAIL_NO_DATA, ())
            return
        self.uiAdapter.clanChallengeResult.showResult = utils.getNow()
        p.cell.queryClanWarChallengeCombatInfo(self.selectedFortId, BigWorld.player().getClanChallengeHostId())

    def handleViewRewardBtnClick(self, *args):
        self.uiAdapter.generalReward.show(CWCCD.data.get('generalRewardId', 1))

    def getGuilcChallengeWidget(self):
        if self.widget and self.widget.guildChallenge:
            return self.widget.guildChallenge
        else:
            return None

    def handleTab0Click(self, *args):
        if self.tabIdx == TAB_IDX_GUILD_CHALLENGE:
            return
        self.tabIdx = TAB_IDX_GUILD_CHALLENGE
        self.refreshInfo()

    @ui.callFilter(0.6)
    def jumpClanChallengeTab(self, tabIdx):
        if self.tabIdx == tabIdx:
            return
        self.tabIdx = tabIdx
        self.widget.gotoAndStop('clanChallenge')
        self.initClanChallenge()
        self.refreshInfo()

    def handleTab1Click(self, *args):
        if self.tabIdx == TAB_IDX_CLAN_CHALLENGE:
            return
        self.jumpClanChallengeTab(TAB_IDX_CLAN_CHALLENGE)

    def handleTab2Click(self, *args):
        if self.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return
        self.jumpClanChallengeTab(TAB_IDX_CROSS_CLAN_CHALLENGE)
