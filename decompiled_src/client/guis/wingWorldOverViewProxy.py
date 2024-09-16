#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldOverViewProxy.o
import BigWorld
from Scaleform import GfxValue
import wingWorldUtils
import gameglobal
import gamelog
import utils
import events
import gametypes
from appSetting import Obj as AppSettings
from gamestrings import gameStrings
import keys
from callbackHelper import Functor
from helpers import taboo
from guis import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import uiUtils
from guis.asObject import TipManager
from data import region_server_config_data as RSCD
from data import wing_world_country_flag_data as WWCFD
from data import wing_world_country_power_level_data as WWCPLD
from data import wing_world_config_data as WWCD
from data import wing_world_city_data as WWCTD
from data import wing_world_country_title_data as WWCTTD
from data import wing_world_data as WWD
from data import wing_world_country_event_data as WWCED
from data import wing_world_season_event_data as WWSED
from data import wing_world_config_data as WWCFGD
from cdata import game_msg_def_data as GMDD
from data import wing_world_camp_army_data as WWCAD
IMPAGE_PATH = 'wingWorld/wingWorldFlagBig/%s.dds'
WING_WORLD_NOT_MARK = 1
WING_WORLD_MARKED = 2
MARK_MAX_CNT = 3
MARK_SCORE_MAX = 5
COUNTRY_EVENT_SELECTED = 1
SEASON_EVENT_SELECTED = 2

class WingWorldOverViewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldOverViewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.isInEdit = False
        self.reset()

    def initPanel(self, widget):
        gamelog.info('jbx:initPanel')
        p = BigWorld.player()
        wingWorldArmyMarkScore = getattr(p, 'wingWorldArmyMarkScore', ({}, 0))
        gamelog.info('jbx:queryWingWorldArmyMark', wingWorldArmyMarkScore[1])
        p.cell.queryWingWorldArmyMark(wingWorldArmyMarkScore[1])
        p.cell.queryWingWorldArmy(p.wingWorld.armyVer, p.wingWorld.armyOnlineVer)
        gamelog.info('jbx:queryWingWorldResume', p.wingWorld.state, p.wingWorld.country, p.wingWorld.cityVer)
        self.queryServerInfo()
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        p.cell.queryWingWorldResume(p.wingWorld.state, p.wingWorld.briefVer, p.wingWorld.countryVer, p.wingWorld.cityVer, p.wingWorld.campVer)
        p.cell.queryWingSeasonAndWorldEvents()
        self.queryCampNotice()

    def unRegisterPanel(self):
        gamelog.info('jbx:unRegisterPanel')
        if self.widget and self.widget.stage:
            self.widget.removeChild(self.textItemRender)
        self.textItemRender = None
        self.reset()

    def reset(self):
        self.textItemRender = None
        self.widget = None
        self.selectedEventType = COUNTRY_EVENT_SELECTED
        self.eventList = []

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        getOriginHostId = p.getOriginHostId()
        self.widget.mainMc.txtCountryName.text = RSCD.data.get(getOriginHostId, {}).get('serverName', '')
        self.widget.mainMc.zhanXunRankBtn.addEventListener(events.BUTTON_CLICK, self.handleZhanXunRankBtnClick, False, 0, True)
        self.widget.mainMc.junZiRankBtn.addEventListener(events.BUTTON_CLICK, self.handleZhanXunRankBtnClick, False, 0, True)
        self.widget.mainMc.voteBtn.addEventListener(events.BUTTON_CLICK, self.handleVoteBtnClick, False, 0, True)
        self.widget.mainMc.changeIconBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeIconBtnClick, False, 0, True)
        self.widget.mainMc.countryEventBtn.addEventListener(events.BUTTON_CLICK, self.handleCountryEventBtnClick, False, 0, True)
        self.widget.mainMc.seasonEventBtn.addEventListener(events.BUTTON_CLICK, self.handleSeasonEventBtnClick, False, 0, True)
        self.widget.mainMc.countryEvent.addEventListener(events.BUTTON_CLICK, self.handleCountryEventClick, False, 0, True)
        self.widget.mainMc.countryEventBtn.selected = True
        self.widget.mainMc.seasonEventBtn.selected = False
        self.widget.mainMc.scrollWndList.itemRenderer = 'WingWorldOverVie_EventListItemRender'
        self.widget.mainMc.scrollWndList.labelFunction = self.itemLableFunction
        self.widget.mainMc.scrollWndList.itemHeightFunction = self.itemHeightFunction
        self.textItemRender = self.widget.getInstByClsName('WingWorldOverVie_EventListItemRender')
        self.widget.addChild(self.textItemRender)
        self.textItemRender.visible = False
        for i in xrange(3):
            getattr(self.widget.mainMc, 'resourcesIcon%d' % i).visible = False
            getattr(self.widget.mainMc, 'resourcesTxt%d' % i).visible = False

        self.widget.mainMc.junZiRankBtn.visible = False
        self.widget.mainMc.kingEventBtn.visible = gameglobal.rds.configData.get('enableWingWorldHistoryBook', False)
        self.widget.mainMc.kingEventBtn.addEventListener(events.BUTTON_CLICK, self.handleKingEventBtnClick, False, 0, True)
        self.widget.mainMc.kingEventFlag.visible = False
        self.widget.mainMc.txtSeason.text = WWCFGD.data.get('wingWorldSeasonTime', 'wingWorldSeasonTime')
        self.widget.mainMc.scoreBtn.addEventListener(events.BUTTON_CLICK, self.handleScoreBtnClick, False, 0, True)
        self.widget.mainMc.gotoww.textfield.htmlText = gameStrings.WING_WORLD_OVERVIEW_GOTOWW
        self.widget.mainMc.gotoww.addEventListener(events.MOUSE_ROLL_OVER, self.handleGotoWWRollOver, False, 0, True)
        self.widget.mainMc.gotoww.addEventListener(events.MOUSE_ROLL_OUT, self.handleGotoWWRollOut, False, 0, True)
        self.widget.mainMc.gotoww.flyBtn.addEventListener(events.MOUSE_CLICK, self.handleFlyBtnClick, False, 0, True)
        TipManager.addTip(self.widget.mainMc.gotoww.flyBtn, gameStrings.WING_WORLD_OVERVIEW_FLYTIP)
        self.isInEdit = False

    def isInNewWnd(self):
        return self.widget.mainMc.currentLabel == 'new'

    def handleKingEventBtnClick(self, *args):
        self.uiAdapter.wingWorldHistoryBook.show()

    def itemLableFunction(self, *args):
        index = int(args[3][0].GetNumber())
        if index >= len(self.eventList):
            return
        itemData = self.eventList[index]
        itemMc = ASObject(args[3][1])
        eventId, time, param = itemData
        itemMc.txtTime.text = utils.formatDate(time, '.')
        itemMc.txtContent.htmlText = self.getTextByParam(eventId, param)

    def getTextByParam(self, eventId, param):
        try:
            if self.selectedEventType == COUNTRY_EVENT_SELECTED:
                eventDesc = WWCED.data.get(eventId, {}).get('msg', '%s' * len(param))
            else:
                eventDesc = WWSED.data.get(eventId, {}).get('msg', '%s' * len(param))
            strList = []
            for arg, argType in param:
                if argType == gametypes.WING_EVENT_PARAM_TYPE_KEEP:
                    strList.append(arg)
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_COUNTRY:
                    strList.append(RSCD.data.get(arg, {}).get('serverName', gameStrings.WING_WORLD_CITY_NO_OWNER))
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_CITY:
                    strList.append(WWCTD.data.get(arg, {}).get('name', ''))
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_CITY_LIST:
                    cityNames = wingWorldUtils.getWingCitysName(arg)
                    strList.append(cityNames)
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_GROUP:
                    strList.append(WWD.data.get(arg, {}).get('name', ''))
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_TITLE:
                    strList.append(WWCTTD.data.get(arg, {}).get('titleName', ''))
                elif argType == gametypes.WING_EVENT_PARAM_TYPE_LIST:
                    strList.extend(arg)

            return eventDesc % tuple(strList)
        except Exception as e:
            gamelog.error('jbx:getTextByParam', eventId, param, self.selectedEventType)
            return ''

    def itemHeightFunction(self, *args):
        index = int(args[3][0].GetNumber())
        if index < len(self.eventList):
            itemData = self.eventList[index]
            eventId = int(itemData[0])
            param = itemData[2]
            self.textItemRender.txtContent.htmlText = self.getTextByParam(eventId, param)
            return GfxValue(self.textItemRender.txtContent.numLines * 23)
        else:
            return GfxValue(23)

    def refreshInfo(self):
        if not self.widget or not self.widget.mainMc:
            return
        gamelog.info('jbx:refreshInfo')
        mainMc = self.widget.mainMc
        if BigWorld.player().isWingWorldCampMode():
            mainMc.gotoAndStop('new')
            self.refreshNewWndInfo()
        else:
            mainMc.gotoAndStop('old')
            self.refreshOldWndInfo()

    def refreshNewWndInfo(self):
        p = BigWorld.player()
        mainMc = self.widget.mainMc
        mainMc.flagBg.gotoAndStop('camp%d' % p.wingWorldCamp)
        mainMc.countryEventBtn.selected = True
        mainMc.seasonEventBtn.selected = False
        mainMc.seasonEventBtn.visible = False
        self.selectedEventType = COUNTRY_EVENT_SELECTED
        mainMc.countryEventBtn.label = gameStrings.WING_WORLD_CAMP_EVENT
        mainMc.junZiRankBtn.visible = False
        mainMc.txtCountryLvDesc.text = ''
        mainMc.lvBg.visible = False
        mainMc.txtCountryLv.text = ''
        mainMc.txtAllScore.text = ''
        mainMc.changeIconBtn.visible = False
        mainMc.txtCountryName.text = utils.getWingCampName(p.wingWorldCamp)
        self.updateCampIcon()
        self.refreshCampNotice()
        self.refreshTop5()
        self.updateCountryEventFlag()
        self.refreshEvents()

    def refreshTop5(self):
        p = BigWorld.player()
        armyMc = self.widget.mainMc.armyMc
        armyData = WWCAD.data
        for i, postId in enumerate(gametypes.WING_WORLD_CAMP_SUPER_MGR_POST_IDS):
            guildLeaderInfo = p.wingWorld.getArmyByPostId(postId)
            posMc = getattr(armyMc, 'pos%d' % i)
            posMc.txtLeaderName.text = guildLeaderInfo.name if guildLeaderInfo and p.isWingWorldCampArmy() else gameStrings.WING_WORLD_NO_LEADER
            posMc.txtGuildName.text = guildLeaderInfo.guildName if guildLeaderInfo and p.isWingWorldCampArmy() else ''
            posMc.armyName.text = armyData.get(postId, {}).get('categoryName1', '') if p.wingWorldCamp == 1 else armyData.get(postId, {}).get('categoryName2', '')
            if i == 0:
                posMc.title.gotoAndStop('c%d1' % p.wingWorldCamp)
                posMc.icon.gotoAndStop('arm%d1' % p.wingWorldCamp)
            else:
                posMc.title.gotoAndStop('c%d2' % p.wingWorldCamp)
                posMc.icon.gotoAndStop('arm%d2' % p.wingWorldCamp)

    def updateCampIcon(self):
        if not self.widget:
            return
        mainMc = self.widget.mainMc
        p = BigWorld.player()
        camp = getattr(p, 'wingWorldCamp', 0)
        campIconName = WWCD.data.get('wingCampIcons', gameStrings.WING_WORLD_CAMP_ICONS).get(camp, '')
        if campIconName:
            mainMc.countryIcon.visible = True
            mainMc.countryIcon.fitSize = True
            mainMc.countryIcon.loadImage(IMPAGE_PATH % campIconName)
        else:
            mainMc.countryIcon.visible = False

    def queryCampNotice(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            p.base.queryWWCNotification()

    def refreshCampNotice(self):
        if not self.widget:
            return
        p = BigWorld.player()
        armyMc = self.widget.mainMc.armyMc
        armyMc.editBtn.visible = False
        armyMc.saveBtn.visible = self.isInEdit
        armyMc.noticeArea.visible = self.isInEdit
        armyMc.noticeText.text = p.wingWorld.country.getOwnCamp().notice if p.wingWorld.country.getOwnCamp().notice else gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO_NO_INFO
        armyMc.editBtn.addEventListener(events.BUTTON_CLICK, self.onEditBtnClick)
        TipManager.addTip(armyMc.editBtn, gameStrings.CHANGE)
        armyMc.saveBtn.addEventListener(events.BUTTON_CLICK, self.onSaveBtnClick)
        TipManager.addTip(armyMc.saveBtn, gameStrings.SAVE)

    def onEditBtnClick(self, *args):
        self.isInEdit = True
        p = BigWorld.player()
        armyMc = self.widget.mainMc.armyMc
        armyMc.noticeArea.noticeInput.text = p.wingWorld.country.getOwnCamp().notice
        self.refreshCampNotice()

    def onSaveBtnClick(self, *args):
        p = BigWorld.player()
        msg = self.widget.mainMc.armyMc.noticeArea.noticeInput.text
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_CAMP_NOTICE_TABOO)
            return
        self.isInEdit = False
        p.base.setWWCNotification(msg)
        self.refreshCampNotice()

    def refreshOldWndInfo(self):
        p = BigWorld.player()
        selfCountry = p.wingWorld.country.getOwn()
        gamelog.info('jbx:refreshInfo')
        mainMc = self.widget.mainMc
        mainMc.flagBg.gotoAndStop('old')
        mainMc.changeIconBtn.visible = True
        armyMc = self.widget.mainMc.armyMc
        for postId in wingWorldUtils.wingPostIdData.ARMY_SUPER_MGR_POST_IDS:
            leaderArmyInfo = p.wingWorld.getArmyByPostId(postId)
            txtLeaderName = getattr(armyMc, 'txtLeaderName%d' % postId)
            txtLeaderName.text = leaderArmyInfo.name if leaderArmyInfo else gameStrings.WING_WORLD_NO_LEADER

        powerLevel = selfCountry.getPowerLevel()
        mainMc.txtCountryLv.text = powerLevel
        mainMc.txtCountryLvDesc.text = WWCPLD.data.get(powerLevel, {}).get('title', powerLevel)
        self.widget.mainMc.txtAllScore.text = gameStrings.WING_WORLD_COUNTRY_TOTAL_SCORE % selfCountry.power if selfCountry.power else ''
        self.widget.mainMc.junZiRankBtn.visible = bool(selfCountry.power)
        self.updateCountryIcon()
        self.refreshArmyMark()
        self.updateCountryEventFlag()
        self.refreshEvents()

    def refreshEvents(self):
        if not self.widget:
            return
        eventList = []
        p = BigWorld.player()
        if self.selectedEventType == COUNTRY_EVENT_SELECTED:
            if p.isWingWorldCampMode():
                eventList = p.wingWorld.country.getOwnCamp().events
            else:
                eventList = p.wingWorld.country.getOwn().events
        else:
            eventList = p.wingWorld.events
        self.eventList = eventList[::-1]
        self.widget.mainMc.scrollWndList.dataArray = range(len(self.eventList))
        self.widget.mainMc.scrollWndList.validateNow()

    def updateCountryIcon(self):
        if not self.widget:
            return
        p = BigWorld.player()
        selfCountry = p.wingWorld.country.getOwn()
        if selfCountry.flagId:
            wwcfd = WWCFD.data.get(selfCountry.flagId, {})
            iconId = wwcfd.get('icon', 0)
            self.widget.mainMc.countryIcon.fitSize = True
            self.widget.mainMc.countryIcon.loadImage(IMPAGE_PATH % str(iconId))
        else:
            self.widget.mainMc.countryIcon.clear()

    def refreshArmyMark(self):
        if not self.widget or self.isInNewWnd():
            return
        p = BigWorld.player()
        wingWorldArmyMark = getattr(p, 'wingWorldArmyMark', {})
        isAllArmy = True
        wingWorldArmyMarkScore = getattr(p, 'wingWorldArmyMarkScore', ({}, 0))
        for postId in wingWorldUtils.wingPostIdData.ARMY_SUPER_MGR_POST_IDS:
            if not p.wingWorld.getArmyByPostId(postId):
                isAllArmy = False
                break

        if not isAllArmy:
            voteState = WING_WORLD_MARKED
            wingWorldArmyMarkScore = ({}, 0)
        elif p.lv < WWCD.data.get('armyMarkMinLv', 69):
            voteState = WING_WORLD_MARKED
            wingWorldArmyMarkScore = ({}, 0)
        elif not wingWorldArmyMark:
            voteState = WING_WORLD_NOT_MARK
        else:
            voteState = WING_WORLD_MARKED
        if voteState == WING_WORLD_NOT_MARK:
            self.widget.mainMc.scoreBtn.visible = True
            for i in xrange(MARK_MAX_CNT):
                scoreMc = getattr(self.widget.mainMc.armyMc, 'score%d' % (i + 1))
                scoreMc.gotoAndStop('star')
                score = 0
                for j in xrange(MARK_SCORE_MAX):
                    starMc = getattr(scoreMc.starList, 'star%d' % j)
                    starMc.visible = j < int(score)

        else:
            self.widget.mainMc.scoreBtn.visible = True
            for i in xrange(MARK_MAX_CNT):
                scoreMc = getattr(self.widget.mainMc.armyMc, 'score%d' % (i + 1))
                scoreMc.gotoAndStop('star')
                score, cnt = wingWorldArmyMarkScore[0].get(i + 1, (0, 0))
                for j in xrange(MARK_SCORE_MAX):
                    starMc = getattr(scoreMc.starList, 'star%d' % j)
                    starMc.visible = j < int(score)

    def updateCountryEventFlag(self, saveMark = False):
        if not self.widget:
            return
        currentMarkStr = self.getCurrentMarkStr()
        gamelog.info('jbx:setWingWorldTrends', currentMarkStr)
        if saveMark:
            self.widget.mainMc.countryEventFlag.visible = False
        else:
            saveMarkStr = AppSettings.get(keys.SET_WING_WORLD_TRENDS, '')
            self.widget.mainMc.countryEventFlag.visible = currentMarkStr != saveMarkStr
        AppSettings[keys.SET_WING_WORLD_TRENDS] = currentMarkStr
        AppSettings.save()

    def getCurrentMarkStr(self):
        markStr = ''
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            for campId in gametypes.WING_WORLD_CAMPS:
                canVal = BigWorld.player().wingWorld.country.getCamp(campId)
                if campId and canVal.trendIds:
                    campStr = ''
                    for trendId in canVal.trendIds:
                        if campStr:
                            campStr += '_'
                        campStr += str(trendId)

                    if markStr:
                        markStr += ','
                    markStr += '%d:' % campId + campStr

        else:
            for hostId, countryVal in BigWorld.player().wingWorld.country.iteritems():
                if not p.wingWorld.country.isNormalHostId(hostId):
                    continue
                if countryVal.trendIds:
                    countryStr = ''
                    for trendId in countryVal.trendIds:
                        if countryStr:
                            countryStr += '_'
                        countryStr += str(trendId)

                    if markStr:
                        markStr += ','
                    markStr += '%d:' % hostId + countryStr

        return markStr

    def onMarkArmy(self, realScores, realArmyIds):
        gamelog.info('jbx:onMarkArmy', realScores, realArmyIds)
        p = BigWorld.player()
        for score in realScores:
            if not score:
                p.showGameMsg(GMDD.data.WING_WORLD_ARMY_MARK_ALL, ())
                return

        msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ARMY_MARK_CONFIRM, '')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.sendArmymark, realScores))

    def sendArmymark(self, realScores):
        gamelog.info('jbx:markWingWorldArmy', realScores)
        BigWorld.player().cell.markWingWorldArmy(realScores)
        self.uiAdapter.worldWar.hideArmyMark()

    def handleScoreBtnClick(self, *args):
        gamelog.info('jbx:handleScoreBtnClick')
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_SOUL_FORBIDDEN, ())
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_MARK)

    def handleChangeIconBtnClick(self, *args):
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_SOUL_FORBIDDEN, ())
            return
        gameglobal.rds.ui.wingWorldWarFlag.show()

    def handleZhanXunRankBtnClick(self, *args):
        gamelog.info('jbx:handleZhanXunRankBtnClick')
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WORLD_ZHAN_XUN_WEEKLY)

    def handleVoteBtnClick(self, *args):
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_SOUL_FORBIDDEN, ())
            return
        gamelog.info('jbx:handleVoteBtnClick')
        self.uiAdapter.wingWorldVote.show()

    def handleCountryEventBtnClick(self, *args):
        if self.selectedEventType == COUNTRY_EVENT_SELECTED:
            return
        self.widget.mainMc.countryEventBtn.selected = True
        self.widget.mainMc.seasonEventBtn.selected = False
        self.selectedEventType = COUNTRY_EVENT_SELECTED
        self.refreshEvents()

    def handleSeasonEventBtnClick(self, *args):
        if self.selectedEventType == SEASON_EVENT_SELECTED:
            return
        self.widget.mainMc.countryEventBtn.selected = False
        self.widget.mainMc.seasonEventBtn.selected = True
        self.selectedEventType = SEASON_EVENT_SELECTED
        self.refreshEvents()

    def handleCountryEventClick(self, *args):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            self.uiAdapter.wingWorldCampTrend.show()
        else:
            self.uiAdapter.wingWorldTrend.show()

    def addPushMsg(self):
        p = BigWorld.player()
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_MARK) and not getattr(p, 'wingWorldArmyMark', {}):
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_MARK, {'click': self.openWingWorldArmy})
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_MARK)

    def openWingWorldArmy(self):
        self.uiAdapter.wingWorld.show()
        self.uiAdapter.loadWidget(uiConst.WIDGET_WW_ARMY_MARK)

    def handleGotoWWLink(self, *args):
        gamelog.debug('ypc@ handleGotoWWLink!!!')
        p = BigWorld.player()
        if p.inWingCityOrBornIsland() or p.inWingWarCity():
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_OVERVIEW_ALREADY_IN_WINGWORLD)
            return
        lastUse = p.wingWorldEnterSkillLastUseTime
        skillCD = wingWorldUtils.getEnterBornIslandSkillCD()
        if utils.getNow() - lastUse > skillCD:
            BigWorld.player().enterToWingBornIslandBySkill(False)
        else:
            uiUtils.findPosById(WWCD.data.get('lvyiweiTrackID', 0))

    def handleGotoWWRollOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.gotoAndStop('over')
        e.currentTarget.textfield.htmlText = gameStrings.WING_WORLD_OVERVIEW_GOTOWW

    def handleGotoWWRollOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.gotoAndStop('normal')
        e.currentTarget.textfield.htmlText = gameStrings.WING_WORLD_OVERVIEW_GOTOWW

    def handleFlyBtnClick(self, *args):
        gamelog.debug('ypc@ handleFlyBtnClick!')
        p = BigWorld.player()
        if p.inWingCityOrBornIsland() or p.inWingWarCity():
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_OVERVIEW_ALREADY_IN_WINGWORLD)
            return
        trackId = WWCD.data.get('lvyiweiTrackID', 0)
        trackId = uiUtils.findTrackId(trackId)
        uiUtils.gotoTrack(trackId)
