#Embedded file name: I:/bag/tmp/tw2/res/entities\client/QuizField.o
import BigWorld
import gameglobal
import const
from sfx import sfx
from iNpc import INpc
from iDisplay import IDisplay
from data import quiz_field_data as QFD

class QuizField(INpc, IDisplay):

    def __init__(self):
        super(QuizField, self).__init__()
        self.trapId = None
        self.noSelected = True

    def getItemData(self):
        md = QFD.data.get(self.fieldId, {})
        if not md:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        return md

    def needBlackShadow(self):
        md = self.getItemData()
        noBlackUfo = md.get('noBlackUfo', False)
        return not noBlackUfo

    def afterModelFinish(self):
        super(QuizField, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.initYaw = self.yaw
        if self.visibility == const.VISIBILITY_HIDE:
            self.model.visible = False
        else:
            self.model.visible = True
        md = self.getItemData()
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
        self.trapId = BigWorld.addRectPot(self.matrix, self.radii / 2, self.radii / 2, self.trapCallback)

    def enterWorld(self):
        super(QuizField, self).enterWorld()
        md = self.getItemData()
        self.radii = md.get('radii', 0)

    def leaveWorld(self):
        super(QuizField, self).leaveWorld()
        if getattr(self, 'trapId', None):
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            md = self.getItemData()
            ans = md.get('answer', 0) - 1
            gameglobal.rds.ui.diGongPuzzle.refreshCurAns(ans)
        else:
            gameglobal.rds.ui.diGongPuzzle.refreshCurAns(-1)

    def getTopLogoHeight(self):
        return self.getItemData().get('heightOffset', super(QuizField, self).getTopLogoHeight())

    def onCheckQuiz(self, succ):
        md = self.getItemData()
        if succ:
            effectId = md.get('succEffectId', 0)
        else:
            effectId = md.get('failEffectId', 0)
        fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         effectId,
         sfx.EFFECT_UNLIMIT))
        if fx:
            self.addFx(effectId, fx)
