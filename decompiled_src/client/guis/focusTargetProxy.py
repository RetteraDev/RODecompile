#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/focusTargetProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from Scaleform import GfxValue
from cdata import game_msg_def_data as GMDD

class FocusTargetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FocusTargetProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerTargetFrame': self.onRegisterTargetFrame,
         'targetSelect': self.onTargetSelect,
         'focusSelect': self.onFocusSelect}
        self.mediator = None
        self.oldDistance = ''
        self.targetDirHandle = None
        self.focusTarId = None
        self.masterId = None
        self.tar2tarId = None
        self.tar2tarMasterId = None
        self.enterState = True

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        BigWorld.callback(0, self.refreshHideBloodState)

    def show(self):
        pass

    def showFocus(self, focusTarId = None):
        p = BigWorld.player()
        if focusTarId == None:
            if p.targetLocked:
                self.setTarget(p.targetLocked.id)
            else:
                p.showGameMsg(GMDD.data.NOT_HAVE_FOCUS, ())
        else:
            self.setTarget(focusTarId)

    def setTarget(self, focusTarId):
        p = BigWorld.player()
        focusTar = BigWorld.entities.get(focusTarId)
        if focusTar and (focusTar.IsAvatarOrPuppet or focusTar.IsMonster):
            if self.mediator == None:
                self.setMonsterId(focusTarId)
                self.uiAdapter.loadWidget(uiConst.WIDGET_FOCUS_TARGET)
                return
            if focusTarId != self.focusTarId:
                self.setMonsterId(focusTarId)
                self.refreshAllProperty()
            else:
                self.hide()
        else:
            p.showGameMsg(GMDD.data.NOT_HAVE_NPC_FOCUS, ())

    def menuShowFocus(self, focusTarId):
        self.showFocus(focusTarId)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FOCUS_TARGET)

    def reset(self):
        self.mediator = None
        self.oldDistance = ''
        self.focusTarId = None
        self.masterId = None
        self.tar2tarId = None
        self.tar2tarMasterId = None
        self.enterState = True
        if self.targetDirHandle:
            BigWorld.cancelCallback(self.targetDirHandle)
            self.targetDirHandle = None

    def onRegisterTargetFrame(self, *arg):
        self.refreshAllProperty()

    def setActive(self, active):
        if self.mediator:
            self.mediator.Invoke('setActive', GfxValue(active))

    def setEntityId(self, entityId):
        if self.mediator:
            self.mediator.Invoke('setEntityId', GfxValue(entityId))

    def setName(self, name):
        if self.mediator:
            self.mediator.Invoke('setName', GfxValue(gbk2unicode(name)))

    def setLevel(self, lv):
        if self.mediator:
            self.mediator.Invoke('setLevel', GfxValue(lv))

    def setHp(self, hp):
        if hp is None:
            return
        else:
            if self.mediator:
                self.mediator.Invoke('setHp', GfxValue(int(hp)))
            return

    def setMhp(self, mhp):
        if self.mediator:
            self.mediator.Invoke('setMhp', GfxValue(int(mhp)))

    def updateTargetDir(self):
        if not BigWorld.player():
            return
        if self.targetDirHandle:
            BigWorld.cancelCallback(self.targetDirHandle)
        ent = BigWorld.entities.get(self.focusTarId)
        if ent and (ent.IsAvatar or ent.IsMonster):
            distance = gbk2unicode(str(self.getTargetLockDist()) + gameStrings.TEXT_AIMCROSS_248)
            if distance != self.oldDistance:
                self.setDistance(distance)
                self.oldDistance = distance
            self.targetDirHandle = BigWorld.callback(0.5, self.updateTargetDir)

    def getTargetLockDist(self):
        p = BigWorld.player()
        focusTar = BigWorld.entities.get(self.focusTarId)
        if not focusTar:
            return -1
        try:
            ret = int((focusTar.position - p.position).length)
        except:
            ret = -1

        return ret

    def setDistance(self, dis):
        if self.mediator:
            self.mediator.Invoke('setDistance', GfxValue(dis))

    def onTargetSelect(self, *arg):
        ent = BigWorld.entities.get(self.tar2tarId)
        if ent:
            uiUtils.onTargetSelect(ent)

    def onFocusSelect(self, *arg):
        p = BigWorld.player()
        if self.mediator:
            ent = BigWorld.entities.get(self.focusTarId)
            if ent:
                uiUtils.onTargetSelect(ent)
        else:
            p.showGameMsg(GMDD.data.NOT_HAVE_FOCUSTARGET, ())

    def setTargetName(self, name):
        if self.mediator:
            self.mediator.Invoke('setTargetName', GfxValue(gbk2unicode(name)))

    def setTargetNameVisible(self, bVisible):
        if self.mediator:
            self.mediator.Invoke('setTargetNameVisible', GfxValue(bVisible))

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

    def setSchool(self, school):
        if self.mediator:
            self.mediator.Invoke('setSchool', GfxValue(school))

    def setTargetLockName(self, id):
        p = BigWorld.player()
        ent = BigWorld.entities.get(id)
        if ent == None or not getattr(ent, 'roleName', None):
            self.setTargetNameVisible(False)
        else:
            self.setTar2tarMonsterId(id)
            self.setTargetNameVisible(True)
            if p.isInSSCorTeamSSC() and ent.IsAvatar:
                self.setTargetName(gameStrings.TEXT_FOCUSTARGETPROXY_210)
            elif p.bHideFightForLoveFighterName(ent) and ent.IsAvatar:
                nameInfo = p.getFightForLoveNameInfo()
                self.setTargetName(nameInfo.get('name', ''))
            elif getattr(ent, 'roleName', None):
                roleName = p.anonymNameMgr.checkNeedAnonymousName(ent, ent.roleName)
                self.setTargetName(roleName)
            if ent.__class__.__name__ == 'VirtualMonster':
                master = BigWorld.entities.get(ent.masterMonsterID)
                self.tar2tarMasterId = ent.masterMonsterID
            else:
                master = ent
                self.tar2tarMasterId = None
            if master and hasattr(master, 'hp'):
                self.setTargetHp(master.hp)
            if master and hasattr(master, 'mhp'):
                self.setTargetMhp(master.mhp)

    def enterView(self):
        if self.enterState:
            if self.mediator:
                self.mediator.Invoke('setOutFocus', GfxValue(False))
                self.enterState = False

    def leaveView(self):
        if not self.enterState:
            if self.mediator:
                self.mediator.Invoke('setOutFocus', GfxValue(True))
                self.enterState = True

    def refreshAllProperty(self):
        p = BigWorld.player()
        focusTar = BigWorld.entities.get(self.focusTarId)
        if focusTar and (focusTar.IsAvatarOrPuppet or focusTar.IsMonster):
            data = {}
            data['entityId'] = self.focusTarId if focusTar else 0
            if hasattr(focusTar, 'realSchool'):
                data['school'] = focusTar.realSchool
            elif focusTar.IsMonster or focusTar.IsSummonedBeast:
                if focusTar.monsterStrengthType == gametypes.MONSTER_ELITE:
                    data['school'] = '-2'
                else:
                    data['school'] = '-1'
            if p.isInSSCorTeamSSC() and focusTar.IsAvatar:
                data['name'] = gameStrings.TEXT_FOCUSTARGETPROXY_210
            elif p.bHideFightForLoveFighterName(focusTar) and focusTar.IsAvatar:
                nameInfo = p.getFightForLoveNameInfo()
                data['name'] = nameInfo.get('name', '')
            elif hasattr(focusTar, 'roleName'):
                data['name'] = p.anonymNameMgr.checkNeedAnonymousName(focusTar, focusTar.roleName)
            else:
                data['name'] = ''
            data['level'] = focusTar.lv if hasattr(focusTar, 'lv') else 0
            if p.isInSSCorTeamSSC() and hasattr(focusTar, 'IsAvatar') and focusTar.IsAvatar:
                data['level'] = 'Lv.%s' % str(focusTar.realLv)
            data['hp'] = focusTar.hp if hasattr(focusTar, 'hp') else 0
            data['mhp'] = focusTar.mhp if hasattr(focusTar, 'mhp') else 0
            self.setTar2tarMonsterId(getattr(focusTar, 'lockedId', None))
            if self.tar2tarId:
                tar2tar = BigWorld.entities.get(self.tar2tarId)
                data['tVisible'] = True
                if p.isInSSCorTeamSSC() and tar2tar.IsAvatar:
                    data['tName'] = gameStrings.TEXT_FOCUSTARGETPROXY_210
                elif p.bHideFightForLoveFighterName(tar2tar) and tar2tar.IsAvatar:
                    nameInfo = p.getFightForLoveNameInfo()
                    data['tName'] = nameInfo.get('name', '')
                elif hasattr(tar2tar, 'roleName'):
                    data['tName'] = p.anonymNameMgr.checkNeedAnonymousName(tar2tar, tar2tar.roleName)
                else:
                    data['tName'] = ''
                data['tHp'] = tar2tar.hp if hasattr(tar2tar, 'hp') else 0
                data['tMhp'] = tar2tar.mhp if hasattr(tar2tar, 'mhp') else 0
            else:
                data['tVisible'] = False
            if getattr(focusTar, 'monsterStrengthType', None) in gametypes.MONSTER_BOSS_TYPE:
                data['isBoss'] = True
            else:
                data['isBoss'] = False
            if self.mediator:
                self.mediator.Invoke('refreshAllProperty', uiUtils.dict2GfxDict(data, True))
                if self.targetDirHandle == None:
                    self.updateTargetDir()
        else:
            p.showGameMsg(GMDD.data.NOT_HAVE_NPC_FOCUS, ())
        self.refreshHideBloodState()

    def setMonsterId(self, monsterId):
        if monsterId:
            self.focusTarId = monsterId
            ent = BigWorld.entities.get(monsterId)
            if ent:
                if ent.__class__.__name__ == 'VirtualMonster':
                    self.masterId = ent.masterMonsterID
                else:
                    self.masterId = None
        else:
            self.focusTarId = None
            self.masterId = None

    def setTar2tarMonsterId(self, monsterId):
        if monsterId:
            self.tar2tarId = monsterId
            ent = BigWorld.entities.get(monsterId, None)
            if ent:
                if ent.__class__.__name__ == 'VirtualMonster':
                    self.tar2tarMasterId = ent.masterMonsterID
                else:
                    self.tar2tarMasterId = None
        else:
            self.tar2tarId = None
            self.tar2tarMasterId = None

    def refreshHideBloodState(self):
        if not self.mediator:
            return
        else:
            if self.focusTarId:
                focusEntiy = BigWorld.entities.get(self.focusTarId, None)
                if not focusEntiy:
                    return
                focusEntiyHideBloodNum = getattr(focusEntiy, 'isHideBloodNum', False)
                focusId = getattr(focusEntiy, 'lockedId', 0)
                target2HideBloodNum = False
                target2 = BigWorld.entities.get(focusId, None)
                if target2:
                    target2HideBloodNum = getattr(target2, 'isHideBloodNum', False)
                self.mediator.Invoke('setHideBloodState', uiUtils.array2GfxAarry((focusEntiyHideBloodNum, target2HideBloodNum)))
                if hasattr(focusEntiy, 'hp') and hasattr(focusEntiy, 'mhp'):
                    self.setMhp(focusEntiy.mhp)
                    self.setHp(focusEntiy.hp)
                if not target2HideBloodNum and target2 and hasattr(target2, 'hp') and hasattr(target2, 'mhp'):
                    self.setTargetMhp(target2.mhp)
                    self.setTargetHp(target2.hp)
            return
