#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFbMessageBoard.o
import cPickle
import zlib
import json
import os
import utils
from guis import uiUtils
import gamelog
import gametypes
import gameglobal
import time
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from commonMessageBoard import EventVal, MsgVal, FbMessageBoardItem
from helpers.messageBoard import FbMessageBoard

class ImpFbMessageBoard(object):

    def onLoadFbMessageBoardInfo(self, info):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@jinjj messageBoard#onLoadFbMessageBoardInfo:', info)
        self.fbMessageBoard = FbMessageBoard().fromDTO(info)

    def onResetFbMessageBoard(self):
        if hasattr(self, 'fbMessageBoard'):
            if self.fbMessageBoard.publishType != 0:
                self.tempFbMessageBoard = self.fbMessageBoard
        self.fbMessageBoard = FbMessageBoard()
        self.saveTempBoardMessage()

    def onUpdateFbMessageBoard(self, dto):
        self.fbMessageBoard.updateMessageBoard(dto)

    def onUpdateFbMessageBoardPublishType(self, publishType):
        self.fbMessageBoard.publishType = publishType

    def onFbMessageBoardEvent(self, event):
        gamelog.debug('@hjx messageBoard#onMessageBoardEvent:', event)
        event = EventVal().fromDTO(event)
        self.showGameMsg(event.msgId, event.args)
        self.fbMessageBoard.addEvent(event)
        self.fbMessageBoard.sortEvent()

    def onQueryFbMessageBoardMsgs(self, msgs, version):
        msgs = cPickle.loads(zlib.decompress(msgs))
        self.messageBoardMsgs = msgs
        self.messageBoardChatVersion = version
        self.queryMessageBoardChatTime = time.time()
        gamelog.debug('@hjx messageBoard#onQueryMessageBoardMsgs:', msgs)
        self.fbMessageBoard.recoverMsgs(msgs)

    def onFbMessageBoardMsg(self, msg):
        gamelog.debug('@hjx messageBoard#onMessageBoardMsg:', msg)
        if not getattr(self, 'messageBoardMsgs', None):
            self.messageBoardMsgs = []
        self.messageBoardMsgs.append(msg)
        msg = MsgVal().fromDTO(msg)
        self.fbMessageBoard.addMsg(msg)
        self.fbMessageBoard.sortMsg()

    def onQueryFbMessageBoardInfo(self, messageBoardInfo, version):
        messageBoardInfo = cPickle.loads(zlib.decompress(messageBoardInfo))
        gamelog.debug('@jinjj messageBoard#onQueryMessageBoardInfo:', messageBoardInfo)
        self.messageBoardVersion = version
        self.messageBoardInfo = messageBoardInfo
        self.queryMessageBoardTime = time.time()

    def onUpdateFbMessageBoardConnection(self, op, gbId, messageBoadItem):
        gamelog.debug('@hjx messageBoard#onUpdateFbMessageBoardConnection:', op, gbId, messageBoadItem)
        if op == gametypes.FB_MESSAGE_BOARD_CONNECTION_OP_PUSH:
            messageBoadItem = FbMessageBoardItem().fromDTO(messageBoadItem)
            self.fbMessageBoard.addConnection(gbId, messageBoadItem)
        elif op == gametypes.FB_MESSAGE_BOARD_CONNECTION_OP_POP:
            self.fbMessageBoard.connections.pop(gbId, None)
        elif op == gametypes.FB_MESSAGE_BOARD_CONNECTION_OP_UPDATE:
            messageBoadItem = FbMessageBoardItem().fromDTO(messageBoadItem)
            self.fbMessageBoard.addConnection(gbId, messageBoadItem)
        elif op == gametypes.FB_MESSAGE_BOARD_CONNECTION_OP_LOGOFF:
            self.fbMessageBoard.updateConnectionOnlineStatus(gbId, False)
        elif op == gametypes.FB_MESSAGE_BOARD_CONNECTION_OP_LOGON:
            self.fbMessageBoard.updateConnectionOnlineStatus(gbId, True)

    def onFbMessageBoardApplyConnectionOvertime(self, gbIds):
        gamelog.debug('@hjx messageBoard#onFbMessageBoardApplyConnectionOvertime:', gbIds)
        for gbId in gbIds:
            self.fbMessageBoard.connections.pop(gbId, None)

    def saveTempBoardMessage(self):
        if hasattr(self, 'tempFbMessageBoard') and self.tempFbMessageBoard != None:
            hasMsg = self.tempFbMessageBoard.publishType
            if not hasMsg:
                return
        else:
            return
        if not os.path.isdir('messageBoard'):
            os.mkdir('messageBoard')
        f = open('messageBoard/%d' % self.gbId, 'w')
        if f:
            data = {}
            p = self
            data['publishType'] = p.tempFbMessageBoard.publishType
            data['fbNo'] = p.tempFbMessageBoard.fbNo
            data['hard'] = p.tempFbMessageBoard.hard
            data['hasNum'] = p.tempFbMessageBoard.hasNum
            data['challengeWeekList'] = p.tempFbMessageBoard.challengeWeekList
            data['challengeTimeStr'] = p.tempFbMessageBoard.challengeTimeStr
            data['desc'] = p.tempFbMessageBoard.desc
            data['num'] = p.tempFbMessageBoard.num
            data_string = json.dumps(data, encoding=utils.defaultEncoding())
            f.write(data_string)
            f.close()
