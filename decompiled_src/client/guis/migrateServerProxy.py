#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/migrateServerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import time
import utils
import gametypes
import const
import gamelog
import formula
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from guis import ui
from ui import unicode2gbk
from guis import pinyinConvert
from cdata import migrate_server_data as MSD
from cdata import migrate_config_data as MCD
from cdata import game_msg_def_data as GMDD
from cdata import migrate_server_group_data as MSGD
from data import mail_template_data as MTD
from data import bonus_data as BD
from data import consumable_item_data as CID
from data import bonus_set_data as BSD
from data import sys_config_data as SCD
from data import region_server_config_data as RSCD

class MigrateServerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MigrateServerProxy, self).__init__(uiAdapter)
        self.modelMap = {'submit': self.onSubmit,
         'chooseServer': self.onChooseServer,
         'closeChoosePanel': self.onCloseChoosePanel,
         'changeServer': self.onChangeServer,
         'getServerNames': self.onGetServerNames}
        self.mediator = None
        self.chooseMed = None
        self.condition = None
        self.npcId = None
        self.serverId = 0
        self.myGroups = None
        self.myGroupServers = []
        self.isOpenByPush = False
        self.chooseSeverType = 0
        self.chooseCallback = None
        self.visibleHostIds = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_MIGRATE_SERVER, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MIGRATE_SERVER_CHOOSE, self.closePanel)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MIGRATE_SERVER:
            self.mediator = mediator
            ret = self.initData()
            return ret
        if widgetId == uiConst.WIDGET_MIGRATE_SERVER_CHOOSE:
            self.chooseMed = mediator
            ret = self._getChooseData(self.visibleHostIds)
            return ret

    def show(self):
        if gameglobal.rds.configData.get('enableMigrateOut', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MIGRATE_SERVER)

    def showServerList(self, chooseSeverType, chooseCallback):
        self.chooseCallback = chooseCallback
        self.chooseSeverType = chooseSeverType
        if chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_MIGRATE:
            p = BigWorld.player()
            p.base.queryOpenMigrateServer()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MIGRATE_SERVER_CHOOSE)

    def realShowChooseServer(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MIGRATE_SERVER_CHOOSE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.chooseMed = None
        self.condition = None
        self.npcId = None
        self.closePanel()
        self.isOpenByPush = False
        self.chooseSeverType = 0
        self.chooseCallback = None
        self.visibleHostIds = []
        gameglobal.rds.ui.funcNpc.onDefaultState()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MIGRATE_SERVER)

    @ui.checkInventoryLock()
    def onSubmit(self, *arg):
        self.serverId = int(arg[3][0].GetNumber())
        if self.serverId == 0:
            BigWorld.player().showGameMsg(GMDD.data.MIGRATE_SERVER_NONE_SERVER_CHOOSE, ())
            return
        else:
            if not self.isOpenByPush and self.npcId != None:
                npc = BigWorld.entity(self.npcId)
                if npc and npc.inWorld:
                    npc.cell.applyMigrate(BigWorld.player().cipherOfPerson, self.serverId)
            elif self.isOpenByPush:
                BigWorld.player().cell.applyNoviceMigrate(BigWorld.player().cipherOfPerson, self.serverId)
            return

    def _getChooseData(self, hostIds):
        ret = {}
        ret['serverId'] = self.serverId
        ret['list'] = self._getServerList(hostIds)
        ret['recommand'] = self._getRecommandServer(hostIds)
        return uiUtils.dict2GfxDict(ret, True)

    def onChooseServer(self, *arg):
        self.showServerList(uiConst.CHOOSE_SERVER_TYPE_MIGRATE, self.changeServer)

    def onCloseChoosePanel(self, *arg):
        self.closePanel()

    def closePanel(self):
        self.chooseSeverType = 0
        self.chooseCallback = None
        self.myGroups = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MIGRATE_SERVER_CHOOSE)

    def _getRecommandServer(self, hostIds):
        ret = []
        selfId = int(gameglobal.rds.g_serverid)
        serverData = MSD.data
        if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_MIGRATE:
            recommandServer = serverData.get(selfId, {}).get('recommandServer', [])
        else:
            recommandServer = []
        recommandServerNames = []
        recommandDict = {}
        for serverId in recommandServer:
            serverName = serverData.get(serverId, {}).get('serverName', '')
            recommandServerNames.append(serverName)
            recommandDict[serverName] = serverId

        srvDict = gameglobal.rds.loginManager.srvDict
        inBusyTime = time.localtime(utils.getNow()).tm_hour >= uiConst.SERVER_BUSY_TIME_START
        serverData = MSD.data
        if srvDict:
            for i, key in enumerate(srvDict.keys):
                for j, v in enumerate(srvDict.item.get(key)):
                    if v.name not in recommandServerNames:
                        continue
                    info = {}
                    serverId = recommandDict.get(v.name, 0)
                    if not serverData.get(serverId, {}).get('migrateIn', 0):
                        continue
                    if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_MIGRATE and serverId not in hostIds:
                        continue
                    busy = int(v.busy)
                    if inBusyTime:
                        if int(v.busy) != uiConst.SERVER_STATE_MAINTENANCE and v.title == v.name:
                            busy = uiConst.SERVER_STATE_BUSY
                    info['busy'] = busy
                    info['locale'] = int(v.locale)
                    info['name'] = v.name
                    info['title'] = v.title
                    info['mode'] = int(v.mode)
                    info['charNum'] = int(v.charNum)
                    info['serverId'] = serverId
                    info['zone'] = key
                    ret.append(info)

        return uiUtils.array2GfxAarry(ret, True)

    def _getServerList(self, hostIds):
        self._updateMyGroupServerNames()
        ret = []
        srvDict = gameglobal.rds.loginManager.srvDict
        inBusyTime = time.localtime(utils.getNow()).tm_hour >= uiConst.SERVER_BUSY_TIME_START
        serverData = MSD.data
        selfId = int(gameglobal.rds.g_serverid)
        if srvDict:
            for i, key in enumerate(srvDict.keys):
                rr = {}
                ar = []
                for j, v in enumerate(srvDict.item.get(key)):
                    if v.name not in self.myGroupServers:
                        continue
                    info = {}
                    serverId = self.myGroups.get(v.name, 0)
                    if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_MIGRATE:
                        if selfId == serverId:
                            continue
                        if serverId not in hostIds:
                            continue
                        if not serverData.get(serverId, {}).get('migrateIn', 0):
                            continue
                    busy = int(v.busy)
                    if inBusyTime:
                        if int(v.busy) != uiConst.SERVER_STATE_MAINTENANCE and v.title == v.name:
                            busy = uiConst.SERVER_STATE_BUSY
                    info['busy'] = busy
                    info['locale'] = int(v.locale)
                    info['name'] = v.name
                    info['title'] = v.title
                    info['mode'] = int(v.mode)
                    info['charNum'] = int(v.charNum)
                    info['serverId'] = serverId
                    ar.append(info)

                charNum = srvDict.getCharNumByZone(key)
                rr['zone'] = key
                rr['values'] = ar
                rr['charNum'] = int(charNum)
                ret.append(rr)

            return uiUtils.array2GfxAarry(ret, True)

    def _updateMyGroupServerNames(self):
        if self.myGroups == None:
            self.myGroups = {}
            self.myGroupServers = []
            selfId = int(gameglobal.rds.g_serverid)
            if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_ARENACHALLENGE:
                selName = utils.getServerName(utils.getHostId())
            else:
                selName = gameglobal.rds.loginManager.titleName()
            gamelog.debug('@nqb titleName is', selName)
            groups = []
            serverData = MSD.data
            srvDict = gameglobal.rds.loginManager.srvDict
            if not srvDict:
                return
            bFlag = False
            for i, key in enumerate(srvDict.keys):
                for j, v in enumerate(srvDict.item.get(key)):
                    serverName = v.name
                    if serverName == selName:
                        if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_MIGRATE:
                            groupId = serverData.get(selfId, {}).get('group', 0)
                            groups = MSGD.data.get(groupId, {}).get('group', [])
                        elif self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_ARENACHALLENGE:
                            groupId = RSCD.data.get(selfId, {}).get('arenaChallengeRegionServer', 0)
                            groups = [ k for k, v in RSCD.data.iteritems() if groupId == v.get('arenaChallengeRegionServer', 0) ]
                        elif not gameglobal.rds.configData.get('enableGlobalFriendServerProgressCheck', False):
                            groupId = serverData.get(selfId, {}).get('globalFriendGroup', 0)
                            groups = MSGD.data.get(groupId, {}).get('group', [])
                        elif gameglobal.rds.ui.yunchuiji.crossMsIds:
                            groups = self.getGroups(gameglobal.rds.ui.yunchuiji.crossMsIds)
                        bFlag = True
                        break

                if bFlag:
                    break

            if self.chooseSeverType in (uiConst.CHOOSE_SERVER_TYPE_ARENACHALLENGE, uiConst.CHOOSE_SERVER_TYPE_ALL):
                data = RSCD.data
            else:
                data = serverData
            for serverId in groups:
                serverName = data.get(serverId, {}).get('serverName', '')
                self.myGroups[serverName] = serverId
                self.myGroupServers.append(serverName)

    def getGroups(self, crossMsIds):
        eventIdList = SCD.data.get('serverEventIdList', ())
        res = []
        for serverId in crossMsIds:
            ids = crossMsIds[serverId]
            bFlag = True
            for eventId in eventIdList:
                if eventId not in ids:
                    bFlag = False
                    break

            if bFlag:
                res.append(serverId)

        return res

    def initData(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['playerName'] = p.playerName
        ret['desc'] = MCD.data.get('migrateServerDesc', '')
        if gameglobal.rds.loginManager.isGtLogonMode():
            serverName = gameglobal.rds.loginManager.titleName()
        else:
            serverName = ''
        ret['serverName'] = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % serverName
        ret['serverId'] = self.serverId
        ret['chooseServer'] = MSD.data.get(self.serverId, {}).get('serverName', gameStrings.TEXT_MIGRATESERVERPROXY_298)
        conditions = []
        configData = MCD.data.get('migrateConditions', {})
        selfId = int(gameglobal.rds.g_serverid)
        serverData = MSD.data.get(selfId, {})
        if self.condition != None:
            for index in self.condition:
                if not configData.has_key(index):
                    continue
                if not gameglobal.rds.configData.get('checkMigrateItem', True) and index == const.MIGRATE_COND_BIND_ITEM:
                    continue
                if not gameglobal.rds.configData.get('enableHome', True) and index == const.MIGRATE_COND_HOME:
                    continue
                conditionObj = {}
                if index == const.MIGRATE_COND_LV:
                    conditionObj['desc'] = configData.get(index, {}).get('desc', gameStrings.TEXT_MIGRATESERVERPROXY_318) % serverData.get('minLv', 59)
                elif index == const.MIGRATE_COND_CASH:
                    conditionObj['desc'] = configData.get(index, {}).get('desc', gameStrings.TEXT_MIGRATESERVERPROXY_320) % serverData.get('maxCash', 100000)
                else:
                    conditionObj['desc'] = configData.get(index, {}).get('desc', gameStrings.TEXT_MIGRATESERVERPROXY_322)
                conditionObj['match'] = self.condition[index]
                conditionObj['helpIndex'] = configData.get(index, {}).get('helpId', 0)
                conditionObj['index'] = configData.get(index, {}).get('index', index)
                conditions.append(conditionObj)

        conditions.sort(key=lambda k: int(k['index']))
        itemHoldMax = MCD.data.get('itemHoldMax', [])
        for data in itemHoldMax:
            itemId = data[0]
            count = data[1]
            ownCount = self._getItemCount(itemId)
            conditionObj = {}
            itemName = uiUtils.getItemColorName(itemId)
            if count == 0:
                conditionObj['desc'] = uiUtils.getTextFromGMD(GMDD.data.MIGRATE_SERVERT_ITEM_FORBIDDEN, gameStrings.TEXT_MIGRATESERVERPROXY_338) % itemName
            elif count > 0:
                conditionObj['desc'] = uiUtils.getTextFromGMD(GMDD.data.MIGRATE_SERVERT_ITEM_LIMIT, gameStrings.TEXT_MIGRATESERVERPROXY_340) % (itemName, count)
            conditionObj['match'] = count >= ownCount
            if conditionObj['match']:
                continue
            conditionObj['helpIndex'] = 0
            conditions.append(conditionObj)

        ret['conditions'] = conditions
        ret['isNewbieServer'] = False
        if serverData.get('noviceServer', 0):
            ret['isNewbieServer'] = gameglobal.rds.configData.get('enableServerBonus', False)
            ret['bonusItems'] = self._getBonusItems(selfId)
            ret['isMatchBonus'] = p.lv >= 49
        ret['bonusDesc'] = MCD.data.get('bonusDesc', '')
        return uiUtils.dict2GfxDict(ret, True)

    def _getItemCount(self, itemId):
        p = BigWorld.player()
        countInInv = p.inv.countItemInPages(itemId)
        countInFashion = 0
        for page in xrange(p.fashionBag.pageCount):
            pos = p.fashionBag.searchAllByID(itemId, page)
            countInFashion += len(pos)

        countInTemp = 0
        for page in xrange(p.tempBag.pageCount):
            pos = p.tempBag.searchAllByID(itemId, page)
            countInTemp += len(pos)

        countInMater = 0
        for page in xrange(p.materialBag.pageCount):
            pos = p.materialBag.searchAllByID(itemId, page)
            countInMater += len(pos)

        countInMall = 0
        for page in xrange(p.mallBag.pageCount):
            pos = p.mallBag.searchAllByID(itemId, page)
            countInMall += len(pos)

        countInStorage = 0
        for page in xrange(p.storage.pageCount):
            pos = p.storage.searchAllByID(itemId, page)
            countInStorage += len(pos)

        allCount = countInInv + countInFashion + countInTemp + countInMater + countInMall + countInStorage
        return allCount

    def _getServerGroupIdx(self, serverId):
        groupData = MSGD.data
        for idx in groupData:
            groups = groupData[idx].get('group', [])
            if serverId in groups:
                return idx

        return 0

    def onChangeServer(self, *arg):
        self.serverId = int(arg[3][0].GetNumber())
        if self.chooseCallback:
            if self.chooseSeverType == uiConst.CHOOSE_SERVER_TYPE_ARENACHALLENGE:
                serverName = RSCD.data.get(self.serverId, {}).get('serverName', '')
            else:
                serverName = MSD.data.get(self.serverId, {}).get('serverName', '')
            self.chooseCallback(self.serverId, serverName)
        self.closePanel()

    def changeServer(self, serverId, serverName):
        ret = {}
        ret['serverId'] = serverId
        ret['serverName'] = serverName
        if self.mediator:
            self.mediator.Invoke('updateChooseServer', uiUtils.dict2GfxDict(ret, True))

    def pushMigrate(self):
        selfId = int(gameglobal.rds.g_serverid)
        if not MSD.data.get(selfId, {}).get('noviceServer', 0):
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MIGRATE_SERVER)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MIGRATE_SERVER, {'click': self.clickOpenMigrate})

    def clickOpenMigrate(self):
        self.isOpenByPush = True
        p = BigWorld.player()
        p.cell.useNoviceMigrate('')

    def onGetServerNames(self, *arg):
        name = unicode2gbk(arg[3][0].GetString().strip())
        ret = []
        if name == '':
            return uiUtils.array2GfxAarry(ret, True)
        name = name.lower()
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return uiUtils.array2GfxAarry(ret, True)
        names = self.myGroupServers
        if len(name) == 1:
            return uiUtils.array2GfxAarry(names, True)
        if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
            ret = [ x for x in names if name in str(pinyinConvert.strPinyinFirst(x)) ]
        else:
            ret = [ x for x in names if name in str(x) ]
        return uiUtils.array2GfxAarry(ret, True)

    def clearData(self):
        self.npcId = None
        self.serverId = 0
        self.myGroups = None
        self.myGroupServers = []

    def _getBonusItems(self, serverId):
        bonusItem = {}
        bonusItem['basicBonus'] = []
        bonusItem['bonus'] = []
        mailTemplateId = MSD.data.get(serverId, {}).get('mailTemplateId', 0)
        bonusId = MTD.data.get(mailTemplateId, {}).get('bonusId', 0)
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        itemSetInfo = CID.data.get(itemId, {}).get('itemSetInfo', [0, 0])[0]
        bonusItemInfo = BSD.data.get(itemSetInfo, [])
        items = []
        for item in bonusItemInfo:
            if item.get('calcType') in (0, 1) and item.get('bonusType') == gametypes.BONUS_TYPE_ITEM:
                itemId = utils.filtItemByConfig(item['bonusId'], lambda e: e)
            else:
                itemId = item['bonusId']
            if not itemId:
                continue
            itemObj = uiUtils.getGfxItemById(itemId)
            items.append(itemObj)

        bonusItem['basicBonus'] = items
        exEailTemplateId = MSD.data.get(serverId, {}).get('exEailTemplateId', 0)
        exBonusId = MTD.data.get(exEailTemplateId, {}).get('bonusId', 0)
        exFixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        exFixedBonus = utils.filtItemByConfig(exFixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if exFixedBonus:
            exItemId = exFixedBonus[0][1]
        else:
            exItemId = 0
        exItemSetInfo = CID.data.get(exItemId, {}).get('itemSetInfo', [0, 0])[0]
        exBonusItemInfo = BSD.data.get(exItemSetInfo, [])
        bonusItems = []
        for item in exBonusItemInfo:
            if item.get('calcType') in (0, 1) and item.get('bonusType') == gametypes.BONUS_TYPE_ITEM:
                itemId = utils.filtItemByConfig(item['bonusId'], lambda e: e)
            else:
                itemId = item['bonusId']
            if not itemId:
                continue
            itemObj = uiUtils.getGfxItemById(itemId)
            bonusItems.append(itemObj)

        bonusItem['bonus'] = bonusItems
        return bonusItem
