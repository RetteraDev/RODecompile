#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import formula
import const
import uiUtils
import gamelog
import menuManager
from ui import gbk2unicode
from uiProxy import DataProxy
from guis import uiConst
from guis import tipUtils
from guis import messageBoxProxy
from callbackHelper import Functor
from guis import ui
from guis.asObject import ASObject
from guis.asObject import ASUtils
from fubenEvalInfo import FubenEvalInfo
from data import fb_data as FD
from data import item_data as ID
from data import fb_award_data as FAD
from cdata import font_config_data as FCD
from data import fb_guide_data as FGD

class FubenProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(FubenProxy, self).__init__(uiAdapter)
        self.bindType = 'fuben'
        self.modelMap = {'clickFuncItem': self.onClickFuncItem,
         'quitFubenClick': self.onQuitFubenClick,
         'getEvalInfo': self.onGetEvalInfo,
         'nextClick': self.onNextClick,
         'addClick': self.onAddClick,
         'closeFubenReward': self.onCloseFubenReward,
         'timeOut': self.onTimeOut,
         'getRewardInfo': self.onGetRewardInfo,
         'getTooltip': self.onGetTooltip,
         'getRewarded': self.onGetRewarded,
         'getRewardItem': self.onGetRewardItem,
         'getRewardedItem': self.onGetRewardedItem,
         'getTotalResult': self.onGetTotalResult,
         'getFubenTarget': self.onGetFubenTarget,
         'getFubenOneResult': self.onGetFubenOneResult,
         'getHeadTip': self.onGetHeadTip,
         'fubenButtonClick': self.onFubenButtonClick,
         'showStat': self.onShowFbStat,
         'getAllStaticsInfo': self.onGetAllStaticsInfo,
         'getGoalInfo': self.onGetGoalInfo,
         'getGoalAward': self.onGetGoalAward,
         'prevClick': self.onPrevClick,
         'playSound': self.onPlaySound,
         'getFubenQueueInfo': self.onGetFubenQueueInfo,
         'quitFubenQueue': self.onQuitFubenQueue,
         'shareFubenReward': self.onShareFubenReward,
         'enableQRCode': self.onEnableQRCode,
         'ifGotoReward': self.onIfGotoReward}
        self.fubenRewardMed = None
        self.topMediator = None
        self.callbackId = None
        self.reset()

    def setFuncList(self, title, option):
        self.title = title
        self.funcList = option

    def reset(self):
        self.title = None
        self.funcList = None
        self.show = False
        self.evalInfo = None
        self.awardId = tuple()
        self.addCnt = 0
        self.isRewarded = False
        self.fubenResult = {}
        self.fubenTarget = []
        self.fubenOneResult = []
        self.fubenSucc = None
        self.fubenLvl = None
        self.headTip = None
        self.headTipMed = None
        self.fameData = None
        self.gotoReward = False

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.fubenRewardMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_REWARD)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_TARGET)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_ONE_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_TOTAL_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_HEAD_TIP)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_TOP)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_LEFT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_RIGHT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)

    def _registerMediator(self, widgetId, mediator):
        gamelog.debug('@hjx media#FubenProxy:', widgetId)
        if widgetId == uiConst.WIDGET_FUBEN_EVAL:
            self.fubenRewardMed = mediator
            if self.fameData:
                self.setFame(self.fameData)
        elif widgetId == uiConst.WIDGET_FUBEN_HEAD_TIP:
            self.headTipMed = mediator
        elif widgetId == uiConst.WIDGET_FUBEN_EVAL_TOP:
            self.topMediator = mediator
        elif widgetId == uiConst.WIDGET_FUBEN_QUEUE:
            self.fbQueueMediator = mediator

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_FUBEN_EVAL:
            self.fubenRewardMed = None
            self.gotoReward = False
        elif widgetId == uiConst.WIDGET_FUBEN_HEAD_TIP:
            self.headTipMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL)

    def onFubenButtonClick(self, *arg):
        p = BigWorld.player()
        if p.inFuben() and not p.inFubenTypes(const.FB_TYPE_ARENA):
            menuManager.getInstance().leaveFuben()
        elif formula.inPhaseSpace(p.spaceNo):
            uiUtils.exitPhase()

    def onShowFbStat(self, *arg):
        gameglobal.rds.ui.fubenStat.show(None, True)

    def onQuitFubenClick(self, *arg):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo not in FD.data:
            return
        if p.fbAwardMultiple == 0.0:
            self.closeFubenReward()
        else:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.confirmOK)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(self.confirmCancel))]
            self.widgetId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_FUBENPROXY_153, buttons)

    def confirmOK(self):
        self.closeFubenReward()

    def confirmCancel(self):
        pass

    def refreshFubenReward(self):
        if self.isRewarded:
            return
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('refreshPanel')

    def onNextClick(self, *arg):
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('nextPage')
            self.gotoReward = True
        if self.topMediator:
            self.topMediator.Invoke('gotoAward')
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_LEFT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_RIGHT)
        self.cancelCallback()

    def onPrevClick(self, *arg):
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('prevPage')
        if self.topMediator:
            self.topMediator.Invoke('gotoEval')
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_LEFT)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_RIGHT)
        self.cancelCallback()

    def cancelCallback(self):
        if self.callbackId:
            BigWorld.cancelCallback(self.callbackId)
            self.callbackId = None

    def onClickFuncItem(self, *arg):
        idNum = int(arg[3][0].GetNumber())
        if gameglobal.rds.ui.npcPanel.inFullScreen:
            gameglobal.rds.ui.npcPanel.hideNpcFullScreen()
        name, data, idx = self.funcList[idNum]
        BigWorld.entities.get(self.npcId).cell.npcTeleport(data, idx)

    def getValue(self, key):
        if self.funcList == None:
            return
        elif key == 'fuben.funclist':
            ar = self.movie.CreateArray()
            i = 0
            for item in self.funcList:
                ar.SetElement(i, GfxValue(gbk2unicode(item[0])))
                i = i + 1

            return ar
        elif key == 'fuben.title':
            return GfxValue(gbk2unicode(self.title))
        else:
            return

    def showFubenApply(self, npcId):
        if self.show == True:
            self.show = False
            return
        self.show = True
        self.npcId = npcId

    def onGetEvalInfo(self, *arg):
        ret = self.movie.CreateObject()
        ret.SetMember('combat', self.evalInfo.getCombatInfo())
        ret.SetMember('record', self.evalInfo.getRecordInfo())
        ret.SetMember('allStatics', self.evalInfo.getAllStatics())
        ret.SetMember('fubenName', self.evalInfo.getFubenName())
        ret.SetMember('evalName', self.evalInfo.getEvalLevel())
        ret.SetMember('levelScore', self.evalInfo.getLevelScore())
        ret.SetMember('maxEval', self.getEvalMaxVal())
        return ret

    def getEvalMaxVal(self):
        ret = {}
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        ret['maxAtt'] = FD.data.get(fbNo, {}).get('maxAtt', 1000)
        ret['maxdef'] = FD.data.get(fbNo, {}).get('maxdef', 1000)
        ret['maxCom'] = FD.data.get(fbNo, {}).get('maxCom', 1000)
        ret['maxAwd'] = FD.data.get(fbNo, {}).get('maxAwd', 1000)
        return uiUtils.dict2GfxDict(ret)

    def onGetAllStaticsInfo(self, *arg):
        return self.evalInfo.getAllStaticsInfo()

    def showFubenEval(self, evalInfo):
        p = BigWorld.player()
        p.motionPin()
        self.evalInfo = FubenEvalInfo(evalInfo)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_TOP)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_LEFT)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_RIGHT)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL)

    def onCloseFuBenEval(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL)

    def _getAddedRatio(self):
        p = BigWorld.player()
        return '%.2f' % p.fbAwardMultiple

    def _getMaxRatio(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        fData = FAD.data.get((fbNo, p.fbScoreLv), {})
        return fData.get('addMutiple', [p.fbAwardMultiple])[-1]

    def _getAddedMoney(self):
        p = BigWorld.player()
        needCash = FAD.data.get(self.awardId, {}).get('consume', (0,))[0]
        isEnough = 1 if p._canPay(needCash) else 0
        msg = '' if isEnough else gameStrings.TEXT_FUBENPROXY_353
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(needCash))
        ar.SetElement(1, GfxValue(isEnough))
        ar.SetElement(2, GfxValue(gbk2unicode(msg)))
        return ar

    def _createItemInstance(self, index):
        p = BigWorld.player()
        if hasattr(p, 'fbAward'):
            if self.isRewarded:
                item = RewardedItemInfo(p.fbAward[index])
            else:
                item = RewardItemInfo(p.fbAward[index])
        else:
            item = IRewardItemInfo()
        return item

    def _getRewardItem(self):
        ret = self.movie.CreateArray()
        for index in xrange(const.FB_REWARD_COUNT):
            item = self._createItemInstance(index)
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(item.getPath()))
            ar.SetElement(1, GfxValue(item.getAmount()))
            ar.SetElement(2, GfxValue(item.getIconId()))
            ar.SetElement(3, GfxValue(gbk2unicode(item.getIconName())))
            ar.SetElement(4, GfxValue(item.getQualityColor()))
            ar.SetElement(5, GfxValue(item.getIconType()))
            ret.SetElement(index, ar)

        return ret

    def onGetRewardItem(self, *arg):
        return self._getRewardItem()

    def onGetRewardedItem(self, *arg):
        self.isRewarded = True
        return self._getRewardItem()

    def onGetRewardInfo(self, *arg):
        ret = self.movie.CreateObject()
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo not in FD.data:
            gamelog.error('hjx onGetRewardInfo error!', fbNo)
            return
        self.awardId = tuple((fbNo, p.fbScoreLv))
        ret.SetMember('eval', self.evalInfo.getEvalLevel())
        ret.SetMember('ratio', GfxValue(self._getAddedRatio()))
        ret.SetMember('maxRatio', GfxValue(self._getMaxRatio()))
        ret.SetMember('money', self._getAddedMoney())
        ret.SetMember('count', GfxValue(FAD.data.get(self.awardId, {}).get('openCounts', 0)))
        ret.SetMember('timeCount', GfxValue(30))
        return ret

    def onGetHeadTip(self, *arg):
        if self.headTip:
            return GfxValue(self.headTip)

    def _genAddClickMsg(self):
        p = BigWorld.player()
        consume = FAD.data.get(self.awardId, {}).get('consume', ())
        if self.addCnt >= len(consume):
            return (False,
             0,
             gameStrings.TEXT_FUBENPROXY_348,
             p.fbAwardMultiple)
        cash = FAD.data.get(self.awardId, {}).get('consume', ())[self.addCnt]
        isEnable = 1 if p._canPay(cash) else 0
        msg = '' if isEnable else gameStrings.TEXT_FUBENPROXY_353
        return (isEnable,
         cash,
         msg,
         p.fbAwardMultiple)

    def onAddClick(self, *arg):
        self.addCnt += 1
        p = BigWorld.player()
        p.cell.addFbAwardMultiple()

    def addAwardMultiple(self):
        isEnable, cash, msg, ratio = self._genAddClickMsg()
        gamelog.debug('hjx debug fuben#onAddClick:', self.addCnt, isEnable, cash, msg, ratio)
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('setRatio', (GfxValue(isEnable),
             GfxValue(cash),
             GfxValue(gbk2unicode(msg)),
             GfxValue('%.2f' % ratio)))

    def closeFubenReward(self):
        p = BigWorld.player()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_TOP)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_LEFT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_RIGHT)
        self.fubenRewardMed = None
        self.addCnt = 0
        self.isRewarded = False
        p.motionUnpin()

    def onCloseFubenReward(self, *arg):
        self.closeFubenReward()

    def _gainRewarded(self, selectedStr):
        p = BigWorld.player()
        selected = [ int(i) for i in selectedStr.strip(',').split(',') ]
        choice = [ False for i in xrange(const.FB_REWARD_COUNT) ]
        for index in selected:
            choice[index] = True

        p.cell.chooseFbAward(choice)

    def showRewardItem(self):
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('rewardedItem')

    def onTimeOut(self, *arg):
        pass

    def onGetTooltip(self, *arg):
        index = int(arg[3][0].GetString())
        return tipUtils.getItemTipById(index)

    def onGetRewarded(self, *arg):
        selIndex = int(arg[3][0].GetString())
        p = BigWorld.player()
        p.cell.chooseFbAward(selIndex)

    def onGetTotalResult(self, *arg):
        result = self.movie.CreateObject()
        result.SetMember('score', GfxValue(self.fubenResult['score']))
        result.SetMember('oldRank', GfxValue(self.fubenResult['oldRank']))
        result.SetMember('newRank', GfxValue(self.fubenResult['newRank']))
        return result

    def onGetFubenTarget(self, *arg):
        return uiUtils.array2GfxAarry([self.fubenLvl, self.fubenTarget])

    def onGetFubenOneResult(self, *arg):
        return uiUtils.array2GfxAarry([self.fubenLvl, self.fubenOneResult])

    def showFubenTotalResult(self, score, oldRank, newRank):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_TOTAL_RESULT)
        self.fubenResult['score'] = score
        self.fubenResult['oldRank'] = oldRank
        self.fubenResult['newRank'] = newRank
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_TOTAL_RESULT)

    def onGetFubenQueueInfo(self, *arg):
        title = gameStrings.TEXT_FUBENPROXY_433 % FD.data.get(self.queueFbNo, {}).get('name', '')
        ret = {'title': title,
         'queueCount': self.queueCount}
        return uiUtils.dict2GfxDict(ret, True)

    def showFubenQueue(self, fbNo, rank):
        self.queueFbNo = fbNo
        self.queueCount = rank
        if hasattr(self, 'fbQueueMediator') and self.fbQueueMediator:
            self.refreshFubenQueue(fbNo, rank)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_QUEUE)

    def refreshFubenQueue(self, fbNo, rank):
        title = gameStrings.TEXT_FUBENPROXY_433 % FD.data.get(fbNo, {}).get('name', '')
        ret = {'title': title,
         'queueCount': rank}
        self.fbQueueMediator.Invoke('refreshFubenQueue', uiUtils.dict2GfxDict(ret, True))

    def closeFubenQueue(self):
        self.fbQueueMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_QUEUE)

    def onQuitFubenQueue(self, *arg):
        self.closeFubenQueue()
        BigWorld.player().cell.cancelFubenQueue(self.queueFbNo)

    def showFubenTarget(self, targets, lvl = 1):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_TARGET)
        self.fubenLvl = lvl
        self.fubenTarget = []
        for targetItem in targets:
            tempItem = []
            tempItem.append(gbk2unicode(targetItem[0]))
            tempItem.append(gbk2unicode(targetItem[1]))
            self.fubenTarget.append(tempItem)

        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_TARGET)
        self.showFubenHeadTip(lvl)

    def showFubenOneResult(self, oneResult, lvl = 1, succ = True):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_ONE_RESULT)
        self.fubenOneResult = []
        self.fubenLvl = lvl
        self.fubenSucc = succ
        for result in oneResult:
            tempResult = []
            tempResult.append(gbk2unicode(result[0]))
            tempResult.append(gbk2unicode(result[1]))
            self.fubenOneResult.append(tempResult)

        self.showFubenHeadTip('succ' if succ else 'fail')

    def showFubenOneResultLoaded(self):
        if len(self.fubenOneResult) > 0:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_ONE_RESULT)
            self.showFubenHeadTip('succ' if self.fubenSucc else 'fail')

    @ui.callAfterTime(0.5)
    def showFubenHeadTip(self, tip):
        self.headTip = tip
        if self.headTipMed:
            self.headTipMed.Invoke('showHeatTip', GfxValue(self.headTip))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_HEAD_TIP)

    def hideFbHeadTip(self):
        self.headTip = None
        self.headTipMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_HEAD_TIP)

    def onGetGoalInfo(self, *arg):
        ret = {}
        ret['score'] = int(self.evalInfo.evalInfo.get(const.FB_EVAL_TYPE_COMP, 0))
        ret['goal'] = []
        fbNo = formula.getFubenNo(BigWorld.player().spaceNo)
        guideVarInfo = self.evalInfo.evalInfo.get('guideVarInfo', [])
        goals = {value.get('stageTag'):value for key, value in FGD.data.items() if key[0] == fbNo and value.get('stageTag') in guideVarInfo}
        for key, value in goals.items():
            titleDesc = value.get('titleDesc', '')
            isReach = guideVarInfo.get(value.get('stageTag', ''), False)
            ret['goal'].append([titleDesc, isReach])

        return uiUtils.dict2GfxDict(ret, True)

    def onGetGoalAward(self, *arg):
        ret = {}
        ret['score'] = int(self.evalInfo.evalInfo.get(const.FB_EVAL_TYPE_EXTRA, 0))
        ret['goal'] = []
        fbNo = formula.getFubenNo(BigWorld.player().spaceNo)
        guideVarInfo = self.evalInfo.evalInfo.get('guideVarInfo', [])
        goals = {value.get('stageTag'):value for key, value in FGD.data.items() if key[0] == fbNo and value.get('reward', [])}
        tmp = []
        for key, value in goals.items():
            reward = value['reward']
            for rewardItem in reward:
                if rewardItem[3] in tmp:
                    continue
                tmp.append(rewardItem[3])
                rewardDesc = rewardItem[2]
                rewardMax = rewardItem[1][0]
                rewardCount = guideVarInfo.get(rewardItem[3], 0)
                ret['goal'].append([rewardDesc, rewardCount, rewardMax])

        return uiUtils.dict2GfxDict(ret, True)

    def onPlaySound(self, *arg):
        gameglobal.rds.sound.playSound(gameglobal.SD_81)

    def setFame(self, fameData):
        if self.fubenRewardMed:
            self.fubenRewardMed.Invoke('setFame', uiUtils.dict2GfxDict(fameData, True))
            self.fameData = None
        else:
            self.fameData = fameData

    def onEnableQRCode(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableQRCode', False))

    def onShareFubenReward(self, *args):
        if self.topMediator:
            widget = ASObject(self.topMediator.Invoke('getWidget'))
            yOffSet = 20
            leftPosX, leftPosY = ASUtils.local2Global(widget, 0, 0)
            rightPosX, rightPosY = ASUtils.local2Global(widget, widget.bg.width, yOffSet + widget.bg.height)
            info = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            info.uiRange = [(leftPosX, leftPosY), (rightPosX, rightPosY)]
            gameglobal.rds.ui.qrCodeAppScanShare.show(info)

    def onIfGotoReward(self, *args):
        return GfxValue(self.gotoReward)


class IRewardItemInfo(object):

    def __init__(self):
        pass

    def getPath(self):
        return ''

    def getAmount(self):
        return 0

    def getIconId(self):
        return 0

    def getIconName(self):
        return ''

    def getQualityColor(self):
        return 'nothing'

    def getIconType(self):
        return gametypes.BONUS_TYPE_ITEM


class RewardItemInfo(IRewardItemInfo):

    def __init__(self, icon):
        super(RewardItemInfo, self).__init__()
        self.icon = icon

    def getPath(self):
        return uiUtils.getItemIconFile40(self.icon[1])

    def getAmount(self):
        return int(self.icon[2])

    def getIconId(self):
        return self.icon[1]

    def getIconName(self):
        return ID.data[self.icon[1]].get('name', '')

    def getQualityColor(self):
        quality = ID.data[self.icon[1]].get('quality', 0)
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'green')
        return qualitycolor

    def getIconType(self):
        return self.icon[0]


class RewardedItemInfo(RewardItemInfo):

    def __init__(self, icon):
        super(RewardedItemInfo, self).__init__(icon)

    def getAmount(self):
        p = BigWorld.player()
        return int(self.icon[2] * p.fbAwardMultiple)
