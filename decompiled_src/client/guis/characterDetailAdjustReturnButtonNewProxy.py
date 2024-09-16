#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterDetailAdjustReturnButtonNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
from uiProxy import UIProxy
from asObject import ASUtils
from asObject import ASObject
from gamestrings import gameStrings

class CharacterDetailAdjustReturnButtonNewProxy(UIProxy):
    MEN_ICON_LIST = (('hao', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_HAO), ('lie', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LIE), ('lin', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LIN))
    WOMEN_ICON_LIST = (('mei', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_MEI), ('li', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LI), ('qing', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_QING))

    def __init__(self, uiAdapter):
        super(CharacterDetailAdjustReturnButtonNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW)

    def initUI(self):
        self.widget.returnBtn.addEventListener(events.BUTTON_CLICK, self.handleReturnBtnClick, False, 0, True)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        inSchoolAvatar = gameglobal.rds.loginScene.inSchoolAvatarConfigStage()
        self.widget.selectSex.men.visible = gameglobal.rds.loginScene.selectGender == const.SEX_MALE if not inSchoolAvatar else True
        self.widget.selectSex.men.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.men.selected = False
        self.widget.selectSex.men.focusable = False
        self.widget.selectSex.women.visible = gameglobal.rds.loginScene.selectGender == const.SEX_FEMALE if not inSchoolAvatar else True
        self.widget.selectSex.women.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.women.selected = False
        self.widget.selectSex.women.focusable = False
        self.widget.subSchool.bodyType.body0.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body1.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body2.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def onEnterFrame(self, *args):
        if not self.widget:
            return
        if not self.isPointInBodyType():
            self.widget.subSchool.visible = False

    def handleReturnBtnClick(self, *args):
        gameglobal.rds.ui.characterDetailAdjust.openReturnWidget()

    def handleSexRollOver(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.target
        if itemMc.name == 'men':
            self.currentSex = const.SEX_MALE
            self.showBodySelectInfo(const.SEX_MALE)
        elif itemMc.name == 'women':
            self.currentSex = const.SEX_FEMALE
            self.showBodySelectInfo(const.SEX_FEMALE)

    def handleBodySelect(self, *args):
        e = ASObject(args[3][0])
        bodyInfo = e.target.data
        if not bodyInfo:
            return
        icon = bodyInfo[0]
        sex = bodyInfo[1]
        bodyType = bodyInfo[2]
        if bodyType == gameglobal.rds.loginScene.selectBodyType and self.currentSex == gameglobal.rds.loginScene.selectGender:
            return
        if self.selectedBodyTypeMc:
            self.selectedBodyTypeMc.selected = False
        e.target.selected = True
        self.selectedBodyTypeMc = e.target
        gameglobal.rds.loginScene.onChangeBodyTypeInDetailAdjust(sex, bodyType)

    def isPointInBodyType(self):
        x = self.widget.stage.mouseX
        y = self.widget.stage.mouseY
        _x, _y = ASUtils.global2Local(self.widget, x, y)
        isInSex = self._isPointInMc(self.widget.selectSex, _x, _y)
        _x, _y = ASUtils.global2Local(self.widget, x, y)
        isInSubSchool = self._isPointInMc(self.widget.subSchool, _x, _y)
        return isInSex or isInSubSchool

    def _isPointInMc(self, mc, x, y):
        return x >= mc.x and x <= mc.x + mc.width and y >= mc.y and y <= mc.y + mc.height

    def showBodySelectInfo(self, currentSex):
        if currentSex == const.SEX_UNKNOWN:
            return
        else:
            jobIconList = []
            curY = -100
            if currentSex == const.SEX_MALE:
                jobIconList = self.MEN_ICON_LIST
                curY = self.widget.selectSex.y + self.widget.selectSex.men.y + 7
            elif currentSex == const.SEX_FEMALE:
                jobIconList = self.WOMEN_ICON_LIST
                curY = self.widget.selectSex.y + self.widget.selectSex.women.y + 7
            self.widget.subSchool.visible = True
            self.widget.subSchool.y = curY
            self.widget.subSchool.gotoAndPlay(0)
            self.selectedBodyTypeMc = None
            jobInfo = gameglobal.rds.loginScene.getSelectSchoolConfig()
            for i in xrange(len(jobIconList)):
                bodyName = jobIconList[i][0]
                text = jobIconList[i][1]
                mc = self.widget.subSchool.bodyType.getChildByName('body%d' % i)
                mc.label = text
                mc.enabled = False
                mc.selected = False
                mc.data = ()
                if gameglobal.rds.loginScene.selectSchool == 7 and currentSex == const.SEX_MALE and i == 0:
                    continue
                for info in jobInfo.get('bodyData', []):
                    icon = info.get('icon', '')
                    sex = info.get('sex', const.SEX_UNKNOWN)
                    bodyType = info.get('bodyType', -1)
                    if bodyName == icon and currentSex == sex:
                        mc.data = (icon, sex, bodyType)
                        mc.enabled = True
                        if bodyType == gameglobal.rds.loginScene.selectBodyType and sex == gameglobal.rds.loginScene.selectGender:
                            mc.selected = True
                            self.selectedBodyTypeMc = mc

            return
