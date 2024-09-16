#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteChatProxy.o
import BigWorld
import uiConst
import utils
import gameglobal
import events
import re
from helpers import taboo
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import richTextUtils
from guis.asObject import ASUtils
from guis.asObject import MenuManager
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import summon_sprite_personalized_chat_data as SSPCD
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteChatProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteChatProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.chatMsg = ''
        self.chatNo = 0
        self.chatList = []
        self.emotePanel = None
        self.selectChatMc = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_CHAT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_CHAT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_CHAT)

    def reset(self):
        self.spriteIndex = None
        self.chatMsg = ''
        self.chatNo = 0
        self.chatList = []
        self.emotePanel = None
        self.selectChatMc = None

    def show(self, spriteIndex):
        if not gameglobal.rds.configData.get('enableSummonedWarSpriteChat', False):
            return
        if not spriteIndex:
            return
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_CHAT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteChatHelpKey', 0)
        self.widget.chatList.itemRenderer = 'SummonedWarSpriteChat_chatItem'
        self.widget.chatList.barAlwaysVisible = True
        self.widget.chatList.dataArray = []
        self.widget.chatList.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        self.chatList = self.getChatList()
        self.widget.chatList.dataArray = self.chatList
        self.widget.chatList.validateNow()

    def handleResetBtnClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        p.base.resetSpriteChat(self.spriteIndex, self.chatNo)

    def handleCancelBtnClick(self, *args):
        self.updateRepairBtnState(False)

    def handleEmoteBtnClick(self, *args):
        e = ASObject(args[3][0])
        chatMc = e.currentTarget.parent
        self.selectChatMc = chatMc
        self.showEmoteMc(chatMc.parent.idx)

    def handleSaveBtnClick(self, *args):
        e = ASObject(args[3][0])
        chatMc = e.currentTarget.parent
        chatMsg = chatMc.chatEdit.richText
        msg = self.analysisChatMsg(chatMsg)
        p = BigWorld.player()
        result, announcement = taboo.checkDisbWord(msg)
        if richTextUtils.isSysRichTxt(announcement):
            BigWorld.player().showGameMsg(GMDD.data.SPRITE_CHAT_TABOO_WORD, ())
            return
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.SPRITE_CHAT_TABOO_WORD, ())
            return
        result, announcement = taboo.checkBWorld(announcement)
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.SPRITE_CHAT_TABOO_WORD, ())
            return
        if taboo.checkMonitorWord(announcement):
            BigWorld.player().showGameMsg(GMDD.data.SPRITE_CHAT_TABOO_WORD, ())
            return
        p.base.setSpriteChat(self.spriteIndex, self.chatNo, announcement)

    def handleRepairBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.chatNo = target.chatNo
        self.updateRepairBtnState(True)

    def handleChangeWord(self, *args):
        e = ASObject(args[3][0])
        chatMc = e.currentTarget.parent
        chatMsg = e.currentTarget.text
        chatMaxLen = SCD.data.get('spriteChatTextMaxLength', 20)
        num = chatMaxLen - e.currentTarget.textField.length
        if num == 0:
            self.chatMsg = chatMsg
        if num < 0:
            num = 0
            chatMc.chatEdit.text = self.chatMsg
        self.updateWordNum(chatMc, num)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.idx = itemData.idx
        self.updateItem(itemMc, itemData)

    def updateItem(self, itemMc, itemData):
        mcName = 'type%d' % itemData.type
        itemMc.gotoAndStop(mcName)
        if itemData.type == 1:
            chatMc = getattr(itemMc, mcName, None)
            chatMc.titleT.text = itemData.chatName
            chatMaxLen = SCD.data.get('spriteChatTextMaxLength', 20)
            num = chatMaxLen - chatMc.chatEdit.textField.length
            self.updateWordNum(chatMc, num)
            chatMc.resetBtn.addEventListener(events.MOUSE_CLICK, self.handleResetBtnClick, False, 0, True)
            chatMc.saveBtn.addEventListener(events.MOUSE_CLICK, self.handleSaveBtnClick, False, 0, True)
            chatMc.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleCancelBtnClick, False, 0)
            chatMc.emoteBtn.addEventListener(events.MOUSE_CLICK, self.handleEmoteBtnClick, False, 0, True)
            chatMc.chatEdit.addEventListener(events.EVENT_CHANGE, self.handleChangeWord, False, 0, True)
            chatMc.chatNo = itemData.chatNo
        else:
            chatMc = getattr(itemMc, mcName, None)
            chatMc.titleT.text = itemData.chatName
            chatMc.chatRichText.text = ''
            chatMc.chatRichText.appandText(itemData.chats)
            chatMc.chatRichText.validateNow()
            chatMc.chatRichText.height = chatMc.chatRichText.textFiled.textHeight + 10
            ASUtils.setHitTestDisable(chatMc.chatRichText, True)
            chatMc.repairBtn.chatNo = itemData.chatNo
            chatMc.repairBtn.enabled = itemData.repairBtnState
            chatMc.repairBtn.addEventListener(events.MOUSE_CLICK, self.handleRepairBtnClick, False, 0, True)

    def getChatList(self):
        p = BigWorld.player()
        itemList = []
        for i, chatNo in enumerate(sorted(SSPCD.data.keys())):
            val = SSPCD.data.get(chatNo)
            chatName = val.get('name', '')
            defaultChat = val.get('defaultChat', '')
            chatMsg = p.spriteChats.getChatText(self.spriteIndex, chatNo)
            itemInfo = {}
            itemInfo['idx'] = i
            itemInfo['chatName'] = chatName
            itemInfo['chatNo'] = chatNo
            itemInfo['type'] = 0
            itemInfo['repairBtnState'] = True
            itemInfo['chats'] = chatMsg if chatMsg else defaultChat
            itemList.append(itemInfo)

        return itemList

    def analysisChatMsg(self, msg):
        msg = gameglobal.rds.ui.chat.parseMessage(msg)
        reFormat = re.compile('<FONT COLOR=\"#BFB499\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        msg = re.compile('!\\$([0-9]{1})').sub('#\\1', msg)
        msg = re.compile('#([0-9]{1})').sub('!$\\1', msg, uiConst.CHAT_MAX_FACE_CNT)
        msg = re.compile('\"!\\$([A-Fa-f0-9]{6})\"').sub('\"#\\1\"', msg)
        return msg

    def delFont(self, matchobj):
        return matchobj.group(1)

    def updateWordNum(self, chatMc, num):
        color = "<font color = \'#6de539\'>"
        if num == 0:
            color = "<font color = \'#f43804\'>"
        showStr = gameStrings.JIEQI_NICKNAME_WORD_NUM % (color, num, 20)
        chatMc.leftT.htmlText = showStr

    def updateRepairBtnState(self, isRepair):
        if not self.widget:
            return
        for itemInfo in self.chatList:
            itemInfo['type'] = 0
            if isRepair:
                itemInfo['repairBtnState'] = False
                if self.chatNo == itemInfo['chatNo']:
                    itemInfo['repairBtnState'] = True
                    itemInfo['type'] = 1
            else:
                itemInfo['repairBtnState'] = True
                if self.chatNo == itemInfo['chatNo']:
                    itemInfo['type'] = 0

        self.widget.chatList.dataArray = self.chatList
        self.widget.chatList.validateNow()

    def showEmoteMc(self, idx):
        self.selectChatMc.chatEdit.addEventListener(events.EVENT_HEIGHT_CHANGE, self.refreshTxtPosHandler, False, 0, True)
        self.emotePanel = self.widget.getInstByClsName('SummonedWarSpriteChat_chatFacePanel')
        self.emotePanel.addEventListener(events.FACE_CLICK, self.handleFaceClick, False, 0, True)
        pos = self.widget.chatList.getIndexPosY(idx)
        MenuManager.getInstance().showMenu(self.selectChatMc.emoteBtn, self.emotePanel, {'x': self.selectChatMc.emoteBtn.x + 15,
         'y': pos + 100 - self.emotePanel.height}, False, self.widget)

    def handleFaceClick(self, *args):
        if not self.selectChatMc:
            return
        if self.selectChatMc.chatNo != self.chatNo:
            return
        e = ASObject(args[3][0])
        faceStr = utils.faceIdToString(int(e.data))
        self.selectChatMc.chatEdit.insertRichText(faceStr)
        self.selectChatMc.chatEdit.focused = 1
        MenuManager.getInstance().hideMenu()

    def refreshTxtPosHandler(self, *args):
        metris = self.selectChatMc.chatEdit.textField.getLineMetrics(self.selectChatMc.chatEdit.textField.numLines - 1)
        if self.selectChatMc.chatEdit.textField.length == 0:
            self.selectChatMc.chatEdit.y = self.selectChatMc.textBg.y + self.selectChatMc.textBg.height - self.selectChatMc.chatEdit.height
        else:
            self.selectChatMc.chatEdit.y = self.selectChatMc.textBg.y + self.selectChatMc.textBg.height - self.selectChatMc.chatEdit.height + metris.descent + metris.leading - 8

    def saveChatSucc(self, index, chatNo, text):
        if not self.widget:
            return
        if self.spriteIndex != index:
            return
        for itemInfo in self.chatList:
            itemInfo['repairBtnState'] = True
            if chatNo == itemInfo['chatNo']:
                itemInfo['type'] = 0
                itemInfo['chats'] = text

        self.widget.chatList.dataArray = self.chatList
        self.widget.chatList.validateNow()

    def resetChatSucc(self, index, chatNo):
        if not self.widget:
            return
        if self.spriteIndex != index:
            return
        for itemInfo in self.chatList:
            itemInfo['repairBtnState'] = True
            if chatNo == itemInfo['chatNo']:
                itemInfo['type'] = 0
                itemInfo['chats'] = SSPCD.data.get(chatNo, {}).get('defaultChat', '')

        self.widget.chatList.dataArray = self.chatList
        self.widget.chatList.validateNow()
