#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityGuideIconProxy.o
import BigWorld
import gameglobal
import const
import events
import gameconfigCommon
from guis.uiProxy import UIProxy
from guis import uiConst
from asObject import ASUtils
from asObject import ASObject
from data import activity_guide_entry_data as AGED
from data import sys_config_data as SCD

class ActivityGuideIconProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityGuideIconProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.itemList = []
        self.showIconIdx = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTIVITY_GUIDE_ICON:
            self.widget = widget
            self.initUI()

    def show(self):
        if not gameconfigCommon.enableActivityGuide():
            return
        if BigWorld.player()._isSoul() or BigWorld.player().mapID != const.SPACE_NO_BIG_WORLD:
            return
        self.uiAdapter.activityGuide.genActivityMap()
        keyList = AGED.data.keys()
        keyList.sort(cmp=lambda a, b: cmp(AGED.data[a].get('sortOrder', 0), AGED.data[b].get('sortOrder', 0)))
        self.itemList = [ keyId for keyId in keyList if self.uiAdapter.activityGuide.getMainTabKeyList(keyId) ]
        if not self.itemList:
            return
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVITY_GUIDE_ICON)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVITY_GUIDE_ICON)
        self.widget = None

    def reset(self):
        self.itemList = []
        self.showIconIdx = 0
        self.timer = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.uiAdapter.activityGuide.genActivityMap()

    def initState(self):
        self.refreshInfo()

    def timerFun(self):
        if not self.widget:
            return
        if not SCD.data.get('activityGuideIconTimer', 0):
            return
        if not self.itemList:
            return
        self.showIconIdx = (self.showIconIdx + 1) % len(self.itemList)
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            self.genIconItem(self.showIconIdx)
            self.refreshIconInfo()
            if SCD.data.get('activityGuideIconTimer', 0) and len(self.itemList) > 1:
                if self.timer:
                    BigWorld.cancelCallback(self.timer)
                self.timer = BigWorld.callback(SCD.data.get('activityGuideIconTimer', 0), self.timerFun)

    def genIconItem(self, itemIdx):
        self.showIconIdx = itemIdx
        p = BigWorld.player()
        self.clearItems()
        if gameglobal.rds.configData.get('enableActivityGuide', False) and not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            for i, showId in enumerate(self.itemList):
                if i == itemIdx:
                    eData = AGED.data.get(showId, {})
                    item = self.widget.content.getChildAt(0)
                    icon = eData.get('icon', None)
                    stateTxt = eData.get('mainTitleIconName', '')
                    item.iconAppear.visible = True
                    item.iconAppear.gotoAndPlay(1)
                    item.iconAppear.itemTxt.textField.text = stateTxt
                    item.iconAppear.canvas.visible = True
                    item.iconAppear.canvas.fitSize = True
                    item.iconAppear.canvas.loadImage(uiConst.ACTIVITY_GUIDE_ICON_PATH % icon)
                    item.iconBtn.visible = False
                    item.iconBtn.stateTxt = stateTxt
                    item.iconBtn.label = stateTxt
                    item.iconBtn.textField.text = stateTxt
                    item.iconBtn.canvas.visible = True
                    item.iconBtn.canvas.fitSize = True
                    item.iconBtn.canvas.loadImage(uiConst.ACTIVITY_GUIDE_ICON_PATH % icon)
                    ASUtils.callbackAtFrame(item.iconAppear, 30, self.setItemInfo, item, stateTxt, icon)
                    item.exId = showId

    def setItemInfo(self, *args):
        asObject = ASObject(args[3][0])
        item = asObject[0]
        stateTxt = asObject[1]
        icon = asObject[2]
        if self.widget and item.iconBtn:
            item.iconAppear.visible = False
            item.iconBtn.visible = True

    def refreshIconInfo(self):
        self.widget.removeAllInst(self.widget.indicator)
        if len(self.itemList) <= 1:
            return
        self.widget.indicator.x = 246 / 2.0 - (26 * len(self.itemList) + 6 * (len(self.itemList) - 1)) / 2.0
        currentX = 0
        for i in range(len(self.itemList)):
            if i == self.showIconIdx:
                indicatorShow = self.widget.getInstByClsName('ActivityGuideIcon_Dadian')
                indicatorShow.x = currentX
                self.widget.indicator.addChildAt(indicatorShow, i)
                currentX += indicatorShow.width + 2
            else:
                indicatorComm = self.widget.getInstByClsName('ActivityGuideIcon_Xiaodian')
                indicatorComm.x = currentX
                indicatorComm.y = 1
                self.widget.indicator.addChildAt(indicatorComm, i)
                indicatorComm.index = i
                indicatorComm.addEventListener(events.MOUSE_CLICK, self.onClickCommBtn, False, 0, True)
                currentX += indicatorComm.width + 2

    def onClickCommBtn(self, *arg):
        e = ASObject(arg[3][0]).target
        self.showIconIdx = e.index
        self.refreshInfo()

    def clearItems(self):
        pass

    def hasBaseData(self):
        if self.widget and gameglobal.rds.configData.get('enableActivityGuide', False):
            return True
        else:
            return False

    def _onIconBtnClick(self, e):
        self.uiAdapter.activityGuide.show(self.itemList[self.showIconIdx])
