#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assignProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import hotkey as HK
import utils
from guis import ui
from guis import uiConst
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiUtils
from guis import hotkeyProxy
from item import Item
from data import item_data as ID
from cdata import font_config_data as FCD
from data import sys_config_data as SCD
DICE_BY_SCHOOL = 0
DICE_IGNORE_SCHOOL = 1

class AssignProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(AssignProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitTeamBagItem': self.onGetInitTeamBagItem,
         'getTeammateNames': self.onGetTeammateNames,
         'assignItemTo': self.onAssignItemTo,
         'getAssignBtnEnable': self.onGetAssignBtnEnable,
         'closeTeamBag': self.onCloseTeamBag,
         'getPlayerAndItemNames': self.onGetPlayerAndItemNames,
         'confirmAssign': self.onConfirmAssign,
         'cancelAssign': self.onCancelAssign,
         'dice': self.onDice,
         'giveUp': self.onGiveUp,
         'greed': self.onGreed,
         'getDiceItem': self.onGetDiceItem,
         'closeDice': self.onCloseDice,
         'getTeamInfo': self.onGetTeamInfo,
         'getTeamState': self.onGetTeamState,
         'isInTeam': self.onIsInTeam,
         'auction': self.onAuction,
         'giveUpAuction': self.onGiveUpAuction,
         'getAuctionInfo': self.onGetAuctionInfo,
         'pauseAuction': self.onPauseAuction,
         'getAuctionHotKey': self.onGetAuctionHotKey,
         'getDiceHotKey': self.onGetDiceHotKey,
         'getDiceWay': self.onGetDiceWay,
         'diceAll': self.onDiceAll,
         'getDiceTips': self.onGetDiceTips,
         'getAssignWay': self.onGetAssignWay}
        self.binding = {}
        self.bindType = 'assign'
        self.type = 'assign'
        self.mediator = None
        self.diceMediator = None
        self.auctionMediator = None
        self.teamBag = [const.CONT_EMPTY_VAL] * const.GROUP_PICK_MAX
        self.assignTarget = [None] * const.GROUP_PICK_MAX
        self.diceBag = []
        self.teammate = []
        self.isTeamBagShow = False
        self.isDiceShow = False
        self.destName = None
        self.destGbId = None
        self.destItem = None
        self.owner = []
        self.selectPos = None
        self.auctionBag = []
        self.curAuctionPrice = 0
        self.curAuctionPlayer = ''
        self.curAuctionUUID = 0
        self.curGiveUp = False
        self.auctionStep = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ASSIGN_TEAMBAG:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_ASSIGN_DICE:
            self.diceMediator = mediator
        elif widgetId == uiConst.WIDGET_ASSIGN_AUCTION:
            self.auctionMediator = mediator

    def onGetInitTeamBagItem(self, *arg):
        ret = self.movie.CreateArray()
        i = 0
        for pos, it in enumerate(self.teamBag):
            if it == const.CONT_EMPTY_VAL:
                continue
            arr = self.movie.CreateArray()
            obj = uiUtils.dict2GfxDict(uiUtils.getGfxItem(it))
            arr.SetElement(0, GfxValue(pos))
            arr.SetElement(1, obj)
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(it.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            if hasattr(it, 'cdura'):
                if it.cdura == 0:
                    arr.SetElement(2, GfxValue(uiConst.EQUIP_BROKEN))
                else:
                    arr.SetElement(2, GfxValue(uiConst.ITEM_NORMAL))
            else:
                arr.SetElement(2, GfxValue(1))
            arr.SetElement(3, GfxValue(color))
            ret.SetElement(i, arr)
            i += 1

        return ret

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[6:]), int(idItem[4:]))

    def _getKey(self, page, pos):
        return 'assign0.slot%d' % pos

    def onGetTeammateNames(self, *arg):
        keyStr = arg[3][0].GetString()
        _, slot = self.getSlotID(keyStr)
        members = BigWorld.player().members
        ret = self.movie.CreateArray()
        self.teammate = []
        i = 0
        for key, val in members.items():
            if not self.assignTarget[slot]:
                break
            if key in self.assignTarget[slot]:
                self.teammate.append([val['roleName'], key])
                ret.SetElement(i, GfxValue(gbk2unicode(val['roleName'])))
                i += 1

        return ret

    def onAssignItemTo(self, *arg):
        slotIdx = int(arg[3][0].GetNumber())
        teammateIdx = int(arg[3][1].GetNumber())
        item = self.teamBag[slotIdx]
        if not item:
            return
        if teammateIdx >= len(self.teammate):
            return
        self.destName = self.teammate[teammateIdx][0]
        self.destGbId = self.teammate[teammateIdx][1]
        self.destItem = item
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ASSIGN_CONFIRM)

    def onGetAssignBtnEnable(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.groupHeader == p.id)

    def onClickTeamBagIcon(self, *arg):
        if self.isTeamBagShow:
            self.closeTeambag()
        else:
            self.showTeambag()

    def onCloseTeamBag(self, *arg):
        self.closeTeambag()

    def onGetPlayerAndItemNames(self, *arg):
        ret = self.movie.CreateArray()
        if not self.destItem:
            return ret
        ret.SetElement(0, GfxValue(gbk2unicode(self.destItem.name)))
        ret.SetElement(1, GfxValue(gbk2unicode(self.destName)))
        if hasattr(self.destItem, 'quality'):
            quality = self.destItem.quality
        else:
            quality = ID.data.get(self.destItem.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('color', '#ffffff')
        ret.SetElement(2, GfxValue(color))
        return ret

    def onConfirmAssign(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_CONFIRM)
        if self.destItem:
            BigWorld.player().cell.allotGroupAward(self.destGbId, self.destItem.uuid)
            if self.mediator:
                self.mediator.Invoke('disableAssignBtn')

    def onCancelAssign(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_CONFIRM)

    def onDiceAll(self, *arg):
        if self.diceBag:
            BigWorld.player().cell.getAllDiceItem(map(lambda x: x[0].uuid, self.diceBag))

    def onGetDiceTips(self, *arg):
        ret = []
        ret.append(SCD.data.get('diceTip', ''))
        ret.append(SCD.data.get('giveUpTip', ''))
        ret.append(SCD.data.get('greedTip', ''))
        return uiUtils.array2GfxAarry(ret, True)

    def onDice(self, *arg):
        itemPos = int(arg[3][0].GetString())
        for item in self.diceBag:
            if itemPos < len(self.diceBag) and item[0].uuid == self.diceBag[itemPos][0].uuid:
                BigWorld.player().cell.diceGroup(item[0].uuid, const.GROUP_DICE_OP_TYPE_NEED)
                break

    def onGiveUp(self, *arg):
        itemPos = int(arg[3][0].GetString())
        for item in self.diceBag:
            if itemPos < len(self.diceBag) and item[0].uuid == self.diceBag[itemPos][0].uuid:
                BigWorld.player().cell.diceGroup(item[0].uuid, const.GROUP_DICE_OP_TYPE_GIVE_UP)
                break

    def onGreed(self, *arg):
        itemPos = int(arg[3][0].GetString())
        for item in self.diceBag:
            if itemPos < len(self.diceBag) and item[0].uuid == self.diceBag[itemPos][0].uuid:
                BigWorld.player().cell.diceGroup(item[0].uuid, const.GROUP_DICE_OP_TYPE_GREEDY)
                break

    def onGetDiceItem(self, *arg):
        self.isDiceShow = True
        ret = self.generateDiceItem()
        return ret

    def onCloseDice(self, *arg):
        isAuto = arg[3][0].GetBool()
        if isAuto:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_ASSIGNPROXY_232, self._doCloseDice)
        else:
            self._doCloseDice()

    def _doCloseDice(self):
        for item in self.diceBag:
            BigWorld.player().cell.diceGroup(item[0].uuid, const.GROUP_DICE_OP_TYPE_GIVE_UP)

        self.diceBag = []
        self.closeDice()

    def generateDiceItem(self):
        p = BigWorld.player()
        ret = self.movie.CreateArray()
        i = 0
        for pos, val in enumerate(self.diceBag):
            it = val[0]
            if it == const.CONT_EMPTY_VAL:
                continue
            passedTime = self._getPassedTime(val[1])
            if passedTime >= const.GROUP_DICE_INTERVAL - 0.5:
                continue
            arr = self.movie.CreateArray()
            obj = uiUtils.dict2GfxDict(uiUtils.getGfxItem(it))
            arr.SetElement(0, obj)
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(it.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            arr.SetElement(1, GfxValue(color))
            arr.SetElement(2, GfxValue(gbk2unicode(it.name)))
            arr.SetElement(3, GfxValue(it.cwrap))
            arr.SetElement(4, GfxValue(pos))
            arr.SetElement(5, GfxValue(self._getPassedTime(val[1])))
            if ID.data[it.id].has_key('schReq'):
                canUse = p.realSchool in ID.data[it.id]['schReq']
            else:
                canUse = True
            arr.SetElement(6, GfxValue(canUse))
            arr.SetElement(7, GfxValue(i))
            ret.SetElement(i, arr)
            i += 1

        return ret

    def showTeambag(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ASSIGN_TEAMBAG)
        self.isTeamBagShow = True

    def closeTeambag(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_TEAMBAG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_CONFIRM)
        self.isTeamBagShow = False
        self.mediator = None

    def showDice(self, item, isOk, pickTime):
        if isOk:
            if [item, pickTime] not in self.diceBag:
                self.diceBag.append([item, pickTime])
        else:
            for it in self.diceBag:
                if it[0].uuid == item:
                    self.diceBag.remove(it)
                    break

        if self.isDiceShow:
            self.refreshDiceItem()
        elif len(self.diceBag):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ASSIGN_DICE)
        else:
            self.closeDice()

    def closeDice(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_DICE)
        self.isDiceShow = False
        self.diceMediator = None

    def showAuction(self):
        if self.auctionMediator:
            self.refreshAuctionInfo()
        elif len(self.auctionBag):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ASSIGN_AUCTION)
        BigWorld.player().justShowCipher()

    def updateAuctionBag(self, item, isOk):
        if isOk:
            if item not in self.auctionBag:
                self.auctionBag.append(item)
        else:
            for it in self.auctionBag:
                if it.uuid == item:
                    self.auctionBag.remove(it)
                    break

            self.setAuctionState('', 0, True)
        if len(self.auctionBag):
            if self.curAuctionUUID != self.auctionBag[0].uuid:
                self.curGiveUp = False
                self.auctionStep = 0
                self.curAuctionPrice = 0
                self.setBtnEnabled(True)
            self.curAuctionUUID = self.auctionBag[0].uuid
            self.showAuction()
        else:
            self.closeAuction()

    def closeAuction(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ASSIGN_AUCTION)
        self.auctionMediator = None

    def setItem(self, item, page, pos):
        if not item:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None):
                data = self.uiAdapter.movie.CreateObject()
                data = uiUtils.dict2GfxDict(uiUtils.getGfxItem(item))
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 1)
                if hasattr(item, 'cdura'):
                    if item.cdura == 0:
                        self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_BROKEN))
                    else:
                        self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(data)
            return

    def removeItem(self, page, pos):
        key = self._getKey(0, pos)
        if self.binding.get(key, None):
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def refreshDiceItem(self):
        if self.diceMediator != None:
            if len(self.diceBag) == 0:
                self.closeDice()
            else:
                self.diceMediator.Invoke('setItem', self.generateDiceItem())

    def updateTeamBag(self, item, isOk, owner):
        if isOk:
            self.owner = owner
            for i, it in enumerate(self.teamBag):
                if it == const.CONT_EMPTY_VAL:
                    self.teamBag[i] = item
                    self.assignTarget[i] = owner
                    self.setItem(item, 0, i)
                    break

        else:
            for i, it in enumerate(self.teamBag):
                if it and it.uuid == item:
                    self.teamBag[i] = const.CONT_EMPTY_VAL
                    self.assignTarget[i] = None
                    if i == self.selectPos:
                        self.selectPos = None
                    self.destItem = const.CONT_EMPTY_VAL
                    self.removeItem(0, i)
                    break

        gameglobal.rds.ui.teamComm.setAssignInfo()

    def reset(self):
        self.teamBag = [const.CONT_EMPTY_VAL] * const.GROUP_PICK_MAX
        self.assignTarget = [None] * const.GROUP_PICK_MAX
        self.diceBag = []
        self.auctionBag = []
        self.isTeamBagShow = False
        self.isDiceShow = False
        self.selectPos = None
        self.mediator = None
        self.diceMediator = None
        self.auctionMediator = None

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bag, itemSlot = self.getSlotID(key)
        self.selectPos = itemSlot
        if bag == uiConst.ASSIGN_MODE_LEADER and itemSlot < len(self.teamBag):
            i = self.teamBag[itemSlot]
        elif bag == uiConst.ASSIGN_MODE_DICE and itemSlot < len(self.diceBag):
            i = self.diceBag[itemSlot][0]
        elif bag == uiConst.ASSIGN_MODE_AUCTION and itemSlot < len(self.auctionBag):
            i = self.auctionBag[itemSlot]
        else:
            i = None
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def _getPassedTime(self, val):
        return BigWorld.player().getServerTime() - val

    def refreshAssignBtn(self, enabled):
        if self.mediator != None:
            self.mediator.Invoke('setAssignBtnEnabled', GfxValue(enabled))

    def onNotifySlotUse(self, *arg):
        pass

    def isTeamBagEmpty(self):
        for it in self.teamBag:
            if it != const.CONT_EMPTY_VAL:
                return False

        return True

    def clearWidget(self):
        self.closeDice()
        self.closeTeambag()

    def refreshTeamInfo(self):
        if self.mediator:
            self.mediator.Invoke('refreshTeamInfo')

    def onGetTeamInfo(self, *arg):
        p = BigWorld.player()
        ret = []
        self.teammate = []
        itemIdx = self.getSlotID(arg[3][0].GetString())[1]
        if p.isInTeam():
            for key, value in p.members.items():
                if self.assignTarget[itemIdx] and key in self.assignTarget[itemIdx]:
                    rolename = utils.getRealRoleName(value['roleName'])
                    self.teammate.append([rolename, key])
                    ret.append([value['school'], rolename, value['isOn']])

        else:
            idx = int(arg[3][1].GetNumber())
            members = uiUtils.recoverArrange(getattr(p, 'arrangeDict', {}))
            if members and self.assignTarget[itemIdx]:
                for i in xrange(5):
                    gbId = members[idx * 5 + i]
                    if not gbId or gbId not in self.assignTarget[itemIdx]:
                        continue
                    value = p.members[gbId]
                    rolename = utils.getRealRoleName(value['roleName'])
                    self.teammate.append([rolename, gbId])
                    ret.append([value['school'], rolename, value['isOn']])

        return uiUtils.array2GfxAarry(ret, True)

    def onGetTeamState(self, *arg):
        teamState = []
        for i in xrange(10):
            teamState.append(self.isTeamEmpty(i))

        return uiUtils.array2GfxAarry(teamState)

    def isTeamEmpty(self, idx):
        p = BigWorld.player()
        members = uiUtils.recoverArrange(getattr(p, 'arrangeDict', {}))
        if members:
            for i in xrange(5):
                gbId = members[idx * 5 + i]
                if gbId:
                    return False

        return True

    def onIsInTeam(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.isInTeam())

    @ui.checkInventoryLock()
    def onAuction(self, *arg):
        if len(self.auctionBag) == 0:
            return
        if not self.auctionMediator:
            return
        uuid = self.auctionBag[0].uuid
        price = int(arg[3][0].GetString())
        BigWorld.player().cell.biddingGroup(uuid, price, False, BigWorld.player().cipherOfPerson)

    def onGiveUpAuction(self, *arg):
        if len(self.auctionBag) == 0:
            return
        uuid = self.auctionBag[0].uuid
        BigWorld.player().cell.biddingGroup(uuid, 0, True, BigWorld.player().cipherOfPerson)
        self.curGiveUp = True

    def onGetAuctionInfo(self, *arg):
        ret = self.createAuctionInfo()
        return ret

    def onPauseAuction(self, *arg):
        pause = arg[3][0].GetBool()
        BigWorld.player().cell.suspendGroupAuction(pause)

    def refreshAuctionInfo(self):
        if len(self.auctionBag):
            if self.auctionMediator:
                self.auctionMediator.Invoke('setAuctionInfo', self.createAuctionInfo(True))
        else:
            self.closeAuction()

    def createAuctionInfo(self, isRefresh = False):
        p = BigWorld.player()
        ret = {}
        ret['isLeader'] = p.isTeamLeader()
        ret['isRefresh'] = isRefresh
        ret['item'] = []
        ret['cash'] = getattr(p, 'cash', 0)
        ret['curPrice'] = self.curAuctionPrice
        ret['curPlayer'] = self.curAuctionPlayer
        ret['interval'] = self.getAuctionInterval()
        ret['protect'] = SCD.data.get('groupAuctionProtect', 1)
        for item in self.auctionBag:
            itemData = ID.data.get(item.id, {})
            iconPath = uiUtils.getItemIconFile64(item.id)
            count = item.cwrap
            name = itemData.get('name', '')
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = itemData.get('quality', 1)
            fontColor = FCD.data.get(('item', quality), {})
            qualitycolor = fontColor.get('color', '#ffffff')
            color = uiUtils.getItemColor(item.id)
            money = self._getMinAuctionPrice(item.id)
            ret['item'].append({'iconPath': iconPath,
             'count': count,
             'name': name,
             'money': money,
             'itemId': item.id,
             'color': color,
             'qualitycolor': qualitycolor})

        return uiUtils.dict2GfxDict(ret, True)

    def startAuction(self):
        if self.auctionMediator:
            self.auctionMediator.Invoke('startAuction')

    def stopAuction(self):
        if self.auctionMediator:
            self.auctionMediator.Invoke('stopAuction')

    def setAuctionState(self, roleName, price, reset = False, btnEnabled = True):
        p = BigWorld.player()
        self.curAuctionPrice = price
        self.curAuctionPlayer = roleName
        btnEnabled = btnEnabled and not self.curGiveUp
        if self.auctionMediator:
            self.auctionMediator.Invoke('setAuctionState', (GfxValue(gbk2unicode(roleName)),
             GfxValue(price),
             GfxValue(reset),
             GfxValue(btnEnabled),
             GfxValue(p.cash)))

    def setBtnEnabled(self, btnEnabled = True):
        if self.auctionMediator:
            self.auctionMediator.Invoke('setBtnEnabled', GfxValue(btnEnabled))

    def _getMinAuctionPrice(self, itemId):
        return ID.data.get(itemId, {}).get('auctionPrice', 1)

    def setAuctionEnabled(self):
        if self.auctionMediator:
            price = self.curAuctionPrice
            if price == 0:
                price = self._getMinAuctionPrice(self.auctionBag[0].id) * getattr(self.auctionBag[0], 'cwrap', 1)
            else:
                price += max(1, price * 0.1)
            self.auctionMediator.Invoke('checkCanAuction', (GfxValue(BigWorld.player().cash), GfxValue(price)))

    def getAuctionInterval(self):
        times = SCD.data.get('groupAuctionInterval', {0: 20,
         1: 15})
        return times.get(self.auctionStep, 10)

    def setMaxAuctionTime(self):
        self.auctionStep += 1
        ret = self.getAuctionInterval()
        protect = SCD.data.get('groupAuctionProtect', 1)
        if self.auctionMediator:
            self.auctionMediator.Invoke('setMaxAuctionTime', (GfxValue(ret), GfxValue(protect)))

    def onGetAuctionHotKey(self, *arg):
        ret = [hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CONFIRM, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CANCEL, False)]
        return uiUtils.array2GfxAarry(ret, True)

    def onGetDiceHotKey(self, *arg):
        ret = [hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CONFIRM, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_GREED, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CANCEL, False)]
        return uiUtils.array2GfxAarry(ret, True)

    def setAuctionHotKey(self, *arg):
        ret = [hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CONFIRM, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CANCEL, False)]
        if self.auctionMediator:
            self.auctionMediator.Invoke('setAuctionHotKey', uiUtils.array2GfxAarry(ret, True))

    def setDiceHotKey(self, *arg):
        ret = [hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CONFIRM, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_GREED, False), hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_ASSIGN_CANCEL, False)]
        if self.diceMediator:
            self.diceMediator.Invoke('setDiceHotKey', uiUtils.array2GfxAarry(ret, True))

    def getAuctionItemById(self, itemId):
        ret = None
        for item in self.auctionBag:
            if item and item.id == itemId:
                ret = item
                break

        if not ret:
            ret = Item(itemId)
        return ret

    def _createDiceWay(self):
        p = BigWorld.player()
        ret = DICE_BY_SCHOOL
        if p.groupAssignWay == const.GROUP_ASSIGN_DICE:
            ret = DICE_IGNORE_SCHOOL
        elif p.groupAssignWay == const.GROUP_ASSIGN_DICE_JOB:
            ret = DICE_BY_SCHOOL
        return ret

    def onGetDiceWay(self, *arg):
        ret = self._createDiceWay()
        return GfxValue(ret)

    def refreshDicePanel(self):
        if self.diceMediator:
            self.diceMediator.Invoke('refreshPanel', GfxValue(self._createDiceWay()))

    def onGetAssignWay(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.groupAssignWay)
