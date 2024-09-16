#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInfoHonorProxy.o
import BigWorld
import uiUtils
import uiConst
import events
import gametypes
from gamescript import FormularEvalEnv
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
import activityFactory
from data import fame_data as FD
from data import play_recomm_activity_data as PRAD
from data import play_recomm_config_data as PRCD
from data import play_recomm_item_data as PRID
ITEM_STATE_NORMAL = 0
ITEM_STATE_SELECTED = 1
ACTIVITY_MAX_CNT = 5
PLAY_RECOMM_PATH = 'playRecomm/'
PLAY_RECOMM_TIPS_BG = 'scheduleBg/'
PLAY_RECOMM_ACTIVITY_ICON = PLAY_RECOMM_PATH + 'activityIcon/'
ITEM_PATH = 'item/icon64/'

class RoleInfoHonorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoleInfoHonorProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.actFactory = activityFactory.getInstance()

    def reset(self):
        self.selectedFameId = -1
        self.lastSelectedMc = None
        self.isHadNewFame = False
        self.fameIdMcRef = {}
        self.fameIdInfoRef = {}
        self.fameIdActivitiesRef = {}
        self.activityInfos = []
        self.activityTipMc = None
        self.questTipMc = None
        self.lastActivityTipIndex = None

    def initPanel(self, widget):
        self.widget = widget
        self.genFameIDActivitiesRef()
        self.needShowEff = True
        self.questTipMc = self.widget.questTips
        ASUtils.setHitTestDisable(self.questTipMc, False)
        self.activityTipMc = self.widget.activityTips
        self.activityTipMc.x = 862
        self.questTipMc.x = self.activityTipMc.x
        ASUtils.setHitTestDisable(self.activityTipMc, False)
        self._initUI()
        self.refreshFrame()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def genFameIDActivitiesRef(self):
        p = BigWorld.player()
        if self.fameIdInfoRef:
            return
        for key, value in PRAD.data.iteritems():
            fameInfos = value.get('rewardFames', ((),))
            if not fameInfos:
                continue
            for fameInfo in fameInfos:
                if not fameInfo:
                    continue
                fameId = fameInfo[0]
                schooldFilter = fameInfo[1:]
                if schooldFilter and p.school not in schooldFilter:
                    continue
                self.fameIdActivitiesRef.setdefault(fameId, []).append(key)

    def _initUI(self):
        self.widget.tree.lvItemGap = 6
        self.widget.tree.itemHeights = [28, 68]
        self.widget.tree.itemRenderers = ('RoleInformationHonorV2_TreeItemLv1', 'RoleInformationHonorV2_HonorItem1')
        self.widget.tree.labelFunction = self.treeLabelFun
        self.widget.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleTreeItemChange, False, 0, True)
        self.widget.mainMc.honorList.canvas.addChild(self.widget.tree)
        self.widget.mainMc.honorList.validateNow()
        self.widget.mainMc.canvasIcon.fitSize = True
        self.widget.mainMc.honorIcon.fitSize = True
        for i in xrange(ACTIVITY_MAX_CNT):
            mc = self.widget.mainMc.getChildByName('getFame%d' % i)
            mc.idx = i
            mc.addEventListener(events.MOUSE_CLICK, self.handleShowTips, False, 0, True)

        self.widget.mainMc.slot0.slot.dragable = False
        self.widget.mainMc.slot1.slot.dragable = False
        self.widget.mainMc.slot2.slot.dragable = False
        ASUtils.setHitTestDisable(self.widget.mainMc.slot0.slot, True)
        ASUtils.setHitTestDisable(self.widget.mainMc.slot1.slot, True)
        ASUtils.setHitTestDisable(self.widget.mainMc.slot2.slot, True)
        self.activityTipMc.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.handleHideTips, False, 0, True)
        self.questTipMc.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.handleHideTips, False, 0, True)

    def handleHideTips(self, *args):
        self.activityTipMc.visible = False
        self.questTipMc.visible = False

    def handleShowTips(self, *args):
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.idx)
        if idx >= len(self.activityInfos):
            return
        info = self.activityInfos[idx]
        pid = info['pid']
        prid = self.getPrid(pid)
        seekId = ''
        funcType = 0
        if prid:
            playRecommItemData = PRID.data.get(prid, {})
            if playRecommItemData:
                funcType = playRecommItemData.get('funcType', 0)
                if funcType == gametypes.RECOMMEND_TYPE_QUMO:
                    items = self.uiAdapter.playRecomm.getDailyQumoItems(funcType, prid, playRecommItemData)
                    if items:
                        seekId = items[0]['seekId']
        tipData = self.uiAdapter.playRecomm.getPlayTipData(pid, seekId, prid, funcType)
        self.activityTipMc.visible = False
        self.questTipMc.visible = False
        if tipData['expendQuestInfo']:
            self.questTipMc.visible = True
            self.questTipMc.tipData = tipData
        else:
            self.activityTipMc.visible = True
            self.activityTipMc.tipData = tipData

    def getPrid(self, pid):
        for key, value in PRID.data.iteritems():
            if value.get('moreInfoId', 0) == pid:
                return key

        return 0

    def getHonorInfo(self):
        p = BigWorld.player()
        data = {}
        for key, value in FD.data.items():
            if value.get('display', 0) == gametypes.FAME_SHOW_IN_HONORPANEL:
                itemData = {'name': value.get('name', ''),
                 'fameId': key}
                itemData['icon'] = 'fame/fame156/%s.dds' % value.get('icon', '')
                fame = BigWorld.player().getFame(key)
                itemData['fame'] = fame
                itemData['isNew'] = p.isNewFameRecord.get(key, False)
                itemData['desc'] = value.get('htmlDesc', '')
                itemData['sortOrder'] = value.get('sortOrder', 100)
                self.fameIdInfoRef[key] = itemData
                if value.get('weekGainLimit', ''):
                    fameW, maxW = BigWorld.player().fameWeek.get(key, (0, 0))
                    if not maxW:
                        maxW = FormularEvalEnv.evaluate(value.get('weekGainLimit', ''), {'lv': BigWorld.player().lv})
                    itemData['honorWeekDesc'] = gameStrings.ROLE_INFO_HONOR_WEEK % (fameW, maxW)
                else:
                    itemData['honorWeekDesc'] = ''
                data.setdefault((value.get('treeName', ''), value.get('tree', 0)), []).append(itemData)

        keys = data.keys()
        keys.sort(cmp=lambda x, y: cmp(x[1], y[1]))
        result = []
        for index, key in enumerate(keys):
            value = data.get(key)
            value.sort(cmp=lambda x, y: cmp(x['sortOrder'], y['sortOrder']))
            result.append({'label': key[0],
             'children': value,
             'expand': index == 0})

        if self.selectedFameId == -1:
            self.selectedFameId = data.get(keys[0])[0]['fameId']
        self.honorInfo = result

    def clearWidget(self):
        self.reset()

    def refreshFrame(self):
        if not self.widget:
            return
        if not self.widget.mainMc:
            return
        self.getHonorInfo()
        self.refreshTree()
        self.refreshFameDetail()

    def refreshTree(self):
        if not self.widget:
            return
        if not self.widget.mainMc:
            return
        self.fameIdMcRef.clear()
        self.widget.mainMc.parent.tree.childItemEffect = self.needShowEff
        self.widget.mainMc.parent.tree.dataArray = self.honorInfo
        self.widget.mainMc.parent.tree.validateNow()
        self.needShowEff = False

    def treeLabelFun(self, *args):
        item = ASObject(args[3][0])
        itemData = ASObject(args[3][1])
        isFirst = ASObject(args[3][2].GetBool())
        if isFirst:
            item.label.htmlText = itemData.label
        else:
            item.fameId = itemData.fameId
            if self.selectedFameId == int(itemData.fameId):
                if self.lastSelectedMc:
                    self.lastSelectedMc.frame.visible = False
                    self.lastSelectedMc.selected = False
                item.frame.visible = True
                self.lastSelectedMc = item
                self.lastSelectedMc.selected = True
                self.lastSelectedMc.frame.visible = True
                self.refreshFameDetail()
            else:
                item.frame.visible = False
                item.selected = False
            item.honorName.text = itemData.name
            item.fameWeek.text = str(int(itemData.fame))
            item.fameIcon.loadImage(itemData.icon)
            item.newNotify.visible = itemData.isNew
            self.fameIdMcRef[int(item.fameId)] = item
            item.addEventListener(events.MOUSE_CLICK, self.handleMouseClick, False, 0, True)
            item.addEventListener(events.MOUSE_OVER, self.handleMouseOver, False, 0, True)
            item.addEventListener(events.MOUSE_OUT, self.handleMouseOut, False, 0, True)

    def fameUpdate(self):
        self.refreshFrame()

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        e.currentTarget.frame.visible = False

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        e.currentTarget.frame.visible = True

    def handleMouseClick(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        self.questTipMc.visible = False
        self.activityTipMc.visible = False
        self.selectedFameId = int(e.currentTarget.fameId)
        p.isNewFameRecord[self.selectedFameId] = False
        if self.lastSelectedMc:
            self.lastSelectedMc.selected = False
            self.lastSelectedMc.frame.visible = False
        self.lastSelectedMc = e.currentTarget
        self.lastSelectedMc.selected = True
        self.lastSelectedMc.frame.visible = True
        self.lastSelectedMc.newNotify.visible = False
        self.refreshFameDetail()
        self.uiAdapter.roleInfo.updateHonor()
        self.uiAdapter.systemButton.showRoleInfoNotify()

    def handleTreeItemChange(self, *args):
        self.widget.mainMc.honorList.refreshHeight(self.widget.mainMc.parent.tree.height)

    def getActivityIcons(self):
        p = BigWorld.player()
        infoList = []
        typeIconBg = PRCD.data.get('prActivityTypeIconBg', {})
        for playRecommId in self.fameIdActivitiesRef.get(self.selectedFameId, []):
            info = {}
            rad = PRAD.data.get(playRecommId, {})
            if not rad:
                continue
            schoolFilter = rad.get('schoolFilter', [])
            if schoolFilter and p.school not in schoolFilter:
                continue
            displayType = rad.get('displayType', (2,))
            if not displayType:
                continue
            itemData = {}
            itemData['iconPath'] = (PLAY_RECOMM_ACTIVITY_ICON + '%s' + uiConst.ICON_SUFFIX) % str(rad.get('icon', 0))
            itemData['name'] = rad.get('name', '')
            info['itemData'] = itemData
            info['typeIcon'] = typeIconBg.get(displayType[0], 'blue')
            info['pid'] = playRecommId
            infoList.append(info)

        self.activityInfos = infoList
        return infoList

    def refreshFameDetail(self):
        p = BigWorld.player()
        if not self.selectedFameId:
            return
        else:
            fd = FD.data.get(self.selectedFameId, {})
            honorInfo = self.fameIdInfoRef.get(self.selectedFameId, {})
            if not fd or not honorInfo:
                return
            fameBg = fd.get('fameBg', 'default')
            self.widget.mainMc.canvasIcon.loadImage('fameBg/%s.dds' % fameBg)
            self.widget.mainMc.honorIcon.loadImage(honorInfo['icon'])
            self.widget.mainMc.txtHonorName.text = honorInfo.get('name', '')
            self.widget.mainMc.txtNow.text = gameStrings.ROLE_INFO_FAME_NOW % honorInfo.get('fame', 0)
            self.widget.mainMc.txtWeekly.text = honorInfo.get('honorWeekDesc', '')
            ASUtils.autoSizeWithFont(self.widget.mainMc.txtWeekly, 13, self.widget.mainMc.txtWeekly.width, 9)
            self.widget.mainMc.txtDesc.htmlText = honorInfo.get('desc', '')
            iconList = self.getActivityIcons()
            for i in xrange(ACTIVITY_MAX_CNT):
                mc = self.widget.mainMc.getChildByName('getFame%d' % i)
                if i >= len(iconList):
                    mc.visible = False
                    continue
                else:
                    mc.visible = True
                itemData = iconList[i]['itemData']
                mc.iconSlot.colorBg.gotoAndStop(iconList[i]['typeIcon'])
                mc.iconSlot.icon.setItemSlotData(itemData)
                mc.iconSlot.icon.dragable = False
                mc.iconSlot.icon.fitSize = True
                mc.activityName.text = iconList[i]['itemData']['name']
                ASUtils.autoSizeWithFont(mc.activityName, 14, mc.activityName.width, 5)

            helpKeys = fd.get('helpKeys', (0, 0))
            self.widget.mainMc.help_GetHonor.helpKey = helpKeys[0]
            self.widget.mainMc.help_GetHonor.validateNow()
            self.widget.mainMc.help_CostFame.helpKey = helpKeys[1]
            self.widget.mainMc.help_CostFame.validateNow()
            seekInfo = fd.get('seekInfo', ())
            if seekInfo:
                index = 0
                for info in seekInfo:
                    if len(info) > 2:
                        icon, txt, filterSchool = info
                    else:
                        icon, txt = info
                        filterSchool = None
                    if filterSchool and p.school not in filterSchool:
                        continue
                    slocMc = self.widget.mainMc.getChildByName('slot%d' % index)
                    if not slocMc:
                        break
                    txtSlotMc = self.widget.mainMc.getChildByName('txtSlot%d' % index)
                    slocMc.visible = True
                    txtSlotMc.visible = True
                    data = {}
                    data['iconPath'] = uiUtils.getItemIconPath(icon)
                    slocMc.slot.setItemSlotData(data)
                    slocMc.slot.validateNow()
                    slocMc.slot.bg.lock.visible = False
                    txtSlotMc.htmlText = txt
                    index += 1

                for i in range(index, 3):
                    slocMc = self.widget.mainMc.getChildByName('slot%d' % i)
                    txtSlotMc = self.widget.mainMc.getChildByName('txtSlot%d' % i)
                    slocMc.visible = False
                    txtSlotMc.visible = False

            else:
                self.widget.mainMc.slot0.visible = False
                self.widget.mainMc.txtSlot0.text = ''
                self.widget.mainMc.slot1.visible = False
                self.widget.mainMc.txtSlot1.text = ''
                self.widget.mainMc.slot2.visible = False
                self.widget.mainMc.txtSlot2.text = ''
            return

    def selectedItemByFameId(self, fameId):
        self.selectedFameId = fameId
        self.widget and self.fameUpdate()
