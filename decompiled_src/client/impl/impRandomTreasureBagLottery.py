#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRandomTreasureBagLottery.o
import gamelog
import gametypes
import gameglobal
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import random_lottery_data as RLD
from data import sys_config_data as SCD
MAX_CHOOSE_NUM = 8

class ImpRandomItemsLottery(object):

    def onSyncRandomItemsLotteryActivity(self):
        """
        \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe6\xb4\xbb\xe5\x8a\xa8\xe6\xaf\x8f\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x8e\xa8\xe9\x80\x81\xe5\x87\xbd\xe6\x95\xb0
        :return:
        """
        if not gameglobal.rds.configData.get('enableRandomTreasureBagMain', False):
            return
        if not gameglobal.rds.ui.randomTreasureBagMain.checkCanOpenMainProxy():
            return
        gameglobal.rds.ui.randomTreasureBagMain.requestAllData()
        gameglobal.rds.ui.randomTreasureBagMain.setNewUpdateMsgCallBack()
        gameglobal.rds.ui.randomTreasureBagMain.pushNewUpdateMsg()

    def onRandomItemsLotterySelectionRequest(self, ret, bagId, randomLotteryItems):
        """
        \xe5\xa5\x96\xe6\xb1\xa0\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :param bagId: \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\xb4\xbb\xe5\x8a\xa8id
        :param randomLotteryItems: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8crandomLotteryItems={\xe5\xa5\x96\xe6\xb1\xa0\xe7\x89\xa9\xe5\x93\x81, \xe6\x95\xb0\xe6\x8d\xae\xe4\xb8\xba {\xe5\xa5\x96\xe6\xb1\xa0groupId1\xef\xbc\x9a[itemId1, itemId2],\xe5\xa5\x96\xe6\xb1\xa0groupId2\xef\xbc\x9a[itemId3, itemId4],...,\xe5\xa5\x96\xe6\xb1\xa0groupId5\xef\xbc\x9a[itemId8],}
                                   \xe5\xa6\x82\xe6\x9e\x9cret != 0, randomLotteryItems={}
        :return:
        """
        if ret == gametypes.RANDOM_LOTTERY_SELECT_SUC:
            self.updatePlayerTreasureBagData(bagId, {'randomLotteryItems': randomLotteryItems})
            gameglobal.rds.ui.randomTreasureBagMain.refreshAll()
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_SELECTION_SUCCESS, ())
        elif ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_SELECTION_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_ITEM_NOT_MATCH:
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_SELECTION_FAILED_BY_ITEM_NOT_MATCH, ())
        elif ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_ALREADY_SELECT:
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_SELECTION_FAILED_BY_ALREADY_SELECT, ())

    def onRandomItemsSelectionReset(self, ret, bagId):
        """
        \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe9\x87\x8d\xe7\xbd\xae\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :param bagId: \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\xb4\xbb\xe5\x8a\xa8id
        :return:
        """
        if ret == gametypes.RANDOM_BAG_LOTTERY_RESET_SUC:
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_RESET_SUCCESS, ())
            if bagId in self.randomTreasureBag and 'randomLotteryItems' in self.randomTreasureBag[bagId]:
                self.updatePlayerTreasureBagData(bagId, {'randomLotteryItemsHistory': self.randomTreasureBag[bagId]['randomLotteryItems']})
            self.updatePlayerTreasureBagData(bagId, {'randomLotteryItems': {}})
            gameglobal.rds.ui.randomTreasureBagMain.refreshAll()
            gameglobal.rds.ui.randomTreasureBagMain.requestAllData()
        elif ret == gametypes.RANDOM_BAG_LOTTERY_RESET_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_RESET_FAILED_BY_INVALID_TIME, ())
        else:
            if ret == gametypes.RANDOM_BAG_LOTTERY_RESET_FAIL_BY_ITEM_NOT_SELECT:
                self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_RESET_FAILED_BY_ITEM_NOT_SELECT, ())
                return
            if ret == gametypes.RANDOM_BAG_LOTTERY_RESET_FAIL_BY_ITEM_NOT_ENOUGH:
                self.showGameMsg(GMDD.data.RANDOM_ITEMS_LOTTERY_RESET_FAILED_BY_ITEM_NOT_ENOUGH, ())
                return

    def onRandomItemsLotteryDrawRequest(self, ret, bagId, items):
        """
        \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\x8a\xbd\xe5\xa5\x961\xe6\xac\xa1
        :param ret:0 \xe8\xa1\xa8\xe7\xa4\xba\xe6\x8a\xbd\xe5\xa5\x96\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c \xe9\x9d\x9e0 \xe8\xa1\xa8\xe7\xa4\xba\xe6\x8a\xbd\xe5\xa5\x96\xe5\xa4\xb1\xe8\xb4\xa5
        :param bagId: \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8bid
        :param items: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8citems=[(groupId, itemId, pos)]
                      \xe5\xa6\x82\xe6\x9e\x9cret != 0, items=[]
        :return:
        """
        if ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_BAG_LOTTERY_DRAW_FAILED_BY_TIME_INVALID, ())
        if ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL_BY_ITEMS_NO_SELECT:
            self.showGameMsg(GMDD.data.RANDOM_BAG_LOTTERY_DRAW_FAILED_BY_ITEMS_NO_SELECT, ())
        elif ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        elif ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL_BY_CONSUME_ITEM_NOT_ENOUGH:
            self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_FAILED_BY_CONSUME_ITEM_NOT_ENOUGH, ())
        else:
            if ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_SUC:
                self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_SUCCESS, ())
                gameglobal.rds.ui.randomTreasureBagMain.startSelectItem(bagId, items)
                return
            if ret == gametypes.RANDOM_BAG_LOTTERY_DRAW_FAIL:
                self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_FAILED, ())
                return

    def onGetTotalItemsLotteryCount(self, bagId, totalLotteryCount):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\x8a\xbd\xe5\xa5\x96\xe8\xbd\xae\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param bagId: \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\xb4\xbb\xe5\x8a\xa8id
        :param curRoundNums: \xe7\x99\xbe\xe5\xae\x9d\xe8\xa2\x8b\xe6\x8a\xbd\xe5\xa5\x96\xe8\xbd\xae\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c
        :return:
        """
        self.updatePlayerTreasureBagData(bagId, {'totalLotteryCount': totalLotteryCount})

    def onReceiveRandomItemsLotteryDrawTotalReward(self, bagId, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe7\xb4\xaf\xe8\xae\xa1\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED_BY_INV_FULL, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.SHOP_BAG_LOCKED, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_ALREADY_RECEIVED:
            self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_TOTAL_REWARD_FAILED_BY_ALREADY_RECEIVED, ())
        else:
            if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_SUC:
                self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_TOTAL_REWARD_SUCCESS, ())
                gameglobal.rds.ui.randomTreasureBagMain.requesGetAccumulativeRewardData(bagId)
                return
            if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL:
                self.showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_TOTAL_REWARD_FAILED, ())
                return

    def onGetRoundFinishRewardMargins(self, bagId, finishRewardMargins):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe8\x87\xaa\xe9\x80\x89\xe5\xa5\x96\xe6\xb1\xa0\xe7\xb4\xaf\xe8\xae\xa1\xe6\x8a\xbd\xe5\xa5\x96\xe6\x95\xb0\xe6\x8d\xae\xe5\x87\xbd\xe6\x95\xb0
        :param finishRewardMargins: \xe5\xaf\xb9\xe5\xba\x94\xe5\xb7\xb2\xe9\xa2\x86\xe5\xa5\x96\xe7\x9a\x84\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\xa3\xe4\xbd\x8d\xe5\x92\x8c\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xa1\xa3\xe4\xbd\x8d\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        self.getAccumulativeRewardDataByFinishRewardMarginsData(bagId, finishRewardMargins)

    def getPlayerAllTreasureBagData(self, forceRefresh = True):
        if gameglobal.rds.ui.randomTreasureBagMain.drawing:
            forceRefresh = False
        if hasattr(self, 'randomBagLotteryInfo') and self.randomBagLotteryInfo:
            for bagId, bagDataDict in self.randomBagLotteryInfo.iteritems():
                self.updatePlayerTreasureBagData(bagId, bagDataDict, False)
                if 'finishRewardMargins' in bagDataDict:
                    self.getAccumulativeRewardDataByFinishRewardMarginsData(bagId, bagDataDict['finishRewardMargins'], False)

        self.updatePlayerTreasureBagData(forceRefresh=forceRefresh)

    def updatePlayerTreasureBagData(self, bagId = 0, resultDict = None, forceRefresh = True):
        if bagId and resultDict:
            if not hasattr(self, 'randomTreasureBag'):
                self.randomTreasureBag = {}
            if bagId not in self.randomTreasureBag:
                self.randomTreasureBag[bagId] = {}
            for name, value in resultDict.iteritems():
                self.randomTreasureBag[bagId][name] = value

        if forceRefresh:
            gameglobal.rds.ui.randomTreasureBagMain.refreshAll()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def getCurBaseBonusIndex(self, finishRewardMarginsDict):
        maxValue = 0
        for key in finishRewardMarginsDict.iterkeys():
            if key is not 'finishRewardLoopMargin':
                maxValue = max(maxValue, key)

        return maxValue

    def getAccumulativeRewardDataByFinishRewardMarginsData(self, bagId, finishRewardMargins, forceRefresh = True):
        self.updatePlayerTreasureBagData(bagId, {'curBaseBonusIndex': self.getCurBaseBonusIndex(finishRewardMargins)}, False)
        if 'finishRewardLoopMargin' in finishRewardMargins:
            self.updatePlayerTreasureBagData(bagId, {'curLoopBonusIndex': finishRewardMargins['finishRewardLoopMargin']}, False)
        self.updatePlayerTreasureBagData(forceRefresh=forceRefresh)
