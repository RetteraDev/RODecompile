#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/isolateProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import utils
import npcConst
from guis import uiConst, uiUtils
from uiProxy import UIProxy
from callbackHelper import Functor
from data import isolate_config_data as ICD
from cdata import game_msg_def_data as GMDD

class IsolateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(IsolateProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmPayBail': self.onConfirmPayBail}
        uiAdapter.registerEscFunc(uiConst.WIDGET_PAY_BAIL, self.hide)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PAY_BAIL:
            self.payMed = mediator
            if self.freeChatType == npcConst.NPC_FUNC_FREE_FB_PUNISH_BY_BAIL:
                self.updateFreeFbPunish()
            else:
                self.updateBailMsg()

    def show(self, *args):
        if args:
            self.npc = args[0]
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PAY_BAIL)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PAY_BAIL)

    def reset(self):
        self.payMed = None
        self.npc = None
        self.npcId = None
        self.freeChatType = None

    def showFreeChatMsg(self, freeType, npcId):
        self.freeChatType = freeType
        self.npcId = npcId
        BigWorld.player().cell.fetchChatBanInfo()

    def showFreeFbPunish(self, npcId):
        self.freeChatType = npcConst.NPC_FUNC_FREE_FB_PUNISH_BY_BAIL
        self.npcId = npcId
        if self.payMed:
            self.updateFreeFbPunish()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PAY_BAIL)

    def onGetChatBanInfo(self):
        if self.freeChatType:
            p = BigWorld.player()
            msgBox = gameglobal.rds.ui.messageBox
            if self.freeChatType == npcConst.NPC_FUNC_CLEAN_CHAT_BLOCK_FREQUENCY:
                if getattr(p, 'chatBlockFrequency', 0) == 0:
                    msg = uiUtils.getTextFromGMD(GMDD.data.CLEAN_CHAT_BLOCK_FAIL_BY_ZERO, gameStrings.TEXT_ISOLATEPROXY_69)
                    msgBox.showAlertBox(msg)
                    return
                elif p.isBlockChat():
                    msg = uiUtils.getTextFromGMD(GMDD.data.CLEAN_CHAT_BLOCK_FAIL_BY_BLOCKING, gameStrings.TEXT_ISOLATEPROXY_75)
                    msgBox.showAlertBox(msg)
                    return
                else:
                    msg = uiUtils.getTextFromGMD(GMDD.data.CLEAN_CHAT_BLOCK_COST_MSG, gameStrings.TEXT_ISOLATEPROXY_81)
                    chatBlockFrequencyCleanInfo = ICD.data.get('chatBlockFrequencyCleanInfo', {})
                    maxCnt = max(chatBlockFrequencyCleanInfo.keys())
                    if p.chatBlockFrequency >= maxCnt:
                        coinCnt = chatBlockFrequencyCleanInfo[maxCnt]
                    else:
                        coinCnt = chatBlockFrequencyCleanInfo[p.chatBlockFrequency]
                    msg = msg % (p.chatBlockFrequency, coinCnt)
                    msgBox.showYesNoMsgBox(msg, yesCallback=self.cleanChatBlockFrequency)
                    return
            if self.freeChatType == npcConst.NPC_FUNC_FREE_CHAT_BY_BAIL:
                if not p.isBlockChat():
                    msg = uiUtils.getTextFromGMD(GMDD.data.NOT_BLOCK_CHAT, gameStrings.TEXT_ISOLATEPROXY_95)
                    msgBox.showAlertBox(msg)
                    return
                freeChatBailsInfo = ICD.data['freeChatBails']
                blockCnt = p.chatBlockFrequency if p.chatBlockFrequency <= max(freeChatBailsInfo.keys()) else max(freeChatBailsInfo.keys())
                bailCnt = freeChatBailsInfo[blockCnt]
                msg = uiUtils.getTextFromGMD(GMDD.data.FREE_CHAT_BLOCK_BAILS_MSG, gameStrings.TEXT_ISOLATEPROXY_102) % (p.chatBlockFrequency, bailCnt)
                blockLeftTime = p.getChatBlockChatDelay()
                leftTime = uiUtils.getTextFromGMD(GMDD.data.FREE_CHAT_BLOCK_LEFT_TIME, gameStrings.TEXT_ISOLATEPROXY_105) % utils.formatTimeStr(blockLeftTime)
                msg = '%s\n%s' % (leftTime, msg)
                msgBox.showYesNoMsgBox(msg, yesCallback=self.freeChatBail, yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)
                return
            if self.freeChatType == npcConst.NPC_FUNC_FREE_CHAT_BY_CASH:
                if not p.isBlockChat():
                    msg = uiUtils.getTextFromGMD(GMDD.data.NOT_BLOCK_CHAT, gameStrings.TEXT_ISOLATEPROXY_95)
                    msgBox.showAlertBox(msg)
                    return
                current = utils.getNow()
                chatFreedomTimeInfo = ICD.data.get('chatFreedomTimeInfo', {})
                blockCnt = p.chatBlockFrequency if p.chatBlockFrequency <= max(chatFreedomTimeInfo.keys()) else max(chatFreedomTimeInfo.keys())
                if p.chatBlockStartTime + chatFreedomTimeInfo.get(blockCnt, 0) > current:
                    msg = uiUtils.getTextFromGMD(GMDD.data.FREE_CHAT_BY_CASH_LEFTTIME, gameStrings.TEXT_ISOLATEPROXY_121)
                    msg = msg % utils.formatTimeStr(p.chatBlockStartTime + chatFreedomTimeInfo.get(blockCnt, 0) - current)
                    msgBox.showAlertBox(msg)
                    return
                chatFreedomCashInfo = ICD.data.get('chatFreedomCashInfo', {})
                blockCnt = p.chatBlockFrequency if p.chatBlockFrequency <= max(chatFreedomCashInfo.keys()) else max(chatFreedomCashInfo.keys())
                needCash = chatFreedomCashInfo.get(blockCnt, 0)
                msg = uiUtils.getTextFromGMD(GMDD.data.FREE_CHAT_BLOCK_CASH_MSG, gameStrings.TEXT_ISOLATEPROXY_130) % (p.chatBlockFrequency, needCash)
                blockLeftTime = p.getChatBlockChatDelay()
                leftTime = uiUtils.getTextFromGMD(GMDD.data.FREE_CHAT_BLOCK_LEFT_TIME, gameStrings.TEXT_ISOLATEPROXY_105) % utils.formatTimeStr(blockLeftTime)
                msg = '%s\n%s' % (leftTime, msg)
                msgBox.showYesNoMsgBox(msg, yesCallback=Functor(self.freeChatCash, needCash), yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def cleanChatBlockFrequency(self):
        npc = BigWorld.entities.get(self.npcId, None)
        if npc:
            npc.cell.npcCleanChatBlockFrequency('0')

    def freeChatCash(self, cashCnt):
        p = BigWorld.player()
        npc = BigWorld.entities.get(self.npcId, None)
        if npc:
            if uiUtils.checkBindCashEnough(cashCnt, p.bindCash, p.cash, Functor(npc.cell.npcFreeChatByCash, '0')):
                npc.cell.npcFreeChatByCash('0')

    def freeChatBail(self):
        npc = BigWorld.entities.get(self.npcId, None)
        if npc:
            npc.cell.npcFreeChatByBail('0')

    def updateBailMsg(self):
        p = BigWorld.player()
        if self.payMed:
            if p.isolateType in (gametypes.ISOLATE_TYPE_TRADE, gametypes.ISOLATE_TYPE_IDLE):
                msg = uiUtils.getTextFromGMD(GMDD.data.FREE_BAIL_FOR_TRADE_IDLE, gameStrings.TEXT_ISOLATEPROXY_159)
            else:
                leftTime = p.isolateTime - utils.getNow() + ICD.data['isolateQuestInterval'].get(p.isolateType, 0)
                msg = uiUtils.getTextFromGMD(GMDD.data.FREE_BAIL_MSG_WITH_LEFT_TIME, gameStrings.TEXT_ISOLATEPROXY_163) % utils.formatTime(leftTime)
            isolateBailsTypeInfo = ICD.data['isolateBails']
            isolateLvInterval = ICD.data['isolateLvInterval']
            obj = {'msg': msg,
             'cash': utils.getIsolateBails(p, isolateBailsTypeInfo, isolateLvInterval)}
            self.payMed.Invoke('updateMsg', uiUtils.dict2GfxDict(obj, True))
            BigWorld.callback(1, self.updateBailMsg)

    def onConfirmPayBail(self, *args):
        if self.freeChatType == npcConst.NPC_FUNC_FREE_FB_PUNISH_BY_BAIL:
            npc = BigWorld.entities.get(self.npcId, None)
            if npc:
                npc.cell.npcFreeFbPunishByBail('0')
        elif self.npc:
            self.npc.cell.npcLiberateWithBail(0)
        self.hide()
        gameglobal.rds.ui.funcNpc.close()

    def updateFreeFbPunish(self):
        if not self.payMed:
            return
        p = BigWorld.player()
        lvl, expireTime = p.getFbMaxPunishBailInfo()
        if lvl < 0:
            self.hide()
            return
        leftTime = utils.formatTime(expireTime - utils.getNow())
        msg = uiUtils.getTextFromGMD(GMDD.data.FREE_FB_PUNISH_MSG, gameStrings.TEXT_ISOLATEPROXY_190) % leftTime
        cash = p.getFreeFbPunishBail()
        obj = {'msg': msg,
         'cash': cash}
        self.payMed.Invoke('updateMsg', uiUtils.dict2GfxDict(obj, True))
