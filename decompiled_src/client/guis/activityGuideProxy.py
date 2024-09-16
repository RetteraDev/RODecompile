#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityGuideProxy.o
import BigWorld
import gameglobal
import time
import random
import gameconfigCommon
import const
import utils
import uiConst
import keys
from guis import events
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
from uiProxy import UIProxy
from data import activity_guide_data as AGD
from data import activity_guide_entry_data as AGED
from data import hand_in_item_data as HIID
from cdata import hand_in_item_crystal_data as HIICD
ACTIVITY_MAX_CNT = 6
REWARD_ITEM_MAX_CNT = 8
CRYSTAL_ITEM_MAX_CNT = 5
CHECK_TYPE_NONE = '0'
CHECK_TYPE_TODAY = '1'
CHECK_TYPE_WEEK = '2'
THEME_ZHENHUNJIE = 'zhenhunjie'
THEME_CRYSTAL_DEFENCE = 'crystalDefence'
THEME_DATU = 'datu'
THEME_CHUNJIE = 'chunjie'
THEME_QINGDI = 'qingdi'
CONTENT_STYLE_ORDINARY = 1
CONTENT_STYLE_CRYSTAL = 2
CONTENT_STYLE_NOTHING = 3

class ActivityGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityGuideProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.pushed = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_GUIDE, self.handleCloseBtnClick)

    def reset(self):
        self.bgFrame = None
        self.selectedKey = 0
        self.subContentStyle = 1
        self.activityMap = {}
        self.mainTabKeyList = []
        self.titleId = 0
        self.subInfo = None
        self.checkType = None
        self.lastMc = None
        self.checkTodayMc = None
        self.checkWeekMc = None
        self.subIdx = 0
        self.mainContentMc = None

    def genActivityMap(self):
        if not self.checkActivityMapNeedUpdate():
            return self.activityMap
        if self.activityMap:
            self.activityMap.clear()
        else:
            self.activityMap = dict()
        for key, info in AGD.data.iteritems():
            mainTab, subTab = key
            if subTab == 0:
                continue
            startTime = info.get('startTime', '')
            endTime = info.get('endTime', '')
            minLv = info.get('minLv', 0)
            maxLv = info.get('maxLv', 999)
            p = BigWorld.player()
            if utils.inCrontabRange(startTime, endTime) and minLv <= p.lv <= maxLv:
                nextEnd = utils.getNextCrontabTime(endTime)
                subInfo = {}
                subInfo['leftTime'] = int(max(0, nextEnd - utils.getNow()))
                subInfo['key'] = key
                subInfo['time'] = (utils.getPreCrontabTime(startTime), utils.getNextCrontabTime(endTime))
                subInfo['titleImg'] = info.get('titleImg', '')
                subInfo['mainTitleName'] = self.getMainTitleNameByKey(mainTab)
                subInfo['contentDesc'] = info.get('contentDesc', '')
                subInfo['rewardItemList'] = info.get('rewardItemList', '')
                subInfo['sortOrder'] = info.get('sortOrder', 5)
                subInfo['linkText'] = info.get('linkText', '')
                subInfo['avatarIcon'] = info.get('avatarIcon', 'default')
                subInfo['showTime'] = info.get('showTime', 1)
                subInfo['label'] = info.get('label', '')
                subInfo['bgFrame'] = info.get('bgFrame', THEME_ZHENHUNJIE)
                subInfo['contentStyle'] = info.get('contentStyle', 1)
                subInfo['crystalTitle'] = info.get('crystalTitle', ())
                subInfo['crystalTips'] = info.get('crystalTips', '')
                subInfo['activityID'] = info.get('activityID', '')
                subInfo['HandInItemID'] = info.get('HandInItem', 1)
                subInfo['helpID'] = info.get('helpID', 0)
                self.activityMap.setdefault(mainTab, []).append(subInfo)

        for mainTabKey, infoList in self.activityMap.iteritems():
            infoList.sort(cmp=lambda a, b: cmp(a['sortOrder'], b['sortOrder']))

        return self.activityMap

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTIVITY_GUIDE:
            self.widget = widget
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_GUIDE_OPEN)
            self.refreshUI()

    def handleCloseBtnClick(self, *args):
        self.hide()
        gameglobal.rds.ui.activityGuideIcon.show()

    def show(self, titleId = 0, showErrMsg = True):
        if not gameconfigCommon.enableActivityGuide():
            return
        if BigWorld.player()._isSoul() or BigWorld.player().mapID != const.SPACE_NO_BIG_WORLD:
            showErrMsg and BigWorld.player().showTopMsg(gameStrings.ACTIVITY_GUIDE_SHOW_LIMIT_MSG)
            return
        self.genActivityMap()
        if not titleId:
            titleId = self.getActiveTitleID()
        self.titleId = titleId
        self.mainTabKeyList = self.getMainTabKeyList(titleId)
        if not self.mainTabKeyList:
            return
        self.selectedKey = self.mainTabKeyList[0]
        self.bgFrame = self.getCurBgFrame()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACTIVITY_GUIDE)

    def refreshUI(self):
        if not self.widget:
            return
        else:
            if self.bgFrame:
                self.widget.gotoAndStop(self.bgFrame)
            else:
                self.widget.gotoAndStop(1)
            self.subInfo = self.getCurSubInfo()
            if not self.subInfo:
                return
            self.subContentStyle = self.getCurContentStyle()
            titleIconMc = None
            txtTimeMc = None
            txtLeftTimeMc = None
            iconMc = None
            sureBtnMc = None
            self.mainContentMc = self.widget.mainMc.content
            if self.bgFrame == THEME_ZHENHUNJIE:
                if self.subContentStyle == CONTENT_STYLE_ORDINARY:
                    titleIconMc = self.widget.mainMc.titleIcon
                    txtTimeMc = self.widget.mainMc.content.txtTime
                    txtLeftTimeMc = self.widget.mainMc.content.txtLeftTime
                    sureBtnMc = self.widget.mainMc.content.sure.gotoBtn
                    iconMc = self.widget.mainMc.icon
                    self.checkTodayMc = self.widget.mainMc.content.checkToday
                    self.checkWeekMc = self.widget.mainMc.content.checkWeek
                    self.mainContentMc = self.widget.mainMc.content
                    self.refrshIcon(iconMc)
                    self.refreshMainContent(self.widget.mainMc.content, 1)
            elif self.bgFrame == THEME_CRYSTAL_DEFENCE:
                self.widget.mainMc.content.gotoAndStop('content%d' % self.subContentStyle)
                curContentMc = getattr(self.widget.mainMc.content, 'content%d' % self.subContentStyle, None)
                if not curContentMc:
                    return
                self.mainContentMc = curContentMc
                titleIconMc = curContentMc.titleIcon
                txtTimeMc = curContentMc.txtTime
                txtLeftTimeMc = curContentMc.txtLeftTime
                sureBtnMc = curContentMc.sure
                if self.subContentStyle == CONTENT_STYLE_ORDINARY:
                    self.checkTodayMc = self.widget.mainMc.content.checkToday
                    self.checkWeekMc = self.widget.mainMc.content.checkWeek
                    iconMc = self.widget.mainMc.content.icon
                    self.refrshIcon(iconMc)
                    self.refreshMainContent(curContentMc, 2)
                elif self.subContentStyle == CONTENT_STYLE_CRYSTAL:
                    self.checkTodayMc = curContentMc.checkToday
                    self.checkWeekMc = curContentMc.checkWeek
                    self.refreshCrystalContent1(curContentMc)
                    self.refreshCrystalContent2(curContentMc)
                    self.refreshCrystalContent3(curContentMc)
            elif self.bgFrame == THEME_DATU:
                self.widget.mainMc.content.gotoAndStop('content%d' % self.subContentStyle)
                curContentMc = getattr(self.widget.mainMc.content, 'content%d' % self.subContentStyle, None)
                if not curContentMc:
                    return
                self.mainContentMc = curContentMc
                titleIconMc = curContentMc.titleIcon
                txtTimeMc = curContentMc.txtTime
                txtLeftTimeMc = curContentMc.txtLeftTime
                sureBtnMc = curContentMc.sure
                self.checkTodayMc = curContentMc.checkToday
                self.checkWeekMc = curContentMc.checkWeek
                if self.subContentStyle == CONTENT_STYLE_CRYSTAL:
                    self.refreshCrystalContent1(curContentMc)
                    self.refreshCrystalContent2(curContentMc)
                    self.refreshCrystalContent4(curContentMc)
                    self.refreshCrystalContent5(curContentMc)
                elif self.subContentStyle == CONTENT_STYLE_NOTHING:
                    self.refreshNothingContent(curContentMc)
            elif self.bgFrame == THEME_CHUNJIE:
                self.widget.mainMc.content.gotoAndStop('content%d' % self.subContentStyle)
                curContentMc = getattr(self.widget.mainMc.content, 'content%d' % self.subContentStyle, None)
                if not curContentMc:
                    return
                self.mainContentMc = curContentMc
                titleIconMc = curContentMc.titleIcon
                txtTimeMc = curContentMc.txtTime
                txtLeftTimeMc = curContentMc.txtLeftTime
                sureBtnMc = curContentMc.sure
                if self.subContentStyle == CONTENT_STYLE_ORDINARY:
                    self.checkTodayMc = self.widget.mainMc.content.checkToday
                    self.checkWeekMc = self.widget.mainMc.content.checkWeek
                    iconMc = self.widget.mainMc.content.icon
                    self.refrshIcon(iconMc)
                    self.refreshMainContent(curContentMc, 4)
            elif self.bgFrame == THEME_QINGDI:
                self.widget.mainMc.content.gotoAndStop('content%d' % self.subContentStyle)
                curContentMc = getattr(self.widget.mainMc.content, 'content%d' % self.subContentStyle, None)
                if not curContentMc:
                    return
                self.mainContentMc = curContentMc
                titleIconMc = curContentMc.titleIcon
                txtTimeMc = curContentMc.txtTime
                txtLeftTimeMc = curContentMc.txtLeftTime
                sureBtnMc = curContentMc.sure
                if self.subContentStyle == CONTENT_STYLE_ORDINARY:
                    self.checkTodayMc = self.widget.mainMc.content.checkToday
                    self.checkWeekMc = self.widget.mainMc.content.checkWeek
                    iconMc = self.widget.mainMc.content.icon
                    self.refrshIcon(iconMc)
                    self.refreshMainContent(curContentMc, 5)
            self.refreshCommonUI()
            self.showHelpKey(self.mainContentMc)
            self.refreshTabs()
            self.refreshTitle(titleIconMc)
            self.refreshShowTime(txtTimeMc, txtLeftTimeMc)
            self.refreshSureBtn(sureBtnMc)
            self.refreshCheck(self.checkTodayMc, self.checkWeekMc)
            return

    def clearAll(self):
        self.activityMap.clear()
        self.pushed = False

    def clearWidget(self):
        if self.widget is None:
            return
        else:
            self.saveCheckTimeData()
            self.widget = None
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTIVITY_GUIDE)
            return

    def refreshCommonUI(self):
        self.widget.mainMc.content.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)

    def refreshTabs(self):
        if not self.widget or not self.widget.mainMc.allTabs:
            return
        for i in xrange(ACTIVITY_MAX_CNT):
            tabMc = self.widget.mainMc.allTabs.getChildByName('tab%d' % i)
            if not tabMc:
                continue
            if i < len(self.mainTabKeyList):
                tabMc.visible = True
                tabMc.gotoAndStop('open')
                tabMc.btn.data = self.mainTabKeyList[i]
                tabMc.btn.label = self.getMainTitleNameByKey(self.mainTabKeyList[i])
                tabMc.btn.addEventListener(events.BUTTON_CLICK, self.handleTabMcBtnClick, False, 0, True)
                tabMc.btn.selected = self.mainTabKeyList[i] == self.selectedKey
                if tabMc.btn.selected:
                    self.lastMc = tabMc.btn
                    if tabMc.selectedEff:
                        ASUtils.setHitTestDisable(tabMc.selectedEff, True)
                        tabMc.selectedEff.visible = True
                        tabMc.selectedEff.gotoAndPlay(1)
                        tabMc.selectedEff.textField.text = self.getMainTitleNameByKey(self.mainTabKeyList[i])
                elif tabMc.selectedEff:
                    tabMc.selectedEff.visible = False
            else:
                tabMc.gotoAndStop('close')

    def handleTabMcBtnClick(self, *args):
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.data)
        if idx != self.selectedKey:
            self.selectedKey = idx
            self.subIdx = 0
            if self.lastMc:
                self.lastMc.selected = False
            self.lastMc = e.currentTarget
            self.lastMc.selected = True
            self.refreshUI()

    def refreshTitle(self, titleIconMc):
        if not titleIconMc:
            return
        titleIconMc.fitSize = True
        titleIconMc.loadImage('activityGuide/%s.dds' % self.subInfo['titleImg'])

    def refreshShowTime(self, txtTimeMc, txtLeftTimeMc):
        if not txtTimeMc or not txtLeftTimeMc:
            return
        if self.subInfo['showTime']:
            txtTimeMc.visible = True
            txtLeftTimeMc.visible = True
            startTime, endTime = self.subInfo['time']
            ts = time.localtime(startTime)
            te = time.localtime(endTime)
            txtTimeMc.text = gameStrings.ACTIVITY_GUIDE_TIME % (ts.tm_mon,
             ts.tm_mday,
             ts.tm_hour,
             ts.tm_min,
             te.tm_mon,
             te.tm_mday,
             te.tm_hour,
             te.tm_min)
            txtLeftTimeMc.text.text = utils.formatTimeStr(self.subInfo['leftTime'], gameStrings.ACTIVITY_GUILD_LEFT_TIME)
        else:
            txtTimeMc.visible = False
            txtLeftTimeMc.visible = False

    def refreshSureBtn(self, sureBtnMc):
        if not sureBtnMc:
            return
        if self.subInfo['label']:
            sureBtnMc.linkText = self.subInfo['linkText']
            sureBtnMc.label = self.subInfo['label']
            sureBtnMc.visible = True
        else:
            sureBtnMc.visible = False

    def refreshCheck(self, checkTodayMc, checkWeekMc):
        if not checkTodayMc or not checkWeekMc:
            return
        checkTodayMc.validateNow()
        checkWeekMc.validateNow()
        checkTodayMc.groupName = 'activityGuideCheck'
        checkWeekMc.groupName = 'activityGuideCheck'
        checkTodayMc.toggle = True
        checkWeekMc.toggle = True
        checkType, checkTime = self.getCheckTime()
        if checkTime > utils.getNow() and checkType == CHECK_TYPE_TODAY:
            self.checkType = CHECK_TYPE_TODAY
        elif checkTime > utils.getNow() and checkType == CHECK_TYPE_WEEK:
            self.checkType = CHECK_TYPE_WEEK
        else:
            self.checkType = CHECK_TYPE_NONE
        checkTodayMc.selected = self.checkType == CHECK_TYPE_TODAY
        checkWeekMc.selected = self.checkType == CHECK_TYPE_WEEK
        checkTodayMc.addEventListener(events.BUTTON_CLICK, self.handleCheckTodayClick, False, 0, True)
        checkWeekMc.addEventListener(events.BUTTON_CLICK, self.handleCheckWeekClick, False, 0, True)

    def handleCheckTodayClick(self, *args):
        e = ASObject(args[3][0])
        if self.checkType == CHECK_TYPE_TODAY:
            self.checkType = None
            e.currentTarget.selected = False
        else:
            self.checkType = CHECK_TYPE_TODAY
        self.saveCheckTimeData()

    def handleCheckWeekClick(self, *args):
        e = ASObject(args[3][0])
        if self.checkType == CHECK_TYPE_WEEK:
            self.checkType = None
            e.currentTarget.selected = False
        else:
            self.checkType = CHECK_TYPE_WEEK
        self.saveCheckTimeData()

    def showHelpKey(self, contentMc):
        helpIconMc = getattr(contentMc, 'helpIcon')
        if helpIconMc and self.subInfo['helpID']:
            helpIconMc.helpKey = self.subInfo['helpID']

    def refreshMainContent(self, contentMc, indicatorItemRenderName = 1):
        if not self.widget or not contentMc:
            return
        count = len(self.activityMap.get(self.selectedKey, []))
        if count == 1:
            contentMc.indicator.visible = False
        else:
            contentMc.indicator.visible = True
            contentMc.indicator.itemRender = 'ActivityGuide_Indicator%d' % indicatorItemRenderName
            contentMc.indicator.indexChangeCallback = self.indexChangeCallback
            contentMc.indicator.count = count
            contentMc.indicator.update(self.subIdx)
            contentMc.indicator.x = int(contentMc.indicator.x)
        contentMc.txtContent.htmlText = self.subInfo['contentDesc']
        rewardItemList = self.subInfo['rewardItemList']
        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemMc = contentMc.getChildByName('rewardItem%d' % i)
            if i < len(rewardItemList):
                itemMc.visible = True
                itemMc.dragable = False
                itemMc.setItemSlotData(uiUtils.getGfxItemById(rewardItemList[i][0], rewardItemList[i][1]))
                itemEffect = itemMc.itemEffect
                if not itemEffect:
                    itemEffect = self.widget.getInstByClsName('ActivityTips_MainEffect')
                    itemEffect.name = 'itemEffect'
                    itemMc.addChild(itemEffect)
                    itemEffect.width = 97
                    itemEffect.height = 56
                    ASUtils.setHitTestDisable(itemEffect, True)
                else:
                    itemEffect.gotoAndPlay(1)
            else:
                itemMc.visible = False

    def indexChangeCallback(self, *args):
        index = int(args[3][0].GetNumber())
        self.subIdx = index
        self.refreshUI()

    def refrshIcon(self, iconMc):
        if not iconMc:
            return
        iconMc.fitSize = True
        iconMc.loadImage('activityGuide/%s.dds' % self.subInfo['avatarIcon'])
        ASUtils.setHitTestDisable(iconMc, True)

    def refreshCrystalContent1(self, contentMc, progressNumsList = None):
        if not self.subInfo['crystalTitle'] or not self.subInfo['crystalTips']:
            return
        if getattr(contentMc, 'content'):
            getattr(contentMc, 'content').htmlText = self.subInfo['contentDesc']
        tipsStr = self.subInfo['crystalTips']
        titleTuple = self.subInfo['crystalTitle']
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        for crystalIdx in xrange(len(HIICD_IDTuple)):
            titleMc = getattr(contentMc, 'crystalTitle%d' % crystalIdx)
            if titleMc:
                titleMc.visible = True
                titleMc.text.text = titleTuple[crystalIdx]
            tipsMc = getattr(contentMc, 'crystalTips%d' % crystalIdx)
            if tipsMc:
                tipsMc.visible = True
                progress = 0 if not progressNumsList else progressNumsList[crystalIdx]
                tipsMc.text.text = tipsStr + '%d%%' % progress

    def refreshCrystalContent2(self, contentMc):
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        handInTotalRewardLimit = HIID.data.get(HIID_ID, {}).get('handInTotalRewardLimt')
        helpID = HIID.data.get(self.subInfo['HandInItemID'], {}).get('helpKeyID')
        curActivityID = self.subInfo['activityID']
        for crystalIdx in xrange(len(HIICD_IDTuple)):
            crystalIconMc = getattr(contentMc, 'crystalIcon%d' % crystalIdx)
            if crystalIconMc:
                crystalIconMc.gotoAndPlay(random.randint(1, 155))
                crystalIconMc.iconEffect.visible = False
                iconMc = crystalIconMc.icon
                startTime = HIICD.data.get(HIICD_IDTuple[crystalIdx], {}).get('startTime')
                hasGotReward = 0
                if not self.checkNowOverTime(startTime):
                    hasGotReward = -1
                iconData = {'actID': curActivityID,
                 'HIID_ID': HIID_ID,
                 'HIICD_ID': HIICD_IDTuple[crystalIdx],
                 'helpID': helpID,
                 'handInTotalRewardLimit': handInTotalRewardLimit,
                 'allRounds': HIICD.data.get(HIICD_IDTuple[crystalIdx], {}).get('round'),
                 'hasGotReward': hasGotReward,
                 'curSubmitNums': 0,
                 'curAllRounds': 0}
                self.updateCrystalClickData(iconMc, iconData)
                iconMc.removeEventListener(events.BUTTON_CLICK, self.handleIconMcEvent)
                iconMc.addEventListener(events.BUTTON_CLICK, self.handleIconMcEvent, False, 0, True)

        self.requestServerData(curActivityID)

    def refreshCrystalContent3(self, contentMc, updatedData = False):
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        for crystalIdx in xrange(len(HIICD_IDTuple)):
            crystalIconMc = getattr(contentMc, 'crystalIcon%d' % crystalIdx)
            if crystalIconMc:
                iconMc = crystalIconMc.icon
                if not updatedData:
                    startTime = HIICD.data.get(HIICD_IDTuple[crystalIdx], {}).get('startTime')
                    if self.checkNowOverTime(startTime):
                        ASUtils.setMcEffect(crystalIconMc, '')
                        iconMc.selected = True
                    else:
                        ASUtils.setMcEffect(crystalIconMc, 'gray')
                elif iconMc.data['curAllRounds'] >= iconMc.data['allRounds']:
                    ASUtils.setMcEffect(crystalIconMc, '')
                    iconMc.selected = False

    def refreshCrystalContent4(self, contentMc, updatedData = False):
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        for crystalIdx in xrange(len(HIICD_IDTuple)):
            crystalIconMc = getattr(contentMc, 'crystalIcon%d' % crystalIdx)
            showItemIconMc = getattr(contentMc, 'showItemIcon%d' % crystalIdx)
            if crystalIconMc and showItemIconMc:
                iconMc = crystalIconMc.icon
                iconMc2 = showItemIconMc.icon
                if not updatedData:
                    showItemIconMc.gotoAndPlay(random.randint(1, 155))
                    showItemIconMc.visible = True
                    crystalIconMc.visible = False
                    iconMc2.data = dict(iconMc.data)
                    iconMc2.removeEventListener(events.BUTTON_CLICK, self.handleIconMcEvent)
                    iconMc2.addEventListener(events.BUTTON_CLICK, self.handleIconMcEvent, False, 0, True)
                elif iconMc.data['curAllRounds'] >= iconMc.data['allRounds']:
                    showItemIconMc.visible = False
                    crystalIconMc.visible = True

    def refreshCrystalContent5(self, contentMc, updatedData = False):
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        dragon = getattr(contentMc, 'dragon', None)
        if dragon:
            if not updatedData:
                dragon.gotoAndStop('state0')
            else:
                for crystalIdx in xrange(len(HIICD_IDTuple)):
                    crystalIconMc = getattr(contentMc, 'crystalIcon%d' % crystalIdx)
                    if crystalIconMc and crystalIconMc.icon:
                        if crystalIconMc.icon.data['curAllRounds'] >= crystalIconMc.icon.data['allRounds']:
                            dragon.gotoAndStop('state%d' % (crystalIdx + 1))

    def requestServerData(self, actID):
        BigWorld.player().base.getHandInItemAllTotalData(actID)

    def refreshCrystalContentByServer(self, actID, progressDict, curSubmitNums, getRewardHIICDIDList):
        if not self.widget or actID != self.subInfo['activityID']:
            return
        HIID_ID = self.subInfo['HandInItemID']
        HIICD_IDTuple = HIID.data.get(HIID_ID, {}).get('crystalData')
        progressNumsList = list()
        for crystalIdx in xrange(len(HIICD_IDTuple)):
            crystalIconMc = getattr(self.mainContentMc, 'crystalIcon%d' % crystalIdx)
            if crystalIconMc:
                iconMc = crystalIconMc.icon
                hasGotReward = iconMc.data['hasGotReward']
                if iconMc.data['hasGotReward'] != -1:
                    hasGotReward = 1 if iconMc.data['HIICD_ID'] in getRewardHIICDIDList else 0
                iconData = {'hasGotReward': hasGotReward,
                 'curSubmitNums': curSubmitNums,
                 'curAllRounds': progressDict.get(HIICD_IDTuple[crystalIdx], 0)}
                self.updateCrystalClickData(iconMc, iconData)
                if hasGotReward == 0 and iconMc.data['curAllRounds'] >= iconMc.data['allRounds']:
                    if iconMc.data['curSubmitNums'] >= iconMc.data['handInTotalRewardLimit']:
                        crystalIconMc.iconEffect.visible = True
                progressNums = min(int(iconMc.data['curAllRounds'] * 100 / iconMc.data['allRounds']), 100)
                progressNumsList.append(progressNums)

        self.refreshCrystalContent1(self.mainContentMc, progressNumsList)
        if self.subContentStyle == CONTENT_STYLE_CRYSTAL:
            if self.bgFrame == THEME_CRYSTAL_DEFENCE:
                self.refreshCrystalContent3(self.mainContentMc, updatedData=True)
            elif self.bgFrame == THEME_DATU:
                self.refreshCrystalContent4(self.mainContentMc, updatedData=True)
                self.refreshCrystalContent5(self.mainContentMc, updatedData=True)

    def handleIconMcEvent(self, *args):
        iconMc = ASObject(args[3][0]).currentTarget
        gameglobal.rds.ui.crystalCleanseProgress.show(iconMc.data)

    def signUpOrShowCrystalMain(self):
        actID = self.subInfo['activityID']
        HIID_ID = self.subInfo['HandInItemID']
        gameglobal.rds.ui.crystalDefenceMain.signUpOrShowCrystalMain(actID, HIID_ID)

    def refreshNothingContent(self, contentMc):
        subContentMc = getattr(contentMc, 'content', None)
        if subContentMc:
            subContentMc.htmlText = self.subInfo['contentDesc']

    def getCheckTime(self):
        checkTimeStr = AppSettings.get(keys.SET_ACTIVITY_GUIDE_CHECK % BigWorld.player().gbId, '')
        if not checkTimeStr:
            return ('', 0)
        else:
            checkType = checkTimeStr[0]
            checkTime = float(checkTimeStr[1:])
            return (checkType, checkTime)

    def checkPush(self):
        if not self.pushed:
            self.pushed = True
            _, checkTime = self.getCheckTime()
            if checkTime and checkTime > utils.getNow():
                gameglobal.rds.ui.activityGuideIcon.show()
                return
            self.show(showErrMsg=False)
        else:
            gameglobal.rds.ui.activityGuideIcon.show()

    def saveCheckTimeData(self):
        if self.checkTodayMc and self.checkWeekMc:
            if self.checkTodayMc.selected:
                AppSettings[keys.SET_ACTIVITY_GUIDE_CHECK % BigWorld.player().gbId] = CHECK_TYPE_TODAY + str(utils.getDaySecond() + 86400)
            elif self.checkWeekMc.selected:
                nextTime = utils.getNextCrontabTime('0 9 * * 3')
                AppSettings[keys.SET_ACTIVITY_GUIDE_CHECK % BigWorld.player().gbId] = CHECK_TYPE_WEEK + str(nextTime)
            else:
                AppSettings[keys.SET_ACTIVITY_GUIDE_CHECK % BigWorld.player().gbId] = CHECK_TYPE_NONE + '0'
            AppSettings.save()

    def getCurBgFrame(self):
        subInfoList = self.activityMap.get(self.selectedKey, [])
        bgFrame = THEME_ZHENHUNJIE
        if subInfoList:
            bgFrame = subInfoList[0].get('bgFrame', THEME_ZHENHUNJIE)
        return bgFrame

    def getCurContentStyle(self):
        subInfoList = self.activityMap.get(self.selectedKey, [])
        contentStyle = 1
        if subInfoList:
            contentStyle = subInfoList[0].get('contentStyle', '')
        return contentStyle

    def getCurSubInfo(self):
        subActivityList = self.activityMap.get(self.selectedKey, [])
        if self.subIdx >= len(subActivityList):
            return None
        else:
            return subActivityList[self.subIdx]

    def getMainTabKeyList(self, titleId):
        mainTabKeyList = self.activityMap.keys()
        if titleId:
            guildeTabList = AGED.data.get(titleId, {}).get('guideTabList', ())
            mainTabKeyList = list(set(mainTabKeyList) & set(guildeTabList))
        mainTabKeyList.sort(cmp=self.cmpMainSortOrder)
        return mainTabKeyList

    def getActiveTitleID(self):
        if self.activityMap:
            subTabId = self.activityMap.iterkeys().next()
            for key, value in AGED.data.iteritems():
                if subTabId in value.get('guideTabList', ()):
                    return key

        else:
            return 0

    def getMainTitleNameByKey(self, keyID):
        return AGD.data.get((keyID, 0), {}).get('mainTitleName', '')

    def cmpMainSortOrder(self, keyA, keyB):
        return AGD.data.get((keyA, 0), {}).get('sortOrder', 0) - AGD.data.get((keyB, 0), {}).get('sortOrder', 0)

    def showHelpByKey(self, helpKeyId):
        gameglobal.rds.ui.showHelpByKey(helpKeyId)

    def checkNowOverTime(self, startTimeStr):
        nextTimeStamp = utils.getTimeSecondFromStr(startTimeStr)
        nowStamp = utils.getNow()
        if nowStamp >= nextTimeStamp:
            return True
        else:
            return False

    def checkActivityMapNeedUpdate(self):
        p = BigWorld.player()
        if not self.activityMap:
            return True
        for key, info in AGD.data.iteritems():
            mainTab, subTab = key
            if subTab == 0:
                continue
            startTime = info.get('startTime', '')
            endTime = info.get('endTime', '')
            minLv = info.get('minLv', 0)
            maxLv = info.get('maxLv', 999)
            if utils.inCrontabRange(startTime, endTime) and minLv <= p.lv <= maxLv:
                if key not in self.activityMap.get(mainTab, []):
                    return True

        return False

    def updateCrystalClickData(self, mc, newData = None):
        if mc and newData and type(newData) == dict:
            if mc.data:
                mcData = dict(mc.data)
                mcData.update(newData)
                mc.data = mcData
            else:
                mc.data = newData

    def test(self):
        self.uiAdapter.startRecordShowList()
        self.uiAdapter.ziXunInfo.show()
        self.show()
        self.uiAdapter.challengePassportAppoint.show()
        self.uiAdapter.stopRecordShowList()
