#Embedded file name: /WORKSPACE/data/entities/client/helpers/envsdkhelper.o
from collections import deque
import json
import BigWorld
import re
import gamelog
import utils
import gameglobal
from guis.ui import unicode2gbk, gbk2unicode
from gameclass import Singleton
from callbackHelper import Functor

class CheckTask(object):

    def __init__(self, info, callback):
        super(CheckTask, self).__init__()
        self.info = info
        self.callback = callback

    def doTask(self):
        content = self.info.get('content', '')
        getInstance().checkContent(content, self.callback)


class CheckTaskMgr(object):

    def __init__(self):
        super(CheckTaskMgr, self).__init__()
        self.checkInterval = 0.1
        self.checkMaxCache = 2000
        self.cycle = True
        self.taskCache = deque()
        self.timer = None

    def start(self):
        if self.timer:
            return
        self.__cycleCheck()

    def __cycleCheck(self):
        self.timer = None
        try:
            self.__doTaskOrder()
        except Exception as e:
            gamelog.error('dxk@CheckTaskMgr.__cycleCheck error', e.message)
            utils.reportExcept()

        if self.cycle:
            self.timer = BigWorld.callback(self.checkInterval, self.__cycleCheck)

    def __doTaskOrder(self):
        if len(self.taskCache) > 0:
            task = self.taskCache.pop()
            while task.expire == True and len(self.taskCache) > 0:
                task = self.taskCache.pop()

            if not task.expire:
                task.expire = True
                try:
                    task.doTask()
                except Exception as e:
                    gamelog.error('dxk:Error doTask except', e.message)

    def isEmpty(self):
        return len(self.taskCache) == 0

    def addTask(self, task):
        if len(self.taskCache) > self.checkMaxCache:
            return
        self.taskCache.appendleft(task)


class EnvSDKHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(EnvSDKHelper, self).__init__()
        self.envSDK = None
        self.envSDKInit = False
        self.tryInitTime = 0
        self.resetRetVal()

    def resetRetVal(self):
        self.valid = False
        self.content = ''
        self.resultContent = ''
        self.isReplace = False

    def initSDK(self):
        if self.envSDKInit:
            return
        if gameglobal.rds.configData.get('enableEnvSDK', False) and hasattr(BigWorld, 'PyEnvSDK'):
            if not self.envSDK:
                self.envSDK = BigWorld.PyEnvSDK()
                if gameglobal.rds.configData.get('enableEnvSDKLog', False) and hasattr(self.envSDK, 'setSwith'):
                    self.envSDK.setSwith('openLog', 1)
            self.doInit()
        else:
            self.envSDK = None

    def doInit(self):
        self.tryInitTime += 1
        if self.tryInitTime == 1:
            self.envSDK.initSDKAsync('pg', 'fui611z310iv84j6', 'optsdk.gameyw.netease.com', self.onInitCallBack)
        elif self.tryInitTime == 2:
            self.envSDK.initSDKAsync('pg', 'fui611z310iv84j6', 'optsdk-ipv6.gameyw.netease.com', self.onInitCallBack)
        else:
            self.envSDK.setSwith('IgnoreInitNetworkError', 1)
            self.envSDK.initSDKAsync('pg', 'fui611z310iv84j6', 'optsdk.gameyw.easebar.com', self.onInitCallBack)

    def testDoInit(self):
        self.envSDK = BigWorld.PyEnvSDK()
        self.envSDK.initSDKAsync('pg', 'fui611z310iv84j6', 'optsdk.gameyw.easebar.com', self.onInitCallBack)

    def onInitCallBack(self, code, message):
        if code == 200:
            self.envSDKInit = True
        elif self.tryInitTime <= 2:
            BigWorld.callback(1.0, self.doInit)
        elif gameglobal.rds.configData.get('enableEnvSDKLog', False):
            raise Exception('error: init envSDK failed:%s' % message.encode(utils.defaultEncoding()))

    def checkName(self, name):
        if self.envSDKInit:
            self.resetRetVal()
            utf8Name = gbk2unicode(name)
            self.envSDK.reviewNickname(utf8Name, Functor(self.output, False, name))
            return (self.valid, self.resultContent)

    def checkContentWithoutReplace(self, content, tag = 'normal'):
        if utils.needDisableUGC() and re.search('!\\$(010|023|103|180|178)', content):
            return (False, '')
        if self.envSDKInit:
            self.resetRetVal()
            utf8Content = gbk2unicode(content)
            utf8Tag = gbk2unicode(tag)
            levelStr = str(getattr(BigWorld.player(), 'lv', 1))
            self.envSDK.reivewWords(utf8Content, levelStr, utf8Tag, Functor(self.output, True, content))
            if self.isReplace:
                return (False, content)
            return (self.valid, self.resultContent)

    def checkContent(self, content, tag = 'normal'):
        if utils.needDisableUGC() and re.search('!\\$(010|023|103|180|178)', content):
            return (False, '')
        if self.envSDKInit:
            self.resetRetVal()
            utf8Content = gbk2unicode(content)
            utf8Tag = gbk2unicode(tag)
            levelStr = str(getattr(BigWorld.player(), 'lv', 1))
            self.envSDK.reivewWords(utf8Content, levelStr, utf8Tag, Functor(self.output, True, content))
            return (self.valid, self.resultContent)

    def checkContentEx(self, content, tag = 'normal'):
        if utils.needDisableUGC() and re.search('!\\$(010|023|103|180|178)', content):
            return (False, '', False)
        if self.envSDKInit:
            self.resetRetVal()
            utf8Content = gbk2unicode(content)
            utf8Tag = gbk2unicode(tag)
            levelStr = str(getattr(BigWorld.player(), 'lv', 1))
            self.envSDK.reivewWords(utf8Content, levelStr, utf8Tag, Functor(self.output, True, content))
            return (self.valid, self.resultContent, self.isReplace)

    def output(self, isContent, content, code, message):
        if isContent:
            if code == 100 or code == 200:
                self.valid = True
                self.resultContent = content
                self.isReplace = False
            elif code == 206:
                self.valid = True
                message = json.loads(message)
                replaceMsg = message.get('message', '')
                self.resultContent = unicode2gbk(replaceMsg.encode(utils.defaultEncoding()))
                self.isReplace = True
            else:
                self.valid = False
                self.resultContent = content
                self.isReplace = False
        elif code == 100 or code == 200:
            self.valid = True
            self.resultContent = content
        else:
            self.valid = False
            self.resultContent = content


def getInstance():
    instance = EnvSDKHelper.getInstance()
    return instance
