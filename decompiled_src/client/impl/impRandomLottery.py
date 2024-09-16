#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRandomLottery.o
from gamestrings import gameStrings
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

class ImpRandomLottery(object):

    def onSyncRandomLotteryActivity(self):
        """
        \xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe6\xb4\xbb\xe5\x8a\xa8\xe6\xaf\x8f\xe6\x97\xa5\xe7\xac\xac\xe4\xb8\x80\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x8e\xa8\xe9\x80\x81\xe5\x87\xbd\xe6\x95\xb0
        :return:
        """
        gameglobal.rds.ui.activitySaleLottery.pushLotteryMessage()

    def onRandomLotterySelectionRequest(self, ret, randomLotteryItems):
        """
        \xe5\xa5\x96\xe6\xb1\xa0\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :param randomLotteryItems: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8crandomLotteryItems={\xe5\xa5\x96\xe6\xb1\xa0\xe7\x89\xa9\xe5\x93\x81, \xe6\x95\xb0\xe6\x8d\xae\xe4\xb8\xba {\xe5\xa5\x96\xe6\xb1\xa0groupId1\xef\xbc\x9a[itemId1, itemId2],\xe5\xa5\x96\xe6\xb1\xa0groupId2\xef\xbc\x9a[itemId3, itemId4],...,\xe5\xa5\x96\xe6\xb1\xa0groupId5\xef\xbc\x9a[itemId8],}
                                   \xe5\xa6\x82\xe6\x9e\x9cret != 0, randomLotteryItems={}
        :return:
        """
        gamelog.info('@zmm onRandomLotterySelectionRequest', ret, randomLotteryItems)
        if ret == gametypes.RANDOM_LOTTERY_SELECT_SUC:
            self.randomLotteryInfo['randomLotteryItems'] = randomLotteryItems
            gameglobal.rds.ui.activitySaleLottery.onRandomLotterySelectionRequest()
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_SELECTION_SUCCESS, ())
        elif ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_SELECTION_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_ITEM_NOT_MATCH:
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_SELECTION_FAILED_BY_ITEM_NOT_MATCH, ())

    def onRandomLotteryDrawRequest(self, ret, items):
        """
        \xe9\x9a\x8f\xe6\x9c\xba\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x961\xe6\xac\xa1/10\xe6\xac\xa1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:0 \xe8\xa1\xa8\xe7\xa4\xba\xe6\x8a\xbd\xe5\xa5\x96\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c \xe9\x9d\x9e0 \xe8\xa1\xa8\xe7\xa4\xba\xe6\x8a\xbd\xe5\xa5\x96\xe5\xa4\xb1\xe8\xb4\xa5
        :param items: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8citems={groupId1:[itemId1, itemId2,], groupId2:[itemId3, itemId2,]}
                      \xe5\xa6\x82\xe6\x9e\x9cret != 0, items={}
        :return:
        """
        gamelog.info('@zmm onRandomLotteryDrawRequest', ret, items)
        if ret == gametypes.RANDOM_LOTTERY_SELECT_FAIL_BY_TIME_INVALID:
            gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_SELECTION_FAILED_BY_INVALID_TIME, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_FAIL_BY_INV_FULL:
            gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_FAILED_BY_INV_FULL, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_FAIL_BY_INV_LOCK:
            gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.RANDOM_LOTTERY_DRAW_FAIL_BY_CONSUME_ITEM_NOT_ENOUGH:
            gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
            gameglobal.rds.ui.activitySaleLottery.remindAgain = True
            self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_FAILED_BY_CONSUME_ITEM_NOT_ENOUGH, ())
        else:
            if ret == gametypes.RANDOM_LOTTERY_DRAW_SUC:
                gameglobal.rds.ui.activitySaleLottery.onRandomLotteryDrawRequest(items)
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_SUCCESS, ())
                return
            if ret == gametypes.RANDOM_LOTTERY_DRAW_FAIL:
                gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_FAILED, ())
                return

    def confirmRandomLotteryDrawByCoins(self, countType):
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        consumeCoins = data.get('consumeCoins', 0) * countType
        msg = uiUtils.getTextFromGMD(GMDD.data.RANDOM_LOTTERY_DRAW_BY_COINS, '') % consumeCoins
        if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_RANDOM_LOTTERY, False):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doConfirmRandomLotteryDrawByCoins, countType), yesBtnText=gameStrings.TEXT_MIXFAMEJEWELRYPROXY_200, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_RANDOM_LOTTERY, noCallback=self._doCancelRandomLotteryDrawByCoins)
        else:
            self._doConfirmRandomLotteryDrawByCoins(countType)

    def _doConfirmRandomLotteryDrawByCoins(self, countType):
        self.cell.randomLotteryDrawByCoinsRequest(countType)

    def _doCancelRandomLotteryDrawByCoins(self):
        gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(True)
        self.cell.randomLotteryPutTempBagFailed()

    def onReceiveRandomLotteryDrawTotalReward(self, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe7\xb4\xaf\xe8\xae\xa1\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        gamelog.info('@zmm onReceiveRandomLotteryDrawTotalReward', ret)
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
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_SUCCESS, ())
                return
            if ret == gametypes.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAIL:
                self.showGameMsg(GMDD.data.RANDOM_LOTTERY_DRAW_TOTAL_REWARD_FAILED, ())
                return

    def onGetTotalLotteryCount(self, totalLotteryCount):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe8\x87\xaa\xe9\x80\x89\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param totalLotteryCount: \xe8\x87\xaa\xe9\x80\x89\xe5\xa5\x96\xe6\xb1\xa0\xe6\x8a\xbd\xe5\xa5\x96\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c
        :return:
        """
        gamelog.debug('@zmm onGetTotalLotteryCount', totalLotteryCount)
        self.randomLotteryInfo['totalLotteryCount'] = totalLotteryCount
        gameglobal.rds.ui.activitySaleLottery.refreshLotteryPanel()

    def onGetFinishRewardMargins(self, finishRewardMargins):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe8\x87\xaa\xe9\x80\x89\xe5\xa5\x96\xe6\xb1\xa0\xe7\xb4\xaf\xe8\xae\xa1\xe6\x8a\xbd\xe5\xa5\x96\xe6\x95\xb0\xe6\x8d\xae\xe5\x87\xbd\xe6\x95\xb0
        :param finishRewardMargins: \xe5\xaf\xb9\xe5\xba\x94\xe5\xb7\xb2\xe9\xa2\x86\xe5\xa5\x96\xe7\x9a\x84\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\xa3\xe4\xbd\x8d\xe5\x92\x8c\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xa1\xa3\xe4\xbd\x8d\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        gamelog.debug('@zmm onGetFinishRewardMargins', finishRewardMargins)
        self.randomLotteryInfo['finishRewardMargins'] = finishRewardMargins
        gamelog.debug('@zmm onGetFinishRewardMargins', finishRewardMargins)
        gameglobal.rds.ui.activitySaleLottery.refreshLotteryPanel()
