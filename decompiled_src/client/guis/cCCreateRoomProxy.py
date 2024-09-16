#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cCCreateRoomProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import gametypes
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy
from ui import unicode2gbk
from guis import uiUtils

class CCCreateRoomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CCCreateRoomProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'getFriendList': self.onGetFriendList,
         'doCreateRoom': self.doCreateRoom,
         'getTitle': self.getTitle}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CC_CREATEROOM, self.closeWidget)

    def reset(self):
        self.dismiss()

    def getTitle(self, *args):
        p = BigWorld.player()
        text = gbk2unicode(const.CC_CREATROOM_TITLE % p.realRoleName)
        return GfxValue(text)

    def doCreateRoom(self, *args):
        source = args[3][0]
        size = 0
        if isinstance(source, GfxValue) and source.GetArraySize() > 0:
            size = source.GetArraySize()
        result = []
        for i in xrange(size):
            result.append(unicode2gbk(source.GetElement(i).GetString()))

        gamelog.debug('jinjj-----doCreateRoom--------', result)
        BigWorld.player().doCreateRoom(result)
        self.closeWidget()

    def onGetFriendList(self, *args):
        p = BigWorld.player()
        friend = p.friend
        friendList = []
        groups = [gametypes.FRIEND_GROUP_FRIEND]
        if gametypes.FRIEND_GROUP_FRIEND in groups:
            for id in friend.groups.iterkeys():
                if friend.isCustomGroup(id):
                    groups.append(id)

        for fVal in friend.itervalues():
            if fVal.state != gametypes.FRIEND_STATE_OFFLINE and not friend.isBlockGroup(fVal.group):
                if fVal.group in groups and fVal.group > 0:
                    friendList.append(gbk2unicode(fVal.name))

        return uiUtils.array2GfxAarry(friendList)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def dismiss(self, *arg):
        if self.isShow:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_CC_CREATEROOM)
        self.isShow = False

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CC_CREATEROOM)
        self.isShow = False

    def show(self):
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CC_CREATEROOM)
        self.isShow = True

    def toggle(self):
        gamelog.debug('jinjj----toggle')
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CC_CREATEROOM)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CC_CREATEROOM)
        self.isShow = not self.isShow
