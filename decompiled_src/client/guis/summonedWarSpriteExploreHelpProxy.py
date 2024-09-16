#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteExploreHelpProxy.o
import BigWorld
import uiConst
import summonSpriteExplore
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteExploreHelpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteExploreHelpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.gbId = 0
        self.posIdx = 0
        self.itemId = 0
        self.itemNum = 0
        self.groupId = 0
        self.daySecond = 0
        self.roleName = ''
        self.dikouNum = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_HELP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_HELP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_HELP)

    def reset(self):
        self.gbId = 0
        self.posIdx = 0
        self.itemId = 0
        self.itemNum = 0
        self.groupId = 0
        self.daySecond = 0
        self.roleName = ''
        self.dikouNum = 0

    def show(self, gbId, index, itemId, itemNum, groupId, daySecond, roleName):
        self.gbId = gbId
        self.posIdx = index
        self.itemId = itemId
        self.itemNum = itemNum
        self.groupId = groupId
        self.daySecond = daySecond
        self.roleName = roleName
        p = BigWorld.player()
        if not p.guild:
            p.showGameMsg(GMDD.data.SUMMONED_SPRITE_EXPLORE_QUIT_GUILD, ())
            return
        if p.gbId == self.gbId:
            p.showGameMsg(GMDD.data.EXPLORE_SPRITE_CANNOT_HELP_MYSELF, ())
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_HELP, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        playName = ''
        if p.guild:
            for member in p.guild.member.values():
                if member.gbId == self.gbId:
                    playName = member.role
                    break

        itemName = uiUtils.getItemColorName(self.itemId)
        contrib = 0
        self.dikouNum = 0
        groupData = summonSpriteExplore.getExploreSpriteGroupData(self.groupId)
        if groupData:
            contrib = groupData.get('contrib', 0)
            self.dikouNum = groupData.get('dikouNum', 0)
        self.widget.desc0.htmlText = gameStrings.SPRITE_EXPLORE_HELP_DESC % playName
        self.widget.desc1.htmlText = gameStrings.SPRITE_EXPLORE_HELP_GET_POINT_DESC % contrib
        self.widget.valTxt.text = self.dikouNum
        self.widget.itemSlot.slot.fitSize = True
        self.widget.itemSlot.slot.dragable = False
        myItemNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, self.itemId)
        if myItemNum >= self.itemNum:
            color = '#d9cfb6'
            self.widget.diKouBtn.selected = False
        else:
            color = '#d34024'
            self.widget.diKouBtn.selected = True
        count = uiUtils.toHtml('%d/%d' % (myItemNum, self.itemNum), color)
        itemInfo = uiUtils.getGfxItemById(self.itemId, count)
        self.widget.itemSlot.slot.setItemSlotData(itemInfo)
        self.updateGiveBtnState()

    def updateGiveBtnState(self):
        p = BigWorld.player()
        isDiKou = self.widget.diKouBtn.selected
        if isDiKou:
            myTianbi = p.unbindCoin + p.bindCoin + p.freeCoin
            if myTianbi < self.dikouNum:
                self.widget.giveBtn.disabled = True
                TipManager.addTip(self.widget.giveBtn, gameStrings.SPRITE_EXPLORE_HELP_LESS_TIANBI_DESC)
            else:
                TipManager.removeTip(self.widget.giveBtn)
                self.widget.giveBtn.disabled = False
        else:
            myItemNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, self.itemId)
            if myItemNum < self.itemNum:
                self.widget.giveBtn.disabled = True
                TipManager.addTip(self.widget.giveBtn, gameStrings.SPRITE_EXPLORE_HELP_LESS_ITEM_DESC)
            else:
                TipManager.removeTip(self.widget.giveBtn)
                self.widget.giveBtn.disabled = False

    def _onGiveBtnClick(self, e):
        isDiKou = self.widget.diKouBtn.selected
        p = BigWorld.player()
        if isDiKou:
            p.cell.exploreSpriteHelpItem(self.gbId, self.posIdx, self.itemId, self.itemNum, self.groupId, self.daySecond, const.EXPLORE_SPRITE_HELP_BY_CASH, self.roleName)
        else:
            p.cell.exploreSpriteHelpItem(self.gbId, self.posIdx, self.itemId, self.itemNum, self.groupId, self.daySecond, const.EXPLORE_SPRITE_HELP_BY_ITEM, self.roleName)

    def _onDiKouBtnClick(self, e):
        self.updateGiveBtnState()

    def _onCancelBtnClick(self, e):
        self.hide()
