#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/summonedSpriteProfileProxy.o
import BigWorld
import gameglobal
import gamelog
import commcalc
import const
import events
from asObject import ASObject
from callbackHelper import Functor
from guis import uiConst
from uiProxy import UIProxy
from guis import ui
from cdata import game_msg_def_data as GMDD
from cdata import prop_def_data as PDD
from data import message_desc_data as MSGDD
from data import summon_sprite_ability_display_data as SSADD
from guis.asObject import ASUtils
from guis.asObject import TipManager
PROPERTY_HEIGHT = 22
SPRITTE_HEIGHT = 23
POINT_ATTR_NAME_LIST = ['attrPw',
 'attrInt',
 'attrPhy',
 'attrSpr',
 'attrAgi']

class SummonedSpriteProfileProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedSpriteProfileProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedSpriteMC = None
        self.selectedSpriteIdx = 1
        self.common = self.getPropsArray(uiConst.COMMON_PROPS)
        self.attack = self.getPropsArray(uiConst.ATTACK_PROPS)
        self.defense = self.getPropsArray(uiConst.DEFENSE_PROPS)
        self.advance = self.getPropsArray(uiConst.ADVANCE_PROPS)

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedSpriteMC = None
        self.selectedSpriteIdx = 1

    def initUI(self):
        self.initSpriteList()

    def initSpriteList(self):
        self.widget.mainMC.spriteList.itemRenderer = 'SummonedSpriteProfile_SpriteScrollWndItem'
        self.widget.mainMC.spriteList.lableFunction = self.itemFunction
        self.widget.mainMC.spriteList.itemHeight = SPRITTE_HEIGHT
        self.widget.mainMC.spriteList.canvas.addEventListener(events.MOUSE_WHEEL, self.handleWheel, False, 1, True)
        self.widget.mainMC.spriteList.scrollbar.addEventListener(events.MOUSE_WHEEL, self.handleWheel, False, 1, True)
        self.widget.mainMC.fightBtn.addEventListener(events.MOUSE_CLICK, self.handleFightClick, False, 1, True)
        self.widget.mainMC.releaseBtn.addEventListener(events.MOUSE_CLICK, self.handleReleaseClick, False, 1, True)
        self.widget.mainMC.lvUpBtn.addEventListener(events.MOUSE_CLICK, self.handleLvUpClick, False, 1, True)
        self.widget.mainMC.summonBtn1.addEventListener(events.MOUSE_CLICK, self.handleSummonClick, False, 1, True)
        self.widget.mainMC.summonBtn2.addEventListener(events.MOUSE_CLICK, self.handleSummonClick, False, 1, True)
        self.widget.mainMC.summonBtn3.addEventListener(events.MOUSE_CLICK, self.handleSummonClick, False, 1, True)
        self.widget.mainMC.summonBtn4.addEventListener(events.MOUSE_CLICK, self.handleSummonClick, False, 1, True)
        self.widget.mainMC.savePointBtn.addEventListener(events.MOUSE_CLICK, self.handleSavePointClick, False, 1, True)
        self.widget.mainMC.resetPointBtn.addEventListener(events.MOUSE_CLICK, self.handleResetPointClick, False, 1, True)
        self.widget.mainMC.attrPwNS.addEventListener(events.INDEX_CHANGE, self.handleAttrNSValueChanged, False, 1, True)
        self.widget.mainMC.attrIntNS.addEventListener(events.INDEX_CHANGE, self.handleAttrNSValueChanged, False, 1, True)
        self.widget.mainMC.attrPhyNS.addEventListener(events.INDEX_CHANGE, self.handleAttrNSValueChanged, False, 1, True)
        self.widget.mainMC.attrSprNS.addEventListener(events.INDEX_CHANGE, self.handleAttrNSValueChanged, False, 1, True)
        self.widget.mainMC.attrAgiNS.addEventListener(events.INDEX_CHANGE, self.handleAttrNSValueChanged, False, 1, True)
        self.widget.mainMC.summonBtn1.visible = False
        self.widget.mainMC.summonBtn2.visible = False
        self.widget.mainMC.summonBtn3.visible = False
        self.widget.mainMC.summonBtn4.visible = False
        self.refreshInfo()

    def handleWheel(self, *args):
        e = ASObject(args[3][0])

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.label = ''
        itemMc.label = itemData.name
        ASUtils.setMcData(itemMc, 'data', itemData)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleSpriteClick, False, 0, True)
        if itemData.index == self.selectedSpriteIdx:
            itemMc.selected = True
            self.selectedSpriteMC = itemMc
            self.refreshSpriteProperty()
        else:
            itemMc.selected = False
        itemMc.validateNow()

    def handleFightClick(self, *args):
        sprite = BigWorld.player().summonSpriteList.get(self.selectedSpriteIdx)
        if not sprite:
            return
        BigWorld.player().base.applySummonSprite(self.selectedSpriteIdx, (0, 0, 0))

    def handleSummonClick(self, *args):
        e = ASObject(args[3][0])
        name = e.currentTarget.name

    def handleReleaseClick(self, *args):
        msg = MSGDD.data.get('releaseSummonedSpriteConfiremMsg', '是否确认放生')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doRelase, self.selectedSpriteIdx), yesBtnText='确定', noCallback=None, noBtnText='取消')

    @ui.checkInventoryLock()
    def doRelase(self, selectedSpriteIdx):
        gamelog.debug('------m.l@SummonedSpriteProfileProxy.doRelase', selectedSpriteIdx)
        BigWorld.player().base.removeSummonSprite(selectedSpriteIdx, BigWorld.player().cipherOfPerson)

    def handleLvUpClick(self, *args):
        gamelog.debug('@smj function removed')

    def handleSavePointClick(self, *args):
        p = BigWorld.player()
        sprite = p.summonSpriteList.get(self.selectedSpriteIdx, {})
        props = sprite.get('props', {})
        pow = self.widget.mainMC.attrPwNS.value - props.get('attrPw', 0)
        int = self.widget.mainMC.attrIntNS.value - props.get('attrInt', 0)
        phy = self.widget.mainMC.attrPhyNS.value - props.get('attrPhy', 0)
        spr = self.widget.mainMC.attrSprNS.value - props.get('attrSpr', 0)
        agi = self.widget.mainMC.attrAgiNS.value - props.get('attrAgi', 0)
        if not pow and not int and not phy and not spr and not agi:
            return
        BigWorld.player().base.onManualAddPorpPoint(self.selectedSpriteIdx, pow, int, phy, spr, agi)

    def handleResetPointClick(self, *args):
        p = BigWorld.player()
        sprite = p.summonSpriteList.get(self.selectedSpriteIdx, {})
        props = sprite.get('props', {})
        for attrName in POINT_ATTR_NAME_LIST:
            getattr(self.widget.mainMC, attrName + 'NS').value = props.get(attrName, 0)

    def handleAttrNSValueChanged(self, *args):
        e = ASObject(args[3][0])
        name = e.currentTarget.name[:-2]
        sprite = BigWorld.player().summonSpriteList.get(self.selectedSpriteIdx)
        if not sprite:
            return
        props = sprite.get('props', {})
        self.checkAttrNSChangable(props)

    def getAvailablePoint(self, props):
        manualPoint = props.get('manualPoint', 0)
        usedPoint = 0
        for attrName in POINT_ATTR_NAME_LIST:
            usedPoint = usedPoint + int(getattr(self.widget.mainMC, attrName + 'NS').value) - props.get(attrName, 0)

        return int(manualPoint - usedPoint)

    def checkAttrNSChangable(self, props):
        if not self.widget:
            return
        availablePoint = self.getAvailablePoint(props)
        for attrName in POINT_ATTR_NAME_LIST:
            if availablePoint <= 0:
                getattr(self.widget.mainMC, attrName + 'NS').nextBtn.enabled = False
            else:
                getattr(self.widget.mainMC, attrName + 'NS').nextBtn.enabled = True
            if getattr(self.widget.mainMC, attrName + 'NS').value <= props.get(attrName, 0):
                getattr(self.widget.mainMC, attrName + 'NS').prevBtn.enabled = False
            else:
                getattr(self.widget.mainMC, attrName + 'NS').prevBtn.enabled = True

        self.widget.mainMC.manualPointTF.text = availablePoint

    def handleSpriteClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedSpriteMC:
            self.selectedSpriteMC.selected = False
            self.selectedSpriteMC = None
        self.selectedSpriteMC = e.currentTarget
        self.selectedSpriteMC.selected = True
        self.selectedSpriteIdx = int(self.selectedSpriteMC.data.index)
        self.refreshSpriteProperty()

    def getPropsTooltip(self, propType, displayOrder):
        key = (propType, displayOrder)
        p = BigWorld.player()
        ret = ''
        data = SSADD.data.get(key, {})
        sprite = p.summonSpriteList.get(self.selectedSpriteIdx)
        if data:
            detail = data.get('detail1', '')
            i = 1
            formulaDate = data.get('formula' + str(i), '')
            while formulaDate:
                for idx, item in enumerate(data.get('formual' + str(i) + 'Params', [])):
                    formulaDate = formulaDate.replace('p' + str(idx + 1), str(commcalc.getSummonedSpritePropValueById(sprite, item)))

                try:
                    val = eval(formulaDate)
                except:
                    val = 0

                detail = detail.replace('[1.p' + str(i) + ']', str(int(val)))
                detail = detail.replace('[2.p' + str(i) + ']', str(round(val * 100, 1)) + '%')
                detail = detail.replace('[3.p' + str(i) + ']', str(round(val, 1)))
                i += 1
                formulaDate = data.get('formula' + str(i), '')

            ret = detail
        return ret

    def createInfo(self):
        common = self.createArr(self.common, False)
        attack = self.createArr(self.attack, True)
        defense = self.createArr(self.defense, True)
        advance = self.createArr(self.advance, True)
        return (common,
         attack,
         defense,
         advance)

    def calcAttr(self, showType, idParam):
        p = BigWorld.player()
        sprite = p.summonSpriteList.get(self.selectedSpriteIdx)
        primaryAttrStr = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> + %d</font>"
        for i, propInfo in enumerate(idParam):
            params, formulaVal = propInfo
            for idx in xrange(len(params)):
                prop = params[idx]
                pVal = commcalc.getSummonedSpritePropValueById(sprite, prop)
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

    def createArr(self, info, isExtra):
        ret = []
        for idx, item in enumerate(info):
            attrStr = ''
            try:
                attrStr = self.calcAttr(item.get('showType', ''), item.get('idParam', []))
            except Exception as e:
                gamelog.debug('----m.l@createArr', idx, item, e.message)

            key = str(item['type']) + ',' + str(item.get('displayOrder', 0))
            ret.append([item['name'],
             attrStr,
             str(item['type']),
             str(item.get('displayOrder', 0))])

        return ret

    def getPropsArray(self, type):
        ret = []
        for key, val in SSADD.data.items():
            if val.get('type', 0) == type:
                ret.append(val)

        ret.sort(key=lambda k: k.get('displayOrder', 0))
        return ret

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.summonSpriteList:
            return
        self.refreshSpriteList()
        self.refreshSpriteProperty()

    def refreshSpriteList(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.summonSpriteList:
            return
        self.spriteInfoList = []
        for key in sorted(p.summonSpriteList.keys()):
            spriteInfo = {}
            sprite = p.summonSpriteList.get(key, {})
            spriteInfo['index'] = key
            spriteInfo['name'] = sprite.get('name', '')
            self.spriteInfoList.append(spriteInfo)

        self.widget.mainMC.spriteList.dataArray = self.spriteInfoList
        self.selectedSpriteIdx = p.summonSpriteList.keys()[0]

    def refreshSpriteProperty(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.summonSpriteList:
            return
        sprite = p.summonSpriteList.get(self.selectedSpriteIdx, {})
        self.refreshSpriteMainProperty(sprite)
        self.refreshSpriteSubProperty(sprite)

    def refreshSpriteMainProperty(self, sprite):
        if not self.widget:
            return
        if not sprite:
            return
        self.widget.mainMC.nameTF.text = sprite.get('name', '')
        self.widget.mainMC.requireLevelTF.text = sprite.get('requireLevel', 0)
        props = sprite.get('props', {})
        manualPoint = props.get('manualPoint', 0)
        self.widget.mainMC.cleverTF.text = '是' if props.get('clever', 0) else '否'
        self.widget.mainMC.expTF.text = props.get('exp', 0)
        self.widget.mainMC.maxExpTF.text = props.get('maxExp', 0)
        self.widget.mainMC.lvTF.text = props.get('lv', 0)
        self.widget.mainMC.lifespanTF.text = props.get('lifespan', 0)
        self.widget.mainMC.sexTF.text = '阳' if props.get('sex', const.SEX_MALE) == const.SEX_MALE else '阴'
        self.widget.mainMC.growthRatioTF.text = '%.3f' % props.get('growthRatio', 0)
        self.widget.mainMC.manualPointTF.text = manualPoint
        self.widget.mainMC.atkTypeTF.text = props.get('atkType', 1)
        self.widget.mainMC.attrPwNS.value = props.get('attrPw', 0)
        self.widget.mainMC.attrIntNS.value = props.get('attrInt', 0)
        self.widget.mainMC.attrPhyNS.value = props.get('attrPhy', 0)
        self.widget.mainMC.attrSprNS.value = props.get('attrSpr', 0)
        self.widget.mainMC.attrAgiNS.value = props.get('attrAgi', 0)
        self.widget.mainMC.aptitudePwTF.text = str(props.get('aptitudePw', 0))
        self.widget.mainMC.aptitudeIntTF.text = str(props.get('aptitudeInt', 0))
        self.widget.mainMC.aptitudePhyTF.text = str(props.get('aptitudePhy', 0))
        self.widget.mainMC.aptitudeSprTF.text = str(props.get('aptitudeSpr', 0))
        self.widget.mainMC.aptitudeAgiTF.text = str(props.get('aptitudeAgi', 0))
        props = sprite.get('props', {})
        BigWorld.callback(0, Functor(self.checkAttrNSChangable, props))

    def refreshSpriteSubProperty(self, sprite):
        if not self.widget:
            return
        if not sprite:
            return
        self.widget.removeAllInst(self.widget.mainMC.propertyView.canvas)
        common, attack, defense, advance = self.createInfo()
        self.createSubMc(attack + defense + advance)
        self.widget.mainMC.propertyView.refreshHeight()

    def createSubMc(self, subInfo):
        for i, info in enumerate(subInfo):
            itemMc = self.widget.getInstByClsName('SummonedSpriteProfile_PropertyDetail')
            itemMc.x = 145 if i % 2 else 0
            itemMc.y = PROPERTY_HEIGHT * int(i / 2)
            itemMc.nameTF.text = info[0]
            itemMc.valueTF.text = info[1]
            self.widget.mainMC.propertyView.canvas.addChild(itemMc)
            tip = self.getPropsTooltip(int(info[2]), int(info[3]))
            TipManager.addTip(itemMc.nameTF, tip)
