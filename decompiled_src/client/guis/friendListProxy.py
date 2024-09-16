#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/friendListProxy.o
import BigWorld
import uiUtils
from uiProxy import UIProxy
from guis import uiConst
from data import photo_border_data as PBD

class FriendListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FriendListProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFriendData': self.onGetFriendData}
        uiAdapter.registerEscFunc(uiConst.WIDGET_FRIEND_LIST, self.hide)
        self.reset()
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FRIEND_LIST:
            self.mediator = mediator

    def onGetFriendData(self, *arg):
        if self.data:
            return uiUtils.array2GfxAarry(self.data, True)

    def show(self, data):
        self.data = data
        for i, info in enumerate(self.data):
            photo = info.get('photo', None)
            hostId = 0
            if photo and photo.find('##') != -1:
                photo, hostId = photo.split('##')
                hostId = int(hostId)
            info['photo'] = photo
            info['hostId'] = hostId
            info['photoBorderIcon'] = info.get('photoBorderIcon', '')

        self.data.reverse()
        if len(self.data) < 7:
            for n in xrange(len(self.data), 7):
                item = {'isShow': 0}
                self.data.append(item)

        if not self.mediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FRIEND_LIST)
        else:
            self.mediator.Invoke('refreshData', uiUtils.array2GfxAarry(self.data, True))

    def clearWidget(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FRIEND_LIST)

    def reset(self):
        self.data = []
