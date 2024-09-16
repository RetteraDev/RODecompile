#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildMerger.o
import copy
import random
import BigWorld
import const
import formula
import gamelog
import gametypes
import utils
import gameglobal
from cdata import game_msg_def_data as GMDD

class ImpGuildMerger(object):

    def onRecommendGuildMergerNotify(self):
        gamelog.info('jbx:onRecommendGuildMergerNotify')
        gameglobal.rds.ui.guildMergePush.show()

    def onQueryTargetInfoInGuildMerger(self, name, leaderRole, r, level, onlineMaxNum):
        gamelog.info('jbx:onQueryTargetInfoInGuildMerger', name, leaderRole, r, level, onlineMaxNum)
        if self.isGuildLeader():
            gameglobal.rds.ui.guildMergeStartConfirm.show(name, leaderRole, r, level, onlineMaxNum)

    def onReceiveGuildMerger(self, fGuildNUID, leaderRole, name):
        gamelog.info('jbx:onReceiveGuildMerger', fGuildNUID, leaderRole, name)
        if self.isGuildLeader():
            gameglobal.rds.ui.guildMergeAccept.show(fGuildNUID, leaderRole, name)

    def onUpdateGuildMergerVal(self, guildNUID, valDTO):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gamelog.info('jbx:onUpdateGuildMergerVal', guildNUID, valDTO)
        self.guild.guildMergerVal.fromDTO(valDTO)

    def onUpdateGuildMergerActivityStartTime(self, guildNUID, startTime):
        if not self.guild or guildNUID != self.guild.nuid:
            return
        gamelog.info('jbx:onUpdateGuildMergerActivityStartTime', guildNUID, startTime)
        self.guildMergeActivityStartTime = startTime

    def onUpdateIgnoreRecommendGuildMergerFlag(self, guildNUID, flag):
        gamelog.info('jbx:onUpdateIgnoreRecommendGuildMergerFlag', guildNUID, flag)
        self.ignoreRecommendGuildMerger = flag

    def onShowGuildBonfireInGuildMergerDura(self):
        if not self.guild:
            return
        gamelog.info('jbx:onShowGuildBonfireInGuildMergerDura')
        gameglobal.rds.ui.guildMergeBonfire.show()

    def onClapForGuildMergerMemberSucc(self):
        gamelog.info('jbx:onClapForGuildMergerMemberSucc')
        gameglobal.rds.ui.guildMergeBonfire.hide(False)
