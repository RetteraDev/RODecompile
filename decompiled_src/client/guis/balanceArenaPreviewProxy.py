#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArenaPreviewProxy.o
import BigWorld
import gameglobal
import commcalc
import gametypes
import utils
import const
import formula
from appearanceInfo import AppearanceInfo
from guis import uiConst
from guis import events
from guis.asObject import ASUtils
from uiProxy import UIProxy
from guis import uiUtils
from ui import gbk2unicode
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis import tipUtils
from data import avatar_lv_data as ALD
from helpers import capturePhoto
from helpers import charRes
from data import role_panel_attr_data as RPAD
from cdata import prop_def_data as PDD
from data import prop_data as PD
PART_EQU_NUM = 42

class TemplateProp(object):
    pass


class BalanceArenaPreviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArenaPreviewProxy, self).__init__(uiAdapter)
        self.common = self.getPropsArray(uiConst.COMMON_PROPS)
        self.attack = self.getPropsArray(uiConst.ATTACK_PROPS)
        self.defense = self.getPropsArray(uiConst.DEFENSE_PROPS)
        self.advance = self.getPropsArray(uiConst.ADVANCE_PROPS)
        self.templateProp = TemplateProp()
        self.widget = None
        self.itemPos = [0, 0]
        self.currItemIndex = 0
        self.headGen = None
        self.currTemplate = None
        self.currTemplateId = 0
        self.cache = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_PREVIEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_PREVIEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.resetHeadGen()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_PREVIEW)

    def show(self, templateId = 0):
        if self.cache.get(templateId, None):
            self.showTemplate(templateId)
        else:
            self.queryServerData(templateId)

    def fillDataWithMine(self):
        p = BigWorld.player()
        self.cache[0] = p.__dict__
        self.showTemplate(0)

    def onGetServerData(self, data):
        templateId = data.get('tempId', 0)
        self.cache[templateId] = data
        self.showTemplate(templateId)

    def queryServerData(self, templateId):
        p = BigWorld.player()
        p.base.queryCharTempBasicInfo(long(templateId))

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initHeadGen()
        self.widget.photo.leftRotateBtn.autoRepeat = True
        self.widget.photo.rightRotateBtn.autoRepeat = True
        self.widget.photo.leftRotateBtn.repeatDelay = 100
        self.widget.photo.rightRotateBtn.repeatDelay = 100
        self.widget.photo.leftRotateBtn.repeatInterval = 100
        self.widget.photo.rightRotateBtn.repeatInterval = 100
        self.widget.photo.leftRotateBtn.addEventListener(events.BUTTON_CLICK, self.onRotateClick)
        self.widget.photo.rightRotateBtn.addEventListener(events.BUTTON_CLICK, self.onRotateClick)
        self.widget.supportBtn.addEventListener(events.BUTTON_CLICK, self.onSupportBtnClick)
        self.widget.leaveMsgBtn.addEventListener(events.BUTTON_CLICK, self.onLeaveMsgBtnClick)
        self.widget.chooseBtn.addEventListener(events.BUTTON_CLICK, self.onChooseBtnClick)
        self.widget.checkWarSpriteBtn.addEventListener(events.BUTTON_CLICK, self.onCheckWarSpriteBtnClick)
        self.widget.checkSkillBtn.addEventListener(events.BUTTON_CLICK, self.onCheckSkillBtnClick)
        self.widget.checkHierogramBtn.addEventListener(events.BUTTON_CLICK, self.onCheckHierogramBtnBtnClick)
        self.widget.huanjianBtn.addEventListener(events.BUTTON_CLICK, self.onHuanjianBtnClick)
        p = BigWorld.player()
        if not formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)) and not p.inBalanceTemplateWhiteList():
            self.widget.chooseBtn.enabled = False

    def onRotateClick(self, *args):
        e = ASObject(args[3][0])
        index = -1
        if e.target.name == 'rightRotateBtn':
            index = 1
        deltaYaw = -0.104 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onSupportBtnClick(self, *args):
        gbId = self.currTemplate.get('gbID', 0)
        p = BigWorld.player()
        p.base.zanCharTemp(long(gbId))

    def onLeaveMsgBtnClick(self, *args):
        templateData = self.currTemplate
        hostId = templateData.get('hostId', 0)
        if self.currTemplate:
            gbId = self.currTemplate.get('gbID', 0)
            if gbId:
                p = BigWorld.player()
                p.getPersonalSysProxy().openZoneOther(long(gbId), hostId=hostId, autoOpenChat=True)

    def onChooseBtnClick(self, *args):
        p = BigWorld.player()
        p.cell.useCharTemp(long(self.currTemplateId), gametypes.CHAR_TEMP_TYPE_ARENA)

    def onCheckWarSpriteBtnClick(self, *args):
        if self.currTemplateId:
            p = BigWorld.player()
            p.base.querySpriteInfo(long(self.currTemplateId))

    def onCheckSkillBtnClick(self, *args):
        if self.currTemplateId:
            p = BigWorld.player()
            p.base.queryCharTempSkillInfo(long(self.currTemplateId))

    def onCheckHierogramBtnBtnClick(self, *args):
        if self.currTemplateId:
            p = BigWorld.player()
            p.cell.queryCharTempHierogramInfo(long(self.currTemplateId))

    def onHuanjianBtnClick(self, *args):
        if self.currTemplateId:
            p = BigWorld.player()
            p.base.queryCharTempCardInfo(long(self.currTemplateId))

    def showTemplate(self, templateId):
        self.currTemplateId = templateId
        self.currTemplate = self.cache.get(templateId, None)
        primaryProp = self.currTemplate.get('primaryProp', {})
        self.templateProp = TemplateProp()
        self.templateProp.__dict__.update(primaryProp.__dict__.get('fixedDict', {}))
        self.templateProp.__dict__.update(self.currTemplate.get('showProps', {}))
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_PREVIEW)
        else:
            self.refreshInfo()

    def getItemTipByIndex(self, itemIndex):
        equip = self.currTemplate.get('equipment', {})
        item = equip[itemIndex]
        if item != None:
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BLARENA_TEMPLATE)
        else:
            return

    def setEquips(self):
        equip = self.currTemplate.get('equipment', {})
        if not equip:
            return
        else:
            for i in xrange(PART_EQU_NUM):
                slot = self.widget.getChildByName('slot' + str(i))
                item = None
                if i < len(equip):
                    item = equip[i]
                if slot:
                    slot.dragable = False
                    if item:
                        slotData = uiUtils.getGfxItem(item, appendInfo={'srcType': 'templateRole' + str(i),
                         'itemId': item.id})
                        slot.setItemSlotData(slotData)
                    else:
                        slot.setItemSlotData(None)

            return

    def getPropsArray(self, type):
        ret = []
        for key, val in RPAD.data.items():
            if val['type'] == type:
                ret.append(val)

        ret.sort(key=lambda k: k['displayOrder'])
        return ret

    def setDetailInfo(self):
        commonAttrs = self.createArr(self.common, False)
        primaryProp = self.currTemplate.get('primaryProp', {})
        i2 = 0
        for i in xrange(2, 7):
            attrName = self.widget.getChildByName('attrName' + str(i))
            attrValue = self.widget.getChildByName('attr' + str(i))
            if i2 < len(commonAttrs):
                attrName.textField.htmlText = commonAttrs[i2][0]
                attrValue.textField.htmlText = commonAttrs[i2][1]
            else:
                attrName.textField.htmlText = ''
                attrValue.textField.htmlText = ''
            i2 += 1

        extraPotPoint = primaryProp.gpoint - min(ALD.data.get(self.currTemplate.get('lv', 0), {}).get('maxGPoint', 0), primaryProp.gpoint)
        ASUtils.textFieldAutoSize(self.widget.potPoint, gameStrings.BALANCE_ARENA_QIANNENG % (primaryProp.gpoint - extraPotPoint))
        if extraPotPoint > 0:
            extrStr = '+' + extraPotPoint
        else:
            extrStr = ''
        ASUtils.textFieldAutoSize(self.widget.extraPotPoint, extrStr)
        self.widget.extraPotPoint.visible = False
        self.widget.potPoint.visible = False
        self.removeDataViewData()
        self.itemPos = [0, 0]
        self.currItemIndex = 0
        attackAttrs = self.createArr(self.attack, True)
        self.createDetailItem(attackAttrs)
        defenseAttrs = self.createArr(self.defense, True)
        self.createDetailItem(defenseAttrs)
        advanceAttrs = self.createArr(self.advance, True)
        self.createDetailItem(advanceAttrs)

    def removeDataViewData(self):
        canvas = self.widget.dataView.canvas
        self.widget.removeAllInst(canvas)

    def createDetailItem(self, propList):
        dataView = self.widget.dataView
        for i, item in enumerate(propList):
            detailItem = self.widget.getInstByClsName('BalanceArenaPreview_DetailProps')
            detailItem.id = item[1]
            details = item[0].split('  ')
            detailItem.nameField.htmlText = details[0]
            detailItem.valField.htmlText = details[1]
            detailItem.x = self.itemPos[0]
            detailItem.y = self.itemPos[1]
            if self.currItemIndex % 2 == 0:
                self.itemPos[0] += detailItem.width + 20
            else:
                self.itemPos[0] = 0
                self.itemPos[1] += detailItem.height
            dataView.canvas.addChild(detailItem)
            self.currItemIndex += 1

        dataView.refreshHeight()
        dataView.validateNow()

    def createArr(self, info, isExtra):
        ret = []
        for idx, item in enumerate(info):
            attrStr = self.calcAttr(item.get('showType', ''), item.get('idParam', []))
            if not attrStr:
                continue
            key = str(item['type']) + ',' + str(item['displayOrder'])
            if isExtra:
                ret.append([item['name'] + '  ' + attrStr, key])
            else:
                ret.append([item['name'], attrStr, key])

        return ret

    def useCharTempSuccess(self, tempId):
        if self.widget:
            self.hide()

    def calcAttr(self, showType, idParam):
        primaryAttrStr = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> + %d</font>"
        primaryProp = self.currTemplate.get('primaryProp', {})
        for i, propInfo in enumerate(idParam):
            params, formulaVal = propInfo
            for idx in xrange(len(params)):
                prop = params[idx]
                if prop in PDD.data.PRIMARY_PROPERTIES:
                    if prop == PDD.data.PROPERTY_ATTR_PW:
                        bVal = primaryProp.bpow
                        showType = primaryAttrStr % (bVal, primaryProp.pow - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_INT:
                        bVal = primaryProp.bint
                        showType = primaryAttrStr % (bVal, primaryProp.int - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_PHY:
                        bVal = primaryProp.bphy
                        showType = primaryAttrStr % (bVal, primaryProp.phy - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_SPR:
                        bVal = primaryProp.bspr
                        showType = primaryAttrStr % (bVal, primaryProp.spr - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_AGI:
                        bVal = primaryProp.bagi
                        showType = primaryAttrStr % (bVal, primaryProp.agi - bVal)
                    continue
                pVal = self.getPropValueById(self.templateProp, prop)
                if pVal == None:
                    return
                if prop in (uiConst.PROPERTY_MIN_PHY_ATK,
                 uiConst.PROPERTY_MAX_PHY_ATK,
                 uiConst.PROPERTY_MIN_MAG_ATK,
                 uiConst.PROPERTY_MAX_MAG_ATK):
                    pVal = min(9999, pVal)
                formulaVal = formulaVal.replace('p' + str(idx + 1), str(pVal))

            if showType.find('p' + str(i + 1)) < 0:
                continue
            val = eval(formulaVal)
            placeHolder = '[1.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(int(val)))
            placeHolder = '[2.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(round(val * 100, 1)) + '%')
            placeHolder = '[3.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(round(val, 1)))

        return showType

    def getPropValueById(self, owner, propId):
        if not PD.data.has_key(propId):
            if propId == 20001:
                return owner.atk[0]
            elif propId == 20002:
                return max(owner.atk[0], owner.atk[1])
            elif propId == 20003:
                return owner.atk[2]
            elif propId == 20004:
                return max(owner.atk[2], owner.atk[3])
            elif propId == 20005:
                return owner.defence[0]
            elif propId == 20006:
                return owner.defence[1]
            elif propId == 20007:
                return max(0, int((0.4 * owner.equipAtk[2] + owner.healAdd) * (1 + owner.atkDefRatio[9])))
            elif propId == 20008:
                return max(0, int((0.4 * max(owner.equipAtk[2], owner.equipAtk[3]) + owner.healAdd) * (1 + owner.atkDefRatio[9])))
            else:
                raise Exception('@zs, getPropValueById, propId wrong:%d' % propId)
                return
        return commcalc.getAvatarPropValueById(owner, propId)

    def takePhoto3D(self):
        p = BigWorld.player()
        if not self.headGen:
            self.headGen = capturePhoto.TemplateRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 442)
        if not self.currTemplate:
            return
        physique = self.currTemplate.get('physique', {})
        signal = self.currTemplate.get('signal', {})
        avatarConfig = self.currTemplate.get('avatarConfig', {})
        aspect = self.currTemplate.get('aspect', {})
        if type(aspect) == dict:
            aspect = AppearanceInfo().createObjFromDict(aspect)
        if not physique:
            return
        modelId = charRes.transBodyType(physique.sex, physique.bodyType)
        showFashion = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_FASHION)
        self.headGen.startCaptureRes(modelId, aspect, physique, avatarConfig, ('1101',), showFashion)

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.TemplateRoleInfoPhotoGen.getInstance('gui/taskmask.tga', 442)
        self.headGen.initFlashMesh()

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currTemplate:
            templateData = self.currTemplate
            roleName = templateData.get('roleName', '')
            hostId = templateData.get('hostId', 0)
            mmp = templateData.get('mmp', 9000)
            mhp = templateData.get('mhp', 50000)
            school = templateData.get('school', 0)
            lv = templateData.get('lv', 0)
            gbId = templateData.get('gbID', 0)
            jingJie = templateData.get('jingJie', 0)
            serverName = utils.getServerName(hostId)
            useNum, zanNum = gameglobal.rds.ui.balanceArenaTemplate.getUseAndZan(gbId)
            self.widget.playerName.text = roleName
            self.widget.roleName.text = roleName
            self.widget.serverName.text = serverName
            self.widget.curHp.text = mhp
            self.widget.hpBar.currentValue = mhp
            self.widget.hpBar.maxValue = mhp
            self.widget.curMp.text = mmp
            self.widget.mpBar.bar.gotoAndStop('sp')
            self.widget.mpBar.currentValue = mmp
            self.widget.mpBar.maxValue = mmp
            self.widget.useNum.text = str(useNum)
            self.widget.supportNum.text = str(zanNum)
            if school:
                self.widget.schoolText.text = const.SCHOOL_DICT[school]
            else:
                self.widget.schoolText.text = ''
            self.widget.lvText.text = lv
            self.widget.jingjie.text = utils.jingJie2Name(jingJie)
            self.setEquips()
            self.takePhoto3D()
            self.setDetailInfo()
