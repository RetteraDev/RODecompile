#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impShareCharConf.o
import BigWorld
import gameglobal
from callbackHelper import Functor

class ImpShareCharConf(object):

    def syncSharedCnt(self, sharedCnt):
        self.sharedCnt = sharedCnt

    def onUploadCharCfgData(self, nuid):
        gameglobal.rds.ui.characterDetailAdjust.showShare(nuid)

    def uploadCharacter(self, entId):
        fun = Functor(self.realUploadPhoto, entId)
        gameglobal.rds.ui.characterDetailAdjust.onClickUploadCharacter(fun)

    def realUploadPhoto(self, entId, noskeys):
        ent = BigWorld.entity(entId)
        if noskeys and ent:
            ent.cell.uploadCharCfgData(self.roleName, self.physique.sex, self.physique.bodyType, noskeys, self.realAvatarConfig)
