#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/HomePermissionProxy.o
import BigWorld
import gameglobal
import const
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import events
from gameStrings import gameStrings
from guis import ui
from guis import uiUtils
from guis import pinyinConvert
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
PERMISSION_MC_START_POS = (0, 10)
PERMISSION_MC_OFFSET_Y = 50

class HomePermissionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HomePermissionProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_PERMISSION, self.hide)
        self._resetData()
        self.authDict = {}

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.keyLimitCnt = SCD.data.get('homeKeyMaxCnt', 5)
        self.refreshFrame()

    def show(self):
        BigWorld.player().base.queryMyRoomAuth()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_PERMISSION)

    def clearWidget(self):
        self._resetData()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_PERMISSION)
        self.authDict = {}
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def getFrameData(self):
        p = BigWorld.player()
        self.permissionData['isPublic'] = p.myHome.eroomAuthType
        self.permissionData['desc'] = SCD.data.get('homePermissionDesc', '')
        self.permissionData['keyGivenInfo'] = []
        count = 0
        for gbId, name in self.authDict.iteritems():
            info = {}
            info['name'] = name
            info['gbId'] = gbId
            count += 1
            self.permissionData['keyGivenInfo'].append(info)

        self.permissionData['keyGivenCnt'] = count
        self.friendList = []
        friendGroups = p.getFriendGroupOrder()
        for gbId, friendInfo in p.friend.iteritems():
            if friendInfo.group not in friendGroups:
                continue
            info = {}
            info['gbId'] = gbId
            info['name'] = friendInfo.getFullName()
            self.friendList.append(info)

    def hadPermission(self, gbId):
        for info in self.permissionData['keyGivenInfo']:
            if str(info['gbId']) == str(gbId):
                return True

        return False

    def refreshFrame(self, authDict = None):
        if authDict != None:
            self.authDict = authDict
        if not self.widget:
            return
        else:
            self.getFrameData()
            self.refreshPermissionSetPanel()
            if self.widget.friendList.visible:
                self.refreshFriendList()
            return

    def _initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick)
        self.widget.publicBtn.addEventListener(events.MOUSE_CLICK, self.onPublicBtnClick, False, 0, True)
        self.widget.privateBtn.addEventListener(events.MOUSE_CLICK, self.onPrivateBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCancelBtnClick, False, 0, True)
        self.widget.dropDownMenu.addEventListener(events.MOUSE_CLICK, self.onDropDownMenuClick, False, 0, True)
        self.widget.friendList.visible = False
        self.widget.friendList.closeBtn.addEventListener(events.MOUSE_CLICK, self.onFriendListCloseBtnClick, False, 0, True)
        self.widget.friendList.nameInput.addEventListener(events.EVENT_CHANGE, self.onNameInputChange, False, 0, True)
        self.widget.friendList.nameInput.maxChars = 8
        self.widget.friendList.importBtn.addEventListener(events.MOUSE_CLICK, self.onImportBtnClick, False, 0, True)
        self.widget.friendList.scrollList.itemRenderer = 'M12_DefaultCheckBoxShen'
        self.widget.friendList.scrollList.lableFunction = self.scrollListLabelFun
        self.widget.friendList.scrollList.itemHeight = 30

    def refreshPermissionSetPanel(self):
        if not self.widget:
            return
        self.widget.inviteDesc.visible = self.permissionData['keyGivenCnt'] == 0
        self.widget.publicBtn.selected = self.permissionData['isPublic'] == const.ENLARGED_ROOM_AUTH_PUBLIC
        self.widget.privateBtn.selected = not self.permissionData['isPublic'] == const.ENLARGED_ROOM_AUTH_PUBLIC
        if self.permissionData['desc']:
            self.widget.desc.text = self.permissionData['desc']
        keyGivenInfo = self.permissionData['keyGivenInfo']
        self.widget.permissionSet.keyGivenDesc.text = gameStrings.HOME_PERMISSION_PROXY_KEY_GIVEN % (self.permissionData['keyGivenCnt'], self.keyLimitCnt)
        self.widget.permissionSet.invitionBtn.enabled = self.permissionData['keyGivenCnt'] != self.keyLimitCnt
        self.widget.permissionSet.invitionBtn.addEventListener(events.MOUSE_CLICK, self.onInviteBtnClick, False, 0, True)
        for i in xrange(self.keyLimitCnt):
            mc = self.widget.permissionSet.getChildByName('member%d' % i)
            if i < self.permissionData['keyGivenCnt']:
                mc.visible = True
                mc.txtName.text = keyGivenInfo[i]['name']
                ASUtils.setMcData(mc, 'data', self.permissionData['keyGivenInfo'][i])
                mc.cancelBtn.addEventListener(events.MOUSE_CLICK, self.onCancelPermissionClick, False, 0, True)
            else:
                mc.visible = False

    @ui.callFilter(2, True)
    def onInviteBtnClick(self, *args):
        self.setFriendListVisible(True)
        self.refreshFriendList()

    def onCancelPermissionClick(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.parent.data
        gbId = int(data.gbId)
        self.removePermissionByGbId(gbId)
        self.refreshPermissionSetPanel()
        self.refreshFriendList()

    def removePermissionByGbId(self, gbId):
        for index, info in enumerate(self.permissionData['keyGivenInfo']):
            if str(info['gbId']) == str(gbId):
                self.permissionData['keyGivenInfo'].pop(index)
                self.permissionData['keyGivenCnt'] -= 1
                break

    @ui.callInCD(0.5)
    def refreshFriendList(self):
        if not self.widget:
            return
        if not self.widget.friendList.visible:
            return
        friendList = self.getFilterFriendList()
        self.refreshInviteNumDes()
        self.widget.friendList.scrollList.dataArray = friendList

    def refreshInviteNumDes(self):
        self.widget.friendList.numTxt.text = '%d/%d' % (len(self.invitedSet), self.keyLimitCnt - self.permissionData['keyGivenCnt'])

    def getFilterFriendList(self):
        return [ info for info in self.friendList if self.filterFriend(info) ]

    def filterFriend(self, info):
        result = True
        if self.searchKey:
            result = result and self.filterPinYin(self.searchKey, info['name'])
        result = result and not self.hadPermission(info['gbId'])
        result = result and not uiUtils.isJieQiTgt(info['gbId'])
        return result

    def filterPinYin(self, searchKey, name):
        pinYin = pinyinConvert.strPinyin(searchKey)
        if not pinYin:
            return False
        pinYin = pinYin.lower()
        sName = pinyinConvert.strPinyinFirst(name).lower()
        fName = pinyinConvert.strPinyin(name).lower()
        return pinYin in sName or pinYin in fName

    def scrollListLabelFun(self, *args):
        data = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        mc.width = 200
        mc.validateNow()
        mc.label = data.name
        ASUtils.setMcData(mc, 'gbId', int(data.gbId))
        contain = int(data.gbId) in self.invitedSet
        if contain and not mc.selected:
            mc.selected = True
        elif mc.selected:
            mc.selected = False
        mc.addEventListener(events.MOUSE_CLICK, self.onInviteFriendClick, False, 0, True)

    def onInviteFriendClick(self, *args):
        mc = ASObject(args[3][0]).currentTarget
        gbId = int(mc.gbId)
        if mc.selected:
            if len(self.invitedSet) + self.permissionData['keyGivenCnt'] == self.keyLimitCnt:
                mc.selected = False
            else:
                self.invitedSet.add(gbId)
        elif gbId in self.invitedSet:
            self.invitedSet.remove(gbId)
        self.refreshInviteNumDes()

    def onImportBtnClick(self, *args):
        e = ASObject(args[3][0])
        for gbId in self.invitedSet:
            info = self.getFriendInfoByGbId(gbId)
            self.permissionData['keyGivenInfo'].append(info)
            self.permissionData['keyGivenCnt'] += 1

        self.invitedSet.clear()
        self.refreshPermissionSetPanel()
        self.refreshFriendList()

    def getFriendInfoByGbId(self, gbId):
        info = {}
        friendInfo = BigWorld.player().friend.get(gbId, {})
        info['gbId'] = gbId
        info['name'] = friendInfo.getFullName()
        return info

    def onNameInputChange(self, *args):
        e = ASObject(args[3][0])
        self.searchKey = e.currentTarget.text
        self.refreshFriendList()

    def onFriendListCloseBtnClick(self, *args):
        self.setFriendListVisible(False)

    def setFriendListVisible(self, visible):
        self.widget.friendList.visible = visible
        if not visible:
            self.invitedSet = set()

    def onCloseClick(self, *args):
        self.hide()

    def onPublicBtnClick(self, *args):
        self.permissionData['isPublic'] = const.ENLARGED_ROOM_AUTH_PUBLIC

    def onPrivateBtnClick(self, *args):
        self.permissionData['isPublic'] = const.ENLARGED_ROOM_AUTH_PRIVATE

    def onConfirmBtnClick(self, *args):
        p = BigWorld.player()
        if p.myHome.eroomAuthType != self.permissionData['isPublic']:
            p.cell.setEnlargedRoomAuth(self.permissionData['isPublic'])
        oldPermissionSet = set(self.authDict)
        newPermissionSet = set([ info['gbId'] for info in self.permissionData['keyGivenInfo'] ])
        addSet = newPermissionSet - oldPermissionSet
        delSet = oldPermissionSet - newPermissionSet
        addList = list(addSet)
        delList = list(delSet)
        nameList = [ p.friend.get(gbId).name for gbId in addList ]
        if len(addList) + len(delList) > 0:
            p.cell.updateEnlargedRoomKey(addList, nameList, delList)
        self.hide()

    def onCancelBtnClick(self, *args):
        self.refreshFrame()
        self.hide()

    def onDropDownMenuClick(self, *args):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())

    def _resetData(self):
        self.widget = None
        self.permissionData = {}
        self.friendList = []
        self.searchKey = ''
        self.invitedSet = set()
