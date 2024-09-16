#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chatRoomWindowProxy.o
from gamestrings import gameStrings
import re
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import utils
import uiUtils
import gametypes
from helpers import taboo
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from item import Item
from cdata import game_msg_def_data as GMDD

class ChatRoomWindowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChatRoomWindowProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickMin': self.onClickMin,
         'getInitData': self.getInitData,
         'clickSetting': self.onClickSetting,
         'chatToChatRoom': self.onChatToChatRoom,
         'linkLeftClick': self.onLinkLeftClick}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHATROOM_WINDOW, self.closeMsg)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHATROOM_WINDOW:
            self.mediator = mediator

    def show(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_CHATROOM):
            return
        if self.mediator:
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CHATROOM_WINDOW, True)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHATROOM_WINDOW)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHATROOM_WINDOW)

    def reset(self):
        super(self.__class__, self).reset()

    def getInitData(self, *arg):
        self.refreshInfo()
        p = BigWorld.player()
        if p.chatRoom:
            return GfxValue(gbk2unicode(BigWorld.player().chatRoom.fName))
        return GfxValue('')

    def delFont(self, matchobj):
        return matchobj.group(1)

    def onChatToChatRoom(self, *arg):
        p = BigWorld.player()
        msg = arg[3][0].GetString()
        msg = uiUtils.parseMsg(unicode2gbk(msg))
        reFormat = re.compile('<FONT COLOR=\"#FFFFE6\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        rawMsg = re.sub('</?FONT.*?>', '', msg, 0, re.DOTALL)
        if utils.isEmpty(rawMsg):
            p.showGameMsg(GMDD.data.CHATROOM_MSG_EMPTY, ())
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.CHATROOM_MSG_TABOO, ())
            return
        p.cell.chatToChatRoom(msg)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if p.chatRoom:
                data = []
                for member in p.chatRoom.member.itervalues():
                    data.append([str(member.gbId),
                     member.role,
                     member.school,
                     member.level,
                     member.roleId == gametypes.CHATROOM_ROLE_LEADER,
                     member.tJoin])

                self.mediator.Invoke('refreshInfo', uiUtils.array2GfxAarry(sorted(data, key=lambda e: e[5]), True))

    def memberLevelUpdate(self, gbId, memberLv):
        p = BigWorld.player()
        if self.mediator and p.chatRoom:
            if gbId in p.chatRoom.member:
                self.mediator.Invoke('memberLevelUpdate', (GfxValue(str(gbId)), GfxValue(memberLv)))

    def memberRename(self, gbId, memberName):
        p = BigWorld.player()
        if self.mediator and p.chatRoom:
            if gbId in p.chatRoom.member:
                self.mediator.Invoke('memberRename', (GfxValue(str(gbId)), GfxValue(gbk2unicode(memberName))))

    def memberAppoint(self, gbId):
        p = BigWorld.player()
        if self.mediator and p.chatRoom:
            if gbId in p.chatRoom.member:
                self.mediator.Invoke('memberAppoint', GfxValue(str(gbId)))

    def clickPushIcon(self):
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_CHATROOM, {'data': 'data'})
        self.show()

    def onClickClose(self, *arg):
        self.closeMsg()

    def onClickSetting(self, *arg):
        p = BigWorld.player()
        if p.chatRoom.rHeader == p.gbId:
            p.cell.getChatRoomData()

    def closeMsg(self):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_CHATROOMWINDOWPROXY_124, self.close)

    def close(self):
        BigWorld.player().cell.leaveChatRoom()
        self.hide()

    def onClickMin(self, *arg):
        if not gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_CHATROOM):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CHATROOM, {'data': 'data'})
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CHATROOM_WINDOW, False)

    def appenInputMsg(self, msg):
        if self.mediator:
            self.mediator.Invoke('appendInputMsg', GfxValue(gbk2unicode(msg)))

    def onLinkLeftClick(self, *arg):
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][0].GetString())
        if roleName[:3] == 'ret':
            retCode = int(roleName[3:])
            p.base.chatToItem(retCode, 'chatRoom')
        elif roleName[:4] == 'item':
            self.showTooltip(const.CHAT_TIPS_ITEM, gameglobal.rds.ui.inventory.GfxToolTip(Item(int(roleName[4:]), 1, False)))
        elif roleName[:4] == 'task':
            self.showTooltip(const.CHAT_TIPS_TASK, gameglobal.rds.ui.chat.taskToolTip(int(roleName[4:])))
        elif roleName[:4] == 'achv':
            self.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, gameglobal.rds.ui.chat.achieveToolTip(roleName[4:]))
        elif roleName.startswith('sprite'):
            p.base.chatToSprite(int(roleName[len('sprite'):]), 'chatRoom')

    def showTooltip(self, tipsType, gfxTipData):
        if self.mediator:
            self.mediator.Invoke('showTooltip', (GfxValue(tipsType), gfxTipData))

    def receiveMsg(self, gbId, msg):
        p = BigWorld.player()
        if self.mediator and p.chatRoom and gbId in p.chatRoom.member:
            member = p.chatRoom.member[gbId]
            m = p._createChatMsg(gbId, member.role, member.school, member.sex, msg, utils.getNow())
            self.mediator.Invoke('addMsg', gameglobal.rds.ui.chatToFriend.msgToGfxVlaue(m))

    def updateName(self):
        if self.mediator:
            self.mediator.Invoke('updateName', GfxValue(gbk2unicode(BigWorld.player().chatRoom.fName)))
