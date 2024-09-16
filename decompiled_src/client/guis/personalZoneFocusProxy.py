#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneFocusProxy.o
import BigWorld
import math
from guis.asObject import ASObject
from helpers import pyq_interface
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
import const
from guis import events
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class PersonalZoneFocusProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneFocusProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_FOCUS, self.hide)

    def reset(self):
        self.pageInfoList = []
        self.currentPage = 1
        self.minPage = 1
        self.maxPage = 100

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_FOCUS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_FOCUS)

    def show(self, page = 0):
        if page:
            self.currentPage = page
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_FOCUS)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'PersonalZoneFocus_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.pageCounter.count = self.currentPage
        self.widget.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange, False, 0, True)

    def getPageInfoList(self, followList):
        pageInfoList = []
        p = BigWorld.player()
        for followInfo in followList:
            pageInfo = {}
            photo = followInfo.get('photo', '')
            if not photo:
                school = followInfo.get('jobId', 1)
                sex = followInfo.get('gender', 1)
                photo = 'headIcon/%s.dds' % str(school * 10 + sex)
            borderId = followInfo.get('borderId', 0)
            serverId = int(followInfo.get('serverId', utils.getHostId()))
            roleId = int(followInfo.get('roleId', 0))
            roleName = followInfo.get('roleName', '')
            if not roleName:
                continue
            roleName = uiUtils.formatLinkZone(roleName, roleId, serverId, addServerName=True)
            borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
            pageInfo['memberInfo'] = (roleId,
             roleName,
             followInfo.get('level', 0),
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
        itemMc.focusBtn.visible = False
        itemMc.focusBtn.data = (gbId, memberName)
        itemMc.viewBtn.addEventListener(events.BUTTON_CLICK, self.handleViewBtnClick, False, 0, True)
        itemMc.focusBtn.addEventListener(events.BUTTON_CLICK, self.handleFocusBtnClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleMouseOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleMouseOut, False, 0, True)

    def handleViewBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId, serverId = e.currentTarget.data
        BigWorld.player().getPersonalSysProxy().openZoneOther(int(gbId), None, const.PERSONAL_ZONE_SRC_LINK, int(serverId))

    def cancelFollowCallback(self, rStatus, content):
        self.getMsg(self.currentPage)

    def handleFocusBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId, name = e.currentTarget.data
        msg = GMD.data.get(GMDD.data.REMOVE_CANCEL_CONFIRM, {}).get('text', 'GMDD.data.REMOVE_CANCEL_CONFIRM%s') % name
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(pyq_interface.cancelFollow, self.cancelFollowCallback, int(gbId)))

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.focusBtn.visible = True
        e.currentTarget.viewBtn.visible = True

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.focusBtn.visible = False
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

    def getMsgCallback(self, rSttus, content):
        if not self.widget:
            return
        self.maxPage = math.ceil(content.get('data', {}).get('count', 0) * 1.0 / const.PERSONAL_ZONE_FOCUS_PAGE_SIZE)
        followList = content.get('data', {}).get('list', [])
        self.pageInfoList = self.getPageInfoList(followList)
        self.widget.scrollWndList.dataArray = range(len(self.pageInfoList))
        self.widget.pageCounter.maxCount = self.maxPage

    def getMsg(self, currentPage = 1):
        pyq_interface.getFollowList(self.getMsgCallback, currentPage, const.PERSONAL_ZONE_FOCUS_PAGE_SIZE)
