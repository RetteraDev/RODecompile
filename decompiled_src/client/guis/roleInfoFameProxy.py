#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInfoFameProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import const
import uiUtils
import utils
from item import Item
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import fame_data as FD
from data import quest_data as QD
from data import sys_config_data as SCD
FAME_BG_PATH_SMALL = 'fame/fame156/%s.dds'
FAME_BG_PATH_BIG = 'fame/fame516/%s.dds'
TAB_IDX_OVERVIEW = 0
TAB_IDX_FAMESHOP = 1
TAB_IDX_SCHOOLFAME = 2
FAME_QUEST_KIND_NUM = 3
SCHOOL_FAME_CARD_NUM = 5

class RoleInfoFameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoleInfoFameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.tabIdx = TAB_IDX_OVERVIEW
        self.daibiToFameMap = {}
        self.questIdToFameMap = {}
        self.fameDict = {}
        self.fameList = []
        self.selectedFameId = 0
        self.fameQuestList = []

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        detail = self.widget.detail
        detail.shopBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShopBtn, False, 0, True)
        TipManager.addTip(detail.shopBtn, SCD.data.get('SHENGWANG_SHOP_TIPS', ''))
        detail.lifeSkillBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLifeSkillBtn, False, 0, True)
        TipManager.addTip(detail.lifeSkillBtn, SCD.data.get('YINSHI_ZHENCHUAN_TIPS', ''))
        detail.fameQuestBtn.addEventListener(events.BUTTON_CLICK, self.handleClickFameQuestBtn, False, 0, True)
        detail.overviewBtn.groupName = 'detail'
        detail.fameShopBtn.groupName = 'detail'
        detail.schoolFameBtn.groupName = 'detail'
        detail.overviewBtn.addEventListener(events.BUTTON_CLICK, self.handleClickOverviewBtn, False, 0, True)
        detail.fameShopBtn.addEventListener(events.BUTTON_CLICK, self.handleClickFameShopBtn, False, 0, True)
        detail.schoolFameBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSchoolFameBtn, False, 0, True)
        overviewPanel = detail.overviewPanel
        for i in xrange(2, 8):
            itemMc = getattr(overviewPanel, 'item%d' % i, None)
            if not itemMc:
                continue
            itemMc.gongping.icon.fitSize = True
            itemMc.gongzi.icon.fitSize = True
            itemMc.zhuanshu.icon.fitSize = True
            ASUtils.setHitTestDisable(itemMc.gpTxt, True)
            itemMc.zhuanshu.itemId = 0
            itemMc.zhuanshu.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)

        fameQuestPanel = self.widget.fameQuestPanel
        for i in xrange(FAME_QUEST_KIND_NUM):
            detailMc = getattr(fameQuestPanel, 'detail%d' % i, None)
            if not detailMc:
                continue
            detailMc.idx = i
            detailMc.lvCheckBox.addEventListener(events.EVENT_SELECT, self.handleSelectLvCheckBox, False, 0, True)
            detailMc.wndList.itemHeight = 26
            detailMc.wndList.itemRenderer = 'RoleInformationFameV2_QuestList_Item'
            detailMc.wndList.lableFunction = self.detailItemFunc

        fameQuestPanel.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseFameQuestPanel, False, 0, True)
        fameQuestPanel.visible = False
        self.initTree()

    def getFameLv(self, fameId, totalFame = None, ignoreQuest = False):
        fdData = FD.data.get(fameId, {})
        if not fdData:
            return (0, 0, 0, 0, 0)
        else:
            extra = 0
            p = BigWorld.player()
            if totalFame == None:
                totalFame = p.getFame(fameId)
            schoolFame = fdData.get('schoolFame', 0)
            if schoolFame and schoolFame == p.school:
                schoolLvUpNeed = fdData.get('schoolLvUpNeed', {})
                if not schoolLvUpNeed:
                    return (0, 0, 0, 0, 0)
                fameLv = 1
                maxLv = len(schoolLvUpNeed)
                for i in range(1, maxLv + 1):
                    v = schoolLvUpNeed.get(i, (0, 0))
                    if totalFame >= v[0] and (ignoreQuest or p.isQuestCompleted(v[1])):
                        fameLv = i + 1
                        extra = totalFame - v[0]
                    else:
                        self.questIdToFameMap[v[1]] = fameId
                        break

                fameLv = min(fameLv, maxLv)
                if fameLv == maxLv and totalFame >= schoolLvUpNeed.get(maxLv, (0, 0))[0]:
                    maxFame = schoolLvUpNeed.get(maxLv, (0, 0))[0] - schoolLvUpNeed.get(maxLv - 1, (0, 0))[0]
                    curFame = maxFame
                else:
                    minFame = schoolLvUpNeed.get(fameLv - 1, (0, 0))[0]
                    maxFame = schoolLvUpNeed.get(fameLv, (0, 0))[0] - minFame
                    curFame = totalFame - minFame
            else:
                lvUpNeed = fdData.get('lvUpNeed', {})
                if not lvUpNeed:
                    return (0, 0, 0, 0, 0)
                fameLv = 1
                maxLv = len(lvUpNeed)
                for i in xrange(1, maxLv + 1):
                    if totalFame >= lvUpNeed.get(i, 0):
                        fameLv = i + 1
                        extra = totalFame - lvUpNeed.get(i, 0)
                    else:
                        break

                fameLv = min(fameLv, maxLv)
                if fameLv == maxLv and totalFame >= lvUpNeed.get(maxLv, 0):
                    maxFame = lvUpNeed.get(maxLv, 0) - lvUpNeed.get(maxLv - 1, 0)
                    curFame = maxFame
                else:
                    minFame = lvUpNeed.get(fameLv - 1, 0)
                    maxFame = lvUpNeed.get(fameLv, 0) - minFame
                    curFame = totalFame - minFame
            return (fameLv,
             maxLv,
             curFame,
             maxFame,
             extra)

    def getFameInfo(self, fameId):
        p = BigWorld.player()
        fdData = FD.data.get(fameId, {})
        schoolFame = fdData.get('schoolFame', 0)
        daibiId = fdData.get('transferToFameOnMaxVal', 0)
        showDaibiIcon = daibiId > 0 and gameglobal.rds.configData.get('enableFameTransfer', False)
        if showDaibiIcon:
            daibiIconType = fdData.get('transferToFameOnMaxValIcon', 'fame')
            daibiValue = p.getFame(daibiId)
            self.daibiToFameMap[daibiId] = fameId
        else:
            daibiIconType = ''
            daibiValue = 0
        fameLv, maxLv, curFame, maxFame, _ = self.getFameLv(fameId)
        if schoolFame:
            if schoolFame == p.school:
                fameLvType = 'selfSchoolType%d' % fameLv
                fameLvName = SCD.data.get('selfSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
                canLvUp = fameLv < maxLv and curFame >= maxFame
            else:
                fameLvType = 'otherSchoolType%d' % fameLv
                fameLvName = SCD.data.get('otherSchoolFameLvName', {}).get(fameLv, '')
                canLvUp = False
        else:
            fameLvType = 'type%d' % fameLv
            fameLvName = ''
            canLvUp = False
        fameInfo = {'fameId': fameId,
         'fameName': fdData.get('fameName', ''),
         'fameLvType': fameLvType,
         'fameLvName': fameLvName,
         'canLvUp': canLvUp,
         'curFame': curFame,
         'maxFame': maxFame,
         'fameTips': '%d/%d' % (curFame, maxFame),
         'showDaibiIcon': showDaibiIcon,
         'daibiIconType': daibiIconType,
         'daibiValue': daibiValue,
         'fameBg': FAME_BG_PATH_SMALL % fdData.get('icon', '')}
        return fameInfo

    def initFameList(self):
        p = BigWorld.player()
        self.fameDict = {}
        self.fameList = []
        tmpDict = {}
        for fameId, value in FD.data.iteritems():
            if value.get('display', 0) != gametypes.FAME_SHOW_IN_FAMEPANEL:
                continue
            if value.get('schoolFame', 0) and not gameglobal.rds.configData.get('enableSchoolFame', False):
                continue
            fameInfo = self.getFameInfo(fameId)
            self.fameDict[fameId] = fameInfo
            tmpDict.setdefault((value.get('treeName', ''), value.get('tree', 0)), []).append(fameId)

        keys = tmpDict.keys()
        keys.sort(key=lambda x: x[1])
        for key in keys:
            value = tmpDict.get(key)
            value.sort(key=lambda x: (0 if p.school == FD.data.get(x, {}).get('schoolFame', 0) else FD.data.get(x, {}).get('schoolFame', 0)))
            self.fameList.append({'label': key[0],
             'children': value})

    def initTree(self):
        self.initFameList()
        self.widget.tree.lvItemGap = 0
        self.widget.tree.itemHeights = [28, 68]
        self.widget.tree.itemRenderers = ('RoleInformationFameV2_TreeItem_Lv1', 'RoleInformationFameV2_TreeItem_Lv2')
        self.widget.tree.labelFunction = self.treeLabelFun
        self.widget.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleTreeItemChange, False, 0, True)
        self.widget.tree.addEventListener(events.EVENT_SELECTED_DATA_CHANGED, self.handleSelectedChange, False, 0, True)
        self.widget.tree.dataArray = self.fameList
        if self.fameList[0] and len(self.fameList[0].get('children')) > 0:
            fameId = self.fameList[0].get('children')[0]
            self.widget.tree.selectData = fameId
        else:
            fameId = 0
        self.widget.fameScrollWnd.canvas.addChild(self.widget.tree)
        self.widget.fameScrollWnd.refreshHeight()
        if FD.data.get(fameId, {}).get('schoolFame', 0):
            self.selectTab(TAB_IDX_SCHOOLFAME)
        else:
            self.selectTab(TAB_IDX_OVERVIEW)

    def treeLabelFun(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        if isFirst:
            itemData = ASObject(args[3][1])
            itemMc.textField.htmlText = itemData.label
        else:
            fameId = int(args[3][1].GetNumber())
            self.updateTreeItem(itemMc, fameId)

    def updateTreeItem(self, itemMc, fameId):
        fameInfo = self.fameDict.get(fameId, {})
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.textField.htmlText = fameInfo.get('fameName', '')
        itemMc.relationIcon.x = itemMc.textField.x + itemMc.textField.textWidth + 8
        itemMc.relationIcon.gotoAndStop(fameInfo.get('fameLvType', ''))
        itemMc.relationIcon.fameLvName.htmlText = fameInfo.get('fameLvName', '')
        itemMc.fameBar.bar.gotoAndStop(fameInfo.get('fameLvType', ''))
        itemMc.fameBar.maxValue = fameInfo.get('maxFame', 0)
        itemMc.fameBar.currentValue = fameInfo.get('curFame', 0)
        TipManager.addTip(itemMc.fameBar, fameInfo.get('fameTips', ''))
        if fameInfo.get('showDaibiIcon', False):
            itemMc.daibiIcon.visible = True
            itemMc.daibiValue.visible = True
            itemMc.daibiIcon.bonusType = fameInfo.get('daibiIconType', '')
            itemMc.daibiValue.htmlText = fameInfo.get('daibiValue', 0)
        else:
            itemMc.daibiIcon.visible = False
            itemMc.daibiValue.visible = False
        itemMc.canLvUp.visible = fameInfo.get('canLvUp', False)
        itemMc.fameBg.fitSize = True
        itemMc.fameBg.loadImage(fameInfo.get('fameBg', ''))

    def handleTreeItemChange(self, *args):
        self.widget.fameScrollWnd.refreshHeight(self.widget.tree.height)

    def handleSelectedChange(self, *args):
        e = ASObject(args[3][0])
        if not e.data or not e.data.selectData:
            return
        fameId = int(e.data.selectData)
        if self.selectedFameId == fameId:
            return
        self.selectedFameId = fameId
        self.refreshDetailInfo(fameId)

    def refreshDetailInfo(self, fameId):
        if not self.widget:
            return
        if self.selectedFameId != fameId:
            return
        p = BigWorld.player()
        detail = self.widget.detail
        fdData = FD.data.get(self.selectedFameId, {})
        schoolFame = fdData.get('schoolFame', 0)
        selfSchool = schoolFame == p.school if schoolFame else True
        daibiId = fdData.get('transferToFameOnMaxVal', 0)
        showDaibiIcon = daibiId > 0 and gameglobal.rds.configData.get('enableFameTransfer', False)
        if showDaibiIcon:
            detail.daibiIcon.visible = True
            detail.daibiValue.visible = True
            detail.daibiIcon.bonusType = fdData.get('transferToFameOnMaxValIcon', 'fame')
            detail.daibiValue.htmlText = p.getFame(daibiId)
        else:
            detail.daibiIcon.visible = False
            detail.daibiValue.visible = False
        detail.fameBg.fitSize = True
        detail.fameBg.loadImage(FAME_BG_PATH_BIG % fdData.get('icon', ''))
        shopSeekId = fdData.get('shopSeekId', (0,))[0]
        detail.shopBtn.visible = shopSeekId > 0
        lifeskillSeekId = fdData.get('lifeskillSeekId', (0,))[0]
        detail.lifeSkillBtn.visible = lifeskillSeekId > 0
        hasFameQuest = False
        for fameSrc in const.ALL_FAME_BONUS_SRC:
            if fdData.get('des%s' % fameSrc, ()):
                hasFameQuest = True
                break

        if hasFameQuest and selfSchool:
            detail.fameQuestBtn.visible = True
            self.refreshFameQuestPanel()
        else:
            detail.fameQuestBtn.visible = False
            self.widget.fameQuestPanel.visible = False
        if schoolFame:
            detail.overviewBtn.visible = False
            detail.schoolFameBtn.visible = True
            self.refreshSchoolFamePanel()
        else:
            detail.overviewBtn.visible = True
            detail.schoolFameBtn.visible = False
            self.refreshOverviewPanel()
        fameShopBtnVisible = (fdData.get('shop1') or fdData.get('shop2')) and selfSchool
        detail.fameShopBtn.visible = fameShopBtnVisible
        if fameShopBtnVisible:
            self.refreshFameShopPanel()
        if self.tabIdx == TAB_IDX_OVERVIEW and schoolFame:
            self.selectTab(TAB_IDX_SCHOOLFAME)
        elif self.tabIdx == TAB_IDX_SCHOOLFAME and not schoolFame:
            self.selectTab(TAB_IDX_OVERVIEW)
        elif self.tabIdx == TAB_IDX_FAMESHOP and not fameShopBtnVisible:
            if schoolFame:
                self.selectTab(TAB_IDX_SCHOOLFAME)
            else:
                self.selectTab(TAB_IDX_OVERVIEW)

    def refreshOverviewPanel(self):
        overviewPanel = self.widget.detail.overviewPanel
        fdData = FD.data.get(self.selectedFameId, {})
        passportDict = fdData.get('passport', {})
        tradeItemDict = fdData.get('tradeItem', {})
        payDict = fdData.get('pay', {})
        rewardDict = fdData.get('reward', {})
        workDict = fdData.get('work', {})
        masterTeachDict = fdData.get('masterTeach', {})
        fameLv, maxLv, _, _, _ = self.getFameLv(self.selectedFameId)
        for i in xrange(2, 8):
            itemMc = getattr(overviewPanel, 'item%d' % i, None)
            if not itemMc:
                continue
            if i > maxLv:
                itemMc.visible = False
                continue
            itemMc.visible = True
            itemMc.dangqiang.visible = i == fameLv
            passport = passportDict.get(i)
            if passport:
                itemMc.huiyuan.visible = True
                itemMc.huiyuan.gotoAndStop('type%d' % passport[0])
                TipManager.addTip(itemMc.huiyuan, passport[1])
            else:
                itemMc.huiyuan.visible = False
            tradeItem = tradeItemDict.get(i)
            if tradeItem:
                itemMc.gongping.visible = True
                itemMc.gongping.icon.loadImage(uiUtils.getItemIconFile40(tradeItem[0]))
                itemMc.gpTxt.text = '%d%%' % int(tradeItem[1] * 100)
                TipManager.addItemTipById(itemMc.gongping, tradeItem[0])
            else:
                itemMc.gongping.visible = False
                itemMc.gpTxt.text = ''
            payItemId = payDict.get(i)
            if payItemId:
                itemMc.gongzi.visible = True
                itemMc.gongzi.icon.loadImage(uiUtils.getItemIconFile40(payItemId))
                TipManager.addItemTipById(itemMc.gongzi, payItemId)
            else:
                itemMc.gongzi.visible = False
            rewardItemId = rewardDict.get(i)
            if rewardItemId:
                itemMc.zhuanshu.visible = True
                itemMc.zhuanshu.icon.loadImage(uiUtils.getItemIconFile40(rewardItemId))
                itemMc.zhuanshu.itemId = rewardItemId
                TipManager.addItemTipById(itemMc.zhuanshu, rewardItemId, True, 'upLeft', 'over', 'fameShop')
            else:
                itemMc.zhuanshu.visible = False
            work = workDict.get(i)
            if work:
                itemMc.jianzhi.visible = True
                itemMc.jianzhi.gotoAndStop('type%d' % work[0])
                TipManager.addTip(itemMc.jianzhi, work[1])
            else:
                itemMc.jianzhi.visible = False
            masterTeach = masterTeachDict.get(i)
            if masterTeach:
                itemMc.dashi.visible = True
                itemMc.dashi.gotoAndStop('type%d' % masterTeach[0])
                TipManager.addTip(itemMc.dashi, masterTeach[1])
            else:
                itemMc.dashi.visible = False

    def refreshFameShopPanel(self):
        fameShopPanel = self.widget.detail.fameShopPanel
        fameLvName = SCD.data.get('fameLvName', {})
        fdData = FD.data.get(self.selectedFameId, {})
        passportDict = fdData.get('passport', {})
        desc = fdData.get('desc', '')
        shop1List = []
        shop1 = fdData.get('shop1', ())
        for i, shop1Item in enumerate(shop1):
            itemId = shop1Item[0]
            fameLv = shop1Item[1]
            passport = passportDict.get(fameLv)
            if passport:
                huiyuanType = 'type%d' % passport[0]
                huiyuanTips = gameStrings.ROLE_INFO_FAME_SHOP_HUIYUAN_TIPS % (desc, fameLvName.get(fameLv, ''))
            else:
                huiyuanType = ''
                huiyuanTips = ''
            shop1List.append({'itemName': uiUtils.getItemColorName(itemId),
             'itemInfo': uiUtils.getGfxItemById(itemId, '', picSize=uiConst.ICON_SIZE110, overPicSize=uiConst.ICON_SIZE110, srcType='fameShop'),
             'huiyuanType': huiyuanType,
             'huiyuanTips': huiyuanTips})

        fameShopPanel.pageList.childItem = 'RoleInformationFameV2_PageList_Item'
        fameShopPanel.pageList.childWidth = 140
        fameShopPanel.pageList.pageItemFunc = self.shopPageListItemFunc
        fameShopPanel.pageList.data = shop1List
        shop2List = []
        shop2 = fdData.get('shop2', ())
        for i, shop2Item in enumerate(shop2):
            itemId = shop2Item[0]
            fameLv = shop2Item[1]
            passport = passportDict.get(fameLv)
            if passport:
                huiyuanType = 'type%d' % passport[0]
                huiyuanTips = gameStrings.ROLE_INFO_FAME_SHOP_HUIYUAN_TIPS % (desc, fameLvName.get(fameLv, ''))
            else:
                huiyuanType = ''
                huiyuanTips = ''
            shop2List.append({'itemName': uiUtils.getItemColorName(itemId),
             'itemInfo': uiUtils.getGfxItemById(itemId, srcType='fameShop'),
             'huiyuanType': huiyuanType,
             'huiyuanTips': huiyuanTips})

        fameShopPanel.scrollWndList.itemWidth = 181
        fameShopPanel.scrollWndList.itemHeight = 63
        fameShopPanel.scrollWndList.column = 3
        fameShopPanel.scrollWndList.itemRenderer = 'RoleInformationFameV2_ScrollWndList_Item'
        fameShopPanel.scrollWndList.lableFunction = self.shopWndListItemFunc
        fameShopPanel.scrollWndList.dataArray = shop2List

    def shopPageListItemFunc(self, *args):
        itemMc = ASObject(args[3][0])
        itemData = ASObject(args[3][1])
        itemMc.itemName.htmlText = itemData.itemName
        itemMc.itemSlot.setItemSlotData(itemData.itemInfo)
        itemMc.itemSlot.dragable = False
        if itemData.huiyuanType != '':
            itemMc.huiyuan.visible = True
            itemMc.huiyuan.gotoAndStop(itemData.huiyuanType)
            TipManager.addTip(itemMc.huiyuan, itemData.huiyuanTips)
        else:
            itemMc.huiyuan.visible = False
        itemMc.itemSlot.itemId = itemData.itemInfo.itemId
        itemMc.itemSlot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)

    def shopWndListItemFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.itemName.htmlText = itemData.itemName
        itemMc.itemSlot.setItemSlotData(itemData.itemInfo)
        itemMc.itemSlot.dragable = False
        if itemData.huiyuanType != '':
            itemMc.huiyuan.visible = True
            itemMc.huiyuan.gotoAndStop(itemData.huiyuanType)
            TipManager.addTip(itemMc.huiyuan, itemData.huiyuanTips)
        else:
            itemMc.huiyuan.visible = False

    def refreshSchoolFamePanel(self):
        schoolFamePanel = self.widget.detail.schoolFamePanel
        p = BigWorld.player()
        fdData = FD.data.get(self.selectedFameId, {})
        schoolFame = fdData.get('schoolFame', 0)
        fameLv, maxLv, curFame, maxFame, _ = self.getFameLv(self.selectedFameId)
        if schoolFame == p.school:
            schoolFamePanel.gotoAndStop('selfSchool')
            schoolFamePanel.fameLvName.text = SCD.data.get('selfSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
            useExtra = False
            schoolLvUpExtra = fdData.get('schoolLvUpExtra')
            if schoolLvUpExtra:
                extraQuestId, extraFameLv = schoolLvUpExtra
                extraQuestStr = gameStrings.ROLE_INFO_FAME_LVUP_BTN_EXTRA_QUEST % QD.data.get(extraQuestId, {}).get('name', '')
                if not p.isQuestCompleted(extraQuestId):
                    extraQuestStr = uiUtils.toHtml(extraQuestStr, color='#BF1000')
                    useExtra = True
                extraNeed = fdData.get('schoolLvUpNeed', {}).get(extraFameLv, (0, 0))[0]
                extraFameStr = gameStrings.ROLE_INFO_FAME_LVUP_BTN_EXTRA_FAME % (fdData.get('name', ''), extraNeed)
                if p.getFame(self.selectedFameId) < extraNeed:
                    extraFameStr = uiUtils.toHtml(extraFameStr, color='#BF1000')
                    useExtra = True
                extraTips = gameStrings.ROLE_INFO_FAME_LVUP_BTN_EXTRA_TIPS % (extraQuestStr, extraFameStr)
            else:
                extraTips = ''
            if useExtra:
                schoolFamePanel.lvUpBtn.enabled = False
                schoolFamePanel.lvUpBtn.mouseEnabled = True
                TipManager.addTip(schoolFamePanel.lvUpBtn, extraTips)
            else:
                canLvUp = fameLv < maxLv and curFame >= maxFame
                seekId = fdData.get('schoolLvUpSeekId', {}).get(fameLv, 0)
                if canLvUp and seekId:
                    schoolFamePanel.lvUpBtn.enabled = True
                    schoolFamePanel.lvUpBtn.data = seekId
                    schoolFamePanel.lvUpBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSchoolLvUpBtn, False, 0, True)
                else:
                    schoolFamePanel.lvUpBtn.enabled = False
                TipManager.removeTip(schoolFamePanel.lvUpBtn)
            schoolFamePanel.lvUpBtn.validateNow()
            selfSchoolFameLvShortName = SCD.data.get('selfSchoolFameLvShortName', {}).get(schoolFame, {})
            for i in xrange(2, SCHOOL_FAME_CARD_NUM + 2):
                itemMc = getattr(schoolFamePanel, 'lvCard%d' % i, None)
                if not itemMc:
                    continue
                if i < fameLv:
                    itemMc.gotoAndStop('active')
                elif i == fameLv:
                    itemMc.gotoAndStop('now')
                else:
                    itemMc.gotoAndStop('inactive')
                itemMc.fameLvName.text = selfSchoolFameLvShortName.get(i, '')

            barTye = 'self'
            if fameLv < 2:
                currentValue = 0
            elif fameLv == maxLv:
                currentValue = 100
            else:
                currentValue = (fameLv - 2) * 25 + 25.0 * curFame / (maxFame if maxFame != 0 else 1)
        else:
            schoolFamePanel.gotoAndStop('otherSchool')
            schoolFamePanel.fameLvName.text = SCD.data.get('otherSchoolFameLvName', {}).get(fameLv, '')
            for i in xrange(1, SCHOOL_FAME_CARD_NUM + 1):
                itemMc = getattr(schoolFamePanel, 'lvCard%d' % i, None)
                if not itemMc:
                    continue
                if i <= fameLv:
                    itemMc.gotoAndStop('active')
                else:
                    itemMc.gotoAndStop('inactive')

            barTye = 'type%d' % fameLv
            if fameLv == maxLv:
                currentValue = 100
            else:
                currentValue = (fameLv - 1) * 25 + 25.0 * curFame / (maxFame if maxFame != 0 else 1)
        schoolFamePanel.progressBar.bar.gotoAndStop(barTye)
        schoolFamePanel.progressBar.currentValue = currentValue
        schoolFamePanel.progressBar.validateNow()

    def refreshFameQuestPanel(self):
        fameQuestPanel = self.widget.fameQuestPanel
        p = BigWorld.player()
        fdData = FD.data.get(self.selectedFameId, {})
        schoolFame = fdData.get('schoolFame', 0)
        fameQuestPanel.title.text = gameStrings.ROLE_INFO_FAME_QUEST_PANEL_TITLE % fdData.get('desc', '')
        if schoolFame != 0:
            fameQuestPanel.doubleRewardHint.visible = False
            fameSrcNames = SCD.data.get('schoolFameSrcNames', {})
            fameBonusSrcDict = SCD.data.get('schoolFameBonusSrcDict', {})
        else:
            fameQuestPanel.doubleRewardHint.visible = True
            fameSrcNames = SCD.data.get('fameSrcNames', {})
            fameBonusSrcDict = SCD.data.get('fameBonusSrcDict', {})
        self.fameQuestList = []
        for fameSrc in const.ALL_FAME_BONUS_SRC:
            detailList = []
            detailNoLvList = []
            for desc, seekId, needLv in fdData.get('des%s' % fameSrc, ()):
                detailInfo = {'desc': uiUtils.toHtml(desc, linkEventTxt='seek:%s' % seekId),
                 'seekId': seekId}
                if p.lv >= needLv:
                    detailList.append(detailInfo)
                detailNoLvList.append(detailInfo)

            if len(detailNoLvList) == 0:
                continue
            allCount = fameBonusSrcDict.get(fameSrc, 0)
            if allCount == 0:
                rate = ''
                done = False
            else:
                bInfo = p.fameBonusInfo.get(self.selectedFameId, {}).get(fameSrc, 0)
                if type(bInfo) == tuple:
                    if utils.isSameDay(bInfo[1], utils.getNow()):
                        rate = '%d/%d' % (bInfo[0], allCount)
                        done = bInfo[0] >= allCount
                    else:
                        rate = '0/%d' % allCount
                        done = False
                else:
                    rate = '0/%d' % allCount
                    done = utils.isSameDay(bInfo, utils.getNow())
            self.fameQuestList.append({'iconType': 'type%d' % fameSrc,
             'title': fameSrcNames.get(fameSrc, ''),
             'rate': rate,
             'done': done,
             'detailList': detailList,
             'detailNoLvList': detailNoLvList})

        fameQuestLen = len(self.fameQuestList)
        for i in xrange(FAME_QUEST_KIND_NUM):
            finishMc = getattr(fameQuestPanel, 'finish%d' % i, None)
            detailMc = getattr(fameQuestPanel, 'detail%d' % i, None)
            if not finishMc or not detailMc:
                continue
            if i >= fameQuestLen:
                finishMc.visible = False
                detailMc.visible = False
                continue
            itemInfo = self.fameQuestList[i]
            finishMc.visible = True
            finishMc.icon.gotoAndStop(itemInfo.get('iconType', ''))
            finishMc.title.text = itemInfo.get('title', '')
            if itemInfo.get('done', False):
                finishMc.rate.visible = False
                finishMc.finishIcon.visible = True
            else:
                finishMc.rate.visible = True
                finishMc.rate.text = itemInfo.get('rate', '')
                finishMc.finishIcon.visible = False
            finishMc.x = 52 + (FAME_QUEST_KIND_NUM - fameQuestLen) * 45 + i * 90
            detailMc.visible = True
            detailMc.title.text = itemInfo.get('title', '')
            detailMc.lvCheckBox.selected = True
            self.updateDetailWndList(detailMc)

    def updateDetailWndList(self, detailMc):
        idx = detailMc.idx
        if idx >= len(self.fameQuestList):
            return
        if detailMc.lvCheckBox.selected:
            dataList = self.fameQuestList[idx].get('detailList', [])
        else:
            dataList = self.fameQuestList[idx].get('detailNoLvList', [])
        detailMc.wndList.dataArray = dataList

    def handleClickShopBtn(self, *args):
        shopSeekId = FD.data.get(self.selectedFameId, {}).get('shopSeekId')
        if shopSeekId:
            uiUtils.findPosWithAlert(shopSeekId)

    def handleClickLifeSkillBtn(self, *args):
        lifeskillSeekId = FD.data.get(self.selectedFameId, {}).get('lifeskillSeekId')
        if lifeskillSeekId:
            uiUtils.findPosWithAlert(lifeskillSeekId)

    def handleClickOverviewBtn(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        self.selectTab(TAB_IDX_OVERVIEW)

    def handleClickFameShopBtn(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        self.selectTab(TAB_IDX_FAMESHOP)

    def handleClickSchoolFameBtn(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        self.selectTab(TAB_IDX_SCHOOLFAME)

    def selectTab(self, tabIdx):
        self.tabIdx = tabIdx
        detail = self.widget.detail
        if tabIdx == TAB_IDX_OVERVIEW:
            detail.overviewBtn.selected = True
            detail.overviewPanel.visible = True
            detail.fameShopPanel.visible = False
            detail.schoolFamePanel.visible = False
        elif tabIdx == TAB_IDX_FAMESHOP:
            detail.fameShopBtn.selected = True
            detail.overviewPanel.visible = False
            detail.fameShopPanel.visible = True
            detail.schoolFamePanel.visible = False
        elif tabIdx == TAB_IDX_SCHOOLFAME:
            detail.schoolFameBtn.selected = True
            detail.overviewPanel.visible = False
            detail.fameShopPanel.visible = False
            detail.schoolFamePanel.visible = True

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        if e.ctrlKey and e.buttonIdx == uiConst.LEFT_BUTTON:
            itemId = int(e.currentTarget.itemId)
            self.uiAdapter.fittingRoom.addItem(Item(itemId))

    def handleSelectLvCheckBox(self, *args):
        e = ASObject(args[3][0])
        self.updateDetailWndList(e.currentTarget.parent)

    def detailItemFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.desc.htmlText = itemData.desc
        itemMc.flyBtn.data = itemData.seekId
        itemMc.flyBtn.addEventListener(events.BUTTON_CLICK, self.handleClickFlyBtn, False, 0, True)

    def handleClickFlyBtn(self, *args):
        e = ASObject(args[3][0])
        seekId = int(e.currentTarget.data)
        uiUtils.gotoTrack(seekId)

    def handleClickSchoolLvUpBtn(self, *args):
        e = ASObject(args[3][0])
        seekId = int(e.currentTarget.data)
        if seekId:
            uiUtils.findPosWithAlert(seekId)

    def handleClickFameQuestBtn(self, *args):
        self.widget.fameQuestPanel.visible = not self.widget.fameQuestPanel.visible

    def handleCloseFameQuestPanel(self, *args):
        self.widget.fameQuestPanel.visible = False

    def updateFame(self, fameId):
        if not self.widget:
            return
        if fameId in self.daibiToFameMap:
            fameId = self.daibiToFameMap.get(fameId)
        fdData = FD.data.get(fameId, {})
        if fdData.get('display', 0) != gametypes.FAME_SHOW_IN_FAMEPANEL:
            return
        if fdData.get('schoolFame', 0) and not gameglobal.rds.configData.get('enableSchoolFame', False):
            return
        fameInfo = self.getFameInfo(fameId)
        self.fameDict[fameId] = fameInfo
        itemMc = self.widget.tree.getItemByData(fameId)
        if itemMc:
            self.updateTreeItem(itemMc, fameId)
        self.refreshDetailInfo(fameId)

    def updateFameByQuestId(self, questId):
        if not self.widget:
            return
        if questId not in self.questIdToFameMap:
            return
        fameId = self.questIdToFameMap.get(questId)
        self.updateFame(fameId)
