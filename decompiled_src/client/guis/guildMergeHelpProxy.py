#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergeHelpProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import gametypes
from uiProxy import UIProxy
GUILD_TYPE_TOP_FIVE = 1
GUILD_TYPE_TOP_FIFTEEN = 2
GUILD_TYPE_SAME_RANK = 3
from data import guild_config_data as GCD

class GuildMergeHelpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergeHelpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_HELP, self.hide)

    def reset(self):
        self.selectedType = GUILD_TYPE_SAME_RANK

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_HELP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_HELP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_HELP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.radio0.selected = False
        self.widget.radio1.selected = False
        self.widget.radio2.selected = True
        self.widget.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleSendBtnClick, False, 0, True)
        self.widget.txtAddMsg.defaultText = GCD.data.get('guildMergeHelpDefText', '')

    def handleSendBtnClick(self, *args):
        gamelog.info('jbx:handleSendBtnClick', self.widget.txtAddMsg.text)
        if self.widget.radio0.selected:
            recommType = gametypes.GUILD_MERGER_RECOMMEND_TYPE_BIG
        elif self.widget.radio1.selected:
            recommType = gametypes.GUILD_MERGER_RECOMMEND_TYPE_MIDDLE
        else:
            recommType = gametypes.GUILD_MERGER_RECOMMEND_TYPE_SAME
        p = BigWorld.player()
        gamelog.info('jbx:applyRecommendGuildMerger', recommType, self.widget.txtAddMsg.text)
        p.cell.applyRecommendGuildMerger(recommType, self.widget.txtAddMsg.text)
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
