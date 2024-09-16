#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hobbyPreSaleCheckProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
from uiProxy import UIProxy
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import hobby_presale_schedule_data as HPSD
from data import hobby_presale_config_data as HPCD
RESERVED_MAX_NUM = 3

class HobbyPreSaleCheckProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HobbyPreSaleCheckProxy, self).__init__(uiAdapter)
        self.widget = None
        self.hobbyReservedList = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOBBY_PRESALE_CHECK, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HOBBY_PRESALE_CHECK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOBBY_PRESALE_CHECK)

    def reset(self):
        self.hobbyReservedList = []

    def show(self, hobbyReservedList):
        self.hobbyReservedList = self.changeCoding(hobbyReservedList or [])
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_HOBBY_PRESALE_CHECK)

    def initUI(self):
        self.widget.confirm.addEventListener(events.MOUSE_CLICK, self.handleCloseClick, False, 0, True)
        self.widget.linkToShop.htmlText = HPCD.data.get('successGuide', {})

    def refreshInfo(self):
        if not self.widget:
            return
        for i in range(RESERVED_MAX_NUM):
            orderInfo = self.widget.getChildByName('orderInfo%d' % i)
            if i < len(self.hobbyReservedList):
                tInfo = self.hobbyReservedList[i]
                orderInfo.visible = True
                orderInfo.orderName.text = gameStrings.HOBBY_PRESALE_RESERVE_CODE % HPSD.data.get(tInfo.get('itemId', 0), {}).get('name', '')
                orderInfo.orderCode.text = tInfo.get('code', '')
                orderInfo.copyCode.codeInfo = tInfo.get('code', '')
                orderInfo.copyCode.addEventListener(events.MOUSE_CLICK, self.handleCopyClick, False, 0, True)
                orderInfo.effectDate.text = gameStrings.HOBBY_PRESALE_TIME_LIMIT % HPSD.data.get(tInfo.get('itemId', 0), {}).get('validTime', '')
            else:
                orderInfo.visible = False

    def handleCopyClick(self, *args):
        e = ASObject(args[3][0])
        codeText = e.currentTarget.codeInfo
        BigWorld.setClipBoardText(codeText)

    def handleCloseClick(self, *args):
        self.hide()

    def changeCoding(self, hobbyReservedList):
        changeArgs = []
        for v in hobbyReservedList:
            map = {}
            for key in v:
                value = v[key]
                if isinstance(key, unicode):
                    key = key.encode(utils.defaultEncoding())
                if isinstance(value, unicode):
                    value = value.encode(utils.defaultEncoding())
                map[key] = value

            changeArgs.append(map)

        return changeArgs
