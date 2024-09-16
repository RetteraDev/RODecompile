#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/gfeManager.o
import BigWorld
import Gfe
import const
import gameglobal
from gameclass import Singleton
from cdata import game_msg_def_data as GMDD

def getInstance():
    return GfeManager.getInstance()


class GfeManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.inited = False
        self.isRecording = False
        self.beforeNum = 0
        self.afterNum = 0
        self.beforeNumState = 1
        self.afterNumState = 1

    def initGfe(self):
        if not gameglobal.rds.configData.get('enableAutoTakeVideo', False):
            return
        if self.inited:
            return
        self.inited = Gfe.init()
        if self.inited:
            hl = [('highlight1', 'marriage', 11, 21)]
            result = Gfe.configureHighlights(hl)
            g = [('group1', 'Group One')]
            result = Gfe.openGroups(g)

    def screenshotMark(self):
        Gfe.screenshotMark('group1', 'highlight1')

    def takeVideoByMarriageScenario(self, beginTime, endTime):
        if not gameglobal.rds.configData.get('enableAutoTakeVideo', False):
            return
        if not self.inited:
            return
        if self.isRecording:
            return

        def _beforeFunc(num):
            self.beforeNum = num
            Gfe.videoMark('group1', 'highlight1', int(beginTime), int(endTime))
            self.curVideoType = const.NV_VIDEO_TYPE_MARRIAGE
            self.isRecording = True

        self.beforeNumState = Gfe.onGetNumHighlights('group1', _beforeFunc)

        def _afterFunc():
            self.afterNumState = Gfe.onGetNumHighlights('group1', self.afterHlNumCallBack)
            if self.beforeNumState == -1 and self.isRecording:
                self.isRecording = False

        BigWorld.callback(endTime / 1000 + 1, _afterFunc)

    def afterHlNumCallBack(self, num):
        if num > self.beforeNum or self.beforeNumState == -1:
            self.beforeNum = num
            p = BigWorld.player()
            if self.isRecording and self.curVideoType == const.NV_VIDEO_TYPE_MARRIAGE:
                p.showGameMsg(GMDD.data.TAKE_MARRIAGE_VIDEO_SUCCESS, ())
            self.curVideoType = None
            self.isRecording = False

    def getCurVideoType(self):
        return self.curVideoType

    def closeGfe(self):
        Gfe.closeGroups()
        Gfe.shutdown()

    def getContent(self):
        Gfe.summary('group1')
