#Embedded file name: /WORKSPACE/data/entities/client/debug/hardpointdebugproxy.o
import ResMgr
import BigWorld
import Pixie
from Scaleform import GfxValue
import const
import gamelog
import clientUtils
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from sfx import sfx
from guis import uiConst
HPName = ['HP_root',
 'HP_leg_right',
 'HP_leg_left',
 'HP_Waist_right',
 'HP_Waist_middle',
 'HP_Waist_left',
 'HP_hand_right_item1',
 'HP_hand_left_item1',
 'HP_hand_right',
 'HP_hand_left',
 'HP_arm_right_item',
 'HP_arm_left_item',
 'HP_LR_front_M',
 'HP_SR_front_M',
 'HP_LR_front_R',
 'HP_SR_front_R',
 'HP_LR_front_L',
 'HP_SR_front_L',
 'HP_hit_default',
 'HP_LR_back_M',
 'HP_SR_back_M',
 'HP_LR_back_L',
 'HP_SR_back_L',
 'HP_LR_back_R',
 'HP_SR_back_R',
 'HP_shoulder_right_item',
 'HP_shoulder_left_item',
 'HP_shoulder_right',
 'HP_shoulder_left',
 'HP_head1',
 'HP_head2',
 'HP_back_item1',
 'HP_back',
 'HP_ride']

class HardPointDebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(HardPointDebugProxy, self).__init__(uiAdapter)
        self.bindType = 'hardPointDebug'
        self.modelMap = {'testHP': self.testHP,
         'changeHP': self.changeHP,
         'changeData': self.changeData,
         'getDataResult': self.getDataResult,
         'testWeapon': self.testWeapon,
         'testEffect': self.testEffect,
         'checkHP': self.checkHP}
        self.HPList = None
        self.isAttach = False
        self.attachHP = None
        self.sampleFx = None
        self.currentHP = None
        self.showHP = False
        self.smallModel = None
        self.dataType = 0
        self.effectList = None
        self.weaponList = None
        self.show = False
        self.fxName = None
        self.fx = None
        self.fxDir = [sfx.DIR_NODE_CONTROL, sfx.DIR_UP_FACEMODEL, sfx.DIR_UP_FACENODE]
        self.fxIndex = 0
        self.attachHP = None
        self.fxId = None
        self.weaponName = None
        self.weapon = None

    def testWeapon(self, *arg):
        if self.show:
            self.detachWeapon()
            self.show = False
        else:
            self.attachWeapon()

    def testEffect(self, *arg):
        gamelog.debug('bgf:fxIndex', arg[3][1].GetString(), self.show)
        self.fxIndex = int(arg[3][1].GetString())
        if self.show:
            self.detachEffect(self.fxId)
            self.show = False
        else:
            self.attachEffect(self.fxId)

    def getDataResult(self, *arg):
        if self.show:
            if self.dataType == 1:
                self.detachWeapon()
            elif self.dataType == 2:
                self.detachEffect(self.fxId)
            self.show = False
        self.dataType = int(arg[3][0].GetString())
        gamelog.debug('dataType', self.dataType)
        if self.dataType == 1:
            if not self.weaponList:
                self.scanWeaponFile()
            return self.weaponList
        if self.dataType == 2:
            if not self.effectList:
                self.scanEffectFile()
            return self.effectList

    def changeData(self, *arg):
        if self.dataType == 1:
            if self.show:
                self.detachWeapon()
            self.weaponName = arg[3][0].GetString()
            if self.show:
                self.attachWeapon()
        elif self.dataType == 2:
            if self.show:
                self.detachEffect(self.fxId)
            self.fxName = arg[3][0].GetString()
            gamelog.debug('bgf:fxName', self.fxName, self.fxName.rfind('/'))
            gamelog.debug('bgf:fxName', self.fxName[self.fxName.rfind('/') + 1:-4])
            self.fxId = int(self.fxName[self.fxName.rfind('/') + 1:-4])
            if self.show:
                self.attachEffect(self.fxId)

    def attachWeapon(self):
        self.show = False
        p = BigWorld.player()
        if self.currentHP:
            node = BigWorld.player().model.node(self.currentHP)
        else:
            p.chatToEventEx('挂接点为空', const.CHANNEL_COLOR_RED)
            return
        if not node:
            p.chatToEventEx('模型没有这个挂接点', const.CHANNEL_COLOR_RED)
            return
        self.weapon = clientUtils.model(self.weaponName)
        if not self.weapon:
            p.chatToEventEX('没有这个武器模型', const.CHANNEL_COLOR_RED)
            return
        weaponNode = self.weapon.node(self.currentHP)
        if not weaponNode:
            p.chatToEventEx('武器上没有这个挂接点', const.CHANNEL_COLOR_RED)
            return
        p.model.setHP(self.currentHP, self.weapon)
        self.show = True

    def detachWeapon(self):
        p = BigWorld.player()
        p.model.setHP(self.currentHP, None)

    def checkHP(self, *arg):
        global HPName
        showExist = bool(arg[3][0].GetString())
        gamelog.debug('bgf:HP', showExist, arg[3][0].GetString())
        if showExist:
            p = BigWorld.player()
            self.HPList = self.movie.CreateArray()
            i = 0
            for hp in HPName:
                node = p.model.node(hp)
                if node:
                    value = GfxValue(hp)
                    self.HPList.SetElement(i, value)
                    i += 1

            return self.HPList
        else:
            self.scanHP()
            return self.HPList

    def getValue(self, key):
        if key == 'hardPointDebug.HPList':
            if not self.HPList:
                self.scanHP()
            return self.HPList

    def testHP(self, *arg):
        if self.currentHP:
            node = BigWorld.player().model.node(self.currentHP)
        else:
            BigWorld.player().chatToEventEx('挂接点为空', const.CHANNEL_COLOR_RED)
            return
        if not node:
            BigWorld.player().chatToEventEx('模型没有这个挂接点', const.CHANNEL_COLOR_RED)
            return
        if not self.smallModel:
            self.smallModel = clientUtils.model('char/2118/2118.model')
        if self.showHP:
            self.showHP = False
            node.detach(self.smallModel)
        else:
            self.showHP = True
            node.attach(self.smallModel)

    def changeHP(self, *arg):
        if self.currentHP:
            node = BigWorld.player().model.node(self.currentHP)
            if self.showHP:
                node.detach(self.smallModel)
        self.currentHP = arg[3][0].GetString()
        if self.showHP:
            node = BigWorld.player().model.node(self.currentHP)
            if node:
                node.attach(self.smallModel)
            else:
                self.showHP = False
                BigWorld.player().chatToEventEx('模型没有这个挂接点', const.CHANNEL_COLOR_RED)

    def attachEffect(self, id):
        self.show = False
        p = BigWorld.player()
        if self.currentHP:
            node = BigWorld.player().model.node(self.currentHP)
        else:
            p.chatToEventEx('挂接点为空', const.CHANNEL_COLOR_RED)
            return
        if not node:
            p.chatToEventEx('模型没有这个挂接点', const.CHANNEL_COLOR_RED)
            return
        if sfx.gEffectMgr.effectCache.hasEffect(id):
            self.fx = sfx.gEffectMgr.effectCache.getEffect(id)
        else:
            self.fx = clientUtils.pixieFetch(sfx.getPath(id))
        x, y, z = self.fxDir[self.fxIndex]
        self.fx.setAttachMode(x, y, z)
        self.fx.clear()
        self.fx.force()
        node.attach(self.fx)
        self.attachHP = node
        self.show = True

    def detachEffect(self, id):
        sfx.gEffectMgr.giveBack(id, self.fx, self.attachHP)

    def scanEffectFile(self):
        self.effectList = self.movie.CreateArray()
        curPath = ['effect/com',
         'effect/char/com',
         'effect/char/buff',
         'effect/weapon',
         'effect/char/combat']
        idx = 0
        for p in curPath:
            folderSection = ResMgr.openSection(p)
            if folderSection:
                for i in folderSection.keys():
                    i = i.lower()
                    if i.endswith('.xml') and i[:-4].isdigit():
                        value = GfxValue(gbk2unicode(p + '/' + i))
                        self.effectList.SetElement(idx, value)
                        idx = idx + 1

        gamelog.debug('effectList', idx)

    def scanWeaponFile(self):
        self.weaponList = self.movie.CreateArray()
        dictPath = {'char/': (70004, 70009),
         'item/model/': (46001, 46010)}
        idx = 0
        for prefixPath in dictPath:
            minId, maxId = dictPath[prefixPath]
            for id in xrange(minId, maxId):
                folderSection = ResMgr.openSection(prefixPath + str(id))
                if folderSection:
                    for i in folderSection.keys():
                        if i.endswith('.model'):
                            value = GfxValue(gbk2unicode(prefixPath + str(id) + '/' + i))
                            self.weaponList.SetElement(idx, value)
                            idx = idx + 1

        gamelog.debug('weaponList', idx)

    def scanHP(self):
        self.HPList = self.movie.CreateArray()
        i = 0
        for hp in HPName:
            value = GfxValue(gbk2unicode(hp))
            self.HPList.SetElement(i, value)
            i = i + 1

    def showHPDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_HP)))
