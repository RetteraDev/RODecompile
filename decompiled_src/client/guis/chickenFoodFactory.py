#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodFactory.o
import copy
import BigWorld
import gamelog
import formula
import gameglobal
import gametypes
import uiConst
import const
import gamelog
import utils
import uiUtils
import clientUtils
from gameStrings import gameStrings
from gameclass import Singleton
from data import bonus_history_check_data as BHCD
from data import sys_config_data as SCD
from data import skill_general_data as SGD
from cdata import chicken_meal_custom_variables_data as CMCVD
from cdata import chicken_meal_quality_material_info_data as CMQMID
COLOR_VALUE_DICT = {1: '#ffffe5',
 2: '#73e539',
 3: '#8dc6ff',
 4: '#ca7fff',
 5: '#ffcc31',
 6: '#ff7f00'}

def getInstance():
    return ChickenFoodFactory.getInstance()


class ChickenFoodFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.initData()
        self.resetData()

    def resetData(self):
        self.varsDic = {}
        self.curFoodInfo = {}
        self.isWaiting = True
        self.curStage = 0
        self.useSkillResult = {}
        self.completeFoodResult = {}
        self.cancelWaitingCallBack()
        self.waitingNum = -1

    def setVars(self, data):
        self.varsDic.update(data)
        self.dealInfo(data)

    def initData(self):
        self.isOver = True
        self.waitingCallBack = None
        self.waitingNum = -1
        self.waitRankShow = False
        self.topRankData = {}
        self.foodInfo = {}
        self.skillResult = {}
        self.foodResult = {}
        self.chickenFoodData = {}
        self.material_key = ('material_chicken', 'material_spices', 'material_onion', 'material_chili', 'material_bean', 'material_oil')
        self.shilianSkillState = None
        self.freeState = None
        for k, v in CMCVD.data.iteritems():
            self.foodInfo[v.get('foodInfo')] = k
            self.skillResult[v.get('useSkillForFoodResult')] = k
            self.foodResult[v.get('foodResult')] = k

        for k, v in CMQMID.data.iteritems():
            for _k, _v in v.iteritems():
                _v['quality'] = k
                self.chickenFoodData[_k] = _v

    def dealInfo(self, data):
        materialChange = False
        for k, v in data.iteritems():
            if k in self.foodInfo:
                gamelog.debug('@zq deal foodInfo', self.foodInfo[k], v)
                if self.foodInfo[k] < self.curFoodInfo.get('foodStage', 0):
                    continue
                self.isWaiting = False
                self.curFoodInfo['foodInfo'] = v
                self.curFoodInfo['foodStage'] = self.foodInfo[k]
                self.curStage = self.foodInfo[k]
                self.calcScoreBarInfo()
                self.calcStarNum()
                gameglobal.rds.ui.chickenFoodAppearance.show(self.foodInfo[k], v)
            if k in self.skillResult:
                gamelog.debug('@zq deal skillResult', self.skillResult[k], v)
                self.curFoodInfo['skillResult'] = v
                self.useSkillResult[k] = v
                gameglobal.rds.ui.actionbar.updateSlots()
                self.updateWaiting()
            if k in self.foodResult:
                gamelog.debug('@zq deal foodResult', self.foodResult[k], v)
                self.completeFoodResult[k] = v
                if self.foodResult[k] == self.curStage and self.isWaiting == False:
                    self.isWaiting = True
                    self.updateWaiting()
                    otherInfo = self.genResultInfo(v)
                    gameglobal.rds.ui.chickenFoodShow.show(self.foodResult[k], self.curFoodInfo['foodInfo'], otherInfo)
                    self.curFoodInfo = {}
            if k in self.material_key:
                gamelog.debug('@zq deal material_key', k, v)
                self.curFoodInfo[k] = v
                materialChange = True
            if k == 'bfy_stage':
                gamelog.debug('@zq deal bfy_stage', k, v)
                if v < self.curStage:
                    continue
                self.curStage = v
            if k == const.CHICKEN_MEAL_ALL_RESULT_INFO:
                gamelog.debug('@zq deal CHICKEN_MEAL_ALL_RESULT_INFO', k, v)
                self.isOver = True
                gameglobal.rds.ui.chickenFoodBalance.show(v)
                self.resetData()
            if k == const.CHICKEN_MEAL_JINENG_SHILIAN:
                gamelog.debug('@zq deal CHICKEN_MEAL_JINENG_SHILIAN', k, v)
                self.shilianSkillState = v
                gameglobal.rds.ui.actionbar.updateSlots()
            if k == const.CHICKEN_MEAL_FREE_STATE:
                gamelog.debug('@zq deal CHICKEN_MEAL_FREE_STATE', k, v)
                self.freeState = v
                gameglobal.rds.ui.actionbar.updateSlots()

        if materialChange:
            self.calcStarNum()
            gameglobal.rds.ui.actionbar.updateSlots()
        self.refreshCookingUI()

    def genResultInfo(self, foodResult):
        barInfo = self.getCurBarInfo()
        _info = {'foodResult': foodResult,
         'barInfo': barInfo}
        return _info

    def getFoodDetailInfoById(self, _id):
        return copy.deepcopy(self.chickenFoodData.get(_id, {}))

    def getCurFoodInfo(self):
        return copy.deepcopy(self.curFoodInfo)

    def getCurFoodDetail(self):
        foodId, quality, lessValue, excessValue = self.hasCurBaseInfo()
        if not (foodId and quality and lessValue and excessValue):
            return None
        else:
            detailInfo = self.getFoodDetailInfoById(foodId)
            return detailInfo

    def hasCurBaseInfo(self):
        foodId, quality, lessValue, excessValue = self.curFoodInfo.get('foodInfo', (0, 0, 0, 0))
        return (foodId,
         quality,
         lessValue,
         excessValue)

    def pushCookingUI(self):
        p = BigWorld.player()
        isOnZaijuOrBianyao = p._isOnZaijuOrBianyao()
        if self.isOver:
            self.closeAllUI(True)
        bfyZaijuNo = SCD.data.get('bfyZaijuNo', ())
        if isOnZaijuOrBianyao and p._getZaijuOrBianyaoNo() in bfyZaijuNo:
            gameglobal.rds.ui.chickenFoodOther.hide()
            if not self.isOver:
                gameglobal.rds.ui.chickenFoodMain.show()
            return gameglobal.rds.ui.chickenFoodMain
        else:
            gameglobal.rds.ui.chickenFoodMain.hide()
            if not self.isOver:
                gameglobal.rds.ui.chickenFoodOther.show()
            return gameglobal.rds.ui.chickenFoodOther

    def calcScoreBarInfo(self):
        foodId, quality, lessValue, excessValue = self.hasCurBaseInfo()
        if not (foodId and quality and lessValue and excessValue):
            return
        detailInfo = self.getFoodDetailInfoById(foodId)
        material = detailInfo.get('material', (0, 0, 0, 0, 0, 0))
        for i, mNum in enumerate(material):
            x = int(mNum * lessValue)
            y = mNum - x
            z = int(mNum * excessValue)
            barInfo = [x, y, z]
            self.curFoodInfo[''.join((self.material_key[i], 'Bar'))] = barInfo

    def calcStarNum(self):
        foodId, quality, lessValue, excessValue = self.hasCurBaseInfo()
        if not (foodId and quality and lessValue and excessValue):
            return
        baseScore = self.getCurBaseScore()
        socreNum = baseScore
        detailInfo = self.getFoodDetailInfoById(foodId)
        maxScore = detailInfo.get('maxScore', 0)
        jInfo = SCD.data.get('foodJudgmentInfo', ())
        starNum = 0
        if len(jInfo) == 4:
            p1, p2, p3, p4 = jInfo
            if socreNum < maxScore * p1:
                starNum = 1
            elif socreNum < maxScore * p2:
                starNum = 2
            elif socreNum < maxScore * p3:
                starNum = 3
            elif socreNum < maxScore * p4:
                starNum = 4
            else:
                starNum = 5
        else:
            starNum = 1
        self.curFoodInfo['starNum'] = starNum

    def getCurBaseScore(self):
        foodId, quality, lessValue, excessValue = self.hasCurBaseInfo()
        if not (foodId and quality and lessValue and excessValue):
            return 0
        detailInfo = self.getFoodDetailInfoById(foodId)
        deduct = detailInfo.get('deduct', 0)
        maxScore = detailInfo.get('maxScore', 0)
        socreNum = 0
        for key in self.material_key:
            mNum = self.curFoodInfo.get(key, 0)
            barInfo = self.curFoodInfo[''.join((key, 'Bar'))]
            x, y, z = barInfo
            socreNum += mNum
            if mNum > x + y:
                socreNum -= (mNum - (x + y)) * deduct

        return socreNum

    def getCurExScore(self):
        totalExtraScore = 0
        for k, v in self.useSkillResult.iteritems():
            _no = self.skillResult.get(k, 0)
            if _no and _no == self.curStage:
                for _k, _v in v.iteritems():
                    _data = SCD.data.get('finishFoodSkillsCondition', {})
                    _result, uTime = _v
                    if _result:
                        exScore = _data.get(_k, {}).get('addExtraScore', 0)
                        totalExtraScore += exScore

        return totalExtraScore

    def getCurFoodStarNum(self):
        return self.curFoodInfo.get('starNum', 0)

    def refreshCookingUI(self):
        p = BigWorld.player()
        if p.mapID == const.FB_NO_SPRING_ACTIVITY and not self.isOver:
            cProxy = self.pushCookingUI()
            cProxy.refreshInfo()
        else:
            self.closeAllUI(True)

    def closeAllUI(self, hasBalance = False):
        gameglobal.rds.ui.chickenFoodOther.hide()
        gameglobal.rds.ui.chickenFoodMain.hide()
        gameglobal.rds.ui.chickenFoodAppearance.hide()
        gameglobal.rds.ui.chickenFoodSubmit.hide()
        gameglobal.rds.ui.chickenFoodRank.hide()
        if not hasBalance:
            gameglobal.rds.ui.chickenFoodBalance.hide()
        self.resetData()

    def getFoodNoStr(self):
        foodNo = self.curStage
        if foodNo and len(gameStrings.CHICKENFOOD_FOODNO) > foodNo:
            _str = gameStrings.CHICKENFOOD_FOODNO_STR % gameStrings.CHICKENFOOD_FOODNO[foodNo]
            return _str
        else:
            return ''

    def getStarNumMax(self):
        return 5

    def getHisSore(self):
        totalScore = 0
        totalExtraScore = 0
        for k, v in self.completeFoodResult.iteritems():
            result, star, score, uTime = v
            totalScore += score

        return (totalScore, totalExtraScore)

    def getScoreStr(self):
        baseScore, exScore = self.getHisSore()
        if exScore > 0:
            _str = gameStrings.CHICKENFOOD_EXSCORE_STR
            _str = _str % (baseScore, exScore)
            return _str
        else:
            _str = gameStrings.CHICKENFOOD_SCORE_STR % baseScore
            return _str

    def getCurBarInfo(self):
        barInfo = []
        for i, v in enumerate(self.material_key):
            curValue = self.curFoodInfo.get(v, 0)
            x, y, z = self.curFoodInfo.get(''.join((v, 'Bar')), (0, 0, 0))
            maxValue = x + y + z
            _info = {'name': gameStrings.CHICKENFOOD_MATERIAL_STR[i],
             'curValue': curValue,
             'x': x,
             'y': y,
             'z': z,
             'maxValue': maxValue}
            barInfo.append(_info)

        return barInfo

    def transFoodName(self, name, quality):
        colorValue = uiUtils.getColorValueByQuality(quality)
        colorValue = COLOR_VALUE_DICT.get(quality, '')
        if colorValue:
            return uiUtils.toHtml(name, colorValue)
        else:
            return name

    def getSkillState(self, skillId):
        p = BigWorld.player()
        _data = SCD.data.get('finishFoodSkillsCondition', {})
        canUse = True
        isLight = False
        _type = 0
        remain = 0
        total = 0
        for k, v in _data.iteritems():
            if skillId == k:
                remain, total = self.calcSkillCoolDownTime(skillId, k, v)
                _type = v.get('type', 0)
                if _type == const.BAI_FENG_YAN_JINENG_CHUGUO:
                    for i, v in enumerate(self.material_key):
                        curValue = self.curFoodInfo.get(v, 0)
                        x, y, z = self.curFoodInfo.get(''.join((v, 'Bar')), (0, 0, 0))
                        if curValue < x or 0 in (x, y, z):
                            canUse = False

                    isLight = canUse
                elif _type == const.BAI_FENG_YAN_JINENG_ZHENGJIU:
                    needLifeSkillId, needLifeSkillLv = v.get('needLifeSkill', (0, 0))
                    if p.lifeSkill.get(needLifeSkillId, {}).get('level', 0) < needLifeSkillLv:
                        canUse = False
                    if canUse:
                        isExcess = False
                        for i, v in enumerate(self.material_key):
                            curValue = self.curFoodInfo.get(v, 0)
                            x, y, z = self.curFoodInfo.get(''.join((v, 'Bar')), (0, 0, 0))
                            if curValue > x + y:
                                isExcess = True
                                break

                        if not isExcess:
                            canUse = False
                elif _type == const.BAI_FENG_YAN_JINENG_SHILIAN:
                    needLifeSkillId, needLifeSkillLv = v.get('needLifeSkill', (0, 0))
                    if p.lifeSkill.get(needLifeSkillId, {}).get('level', 0) < needLifeSkillLv:
                        canUse = False
                    if self.shilianSkillState != gametypes.BAI_FENG_YAN_SHILIAN_STATE_CAN_USE:
                        canUse = False
                    if not self.freeState:
                        canUse = False

        return (isLight,
         canUse,
         _type,
         remain,
         total)

    def calcSkillCoolDownTime(self, skillId, k, v):
        total = 0
        remain = 0
        total = SGD.data.get((skillId, 1), {}).get('cd', 0)
        for _k, _v in self.useSkillResult.iteritems():
            _no = self.skillResult.get(_k, 0)
            if _no:
                for __k, __v in _v.iteritems():
                    if __k == skillId:
                        result, uTime = __v
                        diff = utils.getNow() - uTime
                        if diff >= 0 and diff <= total:
                            remain = total - diff

        return (remain, total)

    def setTopRankData(self, _data, _type):
        if _type == 1:
            self.topRankData['top'] = _data
        elif _type == 2:
            self.topRankData['myself'] = _data
        if not gameglobal.rds.ui.chickenFoodRank.widget and self.waitRankShow:
            gameglobal.rds.ui.chickenFoodRank.show()
            self.waitRankShow = False
        if gameglobal.rds.ui.chickenFoodRank.widget:
            gameglobal.rds.ui.chickenFoodRank.refreshInfo()

    def getTopRankData(self):
        return self.topRankData

    def showRank(self, isShow = False):
        self.waitRankShow = isShow
        p = BigWorld.player()
        p.base.getTopChickenMealScore(0)
        foodNum, bid = SCD.data.get('chickenBaseReward', ())
        group = BHCD.data.get(bid, {}).get('group', 0)
        p.cell.queryBonusHistory(group)

    def getChickenIcon(self, _type, _id):
        if _type == uiConst.ICON_SIZE40:
            return 'item/icon/%d.dds' % _id
        elif _type == uiConst.ICON_SIZE64:
            return 'item/icon64/%d.dds' % _id
        elif _type == uiConst.ICON_SIZE110:
            return 'item/icon110/%d.dds' % _id
        else:
            return None

    def cancelWaitingCallBack(self):
        if self.waitingCallBack:
            BigWorld.cancelCallback(self.waitingCallBack)
            self.waitingCallBack = None

    def setWaitingTimer(self, waitingTime):
        self.cancelWaitingCallBack()
        self.waitingNum = waitingTime
        self.waitingCallBack = BigWorld.callback(1, self.updateWaiting)

    def updateWaiting(self):
        if self.isWaiting:
            self.refreshCookingUI()
            if not self.waitingNum < 0:
                self.waitingNum -= 1
                self.waitingCallBack = BigWorld.callback(1, self.updateWaiting)
            else:
                self.cancelWaitingCallBack()
            if self.waitingNum < 0:
                self.waitingNum = -1
        else:
            self.cancelWaitingCallBack()

    def calcWaitingTime(self):
        remain = 0
        skillId = 9421
        waitingConst = 30
        waitTime = -1
        if not self.isOver:
            for _k, _v in self.useSkillResult.iteritems():
                _no = self.skillResult.get(_k, 0)
                if _no:
                    for __k, __v in _v.iteritems():
                        if __k == skillId:
                            result, uTime = __v
                            if result:
                                diff = utils.getNow() - uTime
                                if diff >= 0:
                                    remain = waitingConst - diff
                                    if remain >= 0:
                                        if waitTime == -1:
                                            waitTime = remain
                                        if remain < waitTime:
                                            waitTime = remain

        return waitTime

    def enterBFY(self):
        gamelog.debug('@zq enterBFY')
        self.isOver = False
        self.pushCookingUI()
        gameglobal.rds.ui.chickenFoodGuide.show()
