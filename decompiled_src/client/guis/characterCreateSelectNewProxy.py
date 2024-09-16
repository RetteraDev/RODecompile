#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterCreateSelectNewProxy.o
import BigWorld
import Sound
import gameglobal
import uiConst
import events
import const
import clientcom
import gameconfigCommon
from helpers import cgPlayer
from callbackHelper import Functor
from gamestrings import gameStrings
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
import gamelog
STAGE_ORIGINAL_WIDTH = 1920
STAGE_ORIGINAL_HEIGHT = 1080
MIN_UI_SCALE = 0.9
CHAR_SELECT_TYPE_CREATE = 0
CHAR_SELECT_TYPE_CHANGE_BODY = 1
CHAR_SELECT_TYPE_CHANGE_SEX = 2

class CharacterCreateSelectNewProxy(UIProxy):
    MEN_ICON_LIST = (('hao', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_HAO), ('lie', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LIE), ('lin', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LIN))
    WOMEN_ICON_LIST = (('mei', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_MEI), ('li', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_LI), ('qing', gameStrings.CHARACTER_CREATE_SELECT_NEW_BODYTYPE_QING))
    SCHOOL_NAME_MAP = {const.SCHOOL_GUANGREN: 'guangren',
     const.SCHOOL_LINGLONG: 'linglong',
     const.SCHOOL_LIUGUANG: 'liuguang',
     const.SCHOOL_SHENTANG: 'shengtang',
     const.SCHOOL_YANTIAN: 'yantian',
     const.SCHOOL_YECHA: 'yecha',
     const.SCHOOL_YUXU: 'yuxu',
     const.SCHOOL_MIAOYIN: 'miaoYin',
     const.SCHOOL_TIANZHAO: 'tianzhao'}
    SCHOOL_SHORTNAME_MAP = {3: 'st',
     4: 'yx',
     5: 'gr',
     6: 'yt',
     7: 'll',
     8: 'lg',
     9: 'yc',
     10: 'tz'}
    RESIZE_CONTROLS = {'LeftTop': ('selectSchool', 'subSchool'),
     'LeftBottom': ('returnLoginBtn', 'selectSex'),
     'RightTop': ('rightTop', 'schoolFeature', 'moviePlay', 'movieWindow', 'movieBack'),
     'RightBottom': ('appearanceBtn',)}
    NO_SCALE_CONTROLS = ['returnLoginBtn', 'appearanceBtn']

    def __init__(self, uiAdapter):
        super(CharacterCreateSelectNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.selectedBodyTypeMc = None
        self.cgPlayer = None
        self.selectSchoolBtn = None
        self.currentSex = const.SEX_MALE
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_CREATE_SELECT_NEW, self.hide)
        self.controlsOriginalOffset = {}
        self.delayPlaySchoolEffectTimer = -1
        self.uiType = CHAR_SELECT_TYPE_CREATE

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHARACTER_CREATE_SELECT_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_CREATE_SELECT_NEW)
        self.selectedBodyTypeMc = None
        self.endMovie()
        self.cgPlayer = None
        self.selectSchoolBtn = None
        if self.delayPlaySchoolEffectTimer != -1:
            BigWorld.cancelCallback(self.delayPlaySchoolEffectTimer)
            self.delayPlaySchoolEffectTimer = -1

    def show(self):
        self.uiType = CHAR_SELECT_TYPE_CREATE
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_CREATE_SELECT_NEW)
        else:
            self.initUI()

    def checkNewSchoolTianZhao(self, *args):
        if not self.widget:
            return
        self.widget.selectSchool.tianzhaoBtn.visible = clientcom.enableNewSchoolTianZhao()
        school = gameglobal.rds.loginScene.selectSchool
        self.widget.moviePlay.yulan.gotoAndStop(self.SCHOOL_SHORTNAME_MAP.get(school, 0))

    def showBodyReset(self, isResetSex):
        if isResetSex:
            self.uiType = CHAR_SELECT_TYPE_CHANGE_SEX
        else:
            self.uiType = CHAR_SELECT_TYPE_CHANGE_BODY
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_CREATE_SELECT_NEW)
        else:
            self.initUI()

    def initUI(self):
        self.widget.visible = False
        self.widget.selectSchool.tianzhaoBtn.visible = False
        if self.uiType == CHAR_SELECT_TYPE_CREATE:
            BigWorld.callback(0.2, Functor(self.delayShowUI))
        elif self.uiType == CHAR_SELECT_TYPE_CHANGE_BODY or self.uiType == CHAR_SELECT_TYPE_CHANGE_SEX:
            BigWorld.callback(0.2, Functor(self.delayShowUIChangeBody))
        ASUtils.callbackAtFrame(self.widget.selectSchool, 18, self.checkNewSchoolTianZhao)

    def delayShowUI(self):
        self.widget.visible = True
        self.widget.gotoAndStop(76)
        self.widget.rightTop.schoolTitles.getChildAt(0).gotoAndStop(45)
        self.restoreOriginalOffset()
        self.realResize()
        self.widget.rightTop.visible = False
        self.widget.schoolFeature.visible = False
        self.widget.subSchool.visible = False
        self.widget.gotoAndPlay(0)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)

    def delayShowUIChangeBody(self):
        self.widget.visible = True
        self.widget.gotoAndStop(self.widget.totalFrames)
        self.widget.selectSchool.visible = False
        self.widget.rightTop.visible = False
        self.widget.schoolFeature.visible = False
        self.widget.moviePlay.visible = False
        self.widget.movieWindow.visible = False
        self.widget.subSchool.visible = False
        self.widget.returnLoginBtn.addEventListener(events.BUTTON_CLICK, self.handleGoBackClick, False, 0, True)
        self.widget.appearanceBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoCharacterDetailAdjust, False, 0, True)
        self.widget.selectSex.men.visible = gameglobal.rds.loginScene.selectGender == const.SEX_MALE
        self.widget.selectSex.men.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.men.selected = False
        self.widget.selectSex.men.focusable = False
        self.widget.selectSex.women.visible = gameglobal.rds.loginScene.selectGender == const.SEX_FEMALE
        self.widget.selectSex.women.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.women.selected = False
        self.widget.selectSex.women.focusable = False
        self.widget.subSchool.bodyType.body0.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body1.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body2.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.restoreOriginalOffset()
        self.realResize()
        for school, name in self.SCHOOL_NAME_MAP.iteritems():
            gamelog.debug('ypc@ child name = ', '%sBtn' % name)
            child = self.widget.selectSchool.getChildByName('%sBtn' % name)
            if not child:
                continue
            child.addEventListener(events.BUTTON_CLICK, self.handleSchoolSelect, False, 0, True)
            child.data = school
            if gameglobal.rds.loginScene.selectSchool == school:
                child.selected = True
                self.selectSchoolBtn = child
            if school == const.SCHOOL_MIAOYIN:
                child.visible = clientcom.enableNewSchoolMiaoYin()
            elif school == const.SCHOOL_TIANZHAO:
                child.visible = clientcom.enableNewSchoolTianZhao()

        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.handleMouseCheck, False, 0, True)
        self.widget.stage.addEventListener(events.EVENT_RESIZE, self.onResize, False, 0, True)

    def uiInitAfterPlayFinished(self):
        self.widget.returnLoginBtn.addEventListener(events.BUTTON_CLICK, self.handleGoBackClick, False, 0, True)
        self.widget.appearanceBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoCharacterDetailAdjust, False, 0, True)
        self.widget.moviePlay.addEventListener(events.BUTTON_CLICK, self.handlePlayMovie, False, 0, True)
        self.widget.selectSex.men.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.men.selected = False
        self.widget.selectSex.men.focusable = False
        self.widget.selectSex.women.addEventListener(events.MOUSE_ROLL_OVER, self.handleSexRollOver, False, 0, True)
        self.widget.selectSex.women.selected = False
        self.widget.selectSex.women.focusable = False
        self.widget.subSchool.bodyType.body0.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body1.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.widget.subSchool.bodyType.body2.addEventListener(events.BUTTON_CLICK, self.handleBodySelect, False, 0, True)
        self.playSchoolTitleEffect()
        for school, name in self.SCHOOL_NAME_MAP.iteritems():
            gamelog.debug('ypc@ child name = ', '%sBtn' % name)
            child = self.widget.selectSchool.getChildByName('%sBtn' % name)
            if not child:
                continue
            child.addEventListener(events.BUTTON_CLICK, self.handleSchoolSelect, False, 0, True)
            child.data = school
            if gameglobal.rds.loginScene.selectSchool == school:
                child.selected = True
                self.selectSchoolBtn = child
            if school == const.SCHOOL_MIAOYIN:
                child.visible = clientcom.enableNewSchoolMiaoYin()
            elif school == const.SCHOOL_TIANZHAO:
                child.visible = clientcom.enableNewSchoolTianZhao()

        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.handleMouseCheck, False, 0, True)
        self.widget.stage.addEventListener(events.EVENT_RESIZE, self.onResize, False, 0, True)

    def restoreOriginalOffset(self):
        self.widget.x = 0
        self.widget.y = 0
        stageWidth = STAGE_ORIGINAL_WIDTH
        stageHeight = STAGE_ORIGINAL_HEIGHT
        for type, controls in self.RESIZE_CONTROLS.iteritems():
            for cname in controls:
                mc = self.widget.getChildByName(cname)
                if not mc:
                    continue
                if type not in self.controlsOriginalOffset:
                    self.controlsOriginalOffset[type] = []
                lx, ly = mc.x, mc.y
                if type == 'LeftBottom':
                    self.controlsOriginalOffset[type].append((cname, lx, stageHeight - ly - mc.height))
                elif type == 'LeftTop':
                    self.controlsOriginalOffset[type].append((cname, lx, ly))
                elif type == 'RightTop':
                    if cname == 'rightTop':
                        self.controlsOriginalOffset[type].append((cname, stageWidth - lx - 475, ly))
                    else:
                        self.controlsOriginalOffset[type].append((cname, stageWidth - lx - mc.width, ly))
                    if cname == 'rightTop':
                        gamelog.debug('ypc@ rightTop : ', lx, ly, mc.width, mc.height, mc.scaleX, mc.scaleY)
                elif type == 'RightBottom':
                    self.controlsOriginalOffset[type].append((cname, stageWidth - lx - mc.width, stageHeight - ly - mc.height))

    def onResize(self, *args):
        BigWorld.callback(0.1, Functor(self.realResize))

    def realResize(self):
        if not self.widget:
            return
        stageWidth = self.widget.stage.stageWidth
        stageHeight = self.widget.stage.stageHeight
        scaleX = float(stageWidth) / STAGE_ORIGINAL_WIDTH
        scaleY = float(stageHeight) / STAGE_ORIGINAL_HEIGHT
        scale = min(scaleX, scaleY)
        scaleX = scaleY = scale
        for type, controlsInfo in self.controlsOriginalOffset.iteritems():
            for cname, offx, offy in controlsInfo:
                mc = self.widget.getChildByName(cname)
                if not mc:
                    continue
                if cname in self.NO_SCALE_CONTROLS:
                    mc.scaleX = max(MIN_UI_SCALE, scale)
                    mc.scaleY = max(MIN_UI_SCALE, scale)
                else:
                    mc.scaleX = scale
                    mc.scaleY = scale
                lx, ly = (0, 0)
                if type == 'LeftTop':
                    lx, ly = ASUtils.global2Local(self.widget, offx * scaleX, offy * scaleY)
                elif type == 'LeftBottom':
                    lx, ly = ASUtils.global2Local(self.widget, offx * scaleX, stageHeight - offy * scaleY - mc.height)
                elif type == 'RightTop':
                    if cname == 'rightTop':
                        lx, ly = ASUtils.global2Local(self.widget, stageWidth - offx * scaleX - 475 * scale, offy * scaleY)
                    else:
                        lx, ly = ASUtils.global2Local(self.widget, stageWidth - offx * scaleX - mc.width, offy * scaleY)
                elif type == 'RightBottom':
                    lx, ly = ASUtils.global2Local(self.widget, stageWidth - offx * scaleX - mc.width, stageHeight - offy * scaleY - mc.height)
                if cname == 'rightTop':
                    gamelog.debug('ypc@ rightTop : ', lx, ly, mc.width, mc.height, mc.scaleX, mc.scaleY, offx, offy)
                mc.x = lx
                mc.y = ly

    def onEnterFrame(self, *args):
        if self.widget.currentFrame == 0:
            self.widget.moviePlay.yulan.gotoAndStop(str(gameglobal.rds.loginScene.selectSchool))
            self.widget.movieWindow.visible = False
        if self.widget.currentFrame == 37:
            self.widget.subSchool.gotoAndStop(0)
        if self.widget.currentFrame >= self.widget.totalFrames:
            self.widget.removeEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame)
            self.uiInitAfterPlayFinished()

    def handleMouseCheck(self, *args):
        if not self.widget:
            return
        if not self.isPointInBodyType() and self.widget.subSchool:
            self.widget.subSchool.visible = False

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def isPointInBodyType(self):
        if not self.widget or not self.widget.selectSex or not self.widget.subSchool:
            return False
        x = self.widget.stage.mouseX
        y = self.widget.stage.mouseY
        _x, _y = ASUtils.global2Local(self.widget, x, y)
        isInSex = self._isPointInMc(self.widget.selectSex, _x, _y)
        _x, _y = ASUtils.global2Local(self.widget, x, y)
        isInSubSchool = self._isPointInMc(self.widget.subSchool, _x, _y)
        return isInSex or isInSubSchool

    def _isPointInMc(self, mc, x, y):
        return x >= mc.x and x <= mc.x + mc.width and y >= mc.y and y <= mc.y + mc.height

    def handleGoBackClick(self, *args):
        gameglobal.rds.loginScene.leaveCreateSelectNewStage()
        gameglobal.rds.loginScene.returnToCharacterCreate()

    def handleGotoCharacterDetailAdjust(self, *args):
        gameglobal.rds.loginScene.leaveCreateSelectNewStage()
        if self.uiType == CHAR_SELECT_TYPE_CREATE:
            gameglobal.rds.loginScene.gotoCharacterDetailAdjust()
        elif self.uiType == CHAR_SELECT_TYPE_CHANGE_BODY:
            gameglobal.rds.loginScene.gotoCharacterDetailAdjustChangeBodySex(False)
        elif self.uiType == CHAR_SELECT_TYPE_CHANGE_SEX:
            gameglobal.rds.loginScene.gotoCharacterDetailAdjustChangeBodySex(True)

    def handleSexRollOver(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.target
        if itemMc.name == 'men':
            self.currentSex = const.SEX_MALE
            self.showBodySelectInfo(const.SEX_MALE)
        elif itemMc.name == 'women':
            self.currentSex = const.SEX_FEMALE
            self.showBodySelectInfo(const.SEX_FEMALE)

    def handleSchoolSelect(self, *args):
        e = ASObject(args[3][0])
        school = int(e.target.data)
        if school == gameglobal.rds.loginScene.selectSchool:
            return
        if self.selectSchoolBtn:
            self.selectSchoolBtn.selected = False
        e.target.selected = True
        self.selectSchoolBtn = e.target
        self.endMovie()
        if self.delayPlaySchoolEffectTimer != -1:
            BigWorld.cancelCallback(self.delayPlaySchoolEffectTimer)
        self.widget.rightTop.visible = False
        self.delayPlaySchoolEffectTimer = BigWorld.callback(1.0, Functor(self.playSchoolTitleEffect))
        self.widget.schoolFeature.visible = False
        self.widget.moviePlay.yulan.gotoAndStop(self.SCHOOL_SHORTNAME_MAP.get(school, 0))
        gamelog.debug('ypc@ handleSchoolSelect!!!', school)
        gameglobal.rds.loginScene.onChangeSchool(school)
        if gameconfigCommon.enableTianZhaoLoginShowIgnore() and school == const.SCHOOL_TIANZHAO:
            ASUtils.DispatchButtonEvent(self.widget.appearanceBtn)

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
        gameglobal.rds.loginScene.onChangeBodyType(sex, bodyType)

    def handlePlayMovie(self, *args):
        self.playMovie()

    def showBodySelectInfo(self, currentSex):
        if currentSex == const.SEX_UNKNOWN:
            return
        else:
            jobIconList = []
            curY = -100
            stageWidth = self.widget.stage.stageWidth
            stageHeight = self.widget.stage.stageHeight
            scaleX = float(stageWidth) / STAGE_ORIGINAL_WIDTH
            scaleY = float(stageHeight) / STAGE_ORIGINAL_HEIGHT
            scale = min(scaleX, scaleY)
            if currentSex == const.SEX_MALE:
                jobIconList = self.MEN_ICON_LIST
                curY = self.widget.selectSex.y + self.widget.selectSex.men.y + 7
            elif currentSex == const.SEX_FEMALE:
                jobIconList = self.WOMEN_ICON_LIST
                curY = self.widget.selectSex.y + self.widget.selectSex.women.y * scale + 7
            self.widget.subSchool.visible = True
            self.widget.subSchool.y = curY
            self.widget.subSchool.gotoAndPlay(0)
            self.selectedBodyTypeMc = None
            jobInfo = gameglobal.rds.loginScene.getSelectSchoolConfig()
            gamelog.debug('ypc@ jobInfo = ', jobInfo)
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
                            gamelog.debug('ypc@ bodyType currentSex = ', bodyType, currentSex)
                            mc.selected = True
                            self.selectedBodyTypeMc = mc

            return

    def playMovie(self):
        if not self.widget:
            return
        self.widget.moviePlay.visible = False
        self.widget.movieWindow.visible = True
        w = self.widget.moviePlay.width - 2
        h = self.widget.moviePlay.height - 2
        x = self.widget.moviePlay.x + 1
        y = self.widget.moviePlay.y + 1
        z = 1.0
        config = {'position': (x, y, z),
         'w': w,
         'h': h,
         'loop': False,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/CharacterCreateSelectNewWidget' + self.uiAdapter.getUIExt(), 'unitDesc01', int(w), int(h))
        school = gameglobal.rds.loginScene.selectSchool
        self.cgPlayer.playMovie('school_%d' % school, config)
        Sound.enableMusic(False)

    def endMovie(self):
        if self.cgPlayer:
            gamelog.debug('ypc@ endMovie')
            self.cgPlayer.endMovie()
            self.cgPlayer = None
            Sound.enableMusic(True)
        if self.widget:
            self.widget.moviePlay.visible = True
            self.widget.movieWindow.visible = False

    def onMovieEnd(self):
        self.endMovie()

    def playSchoolTitleEffect(self):
        if not self.widget:
            return
        self.widget.rightTop.visible = True
        self.widget.rightTop.gotoAndPlay(0)
        self.widget.rightTop.schoolTitles.visible = False
        self.widget.rightTop.schoolIntroduce.visible = False
        if self.widget.rightTop.hasEventListener(events.EVENT_ENTER_FRAME):
            self.widget.rightTop.removeEventListener(events.EVENT_ENTER_FRAME, self.onPlaySchoolEnterFrame)
        self.widget.rightTop.addEventListener(events.EVENT_ENTER_FRAME, self.onPlaySchoolEnterFrame, False, 0, True)
        schoolName = self.SCHOOL_NAME_MAP.get(gameglobal.rds.loginScene.selectSchool, 'yuxu')
        self.widget.schoolFeature.visible = True
        self.widget.schoolFeature.gotoAndPlay(0)
        self.widget.schoolFeature.school.gotoAndPlay(schoolName)

    def onPlaySchoolEnterFrame(self, *args):
        if not self.widget or not self.widget.rightTop:
            return
        schoolName = self.SCHOOL_NAME_MAP.get(gameglobal.rds.loginScene.selectSchool, 'yuxu')
        if self.widget.rightTop.currentFrame == 2:
            self.widget.rightTop.schoolTitles.visible = True
            self.widget.rightTop.schoolTitles.gotoAndStop(schoolName)
            mc = self.widget.rightTop.schoolTitles.getChildByName(schoolName)
            if mc:
                mc.gotoAndPlay(0)
        if self.widget.rightTop.currentFrame == 23:
            self.widget.rightTop.schoolIntroduce.visible = True
            self.widget.rightTop.schoolIntroduce.gotoAndPlay(0)
            self.widget.rightTop.schoolIntroduce.school.gotoAndPlay(schoolName)
            self.widget.rightTop.removeEventListener(events.EVENT_ENTER_FRAME, self.onPlaySchoolEnterFrame)
