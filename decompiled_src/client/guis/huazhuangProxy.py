#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/huazhuangProxy.o
from gamestrings import gameStrings
import math
import BigWorld
import Math
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import clientcom
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from helpers import avatarMorpher as AM
from helpers import avatarMorpherUtils as AMU
from helpers import dyeMorpher
from helpers import charRes
from helpers import tintalt as TA
from data import sys_config_data as SCD
from data import item_data as ID

class HuazhuangProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(HuazhuangProxy, self).__init__(uiAdapter)
        self.bindType = 'huazhuang'
        self.modelMap = {'handleSliderChange': self.onHandleSliderChange,
         'handleFaceZBSlider': self.onHandleFaceZBSlider,
         'handleFaceZBBtn': self.onHandleFaceZBBtn,
         'handleColorBtn': self.onHandleColorBtn,
         'getItem': self.onGetItem,
         'getInitData': self.onGetInitData,
         'getData': self.onGetData,
         'checkItemClick': self.onCheckItemClick,
         'handleOkClick': self.onHandleOkClick,
         'handleCancelClick': self.onHandleCancelClick}
        self.reset()
        self.item = SCD.data.get('huazhuangItems', [240001, 240002])
        self.allUIs = ('yan', 'meizhuang')
        self.itemDict = dict(zip(self.allUIs, self.item))
        uiAdapter.registerEscFunc(uiConst.WIDGET_HUAZHUANG, self.close)

    def reset(self):
        self.refreshUI = True
        self.avatarMorpher = None
        self.hairStyle = 0
        self.avatarData = None
        self.originalAvatarData = None
        self.currentAvatarData = None
        self.med = None
        self.model = None
        self.oldFov = None
        self.isHideAllUI = True
        self.uiName = 'yan'
        self.uiEvent = {}
        self.consumeItemPage = []
        self.consumeItemPos = []
        self.npcEntId = 0

    def onGetItem(self, *arg):
        if self.uiName:
            if not self.uiEvent.has_key(self.uiName):
                self.initUiEvent()
            itemId = self.itemDict[self.uiName]
            data = ID.data.get(itemId, {})
            path = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, data.get('icon'))
            desc = gameStrings.TEXT_HUAZHUANGPLUSPROXY_76 % data.get('name')
            obj = {}
            obj['path'] = path
            obj['desc'] = desc
            obj['itemId'] = itemId
            return uiUtils.dict2GfxDict(obj, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HUAZHUANG:
            self.med = mediator

    def onGetInitData(self, *arg):
        p = BigWorld.player()
        school = p.school
        gender = p.physique.sex
        bodyType = p.physique.bodyType
        bodyIdx = 0
        ar = self.movie.CreateArray()
        if not self.avatarMorpher:
            self.hide()
            return ar
        ar.SetElement(0, GfxValue(gender))
        ar.SetElement(1, GfxValue(bodyType))
        ar.SetElement(2, GfxValue(bodyIdx))
        ar.SetElement(3, GfxValue(school))
        ar.SetElement(4, uiUtils.dict2GfxDict(self.avatarMorpher.morpherLimit))
        ar.SetElement(5, uiUtils.dict2GfxDict(dyeMorpher.getDyeColorFromAvatar(p)))
        return ar

    def onGetData(self, *arg):
        return uiUtils.dict2GfxDict(self.avatarData)

    def show(self, npcEntId = 0):
        self.npcEntId = npcEntId
        p = BigWorld.player()
        if not self.model:
            clientcom.fetchAvatarModel(p, gameglobal.getLoadThread(), self.afterModelFinished)
        else:
            self.afterModelFinished(self.model)

    def afterModelFinished(self, model):
        if not self.model:
            self.model = model
        p = BigWorld.player()
        self.initAvatarMorpher(p)
        if not self.model.inWorld:
            p.addModel(self.model)
        self.model.texturePriority = 100
        self.model.position = p.position
        self.model.yaw = 0
        self.model.action('1101')()
        self.model.expandVisibilityBox(10)
        gameglobal.rds.loginScene.setPlayer(p, self.model)
        c = BigWorld.camera()
        if hasattr(c, 'boundRemain'):
            c.boundRemain = 1.0
        p.hideAllNearby()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self.isHideAllUI = True
        self.uiAdapter.hideAllUI()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HUAZHUANG)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HUAZHUANG)
        p = BigWorld.player()
        p.restoreAllNearby()
        if self.model and self.model.inWorld:
            self.model.texturePriority = 0
            TA.ta_reset([self.model])
            p.delModel(self.model)
        if self.isHideAllUI:
            self.uiAdapter.restoreUI()
            self.isHideAllUI = False
        p.unlockKey(gameglobal.KEY_POS_UI)
        gameglobal.rds.loginScene.setPlayer(None, None)

    def setCamera(self, model, dis = 1.0, fov = 0.6):
        height = (clientcom.getModeNodePosition(model, 'biped Head') - model.position)[1]
        yaw = model.yaw
        pos = model.position + Math.Vector3(math.sin(yaw) * dis, height, math.cos(yaw) * dis)
        dir = Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
        dir *= -1
        m = Math.Matrix()
        m.lookAt(pos, dir, (0, 1, 0))
        pro = BigWorld.projection()
        self.oldFov = pro.fov
        pro.fov = fov
        ca = BigWorld.FreeCamera()
        ca.set(m)
        BigWorld.camera(ca)
        ca.fixed = 1

    def recoverCamera(self):
        BigWorld.camera(gameglobal.rds.cam.cc)
        pro = BigWorld.projection()
        if self.oldFov:
            pro.fov = self.oldFov

    def _refreshFaceAndBody(self, modelId):
        if not self.refreshUI:
            return
        self.refreshUI = False
        self.avatarData = self._fetchAvatarInfo(modelId)

    def _fetchAvatarInfo(self, modelId):
        data = {}
        data.update(self._fetchBodyInfo(modelId))
        data.update(self._fetchFaceInfo(modelId))
        data.update(self._fetchDyeInfo(modelId))
        return data

    def _fetchAvatarColorInfo(self, modelId):
        data = {}
        data.update(self._fetchBodyInfo(modelId))
        data.update(self._fetchFaceInfo(modelId))
        data.update(self._fetchDyeColorInfo(modelId))
        return data

    def _fetchFaceInfo(self, modelId):
        data = {}
        tmpData = {}
        resConfig = AM.getAvatarResConfig(modelId)
        if self.avatarMorpher:
            for k, v in self.avatarMorpher.faceBone.transformMap.iteritems():
                params = AMU.getUIParamByFaceMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

            for k, v in self.avatarMorpher.faceMorpher.transformMap.iteritems():
                params = AMU.getUIParamByFaceMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

        return data

    def _fetchBodyInfo(self, modelId):
        data = {}
        tmpData = {}
        resConfig = AM.getAvatarResConfig(modelId)
        if self.avatarMorpher:
            for k, v in self.avatarMorpher.bodyBone.transformMap.iteritems():
                params = AMU.getUIParamByBodyMorpher(k, v, resConfig)
                if params is not None:
                    self._fillDataValue(data, params[0], params[1], tmpData, v)

        return data

    def _fetchDyeInfo(self, modelId):
        data = {}
        tmpData = {}
        isMale = charRes.retransGender(modelId) == const.SEX_MALE
        if self.avatarMorpher:
            for dyeMorpher in self.avatarMorpher.dyeMorpher.dyeMorphers.itervalues():
                for k, v in dyeMorpher.transformMap.iteritems():
                    params = AMU.getUIParamByDyeMorpher(k, dyeMorpher.getMorphRatio(v), isMale)
                    if params is not None:
                        self._fillDataValue(data, params[0], params[1], tmpData, params[1])

        return data

    def _fetchDyeColorInfo(self, modelId):
        data = {}
        tmpData = {}
        isMale = charRes.retransGender(modelId) == const.SEX_MALE
        if self.avatarMorpher:
            for dyeMorpher in self.avatarMorpher.dyeMorpher.dyeMorphers.itervalues():
                for k, v in dyeMorpher.transformMap.iteritems():
                    params = AMU.getUIParamByDyeMorpher(k, dyeMorpher.getMorphRatio(v), isMale)
                    if params is not None:
                        self._fillDataValue(data, params[0], v[1], tmpData, v[1])

        return data

    def _fillDataValue(self, data, ui, value, tmpData, checkValue):
        tmpValue = tmpData.get(ui)
        if tmpValue:
            return
        tmpData[ui] = checkValue
        data[ui] = value

    def initAvatarMorpher(self, entity):
        if self.avatarMorpher == None:
            mpr = charRes.MultiPartRes()
            avatarConfig = getattr(entity, 'realAvatarConfig', None)
            mpr.queryByAttribute(entity.realPhysique, entity.realAspect, False, avatarConfig, False)
            self.avatarMorpher = AM.SimpleModelMorpher(self.model, entity.physique.sex, entity.physique.school, entity.physique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, 1, entity.availableMorpher)
        modelId = charRes.transDummyBodyType(entity.physique.sex, entity.physique.bodyType, True)
        self.avatarMorpher.readConfig(entity.avatarConfig)
        self._refreshFaceAndBody(modelId)
        self.originalAvatarData = self._fetchAvatarColorInfo(modelId)

    def onHandleSliderChange(self, *arg):
        sliderName = arg[3][0].GetString()
        value = float(arg[3][1].GetNumber())
        self._onHandleSliderChange(sliderName, value)

    def _onHandleSliderChange(self, sliderName, value, enableApply = True):
        p = BigWorld.player()
        modelId = charRes.transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
        gamelog.debug('b.e.:onHandleFaceSlider', sliderName, value)
        if not self.avatarMorpher:
            return
        else:
            resConfig = AM.getAvatarResConfig(modelId)
            if sliderName in AMU.FACE_U2M_MAPPING.keys():
                params = AMU.getFaceMorpherParamByUI(sliderName, value, resConfig)
                if params is None:
                    return
                if params[0] == 0:
                    if enableApply:
                        self.avatarMorpher.setAndApplyFaceBoneMorph(params[1], params[2], params[3])
                    else:
                        self.avatarMorpher.setFaceBoneMorph(params[1], params[2], params[3])
                elif enableApply:
                    self.avatarMorpher.setAndApplyFaceMorph(params[1], params[2], params[3])
                else:
                    self.avatarMorpher.setFaceMorph(params[1], params[2], params[3])
            else:
                params = AMU.getBodyMorpherParamByUI(sliderName, value, resConfig)
                if params is None:
                    return
                if params[0] == 0:
                    if enableApply:
                        self.avatarMorpher.setAndApplyBodyBoneMorph(params[1], params[2], params[3])
                    else:
                        self.avatarMorpher.setBodyBoneMorph(params[1], params[2], params[3])
            return

    def onHandleFaceZBBtn(self, *arg):
        key = arg[3][0].GetString()
        value = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        isMale = p.physique.isMale()
        if not self.avatarMorpher:
            return
        elif key == 'faxing_style':
            self.avatarMorpher.setHairStyle(value)
            self.saveMorpher(p)
            return
        elif key == 'mobanItem':
            self.onClickCharacter(value)
            return
        elif key == 'faxing_color1':
            key = 'faxing_color'
            params = AMU.getDyeMorpherParamByUI(key, value, isMale)
            value = ('%d' % params[2], 'faxing_color1')
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)
            return
        else:
            params = AMU.getDyeMorpherParamByUI(key, value, isMale)
            gamelog.debug('b.e.:onHandleFaceZBBtn', key, value, params)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], params[2])
            return

    def onHandleFaceZBSlider(self, *arg):
        key = arg[3][0].GetString()
        value = float(arg[3][1].GetNumber())
        p = BigWorld.player()
        isMale = p.physique.isMale()
        gamelog.debug('b.e.:onHandleFaceZBSlider', key, value)
        if not self.avatarMorpher:
            return
        else:
            params = AMU.getDyeMorpherParamByUI(key, value, isMale)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                gamelog.debug('onHandleFaceZBSlider', params, AMU.DYE_MORPH_BINDING[params[1]])
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], params[2])
            return

    def onHandleColorBtn(self, *arg):
        key = arg[3][0].GetString()
        r = int(arg[3][1].GetNumber())
        g = int(arg[3][2].GetNumber())
        b = int(arg[3][3].GetNumber())
        alpha = int(arg[3][4].GetNumber())
        if alpha == 0:
            alpha = 255
        value = ('%d,%d,%d,%d' % (r,
          g,
          b,
          alpha),)
        if key == 'faxing_color1':
            key = 'faxing_color'
            value = value + ('faxing_color1',)
        p = BigWorld.player()
        isMale = p.physique.isMale()
        if not self.avatarMorpher:
            return
        else:
            params = AMU.getDyeMorpherParamByUI(key, 0, isMale)
            if params is None:
                return
            if params[1] in AMU.DYE_MORPH_BINDING.keys():
                self.avatarMorpher.setAndApplyDyeMorph(params[0], AMU.DYE_MORPH_BINDING[params[1]], params[2])
            self.avatarMorpher.setAndApplyDyeMorph(params[0], params[1], value)
            return

    def onCheckItemClick(self, *arg):
        self.uiName = arg[3][0].GetString()
        p = BigWorld.player()
        dstPage, dstPos = p.inv.findItemInPages(uiUtils.getParentId(self.itemDict[self.uiName]), enableParentCheck=True)
        if dstPage == const.CONT_NO_PAGE and dstPos == const.CONT_NO_POS:
            return GfxValue(False)
        return GfxValue(True)

    def initUiEvent(self):
        array = self.med.Invoke('getAllItemInSubUI')
        l = array.GetArraySize()
        self.uiEvent[self.uiName] = []
        for i in xrange(0, l):
            key = array.GetElement(i).GetString()
            self.uiEvent[self.uiName].append(key)

    def close(self):
        p = BigWorld.player()
        modelId = charRes.transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
        self.currentAvatarData = self._fetchAvatarColorInfo(modelId)
        if self.currentAvatarData == self.originalAvatarData:
            self.hide()
            return
        consumeItems = {}
        for uiName, keys in self.uiEvent.iteritems():
            for key in keys:
                if self.currentAvatarData[key] != self.originalAvatarData[key]:
                    itemId = self.itemDict[uiName]
                    itemName = ID.data.get(itemId, {}).get('name', '')
                    if itemName not in consumeItems:
                        consumeItems[itemName] = 1
                    else:
                        consumeItems[itemName] += 1
                    break

        msg = []
        for key, value in consumeItems.iteritems():
            msg.append('%sx%d' % (key, value))

        self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.TEXT_HUAZHUANGPLUSPROXY_399 % ','.join(msg), self.saveAndClose, gameStrings.TEXT_DYEPLANEPROXY_444, self.hide, gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def saveAndClose(self):
        p = BigWorld.player()
        self.consumeItemPage = []
        self.consumeItemPos = []
        for uiName, keys in self.uiEvent.iteritems():
            for key in keys:
                if self.currentAvatarData[key] != self.originalAvatarData[key]:
                    itemId = self.itemDict[uiName]
                    itemName = ID.data.get(itemId, {}).get('name', '')
                    dstPage, dstPos = p.inv.findItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
                    if not (dstPage == const.CONT_NO_PAGE and dstPos == const.CONT_NO_POS):
                        self.consumeItemPage.append(dstPage)
                        self.consumeItemPos.append(dstPos)
                    else:
                        msg = gameStrings.TEXT_HUAZHUANGPLUSPROXY_417 % itemName
                        self.uiAdapter.systemTips.show(msg)
                        return
                    break

        if self.consumeItemPage and self.consumeItemPos:
            avatarConfig = self.avatarMorpher.export(p.avatarConfig)
            if self.npcEntId:
                npc = BigWorld.entity(self.npcEntId)
                if npc and npc.inWorld:
                    npc.cell.huazhuangItem(avatarConfig, 0, self.consumeItemPage, self.consumeItemPos)
            else:
                p.cell.huazhuangItem(avatarConfig, 0, self.consumeItemPage, self.consumeItemPos)
            self.hide()

    def onHandleOkClick(self, *arg):
        self.close()

    def onHandleCancelClick(self, *arg):
        self.hide()
