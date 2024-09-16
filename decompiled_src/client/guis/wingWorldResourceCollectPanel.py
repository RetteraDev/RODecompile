#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldResourceCollectPanel.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import time
import events
import utils
import math
import gametypes
import tipUtils
import wingWorldUtils
import random
from helpers import capturePhoto
from guis import uiUtils
from guis import uiConst
from gameStrings import gameStrings
from callbackHelper import Functor
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import summon_sprite_skin_data as SSSKIND
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import wing_world_resource_sprite_slot_data as WWRSSD
from data import wing_world_resource_speed_data as WWRSD
from data import wing_world_config_data as WWCD
from data import wing_world_resource_sprite_random_event_data as WWRSRED
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
PHOTO_RES_NAME = 'WingWorldResourc_unitItem%d'
MIN_INDEX = 1
MAX_INDEX = 4
SPACE_NUM = 2
MOVE_NUM = 1
MOVE_WIDTH = 300
MAX_SPRITE_MODE = 4
RES_CONTUNUE_TIME = 2
SPRITE_COLLECT_RATE = 6

class WingWorldResourceCollectPanel(object):

    def __init__(self):
        super(WingWorldResourceCollectPanel, self).__init__()
        self.panel = None
        self.widget = None
        self.curSelSpriteIndex = 0
        self.addSlotIdx = 0
        self.callback = None
        self.resRandomShowTime = 0
        self.resRandomCallback = None
        self.headGens = {}

    def initPanel(self, panel, widget):
        self.panel = panel
        self.widget = widget
        self.panel.preBtn.addEventListener(events.BUTTON_CLICK, self.handlePreBtnClick, False, 0, True)
        self.panel.lastBtn.addEventListener(events.BUTTON_CLICK, self.handleLastBtnClick, False, 0, True)
        self.panel.getResourceBtn.addEventListener(events.BUTTON_CLICK, self.handleGetResourceBtnClick, False, 0, True)
        self.panel.oncePlaceBtn.addEventListener(events.BUTTON_CLICK, self.handleOncePlaceBtnClick, False, 0, True)
        TipManager.addTip(self.panel.oncePlaceBtn, WWCD.data.get('spriteResourceCollectPlaceOnceTips', ''))
        self.panel.resRandomPanel.visible = False
        self.panel.descMc.desc.text = WWCD.data.get('spriteResourceCollectDesc', '')
        self.widget.selectSpritePanel.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseSpritePanelClick, False, 0, True)
        self.widget.selectSpritePanel.spriteDropdown.addEventListener(events.INDEX_CHANGE, self.handleTypeChange, False, 0, True)
        self.widget.selectSpritePanel.helpIcon.helpKey = 376
        self.widget.selectSpritePanel.spriteList.itemRenderer = 'WingWorldResourc_spriteItem'
        self.widget.selectSpritePanel.spriteList.itemHeight = 77
        self.widget.selectSpritePanel.spriteList.barAlwaysVisible = True
        self.widget.selectSpritePanel.spriteList.dataArray = []
        self.widget.selectSpritePanel.spriteList.lableFunction = self.itemFunction
        p = BigWorld.player()
        p.cell.queryWingWorldResource(True)

    def unRegisterPanel(self):
        self.curSelSpriteIndex = 0
        self.addSlotIdx = 0
        self.callback = None
        self.resRandomShowTime = 0
        self.resRandomCallback = None
        self.panel = None
        self.widget = None

    def onShow(self):
        if not self.widget:
            return
        if not self.panel.visible:
            return
        p = BigWorld.player()
        p.cell.statsTriggerFromClient('loadWidgetTrigger', (uiConst.FAKE_WIDGET_ID_RESOURCE_COLLECT,))
        self.widget.timeDesc.text = WWCD.data.get('wingWorldResCollectTimeDesc', '')
        if not self.panel.preBtn.preIndex:
            self.panel.preBtn.enabled = False
            self.panel.lastBtn.enabled = True
            self.panel.canvas.x = 0
            self.panel.preBtn.preIndex = MIN_INDEX
            self.panel.lastBtn.lastIndex = MIN_INDEX + SPACE_NUM
        self.updateCollectTime()
        self.updateSpriteMode()
        self.updateResource()

    def updateCollectTime(self):
        if not self.widget:
            self.stopCallback()
            return
        if not self.panel.visible:
            self.stopCallback()
            return
        if self.panel.inTime and self.panel.noInTime:
            if self.inValidTime():
                self.panel.inTime.visible = True
                self.panel.noInTime.visible = False
            else:
                self.panel.inTime.visible = False
                self.panel.noInTime.visible = True
        else:
            self.stopCallback()
            return
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.callback = BigWorld.callback(1, self.updateCollectTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def inValidTime(self):
        cur = utils.getNow()
        stime = time.localtime(cur)
        chour, cmin, csec = stime[const.LOCAL_TIME_INDEX_HOUR], stime[const.LOCAL_TIME_INDEX_MIN], stime[const.LOCAL_TIME_INDEX_SEC]
        shour, smin, ehour, emin = WWCD.data.get('spriteResCollectTimeRange', (12, 30, 18, 30))
        currentSecs = chour * 3600 + cmin * 60 + csec
        startSecs = shour * 3600 + smin * 60
        endSecs = ehour * 3600 + emin * 60
        return startSecs < currentSecs < endSecs

    def updateResource(self):
        p = BigWorld.player()
        resDictCurrent = p.spriteWingWorldRes.resDictCurrent
        spriteInSlots = p.spriteWingWorldRes.spriteInSlots
        initResRateSum = {}
        amountResRateSum = {}
        for slotIdx, spriteIndex in spriteInSlots.iteritems():
            spriteInfo = p.summonSpriteList.get(spriteIndex, {})
            propVal = self.getPropVal(spriteInfo)
            for i in range(0, gametypes.WING_RESOURCE_TYPE_COUNT):
                initResVal = wingWorldUtils.getResourceCollectSpeed(i, propVal[i]) * SPRITE_COLLECT_RATE
                if not p.guildNUID:
                    guildResCount = 0
                else:
                    guildResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCountByGuild(p.guildNUID, i)
                countryResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCount(i)
                amountResVal = wingWorldUtils.getResourceCollectSpeed(i, propVal[i], guildResCount, countryResCount) * SPRITE_COLLECT_RATE
                if i in initResRateSum:
                    initResRateSum[i] = initResRateSum[i] + initResVal
                else:
                    initResRateSum[i] = initResVal
                if i in amountResRateSum:
                    amountResRateSum[i] = amountResRateSum[i] + amountResVal
                else:
                    amountResRateSum[i] = amountResVal

        canGetRes = False
        allSpeed = 0
        for i in range(0, gametypes.WING_RESOURCE_TYPE_COUNT):
            valT = getattr(self.panel, 'valT%d' % i, None)
            rateValT = getattr(self.panel, 'rateValT%d' % i, None)
            resIdIcon = getattr(self.panel, 'resIdIcon%d' % i, None)
            resName = WWRSD.data.get(i, {}).get('name', '')
            if i in initResRateSum:
                initResVal = int(initResRateSum[i])
            else:
                initResVal = 0
            if i in amountResRateSum:
                amountResVal = int(amountResRateSum[i])
                extraResVal = amountResVal - initResVal
            else:
                amountResVal = 0
                extraResVal = 0
            allSpeed += amountResVal
            if valT:
                valT.text = int(resDictCurrent.get(i, 0))
            if rateValT:
                rateValT.text = gameStrings.WING_WORLD_RESOURCE_COLLECT_RATE % str(amountResVal)
            if resIdIcon:
                tipDesc = gameStrings.WING_WORLD_RESOURCE_COLLECT_DESC % (resName, initResVal, extraResVal)
                TipManager.addTip(resIdIcon, tipDesc)
            if i in resDictCurrent and resDictCurrent[i]:
                canGetRes = True

        self.panel.getResourceBtn.enabled = canGetRes
        fameCurrent = int(p.spriteWingWorldRes.fameCurrent)
        self.panel.valT3.text = fameCurrent
        tipFame = gameStrings.WING_WORLD_RESOURCE_GETED_FAME_DESC % fameCurrent
        TipManager.addTip(self.panel.fameCurrent, tipFame)
        specialRareLv = int(p.spriteWingWorldRes.specialRareLv)
        maxSpeed = int(p.spriteWingWorldRes.maxSpeed)
        resTotalDay = int(p.spriteWingWorldRes.resTotalDay)
        self.panel.speedValT.text = gameStrings.WING_WORLD_RESOURCE_COLLECT_RATE % allSpeed
        amountResSpeed = self.getAmountResSpeed()
        self.panel.speedIcon.gotoAndStop('iconType%d' % specialRareLv)
        if amountResSpeed:
            tipSpeed = WWCD.data.get('resourceCollectSpeedTip', '%d%d%d') % (amountResSpeed, maxSpeed, resTotalDay)
            TipManager.addTip(self.panel.speedIcon, tipSpeed)
        else:
            TipManager.removeTip(self.panel.speedIcon)
        self.panel.specialIcon.gotoAndStop('iconType%d' % specialRareLv)
        if amountResSpeed:
            tipSpecial = WWCD.data.get('resourceCollectSpecialTip', '%d%d%d') % (amountResSpeed, maxSpeed, resTotalDay)
            TipManager.addTip(self.panel.specialIcon, tipSpecial)
        else:
            TipManager.removeTip(self.panel.specialIcon)

    def getAmountResSpeed(self):
        p = BigWorld.player()
        spData = WWCD.data.get('spriteResCollectRareLv', {}).get(p.wingWorld.step, {})
        for rang, val in spData.iteritems():
            low, high = rang
            return low

        return 0

    def handleGetResourceBtnClick(self, *args):
        p = BigWorld.player()
        p.base.submitSpriteWingWorldResCollect()

    def handleOncePlaceBtnClick(self, *args):
        p = BigWorld.player()
        p.base.oneKeyApplySpriteWingWorldResCollect()

    def handleAddSpriteBtnClick(self, *args):
        e = ASObject(args[3][0])
        spriteMode = e.currentTarget.parent
        self.addSlotIdx = spriteMode.slotIdx
        self.showSelectSpritePanel()

    def handlePreBtnClick(self, *args):
        curIndex = self.panel.preBtn.preIndex
        if curIndex == MIN_INDEX:
            return
        preNextIndex = curIndex - 1
        lastNextIndex = self.panel.lastBtn.lastIndex - 1
        self.udpateTween(self.panel.canvas.x + MOVE_WIDTH, preNextIndex, lastNextIndex)

    def handleLastBtnClick(self, *args):
        curIndex = self.panel.lastBtn.lastIndex
        if curIndex == MAX_INDEX:
            return
        preNextIndex = self.panel.preBtn.preIndex + 1
        lastNextIndex = curIndex + 1
        self.udpateTween(self.panel.canvas.x - MOVE_WIDTH, preNextIndex, lastNextIndex)

    def udpateTween(self, moveVal, preNextIndex, lastNextIndex):
        self.panel.preBtn.enabled = False
        self.panel.lastBtn.enabled = False
        tweenData = {}
        tweenData['time'] = 0.4
        tweenData['transition'] = 'linear'
        tweenData['x'] = moveVal
        tweenData['onCompleteParams'] = (preNextIndex, lastNextIndex)
        ASUtils.addTweener(self.panel.canvas, tweenData, self.endTweenCallBack)

    def endTweenCallBack(self, *args):
        if not self.widget:
            return
        if not self.panel.visible:
            return
        preNextIndex = int(args[3][0].GetNumber())
        lastNextIndex = int(args[3][1].GetNumber())
        if lastNextIndex == MAX_INDEX:
            self.panel.preBtn.enabled = True
            self.panel.lastBtn.enabled = False
        elif preNextIndex == MIN_INDEX:
            self.panel.preBtn.enabled = False
            self.panel.lastBtn.enabled = True
        else:
            self.panel.preBtn.enabled = True
            self.panel.lastBtn.enabled = True
        self.panel.preBtn.preIndex = preNextIndex
        self.panel.lastBtn.lastIndex = lastNextIndex

    def initHeadGen(self):
        self.headGens = {}
        for idx in xrange(1, MAX_SPRITE_MODE + 1):
            headGen = capturePhoto.WingWorldSpriteCollectPhotoGen('gui/taskmask.tga', 340, PHOTO_RES_NAME % idx, idx)
            headGen.initFlashMesh()
            self.headGens[idx] = headGen

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        spriteMode = e.currentTarget
        spriteMode.cancelBtn.visible = True
        spriteMode.overBg.visible = True
        spriteMode.resourceMc.visible = True

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        spriteMode = e.currentTarget
        spriteMode.cancelBtn.visible = False
        spriteMode.overBg.visible = False
        spriteMode.resourceMc.visible = False

    def handleCancelBtnClick(self, *args):
        e = ASObject(args[3][0])
        spriteMode = e.currentTarget.parent
        p = BigWorld.player()
        p.base.cancelSpriteWingWorldResCollect(spriteMode.slotIdx)

    def updateSpriteMode(self):
        p = BigWorld.player()
        spriteInSlots = p.spriteWingWorldRes.spriteInSlots
        unlockedSlots = list(p.spriteWingWorldRes.unlockedSlots)
        for idx in xrange(1, MAX_SPRITE_MODE + 1):
            mcName = 'spriteMode%d' % idx
            spriteMode = getattr(self.panel.canvas, mcName, None)
            if not spriteMode:
                continue
            spriteMode.slotIdx = idx
            spriteMode.overBg.visible = False
            spriteMode.cancelBtn.visible = False
            spriteMode.resourceMc.visible = False
            data = WWRSSD.data.get(idx, {})
            desc = data.get('desc', '')
            unlockDesc = data.get('unlockDesc', '')
            if idx in spriteInSlots:
                spriteIndex = spriteInSlots[idx]
                spriteInfo = p.summonSpriteList.get(spriteIndex, {})
                spriteName = spriteInfo.get('name', '')
                spriteMode.lock.visible = False
                spriteMode.addBtn.visible = False
                spriteMode.desc0.visible = False
                spriteMode.resourceMc.spriteName.text = spriteName
                propVal = self.getPropVal(spriteInfo)
                for i in range(0, gametypes.WING_RESOURCE_TYPE_COUNT):
                    valT = getattr(spriteMode.resourceMc, 'valT%d' % i, None)
                    if not valT:
                        continue
                    if not p.guildNUID:
                        guildResCount = 0
                    else:
                        guildResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCountByGuild(p.guildNUID, i)
                    countryResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCount(i)
                    resVal = int(wingWorldUtils.getResourceCollectSpeed(i, propVal[i], guildResCount, countryResCount) * SPRITE_COLLECT_RATE)
                    if self.getCollectSpeedRatio(i) == 1:
                        color = '#D9CFB6'
                    else:
                        color = '#74C424'
                    valT.htmlText = uiUtils.toHtml(gameStrings.WING_WORLD_RESOURCE_COLLECT_RATE % resVal, color)

                self.takePhoto3D(idx, spriteIndex)
                spriteMode.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
                spriteMode.addEventListener(events.MOUSE_OVER, self.handleMouseOver, False, 0, True)
                spriteMode.addEventListener(events.MOUSE_OUT, self.handleMouseOut, False, 0, True)
            elif idx in unlockedSlots:
                spriteMode.lock.visible = False
                spriteMode.addBtn.visible = True
                spriteMode.desc0.visible = True
                spriteMode.desc0.htmlText = desc
                spriteMode.addBtn.addEventListener(events.BUTTON_CLICK, self.handleAddSpriteBtnClick, False, 0, True)
                if self.headGens:
                    self.headGens[idx].startCapture(None, None, None)
                spriteMode.removeEventListener(events.MOUSE_OVER, self.handleMouseOver)
                spriteMode.removeEventListener(events.MOUSE_OUT, self.handleMouseOut)
            else:
                spriteMode.lock.visible = True
                spriteMode.addBtn.visible = False
                spriteMode.desc0.visible = True
                spriteMode.desc0.htmlText = unlockDesc

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

    def resetHeadGen(self):
        for photo in self.headGens.values():
            photo.endCapture()

        self.headGens = {}

    def handleCloseSpritePanelClick(self, *args):
        self.widget.selectSpritePanel.visible = False

    def handleTypeChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updatSpritesTypeList(itemMc.selectedIndex)

    def showSelectSpritePanel(self):
        self.widget.selectSpritePanel.visible = True
        typeToSort = [gameStrings.TEXT_WINGWORLDRESOURCECOLLECTPANEL_440, gameStrings.TEXT_WINGWORLDRESOURCECOLLECTPANEL_440_1, gameStrings.TEXT_WINGWORLDRESOURCECOLLECTPANEL_440_2]
        typeList = []
        for i, vlaue in enumerate(typeToSort):
            typeInfo = {}
            typeInfo['label'] = vlaue
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.selectSpritePanel.spriteDropdown, typeList)
        self.widget.selectSpritePanel.spriteDropdown.menuRowCount = min(len(typeList), 5)
        if self.widget.selectSpritePanel.spriteDropdown.selectedIndex == -1:
            self.widget.selectSpritePanel.spriteDropdown.selectedIndex = 0
        p = BigWorld.player()
        spriteNumLimit = SCD.data.get('spriteNumLimit', 20)
        self.widget.selectSpritePanel.holdSpritesT.text = '%d/%d' % (len(p.summonSpriteList), spriteNumLimit)
        self.updatSpritesTypeList(self.widget.selectSpritePanel.spriteDropdown.selectedIndex)

    def getResVal(self, resId, val):
        resData = WWRSD.data.get(resId, {})
        speedList = resData.get('speedList', [])
        for value in speedList:
            section = value[0]
            rate = value[1]
            if val >= section[0] and val <= section[1]:
                return math.ceil(val * rate)

        return 0

    def getPropVal(self, spriteInfo):
        vPropCache = spriteInfo['props']['vPropCache']
        attVal = vPropCache[1] if vPropCache[1] >= vPropCache[2] else vPropCache[2]
        defVal = vPropCache[3] if vPropCache[3] >= vPropCache[4] else vPropCache[4]
        return [attVal, defVal, vPropCache[0]]

    def getCollectSpeedRatio(self, resId):
        p = BigWorld.player()
        if not p.guildNUID:
            guildResCount = 0
        else:
            guildResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCountByGuild(p.guildNUID, resId)
        countryResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCount(resId)
        return wingWorldUtils.getResCollectRatioGuild(guildResCount) * wingWorldUtils.getResCollectRatioCountry(countryResCount)

    def sortSpritesList(self, typeIndex):
        p = BigWorld.player()
        spriteInSlots = p.spriteWingWorldRes.spriteInSlots
        itemList = []
        for spriteInfo in p.summonSpriteList.values():
            spriteIndex = spriteInfo['index']
            propVal = self.getPropVal(spriteInfo)
            resVals = []
            szResVals = []
            for i in range(0, gametypes.WING_RESOURCE_TYPE_COUNT):
                if not p.guildNUID:
                    guildResCount = 0
                else:
                    guildResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCountByGuild(p.guildNUID, i)
                countryResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCount(i)
                resVal = int(wingWorldUtils.getResourceCollectSpeed(i, propVal[i], guildResCount, countryResCount) * SPRITE_COLLECT_RATE)
                if self.getCollectSpeedRatio(i) == 1:
                    color = '#D9CFB6'
                else:
                    color = '#74C424'
                szResVal = uiUtils.toHtml(gameStrings.WING_WORLD_RESOURCE_COLLECT_RATE % resVal, color)
                resVals.append(resVal)
                szResVals.append(szResVal)

            itemInfo = {}
            itemInfo['spriteIndex'] = spriteIndex
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['resVals'] = resVals
            itemInfo['szResVals'] = szResVals
            itemInfo['state'] = 1 if spriteIndex in spriteInSlots.values() else 0
            itemList.append(itemInfo)

        return sorted(itemList, key=lambda d: d['resVals'][typeIndex], reverse=True)

    def updatSpritesTypeList(self, typeIndex):
        spritesList = self.sortSpritesList(typeIndex)
        self.widget.selectSpritePanel.spriteList.dataArray = spritesList
        self.widget.selectSpritePanel.spriteList.validateNow()

    def updateSpriteItemDown(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if not self.addSlotIdx:
            return
        if not target.enabled:
            return
        target.selected = True
        self.widget.selectSpritePanel.visible = False
        p = BigWorld.player()
        p.base.applySpriteWingWorldResCollect(self.addSlotIdx, target.spriteIndex)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.groupName = 'empty'
        itemMc.groupName = 'wingWorldResourceCollect%s'
        itemMc.addEventListener(events.BUTTON_CLICK, self.updateSpriteItemDown, False, 0, True)
        itemMc.spriteIndex = itemData.spriteIndex
        spriteName = itemData.name
        state = itemData.state
        stateDesc = gameStrings.TEXT_WINGWORLDRESOURCECOLLECTPANEL_552 if state else ''
        szResVals = itemData.szResVals
        itemMc.labels = [spriteName,
         stateDesc,
         szResVals[0],
         szResVals[1],
         szResVals[2]]
        itemMc.enabled = not state
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.slot.validateNow()
        TipManager.addTipByType(itemMc.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')

    def getRandomSpriteId(self):
        p = BigWorld.player()
        spriteInSlots = p.spriteWingWorldRes.spriteInSlots
        if not spriteInSlots:
            return 0
        spriteIndexs = spriteInSlots.values()
        r = random.randint(0, len(spriteIndexs) - 1)
        spriteInfo = p.summonSpriteList.get(spriteIndexs[r], {})
        spriteId = spriteInfo.get('spriteId', 0)
        return spriteId

    def updateCollectResRandom(self, eIds, showTime):
        if not self.widget:
            return
        if not self.panel.visible:
            return
        self.panel.resRandomPanel.visible = True
        self.resRandomShowTime = showTime
        self.panel.resRandomPanel.gotoAndPlay('up')
        getResMc = self.panel.resRandomPanel.getResMc
        spriteId = self.getRandomSpriteId()
        if spriteId:
            getResMc.slot.visible = True
            getResMc.slotBg.visible = True
            getResMc.noneSpriteIcon.visible = False
            iconId = SSID.data.get(spriteId, {}).get('spriteIcon', '000')
            iconPath = SPRITE_ICON_PATH % str(iconId)
            getResMc.slot.dragable = False
            getResMc.slot.setItemSlotData({'iconPath': iconPath})
        else:
            getResMc.slot.visible = False
            getResMc.slotBg.visible = False
            getResMc.noneSpriteIcon.visible = True
        eventDesc = ''
        for eId in eIds:
            desc = WWRSRED.data.get(eId, {}).get('desc', '')
            if not eventDesc:
                eventDesc = desc
            else:
                eventDesc = eventDesc + '   ' + desc

        getResMc.desc1.text = eventDesc
        self.panel.resRandomPanel.rewardMcClose.addEventListener(events.BUTTON_CLICK, self.closeResRandomPanel, False, 0, True)
        self.updateResRandomTime()

    def updateResRandomTime(self):
        if not self.widget or not self.panel.visible:
            self.stopResRandomCallback()
            return
        costTime = utils.getNow() - self.resRandomShowTime
        if costTime >= RES_CONTUNUE_TIME:
            self.panel.resRandomPanel.gotoAndPlay('end')
            ASUtils.callbackAtFrame(self.panel.resRandomPanel, 25, self.visibleResRandom)
            self.stopResRandomCallback()
            return
        if self.resRandomCallback:
            BigWorld.cancelCallback(self.resRandomCallback)
        self.resRandomCallback = BigWorld.callback(1, self.updateResRandomTime)

    def stopResRandomCallback(self):
        if self.resRandomCallback:
            BigWorld.cancelCallback(self.resRandomCallback)
            self.resRandomCallback = None

    def closeResRandomPanel(self, *args):
        self.panel.resRandomPanel.gotoAndPlay('end')
        ASUtils.callbackAtFrame(self.panel.resRandomPanel, 25, self.visibleResRandom)
        self.stopResRandomCallback()

    def visibleResRandom(self, *args):
        if not self.widget or not self.panel.visible:
            return
        self.panel.resRandomPanel.visible = False

    def updateWindWorldResCollect(self):
        if not self.widget:
            return
        if not self.panel.visible:
            return
        self.updateSpriteMode()
        self.updateResource()
