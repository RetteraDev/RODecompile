#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaChooseHeroBottomProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import skillDataInfo
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis import tipUtils
from data import zaiju_data as ZD
from data import duel_config_data as DCD
from cdata import pskill_template_data as PTD
MAX_SKILL_CNT = 5

class BfDotaChooseHeroBottomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaChooseHeroBottomProxy, self).__init__(uiAdapter)
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.skillMcList = []
        self.zaiju2EntityMap = {}
        self.tickTimer = 0
        self.showEntity = None
        self.turnDir = uiConst.MODEL_TURN_STOP
        self.turnSpeed = 0
        self.turnOffset = 0
        self.nowOffset = 0
        self.dstYaw = 0
        self.lastMouseX = 0
        self.lastYaw = 0

    def _registerASWidget(self, widgetId, widget):
        p = BigWorld.player()
        self.widget = widget
        self._initUI()
        self.refreshFrame()
        self.tickFun()

    def show(self):
        if self.widget:
            return
        self.turnSpeed = DCD.data.get('model_turn_speed', 0.0314)
        self.turnOffset = DCD.data.get('model_turn_offset', 0.314)
        self.mouseTurnSpeed = DCD.data.get('model_mouse_turn_speed', 0.005)
        self.uiAdapter.loadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_BOTTOM)

    def clearWidget(self):
        if self.widget:
            self.widget.stage.removeEventListener(events.MOUSE_MOVE, self.handleMouseMove)
            self.widget.stage.removeEventListener(events.MOUSE_DOWN, self.handleMouseDown)
            self.widget.stage.removeEventListener(events.MOUSE_UP, self.handleMouseUp)
        BigWorld.cancelCallback(self.tickTimer)
        gameglobal.PLANE_MODEL = None
        gameglobal.PLANE_MODEL_PARENT_NODE = None
        for zaiuId, entity in self.zaiju2EntityMap.iteritems():
            BigWorld.destroyEntity(entity.id)

        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_BOTTOM)
        p = BigWorld.player()
        gameglobal.rds.loginScene.resetOldCamera()

    def setTurnDir(self, turnDir):
        if self.turnDir != uiConst.MODEL_TURN_STOP:
            if turnDir != self.turnDir:
                self.turnDir == uiConst.MODEL_TURN_STOP
                self.turnOffset = DCD.data.get('model_turn_offset', 0.314)
                return
            self.turnOffset += DCD.data.get('model_turn_offset', 0.314)
        else:
            self.turnOffset = DCD.data.get('model_turn_offset', 0.314)
        self.turnDir = turnDir
        self.nowOffset = 0

    def tickFun(self):
        if not self.widget:
            return
        if self.showEntity and self.turnDir != uiConst.MODEL_TURN_STOP:
            yawPlus = self.turnSpeed if self.turnDir == uiConst.MODEL_TURN_CLOCKWISE else -self.turnSpeed
            self.nowOffset += self.turnSpeed
            if self.nowOffset > self.turnOffset:
                self.turnDir = uiConst.MODEL_TURN_STOP
                self.turnOffset = DCD.data.get('model_turn_offset', 0.314)
            self.showEntity.filter.yaw += yawPlus
        self.tickTimer = BigWorld.callback(0.03, self.tickFun)

    def refreshFrame(self):
        if not self.widget:
            return
        self.widget.mainMc.gotoAndPlay(1)
        self.refreshSkills()
        self.refreshModel()

    def refreshModel(self, event = None):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if not p:
                return
            if event and event.data != p.gbId:
                return
            selfZaijuId = self.uiAdapter.bfDotaChooseHeroRight.chooseHeroId
            if not selfZaijuId:
                return
            entity = self.zaiju2EntityMap.get(selfZaijuId, None)
            if not entity:
                pos = DCD.data.get('bf_dota_hero_positon', p.position)
                faceDir = DCD.data.get('bf_dota_hero_face_dir', (1, 0, 0))
                entityId = BigWorld.createEntity('LoginModel', p.spaceID, 0, pos, faceDir, {})
                entity = BigWorld.entities[entityId]
                self.zaiju2EntityMap[selfZaijuId] = entity
                self.showEntity = entity
            else:
                self.setShowEntity(entity)
            return

    def setShowEntity(self, entity):
        if self.showEntity:
            if self.showEntity.id == entity.id:
                return
            self.showEntity.filter.yaw = DCD.data.get('bf_dota_hero_face_dir', (1, 0, 0))[2]
        self.showEntity = entity
        self.showEntity.refreshOpacity(gameglobal.OPACITY_FULL)

    def refreshSkills(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if not p:
                return
            zaijuId = self.uiAdapter.bfDotaChooseHeroRight.chooseHeroId
            needShowNoneSkills = False
            if not zaijuId:
                needShowNoneSkills = True
            zjd = ZD.data.get(zaijuId, {})
            skills = zjd.get('skills', [])[1:]
            pathList = [ uiUtils.getSkillIconPath(skillDataInfo.ClientSkillInfo(*skill), uiConst.ICON_SIZE64) for skill in skills ]
            pskill = zjd.get('pskills', ((8501, 1),))[0]
            skills.insert(0, pskill)
            pskillIcon = PTD.data.get(pskill[0], {}).get('icon', '')
            pathList.insert(0, uiConst.SKILL_ICON_IMAGE_RES_64 + str(pskillIcon) + '.dds')
            if len(skills) != MAX_SKILL_CNT:
                needShowNoneSkills = True
            if needShowNoneSkills:
                for mc in self.skillMcList:
                    mc.data = None
                    mc.validateNow()
                    return

            for i in xrange(MAX_SKILL_CNT):
                mc = self.skillMcList[i]
                data = {}
                data['iconPath'] = pathList[i]
                mc.data = data
                mc.dragable = False
                mc.validateNow()
                if i:
                    TipManager.addTipByType(mc, tipUtils.TYPE_SKILL, skills[i][0])
                else:
                    TipManager.addTipByType(mc, tipUtils.TYPE_SKILL, {'skillId': skills[i][0],
                     'lv': skills[i][1],
                     'isPSkill': True})

            return

    def _initUI(self):
        p = BigWorld.player()
        if not p:
            return
        self.skillMcList = []
        for i in xrange(MAX_SKILL_CNT):
            mc = self.widget.mainMc.getChildByName('skill%d' % i)
            self.skillMcList.append(mc)

        self.widget.stage.addEventListener(events.MOUSE_DOWN, self.handleMouseDown, False, 0, True)

    def handleMouseDown(self, *args):
        if not self.widget:
            return
        self.lastMouseX = self.widget.mouseX
        if self.showEntity:
            self.lastYaw = self.showEntity.filter.yaw
        self.widget.stage.addEventListener(events.MOUSE_MOVE, self.handleMouseMove, False, 0, True)
        self.widget.stage.addEventListener(events.MOUSE_UP, self.handleMouseUp, False, 0, True)

    def handleMouseUp(self, *args):
        self.widget.stage.removeEventListener(events.MOUSE_MOVE, self.handleMouseMove)
        self.widget.stage.removeEventListener(events.MOUSE_UP, self.handleMouseUp)

    def handleMouseMove(self, *args):
        offsetX = self.widget.mouseX - self.lastMouseX
        if self.showEntity:
            self.showEntity.filter.yaw = self.lastYaw - offsetX * self.mouseTurnSpeed
