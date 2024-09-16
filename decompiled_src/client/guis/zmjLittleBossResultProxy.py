#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjLittleBossResultProxy.o
import BigWorld
import utils
import const
import formula
import gameglobal
import uiConst
from uiProxy import UIProxy
from data import fame_data as FD
from data import zmj_fuben_config_data as ZFCD
SHOW_ICON_PATH_PREFIX = 'zmjactivity/bossicon/%d.dds'

class ZmjLittleBossResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjLittleBossResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.fbNo = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_LITTLE_BOSS_RESULT_WIDGET, self.hide)

    def reset(self):
        self.resultInfo = {}
        self.fbNo = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_LITTLE_BOSS_RESULT_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_LITTLE_BOSS_RESULT_WIDGET)

    def show(self, resultInfo, fbNo = 0):
        self.resultInfo = resultInfo
        self.fbNo = fbNo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_LITTLE_BOSS_RESULT_WIDGET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.confirmBtn
        zmjDmg = self.resultInfo.get('zmjDmg', 0)
        zmjTime = self.resultInfo.get('zmjTime', 0)
        zmjStar = self.resultInfo.get('star', 0) if self.fbNo else self.resultInfo.get('zmjStar', 0)
        zmjGX = self.resultInfo.get('zmjGX', 0)
        fameCnt = self.resultInfo.get('fameCnt', 0)
        fameId = self.resultInfo.get('fameId', 0)
        zmjTF = self.resultInfo.get('zmjTF', 0)
        succ = self.resultInfo.get('succ', 0)
        if succ:
            self.widget.resultState.gotoAndStop('success')
        else:
            self.widget.resultState.gotoAndStop('fail')
        self.widget.starMc.starTxt.text = zmjStar
        self.widget.timeMc.timeTxt.text = utils.formatTimeStr(int(zmjTime), 'h:m:s', True, sNum=2, mNum=2, hNum=2)
        self.widget.dmgMc.dmgTxt.text = zmjDmg
        if self.fbNo:
            bossTitleName = ZFCD.data.get('zmjActivityBossTitle', 'star')
            self.widget.title.gotoAndStop(bossTitleName)
            self.widget.reward1.textField.text = FD.data.get(fameId, {}).get('name', '')
            self.widget.gongxianMc.gongxianTxt.text = fameCnt
            self.widget.reward2.visible = False
            self.widget.taofaMc.visible = False
        else:
            self.widget.title.gotoAndStop('normal')
            self.widget.gongxianMc.gongxianTxt.text = zmjGX
            self.widget.taofaMc.taofaTxt.text = zmjTF
        p = BigWorld.player()
        curFbNo = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0) if not self.fbNo else self.fbNo
        bossResultIcon = ZFCD.data.get('bossResultIcon', {})
        iconId = bossResultIcon.get(curFbNo, 0)
        self.widget.iconMc.fitSize = True
        self.widget.iconMc.loadImage(SHOW_ICON_PATH_PREFIX % (iconId,))

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        pass
