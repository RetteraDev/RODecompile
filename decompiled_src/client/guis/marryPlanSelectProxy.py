#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryPlanSelectProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import pinyinConvert
import events
from ui import gbk2unicode
from helpers import cgPlayer
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from data import marriage_plan_data as MPD
BUTTON_NUM = 3

class MarryPlanSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryPlanSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_PLAN_SELECT, self.hide)

    def reset(self):
        self.selectedBtn = None
        self.cgPlayer = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_PLAN_SELECT:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.onMovieEnd()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_PLAN_SELECT)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_PLAN_SELECT)

    def initUI(self):
        self.initData()
        self.initSate()

    def initData(self):
        pass

    def initSate(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in xrange(0, BUTTON_NUM):
            btn = getattr(self.widget, 'button' + str(i))
            if btn:
                btn.data = i
                btn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
                pData = MPD.data.get(i + 1, {})
                if pData:
                    btn.canvas.icon.fitSize = True
                    btn.canvas.icon.loadImage(uiConst.MARRY_RES_DIR + pData.get('iconPath', '') + '.dds')

        self.widget.button1.enabled = gameglobal.rds.configData.get('enableMarriageGreat', False)
        self.widget.button2.enabled = False
        self.widget.playBtn.addEventListener(events.MOUSE_CLICK, self.starPlayMovie, False, 0, True)
        self.setSelIndex(0)

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.onMovieEnd()
        self.refreshDescList()

    def _onBuyBtnClick(self, e):
        if not self.hasBaseData():
            return
        self.selectMarryType = 0
        marriageType = self.getCurMarriageType()
        if marriageType == gametypes.MARRIAGE_TYPE_PACKAGE:
            self.uiAdapter.MarryPlanOrder.show()
            self.hide()
        elif marriageType == gametypes.MARRIAGE_TYPE_GREAT:
            self.selectMarryType = 3
            self.uiAdapter.MarryPlanOrder.show()
            self.hide()
        elif marriageType == gametypes.MARRIAGE_TYPE_HIDE:
            p = BigWorld.player()
            p.cell.subscribeHideMarriageDone()

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def setSelIndex(self, index):
        if not self.hasBaseData():
            return
        if self.selectedBtn:
            self.selectedBtn.selected = False
        btn = getattr(self.widget, 'button' + str(int(index)))
        if btn:
            self.selectedBtn = btn
            self.selectedBtn.selected = True
        self.refreshInfo()

    def refreshDescList(self):
        if not self.hasBaseData():
            return
        if not self.selectedBtn:
            return
        pData = MPD.data.get(self.getCurSelecType(), {})
        self.widget.roomName.text = gameStrings.MARRY_LABEL[self.getCurSelecType() - 1]
        self.widget.descScrollWnd.canvas.descTex.htmlText = pData.get('desc', '')
        showItems = pData.get('showItems', ())
        self.widget.removeAllInst(self.widget.descScrollWnd.canvas.itemMc)
        y = self.widget.descScrollWnd.canvas.title.height + self.widget.descScrollWnd.canvas.descTex.textHeight + 20
        self.widget.descScrollWnd.canvas.itemMc.y = y
        for i, itemId in enumerate(showItems):
            item = self.widget.getInstByClsName('MarryPlanSelect_ItemEx')
            if item:
                gfxItem = uiUtils.getGfxItemById(itemId)
                item.item.setItemSlotData(gfxItem)
                item.x = i * 49
                item.y = 0
                item.item.dragable = False
                self.widget.descScrollWnd.canvas.itemMc.addChild(item)

    def handleBtnClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        self.setSelIndex(t.data)

    def getCurMarriageType(self):
        if not self.hasBaseData():
            return
        if not self.selectedBtn:
            return
        marriageType = self.getCurSelecType()
        return marriageType

    def starPlayMovie(self, *args):
        movieName = self.getCurMovieName()
        if movieName:
            self.widget.playBtn.visible = False
            self.widget.photoBg.visible = False
            self.playMovie(movieName)

    def getCurSelecType(self):
        if self.selectedBtn:
            return int(self.selectedBtn.data) + 1

    def getCurMovieName(self):
        pData = MPD.data.get(self.getCurSelecType(), {})
        return pData.get('moivePath', '')

    def playMovie(self, movieName):
        w = 328
        h = 196
        x = 1
        y = 1
        z = 1
        config = {'position': (x, y, z),
         'w': w,
         'h': h,
         'loop': False,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/MarryPlanSelectWidget' + self.uiAdapter.getUIExt(), 'MarryPlanSelect_Photo', 328, 196)
        self.cgPlayer.playMovie(movieName, config)

    def onMovieEnd(self):
        if self.widget:
            self.widget.playBtn.visible = True
            self.widget.photoBg.visible = True
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None
