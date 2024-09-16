#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingCampGuildListProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import uiConst
import utils
from guis import events
from guis.asObject import ASObject
from guis.asObject import MenuManager
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import guildProxy
from data import wing_world_config_data as WWCD
SORT_TYPE_NAME = 0
SORT_TYPE_POS = 1
SORT_TYPE_LV = 2
SORT_TYPE_SCHOOL = 3
SORT_TYPE_OTHER = 4
ATTR_TITLE = [gameStrings.TEXT_WINGCAMPGUILDLISTPROXY_20,
 gameStrings.TEXT_WINGCAMPGUILDLISTPROXY_20_1,
 gameStrings.TEXT_GMENTITY_49_2,
 gameStrings.TEXT_CHALLENGEPROXY_187]

class WingCampGuildListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingCampGuildListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.isSignIn = False
        self.sortType = SORT_TYPE_POS
        self.reverse = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CAMP_GUILD_LIST, self.hide)

    def reset(self):
        self.isSignIn = False
        self.reverse = False
        self.sortType = SORT_TYPE_POS

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CAMP_GUILD_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.isSignIn = False
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CAMP_GUILD_LIST)

    def show(self):
        p = BigWorld.player()
        if p.guild:
            if p.guild.wingWorldCampState >= gametypes.WW_CAMP_GUILD_STATE_COMMIT:
                self.isSignIn = False
            else:
                self.isSignIn = True
        else:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CAMP_GUILD_LIST)
        self.queryServerInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.queryWWCampGuildList()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.attendBtn.addEventListener(events.BUTTON_CLICK, self.onAttendBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.widget.memberList.itemRenderer = 'WingWorldCampGuildList_memberItem'
        self.widget.memberList.labelFunction = self.guildMemberLabelFunc
        self.widget.memberList.dataArray = []

    def isFollowGuild(self, data):
        p = BigWorld.player()
        if p.gbId == long(data.gbId):
            return p.isWWCampFollowGuildSignUp()
        if p.guild:
            if long(data.gbId) in p.guild.wwCampGuildList:
                return True
        return False

    def guildMemberLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        p = BigWorld.player()
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_WING_CAMP_GUILD_LIT, {'roleName': itemData.nameText,
         'gbId': long(itemData.gbId),
         'hostId': p.getOriginHostId()})
        itemMc.roleName.text = itemData.nameText
        itemMc.lv.text = itemData.lvText
        itemMc.school.text = itemData.schoolText
        itemMc.title.text = itemData.postText
        if self.isSignIn:
            itemMc.state.htmlText = gameStrings.WING_WORLD_CAMP_FOLOOW_GUILD if self.isFollowGuild(itemData) else gameStrings.WING_WORLD_CAMP_UNFOLOOW_GUILD
        else:
            itemMc.state.text = utils.convertNum(itemData.wingWorldContri)

    def meFirstSortFunc(self, memeberA, memeberB):
        if memeberA.gbId == BigWorld.player().gbId:
            return -1
        if memeberB.gbId == BigWorld.player().gbId:
            return 1
        return 0

    def nameCmpFunc(self, memeberA, memeberB):
        return cmp(memeberA.role, memeberB.role)

    def otherCmpFunc(self, memeberA, memeberB):
        if self.isSignIn:
            return -cmp(self.isFollowGuild(memeberA), self.isFollowGuild(memeberB))
        else:
            return -cmp(memeberA.wingWorldContri, memeberB.wingWorldContri)

    def getSortedMemberList(self):
        p = BigWorld.player()
        guildMemberList = p.guild.member.values()
        if self.sortType == SORT_TYPE_POS:
            isReverse = guildProxy.SORT_MAP[guildProxy.SORT_TYPE_POST][1]
            if not self.reverse:
                isReverse = not isReverse
            guildMemberList = sorted(guildMemberList, cmp=guildProxy.SORT_MAP[guildProxy.SORT_TYPE_POST][0], reverse=isReverse)
        elif self.sortType == SORT_TYPE_LV:
            isReverse = guildProxy.SORT_MAP[guildProxy.SORT_TYPE_LV][1]
            if not self.reverse:
                isReverse = not isReverse
            guildMemberList = sorted(guildMemberList, cmp=guildProxy.SORT_MAP[guildProxy.SORT_TYPE_LV][0], reverse=isReverse)
        elif self.sortType == SORT_TYPE_SCHOOL:
            isReverse = guildProxy.SORT_MAP[guildProxy.SORT_TYPE_SCHOOL][1]
            if not self.reverse:
                isReverse = not isReverse
            guildMemberList = sorted(guildMemberList, cmp=guildProxy.SORT_MAP[guildProxy.SORT_TYPE_SCHOOL][0], reverse=isReverse)
        elif self.sortType == SORT_TYPE_NAME:
            guildMemberList = sorted(guildMemberList, cmp=self.nameCmpFunc, reverse=self.reverse)
        elif self.sortType == SORT_TYPE_OTHER:
            guildMemberList = sorted(guildMemberList, cmp=self.otherCmpFunc, reverse=self.reverse)
        guildMemberList = sorted(guildMemberList, cmp=self.meFirstSortFunc)
        return guildMemberList

    def refreshAttrTitle(self):
        for i in xrange(5):
            attrItem = self.widget.getChildByName('attr%d' % i)
            attrItem.addEventListener(events.MOUSE_CLICK, self.onAttrItemClick)
            if i == 4:
                if self.isSignIn:
                    titleText = gameStrings.WING_WORLD_CAMP_STATE
                else:
                    titleText = gameStrings.WING_WORLD_CAMP_SCORE
            else:
                titleText = ATTR_TITLE[i]
            if self.sortType == i:
                if self.reverse:
                    titleText += gameStrings.TEXT_WINGCAMPGUILDLISTPROXY_160
                else:
                    titleText += gameStrings.TEXT_WINGCAMPGUILDLISTPROXY_162
            attrItem.text = titleText

    def onAttrItemClick(self, *args):
        e = ASObject(args[3][0])
        sortType = int(e.currentTarget.name[-1])
        if self.sortType == sortType:
            self.reverse = not self.reverse
        else:
            self.sortType = sortType
            self.reverse = False
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.refreshAttrTitle()
        if not self.isSignIn:
            self.widget.disableBtn.visible = False
            self.widget.cancelBtn.visible = False
            self.widget.attendBtn.visible = False
        else:
            state = getattr(p, 'wingWorldCampState', gametypes.WW_CAMP_STATE_DEFAULT)
            self.widget.attendBtn.visible = False
            self.widget.cancelBtn.visible = False
            self.widget.disableBtn.visible = False
            if state in (gametypes.WW_CAMP_STATE_SIGNUP_START, gametypes.WW_CAMP_STATE_START):
                if p.guild.wingWorldCampState == gametypes.WW_CAMP_GUILD_STATE_SIGNED:
                    self.widget.disableBtn.visible = False
                    if p.isWWCampFollowGuildSignUp():
                        self.widget.attendBtn.visible = False
                        self.widget.cancelBtn.visible = True
                    else:
                        self.widget.attendBtn.visible = True
                        self.widget.cancelBtn.visible = False
                elif p.guild.wingWorldCampState != gametypes.WW_CAMP_GUILD_STATE_DEFAULT:
                    self.widget.disableBtn.visible = True
                    self.widget.disableBtn.label = gameStrings.WING_WORLD_CAMP_GUILD_COMMIT
                else:
                    self.widget.disableBtn.visible = True
                    self.widget.disableBtn.label = gameStrings.WING_WORLD_CAMP_GUILD_COMMIT
            else:
                self.widget.disableBtn.visible = True
                self.widget.disableBtn.label = gameStrings.WING_WORLD_CAMP_FOLLOW_NOT_IN_TIME
        membersInfo = []
        if p.guild:
            guildMemberList = self.getSortedMemberList()
            if self.isSignIn:
                for member in guildMemberList:
                    if member and member.level >= 69:
                        memberInfo = gameglobal.rds.ui.guild.createMemberInfo(member)
                        memberInfo['wingWorldContri'] = member.wingWorldContri
                        membersInfo.append(memberInfo)

            else:
                wwCampGuildList = getattr(p.guild, 'wwCampGuildList', [])
                for member in guildMemberList:
                    if member and member.level >= 69 and member.gbId in wwCampGuildList:
                        memberInfo = gameglobal.rds.ui.guild.createMemberInfo(member)
                        memberInfo['wingWorldContri'] = member.wingWorldContri
                        membersInfo.append(memberInfo)

        self.widget.memberList.dataArray = membersInfo

    def onAttendBtnClick(self, *args):
        p = BigWorld.player()
        if p.isWWCampSingleSignUp():
            msg = WWCD.data.get('wingCampGuildSignWithSingleConfirm', gameStrings.WING_WORLD_CAMP_GUILD_SIGNIN_WITH_SINGLE_CONFIRM)
            state = getattr(p, 'wingWorldCampState', gametypes.WW_CAMP_STATE_DEFAULT)
            if state == gametypes.WW_CAMP_STATE_START:
                msg = '%s\n%s' % (msg, gameStrings.WING_WORLD_CAMP_SEASON_START_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.base.signUpWingWorldCampFollowGuild, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)
        else:
            p.base.signUpWingWorldCampFollowGuild()

    def onCancelBtnClick(self, *args):
        p = BigWorld.player()
        p.base.cancelSignUpWingWorldCampWithGuild()
