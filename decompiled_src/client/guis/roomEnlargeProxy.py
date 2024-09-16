#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roomEnlargeProxy.o
import BigWorld
import gameglobal
import gametypes
from uiProxy import UIProxy
from guis import uiConst
from guis import events
from guis.asObject import ASObject
from helpers import cgPlayer
from guis import uiUtils
from data import sys_config_data as SCD
from data import fitting_room_upgrade_data as FRUD
from data import enlarge_room_data as ERD
from data import home_data as HD
from cdata import game_msg_def_data as GMDD
ROOM_ENLARGE_PATH_PREFIX = 'jiayuan/%s.dds'

class RoomEnlargeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoomEnlargeProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_ROOM_ENLARGE, self.hide)
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ROOM_ENLARGE:
            self.widget = widget
            self.initRoomData()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ROOM_ENLARGE)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_ROOM_ENLARGE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.addEventListener(events.MOUSE_CLICK, self.handleClickHelp, False, 0, True)
        self.widget.button0.addEventListener(events.MOUSE_CLICK, self.handleClickButton, False, 0, True)
        self.widget.button1.addEventListener(events.MOUSE_CLICK, self.handleClickButton, False, 0, True)
        self.widget.playBtn.addEventListener(events.MOUSE_CLICK, self.starPlayMovie, False, 0, True)
        self.widget.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleBuyRoom, False, 0, True)
        self.widget.roomName.text = ''
        self.widget.descScrollWnd.canvas.descTex.text = ''
        for buttonName, info in self.roomData.iteritems():
            if not info.data:
                pass
            else:
                mc = getattr(self.widget, buttonName, None)
                if info.icon:
                    self.loadIcon(mc.canvas.icon, info.iconPath)
                if info.movieIcon:
                    self.loadIcon(self.widget.photoBg.icon, info.movieIconPath, True)
                if not self.selectedButton and mc:
                    self.selectedButton = mc
                    self.selectedButton.selected = True

        self.refreshInfo()

    def refreshInfo(self):
        self.onMovieEnd()
        if self.selectedButton:
            widget = self.widget
            roomData = self.getRoomData()
            widget.roomName.text = roomData.roomName
            widget.descScrollWnd.canvas.descTex.text = roomData.desc
            widget.descScrollWnd.refreshHeight()
            if roomData.movieIcon:
                self.loadIcon(self.widget.photoBg.icon, roomData.movieIconPath, True)

    def getRoomData(self):
        if self.selectedButton:
            return self.getRoomDataFromBtnName(self.selectedButton.name)
        else:
            return None

    def getRoomDataFromBtnName(self, btnName):
        roomData = self.roomData.get(btnName, None)
        return roomData

    def handleClickHelp(self, *args):
        gameglobal.rds.ui.help.show(SCD.data.get('DESC_HELP_FOR_ROOM_ENLARGE', ''))

    def handleClickButton(self, *arg):
        e = ASObject(arg[3][0])
        roomData = self.getRoomDataFromBtnName(e.target.name)
        if not roomData.data:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.NO_ENLARGE_ROOM, ())
            return
        if self.selectedButton:
            self.selectedButton.selected = False
        self.selectedButton = e.target
        self.selectedButton.selected = True
        self.refreshInfo()

    def loadIcon(self, mc, iconName, fitSize = False):
        mc.fitSize = fitSize
        mc.loadImage(iconName)

    def starPlayMovie(self, *args):
        roomData = self.getRoomData()
        if roomData:
            self.widget.playBtn.visible = False
            self.widget.photoBg.visible = False
            self.playMovie(roomData.movie)

    def reset(self):
        self.selectedButton = None
        self.roomData = {}
        self.cgPlayer = None

    def initRoomData(self):
        self.roomData['button0'] = FittingRoomData()
        self.roomData['button1'] = EnlargeRoomData()

    def playMovie(self, movieName):
        w = 270
        h = 150
        x = 1
        y = 1
        z = 1.0
        config = {'position': (x, y, z),
         'w': w,
         'h': h,
         'loop': False,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/RoomEnlargeWidget' + self.uiAdapter.getUIExt(), 'RoomEnlarge_Photo', 270, 150)
        self.cgPlayer.playMovie(movieName, config)

    def onMovieEnd(self):
        if self.widget:
            self.widget.playBtn.visible = True
            self.widget.photoBg.visible = True
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None

    def handleBuyRoom(self, *arg):
        roomData = self.getRoomData()
        if roomData:
            roomData.buyRoom()

    def enlargeRoomSuccess(self):
        if not self.widget:
            return
        roomData = self.getRoomData()
        if roomData:
            newData = roomData.initData()
            roomData.init(newData)
            if roomData.icon and self.selectedButton:
                self.loadIcon(self.selectedButton.canvas.icon, roomData.iconPath)
        self.refreshInfo()


class RoomData(object):

    def __init__(self, data = {}):
        data = self.initData()
        self.init(data)
        self.confirmMsg = ''

    def init(self, data = {}):
        self.movie = data.get('movie', '')
        self.icon = data.get('icon', '')
        self.desc = data.get('desc', '')
        self.roomName = data.get('roomName', '')
        self.movieIcon = data.get('movieIcon', '')
        self.data = data

    def initData(self):
        return {}

    def checkCanBuy(self):
        return True

    def buyRoom(self):
        if not self.checkCanBuy():
            return
        else:
            p = BigWorld.player()
            data = self.data
            expandCashNeed = data.get('expandCashNeed', 0) or data.get('cashNeed', 0)
            expandItemNeed = data.get('expandItemNeed', []) or data.get('itemNeed', [])
            itemData = {}
            needNum = 0
            count = 0
            if expandItemNeed:
                itemId, needNum = expandItemNeed[0]
                if itemId:
                    itemData = uiUtils.getGfxItemById(itemId)
                    count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST)
                    itemData['count'] = uiUtils.convertNumStr(count, needNum)
            yesBtnEnable = False
            if p.cash + p.bindCash >= expandCashNeed and itemData and count >= needNum:
                yesBtnEnable = True
            cashStr = uiUtils.convertNumStr(p.cash + p.bindCash, expandCashNeed, showOwnStr=False)
            bonusIcon = {'bonusType': 'bindCash',
             'value': str(cashStr)}
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(self.confirmMsg, self.confirmBuyRoom, itemData=itemData, bonusIcon=bonusIcon, yesBtnEnable=yesBtnEnable, style=uiConst.MSG_BOX_BUY_ITEM, noCallback=None)
            return

    @property
    def iconPath(self):
        if self.icon:
            return ROOM_ENLARGE_PATH_PREFIX % self.icon
        return ''

    @property
    def movieIconPath(self):
        if self.movieIcon:
            return ROOM_ENLARGE_PATH_PREFIX % self.movieIcon
        return ''

    def confirmBuyRoom(self):
        pass


class FittingRoomData(RoomData):

    def __init__(self):
        super(FittingRoomData, self).__init__()
        self.confirmMsg = SCD.data.get('MSG_FOR_BUY_FITTING_ROOM', '')

    def initData(self):
        p = BigWorld.player()
        ud = FRUD.data.get((p.myHome.roomId, p.myHome.fittingRoomLv), {})
        return ud

    def confirmBuyRoom(self):
        p = BigWorld.player()
        p.confirmEnlarageFittingRoom()

    def checkCanBuy(self):
        p = BigWorld.player()
        data = self.data
        if not data:
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_FORBIDDEN, ())
            return False
        if data.get('topLevel', 0):
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_MAX_LV, ())
            return False
        expandCashNeed = data.get('expandCashNeed', 0)
        expandItemNeed = data.get('expandItemNeed', [])
        if not expandCashNeed and not expandItemNeed:
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_FORBIDDEN, ())
            return False
        return True


class EnlargeRoomData(RoomData):

    def __init__(self):
        super(EnlargeRoomData, self).__init__()
        self.confirmMsg = SCD.data.get('MSG_FOR_ENLARGE_ROOM', '')

    def initData(self):
        p = BigWorld.player()
        hd = HD.data.get(p.myHome.roomId, {})
        enlargeRoomId = hd.get('enlargeRoomId', 0)
        erd = ERD.data.get(enlargeRoomId, {})
        return erd

    def confirmBuyRoom(self):
        p = BigWorld.player()
        p.cell.enlargeHomeRoom()

    def checkCanBuy(self):
        p = BigWorld.player()
        data = self.data
        if not data:
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_FORBIDDEN, ())
            return False
        hd = HD.data.get(p.myHome.roomId, {})
        enlargeRoomId = hd.get('enlargeRoomId', 0)
        if enlargeRoomId in p.myHome.erooms:
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_HAVE_BEEN_BOUGHT, ())
            return False
        expandCashNeed = data.get('cashNeed', 0)
        expandItemNeed = data.get('itemNeed', [])
        if not expandCashNeed and not expandItemNeed:
            p.showGameMsg(GMDD.data.ENLARGE_ROOM_MAX_LV, ())
            return False
        return True
