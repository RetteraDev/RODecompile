#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/phaseFubenProxy.o
import BigWorld
from uiProxy import UIProxy
import gameglobal
import formula
import utils
from guis import uiConst
from guis import uiUtils
from data import fb_data as FD
from data import fb_award_data as FAD
from data import bonus_data as BD
from cdata import game_msg_def_data as GMDD
from data import bonus_set_data as BSD
PHASE_FUBEN_ICON_PATH = 'phaseFuben/%s.dds'

class PhaseFubenProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PhaseFubenProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetPhaseData,
         'getRewards': self.onGetRewards,
         'getFubenList': self.onGetFubenList,
         'closeFubenList': self.onCloseFubenList,
         'enterFuben': self.onEnterFuben}
        self.mediator = None
        self.listMed = None
        self.phaseFbNo = 0
        self.evalLevel = 0
        self.phaseEvalLevel = None
        self.selHeaderFb = False
        self.groupFollowOpen = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PHASE_FUBEN_RESULT:
            self.mediator = mediator
        if widgetId == uiConst.WIDGET_PHASE_FUBEN_LIST:
            self.listMed = mediator

    def showFubenResult(self, fbNo, evalInfo):
        self.phaseFbNo = fbNo
        self.phaseEvalLevel = evalInfo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PHASE_FUBEN_RESULT, True, True)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)
        BigWorld.player().lockKey(gameglobal.KEY_POS_UI)

    def showFubenList(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PHASE_FUBEN_LIST)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PHASE_FUBEN_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)
        BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)
        self.selHeaderFb = False
        self.groupFollowOpen = False

    def onGetPhaseData(self, *arg):
        ret = {}
        fbData = FD.data.get(self.phaseFbNo, {})
        ret['title'] = fbData.get('phaseTitle', '')
        ret['desc'] = fbData.get('phaseDesc', '')
        ret['sign'] = fbData.get('phaseSign', '')
        self.evalLevel = self.phaseEvalLevel.get('fbScoreLv', 0)
        ret['level'] = self.evalLevel
        ret['bonus'] = self._getBonusReward()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetRewards(self, *arg):
        BigWorld.player().cell.getPhaseFbAward()
        self.hide()

    def _getBonusReward(self):
        bonusId = FAD.data.get((self.phaseFbNo, self.evalLevel), {}).get('bonusId', 0)
        bonusIds = BD.data.get(bonusId, {}).get('bonusIds', [])
        fixedBonus = []
        for rewardId in bonusIds:
            bonusData = BSD.data.get(rewardId, {})
            for bonus in bonusData:
                fixedBonus.append(bonus)

        ret = {}
        ret['rewards'] = []
        ret['rewardItems'] = []
        for bonus in fixedBonus:
            if bonus['bonusType'] == 1:
                if bonus.get('calcType') in (0, 1):
                    itemId = utils.filtItemByConfig(bonus['bonusId'], lambda e: e)
                else:
                    itemId = bonus['bonusId']
                if not itemId:
                    continue
                ret['rewardItems'].append(uiUtils.getGfxItemById(itemId, count=bonus['maxBonusNum']))
            elif bonus['bonusType'] == 2:
                if bonus['bonusId'] == 1:
                    ret['rewards'].append({'type': 'bindCash',
                     'value': bonus['maxBonusNum']})
                elif bonus['bonusId'] == 0:
                    ret['rewards'].append({'type': 'cash',
                     'value': bonus['maxBonusNum']})
            elif bonus['bonusType'] == 3:
                ret['rewards'].append({'type': 'fame',
                 'value': bonus['maxBonusNum']})
            elif bonus['bonusType'] == 4:
                ret['rewards'].append({'type': 'exp',
                 'value': bonus['maxBonusNum']})
            elif bonus['bonusType'] == 5:
                ret['rewards'].append({'type': 'socialExp',
                 'value': bonus['maxBonusNum']})

        return ret

    def onGetFubenList(self, *arg):
        p = BigWorld.player()
        fbList = getattr(p, 'fbStatusList', [])
        fbList = self.filterFuben(fbList)
        ret = []
        headerSpaceNo = p.membersPos.get(p.headerGbId, (0,))[0]
        headerFbNo = formula.getFubenNo(headerSpaceNo)
        for i in fbList:
            obj = {}
            fbNo = i
            obj['fbId'] = fbNo
            obj['fbName'] = formula.getFbDetailName(fbNo)
            obj['icon'] = PHASE_FUBEN_ICON_PATH % FD.data.get(fbNo, {}).get('phaseIcon', '1')
            obj['selFb'] = self.selHeaderFb and headerFbNo == fbNo
            if obj['selFb']:
                self.selHeaderFb = False
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    def onCloseFubenList(self, *arg):
        self.closePhaseFubenList()

    def closePhaseFubenList(self):
        self.listMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PHASE_FUBEN_LIST)

    def onEnterFuben(self, *arg):
        fbNo = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if self.groupFollowOpen:
            p.cell.applyGroupFollow()
            self.groupFollowOpen = False
        p.cell.getFubenEnterHelpInfo(fbNo)

    def pushPhaseFubenMsg(self, pushMsgId):
        gameglobal.rds.ui.pushMessage.addPushMsg(pushMsgId)
        gameglobal.rds.ui.pushMessage.setCallBack(pushMsgId, {'click': self.openPhaseFubenList})

    def removePhaseFubenMsg(self, pushMsgId):
        gameglobal.rds.ui.pushMessage.removePushMsg(pushMsgId)

    def openPhaseFubenList(self, *arg):
        self._openPhaseFubenList()

    def _openPhaseFubenList(self):
        fbNo = formula.getFubenNo(BigWorld.player().spaceNo)
        if not fbNo:
            self.showFubenList()
        else:
            BigWorld.player().showGameMsg(GMDD.data.ALREADY_IN_FUBEN, ())

    def openPhaseListByGroupFollow(self):
        self.selHeaderFb = True
        self.groupFollowOpen = True
        self._openPhaseFubenList()

    def filterFuben(self, fubenList):
        filteredList = []
        for fbNo in fubenList:
            if FD.data.get(fbNo, {}).get('isPushIcon', 0):
                filteredList.append(fbNo)

        return filteredList
