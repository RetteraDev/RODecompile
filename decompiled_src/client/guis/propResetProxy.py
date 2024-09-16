#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/propResetProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
from uiProxy import UIProxy
from callbackHelper import Functor
from data import school_data as SD
from data import consumable_item_data as CID

class PropResetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PropResetProxy, self).__init__(uiAdapter)
        self.modelMap = {'getItemInfo': self.getItemInfo,
         'getLeftPropInfo': self.onGetLeftPropInfo,
         'dismiss': self.dismiss,
         'commit': self.onCommit}
        self.mediator = None
        self.resetMediator = None
        self.leftPointArray = []
        self.page = 0
        self.pos = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_PROP_RESET, self.closeWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def onGetLeftPropInfo(self, *args):
        p = BigWorld.player()
        data = SD.data.get(p.school)
        if not data:
            return False
        curScheme = p.getPropSchemeById(p.curPropScheme)
        pointList = curScheme['scheme']
        minList = data.get('point', (0, 0, 0, 0, 0, 0))
        self.leftPointArray = []
        textArray = []
        for i in xrange(0, 5):
            leftPoint = pointList[i] - minList[i + 1]
            self.leftPointArray.append(leftPoint)
            textArray.append(gameStrings.TEXT_PROPRESETPROXY_53 % leftPoint)

        return uiUtils.array2GfxAarry(textArray, True)

    def getItemInfo(self, *args):
        path = uiUtils.getItemIconFile64(self.itemId)
        allNum = 0
        p = BigWorld.player()
        allList = p.inv.findAllItemInPages(self.itemId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True, False, False, False)
        for pg, ps in allList:
            cit = p.inv.getQuickVal(pg, ps)
            if not cit.isExpireTTL() and not cit.hasLatch():
                allNum += cit.cwrap

        name = uiUtils.getItemColorName(self.itemId)
        color = uiUtils.getItemColor(self.itemId)
        resetPoint = CID.data.get(self.itemId).get('resetPropVal', 0)
        item = [name,
         path,
         color,
         '%d/1' % allNum,
         self.itemId,
         resetPoint]
        return uiUtils.array2GfxAarry(item, True)

    def closeWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PROP_RESET)
        self.mediator = None

    def onCommit(self, *args):
        idx = int(args[3][0].GetNumber())
        resetPoint = CID.data.get(self.itemId).get('resetPropVal', 0)
        if self.leftPointArray[idx] < resetPoint:
            msg = gameStrings.TEXT_PROPRESETPROXY_81 % (resetPoint, self.leftPointArray[idx])
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onTrueCommit, idx), yesBtnText=gameStrings.TEXT_PROPRESETPROXY_82, noCallback=None, noBtnText=gameStrings.TEXT_PROPRESETPROXY_82_1)
        else:
            self.onTrueCommit(idx)

    def onTrueCommit(self, idx):
        propList = [11000,
         11001,
         11002,
         11003,
         11004]
        BigWorld.player().cell.useResetPropItem(const.RES_KIND_INV, self.page, self.pos, propList[idx])
        self.closeWidget()

    def dismiss(self, *args):
        self.closeWidget()

    def show(self, itemId, page, pos):
        self.itemId = itemId
        self.page = page
        self.pos = pos
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PROP_RESET, True)
