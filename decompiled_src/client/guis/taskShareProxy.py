#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/taskShareProxy.o
from gamestrings import gameStrings
import types
import re
import Math
import BigWorld
from Scaleform import GfxValue
import gameglobal
import commQuest
import gamelog
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from guis.uiProxy import DataProxy
from data import item_data as ID
from data import quest_data as QD
from data import seeker_data as SD
from cdata import font_config_data as FCD

class TaskShareProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(TaskShareProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTaskDetail': self.onGetTaskDetail,
         'autoFindPath': self.onAutoFindPath,
         'acceptTask': self.onAcceptTask,
         'closeShare': self.onCloseShare,
         'showPosition': self.onShowPosition}
        self.isShow = False
        self.questId = None
        self.questDetail = None
        self.ownerId = None

    def onGetTaskDetail(self, *arg):
        ret = self.movie.CreateArray()
        info = self.questDetail
        taskPlace = info.get('taskPlace', '')
        if taskPlace:
            taskPlace = gameStrings.TEXT_TIANYUMALLPROXY_1486 + taskPlace + gameStrings.TEXT_ITEMQUESTPROXY_85_1
        ret.SetElement(0, GfxValue(gbk2unicode(taskPlace)))
        ret.SetElement(1, GfxValue(gbk2unicode(info.get('taskName', ''))))
        ret.SetElement(2, GfxValue(gbk2unicode(info.get('taskDesc', ''))))
        ret.SetElement(3, GfxValue(commQuest.questFailCheck(BigWorld.player(), info['id'])))
        goal = self.movie.CreateArray()
        i = 0
        for item in info.get('taskGoal', []):
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(self._genDesc(item[0]))))
            ar.SetElement(1, GfxValue(item[1]))
            ar.SetElement(2, GfxValue(item[3]))
            ar.SetElement(3, GfxValue(item[2]))
            ar.SetElement(4, GfxValue(gbk2unicode(self._genRate(item[0]))))
            goal.SetElement(i, ar)
            i += 1

        ret.SetElement(4, goal)
        ret.SetElement(5, GfxValue(info.get('taskDeliveryNPCTk', '')))
        ret.SetElement(6, GfxValue(gbk2unicode(info.get('taskDeliveryNPC', ''))))
        ret.SetElement(7, GfxValue(QD.data.get(self.questId, {}).get('type', 1)))
        award = self.movie.CreateObject()
        award.SetMember('money', GfxValue(int(info.get('taskAward', {}).get('money', 0))))
        award.SetMember('exp', GfxValue(int(info.get('taskAward', {}).get('exp', 0))))
        itemList = self.movie.CreateArray()
        i = 0
        for item in info.get('taskAward', {}).get('icon', []):
            ar = self.movie.CreateArray()
            path = uiUtils.getItemIconFile40(item[0])
            ar.SetElement(0, GfxValue(path))
            ar.SetElement(1, GfxValue(item[1]))
            quality = ID.data.get(item[0], {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#FFFFFF')[1:]
            ar.SetElement(2, GfxValue(color))
            ar.SetElement(3, GfxValue(item[0]))
            itemList.SetElement(i, ar)
            i += 1

        award.SetMember('icon', itemList)
        choiceList = self.movie.CreateArray()
        i = 0
        for item in info.get('rewardChoice', []):
            ar = self.movie.CreateArray()
            path = uiUtils.getItemIconFile40(item[0])
            ar.SetElement(0, GfxValue(path))
            ar.SetElement(1, GfxValue(item[1]))
            quality = ID.data.get(item[0], {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#FFFFFF')[1:]
            ar.SetElement(2, GfxValue(color))
            ar.SetElement(3, GfxValue(item[0]))
            choiceList.SetElement(i, ar)
            i += 1

        award.SetMember('choiceIcon', choiceList)
        award.SetMember('moneyUp', GfxValue(info.get('moneyUp', False)))
        award.SetMember('expUp', GfxValue(info.get('expUp', False)))
        ret.SetElement(8, award)
        return ret

    def onAutoFindPath(self, *arg):
        id = arg[3][0].GetString()
        gamelog.debug('wy:onAutoFindPath', id)
        gameglobal.rds.ui.questTrack.findNPC(id)

    def onAcceptTask(self, *arg):
        gamelog.debug('wy:onAcceptTask', self.questId, self.ownerId)
        BigWorld.player().cell.acceptQuestByShared(self.questId, self.ownerId)

    def onCloseShare(self, *arg):
        self.close()

    def onShowPosition(self, *arg):
        id = arg[3][0].GetString()
        id = eval(id)
        p = BigWorld.player()
        if type(id) == types.TupleType:
            idList = list(id)
            minDis = -1
            index = 0
            for item in idList:
                data = SD.data.get(item, None)
                if data:
                    pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                    spaceNo = data['spaceNo']
                    if p.spaceNo == spaceNo:
                        tempDis = (p.position - pos).length
                        if minDis == -1 or minDis > tempDis:
                            minDis = tempDis
                            index = item

            id = index
        if id == 0:
            return GfxValue('')
        elif SD.data.has_key(id):
            sd = SD.data.get(id, {})
            return GfxValue('%d , %d, %d' % (sd.get('xpos', 0), sd.get('zpos', 0), sd.get('ypos', 0)))
        else:
            return

    def show(self, ownerId, questId):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TASK_SHARE)
        self.isShow = True
        self.questId = questId
        self.ownerId = ownerId
        self.questDetail = BigWorld.player().genQuestDetail(questId, -1, True, gameglobal.rds.ui.questLog.isAvailable)

    def close(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TASK_SHARE)
        self.isShow = False

    def _genDesc(self, desc):
        return re.sub(gameStrings.TEXT_QUESTTRACKPROXY_231, '', desc)

    def _genRate(self, desc):
        ret = re.findall(gameStrings.TEXT_QUESTTRACKPROXY_231, desc)
        if len(ret) > 0:
            ret = ret[0]
        else:
            ret = ''
        return ret
