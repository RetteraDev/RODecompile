#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/debugProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import logicInfo
import const
import gametypes
import skillDataInfo
import gamelog
import gameglobal
from gameclass import SkillInfo
from ui import gbk2unicode
from uiProxy import DataProxy
from guis import uiConst
from sfx import sfx
from callbackHelper import Functor
from data import skill_client_data as SD

class DebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(DebugProxy, self).__init__(uiAdapter)
        self.bindType = 'debug'
        self.modelMap = {'clickFuncItem': self.onClickFuncItem,
         'clickDebugSkill': self.onClickDebugSkill,
         'sendSkill': self.onSendSkill,
         'addWushuang': self.addWushuang}
        self.funcMap = [(gameStrings.TEXT_DEBUGPROXY_32, self.onSwitchSummonedSprite),
         (gameStrings.TEXT_DEBUGPROXY_33, self.onSetGroup),
         (gameStrings.TEXT_CONST_5123, self.onSetTeam),
         (gameStrings.TEXT_DEBUGPROXY_35, self.onSetCamp1),
         (gameStrings.TEXT_DEBUGPROXY_36, self.onSetCamp2),
         (gameStrings.TEXT_DEBUGPROXY_37, self.onExitFuben),
         (gameStrings.TEXT_DEBUGPROXY_38, self.onCreateNpcFubenEntry),
         (gameStrings.TEXT_DEBUGPROXY_39, self.onGotoForestSpawnPoint),
         (gameStrings.TEXT_DEBUGPROXY_40, self.onGotoShenci),
         (gameStrings.TEXT_DEBUGPROXY_41, self.onGotoDragon),
         (gameStrings.TEXT_DEBUGPROXY_42, self.onGotoSkillArea),
         (gameStrings.TEXT_DEBUGPROXY_43, self.onGotoSkillShopArea),
         (gameStrings.TEXT_DEBUGPROXY_44, self.onGotoSquare),
         (gameStrings.TEXT_DEBUGPROXY_45, self.onGotoPalace),
         (gameStrings.TEXT_DEBUGPROXY_46, self.onGotoStage),
         (gameStrings.TEXT_DEBUGPROXY_47, self.onGotoSulan),
         (gameStrings.TEXT_DEBUGPROXY_48, self.onGotoWharf),
         (gameStrings.TEXT_DEBUGPROXY_49, self.onGotoPort),
         (gameStrings.TEXT_DEBUGPROXY_50, self.onGotoLinxu),
         (gameStrings.TEXT_DEBUGPROXY_51, self.onGotoHuaHai),
         (gameStrings.TEXT_DEBUGPROXY_52, self.onApplyTaFangFb),
         ('---------------', lambda : None),
         (gameStrings.TEXT_DEBUGPROXY_54, lambda : [BigWorld.setFxaaSampleQuality(5), BigWorld.enableFxaa(True)]),
         (gameStrings.TEXT_DEBUGPROXY_55, lambda : [BigWorld.setFxaaSampleQuality(0), BigWorld.enableFxaa(True)]),
         (gameStrings.TEXT_DEBUGPROXY_56, lambda : BigWorld.enableFxaa(False)),
         (gameStrings.TEXT_DEBUGPROXY_57, lambda : BigWorld.enableSharpenEffect(True)),
         (gameStrings.TEXT_DEBUGPROXY_58, lambda : BigWorld.enableSharpenEffect(False)),
         (gameStrings.TEXT_DEBUGPROXY_59, lambda : BigWorld.resetDepthOfField()),
         (gameStrings.TEXT_DEBUGPROXY_60, lambda : BigWorld.setDepthOfField(False)),
         (gameStrings.TEXT_DEBUGPROXY_61, lambda : BigWorld.setDepthOfField(True, 200, 0, 800, 400, 1)),
         (gameStrings.TEXT_DEBUGPROXY_62, lambda : BigWorld.enableHighQuality(True)),
         (gameStrings.TEXT_DEBUGPROXY_63, lambda : BigWorld.enableHighQuality(False)),
         ('---------------', lambda : None),
         (gameStrings.TEXT_DEBUGPROXY_65, self.onTeleportToForest),
         (gameStrings.TEXT_DEBUGPROXY_66, self.showStoryDebug),
         (gameStrings.TEXT_DEBUGPROXY_67, self.showActionFx),
         (gameStrings.TEXT_DEBUGPROXY_68, self.showWalkLineEditor),
         (gameStrings.TEXT_DEBUGPROXY_69, self.showFbGenMonsterWidget),
         (gameStrings.TEXT_DEBUGPROXY_70, self.showNpcAction),
         (gameStrings.TEXT_DEBUGPROXY_71, self.showMonsterAction),
         (gameStrings.TEXT_DEBUGPROXY_72, self.onTeleportToMuban),
         (gameStrings.TEXT_DEBUGPROXY_73, self.onTeleportToWeiYiCeShi),
         (gameStrings.TEXT_DEBUGPROXY_74, self.onShowDebugSetting),
         (gameStrings.TEXT_DEBUGPROXY_75, self.onGetPosAndYaw),
         (gameStrings.TEXT_DEBUGPROXY_76, self.onTeleportToAMSTArea),
         (gameStrings.TEXT_DEBUGPROXY_77, self.onGenSeekerMap),
         (gameStrings.TEXT_DEBUGPROXY_78, self.showDyeTest),
         (gameStrings.TEXT_DEBUGPROXY_79, self.showPointGen),
         (gameStrings.TEXT_DEBUGPROXY_80, self.reloadCfgData)]
        self.destroyOnHide = True

    def hide(self, destroy = False):
        super(DebugProxy, self).hide(destroy)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DEBUG_VIEW)

    def show(self):
        self.showDebugView()

    def getValue(self, key):
        if key == 'debug.skilllist':
            skillData = SD.data
            keys = skillData.keys()
            keys.sort()
            i = 0
            ar = self.movie.CreateArray()
            for skillId in keys:
                sd = skillDataInfo.ClientSkillInfo(skillId[0], skillId[1])
                if sd.skillData:
                    skillName = sd.getSkillData('sname', gameStrings.TEXT_DEBUGPROXY_101)
                    value = GfxValue(gbk2unicode(str(skillId) + ':' + skillName))
                    ar.SetElement(i, value)
                    i = i + 1

            return ar
        if key == 'debug.funclist':
            ar = self.movie.CreateArray()
            i = 0
            for item in self.funcMap:
                value = GfxValue(gbk2unicode(item[0]))
                ar.SetElement(i, value)
                i = i + 1

            return ar

    def onClickFuncItem(self, *arg):
        idNum = int(arg[3][0].GetNumber())
        self.funcMap[idNum][1]()

    def onSwitchSummonedSprite(self):
        enableSummonedSprite = gameglobal.rds.configData.get('enableSummonedSprite', False)
        gamelog.debug('------m.l@DebugProxy.debug', enableSummonedSprite)
        if enableSummonedSprite:
            msg = '$setGameCfg enableSummonedSprite false'
            BigWorld.player().cell.adminOnCell(msg)
        else:
            msg = '$setGameCfg enableSummonedSprite true'
            BigWorld.player().cell.adminOnCell(msg)

    def onSetGroup(self):
        gamelog.debug('debug:onSetGroup')
        p = BigWorld.player()
        if p.lockedId == 0:
            p.cell.buildGroupWithDefault(gametypes.GROUP_TYPE_RAID_GROUP, False, const.GROUP_GOAL_DEFAULT)
            return
        en = BigWorld.entities.get(p.lockedId)
        if en.__class__.__name__ == 'Avatar':
            p.cell.inviteGroup(en.roleName)
        else:
            p.cell.buildGroupWithDefault(gametypes.GROUP_TYPE_RAID_GROUP, False, const.GROUP_GOAL_DEFAULT)

    def onSetTeam(self):
        gamelog.debug('debug:onSetTeam')
        p = BigWorld.player()
        if p.lockedId == 0:
            p.cell.buildGroupWithDefault(gametypes.GROUP_TYPE_TEAM_GROUP, False, const.GROUP_GOAL_DEFAULT)
            return
        en = BigWorld.entities.get(p.lockedId)
        if en.__class__.__name__ == 'Avatar':
            p.cell.inviteGroup(en.roleName)
        else:
            p.cell.buildGroupWithDefault(gametypes.GROUP_TYPE_TEAM_GROUP, False, const.GROUP_GOAL_DEFAULT)

    def onSetCamp1(self):
        gamelog.debug('debug:onSetCamp1')
        p = BigWorld.player()
        p.cell.setCamp(1)

    def onSetCamp2(self):
        gamelog.debug('debug:onSetCamp2')
        p = BigWorld.player()
        p.cell.setCamp(2)

    def onExitFuben(self):
        msg = '$endFuben'
        p = BigWorld.player()
        p.cell.adminOnCell(msg)

    def onCreateNpcFubenEntry(self):
        p = BigWorld.player()
        p.cell.createNpcFubenEntry()

    def onGotoForestSpawnPoint(self):
        tgtPos = (-132, 296, 19)
        self._gotoTgtPos(tgtPos)

    def onGotoShenci(self):
        tgtPos = (-35.808144, 76.899948, 196.992645)
        self._gotoTgtPos(tgtPos)

    def onGotoDragon(self):
        tgtPos = (284.695526, 63.165676, -111.29808)
        self._gotoTgtPos(tgtPos)

    def onGotoSkillArea(self):
        tgtPos = (5584.14, 5.807, -1533.81)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoSkillShopArea(self):
        tgtPos = (5584.14, 5.807, -1533.81)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoSquare(self):
        tgtPos = (5511.7, 15.3, -1634.2)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoPalace(self):
        tgtPos = (5513.6, 45.9, -1394.7)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoStage(self):
        tgtPos = (5511.7, 15.3, -1634.2)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoSulan(self):
        tgtPos = (5510.7, 9.2, -1960.2)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoWharf(self):
        tgtPos = (5896.7, 3.8, -1949.3)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoPort(self):
        tgtPos = (5938.34, 3.88987, -1826.47)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoLinxu(self):
        tgtPos = (4366.92, 35.795, -1866.02)
        self._gotoTgtPos(tgtPos, 1)

    def onGotoHuaHai(self):
        tgtPos = (4951.24, 42.9999, -2489.1)
        self._gotoTgtPos(tgtPos, 1)

    def _gotoTgtPos(self, tgtPos, spaceNo = ''):
        msg = '$goto %f %f %f %s' % (tgtPos[0],
         tgtPos[1],
         tgtPos[2],
         spaceNo)
        p = BigWorld.player()
        p.cell.adminOnCell(msg)

    def onApplyTaFangFb(self):
        p = BigWorld.player()
        if p.groupNUID == 0:
            p.cell.buildGroupWithDefault(gametypes.GROUP_TYPE_TEAM_GROUP, False, const.GROUP_GOAL_DEFAULT)
            BigWorld.callback(2, self._applyTaFangFb)

    def _applyTaFangFb(self):
        pass

    def onClickDebugSkill(self, *arg):
        data = arg[3][0].GetString()
        skillId, skillLv = data[1:-1].split(',')
        p = BigWorld.player()
        p.skillId = int(skillId)
        p.skillLevel = int(skillLv)
        skillInfo = SkillInfo(p.skillId, p.skillLevel)
        if not skillDataInfo.checkSkillRequest(skillInfo):
            return
        if logicInfo.isSkillCooldowning(p.skillId):
            p.chatToEventEx(gameStrings.TEXT_DEBUGPROXY_273, const.CHANNEL_COLOR_RED)
            return
        if p.spellingType or not logicInfo.isUseableSkill(p.skillId):
            p.chatToEventEx(gameStrings.TEXT_IMPL_IMPCOMBAT_10504, const.CHANNEL_COLOR_RED)
            return
        if logicInfo.isUseableSkill(p.skillId):
            gamelog.debug('skill can use', id, BigWorld.time(), logicInfo.commonCooldownWeaponSkill[0])
            if skillDataInfo.isSkillneedCircle(skillInfo):
                p.circleEffect.cancel()
                p.circleEffect.start(p.skillId, p.skillLevel, True)
            else:
                p.useskill(isDebug=True)

    def showDebugView(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_VIEW)))

    def showActionDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_ACTION)))

    def showParticleDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_PARTICLE)))

    def onSendSkill(self, *arg):
        prefix = arg[3][0].GetString()
        gamelog.debug('onSendSkill', prefix)
        if prefix == '' or not prefix.isdigit():
            return self.getValue('debug.skilllist')
        num = 10 ** (4 - len(prefix))
        prefix = int(prefix)
        skillData = SD.data
        keys = skillData.keys()
        keys.sort()
        i = 0
        ar = self.movie.CreateArray()
        for skillId in keys:
            if skillId[0] / num != prefix:
                continue
            sd = skillDataInfo.ClientSkillInfo(skillId[0], skillId[1])
            if sd.skillData:
                skillName = sd.getSkillData('sname', gameStrings.TEXT_DEBUGPROXY_101)
                value = GfxValue(gbk2unicode(str(skillId) + ':' + skillName))
                ar.SetElement(i, value)
                i = i + 1

        return ar

    def addWushuang(self, *arg):
        p = BigWorld.player()
        p.cell.adminOnCell('$fullws')

    def onTeleportToForest(self):
        p = BigWorld.player()
        p.cell.teleportByPhase(const.SPACE_NO_BIG_WORLD)

    def showStoryDebug(self):
        self.uiAdapter.storyEditDebug.showStoryEdit()

    def showActionFx(self):
        self.uiAdapter.actionFxEditor.showActionFxEditor()

    def showDyeTest(self):
        self.uiAdapter.dyeTest.show()

    def showWalkLineEditor(self):
        self.uiAdapter.walkLineEdit.showWalkLineEdit()

    def showFbGenMonsterWidget(self):
        self.uiAdapter.fbGenMonster.showFbGenMonster()

    def showNpcAction(self):
        self.uiAdapter.npcAction.show()

    def showMonsterAction(self):
        self.uiAdapter.monsterAction.show()

    def onTeleportToMuban(self):
        self._gotoTgtPos((47.0, 202.0, 32.26), const.SPACE_NO_MOBAN)

    def onTeleportToAMSTArea(self):
        self._gotoTgtPos((47.0, 202.0, 32.26), const.SPACE_NO_AMST)

    def onGenSeekerMap(self):
        p = BigWorld.player()
        p.cell.genSeekerMap()

    def onTeleportToWeiYiCeShi(self):
        self._gotoTgtPos((20.6, 20.0, 20.7), const.SPACE_NO_WYCS)

    def onShowDebugSetting(self):
        gameglobal.rds.ui.debugSetting.show()

    def onGetPosAndYaw(self):
        p = BigWorld.player()
        info = 'pos:' + str(p.position) + ' ' + 'yaw:' + str(p.yaw)
        gameglobal.rds.ui.chat.setInputText(info)

    def playEffect(self, effectId, lastTime, effectLv):
        p = BigWorld.player()
        if p.attachFx.has_key(effectId):
            return
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (effectLv,
             p.getBasicEffectPriority(),
             None,
             effectId,
             sfx.EFFECT_UNLIMIT,
             p.position))
            p.addFx(effectId, fx)
            if lastTime > 0:
                BigWorld.callback(lastTime, Functor(self._removeEffect, effectId))
            return

    def _removeEffect(self, effectId):
        p = BigWorld.player()
        p.removeFx(effectId)

    def showPointGen(self):
        gameglobal.rds.ui.pointGen.show()

    def reloadCfgData(self):
        gameglobal.rds.ui.reloadData.show()
