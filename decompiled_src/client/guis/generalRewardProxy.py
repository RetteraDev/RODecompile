#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalRewardProxy.o
import BigWorld
from Scaleform import GfxValue
import clientUtils
import uiConst
from guis import uiUtils
from guis.asObject import ASObject
from data import general_reward_config_data as GRCD
from uiProxy import UIProxy
from guis import events
from gamestrings import gameStrings
SLOT_MAX_CNT = 14
SLOT_ONE_LINE = 7
SLOT_ONE_LINE_HEIGHT = 45
MAX_TAB_NUM = 5
WND_TYPE_NORMAL = 1
WND_TYPE_TAB = 2

class GeneralRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currRewardData = {}
        self.rewardId = 0
        self.wndType = WND_TYPE_NORMAL
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GENERAL_REWARD, self.hide)

    def reset(self):
        self.title = ''
        self.infoList = []
        self.currRewardData = {}
        self.wndType = WND_TYPE_NORMAL
        self.rewardId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_REWARD)
        self.reset()

    def show(self, rewardId):
        rewardData = GRCD.data.get(rewardId, {})
        if not rewardData:
            return
        self.currRewardData = rewardData
        title = rewardData.get('title', '')
        self.title = title
        self.rewardId = rewardId
        self.initInfoList(rewardData)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_REWARD)
        else:
            self.refreshInfo()

    def initInfoList(self, rewardData):
        self.infoList = []
        infoList = rewardData.get('infolist', ())
        for listData in infoList:
            if listData:
                if type(listData) in (tuple, list):
                    self.infoList.extend(listData)
                else:
                    self.infoList.append(listData)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def itemHeightFunction(self, *args):
        index = int(args[3][0].GetNumber())
        if index < len(self.infoList):
            if len(self.infoList[index][1:]) <= SLOT_MAX_CNT / 2:
                return GfxValue(87)
            else:
                return GfxValue(145)
        else:
            return GfxValue(145)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currRewardData.get('subIds', []):
            if self.wndType != WND_TYPE_TAB:
                self.widget.gotoAndStop('tab')
                self.wndType = WND_TYPE_TAB
            subIds = self.currRewardData.get('subIds', [])
            for i in xrange(MAX_TAB_NUM):
                tabMc = self.widget.getChildByName('tab%d' % i)
                if i < len(subIds):
                    tabMc.visible = True
                    tabMc.rewardId = subIds[i]
                    tabName = GRCD.data.get(subIds[i], {}).get('title', '')
                    tabMc.label = tabName
                    tabMc.selected = tabMc.rewardId == self.rewardId
                    tabMc.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)
                else:
                    tabMc.visible = False

            self.widget.title.textField.text = gameStrings.GENERAL_REWARD_DEFAULT_TITLE
        else:
            if self.wndType != WND_TYPE_NORMAL:
                self.widget.gotoAndStop('normal')
                self.wndType = WND_TYPE_NORMAL
            self.widget.title.textField.text = self.title
        tipInfo = self.currRewardData.get('tip', '')
        if not tipInfo:
            self.widget.icon.visible = False
            self.widget.tip.text = ''
        else:
            self.widget.icon.visible = True
            self.widget.tip.text = tipInfo
        self.refreshScrollWndInfo()

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        rewardId = e.currentTarget.rewardId
        if self.rewardId == rewardId:
            return
        self.show(rewardId)

    def refreshScrollWndInfo(self):
        self.removeAllChild(self.widget.scrollWndList.canvas)
        currY = 0
        for index in xrange(len(self.infoList)):
            mc = None
            itemHeight = 0
            if not self.infoList[index]:
                continue
            if type(self.infoList[index]) == str:
                mc = self.widget.getInstByClsName('GeneralReward_SubTitle')
                title = self.infoList[index]
                mc.textField.text = title
            elif type(self.infoList[index]) == tuple:
                if len(self.infoList[index]) == 1:
                    mc = self.widget.getInstByClsName('GeneralReward_tip')
                    args0 = self.infoList[index][0]
                    mc.textField.text = args0
                    itemHeight = mc.textField.textHeight + 8
                else:
                    mc = self.widget.getInstByClsName('GeneralReward_items')
                    args0 = self.infoList[index][0]
                    mc.txtTitle.text = args0
                    mc.rewardArea.y = mc.txtTitle.textHeight + 5
                    itemList = self.infoList[index][1:]
                    if itemList and type(itemList[0]) == int:
                        bonusId = itemList[0]
                        itemList = clientUtils.genItemBonus(bonusId)
                    for i in xrange(SLOT_MAX_CNT):
                        slotMc = getattr(mc.rewardArea, 'item%d' % i)
                        if i < len(itemList):
                            slotMc.visible = True
                            slotMc.dragable = False
                            slotMc.setItemSlotData(uiUtils.getGfxItemById(*itemList[i]))
                        else:
                            slotMc.visible = False

                    areaHeight = mc.rewardArea.height
                    if len(itemList) < SLOT_ONE_LINE:
                        areaHeight = SLOT_ONE_LINE_HEIGHT
                    itemHeight = mc.rewardArea.y + areaHeight
            if mc:
                self.widget.scrollWndList.canvas.addChild(mc)
                mc.y = currY
                itemHeight = itemHeight if itemHeight else mc.height
                currY += itemHeight + 5

        self.widget.scrollWndList.validateNow()
        self.widget.scrollWndList.refreshHeight()

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)
