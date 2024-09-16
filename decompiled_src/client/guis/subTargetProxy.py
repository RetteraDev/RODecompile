#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/subTargetProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import gametypes
import appSetting
import keys
from uiProxy import UIProxy
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from data import monster_model_client_data as NMMD
from data import quest_data as QD
unitTypePath = 'unitType/icon/'

class SubTargetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SubTargetProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerSubTargetFrame': self.onRegisterSubTargetFrame,
         'getQuestTip': self.onGetQuestTip}
        self.mediator = None
        self.targetDirHandle = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SUB_TARGET_UF:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None

    def onRegisterSubTargetFrame(self, *arg):
        p = BigWorld.player()
        data = {}
        data['active'] = False
        data['entityId'] = p.optionalTargetLocked.id if p.optionalTargetLocked else 0
        data['school'] = p.optionalTargetLocked.realSchool if hasattr(p.optionalTargetLocked, 'realSchool') else -1
        data['hpMode'] = appSetting.Obj.get(keys.SET_HP_MODE, 0)
        return uiUtils.dict2GfxDict(data)

    def setActive(self, active):
        if self.mediator:
            self.mediator.Invoke('setActive', GfxValue(active))

    def setEntityId(self, entityId):
        if self.mediator:
            self.mediator.Invoke('setEntityId', GfxValue(entityId))

    def setName(self, name):
        if self.mediator:
            self.mediator.Invoke('setName', GfxValue(gbk2unicode(name)))

    def setHpMode(self, mode):
        if self.mediator:
            self.mediator.Invoke('setHpMode', GfxValue(mode))

    def setHp(self, hp):
        if hp is None:
            return
        else:
            if self.mediator:
                self.mediator.Invoke('setHp', GfxValue(float(hp)))
            return

    def setMhp(self, mhp):
        if self.mediator:
            self.mediator.Invoke('setMhp', GfxValue(float(mhp)))

    def setSp(self, sp):
        if self.mediator:
            self.mediator.Invoke('setSp', GfxValue(int(sp)))

    def setMsp(self, msp):
        if self.mediator:
            self.mediator.Invoke('setMsp', GfxValue(int(msp)))

    def setLevel(self, lv):
        if self.mediator:
            self.mediator.Invoke('setLevel', GfxValue(lv))

    def setSchool(self, school):
        if self.mediator:
            self.mediator.Invoke('setSchool', GfxValue(school))

    def setMonsterLogo(self, logo):
        if self.mediator:
            self.mediator.Invoke('setMonsterLogo', GfxValue(logo))

    def changeFrame(self, frame):
        if self.mediator:
            self.mediator.Invoke('changeFrame', GfxValue(frame))

    def showSubTargetUnitFrame(self):
        p = BigWorld.player()
        t = p.optionalTargetLocked
        BigWorld.callback(0, self.setHideBloodNumState)
        if t == None or t.IsFragileObject:
            return
        else:
            self.setActive(True)
            self.setEntityId(t.id)
            if t != None:
                if self.mediator == None:
                    return
                self.updateTargetDir()
                if getattr(t, 'roleName', None):
                    self.setName(t.roleName)
                if t.IsMonster or t.IsSummonedBeast:
                    if hasattr(t, 'charType'):
                        data = NMMD.data.get(t.charType, None)
                        if data == None:
                            raise Exception('can not find charType :%s' % str(t.charType))
                    self.changeFrame('monster')
                    self.setCombatVisible(False)
                    if hasattr(t, 'roleName') and t.roleName != None:
                        self.setName(t.roleName)
                    if hasattr(t, 'monsterStrengthType'):
                        if t.monsterStrengthType == gametypes.MONSTER_NORMAL:
                            self.setMonsterLogo('normal')
                        elif t.monsterStrengthType == gametypes.MONSTER_ELITE:
                            self.setMonsterLogo('rarestrange')
                        elif t.monsterStrengthType in gametypes.MONSTER_BOSS_TYPE:
                            self.setMonsterLogo('boos')
                    if hasattr(t, 'charType') and t.charType in p.questMonsterInfo.keys():
                        self.setQuestLogoVisible(True)
                elif t.IsAvatar:
                    if p.isEnemy(p.targetLocked):
                        self.changeFrame('enemy')
                    else:
                        self.changeFrame('friend')
                    if getattr(t, 'roleName', None):
                        if p.isInSSCorTeamSSC():
                            self.setName(const.SSC_ROLENAME)
                        elif p.bHideFightForLoveFighterName(p.optionalTargetLocked):
                            nameInfo = p.getFightForLoveNameInfo()
                            self.setName(nameInfo.get('name', ''))
                        elif getattr(t, 'jctSeq', 0) and p.inClanCourier():
                            name = t.getJCTRoleName()
                            self.setName(name)
                        else:
                            roleName = p.anonymNameMgr.checkNeedAnonymousName(t, t.roleName)
                            self.setName(roleName)
                    self.setSchool(t.realSchool)
                elif t.IsCreation or t.__class__.__name__ == 'EmptyZaiju':
                    self.setSchool(-1)
                elif t.__class__.__name__ in gametypes.CLAN_WAR_CLASS:
                    self.changeFrame('NPC')
                elif hasattr(t, 'npcInstance') and hasattr(t, 'npcId'):
                    self.changeFrame('NPC')
                    self.setHp(10000)
                    self.setMhp(10000)
                    self.setSp(10000)
                    self.setMsp(10000)
                    self.setLevel(99)
                    self.setCombatVisible(False)
                    if getattr(t, 'roleName', None):
                        self.setName(t.roleName)
                    return
                if hasattr(t, 'hp'):
                    self.setHp(t.hp)
                    self.setMhp(t.mhp)
                targetSchool = getattr(t, 'realSchool', None)
                if targetSchool != None:
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                elif t.__class__.__name__ == 'EmptyZaiju':
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                elif hasattr(t, 'mp'):
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                self.setLevel(t.realLv if hasattr(t, 'realLv') else getattr(t, 'lv', 1))
            return

    def hideSubTargetUnitFrame(self):
        self.setActive(False)

    def setCombatVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setCombatVisible', GfxValue(bVisible))

    def setQuestLogoVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setQuestLogoVisible', GfxValue(bVisible))

    def reset(self):
        if self.targetDirHandle:
            BigWorld.cancelCallback(self.targetDirHandle)

    def updateTargetDir(self):
        p = BigWorld.player()
        if not p:
            return
        target = p.optionalTargetLocked
        if target and target != BigWorld.player() and (target.IsAvatar or target.IsMonster or target.IsSummonedBeast):
            if self.mediator:
                self.mediator.Invoke('setDir', GfxValue(gbk2unicode(str(self.getTargetLockDist()) + gameStrings.TEXT_AIMCROSS_248)))
            self.targetDirHandle = BigWorld.callback(0.5, self.updateTargetDir)
        else:
            self.mediator.Invoke('setDir', GfxValue(''))

    def getTargetLockDist(self):
        p = BigWorld.player()
        return int((p.optionalTargetLocked.position - p.position).length)

    def updateQuestMonsterLogo(self, isQuestMonster):
        self.setQuestLogoVisible(isQuestMonster)

    def onGetQuestTip(self, *arg):
        p = BigWorld.player()
        tgt = p.optionalTargetLocked
        ret = ''
        if not tgt:
            return GfxValue('')
        if not tgt.IsMonster:
            return GfxValue('')
        if not hasattr(tgt, 'charType'):
            return GfxValue('')
        if tgt.charType in p.questMonsterInfo.keys():
            for questId in p.questMonsterInfo[tgt.charType]:
                qd = QD.data[questId]
                lv = p.getQuestLv(questId, qd)
                name = QD.data.get(questId, {}).get('name', '')
                ret += str(lv) + ' ' + name + '\n'

            return GfxValue(gbk2unicode(ret))
        return GfxValue(ret)

    def setHideBloodNumState(self):
        if not self.mediator:
            return
        t = BigWorld.player().optionalTargetLocked
        isHideBloodNum = False
        if t:
            isHideBloodNum = getattr(t, 'isHideBloodNum', False)
        self.mediator.Invoke('setHideBloodState', GfxValue(isHideBloodNum))
        if t and not isHideBloodNum and hasattr(t, 'hp') and hasattr(t, 'mhp'):
            self.setMhp(t.mhp)
            self.setHp(t.hp)
