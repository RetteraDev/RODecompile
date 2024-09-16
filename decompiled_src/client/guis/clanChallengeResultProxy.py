#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanChallengeResultProxy.o
import BigWorld
from Scaleform import GfxValue
import utils
import gametypes
import uiConst
import const
import events
from guis import ui
from guis import uiUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from guis.asObject import MenuManager
from data import clan_war_fort_data as CWFD
from data import clan_war_challenge_config_data as CWCCD
MEMBER_START_POS_IDXS = [2,
 0,
 1,
 0,
 2]

class ClanChallengeResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanChallengeResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.showResult = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_CHALLENGE_RESULT, self.hide)

    def reset(self):
        self.selectedIdx = None
        self.fortList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_CHALLENGE_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_CHALLENGE_RESULT)

    def show(self, fortId = 0):
        p = BigWorld.player()
        clanChallengeCombatResult = getattr(p, 'clanChallengeCombatResult', {})
        if not clanChallengeCombatResult:
            self.hide()
            return
        self.fortList = clanChallengeCombatResult.keys()
        if not self.fortList:
            return
        if fortId in self.fortList:
            self.selectedIdx = self.fortList.index(fortId)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_CHALLENGE_RESULT)

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.dropDown.dropdown = 'M12_DefaultScrollingList'
        self.widget.dropDown.itemRenderer = 'M12_DefaultListItemRenderer'
        self.widget.dropDown.labelFunction = self.dropDownLabelFunction
        self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
        self.widget.obBtn.addEventListener(events.BUTTON_CLICK, self.handleObBtnClick, False, 0, True)
        self.widget.obBtn.enabled = getattr(p, 'clanWarChallengeState', 0) >= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1

    def handleObBtnClick(self, *args):
        if not self.getFortId():
            return
        self.uiAdapter.clanChallengeObList.show()
        BigWorld.player().cell.startObserveClanWarChallenge(self.getFortId(), BigWorld.player().getClanChallengeHostId())

    def dropDownLabelFunction(self, *args):
        fortId = int(args[3][0].GetNumber())
        fortName = CWFD.data.get(fortId, {}).get('showName', '')
        return GfxValue(ui.gbk2unicode(fortName))

    def testChallengeResult(self):
        fortIdList = [23, 13]
        resultData = []
        p = BigWorld.player()
        roundCountList = [5,
         3,
         1,
         3,
         5]
        gbIdList = p.guild.member.keys()
        p.clanWarChallengeState = const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND3
        clanWarChallengeBaseInfo = []
        clanWarChallengeBaseInfo.append((23,
         p.guild.nuid,
         'defGuldName',
         '',
         0,
         p.guild.nuid + 1,
         'atkGuildName'))
        clanWarChallengeBaseInfo.append((13,
         p.guild.nuid,
         'defGuldName',
         '',
         0,
         p.guild.nuid + 1,
         'atkGuildName'))
        p.onQueryClanWarChallengeBaseInfo(clanWarChallengeBaseInfo)
        for fortId in fortIdList:
            ownerLayoutGbIds = []
            challengeLayoutGbId = []
            resultData.append((fortId,
             p.gbId,
             ownerLayoutGbIds,
             p.gbId,
             challengeLayoutGbId,
             [p.guild.nuid,
              0,
              p.guild.nuid,
              0]))
            for memberCnt in roundCountList:
                roundListOwn = []
                roundListDef = []
                ownerLayoutGbIds.append(roundListOwn)
                challengeLayoutGbId.append(roundListDef)
                for memberIdx in xrange(memberCnt):
                    if memberIdx % 2:
                        roundListOwn.append(0)
                        roundListDef.append(0)
                    else:
                        roundListOwn.append(gbIdList[memberIdx % 2])
                        roundListDef.append(gbIdList[memberIdx % 2])

        p.onQueryClanWarChallengeCombatInfo(resultData)

    def getFortId(self):
        if self.selectedIdx >= 0 and self.selectedIdx < len(self.fortList):
            return self.fortList[self.selectedIdx]
        return 0

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            clanChallengeCombatResult = getattr(p, 'clanChallengeCombatResult', {})
            if not clanChallengeCombatResult:
                self.hide()
                return
            ASUtils.setDropdownMenuData(self.widget.dropDown, self.fortList)
            if not self.selectedIdx:
                self.selectedIdx = 0
            self.widget.dropDown.selectedIndex = self.selectedIdx
            fortCombatResult = clanChallengeCombatResult.get(self.getFortId(), [])
            fortId, ownerCommanderGbId, ownGuildCommander, ownerGuildMember, ownerLayoutGbIds, challengeGuildNuid, challengeCommanderGbId, challengeGuildMember, challengeLayoutGbIds, winGuildNUIDs, tStart = fortCombatResult
            fortBaseInfo = p.getClanWarChallengeBaseInfo(self.getFortId())
            defGuildNuid, atkGuildNuid = fortBaseInfo[2], fortBaseInfo[5]
            self.widget.defGulldName.text = fortBaseInfo[3]
            self.widget.atkGuildName.text = fortBaseInfo[6]
            stage = getattr(p, 'clanWarChallengeState', 0)
            stateRoundIdx = stage - const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1
            for i in xrange(uiConst.ROUND_MAX_COUNT):
                startIdx = MEMBER_START_POS_IDXS[i]
                roundCount = uiConst.ROUND_COUNT_LIST[i]
                roundMc = self.widget.getChildByName('round%d' % i)
                roundDesc, timeDesc = CWCCD.data.get('roundTimeStrs', ('', '', '', '', '', '', '', '', '', ''))[i]
                roundMc.roundDesc.txtRound.text = roundDesc
                roundMc.roundDesc.txtTime.text = timeDesc
                roundMc.leftResult.visible = False
                roundMc.rightResult.visible = False
                if i > stateRoundIdx:
                    roundMc.roundDesc.txtStatus.text = gameStrings.CLAN_CHALLENGE_ROUND_READY
                elif i < len(winGuildNUIDs) and winGuildNUIDs[i] or i < stateRoundIdx:
                    roundMc.roundDesc.txtStatus.text = gameStrings.CLAN_CHALLENGE_ROUND_END
                elif i == stateRoundIdx:
                    roundMc.roundDesc.txtStatus.text = gameStrings.CLAN_CHALLENGE_ROUND_GOING
                if i < len(winGuildNUIDs) and winGuildNUIDs[i]:
                    winGuildNUID = winGuildNUIDs[i]
                    roundMc.leftResult.visible = True
                    roundMc.rightResult.visible = True
                    isDefWin = winGuildNUID == defGuildNuid
                    roundMc.leftResult.gotoAndStop('win' if isDefWin else 'fail')
                    roundMc.rightResult.gotoAndStop('win' if not isDefWin else 'fail')
                for memberIdx in xrange(uiConst.ROUND_MEMBER_MAX_CNT):
                    leftMemberMc = roundMc.getChildByName('leftPlayer%d' % memberIdx)
                    rightMemberMc = roundMc.getChildByName('rightPlayer%d' % memberIdx)
                    if memberIdx < startIdx or memberIdx >= startIdx + roundCount:
                        leftMemberMc.visible = False
                        rightMemberMc.visible = False
                    else:
                        leftMemberMc.visible = True
                        rightMemberMc.visible = True
                        try:
                            leftMemberGbId = ownerLayoutGbIds[i][memberIdx - startIdx]
                            leftMemberDetail = ownerGuildMember.get(leftMemberGbId, ())
                        except:
                            leftMemberGbId = 0
                            leftMemberDetail = None

                        try:
                            rightMemberGbId = challengeLayoutGbIds[i][memberIdx - startIdx]
                            rightMemberDetail = challengeGuildMember.get(rightMemberGbId, ())
                        except:
                            rightMemberGbId = 0
                            rightMemberDetail = None

                        self.refreshMemberMc(leftMemberGbId, leftMemberMc, leftMemberDetail)
                        self.refreshMemberMc(rightMemberGbId, rightMemberMc, rightMemberDetail)

            return

    def refreshMemberMc(self, gbId, memberMc, detailInfo):
        if not self.widget or not memberMc.stage:
            return
        if gbId:
            memberMc.visible = True
        else:
            memberMc.visible = False
            return
        p = BigWorld.player()
        if not detailInfo:
            memberMc.visible = False
            return
        memberMc.visible = True
        if len(detailInfo) == 5:
            name, icon, school, sex, borderId = detailInfo
        else:
            name, icon, school, sex = detailInfo
            borderId = 0
        memberMc.headIcon.fitSize = True
        memberMc.headIcon.dragable = False
        memberMc.borderImg.fitSize = True
        memberMc.borderImg.dragable = False
        if uiUtils.isDownloadImage(icon):
            if p.isDownloadNOSFileCompleted(icon):
                memberMc.headIcon.loadImage('../' + const.IMAGES_DOWNLOAD_DIR + '/' + icon + '.dds')
            else:
                memberMc.headIcon.loadImage('headIcon/%s.dds' % str(school * 10 + sex))
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (gbId, memberMc))
        else:
            memberMc.headIcon.loadImage('headIcon/%s.dds' % str(school * 10 + sex))
        memberMc.borderImg.loadImage(p.getPhotoBorderIcon(borderId))
        memberMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school))
        memberMc.data = gbId
        TipManager.addTip(memberMc, name)
        menuParam = {'roleName': name,
         'gbId': gbId}
        MenuManager.getInstance().registerMenuById(memberMc, uiConst.MENU_TARGET, menuParam)

    def handleMemberClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            gbId = e.currentTarget.data
            MenuManager.getInstance().menuTarget.apply(gbId=long(gbId), hostId=utils.getHostId(), menuId=uiConst.MENU_TARGET)

    def onDownloadPhoto(self, status, callbackArgs):
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.refreshMemberMc(callbackArgs[0], callbackArgs[1])

    def handleIndexChange(self, *args):
        self.selectedIdx = int(self.widget.dropDown.selectedIndex)
        fortId = self.getFortId()
        if fortId:
            BigWorld.player().cell.queryClanWarChallengeCombatInfo(fortId, BigWorld.player().getClanChallengeHostId())
