#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildLuxuryRankProxy.o
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class GuildLuxuryRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildLuxuryRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankList': self.onGetRankList,
         'getMyRankInfo': self.onGetMyRankInfo}
        self.mediator = None
        self.myRank = 0
        self.myLuxury = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_LUXURY_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_LUXURY_RANK:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_LUXURY_RANK)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_LUXURY_RANK)

    def onGetRankList(self, *arg):
        p = BigWorld.player()
        if p.guild == None:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, ())
            return
        else:
            rankList = []
            data = p.guild.member
            myGbId = p.gbId
            rankList = []
            for memberId in data:
                member = data[memberId]
                memberObj = {}
                memberObj['playerName'] = member.role
                memberObj['gbId'] = member.gbId
                memberObj['school'] = const.SCHOOL_DICT[member.school]
                memberObj['roleId'] = member.roleId
                memberObj['role'] = gametypes.GUILD_ROLE_DICT[member.roleId]
                memberObj['level'] = member.level
                memberObj['luxury'] = '%d' % member.luxury
                memberObj['isSelf'] = myGbId == member.gbId
                if myGbId == member.gbId:
                    self.myLuxury = member.luxury
                rankList.append(memberObj)

            temp = sorted(rankList, key=lambda x: x['roleId'])
            rankList = sorted(temp, key=lambda x: int(x['luxury']), reverse=True)
            for index in xrange(len(rankList)):
                rankList[index]['rank'] = index + 1
                if myGbId == rankList[index]['gbId']:
                    self.myRank = index + 1

            return uiUtils.array2GfxAarry(rankList, True)

    def onGetMyRankInfo(self, *arg):
        ret = {}
        ret['myRank'] = self.myRank
        ret['myLuxury'] = self.myLuxury
        return uiUtils.dict2GfxDict(ret)
