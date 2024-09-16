#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impBindingProperty.o
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from cdata import game_msg_def_data as GMDD
from data import binding_property_data as BPD

class ImpBindingProperty(object):

    def onReceiveEkeyReward(self, result):
        p = BigWorld.player()
        if result == gametypes.EKEY_REWARD_REC_SUC:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_SUC, ())
            gameglobal.rds.ui.userAccountBind.updateEKeyBindInfo()
            gameglobal.rds.ui.accountBind.refreshEKeyBind()
        elif result == gametypes.EKEY_REWARD_REC_FAIL_BY_INV_LOCK:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_INV_LOCK, ())
        elif result == gametypes.EKEY_REWARD_REC_FAIL_BY_INV_FULL:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_INV_FULL, ())
        elif result == gametypes.EKEY_REWARD_REC_FAIL_BY_LV_LIMIT:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_LV_LIMIT, ())
        elif result == gametypes.EKEY_REWARD_REC_FAIL_BY_NO_OTP:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_NO_OTP, ())

    def onReceivePhoneBindReward(self, result):
        p = BigWorld.player()
        if result == gametypes.PHONE_BIND_REWARD_REC_SUC:
            p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_SUC, ())
            gameglobal.rds.ui.userAccountBind.updatePhoneBindInfo()
            gameglobal.rds.ui.accountBind.refreshPhoneBind()
        elif result == gametypes.PHONE_BIND_REWARD_REC_FAIL_BY_INV_LOCK:
            p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_FAIL_BY_INV_LOCK, ())
        elif result == gametypes.PHONE_BIND_REWARD_REC_FAIL_BY_INV_FULL:
            p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_FAIL_BY_INV_FULL, ())
        elif result == gametypes.PHONE_BIND_REWARD_REC_FAIL_BY_LV_LIMIT:
            p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_FAIL_BY_LV_LIMIT, ())

    def onBindPhoneByVerifyCode(self, result):
        p = BigWorld.player()
        if result == gametypes.PHONE_BIND_REC_SUC:
            p.showGameMsg(GMDD.data.PHONE_BIND_REC_SUC, ())
        elif result == gametypes.PHONE_BIND_REC_FAIL_BY_CD:
            p.showGameMsg(GMDD.data.PHONE_BIND_REC_FAIL_BY_CD, ())
        elif result == gametypes.PHONE_BIND_REC_FAIL_BY_NUM_NOT_MATCH:
            p.showGameMsg(GMDD.data.PHONE_BIND_REC_FAIL_BY_NUM_NOT_MATCH, ())
        elif result == gametypes.PHONE_BIND_REC_FAIL_BY_CODE_NOT_MATCH:
            p.showGameMsg(GMDD.data.PHONE_BIND_REC_FAIL_BY_CODE_NOT_MATCH, ())
        elif result == gametypes.PHONE_BIND_REC_FAIL_BY_NO_VERIFY:
            p.showGameMsg(GMDD.data.PHONE_BIND_REC_FAIL_BY_NO_VERIFY, ())

    def onReceiveCipherBindReward(self, result):
        p = BigWorld.player()
        if result == gametypes.CIPHER_REWARD_REC_SUC:
            p.showGameMsg(GMDD.data.CIPHER_REWARD_REC_SUC, ())
            gameglobal.rds.ui.userAccountBind.refreshPasswordPanel()
            gameglobal.rds.ui.accountBind.refreshPassword()
            gameglobal.rds.ui.accountBind.refreshLevel()
        elif result == gametypes.CIPHER_REWARD_REC_FAIL_BY_NO_OTP:
            p.showGameMsg(GMDD.data.CIPHER_REWARD_REC_FAIL_BY_NO_OTP, ())
        elif result == gametypes.CIPHER_REWARD_REC_FAIL_BY_INV_LOCK:
            p.showGameMsg(GMDD.data.CIPHER_REWARD_REC_FAIL_BY_INV_LOCK, ())
        elif result == gametypes.CIPHER_REWARD_REC_FAIL_BY_INV_FULL:
            p.showGameMsg(GMDD.data.CIPHER_REWARD_REC_FAIL_BY_INV_FULL, ())
        elif result == gametypes.CIPHER_REWARD_REC_FAIL_BY_LV_LIMIT:
            p.showGameMsg(GMDD.data.CIPHER_REWARD_REC_FAIL_BY_LV_LIMIT, ())

    def pushBindingMsg(self):
        pass

    def clickOpenBindPage(self):
        if gameglobal.rds.configData.get('enableBindReward', False):
            gameglobal.rds.ui.accountBind.show()
        else:
            gameglobal.rds.ui.userAccountBind.show()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_ACCOUNT_BIND)
