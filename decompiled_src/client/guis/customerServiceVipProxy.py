#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/customerServiceVipProxy.o
from gamestrings import gameStrings
import json
import BigWorld
import gameglobal
import utils
import C_ui
import os
import gametypes
from guis.uiProxy import UIProxy
from Scaleform import GfxValue
from PIL import Image
from gamestrings import gameStrings
from ui import gbk2unicode
from ui import unicode2gbk
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
TYPE_WEB_LINK = 0
TYPE_SPRITE = 1
TYPE_SECOND = 2
TYPE_USER_BIND_PAGE = 3

class CustomerServiceVipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CustomerServiceVipProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshContent': self.onRefreshContent,
         'confirmRequest': self.onConfirmRequest,
         'askDanDan': self.onAskDanDan,
         'sendContent': self.onSendContent,
         'selectFile': self.onSelectFile}
        self.mediator = None
        self.buttonData = []
        self.announcement = ''
        self.filePath = ''
        self.canUpload = False
        self.isUploading = False
        self.confirmInfo = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_CUSTOMER_SERVICE_VIP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CUSTOMER_SERVICE_VIP:
            self.mediator = mediator

    def reset(self):
        self.filePath = ''
        self.canUpload = False
        self.isUploading = False

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CUSTOMER_SERVICE_VIP)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CUSTOMER_SERVICE_VIP)

    def onRefreshContent(self, *args):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            info = {'enableUploadPic': gameglobal.rds.configData.get('enableCustomerVipServiceUploadPic', False),
             'announcement': self.announcement,
             'buttonData': self.buttonData}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onSendContent(self, *args):
        contentName = unicode2gbk(args[3][0].GetString().strip())
        content = unicode2gbk(args[3][1].GetString().strip())
        userName = unicode2gbk(args[3][2].GetString().strip())
        phoneNum = unicode2gbk(args[3][3].GetString().strip())
        p = BigWorld.player()
        if self.isUploading:
            p.showGameMsg(GMDD.data.CUSTOMER_SERVICE_VIP_PIC_UPLOADING, ())
            return None
        elif len(contentName) == 0:
            p.showGameMsg(GMDD.data.VIP_MSG_CONTENT_NAME_NEED, ())
            return None
        elif len(content) == 0:
            p.showGameMsg(GMDD.data.VIP_MSG_CONTENT_NEED, ())
            return None
        elif len(phoneNum) == 0:
            p.showGameMsg(GMDD.data.VIP_MSG_PHONE_NEED, ())
            return None
        else:
            self.confirmInfo = {'contentName': contentName,
             'content': content,
             'userName': userName,
             'phoneNum': phoneNum}
            if gameglobal.rds.configData.get('enableCustomerVipServiceUploadPic', False) and self.canUpload:
                self.isUploading = True
                p.uploadNOSFile(self.filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_CUSTOMER_SERVICE_VIP, {'gbId': p.gbId,
                 'roleName': p.realRoleName}, self.onNOSServiceDone, (None,))
            else:
                self.realConfirm()
            return None

    def onNOSServiceDone(self, key, otherArgs):
        p = BigWorld.player()
        self.isUploading = False
        if key:
            content = '%s NOSKey:%s' % (self.confirmInfo.get('content', ''), key)
            self.confirmInfo['content'] = content
            p.showGameMsg(GMDD.data.CUSTOMER_SERVICE_VIP_PIC_UPLOAD_SUCCESS, ())
            self.realConfirm()
        else:
            p.showGameMsg(GMDD.data.CUSTOMER_SERVICE_VIP_PIC_UPLOAD_FAIL, ())

    def realConfirm(self):
        contentName = self.confirmInfo.get('contentName', '')
        userName = self.confirmInfo.get('userName', '')
        phoneNum = self.confirmInfo.get('phoneNum', '')
        content = self.confirmInfo.get('content', '')
        BigWorld.player().base.submitProblemToGM(contentName, userName, phoneNum, content)

    def onAskDanDan(self, *args):
        gameglobal.rds.ui.help.show()

    def onConfirmRequest(self, *args):
        idx = int(args[3][0].GetNumber())
        if idx < len(self.buttonData):
            data = self.buttonData[idx]
            if data['btnType'] == TYPE_WEB_LINK:
                BigWorld.openUrl(data['content'])
            elif data['btnType'] == TYPE_SPRITE:
                gameglobal.rds.ui.help.show(data['content'])
            elif data['btnType'] == TYPE_SECOND:
                gameglobal.rds.ui.customerServiceSecond.queryToShow(idx)
            elif data['btnType'] == TYPE_USER_BIND_PAGE:
                if gameglobal.rds.configData.get('enableBindReward', False):
                    gameglobal.rds.ui.accountBind.show()
                else:
                    gameglobal.rds.ui.userAccountBind.show()

    def queryToShow(self):
        p = BigWorld.player()
        if p and p.__class__.__name__ == 'PlayerAvatar':
            p.base.getCustomerServiceAnnouncement()

    def showCallBack(self, announcement, category):
        self.buttonData = []
        for item in category:
            if item:
                itemData = json.loads(item, encoding=utils.defaultEncoding())
                newData = {}
                newData['content'] = itemData['Content'].encode(utils.defaultEncoding())
                newData['btnName'] = itemData['BtnName'].encode(utils.defaultEncoding())
                newData['btnType'] = int(itemData['BtnType'])
                self.buttonData.append(newData)

        self.announcement = announcement
        self.show()

    def onSelectFile(self, *args):
        if not gameglobal.rds.configData.get('enableCustomerVipServiceUploadPic', False):
            return
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CUSTOMERSERVICEVIPPROXY_179, workPath, self.doSelectFile)

    def doSelectFile(self, path):
        if not self.mediator:
            return
        if not gameglobal.rds.configData.get('enableCustomerVipServiceUploadPic', False):
            return
        if not path or not (path.endswith('.jpg') or path.endswith('.png')):
            return
        self.filePath = path
        i = path.rfind('\\')
        i = path.rfind('/') if i == -1 else i
        fileName = path if i == -1 else path[i + 1:]
        i = fileName.find('.')
        extension = fileName[i:]
        fileName = fileName if i == -1 else fileName[:i]
        showName = fileName + extension
        self.canUpload = False
        p = BigWorld.player()
        try:
            im = Image.open(self.filePath)
            size = im.size
            if size[0] * size[1] > gameglobal.MAX_PHOTO_SIZE * gameglobal.MAX_PHOTO_SIZE:
                p.showGameMsg(GMDD.data.CUSTOMER_SERVICE_VIP_PIC_OPEN_FAIL_BY_MAXSIZE, ())
            else:
                self.canUpload = True
        except IOError:
            p.showGameMsg(GMDD.data.CUSTOMER_SERVICE_VIP_PIC_OPEN_FAIL_BY_TYPE, ())

        if not self.canUpload:
            showName = gameStrings.CUSTOMER_SERVICE_VIP_PIC_UPLOAD_ERROR_PATH
        self.mediator.Invoke('setFilePath', GfxValue(gbk2unicode(showName)))
