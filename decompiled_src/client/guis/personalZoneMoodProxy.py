#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneMoodProxy.o
import BigWorld
import gametypes
import gameglobal
import C_ui
import os
import utils
import const
import gamelog
import time
import gameconfigCommon
from ui import unicode2gbk, gbk2unicode
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis import uiConst
from PIL import Image
from helpers import pyq_interface
from gamestrings import gameStrings
from helpers import taboo
from guis import richTextUtils
from callbackHelper import Functor
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import personal_zone_config_data as PZCD
MAX_PICTURE_NUM = 3

class PersonalZoneMoodProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneMoodProxy, self).__init__(uiAdapter)
        self.widget = None
        self.pictures = []
        self.uploadImgPath = []
        self.topicData = []
        self.isSending = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_MOOD, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_MOOD:
            self.widget = widget
            self.pictures = []
            self.uploadImgPath = []
            self.topicData = []
            self.isSending = False
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_MOOD)
        self.stopCallback()

    def reset(self):
        self.callback = None
        self.facePanel = None
        self.topicId = 0
        self.curUploadInfo = {}

    def show(self, topicId = 0):
        self.topicId = topicId
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_MOOD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.sendBtn.enabled = True
        ASUtils.setHitTestDisable(self.widget.maxCharsDesc, True)
        self.widget.addEventListener(events.MOUSE_CLICK, self.handleWidgetClick, False, 0, True)
        self.widget.msgInput.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleMsgInputFocusIn, False, 0, True)
        self.widget.msgInput.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleMsgInputFocusOut, False, 0, True)
        self.widget.pictureBtn.addEventListener(events.MOUSE_CLICK, self.handlePictureBtnClick, False, 0, True)
        self.widget.sendBtn.addEventListener(events.MOUSE_CLICK, self.handleSendBtnClick, False, 0, True)
        self.widget.faceBtn.addEventListener(events.MOUSE_CLICK, self.handleFaceBtnClick, False, 0, True)
        self.widget.talkDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectTalkDown, False, 0, True)
        self.widget.talkDropdown.visible = gameconfigCommon.enablePYQTopic()
        self.widget.topicDesc.visible = gameconfigCommon.enablePYQTopic()
        self.widget.msgInput.maxChars = 124
        pyq_interface.getTopic(self.topicCallBack)

    def topicCallBack(self, rStatus, content):
        if not self.widget:
            return
        gamelog.info('@yj .. personalZoneMoodProxy .. topicCallBack .. rStatus, content=', rStatus, content)
        self.topicData = [{'name': gameStrings.PERSONAL_ZONE_MOOD_NO_TOPIC,
          'id': 0}] + content.get('data', [])
        typeList = []
        initIndex = 0
        for i, value in enumerate(self.topicData):
            typeInfo = {}
            typeInfo['label'] = value.get('name', '')
            typeInfo['typeIndex'] = i
            if self.topicId == value.get('id', ''):
                initIndex = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.talkDropdown, typeList)
        self.widget.talkDropdown.menuRowCount = min(len(typeList), 5)
        if self.widget.talkDropdown.selectedIndex == -1:
            self.widget.talkDropdown.selectedIndex = initIndex

    def refreshInfo(self):
        if not self.widget:
            return
        self.updatePicture()

    def handleMsgInputFocusIn(self, *args):
        if not self.widget:
            return
        self.widget.maxCharsDesc.visible = False

    def handleMsgInputFocusOut(self, *args):
        if not self.widget:
            return
        if self.widget.msgInput.text == '':
            self.widget.maxCharsDesc.visible = True
        else:
            self.widget.maxCharsDesc.visible = False

    def handleSelectTalkDown(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            pass

    def handlePictureBtnClick(self, *args):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.PERSONAL_ZONE_MOOD_OPEN_PIC_TXT, gameStrings.PERSONAL_ZONE_MOOD_OPEN_FORMAT_TXT, '..\\screenshot', self.doSelectFile)

    def doSelectFile(self, path):
        if not os.path.exists(path):
            return
        elif '.' in os.path.basename(os.path.splitext(path)[0]):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_NAME_ILLEGAL, {}).get('text', gameStrings.IMAGE_PATH_CONTAIN_POINT_ERROR))
            return
        elif not (path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg') or path.endswith('.JPG') or path.endswith('.PNG') or path.endswith('.JPEG')):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_SUFFIX_NAME_ILLEGAL, {}).get('text', gameStrings.IMAGE_PATH_FUFFIX_NAME_ERROR))
            return
        else:
            photoFileName = os.path.basename(path)
            fileName = str(hash(photoFileName.split('.')[0]))
            srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + photoFileName
            newSrcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + 'mood%d' % time.time() + photoFileName
            imagePath = const.IMAGES_DOWNLOAD_DIR + '/mood%d' % time.time() + fileName + '.jpg'
            im = None
            try:
                uiUtils.copyToImagePath(path)
                im = Image.open(srcResPath)
                im.save(newSrcResPath)
                enablePNGProfileIcon = gameglobal.rds.configData.get('enablePNGProfileIcon', False)
                if enablePNGProfileIcon:
                    im.save(imagePath)
                else:
                    BigWorld.convert2DXT5(newSrcResPath, const.IMAGES_DOWNLOAD_DIR)
            except:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.IMAGE_PATH_ERROR)
                return

            if self.widget:
                imageImage = im
                self.pictures.append({'path': path,
                 'filePath': '../' + imagePath,
                 'imgsize': imageImage.size,
                 'uploadImgPath': imagePath})
                self.updatePicture()
            return

    def updatePicture(self):
        for i in xrange(MAX_PICTURE_NUM):
            picture = self.widget.getChildByName('picture%d' % i)
            picture.idx = i
            if i < len(self.pictures):
                picture.visible = True
                picture.gotoAndStop('pic')
                picture.icon.fitSize = True
                picture.icon.loadImage(self.pictures[i]['filePath'])
                picture.cancelBtn.visible = True
                picture.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
                picture.icon.addEventListener(events.MOUSE_CLICK, self.handlePictureClick, False, 0, True)
            elif i == len(self.pictures):
                picture.visible = True
                picture.gotoAndStop('addPic')
                picture.cancelBtn.visible = False
                picture.addPic.addEventListener(events.MOUSE_CLICK, self.handlePictureBtnClick, False, 0, True)
            else:
                picture.visible = False
                picture.cancelBtn.visible = False

        self.widget.pictureBtn.enabled = not len(self.pictures) == MAX_PICTURE_NUM

    def handlePictureClick(self, *args):
        e = ASObject(args[3][0])
        pictureMc = e.currentTarget.parent
        gameglobal.rds.ui.personalZonePicture.show(self.pictures, pictureMc.idx)

    def handleCancelBtnClick(self, *args):
        e = ASObject(args[3][0])
        pictureMc = e.currentTarget.parent
        self.pictures.pop(pictureMc.idx)
        self.updatePicture()

    def handleSendBtnClick(self, *args):
        p = BigWorld.player()
        self.curUploadInfo = {}
        moodDesc = self.widget.msgInput.richText
        if not moodDesc and not self.pictures:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_EMPYT, ())
            return
        msg = gameglobal.rds.ui.summonedWarSpriteChat.analysisChatMsg(moodDesc)
        result, announcement = taboo.checkDisbWord(msg)
        if richTextUtils.isSysRichTxt(announcement):
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        if not result:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        result, announcement = taboo.checkBWorld(announcement)
        if not result:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        if taboo.checkMonitorWord(announcement):
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        if not gameglobal.rds.configData.get('enableNOSCustom', False):
            p.showGameMsg(GMDD.data.UPLOAD_FRIEND_ICON_UNAVAILABLE, ())
            return
        self.widget.sendBtn.enabled = False
        self.isSending = True
        self.uploadImgPath = []
        for i in xrange(len(self.pictures)):
            impPath = self.pictures[i]['uploadImgPath']
            p.uploadNOSFile(impPath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_FRIEND_ICON, {'gbId': p.gbId,
             'roleName': p.realRoleName}, self.onNOSServiceDone, (i,))

        self.checkUploadFinish(announcement)

    def onNOSServiceDone(self, key, otherArgs):
        gamelog.info('@zq .. onNOSServiceDone .. key=', key, otherArgs)
        p = BigWorld.player()
        if key:
            self.uploadImgPath.append(key)
        else:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_PHOTO_UPLOAD_FAIL, (otherArgs + 1,))
            self.stopCallback()
            if self.widget:
                self.widget.sendBtn.enabled = True

    def checkUploadFinish(self, announcement):
        if len(self.uploadImgPath) != len(self.pictures):
            self.callback = BigWorld.callback(0, Functor(self.checkUploadFinish, announcement))
            return
        if not self.isSending:
            return
        if self.widget:
            self.widget.sendBtn.enabled = True
        self.isSending = False
        self.stopCallback()
        imgUrl = ''
        for impKey in self.uploadImgPath:
            if not imgUrl:
                imgUrl = impKey
            else:
                imgUrl = imgUrl + ',' + impKey

        self.curUploadInfo = {'imgUrl': imgUrl,
         'announcement': announcement,
         'imgUrlNum': len(self.uploadImgPath)}
        p = BigWorld.player()
        if len(self.uploadImgPath):
            p.base.checkNosImage(gametypes.NOS_NUM_LIMIT_OP_TYPE_PYQ)
        else:
            self.realSend()

    def onCheckNosImage(self, isValid):
        if not isValid:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.NOS_NUM_LIMIT_OP_TYPE_PYQ_MSG, ())
        else:
            self.realSend()

    def realSend(self):
        imgUrl = self.curUploadInfo.get('imgUrl', '')
        announcement = self.curUploadInfo.get('announcement', '')
        imgUrlNum = self.curUploadInfo.get('imgUrlNum', '')
        topicId = 0
        topicName = ''
        if self.topicData:
            topicId = self.topicData[self.widget.talkDropdown.selectedIndex]['id']
            topicName = self.topicData[self.widget.talkDropdown.selectedIndex]['name']
        gamelog.info('@yj .. checkUploadFinish .. announcement, imgUrl, topicId=', announcement, imgUrl, topicId)
        if topicId:
            msg = gameStrings.PERSONAL_ZONE_TOPIC_FORMAT_TXT % topicName
            topicStr = "<font color = \'%s\'>%s</font>" % ('#F38832', msg)
            announcement = topicStr + announcement
        announcement = announcement.decode('gbk').encode('utf8')
        p = BigWorld.player()
        p.base.addMoment(topicId)
        logInfo = {'topicId': topicId,
         'hasGraph': bool(imgUrl),
         'imgUrlNum': imgUrlNum}

        def _callBack(rStatus, content):
            self.uploadCallBack(rStatus, content, logInfo)

        pyq_interface.sendUserMoods(_callBack, imgUrl, announcement, topicId)

    def uploadCallBack(self, rStatus, content, logInfo):
        gamelog.info('@zq .. uploadCallBack .. rStatus, content=', rStatus, content)
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            momentId = content.get('data', {}).get('id', 0)
            p = BigWorld.player()
            topicId = logInfo.get('topicId', 0)
            hasGraph = logInfo.get('hasGraph', 0)
            p.base.genPyqMomentLog(gametypes.PERSONAL_ZONE_PYQ_OP_SEND_MOMENT, momentId, 0, 0, 0, topicId, 0, hasGraph)
            imgUrlNum = logInfo.get('imgUrlNum', 0)
            p.base.updateNosImage(gametypes.NOS_NUM_LIMIT_OP_TYPE_PYQ, imgUrlNum)
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_SEND_SUCCESS, ())
            self.uiAdapter.personalZoneFriend.refreshCurPageMoments()
            self.hide()
        self.curUploadInfo = {}

    def handleFaceBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.facePanel:
            self.facePanel = self.widget.getInstByClsName('ChatFacePanel')
            self.facePanel.addEventListener(events.FACE_CLICK, self.handleFaceClick, False, 0, True)
            self.widget.addChild(self.facePanel)
            self.facePanel.x = self.widget.faceBtn.x - 14
            self.facePanel.y = self.widget.faceBtn.y - self.facePanel.height + 4
        self.facePanel.visible = True
        e.stopImmediatePropagation()

    def handleFaceClick(self, *args):
        e = ASObject(args[3][0])
        faceStr = utils.faceIdToString(int(e.data))
        self.widget.msgInput.insertRichText(faceStr)
        self.widget.msgInput.focused = 1
        self.facePanel.visible = False

    def handleWidgetClick(self, *args):
        if self.facePanel:
            self.facePanel.visible = False

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None
