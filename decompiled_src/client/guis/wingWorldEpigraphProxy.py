#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldEpigraphProxy.o
import BigWorld
import time
import gameglobal
import uiConst
import wingWorldUtils
from uiProxy import UIProxy
from data import book_content_data as BCD
from data import quest_marker_data as QMD
RED_FONT = "<font color=\'#FF0000\'>%s</font>"
GREEN_FONT = "<font color=\'#00B500\'>%s</font>"

class WingWorldEpigraphProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldEpigraphProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_EPIGRAPH, self.hide)
        self.season = 0
        self.date = 0
        self.city = 0
        self.guild = 0
        self.npcId = -1
        self.topPlayer = ''

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_EPIGRAPH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_EPIGRAPH)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_EPIGRAPH)

    def requestEpigraphData(self, npcId):
        p = BigWorld.player()
        p.cell.getNpcMonumentArgs(npcId)

    def showEpigraph(self, npcId, data):
        if not data or len(data) != 5:
            return
        self.season = int(data[0])
        self.date = int(data[1])
        self.city = int(data[2])
        self.guild = data[3]
        self.topPlayer = data[4]
        self.npcId = npcId
        self.show()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.title.text = ''
        self.widget.content.text = ''
        event = QMD.data.get(self.npcId, {}).get('event', [])
        if not event:
            return
        index = -1
        if event[0][0] == 'showQuestBook':
            index = event[0][1][0]
        if index not in BCD.data:
            return
        self.widget.title.text = BCD.data[index][0].get('Name', '')
        content = BCD.data[index][0].get('Content', '')
        nowTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(self.date))
        if content:
            season = GREEN_FONT % str(self.season)
            nowTime = RED_FONT % nowTime
            cityName = GREEN_FONT % wingWorldUtils.getCityName(self.city)
            guildName = RED_FONT % self.guild
            topPlayer = RED_FONT % self.topPlayer
            self.widget.content.htmlText = content % (season,
             nowTime,
             cityName,
             guildName,
             topPlayer)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type
