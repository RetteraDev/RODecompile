#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemSingleTipProxy.o
import Queue
import BigWorld
import gametypes
import gameglobal
import uiConst
import const
import utils
from uiProxy import UIProxy
from guis import events
from guis import menuManager
from guis import richTextUtils
from data import sys_config_data as SCD
MAX_MSG_CACHE = 100
MSG_SHOW_TIME = 5
MSG_SHOW_TIME_MIN = 3
MSG_SHOW_TIME_MAX = 5
MSG_SHOW_DELAY_TIME = 5
MAX_SHOW_TIME_MSG_MAX_LEN = 2
MSG_SHOW_NEED_DELAY_MSG_MAX_LEN = 5

class SystemSingleTipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemSingleTipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handle = None
        self.reset()

    def reset(self):
        self.callbackStartTime = 0
        self.msgCache = []
        self.isTaunted = False
        self.isCongrated = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SYSTEM_SINGLETIP:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SYSTEM_SINGLETIP)
        self.handle and BigWorld.cancelCallback(self.handle)
        self.handle = None

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SYSTEM_SINGLETIP)

    def initUI(self):
        self.widget.tip.addEventListener(events.MOUSE_ROLL_OVER, self.onTipDelayShowStart, False, 0, True)
        self.widget.tip.addEventListener(events.MOUSE_ROLL_OUT, self.onTipDelayShowEnd, False, 0, True)
        self.hideCurrentMsg()

    def addMsg(self, msgId, data, msgData):
        if len(self.msgCache) >= MAX_MSG_CACHE:
            self.msgCache.pop(0)
        self.msgCache.append((msgId, data, msgData))

    def peekMsg(self):
        if not self.msgCache:
            return None
        else:
            return self.msgCache.pop(0)

    def showSysSingleMsg(self, msgId, data, msgData):
        self.addMsg(msgId, data, msgData)
        if not self.widget:
            return
        if self.handle:
            return
        self.showCurrentMsg()
        self.startCallback()

    def updateTipTextCallback(self):
        self.handle and BigWorld.cancelCallback(self.handle)
        if self.msgCache:
            self.showCurrentMsg()
            self.startCallback()
        else:
            self.hideCurrentMsg()
            self.handle = None

    def startCallback(self):
        self.callbackStartTime = utils.getNow()
        msgLen = len(self.msgCache)
        if msgLen <= MAX_SHOW_TIME_MSG_MAX_LEN:
            callbackTime = MSG_SHOW_TIME_MAX
        else:
            callbackTime = MSG_SHOW_TIME_MIN
        self.widget.tip.callbackTime = callbackTime
        self.handle = BigWorld.callback(callbackTime, self.updateTipTextCallback)

    def showCurrentMsg(self):
        if not self.widget:
            return
        self.widget.tip.visible = True
        self.widget.tip.gotoAndPlay(1)
        msg = self.peekMsg()
        if msg:
            msgId, data, msgData = msg
            self.isTaunted = False
            self.isCongrated = False
            self.widget.tip.textMc.textField.htmlText = self.convertMsgText(msgId, data, msgData)

    def hideCurrentMsg(self):
        self.widget.tip.visible = False

    def convertMsgText(self, msgId, data, msgData):
        text = msgData.get('text') % data
        return richTextUtils.parseSysTxt(text)

    def getMenuData(self, roleName, gbId):
        menuManager.getInstance().menuTarget.apply(roleName=roleName, gbId=int(gbId))
        return menuManager.getInstance().getMenuListById(uiConst.MENU_CHAT)

    def privateChat(self, roleName):
        gameglobal.rds.ui.chat.updateChatTarge(roleName)
        gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)

    def taunt(self, ownerGbId):
        p = BigWorld.player()
        msg = SCD.data.get('systemSingleTipMsg', {}).get('taunt', ' ')
        if ownerGbId not in p.members:
            return
        if self.isTaunted:
            return
        self.isTaunted = True
        if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            gameglobal.rds.ui.chat.sendMessage(const.CHAT_CHANNEL_TEAM, msg, add2History=False)
        elif p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            gameglobal.rds.ui.chat.sendMessage(const.CHAT_CHANNEL_GROUP, msg, add2History=False)
        else:
            return

    def congrats(self, ownerGbId):
        p = BigWorld.player()
        msg = SCD.data.get('systemSingleTipMsg', {}).get('congrats', ' ')
        if ownerGbId not in p.members:
            return
        if self.isCongrated:
            return
        self.isCongrated = True
        if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            gameglobal.rds.ui.chat.sendMessage(const.CHAT_CHANNEL_TEAM, msg, add2History=False)
        elif p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            gameglobal.rds.ui.chat.sendMessage(const.CHAT_CHANNEL_GROUP, msg, add2History=False)
        else:
            return

    def onTipDelayShowStart(self, *args):
        if len(self.msgCache) <= MSG_SHOW_NEED_DELAY_MSG_MAX_LEN:
            callbackTime = self.widget.tip.callbackTime
            if not callbackTime:
                callbackTime = MSG_SHOW_TIME
            remainTime = MSG_SHOW_DELAY_TIME + callbackTime - (utils.getNow() - self.callbackStartTime)
            if remainTime > 0:
                self.handle and BigWorld.cancelCallback(self.handle)
                self.handle = BigWorld.callback(remainTime, self.updateTipTextCallback)

    def onTipDelayShowEnd(self, *args):
        callbackTime = self.widget.tip.callbackTime
        if not callbackTime:
            callbackTime = MSG_SHOW_TIME
        remainTime = callbackTime - (utils.getNow() - self.callbackStartTime)
        if remainTime > 0:
            self.handle and BigWorld.cancelCallback(self.handle)
            self.handle = BigWorld.callback(remainTime, self.updateTipTextCallback)
        else:
            self.updateTipTextCallback()
