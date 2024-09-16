#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameMapProxy.o
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
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import summon_sprite_info_data as SSID
from data import state_data as SD
from data import fame_data as FD
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
BUFF_ICON_LIST = ['buff1',
 'buff2',
 'buff3',
 'buff4']

class MapGameMapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameMapProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_MAP, self.hide)

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

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_MAP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.delTimer()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_MAP)
        gameglobal.rds.ui.setTempWeight(uiConst.WIDGET_CHAT_LOG, -1)

    def show(self):
        version = mapGameCommon.checkVersion()
        if version == uiConst.MAP_GAME_NOT_OPEN:
            return
        if version == uiConst.MAP_GAME_VERSION_2:
            gameglobal.rds.ui.mapGameMapV2.show()
            return
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_MAP)
        p = BigWorld.player()
        p.base.requireMapGameBasicInfo()
        p.base.requireMapGameBuff()
        if not p.mapGameFirstOpen:
            gameglobal.rds.ui.mapGameGuide.show()
            p.cell.openMapGamePanel()

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
        self.widget.scoreMc.score.desc.text = gameStrings.MAP_GAME_SCORE_DESC
        self.widget.scoreMc.shopBtn.addEventListener(events.MOUSE_CLICK, self.handleClickShopBtn, False, 0, True)
        self.widget.scoreMc.guideBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGuideBtn, False, 0, True)
        self.widget.detailMc.buffTitle.tf.text = gameStrings.MAP_GAME_DETAIL_BUFF_TITLE
        self.widget.detailMc.spriteTitle.tf.text = gameStrings.MAP_GAME_DETAIL_SPTITE_TITLE
        self.widget.detailMc.buffList.itemRenderer = 'MapGameMap_buffListItem'
        self.widget.detailMc.buffList.dataArray = []
        self.widget.detailMc.buffList.lableFunction = self.itemFunction
        self.addEvent(events.EVENT_FAME_UPDATE, self.handleFameUpdate)
        mapCanvas = self.widget.mapCanvas
        mapCanvas.bigBoss.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        mapCanvas.boss1.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        mapCanvas.boss2.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        mapCanvas.boss3.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        mapCanvas.boss4.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        mapCanvas.boss5.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)
        ASUtils.setHitTestDisable(mapCanvas.overMap, True)
        mapCanvas.addEventListener(events.MOUSE_DOWN, self.handleDragDown, False, 0, True)
        self.delTimer()
        self.timerFunc()
        self.addTimer()

    def initMapPos(self):
        mapCanvas = self.widget.mapCanvas
        mapWidth = mapCanvas.width
        mapHeight = mapCanvas.height
        mapCanvas.x = self.widget.stage.stageWidth / 2 - mapWidth / 2
        mapCanvas.y = self.widget.stage.stageHeight / 2 - mapHeight / 2

    def refreshInfo(self):
        version = mapGameCommon.checkVersion()
        if version == uiConst.MAP_GAME_NOT_OPEN:
            return
        elif version == uiConst.MAP_GAME_VERSION_2:
            gameglobal.rds.ui.mapGameMapV2.refreshInfo()
            return
        elif not self.widget:
            return
        else:
            p = BigWorld.player()
            if not hasattr(p, 'grids'):
                return
            self.gridsData = p.grids
            self.refreshScore()
            self.widget.removeAllInst(self.widget.mapCanvas.bottomMc)
            for id, info in MGGPD.data.iteritems():
                itemMc = self.widget.getInstByClsName('MapGameMap_gridBtn')
                itemMc.id = id
                itemMc.name = 'grid%d' % id
                pos = info.get('pos', (0, 0))
                x, y = self.getGridPos(pos)
                itemMc.x = x
                itemMc.y = y
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
                elif type in (gametypes.MAP_GAME_GRID_TYPE_BOSS, gametypes.MAP_GAME_GRID_TYPE_ELITE):
                    bossMc = self.widget.mapCanvas.getChildByName(iconType)
                    bossState = STATE_TYPE_LIST[state]
                    bossMc.gotoAndStop(bossState)
                    if bossState == 'fight':
                        ASUtils.setHitTestDisable(bossMc.fightLabel, True)
                    elif bossState == 'finish':
                        ASUtils.setHitTestDisable(bossMc.finishLabel, True)
                elif state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
                    gridMc.icon.gotoAndStop('empty')
                    if iconType in BUFF_ICON_LIST:
                        spritIcon = self.widget.getInstByClsName('MapGameMap_%s' % iconType)
                        spritIcon.name = iconType
                        spritIcon.x = x - 13
                        spritIcon.y = y - 30
                        self.widget.mapCanvas.bottomMc.addChild(spritIcon)
                        ASUtils.setHitTestDisable(spritIcon, True)
                elif state == gametypes.MAP_GAME_GRID_STATE_REWARD:
                    mapGameRewardRecord = p.mapGameRewardRecord
                    if mapGameRewardRecord and id in mapGameRewardRecord.keys():
                        gridMc.icon.gotoAndStop('empty')
                    else:
                        gridMc.icon.gotoAndStop('box')
                        itemMc.shine.visible = True
                        itemMc.reward = 1
                elif iconType in BUFF_ICON_LIST:
                    gridMc.icon.gotoAndStop('empty')
                    spritIcon = None
                    if state == gametypes.MAP_GAME_GRID_STATE_ENABLE:
                        spritIcon = self.widget.getInstByClsName('MapGameMap_%s' % iconType)
                        gridMc.tiredProgressBar.visible = False
                    elif state == gametypes.MAP_GAME_GRID_STATE_DISABLE:
                        spritIcon = self.widget.getInstByClsName('MapGameMap_lock%s' % iconType)
                    if spritIcon:
                        spritIcon.x = x - 13
                        spritIcon.y = y - 30
                        spritIcon.name = iconType
                        self.widget.mapCanvas.bottomMc.addChild(spritIcon)
                        ASUtils.setHitTestDisable(spritIcon, True)
                else:
                    if gridInfo.get('totalBonus', 0) and iconType == 'sprite':
                        gridMc.icon.gotoAndStop('reward')
                    else:
                        gridMc.icon.gotoAndStop(iconType)
                    if state == gametypes.MAP_GAME_GRID_STATE_ENABLE:
                        gridMc.tiredProgressBar.visible = True
                        totalProgress = gridInfo.get('totalProgress', 0)
                        progress = gridVal.progress
                        gridMc.tiredProgressBar.currentValue = progress
                        gridMc.tiredProgressBar.maxValue = totalProgress
                itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickGrid, False, 0, True)

            self.refreshDetailMc()
            gameglobal.rds.ui.mapGameGuide.refreshInfo()
            return

    def refreshGrid(self, gridId):
        version = mapGameCommon.checkVersion()
        if version == uiConst.MAP_GAME_NOT_OPEN:
            return
        if version == uiConst.MAP_GAME_VERSION_2:
            gameglobal.rds.ui.mapGameMapV2.refreshGrid(gridId)
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
        if state in [gametypes.MAP_GAME_GRID_STATE_FINISH, gametypes.MAP_GAME_GRID_STATE_CLOSE]:
            gridMc.icon.gotoAndStop('empty')
        elif state == gametypes.MAP_GAME_GRID_STATE_REWARD:
            mapGameRewardRecord = BigWorld.player().mapGameRewardRecord
            if mapGameRewardRecord and gridId in mapGameRewardRecord.keys():
                gridMc.icon.gotoAndStop('empty')
            else:
                gridMc.icon.gotoAndStop('box')
                itemMc.shine.visible = True
                itemMc.reward = 1
        info = MGGPD.data.get(gridId)
        contentId = info.get('contentId', 0)
        gridInfo = MGGD.data.get(contentId, {})
        type = gridInfo.get('type', 0)
        if state == gametypes.MAP_GAME_GRID_STATE_ENABLE and type not in [gametypes.MAP_GAME_GRID_TYPE_BUFF, gametypes.MAP_GAME_GRID_TYPE_START_POINT]:
            totalProgress = gridInfo.get('totalProgress', 0)
            progress = gridVal.progress
            gridMc.tiredProgressBar.currentValue = progress
            gridMc.tiredProgressBar.maxValue = totalProgress

    def getGridPos(self, pos):
        y = 60 * pos[1]
        offset = 35 if pos[1] % 2 else 0
        x = offset + 70 * pos[0]
        return (x, y)

    def refreshDetailMc(self):
        version = mapGameCommon.checkVersion()
        if version == uiConst.MAP_GAME_NOT_OPEN:
            return
        if version == uiConst.MAP_GAME_VERSION_2:
            gameglobal.rds.ui.mapGameMapV2.refreshDetailMc()
            return
        if not self.widget:
            return
        p = BigWorld.player()
        playerBuff = p.playerBuff.union(BigWorld.player().spriteBuff)
        buffList = MGCD.data.get('mapGameAddBuffList')
        buffArray = []
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
                iconId = SSID.data.get(spriteList[i], {}).get('spriteIcon', '000')
                iconPath = SPRITE_ICON_PATH % str(iconId)
                itemMc.dragable = False
                itemMc.setItemSlotData({'iconPath': iconPath})

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
        version = mapGameCommon.checkVersion()
        if version == uiConst.MAP_GAME_NOT_OPEN:
            return
        if version == uiConst.MAP_GAME_VERSION_2:
            gameglobal.rds.ui.mapGameMapV2.refreshRewardRecord()
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
        gamelog.debug('yedawang### onResize', stageWidth, stageHeight, self.widget.topMc.width)

    def refreshMapPos(self):
        if not self.widget:
            return
        gamelog.debug('yedawang### refreshMapPos')
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

    def handleClickGrid(self, *args):
        if self.isDraged:
            return
        mapGameBossGridIdList = MGCD.data.get('mapGameBossGridIdList', {})
        itemMc = ASObject(args[3][0]).currentTarget
        if itemMc.name == 'bigBoss':
            gridType = gametypes.MAP_GAME_GRID_TYPE_BOSS
            id = mapGameBossGridIdList.get('bigBoss')
        elif itemMc.name.startswith('boss'):
            gridType = gametypes.MAP_GAME_GRID_TYPE_ELITE
            id = mapGameBossGridIdList.get(itemMc.name)
        else:
            id = itemMc.id
            gridType = itemMc.gridType
        gamelog.debug('yedawang### clickGrid', id, gridType)
        if itemMc.reward:
            BigWorld.player().cell.getMapGameFinishReward(id)
            return
        self.closeAllWidget()
        if gridType == gametypes.MAP_GAME_GRID_TYPE_BOSS:
            gameglobal.rds.ui.mapGameBoss.show(id)
        elif gridType in gametypes.FIGHT_MAP_LIST:
            gameglobal.rds.ui.mapGameFight.show(id)
        elif gridType in gametypes.DONATE_MAP_LIST:
            gameglobal.rds.ui.mapGameDonate.show(id)
        elif gridType == gametypes.MAP_GAME_GRID_TYPE_BUFF:
            gameglobal.rds.ui.mapGameBuff.show(id)

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
        if not gameglobal.rds.configData.get('enableMapGame', False):
            isOpen = False
        if not mapGameCommon.checkinMapGameTime():
            isOpen = False
        return isOpen
