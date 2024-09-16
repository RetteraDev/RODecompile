#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/characterSelectProxy.o
import random
import BigWorld
import ResMgr
import Sound
from Scaleform import GfxValue
import gameglobal
import const
import gamelog
import gametypes
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from helpers import cgPlayer
from ui import gbk2unicode
from guis import loginScene
from helpers import cameraControl as CC
from data import school_data as SD

class CharacterSelectProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(CharacterSelectProxy, self).__init__(uiAdapter)
        self.bindType = 'characterSelect'
        self.modelMap = {'clickReturnCreate': self.onClickReturnCreate,
         'clickSelectJob': self.onClickSelectJob,
         'clickCharacterDetail': self.onClickCharacterDetail,
         'clickNext': self.onClickNext,
         'clickReturn': self.onClickReturn,
         'clickPlayMovie': self.onClickPlayMovie,
         'getSelectInfo': self.onGetSelectInfo,
         'clickBodyType': self.onClickBodyType,
         'enableMale2': self.onEnableMale2,
         'enableSchoolChange': self.onEnableSchoolChange}
        self.jobListMed = None
        self.jobDescMed = None
        self.jobNavigationMed = None
        self.cgPlayer = None
        self.reset()

    def reset(self):
        self.school = const.SCHOOL_SHENTANG
        self.gender = const.SEX_MALE
        self.bodyType = const.BODY_TYPE_5
        self.applyAvatarConfig = False
        self.endMovie()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST:
            self.jobListMed = mediator
            if self.jobListMed and gameglobal.rds.loginScene.inSelectOneStage():
                self.jobListMed.Invoke('setSelected', GfxValue(self.school))
        elif widgetId == uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC:
            self.jobDescMed = mediator
        elif widgetId == uiConst.WIDGET_CHARACTER_NAVIGATION:
            self.jobNavigationMed = mediator
            self.showNavigation()

    def showNavigation(self):
        if self.jobNavigationMed:
            stage = 'stage2'
            loginScene = gameglobal.rds.loginScene
            if loginScene.inSelectZeroStage() or loginScene.inSelectOneStage():
                stage = 'stage2'
            elif loginScene.inSelectTwoStage() or loginScene.inBodyTypeStage():
                stage = 'stage2.5'
            elif loginScene.inAvatarStage():
                stage = 'stage3'
            self.jobNavigationMed.Invoke('gotoStage', GfxValue(stage))

    def setJobListVisible(self, school, isVisible):
        if self.jobListMed:
            self.jobListMed.Invoke('setJobListVisible', (GfxValue(school), GfxValue(isVisible)))

    def showDescription(self, school, gender = None, bodyType = None):
        schoolName = ''
        desc = ''
        if school != -1:
            schoolName = SD.data.get(school, {}).get('name', '')
            data = gameglobal.rds.loginScene.getCharShowData(school, gender, bodyType)
            desc = data.get('showDescription', '')
        if self.jobListMed:
            self.jobListMed.Invoke('updateSchoolTip', (GfxValue(gbk2unicode(schoolName)), GfxValue(gbk2unicode(desc))))

    def getValue(self, key):
        if key == 'characterSelect.jobData':
            jobData = SD.data.keys()
            return uiUtils.array2GfxAarry(jobData)
        if key == 'characterSelect.jobDetailData':
            jobInfo = (self.school, [])
            bodyData = loginScene.getCharShowData().get(self.school, [])
            if bodyData:
                for data in bodyData:
                    jobItem = (data['sex'], data['bodyType'], data.get('icon', 'hao'))
                    if not gameglobal.rds.configData.get('enableCreateFemale3Yecha', False) and data['sex'] == const.SEX_FEMALE and data['bodyType'] == const.BODY_TYPE_3 and self.school == const.SCHOOL_YECHA:
                        continue
                    if not gameglobal.rds.configData.get('enableCreateFemale2Yantian', False) and data['sex'] == const.SEX_FEMALE and data['bodyType'] == const.BODY_TYPE_2 and self.school == const.SCHOOL_YANTIAN:
                        continue
                    if gameglobal.rds.loginScene.inBodyTypeStage() and not gameglobal.rds.loginScene.inSchoolStage():
                        if self.gender != data['sex']:
                            jobInfo[1].append(())
                        else:
                            jobInfo[1].append(jobItem)
                    else:
                        jobInfo[1].append(jobItem)

            return uiUtils.array2GfxAarry(jobInfo, True)
        if key == 'characterSelect.jobSelect':
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(self.school))
            ar.SetElement(1, GfxValue(self.gender))
            ar.SetElement(2, GfxValue(self.bodyType))
            return ar
        if key == 'characterSelect.jobDesc':
            if gameglobal.rds.loginScene.inSelectZeroStage():
                return GfxValue(-1)
            return GfxValue(self.school)
        if key == 'characterSelect.descWord':
            csd = gameglobal.rds.loginScene.getCharShowData(self.school, self.gender, self.bodyType)
            return GfxValue(csd.get('icon', 'hao'))

    def clearAllSCWidgets(self):
        self.hide(False)

    def loadAllSCWidgets(self):
        loadWidgetsList = []
        if gameglobal.rds.loginScene.inSelectZeroStage():
            loadWidgetsList = [uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST, uiConst.BUTTON_CHARACTER_RETURN, uiConst.WIDGET_CHARACTER_NAVIGATION]
        elif gameglobal.rds.loginScene.inSelectOneStage():
            loadWidgetsList = [uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST,
             uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC,
             uiConst.BUTTON_CHARACTER_RETURN,
             uiConst.BUTTON_CHARACTER_NEXT]
        elif gameglobal.rds.loginScene.inSelectTwoStage():
            loadWidgetsList = [uiConst.WIDGET_SELECT_JOB_TWO, uiConst.BUTTON_CHARACTER_RETURN, uiConst.BUTTON_CHARACTER_NEXT]
            self.school = gameglobal.rds.loginScene.selectSchool
            self.gender = gameglobal.rds.loginScene.selectGender
            self.bodyType = gameglobal.rds.loginScene.selectBodyType
        elif gameglobal.rds.loginScene.inBodyTypeStage():
            loadWidgetsList = [uiConst.WIDGET_SELECT_JOB_TWO,
             uiConst.BUTTON_CHARACTER_RETURN,
             uiConst.BUTTON_CHARACTER_NEXT,
             uiConst.WIDGET_CHARACTER_NAVIGATION]
            self.school = gameglobal.rds.loginScene.selectSchool
            self.gender = gameglobal.rds.loginScene.selectGender
            self.bodyType = gameglobal.rds.loginScene.selectBodyType
        self.applyAvatarConfig = False
        gameglobal.rds.loginScene.loadWidgets(loadWidgetsList)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.jobListMed = None
        unloadWidgetsList = [uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST, uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC, uiConst.WIDGET_BODYTYPE_BUTTON]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)

    def onClickReturnCreate(self, *arg):
        self.returnToCreate(False)

    def onClickSelectJob(self, *arg):
        BigWorld.setBlackTime(0, 0, 0, 0.99, 0.99, 0.7)
        school = int(arg[3][0].GetNumber())
        try:
            gender = int(arg[3][1].GetNumber())
            bodyType = int(arg[3][2].GetNumber())
            bodyIdx = int(arg[3][3].GetNumber())
        except:
            csd = loginScene.getCharShowData().get(school, [])
            for i, data in enumerate(csd):
                if data.get('showModel', 0):
                    gender = data.get('sex', const.SEX_UNKNOWN)
                    bodyType = data.get('bodyType')
                    bodyIdx = i
                    break

        if gameglobal.rds.loginScene.inSelectZeroStage() or gameglobal.rds.loginScene.inSelectOneStage():
            self.school = school
            self.gender = gender
            self.bodyType = bodyType
            self.applyAvatarConfig = False
            ent = gameglobal.rds.loginScene.searchLoginModel(school, gender, bodyType)
            if ent and getattr(ent, 'firstFetchFinished', False):
                gameglobal.rds.loginScene.enterCharacterSelectOne()
                gameglobal.rds.sound.playSound(gameglobal.SD_493)
            self.endMovie()
            return
        applyAvatarConfig = False
        if gameglobal.rds.loginScene.inSchoolStage() and bodyIdx == -1:
            result = self.findSameBodyType(school)
            if result:
                gender, bodyType, bodyIdx = result
                applyAvatarConfig = True
            else:
                return
        gamelog.debug('b.e.:onClickSelectJob', school, gender, bodyType, bodyIdx, applyAvatarConfig)
        if self.school == school and self.gender == gender and self.bodyType == bodyType and self.applyAvatarConfig == applyAvatarConfig:
            gameglobal.rds.loginScene.moveToDestination(0, 'select_%d_%d.track' % (self.gender, self.bodyType))
            return
        self.school = school
        self.gender = gender
        self.bodyType = bodyType
        self.applyAvatarConfig = applyAvatarConfig
        self.showCharacterDesc(school)
        gameglobal.rds.loginScene.clearLoginModel()
        gameglobal.rds.loginScene.createLoginModel(self.school, self.gender, self.bodyType, bodyIdx, applyAvatarConfig)
        if gameglobal.rds.loginScene.loginModel:
            gameglobal.rds.loginScene.loginModel.showWeapon(True)
        gameglobal.rds.sound.playSound(gameglobal.SD_494)
        self.endMovie()

    def showCharacterDesc(self, school):
        if self.jobDescMed:
            self.jobDescMed.Invoke('updateAvatarMsg', GfxValue(school))

    def onClickCharacterDetail(self, *arg):
        nextStage = gameglobal.rds.loginScene.STAGE_CHARACTER_DETAIL_ADJUST
        try:
            nextStage = arg[0]
        except:
            pass

        BigWorld.setBlackTime(0, 0, 0, 0.99, 0.99, 0.7)
        self.clearAllSCWidgets()
        if nextStage == gameglobal.rds.loginScene.STAGE_CHARACTER_DETAIL_ADJUST:
            gameglobal.rds.loginScene.gotoDetailAdjustStage()
        else:
            gameglobal.rds.loginScene.stage = nextStage
        gameglobal.rds.ui.characterDetailAdjust.clear()
        gameglobal.rds.ui.characterDetailAdjust.loadCharacterDetail()
        gameglobal.rds.ui.characterDetailAdjust.loadAllCDWidgets()
        self.showNavigation()

    def gotoJobSelectTwo(self):
        unloadWidgetsList = [uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST, uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        self.jobDescMed = None
        gameglobal.rds.loginScene.gotoSelectTwoStage()
        self.loadAllSCWidgets()
        self.showNavigation()
        self.endMovie()

    def gotoJobSelectOne(self):
        unloadWidgetsList = [uiConst.WIDGET_SELECT_JOB_TWO, uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC]
        unloadWidgetsList.append(uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST)
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        gameglobal.rds.loginScene.gotoSelectOneStage()
        self.loadAllSCWidgets()
        self.school = gameglobal.rds.loginScene.selectSchool
        self.gender = gameglobal.rds.loginScene.selectGender
        self.bodyType = gameglobal.rds.loginScene.selectBodyType
        self.applyAvatarConfig = False
        self.showDescription(-1)
        self.showNavigation()
        if self.jobListMed:
            self.jobListMed.Invoke('setSelected', GfxValue(self.school))

    def gotoJobSelectZero(self):
        gameglobal.rds.loginScene.unloadWidgets([uiConst.BUTTON_CHARACTER_NEXT, uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC])
        gameglobal.rds.loginScene.gotoSelectZeroStage()
        self.loadAllSCWidgets()
        self.endMovie()
        if self.jobListMed:
            self.jobListMed.Invoke('clearSelected')
        self.showNavigation()

    def returnToCreate(self, isCreateNew = False):
        self.clearAllSCWidgets()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_NAVIGATION)
        if gameglobal.rds.loginScene.inBodyTypeStage():
            gameglobal.rds.loginScene.clearLoginModel()
        else:
            gameglobal.rds.loginScene.hideLoginModels()
        gameglobal.rds.ui.characterCreate.returnToCreate(isCreateNew)

    def genRandCharacterIdx(self, school, gender, bodyType):
        csd = gameglobal.rds.loginScene.getCharShowData(school, gender, bodyType)
        template = csd.get('template', [])
        idx = random.randint(0, len(template) - 1)
        return idx

    def fetchAvatarConfig(self, school, gender, bodyType, idx, applyAvatarConfig = False):
        if applyAvatarConfig:
            chooseAvatarData = gameglobal.rds.ui.characterCreate.getChooseAvatar()
            physique = chooseAvatarData.get('physique')
            hair = physique.hair if physique else 1
            avatarConfig = chooseAvatarData.get('avatarConfig', '')
            return (hair, avatarConfig)
        csd = gameglobal.rds.loginScene.getCharShowData(school, gender, bodyType)
        template = csd.get('template', [])
        avatarInfo = None
        if idx >= 0 and idx < len(template):
            filePath = '%s/char/%d_%d_%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH,
             gender,
             bodyType,
             template[idx])
            avatarInfo = ResMgr.openSection(filePath)
        if avatarInfo:
            hair = avatarInfo.readInt('hair')
            avatarConfig = avatarInfo.readString('avatarConfig')
        else:
            hair = csd.get('hair', 0)
            avatarConfig = ''
        return (hair, avatarConfig)

    def onClickNext(self, *arg):
        gamelog.debug('onClickNext')
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        if gameglobal.rds.loginScene.inSelectOneStage():
            if isinstance(CC.TC, BigWorld.FreeCamera):
                gameglobal.rds.loginScene._directlyEnterCharacterSelectTwo()
            else:
                gameglobal.rds.loginScene.startEnterCharacterSelectTwo()
                self.endMovie()
        elif gameglobal.rds.loginScene.inSelectTwoStage():
            gameglobal.rds.loginScene.unloadWidgets([uiConst.BUTTON_CHARACTER_NEXT, uiConst.WIDGET_SELECT_JOB_TWO])
            self.onClickCharacterDetail()
        elif gameglobal.rds.loginScene.inBodyTypeStage():
            gameglobal.rds.loginScene.unloadWidgets([uiConst.BUTTON_CHARACTER_NEXT, uiConst.WIDGET_SELECT_JOB_TWO])
            if gameglobal.rds.loginScene.inBodyTypeSexStage():
                self.onClickCharacterDetail(gameglobal.rds.loginScene.STAGE_CHARACTER_AVATARCONFIG_2_SUB)
            elif gameglobal.rds.loginScene.inSchoolStage():
                self.onClickCharacterDetail(gameglobal.rds.loginScene.STAGE_CHARACTER_SCHOOL_AVATARCONFIG)
            else:
                self.onClickCharacterDetail(gameglobal.rds.loginScene.STAGE_CHARACTER_AVATARCONFIG_2)

    def onClickReturn(self, *arg):
        gamelog.debug('onClickReturn')
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        if gameglobal.rds.loginScene.inSelectZeroStage():
            gameglobal.rds.loginScene.unloadWidgets([uiConst.BUTTON_CHARACTER_RETURN, uiConst.BUTTON_CHARACTER_NEXT])
            self.onClickReturnCreate()
        if gameglobal.rds.loginScene.inSelectTwoStage():
            if gameglobal.rds.loginManager.zhiShengGbId:
                unloadWidgetsList = [uiConst.WIDGET_SELECT_JOB_TWO,
                 uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC,
                 uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST,
                 uiConst.BUTTON_CHARACTER_RETURN,
                 uiConst.BUTTON_CHARACTER_NEXT]
                gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
                self.onClickReturnCreate()
            else:
                self.gotoJobSelectOne()
                gameglobal.rds.loginScene.returnCharacterSelectOne()
        elif gameglobal.rds.loginScene.inSelectOneStage():
            gameglobal.rds.loginScene.leaveCharacterSelectOne()
        elif gameglobal.rds.loginScene.inAvatarStage():
            gameglobal.rds.ui.characterDetailAdjust.openReturnWidget()
        elif gameglobal.rds.loginScene.inBodyTypeStage():
            gameglobal.rds.loginScene.unloadWidgets([uiConst.BUTTON_CHARACTER_RETURN, uiConst.BUTTON_CHARACTER_NEXT, uiConst.WIDGET_SELECT_JOB_TWO])
            self.onClickReturnCreate()

    def playMovie(self):
        w = 270
        h = 150
        x = 1
        y = 1
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
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/CharacterSelectJobDescWidget' + self.uiAdapter.getUIExt(), 'unitDesc', 270, 150)
        self.cgPlayer.playMovie('school_%d' % self.school, config)
        Sound.enableMusic(False)

    def onMovieEnd(self):
        self.setPlayBtnVisible(True)
        Sound.enableMusic(True)

    def setPlayBtnVisible(self, vis):
        if self.jobDescMed:
            self.jobDescMed.Invoke('setPlayBtnVisible', GfxValue(vis))

    def endMovie(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None
            Sound.enableMusic(True)

    def onClickPlayMovie(self, *arg):
        self.playMovie()

    def onGetSelectInfo(self, *arg):
        school = int(arg[3][0].GetNumber())
        schoolName = SD.data.get(school, {}).get('name', '')
        csd = loginScene.getCharShowData().get(school, [])
        for data in csd:
            if data.get('showModel', 0):
                desc = data.get('showDescription', '')
                ret = [schoolName, desc]
                return uiUtils.array2GfxAarry(ret, True)

    def onClickBodyType(self, *arg):
        account = BigWorld.player()
        character = self.uiAdapter.characterCreate.getChooseAvatar()
        gbID = character.get('gbID', 0)
        player = gameglobal.rds.loginScene.player
        self.uiAdapter.characterDetailAdjust.saveMorpher(player)
        if not self.uiAdapter.characterDetailAdjust.checkCanCreate():
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

    def onEnableMale2(self, *arg):
        ret = gameglobal.rds.configData.get('enableMale2', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)
        return GfxValue(ret)

    def findSameBodyType(self, school):
        csd = loginScene.getCharShowData().get(school, [])
        chooseAvatarData = gameglobal.rds.ui.characterCreate.getChooseAvatar()
        for i, data in enumerate(csd):
            if not (gameglobal.rds.configData.get('enableCreateFemale3Yecha', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)) and data['sex'] == const.SEX_FEMALE and data['bodyType'] == const.BODY_TYPE_3 and school == const.SCHOOL_YECHA:
                continue
            if not (gameglobal.rds.configData.get('enableCreateFemale2Yantian', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)) and data['sex'] == const.SEX_FEMALE and data['bodyType'] == const.BODY_TYPE_2 and school == const.SCHOOL_YANTIAN:
                continue
            if data.get('sex', const.SEX_UNKNOWN) == chooseAvatarData['physique'].sex and data.get('bodyType') == chooseAvatarData['physique'].bodyType:
                gender = chooseAvatarData['physique'].sex
                bodyType = chooseAvatarData['physique'].bodyType
                bodyIdx = i
                return (gender, bodyType, bodyIdx)

    def onEnableSchoolChange(self, *arg):
        ret = gameglobal.rds.loginScene.inSchoolStage() and bool(self.findSameBodyType(self.school))
        return GfxValue(ret)
