#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/targetRoleInfoProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gameconfigCommon
import uiConst
import commcalc
import gametypes
import time
import utils
import const
from item import Item
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from guis import uiUtils
from helpers import capturePhoto
from helpers import charRes
from const import EQUIP_PART_NUM
from cdata import font_config_data as FCD
from data import item_data as ID
from data import jingjie_data as JD
from data import equip_data as ED
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class TargetRoleInfoProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(TargetRoleInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRoleInfo': self.onGetRoleInfo,
         'getFashionSuit': self.onGetFashionSuit,
         'rotateFigure': self.onRotateFigure,
         'checkSkill': self.onCheckSkill,
         'checkHierogram': self.onCheckHierogram,
         'checkWarSprite': self.onCheckWarSprite,
         'getSkillCheckVisible': self.onGetSkillCheckVisible}
        self.binding = {}
        self.bindType = 'tarrole'
        self.type = 'tarroleslot'
        self.roleName = None
        self.lv = None
        self.equip = None
        self.suitsCache = None
        self.school = None
        self.guildName = None
        self.aspect = None
        self.physique = None
        self.avatarConfig = None
        self.mediator = None
        self.headGen = None
        self.lastLogoffTime = None
        self.jingJie = 0
        self.signal = 0
        self.guanYin = None
        self.wenYin = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_TARGET_ROLE_INFO, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TARGET_ROLE_INFO:
            self.mediator = mediator
            self.initHeadGen()
            self.takePhoto3D()

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.104 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[7:]), int(idItem[4:]))

    def getSlotValue(self, movie, idItem, idBar):
        equip = self.getFashionEquipment()
        if not equip:
            return
        item = equip.get(idItem)
        if not item:
            return
        itemInfo = uiUtils.getGfxItem(item)
        if itemInfo.has_key('pinXing'):
            itemInfo.pop('pinXing')
        return uiUtils.dict2GfxDict(itemInfo)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        i = self.equip.get(idNum)
        if i != None:
            return gameglobal.rds.ui.inventory.GfxToolTip(i, const.ITEM_IN_TARGET_ROLE)
        else:
            return

    def _getKey(self, nSlot):
        return 'tarrole0.slot%d' % nSlot

    def updateRoleInfo(self):
        equip = self.getFashionEquipment()
        if not equip:
            return
        for pos, item in enumerate(equip):
            self.removeItem(pos)
            if item:
                self.addItem(item, pos)

        self.setOtherData()

    def addItem(self, item, idSlot):
        if not item:
            return
        else:
            key = self._getKey(idSlot)
            if not self.binding.get(key, None):
                return
            itemInfo = uiUtils.getGfxItem(item)
            if itemInfo.has_key('pinXing'):
                itemInfo.pop('pinXing')
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemInfo))
            return

    def removeItem(self, idSlot):
        key = self._getKey(idSlot)
        if not self.binding.get(key, None):
            return
        else:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            return

    def setOtherData(self):
        jingjieName = JD.data.get(self.jingJie, {}).get('name', '')
        self.mediator.Invoke('setOtherData', (GfxValue('Lv.' + str(self.lv)),
         GfxValue(gbk2unicode(self.roleName)),
         GfxValue(str(self.equip.calcAllEquipScore(self.suitsCache))),
         GfxValue(gbk2unicode(self.guildName)),
         GfxValue(self.jingJie),
         GfxValue(gbk2unicode(jingjieName)),
         GfxValue(gbk2unicode(self.getOfflineTime())),
         GfxValue(True if self.lastLogoffTime else False)))

    def onGetRoleInfo(self, *arg):
        self.target = BigWorld.player()
        arr = self.movie.CreateArray()
        arr.SetElement(0, GfxValue('Lv.' + str(self.lv)))
        arr.SetElement(1, GfxValue(gbk2unicode(self.roleName)))
        score = 0 if not self.equip else self.equip.calcAllEquipScore(self.suitsCache)
        arr.SetElement(2, GfxValue(str(score)))
        arr.SetElement(3, GfxValue(gbk2unicode(self.guildName)))
        arr.SetElement(4, GfxValue(self.jingJie))
        jingjieName = JD.data.get(self.jingJie, {}).get('name', '')
        arr.SetElement(5, GfxValue(gbk2unicode(jingjieName)))
        arr.SetElement(6, GfxValue(gbk2unicode(self.getOfflineTime())))
        arr.SetElement(7, GfxValue(True if self.lastLogoffTime else False))
        return arr

    def getOfflineTime(self):
        nowTime = utils.getNow()
        if self.lastLogoffTime:
            diffTime = nowTime - self.lastLogoffTime
            if diffTime > const.TIME_INTERVAL_WEEK:
                timestr = gameStrings.TEXT_TARGETROLEINFOPROXY_159 + time.strftime(gameStrings.TEXT_TARGETROLEINFOPROXY_159_1, time.localtime(self.lastLogoffTime)) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6
            else:
                timestr = gameStrings.TEXT_TARGETROLEINFOPROXY_159 + gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_116 % (diffTime / const.TIME_INTERVAL_HOUR)
        else:
            timestr = gameStrings.TEXT_TARGETROLEINFOPROXY_163
        return timestr

    def show(self, roleName, equip, lv, school, guildName, jingJie, aspect, physique, avatarConfig, signal, suitsCache, lastLogoffTime, guanYin, wenYin):
        self.roleName = roleName
        self.lv = lv
        self.equip = equip
        self.suitsCache = suitsCache
        self.school = school
        self.aspect = aspect
        self.physique = physique
        self.avatarConfig = avatarConfig
        self.jingJie = jingJie
        self.signal = signal
        self.lastLogoffTime = lastLogoffTime
        self.guanYin = guanYin
        self.wenYin = wenYin
        BigWorld.player().doFillGemToEquipments(self.equip, self.wenYin)
        if not guildName:
            self.guildName = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        else:
            self.guildName = guildName
        if self.mediator != None:
            self.updateRoleInfo()
            self.takePhoto3D()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TARGET_ROLE_INFO)

    def reset(self):
        super(self.__class__, self).reset()
        self.roleName = None
        self.lv = None
        self.equip = None
        self.suitsCache = None
        self.school = None
        self.guildName = None
        self.aspect = None
        self.physique = None
        self.avatarConfig = None
        self.lastLogoffTime = None

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TARGET_ROLE_INFO)
        self.resetHeadGen()

    def closeRoleInfo(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TARGET_ROLE_INFO)
        self.mediator = None
        self.roleName = None
        self.lv = None
        self.equip = None
        self.suitsCache = None
        self.school = None
        self.guildName = None
        self.lastLogoffTime = None

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.TargetRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 442)
        if not self.physique:
            return
        modelId = charRes.transBodyType(self.physique.sex, self.physique.bodyType)
        showFashion = commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION)
        self.headGen.startCaptureRes(modelId, self.aspect, self.physique, self.avatarConfig, ('1101',), showFashion)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.TargetRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 442)
        self.headGen.initFlashMesh()

    def onGetFashionSuit(self, *arg):
        ret = self._genFashionSuit()
        return ret

    def getFashionEquipment(self):
        return self.equip

    def _genFashionSuit(self):
        arr = [0] * EQUIP_PART_NUM
        equip = self.getFashionEquipment()
        if not equip:
            return uiUtils.array2GfxAarry(arr)
        else:
            for i in xrange(EQUIP_PART_NUM):
                item = equip.get(i, None)
                if not item:
                    continue
                eData = ED.data.get(item.id, {})
                parts = eData.get('slotParts', [])
                if parts:
                    arr[i] = 1
                    for part in parts:
                        arr[self.equip.FASHION_PARTS_MAP[part]] = 1

            return uiUtils.array2GfxAarry(arr)

    def test(self):
        p = BigWorld.player()
        self.show(p.realRoleName, None, p.lv, p.school, p.guildName, p.jingJie, p.aspect, p.physique, p.avatarConfig, p.signal, None, None)

    def onCheckSkill(self, *args):
        p = BigWorld.player()
        p.querySkillInfoByChat(self.roleName)

    def onCheckHierogram(self, *args):
        p = BigWorld.player()
        p.queryHierogramInfoByChat(self.roleName)

    def onCheckWarSprite(self, *args):
        p = BigWorld.player()
        p.querySpriteInfoByChat(self.roleName)

    def onGetSkillCheckVisible(self, *args):
        autoLv = SCD.data.get('SKILL_AUTO_UP_LV', 40)
        if self.lv < autoLv:
            return GfxValue(False)
        return GfxValue(True)
