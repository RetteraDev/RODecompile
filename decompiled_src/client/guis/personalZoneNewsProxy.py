#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneNewsProxy.o
import BigWorld
import const
import math
import utils
from helpers import pyq_interface
import uiConst
import gamelog
from guis import events
from guis import uiUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from uiProxy import UIProxy
MAX_PHOTO_CNT = 2
MERGE_MSG_CD = 60

class PersonalZoneNewsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneNewsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_NEWS, self.hide)

    def reset(self):
        self.pageInfoList = []
        self.currentPage = 1
        self.minPage = 1
        self.maxPage = 1
        self.msgTypesDic = {}
        self.msgDic = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_NEWS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_NEWS)

    def show(self, page = 1):
        if page:
            self.currentPage = page
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_NEWS)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.currentPage = 1
        self.widget.scrollWndList.itemRenderer = 'PersonalZoneNews_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction

    def getNameStr(self, memberList):
        nameList = [ uiUtils.formatLinkZone(memberInfo[1], memberInfo[0], memberInfo[5]) for memberInfo in memberList ]
        nameStr = ','.join(nameList[:MAX_PHOTO_CNT])
        if len(memberList) > 1:
            nameStr += gameStrings.PERSONAL_ZONE_MULTI_PEOPLE % len(memberList)
        return nameStr

    def labelFunction(self, *args):
        dataIndex = int(args[3][0].GetNumber())
        if dataIndex >= len(self.pageInfoList):
            return
        pageInfo = self.pageInfoList[dataIndex]
        itemMc = ASObject(args[3][1])
        itemMc.newsType.gotoAndStop(pageInfo['newsType'])
        memberList = pageInfo['memberList']
        startPosX = 12
        for i in xrange(MAX_PHOTO_CNT):
            photoMc = itemMc.getChildByName('photoIcon%d' % i)
            if i < len(memberList):
                photoMc.visible = True
                photoMc.data = memberList[i]
                gbId, memberName, lv, photo, borderIcon, serverId = memberList[i]
                photoMc.txtLv.text = str(lv)
                photoMc.icon.headIcon.borderImg.fitSize = True
                photoMc.icon.headIcon.borderImg.loadImage(borderIcon)
                photoMc.icon.headIcon.icon.fitSize = True
                if utils.isDownloadImage(photo):
                    photoMc.icon.headIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                    photoMc.icon.headIcon.icon.serverId = serverId
                    photoMc.icon.headIcon.icon.url = photo
                else:
                    photoMc.icon.headIcon.icon.loadImage(photo)
                photoMc.x = startPosX
                startPosX += 50
            else:
                photoMc.visible = False

        startPosX += 10
        itemMc.txtNews.x = startPosX
        itemMc.txtNews.txtNews.htmlText = pageInfo['msg']
        itemMc.txtTime.text = pageInfo['timeStr']
        itemMc.img.fitSize = True
        if pageInfo['img']:
            itemMc.img.visible = True
            itemMc.img.fitSize = True
            itemMc.img.imgType = uiConst.IMG_TYPE_NOS_FILE
            if utils.isDownloadImage(pageInfo['img']):
                itemMc.img.url = pageInfo['img']
            else:
                itemMc.img.loadImage(pageInfo['img'])
        else:
            itemMc.img.visible = False

    def refreshMsg(self):
        self.pageInfoList = self.getPageInfoList(self.currentPage)
        self.widget.scrollWndList.dataArray = range(len(self.pageInfoList))

    def handleCounterChange(self, *args):
        currentPage = self.widget.pageCounter.count
        if currentPage != self.currentPage:
            self.currentPage = currentPage
            self.getMsg(self.currentPage)

    def refreshInfo(self):
        if not self.widget:
            return
        self.getMsg(self.currentPage)

    def getMsg(self, currentPage):
        pyq_interface.getNewsList(self.getMsgCallback, currentPage, const.PERSONAL_ZONE_NEWS_PAGE_SIZE)

    def getMsgCallback(self, rSttus, content):
        gamelog.info('jbx:getMsgCallback', rSttus, content)
        self.msgTypesDic.clear()
        self.msgDic.clear()
        data = content.get('data', {})
        count = data.get('count', 0)
        self.maxPage = math.ceil(count * 1.0 / const.PERSONAL_ZONE_NEWS_PAGE_SIZE)
        for msgInfo in data.get('list', []):
            objectInfo = msgInfo.get('objectInfo', {})
            id = objectInfo.get('id', 0)
            msgType = msgInfo.get('type', -1)
            self.msgTypesDic.setdefault(msgType, {}).setdefault(id, []).append(msgInfo)
            self.msgDic[id] = msgInfo

        self.refreshMsgList()

    def getProcessedMsgInfo(self, infoList):
        msgs = []
        p = BigWorld.player()
        infoList.sort(cmp=lambda a, b: cmp(b['createTime'], a['createTime']))
        headInfo = infoList[0]
        msgIdx = 0
        msgLen = len(infoList)
        while msgIdx < msgLen:
            pageInfo = {}
            memberInfo = infoList[msgIdx]
            msgType = memberInfo.get('type', 0)
            photo = memberInfo.get('photo', '')
            borderId = int(memberInfo.get('borderId', 1))
            if not borderId:
                borderId = 1
            lv = int(memberInfo.get('level', 0))
            roleName = memberInfo.get('roleName', 'roleName')
            serverId = int(memberInfo.get('serverId', utils.getHostId()))
            roleId = int(memberInfo.get('roleId', 0))
            school = memberInfo.get('jobId', 4)
            sex = memberInfo.get('gender', 1)
            if not photo:
                photo = 'headIcon/%s.dds' % str(school * 10 + sex)
            borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
            memberList = []
            memberList.append((roleId,
             roleName,
             lv,
             photo,
             borderIcon,
             serverId))
            imgList = headInfo.get('objectInfo', {}).get('imgList', [])
            if imgList:
                pageInfo['img'] = imgList[0].get('pic', '')
            else:
                pageInfo['img'] = ''
            pageInfo['newsType'] = const.MSG_TYPE_ICON_MAP[msgType]
            pageInfo['id'] = memberInfo.get('id')
            time = memberInfo.get('createTime', 0) / 1000
            diffTime = utils.getNow() - time
            pageInfo['time'] = time
            if diffTime <= 0:
                pageInfo['timeStr'] = gameStrings.PERSON_ZONE_RECENTLY
            elif diffTime >= const.SECONDS_PER_DAY:
                pageInfo['timeStr'] = gameStrings.PERSON_ZONE_TIME_DAY % (diffTime / const.SECONDS_PER_DAY)
            elif diffTime >= const.SECONDS_PER_HOUR:
                pageInfo['timeStr'] = gameStrings.PERSON_ZONE_TIME_HOUR % (diffTime / const.SECONDS_PER_HOUR)
            elif diffTime >= const.SECONDS_PER_MIN:
                pageInfo['timeStr'] = gameStrings.PERSON_ZONE_TIME_MIN % (diffTime / const.SECONDS_PER_MIN)
            else:
                pageInfo['timeStr'] = gameStrings.PERSON_ZONE_TIME_SECOND % diffTime
            msgIdx += 1
            while msgIdx < msgLen and time - infoList[msgIdx].get('createTime', 0) / 1000 < MERGE_MSG_CD:
                mergeMsgInfo = infoList[msgIdx]
                photo = mergeMsgInfo.get('photo', '')
                borderId = int(mergeMsgInfo.get('borderId', 1))
                lv = int(mergeMsgInfo.get('level', 0))
                borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
                roleName = mergeMsgInfo.get('roleName', 'roleName')
                serverId = int(mergeMsgInfo.get('serverId', utils.getHostId()))
                roleId = int(mergeMsgInfo.get('roleId', 0))
                school = memberInfo.get('jobId', 4)
                sex = memberInfo.get('gender', 1)
                if not photo:
                    photo = 'headIcon/%s.dds' % str(school * 10 + sex)
                memberList.append((roleId,
                 roleName,
                 lv,
                 photo,
                 borderIcon,
                 serverId))
                msgIdx += 1

            memberList.reverse()
            pageInfo['memberList'] = memberList
            nameStr = self.getNameStr(memberList)
            momnetId = headInfo.get('objectInfo', {}).get('id', 0)
            if msgType == const.MSG_TYPE_GUANZHU:
                contentStr = const.MSG_TYPE_TEXT_MAP[msgType] % (int(memberList[0][0]), int(memberList[0][-1]))
            else:
                contentStr = const.MSG_TYPE_TEXT_MAP[msgType] % int(momnetId)
            if msgType in (const.MSG_TYPE_HOT_CROSS_SERVER, const.MSG_TYPE_HOT):
                pageInfo['msg'] = contentStr
            else:
                pageInfo['msg'] = nameStr + '\n' + contentStr
            msgs.append(pageInfo)

        return msgs

    def refreshMsgList(self):
        if not self.widget:
            return
        msgList = []
        for msgType, typeValues in self.msgTypesDic.iteritems():
            for objectId, objectInfo in typeValues.iteritems():
                msgInfos = self.getProcessedMsgInfo(objectInfo)
                msgList.extend(msgInfos)

        msgList.sort(cmp=lambda a, b: cmp(b['time'], a['time']))
        self.pageInfoList = msgList
        self.widget.scrollWndList.dataArray = range(len(msgList))
        self.widget.pageCounter.removeEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange)
        self.widget.pageCounter.count = self.currentPage
        self.widget.pageCounter.maxCount = self.maxPage
        self.widget.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange, False, 0, True)
