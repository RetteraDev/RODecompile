#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildArmorProxy.o
import BigWorld
import copy
import gametypes
import gameglobal
import uiConst
from uiProxy import UIProxy
from helpers import charRes
from helpers import avatarMorpher
from helpers import capturePhoto
from data import guild_config_data as GCD

class GuildArmorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildArmorProxy, self).__init__(uiAdapter)
        self.modelMap = {'selectArmorColor': self.onSelectArmorColor,
         'confirm': self.onConfirm,
         'close': self.onClose}
        self.mediator = None
        self.armorGen = None
        self.color = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ARMOR_SETTING, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ARMOR_SETTING:
            self.mediator = mediator
            self.initArmorPhoto()
            self.takeArmorPhoto()

    def clearWidget(self):
        self.resetArmorPhoto()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ARMOR_SETTING)

    def reset(self):
        self.armorGen = None
        self.color = None

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ARMOR_SETTING)

    def onSelectArmorColor(self, *arg):
        index = int(arg[3][0].GetString().split('_')[-1])
        gcd = GCD.data.get('zhanPaoColor', [])
        if index < len(gcd):
            color = gcd[index][0:3]
            self.color = ('%d,%d,%d,255' % color, '255,255,255,255')
            self.dyeArmorPhoto(self.color)

    def onConfirm(self, *arg):
        if self.color:
            player = BigWorld.player()
            player.cell.setClanWarArmorColor(self.color)
            gameglobal.rds.ui.guild.dyeArmorPhoto(self.color)
            self.hide()

    def onClose(self, *arg):
        self.hide()

    def takeArmorPhoto(self, modelId = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL, tintMs = None, photoAction = None):
        if not self.armorGen:
            self.armorGen = capturePhoto.ZhanPaoPhotoGen.getInstance('gui/taskmask.tga', 422)
        p = BigWorld.player()
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(p.realPhysique, p.realAspect, False, p.avatarConfig, True)
        res = mpr.getPrerequisites()
        self.armorGen.startCaptureEntAndRes(p, res)

    def resetArmorPhoto(self):
        if self.armorGen:
            self.armorGen.endCapture()

    def initArmorPhoto(self):
        if not self.armorGen:
            self.armorGen = capturePhoto.ZhanPaoPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.armorGen.initFlashMesh()

    def dyeArmorPhoto(self, color):
        if self.armorGen:
            model = self.armorGen.adaptor.attachment
            if model:
                player = BigWorld.player()
                aspect = copy.deepcopy(player.realAspect)
                equipId = aspect.clanWarArmor
                aspect.set(gametypes.EQU_PART_CLAN_WAR_ARMOR, equipId, color)
                mpr = charRes.MultiPartRes()
                mpr.queryByAttribute(player.realPhysique, aspect, False, player.avatarConfig, True)
                dyesDict = mpr.getDyeDict(aspect, False, True)
                m = avatarMorpher.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, dyesDict)
                m.readConfig(player.realAvatarConfig)
                m.applyDyeMorph(True)
