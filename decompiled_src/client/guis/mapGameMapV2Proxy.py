#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameMapV2Proxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import gamelog
import sMath
import utils
import const
import mapGameCommon
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import summon_sprite_info_data as SSID
from data import state_data as SD
from data import fame_data as FD
from cdata import game_msg_def_data as GMDD
GRID_START_X = 0
GRID_START_Y = 0
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
STATE_TYPE_LIST = ['normal',
 'normal',
 'normal',
 'fight',
 'finish',
 'finish',
 'normal']
MAX_SPECIAL_GRID_TYPE = 12
GAME_CAMP_CHIDI = 1
GAME_CAMP_HEIDI = 2
ALTAR_ICON_NUM = 5
BOSS_STAGE_FAKE = 0
BOSS_STAGE_BOSS1 = 1
BOSS_STAGE_BOSS2 = 2
BOSS_STAGE_GRAVE = 3
BOSS_STAGE_GRAVE_END = 4

class MapGameMapV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameMapV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.bossState = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_MAP_V2, self.hide)

    def reset(self):
        self.gridsData = None
        self.mouseDragX = 0
        self.mouseDragY = 0
        self.inDrag = False
        self.isDraged = False
        self.lastStageInfo = []
        self.lastCenterInfo = []
        self.buffGridIdDict = {}
        self.timer = None
        self.gameCamp = 0
        self.enterCntRank = []
        self.callAttackRank = []
        self.gridIdList = []
        self.isLoading = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_MAP_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        if self.widget:
            self.widget.removeAllInst(self.widget.mapCanvas.bottomMc)
        self.widget = None
        self.delTimer()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_MAP_V2)
        gameglobal.rds.ui.setTempWeight(uiConst.WIDGET_CHAT_LOG, -1)

    def show(self):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_MAP_V2)
        p = BigWorld.player()
        p.base.requireMapGameBasicInfo()
        p.base.requireMapGameBuff()
        if not p.mapGameFirstOpen:
            gameglobal.rds.ui.mapGameGuide.show()
            p.cell.openMapGamePanel()
        isGraveStart = self.isGraveStart()
        if isGraveStart:
            self.bossState = BOSS_STAGE_GRAVE
            if p.mapGameGraveEndState:
                self.bossState = BOSS_STAGE_GRAVE_END

    def isGraveStart(self):
        graveStartStr = MGCD.data.get('mapGameGraveStartTime', '')
        graveStartTime = utils.getTimeSecondFromStr(graveStartStr)
        if graveStartTime <= utils.getNow():
            return True
        return False

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.topMc.closeBtn
        self.initMapPos()
        self.onResize()
        gameglobal.rds.ui.setTempWeight(uiConst.WIDGET_CHAT_LOG, uiConst.TOP_WIDGET_WEIGHT)
        gameglobal.rds.ui.setWidgetLevel(uiConst.WIDGET_CHAT_LOG, -1)
        self.widget.stage.addEventListener(events.EVENT_RESIZE, self.onResize)
        self.widget.scoreMc.power.addBtn.addEventListener(events.BUTTON_CLICK, self.handleClickAddBtn, False, 0, True)
        self.widget.scoreMc.power.desc.text = gameStrings.MAP_GAME_POWER_DESC
        tips = MGCD.data.get('MAP_GAME_POWER_TIPS', gameStrings.MAP_GAME_POWER_TIPS)
        TipManager.addTip(self.widget.scoreMc.power.desc, tips)
        self.widget.scoreMc.title.text = MGCD.data.get('MAP_GAME_SCORE_TITLE', gameStrings.MAP_GAME_SCORE_TITLE)
        self.widget.scoreMc.power.desc.text = MGCD.data.get('MAP_GAME_POWER_DESC', gameStrings.MAP_GAME_POWER_DESC)
        self.widget.scoreMc.score.desc.text = MGCD.data.get('MAP_GAME_SCORE_DESC', gameStrings.MAP_GAME_SCORE_DESC)
        self.widget.scoreMc.shopBtn.addEventListener(events.MOUSE_CLICK, self.handleClickShopBtn, False, 0, True)
        self.widget.scoreMc.guideBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGuideBtn, False, 0, True)
        self.widget.scoreMc.eventBtn.addEventListener(events.MOUSE_CLICK, self.handleClickEventBtn, False, 0, True)
        self.widget.detailMc.buffTitle.tf.text = gameStrings.MAP_GAME_DETAIL_BUFF_TITLE
        self.widget.detailMc.spriteTitle.tf.text = gameStrings.MAP_GAME_DETAIL_SPTITE_TITLE
        self.widget.detailMc.buffList.itemRenderer = 'MapGameMapV2_buffListItem'
        self.widget.detailMc.buffList.dataArray = []
        self.widget.detailMc.buffList.lableFunction = self.itemFunction
        self.addEvent(events.EVENT_FAME_UPDATE, self.handleFameUpdate)
        mapCanvas = self.widget.mapCanvas
        altarNum = MGCD.data.get('ALTAR_ICON_NUM', ALTAR_ICON_NUM)
        for i in xrange(altarNum):
            altarMc = mapCanvas.getChildByName('altar%d' % i)
            if altarMc:
                ASUtils.setMcEffect(altarMc, 'gray')

        if MGCD.data.get('isSecondBossMode', False):
            mapCanvas.trueBoss.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        else:
            mapCanvas.bigBoss.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        ASUtils.setHitTestDisable(mapCanvas.overMap, True)
        mapCanvas.addEventListener(events.MOUSE_DOWN, self.handleDragDown, False, 0, True)

    def setGameCamp(self):
        self.gameCamp = BigWorld.player().mapGameCamp
        if not self.widget:
            return
        gameglobal.rds.ui.mapGameCamp.show(self.gameCamp)

    def onChangeGraveState(self):
        graveEnd = BigWorld.player().mapGameGraveEndState
        if graveEnd:
            self.setBossState(False)

    def setBossState(self, state):
        if state:
            self.bossState = BOSS_STAGE_GRAVE
        else:
            self.bossState = BOSS_STAGE_GRAVE_END
            if self.widget:
                gameglobal.rds.ui.mapGameImage.show()

    def setRankData(self, enterCntRank, callAttackRank):
        self.enterCntRank = [ x for x, _ in enterCntRank ]
        self.callAttackRank = [ x for x, _ in callAttackRank ]

    def initMapPos(self):
        if not self.widget:
            return
        self.gameCamp = BigWorld.player().mapGameCamp
        deltaX = 0
        deltaY = 0
        startPos = ()
        campStartPos = MGCD.data.get('campStartPos', [])
        if self.gameCamp == 0 or not campStartPos:
            pass
        elif self.gameCamp == GAME_CAMP_CHIDI:
            startPosInfo = MGGPD.data.get(campStartPos[0], {})
            if startPosInfo:
                startPos = self.getGridPos(startPosInfo.get('pos', ()))
        elif self.gameCamp == GAME_CAMP_HEIDI:
            startPosInfo = MGGPD.data.get(campStartPos[1], {})
            if startPosInfo:
                startPos = self.getGridPos(startPosInfo.get('pos', ()))
        mapCanvas = self.widget.mapCanvas
        mapWidth = mapCanvas.width
        mapHeight = mapCanvas.height
        stageWidth = self.widget.stage.stageWidth
        stageHeight = self.widget.stage.stageHeight
        if startPos:
            deltaX = startPos[0] - mapWidth / 2
            if deltaX > 0:
                deltaX = min(deltaX, (mapWidth - stageWidth) / 2)
            elif deltaX < 0:
                deltaX = max(deltaX, -(mapWidth - stageWidth) / 2)
            deltaY = startPos[1] - mapHeight / 2
            if deltaY > 0:
                deltaY = min(deltaY, (mapHeight - stageHeight) / 2)
            elif deltaX < 0:
                deltaY = max(deltaY, -(mapHeight - stageHeight) / 2)
        mapCanvas.x = self.widget.stage.stageWidth / 2 - mapWidth / 2 - deltaX
        mapCanvas.y = self.widget.stage.stageHeight / 2 - mapHeight / 2 - deltaY

    def refreshInfo(self):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if not self.widget:
            return
        p = BigWorld.player()
        if not hasattr(p, 'grids'):
            return
        self.gridsData = p.grids
        self.refreshScore()
        self.loadAllGrid()
        self.refreshDetailMc()
        self.delTimer()
        self.timerFunc()
        self.addTimer()
        if not p.mapGameGraveEndFlashState and self.bossState == BOSS_STAGE_GRAVE_END:
            gameglobal.rds.ui.mapGameImage.show()
        gameglobal.rds.ui.mapGameGuide.refreshInfo()

    def loadAllGrid(self):
        if not self.widget:
            return
        self.gridIdList = MGGPD.data.keys()
        if not self.isLoading:
            self.loadParticialGrids(0, 50)
        self.refreshFakeBoss()

    def loadParticialGrids(self, gridIndex, gridNum):
        if not self.widget:
            return
        elif not self.gridIdList:
            return
        else:
            self.isLoading = True
            p = BigWorld.player()
            for i in xrange(gridNum):
                if gridIndex + i >= len(self.gridIdList):
                    return
                id = self.gridIdList[gridIndex + i]
                info = MGGPD.data.get(id, {})
                itemMc = self.widget.getInstByClsName('MapGameMapV2_gridBtn')
                itemMc.id = id
                itemMc.name = 'grid%d' % id
                pos = info.get('pos', ())
                if not pos:
                    return
                x, y = self.getGridPos(pos)
                itemMc.x = x
                itemMc.y = y
                itemMc.gmBox.visible = False
                ASUtils.setHitTestDisable(itemMc.gmBox, True)
                self.widget.mapCanvas.bottomMc.addChild(itemMc)
                itemMc.shine.visible = False
                contentId = info.get('contentId', 0)
                gridInfo = MGGD.data.get(contentId, {})
                gridVal = self.gridsData.get(id)
                if not gridVal:
                    continue
                type = gridInfo.get('type', 0)
                itemMc.gridType = type
                itemMc.reward = 0
                if type == gametypes.MAP_GAME_GRID_TYPE_BUFF:
                    if MGCD.data.get('isSecondBossMode', False) and self.bossState == BOSS_STAGE_FAKE:
                        addbuff = gridInfo.get('fakeBuff', {})
                    else:
                        addbuff = gridInfo.get('addBuff', {})
                    for buffs in addbuff.values():
                        for buff in buffs:
                            self.buffGridIdDict[buff] = id

                iconType = gridInfo.get('iconType', 'empty')
                state = gridVal.state
                itemMc.gotoAndStop(STATE_TYPE_LIST[state])
                gridMc = itemMc.getChildByName(STATE_TYPE_LIST[state])
                if type == gametypes.MAP_GAME_GRID_TYPE_START_POINT:
                    gridMc.icon.gotoAndStop(iconType)
                    continue
                elif type in (gametypes.MAP_GAME_GRID_TYPE_BOSS, gametypes.MAP_GAME_GRID_TYPE_ELITE):
                    bossMc = self.widget.mapCanvas.getChildByName(iconType)
                    if iconType == 'trueBoss':
                        fakeBossId = MGCD.data.get('mapGameBossGridIdList', {}).get('fakeBoss')
                        fakeBossState = self.gridsData.get(fakeBossId).state
                        bossMc.visible = fakeBossState > gametypes.MAP_GAME_GRID_STATE_DISABLE
                        if fakeBossState > gametypes.MAP_GAME_GRID_STATE_DISABLE and self.bossState < BOSS_STAGE_BOSS1:
                            self.bossState = BOSS_STAGE_BOSS1
                        secondId = gridVal.secondId
                        if state >= gametypes.MAP_GAME_GRID_STATE_ENABLE and secondId and self.bossState < BOSS_STAGE_BOSS2:
                            self.bossState = BOSS_STAGE_BOSS2
                    else:
                        bossState = STATE_TYPE_LIST[state]
                        bossMc.gotoAndStop(bossState)
                        if bossState == 'fight':
                            ASUtils.setHitTestDisable(bossMc.fightLabel, True)
                        elif bossState == 'finish':
                            ASUtils.setHitTestDisable(bossMc.finishLabel, True)
                    continue
                elif type == gametypes.MAP_GAME_GRID_TYPE_ALTAR:
                    gridMc.visible = False
                    iconName = info.get('iconName', 'fire0')
                    iconMc = self.widget.mapCanvas.getChildByName(iconName)
                    if iconName == 'fakeBoss':
                        iconMc.visible = state == gametypes.MAP_GAME_GRID_STATE_DISABLE
                    elif state == gametypes.MAP_GAME_GRID_STATE_FINISH:
                        ASUtils.setMcEffect(iconMc, '')
                    else:
                        ASUtils.setMcEffect(iconMc, 'gray')
                    iconMc.id = id
                    iconMc.gridType = type
                    iconMc.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
                    continue
                elif type == gametypes.MAP_GAME_GRID_TYPE_ROAD:
                    gridMc.visible = False
                    iconType = info.get('iconName', '')
                    roadMc = self.widget.mapCanvas.getChildByName(iconType)
                    roadMc.visible = state in [gametypes.MAP_GAME_GRID_STATE_ENABLE, gametypes.MAP_GAME_GRID_STATE_FINISH]
                    continue
                if state == gametypes.MAP_GAME_GRID_STATE_DISABLE and info.get('isHide', 0):
                    gridMc.icon.gotoAndStop('text')
                    gridMc.icon.tf.x = 21
                    gridMc.icon.tf.text = '?'
                    itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
                    continue
                if 'buff' in iconType:
                    gridMc.icon.gotoAndStop('empty')
                    if gridMc.tiredProgressBar:
                        gridMc.tiredProgressBar.visible = False
                    spritIcon = None
                    if type == gametypes.MAP_GAME_GRID_TYPE_ALTAR:
                        if state == gametypes.MAP_GAME_GRID_STATE_FINISH:
                            spritIcon = self.widget.getInstByClsName('MapGameMapV2_%s' % iconType)
                        else:
                            spritIcon = self.widget.getInstByClsName('MapGameMapV2_lock%s' % iconType)
                    elif state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_ENABLE, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
                        spritIcon = self.widget.getInstByClsName('MapGameMapV2_%s' % iconType)
                    elif state == gametypes.MAP_GAME_GRID_STATE_DISABLE:
                        spritIcon = self.widget.getInstByClsName('MapGameMapV2_lock%s' % iconType)
                    if spritIcon:
                        spritIcon.x = x - 11
                        spritIcon.y = y - 51
                        spritIcon.name = iconType
                        self.widget.mapCanvas.bottomMc.addChild(spritIcon)
                        ASUtils.setHitTestDisable(spritIcon, True)
                    itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
                    continue
                if state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
                    if type == gametypes.MAP_GAME_GRID_TYPE_HOLY_POWER:
                        gridMc.icon.gotoAndStop(iconType)
                    else:
                        distanceNumber = mapGameCommon.calMineNum(id)
                        if distanceNumber:
                            gridMc.icon.gotoAndStop('text')
                            gridMc.icon.tf.x = 18
                            gridMc.icon.tf.text = distanceNumber
                        else:
                            gridMc.icon.gotoAndStop('empty')
                elif state == gametypes.MAP_GAME_GRID_STATE_REWARD:
                    mapGameRewardRecord = p.mapGameRewardRecord
                    if mapGameRewardRecord and id in mapGameRewardRecord.keys():
                        distanceNumber = mapGameCommon.calMineNum(id)
                        if distanceNumber:
                            gridMc.icon.gotoAndStop('text')
                            gridMc.icon.tf.x = 18
                            gridMc.icon.tf.text = distanceNumber
                        else:
                            gridMc.icon.gotoAndStop('empty')
                    else:
                        gridMc.icon.gotoAndStop('box')
                        itemMc.shine.visible = True
                        itemMc.reward = 1
                else:
                    if gridInfo.get('totalBonus', 0) and iconType == 'sprite':
                        gridMc.icon.gotoAndStop('reward')
                    else:
                        gridMc.icon.gotoAndStop(iconType)
                    if id in self.callAttackRank:
                        gridMc.icon.gotoAndStop('conduct')
                    if id in self.enterCntRank:
                        gridMc.icon.gotoAndStop('hot')
                    if state == gametypes.MAP_GAME_GRID_STATE_ENABLE:
                        gridMc.tiredProgressBar.visible = True
                        totalProgress = gridInfo.get('totalProgress', 0)
                        progress = gridVal.progress
                        gridMc.tiredProgressBar.currentValue = progress
                        gridMc.tiredProgressBar.maxValue = totalProgress
                itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)

            fun = Functor(self.loadParticialGrids, gridIndex + gridNum, gridNum)
            BigWorld.callback(0, fun)
            return

    def refreshGrid(self, gridId):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if not self.widget:
            return
        itemMc = self.widget.mapCanvas.bottomMc.getChildByName('grid%d' % gridId)
        if not itemMc:
            return
        gridVal = self.gridsData.get(gridId)
        if not gridVal:
            return
        state = gridVal.state
        itemMc.gotoAndStop(STATE_TYPE_LIST[state])
        gridMc = itemMc.getChildByName(STATE_TYPE_LIST[state])
        info = MGGPD.data.get(gridId)
        contentId = info.get('contentId', 0)
        gridInfo = MGGD.data.get(contentId, {})
        type = gridInfo.get('type', 0)
        if state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
            if type != gametypes.MAP_GAME_GRID_TYPE_HOLY_POWER:
                distanceNumber = mapGameCommon.calMineNum(gridId)
                if distanceNumber:
                    gridMc.icon.gotoAndStop('text')
                    gridMc.icon.tf.x = 18
                    gridMc.icon.tf.text = distanceNumber
                else:
                    gridMc.icon.gotoAndStop('empty')
        elif state == gametypes.MAP_GAME_GRID_STATE_REWARD:
            mapGameRewardRecord = BigWorld.player().mapGameRewardRecord
            if mapGameRewardRecord and gridId in mapGameRewardRecord.keys():
                distanceNumber = mapGameCommon.calMineNum(id)
                if distanceNumber:
                    gridMc.icon.gotoAndStop('text')
                    gridMc.icon.tf.x = 18
                    gridMc.icon.tf.text = distanceNumber
                else:
                    gridMc.icon.gotoAndStop('empty')
            else:
                gridMc.icon.gotoAndStop('box')
                itemMc.shine.visible = True
                itemMc.reward = 1
        if state == gametypes.MAP_GAME_GRID_STATE_ENABLE and type not in [gametypes.MAP_GAME_GRID_TYPE_BUFF, gametypes.MAP_GAME_GRID_TYPE_START_POINT]:
            totalProgress = gridInfo.get('totalProgress', 0)
            progress = gridVal.progress
            gridMc.tiredProgressBar.currentValue = progress
            gridMc.tiredProgressBar.maxValue = totalProgress

    def refreshFakeBoss(self):
        gridId = MGCD.data.get('mapGameBossGridIdList', {}).get('fakeBoss')
        fakeBossState = self.gridsData.get(gridId).state
        fakeBossMc = self.widget.mapCanvas.getChildByName('fakeBoss')
        trueBossMc = self.widget.mapCanvas.getChildByName('trueBoss')
        if fakeBossMc:
            fakeBossMc.visible = fakeBossState == gametypes.MAP_GAME_GRID_STATE_DISABLE
        if trueBossMc:
            trueBossMc.visible = fakeBossState > gametypes.MAP_GAME_GRID_STATE_DISABLE
        self.refreshDetailMc()
        self.refreshTitle()

    def refreshTitle(self):
        mapMc = self.widget.mapCanvas.map
        overMapMc = self.widget.mapCanvas.overMap
        titleMc = self.widget.topMc.title
        titleMc.text = self.getTitle()
        if MGCD.data.get('isSecondBossMode', False):
            if self.bossState == BOSS_STAGE_FAKE:
                mapMc.gotoAndStop('fake')
                overMapMc.gotoAndStop('fake')
            else:
                mapMc.gotoAndStop('really')
                overMapMc.gotoAndStop('really')

    def getTitle(self):
        titleList = MGCD.data.get('mapGameTitle')
        if self.bossState == BOSS_STAGE_FAKE:
            return titleList[0]
        else:
            return titleList[1]

    def getStage(self):
        p = BigWorld.player()
        isGraveStart = self.isGraveStart()
        if isGraveStart:
            self.bossState = BOSS_STAGE_GRAVE
            if p.mapGameGraveEndState:
                self.bossState = BOSS_STAGE_GRAVE_END
        endStr = MGCD.data.get('mapGameFinishTime', '')
        endTime = utils.getTimeSecondFromStr(endStr)
        if utils.getNow() >= endTime:
            self.bossState = BOSS_STAGE_GRAVE_END
        return self.bossState

    def isGraveState(self):
        bossState = self.getStage()
        return bossState == BOSS_STAGE_GRAVE

    def getGridPos(self, pos):
        y = 60 * pos[1]
        offset = 35 if pos[1] % 2 else 0
        x = offset + 70 * pos[0]
        return (x, y)

    def refreshDetailMc(self):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if not self.widget:
            return
        p = BigWorld.player()
        playerBuff = p.playerBuff.union(BigWorld.player().spriteBuff)
        buffArray = []
        if MGCD.data.get('isSecondBossMode', False) and self.bossState == BOSS_STAGE_FAKE:
            mapGameFakeBuffList = MGCD.data.get('mapGameFakeBuffList')
            for trueBuff, fakeBuff in mapGameFakeBuffList.iteritems():
                sdData = SD.data.get(fakeBuff, {})
                buffInfo = {}
                buffInfo['id'] = fakeBuff
                buffInfo['name'] = sdData.get('name', '')
                buffInfo['buffIcon'] = 'state/40/%d.dds' % sdData.get('iconId', 0)
                buffInfo['buffDesc'] = '%s<br>%s' % (sdData.get('name', ''), sdData.get('desc', ''))
                buffInfo['available'] = trueBuff in playerBuff
                buffArray.append(buffInfo)

        else:
            buffList = MGCD.data.get('mapGameAddBuffList')
            for buffId in buffList:
                sdData = SD.data.get(buffId, {})
                buffInfo = {}
                buffInfo['id'] = buffId
                buffInfo['name'] = sdData.get('name', '')
                buffInfo['buffIcon'] = 'state/40/%d.dds' % sdData.get('iconId', 0)
                buffInfo['buffDesc'] = '%s<br>%s' % (sdData.get('name', ''), sdData.get('desc', ''))
                buffInfo['available'] = buffId in playerBuff
                buffArray.append(buffInfo)

        self.widget.detailMc.buffList.dataArray = buffArray
        self.widget.detailMc.buffList.validateNow()
        specialSpriteInfo = MGCD.data.get('MAP_GAME_EVERYDAY_SPRITE')
        startStr = MGCD.data.get('mapGameStartTime', '')
        startTime = utils.getDisposableCronTabTimeStamp(utils.getCrontabFromStr(startStr))
        intervalDay = utils.getIntervalDay(startTime, utils.getNow())
        spriteToday = specialSpriteInfo.get(intervalDay, {})
        if spriteToday:
            spriteDesc = spriteToday[0]
            if spriteDesc:
                self.widget.detailMc.desc.text = spriteDesc
            else:
                self.widget.detailMc.desc.text = gameStrings.MAP_GAME_DETAIL_NO_SPEICIAL_SPRITE
            spriteList = spriteToday[1:]
            for i in xrange(len(spriteList)):
                itemMc = self.widget.detailMc.getChildByName('slot%d' % i)
                if itemMc:
                    iconId = SSID.data.get(spriteList[i], {}).get('spriteIcon', '000')
                    iconPath = SPRITE_ICON_PATH % str(iconId)
                    itemMc.dragable = False
                    itemMc.setItemSlotData({'iconPath': iconPath})

        else:
            self.widget.detailMc.desc.text = gameStrings.MAP_GAME_DETAIL_NO_SPEICIAL_SPRITE

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.id = itemData.id
        itemMc.buff.icon.fitSize = True
        itemMc.buff.icon.loadImage(itemData.buffIcon)
        itemMc.buffName.text = itemData.name
        itemMc.desc.htmlText = itemData.buffDesc
        if itemData.available:
            ASUtils.setMcEffect(itemMc, '')
            itemMc.flag.htmlText = gameStrings.MAP_GAME_DETAIL_BUFF_FLAG_TRUE
        else:
            ASUtils.setMcEffect(itemMc, 'gray')
            itemMc.flag.htmlText = gameStrings.MAP_GAME_DETAIL_BUFF_FLAG_FALSE
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickBuffItem, False, 0, True)

    def handleClickBuffItem(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        id = int(itemMc.id)
        gridId = self.buffGridIdDict[id]
        if gridId:
            gameglobal.rds.ui.mapGameBuff.show(gridId)

    def handleFameUpdate(self, e):
        if e.data in const.MAP_GAME_FAMES:
            self.refreshScore()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def refreshScore(self):
        if not self.widget:
            return
        p = BigWorld.player()
        power = p.fame.get(const.MAP_GAME_TILI_FAME_ID, 0)
        score = p.fame.get(const.MAP_GAME_SCORE_FAME_ID, 0)
        self.widget.scoreMc.power.value.text = power
        scoreText = '%.1fW' % (float(score) / 10000) if score > 10000 else score
        self.widget.scoreMc.score.value.text = scoreText

    def refreshRewardRecord(self):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if not self.widget:
            return
        mapGameRewardRecord = BigWorld.player().mapGameRewardRecord
        if not mapGameRewardRecord:
            return
        for gridId in mapGameRewardRecord.keys():
            self.refreshGrid(gridId)

    def onResize(self, *args):
        if not self.widget:
            return
        stageWidth = self.widget.stage.stageWidth
        stageHeight = self.widget.stage.stageHeight
        self.widget.mapMask.width = stageWidth
        self.widget.mapMask.height = stageHeight
        if self.lastStageInfo:
            self.refreshMapPos()
        scale = stageHeight / 1280 if stageHeight / 1280 > 1 else 1
        self.widget.topMc.x = stageWidth / 2 - self.widget.topMc.width / 2
        self.widget.scoreMc.x = stageWidth - self.widget.scoreMc.width - 30
        self.widget.detailMc.x = stageWidth - self.widget.detailMc.width - 10
        self.widget.detailMc.y = self.widget.scoreMc.y + self.widget.scoreMc.height + 10
        self.lastStageInfo = [stageWidth, stageHeight]

    def refreshMapPos(self):
        if not self.widget:
            return
        stageWidth = self.widget.stage.stageWidth
        stageHeight = self.widget.stage.stageHeight
        oldX = self.widget.mapCanvas.x
        currentX = oldX - self.lastStageInfo[0] / 2 + stageWidth / 2
        self.widget.mapCanvas.x = sMath.clamp(currentX, stageWidth - self.widget.mapCanvas.width, 0)
        oldY = self.widget.mapCanvas.y
        currentY = oldY - self.lastStageInfo[1] / 2 + stageHeight / 2
        self.widget.mapCanvas.y = sMath.clamp(currentY, stageHeight - self.widget.mapCanvas.height, 0)

    def handleDragDown(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        itemMc = self.widget.mapCanvas
        itemMc.startDrag()
        self.inDrag = True
        self.isDraged = False
        self.mouseDragX = e.stageX
        self.mouseDragY = e.stageY
        self.widget.stage.addEventListener(events.MOUSE_MOVE, self.handleDragMove)
        self.widget.stage.addEventListener(events.MOUSE_UP, self.handleDragUp)

    def handleDragMove(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        if self.inDrag:
            x = self.widget.mapCanvas.x
            y = self.widget.mapCanvas.y
            stageWidth = self.widget.stage.stageWidth
            stageHeight = self.widget.stage.stageHeight
            movementX = e.stageX - self.mouseDragX
            movementY = e.stageY - self.mouseDragY
            if movementX or movementY:
                self.isDraged = True
            if x >= 0 and movementX > 0 or x + self.widget.mapCanvas.width <= stageWidth and movementX < 0 or y >= 0 and movementY > 0 or y + self.widget.mapCanvas.height <= stageHeight and movementY < 0:
                self.widget.mapCanvas.stopDrag()
                if x >= 0 and movementX > 0:
                    self.widget.mapCanvas.x = 0
                elif x + self.widget.mapCanvas.width <= stageWidth and movementX < 0:
                    self.widget.mapCanvas.x = stageWidth - self.widget.mapCanvas.width
                if y >= 0 and movementY > 0:
                    self.widget.mapCanvas.y = 0
                elif y + self.widget.mapCanvas.height <= stageHeight and movementY < 0:
                    self.widget.mapCanvas.y = stageHeight - self.widget.mapCanvas.height
            else:
                self.widget.mapCanvas.startDrag()
                self.widget.mapCanvas.x = sMath.clamp(self.widget.mapCanvas.x, stageWidth - self.widget.mapCanvas.width, 0)
                self.widget.mapCanvas.y = sMath.clamp(self.widget.mapCanvas.y, stageHeight - self.widget.mapCanvas.height, 0)
            self.mouseDragX = e.stageX
            self.mouseDragY = e.stageY

    def handleDragUp(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        itemMc = self.widget.mapCanvas
        itemMc.stopDrag()
        self.inDrag = False
        self.widget.stage.removeEventListener(events.MOUSE_MOVE, self.handleDragMove)
        self.widget.stage.removeEventListener(events.MOUSE_UP, self.handleDragUp)

    def handleClickAddBtn(self, *args):
        mallId = MGCD.data.get('mapGamePowerId', 0)
        if mallId:
            gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, 1, 'mapgame.0')

    def handleClickShopBtn(self, *args):
        self.uiAdapter.compositeShop.closeShop()
        shopId = MGCD.data.get('mapGameRewardShopId', 10361)
        BigWorld.player().base.openPrivateShop(0, shopId)

    def handleClickGuideBtn(self, *args):
        gameglobal.rds.ui.mapGameGuide.show()

    def handleClickEventBtn(self, *args):
        gameglobal.rds.ui.mapGameEvent.show()

    def handleClickGrid(self, *args):
        if self.isDraged:
            return
        p = BigWorld.player()
        mapGameBossGridIdList = MGCD.data.get('mapGameBossGridIdList', {})
        itemMc = ASObject(args[3][0]).currentTarget
        if itemMc.name in ('bigBoss', 'trueBoss'):
            gridType = gametypes.MAP_GAME_GRID_TYPE_BOSS
            id = mapGameBossGridIdList.get(itemMc.name)
        elif itemMc.name.startswith('boss'):
            gridType = gametypes.MAP_GAME_GRID_TYPE_ELITE
            id = mapGameBossGridIdList.get(itemMc.name)
        else:
            id = itemMc.id
            gridType = itemMc.gridType
        gamelog.debug('yedawang### clickGrid', id, gridType)
        gridInfo = MGGPD.data.get(id, {})
        if not mapGameCommon.checkGridCampWithGridId(id, self.gameCamp, gameglobal.rds.ui.mapGameEvent.eventList):
            campName = MGCD.data.get('campNameDict', {})
            p.showGameMsg(GMDD.data.BELONG_TO_CAMP_LIMIT, campName.get(self.gameCamp))
            return
        if MGCD.data.get('isSecondBossMode', False) and self.bossState == BOSS_STAGE_GRAVE:
            p.showGameMsg(GMDD.data.GRAVE_STATE_LIMIT, ())
            return
        gridVal = self.gridsData.get(id)
        state = gridVal.state
        if itemMc.name == 'trueBoss' and gridVal.secondId:
            secondId = gridVal.secondId
            if state == gametypes.MAP_GAME_GRID_STATE_ENABLE and secondId:
                id = secondId
                gridInfo = MGGPD.data.get(id, {})
                gridVal = self.gridsData.get(id)
                state = gridVal.state
                if self.bossState < BOSS_STAGE_BOSS2:
                    self.bossState = BOSS_STAGE_BOSS2
        if state == gametypes.MAP_GAME_GRID_STATE_DISABLE and gridInfo.get('isHide', 0):
            p.showGameMsg(GMDD.data.MAP_GAME_QUESTION_GRID, ())
            return
        if itemMc.reward:
            p.cell.getMapGameFinishReward(id)
            return
        self.closeAllWidget()
        if gridType == gametypes.MAP_GAME_GRID_TYPE_BOSS:
            gameglobal.rds.ui.mapGameBoss.show(id)
        elif gridType in gametypes.FIGHT_MAP_LIST:
            gameglobal.rds.ui.mapGameFight.show(id)
        elif gridType in gametypes.DONATE_MAP_LIST:
            gameglobal.rds.ui.mapGameDonate.show(id)
        elif gridType in [gametypes.MAP_GAME_GRID_TYPE_BUFF, gametypes.MAP_GAME_GRID_TYPE_ALTAR]:
            contentId = gridInfo.get('contentId', 0)
            gridInfo = MGGD.data.get(contentId, {})
            msg = gridInfo.get('informationMsg', '')
            duration = gridInfo.get('questDuration', 0)
            npcId = gridInfo.get('npcId', 0)
            if npcId and state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_ENABLE, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
                gameglobal.rds.ui.autoQuest.show(msg, npcId, duration)
                BigWorld.callback(duration, Functor(gameglobal.rds.ui.mapGameBuff.show, id))
            else:
                gameglobal.rds.ui.mapGameBuff.show(id)
        elif gridType == gametypes.MAP_GAME_GRID_TYPE_DISPATCH:
            if id in p.mapGameGridDispatch.keys():
                dispatchTime = p.mapGameGridDispatch.get(id)
                gridCd = const.SECONDS_PER_HOUR * MGCD.data.get('dispatchGridCD', 4)
                tNow = utils.getNow()
                if tNow < dispatchTime + gridCd:
                    timeText = utils.formatTimeStr(dispatchTime + gridCd - tNow)
                    p.showGameMsg(GMDD.data.MAP_GAME_DISPATCH_GRID_IN_CD, timeText)
                    return
            gameglobal.rds.ui.mapGameDispatch.show(id)

    def closeAllWidget(self):
        gameglobal.rds.ui.mapGameBoss.hide()
        gameglobal.rds.ui.mapGameFight.hide()
        gameglobal.rds.ui.mapGameDonate.hide()
        gameglobal.rds.ui.mapGameBuff.hide()

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(0.1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        if MGCD.data.get('isSecondBossMode', False) and self.bossState <= BOSS_STAGE_GRAVE:
            endStr = MGCD.data.get('mapGameGraveStartTime')
        else:
            endStr = MGCD.data.get('mapGameFinishTime', '')
        endCrontab = utils.getCrontabFromStr(endStr)
        left = 0
        if utils.getDisposableCronTabTimeStamp(endCrontab) >= utils.getNow(False):
            left = utils.getDisposableCronTabTimeStamp(endCrontab) - utils.getNow(False)
        self.widget.topMc.leftTime.text = utils.formatDurationForShort(left)
        if left <= 0:
            self.widget.topMc.leftTime.text = '00:00:00.0'
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def checkRedFlag(self):
        p = BigWorld.player()
        curPower = p.fame.get(const.MAP_GAME_TILI_FAME_ID, 0)
        autoIncLimit = FD.data.get(const.MAP_GAME_TILI_FAME_ID, {}).get('autoIncLimit', 150)
        return curPower >= autoIncLimit

    def isOpen(self):
        isOpen = True
        if not gameglobal.rds.configData.get('enableMapGameV2', False):
            isOpen = False
        if not mapGameCommon.checkinMapGameTime():
            isOpen = False
        return isOpen

    def showGMInfo(self, isShow = False):
        for id in self.gridIdList:
            gridMc = self.widget.mapCanvas.bottomMc.getChildByName('grid%d' % id)
            if gridMc:
                gridMc.gmBox.visible = isShow
                pos = MGGPD.data.get(id, {}).get('pos', (-1, -1))
                gridMc.gmBox.tf.htmlText = 'id:' + str(id) + '<br>' + '(' + str(pos[0]) + ',' + str(pos[1]) + ')'
