#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/vehicleChooseProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import ui
import utils
import gametypes
import const
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import zaiju_data as ZD
from data import skill_general_template_data as SGTD
from data import skill_general_data as SGD
from data import duel_config_data as DCD
from data import skill_client_data as SD
from cdata import game_msg_def_data as GMDD
ROLE_COUNT = 4
SKILL_COUNT_MAX = 3
SIDE_STR_COLOR = '#e59545'

class VehicleChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VehicleChooseProxy, self).__init__(uiAdapter)
        self._resetData()
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_VEHICLE_CHOOSE, self.onCloseClick)
        self.lastCloseTime = 0

    def _resetData(self):
        self.widget = None
        self.roleList = []
        self.sideIndex = 0
        self.selectedRoleMc = None
        self.roleDataList = []
        self.skillMcList = []
        self.exitTime = None
        self.autoClose = True
        self.oldState = gametypes.BIANSHEN_HUMAN

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        p = BigWorld.player()
        self.oldState = p.bianshen[0]
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self._initUI()
        self.refreshFrame()

    @ui.callInCD(2)
    def show(self, autoClose = True):
        self.autoClose = autoClose
        self.sideIndex = BigWorld.player().bfSideIndex
        self.uiAdapter.loadWidget(uiConst.WIDGET_VEHICLE_CHOOSE, isModal=True)

    def setExitTime(self, exitTime):
        self.exitTime = exitTime

    def clearWidget(self):
        self.lastCloseTime = utils.getNow()
        BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VEHICLE_CHOOSE)

    def refreshFrame(self):
        if not self.widget:
            return
        self._getFrameData()
        sideStr = DCD.data.get('side_tips', {}).get(self.sideIndex, '')
        colorStr = uiUtils.toHtml(sideStr, SIDE_STR_COLOR)
        self.widget.title.htmlText = gameStrings.VEHICLE_CHOOSE_PROXY_TITLE % colorStr
        self.widget.tips.text = DCD.data.get('side_des', {}).get(self.sideIndex, '')
        self.roleList = []
        for i in xrange(ROLE_COUNT):
            roleMc = self.widget.roles.getChildByName(('role%d' if self.sideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX else 'roleSprite%d') % i)
            self.roleList.append(roleMc)
            roleMc.fixedSize = True
            roleMc.name0.text = self.roleDataList[i]['name'][0:4]
            roleMc.name1.text = self.roleDataList[i]['name'][4:]
            roleMc.addEventListener(events.EVENT_SELECT, self.onRoleFrameChange, False, 0, True)
            roleMc.addEventListener(events.MOUSE_CLICK, self.onRoleClick, False, 0, True)
            roleMc.addEventListener(events.MOUSE_CLICK, self.onRoleFrameChange, False, 0, True)
            roleMc.addEventListener(events.MOUSE_ROLL_OVER, self.onRoleFrameChange, False, 0, True)
            roleMc.addEventListener(events.MOUSE_ROLL_OUT, self.onRoleFrameChange, False, 0, True)

        self.addTick()
        index = self.getSelectedIndex()
        self.selectRole(index)

    def addTick(self):
        if not self.widget:
            return
        self.updateTick()

    def updateTick(self):
        self.timer = None
        if not self.widget:
            return
        elif self.oldState != BigWorld.player().bianshen[0]:
            self.hide()
            return
        else:
            if self.exitTime:
                leftTime = self.exitTime - utils.getNow()
                leftTime = max(0, leftTime)
                if leftTime == 0:
                    self.widget.count.text = gameStrings.TEXT_VEHICLECHOOSEPROXY_123
                    self.widget.desc0.htmlText = DCD.data.get('HUNT_OVER_TIME_DES', '')
                else:
                    self.widget.count.text = gameStrings.TEXT_UIUTILS_1821 % leftTime
                    self.widget.desc0.htmlText = DCD.data.get('HUNT_CONT_DOWN_DES', '')
                if self.autoClose and leftTime == 0:
                    self.onSureClick()
                    return
            else:
                self.widget.count.text = gameStrings.TEXT_VEHICLECHOOSEPROXY_123
                self.widget.desc0.htmlText = DCD.data.get('HUNT_OVER_TIME_DES', '')
            self.timer = BigWorld.callback(0.5, self.updateTick)
            return

    def selectRole(self, roleIndex):
        for i in range(len(self.roleList)):
            self.roleList[i].selected = i == roleIndex

        if roleIndex >= len(self.roleDataList):
            return
        for skillMc in self.skillMcList:
            skillMc.gotoAndStop('nothing')

        skillInfo = self.roleDataList[roleIndex].get('skillInfo', [])
        skillLen = len(skillInfo)
        for i in xrange(skillLen):
            skillMc = self.skillMcList[i]
            skillMc.gotoAndStop('skill')
            skillData = skillInfo[i]
            skillMc.txtName.text = skillData['name']
            skillMc.skillIcon.setItemSlotData(skillData)
            skillMc.skillIcon.dragable = False
            skillMc.skillIcon.validateNow()
            TipManager.addTipByType(skillMc.skillIcon, tipUtils.TYPE_SKILL, skillData['id'])
            skillMc.txtDesc.text = skillData['describe']
            skillMc.txtCD.text = skillData['cd']
            skillMc.txtCost.text = skillData['cost']
            skillMc.txtCost.visible = self.sideIndex != const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX
            skillMc.skillCost.visible = self.sideIndex != const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX
            skillMc.txtDis.text = skillData['dis']

    def _getFrameData(self):
        zaijuTuble = DCD.data.get('side_zaiju_ref', {}).get(self.sideIndex, ())
        for zaijuId in zaijuTuble:
            zaijuData = ZD.data.get(zaijuId, {})
            if not zaijuData:
                continue
            roleInfo = {}
            skillInfo = []
            roleInfo['zaijuId'] = zaijuId
            roleInfo['name'] = zaijuData.get('name', '')
            skills = zaijuData.get('skills', [])
            roleInfo['skillInfo'] = skillInfo
            self.roleDataList.append(roleInfo)
            for i in range(len(skills)):
                if i >= SKILL_COUNT_MAX:
                    break
                info = {}
                skillId, skillLv = skills[i]
                generalData = SGD.data.get((skillId, skillLv), {})
                icon = SD.data.get((skillId, skillLv), {}).get('icon', 0)
                if not icon:
                    icon = SD.data.get((skillId, 1), {}).get('icon', 0)
                generalTemplaeData = SGTD.data.get(skillId, {})
                info['name'] = generalTemplaeData.get('name', '')
                info['describe'] = generalData.get('describe', '')
                cd = generalData.get('cd', 0)
                info['cd'] = uiUtils.formatTime(cd)
                costItem = generalData.get('candyNeed', 0)
                if costItem:
                    info['cost'] = gameStrings.VEHICLE_CHOOSE_PROXY_GIFT % costItem
                else:
                    info['cost'] = gameStrings.VEHICLE_CHOOSE_PROXY_NOTHING
                rangeMin = generalData.get('rangeMin', 0)
                info['dis'] = gameStrings.TEXT_VEHICLECHOOSEPROXY_198 % rangeMin
                info['iconPath'] = 'skill/icon/%d.dds' % icon
                info['id'] = skillId
                skillInfo.append(info)

    def _initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick, False, 0, True)
        for i in xrange(SKILL_COUNT_MAX):
            skillMC = self.widget.getChildByName('skill%d' % i)
            skillMC.gotoAndStop('nothing')
            self.skillMcList.append(skillMC)

        if self.sideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            self.widget.titleIcon.gotoAndStop('protecter')
            self.widget.roles.gotoAndStop('protecter')
        else:
            self.widget.titleIcon.gotoAndStop('sprite')
            self.widget.roles.gotoAndStop('sprite')
        self.widget.btnSure.addEventListener(events.MOUSE_CLICK, self.onSureClick, False, 0, True)

    def onSureClick(self, *args):
        index = self.getSelectedIndex()
        zaijuData = self.roleDataList[index]
        BigWorld.player().cell.enterSpecificZaijuInBFHunt(zaijuData['zaijuId'])
        self.hide()

    def getSelectedIndex(self):
        index = 0
        if self.selectedRoleMc:
            name = self.selectedRoleMc.name
            index = int(name[-1])
        return index

    def onRoleClick(self, *args):
        e = ASObject(args[3][0])
        self.selectedRoleMc = e.currentTarget
        index = self.getSelectedIndex()
        self.selectRole(index)

    def onRoleFrameChange(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.name[-1])
        if index >= len(self.roleDataList):
            return
        data = self.roleDataList[index]['name']
        e.currentTarget.name0.text = data[0:4]
        e.currentTarget.name1.text = data[4:]

    def onCloseClick(self, *args):
        if not BigWorld.player().bianshen[1]:
            BigWorld.player().showGameMsg(GMDD.data.NOT_IN_BIANSHEN_TIPS, ())
        else:
            self.hide()

    def tryOpen(self):
        p = BigWorld.player()
        canOpen = not p.bianshen[1] and not self.widget and p.life == gametypes.LIFE_ALIVE and utils.getNow() - self.lastCloseTime > 2
        if canOpen:
            self.show(False)
