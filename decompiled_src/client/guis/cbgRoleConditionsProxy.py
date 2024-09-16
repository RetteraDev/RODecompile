#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgRoleConditionsProxy.o
import BigWorld
import sys
import gameglobal
import uiConst
import events
import copy
from uiProxy import UIProxy
from asObject import ASObject
from guis import cbgUtils
from gamestrings import gameStrings
from data import region_server_config_data as RSCD
from data import cbg_config_data as CCD
import gamelog

class CbgRoleConditionsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgRoleConditionsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_ROLE_CONDITIONS, self.hide)

    def reset(self):
        self.conditionType = cbgUtils.CBG_CONDITION_TYPE_REGIST

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_ROLE_CONDITIONS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_ROLE_CONDITIONS)
        self.reset()

    def show(self, type):
        if type not in (cbgUtils.CBG_CONDITION_TYPE_REGIST, cbgUtils.CBG_CONDITION_TYPE_SALE):
            return
        self.conditionType = type
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_ROLE_CONDITIONS, True)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.conditions.itemRenderer = 'CBGCondition_ListItemRenderer'
        self.widget.conditions.dataArray = []
        self.widget.conditions.lableFunction = self.renderConditionItem
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.ruleHelper.addEventListener(events.MOUSE_CLICK, self.handleRuleHelperClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.conditionType == cbgUtils.CBG_CONDITION_TYPE_REGIST:
            self.widget.title.txt.text = gameStrings.CBG_CONDITION_TITLE_REGIST
            self.widget.ruleHelper.textField.htmlText = gameStrings.CBG_SELL_REGIST_RULE_TEXT
        elif self.conditionType == cbgUtils.CBG_CONDITION_TYPE_SALE:
            self.widget.title.txt.text = gameStrings.CBG_CONDITION_TITLE_SALE
            self.widget.ruleHelper.textField.htmlText = gameStrings.CBG_SELL_SELL_RULE_TEXT
        p = BigWorld.player()
        self.widget.roleName.text = p.roleName
        self.widget.level.text = str(p.lv)
        self.widget.serverName.text = RSCD.data.get(p.getOriginHostId(), {}).get('serverName', '')
        if not gameglobal.rds.configData.get('cbgRolePassConditions', False) and not self._isAllConditionOk():
            self.widget.confirmBtn.enabled = False
        else:
            self.widget.confirmBtn.enabled = True
        listArr = self._genConditionListData()
        self.widget.conditions.dataArray = listArr

    def renderConditionItem(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.conformity.visible = data.isConformity
        item.inconformity.visible = not data.isConformity
        if data.helper < 0:
            item.helper.visible = False
        else:
            item.helper.visible = True
            item.helper.helpKey = data.helper
        item.desc.text = data.desc

    def handleConfirmBtnClick(self, *args):
        if self.conditionType == cbgUtils.CBG_CONDITION_TYPE_REGIST:
            gameglobal.rds.ui.cbgMain.onRegistConditionsConfirm()
        elif self.conditionType == cbgUtils.CBG_CONDITION_TYPE_SALE:
            gameglobal.rds.ui.cbgMain.onSellConditionsConfirm()
        self.hide()

    def handleRuleHelperClick(self, *args):
        gamelog.debug('ypc@ handleRuleHelperClick!')
        if self.conditionType == cbgUtils.CBG_CONDITION_TYPE_REGIST:
            gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_REGIST_SIMPLE)
        elif self.conditionType == cbgUtils.CBG_CONDITION_TYPE_SALE:
            gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_SALE_SIMPLE)

    def __isConditionOk(self, cidx):
        conditions = gameglobal.rds.ui.cbgMain.getConditionByType(self.conditionType)
        ret = True
        if type(cidx) is tuple:
            for i in cidx:
                ret = ret and i in conditions and not not conditions[i]

        else:
            ret = ret and cidx in conditions and not not conditions[cidx]
        return ret

    def _isAllConditionOk(self):
        conditions = gameglobal.rds.ui.cbgMain.getConditionByType(self.conditionType)
        for c in conditions.values():
            if not c:
                return False

        return True

    def _genConditionListData(self):
        conditionDesc = []
        if self.conditionType == cbgUtils.CBG_CONDITION_TYPE_SALE:
            conditionDesc = copy.deepcopy(CCD.data.get('roleSaleConditions', []))
        elif self.conditionType == cbgUtils.CBG_CONDITION_TYPE_REGIST:
            conditionDesc = copy.deepcopy(CCD.data.get('roleRegistConditions', []))
        listArr = []
        for i in xrange(len(conditionDesc)):
            desc, conditionIndex, helper = conditionDesc[i]
            isOk = self.__isConditionOk(conditionIndex)
            listArr.append({'desc': desc,
             'helper': helper,
             'isConformity': isOk})

        return listArr
