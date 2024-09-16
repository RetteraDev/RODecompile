#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impEvaluate.o
import gameglobal
import gamelog
import gametypes
import utils
import const
from guis import uiConst
from callbackHelper import Functor
from data import item_data as ID
from data import evaluate_set_data as ESD
from cdata import evaluate_set_appearance_reverse_data as ESARD

class ImpEvaluate(object):

    def onQueryEvaluateInfo(self, evaluateInfo):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\xbd\x93\xe5\x89\x8d\xe8\xaf\x84\xe4\xbb\xb7\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param evaluateInfo:
        :return:
        """
        gamelog.debug('@zq onQueryEvaluateInfo', evaluateInfo)
        self.evaluateAlreadyPush = []
        self.evaluateInfo = evaluateInfo
        self._evaluateRefreshInfo()
        self.calcEvaluatePushMessage()

    def updateEvaluateInfo(self, evaluateInfo):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe5\xbd\x93\xe5\x89\x8d\xe7\x9a\x84\xe8\xaf\x84\xe4\xbb\xb7\xe6\x95\xb0\xe6\x8d\xae
        :param evaluateInfo:
        :return:
        """
        gamelog.debug('@zq updateEvaluateInfo', evaluateInfo)
        self.evaluateInfo = evaluateInfo
        self._evaluateRefreshInfo()
        self.calcEvaluatePushMessage()

    def getCanEvaluatePlay(self, playEvaId):
        if not gameglobal.rds.configData.get('enableEvaluate', False):
            return False
        else:
            eData = ESD.data.get(playEvaId, {})
            if eData:
                beginTime = eData.get('beginTime', None)
                endTime = eData.get('endTime', None)
                if beginTime and endTime and not utils.inCrontabRangeWithYear(beginTime, endTime):
                    return False
                peInfo = self.evaluateInfo.get('playEvaluateInfo', {})
                evaluate = peInfo.get(playEvaId, None)
                if not evaluate:
                    return False
                if evaluate.evaluated == gametypes.EVALUATE_APPLY_YES:
                    return False
                checkIds, count = eData.get('checkInfo', [(), 0])
                if evaluate.finishCount < count:
                    return False
                return True
            return False

    def getCanEvaluateItem(self, itemId):
        if not gameglobal.rds.configData.get('enableEvaluate', False):
            return False
        erData = ESARD.data.get(itemId, {})
        eID = erData.get('ID', 0)
        if eID:
            beginTime = erData.get('beginTime', None)
            endTime = erData.get('endTime', None)
            if beginTime and endTime and not utils.inCrontabRangeWithYear(beginTime, endTime):
                return False
            acSet = getattr(self, 'appearanceItemCollectSet', set([]))
            aeInfo = self.evaluateInfo.get('appearanceItemCollectEvaluateInfo', {})
            eState = aeInfo.get(eID, 0)
            pItemId = ID.data.get(itemId, {}).get('parentId', itemId)
            isHasItem = self.inv.hasItemInPages(pItemId, 1, enableParentCheck=True)
            canEvaluate = False
            if eState == gametypes.EVALUATE_APPLY_NO:
                canEvaluate = True
            elif eState == gametypes.EVALUATE_APPLY_BEFORE:
                canEvaluate = gameglobal.rds.ui.evaluatePlay.isOwnedItem(itemId)
            elif eState == gametypes.EVALUATE_APPLY_AFTER:
                canEvaluate = False
            return canEvaluate
        else:
            return False

    def getCanEvaluateItemPushMessage(self, itemId, inSet = False):
        if not gameglobal.rds.configData.get('enableEvaluate', False):
            return False
        erData = ESARD.data.get(itemId, {})
        appearType = erData.get('appearType', ())
        if uiConst.EVALUATE_APPEARTYPE_PUSH not in appearType:
            return
        eID = erData.get('ID', 0)
        if eID:
            beginTime = erData.get('beginTime', None)
            endTime = erData.get('endTime', None)
            if beginTime and endTime and not utils.inCrontabRangeWithYear(beginTime, endTime):
                return False
            acSet = getattr(self, 'appearanceItemCollectSet', set([]))
            acNewSet = self.evaluateInfo.get('appearanceItemCollectNewSet', set([]))
            aeInfo = self.evaluateInfo.get('appearanceItemCollectEvaluateInfo', {})
            eState = aeInfo.get(eID, 0) if aeInfo else 0
            pItemId = ID.data.get(itemId, {}).get('parentId', itemId)
            isHasItem = self.inv.hasItemInPages(pItemId, 1, enableParentCheck=True)
            canEvaluate = False
            if (gameglobal.rds.ui.evaluatePlay.isOwnedItem(itemId) or inSet) and itemId in acNewSet and eState < gametypes.EVALUATE_APPLY_AFTER:
                canEvaluate = True
            return canEvaluate
        else:
            return False

    def calcEvaPlayPushMessage(self):
        for k, v in self.evaluateInfo.get('playEvaluateInfo', {}).iteritems():
            eData = ESD.data.get(k, {})
            appearType = eData.get('appearType', ())
            if uiConst.EVALUATE_APPEARTYPE_PUSH not in appearType:
                return
            result = self.getCanEvaluatePlay(k)
            if result:
                dList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_EVALUATE_PLAY)
                _data = {'showId': k,
                 'showType': uiConst.EVALUATE_SHOWTYPE_PALY}
                alreadyPush = self.isEvaluatePushMessageHasData(_data, getattr(self, 'evaluateAlreadyPush', []))
                isIn = self.isEvaluatePushMessageHasData(_data, dList)
                if isIn or alreadyPush:
                    continue
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_EVALUATE_PLAY, {'click': Functor(self.clickEvaPlayPushMessage, uiConst.MESSAGE_TYPE_EVALUATE_PLAY)})
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_EVALUATE_PLAY, {'data': _data})

    def calcEvaItemPushMessage(self):
        acSet = getattr(self, 'appearanceItemCollectSet', set([]))
        for k in acSet:
            result = self.getCanEvaluateItemPushMessage(k, True)
            if result:
                dList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_EVALUATE_ITEM)
                _data = {'showId': k,
                 'showType': uiConst.EVALUATE_SHOWTYPE_ITEM}
                alreadyPush = self.isEvaluatePushMessageHasData(_data, getattr(self, 'evaluateAlreadyPush', []))
                isIn = self.isEvaluatePushMessageHasData(_data, dList)
                if isIn or alreadyPush:
                    continue
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_EVALUATE_ITEM, {'click': Functor(self.clickEvaPlayPushMessage, uiConst.MESSAGE_TYPE_EVALUATE_ITEM)})
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_EVALUATE_ITEM, {'data': _data})

    def isEvaluatePushMessageHasData(self, val, dList):
        aShowId = val.get('showId', None)
        aShowType = val.get('showType', None)
        if not aShowId or not aShowType:
            return False
        else:
            for x in dList:
                showId = x.get('data', {}).get('showId', None)
                showType = x.get('data', {}).get('showType', None)
                if aShowId == showId and aShowType == showType:
                    return True

            return False

    def calcEvaluatePushMessage(self):
        if not hasattr(self, 'evaluateAlreadyPush'):
            self.evaluateAlreadyPush = []
        self.calcEvaPlayPushMessage()
        self.calcEvaItemPushMessage()

    def _evaluateRefreshInfo(self):
        gameglobal.rds.ui.playRecommActivation.refreshItemTip()
        gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()
        gameglobal.rds.ui.guibaoge.refreshPreviewInfo()
        gameglobal.rds.ui.guibaoge.refreshAllSlot()

    def clickEvaPlayPushMessage(self, msgType):
        lData = gameglobal.rds.ui.pushMessage.getLastData(msgType)
        _data = lData.get('data', None)
        if not _data:
            return
        else:
            showId = _data.get('showId', None)
            showType = _data.get('showType', None)
            if showId and showType:
                gameglobal.rds.ui.evaluatePlay.show(showId, showType)
            gameglobal.rds.ui.pushMessage.removeData(msgType, lData)
            if not hasattr(self, 'evaluateAlreadyPush'):
                self.evaluateAlreadyPush = []
            self.evaluateAlreadyPush.append({'data': {'showId': showId,
                      'showType': showType}})
            return
