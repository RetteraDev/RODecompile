#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/createGuildProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import uiUtils
import gamelog
import utils
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from helpers import capturePhoto
from callbackHelper import Functor
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class CreateGuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CreateGuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'close': self.onClose,
         'initData': self.onInitData,
         'showZhanQi': self.onShowZhanQi}
        self.mediator = None
        self.npcId = 0
        self.headGen = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CREATE_GUILD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CREATE_GUILD:
            self.mediator = mediator
            self.initHeadGen()
            self.takePhoto3D()
            return uiUtils.dict2GfxDict({'guildNameMaxChars': const.GUILD_NAME_MAX_LEN,
             'isEnVersion': utils.getGameLanuage() == 'en'})

    def show(self, npcId):
        p = BigWorld.player()
        if p.guild:
            p.showGameMsg(GMDD.data.GUILD_CREATE_ALREADY_JOINED, ())
            return
        self.npcId = npcId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CREATE_GUILD)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CREATE_GUILD)

    def reset(self):
        self.npcId = 0
        self.resetHeadGen()
        self.headGen = None
        if gameglobal.rds.ui.zhanQi.mediator:
            gameglobal.rds.ui.zhanQi.hide()

    def hideByNpcId(self, npcId):
        if self.npcId == npcId:
            self.hide()

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        name = unicode2gbk(arg[3][0].GetString())
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            p.showGameMsg(GMDD.data.GUILD_NAME_TABOO, ())
            return
        menifest = unicode2gbk(arg[3][1].GetString())
        result, menifest = taboo.checkDisbWord(menifest)
        if not result:
            p.showGameMsg(GMDD.data.GUILD_MENIFEST_TABOO, ())
            return
        result, menifest = taboo.checkBWorld(menifest)
        if not result:
            p.showGameMsg(GMDD.data.GUILD_MENIFEST_TABOO, ())
            return
        nameLength = int(arg[3][2].GetString())
        if nameLength < const.GUILD_NAME_MIN_LEN / 2:
            p.showGameMsg(GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN / 2, const.GUILD_NAME_MAX_LEN / 2))
            return
        clanWarFlagMorpher = gameglobal.rds.ui.zhanQi.morpherFactory.export()
        clanWarFlagMorpherDict = eval(clanWarFlagMorpher)
        try:
            flag = uiUtils.genGuildFlag(clanWarFlagMorpherDict[2], clanWarFlagMorpherDict[5])
        except:
            gamelog.error('error in CreateGuildProxy#onConfirm!')
            return

        createFee = GCD.data.get('createFee', const.GUILD_CREATE_FEE)
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            if uiUtils.checkBindCashEnough(createFee, p.bindCash, p.cash, Functor(npc.cell.createGuild, name, menifest, clanWarFlagMorpher, flag)):
                npc.cell.createGuild(name, menifest, clanWarFlagMorpher, flag)
        elif self.npcId == 0:
            if uiUtils.checkBindCashEnough(createFee, p.bindCash, p.cash, Functor(p.cell.createGuild, name, menifest, clanWarFlagMorpher, flag)):
                p.cell.createGuild(name, menifest, clanWarFlagMorpher, flag)
        self.hide()

    def onInitData(self, *arg):
        return uiUtils.array2GfxAarry([GCD.data.get('createFee', const.GUILD_CREATE_FEE), uiConst.GUILD_FLAG_ICON_IMAGE_RES, uiConst.GUILD_FLAG_NUM], True)

    def getGuildFlagIconFile(self, id):
        return uiConst.GUILD_FLAG_ICON_IMAGE_RES + str(id) + '.dds'

    def onShowZhanQi(self, *arg):
        gameglobal.rds.ui.zhanQi.show()

    def updateFlag(self, flagId):
        pass

    def takePhoto3D(self, modelId = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL, tintMs = None, photoAction = None):
        if not self.headGen:
            self.headGen = capturePhoto.GuildZhanQiPhotoCreateGen.getInstance('gui/taskmask.tga', 422)
        self.headGen.startCapture(modelId, tintMs, ('1101',))

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.GuildZhanQiPhotoCreateGen.getInstance('gui/taskmask.tga', 422)
        self.headGen.initFlashMesh()
