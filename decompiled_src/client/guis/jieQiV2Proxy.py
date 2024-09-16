#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/jieQiV2Proxy.o
import BigWorld
import utils
import const
import gametypes
import gameglobal
from guis import uiConst
from guis import uiUtils
from guis import events
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import intimacy_data as IND
from data import intimacy_config_data as ICD
from data import school_data as SD
from data import intimacy_func_data as IFD
from data import intimacy_sys_event_data as ISED
from data import quest_data as QD
from data import message_desc_data as MSGDD
from data import intimacy_numeric_data as CIND

class JieQiV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JieQiV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.hasJieQi = False
        self.reset()
        self.curSel = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_JIEQIV2, self.hide)

    def reset(self):
        self.version = 0

    def refresh(self, version):
        self.version = version
        if self.widget:
            self.initView()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_JIEQIV2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_JIEQIV2)

    def show(self):
        p = BigWorld.player()
        if p.friend.intimacyTgt:
            p.cell.queryIntimacyEvent(self.version)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_JIEQIV2)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.previewBtn.addEventListener(events.BUTTON_CLICK, self.onTabClick1, False, 0, True)
        self.widget.introBtn.addEventListener(events.BUTTON_CLICK, self.onTabClick2, False, 0, True)
        self.widget.fightForLoveBtn.addEventListener(events.BUTTON_CLICK, self.onFightForLoveBtnClick, False, 0, True)
        self.widget.fightForLoveBtn.visible = gameglobal.rds.configData.get('enableFightForLove', False)
        self.widget.previewPanel.timelineView.itemHeight = 49
        self.widget.previewPanel.timelineView.itemRenderer = 'JieQiV2_TimeLine_Text'
        self.widget.previewPanel.timelineView.lableFunction = self.timelineLabelFunction
        self.initView()
        introData = self.onGetIntroData()
        self.setIntroPanel(introData)
        self.onTabClick1()

    def refreshInfo(self):
        if not self.widget:
            return

    def onTabClick1(self, *args):
        if self.hasJieQi:
            self.widget.previewBtn.selected = True
            self.widget.introBtn.selected = False
            self.widget.previewPanel.visible = True
            self.widget.previewNoPanel.visible = False
            self.widget.introPanel.visible = False
        else:
            self.widget.previewBtn.selected = True
            self.widget.introBtn.selected = False
            self.widget.previewPanel.visible = False
            self.widget.previewNoPanel.visible = True
            self.widget.introPanel.visible = False

    def onTabClick2(self, *args):
        self.widget.previewBtn.selected = False
        self.widget.introBtn.selected = True
        self.widget.previewPanel.visible = False
        self.widget.previewNoPanel.visible = False
        self.widget.introPanel.visible = True

    def onFightForLoveBtnClick(self, *args):
        p = BigWorld.player()
        p.seekFightForLoveNpc()

    def initView(self):
        data = self.onGetInitData()
        self.hasJieQi = data['hasJieQi']
        if self.hasJieQi:
            self.widget.previewBtn.selected = True
            self.widget.introBtn.selected = False
            self.widget.previewPanel.visible = True
            self.widget.previewNoPanel.visible = False
            self.widget.introPanel.visible = False
            self.widget.previewPanel.playerName.text = data['playerInfo']['name']
            self.widget.previewPanel.playerLv.text = data['playerInfo']['lv']
            self.widget.previewPanel.playerIcon.gotoAndStop('sex' + str(data['playerInfo']['sex']))
            self.widget.previewPanel.playerSex.gotoAndStop('sex' + str(data['playerInfo']['sex']))
            self.widget.previewPanel.targetName.text = data['targetInfo']['name']
            self.widget.previewPanel.targetLv.text = data['targetInfo']['lv']
            self.widget.previewPanel.targetIcon.gotoAndStop('sex' + str(data['targetInfo']['sex']))
            self.widget.previewPanel.targetSex.gotoAndStop('sex' + str(data['targetInfo']['sex']))
            self.widget.previewPanel.intimacyTxt.text = data['targetInfo']['intimacyName']
            self.widget.previewPanel.dayText.text = data['targetInfo']['jieQiDays']
            self.widget.previewPanel.nickname.addEventListener(events.BUTTON_CLICK, self.handleClickNicknameBtn, False, 0, True)
            if data['bNicknameBtn']:
                self.widget.previewPanel.nickname.visible = True
            else:
                self.widget.previewPanel.nickname.visible = False
            self.setIntimacyIcon(data['targetInfo'])
            self.initTimeLine(data['timeLineInfo'])
        else:
            self.widget.previewBtn.selected = True
            self.widget.introBtn.selected = False
            self.widget.previewPanel.visible = False
            self.widget.previewNoPanel.visible = True
            self.widget.introPanel.visible = False
            self.widget.previewNoPanel.playerName.text = data['playerInfo']['name']
            self.widget.previewNoPanel.playerLv.text = data['playerInfo']['lv']
            self.widget.previewNoPanel.playerIcon.gotoAndStop('sex' + str(data['playerInfo']['sex']))
            self.widget.previewNoPanel.playerSex.gotoAndStop('sex' + str(data['playerInfo']['sex']))

    def initTimeLine(self, timeList):
        if not timeList:
            self.widget.previewPanel.timelineView.visible = False
            self.widget.previewPanel.line.visible = False
            self.widget.previewPanel.preview.visible = True
        else:
            self.widget.previewPanel.timelineView.visible = True
            self.widget.previewPanel.line.visible = True
            self.widget.previewPanel.preview.visible = False
            self.widget.previewPanel.timelineView.dataArray = timeList

    def timelineLabelFunction(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.descText.text = data.desc
        item.timeControl.timeText.text = data.time

    def handleClickNicknameBtn(self):
        self.onShowJieQiNickname()

    def onShowJieQiNickname(self, *args):
        if not gameglobal.rds.ui.jieQiNickname.widget:
            gameglobal.rds.ui.jieQiNickname.show()

    def setIntimacyIcon(self, obj):
        canvasLength = 243
        iconX = 0
        iconY = 0
        icon = 0
        iconUpSign = 0
        if obj['isFamiIconUp'] and obj['intimacyMaxLv'] != obj['intimacyLv']:
            iconUpSign = self.widget.getInstByClsName('JieQiV2_IntimacyIconUpSign')
            iconUpSign.x = -28
            iconUpSign.y = -1
            self.widget.previewPanel.xinCanvas.addChild(iconUpSign)
            canvasLength = 265
        if obj['intimacyMaxLv'] == obj['intimacyLv']:
            if obj['isFamiIconUp']:
                icon = self.widget.getInstByClsName('JieQiV2_IntimacyIconUp')
            else:
                icon = self.widget.getInstByClsName('JieQiV2_IntimacyIcon')
            if icon:
                self.widget.previewPanel.xinCanvas.addChild(icon)
                icon.gotoAndStop('full')
        else:
            for i in range(0, obj['intimacyLv'], 1):
                if obj['isFamiIconUp']:
                    icon = self.widget.getInstByClsName('JieQiV2_IntimacyIconUp')
                else:
                    icon = self.widget.getInstByClsName('JieQiV2_IntimacyIcon')
                if icon:
                    if i == obj['intimacyLv'] - 1:
                        if obj['intimacyFull']:
                            icon.gotoAndStop('normal')
                        else:
                            icon.gotoAndStop('empty')
                    else:
                        icon.gotoAndStop('normal')
                    icon.x = iconX
                    iconX += 25
                    icon.y = iconY
                    self.widget.previewPanel.xinCanvas.addChild(icon)

        self.widget.previewPanel.xinCanvas.x = canvasLength - self.widget.previewPanel.xinCanvas.width / 2

    def onGetIntroData(self, *args):
        self.downLoadFriendPhoto()
        ret = IFD.data.items()
        sorted(ret, key=lambda d: d[0])
        return ret

    def downLoadFriendPhoto(self):
        p = BigWorld.player()
        if p.profileIcon != '':
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.profileIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadSelfProfilePhoto, (None,))
        else:
            defaultPhoto = 'headIcon/%s.dds' % str(p.school * 10 + p.physique.sex)
            if self.widget:
                self.setPlayerIcon(defaultPhoto)
        if p.friend.intimacyTgt:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            photo = p._getFriendPhoto(fVal)
            if uiUtils.isDownloadImage(photo):
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (None,))
            elif self.widget:
                self.setTargetIcon(photo)

    def setPlayerIcon(self, iconPath):
        self.widget.previewPanel.playerIcon.icon.fitSize = True
        self.widget.previewNoPanel.playerIcon.icon.fitSize = True
        if self.hasJieQi:
            self.widget.previewPanel.playerIcon.icon.loadImage(iconPath)
        else:
            self.widget.previewNoPanel.playerIcon.icon.loadImage(iconPath)

    def setTargetIcon(self, iconPath):
        self.widget.previewPanel.targetIcon.icon.fitSize = True
        self.widget.previewPanel.targetIcon.icon.loadImage(iconPath)

    def onDownloadSelfProfilePhoto(self, status, callbackArgs):
        p = BigWorld.player()
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.friend.photo + '.dds'
            if self.widget:
                self.setPlayerIcon(photo)

    def onDownloadOtherPhoto(self, status, callbackArgs):
        p = BigWorld.player()
        fVal = p.getFValByGbId(p.friend.intimacyTgt)
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + fVal.photo + '.dds'
            if self.widget:
                self.setTargetIcon(photo)

    def setIntroPanel(self, data):
        initY = 0
        initBtnY = 5
        for i, j in enumerate(data):
            leftBtn = self.widget.getInstByClsName('JieQiV2_LeftBtn')
            leftBtn.validateNow()
            leftBtn.label = j[1]['title']
            self.widget.introPanel.addChild(leftBtn)
            leftBtn.y = initBtnY + i * (leftBtn.height + 4)
            leftBtn.x = 0
            introItem = self.getIntroItemByType(j[1]['type'], j[1])
            self.widget.introPanel.introView.canvas.addChild(introItem)
            introItem.y = initY
            initY = introItem.y + introItem.line.y + 3
            leftBtn.data = introItem.y
            leftBtn.addEventListener(events.BUTTON_CLICK, self.onClickLeft, False, 0, True)

        self.widget.introPanel.introView.refreshHeight()

    def getPicPath(self, id):
        return 'jieqi/%d.dds' % id

    def getIntroItemByType(self, Type, data):
        item = 0
        if Type == 1:
            item = self.widget.getInstByClsName('JieQiV2_Intro_Text')
            item.descText.text = data['desc']
            item.title.text = data['title']
            item.line.y = item.descText.y + item.descText.textHeight + 8
        elif Type == 2:
            item = self.widget.getInstByClsName('JieQiV2_Intro_TextPic')
            item.descText.htmlText = data['desc']
            item.title.text = data['title']
            picY = item.descText.y + item.descText.textHeight + 5
            item.pic.canvas.loadImage(self.getPicPath(data['picId']))
            item.pic.y = picY
            item.line.y = item.pic.y + item.pic.height + 8
        elif Type == 3:
            item = self.widget.getInstByClsName('JieQiV2_Intro_TextIcon')
            item.descText.text = data['desc']
            item.title.text = data['title']
            iconY = item.descText.y + item.descText.textHeight + 5
            for i, j in enumerate(data['skills']):
                icon = self.widget.getInstByClsName('JieQiV2_Item_Icon')
                self.initSkillIcon(j, icon)
                item.addChild(icon)
                icon.y = iconY + 43 * int(i / 3)
                icon.x = 1 + 47 * (i % 3)

            item.line.y = iconY + 43 * int((len(data['skills']) - 1) / 3) + 43 + 8
        elif Type == 4:
            item = self.widget.getInstByClsName('JieQiV2_Intro_TextIcon')
            item.descText.text = data['desc']
            item.title.text = data['title']
            iconY = item.descText.y + item.descText.textHeight + 5
            for i, j in enumerate(data['items']):
                icon = self.widget.getInstByClsName('JieQiV2_Item_Icon')
                self.initItemIcon(j, icon)
                item.addChild(icon)
                icon.y = iconY + 43 * int(i / 3)
                icon.x = 1 + 47 * (i % 3)

            item.line.y = iconY + 43 * int((len(data['items']) - 1) / 3) + 43 + 8
        return item

    def initItemIcon(self, id, icon):
        icon.fitSize = True
        iconPath = 'item/icon64/%d.dds' % id
        icon.loadImage(iconPath)
        self.widget.SimpleTipManager.addTipByType(icon, self.widget.TipsTypeConstants.TYPE_ITEM, id)

    def initSkillIcon(self, id, icon):
        icon.fitSize = True
        iconPath = 'skill/icon/%d.dds' % id
        icon.loadImage(iconPath)
        self.widget.SimpleTipManager.addTipByType(icon, self.widget.TipsTypeConstants.TYPE_SKILL, id)

    def onClickLeft(self, *args):
        e = ASObject(args[3][0])
        if self.curSel:
            self.curSel.selected = False
        e.currentTarget.selected = True
        self.curSel = e.currentTarget
        self.widget.introPanel.introView.scrollTo(e.currentTarget.data)

    def onGetInitData(self, *args):
        ret = {}
        p = BigWorld.player()
        if p.friend.intimacyTgt == 0:
            ret['hasJieQi'] = False
        else:
            ret['hasJieQi'] = True
            if not gameglobal.rds.configData.get('enableIntimacyTgtNickName', False):
                ret['bNicknameBtn'] = False
            else:
                ret['bNicknameBtn'] = True
        playerInfo = {}
        playerInfo['name'] = p.roleName
        school = SD.data.get(p.physique.school, {}).get('name', '')
        playerInfo['lv'] = school + ' Lv' + str(p.lv)
        playerInfo['sex'] = p.physique.sex
        ret['playerInfo'] = playerInfo
        if p.friend.intimacyTgt:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            if fVal:
                info = {}
                info['name'] = fVal.name
                school = SD.data.get(fVal.school, {}).get('name', '')
                info['sex'] = fVal.sex
                info['lv'] = school + ' Lv' + str(fVal.level)
                info['intimacy'] = fVal.intimacy
                info['intimacyMaxLv'] = ICD.data.get('MAX_INTIMACY_LV', 9)
                info['isFamiIconUp'] = CIND.data.get(1, {}).get('minVal', 0) <= fVal.intimacy
                intimacyUpLv = gameglobal.rds.ui.friend.getFamiUpIntimacyLv(fVal.intimacy)
                if info['isFamiIconUp'] and intimacyUpLv:
                    info['intimacyLv'] = intimacyUpLv
                    info['intimacyName'] = CIND.data.get(intimacyUpLv, {}).get('name', '')
                    info['intimacyFull'] = CIND.data.get(intimacyUpLv, {}).get('maxVal', 0) <= fVal.intimacy
                else:
                    info['intimacyLv'] = fVal.intimacyLv
                    info['intimacyName'] = IND.data.get(fVal.intimacyLv, {}).get('name', '')
                    info['intimacyFull'] = IND.data.get(fVal.intimacyLv, {}).get('maxVal', 0) <= fVal.intimacy
                info['jieQiDays'] = utils.diffYearMonthDayInt(int(uiUtils._getTodayDate()), utils.getYearMonthDayInt(p.friend.tBuildIntimacy))
                ret['targetInfo'] = info
        timeLineInfo = []
        if hasattr(p, 'intimacyEvent') and p.intimacyEvent:
            for key in p.intimacyEvent:
                for event in p.intimacyEvent[key]:
                    intimacyEventDesc = self.getDescByMsg(event.msgType, event.msg)
                    if gameglobal.rds.configData.get('enableNotifyBuildIntimacyCnt', False) and p.getBuildIntimacyCnt() > 0 and event.msgType == gametypes.INTIMACY_EVENT_TYPE_SYS and int(event.msg) == 0:
                        if p.isOldBuildIntimacy:
                            cnt = p.getBuildIntimacyCnt() + 100 - p.getBuildIntimacyCnt() % 100
                            extraMsg = MSGDD.data.get('LAST_BUILD_INTIMACY_CNT_MSG', '%s')
                        else:
                            cnt = p.getBuildIntimacyCnt()
                            extraMsg = MSGDD.data.get('BUILD_INTIMACY_CNT_MSG', '%s')
                        intimacyEventDesc += extraMsg % cnt
                    timeLineInfo.append({'time': self.getTimeByWhen(key),
                     'desc': intimacyEventDesc,
                     'when': event.when})

            timeLineInfo = sorted(timeLineInfo, key=lambda d: d['when'], reverse=True)
        ret['timeLineInfo'] = timeLineInfo
        return ret

    def getDescByMsg(self, mType, msg):
        desc = ''
        p = BigWorld.player()
        if mType == gametypes.INTIMACY_EVENT_TYPE_SYS:
            desc = ISED.data.get(int(msg)).get('desc', '')
        elif mType == gametypes.INTIMACY_EVENT_TYPE_DESC:
            desc = msg
        elif mType == gametypes.INTIMACY_EVENT_TYPE_BIRTHDAY:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            if fVal:
                desc = ICD.data.get('INTIMACY_BIRTH_DESC', '') % fVal.name
        elif mType == gametypes.INTIMACY_EVENT_TYPE_QUEST:
            questId = int(msg)
            desc = ICD.data.get('INTIMACY_QUEST_DESC', '') % QD.data.get(questId, {}).get('name', '')
        return desc

    def getTimeByWhen(self, when):
        return str(when[1]) + '.' + str(when[2])
