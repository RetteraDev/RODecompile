#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/dyeTestProxy.o
import BigWorld
import gamelog
import const
import utils
import gametypes
from guis.uiProxy import DataProxy
from guis import uiConst
from helpers import charRes

class DyeTestProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(DyeTestProxy, self).__init__(uiAdapter)
        self.bindType = 'dyeTest'
        self.modelMap = {'copyColor': self.onCopyColor,
         'adjustColor': self.onAdjustColor,
         'adjustPbrHL': self.onAdjustPbrHL,
         'saveColor': self.onSaveColor}
        self.reset()

    def reset(self):
        self.channel = 1
        self.chooseColor0 = ''
        self.chooseColor1 = ''
        self.dyeList = []

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DYE_TEST)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_DYE_TEST)

    def onCopyColor(self, *arg):
        colorText = arg[3][0].GetString()
        BigWorld.setClipBoardText(colorText)

    def onAdjustPbrHL(self, *arg):
        channel = int(arg[3][0].GetNumber())
        pbrHL = arg[3][1].GetString()
        p = BigWorld.player()
        parts = p.isShowFashion() and charRes.PARTS_ASPECT_FASHION or charRes.PARTS_ASPECT_EQUIP
        for part in parts:
            oldDyeList = getattr(p.aspect, part + 'DyeList')()
            index = const.DYES_INDEX_PBR_DUAL_HIGH_LIGHT if channel == const.DYE_CHANNEL_2 else const.DYES_INDEX_PBR_HIGH_LIGHT
            self.dyeList = utils.addDyeLists(oldDyeList, index, pbrHL)
            p.aspect.set(gametypes.ASPECT_PART_DICT[part], getattr(p.aspect, part), self.dyeList)

        gamelog.debug('onAdjustPbrHL', p.aspect.fashionBodyDyeList())
        p.set_aspect(None)

    def onAdjustColor(self, *arg):
        channel = int(arg[3][0].GetNumber())
        self.chooseColor0 = arg[3][1].GetString()
        self.chooseColor1 = arg[3][2].GetString()
        self.channel = channel
        if self.chooseColor0 and self.chooseColor1:
            p = BigWorld.player()
            parts = p.isShowFashion() and charRes.PARTS_ASPECT_FASHION or charRes.PARTS_ASPECT_EQUIP
            for part in parts:
                oldDyeList = getattr(p.aspect, part + 'DyeList')()
                newDyeList = [self.chooseColor0, self.chooseColor1]
                index = const.DYES_INDEX_DUAL_COLOR if channel == const.DYE_CHANNEL_2 else const.DYES_INDEX_COLOR
                self.dyeList = utils.addDyeLists(oldDyeList, index, newDyeList)
                p.aspect.set(gametypes.ASPECT_PART_DICT[part], getattr(p.aspect, part), self.dyeList)

            gamelog.debug('onAdjustColor2', p.aspect.fashionBodyDyeList())
            p.set_aspect(None)

    def onSaveColor(self, *arg):
        p = BigWorld.player()
        parts = p.isShowFashion() and charRes.PARTS_ASPECT_FASHION or charRes.PARTS_ASPECT_EQUIP
        equipPart = []
        for part in parts:
            equipPart.append(gametypes.ASPECT_PART_DICT[part])

        if self.dyeList:
            p.cell.testDyeFashion(equipPart, self.dyeList)
