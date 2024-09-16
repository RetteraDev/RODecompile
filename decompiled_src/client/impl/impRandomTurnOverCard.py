#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRandomTurnOverCard.o
import gamelog
import gametypes
import gameglobal
from guis import uiConst
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import random_turn_over_card_data as RTOCD
MAX_CHOOSE_NUM = 8

class ImpRandomTurnOverCard(object):

    def onSyncRandomTurnOverCardActivity(self):
        """
        \xe7\xbf\xbb\xe7\x89\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe6\xaf\x8f\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x8e\xa8\xe9\x80\x81\xe5\x87\xbd\xe6\x95\xb0
        :return:
        """
        gameglobal.rds.ui.activitySaleTurnOverCard.pushTurnOverCardMessage()

    def onGetTotalTurnOverCount(self, totalTurnOverCount):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe7\xbf\xbb\xe7\x89\x8c\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param totalTurnOverCount: \xe7\xbf\xbb\xe7\x89\x8c\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c
        :return:
        """
        gamelog.debug('@zmm onGetTotalTurnOverCount', totalTurnOverCount)
        self.randomLotteryInfo['totalTurnOverCount'] = totalTurnOverCount
        gameglobal.rds.ui.activitySaleTurnOverCard.refreshAward()
        gameglobal.rds.ui.turnOverCardAward.refreshInfo()

    def onReceiveRandomTurnOverCardTotalReward(self, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe7\xbf\xbb\xe7\x89\x8c\xe7\xb4\xaf\xe8\xae\xa1\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        gamelog.info('@zmm onReceiveRandomTurnOverCardTotalReward', ret)
        if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED_BY_INV_FULL, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.SHOP_BAG_LOCKED, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL_BY_ALREADY_RECEIVED:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED_BY_ALREADY_RECEIVED, ())
        else:
            if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_SUC:
                gameglobal.rds.ui.activitySaleTurnOverCard.refreshAward()
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_SUCCESS, ())
                return
            if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL:
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED, ())
                return

    def onGetFinishTurnOverRewardMargins(self, finishRewardMargins):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe7\xbf\xbb\xe7\x89\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xb4\xaf\xe8\xae\xa1\xe6\x8a\xbd\xe5\xa5\x96\xe6\x95\xb0\xe6\x8d\xae\xe5\x87\xbd\xe6\x95\xb0
        :param finishRewardMargins: \xe5\xaf\xb9\xe5\xba\x94\xe5\xb7\xb2\xe9\xa2\x86\xe5\xa5\x96\xe7\x9a\x84\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\xa3\xe4\xbd\x8d\xe5\x92\x8c\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xa1\xa3\xe4\xbd\x8d\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        gamelog.debug('@zmm onGetFinishTurnOverRewardMargins', finishRewardMargins)
        self.randomTurnOverCardInfo['finishRewardMargins'] = finishRewardMargins
        gamelog.debug('@zmm onGetFinishRewardMargins', finishRewardMargins)

    def onRandomTurnOverCardRequest(self, ret, posInfo):
        """
        \xe9\x9a\x8f\xe6\x9c\xba\xe7\xbf\xbb\xe7\x89\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:0 \xe8\xa1\xa8\xe7\xa4\xba\xe7\xbf\xbb\xe7\x89\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c \xe9\x9d\x9e0 \xe8\xa1\xa8\xe7\xa4\xba\xe7\xbf\xbb\xe7\x89\x8c\xe5\xa4\xb1\xe8\xb4\xa5
        :param posInfo: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8cposInfo={pos1:{itemId1\xef\xbc\x8citemNum1}, pos2:{itemId2\xef\xbc\x8citemNum2}}
                      \xe5\xa6\x82\xe6\x9e\x9cret != 0, posInfo={}
        :return:
        """
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        gamelog.info('@zmm onRandomTurnOverCardRequest', ret, posInfo)
        if ret == gametypes.RANDOM_TURN_OVER_CARD_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_FAILED_BY_INVALID_TIME, ())
        if ret == gametypes.RANDOM_TURN_OVER_CARD_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_REWARD_BY_MAIL_WHILE_INV_LOCK, ())
        if ret == gametypes.RANDOM_TURN_OVER_CARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_REWARD_BY_MAIL_WHILE_INV_FULL, ())
        elif ret == gametypes.RANDOM_TURN_OVER_CARD_BY_CONSUME_ITEM_NOT_ENOUGH:
            self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_FAILED_BY_CONSUME_ITEM_NOT_ENOUGH, ())
            consumeItemIds = data.get('consumeItemIds', (411416,))
            consumeItemTotalNum = 0
            for itemId in consumeItemIds:
                itemNum = self.inv.countItemInPages(itemId)
                consumeItemTotalNum += itemNum

            if consumeItemTotalNum:
                gameglobal.rds.ui.activitySaleTurnOverCard.refreshCardCounter(consumeItemTotalNum)
        else:
            if ret == gametypes.RANDOM_TURN_OVER_CARD_SUC:
                gameglobal.rds.ui.activitySaleTurnOverCard.onRandomTurnOverCardRequest(posInfo)
                self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_SUCCESS, ())
                return
            if ret == gametypes.RANDOM_TURN_OVER_CARD_FAIL_NO_ENOUGH_CARD:
                self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_FAILED_BY_NO_ENOUGH_CARD, ())
                gameglobal.rds.ui.activitySaleTurnOverCard.refreshCardCounter()
                randomTurnOverPosInfo = self.randomTurnOverCardInfo.get('randomTurnOverPosInfo', {})
                turnOverCount = len(randomTurnOverPosInfo)
                if turnOverCount == 50:
                    gameglobal.rds.ui.activitySaleTurnOverCard.handleClickRefreshBtn()
            elif ret == gametypes.RANDOM_TURN_OVER_CARD_FAIL:
                self.showGameMsg(GMDD.data.RANDOM_TURN_OVER_CARD_FAILED, ())
                return
