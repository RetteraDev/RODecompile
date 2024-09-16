#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bottleProxy.o
from gamestrings import gameStrings
import gameglobal
import const
import BigWorld
from guis import uiConst
from guis import uiUtils
from item import Item
from uiProxy import UIProxy
from data import item_data as ID
from cdata import font_config_data as FCD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class BottleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BottleProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'clickConfirm': self.onClickConfirm,
         'clickActivity': self.onClickActivity}
        self.mediator = None
        self.pushId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOTTLE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BOTTLE:
            self.mediator = mediator

    def show(self):
        if not gameglobal.rds.configData.get('enableExpXiuWeiPool', False):
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_BOTTLEPROXY_36,))
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(self.pushId)
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOTTLE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOTTLE)

    def reset(self):
        self.mediator = None

    def onInitData(self, *args):
        ret = self.getData()
        return uiUtils.dict2GfxDict(ret, True)

    def getData(self):
        ret = {}
        p = BigWorld.player()
        activityItemId = SCD.data.get('XIU_WEI_ACTIVITY_ITEMID', 0)
        count = p.inv.countItemInPages(activityItemId, enableParentCheck=True)
        if count != 0:
            page, pos = p.inv.findItemInPages(activityItemId, enableParentCheck=True)
            item = p.inv.getQuickVal(page, pos)
            activityItemId = item.id
            count = '%d/1' % count
            ret['canActivity'] = True
        else:
            item = Item(activityItemId)
            count = "<font color = \'#FB0000\'>0/1</font>"
            ret['canActivity'] = False
        iconPath = uiUtils.getItemIconFile64(activityItemId)
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        useItemData = {'iconPath': iconPath,
         'itemId': activityItemId,
         'count': count,
         'color': color}
        ret['useItemData'] = useItemData
        ret['expXiuWeiPool'] = p.expXiuWeiPool
        ret['expXiuWeiTotal'] = p.expXiuWeiTotal
        currentExp = p.expXiuWeiTotal - p.expXiuWeiPool
        if currentExp < 0:
            currentExp = 0
        ret['currentExp'] = currentExp
        if p.expXiuWeiPool != -1 and p.expXiuWeiTotal != -1:
            ret['expDesc'] = gameStrings.TEXT_BOTTLEPROXY_87 % (currentExp, p.expXiuWeiTotal)
        else:
            ret['expDesc'] = ''
        if p.expXiuWeiPool != -1 and p.expXiuWeiTotal != -1:
            p.cell.getXiuWeiItemId()
        return ret

    def onClickConfirm(self, *args):
        BigWorld.player().cell.makeExpXiuWeiItem()

    def onClickActivity(self, *args):
        p = BigWorld.player()
        activityItemId = SCD.data.get('XIU_WEI_ACTIVITY_ITEMID', 0)
        page, pos = p.inv.findItemInPages(activityItemId, enableParentCheck=True)
        item = p.inv.getQuickVal(page, pos)
        if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
            p.onConfirmUseItem(item, page, pos)

    def refresh(self):
        ret = self.getData()
        if self.mediator:
            self.mediator.Invoke('setData', uiUtils.dict2GfxDict(ret, True))

    def notify(self):
        p = BigWorld.player()
        if p.expXiuWeiPool == 0:
            self.pushId = SCD.data.get('XIU_WEI_PUSHID', 0)
            gameglobal.rds.ui.pushMessage.addPushMsg(self.pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(self.pushId, {'click': self.show})

    def setItem(self, itemId):
        makeItemId = itemId
        iconPath = uiUtils.getItemIconFile64(makeItemId)
        quality = ID.data.get(makeItemId, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        makeItemData = {'iconPath': iconPath,
         'itemId': makeItemId,
         'count': 1,
         'color': color}
        if self.mediator:
            self.mediator.Invoke('setItemData', uiUtils.dict2GfxDict(makeItemData, True))
