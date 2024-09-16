#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/findBeastRecoverProxy.o
import BigWorld
import const
import gameglobal
import gametypes
import uiConst
import uiUtils
import events
import utils
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from copy import copy
from data import push_data as PMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import mall_config_data as MCD
from data import mall_item_data as MID
MSG = [gameStrings.FINDBEAST_RECOVER_TYPE0, gameStrings.FINDBEAST_RECOVER_TYPE1, gameStrings.FINDBEAST_RECOVER_TYPE2]
MAX_FAME_NEED = 99999999
FIRST_RECOVER_TYPE = 0
SECOND_RECOVER_TYPE = 1
THIRD_RECOVER_TYPE = 2
MAX_TYPE = 3
COST_FAME_TYPE_DISHE = 0
COST_FMAE_TYPE_YUNCHUI = 1
COLOR_GRAY = '#B2B2B2'
COLOR_RED = '#FF0000'
LABEL_YPOS = [[],
 [171],
 [158, 184],
 [149, 171, 193]]

class FindBeastRecoverProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FindBeastRecoverProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIND_BEAST_RECOVER, self.hide)
        self.widget = None
        self.radioBtns = None
        self.isShowByClickPush = False
        self.isPushed = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIND_BEAST_RECOVER:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget.raduiBtns = None
        self.widget = None
        self.isShowByClickPush = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIND_BEAST_RECOVER)

    def show(self, isShowByClickPush = False):
        if gameglobal.rds.configData.get('enableRewardRecoveryClient', False):
            self.uiAdapter.welfare.show(uiConst.WELFARE_TAB_REWARD_RECOVERY)
            return
        self.isShowByClickPush = isShowByClickPush
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIND_BEAST_RECOVER)

    def initUI(self):
        self.widget.addEventListener(events.EVENT_TEXTLINK, self.handleTextLink, False, 0, True)
        self.radioBtns = [self.widget.radioBtn0, self.widget.radioBtn1, self.widget.radioBtn2]
        self.radioInfos = [self.widget.infoTextField0, self.widget.infoTextField1, self.widget.infoTextField2]
        self.initText()
        self.relayout()
        self.initLabelAndConfirmBtn()

    def initText(self):
        p = BigWorld.player()
        chain = p.questLoopChain.getChain()
        exp = chain.calcHistoryExp(p) if chain is not None else 0
        self.widget.expTextField.text = str(exp)
        vipFristPackageId = MID.data.get(MCD.data.get('vipFirstBuyBasicPackage', 0), {}).get('packageID', -1)
        vipBasicPackageId = MID.data.get(MCD.data.get('vipBasicPackage', 0), {}).get('packageID', -1)
        superExpPackageId = MID.data.get(MCD.data.get('vipValues', {}).get('value')[0], {}).get('packageID', -1)
        nowTime = utils.getNow()
        hasVipFirstBuyPackage = p.vipBasicPackage.get('packageID') == vipFristPackageId and p.vipBasicPackage.get('tExpire', 0) > nowTime
        hasVipBasicPackage = p.vipBasicPackage.get('packageID') == vipBasicPackageId and p.vipBasicPackage.get('tExpire', 0) > nowTime
        hasVipSuperExpPackage = p.vipAddedPackage.get(superExpPackageId, {}).get('tExpire', 0) > nowTime
        if hasVipFirstBuyPackage or hasVipSuperExpPackage:
            hintText = gameStrings.FINDBEAST_RECOVER_HINTTEXT_SUPEREXP
        elif hasVipBasicPackage:
            hintText = gameStrings.FINDBEAST_RECOVER_HINTTEXT_BASIC
        else:
            hintText = gameStrings.FINDBEAST_RECOVER_HINTTEXT_NONE
        self.widget.hintTextField.text = hintText

    def initLabelAndConfirmBtn(self):
        self.widget.confirmBtn.enabled = False
        firstEnable = -1
        for i in xrange(len(self.radioBtns)):
            if not self.radioBtns[i].visible:
                continue
            isEnable, label = self.getTypeInfo(i)
            self.radioBtns[i].enabled = isEnable
            self.radioInfos[i].htmlText = label
            if firstEnable == -1 and isEnable:
                firstEnable = i

        self.radioBtns[firstEnable].selected = True
        self.widget.confirmBtn.enabled = firstEnable != -1

    def getTypeInfo(self, t):
        p = BigWorld.player()
        chain = p.questLoopChain.getChain()
        if chain is None:
            return
        else:
            if t == FIRST_RECOVER_TYPE:
                needToken = chain.calcGetBackFreeCnt(p)
                ownToken = chain.getBackFreeCnt
            elif t == SECOND_RECOVER_TYPE:
                ret = chain.calcGetBackConsumeFame(p, COST_FAME_TYPE_DISHE)
                needToken = ret[0][1] if ret else MAX_FAME_NEED
                ownToken = BigWorld.player().getFame(const.DI_SHE_GONG_XUN_FAME_ID)
            elif t == THIRD_RECOVER_TYPE:
                ret = chain.calcGetBackConsumeFame(p, COST_FMAE_TYPE_YUNCHUI)
                needToken = ret[0][1] if ret else MAX_FAME_NEED
                ownToken = BigWorld.player().getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            isEnable = needToken <= ownToken
            ownToken = ownToken if isEnable else uiUtils.toHtml(ownToken, COLOR_RED)
            label = MSG[t] % (needToken, ownToken)
            label = label if isEnable else uiUtils.toHtml(label, COLOR_GRAY)
            return (isEnable, label)

    def pushFindBeastRecoverMsg(self):
        if gameglobal.rds.configData.get('enableRewardRecoveryClient', False):
            return
        elif self.isPushed:
            return
        else:
            self.isPushed = True
            pushMsg = gameglobal.rds.ui.pushMessage
            p = BigWorld.player()
            chain = p.questLoopChain.getChain()
            recoverExp = chain.calcHistoryExp(p) if chain is not None else 0
            if recoverExp == 0:
                pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER)
            else:
                callBackDict = {'click': Functor(self.show, True)}
                pushMsg.setCallBack(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER, callBackDict)
                pmd = PMD.data.get(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER, {})
                msgInfo = {'iconId': pmd.get('iconId', 0),
                 'tooltip': pmd.get('tooltip')}
                pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER, msgInfo=msgInfo)
            return

    def _onCloseBtnClick(self, e):
        if self.isShowByClickPush:
            BigWorld.player().showGameMsg(GMDD.data.FIND_BEAST_RECOVER_CANCEL_NOTIFY, ())
        self.hide()

    def _onConfirmBtnClick(self, e):
        for idx, radioBtn in enumerate(self.radioBtns):
            if radioBtn.selected:
                recoverType = gametypes.QUEST_LOOP_CHAIN_GET_BACK_EXP_TYPE[idx]
                BigWorld.player().cell.getBackQuestLoopChainExp(recoverType)

        self.hide()

    def _onCancelBtnClick(self, e):
        if self.isShowByClickPush:
            BigWorld.player().showGameMsg(GMDD.data.FIND_BEAST_RECOVER_CANCEL_NOTIFY, ())
        self.hide()

    def clearAll(self):
        self.isPushed = False

    def resetPushed(self):
        self.isPushed = False

    def relayout(self):
        params = SCD.data.get('questLoopChainGetBackExp')
        if params is None:
            return
        else:
            p = BigWorld.player()
            labelsVisible = [ param[0] <= p.lv <= param[1] for param in params ]
            len(labelsVisible) == 4 and labelsVisible.pop(3)
            labelsVisible[0] = False
            visibleLabelCnt = labelsVisible.count(True)
            labelsYPos = copy(LABEL_YPOS[visibleLabelCnt])
            for idx, v in enumerate(labelsVisible):
                self.radioBtns[idx].visible = v
                self.radioInfos[idx].visible = v
                if not v:
                    continue
                self.radioBtns[idx].y = labelsYPos.pop(0)
                self.radioInfos[idx].y = self.radioBtns[idx].y

            return

    def handleTextLink(self, *args):
        self.uiAdapter.roleInfo.show(uiConst.ROLEINFO_TAB_HONOR, subItem=const.DI_SHE_GONG_XUN_FAME_ID)

    def removeFindBeastRecoverMsg(self, fromConfig = False):
        pushMsg = gameglobal.rds.ui.pushMessage
        if fromConfig:
            pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER)
            self.resetPushed()
            return
        else:
            p = BigWorld.player()
            chain = p.questLoopChain.getChain()
            recoverExp = chain.calcHistoryExp(p) if chain is not None else 0
            if recoverExp == 0:
                pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_FIND_BEAST_RECOVER)
            return
