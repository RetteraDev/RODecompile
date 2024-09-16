#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/xiuYingExpGetProxy.o
import BigWorld
import sys
import gameglobal
import const
import formula
import utils
import gametypes
import gamelog
import events
from asObject import ASObject
from guis import uiConst
from guis import uiUtils
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import UIProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from asObject import ASUtils
from data import sys_config_data as SCD
from data import flowback_bonus_type_data as FBTD
from cdata import game_msg_def_data as GMDD
from data import avatar_lv_data as ALD
from data import vp_level_data as VLD
CONST_UNIT = 10000
ADJUST_POS_WIDTH = 350

class XiuYingExpGetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(XiuYingExpGetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.npcId = None
        self.isNeedShowWidget = False
        self.saveFreeVp = 0
        self.isClose = True
        self.timer = None
        self.playerMaxLv = -1
        self.isInCD = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_XIUYING_EXP_GET, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_XIUYING_EXP_GET:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_XIUYING_EXP_GET)
        gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.npcId = None
        self.cancelTimer()

    def show(self, npcId):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_XIUYING_EXP_GET)

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshInfo()

    def refreshInfo(self, bGetSucc = False):
        if self.hasBaseData():
            p = BigWorld.player()
            enableFlowbackBonus = gameglobal.rds.configData.get('enableFlowbackBonus', False)
            if enableFlowbackBonus and p.flowbackBonus.isValid() and p.flowbackBonus.vpBonus.availCount > 0:
                self.widget.gotoAndStop('zhuanhua')
                self.refreshDailyMc(bGetSucc)
                self.refreshLimitMc()
            else:
                self.widget.gotoAndStop('onlylingqu')
                self.refreshDailyMc(bGetSucc)
            self.timer = BigWorld.callback(1, self.refreshInfo)

    def refreshLimitMc(self):
        p = BigWorld.player()
        self.widget.limitMc.transBtn.addEventListener(events.BUTTON_CLICK, self.handleTransBtn, False, 0, True)
        dueTime = gameStrings.XIUYING_TRANS_REMAIN_TIME % utils.formatDuration(p.flowbackBonus.getBonusRemainTime())
        time = gameStrings.OVERFLOW_XIUYING_TRANS % p.flowbackBonus.vpBonus.availCount
        normal = uiUtils.getTextFromGMD(GMDD.data.XIUYING_QUICK_TRANS) % (int((p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.roFirstExtra) / CONST_UNIT), int(p.flowbackBonus.vpBonus.fixedAmount / CONST_UNIT))
        extra = ''
        baseData = FBTD.data.get(p.flowbackBonus.vpBonus.lostType, {})
        if baseData and p.flowbackBonus.vpBonus.availCount > 0:
            leftTime = p.flowbackBonus.vpBonus.lastApplyTime + baseData.get('vpApplyInterval', 0) - utils.getNow()
            vpBtnEnabled = True
            if leftTime <= 0:
                vpCoolDown = ''
            else:
                vpCoolDown = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
        else:
            vpBtnEnabled = False
            vpCoolDown = ''
        vpBtnLabel = gameStrings.XIUYING_TRANS if vpCoolDown == '' else gameStrings.XIUYING_TRANS_RESET
        self.isInCD = False if vpCoolDown == '' else True
        self.widget.limitMc.remainTime.htmlText = dueTime
        self.widget.limitMc.remainCnt.htmlText = time
        self.widget.limitMc.coolDownTime.htmlText = vpCoolDown if vpCoolDown else uiUtils.toHtml(utils.formatTimeStr(0, 'h:m:s', True, 2, 2, 2), '#7acc29')
        self.widget.limitMc.normalTips.htmlText = normal
        self.widget.limitMc.transBtn.label = vpBtnLabel

    def refreshDailyMc(self, bGetSucc = False):
        p = BigWorld.player()
        self.widget.dailyMc.numInput.addEventListener(events.EVENT_CHANGE, self.handleChangeNum, False, 0, True)
        self.widget.dailyMc.getBtn.addEventListener(events.BUTTON_CLICK, self.handleGetBtn, False, 0, True)
        self.widget.dailyMc.numInput.maxNum = max(0, int((p.overflowExp - p.flowbackGroupBonus.restExp) / CONST_UNIT))
        self.widget.dailyMc.numInput.textField.restrict = '0-9'
        freeVp = int(round(formula.calcFormulaById(const.FREE_VP_WUXING, {'lv': p.lv})))
        vp = getattr(p, 'gainOverflowExpDaily', 0)
        maxNumTxt = gameStrings.XIUYING_NUM % max(0, int((p.overflowExp - p.flowbackGroupBonus.restExp) / CONST_UNIT))
        alreadyGetTxt = gameStrings.XIUYING_ALREADY_GET % int(vp / CONST_UNIT)
        yunChuiNum = self.costVp(freeVp, self.expToWuXing(vp), self.expToWuXing(self.getInputNum() * CONST_UNIT))
        freeXiuYingTxt = uiUtils.getTextFromGMD(GMDD.data.WU_XING_GET_TEXT, '%d') % (self.wuXingToExp(freeVp) / CONST_UNIT)
        self.widget.dailyMc.sIcon1.bonusType = 'yunChui'
        self.widget.dailyMc.maxNumTxt.text = maxNumTxt
        self.widget.dailyMc.alreadyGetTxt.text = alreadyGetTxt
        self.widget.dailyMc.alreadyGetTxt.x = self.widget.dailyMc.maxNumTxt.x + self.widget.dailyMc.maxNumTxt.textWidth
        self.widget.dailyMc.yunChuiTxt.text = str(yunChuiNum)
        ASUtils.setHitTestDisable(self.widget.dailyMc.yunChuiTxt, True)
        ASUtils.setHitTestDisable(self.widget.dailyMc.yunChuiPreTxt, True)
        self.widget.dailyMc.freeXiuYingTxt.htmlText = freeXiuYingTxt
        totalWidth = self.widget.dailyMc.sIcon0.width + 5 + self.widget.dailyMc.numInput.width + 5 + self.widget.dailyMc.maxNumTxt.textWidth + self.widget.dailyMc.alreadyGetTxt.textWidth
        adjustX = ADJUST_POS_WIDTH - totalWidth
        self.widget.dailyMc.sIcon0.x = adjustX / 2
        self.widget.dailyMc.numInput.x = self.widget.dailyMc.sIcon0.x + self.widget.dailyMc.sIcon0.width + 5
        self.widget.dailyMc.maxNumTxt.x = self.widget.dailyMc.numInput.x + self.widget.dailyMc.numInput.width + 5
        self.widget.dailyMc.alreadyGetTxt.x = self.widget.dailyMc.maxNumTxt.x + self.widget.dailyMc.maxNumTxt.textWidth
        if bGetSucc:
            self.widget.dailyMc.numInput.text = ''

    def openXiuYing(self, npcId = None):
        if gameglobal.rds.configData.get('enableBackflowVp', False) and gameglobal.rds.configData.get('enableFlowbackBonus', False):
            self.npcId = npcId
            self.isNeedShowWidget = True
            BigWorld.player().cell.queryBackflowVp()

    def getEntity(self):
        e = None
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
        else:
            e = BigWorld.player()
        return e

    def setMaxVpPushMsg(self, amount):
        p = BigWorld.player()
        if self.playerMaxLv == -1:
            p.cell.getServerPlayerMaxLv()
        if self.playerMaxLv == -1 or p.overflowExp == 0:
            return
        if p.lv >= self.playerMaxLv and p.expXiuWei >= SCD.data.get('forbidAddOverflowVpXiuWeiRatioClient', 1.0) * self.getLvExpNeed(p.lv):
            return
        if self.isClose:
            minFreeVp = SCD.data.get('MSG_WUXING_FREEVP', 0)
            if amount > minFreeVp and self.saveFreeVp != amount:
                self.saveFreeVp = amount

    def getLvExpNeed(self, lv):
        return ALD.data.get(lv, {}).get('upExp', sys.maxint)

    def setPlayerMaxLv(self, lv):
        self.playerMaxLv = lv
        self.setMaxVpPushMsg(p.overflowExp)

    def handleChangeNum(self, *args):
        p = BigWorld.player()
        num = self.getInputNum()
        if num > max(0, int((p.overflowExp - p.flowbackGroupBonus.restExp) / CONST_UNIT)):
            self.widget.dailyMc.numInput.text = max(0, int((p.overflowExp - p.flowbackGroupBonus.restExp) / CONST_UNIT))
        self.refreshDailyMc()

    def handleGetBtn(self, *args):
        num = self.getInputNum()
        if num <= 0:
            return
        p = BigWorld.player()
        currentVp = p.savedVp + p.vpStorage
        exp = num * CONST_UNIT
        if self.expToWuXing(exp) + currentVp > const.MAX_WUXING:
            p.showGameMsg(GMDD.data.REFUSE_GET_WUXING, ())
            return
        p.cell.getOverflowExp(exp)

    def costVp(self, c, x, m):
        return int(round(formula.calcFormulaById(const.COST_VP_WUXING, {'x': x,
         'm': m,
         'c': c})))

    def cancelTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def handleTransBtn(self, *args):
        self.onQuickGet()

    def onQuickGet(self):
        if self.isInCD:
            self.realClearBonusCD()
        else:
            self.realApplyBonus(gametypes.FLOWBACK_BONUS_TYPE_VP)

    def realClearBonusCD(self):
        p = BigWorld.player()
        itemId, itemNum = FBTD.data.get(p.flowbackBonus.vpBonus.lostType, {}).get('vpClearCDItem', (0, 0))
        if itemId == 0 or itemNum == 0:
            itemInfo = None
        else:
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['count'] = uiUtils.convertNumStr(p.inv.countItemInPages(itemId, enableParentCheck=True), itemNum)
        msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_CLEAR_VP_BONUS_CD_HINT, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.clearFlowbackBonusVpCD, itemData=itemInfo)

    def realApplyBonus(self, typeId):
        p = BigWorld.player()
        if typeId == gametypes.FLOWBACK_BONUS_TYPE_VP:
            vData = VLD.data.get(p.lv, {})
            exp = p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.firstExtra
            msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_GET_VP_BONUS_HINT, '%d') % (exp, exp)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyFlowbackBonus, gametypes.FLOWBACK_BONUS_TYPE_VP, False))
        elif typeId in (gametypes.FLOWBACK_BONUS_TYPE_JIULI, gametypes.FLOWBACK_BONUS_TYPE_YAOLI):
            gameglobal.rds.ui.userBackAward.show(typeId)

    def hasBaseData(self):
        if self.widget:
            return True
        return False

    def compensateInfoOnLogin(self, hasAccountBonus):
        if hasAccountBonus == 0:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1)
        else:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2)

    def getXiuYing(self, num):
        self.isNeedRefresh = True
        npcEnt = BigWorld.entities.get(self.npcId)
        if npcEnt:
            npcEnt.cell.getBackflowVp(num)

    def getInputNum(self):
        numStr = self.widget.dailyMc.numInput.text
        if numStr:
            return int(self.widget.dailyMc.numInput.text)
        return 0

    def wuXingToExp(self, num):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        vpDefaultLower = vData.get('vpDefaultLower', 0)
        return num * vpDefaultLower

    def expToWuXing(self, num):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        vpDefaultLower = vData.get('vpDefaultLower', 0)
        if not vpDefaultLower:
            return 0
        return num / vpDefaultLower
