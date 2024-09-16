#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hotkey.o
from gamestrings import gameStrings
import cPickle
import copy
import zlib
import BigWorld
import keys
import gameglobal
from cdata import key_description_data as KDD
ModKeys = (keys.KEY_LSHIFT,
 keys.KEY_RSHIFT,
 keys.KEY_LCONTROL,
 keys.KEY_RCONTROL,
 keys.KEY_LALT,
 keys.KEY_RALT)

def getModsNum(key):
    if key in ModKeys[0:2]:
        return 1
    if key in ModKeys[2:4]:
        return 2
    if key in ModKeys[4:6]:
        return 4
    return 0


def fromModsToKey(mods):
    if mods == 1:
        return (keys.KEY_LSHIFT, keys.KEY_RSHIFT)
    elif mods == 2:
        return (keys.KEY_LCONTROL, keys.KEY_RCONTROL)
    elif mods == 4:
        return (keys.KEY_LALT, keys.KEY_RALT)
    else:
        return ()


def keyToString(key):
    dsc = KDD.data.get(key)
    if dsc:
        return dsc['description']
    return BigWorld.keyToString(key)


def keyToBrief(key):
    dsc = KDD.data.get(key)
    if dsc:
        return dsc['brief_description']
    return BigWorld.keyToString(key)


class keyDef(object):

    def __init__(self, key, down = 1, mods = 0, key2 = 0, down2 = 1, mods2 = 0):
        self.key = key
        self.down = down
        self.mods = mods
        self.key2 = key2
        self.down2 = down2
        self.mods2 = mods2
        self._updateValue()

    def set(self, obj):
        self.key = obj.key
        self.down = obj.down
        self.mods = obj.mods
        self.key2 = obj.key2
        self.down2 = obj.down2
        self.mods2 = obj.mods2
        self._updateValue()

    def isEmpty(self):
        return self.key == 0

    def restoreFromValue(self, value):
        self._value = value & 16383
        self.key = value & 1023
        self.down = value >> 10 & 1
        self.mods = value >> 11 & 7
        value2 = value >> 14
        if value2 == self._value:
            self.key2 = 0
            self.down2 = 1
            self.mods2 = 0
            self._value2 = self._value
        else:
            self.key2 = value2 & 1023
            self.down2 = value2 >> 10 & 1
            self.mods2 = value2 >> 11 & 7
            self._value2 = value2

    def _updateValue(self):
        self._value = self.key | self.down << 10 | self.mods << 11
        if self.key2 == 0:
            self._value2 = self._value
        else:
            self._value2 = self.key2 | self.down2 << 10 | self.mods2 << 11

    def __eq__(self, other):
        if self._value == other._value and self.key != 0 and other.key != 0 or self._value2 == other._value2 and self.key2 != 0 and other.key2 != 0 or self._value == other._value2 and self.key != 0 and other.key2 != 0 or self._value2 == other._value and self.key2 != 0 and other.key != 0:
            return True
        return False

    def isAllDown(self):
        return BigWorld.isKeyDown(self.key) and BigWorld.isKeyDown(self.key2)

    def isAnyDown(self):
        if self.key in (keys.KEY_MOUSE_ROLLUP, keys.KEY_MOUSE_ROLLDOWN) or self.key2 in (keys.KEY_MOUSE_ROLLUP, keys.KEY_MOUSE_ROLLDOWN):
            return True
        return BigWorld.getKeyDownState(self.key, self.mods) or BigWorld.getKeyDownState(self.key2, self.mods2)

    def getDownKey(self):
        keyDownSet = set()
        if BigWorld.getKeyDownState(self.key, 0):
            keyDownSet.add(self.key)
        if BigWorld.getKeyDownState(self.key2, 0):
            keyDownSet.add(self.key2)
        return keyDownSet

    def __DirkeyDown(self):
        if BigWorld.getKeyDownState(self.key, 0):
            return True
        if BigWorld.getKeyDownState(self.key2, 0):
            return True
        keys = fromModsToKey(self.mods)
        for key in keys:
            if BigWorld.getKeyDownState(key, 0) and BigWorld.getKeyDownState(self.key, self.mods):
                return True

        keys = fromModsToKey(self.mods2)
        for key in keys:
            if BigWorld.getKeyDownState(key, 0) and BigWorld.getKeyDownState(self.key2, self.mods2):
                return True

        return False

    def getDirDownKey(self):
        keyDownSet = set()
        if self.__DirkeyDown():
            keyDownSet.add(self.key)
        return keyDownSet

    def removeAlt(self):
        self.mods = self.mods & 3
        self.mods2 = self.mods2 & 3
        self._updateValue()

    def modsToString(self, mods):
        string = ''
        if mods & 1:
            string += 'Shift+'
        if mods & 2:
            string += 'Ctrl+'
        if mods & 4:
            string += 'Alt+'
        return string

    def modsToBrief(self, mods):
        string = ''
        if mods & 1:
            string += 'S+'
        if mods & 2:
            string += 'C+'
        if mods & 4:
            string += 'A+'
        return string

    def getDesc(self, idx = 1):
        if idx == 1:
            keyStr = keyToString(self.key)
            return self.modsToString(self.mods) + keyStr
        else:
            keyStr = keyToString(self.key2)
            return self.modsToString(self.mods2) + keyStr

    def getBrief(self, idx = 1):
        if idx == 1:
            keyStr = keyToBrief(self.key)
            return self.modsToBrief(self.mods) + keyStr
        else:
            keyStr = keyToBrief(self.key2)
            return self.modsToBrief(self.mods2) + keyStr

    def inkeyDef(self, key, mods):
        if self.key and self.key == key and self.mods == mods:
            return 1
        if self.key2 and self.key2 == key and self.mods2 == mods:
            return 2
        return 0

    def clearPart(self, idx):
        if idx == 1:
            self.key = 0
            self.down = 1
            self.mods = 0
        else:
            self.key2 = 0
            self.down2 = 1
            self.mods2 = 0
        self._updateValue()

    def setPart(self, idx, key, mods):
        if idx == 1:
            self.key = key
            self.down = 1
            self.mods = mods
        else:
            self.key2 = key
            self.down2 = 1
            self.mods2 = mods
        self._updateValue()


KEY_SHOWFPS = 500
KEY_SHOWUI = 501
KEY_REPLAST = 502
KEY_SBCTRL1 = 503
KEY_SBCTRL2 = 504
KEY_SBCTRL3 = 505
KEY_SBCTRL4 = 506
KEY_SBCTRL5 = 507
KEY_SBCTRL6 = 508
KEY_SBCTRL7 = 509
KEY_SBCTRL8 = 510
KEY_SC1 = 511
KEY_SC2 = 512
KEY_SC3 = 513
KEY_SC4 = 514
KEY_SC5 = 515
KEY_SC6 = 516
KEY_SC7 = 517
KEY_SC8 = 518
KEY_SC9 = 519
KEY_SC0 = 520
KEY_FLSC1 = 521
KEY_FLSC2 = 522
KEY_FLSC3 = 523
KEY_FLSC4 = 524
KEY_FLSC5 = 525
KEY_FLSC6 = 526
KEY_FLSC7 = 527
KEY_FLSC8 = 528
KEY_FLSC9 = 529
KEY_FLSC0 = 530
KEY_FORWARD = 531
KEY_BACKWARD = 532
KEY_LEFTTURN = 533
KEY_RIGHTTURN = 534
KEY_MOVELEFT = 535
KEY_MOVERIGHT = 536
KEY_BLOODED = 537
KEY_STORE = 538
KEY_STONE = 539
KEY_SWITCHSC = 540
KEY_SWITCHFSC = 541
KEY_ZOOMIN = 542
KEY_ZOOMOUT = 543
KEY_JUMP = 544
KEY_DOWN = 545
KEY_WINGFLYUP = 546
KEY_WINGFLYDOWN = 547
KEY_QREPLY1 = 550
KEY_QREPLY2 = 551
KEY_QREPLY3 = 552
KEY_QREPLY4 = 553
KEY_QREPLY5 = 554
KEY_QREPLY6 = 555
KEY_QREPLY7 = 556
KEY_QREPLY8 = 557
KEY_QREPLY9 = 558
KEY_QREPLY0 = 559
KEY_EDITREPLY = 560
KEY_RIDE = 561
KEY_FLSC31 = 571
KEY_FLSC32 = 572
KEY_FLSC33 = 573
KEY_FLSC34 = 574
KEY_FLSC35 = 575
KEY_FLSC36 = 576
KEY_FLSC37 = 577
KEY_FLSC38 = 578
KEY_FLSC39 = 579
KEY_FLSC30 = 580
KEY_FLSC41 = 581
KEY_FLSC42 = 582
KEY_FLSC43 = 583
KEY_FLSC44 = 584
KEY_FLSC45 = 585
KEY_FLSC46 = 586
KEY_FLSC47 = 587
KEY_FLSC48 = 588
KEY_FLSC49 = 589
KEY_FLSC40 = 590
KEY_SHOWMAIL = 600
KEY_FLSC_PAGE = 601
KEY_FLSC_DOBLELINE = 602
KEY_FLSC_HIDE = 603
KEY_FLSC_VERTICAL = 604
KEY_SWITCHMODE = 605
KEY_SHOWEQUIP = 606
KEY_SHOWBEAST = 607
KEY_SHOWSHOP = 608
KEY_PICKALL = 700
KEY_FOLLOW = 701
KEY_RESETCAM = 702
KEY_GHOST = 703
KEY_TRANS_AVATAR = 704
KEY_TEAMATE_1 = 706
KEY_TEAMATE_2 = 707
KEY_TEAMATE_3 = 708
KEY_TEAMATE_4 = 709
KEY_RELATION = 710
KEY_HIDEOTHER = 711
KEY_FB = 712
KEY_BATTLEFIELD = 713
KEY_HBSKILL = 714
KEY_HBATTR = 715
KEY_FLSC11 = 716
KEY_FLSC12 = 717
KEY_FLSC13 = 718
KEY_FLSC14 = 719
KEY_FLSC15 = 720
KEY_FLSC16 = 721
KEY_FLSC17 = 722
KEY_FLSC18 = 723
KEY_FLSC19 = 724
KEY_FLSC10 = 725
KEY_FLSC_DOBLELINE1 = 726
KEY_FLSC_HIDE1 = 727
KEY_FLSC_VERTICAL1 = 728
KEY_DEBUG_UP = 729
KEY_AUDIOSWITCH = 730
KEY_HBRIDE = 731
KEY_CREDIT = 732
KEY_COMMAND = 733
KEY_EMOTE = 734
KEY_CRAFT = 735
KEY_TEAM = 736
KEY_LEAGUE = 737
KEY_PICK_ITEM = 738
KEY_DODGE = 739
KEY_STUNT = 740
KEY_CLANEVENT = 741
KEY_CLANWAR = 742
KEY_BUYDOUBLE = 743
KEY_SBSKILL1 = 744
KEY_SBSKILL2 = 745
KEY_SBSKILL3 = 746
KEY_SBSKILL4 = 747
KEY_SBSKILL5 = 748
KEY_SBSKILL6 = 749
KEY_SBSKILL7 = 750
KEY_SBSKILL8 = 751
KEY_SBSKILL9 = 752
KEY_SBSKILL0 = 752
KEY_DEBUG_VIEW = 756
KEY_FUBEN_MONSTER = 757
KEY_BATTLE_APPLY = 758
KEY_SINGLE_DEBUG = 759
KEY_SUMMARY = 760
KEY_MORPH_DEBUG = 761
KEY_TINT_DEBUG = 762
KEY_HIDE_MONSTER_LOGO = 763
KYE_MAGICFIELD_DEBUG = 764
KEY_SHOW_TOPLOGO = 765
KEY_SHOW_BAG = 766
KEY_SHOW_ROLEINFO = 767
KEY_SHOW_SYSSETTING = 768
KEY_SHOW_TEAMINFO = 769
KEY_SHOW_TASKLOG = 770
KEY_SHOW_MAP = 771
KEY_SHOW_SKILL = 772
KEY_LEFT_DODGE = 773
KEY_RIGHT_DODGE = 774
KEY_BACK_DODGE = 775
KEY_SHOW_PVP = 776
KEY_SHOW_RANK = 777
KEY_SHOW_LITTLE_MAP = 778
KEY_HIDE_PLAYER_MONSTER = 779
KEY_SELECT_TEAMER1 = 780
KEY_SELECT_TEAMER2 = 781
KEY_SELECT_TEAMER3 = 782
KEY_SELECT_TEAMER4 = 783
KEY_SELECT_TEAMER = 784
KEY_SHOW_SCHEDULE = 785
KEY_USE_ITEM1 = 786
KEY_USE_ITEM2 = 787
KEY_USE_ITEM3 = 788
KEY_USE_ITEM4 = 789
KEY_USE_ITEM5 = 790
KEY_USE_ITEM6 = 791
KEY_USE_ITEM7 = 792
KEY_USE_ITEM8 = 793
KEY_USE_ITEM9 = 794
KEY_USE_ITEM10 = 795
KEY_USE_ITEM11 = 796
KEY_USE_ITEM12 = 797
KEY_USE_ITEM13 = 798
KEY_USE_ITEM14 = 799
KEY_USE_ITEM15 = 800
KEY_USE_ITEM16 = 801
KEY_USE_ITEM17 = 802
KEY_USE_ITEM18 = 803
KEY_USE_ITEM19 = 804
KEY_USE_ITEM20 = 805
KEY_DRAG_UI = 806
KEY_FORWARD_DODGE = 807
KEY_SHOW_FRIEND = 808
KEY_CHANGE_CURSOR = 809
KEY_SWITCH_LAST = 811
KEY_CAMERA_FAR = 812
KEY_CAMERA_NEAR = 813
KEY_CAST_SKILL_TO_SELF = 814
KEY_WING_SPRINT = 816
KEY_SHOW_GENERAL_SKILL = 817
KEY_SHOW_LIFE_SKILL = 818
KEY_SHOW_MAIL = 819
KEY_SHOW_CONSIGN = 820
KEY_RESUME_FREE_ROTATE = 821
KEY_LEAVE_LOCK_ROTATE = 822
KEY_USE_ITEM21 = 823
KEY_USE_ITEM22 = 824
KEY_USE_ITEM23 = 825
KEY_USE_ITEM24 = 826
KEY_WEAPON_IN_HAND = 827
KEY_SHOW_CAMERA = 828
KEY_QTE_SKILL1 = 829
KEY_QTE_SKILL2 = 830
KEY_LEAVE_ZAIJU = 831
KEY_ASSIGN_CONFIRM = 832
KEY_ASSIGN_CANCEL = 833
KEY_ASSIGN_GREED = 834
KEY_SHOW_HELP = 835
KEY_SHOW_PLAYRECOMM = 836
KEY_SWITCH_RUN_WALK = 837
KEY_SHOW_DELEGATION = 838
KEY_NEXT_TRACK_TAB = 839
KEY_SHOW_FASHION = 840
KEY_UP_DODGE = 841
KEY_DOWN_DODGE = 842
KEY_SELECT_TEAMER_ME = 843
KEY_RIDE_WING = 844
KEY_BF_RETURN = 845
KEY_BF_COUNT = 847
KEY_USE_ITEM25 = 848
KEY_USE_ITEM26 = 849
KEY_USE_ITEM27 = 850
KEY_USE_ITEM28 = 851
KEY_USE_ITEM29 = 852
KEY_USE_ITEM30 = 853
KEY_USE_ITEM31 = 854
KEY_USE_ITEM32 = 855
KEY_USE_ITEM33 = 856
KEY_USE_ITEM34 = 857
KEY_USE_ITEM35 = 858
KEY_USE_ITEM36 = 859
KEY_USE_ITEM37 = 860
KEY_USE_ITEM38 = 861
KEY_USE_ITEM39 = 862
KEY_USE_ITEM40 = 863
KEY_USE_ITEM41 = 864
KEY_USE_ITEM42 = 865
KEY_USE_ITEM43 = 866
KEY_USE_ITEM44 = 867
KEY_USE_ITEM45 = 868
KEY_USE_ITEM46 = 869
KEY_USE_ITEM47 = 870
KEY_USE_ITEM48 = 871
KEY_LOCK_TARGETS_TARGET = 872
KEY_TURN_CAMERA = 875
KEY_ROLE_CARD = 876
KEY_FENG_WU_ZHI = 877
KEY_PERSON_SPACE = 878
KEY_MOUNT_WING = 879
KEY_STALL = 880
KEY_PVP_ENHANCE = 881
KEY_CHAT_ROOM = 882
KEY_JIE_QI = 883
KEY_MENTOR = 884
KEY_PVP_JJC = 885
KEY_GUI_BAO = 886
KEY_USER_BACK = 887
KEY_SUMMON_FRIEND = 888
KEY_SIMPLE_FIND_POS = 889
KEY_SHOW_MORE_RECOMM = 890
KEY_ITEM_SOURCE = 891
KEY_SKILL_MACRO = 892
KEY_DOTA_SKILL0 = 893
KEY_DOTA_SKILL1 = 894
KEY_DOTA_SKILL2 = 895
KEY_DOTA_SKILL3 = 896
KEY_DOTA_SKILL4 = 897
KEY_DOTA_SKILL5 = 898
KEY_DOTA_SKILL6 = 899
KEY_DOTA_SKILL7 = 900
KEY_DOTA_ITEM0 = 901
KEY_DOTA_ITEM1 = 902
KEY_DOTA_ITEM2 = 903
KEY_DOTA_ITEM3 = 904
KEY_DOTA_ITEM4 = 905
KEY_DOTA_ITEM5 = 906
KEY_DOTA_OPEN_SHOP = 907
KEY_DOTA_RETURN_HOME = 908
KEY_DOTA_LEARN_SKILL = 909
KEY_DOTA_SHOW_DETAIL = 910
KEY_DOTA_SHOW_PROP = 911
KEY_CHATLOG_SOUND_RECORD = 912
KEY_CHAT_TO_FRIEND_SOUND_RECORD = 913
KEY_DOTA_BUY_ITEM_SHORTCUT0 = 914
KEY_DOTA_BUY_ITEM_SHORTCUT1 = 915
KEY_DOTA_CAMERA_TURN_RIGHT = 917
KEY_GROUP_FOLLOW = 918
KEY_SPRITE_TELEPORT_BACK = 919
KEY_SPRITE_MANUAL_SKILL = 920
KEY_DOTA_MAP_MARK = 921
KEY_DOTA_MAP_ATK = 922
KEY_DOTA_MAP_RETREAT = 923
KEY_DOTA_MAP_GATHER = 924
KEY_SPRITE_WAR = 925
KEY_SELECT_TEAMER_ME_SPRITE = 926
KEY_OPEN_WING_WORLD_UI = 927
KEY_VOICE = 928
KEY_NPCV2_SPEED = 929
KEY_NPCV2_QUICK = 930
KEY_CARD_SYSTEM = 931
KEY_OPEN_ASSASSINATION_MAIN_UI = 932
DefaultHotkeyMap = {KEY_FORWARD: keyDef(keys.KEY_W, 1, 0, keys.KEY_UPARROW),
 KEY_LEFTTURN: keyDef(keys.KEY_Q, 1, 0, keys.KEY_LEFTARROW),
 KEY_RIGHTTURN: keyDef(keys.KEY_E, 1, 0, keys.KEY_RIGHTARROW),
 KEY_BACKWARD: keyDef(keys.KEY_S, 1, 0, keys.KEY_DOWNARROW),
 KEY_DOWN: keyDef(keys.KEY_X),
 KEY_WINGFLYUP: keyDef(keys.KEY_SPACE, 1, 4),
 KEY_WINGFLYDOWN: keyDef(keys.KEY_X, 1, 4),
 KEY_MOVERIGHT: keyDef(keys.KEY_D),
 KEY_MOVELEFT: keyDef(keys.KEY_A),
 KEY_SWITCHMODE: keyDef(keys.KEY_SCROLL),
 keys.KEY_B: keyDef(keys.KEY_B),
 keys.KEY_C: keyDef(keys.KEY_C),
 KEY_RELATION: keyDef(keys.KEY_G),
 keys.KEY_I: keyDef(keys.KEY_I),
 KEY_PICK_ITEM: keyDef(keys.KEY_F, 1, 0, keys.KEY_Z),
 KEY_RIDE: keyDef(keys.KEY_U, 1, 2),
 keys.KEY_H: keyDef(keys.KEY_H),
 keys.KEY_K: keyDef(keys.KEY_K),
 keys.KEY_L: keyDef(keys.KEY_L),
 keys.KEY_M: keyDef(keys.KEY_M),
 keys.KEY_P: keyDef(keys.KEY_P),
 keys.KEY_T: keyDef(keys.KEY_T),
 keys.KEY_U: keyDef(keys.KEY_U),
 keys.KEY_Y: keyDef(keys.KEY_Y),
 keys.KEY_Z: keyDef(keys.KEY_Z),
 keys.KEY_LALT: keyDef(keys.KEY_LALT),
 keys.KEY_MOUSE0: keyDef(keys.KEY_MOUSE0),
 keys.KEY_MOUSE1: keyDef(keys.KEY_MOUSE1),
 KEY_RESETCAM: keyDef(keys.KEY_MOUSE2),
 keys.KEY_NUMLOCK: keyDef(keys.KEY_NUMLOCK),
 keys.KEY_SPACE: keyDef(keys.KEY_SPACE),
 keys.KEY_NUMPADSLASH: keyDef(keys.KEY_NUMPADSLASH),
 KEY_HIDEOTHER: keyDef(keys.KEY_F10),
 keys.KEY_DELETE: keyDef(keys.KEY_DELETE),
 KEY_AUDIOSWITCH: keyDef(keys.KEY_PERIOD),
 KEY_SIMPLE_FIND_POS: keyDef(keys.KEY_F, 1, 2),
 KEY_GROUP_FOLLOW: keyDef(keys.KEY_D, 1, 2),
 KEY_SPRITE_TELEPORT_BACK: keyDef(0),
 KEY_SPRITE_MANUAL_SKILL: keyDef(0),
 KEY_SHOWFPS: keyDef(keys.KEY_R, 1, 2),
 KEY_SHOWUI: keyDef(keys.KEY_F12),
 KEY_REPLAST: keyDef(keys.KEY_R),
 KEY_SBCTRL1: keyDef(keys.KEY_F1),
 KEY_SBCTRL2: keyDef(keys.KEY_F2),
 KEY_SBCTRL3: keyDef(keys.KEY_F3),
 KEY_SBCTRL4: keyDef(keys.KEY_F4),
 KEY_SBCTRL5: keyDef(keys.KEY_F5),
 KEY_SBCTRL6: keyDef(keys.KEY_F6),
 KEY_SBCTRL7: keyDef(keys.KEY_F7),
 KEY_SBCTRL8: keyDef(keys.KEY_F8),
 KEY_SBSKILL1: keyDef(0),
 KEY_SBSKILL2: keyDef(0),
 KEY_SBSKILL3: keyDef(0),
 KEY_SBSKILL4: keyDef(0),
 KEY_SBSKILL5: keyDef(0),
 KEY_SBSKILL6: keyDef(0),
 KEY_SBSKILL7: keyDef(0),
 KEY_SBSKILL8: keyDef(0),
 KEY_SC1: keyDef(keys.KEY_1),
 KEY_SC2: keyDef(keys.KEY_2),
 KEY_SC3: keyDef(keys.KEY_3),
 KEY_SC4: keyDef(keys.KEY_4),
 KEY_SC5: keyDef(keys.KEY_5),
 KEY_SC6: keyDef(keys.KEY_6),
 KEY_SC7: keyDef(keys.KEY_7),
 KEY_SC8: keyDef(keys.KEY_8),
 KEY_SC9: keyDef(keys.KEY_9),
 KEY_SC0: keyDef(keys.KEY_0),
 KEY_FLSC1: keyDef(keys.KEY_1, 1, 2),
 KEY_FLSC2: keyDef(keys.KEY_2, 1, 2),
 KEY_FLSC3: keyDef(keys.KEY_3, 1, 2),
 KEY_FLSC4: keyDef(keys.KEY_4, 1, 2),
 KEY_FLSC5: keyDef(keys.KEY_5, 1, 2),
 KEY_FLSC6: keyDef(keys.KEY_6, 1, 2),
 KEY_FLSC7: keyDef(keys.KEY_7, 1, 2),
 KEY_FLSC8: keyDef(keys.KEY_8, 1, 2),
 KEY_FLSC9: keyDef(keys.KEY_9, 1, 2),
 KEY_FLSC0: keyDef(keys.KEY_0, 1, 2),
 KEY_FLSC11: keyDef(keys.KEY_1, 1, 1),
 KEY_FLSC12: keyDef(keys.KEY_2, 1, 1),
 KEY_FLSC13: keyDef(keys.KEY_3, 1, 1),
 KEY_FLSC14: keyDef(keys.KEY_4, 1, 1),
 KEY_FLSC15: keyDef(keys.KEY_5, 1, 1),
 KEY_FLSC16: keyDef(keys.KEY_6, 1, 1),
 KEY_FLSC17: keyDef(keys.KEY_7, 1, 1),
 KEY_FLSC18: keyDef(keys.KEY_8, 1, 1),
 KEY_FLSC19: keyDef(keys.KEY_9, 1, 1),
 KEY_FLSC10: keyDef(keys.KEY_0, 1, 1),
 KEY_FLSC31: keyDef(0),
 KEY_FLSC32: keyDef(0),
 KEY_FLSC33: keyDef(0),
 KEY_FLSC34: keyDef(0),
 KEY_FLSC35: keyDef(0),
 KEY_FLSC36: keyDef(0),
 KEY_FLSC37: keyDef(0),
 KEY_FLSC38: keyDef(0),
 KEY_FLSC39: keyDef(0),
 KEY_FLSC30: keyDef(0),
 KEY_FLSC41: keyDef(0),
 KEY_FLSC42: keyDef(0),
 KEY_FLSC43: keyDef(0),
 KEY_FLSC44: keyDef(0),
 KEY_FLSC45: keyDef(0),
 KEY_FLSC46: keyDef(0),
 KEY_FLSC47: keyDef(0),
 KEY_FLSC48: keyDef(0),
 KEY_FLSC49: keyDef(0),
 KEY_FLSC40: keyDef(0),
 keys.KEY_1: keyDef(keys.KEY_1, 1, 0),
 keys.KEY_2: keyDef(keys.KEY_2, 1, 0),
 keys.KEY_3: keyDef(keys.KEY_3, 1, 0),
 keys.KEY_4: keyDef(keys.KEY_4, 1, 0),
 keys.KEY_5: keyDef(keys.KEY_5, 1, 0),
 keys.KEY_6: keyDef(keys.KEY_6, 1, 0),
 keys.KEY_7: keyDef(keys.KEY_7, 1, 0),
 keys.KEY_8: keyDef(keys.KEY_8, 1, 0),
 keys.KEY_9: keyDef(keys.KEY_9, 1, 0),
 keys.KEY_0: keyDef(keys.KEY_0, 1, 0),
 keys.KEY_MINUS: keyDef(keys.KEY_MINUS, 1, 0),
 keys.KEY_EQUALS: keyDef(keys.KEY_EQUALS, 1, 0),
 keys.KEY_F1: keyDef(keys.KEY_F1),
 keys.KEY_F2: keyDef(keys.KEY_F2),
 keys.KEY_F3: keyDef(keys.KEY_F3),
 keys.KEY_F4: keyDef(keys.KEY_F4),
 keys.KEY_F5: keyDef(keys.KEY_F5),
 keys.KEY_F6: keyDef(keys.KEY_F6),
 keys.KEY_F7: keyDef(keys.KEY_F7),
 keys.KEY_F8: keyDef(keys.KEY_F8),
 keys.KEY_F9: keyDef(keys.KEY_F9),
 keys.KEY_F10: keyDef(keys.KEY_F10),
 keys.KEY_F11: keyDef(keys.KEY_F11),
 keys.KEY_F12: keyDef(keys.KEY_F12),
 keys.KEY_GRAVE: keyDef(keys.KEY_GRAVE, 1, 2),
 keys.KEY_TAB: keyDef(keys.KEY_TAB),
 keys.KEY_ESCAPE: keyDef(keys.KEY_ESCAPE),
 keys.KEY_LCONTROL: keyDef(keys.KEY_LCONTROL),
 keys.KEY_RCONTROL: keyDef(keys.KEY_RCONTROL),
 KEY_BLOODED: keyDef(0),
 KEY_STORE: keyDef(0),
 KEY_STONE: keyDef(0),
 KEY_ZOOMIN: keyDef(keys.KEY_HOME),
 KEY_ZOOMOUT: keyDef(keys.KEY_END),
 KEY_SHOW_FRIEND: keyDef(keys.KEY_P),
 KEY_SHOWEQUIP: keyDef(keys.KEY_N),
 KEY_SHOWBEAST: keyDef(keys.KEY_F),
 KEY_SHOWSHOP: keyDef(keys.KEY_C, 1, 4),
 KEY_FLSC_PAGE: keyDef(0),
 KEY_FLSC_DOBLELINE: keyDef(keys.KEY_EQUALS, 1, 2),
 KEY_FLSC_HIDE: keyDef(keys.KEY_BACKSLASH, 1, 2),
 KEY_FLSC_VERTICAL: keyDef(keys.KEY_MINUS, 1, 2),
 KEY_FLSC_DOBLELINE1: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_FLSC_HIDE1: keyDef(keys.KEY_BACKSLASH, 1, 1),
 KEY_FLSC_VERTICAL1: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_QREPLY1: keyDef(keys.KEY_NUMPAD1),
 KEY_QREPLY2: keyDef(keys.KEY_NUMPAD2),
 KEY_QREPLY3: keyDef(keys.KEY_NUMPAD3),
 KEY_QREPLY4: keyDef(keys.KEY_NUMPAD4),
 KEY_QREPLY5: keyDef(keys.KEY_NUMPAD5),
 KEY_QREPLY6: keyDef(keys.KEY_NUMPAD6),
 KEY_QREPLY7: keyDef(keys.KEY_NUMPAD7),
 KEY_QREPLY8: keyDef(keys.KEY_NUMPAD8),
 KEY_QREPLY9: keyDef(keys.KEY_NUMPAD9),
 KEY_QREPLY0: keyDef(keys.KEY_NUMPAD0),
 KEY_EDITREPLY: keyDef(keys.KEY_NUMPADPERIOD),
 KEY_PICKALL: keyDef(keys.KEY_Z, 1, 1),
 KEY_FOLLOW: keyDef(keys.KEY_MOUSE4),
 KEY_GHOST: keyDef(0),
 KEY_TRANS_AVATAR: keyDef(keys.KEY_V),
 KEY_SHOW_MORE_RECOMM: keyDef(keys.KEY_O),
 KEY_TEAMATE_1: keyDef(keys.KEY_F1, 1, 1),
 KEY_TEAMATE_2: keyDef(keys.KEY_F2, 1, 1),
 KEY_TEAMATE_3: keyDef(keys.KEY_F3, 1, 1),
 KEY_TEAMATE_4: keyDef(keys.KEY_F4, 1, 1),
 KEY_FB: keyDef(keys.KEY_I, 1, 2),
 KEY_BATTLEFIELD: keyDef(keys.KEY_H, 1, 2),
 KEY_HBSKILL: keyDef(keys.KEY_P, 1, 2),
 KEY_HBATTR: keyDef(keys.KEY_O, 1, 2),
 KEY_HBRIDE: keyDef(keys.KEY_L, 1, 2),
 KEY_CREDIT: keyDef(keys.KEY_M, 1, 2),
 KEY_COMMAND: keyDef(keys.KEY_N, 1, 2),
 KEY_EMOTE: keyDef(keys.KEY_B, 1, 2),
 KEY_CRAFT: keyDef(keys.KEY_V, 1, 2),
 KEY_LEAGUE: keyDef(keys.KEY_J, 1, 2),
 KEY_DODGE: keyDef(keys.KEY_S, 1, 2),
 KEY_STUNT: keyDef(keys.KEY_K, 1, 2),
 KEY_CLANEVENT: keyDef(keys.KEY_D, 1, 2),
 KEY_CLANWAR: keyDef(keys.KEY_A, 1, 2),
 KEY_BUYDOUBLE: keyDef(keys.KEY_E, 1, 2),
 KEY_DEBUG_UP: keyDef(keys.KEY_LBRACKET),
 KEY_SHOW_TOPLOGO: keyDef(keys.KEY_LALT),
 KEY_SHOW_BAG: keyDef(keys.KEY_B),
 KEY_SHOW_ROLEINFO: keyDef(keys.KEY_C),
 KEY_DEBUG_VIEW: keyDef(keys.KEY_D, 1, 4),
 KEY_FUBEN_MONSTER: keyDef(keys.KEY_F, 1, 4),
 KEY_BATTLE_APPLY: keyDef(keys.KEY_Z, 1, 4),
 KEY_SINGLE_DEBUG: keyDef(keys.KEY_S, 1, 4),
 KEY_SUMMARY: keyDef(keys.KEY_NUMPADSTAR),
 KEY_MORPH_DEBUG: keyDef(keys.KEY_M, 1, 4),
 KEY_TINT_DEBUG: keyDef(keys.KEY_T, 1, 4),
 KEY_HIDE_MONSTER_LOGO: keyDef(keys.KEY_F12, 1, 2),
 KYE_MAGICFIELD_DEBUG: keyDef(keys.KEY_Q, 1, 2),
 KEY_SHOW_TEAMINFO: keyDef(keys.KEY_T),
 KEY_SHOW_TASKLOG: keyDef(keys.KEY_L),
 KEY_SHOW_MAP: keyDef(keys.KEY_M),
 KEY_SHOW_SKILL: keyDef(keys.KEY_K),
 KEY_LEFT_DODGE: keyDef(keys.KEY_A, 1, 1),
 KEY_RIGHT_DODGE: keyDef(keys.KEY_D, 1, 1),
 KEY_BACK_DODGE: keyDef(keys.KEY_S, 1, 1),
 KEY_FORWARD_DODGE: keyDef(keys.KEY_W, 1, 1),
 KEY_UP_DODGE: keyDef(keys.KEY_SPACE, 1, 1),
 KEY_DOWN_DODGE: keyDef(keys.KEY_X, 1, 1),
 KEY_WING_SPRINT: keyDef(keys.KEY_W, 1, 4),
 KEY_SHOW_PVP: keyDef(keys.KEY_H),
 KEY_SHOW_RANK: keyDef(keys.KEY_Y, 1, 1),
 KEY_SHOW_LITTLE_MAP: keyDef(keys.KEY_N),
 KEY_HIDE_PLAYER_MONSTER: keyDef(keys.KEY_F10),
 KEY_SELECT_TEAMER1: keyDef(keys.KEY_F1, 1, 1),
 KEY_SELECT_TEAMER2: keyDef(keys.KEY_F2, 1, 1),
 KEY_SELECT_TEAMER3: keyDef(keys.KEY_F3, 1, 1),
 KEY_SELECT_TEAMER4: keyDef(keys.KEY_F4, 1, 1),
 KEY_SELECT_TEAMER: keyDef(keys.KEY_GRAVE),
 KEY_SELECT_TEAMER_ME: keyDef(keys.KEY_F5, 1, 1),
 KEY_SELECT_TEAMER_ME_SPRITE: keyDef(0),
 keys.KEY_RETURN: keyDef(keys.KEY_RETURN, 1, 0),
 KEY_USE_ITEM1: keyDef(keys.KEY_1, 1, 1),
 KEY_USE_ITEM2: keyDef(keys.KEY_2, 1, 1),
 KEY_USE_ITEM3: keyDef(keys.KEY_3, 1, 1),
 KEY_USE_ITEM4: keyDef(keys.KEY_4, 1, 1),
 KEY_USE_ITEM5: keyDef(keys.KEY_5, 1, 1),
 KEY_USE_ITEM6: keyDef(keys.KEY_6, 1, 1),
 KEY_USE_ITEM7: keyDef(keys.KEY_7, 1, 1),
 KEY_USE_ITEM8: keyDef(keys.KEY_8, 1, 1),
 KEY_USE_ITEM9: keyDef(keys.KEY_9, 1, 1),
 KEY_USE_ITEM10: keyDef(keys.KEY_0, 1, 1),
 KEY_USE_ITEM11: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_USE_ITEM12: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_USE_ITEM13: keyDef(0),
 KEY_USE_ITEM14: keyDef(0),
 KEY_USE_ITEM15: keyDef(0),
 KEY_USE_ITEM16: keyDef(0),
 KEY_USE_ITEM17: keyDef(0),
 KEY_USE_ITEM18: keyDef(0),
 KEY_USE_ITEM19: keyDef(0),
 KEY_USE_ITEM20: keyDef(0),
 KEY_USE_ITEM21: keyDef(0),
 KEY_USE_ITEM22: keyDef(0),
 KEY_USE_ITEM23: keyDef(0),
 KEY_USE_ITEM24: keyDef(0),
 KEY_USE_ITEM25: keyDef(0),
 KEY_USE_ITEM26: keyDef(0),
 KEY_USE_ITEM27: keyDef(0),
 KEY_USE_ITEM28: keyDef(0),
 KEY_USE_ITEM29: keyDef(0),
 KEY_USE_ITEM30: keyDef(0),
 KEY_USE_ITEM31: keyDef(0),
 KEY_USE_ITEM32: keyDef(0),
 KEY_USE_ITEM33: keyDef(0),
 KEY_USE_ITEM34: keyDef(0),
 KEY_USE_ITEM35: keyDef(0),
 KEY_USE_ITEM36: keyDef(0),
 KEY_USE_ITEM37: keyDef(0),
 KEY_USE_ITEM38: keyDef(0),
 KEY_USE_ITEM39: keyDef(0),
 KEY_USE_ITEM40: keyDef(0),
 KEY_USE_ITEM41: keyDef(0),
 KEY_USE_ITEM42: keyDef(0),
 KEY_USE_ITEM43: keyDef(0),
 KEY_USE_ITEM44: keyDef(0),
 KEY_USE_ITEM45: keyDef(0),
 KEY_USE_ITEM46: keyDef(0),
 KEY_USE_ITEM47: keyDef(0),
 KEY_USE_ITEM48: keyDef(0),
 KEY_DRAG_UI: keyDef(keys.KEY_F11),
 KEY_CHANGE_CURSOR: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_SWITCH_LAST: keyDef(0),
 KEY_CAMERA_NEAR: keyDef(keys.KEY_MOUSE_ROLLUP),
 KEY_CAMERA_FAR: keyDef(keys.KEY_MOUSE_ROLLDOWN),
 KEY_CAST_SKILL_TO_SELF: keyDef(keys.KEY_LALT),
 KEY_SHOW_GENERAL_SKILL: keyDef(keys.KEY_N),
 KEY_SHOW_LIFE_SKILL: keyDef(keys.KEY_V),
 KEY_SHOW_MAIL: keyDef(keys.KEY_J),
 KEY_SHOW_CONSIGN: keyDef(keys.KEY_R),
 KEY_RESUME_FREE_ROTATE: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_LEAVE_LOCK_ROTATE: keyDef(keys.KEY_LCONTROL, 1),
 KEY_WEAPON_IN_HAND: keyDef(keys.KEY_SLASH),
 KEY_SHOW_CAMERA: keyDef(keys.KEY_F9, 1, 2),
 KEY_QTE_SKILL1: keyDef(0),
 KEY_QTE_SKILL2: keyDef(0),
 KEY_LEAVE_ZAIJU: keyDef(keys.KEY_F8),
 KEY_ASSIGN_CONFIRM: keyDef(keys.KEY_NUMPAD1),
 KEY_ASSIGN_CANCEL: keyDef(keys.KEY_NUMPAD2),
 KEY_ASSIGN_GREED: keyDef(keys.KEY_NUMPAD0),
 KEY_BF_RETURN: keyDef(keys.KEY_NUMPAD6),
 KEY_BF_COUNT: keyDef(keys.KEY_NUMPAD5),
 KEY_SHOW_HELP: keyDef(keys.KEY_H, 1, 2),
 KEY_SHOW_PLAYRECOMM: keyDef(keys.KEY_U),
 KEY_SWITCH_RUN_WALK: keyDef(keys.KEY_NUMPADSLASH),
 KEY_SHOW_DELEGATION: keyDef(keys.KEY_I),
 KEY_RIDE_WING: keyDef(0),
 KEY_NEXT_TRACK_TAB: keyDef(keys.KEY_TAB, mods=2),
 KEY_LOCK_TARGETS_TARGET: keyDef(0),
 KEY_TURN_CAMERA: keyDef(keys.KEY_Q, 1, 1),
 KEY_ROLE_CARD: keyDef(keys.KEY_L, 1, 1),
 KEY_FENG_WU_ZHI: keyDef(keys.KEY_I, 1, 1),
 KEY_SPRITE_WAR: keyDef(keys.KEY_G, 1, 1),
 KEY_PERSON_SPACE: keyDef(keys.KEY_C, 1, 1),
 KEY_MOUNT_WING: keyDef(keys.KEY_Z, 1, 1),
 KEY_STALL: keyDef(keys.KEY_F, 1, 1),
 KEY_PVP_ENHANCE: keyDef(0),
 KEY_CHAT_ROOM: keyDef(keys.KEY_P, 1, 1),
 KEY_JIE_QI: keyDef(keys.KEY_J, 1, 2),
 KEY_MENTOR: keyDef(keys.KEY_Z, 1, 2),
 KEY_PVP_JJC: keyDef(keys.KEY_H, 1, 4),
 KEY_GUI_BAO: keyDef(keys.KEY_Y, 1, 4),
 KEY_USER_BACK: keyDef(keys.KEY_O, 1, 2),
 KEY_SUMMON_FRIEND: keyDef(keys.KEY_P, 1, 2),
 KEY_ITEM_SOURCE: keyDef(keys.KEY_F7),
 KEY_SKILL_MACRO: keyDef(keys.KEY_B, 1, 1),
 KEY_CHATLOG_SOUND_RECORD: keyDef(keys.KEY_A, 1, 2),
 KEY_CHAT_TO_FRIEND_SOUND_RECORD: keyDef(keys.KEY_X, 1, 2),
 KEY_OPEN_WING_WORLD_UI: keyDef(keys.KEY_J, 1, 1),
 KEY_OPEN_ASSASSINATION_MAIN_UI: keyDef(keys.KEY_K, 1, 1),
 KEY_VOICE: keyDef(keys.KEY_Q, 1, 2),
 KEY_NPCV2_SPEED: keyDef(keys.KEY_Z),
 KEY_NPCV2_QUICK: keyDef(keys.KEY_R),
 KEY_CARD_SYSTEM: keyDef(keys.KEY_H, 1, 1)}
WanMeiHotkeyMap = {KEY_FORWARD: keyDef(keys.KEY_W, 1, 0, keys.KEY_UPARROW),
 KEY_BACKWARD: keyDef(keys.KEY_S, 1, 0, keys.KEY_DOWNARROW),
 KEY_MOVERIGHT: keyDef(keys.KEY_D, 1, 0, keys.KEY_RIGHTARROW),
 KEY_MOVELEFT: keyDef(keys.KEY_A, 1, 0, keys.KEY_LEFTARROW),
 KEY_LEFTTURN: keyDef(0),
 KEY_RIGHTTURN: keyDef(0),
 KEY_WINGFLYUP: keyDef(keys.KEY_SPACE, 1, 4),
 KEY_WINGFLYDOWN: keyDef(keys.KEY_X, 1, 4),
 KEY_SWITCHMODE: keyDef(keys.KEY_SCROLL),
 KEY_DOWN: keyDef(keys.KEY_X),
 keys.KEY_B: keyDef(keys.KEY_B),
 keys.KEY_C: keyDef(keys.KEY_C),
 KEY_RELATION: keyDef(keys.KEY_G),
 keys.KEY_I: keyDef(keys.KEY_I),
 KEY_PICK_ITEM: keyDef(keys.KEY_F, 1, 0, keys.KEY_Z),
 KEY_SHOW_TEAMINFO: keyDef(keys.KEY_T),
 KEY_SHOW_TASKLOG: keyDef(keys.KEY_L),
 KEY_SHOW_MAP: keyDef(keys.KEY_M),
 KEY_SHOW_SKILL: keyDef(keys.KEY_K),
 KEY_LEFT_DODGE: keyDef(keys.KEY_A, 1, 1),
 KEY_RIGHT_DODGE: keyDef(keys.KEY_D, 1, 1),
 KEY_BACK_DODGE: keyDef(keys.KEY_S, 1, 1),
 KEY_FORWARD_DODGE: keyDef(keys.KEY_W, 1, 1),
 KEY_UP_DODGE: keyDef(keys.KEY_SPACE, 1, 1),
 KEY_DOWN_DODGE: keyDef(keys.KEY_X, 1, 1),
 KEY_WING_SPRINT: keyDef(keys.KEY_W, 1, 4),
 KEY_RIDE: keyDef(keys.KEY_U, 1, 2),
 keys.KEY_K: keyDef(keys.KEY_K),
 keys.KEY_L: keyDef(keys.KEY_L),
 keys.KEY_M: keyDef(keys.KEY_M),
 keys.KEY_P: keyDef(keys.KEY_P),
 keys.KEY_U: keyDef(keys.KEY_U),
 keys.KEY_X: keyDef(keys.KEY_X),
 keys.KEY_Y: keyDef(keys.KEY_Y),
 keys.KEY_Z: keyDef(keys.KEY_Z),
 keys.KEY_LALT: keyDef(keys.KEY_LALT, 1, 0, keys.KEY_RALT),
 keys.KEY_MOUSE0: keyDef(keys.KEY_MOUSE0),
 keys.KEY_MOUSE1: keyDef(keys.KEY_MOUSE1),
 KEY_RESETCAM: keyDef(keys.KEY_MOUSE2),
 keys.KEY_NUMLOCK: keyDef(keys.KEY_NUMLOCK, 1, 0, keys.KEY_MOUSE3),
 keys.KEY_SPACE: keyDef(keys.KEY_SPACE),
 keys.KEY_NUMPADSLASH: keyDef(keys.KEY_NUMPADSLASH),
 keys.KEY_F10: keyDef(keys.KEY_F10),
 KEY_HIDEOTHER: keyDef(keys.KEY_F10),
 keys.KEY_DELETE: keyDef(keys.KEY_DELETE),
 KEY_AUDIOSWITCH: keyDef(keys.KEY_PERIOD),
 KEY_SIMPLE_FIND_POS: keyDef(keys.KEY_F, 1, 2),
 KEY_GROUP_FOLLOW: keyDef(keys.KEY_D, 1, 2),
 KEY_SPRITE_TELEPORT_BACK: keyDef(0),
 KEY_SPRITE_MANUAL_SKILL: keyDef(0),
 KEY_SHOWFPS: keyDef(keys.KEY_R, 1, 2),
 KEY_SHOWUI: keyDef(keys.KEY_F12),
 KEY_REPLAST: keyDef(keys.KEY_R),
 KEY_SBCTRL1: keyDef(keys.KEY_F1),
 KEY_SBCTRL2: keyDef(keys.KEY_F2),
 KEY_SBCTRL3: keyDef(keys.KEY_F3),
 KEY_SBCTRL4: keyDef(keys.KEY_F4),
 KEY_SBCTRL5: keyDef(keys.KEY_F5),
 KEY_SBCTRL6: keyDef(keys.KEY_F6),
 KEY_SBCTRL7: keyDef(keys.KEY_F7),
 KEY_SBCTRL8: keyDef(keys.KEY_F8),
 KEY_SBSKILL1: keyDef(0),
 KEY_SBSKILL2: keyDef(0),
 KEY_SBSKILL3: keyDef(0),
 KEY_SBSKILL4: keyDef(0),
 KEY_SBSKILL5: keyDef(0),
 KEY_SBSKILL6: keyDef(0),
 KEY_SBSKILL7: keyDef(0),
 KEY_SBSKILL8: keyDef(0),
 KEY_SC1: keyDef(keys.KEY_1),
 KEY_SC2: keyDef(keys.KEY_2),
 KEY_SC3: keyDef(keys.KEY_3),
 KEY_SC4: keyDef(keys.KEY_4),
 KEY_SC5: keyDef(keys.KEY_5),
 KEY_SC6: keyDef(keys.KEY_6),
 KEY_SC7: keyDef(keys.KEY_7),
 KEY_SC8: keyDef(keys.KEY_8),
 KEY_SC9: keyDef(keys.KEY_9),
 KEY_SC0: keyDef(keys.KEY_0),
 KEY_FLSC1: keyDef(keys.KEY_1, 1, 2),
 KEY_FLSC2: keyDef(keys.KEY_2, 1, 2),
 KEY_FLSC3: keyDef(keys.KEY_3, 1, 2),
 KEY_FLSC4: keyDef(keys.KEY_4, 1, 2),
 KEY_FLSC5: keyDef(keys.KEY_5, 1, 2),
 KEY_FLSC6: keyDef(keys.KEY_6, 1, 2),
 KEY_FLSC7: keyDef(keys.KEY_7, 1, 2),
 KEY_FLSC8: keyDef(keys.KEY_8, 1, 2),
 KEY_FLSC9: keyDef(keys.KEY_9, 1, 2),
 KEY_FLSC0: keyDef(keys.KEY_0, 1, 2),
 KEY_FLSC11: keyDef(keys.KEY_1, 1, 1),
 KEY_FLSC12: keyDef(keys.KEY_2, 1, 1),
 KEY_FLSC13: keyDef(keys.KEY_3, 1, 1),
 KEY_FLSC14: keyDef(keys.KEY_4, 1, 1),
 KEY_FLSC15: keyDef(keys.KEY_5, 1, 1),
 KEY_FLSC16: keyDef(keys.KEY_6, 1, 1),
 KEY_FLSC17: keyDef(keys.KEY_7, 1, 1),
 KEY_FLSC18: keyDef(keys.KEY_8, 1, 1),
 KEY_FLSC19: keyDef(keys.KEY_9, 1, 1),
 KEY_FLSC10: keyDef(keys.KEY_0, 1, 1),
 KEY_FLSC31: keyDef(0),
 KEY_FLSC32: keyDef(0),
 KEY_FLSC33: keyDef(0),
 KEY_FLSC34: keyDef(0),
 KEY_FLSC35: keyDef(0),
 KEY_FLSC36: keyDef(0),
 KEY_FLSC37: keyDef(0),
 KEY_FLSC38: keyDef(0),
 KEY_FLSC39: keyDef(0),
 KEY_FLSC30: keyDef(0),
 KEY_FLSC41: keyDef(0),
 KEY_FLSC42: keyDef(0),
 KEY_FLSC43: keyDef(0),
 KEY_FLSC44: keyDef(0),
 KEY_FLSC45: keyDef(0),
 KEY_FLSC46: keyDef(0),
 KEY_FLSC47: keyDef(0),
 KEY_FLSC48: keyDef(0),
 KEY_FLSC49: keyDef(0),
 KEY_FLSC40: keyDef(0),
 keys.KEY_1: keyDef(keys.KEY_1, 1, 0),
 keys.KEY_2: keyDef(keys.KEY_2, 1, 0),
 keys.KEY_3: keyDef(keys.KEY_3, 1, 0),
 keys.KEY_4: keyDef(keys.KEY_4, 1, 0),
 keys.KEY_5: keyDef(keys.KEY_5, 1, 0),
 keys.KEY_6: keyDef(keys.KEY_6, 1, 0),
 keys.KEY_7: keyDef(keys.KEY_7, 1, 0),
 keys.KEY_8: keyDef(keys.KEY_8, 1, 0),
 keys.KEY_9: keyDef(keys.KEY_9, 1, 0),
 keys.KEY_0: keyDef(keys.KEY_0, 1, 0),
 keys.KEY_MINUS: keyDef(keys.KEY_MINUS, 1, 0),
 keys.KEY_EQUALS: keyDef(keys.KEY_EQUALS, 1, 0),
 keys.KEY_F1: keyDef(keys.KEY_F1),
 keys.KEY_F2: keyDef(keys.KEY_F2),
 keys.KEY_F3: keyDef(keys.KEY_F3),
 keys.KEY_F4: keyDef(keys.KEY_F4),
 keys.KEY_F5: keyDef(keys.KEY_F5),
 keys.KEY_F6: keyDef(keys.KEY_F6),
 keys.KEY_F7: keyDef(keys.KEY_F7),
 keys.KEY_F8: keyDef(keys.KEY_F8),
 keys.KEY_F9: keyDef(keys.KEY_F9),
 keys.KEY_F10: keyDef(keys.KEY_F10),
 keys.KEY_F11: keyDef(keys.KEY_F11),
 keys.KEY_F12: keyDef(keys.KEY_F12),
 keys.KEY_GRAVE: keyDef(keys.KEY_GRAVE, 1, 2),
 keys.KEY_TAB: keyDef(keys.KEY_TAB),
 keys.KEY_ESCAPE: keyDef(keys.KEY_ESCAPE),
 keys.KEY_LCONTROL: keyDef(keys.KEY_LCONTROL),
 keys.KEY_RCONTROL: keyDef(keys.KEY_RCONTROL),
 KEY_BLOODED: keyDef(0),
 KEY_STORE: keyDef(0),
 KEY_STONE: keyDef(0),
 KEY_ZOOMIN: keyDef(keys.KEY_HOME),
 KEY_ZOOMOUT: keyDef(keys.KEY_END),
 KEY_SHOW_FRIEND: keyDef(keys.KEY_P),
 KEY_SHOWEQUIP: keyDef(keys.KEY_N),
 KEY_SHOWBEAST: keyDef(keys.KEY_F),
 KEY_SHOWSHOP: keyDef(keys.KEY_C, 1, 4),
 KEY_FLSC_PAGE: keyDef(0),
 KEY_FLSC_DOBLELINE: keyDef(keys.KEY_EQUALS, 1, 2),
 KEY_FLSC_HIDE: keyDef(keys.KEY_BACKSLASH, 1, 2),
 KEY_FLSC_VERTICAL: keyDef(keys.KEY_MINUS, 1, 2),
 KEY_FLSC_DOBLELINE1: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_FLSC_HIDE1: keyDef(keys.KEY_BACKSLASH, 1, 1),
 KEY_FLSC_VERTICAL1: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_QREPLY1: keyDef(keys.KEY_NUMPAD1),
 KEY_QREPLY2: keyDef(keys.KEY_NUMPAD2),
 KEY_QREPLY3: keyDef(keys.KEY_NUMPAD3),
 KEY_QREPLY4: keyDef(keys.KEY_NUMPAD4),
 KEY_QREPLY5: keyDef(keys.KEY_NUMPAD5),
 KEY_QREPLY6: keyDef(keys.KEY_NUMPAD6),
 KEY_QREPLY7: keyDef(keys.KEY_NUMPAD7),
 KEY_QREPLY8: keyDef(keys.KEY_NUMPAD8),
 KEY_QREPLY9: keyDef(keys.KEY_NUMPAD9),
 KEY_QREPLY0: keyDef(keys.KEY_NUMPAD0),
 KEY_EDITREPLY: keyDef(keys.KEY_NUMPADPERIOD),
 KEY_PICKALL: keyDef(keys.KEY_Z, 1, 1),
 KEY_FOLLOW: keyDef(keys.KEY_MOUSE4),
 KEY_GHOST: keyDef(0),
 KEY_TRANS_AVATAR: keyDef(keys.KEY_V),
 KEY_SHOW_MORE_RECOMM: keyDef(keys.KEY_O),
 KEY_TEAMATE_1: keyDef(keys.KEY_F1, 1, 1),
 KEY_TEAMATE_2: keyDef(keys.KEY_F2, 1, 1),
 KEY_TEAMATE_3: keyDef(keys.KEY_F3, 1, 1),
 KEY_TEAMATE_4: keyDef(keys.KEY_F4, 1, 1),
 KEY_FB: keyDef(keys.KEY_I, 1, 2),
 KEY_BATTLEFIELD: keyDef(keys.KEY_H, 1, 2),
 KEY_HBSKILL: keyDef(keys.KEY_P, 1, 2),
 KEY_HBATTR: keyDef(keys.KEY_O, 1, 2),
 KEY_HBRIDE: keyDef(keys.KEY_L, 1, 2),
 KEY_CREDIT: keyDef(keys.KEY_M, 1, 2),
 KEY_COMMAND: keyDef(keys.KEY_N, 1, 2),
 KEY_EMOTE: keyDef(keys.KEY_B, 1, 2),
 KEY_CRAFT: keyDef(keys.KEY_V, 1, 2),
 KEY_LEAGUE: keyDef(keys.KEY_J, 1, 2),
 KEY_DODGE: keyDef(keys.KEY_S, 1, 2),
 KEY_STUNT: keyDef(keys.KEY_K, 1, 2),
 KEY_CLANEVENT: keyDef(keys.KEY_D, 1, 2),
 KEY_CLANWAR: keyDef(keys.KEY_A, 1, 2),
 KEY_BUYDOUBLE: keyDef(keys.KEY_E, 1, 2),
 KEY_DEBUG_UP: keyDef(keys.KEY_LBRACKET),
 KEY_SHOW_TOPLOGO: keyDef(keys.KEY_LALT),
 KEY_SHOW_BAG: keyDef(keys.KEY_B),
 KEY_SHOW_ROLEINFO: keyDef(keys.KEY_C),
 KEY_DEBUG_VIEW: keyDef(keys.KEY_D, 1, 4),
 KEY_FUBEN_MONSTER: keyDef(keys.KEY_F, 1, 4),
 KEY_BATTLE_APPLY: keyDef(keys.KEY_Z, 1, 4),
 KEY_SINGLE_DEBUG: keyDef(keys.KEY_S, 1, 4),
 KEY_SUMMARY: keyDef(keys.KEY_NUMPADSTAR),
 KEY_MORPH_DEBUG: keyDef(keys.KEY_M, 1, 4),
 KEY_TINT_DEBUG: keyDef(keys.KEY_T, 1, 4),
 KEY_HIDE_MONSTER_LOGO: keyDef(keys.KEY_F12, 1, 2),
 KYE_MAGICFIELD_DEBUG: keyDef(keys.KEY_Q, 1, 2),
 KEY_SHOW_PVP: keyDef(keys.KEY_H),
 KEY_SHOW_RANK: keyDef(keys.KEY_Y, 1, 1),
 KEY_SHOW_LITTLE_MAP: keyDef(keys.KEY_N),
 KEY_HIDE_PLAYER_MONSTER: keyDef(keys.KEY_F10),
 KEY_SELECT_TEAMER1: keyDef(keys.KEY_F1, 1, 1),
 KEY_SELECT_TEAMER2: keyDef(keys.KEY_F2, 1, 1),
 KEY_SELECT_TEAMER3: keyDef(keys.KEY_F3, 1, 1),
 KEY_SELECT_TEAMER4: keyDef(keys.KEY_F4, 1, 1),
 KEY_SELECT_TEAMER: keyDef(keys.KEY_GRAVE),
 KEY_SELECT_TEAMER_ME: keyDef(keys.KEY_F5, 1, 1),
 KEY_SELECT_TEAMER_ME_SPRITE: keyDef(0),
 keys.KEY_RETURN: keyDef(keys.KEY_RETURN, 1, 0),
 KEY_USE_ITEM1: keyDef(keys.KEY_1, 1, 1),
 KEY_USE_ITEM2: keyDef(keys.KEY_2, 1, 1),
 KEY_USE_ITEM3: keyDef(keys.KEY_3, 1, 1),
 KEY_USE_ITEM4: keyDef(keys.KEY_4, 1, 1),
 KEY_USE_ITEM5: keyDef(keys.KEY_5, 1, 1),
 KEY_USE_ITEM6: keyDef(keys.KEY_6, 1, 1),
 KEY_USE_ITEM7: keyDef(keys.KEY_7, 1, 1),
 KEY_USE_ITEM8: keyDef(keys.KEY_8, 1, 1),
 KEY_USE_ITEM9: keyDef(keys.KEY_9, 1, 1),
 KEY_USE_ITEM10: keyDef(keys.KEY_0, 1, 1),
 KEY_USE_ITEM11: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_USE_ITEM12: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_USE_ITEM13: keyDef(0),
 KEY_USE_ITEM14: keyDef(0),
 KEY_USE_ITEM15: keyDef(0),
 KEY_USE_ITEM16: keyDef(0),
 KEY_USE_ITEM17: keyDef(0),
 KEY_USE_ITEM18: keyDef(0),
 KEY_USE_ITEM19: keyDef(0),
 KEY_USE_ITEM20: keyDef(0),
 KEY_USE_ITEM21: keyDef(0),
 KEY_USE_ITEM22: keyDef(0),
 KEY_USE_ITEM23: keyDef(0),
 KEY_USE_ITEM24: keyDef(0),
 KEY_USE_ITEM25: keyDef(0),
 KEY_USE_ITEM26: keyDef(0),
 KEY_USE_ITEM27: keyDef(0),
 KEY_USE_ITEM28: keyDef(0),
 KEY_USE_ITEM29: keyDef(0),
 KEY_USE_ITEM30: keyDef(0),
 KEY_USE_ITEM31: keyDef(0),
 KEY_USE_ITEM32: keyDef(0),
 KEY_USE_ITEM33: keyDef(0),
 KEY_USE_ITEM34: keyDef(0),
 KEY_USE_ITEM35: keyDef(0),
 KEY_USE_ITEM36: keyDef(0),
 KEY_USE_ITEM37: keyDef(0),
 KEY_USE_ITEM38: keyDef(0),
 KEY_USE_ITEM39: keyDef(0),
 KEY_USE_ITEM40: keyDef(0),
 KEY_USE_ITEM41: keyDef(0),
 KEY_USE_ITEM42: keyDef(0),
 KEY_USE_ITEM43: keyDef(0),
 KEY_USE_ITEM44: keyDef(0),
 KEY_USE_ITEM45: keyDef(0),
 KEY_USE_ITEM46: keyDef(0),
 KEY_USE_ITEM47: keyDef(0),
 KEY_USE_ITEM48: keyDef(0),
 KEY_DRAG_UI: keyDef(keys.KEY_F11),
 KEY_CHANGE_CURSOR: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_SWITCH_LAST: keyDef(0),
 KEY_CAMERA_NEAR: keyDef(keys.KEY_MOUSE_ROLLUP),
 KEY_CAMERA_FAR: keyDef(keys.KEY_MOUSE_ROLLDOWN),
 KEY_CAST_SKILL_TO_SELF: keyDef(keys.KEY_LALT),
 KEY_SHOW_GENERAL_SKILL: keyDef(keys.KEY_N),
 KEY_SHOW_LIFE_SKILL: keyDef(keys.KEY_V),
 KEY_SHOW_MAIL: keyDef(keys.KEY_J),
 KEY_SHOW_CONSIGN: keyDef(keys.KEY_R),
 KEY_RESUME_FREE_ROTATE: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_LEAVE_LOCK_ROTATE: keyDef(keys.KEY_LCONTROL, 1),
 KEY_WEAPON_IN_HAND: keyDef(keys.KEY_SLASH),
 KEY_SHOW_CAMERA: keyDef(keys.KEY_F9, 1, 2),
 KEY_QTE_SKILL1: keyDef(0),
 KEY_QTE_SKILL2: keyDef(0),
 KEY_LEAVE_ZAIJU: keyDef(keys.KEY_F8),
 KEY_ASSIGN_CONFIRM: keyDef(keys.KEY_NUMPAD1),
 KEY_ASSIGN_CANCEL: keyDef(keys.KEY_NUMPAD2),
 KEY_ASSIGN_GREED: keyDef(keys.KEY_NUMPAD0),
 KEY_BF_RETURN: keyDef(keys.KEY_NUMPAD6),
 KEY_BF_COUNT: keyDef(keys.KEY_NUMPAD5),
 KEY_SHOW_HELP: keyDef(keys.KEY_H, 1, 2),
 KEY_SHOW_PLAYRECOMM: keyDef(keys.KEY_U),
 KEY_SWITCH_RUN_WALK: keyDef(keys.KEY_NUMPADSLASH),
 KEY_SHOW_DELEGATION: keyDef(keys.KEY_I),
 KEY_RIDE_WING: keyDef(0),
 KEY_NEXT_TRACK_TAB: keyDef(keys.KEY_TAB, mods=2),
 KEY_LOCK_TARGETS_TARGET: keyDef(0),
 KEY_TURN_CAMERA: keyDef(keys.KEY_Q, 1, 1),
 KEY_ROLE_CARD: keyDef(keys.KEY_L, 1, 1),
 KEY_FENG_WU_ZHI: keyDef(keys.KEY_I, 1, 1),
 KEY_SPRITE_WAR: keyDef(keys.KEY_G, 1, 1),
 KEY_PERSON_SPACE: keyDef(keys.KEY_C, 1, 1),
 KEY_MOUNT_WING: keyDef(keys.KEY_Z, 1, 1),
 KEY_STALL: keyDef(keys.KEY_F, 1, 1),
 KEY_PVP_ENHANCE: keyDef(0),
 KEY_CHAT_ROOM: keyDef(keys.KEY_P, 1, 1),
 KEY_JIE_QI: keyDef(keys.KEY_J, 1, 2),
 KEY_MENTOR: keyDef(keys.KEY_Z, 1, 2),
 KEY_PVP_JJC: keyDef(keys.KEY_H, 1, 4),
 KEY_GUI_BAO: keyDef(keys.KEY_Y, 1, 4),
 KEY_USER_BACK: keyDef(keys.KEY_O, 1, 2),
 KEY_SUMMON_FRIEND: keyDef(keys.KEY_P, 1, 2),
 KEY_ITEM_SOURCE: keyDef(keys.KEY_F7),
 KEY_SKILL_MACRO: keyDef(keys.KEY_B, 1, 1),
 KEY_CHATLOG_SOUND_RECORD: keyDef(keys.KEY_A, 1, 2),
 KEY_CHAT_TO_FRIEND_SOUND_RECORD: keyDef(keys.KEY_X, 1, 2),
 KEY_OPEN_WING_WORLD_UI: keyDef(keys.KEY_J, 1, 1),
 KEY_OPEN_ASSASSINATION_MAIN_UI: keyDef(keys.KEY_K, 1, 1),
 KEY_VOICE: keyDef(keys.KEY_Q, 1, 2),
 KEY_NPCV2_SPEED: keyDef(keys.KEY_Z),
 KEY_NPCV2_QUICK: keyDef(keys.KEY_R),
 KEY_CARD_SYSTEM: keyDef(keys.KEY_H, 1, 1)}
BnsHotkeyMap = {KEY_FORWARD: keyDef(keys.KEY_W, 1, 0, keys.KEY_UPARROW),
 KEY_LEFTTURN: keyDef(0),
 KEY_RIGHTTURN: keyDef(0),
 KEY_BACKWARD: keyDef(keys.KEY_S, 1, 0, keys.KEY_DOWNARROW),
 KEY_DOWN: keyDef(keys.KEY_X),
 KEY_WINGFLYUP: keyDef(keys.KEY_SPACE, 1, 4),
 KEY_WINGFLYDOWN: keyDef(keys.KEY_X, 1, 4),
 KEY_MOVERIGHT: keyDef(keys.KEY_D, 1, 0, keys.KEY_RIGHTARROW),
 KEY_MOVELEFT: keyDef(keys.KEY_A, 1, 0, keys.KEY_LEFTARROW),
 KEY_SWITCHMODE: keyDef(keys.KEY_SCROLL),
 keys.KEY_B: keyDef(keys.KEY_B),
 keys.KEY_C: keyDef(keys.KEY_C),
 KEY_RELATION: keyDef(keys.KEY_G, 1, 2),
 keys.KEY_I: keyDef(keys.KEY_I),
 KEY_PICK_ITEM: keyDef(keys.KEY_F, 1, 0, keys.KEY_Z),
 KEY_RIDE: keyDef(keys.KEY_U, 1, 2),
 keys.KEY_H: keyDef(keys.KEY_H),
 keys.KEY_K: keyDef(keys.KEY_K),
 keys.KEY_L: keyDef(keys.KEY_L),
 keys.KEY_M: keyDef(keys.KEY_M),
 keys.KEY_P: keyDef(keys.KEY_P),
 keys.KEY_T: keyDef(keys.KEY_T),
 keys.KEY_U: keyDef(keys.KEY_U),
 keys.KEY_Y: keyDef(keys.KEY_Y),
 keys.KEY_Z: keyDef(keys.KEY_Z),
 keys.KEY_LALT: keyDef(keys.KEY_LALT),
 keys.KEY_MOUSE0: keyDef(keys.KEY_MOUSE0),
 keys.KEY_MOUSE1: keyDef(keys.KEY_MOUSE1),
 KEY_RESETCAM: keyDef(keys.KEY_MOUSE2),
 keys.KEY_NUMLOCK: keyDef(keys.KEY_NUMLOCK, 1, 0, keys.KEY_MOUSE3),
 keys.KEY_SPACE: keyDef(keys.KEY_SPACE),
 keys.KEY_NUMPADSLASH: keyDef(keys.KEY_NUMPADSLASH),
 KEY_HIDEOTHER: keyDef(keys.KEY_F10),
 keys.KEY_DELETE: keyDef(keys.KEY_DELETE),
 KEY_AUDIOSWITCH: keyDef(keys.KEY_PERIOD),
 KEY_SIMPLE_FIND_POS: keyDef(keys.KEY_F, 1, 2),
 KEY_GROUP_FOLLOW: keyDef(keys.KEY_D, 1, 2),
 KEY_SPRITE_TELEPORT_BACK: keyDef(0),
 KEY_SPRITE_MANUAL_SKILL: keyDef(0),
 KEY_SHOWFPS: keyDef(keys.KEY_R, 1, 2),
 KEY_SHOWUI: keyDef(keys.KEY_F12),
 KEY_REPLAST: keyDef(keys.KEY_R),
 KEY_SBCTRL1: keyDef(keys.KEY_F1),
 KEY_SBCTRL2: keyDef(keys.KEY_F2),
 KEY_SBCTRL3: keyDef(keys.KEY_F3),
 KEY_SBCTRL4: keyDef(keys.KEY_F4),
 KEY_SBCTRL5: keyDef(keys.KEY_F5),
 KEY_SBCTRL6: keyDef(keys.KEY_F6),
 KEY_SBCTRL7: keyDef(keys.KEY_F7),
 KEY_SBCTRL8: keyDef(keys.KEY_F8),
 KEY_SBSKILL1: keyDef(0),
 KEY_SBSKILL2: keyDef(0),
 KEY_SBSKILL3: keyDef(0),
 KEY_SBSKILL4: keyDef(0),
 KEY_SBSKILL5: keyDef(0),
 KEY_SBSKILL6: keyDef(0),
 KEY_SBSKILL7: keyDef(0),
 KEY_SBSKILL8: keyDef(0),
 KEY_SC1: keyDef(keys.KEY_1),
 KEY_SC2: keyDef(keys.KEY_2),
 KEY_SC3: keyDef(keys.KEY_3),
 KEY_SC4: keyDef(keys.KEY_4),
 KEY_SC5: keyDef(keys.KEY_5),
 KEY_SC6: keyDef(keys.KEY_6),
 KEY_SC7: keyDef(keys.KEY_7),
 KEY_SC8: keyDef(keys.KEY_8),
 KEY_SC9: keyDef(keys.KEY_9),
 KEY_SC0: keyDef(keys.KEY_0),
 KEY_FLSC1: keyDef(keys.KEY_1, 1, 2),
 KEY_FLSC2: keyDef(keys.KEY_2, 1, 2),
 KEY_FLSC3: keyDef(keys.KEY_3, 1, 2),
 KEY_FLSC4: keyDef(keys.KEY_4, 1, 2),
 KEY_FLSC5: keyDef(keys.KEY_5, 1, 2),
 KEY_FLSC6: keyDef(keys.KEY_6, 1, 2),
 KEY_FLSC7: keyDef(keys.KEY_7, 1, 2),
 KEY_FLSC8: keyDef(keys.KEY_8, 1, 2),
 KEY_FLSC9: keyDef(keys.KEY_9, 1, 2),
 KEY_FLSC0: keyDef(keys.KEY_0, 1, 2),
 KEY_FLSC11: keyDef(keys.KEY_1, 1, 1),
 KEY_FLSC12: keyDef(keys.KEY_2, 1, 1),
 KEY_FLSC13: keyDef(keys.KEY_3, 1, 1),
 KEY_FLSC14: keyDef(keys.KEY_4, 1, 1),
 KEY_FLSC15: keyDef(keys.KEY_5, 1, 1),
 KEY_FLSC16: keyDef(keys.KEY_6, 1, 1),
 KEY_FLSC17: keyDef(keys.KEY_7, 1, 1),
 KEY_FLSC18: keyDef(keys.KEY_8, 1, 1),
 KEY_FLSC19: keyDef(keys.KEY_9, 1, 1),
 KEY_FLSC10: keyDef(keys.KEY_0, 1, 1),
 KEY_FLSC31: keyDef(0),
 KEY_FLSC32: keyDef(0),
 KEY_FLSC33: keyDef(0),
 KEY_FLSC34: keyDef(0),
 KEY_FLSC35: keyDef(0),
 KEY_FLSC36: keyDef(0),
 KEY_FLSC37: keyDef(0),
 KEY_FLSC38: keyDef(0),
 KEY_FLSC39: keyDef(0),
 KEY_FLSC30: keyDef(0),
 KEY_FLSC41: keyDef(0),
 KEY_FLSC42: keyDef(0),
 KEY_FLSC43: keyDef(0),
 KEY_FLSC44: keyDef(0),
 KEY_FLSC45: keyDef(0),
 KEY_FLSC46: keyDef(0),
 KEY_FLSC47: keyDef(0),
 KEY_FLSC48: keyDef(0),
 KEY_FLSC49: keyDef(0),
 KEY_FLSC40: keyDef(0),
 keys.KEY_1: keyDef(keys.KEY_1, 1, 0),
 keys.KEY_2: keyDef(keys.KEY_2, 1, 0),
 keys.KEY_3: keyDef(keys.KEY_3, 1, 0),
 keys.KEY_4: keyDef(keys.KEY_4, 1, 0),
 keys.KEY_5: keyDef(keys.KEY_5, 1, 0),
 keys.KEY_6: keyDef(keys.KEY_Q, 1, 0),
 keys.KEY_7: keyDef(keys.KEY_E, 1, 0),
 keys.KEY_8: keyDef(keys.KEY_R, 1, 0),
 keys.KEY_9: keyDef(keys.KEY_T, 1, 0),
 keys.KEY_0: keyDef(keys.KEY_G, 1, 0),
 keys.KEY_MINUS: keyDef(keys.KEY_MINUS, 1, 0),
 keys.KEY_EQUALS: keyDef(keys.KEY_EQUALS, 1, 0),
 keys.KEY_F1: keyDef(keys.KEY_F1),
 keys.KEY_F2: keyDef(keys.KEY_F2),
 keys.KEY_F3: keyDef(keys.KEY_F3),
 keys.KEY_F4: keyDef(keys.KEY_F4),
 keys.KEY_F5: keyDef(keys.KEY_F5),
 keys.KEY_F6: keyDef(keys.KEY_F6),
 keys.KEY_F7: keyDef(keys.KEY_F7),
 keys.KEY_F8: keyDef(keys.KEY_F8),
 keys.KEY_F9: keyDef(keys.KEY_F9),
 keys.KEY_F10: keyDef(keys.KEY_F10),
 keys.KEY_F11: keyDef(keys.KEY_F11),
 keys.KEY_F12: keyDef(keys.KEY_F12),
 keys.KEY_GRAVE: keyDef(keys.KEY_GRAVE, 1, 2),
 keys.KEY_TAB: keyDef(keys.KEY_TAB),
 keys.KEY_ESCAPE: keyDef(keys.KEY_ESCAPE),
 keys.KEY_LCONTROL: keyDef(keys.KEY_LCONTROL),
 keys.KEY_RCONTROL: keyDef(keys.KEY_RCONTROL),
 KEY_BLOODED: keyDef(0),
 KEY_STORE: keyDef(0),
 KEY_STONE: keyDef(0),
 KEY_ZOOMIN: keyDef(keys.KEY_HOME),
 KEY_ZOOMOUT: keyDef(keys.KEY_END),
 KEY_SHOW_FRIEND: keyDef(keys.KEY_P),
 KEY_SHOWEQUIP: keyDef(0),
 KEY_SHOWBEAST: keyDef(keys.KEY_F),
 KEY_SHOWSHOP: keyDef(keys.KEY_C, 1, 4),
 KEY_FLSC_PAGE: keyDef(0),
 KEY_FLSC_DOBLELINE: keyDef(keys.KEY_EQUALS, 1, 2),
 KEY_FLSC_HIDE: keyDef(keys.KEY_BACKSLASH, 1, 2),
 KEY_FLSC_VERTICAL: keyDef(keys.KEY_MINUS, 1, 2),
 KEY_FLSC_DOBLELINE1: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_FLSC_HIDE1: keyDef(keys.KEY_BACKSLASH, 1, 1),
 KEY_FLSC_VERTICAL1: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_QREPLY1: keyDef(keys.KEY_NUMPAD1),
 KEY_QREPLY2: keyDef(keys.KEY_NUMPAD2),
 KEY_QREPLY3: keyDef(keys.KEY_NUMPAD3),
 KEY_QREPLY4: keyDef(keys.KEY_NUMPAD4),
 KEY_QREPLY5: keyDef(keys.KEY_NUMPAD5),
 KEY_QREPLY6: keyDef(keys.KEY_NUMPAD6),
 KEY_QREPLY7: keyDef(keys.KEY_NUMPAD7),
 KEY_QREPLY8: keyDef(keys.KEY_NUMPAD8),
 KEY_QREPLY9: keyDef(keys.KEY_NUMPAD9),
 KEY_QREPLY0: keyDef(keys.KEY_NUMPAD0),
 KEY_EDITREPLY: keyDef(keys.KEY_NUMPADPERIOD),
 KEY_PICKALL: keyDef(keys.KEY_Z, 1, 1),
 KEY_FOLLOW: keyDef(keys.KEY_MOUSE4),
 KEY_GHOST: keyDef(0),
 KEY_TRANS_AVATAR: keyDef(keys.KEY_V),
 KEY_SHOW_MORE_RECOMM: keyDef(keys.KEY_O),
 KEY_TEAMATE_1: keyDef(keys.KEY_F1, 1, 1),
 KEY_TEAMATE_2: keyDef(keys.KEY_F2, 1, 1),
 KEY_TEAMATE_3: keyDef(keys.KEY_F3, 1, 1),
 KEY_TEAMATE_4: keyDef(keys.KEY_F4, 1, 1),
 KEY_BATTLEFIELD: keyDef(keys.KEY_H, 1, 2),
 KEY_HBSKILL: keyDef(keys.KEY_P, 1, 2),
 KEY_HBATTR: keyDef(keys.KEY_O, 1, 2),
 KEY_HBRIDE: keyDef(keys.KEY_L, 1, 2),
 KEY_CREDIT: keyDef(keys.KEY_M, 1, 2),
 KEY_COMMAND: keyDef(keys.KEY_N, 1, 2),
 KEY_EMOTE: keyDef(keys.KEY_B, 1, 2),
 KEY_CRAFT: keyDef(keys.KEY_V, 1, 2),
 KEY_LEAGUE: keyDef(keys.KEY_J, 1, 2),
 KEY_DODGE: keyDef(keys.KEY_S, 1, 2),
 KEY_STUNT: keyDef(keys.KEY_K, 1, 2),
 KEY_CLANEVENT: keyDef(keys.KEY_D, 1, 2),
 KEY_CLANWAR: keyDef(keys.KEY_A, 1, 2),
 KEY_BUYDOUBLE: keyDef(keys.KEY_E, 1, 2),
 KEY_DEBUG_UP: keyDef(keys.KEY_LBRACKET),
 KEY_SHOW_TOPLOGO: keyDef(keys.KEY_LALT),
 KEY_SHOW_BAG: keyDef(keys.KEY_B),
 KEY_SHOW_ROLEINFO: keyDef(keys.KEY_C),
 KEY_DEBUG_VIEW: keyDef(keys.KEY_D, 1, 4),
 KEY_FUBEN_MONSTER: keyDef(keys.KEY_F, 1, 4),
 KEY_BATTLE_APPLY: keyDef(keys.KEY_Z, 1, 4),
 KEY_SINGLE_DEBUG: keyDef(keys.KEY_S, 1, 4),
 KEY_SUMMARY: keyDef(keys.KEY_NUMPADSTAR),
 KEY_MORPH_DEBUG: keyDef(keys.KEY_M, 1, 4),
 KEY_TINT_DEBUG: keyDef(keys.KEY_T, 1, 4),
 KEY_HIDE_MONSTER_LOGO: keyDef(keys.KEY_F12, 1, 2),
 KYE_MAGICFIELD_DEBUG: keyDef(keys.KEY_Q, 1, 2),
 KEY_SHOW_TEAMINFO: keyDef(keys.KEY_T, 1, 2),
 KEY_SHOW_TASKLOG: keyDef(keys.KEY_L),
 KEY_SHOW_MAP: keyDef(keys.KEY_M),
 KEY_SHOW_SKILL: keyDef(keys.KEY_K),
 KEY_LEFT_DODGE: keyDef(keys.KEY_A, 1, 1),
 KEY_RIGHT_DODGE: keyDef(keys.KEY_D, 1, 1),
 KEY_BACK_DODGE: keyDef(keys.KEY_S, 1, 1),
 KEY_FORWARD_DODGE: keyDef(keys.KEY_W, 1, 1),
 KEY_UP_DODGE: keyDef(keys.KEY_SPACE, 1, 1),
 KEY_DOWN_DODGE: keyDef(keys.KEY_X, 1, 1),
 KEY_WING_SPRINT: keyDef(keys.KEY_W, 1, 4),
 KEY_SHOW_PVP: keyDef(keys.KEY_H),
 KEY_SHOW_RANK: keyDef(keys.KEY_Y, 1, 1),
 KEY_SHOW_LITTLE_MAP: keyDef(keys.KEY_N),
 KEY_HIDE_PLAYER_MONSTER: keyDef(keys.KEY_F10),
 KEY_SELECT_TEAMER1: keyDef(keys.KEY_F1, 1, 1),
 KEY_SELECT_TEAMER2: keyDef(keys.KEY_F2, 1, 1),
 KEY_SELECT_TEAMER3: keyDef(keys.KEY_F3, 1, 1),
 KEY_SELECT_TEAMER4: keyDef(keys.KEY_F4, 1, 1),
 KEY_SELECT_TEAMER: keyDef(keys.KEY_GRAVE),
 KEY_SELECT_TEAMER_ME: keyDef(keys.KEY_F5, 1, 1),
 KEY_SELECT_TEAMER_ME_SPRITE: keyDef(0),
 keys.KEY_RETURN: keyDef(keys.KEY_RETURN, 1, 0),
 KEY_USE_ITEM1: keyDef(keys.KEY_1, 1, 1),
 KEY_USE_ITEM2: keyDef(keys.KEY_2, 1, 1),
 KEY_USE_ITEM3: keyDef(keys.KEY_3, 1, 1),
 KEY_USE_ITEM4: keyDef(keys.KEY_4, 1, 1),
 KEY_USE_ITEM5: keyDef(keys.KEY_5, 1, 1),
 KEY_USE_ITEM6: keyDef(keys.KEY_6, 1, 1),
 KEY_USE_ITEM7: keyDef(keys.KEY_7, 1, 1),
 KEY_USE_ITEM8: keyDef(keys.KEY_8, 1, 1),
 KEY_USE_ITEM9: keyDef(keys.KEY_9, 1, 1),
 KEY_USE_ITEM10: keyDef(keys.KEY_0, 1, 1),
 KEY_USE_ITEM11: keyDef(keys.KEY_MINUS, 1, 1),
 KEY_USE_ITEM12: keyDef(keys.KEY_EQUALS, 1, 1),
 KEY_USE_ITEM13: keyDef(0),
 KEY_USE_ITEM14: keyDef(0),
 KEY_USE_ITEM15: keyDef(0),
 KEY_USE_ITEM16: keyDef(0),
 KEY_USE_ITEM17: keyDef(0),
 KEY_USE_ITEM18: keyDef(0),
 KEY_USE_ITEM19: keyDef(0),
 KEY_USE_ITEM20: keyDef(0),
 KEY_USE_ITEM21: keyDef(0),
 KEY_USE_ITEM22: keyDef(0),
 KEY_USE_ITEM23: keyDef(0),
 KEY_USE_ITEM24: keyDef(0),
 KEY_USE_ITEM25: keyDef(0),
 KEY_USE_ITEM26: keyDef(0),
 KEY_USE_ITEM27: keyDef(0),
 KEY_USE_ITEM28: keyDef(0),
 KEY_USE_ITEM29: keyDef(0),
 KEY_USE_ITEM30: keyDef(0),
 KEY_USE_ITEM31: keyDef(0),
 KEY_USE_ITEM32: keyDef(0),
 KEY_USE_ITEM33: keyDef(0),
 KEY_USE_ITEM34: keyDef(0),
 KEY_USE_ITEM35: keyDef(0),
 KEY_USE_ITEM36: keyDef(0),
 KEY_USE_ITEM37: keyDef(0),
 KEY_USE_ITEM38: keyDef(0),
 KEY_USE_ITEM39: keyDef(0),
 KEY_USE_ITEM40: keyDef(0),
 KEY_USE_ITEM41: keyDef(0),
 KEY_USE_ITEM42: keyDef(0),
 KEY_USE_ITEM43: keyDef(0),
 KEY_USE_ITEM44: keyDef(0),
 KEY_USE_ITEM45: keyDef(0),
 KEY_USE_ITEM46: keyDef(0),
 KEY_USE_ITEM47: keyDef(0),
 KEY_USE_ITEM48: keyDef(0),
 KEY_DRAG_UI: keyDef(keys.KEY_F11),
 KEY_CHANGE_CURSOR: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_SWITCH_LAST: keyDef(0),
 KEY_CAMERA_NEAR: keyDef(keys.KEY_MOUSE_ROLLUP),
 KEY_CAMERA_FAR: keyDef(keys.KEY_MOUSE_ROLLDOWN),
 KEY_CAST_SKILL_TO_SELF: keyDef(keys.KEY_LALT),
 KEY_SHOW_GENERAL_SKILL: keyDef(keys.KEY_N),
 KEY_SHOW_LIFE_SKILL: keyDef(keys.KEY_V),
 KEY_SHOW_MAIL: keyDef(keys.KEY_J),
 KEY_SHOW_CONSIGN: keyDef(keys.KEY_Y, 1, 2),
 KEY_RESUME_FREE_ROTATE: keyDef(keys.KEY_LCONTROL, 1, 2),
 KEY_LEAVE_LOCK_ROTATE: keyDef(keys.KEY_LCONTROL, 1),
 KEY_WEAPON_IN_HAND: keyDef(keys.KEY_SLASH),
 KEY_SHOW_CAMERA: keyDef(keys.KEY_F9, 1, 2),
 KEY_QTE_SKILL1: keyDef(0),
 KEY_QTE_SKILL2: keyDef(0),
 KEY_LEAVE_ZAIJU: keyDef(keys.KEY_F8),
 KEY_ASSIGN_CONFIRM: keyDef(keys.KEY_NUMPAD1),
 KEY_ASSIGN_CANCEL: keyDef(keys.KEY_NUMPAD2),
 KEY_ASSIGN_GREED: keyDef(keys.KEY_NUMPAD0),
 KEY_BF_RETURN: keyDef(keys.KEY_NUMPAD6),
 KEY_BF_COUNT: keyDef(keys.KEY_NUMPAD5),
 KEY_SHOW_HELP: keyDef(keys.KEY_H, 1, 2),
 KEY_SHOW_PLAYRECOMM: keyDef(keys.KEY_U),
 KEY_SWITCH_RUN_WALK: keyDef(keys.KEY_NUMPADSLASH),
 KEY_SHOW_DELEGATION: keyDef(keys.KEY_I),
 KEY_RIDE_WING: keyDef(0),
 KEY_NEXT_TRACK_TAB: keyDef(keys.KEY_TAB, mods=2),
 KEY_LOCK_TARGETS_TARGET: keyDef(0),
 KEY_TURN_CAMERA: keyDef(keys.KEY_Q, 1, 1),
 KEY_ROLE_CARD: keyDef(keys.KEY_L, 1, 1),
 KEY_FENG_WU_ZHI: keyDef(keys.KEY_I, 1, 1),
 KEY_SPRITE_WAR: keyDef(keys.KEY_G, 1, 1),
 KEY_PERSON_SPACE: keyDef(keys.KEY_C, 1, 1),
 KEY_MOUNT_WING: keyDef(keys.KEY_Z, 1, 1),
 KEY_STALL: keyDef(keys.KEY_F, 1, 1),
 KEY_PVP_ENHANCE: keyDef(0),
 KEY_CHAT_ROOM: keyDef(keys.KEY_P, 1, 1),
 KEY_JIE_QI: keyDef(keys.KEY_J, 1, 2),
 KEY_MENTOR: keyDef(keys.KEY_Z, 1, 2),
 KEY_PVP_JJC: keyDef(keys.KEY_H, 1, 4),
 KEY_GUI_BAO: keyDef(keys.KEY_Y, 1, 4),
 KEY_USER_BACK: keyDef(keys.KEY_O, 1, 2),
 KEY_SUMMON_FRIEND: keyDef(keys.KEY_P, 1, 2),
 KEY_ITEM_SOURCE: keyDef(keys.KEY_F7),
 KEY_SKILL_MACRO: keyDef(keys.KEY_B, 1, 1),
 KEY_CHATLOG_SOUND_RECORD: keyDef(keys.KEY_A, 1, 2),
 KEY_CHAT_TO_FRIEND_SOUND_RECORD: keyDef(keys.KEY_X, 1, 2),
 KEY_DOTA_MAP_MARK: keyDef(keys.KEY_M),
 KEY_DOTA_MAP_ATK: keyDef(keys.KEY_V),
 KEY_DOTA_MAP_RETREAT: keyDef(keys.KEY_X),
 KEY_DOTA_MAP_GATHER: keyDef(keys.KEY_C),
 KEY_OPEN_WING_WORLD_UI: keyDef(keys.KEY_J, 1, 1),
 KEY_OPEN_ASSASSINATION_MAIN_UI: keyDef(keys.KEY_K, 1, 1),
 KEY_VOICE: keyDef(keys.KEY_Q, 1, 2),
 KEY_NPCV2_SPEED: keyDef(keys.KEY_Z),
 KEY_NPCV2_QUICK: keyDef(keys.KEY_R),
 KEY_CARD_SYSTEM: keyDef(keys.KEY_H, 1, 1)}
BfDotaHotKeyPart_Default = {KEY_DOTA_SKILL0: keyDef(keys.KEY_1, 1),
 KEY_DOTA_SKILL1: keyDef(0),
 KEY_DOTA_SKILL2: keyDef(keys.KEY_2, 1),
 KEY_DOTA_SKILL3: keyDef(keys.KEY_3, 1),
 KEY_DOTA_SKILL4: keyDef(keys.KEY_4, 1),
 KEY_DOTA_SKILL5: keyDef(keys.KEY_5, 1),
 KEY_DOTA_SKILL6: keyDef(keys.KEY_6, 1),
 KEY_DOTA_SKILL7: keyDef(keys.KEY_7, 1),
 KEY_DOTA_ITEM0: keyDef(keys.KEY_1, 1, 1),
 KEY_DOTA_ITEM1: keyDef(keys.KEY_2, 1, 1),
 KEY_DOTA_ITEM2: keyDef(keys.KEY_3, 1, 1),
 KEY_DOTA_ITEM3: keyDef(keys.KEY_4, 1, 1),
 KEY_DOTA_ITEM4: keyDef(keys.KEY_5, 1, 1),
 KEY_DOTA_ITEM5: keyDef(keys.KEY_6, 1, 1),
 KEY_DOTA_OPEN_SHOP: keyDef(keys.KEY_N, 1),
 KEY_DOTA_RETURN_HOME: keyDef(keys.KEY_B, 1),
 KEY_DOTA_LEARN_SKILL: keyDef(keys.KEY_LCONTROL, 1),
 KEY_DOTA_SHOW_DETAIL: keyDef(keys.KEY_GRAVE, 1),
 KEY_DOTA_SHOW_PROP: keyDef(keys.KEY_Z, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT0: keyDef(keys.KEY_F1, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT1: keyDef(keys.KEY_F2, 1),
 KEY_DOTA_MAP_MARK: keyDef(keys.KEY_M),
 KEY_DOTA_MAP_ATK: keyDef(keys.KEY_V),
 KEY_DOTA_MAP_RETREAT: keyDef(keys.KEY_X),
 KEY_DOTA_MAP_GATHER: keyDef(keys.KEY_C)}
BfDotaHotKeyPart_WanMei = {KEY_DOTA_SKILL0: keyDef(keys.KEY_1, 1),
 KEY_DOTA_SKILL1: keyDef(0),
 KEY_DOTA_SKILL2: keyDef(keys.KEY_2, 1),
 KEY_DOTA_SKILL3: keyDef(keys.KEY_3, 1),
 KEY_DOTA_SKILL4: keyDef(keys.KEY_4, 1),
 KEY_DOTA_SKILL5: keyDef(keys.KEY_5, 1),
 KEY_DOTA_SKILL6: keyDef(keys.KEY_6, 1),
 KEY_DOTA_SKILL7: keyDef(keys.KEY_7, 1),
 KEY_DOTA_ITEM0: keyDef(keys.KEY_1, 1, 1),
 KEY_DOTA_ITEM1: keyDef(keys.KEY_2, 1, 1),
 KEY_DOTA_ITEM2: keyDef(keys.KEY_3, 1, 1),
 KEY_DOTA_ITEM3: keyDef(keys.KEY_4, 1, 1),
 KEY_DOTA_ITEM4: keyDef(keys.KEY_5, 1, 1),
 KEY_DOTA_ITEM5: keyDef(keys.KEY_6, 1, 1),
 KEY_DOTA_OPEN_SHOP: keyDef(keys.KEY_N, 1),
 KEY_DOTA_RETURN_HOME: keyDef(keys.KEY_B, 1),
 KEY_DOTA_LEARN_SKILL: keyDef(keys.KEY_LCONTROL, 1),
 KEY_DOTA_SHOW_DETAIL: keyDef(keys.KEY_GRAVE, 1),
 KEY_DOTA_SHOW_PROP: keyDef(keys.KEY_Z, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT0: keyDef(keys.KEY_F1, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT1: keyDef(keys.KEY_F2, 1),
 KEY_DOTA_MAP_MARK: keyDef(keys.KEY_M),
 KEY_DOTA_MAP_ATK: keyDef(keys.KEY_V),
 KEY_DOTA_MAP_RETREAT: keyDef(keys.KEY_X),
 KEY_DOTA_MAP_GATHER: keyDef(keys.KEY_C)}
BfDotaHotKeyPart_Action = {KEY_DOTA_SKILL0: keyDef(0, 1),
 KEY_DOTA_SKILL1: keyDef(0),
 KEY_DOTA_SKILL2: keyDef(keys.KEY_Q, 1),
 KEY_DOTA_SKILL3: keyDef(keys.KEY_E, 1),
 KEY_DOTA_SKILL4: keyDef(keys.KEY_R, 1),
 KEY_DOTA_SKILL5: keyDef(keys.KEY_T, 1),
 KEY_DOTA_SKILL6: keyDef(keys.KEY_F, 1),
 KEY_DOTA_SKILL7: keyDef(keys.KEY_G, 1),
 KEY_DOTA_ITEM0: keyDef(keys.KEY_1, 1),
 KEY_DOTA_ITEM1: keyDef(keys.KEY_2, 1),
 KEY_DOTA_ITEM2: keyDef(keys.KEY_3, 1),
 KEY_DOTA_ITEM3: keyDef(keys.KEY_4, 1),
 KEY_DOTA_ITEM4: keyDef(keys.KEY_5, 1),
 KEY_DOTA_ITEM5: keyDef(keys.KEY_6, 1),
 KEY_DOTA_OPEN_SHOP: keyDef(keys.KEY_N, 1),
 KEY_DOTA_RETURN_HOME: keyDef(keys.KEY_B, 1),
 KEY_DOTA_LEARN_SKILL: keyDef(keys.KEY_LCONTROL, 1),
 KEY_DOTA_SHOW_DETAIL: keyDef(keys.KEY_GRAVE, 1),
 KEY_DOTA_SHOW_PROP: keyDef(keys.KEY_Z, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT0: keyDef(keys.KEY_F1, 1),
 KEY_DOTA_BUY_ITEM_SHORTCUT1: keyDef(keys.KEY_F2, 1),
 KEY_DOTA_MAP_MARK: keyDef(keys.KEY_M),
 KEY_DOTA_MAP_ATK: keyDef(keys.KEY_V),
 KEY_DOTA_MAP_RETREAT: keyDef(keys.KEY_X),
 KEY_DOTA_MAP_GATHER: keyDef(keys.KEY_C)}

def getForbideChangeKeyList():
    p = BigWorld.player()
    operatonMode = p.getOperationMode() if p and hasattr(p, 'getOperationMode') else None
    if operatonMode == gameglobal.ACTION_MODE:
        return ForbideChangeKeyList_Action
    elif operatonMode == gameglobal.MOUSE_MODE:
        return ForbideChangeKeyList_Mouse
    else:
        return ForbideChangeKeyList_Keyboard


ForbideChangeKeyList_Keyboard = [KEY_DOTA_LEARN_SKILL]
ForbideChangeKeyList_Mouse = [KEY_DOTA_LEARN_SKILL]
ForbideChangeKeyList_Action = [KEY_DOTA_SKILL0, KEY_DOTA_LEARN_SKILL]
DefaultHotkeyMap.update(BfDotaHotKeyPart_Default)
WanMeiHotkeyMap.update(BfDotaHotKeyPart_WanMei)
BnsHotkeyMap.update(BfDotaHotKeyPart_Action)
BfDotaSkillHotkeyList = [KEY_DOTA_SKILL0,
 KEY_DOTA_SKILL1,
 KEY_DOTA_SKILL2,
 KEY_DOTA_SKILL3,
 KEY_DOTA_SKILL4,
 KEY_DOTA_SKILL5,
 KEY_DOTA_SKILL6,
 KEY_DOTA_SKILL7]
BfDotaItemHotkeyList = [KEY_DOTA_ITEM0,
 KEY_DOTA_ITEM1,
 KEY_DOTA_ITEM2,
 KEY_DOTA_ITEM3,
 KEY_DOTA_ITEM4,
 KEY_DOTA_ITEM5]
hotkeyMap = copy.deepcopy(DefaultHotkeyMap)
HKM = hotkeyMap
SHORTCUT_KEYS = (keys.KEY_1,
 keys.KEY_2,
 keys.KEY_3,
 keys.KEY_4,
 keys.KEY_5,
 keys.KEY_6,
 keys.KEY_7,
 keys.KEY_8,
 keys.KEY_9,
 keys.KEY_0,
 keys.KEY_MINUS,
 keys.KEY_EQUALS,
 keys.KEY_F1,
 keys.KEY_F2,
 keys.KEY_F3,
 keys.KEY_F4,
 keys.KEY_F5,
 keys.KEY_F6,
 KEY_USE_ITEM1,
 KEY_USE_ITEM2,
 KEY_USE_ITEM3,
 KEY_USE_ITEM4,
 KEY_USE_ITEM5,
 KEY_USE_ITEM6,
 KEY_USE_ITEM7,
 KEY_USE_ITEM8,
 KEY_USE_ITEM9,
 KEY_USE_ITEM10,
 KEY_USE_ITEM11,
 KEY_USE_ITEM12,
 KEY_USE_ITEM13,
 KEY_USE_ITEM14,
 KEY_USE_ITEM15,
 KEY_USE_ITEM16,
 KEY_USE_ITEM17,
 KEY_USE_ITEM18,
 KEY_USE_ITEM19,
 KEY_USE_ITEM20,
 KEY_USE_ITEM21,
 KEY_USE_ITEM22,
 KEY_USE_ITEM23,
 KEY_USE_ITEM24,
 KEY_USE_ITEM25,
 KEY_USE_ITEM26,
 KEY_USE_ITEM27,
 KEY_USE_ITEM28,
 KEY_USE_ITEM29,
 KEY_USE_ITEM30,
 KEY_USE_ITEM31,
 KEY_USE_ITEM32,
 KEY_USE_ITEM33,
 KEY_USE_ITEM34,
 KEY_USE_ITEM35,
 KEY_USE_ITEM36,
 KEY_USE_ITEM37,
 KEY_USE_ITEM38,
 KEY_USE_ITEM39,
 KEY_USE_ITEM40,
 KEY_USE_ITEM41,
 KEY_USE_ITEM42,
 KEY_USE_ITEM43,
 KEY_USE_ITEM44,
 KEY_USE_ITEM45,
 KEY_USE_ITEM46,
 KEY_USE_ITEM47,
 KEY_USE_ITEM48)
SHORTCUT_ITEM_KEYS = (KEY_USE_ITEM1,
 KEY_USE_ITEM2,
 KEY_USE_ITEM3,
 KEY_USE_ITEM4,
 KEY_USE_ITEM5,
 KEY_USE_ITEM6,
 KEY_USE_ITEM7,
 KEY_USE_ITEM8,
 KEY_USE_ITEM9,
 KEY_USE_ITEM10,
 KEY_USE_ITEM11,
 KEY_USE_ITEM12,
 KEY_USE_ITEM13,
 KEY_USE_ITEM14,
 KEY_USE_ITEM15,
 KEY_USE_ITEM16,
 KEY_USE_ITEM17,
 KEY_USE_ITEM18,
 KEY_USE_ITEM19,
 KEY_USE_ITEM20,
 KEY_USE_ITEM21,
 KEY_USE_ITEM22,
 KEY_USE_ITEM23,
 KEY_USE_ITEM24,
 KEY_USE_ITEM25,
 KEY_USE_ITEM26,
 KEY_USE_ITEM27,
 KEY_USE_ITEM28,
 KEY_USE_ITEM29,
 KEY_USE_ITEM30,
 KEY_USE_ITEM31,
 KEY_USE_ITEM32,
 KEY_USE_ITEM33,
 KEY_USE_ITEM34,
 KEY_USE_ITEM35,
 KEY_USE_ITEM36,
 KEY_USE_ITEM37,
 KEY_USE_ITEM38,
 KEY_USE_ITEM39,
 KEY_USE_ITEM40,
 KEY_USE_ITEM41,
 KEY_USE_ITEM42,
 KEY_USE_ITEM43,
 KEY_USE_ITEM44,
 KEY_USE_ITEM45,
 KEY_USE_ITEM46,
 KEY_USE_ITEM47,
 KEY_USE_ITEM48)
SHORCUT_SKILL_KEYS = (keys.KEY_1,
 keys.KEY_2,
 keys.KEY_3,
 keys.KEY_4,
 keys.KEY_5,
 keys.KEY_6,
 keys.KEY_7,
 keys.KEY_8,
 keys.KEY_9,
 keys.KEY_0,
 keys.KEY_MINUS,
 keys.KEY_EQUALS,
 keys.KEY_F1,
 keys.KEY_F2,
 keys.KEY_F3,
 keys.KEY_F4,
 keys.KEY_F5,
 keys.KEY_F6)
SHORCUT_SKILL_KEYS_DOTA = (KEY_DOTA_SKILL0,
 KEY_DOTA_SKILL1,
 KEY_DOTA_SKILL2,
 KEY_DOTA_SKILL3,
 KEY_DOTA_SKILL4,
 KEY_DOTA_SKILL5,
 KEY_DOTA_SKILL6,
 KEY_DOTA_SKILL7)
SHORTCUT_ITEM_KEYS_DOTA = (KEY_DOTA_ITEM0,
 KEY_DOTA_ITEM1,
 KEY_DOTA_ITEM2,
 KEY_DOTA_ITEM3,
 KEY_DOTA_ITEM4,
 KEY_DOTA_ITEM5)
SHORTCUT_QTE_SKILL_KEYS = (KEY_QTE_SKILL1, KEY_QTE_SKILL2)

def sendHotkey(s):
    p = BigWorld.player()
    if p and p.__class__.__name__ == 'PlayerAvatar':
        p.hotkeyData[p.getOperationMode()] = s
        saveStr = zlib.compress(cPickle.dumps(p.hotkeyData, -1))
        p.base.saveHotkey(saveStr)


defaultValue = 16778240

def loadHotkey(keyData):
    global defaultValue
    global hotkeyMap
    p = BigWorld.player()
    if p and p.__class__.__name__ == 'PlayerAvatar':
        detialKeyData = keyData.get(p.getOperationMode(), {})
        if isinstance(detialKeyData, dict):
            tmpArr = []
            for key, value in detialKeyData.items():
                if key not in hotkeyMap:
                    continue
                defKey = hotkeyMap[key]
                if value == 0:
                    value = defaultValue
                defKey.restoreFromValue(value)
                if key in SHORTCUT_KEYS:
                    if defKey.key != 0:
                        tmpArr.append([key, defKey.getBrief()])
                    elif defKey.key2 != 0:
                        tmpArr.append([key, defKey.getBrief(2)])
                    else:
                        tmpArr.append([key, ''])

            tmpArr.sort(key=lambda k: k[0])
            keyArr = []
            for item in tmpArr:
                keyArr.append(item[1])

            if keyArr:
                gameglobal.rds.ui.actionbar.slotKey = keyArr


def setDefaultHotkey():
    global hotkeyMap
    global HKM
    p = BigWorld.player()
    if p and p.__class__.__name__ == 'PlayerAvatar':
        if p.getOperationMode() == gameglobal.KEYBOARD_MODE:
            hotkeyMap = copy.deepcopy(DefaultHotkeyMap)
        elif p.getOperationMode() == gameglobal.MOUSE_MODE:
            hotkeyMap = copy.deepcopy(WanMeiHotkeyMap)
        else:
            hotkeyMap = copy.deepcopy(BnsHotkeyMap)
        HKM = hotkeyMap


def checkMouseRollUp():
    key = HKM[KEY_CAMERA_NEAR]
    if key.key == keys.KEY_MOUSE_ROLLUP or key.key2 == keys.KEY_MOUSE_ROLLUP:
        return True
    return False


def checkMouseRollDown():
    key = HKM[KEY_CAMERA_FAR]
    if key.key == keys.KEY_MOUSE_ROLLDOWN or key.key2 == keys.KEY_MOUSE_ROLLDOWN:
        return True
    return False


def isCastSelfKeyDown():
    global CAST_SELF_KEY_INDEX
    if getattr(BigWorld.player(), 'keyEventMods', None) == getCastSelfKeyMod():
        return False
    else:
        idx = CAST_SELF_KEY_INDEX % 4
        key1, key2 = CAST_SELF_KEY_ARRAY[idx][1:]
        isDown = False
        if key1:
            isDown |= BigWorld.getKeyDownState(key1, 0)
        if key2:
            isDown |= BigWorld.getKeyDownState(key2, 0)
        return isDown


CAST_SELF_KEY_ARRAY = [(gameStrings.TEXT_HOTKEY_1974, keys.KEY_LALT, keys.KEY_RALT),
 (gameStrings.TEXT_HOTKEY_1974_1, keys.KEY_LCONTROL, keys.KEY_RCONTROL),
 (gameStrings.TEXT_HOTKEY_1975, keys.KEY_LSHIFT, keys.KEY_RSHIFT),
 (gameStrings.TEXT_BATTLEFIELDPROXY_1605, keys.KEY_NONE, keys.KEY_NONE)]
SHOW_CURSOR_KEY_ARRAY = [(gameStrings.TEXT_HOTKEY_1974, keys.KEY_LALT, keys.KEY_RALT), (gameStrings.TEXT_HOTKEY_1974_1, keys.KEY_LCONTROL, keys.KEY_RCONTROL), (gameStrings.TEXT_HOTKEY_1975, keys.KEY_LSHIFT, keys.KEY_RSHIFT)]
CAST_SELF_KEY_INDEX = 0

def getCastSelfKeyMod():
    idx = CAST_SELF_KEY_INDEX % 4
    key = CAST_SELF_KEY_ARRAY[idx][1]
    return getModsNum(key)


def setCastSelfKey(idx):
    global CAST_SELF_KEY_INDEX
    CAST_SELF_KEY_INDEX = idx


def setShowCursorKey(index):
    idx = index % 3
    if idx == 0:
        key = keys.KEY_LALT
        mods = 4
    elif idx == 1:
        key = keys.KEY_LCONTROL
        mods = 2
    elif idx == 2:
        key = keys.KEY_LSHIFT
        mods = 1
    HKM[KEY_CHANGE_CURSOR] = keyDef(key, 1, mods)


def getCastSelfKeyIndex():
    return CAST_SELF_KEY_INDEX
