#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guibaogeProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import const
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from item import Item
from Scaleform import GfxValue
from ui import gbk2unicode
from helpers import fittingModel
from data import gui_bao_ge_data as GBGD
from data import gui_bao_ge_config_data as GBDCD
from data import item_data as ID
from data import seeker_data as SEEKD
from data import npc_data as ND
from data import school_data as SD
from cdata import evaluate_set_appearance_reverse_data as ESARD

class GuibaogeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuibaogeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetGuiBaoData,
         'getItemDetailInfo': self.onGetGuiBaoDetailInfo,
         'getJishiInfo': self.onGetJishiInfo,
         'openAchievementPanel': self.onOpenAchievePanel,
         'findPath': self.onGuibaoFindPath,
         'resetPreview': self.onResetPreview,
         'updatePreview': self.onUpdatePreview,
         'rotateFigure': self.onRotateFigure,
         'zoomFigure': self.onZoomFigure,
         'getFashionDesc': self.onGetFashionDesc,
         'getRankData': self.onGetRankData,
         'enableRank': self.onEnableRank,
         'openEvaluate': self.onOpenEvaluate}
        self.mediator = None
        self.dataCache = None
        self.categories = None
        self.firstCateItems = None
        self.fittingModel = None
        self.rankCache = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUI_BAO_GE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUI_BAO_GE:
            self.mediator = mediator
            self.fittingModel = fittingModel.FittingModel('GuiBaoGePhotoGen', 477, None, self)
            self.fittingModel.initHeadGeen()
            self.fittingModel.restorePhoto3D()
            return uiUtils.array2GfxAarry(self._genCategories(), True)
        else:
            return

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUI_BAO_GE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUI_BAO_GE)
        if self.fittingModel:
            self.fittingModel.resetHeadGen()
        self.fittingModel = None

    def clearData(self):
        self.dataCache = None
        self.categories = None
        self.firstCateItems = None

    def onGetGuiBaoData(self, *arg):
        category = int(arg[3][0].GetNumber())
        subCate = int(arg[3][1].GetNumber())
        if self.dataCache == None:
            self.initGuibaoData()
        data = self._genCategoryData(category, subCate)
        return uiUtils.dict2GfxDict(data, True)

    def _genCategoryData(self, category, subCate):
        categoryData = self.dataCache.get(category, {})
        subData = categoryData.get(subCate, {})
        configData = GBGD.data
        p = BigWorld.player()
        data = {}
        data['items'] = []
        totalCount = 0
        ownCount = 0
        for thirdCate in sorted(subData.keys(), reverse=True):
            obj = {}
            obj['items'] = []
            obj['cateName'] = GBDCD.data.get('guibaoThirdCates', {}).get(thirdCate, gameStrings.TEXT_GUIBAOGEPROXY_99 % thirdCate)
            items = subData[thirdCate]
            totalCount += len(items)
            for itemId in items:
                owned = False
                associateIds = list(configData.get(itemId, {}).get('associateIds', []))
                if itemId not in associateIds:
                    associateIds.append(itemId)
                for associateId in associateIds:
                    if associateId in getattr(BigWorld.player(), 'appearanceItemCollectSet', set([])):
                        owned = True
                        ownCount += 1
                        break

                state = 1 if owned else 5
                idx = configData.get(itemId, {}).get('idx', 0)
                canEvaluate = p.getCanEvaluateItem(itemId) and p.lv >= const.EVALUATE_LIMIT_OF_PART_LV
                obj['items'].append(uiUtils.getGfxItemById(itemId, appendInfo={'state': state,
                 'idx': idx,
                 'canEvaluate': canEvaluate}, srcType='guibaoge'))

            obj['items'].sort(key=lambda k: k['idx'], reverse=True)
            data['items'].append(obj)

        data['count'] = '%d/%d' % (ownCount, totalCount)
        return data

    def initGuibaoData(self):
        data = GBGD.data
        self.dataCache = {}
        self.categories = {}
        self.firstCateItems = {}
        for itemId in data:
            itemObj = data[itemId]
            category = itemObj.get('category', 0)
            subCate = itemObj.get('subCate', [])
            thirdCate = itemObj.get('thirdCate', [])
            if not self.dataCache.has_key(category):
                self.dataCache[category] = {}
            if not self.categories.has_key(category):
                self.categories[category] = []
            if not self.firstCateItems.has_key(category):
                self.firstCateItems[category] = []
            for index in xrange(len(subCate)):
                subCateId = subCate[index]
                if index < len(thirdCate):
                    thirdCateId = thirdCate[index]
                    if not self.dataCache[category].has_key(subCateId):
                        self.dataCache[category][subCateId] = {}
                    if not self.dataCache[category][subCateId].has_key(thirdCateId):
                        self.dataCache[category][subCateId][thirdCateId] = []
                    if subCateId not in self.categories[category]:
                        self.categories[category].append(subCateId)
                    if self._checkItemMatch(itemId):
                        self.dataCache[category][subCateId][thirdCateId].append(itemId)
                        if itemId not in self.firstCateItems[category]:
                            self.firstCateItems[category].append(itemId)

    def _checkItemMatch(self, itemId):
        p = BigWorld.player()
        physique = getattr(p, 'physique', None)
        sex = getattr(physique, 'sex', -1)
        school = getattr(p, 'realSchool', const.SCHOOL_DEFAULT)
        bodyType = getattr(physique, 'bodyType', -1)
        sexReq = ID.data.get(itemId, {}).get('sexReq', 0)
        if sexReq > 0 and sex != sexReq:
            return False
        elif not utils.inAllowBodyType(itemId, bodyType, ID):
            return False
        schReq = ID.data.get(itemId, {}).get('schReq', 0)
        if schReq != 0 and school not in schReq:
            return False
        else:
            return True

    def _genCategories(self):
        if self.categories == None:
            self.initGuibaoData()
        categories = []
        for category in sorted(self.categories.keys()):
            obj = {}
            obj['categoryId'] = category
            obj['categoryName'] = GBDCD.data.get('guibaogeCategories', {}).get(category, gameStrings.TEXT_GUIBAOGEPROXY_193 % category)
            obj['subCates'] = []
            subCates = self.categories[category]
            subCates.sort()
            for subCate in subCates:
                obj['subCates'].append({'subCateId': subCate,
                 'subCateName': GBDCD.data.get('guibaogeSubCates', {}).get(subCate, gameStrings.TEXT_GUIBAOGEPROXY_198 % subCate)})

            categories.append(obj)

        return categories

    def onGetGuiBaoDetailInfo(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        configData = GBGD.data.get(itemId, {})
        itemData = {}
        itemData['slotData'] = uiUtils.getGfxItemById(itemId)
        itemData['slotName'] = uiUtils.getItemColorName(itemId)
        itemData['getWay'] = self.ganreteeGetWay(configData.get('getway', []))
        itemData['score'] = configData.get('score', 0)
        itemData['historyDesc'] = ID.data.get(itemId, {}).get('historyDesc', '')
        p = BigWorld.player()
        itemData['canEvaluate'] = p.getCanEvaluateItem(itemId) and p.lv >= const.EVALUATE_LIMIT_OF_PART_LV
        self.setLoadingMcVisible(False)
        item = Item(itemId)
        if self.fittingModel:
            self.fittingModel.addItem(item)
        return uiUtils.dict2GfxDict(itemData, True)

    def ganreteeGetWay(self, ways):
        getStr = ''
        for idx in ways:
            getStr += GBDCD.data.get('getway', {}).get(idx, '') + '\n'

        return getStr

    def onGetJishiInfo(self, *arg):
        if self.firstCateItems == None:
            self.initGuibaoData()
        p = BigWorld.player()
        ret = {}
        ret['totalView'] = []
        for categoryId in self.firstCateItems:
            items = self.firstCateItems[categoryId]
            ownCount = 0
            totalCount = len(items)
            for itemsId in items:
                associateIds = GBGD.data.get(itemsId, {}).get('associateIds', [])
                associateIds = list(associateIds)
                if itemsId not in associateIds:
                    associateIds.append(itemsId)
                for associateId in associateIds:
                    if associateId in getattr(p, 'appearanceItemCollectSet', set([])):
                        ownCount += 1
                        break

            cateName = GBDCD.data.get('guibaogeCategories', {}).get(categoryId, gameStrings.TEXT_GUIBAOGEPROXY_193 % categoryId)
            ret['totalView'].append({'cateName': cateName,
             'count': '%d/%d' % (ownCount, totalCount)})

        ret['totalFame'] = GBDCD.data.get('guibaogeTotalScore', gameStrings.TEXT_GUIBAOGEPROXY_254) % getattr(p, 'appearanceItemCollectPoint', 0)
        ret['avaliableFame'] = GBDCD.data.get('guibaogeCurrentScore', gameStrings.TEXT_GUIBAOGEPROXY_255) % p.fame.get(const.APPERANCE_ITEM_COLLECT_FAME_ID, 0)
        seekId = GBDCD.data.get('guibaogeNpcId', 110155853)
        ret['seekId'] = seekId
        npcId = SEEKD.data.get(seekId, {}).get('npcId', 0)
        if npcId == 0:
            ret['npcName'] = gameStrings.TEXT_GUIBAOGEPROXY_261 % SEEKD.data.get(seekId, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        else:
            ret['npcName'] = gameStrings.TEXT_GUIBAOGEPROXY_261 % ND.data.get(npcId, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        return uiUtils.dict2GfxDict(ret, True)

    def refreshView(self):
        if self.mediator:
            self.mediator.Invoke('refreshView')

    def onOpenAchievePanel(self, *arg):
        gameglobal.rds.ui.achvment.show()

    def onGuibaoFindPath(self, *arg):
        pathStr = arg[3][0].GetString()
        uiUtils.findPosById(pathStr)

    def setLoadingMcVisible(self, value):
        if self.mediator:
            self.mediator.Invoke('setLoadingMcVisible', GfxValue(value))

    def onResetPreview(self, *arg):
        if self.fittingModel:
            self.fittingModel.restorePhoto3D()
            headGen = self.fittingModel.headGen
            if headGen:
                headGen.resetYaw()

    def onUpdatePreview(self, *arg):
        if self.fittingModel:
            self.fittingModel.showItem()

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onZoomFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.zoom(deltaZoom)

    def onGetFashionDesc(self, *arg):
        if self.fittingModel:
            desc = self.uiAdapter.fittingRoom.getFashionDesc(self.fittingModel.item)
            return GfxValue(gbk2unicode(desc))

    def onGetRankData(self, *arg):
        BigWorld.player().base.queryFriendACRank()
        return uiUtils.array2GfxAarry(self._genRankData(self.rankCache), True)

    def refreshRankView(self, data):
        self.rankCache = data
        if self.mediator:
            self.mediator.Invoke('updateRankView', uiUtils.array2GfxAarry(self._genRankData(self.rankCache), True))

    def _genRankData(self, data):
        ret = []
        gbId = BigWorld.player().gbId
        for i in xrange(len(data)):
            obj = {}
            obj['rank'] = i + 1
            obj['playerName'] = data[i][0]
            obj['school'] = SD.data.get(data[i][1], {}).get('name', gameStrings.TEXT_GAME_1747)
            obj['score'] = data[i][2]
            obj['isSelf'] = gbId == data[i][3]
            ret.append(obj)

        return ret

    def onEnableRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableAppearanceRank', False))

    def onOpenEvaluate(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.evaluatePlay.show(itemId, uiConst.EVALUATE_SHOWTYPE_ITEM)

    def refreshPreviewInfo(self):
        if self.mediator:
            self.mediator.Invoke('refreshPreview')

    def refreshAllSlot(self):
        if self.mediator:
            self.mediator.Invoke('refreshAllSlot')
