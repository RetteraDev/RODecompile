#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarRobRankProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import clientUtils
import gametypes
import const
from uiProxy import UIProxy
from guis import uiUtils
from guis import uiConst
from data import world_war_config_data as WWCD
from cdata import top_reward_data as TRD

class WorldWarRobRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldWarRobRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getWWRobRankData': self.onGetWWRobRankData}
        self.mediator = None
        self.wwRobRankData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_WAR_ROB_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        initData = {'playerSchool': p.physique.school}
        self.mediator = mediator
        if initData:
            return uiUtils.dict2GfxDict(initData, True)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WORLD_WAR_ROB_RANK)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WORLD_WAR_ROB_RANK)

    def onGetWWRobRankData(self, *args):
        school = int(args[3][0].GetNumber())
        ver, _ = self.wwRobRankData.get(school, (0, []))
        spaceNo = BigWorld.player().spaceNo
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            key = str(school) + '_' + str(gametypes.WORLD_WAR_TYPE_ROB)
            if spaceNo == const.SPACE_NO_WORLD_WAR_ROB_YOUNG:
                key = str(school) + '_' + str(gametypes.WORLD_WAR_TYPE_ROB_YOUNG)
        else:
            key = str(school) + '_' + str(gametypes.WORLD_WAR_TYPE_NORMAL)
        BigWorld.player().base.getTopWWRobScore(ver, key)
        return uiUtils.dict2GfxDict(self.getWWRobRankData(school), True)

    def getWWRobRankData(self, school):
        ret = {}
        p = BigWorld.player()
        ww = p.worldWar
        ret['myContribute'] = str(ww.robScore)
        rankList = []
        _, val = self.wwRobRankData.get(school, (0, []))
        if val:
            for item in val[1]:
                name = item[1]
                tmpSchool = item[2]
                contribute = item[3]
                rankList.append({'playerName': name,
                 'school': const.SCHOOL_DICT.get('tmpSchool', ''),
                 'contribute': contribute})

        rankList.sort(cmp=lambda x, y: cmp(x.get('contribute', 0), y.get('contribute', 0)), reverse=True)
        ret['list'] = rankList
        rankItem = {}
        if school == p.physique.school:
            ret['playerRank'] = 0
            for idx, val in enumerate(rankList):
                if val.get('playerName') == p.realRoleName:
                    ret['playerRank'] = idx + 1
                    rankItem = self.getWWRobRankReward(ret['playerRank'])
                    break

        else:
            ret['playerRank'] = -1
        if ret['playerRank'] == 0:
            rankItem = self.getWWRobRankReward()
            ret['playerRankTxt'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        if rankItem.get('bonusId', 0):
            ret['desc'] = rankItem.get('desc', '') + gameStrings.TEXT_WORLDWARROBRANKPROXY_87
        else:
            ret['desc'] = ''
        bonusId = rankItem.get('bonusId', 0)
        if bonusId:
            itemId, cnt = clientUtils.genItemBonus(bonusId)[0]
            ret['reward'] = uiUtils.getGfxItemById(itemId, cnt)
        ret['rule'] = WWCD.data.get('wwrRankRules', '')
        return ret

    def getWWRobRankReward(self, rank = 0):
        p = BigWorld.player()
        rankType = gametypes.TOP_TYPE_WW_ROB_SCORE
        if p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_ROB:
            rankType = gametypes.TOP_TYPE_WW_ROB_SCORE_QL
        elif p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            rankType = gametypes.TOP_TYPE_WW_ROB_SCORE_BH
        if not rank:
            rankItem = TRD.data.get((rankType, 0, 0), ())[-1]
            return rankItem
        else:
            for rankItem in TRD.data.get((rankType, 0, 0), ()):
                rankStart, rankEnd = rankItem.get('rankRange')
                if rank >= rankStart and rank <= rankEnd:
                    return rankItem

            return {}

    def setWWRobTopData(self, data):
        ver = data[0]
        strList = data[3].split('_')
        school = int(strList[0])
        self.wwRobRankData[school] = (ver, data)
        if self.mediator:
            selSchool = int(self.mediator.Invoke('getSelectedSchool').GetNumber())
            if selSchool == school:
                self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self.getWWRobRankData(selSchool), True))
