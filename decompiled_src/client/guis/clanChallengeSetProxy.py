#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanChallengeSetProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import const
import gamelog
import uiConst
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.clanChallengeProxy import TAB_IDX_CROSS_CLAN_CHALLENGE
from guis import ui
from callbackHelper import Functor
from gamestrings import gameStrings
import events
from guis import uiUtils
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import clan_war_fort_data as CWFD
from data import clan_war_challenge_config_data as CWCCD
from data import game_msg_data as GMD
ROUND_CNT = 5

class ClanChallengeSetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanChallengeSetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_CHALLENGE_SET, self.hide)

    def reset(self):
        self.fortIdList = []
        self.selectedMemberPos = None
        self.lastSelectedMemberMc = None
        self.isFirst = True
        self.selectedIdx = -1
        self.chooseMemberPos = None
        self.isSetCommander = False
        self.searchKey = ''
        self.selectedFortId = 0
        self.oneVsOneGbIdSet = set()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_CHALLENGE_SET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_CHALLENGE_SET)

    def show(self, selectedFortId = 0):
        if not self.widget:
            p = BigWorld.player()
            if selectedFortId <= 0 and getattr(p, 'targetChallengeGuild', {}).keys():
                selectedFortId = getattr(p, 'targetChallengeGuild', {}).keys()[0]
            self.selectedFortId = selectedFortId
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_CHALLENGE_SET)
            if self.uiAdapter.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE and getattr(p, 'clanWarCrossHostId', 0) and p.clanWarCrossHostId != self.uiAdapter.crossClanWar.getGlobalHostId():
                p.cell.queryClanWarChallengeAllMemberInfo(p.clanWarCrossHostId)
                BigWorld.callback(0.6, Functor(p.cell.queryClanWarChallengeAllMemberInfo, p.getOriginHostId()))
            else:
                p.cell.queryClanWarChallengeAllMemberInfo(p.getOriginHostId())
                BigWorld.callback(0.6, Functor(p.cell.queryClanWarChallengeAllMemberInfo, p.clanWarCrossHostId))

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteBtnClick, False, 0, True)
        self.widget.memberList.itemRenderer = 'ClanChallengeSet_ItemRender'
        self.widget.memberList.labelFunction = self.memberListLabelFunction
        self.widget.inviteList.visible = False
        self.widget.inviteList.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteCloseBtnClick, False, 0, True)
        self.widget.inviteList.inputText.addEventListener(events.EVENT_CHANGE, self.handleInputTextChange, False, 0, True)
        self.widget.inviteList.list.itemRenderer = 'ClanChallengeSet_InviteItemRender'
        self.widget.inviteList.list.labelFunction = self.inviteItemLabelFunction
        self.widget.changeBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeBtnClick, False, 0, True)
        self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.handleDropDownIndexChange, False, 0, True)
        self.widget.inviteList.searchBtn.addEventListener(events.BUTTON_CLICK, self.handleSearchBtnClick, False, 0, True)
        roundTimeStrs = CWCCD.data.get('roundTimeStrs', [('', '')] * 5)
        for i in xrange(ROUND_CNT):
            txtTime = self.widget.getChildByName('txtTime%d' % i)
            txtRount = self.widget.getChildByName('txtRound%d' % i)
            txtRount.text = roundTimeStrs[i][0]
            txtTime.text = roundTimeStrs[i][1]

    def handleSearchBtnClick(self, *args):
        self.searchKey = self.widget.inviteList.inputText.text
        self.widget.inviteList.list.dataArray = self.getInviteMemberList()
        self.searchKey = None

    def getMemberGbIdByPos(self, fortId, round, roundIdx):
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(fortId, [])
        if len(clanChallengeMemberInfo) > 3 and len(clanChallengeMemberInfo[3]) > round and clanChallengeMemberInfo[3][round][roundIdx]:
            return clanChallengeMemberInfo[3][round][roundIdx]
        else:
            return 0

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.oneVsOneGbIdSet.clear()
        self.widget.dropDown.defaultText = gameStrings.CROSS_CLAN_CHALLENGE_DROP_DOWN_DEFAULT
        self.widget.dropDown.labelFunction = self.dropDownLabelFunction
        self.widget.dropDown.dropdown = 'M12_DefaultScrollingList'
        self.widget.dropDown.itemRenderer = 'M12_DefaultListItemRenderer'
        targetChallengeGuild = getattr(p, 'targetChallengeGuild', {})
        self.fortIdList = [ fortId for fortId in targetChallengeGuild.keys() if self.uiAdapter.clanChallenge.enableMemberSetting(fortId) ]
        ASUtils.setDropdownMenuData(self.widget.dropDown, self.fortIdList)
        if self.selectedFortId in self.fortIdList:
            self.selectedIdx = self.fortIdList.index(self.selectedFortId)
        if self.selectedIdx < 0 and self.fortIdList:
            self.selectedIdx = 0
        self.widget.dropDown.selectedIndex = self.selectedIdx
        if self.widget.dropDown.selectedIndex < 0 or self.widget.dropDown.selectedIndex >= len(self.fortIdList):
            self.widget.txtGuildName.text = ''
            self.widget.txtCommandName.text = ''
            for i in xrange(uiConst.ROUND_MAX_COUNT):
                roundMc = getattr(self.widget, 'round%d' % i)
                for childrenIdx in xrange(roundMc.numChildren):
                    mc = roundMc.getChildAt(childrenIdx)
                    mc.visible = False

            self.widget.changeBtn.enabled = False
        else:
            fortId = self.fortIdList[self.widget.dropDown.selectedIndex]
            clanWarChallengeBaseInfo = getattr(p, 'clanWarChallengeBaseInfo', {}).get(fortId, [''] * 3)
            self.widget.txtGuildName.text = clanWarChallengeBaseInfo[3] if clanWarChallengeBaseInfo[3] != p.guild.name else clanWarChallengeBaseInfo[6]
            clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(fortId, [])
            commandGbId = clanChallengeMemberInfo[1] if clanChallengeMemberInfo else 0
            self.widget.txtCommandName.text = p.guild.member[commandGbId].role if p.guild.member.has_key(commandGbId) else ''
            self.widget.changeBtn.enabled = p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER or commandGbId == p.gbId
            for i in xrange(uiConst.ROUND_MAX_COUNT):
                roundMc = getattr(self.widget, 'round%d' % i)
                for j in xrange(uiConst.ROUND_MEMBER_MAX_CNT):
                    memberMc = getattr(roundMc, 'player%d' % j)
                    if not memberMc:
                        break
                    memberMc.visible = True
                    if len(clanChallengeMemberInfo) > 3 and len(clanChallengeMemberInfo[3]) > i and j < len(clanChallengeMemberInfo[3][i]) and clanChallengeMemberInfo[3][i][j]:
                        memberMc.gotoAndStop('player')
                        memberGbId = clanChallengeMemberInfo[3][i][j]
                        guildMember = p.guild.member[memberGbId]
                        if uiConst.ROUND_COUNT_LIST[i] == 1:
                            self.oneVsOneGbIdSet.add(memberGbId)
                        memberMc.player.removeBtn.visible = p.isClanChallengeCommander(self.selectedFortId) and getattr(p, 'clanWarChallengeState', 0) == const.CLAN_WAR_CHALLENGE_STAGE_PREPARE
                        memberMc.player.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
                        memberMc.player.removeBtn.data = (i, j)
                        memberMc.player.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(guildMember.school))
                        memberMc.player.btn1.label = guildMember.role
                        memberMc.player.btn1.addEventListener(events.BUTTON_CLICK, self.handleSelectedBtnClick, False, 0, True)
                        memberMc.player.btn1.data = (i, j)
                        p.memberMc = memberMc
                    else:
                        memberMc.gotoAndStop('none')
                        memberMc.selectedBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectedBtnClick, False, 0, True)
                        memberMc.selectedBtn.data = (i, j)

        self.widget.inviteBtn.enabled = p.isClanChallengeCommander(self.selectedFortId) and getattr(p, 'clanWarChallengeState', 0) == const.CLAN_WAR_CHALLENGE_STAGE_PREPARE
        self.refreshBattleMemberInfo()
        self.refreshInviteList()

    def testMemberSetting(self):
        fortIdList = [23, 13]
        memberData = []
        p = BigWorld.player()
        roundCountList = [5,
         3,
         1,
         3,
         5]
        gbIdList = p.guild.member.keys()
        p.targetChallengeGuild = {}
        p.targetChallengeGuild[23] = 'fort23'
        p.targetChallengeGuild[13] = 'fort13'
        for fortId in fortIdList:
            memberList = []
            memberData.append((fortId,
             p.gbId,
             set(gbIdList),
             memberList))
            for memberCnt in roundCountList:
                roundList = []
                memberList.append(roundList)
                for memberIdx in xrange(memberCnt):
                    if memberIdx % 2:
                        roundList.append(0)
                    else:
                        roundList.append(gbIdList[memberIdx % 2])

        p.onQueryClanWarChallengeMemberInfo(memberData)

    def handleSelectedBtnClick(self, *args):
        e = ASObject(args[3][0])
        if self.lastSelectedMemberMc:
            if self.lastSelectedMemberMc.data[0] == e.currentTarget.data[0] and self.lastSelectedMemberMc.data[1] == e.currentTarget.data[1]:
                return
            self.lastSelectedMemberMc.selected = False
        self.lastSelectedMemberMc = e.currentTarget
        self.lastSelectedMemberMc.selected = True
        self.selectedMemberPos = self.lastSelectedMemberMc.data
        self.widget.inviteList.visible = False
        self.refreshBattleMemberInfo()

    def handleRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        round, roundIdx = e.currentTarget.data[0], e.currentTarget.data[1]
        memberGbId = self.getMemberGbIdByPos(self.selectedFortId, round, roundIdx)
        memberName = p.guild.member.get(memberGbId).role
        msg = GMD.data.get(GMDD.data.REMOVE_ROUND_MEMBER_CONFIRM, {}).get('text', 'GMDD.data.REMOVE_ROUND_MEMBER_CONFIRM %s') % memberName
        gamelog.info('jbx:setClanWarChallengeLayout', self.selectedFortId, p.guild.nuid, 0, round, roundIdx)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.setClanWarChallengeLayout, self.selectedFortId, 0, round, roundIdx, BigWorld.player().getClanChallengeHostId()))

    def getSelectedPosMemberGbId(self):
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {})
        if clanChallengeMemberInfo.has_key(self.selectedFortId) and self.selectedMemberPos:
            info = clanChallengeMemberInfo[self.selectedFortId]
            if info:
                return info[3][self.selectedMemberPos[0]][self.selectedMemberPos[1]]
        return 0

    def getBattleMemberList(self):
        memberList = []
        p = BigWorld.player()
        selectedMemberGbId = self.getSelectedPosMemberGbId()
        if p.clanChallengeMemberInfo.has_key(self.selectedFortId):
            for gbId in p.clanChallengeMemberInfo[self.selectedFortId][2]:
                if gbId == selectedMemberGbId:
                    continue
                guildMember = p.guild.member[gbId]
                memberInfo = {}
                memberInfo['schoolId'] = guildMember.school
                memberInfo['name'] = guildMember.role
                memberInfo['gbId'] = gbId
                memberList.append(memberInfo)

        return memberList

    def refreshBattleMemberInfo(self):
        if not self.widget:
            return
        self.widget.memberList.dataArray = self.getBattleMemberList()

    def handleChangeBtnClick(self, *args):
        self.isSetCommander = True
        self.widget.memberList.False = True
        self.widget.inviteList.visible = True
        self.widget.inviteList.list.dataArray = self.getInviteMemberList()

    def dropDownLabelFunction(self, *args):
        fortId = int(args[3][0].GetNumber())
        return GfxValue(ui.gbk2unicode(CWFD.data.get(fortId, {}).get('showName', '')))

    def onDownloadPhoto(self, status, callbackArgs):
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            labelFunction, itemData, itemMc = callbackArgs
            if self.widget and itemMc.state:
                labelFunction(itemMc, itemData)

    def inviteItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.doInviteItemLabelFunction(itemData, itemMc)

    def doInviteItemLabelFunction(self, itemData, itemMc):
        headIcon = itemData.headIcon
        schoolId = int(itemData.schoolId)
        sex = int(itemData.sex)
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.schoolId))
        p = BigWorld.player()
        itemMc.headIcon.fitSize = True
        if uiUtils.isDownloadImage(headIcon):
            if p.isDownloadNOSFileCompleted(headIcon):
                itemMc.headIcon.loadImage('../' + const.IMAGES_DOWNLOAD_DIR + '/' + headIcon + '.dds')
            else:
                itemMc.headIcon.loadImage('headIcon/%s.dds' % str(schoolId * 10 + sex))
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, headIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (self.doInviteItemLabelFunction, itemData, itemMc))
        else:
            itemMc.headIcon.loadImage('headIcon/%s.dds' % str(schoolId * 10 + sex))
        itemMc.txtName.text = itemData.name
        itemMc.txtPoint.text = itemData.txtPoint
        itemMc.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteMemberBtnClick, False, 0, True)
        itemMc.inviteBtn.data = itemData.gbId
        itemMc.inviteBtn.label = gameStrings.CROSS_CLAN_CHALLENGE_INVITE if not self.isSetCommander else gameStrings.CROSS_CLAN_CHALLENGE_SET_COMMAND

    def handleInviteMemberBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId = int(e.currentTarget.data)
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, [])
        memberName = p.guild.member[gbId].role
        if self.isSetCommander:
            self.isSetCommander = False
            self.widget.inviteList.visible = False
            gamelog.info('jbx:setClanWarChallengeCommander', clanChallengeMemberInfo[0], p.guild.nuid, gbId)
            msg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_CHANGE_COMMADER, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_CHANGE_COMMADER %s') % p.guild.member[gbId].role
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.setClanWarChallengeCommander, clanChallengeMemberInfo[0], gbId, memberName, BigWorld.player().getClanChallengeHostId()))
        else:
            gamelog.info('jbx:addClanWarChallengeMember', clanChallengeMemberInfo[0], gbId, memberName, BigWorld.player().getClanChallengeHostId())
            BigWorld.player().cell.addClanWarChallengeMember(clanChallengeMemberInfo[0], gbId, memberName, BigWorld.player().getClanChallengeHostId())

    def handleChangeMemberClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        gbId = int(e.currentTarget.data)
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, [])
        if not clanChallengeMemberInfo or not self.selectedMemberPos:
            return
        if gbId in self.oneVsOneGbIdSet and uiConst.ROUND_COUNT_LIST[self.selectedMemberPos[0]] == 1:
            p.showGameMsg(GMDD.data.ONE_VS_ONE_MEMBER_REPEAT)
            return
        if not p.isClanChallengeCommander(self.selectedFortId):
            p.showGameMsg(GMDD.data.CWC_SET_LAYOUT_FAIL_NO_AUTH, ())
            return
        gamelog.info('jbx:setClanWarChallengeLayout', clanChallengeMemberInfo[0], p.guild.nuid, gbId, self.selectedMemberPos[0], self.selectedMemberPos[1])
        p.cell.setClanWarChallengeLayout(clanChallengeMemberInfo[0], gbId, self.selectedMemberPos[0], self.selectedMemberPos[1], p.getClanChallengeHostId())

    def handleInputTextChange(self, *args):
        pass

    def handleInviteCloseBtnClick(self, *args):
        self.widget.inviteList.visible = False

    def handleDropDownIndexChange(self, *args):
        if self.lastSelectedMemberMc:
            self.lastSelectedMemberMc.selected = False
        self.selectedIdx = int(self.widget.dropDown.selectedIndex)
        self.lastSelectedMemberMc = None
        self.selectedMemberPos = None
        self.widget.inviteList.visible = False
        self.selectedFortId = self.fortIdList[self.selectedIdx] if self.selectedIdx < len(self.fortIdList) else 0
        BigWorld.player().queryClanWarChallengeMemberInfo(self.selectedFortId)
        self.refreshInfo()

    def memberListLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.schoolId))
        ASUtils.setHitTestDisable(itemMc.schoolIcon, True)
        itemMc.btn1.label = itemData.name
        itemMc.btn1.data = itemData.gbId
        itemMc.btn1.addEventListener(events.BUTTON_CLICK, self.handleChangeMemberClick, False, 0, True)
        stage = getattr(BigWorld.player(), 'clanWarChallengeState', None)
        itemMc.removeBtn.visible = BigWorld.player().isClanChallengeCommander(self.selectedFortId) and stage == const.CLAN_WAR_CHALLENGE_STAGE_PREPARE
        itemMc.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveSetMemeberClick, False, 0, True)
        itemMc.removeBtn.data = itemData.gbId

    def handleRemoveSetMemeberClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        gbId = int(e.currentTarget.data)
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, [])
        if not clanChallengeMemberInfo:
            return
        isInLayout = False
        for roundGbIdList in clanChallengeMemberInfo[3]:
            if gbId in roundGbIdList:
                isInLayout = True
                break

        gamelog.info('jbx:onRemoveClanWarChallengeMember', clanChallengeMemberInfo[0], p.guild.nuid, gbId)
        if isInLayout:
            msg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_REMOVE_MEMBER_IN_LAYOUT_CONFIRM, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_REMOVE_MEMBER_IN_LAYOUT_CONFIRM %s') % p.guild.member[gbId].role
        else:
            msg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_REMOVE_MEMBER_CONFIRM, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_REMOVE_MEMBER_CONFIRM %s') % p.guild.member[gbId].role
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.cell.removeClanWarChallengeMember, clanChallengeMemberInfo[0], gbId, p.getClanChallengeHostId()))

    def getInviteMemberList(self):
        p = BigWorld.player()
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, [])
        invitedMemberSet = set()
        for info in getattr(p, 'localClanChallengeMemberInfo', {}).itervalues():
            invitedMemberSet.update(set(info[2]))

        for info in getattr(p, 'crossClanChallengeMemberInfo', {}).itervalues():
            invitedMemberSet.update(set(info[2]))

        memberList = []
        if not clanChallengeMemberInfo:
            return memberList
        else:
            commanderId = 0
            if clanChallengeMemberInfo and self.isSetCommander:
                commanderId = clanChallengeMemberInfo[1]
            for gbId, guildMember in p.guild.member.iteritems():
                if not guildMember.online:
                    continue
                if self.isSetCommander:
                    if gbId == commanderId:
                        continue
                elif gbId in invitedMemberSet:
                    continue
                if self.searchKey and not uiUtils.filterPinYin(self.searchKey, guildMember.role):
                    continue
                memberInfo = {}
                memberInfo['schoolId'] = guildMember.school
                memberDetail = p.getClanChallengeMeberDetail(gbId)
                if not memberDetail:
                    headIcon = None
                    sex = 2
                else:
                    name, headIcon, schoold, sex, borderId = memberDetail
                memberInfo['name'] = guildMember.role
                memberInfo['txtPoint'] = gameStrings.CROSS_CLAN_CHALLENGE_COMBAT % guildMember.combatScore
                memberInfo['gbId'] = gbId
                memberInfo['headIcon'] = headIcon
                memberInfo['sex'] = sex
                memberList.append(memberInfo)

            memberList.sort(cmp=lambda a, b: cmp(b['txtPoint'], a['txtPoint']))
            return memberList

    def refreshInviteList(self):
        if self.widget and self.widget.inviteList.visible:
            self.widget.inviteList.list.dataArray = self.getInviteMemberList()

    def handleInviteBtnClick(self, *args):
        p = BigWorld.player()
        if not self.selectedFortId:
            return
        self.isSetCommander = False
        clanChallengeMemberInfo = getattr(p, 'clanChallengeMemberInfo', {}).get(self.selectedFortId, [])
        if not clanChallengeMemberInfo:
            return
        if len(clanChallengeMemberInfo[2]) >= CWCCD.data.get('maxCombatMemberCnt', 8):
            p.showGameMsg(GMDD.data.CLAN_WAR_CHALLENGE_MEMBER_MAX_CNT, ())
        self.widget.inviteList.visible = True
        self.widget.inviteList.list.dataArray = self.getInviteMemberList()
