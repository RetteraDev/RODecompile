#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marrySettingBgProxy.o
import BigWorld
import gameglobal
import gametypes
import uiConst
import const
from uiTabProxy import UITabProxy
from helpers import taboo
MARRY_TAB_INVITE_FRIEND = 0
MARRY_TAB_INVITE_MANWOMAN = 1
MARRY_TAB_PLAN_SETTING = 2

class MarrySettingBgProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(MarrySettingBgProxy, self).__init__(uiAdapter)
        self.frindCache = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_SETTING_BG, self.hide)

    def reset(self):
        super(MarrySettingBgProxy, self).reset()
        self.marriageInfo = {}

    def clearAll(self):
        self.frindCache = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_SETTING_BG:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(MarrySettingBgProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_SETTING_BG)

    def _getTabList(self):
        return [{'tabIdx': MARRY_TAB_INVITE_FRIEND,
          'tabName': 'tabBtn0',
          'view': 'MarryInviteFriendWidget',
          'proxy': 'marryInviteFriend'}, {'tabIdx': MARRY_TAB_INVITE_MANWOMAN,
          'tabName': 'tabBtn1',
          'view': 'MarryInviteManWomanWidget',
          'proxy': 'marryInviteManWoman'}, {'tabIdx': MARRY_TAB_PLAN_SETTING,
          'tabName': 'tabBtn2',
          'view': 'MarryPlanSettingWidget',
          'proxy': 'marryPlanSetting'}]

    def show(self, tabIndex = 0, marriageInfo = {}):
        if marriageInfo:
            self.marriageInfo = marriageInfo
        self.showTabIndex = tabIndex
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_SETTING_BG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(MARRY_TAB_INVITE_FRIEND)
        else:
            self.widget.setTabIndex(self.showTabIndex)

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def onTabChanged(self, *args):
        super(MarrySettingBgProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def getFriendPhoto(self, friendInfo):
        if not friendInfo:
            return ''
        if isinstance(friendInfo, dict):
            photo = friendInfo.get('photo', '')
            school = friendInfo.get('school', '')
            sex = friendInfo.get('sex', '')
        else:
            photo = friendInfo.photo
            school = friendInfo.school
            sex = friendInfo.sex
        if photo:
            return photo
        elif school and sex:
            return 'headIcon/%s.dds' % str(school * 10 + sex)
        else:
            return 'headIcon/%s.dds' % str(school * 10 + sex)

    def openMarrySetting(self):
        p = BigWorld.player()
        if p.marriageNUID:
            p.cell.queryMarriageInfo(p.marriageNUID)

    def getCurServerMarriageType(self):
        mType = self.marriageInfo.get('package', {}).get('mType', 0)
        subType = self.marriageInfo.get('package', {}).get('subType', 0)
        return (mType, subType)

    def getCurServerPackageList(self):
        packageList = self.marriageInfo.get('package', {}).get('packageList', [])
        return packageList

    def getCurServerManAndWomanMap(self):
        bestmanDict = self.marriageInfo.get('bestmanMember', {})
        bridesmaidDict = self.marriageInfo.get('bridesmaidMember', {})
        return (bestmanDict, bridesmaidDict)

    def getCurServerGuestMap(self):
        return self.marriageInfo.get('guestMember', {})

    def getCurServerMember(self):
        member = self.marriageInfo.get('member', {})
        return member

    def getCurServerAllowGuest(self):
        allowGuestCnt = self.marriageInfo.get('allowGuestCnt', {})
        return allowGuestCnt

    def onSetMarriagePackage(self, mType, subType, packageList, curMarriageGuestCnt):
        if self.widget:
            self.marriageInfo['package']['mType'] = mType
            self.marriageInfo['package']['subType'] = subType
            self.marriageInfo['package']['packageList'] = packageList
            self.marriageInfo['allowGuestCnt'] = curMarriageGuestCnt
            self.refreshInfo()

    def onSetMarriageGuests(self, guestDict):
        if self.widget:
            self.marriageInfo['guestMember'] = guestDict
            self.checkFriendData(gametypes.MARRIAGE_QUERY_TYPE_REFRESH_SETTING)

    def onSetExtendGuest(self, curMarriageGuestCnt):
        if self.widget:
            self.marriageInfo['allowGuestCnt'] = curMarriageGuestCnt

    def onSetMarriageMaids(self, bridesmaidDict, bestmanDict):
        if self.widget:
            self.marriageInfo['bridesmaidMember'] = bridesmaidDict
            self.marriageInfo['bestmanMember'] = bestmanDict
            self.checkFriendData(gametypes.MARRIAGE_QUERY_TYPE_REFRESH_SETTING)

    def openByMarriageInfo(self, marriageInfo):
        self.marriageInfo = marriageInfo
        self.checkFriendData(gametypes.MARRIAGE_QUERY_TYPE_OPEN_SETTING)

    def checkFriendData(self, opType):
        guestMap = self.getCurServerGuestMap()
        manMap, womanMap = self.getCurServerManAndWomanMap()
        needPatchData = []
        serverIdList = []
        p = BigWorld.player()
        for gbId, value in guestMap.iteritems():
            if self.needPatchGbId(gbId, needPatchData):
                needPatchData.append(gbId)
                serverIdList.append(value.get('srcHostId', 0))

        for gbId, value in manMap.iteritems():
            if self.needPatchGbId(gbId, needPatchData):
                needPatchData.append(gbId)
                serverIdList.append(value.get('srcHostId', 0))

        for gbId, value in womanMap.iteritems():
            if self.needPatchGbId(gbId, needPatchData):
                needPatchData.append(gbId)
                serverIdList.append(value.get('srcHostId', 0))

        if not needPatchData:
            self.onMarriageQueryFriendData(opType, {})
            return True
        p.queryMarriageUnitInfoEx(opType, serverIdList, needPatchData)

    def needPatchGbId(self, gbId, needPatchData):
        if not self.getFriendInfo(gbId) and gbId not in needPatchData and gbId not in const.VIRTUAL_FRIEND_SET:
            return True
        return False

    def onMarriageQueryFriendData(self, opType, friendInfo):
        self.frindCache.update(friendInfo)
        if opType == gametypes.MARRIAGE_QUERY_TYPE_OPEN_SETTING:
            self.show()
        elif opType == gametypes.MARRIAGE_QUERY_TYPE_REFRESH_SETTING:
            self.refreshInfo()
        elif opType == gametypes.MARRIAGE_QUERY_TYPE_INVITE_MAN_PAGE:
            self.uiAdapter.marryInviteManWoman.refreshRightList()
        elif opType == gametypes.MARRIAGE_QUERY_TYPE_INVITE_FRIEND_PAGE:
            self.uiAdapter.marryInviteFriend.refreshRightList()

    def getFriendInfo(self, gbId):
        p = BigWorld.player()
        if gbId in self.frindCache:
            info = self.frindCache.get(gbId)
            info['gbId'] = gbId
            info['name'] = info['roleName']
            return info
        return {}

    def tabooCheck(self, msg):
        isNormal1, msg1 = taboo.checkDisbWord(msg)
        isNormal2, msg2 = taboo.checkBSingle(msg)
        return isNormal1 and isNormal2

    def switchToUpgradePlan(self):
        if self.widget:
            self.widget.setTabIndex(MARRY_TAB_PLAN_SETTING)
