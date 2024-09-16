#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeSelectProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import gametypes
import formula
from callbackHelper import Functor
from guis import events
from guis.asObject import ASUtils, ASObject
from data import summon_sprite_info_data as SSID
from guis import tipUtils
from guis.asObject import TipManager
from guis import spriteChallengeHelper
from guis import voidLunHuiHelper
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from guis import menuManager
from data import state_data as SD
from data import sprite_challenge_data as SCD
MAX_SLOT_NUM = 4
MAX_BUFF_NUM = 4
MAX_AFF_NUM = 3
BOSS_START_Y = 54
MONS_START_Y = 145
CENTER_START_Y = 105
BOSS_WIDTH = 82
MONS_WIDTH = 50
BUFF_ITEM_WIDTH = 36
AFF_ITEM_START_X = 858
RIGHT_TOP_POS_X1 = 816
RIGHT_TOP_POS_X2 = 849

class SpriteChallengeSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpriteChallengeSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectIndex = 0
        self.type = 'spriteChallengeSelect'
        self.selectSpriteInfo = {}
        self.familist = []
        self.currentLevel = 0
        self.maxAttendNum = 1
        self.isPrepare = False
        self.canOperate = True
        self.reset()

    def reset(self):
        self.selectIndex = 0
        self.maxAttendNum = 1
        self.currentLevel = 0
        self.isPrepare = False
        self.canOperate = True
        self.selectSpriteInfo = {}
        self.familist = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_CHALLENGE_SELECT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_SELECT)
        self.reset()

    def show(self, level, isPrepare = False, canOprate = True):
        self.currentLevel = level
        self.isPrepare = isPrepare
        self.canOperate = canOprate
        self.maxAttendNum = spriteChallengeHelper.getInstance().getMaxAttendNum(self.currentLevel)
        self.familist = spriteChallengeHelper.getInstance().getTopSpriteFami(self.maxAttendNum)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_SELECT)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick)
        self.widget.spriteList.itemRenderer = 'SpriteChallengeSelect_SpriteItem'
        self.widget.spriteList.labelFunction = self.spriteLabelFunc
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.dataArray = []
        self.initStartSlots()
        self.initSelectList()
        self.widget.startBtn.addEventListener(events.BUTTON_CLICK, self.onStartBtnClick)
        if gameglobal.rds.configData.get('enableSpriteChallengeSpBuff', False):
            self.widget.buffText.visible = True
        else:
            self.widget.buffText.visible = False

    def initSelectList(self):
        p = BigWorld.player()
        self.selectSpriteInfo = {}
        needReset = spriteChallengeHelper.getInstance().needResetSpriteFami(self.maxAttendNum)
        spriteChallengeList = spriteChallengeHelper.getInstance().getLastSelectCheckList(self.maxAttendNum)
        for i, info in enumerate(spriteChallengeList):
            if p.summonSpriteList.has_key(info[0]):
                self.selectSpriteInfo[i] = list(info)

        for i in xrange(0, self.maxAttendNum):
            if not self.selectSpriteInfo.has_key(i):
                self.selectSpriteInfo[i] = [0, 0, 0]
            if needReset:
                self.selectSpriteInfo[i][2] = i

    def refreshSelectList(self):
        for i in xrange(self.maxAttendNum, MAX_SLOT_NUM):
            if self.selectSpriteInfo.has_key(i):
                del self.selectSpriteInfo[i]

    def initStartSlots(self):
        for i in xrange(MAX_SLOT_NUM):
            spMc = self.widget.getChildByName('sp%d' % i)
            spMc.slot.binding = 'spriteChallengeSelect.%s.%s' % (i, 0)
            spMc.lockMc.visible = False

    def spriteLabelFunc(self, *args):
        info = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.focusable = False
        if self.isSpriteSelected(info.spriteIndex):
            itemMc.gotoAndStop('select')
            itemMc.headMc.slot.dragable = False
        else:
            itemMc.gotoAndStop('normal')
            itemMc.headMc.slot.dragable = True and self.canOperate
        itemMc.spName.text = info.spriteName
        itemMc.lvText.text = 'Lv %d' % info.spriteLv
        itemMc.headMc.slot.setItemSlotData({'iconPath': info.iconPath})
        itemMc.headMc.slot.binding = 'spriteChallengeSelect.%s.%s' % (-1, info.spriteIndex)
        itemMc.headMc.slot.validateNow()
        itemMc.detailBtn.visible = False
        TipManager.addTipByType(itemMc.headMc.slot, tipUtils.TYPE_SPRITE_DETAIL_TIP, (info.spriteIndex,), False, 'upLeft')

    def isSpriteSelected(self, spriteIdx):
        selectInfo = self.selectSpriteInfo.values()
        for info in selectInfo:
            if spriteIdx == info[0]:
                return True

        return False

    def refreshInfo(self):
        if not self.widget:
            return
        if self.isPrepare:
            self.widget.startBtn.label = gameStrings.SPRITE_CHALLENGE_START
            self.widget.minBtn.visible = False
            self.widget.closeBtn.visible = True
            self.widget.closeBtn.x = RIGHT_TOP_POS_X2
        else:
            self.widget.startBtn.label = gameStrings.SPRITE_CHALLENGE_START_CONFIRM
            self.widget.closeBtn.visible = False
            self.widget.minBtn.visible = True
            self.widget.minBtn.x = RIGHT_TOP_POS_X2
        self.widget.startBtn.enabled = self.canOperate
        self.widget.minBtn.enabled = not self.canOperate
        self.widget.minBtn.addEventListener(events.BUTTON_CLICK, self.onMinBtnClick)
        self.refreshSelectList()
        self.widget.diffText.text = self.currentLevel
        self.refreshSpriteList()
        self.refreshSelectInfo()
        self.refreshCheckInfo()
        self.refreshDropInfo()
        self.refreshBuffsAffs()
        self.refreshEnermyInfo()

    def removeAllChild(self, mc):
        while mc.numChildren > 0:
            mc.removeChildAt(0)

    def refreshBuffsAffs(self):
        buffIds = spriteChallengeHelper.getInstance().getFullBuffByDiffIdx(spriteChallengeHelper.getInstance().getSelfLvKey(), self.currentLevel)
        affIds = spriteChallengeHelper.getInstance().getFullAffByDiffIdx(spriteChallengeHelper.getInstance().getSelfLvKey(), self.currentLevel)
        self.removeAllChild(self.widget.buffArea)
        self.removeAllChild(self.widget.affArea)
        for i in xrange(len(buffIds)):
            buffMc = self.widget.getInstByClsName('SpriteChallengeSelect_bufficon')
            self.widget.buffArea.addChild(buffMc)
            buffId = buffIds[i]
            cfg = SD.data.get(buffId, {})
            iconId = cfg.get('iconId', 'notFound')
            iconPath = 'state/22/%s.dds' % iconId
            buffMc.fitSize = True
            buffMc.loadImage(iconPath)
            buffMc.x = BUFF_ITEM_WIDTH * i
            TipManager.addTip(buffMc, cfg.get('desc', ''), tipUtils.TYPE_DEFAULT_BLACK)

        self.widget.affArea.x = AFF_ITEM_START_X - len(affIds) * BUFF_ITEM_WIDTH
        self.widget.affText.visible = len(affIds) > 0
        self.widget.affText.x = AFF_ITEM_START_X - len(affIds) * BUFF_ITEM_WIDTH - self.widget.affText.width - 10
        for i in xrange(len(affIds)):
            affMc = self.widget.getInstByClsName('SpriteChallengeSelect_bufficon')
            self.widget.affArea.addChild(affMc)
            affId = affIds[i]
            voidLunHuiHelper.getInstance().setCiZhuiInfo(affMc, affId)
            affMc.x = BUFF_ITEM_WIDTH * i

    def spriteSortFunc(self, idx1, idx2):
        p = BigWorld.player()
        spriteInfo1 = p.summonSpriteList.get(idx1, {})
        spriteInfo2 = p.summonSpriteList.get(idx2, {})
        if spriteInfo1 and spriteInfo2:
            return cmp(spriteInfo2.get('props', {}).get('lv', 0), spriteInfo1.get('props', {}).get('lv', 0))
        return 0

    def refreshSpriteList(self):
        p = BigWorld.player()
        spriteIndexs = p.summonSpriteList.keys()
        spriteIndexs.sort(cmp=self.spriteSortFunc)
        self.widget.spriteList.dataArray = self.getSpriteListInfoByIndex(spriteIndexs)

    def getSpriteListInfoByIndex(self, indexs):
        p = BigWorld.player()
        dataArray = []
        for index in indexs:
            spriteInfo = p.summonSpriteList.get(index)
            spriteId = spriteInfo.get('spriteId', 0)
            ssidData = SSID.data.get(spriteId, {})
            iconId = ssidData.get('spriteIcon', '000')
            iconPath = uiConst.SPRITE_ICON_PATH % str(iconId)
            info = {}
            info['iconPath'] = iconPath
            info['spriteName'] = spriteInfo.get('name', '')
            info['spriteLv'] = spriteInfo.get('props', {}).get('lv', 0)
            info['spriteIndex'] = index
            info['spriteId'] = spriteId
            dataArray.append(info)

        return dataArray

    def onSpriteDrag(self, nSpSrc, nSpIdSrc, nSpDes, nSpIdDes):
        spriteSrcIdx = int(nSpIdSrc)
        slotSrcIdx = int(nSpSrc)
        spriteDestIdx = int(nSpIdDes)
        slotDesIdx = int(nSpDes)
        if slotSrcIdx >= 0:
            if slotDesIdx == -1:
                if self.isSpriteSelected(spriteDestIdx):
                    return
            self.selectSpriteInfo[slotSrcIdx] = [spriteDestIdx, 0, self.selectSpriteInfo[slotSrcIdx][2]]
        if slotDesIdx >= 0:
            self.selectSpriteInfo[slotDesIdx] = [spriteSrcIdx, 0, self.selectSpriteInfo[slotDesIdx][2]]
        if self.widget:
            self.refreshSelectInfo()
            self.widget.spriteList.dataArray = self.widget.spriteList.dataArray
            self.refreshCheckInfo()
            self.refreshDropInfo()

    def getSlotBuffInfo(self, slotIdx):
        text = spriteChallengeHelper.getInstance().getSpriteSlotTip(self.currentLevel, slotIdx)
        buffId = spriteChallengeHelper.getInstance().getSpriteSlotBuff(self.currentLevel, slotIdx)
        return (buffId, text)

    def refreshSelectInfo(self):
        p = BigWorld.player()
        for i in xrange(MAX_SLOT_NUM):
            spMc = self.widget.getChildByName('sp%d' % i)
            buffId, buffText = self.getSlotBuffInfo(slotIdx=i)
            if buffId >= 0:
                spMc.slotBuff.visible = True
                spMc.slotBuff.fitSize = True
                cfg = SD.data.get(buffId, {})
                iconId = cfg.get('iconId', 'notFound')
                iconPath = 'state/22/%s.dds' % iconId
                spMc.slotBuff.loadImage(iconPath)
                TipManager.addTip(spMc.slotBuff, buffText)
            else:
                spMc.slotBuff.visible = False
            selectInfo = self.selectSpriteInfo.get(i, None)
            if i < self.maxAttendNum:
                spMc.slot.dragable = self.canOperate
                if selectInfo and p.summonSpriteList.has_key(selectInfo[0]):
                    spriteIdx = selectInfo[0]
                    spriteInfo = p.summonSpriteList.get(spriteIdx)
                    spriteId = spriteInfo.get('spriteId', 0)
                    ssidData = SSID.data.get(spriteId, {})
                    iconId = ssidData.get('spriteIcon', '000')
                    iconPath = uiConst.SPRITE_ICON_PATH % str(iconId)
                    spMc.slot.setItemSlotData({'iconPath': iconPath})
                    spMc.slot.binding = 'spriteChallengeSelect.%s.%s' % (i, spriteIdx)
                    spMc.slot.validateNow()
                    TipManager.addTipByType(spMc.slot, tipUtils.TYPE_SPRITE_DETAIL_TIP, (spriteIdx,), False, 'upLeft')
                else:
                    spMc.slot.setItemSlotData(None)
                    spMc.slot.binding = 'spriteChallengeSelect.%s.%s' % (i, 0)
                    spMc.slot.validateNow()
                    TipManager.removeTip(spMc.slot)
            else:
                spMc.slotBuff.visible = False
                spMc.slot.visible = False
                spMc.lockMc.visible = True

    def refreshEnermyInfo(self):
        levelData = SCD.data.get((spriteChallengeHelper.getInstance().getSelfLvKey(), self.currentLevel), {})
        bossNum = levelData.get('bossNum', 0)
        monsterNum = levelData.get('monsterNum', 1)
        self.removeOtherIcon()
        monsterStartY = MONS_START_Y
        bossStartY = BOSS_START_Y
        areaWidth = self.widget.bossArea.width
        if bossNum == 0:
            monsterStartY = CENTER_START_Y
        monsterStartX = areaWidth / 2 - monsterNum * MONS_WIDTH / 2
        if monsterNum == 0:
            bossStartY = CENTER_START_Y
        bossStartX = areaWidth / 2 - bossNum * BOSS_WIDTH / 2
        for i in xrange(bossNum):
            bossMc = self.widget.getInstByClsName('SpriteChallengeSelect_bossMc')
            self.widget.bossArea.addChild(bossMc)
            bossMc.x = bossStartX + (BOSS_WIDTH * i + (BOSS_WIDTH - bossMc.width) / 2)
            bossMc.y = bossStartY

        for i in xrange(monsterNum):
            monstMc = self.widget.getInstByClsName('SpriteChallengeSelect_smallBossMc')
            self.widget.bossArea.addChild(monstMc)
            monstMc.x = monsterStartX + (MONS_WIDTH * i + (MONS_WIDTH - monstMc.width) / 2)
            monstMc.y = monsterStartY

    def removeOtherIcon(self):
        bossArea = self.widget.bossArea
        removeMcs = []
        for i in xrange(bossArea.numChildren):
            mc = bossArea.getChildAt(i)
            if mc.name != 'bg':
                removeMcs.append(mc)

        for mc in removeMcs:
            bossArea.removeChild(mc)

    def refreshCheckInfo(self):
        for i in xrange(MAX_SLOT_NUM):
            ckBoxMc = self.widget.getChildByName('ckbox%d' % i)
            selectInfo = self.selectSpriteInfo.get(i, None)
            ckBoxMc.removeEventListener(events.EVENT_SELECT, self.onCheckBoxSelect)
            if selectInfo:
                ckBoxMc.selected = bool(selectInfo[1])
                ckBoxMc.enabled = True and self.canOperate
            else:
                ckBoxMc.selected = False
                ckBoxMc.enabled = False
            ckBoxMc.addEventListener(events.EVENT_SELECT, self.onCheckBoxSelect)

    def refreshDropInfo(self):
        for i in xrange(MAX_SLOT_NUM):
            dropMc = self.widget.getChildByName('drop%d' % i)
            selectInfo = self.selectSpriteInfo.get(i, None)
            dropMc.dropItem.enabled = True and self.canOperate
            TipManager.addTip(dropMc.loveIcon, gameStrings.SRPITE_FAME_TIP)
            if selectInfo and i < self.maxAttendNum:
                dropMc.visible = True
                ASUtils.setDropdownMenuData(dropMc.dropItem, self.getFamilList())
                dropMc.dropItem.removeEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
                dropMc.dropItem.selectedIndex = selectInfo[2]
                dropMc.dropItem.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
                dropMc.dropItem.index = i
            else:
                dropMc.visible = False

    def getFamilList(self):
        lst = []
        for info in self.familist:
            lst.append({'label': str(info[0])})

        return lst

    def handleIndexChange(self, *args):
        e = ASObject(args[3][0])
        index = e.currentTarget.index
        selectIdx = e.currentTarget.selectedIndex
        oldFamiIdx = self.selectSpriteInfo[index][2]
        newFamiIdx = selectIdx
        for i in xrange(self.maxAttendNum):
            if self.selectSpriteInfo[i][2] == newFamiIdx:
                self.selectSpriteInfo[i][2] = oldFamiIdx
            elif self.selectSpriteInfo[i][2] == oldFamiIdx:
                self.selectSpriteInfo[i][2] = newFamiIdx

        self.refreshDropInfo()

    def onCheckBoxSelect(self, *args):
        e = ASObject(args[3][0])
        mcName = e.currentTarget.name
        index = int(mcName[-1])
        selectInfo = self.selectSpriteInfo.get(index, None)
        if selectInfo:
            selectInfo = list(selectInfo)
            selectInfo[1] = 1 if e.currentTarget.selected else 0
            self.selectSpriteInfo[index] = selectInfo
        self.refreshCheckInfo()

    def onStartBtnClick(self, *args):
        p = BigWorld.player()
        spriteList = []
        checkList = []
        fameList = []
        for i in xrange(MAX_SLOT_NUM):
            selectInfo = self.selectSpriteInfo.get(i, None)
            if selectInfo:
                if selectInfo[0]:
                    spriteList.append(selectInfo[0])
                    checkList.append(selectInfo[1])
                    fameList.append(selectInfo[2])

        if not len(spriteList) == self.maxAttendNum:
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SPRITE_CHALLENGE_NO_SPRITE)
            return
        else:
            if self.isPrepare:
                p.base.spriteChallengeStart(spriteChallengeHelper.getInstance().getSelfLvKeyStr(), self.currentLevel, spriteList, checkList, fameList)
                self.hide()
            else:
                p.base.spriteListConfirm(self.currentLevel, spriteList, checkList, fameList)
            return

    def onCloseBtnClick(self, *args):
        if self.isPrepare:
            self.hide()
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SPRITE_CHALLENGE_QUIT_CONFIRM, self.quitFb, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)

    def onMinBtnClick(self, *args):
        self.hide()
        self.addPushMsg()

    def removePushMsg(self):
        pushId = uiConst.MESSAGE_TYPE_SPRITE_CHALLENGE_SELECT
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def addPushMsg(self):
        self.removePushMsg()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SPRITE_CHALLENGE_SELECT)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SPRITE_CHALLENGE_SELECT, {'click': self.onPushMsgClick})

    def onPushMsgClick(self):
        p = BigWorld.player()
        level = getattr(p, 'spriteChallengeProgress', 0)
        isPrepare = False
        p = BigWorld.player()
        if formula.inSpriteChallengeSpace(p.spaceNo):
            self.show(level, isPrepare, False)
        self.removePushMsg()

    def quitFb(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        fbType = formula.whatFubenType(fbNo)
        menuManager.getInstance().confirmOK(fbType)
        self.hide()
