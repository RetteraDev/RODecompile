#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ime.o
import BigWorld
import gameglobal
INPUT_LEFT = 'ime/input_left.wap'
INPUT_MIDDLE = 'ime/input_middle.wap'
INPUT_RIGHT = 'ime/input_right.wap'
INPUT_PAGE_UP = 'ime/pageup.wap'
INPUT_PAGE_DOWN = 'ime/pagedown.wap'
g_imeObj = None
INPUT_MAIN_GUI = 'ime/waiting.wap'
INPUT_MAIN_CHINESE = 'ime/chinese.wap'
INPUT_MAIN_ENGLISH = 'ime/english.wap'
INPUT_MAIN_BANJIAO = 'ime/banjiao.wap'
INPUT_MAIN_QUANJIAO = 'ime/quanjiao.wap'
INPUT_MAIN_ENGLISH_BIAODIAN = 'ime/english_biaodian.wap'
INPUT_MAIN_CHINESE_BIAODIAN = 'ime/chinese_biaodian.wap'

class ImeMainGUI:

    def __init__(self):
        global g_imeObj
        self.HKLMap = {}
        self.currentHKL = 0
        self.allImeHKL = None
        g_imeObj = self

    def update(self):
        comp, candidate = BigWorld.getImeComp()
        if BigWorld.isImeChinese() == False:
            comp = ''
        self.setcmp_candidate(comp, candidate)

    def setcmp_candidate(self, comp, candidate):
        if candidate:
            gameglobal.rds.ui.ime.setCandidate(comp, candidate)
        if comp == '':
            gameglobal.rds.ui.ime.hideMenu(True)
        else:
            gameglobal.rds.ui.ime.hideMenu(False)
        self.__updateIcon()

    def setHKL(self, hkl):
        if not BigWorld.enableNtIme():
            return
        else:
            self.__updateIcon()
            return
            if self.currentHKL == 0 and hkl != 0:
                pos = BigWorld.getEditPos()
                if pos != None:
                    self.setCompPos(pos[0], pos[1])
            self.currentHKL = hkl
            if not BigWorld.enableNtIme():
                return
            if self.allImeHKL == None:
                self.allImeHKL = BigWorld.getAllIme()
                if self.allImeHKL:
                    for i, item in enumerate(self.allImeHKL):
                        tex = BigWorld.getImeIconTex(item)
                        self.HKLMap[item] = tex

            if hkl != 0:
                self.hide(0)
                tex = None
                if self.HKLMap.has_key(hkl):
                    tex = self.HKLMap[hkl]
                else:
                    tex = BigWorld.getImeIconTex(hkl)
                    self.HKLMap[hkl] = tex
            return

    def __updateIcon(self):
        shape = BigWorld.isImeSharp()
        chinese = BigWorld.isImeChinese()
        gameglobal.rds.ui.ime.setQuanJiao(shape)
        gameglobal.rds.ui.ime.setLanguage(chinese)

    def message(self, msgid):
        pass

    def popupMenu(self):
        tex = None
        allImeHKL = BigWorld.getAllIme()
        self.menu.clear()
        if allImeHKL:
            for i, hkl in enumerate(allImeHKL):
                if self.HKLMap.has_key(hkl):
                    tex = self.HKLMap[hkl]
                else:
                    tex = BigWorld.getImeIconTex(hkl)
                    self.HKLMap[hkl] = tex
                if tex == None:
                    continue
                self.menu.addItem(hkl, tex, BigWorld.getImeName(hkl))

        self.menu.relayout()
        self.menu.hide(0)
        screenw, screenh, a, b = BigWorld.getScreenState()
        absx, absy = self.icon.get_abs_coord()
        x = self.iconCoord[0]
        y = -self.menu.height + self.iconCoord[1]
        if absx + self.menu.width > screenw:
            x -= absx + self.menu.width - screenw
        if absy - self.menu.height < 0:
            y = self.iconCoord[1] + self.iconSize
        self.menu.set_coord(x, y)
        self.showMenu = True

    def setCompPos(self, x, y):
        gameglobal.rds.ui.setImePos(x, y)

    def hideMenu(self):
        self.menu.hide(1)
        self.showMenu = False

    def dumptex(self):
        i = 0
        for k, v in self.HKLMap.iteritems():
            s = 'd:/%d.tga' % i
            v.saveAs(s)
            i += 1

    def onRecreateDevice(self):
        enableCustomIme = gameglobal.rds.configData.get('enableCustomIme', False)
        if BigWorld.realFullScreen() and enableCustomIme:
            if hasattr(gameglobal.rds.ui, 'uiObj'):
                gameglobal.rds.ui.ime.showIme()
            if BigWorld.enableNtIme() == False:
                BigWorld.enableNtIme(True)
                self.setHKL(BigWorld.getCurrentHKL())
        else:
            if hasattr(gameglobal.rds.ui, 'uiObj'):
                gameglobal.rds.ui.ime.hideIme()
            if BigWorld.enableNtIme():
                BigWorld.enableNtIme(False)
                self.update()

    def hide(self, h):
        super(ImeMainGUI, self).hide(h)
        if h or BigWorld.isImeChinese() == False:
            self.ime.hide(1)
            self.hideMenu()
        else:
            self.topmost()
            comp, candidate = BigWorld.getImeComp()
            if comp != '':
                self.ime.hide(0)


def onRecreateDevice():
    if g_imeObj:
        g_imeObj.onRecreateDevice()


def setCompPos(x, y):
    if g_imeObj:
        screenw, screenh, a, b = BigWorld.getScreenState()
        x = x * screenw
        y = y * screenh
        g_imeObj.setCompPos(x, y)


def hideMenu():
    if g_imeObj:
        g_imeObj.hideMenu()
