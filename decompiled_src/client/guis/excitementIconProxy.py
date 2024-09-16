#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/excitementIconProxy.o
import BigWorld
import gameglobal
import ui
import const
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from asObject import ASUtils
from asObject import ASObject
from data import excitement_data as ED

class ExcitementIconProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExcitementIconProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemList = []
        self.itemState = {}
        self.showIconIdx = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EXCITEMENT_ICON:
            self.widget = widget
            self.initUI()

    def show(self):
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXCITEMENT_ICON)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXCITEMENT_ICON)
        self.widget = None

    def reset(self):
        self.itemList = []
        self.itemState = {}

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.refreshInfo()

    @ui.callAfterTime()
    def refreshInfo(self):
        if self.hasBaseData():
            self.genIconItem(self.showIconIdx)
            self.refreshIconInfo()
        if self.widget:
            if len(self.itemList) == 0:
                self.widget.indicator.visible = False
            else:
                self.widget.indicator.visible = True

    def genIconItem(self, itemIdx):
        self.showIconIdx = itemIdx
        p = BigWorld.player()
        curShowIds = p.getExcitementByLv()
        self.clearItems()
        if gameglobal.rds.configData.get('enableExcitementClientShow', False) and not p._isSoul() and not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            tmpState = {}
            for i, showId in enumerate(curShowIds):
                eData = ED.data.get(showId, {})
                serverProgressMsId = eData.get('serverEvent', 0)
                if serverProgressMsId and not p.checkServerProgress(serverProgressMsId, False):
                    continue
                item = self.widget.getInstByClsName('ExcitementIcon_Item')
                iconNum = eData.get('icon', None)
                stateTxt = ''
                if not p.checkAllCondition(showId, False):
                    stateTxt = eData.get('stateTxt1', '')
                else:
                    stateTxt = eData.get('stateTxt2', '')
                name = eData.get('name', '')
                if iconNum:
                    item.iconAppear.gotoAndPlay(0)
                    item.iconAppear.itemTxt.openStateMc.text = stateTxt
                    item.iconAppear.itemTxt.nameTxt.text = name
                    item.iconAppear.canvas.visible = True
                    item.iconAppear.canvas.fitSize = True
                    item.iconAppear.canvas.loadImage(uiConst.EXCITEMENT_IMPAGE_PATH % iconNum)
                    ASUtils.callbackAtFrame(item, 31, self.setItemInfo, item, name, stateTxt, iconNum)
                if i == itemIdx:
                    self.widget.content.addChild(item)
                if not p.checkAllCondition(showId, False):
                    tmpState[showId] = 'coming'
                else:
                    tmpState[showId] = 'open'
                    if self.itemState.get(showId, '') != 'open':
                        gameglobal.rds.sound.playSound(406)
                item.exId = showId
                self.itemList.append(item)

            self.itemState = tmpState

    def setItemInfo(self, *args):
        asObject = ASObject(args[3][0])
        item = asObject[0]
        name = asObject[1]
        stateTxt = asObject[2]
        iconNum = asObject[3]
        labels = (name, stateTxt)
        if self.widget and item.iconBtn:
            item.iconBtn.validateNow()
            item.iconBtn.labels = labels
            item.iconBtn.canvas.visible = True
            item.iconBtn.canvas.fitSize = True
            item.iconBtn.canvas.loadImage(uiConst.EXCITEMENT_IMPAGE_PATH % iconNum)

    def refreshIconInfo(self):
        self.widget.removeAllInst(self.widget.indicator)
        width = len(self.itemList) * 6 + 27
        self.widget.indicator.x = 69 - width / 2
        currentX = 0
        for i in range(len(self.itemList)):
            if i == self.showIconIdx:
                indicatorShow = self.widget.getInstByClsName('ExcitementIcon_Dadian')
                indicatorShow.x = currentX
                self.widget.indicator.addChildAt(indicatorShow, i)
                currentX += indicatorShow.width
            else:
                indicatorComm = self.widget.getInstByClsName('ExcitementIcon_Xiaodian')
                indicatorComm.x = currentX
                self.widget.indicator.addChildAt(indicatorComm, i)
                indicatorComm.index = i
                indicatorComm.addEventListener(events.MOUSE_CLICK, self.onClickCommBtn, False, 0, True)
                currentX += indicatorComm.width

    def onClickCommBtn(self, *arg):
        e = ASObject(arg[3][0]).target
        self.showIconIdx = e.index
        self.refreshInfo()

    def clearItems(self):
        self.widget.removeAllInst(self.widget.content)
        self.itemList = []

    def hasBaseData(self):
        if self.widget and gameglobal.rds.configData.get('enableExcitementClientShow', False):
            return True
        else:
            return False

    def _onIconBtnClick(self, e):
        t = e.target.parent
        pos = (self.widget.x + t.parent.x, self.widget.y + t.parent.y)
        gameglobal.rds.ui.excitementDetail.show(t.exId, pos)
