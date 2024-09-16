#Embedded file name: /WORKSPACE/data/entities/client/guis/wuxinggetproxy.o
import BigWorld
import sys
import gameglobal
import const
import formula
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import UIProxy
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import flowback_bonus_type_data as FBTD
from cdata import game_msg_def_data as GMDD
from data import avatar_lv_data as ALD

class WuXingGetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WuXingGetProxy, self).__init__(uiAdapter)
        self.modelMap = {'init': self.onInit,
         'normalGet': self.onNormalGet,
         'quickGet': self.onQuickGet,
         'numChange': self.onNumChange}
        self.mediator = None
        self.maxVp = 0
        self.npcId = None
        self.isNeedShowWidget = False
        self.isNeedRefresh = False
        self.saveFreeVp = 0
        self.isClose = True
        self.timer = None
        self.playerMaxLv = -1

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WUXING_GET:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WUXING_GET)
        gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.maxVp = 0
        self.npcId = None
        self.isNeedShowWidget = False
        self.isNeedRefresh = False
        self.isClose = True
        self.stopTimer()

    def show(self, npcId):
        if gameglobal.rds.configData.get('enableBackflowVp', False) and gameglobal.rds.configData.get('enableFlowbackBonus', False):
            self.npcId = npcId
            self.isNeedShowWidget = True
            BigWorld.player().cell.queryBackflowVp()

    def onInit(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            freeVp = int(round(formula.calcFormulaById(const.FREE_VP_WUXING, {'lv': p.lv})))
            vp = getattr(p, 'gainBackflowVpDaily', 0)
            info['maxNum'] = self.maxVp
            info['maxNumText'] = '/%s（今日已领取：%s）' % (self.maxVp, vp)
            info['yunChuiText'] = '本次领取需要消耗云垂积分：%s' % format(self.costVp(freeVp, vp, 0), ',')
            info['freeWuXingText'] = uiUtils.getTextFromGMD(GMDD.data.WU_XING_GET_TEXT, '%d') % freeVp
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def setWuXing(self, num):
        self.isNeedRefresh = True
        npcEnt = BigWorld.entities.get(self.npcId)
        if npcEnt:
            npcEnt.cell.getBackflowVp(num)

    def refreshInfoMap(self):
        if self.isNeedShowWidget:
            BigWorld.player().cell.queryBackflowVp()

    def onNormalGet(self, *arg):
        num = int(arg[3][0].GetNumber())
        if num <= 0:
            return
        p = BigWorld.player()
        currentVp = p.savedVp + p.vpStorage
        if num + currentVp > const.MAX_WUXING:
            p.showGameMsg(GMDD.data.REFUSE_GET_WUXING, ())
            return
        if p.flowbackBonus.isValid():
            unUseYunChuiVp = p.flowbackBonus.vpBonus.fixedAmount * p.flowbackBonus.vpBonus.availCount
            if self.maxVp - num < unUseYunChuiVp:
                msg = uiUtils.getTextFromGMD(GMDD.data.GET_WUXING_TOO_MUCH, '%d') % unUseYunChuiVp
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.setWuXing, num), yesBtnText='继续领取', noBtnText='放弃领取')
            else:
                self.setWuXing(num)
        else:
            self.setWuXing(num)

    def onQuickGet(self, *arg):
        isInCD = arg[3][0].GetBool()
        if isInCD:
            gameglobal.rds.ui.userBack.realClearBonusCD()
        else:
            gameglobal.rds.ui.userBack.realApplyBonus(gametypes.FLOWBACK_BONUS_TYPE_VP)

    def onNumChange(self, *arg):
        num = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        freeVp = int(round(formula.calcFormulaById(const.FREE_VP_WUXING, {'lv': p.lv})))
        vp = getattr(p, 'gainBackflowVpDaily', 0)
        yunChuiText = '本次领取需要消耗云垂积分：%s' % format(self.costVp(freeVp, vp, num), ',')
        return GfxValue(gbk2unicode(yunChuiText))

    def costVp(self, c, x, m):
        return int(round(formula.calcFormulaById(const.COST_VP_WUXING, {'x': x,
         'm': m,
         'c': c})))

    def setMaxVp(self, amount):
        self.maxVp = amount
        if self.isNeedShowWidget:
            if self.isNeedRefresh:
                self.refreshInfo()
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WUXING_GET)
        else:
            self.setMaxVpPushMsg(amount)

    def setMaxVpPushMsg(self, amount):
        p = BigWorld.player()
        if self.playerMaxLv == -1:
            p.cell.getServerPlayerMaxLv()
        if self.playerMaxLv == -1 or self.maxVp == 0:
            return
        if p.lv >= self.playerMaxLv and p.expXiuWei >= SCD.data.get('forbidAddOverflowVpXiuWeiRatioClient', 1.0) * self.getLvExpNeed(p.lv):
            return
        if self.isClose:
            minFreeVp = SCD.data.get('MSG_WUXING_FREEVP', 0)
            if amount > minFreeVp and self.saveFreeVp != amount:
                self.saveFreeVp = amount

    def checkWuxing(self):
        BigWorld.player().cell.queryBackflowVp()

    def compensateInfoOnLogin(self, hasAccountBonus):
        if hasAccountBonus == 0:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1)
        else:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2)

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.mediator:
            p = BigWorld.player()
            needTimer = False
            info = {}
            if not p.flowbackBonus.isValid() or p.flowbackBonus.vpBonus.availCount <= 0:
                info['showExtra'] = False
                info['noQuickGetHint'] = uiUtils.getTextFromGMD(GMDD.data.WU_XING_GET_NO_QUICK_GET_HINT, '你很活跃，无需快速领悟')
            else:
                info['showExtra'] = True
                needTimer = True
                info['dueTime'] = '剩余时间：<br>%s' % utils.formatDuration(p.flowbackBonus.getBonusRemainTime())
                vp = {}
                vp['title'] = '悟性'
                vp['time'] = '可领悟%d次' % p.flowbackBonus.vpBonus.availCount
                vp['normal'] = '首次可免费领悟%d点, 其后每次可领悟%d点悟性直接获得经验' % (p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.roFirstExtra, p.flowbackBonus.vpBonus.fixedAmount)
                vp['extra'] = ''
                info['vp'] = vp
                baseData = FBTD.data.get(p.flowbackBonus.vpBonus.lostType, {})
                if baseData and p.flowbackBonus.vpBonus.availCount > 0:
                    leftTime = p.flowbackBonus.vpBonus.lastApplyTime + baseData.get('vpApplyInterval', 0) - utils.getNow()
                    info['vpBtnEnabled'] = True
                    if leftTime <= 0:
                        info['vpCoolDown'] = ''
                    else:
                        info['vpCoolDown'] = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
                else:
                    info['vpBtnEnabled'] = False
                    info['vpCoolDown'] = ''
                info['vpBtnLabel'] = '领 悟' if info['vpCoolDown'] == '' else '重 置'
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            if needTimer:
                self.timer = BigWorld.callback(1, self.updateTime)

    def getLvExpNeed(self, lv):
        return ALD.data.get(lv, {}).get('upExp', sys.maxint)

    def setPlayerMaxLv(self, lv):
        self.playerMaxLv = lv
        self.setMaxVpPushMsg(self.maxVp)
