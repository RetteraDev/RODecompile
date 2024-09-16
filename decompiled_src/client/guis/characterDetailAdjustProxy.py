#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterDetailAdjustProxy.o
from gamestrings import gameStrings
import os
import time
import cPickle
import BigWorld
import C_ui
from Scaleform import GfxValue
import ResMgr
import Sound
import utils
import gameglobal
import gametypes
import gamelog
import const
import keys
import commcalc
import clientcom
import clientUtils
from guis import ui
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from helpers import avatarMorpher as AM
from helpers import avatarMorpherUtils as AMU
from helpers import dyeMorpher
from helpers import charRes, taboo
from helpers import cgPlayer
from helpers import tintalt as TA
from helpers import capturePhoto
from callbackHelper import Functor
from gamestrings import gameStrings
from cdata import suit_data as SD
from data import equip_data as ED
from data import sys_config_data as SCD
from data import char_show_new_data as CSD
PATH = '../game/avatar/'
AUTO_SAVE = gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_43

class CharacterDetailAdjustProxy(DataProxy):
    SAVE_INTERVAL = 30

    def __init__(self, uiAdapter):
        super(CharacterDetailAdjustProxy, self).__init__(uiAdapter)
        self.bindType = 'characterDetailAdjust'
        self.modelMap = {'clickFaceAdjust': self.onClickFaceAdjust,
         'clickBodyAdjust': self.onClickBodyAdjust,
         'clickReturnSelect': self.onClickReturnSelect,
         'clickFashion': self.onClickFashion,
         'clickEmotion': self.onClickEmotion,
         'clickFaceEmotion': self.onClickFaceEmotion,
         'enableFaceEmote': self.onEnableFaceEmote,
         'clickSound': self.onClickSound,
         'changeFxType': self.onChangeFxType,
         'clickCharacter': self.onClickCharacter,
         'downClickLeftRotate': self.onDownClickLeftRotate,
         'downClickRightRotate': self.onDownClickRightRotate,
         'upClickRotate': self.onUpClickRotate,
         'clickZoomIn': self.onClickZoomIn,
         'clickZoomOut': self.onClickZoomOut,
         'clickReset': self.onClickReset,
         'handleFaceZBBtn': self.onHandleFaceZBBtn,
         'handleFaceZBSlider': self.onHandleFaceZBSlider,
         'handleColorBtn': self.onHandleColorBtn,
         'clickCreateCharacter': self.onClickCreateCharacter,
         'saveAvatarConfig': self.onSaveAvatarConfig,
         'readAvatarConfig': self.onReadAvatarConfig,
         'saveNpcConfig': self.onSaveNpcConfig,
         'getNpcFashion': self.onGetNpcFashion,
         'exportNpcFile': self.onExportNpcFile,
         'exportObjFile': self.onExportObjFile,
         'getFashionDesc': self.onGetFashionDesc,
         'exportTintInfo': self.onExportTintInfo,
         'updateDyeInfo': self.onUpdateDyeInfo,
         'clickItemAdjust': self.onClickItemAdjust,
         'handleSliderChange': self.onHandleSliderChange,
         'closeNameInput': self.onCloseNameInput,
         'createRole': self.onCreateRole,
         'createRoleCiKe': self.onCreateRoleCiKe,
         'closeReturn': self.onCloseReturn,
         'continueReturn': self.onContinueReturn,
         'continueReturnSave': self.onContinueReturnSave,
         'closeReset': self.onCloseReset,
         'resetAvatar': self.onResetAvatar,
         'resetSaveAvatar': self.onResetSaveAvatar,
         'resetAvatarConfig': self.onResetAvatarConfig,
         'clickRandom': self.onClickRandom,
         'clickRecover': self.onClickRecover,
         'closeTips': self.onCloseTips,
         'getLookAtChoice': self.onGetLookAtChoice,
         'setLookAtChoice': self.onSetLookAtChoice,
         'clickPlayMovie': self.onClickPlayMovie,
         'setMovieType': self.onSetMovieType,
         'getWingIDs': self.onGetWingIDs,
         'showWing': self.onShowWing,
         'showMovieDetail': self.onShowMovieDetail,
         'getAvatarVideoAndWingCfg': self.onGetAvatarVideoAndWingCfg,
         'clickWeather': self.onClickWeather,
         'enableWeather': self.onEnableWeather,
         'clickUploadCharacter': self.onClickUploadCharacter,
         'enableUpload': self.onEnableUpload,
         'clickShareEnter': self.onClickShareEnter,
         'clickShareQuit': self.onClickShareQuit,
         'useOldAvatarConfig': self.onUseOldAvatarConfig,
         'getCreateBtnName': self.onGetCreateBtnName,
         'enableUseOldAvatarConfig': self.onEnableUseOldAvatarConfig,
         'randomRoleName': self.onRandomRoleName}
        self.autoSaveHandle = None
        self.operationLog = None
        self.isCharacterPhotoUpload = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_TIP, 'unLoadWidget')
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_SHARE, 'unLoadWidget')

    def reset(self):
        self.refreshUI = True
        self.avatarMorpher = None
        self.hairStyle = 0
        self.isRotate = True
        self.tipVisible = 0
        self.avatarData = None
        self.suitId = 0
        self.characterId = 0
        self.detailAdjustMed = None
        self.characterNameMed = None
        self.actSoundMed = None
        if self.autoSaveHandle:
            BigWorld.cancelCallback(self.autoSaveHandle)
        self.autoSaveHandle = None
        if self.operationLog:
            self.operationLog.release()
        self.operationLog = None
        self.itemData = None
        self.tipMediator = None
        self.GSNumberInputMediator = None
        self.enableLookAt = True
        self.cgPlayer = None
        self.videoName = SCD.data.get('loginSceneVideos', [{}])[0].get('video', 'xizao')
        self.videoWeb = SCD.data.get('loginSceneVideos', [{}])[0].get('web', 'http://tianyu.163.com')
        gameglobal.rds.loginScene.wingActionId = str(CSD.data.get(gameglobal.rds.loginScene.selectSchool, [{}])[0].get('wingActionId', '21101'))
        self.endMovie()
        self.characterClickInfo = {}
        self.hasSelfAvatar = False
        self.headGen = None
        self.uploadAvatarConfig = None
        self.uploadSum = 6
        self.allUploadKeys = []
        self.nuid = None
        self.uploadCallback = None

    def addCharacterClickInfo(self, id):
        id += 1
        id = str(id)
        self.characterClickInfo.setdefault('character', {})
        self.characterClickInfo['character'].setdefault(id, 0)
        self.characterClickInfo['character'][id] += 1

    def addHairClickInfo(self, id):
        id += 1
        id = str(id)
        self.characterClickInfo.setdefault('hair', {})
        self.characterClickInfo['hair'].setdefault(id, 0)
        self.characterClickInfo['hair'][id] += 1

    def _registerMediator(self, widgetId, mediator):
        gamelog.debug('b.e.:init widget', widgetId, mediator)
        if widgetId == uiConst.WIDGET_AVATAR_DETAIL_ADJUST_NEW:
            self.detailAdjustMed = mediator
            return uiUtils.dict2GfxDict({'useLoginSceneNew': True})
        if widgetId == uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW:
            self.characterNameMed = mediator
            isInternationalVersion = utils.isInternationalVersion()
            if gameglobal.rds.loginScene.inCreateStage():
                return uiUtils.dict2GfxDict({'titleName': gameStrings.DESC_TITLE_CHANGE_NAME,
                 'createLabel': gameStrings.DESC_BTN_CHANGE_NAME,
                 'maxChars': const.MAX_CHAR_NAME,
                 'isInternationalVersion': isInternationalVersion}, True)
            else:
                return uiUtils.dict2GfxDict({'maxChars': const.MAX_CHAR_NAME,
                 'isInternationalVersion': isInternationalVersion})
        else:
            if widgetId == uiConst.WIDGET_CHARACTER_ACT_SOUND_NEW:
                self.actSoundMed = mediator
                fxTypeNames = SCD.data.get('fxTypeNames', {})
                return uiUtils.array2GfxAarry(fxTypeNames.items(), True)
            if widgetId == uiConst.WIDGET_TIP:
                self.tipMediator = mediator
            elif widgetId == uiConst.WIDGET_CHARACTER_SHARE:
                if self.nuid:
                    return GfxValue(uiUtils.getQRCodeBuff(self.nuid, 4))
                else:
                    return GfxValue('')

    def getValue(self, key):
        if key == 'characterDetailAdjust.msg':
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(self.tipVisible))
            ar.SetElement(1, GfxValue(gbk2unicode(self.msg)))
            self.tipVisible = 0
            return ar
        if key == 'characterDetailAdjust.init':
            school = gameglobal.rds.loginScene.selectSchool
            gender = gameglobal.rds.loginScene.selectGender
            bodyType = gameglobal.rds.loginScene.selectBodyType
            bodyIdx = gameglobal.rds.loginScene.bodyIdx
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gender))
            ar.SetElement(1, GfxValue(bodyType))
            ar.SetElement(2, GfxValue(bodyIdx))
            ar.SetElement(3, GfxValue(school))
            diableInfo = AM.getDisableMorpherInfoFromAvatar(gameglobal.rds.loginScene.player)
            ar.SetElement(4, uiUtils.dict2GfxDict(diableInfo))
            ar.SetElement(5, uiUtils.dict2GfxDict(dyeMorpher.getDyeColorFromAvatar(gameglobal.rds.loginScene.player)))
            ar.SetElement(6, GfxValue(gameglobal.rds.loginScene.inDetailAdjustStage()))
            csd = gameglobal.rds.loginScene.getCharShowData(school, gender, bodyType)
            newIcon = csd.get('newIcon', [])
            tips = csd.get('tips', [])
            ar.SetElement(7, uiUtils.array2GfxAarry(newIcon))
            ar.SetElement(8, uiUtils.array2GfxAarry(tips, True))
            return ar
        if key == 'characterDetailAdjust.setData':
            return self.avatarData

    def setFaceAdjustVisible(self, faceAdjustFlag):
        if self.faceAdjustMed:
            self.faceAdjustMed.Invoke('setVisible', GfxValue(faceAdjustFlag))

    def setBodyAdjustVisible(self, bodyAdjustFlag):
        if self.bodyAdjustMed:
            self.bodyAdjustMed.Invoke('setVisible', GfxValue(bodyAdjustFlag))

    def clearAllCDWidgets(self):
        self.hide()

    def loadAllCDWidgets(self):
        loadWidgetsList = [uiConst.WIDGET_AVATAR_BASIC_NEW,
         uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB,
         uiConst.WIDGET_AVATAR_DETAIL_ADJUST_NEW,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW,
         uiConst.WIDGET_CHARACTER_ACT_SOUND_NEW,
         uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_BOTTOM,
         uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW]
        if gameglobal.rds.loginScene.inAvatarconfigStage() or gameglobal.rds.loginScene.inAvatarconfigStage2():
            if gameglobal.rds.loginScene.inSchoolAvatarConfigStage():
                character = gameglobal.rds.ui.characterCreate.getChooseAvatar()
                if character:
                    myBodyType = character['physique'].bodyType
                    myGender = character['physique'].sex
                    if myBodyType == gameglobal.rds.loginScene.selectBodyType and myGender == gameglobal.rds.loginScene.selectGender:
                        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_USE_CONFIG_BTN)
            else:
                loadWidgetsList.remove(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW)
                loadWidgetsList.append(uiConst.WIDGET_BODYTYPE_BUTTON_NEW)
        if BigWorld.isPublishedVersion():
            if uiConst.WIDGET_SAVEAVATARCONFIG in loadWidgetsList:
                loadWidgetsList.remove(uiConst.WIDGET_SAVEAVATARCONFIG)
        gameglobal.rds.loginScene.loadWidgets(loadWidgetsList)
        if self.autoSaveHandle:
            BigWorld.cancelCallback(self.autoSaveHandle)
        BigWorld.callback(self.SAVE_INTERVAL, self._autoSave)
        self.operationLog = OperationLog()
        self.adjustStartTime = utils.getNow()
        BigWorld.projection().nearPlane = 0.25
        gameglobal.rds.ui.realSense.initCamera()

    def _autoSave(self):
        if gameglobal.rds.loginScene.inDetailAdjustStage():
            self.onSaveNpcConfig()
            self.autoSaveHandle = BigWorld.callback(self.SAVE_INTERVAL, self._autoSave)
            if gameglobal.rds.configData.get('isReservationOnlyServer', False):
                deadLine = time.struct_time([2015,
                 6,
                 19,
                 8,
                 0,
                 0,
                 0,
                 0,
                 0])
                if utils.getNow() < time.mktime(deadLine):
                    BigWorld.callback(5, Functor(self.uiAdapter.systemTips.show, gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_297))

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        unloadWidgetsList = [uiConst.WIDGET_SAVEAVATARCONFIG,
         uiConst.WIDGET_LOOK_AT,
         uiConst.WIDGET_CHARACTER_SHARE,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_USE_CONFIG_BTN]
        unloadWidgetsList.extend([uiConst.WIDGET_CHARACTER_ACT_SOUND_NEW,
         uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_BOTTOM,
         uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW,
         uiConst.WIDGET_AVATAR_BASIC_NEW,
         uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB,
         uiConst.WIDGET_AVATAR_DETAIL_ADJUST_NEW,
         uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW,
         uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_RETURN_BUTTON_NEW,
         uiConst.WIDGET_BODYTYPE_BUTTON_NEW])
        self.closeTips()
        self.endMovie()
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        gameglobal.rds.ui.realSense.hide()
        self.onClickWeather(0)

    def onClickFaceAdjust(self, *arg):
        self._faceAdjust()

    def onClickBodyAdjust(self, *arg):
        self._bodyAdjust()

    def _faceAdjust(self):
        self.setFaceAdjustVisible(True)
        self.setBodyAdjustVisible(False)
        gameglobal.rds.loginScene.zoomIn()

    def _bodyAdjust(self):
        self.setFaceAdjustVisible(False)
        self.setBodyAdjustVisible(True)
        gameglobal.rds.loginScene.zoomOut()

    def onClickReturnSelect(self, *arg):
        if gameglobal.rds.loginScene.inAvatarconfigStage():
            self.returnToCreate(False)
            return
        if gameglobal.rds.loginScene.inDetailAdjustStage():
            self.clearAllCDWidgets()
            gameglobal.rds.loginScene.isZoom = uiConst.ZOOMOUT
            gameglobal.rds.loginScene.clearPlayer()
            gameglobal.rds.loginScene.gotoCharCreateNewStage()
        elif gameglobal.rds.loginScene.inAvatarconfigStage2():
            self.returnToCreate(False)

    def onClickItemAdjust(self, *arg):
        topUI = arg[3][0].GetString()
        subUI = arg[3][1].GetString()
        gamelog.debug('onClickItemAdjust', topUI, subUI)
        self.clickItemAdjust(subUI)

    def clickItemAdjust(self, subUI):
        if self.detailAdjustMed:
            self.detailAdjustMed.Invoke('selectSubUI', GfxValue(subUI))

    def onClickFashion(self, *arg):
        key = int(arg[3][0].GetNumber())
        p = gameglobal.rds.loginScene.player
        gamelog.debug('b.e.: onClickFashion', key)
        self.downWing()
        csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
        cloth = csd.get('cloth')
        actions = csd.get('actions')
        if cloth and key < len(cloth):
            suitId = cloth[key]
        else:
            suitId = 0
        if self.suitId == suitId:
            return
        else:
            self.suitId = suitId
            self._updateSuit(self.suitId, p)
            if hasattr(p, 'fashion'):
                dressAction = csd.get('dressAction')
                if dressAction is not None:
                    p.fashion.playActionSequence(p.model, (dressAction,), self._onEndEmotion)
                    p.am.matchCaps = [actions[0][1], keys.CAPS_AVATAR_IDLE]
            return

    def onClickEmotion(self, *arg):
        key = int(arg[3][0].GetNumber())
        p = gameglobal.rds.loginScene.player
        gamelog.debug('b.e.: onClickEmotion', key)
        self.downWing()
        if hasattr(p, 'am') and hasattr(p, 'fashion'):
            csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
            actions = csd.get('actions')
            if actions and key < len(actions):
                emotion = actions[key]
                if emotion is not None:
                    if key == 0:
                        self._setLookAtChoice(True) if self.enableLookAt else None
                    else:
                        self._setLookAtChoice(False)
                    p.am.matchCaps = [emotion[1], keys.CAPS_AVATAR_IDLE]
                    p.am.matcherCoupled = True
                    if emotion[0]:
                        p.fashion.playActionSequence(p.model, (emotion[0],), self._onEndEmotion)
                    else:
                        p.fashion.stopModelAction(p.model)

    def onClickFaceEmotion(self, *arg):
        key = int(arg[3][0].GetNumber())
        p = gameglobal.rds.loginScene.player
        gamelog.debug('b.e.: onClickFaceEmotion', key)
        csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
        faceEmotions = csd.get('faceEmotions')
        if faceEmotions and key < len(faceEmotions):
            faceEmotion = faceEmotions[key]
        if faceEmotion and key != 0:
            p.startFaceEmote(faceEmotion)
        else:
            p.endFaceEmote()

    def onEnableFaceEmote(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableFaceEmote', False))

    def _onEndEmotion(self):
        p = gameglobal.rds.loginScene.player
        if p and hasattr(p, 'am'):
            p.am.matcherCoupled = True

    def onClickSound(self, *arg):
        key = int(arg[3][0].GetNumber())
        p = gameglobal.rds.loginScene.player
        if hasattr(p, 'am') and hasattr(p, 'fashion'):
            csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
            fxs = csd.get('fxs')
            if fxs and key < len(fxs):
                fx = fxs[key]
                if fx is not None:
                    gameglobal.rds.sound.playFx(fx, BigWorld.player().position, False, BigWorld.player())

    def onChangeFxType(self, *arg):
        fxType = int(arg[3][0].GetNumber())
        if self.avatarMorpher:
            self.avatarMorpher.fxType = fxType
            Sound.setFxStyle(fxType)

    def onClickCharacter(self, *arg):
        try:
            key = int(arg[3][0].GetNumber())
        except:
            key = arg[0]

        gamelog.debug('b.e.: onClickCharacter', key)
        self._onClickCharacter(key)
        self.addCharacterClickInfo(key)
        self.hasSelfAvatar = False

    def _onClickCharacter(self, key):
        p = gameglobal.rds.loginScene.player
        if key == -1:
            key = gameglobal.rds.loginScene.genRandCharacterIdx(p.physique.school, p.physique.sex, p.physique.bodyType)
        self.characterId = key
        hair, avatarConfig = gameglobal.rds.loginScene.fetchAvatarConfig(p.physique.school, p.physique.sex, p.physique.bodyType, key)
        p.physique.hair = hair
        p.set_physique(None)
        if p.avatarConfig != avatarConfig:
            p.avatarConfig = avatarConfig
            self.refreshUI = True
            p.useAvatarConfig(None)

    def loadCharacterDetail(self):
        school = gameglobal.rds.loginScene.selectSchool
        gender = gameglobal.rds.loginScene.selectGender
        bodyType = gameglobal.rds.loginScene.selectBodyType
        gamelog.debug('b.e.: loadCharacterDetail', school, gender, bodyType)
        csd = gameglobal.rds.loginScene.getCharShowData(school, gender, bodyType)
        cloth = csd.get('cloth')
        self.suitId = cloth[0] if cloth else 0
        availableMorpher = {}
        character = self.uiAdapter.characterCreate.getChooseAvatar()
        if character:
            if gameglobal.rds.loginScene.inAvatarconfigStage() or gameglobal.rds.loginScene.inAvatarconfigStage2() and character['physique'].bodyType == bodyType and character['physique'].sex == gender:
                hair = character['physique'].hair
                avatarConfig = character['avatarConfig']
                availableMorpher = character.get('extra', {}).get('availableMorpher', {})
            elif gameglobal.rds.loginScene.inAvatarconfigStage2():
                availableMorpher = character.get('extra', {}).get('availableMorpher', {})
                hair, avatarConfig = gameglobal.rds.loginScene.fetchAvatarConfig(school, gender, bodyType, 0)
            else:
                hair, avatarConfig = gameglobal.rds.loginScene.fetchAvatarConfig(school, gender, bodyType, 0)
        else:
            hair, avatarConfig = gameglobal.rds.loginScene.fetchAvatarConfig(school, gender, bodyType, 0)
        self.refreshUI = True
        gameglobal.rds.loginScene.trackNo = 0
        gameglobal.rds.loginScene.createPlayer(school, gender, bodyType, True, hair, self.suitId, avatarConfig, availableMorpher)

    def _refreshFaceAndBody(self, modelId):
        if not self.refreshUI:
            return
        self.refreshUI = False
        self.avatarData = self._fetchAvatarInfo(modelId)
        if self.detailAdjustMed:
            self.detailAdjustMed.Invoke('setData', self.avatarData)

    def _fetchAvatarInfo(self, modelId):
        data = {'mobanItem': self.characterId,
         'faxing_style': self.avatarMorpher.getHairStyle() if self.avatarMorpher else 0}
        data.update(self._fetchBodyInfo(modelId))
        data.update(self._fetchFaceInfo(modelId))
        data.update(self._fetchDyeInfo(modelId))
        return uiUtils.dict2GfxDict(data)

    def _fetchFaceInfo(self, modelId):
        data = {}
        tmpData = {}
        resConfig = AM.getAvatarResConfig(modelId)
        if self.avatarMorpher:
            for k, v in self.avatarMorpher.faceBone.transformMap.iteritems():
                params = AMU.getUIParamByFaceMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

            for k, v in self.avatarMorpher.faceMorpher.transformMap.iteritems():
                params = AMU.getUIParamByFaceMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

        return data

    def _fetchBodyInfo(self, modelId):
        data = {}
        tmpData = {}
        resConfig = AM.getAvatarResConfig(modelId)
        if self.avatarMorpher:
            for k, v in self.avatarMorpher.bodyBone.transformMap.iteritems():
                params = AMU.getUIParamByBodyMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

        return data

    def _fetchDyeInfo(self, modelId):
        data = {}
        tmpData = {}
        isMale = charRes.retransGender(modelId) == const.SEX_MALE
        if self.avatarMorpher:
            for dyeMorpher in self.avatarMorpher.dyeMorpher.dyeMorphers.itervalues():
                for k, v in dyeMorpher.transformMap.iteritems():
                    params = AMU.getUIParamByDyeMorpher(k, dyeMorpher.getMorphRatio(v), isMale)
                    if params is not None:
                        self._fillDataValue(data, params[0], params[1], tmpData, params[1])

        return data

    def _fillDataValue(self, data, ui, value, tmpData, checkValue):
        tmpValue = tmpData.get(ui)
        if tmpValue:
            return
        tmpData[ui] = checkValue
        data[ui] = value

    def _updateSuit(self, suitId, p):
        self.saveMorpher(p)
        isFashion = utils.setDefaultSuit(suitId, p.physique.school, p.aspect, SD, ED)
        p.set_aspect(None)
        old_signal = p.signal
        signal = commcalc.setSingleBit(old_signal, gametypes.SIGNAL_SHOW_FASHION, isFashion)
        p.signal = signal
        p.set_signal(old_signal)

    def setMsg(self, msg):
        gamelog.debug('hjxmsg:', msg)
        self.msg = msg

    def onCloseTips(self, *arg):
        self.tipMediator = None

    def closeTips(self):
        self.onCloseTips(0)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TIP)

    def showTips(self, msg, visible = 0):
        self.tipVisible = visible
        self.setMsg(msg)
        if self.tipMediator:
            self.tipMediator.Invoke('updateMsg', GfxValue(gbk2unicode(msg)))
            self.tipMediator.Invoke('setBtnVisible', GfxValue(visible))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TIP, True)

    def _initAvatarMorpher(self, p):
        if self.avatarMorpher is None:
            self.avatarMorpher = AM.AvatarModelMorpher(p.id)
        self.operationLog.set(self)

    def clear(self):
        self.avatarMorpher = None
        self.hairStyle = 0
        self.endMovie()

    def applyMorpher(self, entity = None):
        if entity == None:
            return
        else:
            self.avatarMorpher = None
            modelId = charRes.transDummyBodyType(entity.physique.sex, entity.physique.bodyType, True)
            gamelog.debug('b.e.:applyMorpher', entity.id, modelId, len(entity.avatarConfig))
            self._initAvatarMorpher(entity)
            self.avatarMorpher.readConfig(entity.avatarConfig)
            self.avatarMorpher.apply(False)
            self._refreshFaceAndBody(modelId)
            gameglobal.rds.loginScene.getPlayerHeight()
            BigWorld.callback(0.1, Functor(self.adjustCamera, entity.physique.sex, entity.physique.bodyType))
            BigWorld.callback(0.5, Functor(self.adjustCamera, entity.physique.sex, entity.physique.bodyType))
            if self.enableLookAt:
                self._setLookAtChoice(self.enableLookAt)
            return

    def adjustCamera(self, sex, bodyType):
        gameglobal.rds.loginScene.moveToDestination(gameglobal.rds.loginScene.trackNo, 'detailAdjust_%d_%d.track' % (sex, bodyType))

    def saveMorpher(self, entity = None, needCompress = True, needEncrypt = False):
        if entity == None:
            return
        else:
            if not self.avatarMorpher:
                self.avatarMorpher = AM.AvatarModelMorpher(entity.id)
                self.avatarMorpher.readConfig(getattr(entity, 'avatarConfig', ''))
            if self.avatarMorpher:
                entity.avatarConfig = self.avatarMorpher.export(entity.avatarConfig, needCompress, needEncrypt)
            return

    def onDownClickLeftRotate(self, *arg):
        self.isRotate = True
        gameglobal.rds.loginScene.turnLeft()

    def onDownClickRightRotate(self, *arg):
        gamelog.debug('b.e.:onDownClickRightRotate')
        self.isRotate = True
        gameglobal.rds.loginScene.turnRight()

    def onUpClickRotate(self, *arg):
        self.isRotate = False
        self._onEndEmotion()

    def onClickZoomIn(self, *arg):
        gameglobal.rds.loginScene.zoomIn()

    def onClickZoomOut(self, *arg):
        gameglobal.rds.loginScene.zoomOut()

    def onClickReset(self, *arg):
        self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_662)

    def onHandleSliderChange(self, *arg):
        self.operationLog.record()
        sliderName = arg[3][0].GetString()
        value = float(arg[3][1].GetNumber())
        self._onHandleSliderChange(sliderName, value)

    def _onHandleSliderChange(self, sliderName, value, enableApply = True):
        self.hasSelfAvatar = True
        p = gameglobal.rds.loginScene.player
        if not p or not hasattr(p, 'physique'):
            return
        else:
            modelId = charRes.transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
            gamelog.debug('b.e.:onHandleFaceSlider', sliderName, value)
            if not self.avatarMorpher:
                return
            resConfig = AM.getAvatarResConfig(modelId)
            if sliderName in AMU.FACE_U2M_MAPPING.keys():
                params = AMU.getFaceMorpherParamByUI(sliderName, value, resConfig)
                if params is None:
                    return
                if params[0] == 0:
                    if enableApply:
                        self.avatarMorpher.setAndApplyFaceBoneMorph(params[1], params[2], params[3])
                    else:
                        self.avatarMorpher.setFaceBoneMorph(params[1], params[2], params[3])
                elif enableApply:
                    self.avatarMorpher.setAndApplyFaceMorph(params[1], params[2], params[3])
                else:
                    self.avatarMorpher.setFaceMorph(params[1], params[2], params[3])
            else:
                params = AMU.getBodyMorpherParamByUI(sliderName, value, resConfig)
                if params is None:
                    return
                if params[0] == 0:
                    if enableApply:
                        self.avatarMorpher.setAndApplyBodyBoneMorph(params[1], params[2], params[3])
                    else:
                        self.avatarMorpher.setBodyBoneMorph(params[1], params[2], params[3])
                if gameglobal.rds.loginScene.trackNo:
                    gameglobal.rds.loginScene.moveToDestination(gameglobal.rds.loginScene.trackNo, 'detailAdjust_%d_%d.track' % (p.physique.sex, p.physique.bodyType))
            return

    def onHandleFaceZBBtn(self, *arg):
        self.hasSelfAvatar = True
        self.operationLog.record()
        key = arg[3][0].GetString()
        value = int(arg[3][1].GetNumber())
        p = gameglobal.rds.loginScene.player
        gameglobal.rds.sound.playSound(gameglobal.SD_496)
        if not p:
            return
        else:
            isMale = p.physique.isMale()
            if not self.avatarMorpher:
                return
            if key == 'faxing_style':
                self.hairStyle = value
                self.addHairClickInfo(value)
                self.avatarMorpher.setHairStyle(value)
                self.saveMorpher(p)
                p.physique.hair = self.avatarMorpher.hair
                p.set_physique(None)
                self.resetFaceEmotionBtn()
                return
            if key == 'mobanItem':
                self.onClickCharacter(value)
                self.resetFaceEmotionBtn()
                return
            if key == 'faxing_color1':
                key = 'faxing_color'
                params = AMU.getDyeMorpherParamByUI(key, value, isMale)
                value = ('%d' % params[2], 'faxing_color1')
                self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)
                return
            params = AMU.getDyeMorpherParamByUI(key, value, isMale)
            gamelog.debug('b.e.:onHandleFaceZBBtn', key, value, params)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], params[2])
            return

    def onHandleFaceZBSlider(self, *arg):
        self.hasSelfAvatar = True
        self.operationLog.record()
        key = arg[3][0].GetString()
        value = float(arg[3][1].GetNumber())
        p = gameglobal.rds.loginScene.player
        isMale = p.physique.isMale()
        gamelog.debug('b.e.:onHandleFaceZBSlider', key, value)
        if not self.avatarMorpher:
            return
        else:
            params = AMU.getDyeMorpherParamByUI(key, value, isMale)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                gamelog.debug('onHandleFaceZBSlider', params, AMU.DYE_MORPH_BINDING[params[1]])
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], params[2])
            return

    def onHandleColorBtn(self, *arg):
        self.hasSelfAvatar = True
        self.operationLog.record()
        key = arg[3][0].GetString()
        r = int(arg[3][1].GetNumber())
        g = int(arg[3][2].GetNumber())
        b = int(arg[3][3].GetNumber())
        alpha = int(arg[3][4].GetNumber())
        if alpha == 0:
            alpha = 255
        value = ('%d,%d,%d,%d' % (r,
          g,
          b,
          alpha),)
        if key == 'faxing_color1':
            key = 'faxing_color'
            value = value + ('faxing_color1',)
        p = gameglobal.rds.loginScene.player
        isMale = p.physique.isMale()
        if not self.avatarMorpher:
            return
        else:
            params = AMU.getDyeMorpherParamByUI(key, 0, isMale)
            gamelog.debug('b.e.:onHandleColorBtn', key, value, params)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)
            gameglobal.rds.sound.playSound(gameglobal.SD_496)
            return

    def onClickCreateCharacter(self, *arg):
        self.clickCreateCharacter()

    def clickCreateCharacter(self):
        if gameglobal.rds.loginScene.inSchoolAvatarConfigStage():
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.CHARACTER_DETAIL_ADJUST_NEW_BODY_TYPE_TIP, yesCallback=self._confirmChangeSchool)
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW, True)
        p = BigWorld.player()
        if hasattr(p.base, 'onAdjustCharactorDone'):
            p.base.onAdjustCharactorDone(utils.getNow() - self.adjustStartTime)

    def _confirmChangeSchool(self):
        account = BigWorld.player()
        character = self.uiAdapter.characterCreate.getChooseAvatar()
        gbID = character.get('gbID', 0)
        player = gameglobal.rds.loginScene.player
        self.saveMorpher(player)
        if not self.checkCanCreate():
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

    def getCharacterClickInfo(self):
        return (self.characterClickInfo,
         self.characterId + 1,
         self.hairStyle + 1,
         self.hasSelfAvatar)

    def onCloseNameInput(self, *arg):
        self.characterNameMed = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW)

    def setErrorMsg(self, data):
        if self.characterNameMed:
            self.characterNameMed.Invoke('setErrorMsg', GfxValue(gbk2unicode(data)))
        else:
            gameglobal.rds.ui.systemTips.show(data)

    def checkForceChangeName(self, newName):
        try:
            newName = unicode2gbk(newName)
        except UnicodeError:
            return False

        if not newName:
            return False
        if len(newName) > const.MAX_CHAR_NAME:
            return False
        retval, newName = taboo.checkNameDisWord(newName)
        if not retval:
            return False
        return True

    def checkName(self, newName):
        try:
            newName = unicode2gbk(newName)
        except UnicodeError:
            self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_859)
            return False

        if not newName:
            self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_862)
            return False
        if len(newName) > 32:
            self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_865)
            return False
        return True

    @ui.callFilter(uiConst.CREATE_CHARACTER_INTERVAL)
    def onCreateRole(self, *arg):
        if gameglobal.rds.loginScene.inCreateStage():
            gameglobal.rds.ui.loginSelectServer.onClickConfirmChange(*arg)
            return
        newName = arg[3][0].GetString()
        if not self.checkName(newName):
            return
        newName = unicode2gbk(newName)
        p = gameglobal.rds.loginScene.player
        if not p or not hasattr(p, 'physique'):
            return
        p.physique.face = 0
        self.saveMorpher(p)
        if not self.checkCanCreate():
            return
        gamelog.debug('jorsef enterGame:', newName, p.physique.sex, p.physique.school, p.physique.face, p.physique.hair, p.physique.bodyType, p.avatarConfig)
        BigWorld.player().base.createCharacter(newName, p.physique.sex, p.physique.school, p.physique.face, p.physique.hair, p.physique.bodyType, p.avatarConfig, gameglobal.rds.loginManager.zhiShengGbId)

    def onCreateRoleCiKe(self, *arg):
        newName = arg[3][0].GetString()
        if not self.checkName(newName):
            return
        newName = unicode2gbk(newName)
        p = gameglobal.rds.loginScene.player
        if not p or not hasattr(p, 'physique'):
            return
        p.physique.face = 0
        self.saveMorpher(p)
        if not self.checkCanCreate():
            return
        gamelog.debug('-----m.l enterGame:', newName, p.physique.sex, const.SCHOOL_YECHA, p.physique.face, p.physique.hair, p.physique.bodyType)
        BigWorld.player().base.createCharacter(newName, const.SEX_MALE, const.SCHOOL_YECHA, p.physique.face, p.physique.hair, const.BODY_TYPE_3, p.avatarConfig, gameglobal.rds.loginManager.zhiShengGbId)

    def reScreenshot(self):
        self.uploadAvatarConfig = None
        self.onClickUploadCharacter()

    @ui.callFilter(5)
    def onClickUploadCharacter(self, *arg):
        if arg and arg[0]:
            self.uploadCallback = arg[0]
        if gameglobal.rds.configData.get('enableCharacterSharePreview', False) and self.isCharacterPhotoUpload == False:
            self.uploadAvatarConfig = None
        account = BigWorld.player()
        if account.sharedCnt >= SCD.data.get('CharCfgShareCnt', 10):
            self.uiAdapter.systemTips.show(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_932)
            return
        else:
            if not self.headGen:
                self.headGen = capturePhoto.CharacterPhotoGen.getInstance('gui/taskmask.tga', 10)
            p = gameglobal.rds.loginScene.player if gameglobal.rds.GameState <= gametypes.GS_LOGIN else account
            if p and p.model:
                if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                    self.saveMorpher(p)
                if self.uploadAvatarConfig == p.avatarConfig:
                    if self.uploadSum == len(self.allUploadKeys):
                        self.onUploadPhoto(None)
                    else:
                        self.uiAdapter.systemTips.show(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_944)
                    return
                self.isCharacterPhotoUpload = False
                self.headGen.setModelFinishCallback(Functor(self.takeAndSavePhoto, 0))
                self.headGen.initFlashMesh()
                self.headGen.startCaptureEnt(p, ('1901',))
                self.allUploadKeys = []
                self.setUploadEnable(False)
            return

    def takeAndSavePhoto(self, index):
        if index == self.uploadSum:
            self.headGen.endCapture()
            p = gameglobal.rds.loginScene.player if gameglobal.rds.GameState <= gametypes.GS_LOGIN else BigWorld.player()
            self.uploadAvatarConfig = p.avatarConfig
            if gameglobal.rds.configData.get('enableCharacterSharePreview', False):
                gameglobal.rds.ui.characterSharePreview.show()
            else:
                self.uploadCharacterPhoto()
            return
        func = Functor(self.takeAndSavePhoto, index + 1)
        if index == 0:
            for i in xrange(0, 6):
                imgPath = 'character%d.jpg' % i
                try:
                    os.remove(imgPath)
                except:
                    pass

            BigWorld.callback(1.0, Functor(self.headGen.takeAndSave, index, func))
        else:
            self.headGen.takeAndSave(index, func)

    def uploadCharacterPhoto(self):
        account = BigWorld.player()
        self.setUploadEnable(True)
        for i in xrange(0, self.uploadSum):
            account.uploadNOSFile('../game/character%d.jpg' % i, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_CHAR_PHOTO, {'urs': account.playerName}, self.onUploadPhoto)

    def setUploadEnable(self, value):
        gameglobal.rds.ui.characterDetailAdjustCreateNew.setUploadEnable(value)

    def onUploadPhoto(self, key):
        if key:
            self.allUploadKeys.append(key)
        if self.uploadSum == len(self.allUploadKeys):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(SCD.data.get('confirmUploadCharacterMsg', ''), yesCallback=self.realUploadPhoto)

    def realUploadPhoto(self):
        account = BigWorld.player()
        if self.uploadAvatarConfig and self.allUploadKeys and len(self.allUploadKeys) == self.uploadSum:
            map = dict(zip(range(1, self.uploadSum + 1), self.allUploadKeys))
            if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                p = gameglobal.rds.loginScene.player
                if p and account and hasattr(account.base, 'uploadCharCfgData'):
                    account.base.uploadCharCfgData(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_998, p.physique.sex, p.physique.bodyType, cPickle.dumps(map), self.uploadAvatarConfig)
            elif self.uploadCallback:
                self.uploadCallback(cPickle.dumps(map))
                self.uploadCallback = None
        self.isCharacterPhotoUpload = True

    def onEnableUpload(self, *arg):
        return GfxValue(self.enableUpload())

    def enableUpload(self):
        return gameglobal.rds.configData.get('enableUploadCharacterPhoto', False)

    def onClickShareEnter(self, *arg):
        gamelog.debug('onClickShareEnter')
        clientcom.openFeedbackUrl('http://hd.tianyu.163.com/avatar/')

    def onClickShareQuit(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_SHARE)

    def openCreateCiKe(self):
        if self.characterNameMed:
            self.characterNameMed.Invoke('enableCreateCike')

    def checkCanCreate(self):
        p = gameglobal.rds.loginScene.player
        disableMorpher = AM.getDisableMorpher(p.availableMorpher, p.physique.sex, p.physique.bodyType, p.physique.school)
        disableHair = disableMorpher.get('faxing_style', {})
        disableZhuangshi = disableMorpher.get('zhuangshi_style', {})
        if self.avatarMorpher and not self.avatarMorpher.isValidHair():
            self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1028)
            return False
        elif p.physique.hair in disableHair:
            self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1031)
            return False
        else:
            if self.avatarMorpher and self.avatarMorpher.dyeMorpher:
                headDye = self.avatarMorpher.dyeMorpher.dyeMorphers.get('head', None)
                zhuangshi = headDye.transformMap['maskCTex'][1][0] if headDye else 0
                if zhuangshi in disableZhuangshi:
                    self.setErrorMsg(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1037)
                    return False
            return True

    def onSaveAvatarConfig(self, *arg):
        p = gameglobal.rds.loginScene.player
        configFile = '%d_%d_%d.xml' % (p.physique.sex, p.physique.bodyType, self.characterId + 1)
        if clientcom.isFileExist(PATH + configFile):
            os.remove(PATH + configFile)
        p = gameglobal.rds.loginScene.player
        self.saveMorpher(p, False)
        output = ResMgr.root.createSection(PATH + configFile)
        output.writeInt('school', p.physique.school)
        output.writeInt('gender', p.physique.sex)
        output.writeInt('bodyType', p.physique.bodyType)
        output.writeInt('hair', p.physique.hair)
        if p.isShowFashion():
            output.writeInt('body', p.aspect.fashionBody)
            output.writeInt('hand', p.aspect.fashionHand)
            output.writeInt('leg', p.aspect.fashionLeg)
            output.writeInt('shoe', p.aspect.fashionShoe)
            output.writeString('headDye', p.aspect.fashionHeadDyeList())
            output.writeString('bodyDye', p.aspect.fashionBodyDyeList())
            output.writeString('handDye', p.aspect.fashionHandDyeList())
            output.writeString('legDye', p.aspect.fashionLegDyeList())
            output.writeString('shoeDye', p.aspect.fashionShoeDyeList())
        else:
            output.writeInt('body', p.aspect.body)
            output.writeInt('hand', p.aspect.hand)
            output.writeInt('leg', p.aspect.leg)
            output.writeInt('shoe', p.aspect.shoe)
            output.writeString('headDye', p.aspect.headDyeList())
            output.writeString('bodyDye', p.aspect.bodyDyeList())
            output.writeString('handDye', p.aspect.handDyeList())
            output.writeString('legDye', p.aspect.legDyeList())
            output.writeString('shoeDye', p.aspect.shoeDyeList())
        output.writeString('avatarConfig', p.avatarConfig)
        output.save()
        self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1076 + PATH + configFile)

    def onSaveNpcConfig(self, *arg):
        strArg = arg[3][0].GetString() if arg else ''
        self.saveNpcConfig(strArg)

    def saveNpcConfig(self, strArg):
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            p = gameglobal.rds.loginScene.player
        else:
            p = BigWorld.player()
        if not p:
            return
        newName = AUTO_SAVE
        isAutoSave = True
        configFile = newName + time.strftime('%Y%m%d') + '.xml'
        try:
            if strArg == 'manual_save':
                newName = gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1094
                isAutoSave = False
                configFile = newName + time.strftime('%Y%m%d%H%M') + '.xml'
            elif gameglobal.rds.GameState > gametypes.GS_LOGIN:
                newName = p.realRoleName
                isAutoSave = False
                configFile = newName + time.strftime('%Y%m%d%H%M') + '.xml'
        except:
            pass

        if clientcom.isFileExist(PATH + configFile):
            os.remove(PATH + configFile)
        self.saveMorpher(p, True, True)
        school = p.physique.school
        gender = p.physique.sex
        bodyType = p.physique.bodyType
        hair = p.physique.hair
        output = ResMgr.root.createSection(PATH + configFile)
        if BigWorld.isPublishedVersion():
            output.writeInt('transModelId', 1)
        else:
            output.writeInt('transModelId', 0)
        output.writeInt('school', school)
        output.writeInt('gender', gender)
        output.writeInt('bodyType', bodyType)
        output.writeInt('hair', hair)
        output.writeInt('headType', charRes.HEAD_TYPE0)
        if BigWorld.isPublishedVersion():
            csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
            suitId = csd.get('cloth')[0]
            suitData = SD.data.get(suitId)
            for part in charRes.PARTS_ASPECT_BODY:
                partValue = suitData.get(part, charRes.PART_NOT_EQUIPPED)
                output.writeInt(part, partValue)

        else:
            for part in charRes.PARTS_ASPECT_BODY:
                isFound = False
                for path in p.model.sources:
                    path = path.split('/')[-1]
                    if path.find(part) != -1 or part == 'leg' and path.find('tui') != -1:
                        _, partValue, _, _ = path.split('_')
                        output.writeInt(part, int(partValue))
                        isFound = True
                        break

                if not isFound:
                    output.writeInt(part, charRes.PART_NOT_NEED)

        if p.isShowFashion():
            output.writeString('headDye', p.aspect.fashionHeadDyeList())
            output.writeString('bodyDye', p.aspect.fashionBodyDyeList())
            output.writeString('handDye', p.aspect.fashionHandDyeList())
            output.writeString('legDye', p.aspect.fashionLegDyeList())
            output.writeString('shoeDye', p.aspect.fashionShoeDyeList())
        else:
            output.writeString('headDye', p.aspect.headDyeList())
            output.writeString('bodyDye', p.aspect.bodyDyeList())
            output.writeString('handDye', p.aspect.handDyeList())
            output.writeString('legDye', p.aspect.legDyeList())
            output.writeString('shoeDye', p.aspect.shoeDyeList())
        output.writeString('avatarConfig', p.avatarConfig)
        try:
            output.save()
        except Exception as e:
            clientUtils.reportEngineException('%s %s' % (configFile, e.message))

        if isAutoSave:
            self.uiAdapter.systemTips.show(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1161 % configFile)
        else:
            self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1163 + PATH + configFile)

    def onReadAvatarConfig(self, *arg):
        self.readAvatarConfig()

    def readAvatarConfig(self):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            workPath += '\\avatar'
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174_1, workPath, self.readAvatarConfigFinish)
        else:
            path = C_ui.openFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174_1)
            self.readAvatarConfigFinish(path)

    def readAvatarConfigFinish(self, path):
        if not path or not (path.endswith('xml') or path.endswith('XML')):
            return
        else:
            i = path.rfind('\\')
            i = path.rfind('/') if i == -1 else i
            fileName = path if i == -1 else path[i + 1:]
            gamelog.debug('b.e.:onReadAvatarConfig', path, fileName)
            dataInfo = ResMgr.openSection(PATH + fileName)
            if not dataInfo:
                self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1188 + PATH)
                return
            p = gameglobal.rds.loginScene.player
            if not p:
                return
            itemData = clientcom._getAvatarConfigFromFile(dataInfo)
            self.itemData = itemData
            gender = itemData.get('sex')
            bodyType = itemData.get('bodyType')
            if p.physique.sex != gender or p.physique.bodyType != bodyType:
                self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1199)
                return
            hair = itemData.get('hair', 0)
            head = itemData.get('head')
            body = itemData.get('body')
            hand = itemData.get('hand')
            leg = itemData.get('leg')
            shoe = itemData.get('shoe')
            transModelId = itemData.get('transModelId', 1)
            dyesDict = itemData.get('dyesDict', {})
            avatarConfig = itemData.pop('avatarConfig')
            if transModelId:
                p.physique.hair = hair
                p.set_physique(None)
                p.aspect.set(gametypes.EQU_PART_HEAD, head, dyesDict.get('head', []))
                p.aspect.set(gametypes.EQU_PART_BODY, body, dyesDict.get('body', []))
                p.aspect.set(gametypes.EQU_PART_HAND, hand, dyesDict.get('hand', []))
                p.aspect.set(gametypes.EQU_PART_LEG, leg, dyesDict.get('leg', []))
                p.aspect.set(gametypes.EQU_PART_SHOE, shoe, dyesDict.get('shoe', []))
                p.set_aspect(None)
            else:
                p.physique.hair = hair
                p.modelServer.bodyUpdateFromData(itemData)
            self.applyAvatarConfig(avatarConfig)
            return

    def applyAvatarConfig(self, avatarConfig):
        p = gameglobal.rds.loginScene.player
        if p.avatarConfig != avatarConfig:
            p.avatarConfig = avatarConfig
            self.refreshUI = True
            p.useAvatarConfig(None)

    def onGetNpcFashion(self, *arg):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1240, workPath, self.getNpcFashionFinish)
        else:
            path = C_ui.openFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1240)
            self.getNpcFashionFinish(path)

    def getNpcFashionFinish(self, path):
        i = path.rfind('\\')
        i = path.rfind('/') if i == -1 else i
        modelName = path if i == -1 else path[i + 1:]
        try:
            bodyTypeStr, modelIdStr, _, _ = modelName.split('_')
        except:
            gamelog.error('The wrong model has choosed!')
            return

        p = gameglobal.rds.loginScene.player
        sex = p.physique.sex
        school = p.physique.school
        bodyType = p.physique.bodyType
        hair = p.physique.hair
        bodyType = charRes.transBodyType(sex, bodyType)
        if bodyType == int(bodyTypeStr):
            itemData = {'multiPart': True,
             'transModelId': 0,
             'bodyType': p.physique.bodyType,
             'school': school,
             'hair': hair,
             'shoe': charRes.PART_NOT_NEED,
             'leg': charRes.PART_NOT_NEED,
             'body': int(modelIdStr),
             'hand': charRes.PART_NOT_NEED,
             'sex': sex,
             'headType': 0}
            p.modelServer.bodyUpdateFromData(itemData)
        else:
            gamelog.error('The wrong model has choosed!')

    def onExportNpcFile(self, *arg):
        p = gameglobal.rds.loginScene.player
        path = list(p.model.sources)
        if len(path) == 4:
            newName = 'npcTest'
            if self.characterNameMed:
                try:
                    newName = unicode2gbk(self.characterNameMed.Invoke('getCharacterName').GetString())
                except UnicodeError:
                    self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1279)
                    return

            path = path[0:3]
            import os
            os.chdir('../res')
            clientcom.checkRes(path)
            os.system('UnionAvatar.py %s %s %s %s' % (path[0],
             path[1],
             path[2],
             newName))
            os.chdir('../game')
        else:
            self.showTips(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1288)

    def returnToCreate(self, isCreateNew = False):
        self.clearAllCDWidgets()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_NAVIGATION)
        gameglobal.rds.ui.characterCreate.returnToCreate(isCreateNew)

    def onGetFashionDesc(self, *arg):
        p = gameglobal.rds.loginScene.player
        key = int(arg[3][0].GetNumber())
        csd = gameglobal.rds.loginScene.getCharShowData(p.physique.school, p.physique.sex, p.physique.bodyType)
        cloth = csd.get('cloth')
        suitId = 0
        if cloth and key < len(cloth):
            suitId = cloth[key]
        desc = SD.data.get(suitId, {}).get('desc', '')
        return GfxValue(gbk2unicode(desc))

    def onExportObjFile(self, *arg):
        gamelog.debug('onExportObjFile')
        p = gameglobal.rds.loginScene.player
        p.am.matchCaps = []
        p.model.tpos()
        BigWorld.callback(1, p.model.saveAvatarToObj)

    def onExportTintInfo(self, *arg):
        model = gameglobal.rds.loginScene.player.model
        sources = model.sources
        propertyNamesVisual = []
        propertyKeysVisual = []
        propertyValuesVisual = []
        propertyNamesTint = []
        propertyKeysTint = []
        propertyValuesTint = []
        for source in sources:
            if source.find('head.model') != -1:
                modelPath = source[source.find('char'):]
                visualPath = modelPath.replace('.model', '.visual')
                tree = ResMgr.openSection(visualPath)
                renderSets = tree.openSections('renderSet')
                geometrys = renderSets[0].openSections('geometry')
                primitiveGroups = geometrys[0].openSections('primitiveGroup')
                materials = primitiveGroups[0].openSections('material')
                material = materials[0]
                propertyNamesVisual = material.readStrings('property')
                propertys = material.openSections('property')
                propertyKeysVisual = []
                propertyValuesVisual = []
                for property in propertys:
                    for key in property.keys():
                        propertyKeysVisual.append(key)
                        value = property.readString(key)
                        propertyValuesVisual.append(value)

        headInfo = self.avatarMorpher.dyeMorpher.exportTintInfo()['head']
        file = open('..\\res\\effect\\tintalt\\' + headInfo[0][0] + '.xml', 'r')
        tintInfos = file.readlines()
        file.close()
        tintInfos = tintInfos[3:]
        tintInfos = tintInfos[:-1]
        tintInfo = ''
        for item in tintInfos:
            tintInfo += item

        tintInfo = tintInfo % tuple(headInfo[0][1])
        tintInfo = '<root>\n' + tintInfo + '\n</root>'
        file = open('../../bigworld/tools/misc/bakeface/temp_liyy.xml', 'wb')
        file.write(tintInfo)
        file.close()
        ResMgr.purge('../tools/misc/bakeface/temp_liyy.xml')
        tree = ResMgr.openSection('../tools/misc/bakeface/temp_liyy.xml')
        Ta = tree.openSections('ta')[0]
        propertyNamesTint = Ta.readStrings('property')
        propertys = Ta.openSections('property')
        propertyKeysTint = []
        propertyValuesTint = []
        for property in propertys:
            for key in property.keys():
                propertyKeysTint.append(key)
                value = property.readString(key)
                propertyValuesTint.append(value)

        VisualDic = {}
        TintDic = {}
        for i in xrange(0, len(propertyNamesVisual)):
            VisualDic[propertyNamesVisual[i]] = (propertyKeysVisual[i], propertyValuesVisual[i])

        for i in xrange(0, len(propertyNamesTint)):
            TintDic[propertyNamesTint[i]] = (propertyKeysTint[i], propertyValuesTint[i])

        for key in VisualDic.keys():
            if TintDic.get(key) == None:
                TintDic[key] = VisualDic[key]

        file = open('../../bigworld/tools/misc/bakeface/temp_liyy.txt', 'wb')
        if headInfo[0][0] == 'avatarHead2':
            file.write('girl_face.fxo')
        elif headInfo[0][0] == 'avatarHead1':
            file.write('boy_face.fxo')
        file.write('\n')
        for key in TintDic.keys():
            file.write(key)
            file.write('#')
            file.write(TintDic[key][0])
            file.write('#')
            file.write(TintDic[key][1])
            file.write('\n')

        file.write('#####')
        file.close()

    def openReturnWidget(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_RETURN_NEW, True)

    def onCloseReturn(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RETURN_NEW)

    def onContinueReturn(self, *arg):
        gameglobal.rds.ui.characterDetailAdjust.onClickReturnSelect()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RETURN_NEW)

    def onContinueReturnSave(self, *arg):
        self.onSaveNpcConfig()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RETURN_NEW)
        BigWorld.callback(1.0, self.onClickReturnSelect)

    def openResetWidget(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_RESET, True)

    def onCloseReset(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RESET)

    def onResetAvatar(self, *arg):
        p = gameglobal.rds.loginScene.player
        p.avatarConfig = ''
        self.onClickCharacter(self.characterId)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RESET)

    def onResetSaveAvatar(self, *arg):
        self.onSaveNpcConfig()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_RESET)
        self.onClickCharacter(self.characterId)

    def onResetAvatarConfig(self, *arg):
        self.resetAvatarConfig()

    def resetAvatarConfig(self):
        self.openResetWidget()

    def onClickRandom(self, *arg):
        self.clickRandom()

    def clickRandom(self):
        self.operationLog.record()
        gamelog.debug('onClickRandom')
        if self.detailAdjustMed:
            array = self.detailAdjustMed.Invoke('getAllItemInSubUI')
            keys = array.GetElement(0)
            types = array.GetElement(1)
            l = keys.GetArraySize()
            p = gameglobal.rds.loginScene.player
            for i in xrange(0, l):
                key = keys.GetElement(i).GetString()
                type = int(types.GetElement(i).GetNumber())
                if type == AMU.BONE_VERTEX_SLIDER:
                    self._onHandleSliderChange(key, AMU.genRandSliderValue(), True)
                else:
                    isMale = p.physique.isMale()
                    params = AMU.getDyeMorpherParamByUI(key, 0, isMale)
                    if not params and key not in ('mobanItem', 'faxing_style'):
                        continue
                    elif type == AMU.ZHUANGBAN_BTN:
                        if key == 'mobanItem':
                            self._onClickCharacter(-1)
                        elif key == 'faxing_style':
                            value = self.avatarMorpher.getRandomHair()
                            self.avatarMorpher.setHairStyle(value)
                            self.saveMorpher(p)
                            p.physique.hair = self.avatarMorpher.hair
                            p.set_physique(None)
                        else:
                            value = self.avatarMorpher.getDyeMorpherRandomValue(params[0], params[1])
                            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)
                    elif type == AMU.ZHUANGBAN_SLIDER:
                        value = self.avatarMorpher.getDyeMorpherRandomValue(params[0], params[1])
                        self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)

            modelId = charRes.transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
            self.refreshUI = True
            self._refreshFaceAndBody(modelId)

    def onClickRecover(self, *arg):
        self.clickRecover()

    def clickRecover(self):
        gamelog.debug('onClickRecover')
        self.operationLog.recover()

    def onUpdateDyeInfo(self, *arg):
        if self.itemData:
            itemData = self.itemData
            transModelId = itemData.get('transModelId', 1)
            dyesDict = itemData.get('dyesDict', {})
            p = gameglobal.rds.loginScene.player
            if not transModelId:
                p.aspect.set(gametypes.EQU_PART_HEAD, p.aspect.head, dyesDict.get('head', []))
                p.aspect.set(gametypes.EQU_PART_BODY, p.aspect.body, dyesDict.get('body', []))
                p.aspect.set(gametypes.EQU_PART_HAND, p.aspect.hand, dyesDict.get('hand', []))
                p.aspect.set(gametypes.EQU_PART_LEG, p.aspect.leg, dyesDict.get('leg', []))
                p.aspect.set(gametypes.EQU_PART_SHOE, p.aspect.shoe, dyesDict.get('shoe', []))
                mpr = charRes.convertToMultiPartRes(itemData)
                m = AM.SimpleModelMorpher(p.model, p.realPhysique.sex, p.realPhysique.school, p.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, dyesDict)
                m.readConfig(p.realAvatarConfig)
                m.applyDyeMorph(True)

    def isValidGsNumber(self, number):
        data = number.split('-')
        if len(data) != 4:
            return False
        for item in data:
            if len(item) != 4:
                return False

        return True

    def onGetLookAtChoice(self, *arg):
        return GfxValue(self.getLookAtChoice())

    def getLookAtChoice(self):
        return self.enableLookAt

    def onSetLookAtChoice(self, *arg):
        value = arg[3][0].GetBool()
        self.setLookAtChoice(value)

    def setLookAtChoice(self, value):
        self.enableLookAt = value
        self._setLookAtChoice(value)

    def onClickPlayMovie(self, *arg):
        self.playMovie()

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
         'callback': Functor(self.setPlayBtnVisible, True)}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/CharacterActSoundNewWidget' + self.uiAdapter.getUIExt(), 'unitDesc', 270, 150)
        self.cgPlayer.playMovie(self.videoName, config)
        Sound.enableMusic(False)

    def onSetMovieType(self, *args):
        self.endMovie()
        movieType = int(list(args[3][0].GetString())[-1])
        self.videoName = SCD.data.get('loginSceneVideos', {})[movieType].get('video', 'xizao')
        self.videoWeb = SCD.data.get('loginSceneVideos', {})[movieType].get('web', 'http://tianyu.163.com')

    def setPlayBtnVisible(self, vis):
        if self.actSoundMed:
            self.actSoundMed.Invoke('setPlayBtnVisible', GfxValue(vis))

    def equipWing(self, wingId):
        player = gameglobal.rds.loginScene.player
        player.modelServer.wingFlyModel.detach()
        player.model.action('21101').stop()
        maxStage = ED.data.get(wingId, {}).get('maxStage', 0)
        player.modelServer.wingFlyModel.equipItem(wingId, maxStage)
        player.modelServer.wingFlyModel.attach(player.model)
        player.model.action('21101')()
        gameglobal.rds.loginScene.zoomTo(3)

    def downWing(self):
        player = gameglobal.rds.loginScene.player
        player.model.action('21101').stop()
        if player.modelServer.wingFlyModel.isAttached():
            player.modelServer.wingFlyModel.detach()
            gameglobal.rds.loginScene.zoomTo(0)

    def onShowWing(self, *args):
        wingId = int(args[3][0].GetNumber())
        if wingId == 0:
            self.downWing()
        else:
            self.equipWing(wingId)

    def onClickWeather(self, *args):
        try:
            index = int(args[3][0].GetNumber())
        except:
            index = 0

        param = gameglobal.AVATAR_WEATHER_PARAM[index]
        player = gameglobal.rds.loginScene.player
        if player and player.model:
            if param:
                TA.ta_add([player.model], 'avatarSkinWeather', param)
            else:
                TA.ta_del([player.model], 'avatarSkinWeather')
        for key, value in gameglobal.AVATAR_ZONE_PARAM.iteritems():
            if key != index:
                BigWorld.setZonePriority(value, -gameglobal.LOGINZONE_PRIO)
            else:
                BigWorld.setZonePriority(value, gameglobal.LOGINZONE_PRIO)

    def onEnableWeather(self, *args):
        ret = gameglobal.rds.configData.get('enableLoginWeather', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)
        return GfxValue(ret)

    def onShowMovieDetail(self, *args):
        BigWorld.openUrl(self.videoWeb)

    def endMovie(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.setPlayBtnVisible(True)
            self.cgPlayer = None
        Sound.enableMusic(True)

    def onGetWingIDs(self, *args):
        res = []
        player = gameglobal.rds.loginScene.player
        wingIDs = CSD.data.get(player.school, [{}])[0].get('wingList', [])
        for itemId in wingIDs:
            iconPath = uiUtils.getItemIconFile64(itemId)
            icon = {'iconPath': iconPath,
             'itemId': itemId,
             'count': 1}
            res.append(icon)

        return uiUtils.array2GfxAarry(res, True)

    def _setLookAtChoice(self, value):
        player = gameglobal.rds.loginScene.player
        if player:
            player.modelServer.poseManager.lookAtModeEnable = value
            player.modelServer.poseManager.setPoseModel()
            if value:
                player.modelServer.poseManager.startLookAtPose()
                player.modelServer.poseManager.startGaze()
            else:
                player.modelServer.poseManager.stopPoseModel()
                player.modelServer.poseManager.stopGaze()

    def onGetAvatarVideoAndWingCfg(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableAvatarVideoAndWing', False))

    def resetFaceEmotionBtn(self):
        if self.actSoundMed:
            self.actSoundMed.Invoke('setFaceEmotionSelect', GfxValue(0))

    def showShare(self, nuid):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_SHARE)
        self.allUploadKeys = []
        self.nuid = nuid

    def onUseOldAvatarConfig(self, *args):
        p = gameglobal.rds.loginScene.player
        chooseAvatarData = gameglobal.rds.ui.characterCreate.getChooseAvatar()
        avatarConfig = chooseAvatarData['avatarConfig']
        hair = chooseAvatarData['physique'].hair
        p.physique.hair = hair
        p.set_physique(None)
        if p.avatarConfig != avatarConfig:
            p.avatarConfig = avatarConfig
            self.refreshUI = True
            p.useAvatarConfig(None)

    def onEnableUseOldAvatarConfig(self, *args):
        if gameglobal.rds.loginScene.inSchoolAvatarConfigStage():
            chooseAvatarData = gameglobal.rds.ui.characterCreate.getChooseAvatar()
            physique = chooseAvatarData['physique']
            gender = gameglobal.rds.loginScene.selectGender
            bodyType = gameglobal.rds.loginScene.selectBodyType
            if physique.sex == gender and physique.bodyType == bodyType:
                return GfxValue(True)
        return GfxValue(False)

    def onGetCreateBtnName(self, *args):
        return GfxValue(self.getCreateBtnName())

    def getCreateBtnName(self):
        if gameglobal.rds.loginScene.inSchoolAvatarConfigStage():
            return gbk2unicode(gameStrings.CHARACTER_DETAIL_ADJUST_NEW_CREATEBTN_NAME)
        return ''

    def onRandomRoleName(self, *arg):
        p = gameglobal.rds.loginScene.player
        account = BigWorld.player()
        if gameglobal.rds.configData.get('enableRandomName', False):
            if hasattr(account.base, 'requestRandomName'):
                account.base.requestRandomName(p.physique.sex == const.SEX_MALE)

    def setInputName(self, roleName):
        if self.characterNameMed:
            self.characterNameMed.Invoke('setInputName', GfxValue(gbk2unicode(roleName)))


class OperationLog(object):

    def __init__(self):
        self.detailAdjust = None
        self.stack = []

    def set(self, detailAdjust):
        self.detailAdjust = detailAdjust

    def record(self):
        p = gameglobal.rds.loginScene.player
        if p and p.inWorld:
            self.stack.append((self.detailAdjust.characterId, p.physique.hair, self.detailAdjust.avatarMorpher.export(p.avatarConfig)))

    def recover(self):
        if self.stack:
            characterId, hair, avatarConfig = self.stack.pop(-1)
            self.detailAdjust.characterId = characterId
            self.detailAdjust.refreshUI = True
            p = gameglobal.rds.loginScene.player
            p.physique.hair = hair
            p.set_physique(None)
            if p.avatarConfig != avatarConfig:
                p.avatarConfig = avatarConfig
                p.useAvatarConfig(None)
        else:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1729)

    def release(self):
        self.stack = []
        self.detailAdjust = None
