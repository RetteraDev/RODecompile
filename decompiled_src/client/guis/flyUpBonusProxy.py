#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/flyUpBonusProxy.o
import BigWorld
import gameglobal
from uiProxy import UIProxy
from guis.asObject import RichItemConst
from item import Item
from guis import richTextUtils

class FlyUpBonusProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FlyUpBonusProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.bonusDesc.setParsers([RichItemConst.ITEM_PARSER, RichItemConst.SKILL_PARSER, RichItemConst.IMG_PARSER])

    def testRichText(self):
        self.widget.bonusDesc.text = '[img local:photoGenBg/1003.dds@100_100][skill1001][item999]\ndddd'
