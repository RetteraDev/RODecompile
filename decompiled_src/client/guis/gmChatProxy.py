#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gmChatProxy.o
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gametypes
import const
import clientcom
import ui
from uiProxy import UIProxy
from guis import uiUtils
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from callbackHelper import Functor

class GmChatProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GmChatProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickIcon': self.onClickIcon,
         'clickClose': self.onClickClose,
         'sendMsgToGM': self.onSendMsgToGM,
         'getInit': self.onGetInit,
         'linkLeftClick': self.onLinkLeftClick}
        self.gmChatMediator = None
        self.gmChatPanelMediator = None
        self.gmchatType = uiConst.GM_CAHT_HIDE
        self.msgs = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GM_CHAT:
            self.gmChatMediator = mediator
            self.setState(self.gmchatType)
        elif widgetId == uiConst.WIDGET_GM_CHAT_PANEL:
            self.gmChatPanelMediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.gmChatPanelMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GM_CHAT_PANEL)

    def reset(self):
        super(self.__class__, self).reset()
        self.msgs = []
        self.gmchatType = uiConst.GM_CAHT_HIDE

    def onGetInit(self, *arg):
        for msg in self.msgs:
            self.gmChatPanelMediator.Invoke('addMsg', msg)

    def onLinkLeftClick(self, *arg):
        linkText = unicode2gbk(arg[3][0].GetString())
        if linkText[:3] == 'net':
            BigWorld.openUrl('http://' + linkText[3:])

    def onClickIcon(self, *arg):
        if not self.gmChatPanelMediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GM_CHAT_PANEL)
            self.setState(uiConst.GM_CAHT_NORMAL)

    def onClickClose(self, *arg):
        self.hide(False)

    def onSendMsgToGM(self, *arg):
        msg = arg[3][0].GetString()
        msg = uiUtils.parseMsg(unicode2gbk(msg))
        BigWorld.player().base.chatToGM(msg)

    def sendMsgToGM(self, msg):
        msgObject = self.msgToGfxVlaue(msg)
        self.msgs.append(msgObject)
        if self.gmChatPanelMediator:
            self.gmChatPanelMediator.Invoke('addMsg', msgObject)

    @ui.checkWidgetLoaded(uiConst.WIDGET_GM_CHAT)
    def setState(self, state):
        self.gmchatType = state
        if self.gmChatMediator:
            self.gmChatMediator.Invoke('setState', GfxValue(state))

    def receiveMsg(self, msg):
        msgObject = self.msgToGfxVlaue(msg, False)
        self.msgs.append(msgObject)
        if self.gmChatPanelMediator:
            self.gmChatPanelMediator.Invoke('addMsg', msgObject)
        else:
            self.setState(uiConst.GM_CAHT_ACTIVE)

    def msgToGfxVlaue(self, msg, isMe = True):
        gfxMsg = self.movie.CreateObject()
        gfxMsg.SetMember('isMe', GfxValue(isMe))
        gfxMsg.SetMember('time', GfxValue(time.time()))
        gfxMsg.SetMember('msg', GfxValue(gbk2unicode(msg)))
        p = BigWorld.player()
        if isMe:
            gfxMsg.SetMember('name', GfxValue(gbk2unicode(p.realRoleName)))
            photo = p._getFriendPhoto(p)
            if uiUtils.isDownloadImage(photo):
                imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                if not clientcom.isFileExist(imagePath):
                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
                else:
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            gfxMsg.SetMember('photo', GfxValue(photo))
        else:
            gfxMsg.SetMember('name', GfxValue(gbk2unicode('GM')))
            gfxMsg.SetMember('photo', GfxValue('headIcon/32.dds'))
        return gfxMsg

    def onDownloadPhoto(self, status, callbackArgs):
        pass
