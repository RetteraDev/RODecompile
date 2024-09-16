#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryReceiveRedPacketProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_config_data as MCD
NEED_FIX_NUM = 12
FIX_NUM = 2

class MarryReceiveRedPacketProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryReceiveRedPacketProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.tgtType = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_RECEIVE_RED_PACKET:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_RECEIVE_RED_PACKET)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_RECEIVE_RED_PACKET)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.list.itemRenderer = 'MarryReceiveRedPacket_Item'
        self.widget.list.lableFunction = self.listItemFunction
        self.widget.list.itemHeight = 28
        self.widget.list.itemWidth = 323
        self.widget.list.dataArray = []

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.widget.list.dataArray = self.getListData()

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def listItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            if info.isEmpty:
                itemMc.roleNameTxt.visible = False
                itemMc.numTxt.visible = False
                itemMc.receiveBtn.visible = False
                itemMc.alreadyTxt.visible = False
                itemMc.expireTxt.visible = False
                itemMc.tianbiIcon.visible = False
            else:
                itemMc.roleNameTxt.visible = True
                itemMc.numTxt.visible = True
                itemMc.tianbiIcon.visible = True
                itemMc.roleNameTxt.text = info.roleName
                itemMc.numTxt.text = info.money
                if info.receiveType == uiConst.RECEIVE_TYPE_ACCESS:
                    itemMc.receiveBtn.visible = True
                    itemMc.alreadyTxt.visible = False
                    itemMc.expireTxt.visible = False
                elif info.receiveType == uiConst.RECEIVE_TYPE_GOT:
                    itemMc.receiveBtn.visible = False
                    itemMc.alreadyTxt.visible = True
                    itemMc.expireTxt.visible = False
                elif info.receiveType == uiConst.RECEIVE_TYPE_EXPIRED:
                    itemMc.receiveBtn.visible = False
                    itemMc.alreadyTxt.visible = False
                    itemMc.expireTxt.visible = True
                itemMc.sn = info.serinalNum
                itemMc.msg = info.msg
                itemMc.money = info.money
                itemMc.receiveBtn.addEventListener(events.BUTTON_CLICK, self.handleReceiveBtnClick, False, 0, True)

    def getListData(self):
        p = BigWorld.player()
        dataArray = []
        marriageRedPacketInfo = getattr(p, 'marriageRedPacketInfo', [])
        for i, rList in enumerate(marriageRedPacketInfo):
            serinalNum, money, msg, srcName, receiveType = rList
            info = {'serinalNum': serinalNum,
             'money': money,
             'msg': msg,
             'roleName': srcName,
             'receiveType': receiveType,
             'isEmpty': False}
            if receiveType == uiConst.RECEIVE_TYPE_ACCESS:
                dataArray.insert(0, info)
            else:
                dataArray.append(info)

        if len(dataArray) >= NEED_FIX_NUM:
            info = {'serinalNum': 0,
             'money': 0,
             'msg': '',
             'roleName': '',
             'receiveType': 0,
             'isEmpty': True}
            for i in xrange(0, FIX_NUM):
                dataArray.append(info)

        return dataArray

    def handleReceiveBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            p = BigWorld.player()
            p.base.getRedPacket(t.parent.sn, const.RED_PACKET_TYPE_MARRIAGE_HALL_COIN, t.parent.msg, t.parent.money)
