#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/targetProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
from VirtualMonster import VirtualMonster
import const
import gameglobal
import gametypes
import appSetting
import formula
import keys
import ui
import menuManager
import utils
from uiProxy import DataProxy
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from guis import events
from guis.asObject import ASObject
from gameStrings import gameStrings
from callbackHelper import Functor
from helpers.eventDispatcher import Event
from data import monster_model_client_data as NMMD
from data import npc_model_client_data as NMCD
from data import quest_data as QD
from data import monster_random_prop_data as MRPD
from data import item_data as ID
from data import sys_config_data as SYSCD
from data import sheng_si_chang_data as SSCD
from data import arena_mode_data as AMD
from data import summon_sprite_info_data as SSID
from data import photo_border_data as PBD
unitTypePath = 'unitType/icon/'
REFRESH_INTERVAL = 0.05

class TargetProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(TargetProxy, self).__init__(uiAdapter)
        self.bindType = 'target'
        self.binding = {}
        self.modelMap = {'registerTargetCastbar': self.onRegisterTargetCastbar,
         'registerTargetFrame': self.onRegisterTargetFrame,
         'targetSelect': self.onTargetSelect,
         'getQuestTip': self.onGetQuestTip,
         'initTarget': self.onInitTarget}
        self.mediator = None
        self.pct = 0
        self.tar2tar = None
        self.target = None
        self.lefttick = 0
        self.mc = None
        self.targetDirHandle = None
        self.oldDistance = ''
        self.starttick = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TARGET_UF:
            self.mediator = mediator
            self.setHpThreshold(SYSCD.data.get('hideMaxHpThreshold', -1))
            BigWorld.callback(0, self.setHideBloodState)

    def clearWidget(self):
        self.mediator = None

    def onRegisterTargetFrame(self, *arg):
        p = BigWorld.player()
        data = {}
        data['active'] = False
        data['entityId'] = p.targetLocked.id if p.targetLocked else 0
        data['school'] = p.targetLocked.realSchool if hasattr(p.targetLocked, 'realSchool') else -1
        data['hpMode'] = appSetting.Obj.get(keys.SET_HP_MODE, 0)
        borderId = getattr(p.targetLocked, 'photoBorderId', 0)
        data['prefixBg'] = PBD.data.get(borderId, {}).get('prefixBg', '')
        return uiUtils.dict2GfxDict(data, True)

    def getIconPath(self, t):
        iconPath = ''
        if getattr(t, 'IsAvatar', False) or utils.instanceof(t, 'Puppet'):
            iconPath = 'headIcon/%s.dds' % str(t.school * 10 + t.physique.sex)
        elif getattr(t, 'IsSummonedSprite', False):
            iconId = SSID.data.get(t.spriteId, {}).get('spriteIcon', '000')
            iconPath = 'summonedSprite/icon/%s.dds' % iconId
        elif t.IsMonster or t.IsSummonedBeast:
            iconPath = unitTypePath + NMMD.data.get(t.charType, {}).get('icon', '40000') + '.dds'
        elif hasattr(t, 'npcInstance') and hasattr(t, 'npcId'):
            iconPath = unitTypePath + NMCD.data.get(t.npcId, {}).get('icon', '40000') + '.dds'
        elif t.IsCreation or t.__class__.__name__ == 'EmptyZaiju':
            iconPath = unitTypePath + '30009.dds'
        elif t.__class__.__name__ == 'LifeCsmItem':
            targetItemId = t.getTargetItemId()
            if not targetItemId:
                icon = t.getOptionalIcon()
                iconPath = 'item/icon/%s.dds' % icon
            else:
                data = ID.data.get(targetItemId, {})
                iconPath = 'item/icon/%s.dds' % data.get('icon', 'notFound')
        return iconPath

    def setActive(self, active):
        if self.mediator:
            self.mediator.Invoke('setActive', GfxValue(active))

    def setEntityId(self, entityId):
        if self.mediator:
            self.mediator.Invoke('setEntityId', GfxValue(entityId))

    def setHideBloodState(self):
        p = BigWorld.player()
        t = p.targetLocked
        if t == None or t.IsFragileObject:
            return
        else:
            isTargetHideBloodNum = getattr(t, 'isHideBloodNum', False)
            lockId = getattr(t, 'lockedId', 0)
            lockEntity = BigWorld.entities.get(lockId, None)
            lockEntityHideBloodNum = False
            if lockEntity:
                lockEntityHideBloodNum = getattr(lockEntity, 'isHideBloodNum', False)
            if self.mediator:
                self.mediator.Invoke('setHideBloodState', uiUtils.array2GfxAarry((isTargetHideBloodNum, lockEntityHideBloodNum), False))
            if hasattr(t, 'hp') and hasattr(t, 'mhp'):
                self.setMhp(t.mhp)
                self.setHp(t.hp)
            if not lockEntityHideBloodNum and lockEntity and hasattr(lockEntity, 'hp') and hasattr(lockEntity, 'mhp'):
                self.setTargetMhp(lockEntity.mhp)
                self.setTargetHp(lockEntity.hp)
            return

    def setName(self, name):
        if self.mediator:
            p = BigWorld.player()
            t = p.targetLocked
            if p.isInSSCorTeamSSC():
                name = const.SSC_ROLENAME
            if p.bHideFightForLoveFighterName(p.targetLocked):
                nameInfo = p.getFightForLoveNameInfo()
                name = nameInfo.get('name', '')
            if getattr(t, 'jctSeq', 0) and BigWorld.player().inClanCourier():
                name = t.getJCTRoleName()
            realName = p.anonymNameMgr.checkNeedAnonymousName(t, name)
            self.mediator.Invoke('setName', GfxValue(gbk2unicode(realName)))

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

    def setHpThreshold(self, hpThresHold):
        if hpThresHold is None:
            return
        else:
            if self.mediator:
                self.mediator.Invoke('setHpThreshold', GfxValue(float(hpThresHold)))
            return

    def setMhp(self, mhp):
        if self.mediator:
            self.mediator.Invoke('setMhp', GfxValue(float(mhp)))

    def refreshRandProps(self):
        if self.mediator:
            p = BigWorld.player()
            t = p.targetLocked
            self.setRandProps(getattr(t, 'randProps', ()))

    def setRandProps(self, randProps):
        if self.mediator:
            propsList = []
            for props in randProps:
                if props in MRPD.data:
                    name = MRPD.data[props].get('name', '')
                    type = MRPD.data[props].get('colorType', 1)
                    propsList.append((name, type))

            self.mediator.Invoke('setRandProps', uiUtils.array2GfxAarry(propsList, True))

    def setLifeCsmInfo(self, phase, name, desc, phaseName, iconPath, count):
        if self.mediator:
            data = [phase,
             name,
             desc,
             phaseName,
             iconPath,
             count]
            self.mediator.Invoke('setLifeCsmInfo', uiUtils.array2GfxAarry(data, True))

    def setSp(self, sp):
        if self.mediator:
            self.mediator.Invoke('setSp', GfxValue(int(sp)))

    def setMsp(self, msp):
        if self.mediator:
            self.mediator.Invoke('setMsp', GfxValue(int(msp)))

    def setLevel(self, lv):
        p = BigWorld.player()
        if p.isInSSCorTeamSSC() and SSCD.data.get(formula.getFubenNo(p.spaceNo), {}).has_key('sscLv'):
            ent = p.targetLocked
            if ent and hasattr(ent, 'IsAvatar') and ent.IsAvatar:
                lv = 'Lv.%d' % ent.realLv
        fbNo = formula.getFubenNo(p.spaceNo)
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        ent = p.targetLocked
        if p.inFubenTypes(const.FB_TYPE_ARENA) and AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
            if ent and hasattr(ent, 'IsAvatar') and ent.IsAvatar:
                lv = 'Lv.%d' % ent.realLv
        if p.isInSSCorTeamSSC() and hasattr(ent, 'IsAvatar') and ent.IsAvatar:
            lv = 'Lv.%s' % str(ent.realLv)
        if p.isInBfDota() and getattr(ent, 'IsAvatar', True):
            lv = str(ent.battleFieldDotaLv)
        if self.mediator:
            if ent and hasattr(ent, 'needHideTargetProxyLv') and ent.needHideTargetProxyLv():
                self.mediator.Invoke('hideLevel')
            elif type(lv) == str:
                self.mediator.Invoke('setLevel', GfxValue(gbk2unicode(lv)))
            else:
                lv = 'Lv.%d' % lv
                self.mediator.Invoke('setLevel', GfxValue(gbk2unicode(lv, True)))

    def setTargetIcon(self, targetIcon):
        if self.mediator:
            self.mediator.Invoke('setTargetIcon', GfxValue(targetIcon))

    def setSchool(self, school):
        if self.mediator:
            self.mediator.Invoke('setSchool', GfxValue(school))

    def setTargetName(self, name):
        if self.mediator:
            p = BigWorld.player()
            if p.isInSSCorTeamSSC():
                name = const.SSC_ROLENAME
            t = p.targetLocked
            lockedId = getattr(t, 'lockedId', None)
            if t == None or t.IsFragileObject:
                return
            ent = None
            if lockedId != None:
                ent = BigWorld.entities.get(lockedId, None)
            if p.bHideFightForLoveFighterName(ent):
                nameInfo = p.getFightForLoveNameInfo()
                name = nameInfo.get('name', '')
            if getattr(ent, 'jctSeq', 0) and p.inClanCourier():
                name = ent.getJCTRoleName()
            realName = p.anonymNameMgr.checkNeedAnonymousName(ent, name)
            self.mediator.Invoke('setTargetName', GfxValue(gbk2unicode(realName)))
            self.setHideBloodState()

    def setTargetNameVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setTargetNameVisible', GfxValue(bVisible))
            if bVisible:
                self.setHideBloodState()

    def setTargetHp(self, value):
        if self.mediator:
            if not value:
                value = 0
            self.mediator.Invoke('setT2THp', GfxValue(float(value)))

    def setTargetMhp(self, value):
        if self.mediator:
            if not value:
                value = 0
            self.mediator.Invoke('setT2TMhp', GfxValue(float(value)))

    def setMonsterLogo(self, logo):
        if self.mediator:
            self.mediator.Invoke('setMonsterLogo', GfxValue(logo))

    def showRightMenu(self, menuId, hostId = None):
        if self.mediator:
            menuManager.getInstance().menuTarget.apply(entity=BigWorld.player().targetLocked, hostId=hostId)
            menuData = menuManager.getInstance().getMenuListById(menuId)
            if menuData:
                self.mediator.Invoke('showRightMenuF', uiUtils.dict2GfxDict(menuData, True))

    def hideRightMenu(self):
        if self.mediator:
            self.mediator.Invoke('hideMenu')

    def changeFrame(self, frame):
        if self.mediator:
            self.mediator.Invoke('changeFrame', GfxValue(frame))

    def setHideHpNum(self, hide):
        if self.mediator:
            self.mediator.Invoke('setHideHPNum', GfxValue(hide))

    def showTargetUnitFrame(self):
        p = BigWorld.player()
        t = p.targetLocked
        lockedId = getattr(t, 'lockedId', None)
        if t == None or t.IsFragileObject:
            return
        else:
            self.setActive(True)
            self.hideRightMenu()
            if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                self.setEntityId(0)
            else:
                self.setEntityId(t.id)
            if lockedId != None:
                ent = BigWorld.entities.get(lockedId, None)
            else:
                ent = None
            if self.mc:
                self.mc.SetVisible(t == self.target and self.lefttick > 0)
                self.setHideHpNum(0)
            self.setHideBloodState()
            if t != None:
                self.updateTargetDir()
                self.setPrefixBg()
                self.setCombatVisible(False)
                if t.IsMonster or t.IsSummonedBeast:
                    data = NMMD.data.get(t.charType, None)
                    if data == None:
                        raise Exception('can not find charType :%s' % str(t.charType))
                    self.setHideHpNum(data.get('hideHpNum', 0))
                    self.changeFrame('monster')
                    self.setCombatVisible(False)
                    if hasattr(t, 'roleName') and t.roleName != None:
                        self.setName(t.roleName)
                    if t.monsterStrengthType == gametypes.MONSTER_NORMAL:
                        self.setMonsterLogo('normal')
                    elif t.monsterStrengthType == gametypes.MONSTER_ELITE:
                        self.setMonsterLogo('rarestrange')
                    elif t.monsterStrengthType in gametypes.MONSTER_BOSS_TYPE:
                        self.setMonsterLogo('boos')
                    if t.charType in p.questMonsterInfo.keys():
                        self.setQuestLogoVisible(True)
                    self.updateJingJie(t)
                elif t.IsAvatar or utils.instanceof(t, 'Puppet'):
                    if p.isEnemy(p.targetLocked):
                        self.changeFrame('enemy')
                    else:
                        self.changeFrame('friend')
                    if getattr(t, 'roleName', None):
                        if p.isInSSCorTeamSSC():
                            self.setName(const.SSC_ROLENAME)
                        elif p.bHideFightForLoveFighterName(p.targetLocked):
                            nameInfo = p.getFightForLoveNameInfo()
                            self.setName(nameInfo.get('name', ''))
                        elif gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                            campName = gameglobal.rds.ui.battleOfFortProgressBar.getAvatarCampName(t)
                            self.setName(campName)
                        else:
                            self.setName(t.roleName)
                    self.setSchool(t.realSchool)
                    self.updateJingJie(t)
                    self.onInitTarget()
                elif t.IsCreation or t.__class__.__name__ == 'EmptyZaiju' or t.__class__.__name__ == 'WingWorldCarrier' or t.IsWingCityWarBuilding or t.__class__.__name__ == 'HomeFurniture' or t.__class__.__name__ == 'NoticeBoard':
                    self.changeFrame('monster')
                    self.setCombatVisible(False)
                    self.setMonsterLogo('normal')
                    self.updateJingJie(t)
                elif t.__class__.__name__ == 'LifeCsmItem':
                    self.changeFrame('monster')
                    self.setHp(1)
                    self.setMhp(0)
                    self.changeFrame('LifeCsmItem')
                    phase = 'Lv.' + str(t.lv)
                    name = t.getColorName()
                    desc = SYSCD.data.get('lifeCsmDesc', {1: gameStrings.TEXT_TARGETPROXY_399,
                     3: gameStrings.TEXT_TARGETPROXY_399_1,
                     4: gameStrings.TEXT_TARGETPROXY_399_2}).get(t.getSubType(), '')
                    phaseName = t.getPhaseName()
                    iconPath = self.getIconPath(t)
                    self.updateJingJie(t)
                    self.setLifeCsmInfo(phase, name, desc, phaseName, iconPath, t.quantity)
                elif t.__class__.__name__ in gametypes.CLAN_WAR_CLASS:
                    self.changeFrame('NPC')
                    self.updateJingJie(t)
                elif hasattr(t, 'npcInstance') and hasattr(t, 'npcId'):
                    self.changeFrame('NPC')
                    self.setHp(10000)
                    self.setMhp(10000)
                    self.setSp(10000)
                    self.setMsp(10000)
                    self.setLevel(99)
                    self.updateJingJie(t)
                    self.setCombatVisible(False)
                    self.setRandProps(getattr(t, 'randProps', ()))
                    if getattr(t, 'roleName', None):
                        self.setName(t.roleName)
                    if ent == None:
                        self.setTargetNameVisible(False)
                    else:
                        self.tar2tar = ent
                        if hasattr(ent, 'roleName') and ent.roleName:
                            self.setTargetName(ent.roleName)
                        if hasattr(ent, 'hp'):
                            self.setTargetHp(ent.hp)
                        if hasattr(ent, 'mhp'):
                            self.setTargetMhp(ent.mhp)
                    return
                if hasattr(t, 'IsSummonedSprite') and t.IsSummonedSprite:
                    self.changeFrame('friend')
                    self.setTargetIcon('summonSprite')
                    self.onInitTarget()
                    spriteName = SSID.data.get(t.spriteId, {}).get('name', '000')
                    self.setName(getattr(t, 'roleName', spriteName))
                if getattr(t, 'roleName', None):
                    self.setName(t.roleName)
                self.setRandProps(getattr(t, 'randProps', ()))
                if hasattr(t, 'hp'):
                    t.hp = int(t.hp)
                    self.setHp(t.hp)
                    self.setMhp(t.mhp)
                targetSchool = getattr(t, 'realSchool', None)
                if targetSchool != None and hasattr(t, 'mp'):
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                elif t.__class__.__name__ == 'EmptyZaiju':
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                elif hasattr(t, 'mp'):
                    self.setSp(t.mp)
                    self.setMsp(t.mmp)
                tlv = 0
                if hasattr(t, 'realLv'):
                    tlv = t.realLv
                elif hasattr(t, 'lv'):
                    tlv = t.lv
                self.setLevel(tlv)
                if ent == None:
                    self.setTargetNameVisible(False)
                else:
                    self.tar2tar = ent
                    if getattr(ent, 'roleName', None):
                        self.setTargetName(ent.roleName)
                    if ent.__class__.__name__ == 'VirtualMonster':
                        master = BigWorld.entities.get(ent.masterMonsterID)
                    else:
                        master = ent
                    if master and hasattr(master, 'hp'):
                        self.setTargetHp(master.hp)
                    if master and hasattr(master, 'mhp'):
                        self.setTargetMhp(master.mhp)
                self.updateMergeBuff()
            return

    def updateMergeBuff(self):
        if not self.mediator:
            return
        else:
            target = BigWorld.player().targetLocked
            mergeData = []
            if getattr(target, 'getMergeBuffDesc', None):
                mergeData = target.getMergeBuffDesc()
            self.mediator.Invoke('updateMergeBuff', uiUtils.array2GfxAarry(mergeData, True))
            return

    def hideTargetUnitFrame(self):
        self.setActive(False)
        if self.mc:
            self.mc.SetVisible(False)
        self.Mode = uiConst.MODE_Inactive

    def _needShowBossState(self):
        target = BigWorld.player().targetLocked
        if isinstance(target, VirtualMonster):
            master = BigWorld.entities.get(target.masterMonsterID)
        else:
            master = target
        if master and hasattr(master, 'charType'):
            showBlood = uiUtils._isNeedShowBossBlood(master.charType)
        else:
            showBlood = False
        return showBlood

    def changeStateIcon(self, addData, delData):
        if self.mediator:
            self.mediator.Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))

    def clearStateIcon(self):
        if self._needShowBossState():
            gameglobal.rds.ui.bossBlood.clearPartStateIcon()
        elif self.mediator:
            self.mediator.Invoke('clearBuff')

    def setPrefixBg(self):
        if not self.mediator:
            return
        m = ASObject(self.mediator)
        p = BigWorld.player()
        t = p.targetLocked
        if t:
            borderId = getattr(p.targetLocked, 'photoBorderId', 0)
            prefixBg = PBD.data.get(borderId, {}).get('prefixBg', '')
            m.prefixBg = prefixBg
        else:
            m.prefixBg = ''

    def setCombatVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setCombatVisible', GfxValue(bVisible))

    def setQuestLogoVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setQuestLogoVisible', GfxValue(bVisible))

    def setTargetLockName(self, id):
        ent = BigWorld.entities.get(id, None)
        if ent == None or not getattr(ent, 'roleName', None):
            self.setTargetNameVisible(False)
        else:
            self.tar2tar = ent
            if getattr(ent, 'roleName', None):
                self.setTargetName(ent.roleName)
            if ent.__class__.__name__ == 'VirtualMonster':
                master = BigWorld.entities.get(ent.masterMonsterID)
            else:
                master = ent
            if master and hasattr(master, 'hp'):
                self.setTargetHp(master.hp)
            if master and hasattr(master, 'mhp'):
                self.setTargetMhp(master.mhp)

    def onRegisterTargetCastbar(self, *arg):
        self.mc = arg[3][0]
        self.castTimeRef = self.mc.GetMember('castTime')
        self.castName = self.mc.GetMember('abilityName')
        self.barRef0 = self.mc.GetMember('castbar0')
        self.barRef1 = self.mc.GetMember('castbar1')
        self.castbarBg = self.mc.GetMember('bg')
        self.maskRef0 = self.barRef0.GetMember('mask')
        self.fillRef0 = self.barRef0.GetMember('fill')
        self.maskRef1 = self.barRef1.GetMember('mask')
        self.fillRef1 = self.barRef1.GetMember('fill')
        self.barRef1.SetVisible(False)
        self.mc.SetVisible(False)
        self.fillStartX = self.fillRef0.GetMember('x').GetNumber()
        self.fillEndX = self.fillRef0.GetMember('width').GetNumber() + self.fillStartX
        self.Mode = uiConst.MODE_Inactive

    def startTargetCastbar(self, name, time, countDown = False, target = None, noInterrupt = False):
        if not hasattr(self, 'castbarBg'):
            return
        if noInterrupt:
            self.castbarBg.GotoAndStop('noInterrupt')
        else:
            self.castbarBg.GotoAndStop('Interrupt')
        self.totaltick = BigWorld.time() + time
        self.starttick = BigWorld.time()
        self.nowtick = BigWorld.time()
        self.target = target
        self.castName.SetText(gbk2unicode(name))
        self._updateCastBar(countDown)

    def _updateCastBar(self, countDown = False):
        self.nowtick = BigWorld.time()
        self.lefttick = self.totaltick - self.nowtick
        if self.lefttick > 0 and self.Mode != uiConst.MODE_Active:
            self._setPercent(1 if countDown else 0, self.lefttick)
            if self.target == BigWorld.player().targetLocked or isinstance(BigWorld.player().targetLocked, VirtualMonster) and BigWorld.player().targetLocked.masterMonsterID == self.target.id:
                self.mc.SetVisible(True)
                self.mc.SetAlpha(100)
            self.fillRef0.GotoAndPlay('casting')
            self.Mode = uiConst.MODE_Active
            BigWorld.callback(REFRESH_INTERVAL, Functor(self._updateCastBar, countDown))
            return
        else:
            if self.Mode == uiConst.MODE_FadeOutHold:
                if self.nowtick - self.fadetick > 0.5:
                    self.Mode = uiConst.MODE_FadeOut
                BigWorld.callback(REFRESH_INTERVAL, Functor(self._updateCastBar, countDown))
            elif self.Mode == uiConst.MODE_FadeOut:
                fadePct = (self.nowtick - self.fadetick) * 1000 / 250
                if fadePct > 1:
                    self.Mode = uiConst.MODE_Inactive
                    self.mc.SetVisible(False)
                    self.target = None
                else:
                    self.mc.SetAlpha((1 - fadePct) * 100)
                    BigWorld.callback(REFRESH_INTERVAL, Functor(self._updateCastBar, countDown))
            if self.lefttick + REFRESH_INTERVAL > 0:
                pct = self._getPct() if self.lefttick > 0 else 0
                self.pct = 1 - pct if countDown else pct
                self._setPercent(self.pct, self.lefttick)
                BigWorld.callback(REFRESH_INTERVAL, Functor(self._updateCastBar, countDown))
            elif self.Mode == uiConst.MODE_Active:
                self.fillRef0.GotoAndPlay('completed')
                self.Mode = uiConst.MODE_FadeOutHold
                BigWorld.callback(REFRESH_INTERVAL, self._updateCastBar)
                self.fadetick = BigWorld.time()
            return

    def _getPct(self):
        return (self.nowtick - self.starttick) / (self.totaltick - self.starttick) + 0.1

    def _setPercent(self, pct, leftTicks):
        self._setPercentBar(pct, self.maskRef0)
        ct = max(0, leftTicks)
        buf = '%.1f' % ct
        self.castTimeRef.SetText(buf)

    def _setPercentBar(self, pct, maskref):
        maskref.SetXScale(max(1, (pct + 0.1) * 100))

    def notifyTargetCastInterrupt(self):
        if not hasattr(self, 'barRef1'):
            return
        self.barRef1.SetVisible(True)
        self._setPercentBar(self.pct, self.maskRef1)
        self.fillRef1.GotoAndPlay('interrupted')
        self.maskRef0.SetXScale(1.0)
        self.Mode = uiConst.MODE_FadeOutHold
        self.totaltick = BigWorld.time() - REFRESH_INTERVAL
        self.fadetick = BigWorld.time()
        BigWorld.callback(0.1, self._updateCastBar)

    def onTargetSelect(self, *arg):
        uiUtils.onTargetSelect(self.tar2tar)

    def reset(self):
        if self.targetDirHandle:
            BigWorld.cancelCallback(self.targetDirHandle)
            self.targetDirHandle = None

    def updateTargetDir(self):
        if not BigWorld.player():
            return
        else:
            if self.targetDirHandle:
                BigWorld.cancelCallback(self.targetDirHandle)
                self.targetDirHandle = None
            target = BigWorld.player().targetLocked
            if target and target != BigWorld.player() and (getattr(target, 'IsAvatar', False) or getattr(target, 'IsMonster', False) or getattr(target, 'IsSummonedBeast', False) or getattr(target, 'IsOreSpawnPoint', False)) or utils.instanceof(target, 'Puppet'):
                distance = gbk2unicode(str(self.getTargetLockDist()) + gameStrings.TEXT_AIMCROSS_248)
                distanceEvent = Event(events.EVENT_TARGET_DISTANCE_UPDATE, distance)
                if distance != self.oldDistance:
                    gameglobal.rds.ui.dispatchEvent(distanceEvent)
                    self.oldDistance = distance
                self.targetDirHandle = BigWorld.callback(0.5, self.updateTargetDir)
            else:
                distanceEvent = Event(events.EVENT_TARGET_DISTANCE_UPDATE, '')
                if self.oldDistance != '':
                    gameglobal.rds.ui.dispatchEvent(distanceEvent)
                    self.oldDistance = ''
            return

    @ui.uiEvent(uiConst.WIDGET_TARGET_UF, events.EVENT_TARGET_DISTANCE_UPDATE)
    def setDistance(self, event):
        if self.mediator:
            self.mediator.Invoke('setDir', GfxValue(event.data))

    def getTargetLockDist(self):
        p = BigWorld.player()
        if not p.targetLocked:
            return -1
        try:
            ret = int((p.targetLocked.position - p.position).length)
        except:
            ret = -1

        return ret

    def resetTimer(self):
        if self.mediator:
            self.mediator.Invoke('resetTimer')

    def updateQuestMonsterLogo(self, isQuestMonster):
        self.setQuestLogoVisible(isQuestMonster)

    def getWidget(self):
        if not self.mediator:
            return None
        else:
            return ASObject(self.mediator).getWidget()

    def onInitTarget(self, *args):
        widget = self.getWidget()
        if not widget or not widget.mainMc.playerIcon:
            return
        t = BigWorld.player().targetLocked
        if not t:
            return
        defaultPhoto = self.getIconPath(t)
        widget.mainMc.playerIcon.headIcon.fitSize = True
        widget.mainMc.playerIcon.headIcon.loadImage(defaultPhoto)
        widget.mainMc.playerIcon.borderImg.fitSize = True
        borderIconPath = BigWorld.player().getPhotoBorderIcon(getattr(t, 'photoBorderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE40)
        widget.mainMc.playerIcon.borderImg.loadImage(borderIconPath)
        widget.mainMc.job.visible = not bool(getattr(t, 'IsSummonedSprite', False))

    def onGetQuestTip(self, *arg):
        p = BigWorld.player()
        tgt = p.targetLocked
        ret = ''
        if not tgt:
            return GfxValue('')
        if not tgt.IsMonster:
            return GfxValue('')
        if tgt.charType in p.questMonsterInfo.keys():
            for questId in p.questMonsterInfo[tgt.charType]:
                qd = QD.data[questId]
                lv = p.getQuestLv(questId, qd)
                name = QD.data.get(questId, {}).get('name', '')
                ret += str(lv) + ' ' + name + '\n'

            return GfxValue(gbk2unicode(ret))
        return GfxValue(ret)

    def setJingjie(self, jingjie):
        if jingjie is None:
            return
        else:
            if self.mediator:
                self.mediator.Invoke('setJingjie', GfxValue(int(jingjie)))
            return

    def updateJingJie(self, obj):
        if getattr(obj, 'jingJie', None):
            self.setJingjie(obj.jingJie)
        else:
            self.setJingjie(0)
