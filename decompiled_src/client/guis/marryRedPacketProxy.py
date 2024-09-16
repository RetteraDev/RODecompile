#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryRedPacketProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
import uiConst
import utils
import uiUtils
import const
import pinyinConvert
import events
import ui
from guis import richTextUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_config_data as MCD
from data import marriage_package_data as MPD
from cdata import marriage_subscribe_date_data as MSDD
from cdata import game_msg_def_data as GMDD
COUNT_BTN_NUM = 4

class MarryRedPacketProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryRedPacketProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_RED_PACKET, self.hide)

    def reset(self):
        self.selectedCountBtn = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_RED_PACKET:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_RED_PACKET)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_RED_PACKET)

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.widget.manBtn.targetType = 'man'
        self.widget.womanBtn.targetType = 'woman'

    def initState(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        ASUtils.setHitTestDisable(self.widget.titleName, True)
        redPacketNumList = MCD.data.get('redPacketNumList', (1, 2, 3, 4))
        for i, num in enumerate(redPacketNumList):
            btn = getattr(self.widget, 'countBtn' + str(i))
            if btn:
                btn.data = num
                btn.index = i
                btn.label = str(num)
                btn.addEventListener(events.BUTTON_CLICK, self.handleCountBtnClick, False, 0, True)

        self.widget.womanBtn.selected = True
        self.widget.blessWord.maxChars = 20
        DefaultRedPacketMsg = MCD.data.get('DefaultRedPacketMsg', '')
        self.widget.blessWord.defaultText = DefaultRedPacketMsg
        self.setCount(0)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.moneyTxt.text = self.getCurSelectedMoneyNum()

    def getCurSelectedMoneyNum(self):
        moneyUnit = MCD.data.get('redPacketMoneyUnit', 0)
        pNum = self.getCurCount()
        moneyNum = moneyUnit * pNum
        return moneyNum

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def setCount(self, index):
        if not self.hasBaseData():
            return
        if self.selectedCountBtn:
            self.selectedCountBtn.selected = False
        btn = getattr(self.widget, 'countBtn' + str(int(index)))
        if btn:
            self.selectedCountBtn = btn
            self.selectedCountBtn.selected = True
        self.refreshInfo()

    def handleCountBtnClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        self.setCount(t.index)

    def getCurTaretType(self):
        if self.hasBaseData():
            return self.widget.manBtn.group.selectedButton.targetType

    def getCurCount(self):
        if self.hasBaseData():
            return self.selectedCountBtn.data

    def getRedPacketData(self):
        return []

    @ui.checkInventoryLock()
    def _onPayBtnClick(self, e):
        p = BigWorld.player()
        pType = const.RED_PACKET_TYPE_MARRIAGE_HALL_COIN
        moneyUnit = MCD.data.get('redPacketMoneyUnit', 0)
        channel = const.CHAT_CHANNEL_MARRIAGE_HALL
        msg = self.getCustomMessage()
        tatGbIds, tgtNames = self.getTargetInfo()
        count = self.getCurCount()
        if not self.uiAdapter.marrySettingBg.tabooCheck(msg):
            p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        if richTextUtils.isSysRichTxt(msg):
            p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        if p.unbindCoin < moneyUnit * count:
            BigWorld.player().openRechargeFunc()
        else:
            p.base.addRedPacketBase(pType, moneyUnit * count, 1, channel, msg, [tatGbIds], [tgtNames], p.cipherOfPerson)
            self.hide()

    def getCustomMessage(self):
        if not self.hasBaseData():
            return ''
        if self.widget.blessWord.text:
            return self.widget.blessWord.text
        return self.widget.blessWord.defaultText

    def getCurMarriageType(self):
        p = BigWorld.player()
        if p.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL:
            return (p.marriageType, p.marriageSubType)
        else:
            marriageBeInvitedInfo = getattr(p, 'marriageBeInvitedInfo', None)
            if marriageBeInvitedInfo:
                return (marriageBeInvitedInfo.get('mType'), marriageBeInvitedInfo.get('subType'))
            return (0, 0)

    def getTargetInfo(self):
        p = BigWorld.player()
        targetType = self.getCurTaretType()
        marriageBeInvitedInfo = getattr(p, 'marriageBeInvitedInfo')
        gbId = 0
        name = ''
        if targetType == 'man':
            gbId = marriageBeInvitedInfo.get('hunsbandGbId', 0)
            name = marriageBeInvitedInfo.get('husbandName', '')
        elif targetType == 'woman':
            gbId = marriageBeInvitedInfo.get('wifeGbId', 0)
            name = marriageBeInvitedInfo.get('wifeName', '')
        return (gbId, name)
