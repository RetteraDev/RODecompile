#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/userAccountBindProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
import utils
from callbackHelper import Functor
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import binding_property_data as BPD

class UserAccountBindProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UserAccountBindProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPhoneBindInfo': self.onGetPhoneBindInfo,
         'getEKeyBindInfo': self.onGetEKeyBindInfo,
         'getBindYZM': self.onGetBindYZM,
         'getReward': self.onGetUserBindReward,
         'verifyUserPhone': self.onVerifyUserPhone,
         'openEKeyWeb': self.onOpenEKeyWeb,
         'getVerifyTime': self.onGetVerifyTime,
         'getPasswordInfo': self.onGetPasswordInfo,
         'setPassword': self.onSetUserPassword,
         'resetPassword': self.onResetPassword,
         'clearPassword': self.onClearUserPassword,
         'getLevel': self.onGetLevel,
         'getPasswordReward': self.onGetPasswordReward}
        self.mediator = None
        self.timer = 0
        self.timerId = 0
        self.qrContent = 'http://mkey.163.com/'
        uiAdapter.registerEscFunc(uiConst.WIDGET_USER_ACCOUNT_BIND, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_USER_ACCOUNT_BIND:
            self.mediator = mediator
        self.refreshEkeyLoading()

    def show(self):
        if gameglobal.rds.configData.get('enableBindReward', False):
            gameglobal.rds.ui.accountBind.show()
        elif gameglobal.rds.configData.get('enableBindingProperty', True):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_USER_ACCOUNT_BIND)
            self.updateTimer()
        else:
            BigWorld.player().showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NOT_OPEN, ())

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.onDefaultState()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_USER_ACCOUNT_BIND)

    def onGetLevel(self, *arg):
        level = self._getLevel()
        return GfxValue(level)

    def _getLevel(self):
        level = 0
        p = BigWorld.player()
        if p.bindPhoneNum:
            level += 1
        if p.securityTypeOfCell in const.SECURITY_TYPE_EKEY:
            level += 1
        if p.hasInvPassword:
            level += 1
        return level

    def onGetPhoneBindInfo(self, *arg):
        ret = self._getPhoneBindData()
        return uiUtils.dict2GfxDict(ret, True)

    def updatePhoneBindInfo(self):
        ret = self._getPhoneBindData()
        if self.mediator:
            self.mediator.Invoke('updatePhoneBindPanel', uiUtils.dict2GfxDict(ret, True))

    def _getPhoneBindData(self):
        ret = {}
        p = BigWorld.player()
        ret['hasPhoneBinding'] = p.hasPhoneBinding
        ret['hasPhoneRewardReceived'] = p.hasPhoneRewardReceived
        ret['bindPhoneNum'] = p.bindPhoneNum
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('PhoneBindingDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_FREQUENCY, gameStrings.TEXT_USERACCOUNTBINDPROXY_96)
        if not p.hasPhoneBinding:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_NEED_BIND, gameStrings.TEXT_USERACCOUNTBINDPROXY_99)
        elif p.hasPhoneRewardReceived:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_GOT, gameStrings.TEXT_USERACCOUNTBINDPROXY_102)
        else:
            ret['tip'] = ''
        ret['timer'] = self.timer
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_DESC, gameStrings.TEXT_USERACCOUNTBINDPROXY_107)
        ret['itemDetial'] = BPD.data.get('PhoneBonusDetail', gameStrings.TEXT_USERACCOUNTBINDPROXY_108)
        return ret

    def onGetEKeyBindInfo(self, *arg):
        ret = self._getEkeyBindInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def updateEKeyBindInfo(self):
        ret = self._getEkeyBindInfo()
        if self.mediator:
            self.mediator.Invoke('updateEKeyBindPanel', uiUtils.dict2GfxDict(ret, True))

    def _getEkeyBindInfo(self):
        p = BigWorld.player()
        ret = {}
        ret['hasEkeyRewardReceived'] = p.hasEkeyRewardReceived
        hasBindEkey = p.securityTypeOfCell in const.SECURITY_TYPE_EKEY
        ret['hasBindEkey'] = hasBindEkey
        ret['tipText'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BINDED, gameStrings.TEXT_USERACCOUNTBINDPROXY_127) if hasBindEkey else uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_UNBINDED, gameStrings.TEXT_USERACCOUNTBINDPROXY_127_1)
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('EKeyDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_FREQUENCY, gameStrings.TEXT_USERACCOUNTBINDPROXY_129)
        if not hasBindEkey:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_NEED_BIND, gameStrings.TEXT_USERACCOUNTBINDPROXY_132)
        elif p.hasEkeyRewardReceived:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_GOT, gameStrings.TEXT_USERACCOUNTBINDPROXY_135)
        else:
            ret['tip'] = ''
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_DESC, gameStrings.TEXT_USERACCOUNTBINDPROXY_139)
        ret['itemDetial'] = BPD.data.get('EKeyBonusDetail', gameStrings.TEXT_USERACCOUNTBINDPROXY_108)
        return ret

    def onGetBindYZM(self, *arg):
        phoneNum = arg[3][0].GetString()
        p = BigWorld.player()
        if phoneNum == '':
            p.showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NONE_PHONE_NUMBER, ())
            return
        if not utils.isValidPhoneNum(phoneNum):
            p.showGameMsg(GMDD.data.INVALID_PHONE_NUM, phoneNum)
            return
        p.base.requestBindPhoneVerifyCode(phoneNum)
        self.timer = BPD.data.get('verifyTime', 60)
        self.timerId = BigWorld.callback(1.0, self.updateTimer)

    def onGetUserBindReward(self, *arg):
        key = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        playerLv = p.lv
        if key == 0:
            limitLv = BPD.data.get('EkeyLimitLv', 20)
            if playerLv < limitLv:
                p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_LV_LIMIT, ())
            else:
                p.cell.receiveEkeyReward()
        elif key == 1:
            limitLv = BPD.data.get('PhoneBindLimitLv', 30)
            if playerLv < limitLv:
                p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_FAIL_BY_LV_LIMIT, ())
            else:
                p.cell.receivePhoneBindReward()

    def onVerifyUserPhone(self, *arg):
        phoneNum = arg[3][0].GetString()
        verifyCode = arg[3][1].GetString()
        p = BigWorld.player()
        temp = phoneNum
        if phoneNum.find('-'):
            temp = phoneNum[phoneNum.index('-') + 1:len(phoneNum)]
        if temp == '':
            p.showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NONE_PHONE_NUMBER, ())
            return
        if verifyCode == '':
            p.showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NONE_VERIFY_CODE, ())
            return
        if utils.isValidPhoneNum(phoneNum):
            p.base.bindPhoneByVerifyCode(phoneNum, verifyCode)
        else:
            p.showGameMsg(GMDD.data.INVALID_PHONE_NUM, phoneNum)

    def onOpenEKeyWeb(self, *arg):
        BigWorld.openUrl('http://reg.163.com/mibao/controller/goIndex.jsp')
        msg = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_OPEN_EKEY_PAGE_TIP, gameStrings.TEXT_USERACCOUNTBINDPROXY_199)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.bindEkeySuc), yesBtnText=gameStrings.TEXT_USERACCOUNTBINDPROXY_200, noBtnText=gameStrings.TEXT_ACCOUNT_452_1)

    def bindEkeySuc(self):
        self.updateEKeyBindInfo()

    def onGetVerifyTime(self, *arg):
        verifyTime = BPD.data.get('verifyTime', 60)
        return GfxValue(verifyTime)

    def updateTimer(self):
        self.updateYZMBtnState()
        if self.timer > 0:
            self.timer -= 1
            self.timerId = BigWorld.callback(1.0, self.updateTimer)
        else:
            BigWorld.cancelCallback(self.timerId)

    def updateYZMBtnState(self):
        if self.mediator:
            msg = gameStrings.TEXT_NEWRECHARGEPROXY_136
            enable = True
            if self.timer > 0:
                msg = gameStrings.TEXT_USERACCOUNTBINDPROXY_222 % self.timer
                enable = False
            self.mediator.Invoke('updateYZMBtnState', (GfxValue(gbk2unicode(msg)), GfxValue(enable)))

    def refreshEkeyLoading(self):
        if self.mediator:
            if not self.qrContent:
                self.mediator.Invoke('setIsLoading', GfxValue(True))
            else:
                self.mediator.Invoke('setIsLoading', GfxValue(False))
                buffer = uiUtils.getQRCodeBuff(self.qrContent)
                self.mediator.Invoke('setQRCode', GfxValue(buffer))

    def onGetPasswordInfo(self, *arg):
        ret = self._getPasswordInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def _getPasswordInfo(self):
        ret = {}
        p = BigWorld.player()
        ret['hasPassword'] = p.hasInvPassword
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PASSWORD_DESC, gameStrings.TEXT_USERACCOUNTBINDPROXY_245)
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('PasswordDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PASSWORD_BIND_REWARD_FREQUENCY, gameStrings.TEXT_USERACCOUNTBINDPROXY_247)
        ret['itemDetial'] = BPD.data.get('PasswordBonusDetail', gameStrings.TEXT_USERACCOUNTBINDPROXY_108)
        ret['hasCipherRewardReceived'] = p.hasCipherRewardReceived
        return ret

    def onSetUserPassword(self, *arg):
        password = arg[3][0].GetString()
        passwordConfirm = arg[3][1].GetString()
        if not password:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())
            return
        if password != passwordConfirm:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INCONSISTENT_PASSWORD, ())
            return
        BigWorld.player().cell.modifyCipher('', password)

    def onResetPassword(self, *arg):
        old = arg[3][0].GetString()
        new1 = arg[3][1].GetString()
        new2 = arg[3][2].GetString()
        if not old:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())
            return
        if not new1:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())
            return
        if new1 != new2:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INCONSISTENT_PASSWORD, ())
            return
        BigWorld.player().cell.modifyCipher(old, new1)

    def onClearUserPassword(self, *arg):
        selectType = int(arg[3][0].GetNumber())
        if selectType == 0:
            oldPassword = arg[3][1].GetString()
            if not oldPassword:
                return
            BigWorld.player().cell.modifyCipher(oldPassword, '')
        else:
            p = BigWorld.player()
            p.base.resetCipher()
            if p.cipherResetTime > 0:
                p.showTopMsg(gameStrings.TEXT_CLEARPASSWORDPROXY_58)

    def refreshPasswordPanel(self):
        BigWorld.callback(0.5, self.realRefreshPasswordPanel)

    def realRefreshPasswordPanel(self):
        if self.mediator:
            ret = self._getPasswordInfo()
            self.mediator.Invoke('updatePasswordPanel', uiUtils.dict2GfxDict(ret, True))
            self.refreshAccountLevel()

    def onGetPasswordReward(self, *arg):
        BigWorld.player().cell.receiveCipherReward()

    def refreshAccountLevel(self):
        if self.mediator:
            level = self._getLevel()
            self.mediator.Invoke('updateLevel', GfxValue(level))
