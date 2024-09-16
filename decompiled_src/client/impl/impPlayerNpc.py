#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerNpc.o
from gamestrings import gameStrings
import Math
import BigWorld
import gameglobal
import gametypes
import npcConst
import utils
import const
import gamelog
from guis import uiConst, messageBoxProxy
from callbackHelper import Functor
from guis import uiUtils
from guis import npcFuncMappings
from data import npc_data as ND
from data import quest_npc_data as QND
from data import social_school_data as SSD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import qiren_clue_reverse_data as QCRD
from data import qiren_clue_data as QCD
from data import client_building_proxy_data as CBPD

class ImpPlayerNpc(object):

    def setCameraToNPC(self, npcId, dis = 2.5, fov = 0.6):
        e = BigWorld.entities.get(npcId)
        height = e.model.height * 0.8
        dir = self.position - e.position
        dir[1] = 0
        dir.normalise()
        pos = e.model.position + Math.Vector3(dir[0] * dis, height, dir[2] * dis)
        dir *= -1
        m = Math.Matrix()
        m.lookAt(pos, dir, (0, 1, 0))
        gamelog.debug('bgf:camera', self.position, e.position, height, dir, pos)
        pro = BigWorld.projection()
        oldFov = pro.fov
        pro.fov = fov
        ca = BigWorld.FreeCamera()
        ca.set(m)
        BigWorld.camera(ca)
        ca.fixed = 1
        BigWorld.setDofTransitTime(0.5)
        BigWorld.setDepthOfField(True, 0, 5, 10, 5, 3)
        self.lockKey(gameglobal.KEY_POS_NPC)
        return (oldFov, npcId)

    def recoverCamera(self, data):
        e = BigWorld.entity(data[1])
        if e:
            e.model.setModelNeedHide(True, 1.0)
        BigWorld.camera(gameglobal.rds.cam.cc)
        self.unlockKey(gameglobal.KEY_POS_NPC)
        self.updateActionKeyState()
        pro = BigWorld.projection()
        pro.fov = data[0]
        BigWorld.resetDepthOfField()

    def npcDialog(self, entId, options):
        gamelog.debug('jorsef: npcId: ', entId, ' options: ', options)
        npcEnt = BigWorld.entity(entId)
        npcId = npcEnt.npcId
        npcData = ND.data.get(npcId, None)
        if npcData == None:
            return
        else:
            schoolLimits = npcData.get('schoolLimits', ())
            if schoolLimits and self.school not in schoolLimits:
                chatIds = SCD.data.get('SCHOOL_LIMIT_CHAT_IDS', [2])
                npcEnt.showMultiNpcChatWindow(chatIds)
                return
            openType = npcData.get('full', 0)
            panelOpenType = npcData.get('open', 0)
            defaultChatId = ND.data.get(npcId, {}).get('chat', [])
            gameglobal.rds.ui.npcPanel.setNPCInfo(entId, options, defaultChatId)
            funcNum = len(options)
            hasQuest = False
            priority = npcEnt.getNpcPriority()
            if priority in (gameglobal.NPC_WITH_COMPLETE_QUEST, gameglobal.NPC_WITH_AVAILABLE_QUEST, gameglobal.NPC_WITH_UNCOMPLETE_QUEST):
                hasQuest = True
            else:
                for key in options.keys():
                    if key[0] in (npcConst.NPC_FUNC_QUEST,):
                        options.pop(key)
                        funcNum -= 1

            for key in options.keys():
                if key[0] in (npcConst.NPC_FUNC_MARKER,):
                    options.pop(key)
                    funcNum -= 1

            if not options or funcNum <= 0:
                funcClosedChatId = ND.data.get(npcId, {}).get('funcClosedChatId', [])
                if funcClosedChatId:
                    defaultChatId = funcClosedChatId
                if defaultChatId:
                    if npcEnt:
                        npcEnt.showMultiNpcChatWindow(defaultChatId)
                return
            if priority == gameglobal.NPC_WITH_COMPLETE_QUEST and self.autoCompleteQuestLoop(entId):
                return
            gamelog.debug('jorsef: npcId:1 ', openType, panelOpenType, funcNum, options, hasQuest)
            if panelOpenType == 1 or funcNum == 1:
                items = options.items()
                key, item = items[0]
                if hasQuest:
                    for _key, _item in items:
                        if _key[0] == npcConst.NPC_FUNC_QUEST:
                            key, item = _key, _item
                            break

                type = key[0]
                if not npcFuncMappings.onImpPlayerCallFunc(type, entId, options, hasQuest):
                    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)
            else:
                for key, item in options.items():
                    type = key[0]
                    if type == npcConst.NPC_FUNC_GUILD:
                        op = item[0]
                        if op in gametypes.GUILD_NPC_FREE_RESIDENT:
                            if gameglobal.rds.ui.guild.residentNpcId != entId:
                                npcEnt.cell.openGuildResident()
                                return
                            BigWorld.player().onOpenGuildResident(BigWorld.player().guildNUID, gameglobal.rds.ui.guild.residentNpcId, gameglobal.rds.ui.guild.residentTemplateId, gameglobal.rds.ui.guild.bNeedTreat)

                gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)
            return

    def directTranfer(self, entId, data, idx):
        BigWorld.entities.get(entId).cell.npcDirectTeleport(data, idx)

    def rejoinSocSchool(self, toSchool):
        if self.curSocSchool:
            self.showGameMsg(GMDD.data.SOCIAL_SCHOOL_OCCUPIED, ())
            return
        if not self.socSchools.has_key(toSchool):
            self.showGameMsg(GMDD.data.SOCIAL_SCHOOL_ERROR_SCHOOL, ())
            return
        msg = gameStrings.TEXT_IMPPLAYERNPC_158 % SSD.data.get(toSchool, {}).get('socMoney', 0)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.rejoinSocSchool, toSchool))

    def npcTeleportByClientNpc(self, hostId, data, idx):
        self.cell.npcTeleportByClientNpc(hostId, data, idx)

    def acceptQuestByClientNpc(self, npcID, npcNo, hostId, questId):
        self.cell.acceptQuestByClientNpc(npcID, npcNo, hostId, questId)

    def onAcceptQuestByClientNpc(self, npcID, questId, isSucc):
        self.acceptQuest(questId, isSucc)
        clientNpc = BigWorld.entities.get(npcID)
        if clientNpc:
            clientNpc.onAcceptQuest(questId)

    def completeQuestByClientNpc(self, npcID, npcNo, hostId, questId, optionKeys, optionVals):
        self.cell.completeQuestByClientNpc(npcID, npcNo, hostId, questId, optionKeys, optionVals)

    def onCompleteQuestByClientNpc(self, npcID, questId):
        clientNpc = BigWorld.entities.get(npcID)
        if clientNpc:
            clientNpc.onCompleteQuest(questId)

    def triggerNpcChat(self, npcId, chatId):
        chatClues = QCRD.data.get(const.CHAR_STORY_CON_NPC_CHAT, {}).get('clues', [])
        for cid in chatClues:
            if not QCD.data.has_key(cid):
                continue
            cond = QCD.data[cid].get('condition')
            if not cond or cond({'npcId': npcId,
             'chatId': chatId}):
                self.cell.triggerCharsConditionByClient(const.CHAR_STORY_CON_NPC_CHAT, ('npcId', 'chatId'), (str(npcId), str(chatId)))
                break

    def enterClientTransportPot(self, cid):
        if cid not in self.clientTransportList:
            self.clientTransportList.append(cid)
        if self.clientTransportList:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ENTRY_POT)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ENTRY_POT, {'click': self.onOpenClientTransportPmg})

    def leaveClientTransportPot(self, cid):
        if cid in self.clientTransportList:
            self.clientTransportList.remove(cid)
        if not self.clientTransportList:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTRY_POT)

    def clearClientTransportPot(self):
        if self.clientTransportList:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTRY_POT)
        if getattr(self, 'clientTransportMsgBoxId', None) and self.clientTransportMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.clientTransportMsgBoxId)
        self.clientTransportList = []

    def onOpenClientTransportPmg(self):
        if not self.inWorld:
            return
        elif not self.clientTransportList:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTRY_POT)
            return
        else:
            cid = self.clientTransportList[0]
            cbpd = CBPD.data.get(cid)
            if not cbpd:
                return
            elif cid not in self.buildingProxy.cProxies or not self.buildingProxy.cProxies[cid].bindEntity or not self.buildingProxy.cProxies[cid].bindEntity.trapConditionCheck():
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTRY_POT)
                return
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_IMPARENA_582, Functor(self.triggerClientTransportPmg, cid, self.buildingProxy.cProxies[cid].bindEntity.id), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
            transportType = cbpd.get('transportType', None)
            if transportType == gametypes.CLIENT_TRANSPORT_FUBEN:
                msg = gameStrings.TEXT_IMPPLAYERNPC_240
                title = gameStrings.TEXT_IMPPLAYERNPC_241
            elif transportType == gametypes.CLIENT_TRANSPORT_MULTILINE:
                msg = gameStrings.TEXT_IMPPLAYERNPC_243
                title = gameStrings.TEXT_IMPPLAYERNPC_244
            if getattr(self, 'clientTransportMsgBoxId', None) and self.clientTransportMsgBoxId:
                gameglobal.rds.ui.messageBox.dismiss(self.clientTransportMsgBoxId)
            self.clientTransportMsgBoxId = gameglobal.rds.ui.messageBox.show(False, title, msg, buttons)
            return

    def triggerClientTransportPmg(self, cid, centId):
        if not self.inWorld:
            return
        else:
            if getattr(self, 'clientTransportMsgBoxId', None) and self.clientTransportMsgBoxId:
                gameglobal.rds.ui.messageBox.dismiss(self.clientTransportMsgBoxId)
            BigWorld.player().cell.clientTransportTrigger(cid, centId)
            return
