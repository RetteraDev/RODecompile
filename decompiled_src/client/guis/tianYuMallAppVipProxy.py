#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tianYuMallAppVipProxy.o
import gameglobal
import BigWorld
import time
import utils
import clientcom
from guis import uiConst
from guis import events
from guis import messageBoxProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import mall_config_data as MCFD
from data import netease_membership_item_data as NMID
from data import netease_membership_config_data as NMCD
TYPE_MALL_RECOMMEND = 1
TYPE_MALL_ITEM = 2
TYPE_VIP_RECOMMEND = 4
NUM_ONE_LINE = 4
MAIN_TAB_APP_VIP = 13
PRIVILEGE_WIDTH = 230
DEFALUT_CANVAS_LEFT = 30
PRIVILEGE_BUY = 0
PRIVILEGE_RECEIVE = 1

class TianYuMallAppVipProxy(object):

    def __init__(self):
        self.widget = None
        self.mall = None
        self.currPrivilgeIndex = 0
        self.privilegeKeys = []
        self.showTitle = []
        self.privilegeLen = 0

    def onWidgetRegister(self, widget, mall):
        self.widget = ASObject(widget)
        self.mall = mall
        self.initUI()
        self.refreshInfo()
        p = BigWorld.player()
        p.base.requireRecordOpenMembershipMall()

    def initUI(self):
        tabbar = self.widget.subTabBar
        for i in xrange(8):
            tab = tabbar.getChildByName('subTab' + str(i))
            tab.visible = False

        tabbar.subTab0.visible = True
        tabbar.subTab0.addEventListener(events.BUTTON_CLICK, self.onMallBtnClick)
        tabbar.subTab1.visible = True
        tabbar.subTab1.addEventListener(events.BUTTON_CLICK, self.onPrivilegeBtnClick)
        self.widget.privilege.leftBtn.addEventListener(events.BUTTON_CLICK, self.onLeftBtnClick)
        self.widget.privilege.rightBtn.addEventListener(events.BUTTON_CLICK, self.onRightBtnclick)
        self.widget.privilege.leftBtn.enabled = False
        self.widget.privilege.rightBtn.enabled = True
        self.currPrivilgeIndex = 0
        self.widget.privilege.canvas.x = DEFALUT_CANVAS_LEFT
        self.widget.itemList.itemRenderer = 'CombineTianyuMall_CombineMall_Item'
        self.widget.itemList.lableFunction = self.itemLabelFunc
        self.widget.itemList.column = NUM_ONE_LINE
        self.appendSubTabs()
        self.onMallBtnClick()

    def refreshInfo(self):
        if not self.widget:
            return
        self.setMemberInfo()
        self.setItemList()
        self.setPrivilegeList()

    def setMemberInfo(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            vipInfo = p.neteaseMembershipInfo
            level = vipInfo.level
            if not vipInfo.isMembershipExpire():
                self.widget.bindText.visible = True
                self.widget.vipLevel.visible = True
                self.widget.vipType.visible = True
                self.widget.validTime.visible = True
                self.widget.bindText.text = gameStrings.MALL_BIND if vipInfo.isHasMallDiscount() else gameStrings.MALL_UNBIND
                timeArray = time.localtime(p.neteaseMembershipInfo.getMembershpExpireDate())
                timeStr = gameStrings.MALL_APP_EXPIRE_DATE % str(time.strftime('%Y/%m/%d', timeArray))
                self.widget.validTime.text = timeStr
                if self.isSuperVip():
                    self.widget.vipType.gotoAndStop('normal')
                elif self.isCommonVip():
                    self.widget.vipType.gotoAndStop('normal')
            else:
                self.widget.bindText.visible = False
                self.widget.validTime.visible = False
                self.widget.vipType.visible = False
            if level <= -1:
                self.widget.vipLevel.visible = False
            else:
                self.widget.vipLevel.visible = True
                self.widget.vipLevel.gotoAndStop('v' + str(level))
        else:
            self.widget.bindText.visible = False
            self.widget.vipLevel.visible = False
            self.widget.validTime.visible = False
            self.widget.vipType.visible = False

    def isSuperVip(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return p.neteaseMembershipInfo.isSuperMembership()
        return False

    def isCommonVip(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return p.neteaseMembershipInfo.isGameMembership()
        return False

    def showPrivilegeBindWnd(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            if p.neteaseMembershipInfo.isHasMallDiscount():
                return True
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.MALL_BIND_CONFIRM, self.bindAppPrivilege), MBButton(gameStrings.CBG_HOME_GUANBI, None)]
            gameglobal.rds.ui.messageBox.show(True, gameStrings.MALL_BIND_TITLE, gameStrings.MALL_BIND_MSG, buttons)
        return False

    def bindAppPrivilege(self):
        p = BigWorld.player()
        p.base.applyMembershipInGame()

    def itemLabelFunc(self, *args):
        itemInfo = ASObject(args[3][0])
        listItem = ASObject(args[3][1])
        listItem.setBoxData(itemInfo, TYPE_MALL_ITEM, 0)
        listItem.addEventListener(events.EVENT_MALL_BUY, self.mibEventListener)
        listItem.addEventListener(events.EVENT_MALL_GIVE, self.mibEventListener)
        listItem.addEventListener(events.EVENT_MALL_TAKE, self.mibEventListener)
        listItem.addEventListener(events.EVENT_MALL_SELECT, self.mibEventListener)

    def setItemList(self):
        if self.mall.tabMgr.getSelChild().selChildId != 1:
            return
        self.removeAllChild(self.widget.itemList.canvas)
        info = self.mall.genTabContentInfo()
        itemsInfo = []
        for lineInfo in info.get('itemsInfo', []):
            for itemInfo in lineInfo:
                itemsInfo.append(itemInfo)

        self.widget.itemList.dataArray = itemsInfo

    def mibEventListener(self, *args):
        e = ASObject(args[3][0])
        mallId = e.target.mallData['mallId']
        buyNum = e.target.buyCount
        btnIdx = e.target.btnIdx
        if e.type == events.EVENT_MALL_BUY or e.type == events.EVENT_MALL_GIVE:
            if not self.isUserVipEnabled():
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.MALL_KNOWN_VIP, self.gotoMemberShipPage), MBButton(gameStrings.CBG_HOME_GUANBI, None)]
                gameglobal.rds.ui.messageBox.show(True, gameStrings.MALL_NOT_VIP, gameStrings.MALL_NOT_VIP_MSG, buttons)
                return
            if not self.showPrivilegeBindWnd():
                return
        if e.type == events.EVENT_MALL_BUY:
            self.mall.mallBuyConfirm(mallId, buyNum, 'appVip.' + str(btnIdx))
        elif e.type == events.EVENT_MALL_GIVE:
            self.mall.confirmGiveMallId = mallId
            self.mall.confirmGiveNum = buyNum
            gameglobal.rds.ui.loadWidget(self.mall.giveWidgetId, True)

    def gotoMemberShipPage(self):
        clientcom.openFeedbackUrl(NMCD.data.get('vipUrl', ''))

    def handleRecieveItem(self, *args):
        if not self.showPrivilegeBindWnd():
            return
        e = ASObject(args[3][0])
        privilegeKey = e.target.privilegeKey
        p = BigWorld.player()
        p.base.receiveMallVIPPrivilegeTitle([privilegeKey])

    def appendSubTabs(self):
        tabMgr = self.mall.tabMgr
        mallItems = {'value': NMCD.data.get('mallItems', ())}
        tabMgr.children[MAIN_TAB_APP_VIP].appendSubTab(1, mallItems)
        itemsValue = []
        self.privilegeKeys = []
        for key in NMID.data:
            itemInfo = NMID.data.get(key)
            itemsValue.append(itemInfo.get('value'))
            self.privilegeKeys.append(key)

        tabMgr.children[MAIN_TAB_APP_VIP].appendSubTab(2, {'value': itemsValue})

    def onMallBtnClick(self, *args):
        self.mall.selectSubTabById(1)
        self.widget.subTabBar.subTab0.selected = True
        self.widget.subTabBar.subTab1.selected = False
        self.widget.privilege.visible = False
        self.widget.itemList.visible = True
        self.refreshInfo()

    def onPrivilegeBtnClick(self, *args):
        self.mall.selectSubTabById(2)
        self.widget.subTabBar.subTab0.selected = False
        self.widget.subTabBar.subTab1.selected = True
        self.widget.privilege.visible = True
        self.widget.itemList.visible = False
        self.refreshInfo()

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)

    def isUserVipEnabled(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return p.neteaseMembershipInfo.isHasMembershipRight()
        return False

    def setPrivilegeList(self):
        if self.mall.tabMgr.getSelChild().selChildId != 2:
            return
        else:
            self.removeAllChild(self.widget.privilege.canvas)
            info = self.mall.genTabContentInfo()
            p = BigWorld.player()
            privilegesData = getattr(p, 'mallPrivilegeData', {})
            self.showTitle = []
            itemsInfo = []
            for lineInfo in info['itemsInfo']:
                for itemInfo in lineInfo:
                    itemsInfo.append(itemInfo)

            currIndex = 0
            for itemInfo in itemsInfo:
                if currIndex >= len(self.privilegeKeys):
                    break
                key = self.privilegeKeys[currIndex]
                privilegeInfo = NMID.data.get(key)
                listItem = None
                if privilegeInfo.get('privilegeType', 0) == 0:
                    listItem = self.widget.getInstByClsName('CombineTianyuMall_Privilege_Box')
                    listItem.itemBox.addEventListener(events.EVENT_MALL_BUY, self.mibEventListener)
                    listItem.itemBox.addEventListener(events.EVENT_MALL_GIVE, self.mibEventListener)
                    listItem.itemBox.addEventListener(events.EVENT_MALL_TAKE, self.mibEventListener)
                    listItem.itemBox.addEventListener(events.EVENT_MALL_SELECT, self.mibEventListener)
                else:
                    listItem = self.widget.getInstByClsName('CombineTianyuMall_Privilege_Box2')
                    listItem.itemBox.receiveBtn.privilegeKey = key
                    listItem.itemBox.receiveBtn.addEventListener(events.BUTTON_CLICK, self.handleRecieveItem)
                privilegeData = privilegesData.get(key, {})
                detail = privilegeInfo.get('detail', '')
                if detail:
                    detail = detail % str(privilegeData.get('value', 0))
                listItem.itemBox.desc.text = privilegeInfo.get('desc', '')
                listItem.itemBox.detail.text = detail
                privilegeTitleId = privilegeInfo.get('privilegeTitleId', 0)
                if privilegeTitleId and privilegeTitleId in NMCD.data.get('privilegeTitle', {}) and privilegeTitleId not in self.showTitle:
                    listItem.titleMc.title.text = NMCD.data.get('privilegeTitle', {}).get(privilegeTitleId, '')
                    self.showTitle.append(privilegeTitleId)
                else:
                    listItem.titleMc.visible = False
                itemInfo['state'] = uiConst.ITEM_NORMAL
                itemInfo['iconPathLarge'] = itemInfo['iconPath']
                if privilegeInfo.get('privilegeType') == PRIVILEGE_BUY:
                    if itemInfo['leftNum'] == 0 and itemInfo['limitType'] in (6, 7, 8, 9):
                        listItem.itemBox.detail.text = gameStrings.MALL_ALREADYBUY
                        itemInfo['state'] = uiConst.ITEM_DISABLE
                        listItem.itemBox.disableRollOver()
                if privilegeData.get('state', 0) == 0:
                    itemInfo['state'] = uiConst.ITEM_DISABLE
                    listItem.itemBox.disableRollOver()
                    if privilegeInfo.get('privilegeType') == PRIVILEGE_RECEIVE:
                        listItem.itemBox.receiveBtn.enabled = False
                    if not self.isUserVipEnabled():
                        listItem.itemBox.detail.text = gameStrings.MALL_NO_VIP_CANT_BUY
                if privilegeData.get('state', 0) == -1:
                    itemInfo['state'] = uiConst.ITEM_DISABLE
                    listItem.itemBox.disableRollOver()
                    if privilegeInfo.get('privilegeType') == PRIVILEGE_RECEIVE:
                        listItem.itemBox.detail.text = gameStrings.MALL_HAVE_RECIEVE
                        itemInfo['leftNum'] = 0
                        listItem.itemBox.receiveBtn.enabled = False
                if not self.isSuperVip() and privilegeInfo.get('isSuper', 0):
                    itemInfo['state'] = uiConst.ITEM_DISABLE
                    listItem.itemBox.disableRollOver()
                    listItem.itemBox.detail.text = gameStrings.MALL_NOT_SUPER_VIP
                listItem.itemBox.setBoxData(itemInfo, TYPE_VIP_RECOMMEND, currIndex)
                listItem.x = listItem.width * currIndex
                self.widget.privilege.canvas.addChild(listItem)
                currIndex += 1

            self.privilegeLen = len(itemsInfo)
            return

    def onLeftBtnClick(self, *args):
        self.movePrivelegeListBy(1)

    def onRightBtnclick(self, *args):
        self.movePrivelegeListBy(-1)

    def movePrivelegeListBy(self, offset):
        if self.currPrivilgeIndex + offset - NUM_ONE_LINE >= -self.privilegeLen and self.currPrivilgeIndex + offset <= 0:
            self.currPrivilgeIndex += offset
            param = {'time': 0.15,
             'x': self.currPrivilgeIndex * PRIVILEGE_WIDTH + DEFALUT_CANVAS_LEFT,
             'transition': 'easeOutSine'}
            ASUtils.addTweener(self.widget.privilege.canvas, param)
        if self.currPrivilgeIndex - NUM_ONE_LINE == -self.privilegeLen:
            self.widget.privilege.rightBtn.enabled = False
        else:
            self.widget.privilege.rightBtn.enabled = True
        if self.currPrivilgeIndex == 0:
            self.widget.privilege.leftBtn.enabled = False
        else:
            self.widget.privilege.leftBtn.enabled = True

    def onWidgetUnRegister(self):
        self.widget = None
        self.mall = None
