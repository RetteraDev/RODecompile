#Embedded file name: /WORKSPACE/data/entities/client/helpers/searchitemhelper.o
import BigWorld
import utils
import const
from guis import uiConst
from gameclass import Singleton
from data import item_data as ID

def getInstance():
    return SearchItemHelper.getInstance()


class SearchTaskBase(object):

    def __init__(self, searchId, callback, argsInfo, cancelCallback):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        pass


class SearchTask(SearchTaskBase):

    def __init__(self, searchId, callback, argsInfo, cancelCallback):
        self.searchId = searchId
        self.argsInfo = argsInfo
        self.callback = callback
        self.cancelCallback = cancelCallback
        self.callbackId = 0
        self.itemIds = []
        self.dataIter = None
        self.isCancel = False

    def start(self):
        self.dataIter = self.getInitDataIter()
        self.itemIds = []
        self.isCancel = False
        self.process()

    def getInitDataIter(self):
        return ID.data.iteritems()

    def stop(self):
        self.isCancel = True

    def process(self):
        if self.isCancel:
            if self.cancelCallback:
                self.cancelCallback(self.searchId)
            return
        complete = self.processItemData()
        if not complete:
            if self.callbackId:
                BigWorld.cancelCallback(self.callbackId)
            self.callbackId = BigWorld.callback(0, self.process)
        elif self.callback:
            self.callback(self.searchId, self.itemIds)

    def processItemData(self):
        pass


class ConsignTask(SearchTask):

    def processItemData(self):
        owner = self.argsInfo.get('owner', None)
        name = self.argsInfo.get('name', 0)
        school = self.argsInfo.get('school', -1)
        mType = self.argsInfo.get('mType', -1)
        sType = self.argsInfo.get('sType', -1)
        consignType = self.argsInfo.get('consignType', 0)
        hasItemName = self.argsInfo.get('hasItemName', 0)
        forme = self.argsInfo.get('forme', 0)
        limitNum = 500
        count = 0
        p = BigWorld.player()
        while True:
            if count > uiConst.TABAUCTION_PROCESS_SEARCH_NUM:
                return False
            itemId, itemData = next(self.dataIter, (0, {}))
            if not itemId:
                break
            count += 1
            itemName = itemData.get('name', '')
            if len(name) > len(itemName):
                continue
            if name in itemName:
                if consignType == uiConst.CONSIGN_TYPE_COMMON and utils.getItemNoConsign(itemData):
                    continue
                if consignType == uiConst.CONSIGN_TYPE_COIN and not utils.getItemCoinConsign(itemData):
                    continue
                if forme:
                    if itemData.get('lvReq', 0) > p.lv:
                        continue
                    if p.school not in itemData.get('schReq', ()):
                        continue
                elif school != -1:
                    if school not in itemData.get('schReq', ()):
                        continue
                if mType != -1:
                    if mType != itemData.get('category', 0):
                        continue
                    if sType != -1 and sType != itemData.get('subcategory', 0):
                        continue
                hasItemName = hasItemName or itemName == name
                self.argsInfo['hasItemName'] = hasItemName
                if itemName == name:
                    self.itemIds.insert(0, itemId)
                else:
                    self.itemIds.append(itemId)
                if len(self.itemIds) >= const.ITEM_CONSIGN_MATCH and hasItemName:
                    break

        return True


class CrossServerConsignTask(SearchTask):

    def processItemData(self):
        owner = self.argsInfo.get('owner', None)
        name = self.argsInfo.get('name', 0)
        school = self.argsInfo.get('school', -1)
        mType = self.argsInfo.get('mType', -1)
        sType = self.argsInfo.get('sType', -1)
        hasItemName = self.argsInfo.get('hasItemName', 0)
        forme = self.argsInfo.get('forme', 0)
        count = 0
        p = BigWorld.player()
        while True:
            if count > uiConst.TABAUCTION_PROCESS_SEARCH_NUM:
                return False
            itemId, itemData = next(self.dataIter, (0, {}))
            if not itemId:
                break
            count += 1
            if not utils.getItemCrossConsign(itemData):
                continue
            if name in itemData.get('name', ''):
                if forme:
                    if itemData.get('lvReq', 0) > p.lv:
                        continue
                    if p.school not in itemData.get('schReq', ()):
                        continue
                elif school != -1:
                    if school not in itemData.get('schReq', ()):
                        continue
                if mType != -1:
                    if mType != itemData.get('category', 0):
                        continue
                    if sType != -1 and sType != itemData.get('subcategory', 0):
                        continue
                hasItemName = hasItemName or itemData.get('name') == name
                self.argsInfo['hasItemName'] = hasItemName
                if itemData.get('name') == name:
                    self.itemIds.insert(0, itemId)
                else:
                    self.itemIds.append(itemId)
                if len(self.itemIds) >= const.ITEM_CONSIGN_MATCH and hasItemName:
                    break

        return True


class SearchItemHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.sId = 1
        self.taskDict = {}

    def _addSearchItemTask(self, argsInfo, callback, task, searchId):
        self.taskDict[searchId] = {'callback': callback,
         'task': task}
        self.sId += 1
        task.start()

    def taskComplete(self, searchId, itemIds):
        if searchId not in self.taskDict:
            return
        completeFunc = self.taskDict.get(searchId, {}).get('callback', None)
        completeFunc(searchId, itemIds)
        del self.taskDict[searchId]

    def _taskStopCallback(self, searchId):
        if searchId not in self.taskDict:
            return
        del self.taskDict[searchId]

    def cancelTask(self, searchId):
        task = self.taskDict.get(searchId, {}).get('task', None)
        if task:
            task.stop()

    def addConsignTask(self, argsInfo, callback):
        searchId = self.sId
        task = ConsignTask(searchId, self.taskComplete, argsInfo, self._taskStopCallback)
        self._addSearchItemTask(argsInfo, callback, task, searchId)
        return searchId

    def addCrossServerConsignTask(self, argsInfo, callback):
        searchId = self.sId
        task = CrossServerConsignTask(searchId, self.taskComplete, argsInfo, self._taskStopCallback)
        self._addSearchItemTask(argsInfo, callback, task, searchId)
        return searchId
