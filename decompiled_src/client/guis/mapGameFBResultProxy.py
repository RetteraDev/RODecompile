#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameFBResultProxy.o
import BigWorld
import utils
import const
import gamelog
import gameglobal
import uiConst
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
SHOW_ICON_PATH_PREFIX = 'mapgame/%s.dds'

class MapGameFBResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameFBResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_FB_RESULT, self.hide)

    def reset(self):
        self.resultInfo = {}
        self.fbNo = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_FB_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_FB_RESULT)

    def show(self, fbNo, resultInfo):
        self.fbNo = fbNo
        self.resultInfo = resultInfo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_FB_RESULT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.confirmBtn
        damage = self.resultInfo.get('damage', 0)
        duration = self.resultInfo.get('mapGameTime', 0)
        scoreLv = self.resultInfo.get('gainFame', 0)
        fbResultTitle = MGCD.data.get('mapGameFBResultTitle', {})
        title = fbResultTitle.get(self.fbNo, '')
        self.widget.titleMc.tf.text = title
        self.widget.scoreMc.desc.text = MGCD.data.get('mapGameFBScoreDesc', '')
        self.widget.starMc.starTxt.text = scoreLv
        self.widget.timeMc.timeTxt.text = utils.formatTimeStr(int(duration), 'h:m:s', True, sNum=2, mNum=2, hNum=2)
        self.widget.dmgMc.dmgTxt.text = damage
        bossResultIcon = MGCD.data.get('mapGameFBResultIcon', {})
        iconId = bossResultIcon.get(self.fbNo, 0)
        self.widget.iconMc.fitSize = True
        self.widget.iconMc.loadImage(SHOW_ICON_PATH_PREFIX % str(iconId))

    def refreshInfo(self):
        if not self.widget:
            return
