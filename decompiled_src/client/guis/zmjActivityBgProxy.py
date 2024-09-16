#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjActivityBgProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import zmjCommon
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from uiTabProxy import UITabProxy
from data import fb_entity_data as FED
from data import monster_data as MD
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD
from data import fame_data as FD
TAB_ONE_IDX = 0
TAB_TWO_IDX = 1
TAB_THREE_IDX = 2
BOSS_NO_SUFFIX = '0001'
BG_TYPE_NORMAL = 1
BG_TYPE_ACTIVITY = 2

class ZmjActivityBgProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(ZmjActivityBgProxy, self).__init__(uiAdapter)
        self.tabIndexList = [TAB_ONE_IDX, TAB_TWO_IDX, TAB_THREE_IDX]
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_ACTIVITY_BG, self.hide)

    def reset(self):
        super(ZmjActivityBgProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_ACTIVITY_BG:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(ZmjActivityBgProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_ACTIVITY_BG)

    def _getTabList(self):
        return [{'tabIdx': TAB_ONE_IDX,
          'tabName': 'littleBossBtn',
          'view': 'ZmjLittleBossPanel',
          'proxy': 'zmjLittleBossPanel'}, {'tabIdx': TAB_TWO_IDX,
          'tabName': 'bigBossBtn',
          'view': 'ZmjBigBossPanel',
          'proxy': 'zmjBigBossPanel'}, {'tabIdx': TAB_THREE_IDX,
          'tabName': 'activityBossBtn',
          'view': 'ZmjActivityBossPanel',
          'proxy': 'zmjActivityBossPanel'}]

    def show(self, tabIndex = TAB_ONE_IDX):
        if not gameglobal.rds.configData.get('enableZMJFuben', False):
            return
        if tabIndex == TAB_THREE_IDX and not gameglobal.rds.configData.get('enableZMJStarBoss', False):
            tabIndex = TAB_ONE_IDX
        p = BigWorld.player()
        minLvNeed = ZFCD.data.get('minLvNeed', 0)
        if p.lv < minLvNeed:
            p.showGameMsg(GMDD.data.ZMJ_LV_LIMIT_MSG, ())
            return
        if not zmjCommon.checkinZMJTime():
            p.showGameMsg(GMDD.data.ZMJ_TIME_LIMIT_MSG, ())
            return
        self.showTabIndex = tabIndex if tabIndex in self.tabIndexList else TAB_ONE_IDX
        self.queryServerInfo()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_ACTIVITY_BG)
        elif self.currentTabIndex != self.showTabIndex:
            ASUtils.DispatchButtonEvent(self.widget.tabButtons[self.showTabIndex])
        else:
            self.refreshInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.getZMJPhotoData()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_ONE_IDX)
        else:
            self.widget.setTabIndex(self.showTabIndex)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTabsVisible()
        self.refreshBg()
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def refreshBg(self):
        if self.currentTabIndex == TAB_THREE_IDX:
            bgType = ZFCD.data.get('zmjStarBossBgType', BG_TYPE_ACTIVITY)
            self.widget.bg.gotoAndStop('type%d' % bgType)
        else:
            self.widget.bg.gotoAndStop('type%d' % BG_TYPE_NORMAL)

    def refreshTabsVisible(self):
        self.widget.activityBossBtn.visible = gameglobal.rds.configData.get('enableZMJStarBoss', False)

    def onTabChanged(self, *args):
        super(ZmjActivityBgProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def _onTabBtn0Click(self, e):
        pass

    def hasNewInfo(self):
        p = BigWorld.player()
        curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
        notTake = gameglobal.rds.ui.zmjSpriteReward.notTake
        zhanmoAutoIncLimit = FD.data.get(const.ZMJ_ZHANMO_FAME_ID, {}).get('autoIncLimit', 200)
        hasNewStarBoss = gameglobal.rds.ui.zmjActivityBossPanel.needPushMsg()
        return curZhanmo >= zhanmoAutoIncLimit or bool(notTake) or hasNewStarBoss

    def getBossInfo(self, fbNo):
        monsterId = int(str(fbNo) + BOSS_NO_SUFFIX)
        eData = FED.data.get(monsterId, {})
        entityNo = eData.get('entityNo', 0)
        mData = MD.data.get(entityNo, {})
        name = mData.get('name', '')
        info = {'name': name}
        return info
