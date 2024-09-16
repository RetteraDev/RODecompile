#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneMomentProxy.o
import math
import BigWorld
import gametypes
import events
import utils
import const
import ui
from guis import uiUtils
from helpers import taboo
import gameglobal
import uiConst
from guis import richTextUtils
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from callbackHelper import Functor
from helpers import pyq_interface
from gamestrings import gameStrings
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from cdata import personal_zone_config_data as PZCD
OP_TYPE_GET_MOMENT_INIT = 1
OP_TYPE_GET_MOMENT_REFRESH = 2

class PersonalZoneMomentProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneMomentProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_MOMENT, self.hide)

    def reset(self):
        self.momentId = 0
        self.curCommentData = []
        self.momentdata = {}
        self.facePanel = None
        self.opType = const.PERSONAL_ZONE_MOMENT_ADD_COMMENT
        self.replyInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_MOMENT:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_MOMENT)

    def show(self, momentId, momentData = None, opType = const.PERSONAL_ZONE_MOMENT_ADD_COMMENT, replyInfo = None):
        self.momentId = momentId
        self.momentdata = dict() if not momentData else momentData
        self.replyInfo = dict() if not replyInfo else replyInfo
        self.opType = opType
        if not self.widget:
            if not momentData:
                self.getMomentById(momentId, OP_TYPE_GET_MOMENT_INIT)
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_MOMENT)
        else:
            self.refreshMomentData()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.momentMc.bgMc.visible = False
        self.widget.addEventListener(events.MOUSE_CLICK, self.handleWidgetClick, False, 0, True)
        self.widget.counterMc.pageCounter.enableMouseWheel = False
        self.widget.counterMc.pageCounter.count = 1
        self.widget.counterMc.pageCounter.minCount = 1
        self.widget.counterMc.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handlePageChange, False, 0, True)
        self.refreshMoments()
        self.refreshCurPageComment()

    def refreshMomentData(self):
        if not self.hasBaseData():
            return
        self.refreshMoments()
        self.refreshCurPageComment()

    def getMomentId(self):
        return self.momentId

    def refreshInfo(self):
        if not self.widget:
            return
        self.setMomentsItem(self.widget.momentMc, self.momentdata)

    def refreshCurPageComment(self):
        if not self.hasBaseData():
            return
        if self.opType == const.PERSONAL_ZONE_MOMENT_FORWARD:
            self.getForwardList(self.momentId, self.widget.counterMc.pageCounter.count)
        else:
            self.getCommentList(self.momentId, self.widget.counterMc.pageCounter.count)

    def refreshMoments(self):
        if not self.hasBaseData():
            return
        momentId = self.momentId
        self.getMomentById(momentId)

    def getMomentById(self, momentId, op = OP_TYPE_GET_MOMENT_REFRESH):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetMomentById(rStatus, content, op)

        pyq_interface.getMomentById(_callBack, momentId)

    def onGetMomentById(self, rStatus, content, op):
        if not self.hasBaseData() and op != OP_TYPE_GET_MOMENT_INIT:
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.momentdata = content.get('data', [])
            if op == OP_TYPE_GET_MOMENT_REFRESH:
                self.setMomentsItem(self.widget.momentMc, self.momentdata)
            elif self.momentdata:
                self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_MOMENT)
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOMENT_DELETED_TIPS, ())
            if op == OP_TYPE_GET_MOMENT_INIT:
                self.reset()
            else:
                self.hide()

    def getCommentList(self, momentId, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetCommentList(rStatus, content, page)

        pyq_interface.getCommentList(_callBack, momentId, page)

    def onGetCommentList(self, rStatus, content, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            listData = content.get('data', [])
            self.curCommentData = listData.get('list', [])
            self.setMomentsItem(self.widget.momentMc, self.momentdata)
            count = listData.get('count', 0)
            self.setCounterData(self.widget.counterMc.pageCounter, count)

    def getForwardList(self, momentId, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetForwardList(rStatus, content, page)

        pyq_interface.getForwardList(_callBack, momentId, page)

    def onGetForwardList(self, rStatus, content, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            listData = content.get('data', [])
            self.curCommentData = listData.get('list', [])
            self.setMomentsItem(self.widget.momentMc, self.momentdata)
            count = listData.get('count', 0)
            self.setCounterData(self.widget.counterMc.pageCounter, count)

    def addComment(self, momentId, text, replyId = 0, replyCommentId = 0, logInfo = None):
        logInfo['momentId'] = momentId
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onAddComment(rStatus, content, replyId, logInfo)

        pyq_interface.addComment(_callBack, momentId, text, replyId, replyCommentId)

    def onAddComment(self, rStatus, content, replyId, logInfo):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            msgInputMc = self.widget.momentMc.canvas.msgInputMc
            msgInputMc.msgInput.clearTxt()
            msgInputMc.maxCharsDesc.visible = True
            self.refreshMomentData()
            self.uiAdapter.personalZoneFriend.refreshCurPageMoments()
            commentId = content.get('data', {}).get('id')
            momentId = logInfo.get('momentId', 0)
            gbId = logInfo.get('gbId', 0)
            p = BigWorld.player()
            p.base.genPyqOpLog(gametypes.PERSONAL_ZONE_PYQ_OP_ADD_COMMENT, int(gbId), int(momentId), int(commentId))
        elif replyId:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_COMMENT_DELETED_TIPS, ())

    def forwardMoments(self, momentId, text, topicId, logInfo):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onForwardMoments(rStatus, content, logInfo)

        pyq_interface.forwardMoments(_callBack, momentId, text)

    def onForwardMoments(self, rStatus, content, logInfo):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_FORWARD_SUCC_TIPS, ())
            self.uiAdapter.personalZoneFriend.refreshCurPageMoments()
            self.hide()
            gbId = logInfo.get('momentGbId', 0)
            momentId = content.get('data', {}).get('id', 0)
            likeNum = logInfo.get('likeNum', 0)
            hostId = logInfo.get('hostId', 0)
            commentNum = logInfo.get('commentNum', 0)
            forwardNum = logInfo.get('forwardNum', 0)
            topicId = logInfo.get('topicId', 0)
            srcId = logInfo.get('srcId', 0)
            hasGraph = logInfo.get('hasGraph', 0)
            p = BigWorld.player()
            p.base.genPyqMomentLog(gametypes.PERSONAL_ZONE_PYQ_OP_FORWARD_MOMENT, momentId, likeNum, commentNum, forwardNum, topicId, srcId, hasGraph)
            p.base.operateMoment(int(gbId), int(hostId), gametypes.PYQ_OP_TYPE_FORWARD, int(momentId), int(topicId))
        else:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOMENT_DELETED_TIPS, ())

    def setCounterData(self, counterMc, count):
        if not counterMc:
            return
        counterMc.maxCount = max(math.ceil(count * 1.0 / const.PERSONAL_ZONE_MOMENT_COMMENT_NUM_PER_PAGE), 1)

    def setMomentsItem(self, scrollWnd, data):
        if not self.hasBaseData():
            return 0
        elif not self.momentId:
            return
        elif not self.momentdata:
            return
        else:
            item = scrollWnd.canvas
            item.addEventListener(events.MOUSE_ROLL_OVER, self.handleItemRollOver, False, 0, True)
            item.addEventListener(events.MOUSE_ROLL_OUT, self.handleItemRollOut, False, 0, True)
            self.widget.removeAllInst(item)
            p = BigWorld.player()
            momentsGbId = int(data.get('roleId', 0))
            height = 8
            posY = 0
            isSelf = False
            if momentsGbId == p.gbId:
                isSelf = True
            item.momentsGbId = momentsGbId
            item.isSelf = isSelf
            hostId = data.get('serverId', 0)
            if not hostId:
                hostId = 0
            item.isCrossServer = hostId != utils.getHostId()
            momentBg = self.addMomentBg(item)
            headIcon = self.addHeadIcon(item, data)
            commonX = headIcon.x + headIcon.width
            nameTxt = self.addNameTxt(item, data, height, commonX)
            timeMc = self.addTimeMc(item, data, height)
            height = nameTxt.y + nameTxt.height
            reportBtn = self.addReportBtn(item, nameTxt, timeMc, data)
            descMc = self.addDescMc(item, data, height, commonX)
            height = descMc.y + descMc.richTxt.textFiled.textHeight
            imgList = data.get('forwardMoment', {}).get('imgList', [])
            if not imgList:
                imgList = data.get('imgList', [])
            self.addImgList(item, imgList, height, commonX, data)
            height += math.ceil(len(imgList) * 1.0 / 3) * 89
            delMomentBtn = self.addDelMomentBtn(item, data, height)
            operationMc = self.addOperationMc(item, data, height, commonX)
            height = operationMc.y + operationMc.height
            msgInputMc = self.addMsgInputMc(item, data, height, commonX)
            height = msgInputMc.y + msgInputMc.height
            commentBg = self.widget.getInstByClsName('PersonalZoneMoment_CommentBg')
            commentBg.x = commonX
            commentBg.y = height + 5
            commentBg.width = 388
            commmentHeight = 0
            likeListMc = None
            likeUsers = data.get('likeUsers', [])
            if likeUsers:
                likeListMc = self.addLikeListMc(item, likeUsers, height, commonX)
                commmentHeight += likeListMc.height
                height = likeListMc.y + likeListMc.height
            commentList = self.curCommentData
            if self.opType != const.PERSONAL_ZONE_MOMENT_FORWARD and not commentList:
                commentList = data.get('commentList', [])
            commentCanvas = self.widget.getInstByClsName('PersonalZoneMoment_CommentCanvas')
            self.widget.removeAllInst(commentCanvas)
            commentCanvas.x = commonX
            commentCanvas.y = height
            item.addChild(commentCanvas)
            for commentInfo in commentList:
                commentMc = self.addCommentMc(commentCanvas, data, commentInfo, commentCanvas.height, 0)

            commmentHeight = commentCanvas.y + commentCanvas.height - commentBg.y
            height = commentCanvas.y + commentCanvas.height
            if likeUsers or commentList:
                item.addChild(commentBg)
                item.setChildIndex(commentBg, 0)
            if commmentHeight:
                commentBg.alpha = 1
                commentBg.height = commmentHeight
                height = commentBg.y + commentBg.height
            momentBg.height = height
            scrollWnd.refreshHeight()
            return height

    def addMomentBg(self, item):
        momentBg = self.widget.getInstByClsName('PersonalZoneMoment_CommentBg')
        momentBg.x = 0
        momentBg.y = 0
        momentBg.width = 456
        momentBg.alpha = 0
        item.addChild(momentBg)
        return momentBg

    def addHeadIcon(self, item, data):
        headIcon = self.widget.getInstByClsName('PersonalZoneMoment_HeadIcon')
        headIcon.x = 0
        headIcon.y = 0
        item.addChild(headIcon)
        headIcon.leftFlag.visible = False
        headIcon.lvTxt.text = data.get('level', 0)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        gbId = data.get('roleId', 0)
        hostId = data.get('serverId', 0)
        if not hostId:
            hostId = 0
        headIcon.gbId = gbId
        headIcon.hostId = hostId
        headIcon.addEventListener(events.MOUSE_CLICK, self.handelHeadIconClick, False, 0, True)
        p = BigWorld.player()
        borderId = data.get('borderId', 1)
        if not borderId:
            borderId = SCD.data.get('defaultBorderId', 1)
        borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        headIcon.headMc.borderImg.fitSize = True
        headIcon.headMc.borderImg.loadImage(borderIcon)
        headIcon.headMc.icon.setContentUnSee()
        headIcon.headMc.icon.fitSize = True
        headIcon.headMc.icon.serverId = hostId
        headIcon.headMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
        photo = data.get('photo', '')
        if not photo:
            school = data.get('jobId', 4)
            sex = data.get('gender', 1)
            photo = utils.getDefaultPhoto(school, sex)
            headIcon.headMc.icon.loadImage(photo)
        elif utils.isDownloadImage(photo):
            headIcon.headMc.icon.url = photo
        else:
            headIcon.headMc.icon.loadImage(photo)
        return headIcon

    def addNameTxt(self, item, data, height, commonX):
        nameTxt = self.widget.getInstByClsName('PersonalZoneMoment_NameTxtMc')
        nameTxt.name = 'nameTxt'
        nameTxt.x = commonX
        nameTxt.y = height
        item.addChild(nameTxt)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        gbId = data.get('roleId', 0)
        hostId = data.get('serverId', 0)
        if not hostId:
            hostId = 0
        roleName = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
        roleName = uiUtils.formatLinkZone(roleName, int(gbId), int(hostId), underLine=False)
        nameTxt.nameTxt.htmlText = roleName
        return nameTxt

    def addTimeMc(self, item, data, height):
        timeMc = self.widget.getInstByClsName('PersonalZoneMoment_TimeMc')
        timeMc.x = 386
        timeMc.y = height
        item.addChild(timeMc)
        time = data.get('createTime', 0) / 1000
        timeStr = utils.formatTimeAgo(time, fuzzyTime=60)
        timeMc.timeTxt.text = timeStr
        return timeMc

    def addReportBtn(self, item, nameTxt, timeMc, data):
        reportBtn = self.widget.getInstByClsName('PersonalZoneMoment_ReportBtn')
        reportBtn.name = 'reportBtn'
        reportBtn.x = timeMc.x - 18
        reportBtn.y = nameTxt.y + 4
        reportBtn.visible = False
        item.addChild(reportBtn)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        reportBtn.data = roleName
        reportBtn.addEventListener(events.BUTTON_CLICK, self.handleReportBtn, False, 0, True)
        return reportBtn

    def addDescMc(self, item, data, height, commonX):
        descMc = self.widget.getInstByClsName('PersonalZoneMoment_DescMc')
        descMc.name = 'descMc'
        descMsg = data.get('text', '')
        previousForwards = data.get('previousForwards', [])
        forwardMoment = data.get('forwardMoment', {})
        if previousForwards or forwardMoment:
            descMsg += gameStrings.PERSONAL_ZONE_FORWARD_SIG_TXT
        for pfInfo in previousForwards:
            forwardText = pfInfo.get('text')
            roleInfo = pfInfo.get('roleinfo', {})
            pGbId = roleInfo.get('roleId', 0)
            pHostId = roleInfo.get('serverId', 0)
            roleName = roleInfo.get('roleName', '')
            if not roleName:
                roleName = ''
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(pHostId))
            forwardRoleName = gameStrings.PERSONAL_ZONE_AT_NAME_TXT + roleName
            descMsg += uiUtils.formatLinkZone(forwardRoleName, int(pGbId), int(pHostId)) + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT + forwardText + gameStrings.PERSONAL_ZONE_FORWARD_SIG_TXT

        if forwardMoment:
            forwardMomentText = forwardMoment.get('text', '')
            pGbId = forwardMoment.get('roleId', 0)
            pHostId = forwardMoment.get('serverId', 0)
            roleName = forwardMoment.get('roleName', '')
            if not roleName:
                roleName = ''
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(pHostId))
            authorName = gameStrings.PERSONAL_ZONE_AT_NAME_TXT + roleName
            descMsg += uiUtils.formatLinkZone(authorName, int(pGbId), int(pHostId)) + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT + forwardMomentText
        descMc.richTxt.text = ''
        descMc.richTxt.appandText(descMsg)
        descMc.richTxt.validateNow()
        descMc.x = commonX
        descMc.y = height
        descMc.richTxt.textFiled.height = descMc.richTxt.textFiled.textHeight + 10
        item.addChild(descMc)
        return descMc

    def addImgList(self, item, imgList, height, commonX, data):
        imgHeight = 0
        forwardMoment = data.get('forwardMoment', {})
        isForward = bool(forwardMoment)
        hostId = 0
        if isForward:
            hostId = forwardMoment.get('serverId', 0)
        else:
            hostId = data.get('serverId', 0)
        for i, imgUrl in enumerate(imgList):
            hostId = data.get('serverId', 0)
            imgMc = self.widget.getInstByClsName('PersonalZoneMoment_PicMc')
            imgMc.icon.addEventListener(events.EVENT_LOAD_REMOTE_IMG_FAIL, self.handleImgLoadFailBtn, False, 0, True)
            imgMc.icon.addEventListener(events.EVENT_COMPLETE, self.handleImgLoadDone, False, 0, True)
            imgMc.x = commonX + i % 3 * (imgMc.icon.oriWidth + 3)
            imgMc.y = height + 10 + i / 3 * (imgMc.icon.oriHeight + 3)
            imgMc.gotoAndStop('zhaopian')
            imgMc.icon.scaleType = uiConst.SCALE_TYPE_FILL_FRAME
            imgMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            imgMc.icon.serverId = hostId
            imgMc.icon.url = imgUrl.get('pic', '')
            imgMc.alpha = 1
            imgHeight = imgMc.height
            item.addChild(imgMc)
            item.setChildIndex(imgMc, 0)
            imgMc.picIdx = i
            imgMc.canOpen = False
            touchImgMc = self.widget.getInstByClsName('PersonalZoneMoment_PicMc')
            touchImgMc.x = imgMc.x
            touchImgMc.y = imgMc.y
            touchImgMc.alpha = 0
            touchImgMc.relatedMc = imgMc
            item.addChild(touchImgMc)
            touchImgMc.addEventListener(events.MOUSE_CLICK, self.handleOpenPicture, False, 0, True)

    def addDelMomentBtn(self, item, data, height):
        momentId = data.get('id')
        delMomentBtn = self.widget.getInstByClsName('PersonalZoneMoment_DelBtn')
        delMomentBtn.name = 'delMomentBtn'
        delMomentBtn.momentId = momentId
        likeCount = data.get('likeCount', 0)
        commentCount = data.get('commentCount', 0)
        forwardCount = data.get('forwardCount', 0)
        topicId = data.get('topicId', 0)
        momentId = data.get('momentId', 0)
        forwardMoment = data.get('forwardMoment', 0)
        impList = forwardMoment.get('imgList', [])
        previousForwards = data.get('previousForwards', [])
        lastForwardMomentId = 0
        if len(previousForwards):
            lastForwardMomentId = previousForwards[0].get('id', 0)
        if not lastForwardMomentId:
            lastForwardMomentId = momentId
        delMomentBtn.likeNum = likeCount
        delMomentBtn.commentNum = commentCount
        delMomentBtn.forwardNum = forwardCount
        delMomentBtn.topicId = topicId
        delMomentBtn.srcId = lastForwardMomentId
        delMomentBtn.hasGraph = bool(impList)
        delMomentBtn.x = 426
        delMomentBtn.y = height + 15
        delMomentBtn.visible = False
        delMomentBtn.addEventListener(events.BUTTON_CLICK, self.handleDelMomentBtn, False, 0, True)
        item.addChild(delMomentBtn)
        return delMomentBtn

    def addOperationMc(self, item, data, height, commonX):
        p = BigWorld.player()
        momentsGbId = int(data.get('roleId', 0))
        hostId = data.get('serverId', 0)
        roleName = data.get('roleName', '')
        momentId = data.get('id', 0)
        topicId = data.get('topicId', 0)
        if not roleName:
            roleName = ''
        isSelf = False
        if momentsGbId == p.gbId:
            isSelf = True
        operationMc = self.widget.getInstByClsName('PersonalZoneMoment_OperationMc')
        operationMc.x = commonX
        operationMc.y = height + 10
        operationMc.transpondBtn.btn.momentId = momentId
        operationMc.transpondBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleTranspondBtn, False, 0, True)
        forwardCount = data.get('forwardCount', 0)
        operationMc.transpondBtn.numTxt.text = forwardCount
        ASUtils.setHitTestDisable(operationMc.transpondBtn.numTxt, True)
        operationMc.commentBtn.btn.momentId = momentId
        operationMc.commentBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleCommentBtn, False, 0, True)
        commentCount = data.get('commentCount', 0)
        operationMc.commentBtn.numTxt.text = commentCount
        ASUtils.setHitTestDisable(operationMc.commentBtn.numTxt, True)
        isUserLiked = data.get('isUserLiked', 0)
        operationMc.likeBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleLikeBtn, False, 0, True)
        operationMc.unlikeBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleUnlikeBtn, False, 0, True)
        likeCount = data.get('likeCount', 0)
        operationMc.unlikeBtn.btn.momentId = momentId
        operationMc.likeBtn.btn.momentId = momentId
        operationMc.likeBtn.btn.topicId = topicId
        operationMc.likeBtn.btn.gbId = momentsGbId
        if isUserLiked:
            operationMc.unlikeBtn.visible = True
            operationMc.unlikeBtn.numTxt.text = likeCount
            ASUtils.setHitTestDisable(operationMc.unlikeBtn.numTxt, True)
            operationMc.likeBtn.visible = False
        else:
            operationMc.likeBtn.visible = True
            operationMc.likeBtn.numTxt.text = likeCount
            ASUtils.setHitTestDisable(operationMc.likeBtn.numTxt, True)
            operationMc.unlikeBtn.visible = False
        operationMc.giftBtn.visible = not isSelf
        operationMc.giftBtn.gbId = momentsGbId
        operationMc.giftBtn.hostId = hostId
        operationMc.giftBtn.roleName = roleName
        operationMc.giftBtn.addEventListener(events.BUTTON_CLICK, self.handleGiftBtn, False, 0, True)
        operationMc.followBtn.gbId = momentsGbId
        operationMc.followBtn.addEventListener(events.BUTTON_CLICK, self.handleFollowBtn, False, 0, True)
        operationMc.followBtn.label = gameStrings.PERSONAL_ZONE_FOLLOW_TXT
        isFollowing = data.get('isFollowing', 0)
        operationMc.followBtn.visible = not isSelf and not isFollowing
        item.addChild(operationMc)
        return operationMc

    def addMsgInputMc(self, item, data, height, commonX):
        msgInputMc = self.widget.getInstByClsName('PersonalZoneMoment_InputMc')
        msgInputMc.name = 'msgInputMc'
        msgInputMc.x = commonX
        msgInputMc.y = height + 5
        item.addChild(msgInputMc)
        ASUtils.setHitTestDisable(msgInputMc.maxCharsDesc, True)
        msgInputMc.msgInput.addEventListener(events.EVENT_CHANGE, self.handleMsgInputChange, False, 0, True)
        msgInputMc.msgInput.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleMsgInputFocusIn, False, 0, True)
        msgInputMc.msgInput.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleMsgInputFocusOut, False, 0, True)
        msgInputMc.faceBtn.addEventListener(events.MOUSE_CLICK, self.handleFaceBtnClick, False, 0, True)
        msgInputMc.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleSendBtnClick, False, 0, True)
        if self.opType == const.PERSONAL_ZONE_MOMENT_ADD_COMMENT:
            msgInputMc.sendBtn.label = gameStrings.PERSONAL_ZONE_COMMENT_TXT
            msgInputMc.maxCharsDesc.text = gameStrings.PERSONAL_ZONE_MSG_INPUT_COMMENT_TXT
        elif self.opType == const.PERSONAL_ZONE_MOMENT_FORWARD:
            msgInputMc.sendBtn.label = gameStrings.PERSONAL_ZONE_FORWARD_TXT
            msgInputMc.maxCharsDesc.text = gameStrings.PERSONAL_ZONE_MSG_INPUT_FORWARD_TXT
        elif self.opType == const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT:
            roleName = self.replyInfo.get('roleName', '')
            msg = gameStrings.PERSONAL_ZONE_MSG_INPUT_REPLY_TXT % roleName
            msgInputMc.maxCharsDesc.text = msg
            msgInputMc.sendBtn.label = gameStrings.PERSONAL_ZONE_COMMENT_TXT
        return msgInputMc

    def addLikeListMc(self, item, likeUsers, height, commonX):
        likeListMc = self.widget.getInstByClsName('PersonalZoneMoment_LikeListMc')
        likeListMc.x = commonX
        likeListMc.y = height + 5
        likeListMc.likeUsersTxt.htmlText = ''
        item.addChild(likeListMc)
        likeUserStr = ''
        lastStr = ''
        for userInfo in likeUsers:
            gbId = int(userInfo.get('roleId', 0))
            hostId = userInfo.get('serverId', 0)
            if not hostId:
                hostId = 0
            roleName = userInfo.get('roleName', '')
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
            userZoneLink = uiUtils.formatLinkZone(roleName, gbId=gbId, hostId=hostId)
            if likeUserStr:
                likeUserStr = gameStrings.PERSONAL_ZONE_COMMA_TXT.join((likeUserStr, userZoneLink))
            else:
                likeUserStr = ''.join((likeUserStr, userZoneLink))
            lastStr = likeUserStr

        if len(likeUsers) >= const.PERSONAL_ZONE_LIKE_USERS_SHOW_NUM:
            likeUserStr = likeUserStr + gameStrings.PERSONAL_ZONE_ETC_TXT
        likeListMc.likeUsersTxt.htmlText = likeUserStr
        likeListMc.likeUsersTxt.height = likeListMc.likeUsersTxt.textHeight + 5
        likeListMc.likeBg.height = likeListMc.likeUsersTxt.textHeight + 10
        return likeListMc

    def addCommentMc(self, item, data, commentInfo, height, commonX):
        roleName = commentInfo.get('roleName', '')
        if not roleName:
            roleName = ''
        momentId = data.get('id', 0)
        commentText = commentInfo.get('text', '')
        gbId = int(commentInfo.get('roleId', 0))
        hostId = commentInfo.get('serverId', 0)
        if not hostId:
            hostId = 0
        commentId = commentInfo.get('id', 0)
        commentMc = self.widget.getInstByClsName('PersonalZoneMoment_CommentItem')
        commentMc.commentGbId = gbId
        commentMc.x = 5
        commentMc.y = height
        roleNameEx = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
        commentMc.roleNameTxt.htmlText = ''
        roleNameStr = uiUtils.formatLinkZone(roleNameEx + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT, gbId=gbId, hostId=hostId)
        commentMc.setChildIndex(commentMc.roleNameTxt, 0)
        commentMc.setChildIndex(commentMc.commentItemBg, 0)
        commentMc.commentTxt.x = commentMc.roleNameTxt.textWidth + 5
        commentMc.commentTxt.textFiled.width = 344 - commentMc.commentTxt.x
        commentMc.delBtn.momentId = momentId
        commentMc.delBtn.commentId = commentId
        commentMc.delBtn.gbId = gbId
        commentMc.delBtn.addEventListener(events.BUTTON_CLICK, self.handleCommentItemDel, False, 0, True)
        commentMc.delBtn.visible = False
        commentMc.reportBtn.data = roleName
        commentMc.reportBtn.addEventListener(events.BUTTON_CLICK, self.handleCommentItemReport, False, 0, True)
        commentMc.reportBtn.visible = False
        commentMc.commentId = commentId
        commentMc.gbId = gbId
        commentMc.hostId = hostId
        commentMc.roleName = roleName
        commentMc.isCrossServer = hostId != utils.getHostId()
        replyInfo = commentInfo.get('replyInfo', {})
        msg = roleNameStr
        if replyInfo:
            replyGbId = replyInfo.get('roleId', 0)
            if replyGbId:
                replyRoleName = replyInfo.get('roleName', 0)
                replyServerId = replyInfo.get('serverId', 0)
                if not replyServerId:
                    replyServerId = 0
                replyRoleNameEx = uiUtils.getRoleNameWithSeverName(replyRoleName, int(replyServerId))
                msg += gameStrings.PERSONAL_ZONE_REPLY_TXT + uiUtils.formatPersonalZoneNameColor(replyRoleNameEx + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT)
        msg += commentText
        commentMc.commentTxt.text = ''
        commentMc.commentTxt.appandText(msg)
        commentMc.commentTxt.validateNow()
        commentMc.commentTxt.textFiled.height = commentMc.commentTxt.textFiled.textHeight + 5
        commentMc.commentTxt.addEventListener(events.MOUSE_CLICK, self.handleReplyComment, False, 0, True)
        commentMc.dashLine.y = commentMc.commentTxt.y + commentMc.commentTxt.height + 5
        commentMc.commentItemBg.height = commentMc.dashLine.y + commentMc.dashLine.height
        commentMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleCommentItemRollOver, False, 0, True)
        commentMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleCommentItemRollOut, False, 0, True)
        item.addChild(commentMc)
        return commentMc

    def handleItemRollOver(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        if t.isSelf:
            t.delMomentBtn.visible = True
        elif not t.isCrossServer:
            t.reportBtn.visible = True

    def handleItemRollOut(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.reportBtn.visible = False
        t.delMomentBtn.visible = False

    def handleCommentItemRollOver(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        p = BigWorld.player()
        if int(t.commentGbId) == int(p.gbId):
            if self.opType in (const.PERSONAL_ZONE_MOMENT_ADD_COMMENT, const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT):
                t.delBtn.visible = True
        elif not t.isCrossServer:
            t.reportBtn.visible = True

    def handleCommentItemRollOut(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.reportBtn.visible = False
        t.delBtn.visible = False

    def handleDelMomentBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'likeNum': t.likeNum,
         'commentNum': t.commentNum,
         'forwardNum': t.forwardNum,
         'topicId': t.topicId,
         'srcId': t.srcId,
         'hasGraph': t.hasGraph}
        self.uiAdapter.personalZoneFriend.delMoments(t.momentId, logInfo)

    def handleReportBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.prosecute.show(t.data, uiConst.MENU_PERSONAL_ZONE_PROSECUTE)

    def handleTranspondBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.switchOpType(const.PERSONAL_ZONE_MOMENT_FORWARD)

    def handleCommentBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.switchOpType(const.PERSONAL_ZONE_MOMENT_ADD_COMMENT)

    def handleLikeBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'gbId': t.gbId}
        self.uiAdapter.personalZoneFriend.likeMoments(t.momentId, 'do', int(t.topicId), logInfo)

    def handleUnlikeBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target

    def handleFollowBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.uiAdapter.personalZoneFriend.addFollow(int(t.gbId), 0)

    def handleGiftBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.spaceGiftGiving.show(t.gbId, t.roleName, t.hostId)

    def handleCommentItemReport(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.prosecute.show(t.data, uiConst.MENU_PERSONAL_ZONE_PROSECUTE)

    def handleCommentItemDel(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'momentId': t.momentId,
         'gbId': t.gbId}
        self.uiAdapter.personalZoneFriend.delComment(t.commentId, logInfo)

    def handleReplyComment(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        replyInfo = {'commentId': t.parent.commentId,
         'gbId': t.parent.gbId,
         'hostId': t.parent.hostId,
         'roleName': t.parent.roleName}
        self.switchOpType(const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT, replyInfo)

    def handlePageChange(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.refreshCurPageComment()

    def handleMsgInputFocusIn(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.parent.maxCharsDesc.visible = False

    def handleMsgInputFocusOut(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        if t.parent.msgInput.text == '':
            t.parent.maxCharsDesc.visible = True
        else:
            t.parent.maxCharsDesc.visible = False

    def handleMsgInputChange(self, *arg):
        if not self.hasBaseData():
            return
        msgInputMc = self.widget.momentMc.canvas.msgInputMc
        if msgInputMc.msgInput.text:
            msgInputMc.maxCharsDesc.visible = False
        else:
            msgInputMc.maxCharsDesc.visible = True

    def handleFaceBtnClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        if not self.facePanel:
            self.facePanel = self.widget.getInstByClsName('ChatFacePanel')
            self.facePanel.addEventListener(events.FACE_CLICK, self.handleFaceClick, False, 0, True)
            self.widget.addChild(self.facePanel)
            faceBtn = self.widget.momentMc.canvas.msgInputMc.faceBtn
            x, y = ASUtils.local2Global(self.widget.momentMc.canvas.msgInputMc, faceBtn.x, faceBtn.y)
            x, y = ASUtils.global2Local(self.widget, x, y)
            self.facePanel.x = x - 14
            self.facePanel.y = y - self.facePanel.height + 4
        self.facePanel.visible = True
        e.stopImmediatePropagation()

    def handleFaceClick(self, *arg):
        e = ASObject(arg[3][0])
        faceStr = utils.faceIdToString(int(e.data))
        msgInput = self.widget.momentMc.canvas.msgInputMc.msgInput
        msgInput.insertRichText(faceStr)
        msgInput.focused = 1
        self.facePanel.visible = False

    def handleWidgetClick(self, *arg):
        if self.facePanel:
            self.facePanel.visible = False

    def handleImgLoadFailBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t.parent:
            t.parent.canOpen = False
            if int(e.loadStatus) == gametypes.NOS_FILE_STATUS_ILLEGAL:
                t.parent.gotoAndStop('butongguo')
            else:
                t.parent.gotoAndStop('shenghezhong')

    def handleImgLoadDone(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t.parent:
            t.parent.canOpen = True

    def handelHeadIconClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        roleName = str(t.roleName)
        gbId = int(t.gbId)
        hostId = int(t.hostId)
        menuId = uiConst.MENU_PERSOANL_SPACE
        if hostId != self.uiAdapter.personalZoneSystem.getHostId():
            menuId = uiConst.MENU_PERSOANL_SPACE_CROSS_SERVER
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.uiAdapter.showUserLinkMenu(roleName, gbId, hostId, menuId)
        else:
            self.uiAdapter.personalZoneSystem.openZoneOther(int(t.gbId), '', 0, int(t.hostId))

    def handleOpenPicture(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget.relatedMc
        p = BigWorld.player()
        if not t.canOpen:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_PIC_AUDIT_TIPS, ())
            return None
        else:
            imgList = self.momentdata.get('forwardMoment', {}).get('imgList', [])
            if not imgList:
                imgList = self.momentdata.get('imgList', [])
            picList = []
            numberIdx = 0
            for i, info in enumerate(imgList):
                pic = info.get('pic', '')
                status, _, _ = p.nosFileStatusCache.get(pic, (None, None, None))
                if status == gametypes.NOS_FILE_STATUS_APPROVED:
                    picList.append({'filePath': pic})
                    if i == int(t.picIdx):
                        numberIdx = len(picList) - 1

            if picList:
                gameglobal.rds.ui.personalZonePicture.show(picList, numberIdx)
            return None

    def handleSendBtnClick(self, *arg):
        msgInput = self.widget.momentMc.canvas.msgInputMc.msgInput
        moodDesc = msgInput.richText
        momentId = self.momentdata.get('id', 0)
        momentGbId = self.momentdata.get('roleId', 0)
        hostId = self.momentdata.get('serverId', 0)
        likeCount = self.momentdata.get('likeCount', 0)
        commentCount = self.momentdata.get('commentCount', 0)
        forwardCount = self.momentdata.get('forwardCount', 0)
        topicId = self.momentdata.get('topicId', 0)
        forwardMoment = self.momentdata.get('forwardMoment', 0)
        forwardMomentId = forwardMoment.get('id', 0)
        impList = forwardMoment.get('imgList', [])
        previousForwards = self.momentdata.get('previousForwards', [])
        lastForwardMomentId = 0
        if len(previousForwards):
            lastForwardMomentId = previousForwards[0].get('id', 0)
        if not lastForwardMomentId:
            lastForwardMomentId = momentId
        topicId = self.momentdata.get('topicId', 0)
        msg = self.uiAdapter.personalZoneSystem.analysisChatMsg(moodDesc)
        p = BigWorld.player()
        if not msg:
            if self.opType == const.PERSONAL_ZONE_MOMENT_FORWARD:
                msg = gameStrings.PERSONAL_ZONE_FORWARD_DEFAULT_TXT
            else:
                p.showGameMsg(GMDD.data.PERSONAL_ZONE_MSG_NONE_TIPS, ())
                return
        result, announcement = taboo.checkDisbWord(msg)
        if richTextUtils.isSysRichTxt(announcement):
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        if not result:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        result, announcement = taboo.checkBWorld(announcement)
        if not result:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        if taboo.checkMonitorWord(announcement):
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOOD_TABOO_WORD, ())
            return
        try:
            msg = announcement.decode('gbk').encode('utf8')
        except:
            pass

        if self.opType == const.PERSONAL_ZONE_MOMENT_ADD_COMMENT:
            logInfo = {'gbId': momentGbId}
            self.addComment(momentId, msg, logInfo=logInfo)
        elif self.opType == const.PERSONAL_ZONE_MOMENT_FORWARD:
            logInfo = {'likeNum': likeCount,
             'commentNum': commentCount,
             'forwardNum': forwardCount,
             'topicId': topicId,
             'srcId': lastForwardMomentId,
             'hasGraph': bool(impList),
             'momentGbId': momentGbId,
             'hostId': hostId}
            self.forwardMoments(momentId, msg, topicId, logInfo)
        elif self.opType == const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT:
            replyId = self.replyInfo.get('gbId', 0)
            commentId = self.replyInfo.get('commentId', 0)
            logInfo = {'gbId': momentGbId}
            self.addComment(momentId, msg, replyId, commentId, logInfo=logInfo)

    def switchOpType(self, opType, replyInfo = None):
        if not self.hasBaseData():
            return
        self.opType = opType
        self.replyInfo = replyInfo
        self.refreshMomentData()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
