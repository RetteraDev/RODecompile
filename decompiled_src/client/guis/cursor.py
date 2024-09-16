#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cursor.o
import BigWorld
import C_ui
import gamelog
import const
Normal_Cursor = 'arrow_normal'
NLight_Cursor = 'arrow_light'
Down_Cursor = 'arrow_down'
attack = 'cursor_attack'
attack_dis = 'cursor_attack_dis'
pickup = 'cursor_pickup'
pickup_dis = 'cursor_pickup_dis'
usebox = 'cursor_usebox'
usebox_dis = 'cursor_usebox_dis'
talk = 'cursor_talk'
talk_dis = 'cursor_talk_dis'
jiguan = 'cursor_jiguan'
jiguan_dis = 'cursor_jiguan_dis'
choose = 'cursor_choose'
choose_dis = 'cursor_choose_dis'
gather_ore = 'cursor_gatherore'
gather_ore_dis = 'cursor_gatherore_dis'
gather_gem = 'cursor_gathergem'
gather_gem_dis = 'cursor_gathergem_dis'
gather_plant = 'cursor_gatherplant'
gather_plant_dis = 'cursor_gatherplant_dis'
gather_stone = 'cursor_gatherstone'
gather_stone_dis = 'cursor_gatherstone_dis'
gather_wood = 'cursor_gatherwood'
gather_wood_dis = 'cursor_gatherwood_dis'
booth = 'cursor_booth'
booth_dis = 'cursor_booth_dis'
pickup_home = 'cursor_jiayuan'
pickup_home_dis = 'cursor_jiayuan_dis'
cipherlock = 'cursor_cipherlock'
timelock = 'cursor_timelock'
clickable = 'cursor_click'
process = 'cursor_process'
buy = 'cursor_buy'
sell = 'cursor_sell'
repair = 'cursor_repair'
gather_feed = 'cursor_feed'
gather_fish = 'cursor_gatherfish'
split_item = 'cursor_split'
split_item_dis = 'cursor_split'
mark_map = 'cursor_pickup'
zaiju = 'cursor_zaiju'
littlemap_sendpos = 'cursor_mapsendpos'
decompose = 'cursor_decompose'
splitItem = 'cursor_splitItem'
unlock = 'cursor_unlock'
dye = 'cursor_dye'
equipSign = 'cursor_equipSign'
identify = 'cursor_identify'
changeOwner = 'cursor_changeOwner'
equipCancelAbility = 'cursor_cancel_ability'
equipCancelAbilityDis = 'cursor_cancel_ability_dis'
changeBind = 'cursor_changeBind'
itemSearch = 'cursor_itemSearch'
disassemble = 'cursor_disassemble'
addStarExp = 'cursor_addStarExp'
cursor_wing_world_mark0 = 'cursor_wing_world_mark0'
cursor_wing_world_mark1 = 'cursor_wing_world_mark1'
cursor_wing_world_mark2 = 'cursor_wing_world_mark2'
cursor_wing_world_mark3 = 'cursor_wing_world_mark3'
Obj = None
TALK_DISTANCE = 3.5
CURSOR_DEFAUT_OUT_POS = -10000
CURSOR_DEFAUT_OUT_POS_ARR = [-10000, -10000]
oldCursorPos = [0, 0]
ignoreCursorPos = False

def oldCursorPosValid():
    global oldCursorPos
    if oldCursorPos and oldCursorPos[0] > 0:
        return True
    return False


def setOutAndSaveOldPos(cord = None):
    global ignoreCursorPos
    global oldCursorPos
    if C_ui.get_cursor_pos()[0] < 0 and not ignoreCursorPos:
        return oldCursorPos
    if cord and len(cord) == 2:
        C_ui.set_cursor_pos(cord[0], cord[1])
    oldPos = list(C_ui.cursor_pos(CURSOR_DEFAUT_OUT_POS, CURSOR_DEFAUT_OUT_POS))
    if oldPos != CURSOR_DEFAUT_OUT_POS_ARR:
        oldCursorPos = oldPos
    ignoreCursorPos = False
    return oldCursorPos


def setInAndRestoreOldPos(force = False):
    global oldCursorPos
    if oldCursorPosValid():
        C_ui.cursor_pos(oldCursorPos[0], oldCursorPos[1])
        oldCursorPos = []
    elif force:
        C_ui.cursor_pos(100, 100)
        oldCursorPos = []


class UICursor(object):

    def __init__(self):
        global Obj
        self.reset()
        Obj = self
        self.state = 0
        self.bindItemPos = [const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS]

    def set_bindItemPos(self, kind, page, pos):
        self.bindItemPos = [kind, page, pos]

    def get_bindItemPos(self):
        return self.bindItemPos

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def isInChoose(self):
        if hasattr(BigWorld.player(), 'isInChoose') and BigWorld.player().isInChoose():
            return True
        return False

    def reset(self):
        self._upCursor = Normal_Cursor
        self._downCursor = Down_Cursor
        self._hoverCursor = NLight_Cursor
        if self.isInChoose():
            self._upCursor = choose
            self._oldCursor = C_ui.cursor(choose)
        else:
            self._upCursor = Normal_Cursor
            self._oldCursor = C_ui.cursor(Normal_Cursor)
        self._lock = 0
        self.state = 0
        self._cursorTag = ''
        self.bindItemPos = [const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS]

    def setCursor(self, tag):
        if self._lock or self.isWap():
            return
        if tag[-4:].lower() == '.wap':
            self._oldCursor = C_ui.wapCursor(tag)
        elif tag == '':
            self._oldCursor = C_ui.cursor('', self._oldCursor)
        else:
            self._oldCursor = C_ui.cursor(tag)
        self._cursorTag = tag
        return self._oldCursor

    def setUpDown(self, up, down):
        if up != None:
            self._upCursor = up
        if down != None:
            self._downCursor = down

    def upCursor(self):
        self.setCursor(self._upCursor)

    def downCursor(self):
        self.setCursor(self._downCursor)

    def hoverCursor(self, hover):
        if hover:
            self.setCursor(self._hoverCursor)
        else:
            self.upCursor()

    def isWap(self):
        return self._cursorTag[-4:].lower() == '.wap'

    def tag(self):
        return self._cursorTag

    def lock(self):
        self._lock += 1

    def release(self):
        self._lock -= 1
        if self._lock < 0:
            gamelog.error('Error:cursor lock count error!')

    def isLock(self):
        return self._lock > 0
