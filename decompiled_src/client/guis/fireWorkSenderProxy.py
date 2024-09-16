#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fireWorkSenderProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from callbackHelper import Functor
from guis.uiProxy import UIProxy
from ui import unicode2gbk
from ui import gbk2unicode
from helpers import taboo
from item import Item
from cdata import game_msg_def_data as GMDD

class FireWorkSenderProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FireWorkSenderProxy, self).__init__(uiAdapter)
        self.modelMap = {'sendInfo': self.onSendInfo,
         'getName': self.onGetName}
        self.mediator = None
        self.targetName = ''
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIRE_WORK, self.clearWidget)

    def clearWidget(self):
        self.mediator = None
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        self.targetName = ''
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FIRE_WORK)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, name = '', usePage = const.CONT_NO_PAGE, usePos = const.CONT_NO_POS):
        self.targetName = name
        p = BigWorld.player()
        self.page = usePage
        self.pos = usePos
        if usePage == const.CONT_NO_PAGE:
            pages = p.inv.getPageTuple()
            finded = False
            for page in pages:
                for pos in p.inv.getPosTuple(page):
                    obj = p.inv.getQuickVal(page, pos)
                    if obj == const.CONT_EMPTY_VAL:
                        continue
                    if obj.cstype == Item.SUBTYPE_2_FIREWORKS:
                        self.page = page
                        self.pos = usePos
                        finded = True
                        break

                if finded:
                    break

        if self.page == const.CONT_NO_PAGE:
            BigWorld.showGameMsg(GMDD.data.DO_NOT_HAVA_FIRE_WORK, ())
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FIRE_WORK)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onSendInfo(self, *args):
        name = unicode2gbk(args[3][0].GetString())
        msg = unicode2gbk(args[3][1].GetString())
        isAnyous = args[3][2].GetBool()
        useLaba = args[3][3].GetBool()
        p = BigWorld.player()
        if not name:
            p.showGameMsg(GMDD.data.FIRE_WORK_INPUT_NAME, ())
            return
        if not msg:
            p.showGameMsg(GMDD.data.FIRE_WORK_INPUT_MSG, ())
            return
        if useLaba:
            isNormal = taboo.checkDisbWordNoReplace(msg)
        else:
            isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        if useLaba:
            isNormal, msg = gameglobal.rds.ui.chat._tabooCheck(const.CHAT_CHANNEL_WORLD_EX, msg)
        else:
            isNormal, msg = gameglobal.rds.ui.chat._tabooCheck(const.CHAT_CHANNEL_SINGLE, msg, name)
        if not isNormal:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        if isAnyous:
            useType = const.ANONYMOUS_CHAT_MSG
        else:
            useType = const.NORMAL_CHAT_MSG
        msg = msg + ':role'
        if useLaba:
            itemName = gameStrings.TEXT_FIREWORKSENDERPROXY_101 if isAnyous else gameStrings.TEXT_FIREWORKSENDERPROXY_101_1
            showMsg = gameStrings.TEXT_FIREWORKSENDERPROXY_102 % itemName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(showMsg, Functor(self.realUseFireworksLaba, self.page, self.pos, name, msg, useType, useLaba))
        else:
            BigWorld.player().cell.useFireworksLaba(self.page, self.pos, name, msg, useType, useLaba)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, msg, name, False, True)

    def realUseFireworksLaba(self, page, pos, name, msg, useType, useLaba):
        BigWorld.player().cell.useFireworksLaba(page, pos, name, msg, useType, useLaba)

    def onGetName(self, *args):
        return GfxValue(gbk2unicode(self.targetName))

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if page == self.page and pos == self.pos:
                return True
        return False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FIRE_WORK:
            self.mediator = mediator
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
