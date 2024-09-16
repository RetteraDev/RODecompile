#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemMessageProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import math
import utils
import time
import gamelog
import const
from guis.asObject import ASObject
from uiProxy import UIProxy
from gameStrings import gameStrings
from data import game_msg_data as GMD
SYSTEM_MESSAGE_DEFAULT_PATH = 'systemMessageIcon/systemMsgSmall.dds'

class SystemMessageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemMessageProxy, self).__init__(uiAdapter)
        self.widget = None
        self.curPage = 1
        self.totalPage = 1
        self.systemMsgList = []
        self.tempMsgList = []
        self.recordSystemNewMsg = []
        self.historyMsgNum = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SYSTEM_MESSAGE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SYSTEM_MESSAGE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if not gameglobal.rds.configData.get('enableSystemMessage', False):
            return
        enableChatGroup = gameglobal.rds.configData.get('enableChatGroup', False)
        if self.widget:
            self.refreshInfo()
            return
        if enableChatGroup and gameglobal.rds.ui.groupChat.checkCurrentChated(const.FRIEND_SYSTEM_NOTIFY_ID):
            gameglobal.rds.ui.groupChat.appendNewSystemNotifyMsg()
            return
        if not enableChatGroup:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SYSTEM_MESSAGE)
        else:
            gameglobal.rds.ui.groupChat.addSystemMsgItem()

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SYSTEM_MESSAGE)

    def reset(self):
        self.curPage = 1
        self.totalPage = 1
        self.recordSystemNewMsg = []
        self.historyMsgNum = 0
        self.tempMsgList = []

    def clearTempMsg(self):
        self.tempMsgList = []

    def initUI(self, *args):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.pageInput.textField.restrict = '0-9'
        self.widget.pageInput.addEventListener(events.EVENT_CHANGE, self.handleInputPage, False, 0, True)
        self.widget.lastBtn.addEventListener(events.BUTTON_CLICK, self.handleLastBtnClick, False, 0, True)
        self.widget.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)
        self.widget.headBtn.addEventListener(events.BUTTON_CLICK, self.handleHeadBtnClick, False, 0, True)
        self.widget.tailBtn.addEventListener(events.BUTTON_CLICK, self.handleTailBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.getSystemNotifyInfo(self.curPage)

    def handleLastBtnClick(self, *args):
        if self.curPage > 1:
            self.curPage = self.curPage - 1
            self.getSystemNotifyInfo(self.curPage)

    def handleNextBtnClick(self, *args):
        if self.curPage < self.totalPage:
            self.curPage = self.curPage + 1
            self.getSystemNotifyInfo(self.curPage)

    def handleInputPage(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.text == '':
            e.currentTarget.text = '1'
        page = int(e.currentTarget.text)
        if page < 1:
            page = 1
        elif page > self.totalPage:
            page = self.totalPage
        e.currentTarget.text = str(page)
        self.curPage = page
        self.getSystemNotifyInfo(self.curPage)

    def appendNewSystemNotifyMsg(self):
        if not self.widget:
            return
        offSet = (self.totalPage - self.curPage) * uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
        limit = min(uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM, self.historyMsgNum - offSet + 1)
        p = BigWorld.player()
        p.fetchSystemNotifyHistory(p.gbId, int(offSet), int(limit))

    def getSystemNotifyInfo(self, pageNum):
        if pageNum and self.historyMsgNum:
            totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
            offSet = (totalPage - pageNum) * uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
            limit = min(uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM, self.historyMsgNum - offSet)
        else:
            offSet = 0
            limit = uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
        p = BigWorld.player()
        p.fetchSystemNotifyHistory(p.gbId, int(offSet), int(limit))

    def appendSystemNotifyHistoryMsg(self, gbId, msgs, total, offset, limit):
        if gameglobal.rds.configData.get('enableChatGroup', False) and gameglobal.rds.ui.groupChat.checkCurrentChated(const.FRIEND_SYSTEM_NOTIFY_ID):
            gameglobal.rds.ui.groupChat.appendSystemNotifyHistoryMsg(gbId, msgs, total, offset, limit)
            return
        self.historyMsgNum = total
        totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
        currentPage = totalPage - math.ceil(offset / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
        p = BigWorld.player()
        gfxMsg = []
        for msg in msgs:
            msgId = msg.get('msgId', 0)
            time = msg.get('time', 0)
            args = msg.get('args', [])
            args = self.changeCoding(args)
            text = p.getLinkText(args, GMD.data.get(msgId, {}))
            try:
                msgInfo = p.formatMsg(text, args)
            except:
                gamelog.debug('systemMssage error', text, args)
                continue

            sysTypeIcon = GMD.data.get(msgId, {}).get('sysTypeIcon', SYSTEM_MESSAGE_DEFAULT_PATH)
            gfxMsg.append({'msgId': msgId,
             'time': time,
             'msg': msgInfo,
             'sysTypeIcon': sysTypeIcon})

        self.systemMsgList = []
        self.systemMsgList = gfxMsg
        self.totalPage = max(int(totalPage), 1)
        self.curPage = max(int(currentPage), 1)
        self.updateSystemMsgList()
        self.updatePageStepper()

    def appendTempSystemNotifyMsg(self, msg, msgId):
        msgTime = msg.get('time', utils.getNow())
        self.reocrdSystemNewMsg(msgId, msgTime)
        self.tempMsgList.append(msg)

    def changeCoding(self, args):
        changeArgs = []
        for v in args:
            if isinstance(v, unicode):
                v = v.encode(utils.defaultEncoding())
            changeArgs.append(v)

        return tuple(changeArgs)

    def updateSystemMsgList(self):
        self.widget.removeAllInst(self.widget.msgList.canvas)
        cutLine = self.widget.getInstByClsName('SystemMessage_CutLine')
        bFirstNewMsg = False
        bHistoryMsg = False
        posY = 0
        if self.tempMsgList:
            self.systemMsgList.extend(self.tempMsgList)
        for tInfo in self.systemMsgList:
            itemMc = self.widget.getInstByClsName('SystemMessage_SystemMsgInfo')
            if (tInfo.get('msgId', 0), tInfo.get('time', 0)) in self.recordSystemNewMsg:
                if not bFirstNewMsg:
                    bFirstNewMsg = True
                    if bHistoryMsg:
                        cutLine.y = posY + 10
                        posY += cutLine.height
                        cutLine.gotoAndStop('cutLine1')
                        self.widget.msgList.canvas.addChild(cutLine)
                itemMc.gotoAndStop('newMsg')
            else:
                bHistoryMsg = True
                itemMc.gotoAndStop('historyMsg')
            path = tInfo.get('sysTypeIcon', SYSTEM_MESSAGE_DEFAULT_PATH)
            itemMc.head.icon.clear()
            itemMc.head.icon.loadImage(path)
            itemMc.nameTxt.text = gameStrings.SYSTEM_MESSAGE_FRIEND_NAME
            itemMc.time.text = self.getSystemMsgTimeStr(tInfo.get('time', 0))
            itemMc.msg.text = tInfo.get('msg', '')
            itemMc.msg.height = itemMc.msg.textFiled.textHeight + 10
            itemMc.time.x = itemMc.msg.x + itemMc.msg.width - itemMc.time.textWidth - 12
            lineEnd = itemMc.msg.textFiled.numLines - 1
            endIndex = itemMc.msg.textFiled.getLineOffset(lineEnd) + itemMc.msg.textFiled.getLineLength(lineEnd) - 1
            endWordRect = itemMc.msg.textFiled.getCharBoundaries(endIndex)
            endlineWidth = endWordRect.x + endWordRect.width if endWordRect else 0
            if endlineWidth + itemMc.time.textWidth + 12 <= itemMc.msg.tf.width:
                itemMc.time.y = itemMc.msg.y + itemMc.msg.textFiled.textHeight - itemMc.time.textHeight
                itemMc.bg.height = itemMc.msg.y + itemMc.msg.height
            else:
                itemMc.time.y = itemMc.msg.y + itemMc.msg.textFiled.textHeight + 10
                itemMc.bg.height = itemMc.msg.y + itemMc.msg.height + itemMc.time.height
            itemMc.y = posY
            posY += itemMc.height
            self.widget.msgList.canvas.addChild(itemMc)

        if not bFirstNewMsg and self.curPage == self.totalPage:
            cutLine.y = posY + 10
            cutLine.gotoAndStop('cutLine2')
            self.widget.msgList.canvas.addChild(cutLine)
        self.widget.msgList.refreshHeight()
        self.widget.msgList.scrollToEnd()

    def updatePageStepper(self):
        self.widget.pageText.text = '/%d' % self.totalPage
        self.widget.pageInput.text = self.curPage
        self.widget.headBtn.enabled = self.curPage != 1 and self.totalPage != 1
        self.widget.lastBtn.enabled = self.curPage > 1 and self.totalPage != 1
        self.widget.nextBtn.enabled = self.curPage < self.totalPage and self.totalPage != 1
        self.widget.tailBtn.enabled = self.curPage != self.totalPage and self.totalPage != 1

    def handleHeadBtnClick(self, *args):
        if self.curPage != 1:
            self.curPage = 1
            self.getSystemNotifyInfo(self.curPage)

    def handleTailBtnClick(self, *args):
        if self.curPage != self.totalPage:
            self.curPage = self.totalPage
            self.getSystemNotifyInfo(self.curPage)

    def getSystemMsgTimeStr(self, messageTime):
        return time.strftime('%m-%d %H:%M:%S', utils.localtimeEx(messageTime))

    def reocrdSystemNewMsg(self, msgId, createdTime):
        self.recordSystemNewMsg.append((msgId, createdTime))
