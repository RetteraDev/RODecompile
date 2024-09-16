#Embedded file name: /WORKSPACE/data/entities/common/inventorycommon.o
import const
import gametypes
import BigWorld
from container import Container
from item import Item
from data import consumable_item_data as CID
from data import item_data as ID
COMP_WITHOUT_BIND_POLICY = 0
COMP_WITH_BIND_POLICY = 1
import utils

class InventoryCommon(Container):

    def __init__(self, pageCount, width, height, resKind):
        super(InventoryCommon, self).__init__(pageCount, width, height)
        self.RES_KIND = resKind

    def canTake(self, page):
        return True

    def canGive(self, page):
        return True

    def canUse(self, page):
        return True

    def canEquip(self, page):
        return True

    def searchBestInPages(self, itemId, amount, src = None):
        if amount > Item.maxWrap(itemId):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)
        if not src:
            src = Item(itemId, cwrap=amount, genRandProp=False)
        pages = self.getPageTuple()
        if src.canWrap():
            for pg in pages:
                posCount = self.getPosCount(pg)
                for ps in xrange(posCount):
                    dst = self.getQuickVal(pg, ps)
                    if dst == const.CONT_EMPTY_VAL:
                        continue
                    if dst.id != src.id:
                        continue
                    if dst.overBear(amount):
                        continue
                    if not src.canMerge(src, dst):
                        continue
                    return (pg, ps)

        for pg in pages:
            ps = self.searchEmpty(pg)
            if ps != const.CONT_NO_POS:
                return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def searchBestInPagesWithList--- This code section failed: ---

0	LOAD_GLOBAL       'dict'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'pageAndPosResult'

9	LOAD_GLOBAL       'dict'
12	CALL_FUNCTION_0   None
15	STORE_FAST        'tempPosHasOccucyRecord'

18	SETUP_LOOP        '668'
21	LOAD_FAST         'itemDataList'
24	GET_ITER          None
25	FOR_ITER          '667'
28	STORE_FAST        'itemData'

31	LOAD_FAST         'itemData'
34	LOAD_ATTR         'get'
37	LOAD_CONST        'itemId'
40	LOAD_CONST        0
43	CALL_FUNCTION_2   None
46	STORE_FAST        'itemId'

49	LOAD_FAST         'itemData'
52	LOAD_ATTR         'get'
55	LOAD_CONST        'amount'
58	LOAD_CONST        0
61	CALL_FUNCTION_2   None
64	STORE_FAST        'amount'

67	LOAD_FAST         'itemData'
70	LOAD_ATTR         'get'
73	LOAD_CONST        'uuid'
76	LOAD_CONST        0
79	CALL_FUNCTION_2   None
82	STORE_FAST        'itemUUID'

85	LOAD_FAST         'itemId'
88	UNARY_NOT         None
89	POP_JUMP_IF_TRUE  '25'
92	LOAD_FAST         'amount'
95	UNARY_NOT         None
96	POP_JUMP_IF_TRUE  '25'
99	LOAD_FAST         'itemUUID'
102	UNARY_NOT         None
103_0	COME_FROM         '89'
103_1	COME_FROM         '96'
103	POP_JUMP_IF_FALSE '112'

106	CONTINUE          '25'
109	JUMP_FORWARD      '112'
112_0	COME_FROM         '109'

112	LOAD_FAST         'amount'
115	LOAD_GLOBAL       'Item'
118	LOAD_ATTR         'maxWrap'
121	LOAD_FAST         'itemId'
124	CALL_FUNCTION_1   None
127	COMPARE_OP        '>'
130	POP_JUMP_IF_FALSE '161'

133	LOAD_GLOBAL       'const'
136	LOAD_ATTR         'CONT_NO_PAGE'
139	LOAD_GLOBAL       'const'
142	LOAD_ATTR         'CONT_NO_POS'
145	BUILD_LIST_2      None
148	LOAD_FAST         'pageAndPosResult'
151	LOAD_FAST         'itemUUID'
154	STORE_SUBSCR      None

155	CONTINUE          '25'
158	JUMP_FORWARD      '161'
161_0	COME_FROM         '158'

161	LOAD_GLOBAL       'hasattr'
164	LOAD_FAST         'itemData'
167	LOAD_CONST        'src'
170	CALL_FUNCTION_2   None
173	POP_JUMP_IF_FALSE '197'

176	LOAD_FAST         'itemData'
179	LOAD_ATTR         'get'
182	LOAD_CONST        'src'
185	LOAD_CONST        None
188	CALL_FUNCTION_2   None
191	STORE_FAST        'src'
194	JUMP_FORWARD      '221'

197	LOAD_GLOBAL       'Item'
200	LOAD_FAST         'itemId'
203	LOAD_CONST        'cwrap'
206	LOAD_FAST         'amount'
209	LOAD_CONST        'genRandProp'
212	LOAD_GLOBAL       'False'
215	CALL_FUNCTION_513 None
218	STORE_FAST        'src'
221_0	COME_FROM         '194'

221	LOAD_FAST         'self'
224	LOAD_ATTR         'getPageTuple'
227	CALL_FUNCTION_0   None
230	STORE_FAST        'pages'

233	LOAD_FAST         'src'
236	LOAD_ATTR         'canWrap'
239	CALL_FUNCTION_0   None
242	POP_JUMP_IF_FALSE '472'

245	SETUP_LOOP        '472'
248	LOAD_FAST         'pages'
251	GET_ITER          None
252	FOR_ITER          '468'
255	STORE_FAST        'pg'

258	LOAD_FAST         'self'
261	LOAD_ATTR         'getPosCount'
264	LOAD_FAST         'pg'
267	CALL_FUNCTION_1   None
270	STORE_FAST        'posCount'

273	SETUP_LOOP        '464'
276	LOAD_GLOBAL       'xrange'
279	LOAD_FAST         'posCount'
282	CALL_FUNCTION_1   None
285	GET_ITER          None
286	FOR_ITER          '460'
289	STORE_FAST        'ps'

292	LOAD_FAST         'self'
295	LOAD_ATTR         'getQuickVal'
298	LOAD_FAST         'pg'
301	LOAD_FAST         'ps'
304	CALL_FUNCTION_2   None
307	STORE_FAST        'dst'

310	LOAD_FAST         'dst'
313	LOAD_GLOBAL       'const'
316	LOAD_ATTR         'CONT_EMPTY_VAL'
319	COMPARE_OP        '=='
322	POP_JUMP_IF_FALSE '331'

325	CONTINUE          '286'
328	JUMP_FORWARD      '331'
331_0	COME_FROM         '328'

331	LOAD_FAST         'dst'
334	LOAD_ATTR         'id'
337	LOAD_FAST         'src'
340	LOAD_ATTR         'id'
343	COMPARE_OP        '!='
346	POP_JUMP_IF_FALSE '355'

349	CONTINUE          '286'
352	JUMP_FORWARD      '355'
355_0	COME_FROM         '352'

355	LOAD_FAST         'dst'
358	LOAD_ATTR         'overBear'
361	LOAD_FAST         'amount'
364	CALL_FUNCTION_1   None
367	POP_JUMP_IF_FALSE '376'

370	CONTINUE          '286'
373	JUMP_FORWARD      '376'
376_0	COME_FROM         '373'

376	LOAD_FAST         'src'
379	LOAD_ATTR         'canMerge'
382	LOAD_FAST         'src'
385	LOAD_FAST         'dst'
388	CALL_FUNCTION_2   None
391	POP_JUMP_IF_TRUE  '400'

394	CONTINUE          '286'
397	JUMP_FORWARD      '400'
400_0	COME_FROM         '397'

400	LOAD_FAST         'pg'
403	LOAD_FAST         'ps'
406	BUILD_TUPLE_2     None
409	LOAD_FAST         'tempPosHasOccucyRecord'
412	COMPARE_OP        'in'
415	POP_JUMP_IF_FALSE '424'

418	CONTINUE          '286'
421	JUMP_FORWARD      '424'
424_0	COME_FROM         '421'

424	LOAD_CONST        1
427	LOAD_FAST         'tempPosHasOccucyRecord'
430	LOAD_FAST         'pg'
433	LOAD_FAST         'ps'
436	BUILD_TUPLE_2     None
439	STORE_SUBSCR      None

440	LOAD_FAST         'pg'
443	LOAD_FAST         'ps'
446	BUILD_LIST_2      None
449	LOAD_FAST         'pageAndPosResult'
452	LOAD_FAST         'itemUUID'
455	STORE_SUBSCR      None

456	BREAK_LOOP        None
457	JUMP_BACK         '286'
460	POP_BLOCK         None

461	CONTINUE          '252'
464_0	COME_FROM         '273'

464	BREAK_LOOP        None
465	JUMP_BACK         '252'
468	POP_BLOCK         None
469_0	COME_FROM         '245'
469	JUMP_FORWARD      '472'
472_0	COME_FROM         '469'

472	SETUP_LOOP        '627'
475	LOAD_FAST         'pages'
478	GET_ITER          None
479	FOR_ITER          '626'
482	STORE_FAST        'pg'

485	LOAD_FAST         'self'
488	LOAD_ATTR         'areFill'
491	LOAD_FAST         'pg'
494	CALL_FUNCTION_1   None
497	POP_JUMP_IF_TRUE  '479'

500	LOAD_FAST         'self'
503	LOAD_ATTR         'getPosCount'
506	LOAD_FAST         'pg'
509	CALL_FUNCTION_1   None
512	STORE_FAST        'posCount'

515	SETUP_LOOP        '619'
518	LOAD_GLOBAL       'xrange'
521	LOAD_FAST         'posCount'
524	CALL_FUNCTION_1   None
527	GET_ITER          None
528	FOR_ITER          '615'
531	STORE_FAST        'ps'

534	LOAD_FAST         'self'
537	LOAD_ATTR         'getQuickVal'
540	LOAD_FAST         'pg'
543	LOAD_FAST         'ps'
546	CALL_FUNCTION_2   None
549	POP_JUMP_IF_TRUE  '528'

552	LOAD_FAST         'pg'
555	LOAD_FAST         'ps'
558	BUILD_TUPLE_2     None
561	LOAD_FAST         'tempPosHasOccucyRecord'
564	COMPARE_OP        'in'
567_0	COME_FROM         '549'
567	POP_JUMP_IF_FALSE '576'

570	CONTINUE          '528'
573	JUMP_FORWARD      '576'
576_0	COME_FROM         '573'

576	LOAD_CONST        1
579	LOAD_FAST         'tempPosHasOccucyRecord'
582	LOAD_FAST         'pg'
585	LOAD_FAST         'ps'
588	BUILD_TUPLE_2     None
591	STORE_SUBSCR      None

592	LOAD_FAST         'pg'
595	LOAD_FAST         'ps'
598	BUILD_LIST_2      None
601	LOAD_FAST         'pageAndPosResult'
604	LOAD_FAST         'itemUUID'
607	STORE_SUBSCR      None

608	BREAK_LOOP        None
609	JUMP_BACK         '528'
612	JUMP_BACK         '528'
615	POP_BLOCK         None

616	CONTINUE          '479'
619_0	COME_FROM         '515'

619	BREAK_LOOP        None
620	JUMP_BACK         '479'
623	JUMP_BACK         '479'
626	POP_BLOCK         None
627_0	COME_FROM         '472'

627	LOAD_FAST         'itemUUID'
630	LOAD_FAST         'pageAndPosResult'
633	COMPARE_OP        'not in'
636	POP_JUMP_IF_FALSE '25'

639	LOAD_GLOBAL       'const'
642	LOAD_ATTR         'CONT_NO_PAGE'
645	LOAD_GLOBAL       'const'
648	LOAD_ATTR         'CONT_NO_POS'
651	BUILD_LIST_2      None
654	LOAD_FAST         'pageAndPosResult'
657	LOAD_FAST         'itemUUID'
660	STORE_SUBSCR      None
661	JUMP_BACK         '25'
664	JUMP_BACK         '25'
667	POP_BLOCK         None
668_0	COME_FROM         '18'

668	LOAD_FAST         'pageAndPosResult'
671	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `JUMP_BACK' token at offset 612

    def searchEmptyInPages(self):
        pages = self.getPageTuple()
        for pg in pages:
            dstPos = self.searchEmpty(pg)
            if dstPos != const.CONT_NO_POS:
                return (pg, dstPos)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findItemInPages(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, startPage = 0, startPos = 0, owner = None, commonUseCheck = False):
        for pg, ps in self._searchItemCandidates(itemId, 1, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun, startPage, startPos):
            dst = self.getQuickVal(pg, ps)
            if owner and commonUseCheck and not owner._checkUseItemCommon(dst, owner, True):
                continue
            if dst != const.CONT_EMPTY_VAL:
                return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findAllItemInPages(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, startPage = 0, startPos = 0):
        itemList = []
        for pg, ps in self._searchItemCandidates(itemId, 1, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun, startPage, startPos):
            dst = self.getQuickVal(pg, ps)
            if dst != const.CONT_EMPTY_VAL:
                itemList.append([pg, ps])

        return itemList

    def compClosure(self, compType):

        def compForPassiveUseItem(item1, item2):
            page1, pos1 = item1
            page2, pos2 = item2
            usePriv1 = 0
            usePriv2 = 0
            maxLv1 = const.MAX_LEVEL + 1
            maxLv2 = const.MAX_LEVEL + 1
            it1 = self.getQuickVal(page1, pos1)
            if it1 != const.CONT_EMPTY_VAL:
                maxLv1 = ID.data.get(it1.id, {}).get('maxLvReq', const.MAX_LEVEL + 1)
                usePriv1 = it1.getPassiveUsePriority()
            it2 = self.getQuickVal(page2, pos2)
            if it2 != const.CONT_EMPTY_VAL:
                maxLv2 = ID.data.get(it2.id, {}).get('maxLvReq', const.MAX_LEVEL + 1)
                usePriv2 = it2.getPassiveUsePriority()
            if usePriv1 != usePriv2:
                if usePriv1 > usePriv2:
                    return -1
                return 1
            if maxLv1 != maxLv2:
                if maxLv1 > maxLv2:
                    return 1
                return -1
            conditionsList1 = ID.data.get(it1.id, {}).get('conditionsList')
            conditionsList2 = ID.data.get(it2.id, {}).get('conditionsList')
            if conditionsList1 and conditionsList2:
                condition1 = it1.getCondition(const.CON_SKILL_ENHANC_POINT)
                condition2 = it2.getCondition(const.CON_SKILL_ENHANC_POINT)
                maxLimitTuple1 = (condition1.get('eq'), condition1.get('lt'), condition1.get('lte'))
                maxLimit1, priority1 = (None, None)
                for pos, val in enumerate(maxLimitTuple1):
                    if val:
                        maxLimit1 = val
                        priority1 = pos

                maxLimitTuple2 = (condition2.get('eq'), condition2.get('lt'), condition2.get('lte'))
                maxLimit2, priority2 = (None, None)
                for pos, val in enumerate(maxLimitTuple2):
                    if val:
                        maxLimit2 = val
                        priority2 = pos

                if maxLimit1 != maxLimit2:
                    if maxLimit1 == None:
                        return 1
                    if maxLimit2 == None:
                        return -1
                    if maxLimit1 > maxLimit2:
                        return 1
                    return -1
                if maxLimit1 and maxLimit2:
                    if priority1 != priority2:
                        if priority1 > priority2:
                            return 1
                        return -1
            if compType == COMP_WITH_BIND_POLICY:
                if it1.isForeverBind() and not it2.isForeverBind():
                    return -1
                if not it1.isForeverBind() and it2.isForeverBind():
                    return 1
            expireTime1 = it1.getTTLExpireTime()
            expireTime2 = it2.getTTLExpireTime()
            if expireTime1 and not expireTime2:
                return -1
            if not expireTime1 and expireTime2:
                return 1
            if expireTime1 != expireTime2:
                if expireTime1 > expireTime2:
                    return 1
                return -1
            return 0

        return compForPassiveUseItem

    def findPassiveUseItemByAttr(self, owner, attrs, showMsg = False, messageList = None, skipLatchItem = False, lv = None):
        candidates = []
        pages = self.getPageTuple()
        messageBuf = {}
        for page in pages:
            for pos in self.getPosTuple(page):
                obj = self.getQuickVal(page, pos)
                if obj == const.CONT_EMPTY_VAL:
                    continue
                if skipLatchItem and obj.hasLatch():
                    continue
                if lv != None:
                    itemData = ID.data.get(obj.id, {})
                    if lv < itemData.get('lvReq', 0) or lv > itemData.get('maxLvReq', 99):
                        continue
                if obj.getPassiveUse():
                    flag = True
                    for k, v in attrs.iteritems():
                        if (not hasattr(obj, k) or getattr(obj, k) != v) and (not CID.data.get(obj.id, {}).has_key(k) or CID.data[obj.id][k] != v):
                            flag = False
                            break
                        if BigWorld.component in ('base', 'cell') and not owner._checkUseItemCommon(obj, owner, True, showMsg=False, messageBuf=messageBuf):
                            flag = False
                            break

                    if flag:
                        candidates.append((page, pos))

        candidates.sort(self.compClosure(COMP_WITH_BIND_POLICY))
        if len(candidates) > 0:
            return candidates[0]
        else:
            message = utils.selectUseItemProperMessage(messageBuf)
            if message and messageList is not None:
                messageList.append(message)
            if showMsg and message:
                owner.client and owner.client.showGameMsg(message[0], message[1])
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findItemByUUID(self, uuid):
        pages = self.getPageTuple()
        for page in pages:
            for dstPos in self.getPosTuple(page):
                obj = self.getQuickVal(page, dstPos)
                if obj == const.CONT_EMPTY_VAL:
                    continue
                if obj.uuid != uuid:
                    continue
                else:
                    return (obj, page, dstPos)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findItemByAttr(self, attrs, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST):
        pages = self.getPageTuple()
        tempItems = {}
        for pg in pages:
            ps = 0
            ps = self._searchByAttr(attrs, pg, startPos=ps, bindPolicy=bindPolicy)
            while ps != const.CONT_NO_POS:
                dst = self.getQuickVal(pg, ps)
                if dst.isForeverBind():
                    if dst.isOneMall():
                        tempItems.setdefault(gametypes.ITEM_SHOP_BIND, []).append((pg, ps))
                    else:
                        tempItems.setdefault(gametypes.ITEM_COMMON_BIND, []).append((pg, ps))
                elif dst.isOneMall():
                    tempItems.setdefault(gametypes.ITEM_SHOP_UNBIND, []).append((pg, ps))
                else:
                    tempItems.setdefault(gametypes.ITEM_COMMON_UNBIND, []).append((pg, ps))
                ps += 1
                ps = self._searchByAttr(attrs, pg, startPos=ps, bindPolicy=bindPolicy)

        if bindPolicy == gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST:
            candidates = tempItems.get(gametypes.ITEM_SHOP_UNBIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, []) + tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_BIND, [])
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_ONLY:
            candidates = tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_BIND, [])
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_FIRST:
            candidates = tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_BIND, []) + tempItems.get(gametypes.ITEM_SHOP_UNBIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, [])
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_COMMON_FIRST:
            candidates = tempItems.get(gametypes.ITEM_COMMON_BIND, []) + tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, []) + tempItems.get(gametypes.ITEM_SHOP_UNBIND, [])
        else:
            candidates = tempItems.get(gametypes.ITEM_SHOP_UNBIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, [])
        if candidates:
            return candidates[0]
        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findAllItemByAttr(self, attrs, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST):
        pages = self.getPageTuple()
        result = []
        for pg in pages:
            curPos = 0
            while True:
                ps = self._searchByAttr(attrs, pg, curPos, bindPolicy)
                if ps != const.CONT_NO_POS:
                    result.append((pg, ps))
                    curPos = ps + 1
                else:
                    break

        return result

    def _searchByAttr(self, attrs, page, startPos = 0, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == const.CONT_EMPTY_VAL:
                continue
            if not self._checkBindPolicy(bindPolicy, obj):
                continue
            for k, v in attrs.iteritems():
                if not hasattr(obj, k) or getattr(obj, k) != v:
                    break
            else:
                return dstPos

        return const.CONT_NO_POS

    def getItemHasEnhLv(self, itemId, num = -1, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        cnt = 0
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                cnt += it.cwrap
                if hasattr(it, 'enhLv') and it.enhLv >= 1:
                    return True
                if cnt >= num and num != -1:
                    break

        return False

    def getItemHasValuableTradeItem(self, itemId, num = -1, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        cnt = 0
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                cnt += it.cwrap
                if not utils.checkValuableTradeItem(it):
                    return True
                if cnt >= num and num != -1:
                    break

        return False

    def countItemInPages(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        cnt = 0
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                cnt += it.cwrap

        return cnt

    def countItemListInPages(self, itemList, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        cnt = 0
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() not in itemList if enableParentCheck else it.id not in itemList:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                cnt += it.cwrap

        return cnt

    def countItemsInPagesBySType(self, stype, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        ret = {}
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                itemSType = CID.data.get(it.id, {}).get('sType')
                if itemSType != stype:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                ret[it.id] = ret.get(it.id, 0) + it.cwrap

        return ret

    def countItemChild(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        cnt = 0
        itemIdList = []
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId or itemId == it.id:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                itemIdList.append(it.id)
                cnt += it.cwrap

        return (cnt, itemIdList)

    def countItemBind(self, itemId, enableParentCheck = False):
        hasBind = False
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if it.isForeverBind() and not it.hasLatch():
                    hasBind = True
                    return hasBind

        return hasBind

    def _checkBindPolicy(self, bindPolicy, item):
        if bindPolicy in gametypes.ITEM_REMOVE_POLICY_ALL:
            return True
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_ONLY:
            return item.isForeverBind()
        else:
            return not item.isForeverBind()

    def _searchItemCandidates(self, itemId, amount, bindPolicy, enbaleParentCheck, includeExpired, includeLatch, includeShihun, startPage = 0, startPos = 0, filterFunc = None):
        tempItems = {}
        ps = startPos
        for pg in range(startPage, self.pageCount):
            ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)
            while ps != const.CONT_NO_POS:
                dst = self.getQuickVal(pg, ps)
                if not includeExpired and dst.isExpireTTL():
                    ps += 1
                    ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)
                    continue
                if not includeLatch and dst.hasLatch():
                    ps += 1
                    ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)
                    continue
                if not includeShihun and dst.isShihun():
                    ps += 1
                    ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)
                    continue
                if filterFunc and not filterFunc(dst):
                    ps += 1
                    ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)
                    continue
                if dst.isForeverBind():
                    if dst.isOneMall():
                        tempItems.setdefault(gametypes.ITEM_SHOP_BIND, []).append((pg, ps))
                    else:
                        tempItems.setdefault(gametypes.ITEM_COMMON_BIND, []).append((pg, ps))
                elif dst.isOneMall():
                    tempItems.setdefault(gametypes.ITEM_SHOP_UNBIND, []).append((pg, ps))
                else:
                    tempItems.setdefault(gametypes.ITEM_COMMON_UNBIND, []).append((pg, ps))
                ps += 1
                ps = self.searchByParentId(itemId, pg, ps) if enbaleParentCheck else self.searchByID(itemId, pg, ps)

            ps = 0

        tmpList = []
        if bindPolicy == gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_ONLY:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_UNBIND_ONLY:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_COMMON_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
        else:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, []) + tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        candidates = []
        for tmp in tmpList:
            tmp.sort(self.compClosure(COMP_WITHOUT_BIND_POLICY))
            candidates.extend(tmp)

        return candidates

    def _searchItemListCandidates(self, itemList, amount, bindPolicy, enbaleParentCheck, includeExpired, includeLatch, includeShihun, startPage = 0, startPos = 0, filterFunc = None):
        tempItems = {}
        ps = startPos
        for pg in range(startPage, self.pageCount):
            ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)
            while ps != const.CONT_NO_POS:
                dst = self.getQuickVal(pg, ps)
                if not includeExpired and dst.isExpireTTL():
                    ps += 1
                    ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)
                    continue
                if not includeLatch and dst.hasLatch():
                    ps += 1
                    ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)
                    continue
                if not includeShihun and dst.isShihun():
                    ps += 1
                    ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)
                    continue
                if filterFunc and not filterFunc(dst):
                    ps += 1
                    ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)
                    continue
                if dst.isForeverBind():
                    if dst.isOneMall():
                        tempItems.setdefault(gametypes.ITEM_SHOP_BIND, []).append((pg, ps))
                    else:
                        tempItems.setdefault(gametypes.ITEM_COMMON_BIND, []).append((pg, ps))
                elif dst.isOneMall():
                    tempItems.setdefault(gametypes.ITEM_SHOP_UNBIND, []).append((pg, ps))
                else:
                    tempItems.setdefault(gametypes.ITEM_COMMON_UNBIND, []).append((pg, ps))
                ps += 1
                ps = self.searchByParentList(itemList, pg, ps) if enbaleParentCheck else self.searchByIDList(itemList, pg, ps)

            ps = 0

        tmpList = []
        if bindPolicy == gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_ONLY:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_UNBIND_ONLY:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_COMMON_FIRST:
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_BIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_COMMON_UNBIND, []))
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []))
        else:
            tmpList.append(tempItems.get(gametypes.ITEM_SHOP_UNBIND, []) + tempItems.get(gametypes.ITEM_COMMON_UNBIND, []) + tempItems.get(gametypes.ITEM_SHOP_BIND, []) + tempItems.get(gametypes.ITEM_COMMON_BIND, []))
        candidates = []
        for tmp in tmpList:
            tmp.sort(self.compClosure(COMP_WITHOUT_BIND_POLICY))
            candidates.extend(tmp)

        return candidates

    def hasItemInPages(self, itemId, amount = 1, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        itemCnt = self.countItemInPages(itemId, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun)
        if itemCnt >= amount:
            return True
        return False

    def hasItemListInPages(self, itemList, amount, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        itemCnt = self.countItemListInPages(itemList, bindPolicy=bindPolicy, enableParentCheck=enableParentCheck, includeExpired=includeExpired, includeLatch=includeLatch, includeShihun=includeShihun)
        if itemCnt >= amount:
            return True
        return False

    def countBlankInPages(self):
        sum = 0
        for pg in self.getPageTuple():
            sum += self.countBlank(pg)

        return sum

    def _checkInsertItem(self, itemId):
        if Item.isQuestItem(itemId) and self.RES_KIND != const.RES_KIND_QUEST_BAG:
            return False
        if not Item.isQuestItem(itemId) and self.RES_KIND == const.RES_KIND_QUEST_BAG:
            return False
        if Item.isBusinessItem(itemId) and self.RES_KIND != const.RES_KIND_ZAIJU_BAG:
            return False
        return True

    def _canInsertItems(self, items):
        cntInsert = 0
        for itemId, amount in items.iteritems():
            if not self._checkInsertItem(itemId):
                return False
            if Item.isQuestItem(itemId):
                pg, posNum, way = self.__canInsertQuest(itemId, amount)
            else:
                pg, posNum, way = self.__canInsertItems(itemId, amount)
            if way == const.CONT_PLACE_NO:
                return False
            if way == const.CONT_PLACE_WRAP:
                continue
            elif way == const.CONT_PLACE_INSERT:
                cntInsert += posNum
                continue
            else:
                return False

        cntBlank = self.countBlankInPages()
        if cntInsert > cntBlank:
            return False
        return True

    def _canInsertItemsEx(self, items):
        cntInsert = 0
        for it in items:
            if not self._checkInsertItem(it.id):
                return False
            if Item.isQuestItem(it.id):
                pg, posNum, way = self.__canInsertQuest(it.id, it.cwrap, it)
            else:
                pg, posNum, way = self.__canInsertItems(it.id, it.cwrap, it)
            if way == const.CONT_PLACE_NO:
                return False
            if way == const.CONT_PLACE_WRAP:
                continue
            elif way == const.CONT_PLACE_INSERT:
                cntInsert += posNum
                continue
            else:
                return False

        cntBlank = self.countBlankInPages()
        if cntInsert > cntBlank:
            return False
        return True

    def canRemoveItems(self, items, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        for itemId, amount in items.iteritems():
            if not self.hasItemInPages(itemId, amount, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun):
                return False

        return True

    def canRemoveItemList(self, items, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        for itemList, amount in items:
            if not self.hasItemListInPages(itemList, amount, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun):
                return False

        return True

    def canRemoveItemsEx(self, items, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False):
        for itemId, amount in items.iteritems():
            if not self.hasItemInPages(itemId, amount, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun):
                return itemId

    def cntItemWithPlans(self, itemId, itemNum, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        remain = itemNum
        res = []
        for pg, ps in self._searchItemCandidates(itemId, 1, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun, filterFunc=filterFunc):
            if remain <= 0:
                break
            it = self.getQuickVal(pg, ps)
            if remain >= it.cwrap:
                remain -= it.cwrap
                res.append((pg, ps, it.cwrap))
            else:
                res.append((pg, ps, remain))
                remain = 0

        return (remain, res)

    def canRemoveItemWithPlans(self, itemId, itemNum, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        remain, res = self.cntItemWithPlans(itemId, itemNum, bindPolicy, enableParentCheck, includeExpired, includeLatch, includeShihun, filterFunc)
        if remain > 0:
            return False
        else:
            return res

    def hasItemExpireTTL(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck = False):
        pages = self.getPageTuple()
        for pg in pages:
            for ps in self.getPosTuple(pg):
                i = self.getQuickVal(pg, ps)
                if i is const.CONT_EMPTY_VAL:
                    continue
                if i.getParentId() != itemId if enableParentCheck else i.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, i):
                    continue
                if i.isExpireTTL():
                    return True

        return False

    def xItems(self):
        pages = self.getPageTuple()
        for pg in pages:
            posCount = self.getPosCount(pg)
            for dstPos in xrange(posCount):
                obj = self.getQuickVal(pg, dstPos)
                if obj == const.CONT_EMPTY_VAL:
                    continue
                yield (pg, dstPos, obj)

    def __canInsertItems(self, itemId, amount, srcIt = None):
        if not srcIt:
            srcIt = Item(itemId, amount, genRandProp=False)
        page, pos = (0, 0)
        while True:
            page, pos = self.findItemInPages(srcIt.id, includeExpired=False, includeLatch=False, includeShihun=True, startPage=page, startPos=pos)
            if pos == const.CONT_NO_POS:
                mwrap = Item.maxWrap(srcIt.id)
                pageNum = amount / mwrap + (1 if amount % mwrap > 0 else 0)
                blank = self.countBlankInPages()
                if pageNum > blank:
                    return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)
                else:
                    return (page, pageNum, const.CONT_PLACE_INSERT)
            else:
                item = self.getQuickVal(page, pos)
                if Item.canMerge(item, srcIt):
                    if not item.overBear(amount):
                        return (page, pos, const.CONT_PLACE_WRAP)
                    amount -= item.mwrap - item.cwrap
                pos += 1
                if pos > self.getPosCount(page):
                    page += 1
                    pos = 0

        return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)

    def __canInsertQuest(self, itemId, amount):
        if amount > Item.maxWrap(itemId):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)
        page, pos = self.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
        if pos == const.CONT_NO_POS:
            pg2, pos2 = self.searchEmptyInPages()
            if pos2 == const.CONT_NO_POS:
                return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)
            else:
                return (pg2, pos2, const.CONT_PLACE_INSERT)
        else:
            item = self.getQuickVal(page, pos)
            if item.overBear(amount):
                return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)
            return (page, pos, const.CONT_PLACE_WRAP)
        return (const.CONT_NO_PAGE, const.CONT_NO_POS, const.CONT_PLACE_NO)

    def findFirstUnLatchItemById(self, id):
        lastLatchPage = -1
        lastLatchPos = -1
        pages = self.getPageTuple()
        for pg in pages:
            posCount = self.getPosCount(pg)
            for dstPos in xrange(posCount):
                obj = self.getQuickVal(pg, dstPos)
                if obj == const.CONT_EMPTY_VAL:
                    continue
                if obj.id != id:
                    continue
                if self.getQuickVal(pg, dstPos).hasLatch():
                    lastLatchPage = pg
                    lastLatchPos = dstPos
                    continue
                return (pg, dstPos)

        return (lastLatchPage, lastLatchPos)

    def updateExpireTimeOfRenewalType(self, owner, renewalType, expireTime):
        updatedCount = 0
        for page in range(self.pageCount):
            for pos in range(self.posCount):
                if not self._isValid(page, pos):
                    break
                it = self.getQuickVal(page, pos)
                if not utils.updateExpireTime(owner, it, renewalType, expireTime, self.RES_KIND):
                    continue
                owner.client.resInsert(self.RES_KIND, it, page, pos)
                updatedCount += 1

        return updatedCount

    def checkItemCnt(self, owner, item, msg = True, enableParentCheck = True):
        itemId, itemCnt = item
        if itemCnt <= 0:
            return True
        if self.countItemInPages(itemId, enableParentCheck=enableParentCheck) < itemCnt:
            if msg:
                from cdata import game_msg_def_data as GMDD
                itemName = utils.getItemName(itemId)
                owner.client.showGameMsg(GMDD.data.MAKE_WISH_FAILED_NO_SUCH_ITEM, (itemCnt, itemName))
            return False
        return True
