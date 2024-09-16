#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/sidiGuideProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from data import challenge_mission_data as CMD
from data import state_data as SD
from data import sys_config_data as SCD
from guis.asObject import TipManager
from guis import tipUtils
LIFE_MAX_COUNT = 3
BUFF_MAX_COUNT = 3
TYPE_NORMAL = 1

class SidiGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SidiGuideProxy, self).__init__(uiAdapter)
        self.widget = None
        self.frameInfo = {}
        self.frameInfo['number'] = 0
        self.frameInfo['title'] = ''
        self.frameInfo['life'] = 3
        self.frameInfo['buffList'] = [0, 0, 0]
        self.frameInfo['scoreList'] = [0, 0, 0]
        self.frameInfo['hideConditon'] = False
        self.frameInfo['content'] = ''
        self.frameInfo['succ'] = False
        self.frameInfo['missonId'] = 0
        self.isOnMission = False
        self.autoClose = False

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self):
        p = BigWorld.player()
        if getattr(p, 'mapID', 0) in SCD.data.get('sidiFubenList', []):
            self.uiAdapter.loadWidget(uiConst.WIDGET_SIDI_GUIDE)

    def clearWidget(self):
        self.widget = None
        if not self.isOnMission:
            self.cleanData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SIDI_GUIDE)

    def cleanData(self):
        self.frameInfo = {}
        self.frameInfo['number'] = 0
        self.frameInfo['title'] = ''
        self.frameInfo['life'] = 3
        self.frameInfo['buffList'] = [0, 0, 0]
        self.frameInfo['scoreList'] = [0, 0, 0]
        self.frameInfo['hideConditon'] = False
        self.frameInfo['content'] = ''
        self.frameInfo['succ'] = False
        self.frameInfo['missonId'] = 0

    def refreshFrame(self):
        if not self.widget:
            return
        missionType = CMD.data.get(self.frameInfo['missonId'], {}).get('type', 0)
        widget = self.widget
        self.widget.num.visible = missionType == TYPE_NORMAL
        widget.num.text = str(self.frameInfo['number'])
        widget.title.text = str(self.frameInfo['title'])
        self._updateLife()
        self._updateBuff()
        self._updateScore()
        self._setHide()
        widget.content.text = self.frameInfo['content']
        widget.success.visible = self.frameInfo['succ']
        if self.frameInfo['succ']:
            widget.success.gotoAndPlay(1)

    def _updateLife(self):
        for i in range(LIFE_MAX_COUNT):
            name = 'life%d' % i
            mc = self.widget.getChildByName(name)
            if i < self.frameInfo['life']:
                mc.gotoAndStop('light')
            else:
                mc.gotoAndStop('dislight')

    def _updateBuff(self):
        life = self.frameInfo['life']
        if life == 3:
            self._setBuff(self.widget.buff0, self.frameInfo['buffList'][0], False)
            self._setBuff(self.widget.buff1, self.frameInfo['buffList'][1], False)
            self._setBuff(self.widget.buff2, self.frameInfo['buffList'][2], False)
        elif life == 2:
            self._setBuff(self.widget.buff0, self.frameInfo['buffList'][0], True)
            self._setBuff(self.widget.buff1, self.frameInfo['buffList'][1], False)
            self._setBuff(self.widget.buff2, self.frameInfo['buffList'][2], False)
        else:
            self._setBuff(self.widget.buff0, self.frameInfo['buffList'][0], True)
            self._setBuff(self.widget.buff1, self.frameInfo['buffList'][1], True)
            self._setBuff(self.widget.buff2, self.frameInfo['buffList'][2], True)

    def _setBuff(self, mc, buffId, enabled):
        data = {}
        cfg = SD.data.get(buffId, {})
        iconId = cfg.get('iconId', 'notFound')
        data['iconPath'] = 'state/22/%s.dds' % iconId
        mc.setItemSlotData(data)
        if not enabled:
            mc.setSlotState(uiConst.EQUIP_NOT_USE)
        else:
            mc.setSlotState(uiConst.ITEM_NORMAL)
        mc.validateNow()
        mc.dragable = False
        TipManager.addTipByType(mc, tipUtils.TYPE_BUFF, buffId)

    def _updateScore(self):
        self.widget.baseScore.text = str(self.frameInfo['scoreList'][0])
        self.widget.timeScore.text = str(self.frameInfo['scoreList'][1])
        self.widget.hideScore.text = str(self.frameInfo['scoreList'][2])

    def _setHide(self):
        self.widget.hide1.visible = self.frameInfo['hideConditon']
        if self.frameInfo['hideConditon']:
            self.widget.hide1.gotoAndPlay(1)
        self.widget.hide0.gotoAndPlay(1)

    def _initUI(self):
        self.widget.success.visible = False
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick)

    def onCloseClick(self, *args):
        self.autoClose = True
        self.hide()

    def sendFubenVars(self, fbNo, stage, info):
        if info.has_key('sidi_live'):
            self.frameInfo['life'] = info.get('sidi_live')
        if info.has_key('encrg1'):
            self.frameInfo['buffList'][0] = info.get('encrg1')
        if info.has_key('encrg2'):
            self.frameInfo['buffList'][1] = info.get('encrg2')
        if info.has_key('encrg3'):
            self.frameInfo['buffList'][2] = info.get('encrg3')
        self.refreshFrame()

    def missionStart(self, iNormalMission, missionId):
        self.frameInfo['missonId'] = missionId
        self.frameInfo['succ'] = False
        self.frameInfo['number'] = iNormalMission
        data = CMD.data.get(missionId, {})
        self.frameInfo['title'] = data.get('name', '')
        self.frameInfo['content'] = data.get('missionTip', '')
        self.frameInfo['scoreList'] = [0, 0, 0]
        self.frameInfo['hideConditon'] = False
        if not self.isOnMission:
            self.isOnMission = True
            gameglobal.rds.ui.topBar.refreshTopBarWidgets()
            self.show()
            return
        if self.autoClose:
            self.hide()
            return

    def missionEnd(self, iNormalMisson, missionId, baseScore, timeScore, extraScore, succ):
        if not self.isOnMission:
            self.isOnMission = True
            gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.frameInfo['missonId'] = missionId
        self.frameInfo['number'] = iNormalMisson
        data = CMD.data.get(missionId, {})
        self.frameInfo['title'] = data.get('name', '')
        self.frameInfo['content'] = data.get('missionTip', '')
        self.frameInfo['succ'] = succ
        scoreList = []
        scoreList.extend([baseScore, timeScore, extraScore])
        self.frameInfo['scoreList'] = scoreList
        self.frameInfo['hideConditon'] = extraScore > 0
        if not self.widget:
            self.show()
        else:
            self.refreshFrame()

    def missionAllEnd(self):
        self.isOnMission = False
        self.hide()

    def missionRestart(self, missionId):
        self.missionStart(0, missionId)
