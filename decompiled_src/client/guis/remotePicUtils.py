#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/remotePicUtils.o
from gamestrings import gameStrings
import BigWorld
import const
import gameglobal
import gametypes
import utils
from gameclass import Singleton
from appSetting import Obj as AppSettings
from helpers import remoteInterface
DLOAD_PIC_INTERVAL = 2
QUERY_PIC_VERSION_CD = 60
PIC_FLAG_PENDING = 0
PIC_FLAG_DOWNLOADING = 1
PIC_FLAG_DOWNLOADED = 2

def getInstance():
    return RemotePicMgr.getInstance()


class RemotePicMgr(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.pendingGroupList = []
        self.currentGroup = None
        self.currentPicInfo = None
        self.downLoadHandler = None

    def downloadPicRequest(self, group):
        if group in self.pendingGroupList:
            return
        else:
            self.pendingGroupList.append(group)
            if self.downLoadHandler:
                BigWorld.cancelCallback(self.downLoadHandler)
                self.downLoadHandler = None
            self.downLoadHandler = BigWorld.callback(0, self.downLoadPendingPic)
            return

    def downLoadPendingPic(self):
        self.currentPicInfo = self.popNextPendingPicInfo()
        if self.currentPicInfo == None:
            self.downLoadHandler = None
            self.pendingGroupList = []
            return
        else:
            p = BigWorld.player()
            if not p:
                return
            try:
                url = self.currentPicInfo.get('url', '').split('/')[-1]
                p.downloadNOSFileDirectly(const.IMAGES_DOWNLOAD_RELATIVE_DIR, url, gametypes.NOS_FILE_PICTURE, self.downloadFileDone, (url,))
            except:
                msg = 'Download Mall Ad Split Error'
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
                return

            self.downLoadHandler = BigWorld.callback(DLOAD_PIC_INTERVAL, self.downLoadPendingPic)
            return

    def popNextPendingPicInfo(self):
        if not self.pendingGroupList:
            return None
        else:
            for i, group in enumerate(self.pendingGroupList):
                if not group.pendingPicList:
                    continue
                picInfo = group.pendingPicList.pop(0)
                self.currentGroup = group
                return picInfo

            return None

    def downloadFileDone(self, status, callbackArgs):
        if status != gametypes.NOS_FILE_STATUS_APPROVED:
            return
        self.currentPicInfo['flag'] = PIC_FLAG_DOWNLOADED
        self.currentGroup.dloadedPicList.append(self.currentPicInfo)
        if not self.currentGroup.pendingPicList:
            if self.currentGroup.checkEval():
                self.currentGroup.downloadADOver()


class RemotePicGroup(object):

    def __init__(self):
        self.remoteKey = 'remoteKey'
        self.remoteQueryCD = QUERY_PIC_VERSION_CD
        self.lastQueryTime = 0
        self.pendingPicList = []
        self.dloadedPicList = []
        self.path = None
        self.remoteVersion = 0

    def enableRemotePic(self):
        if gameglobal.rds.configData.get('enableRemotePic', False):
            return True

    def reset(self):
        self.pendingPicList = []
        self.dloadedPicList = []

    def getPicInfoList(self):
        picInfoList = []
        if self.getVersion():
            picInfoList = self.getLocalPicInfoList()
        if not picInfoList:
            picInfoList = self.getBuiltInPicInfoList()
        self.queryRemotePicInfo()
        return picInfoList

    def queryRemotePicInfo(self):
        if not self.enableRemotePic():
            return
        now = utils.getNow()
        if now - self.lastQueryTime < self.remoteQueryCD:
            return
        self.lastQueryTime = now
        remoteInterface.queryRemotePicVersion(self.remoteKey, self.queryPicInfoCallback)

    def queryPicInfoCallback(self, status, data):
        if status != 200:
            return
        if not data:
            return
        if data.get('key', 'unknown') != self.remoteKey:
            return
        if BigWorld.isPublishedVersion() and data.get('switch', 'off') != 'on':
            return
        self.checkPicLenth(data)
        if not self.checkNewVersion(data.get('version', 0)):
            return
        self.dloadPicPrepare(data)
        getInstance().downloadPicRequest(self)

    def checkPicLenth(self, data):
        urlList = data.get('urlList', [])
        remotePicLenth = len(urlList)
        picNum = AppSettings.get(self.path + 'picNum', -1) + 1
        if remotePicLenth != picNum:
            AppSettings[self.path + 'version'] = 0

    def dloadPicPrepare(self, picData):
        urlList = picData.get('urlList', [])
        paramList = picData.get('paramList', [])
        if len(urlList) != len(paramList):
            raise Exception('RemotePicGroup, urlList, paramList config err: %s:(%d, %d)' % (self.remoteKey, len(urlList), len(paramList)))
        self.pendingPicList = []
        self.dloadedPicList = []
        for i, url in enumerate(urlList):
            picInfo = {}
            picInfo['idx'] = i
            picInfo['url'] = url
            picInfo['param'] = paramList[i]
            picInfo['flag'] = PIC_FLAG_PENDING
            self.pendingPicList.append(picInfo)

    def checkNewVersion(self, remoteVersion):
        currentVersion = self.getVersion()
        if currentVersion < int(remoteVersion):
            self.remoteVersion = remoteVersion
            return True
        else:
            return False

    def getVersion(self):
        versionPath = self.path + 'version'
        v = int(AppSettings.get(versionPath, 0))
        return v

    def checkEval(self):
        ret = True
        for i, item in enumerate(self.dloadedPicList):
            try:
                paramMap = eval(item.get('param', '1'))
            except:
                msg = gameStrings.TEXT_REMOTEPICUTILS_195
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
                ret = False

        return ret

    def getPathGroup(self, i):
        pathGroup = {}
        PIC_NUMBER = 'PIC' + str(i)
        pathGroup['ASAP_ICONNAME'] = self.path + PIC_NUMBER + '/iconName'
        pathGroup['ASAP_MAINID'] = self.path + PIC_NUMBER + '/mainId'
        pathGroup['ASAP_SUBID'] = self.path + PIC_NUMBER + '/subId'
        pathGroup['ASAP_TYPE'] = self.path + PIC_NUMBER + '/type'
        return pathGroup

    def downloadADOver(self):
        pass

    def writeList2config(self):
        pass

    def getDloadPicList(self):
        pass

    def getLocalPicInfoList(self, i):
        pass

    def getBuiltInPicInfoList(self):
        return []
