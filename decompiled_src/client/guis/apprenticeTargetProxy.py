#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/apprenticeTargetProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import formula
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import asObject
from guis import uiUtils
from asObject import ASObject
from gamestrings import gameStrings
from data import apprentice_new_config_data as ANCD
from data import apprentice_target_data as ATD
from cdata import game_msg_def_data as GMDD

class ApprenticeTargetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ApprenticeTargetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_APPRENTICE_TARGET, self.hide)

    def reset(self):
        self.selectGbId = 0
        self.selectAssigned = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_APPRENTICE_TARGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_APPRENTICE_TARGET)

    def show(self):
        if not gameglobal.rds.configData.get('enableApprenticeTarget'):
            return
        unGraduateGbIds = [ gbId for gbId, isGraduate in BigWorld.player().apprenticeGbIds if not isGraduate ]
        if not unGraduateGbIds:
            BigWorld.player().showGameMsg(GMDD.data.NO_APPENTICE_TO_ASSIGN_TARGET, ())
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_APPRENTICE_TARGET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.targetRefreshDesc.htmlText = ANCD.data.get('targetRefreshDesc')
        self.widget.targetList.itemRenderer = 'ApprenticeTarget_TargetItem'
        self.widget.targetList.column = 2
        self.widget.targetList.itemWidth = 275
        self.widget.targetList.itemHeight = 85
        self.widget.targetList.lableFunction = self.targetListLabelFunc

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        unGraduateGbIds = [ gbId for gbId, isGraduate in p.apprenticeGbIds if not isGraduate ]
        for x in xrange(ANCD.data.get('maxApprenticeNum', 5)):
            btn = self.widget.getChildByName('btn%s' % x)
            btn.visible = x < len(unGraduateGbIds)
            if btn.visible:
                gbId = unGraduateGbIds[x]
                targetInfo = self.getTargetsInfoByGbId(gbId)
                info = self.uiAdapter.mentorEx._getInfoByGbId(gbId)
                btn.label = info.get('name')
                btn.apprenticeVal.text = gameStrings.APPRENTICE_VAL % info.get('apprenticeVal')
                btn.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
                btn.headIcon.fitSize = True
                btn.headIcon.url = info.get('headIcon')
                btn.borderImg.fitSize = True
                btn.borderImg.loadImage(info.get('photoBorderIcon40', ''))
                btn.assignIcon.visible = utils.isSameDay(targetInfo['assignTime'])
                btn.gbId = gbId
                btn.addEventListener(events.BUTTON_CLICK, self.handleApprenticeBtnSelected)
                if x == 0 and self.selectGbId == 0:
                    self.setApprenticeSelected(gbId)

    def setApprenticeSelected(self, gbId):
        self.selectGbId = gbId
        for x in xrange(ANCD.data.get('maxApprenticeNum', 5)):
            btn = self.widget.getChildByName('btn%s' % x)
            if btn:
                btn.selected = btn.gbId and long(btn.gbId) == gbId

        self.refreshTargetsView()

    @staticmethod
    def targetSortedFunc(t1, t2):
        targetProxy = gameglobal.rds.ui.apprenticeTarget
        targetInfo = targetProxy.getTargetsInfoByGbId(targetProxy.selectGbId)
        targets = targetInfo.get('targets').keys()
        vals = [1, 1]
        for i, t in enumerate((t1, t2)):
            if t in targets:
                vals[i] = vals[i] << 1
                if targetInfo.get('targets').get(t):
                    vals[i] = vals[i] << 1

        return cmp(*vals)

    def refreshTargetsView(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            targetsInfo = self.getTargetsInfoByGbId(self.selectGbId)
            rewarded = targetsInfo['rewarded']
            targetIds = targetsInfo['targets']
            self.selectAssigned = utils.isSameDay(targetsInfo['assignTime'])
            cnt = sum(targetIds.values())
            apprenticeTargetRewardCnt = ANCD.data.get('apprenticeTargetRewardCnt', 5)
            finished = cnt >= apprenticeTargetRewardCnt
            self.widget.remindBtn.visible = self.selectAssigned
            self.widget.getRewarBtn.enabled = not rewarded and finished
            for x in xrange(apprenticeTargetRewardCnt):
                finishedIcon = self.widget.getChildByName('finished%s' % x)
                if finishedIcon:
                    finishedIcon.visible = x < cnt

            if self.selectAssigned:
                self.widget.assignTargetTip.htmlText = ANCD.data.get('assignedTargetTip')
                targetList = targetIds.keys()
            else:
                fVal = p.friend.get(self.selectGbId, None)
                lv = fVal.level if fVal else 0
                self.widget.assignTargetTip.htmlText = ANCD.data.get('assignTargetTip')
                targetList = formula.getApprenticeTargetPoolBySeed(p.apprenticeTargetPoolSeed, lv)
            targetList = sorted(targetList, ApprenticeTargetProxy.targetSortedFunc)
            self.widget.targetList.dataArray = targetList
            return

    def targetListLabelFunc(self, *args):
        targetId = args[3][0].GetNumber()
        mc = ASObject(args[3][1])
        mc.validateNow()
        mc.mouseChildren = True
        targetVal = ATD.data.get(targetId)
        targetsInfo = self.getTargetsInfoByGbId(self.selectGbId)
        mc.item.setItemSlotData(uiUtils.getGfxItemById(int(targetVal.get('itemId', 0))))
        mc.item.dragable = False
        mc.label = targetVal.get('name')
        mc.desc.htmlText = targetVal.get('desc')
        mc.assignBtn.data = targetId
        mc.stateIcon.visible = targetId in targetsInfo.get('targets').keys()
        mc.assignBtn.visible = not mc.stateIcon.visible
        if mc.stateIcon.visible:
            finished = targetsInfo.get('targets').get(targetId)
            if finished:
                mc.stateIcon.gotoAndStop('finished')
            else:
                mc.stateIcon.gotoAndStop('assigned')

    def getTargetsInfoByGbId(self, gbId):
        p = BigWorld.player()
        apprenticeTargets = getattr(p, 'apprenticeTargets', {})
        info = {'targets': {},
         'rewarded': False,
         'assignTime': 0}
        if apprenticeTargets.has_key(gbId):
            val = apprenticeTargets[gbId]
            info['targets'] = val[0]
            info['rewarded'] = val[1]
            info['assignTime'] = val[2]
        return info

    def handleApprenticeBtnSelected(self, *args):
        gbId = long(asObject.ASObject(args[3][0]).currentTarget.gbId)
        if self.selectGbId != gbId:
            self.setApprenticeSelected(gbId)

    def _onAssignBtnClick(self, e):
        targetId = e.target.data
        if targetId:
            lv = BigWorld.player().friend.get(self.selectGbId).level
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_ASSIGN_TARGET)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().base.assignApprenticeTarget, self.selectGbId, targetId, lv))

    def _onGetRewarBtnClick(self, e):
        if self.selectGbId:
            BigWorld.player().base.getApprenticeTargetReward(self.selectGbId)

    def _onRemindBtnClick(self, e):
        if self.selectGbId:
            self.uiAdapter.friend.beginChat(self.selectGbId)
