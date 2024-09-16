#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pushNoticeProxy.o
import time
import uiConst
from uiProxy import UIProxy
from guis import uiUtils

class PushNoticeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PushNoticeProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUSH_NOTICE, self.hide)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PUSH_NOTICE:
            self.med = mediator
            if self.content:
                return uiUtils.dict2GfxDict(self.content, True)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUSH_NOTICE)

    def reset(self):
        self.med = None
        self.content = None

    def show(self, *args):
        if len(args) == 1:
            self.content = args[0]
            if self.med:
                self.med.Invoke('refreshContent', uiUtils.dict2GfxDict(self.content, True))
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_PUSH_NOTICE)

    def addPushNotice(self, icon, tip, title, content, name, timeStamp, sound = 404):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_NOTICE_PUSH)
        pushInfo = {'iconId': icon,
         'tooltip': tip,
         'soundIdx': sound}
        pushData = {'title': title,
         'desc': content,
         'name': name,
         'time': time.strftime('%Y.%m.%d', time.localtime(timeStamp))}
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_NOTICE_PUSH, {'data': pushData}, pushInfo)

    def clickPushNotice(self):
        data = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_SPC_GMT_NOTICE_PUSH)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_NOTICE_PUSH)
        if data:
            self.show(data.get('data', ''))
