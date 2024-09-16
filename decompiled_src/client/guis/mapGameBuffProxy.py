#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameBuffProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import gametypes
import mapGameCommon
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import state_data as SD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import map_game_config_data as MGCD
from cdata import game_msg_def_data as GMDD
HEAD_ICON_PATH_PREFIX = 'mapgame/%s.dds'
BUFF_ICON_PATH_PREFIX = 'state/40/%s.dds'
BOSS_STAGE_FAKE = 0

class MapGameBuffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameBuffProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_BUFF, self.hide)

    def reset(self):
        self.id = 0
        self.contentId = 0
        self.buffId = 0
        self.state = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_BUFF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_BUFF)

    def show(self, id):
        self.id = id
        p = BigWorld.player()
        gameCamp = p.mapGameCamp
        if not mapGameCommon.checkGridCampWithGridId(id, gameCamp, gameglobal.rds.ui.mapGameEvent.eventList):
            campName = MGCD.data.get('campNameDict', {})
            p.showGameMsg(GMDD.data.BELONG_TO_CAMP_LIMIT, campName.get(gameCamp))
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_BUFF)
        p.base.requireMapGameDetailInfo(id)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.title.visible = False
        self.widget.headMc.icon.fitSize = True
        self.widget.buffIcon.icon.fitSize = True

    def refreshInfo(self):
        gamelog.debug('yedawang### BUFF refreshInfo')
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
        self.widget.title.tf.text = gridInfo.get('title', '')
        self.widget.title.visible = True
        headIconId = gridInfo.get('headIconId', '10001')
        self.widget.headMc.icon.loadImage(HEAD_ICON_PATH_PREFIX % headIconId)
        type = gridInfo.get('type', 0)
        gridState = gridDetail.state
        if type == gametypes.MAP_GAME_GRID_TYPE_BUFF:
            if gridState in gametypes.MAP_GAME_GRID_STATES_HAS_FINISH or gridState == gametypes.MAP_GAME_GRID_STATE_ENABLE:
                self.state = 1
                self.widget.flag.tf.htmlText = gameStrings.MAP_GAME_BUFF_FLAG_TRUE
            else:
                self.state = 0
                self.widget.flag.tf.htmlText = gameStrings.MAP_GAME_BUFF_FLAG_FALSE
        elif type == gametypes.MAP_GAME_GRID_TYPE_ALTAR:
            desc = gridInfo.get('progressTitle', gameStrings.MAP_GAME_BUFF_FLAG_PROGRESS)
            self.widget.flag.tf.htmlText = desc % (int(gridDetail.progress), gridInfo.get('totalProgress'))
        self.widget.getWay.htmlText = gridInfo.get('getWay', '')
        self.widget.getDesc.text = gridInfo.get('getDesc', gameStrings.MAP_GAME_BUFF_GET_DESC)
        buffIcon = self.widget.buffIcon
        stage = gameglobal.rds.ui.mapGameMapV2.getStage()
        if MGCD.data.get('isSecondBossMode', False) and stage == BOSS_STAGE_FAKE:
            fakeBossBuff = gridInfo.get('fakeBuff', {})
            buffList = []
            for buffs in fakeBossBuff.values():
                for buff in buffs:
                    buffList.append(buff)

            self.buffId = buffList[0] if buffList else 40680
        else:
            self.buffId = gridInfo.get('addBossBuff', 40680)
        buffInfo = SD.data.get(self.buffId, {})
        iconPath = BUFF_ICON_PATH_PREFIX % buffInfo.get('iconId', '')
        buffIcon.icon.loadImage(iconPath)
        self.widget.buffName.text = buffInfo.get('name', '')
        self.widget.buffDesc.htmlText = buffInfo.get('desc', '')
