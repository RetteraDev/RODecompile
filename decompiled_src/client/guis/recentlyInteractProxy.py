#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/recentlyInteractProxy.o
import BigWorld
import time
import math
import uiConst
import uiUtils
import const
import events
from uiProxy import UIProxy
from asObject import ASObject
from asObject import MenuManager
from gamestrings import gameStrings
from data import battle_field_data as BFD
from data import quest_loop_data as QLD
from data import fb_data as FD
from data import arena_data as AD
PERPAGE_ITEM_CNT = 4
MAX_MEMBER_CNT = 5
MIN_PAGE = 1
TIMESTAMP_IDX = 0
TYPE_IDX = 1
ID_IDX = 2
MATELIST_IDX = 3
GBID_IDX = 0
ROLENAME_IDX = 1
LEADERFLAG_IDX = 2
PHOTO_IDX = 3
SEX_IDX = 4
SCHOOL_IDX = 5

class RecentlyInteractProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RecentlyInteractProxy, self).__init__(uiAdapter)
        self.widget = None
        self.interactTeams = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RECENTLY_INTERACT, self.hide)

    def reset(self):
        self.maxPage = MIN_PAGE
        self.curPage = MIN_PAGE

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RECENTLY_INTERACT:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RECENTLY_INTERACT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RECENTLY_INTERACT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initListProp()
        self.initPageMc()
        self.getInteractTeams()

    def initListProp(self):
        self.widget.teamList.itemRenderer = 'RecentlyInteract_Item'
        self.widget.teamList.lableFunction = self.itemLabelFunc

    def initPageMc(self):
        self.widget.pageMc.headBtn.addEventListener(events.BUTTON_CLICK, self.handleHeadBtnClick, False, 0, True)
        self.widget.pageMc.tailBtn.addEventListener(events.BUTTON_CLICK, self.handleTailBtnClick, False, 0, True)
        self.widget.pageMc.pageMc.prevBtn.addEventListener(events.BUTTON_CLICK, self.handlePrevBtnClick, False, 0, True)
        self.widget.pageMc.pageMc.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)
        self.updatePageMc()

    def updatePageMc(self):
        if not self.widget:
            return
        self.maxPage = math.ceil(float(len(self.interactTeams)) / PERPAGE_ITEM_CNT)
        if self.maxPage <= MIN_PAGE:
            self.widget.pageMc.visible = False
        else:
            self.widget.pageMc.visible = True
            self.widget.pageMc.pageMc.textField.text = '%d/%d' % (self.curPage, self.maxPage)
            self.widget.pageMc.headBtn.enabled = self.curPage != MIN_PAGE
            self.widget.pageMc.tailBtn.enabled = self.curPage != self.maxPage
            self.widget.pageMc.pageMc.prevBtn.enabled = self.curPage != MIN_PAGE
            self.widget.pageMc.pageMc.nextBtn.enabled = self.curPage != self.maxPage

    def getInteractTeams(self):
        BigWorld.player().base.getInteractTeams()

    def onGetInteractTeams(self, interactTeamList):
        interactTeamList.sort(key=lambda item: item[0], reverse=True)
        self.interactTeams = interactTeamList
        self.updatePageMc()
        self.updateScrollList()

    def updateScrollList(self, needReset = True):
        if not self.widget:
            return
        self.widget.teamList.dataArray = self.getPageListData()
        self.widget.teamList.validateNow()
        needReset and self.widget.teamList.scrollToHead()

    def getPageListData(self):
        startPos = int((self.curPage - 1) * PERPAGE_ITEM_CNT)
        endPos = startPos + PERPAGE_ITEM_CNT
        if endPos < len(self.interactTeams):
            return self.interactTeams[startPos:endPos]
        else:
            return self.interactTeams[startPos:]

    def itemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        self.refreshItemInfo(item, itemData)
        self.refreshMembersInfo(item, itemData)

    def refreshItemInfo(self, item, itemData):
        item.titleTf.htmlText = self.getItemTitleStr(itemData[TYPE_IDX], itemData[ID_IDX])
        item.timeTf.htmlText = self.getItemTimeStr(itemData[TIMESTAMP_IDX])

    def getItemTitleStr(self, itemType, itemId):
        if itemType == const.INTERACTION_GROUP_INVITE_TYPE_QUEST_LOOP:
            itemName = QLD.data.get(itemId, {}).get('name', '')
        elif itemType == const.INTERACTION_GROUP_INVITE_TYPE_FB:
            fbName = FD.data.get(itemId, {}).get('name', '')
            fbPrimaryLevelName = FD.data.get(itemId, {}).get('primaryLevelName', '')
            fbModeName = FD.data.get(itemId, {}).get('modeName', '')
            itemName = '%s %s %s' % (fbName, fbPrimaryLevelName, fbModeName)
        elif itemType == const.INTERACTION_GROUP_INVITE_TYPE_BATTLE:
            itemName = BFD.data.get(itemId, {}).get('name', '')
        elif itemType == const.INTERACTION_GROUP_INVITE_TYPE_JJC:
            itemName = AD.data.get(itemId, {}).get('name', '')
        else:
            itemName = ''
        return itemName

    def getItemTimeStr(self, timeStamp):
        t = time.localtime(timeStamp)
        return '%d-%.2d-%.2d %.2d:%.2d' % (t.tm_year,
         t.tm_mon,
         t.tm_mday,
         t.tm_hour,
         t.tm_min)

    def refreshMembersInfo(self, item, itemData):
        members = itemData[MATELIST_IDX]
        memberCnt = len(members)
        for idx in xrange(MAX_MEMBER_CNT):
            memberMc = getattr(item, 'member%d' % idx)
            if idx >= memberCnt:
                memberMc.visible = False
            else:
                pInfo = members[idx]
                roleName = pInfo[ROLENAME_IDX]
                gbId = long(pInfo[GBID_IDX])
                self.refreshMemberPhoto(memberMc.photoIcon, gbId, pInfo[PHOTO_IDX], pInfo[SEX_IDX], pInfo[SCHOOL_IDX])
                memberMc.leaderIcon.visible = bool(pInfo[LEADERFLAG_IDX])
                label = self.getLabelFrameName(gbId)
                memberMc.labelMc.visible = bool(label)
                label and memberMc.labelMc.gotoAndStop(label)
                memberMc.nameTf.text = roleName
                memberMc.visible = True
                memberMc.roleName = roleName
                memberMc.addEventListener(events.MOUSE_CLICK, self.handleMemberMcClick, False, 0, True)

    def refreshMemberPhoto(self, iconMc, gbId, photo, sex, school):
        p = BigWorld.player()
        iconMc.setContentUnSee()
        iconMc.fitSize = True
        if p.gbId == gbId:
            iconMc.imgType = uiConst.IMG_TYPE_NOS_FILE
            iconMc.url = p._getFriendPhoto(p)
        elif not photo:
            photo = p.friend.getDefaultPhoto(school, sex)
            iconMc.loadImage(photo)
        else:
            iconMc.imgType = uiConst.IMG_TYPE_NOS_FILE
            iconMc.url = photo

    def getLabelFrameName(self, gbId):
        p = BigWorld.player()
        if p.gbId == gbId:
            return ''
        elif uiUtils.isJieQiTgt(gbId):
            return 'isCouple'
        elif uiUtils.isZhenChuanTgt(gbId):
            return 'isZhenChuan'
        elif uiUtils.isPartner(gbId):
            return 'isPartner'
        elif uiUtils.isMentor(gbId) or uiUtils.isApprentice(gbId):
            return 'isShitu'
        elif p.friend.isFriend(gbId):
            return 'isFriend'
        elif uiUtils.isSameGuild(gbId):
            return 'isGuild'
        else:
            return ''

    def handleHeadBtnClick(self, *args):
        self.curPage = MIN_PAGE
        self.updatePageMc()
        self.updateScrollList()

    def handleTailBtnClick(self, *args):
        self.curPage = self.maxPage
        self.updatePageMc()
        self.updateScrollList()

    def handlePrevBtnClick(self, *args):
        self.curPage = max(MIN_PAGE, self.curPage - 1)
        self.updatePageMc()
        self.updateScrollList()

    def handleNextBtnClick(self, *args):
        self.curPage = min(self.maxPage, self.curPage + 1)
        self.updatePageMc()
        self.updateScrollList()

    def handleMemberMcClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            roleName = e.currentTarget.roleName
            BigWorld.player().cell.getRoleInfo(roleName)
