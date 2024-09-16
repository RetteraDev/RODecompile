#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildProduceProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from helpers import guild as guildUtils
from data import guild_factory_product_data as GFPD
from data import guild_resident_pskill_data as GRPD

def sort_resident(a, b):
    return a['isWorking'] - b['isWorking']


class GuildProduceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildProduceProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickResident': self.onClickResident,
         'confirm': self.onConfirm}
        self.mediator = None
        self.markerId = 0
        self.productId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_PRODUCE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_PRODUCE:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, markerId, productId):
        self.markerId = markerId
        self.productId = productId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_PRODUCE)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_PRODUCE)

    def reset(self):
        self.markerId = 0
        self.productId = 0

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            productInfo = GFPD.data.get(self.productId, {})
            info = {}
            if buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
                info['titleName'] = gameStrings.TEXT_GUILDPRODUCEPROXY_62
            elif buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
                info['titleName'] = gameStrings.TEXT_GUILDPRODUCEPROXY_64
            else:
                return
            itemId = productInfo.get('itemId', 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
            info['itemInfo'] = itemInfo
            factory = guild._getFactory(productInfo.get('type', gametypes.GUILD_FACTORY_PRODUCT_MACHINE))
            mojing, xirang, wood, bindCash, consumeItems = factory.getProduceCost(guild, self.productId)
            enabledState = True
            info['cash'] = bindCash
            info['cashHave'] = guild.bindCash
            if info['cash'] > info['cashHave']:
                info['cashHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['cashHaveColor'] = '0xFFFFE7'
            info['wood'] = wood
            info['woodHave'] = guild.wood
            if info['wood'] > info['woodHave']:
                info['woodHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['woodHaveColor'] = '0xFFFFE7'
            info['mojing'] = mojing
            info['mojingHave'] = guild.mojing
            if info['mojing'] > info['mojingHave']:
                info['mojingHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['mojingHaveColor'] = '0xFFFFE7'
            info['xirang'] = xirang
            info['xirangHave'] = guild.xirang
            if info['xirang'] > info['xirangHave']:
                info['xirangHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['xirangHaveColor'] = '0xFFFFE7'
            costItemList = []
            if consumeItems:
                for itemId, needNum in consumeItems:
                    if itemId == 0:
                        continue
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                    ownNum = guild.otherRes.get(itemId, 0)
                    itemInfo['itemNum'] = uiUtils.convertNumStr(ownNum, needNum)
                    if ownNum < needNum:
                        enabledState = False
                    costItemList.append(itemInfo)

            info['costItemList'] = costItemList
            info['costTime'] = ''
            info['enabledState'] = enabledState
            pskillId = productInfo.get('pskillId', 0)
            skillName = GRPD.data.get((pskillId, 1), {}).get('name', '')
            if skillName != '':
                info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_130 % skillName
                info['reqSkillColor'] = '0xF43804'
                info['pskillExist'] = False
            else:
                info['reqSkill'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                info['reqSkillColor'] = '0xFFFFE7'
                info['pskillExist'] = True
            normalList = []
            normalWorkers = marker.getFuncWorkers()
            for residentNUID in normalWorkers:
                residentInfo = guildUtils.createResidentInfo(guild, residentNUID)
                normalList.append(residentInfo)

            normalList.sort(cmp=sort_resident)
            info['normalList'] = normalList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onClickResident(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        guild = BigWorld.player().guild
        info = {}
        resident = guild.hiredResident.get(residentNUID)
        costTime = resident.getProduceTime(guild, self.productId)
        info['costTime'] = costTime
        productInfo = GFPD.data.get(self.productId, {})
        pskillId = productInfo.get('pskillId', 0)
        skillName = GRPD.data.get((pskillId, 1), {}).get('name', '')
        if skillName != '':
            if pskillId not in resident.pskills:
                info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_130 % skillName
                info['reqSkillColor'] = '0xF43804'
                info['pskillExist'] = False
            else:
                info['reqSkill'] = gameStrings.TEXT_GUILDPRODUCEPROXY_167 % skillName
                info['reqSkillColor'] = '0xFFFFE7'
                info['pskillExist'] = True
        else:
            info['reqSkill'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
            info['reqSkillColor'] = '0xFFFFE7'
            info['pskillExist'] = True
        return uiUtils.dict2GfxDict(info, True)

    def onConfirm(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.addGuildFactoryTask(self.productId, residentNUID)
        self.hide()
