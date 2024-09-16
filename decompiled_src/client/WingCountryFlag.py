#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingCountryFlag.o
import BigWorld
import gameglobal
import const
import gametypes
import gamelog
import iNpc
from guis import zhanQiMorpherFactory
from guis import uiUtils
from data import wing_world_config_data as WWCD

class WingCountryFlag(iNpc.INpc):

    def __init__(self):
        super(WingCountryFlag, self).__init__()
        self.isEnterTopLogoRange = False
        self.firstFetchFinished = False
        self.isLeaveWorld = False

    def afterModelFinish(self):
        super(WingCountryFlag, self).afterModelFinish()
        if self.isEnterTopLogoRange:
            self.enterTopLogoRange()
        self.updateMorpher()

    def updateMorpher(self):
        gamelog.debug('@yj updateMorpher', self.flagId)
        player = BigWorld.player()
        fileKey = 0
        try:
            self.morpher = str({0: 0,
             1: 0,
             2: self.flagId,
             3: 0,
             4: 0,
             5: 0,
             6: 1.3,
             7: (0.0, 0.0)})
            morpher = eval(self.morpher)
            fileKey = morpher.get(zhanQiMorpherFactory.FLAG_HUIJI_TEXTURE, 0)
        except:
            fileKey = 0

        if uiUtils.isDownloadImage(fileKey):
            player.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, fileKey, gametypes.NOS_FILE_PICTURE, self.onDownloadAdvertise, ())
        else:
            self.useMorpher()

    def onDownloadAdvertise(self, status):
        gamelog.debug('@yj onDownloadAdvertise', self.id, status)
        if not self.inWorld:
            return
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.useMorpher()

    def useMorpher(self):
        dyeMorpher = zhanQiMorpherFactory.ZhanqiDyeMorpher(self.model, WWCD.data.get('clanWingWorldFlagDefaultModel', gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL))
        dyeMorpher.read(self.morpher)
        dyeMorpher.apply()

    def enterWorld(self):
        super(WingCountryFlag, self).enterWorld()

    def leaveWorld(self):
        super(WingCountryFlag, self).leaveWorld()
        self.isLeaveWorld = True

    def enterTopLogoRange(self, rangeDist = -1):
        self.isEnterTopLogoRange = True
        if not self.firstFetchFinished:
            return
        super(WingCountryFlag, self).enterTopLogoRange()

    def leaveTopLogoRange(self, rangeDist = -1):
        self.isEnterTopLogoRange = False
        super(WingCountryFlag, self).leaveTopLogoRange(rangeDist)

    def getItemData(self):
        return {'model': WWCD.data.get('clanWingWorldFlagDefaultModel', gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL),
         'dye': 'Default'}

    def getModelScale(self):
        scale = WWCD.data.get('clanWingWorldFlagModelScale', 10)
        return (scale, scale, scale)

    def showTargetUnitFrame(self):
        return False
