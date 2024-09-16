#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCBG.o
import BigWorld
import cPickle
import gameglobal
import zlib
import gamelog
import const
from guis import events
from helpers.eventDispatcher import Event
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
import gamelog

class ImpCBG(object):

    def updateOwnCBG(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = {}

        evt = Event(events.EVENT_UPDATE_OWN_CBG_DATA, data)
        gameglobal.rds.ui.dispatchEvent(evt)

    def removeOwnCBG(self, cbgId):
        evt = Event(events.EVENT_REMOVE_OWN_CBG_DATA, {'cbgId': cbgId})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateCBGBought(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = {}

        evt = Event(events.EVENT_UPDATE_BOUGHT_CBG_DATA, data)
        gameglobal.rds.ui.dispatchEvent(evt)

    def removeCBGBought(self, cbgId):
        evt = Event(events.EVENT_REMOVE_BOUGHT_CBG_DATA, {'cbgId': cbgId})
        gameglobal.rds.ui.dispatchEvent(evt)

    def fastCbgLogon(self, data):
        self.autoLoginUrl = data
        self.base.exchangeTicketByCookie()

    def onSellCashInCbg(self, succ):
        if not succ:
            return
        gameglobal.rds.ui.dispatchEvent(events.EVENT_SELL_CASH_DONE)

    def onQueryAllCbgData(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = {}

        evt = Event(events.EVENT_UPDATE_QUERY_ALL_DATA, data)
        gameglobal.rds.ui.dispatchEvent(evt)

    def takeBackCBGCashFailed(self, stat):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TAKE_BACK_FAILED)

    def onGetRoleSaleData(self, data):
        """
        \xe5\x90\x8c\xe6\xad\xa5p.roleSaleData\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x8c\xe8\xa7\x81roleSaleData.py
        :param data: 
        """
        gamelog.debug('ypc@ onGetRoleSaleData ', data)
        self.roleSaleData = data

    def onApplyRegisterSaleRole(self, isOk, conditions):
        """
        \xe7\x99\xbb\xe8\xae\xb0\xe8\xa7\x92\xe8\x89\xb2\xe5\x87\xba\xe5\x94\xae
        :param isOk: \xe6\x98\xaf\xe5\x90\xa6\xe7\x99\xbb\xe8\xae\xb0\xe6\x88\x90\xe5\x8a\x9f
        :param conditions: \xe5\xa6\x82\xe6\x9e\x9c\xe5\xa4\xb1\xe8\xb4\xa5\xe4\xbc\x9a\xe8\xbf\x94\xe5\x9b\x9e\xe5\x8e\x9f\xe5\x9b\xa0\xe5\xad\x97\xe5\x85\xb8\xef\xbc\x9b\xe6\x88\x90ui_\xe5\x8a\x9f\xe6\x97\xb6\xe4\xb8\xba{}
        """
        gamelog.debug('ypc@ onApplyRegisterSaleRole!', isOk, conditions)
        evt = Event(events.EVENT_CBG_ROLE_REGIST, {'isOk': isOk,
         'conditions': conditions})
        gameglobal.rds.ui.dispatchEvent(evt)

    def onApplyUnRegisterSaleRole(self, isOk):
        """
        \xe5\x8f\x96\xe6\xb6\x88\xe7\x99\xbb\xe8\xae\xb0\xe8\xa7\x92\xe8\x89\xb2\xe5\x87\xba\xe5\x94\xae
        :param isOk: \xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\x96\xe6\xb6\x88\xe7\x99\xbb\xe8\xae\xb0\xe6\x88\x90\xe5\x8a\x9f 
        """
        gamelog.debug('ypc@ onApplyUnRegisterSaleRole!', isOk)
        evt = Event(events.EVENT_CBG_ROLE_UNREGIST_SALE, isOk)
        gameglobal.rds.ui.dispatchEvent(evt)

    def onApplySaleRole(self, isOk, conditions):
        """
        \xe8\xa7\x92\xe8\x89\xb2\xe4\xb8\x8a\xe6\x9e\xb6\xe5\x9b\x9e\xe8\xb0\x83
        :param isOk: 
        :param conditions: \xe5\xa6\x82\xe6\x9e\x9c\xe5\xa4\xb1\xe8\xb4\xa5\xe4\xbc\x9a\xe8\xbf\x94\xe5\x9b\x9e\xe5\x8e\x9f\xe5\x9b\xa0\xe5\xad\x97\xe5\x85\xb8\xef\xbc\x9b\xe6\x88\x90\xe5\x8a\x9f\xe6\x97\xb6\xe4\xb8\xba{}
        """
        gamelog.debug('ypc@ onApplySaleRole!', isOk, conditions)
        evt = Event(events.EVENT_CBG_ROLE_SALE, {'isOk': isOk,
         'conditions': conditions})
        gameglobal.rds.ui.dispatchEvent(evt)

    def onSendRoleToCbgFail(self, cause):
        """
        \xe5\x90\x91\xe8\x97\x8f\xe5\xae\x9d\xe9\x98\x81\xe5\x8f\x91\xe9\x80\x81\xe6\x95\xb0\xe6\x8d\xae\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe8\xb0\x83\xe7\x94\xa8applySaleRole\xe4\xb9\x8b\xe5\x90\x8e\xe7\x9a\x84\xe5\xa4\xb1\xe8\xb4\xa5\xe9\x83\xbd\xe4\xbc\x9a\xe8\xb0\x83\xe7\x94\xa8\xe8\xbf\x99\xe4\xb8\xaa
        :return: 
        """
        gamelog.debug('ypc@ onSendRoleToCbgFail!')
        self.onCbgRoleFinishSelling()
        if cause == const.CBG_PUT_ON_SALE_FAIL_TYPE_SEND:
            self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.CBG_ROLE_SALE_FAILED)
        elif cause == const.CBG_PUT_ON_SALE_FAIL_TYPE_COIN:
            self.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
        gameglobal.rds.ui.cbgMain.closeWaitingMsg()

    def onQueryRegisterSaleRoleConditions(self, conditions):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe7\x99\xbb\xe8\xae\xb0\xe6\x9d\xa1\xe4\xbb\xb6
        :param conditions: 
        """
        gamelog.debug('ypc@ onQueryRegisterSaleRoleConditions!', conditions)
        gameglobal.rds.ui.cbgMain.onQueryRegisterConditions(conditions)

    def onQuerySaleRoleConditions(self, conditions):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe4\xb8\x8a\xe6\x9e\xb6\xe6\x9d\xa1\xe4\xbb\xb6
        :param conditions: 
        """
        gamelog.debug('ypc@ onQuerySaleRoleConditionsonQuerySaleRoleConditions!', conditions)
        gameglobal.rds.ui.cbgMain.onQuerySellConditions(conditions)
