#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityReSignInProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from guis import uiUtils
from guis import uiConst
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import activity_resignin_config_data as ARCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import activity_signin_type_data as ASTD
SIGN_IN_TYPE_NORNAL = 0
SIGN_IN_TYPE_FENWEI = 1

class ActivityReSignInProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityReSignInProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickCancel': self.onClickCancel,
         'clickConfirm': self.onClickConfirm,
         'getInfo': self.onGetInfo}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_RESIGNIN, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVITY_RESIGNIN:
            self.mediator = mediator

    def show(self, canResignCnt = 0, isNewSignIn = False, activityId = 0):
        if isNewSignIn:
            self.activityId = activityId
        else:
            self.activityId = uiUtils.getActivitySignId()
        if not self.activityId:
            return
        self.canResignCnt = canResignCnt
        self.isNewSignIn = isNewSignIn
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVITY_RESIGNIN)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVITY_RESIGNIN)

    def reset(self):
        self.mediator = None
        self.canResignCnt = 0
        self.activityId = 0
        self.isClickConfirm = False
        self.isNewSignIn = False

    def onGetInfo(self, *args):
        ret = self._getInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def _getInfo(self):
        p = BigWorld.player()
        ret = {}
        resign = ARCD.data.get(self.activityId, {})
        resignItemId = resign.get('reSignInItemId', 0)
        reSignInItemCnt = resign.get('reSignInItemCnt', {})
        newSignInInfo = getattr(p, 'newSignInInfo', {}).get(self.activityId, {})
        resignCnt = getattr(newSignInInfo, 'resignCnt', 0)
        allItemCount = p.inv.countItemInPages(resignItemId, enableParentCheck=True)
        needItemCount = reSignInItemCnt.get(resignCnt + 1, 2)
        icon = {}
        if resignItemId:
            icon['iconPath'] = uiUtils.getItemIconFile64(resignItemId)
            if allItemCount < needItemCount:
                icon['count'] = "<font color=\'#ff0000\'>" + str(allItemCount) + '/' + str(needItemCount) + '</font>'
                ret['enbaled'] = False
            else:
                icon['count'] = str(allItemCount) + '/' + str(needItemCount)
            icon['itemId'] = resignItemId
        if self.isNewSignIn:
            data = ASTD.data.get(self.activityId, {})
            msg = data.get('resignWidgetDesc', gameStrings.TEXT_ACTIVITYRESIGNINPROXY_86)
            ret['title'] = data.get('reSignInDesc', gameStrings.NEW_SIGNIN_RESIGN_DESC)
        else:
            msg = GMD.data.get(GMDD.data.RESIGNIN_ITEM_COST, {}).get('text', gameStrings.TEXT_ACTIVITYRESIGNINPROXY_86)
            ret['title'] = gameStrings.NEW_SIGNIN_RESIGN_DESC
        ret['resignDesc'] = msg
        if self.canResignCnt <= 0:
            ret['enbaled'] = False
        ret['icon'] = icon
        return ret

    def onClickCancel(self, *args):
        self.hide()

    def onClickConfirm(self, *args):
        self.isClickConfirm = True
        p = BigWorld.player()
        data = ASTD.data.get(self.activityId, {})
        if data and data.get('activityType') == SIGN_IN_TYPE_FENWEI:
            p.cell.applyActivityReSignIn(self.activityId)
        elif data and data.get('activityType') == SIGN_IN_TYPE_NORNAL:
            p.cell.applyReSignInRewardV2(self.activityId)

    def refresh(self):
        if self.mediator:
            self.canResignCnt -= 1
            self.mediator.Invoke('refresh', uiUtils.dict2GfxDict(self._getInfo(), True))
            self.isClickConfirm = False
            if self.canResignCnt == 0:
                self.hide()
