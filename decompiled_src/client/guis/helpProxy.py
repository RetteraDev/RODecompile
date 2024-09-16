#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/helpProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import time
import re
import json
import utils
import const
import formula
import clientcom
import gametypes
from helpers import remoteInterface
from helpers import navigator
from helpers import taboo
from guis.uiProxy import UIProxy
from guis.ui import unicode2gbk, gbk2unicode
from item import Item
from game import gameglobal
from guis import uiConst, uiUtils
from guis import richTextUtils
from guis import ui
from data import item_data as ID
from cdata import font_config_data as FCD
from data import mall_item_data as MD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
KEY_WORD_HOME_PAGE = gameStrings.TEXT_QNAINTERFACE_11
KEY_WORD_LVL_HOT = gameStrings.TEXT_HELPPROXY_37
KEY_WORD_GUIDE = gameStrings.TEXT_HELPPROXY_38
KEY_WORD_LV_UP = gameStrings.TEXT_HELPPROXY_40
KEY_WORD_MONEY = gameStrings.TEXT_HELPPROXY_41
KEY_WORD_STRONG = gameStrings.TEXT_HELPPROXY_42
KEY_WORD_NEWS = gameStrings.TEXT_HELPPROXY_44
KEY_WORD_LATEST_UPDATE = gameStrings.TEXT_HELPPROXY_45
KEY_WORD_HOT_SPOT = gameStrings.TEXT_HELPPROXY_46
KEY_WORD_ERROR_CORRECT = gameStrings.TEXT_HELPPROXY_47
CANT_CORRECT_QUEST_PREFIX = gameStrings.TEXT_HELPPROXY_49
RITEM_KEY_WORD = '<tuijiandaoju>'
RITEM_PATTERN = '</?tuijiandaoju.*?>'
NO_EVALUATE = '<noEvaluate/>'
HIDE_QUES = '@@H_ques'
HIDE_QUES_IN_ANSWER = '<H_ques>'
ALL_KEY_WORDS = (KEY_WORD_HOME_PAGE,
 KEY_WORD_LVL_HOT,
 KEY_WORD_NEWS,
 KEY_WORD_LATEST_UPDATE,
 KEY_WORD_HOT_SPOT,
 KEY_WORD_LV_UP,
 KEY_WORD_MONEY,
 KEY_WORD_STRONG)
KEY_BUTTON_WORDS = (KEY_WORD_LV_UP,
 KEY_WORD_MONEY,
 KEY_WORD_STRONG,
 KEY_WORD_NEWS,
 KEY_WORD_LATEST_UPDATE,
 KEY_WORD_HOT_SPOT)
QUERY_INTERVAL = 1.5

class HelpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HelpProxy, self).__init__(uiAdapter)
        self.modelMap = {'linkLeftClick': self.onLinkLeftClick,
         'getHomeMsg': self.onGetHomePage,
         'getPlayerInfo': self.onGetPlayerInfo,
         'getQueryResult': self.onGetQueryResult,
         'feedBack': self.onFeedBack,
         'keyBtnClick': self.onKeyBtnClick,
         'showRItems': self.onShowRItems,
         'showHelpPanel': self.onShowHelpPanel,
         'showSprite': self.onShowSprite,
         'getShowSprite': self.onGetShowSprite,
         'clickRItem': self.onClickRItem,
         'saveMsgs': self.onSaveMsgs,
         'closeReItems': self.onCloseReItems,
         'topClick': self.onTopClick,
         'getHotWords': self.onGetHotWords,
         'showErrorCorrect': self.onShowErrorCorrect,
         'submitTxt': self.onSubmitTxt}
        self.currentQid = 1
        self.gfxMsgs = None
        self.queryMsgs = {}
        self.reset()
        self.canEvaluateQids = []
        self.lvlHotResult = None
        self.autoPushTimer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_HELP_SPRITE, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_HELP_ERROR_CORRECT, self.hideErrorCorret)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HELP_SPRITE:
            self.med = mediator
            self.showRecomandItems([])
            initData = {'showHomeMsg': True}
            if self.initQueryTxt:
                self.queryText(str(self.initQueryTxt), True, True)
                initData['showHomeMsg'] = False
            if self.gfxMsgs and self.gfxMsgs.GetArraySize() > 0:
                initData['showHomeMsg'] = True
                initData['msgs'] = self.gfxMsgs
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_HELP_ERROR_CORRECT:
            if self.med:
                self.correctMed = mediator
                txt = unicode2gbk(self.med.Invoke('getCurrentQuest').GetString())
                if txt.startswith(CANT_CORRECT_QUEST_PREFIX):
                    txt = ''
                return uiUtils.dict2GfxDict({'quest': txt}, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_HELP_ERROR_CORRECT:
            self.hideErrorCorret()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def hideErrorCorret(self):
        self.correctMed = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HELP_ERROR_CORRECT)

    def showByItemId(self, itemId):
        name = ID.data.get(itemId, {}).get('name', '')
        self.show(name)
        if self.med:
            self.med.Invoke('swapPanelToFront')

    def show(self, *args):
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.FORBIDDEN_ON_CROSS, ())
            return
        if gameglobal.rds.configData.get('enableHelpSystem', True):
            if self.med:
                if args:
                    self.queryText(str(args[0]), True, True)
            else:
                if args:
                    self.initQueryTxt = args[0]
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HELP_SPRITE)
        else:
            url = SCD.data.get('helpSystemUrl')
            if url:
                if args:
                    url = url + '?txt=' + str(args[0])
                BigWorld.openUrl(url)

    def clearWidget(self):
        self.med = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HELP_SPRITE)
        self.hideErrorCorret()
        if self.lvlHotQueryCallback:
            BigWorld.cancelCallback(self.lvlHotQueryCallback)

    def reset(self):
        self.med = None
        self.correctMed = None
        self.rItems = []
        self.homePageQid = None
        self.lvlHotQid = None
        self.guideQid = None
        self.birthday = None
        self.initQueryTxt = None
        self.isTopClick = 0
        self.hotWordsDict = {}
        self.lvlHotQueryCallback = None

    def onGetShowSprite(self, *args):
        p = BigWorld.player()
        spriteLv = SCD.data.get('showSprite', 17)
        isShow = gameglobal.rds.ui.spriteAni.getSetting()
        enabled = p.lv >= spriteLv
        ret = [isShow, enabled]
        return uiUtils.array2GfxAarry(ret)

    def onClickRItem(self, *args):
        mallId = args[3][0].GetNumber()
        gameglobal.rds.ui.tianyuMall.show(mallId)

    def onSaveMsgs(self, *args):
        self.gfxMsgs = args[3][0]

    def onShowSprite(self, *args):
        isShow = int(args[3][0].GetBool())
        if isShow:
            gameglobal.rds.ui.spriteAni.show()
            if gameglobal.rds.ui.spriteAni.callback:
                BigWorld.cancelCallback(gameglobal.rds.ui.spriteAni.callback)
                gameglobal.rds.ui.spriteAni.callback = None
        else:
            gameglobal.rds.ui.spriteAni.disappear()

    def onGetHomePage(self, *args):
        self.homePageQid = self._queryText(KEY_WORD_HOME_PAGE, False, False)
        if self.lvlHotQueryCallback:
            BigWorld.cancelCallback(self.lvlHotQueryCallback)
        if self.lvlHotResult:
            self.showLvlHot(self.lvlHotResult)
        else:
            self.lvlHotQueryCallback = BigWorld.callback(QUERY_INTERVAL, self.queryLvlHot)

    def queryLvlHot(self):
        if self.med:
            self.lvlHotQid = self._queryText(KEY_WORD_LVL_HOT, False, False)

    def onGetPlayerInfo(self, *args):
        playerInfo = self.movie.CreateObject()
        p = BigWorld.player()
        playerInfo.SetMember('school', GfxValue(p.school))
        playerInfo.SetMember('lvl', GfxValue(p.lv))
        photo = p._getFriendPhoto(p)
        if uiUtils.isDownloadImage(photo):
            imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            if not clientcom.isFileExist(imagePath):
                BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
            else:
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        playerInfo.SetMember('photo', GfxValue(photo))
        playerInfo.SetMember('name', GfxValue(gbk2unicode(p.playerName)))
        return playerInfo

    def onLinkLeftClick(self, *args):
        eventName = unicode2gbk(args[3][0].GetString())
        handled = True
        try:
            if eventName.startswith('item'):
                self.showTooltip(const.CHAT_TIPS_ITEM, gameglobal.rds.ui.inventory.GfxToolTip(Item(int(eventName[5:]), 1, False)))
            elif eventName.startswith('task'):
                self.showTooltip(const.CHAT_TIPS_TASK, gameglobal.rds.ui.chat.taskToolTip(int(eventName[5:])))
            elif eventName.startswith('achv'):
                self.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, gameglobal.rds.ui.chat.achieveToolTip(eventName[5:]))
            elif eventName.startswith('sec_ask'):
                self.queryText(eventName[len('sec_ask') + 1:], True, True)
            elif eventName.startswith('seek'):
                seekId = eventName[len('seek') + 1:]
                uiUtils.findPosById(seekId)
            elif eventName.startswith('http'):
                BigWorld.openUrl(eventName)
            elif eventName.startswith('findPos'):
                pos = eventName[len('findPos') + 1:].split(',')
                navigator.getNav().pathFinding((float(pos[1]),
                 float(pos[2]),
                 float(pos[3]),
                 float(pos[0])), None, None, True, 0.5)
            else:
                handled = False
        except:
            pass

        return GfxValue(handled)

    def onGetQueryResult(self, *args):
        txt = unicode2gbk(args[3][0].GetString())
        txt = ''.join(txt.split())
        click = args[3][0].GetBool()
        self.queryText(txt, click, True)

    def onGetQuickLvlGuide(self, *args):
        self.guideQid = self.queryText(KEY_WORD_GUIDE, True)

    def onKeyBtnClick(self, *args):
        index = int(args[3][0].GetNumber())
        if index >= 0 and index < len(KEY_BUTTON_WORDS):
            self.guideQid = self.queryText(KEY_BUTTON_WORDS[index], True, False)

    def onShowRItems(self, *args):
        qid = int(args[3][0].GetNumber())
        ritems = self.queryMsgs.get(qid)
        if ritems and isinstance(ritems[-1], list):
            self.showRecomandItems(ritems[-1])

    def onTopClick(self, *args):
        self.isTopClick = 1

    def onCloseReItems(self, *args):
        qid = int(args[3][0].GetNumber())
        if qid in self.queryMsgs.keys():
            msgResult = self.queryMsgs.get(qid)
            msgResult[-1] = []

    def onFeedBack(self, *args):
        isGood = args[3][0].GetBool()
        answer = unicode2gbk(args[3][1].GetString())
        quest = unicode2gbk(args[3][2].GetString())
        isClick = int(args[3][3].GetBool())
        p = BigWorld.player()
        vipgrade = utils.getVipGrade(BigWorld.player())
        pid = p.gbId
        name = p.realRoleName
        urs = gameglobal.rds.ui.loginWin.userName
        plv = p.lv
        school = p.school
        birthday = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.birthday))
        tOn = args[3][4].GetNumber()
        tOff = args[3][5].GetNumber()
        host = args[3][6].GetString()
        spaceName = formula.whatSpaceName(p.spaceNo) + str(p.position)
        gameid = 37
        remoteInterface.evaluateSprite(vipgrade, pid, name, urs, plv, host, school, birthday, tOn, tOff, spaceName, isClick, gameid, quest, answer, int(isGood), self.isTopClick, self.feedBackCallBack)

    def onShowHelpPanel(self, *arg):
        self.show()

    def feedBackCallBack(self, data, isGood):
        if isGood:
            BigWorld.player().showGameMsg(GMDD.data.HELP_GOOD_FEED_BACK, ())
        else:
            BigWorld.player().showGameMsg(GMDD.data.HELP_BAD_FEED_BACK, ())

    def showRecomandItems(self, recomandItems):
        self.rItems = recomandItems
        if self.med:
            items = []
            for mallId in recomandItems:
                itemId = MD.data.get(int(mallId), {}).get('itemId', 0)
                if itemId:
                    data = ID.data.get(int(itemId), {})
                    itemData = {}
                    path = uiUtils.getItemIconFile64(int(itemId))
                    itemData['iconPath'] = path
                    quality = data.get('quality', 1)
                    color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                    itemData['color'] = color
                    itemData['count'] = MD.data.get(int(mallId), {}).get('useTimes', 1)
                    itemData['itemId'] = itemId
                    itemData['label'] = MD.data.get(int(mallId), {}).get('label', 0)
                    itemData['mallId'] = int(mallId)
                    items.append(itemData)

            self.med.Invoke('showRecommendItems', uiUtils.array2GfxAarry(items))

    def showLvlHot(self, guideTxt):
        if self.med:
            self.med.Invoke('showRecommandText', GfxValue(gbk2unicode(guideTxt)))

    def showQueryResult(self, qid, result, birthday, tOn, tOff, host):
        self.birthday = birthday
        txtInfo = self.queryMsgs.get(qid)
        qTxt = txtInfo[1]
        if qid == self.lvlHotQid:
            self.lvlHotResult = result
        if self.med and txtInfo and not qTxt.startswith(KEY_WORD_ERROR_CORRECT):
            answer, rItems, canEvaluate, canCorrect, hideQues = self._parseResult(result)
            if qid not in self.canEvaluateQids:
                canEvaluate = False
            if qTxt.startswith(CANT_CORRECT_QUEST_PREFIX):
                canCorrect = False
            resultObj = self._getSpriteGfxResult(qTxt, richTextUtils.parseRichText(answer), not qid == self.homePageQid, qid, tOn, tOff, host, canEvaluate)
            resultObj.SetMember('canCorrect', GfxValue(canCorrect))
            resultObj.SetMember('answer', GfxValue(gbk2unicode(answer)))
            self.queryMsgs[qid].append(answer)
            self.queryMsgs[qid].append(rItems)
            if qid == self.homePageQid:
                self.med.Invoke('addMsg', (resultObj, GfxValue(True)))
            elif qid == self.lvlHotQid:
                self.showLvlHot(result)
            elif txtInfo:
                self.med.Invoke('clearMsg')
                self.med.Invoke('addMsg', self._getMyGfxQuery(txtInfo[1], txtInfo[0], txtInfo[2] or hideQues))
                self.med.Invoke('addMsg', resultObj)

    @ui.callFilter(1, True)
    def queryText(self, txt, click, evaluate):
        return self._queryText(txt, click, evaluate)

    def _queryText(self, txt, click, evaluate):
        hideQues = False
        rHideQues = re.findall(HIDE_QUES, txt, re.DOTALL)
        if rHideQues and len(rHideQues):
            hideQues = True
        txt = re.sub(HIDE_QUES, '', txt, 0, re.DOTALL)
        qid = self.getQid()
        if evaluate:
            self.canEvaluateQids.append(qid)
        viewText, fullText = richTextUtils.getOpCodeFullText(txt)
        self.queryMsgs[qid] = [click, viewText, hideQues]
        BigWorld.player().base.questionGame(qid, fullText, BigWorld.player().position, bool(click))
        return qid

    def _getSpriteGfxResult(self, qtxt, result, isReply = True, qid = None, tOn = None, tOff = None, host = None, canEvaluate = True):
        resultObj = self.movie.CreateObject()
        resultObj.SetMember('isMe', GfxValue(False))
        resultObj.SetMember('time', GfxValue(time.time()))
        resultObj.SetMember('photo', GfxValue('headIcon/1.dds'))
        resultObj.SetMember('name', GfxValue(gbk2unicode(gameStrings.TEXT_HELPPROXY_411)))
        resultObj.SetMember('isReply', GfxValue(isReply))
        resultObj.SetMember('msg', GfxValue(gbk2unicode(result)))
        resultObj.SetMember('qid', GfxValue(qid))
        resultObj.SetMember('tOn', GfxValue(tOn))
        resultObj.SetMember('tOff', GfxValue(tOff))
        resultObj.SetMember('host', GfxValue(host))
        resultObj.SetMember('canEvaluate', GfxValue(qtxt not in ALL_KEY_WORDS and canEvaluate))
        return resultObj

    def _getMyGfxQuery(self, queryTxt, isClick, hideQues):
        p = BigWorld.player()
        obj = self.movie.CreateObject()
        obj.SetMember('isMe', GfxValue(True))
        obj.SetMember('time', GfxValue(time.time()))
        photo = p._getFriendPhoto(p)
        if uiUtils.isDownloadImage(photo):
            imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            if not clientcom.isFileExist(imagePath):
                BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
            else:
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        obj.SetMember('photo', GfxValue(photo))
        obj.SetMember('name', GfxValue(gbk2unicode(p.realRoleName)))
        obj.SetMember('msg', GfxValue(gbk2unicode(queryTxt)))
        obj.SetMember('isClick', GfxValue(isClick))
        obj.SetMember('hide', GfxValue(hideQues))
        return obj

    def _parseResult(self, result):
        resultRitems = []
        rItems = re.findall(RITEM_PATTERN, result, re.DOTALL)
        canEvaluate = True
        canCorrect = True
        hideQues = False
        if rItems and len(rItems):
            lastRItem = rItems[-1]
            resultRitems = lastRItem[len('<tuijiandaoju'):-1].strip().split(',')
        rEva = re.findall(NO_EVALUATE, result, re.DOTALL)
        if rEva and len(rEva):
            canEvaluate = False
        rCorrect = re.findall(uiConst.NO_ERROR_CORRECT, result, re.DOTALL)
        if rCorrect and len(rCorrect):
            canCorrect = False
        rHdieQues = re.findall(HIDE_QUES_IN_ANSWER, result, re.DOTALL)
        if rHdieQues and len(rHdieQues):
            hideQues = True
        result = re.sub(RITEM_PATTERN, '', result, 0, re.DOTALL)
        result = re.sub(NO_EVALUATE, '', result, 0, re.DOTALL)
        result = re.sub(HIDE_QUES_IN_ANSWER, '', result, 0, re.DOTALL)
        return (result,
         resultRitems,
         canEvaluate,
         canCorrect,
         hideQues)

    def showTooltip(self, tipsType, gfxTipData):
        if self.med:
            self.med.Invoke('showTooltip', (GfxValue(tipsType), gfxTipData))

    def getQid(self):
        self.currentQid += 1
        return self.currentQid

    def isShow(self):
        return self.med != None

    def onDownloadPhoto(self, status, callbackArgs):
        pass

    @ui.callAfterTime()
    def onGetHotWords(self, *args):
        prefix = unicode2gbk(args[3][0].GetString()).strip()
        data = self.hotWordsDict.get(prefix)
        if data:
            self._getHotWordsCallback(prefix, data)
        else:
            remoteInterface.getSpriteAutoHotWordsByPrefix(prefix, self._getHotWordsCallback)

    def onShowErrorCorrect(self, *args):
        if self.correctMed:
            self.hideErrorCorret()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_HELP_ERROR_CORRECT)

    def onSubmitTxt(self, *args):
        question = unicode2gbk(args[3][0].GetString())
        answer = unicode2gbk(args[3][1].GetString())
        if question and answer:
            txt = gameStrings.TEXT_HELPPROXY_499 % (question, answer)
            txt = re.sub('\r|\n', '#r', txt)
            self._queryText(txt, False, False)
        BigWorld.player().showGameMsg(GMDD.data.MSG_HELP_ERROR_CORRECT, ())

    def _getHotWordsCallback(self, prefix, data):
        if data:
            self.hotWordsDict[prefix] = data
            if self.med:
                result = {}
                try:
                    data = json.loads(data, encoding='GBK')
                    if data and data.get('success'):
                        result = {'prefix': prefix,
                         'hotWords': [ gameStrings.TEXT_HELPPROXY_512 + str(x.encode('GBK')) for x in data.get('data', []) ]}
                    self.med.Invoke('setHotWord', uiUtils.dict2GfxDict(result, True))
                except:
                    self.hotWordsDict[prefix] = None

    def clickPushHelp(self):
        data = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_SPC_GMT_HELP_PUSH)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_HELP_PUSH)
        if data:
            self.show(data.get('data', ''))

    def addPushData(self, icon, data, tip, sound = 404):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_HELP_PUSH)
        pushInfo = {'iconId': icon,
         'tooltip': tip,
         'soundIdx': sound}
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SPC_GMT_HELP_PUSH, {'data': data}, pushInfo)

    def canAutoPush(self, msg):
        if self.autoPushTimer:
            return
        _, msg = utils.decodeMsgHeader(msg)
        needPush, helpStr, showStr, type, link = taboo.checkAutoPushSystemWords(msg, BigWorld.player())
        if needPush:
            if type == 0:
                linkEventTxt = 'uiShow:help.show(\"%s\")' % helpStr
            else:
                linkEventTxt = link
            if showStr:
                autoPushChatStr = uiUtils.toHtml(showStr, linkEventTxt=linkEventTxt)
                autoPushSpriteAniStr = uiUtils.toHtml(showStr, linkEventTxt=linkEventTxt)
            else:
                autoPushChatStr = uiUtils.toHtml(SCD.data.get('autoPushChatStr', '%s') % helpStr, linkEventTxt=linkEventTxt)
                autoPushSpriteAniStr = uiUtils.toHtml(SCD.data.get('autoPushSpriteAniStr', '%s') % helpStr, linkEventTxt=linkEventTxt)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_INFO, autoPushChatStr, SCD.data.get('autoPushName', ''))
            gameglobal.rds.ui.spriteAni.setPopMsg(autoPushSpriteAniStr, const.SPRITE_POPO_MSG_FANKUI, 30)
            self.startAutoPushTimer()

    def startAutoPushTimer(self):
        if self.autoPushTimer:
            return
        self.autoPushTimer = BigWorld.callback(SCD.data.get('autoPushCD', 10), self.stopAutoPushTimer)

    def stopAutoPushTimer(self):
        if self.autoPushTimer:
            BigWorld.cancelCallback(self.autoPushTimer)
            self.autoPushTimer = None

    def setQuestionText(self, qTxt):
        if self.med and qTxt:
            self.med.Invoke('setQuestionTxt', GfxValue(gbk2unicode(qTxt)))
