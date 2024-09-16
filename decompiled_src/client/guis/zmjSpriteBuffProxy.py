#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjSpriteBuffProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import gamelog
import utils
from asObject import ASUtils
from uiProxy import UIProxy
from guis.asObject import TipManager
from asObject import ASObject
from data import zmj_sprite_buff_data as ZSBD
from data import consumable_item_data as CID
from data import item_data as ID
from data import summon_sprite_info_data as SSID
TAB_NEAR_PHYSICAL = 0
TAB_NEAR_SPELL = 1
TAB_FAR_PHYSICAL = 2
TAB_FAR_SPELL = 3
MAX_BUFF_NUM = 8
sprite_atk_tab_map = {1: 0,
 2: 2,
 3: 3,
 4: 1}

class ZmjSpriteBuffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjSpriteBuffProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.sptiteItemStateData = {}
        self.reset()

    def reset(self):
        self.selectedTab = TAB_NEAR_PHYSICAL
        self.buffList = {}
        self.isFirstTime = True
        self.delTimer()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_SPRITE_BUFF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_SPRITE_BUFF)

    def setSptiteItemStateData(self, data):
        self.sptiteItemStateData = data
        self.refreshInfo()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_SPRITE_BUFF)
        self.refreshInfo()

    def afterSummonedSprite(self):
        p = BigWorld.player()
        if p.summonedSpriteInWorld:
            spriteId = p.summonedSpriteInWorld.spriteId
            spriteAtkType = SSID.data.get(spriteId, {}).get('atkType', 0)
            self.selectedTab = sprite_atk_tab_map.get(spriteAtkType, 0)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.buffList = {}
        for i, info in ZSBD.data.iteritems():
            type = info.get('type')
            self.buffList.setdefault(type, []).append(info)

        if self.isFirstTime:
            p = BigWorld.player()
            if p.summonedSpriteInWorld:
                spriteId = p.summonedSpriteInWorld.spriteId
                spriteAtkType = SSID.data.get(spriteId, {}).get('atkType', 0)
                self.selectedTab = sprite_atk_tab_map.get(spriteAtkType, 0)
            self.isFirstTime = False
        self.setAllTabNotSelected()
        tabBtn = self.widget.mainMc.getChildByName('tabBtn%d' % self.selectedTab)
        tabBtn.selected = True
        selectBuffList = self.buffList.get(self.selectedTab)
        for i in xrange(MAX_BUFF_NUM):
            itemMc = self.widget.mainMc.getChildByName('buff%d' % i)
            if i < len(selectBuffList):
                itemMc.visible = True
            else:
                itemMc.visible = False
                continue
            val = selectBuffList[i]
            itemMc.desc.text = val.get('name')
            itemMc.iconCnt.text = '0/5'
            buffId = val.get('buffid')
            buffInfo = ID.data.get(buffId)
            iconPath = 'state/48/%d.dds' % buffInfo.get('icon', 0)
            buffTip = buffInfo.get('funcDesc', '')
            itemMc.slot.fitSize = True
            itemMc.slot.dragable = False
            itemMc.slot.setItemSlotData({'iconPath': iconPath})
            ASUtils.setHitTestDisable(itemMc.slot, False)
            ASUtils.setHitTestDisable(itemMc.iconCnt, True)
            itemMc.slot.validateNow()
            TipManager.addTip(itemMc.slot, buffTip)
            atkTypeInfo = self.sptiteItemStateData.get(const.SPRITE_STATE_FILTER_ATK_TYPES)
            spriteStateMaxLayer = CID.data.get(buffId).get('spriteStateMaxLayer', 5)
            if atkTypeInfo and buffId in atkTypeInfo.keys():
                itemMc.iconCnt.text = '%d/%d' % (len(atkTypeInfo[buffId]), spriteStateMaxLayer)
            else:
                itemMc.iconCnt.text = '%d/%d' % (0, spriteStateMaxLayer)

    def initUI(self):
        self.widget.showInfoBtn.addEventListener(events.MOUSE_CLICK, self.handleClickshowInfoBtn, False, 0, True)
        self.widget.mainMc.tabBtn0.addEventListener(events.MOUSE_CLICK, self.handleClickTabBtn, False, 0, True)
        self.widget.mainMc.tabBtn1.addEventListener(events.MOUSE_CLICK, self.handleClickTabBtn, False, 0, True)
        self.widget.mainMc.tabBtn2.addEventListener(events.MOUSE_CLICK, self.handleClickTabBtn, False, 0, True)
        self.widget.mainMc.tabBtn3.addEventListener(events.MOUSE_CLICK, self.handleClickTabBtn, False, 0, True)
        self.widget.showInfoBtn.gotoAndStop('hide')
        self.timerFunc()
        self.addTimer()

    def handleClickshowInfoBtn(self, *args):
        self.widget.mainMc.visible = not self.widget.mainMc.visible
        if self.widget.mainMc.visible:
            self.widget.showInfoBtn.gotoAndStop('hide')
        else:
            self.widget.showInfoBtn.gotoAndStop('show')
        if self.widget.mainMc.visible:
            self.refreshInfo()

    def handleClickTabBtn(self, *args):
        target = ASObject(args[3][0]).currentTarget
        index = target.data
        self.selectedTab = index
        self.refreshInfo()

    def setAllTabNotSelected(self):
        if not self.widget:
            return
        self.widget.mainMc.tabBtn0.selected = False
        self.widget.mainMc.tabBtn1.selected = False
        self.widget.mainMc.tabBtn2.selected = False
        self.widget.mainMc.tabBtn3.selected = False

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        needRefresh = False
        atkTypeInfo = self.sptiteItemStateData.get(const.SPRITE_STATE_FILTER_ATK_TYPES)
        if not atkTypeInfo:
            return
        for key, value in atkTypeInfo.iteritems():
            for expireTime in reversed(value):
                if expireTime < utils.getNow():
                    value.remove(expireTime)
                    needRefresh = True

        if needRefresh:
            self.refreshInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None
