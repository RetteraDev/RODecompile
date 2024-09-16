#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneVistorProxy.o
import BigWorld
import math
import const
import utils
from guis import uiUtils
from helpers import pyq_interface
from guis.asObject import ASObject
from guis import uiConst
from guis import events
from uiProxy import UIProxy
from gamestrings import gameStrings

class PersonalZoneVistorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneVistorProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_VISITOR, self.hide)

    def reset(self):
        self.pageInfoList = []
        self.currentPage = 1
        self.minPage = 1
        self.maxPage = 100

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_VISITOR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_VISITOR)

    def show(self, page = 0):
        if page:
            self.currentPage = page
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_VISITOR)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'PersonalZoneVistor_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.pageCounter.minCount = self.minPage
        self.widget.pageCounter.count = self.currentPage
        self.widget.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange, False, 0, True)

    def getPageInfoList(self, vistorList):
        pageInfoList = []
        p = BigWorld.player()
        for vistorInfo in vistorList:
            pageInfo = {}
            photo = vistorInfo.get('photo', '')
            if not photo:
                school = vistorInfo.get('jobId', 1)
                sex = vistorInfo.get('gender', 1)
                photo = 'headIcon/%s.dds' % str(school * 10 + sex)
            borderId = vistorInfo.get('borderId', 0)
            serverId = int(vistorInfo.get('serverId', utils.getHostId()))
            roleId = int(vistorInfo.get('roleId', 0))
            roleName = vistorInfo.get('roleName', '')
            roleName = uiUtils.formatLinkZone(roleName, roleId, serverId, addServerName=True)
            borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
            pageInfo['memberInfo'] = (roleId,
             roleName,
             vistorInfo.get('level', 0),
             photo,
             borderIcon,
             serverId)
            pageInfoList.append(pageInfo)

        return pageInfoList

    def labelFunction(self, *args):
        dataIndex = int(args[3][0].GetNumber())
        if dataIndex >= len(self.pageInfoList):
            return
        pageInfo = self.pageInfoList[dataIndex]
        itemMc = ASObject(args[3][1])
        memberInfo = pageInfo['memberInfo']
        photoMc = itemMc.headIcon
        itemMc.data = memberInfo
        gbId, memberName, lv, photo, borderIcon, serverId = memberInfo
        itemMc.txtLv.text = str(lv)
        photoMc.borderImg.fitSize = True
        photoMc.borderImg.loadImage(borderIcon)
        photoMc.icon.fitSize = True
        if utils.isDownloadImage(photo):
            photoMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            photoMc.icon.url = photo
        else:
            photoMc.icon.loadImage(photo)
        itemMc.txtName.htmlText = memberName
        itemMc.viewBtn.visible = False
        itemMc.viewBtn.data = (gbId, serverId)
        itemMc.chatBtn.visible = False
        itemMc.chatBtn.data = (gbId, memberName)
        itemMc.viewBtn.addEventListener(events.BUTTON_CLICK, self.handleViewBtnClick, False, 0, True)
        itemMc.chatBtn.addEventListener(events.BUTTON_CLICK, self.handleChatBtnClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleMouseOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleMouseOut, False, 0, True)

    def handleViewBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId, serverId = e.currentTarget.data
        BigWorld.player().getPersonalSysProxy().openZoneOther(int(gbId), None, const.PERSONAL_ZONE_SRC_LINK, int(serverId))

    def handleChatBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId, name = e.currentTarget.data
        self.uiAdapter.friend.beginChat(int(gbId))

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.chatBtn.visible = True
        e.currentTarget.viewBtn.visible = True

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.chatBtn.visible = False
        e.currentTarget.viewBtn.visible = False

    def handleCounterChange(self, *args):
        currentPage = self.widget.pageCounter.count
        if currentPage != self.currentPage:
            self.currentPage = currentPage
            self.getMsg(self.currentPage)

    def refreshInfo(self):
        if not self.widget:
            return
        self.getMsg(self.currentPage)

    def getMsgCallback(self, rStatus, content):
        if not self.widget:
            return
        vistorList = content.get('data', {}).get('list', [])
        self.maxPage = math.ceil(len(vistorList) * 1.0 / const.PERSONAL_ZONE_VISTOR_PAGE_SIZE)
        self.pageInfoList = self.getPageInfoList(vistorList)
        self.widget.scrollWndList.dataArray = range(len(self.pageInfoList))
        self.widget.pageCounter.maxCount = self.maxPage

    def getMsg(self, currentPage):
        pyq_interface.getVistorList(self.getMsgCallback, currentPage, const.PERSONAL_ZONE_VISTOR_PAGE_SIZE)
