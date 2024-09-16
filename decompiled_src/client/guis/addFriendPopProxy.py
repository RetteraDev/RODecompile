#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/addFriendPopProxy.o
import BigWorld
import const
import uiConst
import utils
import events
import gametypes
from uiProxy import UIProxy
from guis import menuManager
from asObject import ASObject
from asObject import TipManager
from gamestrings import gameStrings
from data import sys_config_data as SCD
MEMBER_MAX = 4
SRC_ID = {gametypes.GET_ZONE_TOUCH_NUM_FOR_TEAM_MONSTER_TRIGGER: const.FRIEND_SRC_MONSTER_TRIGGER,
 gametypes.GET_ZONE_TOUCH_NUM_FOR_TEAM_SSC_END: const.FRIENT_SRC_TEAM_SSC}

class AddFriendPopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AddFriendPopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ADD_FRIEND_POP, self.hide)

    def reset(self):
        self.hintText = None
        self.gbIdItems = {}
        self.touchInfo = {}
        self.signTextInfo = {}
        self.useType = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ADD_FRIEND_POP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ADD_FRIEND_POP)

    def show(self, useType, memberData = None):
        self.useType = useType
        self.initMemberData(memberData)
        self.hintText = SCD.data.get('addFriendPopUseType', {}).get(useType)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ADD_FRIEND_POP)

    def initMemberData(self, memberData):
        if memberData:
            self.memberData = memberData
        else:
            p = BigWorld.player()
            self.memberData = {gbId:pInfo for gbId, pInfo in p.members.iteritems() if self.isSameTeam(gbId)}

    def isSameTeam(self, gbId):
        p = BigWorld.player()
        return utils.isSameTeam(p.arrangeDict.get(gbId), p.groupIndex)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.hintTf.htmlText = self.hintText
        self.initMembers()
        self.initTouchBtn()
        self.initSignBtn()

    def initTouchBtn(self):
        for ownerGbId, touched in self.touchInfo.iteritems():
            self.refreshTouchBtn(ownerGbId, touched)

    def initSignBtn(self):
        for ownerGbId, signText in self.signTextInfo.iteritems():
            self.refreshSignText(ownerGbId, signText)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        self.hide()

    def initMembers(self):
        p = BigWorld.player()
        memberCnt = 0
        for gbId, pInfo in self.memberData.iteritems():
            if gbId == p.gbId:
                continue
            memberMc = getattr(self.widget, 'memberMc%d' % memberCnt)
            roleName = pInfo.get('roleName')
            memberMc.nameTf.text = roleName
            memberMc.lvTf.text = 'Lv.%d' % pInfo.get('level')
            memberMc.leaderMc.visible = pInfo.get('isHeader')
            memberMc.schoolMc.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[pInfo.get('school', const.SCHOOL_SHENTANG)])
            memberMc.addBtn.visible = not p.friend.isFriend(gbId)
            memberMc.addBtn.addEventListener(events.BUTTON_CLICK, self.handleAddBtnClick, False, 0, True)
            memberMc.touchBtn.visible = True
            memberMc.touchBtn.addEventListener(events.BUTTON_CLICK, self.handleTouchBtnClick, False, 0, True)
            memberMc.visible = True
            setattr(memberMc.addBtn, 'gbId', gbId)
            setattr(memberMc.touchBtn, 'gbId', gbId)
            setattr(memberMc.touchBtn, 'roleName', roleName)
            self.setItemByGbId(gbId, memberMc)
            memberCnt += 1

        for idx in xrange(memberCnt, MEMBER_MAX):
            memberMc = getattr(self.widget, 'memberMc%d' % memberCnt)
            memberMc.visible = False
            memberCnt += 1

    def setItemByGbId(self, gbId, item):
        self.gbIdItems[gbId] = item

    def getItemByGbId(self, gbId):
        return self.gbIdItems.get(gbId)

    def handleAddBtnClick(self, *args):
        addBtn = ASObject(args[3][0]).currentTarget
        if not hasattr(addBtn, 'gbId'):
            return
        menuManager.getInstance().menuTarget.apply(gbId=long(addBtn.gbId), hostId=utils.getHostId(), menuId=0)
        menuManager.getInstance().addFriend(srcId=SRC_ID.get(self.useType, const.FRIEND_SRC_MONSTER_TRIGGER))
        addBtn.visible = False

    def handleTouchBtnClick(self, *args):
        touchBtn = ASObject(args[3][0]).currentTarget
        if not hasattr(touchBtn, 'gbId') or not hasattr(touchBtn, 'roleName'):
            return
        self.uiAdapter.spaceTouch.show(long(touchBtn.gbId), touchBtn.roleName, utils.getHostId(), noZoneInfo=True)

    def onReceivedTouchInfo(self, ownerGbId, touched, useType):
        self.touchInfo[ownerGbId] = touched
        self.refreshTouchBtn(ownerGbId, touched)

    def refreshTouchBtn(self, ownerGbId, touched):
        item = self.getItemByGbId(ownerGbId)
        if item is None:
            return
        else:
            touchBtn = item.touchBtn
            if not touched:
                touchBtn.enabled = True
                TipManager.removeTip(touchBtn)
            else:
                touchBtn.enabled = False
                touchBtn.mouseEnabled = True
                TipManager.addTip(touchBtn, gameStrings.TOUCHBTN_TIPS)
            return

    def onReceivedSignTextInfo(self, ownerGbId, signText):
        self.signTextInfo[ownerGbId] = signText
        self.refreshSignText(ownerGbId, signText)

    def refreshSignText(self, ownerGbId, signText):
        item = self.getItemByGbId(ownerGbId)
        if item is None:
            return
        else:
            item.signTf.htmlText = signText
            return

    def sendTouch(self, ownerGbId):
        self.refreshTouchBtn(ownerGbId, True)
