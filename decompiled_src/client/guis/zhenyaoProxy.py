#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhenyaoProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
import const
import utils
import formula
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from ui import unicode2gbk
from helpers import capturePhoto
from data import sys_config_data as SCD
from data import zhenyao_monster_config_data as ZMCD
from data import activity_basic_data as ABD
from data import fb_data as FD
ZHENYAO_ACITIVITY_ID = 10248

class ZhenyaoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZhenyaoProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankData': self.onGetRankData,
         'getFbResult': self.onGetFbResult,
         'getActivityDesc': self.onGetActivityDesc,
         'getProgressData': self.onGetProgressData,
         'closeActivityDesc': self.onCloseActivityDesc,
         'openActitivyDesc': self.onOpenActitivyDesc,
         'openRankReward': self.onOpenRankReward,
         'closeFbResult': self.onCloseFbResult,
         'closeRankList': self.onCloseRankList,
         'getProgressCountDown': self.onGetProgressCountDown,
         'openTeamDetail': self.onOpenTeamDetail,
         'openRankList': self.onOpenRankList}
        self.rankMed = None
        self.progressMed = None
        self.resultMed = None
        self.descMed = None
        self.rankCacheData = {}
        self.fbResult = {}
        self.progressCache = []
        self.selectedLvKey = 0
        self.fubenData = {'zy_level': 0,
         'hdn_num': 0,
         'punish_times': 0,
         'c_start_time': 0,
         'is_fb_finish': 1}
        self.myResultRank = 0
        self.headGen = None
        self.myRank = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHENYAO_DESC, self.closeActivityPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHENYAO_RANK, self.closeRankList)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZHENYAO_DESC:
            self.descMed = mediator
            return GfxValue(gbk2unicode(self._getZhenYaoActivityDesc()))
        if widgetId == uiConst.WIDGET_ZHENYAO_PROGRESS:
            self.progressMed = mediator
            ret = self._genProgressData(self.progressCache, 0)
            return uiUtils.dict2GfxDict(ret, True)
        if widgetId == uiConst.WIDGET_ZHENYAO_FB_RESULT:
            self.resultMed = mediator
            self.initHeadGen()
            self.takePhoto3D()
        if widgetId == uiConst.WIDGET_ZHENYAO_RANK:
            self.rankMed = mediator

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_ZHENYAO_DESC:
            self.closeActivityPanel()
        if widgetId == uiConst.WIDGET_ZHENYAO_PROGRESS:
            self.closeProgressPanel()
        if widgetId == uiConst.WIDGET_ZHENYAO_FB_RESULT:
            self.closeFbResult()
        if widgetId == uiConst.WIDGET_ZHENYAO_RANK:
            self.closeRankList()

    def showRankList(self):
        if not gameglobal.rds.configData.get('enableZhenyaoActivity', False):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHENYAO_RANK)

    def closeRankList(self):
        self.rankMed = None
        self.myRank = 0
        self.myResultRank = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHENYAO_RANK)
        gameglobal.rds.ui.funcNpc.close()

    def onCloseRankList(self, *arg):
        self.closeRankList()

    def onGetRankData(self, *arg):
        lvKey = int(arg[3][0].GetNumber())
        if lvKey == 0:
            lvKey = self._getPlayerLvStr()
        self.lvInterval = self.fromLvKey2LvInterval(lvKey)
        if self.rankCacheData.has_key(lvKey):
            self.updateRankData(self.rankCacheData[lvKey], lvKey)
        else:
            self.updateRankInitData(lvKey)
        p = BigWorld.player()
        p.base.reqZhenyaoFinalRank(lvKey)
        p.base.reqZhenyaoMatchFinalGbIdRank()

    def updateSelfRank(self, rank):
        self.myRank = rank
        if self.rankMed:
            self.rankMed.Invoke('updateRank', GfxValue(self.myRank))

    def updateRankData(self, data, lvKey):
        if not self.rankCacheData.has_key(lvKey):
            self.rankCacheData[lvKey] = []
        self.rankCacheData[lvKey] = data
        self.selectedLvKey = lvKey
        self.refreshRankData(data)

    def refreshRankData(self, data):
        ret = self._genRankData(data)
        if self.rankMed:
            self.rankMed.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))

    def _genRankData(self, data):
        ret = {}
        ret['myRank'] = self.myRank
        ret['list'] = []
        ret['lvKey'] = self.selectedLvKey
        for i in xrange(len(data)):
            temp = data[i]
            obj = {}
            obj['rank'] = i + 1
            obj['teamName'] = temp.group.groupName
            obj['time'] = utils.formatTimeStr(temp.scoreInfo.interval, 'h:m:s', True, 2, 2, 2)
            obj['score'] = temp.scoreInfo.score
            obj['id'] = temp.groupNUID
            uuidStr = '%d' % temp.groupNUID
            gameglobal.rds.ui.ranking.saveTeamUuid(uuidStr, temp.groupNUID)
            ret['list'].append(obj)

        return ret

    def _getPlayerLvStr(self):
        p = BigWorld.player()
        if 1 <= p.lv <= 59:
            return 1
        if 60 <= p.lv <= 69:
            return 2
        if 70 <= p.lv <= 89:
            return 3
        return 1

    def onOpenRankReward(self, *arg):
        if not gameglobal.rds.configData.get('enableZhenyaoActivity', False):
            return
        gameglobal.rds.ui.ranking.openRewardPanel(const.PROXY_KEY_GROUP_ZHENYAO_RANK, uiConst.ZHENYAO_FUBEN_ID, self.lvInterval)

    def onOpenTeamDetail(self, *arg):
        uuid = arg[3][0].GetString()
        teamName = unicode2gbk(arg[3][1].GetString())
        gameglobal.rds.ui.ranking.openTeamDetail(0, uuid, teamName, fromRank=uiConst.GROUP_FUBEN_DETAIL_ZHENYAO)

    def showFbResult(self):
        if not gameglobal.rds.configData.get('enableZhenyaoActivity', False):
            return
        p = BigWorld.player()
        if self.fbResult and self.myResultRank and p.inFuben():
            if self.progressMed:
                self.progressMed.Invoke('stopCountDown')
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHENYAO_FB_RESULT)

    def closeFbResult(self):
        self.resultMed = None
        self.myResultRank = 0
        self.fbResult = {}
        self.resetHeadGen()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHENYAO_FB_RESULT)

    def onGetFbResult(self, *arg):
        ret = {}
        ret['timeCost'] = utils.formatTimeStr(self.fbResult.get('duration', 0), 'h:m:s', True, 2, 2, 2)
        ret['score'] = self.fbResult.get('score', 0)
        ret['rank'] = self.myResultRank
        ret['evaluate'] = self.getEvaluateDesc(ret['score'])
        list = self._genFbResultData(self.fbResult.get('bossDetailList', {}))
        ret['hideList'] = list[1]
        ret['showlist'] = list[0]
        ret['currentLevel'] = self.fubenData['zy_level']
        ret['hidetLevel'] = self.fubenData['hdn_num']
        ret['punishLevel'] = self.fubenData['punish_times']
        return uiUtils.dict2GfxDict(ret, True)

    def setResultDetail(self, detail):
        self.fbResult = detail
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo == const.FB_NO_QINGLINZHENYAO_YUESAI:
            p.base.reqZhenyaoMatchFinalGbIdRank()

    def setResultRank(self, rank):
        self.myResultRank = rank

    def getEvaluateDesc(self, socre):
        ret = ''
        for key in SCD.data.get('ZHENYAO_EVALUATE_LEVEL', const.ZHENYAO_EVALUATE_LEVEL):
            if socre > key[0]:
                ret = key[1]

        return ret

    def _genFbResultData(self, data):
        retShow = []
        retHide = []
        showCnt = 1
        hideCnt = 11
        for key in data:
            temp = data[key]
            obj = {}
            obj['score'] = temp[2]
            obj['timeCost'] = utils.formatTimeStr(temp[1], 'h:m:s', True, 2, 2, 2)
            obj['isKo'] = temp[0]
            if obj['isKo']:
                obj['icon'] = 'fubenResultPic/%d.dds' % ZMCD.data.get(key, {}).get('icon', 0)
                addTips = "%s      <font color = \'#146622\'>%s</font>" % (ZMCD.data.get(key, {}).get('name', ''), gameStrings.TEXT_ZHENYAOPROXY_238)
            else:
                obj['icon'] = 'fubenResultPic/%d.dds' % ZMCD.data.get(key, {}).get('grayIcon', 0)
                addTips = "%s      <font color = \'#be0a0a\'>%s</font>" % (ZMCD.data.get(key, {}).get('name', ''), gameStrings.TEXT_ZHENYAOPROXY_241)
            obj['title'] = addTips
            if ZMCD.data.get(key, {}).get('isHidden', ''):
                if ZMCD.data.get(key, {}).get('order', 0) == hideCnt:
                    retHide.append(obj)
                    hideCnt += 1
            elif ZMCD.data.get(key, {}).get('order', 0) == showCnt:
                retShow.append(obj)
                showCnt += 1

        return (retShow, retHide)

    def onCloseFbResult(self, *arg):
        self.closeFbResult()

    def onOpenRankList(self, *arg):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo == const.FB_NO_QINGLINZHENYAO_YUESAI:
            self.showRankList()
        elif fbNo == const.FB_NO_QINGLINZHENYAO_PUTONG:
            gameglobal.rds.ui.ranking.show(tabId=2, displayType=uiConst.RANK_TYPE_OTHER, fbNo=fbNo)

    def showActivityPanel(self):
        if not gameglobal.rds.configData.get('enableZhenyaoActivity', False):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHENYAO_DESC)

    def closeActivityPanel(self):
        self.descMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHENYAO_DESC)

    def updateActivityPanel(self):
        pass

    def onGetActivityDesc(self, *arg):
        pass

    def _getZhenYaoActivityDesc(self):
        desc = SCD.data.get('zhenyaoActivityDesc', '')
        return desc

    def onCloseActivityDesc(self, *arg):
        self.closeActivityPanel()

    def showProgressPanel(self):
        p = BigWorld.player()
        activityData = ABD.data.get(ZHENYAO_ACITIVITY_ID, {})
        weekset = activityData.get('weekSet', 0)
        startTimes = activityData.get('startTimes', None)
        endTimes = activityData.get('endTimes', None)
        isActivity = utils.inCrontabRange(startTimes[0], endTimes[0], weekSet=weekset)
        fbNo = formula.getFubenNo(p.spaceNo)
        isUseProgressPanel = FD.data.get(fbNo, {}).get('isUseInTimeRank', 0)
        if gameglobal.rds.configData.get('enableZhenyaoActivity', False) and isActivity and self.fubenData['c_start_time'] and not self.fubenData['is_fb_finish'] and isUseProgressPanel:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHENYAO_PROGRESS)

    def closeProgressPanel(self):
        self.progressMed = None
        self.progressCache = []
        self.fubenData = {'zy_level': 0,
         'hdn_num': 0,
         'punish_times': 0,
         'c_start_time': 0,
         'is_fb_finish': 1}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHENYAO_PROGRESS)

    def updateProgressPanel(self, data = [], mySocre = 0):
        self.progressCache = data
        if self.progressMed:
            ret = self._genProgressData(self.progressCache, mySocre)
            self.progressMed.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))
        else:
            self.showProgressPanel()

    def _getMyTeamInfo(self, myScore):
        ret = {}
        if myScore == 0:
            return ret
        p = BigWorld.player()
        ret['score'] = myScore
        ret['id'] = p.groupNUID
        ret['rank'] = 11
        ret['teamName'] = p.detailInfo['teamName']
        return ret

    def onGetProgressData(self, *arg):
        pass

    def onOpenActitivyDesc(self, *arg):
        if not gameglobal.rds.configData.get('enableZhenyaoActivity', False):
            return
        self.showActivityPanel()

    def _genProgressData(self, data, myScore = 0):
        p = BigWorld.player()
        ret = {}
        arr = []
        myRankData = {}
        for i in xrange(len(data)):
            obj = {}
            temp = data[i]
            obj['id'] = temp.groupNUID
            obj['rank'] = i + 1
            obj['teamName'] = temp.groupName
            obj['score'] = temp.scoreInfo.score
            arr.append(obj)
            if temp.groupNUID == p.groupNUID:
                myRankData = obj

        ret['rankList'] = arr
        if myRankData:
            ret['myTeam'] = myRankData
        else:
            ret['myTeam'] = self._getMyTeamInfo(myScore)
        return ret

    def onGetProgressCountDown(self, *arg):
        endTimes = SCD.data.get('zhenyaoProgressEndTimes', 1800) - (utils.getNow() - self.fubenData['c_start_time'])
        return GfxValue(endTimes)

    def updateRankInitData(self, lvKey):
        if self.rankMed:
            self.rankMed.Invoke('updateRankInitData', GfxValue(lvKey))

    def fromLvKey2LvInterval(self, lvKey):
        if lvKey == 1:
            return (0, 59)
        if lvKey == 2:
            return (60, 69)
        if lvKey == 3:
            return (70, 89)

    def setFbInfo(self, info):
        if info.has_key('zy_level'):
            self.fubenData['zy_level'] = info.get('zy_level')
        if info.has_key('hdn_num'):
            self.fubenData['hdn_num'] = info.get('hdn_num')
        if info.has_key('punish_times'):
            self.fubenData['punish_times'] = info.get('punish_times')
        if info.has_key('c_start_time'):
            self.fubenData['c_start_time'] = info.get('c_start_time')
            self.updateProgressPanel()
        if info.has_key('is_fb_finish'):
            self.fubenData['is_fb_finish'] = info.get('is_fb_finish')
            self.updateProgressPanel()

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.ZhenYaoPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.startCapture(0, None, ('1101',))

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.ZhenYaoPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.initFlashMesh()
