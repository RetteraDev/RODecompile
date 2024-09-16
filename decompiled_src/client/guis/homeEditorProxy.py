#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeEditorProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
from helpers import editorHelper
from guis.uiProxy import UIProxy
from guis import messageBoxProxy
from guis import uiConst
from guis import ui
from data import home_data as HD

class HomeEditorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HomeEditorProxy, self).__init__(uiAdapter)
        self.modelMap = {'handleClickBtn': self.onHandleClickBtn,
         'enableFittingRoomLvUp': self.onEnableFittingRoomLvUp,
         'enableHomePermissionSet': self.onEnablePermissionSet}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOME_EDITOR_TOP:
            self.mediator = mediator

    def show(self):
        if not self.canShow():
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_EDITOR_TOP)
        self.ins = editorHelper.instance()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_EDITOR_TOP)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_EDITOR_BOTTOM)
        if self.isInHomeEditorMode:
            gameglobal.rds.ui.restoreUI()
        editorHelper.instance().destroy()

    def reset(self):
        self.mediator = None
        self.ins = None
        self.messageBoxId = None

    def onHandleClickBtn(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('onHandleClickBtn', btnName)
        p = BigWorld.player()
        if btnName == 'furnitureArrange':
            p.base.beginModifyRoom()
        elif btnName == 'homeEnlarge':
            if gameglobal.rds.configData.get('enableEnlargeHomeRoom', False):
                gameglobal.rds.ui.roomEnlarge.show()
            else:
                p.enlarageFittingRoom()
        elif btnName == 'authoritySet':
            if gameglobal.rds.configData.get('enableHomePermissionSet', False):
                gameglobal.rds.ui.homePermission.show()
        elif btnName == 'quit':
            self.quitEditMode()
        elif btnName == 'save':
            self.saveArrange()
        elif btnName == 'openInv':
            self.openInv()

    @ui.callFilter(1, True)
    def quitEditMode(self):
        if self.ins.haveModified():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_DYEPLANEPROXY_444, self.confirmSave), MBButton(gameStrings.TEXT_HOMEEDITORPROXY_76_1, self.confirmNotSave), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.cancel)]
            if not self.messageBoxId:
                self.messageBoxId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_HOMEEDITORPROXY_78, buttons)
        else:
            self.endEditMode()

    def confirmSave(self):
        self.saveArrange(True)
        self.messageBoxId = None

    def confirmNotSave(self):
        if self.ins:
            self.ins.returnToSaveState()
        self.endEditMode()
        self.messageBoxId = None

    def cancel(self):
        self.messageBoxId = None

    def openInv(self, forceOpen = False):
        if forceOpen or not gameglobal.rds.ui.inventory.isShow():
            gameglobal.rds.ui.inventory.show()
            gameglobal.rds.ui.inventory.setItemFilter(uiConst.FILTER_ITEM_FURNITURE)
        else:
            gameglobal.rds.ui.inventory.hide()

    def endEditMode(self):
        p = BigWorld.player()
        p.base.endModifyRoom()
        self.setEditMode()

    @ui.callFilter(1, True)
    def saveArrange(self, saveAndQuit = False):
        if self.ins:
            self.ins.saveArrange(saveAndQuit)

    def setEditMode(self):
        if not self.ins:
            return
        if not self.isInHomeEditorMode():
            self.ins.setEditMode(True)
            self.ins.saveState()
            gameglobal.rds.ui.hideAllUI()
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_HOME_EDITOR_TOP, True)
            self.switchVisibility(False)
            if gameglobal.rds.ui.inventory.isShow():
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_INVENTORY, True)
                gameglobal.rds.ui.inventory.setItemFilter(uiConst.FILTER_ITEM_FURNITURE)
            else:
                self.openInv(True)
        else:
            self.ins.setEditMode(False)
            self.switchVisibility(True)
            gameglobal.rds.ui.inventory.setItemFilter(uiConst.FASHION_FILTER_ITEM_ALL)
            gameglobal.rds.ui.restoreUI()

    def switchVisibility(self, value):
        if self.mediator:
            self.mediator.Invoke('switchVisibility', GfxValue(value))
        if not value:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_EDITOR_BOTTOM)
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_EDITOR_BOTTOM)

    def isInHomeEditorMode(self):
        return self.ins and self.ins.editMode

    def useFurniture(self, it, nPage, nPos, resKind):
        if not self.ins:
            return
        self.ins.useFurniture(it, nPage, nPos, resKind)

    def canShow(self):
        ins = editorHelper.instance()
        player = BigWorld.player()
        if ins.ownerGbID == player.gbId:
            return True
        if gameglobal.rds.configData.get('enableHomeIntimacy', False) and ins.ownerGbID == getattr(player.friend, 'intimacyTgt', 0):
            return True
        return False

    def isFurnitureUsedOut(self, it):
        if self.ins and self.ins.isFurnitureUsedOut(it):
            return True
        return False

    def onEnableFittingRoomLvUp(self, *args):
        player = BigWorld.player()
        ins = editorHelper.instance()
        return GfxValue(gameglobal.rds.configData.get('enableFittingRoomLvUp', False) and ins.ownerGbID == player.gbId)

    def onEnablePermissionSet(self, *args):
        player = BigWorld.player()
        ins = editorHelper.instance()
        hd = HD.data.get(player.myHome.roomId, {})
        enlargeRoomId = hd.get('enlargeRoomId', 0)
        hasEnlargeRoom = enlargeRoomId in player.myHome.erooms
        return GfxValue(gameglobal.rds.configData.get('enableHomePermissionSet', False) and ins.ownerGbID == player.gbId and hasEnlargeRoom)
