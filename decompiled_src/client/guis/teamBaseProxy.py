#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamBaseProxy.o
import BigWorld
from Scaleform import GfxValue
import const
import gamelog
import uiUtils
from uiProxy import UIProxy
from sMath import distance2D
from guis import ui
DIST_AOI = 80
DIST_FAR = 75
DIST_MEDIUM = 50
DIST_NEAR = 25

class TeamBaseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamBaseProxy, self).__init__(uiAdapter)
        self.membersInfo = {}
        self.teamPlayerMed = None
        self.currentBuffData = {}
        self.reset()

    @ui.callInterval()
    def updateBuffData(self, targetRoleName, buffData, defBuff, refresh):
        data = [targetRoleName,
         buffData,
         defBuff,
         refresh]
        inputData = uiUtils.array2GfxAarry(data, True)
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('updateBuff', inputData)

    def showLog(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('showLog', ())
            return

    def freshBuffInfo(self, *arg):
        pos = int(arg[3][0].GetNumber())
        if pos != -1:
            eid = self.memberId[pos]
            entity = self._getEntityById(eid)
            if entity:
                entity.clientBuffRefresh()
        else:
            BigWorld.player()._refreshTeamBuff()

    def reset(self):
        self.oldIndex = -1
        self._resetPlayerProperty()

    def _resetPlayerProperty(self):
        self.oldHp = [ -1 for i in xrange(5) ]
        self.oldMhp = [ -1 for i in xrange(5) ]
        self.oldMp = [ -1 for i in xrange(5) ]
        self.oldMmp = [ -1 for i in xrange(5) ]
        self.oldLv = [ 0 for i in xrange(5) ]
        self.isReal = False
        self.memberId = [ 0 for i in xrange(5) ]
        self.roleNameList = [ '' for i in xrange(5) ]

    def setOldVal(self, index, hp, mhp, mp, mmp, lv):
        if hp >= 0:
            self.oldHp[index] = hp
        if mhp >= 0:
            self.oldMhp[index] = mhp
        if mp >= 0:
            self.oldMp[index] = mp
        if mmp >= 0:
            self.oldMmp[index] = mmp
        if lv >= 0:
            self.oldLv[index] = lv
            self.isReal = True

    def _getEntityById(self, id, maxDist = DIST_AOI):
        if BigWorld.entities.has_key(id):
            p = BigWorld.player()
            ent = BigWorld.entities.get(id)
            if distance2D(p.position, ent.position) <= maxDist:
                self.isReal = True
                return ent

    def getHp(self, index, id):
        return GfxValue(self.getPyHp(index, id))

    def getMhp(self, index, id):
        return GfxValue(self.getPyMhp(index, id))

    def getMp(self, index, id):
        return GfxValue(self.getPyMp(index, id))

    def getMmp(self, index, id):
        return GfxValue(self.getPyMmp(index, id))

    def getPyHp(self, index, id):
        entity = self._getEntityById(id)
        if index >= len(self.oldHp):
            gamelog.error('hjx error in _getHp out of index:', index)
            return 0
        elif entity and hasattr(entity, 'hp'):
            self.oldHp[index] = entity.hp
            return int(entity.hp)
        else:
            return int(self.oldHp[index])

    def getPyMhp(self, index, id):
        entity = self._getEntityById(id, DIST_FAR)
        if index >= len(self.oldMhp):
            gamelog.error('hjx error in _getHp out of index:', index)
            return 0
        elif entity:
            self.oldMhp[index] = entity.mhp
            return int(entity.mhp)
        else:
            return int(self.oldMhp[index])

    def getPyMp(self, index, id):
        entity = self._getEntityById(id)
        if index >= len(self.oldMp):
            gamelog.error('hjx error in _getHp out of index:', index)
            return 0
        elif entity:
            self.oldMp[index] = entity.mp
            return int(entity.mp)
        else:
            return int(self.oldMp[index])

    def getPyMmp(self, index, id):
        entity = self._getEntityById(id, DIST_FAR)
        if index >= len(self.oldMmp):
            gamelog.error('hjx error in _getHp out of index:', index)
            return 0
        elif entity:
            self.oldMmp[index] = entity.mmp
            return int(entity.mmp)
        else:
            return int(self.oldMmp[index])

    def getPyPlayerInfo(self, index, id):
        entity = self._getEntityById(id, DIST_FAR)
        if entity:
            self.oldMmp[index] = entity.mmp
            mmp = int(entity.mmp)
            self.oldMp[index] = entity.mp
            mp = int(entity.mp)
            self.oldHp[index] = entity.hp
            hp = int(entity.hp)
            self.oldMhp[index] = entity.mhp
            mhp = int(entity.mhp)
            return (hp,
             mhp,
             mp,
             mmp)
        else:
            return (self.oldHp[index],
             self.oldMhp[index],
             self.oldMp[index],
             self.oldMmp[index])

    def getLv(self, index, id):
        entity = self._getEntityById(id)
        if index >= len(self.oldLv):
            gamelog.error('hjx error in _getHp out of index:', index)
            return 0
        elif entity:
            self.oldLv[index] = entity.lv
            return int(entity.lv)
        else:
            return int(self.oldLv[index])

    def setHp(self, index, hp, mhp):
        if index == -1:
            return
        elif hp == None or mhp == None:
            return
        else:
            if self.teamPlayerMed:
                self.teamPlayerMed.Invoke('setHp', (GfxValue(index), GfxValue(int(hp)), GfxValue(int(mhp))))
            if getattr(self, 'groupMemMed', None):
                self.groupMemMed.Invoke('setHp', (GfxValue(index), GfxValue(int(hp)), GfxValue(int(mhp))))
            return

    def setMhp(self, index, hp, mhp):
        if index == -1:
            return
        elif hp == None or mhp == None:
            return
        else:
            if self.teamPlayerMed:
                self.teamPlayerMed.Invoke('setMhp', (GfxValue(index), GfxValue(int(hp)), GfxValue(int(mhp))))
            return

    def setMp(self, index, mp, mmp):
        if index == -1:
            return
        elif mp == None or mmp == None:
            return
        else:
            if self.teamPlayerMed:
                self.teamPlayerMed.Invoke('setMp', (GfxValue(index), GfxValue(int(mp)), GfxValue(int(mmp))))
            if getattr(self, 'groupMemMed', None):
                self.groupMemMed.Invoke('setMp', (GfxValue(index), GfxValue(int(mp)), GfxValue(int(mmp))))
            return

    def setMmp(self, index, mp, mmp):
        if index == -1:
            return
        elif mp == None or mmp == None:
            return
        else:
            if self.teamPlayerMed:
                self.teamPlayerMed.Invoke('setMmp', (GfxValue(index), GfxValue(int(mp)), GfxValue(int(mmp))))
            return

    def setLv(self, index, lv):
        if index == -1:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setLv', (GfxValue(index), GfxValue(int(lv))))

    def tweenMp(self, index, time):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('tweenMp', (GfxValue(index), GfxValue(time)))

    def stopTweenMp(self, index):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('stopTweenMp', GfxValue(index))

    def getBuffList(self):
        return self.movie.CreateArray()

    def _resetPropertyByIndex(self, index):
        self.oldHp[index] = 0
        self.oldMhp[index] = 0
        self.oldMp[index] = 0
        self.oldMmp[index] = 0

    def closeTeamPlayer(self):
        p = BigWorld.player()
        p and p.cancelTeamCallback()

    def onGetMemberInfo(self, *arg):
        pass

    def refreshMemberInfo(self, isNeedOpen = True, refreshSelfWidget = True):
        gamelog.debug('@hjx group#super#refreshMemberInfo:', isNeedOpen)
        if isNeedOpen:
            p = BigWorld.player()
            if not p:
                return
            if p.inFubenTypes(const.FB_TYPE_ARENA):
                p.refreshArenaCampInfo()
            elif p.isInPUBG():
                p.refreshMemberInfo()
            elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                p.refreshBattleFieldCampInfo()
            elif p.groupNUID > 0:
                p.refreshMemberInfo()
            p.refreshMemberPos()

    def onSelectTeamPlayer(self, *arg):
        index = int(arg[3][0].GetNumber())
        if not self.oldIndex or self.oldIndex and index != self.oldIndex:
            entity = self._getEntityById(self.memberId[index])
            uiUtils.onTargetSelect(entity)

    def _getTeamIndex(self, id):
        for key, value in enumerate(self.memberId):
            if value and value == id:
                return key

        return -1

    def setTeamHp(self, id, hp, mhp):
        index = self._getTeamIndex(id)
        self.setHp(index, hp, mhp)
        self.setMhp(index, hp, mhp)

    def setTeamMp(self, id, mp, mmp):
        index = self._getTeamIndex(id)
        self.setMp(index, mp, mmp)
        self.setMmp(index, mp, mmp)

    def setTeamLv(self, id, lv):
        index = self._getTeamIndex(id)
        self.setLv(index, lv)
