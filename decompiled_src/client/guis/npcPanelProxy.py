#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcPanelProxy.o
from gamestrings import gameStrings
import random
import BigWorld
from Scaleform import GfxValue
import gameglobal
import npcConst
import gamelog
import gametypes
import messageBoxProxy
from uiProxy import UIProxy
from guis import uiConst
from ui import gbk2unicode
from helpers import capturePhoto
from uiUtils import getNpcName
from guis import uiUtils
from guis import ui
from gamestrings import gameStrings
from data import dialogs_data as DD
from data import npc_func_data as NFD
from data import npc_data as ND
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import teleport_data as TD
from callbackHelper import Functor

class NpcPanelProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcPanelProxy, self).__init__(uiAdapter)
        self.modelMap = {'getType': self.onGetType,
         'getTitle': self.onGetTitle,
         'getContent': self.onGetContent,
         'getButton': self.onGetButton,
         'closePanel': self.onClosePanel,
         'clickFuncBtn': self.onClickFuncBtn,
         'gotoMain': self.onGotoMain,
         'leftPanel': self.onLeftPanel,
         'getNpcName': self.onGetNpcName,
         'getTowerDefenseInfo': self.onGetTowerDefenseInfo,
         'registerNpcTDPanel': self.onRegisterNpcTDPanel,
         'npcTDClick': self.onNpcTDClick,
         'clickClose': self.onClickClose,
         'getTeleportInfo': self.onGetTeleportInfo,
         'clickTeleport': self.onClickTeleport,
         'chooseDifficulty': self.onChooseDifficulty}
        self.inFullScreen = False
        self.towerDenfenseNpc = None
        self.tdNpcId = None
        self.btnId = None
        self.npcId = None
        self.headGen = None
        self.teleportList = []
        self.shishenAimMode = 0

    def showTDNpc(self, npcId, tdNpcId = 10001):
        self.tdNpcId = tdNpcId
        self.npcId = npcId
        self.uiAdapter.openQuestWindow(uiConst.NPC_TOWER)

    def onClickClose(self, *arg):
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()

    def onGetNpcName(self, *arg):
        p = BigWorld.player()
        entity = p.targetLocked
        if entity:
            gameglobal.rds.ui.quest.takePhoto3D(entity.npcId)
            return GfxValue(gbk2unicode(entity.roleName))

    def _getFNADInfo(self):
        return NFD.data.get(self.tdNpcId, [])

    def onGetTowerDefenseInfo(self, *arg):
        if not self.tdNpcId:
            return
        npc = BigWorld.entities.get(self.npcId)
        if not npc:
            return
        self.initHeadGen(npc)
        npcData = ND.data.get(npc.npcId, {})
        self.TDinfo = self._getFNADInfo()
        ret = self.movie.CreateObject()
        chat = npcData.get('Uichat', [])
        if len(chat) > 0:
            chat = DD.data.get(chat[0], {}).get('details', '')
        else:
            chat = ''
        ret.SetMember('chat', GfxValue(gbk2unicode(chat)))
        ret.SetMember('roleName', GfxValue(gbk2unicode(getNpcName(npc.npcId))))
        title = npcData.get('title', gameStrings.NPC_DEFAULT_TITLE)
        ret.SetMember('title', GfxValue(gbk2unicode(title)))
        ret.SetMember('icon', GfxValue(''))
        opt = self.movie.CreateArray()
        arrow = []
        for index, value in enumerate(self.TDinfo):
            text = value.get('text', '')
            val = value.get('itemNum', '')
            opt.SetElement(index, GfxValue(gbk2unicode(text + str(val))))
            arrow.append(value.get('arrow', 0))

        ret.SetMember('debateOptions', opt)
        ret.SetMember('arrow', uiUtils.array2GfxAarry(arrow))
        return ret

    def onGetTowerDefenseInfoPy(self):
        if not self.tdNpcId:
            return
        npc = BigWorld.entities.get(self.npcId)
        if not npc:
            return
        npcData = ND.data.get(npc.npcId, {})
        self.TDinfo = self._getFNADInfo()
        ret = {}
        chat = npcData.get('Uichat', [])
        if len(chat) > 0:
            chat = DD.data.get(chat[0], {}).get('details', '')
        else:
            chat = ''
        ret['chat'] = chat
        ret['roleName'] = getNpcName(npc.npcId)
        title = npcData.get('title', gameStrings.NPC_DEFAULT_TITLE)
        ret['title'] = title
        ret['icon'] = ''
        ret['npcId'] = self.npcId
        opt = []
        arrow = []
        for index, value in enumerate(self.TDinfo):
            text = value.get('text', '')
            val = value.get('itemNum', '')
            opt.append(text + str(val))
            arrow.append(value.get('arrow', 0))

        ret['debateOptions'] = opt
        ret['arrow'] = arrow
        return ret

    def onRegisterNpcTDPanel(self, *arg):
        self.towerDenfenseNpc = arg[3][0]

    def onNpcTDClick(self, *arg):
        index = int(arg[3][0].GetString())
        self.npcTDClick(index)

    @ui.callFilter(2, True)
    def npcTDClick(self, index):
        gamelog.debug('hjx debug onNpcTDClick:', index, self.TDinfo[index]['id'])
        npc = BigWorld.entities.get(self.npcId)
        if npc is not None:
            cType = self.TDinfo[index].get('cType', gametypes.NPC_OP_TYPE_DEFAULT)
            if cType == gametypes.NPC_OP_TYPE_DEFAULT:
                self.executeFbAI(npc, index, self.TDinfo[index]['id'], uiConst.TRAINING_FUBEN_TYPE_OLD)
            elif cType == gametypes.NPC_OP_TYPE_UNBIND_FRIENDSHIP_WITH_SINGLE:
                npc.cell.unbindFriendshipWithSingle()
            elif cType == gametypes.NPC_OP_TYPE_UNBIND_FRIENDSHIP_WITH_DOUBLE:
                npc.cell.unbindFriendshipWithDouble()
            elif cType == gametypes.NPC_OP_TYPE_BIND_FRIENDSHIP:
                style = self.TDinfo[index].get('arg', 0)
                if style:
                    npc.cell.bindFriendship(style)
        if gameglobal.rds.ui.quest.isShow:
            self.hideNpcFullScreen()
        if gameglobal.rds.ui.npcV2.isShow:
            self.uiAdapter.npcV2.leaveStage()

    def executeFbAI(self, npc, index, aiId, aiType):
        player = BigWorld.player()
        if not player:
            return
        elif not player.inWorld:
            return
        else:
            needHeader = self.TDinfo[index].get('needHeader', False)
            if needHeader:
                if player.groupHeader == player.id:
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(npc.cell.executeFbAI, aiId, aiType), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
                    msg = uiUtils.getTextFromGMD(self.TDinfo[index].get('confirmMsgId', 0), gameStrings.TEXT_NPCPANELPROXY_196)
                    gameglobal.rds.ui.messageBox.show(False, '', msg, buttons)
                else:
                    player.showGameMsg(GMDD.data.QUEST_ACCEPT_HEADER_FAIL, ())
            else:
                npc.cell.executeFbAI(self.TDinfo[index]['id'], uiConst.TRAINING_FUBEN_TYPE_OLD)
            return

    def onGetType(self, *arg):
        gamelog.debug('getType')
        return GfxValue('type.png')

    def onGotoMain(self, *arg):
        gamelog.debug('onGotoMain')

    def onLeftPanel(self, *arg):
        gamelog.debug('onLeftPanel')
        self.hideNpcFullScreen()

    def setNPCInfo(self, npcId, options, defaultChatId):
        ent = BigWorld.entities.get(npcId)
        self.name = ent.roleName
        if defaultChatId:
            self.chat = DD.data.get(random.choice(defaultChatId), {}).get('details', '')
        else:
            self.chat = ''
        self.options = options

    def onGetTitle(self, *arg):
        gamelog.debug('getTitle')
        return GfxValue(gbk2unicode(self.name))

    def onGetContent(self, *arg):
        gamelog.debug('getContent')
        self.chat = self.chat.replace('$P', BigWorld.player().realRoleName)
        return GfxValue(gbk2unicode(self.chat))

    def onClickFuncBtn(self, *arg):
        self.btnId = int(arg[3][0].GetNumber())
        gamelog.debug('onClickFuncBtn', self.btnId)
        type = self.options.items()[self.btnId][0][0]
        list = self.options.items()[self.btnId][1]
        if type == npcConst.NPC_FUNC_TELEPORT:
            gameglobal.rds.ui.fuben.setFuncList(gameStrings.TEXT_NPCPANELPROXY_238, list)
            gameglobal.rds.ui.fuben.showFubenApply(self.npcId)
        elif type == npcConst.NPC_FUNC_SHOP:
            BigWorld.entities.get(self.npcId).cell.openShop(list[0])
        elif type == npcConst.NPC_FUNC_FASHION_TRANSFER:
            gameglobal.rds.ui.fashionPropTransfer.show()
            gameglobal.rds.ui.inventory.show()
        elif type == npcConst.NPC_FUNC_RUBBING:
            gameglobal.rds.ui.equipCopy.show(self.npcId)
            gameglobal.rds.ui.inventory.show()
        elif type == npcConst.NPC_FUNC_BIRDLET:
            if gameglobal.rds.ui.birdLetHotLine.mediator:
                gameglobal.rds.ui.birdLetHotLine.hide()
        elif type == npcConst.NPC_FUNC_MIX_EQUIP:
            gameglobal.rds.ui.equipMix.show(self.npcId)
            gameglobal.rds.ui.inventory.show()
        elif type == npcConst.NPC_FUNC_MIX_EQUIP_NEW:
            gameglobal.rds.ui.equipMixNew.show(self.npcId)
            gameglobal.rds.ui.inventory.show()
        elif type == npcConst.NPC_FUNC_UPGRADE_EQUIP:
            gameglobal.rds.ui.inventory.show()
        elif type == npcConst.NPC_FUNC_APPLY_PK_MODE:
            npcEnt = BigWorld.entity(self.npcId)
            if npcEnt:
                npcEnt.cell.applyPolicePkMode()
        elif type == npcConst.NPC_FUNC_APPLY_SHENG_SI_CHANG:
            npcEnt = BigWorld.entity(self.npcId)
            if npcEnt:
                npcEnt.cell.applyShengSiChang()
        elif type == npcConst.NPC_FUNC_SUMMON_PLANE_IN_FORT_BATTLE_FIELD:
            npcEnt = BigWorld.entity(self.npcId)
            if npcEnt:
                npcEnt.cell.summonPlaneInFortBattleField()
        elif type == npcConst.NPC_FUNC_ACTIVITY_RESET_CHAR:
            self.showResetCharConfirm(self.npcId, list[0])
        elif type == npcConst.NPC_FUNC_MAKE_MANUAL_EQUIP:
            gameglobal.rds.ui.manualEquip.show(self.npcId)
        elif type == npcConst.NPC_FUNC_GUANYIN_REPAIR:
            gameglobal.rds.ui.huiZhangRepair.show()
            gameglobal.rds.ui.inventory.show()

    def showResetCharConfirm(self, npcId, templateId):
        msg = SCD.data.get('resetCharConfirmMsg', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmReset, npcId, templateId))

    def onConfirmReset(self, npcId, templateId):
        npcEnt = BigWorld.entity(npcId)
        if npcEnt:
            npcEnt.cell.applyResetChar(templateId)

    def onGetButton(self, *arg):
        gamelog.debug('getButton')
        for item in self.options.items():
            type = item[0][0]
            list = item[1]
            if type == npcConst.NPC_FUNC_TELEPORT:
                gameglobal.rds.ui.fuben.setFuncList(gameStrings.TEXT_NPCPANELPROXY_238, list)
                gameglobal.rds.ui.fuben.showFubenApply(self.npcId)
                break

        btnObj = self.movie.CreateObject()
        label = self.movie.CreateArray()
        i = 0
        for key, item in self.options.items():
            btnName = key[1]
            gamelog.debug('onGetButton', btnName)
            label.SetElement(i, GfxValue(gbk2unicode('  ' + btnName + '   ')))
            i = i + 1

        btnObj.SetMember('cnt', GfxValue(i))
        btnObj.SetMember('label', label)
        return btnObj

    def onClosePanel(self, *arg):
        gamelog.debug('closePanel')

    def clearNpcPanel(self):
        if gameglobal.rds.ui.shop.show:
            gameglobal.rds.ui.shop.hide()
        if gameglobal.rds.ui.compositeShop.isOpen:
            gameglobal.rds.ui.compositeShop.closeShop()

    def showNpcFullScreen(self, entId):
        self.npcId = entId
        self.teleportList = []
        self.uiAdapter.openQuestWindow(uiConst.NPC_TELEPORT)

    def hideNpcFullScreen(self):
        self.uiAdapter.quest.onClickCloseBtn()

    def initHeadGen(self, npc):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        uiUtils.takePhoto3D(self.headGen, npc, npc.npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def getTeleportTitle(self):
        npc = BigWorld.entity(self.npcId)
        if npc and npc.inWorld:
            nd = ND.data.get(npc.npcId, {})
            functions = nd.get('functions', {})
            for funcName, func, funcId in functions:
                if func == npcConst.NPC_FUNC_TELEPORT:
                    return TD.data.get(funcId, {}).get('title', gameStrings.TEXT_NPCPANELPROXY_238)

        return gameStrings.TEXT_NPCPANELPROXY_238

    def onGetTeleportInfo(self, *arg):
        npc = BigWorld.entity(self.npcId)
        self.initHeadGen(npc)
        ret = self.movie.CreateObject()
        ret.SetMember('chat', GfxValue(gbk2unicode(self.chat)))
        ret.SetMember('roleName', GfxValue(gbk2unicode(self.name)))
        ret.SetMember('title', GfxValue(gbk2unicode(self.getTeleportTitle())))
        ret.SetMember('icon', GfxValue(''))
        opt = self.movie.CreateArray()
        for item in self.options.items():
            type = item[0][0]
            list = item[1]
            if type == npcConst.NPC_FUNC_TELEPORT:
                self.teleportList = list
                for i, it in enumerate(list):
                    opt.SetElement(i, GfxValue(gbk2unicode(it[0])))

                break

        ret.SetMember('option', opt)
        return ret

    def onGetTeleportInfoPy(self):
        ret = {}
        ret['chat'] = self.chat
        ret['roleName'] = self.name
        ret['title'] = self.getTeleportTitle()
        ret['icon'] = ''
        ret['npcId'] = self.npcId
        opt = []
        for item in self.options.items():
            type = item[0][0]
            list = item[1]
            if type == npcConst.NPC_FUNC_TELEPORT:
                self.teleportList = list
                for i, it in enumerate(list):
                    opt.append(it[0])

                break

        ret['option'] = opt
        return ret

    def onClickTeleport(self, *arg):
        idNum = int(arg[3][0].GetString())
        self.teloport(idNum)

    def teloport(self, idNum):
        if gameglobal.rds.ui.quest.isShow:
            self.hideNpcFullScreen()
        if gameglobal.rds.ui.npcV2.isShow:
            self.uiAdapter.npcV2.leaveStage()
        name, data, idx = self.teleportList[idNum]
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            npc.cell.npcTeleport(data, idx)

    def isYaoJingQiTanFuBen(self, id):
        if id in SCD.data.get('yaojingqitanFubenNo', ()):
            return True
        else:
            return False

    def onChooseDifficulty(self, *arg):
        mode = int(arg[3][0].GetNumber())
        self.chooseDifficulty(mode)

    def chooseDifficulty(self, mode):
        currentMode = gameglobal.rds.ui.currentShishenMode
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        self.shishenAimMode = mode
        p = BigWorld.player()
        if currentMode == 0:
            p.showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_124)
            return
        if currentMode == self.shishenAimMode:
            p.showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_127 % modeStr[self.shishenAimMode])
            return
        if currentMode > self.shishenAimMode:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FUBENDEGREEPROXY_130 % modeStr[self.shishenAimMode], Functor(self.comfirmSetShishenMode))
        else:
            p.showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_132)

    def comfirmSetShishenMode(self):
        if self.shishenAimMode == 0:
            return
        BigWorld.player().cell.setShishenMode(self.shishenAimMode)
