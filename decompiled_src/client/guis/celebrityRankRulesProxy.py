#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityRankRulesProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import uiConst
import utils
import uiUtils
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import ASObject
from data import hall_of_fame_rules_desc_data as HOFRDD
from data import hall_of_fame_config_data as HOFCD
DESC_TYPE_TITLE = 0
DESC_TYPE_MAIN = 1
DESC_TYPE_MENTION = 2
TEXT_OFFSET = 10

class CelebrityRankRulesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityRankRulesProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.itemMc = None
        self.topType = 0
        self.dataCache = {}
        self.version = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CELEBRITY_RULES, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CELEBRITY_RULES:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CELEBRITY_RULES)

    def show(self, topType = 0):
        self.topType = topType
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_CELEBRITY_RULES)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.list.itemHeightFunction = self.listItemHeightFunc
        self.widget.list.itemRenderer = 'CelebrityRankRules_listItem_Text'
        self.widget.list.lableFunction = self.listItemFunc

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            if self.topType == 0:
                self.widget.mainName.text = HOFCD.data.get('rulesListName', '')
                ruleList = []
                for k, v in HOFRDD.data.iteritems():
                    ruleList.append(v)

                self.widget.list.dataArray = ruleList
            else:
                self.widget.mainName.text = HOFCD.data.get('fameResultListName', '')
                curSeason = self.dataCache.get('curSeason', None)
                if curSeason == None:
                    pass
                else:
                    allList = []
                    for seasonTitle, value in self.dataCache.get(self.topType, {}).iteritems():
                        titleInfo = {'type': DESC_TYPE_TITLE,
                         'desc': seasonTitle}
                        allList.append(titleInfo)
                        if self.topType in [gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI, gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING]:
                            for typeTitle, nameList in value.iteritems():
                                titleInfo = {'type': DESC_TYPE_MENTION,
                                 'desc': typeTitle}
                                allList.append(titleInfo)
                                allList.extend(nameList)

                        else:
                            allList.extend(value)

                    self.widget.list.dataArray = allList
            return

    def onGetFameHallInfo(self, infoDic, curTopType, ver):
        if self.version == ver:
            self.show(curTopType)
            return
        self.dataCache = {}
        self.version = ver
        info = sorted(infoDic.iteritems(), key=lambda d: d[0])
        lastSeason = 0
        for season, value in info:
            lastSeason = season
            for topType, dataDict in value.iteritems():
                topDic = self.dataCache.setdefault(topType, {})
                for lvKey in sorted(dataDict.keys(), reverse=True):
                    dataList = dataDict[lvKey]
                    dataList.sort(key=lambda v: v[3])
                    seasonKey = gameStrings.CELEBRITY_RANK_STATUE_TITLE.format(season=season, topName=HOFCD.data.get('rankName', {}).get(topType, ''))
                    lvStr = self.getLvTitleStr(lvKey)
                    for data in dataList:
                        hostId = utils.getHostIdFromNameWithHostIdStr(data[1])
                        roleName = utils.getRoleNameFromNameWithHostIdStr(data[1])
                        schoolId = data[2]
                        showText = '{name} - {serverName}'.format(name=roleName, serverName=utils.getServerName(hostId))
                        showInfo = {'type': DESC_TYPE_MAIN,
                         'desc': showText}
                        if topType == gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI:
                            topDic.setdefault(seasonKey, {}).setdefault(lvStr, []).append(showInfo)
                        elif topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING:
                            if lvKey in gametypes.TOTAL_TOP_RANK_KEY_TYPE:
                                continue
                            lvKey = '{lvStr}-{schoolName}'.format(lvStr=lvStr, schoolName=uiUtils.getSchoolNameById(schoolId))
                            topDic.setdefault(seasonKey, {}).setdefault(lvKey, []).append(showInfo)
                        else:
                            topDic.setdefault(seasonKey, []).append(showInfo)

        self.dataCache['curSeason'] = lastSeason
        self.show(curTopType)

    def getLvTitleStr(self, lvKey):
        tSplit = lvKey.split('_')
        szKey = ''
        if len(tSplit) > 1:
            szKey = gameStrings.CELEBRITY_LEVEL_TITLE_STR % (tSplit[0], tSplit[1])
        return szKey

    def listItemFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.itemMc = itemMc
        if itemData.type == DESC_TYPE_MENTION:
            itemMc.mentionTextMc.visible = True
            itemMc.mainTextMc.visible = False
            itemMc.titleText.visible = False
            itemMc.mentionTextMc.htmlText = itemData.desc
            itemMc.mentionTextMc.height = itemMc.mentionTextMc.textHeight + TEXT_OFFSET
        elif itemData.type == DESC_TYPE_MAIN:
            itemMc.mentionTextMc.visible = False
            itemMc.mainTextMc.visible = True
            itemMc.titleText.visible = False
            itemMc.mainTextMc.htmlText = itemData.desc
            itemMc.mainTextMc.height = itemMc.mainTextMc.textHeight + TEXT_OFFSET
        elif itemData.type == DESC_TYPE_TITLE:
            itemMc.mentionTextMc.visible = False
            itemMc.mainTextMc.visible = False
            itemMc.titleText.visible = True
            itemMc.titleText.htmlText = itemData.desc
            itemMc.titleText.height = itemMc.titleText.textHeight + TEXT_OFFSET

    def listItemHeightFunc(self, *args):
        itemData = ASObject(args[3][0])
        if itemData.type == DESC_TYPE_MENTION:
            self.widget.textHelper.mentionTextMc.text = itemData.desc
            return GfxValue(self.widget.textHelper.mentionTextMc.textHeight + TEXT_OFFSET)
        if itemData.type == DESC_TYPE_MAIN:
            self.widget.textHelper.mainTextMc.text = itemData.desc
            return GfxValue(self.widget.textHelper.mainTextMc.textHeight + TEXT_OFFSET)
        if itemData.type == DESC_TYPE_TITLE:
            self.widget.textHelper.titleText.text = itemData.desc
            return GfxValue(self.widget.textHelper.titleText.textHeight + TEXT_OFFSET)
