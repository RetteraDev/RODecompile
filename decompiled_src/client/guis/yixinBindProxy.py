#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yixinBindProxy.o
import BigWorld
import gameglobal
import const
import utils
from guis import uiConst
from guis.uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class YixinBindProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YixinBindProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'getCode': self.getCode,
         'bindYixin': self.bindYixin}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YIXIN_BIND, self.closeWidget)

    def reset(self):
        self.dismiss()

    def getCode(self, *args):
        phoneNum = args[3][0].GetString()
        phoneNum = phoneNum.strip()
        if phoneNum.find('+86-') != -1:
            phoneNum = phoneNum[4:len(phoneNum)]
        if phoneNum:
            if utils.isValidPhoneNum(phoneNum) and phoneNum.find('+86') == -1:
                BigWorld.player().base.requestYixinCaptcha(phoneNum)
                self.mediator.Invoke('startCaptchaTimer', ())
            else:
                BigWorld.player().showGameMsg(GMDD.data.YIXIN_INPUT_CORRECT_PHONENUM, ())
        else:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_INPUT_PHONENUM, ())

    def bindYixin(self, *args):
        phoneNum = args[3][0].GetString()
        secCode = args[3][1].GetString()
        phoneNum = phoneNum.strip()
        if phoneNum.find('+86-') != -1:
            phoneNum = phoneNum[4:len(phoneNum)]
        if phoneNum:
            if utils.isValidPhoneNum(phoneNum):
                if secCode:
                    BigWorld.player().base.bindYixin(phoneNum, secCode)
                    return
                BigWorld.player().showGameMsg(GMDD.data.YIXIN_INPUT_CAPCHA, ())
            else:
                BigWorld.player().showGameMsg(GMDD.data.YIXIN_INPUT_CORRECT_PHONENUM, ())
        else:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_INPUT_PHONENUM, ())
        self.mediator.Invoke('wrongCallBack', ())

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        BigWorld.player().registerEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinSuccess)
        BigWorld.player().registerEvent(const.EVENT_YIXIN_BIND_FAILED, self.bindYixinFailed)

    def bindYixinFailed(self, params):
        self.mediator.Invoke('wrongCallBack', ())
        if params[0] == const.YIXIN_ERR_BAD_YIXIN_SERVER_REPLY:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_BAD_YIXIN_SERVER_REPLY, ())
        if params[0] == const.YIXIN_ERR_PLAYER_NOT_EXIST:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_PLAYER_NOT_EXIST, ())
        elif params[0] == const.YIXIN_ERR_BAD_MOBILE:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_BAD_MOBILE, ())
        elif params[0] == const.YIXIN_ERR_DOUBLE_YIXIN_BIND:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_DOUBLE_YIXIN_BIND, ())
        elif params[0] == const.YIXIN_ERR_DOUBLE_USER_BIND:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_DOUBLE_USER_BIND, ())
        elif params[0] == const.YIXIN_ERR_COOLING_DOWN:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_COOLING_DOWN, ())
        elif params[0] == const.YIXIN_ERR_CAPTCHA_ERROR:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ERR_CAPTCHA_ERROR, ())
        else:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_UNKNOW_ERROR, params[0])

    def bindYixinSuccess(self, params):
        self.closeWidget()
        BigWorld.player().showGameMsg(GMDD.data.YIXIN_BIND_SUCCESS, ())
        gameglobal.rds.ui.yixinRewards.show()

    def dismiss(self, *arg):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_BIND)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.isShow = False
        self.mediator = None
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinSuccess)
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_FAILED, self.bindYixinFailed)

    def toggle(self):
        if self.isShow:
            isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
            if not isShowYixin:
                return
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_BIND)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_BIND)
        self.isShow = not self.isShow

    def show(self):
        isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
        if not isShowYixin:
            return
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_BIND)
        self.isShow = True
