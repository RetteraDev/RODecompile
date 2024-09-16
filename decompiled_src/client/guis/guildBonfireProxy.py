#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBonfireProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import utils
import const
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import ui
from guis import uiUtils
from sfx import sfx
from data import guild_config_data as GCD
from data import game_msg_data as GMD
from data import npc_data as ND
from cdata import game_msg_def_data as GMDD
GUILD_PUZZLE_MAX_CNT = 5
TORCH_MAX_CNT = 10
BONFIRE_ACTIVITY_ID = 6

class GuildBonfireProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBonfireProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()
        self.bonfireEntityId = 0
        self.torchEntityIds = []

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_BONFIRE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.timerFun()
            self.addTimer()
            self.addEntities()

    def addTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self.timer = BigWorld.callback(1, self.timerFun)

    def delTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def timerFun(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if not getattr(p, 'guild', None):
                self.hide()
                return
            endTime = p.guild.bonfire.endTime
            now = utils.getNow()
            left = max(0, endTime - now)
            self.widget.txtLeftTime.text = gameStrings.TEXT_GUILDBONFIREPROXY_67 % (left / 60, left % 60)
            self.timer = BigWorld.callback(1, self.timerFun)
            return

    def clearWidget(self):
        self.delEntities()
        self.delTimer()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_BONFIRE)
        self.delPushMsg()

    def show(self):
        self.delPushMsg()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_BONFIRE)

    def initUI(self):
        self.widget.txtTitile.text = gameStrings.GUILD_BONFIRE_TXT_TITLE

    @ui.callInCD(0.5)
    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.txtProgress.text = '%d/%d' % (p.guild.getPuzzleRoundNum(), GCD.data.get(BONFIRE_ACTIVITY_ID, {}).get('roundNum', GUILD_PUZZLE_MAX_CNT))
        self.widget.txtCnt.text = str(p.getGuildMemberCnt()) + gameStrings.GUILD_BONFIRE_TXT_AVATAR_CNT
        self.widget.txtPercent.text = '%d%%' % (self.getExp() * 100)

    def getExp(self):
        p = BigWorld.player()
        if not getattr(p, 'guild', None):
            return
        else:
            num = len([ isLight for isLight in p.guild.bonfire.torch if isLight ])
            exp = 1 + num * GCD.data.get('bonfireExpCoef', 0.1)
            return exp

    def _onBtnLightClick(self, *args):
        p = BigWorld.player()
        if not getattr(p, 'guild', None):
            return
        else:
            endTime = p.guild.bonfire.endTime
            now = utils.getNow()
            left = max(0, endTime - now)
            if left <= 0:
                return
            for i in xrange(const.GUILD_TORCH_NUM):
                if not p.guild.bonfire.torch.get(i + 1, False):
                    tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
                    if tianbi < GCD.data.get('bonfireCoin', 20):
                        p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
                        return
                    self.lightBonfire(i + 1)
                    return

            p.showGameMsg(GMDD.data.LIGHT_BONFIRE_CNT_MAX, ())
            return

    @ui.checkInventoryLock()
    def lightBonfire(self, torchIdx):
        p = BigWorld.player()
        if not p.guild.bonfire.torch.get(torchIdx, False):
            tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
            if tianbi < GCD.data.get('bonfireCoin', 20):
                p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
                return
            text = GMD.data.get(GMDD.data.LIGHT_BONFIRE_CONFIRM, {}).get('text', '%d') % GCD.data.get('bonfireCoin', 20)
            self.uiAdapter.messageBox.showYesNoMsgBox(text, Functor(p.cell.lightGuildTorch, torchIdx, p.cipherOfPerson))
            return
        p.showGameMsg(GMDD.data.GUILD_TORCH_ALREAD_ON, ())

    def lightBonfireSucc(self, idx):
        if idx - 1 < len(self.torchEntityIds):
            entityId = self.torchEntityIds[idx - 1]
            if not entityId or not BigWorld.entities.get(entityId, None):
                return
            entity = BigWorld.entities.get(entityId, None)
            if not entity:
                return
            p = BigWorld.player()
            if entity.model:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
                 p.getEquipEffectPriority(),
                 entity.model,
                 GCD.data.get('bonfireTorchEffect', 1001),
                 sfx.EFFECT_LIMIT_MISC))
            titleName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % p.guild.bonfire.torch[idx]
            entity.titleName = titleName
            if getattr(entity, 'topLogo', None):
                entity.topLogo.titleName = titleName
                entity.topLogo.setTitleName(titleName)

    def createClientNpc(self, pos, npcId, torchIdx = -1):
        param = {'roleName': '',
         'petName': '',
         'showLogo': False,
         'npcId': npcId}
        spaceID = BigWorld.player().spaceID
        entityID = BigWorld.createEntity('Npc', spaceID, 0, pos, (0, 0, 0), param)
        BigWorld.entities[entityID].torchIdx = torchIdx
        BigWorld.entities[entityID].roleName = ND.data.get(npcId, {}).get('name', '')
        return entityID

    def addEntities(self):
        bonfireData = GCD.data.get('bonfireNpcIds', {}).get('bonfire', ())
        torchDatas = GCD.data.get('bonfireNpcIds', {}).get('torch', ())
        if not bonfireData or not torchDatas:
            return
        self.bonfireEntityId = self.createClientNpc(bonfireData[1], bonfireData[0])
        for i in xrange(TORCH_MAX_CNT):
            if i >= len(torchDatas):
                break
            torchEntityId = self.createClientNpc(torchDatas[i][1], torchDatas[i][0], i + 1)
            self.torchEntityIds.append(torchEntityId)

    def delEntities(self):
        if self.bonfireEntityId:
            BigWorld.destroyEntity(self.bonfireEntityId)
        for entityId in self.torchEntityIds:
            if entityId:
                BigWorld.destroyEntity(entityId)

        self.torchEntityIds = []

    def onGotoGuild(self, *args):
        p = BigWorld.player()
        if not p.inGuildSpace():
            if p.guildMemberSkills.has_key(uiConst.GUILD_SKILL_DZG):
                self.uiAdapter.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG)
            else:
                seekId = GCD.data.get('guildRobberSeekId', ())
                uiUtils.findPosById(seekId)

    def addPushMsg(self):
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_BONFIRE)
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_BONFIRE, {'click': self.onGotoGuild})

    def delPushMsg(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_BONFIRE)
