#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhanQiProxy.o
from gamestrings import gameStrings
import BigWorld
import os
import gamelog
import gametypes
import gameglobal
import utils
import C_ui
import const
import commGuild
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from guis import zhanQiMorpherFactory
from helpers import capturePhoto
from PIL import Image
from data import guild_config_data as GCD
from data import game_msg_data as GMD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
SLIDER_RANGE = [1, 5]

def calSliderValue(val):
    return sum(SLIDER_RANGE) - val


class ZhanQiProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ZhanQiProxy, self).__init__(uiAdapter)
        self.bindType = 'zhanQi'
        self.modelMap = {'getUploadCD': self.onGetUploadCD,
         'getDDS': self.onGetDDS,
         'ddsClick': self.onDDSClick,
         'colorClick': self.onColorClick,
         'getColorDesc': self.onGetColorDesc,
         'selectType': self.onSelectType,
         'selectSubType': self.onSelectSubType,
         'locationClick': self.onLocationClick,
         'handleSlider': self.onHandleSlider,
         'saveClick': self.onSaveClick,
         'cancelClick': self.onCancelClick,
         'randomClick': self.onRandomClick,
         'getSliderValue': self.onGetSliderValue,
         'userDefineDDSValid': self.onUserDefineDDSValid,
         'getUserDefineDDSSucc': self.onGetUserDefineDDSSucc,
         'getUserDefineDDSError': self.onGetUserDefineDDSError,
         'getSelectedInfo': self.onGetSelectedInfo,
         'selectFileClick': self.onSelectFileClick,
         'uploadClick': self.onUploadClick,
         'useClick': self.onUseClick,
         'showClick': self.onShowClick,
         'getUserDefFileInfo': self.onGetUserDefFileInfo,
         'userDefFileClick': self.onUserDefFileClick,
         'getFailedReason': self.onGetFailedReason,
         'clickRefresh': self.onClickRefresh,
         'getRefreshLimit': self.onGetRefreshLimit}
        self.mediator = None
        self.morpherFactory = zhanQiMorpherFactory.getInstance()
        self.previewCallback = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHAN_QI, self.hide)

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHAN_QI)
            self.morpherFactory.createMorpherIns()
            self.morpherFactory.readConfigFromPlayer()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHAN_QI)
        self.resetHeadGen()

    def onGetSliderValue(self, *arg):
        ret = list(SLIDER_RANGE)
        val = calSliderValue(self.morpherFactory.morpherIns[uiConst.ZHAN_QI_MORPHER_LOCATION].size)
        ret.append(val)
        return uiUtils.array2GfxAarry(ret)

    def onGetDDS(self, *arg):
        return self.curMorpher.getDDS()

    def onSelectType(self, *arg):
        parentType = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx zhanQi#onSelectType:', parentType)
        self.curMorpher = self.morpherFactory.morpherIns[parentType]
        gamelog.debug('@hjx zhanQi#curMorpher:', self.curMorpher)

    def onSelectSubType(self, *arg):
        parentType = int(arg[3][0].GetNumber())
        subType = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx zhanQi#onSelectSubType:', parentType, subType)
        self.curMorpher = self.morpherFactory.morpherIns[parentType]
        self.curMorpher.setCurSubMorpher(subType)
        self.curMorpher = self.curMorpher.getCurSubMorpher()
        gamelog.debug('@hjx zhanQi#curMorpher:', self.curMorpher)

    def onGetColorDesc(self, *arg):
        return self.curMorpher.getColorDesc()

    def onColorClick(self, *arg):
        colorStr = arg[3][0].GetString()
        gamelog.debug('@hjx zhanQi#colorStr:', colorStr)
        index = colorStr.rfind('_')
        btnName = colorStr[:index]
        val = colorStr[index + 1:]
        self.curMorpher.setIndex(btnName, int(val))
        self.applyTint(self.headGen)

    def onDDSClick(self, *arg):
        index = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx zhanQi#onDDSClick:', index)
        self.curMorpher.setIndex(index)
        self.applyTint(self.headGen)
        if self.curMorpher.tag == uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC:
            self.morpherFactory.morpherIns[uiConst.ZHAN_QI_MORPHER_HUIJI].subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE].isUsed = False

    def onLocationClick(self, *arg):
        directionStr = arg[3][0].GetString()
        gamelog.debug('@hjx zhanQi#onLocationClick:', directionStr)
        dir = {'upBtn': (0, 0.1),
         'downBtn': (0, -0.1),
         'leftBtn': (0.1, 0),
         'rightBtn': (-0.1, 0)}
        self.curMorpher.setLocation(dir[directionStr])
        self.applyTint(self.headGen)

    def onHandleSlider(self, *arg):
        val = arg[3][0].GetNumber()
        val = calSliderValue(val)
        gamelog.debug('@hjx zhanQi#onHandleSlider:', val)
        self.curMorpher.setIndex(val)
        self.applyTint(self.headGen)

    def onSaveClick(self, *arg):
        player = BigWorld.player()
        morpher = self.morpherFactory.export()
        curSubMorpher = self.morpherFactory.morpherIns[uiConst.ZHAN_QI_MORPHER_HUIJI].curSubMorpher
        if curSubMorpher.tag == uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE and curSubMorpher.isUsed:
            if player.guildIcon == '':
                player.showGameMsg(GMDD.data.ZHAN_QI_SAVE_FAILED_USER_DEF_OUT_OF_DATE, ())
                self.hide()
                return
        player.updateClanWarFlag(morpher)
        self.hide()
        if gameglobal.rds.ui.createGuild.headGen:
            self.applyTint(gameglobal.rds.ui.createGuild.headGen)

    def onCancelClick(self, *arg):
        self.hide()

    def onRandomClick(self, *arg):
        self.morpherFactory.applyRondomMorpher()
        self.applyTint(self.headGen)

    def reset(self):
        self.curMorpher = None
        self.headGen = None
        self.filePath = ''
        self.imagePath = ''
        self.imageHeight = 0
        self.imageWidth = 0

    def takePhoto3D(self, modelId = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL, tintMs = None, photoAction = None):
        if not self.headGen:
            self.headGen = capturePhoto.ZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.headGen.startCapture(modelId, tintMs, ('1101',))

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.ZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.headGen.initFlashMesh()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZHAN_QI:
            self.initHeadGen()
            self.takePhoto3D()
            self.mediator = mediator
            enableUserDefGuildCrest = gameglobal.rds.configData.get('enableUserDefGuildCrest', False)
            self.mediator.Invoke('setUserDefineBtn', GfxValue(enableUserDefGuildCrest and self.checkUserDefValid()))

    def applyTint(self, headGen):
        if headGen:
            model = headGen.adaptor.attachment
            config = self.morpherFactory.export()
            if model:
                dyeMorpher = zhanQiMorpherFactory.ZhanqiDyeMorpher(model, gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL)
                dyeMorpher.read(config)
                dyeMorpher.apply()

    def applyShowTint(self, headGen):
        if headGen:
            model = headGen.adaptor.attachment
            config = self.morpherFactory.exportShow()
            if model:
                dyeMorpher = zhanQiMorpherFactory.ZhanqiDyeMorpher(model, gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL)
                dyeMorpher.read(config)
                dyeMorpher.apply()

    def _checkUserDefineDDSValid(self, userDefineDDS):
        try:
            userDefineDDS = int(userDefineDDS)
            if userDefineDDS >= uiConst.ZHAN_QI_HUIJI_PIC_LIMIT:
                return True
            return False
        except:
            return False

    def onUserDefineDDSValid(self, *arg):
        if not self._checkUserDefineDDSValid(arg[3][0].GetString()):
            BigWorld.player().showGameMsg(GMDD.data.ZHAN_QI_USER_DEFINE_CODE_ILLEGAL, ())
            return GfxValue(False)
        else:
            return GfxValue(True)

    def onGetUserDefineDDSSucc(self, *arg):
        self.imageHeight = int(arg[3][0].GetNumber())
        self.imageWidth = int(arg[3][1].GetNumber())

    def onGetUserDefineDDSError(self, *arg):
        pass

    def onGetSelectedInfo(self, *arg):
        return self.morpherFactory.getSelectedInfo()

    def onSelectFileClick(self, *arg):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_ZHANQIPROXY_250, workPath, self.onSelectFile)

    def onSelectFile(self, path):
        if '.' in os.path.basename(os.path.splitext(path)[0]):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_NAME_ILLEGAL, {}).get('text', gameStrings.TEXT_FRIENDPROXY_1507))
            return
        if not path or not (path.endswith('.jpg') or path.endswith('.png')):
            return
        self.filePath = path
        i = path.rfind('\\')
        i = path.rfind('/') if i == -1 else i
        self.fileName = path if i == -1 else path[i + 1:]
        i = self.fileName.find('.')
        extension = self.fileName[i:]
        self.fileName = self.fileName if i == -1 else self.fileName[:i]
        self.srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + self.fileName + extension
        self.imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + self.fileName + '.dds'
        try:
            uiUtils.copyToImagePath(self.filePath)
            im = Image.open(self.srcResPath)
            im = im.resize((256, 256))
            im.save(self.srcResPath)
            BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
        except:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_FRIENDPROXY_1525)
            return

        if self.mediator:
            p = BigWorld.player()
            self.mediator.Invoke('setFilePath', (GfxValue(gbk2unicode(self.fileName) + extension), GfxValue('../' + self.imagePath), GfxValue(p.guildIconStatus == gametypes.NOS_FILE_STATUS_APPROVED)))

    def onGetUploadCD(self, *arg):
        p = BigWorld.player()
        guildIconUpLoadInterval = GCD.data.get('guildIconUpLoadInterval', 0)
        delta = guildIconUpLoadInterval - (utils.getNow() - p.updateGuildIconTime)
        return GfxValue(delta)

    def onUploadClick(self, *arg):
        p = BigWorld.player()
        if self.filePath == '':
            return
        gamelog.debug('@hjx guildIcon#onUploadClick:', self.imagePath, self.filePath)
        if self.imageHeight > const.IMAGES_HEIGHT or self.imageWidth > const.IMAGES_WIDTH:
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_NON_STANDARD, ())
            return
        guildIconUpLoadInterval = GCD.data.get('guildIconUpLoadInterval', 0)
        now = utils.getNow()
        if now - p.updateGuildIconTime < guildIconUpLoadInterval:
            delta = guildIconUpLoadInterval - (now - p.updateGuildIconTime)
            amount = GCD.data.get('cleanUploadCDItemAmount', 0)
            itemCnt = commGuild.getGuildFlagItemCnt(p, amount, guildIconUpLoadInterval)
            cleanUploadCDItemId = GCD.data.get('cleanUploadCDItemId')
            if cleanUploadCDItemId:
                msg = GMD.data.get(GMDD.data.GUILD_NOS_FILE_TIME_LIMIT_NOTIFY, {}).get('text', '%s %d %s')
                itemName = ID.data.get(cleanUploadCDItemId, {}).get('name', '')
                msg = msg % (utils.formatDuration(delta), itemCnt, itemName)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doUploadCheck, yesBtnText=gameStrings.TEXT_ZHANQIPROXY_314)
            else:
                p.showGameMsg(GMDD.data.USE_DEFINE_FILE_TIME_LIMIT, (utils.formatDuration(delta),))
        else:
            p.cell.updateGuildIconCheck(self.imagePath)

    def _doUploadCheck(self):
        p = BigWorld.player()
        guildIconUpLoadInterval = GCD.data.get('guildIconUpLoadInterval', 0)
        amount = GCD.data.get('cleanUploadCDItemAmount', 0)
        itemCnt = commGuild.getGuildFlagItemCnt(p, amount, guildIconUpLoadInterval)
        cleanUploadCDItemId = GCD.data.get('cleanUploadCDItemId')
        if cleanUploadCDItemId and p.inv.canRemoveItems({cleanUploadCDItemId: itemCnt}, enableParentCheck=True):
            p.cell.updateGuildIconCheck(self.imagePath)
        else:
            itemName = ID.data.get(cleanUploadCDItemId, {}).get('name', '')
            p.showGameMsg(GMDD.data.NOS_UPLOAD_FAILED_NO_SUCH_ITEM, (itemCnt, itemName))

    def _cancelUpload(self):
        self.setUploadBtn(True)

    def setUploadBtn(self, flag):
        self.mediator and self.mediator.Invoke('setUploadBtn', GfxValue(flag))

    def _realUpload(self, guildIcon):
        p = BigWorld.player()
        p.uploadNOSFile(guildIcon, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_GUILD_FLAG, {'gbId': p.gbId,
         'guildNUID': p.guildNUID,
         'guildName': p.guildName}, self.onGuildIconNOSServiceDone, (None,))

    def onGuildIconNOSServiceDone(self, key, otherArgs):
        gamelog.debug('@hjx guildIcon#onGuildIconNOSServiceDone:', key)
        p = BigWorld.player()
        if key:
            p.cell.setGuildIconStatus(gametypes.NOS_FILE_STATUS_PENDING)
            self.refreshUserDefineInfo()
            p.cell.updateGuildIcon(key)
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_UPLOAD_SUCC, ())
            self.setUploadBtn(True)
        else:
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_UPLOAD_FAILED, ())

    def onUseClick(self, *arg):
        p = BigWorld.player()
        if p.guildIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            gamelog.error('@hjx onUseClick failed:', p.guildIconStatus)
            return
        self.morpherFactory.morpherIns[uiConst.ZHAN_QI_MORPHER_HUIJI].subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE].isUsed = True
        self.applyTint(self.headGen)
        if self.mediator:
            self.mediator.Invoke('setSaveBtn', GfxValue(True))

    def stopPreviewGuild(self):
        p = BigWorld.player()
        if p.topLogo:
            p.topLogo.removeGuildIcon()
            p.topLogo.addGuildIcon(p.guildFlag)

    def onShowClick(self, *arg):
        self.applyShowTint(self.headGen)
        p = BigWorld.player()
        p.topLogo.setGuildImage('../../' + self.imagePath, '', True)
        if self.previewCallback:
            BigWorld.cancelCallback(self.previewCallback)
        self.previewCallback = BigWorld.callback(10, self.stopPreviewGuild)

    def checkUserDefValid(self):
        p = BigWorld.player()
        if not p.inWorld:
            return False
        elif p.guildNUID == 0:
            return False
        elif p.guild is None:
            return False
        elif p.guild.memberMe.roleId not in gametypes.GUILD_ROLE_LEADERS:
            return False
        else:
            return True

    def onGetUserDefFileInfo(self, *arg):
        gamelog.debug('@hjx guildIcon#onGetUserDefFileInfo')
        infoDict = {'isUploaded': False,
         'filePath': '',
         'status': gametypes.NOS_FILE_STATUS_PENDING}
        p = BigWorld.player()
        if not self.checkUserDefValid():
            return uiUtils.dict2GfxDict(infoDict, True)
        if p.guildIcon == '':
            return uiUtils.dict2GfxDict(infoDict, True)
        infoDict['isUploaded'] = True
        if p.isGuildIconDownloaded():
            infoDict['filePath'] = uiUtils.getGuildIconPath(p.guildIcon)
        else:
            infoDict['filePath'] = '../' + self.imagePath
        infoDict['status'] = p.getGuildIconStatus()
        infoDict['isUsed'] = p.isGuildIconUsed()
        return uiUtils.dict2GfxDict(infoDict)

    def onUserDefFileClick(self, *arg):
        p = BigWorld.player()
        enableUserDefGuildCrest = gameglobal.rds.configData.get('enableUserDefGuildCrest', False)
        if not enableUserDefGuildCrest:
            p.showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())
            return GfxValue(False)
        elif not self.checkUserDefValid():
            return GfxValue(False)
        else:
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.guildIcon, gametypes.NOS_FILE_PICTURE, p.onGuildIconDownloadNOSFile, (None,))
            return GfxValue(True)

    def getFailedReason(self):
        p = BigWorld.player()
        ret = ''
        if p.getGuildIconStatus() == gametypes.NOS_FILE_STATUS_ILLEGAL:
            ret += p.nosFileStatusCache[p.guildIcon][2]['annotation']
        return ret

    def onGetFailedReason(self, *arg):
        return GfxValue(gbk2unicode(self.getFailedReason()))

    def onClickRefresh(self, *arg):
        p = BigWorld.player()
        p.refreshNOSFileStatus(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.guildIcon, gametypes.NOS_FILE_PICTURE, p.onRefreshNOSFileStatus, ())

    def onGetRefreshLimit(self, *arg):
        p = BigWorld.player()
        guildIconRefreshCD = GCD.data.get('guildIconRefreshCD', 10)
        delta = guildIconRefreshCD - (utils.getNow() - p.guildIconRefreshTime)
        return GfxValue(delta)

    def startRefreshTimer(self):
        if self.mediator:
            self.mediator.Invoke('startRefreshTimer')

    def refreshUserDefineStatus(self):
        p = BigWorld.player()
        if self.mediator:
            self.mediator.Invoke('refreshUserDefineStatus', (GfxValue(p.getGuildIconStatus()), GfxValue(gbk2unicode(self.getFailedReason()))))

    def refreshUserDefineInfo(self):
        gamelog.debug('@hjx guildIcon#refreshUserDefineInfo:')
        if self.mediator:
            self.mediator.Invoke('setUserDefinePanel')
