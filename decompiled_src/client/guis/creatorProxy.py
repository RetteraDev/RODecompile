#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/creatorProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import Creator
import const
import gameglobal
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import DataProxy
from guis import uiConst

class CreatorProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(CreatorProxy, self).__init__(uiAdapter)
        self.bindType = 'creator'
        self.bShowPro = False
        self.modelMap = {'registerCreatorOptionsPage': self.onRegisterCreatorOptionsPage,
         'creatorOptionsPageListItemClick': self.onListItemClick,
         'creatorProPageConfirmBtnClick': self.onConfirmBtnClick,
         'creatorProGenFishBtnClick': self.onGenFishBtnClick,
         'isHideGenFishBtn': self.onIsHideGenFishBtn}
        self.fishCnt = 0
        self.entType = ''

    def getValue(self, key):
        if key == 'creatorOpt.list':
            ar = self.movie.CreateArray()
            self.desc = Creator.Obj.desc
            i = 0
            for t in copy.copy(self.desc.keys()):
                if not self.desc[t].has_key(t):
                    raise Exception('%s should be configured in gmEntity[entityDescDict][%s]' % (t, t))
                ar.SetElement(i, GfxValue(gbk2unicode(t + ':' + self.desc[t][t])))
                i = i + 1

            return ar
        if key == 'creatorPro.list':
            ar = self.movie.CreateArray()
            self.entType = Creator.Obj.entType
            self.property = copy.copy(Creator.Obj.property)
            i = 0
            for name in self.property:
                data = self.movie.CreateArray()
                data.SetElement(0, GfxValue(gbk2unicode(name)))
                data.SetElement(1, GfxValue(gbk2unicode(self.desc[self.entType][name])))
                data.SetElement(2, GfxValue(gbk2unicode(str(self.property[name]))))
                ar.SetElement(i, data)
                i = i + 1

            return ar

    def onRegisterCreatorOptionsPage(self, *arg):
        self.handler = arg[3][0]

    def onListItemClick(self, *arg):
        clickItem = arg[3][0].GetNumber()
        entity = BigWorld.entity(Creator.Obj.id)
        if entity is None:
            return
        else:
            urs = gameglobal.rds.ui.loginWin.userName
            entity.cell.querySpec(urs, self.desc.keys()[int(clickItem)])
            return

    def getType(self, proName):
        if self.entType == 'FishSpawnPoint' and proName.find('spawnPointList') != -1:
            _type = tuple
        else:
            _type = type(self.property[proName])
        return _type

    def onConfirmBtnClick(self, *arg):
        listVal = arg[3][0]
        listName = arg[3][1]
        for i in xrange(listName.GetArraySize()):
            value = listVal.GetElement(i)
            newValue = unicode2gbk(value.GetString())
            name = listName.GetElement(i).GetString()
            _type = self.getType(name)
            if _type != str:
                if newValue:
                    self.property[name] = eval(newValue)
            else:
                self.property[name] = newValue

        Creator.Obj.onEdited(self.entType, self.property)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CREATOR_PROPAGE)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CREATOR_OPTIONPAGE)
        self.fishCnt = 0

    def onGenFishBtnClick(self, *arg):
        p = BigWorld.player()
        fishPointVal = (p.position, (p.pitch, p.roll, p.yaw))
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(const.FISH_SP_LIST + str(self.fishCnt)))
        ret.SetElement(1, GfxValue(gbk2unicode(gameStrings.TEXT_CREATORPROXY_106 + str(self.fishCnt))))
        ret.SetElement(2, GfxValue(str(fishPointVal)))
        self.fishCnt += 1
        return ret

    def onIsHideGenFishBtn(self, *arg):
        return GfxValue(self.entType != 'FishSpawnPoint')

    def _asTuple(self, mt, name):
        mt = mt.strip(')')
        mt = mt.strip('(')
        mt = mt.rstrip(',')
        eles = mt.split(',')
        ret = []
        t = self.getType(name)
        for e in eles:
            ret.append(t(e))

        return tuple(ret)

    def addItem(self, str):
        self.handler.Invoke('addItem', GfxValue(gbk2unicode(str)))

    def showCreatorOptionsPage(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CREATOR_OPTIONPAGE)

    def showCreatorProPage(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CREATOR_PROPAGE)
