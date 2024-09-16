#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/littlemap.o
import C_ui
import BigWorld
import uiConst

class LittleMap(object):
    INCOMBAT_DELTA = 0.3
    NOINCOMBAT_DELTA = 0.1

    def addEntity(self, matrix, userData, type):
        C_ui.littlemap_addEntity(matrix, userData, type)

    def delEntity(self, userData):
        C_ui.littlemap_delEntity(userData)

    def delEntitiesOfType(self, type):
        C_ui.littlemap_delEntitiesOfType(type)

    def onLittleMapEnter(self, entity):
        p = BigWorld.player()
        if entity.__class__.__name__ == 'Avatar':
            if entity.isInTeamOrGroup() and p.groupNUID == entity.groupNUID:
                self.onEnter(uiConst.ICON_TYPE_TEAMATE, entity)
            else:
                self.delEntity(entity.id)

    def onLittleMapLeave(self, en):
        self.delEntity(en.id)

    def onEnter(self, etype, en):
        self.addEntity(en.matrix, en.id, etype)

    def resetDeltaTime(self):
        if hasattr(C_ui, 'littlemap_setDeltaTime'):
            p = BigWorld.player()
            delta = 0.1
            if p.inCombat:
                delta = LittleMap.INCOMBAT_DELTA
            else:
                delta = LittleMap.NOINCOMBAT_DELTA
            C_ui.littlemap_setDeltaTime(delta)
