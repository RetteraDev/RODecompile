#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Snare.o
import BigWorld
import gameglobal
import const
import gametypes
import clientcom
import utils
from sfx import sfx
from iNpc import INpc
from iDisplay import IDisplay
from data import monster_model_client_data as NMMD

class Snare(INpc, IDisplay):

    def __init__(self):
        super(Snare, self).__init__()
        self.effects = []
        self.noSelected = True

    def getItemData(self):
        md = NMMD.data.get(self.typeID, {})
        if not md:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        return md

    def needBlackShadow(self):
        md = NMMD.data.get(self.typeID, {})
        noBlackUfo = md.get('noBlackUfo', False)
        return not noBlackUfo

    def afterModelFinish(self):
        super(Snare, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.initYaw = self.yaw
        if self.visibility == const.VISIBILITY_HIDE:
            self.model.visible = False
        else:
            self.model.visible = True
        md = NMMD.data.get(self.typeID, None)
        effect = md.get('effects', None)
        fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         effect,
         sfx.EFFECT_UNLIMIT))
        if fx:
            self.addFx(effect, fx)
        self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)

    def getTopLogoHeight(self):
        return self.getItemData().get('heightOffset', super(Snare, self).getTopLogoHeight())

    def showScopeViewDebug(self, viewType, args):
        if BigWorld.isPublishedVersion():
            return
        if args:
            shapeType = args[0]
            if shapeType == gametypes.CALC_SCOPCE_TYPE_SPHERE:
                centerPos = args[1]
                radii = args[2]
                delay = args[3] if len(args) >= 4 else 0.3
                color = args[4] if len(args) >= 5 else None
                clientcom.drawCylinderDebug(centerPos, radii, radii, radii, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CYLINDER:
                centerPos = args[1]
                radii = args[2]
                height = args[3]
                depth = args[4]
                delay = args[5] if len(args) >= 6 else 0.3
                color = args[6] if len(args) >= 7 else None
                clientcom.drawCylinderDebug(centerPos, radii, height, depth, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CUBE:
                srcPosition = args[1]
                centerPos = args[2]
                width = args[3]
                depth = args[4]
                height = args[5]
                yaw = args[6]
                delay = args[7] if len(args) >= 8 else 0.5
                color = args[8] if len(args) >= 9 else None
                if not centerPos:
                    centerPos = srcPosition
                clientcom.drawCubeViewDebug(centerPos, width, depth, height, yaw, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RADIAN:
                srcPosition = args[1]
                centerPos = args[2]
                radii = args[3]
                radian = args[4]
                height = args[5]
                yaw = args[6]
                delay = args[7] if len(args) >= 8 else 0.5
                color = args[8] if len(args) >= 9 else None
                if not centerPos:
                    centerPos = srcPosition
                clientcom.drawRadianDebug(centerPos, radii, radian, height, yaw, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RING:
                centerPos = args[1]
                innerRadius = args[2]
                outerRadius = args[3]
                height = args[4]
                delay = args[5] if len(args) >= 6 else 0.5
                innterColor = args[6] if len(args) >= 7 else (0, 0, 255, 0)
                outerColor = args[7] if len(args) >= 8 else None
                clientcom.drawRingDebug(centerPos, innerRadius, outerRadius, height, delay, innterColor, outerColor)
