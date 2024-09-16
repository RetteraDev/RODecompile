#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterCreateProxy.o
from gamestrings import gameStrings
import time
import BigWorld
import C_ui
import Sound
from Scaleform import GfxValue
import gameglobal
import gametypes
import game
import const
import keys
import gamelog
import clientcom
import ui
import Account
import formula
import events
import utils
from gamestrings import gameStrings
from guis import uiConst
from guis import messageBoxProxy
from appSetting import Obj as AppSettings
from callbackHelper import Functor
from ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiUtils
from asObject import ASObject
from helpers import loadingProgress
from helpers import black
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from sfx import keyboardEffect
CHECK_FLAG = 1 << gametypes.RESET_PROPERTY_NAME | 1 << gametypes.RESET_PROPERTY_BODYTYPE | 1 << gametypes.RESET_PROPERTY_AVATARCONFIG

class CharacterCreateProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(CharacterCreateProxy, self).__init__(uiAdapter)
        self.bindType = 'characterCreate'
        self.modelMap = {'clickReturnLogin': self.onClickReturnLogin,
         'clickSelectCharacter': self.onClickSelectCharacter,
         'clickEnterGame': self.onClickEnterGame,
         'clickDelete': self.onClickDelete,
         'doubleClickEnterGame': self.onDoubleClickEnterGame,
         'clickChooseServer': self.onClickChooseServer,
         'clickReset': self.onClickReset,
         'clickCreateTip': self.onClickCreateTip,
         'getDeleteTimeInfo': self.onGetDeleteTimeInfo,
         'clickCancelDelete': self.onClickCancelDelete,
         'getAuthVal': self.onGetAuthVal,
         'getCharacterInfo': self.onGetCharacterInfo,
         'getResetInfo': self.onGetResetInfo,
         'clickRename': self.onClickRename,
         'clickCancelSex': self.onClickCancelSex,
         'getDescTip': self.onGetDescTip,
         'clickNewServer': self.onClickNewServer,
         'clickPrePay': self.onClickPrePay,
         'getPreBtnState': self.onGetPreBtnState,
         'getHolidayTips': self.onGetHolidayTips,
         'showBoughtCharacter': self.onShowBoughtCharacter,
         'boughtCharacterListItemRender': self.onBoughtCharacterListItemRender,
         'handleTakebackFromSelling': self.onHandleTakebackFromSelling}
        self.mediator = None
        self.enterMediator = None
        self.oldIndex = 0
        self.newIndex = 0
        self.loginName = ''
        self.reset()

    def reset(self):
        self.deleteBoxId = None
        self.isReturn = False
        self.cancelDelBoxId = None
        self.cancelSexBoxId = None
        self.selectBoughtCharacterItem = None

    def getValue(self, key):
        characterList = gameglobal.rds.loginManager.characterList
        if key == 'characterCreate.Characterlist':
            ar = self.movie.CreateArray()
            for i, item in enumerate(characterList.characterDetail):
                data = characterList.getCharacterInfo(i)
                data = uiUtils.dict2GfxDict(data, True)
                ar.SetElement(i, data)

            return ar
        if key == 'characterCreate.setFocusCharacter':
            if characterList.count > 0:
                if self.isReturn:
                    return GfxValue(characterList.count - 1)
                else:
                    return GfxValue(self.newIndex)
            else:
                return GfxValue(-1)
        elif key == 'characterCreate.getServerName':
            isNovice = False
            hostName = gameStrings.TEXT_CHARACTERCREATEPROXY_102
            try:
                if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
                    isNovice = True
                hostName = gameglobal.rds.loginManager.titleName()
            except:
                hostName = gameStrings.TEXT_CHARACTERCREATEPROXY_102

            return (GfxValue(gbk2unicode(hostName)), GfxValue(isNovice))

    def _registerMediator(self, widgetId, mediator):
        gamelog.debug('@hjx media#CharacterCreateProxy:', widgetId)
        if widgetId == uiConst.WIDGET_CHARACTER_CREATE_LIST:
            self.mediator = mediator
            self.onShowBoughtCharacter()
        elif widgetId == uiConst.WIDGET_CHARACTER_ENTER_GAME:
            self.enterMediator = mediator

    def setFocusCharacter(self, index):
        self.newIndex = index
        self.oldIndex = index
        if self.mediator is not None:
            self.mediator.Invoke('setFocusCharacter', GfxValue(index))
        self.setEnterGameBtn()

    def setEnterGameBtn(self):
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[self.newIndex]:
            keyboardEffect.removeSelectCharKBE()
        else:
            characterDetail = characterList.characterDetail[self.newIndex]
            if characterDetail['auth'] in (const.AUTH_VALID_COOL, const.AUTH_VALID_DELETE):
                gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_ENTER_GAME)
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_ENTER_GAME)
            school = characterDetail.get('school')
            keyboardEffect.addSelectCharKBE(school)
        self.updatePreBtnState()

    def setRoleCharacter(self, index, info):
        gamelog.debug('setRoleCharacter', self.mediator, index, info)
        info = uiUtils.dict2GfxDict(info, True)
        if self.mediator is not None:
            self.mediator.Invoke('setRoleCharacter', (GfxValue(index), info))

    def test(self):
        ret = {}
        ret['auth'] = 0
        ret['name'] = 'name'
        ret['school'] = 3
        ret['lv'] = 50
        ret['where'] = 'teset'
        ret['resetInfo'] = {}
        ret['extra'] = {}
        self.setRoleCharacter(0, ret)

    def updateCharacterName(self, index, info):
        info = uiUtils.dict2GfxDict(info, True)
        if self.mediator is not None:
            self.mediator.Invoke('updateCharacterName', (GfxValue(index), info))

    def setDeleteCharacter(self, index):
        if self.mediator:
            self.mediator.Invoke('setDeleteCharacter', (GfxValue(index),))

    def setCoolCharacter(self, index):
        if self.mediator:
            self.mediator.Invoke('setCoolCharacter', (GfxValue(index),))

    def setCancelDeleteCharacter(self, index):
        if self.mediator:
            self.mediator.Invoke('setCancelDeleteCharacter', (GfxValue(index),))

    def setSellingCharacter(self, index):
        if self.mediator:
            self.mediator.Invoke('setSellingCharacter', (GfxValue(index),))
        else:
            gamelog.debug('ypc@ setSellingCharacter mediator is null!')

    def setBoughtCharacter(self, index):
        if self.mediator:
            self.mediator.Invoke('setBoughtCharacter', (GfxValue(index),))

    def clearAllCCWidgets(self):
        self.hide()

    def loadAllCCWidgets(self):
        loadWidgetsList = [uiConst.WIDGET_CHARACTER_CREATE_LIST, uiConst.WIDGET_CHARACTER_CREATE_RETURN_LOGIN, uiConst.WIDGET_CHARACTER_ENTER_GAME]
        characterList = gameglobal.rds.loginManager.characterList
        if len(characterList.characterDetail) == 0:
            loadWidgetsList.append(uiConst.WIDGET_CHARACTER_CREATE_TIP)
        loadWidgetsList.append(uiConst.WIDGET_SYSTEMTIPS)
        gameglobal.rds.loginScene.loadWidgets(loadWidgetsList)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.enterMediator = None
        unloadWidgetsList = [uiConst.WIDGET_CHARACTER_CREATE_LIST,
         uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW,
         uiConst.WIDGET_CHARACTER_CREATE_RETURN_LOGIN,
         uiConst.WIDGET_CHARACTER_ENTER_GAME,
         uiConst.WIDGET_CHARACTER_CREATE_TIP]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        gameglobal.rds.ui.characterDetailAdjust.closeTips()
        if self.deleteBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.deleteBoxId)
            self.deleteBoxId = None
        if self.cancelDelBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.cancelDelBoxId)
            self.cancelDelBoxId = None
        if self.cancelSexBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.cancelSexBoxId)
            self.cancelSexBoxId = None

    def onClickDelete(self, *args):
        if gameglobal.PIN_JIAN_TEST:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_CHARACTERCREATEPROXY_220)
            return
        characterList = gameglobal.rds.loginManager.characterList
        if gameglobal.rds.configData.get('isReservationOnlyServer', False) and gameglobal.rds.configData.get('enablePrePayCoin', False):
            if len(characterList.characterDetail) > 0 and getattr(BigWorld.player(), 'prePayGbId', 0) > 0:
                msg = uiUtils.getTextFromGMD(GMDD.data.CHARACTER_PREPAY_DELETE_CHARACTER_HINT, gameStrings.TEXT_CHARACTERCREATEPROXY_228)
                gameglobal.rds.ui.messageBox.showMsgBox(msg)
                return
        try:
            characterName = characterList.characterDetail[self.newIndex]['name']
            auth = characterList.characterDetail[self.newIndex]['auth']
            lv = characterList.characterDetail[self.newIndex]['lv']
        except:
            gamelog.error(gameStrings.TEXT_CHARACTERCREATEPROXY_237)
            return

        MBButton = messageBoxProxy.MBButton
        msg = ''
        if auth == const.AUTH_VALID_RENAME:
            self.deleteBoxId = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_CHARACTERCREATEPROXY_244)
            return
        if auth == const.AUTH_VALID_DELETE or auth == const.AUTH_VALID_COOL and characterList.isDeleteTimeOut(self.newIndex):
            msg += gameStrings.TEXT_CHARACTERCREATEPROXY_248
        elif auth == const.AUTH_VALID_PERMIT:
            if lv < const.ACCOUNT_DELETE_LEVEL:
                msg += gameStrings.TEXT_CHARACTERCREATEPROXY_251 % const.ACCOUNT_DELETE_LEVEL
                msg += gameStrings.TEXT_CHARACTERCREATEPROXY_252
            else:
                msg += gameStrings.TEXT_CHARACTERCREATEPROXY_252
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.onConfirmDelete, characterName, auth)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        self.deleteBoxId = gameglobal.rds.ui.messageBox.show(True, '', msg % characterName, buttons)

    def confirmDeleteWithCoin(self, characterName, coin, mallCash):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.onConfirmDeleteWithCoin, characterName)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        msg = gameStrings.TEXT_CHARACTERCREATEPROXY_262
        self.deleteBoxId = gameglobal.rds.ui.messageBox.show(True, '', msg % (characterName, coin, mallCash), buttons)

    def onConfirmDeleteWithCoin(self, characterName):
        if characterName:
            p = BigWorld.player()
            p.base.deleteCharacter(characterName, True)

    def onConfirmDelete(self, characterName, auth):
        if characterName:
            characterList = gameglobal.rds.loginManager.characterList
            p = BigWorld.player()
            if auth == const.AUTH_VALID_DELETE:
                p.base.dropCharacter(characterName)
            elif auth == const.AUTH_VALID_COOL and characterList.isDeleteTimeOut(self.newIndex):
                p.base.dropCharacter(characterName)
            elif auth == const.AUTH_VALID_PERMIT:
                p.base.deleteCharacter(characterName, False)
            else:
                print '@hjx error:onConfirmDelete:', auth

    def onClickCancelDelete(self, *arg):
        characterList = gameglobal.rds.loginManager.characterList
        try:
            characterName = characterList.characterDetail[self.newIndex]['name']
        except:
            gamelog.error(gameStrings.TEXT_CHARACTERCREATEPROXY_237)
            return

        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.onConfirmCancelDelete, characterName)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        self.cancelDelBoxId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_CHARACTERCREATEPROXY_294 % characterName, buttons)

    def onConfirmCancelDelete(self, characterName):
        if characterName:
            p = BigWorld.player()
            p.base.freeCharacter(characterName)

    def onClickReturnLogin(self, *arg):
        self.doReturnLogin()

    def doReturnLogin(self, bRefreshServerList = True):
        self.clearAllCCWidgets()
        gameglobal.rds.loginScene.clearPlayer()
        gameglobal.rds.loginManager.disconnectFromGame()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        if not gameglobal.rds.enableBinkLogoCG:
            Sound.changeZone(gameglobal.NEW_LOGIN_MUSIC, '')
        if bRefreshServerList:
            gameglobal.rds.ui.loginSelectServer.onRefreshServerList()

    @ui.callFilter(1, False)
    def onDoubleClickEnterGame(self, *arg):
        characterList = gameglobal.rds.loginManager.characterList
        if gameglobal.rds.ui.messageBox.isShow(self.deleteBoxId):
            return
        if gameglobal.rds.ui.messageBox.isShow(self.cancelSexBoxId):
            return
        if not characterList.isEmpty[self.newIndex]:
            if self.checkEnterGame(0):
                name = characterList.characterDetail[self.newIndex]['name']
                isHoliday = characterList.characterDetail[self.newIndex]['isHoliday']
                if isHoliday:
                    gameglobal.rds.ui.holidayMessageBox.show()
                    return
                self.enterGame(name)

    def onClickSelectCharacter(self, *arg):
        characterList = gameglobal.rds.loginManager.characterList
        self.newIndex = int(arg[3][0].GetString())
        gamelog.debug('@hjx delete#onClickSelectCharacter', characterList.count)
        if self.newIndex == self.oldIndex and characterList.count != 0:
            return
        self.setEnterGameBtn()
        characterDetail = characterList.getCharacterOriginalInfo(self.newIndex)
        gameglobal.rds.loginManager.zhiShengGbId = 0
        if characterList.isEmpty[self.newIndex]:
            self.newIndex = self.oldIndex
            self.gotoCharacterSelectZero()
        elif characterDetail and characterDetail['auth'] == const.AUTH_VALID_LVUP:
            gameglobal.rds.loginManager.zhiShengGbId = characterDetail.get('sourceGbId', 0)
            self.newIndex = len(characterList.characterDetail) - 1
            self.enterZhiSheng()
        else:
            gameglobal.rds.loginScene.placePlayer(characterDetail)
        self.oldIndex = self.newIndex

    def enterSchoolChange(self, changedSchool = 0):
        bodyData = gameglobal.rds.loginScene.getAllCharShowData().get(changedSchool, [])
        if not bodyData:
            return
        self.hide()
        gender = bodyType = bdIdx = -1
        for bodyIdx, data in enumerate(bodyData):
            if data.get('showModel', 0):
                gender = data.get('sex', const.SEX_MALE)
                bodyType = data.get('bodyType', const.BODY_TYPE_5)
                bdIdx = bodyIdx
                break

        gameglobal.rds.loginScene.enterCharDetailAdjustSchoolAvatarConfig(changedSchool, gender, bodyType)
        if gameglobal.rds.loginScene.player:
            gameglobal.rds.loginScene.player.hide(True)
            gameglobal.rds.loginScene.player.targetCaps = []

    @ui.callFilter(1, False)
    def onClickEnterGame(self, *arg):
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[0]:
            return
        if self.checkEnterGame(0):
            name = characterList.characterDetail[self.newIndex]['name']
            isHoliday = characterList.characterDetail[self.newIndex]['isHoliday']
            if isHoliday:
                gameglobal.rds.ui.holidayMessageBox.show()
                return
            self.enterGame(name)
        gameglobal.rds.sound.playSound(gameglobal.SD_38)

    def enterGame(self, name = '', isHoliday = False):
        characterList = gameglobal.rds.loginManager.characterList
        gameglobal.loadingSpaceNo = characterList.characterDetail[self.newIndex]['spaceNo']
        gameglobal.loadingChunk = characterList.characterDetail[self.newIndex]['chunk']
        self.loginName = characterList.characterDetail[self.newIndex]['name']
        loadingProgress.instance().preLoad()
        if game.cgMovie and game.cgMovie.cgName:
            return
        if not AppSettings.get(keys.SET_TITLE_CG3, 0):
            cgName = 'bw'
            game.playTitleCg(keys.SET_TITLE_CG3, cgName, self.endTitleCg)
        elif isHoliday:
            self.__realEnterGame(True)
        else:
            self.__realEnterGame()

    def endTitleCg(self, enableMusic = True):
        C_ui.enableUI(True)
        if enableMusic:
            Sound.enableMusic(True)
        if game.cgMovie:
            game.cgMovie.endMovie()
        self.__realEnterGame()

    def __realEnterGame(self, forceEnter = False):
        p = gameglobal.rds.loginScene.player
        gameglobal.rds.ui.holidayMessageBox.hide()
        if hasattr(p, 'school') and self.loginName:
            BigWorld.player().base.selectCharacter(self.loginName, p.school, clientcom.CLIENT_REVISION, forceEnter)

    def clear(self):
        self.clearAllCCWidgets()
        gameglobal.rds.loginManager.characterList.clearAll()
        gameglobal.rds.loginScene.clearScene()

    def returnToCreate(self, isCreateNew = False):
        self.loadAllCCWidgets()
        BigWorld.setBlackTime(0, 0, 0, 0.99, 0.99, 0.7)
        BigWorld.setZonePriority('hand', gameglobal.LOGINZONE_PRIO)
        gameglobal.rds.loginScene.clearLoginModel()
        gameglobal.rds.loginScene.gotoCreateStage()
        self.isReturn = isCreateNew
        characterList = gameglobal.rds.loginManager.characterList
        index = self.newIndex
        if isCreateNew:
            index = len(characterList.characterDetail) - 1
        if not characterList.isEmpty[index]:
            gameglobal.rds.loginScene.placePlayer(characterList.characterDetail[index])
        self.setFocusCharacter(index)
        gameglobal.rds.loginScene.trackNo = 0
        if gameglobal.rds.configData.get('forbidEnterWorld', False):
            return
        else:
            if isCreateNew:
                self.onClickEnterGame(None)
            return

    def onClickChooseServer(self, *arg):
        gamelog.debug('onClickChooseServer')

    def onClickCreateTip(self, *arg):
        gameglobal.rds.ui.loginWin.enterNewXrjm()

    def onGetDeleteTimeInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        deleteInfo = {}
        deleteInfo['tDeleteInterval'] = 0
        deleteInfo['name'] = ''
        if index >= len(gameglobal.rds.loginManager.characterList.characterDetail):
            return uiUtils.dict2GfxDict(deleteInfo)
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.characterDetail[index]['auth'] != const.AUTH_VALID_COOL:
            return uiUtils.dict2GfxDict(deleteInfo)
        tDeleteInterval = characterList.characterDetail[index]['extra']['tDeleteInterval']
        tNotify = characterList.characterDetail[index]['extra']['tNotify']
        deleteInfo['tDeleteInterval'] = tDeleteInterval - (time.time() - tNotify)
        deleteInfo['name'] = characterList.characterDetail[index]['name']
        return uiUtils.dict2GfxDict(deleteInfo, True)

    def onGetAuthVal(self, *arg):
        index = int(arg[3][0].GetNumber())
        characterList = gameglobal.rds.loginManager.characterList
        return GfxValue(characterList.characterDetail[index]['auth'])

    def onGetCharacterInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        characterDetail = gameglobal.rds.loginManager.characterList.getCharacterInfo(index)
        return uiUtils.dict2GfxDict(characterDetail, True)

    def gotoCharacterSelectZero(self):
        if not gameglobal.rds.configData.get('enableCreateRole', True):
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_CHARACTERCREATEPROXY_485)
            return
        if gameglobal.rds.configData.get('oneCharacterLimit', False) and len(gameglobal.rds.loginManager.characterList.characterDetail) >= 1:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_CHARACTERCREATEPROXY_489)
            return
        self.clearAllCCWidgets()
        gameglobal.rds.loginScene.gotoCharCreateNewStage()
        gameglobal.rds.loginScene.setTaTint(False)
        BigWorld.setZonePriority('hand', -gameglobal.LOGINZONE_PRIO)
        characterList = gameglobal.rds.loginManager.characterList
        self.newIndex = len(characterList.characterDetail) - 1
        if gameglobal.rds.loginScene.player:
            gameglobal.rds.loginScene.player.hide(True)
            gameglobal.rds.loginScene.player.setTargetCapsUse(False)

    def checkEnterGame(self, checkFlag = CHECK_FLAG):
        if gameglobal.rds.loginManager.waitingForEnterGame:
            return
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[0]:
            return False
        if self.newIndex >= len(characterList.characterDetail):
            return False
        name = characterList.characterDetail[self.newIndex]['name']
        rename = characterList.characterDetail[self.newIndex].get('rename', '')
        gbID = characterList.characterDetail[self.newIndex].get('gbID', 0)
        auth = characterList.characterDetail[self.newIndex]['auth']
        if rename:
            gameglobal.loadingSpaceNo = characterList.characterDetail[self.newIndex]['spaceNo']
            gameglobal.loadingChunk = characterList.characterDetail[self.newIndex]['chunk']
            gameglobal.rds.ui.loginSelectServer.showForceChangeNameWidget(rename, gameglobal.rds.loginScene.player.school, clientcom.CLIENT_REVISION, gbID)
            return False
        if gameglobal.rds.configData.get('enableEnvSDK', False) and gameglobal.rds.configData.get('enableForceRoleRename', False):
            if not gameglobal.rds.ui.characterDetailAdjust.checkForceChangeName(uiUtils.gbk2unicode(name)):
                gameglobal.loadingSpaceNo = characterList.characterDetail[self.newIndex]['spaceNo']
                gameglobal.loadingChunk = characterList.characterDetail[self.newIndex]['chunk']
                gameglobal.rds.ui.loginSelectServer.envSDKForceChangeName(name, gameglobal.rds.loginScene.player.school, clientcom.CLIENT_REVISION)
                return False
        if auth == const.AUTH_VALID_COOL:
            return False
        account = BigWorld.player()
        if not hasattr(account, 'resetPropFlags'):
            return False
        if account.resetPropFlags.has_key(gbID) and account.resetPropFlags[gbID]:
            flags = account.resetPropFlags[gbID]
            changedSchool = flags.get(gametypes.RESET_PROPERTY_SCHOOL, 0)
            if changedSchool:
                self.enterSchoolChange(changedSchool)
                return False
            if flags.get(gametypes.RESET_PROPERTY_SEX, 0):
                self.enterBodyType(resetSex=True)
                return False
            if flags.get(gametypes.RESET_PROPERTY_NAME, 0) and checkFlag & 1 << gametypes.RESET_PROPERTY_NAME:
                p = gameglobal.rds.loginScene.player
                gameglobal.rds.ui.loginSelectServer.showForceChangeNameWidget(name, p.school, clientcom.CLIENT_REVISION, gbID)
                return False
            if flags.get(gametypes.RESET_PROPERTY_BODYTYPE, 0) and checkFlag & 1 << gametypes.RESET_PROPERTY_BODYTYPE:
                self.enterBodyType()
                return False
            if flags.get(gametypes.RESET_PROPERTY_AVATARCONFIG, 0) and checkFlag & 1 << gametypes.RESET_PROPERTY_AVATARCONFIG:
                self.enterAvatarConfig()
                return False
        return True

    def enterBodyType(self, resetSex = False):
        character = self.getChooseAvatar()
        aspect = character.get('appearance', None)
        if not resetSex and not utils.checkCanChangeBodyTypeByAppearance(aspect):
            msg = uiUtils.getTextFromGMD(GMDD.data.TAKE_OFF_EQUIP_BODYREQ)
            gameglobal.rds.ui.systemTips.show(msg, True)
            return
        elif resetSex and not utils.checkCanChangeSexByAppearance(aspect):
            msg = uiUtils.getTextFromGMD(GMDD.data.TAKE_OFF_EQUIP_BODYREQ)
            gameglobal.rds.ui.systemTips.show(msg, True)
            return
        else:
            self.hide()
            if not resetSex:
                school = character['school']
                gender = character['physique'].sex
                bodyType = character['physique'].bodyType
                bodyData = gameglobal.rds.loginScene.getAllCharShowData().get(school, [])
                bodyIdx = 0
                if bodyData:
                    for i, data in enumerate(bodyData):
                        if data['sex'] == gender and data['bodyType'] == bodyType:
                            bodyIdx = i
                            break

                gameglobal.rds.loginScene.setCharCreateSelectNewStage()
            else:
                school = character['school']
                gender = character['physique'].sex
                bodyType = character['physique'].bodyType
                bodyIdx = 0
                bodyData = gameglobal.rds.loginScene.getAllCharShowData().get(school, [])
                if bodyData:
                    for i, data in enumerate(bodyData):
                        if data['sex'] != gender:
                            bodyIdx = i
                            gender = data['sex']
                            bodyType = data['bodyType']
                            break

                if gender == character['physique'].sex:
                    return
                gameglobal.rds.loginScene.setCharCreateSelectNewStage()
            gameglobal.rds.loginScene.gotoCharCreateNewResetStage(school, gender, bodyType)
            if gameglobal.rds.loginScene.player:
                gameglobal.rds.loginScene.player.hide(True)
                gameglobal.rds.loginScene.player.targetCaps = []
            return

    def enterZhiSheng(self):
        self.hide()
        school = const.SCHOOL_YECHA
        gender = const.SEX_MALE
        bodyType = const.BODY_TYPE_3
        bodyIdx = 0
        bodyData = gameglobal.rds.loginScene.getAllCharShowData().get(school, [])
        for i, data in enumerate(bodyData):
            if data.get('showModel', 0):
                gender = data['sex']
                bodyType = data['bodyType']
                bodyIdx = i
                break

        gameglobal.rds.loginScene.gotoSelectTwoStage()
        gameglobal.rds.loginScene.gotoCharCreateNewStage()
        if gameglobal.rds.loginScene.player:
            gameglobal.rds.loginScene.player.hide(True)
            gameglobal.rds.loginScene.player.targetCaps = []

    def getChooseAvatar(self):
        characters = gameglobal.rds.loginManager.characterList.characterDetail
        if self.newIndex < len(characters) and self.newIndex >= 0:
            character = gameglobal.rds.loginManager.characterList.characterDetail[self.newIndex]
            return character
        else:
            return None

    def enterAvatarConfig(self):
        self.hide()
        player = gameglobal.rds.loginScene.player
        gameglobal.rds.loginScene.selectSchool = player.physique.school
        gameglobal.rds.loginScene.selectGender = player.physique.sex
        gameglobal.rds.loginScene.selectBodyType = player.physique.bodyType
        csd = gameglobal.rds.loginScene.getAllCharShowData().get(player.physique.school, [])
        for i, data in enumerate(csd):
            if data['bodyType'] == player.physique.bodyType and data['sex'] == player.physique.sex:
                gameglobal.rds.loginScene.bodyIdx = i
                break

        gameglobal.rds.loginScene.gotoAvatarconfigStage()
        gameglobal.rds.ui.characterDetailAdjust.loadCharacterDetail()
        gameglobal.rds.ui.characterDetailAdjust.loadAllCDWidgets()

    def onGetResetInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        characterList = gameglobal.rds.loginManager.characterList.characterDetail[index]
        return uiUtils.dict2GfxDict(characterList['resetInfo'])

    def onClickRename(self, *arg):
        self.checkEnterGame(1 << gametypes.RESET_PROPERTY_NAME)

    def onClickReset(self, *arg):
        self.checkEnterGame(1 << gametypes.RESET_PROPERTY_BODYTYPE | 1 << gametypes.RESET_PROPERTY_AVATARCONFIG | 1 << gametypes.RESET_PROPERTY_SEX)

    def onClickCancelSex(self, *arg):
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[0]:
            return
        if self.newIndex >= len(characterList.characterDetail):
            return
        gbID = characterList.characterDetail[self.newIndex].get('gbID', 0)
        auth = characterList.characterDetail[self.newIndex]['auth']
        if auth == const.AUTH_VALID_COOL:
            return
        account = BigWorld.player()
        if not hasattr(account, 'resetPropFlags'):
            return
        if account.resetPropFlags.has_key(gbID) and account.resetPropFlags[gbID]:
            flags = account.resetPropFlags[gbID]
            if flags.get(gametypes.RESET_PROPERTY_SEX, 0):
                msg = SCD.data.get('CancelChangeSexMsg', gameStrings.TEXT_CHARACTERCREATEPROXY_693)
                self.cancelSexBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmCancelSex)
                gameglobal.rds.loginManager.cache = {'gbID': gbID}

    def confirmCancelSex(self):
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[0]:
            return
        if self.newIndex >= len(characterList.characterDetail):
            return
        gbID = characterList.characterDetail[self.newIndex].get('gbID', 0)
        account = BigWorld.player()
        account.base.cancelPropFlag(gbID, gametypes.RESET_PROPERTY_SEX)

    def onGetDescTip(self, *arg):
        desc = SCD.data.get('NOVICE_LOGIN_DESC', gameStrings.TEXT_CHARACTERCREATEPROXY_711)
        return GfxValue(gbk2unicode(desc))

    def onClickNewServer(self, *arg):
        url = SCD.data.get('NOVICE_LOGIN_LINK', '')
        if url:
            clientcom.openFeedbackUrl(url)

    def onClickPrePay(self, *arg):
        if len(gameglobal.rds.loginManager.characterList.characterDetail) <= 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.CHARACTER_PREPAY_NO_CHARACTER_HINT, gameStrings.TEXT_CHARACTERCREATEPROXY_721)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
        else:
            gameglobal.rds.ui.characterPrePay.show()

    def onGetPreBtnState(self, *arg):
        self.updatePreBtnState()

    def onGetHolidayTips(self, *arg):
        holidayTips = uiUtils.getTextFromGMD(GMDD.data.LOGIN_HOLIDAY_TIPS, gameStrings.TEXT_CHARACTERCREATEPROXY_730)
        return GfxValue(gbk2unicode(holidayTips))

    def updatePreBtnState(self):
        if self.enterMediator:
            info = {}
            if gameglobal.rds.configData.get('isReservationOnlyServer', False) and gameglobal.rds.configData.get('enablePrePayCoin', False):
                info['showPrePayBtn'] = True
                prePayGbId = getattr(BigWorld.player(), 'prePayGbId', 0)
                if prePayGbId > 0:
                    info['prePayEnabled'] = False
                    info['prePayBtnLabel'] = gameStrings.TEXT_CHARACTERCREATEPROXY_742
                    info['prePayTips'] = gameStrings.TEXT_CHARACTERCREATEPROXY_743 % uiUtils.getTextFromGMD(GMDD.data.CHARACTER_PREPAY_HINT, '')
                else:
                    info['prePayBtnLabel'] = gameStrings.TEXT_CHARACTERCREATEPROXY_745
                    info['prePayEnabled'] = True
            else:
                info['showPrePayBtn'] = False
            chooseAvatar = self.getChooseAvatar()
            if chooseAvatar and chooseAvatar['resetInfo'].get(gametypes.RESET_PROPERTY_SCHOOL, None):
                info['changedSchool'] = True
                info['changedSchoolDesc'] = gameStrings.TEXT_CHARACTERCREATEPROXY_752
            else:
                info['changedSchoolDesc'] = gameStrings.TEXT_CHARACTERCREATEPROXY_754
            self.enterMediator.Invoke('updatePreBtnState', uiUtils.dict2GfxDict(info, True))

    def onShowBoughtCharacter(self, *args):
        gamelog.debug('ypc@ showBoughtCharacter!')
        if self.mediator:
            gamelog.debug('ypc@ showBoughtCharacter!')
            widget = ASObject(self.mediator.Invoke('getWidget'))
            self.selectBoughtCharacterItem = None
            boughtCharacterDatas = self._getAllBoughtCharacterData()
            if boughtCharacterDatas:
                widget.waitTakebackPanel.visible = True
                widget.waitTakebackPanel.list.dataArray = boughtCharacterDatas
            else:
                widget.waitTakebackPanel.visible = False
                widget.waitTakebackPanel.list.dataArray = []
        else:
            gamelog.debug('ypc@ showBoughtCharacter mediator error!')

    def onBoughtCharacterListItemRender(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.gotoAndStop('up')
        itemMc.characterName.text = itemData.name
        itemMc.roleicon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC_NO_ALL.get(itemData.school, 'shengtang'))
        itemMc.characterLv.text = 'Lv%d' % itemData.lv
        itemMc.characterWhere.text = formula.whatLocationName(itemData.spaceNo, itemData.chunk)
        itemMc.getBtn.addEventListener(events.BUTTON_CLICK, self.handleGetBoughtCharacter, False, 0, True)
        itemMc.getBtn.data = itemData.gbId
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleBoughtCharacterRollOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleBoughtCharacterRollOut, False, 0, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleBoughtCharacterClick, False, 0, True)

    def _getAllBoughtCharacterData(self):
        p = BigWorld.player()
        if not hasattr(p, 'boughtCharacterData') or not p.boughtCharacterData:
            gamelog.debug('ypc@ error has no boughtCharacterData!')
            return []
        return [ {'gbId': str(gbId),
         'name': bcd['name'],
         'school': bcd['physique'].school,
         'lv': bcd['lv'],
         'spaceNo': bcd['spaceNo'],
         'chunk': bcd['chunk']} for gbId, bcd in p.boughtCharacterData.iteritems() ]

    def _showFakeBoughtCharacter(self):
        if self.mediator:
            widget = ASObject(self.mediator.Invoke('getWidget'))
            self.selectBoughtCharacterItem = None
            widget.waitTakebackPanel.visible = True
            widget.waitTakebackPanel.list.dataArray = self._getFakeBoughtCharacterData()

    def _getFakeBoughtCharacterData(self):
        import random
        import string
        ret = []
        for i in range(10):
            name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            school = random.choice(uiConst.SCHOOL_FRAME_DESC_NO_ALL.keys())
            lv = random.randrange(0, 100)
            gbId = random.randrange(100000000000L, 999999999999L)
            ret.append({'gbId': gbId,
             'name': name,
             'school': school,
             'lv': lv,
             'spaceNo': 99,
             'chunk': 'jingjichang'})

        return ret

    def handleGetBoughtCharacter(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        gbId = long(itemMc.data)
        if not gbId:
            return
        p = BigWorld.player()
        if not p or not isinstance(p, Account.PlayerAccount):
            return
        gamelog.debug('ypc@ handleGetBoughtCharacter gbId is ', gbId)
        p.base.takeAwayCharacter(gbId)

    def onHandleTakebackFromSelling(self, *args):
        index = int(args[3][0].GetString())
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.CBG_ROLE_TAKEBACK_WARNING, yesCallback=lambda : self._realHandleTakebackFromSelling(index), yesBtnText=gameStrings.COMMON_BTN_YES, noBtnText=gameStrings.COMMON_BTN_NO)

    def _realHandleTakebackFromSelling(self, index):
        characterList = gameglobal.rds.loginManager.characterList
        if characterList.isEmpty[index]:
            return
        characterDetail = characterList.characterDetail[index]
        p = BigWorld.player()
        p.base.takeBackCharacter(characterDetail['gbID'])

    def handleBoughtCharacterRollOver(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget == self.selectBoughtCharacterItem:
            return
        e.currentTarget.gotoAndStop('over')

    def handleBoughtCharacterRollOut(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget == self.selectBoughtCharacterItem:
            return
        e.currentTarget.gotoAndStop('up')

    def handleBoughtCharacterClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget == self.selectBoughtCharacterItem:
            return
        if self.selectBoughtCharacterItem:
            self.selectBoughtCharacterItem.gotoAndStop('up')
        e.currentTarget.gotoAndStop('select')
        self.selectBoughtCharacterItem = e.currentTarget
