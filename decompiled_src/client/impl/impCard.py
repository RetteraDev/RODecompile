#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCard.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import utils
import copy
import formula
from card import Card
from data import item_data as ID
from data import base_card_data as BCD
from data import sys_config_data as SCD
from data import map_config_data as MCD
from data import card_wash_group_data as CWGD
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD

class ImpCard(object):
    """
    \xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe6\x8f\x90\xe4\xbe\x9b\xe7\x9a\x84\xe7\x9b\xb8\xe5\x85\xb3\xe6\x95\xb0\xe6\x8d\xae\xe5\x92\x8c\xe6\x8e\xa5\xe5\x8f\xa3\xe8\xaf\xb4\xe6\x98\x8e\xef\xbc\x9a
    
    \xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\x9a\x84\xe5\x8d\xa1\xe7\x89\x8c\xe6\x95\xb0\xe6\x8d\xae\xe6\x89\x80\xe6\x9c\x89\xe9\x83\xbd\xe5\xad\x98\xe5\x9c\xa8\xe4\xb8\x80\xe4\xb8\xaacardBag\xe7\x9a\x84\xe5\xad\x97\xe5\x85\xb8\xe9\x87\x8c\xe9\x9d\xa2\xef\xbc\x8c\xe7\x8e\xa9\xe5\xae\xb6\xe5\xae\x8c\xe6\x88\x90\xe7\x99\xbb\xe5\xbd\x95\xe5\x90\x8e\xe5\xb7\xb2\xe7\xbb\x8f\xe5\x90\x8c\xe6\xad\xa5\xe4\xba\x86\xe6\x95\xb0\xe6\x8d\xae,\xe5\xaf\xb9\xe5\x8d\xa1\xe7\x89\x8c\xe8\x83\x8c\xe5\x8c\x85\xe7\x9a\x84\xe5\xb0\x81\xe8\xa3\x85\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\xa0\xb9\xe6\x8d\xae\xe8\x87\xaa\xe8\xba\xab\xe9\x9c\x80\xe8\xa6\x81\xe5\xb0\x81\xe8\xa3\x85
    cardBag =
    {
        fragmentCnt = 0  # \xe7\xa2\x8e\xe7\x89\x87\xe4\xb8\xaa\xe6\x95\xb0
        cardDict = {}  # \xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaacard\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe5\xad\x97\xe5\x85\xb8,\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x92\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\x90\x84\xe6\x9c\x89\xe4\xb8\x80\xe4\xb8\xaacard\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\xa7\xe6\x89\xbf\xe4\xb8\x8ecommonCard\xef\xbc\x8c
                            \xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe9\x9c\x80\xe8\xa6\x81\xe7\x9a\x84\xe6\xa3\x80\xe6\x9f\xa5\xe5\x92\x8c\xe7\x9b\xb8\xe5\x85\xb3\xe5\xad\x97\xe6\xae\xb5\xe5\xbe\x80\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\x9a\x84card\xe9\x87\x8c\xe5\x8a\xa0\xef\xbc\x8c\xe5\xa6\x82\xe6\x9e\x9c\xe9\x9c\x80\xe8\xa6\x81\xe6\x94\xb9\xe5\x88\xb0commonCard\xe8\xaf\xb7\xe7\xa1\xae\xe8\xae\xa4\xe4\xb8\x8d\xe4\xbc\x9a\xe5\xbd\xb1\xe5\x93\x8d\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf
        cardSlots = [0] * (const.CARD_OPEN_SLOT_COUNT + 1)  # \xe5\x8d\xa1\xe6\xa7\xbd\xe9\x87\x8c\xe9\x9d\xa2\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84\xe5\x8d\xa1\xe7\x89\x8cId\xef\xbc\x8c\xe5\x8d\xa1\xe6\xa7\xbd\xe6\x98\xaf\xe4\xbb\x8e1\xe5\xbc\x80\xe5\xa7\x8b\xe7\x9a\x84\xef\xbc\x8c0\xe4\xbd\x9c\xe4\xb8\xba\xe5\xa4\x9a\xe4\xbd\x99\xe5\xad\x97\xe6\xae\xb5
    }
    """

    def initCardBag(self, cardDatas):
        gamelog.debug('@zq#card initCardBag', cardDatas)
        if not cardDatas:
            cardDatas = {}
        if not hasattr(self, 'allCardBags'):
            self.allCardBags = {}
        tempId = cardDatas.get('tempId', 0)
        self.allCardBags.setdefault(tempId, {})
        self.appendCardBagInfo(self.allCardBags[tempId], cardDatas)

    @property
    def cardBag(self):
        return self.allCardBags[0]

    def appendCardBagInfo(self, cardBag, cardDatas):
        tempId = cardDatas.get('tempId', 0)
        cardBag['school'] = cardDatas.get('school', 0) if tempId else self.school
        cardBag['fragment'] = cardDatas.get('fragment', {})
        if cardBag['fragment'] == None:
            cardBag['fragment'] = {}
        cardBag['fragment'].setdefault(const.CARD_PROP_TYPE_PVE, 0)
        cardBag['fragment'].setdefault(const.CARD_PROP_TYPE_PVP, 0)
        cardBag['cardWashPoint'] = cardDatas.get('cardWashPoint', {})
        cardBag['equipSlot'] = cardDatas.get('equipSlot', 0)
        cards = cardDatas.get('cards', {})
        slotNums = cardDatas.get('cardSlots', {})
        cardBag['slotNum'] = {}
        cardBag['equipSuit'] = {}
        for numData in slotNums:
            num = numData.get('slotNum', 0)
            slot = numData.get('id', 0)
            cardBag['slotNum'][slot] = num
            suitId = numData.get('suitId', 0)
            suitRank = numData.get('suitRank', 0)
            cardBag['equipSuit'][slot] = (suitId, suitRank)

        cardAwards = cardDatas.get('cardAwards', {})
        cardBag['cardAwards'] = cardAwards
        cardBag['cardDict'] = {}
        cardBag['cardSlots'] = {}
        for data in cards:
            card = Card(data['id'], data['actived'], data['progress'], data['advanceLv'], data['slot'])
            card.washProps = data['washProps']
            card.washPropsEx = data['washPropsEx']
            card.newWashProps = data['newWashProps']
            card.lastDelWashTime = data['lastDelWashTime']
            card.washTime = data['washTime']
            card.washNum = data['washNum']
            card.dueTime = data['dueTime']
            card.notValid = data['notValid']
            card.washIndex = data['washIndex']
            card.washSchemeLock = data['washSchemeLock']
            cardBag['cardDict'][card.id] = card
            for slotId in card.slot:
                cardBag['cardSlots'][slotId] = card.id

        cardBag['specialProp'] = cardDatas.get('specialProp', {})
        if cardBag['specialProp'].get('addCardRank', None):
            for cardId, addAdvanceLv in cardBag['specialProp']['addCardRank'].iteritems():
                card = self.getCard(cardId, tempId=tempId)
                if card:
                    card.addAdvanceLv = addAdvanceLv

        gameglobal.rds.ui.cardSystem.init()

    def getCard(self, cardId, createNoActive = False, tempId = 0):
        cardBag = self.allCardBags.get(tempId, {})
        if not cardBag:
            return
        else:
            card = cardBag['cardDict'].get(cardId, None)
            if card:
                return card
            if not createNoActive:
                return
            cardConfig = BCD.data.get(cardId)
            if not cardConfig:
                gamelog.error('@hxm data not configured in card_data!! %d' % cardId)
                return
            card = Card(cardId, False)
            cardBag['cardDict'][cardId] = card
            return card

    def onCompoundCard(self, cardId, costFragment, param):
        gamelog.debug('@zq#card onCompoundCard', cardId, costFragment)
        card = self.getCard(cardId, True)
        if not card:
            gamelog.error('onCompoundCard error')
            return
        card.compound(bool(costFragment))
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        if param == const.CARD_COMPOUND_TYPE_REPLACE:
            gameglobal.rds.ui.cardSlot.onCompoundCard(cardId, costFragment, param)

    def onDecomposeCard(self, cardId, gainFragment):
        gamelog.debug('@zq#card onDecomposeCard', cardId, gainFragment)
        card = self.getCard(cardId)
        if not card:
            gamelog.error('onDecomposeCard error')
            return
        unfixSlotIds = []
        for slotId in card.slot:
            if self.cardBag['cardSlots'][slotId] == cardId:
                unfixSlotIds.append(slotId)
                self.cardBag['cardSlots'][slotId] = 0

        for slotId in unfixSlotIds:
            card.unfixFromSlot(slotId)

        card.decompose()
        self.cardBag['fragment'][card.propType] += gainFragment
        self.onChangeFragmentCnt(card.propType, self.cardBag['fragment'][card.propType], gainFragment)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        self.reCalcBuffListenerIds()

    def onUpgradeCardProgress(self, cardId, inc, costFragment):
        gamelog.debug('@zq#card onUpgradeCardProgress', cardId, inc, costFragment)
        card = self.getCard(cardId)
        if not card:
            gamelog.error('onUpgradeCardProgress error')
            return
        card.upgradeProgress(inc)
        self.cardBag['fragment'][card.propType] -= costFragment
        self.onChangeFragmentCnt(card.propType, self.cardBag['fragment'][card.propType], -costFragment)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()

    def onDegradeCardProgress(self, cardId, dec, gainFragment):
        gamelog.debug('@zq#card onDegradeCardProgress', cardId, dec, gainFragment)
        card = self.getCard(cardId)
        if not card:
            gamelog.error('onDegradeCardProgress error')
            return
        card.degradeProgress(dec)
        self.cardBag['fragment'][card.propType] += gainFragment
        self.onChangeFragmentCnt(card.propType, self.cardBag['fragment'][card.propType], gainFragment)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        self.reCalcBuffListenerIds()

    def onAdvanceCard(self, cardId):
        gamelog.debug('@zq#card onAdvanceCard', cardId)
        card = self.getCard(cardId)
        if not card:
            gamelog.error('onAdvanceCard error')
            return
        preCard = copy.deepcopy(card)
        card.advance()
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        if not preCard.isBreakRank and card.isBreakRank:
            gameglobal.rds.ui.cardMake.showCardAnim(preCard, card)

    def onChangeFragmentCnt(self, tp, cur, change, args = {}):
        gamelog.debug('@zq#card onChangeFragmentCnt', tp, cur, change, args)
        self.cardBag['fragment'][tp] = cur
        if change > 0:
            itemId = args.get('itemId', 0)
            CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
            fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(tp, '')
            if not itemId:
                self.showGameMsg(GMDD.data.GET_CARD_FRAGMENT, (fragmentName, change))
            else:
                cardId = CID.data.get(itemId, {}).get('cardId', 0)
                itemName = ID.data.get(itemId, {}).get('name', '')
                cardObj = self.getCard(cardId, True)
                if cardObj:
                    if cardObj.isBreakRank:
                        self.showGameMsg(GMDD.data.CARD_DECOMPOSE_RANK4, (itemName,
                         itemName,
                         fragmentName,
                         change))
                    else:
                        self.showGameMsg(GMDD.data.CARD_DECOMPOSE, (itemName, fragmentName, change))
        gameglobal.rds.ui.cardSystem.refreshCurCardList()

    def onChangeWashPoint(self, tp, cur, change):
        gamelog.debug('@zq#card onChangeWashPoint', tp, cur, change)
        self.cardBag['cardWashPoint'][tp] = cur
        gameglobal.rds.ui.cardChange.refreshRightInfo()

    def onSetEquipSlot(self, oldEquipSlot, newEquipSlot):
        self.cardBag['equipSlot'] = newEquipSlot
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardSlot.refreshSlotList()

    def onFixCardToSlot(self, cardId, slot):
        gamelog.debug('@zq#card onFixCardToSlot', cardId, slot)
        card = self.getCard(cardId)
        sType, slotIndex = gameglobal.rds.ui.cardSystem.parseSlotId(slot)
        for slotId in card.slot:
            _sType, _slotIndex = gameglobal.rds.ui.cardSystem.parseSlotId(slotId)
            if _sType == sType:
                self.onUnfixCardFromSlot(slotId)

        self.cardBag['cardSlots'][slot] = cardId
        card.fixToSlot(slot)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardSlot.refreshSlotList()
        gameglobal.rds.ui.cardSlot.autoSelectEmptySlot()

    def onReplaceSlotCard(self, cardId, slot):
        gamelog.debug('@zq#card onReplaceSlotCard', cardId, slot)
        oldCardId = self.cardBag['cardSlots'][slot]
        oldCard = self.getCard(oldCardId)
        card = self.getCard(cardId)
        self.cardBag['cardSlots'][slot] = cardId
        oldCard.unfixFromSlot(slot)
        card.fixToSlot(slot)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardSlot.refreshSlotList()

    def onUnfixCardFromSlot(self, slot):
        gamelog.debug('@zq#card onUnfixCardFromSlot', slot)
        cardId = self.cardBag['cardSlots'].get(slot, 0)
        self.cardBag['cardSlots'][slot] = 0
        card = self.getCard(cardId, True)
        if not card:
            gamelog.error('onUnfixCardFromSlot error')
            return
        card.unfixFromSlot(slot)
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardSlot.refreshSlotList()
        self.reCalcBuffListenerIds()

    def onWashCard(self, cardId, props, washTime, washNum):
        gamelog.debug('@zq#card onWashCard', cardId, props, washTime, washNum)
        card = self.getCard(cardId, True)
        if card:
            card.newWashProps = props
            card.washTime = washTime
            card.washNum = washNum
        gameglobal.rds.ui.cardChange.refreshInfo()

    def onConfirmWashCard(self, cardId, props, schemeSelect):
        gamelog.debug('@zq#card onConfirmWashCard', cardId, props)
        card = self.getCard(cardId, True)
        if card:
            if schemeSelect:
                card.washPropsEx = props
            else:
                card.washProps = props
            card.newWashProps = {}
        gameglobal.rds.ui.cardChange.refreshInfo()
        self.reCalcBuffListenerIds()

    def onDelWashCard(self, cardId, lastDelWashTime):
        gamelog.debug('@zq#card onDelWashCard', cardId, lastDelWashTime)
        card = self.getCard(cardId, True)
        if card:
            card.washProps = {}
            card.washPropsEx = {}
            card.newWashProps = {}
            card.lastDelWashTime = lastDelWashTime
        gameglobal.rds.ui.cardChange.refreshInfo()
        self.reCalcBuffListenerIds()

    def onGetCardAward(self, awardType, rank, oldRank):
        gamelog.debug('@zq#card onGetCardAward', awardType, rank, oldRank)
        self.cardBag['cardAwards'][awardType] = rank
        gameglobal.rds.ui.cardRankReward.refreshInfo()
        gameglobal.rds.ui.cardRewardReceived.refreshInfo()
        gameglobal.rds.ui.cardCollection.refreshRewardPoint()

    def getSlotId(self, id):
        for slotId, cardId in enumerate(self.cardBag['cardSlots'].iteritems()):
            if id == cardId:
                return slotId

        return 0

    def onSyncCardInfo(self, info):
        gamelog.debug('@zq card onSyncCardInfo', info)
        updateInfo = info.get('updateInfo', {})
        delList = info.get('delList', [])
        for cardId, data in updateInfo.iteritems():
            card = self.cardBag['cardDict'].get(cardId)
            if not card:
                slotId = data.get('slotId', [])
                card = Card(cardId, data.get('actived', False), data.get('progress', 0), data.get('advanceLv', 0), slotId)
                if slotId:
                    self.cardBag['cardSlots'][slotId] = card.id
            else:
                oldSlotId = self.getSlotId(card.id)
                for attrName, attrVal in data.iteritems():
                    if hasattr(card, attrName) and attrVal is not None:
                        setattr(card, attrName, attrVal)

                slotId = self.getSlotId(card.id)
                if oldSlotId != slotId:
                    self.cardBag['cardSlots'][oldSlotId] = 0
                    self.cardBag['cardSlots'][slotId] = card.id

        for cardId in delList:
            if self.cardBag['cardDict'].has_key(cardId):
                self.cardBag['cardDict'][cardId] = Card(cardId, False)

    def onCardSpecialPropChanged(self, seId, cardId, newVal, changeVal):
        gamelog.debug('@zq card onCardSpecialPropChanged', seId, cardId, newVal, changeVal)
        if seId == gametypes.CARD_SE_CARD_ADVANCE_LEVEL_REDUCE:
            self.cardBag['specialProp']['reduceAdvanceLevel'][cardId] = newVal
        elif seId == gametypes.CARD_SE_CARD_RANK_ADD_NEED_EQUIP or seId == gametypes.CARD_SE_CARD_RANK_ADD_NO_EQUIP:
            card = self.getCard(cardId)
            if card:
                card.addAdvanceLv = newVal

    def onCardSpecialPropClear(self):
        self.cardBag['specialProp']['reduceAdvanceLevel'].clear()
        for card in self.cardBag['cardDict'].itervalues():
            if card.addAdvanceLv != 0:
                card.addAdvanceLv = 0

    def calcCardSummonedAccessoryProp(self):
        equipSlot = self.cardBag.get('equipSlot', 0)
        slotNum = self.cardBag.get('slotNum', {}).get(equipSlot, 0)
        allPropAddDict = {}

        def _calc(mCard):
            addDict = {}
            washProps = mCard.washProps
            for k, v in washProps.iteritems():
                if not mCard.isBreakRank:
                    break
                washGroupId = v.get('washGroupId', 0)
                sequence = k
                stage = v.get('stage', 0)
                sType = v.get('sType', 0)
                sId = v.get('sId', 0)
                sNum = v.get('sNum', 0)
                if sType == const.CARD_PROP_TYPE_SPECIAL:
                    wData = CWGD.data.get((washGroupId,
                     sequence,
                     stage,
                     sType,
                     sId), {})
                    seParam = wData.get('seParam', ())
                    if isinstance(sId, tuple) and len(sId) and sId[0] == gametypes.CARD_SE_SUMMON_SPRITE_ACCESSORY_ENH_BY_POS:
                        validParts, val = seParam
                        for part in validParts:
                            addDict.setdefault(part, 0)
                            addDict[part] += val

            return addDict

        for i in xrange(0, slotNum):
            slotId = equipSlot * const.CARD_SLOT_DIV_NUM + i + 1
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            slotCard = self.getCard(slotCardId)
            if slotCard:
                propAddDict = _calc(slotCard)
                for k, v in propAddDict.iteritems():
                    allPropAddDict.setdefault(k, 0)
                    allPropAddDict[k] += v

        return allPropAddDict

    def isBaseCardSysOpen(self):
        return self.lv >= SCD.data.get('cardBaseFuncOpenLevel', 0)

    def isAdvanceCardSysOpen(self, opTypes):
        if not self.isBaseCardSysOpen():
            return False
        elif type(opTypes) in (tuple, list):
            for opType in opTypes:
                events = formula.getAdvanceCardEvents(opType)
                for serverProgressMsId in events:
                    if self.checkServerProgress(serverProgressMsId, False, extra=True):
                        return True

            return False
        else:
            events = formula.getAdvanceCardEvents(opTypes)
            for serverProgressMsId in events:
                if self.checkServerProgress(serverProgressMsId, False, extra=True):
                    return True

            return False

    def cardPrepareCacheScore(self):
        pass

    def getCardSceneType(self):
        mapId = formula.getMapId(self.spaceNo)
        sceneType = MCD.data.get(mapId, {}).get('cardSceneType', 0)
        return sceneType

    def onSetCardSlotSuit(self, slotId, suitId, suitRank):
        self._updateSelSuitData(slotId, suitId, suitRank)

    def onUpdateCardSuit(self, slotId, suitId, suitRank):
        self._updateSelSuitData(slotId, suitId, suitRank)

    def _updateSelSuitData(self, slotId, suitId, suitRank):
        p = BigWorld.player()
        self.cardBag['equipSuit'][slotId] = (suitId, suitRank)
        gameglobal.rds.ui.cardSlot.refreshCurSuitMenu()
        gameglobal.rds.ui.cardSlot.refreshPropertyList()
        gameglobal.rds.ui.cardSlot.refreshResonancePanel()
        p.reCalcBuffListenerIds()

    def onValidateCard(self, cardId, dueTime):
        card = self.getCard(cardId, True)
        if card:
            card.notValid = False
            card.dueTime = dueTime
        gameglobal.rds.ui.cardSystem.refreshCurCardList()

    def onInvalidateCard(self, cardId, dueTime):
        card = self.getCard(cardId, True)
        if card:
            card.notValid = True
            card.dueTime = dueTime
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        self.reCalcBuffListenerIds()

    def onAddCardDuration(self, cardId, dueTime, dueTimeDelta):
        card = self.getCard(cardId, True)
        if card:
            card.dueTime = dueTime
        gameglobal.rds.ui.cardSystem.refreshCurCardList()

    def onUnlockCardSlot(self, slotVal, slotNum):
        """
        \xe8\xa7\xa3\xe9\x94\x81\xe5\xb9\xbb\xe5\x8c\xa3\xe6\xa7\xbd\xe4\xbd\x8d
        :param slotVal: \xe5\xb9\xbb\xe5\x8c\xa3id * 1000 + \xe6\xa7\xbd\xe4\xbd\x8did
        :param slotNum: \xe5\xbd\x93\xe5\x89\x8d\xe8\xa7\xa3\xe9\x94\x81\xe5\x88\xb0\xe7\x9a\x84\xe6\xa7\xbd\xe4\xbd\x8d
        :return:
        """
        sType, slotIndex = gameglobal.rds.ui.cardSystem.parseSlotId(slotVal)
        self.cardBag['slotNum'][sType] = slotNum
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardSlot.refreshSlotList()

    def onChangeCardWashScheme(self, cardId, oldScheme, newScheme):
        card = self.getCard(cardId)
        if card:
            card.washIndex = newScheme
        gameglobal.rds.ui.cardSystem.refreshCurCardList()
        gameglobal.rds.ui.cardChange.refreshRightInfo()
        gameglobal.rds.ui.cardChange.refreshLeftDetailMc()

    def onUnlockWashScheme(self, cardId, scheme):
        card = self.getCard(cardId)
        if card:
            card.washSchemeLock = scheme
        self.base.changeCardWashScheme(cardId, scheme)

    def updateCardWashNum(self, cardId, washNum):
        card = self.getCard(cardId)
        if card:
            card.washNum = washNum

    def onAutoWashCard(self, cardId, props, washTime, washNum, result):
        gamelog.info('@zzy onAutoWashCard', props, result)

    def stopAutoWashCard(self):
        pass

    def onAutoConfirmWashCard(self, cardId, props, schemeSelect):
        card = self.getCard(cardId, True)
        if card:
            if schemeSelect:
                card.washPropsEx = props
            else:
                card.washProps = props
        gameglobal.rds.ui.cardChange.refreshInfo()
        self.reCalcBuffListenerIds()
