#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamEnemyArenaProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gamelog
import formula
import utils
from ui import gbk2unicode
from teamBaseProxy import TeamBaseProxy
from data import school_data as SD
from data import arena_mode_data as AMD

class TeamEnemyArenaProxy(TeamBaseProxy):

    def __init__(self, uiAdapter):
        super(TeamEnemyArenaProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMemberInfo': self.onGetMemberInfo,
         'selectTeamPlayer': self.onSelectTeamPlayer}
        self.teamPlayerMed = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ARENA_ENEMY_TEAM:
            self.teamPlayerMed = mediator

    def closeTeamPlayer(self):
        super(TeamEnemyArenaProxy, self).closeTeamPlayer()
        self.teamPlayerMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_ENEMY_TEAM)
        self._resetPlayerProperty()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.teamPlayerMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_ENEMY_TEAM)

    def onGetMemberInfo(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        index = 0
        fbNo = formula.getFubenNo(p.spaceNo)
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        for key, value in p.arenaTeam.iteritems():
            if not p._checkValidSchool(value['school']):
                continue
            if value['sideNUID'] == p.sideNUID or p.inClanChallengeOb() and p.guild and p.guild.nuid == value['sideNUID']:
                continue
            if not value['isIn']:
                continue
            if AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
                lv = formula.calcArenaLv(arenaMode, value['level'])
            else:
                lv = value['level']
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(utils.getRealRoleName(value['roleName']))))
            ar.SetElement(1, GfxValue(lv))
            ar.SetElement(2, GfxValue(value['school']))
            ar.SetElement(3, GfxValue(False))
            ar.SetElement(4, self.getHp(index, value['id']))
            ar.SetElement(5, self.getMhp(index, value['id']))
            ar.SetElement(6, self.getMp(index, value['id']))
            ar.SetElement(7, self.getMmp(index, value['id']))
            ar.SetElement(8, self.getBuffList())
            ar.SetElement(9, GfxValue(value['isOn']))
            ar.SetElement(10, GfxValue(True))
            ret.SetElement(index, ar)
            self.memberId[index] = value['id']
            index += 1

        for i in xrange(index, const.TEAM_MAX_NUMBER):
            self._resetPropertyByIndex(i)

        return ret

    def refreshMemberInfo(self, isNeedOpen = True):
        super(TeamEnemyArenaProxy, self).refreshMemberInfo(isNeedOpen)
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshInfo')
        elif isNeedOpen:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_ENEMY_TEAM)

    def onSelectTeamPlayer(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        gamelog.debug('hjx debug onSelectTeamPlayer0', index)
        if index != -1:
            entity = self._getEntityById(self.memberId[index])
            if entity:
                p.lockTarget(entity)
                gamelog.debug('hjx debug onSelectTeamPlayer1', self.memberId[index], entity.roleName)
