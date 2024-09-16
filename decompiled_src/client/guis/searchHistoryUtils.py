#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/searchHistoryUtils.o
from appSetting import Obj as AppSettings
from collections import deque
SEARCH_NAME_PATH = 'conf/ui/%s/searchName'
SEARCH_COUNT_PATH = 'conf/ui/%s/searchCount'

class SearchHistoryUtils(object):

    def __init__(self, arg):
        self.searchNamePath = SEARCH_NAME_PATH % arg
        self.searchCountPath = SEARCH_COUNT_PATH % arg
        self.searchHistoryQueue = deque([])
        self.searchHistoryCount = 0
        self.maxCount = 0

    def addSearchHistoryData(self, searchName):
        self.addQueueData(searchName)

    def addQueueData(self, data):
        self.searchHistoryCount = len(self.searchHistoryQueue)
        if data in self.searchHistoryQueue:
            self.searchHistoryQueue.remove(data)
            self.searchHistoryQueue.append(data)
        elif self.searchHistoryCount >= self.maxCount:
            self.searchHistoryQueue.popleft()
            self.searchHistoryQueue.append(data)
        else:
            self.searchHistoryQueue.append(data)

    def querySearchHistoryList(self, searchName):
        ret = []
        for name in list(self.searchHistoryQueue):
            if searchName in name:
                ret.append(name)

        return ret

    def readConfigData(self):
        self.searchHistoryCount = AppSettings.get(self.searchCountPath, 0)
        for i in range(self.searchHistoryCount):
            path = self.searchNamePath + str(i)
            self.searchHistoryQueue.append(AppSettings.get(path, ''))

    def writeConfigData(self):
        self.searchHistoryCount = len(self.searchHistoryQueue)
        AppSettings[self.searchCountPath] = self.searchHistoryCount
        for i in range(self.searchHistoryCount):
            path = self.searchNamePath + str(i)
            AppSettings[path] = self.searchHistoryQueue.popleft()

    def getReverseHistoryList(self):
        queueList = list(self.searchHistoryQueue)
        reverseList = queueList[::-1]
        return reverseList

    def getHistoryList(self):
        queueList = list(self.searchHistoryQueue)
        return queueList

    def printPath(self):
        print self.searchNamePath
