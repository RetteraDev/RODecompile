#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRandomCardDraw.o
import gamelog
import gametypes
import gameglobal
from guis import uiConst
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import random_card_draw_data as RCDD
MAX_CHOOSE_NUM = 8

class ImpRandomCardDraw(object):

    def onSyncRandomCardDrawActivity(self):
        """
        \xe5\x8d\xa1\xe7\x89\x8c\xe6\x8a\xbd\xe5\xa5\x96\xe6\xb4\xbb\xe5\x8a\xa8\xe6\xaf\x8f\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x8e\xa8\xe9\x80\x81\xe5\x87\xbd\xe6\x95\xb0
        :return:
        """
        gameglobal.rds.ui.activitySaleRandomCardDraw.pushRandomCardDrawMessage()
        gamelog.info('@zmm onSyncRandomCardDrawActivity')

    def onGetTotalCardDrawCount(self, activityId, totalCardDrawCount):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe4\xb8\xaa\xe5\x8d\xa1\xe7\x89\x8c\xe6\x8a\xbd\xe5\x8d\xa1\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x8a\xbd\xe5\x8d\xa1\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param activityId: \xe6\xb4\xbb\xe5\x8a\xa8id
        :param totalCardDrawCount: \xe6\x8a\xbd\xe5\x8d\xa1\xe6\xac\xa1\xe6\x95\xb0\xe6\x80\xbb\xe5\x92\x8c
        :return:
        """
        gamelog.debug('@zmm onGetTotalCardDrawCount', activityId, totalCardDrawCount)
        self.randomCardDrawInfo[activityId]['totalCardDrawCount'] = totalCardDrawCount

    def onReceiveRandomCardDrawTotalReward(self, activityId, ret):
        """
        \xe6\x9f\x90\xe4\xb8\xaa\xe5\x8d\xa1\xe7\x89\x8c\xe6\x8a\xbd\xe5\x8d\xa1\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xb4\xaf\xe8\xae\xa1\xe5\xa5\x96\xe5\x8a\xb1\xe5\x8f\x91\xe6\x94\xbe\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param activityId:
        :param ret:
        :return:
        """
        gamelog.info('@zmm onReceiveRandomCardDrawTotalReward', ret)
        if ret == gametypes.RANDOM_CARD_DRAW_TOTAL_REWARD_SUC:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_TOTAL_REWARD_BY_MAIL_SUCCESS, ())
            return

    def onGetFinishCardDrawRewardMargins(self, activityId, finishRewardMargins):
        """
        \xe6\xb4\xbb\xe5\x8a\xa8\xe7\xb4\xaf\xe8\xae\xa1\xe6\x8a\xbd\xe5\x8d\xa1\xe6\x95\xb0\xe6\x8d\xae\xe6\x9b\xb4\xe6\x96\xb0
        :param finishRewardMargins: \xe5\xaf\xb9\xe5\xba\x94\xe5\xb7\xb2\xe9\xa2\x86\xe5\xa5\x96\xe7\x9a\x84\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\xa3\xe4\xbd\x8d\xe5\x92\x8c\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xa1\xa3\xe4\xbd\x8d\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        gamelog.info('@zmm onGetFinishCardDrawRewardMargins', activityId, finishRewardMargins)
        self.randomCardDrawInfo[activityId]['finishRewardMargins'] = finishRewardMargins

    def onRandomCardDrawRequest(self, activityId, ret, posInfo):
        """
        \xe9\x9a\x8f\xe6\x9c\xba\xe6\x8a\xbd\xe5\x8d\xa1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:0 \xe8\xa1\xa8\xe7\xa4\xba\xe7\xbf\xbb\xe7\x89\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c \xe9\x9d\x9e0 \xe8\xa1\xa8\xe7\xa4\xba\xe7\xbf\xbb\xe7\x89\x8c\xe5\xa4\xb1\xe8\xb4\xa5
        :param posInfo: \xe5\xa6\x82\xe6\x9e\x9cret == 0\xef\xbc\x8cposInfo={pos1:{itemId1\xef\xbc\x8citemNum1}, pos2:{itemId2\xef\xbc\x8citemNum2}}
                      \xe5\xa6\x82\xe6\x9e\x9cret != 0, posInfo={}
        :return:
        """
        gamelog.info('@zmm onRandomCardDrawRequest', activityId, ret, posInfo)
        if ret == gametypes.RANDOM_CARD_DRAW_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_FAILED_BY_INVALID_TIME, ())
        if ret == gametypes.RANDOM_CARD_DRAW_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_REWARD_BY_MAIL_WHILE_INV_LOCK, ())
        if ret == gametypes.RANDOM_CARD_DRAW_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_REWARD_BY_MAIL_WHILE_INV_FULL, ())
        elif ret == gametypes.RANDOM_CARD_DRAW_BY_CONSUME_ITEM_NOT_ENOUGH:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_FAILED_BY_CONSUME_ITEM_NOT_ENOUGH, ())
        elif ret == gametypes.RANDOM_CARD_DRAW_SUC:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_SUCCESS, ())
            resultList = []
            for pos, info in posInfo.iteritems():
                if pos == 'fixedItems':
                    continue
                item = [ (x, y) for x, y in info.items() ]
                resultList.append(item[0])

            gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult = True
            gameglobal.rds.ui.randomCardDrawResult.show(activityId, resultList)
        elif ret == gametypes.RANDOM_CARD_DRAW_FAIL:
            self.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_FAILED, ())
            return
