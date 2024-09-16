#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameDispatchProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import gametypes
import formula
import utils
import mapGameCommon
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import tipUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from helpers import capturePhoto
from guis import uiUtils
from callbackHelper import Functor
from data import state_data as SD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from data import summon_sprite_info_data as SSID
from data import map_game_config_data as MGCD
from data import summon_sprite_skin_data as SSSKIND
from cdata import game_msg_def_data as GMDD
HEAD_ICON_PATH_PREFIX = 'mapgame/%s.dds'
BUFF_ICON_PATH_PREFIX = 'state/40/%s.dds'
PHOTO_RES_NAME = 'MapGameDispatch_unitItem%d'
MAX_SPRITE_NUM = 3

class MapGameDispatchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameDispatchProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_DISPATCH, self.hide)

    def reset(self):
        self.id = 0
        self.contentId = 0
        self.state = 0
        self.type = 'mapGameDispatch'
        self.selectSpriteInfo = [-1, -1, -1]
        self.headGens = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_DISPATCH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_DISPATCH)

    def show(self, id):
        self.id = id
        p = BigWorld.player()
        gameCamp = p.mapGameCamp
        if not mapGameCommon.checkGridCampWithGridId(id, gameCamp, gameglobal.rds.ui.mapGameEvent.eventList):
            campName = MGCD.data.get('campNameDict', {})
            p.showGameMsg(GMDD.data.BELONG_TO_CAMP_LIMIT, campName.get(gameCamp))
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_DISPATCH)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.title.visible = False
        self.widget.spriteList.itemRenderer = 'MapGameDispatch_spriteItem'
        self.widget.spriteList.itemHeight = 71
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.lableFunction = self.itemFunction
        for i in xrange(MAX_SPRITE_NUM):
            spriteItem = self.widget.getChildByName('sprite%d' % i)
            spriteItem.binding = 'mapGameDispatch.0.%d' % i

        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.initHeadGen()
        self.refreshScore()

    def initHeadGen(self):
        self.headGens = {}
        for idx in xrange(MAX_SPRITE_NUM):
            headGen = capturePhoto.MapGameSpriteDispatchPhotoGen('gui/taskmask.tga', 238, PHOTO_RES_NAME % idx, idx)
            headGen.initFlashMesh()
            self.headGens[idx] = headGen

    def refreshInfo(self):
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
        p = BigWorld.player()
        itemList = []
        for spriteInfo in p.summonSpriteList.values():
            itemInfo = {}
            spriteIndex = spriteInfo['index']
            if spriteIndex in p.mapGameSpriteDispatch.keys():
                dispatchTime = p.mapGameGridDispatch.get(spriteIndex, 0)
                if utils.getNow() < dispatchTime + 3600 * MGCD.data.get('dispatchSpriteCD', 4):
                    continue
            itemInfo['spriteIndex'] = spriteIndex
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['lv'] = spriteInfo['props']['lv']
            itemInfo['score'] = self.calDispatchScore(spriteInfo)
            itemList.append(itemInfo)

        itemList.sort(key=lambda info: info.get('score'), reverse=True)
        self.widget.spriteList.dataArray = itemList
        self.widget.spriteList.validateNow()
        self.widget.power.text = gridInfo.get('dispatchFameNum', 0)
        gridState = gridDetail.state
        self.state = gridState == gametypes.MAP_GAME_GRID_STATE_ENABLE
        self.widget.confirmBtn.enabled = self.state

    def calDispatchScore(self, spriteInfo):
        if not spriteInfo:
            return
        lv = spriteInfo['props']['lv']
        familiar = spriteInfo['props']['familiar']
        spritePower = spriteInfo['combatScore']
        args = {'lv': lv,
         'familiar': familiar,
         'spritePower': spritePower}
        formulaId = MGCD.data.get('dispatchSpriteFormula', 0)
        return formula.calcFormulaById(formulaId, args)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.groupName = 'empty'
        itemMc.groupName = 'mapGameDispatch'
        itemMc.spriteIndex = itemData.spriteIndex
        if itemMc.spriteIndex in self.selectSpriteInfo:
            itemMc.gotoAndStop('select')
            itemMc.icon.dragable = False
        else:
            itemMc.gotoAndStop('normal')
            itemMc.icon.dragable = True
        spriteName = itemData.name
        spriteLv = itemData.lv
        itemMc.textField.text = spriteName
        itemMc.textField1.text = 'LV ' + str(spriteLv)
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = uiConst.SPRITE_ICON_PATH % str(iconId)
        itemMc.icon.setItemSlotData({'iconPath': iconPath})
        itemMc.mouseChildren = True
        itemMc.icon.validateNow()
        itemMc.icon.binding = 'mapGameDispatch.1.' + str(itemData.spriteIndex)
        TipManager.addTipByType(itemMc.icon, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')

    def getPropVal(self, spriteInfo):
        vPropCache = spriteInfo['props']['vPropCache']
        attVal = vPropCache[1] if vPropCache[1] >= vPropCache[2] else vPropCache[2]
        defVal = vPropCache[3] if vPropCache[3] >= vPropCache[4] else vPropCache[4]
        return [attVal, defVal, vPropCache[0]]

    def onSpriteDrag(self, nSpSrc, nSpIdSrc, nSpDes, nSpIdDes):
        slotSrcIdx = int(nSpSrc)
        spriteSrcIdx = int(nSpIdSrc)
        slotDesIdx = int(nSpDes)
        spriteDestIdx = int(nSpIdDes)
        if slotSrcIdx > 0 and slotDesIdx >= 0:
            self.selectSpriteInfo[spriteDestIdx] = spriteSrcIdx
        if slotDesIdx > 0:
            self.selectSpriteInfo[slotSrcIdx] = -1
        if self.widget:
            self.widget.spriteList.dataArray = self.widget.spriteList.dataArray
            self.refreshDispatchSprite()

    def refreshDispatchSprite(self):
        if not self.widget:
            return
        else:
            for i in xrange(MAX_SPRITE_NUM):
                spMc = self.widget.getChildByName('sprite%d' % i)
                spMc.slotIdx = i
                spriteIndex = self.selectSpriteInfo[i]
                if spriteIndex >= 0:
                    spMc.addMc.visible = False
                    self.takePhoto3D(i, spriteIndex)
                    spMc.addEventListener(events.MOUSE_CLICK, self.handleCancelSprite, False, 0, True)
                else:
                    spMc.addMc.visible = True
                    if self.headGens:
                        self.headGens[i].startCapture(None, None, None)

            self.refreshScore()
            return

    def refreshScore(self):
        score = 0
        for index in self.selectSpriteInfo:
            if index >= 0:
                spriteInfo = BigWorld.player().summonSpriteList.get(index)
                score += self.calDispatchScore(spriteInfo)

        self.widget.score.htmlText = gameStrings.MAP_GAME_DISPATCH_SCORE_DESC % score
        self.widget.confirmBtn.enabled = self.state and score > 0

    def handleCancelSprite(self, *args):
        e = ASObject(args[3][0])
        spriteMc = e.currentTarget
        self.selectSpriteInfo[spriteMc.slotIdx] = -1
        self.widget.spriteList.dataArray = self.widget.spriteList.dataArray
        self.refreshDispatchSprite()

    def takePhoto3D(self, idx, spriteIndex):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        skinId = 0
        if p.summonSpriteSkin.has_key(spriteId):
            skinId = p.summonSpriteSkin[spriteId].curUseDict.get(spriteIndex, 0)
        skinData = SSSKIND.data.get((spriteId, skinId), {})
        spriteModel = skinData.get('transformModelIdBefore', 0)
        materials = skinData.get('materialsBefore', 'Default')
        if self.headGens:
            self.headGens[idx].startCapture(spriteModel, materials, None)

    def isSpriteSelected(self, spriteIdx):
        return spriteIdx in self.selectSpriteInfo

    def handleConfirmBtnClick(self, *args):
        indexList = []
        p = BigWorld.player()
        for index in self.selectSpriteInfo:
            if index >= 0:
                indexList.append(index)

        if not indexList:
            p.showGameMsg(GMDD.data.DISPATCH_NUM_ZERO, ())
            return
        if len(indexList) < 3:
            msg = uiUtils.getTextFromGMD(GMDD.data.DIPATCH_NUM_NOT_ENOUGH)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.dispatchMapGameGrid, indexList))
        elif len(indexList) == 3:
            self.dispatchMapGameGrid(indexList)

    def dispatchMapGameGrid(self, indexList):
        BigWorld.player().cell.dispatchMapGameGrid(self.id, indexList)
