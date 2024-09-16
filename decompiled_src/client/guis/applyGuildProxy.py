#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/applyGuildProxy.o
import BigWorld
from Scaleform import GfxValue
from ui import unicode2gbk
import gameglobal
import gametypes
import uiConst
import const
import uiUtils
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import zhanQiMorpherFactory
from data import guild_config_data as GCD

class ApplyGuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ApplyGuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'autoApply': self.onAutoApply,
         'confirm': self.onConfirm,
         'initData': self.onInitData,
         'changeState': self.onChangeState,
         'prevPage': self.onPrevPage,
         'nextPage': self.onNextPage,
         'setSort': self.onSetSort,
         'checkGuildItem': self.onCheckGuildItem,
         'searchGuild': self.onSearchGuild}
        self.mediator = None
        self.page = None
        self.totalPages = None
        self.data = None
        self.state = gametypes.GUILD_STATE_ACTIVE
        self.npcId = 0
        self.sortType = gametypes.GUILD_ORDER_BY_LEVEL
        self.reverse = True
        self.flagGen = None
        self.flagDict = {}
        self.selectGuildNUID = 0
        self.dbID2nuid = {}
        self.qName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_APPLY_GUILD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_APPLY_GUILD:
            self.mediator = mediator
            self.initFlagGen()
            self.takePhoto3D()

    def show(self, state, totalPages, page, data, sortBy, reverse):
        self.state = state
        self.page = page
        self.totalPages = totalPages
        self.data = data
        self.sortType = sortBy
        self.reverse = reverse
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_APPLY_GUILD)

    def hideByNpcId(self, npcId):
        if self.npcId == npcId:
            self.hide()

    def clearWidget(self):
        self.mediator = None
        self.npcId = 0
        self.qName = ''
        self.resetFlagGen()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_APPLY_GUILD)

    def getGuildData(self, npcId):
        self.npcId = npcId
        self.queryGuildList(gametypes.GUILD_STATE_ACTIVE, self.qName, 1, gametypes.GUILD_ORDER_BY_LEVEL, True)

    def queryGuildList(self, state, qname, page, sortBy, reverse):
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            npc.cell.queryGuildList(state, qname, page, sortBy, reverse)
        elif self.npcId == 0:
            BigWorld.player().base.queryGuildList(state, qname, page, sortBy, reverse)

    def reset(self):
        self.page = None
        self.totalPages = None
        self.data = None
        self.state = gametypes.GUILD_STATE_ACTIVE
        self.npcId = 0
        self.sortType = gametypes.GUILD_ORDER_BY_LEVEL
        self.reverse = True
        self.flagGen = None
        self.flagDict = {}
        self.selectGuildNUID = 0

    def onAutoApply(self, *arg):
        BigWorld.player().cell.autoGuildJoin()

    def onConfirm(self, *arg):
        BigWorld.player().cell.applyGuildJoin(self.dbID2nuid[int(arg[3][0].GetString())])
        self.hide()

    def onChangeState(self, *arg):
        self.state = int(arg[3][0].GetString())
        self.qName = ''
        self.queryGuildList(int(arg[3][0].GetString()), self.qName, 1, gametypes.GUILD_ORDER_BY_LEVEL, True)

    def onInitData(self, *arg):
        if self.mediator:
            info = {}
            info['guildstate'] = self.state
            info['totalPages'] = self.totalPages
            info['page'] = self.page
            info['guildArray'] = self.data
            info['vitalityTip'] = GCD.data.get('vitalityTip', '')
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.mediator.Invoke('setSort', (GfxValue(self.sortType), GfxValue(self.reverse)))

    def onPrevPage(self, *arg):
        if self.page and self.page > 1:
            self.queryGuildList(self.state, self.qName, self.page - 1, self.sortType, self.reverse)

    def onNextPage(self, *arg):
        if self.page and self.page < self.totalPages:
            self.queryGuildList(self.state, self.qName, self.page + 1, self.sortType, self.reverse)

    def onSetSort(self, *arg):
        if self.sortType == int(arg[3][0].GetString()) and self.reverse == arg[3][1].GetBool():
            return
        sortType = int(arg[3][0].GetString())
        reverse = arg[3][1].GetBool()
        self.queryGuildList(self.state, self.qName, self.page, sortType, reverse)

    def refreshInfo(self, state, totalPages, page, data, sortBy, reverse):
        if self.mediator:
            self.selectGuildNUID = 0
            self.state = state
            self.page = page
            self.totalPages = totalPages
            self.data = data
            self.sortType = sortBy
            self.reverse = reverse
            info = {}
            info['guildstate'] = self.state
            info['totalPages'] = self.totalPages
            info['page'] = self.page
            info['guildArray'] = self.data
            info['vitalityTip'] = GCD.data.get('vitalityTip', '')
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.mediator.Invoke('setSort', (GfxValue(self.sortType), GfxValue(self.reverse)))

    def onCheckGuildItem(self, *arg):
        guildNUID = self.dbID2nuid.get(int(arg[3][0].GetNumber()))
        self.selectGuildNUID = guildNUID
        if guildNUID not in self.flagDict:
            self.flagDict[guildNUID] = str({zhanQiMorpherFactory.FLAG_HUIJI_SIZE: 2})
            BigWorld.player().cell.queryGuildFlag(guildNUID)
        self.refreshFlag(guildNUID)

    def updateFlag(self, guildNUID, newMorpher):
        p = BigWorld.player()
        self.flagDict[guildNUID] = newMorpher
        config = eval(newMorpher)
        guildIcon = config.get(2, '')
        if uiUtils.isDownloadImage(guildIcon):
            path = const.IMAGES_DOWNLOAD_DIR.replace('\\', '/')
            icon = '%s/%s.dds' % (path, guildIcon)
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, gametypes.NOS_FILE_PICTURE, self.guildIconDownloadNOSFile, (guildNUID,))
        self.refreshFlag(guildNUID)

    def guildIconDownloadNOSFile(self, status, callbackArgs):
        guildNUID = callbackArgs
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.refreshFlag(guildNUID)

    def refreshFlag(self, guildNUID):
        if guildNUID != self.selectGuildNUID:
            return
        model = self.flagGen.adaptor.attachment
        config = self.flagDict[self.selectGuildNUID]
        if model:
            dyeMorpher = zhanQiMorpherFactory.ZhanqiDyeMorpher(model, gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL)
            dyeMorpher.read(config)
            dyeMorpher.apply()

    def takePhoto3D(self, modelId = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL, tintMs = None):
        if not self.flagGen:
            self.flagGen = capturePhoto.ApplyGuildZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.flagGen.startCapture(modelId, tintMs, ('1101',))

    def resetFlagGen(self):
        if self.flagGen:
            self.flagGen.endCapture()

    def initFlagGen(self):
        if not self.flagGen:
            self.flagGen = capturePhoto.ApplyGuildZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.flagGen.initFlashMesh()

    def onSearchGuild(self, *arg):
        qName = unicode2gbk(arg[3][0].GetString())
        page = self.page if qName == self.qName else 1
        self.qName = qName
        self.queryGuildList(self.state, qName, page, self.sortType, self.reverse)
