#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pinJiuProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
from uiProxy import UIProxy
from callbackHelper import Functor
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class PinJiuProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PinJiuProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'doPinJiu': self.onDoPinJiu,
         'endPinJiu': self.onEndPinJiu}
        self.mediator = None
        self.state = const.PINJIU_NORMAL
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_PINJIU, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PINJIU:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PINJIU)

    def reset(self):
        self.state = const.PINJIU_NORMAL
        self.npcId = 0
        BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)

    def checkAndHide(self):
        if self.state == const.PINJIU_NORMAL:
            msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_CLOSE_HINT, gameStrings.TEXT_PINJIUPROXY_43)
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(npc.cell.endPinjiu))
            else:
                self.hide()
        else:
            self.hide()

    def show(self, state, npcId):
        self.state = state
        self.npcId = npcId
        BigWorld.player().lockKey(gameglobal.KEY_POS_UI, False)
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PINJIU)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            msg = ''
            info['title'] = SCD.data.get('zuiyiTitle', gameStrings.TEXT_PINJIUPROXY_70)
            statsBtnNames = SCD.data.get('zuiyiBtns', [(gameStrings.TEXT_PINJIUPROXY_71, gameStrings.TEXT_PINJIUPROXY_71_1),
             (gameStrings.TEXT_AVATAR_6426_1,),
             (gameStrings.TEXT_AVATAR_6426_1,),
             (gameStrings.TEXT_AVATAR_6426_1,)])
            if self.state == const.PINJIU_NORMAL:
                btnState = 'normal'
                zuiyiDesc = SCD.data.get('zuiyiDesc', ((0, 20, ''),
                 (21, 49, ''),
                 (50, 79, ''),
                 (80, 100, '')))
                for low, high, desc in zuiyiDesc:
                    if p.zuiyi >= low and p.zuiyi <= high:
                        msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_NORMAL_HINT, '%s') % desc
                        break

                info['doPinJiuBtnLabel'] = statsBtnNames[self.state][0]
                info['endPinJiuBtnLabel'] = statsBtnNames[self.state][1]
            elif self.state == const.PINJIU_WIN:
                btnState = 'end'
                msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_WIN_HINT, '')
                info['closePinJiuBtnLabel'] = statsBtnNames[self.state][0]
            elif self.state == const.PINJIU_LOSE:
                btnState = 'end'
                msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_LOSE_HINT, '')
                info['closePinJiuBtnLabel'] = statsBtnNames[self.state][0]
            elif self.state == const.PINJIU_LOSE_OVER:
                btnState = 'end'
                msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_LOSE_OVER_HINT, '')
                info['closePinJiuBtnLabel'] = statsBtnNames[self.state][0]
            info['content'] = msg
            info['btnState'] = btnState
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onClose(self, *arg):
        self.checkAndHide()

    def onDoPinJiu(self, *arg):
        msg = uiUtils.getTextFromGMD(GMDD.data.PIN_JIU_GO_ON_HINT, '')
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(npc.cell.doPinjiu))
        else:
            self.hide()

    def onEndPinJiu(self, *arg):
        self.checkAndHide()
