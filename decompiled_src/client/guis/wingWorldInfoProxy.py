#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldInfoProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import events
import gamelog
import utils
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASUtils
from cdata import wing_world_schedule_data as WWSD
from data import wing_world_config_data as WWCD
COUNTRY_MAX_CNT = 3

class WingWorldInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_INFO, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_INFO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_INFO)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_INFO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.detailBtn.addEventListener(events.BUTTON_CLICK, self.handleDetailBtnClick, False, 0, True)
        ASUtils.setHitTestDisable(self.widget.titleName, True)
        ASUtils.setHitTestDisable(self.widget.txtLeftTime, True)
        self.timerFun()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        info = self.uiAdapter.wingWorldDetailInfo.getInfo()
        buildingMaxScore = WWCD.data.get('buildingMaxScore', 500)
        scoreDic = info['scoreDic']
        scoreList = scoreDic.values()
        scoreList.sort(cmp=lambda x, y: cmp(x['buildScore'], y['buildScore']), reverse=True)
        for i in xrange(COUNTRY_MAX_CNT):
            progressBarMc = getattr(self.widget, 'progressbar%d' % i)
            txtScoreMc = getattr(self.widget, 'txtScore%d' % i)
            if i < len(scoreList):
                progressBarMc.visible = True
                txtScoreMc.visible = True
                scoreInfo = scoreList[i]
                buildScore = scoreInfo['buildScore']
                colorIdx = scoreInfo['campIdx'] - 1
                currentValues = [0, 0, 0]
                currentValues[colorIdx] = buildScore * 1.0 / buildingMaxScore * 100
                progressBarMc.currentValues = currentValues
                countryName = scoreInfo['countryName']
                txtScoreMc.text = '%s:%d' % (countryName, buildScore)
            else:
                progressBarMc.visible = False
                txtScoreMc.visible = False

    def handleDetailBtnClick(self, *args):
        gamelog.info('jbx:handleDetailBtnClick')
        self.uiAdapter.wingWorldDetailInfo.show()

    def handleMapBtnClick(self, *args):
        gamelog.info('jbx:handleMapBtnClick')

    def timerFun(self):
        if not self.widget:
            return
        endTime = utils.getNextCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_SETTLEMENT].get('crontab', ''))
        if not utils.isSameWeek(endTime, utils.getNow()):
            endTime = utils.getPreCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_SETTLEMENT].get('crontab', ''))
        leftTime = max(0, int(endTime) - utils.getNow())
        self.widget.txtLeftTime.text = utils.formatTimeStr(leftTime, gameStrings.TEXT_WINGWORLDINFOPROXY_90, True, 2, 2, 1)
        BigWorld.callback(1, self.timerFun)
