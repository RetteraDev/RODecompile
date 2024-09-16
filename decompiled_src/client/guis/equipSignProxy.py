#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipSignProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
from guis import ui
from guis import uiConst
from guis.uiProxy import UIProxy
from ui import unicode2gbk
from helpers import taboo
from item import Item
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD

class EquipSignProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipSignProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'commit': self.commit}
        self.mediator = None
        self.isShow = False
        self.reset()
        self.equipPage = const.CONT_NO_PAGE
        self.equipPos = const.CONT_NO_PAGE
        self.consumeItemPage = const.CONT_NO_PAGE
        self.consumeItemPos = const.CONT_NO_PAGE
        self.resKind = const.RES_KIND_INV
        self.signCode = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_SIGN, self.closeWidget)

    def reset(self):
        self.dismiss()

    def commit(self, *args):
        self.signCode = unicode2gbk(args[3][0].GetString())
        if not self.signCode:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_EQUIPSIGNPROXY_50)
            return
        p = BigWorld.player()
        bs, msg = taboo.checkBSingle(self.signCode)
        bw, msg = taboo.checkBWorld(self.signCode)
        ba, msg = taboo.checkAllLvDisWorld(self.signCode)
        if taboo.checkMonitorWord(self.signCode) or not bs or not bw or not ba or not taboo.checkDisbWordNoReplace(self.signCode):
            p.showGameMsg(GMDD.data.EQUIPSIGN_TABOO_WORD, ())
            return
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_EQUIPSIGNPROXY_61, self._trueCommit)

    def _trueCommit(self):
        self.cellSignEquip(self.equipPage, self.equipPos, self.consumeItemPage, self.consumeItemPos, self.signCode, self.resKind)
        self.closeWidget()

    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.EQUIP_SIGN)
    def cellSignEquip(self, ePage, ePos, iPage, iPos, signCode, resKind):
        BigWorld.player().cell.signEquip(ePage, ePos, iPage, iPos, signCode, resKind)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def dismiss(self, *arg):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_SIGN)
        self.isShow = False
        self.mediator = None
        self.equipPage = const.CONT_NO_PAGE
        self.equipPos = const.CONT_NO_PAGE
        self.consumeItemPage = const.CONT_NO_PAGE
        self.consumeItemPos = const.CONT_NO_PAGE
        self.resKind = const.RES_KIND_INV
        self.signCode = ''

    def show(self, equipPage, equipPos, consumeItemPage, consumeItemPos, resKind = const.RES_KIND_INV):
        p = BigWorld.player()
        signItem = p.inv.getQuickVal(consumeItemPage[0], consumeItemPos[0])
        if getattr(signItem, 'cstype', 0) == Item.SUBTYPE_2_SIGN_CLEAN:
            self.hide()
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.MSG_CLEAN_SING, self.confirmCleanSign)
        elif not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_SIGN, True)
            self.isShow = True
        self.equipPage = equipPage
        self.equipPos = equipPos
        self.consumeItemPage = consumeItemPage
        self.consumeItemPos = consumeItemPos
        self.resKind = resKind

    def confirmCleanSign(self):
        BigWorld.player().cell.cleanSignEquip(self.equipPage, self.equipPos, self.consumeItemPage, self.consumeItemPos, self.resKind)
