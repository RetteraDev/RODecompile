#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/runeViewProxy.o
import re
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import const
from gameclass import PSkillInfo
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from data import item_data as ID
from cdata import font_config_data as FCD
from data import rune_effect_data as RED
from cdata import rune_tips_data as RTD
from cdata import pskill_data as PD
SED_FLAG = 1
SD_FLAG = 2
SCD_FLAG = 3
INT_FLAG = 0
PERCENT_FLAG = 1

class RuneViewProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneViewProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'getData': self.onGetData}
        self.mediator = None
        self.bindType = 'runeView'
        self.type = 'runeView'
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_VIEW, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_VIEW:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_VIEW)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_VIEW)

    def onClickClose(self, *arg):
        self.hide()

    def onGetData(self, *arg):
        p = BigWorld.player()
        dataObj = self.movie.CreateObject()
        runeArray = self.movie.CreateArray()
        allHieroEffect = []
        pSkills = {}
        if gameglobal.rds.configData.get('enableHierogram', False):
            allHieroEffect = p.hierogramDict.get('totalEffects', [0] * const.RUNE_EFFECT_TYPE_NUM)
            pSkills = p.hierogramDict.get('pSkills', {})
        else:
            allHieroEffect = p.runeBoard.allRuneEffects
            pSkills = p.runeBoard.pskillSet
        dataObj.SetMember('effectArray', uiUtils.array2GfxAarry(allHieroEffect))
        runeArray = self.movie.CreateArray()
        for i, id in enumerate(RED.data):
            activate = False
            runeNodeObj = self.movie.CreateObject()
            runeItemArray = self.movie.CreateArray()
            if id in pSkills:
                pskillLv = pSkills[id][1]
                activate = True
            else:
                pskillLv = 1
            runeEffextData = RED.data[id][pskillLv - 1]
            runeNodeObj.SetMember('effectId', GfxValue(str(id)))
            runeNodeObj.SetMember('activate', GfxValue(activate))
            runeNodeObj.SetMember('pskillLv', GfxValue(pskillLv))
            runeNodeObj.SetMember('name', GfxValue(gbk2unicode(runeEffextData['name'])))
            runeNodeObj.SetMember('valueArray', uiUtils.array2GfxAarry(runeEffextData['runeEffectsNeed']))
            pskillId = runeEffextData['pskillId']
            runeNodeObj.SetMember('desc', GfxValue(gbk2unicode(self.generateDesc(pskillId, PSkillInfo(pskillId, pskillLv, {}), pskillLv))))
            for itemId in range(len(RED.data[id])):
                runeItemObj = self.movie.CreateObject()
                runeItemObj.SetMember('effectId', GfxValue(str(itemId)))
                runeItemObj.SetMember('name', GfxValue(gbk2unicode(RED.data[id][itemId]['name'])))
                runeItemObj.SetMember('valueArray', uiUtils.array2GfxAarry(RED.data[id][itemId]['runeEffectsNeed']))
                itemPskillId = runeEffextData['pskillId']
                runeItemObj.SetMember('desc', GfxValue(gbk2unicode(self.generateDesc(itemPskillId, PSkillInfo(itemPskillId, itemId + 1, {}), itemId + 1))))
                runeItemArray.SetElement(itemId, runeItemObj)

            runeNodeObj.SetMember('itemArray', runeItemArray)
            runeArray.SetElement(i, runeNodeObj)

        dataObj.SetMember('runeArray', runeArray)
        return dataObj

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[8:]), int(idItem[4:]))

    def _getKey(self, nBar, nSlot):
        return 'runeView%d.slot%d' % (nBar, nSlot)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        item = None
        if page == uiConst.RUNE_TYPE_EQUIP:
            item = p.runeBoard.runeEquip
        else:
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.item and page == runeDataVal.runeSlotsType and pos == runeDataVal.part:
                    item = runeDataVal.item
                    break

        if not item:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(item)

    def addItem(self, item, page, pos):
        if item is not None:
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = self.uiAdapter.movie.CreateObject()
                icon = uiUtils.getItemIconFile40(item.id)
                idNum = GfxValue(item.id)
                name = GfxValue('item')
                iconPath = GfxValue(icon)
                count = GfxValue(item.cwrap)
                data.SetMember('id', idNum)
                data.SetMember('name', name)
                data.SetMember('iconPath', iconPath)
                data.SetMember('count', count)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(data)

    def removeItem(self, page, pos):
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def updatePskill(self):
        if self.mediator:
            p = BigWorld.player()
            dataObj = self.movie.CreateObject()
            allHieroEffect = []
            pSkills = {}
            if gameglobal.rds.configData.get('enableHierogram', False):
                allHieroEffect = p.hierogramDict.get('totalEffects', [0] * const.RUNE_EFFECT_TYPE_NUM)
                pSkills = p.hierogramDict.get('pSkills', {})
            else:
                allHieroEffect = p.runeBoard.allRuneEffects
                pSkills = p.runeBoard.pskillSet
            dataObj.SetMember('effectArray', uiUtils.array2GfxAarry(allHieroEffect))
            runeArray = self.movie.CreateArray()
            for i, id in enumerate(RED.data):
                activate = False
                runeNodeObj = self.movie.CreateObject()
                if id in pSkills:
                    pskillLv = pSkills[id][1]
                    activate = True
                else:
                    pskillLv = 1
                runeEffextData = RED.data[id][pskillLv - 1]
                runeNodeObj.SetMember('effectId', GfxValue(str(id)))
                runeNodeObj.SetMember('activate', GfxValue(activate))
                runeNodeObj.SetMember('pskillLv', GfxValue(pskillLv))
                runeNodeObj.SetMember('name', GfxValue(gbk2unicode(runeEffextData['name'])))
                runeNodeObj.SetMember('valueArray', uiUtils.array2GfxAarry(runeEffextData['runeEffectsNeed']))
                pskillId = runeEffextData['pskillId']
                runeNodeObj.SetMember('desc', GfxValue(gbk2unicode(self.generateDesc(pskillId, PSkillInfo(pskillId, pskillLv, {}), pskillLv))))
                runeArray.SetElement(i, runeNodeObj)

            dataObj.SetMember('runeArray', runeArray)
            self.mediator.Invoke('updatePskill', dataObj)

    def generateDesc(self, pskillId, pSkillInfo, pskillLv = 1):
        desc = PD.data[pskillId, pskillLv]['desc']
        matchobj = re.search('\\$(.+?)\\$', desc)
        while matchobj:
            if matchobj.group(1) + 'Type' in PD.data[pskillId, 1]:
                valueType = PD.data[pskillId, 1][matchobj.group(1) + 'Type']
                value = pSkillInfo.getSkillData(matchobj.group(1))
            else:
                pSkillData = pSkillInfo.getSkillData('affectSkillData')[int(matchobj.group(1)[8:]) - 1]
                dataType = pSkillData[0]
                arg = pSkillData[1]
                index = pSkillData[2]
                if (dataType, arg, index) in RTD.data:
                    valueType = RTD.data[dataType, arg, index]['flag']
                value = pSkillData[4]
            if valueType == INT_FLAG:
                if value == int(value):
                    desc = desc.replace(matchobj.group(0), str(int(value)))
                else:
                    desc = desc.replace(matchobj.group(0), str(int(value * 1000) / 1000.0))
            else:
                desc = desc.replace(matchobj.group(0), str(int(value * 100)))
            matchobj = re.search('\\$(.+?)\\$', desc)

        return desc
