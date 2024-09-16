#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/accountBindProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import ui
import const
import base64
import utils
import gametypes
import keys
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import ASObject
from callbackHelper import Functor
from guis.asObject import ASUtils
from appSetting import Obj as AppSettings
from data import binding_property_data as BPD
from data import push_data as PD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
WEIXING_BIND = 0
EKEY_BIND = 1
APP_BIND = 2
PHONT_BIND = 3
PASSWORD_BIND = 4
DEFAULT_ORDERS = [WEIXING_BIND,
 EKEY_BIND,
 APP_BIND,
 PHONT_BIND,
 PASSWORD_BIND]
KEY_FRAME_NAMES = ['weixin',
 'jiangjunling',
 'Appbangding',
 'shoujibangding',
 'tongyongmima']
EKEY_URL_PATH = 'http://mkey.163.com/'
WEIXIN_URL_PATH = 'http://weixin.qq.com/r/uHVAWHnEdCQLrT079yCq/'
APP_URL_PATH = 'http://tianyu.163.com/m/download/app/download.html'
BIND_STATUS = [gametypes.BIND_STATUS_SUCC, gametypes.BIND_STATUS_EXPIRED]
QUERY_INTERVAL = 60

class AccountBindProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AccountBindProxy, self).__init__(uiAdapter)
        self._resetData()
        self.uiAdapter.registerEscFunc(uiConst.WIDGET_ACCOUNT_BIND, self.hide)
        self.clickQueryTimeRecord = {}
        self.globalTimer = 0

    def _resetData(self):
        self.widget = None
        self.dataDic = {}
        self.mcRecord = {}
        self.qrContents = {}
        self.level = 0
        self.timer = 0
        self.timerId = 0
        self.jumpIndex = -1

    def _registerASWidget(self, widgetId, widget):
        self.delPushMsg()
        self.widget = widget
        self._initUI()
        self.refreshFrame()
        self.startGlobalTimer()

    def startGlobalTimer(self):
        if not self.widget:
            return
        if not self.widget.pageList:
            return
        self.updateWeiXinTimer()
        self.updateAppBindTimer()
        self.globalTimer = BigWorld.callback(1, self.startGlobalTimer)

    def updateWeiXinTimer(self):
        now = utils.getNow()
        widget = self.widget.pageList.canvas.getChildByName(str(WEIXING_BIND))
        lastClickTime = self.clickQueryTimeRecord.get(WEIXING_BIND, 0)
        pastTime = now - lastClickTime
        if widget:
            if widget.weiXinPanel.grayBtn:
                if now - lastClickTime < QUERY_INTERVAL:
                    widget.weiXinPanel.grayBtn.enabled = False
                    widget.weiXinPanel.grayBtn.label = '%s(%ds)' % (gameStrings.ACCOUNT_BIND_PROXY_STATUS_SEARCH, QUERY_INTERVAL - pastTime)
                else:
                    widget.weiXinPanel.grayBtn.enabled = True
                    widget.weiXinPanel.grayBtn.label = gameStrings.ACCOUNT_BIND_PROXY_STATUS_SEARCH

    def updateAppBindTimer(self):
        now = utils.getNow()
        widget = self.widget.pageList.canvas.getChildByName(str(APP_BIND))
        lastClickTime = self.clickQueryTimeRecord.get(APP_BIND, 0)
        pastTime = now - lastClickTime
        if widget:
            if widget.appPanel.grayBtn:
                if now - lastClickTime < QUERY_INTERVAL:
                    widget.appPanel.grayBtn.enabled = False
                    widget.appPanel.grayBtn.label = '%s(%ds)' % (gameStrings.ACCOUNT_BIND_PROXY_STATUS_SEARCH, QUERY_INTERVAL - pastTime)
                else:
                    widget.appPanel.grayBtn.enabled = True
                    widget.appPanel.grayBtn.label = gameStrings.ACCOUNT_BIND_PROXY_STATUS_SEARCH

    def show(self):
        if gameglobal.rds.configData.get('enableBindingProperty', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACCOUNT_BIND)
        else:
            BigWorld.player().showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NOT_OPEN, ())

    def clearWidget(self):
        BigWorld.cancelCallback(self.globalTimer)
        self.globalTimer = 0
        self._resetData()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACCOUNT_BIND)

    def getLevel(self, ignoreExpiredStatus = True):
        level = 0
        p = BigWorld.player()
        if p.bindPhoneNum:
            level += 1
        if p.securityTypeOfCell in const.SECURITY_TYPE_EKEY:
            level += 1
        if p.hasInvPassword:
            level += 1
        if p.appBindStatus in BIND_STATUS and (ignoreExpiredStatus or p.appBindStatus != gametypes.BIND_STATUS_EXPIRED):
            level += 1
        if p.weixinBindStatus in BIND_STATUS and (ignoreExpiredStatus or p.weixinBindStatus != gametypes.BIND_STATUS_EXPIRED):
            level += 1
        self.level = level
        return self.level

    def getWeiXinData(self):
        ret = {}
        p = BigWorld.player()
        ret['desc'] = BPD.data.get('WeiXinBindDesc', '')
        qrContent = self.qrContents.get(WEIXING_BIND, None)
        if not qrContent:
            qrContent = uiUtils.getQRCodeBuff(WEIXIN_URL_PATH)
        self.qrContents[EKEY_BIND] = qrContent
        ret['qrContent'] = qrContent
        ret['spriteKey'] = BPD.data.get('WeiXinSpriteKey', 0)
        ret['hasBindWeiXin'] = p.weixinBindStatus in BIND_STATUS
        ret['expired'] = p.weixinBindStatus == gametypes.BIND_STATUS_EXPIRED
        ret['itemTip'] = BPD.data.get('WeiXinItemTip', '')
        rewardItemId = BPD.data.get('WeiXinDisplayItemId', 0)
        ret['items'] = uiUtils.getGfxItemById(rewardItemId)
        ret['rewardDetail'] = BPD.data.get('WeiXinBindDetail', '')
        ret['WeiXinTips'] = BPD.data.get('WeiXinTips', '')
        ret['WeiXinExpiredTips'] = BPD.data.get('WeiXinExpiredTips', '')
        ret['hasReward'] = not p.weixinBindRewarded
        if self.jumpIndex < 0 and ret['hasBindWeiXin'] and ret['hasReward']:
            self.jumpIndex = WEIXING_BIND
        ret['receivedDesc'] = BPD.data.get('WeiXinRewardReceivedDesc', '')
        self.dataDic[WEIXING_BIND] = ret
        return ret

    def getEKeyData(self):
        p = BigWorld.player()
        ret = {}
        qrContent = self.qrContents.get(EKEY_BIND, None)
        if not qrContent:
            qrContent = uiUtils.getQRCodeBuff(EKEY_URL_PATH)
        self.qrContents[EKEY_BIND] = qrContent
        ret['qrContent'] = qrContent
        ret['hasEkeyRewardReceived'] = p.hasEkeyRewardReceived
        hasBindEkey = p.securityTypeOfCell in const.SECURITY_TYPE_EKEY
        ret['hasBindEkey'] = hasBindEkey
        ret['tipText'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BINDED, '') if hasBindEkey else uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_UNBINDED, '')
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('EKeyDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_FREQUENCY, '')
        if not hasBindEkey:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_NEED_BIND, '')
        elif p.hasEkeyRewardReceived:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_BIND_REWARD_GOT, '')
        else:
            ret['tip'] = ''
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_EKEY_DESC, '')
        ret['itemDetial'] = BPD.data.get('EKeyBonusDetail', '')
        if self.jumpIndex < 0 and ret['hasBindEkey'] and not ret['hasEkeyRewardReceived']:
            self.jumpIndex = EKEY_BIND
        self.dataDic[EKEY_BIND] = ret
        return ret

    def getAPPData(self):
        p = BigWorld.player()
        ret = {}
        ret['desc'] = BPD.data.get('AppBindDesc', '')
        qrContent = self.qrContents.get(APP_BIND, None)
        if not qrContent:
            qrContent = uiUtils.getQRCodeBuff(APP_URL_PATH)
        self.qrContents[APP_BIND] = qrContent
        ret['qrContent'] = qrContent
        ret['spriteKey'] = BPD.data.get('AppSpriteKey', 0)
        ret['hasBindApp'] = p.appBindStatus in BIND_STATUS
        ret['expired'] = p.appBindStatus == gametypes.BIND_STATUS_EXPIRED
        ret['itemTip'] = BPD.data.get('AppItemTip', '')
        rewardItemId = BPD.data.get('AppDisplayItemId', 0)
        ret['items'] = uiUtils.getGfxItemById(rewardItemId)
        ret['rewardDetail'] = BPD.data.get('AppBindDetail', '')
        ret['AppTips'] = BPD.data.get('AppTips', '')
        ret['AppExpiredTips'] = BPD.data.get('AppExpiredTips', '')
        ret['hasReward'] = not p.appBindRewarded
        ret['receivedDesc'] = BPD.data.get('AppRewardReceivedDesc', '')
        if self.jumpIndex < 0 and ret['hasBindApp'] and ret['hasReward']:
            self.jumpIndex = APP_BIND
        self.dataDic[APP_BIND] = ret
        return ret

    def getPhoneData(self):
        ret = {}
        p = BigWorld.player()
        ret['key'] = PHONT_BIND
        ret['hasPhoneBinding'] = p.hasPhoneBinding
        ret['hasPhoneRewardReceived'] = p.hasPhoneRewardReceived
        ret['bindPhoneNum'] = p.bindPhoneNum
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('PhoneBindingDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_FREQUENCY, '')
        if not p.hasPhoneBinding:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_NEED_BIND, '')
        elif p.hasPhoneRewardReceived:
            ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_BIND_REWARD_GOT, '')
        else:
            ret['tip'] = ''
        ret['timer'] = self.timer
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PHONE_DESC, '')
        ret['itemDetial'] = BPD.data.get('PhoneBonusDetail', '')
        if self.jumpIndex < 0 and ret['hasPhoneBinding'] and not ret['hasPhoneRewardReceived']:
            self.jumpIndex = PHONT_BIND
        self.dataDic[PHONT_BIND] = ret
        return ret

    def getPassWordData(self):
        ret = {}
        p = BigWorld.player()
        ret['hasPassword'] = p.hasInvPassword
        ret['desc'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PASSWORD_DESC, '')
        ret['items'] = uiUtils.getGfxItemById(BPD.data.get('PasswordDisplayItemId', 0))
        ret['itemTip'] = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_PASSWORD_BIND_REWARD_FREQUENCY, '')
        ret['itemDetial'] = BPD.data.get('PasswordBonusDetail', '')
        ret['hasCipherRewardReceived'] = p.hasCipherRewardReceived
        if self.jumpIndex < 0 and ret['hasPassword'] and not ret['hasCipherRewardReceived']:
            self.jumpIndex = PASSWORD_BIND
        self.dataDic[PASSWORD_BIND] = ret
        return ret

    def refreshLevel(self):
        if not self.widget:
            return
        self.getLevel()
        self.widget.level.gotoAndStop('s%d' % self.level)
        for i in xrange(len(DEFAULT_ORDERS)):
            mc = self.widget.getChildByName('star%d' % i)
            if self.level > i:
                mc.gotoAndStop('full')
            else:
                mc.gotoAndStop('empty')

    def refreshEKeyBind(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(EKEY_BIND, None)
            if not widget:
                return
            if not widget.ekeyPanel:
                return
            data = self.getEKeyData()
            if data['hasBindEkey']:
                widget.ekeyPanel.gotoAndPlay('finished')
            else:
                widget.ekeyPanel.gotoAndPlay('normal')
                widget.ekeyPanel.commonBtn.visible = not data['hasBindEkey']
                widget.ekeyPanel.commonBtn.addEventListener(events.MOUSE_CLICK, self.onBindEkeyClick, False, 0, True)
                widget.ekeyPanel.picture.loading.visible = False
                widget.ekeyPanel.picture.pictureCanvas.fitSize = True
                widget.ekeyPanel.picture.pictureCanvas.loadImageByBase64(data['qrContent'])
            widget.ekeyPanel.itemTip.htmlText = data['itemTip']
            widget.ekeyPanel.desc.htmlText = data['desc']
            widget.ekeyPanel.detail.htmlText = data['itemDetial']
            item = widget.ekeyPanel.item
            item.dragable = False
            item.setItemSlotData(data['items'])
            item.validateNow()
            TipManager.addItemTipById(item, int(data['items']['itemId']))
            widget.ekeyPanel.getItemBtn.visible = data['hasBindEkey'] and not data['hasEkeyRewardReceived']
            widget.ekeyPanel.tipText.htmlText = data['tip']
            widget.ekeyPanel.tipText.visible = data['hasBindEkey'] and data['hasEkeyRewardReceived']
            widget.ekeyPanel.getItemBtn.addEventListener(events.MOUSE_CLICK, self.onBindEkeyRewardClick, False, 0, True)
            return

    def onBindEkeyRewardClick(self, *args):
        p = BigWorld.player()
        if not p:
            return
        playerLv = p.lv
        limitLv = BPD.data.get('EkeyLimitLv', 20)
        if playerLv < limitLv:
            p.showGameMsg(GMDD.data.EKEY_REWARD_REC_FAIL_BY_LV_LIMIT, ())
        else:
            p.cell.receiveEkeyReward()

    def onBindEkeyClick(self, *args):
        BigWorld.openUrl('http://reg.163.com/mibao/controller/goIndex.jsp')
        msg = uiUtils.getTextFromGMD(GMDD.data.USER_ACCOUNT_BIND_OPEN_EKEY_PAGE_TIP, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.bindEkeySuc), yesBtnText=gameStrings.ACCOUNT_BIND_PROXY_BINDED, noBtnText=gameStrings.ACCOUNT_BIND_PROXY_NOT_BIND)

    def bindEkeySuc(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(EKEY_BIND, None)
            if widget:
                self.refreshEKeyBind()
                self.refreshLevel()
            else:
                self.refreshFrame()
            return

    def refreshPhoneBind(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(PHONT_BIND, None)
            if not widget:
                return
            if not widget.phonePanel:
                return
            data = self.getPhoneData()
            widget.phonePanel.gotoAndStop('normal')
            widget.phonePanel.changePhoneBtn.visible = data['bindPhoneNum'] != ''
            widget.phonePanel.commonBtn.label = gameStrings.ACCOUNT_BIND_PROXY_VERTIFY if data['hasPhoneBinding'] else gameStrings.ACCOUNT_BIND_PROXY_COMMIT
            widget.phonePanel.commonBtn.visible = not data['hasPhoneBinding']
            widget.phonePanel.accountInput2.textField.restrict = '0-9'
            widget.phonePanel.cancelBtn.visible = False
            widget.phonePanel.commonBtn.x = 90
            widget.phonePanel.reachedMc.visible = data['hasPhoneBinding']
            if data['bindPhoneNum']:
                phone = data['bindPhoneNum']
                temp = ASUtils.splitPhoneNumber(phone)
                widget.phonePanel.accountInput1.area = temp[0]
                widget.phonePanel.accountInput1.phone = temp[1]
            widget.phonePanel.accountInput1.onlyDisplay = data['bindPhoneNum'] != ''
            item = widget.phonePanel.item
            item.dragable = False
            item.setItemSlotData(data['items'])
            item.validateNow()
            TipManager.addItemTipById(item, data['items']['itemId'])
            widget.phonePanel.getYZMBtn.addEventListener(events.MOUSE_CLICK, self.onGetYZMClick, False, 0, True)
            widget.phonePanel.changePhoneBtn.addEventListener(events.MOUSE_CLICK, self.onChangePhoneClick, False, 0, True)
            widget.phonePanel.getItemBtn.addEventListener(events.MOUSE_CLICK, self.onPhoneRewardClick, False, 0, True)
            widget.phonePanel.commonBtn.addEventListener(events.BUTTON_CLICK, self.onCommonClick, False, 0, True)
            widget.phonePanel.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCancelClick, False, 0, True)
            widget.phonePanel.itemTip.htmlText = data['itemTip']
            widget.phonePanel.tip.htmlText = data['tip']
            widget.phonePanel.getItemBtn.visible = data['hasPhoneBinding'] and not data['hasPhoneRewardReceived']
            widget.phonePanel.getYZMBtn.label = gameStrings.ACCOUNT_BIND_PROXY_GETYZM
            isCountDown = True if data['timer'] > 0 else False
            widget.phonePanel.countdown.visible = isCountDown
            widget.phonePanel.getYZMBtn.htmlText = gameStrings.ACCOUNT_BIND_PROXY_YZM_SENDED % data['timer']
            widget.phonePanel.getYZMBtn.enabled = not isCountDown
            widget.phonePanel.countdown.visible = isCountDown
            widget.phonePanel.desc.htmlText = data['desc']
            widget.phonePanel.detail.htmlText = data['itemDetial']
            return

    def onGetYZMClick(self, *args):
        e = ASObject(args[3][0])
        accountInput1 = e.currentTarget.parent.accountInput1
        phoneNum = accountInput1.entirePhone
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

    def updateTimer(self):
        self.updateYZMBtnState()
        if self.timer > 0:
            self.timer -= 1
            self.timerId = BigWorld.callback(1.0, self.updateTimer)
        else:
            BigWorld.cancelCallback(self.timerId)

    def updateYZMBtnState(self):
        widget = self.mcRecord.get(PHONT_BIND, None)
        if not widget:
            return
        elif not widget.phonePanel:
            return
        else:
            msg = gameStrings.ACCOUNT_BIND_PROXY_GETYZM
            enable = True
            if self.timer > 0:
                msg = gameStrings.ACCOUNT_BIND_PROXY_YZM_SENDED % self.timer
                enable = False
            widget.phonePanel.getYZMBtn.enabled = enable
            widget.phonePanel.countdown.visible = not enable
            widget.phonePanel.countdown.htmlText = msg
            return

    def onChangePhoneClick(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        widget.phonePanel.accountInput1.phone = ''
        widget.phonePanel.accountInput1.onlyDisplay = False
        widget.phonePanel.accountInput1.phoneNumberInput.textField.restrict = '0-9'
        widget.phonePanel.changePhoneBtn.visible = False
        widget.phonePanel.commonBtn.label = gameStrings.ACCOUNT_BIND_PROXY_COMMIT
        widget.phonePanel.commonBtn.visible = True
        widget.phonePanel.cancelBtn.visible = True
        widget.phonePanel.commonBtn.x = 40

    def onPhoneRewardClick(self, *args):
        limitLv = BPD.data.get('PhoneBindLimitLv', 30)
        p = BigWorld.player()
        playerLv = p.lv
        if playerLv < limitLv:
            p.showGameMsg(GMDD.data.PHONE_BIND_REWARD_REC_FAIL_BY_LV_LIMIT, ())
        else:
            p.cell.receivePhoneBindReward()

    def onCommonClick(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        phoneNum = widget.phonePanel.accountInput1.entirePhone
        verifyCode = widget.phonePanel.accountInput2.text
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

    def onCancelClick(self, *args):
        e = ASObject(args[3][0])
        self.refreshPhoneBind()

    def refreshPassword(self):
        BigWorld.callback(0.5, self.realRefreshPassword)

    def realRefreshPassword(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(PASSWORD_BIND, None)
            if not widget:
                return
            if not widget.passwordPanel:
                return
            data = self.getPassWordData()
            widget.passwordPanel.getItemBtn.addEventListener(events.MOUSE_CLICK, self.onGetPasswordReward, False, 0, True)
            if data['hasPassword']:
                self.updatePasswordNormal()
            else:
                self.updatePasswordSet()
            return

    def updatePasswordSet(self):
        widget = self.mcRecord.get(PASSWORD_BIND, None)
        data = self.dataDic.get(PASSWORD_BIND, {})
        passwordDesc = data.get('desc', '')
        if not self.widget:
            return
        elif not widget or not data:
            return
        else:
            widget.passwordPanel.gotoAndStop('passwordSet')
            widget.passwordPanel.desc.htmlText = passwordDesc
            widget.passwordPanel.input1.textField.restrict = 'a-zA-Z0-9'
            widget.passwordPanel.input2.textField.restrict = 'a-zA-Z0-9'
            widget.passwordPanel.commonBtn.addEventListener(events.MOUSE_CLICK, self.onSubmitSetPassword, False, 0, True)
            self.updatePasswordReward()
            return

    def updatePasswordNormal(self):
        widget = self.mcRecord.get(PASSWORD_BIND, None)
        data = self.dataDic.get(PASSWORD_BIND, {})
        passwordDesc = data.get('desc', '')
        if not self.widget:
            return
        elif not widget or not data:
            return
        else:
            widget.passwordPanel.gotoAndStop('passwordNormal')
            widget.passwordPanel.desc.htmlText = passwordDesc
            widget.passwordPanel.commonBtn.addEventListener(events.MOUSE_CLICK, self.onResetPassword, False, 0, True)
            widget.passwordPanel.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onClearPassword, False, 0, True)
            self.updatePasswordReward()
            return

    def updatePasswordReward(self):
        widget = self.mcRecord.get(PASSWORD_BIND, None)
        if not self.widget:
            return
        elif not widget:
            return
        else:
            psswordData = self.dataDic[PASSWORD_BIND]
            if not psswordData:
                return
            widget.passwordPanel.detail.htmlText = psswordData['itemDetial']
            item = widget.passwordPanel.item
            item.dragable = False
            item.setItemSlotData(psswordData['items'])
            item.validateNow()
            TipManager.addItemTipById(item, psswordData['items']['itemId'])
            widget.passwordPanel.getItemBtn.visible = psswordData['hasPassword'] and not psswordData['hasCipherRewardReceived']
            widget.passwordPanel.tipText.visible = psswordData['hasPassword'] and psswordData['hasCipherRewardReceived']
            widget.passwordPanel.tipText.htmlText = gameStrings.ACCOUNT_BIND_PROXY_GAINED_M
            widget.passwordPanel.itemTip.htmlText = psswordData['itemTip']
            return

    def updatePasswordClear(self):
        widget = self.mcRecord.get(PASSWORD_BIND, None)
        passwordDesc = self.dataDic.get(PASSWORD_BIND, {}).get('desc', '')
        if not widget or not self.widget or not passwordDesc:
            return
        else:
            widget.passwordPanel.gotoAndStop('passwordClear')
            widget.passwordPanel.radioBtn1.selected = True
            widget.passwordPanel.radioBtn2.selected = False
            widget.passwordPanel.radioBtn1.addEventListener(events.MOUSE_CLICK, self.handleSelect, False, 0, True)
            widget.passwordPanel.desc.htmlText = passwordDesc
            widget.passwordPanel.input1.textField.restrict = 'a-zA-Z0-9'
            widget.passwordPanel.commonBtn.addEventListener(events.MOUSE_CLICK, self.onConfirmClearPassword, False, 0, True)
            widget.passwordPanel.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCancelClearPassword, False, 0, True)
            self.updatePasswordReward()
            return

    def handleSelect(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        widget.passwordPanel.input1.focused = 1

    def onConfirmClearPassword(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        selectType = 0 if widget.passwordPanel.radioBtn1.selected else 1
        oldPassword = widget.passwordPanel.input1.text
        if selectType == 0:
            if not oldPassword:
                return
            BigWorld.player().cell.modifyCipher(oldPassword, '')
        else:
            p = BigWorld.player()
            p.base.resetCipher()
            if p.cipherResetTime > 0:
                p.showTopMsg(gameStrings.ACCOUNT_BIND_PROXY_CLEAR_PWD)

    def onClearPassword(self, *args):
        self.updatePasswordClear()

    def onGetPasswordReward(self, *args):
        BigWorld.player().cell.receiveCipherReward()

    def onResetPassword(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        data = self.dataDic.get(PASSWORD_BIND, {})
        if not data:
            return
        widget.passwordPanel.gotoAndStop('passwordReset')
        passwordDesc = data['desc']
        widget.passwordPanel.desc.htmlText = passwordDesc
        widget.passwordPanel.input1.textField.restrict = 'a-zA-Z0-9'
        widget.passwordPanel.input2.textField.restrict = 'a-zA-Z0-9'
        widget.passwordPanel.input3.textField.restrict = 'a-zA-Z0-9'
        widget.passwordPanel.commonBtn.addEventListener(events.MOUSE_CLICK, self.onSubmitResetPassword, False, 0, True)
        widget.passwordPanel.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCanceResetPassword, False, 0, True)

    def onSubmitResetPassword(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        old = widget.passwordPanel.input1.text
        new1 = widget.passwordPanel.input2.text
        new2 = widget.passwordPanel.input3.text
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

    def onCanceResetPassword(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        widget.passwordPanel.gotoAndStop('passwordNormal')

    def onClearPassword(self, *args):
        self.updatePasswordClear()

    def onSubmitSetPassword(self, *args):
        e = ASObject(args[3][0])
        widget = e.currentTarget.parent.parent
        password = widget.passwordPanel.input1.text
        passwordConfirm = widget.passwordPanel.input2.text
        if not password:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())
            return
        if password != passwordConfirm:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INCONSISTENT_PASSWORD, ())
            return
        BigWorld.player().cell.modifyCipher('', password)

    def onCancelClearPassword(self, *args):
        self.updatePasswordNormal()

    def refreshWeiXinBind(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(WEIXING_BIND, None)
            if not widget:
                return
            if not widget.weiXinPanel:
                return
            data = self.getWeiXinData()
            if data['hasBindWeiXin'] and not data['expired']:
                self.updateWeiXinBind(widget, data)
            else:
                self.updateWeiXinNotBind(widget, data)
            return

    def updateWeiXinBind(self, widget, data):
        widget.weiXinPanel.gotoAndStop('finsh')
        hasReward = data['hasReward']
        widget.weiXinPanel.tips.visible = not hasReward
        widget.weiXinPanel.tips.text = data['receivedDesc']
        widget.weiXinPanel.getItemBtn.visible = hasReward
        widget.weiXinPanel.getItemBtn.addEventListener(events.MOUSE_CLICK, self.onGetWeiXinReward, False, 0, True)
        self.updateWeiXinReward(widget, data)

    def updateWeiXinNotBind(self, widget, data):
        widget.weiXinPanel.gotoAndStop('nothing')
        widget.weiXinPanel.picture.fitSize = True
        widget.weiXinPanel.picture.loadImageByBase64(data['qrContent'])
        widget.weiXinPanel.sprite.helpKey = data['spriteKey']
        widget.weiXinPanel.tips.text = data['WeiXinTips'] if not data['expired'] else data['WeiXinExpiredTips']
        widget.weiXinPanel.grayBtn.addEventListener(events.MOUSE_CLICK, self.onQueryWeiXinBindState, False, 0, True)
        self.updateWeiXinTimer()
        self.updateWeiXinReward(widget, data)

    def updateWeiXinReward(self, widget, data):
        widget.weiXinPanel.desc.htmlText = data['desc']
        widget.weiXinPanel.itemTip.text = data['itemTip']
        item = widget.weiXinPanel.item
        item.setItemSlotData(data['items'])
        item.validateNow()
        TipManager.addItemTipById(item, data['items']['itemId'])
        widget.weiXinPanel.detail.htmlText = data['rewardDetail']

    def onGetWeiXinReward(self, *args):
        p = BigWorld.player()
        if p.weixinBindStatus == gametypes.BIND_STATUS_EXPIRED:
            p.showGameMsg(GMDD.data.WEIXIN_NOTIFY_REBIND, ())
        else:
            limitLv = BPD.data.get('WEIXIN_BIND_LV_LIMIT', 20)
            if p.lv < limitLv:
                p.showGameMsg(GMDD.data.APPLY_BIND_REWARD_FAILED_LV_LIMIT, (limitLv,))
            else:
                addMental = BPD.data.get('WEIXIN_BIND_BONUS_MENTAL', 300)
                addLabour = BPD.data.get('WEIXIN_BIND_BONUS_LABOUR', 300)
                if self.isMentalLabourOver(addMental, addLabour):
                    msg = GMD.data.get(GMDD.data.MENTAL_LABOUR_OVER_LIMIT_CONFIRM, {}).get('text', '')
                    self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=p.cell.applyWeixinBindReward)
                else:
                    p.cell.applyWeixinBindReward()

    def onQueryWeiXinBindState(self, *args):
        now = utils.getNow()
        lastClickTime = self.clickQueryTimeRecord.get(WEIXING_BIND, 0)
        if now - lastClickTime < 60:
            return
        p = BigWorld.player()
        p.base.queryWeixinBindStatus()
        self.clickQueryTimeRecord[WEIXING_BIND] = now

    def refreshAppBind(self):
        if not self.widget:
            return
        else:
            widget = self.mcRecord.get(APP_BIND, None)
            if not widget:
                return
            if not widget.appPanel:
                return
            data = self.getAPPData()
            if data['hasBindApp'] and not data['expired']:
                self.updateAppBind(widget, data)
            else:
                self.updateAppNotBind(widget, data)
            return

    def updateAppBind(self, widget, data):
        widget.appPanel.gotoAndStop('finsh')
        hasReward = data['hasReward']
        widget.appPanel.tips.visible = not hasReward
        widget.appPanel.tips.text = data['receivedDesc']
        widget.appPanel.getItemBtn.visible = hasReward
        widget.appPanel.getItemBtn.addEventListener(events.MOUSE_CLICK, self.onGetAppReward, False, 0, True)
        self.updateAppReward(widget, data)

    def updateAppNotBind(self, widget, data):
        widget.appPanel.gotoAndStop('nothing')
        widget.appPanel.picture.fitSize = True
        widget.appPanel.picture.loadImageByBase64(data['qrContent'])
        widget.appPanel.sprite.helpKey = data['spriteKey']
        widget.appPanel.tips.text = data['AppTips'] if not data['expired'] else data['AppExpiredTips']
        widget.appPanel.grayBtn.addEventListener(events.MOUSE_CLICK, self.onQueryAppBindState, False, 0, True)
        self.updateAppBindTimer()
        self.updateAppReward(widget, data)

    def updateAppReward(self, widget, data):
        widget.appPanel.desc.htmlText = data['desc']
        widget.appPanel.itemTip.text = data['itemTip']
        item = widget.appPanel.item
        item.setItemSlotData(data['items'])
        item.validateNow()
        TipManager.addItemTipById(item, data['items']['itemId'])
        widget.appPanel.detail.htmlText = data['rewardDetail']

    def onGetAppReward(self, *args):
        p = BigWorld.player()
        if p.appBindStatus == gametypes.BIND_STATUS_EXPIRED:
            p.showGameMsg(GMDD.data.APP_NOTIFY_REBIND, ())
        else:
            limitLv = BPD.data.get('APP_BIND_LV_LIMIT', 20)
            if p.lv < limitLv:
                p.showGameMsg(GMDD.data.APPLY_BIND_REWARD_FAILED_LV_LIMIT, (limitLv,))
            else:
                p.cell.applyAppBindReward()

    def onQueryAppBindState(self, *args):
        now = utils.getNow()
        lastClickTime = self.clickQueryTimeRecord.get(APP_BIND, 0)
        if now - lastClickTime < 60:
            return
        p = BigWorld.player()
        p.base.queryAppBindStatus()
        self.clickQueryTimeRecord[APP_BIND] = now

    def refreshFrame(self):
        if not self.widget:
            return
        self.refreshLevel()
        self.jumpIndex = -1
        self.widget.removeAllInst(self.widget.pageList.canvas, True)
        self.mcRecord = {}
        self.getWeiXinData()
        self.getEKeyData()
        self.getAPPData()
        self.getPhoneData()
        self.getPassWordData()
        self.widget.pageList.data = DEFAULT_ORDERS
        self.widget.pageList.validateNow()
        if self.jumpIndex >= 0:
            self.widget.pageList.jumpToIndex(self.jumpIndex)

    def _initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick)
        self.widget.pageList.childItem = 'AccountBind_Item'
        self.widget.pageList.pageItemFunc = self.pageItemFunc
        self.widget.pageList.childWidth = 273

    def onCloseClick(self, *args):
        self.hide()

    def pageItemFunc(self, *args):
        mc = ASObject(args[3][0])
        key = int(args[3][1].GetNumber())
        mc.gotoAndStop(KEY_FRAME_NAMES[key])
        self.mcRecord[key] = mc
        mc.name = str(key)
        if key == EKEY_BIND:
            self.refreshEKeyBind()
        elif key == PHONT_BIND:
            self.refreshPhoneBind()
        elif key == PASSWORD_BIND:
            self.realRefreshPassword()
        elif key == WEIXING_BIND:
            self.refreshWeiXinBind()
        elif key == APP_BIND:
            self.refreshAppBind()

    def addPushMsg(self):
        if not gameglobal.rds.configData.get('enableBindReward', False):
            return
        pushOnce = AppSettings.get(keys.SET_ACCOUNT_BIND_REMIND_FLAG, 0)
        pushMsg = gameglobal.rds.ui.pushMessage
        if not pushOnce:
            callBackDict = {'click': Functor(self.show)}
            pushMsg.setCallBack(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ONCE_ONLY_REMID, callBackDict)
            pmd = PD.data.get(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ONCE_ONLY_REMID, {})
            msgInfo = {'iconId': pmd.get('iconId', 0),
             'tooltip': pmd.get('tooltip', '')}
            pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ONCE_ONLY_REMID, msgInfo=msgInfo)
            AppSettings[keys.SET_ACCOUNT_BIND_REMIND_FLAG] = 1
            AppSettings.save()

    def addWeeklyPushMsg(self):
        if not gameglobal.rds.configData.get('enableBindReward', False):
            return
        pushMsg = gameglobal.rds.ui.pushMessage
        callBackDict = {'click': Functor(self.show)}
        pushMsg.setCallBack(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ZERO_LEVEL, callBackDict)
        pmd = PD.data.get(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ZERO_LEVEL, {})
        msgInfo = {'iconId': pmd.get('iconId', 0),
         'tooltip': pmd.get('tooltip', '')}
        pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ZERO_LEVEL, msgInfo=msgInfo)

    def isMentalLabourOver(self, addMental, addLabour):
        p = BigWorld.player()
        addMental = int(addMental / 10)
        addLabour = int(addLabour / 10)
        nowMental = int(p.mental / 10)
        nowLabour = int(p.labour / 10)
        if uiUtils.hasVipBasic():
            mLabour = 2 * int(p.mLabour / 10)
            mMental = 2 * int(p.mMental / 10)
        else:
            mLabour = int(p.mLabour / 10)
            mMental = int(p.mMental / 10)
        return nowMental + addMental >= mMental or nowLabour + addLabour >= mLabour

    def delPushMsg(self):
        pushMsg = gameglobal.rds.ui.pushMessage
        pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ONCE_ONLY_REMID)
        pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_ACCOUNT_BIND_ZERO_LEVEL)
