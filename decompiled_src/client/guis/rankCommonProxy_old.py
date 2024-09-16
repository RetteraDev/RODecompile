#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankCommonProxy_old.o
from gamestrings import gameStrings
import random
import string
import BigWorld
import const
import gamelog
import gameglobal
import uiConst
import events
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import MenuManager
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis import rankPanelUtils
from guis import rankCommonUtils
from guis import uiUtils
from guis import tipUtils
from callbackHelper import Functor
from gamestrings import gameStrings
from data import rank_common_data as RCD
from data import rank_common_format_data as RCFD
GROUP_INTERNAL = 10
START_TOP_POS = 67
RANK_ITEM_RENDER_HEIGHT = 36
RANK_ITEM_SEASON_RENDER_HEIGHT = 140
TOTAL_COL_NUM = 6
CUSTORM_DROPDOWN_WITH_SCHOOL_X = 137
FONT_COLOR_GREEN = '#5EBC5E'

def getAllLvIndex(lvRanges):
    if not lvRanges:
        return -1
    arr = []
    for item in lvRanges:
        arr.extend(item.split('_'))

    if len(arr) < 2:
        return -1
    arr.sort()
    maxStr = str(arr[0]) + '_' + str(arr[-1])
    for i in xrange(0, len(lvRanges)):
        if lvRanges[i] == maxStr:
            return i

    return -1


def handleTop3Icon(item, rank):
    if rank > 0 and rank <= 3:
        item.top3Icon.visible = True
        item.top3Icon.x = 2
        item.rank.text = ''
        item.rank.htmlText = ''
        item.top3Icon.gotoAndStop(rank * 5)
    else:
        item.top3Icon.visible = False


class RankCommonProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankCommonProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.currentTopId = -1
        self.selectedItem = None
        self.currentList = None
        self.lvKey = ''
        self.originLvBtnGroupPosX = 0
        self.listColX = []
        self.listColWidth = []
        self.selectItem = None
        self.schoolId = 0
        self.commonRankInfo = {}
        self.updateBtnCooldownTimeDic = {}
        self.myRank = -1
        self.myRankIdx = -1
        self.customDropdownKey = -1
        self.customKey = -1
        self.zmjSpriteData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANK_COMMON, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANK_COMMON:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.funcNpc.close()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANK_COMMON)
        self.selectedItem = None
        self.currentList = None
        self.originLvBtnGroupPosX = 0
        self.listColX = []
        self.listColWidth = []
        self.selectItem = None

    def initUI(self):
        self.schoolMenu = rankPanelUtils.SchoolMenuUtil()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.filterGroup.lvBtnGroup.lvBtn0.addEventListener(events.BUTTON_CLICK, self.onLvClick, False, 0, True)
        self.widget.filterGroup.lvBtnGroup.lvBtn1.addEventListener(events.BUTTON_CLICK, self.onLvClick, False, 0, True)
        self.widget.filterGroup.lvBtnGroup.lvBtn2.addEventListener(events.BUTTON_CLICK, self.onLvClick, False, 0, True)
        self.widget.filterGroup.lvBtnGroup.lvBtn3.addEventListener(events.BUTTON_CLICK, self.onLvClick, False, 0, True)
        self.originLvBtnGroupPosX = self.widget.filterGroup.lvBtnGroup.x
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleUpdateBtnClick, False, 0, True)
        self.widget.checkMyRank.addEventListener(events.BUTTON_CLICK, self.handleCheckMyRank, False, 0, True)
        self.refreshCommonRank(self.currentTopId)
        self.requestCommonRank()

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def showRankCommon(self, topId, customDropdownKey = -1):
        if topId not in RCD.data:
            return
        gamelog.debug('ypc@ showRankCommon ', topId)
        self.currentTopId = topId
        self.customKey = rankCommonUtils.getCustomKeyByTopId(topId)
        self.customDropdownKey = customDropdownKey if customDropdownKey >= 0 else rankCommonUtils.getCustomDropdownKeyByTopId(topId)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANK_COMMON)
        else:
            self.refreshCommonRank(topId)
            self.requestCommonRank()

    def refreshCommonRank(self, topId):
        if not self.widget or topId not in RCD.data:
            return
        else:
            p = BigWorld.player()
            self.currentTopId = topId
            config = RCD.data.get(topId, {})
            self.widget.tabGroup.visible = False
            self.widget.rewardGroup.visible = False
            self.widget.rewardGroup.rule.htmlText = ''
            self.widget.filterGroup.visible = False
            self.widget.filterGroup.customDropdown.visible = False
            self.widget.detailLabel.visible = False
            self.widget.listGroup.listrow9.visible = False
            self.widget.listGroup.listrow10.visible = False
            self.widget.listGroup.listrow11.visible = False
            self.widget.listGroup.listrow12.visible = False
            self.widget.myRank.visible = False
            self.widget.checkMyRank.visible = False
            self.widget.lastRank.visible = False
            self.widget.rewardGroup.rewardInfo.visible = False
            self.widget.addition.htmlText = ''
            self.widget.myRank.htmlText = ''
            self.widget.lastRank.htmlText = ''
            self.schoolId = 0
            self.lvKey = ''
            self.widget.rankTitle.text = config.get('TopTitle', '')
            startY = START_TOP_POS
            listRowNum = 0
            tabTopIds = config.get('TabTopIds', ())
            if tabTopIds:
                tabCount = len(tabTopIds)
                self.widget.tabGroup.gotoAndStop('num%d' % tabCount)
                self.widget.tabGroup.visible = True
                self.widget.tabGroup.y = startY
                startY += self.widget.tabGroup.height + GROUP_INTERNAL
                listRowNum += 1
                for i in xrange(0, tabCount):
                    tab = self.widget.tabGroup.getChildByName('tabBtn%d' % (i + 1))
                    if not tab.hasEventListener(events.BUTTON_CLICK):
                        tab.addEventListener(events.BUTTON_CLICK, self.onTabClickBtn, False, 0, True)
                    tabName = RCD.data.get(tabTopIds[i], {}).get('Rankingname', '')
                    tab.data = tabTopIds[i]
                    tab.selected = i == tabTopIds.index(self.currentTopId)
                    tab.label = tabName

            topDesc = config.get('TopDesc', None)
            rewardInfo = config.get('RewardInfo', None)
            haswards = config.get('warditem1', None) or config.get('warditem2', None) or config.get('warditem3', None)
            if topDesc or rewardInfo or haswards:
                self.widget.rewardGroup.visible = True
                self.widget.rewardGroup.y = startY
                startY += self.widget.rewardGroup.height + GROUP_INTERNAL
                listRowNum += 2
                rewardCount = 0
                for x in xrange(0, 3):
                    if config.get('warditem%d' % (x + 1), None):
                        rewardCount += 1

                self.widget.rewardGroup.gotoAndStop('num%d' % rewardCount)
                for i in xrange(0, rewardCount):
                    itemId = config.get('warditem%d' % (i + 1), -1)
                    rewardMc = self.widget.rewardGroup.getChildByName('reward%d' % (i + 1))
                    if itemId > 0:
                        rewardMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, 0))
                        rewardMc.slot.dragable = False
                        rewardMc.slot.enabled = True

                if config.get('TopDesc', None):
                    self.widget.rewardGroup.rule.htmlText = config['TopDesc']
                rewardInfoMc = self.widget.rewardGroup.getChildByName('rewardInfo')
                if rewardInfoMc:
                    self.widget.rewardGroup.rewardInfo.visible = config.get('RewardInfo', None) is not None
                    self.widget.rewardGroup.rewardInfo.addEventListener(events.BUTTON_CLICK, self.handleShowRewardInfo, False, 0, True)
                    self.widget.rewardGroup.rewardInfo.label = gameStrings.GENERAL_REWARD_DEFAULT_TITLE
            showLvFilter = config.get('LvFiter', 0) == 1
            showSchoolFiter = config.get('schoolFiter', 0) == 1
            customDropdownData = config.get('customDropdown', ())
            if showLvFilter or showSchoolFiter or customDropdownData:
                self.widget.filterGroup.visible = True
                self.widget.filterGroup.y = startY
                startY += self.widget.filterGroup.height + GROUP_INTERNAL
                listRowNum += 1
                self.widget.filterGroup.schoolDropdown.visible = showSchoolFiter
                if showSchoolFiter:
                    showAllSchool = config.get('schoolAll', 0)
                    schoolList = rankPanelUtils.getCompleteMenuData() if showAllSchool else rankPanelUtils.getDefaultSchoolMenuData()
                    self.schoolMenu.unregister()
                    self.schoolId = 0 if showAllSchool else BigWorld.player().realSchool
                    schoolIndex = 0
                    for i in xrange(0, len(schoolList)):
                        if self.schoolId == schoolList[i]['schoolId']:
                            schoolIndex = i
                            break

                    self.schoolMenu.register(self.widget.filterGroup.schoolDropdown, self.onSchoolMenuChange, schoolList, schoolIndex)
                self.widget.filterGroup.lvBtnGroup.visible = showLvFilter
                if showLvFilter:
                    lvRanges = config.get('lvint', ['0_0'])
                    lvRangeNum = len(lvRanges)
                    allLvIndex = getAllLvIndex(lvRanges)
                    self.lvKey = ''
                    for i in xrange(0, 4):
                        btn = self.widget.filterGroup.lvBtnGroup.getChildByName('lvBtn' + str(i))
                        if i < lvRangeNum:
                            label = gameStrings.RANKINGV2_ALL_LEVEL if allLvIndex == i else 'Lv.' + str(lvRanges[i]).replace('_', '-')
                            if gameglobal.rds.configData.get('enableTopRankNewLv89', False):
                                label = label.replace('79', '89')
                            btn.label = label
                            btn.data = lvRanges[i]
                            btn.visible = True
                            lvRange = lvRanges[i].split('_')
                            if not self.lvKey and p.lv in xrange(int(lvRange[0]), int(lvRange[1]) + 1):
                                self.lvKey = lvRanges[i]
                                btn.selected = True
                        else:
                            btn.visible = False

                    if self.lvKey == '' and lvRangeNum > 0:
                        self.lvKey = lvRanges[0]
                        self.widget.filterGroup.lvBtnGroup.getChildByName('lvBtn0').selected = True
                    self.widget.filterGroup.lvBtnGroup.x = self.originLvBtnGroupPosX + 60 * (4 - lvRangeNum)
                if customDropdownData:
                    self.widget.filterGroup.customDropdown.visible = True
                    if showSchoolFiter:
                        self.widget.filterGroup.customDropdown.x = CUSTORM_DROPDOWN_WITH_SCHOOL_X
                    else:
                        self.widget.filterGroup.customDropdown.x = 0
                    selectIdx = -1
                    if self.customDropdownKey != -1:
                        for i, cdData in enumerate(customDropdownData):
                            if cdData[1] == self.customDropdownKey:
                                selectIdx = i
                                break

                    if selectIdx == -1:
                        self.customDropdownKey = customDropdownData[0][1]
                        selectIdx = 0
                    ddData = [ {'label': cdd[0],
                     'data': cdd[1]} for cdd in customDropdownData ]
                    ASUtils.setDropdownMenuData(self.widget.filterGroup.customDropdown, ddData)
                    self.widget.filterGroup.customDropdown.removeEventListener(events.INDEX_CHANGE, self.handleCustomDropdown)
                    self.widget.filterGroup.customDropdown.selectedIndex = selectIdx
                    self.widget.filterGroup.customDropdown.addEventListener(events.INDEX_CHANGE, self.handleCustomDropdown, False, 0, True)
            if not self.widget.rewardGroup.visible or not self.widget.filterGroup.visible:
                self.widget.detailLabel.visible = True
                self.widget.detailLabel.y = startY
                startY += self.widget.detailLabel.height + GROUP_INTERNAL
                listRowNum += 1
            self.currentList = self.widget.listGroup.getChildByName('listrow%d' % (12 - listRowNum + 1))
            self.currentList.visible = True
            self.widget.listGroup.y = self.widget.downline.y - 4 - self.currentList.height - 30
            generalConfigs = config.get('GeneralColConfigs', [])
            if generalConfigs:
                isSeason = config.get('isSeason', 0) == 1
                self.currentList.itemHeight = RANK_ITEM_SEASON_RENDER_HEIGHT if isSeason else RANK_ITEM_RENDER_HEIGHT
                self.currentList.itemRenderer = 'RankCommon_CommonRankItem_Hero' if isSeason else 'RankCommon_Item'
                self.currentList.lableFunction = self.commonRankItemHeroFunction if isSeason else self.commonRankItemFunction
                self.currentList.dataArray = []
                self.listColX = []
                self.listColWidth = []
                totalWidth = 0
                colNum = len(generalConfigs)
                colConfigs = []
                for cfgIdx in generalConfigs:
                    tmpIdx = cfgIdx
                    if type(cfgIdx) is tuple:
                        tmpIdx = cfgIdx[0]
                    colCfg = RCFD.data.get(tmpIdx, {})
                    if not colCfg.get('isHide', False):
                        colWidth = colCfg.get('Width', 0)
                        colName = colCfg.get('name', '')
                        totalWidth += colWidth
                        colConfigs.append((colWidth, colName))

                interval = max(0, (511 - totalWidth) / (colNum + 1))
                curX = 48 + interval
                for i in xrange(0, 5):
                    mc = self.widget.listGroup.getChildByName('rankcol%d' % (i + 1))
                    if i < colNum:
                        colWidth = colConfigs[i][0]
                        mc.text = colConfigs[i][1]
                        mc.x = curX
                        mc.width = colWidth
                        mc.visible = True
                        self.listColX.append(curX)
                        self.listColWidth.append(colWidth)
                        curX += colWidth + interval
                    else:
                        mc.visible = False

            self.widget.refreshBtn.visible = config.get('refreshBtn', 0) == 1
            self.widget.bottomRule.htmlText = config.get('BottomDesc', '')
            if config.get('Newranking', 0) == 1:
                self.widget.myRank.visible = True
                self.widget.myRank.htmlText = gameStrings.COMMON_RANK_MY_RANK % ''
            if config.get('Newrankingicon', 0) == 1:
                self.widget.checkMyRank.visible = True
            if config.get('LastWeekranking', 0) == 1:
                self.widget.lastRank.visible = True
                self.widget.lastRank.htmlText = gameStrings.COMMON_RANK_LASTWEEK_RANK % ''
            self.refreshUpdateBtnState()
            return

    def onTabClickBtn(self, *args):
        e = ASObject(args[3][0])
        topId = e.currentTarget.data
        if self.currentTopId == topId or topId not in RCD.data:
            return
        if self.selectedItem:
            self.selectedItem.selected = False
        self.selectedItem = e.currentTarget
        self.selectedItem.selected = True
        self.showRankCommon(topId)

    def onLvClick(self, *args):
        e = ASObject(args[3][0])
        self.lvKey = e.currentTarget.data
        self.requestCommonRank()

    def onSchoolMenuChange(self):
        self.schoolId = self.schoolMenu.menuData[self.schoolMenu.menuMc.selectedIndex]['schoolId']
        self.requestCommonRank()

    def commonRankItemHeroFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.seasonDes.htmlText = getattr(itemData, 'desc', '')
        for i in xrange(0, 3):
            child = itemMc.getChildByName('rank%d' % i)
            childData = getattr(itemData, 'rank%d' % i, None)
            if not childData:
                child.visible = False
            else:
                child.visible = True
                self.commonRankItemFunctionInternal(childData, child)

    def commonRankItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.commonRankItemFunctionInternal(itemData, itemMc)

    def commonRankItemFunctionInternal(self, itemData, itemMc):
        FORMAT_COLOR = "<font color = \'#a65b11\'>%s</font>"
        config = RCD.data.get(self.currentTopId, {})
        if config:
            if itemMc.memberNum:
                itemMc.memberNum.visible = False
            index = getattr(itemData, 'index', 0)
            isSelf = getattr(itemData, 'isSelf', False)
            itemMc.rank.htmlText = FORMAT_COLOR % str(index) if isSelf else index
            handleTop3Icon(itemMc, index)
            roleName = ''
            gbId = 0
            colSevIndices = []
            generalConfigs = config.get('GeneralColConfigs', [])
            for cfgIdx in generalConfigs:
                fmtCfg = RCFD.data.get(cfgIdx, {})
                if not fmtCfg.get('isHide', False):
                    colSevIndices.append(fmtCfg.get('ServerIndex', 0))

            colNum = len(generalConfigs)
            itemMc.rank.x = -15
            for i in xrange(1, TOTAL_COL_NUM):
                child = itemMc.getChildByName('data%d' % i)
                data = getattr(itemData, 'data%d' % i, '')
                if i <= colNum:
                    if colSevIndices[i - 1] == gametypes.TOP_UNIVERSAL_ROLE_NAME:
                        roleName = getattr(itemData, 'data%d' % i, '')
                        gbId = getattr(itemData, 'roleGbid', 0)
                    child.x = self.listColX[i - 1] - 9
                    child.width = self.listColWidth[i - 1]
                    if colSevIndices[i - 1] == gametypes.TOP_UNIVERSAL_GUILD_ATTEND_COUNT_EX:
                        itemMc.memberNum.gotoAndStop(data)
                        itemMc.memberNum.x = child.x + child.width * 0.5 - itemMc.memberNum.width * 0.5
                        itemMc.memberNum.visible = True
                        child.visible = False
                    else:
                        child.htmlText = FORMAT_COLOR % data if isSelf else data
                        child.visible = True
                else:
                    child.visible = False
                dmgTip = getattr(itemData, 'dmgTip%d' % i, '')
                if dmgTip:
                    TipManager.addTip(child, dmgTip)
                else:
                    TipManager.removeTip(child)

            itemMc.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)
            if gbId:
                itemMc.gbId = gbId
            if roleName and gbId:
                MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': roleName,
                 'gbId': gbId})
            spriteUUID = getattr(itemData, 'spriteUUID', None)
            if spriteUUID:
                TipManager.addTipByType(itemMc, tipUtils.TYPE_SPRITE_SIMPLE_TIP, (spriteUUID,), False)
            tipContent = getattr(itemData, 'tipContent', '')
            if self.currentTopId not in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
                if tipContent:
                    TipManager.addTip(itemMc, tipContent)
            if self.currentTopId in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
                detailInfo = self.zmjSpriteData.get(int(gbId), {})
                spriteId = detailInfo.get(const.SPRITE_DICT_INDEX_spriteId, 0)
                if gbId and spriteId:
                    TipManager.addTipByType(itemMc, tipUtils.TYPE_ZMJ_SPRITE_SIMPLE_TIP, (int(gbId),), False)

    def onItemClick(self, *args):
        gamelog.debug('ypc@onItemClick')
        e = ASObject(args[3][0])
        if self.selectItem:
            self.selectItem.gotoAndStop('up')
        self.selectItem = e.currentTarget
        self.selectItem.gotoAndStop('down')
        if self.currentTopId in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
            if self.selectItem.gbId:
                spriteTip = TipManager.getTargetTip()
                detailInfo = self.zmjSpriteData.get(int(self.selectItem.gbId), {})
                spriteId = detailInfo.get(const.SPRITE_DICT_INDEX_spriteId, 0)
                if spriteTip and spriteId:
                    gameglobal.rds.ui.summonedWarSprite.showSpriteDetailTip(detailInfo, 'zmjSprite', spriteTip.x, spriteTip.y)

    def requestCommonRank(self):
        p = BigWorld.player()
        config = RCD.data.get(self.currentTopId, {})
        cachekey, serverKey = rankCommonUtils.genCacheKeyAndServerKey(config, self.lvKey, self.schoolId, self.customDropdownKey, self.customKey)
        if cachekey not in self.commonRankInfo:
            self.commonRankInfo[cachekey] = {}
        else:
            cache = self.commonRankInfo[cachekey].get('cache', {})
            if cache.get('playerGbId', 0) and cache.get('playerGbId', 0) != p.gbId:
                self.commonRankInfo[cachekey] = {}
        ver = self.commonRankInfo[cachekey].get('ver', 0)
        self.refreshCommonRankView(self.commonRankInfo[cachekey].get('cache', {}))
        if self.currentTopId == gametypes.TOP_TYPE_CLAN_WAR_EVENT:
            gamelog.info('jbx:queryClanWarEventTop', ver, serverKey)
            p.cell.queryClanWarEventTop(ver, serverKey)
        elif self.currentTopId == gametypes.TOP_TYPE_GUILD_MEMBER_RECORD_SCORE:
            gamelog.info('jbx:queryGuildMemberTopRecordScore', ver, serverKey)
            p.cell.queryGuildMemberTopRecordScore(ver, serverKey)
        else:
            p.base.queryTopUniversal(self.currentTopId, ver, serverKey)
        gamelog.debug('ypc@ request customKey = ', self.customKey)
        gamelog.debug('ypc@ request cache key = ', cachekey)
        gamelog.debug('ypc@ request server key = ', serverKey)

    def refreshCommonRankView(self, cacheData):
        if not self.widget:
            return
        self.myRank = cacheData.get('myRank', -1)
        self.myRankIdx = cacheData.get('myRankIdx', -1)
        myLastRank = cacheData.get('lastRank', -1)
        addition = cacheData.get('addition', ())
        datalist = cacheData.get('list', [])
        config = RCD.data.get(self.currentTopId, {})
        customContents = config.get('customKey', ())
        if 'customKey' in cacheData and cacheData['customKey'] in xrange(0, len(customContents)):
            self.widget.filterGroup.specialTitle.visible = True
            self.widget.filterGroup.specialTitle.textfield.text = customContents[cacheData['customKey']][0]
        else:
            self.widget.filterGroup.specialTitle.visible = False
        self._changeColLabel()
        self.widget.checkMyRank.enabled = self.myRank > 0
        self.widget.myRank.htmlText = gameStrings.COMMON_RANK_MY_RANK % str(self.myRank) if self.myRank > 0 else gameStrings.COMMON_RANK_OUT_OF_RANK
        self.widget.lastRank.htmlText = gameStrings.COMMON_RANK_LASTWEEK_RANK % (str(myLastRank) if myLastRank > 0 else '')
        self._updateAddtionValueSpecial(addition)
        if self.currentTopId in (gametypes.TOP_TYPE_ZMJ_FUBEN,):
            self.currentList.dataArray = datalist[0:const.ZMJ_REWARD_REFREENCE_RANK]
        else:
            self.currentList.dataArray = datalist

    def _changeColLabel(self):
        config = RCD.data.get(self.currentTopId, {})
        dropdownData = config.get('customDropdown', [])
        if dropdownData:
            generalConfigs = config.get('GeneralColConfigs', [])
            gamelog.debug('ypc@ generalConfigs = ', generalConfigs)
            for i in range(0, min(TOTAL_COL_NUM, len(generalConfigs))):
                colcfgIndex = generalConfigs[i]
                gamelog.debug('ypc@ colcfgIndex = ', colcfgIndex)
                if type(colcfgIndex) is tuple:
                    ddKeyIdx = -1
                    ddKeys = [ x[1] for x in dropdownData ]
                    gamelog.debug('ypc@ ddKeys = ', ddKeys)
                    if self.customDropdownKey in ddKeys:
                        ddKeyIdx = ddKeys.index(self.customDropdownKey)
                    if ddKeyIdx != -1:
                        colMc = self.widget.listGroup.getChildByName('rankcol%d' % (i + 1))
                        colCfg = RCFD.data.get(colcfgIndex[ddKeyIdx], {})
                        if colMc and not colCfg.get('isHide', False):
                            colMc.text = colCfg.get('name', '')

    def updateCommnonRankData(self, data):
        gamelog.debug('ypc@ updateCommnonRankData = ', data)
        topId = data[gametypes.TOP_UNIVERSAL_TOP_ID]
        if topId != self.currentTopId:
            return
        serverKey = data.get(gametypes.TOP_UNIVERSAL_KEY, '')
        cacheKey = rankCommonUtils.getRankCommonCacheKey(topId, serverKey)
        ver = data.get(gametypes.TOP_UNIVERSAL_VERSION, 0)
        myInfo = data.get(gametypes.TOP_UNIVERSAL_MY_INFO, {})
        datalist = data.get(gametypes.TOP_UNIVERSAL_DATA_LIST, [])
        sortRule = data.get(gametypes.TOP_UNIVERSAL_SORT, ())
        gamelog.debug('ypc@ updateCommnonRankData sort = ', sortRule)
        config = RCD.data.get(topId, {})
        ret = {}
        ret.update(rankCommonUtils.getRankDataByConfig(config, datalist, myInfo, sortRule, serverKey))
        self.commonRankInfo[cacheKey] = {}
        self.commonRankInfo[cacheKey]['ver'] = ver
        self.commonRankInfo[cacheKey]['cache'] = ret
        self.refreshCommonRankView(ret)
        gamelog.debug('ypc@ update customKey = ', self.customKey)
        gamelog.debug('ypc@ update cache key = ', cacheKey)
        gamelog.debug('ypc@ update server key = ', serverKey)

    def startUpdateBtnCooldownTimer(self):
        self.updateBtnCooldownTimeDic[self.currentTopId] = 61
        BigWorld.callback(0, Functor(self.__updateBtnTimerCallback, self.currentTopId))

    def __updateBtnTimerCallback(self, *args):
        topId = args[0]
        self.updateBtnCooldownTimeDic[topId] -= 1
        if self.updateBtnCooldownTimeDic[topId] > 0:
            BigWorld.callback(1, Functor(self.__updateBtnTimerCallback, topId))
        if self.currentTopId == topId:
            self.setUpdateBtnState(self.updateBtnCooldownTimeDic[topId])

    def refreshUpdateBtnState(self):
        self.setUpdateBtnState(self.updateBtnCooldownTimeDic.get(self.currentTopId, 0))

    def setUpdateBtnState(self, cooldownTime):
        if not self.widget:
            return
        updateBtn = self.widget.refreshBtn
        updateBtn.enabled = cooldownTime == 0
        if cooldownTime > 0:
            updateBtn.label = gameStrings.REFRESH_BTN_LABEL_CD % cooldownTime
        else:
            updateBtn.label = gameStrings.REFRESH_BTN_LABEL

    def handleUpdateBtnClick(self, *args):
        self.startUpdateBtnCooldownTimer()
        self.requestCommonRank()

    def handleCheckMyRank(self, *args):
        if self.myRankIdx >= 0:
            self.currentList.scrollTo(self.myRankIdx * 37)

    def handleShowRewardInfo(self, *args):
        rewardKey = RCD.data.get(self.currentTopId, {}).get('RewardInfo', None)
        if not rewardKey:
            return
        else:
            rewards = rankCommonUtils.getCommonAwardInfo(rewardKey)
            gameglobal.rds.ui.rankingAwardCommon.showAwardCommon(rewards)
            return

    def handleCustomDropdown(self, *args):
        e = ASObject(args[3][0])
        selected = self.widget.filterGroup.customDropdown.selectedIndex
        customDropdownKeys = RCD.data.get(self.currentTopId, {}).get('customDropdown', ())
        if not customDropdownKeys or selected not in xrange(0, len(customDropdownKeys)):
            return
        self.customDropdownKey = customDropdownKeys[selected][1]
        self.requestCommonRank()

    def clearCache(self):
        gamelog.debug('ypc@ common rank clear cache!')
        self.commonRankInfo = {}
        self.clearWidget()

    def _updateAddtionValueSpecial(self, additionData):
        if not self.widget:
            return
        self.widget.cutoff.y = 605
        if not additionData or len(additionData) % 2 != 0:
            self.widget.addition.htmlText = ''
            return
        config = RCD.data.get(self.currentTopId, {})
        if 'addition' not in config:
            self.widget.addition.htmlText = ''
            return
        value = rankCommonUtils.getAdditionValueLocal(self.currentTopId)
        if value:
            label, index = config['addition']
            self.widget.addition.htmlText = ': '.join((label, self.colorString(str(value), FONT_COLOR_GREEN)))
        else:
            addtionText = ''
            for i in xrange(len(additionData) / 2):
                label = additionData[i * 2]
                value = additionData[i * 2 + 1]
                addtionText += ': '.join((label, self.colorString(str(value), FONT_COLOR_GREEN)))
                if i != len(additionData) / 2 - 1:
                    addtionText += '\n'

            self.widget.addition.htmlText = addtionText
            self.widget.cutoff.y = self.widget.downline.y + self.widget.addition.textHeight + 8
            gamelog.debug('ypc@ _updateAddtionValueSpecial!', addtionText, additionData)

    def colorString(self, str, color):
        str = "<font color = \'" + color + "\'>" + str + '</font>'
        return str

    def genFakeData(self):
        FAKE_DATA_NUM = 100
        config = RCD.data.get(self.currentTopId, {})
        data = {}
        data[gametypes.TOP_UNIVERSAL_TOP_ID] = self.currentTopId
        cachekey, serverKey = rankCommonUtils.genCacheKeyAndServerKey(config, self.lvKey, self.schoolId, self.customDropdownKey, self.customKey)
        data[gametypes.TOP_UNIVERSAL_KEY] = serverKey
        data[gametypes.TOP_UNIVERSAL_VERSION] = self.commonRankInfo[cachekey].get('ver', 0)
        if 'addition' in config:
            addition = config['addition']
            tmp = {}
            for i in xrange(len(addition) / 2):
                serverIndex = addition[i * 2 + 1]
                tmp[serverIndex] = int(random.random() * 10000)

            data[gametypes.TOP_UNIVERSAL_MY_INFO] = tmp
            gamelog.debug('ypc@ genFakeData addition', data[gametypes.TOP_UNIVERSAL_MY_INFO])
        else:
            data[gametypes.TOP_UNIVERSAL_MY_INFO] = {}
        data[gametypes.TOP_UNIVERSAL_SORT] = []
        colCfg = config.get('GeneralColConfigs', [])
        for c in colCfg:
            if RCFD.data.get(c, {}).get('ServerIndex', -1) == gametypes.TOP_UNIVERSAL_GUILD_ATTEND_COUNT_EX:
                data[gametypes.TOP_UNIVERSAL_SORT].append((gametypes.TOP_UNIVERSAL_SORT_DESC, gametypes.TOP_UNIVERSAL_GUILD_ATTEND_COUNT_EX))
                break

        data[gametypes.TOP_UNIVERSAL_SORT] = tuple(data[gametypes.TOP_UNIVERSAL_SORT])
        data[gametypes.TOP_UNIVERSAL_DATA_LIST] = []
        for i in range(FAKE_DATA_NUM):
            fakeDataTmp = {}
            for c in colCfg:
                fmtCfg = RCFD.data.get(c, {})
                sidx = fmtCfg.get('ServerIndex', None)
                if sidx == gametypes.TOP_UNIVERSAL_ROLE_NAME or sidx == gametypes.TOP_UNIVERSAL_GUILD_NAME:
                    fakeDataTmp[sidx] = self._makeRandomString()
                else:
                    fakeDataTmp[sidx] = int(random.random() * 1000)

            if i == 0:
                fakeDataTmp[gametypes.TOP_UNIVERSAL_TIP_CONTENT] = gameStrings.TEXT_RANKCOMMONPROXY_705
            else:
                fakeDataTmp[gametypes.TOP_UNIVERSAL_TIP_CONTENT] = (11111,
                 'asdfasdf',
                 1.2333,
                 gameStrings.TEXT_RANKCOMMONPROXY_705)
            data[gametypes.TOP_UNIVERSAL_DATA_LIST].append(fakeDataTmp)

        self.updateCommnonRankData(data)

    def _makeRandomString(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def addZmjSpriteInfo(self, gbId, info):
        if gbId and info:
            self.zmjSpriteData[int(gbId)] = info

    def getZmjSpriteTipDataByGbId(self, gbId):
        detailInfo = self.zmjSpriteData.get(int(gbId), {})
        if not detailInfo:
            return detailInfo
        info = {}
        info['spriteId'] = detailInfo.get(const.SPRITE_DICT_INDEX_spriteId, 0)
        info['bindType'] = detailInfo.get(const.SPRITE_DICT_INDEX_bindType, 0)
        info['skills'] = {'naturals': detailInfo.get(const.SPRITE_DICT_INDEX_naturals, []),
         'bonus': detailInfo.get(const.SPRITE_DICT_INDEX_bonus, [])}
        info['name'] = detailInfo.get(const.SPRITE_DICT_INDEX_name, '')
        famiEffLv = detailInfo.get(const.SPRITE_DICT_INDEX_famiEffLv, 0)
        famiEffAdd = detailInfo.get(const.SPRITE_DICT_INDEX_famiEffAdd, 0)
        info['props'] = {'lv': detailInfo.get(const.SPRITE_DICT_INDEX_lv, 0),
         'famiEffLv': famiEffLv,
         'famiEffAdd': famiEffAdd,
         'familiar': famiEffLv - famiEffAdd}
        tipInfo = gameglobal.rds.ui.summonedWarSpriteMine.getSpriteTipByInfo(info, oriData=True)
        tipInfo['spriteDps'] = detailInfo.get('spriteDps', 0)
        return uiUtils.dict2GfxDict(tipInfo, True)
