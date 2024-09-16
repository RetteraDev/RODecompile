#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhanQiMorpherFactory.o
import BigWorld
import const
import gameglobal
import uiConst
import gametypes
import random
import utils
import uiUtils
from gameclass import Singleton
from Scaleform import GfxValue
from ui import gbk2unicode
from helpers import tintalt as TA
from data import guild_config_data as GCD
ZHAN_QI_DDS_PATH = 'zhanqi/'
DYE_INDEX_MAP = {uiConst.ZHAN_QI_MORPHER_HUIJI: (2,),
 uiConst.ZHAN_QI_MORPHER_STYLE: (0,),
 uiConst.ZHAN_QI_MORPHER_BG: (1,),
 uiConst.ZHAN_QI_MORPHER_LOCATION: (6, 7),
 uiConst.ZHAN_QI_MORPHER_DYE: (3, 4, 5)}
TYPE_TEXTURE = 1
TYPE_TABLE = 2
TYPE_EXACT = 3
TYPE_EXACT_STR = 4
ZHANQI_I2M_MAPPING = {0: ('ma_a', TYPE_TEXTURE),
 1: ('mb', TYPE_TEXTURE),
 2: ('mc', TYPE_TEXTURE),
 3: ('zhanQiBGColor', TYPE_TABLE),
 4: ('zhanQiStyleColor', TYPE_TABLE),
 5: ('zhanQiHuiJiColor', TYPE_TABLE),
 6: ('C_tuyang_daxiao', TYPE_EXACT),
 7: ('C_tuyang_weiyi', TYPE_EXACT_STR)}
FLAG_HUIJI_TEXTURE = 2
FLAG_HUIJI_COLOR = 5
FLAG_HUIJI_SIZE = 6

class IMorpherInfo(object):

    def __init__(self, tag):
        self.tag = tag
        self.dds = []
        self.index = 0

    def getDDS(self):
        ret = gameglobal.rds.ui.movie.CreateArray()
        for i in xrange(len(self.dds) / 4 + 1):
            ar = gameglobal.rds.ui.movie.CreateArray()
            for j in xrange(4):
                if i * 4 + j < len(self.dds):
                    ar.SetElement(j, GfxValue(ZHAN_QI_DDS_PATH + str(self.dds[i * 4 + j]) + '.dds'))

            ret.SetElement(i, ar)

        return ret

    def setIndex(self, value):
        self.index = value

    def read(self, config):
        self.index = config[DYE_INDEX_MAP[self.tag][0]]

    def export(self):
        return {DYE_INDEX_MAP[self.tag][0]: self.index}

    def chooseRandomVal(self):
        self.index = random.randint(0, len(self.dds) - 1)

    def getSelectedInfo(self):
        return {self.tag: self.index}


class HuiJiSubPicMorpher(IMorpherInfo):

    def __init__(self, parentTag, tag):
        super(HuiJiSubPicMorpher, self).__init__(tag)
        self.parentTag = parentTag
        self.dds = GCD.data.get('zhanQiHuiJiPic', [])

    def export(self):
        return {DYE_INDEX_MAP[self.parentTag][0]: self.index}

    def exportShow(self):
        return {DYE_INDEX_MAP[self.parentTag][0]: self.index}


class HuiJiSubWordMorpher(IMorpherInfo):

    def __init__(self, parentTag, tag):
        super(HuiJiSubWordMorpher, self).__init__(tag)


class HuiJiSubUserDefineMorpher(IMorpherInfo):

    def __init__(self, parentTag, tag):
        super(HuiJiSubUserDefineMorpher, self).__init__(tag)
        self.parentTag = parentTag
        self.dds = []
        self.isUsed = False

    def isLoadedDDSSucc(self):
        return len(self.dds) > 0

    def setDDS(self, ddsName):
        self.dds = [int(ddsName)]
        self.index = 0

    def export(self):
        return {DYE_INDEX_MAP[self.parentTag][0]: BigWorld.player().guildIcon}

    def exportShow(self):
        fileName = gameglobal.rds.ui.zhanQi.fileName
        return {DYE_INDEX_MAP[self.parentTag][0]: const.IMAGES_SHOW_PREFIX + fileName}


class HuiJiMorpherInfo(IMorpherInfo):

    def __init__(self, tag):
        super(HuiJiMorpherInfo, self).__init__(tag)
        self.subMorpherIns = {}
        self._createSubInstance()
        self.curSubMorpher = self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC]

    def _createSubInstance(self):
        self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC] = HuiJiSubPicMorpher(self.tag, uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC)
        self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE] = HuiJiSubUserDefineMorpher(self.tag, uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE)

    def export(self):
        if self.curSubMorpher.tag == uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE and self.curSubMorpher.isUsed:
            return self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE].export()
        else:
            return self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC].export()

    def exportShow(self):
        if self.curSubMorpher.tag == uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE:
            return self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_USER_DEFINE].exportShow()
        else:
            return self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC].exportShow()

    def setCurSubMorpher(self, subType):
        self.curSubMorpher = self.subMorpherIns[subType]

    def getCurSubMorpher(self):
        return self.curSubMorpher

    def read(self, config):
        for morpher in self.subMorpherIns.itervalues():
            morpher.read(config)

    def getSelectedInfo(self):
        return {self.tag: self.subMorpherIns[uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC].index}

    def chooseRandomVal(self):
        self.curSubMorpher.chooseRandomVal()


class StyleMorpherInfo(IMorpherInfo):

    def __init__(self, tag):
        super(StyleMorpherInfo, self).__init__(tag)
        self.dds = GCD.data.get('zhanQiStyle', [])


class BGMorpherInfo(IMorpherInfo):

    def __init__(self, tag):
        super(BGMorpherInfo, self).__init__(tag)
        self.dds = GCD.data.get('zhanQiBG', [])


class LocationMorpher(IMorpherInfo):

    def __init__(self, tag):
        super(LocationMorpher, self).__init__(tag)
        self.location = [0.0, 0.0]
        self.size = 2.0

    def setIndex(self, value):
        self.size = value

    def setLocation(self, location):
        self.location[0] += location[0]
        self.location[1] += location[1]

    def export(self):
        ret = {}
        map = DYE_INDEX_MAP[self.tag]
        index = [self.size, self.location]
        for i, item in enumerate(map):
            ret[item] = index[i]

        return ret

    def read(self, config):
        map = DYE_INDEX_MAP[self.tag]
        self.size = config[map[0]]
        self.location = config[map[1]]

    def chooseRandomVal(self):
        self.size = random.random() * 5.0
        self.location = [random.random(), random.random()]

    def getSelectedInfo(self):
        return {}


class DyeMorpher(IMorpherInfo):

    def __init__(self, tag):
        super(DyeMorpher, self).__init__(tag)
        configData = GCD.data
        self.styleColor = configData.get('zhanQiStyleColor', ())
        self.bgColor = configData.get('zhanQiBGColor', ())
        self.huiJiColor = configData.get('zhanQiHuiJiColor', ())
        self.styleColorIndex = 0
        self.bgColorIndex = 0
        self.huiJiColorIndex = 0

    def getColorDesc(self):
        ret = gameglobal.rds.ui.movie.CreateObject()
        styleAr = gameglobal.rds.ui.movie.CreateArray()
        for index, color in enumerate(self.styleColor):
            styleAr.SetElement(index, GfxValue(gbk2unicode(color[3])))

        ret.SetMember('zhanQiStyleColor', styleAr)
        bgAr = gameglobal.rds.ui.movie.CreateArray()
        for index, color in enumerate(self.bgColor):
            bgAr.SetElement(index, GfxValue(gbk2unicode(color[3])))

        ret.SetMember('zhanQiBGColor', bgAr)
        huiJiAr = gameglobal.rds.ui.movie.CreateArray()
        for index, color in enumerate(self.huiJiColor):
            huiJiAr.SetElement(index, GfxValue(gbk2unicode(color[3])))

        ret.SetMember('zhanQiHuiJiColor', huiJiAr)
        return ret

    def setIndex(self, btnName, value):
        if btnName == 'zhanQi_color':
            self.styleColorIndex = value
        elif btnName == 'huiji_color':
            self.huiJiColorIndex = value
        elif btnName == 'bg_color':
            self.bgColorIndex = value

    def export(self):
        ret = {}
        map = DYE_INDEX_MAP[self.tag]
        index = [self.bgColorIndex, self.styleColorIndex, self.huiJiColorIndex]
        for i, item in enumerate(map):
            ret[item] = index[i]

        return ret

    def read(self, config):
        map = DYE_INDEX_MAP[self.tag]
        val = []
        for item in map:
            val.append(config[item])

        self.bgColorIndex, self.styleColorIndex, self.huiJiColorIndex = val

    def chooseRandomVal(self):
        self.styleColorIndex = random.randint(0, len(self.styleColor) - 1)
        self.bgColorIndex = random.randint(0, len(self.bgColor) - 1)
        self.huiJiColorIndex = random.randint(0, len(self.huiJiColor) - 1)

    def getSelectedInfo(self):
        return {self.tag: {'zhanQiStyleColor': self.styleColorIndex,
                    'zhanQiBGColor': self.bgColorIndex,
                    'zhanQiHuiJiColor': self.huiJiColorIndex}}


class ZhanQiMorpherFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.resetMorpherIns()
        self.createMorpherIns()

    def createMorpherIns(self):
        try:
            self.morpherIns[uiConst.ZHAN_QI_MORPHER_HUIJI] = HuiJiMorpherInfo(uiConst.ZHAN_QI_MORPHER_HUIJI)
            self.morpherIns[uiConst.ZHAN_QI_MORPHER_STYLE] = StyleMorpherInfo(uiConst.ZHAN_QI_MORPHER_STYLE)
            self.morpherIns[uiConst.ZHAN_QI_MORPHER_BG] = BGMorpherInfo(uiConst.ZHAN_QI_MORPHER_BG)
            self.morpherIns[uiConst.ZHAN_QI_MORPHER_LOCATION] = LocationMorpher(uiConst.ZHAN_QI_MORPHER_LOCATION)
            self.morpherIns[uiConst.ZHAN_QI_MORPHER_DYE] = DyeMorpher(uiConst.ZHAN_QI_MORPHER_DYE)
        except:
            print '@hjx error createMorpherIns'

    def resetMorpherIns(self):
        self.morpherIns = {}

    def export(self):
        ret = {}
        for morpher in self.morpherIns.itervalues():
            ret.update(morpher.export())

        return str(ret)

    def reset(self):
        self.resetMorpherIns()
        self.createMorpherIns()

    def exportShow(self):
        ret = {}
        for morpher in self.morpherIns.itervalues():
            if hasattr(morpher, 'exportShow'):
                info = morpher.exportShow()
            else:
                info = morpher.export()
            ret.update(info)

        return str(ret)

    def read(self, config):
        try:
            config = eval(config)
        except:
            return

        for morpher in self.morpherIns.itervalues():
            morpher.read(config)

    def getSelectedInfo(self):
        selectedInfo = {}
        for morpher in self.morpherIns.itervalues():
            selectedInfo.update(morpher.getSelectedInfo())

        return uiUtils.dict2GfxDict(selectedInfo)

    def applyRondomMorpher(self):
        self.morpherIns[uiConst.ZHAN_QI_MORPHER_HUIJI].setCurSubMorpher(uiConst.ZHAN_QI_MORPHER_SUB_HUIJI_PIC)
        for morpher in self.morpherIns.itervalues():
            morpher.chooseRandomVal()

    def readConfigFromPlayer(self):
        p = BigWorld.player()
        if p.guild:
            clanWarFlagMorpher = eval(p.guild.clanWarFlagMorpher)
            if utils.isDownloadImage(clanWarFlagMorpher[2]):
                if p.guildFlagIconStatus == gametypes.NOS_FILE_STATUS_APPROVED:
                    self.read(p.guild.clanWarFlagMorpher)
                else:
                    clanWarFlagMorpher[2] = '0'
                    self.read(str(clanWarFlagMorpher))
            else:
                self.read(p.guild.clanWarFlagMorpher)


def getInstance():
    return ZhanQiMorpherFactory.getInstance()


class ZhanqiDyeMorpher(object):
    TEXTURE_PATH = 'char/%d/texture/%d_%s_%d.tga'
    HUIJI_TEXTURE_PATH = 'char/%d/texture/%d_%s_%d_a.tga'
    HUIJI_CLASS = 2
    MATTER = 'flag'
    TINT_NAME = 'flag'
    DYE_COUNT = 8

    def __init__(self, model, modelId):
        super(ZhanqiDyeMorpher, self).__init__()
        self.model = model
        self.modelId = modelId
        self.configData = GCD.data
        self.param = []

    def read(self, config):
        try:
            config = eval(config)
        except:
            config = {}

        self.param = []
        if config:
            for i in xrange(self.DYE_COUNT):
                value = config.get(i, 0)
                type_value, type = ZHANQI_I2M_MAPPING.get(i)
                if i == FLAG_HUIJI_COLOR and config.get(FLAG_HUIJI_TEXTURE, 0) >= uiConst.ZHAN_QI_HUIJI_PIC_LIMIT:
                    value = '1.0 1.0 1.0 1.0'
                    self.param.append(value)
                elif type == TYPE_TEXTURE:
                    if i == self.HUIJI_CLASS:
                        if uiUtils.isDownloadImage(value):
                            path = const.IMAGES_DOWNLOAD_DIR.replace('\\', '/')
                            self.param.append('%s/%s.dds' % (path, value))
                        elif uiUtils.isZhanQiShowImage(value):
                            path = const.IMAGES_DOWNLOAD_DIR.replace('\\', '/')
                            fileName = value[len(const.IMAGES_SHOW_PREFIX):]
                            self.param.append('%s/%s.dds' % (path, fileName))
                        else:
                            self.param.append(self.HUIJI_TEXTURE_PATH % (self.modelId,
                             self.modelId,
                             type_value,
                             uiUtils.calTextureVal(value)))
                    else:
                        self.param.append(self.TEXTURE_PATH % (self.modelId,
                         self.modelId,
                         type_value,
                         uiUtils.calTextureVal(value)))
                elif type == TYPE_TABLE:
                    value = self.configData.get(type_value, [])[value]
                    value = '%.2f %.2f %.2f 1.0' % (value[0] / 255.0, value[1] / 255.0, value[2] / 255.0)
                    self.param.append(value)
                elif type == TYPE_EXACT:
                    self.param.append(value)
                elif type == TYPE_EXACT_STR:
                    if value == 0:
                        value = (0, 0)
                    self.param.append('%.2f %.2f 0 0' % tuple(value))

    def apply(self):
        if self.param and self.model:
            for texture in self.param:
                texture = str(texture).strip()
                if texture.endswith('.tga') or texture.endswith('.dds'):
                    self.model.addTintFxTexture(texture)

            TA.addExtraTint(self.model, self.TINT_NAME, self.param, 0, self.MATTER)

    def genDefaultParam(self):
        p = BigWorld.player()
        if p.guild:
            clanWarFlagMorpher = eval(p.guild.clanWarFlagMorpher)
            if utils.isDownloadImage(clanWarFlagMorpher[2]):
                if p.guildFlagIconStatus == gametypes.NOS_FILE_STATUS_APPROVED:
                    self.read(p.guild.clanWarFlagMorpher)
                else:
                    clanWarFlagMorpher[2] = '0'
                    self.read(str(clanWarFlagMorpher))
            else:
                self.read(p.guild.clanWarFlagMorpher)
        else:
            self.read(str({FLAG_HUIJI_SIZE: 2}))


class NoticeBoardMorpher(object):
    MATTER = 'logo'
    TINT_NAME = 'logo'

    def __init__(self, model):
        super(NoticeBoardMorpher, self).__init__()
        self.model = model
        self.param = []

    def read(self, texturePath):
        self.param = [texturePath, texturePath]

    def apply(self):
        if self.param and self.model:
            for texture in self.param:
                texture = str(texture).strip()
                if texture.endswith('.tga') or texture.endswith('.dds'):
                    self.model.addTintFxTexture(texture)

            TA.addExtraTint(self.model, self.TINT_NAME, self.param, 0, self.MATTER)
