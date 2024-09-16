#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentDetailProxy.o
import time
import math
from Scaleform import GfxValue
import BigWorld
import gameglobal
from guis import uiConst
from guis import events
from guis import uiUtils
from guis import tipUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import MenuManager
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
from data import achievement_data as AD
from data import achievement_class_data as ACD
from data import achieve_target_data as ATD
RECENT_CLASS_ID = 0
RECENT_SUB_CLASS_ID = 1
RECENT_CLASS_DETAIL_CNT = 20
COLUMN_NUM = 8
ACHIEVE_CNT_IDX = 0
TOTAL_CNT_IDX = 1
NAME_IDX = 0
CLASS_IDX = 1
EXPAND_NONE = 0
EXPAND_NONE_SHOW_PROGRESS = 1
CHECKBOX_LINE_EXPAND1 = 2
CHECKBOX_LINE_EXPAND2 = 3
ITEM_MAIN_HEIGHT = 100
ITEM_CUP_EXPAND_HEIGHT = 89
AWARD_ICON_X_OFFSET = 10
CLASS_ITEM_HEIGHT = 72
SUB_CLASS_ITEM_HEIGHT = 32
CHECKBOX_CANVAS_TOP_OFFSET = 0
CHECKBOX_CANVAS_BOTTOM_OFFSET = 15
CHECKBOX_LINE_1ITEM_X = (0,)
CHECKBOX_LINE_2ITEM_X = (0, 256)
CHECKBOX_LINE_3ITEM_X = (0, 180, 360)
CHECKBOX_LINE_ITEM_X = (0,
 CHECKBOX_LINE_1ITEM_X,
 CHECKBOX_LINE_2ITEM_X,
 CHECKBOX_LINE_3ITEM_X)
CHECKBOX_LINE_ITEM_H = 25
RANK_TEAM_HEIGHT = 34
RANK_PLAYER_HEIGHT = 29
CUP_CANVAS_TOP_OFFSET = 14
CUP_CANVAS_BOTTOM_OFFSET = 15
CUP_LINE_CNT = 2
CUP_LINE_1ITEM_X = (0,)
CUP_LINE_2ITEM_X = (0, 256)
CUP_LINE_3ITEM_X = (0, 180, 360)
CUP_LINE_ITEM_X = (0,
 CUP_LINE_1ITEM_X,
 CUP_LINE_2ITEM_X,
 CUP_LINE_3ITEM_X)
CUP_LINE_ITEM_H = 28
COLOR_UNACHIEVE = '#969696'
COLOR_ACHIEVED = '#ffc961'
CLASS_BG_PATH = 'achieve/%d.dds'
DEFAULT_ICON = 25
TARGET_IDX = 0
TIME_IDX = 1
MEMBERS_IDX = 2
MEMBER_GBID_IDX = 0
MEMBER_NAME_IDX = 1
MEMBER_INVALID_IDX = 2
MEMBER_SCHOOL_IDX = 3

class AchvmentDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentDetailProxy, self).__init__(uiAdapter)
        self.rankData = {}
        self.reset()

    def reset(self):
        self.widget = None
        self.selectAchieveId = 0
        self.selectedSubClassId = -1
        self.oldSelItem = None
        self.achieves = {}
        self.achieveTargets = {}
        self.achieveFilterData = {}
        self.classProgress = {}
        self.subClassInfo = {}
        self.expandHistory = {}
        self.classifyData = []
        self.detailData = {}
        self.groupAchievement = {}
        self.linkData = []
        self.searchInfo = {}
        self.needResetSearchText = False

    def clearAll(self):
        self.rankData = {}

    def initPanel(self, widget):
        self.widget = widget.mainMc
        self.initData()
        self.initTopRankPanel()
        self.initTreeProp()
        self.initListProp()
        self.refreshInfo()
        self.widget.searchTextInput.addEventListener(events.EVENT_CHANGE, self.onSearchChange)

    def unRegisterPanel(self):
        self.widget = None

    def initData(self):
        self.achieves = gameglobal.rds.ui.achvment.achieves
        self.achieveTargets = gameglobal.rds.ui.achvment.achieveTargets
        self.achieveFilterData = gameglobal.rds.ui.achvment.achieveFilterData
        self.subClassInfo = gameglobal.rds.ui.achvment.subClassInfo
        self.classProgress = gameglobal.rds.ui.achvment.classProgress
        self.initGroupAchieve()
        self.initClassifyData()
        self.initDetailInfo()
        if self.selectedSubClassId == -1:
            self.selectedSubClassId = RECENT_SUB_CLASS_ID

    def initClassifyData(self):
        if self.classifyData:
            return
        classSortData = sorted(ACD.data.items())
        self.classifyData = [ self.genClassifyData(classId, info) for classId, info in classSortData ]
        self.classifyData.insert(0, self.genRecentClassifyData())
        self.classifyData.sort()
        self.subClassInfo[RECENT_SUB_CLASS_ID] = (gameStrings.RECENT_CLASS_LABEL, RECENT_CLASS_ID)

    def initDetailInfo(self):
        if self.detailData and self.searchInfo:
            return
        for achieveId, info in self.achieveFilterData.iteritems():
            if self.isAchieveGroupHideItem(achieveId):
                continue
            subClassId = info.get('class')
            if subClassId not in self.detailData:
                self.detailData[subClassId] = []
            self.detailData[subClassId].append(achieveId)
            self.searchInfo[info.get('name')] = achieveId
            self.searchInfo[info.get('desc')] = achieveId

        for achieveIds in self.detailData.itervalues():
            achieveIds.sort(self.compare)

        self.detailData[RECENT_SUB_CLASS_ID] = self.getRecentAchieves()
        recentlen = len(self.detailData[RECENT_SUB_CLASS_ID])
        self.classProgress[RECENT_CLASS_ID] = (recentlen, recentlen)

    def updateExpandHistoryBySel(self):
        classId = self.subClassInfo.get(self.selectedSubClassId, ('', 0))[CLASS_IDX]
        self.expandHistory[classId] = True

    def isAchieveGroupHideItem(self, achieveId):
        group = AD.data.get(achieveId, {}).get('group')
        if not group:
            return False
        groupId, curIdx = self.getGroupInfo(group)
        maxAchievedIdx = 0
        if groupId not in self.groupAchievement:
            return True
        for idx, achieveId in self.groupAchievement[groupId].iteritems():
            if achieveId in self.achieves:
                maxAchievedIdx = max(idx, maxAchievedIdx)

        if curIdx < maxAchievedIdx:
            return True
        return False

    def getCurrentGroupAchieveId(self, groupAchieveId):
        group = AD.data.get(groupAchieveId, {}).get('group')
        if not group:
            return groupAchieveId
        groupId, curIdx = self.getGroupInfo(group)
        if groupId not in self.groupAchievement:
            return groupAchieveId
        maxAchievedIdx = 0
        curAchieveId = groupAchieveId
        for idx, achieveId in self.groupAchievement[groupId].iteritems():
            if achieveId in self.achieves:
                oldMax = maxAchievedIdx
                maxAchievedIdx = max(idx, oldMax)
                if oldMax != maxAchievedIdx:
                    curAchieveId = achieveId

        return curAchieveId

    def getRecentAchieves(self):
        sortedAchieves = sorted(self.achieves.iterkeys(), key=lambda k: self.achieves[k], reverse=True)
        ret = []
        for achieveId in sortedAchieves:
            if self.uiAdapter.achvment.isHideAchieve(achieveId):
                continue
            ret.append(achieveId)
            if len(ret) == RECENT_CLASS_DETAIL_CNT:
                break

        return ret

    def initGroupAchieve(self):
        if self.groupAchievement:
            return
        if not self.achieveFilterData:
            self.achieveFilterData = gameglobal.rds.ui.achvment.genAchieveFilterData()
        for achieveId, info in self.achieveFilterData.iteritems():
            group = info.get('group')
            if not group:
                continue
            groupId, idx = self.getGroupInfo(group)
            if groupId not in self.groupAchievement:
                self.groupAchievement[groupId] = {idx: achieveId}
            else:
                self.groupAchievement[groupId][idx] = achieveId

    def getGroupInfo(self, groupStr):
        if not groupStr:
            return (0, 0)
        groupId, idx = groupStr.split(':')
        return (int(groupId), int(idx))

    def genRecentClassifyData(self):
        return {'label': RECENT_CLASS_ID,
         'children': [RECENT_SUB_CLASS_ID],
         'expand': True}

    def genClassifyData(self, classId, info):
        childrenIds = sorted(info.get('newvalue', {}).keys())
        expand = self.expandHistory.get(classId, False)
        return {'label': classId,
         'children': childrenIds,
         'expand': expand}

    def updateClassifyData(self):
        for data in self.classifyData:
            data['expand'] = self.expandHistory.get(data['label'], False)

    def compare(self, id1, id2):
        if id1 in self.achieves and id2 not in self.achieves:
            return -1
        if id1 not in self.achieves and id2 in self.achieves:
            return 1
        return cmp(id1, id2)

    def initTreeProp(self):
        tree = self.widget.classifyTreeView.tree
        tree.itemHeights = [CLASS_ITEM_HEIGHT, SUB_CLASS_ITEM_HEIGHT]
        tree.itemRenderers = ['AchvmentDetailPanel_ClassifyGroupItem', 'AchvmentDetailPanel_ClassifyItem']
        tree.labelFunction = self.classifyGroupLabelFunc
        tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.onExpandChange, False, 0, True)

    def initTopRankPanel(self):
        self.widget.topRankPanel.visible = False
        self.widget.topRankPanel.closeRankBtn.addEventListener(events.MOUSE_CLICK, self.onCloseRankBtnClick, False, 0, True)

    def initListProp(self):
        self.widget.detailListView.itemRenderer = 'AchvmentDetailPanel_DetailItem'
        self.widget.detailListView.labelFunction = self.detailItemLabelFunc
        self.widget.detailListView.itemHeightFunction = self.itemHeightFunction

    def resetSearchText(self):
        if self.widget:
            self.widget.searchTextInput.text = ''
        else:
            self.needResetSearchText = True

    def refreshInfo(self):
        self.refreshCompleteness()
        if self.needResetSearchText:
            self.widget.searchTextInput.text = ''
            self.needResetSearchText = False
        if self.linkData:
            self.refreshLinkResult(self.linkData)
        elif self.widget.searchTextInput.text:
            self.refreshSearchResult(self.widget.searchTextInput.text)
        else:
            self.updateExpandHistoryBySel()
            self.refreshClassifyTree(self.classifyData)
            self.refreshDetailList(self.detailData.get(self.selectedSubClassId, []))

    def refreshCompleteness(self):
        currentPoint, maxPoint = gameglobal.rds.ui.achvment.getAchievementPoint()
        self.widget.achievePointTf.text = currentPoint
        self.widget.achieveTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_TEXT % len(self.achieves)

    def refreshSearchResult(self, searchText):
        self.expandHistory = {}
        retIds = list(set([ self.searchInfo[name] for name in self.searchInfo if uiUtils.isContainString(name, searchText) ]))
        self.refreshDetailList(retIds)
        self.refreshClassifyTree(self.classifyData, -1)

    def refreshLinkResult(self, achieveIds):
        self.refreshClassifyTree(self.classifyData, -1)
        self.refreshDetailList(achieveIds)
        self.linkData = []

    def refreshClassifyTree(self, listData, selectSubClassId = 0):
        self.updateClassifyData()
        if selectSubClassId:
            self.selectedSubClassId = selectSubClassId
        self.widget.classifyTreeView.tree.dataArray = listData
        self.scrollToSubClassSel(self.selectedSubClassId)

    def scrollToSubClassSel(self, selId):
        self.widget.classifyTreeView.validateNow()
        if selId != RECENT_SUB_CLASS_ID and selId != -1:
            self.widget.classifyTreeView.scrollTo(self.getSubClassSelPos(selId))
        else:
            self.widget.classifyTreeView.scrollToHead()

    def classifyGroupLabelFunc(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        if isFirst:
            rootClassData = ASObject(args[3][1])
            classId = rootClassData.label
            itemMc.classId = classId
            itemMc.nameTf.text = ACD.data.get(classId, {}).get('name', gameStrings.RECENT_CLASS_LABEL)
            achieveCnt = self.classProgress[classId][ACHIEVE_CNT_IDX]
            totalCnt = self.classProgress[classId][TOTAL_CNT_IDX]
            itemMc.cntTf.text = '%d/%d' % (achieveCnt, totalCnt)
            itemMc.progressbar.currentValue = achieveCnt
            itemMc.progressbar.maxValue = totalCnt
            itemMc.bg.fitSize = True
            itemMc.bg.loadImage(CLASS_BG_PATH % ACD.data.get(classId, {}).get('newIcon', DEFAULT_ICON))
        else:
            subClassId = int(args[3][1].GetNumber())
            isSelected = bool(self.selectedSubClassId == subClassId)
            itemMc.selected = isSelected
            itemMc.subClassId = subClassId
            itemMc.textField.text = self.subClassInfo.get(subClassId, (gameStrings.RECENT_CLASS_LABEL, 0))[NAME_IDX]
            itemMc.addEventListener(events.MOUSE_CLICK, self.onSubClassItemClick, False, 0, True)

    def refreshDetailList(self, listData):
        if self.selectAchieveId not in listData and self.isAchieveGroupHideItem(self.selectAchieveId):
            self.selectAchieveId = self.getCurrentGroupAchieveId(self.selectAchieveId)
        self.widget.searchResultTf.visible = not listData
        self.widget.detailListView.dataArray = listData
        self.widget.detailListView.validateNow()
        if self.selectAchieveId in listData:
            index = listData.index(self.selectAchieveId)
            self.widget.detailListView.scrollTo(index * ITEM_MAIN_HEIGHT)
        else:
            self.widget.detailListView.scrollTo(0)

    def detailItemLabelFunc(self, *args):
        achieveId = int(args[3][0].GetNumber())
        item = ASObject(args[3][1])
        item.achieveId = achieveId
        data = AD.data.get(achieveId, {})
        rewardTitle = data.get('rewardTitle')
        bonusId = data.get('bonusId')
        isSelected = bool(achieveId == self.selectAchieveId)
        isAchieved = bool(achieveId in self.achieves)
        item.checkboxLineTarget.visible = self.canExpandCheckBoxLine(achieveId) and isSelected
        item.cupLineTarget.visible = self.canExpandCupLine(achieveId) and isSelected
        item.nameTf.text = data.get('name')
        item.awardMc.visible = bool(rewardTitle or bonusId)
        if rewardTitle or bonusId:
            item.awardMc.x = item.nameTf.x + item.nameTf.textWidth + AWARD_ICON_X_OFFSET
            awardText = gameglobal.rds.ui.achvment.getAwardString(rewardTitle, bonusId)
            TipManager.addTip(item.awardMc, awardText, tipUtils.TYPE_DEFAULT_BLACK)
        expandType = data.get('expandType', EXPAND_NONE)
        color = COLOR_ACHIEVED if isAchieved else COLOR_UNACHIEVE
        item.progressMc.achievePointTf.htmlText = uiUtils.toHtml(data.get('rewardPoint', 0), color)
        item.progressMc.achievedTf.visible = isAchieved
        item.progressMc.progressTf.visible = not isAchieved and expandType == EXPAND_NONE_SHOW_PROGRESS
        if expandType == EXPAND_NONE_SHOW_PROGRESS and not isAchieved:
            achieveCnt, totalCnt = gameglobal.rds.ui.achvment.getAchieveProgress(achieveId)
            item.progressMc.progressTf.text = '%d/%d' % (achieveCnt, totalCnt)
            item.progressMc.currentValue = achieveCnt * 100.0 / totalCnt
        else:
            item.progressMc.currentValue = 100 * int(isAchieved)
        item.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)
        self.refreshAchieveTarget(item, achieveId, data)
        self.refreshAchieveMain(item, achieveId, data)
        isSelected and self.refreshTopRankPanel(achieveId)

    def refreshAchieveMain(self, item, achieveId, data):
        isSelected = bool(achieveId == self.selectAchieveId)
        isAchieved = bool(achieveId in self.achieves)
        itemMain = item.itemMain
        itemMain.disible = not isAchieved
        itemMain.selected = isSelected
        if isSelected:
            self.oldSelItem = itemMain
        itemMain.expandStateIcon.visible = isSelected and (self.canExpandCheckBoxLine(achieveId) or self.canExpandCupLine(achieveId))
        itemMain.collapseStateIcon.visible = not isSelected and (self.canExpandCheckBoxLine(achieveId) or self.canExpandCupLine(achieveId))
        itemMain.descTf.text = '???' if data.get('hideDesc') and not isAchieved else data.get('desc')
        itemMain.achieveDateTf.text = self.getDateText(achieveId)
        itemMain.icon.gotoAndStop(str(isAchieved))

    def refreshAchieveTarget(self, item, achieveId, data):
        if achieveId != self.selectAchieveId:
            return
        expandType = data.get('expandType', EXPAND_NONE)
        if data.get('group') and achieveId in self.achieves:
            self.refreshCupLineTarget(item.cupLineTarget, data)
        elif expandType == CHECKBOX_LINE_EXPAND1 or expandType == CHECKBOX_LINE_EXPAND2:
            self.refreshCheckBoxLineTarget(item.checkboxLineTarget, data, expandType)

    def refreshCheckBoxLineTarget(self, item, data, expandType):
        lineCnt = data.get('expandCount', 2)
        targetIds = data.get('achieveTargets', ())
        targetCnt = len(targetIds)
        isLinkExpand = bool(expandType == CHECKBOX_LINE_EXPAND2)
        if targetCnt == 0:
            return
        view = gameglobal.rds.ui.achvment.widget
        for index, targetId in enumerate(targetIds):
            box = getattr(item.canvas, 'box%d' % index)
            if not box:
                box = view.getInstByClsName('AchvmentDetailPanel_Checkbox')
                item.canvas.addChild(box)
                setattr(item.canvas, 'box%d' % index, box)
            x, y = self.getCheckboxItemPos(index, lineCnt)
            targetData = ATD.data.get(targetId, {})
            linkAchieveId = targetData.get('achieveId')
            box.fitSize = True
            box.selected = bool(targetId in self.achieveTargets and self.achieveTargets[targetId]['done'])
            box.label = AD.data.get(linkAchieveId, {}).get('name') if isLinkExpand else targetData.get('name')
            box.x = x
            box.y = y
            box.targetId = targetId
            if isLinkExpand:
                box.achieveId = linkAchieveId
                box.addEventListener(events.MOUSE_CLICK, self.onItemTargetClick, False, 0, True)
            else:
                box.achieveId = -1
                box.removeEventListener(events.MOUSE_CLICK, self.onItemTargetClick)

        for index in xrange(item.canvas.numChildren):
            box = getattr(item.canvas, 'box%d' % index)
            if box:
                box.visible = bool(index < targetCnt)

        item.bg.height = self.getCheckboxTargetMcHeight(lineCnt, targetCnt)

    def refreshCupLineTarget(self, item, data):
        lineCnt = data.get('expandCount', 2)
        groupId, curIdx = self.getGroupInfo(data.get('group'))
        if groupId not in self.groupAchievement:
            return
        groupInfo = sorted(self.groupAchievement[groupId].iteritems(), key=lambda d: d[0])
        achievedIds = [ v for k, v in groupInfo ]
        achievedIdsCnt = len(achievedIds)
        view = gameglobal.rds.ui.achvment.widget
        for i in xrange(achievedIdsCnt):
            cup = getattr(item.canvas, 'cup%d' % i)
            if not cup:
                cup = view.getInstByClsName('AchvmentDetailPanel_Cup')
                item.canvas.addChild(cup)
                setattr(item.canvas, 'cup%d' % i, cup)
            x, y = self.getCupItemPos(i, lineCnt)
            achieveId = achievedIds[i]
            isAchieved = achieveId in self.achieves
            cup.nameTf.autoSize = 'left'
            cup.nameTf.text = AD.data.get(achieveId, {}).get('desc')
            TipManager.addTip(cup, gameStrings.ACHIEVEMENT_POINT_TEXT % AD.data.get(achieveId, {}).get('rewardPoint', 0), tipUtils.TYPE_DEFAULT_BLACK, 'over', 'mouse')
            cup.x, cup.y = x, y
            cup.icon.gotoAndStop(str(isAchieved))
            if not isAchieved:
                cup.achieveId = achieveId
                cup.addEventListener(events.MOUSE_CLICK, self.onItemTargetClick, False, 0, True)
            else:
                cup.achieveId = -1
                cup.removeEventListener(events.MOUSE_CLICK, self.onItemTargetClick)

        for index in xrange(item.canvas.numChildren):
            cup = getattr(item.canvas, 'cup%d' % index)
            if cup:
                cup.visible = bool(index < achievedIdsCnt)

        item.bg.height = self.getCupTargetMcHeight(lineCnt, achievedIdsCnt)

    def getCheckboxItemPos(self, index, lineCnt):
        x = CHECKBOX_LINE_ITEM_X[lineCnt][index % lineCnt]
        y = CHECKBOX_CANVAS_TOP_OFFSET + CHECKBOX_LINE_ITEM_H * int(math.floor(index * 1.0 / lineCnt))
        return (x, y)

    def getCheckboxTargetMcHeight(self, lineCnt, targetCnt):
        return CHECKBOX_CANVAS_TOP_OFFSET + CHECKBOX_LINE_ITEM_H * int(math.ceil(targetCnt * 1.0 / lineCnt)) + CHECKBOX_CANVAS_BOTTOM_OFFSET

    def getCupItemPos(self, index, lineCnt):
        x = CUP_LINE_ITEM_X[lineCnt][index % lineCnt]
        y = CUP_LINE_ITEM_H * int(math.floor(index * 1.0 / lineCnt))
        return (x, y)

    def getCupTargetMcHeight(self, lineCnt, targetCnt):
        return CUP_CANVAS_TOP_OFFSET + CUP_LINE_ITEM_H * int(math.ceil(targetCnt * 1.0 / lineCnt)) + CUP_CANVAS_BOTTOM_OFFSET

    def canExpandCheckBoxLine(self, achieveId):
        data = AD.data.get(achieveId, {})
        expand = data.get('expandType', EXPAND_NONE)
        isExpand = data.get('isExpand', 0)
        if isExpand and expand != EXPAND_NONE_SHOW_PROGRESS:
            return True
        return False

    def canExpandCupLine(self, achieveId):
        return AD.data.get(achieveId, {}).get('group') and achieveId in self.achieves

    def itemHeightFunction(self, *args):
        achieveId = int(args[3][0].GetNumber())
        if achieveId != self.selectAchieveId:
            return GfxValue(ITEM_MAIN_HEIGHT)
        elif self.canExpandCheckBoxLine(achieveId):
            data = AD.data.get(achieveId, {})
            lineCnt = data.get('expandCount', 2)
            targetCnt = len(data.get('achieveTargets', ()))
            itemTargetHeight = self.getCheckboxTargetMcHeight(lineCnt, targetCnt)
            return GfxValue(ITEM_MAIN_HEIGHT + itemTargetHeight)
        elif self.canExpandCupLine(achieveId):
            data = AD.data.get(achieveId, {})
            groupId, curIdx = self.getGroupInfo(data.get('group'))
            lineCnt = data.get('expandCount', 2)
            itemTargetHeight = self.getCupTargetMcHeight(lineCnt, len(self.groupAchievement[groupId]))
            return GfxValue(ITEM_MAIN_HEIGHT + itemTargetHeight)
        else:
            return GfxValue(ITEM_MAIN_HEIGHT)

    def getSubClassSelPos(self, subClassId):
        pos = 0
        for info in self.classifyData:
            pos += CLASS_ITEM_HEIGHT
            classId = info.get('label', 0)
            subClassIds = info.get('children', ())
            if subClassId not in subClassIds:
                pos += SUB_CLASS_ITEM_HEIGHT * len(subClassIds) * int(self.expandHistory.get(classId, False))
            else:
                subClassIdx = subClassIds.index(subClassId)
                pos += SUB_CLASS_ITEM_HEIGHT * subClassIdx
                break

        return pos

    def getDateText(self, achieveId):
        if achieveId in self.achieves:
            t = time.localtime(self.achieves[achieveId])
            return time.strftime('%d/%.2d/%.2d' % (t.tm_year, t.tm_mon, t.tm_mday))
        else:
            return ''

    def selectSubClass(self, item = None, subClassId = 0):
        subClassId = item.subClassId if item else subClassId
        self.refreshDetailList(self.detailData.get(subClassId, ()))
        self.widget.searchTextInput.text = ''
        classId = self.subClassInfo.get(subClassId, ('', 0))[CLASS_IDX]
        self.expandHistory[classId] = True
        if item:
            oldSelItem = self.widget.classifyTreeView.tree.getItemByData(self.selectedSubClassId)
            if oldSelItem:
                oldSelItem.selected = False
            item.selected = True
            self.selectedSubClassId = subClassId
        elif subClassId:
            self.refreshClassifyTree(self.classifyData, subClassId)

    def sendAchievement(self, achieveId):
        ret = achieveId
        if achieveId in self.achieves:
            localTime = time.localtime(self.achieves[achieveId])
            ret = '%d:time%d/%d/%d:%s' % (achieveId,
             localTime[0],
             localTime[1],
             localTime[2],
             BigWorld.player().realRoleName)
        elif self.canExpandCheckBoxLine(achieveId):
            ret = str(achieveId)
            for targetId in AD.data.get(achieveId, {}).get('achieveTargets', ()):
                if targetId in self.achieveTargets and self.achieveTargets[targetId]['done']:
                    ret += ':%d' % targetId

        color = FCD.data['achieve', 0]['color']
        msg = "<font color=\'%s\'>[<a href = \'event:achvid %s\'><u>%s</u></a>]</font>" % (color, ret, AD.data.get(achieveId, {}).get('name'))
        gameglobal.rds.ui.sendLink(msg)

    def onItemClick(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        achieveId = item.achieveId
        if e.shiftKey:
            self.sendAchievement(item.achieveId)
        if self.selectAchieveId == achieveId:
            self.selectAchieveId = 0
        else:
            self.selectAchieveId = achieveId
        old = self.widget.detailListView.dataArray
        self.widget.detailListView.dataArray = []
        self.widget.detailListView.dataArray = old
        self.widget.detailListView.validateNow()

    def onItemTargetClick(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        achieveId = item.achieveId
        subClassId = AD.data.get(achieveId, {}).get('class', 0)
        if not subClassId:
            return
        self.selectAchieveId = achieveId
        self.selectSubClass(subClassId=subClassId)
        e.stopImmediatePropagation()

    def onSearchChange(self, *args):
        e = ASObject(args[3][0])
        if e.target != self.widget.searchTextInput:
            return
        text = e.currentTarget.text
        if text:
            self.refreshSearchResult(text)
        else:
            if self.selectedSubClassId == -1:
                self.selectedSubClassId = RECENT_SUB_CLASS_ID
            self.refreshClassifyTree(self.classifyData, self.selectedSubClassId)
            self.refreshDetailList(self.detailData.get(self.selectedSubClassId, ()))

    def onExpandChange(self, *args):
        e = ASObject(args[3][0])
        groupLabel = e.data.data.label
        expand = e.data.expand
        self.expandHistory[groupLabel] = expand

    def onSubClassItemClick(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        self.selectSubClass(item=item)

    def onQueryFirstKill(self, fbNo, data, version):
        self.rankData[fbNo] = {'data': data,
         'version': version}
        if not self.widget:
            return
        fbNoSel = AD.data.get(self.selectAchieveId, {}).get('fbNo', 0)
        if fbNoSel != fbNo:
            return
        self.refreshTopRankTree(data)

    def refreshTopRankPanel(self, achieveId):
        fbNo = AD.data.get(achieveId, {}).get('fbNo', 0)
        if not fbNo:
            self.widget.topRankPanel.visible = False
            return
        version = self.rankData.get(fbNo, {}).get('version', 0)
        BigWorld.player().cell.queryFirstKill(fbNo, version, achieveId)
        if fbNo in self.rankData:
            data = self.rankData.get(fbNo, {}).get('data')
            self.refreshTopRankTree(data)

    def refreshTopRankTree(self, data):
        self.widget.topRankPanel.visible = bool(data)
        if not data:
            BigWorld.player().showGameMsg(GMDD.data.NO_FIVE_RANK, ())
            return
        treeData = []
        for idx, team in enumerate(data):
            treeData.append({'label': team[MEMBERS_IDX][0],
             'rank': idx + 1,
             'children': team[MEMBERS_IDX]})

        tree = self.widget.topRankPanel.rankTree.tree
        tree.itemHeights = [RANK_TEAM_HEIGHT, RANK_PLAYER_HEIGHT]
        tree.itemRenderers = ['AchvmentDetailPanel_TeamItem', 'AchvmentDetailPanel_PlayerItem']
        tree.labelFunction = self.topRankLabelFunc
        self.widget.topRankPanel.rankTree.tree.dataArray = treeData
        self.widget.topRankPanel.rankTree.tree.validateNow()

    def topRankLabelFunc(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        if isFirst:
            rank = ASObject(args[3][1]).rank
            itemMc.rankTf.text = rank
            leaderData = ASObject(args[3][1]).label
            leaderName = leaderData[MEMBER_NAME_IDX]
            itemMc.teamNameTf.text = gameStrings.ACHIEVEMENT_TOP_TEAMNAME % leaderName
        else:
            itemData = ASObject(args[3][1])
            gbId = itemData[MEMBER_GBID_IDX]
            name = itemData[MEMBER_NAME_IDX]
            invalid = itemData[MEMBER_INVALID_IDX]
            school = itemData[MEMBER_SCHOOL_IDX]
            itemMc.jobIcon.visible = school and not invalid
            itemMc.jobIcon.visible and itemMc.jobIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[school])
            itemMc.nameTf.text = gameStrings.ACHIEVEMENT_TOP_INVALID_PLAYERNAME % name if invalid else name
            menuParam = {'roleName': name,
             'gbId': long(gbId)}
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_ACHIEVEMENT_TOPRANK, menuParam)

    def onCloseRankBtnClick(self, *args):
        self.widget.topRankPanel.visible = False
