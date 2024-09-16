#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/WingWorldCampProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import events
import uiUtils
import const
import utils
import wingWorldUtils
from guis.asObject import ASObject
import gametypes
from gamestrings import gameStrings
from guis.asObject import ASUtils
from uiProxy import UIProxy
from data import region_server_config_data as RSCD
from data import wing_world_config_data as WWCD
from data import wing_world_city_data as WWCID
from cdata import game_msg_def_data as GMDD
from guis.asObject import Tweener
RANK_TAB_GUILD = 0
RANK_TAB_PLAYER = 1
CITY_MARGIN = 5
CITY_WIDTH = 70
RANK_ITEM_NUM = 5
PAGE_CITY_NUM = 6
INDICATOR_X = 249
INDICATOR_STEP = 12

class WingWorldCampProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCampProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currCamp = 0
        self.reset()
        self.rankTab = RANK_TAB_GUILD
        self.guildRankCache = {}
        self.personRankCache = {}

    def reset(self):
        self.widget = None
        self.currCamp = 0
        self.rankTab = RANK_TAB_GUILD

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        self.queryServerInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        if p.guild:
            BigWorld.player().base.queryWingWorldCampGuildInfo()
            p.base.queryWingWorldCampCities(0)

    def queryTopInfo(self):
        if self.rankTab == RANK_TAB_GUILD:
            self.queryGuildTopInfo()
        else:
            self.queryPersonTopInfo()

    def queryGuildTopInfo(self):
        p = BigWorld.player()
        if self.currCamp:
            rankData = self.guildRankCache.get(self.currCamp, {})
            p.base.queryWWCGuildContriVeryTop(self.currCamp, rankData.get('ver', 0))

    def updateGuildRank(self, groupId, campId, ver, topData):
        rankData = {'groupId': groupId,
         'campId': campId,
         'ver': ver,
         'topData': topData}
        self.guildRankCache[campId] = rankData
        self.refreshRankInfo()

    def queryPersonTopInfo(self):
        p = BigWorld.player()
        if self.currCamp:
            rankData = self.personRankCache.get(self.currCamp, {})
            p.base.queryWWCPersonContriVeryTop(self.currCamp, rankData.get('ver', 0))

    def updatePersonRank(self, groupId, campId, ver, topData):
        rankData = {'groupId': groupId,
         'campId': campId,
         'ver': ver,
         'topData': topData}
        self.personRankCache[campId] = rankData
        self.refreshRankInfo()

    def unRegisterPanel(self):
        self.reset()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.camp1Btn.selected = self.currCamp == 1 and p.wingWorldCamp
        self.widget.camp2Btn.selected = self.currCamp == 2 and p.wingWorldCamp
        ASUtils.setHitTestDisable(self.widget.camp1Btn, False)
        ASUtils.setHitTestDisable(self.widget.camp2Btn, False)
        if p.wingWorldCamp == 1:
            if p.guild and p.isWWCampGuildCampSame():
                guildName = p.guild.name
                stateName = '(%s)' % gameStrings.WING_WORLD_GUILD_SIGN_IN
            else:
                guildName = p.roleName
                stateName = '(%s)' % gameStrings.WING_WORLD_SELF_SIGN_IN
            self.widget.camp1Btn.labels = [gameStrings.WING_WORLD_JOIN_THIS_CAMP, guildName, stateName]
            self.widget.camp2Btn.labels = ['', '', '']
        elif p.wingWorldCamp == 2:
            if p.guild and p.isWWCampGuildCampSame():
                guildName = p.guild.name
                stateName = '(%s)' % gameStrings.WING_WORLD_GUILD_SIGN_IN
            else:
                guildName = p.roleName
                stateName = '(%s)' % gameStrings.WING_WORLD_SELF_SIGN_IN
            self.widget.camp1Btn.labels = ['', '', '']
            self.widget.camp2Btn.labels = [gameStrings.WING_WORLD_JOIN_THIS_CAMP, guildName, stateName]
        else:
            ASUtils.setHitTestDisable(self.widget.camp1Btn, True)
            ASUtils.setHitTestDisable(self.widget.camp2Btn, True)
            self.widget.camp1Btn.labels = ['', '', '']
            self.widget.camp2Btn.labels = ['', '', '']
        if p.isInWingWorldCamp():
            self.widget.campMc.visible = True
            self.widget.attendMc.visible = False
            self.refreshCampMc()
        else:
            self.widget.campMc.visible = False
            self.widget.attendMc.visible = True
            self.refreshSignIn()

    def initSignInMc(self):
        signInMc = self.widget.attendMc
        signInMc.soloBtn.addEventListener(events.BUTTON_CLICK, self.onSoloBtnClick)
        signInMc.quitSoloBtn.addEventListener(events.BUTTON_CLICK, self.onQuitSoloBtnClick)
        signInMc.relationBtn.addEventListener(events.BUTTON_CLICK, self.onRelationBtnClick)
        signInMc.memberBtn.addEventListener(events.BUTTON_CLICK, self.onSignInMemberBtnClick)
        signInMc.guildBtn.addEventListener(events.BUTTON_CLICK, self.onSignInGuildBtnClick)
        signInMc.commitBtn.addEventListener(events.BUTTON_CLICK, self.onSignInCommitBtnClick)

    def onSignInMemberBtnClick(self, *args):
        p = BigWorld.player()
        if p.guild.wingWorldCampState == gametypes.WW_CAMP_GUILD_STATE_DEFAULT:
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_GUILD_NO_SIGN_CLICK)
            return
        gameglobal.rds.ui.wingCampGuildList.show()

    def onSignInGuildBtnClick(self, *args):
        p = BigWorld.player()
        msg = WWCD.data.get('wingCampGuildSignConfirm', gameStrings.WING_WORLD_CAMP_GUILD_SIGNIN_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.base.guildSignUpWingWorldCamp, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def onSignInCommitBtnClick(self, *args):
        p = BigWorld.player()
        p.base.commitWingWorldCamp()

    def onRelationBtnClick(self, *args):
        gameglobal.rds.ui.wingCampGuildRelation.show()

    def onSoloBtnClick(self, *args):
        p = BigWorld.player()
        if p.isWWCampFollowGuildSignUp():
            msg = WWCD.data.get('wingCampSingleSignWithGuildConfirm', gameStrings.WING_WORLD_CAMP_PERSON_SIGNIN_WITH_GUILD_CONFIRM)
        else:
            msg = WWCD.data.get('wingCampSingleSignConfirm', gameStrings.WING_WORLD_CAMP_PERSON_SIGNIN_CONFIRM)
        state = getattr(p, 'wingWorldCampState', gametypes.WW_CAMP_STATE_DEFAULT)
        if state == gametypes.WW_CAMP_STATE_START:
            msg = '%s\n%s' % (msg, gameStrings.WING_WORLD_CAMP_SEASON_START_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().base.signUpWingWorldCamp, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def onQuitSoloBtnClick(self, *args):
        BigWorld.player().base.cancelSignUpWingWorldCamp()

    def initCampMc(self):
        campMc = self.widget.campMc
        campMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        campMc.memberBtn.addEventListener(events.BUTTON_CLICK, self.onMemberBtnClick)
        campMc.fullRankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        campMc.guildRankTab.addEventListener(events.BUTTON_CLICK, self.onGuildRankBtnClick)
        campMc.soloRankTab.addEventListener(events.BUTTON_CLICK, self.onSoloRankBtnClick)
        p = BigWorld.player()
        if p.guild and p.wingWorldCamp and p.isWWCampGuildCampSame():
            campMc.memberBtn.visible = True
        else:
            campMc.memberBtn.visible = False
        self.initCityMc()

    def refreshCampMc(self):
        if not self.widget:
            return
        campMc = self.widget.campMc
        campMc.camp1Title.visible = self.currCamp == 1
        campMc.camp2Title.visible = self.currCamp == 2
        p = BigWorld.player()
        if p.guild:
            campMc.memberBtn.enabled = True
        else:
            campMc.memberBtn.enabled = False
        self.refreshCityMc()
        self.refreshRankInfo()
        self.queryTopInfo()

    def initCityMc(self):
        cityMc = self.widget.campMc.citiesMc
        cityCanvas = cityMc.cityList.canvas
        cityMc.cityList.cityIdx = 0
        cityCanvas.x = 0
        cityMc.leftBtn.addEventListener(events.BUTTON_CLICK, self.onLeftBtnClick)
        cityMc.rightBtn.addEventListener(events.BUTTON_CLICK, self.onRightBtnClick)
        for i in xrange(3):
            idxMc = cityMc.indicator.getChildByName('i%d' % i)
            idxMc.idx = i
            idxMc.addEventListener(events.BUTTON_CLICK, self.onIndicatorBtnClick)

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)

    def onLeftBtnClick(self, *args):
        e = ASObject(args[3][0])
        idx = e.currentTarget.parent.cityList.cityIdx
        idx -= 1
        idx = max(0, idx)
        self.refreshCityListPos(idx)

    def onRightBtnClick(self, *args):
        e = ASObject(args[3][0])
        idx = e.currentTarget.parent.cityList.cityIdx
        idx += 1
        idx = min(2, idx)
        self.refreshCityListPos(idx)

    def onIndicatorBtnClick(self, *args):
        e = ASObject(args[3][0])
        idx = e.currentTarget.idx
        self.refreshCityListPos(idx)

    def refreshCityListPos(self, newIdx, doAnim = True):
        cityMc = self.widget.campMc.citiesMc
        left, right = self.getCityScrollRange()
        cityMc.leftBtn.enabled = newIdx > left
        cityMc.rightBtn.enabled = newIdx < right
        cityMc.cityList.cityIdx = newIdx
        cityCanvas = cityMc.cityList.canvas
        toPosX = -(newIdx * cityMc.cityList.canvasMask.width)
        self.refreshIndicator(newIdx)
        if doAnim:
            Tweener.addTween(cityCanvas, {'x': toPosX,
             'time': 0.15,
             'transition': 'easeinsine'})
        else:
            cityCanvas.x = toPosX

    def getCityScrollRange(self):
        p = BigWorld.player()
        ownedCities = p.wingWorld.country.getCamp(self.currCamp).ownedCityIds
        realOwnerCities = []
        groupId = RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldGroupId', 0)
        for cityId in ownedCities:
            if wingWorldUtils.isCitySwallow(groupId, cityId):
                continue
            realOwnerCities.append(cityId)

        return (0, int(max(0, len(realOwnerCities) - 1) / PAGE_CITY_NUM))

    def refreshIndicator(self, currIdx):
        cityMc = self.widget.campMc.citiesMc
        left, right = self.getCityScrollRange()
        for i in xrange(3):
            idxMc = cityMc.indicator.getChildByName('i%d' % i)
            idxMc.selected = currIdx == i
            idxMc.visible = left <= i <= right and right != 0

        cityMc.indicator.x = INDICATOR_X if right >= 2 else INDICATOR_X + INDICATOR_STEP

    def refreshCityMc(self):
        if not self.widget or not self.widget.campMc.visible:
            return
        cityMc = self.widget.campMc.citiesMc
        cityCanvas = cityMc.cityList.canvas
        self.removeAllChild(cityCanvas)
        p = BigWorld.player()
        groupId = RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldGroupId', 0)
        ownedCities = p.wingWorld.country.getCamp(self.currCamp).ownedCityIds
        realOwnerCities = []
        for cityId in ownedCities:
            if wingWorldUtils.isCitySwallow(groupId, cityId):
                continue
            realOwnerCities.append(cityId)

        for i, cityId in enumerate(realOwnerCities):
            itemMc = self.widget.getInstByClsName('WingWorldCamp_city')
            cityCanvas.addChild(itemMc)
            if self.currCamp == 1:
                itemMc.gotoAndStop('red')
            else:
                itemMc.gotoAndStop('blue')
            itemMc.x = CITY_MARGIN + i * (CITY_MARGIN * 2 + CITY_WIDTH)
            itemMc.cityName.text = WWCID.data.get(cityId, {}).get('name', '')

        self.refreshCityListPos(0)
        if cityMc.noText:
            if not realOwnerCities:
                cityMc.noText.visible = True
            else:
                cityMc.noText.visible = False

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_WINGWORLD_CAMP)

    def onMemberBtnClick(self, *args):
        p = BigWorld.player()
        if p.guild.wingWorldCampState == gametypes.WW_CAMP_GUILD_STATE_DEFAULT:
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_GUILD_NO_SIGN_CLICK)
            return
        gameglobal.rds.ui.wingCampGuildList.show()

    def onRankBtnClick(self, *args):
        if self.rankTab == RANK_TAB_GUILD:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WORLD_CAMP_CONTRI_GUILD)
        else:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WORLD_CAMP_CONTRI_PERSON)

    def onGuildRankBtnClick(self, *args):
        self.rankTab = RANK_TAB_GUILD
        self.queryTopInfo()
        self.refreshRankInfo()

    def onSoloRankBtnClick(self, *args):
        self.rankTab = RANK_TAB_PLAYER
        self.queryTopInfo()
        self.refreshRankInfo()

    def refreshRankInfo(self):
        if not self.widget:
            return
        campMc = self.widget.campMc
        campMc.guildRankTab.selected = self.rankTab == RANK_TAB_GUILD
        campMc.soloRankTab.selected = self.rankTab == RANK_TAB_PLAYER
        campMc.guildRank.visible = self.rankTab == RANK_TAB_GUILD
        campMc.soloRank.visible = self.rankTab == RANK_TAB_PLAYER
        if self.rankTab == RANK_TAB_GUILD:
            rankData = self.guildRankCache.get(self.currCamp, {}).get('topData', [])
            for i in xrange(RANK_ITEM_NUM):
                rankItem = campMc.guildRank.getChildByName('item%d' % i)
                if i < len(rankData):
                    data = rankData[i]
                    rankItem.visible = True
                    rankItem.val0.text = i + 1
                    rankItem.val1.text = '%s-%s' % (data[1], utils.getServerName(data[4]))
                    rankItem.val2.text = data[3]
                    rankItem.val3.text = data[2]
                else:
                    rankItem.visible = False

        elif self.rankTab == RANK_TAB_PLAYER:
            rankData = self.personRankCache.get(self.currCamp, {}).get('topData', [])
            for i in xrange(RANK_ITEM_NUM):
                rankItem = campMc.soloRank.getChildByName('item%d' % i)
                if i < len(rankData):
                    data = rankData[i]
                    rankItem.visible = True
                    rankItem.val0.text = i + 1
                    rankItem.val1.text = '%s-%s' % (data[1], utils.getServerName(data[3]))
                    rankItem.val2.text = const.SCHOOL_DICT.get(data[4], '')
                    rankItem.val3.text = data[2]
                else:
                    rankItem.visible = False

    def onCampBtnClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.name == 'camp1Btn':
            camp = 1
        else:
            camp = 2
        if camp != self.currCamp:
            self.currCamp = camp
            self.refreshInfo()

    def refreshSignIn(self):
        if not self.widget:
            return
        signInMc = self.widget.attendMc
        p = BigWorld.player()
        state = getattr(p, 'wingWorldCampState', gametypes.WW_CAMP_STATE_DEFAULT)
        if state < gametypes.WW_CAMP_STATE_START:
            signInMc.timeTitle.htmlText = gameStrings.WING_WORLD_CAMP_BEFORE_BATTLE_SIGN_TIME
            signInMc.desc.htmlText = WWCD.data.get('wingCampDesc', '')
            signInMc.signupTime.text = WWCD.data.get('wingCampSignInTime', '')
            signInMc.soloDesc.htmlText = WWCD.data.get('wingCampSingleDesc', gameStrings.WING_WORLD_CAMP_SINGLE_DESC)
            signInMc.guildDesc.htmlText = WWCD.data.get('wingCampGuildDesc', gameStrings.WING_WORLD_CAMP_GUILD_DESC)
        elif state == gametypes.WW_CAMP_STATE_START:
            signInMc.timeTitle.htmlText = gameStrings.WING_WORLD_CAMP_IN_BATTLE_SIGN_TIME
            signInMc.desc.htmlText = WWCD.data.get('wingCampDesc2', '')
            signInMc.soloDesc.htmlText = WWCD.data.get('wingCampSingleDesc2', gameStrings.WING_WORLD_CAMP_SINGLE_DESC)
            signInMc.guildDesc.htmlText = WWCD.data.get('wingCampGuildDesc2', gameStrings.WING_WORLD_CAMP_GUILD_DESC)
            signInMc.signupTime.text = ''
        else:
            signInMc.timeTitle.htmlText = gameStrings.WING_WORLD_CAMP_IN_OVER_SIGN_TIME
            signInMc.desc.htmlText = WWCD.data.get('wingCampDesc2', '')
            signInMc.soloDesc.htmlText = WWCD.data.get('wingCampSingleDesc2', gameStrings.WING_WORLD_CAMP_SINGLE_DESC)
            signInMc.guildDesc.htmlText = WWCD.data.get('wingCampGuildDesc2', gameStrings.WING_WORLD_CAMP_GUILD_DESC)
            signInMc.signupTime.text = ''
        if p.guild and p.guild.wingWorldCampState != gametypes.WW_CAMP_GUILD_STATE_DEFAULT and not p.isWWCampFollowGuildSignUp():
            signInMc.followAlert.visible = True
        else:
            signInMc.followAlert.visible = False
        signInMc.commitBtn.visible = False
        signInMc.guildBtn.visible = True
        signInMc.relationBtn.enabled = True
        signInMc.memberBtn.enabled = True
        signInMc.guildBtn.label = gameStrings.WING_WORLD_GUILD_SIGN_IN
        if p.guild:
            if p.guild.wingWorldCampState == gametypes.WW_CAMP_GUILD_STATE_SIGNED:
                if state == gametypes.WW_CAMP_STATE_START:
                    signInMc.commitBtn.visible = True
                    signInMc.guildBtn.visible = False
                else:
                    signInMc.guildBtn.enabled = False
                    signInMc.guildBtn.label = gameStrings.WING_WORLD_GUILD_SIGN_IN_OVER
            elif p.guild.wingWorldCampState in (gametypes.WW_CAMP_GUILD_STATE_FINISH, gametypes.WW_CAMP_GUILD_STATE_COMMIT):
                signInMc.guildBtn.enabled = False
                signInMc.guildBtn.label = gameStrings.WING_WORLD_GUILD_SIGN_IN_OVER
            else:
                signInMc.guildBtn.enabled = True
        else:
            signInMc.guildBtn.enabled = False
            signInMc.relationBtn.enabled = False
            signInMc.memberBtn.enabled = False
        signInMc.soloBtn.visible = not p.isWWCampSingleSignUp()
        signInMc.quitSoloBtn.visible = p.isWWCampSingleSignUp()
        if state not in (gametypes.WW_CAMP_STATE_SIGNUP_START, gametypes.WW_CAMP_STATE_START):
            signInMc.commitBtn.enabled = False
            signInMc.guildBtn.enabled = False
            signInMc.soloBtn.enabled = False
        if state in (gametypes.WW_CAMP_STATE_SIGNUP_START,
         gametypes.WW_CAMP_STATE_SIGNUP_END,
         gametypes.WW_CAMP_STATE_ALLOC,
         gametypes.WW_CAMP_STATE_NOTIFICATION):
            signInMc.relationBtn.visible = True
        else:
            signInMc.relationBtn.visible = False

    def initUI(self):
        p = BigWorld.player()
        if not self.currCamp:
            self.currCamp = p.wingWorldCamp
        if self.currCamp == 0:
            self.currCamp = 1
        self.initCampMc()
        self.initSignInMc()
        self.widget.camp1Btn.addEventListener(events.BUTTON_CLICK, self.onCampBtnClick)
        self.widget.camp2Btn.addEventListener(events.BUTTON_CLICK, self.onCampBtnClick)
