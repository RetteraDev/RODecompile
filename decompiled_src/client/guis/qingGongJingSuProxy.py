#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qingGongJingSuProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import ui
from ui import gbk2unicode
from data import qing_gong_jing_su_data as QGJSD

class QingGongJingSuProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(QingGongJingSuProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.modelMap = {'getInfo': self.onGetInfo,
         'setTextBtnState': self.onSetTextBtnState}
        self.mediator = None
        self.data = None
        self.jingSuVer = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_QING_GONG_JING_SU, self.hide)

    def show(self, data):
        self.jingSuVer = data[0]
        self.data = self.turnData(data[1])
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QING_GONG_JING_SU)

    def turnData(self, oldData):
        if not oldData:
            return
        questList = QGJSD.data[1].get('quests', [])
        if len(questList) <= 0:
            return
        nameSetList = []
        for questNum in xrange(len(questList)):
            questResult = oldData[questNum + 2][1]
            nameSet = set()
            for record in questResult:
                if record[1]:
                    nameSet.add(record[1])

            nameSetList.append(nameSet)

        resultSet = nameSetList[0]
        for nameSet in nameSetList:
            resultSet = resultSet & nameSet

        allTimeList = []
        for idx, name in enumerate(resultSet):
            time = 0
            for questNum in xrange(len(questList)):
                questResult = oldData[questNum + 2][1]
                for record in questResult:
                    if name == record[1]:
                        time += record[2]

            allTimeList.append((idx, name, time))

        oldData.append((0, allTimeList))
        newData = []
        for questNum in xrange(len(questList) + 1):
            questResult = oldData[questNum + 2][1]
            questResult.sort(key=lambda record: record[2])
            tempList = []
            for idx, record in enumerate(questResult):
                tempList.append((idx, record[1], record[2]))

            if len(tempList) < 10:
                for num in xrange(10 - len(tempList)):
                    tempList.append(())

            tempTenList = tempList[:10]
            for idx, record in enumerate(tempList):
                if record and BigWorld.player().roleName == record[1]:
                    if idx > 0:
                        tempTenList.append(tempList[idx - 1])
                    tempTenList.append(tempList[idx])
                    if idx < len(tempList) - 1:
                        tempTenList.append(tempList[idx + 1])
                    break

            newData.append((questNum + 1, tempTenList))

        return newData

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QING_GONG_JING_SU:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            self.data = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QING_GONG_JING_SU)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.data = None

    @ui.callFilter(5, True)
    def showResult(self):
        BigWorld.player().base.getQingGongJingSuResult(1, self.jingSuVer)

    def onGetInfo(self, *arg):
        rankList = self.movie.CreateArray()
        for i in xrange(len(self.data)):
            subRankList = self.movie.CreateArray()
            for j in xrange(len(self.data[i][1])):
                obj = self.movie.CreateObject()
                if self.data[i][1][j]:
                    obj.SetMember('rank', GfxValue(self.data[i][1][j][0]))
                    obj.SetMember('name', GfxValue(gbk2unicode(self.data[i][1][j][1])))
                    obj.SetMember('time', GfxValue(self.data[i][1][j][2]))
                else:
                    obj.SetMember('rank', GfxValue(-1))
                subRankList.SetElement(j, obj)

            rankList.SetElement(i, subRankList)

        return rankList

    def onSetTextBtnState(self, *arg):
        quests = QGJSD.data.get(1, {}).get('quests', ())
        tabIdx = 0
        if len(quests):
            for idx, q in enumerate(quests):
                if q in BigWorld.player().quests:
                    tabIdx = idx
                    break

        return GfxValue(tabIdx)
