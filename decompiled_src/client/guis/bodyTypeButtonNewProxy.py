#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bodyTypeButtonNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
from uiProxy import UIProxy
from gamestrings import gameStrings

class BodyTypeButtonNewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BodyTypeButtonNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BODYTYPE_BUTTON_NEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BODYTYPE_BUTTON_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BODYTYPE_BUTTON_NEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BODYTYPE_BUTTON_NEW)

    def initUI(self):
        self.widget.bodyTypeBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def clickBtn(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.CHARACTER_DETAIL_ADJUST_NEW_BODY_TYPE_TIP, yesCallback=self._realChangeBodyType)

    def _realChangeBodyType(self):
        account = BigWorld.player()
        character = gameglobal.rds.ui.characterCreate.getChooseAvatar()
        gbID = character.get('gbID', 0)
        player = gameglobal.rds.loginScene.player
        gameglobal.rds.ui.characterDetailAdjust.saveMorpher(player)
        if not gameglobal.rds.ui.characterDetailAdjust.checkCanCreate():
            return
        flag = gametypes.RESET_PROPERTY_AVATARCONFIG
        if gameglobal.rds.loginScene.inAvatarconfigStage2():
            flag = gametypes.RESET_PROPERTY_BODYTYPE
        if gameglobal.rds.loginScene.inAvatarconfigStage2Sub():
            flag = gametypes.RESET_PROPERTY_SEX
        if gameglobal.rds.loginScene.inSchoolAvatarConfigStage():
            flag = gametypes.RESET_PROPERTY_SCHOOL
        account.base.resetAvatarProp(gbID, flag, player.physique.bodyType, player.physique.sex, player.physique.hair, player.avatarConfig)
        gameglobal.rds.loginManager.cache = {'gbID': gbID,
         'hair': player.physique.hair,
         'avatarConfig': player.avatarConfig,
         'bodyType': player.physique.bodyType,
         'sex': player.physique.sex}
