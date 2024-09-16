#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/roleDebugProxy.o
import random
import Math
import BigWorld
import ResMgr
from Scaleform import GfxValue
import gameglobal
import gamelog
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst

class RoleDebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(RoleDebugProxy, self).__init__(uiAdapter)
        self.bindType = 'roleDebug'
        self.modelMap = {'ClickRole': self.onClickRole,
         'DetachRole': self.onDetachRole}
        self.RoleList = []
        self.role = None
        self.entityList = []

    def scanRoleFile(self):
        for id in xrange(10001, 10011):
            folderSection = ResMgr.openSection(gameglobal.charRes + str(id))
            if folderSection:
                for i in folderSection.keys():
                    if i.endswith('.model'):
                        self.RoleList.append(gameglobal.charRes + str(id) + '/' + i)

    def getRoleArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.RoleList:
            self.scanRoleFile()
        for item in self.RoleList:
            value = GfxValue(gbk2unicode(self.RoleList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getValue(self, key):
        if key == 'roleDebug.roleList':
            ar = self.getRoleArray()
            return ar

    def onClickRole(self, *arg):
        roleName = arg[3][0].GetString()
        gamelog.debug('roleDebug', roleName)
        if not self.role:
            self.role = BigWorld.player()
        gameglobal.rds.offlinemodel = roleName
        offset = Math.Vector3(random.randint(-4, 4), 0, random.randint(-4, 4))
        eId = BigWorld.createEntity('Avatar', self.role.spaceID, 0, self.role.position + offset, (0, 0, 0), {'name': '»√∏Á≥Ú≥Ú'})
        e = BigWorld.entity(eId)
        e.fashion.loadSinglePartModel(roleName)
        e.setTargetCapsUse(True)
        self.entityList.append(eId)

    def onDetachRole(self, *arg):
        for i in self.entityList:
            BigWorld.destroyEntity(i)

    def showRoleDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_ROLE)))
