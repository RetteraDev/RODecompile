#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameFightProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import gamelog
import clientUtils
import gametypes
import utils
import math
import const
import mapGameCommon
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import state_data as SD
from data import fb_data as FD
from data import map_game_config_data as MGCD
from cdata import game_msg_def_data as GMDD
HEAD_ICON_PATH_PREFIX = 'mapgame/%s.dds'
BUFF_ICON_PATH_PREFIX = 'state/40/%s.dds'
MAX_REWARD_NUM = 6
SCORE_ITEM_RENDER_HEIGHT = 26

class MapGameFightProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameFightProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_FIGHT, self.hide)

    def reset(self):
        self.id = 0
        self.type = 0
        self.progress = 0
        self.state = 0
        self.rankVersion = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_FIGHT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_FIGHT)

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
        p = BigWorld.player()
        gameCamp = p.mapGameCamp
        if not mapGameCommon.checkGridCampWithGridId(id, gameCamp, gameglobal.rds.ui.mapGameEvent.eventList):
            campName = MGCD.data.get('campNameDict', {})
            p.showGameMsg(GMDD.data.BELONG_TO_CAMP_LIMIT, campName.get(gameCamp))
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_FIGHT)
        p.base.requireMapGameDetailInfo(id)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.scoreList.itemHeight = SCORE_ITEM_RENDER_HEIGHT
        self.widget.scoreList.itemRenderer = 'MapGameFight_scoreItem'
        self.widget.scoreList.lableFunction = self.itemFunction
        self.widget.scoreList.itemHeight = 26
        self.widget.scoreList.dataArray = []
        self.widget.listTitle.text = MGCD.data.get('MAP_GAME_FIGHT_RANK_TITLE', gameStrings.MAP_GAME_FIGHT_RANK_TITLE)
        self.registerMenu()

    def refreshInfo(self):
        gamelog.debug('yedawang### FIGHT refreshInfo')
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
        headIconId = gridInfo.get('headIconId', '10001')
        self.widget.headMc.icon.loadImage(HEAD_ICON_PATH_PREFIX % headIconId)
        self.widget.progressDesc.text = gridInfo.get('progressDesc', '')
        totalProgress = gridInfo.get('totalProgress', 0)
        self.progress = gridDetail.progress
        self.widget.progressBar.labelFunction = self.progressLableFunc
        self.widget.progressBar.currentValue = self.progress
        self.widget.progressBar.maxValue = totalProgress
        self.widget.rewardDesc.text = gridInfo.get('rewardDesc', '')
        rewardId = gridInfo.get('showBonus', 20001)
        rewardList = clientUtils.genItemBonus(rewardId)
        rewardNum = len(rewardList)
        for i in xrange(MAX_REWARD_NUM):
            itemMc = self.widget.getChildByName('reward%d' % i)
            if rewardNum > i:
                itemMc.visible = True
                itemId, itemCount = rewardList[i]
                itemMc.dragable = False
                itemMc.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
            else:
                itemMc.visible = False

        buffId = gridInfo.get('itemId', 999)
        buffInfo = SD.data.get(buffId, {})
        iconPath = BUFF_ICON_PATH_PREFIX % buffInfo.get('iconId', '')
        self.widget.smallIcon.icon.fitSize = True
        self.widget.smallIcon.icon.loadImage(iconPath)
        self.widget.bossName.text = buffInfo.get('name', '')
        if self.type == gametypes.MAP_GAME_GRID_TYPE_SINGLE_FB or self.type == gametypes.MAP_GAME_GRID_TYPE_SPRITE_FB:
            self.widget.typeDesc.text = gameStrings.MAP_GAME_FIGHT_POEPLE_SINGLE
        elif self.type == gametypes.MAP_GAME_GRID_TYPE_GROUP_FB:
            self.widget.typeDesc.text = gameStrings.MAP_GAME_FIGHT_POEPLE_TEAM
        self.widget.bossDesc.text = gridInfo.get('desc')
        rank = gridDetail.rank.get('0', {})
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
        gameglobal.rds.ui.mapGameMap.refreshGrid(self.id)

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

    def registerMenu(self):
        p = BigWorld.player()
        serverName = utils.getServerName(p.getOriginHostId())
        menuOffsetPos = [15, self.widget.summonBtn.height + 2]
        MenuManager.getInstance().registerMenuById(self.widget.summonBtn, uiConst.MENU_MAP_GAME_CALL_FIGHT, {'data': {'gridId': self.id,
                  'serverName': serverName,
                  'playerName': p.roleName}}, events.LEFT_BUTTON, menuOffsetPos)
