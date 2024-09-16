#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClanWarFlag.o
import BigWorld
import gameglobal
import const
import gametypes
import gamelog
import iNpc
from guis import zhanQiMorpherFactory
from guis import uiUtils
from data import wing_world_config_data as WWCD

class ClanWarFlag(iNpc.INpc):

    def __init__(self):
        super(ClanWarFlag, self).__init__()
        self.isEnterTopLogoRange = False
        self.firstFetchFinished = False
        self.isLeaveWorld = False

    def afterModelFinish(self):
        super(ClanWarFlag, self).afterModelFinish()
        if self.isEnterTopLogoRange:
            self.enterTopLogoRange()
        self.updateMorpher()

    def updateMorpher(self):
        player = BigWorld.player()
        fileKey = 0
        try:
            morpher = eval(self.morpher)
            fileKey = morpher.get(zhanQiMorpherFactory.FLAG_HUIJI_TEXTURE, 0)
        except:
            fileKey = 0

        if uiUtils.isDownloadImage(fileKey):
            if self.hostId:
                player.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, fileKey, self.hostId, gametypes.NOS_FILE_PICTURE, self.onDownloadAdvertise, ())
            else:
                player.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, fileKey, gametypes.NOS_FILE_PICTURE, self.onDownloadAdvertise, ())
        else:
            self.useMorpher()

    def onDownloadAdvertise(self, status):
        gamelog.debug('@clanWarFlag onDownloadAdvertise', self.id, status)
        if not self.inWorld:
            return
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.useMorpher()

    def useMorpher(self):
        p = BigWorld.player()
        if p.inWingCity():
            defaultModel = WWCD.data.get('wingWorldGuildFlagModel', gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL)
        else:
            defaultModel = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL
        dyeMorpher = zhanQiMorpherFactory.ZhanqiDyeMorpher(self.model, defaultModel)
        dyeMorpher.read(self.morpher)
        dyeMorpher.apply()

    def enterWorld(self):
        super(ClanWarFlag, self).enterWorld()

    def leaveWorld(self):
        super(ClanWarFlag, self).leaveWorld()
        self.isLeaveWorld = True

    def enterTopLogoRange(self, rangeDist = -1):
        self.isEnterTopLogoRange = True
        if not self.firstFetchFinished:
            return
        super(ClanWarFlag, self).enterTopLogoRange()

    def leaveTopLogoRange(self, rangeDist = -1):
        self.isEnterTopLogoRange = False
        super(ClanWarFlag, self).leaveTopLogoRange(rangeDist)

    def getItemData(self):
        p = BigWorld.player()
        if p.inWingCity():
            defaultModel = WWCD.data.get('wingWorldGuildFlagModel', gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL)
        else:
            defaultModel = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL
        return {'model': defaultModel,
         'modelScale': self.modelScale,
         'dye': 'Default'}

    def getModelScale(self):
        scale = self.modelScale
        return (scale, scale, scale)

    def showTargetUnitFrame(self):
        return False

    def set_morpher(self, oldVal):
        gamelog.debug('zt: set_morpher', oldVal, self.morpher)
        self.updateMorpher()
