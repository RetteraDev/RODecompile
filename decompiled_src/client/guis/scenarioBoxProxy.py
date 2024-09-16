#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/scenarioBoxProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy
from data import sys_config_data as SCD
from data import scenario_data as SCND
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from helpers import scenario
from guis import uiUtils
import gamelog

class ScenarioBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ScenarioBoxProxy, self).__init__(uiAdapter)
        self.modelMap = {'skipScenario': self.onSkipScenario,
         'getCurrentMsgData': self.onGetCurrentMsgData,
         'cancelDialog': self.onCancelDialog}
        self.isShow = False
        self.med = None
        self.reset()

    def reset(self):
        self.dismiss()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SCENARIO_BOX:
            self.med = mediator

    def onGetCurrentMsgData(self, *arg):
        currentPlayingId = self._getCurrentPlayScenarioID()
        usedData = SCND.data.get(currentPlayingId, 0)
        storyPoint = usedData.get('storyPoint', 0)
        frameId = SCD.data.get('storyPointFameId', 0)
        currentHavePoint = BigWorld.player().fame.get(frameId, 0)
        currentItemList = usedData.get('itemList', [])
        finalItemList = []
        for item in currentItemList:
            iconPath = uiUtils.getItemIconFile64(item[0])
            count = item[1]
            color = uiUtils.getItemColor(item[0])
            finalItemList.append([iconPath,
             count,
             color,
             item[0]])

        currentItemPointList = usedData.get('itemPoint', [])
        msg = GMD.data.get(GMDD.data.SKIP_PLAY_SCENARIO_CONFIRM, {}).get('text', gameStrings.TEXT_SCENARIOBOXPROXY_58)
        msg = msg % storyPoint
        msg2 = []
        for item in currentItemPointList:
            needPoint = item - currentHavePoint
            tmpMsg = ''
            if needPoint > 0:
                tmpMsg = GMD.data.get(GMDD.data.SKIP_PLAY_SCENARIO_NEED_POINT, {}).get('text', gameStrings.TEXT_SCENARIOBOXPROXY_65)
                tmpMsg = tmpMsg % needPoint
            else:
                tmpMsg = GMD.data.get(GMDD.data.SKIP_PLAY_SCENARIO_CAN_GET, {}).get('text', gameStrings.TEXT_SCENARIOBOXPROXY_68)
            msg2.append(gbk2unicode(tmpMsg))

        ret = [GfxValue(gbk2unicode(msg)), uiUtils.array2GfxAarry(msg2), uiUtils.array2GfxAarry(finalItemList)]
        return uiUtils.array2GfxAarry(ret)

    def _getCurrentPlayScenarioName(self):
        scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
        if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return scenarioIns.name
        else:
            return None

    def _getCurrentPlayScenarioID(self):
        name = self._getCurrentPlayScenarioName()
        for scenarioId, data in SCND.data.iteritems():
            fullname = 'intro/scenario/' + data.get('name')
            if fullname == name:
                return scenarioId

        return -1

    def onSkipScenario(self, *arg):
        scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
        if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.QUIT_SCENARIO_PLAY, ())
            scenarioIns.stopPlay()

    def onCancelDialog(self, *arg):
        self.dismiss()

    def show(self):
        currentPlayingId = self._getCurrentPlayScenarioID()
        usedData = SCND.data.get(currentPlayingId, {})
        if usedData:
            storyPoint = usedData.get('storyPoint', 0)
            if not self.isShow and storyPoint > 0:
                self.isShow = True
                self.uiAdapter.loadWidget(uiConst.WIDGET_SCENARIO_BOX)
            elif storyPoint <= 0:
                scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
                if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                    p = BigWorld.player()
                    p.showGameMsg(GMDD.data.QUIT_SCENARIO_PLAY, ())
                    scenarioIns.stopPlay()
        else:
            scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
            if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                p = BigWorld.player()
                p.showGameMsg(GMDD.data.QUIT_SCENARIO_PLAY, ())
                scenarioIns.stopPlay()

    def dismiss(self):
        if self.isShow:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCENARIO_BOX)
        self.isShow = False
        self.med = None
