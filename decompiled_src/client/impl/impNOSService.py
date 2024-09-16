#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNOSService.o
from gamestrings import gameStrings
import BigWorld
from PIL import Image
import gamelog
import gametypes
import const
import gameglobal
import utils
from helpers import seqTask
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ImpNOSService(object):

    def uploadNOSFile(self, filePath, fileType, fileSrc, extra, callbackFunc = None, callbackArgs = ()):
        enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
        if not enableNOSService:
            return
        if fileType != gametypes.NOS_FILE_DUMP and '.' in filePath.split('/')[-1][:-4]:
            self.showGameMsg(GMDD.data.UPLOAD_PIC_FAIL_BY_INVALIDNAME, ())
            return
        gamelog.info('@szh uploadNOSFile ', filePath, fileType, fileSrc, extra)
        player = BigWorld.player()
        if not hasattr(player, 'nosUploadCallbackCaches'):
            player.nosUploadCallbackCaches = {}
        player.nosUploadCallbackCaches[filePath] = (fileType,
         fileSrc,
         extra,
         callbackFunc,
         callbackArgs)
        if extra.has_key('md5'):
            md5, timeStamp = extra.pop('md5')
            self.onFetchNOSKey(md5, timeStamp, filePath)
        else:
            player.base.fetchNOSKey(filePath)

    def onFetchNOSKey(self, md5, timeStamp, filePath):
        gamelog.info('@szh onFetchNOSKey, md5=%s, timeStamp=%d, filePath=%s' % (md5, timeStamp, filePath))
        player = BigWorld.player()
        if player.nosUploadCallbackCaches.has_key(filePath):
            fileType, fileSrc, extra, callbackName, callbackArgs = player.nosUploadCallbackCaches.pop(filePath)
        else:
            fileType, fileSrc, extra, callbackName, callbackArgs = (gametypes.NOS_FILE_UNKNOWN,
             None,
             None,
             None,
             None)
        seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_UPLOAD, (md5,
         timeStamp,
         filePath,
         fileType,
         fileSrc,
         extra), (callbackName, callbackArgs))

    def downloadNOSFile(self, filePath, key, fileType, callbackFunc, callbackArgs):
        if not self.inWorld:
            return
        else:
            enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
            if not enableNOSService:
                return
            if key is None or len(key) == 0:
                return
            gamelog.info('@szh downloadNOSFile ', filePath, key, fileType)
            player = BigWorld.player()
            if player.nosFileStatusCache.has_key(key):
                status, _, _ = player.nosFileStatusCache[key]
                if status == gametypes.NOS_FILE_STATUS_SERVER_APPROVED:
                    seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (filePath,
                     key,
                     fileType,
                     status), (callbackFunc, callbackArgs))
                else:
                    now = utils.getNow()
                    timeStamp = player.nosFileStatusTimeStamp.get(key, 0)
                    if status == gametypes.NOS_FILE_STATUS_PENDING and now - timeStamp > gametypes.NOS_STATUS_RE_FETCH_TIME:
                        seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_STATUS_CHECK, (filePath, key, fileType), (callbackFunc, callbackArgs))
                        return
                    if callbackFunc:
                        callbackFunc(status, *callbackArgs)
            else:
                seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_STATUS_CHECK, (filePath, key, fileType), (callbackFunc, callbackArgs))
            return

    def downloadCrossNOSFile(self, filePath, key, serverId, fileType, callbackFunc, callbackArgs):
        enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
        if not enableNOSService:
            return
        elif key is None or len(key) == 0:
            return
        else:
            gamelog.info('@szh downloadCrossNOSFile ', filePath, key, fileType)
            player = BigWorld.player()
            if player.nosFileStatusCache.has_key(key):
                status, _, _ = player.nosFileStatusCache[key]
                if status == gametypes.NOS_FILE_STATUS_SERVER_APPROVED:
                    seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (filePath,
                     key,
                     fileType,
                     status), (callbackFunc, callbackArgs))
                else:
                    now = utils.getNow()
                    timeStamp = player.nosFileStatusTimeStamp.get(key, 0)
                    if status == gametypes.NOS_FILE_STATUS_PENDING and now - timeStamp > gametypes.NOS_STATUS_RE_FETCH_TIME:
                        seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_STATUS_CROSS_CHECK, (filePath,
                         key,
                         serverId,
                         fileType), (callbackFunc, callbackArgs))
                        return
                    if callbackFunc:
                        callbackFunc(status, *callbackArgs)
            else:
                seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_STATUS_CROSS_CHECK, (filePath,
                 key,
                 serverId,
                 fileType), (callbackFunc, callbackArgs))
            return

    def isDownloadNOSFileCompleted(self, key):
        return self.nosFileStatusCache.has_key(key) and self.nosFileStatusCache[key][0] != gametypes.NOS_FILE_STATUS_SERVER_APPROVED

    def downloadNOSFileDirectly(self, filePath, key, fileType, callbackFunc, callbackArgs):
        enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
        if not enableNOSService:
            return
        elif key is None or len(key) == 0:
            return
        else:
            gamelog.info('@szh downloadNOSFileDirectly ', filePath, key, fileType)
            player = BigWorld.player()
            if player.nosFileStatusCache.has_key(key) and player.nosFileStatusCache[key][0] == gametypes.NOS_FILE_STATUS_APPROVED:
                if callbackFunc:
                    callbackFunc(player.nosFileStatusCache[key][0], *callbackArgs)
            else:
                seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (filePath,
                 key,
                 fileType,
                 gametypes.NOS_FILE_STATUS_DOWNLOAD_DIRECTLY), (callbackFunc, callbackArgs))
            return

    def refreshNOSFileStatus(self, filePath, key, fileType, callbackFunc, callbackArgs):
        player = BigWorld.player()
        if player.nosFileStatusCache.has_key(key):
            player.nosFileStatusCache.pop(key)
        self.downloadNOSFile(filePath, key, fileType, callbackFunc, callbackArgs)

    def onRefreshNOSFileStatus(self, status):
        self.cell.setGuildIconStatus(status)
        self.guildIconRefreshTime = utils.getNow()
        gameglobal.rds.ui.zhanQi.refreshUserDefineInfo()
        gameglobal.rds.ui.zhanQi.startRefreshTimer()

    def onFetchNOSFileStatus(self, status, fileType, key, extra):
        player = BigWorld.player()
        player.nosFileStatusCache[key] = (status, fileType, extra)
        player.nosFileStatusTimeStamp[key] = utils.getNow()
        seqTask.onFetchNOSFileStatus(status, fileType, key)

    def downloadYixinFile(self, account, urlpath, callbackFunc, callbackArgs):
        enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
        if not enableNOSService:
            return
        gamelog.info('@szh downloadYixinFile ', account, urlpath)
        seqTask.addYinxinSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (account, urlpath), (callbackFunc, callbackArgs))

    def downloadAudioFile(self, filePath, key, fileType, callbackFunc, callbackArgs):
        enableNOSService = gameglobal.rds.configData.get('enableNOSService', False)
        if not enableNOSService:
            return
        seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (filePath,
         key,
         fileType,
         gametypes.NOS_FILE_STATUS_SERVER_APPROVED), (callbackFunc, callbackArgs))

    def testDownloadNOSFile(self):
        for i in xrange(500):
            player = BigWorld.player()
            player.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, self.guildIcon, gametypes.NOS_FILE_PICTURE, self.onGuildIconDownloadNOSFile, (None,))

    def abandonNOSFile(self, fileKey):
        player = BigWorld.player()
        player.base.abandonNOSFile(fileKey)

    def checkCameraSharePicNum(self, num = 1):
        player = BigWorld.player()
        useAppVol = gameglobal.rds.configData.get('enableAppAlbumManualVol')
        if useAppVol:
            conf = SCD.data.get('AppAlbumVolByLevel', ((1, 30, 50, 60, 70), (50, 100, 200, 300, 400)))
            if player.lv < conf[0][0]:
                self.showGameMsg(GMDD.data.NOS_CAMERA_SHARE_PIC_MAX_NUM_15, (conf[0][0],))
                return False
        maxNum = getattr(self, 'appAlbumVolLimit', 0)
        if getattr(self, 'cameraSharePicNum', 10000) + num > maxNum:
            if not useAppVol:
                self.showGameMsg(GMDD.data.NOS_CAMERA_SHARE_PIC_MAX_NUM, (maxNum,))
            else:
                self.showGameMsg(GMDD.data.NOS_CAMERA_SHARE_PIC_MAX_NUM_APP, (str(getattr(self, 'cameraSharePicNum', 10000)) + '/' + str(maxNum),))
            return False
        return True

    def uploadCameraSharePic(self, filePath, callbackFunc = None, callbackArgs = (), idx = 0, allFileKeys = None):
        enableCameraShare = gameglobal.rds.configData.get('enableCameraShare', False)
        if not enableCameraShare:
            return False
        else:
            try:
                im = Image.open(filePath)
                size = im.size
                if size[0] * size[1] > gameglobal.MAX_PHOTO_SIZE * gameglobal.MAX_PHOTO_SIZE:
                    self.showGameMsg(GMDD.data.CAMERA_PIC_UPLOAD_FAIL_BY_MAXSIZE, ())
                    gameglobal.rds.ui.qrCode.onUpLoadSuccess(None, filePath)
                    return False
            except IOError:
                self.showGameMsg(GMDD.data.CAMERA_PIC_UPLOAD_FAIL_BY_TYPE, ())
                gameglobal.rds.ui.qrCode.onUpLoadSuccess(None, filePath)
                return False

            extra = {'gbId': self.gbId,
             'roleName': self.roleName}
            self.uploadNOSFile(filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_CAMERA_SHARE, extra, lambda fileKey, callbackFunc, callbackArgs, idx = idx, allFileKeys = allFileKeys: self.onUploadCameraSharePic(fileKey, callbackFunc, callbackArgs, idx, allFileKeys), (callbackFunc, callbackArgs))
            return True

    def uploadQRCodeSharePic(self, filePath, callbackFunc = None, callbackArgs = ()):
        if not gameglobal.rds.configData.get('enableQRCode', False):
            return False
        extra = {'gbId': self.gbId,
         'roleName': self.roleName}
        self.uploadNOSFile(filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_CAMERA_SHARE, extra, callbackFunc, callbackArgs)
        return True

    def onUploadCameraSharePic(self, fileKey, callbackFunc = None, callbackArgs = (), idx = 0, allFileKeys = None):
        gamelog.info('@szh onUploadCameraSharePic', fileKey)
        if fileKey:
            if allFileKeys is None:
                self.base.uploadCameraSharePic([fileKey])
            else:
                allFileKeys[idx] = fileKey
                if len([ x for x in allFileKeys if x ]) == len(allFileKeys):
                    self.base.uploadCameraSharePic(allFileKeys)
        if callbackFunc:
            callbackFunc(fileKey, *callbackArgs)

    def uploadCharSnapshot(self, filePath, callbackFunc = None, callbackArgs = ()):
        enableCharSnapshot = gameglobal.rds.configData.get('enableCharSnapshot', False)
        if not enableCharSnapshot:
            return False
        gamelog.info('@szh uploadCharSnapshot', filePath)
        try:
            im = Image.open(filePath)
            size = im.size
            if size[0] * size[1] > 4194304:
                self.showGameMsg(GMDD.data.CAMERA_PIC_UPLOAD_FAIL_BY_MAXSIZE, ())
                gameglobal.rds.ui.qrCode.uploadFailed()
                return False
        except IOError:
            self.showGameMsg(GMDD.data.CAMERA_PIC_UPLOAD_FAIL_BY_TYPE, ())
            gameglobal.rds.ui.qrCode.uploadFailed()
            return False

        extra = {'gbId': self.gbId,
         'roleName': self.roleName}
        self.uploadNOSFile(filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_CHAR_SNAPSHOT, extra, self.onUploadCharSnapshot, (callbackFunc, callbackArgs))
        return True

    def onUploadCharSnapshot(self, fileKey, callbackFunc = None, callbackArgs = ()):
        gamelog.info('@szh onUploadCharSnapshot', fileKey)
        if fileKey:
            self.cell.updateCharSnapShot(fileKey)
        if callbackFunc:
            callbackFunc(fileKey, *callbackArgs)
        if not fileKey:
            self.onUpdateCharSnapShot(fileKey)

    def takeCharSnapshotBeforeQuit(self, op = 0, resetNeed = True):
        if gameglobal.rds.configData.get('enableLogoutCharSnapshot', False):
            if self.charSnapshopOp == gametypes.CHAR_SNAPSHOT_EXIT_GAME_WAITING:
                self.charSnapshopOp = op
                if op == gametypes.CHAR_SNAPSHOT_EXIT_GAME:
                    gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPNOSSERVICE_291, hideBtn=True, isModal=True)
                return True
            if self.isAppBind and self.needCharSnapshot:
                if resetNeed:
                    self.needCharSnapshot = False
                self.base.checkCharSnapShotNum(op)
                return True
        return False

    def onCheckCharSnapShotNum(self, op, avail):
        self.needCharSnapshot = False
        if not avail:
            self._handleCharSnapshotOp(op)
        else:
            self.charSnapshopOp = op
            self.onCheckUploadCharSnapshot(fileName='figure.png')

    def onCheckNosImage(self, op, isValid):
        if op == gametypes.NOS_NUM_LIMIT_OP_TYPE_PYQ:
            gameglobal.rds.ui.personalZoneMood.onCheckNosImage(isValid)

    def onUpdateCharSnapShot(self, keyName):
        self._handleCharSnapshotOp(getattr(self, 'charSnapshopOp', 0))

    def _handleCharSnapshotOp(self, op):
        if op == gametypes.CHAR_SNAPSHOT_RETURN_TO_LOGIN:
            gameglobal.rds.ui._doReturnToLogin()
            self.charSnapshopOp = 0
        elif op == gametypes.CHAR_SNAPSHOT_EXIT_GAME:
            self.charSnapshopOp = 0
            gameglobal.rds.ui.playRecomm._doRealQuit()
        elif op == gametypes.CHAR_SNAPSHOT_EXIT_GAME_WAITING:
            self.charSnapshopOp = gametypes.CHAR_SNAPSHOT_EXIT_GAME_DONE

    def sendCameraSharePicNum(self, num):
        self.cameraSharePicNum = num

    def onAppAlbumVolLimit(self, val):
        self.appAlbumVolLimit = val
