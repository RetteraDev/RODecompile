#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryInvitationCardProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_plan_data as MPD
from cdata import marriage_subscribe_date_data as MSDD

class MarryInvitationCardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryInvitationCardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_INVITATION_CARD, self.hide)

    def reset(self):
        self.selectedBtn = None
        self.marriageInfo = None
        self.customMessage = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_INVITATION_CARD:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_INVITATION_CARD)

    def show(self, marriageInfo):
        self.marriageInfo = marriageInfo
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_INVITATION_CARD)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        mType = self.marriageInfo.get('package', {}).get('mType', 1)
        if mType == gametypes.MARRIAGE_TYPE_PACKAGE:
            self.widget.gotoAndStop('type1')
        else:
            self.widget.gotoAndStop('type2')
        self.widget.defaultCloseBtn = self.widget.canvas.closeBtn
        ASUtils.setHitTestDisable(self.widget.canvas.bg, True)

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        else:
            serverId = self.marriageInfo.get('mainHostId', 0)
            mType = self.marriageInfo.get('package', {}).get('mType', 0)
            member = self.marriageInfo.get('member', {})
            for gbId, roleInfo in member.iteritems():
                roleType = roleInfo.get('roleType', 0)
                photo = roleInfo.get('photo', 0)
                roleName = roleInfo.get('roleName', 0)
                school = roleInfo.get('school', 0)
                sex = roleInfo.get('sex', 0)
                curIcon = None
                roleNameTxt = None
                if roleType == gametypes.MARRIAGE_ROLE_TYPE_HUSBAND:
                    curIcon = self.widget.canvas.mainMc.contentMc.icon1
                elif roleType == gametypes.MARRIAGE_ROLE_TYPE_WIFE:
                    curIcon = self.widget.canvas.mainMc.contentMc.icon2
                if roleType == gametypes.MARRIAGE_ROLE_TYPE_HUSBAND:
                    roleNameTxt = self.widget.canvas.mainMc.contentMc.roleName1
                elif roleType == gametypes.MARRIAGE_ROLE_TYPE_WIFE:
                    roleNameTxt = self.widget.canvas.mainMc.contentMc.roleName2
                if curIcon:
                    photoInfo = {'photo': photo,
                     'school': school,
                     'sex': sex}
                    curIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
                    curIcon.fitSize = True
                    if mType == gametypes.MARRIAGE_TYPE_GREAT and serverId:
                        curIcon.serverId = serverId
                    curIcon.url = self.getFriendPhoto(photoInfo)
                if roleNameTxt:
                    roleNameTxt.htmlText = roleName

            self.widget.canvas.mainMc.contentMc.customMsg.text = self.customMessage
            packageInfo = self.marriageInfo.get('package', {})
            month = packageInfo.get('month', 0)
            day = packageInfo.get('day', 0)
            timeIndex = packageInfo.get('timeIndex', 0)
            self.widget.canvas.mainMc.contentMc.timeStr.htmlText = self.getTimeStrFormat(month, day, timeIndex)
            return

    def getTimeStrFormat(self, month, day, timeIndex):
        timeData = MSDD.data.get(timeIndex, {})
        beginTimeTuple = timeData.get('beginTimeTuple', [])
        endTimeTuple = timeData.get('endTimeTuple', [])
        marriageStartTimeDesc = gameStrings.MARRY_INVITATION_CARD_DATE % (month,
         day,
         beginTimeTuple[0],
         beginTimeTuple[1],
         endTimeTuple[0],
         endTimeTuple[1])
        return marriageStartTimeDesc

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def openInvitationCard(self, mNUID, customMessage):
        self.customMessage = customMessage
        p = BigWorld.player()
        p.cell.queryMarriageInfo(long(mNUID))

    def getFriendPhoto(self, friendInfo):
        return self.uiAdapter.marrySettingBg.getFriendPhoto(friendInfo)
