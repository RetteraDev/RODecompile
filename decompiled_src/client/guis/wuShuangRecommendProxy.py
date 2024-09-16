#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wuShuangRecommendProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import skillDataInfo
import const
from Scaleform import GfxValue
from uiProxy import UIProxy
from guis import asObject
from guis import tipUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from gameStrings import gameStrings
from data import skill_general_template_data as SGTD
from cdata import game_msg_def_data as GMDD
WUSHUANG_SLOT_KEY = [12,
 13,
 14,
 15,
 16,
 17]
DAO_HANG_NUM = 5
TITLE_NUM = 2
TITLE_NAMES = {const.SCHOOL_SHENTANG: ('TianFa', 'ShenYou'),
 const.SCHOOL_YUXU: ('WanXiang', 'XingLuo'),
 const.SCHOOL_GUANGREN: ('WenQing', 'WenDao'),
 const.SCHOOL_YANTIAN: ('YanSha', 'TianShu'),
 const.SCHOOL_LINGLONG: ('QiaoYu', 'HuaYan'),
 const.SCHOOL_LIUGUANG: ('JiMie', 'YanGuang'),
 const.SCHOOL_YECHA: ('YeSha1', 'YeSha2')}

class WuShuangRecommendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WuShuangRecommendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.wsSkillInfo = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WUSHUANG_RECOMMEND, self.hidePanel)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        if self.initData():
            self.refreshPanel()

    def initData(self):
        p = BigWorld.player()
        self.wsSkillInfo = getattr(p, 'carrerGuideData', {}).get('wsSkillInfo', {})
        if not self.wsSkillInfo:
            BigWorld.player().showGameMsg(GMDD.data.WU_SHUANG_RECOMMM_NOT_EXIST, ())
            self.clearWidget()
            return False
        return True

    def refreshPanel(self):
        self.setTitle()
        for i in xrange(0, len(WUSHUANG_SLOT_KEY)):
            skillIcon = self.widget.getChildByName('skillIcon%d' % i)
            daoHangMc = self.widget.getChildByName('daoHangMc%d' % i)
            skillId = self.wsSkillInfo.get(WUSHUANG_SLOT_KEY[i], [])[0]
            sd = skillDataInfo.ClientSkillInfo(skillId)
            icon = sd.getSkillData('icon', None)
            data = {'iconPath': 'skill/icon64/%s.dds' % icon}
            skillIcon.slot.setItemSlotData(data)
            skillIcon.slot.dragable = False
            skillIcon.slot.keyBind.text = ''
            skillName = SGTD.data.get(skillId, {}).get('name', '')
            skillIcon.skillName.textField.text = skillName
            skillIcon.slot.validateNow()
            daoHangArray = self.wsSkillInfo.get(WUSHUANG_SLOT_KEY[i], [])[1]
            extraInfo = self.getExtraInfo(daoHangArray)
            TipManager.addTipByType(skillIcon.slot, tipUtils.TYPE_WS_SKILL, {'skillId': skillId,
             'lv': 0,
             'extraInfo': extraInfo})
            self.daoHangMc = daoHangMc
            for d in daoHangArray:
                idx = d - 1
                realIdx = uiConst.WUSHUANG_IDX[idx]
                daoHang = daoHangMc.getChildByName('daoHang%d' % realIdx)
                daoHang.gotoAndPlay('activation')
                daoHang.num.text = DAO_HANG_NUM
                daoHang.num.gotoAndStop('five')
                self.daoHang = daoHang

        self.widget.confirm.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn)
        self.widget.cancel.addEventListener(events.MOUSE_CLICK, self.handleClickCancel)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancel)

    def setTitle(self):
        p = BigWorld.player()
        for i in xrange(0, TITLE_NUM):
            school = p.school
            self.widget.getChildByName('wushuang%d' % i).gotoAndStop(TITLE_NAMES[school][i])

    def getExtraInfo(self, daoHangArray):
        extraInfo = {'windCnt': 0,
         'forestCnt': 0,
         'hillCnt': 0,
         'fireCnt': 0}
        for d in daoHangArray:
            idx = d - 1
            if uiConst.WUSHUANG_IDX[idx] == uiConst.WIND_TYPE:
                extraInfo['windCnt'] = 5
            elif uiConst.WUSHUANG_IDX[idx] == uiConst.WOOD_TYPE:
                extraInfo['forestCnt'] = 5
            elif uiConst.WUSHUANG_IDX[idx] == uiConst.HILL_TYPE:
                extraInfo['hillCnt'] = 5
            elif uiConst.WUSHUANG_IDX[idx] == uiConst.FIRE_TYPE:
                extraInfo['fireCnt'] = 5

        return extraInfo

    def show(self):
        p = BigWorld.player()
        if not self.widget and hasattr(p, 'carrerGuideData'):
            self.uiAdapter.loadWidget(uiConst.WIDGET_WUSHUANG_RECOMMEND)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WUSHUANG_RECOMMEND)

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().cell.applyWuShuangGuideData()

    def handleClickCancel(self, *args):
        self.clearWidget()

    def hidePanel(self):
        self.clearWidget()
