#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendBGV2Proxy.o
import BigWorld
import gameglobal
import uiConst
from guis import events
from guis import ui
from uiTabProxy import UITabProxy
from asObject import RedPotManager
from Scaleform import GfxValue

class SummonFriendBGV2Proxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendBGV2Proxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMON_FRIEND_BG_V2, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMON_FRIEND_BG_V2:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(SummonFriendBGV2Proxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMON_FRIEND_BG_V2)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def clearAll(self):
        pass

    def reset(self):
        super(SummonFriendBGV2Proxy, self).reset()

    def _getTabList(self):
        return [{'tabIdx': uiConst.SUMMON_FRIEND_TAB_INDEX0,
          'tabName': 'shopBtn',
          'view': 'SummonFriendShopV2Widget',
          'proxy': 'summonFriendShopV2'}, {'tabIdx': uiConst.SUMMON_FRIEND_TAB_INDEX1,
          'tabName': 'activityBtn',
          'view': 'SummonFriendInviteV2Widget',
          'proxy': 'summonFriendInviteV2'}, {'tabIdx': uiConst.SUMMON_FRIEND_TAB_INDEX2,
          'tabName': 'backBtn',
          'view': 'SummonFriendBackV2Widget',
          'proxy': 'summonFriendBackV2'}]

    def show(self, showTabIndex = 0, tabBtnName = None):
        if not gameglobal.rds.configData.get('enableSummonFriendV2', False):
            return
        else:
            self.showTabIndex = showTabIndex
            if self.widget:
                self.widget.setTabIndex(self.showTabIndex)
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMON_FRIEND_BG_V2)
            if tabBtnName:
                tabProxy = getattr(self.uiAdapter, self._getTabList()[showTabIndex]['proxy'], None)
                hasattr(tabProxy, 'setBtnTabName') and tabProxy.setBtnTabName(tabBtnName)
            return

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        RedPotManager.removeRedPotById(uiConst.SUMMON_FRIEND_BACK_BTN_RED_POT)
        RedPotManager.addRedPot(self.widget.backBtn, uiConst.SUMMON_FRIEND_BACK_BTN_RED_POT, (self.widget.backBtn.width - 5, -4), self.visiblePotFunBackBtn)

    def onTabChanged(self, *args):
        super(SummonFriendBGV2Proxy, self).onTabChanged(*args)
        self.refreshInfo()

    @ui.uiEvent(uiConst.WIDGET_SUMMON_FRIEND_BG_V2, events.EVENT_INVITE_POINT_CHANGE)
    def refreshInfo(self):
        if not self.widget:
            return
        self.updateRedPotBtns()
        if self.currentTabIndex == uiConst.SUMMON_FRIEND_TAB_INDEX2 and gameglobal.rds.ui.summonFriendBackV2.isBackInValidTime() and gameglobal.rds.ui.summonFriendBackV2.enableRecall():
            p = BigWorld.player()
            p.base.getFriendsRecallData()
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def pushFriendRecallMessage(self):
        if uiConst.MESSAGE_TYPE_SUMMON_FRIEND_RECALL not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SUMMON_FRIEND_RECALL)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SUMMON_FRIEND_RECALL, {'click': self.onPushMsgClick})

    def removeFriendRecallPushMsg(self):
        if uiConst.MESSAGE_TYPE_SUMMON_FRIEND_RECALL in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SUMMON_FRIEND_RECALL)

    def onPushMsgClick(self):
        self.show(uiConst.SUMMON_FRIEND_TAB_INDEX2, 'recallBtn')
        self.removeFriendRecallPushMsg()

    def visiblePotFunBackBtn(self, *args):
        isRedPot = gameglobal.rds.ui.summonFriendBackV2.checkRedFlag()
        return GfxValue(isRedPot)

    def updateRedPotBackBtn(self):
        RedPotManager.updateRedPot(uiConst.SUMMON_FRIEND_BACK_BTN_RED_POT)

    def updateRedPotBtns(self):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        self.updateRedPotBackBtn()
        gameglobal.rds.ui.summonFriendBackV2.updateRedPotRecallBtn()
