#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impOpenServerBonus.o
import BigWorld
import const
import utils
import gameglobal
from commOpenServerBonus import OpenServerBonusVal, OpenServerBonus
from cdata import game_msg_def_data as GMDD
from cdata import open_server_bonus_vp_data as OSBVD
from data import new_server_activity_data as NSAD

class ImpOpenServerBonus(object):

    def _isOpenServerBonusEnabled(self):
        if not gameglobal.rds.configData.get('enableOpenServerBonus', False):
            return
        days = utils.getServerOpenDays() + 1
        openServerBonusDayLimit = NSAD.data.get('openServerBonusDayLimit', 40)
        if days > openServerBonusDayLimit:
            return
        return days

    def onSendOpenServerBonus(self, data):
        self.openServerBonus = OpenServerBonus()
        days = utils.getServerOpenDays() + 1
        for dto in data:
            val = OpenServerBonusVal().fromDTO(dto)
            if val.day > days:
                continue
            self.openServerBonus[val.day] = val

        self.openServerBonus.recalcTEnd()
        self._checkReadyPushMsg()
        self._checkOpenServerBonus()

    def onAddOpenServerBonus(self, dto):
        val = OpenServerBonusVal().fromDTO(dto)
        self.openServerBonus[val.day] = val
        self.openServerBonus.recalcTEnd()
        self._checkOpenServerBonus()

    def onGainOpenServerBonus(self, day):
        openServerBonus = self.openServerBonus.get(day)
        if not openServerBonus:
            return
        openServerBonus.tPass = const.OPEN_SERVER_READY_TIME
        openServerBonus.state = const.OPEN_SERVER_BONUS_STATE_REWARDED
        self._checkOpenServerBonus()
        self.showGameMsg(GMDD.data.OPEN_SERVER_BONUS_GAIN, (day,))
        gameglobal.rds.ui.newServiceWelfare.updateNewServiceWelfare()
        key = (day, openServerBonus.vpLv)
        if OSBVD.data.has_key(key):
            gameglobal.rds.ui.roleInfo.show(subPanel='vp')

    def onRefreshOpenServerBonusDaily(self):
        self.openServerBonus.lastTime = utils.getNow()

    def _checkOpenServerBonus(self):
        if not self._isOpenServerBonusEnabled():
            return
        elif not self.inWorld:
            return
        elif not self.openServerBonus:
            return
        else:
            openServerBonusCheckCallback = getattr(self, 'openServerBonusCheckCallback', None)
            if openServerBonusCheckCallback:
                BigWorld.cancelCallback(openServerBonusCheckCallback)
                self.openServerBonusCheckCallback = 0
            minTimeLeft, day = self.openServerBonus.getMinLeftTime(self)
            for openServerBonus in self.openServerBonus.itervalues():
                if openServerBonus.state == const.OPEN_SERVER_BONUS_STATE_READY:
                    gameglobal.rds.ui.newServiceWelfare.updateNewServiceWelfare()

            if minTimeLeft > 0:
                self.openServerBonusCheckCallback = BigWorld.callback(minTimeLeft, self._checkOpenServerBonus)
            return

    def _checkReadyPushMsg(self):
        enableNewServerSignInPanel = gameglobal.rds.configData.get('enableNewServerSignInPanel', False)
        for openServerBonus in self.openServerBonus.itervalues():
            if openServerBonus.state == const.OPEN_SERVER_BONUS_STATE_READY:
                if enableNewServerSignInPanel:
                    gameglobal.rds.ui.newServiceWelfare.updateNewServiceWelfare()
