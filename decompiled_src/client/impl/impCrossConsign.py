#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCrossConsign.o
import time
import BigWorld
import gamelog
import gameglobal
import cPickle
import zlib
import const
import utils
from callbackHelper import Functor
from guis import uiConst
from cdata import coin_consign_config_Data as CCCD

class ImpCrossConsign(object):
    """
    \xe8\xb7\xa8\xe6\x9c\x8d\xe6\x8b\x8d\xe5\x8d\x96\xe8\xa1\x8c CrossConsign or XConsign \xe7\x8e\xa9\xe5\xae\xb6\xe6\x8e\xa5\xe5\x8f\xa3\xef\xbc\x88Client\xef\xbc\x89
        2016-10-26 hzshengmaojia@corp.netease.com
    
        \xe4\xbb\x8b\xe7\xbb\x8d\xe8\xa7\x81 CrossConsignCentralStub.py
    """

    def notifyCoinFromXConsign(self, opType, coinNum, clrDBID, itemID):
        gamelog.debug('@zq notifyCoinFromXConsign', opType, coinNum, clrDBID, itemID)
        info = {'opType': opType,
         'coinNum': coinNum,
         'clrDBID': clrDBID,
         'itemId': itemID}
        if opType == const.XCONSIGN_OP_TYPE_OVERBID:
            if info in gameglobal.rds.ui.tabAuctionCrossServer.bidFailedPushMessageInfo:
                return
            gameglobal.rds.ui.tabAuctionCrossServer.bidFailedPushMessageInfo.append(info)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED, {'click': Functor(self.openNotifyCoinFromXConsignMessage, uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID)})
            msgInfo = gameglobal.rds.ui.tabAuctionCrossServer.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED, msgInfo=msgInfo)
        elif opType == const.XCONSIGN_OP_TYPE_COINSOLD:
            if info in gameglobal.rds.ui.tabAuctionCrossServer.sellSuccessPushMessageInfo:
                return
            gameglobal.rds.ui.tabAuctionCrossServer.sellSuccessPushMessageInfo.append(info)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS, {'click': Functor(self.openNotifyCoinFromXConsignMessage, uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD)})
            msgInfo = gameglobal.rds.ui.tabAuctionCrossServer.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS, msgInfo=msgInfo)
        elif opType == const.XCONSIGN_OP_TYPE_FAIL2BID:
            if info in gameglobal.rds.ui.tabAuctionCrossServer.submitFailedPushMessageInfo:
                return
            gameglobal.rds.ui.tabAuctionCrossServer.submitFailedPushMessageInfo.append(info)
            gameglobal.rds.ui.tabAuctionCrossServer.submitFailedPushMessageInfo.sort(key=lambda x: x['coinNum'], reverse=True)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED, {'click': Functor(self.openNotifyCoinFromXConsignMessage, uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID)})
            msgInfo = gameglobal.rds.ui.tabAuctionCrossServer.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED, msgInfo=msgInfo)
        else:
            gamelog.debug('@zq notifyCoinFromXConsign err opType', opType, coinNum, clrDBID, itemID)

    def openNotifyCoinFromXConsignMessage(self, opNUID):
        gamelog.debug('@zq openNotifyCoinFromXConsignMessage')
        gameglobal.rds.ui.tabAuctionCrossServer.openXConsignPushMessage(opNUID)

    def onXConsignItemRes(self, errCode, curDBID):
        if errCode == const.XCONSIGN_ERRCODE_NOT_ERROR:
            gamelog.debug('@zq onXConsignItemRes OK', curDBID)
            gameglobal.rds.ui.tabAuctionCrossServer.onXConsignItemRes(curDBID)
        else:
            gamelog.debug('@zq onXConsignItemRes Fail', errCode)

    def onXConsignWithdrawRes(self, errCode, curDBID):
        if errCode == const.XCONSIGN_ERRCODE_NOT_ERROR:
            gamelog.debug('@zq onXConsignWithdrawRes OK', curDBID)
            gameglobal.rds.ui.tabAuctionCrossServer.onXConsignWithdrawRes(curDBID)
        else:
            gamelog.debug('@zq onXConsignWithdrawRes Fail', errCode)

    def onXConsignBidRes(self, errCode, curDBID):
        if errCode == const.XCONSIGN_ERRCODE_NOT_ERROR:
            gamelog.debug('@zq onXConsignBidRes OK', curDBID)
            gameglobal.rds.ui.tabAuctionCrossServer.onXConsignBidRes(curDBID)
        else:
            gameglobal.rds.ui.tabAuctionCrossServer.refreshOneCurItemWithUpdate([curDBID])
            gamelog.debug('@zq onXConsignBidRes Fail', errCode, curDBID)

    def onXConsignBiddingDBIDs(self, opNUID, listCurDBID):
        gamelog.debug('@zq onXConsignBiddingDBIDs', opNUID, listCurDBID)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignBiddingDBIDs(opNUID, listCurDBID)

    def onXConsignSellingDBIDs(self, opNUID, listCurDBID):
        gamelog.debug('@zq onXConsignSellingDBIDs', opNUID, listCurDBID)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignSellingDBIDs(opNUID, listCurDBID)

    def onXConsignFollowingDBIDs(self, opNUID, listCurDBID):
        gamelog.debug('@zq onXConsignFollowingDBIDs', opNUID, listCurDBID)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignFollowingDBIDs(opNUID, listCurDBID)

    def onXConsignHistories(self, opNUID, listResDBID):
        gamelog.debug('@zq onXConsignHistories', opNUID, listResDBID)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignHistories(opNUID, listResDBID)

    def onXConsignInfoByResultClrDBIDs(self, opNUID, compressedDict):
        gamelog.debug('@zq onXConsignInfoByResultClrDBIDs', opNUID)
        res = cPickle.loads(zlib.decompress(compressedDict))
        gameglobal.rds.ui.tabAuctionCrossServer.onGetHisItemInfoFormServer(opNUID, res)

    def onGetXConsignInfoByCurDBIDs(self, opNUID, compressedDict, volatileOnly, errCode):
        gamelog.debug('@zq onGetXConsignInfoByCurDBIDs', opNUID, volatileOnly, errCode)
        if errCode != const.XCONSIGN_ERRCODE_NOT_ERROR:
            return
        res = cPickle.loads(zlib.decompress(compressedDict))
        gameglobal.rds.ui.tabAuctionCrossServer.onGetCurItemInfoFormServer(opNUID, res, volatileOnly)

    def onSearchXConsignByID(self, opNUID, curDBIDs, errCode, advArgs):
        gamelog.debug('@zq onSearchXConsignByID', opNUID, curDBIDs, errCode, advArgs)
        if errCode == const.XCONSIGN_ERRCODE_NOT_ERROR:
            gameglobal.rds.ui.tabAuctionCrossServer.onSearchXConsignByID(opNUID, curDBIDs)
        else:
            gamelog.debug('@zq onSearchXConsignByID Fail', errCode)

    def onSearchXConsignByType(self, opNUID, curDBIDs, errCode, advArgs):
        gamelog.debug('@zq onSearchXConsignByID', opNUID, curDBIDs, advArgs)
        if errCode == const.XCONSIGN_ERRCODE_NOT_ERROR:
            gameglobal.rds.ui.tabAuctionCrossServer.onSearchXConsignByID(opNUID, curDBIDs)
        else:
            gamelog.debug('@zq onSearchXConsignByType Fail', errCode)

    def onXConsignFollowDone(self, itemID, curDBID, newFollowCount):
        gamelog.debug('@zq onXConsignFollowDone', itemID, curDBID, newFollowCount)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignFollowDone(curDBID, newFollowCount)

    def onXConsignCancelFollowDone(self, itemID, curDBID, newFollowCount):
        gamelog.debug('@zq onXConsignCancelFollowDone', itemID, curDBID, newFollowCount)
        gameglobal.rds.ui.tabAuctionCrossServer.onXConsignCancelFollowDone(curDBID, newFollowCount)

    def onGetXConsignAvgPrice(self, itemID, avgPrice):
        gamelog.debug('@zq onGetXConsignAvgPrice', itemID, avgPrice)
        gameglobal.rds.ui.tabAuctionCrossServer.onUpdatePrice(itemID, avgPrice)

    def openAuctionFun(self, npcId = 0, layoutType = uiConst.LAYOUT_DEFAULT, searchItemName = '', seekId = 0):
        if gameglobal.rds.configData.get('enableTabAuction', False):
            gameglobal.rds.ui.tabAuctionConsign.show(npcId=npcId, layoutType=uiConst.LAYOUT_NPC_FUNC, searchItemName=searchItemName, seekId=seekId)
        else:
            gameglobal.rds.ui.consign.show(npcId=npcId, layoutType=uiConst.LAYOUT_NPC_FUNC, searchItemName=searchItemName, seekId=seekId)

    def closeAuctionFun(self):
        gameglobal.rds.ui.tabAuction.hide()
        gameglobal.rds.ui.consign.hide()

    def setXConsignStartCallBack(self):
        serverProgressMsId = CCCD.data.get('crossConsignServerProgressID', 0)
        if not self._isSoul() and gameglobal.rds.configData.get('enableCrossConsign', False) and gameglobal.rds.configData.get('enableTabAuction', False) and self.checkServerProgress(serverProgressMsId, False):
            limit = 0
            coinConsignLimit = CCCD.data.get('crossConsignSellMax', {})
            coinConsignLimit = sorted(coinConsignLimit.items(), reverse=True)
            for data in coinConsignLimit:
                if self.lv >= data[0]:
                    limit = data[1]
                    break

            if not limit > 0:
                return
            if getattr(gameglobal.rds.ui.tabAuctionCrossServer, 'xconsignStartCallBack', None):
                BigWorld.cancelCallback(gameglobal.rds.ui.tabAuctionCrossServer.xconsignStartCallBack)
                gameglobal.rds.ui.tabAuctionCrossServer.xconsignStartCallBack = None
            dayBegin = CCCD.data.get('xConsignTime2PubEnd', 1859) + 1
            _hours = int(dayBegin / 100)
            _min = int(dayBegin % 100)
            while _min >= 60:
                _min -= 60
                _hours += 1

            tmpT = utils.localtimeEx(utils.getNow())
            _time1 = tmpT.tm_hour * 60 * 60 + tmpT.tm_min * 60 + tmpT.tm_sec
            _time2 = _hours * 60 * 60 + _min * 60
            delay = _time2 - _time1
            if delay > 0:
                gameglobal.rds.ui.tabAuctionCrossServer.xconsignStartCallBack = BigWorld.callback(delay, self._xconsignStart)
                gamelog.debug('@zq setXConsignStartCallBack', delay)

    def _xconsignStart(self):
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_XCONSIGN_START, {'click': self._xconsignStartClick})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_START)

    def _xconsignStartClick(self):
        gameglobal.rds.ui.tabAuction.show(uiConst.TABAUCTION_TAB_CROSS_SERVER)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_START)
