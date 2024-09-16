#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceHeadSettingProxy.o
from gamestrings import gameStrings
import time
import os
from PIL import Image
from Scaleform import GfxValue
import BigWorld
import gamelog
import gameglobal
import gametypes
import const
import C_ui
import utils
import math
from guis.ui import unicode2gbk
from guis.ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from gamestrings import gameStrings
from data import personal_zone_head_data as PZHD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import item_data as ID
from data import photo_border_data as PBD
SYSHEADTYPE = {1: gameStrings.TEXT_SPACEHEADSETTINGPROXY_32,
 2: gameStrings.TEXT_SPACEHEADSETTINGPROXY_33,
 3: gameStrings.TEXT_EASYPAYPROXY_538}
DEFAULTPHOTO = 'headIcon/%s.dds'
TAB_SET_HEAD = 0
TAB_SYS_HEAD = 1
TAB_BORDER_HEAD = 2

class SpaceHeadSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpaceHeadSettingProxy, self).__init__(uiAdapter)
        self.modelMap = {'getBaseInfo': self.onGetBaseInfo,
         'setCurTab': self.onSetCurTab,
         'getCurHead': self.onGetCurHead,
         'selectFile': self.onSelectFile,
         'scaleImage': self.onScaleImage,
         'saveFunc': self.onSaveFunc,
         'getHeadData': self.onGetHeadData,
         'setCurSysHead': self.onSetCurSysHead,
         'getBorderHeadData': self.onGetBorderHeadData,
         'setCurBorderHeadId': self.onSetCurBorderHeadId,
         'getTabBtnVisible': self.onGetTabBtnVisible,
         'getSchoolHeadIcon': self.onGetSchoolHeadIcon,
         'getShowTabIndex': self.onGetShowTabIndex}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACE_HEAD_SETTING, self.hide)
        self.reset()
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACE_HEAD_SETTING:
            self.mediator = mediator

    def onGetBaseInfo(self, *args):
        baseInfo = {}
        p = BigWorld.player()
        baseInfo['iconState'] = p.profileIconStatus
        baseInfo['isUsed'] = p.profileIconUsed
        baseInfo['isUpload'] = p.iconUpload
        baseInfo['preview'] = self._preview
        return uiUtils.dict2GfxDict(baseInfo, True)

    def onGetCurHead(self, *args):
        if self.curTab == uiConst.HEADTYPE_CUSTOM:
            return GfxValue(self.customHead)
        elif self.curTab == uiConst.HEADTYPE_SYS:
            return GfxValue(self.sysHead)
        elif self.curTab == uiConst.HEADTYPE_BORDER:
            return GfxValue(self.customHead)
        else:
            return ''

    def onGetHeadData(self, *args):
        _data = PZHD.data
        types = SCD.data.get('SYSHEADTYPE', SYSHEADTYPE)
        ret = []
        for key in types:
            tempItem = {'labelName': types[key],
             'items': []}
            ret.append(tempItem)

        for v in _data:
            iconPath = _data.get(v, {}).get('iconPath', '')
            _type = _data.get(v, {}).get('type', 1) - 1
            if _type > len(types):
                _type = len(types) - 1
            labelType = _data.get(v, {}).get('labelType', 0)
            tips = _data.get(v, {}).get('desc', '')
            _school = _data.get(v, {}).get('school', '')
            _sex = _data.get(v, {}).get('sex', '')
            headItem = {'iconPath': iconPath,
             'type': _type,
             'labelType': labelType,
             'tips': tips}
            if self.school == _school and self.sex == _sex:
                ret[_type]['items'].append(headItem)

        return uiUtils.array2GfxAarry(ret, True)

    def refreshPhotoBorderList(self):
        p = BigWorld.player()
        currents = []
        defaults = []
        unlockeds = []
        unUnlockeds = []
        defaultBorderId = SCD.data.get('defaultBorderId', 0)
        for key in PBD.data.keys():
            if key == defaultBorderId:
                defaults.append(defaultBorderId)
                continue
            if key == p.photoBorder.borderId:
                currents.append(key)
            elif not p.photoBorder.isExpire(key):
                unlockeds.append(key)
            else:
                unUnlockeds.append(key)

        self.photoBorderList = currents + defaults + sorted(unlockeds, reverse=True) + sorted(unUnlockeds, reverse=True)

    def onGetBorderHeadData(self, *args):
        ret = []
        p = BigWorld.player()
        self.refreshPhotoBorderList()
        for key in self.photoBorderList:
            value = PBD.data.get(key, {})
            itemInfo = {}
            itemInfo['borderId'] = key
            itemInfo['name'] = value.get('name', '')
            itemInfo['useDesc'] = value.get('useDesc', '')
            itemInfo['iconPath40'] = p.getPhotoBorderIcon(key, uiConst.PHOTO_BORDER_ICON_SIZE40)
            itemInfo['iconPath108'] = p.getPhotoBorderIcon(key, uiConst.PHOTO_BORDER_ICON_SIZE108)
            itemInfo['isInUse'] = p.photoBorder.borderId == key
            if self.fromItemBorderId:
                itemInfo['isSelected'] = key == self.fromItemBorderId
            else:
                itemInfo['isSelected'] = key == p.photoBorder.borderId
            if key in p.photoBorder.borderDict:
                endTime = p.photoBorder.borderDict[key].tTime
                if endTime == const.PHOTO_BORDER_FOREVER_EXPIRE_TIME:
                    timeDesc = gameStrings.PHOTO_BORDER_FOREVER_DESC
                    isShowlock = False
                else:
                    timeDesc = gameStrings.PHOTO_BORDER_TIME_LIMIT_DESC % time.strftime('%Y%m%d %H:%M', time.localtime(endTime))
                    isShowlock = utils.getNow() > endTime
            else:
                timeDesc = ''
                isShowlock = True
            itemInfo['timeTxt'] = timeDesc
            itemInfo['isShowlock'] = isShowlock
            ret.append(itemInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetTabBtnVisible(self, *args):
        curTabIdx = int(args[3][0].GetNumber())
        if curTabIdx == uiConst.HEADTYPE_BORDER:
            return GfxValue(gameglobal.rds.configData.get('enablePhotoBorder', False))
        return GfxValue(True)

    def onGetSchoolHeadIcon(self, *args):
        schoolHeadIcon = self.customHead
        for v in PZHD.data:
            pzhdData = PZHD.data.get(v, {})
            school = pzhdData.get('school', '')
            sex = pzhdData.get('sex', '')
            if self.school == school and self.sex == sex and pzhdData.get('type', 1) == 1:
                schoolHeadIcon = pzhdData.get('iconPath', '')
                break

        return GfxValue(schoolHeadIcon)

    def onGetShowTabIndex(self, *args):
        if self.fromItemBorderId:
            return GfxValue(TAB_BORDER_HEAD)
        return GfxValue(TAB_SET_HEAD)

    def onSetCurBorderHeadId(self, *args):
        self.borderId = int(args[3][0].GetNumber())

    def onSetCurSysHead(self, *args):
        path = unicode2gbk(args[3][0].GetString())
        self.sysHead = path

    def onSetCurTab(self, *args):
        self.curTab = int(args[3][0].GetNumber())

    def onSelectFile(self, *arg):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_FRIENDPROXY_1501, workPath, self.doSelectFile)

    def doSelectFile(self, path):
        if not os.path.exists(path):
            return
        elif '.' in os.path.basename(os.path.splitext(path)[0]):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_NAME_ILLEGAL, {}).get('text', gameStrings.TEXT_FRIENDPROXY_1507))
            return
        elif not (path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg') or path.endswith('.JPG') or path.endswith('.PNG') or path.endswith('.JPEG')):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_SUFFIX_NAME_ILLEGAL, {}).get('text', gameStrings.TEXT_FRIENDPROXY_1510))
            return
        else:
            self.photoFileName = os.path.basename(path)
            fileName = self.photoFileName.split('.')[0]
            self.path = path
            self.srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + self.photoFileName
            self.imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + utils.getProfileIconSuffix()
            self.tgaPath = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.tga'
            im = None
            try:
                uiUtils.copyToImagePath(path)
                im = Image.open(self.srcResPath)
                self.srcSize = im.size
                im.save(self.srcResPath)
                enablePNGProfileIcon = gameglobal.rds.configData.get('enablePNGProfileIcon', False)
                if enablePNGProfileIcon:
                    im.save(self.imagePath)
                else:
                    BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
            except:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_SPACEHEADSETTINGPROXY_246)
                return

            if self.mediator:
                self.imageImage = im
                self.customHead = '../' + self.imagePath
                self.mediator.Invoke('setFilePath', (GfxValue(gbk2unicode(path)), GfxValue('../' + self.imagePath), uiUtils.array2GfxAarry(self.imageImage.size)))
            return

    def onScaleImage(self, *args):
        if self.imageImage:
            _scale = float(args[3][0].GetNumber())
            gamelog.debug('self.imageImage.size  ', _scale)
            gamelog.debug(self.imageImage.size)
            self.imageImage = self.imageImage.resize((int(self.srcSize[0] * _scale), int(self.srcSize[1] * _scale)))
            gamelog.debug(self.imageImage.size)
            self.imageImage.save(self.srcResPath)
            enablePNGProfileIcon = gameglobal.rds.configData.get('enablePNGProfileIcon', False)
            if enablePNGProfileIcon:
                self.imageImage.save(self.imagePath)
            else:
                BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
            if self.mediator:
                self.mediator.Invoke('setFilePath', (GfxValue(gbk2unicode(self.path)), GfxValue(gbk2unicode('../' + self.imagePath)), uiUtils.array2GfxAarry(self.imageImage.size)))

    def savePreview(self, _scale, _x, _y, _w, _h):
        if self.imageImage:
            gamelog.debug(os.path.exists(self.srcResPath))
            gamelog.debug(os.path.exists(self.imagePath))
            gamelog.debug(os.path.exists(self.tgaPath))
            self.previewImage = self.imageImage.resize((int(self.imageImage.size[0] * _scale), int(self.imageImage.size[1] * _scale)))
            self.previewImage = self.previewImage.crop((_x,
             _y,
             _w,
             _h))
            gamelog.debug('crop size', (_x,
             _y,
             _w,
             _h))
            self.converTmpPath()
            return True

    def converTmpPath(self):
        try:
            os.remove(self.srcResPath)
            os.remove(self.imagePath)
            os.remove(self.tgaPath)
        except:
            pass

        fileName = self.photoFileName.split('.')[0]
        self.srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + 'tmp%d' % time.time() + self.photoFileName
        enablePNGProfileIcon = gameglobal.rds.configData.get('enablePNGProfileIcon', False)
        self.imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + 'tmp%d' % time.time() + fileName + utils.getProfileIconSuffix()
        self.tgaPath = const.IMAGES_DOWNLOAD_DIR + '/' + 'tmp%d' % time.time() + fileName + '.tga'
        self.previewImage = self.previewImage.resize((256, 256))
        self.previewImage.save(self.srcResPath)
        if enablePNGProfileIcon:
            self.previewImage.save(self.imagePath)
        else:
            BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
        BigWorld.player().cell.updateImageName('tmp%d' % time.time() + fileName)

    def onSaveFunc(self, *args):
        if self.curTab == uiConst.HEADTYPE_CUSTOM:
            _scale = float(args[3][0].GetNumber())
            _x = int(args[3][1].GetNumber())
            _y = int(args[3][2].GetNumber())
            _w = int(args[3][3].GetNumber())
            _h = int(args[3][4].GetNumber())
            if self.savePreview(_scale, _x, _y, _w, _h):
                self.onUploadFile()
        elif self.curTab == uiConst.HEADTYPE_SYS:
            self.saveHeadKey(const.PERSONAL_ZONE_DATA_SYS_PHOTO)
        elif self.curTab == uiConst.HEADTYPE_BORDER:
            p = BigWorld.player()
            p.base.switchPhotoBorder(self.borderId)
            self.hide()

    def onUploadFile(self, *arg):
        p = BigWorld.player()
        if self.imagePath == '':
            return
        profileIconUpLoadInterval = GCD.data.get('profileIconUpLoadInterval', 3600)
        now = utils.getNow()
        if now - p.profileIconLastUploadTimestamp < profileIconUpLoadInterval:
            delta = profileIconUpLoadInterval - (now - p.profileIconLastUploadTimestamp)
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_TIME_LIMIT, (utils.formatDuration(delta),))
            return
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FRIENDPROXY_1561 % utils.formatDuration(profileIconUpLoadInterval), self.realUpload)

    def showUploadTime(self):
        itemId, amount = SCD.data.get('friendIconUploadItem', (0, 0))
        p = BigWorld.player()
        if not p.inv.canRemoveItems({itemId: amount}, enableParentCheck=True):
            p.showGameMsg(GMDD.data.CUSTOM_NEED_ITEM, ID.data.get(itemId, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1568))
        else:
            profileIconUpLoadInterval = GCD.data.get('profileIconUpLoadInterval', 3600)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FRIENDPROXY_1561 % utils.formatDuration(profileIconUpLoadInterval), self.realUpload)

    def realUpload(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableNOSCustom', False):
            p.showGameMsg(GMDD.data.UPLOAD_FRIEND_ICON_UNAVAILABLE, ())
            return None
        else:
            p.uploadNOSFile(self.imagePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_FRIEND_ICON, {'gbId': p.gbId,
             'roleName': p.realRoleName}, self.onNOSServiceDone, (None,))
            return None

    def onNOSServiceDone(self, key, otherArgs):
        p = BigWorld.player()
        if key:
            if p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING or p.profileIconStatus == gametypes.NOS_FILE_STATUS_APPROVED and p.profileIcon != p.friend.photo:
                p.base.abandonNOSFile(p.profileIcon)
            p.cell.updateProfileData(key, gametypes.NOS_FILE_STATUS_PENDING, False, True)
            p.iconUpload = True
            self.customHead = key
            self.saveHeadKey(const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO)
        else:
            p.showGameMsg(GMDD.data.USE_CUSTOM_PHOTO_UPLOAD_FAIL, ())

    def saveHeadKey(self, _type):
        p = BigWorld.player()
        keyList = [const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, const.PERSONAL_ZONE_DATA_SYS_PHOTO, const.PERSONAL_ZONE_DATA_CURR_PHOTO]
        valueList = [self.customHead, self.sysHead]
        if _type == const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO:
            valueList.append(self.sysHead)
        elif _type == const.PERSONAL_ZONE_DATA_SYS_PHOTO:
            valueList.append(self.sysHead)
            p.cell.updateProfileApply(False, p.iconUpload)
            p.cell.updateImageName('')
            p.imageName = ''
        else:
            valueList.append('')
        p.base.setPersonalZoneInfo(keyList, valueList)
        self.hide()

    def show(self, custom, sys, school, sex, preview, fromItemBorderId = 0):
        self.customHead = custom
        self.sysHead = sys
        self.school = school
        self.sex = sex
        self._preview = preview
        self.fromItemBorderId = fromItemBorderId
        self.uiAdapter.loadWidget(uiConst.WIDGET_SPACE_HEAD_SETTING)

    def clearWidget(self):
        self.mediator = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPACE_HEAD_SETTING)

    def reset(self):
        p = BigWorld.player()
        self.data = []
        self.curTab = -1
        self.customHead = ''
        self.sysHead = ''
        self._preview = ''
        self.imageImage = None
        self.previewImage = None
        self.srcSize = None
        self.school = -1
        self.sex = -1
        self.borderId = 0
        self.fromItemBorderId = 0
        self.photoBorderList = []

    def updateBodrerPanel(self, fromItemBorderId):
        if not self.mediator:
            return
        if self.curTab != uiConst.HEADTYPE_BORDER:
            return
        self.fromItemBorderId = fromItemBorderId
        page = 0
        self.refreshPhotoBorderList()
        for i in xrange(1, len(self.photoBorderList) + 1):
            if self.photoBorderList[i - 1] == self.fromItemBorderId:
                page = int(math.ceil(i / 9.0)) - 1
                break

        self.mediator.Invoke('refreshBorderHeadPanel', GfxValue(page))
