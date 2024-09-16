#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameDonateProxy.o
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
import mapGameCommon
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import state_data as SD
from data import map_game_config_data as MGCD
from cdata import game_msg_def_data as GMDD
HEAD_ICON_PATH_PREFIX = 'mapgame/%s.dds'
BUFF_ICON_PATH_PREFIX = 'state/40/%s.dds'
MAX_REWARD_NUM = 6
SCORE_ITEM_RENDER_HEIGHT = 26

class MapGameDonateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameDonateProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_DONATE, self.hide)

    def reset(self):
        self.widget = None
        self.id = 0
        self.type = 0
        self.progress = 0
        self.state = 0
        self.rankVersion = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_DONATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_DONATE)

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
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_DONATE)
        p.base.requireMapGameDetailInfo(id)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.scoreList.itemHeight = SCORE_ITEM_RENDER_HEIGHT
        self.widget.scoreList.itemRenderer = 'MapGameDonate_scoreItem'
        self.widget.scoreList.lableFunction = self.itemFunction
        self.widget.scoreList.itemHeight = 26
        self.widget.scoreList.dataArray = []
        self.registerMenu()

    def refreshInfo(self):
        gamelog.debug('yedawang### DONATE refreshInfo')
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
        self.widget.itemName.text = buffInfo.get('name', '')
        self.widget.itemDesc.text = gridInfo.get('desc')
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
        if self.type == gametypes.MAP_GAME_GRID_TYPE_HANDIN_ITEM:
            self.widget.confirmBtn.label = gameStrings.MAP_GAME_DONATE_ITEM_LABEL
        elif self.type == gametypes.MAP_GAME_GRID_TYPE_HANDIN_FAME:
            self.widget.confirmBtn.label = gameStrings.MAP_GAME_DONATE_POWER_LABEL
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
        contentId = MGGPD.data.get(self.id, {}).get('contentId', 0)
        gridInfo = MGGD.data.get(contentId, {})
        itemId = gridInfo.get('handinShowId', 999)
        handinNum = gridInfo.get('handinNum', 0)
        itemData = uiUtils.getGfxItemById(itemId, handinNum)
        addFame = gridInfo.get('addFame', 0)
        if self.type == gametypes.MAP_GAME_GRID_TYPE_HANDIN_ITEM:
            confirmMsg = gameStrings.MAP_GAME_DONATE_ITEM_CONFIRM_MSG % (handinNum, addFame)
            itemNum = BigWorld.player().inv.countItemInPages(itemId)
            self.uiAdapter.messageBox.showCounterMsgBox(confirmMsg, self.donateItemConfirmCallback, counterData=itemData, counterRange=(0, itemNum / handinNum))
        elif self.type == gametypes.MAP_GAME_GRID_TYPE_HANDIN_FAME:
            confirmMsg = gameStrings.MAP_GAME_DONATE_POWER_CONFIRM_MSG % (handinNum, addFame)
            self.uiAdapter.messageBox.showYesNoMsgBox(confirmMsg, self.donatePowerConfirmCallback, itemData=itemData)

    def donatePowerConfirmCallback(self):
        BigWorld.player().cell.donateMapGameTili(self.id, 1)

    def donateItemConfirmCallback(self, conut):
        BigWorld.player().cell.donateMapGameItem(self.id, conut)

    def registerMenu(self):
        p = BigWorld.player()
        serverName = utils.getServerName(p.getOriginHostId())
        menuOffsetPos = [15, self.widget.summonBtn.height + 2]
        MenuManager.getInstance().registerMenuById(self.widget.summonBtn, uiConst.MENU_MAP_GAME_CALL_DONATE, {'data': {'gridId': self.id,
                  'serverName': serverName,
                  'playerName': p.roleName}}, events.LEFT_BUTTON, menuOffsetPos)
