#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcInteractiveProxy.o
import BigWorld
import gameconfigCommon
import commNpcFavor
import gametypes
from gamestrings import gameStrings
import uiConst
import gamelog
from helpers import capturePhoto
from guis import events
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
import gameglobal
from data import fame_data as FD
from data import sys_config_data as SCD
from data import nf_npc_level_data as NNLD
from data import nf_npc_data as NND
from data import nf_npc_friendly_level_data as NNFLD
from uiProxy import UIProxy
SWF_W = 1920.0
SWF_H = 1080.0
TRIGGER_DESC_MAX_CNT = 3

class NpcInteractiveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcInteractiveProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NPC_INTERACTIVE, self.hide)

    def reset(self):
        self.entId = 0
        self.largeHead = None
        self.activityTip = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NPC_INTERACTIVE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
        self.handleSendBtnClick()
        BigWorld.callback(0, lambda : self.uiAdapter.npcSendGift.show(npcId=self.getNpcId()))

    def initHeadGen(self):
        size = 1920
        self.largeHead = capturePhoto.NpcInteractiveLargePhotoGen.getInstance('gui/taskmask.tga', size, 1014)
        self.largeHead.initFlashMesh()
        npc = BigWorld.entities.get(self.entId, None)
        if npc:
            uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)

    def doAction(self, npcId, actionId):
        if self.getNormalNpcId() != npcId:
            return
        if self.largeHead:
            self.largeHead.playTmpAction(str(actionId))

    def clearWidget(self):
        if self.largeHead:
            self.largeHead.endCapture()
        if self.activityTip:
            self.widget.removeChild(self.activityTip)
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_INTERACTIVE)
        self.uiAdapter.restoreUI()
        BigWorld.resetDepthOfField()
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)

    def show(self, entId):
        if not gameconfigCommon.enableNpcFavor():
            return False
        if not self.widget:
            self.uiAdapter.hideAllUI()
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_INTERACTIVE)
        self.entId = entId
        BigWorld.setDofTransitTime(0.5)
        BigWorld.setDepthOfField(True, 5, 0.15)
        p = BigWorld.player()
        p.ap.stopMove(True)
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI)
        npcId = self.getNpcId()
        gamelog.info('jbx:queryTopPFriendlyWithLvNF', npcId)
        BigWorld.player().base.queryTopPFriendlyWithLvNF(npcId)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.left.exitBtn
        self.initHeadGen()
        self.widget.bottom.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleSendBtnClick, False, 0, True)
        self.widget.bottom.addFriendBtn.addEventListener(events.BUTTON_CLICK, self.handleAddFrindBtnClick, False, 0, True)
        self.widget.bottom.addFriendBtn.enabled = True
        self.widget.left.detailBtn.addEventListener(events.BUTTON_CLICK, self.handleDetailBtnClick, False, 0, True)
        self.widget.bottom.rewardItem.dragable = False
        self.widget.addEventListener(events.WIDGET_REFLOWED, self.handleResize, False, 0, True)
        self.widget.bottom.dailyFriendly.visible = self.getNpcId() == BigWorld.player().npcFavor.todayFavor[0]
        self.widget.bottom.limitDescs.itemRenderer = 'NpcInteractive_limitDesc'
        self.widget.bottom.limitDescs.labelFunction = self.lableFunction
        TipManager.addTip(self.widget.bottom.dailyFriendly, gameStrings.NPC_INTERACTIVE_DAILY_VALUE)
        self.activityTip = self.widget.getInstByClsName('Activity_Tip_TipMc')
        self.widget.addChild(self.activityTip)
        self.activityTip.visible = False
        self.widget.bottom.weekHeartBeat.helpIcon.helpKey = SCD.data.get('ncFavorHelpKey', 461)
        self.widget.bottom.weekHeartBeat.visible = gameconfigCommon.enableNFNewQuestLoop()
        self.widget.bottom.progressBar.lockMc.visible = gameconfigCommon.enableNFNewQuestLoop()

    def hideTipListener(self, *args):
        if self.activityTip:
            self.activityTip.visible = False

    def handleAddFrindBtnClick(self, *args):
        BigWorld.player().base.addContactNF(self.getNpcId())

    def handleResize(self, *args):
        if not self.widget:
            return
        self.widget.width = self.widget.stage.stageWidth
        self.widget.height = self.widget.stage.stageHeight
        self.widget.bottom.scaleX = self.widget.stage.stageWidth / SWF_W
        self.widget.bottom.scaleY = self.widget.bottom.scaleX
        self.widget.left.scaleY = self.widget.stage.stageHeight / SWF_H
        self.widget.left.scaleX = self.widget.left.scaleY
        self.widget.bottom.y = self.widget.height - self.widget.bottom.height
        self.widget.largePhoto.width = self.widget.width
        self.widget.largePhoto.height = self.widget.width
        self.widget.largePhoto.x = 0
        self.widget.largePhoto.y = -(self.widget.largePhoto.height - self.widget.height) * 0.5

    def getNpcId(self):
        npc = BigWorld.entities.get(self.entId, None)
        if npc:
            return commNpcFavor.getNpcPId(npc.npcId)
        else:
            return 0

    def getNormalNpcId(self):
        npc = BigWorld.entities.get(self.entId, None)
        if npc:
            return npc.npcId
        else:
            return 0

    def refreshLeft(self):
        if not self.widget:
            return
        npcId = self.getNpcId()
        cfgData = NND.data.get(npcId, {})
        self.widget.left.npcName.htmlText = cfgData.get('name', '')
        self.widget.left.quality.gotoAndStop('level%d' % (commNpcFavor.getNpcLv(npcId) - 1))
        self.widget.left.txtBirthday.htmlText = cfgData.get('birthday', 'birthday')
        self.widget.left.txtDesc.htmlText = cfgData.get('txtDesc', 'desc')
        foodVal, moodVal, healthVal, socialVal = BigWorld.player().npcFavor.getNpcStatus(npcId)
        self.widget.left.hungryValue.text = foodVal
        self.widget.left.moodValue.text = moodVal
        self.widget.left.healythValue.text = healthVal
        self.widget.left.socialValue.text = socialVal
        self.widget.left.quality.x = self.widget.left.npcName.x + self.widget.left.npcName.textWidth + 20

    def getLvConfigData(self):
        p = BigWorld.player()
        npcId = self.getNpcId()
        level, _ = p.npcFavor.getPlayerRelationLvAndVal(npcId)
        return NNLD.data.get((npcId, level), {})

    def refreshBottom(self):
        if not self.widget:
            return
        p = BigWorld.player()
        level, pVal = p.npcFavor.getPlayerRelationLvAndVal(self.getNpcId())
        self.widget.bottom.relationshipLevel.gotoAndStop('level%d' % level)
        self.widget.bottom.helpIcon.helpKey = SCD.data.get('npcLevelHelpKeys', {}).get(level, 1)
        npcQuality = commNpcFavor.getNpcLv(self.getNpcId())
        levelData = NNFLD.data.get((npcQuality, level), {})
        if NNFLD.data.has_key((npcQuality, level + 1)):
            rewardId = NNFLD.data.get((npcQuality, level + 1), {}).get('rewardId', 0)
        else:
            rewardId = NNFLD.data.get((npcQuality, level), {}).get('rewardId', 0)
        self.widget.bottom.rewardItem.visible = bool(rewardId)
        self.widget.bottom.rewardItem.setItemSlotData(uiUtils.getGfxItemById(rewardId))
        minVal = levelData.get('friendlyBegin', 0)
        maxVal = levelData.get('friendlyEnd', 1)
        self.widget.bottom.progressBar.minValue = minVal
        self.widget.bottom.progressBar.maxValue = maxVal
        self.widget.bottom.progressBar.currentValue = int(pVal)
        self.widget.bottom.addFriendBtn.visible = not (p.friend.has_key(self.getNpcId()) and p.friend[self.getNpcId()].group == gametypes.FRIEND_GROUP_NPC)
        self.widget.bottom.dailyFriendly.txtValue.text = p.npcFavor.npcFavorValueDaily.get(self.getNpcId(), 0)
        self.widget.bottom.limitDescs.dataArray = self.getTriggerDes()
        text = self.widget.bottom.weekHeartBeat.txtValue
        self.widget.bottom.progressBar.lockMc.visible = p.npcFavor.isLockLvState(self.getNpcId(), level) and gameconfigCommon.enableNFNewQuestLoop()
        self.widget.bottom.weekHeartBeat.txtValue.text = p.npcFavor.nfWHeartBeat.get(self.getNpcId(), 0)
        self.widget.bottom.weekHeartBeat.helpIcon.x = text.x + text.textWidth + 10

    def lableFunction(self, *args):
        p = BigWorld.player()
        level, pVal = p.npcFavor.getPlayerRelationLvAndVal(self.getNpcId())
        itemData = ASObject(args[3][0])
        triggerMc = ASObject(args[3][1])
        triggerMc.visible = True
        triggerDesc = itemData[0]
        triggerTips = itemData[1]
        triggerMc.txtDesc.text = triggerDesc[1]
        triggerMc.limit.visible = triggerDesc[3]
        if level >= triggerDesc[0]:
            triggerMc.txtDesc.htmlText = triggerDesc[1]
        else:
            triggerMc.txtDesc.htmlText = uiUtils.toHtml(triggerDesc[1], '#969696')
        TipManager.addTip(triggerMc, triggerTips)

    def getLimitDesc(self, lv, key, npcId = 0):
        npcId = self.getNpcId() if not npcId else npcId
        lvName = NNFLD.data.get((commNpcFavor.getNpcLv(npcId), lv), {}).get('friendlyName', '')
        if key == 'fameBuff':
            fameId = NNLD.data.get((npcId, lv), {}).get('fameId', 0)
            fameName = FD.data.get(fameId, {}).get('name')
            return SCD.data.get('NPC_FUNC_LIMIT', {}).get(key, '%s %s') % (lvName, fameName)
        if key == 'expBuff':
            expName = NNLD.data.get((npcId, lv), {}).get('expName', 'expName')
            return SCD.data.get('NPC_FUNC_LIMIT', {}).get(key, '%s %s') % (lvName, expName)
        return SCD.data.get('NPC_FUNC_LIMIT', {}).get(key, '%s') % lvName

    def getTriggerDes(self):
        npcPId = self.getNpcId()
        friendLv, _ = BigWorld.player().npcFavor.getPlayerRelationLvAndVal(npcPId)
        limitDict = {}
        tipsDict = {}
        for (pId, lv), info in NNLD.data.iteritems():
            if pId != npcPId:
                continue
            for keys, keyName in gameStrings.NPC_FUNC_LIMIT_TYPE.iteritems():
                limitTipsInfo = info.get('NPC_FUNC_LIMIT_TIPS', {})
                if not limitTipsInfo.has_key(keys):
                    continue
                isCompleted = bool(BigWorld.player().npcFavor.checkIsCompleted(keys, npcPId, lv))
                if not limitDict.has_key(keys):
                    limitDict[keys] = (lv,
                     self.getLimitDesc(lv, keys),
                     keys,
                     isCompleted)
                    tipsDict[keys] = limitTipsInfo.get(keys, '')
                elif friendLv >= lv:
                    limitDict[keys] = (lv,
                     self.getLimitDesc(lv, keys),
                     keys,
                     isCompleted or limitDict[keys][3])
                    tipsDict[keys] = limitTipsInfo.get(keys, '')

        keys = limitDict.keys()
        keys.sort(cmp=lambda a, b: cmp(limitDict[a][0], limitDict[b][0]))
        return [ (limitDict[key], tipsDict[key]) for key in keys ]

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeft()
        self.refreshBottom()

    def handleDetailBtnClick(self, *args):
        npc = BigWorld.entities.get(self.entId, None)
        if npc:
            self.uiAdapter.npcRelationship.show(uiConst.NPC_RELATIONSHIP_TAB_OVERVIEW, self.getNpcId())

    def handleSendBtnClick(self, *args):
        npc = BigWorld.entities.get(self.entId, None)
        if npc:
            self.uiAdapter.npcSendGift.show(uiConst.NPC_SEND_GIFT_TAB, self.entId, self.getNpcId())
