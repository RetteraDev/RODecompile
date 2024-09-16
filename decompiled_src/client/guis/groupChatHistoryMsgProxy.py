#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupChatHistoryMsgProxy.o
import BigWorld
import gamelog
import gameglobal
import time
from uiProxy import UIProxy
from guis import events
from guis import uiConst
from guis.asObject import ASObject
from guis.asObject import RichItemConst

class GroupChatHistoryMsgProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupChatHistoryMsgProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUP_CHAT_HISTORY_MSG, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUP_CHAT_HISTORY_MSG:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GROUP_CHAT_HISTORY_MSG)
        gameglobal.rds.ui.groupChatRoom.clearHistroyNum()
        gameglobal.rds.ui.chatToFriend.onCloseHistory()

    def reset(self):
        self.fid = 0
        self.groupNUID = 0
        self.historyMsg = []
        self.totalPage = 0
        self.currentPage = 0
        self.lastHistoryBottom = 0
        self.isGroupChat = False

    def show(self, fid = 0, historyMsg = None, totalPage = 1, currentPage = 1, groupNUID = 0):
        if not historyMsg:
            historyMsg = []
        gfxMsg = []
        for msg in historyMsg:
            gfxMsg.append(gameglobal.rds.ui.groupChat.setPMsgData(None, msg))

        self.fid = int(fid)
        self.groupNUID = int(groupNUID)
        self.isGroupChat = True if self.groupNUID else False
        self.historyMsg = gfxMsg
        self.totalPage = int(totalPage)
        self.currentPage = int(currentPage)
        if self.widget:
            self.refreshInfo()
            return
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GROUP_CHAT_HISTORY_MSG)
            return

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.counter.maxCount = self.totalPage
        self.widget.counter.count = self.currentPage
        self.widget.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateHistoryMsg()

    def handleCountChange(self, *arg):
        e = ASObject(arg[3][0])
        self.currentPage = int(self.widget.counter.count)
        if not self.isGroupChat:
            gameglobal.rds.ui.chatToFriend._getHistoryByFid(self.fid, 0, self.currentPage)
        else:
            gameglobal.rds.ui.groupChatRoom.getHistoryByNuId(self.groupNUID, self.currentPage)

    def updateHistoryMsg(self):
        self.widget.removeAllInst(self.widget.msgHistoryScollWnd.canvas)
        lastHistory = 0
        for msg in self.historyMsg:
            nameTxt = self.widget.getInstByClsName('GroupChatHistoryMsg_HistoryMsgName')
            self.widget.msgHistoryScollWnd.canvas.addChild(nameTxt)
            nameTxt.playNameText.tf.width = 200
            nameTxt.playNameText.text = str(msg.get('name', ''))
            nameTxt.timeTextField.text = time.strftime('%m-%d %H:%M', time.localtime(msg.get('time', 0)))
            nameTxt.timeTextField.x = nameTxt.playNameText.tf.textWidth + 12
            contentTxt = self.widget.getInstByClsName('GroupChatHistoryMsg_HistoryMsgContent')
            contentTxt.setParsers([RichItemConst.MP_PARSER, RichItemConst.RED_PACKET_PARSER, RichItemConst.SOUND_RECORD_PARSER])
            self.widget.msgHistoryScollWnd.canvas.addChild(contentTxt)
            contentTxt.appandText(str(msg.get('msg', '')))
            contentTxt.validateNow()
            contentTxt.height = contentTxt.textFiled.textHeight + 10
            nameTxt.y = lastHistory
            contentTxt.y = nameTxt.y + nameTxt.height - 6
            lastHistory = contentTxt.y + contentTxt.height - 2

        self.widget.msgHistoryScollWnd.refreshHeight(self.widget.msgHistoryScollWnd.canvas.height + 4)
        self.widget.msgHistoryScollWnd.scrollToEnd()
