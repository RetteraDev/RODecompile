#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/userBackProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import utils
from uiProxy import UIProxy
from callbackHelper import Functor
from data import flowback_activity_data as FAD
from data import flowback_bonus_type_data as FBTD
from data import vp_level_data as VLD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
FUNC_GOTO = 1
FUNC_CHAT = 2
FUNC_ITEM = 3
GUILD_ACTIVITY = 3

class UserBackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UserBackProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'clickFuncBtn': self.onClickFuncBtn,
         'applyBonus': self.onApplyBonus,
         'clearBonusCD': self.onClearBonusCD}
        self.mediator = None
        self.idx = 0
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_USER_BACK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_USER_BACK:
            self.mediator = mediator
            self.refreshExtraInfo()
            tabInfo = {}
            for i, value in FAD.data.iteritems():
                tabInfo[i] = value.get('name', '')

            return uiUtils.dict2GfxDict({'tabInfo': tabInfo,
             'showExtra': BigWorld.player().flowbackBonus.isValid()}, True)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_USER_BACK)

    def reset(self):
        self.idx = 0
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def checkInTime(self):
        if SCD.data.has_key('flowbackStartTimes') and SCD.data.has_key('flowbackEndTimes'):
            fbStartTime = SCD.data['flowbackStartTimes']
            fbEndTime = SCD.data['flowbackEndTimes']
            current = utils.getNow()
            if not any([ utils.inTimeTupleRange(fbStartTime[i], fbEndTime[i], current) for i in xrange(len(fbStartTime)) ]):
                return False
            else:
                return True
        else:
            return True

    def showFlowBackPushMsg(self):
        if not gameglobal.rds.configData.get('enableFlowbackBonus', False):
            return
        if not self.checkInTime():
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_FLOW_BACK)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FLOW_BACK, {'click': self.show})

    def show(self):
        gameglobal.rds.ui.systemButton.hideUserBackHint()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FLOW_BACK)
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableFlowbackBonus', False):
            p.showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())
            return
        if not self.checkInTime():
            p.showGameMsg(GMDD.data.FLOWBACK_PANEL_NOT_IN_TIME_HINT, ())
            return
        if p.realLv < SCD.data.get('FLOWBACK_MIN_LV', 20):
            p.showGameMsg(GMDD.data.FLOWBACK_PANEL_LV_HINT, ())
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_USER_BACK)

    def onGetInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.idx = idx
        self.refreshMainInfo(idx)

    def refreshMainInfo(self, idx):
        if self.idx != idx:
            return
        if self.mediator:
            info = {}
            info['idx'] = self.idx
            baseInfo = FAD.data.get(self.idx + 1, {})
            info['title'] = baseInfo.get('name', '')
            info['desc'] = baseInfo.get('desc', '')
            funcList = []
            if baseInfo.get('fun1'):
                funcInfo = {}
                funcInfo['funcType'] = FUNC_GOTO
                funcInfo['label'], _ = baseInfo.get('fun1')
                funcInfo['idx'] = self.idx + 1
                funcList.append(funcInfo)
            if baseInfo.get('fun2'):
                funcInfo = {}
                funcInfo['funcType'] = FUNC_CHAT
                funcInfo['label'], _ = baseInfo.get('fun2')
                funcInfo['idx'] = self.idx + 1
                funcList.append(funcInfo)
            if baseInfo.get('fun3'):
                funcInfo = {}
                funcInfo['funcType'] = FUNC_ITEM
                funcInfo['label'], _ = baseInfo.get('fun3')
                funcInfo['idx'] = self.idx + 1
                funcList.append(funcInfo)
            info['funcList'] = funcList
            self.mediator.Invoke('refreshMainInfo', uiUtils.dict2GfxDict(info, True))

    def refreshExtraInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.flowbackBonus.isValid():
                return
            info = {}
            info['total'] = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_PANEL_BONUS_HINT, '%d<br>%d<br>%d') % ((p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.extraAmount) / 10000 * p.flowbackBonus.vpBonus.totalCount + p.flowbackBonus.vpBonus.roFirstExtra / 10000, (p.flowbackBonus.yaoliBonus.fixedAmount / 10 + p.flowbackBonus.yaoliBonus.extraAmount / 10) * p.flowbackBonus.yaoliBonus.totalCount, (p.flowbackBonus.jiuliBonus.fixedAmount + p.flowbackBonus.jiuliBonus.extraAmount) * p.flowbackBonus.jiuliBonus.totalCount)
            vp = {}
            vp['typeId'] = gametypes.FLOWBACK_BONUS_TYPE_VP
            vp['title'] = '修盈经验'
            vp['time'] = '可转换%d次' % p.flowbackBonus.vpBonus.availCount
            vp['normal'] = '首次可免费转换%d万点, 其后每次可转换%d万点经验' % ((p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.roFirstExtra) / 10000, p.flowbackBonus.vpBonus.fixedAmount / 10000)
            vp['extra'] = ''
            info['vp'] = vp
            yaoli = {}
            yaoli['typeId'] = gametypes.FLOWBACK_BONUS_TYPE_YAOLI
            yaoli['title'] = '地宫经验怪数'
            yaoli['time'] = '可领取%d次' % p.flowbackBonus.yaoliBonus.availCount
            yaoli['normal'] = '每次可增加%d个%s' % (p.flowbackBonus.yaoliBonus.fixedAmount / 10, yaoli['title'])
            yaoli['extra'] = '额外多增加%d个%s' % (p.flowbackBonus.yaoliBonus.extraAmount / 10, yaoli['title'])
            info['yaoli'] = yaoli
            jiuli = {}
            jiuli['typeId'] = gametypes.FLOWBACK_BONUS_TYPE_JIULI
            jiuli['title'] = '酒力'
            jiuli['time'] = '可领取%d次' % p.flowbackBonus.jiuliBonus.availCount
            jiuli['normal'] = '每次可增加%d点%s' % (p.flowbackBonus.jiuliBonus.fixedAmount, jiuli['title'])
            jiuli['extra'] = '额外多增加%d点%s' % (p.flowbackBonus.jiuliBonus.extraAmount, jiuli['title'])
            info['jiuli'] = jiuli
            self.mediator.Invoke('refreshExtraInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.mediator:
            p = BigWorld.player()
            needTimer = False
            info = {}
            baseData = FBTD.data.get(p.flowbackBonus.vpBonus.lostType, {})
            if baseData and p.flowbackBonus.vpBonus.availCount > 0:
                leftTime = p.flowbackBonus.vpBonus.lastApplyTime + baseData.get('vpApplyInterval', 0) - utils.getNow()
                info['vpBtnEnabled'] = True
                if leftTime <= 0:
                    info['vpCoolDown'] = ''
                else:
                    info['vpCoolDown'] = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
                    needTimer = True
            else:
                info['vpBtnEnabled'] = False
                info['vpCoolDown'] = ''
            info['vpBtnLabel'] = '领 悟' if info['vpCoolDown'] == '' else '重 置'
            baseData = FBTD.data.get(p.flowbackBonus.yaoliBonus.lostType, {})
            if baseData and p.flowbackBonus.yaoliBonus.availCount > 0:
                leftTime = p.flowbackBonus.yaoliBonus.lastApplyTime + baseData.get('yaoliApplyInterval', 0) - utils.getNow()
                if leftTime <= 0:
                    info['yaoliBtnEnabled'] = True
                    info['yaoliCoolDown'] = ''
                else:
                    info['yaoliBtnEnabled'] = False
                    info['yaoliCoolDown'] = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
                    needTimer = True
            else:
                info['yaoliBtnEnabled'] = False
                info['yaoliCoolDown'] = ''
            baseData = FBTD.data.get(p.flowbackBonus.jiuliBonus.lostType, {})
            if baseData and p.flowbackBonus.jiuliBonus.availCount > 0:
                leftTime = p.flowbackBonus.jiuliBonus.lastApplyTime + baseData.get('jiuliApplyInterval', 0) - utils.getNow()
                if leftTime <= 0:
                    info['jiuliBtnEnabled'] = True
                    info['jiuliCoolDown'] = ''
                else:
                    info['jiuliBtnEnabled'] = False
                    info['jiuliCoolDown'] = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
                    needTimer = True
            else:
                info['jiuliBtnEnabled'] = False
                info['jiuliCoolDown'] = ''
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            if needTimer:
                self.timer = BigWorld.callback(1, self.updateTime)

    def onClickFuncBtn(self, *arg):
        funcType = int(arg[3][0].GetNumber())
        idx = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if funcType == FUNC_GOTO:
            p.cell.useNoviceBoostTeleportWithFlowback(idx)
        elif funcType == FUNC_CHAT:
            p.cell.chatToWorldForCompanionWithFlowback(idx)
        elif funcType == FUNC_ITEM:
            if idx == GUILD_ACTIVITY:
                if p.guild:
                    msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_GET_ITEM_BONUS_HINT, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.retrieveFlowbackBonusFromGuild)
                else:
                    p.showGameMsg(GMDD.data.YCWZ_TIP_NONE_GUILD, ())
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_GET_ITEM_BONUS_HINT, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyFlowbackBonus, gametypes.FLOWBACK_BONUS_TYPE_ITEM, False))

    def onApplyBonus(self, *arg):
        typeId = int(arg[3][0].GetNumber())
        self.realApplyBonus(typeId)

    def realApplyBonus(self, typeId):
        p = BigWorld.player()
        if typeId == gametypes.FLOWBACK_BONUS_TYPE_VP:
            vData = VLD.data.get(p.lv, {})
            exp = p.flowbackBonus.vpBonus.fixedAmount + p.flowbackBonus.vpBonus.firstExtra
            msg = uiUtils.getTextFromGMD(GMDD.data.FLOWBACK_GET_VP_BONUS_HINT, '%d') % (exp, exp)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyFlowbackBonus, gametypes.FLOWBACK_BONUS_TYPE_VP, False))
        elif typeId in (gametypes.FLOWBACK_BONUS_TYPE_JIULI, gametypes.FLOWBACK_BONUS_TYPE_YAOLI):
            gameglobal.rds.ui.userBackAward.show(typeId)

    def onClearBonusCD(self, *arg):
        typeId = int(arg[3][0].GetNumber())
        if typeId != gametypes.FLOWBACK_BONUS_TYPE_VP:
            return
        self.realClearBonusCD()

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

    def wuXingToExp(self, num):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        vpDefaultLower = vData.get('vpDefaultLower', 0)
        return num * vpDefaultLower
