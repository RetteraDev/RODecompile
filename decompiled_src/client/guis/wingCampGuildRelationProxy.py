#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingCampGuildRelationProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import wing_world_config_data as WWCD

class WingCampGuildRelationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingCampGuildRelationProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CAMP_GUILD_RELATION, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CAMP_GUILD_RELATION:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CAMP_GUILD_RELATION)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CAMP_GUILD_RELATION)
        self.queryServerInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.queryWingWorldCampGuildRelation()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.friendInput.visible = False
        self.widget.friendBtn.visible = self.canEditRelation()
        self.widget.friendBtn.label = gameStrings.CHANGE
        self.widget.friendBtn.addEventListener(events.BUTTON_CLICK, self.onFriendBtnClick)
        self.widget.enermyInput.visible = False
        self.widget.enermyBtn.visible = self.canEditRelation()
        self.widget.enermyBtn.label = gameStrings.CHANGE
        self.widget.enermyBtn.addEventListener(events.BUTTON_CLICK, self.onEnermyBtnClick)
        self.widget.Tip.htmlText = WWCD.data.get('wingCampGuildRelationTip', gameStrings.WING_WORLD_CAMP_GUILD_RELATION_TIP)
        self.widget.friendTip.htmlText = WWCD.data.get('wingCampGuildRelationFriendTip', gameStrings.WING_WORLD_CAMP_GUILD_RELATION_FRIEND_TIP)
        self.widget.enermyTip.htmlText = WWCD.data.get('wingCampGuildRelationEnermyTip', gameStrings.WING_WORLD_CAMP_GUILD_RELATION_ENERMY_TIP)

    def canEditRelation(self):
        p = BigWorld.player()
        state = getattr(p, 'wingWorldCampState', gametypes.WW_CAMP_STATE_DEFAULT)
        if state != gametypes.WW_CAMP_STATE_SIGNUP_START:
            return False
        if p.guild:
            return gameglobal.rds.ui.guild._hasPrivilege(p.guild.memberMe.roleId, gametypes.GUILD_ACTION_WING_WORLD_CAMP_SIGNUP)
        return False

    def onFriendBtnClick(self, *args):
        p = BigWorld.player()
        if self.widget.friendInput.visible:
            self.widget.friendInput.visible = False
            self.widget.friendName.visible = True
            self.widget.friendBtn.label = gameStrings.CHANGE
            friendName = self.widget.friendInput.text
            p.base.setGuildWorldCampGuildFriend(friendName)
            self.refreshInfo()
        else:
            self.widget.friendBtn.label = gameStrings.CONFIRM
            self.widget.friendInput.visible = True
            self.widget.friendName.visible = False

    def onEnermyBtnClick(self, *args):
        p = BigWorld.player()
        if self.widget.enermyInput.visible:
            self.widget.enermyInput.visible = False
            self.widget.enermyName.visible = True
            self.widget.enermyBtn.label = gameStrings.CHANGE
            enermyName = self.widget.enermyInput.text
            p.base.setWingWorldCampGuildEnemy(enermyName)
            self.refreshInfo()
        else:
            self.widget.enermyBtn.label = gameStrings.CONFIRM
            self.widget.enermyInput.visible = True
            self.widget.enermyName.visible = False

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            friendGuildName = ''
            enermyGuildName = ''
            if getattr(p, 'guild', None):
                friendGuildName = getattr(p.guild, 'wingWorldCampFriendName', '')
                enermyGuildName = getattr(p.guild, 'wingWorldCampEnemyName', '')
            self.widget.friendInput.text = friendGuildName
            self.widget.friendName.text = friendGuildName if friendGuildName else gameStrings.WING_WORLD_NO_GUILD_NAME
            self.widget.enermyInput.text = enermyGuildName
            self.widget.enermyName.text = enermyGuildName if enermyGuildName else gameStrings.WING_WORLD_NO_GUILD_NAME
            return
