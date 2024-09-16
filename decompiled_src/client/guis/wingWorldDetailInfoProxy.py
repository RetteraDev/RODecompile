#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldDetailInfoProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import TipManager
from data import wing_world_city_data as WWCD
from data import region_server_config_data as RSCD
from data import wing_world_config_data as WWCFD
from data import wing_city_building_data as WCBD
COUNTRY_MAX_CNT = 3

class WingWorldDetailInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldDetailInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_DETAIL_INFO, self.hide)

    def reset(self):
        self.timer = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_DETAIL_INFO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_DETAIL_INFO)

    def show(self):
        p = BigWorld.player()
        if not p.inWingWarCity():
            return
        else:
            if not self.widget:
                if p.wingWorld.state == gametypes.WING_WORLD_STATE_FINISH:
                    if self.timer:
                        BigWorld.cancelCallback(self.timer)
                        self.timer = None
                    if not self.uiAdapter.wingWorldResult.hadOpened:
                        self.timer = BigWorld.callback(WWCFD.data.get('wingWorldResultDealyShowTime', 3), self.realShow)
                    else:
                        self.realShow()
                    isWin = self.getWinnerHostId() == self.getSelfSideHostId()
                    self.uiAdapter.wingWorldResult.show(isWin)
                else:
                    self.realShow()
            return

    def getSelfSideHostId(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            return p.wingWorldCamp
        else:
            return p.getOriginHostId()

    def realShow(self):
        self.timer = 0
        self.uiAdapter.wingWorldResult.hide()
        self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_DETAIL_INFO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.seekRankBtn.addEventListener(events.BUTTON_CLICK, self.handleSeekRankBtnClick, False, 0, True)
        TipManager.addTip(self.widget.res1, WWCFD.data.get('restype1', ''))
        TipManager.addTip(self.widget.res2, WWCFD.data.get('restype2', ''))
        TipManager.addTip(self.widget.res3, WWCFD.data.get('restype3', ''))

    def getBuildingScore(self, hostId, buildingType, isCore):
        score = 0
        for buildingId in getattr(BigWorld.player(), 'wingWorldCityWarScore', {}).get(hostId, {}).get('buildings', []):
            cfgData = WCBD.data.get(buildingId, {})
            type = cfgData.get('buildingType', 0)
            core = cfgData.get('core', 0)
            if buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD == type:
                score += cfgData.get('score', 100)
            elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_STONE == type and isCore == core:
                score += cfgData.get('score', 100)

        return score

    def getWinnerHostId(self):
        hostId = 0
        isEnd = BigWorld.player().wingWorld.state > gametypes.WING_WORLD_STATE_OPEN
        maxScore = 0
        p = BigWorld.player()
        if isEnd:
            for id, data in getattr(p, 'wingWorldCityWarScore', {}).iteritems():
                score = self.getBuildingScore(id, gametypes.WING_CITY_BUILDING_TYPE_STONE, True) + self.getBuildingScore(id, gametypes.WING_CITY_BUILDING_TYPE_STONE, False) + self.getBuildingScore(id, gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD, True)
                if score > maxScore:
                    maxScore = score
                    hostId = id

        return hostId

    def getIsAtk(self, hostId):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            ownCities = p.wingWorld.country.getCamp(hostId).ownedCityIds
        else:
            ownCities = p.wingWorld.country.getCountry(hostId).ownedCityIds
        return getattr(p, 'wingWorldBattleCityId', 0) not in ownCities

    def getInfo(self):
        p = BigWorld.player()
        info = {}
        info['cityName'] = WWCD.data.get(BigWorld.player().getWingWarCityId(), {}).get('name', '')
        info['isEnd'] = False
        scoreDict = {}
        scoreData = getattr(BigWorld.player(), 'wingWorldCityWarScore', {})
        winnerHostId = self.getWinnerHostId()
        wingWorldMiniMap = BigWorld.player().wingWorldMiniMap
        for hostId, campIdx in wingWorldMiniMap.attendHost2ColorIdx.iteritems():
            scoreInfo = {}
            scoreInfo['isWinner'] = winnerHostId == hostId
            scoreInfo['isAtk'] = self.getIsAtk(hostId)
            import utils
            scoreInfo['countryName'] = utils.getCountryName(hostId)
            scoreInfo['hostId'] = hostId
            scoreInfo['level0Score'] = self.getBuildingScore(hostId, gametypes.WING_CITY_BUILDING_TYPE_STONE, True)
            scoreInfo['level1Score'] = self.getBuildingScore(hostId, gametypes.WING_CITY_BUILDING_TYPE_STONE, False)
            scoreInfo['level2Score'] = self.getBuildingScore(hostId, gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD, True)
            scoreInfo['buildScore'] = scoreInfo['level0Score'] + scoreInfo['level1Score'] + scoreInfo['level2Score']
            dmgScore = scoreData.get(hostId, {}).get('destroyScore', 100 * campIdx)
            dmgScore = gameStrings.WING_WORLD_DMG_SCORE % (dmgScore / 10000.0)
            scoreInfo['dmgScore'] = dmgScore
            scoreInfo['campIdx'] = campIdx
            scoreDict[campIdx] = scoreInfo

        info['scoreDic'] = scoreDict
        info['robResDict'] = scoreData.get(self.getSelfSideHostId(), {}).get('robResDict', {})
        return info

    def refreshInfo(self):
        if not self.widget:
            return
        info = self.getInfo()
        if BigWorld.player().isWingWorldCampMode():
            self.widget.attr0.text = gameStrings.CAMP
        else:
            self.widget.attr0.text = gameStrings.COUNTRY
        self.widget.txtCityName.text = info['cityName']
        scoreDic = info['scoreDic']
        for i in xrange(COUNTRY_MAX_CNT):
            iconWinner = getattr(self.widget, 'iconWinner%d' % i)
            txtCountryName = getattr(self.widget, 'txtCountryName%d' % i)
            iconFlag = getattr(self.widget, 'iconFlag%d' % i)
            bg = getattr(self.widget, 'bg%d' % i)
            txtList = []
            for j in xrange(3):
                txtList.append(getattr(self.widget, 'txt%d%d' % (i, j)))

            txtBuildingScore = getattr(self.widget, 'txtBuildingScore%d' % i)
            txtDmgScore = getattr(self.widget, 'txtDmgScore%d' % i)
            if scoreDic.has_key(i + 1):
                scoreInfo = scoreDic[i + 1]
                iconWinner.visible = scoreInfo['isWinner']
                txtCountryName.text = scoreInfo['countryName']
                iconFlag.visible = True
                iconFlag.gotoAndStop('gong' if scoreInfo['isAtk'] else 'shou')
                txtList[0].text = scoreInfo['level0Score']
                txtList[1].text = scoreInfo['level1Score']
                txtList[2].text = scoreInfo['level2Score']
                txtBuildingScore.text = scoreInfo['buildScore']
                txtDmgScore.text = scoreInfo['dmgScore']
                bg.visible = True
            else:
                iconWinner.visible = False
                txtCountryName.text = ''
                iconFlag.visible = False
                txtList[0].text = ''
                txtList[1].text = ''
                txtList[2].text = ''
                txtBuildingScore.text = ''
                txtDmgScore.text = ''
                bg.visible = False

        self.widget.txtReward0.text = info['robResDict'].get(0, 0)
        self.widget.txtReward1.text = info['robResDict'].get(1, 0)
        self.widget.txtReward2.text = info['robResDict'].get(2, 0)
        tips = WWCFD.data.get('wingWorldIconTips', ('tips0', 'tips1', 'tips2'))
        TipManager.addTip(self.widget.iconTips0, tips[0])
        TipManager.addTip(self.widget.iconTips1, tips[1])
        TipManager.addTip(self.widget.iconTips2, tips[2])

    def handleSeekRankBtnClick(self, *args):
        gamelog.info('jbx:handleSeekRankBtnClick')
        p = BigWorld.player()
        state = p.wingWorld.state
        if state == gametypes.WING_WORLD_STATE_DECLARE_END or state == gametypes.WING_WORLD_STATE_OPEN or state == gametypes.WING_WORLD_STATE_SETTLEMENT:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WAR_TEMP_GUILD_CONTRIBUTE)
        else:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WAR_GUILD_CONTRIBUTE)

    def handleCloseBtnClick(self, *args):
        gamelog.info('jbx:handleCloseBtnClick')
        self.hide()
