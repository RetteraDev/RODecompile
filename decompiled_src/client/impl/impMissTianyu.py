#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMissTianyu.o
import gameglobal
import gametypes
from guis import events
import gamelog

class ImpMissTianyu(object):

    def onQueryGroupValMT(self, val):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_MISS_TIANYU_GROUP_PRELIMINARY_HEAT_UPDATE, {'heat': val})

    def onLogOnMT(self, state):
        gamelog.debug('ypc@ onLogOnMT', state)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_ITEM_DYE_SCHEME_CHANGED)
        self.missTianyuState = state

    def isMTInGroupTime(self):
        return self.missTianyuState == gametypes.MISS_TIANYU_GROUP_GAME or self.missTianyuState == gametypes.MISS_TIANYU_GROUP_PROCESS

    def isMTInPlayoffTime(self):
        return self.missTianyuState == gametypes.MISS_TIANYU_PLAY_OFF or self.missTianyuState == gametypes.MISS_TIANYU_REWARD
