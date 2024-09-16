#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentDiffDetailProxy.o
from gamestrings import gameStrings
import time
import BigWorld
import gameglobal
import tipUtils
from guis import events
from guis import uiUtils
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import achievement_data as AD
from data import achievement_class_data as ACD
CLASS_ITEM_HEIGHT = 72
SUB_CLASS_ITEM_HEIGHT = 32
SUB_CLASS_NAME_IDX = 0
CLASS_ID_IDX = 1
ACHIEVED_CNT_IDX = 0
TOTAL_CNT_IDX = 1
COLOR_UNACHIEVE = '#969696'
COLOR_ACHIEVED = '#ffc961'
COLOR_OTHER_ACHIEVED = '#85c521'
EXPAND_NONE = 0
EXPAND_NONE_SHOW_PROGRESS = 1
AWARD_ICON_X_OFFSET = 10
CLASS_BG_PATH = 'achieve/%d.dds'

class AchvmentDiffDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentDiffDetailProxy, self).__init__(uiAdapter)
        self.selectedSubClassId = -1
        self.oldSelSubClassItem = None
        self.reset()

    def reset(self):
        self.widget = None
        self.otherName = ''
        self.myAchievePoint = 0
        self.otherAchievePoint = 0
        self.maxPoint = 0
        self.myAchieves = {}
        self.otherAchieves = {}
        self.myAchieveTargets = {}
        self.otherAchieveTargets = {}
        self.achieveFilterData = {}
        self.detailData = {}
        self.searchInfo = {}
        self.classifyData = {}
        self.subClassInfo = {}

    def clearAll(self):
        pass

    def initPanel(self, widget):
        self.widget = widget.mainMc
        self.initData()
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.selectedSubClassId = -1
        self.oldSelSubClassItem = None

    def initData(self):
        self.otherName = gameglobal.rds.ui.achvmentDiff.otherName
        self.myAchievePoint = gameglobal.rds.ui.achvmentDiff.myAchievePoint
        self.otherAchievePoint = gameglobal.rds.ui.achvmentDiff.otherAchievePoint
        self.maxPoint = gameglobal.rds.ui.achvmentDiff.maxPoint
        self.achieveFilterData = gameglobal.rds.ui.achvmentDiff.achieveFilterData
        self.myAchieves = gameglobal.rds.ui.achvmentDiff.myAchieves
        self.otherAchieves = gameglobal.rds.ui.achvmentDiff.otherAchieves
        self.classProgress = gameglobal.rds.ui.achvmentDiff.classProgress
        self.subClassInfo = gameglobal.rds.ui.achvmentDiff.subClassInfo
        self.initClassifyData()
        self.initDetailInfo()
        self.initSelect()

    def initUI(self):
        maxAchieves = len(self.achieveFilterData)
        otherAchieveCnt = len(self.otherAchieves)
        self.widget.otherProgressTf.text = gameStrings.TEXT_ACHVMENTDIFFDETAILPROXY_93 % (otherAchieveCnt, 100.0 * otherAchieveCnt / maxAchieves)
        self.initTreeProp()
        self.initListProp()
        self.refreshClassTree()
        self.refreshDetailList(self.detailData.get(self.selectedSubClassId))

    def initDetailInfo(self):
        if self.detailData and self.searchInfo:
            return
        for achieveId, info in self.achieveFilterData.iteritems():
            subClassId = info.get('class')
            if subClassId not in self.detailData:
                self.detailData[subClassId] = []
            self.detailData[subClassId].append(achieveId)
            self.searchInfo[info.get('name')] = achieveId

        for achieveIds in self.detailData.itervalues():
            achieveIds.sort(self.compare)

    def compare(self, id1, id2):
        if id1 in self.otherAchieves and id2 not in self.otherAchieves:
            return -1
        if id1 not in self.otherAchieves and id2 in self.otherAchieves:
            return 1
        return cmp(id1, id2)

    def initClassifyData(self):
        if not self.classifyData:
            classSortData = sorted(ACD.data.items())
            self.classifyData = [ self.genClassifyData(classId, info) for classId, info in classSortData ]
            self.classifyData.sort()

    def genClassifyData(self, classId, info):
        childrenIds = sorted(info.get('newvalue', {}).keys())
        return {'label': classId,
         'children': childrenIds}

    def initSelect(self):
        if self.selectedSubClassId == -1:
            self.selectedSubClassId = self.classifyData[0].get('children', (101,))[0]
        self.setTreeExpand(self.selectedSubClassId, True)

    def resetTreeExpand(self):
        for data in self.classifyData:
            data['expand'] = False

    def setTreeExpand(self, subClassId, expand):
        for data in self.classifyData:
            if subClassId in data.get('children', ()):
                data['expand'] = expand

    def selSubClassItem(self, item):
        if not item:
            return
        if item.subClassId == self.selectedSubClassId:
            return
        item.selected = True
        if self.oldSelSubClassItem:
            self.oldSelSubClassItem.selected = False
        self.oldSelSubClassItem = item
        self.selectedSubClassId = item.subClassId
        self.refreshDetailList(self.detailData.get(self.selectedSubClassId, ()))

    def initTreeProp(self):
        tree = self.widget.classTree.tree
        tree.itemHeights = [CLASS_ITEM_HEIGHT, SUB_CLASS_ITEM_HEIGHT]
        tree.itemRenderers = ['AchvmentDiffDetailPanel_ClassItem', 'AchvmentDiffDetailPanel_SubClassItem']
        tree.labelFunction = self.classifyGroupLabelFunc

    def initListProp(self):
        self.widget.detailList.itemRenderer = 'AchvmentDiffDetailPanel_DetailItem'
        self.widget.detailList.labelFunction = self.detailItemLabelFunc

    def classifyGroupLabelFunc(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        if isFirst:
            rootClassData = ASObject(args[3][1])
            classId = rootClassData.label
            itemMc.classId = classId
            itemMc.nameTf.text = ACD.data.get(classId, {}).get('name')
            achieveCnt = self.classProgress[classId][ACHIEVED_CNT_IDX]
            totalCnt = self.classProgress[classId][TOTAL_CNT_IDX]
            itemMc.cntTf.text = '%d/%d' % (achieveCnt, totalCnt)
            itemMc.progressbar.currentValue = achieveCnt
            itemMc.progressbar.maxValue = totalCnt
            itemMc.bg.bg.fitSize = True
            itemMc.bg.bg.loadImage(CLASS_BG_PATH % ACD.data.get(classId, {}).get('newIcon', 1))
        else:
            subClassId = int(args[3][1].GetNumber())
            isSelected = bool(self.selectedSubClassId == subClassId)
            itemMc.selected = isSelected
            if isSelected:
                self.oldSelSubClassItem = itemMc
            itemMc.subClassId = subClassId
            itemMc.textField.text = self.subClassInfo.get(subClassId, ('', 0))[SUB_CLASS_NAME_IDX]
            itemMc.addEventListener(events.MOUSE_CLICK, self.onSubClassItemClick, False, 0, True)

    def refreshClassTree(self):
        self.widget.classTree.tree.dataArray = self.classifyData
        self.widget.classTree.validateNow()
        self.widget.classTree.scrollToHead()

    def refreshDetailList(self, listData):
        self.widget.detailList.dataArray = listData
        self.widget.detailList.validateNow()
        self.widget.detailList.scrollToHead()

    def detailItemLabelFunc(self, *args):
        achieveId = int(args[3][0].GetNumber())
        item = ASObject(args[3][1])
        item.achieveId = achieveId
        data = AD.data.get(achieveId, {})
        rewardTitle = data.get('rewardTitle')
        bonusId = data.get('bonusId')
        item.nameTf.text = data.get('name')
        item.descTf.text = '???' if data.get('hideDesc') else data.get('desc')
        item.dateTf.text = self.getDateText(achieveId)
        item.icon.gotoAndStop(str(bool(achieveId in self.otherAchieves)))
        item.awardMc.visible = bool(rewardTitle or bonusId)
        if rewardTitle or bonusId:
            item.awardMc.x = item.nameTf.x + item.nameTf.textWidth + AWARD_ICON_X_OFFSET
            awardText = gameglobal.rds.ui.achvment.getAwardString(rewardTitle, bonusId)
            TipManager.addTip(item.awardMc, awardText, tipUtils.TYPE_DEFAULT_BLACK)
        isMyAchieved = achieveId in self.myAchieves
        isOtherAchieved = achieveId in self.otherAchieves
        myColor = COLOR_ACHIEVED if isMyAchieved else COLOR_UNACHIEVE
        otherColor = COLOR_OTHER_ACHIEVED if isOtherAchieved else COLOR_UNACHIEVE
        item.myAchievePointTf.htmlText = uiUtils.toHtml(data.get('rewardPoint', 0), myColor)
        item.otherAchievePointTf.htmlText = uiUtils.toHtml(data.get('rewardPoint', 0), otherColor)
        item.myAchievedTf.visible = isMyAchieved
        item.otherAchievedTf.visible = isOtherAchieved
        self.setHitTestDisable(item)
        item.addEventListener(events.MOUSE_CLICK, self.onDetailItemClick, False, 0, True)

    def getDateText(self, achieveId):
        if achieveId in self.otherAchieves:
            t = time.localtime(self.otherAchieves[achieveId])
            return time.strftime('%d/%.2d/%.2d' % (t.tm_year, t.tm_mon, t.tm_mday))
        else:
            return ''

    def setHitTestDisable(self, item):
        ASUtils.setHitTestDisable(item.nameTf, True)
        ASUtils.setHitTestDisable(item.dateTf, True)
        ASUtils.setHitTestDisable(item.icon, True)
        ASUtils.setHitTestDisable(item.descTf, True)
        ASUtils.setHitTestDisable(item.myProgress, True)
        ASUtils.setHitTestDisable(item.otherProgress, True)

    def getLinkAchieveId(self, achieveId):
        gameglobal.rds.ui.achvmentDetail.initGroupAchieve()
        isAchieveGroupHideItem = gameglobal.rds.ui.achvmentDetail.isAchieveGroupHideItem(achieveId)
        if not isAchieveGroupHideItem:
            return achieveId
        else:
            return gameglobal.rds.ui.achvmentDetail.getCurrentGroupAchieveId(achieveId)

    def onSubClassItemClick(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        self.selSubClassItem(item)

    def onSearchChange(self, *args):
        e = ASObject(args[3][0])
        text = e.currentTarget.text
        if text:
            retIds = [ self.searchInfo[name] for name in self.searchInfo if uiUtils.isContainString(name, text) ]
            self.selectedSubClassId = -1
            self.resetTreeExpand()
            self.refreshClassTree()
            self.refreshDetailList(retIds)
        else:
            self.selectedSubClassId = self.classifyData[0].get('children', (101,))[0]
            self.setTreeExpand(self.selectedSubClassId, True)
            self.refreshClassTree()
            self.refreshDetailList(self.detailData.get(self.selectedSubClassId, ()))

    def onDetailItemClick(self, *args):
        e = ASObject(args[3][0])
        achieveId = e.currentTarget.achieveId
        linkAchieveId = self.getLinkAchieveId(achieveId)
        if not gameglobal.rds.ui.achvment.widget:
            gameglobal.rds.ui.achvment.linkAchieveId = achieveId
            gameglobal.rds.ui.achvment.getAchieveData()
        else:
            gameglobal.rds.ui.achvment.link2AchvmentDetailView(achieveId=linkAchieveId)
