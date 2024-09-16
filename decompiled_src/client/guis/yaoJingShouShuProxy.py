#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoJingShouShuProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import uiConst
import gamelog
from guis import events
from guis import uiUtils
from uiProxy import UIProxy
from helpers import tickManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from gamestrings import gameStrings
YAOJING_SHOUSHU_ID = 400601
DEFAULT_COST_LIST = {1: (2, 1, 40555),
 2: (18, 5, 40556),
 3: (90, 20, 40557)}
SHOUSHU_COST = 0
SHOUSHU_REWARD = 1

class YaoJingShouShuProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YaoJingShouShuProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOJING_QITAN, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YAOJING_QITAN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YAOJING_QITAN)

    def show(self):
        if not gameglobal.rds.configData.get('enableYaojingqitanCustomCost', False):
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_YAOJINGSHOUSHUPROXY_44)
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_YAOJING_QITAN)

    def getReward(self, index):
        return self.shouShuCostList[index + 1][SHOUSHU_REWARD]

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.waitingPage.visible = False
        self.widget.helpBtn.visible = False
        self.shouShuID = YAOJING_SHOUSHU_ID
        self.shouShuCostList = SCD.data.get('yaojingqitanCost', DEFAULT_COST_LIST)
        player = BigWorld.player()
        if not player:
            self.clearWidget()
            return
        self.shouShuNum = player.inv.countItemInPages(self.shouShuID, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        self.widget.shouShuSlot.setItemSlotData(uiUtils.getGfxItemById(self.shouShuID, self.shouShuNum))
        self.widget.shouShuSlot.dragable = False
        self.widget.tip.text = SCD.data.get('yaojingqitanCostTip', gameStrings.TEXT_YAOJINGSHOUSHUPROXY_68)
        for i in range(len(self.shouShuCostList)):
            ck_box = getattr(self.widget.selectPage, 'ckBox' + str(i))
            if ck_box:
                shoushu_cost = self.shouShuCostList[i + 1][SHOUSHU_COST]
                ck_box.data = i
                ck_box.label = str(shoushu_cost)
                if i == getattr(player, 'yaojingqitanCostType', 1) - 1:
                    ck_box.selected = True
                    self.selectIndex = i
                ck_box.addEventListener(events.MOUSE_CLICK, self.onChangeNum, False, 0, True)

        self.refreshReward()
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirm, False, 0, True)

    def onChangeNum(self, *args):
        data = ASObject(args[3][0]).target.data
        self.selectIndex = int(data)
        self.defaultSelectIndex = self.selectIndex
        self.refreshReward()

    def refreshReward(self):
        if self.selectIndex < 0:
            self.widget.rewardMultiRate.text = '0%'
            return
        self.widget.rewardMultiRate.text = str(self.shouShuCostList[self.selectIndex + 1][SHOUSHU_REWARD]) + '00%'

    def onConfirm(self, *args):
        self.postCostData()
        self.clearWidget()

    def postCostData(self):
        p = BigWorld.player()
        gamelog.debug('dxk@yaoJingShouShuProxy post cost data:', self.selectIndex + 1)
        p.cell.setYaojingqitanCostType(self.selectIndex + 1)

    def refreshInfo(self):
        if not self.widget:
            return
