#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/uiSurveyProxy.o
from guis import uiConst
from guis.uiProxy import UIProxy
from guis import events
from guis import asObject
from guis.asObject import ASUtils
from callbackHelper import Functor
import gameglobal
import BigWorld
import formula

class UISurveyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UISurveyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.selectBtn = 1
        self.selectPic = 0
        self.initHeight = 0
        self.sceneList = []
        self.bg = None
        self.selectPos = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == SURVEY_WIDGET_ID:
            self.widget = widget
            self.initHeight = self.widget.height
            self.initUI()

    def clearWidget(self):
        if self.bg and self.bg.parent:
            self.bg.parent.removeChild(self.bg)
        self.widget = None
        self.uiAdapter.unLoadWidget(SURVEY_WIDGET_ID)
        self.uiAdapter.initHud()

    def show(self):
        self.uiAdapter.loadWidget(SURVEY_WIDGET_ID)

    def initUI(self):
        self.widget.stage.addEventListener(events.EVENT_RESIZE, self.bgLoadComp)
        self.widget.addEventListener(events.BUTTON_CLICK, self.btnClick)
        self.icon = self.widget.getInstByClsName('com.scaleform.mmo.core.component.SwfLoader')
        self.widget.addChild(self.icon)
        self.icon.setCallback(self.iconLoadComp)
        self.bg = self.widget.getInstByClsName('com.scaleform.mmo.core.component.SwfLoader')
        ASUtils.setHitTestDisable(self.bg, True)
        self.bg.setCallback(self.bgLoadComp)
        for x in xrange(4):
            btn = self.widget.getChildByName('btn%s' % (x + 1))
            btn.groupName = 'uiSurvey'
            btn.toggle = True
            btn.data = x + 1
            btn.selected = self.selectBtn == x + 1

        for x in xrange(10):
            btn = self.widget.getChildByName('pic%s' % (x + 1))
            btn.groupName = 'uiSurveyPic'
            btn.toggle = True
            btn.data = x + 1
            btn.selected = self.selectPic == x + 1

        self.sceneList = [{'label': '最暗1',
          'data': 1,
          'pos': (414, 4, -304),
          'fbNo': 1501,
          'pitch': 0.084,
          'yaw': 0.888},
         {'label': '最暗2',
          'data': 1,
          'pos': (448, 16, -208),
          'fbNo': 1501,
          'pitch': -0.186,
          'yaw': 0.834},
         {'label': '最亮1',
          'data': 1,
          'pos': (270, 14, -92),
          'fbNo': 1501,
          'pitch': -1.306,
          'yaw': -2.1},
         {'label': '最亮2',
          'data': 2,
          'pos': (-297, 159, -203),
          'lineNo': 120,
          'pitch': 0.049,
          'yaw': -1.527}]
        ASUtils.setDropdownMenuData(self.widget.sceneMenu, self.sceneList)
        self.widget.sceneMenu.addEventListener(events.INDEX_CHANGE, self.hanelSelectPos)
        self.bg.load('widgets/uiSurvey/0.swf')
        self.uiAdapter.unLoadAllWidget([SURVEY_WIDGET_ID])
        self.widget.sceneMenu.selectedIndex = 3
        self.hanelSelectPos()

    def iconLoadComp(self, *args):
        self.icon.x = (self.widget.stage.stageWidth - self.icon.width) / 2 - self.widget.x
        self.icon.y = (self.widget.stage.stageHeight - self.icon.height) / 2 - self.widget.y
        self.icon.y = max(self.icon.y, self.initHeight + 20)

    def bgLoadComp(self, *args):
        self.bg.width = self.widget.stage.stageWidth
        self.bg.height = self.widget.stage.stageHeight
        self.widget.stage.addChildAt(self.bg, 0)

    def btnClick(self, *args):
        e = asObject.ASObject(args[3][0])
        name = e.target.name
        needRefresh = False
        if name.startswith('btn'):
            self.selectBtn = int(e.target.data)
            needRefresh = True
        elif name.startswith('pic'):
            self.selectPic = int(e.target.data)
            needRefresh = True
        if needRefresh:
            if e.target.selected:
                self.icon.visible = True
                self.icon.load('widgets/uiSurvey/%s-%s.swf' % (self.selectBtn, self.selectPic))
            else:
                self.icon.visible = False
            self.uiAdapter.unLoadAllWidget([SURVEY_WIDGET_ID], True)

    def hanelSelectPos(self, *args):
        self.selectPos = self.sceneList[self.widget.sceneMenu.selectedIndex]
        p = BigWorld.player()
        msgs = []
        if self.selectPos.get('fbNo', 0):
            if p.mapID != self.selectPos['fbNo']:
                msgs.append('$createfuben %s 1' % self.selectPos['fbNo'])
        elif self.selectPos.get('lineNo'):
            if formula.spaceInFuben(p.spaceNo):
                msgs.append('$leavefuben')
            if p.mapID != self.selectPos['lineNo']:
                msgs.append('$enterLine 0 %s' % (self.selectPos['lineNo'] + 1))
        msgs.append('$goto %s %s %s' % self.selectPos['pos'])
        self.executmgs(msgs)

    def executmgs(self, msgs = None):
        if not msgs:
            return
        BigWorld.player().cell.adminOnCell(msgs[0])
        if len(msgs) > 1:
            BigWorld.callback(5, Functor(self.executmgs, msgs[1:]))
        else:
            if self.selectPos.get('lineNo'):
                gameglobal.rds.ui.skill.enterWingFly()
            self.refreshPosition()
            BigWorld.callback(5, self.refreshPosition)

    def refreshPosition(self):
        BigWorld.dcursor().pitch = self.selectPos['pitch']
        BigWorld.dcursor().yaw = self.selectPos['yaw']
        self.uiAdapter.unLoadAllWidget([SURVEY_WIDGET_ID], True)


if not hasattr(gameglobal.rds.ui, 'uiSurvey'):
    gameglobal.rds.ui.uiSurvey = UISurveyProxy(gameglobal.rds.ui)
    SURVEY_WIDGET_ID = 30000
    uiConst.FUBEN_FILTER_WIDGETS.append(SURVEY_WIDGET_ID)
    uiConst.UI_INFO.append([SURVEY_WIDGET_ID, 'UISurveyWidget', 'uiSurvey'])
    from data import ui_location_data as ULD
    ULD.data[SURVEY_WIDGET_ID] = {'NPCLocation': ('center', 'top', 0, 0, 1280, 720, 1, 1, 1),
     'location': ('center', 'top', 0, 0, 1280, 720, 1, 1, 1)}
    ui = asObject.ASObject(gameglobal.rds.ui.uiObj)
    ui.resetInstance()
    gameglobal.rds.ui.uiSurvey.show()
