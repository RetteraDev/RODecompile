#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpEnhanceProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
import gametypes
import math
import utils
from uiProxy import UIProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from data import item_data as ID
from data import sys_config_data as SCD
from data import pvp_enhance_display_data as PEDD
from cdata import pvp_enhance_reset_consume_data as PERCD
from cdata import pvp_enhance_lv_data as PELD
from cdata import pvp_enhance_times_consume_data as PETCD
from cdata import game_msg_def_data as GMDD
from cdata import pursue_pvp_enhance_data as PPED

class PvpEnhanceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpEnhanceProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData,
         'selectSkill': self.onSelectSkill,
         'reset': self.onReset,
         'addTimes': self.onAddTimes,
         'useBind': self.onUseBind,
         'useAll': self.onUseAll,
         'usePoint': self.onUsePoint,
         'lvUp': self.onLvUp,
         'speedUp': self.onSpeedUp,
         'showPvpMasteryCatchUp': self.onShowPvpMasteryCatchUp}
        self.mediator = None
        self.pvpEnhance = {}
        self.eType = 0
        self.school = 0
        self.lvUpEffectSkill = (0, 0)
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_ENHANCE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PVP_ENHANCE:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PVP_ENHANCE)

    def reset(self):
        self.eType = 0
        self.school = 0
        self.lvUpEffectSkill = (0, 0)

    def clearAll(self):
        self.pvpEnhance = {}
        self.reset()

    def checkShow(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableWingWorldReady', False):
            if not gameglobal.rds.configData.get('enableWorldWar', False):
                p.showGameMsg(GMDD.data.PVP_ENHANCE_WORLD_WAR_NO_GROUP, ())
                return
            p.cell.queryWorldWar(p.worldWar.ver)
            if p.worldWar.getCountry().groupId not in gametypes.WORLD_WAR_GROUP:
                p.showGameMsg(GMDD.data.PVP_ENHANCE_WORLD_WAR_NO_GROUP, ())
                return
            if p.worldWar.state == gametypes.WORLD_WAR_STATE_CLOSE:
                p.showGameMsg(GMDD.data.PVP_ENHANCE_WORLD_WAR_NOT_OPEN, ())
                return
        pvpEnhancePanelLvLimit = SCD.data.get('pvpEnhancePanelLvLimit', 0)
        if p.realLv < pvpEnhancePanelLvLimit:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_PANEL_LV_LIMIT, (pvpEnhancePanelLvLimit,))
            return
        self.show()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PVP_ENHANCE)

    def updateInfo(self, data):
        curExp, limitLv = self.getCurExpAndLimitLv(self.eType, self.school)
        oldSkillLv = self.calcCurLv(self.eType, self.school, curExp, limitLv)
        self.pvpEnhance.update(data)
        curExp, limitLv = self.getCurExpAndLimitLv(self.eType, self.school)
        newSkillLv = self.calcCurLv(self.eType, self.school, curExp, limitLv)
        if oldSkillLv < newSkillLv:
            self.lvUpEffectSkill = (self.eType, self.school)
        self.refreshInfo()
        if gameglobal.rds.ui.pvpMasteryCatchUp.widget:
            gameglobal.rds.ui.pvpMasteryCatchUp.refreshInfo()

    def onGetInitData(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            info = {}
            schoolList = list(const.SCHOOL_SET)
            if not gameglobal.rds.configData.get('enableNewSchoolYeCha', False):
                schoolList.remove(const.SCHOOL_YECHA)
            allExp = 0
            atkList = []
            defList = []
            for (eType, school), value in PEDD.data.iteritems():
                if school not in schoolList:
                    continue
                skillInfo = {}
                skillInfo['eType'] = eType
                skillInfo['school'] = school
                skillInfo['schoolIcon'] = uiConst.SCHOOL_FRAME_DESC.get(school, '')
                skillInfo['skillName'] = value.get('name', '')
                skillInfo['iconPath'] = 'pvpEnhance/%d.dds' % value.get('icon', 0)
                curExp, limitLv = self.getCurExpAndLimitLv(eType, school)
                skillInfo['skillLv'] = 'Lv.%d' % self.calcCurLv(eType, school, curExp, limitLv)
                allExp += curExp
                if eType == const.PVP_ENHANCE_TYPE_ATK:
                    atkList.append(skillInfo)
                elif eType == const.PVP_ENHANCE_TYPE_DEF:
                    defList.append(skillInfo)

            atkList.sort(key=lambda x: x['school'])
            defList.sort(key=lambda x: x['school'])
            info['skillList'] = atkList + defList
            info['resetBtnEnabled'] = allExp > 0
            info['resetTips'] = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_RESET_BTN_TIPS, '%d') % len(PERCD.data)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onSelectSkill(self, *arg):
        self.eType = int(arg[3][0].GetNumber())
        self.school = int(arg[3][1].GetNumber())
        self.refreshDetailInfo()

    def refreshDetailInfo(self):
        if self.mediator:
            p = BigWorld.player()
            pedData = PEDD.data.get((self.eType, self.school), {})
            if not pedData:
                return
            info = {}
            info['skillInfo'] = {'iconPath': 'pvpEnhance/%d.dds' % pedData.get('icon', 0)}
            curExp, limitLv = self.getCurExpAndLimitLv(self.eType, self.school)
            skillLv = self.calcCurLv(self.eType, self.school, curExp, limitLv)
            info['skillLv'] = 'Lv.%d' % skillLv
            info['limitLv'] = gameStrings.TEXT_PVPENHANCEPROXY_170 % limitLv
            info['limitLvTips'] = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_LIMIT_LV_TIPS, '')
            if self.lvUpEffectSkill == (self.eType, self.school):
                self.lvUpEffectSkill = (0, 0)
                info['playLvUpEffect'] = True
            else:
                info['playLvUpEffect'] = False
            lvMax = pedData.get('lvMax', 0)
            currentValue = 100.0
            if skillLv >= lvMax:
                isMax = True
                expText = 'MAX'
                canLvUpEffectVisible = False
            else:
                isMax = False
                nowLvExp = PELD.data.get((skillLv, self.eType, self.school), {}).get('exp', 0)
                exp = curExp - nowLvExp
                maxExp = PELD.data.get((skillLv + 1, self.eType, self.school), {}).get('exp', 0) - nowLvExp
                if exp < maxExp:
                    currentValue = currentValue * exp / maxExp
                    canLvUpEffectVisible = False
                else:
                    lvLimit = PELD.data.get((skillLv + 1, self.eType, self.school), {}).get('lvLimit', 0)
                    canLvUpEffectVisible = p.realLv > lvLimit
                expText = '%d/%d' % (exp, maxExp)
            info['currentValue'] = currentValue
            info['expText'] = expText
            info['canLvUpEffectVisible'] = canLvUpEffectVisible
            info['isMax'] = isMax
            desc = pedData.get('desc', [])
            descList = []
            for descItem in desc:
                descInfo = {}
                descInfo['desc'] = descItem
                if self.eType == const.PVP_ENHANCE_TYPE_ATK:
                    oldVal = PELD.data.get((skillLv, self.eType, self.school), {}).get('atkEff', 0)
                elif self.eType == const.PVP_ENHANCE_TYPE_DEF:
                    oldVal = PELD.data.get((skillLv, self.eType, self.school), {}).get('defEff', 0)
                else:
                    oldVal = 0
                descInfo['oldVal'] = '%s%%' % str(round(oldVal * 100, 1))
                if skillLv >= lvMax:
                    descInfo['newVal'] = ''
                else:
                    if self.eType == const.PVP_ENHANCE_TYPE_ATK:
                        newVal = PELD.data.get((skillLv + 1, self.eType, self.school), {}).get('atkEff', 0)
                    elif self.eType == const.PVP_ENHANCE_TYPE_DEF:
                        newVal = PELD.data.get((skillLv + 1, self.eType, self.school), {}).get('defEff', 0)
                    else:
                        newVal = 0
                    descInfo['newVal'] = '%s%%' % str(round(newVal * 100, 1))
                descList.append(descInfo)

            info['descList'] = descList
            if p.totalPvpEnhVal > 0:
                info['state'] = 'free'
                info['usePointHint'] = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_USE_POINT_HINT, '')
                info['point'] = gameStrings.TEXT_PVPENHANCEPROXY_232 % format(p.totalPvpEnhVal, ',')
            else:
                info['state'] = 'normal'
            itemId = SCD.data.get('pvpEnhanceItemId', 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['count'] = '%d' % p.inv.countItemInPages(itemId, enableParentCheck=True)
            if itemInfo['count'] == '0':
                itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
            else:
                itemInfo['state'] = uiConst.ITEM_NORMAL
            info['itemInfo'] = itemInfo
            allNum = p.remainFreePvpEnhNum + p.remainCostPvpEnhNum
            if allNum <= 0:
                color = '#F43804'
            else:
                color = '#FFCC33'
            maxFreePvpEnhTimes = SCD.data.get('maxFreePvpEnhTimes', 0)
            info['canUseTimes'] = gameStrings.TEXT_PVPENHANCEPROXY_252 + uiUtils.toHtml('%d/%d' % (allNum, maxFreePvpEnhTimes), color)
            info['canUseTimesTips'] = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_CAN_USE_TIMES_HINT, '%d%d') % (allNum, maxFreePvpEnhTimes)
            info['addTimesBtnTips'] = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_ADD_TIMES_BTN_HINT, '%d%d') % (allNum, maxFreePvpEnhTimes)
            info['speedUpText'] = gameStrings.CATCH_UP_PROXY_BTN_TEXT
            weekDiff = uiUtils.getCatchUpWeekDiff('pvpInterval')
            targetExp = PPED.data.get(weekDiff, {}).get('standard', 0)
            info['showSpeedUp'] = False
            if gameglobal.rds.configData.get('enablePursuePvp', False) and targetExp != 0:
                info['showSpeedUp'] = True
            self.mediator.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def calcCurLv(self, eType, school, exp, limitLv):
        lvMax = PEDD.data.get((eType, school), {}).get('lvMax', 0)
        for lv in range(1, lvMax + 1):
            if exp < PELD.data.get((lv, eType, school), {}).get('exp', 0):
                return min(limitLv, lv - 1)

        return min(limitLv, lvMax)

    def getCurExpAndLimitLv(self, eType, school):
        singlePvpEnhance = self.pvpEnhance.get(school)
        if eType == const.PVP_ENHANCE_TYPE_ATK:
            curExp = singlePvpEnhance[0] if singlePvpEnhance else 0
            limitLv = singlePvpEnhance[1] if singlePvpEnhance else 0
        else:
            curExp = singlePvpEnhance[2] if singlePvpEnhance else 0
            limitLv = singlePvpEnhance[3] if singlePvpEnhance else 0
        return (curExp, limitLv)

    def canLvUp(self, eType, school):
        curExp, limitLv = self.getCurExpAndLimitLv(eType, school)
        lvMax = PEDD.data.get((eType, school), {}).get('lvMax', 0)
        if limitLv >= lvMax:
            limitLv = lvMax - 1
        return curExp >= PELD.data.get((limitLv + 1, eType, school), {}).get('exp', 0)

    def onReset(self, *arg):
        p = BigWorld.player()
        resetNum = p.resetPvpEnhWeekly + 1
        pd = PERCD.data.get(resetNum)
        if not pd:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_RESET_ERROR_NO_TIMES, ())
            return
        btnEnabled = True
        itemId = pd.get('itemNeed', 0)
        needNum = pd.get('itemNum', 0)
        if itemId != 0 and needNum != 0:
            itemInfo = uiUtils.getGfxItemById(itemId)
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if ownNum < needNum:
                itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                btnEnabled = False
            else:
                itemInfo['count'] = '%d/%d' % (ownNum, needNum)
        else:
            itemInfo = {}
        cash = pd.get('cash', 0)
        if cash != 0:
            if p.cash < cash:
                cashVal = uiUtils.toHtml(format(cash, ','), '#F43804')
                btnEnabled = False
            else:
                cashVal = format(cash, ',')
            bonusInfo = {'bonusType': 'cash',
             'value': cashVal}
        else:
            bonusInfo = {}
        if itemInfo or bonusInfo:
            msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_RESET_HINT, '%d%d') % (resetNum, len(PERCD.data) - resetNum)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_RESET_ENPTY_HINT, '%d%d') % (resetNum, len(PERCD.data) - resetNum)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.resetPvpEnhance, itemData=itemInfo, bonusIcon=bonusInfo, yesBtnEnable=btnEnabled)

    def resetSuccess(self, value):
        msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_RESET_SUCCESS_HINT, '%s') % format(value, ',')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def onAddTimes(self, *arg):
        p = BigWorld.player()
        if p.addRemainPvpEnhTimes >= SCD.data.get('maxAddRemainPvpEnhTimes', 5):
            p.showGameMsg(GMDD.data.ADD_PVP_TIMES_FAILED_LIMIT, ())
            return
        pd = PETCD.data.get(p.addRemainPvpEnhTimes + 1)
        if not pd:
            return
        maxCostNum = SCD.data.get('PVP_ENHANCE_MAX_COST_NUM', 600)
        if gameglobal.rds.configData.get('enablePvpEnhanceMaxCostNum', False) and p.remainCostPvpEnhNum >= maxCostNum:
            p.showGameMsg(GMDD.data.ADD_PVP_TIMES_FAILED, ())
            return
        btnEnabled = True
        itemId = pd.get('itemNeed', 0)
        needNum = pd.get('itemNum', 0)
        itemInfo = uiUtils.getGfxItemById(itemId)
        ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if ownNum < needNum:
            itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
            btnEnabled = False
        else:
            itemInfo['count'] = '%d/%d' % (ownNum, needNum)
            itemInfo['state'] = uiConst.ITEM_NORMAL
        cash = pd.get('cash', 0)
        if cash != 0:
            if p.cash < cash:
                cashVal = uiUtils.toHtml(format(cash, ','), '#F43804')
                btnEnabled = False
            else:
                cashVal = format(cash, ',')
            bonusInfo = {'bonusType': 'cash',
             'value': cashVal}
        else:
            bonusInfo = {}
        addedCostNum = p.remainCostPvpEnhNum + SCD.data.get('costPvpEnhNumDelta', 50)
        if gameglobal.rds.configData.get('enablePvpEnhanceMaxCostNum', False) and addedCostNum > maxCostNum:
            msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_OVER_MAX_HINT, '%d%d%d') % (maxCostNum, maxCostNum - p.remainCostPvpEnhNum, p.addRemainPvpEnhTimes + 1)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_ADD_TIMES_HINT, '%d') % (p.addRemainPvpEnhTimes + 1)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.addPvpEnhTimes, itemData=itemInfo, bonusIcon=bonusInfo, yesBtnEnable=btnEnabled)

    def onUseBind(self, *arg):
        eType = int(arg[3][0].GetNumber())
        school = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if self.canLvUp(eType, school):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_ENOUGH_EXP, ())
            return
        if p.remainFreePvpEnhNum + p.remainCostPvpEnhNum <= 0:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_NO_NUM, ())
            return
        itemId = SCD.data.get('pvpEnhanceItemId', 0)
        itemBindNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=True)
        if itemBindNum <= 0:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_NO_BIND_ITEM, ())
            return
        itemNum = min(itemBindNum, p.remainFreePvpEnhNum + p.remainCostPvpEnhNum)
        p.cell.addPvpEnh(school, eType, itemId, itemNum, 0)

    def onUseAll(self, *arg):
        eType = int(arg[3][0].GetNumber())
        school = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if self.canLvUp(eType, school):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_ENOUGH_EXP, ())
            return
        if p.remainFreePvpEnhNum + p.remainCostPvpEnhNum <= 0:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_NO_NUM, ())
            return
        itemId = SCD.data.get('pvpEnhanceItemId', 0)
        itemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if itemNum <= 0:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_NO_ITEM, ())
            return
        itemNum = min(itemNum, p.remainFreePvpEnhNum + p.remainCostPvpEnhNum)
        expDelta = ID.data.get(itemId).get('pvpEnhExp', 0)
        if expDelta <= 0:
            return
        curExp, limitLv = self.getCurExpAndLimitLv(eType, school)
        if limitLv == PEDD.data.get((eType, school), {}).get('lvMax', 0):
            limitLv -= 1
        exp = PELD.data.get((limitLv + 1, eType, school), {}).get('exp', 0)
        if exp <= curExp:
            return
        tNum = int(math.ceil((exp - curExp) * 1.0 / expDelta))
        itemNum = min(itemNum, tNum)
        p.cell.addPvpEnh(school, eType, itemId, itemNum, 1)

    def onUsePoint(self, *arg):
        eType = int(arg[3][0].GetNumber())
        school = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if self.canLvUp(eType, school):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_ENOUGH_EXP, ())
            return
        curExp, limitLv = self.getCurExpAndLimitLv(eType, school)
        skillLv = self.calcCurLv(eType, school, curExp, limitLv)
        val = max(PELD.data.get((skillLv + 1, eType, school), {}).get('exp', 0) - curExp, 0)
        val = min(val, p.totalPvpEnhVal)
        msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_ASSIGN_POINT_HINT, gameStrings.TEXT_PVPENHANCEPROXY_456) % format(val, ',')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.assignPvpEnhVal, school, eType, val))

    def onLvUp(self, *arg):
        eType = int(arg[3][0].GetNumber())
        school = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        curExp, limitLv = self.getCurExpAndLimitLv(eType, school)
        pd = PELD.data.get((limitLv + 1, eType, school))
        if not pd:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_LVUP_ERROR_NO_NEXT_LV, ())
            return
        if curExp < pd.get('exp', 0):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_LVUP_ERROR_NO_ENOUGH_EXP, ())
            return
        lvLimit = pd.get('lvLimit', 0)
        if p.realLv <= lvLimit:
            p.showGameMsg(GMDD.data.PVP_ENHANCE_LVUP_ERROR_PLAYER_LV, (lvLimit,))
            return
        btnEnabled = True
        itemList = []
        for itemId, needNum in pd.get('itemNeed', []):
            itemInfo = uiUtils.getGfxItemById(itemId)
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if ownNum < needNum:
                itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                btnEnabled = False
            else:
                itemInfo['count'] = '%d/%d' % (ownNum, needNum)
            itemList.append(itemInfo)

        cash = pd.get('cash', 0)
        if p.cash < cash:
            cashVal = uiUtils.toHtml(format(cash, ','), '#F43804')
            btnEnabled = False
        else:
            cashVal = format(cash, ',')
        bonusInfo = {'bonusType': 'cash',
         'value': cashVal}
        msg = uiUtils.getTextFromGMD(GMDD.data.PVP_ENHANCE_LVUP_HINT, gameStrings.TEXT_PVPENHANCEPROXY_500)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.activatePvpEnhLv, school, eType), itemData=itemList, bonusIcon=bonusInfo, yesBtnEnable=btnEnabled)

    def onSpeedUp(self, *args):
        eType = int(args[3][0].GetNumber())
        school = int(args[3][1].GetNumber())
        if gameglobal.rds.ui.pvpMasteryCatchUp.widget:
            gameglobal.rds.ui.pvpMasteryCatchUp.hide()
        else:
            gameglobal.rds.ui.pvpMasteryCatchUp.show(school, eType)

    def onShowPvpMasteryCatchUp(self, *args):
        show = args[3][0].GetBool()
        if show:
            p = BigWorld.player()
            maxPursuePvpEnhNum = p.maxPursuePvpEnhNum
            if maxPursuePvpEnhNum != 0:
                gameglobal.rds.ui.pvpMasteryCatchUp.show(self.school, self.eType)
            else:
                gameglobal.rds.ui.pvpMasteryCatchUp.hide()
        else:
            gameglobal.rds.ui.pvpMasteryCatchUp.hide()

    def getPvpEnhanceList(self):
        return self.pvpEnhance
