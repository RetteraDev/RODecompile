#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/xinmoBookProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import ui
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import uiUtils
from cdata import collect_item_pos2item_data as CIPD
from cdata import game_msg_def_data as GMDD
from data import collect_item_data as CID

class XinmoBookProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(XinmoBookProxy, self).__init__(uiAdapter)
        self.modelMap = {'getBookType': self.onGetBookType,
         'closeXinmoBook': self.onCloseXinmoBook,
         'clickItem': self.onClickItem,
         'getPosInfo': self.onGetPosInfo,
         'getTipInfo': self.onGetTipInfo}
        self.mediator = None
        self.bookType = 0
        self.needShow = False
        self.activityId = None
        self.roundInfo = None
        self.countDown = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_XINMO_BOOK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def reset(self):
        self.needShow = False
        self.activityId = None
        self.roundInfo = None

    def onGetTipInfo(self, *args):
        p = BigWorld.player()
        pos = args[3][0].GetNumber()
        if not self.roundInfo['needItemCnt']:
            ret = ['0', gameStrings.TEXT_XINMOBOOKPROXY_46 % 0, gameStrings.TEXT_XINMOBOOKPROXY_46_1 % 0]
            return uiUtils.array2GfxAarry(ret, True)
        rarePos = self.roundInfo.get('rarePos', -1)
        current = self.roundInfo['posInfo'].get(pos, 0)
        total = self.roundInfo['needItemCnt']
        roundNo = self.roundInfo['roundNo']
        itemId = CIPD.data.get(pos, {}).get('originItem', 0)
        count = p.inv.countItemInPages(itemId, enableParentCheck=True)
        tips = CID.data.get(1, {}).get('rareCharacterTip', gameStrings.TEXT_XINMOBOOKPROXY_54)
        ret = [current,
         total,
         gameStrings.TEXT_XINMOBOOKPROXY_46 % roundNo,
         gameStrings.TEXT_XINMOBOOKPROXY_46_1 % count,
         rarePos,
         tips]
        return uiUtils.array2GfxAarry(ret, True)

    def onGetPosInfo(self, *args):
        ret = None
        p = BigWorld.player()
        if self.roundInfo:
            ret = self.roundInfo
            return uiUtils.dict2GfxDict(ret)
        else:
            return

    def onGetBookType(self, *args):
        return GfxValue(self.bookType)

    def onCloseXinmoBook(self, *args):
        self.hide()

    def onClickItem(self, *args):
        if self.countDown > 0:
            return
        pos = args[3][0].GetNumber()
        p = BigWorld.player()
        if self.activityId:
            itemId = CIPD.data.get(pos, {}).get('originItem', 0)
            replaceId = CIPD.data.get(pos, {}).get('replaceItems', [0])[0]
            name = CIPD.data.get(pos, {}).get('name', '')
            itemCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
            replaceCount = p.inv.countItemInPages(replaceId, enableParentCheck=True)
            if itemCount <= 0 and replaceCount <= 0:
                p.showGameMsg(GMDD.data.COLLECT_ITEM_CHA_NOT_ENOUGH, name)
            elif itemCount <= 0 and replaceCount > 0:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_XINMOBOOKPROXY_85 % name, Functor(self.realhandIn, pos, replaceId))
            else:
                p.base.handInCollectItem(self.activityId, pos)

    def realhandIn(self, pos, itemId):
        p = BigWorld.player()
        p.base.handInCollectItemReplace(self.activityId, pos, itemId)

    def clearWidget(self):
        self.mediator = None
        ui.reset_cursor()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_XINMO_BOOK)

    def show(self, activityId, roundInfo):
        if self.needShow:
            p = BigWorld.player()
            if not gameglobal.rds.ui.xinmoRecord._checkActivityTime():
                p.showGameMsg(GMDD.data.XINMO_ACTIVITY_JOIN_TIME_WRONG, ())
                self.needShow = False
                return
            if not gameglobal.rds.ui.xinmoRecord._checkCollectItemSignUp():
                p.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_NO_SIGNUP, ())
                self.needShow = False
                return
            self.activityId = activityId
            self.roundInfo = roundInfo
            ui.reset_cursor()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_XINMO_BOOK)

    def queryInfo(self, actId, bookType):
        p = BigWorld.player()
        p.base.queryRoundInfo(actId)
        self.needShow = True
        self.bookType = bookType

    def refreshView(self, roundInfo):
        if self.mediator:
            self.roundInfo = roundInfo
            self.mediator.Invoke('refreshView')

    def playAnimation(self, roundInfo):
        if self.mediator:
            self.roundInfo = roundInfo
            self.mediator.Invoke('playAnimation')

    def playSucItem(self, pos):
        if self.mediator:
            self.mediator.Invoke('playSucItem', GfxValue(pos))
        if self.countDown <= 0:
            self.countDown = 2
            BigWorld.callback(0.1, self.refreshCountDown)

    def refreshCountDown(self):
        self.countDown -= 0.1
        if self.countDown > 0:
            BigWorld.callback(0.1, self.refreshCountDown)
            if self.mediator:
                self.mediator.Invoke('refreshCountDown', (GfxValue(self.countDown), GfxValue(True)))
        elif self.mediator:
            self.mediator.Invoke('refreshCountDown', (GfxValue(self.countDown), GfxValue(False)))
