#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/selectFriendProxy.o
import BigWorld
import gameglobal
from guis import events
from guis import uiConst
from guis.asObject import ASObject
from guis.asObject import ASUtils
from ui import gbk2unicode
from ui import unicode2gbk
from uiUtils import array2GBKArray
from uiProxy import UIProxy
GROUP_HEIGHT = 23
ITEM_HEIGHT = 35

class SelectFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SelectFriendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.confirmCallback = None
        self.selectedFriends = set([])
        uiAdapter.registerEscFunc(uiConst.WIDGET_SELECT_FRIEND, self.onClose)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SELECT_FRIEND:
            self.widget = widget
            self.initUI()

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *args):
        if self.confirmCallback:
            self.confirmCallback(self.selectedFriends)
        self.hide()

    def onCancel(self, *args):
        self.hide()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SELECT_FRIEND)
        self.reset()

    def show(self, callback):
        self.confirmCallback = callback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SELECT_FRIEND)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirm, False, 1, True)
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCancel, False, 1, True)
        friendsView = self.widget.friendsView
        friendsView.tree.itemHeights = [GROUP_HEIGHT, ITEM_HEIGHT]
        friendsView.tree.lvItemGap = 2
        friendsView.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleExpandChanged)
        groups = BigWorld.player().getMiniGameInviteGroup()
        info = gameglobal.rds.ui.friend._getFriendListData(groups, gameglobal.FRIENDS_ALL, True, True)
        self.setFriendsList(info)

    def selectFriend(self, select, gbId):
        if select:
            self.selectedFriends.add(gbId)
        elif gbId in self.selectedFriends:
            self.selectedFriends.remove(gbId)

    def handleExpandChanged(self, *args):
        pass

    def setFriendsList(self, friendInfoList):
        if not self.widget:
            return
        if self.widget.friendsView:
            self.widget.friendsView.tree.itemRenderers = ['SelectFriend_GroupBtn', 'SelectFriend_IMPlayerItem']
            self.widget.friendsView.tree.itemHeights = [GROUP_HEIGHT, ITEM_HEIGHT]
            self.widget.friendsView.tree.labelFunction = self.friendsLabelFunction
            friendInfoList = array2GBKArray(friendInfoList)
            self.widget.friendsView.tree.dataArray = friendInfoList

    def friendsLabelFunction(self, *args):
        itemMc = ASObject(args[3][0])
        childData = ASObject(args[3][1])
        isFirst = args[3][2].GetBool()
        if isFirst:
            itemMc.icon.visible = True
            itemMc.btn.num.visible = True
            itemMc.btn.label = childData.name
            itemMc.btn.num.text = childData.num
        else:
            self.friendsSecondLabelFunction(itemMc, childData, isFirst)

    def friendsSecondLabelFunction(self, item, data, isFrist):
        if item:
            item.setData(data, 0)
            item.validateNow()

    def reset(self):
        self.confirmCallback = None
        self.selectedFriends = set([])
