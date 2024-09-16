#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameBossProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import gamelog
import gametypes
import utils
import const
import math
import mapGameCommon
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from helpers import cgPlayer
from guis import tipUtils
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import state_data as SD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import fb_data as FD
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
from guis import rankPanelUtils
MAX_BUFF_NUM = 4
SCORE_ITEM_RENDER_HEIGHT = 26
BOSS_STAGE_FAKE = 0
BOSS_STAGE_BOSS1 = 1
BOSS_STAGE_BOSS2 = 2
BOSS_STAGE_GRAVE = 3
BOSS_STAGE_GRAVE_END = 4

class MapGameBossProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameBossProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_BOSS, self.hide)

    def reset(self):
        self.id = 0
        self.detailInfo = None
        self.state = 0
        self.progress = 0
        self.rankVersion = -1
        self.cgPlayer = None
        self.schoolId = 0
        self.showRewardEffect = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_BOSS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_BOSS)
        if self.cgPlayer:
            self.onMovieEnd()

    def show(self, id):
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_NOT_OPEN:
            return
        if mapGameCommon.checkVersion() == uiConst.MAP_GAME_VERSION_1:
            mapGameProxy = gameglobal.rds.ui.mapGameMap
        else:
            mapGameProxy = gameglobal.rds.ui.mapGameMapV2
        if not mapGameProxy.widget:
            mapGameProxy.show()
        self.id = id
        self.schoolId = BigWorld.player().school
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_BOSS)
        BigWorld.player().base.requireMapGameDetailInfo(id)
        BigWorld.player().base.requireMapGameBuff()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if self.schoolId:
            self.widget.school.visible = True
            self.widget.school.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(self.schoolId, 'yuxu'))
        else:
            self.widget.school.visible = False
        ASUtils.setDropdownMenuData(self.widget.schoolChoose, rankPanelUtils.getDefaultSchoolMenuData())
        self.widget.schoolChoose.menuRowCount = len(rankPanelUtils.getDefaultSchoolMenuData())
        self.widget.schoolChoose.selectedIndex = const.SCHOOL_SET.index(self.schoolId)
        self.widget.schoolChoose.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.onChangeCallback, False, 0, True)
        self.widget.scoreList.itemHeight = SCORE_ITEM_RENDER_HEIGHT
        self.widget.scoreList.itemRenderer = 'MapGameBoss_scoreItem'
        self.widget.scoreList.lableFunction = self.itemFunction
        self.widget.scoreList.itemHeight = 26
        self.widget.scoreList.dataArray = []
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRewardBtn, False, 0, True)
        self.setTimeDesc()
        self.refreshRewardBtn()
        self.registerMenu()

    def onChangeCallback(self, *args):
        self.schoolId = rankPanelUtils.getDefaultSchoolMenuData()[self.widget.schoolChoose.selectedIndex]['schoolId']
        if self.schoolId:
            self.widget.school.visible = True
            self.widget.school.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(self.schoolId, 'yuxu'))
        else:
            self.widget.school.visible = False
        self.refreshRankList()

    def refreshInfo(self):
        gamelog.debug('yedawang### BOSS refreshInfo')
        if not self.widget:
            return
        p = BigWorld.player()
        if not hasattr(p, 'grids'):
            return
        if not p.grids.has_key(self.id):
            return
        contentId = MGGPD.data.get(self.id, {}).get('contentId', 0)
        gridInfo = MGGD.data.get(contentId, {})
        gridDetail = p.grids[self.id]
        self.type = gridInfo.get('type', 0)
        self.widget.title.tf.text = gridInfo.get('title')
        self.widget.progressDesc.text = gridInfo.get('progressDesc', '')
        totalProgress = gridInfo.get('totalProgress', 0)
        self.progress = gridDetail.progress
        self.widget.progressBar.labelFunction = self.progressLableFunc
        self.widget.progressBar.currentValue = self.progress
        self.widget.progressBar.maxValue = totalProgress
        self.widget.powerIcon.bonusType = gridInfo.get('moneyType')
        fbId = gridInfo.get('fubenid')
        fubenInfo = FD.data.get(fbId, {})
        needFame = 0
        if fubenInfo:
            reqFame = fubenInfo.get('reqFame', ((0, 0),))
            for fameId, fameValue in reqFame:
                if fameId == const.MAP_GAME_TILI_FAME_ID:
                    needFame = fameValue

        self.widget.power.text = needFame
        gridState = gridDetail.state
        self.state = gridState == gametypes.MAP_GAME_GRID_STATE_ENABLE
        self.widget.summonBtn.enabled = self.state
        self.widget.confirmBtn.enabled = self.state
        self.refreshRankList()
        self.refreshBuffList()
        gameglobal.rds.ui.mapGameMap.refreshGrid(self.id)

    def refreshRankList(self):
        p = BigWorld.player()
        gridDetail = p.grids[self.id]
        school = str(self.schoolId)
        rank = gridDetail.rank.get(school, {})
        rankList = []
        if rank and self.rankVersion != rank.get('ver'):
            data = rank.get('data', [])
            data.sort(key=lambda x: x[2], reverse=True)
            index = 1
            for info in data:
                rankInfo = {}
                rankInfo['rank'] = index
                rankInfo['name'] = info[1]
                rankInfo['hostId'] = info[3]
                rankInfo['value'] = info[2]
                rankInfo['gbId'] = info[0]
                index += 1
                rankList.append(rankInfo)

        self.widget.scoreList.dataArray = rankList
        self.widget.scoreList.validateNow()

    def refreshBuffList(self):
        if not self.widget:
            return
        bossBuff = BigWorld.player().bossBuff
        contentId = MGGPD.data.get(self.id, {}).get('contentId', 0)
        gridInfo = MGGD.data.get(contentId, {})
        buffList = gridInfo.get('bossBuffList', ())
        for i in xrange(MAX_BUFF_NUM):
            buffMc = self.widget.getChildByName('buff%d' % i)
            if i >= len(buffList):
                buffMc.visible = False
                continue
            buffMc.visible = True
            buffId = buffList[i]
            if buffId in bossBuff:
                buffMc.buff.gotoAndStop('buff')
            else:
                buffMc.buff.gotoAndStop('tip')
            buffInfo = SD.data.get(buffId, {})
            buffMc.buff.icon.fitSize = True
            iconPath = 'state/40/%s.dds' % buffInfo.get('iconId', '')
            buffMc.buff.icon.icon.loadImage(iconPath)
            TipManager.addTipByType(buffMc.buff.icon, tipUtils.TYPE_BUFF, buffId)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.x = 14
        itemMc.rank.text = itemData.rank
        itemMc.playerName.text = itemData.name
        itemMc.host.text = utils.getServerName(itemData.hostId)
        itemMc.score.text = itemData.value
        itemMc.gbId = itemData.gbId
        itemMc.name = itemData.name
        itemMc.hostId = itemData.hostId
        self.handleTop3Icon(itemMc, itemData.rank)
        itemMc.addEventListener(events.MOUSE_CLICK, self.onRankItemClick, False, 0, True)

    def onRankItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        gbId = long(itemMc.gbId)
        menuData = {'roleName': itemMc.name,
         'gbId': gbId,
         'hostId': itemMc.hostId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_MAP_GAME_RANK_LINK, menuData)

    def handleTop3Icon(self, item, rank):
        if rank > 0 and rank <= 3:
            item.top3Icon.visible = True
            item.top3Icon.x = 2
            item.rank.text = ''
            item.rank.htmlText = ''
            item.top3Icon.gotoAndStop(rank * 5)
        else:
            item.top3Icon.visible = False

    def progressLableFunc(self, *args):
        currentVal = int(args[3][0].GetNumber())
        maxVal = int(args[3][1].GetNumber())
        if float(currentVal) / maxVal == 0 and self.state:
            progress = 1e-06
        else:
            progress = math.floor(currentVal * 100000000 / maxVal) / 1000000.0
            progress = max(min(progress, 100), 0)
        return GfxValue('%.6f%%' % progress)

    def handleClickSummonBtn(self, *args):
        BigWorld.player().cell.callAttackMapGame(self.id)

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().cell.openMapGameFuben(self.id)

    def handleClickRewardBtn(self, *args):
        gameglobal.rds.ui.mapGameDamage.show(self.id)

    def playMovie(self, movieName):
        w = 238
        h = 238
        config = {'position': (0, 0, 0),
         'w': w,
         'h': h,
         'loop': True,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/MapGameBossWidget' + self.uiAdapter.getUIExt(), 'MapGameBoss_Photo', w, h)
        self.cgPlayer.playMovie(movieName, config)

    def onMovieEnd(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None

    def registerMenu(self):
        p = BigWorld.player()
        serverName = utils.getServerName(p.getOriginHostId())
        menuOffsetPos = [15, self.widget.summonBtn.height + 2]
        MenuManager.getInstance().registerMenuById(self.widget.summonBtn, uiConst.MENU_MAP_GAME_CALL_FIGHT, {'data': {'gridId': self.id,
                  'serverName': serverName,
                  'playerName': p.roleName}}, events.LEFT_BUTTON, menuOffsetPos)

    def setTimeDesc(self):
        if not self.widget:
            return
        stage = gameglobal.rds.ui.mapGameMapV2.getStage()
        movieName = ''
        if MGCD.data.get('isSecondBossMode', False):
            if stage <= BOSS_STAGE_GRAVE:
                finishStr = MGCD.data.get('mapGameGraveStartTime')
            else:
                finishStr = MGCD.data.get('mapGameFinishTime')
            if stage == BOSS_STAGE_BOSS1:
                movieName = 'mapgamefakeboss'
            else:
                movieName = 'mapgameboss'
        else:
            finishStr = MGCD.data.get('mapGameFinishTime')
            movieName = 'mapgameboss'
        finishTime = utils.getTimeSecondFromStr(finishStr)
        self.widget.listTitle.text = MGCD.data.get('MAP_GAME_BOSS_RANK_TITLE', gameStrings.MAP_GAME_BOSS_RANK_TITLE)
        self.widget.timeDesc.text = gameStrings.MAP_GAME_BOSS_OPEN_TIME % utils.formatDatetime(finishTime)
        self.playMovie(movieName)

    def refreshRewardBtn(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.showRewardEffect = False
        damageMargins = MGCD.data.get('mapGameDamageMargins', (10000, 20000, 30000, 40000, 50000))
        bossReward = p.mapGameBossReward.get(self.id, {}) if p.mapGameBossReward else {}
        mapGameBossDamage = p.mapGameBossDamage
        bossDamage = mapGameBossDamage.get(self.id, 0) if mapGameBossDamage else 0
        for index in xrange(len(damageMargins)):
            margin = damageMargins[index]
            if bossDamage >= margin and index not in bossReward.keys():
                self.showRewardEffect = True

        self.widget.rewardEffect.visible = self.showRewardEffect
        gameglobal.rds.ui.mapGameDamage.setConfirmBtn(self.showRewardEffect)
