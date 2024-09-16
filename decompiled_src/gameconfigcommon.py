#Embedded file name: /WORKSPACE/data/entities/common/gameconfigcommon.o
import time
import BigWorld
CONFIG = {}
CONFIG_CID2NAME = {}
CONFIG_NAME2CID = {}

def Bool(s):
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    raise RuntimeError('Can not convert %s to bool' % (s,))


def Int(s):
    return int(s)


def Float(s):
    return float(s)


def Str(s):
    return s


def TimeStr(ts):
    if ts:
        try:
            time.strptime(ts, '%Y.%m.%d.%H.%M.%S')
        except:
            raise RuntimeError('TimeStr format error! %s' % (ts,))

    return ts


def convertDataWithCid(data):
    r = {}
    for cid, v in data.iteritems():
        r[CONFIG_CID2NAME.get(cid, cid)] = v

    return r


def config(convFunc, default, desc, clientConfig = False, cid = 0):

    def _config(func):
        global CONFIG
        name = func.__name__
        if name in CONFIG:
            raise RuntimeError('Config %s duplicated!' % (name,))
        if type(default) is not str:
            raise RuntimeError('Config %s default must be string!' % (name,))
        if clientConfig:
            if not cid:
                raise RuntimeError('Config %s for client must be assigned with cid!' % (name,))
            if CONFIG_CID2NAME.has_key(cid) and CONFIG_CID2NAME.get(cid) != name:
                raise RuntimeError('Duplicated cid %d for name %s and %s!' % (cid, name, CONFIG_CID2NAME.get(cid)))
            if CONFIG_NAME2CID.has_key(name) and CONFIG_NAME2CID.get(name) != cid:
                raise RuntimeError('Duplicated name %s for cid %s and %s!' % (name, cid, CONFIG_NAME2CID.get(name)))
        try:
            defaultv = convFunc(default)
        except:
            raise RuntimeError('Config %s default value error!' % (name,))

        if clientConfig:
            CONFIG_CID2NAME[cid] = name
            CONFIG_NAME2CID[name] = cid
        if BigWorld.component == 'client':
            CONFIG[name] = defaultv
        else:
            CONFIG[name.lower()] = (name,
             convFunc,
             default,
             defaultv,
             desc,
             clientConfig)

        def _func():
            if BigWorld.component == 'client':
                if clientConfig:
                    import gameglobal
                    return gameglobal.rds.configData.get(name, False)
            else:
                return BigWorld.globalData['CONFIG'][name]

        if BigWorld.component in ('base', 'cell'):
            import gameconfig
            setattr(gameconfig, name, _func)
        return _func

    return _config


if BigWorld.component in ('base', 'cell'):
    import gameconst

    @config(Int, str(gameconst.ONLINE_MASS_MAX), 'ϵͳ�����������')
    def maxOnline():
        pass


@config(Int, '0', '�ͻ��˵�¼�汾������')
def clientVersionThreshold():
    pass


@config(Bool, 'false', '�Ƿ����ͻ��˵�¼�汾�ż��')
def clientVersionCheck():
    pass


@config(Int, str(int(time.time())), '��������һ������ʱ��', True, cid=1)
def serverOpenTime():
    pass


@config(Int, '0', '������ֻʹ��ָ����ͼ')
def disableArenaMap():
    pass


@config(Int, '0', '����3V3��������������')
def arena3v3Num():
    pass


@config(Int, '0', '����ս����������')
def bfRecycleNum():
    pass


@config(Int, '0', '����ս���ر�ʱ��')
def bfDurationTime():
    pass


@config(Int, '0', '���þ���������ʱ��')
def arenaDurationTime():
    pass


@config(Int, '0', '����ս����������')
def bfMaxNum():
    pass


@config(Int, '0', '�����ӳɶ�����')
def groupMatchNum():
    pass


@config(Int, '120', 'entityController������ޱ�����ֵ')
def entityControllerLimitCount():
    pass


@config(Bool, 'true', '�Ƿ���cc', True, cid=2)
def isCCVersion():
    pass


@config(Int, '800', '��ս���ݵ�������������')
def clanWarFortMaxPlayer():
    pass


@config(Int, '3500', '��ս��������������')
def clanWarWarningPlayerNum():
    pass


@config(Bool, 'true', '�Ƿ�����Ч�ƺ�', True, cid=3)
def enableEffectTitle():
    pass


@config(Bool, 'true', '�Ƿ�������CPU���Ż��ֶ�')
def enableReduceCPUOverHead():
    pass


@config(Bool, 'false', '�Ƿ���װ��ι��', True, cid=4)
def enableFeedEquip():
    pass


@config(Bool, 'true', '�Ƿ���avatar�����ͻ��˽���', True, cid=5)
def enableMFClientCalc():
    pass


@config(Bool, 'true', '�Ƿ�����ͨ���ܵĿͻ��˽���', True, cid=6)
def enableSkillClientCalc():
    pass


@config(Bool, 'false', '�������������ܾ��߿ͻ��˽�����߼�(�н�����ʱ��ֱ�Ӻ�����ʱ)', True, cid=7)
def forceSkillClientCalc():
    pass


@config(Bool, 'true', '�Ƿ��Զ�ʹ��qte����', True, cid=8)
def enableAutoUseQteSkills():
    pass


@config(Bool, 'true', '�Ƿ񾺼�����������̭���̶�����')
def enableArenaPlayoffsFinalHardGroup():
    pass


@config(Bool, 'false', '�Ƿ����þ������̶�30s׼��ʱ��')
def enableArenaPlayoffsQuickReady():
    pass


@config(Bool, 'true', '�Ƿ�ȷ��ս����SpaceNo�����ٺ�pop')
def enableBFSpaceNoPopOrder():
    pass


@config(Bool, 'false', '�Ƿ������ռ��')
def enableRiskControl():
    pass


@config(Bool, 'false', '�Ƿ���Ͷ�ż�ر�����popo')
def enableRiskControlProcess():
    pass


@config(Bool, 'true', '�Ƿ���ȫ��Ͷ������')
def enableGlobalGenerationControl():
    pass


@config(Float, '1.0', '�����شﵽ����ʱ��ֱ�ӽ�ֹ����ͷż���')
def useSkillLoadLimit():
    pass


@config(Int, '0', 'ǿ�����÷������ĸ��صȼ�')
def forceLoadLv():
    pass


@config(Bool, 'false', '�������Ƿ�Ҳ��loadLv��Ӱ��')
def enableGlobalLoadCheck():
    pass


@config(Bool, 'true', '�Ƿ�����������')
def enablePhoneMessageSend():
    pass


@config(Bool, 'true', '�Ƿ��������ȼ�����')
def enableFameBonus():
    pass


@config(Bool, 'true', '�Ƿ���������������')
def enableFameLvUpBonus():
    pass


@config(Bool, 'true', '�Ƿ��������䱦��', True, cid=9)
def enableGuildShop():
    pass


@config(Bool, 'true', '�Ƿ�������Ѱ��')
def enableGuildMatch():
    pass


@config(Bool, 'true', '�Ƿ��������װ���;ö�����', True, cid=10)
def enableLifeDura():
    pass


@config(Bool, 'false', '�Ƿ�ر��̳�', True, cid=11)
def offMall():
    pass


@config(Bool, 'false', '�Ƿ�ر�Ԫ����ֵ', True, cid=12)
def offCharge():
    pass


@config(Bool, 'false', '�Ƿ�رճ�ֵ����', True, cid=13)
def offCoinRefund():
    pass


@config(Bool, 'false', '�Ƿ�ر�Ԫ������', True, cid=14)
def offCoinMarket():
    pass


@config(Bool, 'true', '�Ƿ���ʧ������', True, cid=15)
def enableShiHunRepair():
    pass


@config(Bool, 'true', '�Ƿ��������Զ���ͷ��', True, cid=16)
def enableCustomRadio():
    pass


@config(Bool, 'false', '�Ƿ�رհ�ȫģʽ', True, cid=17)
def offSafeMode():
    pass


@config(Bool, 'false', '�Ƿ�������', True, cid=18)
def enableYixin():
    pass


@config(Bool, 'false', '�Ƿ������ֽ�������', True, cid=19)
def enableAchieveScore():
    pass


@config(Bool, 'false', '�Ƿ������ʹ�Ŀ��/�����ֲ�', True, cid=20)
def enableGuideGoal():
    pass


@config(Bool, 'true', '�Ƿ���������ģʽ', True, cid=21)
def enableArenaMode():
    pass


@config(Bool, 'true', '�Ƿ�������������', True, cid=22)
def enableArenaApply():
    pass


@config(Bool, 'true', '�Ƿ�PVP��������', True, cid=23)
def enableDuelLimit():
    pass


@config(Bool, 'true', '�Ƿ�������ģʽ', True, cid=24)
def enableTradeMode():
    pass


@config(Bool, 'true', '�Ƿ�������Զ��幫��ս�칦��', True, cid=25)
def enableUserDefGuildCrest():
    pass


@config(Bool, 'true', '�Ƿ������繦��', True, cid=26)
def enableJingJie():
    pass


@config(Bool, 'true', '�Ƿ����Զ�ͻ�ƾ��繦��', True, cid=27)
def enableAutoBreakJingJie():
    pass


@config(Bool, 'true', '�Ƿ����ûع���ǩ', True, cid=28)
def enableBuyBackTab():
    pass


@config(Bool, 'true', '�Ƿ������������Ϊ����ʾ', True, cid=29)
def enableNoDiaplayQuests():
    pass


@config(Bool, 'true', '�Ƿ�������', True, cid=30)
def enableGuildActivity():
    pass


@config(Bool, 'true', '�Ƿ���NOS����', True, cid=31)
def enableNOSService():
    pass


@config(Bool, 'true', '�Ƿ�����ս����', True, cid=32)
def enableAirSkill():
    pass


@config(Bool, 'false', '�Ƿ�������е�¼����', True, cid=33)
def enableLoginCityFilter():
    pass


@config(Bool, 'false', '�Ƿ�����������������г�', True, cid=34)
def enableKuilingOrg():
    pass


@config(Bool, 'true', 'ͻ�ƾ���ʱ�Ƿ���Ԫ��', True, cid=35)
def enableYSCheck():
    pass


@config(Bool, 'true', '�Ƿ���������幫�Ὠ��Tabҳ', True, cid=36)
def enableGuildBuildingTab():
    pass


@config(Bool, 'false', '�Ƿ���������幫�Ὠ��Զ��ʹ��', True, cid=37)
def enableRemoteGuildBuilding():
    pass


@config(Bool, 'true', '�Ƿ���VIP����', True, cid=38)
def enableVip():
    pass


@config(Bool, 'true', '�Ƿ�������ʵ����Ŀ����', False)
def enableFubenAlert():
    pass


@config(Bool, 'true', '�Ƿ����������ظ��ӳ�ƥ��', False)
def enableArenaDupDelay():
    pass


@config(Bool, 'true', '�Ƿ���AvatarPeek�Ĵ���', False)
def enableAvatarPeekProxy():
    pass


@config(Bool, 'false', '�Ƿ�֧�ֹ�����Ʒ����', True, cid=39)
def enableValuableTrade():
    pass


@config(Bool, 'true', '�Ƿ������ȡ˫������', True, cid=40)
def enableExpBonus():
    pass


@config(Bool, 'false', '�Ƿ����ι�������Ƭ', True, cid=41)
def enableAddRuneEquipExp():
    pass


@config(Bool, 'false', '�Ƿ����ϴ�������Ƭ', True, cid=42)
def enableRuneEquipXiLian():
    pass


@config(Bool, 'false', '�Ƿ��������������Ƭ', True, cid=43)
def enableReforgRune():
    pass


@config(Bool, 'false', '�Ƿ�������������Ƭ', True, cid=44)
def enableRuneEquipOrderUp():
    pass


@config(Bool, 'true', '�Ƿ�����ϵͳ:Hierogram or Rune', True, cid=45)
def enableHierogramOrRune():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�������ϵͳ:Hierogram', True, cid=46)
def enableHierogram():
    pass


@config(Bool, 'false', '�Ƿ�򿪵�¼ʱ������Ʒ�ظ�uuid�Ĺ���(smj)')
def enableFindDuplicatedUUID():
    pass


@config(Bool, 'false', '�Ƿ��������Ʒ�ظ�uuid�Ĺ��ܣ���ҪenableFindDuplicatedUUID��(smj)')
def enableModifyDuplicatedUUID():
    pass


@config(Bool, 'false', '�Ƿ��APP����ֶ�����', True, cid=47)
def enableAppAlbumManualVol():
    pass


@config(Bool, 'false', '�Ƿ������Ƶ��', True, cid=48)
def enableSecretChannel():
    pass


@config(Bool, 'true', '�Ƿ�򿪻��ڸ������ĵ��¸��ؾ�������Ż�', True, cid=49)
def enableNewBalanceBarycenter():
    pass


@config(Bool, 'false', '�Ƿ�ȫ��ͼ�������ڸ������ĵ��¸��ؾ�������Ż�', False)
def enableAllNewBalanceBarycenter():
    pass


@config(Bool, 'false', '�Ƿ�򿪸߸���ʱ���Զ�PythonProfile', False)
def enableAutoPythonProfileHighLoad():
    pass


@config(Bool, 'false', '�Ƿ��states�·��ķ��������Ż�', False)
def enablePubSubStates():
    pass


@config(Bool, 'true', '�Ƿ�򿪿ͻ��˷��������б��ά��', True, cid=691)
def enablePubSubOperationClient():
    pass


@config(Bool, 'false', '�Ƿ�򿪷���˷��������б��ά��', False)
def enablePubSubOperation():
    pass


@config(Bool, 'false', '�Ƿ��δ����������ѽ���ÿ���޶�')
def enableLimitTeenCoinConsume():
    pass


@config(Bool, 'true', '�Ƿ���APP��Ϣ���͹���', True, cid=50)
def enableAppMsg():
    pass


@config(Bool, 'true', '������Ϣ���Ƿ��͵�popo')
def criticalMsgToPopo():
    pass


@config(Bool, 'true', '�ͻ��˵��쳣��Ϣ���Ƿ��͵�popo')
def clientExceptionToPopo():
    pass


@config(Bool, 'false', '�Ƿ�����ֻ��ͬʱ����һ����ɫ', True, cid=51)
def oneCharacterLimit():
    pass


@config(Bool, 'false', '�Ƿ���״̬��һ���Լ��')
def stateConsistentCheck():
    pass


@config(Bool, 'false', '�Ƿ�����Դ��ȡ�����ռ�', True, cid=52)
def enableMiniClient():
    pass


@config(Bool, 'true', '�Ƿ����ڱ�����', True, cid=53)
def enableWabao():
    pass


@config(Bool, 'true', '�Ƿ��鼤���˺Ŷ�Ӧ�ķ�����ID')
def checkActivatedAccountServerId():
    pass


@config(Bool, 'true', '�Ƿ���TopSpeed���')
def enableTopSpeedCheck():
    pass


@config(Bool, 'false', '�Ƿ�����������ͼƬ', True, cid=54)
def enableYixinImage():
    pass


@config(Bool, 'true', '�Ƿ�����������״̬�޸�', True, cid=55)
def enableQuestRepair():
    pass


@config(Bool, 'false', '�Ƿ������¹���', True, cid=56)
def enableInviteMate():
    pass


@config(Bool, 'true', '�Ƿ��������˹���', True, cid=57)
def enableFriendInvite():
    pass


@config(Bool, 'false', '�Ƿ������뵥�˶���Ĺ���', True, cid=58)
def enableIgnoreTgtGroup():
    pass


@config(Bool, 'false', '�˺ŵ�½ʱ�Ƿ��鼤����֤')
def checkAccountLoginPermission():
    pass


@config(Bool, 'false', '�Ƿ����������ߵ����¹���', False)
def enableInviteMateIter():
    pass


@config(Bool, 'true', '�Ƿ������²�������')
def enableInviteAccountBanCheck():
    pass


@config(Bool, 'true', '�Ƿ�ʹ��ƽ��ս��ְҵƥ��')
def enableBFBalanceSchool():
    pass


@config(Bool, 'false', '�Ƿ�ʹ��ս��ƥ��log')
def enableBFMatchLog():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�ܾ�������������')
def enableArenaReBalance():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�ܾ�������������log')
def enableArenaReBalanceLog():
    pass


@config(Bool, 'true', '�������ŷ���˻ز������Ϣ')
def enableYixinQuery():
    pass


@config(Bool, 'false', '�Ƿ�������״̬��double check', True, cid=59)
def enableRelationCheck():
    pass


@config(Bool, 'false', '�Ƿ������ϵͳ', True, cid=60)
def enablePartner():
    pass


@config(Bool, 'true', '�Ƿ�����canInsertItemsEx', True, cid=61)
def enableCanInsertItemsEx():
    pass


@config(Bool, 'true', '�Ƿ����ó�ս���� ͳ��', True, cid=62)
def enableClanWarStats():
    pass


@config(Bool, 'true', '�Ƿ������̳���Ʒ����', True, cid=63)
def enableMallItemRenewal():
    pass


@config(Bool, 'true', '�Ƿ��������ʹ����Ʒ')
def enableBatchUseItem():
    pass


@config(Bool, 'true', '�Ƿ����ô���CD���')
def enableTeleportCheck():
    pass


@config(Bool, 'true', '�Ƿ�����ͨ��', True, cid=64)
def enableInventoryLock():
    pass


@config(Bool, 'true', '�Ƿ�������ʶ��', True, cid=65)
def enableSemantics():
    pass


@config(Bool, 'true', '�Ƿ���������ʽ', True, cid=66)
def enableContract():
    pass


@config(Bool, 'false', '�Ƿ����������꽱��', True, cid=67)
def enableIntimacyYearlyReward():
    pass


@config(Bool, 'false', '�Ƿ����������꽱������', True, cid=68)
def enableIntimacyYearlyCompensate():
    pass


@config(Bool, 'true', '�Ƿ�������֮��', True, cid=69)
def enableIntimacyRegister():
    pass


@config(Bool, 'false', '�Ƿ�������֮�Ľ�����ȡ', False)
def enableIntimacyRegisterReward():
    pass


@config(Bool, 'true', '�Ƿ����÷���˵ĸ��ؼ�¼')
def enableServerLoadCheck():
    pass


@config(Bool, 'true', '�Ƿ����÷���������Mongo��־', False)
def enableServerLoadDataMongo():
    pass


@config(Float, '0.95', '����˿��ټ�¼�ĸ�����ֵ')
def serverLoadCheckThreshold():
    pass


@config(Float, '5.0', 'ͬ��ս�������λ�õ�ʱ����', True, cid=70)
def battlefieldPosRefreshInterval():
    pass


@config(Bool, 'false', '�Ƿ�����ҵϵͳ', True, cid=71)
def enableApprentice():
    pass


@config(Bool, 'true', '�Ƿ�������ҵϵͳ', True, cid=72)
def enableNewApprentice():
    pass


@config(Bool, 'false', '�Ƿ���������', True, cid=73)
def enableAntiIndulgence():
    pass


@config(Bool, 'false', '�Ƿ��������Ե�¼����')
def enableAntiIndulgenceLogin():
    pass


@config(Bool, 'false', '�Ƿ��������Ե�¼����(�ͻ���)', True, cid=74)
def enableAntiIndulgenceLoginClient():
    pass


@config(Bool, 'true', '������뺼��NOS���ƽ̨')
def enableHYNOSExamineAPI():
    pass


@config(Bool, 'true', '�Ƿ���Ⱥս���㲥avatarConfig���Ż��ֶ�')
def enablePubAvatarConfig():
    pass


@config(Bool, 'true', '�Ƿ���Ⱥս���㲥aspect���Ż��ֶ�')
def enablePubAspect():
    pass


@config(Bool, 'true', '�Ƿ��ÿ�������Լ���entity��������')
def enableEntityWarning():
    pass


@config(Bool, 'false', '�Ƿ�׷��Avatar��Cell����ӡ��־')
def enableTraceCellSwitch():
    pass


@config(Bool, 'true', '�Ƿ���Ԫ������', True, cid=75)
def enableCoinConsign():
    pass


@config(Bool, 'false', '�Ƿ��������Ŀ�������й���', True, cid=76)
def enableCrossConsign():
    pass


@config(Bool, 'true', '�Ƿ�������������ķ��ķ���', True, cid=77)
def enableCrossConsignCenter():
    pass


@config(Bool, 'true', '��Ӫ������ҷ����µĿ����������', True, cid=78)
def enableNewCrossConsignReq():
    pass


@config(Bool, 'false', '��������и߼�����', True, cid=79)
def enableCrossConsignFilterSearch():
    pass


@config(Bool, 'true', '�Ƿ����޽�֮��ս��', True, cid=80)
def enableFortBf():
    pass


@config(Bool, 'false', '�Ƿ�������ս��', True, cid=81)
def enableHookBf():
    pass


@config(Bool, 'true', '�Ƿ���ս�������ӳ�ƥ��', False)
def enableGroupApplyDelayMatch():
    pass


@config(Bool, 'false', '�Ƿ���npc����Ż�', True, cid=82)
def enableRobModel():
    pass


@config(Bool, 'false', '�Ƿ���npc�����ǹ��Ż�', True, cid=83)
def enableRobAvatarModel():
    pass


@config(Bool, 'true', '�Ƿ���ccbox', True, cid=84)
def enableCCBox():
    pass


@config(Bool, 'true', '�Ƿ�����ս��', True, cid=85)
def enableFlagBf():
    pass


@config(Bool, 'false', '�Ƿ���˫��ս��', True, cid=86)
def enableHuntBf():
    pass


@config(Bool, 'false', '�Ƿ���dotaս��', True, cid=87)
def enableDotaBf():
    pass


@config(Bool, 'true', '�Ƿ�ʹ��ս����������ʱ����', True, cid=88)
def enableDuelTimeCheck():
    pass


@config(Bool, 'true', '�Ƿ����⻷������������')
def enableAuraCalcNumConfig():
    pass


@config(Bool, 'false', '�Ƿ��¼�û���ս�����ݹ鵵', True, cid=89)
def enableRecordBattleFieldData():
    pass


@config(Bool, 'true', '�Ƿ�رչ������ڵ��ߵ�ʱ����ʾ', True, cid=90)
def enableCommonResumeHide():
    pass


@config(Bool, 'true', '�Ƿ񿪷��¹��Ṧ��', True, cid=91)
def enableNewGuild():
    pass


@config(Bool, 'true', '�Ƿ�������Բ������', True, cid=92)
def enableGuildRoundTable():
    pass


@config(Bool, 'false', '�Ƿ񿪷�ѡ�˽��涥�Ź���', True, cid=93)
def enableLoginPassedPhaseRelog():
    pass


@config(Bool, 'true', '�Ƿ񿪷ų�ս�ڼ�����֮ŭ��buff����')
def enableClanWarCalcMultiply():
    pass


@config(Bool, 'true', '�Ƿ񿪷��µ���ľ�幱�׷�ͳ�ƹ���')
def enableNewYmfScore():
    pass


@config(Bool, 'true', '����NPC��Ʒ���չ���', True, cid=94)
def enableItemRecall():
    pass


@config(Bool, 'false', '�Ƿ��������ӳ�ͳ��', False)
def sendLatencyInfo():
    pass


@config(Bool, 'true', '�Ƿ����ر���', True, cid=95)
def enableCBG():
    pass


@config(Bool, 'false', '�Ƿ����ر��������˺���ת', True, cid=96)
def enableCBGOpenURLSkip():
    pass


@config(Bool, 'false', '�Ƿ����ر����ɫ����', True, cid=695)
def enableCBGRole():
    pass


@config(Bool, 'true', '�������׺�����')
def enableBlackListCheck():
    pass


@config(Bool, 'true', '��������������')
def enableBlackMachineCheck():
    pass


@config(Bool, 'true', '����������ɫ', True, cid=97)
def enableCreateRole():
    pass


@config(Bool, 'true', '����roll��ļ��')
def enableRollCheck():
    pass


@config(Bool, 'true', '�Ƿ����ƴ����߰�', True, cid=98)
def enableYunchuiTopRank():
    pass


@config(Bool, 'true', '�Ƿ����������а�', True, cid=99)
def enableGroupFubenRank():
    pass


@config(Bool, 'True', '�Ƿ�������������', True, cid=100)
def enableNewLifeSkill():
    pass


@config(Bool, 'true', '�Ƿ�����Ʒlogȫ�����ӹ㲥', False)
def enableItemLogBroadcast():
    pass


@config(Bool, 'true', '�Ƿ��¼���֧���ͻ���log', True, cid=101)
def enableEasyPayLog():
    pass


@config(Bool, 'true', '�Ƿ�֧��֧������ֵ', True, cid=102)
def enableAlipay():
    pass


@config(Bool, 'true', '�Ƿ���ս���콵���', True, cid=103)
def enableTJL():
    pass


@config(Bool, 'true', '�����ٶȹ���', True, cid=104)
def enableRideWingShareSpeed():
    pass


@config(Bool, 'true', '�Ƿ�֧�ְ��ֻ��������', True, cid=105)
def enableBindingProperty():
    pass


@config(Bool, 'true', '�Ƿ�ʹ��ȷ�Ͼ�λ', True, cid=106)
def enableGroupPrepare():
    pass


@config(Bool, 'true', '�Ƿ�֧�ֿ��ٿ��̳Ǳ���')
def enableAutoOpenMallBoxItem():
    pass


@config(Bool, 'true', '�Ƿ����������޵Ĺ���')
def enableMaxQueueCheck():
    pass


@config(Bool, 'true', '�Ƿ�����ħϵͳ', True, cid=107)
def enableQumo():
    pass


@config(Bool, 'true', '�Ƿ񹫻���ս', True, cid=108)
def enableGuildChallenge():
    pass


@config(Bool, 'true', '�Ƿ���������Ǯ/����Ʒ����', False)
def enableDawdlerReward():
    pass


@config(Bool, 'true', '�Ƿ�decode error�쳣���', False)
def enableCheckDecodeError():
    pass


@config(Bool, 'false', '�Ƿ���console�д�ӡmongo��־', False)
def enableConsoleLog():
    pass


@config(Bool, 'true', '�Ƿ������׼��', True, cid=109)
def enableTradeWatch():
    pass


@config(Bool, 'true', '�Ƿ�����Ļ', True, cid=110)
def enableBarrage():
    pass


@config(Bool, 'true', '�Ƿ������ܶȹ���', True, cid=111)
def enableIntimacy():
    pass


@config(Bool, 'true', '�Ƿ������ܶȳɾʹ�������', True, cid=112)
def enableIntimacyTrigger():
    pass


@config(Int, '0', '������Ĭ�ϼ��ص�cell����', False)
def defaultBigWorldMinCellNum():
    pass


@config(Bool, 'false', '�Ƿ����ͻ���������־', True, cid=113)
def enableLogClientPerformance():
    pass


@config(Bool, 'false', '�Ƿ���ӳ�ʱ����uu', True, cid=114)
def enablePushUU():
    pass


@config(Bool, 'true', '�Ƿ��������Ʊҹ���', True, cid=115)
def enableGuildPayCash():
    pass


@config(Bool, 'true', '�Ƿ���������ҹ���', True, cid=116)
def enableGuildPayCoin():
    pass


@config(Bool, 'false', '�������ı�ʯ�Ƿ���Ҫ���ù���', True, cid=117)
def enableGemOwner():
    pass


@config(Bool, 'true', '�Ƿ�����VIP������Ȩ', True, cid=118)
def enableVipBar():
    pass


@config(Bool, 'true', '�Ƿ�����Ըϵͳ', True, cid=119)
def enableWish():
    pass


@config(Bool, 'true', '�Ƿ��proxyDist', True, cid=120)
def enableProxyDist():
    pass


@config(Bool, 'true', '����ж�ģʽ', True, cid=121)
def enableGuildEnemy():
    pass


@config(Bool, 'true', '�����Ŷ���Ůzhibo', True, cid=122)
def enableCCliveBroadcast():
    pass


@config(Bool, 'true', '�Ƿ����ɴ��ƶ�ƽ̨ǰ�ü��', False)
def enableMPMutex():
    pass


@config(Bool, 'true', '�Ƿ�����AdminStub����', False)
def enableSendToAdmin():
    pass


@config(Bool, 'true', '�Ƿ������������', True, cid=123)
def enableCrossServerArena():
    pass


@config(Bool, 'false', '�Ƿ��ǽ����ṩԤԼ�ķ�����', True, cid=124)
def isReservationOnlyServer():
    pass


@config(Bool, 'true', '�Ƿ�������������', True, cid=125)
def enableServerProgress():
    pass


@config(Bool, 'true', '�Ƿ������ȡ���кż����', True, cid=126)
def enableApplyActivationCodeReward():
    pass


@config(Bool, 'false', '�Ƿ�һ������Ż�ȯ', True, cid=127)
def enableKaola():
    pass


@config(Bool, 'true', '�Ƿ񿪷Ų��ϰ�', True, cid=128)
def enableMaterialBag():
    pass


@config(Bool, 'true', '�Ƿ����Զ���IME', True, cid=129)
def enableCustomIme():
    pass


@config(Bool, 'true', '�Ƿ���������˫�ĵ�����', True, cid=130)
def enableGuildWSPractice():
    pass


@config(Bool, 'false', '�Ƿ���������˫��������', True, cid=131)
def enableGuildWSDaoheng():
    pass


@config(Bool, 'false', '�Ƿ�����˫����෽��', True, cid=132)
def enableWSSchemes():
    pass


@config(Bool, 'true', '�Ƿ�����˫����෽����ݼ�', True, cid=133)
def enableWSSchemeHotKeys():
    pass


@config(Bool, 'false', '�Ƿ����������͸�����ֵƽ��ģʽ', True, cid=134)
def enableRebalance():
    pass


@config(Bool, 'false', '�Ƿ����ж���Ʒ����', True, cid=135)
def enableCalcRarityMiracle():
    pass


@config(Bool, 'false', '�Ƿ�Ҫ�������������ͬ����App��API', True, cid=136)
def enableSyncCrossConsignToApp():
    pass


@config(Bool, 'true', '�Ƿ����α�Ŷ�', False)
def enableReCalcQueuePlace():
    pass


@config(Bool, 'true', '�Ƿ���֪ͨ', False)
def enableServerLoadedNotify():
    pass


@config(Int, '0', '����������ƫ����', False)
def serverLoadedOffset():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�ÿ����������������', False)
def enableCrossArenaBasic():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�ð�ʱ�仺���log', False)
def enableDeadlineCachedLog():
    pass


@config(Int, str(5 * 60), 'log����ʱ��', False)
def deadlineCachedLogExpireTime():
    pass


@config(Bool, 'false', '�Ƿ����ɵ���������', True, cid=137)
def oldLilian():
    pass


@config(Bool, 'true', '�Ƿ����µ���������', True, cid=138)
def newLilian():
    pass


@config(Bool, 'true', '�Ƿ���߱�����', True, cid=139)
def enableShishenCascade():
    pass


@config(Bool, 'true', '�Ƿ���ͬ���������', True, cid=140)
def enableNepSync():
    pass


@config(Bool, 'true', '�Ƿ����������ȼ����ӳ�', True, cid=141)
def enableServerExpAdd():
    pass


@config(Bool, 'false', '�Ƿ�����ӡ�ͻ��˵�log��Ϣ������gm_client_info�� ', True, cid=142)
def enablePrintClientLog():
    pass


@config(Bool, 'false', '�Ƿ����ƹ�Աϵͳ', True, cid=143)
def enableGsSystem():
    pass


@config(Bool, 'false', '�Ƿ����·�����', True, cid=144)
def enableOpenServerBonus():
    pass


@config(Bool, 'true', '�Ƿ����·�����������ƿ����', True, cid=145)
def enableOpenServerBonusVpStorage():
    pass


@config(Bool, 'false', '�Ƿ���UI��GC����', True, cid=146)
def enableUIGCControl():
    pass


@config(Bool, 'false', '����cc�Ը���', True, cid=147)
def enableCCSelfUpdate():
    pass


@config(Bool, 'true', '�ص��Ƽ�ҳδ�����Ŀǿ����', True, cid=148)
def enableIncompleteItemsNotify():
    pass


@config(Bool, 'true', '�Ƿ���VIP 7�������������ֵ��', True, cid=149)
def enableTrialVipGift():
    pass


@config(Bool, 'true', '�Ƿ�����������Ʒʹ��logmerge')
def enableContinuousItemLogMerge():
    pass


@config(Bool, 'true', '�Ƿ����ع������Զ���ӹ���', True, cid=150)
def enableDiGongQuickJoinGroup():
    pass


@config(Bool, 'true', '�Ƿ�����ս�����Զ���ӹ���', True, cid=151)
def enableWorldWarQuickJoinGroup():
    pass


@config(Bool, 'false', '�Ƿ���cc��˸', True, cid=152)
def enableCCShine():
    pass


@config(Bool, 'false', '�Ƿ�����λ������ȡ', True, cid=153)
def enableDuanWeiAward():
    pass


@config(Bool, 'false', '�Ƿ���������ս��ս����', True, cid=154)
def enableRejectGuildChallenge():
    pass


@config(Bool, 'true', '����������־�ϲ�')
def enableFameLogMerge():
    pass


@config(Bool, 'false', '��������������֪ͨ', True, cid=155)
def enableNotifyBuildIntimacyCnt():
    pass


@config(Bool, 'true', '���������������ȡ')
def enableActivityReward():
    pass


@config(Bool, 'true', '����NOS�����CDN����', True, cid=156)
def enableNOSCDNDeploy():
    pass


@config(Bool, 'false', '�Ƿ���Ϸ�˳�����', True, cid=157)
def enableForceOpenUrl():
    pass


@config(Bool, 'true', '�Ƿ�̬�޸���ħ�ȼ�')
def enableQumoRepair():
    pass


@config(Bool, 'true', '����֮·��Ҫ��ǿtabҳ', True, cid=158)
def enablePlayRecommStrongerTab():
    pass


@config(Bool, 'true', '�Ƿ������ά������', True, cid=159)
def enableGuildRewardSalary():
    pass


@config(Bool, 'true', '�Ƿ���������Ϊ', True, cid=160)
def enableExpXiuWei():
    pass


@config(Bool, 'true', '�Ƿ������ս��', True, cid=161)
def enableCrossServerBF():
    pass


@config(Bool, 'true', '�Ƿ����������', True, cid=162)
def enableCrossServerLaba():
    pass


@config(Bool, 'false', '�Ƿ��������ս����', True, cid=163)
def enableWorldWarLaba():
    pass


@config(Bool, 'true', '���������̵귵��ʵ��')
def enableCompositeShopReturnInstance():
    pass


@config(Bool, 'false', '�Ƿ�����Ԫ�飩����', True, cid=164)
def enableYuanLing():
    pass


@config(Bool, 'false', '�Ƿ�������ͷ��', True, cid=165)
def enableHideFashionHead():
    pass


@config(Bool, 'false', '�Ƿ����������Ի', True, cid=166)
def enableGuildActivityHunt():
    pass


@config(Bool, 'false', '�Ƿ�����Ʒ�ظ�UUIDɨ��')
def enableItemScan():
    pass


@config(Bool, 'true', '�Ƿ����µ����а�', True, cid=167)
def enableNewArenaRank():
    pass


@config(Bool, 'true', 'һ��ѧ�������Ṧ', True, cid=168)
def learnAllQingGongIgnoreLv():
    pass


@config(Bool, 'false', '����������ƶ���λ�õļ�¼', True, cid=169)
def recordMoveToPosition():
    pass


@config(Bool, 'true', '���������Դ', True, cid=170)
def enableGuildLight():
    pass


@config(Int, '17', '�����̳ǿ����ȼ�, �ܿ��� offMall����', True, cid=171)
def mallUseableMinLv():
    pass


@config(Int, '100', 'MDB�Ŀ�������', True, cid=172)
def memoryDBRate():
    pass


@config(Bool, 'false', '�Ƿ�����deep�������', True, cid=173)
def enableAvatarPeekAnother():
    pass


@config(Bool, 'false', '�Ƿ����ת��', True, cid=174)
def enableMigrateOut():
    pass


@config(Bool, 'false', '��������������Ƿ����ת���˷�', True, cid=175)
def enableMigrateIn():
    pass


@config(Bool, 'false', '�Ƿ��������ת��', True, cid=176)
def enableFreeMigrate():
    pass


@config(Bool, 'true', 'װ��ǰ׺�����û�', True, cid=177)
def enableExchangeEquipPreProp():
    pass


@config(Bool, 'true', 'װ������ת��', True, cid=178)
def enableTransferEquipProps():
    pass


@config(Bool, 'false', '�Ƿ���GMָ��㲥�Ż�')
def enableGmCommandBroadCastOptimization():
    pass


@config(Bool, 'true', '�Ƿ������̹���', True, cid=179)
def enableGuildBusiness():
    pass


@config(Bool, 'true', '�Ƿ�������ί�й���', True, cid=180)
def enableGuildDgtBusiness():
    pass


@config(Bool, 'true', 'ȫ�����¼�', True, cid=181)
def enableFullScreenFittingRoom():
    pass


@config(Bool, 'true', '�Ƿ���ʦͽ�Ƽ�', True, cid=182)
def enableApprenticePool():
    pass


@config(Bool, 'true', '�Ƿ�����Ʒת��', True, cid=183)
def enableBindItemConvert():
    pass


@config(Bool, 'true', '�Ƿ���ս��˫�˱���', True, cid=184)
def enableBFDoubleApply():
    pass


@config(Bool, 'true', '�Ƿ������������', True, cid=185)
def enableCameraShare():
    pass


@config(Bool, 'true', '�Ƿ�����ɫץ�Ĺ��ܹ���', True, cid=186)
def enableCharSnapshot():
    pass


@config(Bool, 'true', '�Ƿ���zoomIn', True, cid=187)
def enableCameraZoomIn():
    pass


@config(Bool, 'true', '�Ƿ����������', False)
def enableWorldPuzzle():
    pass


@config(Bool, 'true', '�Ƿ��ڶ���ģʽ׼��״̬�´�͸����UI', True, cid=188)
def disableUIInActionMode():
    pass


@config(Str, '', '��Щ�����������Ҫ����,Ӣ�Ķ��ŷָ�', True, cid=189)
def hideActivityRewardTypes():
    pass


@config(Str, '0,0', '˫��ս���Ŀ�������,2����Ӫ,�÷ֺŸ���,ǰ���Ϊ������', True, cid=190)
def bfHuntSideNum():
    pass


@config(Str, '', '���ս��Ӣ�ۺ�����,��Ӣ�Ķ��Ÿ���', True, cid=191)
def bfDotaRoleBlackList():
    pass


@config(Bool, 'true', '�����뿪������ִ�������ʱ�����ĸ�����Ʒ')
def enableRemoveFbTempBagItems():
    pass


@config(Bool, 'true', '�����˫������', True, cid=192)
def enableActivityStateBonus():
    pass


@config(Bool, 'true', '�����������˫��״̬���')
def enableActivityStateDoubleCheck():
    pass


@config(Bool, 'true', '�����·�ǩ��', True, cid=193)
def enableNewServerSignIn():
    pass


@config(Int, '49', '���ַ������ҵȼ�', True, cid=194)
def noviceServerMaxPlayerLv():
    pass


@config(Int, '30', '���ַ�������ȼ�', True, cid=195)
def noviceServerMaxSocLv():
    pass


@config(Int, '4000', '���ַ������ħ����', True, cid=196)
def noviceServerMaxQuMo():
    pass


@config(Int, '30000', '���ַ������ۼ������', True, cid=197)
def noviceServerMaxJunJie():
    pass


@config(Bool, 'true', '�Ƿ������ս')
def enableClanWar():
    pass


@config(Bool, 'true', '�Ƿ�ˢ�������')
def enableRefreshWorldMonster():
    pass


@config(Bool, 'true', '�Ƿ��32λ�����ڴ����', True, cid=198)
def enableNewMemoryLimit():
    pass


@config(Bool, 'true', '�Ƿ������а�����ȡ����')
def enableTopRankRewardPushNotify():
    pass


@config(Bool, 'true', '�Ƿ�����Ӫ�tabҳ', True, cid=199)
def enableOpratingActiviesTab():
    pass


@config(Bool, 'true', '�Ƿ������ģʽ', True, cid=200)
def enableFubenHelpMode():
    pass


@config(Bool, 'true', '�Ƿ���������ȫ�������', True, cid=201)
def enableSendGlobalItemGainNotify():
    pass


@config(Bool, 'true', '�Ƿ����������ȫ�������', True, cid=202)
def enableRecvGlobalItemGainNotify():
    pass


@config(Bool, 'true', '�Ƿ�֧�ַ������¼���������')
def enableServerProgressMaxExp():
    pass


@config(Bool, 'true', '�Ƿ�����������', True, cid=203)
def enableGuildTournament():
    pass


@config(Bool, 'true', '�Ƿ���������������ģʽ', True, cid=204)
def enableGuildTournamentMultiGroup():
    pass


@config(Bool, 'true', '�Ƿ���������������', True, cid=205)
def enableGuildTournamentApply():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�ù�����������ս��', True, cid=206)
def enableGuildTournamentTestBF():
    pass


@config(Bool, 'false', '�Ƿ��������������', True, cid=207)
def enableCrossGuildTournament():
    pass


@config(Bool, 'false', '�Ƿ������������������а��ѡ���', True, cid=208)
def enableArenaPlayoffsTopRank():
    pass


@config(Bool, 'true', '�Ƿ���������������(�����)', True, cid=209)
def enableArenaPlayoffs():
    pass


@config(Bool, 'false', '�Ƿ���������������Ѻע����', True, cid=210)
def enableArenaPlayoffsBet():
    pass


@config(Bool, 'false', '�Ƿ��������̨���Ĺ���', True, cid=211)
def enableArenaChallenge():
    pass


@config(Bool, 'false', '�Ƿ��������̨���Ĺ�ս����', True, cid=212)
def enableArenaChallengeLive():
    pass


@config(Bool, 'false', '�Ƿ���������������ͨ�������ж���Ӯ�Ĺ���', True, cid=213)
def enableArenaPlayoffsBetTest():
    pass


@config(Bool, 'true', '�Ƿ������������������¶ҽ�����', True, cid=214)
def enableArenaPlayoffsBetReward():
    pass


@config(Bool, 'false', '�Ƿ�����������������������Զ�����', True, cid=215)
def enableCrossGtnApplyAlter():
    pass


@config(Bool, 'true', '�Ƿ���ѡ�˽�����Ƶ�ͳ��', True, cid=216)
def enableAvatarVideoAndWing():
    pass


@config(Bool, 'true', '�Ƿ�������29���Զ������', True, cid=217)
def enableReliveAutoWithLvLess():
    pass


@config(Bool, 'true', '�����·��������', True, cid=218)
def enableActivityAchieveScore():
    pass


@config(Bool, 'true', '�������������ù���', True, cid=219)
def enableCheckServerConfig():
    pass


@config(Bool, 'false', '�Ƿ��������ڿ�Ĺ���', True, cid=220)
def enableFashionNeiYi():
    pass


@config(Bool, 'true', '�Ƿ��Զ��Ӽ��ܵ�', True, cid=221)
def enableSkillLvAutoUp():
    pass


@config(Bool, 'true', '�Ƿ�����ɫУ��', True, cid=222)
def enableCheckSkin():
    pass


@config(Bool, 'false', '�Ƿ����·�ǩ�����', True, cid=223)
def enableNewServerSignInPanel():
    pass


@config(TimeStr, '', '崻�ʱ�䣬���ڸ���cd�Զ�����', False)
def fbReviseDowntime():
    pass


@config(Bool, 'true', '�Ƿ���л���ͼ��������', False)
def enableAbandonQuestWithSpaceChange():
    pass


@config(Bool, 'true', '�Ƿ�������ֱ��', True, cid=224)
def enableNoviceBoost():
    pass


@config(Bool, 'true', '�Ƿ�򿪴�����͵ع�ָ��', False)
def enableGroupGuide():
    pass


@config(Bool, 'true', '���ܽ�ѧ����', True, cid=225)
def enableSkillGuide():
    pass


@config(Bool, 'true', '�����Ѫ��', True, cid=226)
def enableMonsterBlood():
    pass


@config(Bool, 'false', '˫������Ŀ���', True, cid=227)
def enableDoubleExpPointInML():
    pass


@config(Bool, 'true', '�ǩ������', True, cid=228)
def enableActivityAttend():
    pass


@config(Bool, 'true', '����ֿ���', True, cid=229)
def enableActivityScore():
    pass


@config(Bool, 'true', '�Ƿ�����ģ����б����', True, cid=230)
def enableApplyModelRoll():
    pass


@config(Bool, 'true', '�Ƿ������������淨', True, cid=231)
def enableWorldPlayActivity():
    pass


@config(Bool, 'true', '�Ƿ�����ֵ�', True, cid=232)
def enableChargeActivity():
    pass


@config(Bool, 'true', '�Ƿ����·��߿����߼�', True, cid=233)
def enableDiGongLineLogic():
    pass


@config(Bool, 'true', '�Ƿ���space����initData�������', False)
def enableSpaceInitDataCheck():
    pass


@config(Bool, 'true', '�Ƿ����ͷ�', True, cid=234)
def enableCustomerService():
    pass


@config(Bool, 'true', '�Ƿ���vip�ͷ�', True, cid=235)
def enableCustomerVipService():
    pass


@config(Bool, 'false', '�Ƿ���vip�ͷ�ͼƬ�ϴ�', True, cid=236)
def enableCustomerVipServiceUploadPic():
    pass


@config(Bool, 'true', '�Ƿ���ð���ֲ�', True, cid=237)
def enableDelegation():
    pass


@config(Int, '1', 'vip�ȼ�1', True, cid=238)
def vipServiceLevel1():
    pass


@config(Int, '6', 'vip�ȼ�2', True, cid=239)
def vipServiceLevel2():
    pass


@config(Bool, 'false', '�Ƿ���ؾߺ͹���buff��һ���Խ��м��', True, cid=240)
def enableDoubleCheckZaijuBuffRelation():
    pass


@config(Bool, 'true', '�Ƿ������ϰ�ȫ���', True, cid=241)
def enableSecInfo():
    pass


@config(Bool, 'true', '�Ƿ��������ټ�', True, cid=242)
def enableGuildGather():
    pass


@config(Bool, 'true', '���������������', True, cid=243)
def enableFlowbackBonus():
    pass


@config(Bool, 'true', '�Ƿ񿨵����̽�صĵȼ�', False)
def enableFEManualUp():
    pass


@config(Bool, 'true', '�Ƿ��������˻', True, cid=244)
def enableFriendInviteActivity():
    pass


@config(Bool, 'true', '�Ƿ����������Ի���', True, cid=245)
def enableBackflowVp():
    pass


@config(Bool, 'false', '�Ƿ���У԰�л', True, cid=246)
def enableSchoolActivity():
    pass


@config(Bool, 'true', '�Ƿ�ɾ����ɫ��ʱ����', False)
def enableDeleteAccountCheck():
    pass


@config(Bool, 'false', 'UI�ӿ�ʹ��������', True, cid=247)
def useWeakrefUIInterface():
    pass


@config(Bool, 'true', '�Ƿ�����������', True, cid=248)
def enableInvSearch():
    pass


@config(Bool, 'true', '���õع��������', True, cid=249)
def enableDigongDetail():
    pass


@config(Bool, 'false', '������Ȫ�������', True, cid=250)
def enableWenQuanDetail():
    pass


@config(Bool, 'true', '����Ԫ��ƿ', True, cid=251)
def enableExpXiuWeiPool():
    pass


@config(Bool, 'true', '������Լƽ̨', True, cid=252)
def enableMessageBoard():
    pass


@config(Bool, 'true', '�Ƿ�����װ����װ�����', True, cid=253)
def enableEquipAddSuitEffect():
    pass


@config(Bool, 'true', '�������ѻ�������', True, cid=254)
def enableFriendFlowBack():
    pass


@config(Bool, 'true', '���������������', True, cid=255)
def enableGuildFlowBack():
    pass


@config(Bool, 'true', '��ս��Ʒ�ڹ涨ʱ����֧���з���Ȩ�޵���ҿ���ͨ', True, cid=256)
def enableGroupTrade():
    pass


@config(Bool, 'true', '��װ���Ĳ������²���GroupTradeʱ����������ȷ��', True, cid=257)
def enableLooseGroupTradeConfirm():
    pass


@config(Bool, 'true', '�Ƿ���npc�������', True, cid=258)
def enableNpcPuzzle():
    pass


@config(Bool, 'false', '�Ƿ���npc������ⴥ��', True, cid=259)
def enableNpcPuzzleTrigger():
    pass


@config(Bool, 'true', '�Ƿ�������ǷԪ��')
def enableDebtCoin():
    pass


@config(Bool, 'true', '�Ƿ���������֮ӡ�����Χ�ط���Ӫ')
def enableClanWarCreationGuardCheck():
    pass


@config(Bool, 'false', '�Ƿ������������ս', True, cid=260)
def enableWorldChallenge():
    pass


@config(Bool, 'true', 'ת�����Ƿ��������Ʒ', True, cid=261)
def checkMigrateItem():
    pass


@config(Bool, 'True', '������ع�Ѱ·', True, cid=262)
def enableCrossDiGongNavigator():
    pass


@config(Bool, 'true', '��ľ�����λ��ˢ��', True, cid=263)
def enableYmfMemberPos():
    pass


@config(Bool, 'true', '���������Ϣ����', True, cid=264)
def enableTeamInfoShare():
    pass


@config(Bool, 'true', '�Ƿ����ƾٹ���', True, cid=265)
def enableKeju():
    pass


@config(Bool, 'true', '�Ƿ���������ר�ü��ܷ���', True, cid=266)
def enableArenaSkillScheme():
    pass


@config(Bool, 'false', '�Ƿ��ڱ���ʱ��龺�������ܷ���', True, cid=267)
def enableCheckArenaSkillOnApply():
    pass


@config(Bool, 'true', '�Ƿ���ʹ����Ʒ��ȡ���ܶ�', False)
def enableAddIntimacyUseItem():
    pass


@config(Bool, 'true', '�Ƿ���������ս', True, cid=268)
def enableMutualBenefit():
    pass


@config(Bool, 'true', '�Ƿ���˫��', True, cid=269)
def enableShuangxiu():
    pass


@config(Bool, 'true', '�����������', True, cid=270)
def enableGlobalFriend():
    pass


@config(Bool, 'true', '�����µ�f�����Ⱦ', True, cid=271)
def enableNewFPanelRender():
    pass


@config(Bool, 'true', '�Ƿ����콵�������߽�������', True, cid=272)
def enableLoginReward():
    pass


@config(Bool, 'false', '�Ƿ�������ѧԺ�������', True, cid=273)
def enableServerBonus():
    pass


@config(Bool, 'true', '�Ƿ�������־', True, cid=274)
def enableRoleCardCollect():
    pass


@config(Bool, 'true', '�Ƿ�������־', True, cid=275)
def enableFengWuZhi():
    pass


@config(Bool, 'false', 'ʱװ����ת��', True, cid=276)
def enableFashionPropTrans():
    pass


@config(Bool, 'true', '�Ƿ��̳ǹ������', True, cid=277)
def enableRemotePic():
    pass


@config(Bool, 'true', '�Ƿ���һЩGM��ֻ���������������Ŷ�', False)
def enableLoginFromNeteaseOnlyCheck():
    pass


@config(Bool, 'true', '��̯�Զ���', True, cid=278)
def enableBoothCustom():
    pass


@config(Bool, 'true', '�Ƿ�ʹ���¸���ָ��', True, cid=279)
def enableNewFubenTargetGuide():
    pass


@config(Bool, 'true', '�Ƿ�����һ֡����AI', False)
def enableTriggerNextFrame():
    pass


@config(Bool, 'true', '�Ƿ���������ħ¼�', True, cid=280)
def enableCollectItem():
    pass


@config(Bool, 'true', '����ս��cc����Ҫ����cc����Դ���������', True, cid=281)
def enableZhanChangCC():
    pass


@config(Bool, 'true', '�Ƿ����ö��˺��������ı���', False)
def enableMultiPlayerTreasureBox():
    pass


@config(Bool, 'true', '�Ƿ������Ṥ����', True, cid=282)
def enableGuildQuestBoard():
    pass


@config(Bool, 'true', '�Ƿ�����������л���', True, cid=283)
def enableOfflineFlowback():
    pass


@config(Bool, 'false', '����㹦��', True, cid=284)
def enableInvitePoint():
    pass


@config(Bool, 'true', '��Ϸ��װ��������������վ���ݿ�', True, cid=285)
def enableEquipGotoWeb():
    pass


@config(Bool, 'true', '�Ƿ�������ֱ���ȼ�', True, cid=286)
def enableNoviceBoostLevelUp():
    pass


@config(Bool, 'false', '�Ƿ��ֹ��ҵ�½', True, cid=287)
def forbidEnterWorld():
    pass


@config(Bool, 'true', '�Ƿ����������ս��')
def enableNationalCombatScoreCalc():
    pass


@config(Bool, 'true', '�Ƿ���������ع���', True, cid=288)
def enableYaoPei():
    pass


@config(Bool, 'false', '�Ƿ���ȫ�����а�', True, cid=289)
def enableCrossArenaRank():
    pass


@config(Bool, 'false', '�Ƿ���������Ӫ', True, cid=290)
def enableWorldCamp():
    pass


@config(Bool, 'true', '�Ƿ�����ֵ����', True, cid=291)
def enableChargeReward():
    pass


@config(Bool, 'false', '�Ƿ���Ѻ�ڹ���', True, cid=292)
def enableYabiao():
    pass


@config(Bool, 'true', '�Ƿ���װ�������', True, cid=293)
def enableUnbindEquip():
    pass


@config(Bool, 'true', '�Ƿ���ְҵ��������', True, cid=294)
def enablePvpEnhance():
    pass


@config(Bool, 'true', '�Ƿ�������ϵͳ', True, cid=295)
def enableMingpai():
    pass


@config(Bool, 'true', '�Ƿ�������ֵϵͳ', True, cid=296)
def enableHaoqiVal():
    pass


@config(Bool, 'true', '�Ƿ�����Ʒֵϵͳ', True, cid=297)
def enableRenpinVal():
    pass


@config(Bool, 'true', '�Ƿ�������ʱ��', True, cid=298)
def enableIntimacyEvent():
    pass


@config(Bool, 'true', '�Ƿ�������ʱ��V2', True, cid=299)
def enableIntimacyEventV2():
    pass


@config(Bool, 'true', '�Ƿ����屦����ع���', True, cid=300)
def enableGuiBaoGe():
    pass


@config(Bool, 'true', '�Ƿ��������ҹ���', True, cid=301)
def enableFameTransfer():
    pass


@config(Bool, 'false', '�Ƿ���ʦͽ�Ӻ�����ع���', False)
def enableApprenticeFriend():
    pass


@config(Bool, 'true', '�Ƿ������߼Ӻ���', False)
def enableOfflineAddFriend():
    pass


@config(Bool, 'true', '�Ƿ������߲鿴װ��', False)
def enableOfflineWatchEquip():
    pass


@config(Bool, 'false', '�Ƿ��������ս', True, cid=302)
def enableWorldWar():
    pass


@config(Bool, 'true', '�Ƿ��������ս�µ�ͼ', True, cid=303)
def enableWorldWarNewMap():
    pass


@config(Bool, 'false', '�Ƿ��������սʤ������', True, cid=304)
def enableWorldWarJudge():
    pass


@config(Bool, 'true', '�Ƿ��������ս����������', True, cid=305)
def enableWorldWarUpgrade():
    pass


@config(Bool, 'false', '�Ƿ����۹��߾��Ӷ�', True, cid=306)
def enableWorldWarRob():
    pass


@config(Bool, 'false', '�Ƿ����۹��߾���ս', True, cid=307)
def enableWorldWarBattle():
    pass


@config(Bool, 'false', '�Ƿ����۹��߾���ս��Ӷ��', True, cid=308)
def enableWorldWarBattleHire():
    pass


@config(Bool, 'true', '�Ƿ����۹��߾����ڳ������')
def enableWorldWarRemoveZombie():
    pass


@config(Bool, 'false', '�Ƿ��������ս��Դ', True, cid=309)
def enableWorldWarBattleRes():
    pass


@config(Bool, 'false', '�Ƿ������Ҿ���', True, cid=310)
def enableWorldWarArmy():
    pass


@config(Bool, 'false', '�Ƿ������Ҿ��Ӽ���', True, cid=311)
def enableWorldWarArmySkill():
    pass


@config(Str, '', '�Ƿ������Ҿ��ӷ���(123ȫ��)', True, cid=312)
def worldWarBattleGroup():
    pass


@config(Bool, 'false', '�Ƿ�����սspace�쳣����', True, cid=313)
def enableWorldWarSpaceCheck():
    pass


@config(Bool, 'false', '�Ƿ��������ս�߳��Ƿ���ɫ')
def enableWorldWarKickDanger():
    pass


@config(Bool, 'true', '�Ƿ������ս�����¼')
def enableWorldWarSoulEnter():
    pass


@config(Bool, 'true', '�Ƿ����������', True, cid=314)
def enableCrossServerBag():
    pass


@config(Bool, 'true', '�Ƿ���ʱװȾɫ�Լ�', True, cid=315)
def enableCheckFashionDyeMaterials():
    pass


@config(Bool, 'true', '�Ƿ�����ս�߾���ԭ�ظ�����Ʒ���Ĺ���', True, cid=316)
def enableCrossBoarderReliveNow():
    pass


@config(Int, '500', '��ս���߾��������')
def worldWarMaxPlayer():
    pass


@config(Int, '300', '��ս��ս���߾��������������')
def worldWarBattleMaxPlayer():
    pass


@config(Int, '500', '��ս�Ӷᵥ�߾��������������')
def worldWarRobMaxPlayer():
    pass


@config(Int, '100', '��ս��ս���߾���������׻���')
def worldWarBattleYoungMaxPlayer():
    pass


@config(Int, '500', '��ս�Ӷᵥ�߾���������׻���')
def worldWarRobYoungMaxPlayer():
    pass


@config(Bool, 'true', '�Ƿ�����ս��ս�Ӷ�ֵȼ�', True, cid=317)
def enableWorldWarYoungGroup():
    pass


@config(Bool, 'true', '�Ƿ�����ս���ӷֵȼ�', True, cid=318)
def enableWorldWarArmyYoungGroup():
    pass


@config(Int, '150', '��ս��ս���߾�����Ӷ����')
def worldWarBattleMaxPlayerHire():
    pass


@config(Int, '50', '��ս�׻���ս���߾�����Ӷ����')
def worldWarBattleYoungMaxPlayerHire():
    pass


@config(Int, '30', '��ս�ܱ�������������')
def worldWarAssistLimit():
    pass


@config(Bool, 'true', '�Ƿ��������սIP����', True, cid=319)
def enableWorldWarMacAddressCheck():
    pass


@config(Bool, 'false', '�Ƿ�����Ԥ����ԤԼ', True, cid=320)
def enablePrePayCoin():
    pass


@config(Bool, 'true', '�Ƿ�����ӡ', True, cid=321)
def enableGuanYin():
    pass


@config(Bool, 'true', '�Ƿ�����ӡ�ڶ���', True, cid=322)
def enableGuanYinSecondPhase():
    pass


@config(Bool, 'true', '�Ƿ�����ӡ�꼼', True, cid=323)
def enableGuanYinSuperSkill():
    pass


@config(Bool, 'true', '�Ƿ�����������������', True, cid=324)
def enableSharedRideWingProp():
    pass


@config(Bool, 'true', '�Ƿ�������ֱ��', True, cid=325)
def enableGuildNoviceBoost():
    pass


@config(Bool, 'true', '�Ƿ�����VIP����', True, cid=326)
def enableVipQueue():
    pass


@config(Bool, 'true', '�Ƿ������ӳ����������', True, cid=327)
def enableDelayKickAvatar():
    pass


@config(Bool, 'false', '�Ƿ�֧���������', True, cid=328)
def enableRandomQuest():
    pass


@config(Bool, 'true', '�Ƿ�����ڱ���ʹ�ÿ����������Ʒ', True, cid=329)
def enableUseCrossInv():
    pass


@config(Bool, 'true', '�Ƿ��������ս', True, cid=330)
def enableMonsterClanWar():
    pass


@config(Bool, 'true', '�Ƿ���������', True, cid=331)
def enableRandWingFly():
    pass


@config(Bool, 'true', '�Ƿ�����ѭ����־', True, cid=332)
def enableRecursionLog():
    pass


@config(Bool, 'true', '�Ƿ�������ǰ��spell����', True, cid=333)
def enableTeleportSpell():
    pass


@config(Bool, 'false', '������remove����Ҫ������buff', True, cid=334)
def removeStateOnOffline():
    pass


@config(Bool, 'true', '�Ƿ����ø����淨', True, cid=335)
def enableDisturb():
    pass


@config(Bool, 'true', '�Ƿ��������Ը����淨', True, cid=336)
def enableInfect():
    pass


@config(Bool, 'true', '�Ƿ��ڱ�LOG', False)
def enableWabaoLog():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�����굹��ʱ����', True, cid=337)
def enableNewYearAni():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�����굹��ʱ����', False)
def enableSoulSaveShortcut():
    pass


@config(Bool, 'false', '�Ƿ���NPC���ϰ����', True, cid=338)
def enableMeterialNpc():
    pass


@config(Bool, 'false', '�Ƿ����ƴ��', True, cid=339)
def enablePinjiu():
    pass


@config(Bool, 'true', '�Ƿ��̳��ۿ�', True, cid=340)
def enableMallDiscount():
    pass


@config(Bool, 'true', '�Ƿ�������Ʒ֧����������', True, cid=341)
def enableLifeEquipEffect():
    pass


@config(Bool, 'true', '�Ƿ���cellapp������ʱ�Զ����ͷ���������', True, cid=342)
def enableAutoReduceOnlineLimitOnCellAppOverload():
    pass


@config(Bool, 'false', '�Ƿ�������ģʽ', True, cid=343)
def enableHolidayMode():
    pass


@config(Bool, 'true', '�Ƿ�֧�ֺ��', True, cid=344)
def enableRedPacket():
    pass


@config(Bool, 'false', '�Ƿ���ͼ��ͼƬ֧��', True, cid=345)
def enableBookPictureShow():
    pass


@config(Bool, 'true', '�Ƿ�����Ʊ', True, cid=346)
def enableLottery():
    pass


@config(Bool, 'false', '�Ƿ�������ie', True, cid=347)
def enableInnerIE():
    pass


@config(Bool, 'true', '�Ƿ�����Ѷ����', True, cid=348)
def enablePushZixun():
    pass


@config(Bool, 'true', '�Ƿ񿪷��²��ϰ�', True, cid=349)
def enableNewMaterialBag():
    pass


@config(Bool, 'true', '�Ƿ�����ռ���������', True, cid=350)
def enableAppearanceRank():
    pass


@config(Bool, 'true', '�Ƿ�������ҽ������ִ岢����')
def doXinshoucunAvatarCheck():
    pass


@config(Bool, 'true', '�Ƿ񿪷����ܶȼ���', True, cid=351)
def enableIntimacySkill():
    pass


@config(Bool, 'true', '�Ƿ񿪷�ս����Ӫ���', False)
def enableBfCampCheck():
    pass


@config(Bool, 'true', '�Ƿ񿪷����뵥���޶���ҵ��¹���', False)
def enableApplyGroupWithNonGroup():
    pass


@config(Bool, 'true', '����������Ʒ�Ͻɹ���', True, cid=352)
def enableWWNpcItemCommit():
    pass


@config(Bool, 'true', '�Ƿ���Ʒʹ������', True, cid=353)
def enableItemUsePush():
    pass


@config(Bool, 'true', '�Ƿ�ʹ���µ����url', True, cid=354)
def enableCameraNewURL():
    pass


@config(Bool, 'false', '�Ƿ�����Ӫ��������', True, cid=355)
def enableActivityHallIcon():
    pass


@config(Bool, 'true', '�Ƿ������뾺���������޸�', True, cid=356)
def enableArenaApplyNotify():
    pass


@config(Bool, 'true', '�Ƿ���Ѫ���Ĵ��󱨾�')
def enableXiezhanReporting():
    pass


@config(Bool, 'true', '�Ƿ񿪷����ܶȼ�����������', True, cid=357)
def enableIntimacySkillSSXS():
    pass


@config(Bool, 'true', '�����ܻ��Ƿ����˺�Ѫ����ֵӰ��', True, cid=358)
def enableHitActHpPercent():
    pass


@config(Bool, 'true', '�Ƿ������������', True, cid=359)
def enableZhenyaoActivity():
    pass


@config(Bool, 'true', '�Ƿ����޵е�doublecheck,��1�š�10���Լ����е�PVP��ͼ�У�doDamageʱ������Ǵ���Ѫս�����������һ�ε�WUDI���', False)
def enableXiezhanWudiDoubleCheck():
    pass


@config(Bool, 'true', '�������ձ���', True, cid=360)
def enableFaceEmote():
    pass


@config(Bool, 'true', '�µĶ���ģʽѡ���ˢ��', True, cid=361)
def enableNewAimCross():
    pass


@config(Bool, 'false', '�µĽŲ������Ź���', True, cid=362)
def enableNewFootSound():
    pass


@config(Bool, 'false', '��Ʒ�ӹ�', True, cid=363)
def enableMixJewelry():
    pass


@config(Bool, 'true', '�������ͺ�����Ĭ��pitchֵ', True, cid=364)
def enableSetTeleportPitch():
    pass


@config(Bool, 'true', '�Ƿ����˺�����Ķ���ȷ�ϣ����ڽ����Щghost����ͬ������ʱ���µĽ���������⣩')
def enableDoDamageParamDoubleCheck():
    pass


@config(Bool, 'true', 'double check�������������˵���entityֻ����һ�Σ����ڽ����Щghost����ͬ������ʱ���µĽ���������⣩')
def enableCreationCalcEntitiesDoubleCheck():
    pass


@config(Bool, 'true', '�������������Ʒ��鱨��', False)
def enableCrossInvItemWarning():
    pass


@config(Str, '<', '��������Ա���������bodyProp�ȽϷ�soulProp', False)
def crossPropWarningOp():
    pass


@config(Bool, 'true', '�Ƿ���ս���ٱ�����', True, cid=365)
def enableBfReport():
    pass


@config(Bool, 'true', '�Ƿ�����һ������ʾ���', True, cid=366)
def enablePushMessageOnceFlag():
    pass


@config(Bool, 'true', '��б�����Ǽ�����', True, cid=367)
def enableActivitySortedByStar():
    pass


@config(Int, '0', '�������˵���͵ȼ�')
def businessManMinLv():
    pass


@config(Bool, 'false', '�Ƿ������µĽ������', True, cid=368)
def enableNewRewardHall():
    pass


@config(Bool, 'true', '��ȡ���½���', True, cid=369)
def enableUpdateBonus():
    pass


@config(Bool, 'false', '�������Ĺ������а�', True, cid=370)
def enableGuildKindness():
    pass


@config(Bool, 'true', '���ù�ս��������', True, cid=371)
def enableWWQuestGuide():
    pass


@config(Bool, 'true', '�Ƿ�����������ɶ���', True, cid=372)
def enableCompleteQuestTip():
    pass


@config(Bool, 'true', '�Ƿ�����������ʾ����', True, cid=373)
def enableLvUpTip():
    pass


@config(Bool, 'true', '�Ƿ���buff�쳣��ʧ����')
def enableDebugStateDisappear():
    pass


@config(Bool, 'false', '�Ƿ�����Ϳװ', True, cid=374)
def enableTuzhuang():
    pass


@config(Bool, 'false', '�Ƿ����û÷�', True, cid=375)
def enableHuanFu():
    pass


@config(Bool, 'true', '�Ƿ���׷���߽���', True, cid=376)
def enableTradeApprentice():
    pass


@config(Bool, 'false', '�Ƿ���ͽ����ʦ������', True, cid=377)
def enableTradeToMentor():
    pass


@config(Bool, 'true', '�Ƿ��������ս', True, cid=378)
def enableRandomChallenge():
    pass


@config(Bool, 'false', '�Ƿ���realSense', True, cid=379)
def enableRealSense():
    pass


@config(Bool, 'false', '�Ƿ����״λ�ģʽ�ļ���λ��', True, cid=380)
def enableOperationShortCut():
    pass


@config(Bool, 'true', '�Ƿ����ֹ�װ��', True, cid=381)
def enableManualEquip():
    pass


@config(Bool, 'true', '�Ƿ������ֽ���', True, cid=382)
def enableNoviceReward():
    pass


@config(Bool, 'true', '�Ƿ���������ɽ����ڶ��׶�ui', True, cid=383)
def enableInteractiveObjReward():
    pass


@config(Bool, 'true', '�Ƿ��������������ȼ����㹦��', True, cid=384)
def enableUseFormulaToCalcExp():
    pass


@config(Bool, 'true', '�Ƿ���ʦͽֵmacaddress���', False)
def enableApprenticeValMacAddresCheck():
    pass


@config(Bool, 'false', '�Ƿ���ɹ�������������/ս��', False)
def enableEnterDuelCheck():
    pass


@config(Bool, 'false', '�Ƿ������˿ռ�', True, cid=385)
def enablePersonalZone():
    pass


@config(Bool, 'false', '�Ƿ������ڹ���', True, cid=386)
def enableBfBullet():
    pass


@config(Bool, 'true', '������������', True, cid=387)
def enableWearPhysics():
    pass


@config(Bool, 'false', '�Ƿ���avatar����', False)
def enableCheckAavatarCreate():
    pass


@config(Bool, 'false', '�Ƿ�����Ʒ������Դ��ѯ', True, cid=388)
def enableItemSearchIcon():
    pass


@config(Bool, 'false', '�Ƿ����°���Ʒ������Դ��ѯ', True, cid=389)
def enableNewItemSearch():
    pass


@config(Bool, 'false', '�Ƿ���VIP���칦��', False)
def enableVipCompensate():
    pass


@config(Bool, 'true', '�Ƿ���ҵɲ�����ְҵ��������ҵɲ��', True, cid=390)
def enableNewSchoolYeCha():
    pass


@config(Bool, 'true', '�Ƿ������ǵ�Rpc���󱨾�')
def enableAvatarRpcErrorWarning():
    pass


@config(Bool, 'false', '�Ƿ�����2', True, cid=391)
def enableMale2():
    pass


@config(Bool, 'true', '�Ƿ���������reloaddata')
def useIncrementalReloadData():
    pass


@config(Bool, 'true', '�Ƿ�����Item��Version')
def useItemVersion():
    pass


@config(Bool, 'true', '�Ƿ����ø�������2sCD���')
def enableEnteringFbCD():
    pass


@config(Bool, 'false', '�Ƿ���ѡ�˽���������ı�', True, cid=392)
def enableLoginWeather():
    pass


@config(Bool, 'false', '�Ƿ���װ��������ϵֿ�', True, cid=394)
def enableEquipDiKou():
    pass


@config(Bool, 'false', '�Ƿ�����ά�빦��', True, cid=395)
def enableQRCode():
    pass


@config(Bool, 'false', '�Ƿ���װ�����', True, cid=396)
def enableDisassembleEquip():
    pass


@config(Bool, 'false', '�Ƿ�����Ծ��', True, cid=397)
def enableActivation():
    pass


@config(Bool, 'true', '�Ƿ�����ս', True, cid=398)
def enableFightObserve():
    pass


@config(Bool, 'true', '�Ƿ�ս��VIP�ӳ�')
def enableBattleFieldVip():
    pass


@config(Bool, 'true', '�Ƿ���dotaս���Ŷ�ʱ������鱨��')
def enableDotaQueueItemNumCheck():
    pass


@config(Bool, 'true', '�Ƿ���ɱ��', True, cid=399)
def enableShaxing():
    pass


@config(Bool, 'false', '�Ƿ����µĸ����������', True, cid=400)
def enableNewFubenProgress():
    pass


@config(Bool, 'false', '�Ƿ�TreasureBox������Ʒ��ʱ��ȫ���ܿ���base��')
def enableTreasureBoxGenItemLimitCalledInBase():
    pass


@config(Bool, 'false', 'ʹ���µ�ͷ���ϴ�����', True, cid=401)
def enableNewFigureUpload():
    pass


@config(Int, '100', '����ͳ�Ʊ�����ֵ')
def monsterCheckMaxNum():
    pass


@config(Int, '50', '����ͳ�Ʊ�����Χ')
def monsterCheckDist():
    pass


@config(Bool, 'false', '�Ƿ������ϰ�����', True, cid=402)
def enableMaterialBagManualLifeSkill():
    pass


@config(Bool, 'true', '�Ƿ������᳡���еĹ�������֧��')
def enableReliveInGuildSpace():
    pass


@config(Bool, 'true', '������Ǯ����������Ʒ���Բ�һ�º��Ƿ񱨾�', False)
def enableCrossPropertyDiffWarning():
    pass


@config(Bool, 'true', '���ʼ�������ȡ��ʱ�����Ծ��', False)
def enableMailFetchCheckActivities():
    pass


@config(Bool, 'true', '�Ƿ�����԰', True, cid=403)
def enableHome():
    pass


@config(Bool, 'false', '�Ƿ�����԰�ֿ�', True, cid=404)
def enableStorageHome():
    pass


@config(Bool, 'true', '�Ƿ���ѡ�˽����Զ���ͷ��+�����ϴ�', True, cid=405)
def enableUploadCharacterPhoto():
    pass


@config(Bool, 'false', '�Ƿ��ܴ���Ů3ҵɲ', True, cid=406)
def enableCreateFemale3Yecha():
    pass


@config(Bool, 'false', '�Ƿ��ܴ���Ů2����', True, cid=407)
def enableCreateFemale2Yantian():
    pass


@config(Str, '', '������ѯtab�����tabIndex�ö��Ÿ���', True, cid=408)
def disableZixunTab():
    pass


@config(Bool, 'false', '�Ƿ�������', True, cid=409)
def enableFuDaiProxy():
    pass


@config(Bool, 'true', '�Ƿ��������ָ��', True, cid=410)
def enableChatCommand():
    pass


@config(Bool, 'false', '�Ƿ�����ѡװ����', True, cid=411)
def enableSubEquipment():
    pass


@config(Bool, 'true', '�Ƿ���װ�����Թ���', True, cid=412)
def enableShareEquipProp():
    pass


@config(Bool, 'false', '�Ƿ���˫��������', True, cid=413)
def enableTeamShengSiChang():
    pass


@config(Bool, 'false', '�Ƿ���˫�������������ݲ���', True, cid=414)
def enableTeamShengSiChangFakeMan():
    pass


@config(Bool, 'false', '�Ƿ������˽���', True, cid=415)
def enableQiRenReward():
    pass


@config(Bool, 'false', '�������䵫�������ʱ����')
def enableQuickOpenBox():
    pass


@config(Bool, 'true', '�Ƿ�����Ǯlogȫ�����ӹ㲥', False)
def enableCashLogBroadcast():
    pass


@config(Bool, 'true', '�Ƿ�������logȫ�����ӹ㲥', False)
def enableFameLogBroadcast():
    pass


@config(Bool, 'true', '�Ƿ���GroupStub�����Ż�')
def enableGroupStubShard():
    pass


@config(Bool, 'false', '������ʦͽ��ʦ����')
def enableApprenticeGraduateRevise():
    pass


@config(Bool, 'false', '�Ƿ�ʹ���µ�refreshscript')
def enableRefreshScriptNew():
    pass


@config(Bool, 'false', '�Ƿ�������refreshscript')
def enableQuickRefresh():
    pass


@config(Bool, 'true', '�Ƿ���������λ�ü�⹦��')
def enableArenaPositionCheck():
    pass


@config(Bool, 'true', '�Ƿ�����������������ս����', True, cid=416)
def enableArenaPlayoffsLive():
    pass


@config(Bool, 'true', '�Ƿ���GCGO')
def enableGcGo():
    pass


@config(Bool, 'false', '�Ƿ���70_79�ȼ��μ���������')
def enableArenaPlayoffsStatue():
    pass


@config(Bool, 'true', '�Ƿ�ɽ��������⹦��')
def enableInteractiveCheckPlayer():
    pass


@config(Bool, 'false', '�Ƿ���װ�����쾫��tab', True, cid=417)
def enableEquipChangeEnhance():
    pass


@config(Bool, 'false', '�Ƿ���װ����������tab', True, cid=418)
def enableEquipChangeReforge():
    pass


@config(Bool, 'true', '�Ƿ���dota��doubleCheck����')
def enableDotaDoubleCheckReport():
    pass


@config(Bool, 'false', '�Ƿ���װ�������λtab', True, cid=419)
def enableEquipChangeStar():
    pass


@config(Bool, 'false', '�Ƿ���װ��������װtab', True, cid=420)
def enableEquipChangeSuit():
    pass


@config(Bool, 'false', '�Ƿ���װ��������ӡtab', True, cid=421)
def enableEquipChangeGem():
    pass


@config(Bool, 'false', '�Ƿ�����Ѿ�����������', True, cid=422)
def enableFreeJuexingRebuild():
    pass


@config(Bool, 'true', '�Ƿ����˳�ͬ��Avatar����APP', True, cid=423)
def enableLogoutCharSnapshot():
    pass


@config(Bool, 'false', '�Ƿ�����ϦԸ��', True, cid=424)
def enableFestivalWishMadeView():
    pass


@config(Bool, 'false', '�Ƿ�����Ӱ����ʥ���Զ�ʹ�ù���', True, cid=425)
def enableAutoUseBattleFieldShopItem():
    pass


@config(Bool, 'false', '�Ƿ����ͻ��˵����ݰ������Լ��', True, cid=426)
def enableClientPackageCheck():
    pass


@config(Bool, 'false', '�Ƿ����ƴ��̻�', True, cid=427)
def enableYunChuiShop():
    pass


@config(Bool, 'false', '�Ƿ��������ƴ��̻�', True, cid=428)
def enablePrivateYunChuiShop():
    pass


@config(Bool, 'false', '�Ƿ������ض���ͼ����������˫Ӱ��')
def enableWsResetOnDieOrRelive():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=430)
def enableGuildRunMan():
    pass


@config(Bool, 'false', '�Ƿ�����԰��������')
def enableRearrangementRoom():
    pass


@config(Bool, 'true', '�Ƿ���������ȫ����Ա������')
def enableGiveAllTeamMemberReward():
    pass


@config(Bool, 'false', '�Ƿ����׳佱��', True, cid=431)
def enableFirstChargeReward():
    pass


@config(Bool, 'true', '�Ƿ������ֹ��������ֵѹ����')
def enableMonsterDmgReductionVSAvatar():
    pass


@config(Bool, 'false', '�Ƿ�����ֵ�ȼ�����', True, cid=432)
def enableChargeLvReward():
    pass


@config(Bool, 'true', '�Ƿ���װ��͸������Ⱦɫ', True, cid=433)
def enableEquipTransparenceDye():
    pass


@config(Bool, 'true', '�Ƿ����¹�������', True, cid=434)
def enableGuildTutorialNew():
    pass


@config(Bool, 'true', '�Ƿ����¹������������ʼ�����', True, cid=435)
def enableGuildTutorialMail():
    pass


@config(Bool, 'true', '�Ƿ�������ϵͳ', True, cid=436)
def enableHelpSystem():
    pass


@config(Bool, 'false', '�Ƿ�����԰����', True, cid=437)
def enableHomeIntimacy():
    pass


@config(Bool, 'false', '�Ƿ��������ǰ�㲥', False)
def enableActivityPreNotify():
    pass


@config(Bool, 'true', '�Ƿ���ٺ»����', True, cid=438)
def enableAward():
    pass


@config(Bool, 'false', '�Ƿ�����Ӫ����', True, cid=439)
def enableRewardGiftActivityIcons():
    pass


@config(Bool, 'false', '�Ƿ����ػݻ', True, cid=440)
def enableActivitySale():
    pass


@config(Bool, 'false', '�Ƿ��������ڸ���', True, cid=441)
def enableNewbiePay():
    pass


@config(Int, str(int(time.time())), '�����ڸ��ѹ��ܿ���ʱ��', True, cid=442)
def getNewbiePayEnableTime():
    pass


@config(Bool, 'false', '�Ƿ��������', True, cid=443)
def enableWelfare():
    pass


@config(Bool, 'true', '�Ƿ������˿ռ�APP���ݻ�ͨ', True, cid=444)
def enablePersonalZoneInterface():
    pass


@config(Bool, 'false', '�Ƿ�����ڨ�Ӻ���֪ͨAPP��', False)
def enableAddFriendPostMsg2App():
    pass


@config(Bool, 'false', '�Ƿ������˿ռ�APP������ͨ', True, cid=445)
def enablePersonalZoneAudio():
    pass


@config(Bool, 'true', '�Ƿ��������¼�', True, cid=446)
def enableWorldArea():
    pass


@config(Bool, 'true', 'enable GM ip address check?', True, cid=447)
def enableCheckGmIP():
    pass


@config(Bool, 'true', 'enable exception log?', True, cid=448)
def enableExceptionLog():
    pass


@config(Bool, 'false', '�Ƿ���µ����Լ��㣬ֻ���������ܲ���')
def enableNewPropCalc():
    pass


@config(Bool, 'false', '�Ƿ�ֻ���µ����Լ���')
def enableOnlyNewPropCalc():
    pass


@config(Bool, 'true', '�Ƿ��ھ����Լ����в�������Diff')
def enableInnerPropCheck():
    pass


@config(Bool, 'false', '�Ƿ�ʱ��У���¾����Լ�����Diff')
def enableTimerPropCheck():
    pass


@config(Float, '0.3', '�Ƿ�ʱ��У���¾����Լ�����Diff�ĸ���')
def probTimerPropCheck():
    pass


@config(Bool, 'false', '����ڵ�¼loadingͼ', True, cid=449)
def enableZhongQiuLoadingPic():
    pass


@config(Bool, 'false', '�Ƿ�������ͳ˧', True, cid=450)
def enableWWArmyImpeach():
    pass


@config(Bool, 'true', '�Ƿ���stream msgpack�Ż�')
def enableServerStartCheck():
    pass


@config(Bool, 'true', '�Ƿ�������ǿ������', True, cid=451)
def enableGuildRobber():
    pass


@config(Bool, 'false', 'enable kick the inactive players', True, cid=452)
def enableKickInactivePlayer():
    pass


@config(Bool, 'true', '�Ƿ����͸�Ϊ������֮·', True, cid=453)
def enablePlayRecommPush():
    pass


@config(Bool, 'false', '�Ƿ�֧��Ԥ���Ҿ�', True, cid=454)
def enablePreviewHomeFurniture():
    pass


@config(Bool, 'true', 'enable mail cash', True, cid=455)
def enableMailCash():
    pass


@config(Bool, 'true', '�Ƿ���֪ͨ���GM�ʼ�', True, cid=456)
def enableIngameGMMail():
    pass


@config(Bool, 'true', 'enable homosexual intimacy', True, cid=457)
def enableHomosexualIntimacy():
    pass


@config(Bool, 'true', 'enable festival event', True, cid=458)
def enableFestivalEvent():
    pass


@config(Bool, 'true', '�����ֿ����Ƿ�ʹ���Ż���ĵ�������ʽ', False)
def enableOptimizedItemSortFunc():
    pass


@config(Bool, 'false', '���¼�����', True, cid=459)
def enableFittingRoomLvUp():
    pass


@config(Bool, 'false', '��������', True, cid=460)
def enableEnlargeHomeRoom():
    pass


@config(Bool, 'True', '�Ƿ�����ս��������', True, cid=461)
def enableWWGuildTournament():
    pass


@config(Bool, 'true', '�Ƿ���������', True, cid=462)
def enableWMD():
    pass


@config(Bool, 'false', '����������ƶ��Ҿ�', True, cid=463)
def enableKeyBoardMoveFurniture():
    pass


@config(Bool, 'false', '����תְ', True, cid=464)
def enableSchoolTransfer():
    pass


@config(Bool, 'true', '����תְ״̬���', True, cid=465)
def enableSchoolTransferStatusCheck():
    pass


@config(Bool, 'true', '����תְ�����ж�', True, cid=466)
def enableSchoolTransferConditionCheck():
    pass


@config(Bool, 'false', '���������̵�', True, cid=467)
def enablePrivateShop():
    pass


@config(Bool, 'false', '�������ֿܵ�', True, cid=468)
def enableSkillDiKou():
    pass


@config(Bool, 'true', '�Ƿ����ƴ����а񹤻��Ա����ģʽ', True, cid=469)
def enableYunChuiRankGuildMemberAward():
    pass


@config(Int, str(int(time.time())), '�ƴ��½���ģʽ��һ������ʱ��', True, cid=470)
def clanWarFirstOpenTimeAfterNewReward():
    pass


@config(Bool, 'false', '�����ռ�����', True, cid=471)
def enablePersonalZoneVoice():
    pass


@config(Bool, 'true', '�Ƿ������ս���а񹫻��Ա��ս����', True, cid=472)
def enableClanWarTopGuildMemberAward():
    pass


@config(Bool, 'true', '�Ƿ��������ȡʱquests��questDataУ��', False)
def enableQuestsAndQuestDataCheck():
    pass


@config(Bool, 'false', '�Ƿ���������ս�������', True, cid=473)
def enableMonsterTalkInCombat():
    pass


@config(Bool, 'false', '�Ƿ������ǿ����д��ϸ����', True, cid=474)
def enableGroupDetailForcely():
    pass


@config(Bool, 'true', '�Ƿ������Ƿ��ѿ�', False)
def enableCheckOuterNet():
    pass


@config(Bool, 'true', '�Ƿ�������Ӫ�жԹ���', True, cid=475)
def enableNewCampRelation():
    pass


@config(Bool, 'false', '���������Ƿ���԰ڷ�avatar�Ҿ�', True, cid=476)
def enableFittingRoomIntimacy():
    pass


@config(Int, '0', '�����̳���ҳ', True, cid=477)
def enableShowMallWeb():
    pass


@config(Bool, 'false', 'ɨ��֧������', True, cid=478)
def enableQrcodeRecharge():
    pass


@config(Bool, 'false', '�����Ҿ�pitch��ת', True, cid=479)
def enableFurnitureRotatePitch():
    pass


@config(Bool, 'false', '�Ƿ�����������ս���ų��������', True, cid=480)
def enableChangeLeaderInFortBattleField():
    pass


@config(Bool, 'false', '�Ƿ����ף����������')
def enableCalcBlessAndCurse():
    pass


@config(Bool, 'false', '����createfubenָ����Խ������', True, cid=481)
def enableCreateFubenIgnoreCheck():
    pass


@config(Float, str(2.0), '�·�����ʱ��֮������ʱ��', False)
def newServerOpenOuterNetDelay():
    pass


@config(Int, str(200), '�·�������ʱ��֮ǰ�����������', False)
def newServerMassLimitBeforeOpenOuterNet():
    pass


@config(Bool, 'true', '�Ƿ��·�ǰ��Сʱ������������', False)
def enableNewServerMassLimitBeforeOpenOuterNet():
    pass


@config(Bool, 'false', '��԰��������', True, cid=482)
def enableInteractiveHomeChat():
    pass


@config(Bool, 'false', '�ɽ������������', True, cid=483)
def enableInteractiveCoupleEmote():
    pass


@config(Bool, 'false', '�°�������', True, cid=484)
def enableTabAuction():
    pass


@config(Bool, 'false', '�Ƿ���忪��GC', True, cid=485)
def enableCtrlWidgetGC():
    pass


@config(Bool, 'true', '�Ƿ���ʱװ������', True, cid=486)
def enableFashionBagRenew():
    pass


@config(Bool, 'false', '�Ƿ���ֱ��', False)
def enableStraightLvUp():
    pass


@config(Bool, 'false', '�Ƿ���app/΢�Ű󶨽�������', True, cid=487)
def enableBindReward():
    pass


@config(Bool, 'false', '�Ƿ���buffer��̬���Լ���Ĺ���', True, cid=488)
def enableBufferPropQuery():
    pass


@config(Bool, 'true', '�Ƿ�֧�ֹ�������', True, cid=489)
def enableClan():
    pass


@config(Bool, 'false', '�Ƿ���װ������', True, cid=490)
def enableEquipSoul():
    pass


@config(Bool, 'true', '�Ƿ���װ�����鼤����Ч', True, cid=491)
def enableEquipSoulFlyEffect():
    pass


@config(Bool, 'false', '�Ƿ���װ������෽��', True, cid=492)
def enableEquipSoulSchemes():
    pass


@config(Bool, 'false', '�Ƿ�ʼ��������', True, cid=493)
def enableChatLink():
    pass


@config(Bool, 'false', '�Ƿ���ֱ��ͻ��', True, cid=494)
def enableLevelBreakthrough():
    pass


@config(Bool, 'true', '�Ƿ����½�ɫnovice�쳣����', False)
def enableSendNewAvatarNoviceError():
    pass


@config(Bool, 'false', '�Ƿ���ǿ������noviceΪtrue', False)
def enableSetNoviceTrue():
    pass


@config(Bool, 'false', '�Ƿ񻺴�UI����', True, cid=495)
def enableCacheUI():
    pass


@config(Bool, 'false', '�Ƿ��ѵ����ҵɲְҵ', True, cid=496)
def enableTrainingAreaYeCha():
    pass


@config(Str, '1111111111000', '����תְת��ְҵ����', True, cid=497)
def schoolTransferOutLimit():
    pass


@config(Str, '1111111111000', '����תְת��ְҵ����', True, cid=498)
def schoolTransferInLimit():
    pass


@config(Bool, 'true', '�Ƿ������Ԥ��', True, cid=499)
def enableCharacterSharePreview():
    pass


@config(Bool, 'false', '�Ƿ���stream�Ż�')
def enableStreamOptimization():
    pass


@config(Bool, 'false', '�Ƿ���stream�Ż����')
def enableStreamCheckAlways():
    pass


@config(Bool, 'false', '�Ƿ���stream msgpack�Ż�')
def enableStreamMsgPack():
    pass


@config(Bool, 'false', '�Ƿ������ú����Ż�')
def enableFrequentCache():
    pass


@config(Bool, 'false', '�Ƿ������ú����Ż����')
def enableFrequentCacheCheck():
    pass


@config(Bool, 'false', '�Ƿ�����ս�����߱�������')
def enableBFNewStaticProtect():
    pass


@config(Bool, 'true', '�Ƿ�����ս�Ӷᴫ�ͷ���˿ɴ���')
def enableTeleportServerCheck():
    pass


@config(Bool, 'true', '�Ƿ������������ҽӵ������ϵ�cue�¼�', True, cid=500)
def enableAttachWeaponCue():
    pass


@config(Bool, 'false', '�Ƿ������ܾ����Զ�߽��Ż�', True, cid=501)
def enableSkillDistAutoOpt():
    pass


@config(Int, str(0), 'CPU����ѭ������������10000�ı�����')
def dummyCPULoopCount():
    pass


@config(Bool, 'true', '�Ƿ�������ݴ���', False)
def enableCrossServerSpaceCheck():
    pass


@config(Bool, 'true', '�Ƿ���תְ�󾺼������ܵ�����')
def enableArenaSkillPointReCalc():
    pass


@config(Bool, 'true', '�����µ�GfxValue����', True, cid=502)
def enableNewGfxValue():
    pass


@config(Bool, 'true', '�Ƿ�������Բ������', False)
def enableFubenRoundTable():
    pass


@config(Bool, 'false', '�Ƿ�����԰���Ե�ͼ', False)
def debugHomeMap():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�����Ҽ��˵�', True, cid=503)
def enableNewMenu():
    pass


@config(Bool, 'false', '�Ƿ���pvp׷��ϵͳ', True, cid=504)
def enablePursuePvp():
    pass


@config(Bool, 'false', '�Ƿ��������׷��ϵͳ', True, cid=505)
def enablePursueYaopei():
    pass


@config(Bool, 'false', '�Ƿ�������Ȩ�����ù���', True, cid=506)
def enableHomePermissionSet():
    pass


@config(Bool, 'false', '�Ƿ���hotKey��ͻ����', False)
def enableHotKeyCheckConflict():
    pass


@config(Bool, 'true', '�Ƿ���Avatar��¼�·��Ż�', True, cid=507)
def enableSendAvatarDataOptimization():
    pass


@config(Bool, 'true', '�Ƿ���Avatar��¼��Ʒ�����Ż�', True, cid=508)
def enableSendAvatarDataNoChangeToItem():
    pass


@config(Bool, 'false', '���������Ż�', True, cid=509)
def enableCubeOptimization():
    pass


@config(Int, '1500', '���������Ż�', True, cid=510)
def homeCubeMaxNum():
    pass


@config(Int, '2', '����սһ�ܿ��Ŷ��ٴ�,���ϴ������')
def worldWarRobMaxWeeklyOpen():
    pass


@config(Int, '0', '���������ܶȵȼ�����:Ϊ0ʱ��������0ʱ��Ч')
def acIntimacyMinLv():
    pass


@config(Bool, 'false', '�Ƿ���������ϰ��۳�', True, cid=511)
def enableQuestMaterialBag():
    pass


@config(Bool, 'false', '�Ƿ��������¼�����ǿ�ȵ���')
def enableAreaEventMonsterPowerSet():
    pass


@config(Bool, 'false', '�Ƿ��������Ȧ���ӵ�������')
def enableMonsterOverlapChange():
    pass


@config(Bool, 'false', '�Ƿ��������̵���ͨ�۳�', True, cid=512)
def enableSellNormalToCompositeShop():
    pass


@config(Bool, 'true', '�Ƿ���Boss��ս�ֲ������')
def enableBossVirtualMonsterCheck():
    pass


@config(Bool, 'false', '�Ƿ���UIͳ��Log', True, cid=513)
def enableUIStatistisc():
    pass


@config(Bool, 'false', '�Ƿ�����˷�', True, cid=514)
def enableRemoveHome():
    pass


@config(Bool, 'false', '�Ƿ�����ս����dummyCheck', False)
def enableBfDummyCheck():
    pass


@config(Bool, 'false', '���������ǳƵ����ÿ���', True, cid=515)
def enableIntimacyTgtNickName():
    pass


@config(Bool, 'true', '���ܺ꿪��', True, cid=516)
def enableSkillMacro():
    pass


@config(Bool, 'false', '�������LOG�Ƿ���', True, cid=517)
def enableLianYunStatistisc():
    pass


@config(Bool, 'true', '�����еĸ��س����Ƿ���', True, cid=518)
def enableCheckTaskLoad():
    pass


@config(Bool, 'false', '�Ƿ���Bossǿ�ȵ���')
def enableBossPowerSet():
    pass


@config(Bool, 'true', '������ѷ������¼�����Ƿ���', True, cid=519)
def enableGlobalFriendServerProgressCheck():
    pass


@config(Bool, 'false', '��Ӹ���', True, cid=520)
def enableGroupFollow():
    pass


@config(Bool, 'false', '��Ӹ����������', True, cid=521)
def enableTempGroupFollow():
    pass


@config(Bool, 'false', '�Ƿ�����Ӹ����Զ�ս��', True, cid=522)
def enableGroupFollowAutoAttack():
    pass


@config(Int, '5', '����������Զ�ˢ�¼��', True, cid=523)
def xConsignClientAutoRefresh():
    pass


@config(Bool, 'true', '�Ƿ�����ս����ؼ�¼')
def enableCheckWorldWarLoad():
    pass


@config(Bool, 'false', '�Ƿ񻺴���Ʒtip', True, cid=524)
def enableCacheTip():
    pass


@config(Bool, 'false', '�Ƿ����ؾ߼������ڶ���', True, cid=525)
def enableZaijuV2():
    pass


@config(Bool, 'false', '�Ƿ����ʾ���', True, cid=526)
def enableQuestion():
    pass


@config(Bool, 'false', '�Ƿ��������ϰ�������֪ͨ����', False)
def enableNotifyLogOnTopDataBack():
    pass


@config(Bool, 'false', '�Ƿ�����������ʱװ����', True, cid=527)
def enableXinshouSevenDay():
    pass


@config(Bool, 'false', '�Ƿ����Ṧ�Զ�Ѱ·', True, cid=528)
def enableQingGongPathFinding():
    pass


@config(Bool, 'false', '�Ƿ������а񸻹�ֵ', True, cid=529)
def enableRankingHomeWealth():
    pass


@config(Bool, 'false', '�Ƿ���mongolog��schema��鹦��')
def enableMongoLogSchemaCheck():
    pass


@config(Bool, 'true', '�Ƿ���ͬһʱ����������౨��')
def enableAlarmOfEnterFubenTooMany():
    pass


@config(Int, '8', '���ý�������������ֵ')
def enterFubenTooManyAlarmCount():
    pass


@config(Bool, 'true', '�Ƿ���ͬһʱ��WriteToDB���౨��')
def enableAlarmOfWriteToDBTooMany():
    pass


@config(Int, '5', '����CellApp��WriteToDBһ���ڴ���������ֵ')
def enterWriteToDBTooManyAlarmCount():
    pass


@config(Bool, 'true', '�Ƿ��������¼�����')
def enableDebugWorldAreaManager():
    pass


@config(Bool, 'true', '�Ƿ�������TPOS���Ż�', True, cid=530)
def enableNeedIgnoreTpos():
    pass


@config(Bool, 'false', '�Ƿ���ս�鿪��', True, cid=531)
def enableSummonedSprite():
    pass


@config(Bool, 'true', '�Ƿ���������ս��Ĺ���', False)
def enableGetSummonedSpriteByQuest():
    pass


@config(Bool, 'true', '�Ƿ�����ս�����ͳ����Mongo��־')
def enableSpriteStatLog():
    pass


@config(Bool, 'false', '�Ƿ����淨�������', True, cid=532)
def enableEvaluate():
    pass


@config(Bool, 'false', '�Ƿ������ͷ����ʶ', True, cid=533)
def enableTeamIdentity():
    pass


@config(Int, '28345', '���������¼��������Id')
def debugWorldAreaMonserCharType():
    pass


@config(Bool, 'false', '�Ƿ���ϵͳ��Ϣ����', True, cid=534)
def enableSystemMessage():
    pass


@config(Bool, 'true', '�Ƿ�����Ǯ�ճ��淨', True, cid=535)
def enableWorldQuestLoopRefresh():
    pass


@config(Bool, 'false', '�Ƿ���������һ�ڼ�����', True, cid=536)
def enableConsignMaxFixedPrice():
    pass


@config(Bool, 'true', '�Ƿ������ߺ�����Ϣ����', True, cid=537)
def enableOfflineFriendNotifyMsg():
    pass


@config(Bool, 'true', '�Ƿ����ȡ��', True, cid=538)
def enableRandomName():
    pass


@config(Bool, 'false', '�Ƿ������loadingͼ', True, cid=539)
def enableRandomLoadingPic():
    pass


@config(Bool, 'true', '�Ƿ���Է��ʿ����԰', True, cid=540)
def enableCrossServerHome():
    pass


@config(Bool, 'true', '�Ƿ�����hotfix��runscript֮ǰ���һ���ļ��Ƿ����python�﷨', True, cid=541)
def enableCheckRunscriptFileErrors():
    pass


@config(Bool, 'false', '�Ƿ����������V2', True, cid=542)
def enableHonorV2():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=543)
def enableSchoolFame():
    pass


@config(Bool, 'true', '�Ƿ���С��Ϸ', True, cid=544)
def enableMiniGame():
    pass


@config(Bool, 'true', '�Ƿ��������Ƽ�', True, cid=545)
def enableRecommendFriend():
    pass


@config(Int, '0', '�����Ƽ����Է�����ID')
def recommendFriendTestHostId():
    pass


@config(Int, '0', '�����Ƽ��������GBID')
def recommendFriendTestGbId():
    pass


@config(Bool, 'true', '�Ƿ����˷ܵ㹦�ܿ������', True, cid=546)
def enableExcitementFeatureCheck():
    pass


@config(Int, '40', '�����Ƽ�������Ŀ����')
def recommendFriendOnlineMaxNum():
    pass


@config(Bool, 'false', '�Ƿ����͵ȼ����תְ', True, cid=547)
def enableLowLvFreeSchoolTransfer():
    pass


@config(Bool, 'true', '�Ƿ��������������õ�����ǰ��״̬ʱ�ı���')
def warnOnPSkillPreconditionAttrUsed():
    pass


@config(Bool, 'true', '�Ƿ���������˿ռ�', True, cid=548)
def enableCrossServerZone():
    pass


@config(Bool, 'false', '�Ƿ�����������õ�ͼ�ĸ������ʱ�䶯̬�ɵ���', True, cid=549)
def enableCalcAvatarReliveIntervalDynamicAdjust():
    pass


@config(Bool, 'true', '�Ƿ����˷ܵ㹦�ܿͻ���UI', True, cid=550)
def enableExcitementClientShow():
    pass


@config(Bool, 'true', '�Ƿ������˫������', True, cid=551)
def enableCrossRideTogether():
    pass


@config(Bool, 'true', '�Ƿ��������ѡװ����', True, cid=552)
def enableCrossSubEquipment():
    pass


@config(Bool, 'true', '�Ƿ������ʹ�ù��Ἴ��', True, cid=553)
def enableCrossUseGuildMemberSkill():
    pass


@config(Bool, 'false', '�Ƿ����Ṧ����ѧ��Ƶͼ������', True, cid=554)
def enableQinggongWingTutorialIcon():
    pass


@config(Bool, 'false', '�Ƿ���Cython�Ż�')
def enableCythonSkillObject():
    pass


@config(Bool, 'false', '�Ƿ���UIProfile', True, cid=555)
def enableUIProfile():
    pass


@config(Int, '10', 'ÿ֡ͬʱ���������������', True, cid=556)
def enableToplogoTotalOptimize():
    pass


@config(Bool, 'true', '�Ƿ����������', True, cid=557)
def enableGuildPuzzle():
    pass


@config(Bool, 'false', '�Ƿ�����Ч�����Ż�', True, cid=558)
def enableEffectLoadOptimize():
    pass


@config(Bool, 'false', '������ʦͽ����', True, cid=559)
def enableApprenticeOptimize20174():
    pass


@config(Bool, 'false', '�Ƿ���USʦͽ�Ƽ�', True, cid=560)
def enableUSRecommendApprentice():
    pass


@config(Int, '0', 'ʦͽ�Ƽ����Է�����ID')
def recommendApprenticeTestHostId():
    pass


@config(Int, '0', 'ʦͽ�Ƽ��������GBID')
def recommendApprenticeTestGbId():
    pass


@config(Bool, 'false', '����¼���ϴ�����', True, cid=561)
def enableSoundRecord():
    pass


@config(Bool, 'false', 'App����¼���ϴ�����', True, cid=562)
def enableSoundRecordFromApp():
    pass


@config(Bool, 'true', '�Ƿ����ɽ����������', True, cid=563)
def enableQuestInteractive():
    pass


@config(Bool, 'false', '�Ƿ���һ����', True, cid=564)
def enableQuestLoopChain():
    pass


@config(Int, '1497484800', 'һ��������ʱ��', True, cid=565)
def questLoopChainStartTime():
    pass


@config(Bool, 'true', '�Ƿ����޾���ս', True, cid=566)
def enableEndlessChallenge():
    pass


@config(Bool, 'true', '�Ƿ���npc˫�˴���', True, cid=567)
def enableNpcPairPuzzle():
    pass


@config(Bool, 'false', '�Ƿ�����ħ�Ż�', True, cid=568)
def enableQumoOptimize():
    pass


@config(Bool, 'false', '�Ƿ����ճ������޾�ѭ��ģʽ', True, cid=569)
def enableEndlessLoopMode():
    pass


@config(Bool, 'false', '�Ƿ���������Bonus��Ʒ����', True, cid=570)
def enableFirstLoopBonusReward():
    pass


@config(Bool, 'true', '�Ƿ������ս�����Ǻ���')
def enableAvatarCallHelpOnDotaBattle():
    pass


@config(Bool, 'false', '�Ƿ���toplogo�Ż�', True, cid=571)
def enableTopLogoOptimize():
    pass


@config(Bool, 'false', '�Ƿ���toplogo�Ż�(toplogo�����û���)', True, cid=572)
def enableTopLogoSuperOptimize():
    pass


@config(Int, '-1', 'ʹ��Ѷĳ��tabҳ�ö�', True, cid=573)
def setZixunTabTop():
    pass


@config(Bool, 'true', '�Ƿ��������¼��ѯ����', True, cid=574)
def enableBoxItemHistory():
    pass


@config(Bool, 'false', '�Ƿ���PNG����ͷ��', True, cid=575)
def enablePNGProfileIcon():
    pass


@config(Bool, 'false', '�Ƿ������˿ռ�ս������', True, cid=576)
def enablePersonalSpaceBfData():
    pass


@config(Int, '1499011200', '��������������ʼʱ��', True, cid=577)
def gtnSeasonStartTime():
    pass


@config(Bool, 'false', '�����ڴ滷���ü��')
def enableDestroyEntityCheck():
    pass


@config(Bool, 'true', '�Ƿ���������������', True, cid=578)
def enableGuildTournamentSeason():
    pass


@config(Bool, 'true', '�Ƿ�������ί��ϵͳ', True, cid=579)
def enableOpenSchoolEntrust():
    pass


@config(Bool, 'false', '�Ƿ���ʦͽСĿ��', True, cid=580)
def enableApprenticeTarget():
    pass


@config(Bool, 'true', 'Ӧ���µ���Ƶѡ��', True, cid=581)
def enableNewVideoConfig():
    pass


@config(Str, '', '��ս���Ӻ�ѡ����ָ������,���⴦��ʹ��, Ĭ��Ӧ��Ϊ���ַ���')
def worldWarVoteGroupType():
    pass


@config(Bool, 'true', '�Ƿ�����������ɱ����', True, cid=582)
def enableFirstKill():
    pass


@config(Bool, 'true', '�Ƿ���MultiCellFubenManager��ֵ���ͬ��base��')
def enableSplitFbMgr():
    pass


@config(Bool, 'false', '�Ƿ�����԰���书��')
def enableHomeTreasureBox():
    pass


@config(Str, '123.58.167.166:8181', 'deeppeek�����ɫ��gtAdmin��IP:PORT', True, cid=583)
def deeppeekAddress():
    pass


@config(Bool, 'true', '�Ƿ���Npc����lod', True, cid=584)
def enableHideNpc():
    pass


@config(Bool, 'false', '�Ƿ���С��ͼλ�����', True, cid=585)
def enableDotaHeroTweenPos():
    pass


@config(Bool, 'false', '�Ƿ���������ﱥʳ��', True, cid=586)
def enableRideWingDurability():
    pass


@config(Bool, 'true', '�Ƿ�����ʱװת������', True, cid=587)
def enableFashionExhange():
    pass


@config(Int, '150', '������ɼ�NPC����', True, cid=588)
def getNpcModelMaxCnt():
    pass


@config(Bool, 'false', '�����Ǵ�����ʱ�򣬶�cellDataʹ��copy������deepcopy')
def useCopyOnAvatarCellDataCreate():
    pass


@config(Bool, 'false', '��Ӹ��棬��Ա����ӳ�Ѱ·', True, cid=589)
def enableGroupFollowHeaderPath():
    pass


@config(Bool, 'false', '�Ƿ����Զ�����', True, cid=590)
def enableAutoQuest():
    pass


@config(Bool, 'true', '��ȷ����HOT,DOT��������buff�ĳ���ʱ��', True, cid=591)
def enableAccurateDotTime():
    pass


@config(Bool, 'true', '�Ƿ�����ά�������', True, cid=592)
def enableGmFLowbackBonus():
    pass


@config(Bool, 'true', '�Ƿ�����԰����', True, cid=593)
def enableClearDeadHome():
    pass


@config(Bool, 'false', '�Ƿ����ֱ�ӹر�ʵ����֤����', True, cid=594)
def enableForceCloseRealNameWnd():
    pass


@config(Bool, 'false', '�Ƿ��������ڴ����ͳ��', True, cid=595)
def enableNewAnimationMemoryLimit():
    pass


@config(Bool, 'false', '�Ƿ������װ��չʾ����', True, cid=596)
def enablePartnerEquipment():
    pass


@config(Bool, 'true', '�Ƿ�����һ����ʹ�ö����Ʒ���ѵ���һ��', True, cid=597)
def enableUseMultipleItems():
    pass


@config(Bool, 'true', '�Ƿ��Զ��޸��ض����������', False)
def enableAutoFixSomeQuest():
    pass


@config(Bool, 'true', '�Ƿ��� ����ʾ��ʵ���toplogo������', True, cid=598)
def enableNotCreateTopLogoForHide():
    pass


@config(Bool, 'true', '�Ƿ���ƶ࿪����ҵĻ�Ծ�Ȼ�ȡ', False)
def enableActivationSameMacLimit():
    pass


@config(Bool, 'false', '�Ƿ���redis����', True, cid=599)
def enableRedisConnection():
    pass


@config(Bool, 'false', '�Ƿ�������ع��¹���', True, cid=600)
def enableZhiZunHuiGui():
    pass


@config(Bool, 'false', '�Ƿ���redis���ʽӿ�', True, cid=601)
def enableRedisOperation():
    pass


@config(Bool, 'true', '�Ƿ����ü�԰founder�Զ������ݱ�', True, cid=602)
def enableCustomHomeFounderDataTable():
    pass


@config(Bool, 'false', '�Ƿ�����ü�԰founder�Զ������ݱ������޸ĺ��´�����founder��ֱ��ʹ��game_��', True, cid=603)
def enableOnlyCustomHomeFounderDataTable():
    pass


@config(Bool, 'false', '�Ƿ�ʹ������2UI', True, cid=604)
def enableUIVersion2():
    pass


@config(Bool, 'true', '�Ƿ������������Ż�', True, cid=605)
def enableGuildQuestOptimize():
    pass


@config(Bool, 'true', '�Ƿ����᳤�Զ���λ', True, cid=606)
def enableGuildLeaderAutoResign():
    pass


@config(Bool, 'true', '�Ƿ����᳤�Զ���λ�ͻ������', True, cid=607)
def enableClientGuildLeaderAutoResign():
    pass


@config(Bool, 'true', '�Ƿ�����ս���Ʒ�BUFF', True, cid=608)
def enableWorldWarYoungServerBuff():
    pass


@config(Bool, 'true', '�Ƿ���ս�����Ʒ�BUFF', True, cid=609)
def enableBattleFieldYoungServerBuff():
    pass


@config(Bool, 'true', '�Ƿ������߼�¼����log')
def enableGenFubenLogOnLogOff():
    pass


@config(Bool, 'false', '�Ƿ���trap�⻷', True, cid=610)
def enableTrapAura():
    pass


@config(Bool, 'true', '�Ƿ������Ӷ��hub', False)
def enableMultipleHubs():
    pass


@config(Bool, 'false', '�Ƿ����̵�����ʾ�������', True, cid=611)
def enableQuestFlagInShop():
    pass


@config(Bool, 'false', '�Ƿ���������', True, cid=612)
def enableHallOfFame():
    pass


@config(Bool, 'true', '�Ƿ������log', True, cid=613)
def enablePrintBfDotaLog():
    pass


@config(Bool, 'false', '�Ƿ���hotfix/run_script/refreshData��popo����', True, cid=614)
def enablePopoReportOnServerHotfix():
    pass


@config(Bool, 'true', '�Ƿ�������������', True, cid=615)
def enableCareerGuilde():
    pass


@config(Bool, 'false', '�Ƿ���������������flag', True, cid=616)
def enableSpellAndGuideFlag():
    pass


@config(Int, str(int(time.time())), '�����᳤�Զ���λʱ��', True, cid=617)
def guildLeaderAutoResignEnableTime():
    pass


@config(Bool, 'false', '�Ƿ������˿ռ任������', True, cid=618)
def enablePersonalZoneSkin():
    pass


@config(Bool, 'true', '�Ƿ����ٷ���', True, cid=619)
def enableChickenFood():
    pass


@config(Bool, 'false', '�Ƿ���������뿪��', True, cid=620)
def enableTeamInvite():
    pass


@config(Bool, 'false', '�Ƿ����������', True, cid=621)
def enableGuildMassAstrology():
    pass


@config(Bool, 'false', '�Ƿ���US���ѱ�ǩ��ѯ', True, cid=622)
def enableFriendTag():
    pass


@config(Bool, 'false', '�Ƿ��������Ż', True, cid=623)
def enableMissTianyu():
    pass


@config(Int, '1504767540', '�����Ż��ֹʱ��', True, cid=624)
def missTianyuEndtime():
    pass


@config(Bool, 'false', '�Ƿ��������ð�ȫ������', True, cid=625)
def enableHallOfFameAll():
    pass


@config(Bool, 'false', '�Ƿ����������ȡ��������', True, cid=626)
def enalbeGetCompensationFromGUI():
    pass


@config(Bool, 'true', '����400*400��ͷ���ϴ�', True, cid=629)
def enableBigHeadSnapShot():
    pass


@config(Bool, 'false', '�Ƿ���Ѫ����', True, cid=630)
def enableHpMpPool():
    pass


@config(Bool, 'false', '�Ƿ����ڷֽ�װ��ʱԤ�Ȱ���')
def enablePeelBeforeDisassembleEquip():
    pass


@config(Bool, 'false', '�Ƿ���ʰȡʱ��������', False)
def enableQuestCheckOnPickItem():
    pass


@config(Bool, 'false', '�Ƿ����׻���Ӷ��', True, cid=631)
def enableWorldWarBattleYoungHire():
    pass


@config(Bool, 'false', '�Ƿ�������ȷ������������Ʒʱ�Զ��ƴ����ֵֿ�', True, cid=632)
def enableYunChuiScoreDikou():
    pass


@config(Bool, 'false', '�Ƿ�������ȷ������������Ʒʱ�Զ���ҵֿ�', True, cid=633)
def enableCoinDikou():
    pass


@config(Bool, 'true', '�Ƿ����������', True, cid=634)
def enableGuildIdentifyStar():
    pass


@config(Bool, 'true', '�Ƿ�����������������', True, cid=635)
def enableSkillHierogramShare():
    pass


@config(Bool, 'false', '�Ƿ����������ռ���ҵĿͻ�����������', True, cid=636)
def enableClientPerformanceFilter():
    pass


@config(Bool, 'true', 'states�����ӳ�һ֡��Ч', True, cid=637)
def enableStatesNextFrame():
    pass


@config(int, '-1', '�Ƿ���gatherInput����', True, cid=638)
def enableGatherInputCache():
    pass


@config(Bool, 'false', '�Ƿ����������������ݺ͵���', True, cid=639)
def enableHofHistoryAndStatue():
    pass


@config(Bool, 'false', '�Ƿ��ڸ߸��س���ͬ������Ŀ�����Ϣ', True, cid=641)
def enableTargetLockedUpdateInHighLoadScene():
    pass


@config(Bool, 'false', '�Ƿ���ʾ�����ð�ť', True, cid=642)
def enableHideHallOfFameBtn():
    pass


@config(Bool, 'false', '�Ƿ�����ֹ����������ض��񵥰�ť', True, cid=643)
def enableHallOfFameDisableTabBtn():
    pass


@config(Int, '0', 'ͬһ֡ͬһ��gfxValue���ô�����ֵ����������', True, cid=644)
def gfxValueLimitCall():
    pass


@config(Bool, 'false', '�Ƿ���hp��mp�㲥�Ż�', True, cid=645)
def enableHpMpOptimization():
    pass


@config(Bool, 'false', '�Ƿ�����ս�ٴ�Ѱ·����', True, cid=646)
def enableRestartPathFindAfterCombat():
    pass


@config(Bool, 'true', '�Ƿ���·��ػݻ��Ϊ�����ػݻ', True, cid=647)
def enableNewPlayerActivity():
    pass


@config(Float, '0.0', '�Ƿ��¼loadͼʱ��ĸ���', True, cid=648)
def propOfLogLoadSpaceTime():
    pass


@config(Bool, 'false', '�Ƿ�����Ʒ������', True, cid=649)
def enableUseItemWish():
    pass


@config(Int, '500000', 'PVP�������ֵ����')
def pvpHurtPopoThreshold():
    pass


@config(Bool, 'true', '��ϲ�ǹ���')
def enableMarriageShareCandy():
    pass


@config(Bool, 'true', '�Ƿ����ܻ�Ծ�ȹ���', True, cid=650)
def enableWeekActivation():
    pass


@config(Bool, 'false', '�Ƿ���С��ͼ���', True, cid=651)
def enableBfDotaMapMark():
    pass


@config(Bool, 'false', '�Ƿ����³ɾ�ϵͳ', True, cid=652)
def enableNewAchievement():
    pass


@config(Bool, 'false', '�Ƿ�����ͼ��ʱ�����', True, cid=653)
def enableItemUseFeedback():
    pass


@config(Bool, 'false', '�Ƿ�������IM�Ż�', True, cid=654)
def enableIMOptimize():
    pass


@config(Int, str(50), '�����ߵȼ�', True, cid=655)
def inviterLevel():
    pass


@config(Bool, 'false', '�Ƿ�����ϯ���ɴ���ӵ���ʵʱˢ�¹���', True, cid=656)
def enableRefreshShoolTopOneNpcModel():
    pass


@config(Bool, 'false', '�Ƿ��������ۼ�ǩ������', True, cid=657)
def enableNoviceCheckInReward():
    pass


@config(Bool, 'false', '�Ƿ������ᴫ��', True, cid=658)
def enableGuildInherit():
    pass


@config(Bool, 'true', '�Ƿ�������������', True, cid=659)
def enableGuildConsign():
    pass


@config(Bool, 'true', '�Ƿ�������������', True, cid=672)
def enableWorldConsign():
    pass


@config(Bool, 'true', '�Ƿ񹫻������������Ԥ���')
def enableWorldConsignPreOrder():
    pass


@config(Bool, 'false', '�Ƿ�����ְҵ', True, cid=660)
def enableNewSchoolSummon():
    pass


@config(Bool, 'false', '�Ƿ������߶Ծ�Ӣ��չʾ', True, cid=661)
def enableBfDotaHeros():
    pass


@config(Bool, 'false', '�Ƿ�����Ч����', True, cid=662)
def enableKeyboardEffect():
    pass


@config(Bool, 'false', '�Ƿ�����ϵͳ���㿪��ʱ��', True, cid=663)
def enableArenaPlayoffsTimeCalc():
    pass


@config(Bool, 'true', '�Ƿ�ſ�Ը�����Avatar��buff��������', True, cid=664)
def enableHighStateLimitInFuben():
    pass


@config(Bool, 'false', '�Ƿ������յ�¼����', True, cid=665)
def enableNoviceCheckInRewardOld():
    pass


@config(Bool, 'true', '�Ƿ���л���', True, cid=666)
def enableMarriage():
    pass


@config(Bool, 'true', '�Ƿ��������̵�', True, cid=667)
def enableDynamicShop():
    pass


@config(Bool, 'true', '�Ƿ����ܻ�Ծ����Ȩ����', True, cid=668)
def enableWeekPrivilegeBuy():
    pass


@config(Bool, 'true', '�Ƿ������ֱ�ӹ����ƴ�����', True, cid=669)
def enableBuyYunChuiCreditThroughCoin():
    pass


@config(Bool, 'false', '�Ƿ���CEF��ʱ����', True, cid=670)
def enableCEFOverTimeWarning():
    pass


@config(Bool, 'true', '�Ƿ������ϴ��Զ���ͼƬ', True, cid=671)
def enableNOSCustom():
    pass


@config(Bool, 'false', '�Ƿ�Ԥ����CEF', True, cid=673)
def enablePreOpenCEF():
    pass


@config(Bool, 'false', '���ս��AoI���޴�', True, cid=674)
def bfDotaAoIInfinity():
    pass


@config(Bool, 'false', '�Ƿ����ٷ��繫������', True, cid=675)
def enableGuildChickenMeal():
    pass


@config(Bool, 'true', '�Ƿ������������������', True, cid=676)
def enableGuildFishActivity():
    pass


@config(Bool, 'true', '�Ƿ����ķ�֮�ҹ�������', True, cid=677)
def enableGuildMonsterClanWar():
    pass


@config(Bool, 'true', '�Ƿ���ʹ�ø�����Ҽ���Ҳ��������ս', True, cid=678)
def enableRelivePlayerIsAttendCw():
    pass


@config(Bool, 'false', '�Ƿ����ø��˱���α���Ͷ��', True, cid=679)
def enableBoxProbabilityAdjustment():
    pass


@config(Bool, 'true', '�Ƿ����㲥��ȡ�����Ʒ', True, cid=680)
def enableGetItemTeamBroadcast():
    pass


@config(Bool, 'false', '����as�״��ϴ�', True, cid=681)
def enableReportASError():
    pass


@config(Bool, 'false', '���������鹦��', True, cid=682)
def enableFlowbackGroup():
    pass


@config(Bool, 'true', '�Ƿ����ػݻ-����չʾ������', True, cid=683)
def enablePreferentialActivity():
    pass


@config(Bool, 'true', '��������ǩ��', True, cid=684)
def enableGuildSignIn():
    pass


@config(Bool, 'true', '����������', True, cid=685)
def enableGuildRedPacket():
    pass


@config(Bool, 'true', '�Ƿ�������֮·��Ʒ�', True, cid=686)
def enableOperationActivity():
    pass


@config(Bool, 'true', '�Ƿ���������ʱbuffID���', True, cid=687)
def enableQuestTempStateId():
    pass


@config(Bool, 'false', '������������ְλ��ʾ', True, cid=688)
def enableShowGuildPrivilegesInChat():
    pass


@config(Bool, 'false', '�Ƿ��������̵���ҼƷ���־')
def enablePrivateShopMallBuyLog():
    pass


@config(Bool, 'true', '�Ƿ�������', True, cid=689)
def enableEngage():
    pass


@config(Bool, 'false', '�Ƿ�������Ƶ���Ż�')
def enableGuildChatOpt():
    pass


@config(Bool, 'true', '�Ƿ���ÿ�ո�����ֵ����', True, cid=690)
def enableDailyWelfareActivity():
    pass


@config(Bool, 'true', '�̳��Ƿ�֧��ֻ�۷ǰ����', cid=691)
def enableBuyMallItemOnlyUnbindCoin():
    pass


@config(Bool, 'true', '�Ƿ�ѹ����԰roomData')
def enableZipRoomData():
    pass


@config(Bool, 'true', '�Ƿ����ɽ������ʹ��״̬���')
def enableUseInteractiveObjectStateCheck():
    pass


@config(Bool, 'true', '�Ƿ������῾��', True, cid=692)
def enableGuildBonfire():
    pass


@config(Bool, 'false', '�Ƿ�������2����', True, cid=693)
def enablePushMessageV2():
    pass


@config(Bool, 'false', '�Ƿ���ս�����ջ', True, cid=694)
def enableBfTodayActivity():
    pass


@config(Bool, 'true', '�Ƿ���������ľ�����а�', True, cid=696)
def enableGuildYMF():
    pass


@config(Bool, 'true', '�Ƿ�����������������ս�͹������', True, cid=697)
def enableGuildTournamentLiveAndInspire():
    pass


@config(Bool, 'true', '�Ƿ������ԤԼϵͳ', True, cid=698)
def enableMarriageSubscribe():
    pass


@config(Bool, 'true', '�Ƿ������������̵�', True, cid=699)
def enableGuildCompositeShop():
    pass


@config(Bool, 'false', '�Ƿ���������', True, cid=700)
def enableWingWorld():
    pass


@config(Bool, 'false', '�Ƿ�׼�������ӹ�ս���ȵ�������')
def enableWorldWarToWingWorld():
    pass


@config(Bool, 'false', '�Ƿ���������������', True, cid=701)
def enableRemoveSkillEnhance():
    pass


@config(Bool, 'true', '�Ƿ����������������а񡢹������а���', True, cid=702)
def enableGuildSXY():
    pass


@config(Bool, 'true', '�Ƿ��������������а�', True, cid=703)
def enableGuildPrestigeTopRank():
    pass


@config(Bool, 'true', '�Ƿ������ս��������������', True, cid=704)
def enableClanWarOutputToGuildConsign():
    pass


@config(Bool, 'true', '�Ƿ����������̵깫��ȫ������', True, cid=705)
def enablePrivateShopGuildLimit():
    pass


@config(Bool, 'false', '�Ƿ��������翪��', True, cid=706)
def enableWingWorldOpenDoor():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�����ι���', True, cid=707)
def enableSummonedWarSpriteDisabledFun():
    pass


@config(Bool, 'false', '�Ƿ�������Ѱ���Ż�', True, cid=708)
def enableGuildMatchOptimize():
    pass


@config(Bool, 'false', '��ֹC_ui�����ʹ��', True, cid=709)
def disableCUIFont():
    pass


@config(Bool, 'false', '�Ƿ���ս���ս��ͳ��', True, cid=710)
def enableSpriteCombatStats():
    pass


@config(Bool, 'true', '�Ƿ�������ܻ�Ծ�ȴ�ɼӹ�������', True, cid=711)
def enableAddPrestigeByWeekActivation():
    pass


@config(Int, str(0), 'ս��ģ�������', True, cid=712)
def maxSpriteModelCnt():
    pass


@config(Bool, 'false', '�Ƿ������ᱦ��', True, cid=713)
def enableGuildLady():
    pass


@config(Bool, 'false', '�Ƿ������߶Ծ���Cell����', False)
def enableSingleCellMobaDotaSpace():
    pass


@config(Bool, 'false', '�Ƿ������ѧϰ����Ӧ��', True, cid=715)
def enableDeepLearningDataApply():
    pass


@config(Bool, 'true', '�Ƿ����������������ڶ����������������Ź�������', False)
def enableGtRoundTowRewardOnGconsignSale():
    pass


@config(Bool, 'true', '��������������ս���ͼ��', False)
def enableGtLiveTeleportCheck():
    pass


@config(Bool, 'false', '�����������۵������жϷ������¼�', False, 716)
def enableFbRequireItemByMileStoneId():
    pass


@config(Bool, 'true', '����Ƿ�ر�gmFollow', True, cid=717)
def enableCheckGmFollow():
    pass


@config(Bool, 'false', '�Ƿ������Avatar�ɼ��Լ��', True, cid=718)
def enableDotaAvatarVisibleCheck():
    pass


@config(Bool, 'false', '�Ƿ�����������ƥ�����', False, cid=720)
def enableArenaNewMatchRules():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=721)
def enableSkyWingChallenge():
    pass


@config(Bool, 'false', '�Ƿ�������������', True, cid=722)
def enableChatMultiLanguage():
    pass


@config(Bool, 'false', '���������һ�', True, cid=723)
def enableRewardRecovery():
    pass


@config(Bool, 'false', '�Ƿ��������һص�����ȫ������ʱ�俪��', True, cid=724)
def enableRewardRecoveryForServerOpTime():
    pass


@config(Bool, 'false', '�Ƿ�������ί���Ż�����', True, cid=725)
def enableSchoolEntrustOptimize():
    pass


@config(Bool, 'false', '�����ͻ��˽����һ����', True, cid=726)
def enableRewardRecoveryClient():
    pass


@config(Bool, 'true', '�������������̵��Զ�ˢ��', True, cid=727)
def enableGuildPrivateShopAutoRefresh():
    pass


@config(Bool, 'false', '����������Ҿ���', True, cid=728)
def enableGuildDonateWithCoin():
    pass


@config(Bool, 'false', '�Ƿ���������������֮ս', True, cid=729)
def enableGuildTournamentTraining():
    pass


@config(Bool, 'false', '�Ƿ񿪷�Ӣ����ϰ�', True, cid=730)
def enableSpriteMaterialBag():
    pass


@config(Bool, 'false', '�Ƿ񿪷Ź���NPC����', True, cid=731)
def enableGuildInheritByNpc():
    pass


@config(Bool, 'false', '�Ƿ�����ֵѭ������', True, cid=732)
def enableChargeRewardLoop():
    pass


@config(Bool, 'false', '�Ƿ�������������', True, cid=733)
def activitiesWeeklyReward():
    pass


@config(Bool, 'true', '�Ƿ񿪷ſ���ϵͳ', True, cid=734)
def enableCardSys():
    pass


@config(Bool, 'false', '�Ƿ����������߶Ծ�ģ�Ϳɼ���', True, cid=735)
def enableFixDotaModelVisible():
    pass


@config(Int, '0', '���������һ�κϷ���ʱ��', True, cid=736)
def serverLatestMergeTime():
    pass


@config(Bool, 'true', '�Ƿ������޻', True, cid=737)
def enableExchangeMysteryAnimal():
    pass


@config(Bool, 'false', '�Ƿ�������Esc���', True, cid=738)
def enableSystemSettingV2():
    pass


@config(Bool, 'false', '�Ƿ�������ʱ�����', True, cid=739)
def enableQuestTimerCheck():
    pass


@config(Bool, 'false', '�Ƿ����·����Ի', True, cid=740)
def enableNewServerTopRankAct():
    pass


@config(Str, '', '�����һغ�����,���ݽ������͹���,��Ӣ�Ķ��Ÿ���', True, cid=741)
def rewardRecoveryBlackList():
    pass


@config(Bool, 'false', '�Ƿ����չ���촰', True, cid=742)
def enableExtendChatBox():
    pass


@config(Bool, 'false', '�Ƿ�������ϲ�', True, cid=743)
def enableGuildMerger():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�����ܶ�ת��', True, cid=744)
def enableSummonedWarSpriteFamiliar():
    pass


@config(Bool, 'false', '�Ƿ�����Ʊ�һ�', True, cid=745)
def enableLotteryExchange():
    pass


@config(Bool, 'false', '�Ƿ������۱���', True, cid=746)
def enableExchangeMysteryBox():
    pass


@config(Bool, 'false', '�Ƿ���¼��')
def enableAnnalRecord():
    pass


@config(Bool, 'false', '�Ƿ���¼��ط�')
def enableAnnalReplay():
    pass


@config(Int, '10', '¼����ռ��')
def annalSnapshotInterval():
    pass


@config(Bool, 'false', '�Ƿ����·�������ʮ�󹫻�)', True, cid=750)
def enableNewServerGuildPrestige():
    pass


@config(Bool, 'false', '�Ƿ�����ɱ�ͽ�ʹ', True, cid=751)
def enableKillFallenRedGuard():
    pass


@config(Bool, 'true', '�Ƿ�����ɱ�ͽ�ʹǿ��PK')
def enableKillFallenRedGuardPK():
    pass


@config(Bool, 'false', '���������ٻػ', True, cid=752)
def enableFriendRecall():
    pass


@config(Float, '0.3', '�Ż�˲�ƺ��λ�Ƽ��ܣ�λ�ü��㲻�Ե�����', True, cid=753)
def teleportMoveDelayTime():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=754)
def enableLifeLink():
    pass


@config(Bool, 'false', '����Ԥ���Ź�ϵͳ', True, cid=755)
def enableGroupPurchase():
    pass


@config(Bool, 'false', '�Ƿ������������', True, cid=756)
def enableWingWorldArmy():
    pass


@config(Bool, 'false', '�������ģ��Ԥ����', True, cid=757)
def enableDotaZaijuPreLoad():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ������', True, cid=758)
def enableSummonedWarSpriteChat():
    pass


@config(Bool, 'false', '���������һ��¹�����', True, cid=759)
def enableRewardRecoveryNew():
    pass


@config(Bool, 'false', '������鼼��', True, cid=760)
def enableMarriageSkill():
    pass


@config(Bool, 'false', '�Ƿ��������������Ĺ��ܣ��������ǣ�', cid=761)
def enablePrestigeFlag():
    pass


@config(Bool, 'false', '����������5����ս��', False)
def enableIgnoreBFDotaCalc():
    pass


@config(Float, '3.2', '����ս�޸�����', cid=762)
def enableDotaFollowFix():
    pass


@config(Bool, 'false', '�Ƿ�����������������ȷ��', cid=763)
def enableFbTeamSchoolDoubleCheck():
    pass


@config(Bool, 'false', '�Ƿ������ѻع�V2', True, cid=764)
def enableSummonFriendV2():
    pass


@config(Bool, 'true', '�Ƿ���Զ�źŽ�', True, cid=765)
def enableYuanguLaba():
    pass


@config(Bool, 'true', '�Ƿ���ɱ�Ǳ�������ǰ��ս����', cid=766)
def enableShaXingEnterCombatEarlyReport():
    pass


@config(Bool, 'true', '�Ƿ�����ѡ���س齱����', cid=767)
def enableActivitySaleLottery():
    pass


@config(Bool, 'false', '�Ƿ�����F11���ع���', True, cid=769)
def enableF11Hide():
    pass


@config(Bool, 'true', '�Ƿ����ý�ɫ�����Ը�������')
def enableCreateCharacterIsInRenameList():
    pass


@config(Int, '0', '���ָ��idʵ��ļ���debug��Ϣ��info��־')
def debugSkillCalcEntId():
    pass


@config(Bool, 'false', 'ս����λְҵƽ��')
def enableBFJumpQueueRebalance():
    pass


@config(Bool, 'false', '������ű��������Ϳ���', True, cid=770)
def enableWingWorldAnimPush():
    pass


@config(Bool, 'false', '�������س齱�', True, cid=771)
def enableRandomLottery():
    pass


@config(Bool, 'false', '�鿴����Ӣ�鿪��', True, cid=772)
def enableSummonedSpriteOther():
    pass


@config(Bool, 'true', '�Ƿ�򿪼��ܺ����', True, cid=773)
def enableOpenSkillMacroEntry():
    pass


@config(Bool, 'false', '�Ƿ�����������ħ', True, cid=774)
def enableWingWorldXinMo():
    pass


@config(Str, '2,200', '�����������俪������')
def skyWingFbWindowsArgs():
    pass


@config(Bool, 'false', '�Ƿ���������̷�౶�ֿ�', True, cid=775)
def enableYaojingqitanCustomCost():
    pass


@config(Int, '3000', '�����������丱��ͬʱ������������')
def skyWingFbExistLimit():
    pass


@config(Bool, 'false', '�������س齱�-�Ż��߼�����', True, cid=777)
def enableRandomLotteryOptimize():
    pass


@config(Bool, 'false', 'ʢ�����񿪹�', True, cid=778)
def enableMarriageGreat():
    pass


@config(Bool, 'false', '��������չ����', True, cid=779)
def enableMarriageGuestExtend():
    pass


@config(Str, '1,10', '�����������丱�����ٴ���')
def skyWingFbDestoryArgs():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ��̽��', True, cid=781)
def enableExploreSprite():
    pass


@config(Bool, 'true', '�������佱��ͼ����ʾ', True, cid=782)
def enableItemBoxRewardShow():
    pass


@config(Bool, 'true', '�Ƿ����ڱ���globalMailBox��Ϣֱ��')
def enableGlobalMailBoxMsgOptimize():
    pass


@config(Bool, 'false', '�Ƿ����ƴ������ԣ�����嶥��', True, cid=783)
def enableQuizzes():
    pass


@config(Bool, 'true', '���������״̬��鱨������(���������������Է���)', True, cid=784)
def enableWingWorldCheckCityWarning():
    pass


@config(Bool, 'false', '�Ƿ������ܺ꽱��', True, cid=785)
def enableSkillMacroTopReward():
    pass


@config(Bool, 'false', '�Զ�¼����', True, cid=786)
def enableAutoTakeVideo():
    pass


@config(Bool, 'false', '��ͨ����ͻ��˿���', True, cid=787)
def enableNormalMarriage():
    pass


@config(Bool, 'false', '�Ƿ���NpcV2', True, cid=788)
def enableNpcV2():
    pass


@config(Bool, 'false', '��Ӫ����ֱ������������������ʾ', True, cid=789)
def enableLiveStreamingIcon():
    pass


@config(Int, '500', '�������ս��ͼ������������', True, cid=790)
def wingWorldWarCityMaxCount():
    pass


@config(Bool, 'false', '����������������', True, cid=791)
def enableAvoidDoingActivity():
    pass


@config(Bool, 'false', '������Ѻ��', True, cid=792)
def enableWingWorldYabiao():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ��ѱ��', True, cid=793)
def enableTrainingSprite():
    pass


@config(Bool, 'false', '�������������������')
def enableKoalaOrder():
    pass


@config(Int, '5', '��������������')
def koalaOrderQueryInterval():
    pass


@config(Int, '50', '��������һ������������Ŀ')
def koalaOrderQueryLimit():
    pass


@config(Bool, 'false', '�����ƺŵ�������', True, cid=794)
def enablePropTitle():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�鼼��ת��', True, cid=795)
def enableSpriteSkillTransfer():
    pass


@config(Bool, 'false', '�Ƿ�����ϡ��Ӣ��ת��', True, cid=796)
def enableSpriteRareTransfer():
    pass


@config(Bool, 'false', '�Ƿ�������Ӣ�����', True, cid=797)
def enableSpriteUpgrade():
    pass


@config(Bool, 'false', '����װ�����ѵ�serverConfig', True, cid=798)
def enableEquipJuexingServerConfig():
    pass


@config(Bool, 'false', '����ͨ�ð汾�������а�', True, cid=799)
def enableNewWmdRankListConfig():
    pass


@config(Bool, 'true', '�Ƿ�������������֮��', True, cid=800)
def enableWingWorldSoulBoss():
    pass


@config(Bool, 'false', '�Ƿ��������繫��ְλ����', True, cid=801)
def enableWingWorldGuildRoleOptimization():
    pass


@config(Bool, 'true', '�Ƿ����쳣���㱨��')
def enableErrorCombatCalcValueAlert():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ������', True, cid=802)
def enableSpriteGrowth():
    pass


@config(Bool, 'false', '�Ƿ���������Ӣ����Դ�ɼ�')
def enableWingWorldSpriteResCollect():
    pass


@config(Bool, 'false', '�Ƿ���ͳ��Ӣ���ֻس�������츳�Ĵ���')
def enableRecordBonusOccurrences():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�����ֻ�', True, cid=804)
def enableSpritePrayLunhui():
    pass


@config(Bool, 'false', 'ʱ��1�ĳ�ս����', True, cid=805)
def enableWingWarGroup1():
    pass


@config(Bool, 'false', 'ʱ��2�ĳ�ս����', True, cid=806)
def enableWingWarGroup2():
    pass


@config(Bool, 'false', 'ʱ��3�ĳ�ս����', True, cid=807)
def enableWingWarGroup3():
    pass


@config(Bool, 'false', '�Ƿ������ս����������˽���', True, cid=808)
def enableBFDotaCreationServerCalc():
    pass


@config(Bool, 'false', '�Ƿ���������ר�ü��ܷ���', True, cid=809)
def enableWingWorldSkillScheme():
    pass


@config(Int, '0', '(�ѷ�����ʹ���¿���enableWingCityDeclareList1)�����翪�ųǳ�����,��ֹ��ս�ĳ���Id��ʼ', True, cid=810)
def wingWorldCityDisableDeclareStart():
    pass


@config(Int, '0', '(�ѷ�����ʹ���¿���enableWingCityDeclareList1)�����翪�ųǳ�����,��ֹ��ս�ĳ���Id����', True, cid=811)
def wingWorldCityDisableDeclareEnd():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ���Զ���ս', True, cid=812)
def enableSpriteAutoCallOut():
    pass


@config(Bool, 'false', '�Ƿ���ְҵר��������������', True, cid=813)
def enablePvpEnhanceMaxCostNum():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�鼼����Ƕ', True, cid=814)
def enableSpriteSkillBeset():
    pass


@config(Bool, 'false', '�Ƿ�֧�ֿ��������������', True, cid=815)
def enableGuildAuctionCrossPush():
    pass


@config(Bool, 'false', '�Ƿ�������������ö�', True, cid=816)
def enableChatTopWhenLoading():
    pass


@config(Bool, 'false', '�����Ṧ�ظ��ٶȹ���', True, cid=817)
def enableRideWingShareEpRegen():
    pass


@config(Bool, 'false', '�Ƿ�����������')
def enableConditionalProp():
    pass


@config(Bool, 'false', '�Ƿ����°�ǩ������', True, cid=818)
def enableNewActivitySignin():
    pass


@config(Bool, 'false', '�Ƿ���ͳ��ÿ��ǩ���ۼƴ���')
def enableRecordDailySignIn():
    pass


@config(Bool, 'false', '�Ƿ�׼����������������', True, cid=819)
def enableWingWorldReady():
    pass


@config(Bool, 'false', '�Ƿ��ֹŷ��IP��¼')
def enableForbidIpOfEurope():
    pass


@config(Bool, 'true', '�Ƿ���cc����', True, cid=820)
def enableCCSpeak():
    pass


@config(Bool, 'false', '�Ƿ�ʹ���µ�Ӣ��ϴ�������')
def enableNewSpriteRerandRuleData():
    pass


@config(Bool, 'false', '�Ƿ���ͣ����ϲ�����')
def enablePauseApplyGuildMerger():
    pass


@config(Bool, 'false', '�Ƿ�ʹ������������������')
def enableNewAddDaoHengType():
    pass


@config(Bool, 'false', '�Ƿ��ֹ��ͨ�û���½������')
def enableWingWorldForbidLogin():
    pass


@config(Bool, 'false', '�Ƿ�������ģʽ��Ʒ����������', True, cid=821)
def enableAuctionItemWhiteList():
    pass


@config(Bool, 'false', '�Ƿ������������ְҵ��������������', True, cid=822)
def enableNewSchoolMiaoyin():
    pass


@config(Bool, 'false', '�Ƿ������߶Ծ��ٱ�����', True, cid=823)
def enableDotaBFVote():
    pass


@config(Bool, 'false', '�Ƿ���ʾ���Ѫ������', True, cid=824)
def enablePlayerHpTxtVisible():
    pass


@config(Bool, 'true', '�Ƿ�������Ѱ���ڶ����Ż�', True, cid=825)
def enableGuildMatchOptimizeSecond():
    pass


@config(Bool, 'true', '�Ƿ�����������¯', True, cid=826)
def enableWingWorldForge():
    pass


@config(Bool, 'true', '�Ƿ����������ս�ؾ߽���', True, cid=827)
def enableWingWorldCarrierBuild():
    pass


@config(Bool, 'true', '����л���ϻ�����Ƿ��������')
def enableCrossSetCardEquipSlot():
    pass


@config(Str, '', '������ʱ��1������ս�ĳǳأ��Զ�������񣬱���1,2,3', True, cid=829)
def enableWingCityDeclareList1():
    pass


@config(Str, '', '������ʱ��2������ս�ĳǳأ��Զ�������񣬱���1,2,3', True, cid=830)
def enableWingCityDeclareList2():
    pass


@config(Str, '', '������ʱ��3������ս�ĳǳأ��Զ�������񣬱���1,2,3', True, cid=831)
def enableWingCityDeclareList3():
    pass


@config(Bool, 'true', '�Ƿ�����ü�ͬʱװ���ڶ����ϻ', True, cid=832)
def enableCardEquipInMutiSlots():
    pass


@config(Bool, 'false', '�Ƿ����¶���ս������ʯ������ս��', True, cid=833)
def enableNewFlagBF():
    pass


@config(Bool, 'false', '�Ƿ����¶���ս�����ƥ��', True, cid=1031)
def enableNewFlagBFCrossMatch():
    pass


@config(Bool, 'false', '�Ƿ������߶Ծ���ֹ��ͬ�豸����')
def enableDotaCheckMac():
    pass


@config(Bool, 'false', '�ڷ��ر����ɫ����������վ����')
def cbgRolePassHttpReq():
    pass


@config(Bool, 'false', '�ڷ��ر����ɫ���������������', True, cid=899)
def cbgRolePassConditions():
    pass


@config(Bool, 'false', '�ر����ɫ����֪ͨ�ͷ�����Ϣ����')
def enableCBGRoleMsg():
    pass


@config(Bool, 'false', '�������ģ��')
def enableCharTemp():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=834)
def enableFightForLove():
    pass


@config(Bool, 'true', '�Ƿ���ƽ�⾺����', True, cid=835)
def enableBalanceArena():
    pass


@config(Int, '60', '���߶Ծ��ٱ�ʱ����')
def dotaBattleFieldReportInterval():
    pass


@config(Bool, 'true', '�Ƿ������޸�ģ��', True, cid=836)
def enableChangeCharTemp():
    pass


@config(Bool, 'true', 'ģ���Ƿ�ʱ�Ӽ�����')
def enabelFakeCharTempData():
    pass


@config(Bool, 'false', ' �Ƿ�����ʱ�����ֵ��־���')
def enableMonitorRoleValLog():
    pass


@config(Bool, 'false', '�������ƻ', True, cid=900)
def enableRandomTurnOverCard():
    pass


@config(Bool, 'false', '�Ƿ�ֻ������������ʹ�ý�ɫ����', True, cid=837)
def enableCBGRoleWhiteList():
    pass


@config(Bool, 'false', '�Ƿ�Ĭ�ϱ���ָ�����Ѳ����ϼܽ�ɫ', True, cid=901)
def enableCBGRoleDefaultFriendTarget():
    pass


@config(Bool, 'false', '�Ƿ���벻ָ�����Ѳ����ϼܽ�ɫ', True, cid=902)
def enableCBGRoleNotFriendTarget():
    pass


@config(Bool, 'false', '�Ƿ���������Ϸ��ԱȨ��', True, cid=838)
def enableNeteaseGameMembershipRights():
    pass


@config(Bool, 'true', '�Ƿ���ƽ�⾺������λ������ȡ', True, cid=839)
def enableDuanWeiAwardBalance():
    pass


@config(Bool, 'false', '�Ƿ������ȡ�������ܽ���', True, cid=840)
def enableArenaWeeklyAward():
    pass


@config(Bool, 'false', '�Ƿ������ȡƽ�⾺�����ܽ���', True, cid=841)
def enableArenaWeeklyAwardBalance():
    pass


@config(Bool, 'true', '�Ƿ�����ύģ��', True, cid=842)
def enableCommitCharTemp():
    pass


@config(Bool, 'false', '�Ƿ����ر����ɫ������Ӫ����')
def enableCBGRoleAward():
    pass


@config(Bool, 'false', '�Ƿ���������ϯ�淨', True, cid=843)
def enableSchoolTopMatch():
    pass


@config(Str, '2,50', '���ú�ʯ��ս����������')
def newFlagBFWindowsArgs():
    pass


@config(Bool, 'false', '�Ƿ����Ʊ�����������')
def enableBuyCoinRobot():
    pass


@config(Bool, 'false', '�Ƿ���һ����װ', True, cid=844)
def enableOneKeyConfig():
    pass


@config(Bool, 'false', '�Ƿ���ȫ���̻�', True, cid=846)
def enableFullScreenFireworks():
    pass


@config(Bool, 'false', '�Ƿ������ھ�����׼���ع�(701)������', cid=845)
def enableGroupOnBalanceReadyRoom():
    pass


@config(Bool, 'false', '��ϻ�л�����', True, cid=847)
def enableChangeCardSuit():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ���λ��չ', True, cid=848)
def enableExpandSpriteSlot():
    pass


@config(Bool, 'false', '�Ƿ���������ͬ������ģ������(�ǵ�ǰģ��)', True, cid=849)
def syncAllCharTempInfoToHezuofu():
    pass


@config(Bool, 'false', '�Ƿ�����ʱװ��λ', True, cid=850)
def enableFashionCapeSlot():
    pass


@config(Bool, 'true', '�Ƿ�������ұ��棬ʹ��ģ�巽��', True, cid=851)
def enableCharTempScheme():
    pass


@config(Bool, 'false', '�Ƿ���ʹ��ָ�����߽��о�������', True, cid=852)
def enableReforgeEquipJuexingWithItem():
    pass


@config(Bool, 'false', '�Ƿ���˫�˾�����', True, cid=853)
def enableDoubleArena():
    pass


@config(Bool, 'false', '�Ƿ�����˫�˾���������ս��ְҵ���')
def enableDoubleArenaSchoolCheck():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ����������', True, cid=854)
def enableRecoverSpriteGrowth():
    pass


@config(Bool, 'true', '�Ƿ�����ʷ���ѷ����', True, cid=855)
def enableHistoryConsumed():
    pass


@config(Bool, 'false', '�Ƿ����������', True, cid=912)
def enableSkillAppearance():
    pass


@config(Bool, 'false', '�Ƿ�������ڻ�淨', True, cid=913)
def enableWingCelebrationActivity():
    pass


@config(Str, '', '�Ƿ����·����0Ѱ�龭�� 1�·����� 2�¹���ϻ 3ʮ�󹫻� 4ս������ 5�ȼ����� 6�����۷� 7�������� 8������ɱ 9�������� 10���˵�ͷ 11�������У�������1,2,3', True, cid=914)
def enableNewServerActivity():
    pass


@config(Bool, 'false', '�Ƿ�������������', True, cid=915)
def enableWingWorldHistoryBook():
    pass


@config(Bool, 'false', '�Ƿ��޸����Ƴ��������б��ɫ��Ŀ��ʾ�Ƴ�', True, cid=916)
def enableFixOldRoleNumError():
    pass


@config(Bool, 'false', '�Ƿ����ر����������')
def enableSecondStageDataCBG():
    pass


@config(Bool, 'false', '�Ƿ����ü�ָ��ϴ��', True, cid=917)
def enableCardSpecialChange():
    pass


@config(Bool, 'false', '�Ƿ���������������', True, cid=918)
def enableArenaScore():
    pass


@config(Bool, 'false', '�Ƿ����·�������⽱����', True, cid=919)
def enableTreasureBoxExtraBonus():
    pass


@config(Bool, 'false', '�Ƿ�����������ʱ�������ܵ���', True, cid=920)
def enableArenaTempPskills():
    pass


@config(Bool, 'false', '�Ƿ����鿴��ϸ���갴ť', True, cid=921)
def enableSummonedWarSpriteEffect():
    pass


@config(Bool, 'false', '�Ƿ�����ƽ�⾺�����������', True, cid=922)
def enableBalanceArenaFinalResult():
    pass


@config(Bool, 'false', '�Ƿ�������camera', True, cid=923)
def enableNewCamera():
    pass


@config(Bool, 'false', '�Ƿ����ͻ���log��ӡ�ֲ�����', True, cid=924)
def enableClientLogPrintLoacalVars():
    pass


@config(Bool, 'true', '�Ƽ��Ƿ񷵻�ӳ��֮��', True, cid=925)
def enableCardReturnBossItem():
    pass


@config(Bool, 'false', '�Ƿ�����������չС��ͼ', True, cid=926)
def enableWingWorldMap():
    pass


@config(Bool, 'false', '�Ƿ�����CronStrת��list��ʽ', True, cid=927)
def enableParseCronStr2List():
    pass


@config(Bool, 'false', '�Ƿ������鹦�����һҳ', True, cid=928)
def enableEquipSoulNewest():
    pass


@config(Bool, 'false', '�Ƿ�����������ǿ������', True, cid=929)
def enableEquipChangeJuexingStrength():
    pass


@config(Bool, 'false', '�Ƿ���������ϯ�������', True, cid=930)
def enableSchoolTopTestFuben():
    pass


@config(Bool, 'false', '�Ƿ������ս������ս��', True, cid=931)
def enableUpBFRegion():
    pass


@config(Bool, 'false', '�Ƿ���������ս', True, cid=932)
def enableCrossClanWar():
    pass


@config(Bool, 'true', '����������ʱ�Ƿ������Զ����', True, cid=933)
def enableAutoBuildArenaScoreTeam():
    pass


@config(Bool, 'true', '�Ƿ�ʹ�ù�ʽ���ü��㾺��������', True, cid=934)
def enableFormulaValue():
    pass


@config(Bool, 'false', '�ͻ���˫�˾������Ƿ���ս��', True, cid=935)
def enableDoubleArenaZhanBao():
    pass


@config(Bool, 'false', '�Ƿ�������ͨ������', True, cid=936)
def enableFTB():
    pass


@config(Bool, 'true', '�ͻ���˫�˾�����16ǿ�Ƿ���ս��', True, cid=937)
def enableDoubleArena16QiangZhanBao():
    pass


@config(Bool, 'false', '�ͻ����Ƿ����ؾ�����tabҳ', True, cid=938)
def hidePvpArenaPanel():
    pass


@config(Bool, 'false', '�Ƿ���˫�˾�������ս����', True, cid=939)
def enableDoubleArenaAnnal():
    pass


@config(Bool, 'false', '�Ƿ���ƽ�⾺���������صǹ���', True, cid=940)
def enableBalanceReLogon():
    pass


@config(Bool, 'true', 'npc3dͷ���Ż�', True, cid=941)
def enableLargePhotoSize():
    pass


@config(Bool, 'true', '�Ƿ���ƽ�⾺������ֹ��ͬ�豸����')
def enableBalanceArenaCheckMac():
    pass


@config(Str, '5,1,100000,100000', '��ս����ͳ��ͬ������(1.ͬ�����2.ͬ����ɱ��ֵ3.ͬ���˺���ֵ4.ͬ��������ֵ)')
def syncClanWarStatsParams():
    pass


@config(Bool, 'false', '�Ƿ���նħ������', True, cid=942)
def enableZMJFuben():
    pass


@config(Bool, 'true', '�Ƿ񿪶��ߺ��ֹ�ؽ�ƽ�������', True, cid=943)
def enableNoRenterPlayoffs():
    pass


@config(Bool, 'false', '�Ƿ���ģ�͡���Ч�͵�ͼ���ʵļ���ͳ��', True, cid=944)
def enableMaterialLoadStatistics():
    pass


@config(Bool, 'false', '�Ƿ�ͨ������', True, cid=945)
def enableGeneralPush():
    pass


@config(Bool, 'false', '�Ƿ���ȫ����Ʊ�', True, cid=946)
def enableGlobalLottery():
    pass


@config(Bool, 'false', '�Ƿ����°��ظ����߱���')
def enableDuplicateItemReportV2():
    pass


@config(Bool, 'false', '�Ƿ�����սͨ��֤', True, cid=947)
def enableChallengePassport():
    pass


@config(Bool, 'false', '�Ƿ���ʾ����������ι���', True, cid=948)
def enableSkillAppearanceBlock():
    pass


@config(Bool, 'false', '�Ƿ����ӳ����Լ��㹦�ܣ���ͬ�������е����Լ��㽵��һ�Σ�')
def enableDeferredPropCalc():
    pass


@config(Bool, 'true', '����������µļ��', True, cid=949)
def enableCheckBelowTerrain():
    pass


@config(Bool, 'false', '�Ƿ���Avatar spaceType,fbNo,fbType����')
def enableCacheSpaceType():
    pass


@config(Bool, 'false', '�Ƿ���ȫ��Ѱ��ɱ��˫������', True, cid=950)
def enableGlobalExpBonus():
    pass


@config(Bool, 'true', '�Ƿ�����ЧLRU����', True, cid=951)
def enableLRUCache():
    pass


@config(Bool, 'false', '�Ƿ���Զ���Ž�', True, cid=952)
def enableCrossClanWarLaba():
    pass


@config(Bool, 'false', '�Ƿ���������ս��ϵ�ж�', True, cid=953)
def enableCrossClanWarRelation():
    pass


@config(Bool, 'false', '�Ƿ������ḱ��', True, cid=954)
def enableGuildFuben():
    pass


@config(Bool, 'false', '�Ƿ����¹�ϵͳ(��ʱװ���)', True, cid=955)
def enableWardrobe():
    pass


@config(Bool, 'false', '�Ƿ���5v5�����', True, cid=957)
def enablePlayoffs5V5():
    pass


@config(Bool, 'false', '�Ƿ����°�������', True, cid=958)
def enableNewEmotionPanel():
    pass


@config(Bool, 'false', '�Ƿ������ս��Ӣ��ս', True, cid=959)
def enableClanWarChallenge():
    pass


@config(Bool, 'false', '�Ƿ����¹�ϵͳ��ʱװ����װѡ�ע�ⲻ���¹���俪�أ�', True, cid=960)
def enableWardrobeSuitShow():
    pass


@config(Bool, 'false', '�Ƿ�������Ὰѡ����', True, cid=961)
def enablePlayoffsVoteLuckyBag():
    pass


@config(Bool, 'false', '�Ƿ�������', True, cid=962)
def enableFlyUp():
    pass


@config(Bool, 'false', '�Ƿ����¹�ϵͳ����Ⱦɫ��������', True, cid=963)
def enableWardrobeMultiDyeScheme():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�þ��ȷֲ���findRandomNeighbourPoint')
def enableSquareFindRandomNeighbourPoint():
    pass


@config(Bool, 'false', '�Ƿ��������ս������������ʹ��ս��')
def enableSummonedSpriteInCWAndWMD():
    pass


@config(Bool, 'false', '�Ƿ�������Ϊ�����')
def enableBehaviorStub():
    pass


@config(Bool, 'false', '�Ƿ������������Զ�ѡ����AI')
def enableSelectDirectionByEnemyNum():
    pass


@config(Bool, 'false', '�Ƿ����¹�ϵͳ�Զ�����书��', True, cid=964)
def enableWardrobeScheme():
    pass


@config(Bool, 'false', '�Ƿ�����PUPPET')
def enablePuppet():
    pass


@config(Int, '500', 'PUPPETͬʱ������������')
def puppetNumLimit():
    pass


@config(Bool, 'false', '�Ƿ����ƽ��Ա������ݴ���PUPPET')
def enableOnlyLocalPuppet():
    pass


@config(Str, '', '��ֹ����Щ���������PUPPETԭ���������')
def puppetExcludeHosts():
    pass


@config(Bool, 'false', '�Ƿ����µ�ս����ɱͳ��')
def enableBattleFieldNewStats():
    pass


@config(Bool, 'false', '�Ƿ���������������ɴ����ս')
def enableClanWarInSelfAndCross():
    pass


@config(Bool, 'false', '������񱳰�', True, cid=965)
def enableHierogramBag():
    pass


@config(Bool, 'false', '���������2019.3�汾)', True, cid=966)
def enableNewHierogram():
    pass


@config(Bool, 'false', '�����ת�����(2019.03��������)', True, cid=967)
def enableTransToNewHierogram():
    pass


@config(Bool, 'false', '�����(2019.03��������)ת�����', True, cid=968)
def enableTransBackOldHierogram():
    pass


@config(Bool, 'false', '�Ƿ������սȫ������', True, cid=969)
def enableGlobalClanWar():
    pass


@config(Bool, 'false', '�Ƿ������Է����պŽǡ��������͡����������', True, cid=970)
def enableReceiveMsgInRegionServer():
    pass


@config(Bool, 'false', '�Ƿ���������սԤ�Ȼ', True, cid=971)
def enableCrossClanWarPreActivity():
    pass


@config(Bool, 'false', 'תְ����������<=1200����', True, cid=972)
def enableTransSchoolArenaScoreLimit():
    pass


@config(Bool, 'false', '���ḱ��˽�����������ж�')
def enableGuildFubenNoCheck():
    pass


@config(Bool, 'false', '�Ƿ���װ������-���', True, cid=973)
def enableEquipChangeRune():
    pass


@config(Bool, 'false', '�Ƿ���˽����������սʱ��')
def enableClanWarNoCheck():
    pass


@config(Bool, 'false', '���������ų�ʱ����Ƿ�͵������ƥ��')
def enableHybridSoloTeam():
    pass


@config(Bool, 'false', '��Ա����Ӹ���״̬�Զ�����', True, cid=974)
def enableAutoTeleportInFollow():
    pass


@config(Bool, 'false', '�ŶӸ���', True, cid=975)
def enableNewGroupFollow():
    pass


@config(Bool, 'false', '��Ӹ����ٻ���Ա����', True, cid=976)
def enableCallTeamMember():
    pass


@config(Bool, 'false', '˽���ڷ�������ս�����')
def enableIgnoreFlyUpGroupCheck():
    pass


@config(Bool, 'true', '�����ʱ����ʾ��ҹ���ͼ��', True, cid=977)
def enableCrossServerGuildIcon():
    pass


@config(Bool, 'false', '�Ƿ�3v3���������ܳ���3������Ӫ')
def enable3v3SoloLingLongLimit():
    pass


@config(Bool, 'false', '�Ƿ���ʱװ���˻ر�������', True, cid=978)
def enableWardrobeReturn():
    pass


@config(Bool, 'false', '�Ƿ����·�ͨ��֤(����������ͨ��֤)', True, cid=979)
def enableNewServerChallengePassport():
    pass


@config(Bool, 'false', '�Ƿ���նħ��Эս����', True, cid=980)
def enableZMJAssist():
    pass


@config(Bool, 'false', '�Ƿ���ʱװ���������Ĳ���', True, cid=981)
def enablePutMoreItCategoryIntoFashionBag():
    pass


@config(Bool, 'false', '�Ƿ�������ͨ������', True, cid=982)
def enableFtbPaimai():
    pass


@config(Bool, 'false', '�Ƿ��������һ�ת������', True, cid=983)
def enableExchangeHierogram():
    pass


@config(Bool, 'false', '�Ƿ������Ⱦɫ', True, cid=984)
def enableRandomDye():
    pass


@config(Bool, 'false', '�Ƿ���װ��������ӡ-�ϳ�', True, cid=985)
def enableEquipChangeGemLvUp():
    pass


@config(Bool, 'false', '�Ƿ���SQLע����')
def enableCheckSqlInjectionCodes():
    pass


@config(Bool, 'false', '�Ƿ������ᾫӢ����(�����ؾ�.��ս)��������������', True, cid=986)
def enableGuildFubenTopReward():
    pass


@config(Bool, 'false', '�Ƿ��������������ָ��������ɾ���ӹ���', False, cid=987)
def enableGuildGrowthVolumnMaxAchieveCheck():
    pass


@config(Bool, 'false', '�Ƿ������ḱ����ս', True, cid=988)
def enableGuildFubenObserve():
    pass


@config(Bool, 'false', '�Ƿ���������ҩ����', True, cid=989)
def enableGuildPotionProduct():
    pass


@config(Bool, 'false', '�Ƿ���������֮ս�Ŷӻ���', True, cid=990)
def enableWingWorldWarQueue():
    pass


@config(Bool, 'false', '�Ƿ���������ս�Ż�')
def enableGuildChallengeEx():
    pass


@config(Int, '-1', '���ḱ����ս����')
def guildFubenObserveNum():
    pass


@config(Bool, 'false', '�Ƿ���ս��������', True, cid=991)
def enableBattleFieldPuppet():
    pass


@config(Bool, 'false', '�Ƿ����������֮�����а�', True, cid=992)
def enableGuildNewFlag():
    pass


@config(Bool, 'false', '�Ƿ������������־', True, cid=993)
def enableWingWorldFengWuZhi():
    pass


@config(Bool, 'false', '�Ƿ��������ӳٿ��źͷ���������ӳ�����', True, cid=994)
def enableServerExpAddLimit():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�÷���ͨ������������url', True, cid=995)
def enableFtbAuctionTestUrl():
    pass


@config(Bool, 'false', '�Ƿ��������������ֽ���', True, cid=996)
def enableGuildGrowthScoreReward():
    pass


@config(Bool, 'false', '�Ƿ���ʹ����Ʒ������������')
def enableUseItemStartGuildConsign():
    pass


@config(Bool, 'false', '�����쳣�Ƿ�������Ⱥ����')
def enableAddFishGroupNumWhenFail():
    pass


@config(Bool, 'true', '����״̬��μ��(����, �Զ�)')
def enableFishMultiCheck():
    pass


@config(Bool, 'false', '���ḱ���Զ��߳������������', True, cid=997)
def enableGuildFubenKickMember():
    pass


@config(Bool, 'false', '���ḱ�������Ż������޸Ľ�ʬ�����״̬')
def enableScheduleActiveGuildFuben():
    pass


@config(Bool, 'false', '�Ƿ���ͷ�����', True, cid=999)
def enablePhotoBorder():
    pass


@config(Bool, 'false', '�Ƿ�������Ȧ', True, cid=1000)
def enablePYQ():
    pass


@config(Bool, 'false', '�Ƿ������ս������ҳ', True, cid=1001)
def enableCrossBFSkillScheme():
    pass


@config(Bool, 'false', '�Ƿ������߶Ծ�ƥ��Լ���Ż�')
def enableDotaBFGenHybirdLimitOpt():
    pass


@config(Bool, 'false', '�Ƿ������ս�Ż�', True, cid=1002)
def enableClanWarOptimization():
    pass


@config(Bool, 'false', '�Ƿ�������������', True, cid=1006)
def enableFbAvoidDieItem():
    pass


@config(Bool, 'false', '�Ƿ������͵�gm�������', True, cid=1003)
def enableTransToGmServer():
    pass


@config(Bool, 'false', '�Ƿ����߼��������', True, cid=1004)
def enableRuneSuperExchange():
    pass


@config(Bool, 'false', '�Ƿ������̳ǵ����׻�Ա����', True, cid=1005)
def hideNeteaseGameMembershipMall():
    pass


@config(Bool, 'false', '�Ƿ���ս����ƽ�⣨����ͱ�����', True, cid=1007)
def enableCrossBattleFieldRebalance():
    pass


@config(Bool, 'false', '�Ƿ�����Ӫ���δʿ�SDK����', True, cid=1008)
def enableEnvSDK():
    pass


@config(Bool, 'false', '�Ƿ����������ȼ����ӳ�(��ģʽ��', True, cid=1009)
def enableServerExpAddNew():
    pass


@config(Bool, 'false', '�Ƿ����ֻ����򸱱�', True, cid=1010)
def enableTeamEndless():
    pass


@config(Bool, 'false', '�Ƿ��������Ķ������', True, cid=1011)
def enableFreeRecoverSpriteGrowth():
    pass


@config(Bool, 'false', '�Ƿ����ü�����չ', True, cid=1012)
def enableCardSlotExtend():
    pass


@config(Bool, 'true', '�Ƿ��þ���ȼ��ж�ָ��ģʽ', True, cid=1013)
def enableGuideModeWithXiuweiLv():
    pass


@config(Bool, 'true', '�Ƿ�����ʹ�þ��鵤', True, cid=1014)
def enableBuffExp():
    pass


@config(Bool, 'false', '�Ƿ��ǿ���������ļ��')
def enableEnterTeleportEnhanceCheck():
    pass


@config(Bool, 'false', '�Ƿ���buff��ع���', True, cid=1015)
def enableBuffListener():
    pass


@config(Bool, 'false', '�Ƿ�������Ǯ��', True, cid=1016)
def enableFtbWallet():
    pass


@config(Bool, 'true', '���õ����configName[1]', True, cid=1017)
def enableConfigNameOneForBonus():
    pass


@config(Bool, 'false', '�Ƿ�������׷������', True, cid=1018)
def enableExpPursueGuide():
    pass


@config(Bool, 'false', '�Ƿ�ͳ��ս����������')
def enableStatsCombatScoreType():
    pass


@config(Bool, 'false', '�����������')
def enableArenaPlayoffsRedPacket():
    pass


@config(Bool, 'false', '���˿ռ�����濪��', True, cid=1019)
def enablePersonalZoneV2():
    pass


@config(Bool, 'false', '�Ƿ���Ϯ��¼�������')
def enablePropLogOnWeakerProtect():
    pass


@config(Bool, 'false', '��ǿ��ǿ�����������޸�')
def enableAtkAndDefAdjust():
    pass


@config(Bool, 'false', '�Ƿ������ս�Ż�_ս��', True, cid=1020)
def enableClanWarOptimizationRecord():
    pass


@config(Bool, 'false', '�Ƿ������ս�Ż�_�¼�', True, cid=1021)
def enableClanWarOptimizationEvent():
    pass


@config(Bool, 'false', '�Ƿ������ս�Ż�_����', True, cid=1022)
def enableClanWarOptimizationSkill():
    pass


@config(Bool, 'true', '�Ƿ���showBroodLabel�Ż�', True, cid=1023)
def enableOptimizeShowBroodLabel():
    pass


@config(Bool, 'false', '�Ƿ�������Ȧ����', True, cid=1024)
def enableNewPYQ():
    pass


@config(Bool, 'false', '�Ƿ������֮��ս��', True, cid=1025)
def enableCqzzBf():
    pass


@config(Bool, 'false', '�Ƿ�������ս��', True, cid=1026)
def enableRaceBattleField():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=1027)
def enableChatGroup():
    pass


@config(Bool, 'false', 'Ӣ�鴫��ǰ���Ŀ����Ƿ��ڵ�ͼ��Χ��')
def enableSpriteTeleportCheck():
    pass


@config(Bool, 'false', '�Ƿ����������Ż', True, cid=1028)
def enableNewMissTianyu():
    pass


@config(Bool, 'false', '�Ƿ������ѽ���Ӣ�鴫��', True, cid=1029)
def enableUnlockSpriteBioInMoney():
    pass


@config(Bool, 'false', '�������Ƴ鿨�', True, cid=1030)
def enableRandomCardDraw():
    pass


@config(Bool, 'false', '�Ƿ����������ܵĹ̶�����ת��')
def enablePskillPropTransferProp():
    pass


@config(Bool, 'false', '�Ƿ�������Ч��', True, cid=1032)
def enableLingShi():
    pass


@config(Bool, 'false', '�Ƿ�����Ӫ���δʿ�SDK log(��Ҫ����enableEnvSDK)', True, cid=1033)
def enableEnvSDKLog():
    pass


@config(Bool, 'true', '�Ƿ���ǿ����Ҹ���(�Ƿ�����)', True, cid=1034)
def enableForceRoleRename():
    pass


@config(Bool, 'false', '����ȡ��֧�����', True, cid=1035)
def enablePayMailCoin():
    pass


@config(Bool, 'false', '�Ƿ�������Ȧ����', True, cid=1036)
def enablePYQTopic():
    pass


@config(Bool, 'false', '��ӡ����(���ƣ����¶���)', True, cid=1037)
def enableGuanYinThirdPhase():
    pass


@config(Bool, 'false', 'ͬһmac��ַ�ع���ӡ����')
def enableSameMacAddressWarning():
    pass


@config(Bool, 'false', '�Ƿ��������Ƽ����', True, cid=1038)
def enableActivityGuide():
    pass


@config(Bool, 'false', '�Ƿ���������������ϵͳ(������ϵͳ����)', True, cid=1039)
def enableSkillXiuLianScore():
    pass


@config(Bool, 'false', '��������������㳡����Ҫ������ơ��˺�Ҫ��', True, cid=1040)
def enableBalanceArenaWeekCntLimit():
    pass


@config(Bool, 'false', '�Ƿ���ͨ��֤��������')
def enableNewServerReissueBonus():
    pass


@config(Bool, 'false', '�Ƿ�����ӡ��װ������', True, cid=1041)
def enableSplitWenYinFromEquip():
    pass


@config(Bool, 'false', '�Ƿ�����������������')
def enableCreationDestroyByDistance():
    pass


@config(Bool, 'false', '�ü�ϴ���෽��', True, cid=1042)
def enableCardWashScheme():
    pass


@config(Bool, 'false', '�Ƿ��������濪����������', True, cid=1043)
def enableShiwanPublicServerPYQ():
    pass


@config(Bool, 'false', '���������������Եȼ�����', True, cid=1044)
def enableGuildGrowthRegress():
    pass


@config(Bool, 'false', '�Ƿ���ս����������', True, cid=1045)
def enableBattleFieldFame():
    pass


@config(Bool, 'false', '�Ƿ��µķ���Ǯ���ӿ�', True, cid=1046)
def enableFtbWalletV2():
    pass


@config(Bool, 'false', '�Ƿ�ʹ���µķ���ͨ���ڿ�ӿ�', True, cid=1047)
def enableFtbV2():
    pass


@config(Bool, 'false', '�Ƿ����ø�ְҵ', True, cid=1048)
def enableSecondSchool():
    pass


@config(Bool, 'false', '�Ƿ���hot��buff�����ı�ʱˢ��״̬hijack����')
def enableRefreshHijackOnHotStateAddLayer():
    pass


@config(Bool, 'false', '�Ƿ���dot��buff�����ı�ʱˢ��״̬hijack����')
def enableRefreshHijackOnDotStateAddLayer():
    pass


@config(Bool, 'false', '�Ƿ�����������������չ', True, cid=1049)
def enablePskillExtraAttr():
    pass


@config(Bool, 'false', '�Ƿ��Զ��������������������')
def enableAutoClearGTNScore():
    pass


@config(Bool, 'false', '�����紫���Ƿ�ӵȼ�����')
def enableWingWorldTeleportLvCheck():
    pass


@config(Bool, 'false', '�����紫���Ǽӵȼ�����')
def enableWingWorldTeleportLvWaring():
    pass


@config(Str, '0, 0', '������ʱ������ͳ�ƣ�������ֵ������+������ֵ��Ϊ0��ͳ�ƣ�', True, cid=1050)
def skillDelayCastStatParams():
    pass


@config(Bool, 'false', '��ϻ��ְҵ��������', True, cid=1051)
def enableSecondSchoolCardSlotScheme():
    pass


@config(Bool, 'false', '�ü�ϴ����ְҵ��������', True, cid=1052)
def enableSecondSchoolCardWashScheme():
    pass


@config(Bool, 'false', '�����ӦԮ', True, cid=1053)
def enableArenaPlayoffsAid():
    pass


@config(Bool, 'false', '����ᵥ��Ѻע', True, cid=1054)
def enableArenaPlayoffsBetOne():
    pass


@config(Bool, 'false', '���������������', True, cid=1055)
def enableUGCLimit():
    pass


@config(Bool, 'false', 'ǿ�����������������(��ʱ����,��Ҫ�ǵü�ʱ�ص�)', True, cid=1056)
def enableUGCForceLimit():
    pass


@config(Int, '0', '������֮ս����aoi(0����Ч)')
def enableWingWarAoIRadius():
    pass


@config(Bool, 'false', '�Ƿ�������ᵥ��Ѻע', True, cid=1057)
def enablePlayoffsBetDayNew():
    pass


@config(Bool, 'false', '�Ƿ��Զ���Ч�͵ȼ�����ӡ', True, cid=1058)
def enableLessLvWenYin():
    pass


@config(Bool, 'false', '�Ƿ���������֮ս��ձ����Ż�')
def enableClearInvInWingWar():
    pass


@config(Bool, 'false', '5v5������ֹ��������')
def enableNoRenter5v5Playoffs():
    pass


@config(Bool, 'false', '�Ƿ�����ӡ��������Ϊ��log')
def enablePuppetPrintLog():
    pass


@config(Bool, 'false', '�Ƿ�����Դ�������', True, cid=1059)
def enableBenYuanHirogramLock():
    pass


@config(Bool, 'false', '�Ƿ��������������', True, cid=1060)
def enableGuanYinLock():
    pass


@config(Bool, 'false', 'ˮ������ս', True, cid=1061)
def enableHandInItem():
    pass


@config(Bool, 'false', '�Ƿ���ˮ������ս�������õĲ����ռ��������', True, cid=1062)
def enableCollectItemMessagePush():
    pass


@config(Bool, 'false', '�Ƿ���ͷ��������', True, cid=1063)
def enableTopChatRoom():
    pass


@config(Bool, 'false', '�Ƿ������׻�Ա���v2')
def enableMembershipGiftV2():
    pass


@config(Bool, 'true', '����ǰ������ڳ���������פ�غ͵ع�Ҫ�Ȼش�����')
def enableCheckSceneBeforeFuben():
    pass


@config(Bool, 'false', '�Ƿ�����ɱϵͳ', True, cid=1064)
def enableAssassination():
    pass


@config(Bool, 'true', '�Ƿ�֧�ֿ���ӵ���')
def enableAddDaoHengInCross():
    pass


@config(Bool, 'true', '�Ƿ�֧�ֿ������˫�ĵ�')
def enableAddWSProficiencyInCross():
    pass


@config(Bool, 'true', '�Ƿ��������ս����Ȩ(����ս����ΧС����)', True, cid=1065)
def enablePlayoffsTeamPrivilege():
    pass


@config(Int, '-1', '�������������(���ٰ����õ�������)', True, cid=1066)
def arenaPlayoffsSeason():
    pass


@config(Bool, 'false', '�������սʹ����Ӫ', True, cid=1067)
def enableWingWorldWarCamp():
    pass


@config(Bool, 'false', '�������ս��Ӫ����', True, cid=1068)
def enableWingWorldWarCampSignUp():
    pass


@config(Bool, 'false', '�Ƿ�����ս��ƥ�����')
def enableNewBattleFieldMatch():
    pass


@config(Bool, 'false', '�Ƿ���ս�����Ҷ�ģʽ', True, cid=1069)
def enableBattleFieldChaosMode():
    pass


@config(Bool, 'false', '������ǳ�����', True, cid=1070)
def enableWingWorldSwallow():
    pass


@config(Str, '', '������ʱ��1�����ɵĳǳأ��Զ�������񣬱���1,2,3', True, cid=1071)
def enableWingCitySwallowList1():
    pass


@config(Str, '', '������ʱ��2�����ɵĳǳأ��Զ�������񣬱���1,2,3', True, cid=1072)
def enableWingCitySwallowList2():
    pass


@config(Str, '', '������ʱ��3�����ɵĳǳأ��Զ�������񣬱���1,2,3', True, cid=1073)
def enableWingCitySwallowList3():
    pass


@config(Bool, 'false', '�Ƿ���������Ч���', True, cid=1074)
def enableActAppearance():
    pass


@config(Bool, 'false', '�Ƿ���ֱ��2.0', True, cid=1075)
def enableStraightLvUpV2():
    pass


@config(Bool, 'false', '������ǳ���ս����ͨ���ж�', True, cid=1076)
def enableWingWorldDeclareNewLink():
    pass


@config(Bool, 'false', '�������սʹ����Ӫģʽ', True, cid=1077)
def enableWingWorldWarCampMode():
    pass


@config(Bool, 'true', '��������Ӫ����', True, cid=1078)
def enableWingWorldCampLaba():
    pass


@config(Bool, 'false', '�����ٱ������س齱�', True, cid=1079)
def enableRandomItemsLottery():
    pass


@config(Bool, 'false', '�Ƿ�������', True, cid=1080)
def enableBet():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�û������쳣״̬���')
def enablePuppetInvalidCheck():
    pass


@config(Bool, 'false', 'ʵ����֤����', True, cid=1081)
def enableRealNameCheck():
    pass


@config(Bool, 'false', 'gtͬһursֻ����һ��', True, cid=1082)
def enableGtOneAvatar():
    pass


@config(Bool, 'false', 'ʵ����Ϸʱ������', True, cid=1083)
def enableRealNameGameLimit():
    pass


@config(Bool, 'false', 'ʵ���Ƴ�ֵ����', True, cid=1084)
def enableRealNameChargeLimit():
    pass


@config(Bool, 'false', 'ս���淨ƥ�����ƶ࿪', True, cid=1085)
def enableFubenMultiLimit():
    pass


@config(Bool, 'false', '�������������������׷���', True, cid=1086)
def enableGConsigntmentProfitByWeight():
    pass


@config(Bool, 'false', '�Ƿ�����ͼ�淨', True, cid=1087)
def enableMapGame():
    pass


@config(Bool, 'false', '�Ƿ����ٱ�������', True, cid=1088)
def enableRandomTreasureBagMainMessagePush():
    pass


@config(Bool, 'false', '�Ƿ����ٱ����', True, cid=1089)
def enableRandomTreasureBagMain():
    pass


@config(Bool, 'false', 'ս��ƥ�����ս������')
def enableGroupByCombatScoreInBF():
    pass


@config(Bool, 'false', '�Ƿ������Ͱ�ɱ-�����յ���ɱ�ɹ�������', True, cid=1090)
def enableAssEmployerPush():
    pass


@config(Bool, 'false', '�Ƿ�������Ȩ������')
def enableInitGuildPrivilege():
    pass


@config(Bool, 'false', '�Ƿ�����Ҹ����ʼ���Ʒ������')
def enableCoinPayMailItemWhiteList():
    pass


@config(Bool, 'false', '�Ƿ������ս�������������׷ֺ�')
def enableClanWarConsignProfitByContribute():
    pass


@config(Bool, 'false', '�Ƿ���Ԫ�������ϼ�')
def enableCoinConsignPlace():
    pass


@config(Int, '10000', '��ͼ�����ֶ������ 10000��ʾ100%', True, cid=1091)
def mapGameFubenMultiply():
    pass


@config(Bool, 'false', '�������ܸ�Ӣ��ӱ���/����', True, cid=1092)
def enablePSkillExtraEffect():
    pass


@config(Bool, 'false', '�ü�װ��ʱ����װ���', True, cid=1093)
def enableCheckCardSuitOnFix():
    pass


@config(Bool, 'false', '�ɻ������Ƿ����ʵ��')
def enableFeihuoRealName():
    pass


@config(Bool, 'false', '�Ƿ������սѺ��', True, cid=1094)
def enableClanWarCourier():
    pass


@config(Bool, 'false', '��ͼ�淨,˽��������Ϊ���ķ�, ������������ķ����������ķ���ʧЧ')
def enableMapGameDebugMode():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ�����ܶ��Ż�', True, cid=1095)
def enableSpriteFamiV2():
    pass


@config(Bool, 'true', '���ʼ�ʱ,�����ѵ��Զ����')
def enableAutoSplitMail():
    pass


@config(Bool, 'true', '�����ӳٸ��µ����ķ�')
def enableMapGameDelayUpdate():
    pass


@config(Bool, 'false', '�Ƿ�������ʼ���Ʒ��������', True, cid=1096)
def enableCoinMailHandoverCheck():
    pass


@config(Bool, 'false', '�Ƿ�������������������', True, cid=1097)
def enableWingWorldCampArmy():
    pass


@config(Bool, 'false', '�Ƿ���NPC�øж�', True, cid=1098)
def enableNpcFavor():
    pass


@config(Bool, 'false', 'Ӣ������ת�ƴ��ڿ���', True, cid=1099)
def enableSpriteFamiTransferInFestival():
    pass


@config(Bool, 'false', '��ͼ�����Ƿ������ȡ', True, cid=1100)
def enableMapGameReward():
    pass


@config(Bool, 'false', '��������Ӫ����һ��δ��¼�����ʵ��', True, cid=1101)
def enableWWCIgnoreInActivePower():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ������', True, cid=1102)
def enableSpriteChallenge():
    pass


@config(Bool, 'false', '�Ƿ�����ս', True, cid=1103)
def enableOpenWingWorldWar():
    pass


@config(Bool, 'false', '�Ƿ�������׷��', True, cid=1104)
def enablePursueJunJie():
    pass


@config(Bool, 'false', '�Ƿ����ֹ�װ����', True, cid=1105)
def enableRefineManualEquipment():
    pass


@config(Bool, 'false', '��սӢ�����ܻ�ȡ����')
def enableSpriteAddFamiV2():
    pass


@config(Bool, 'false', '�Ƿ�����¯���������Ż�')
def enableSendForgeGConsignRightNow():
    pass


@config(Bool, 'false', '�Ƿ�ʹ�üƷ����к�ҵ��������')
def enableNewNetBarRewardHost():
    pass


@config(Bool, 'false', '�Ƿ����Լ�ս��', True, cid=1106)
def enablePUBG():
    pass


@config(Str, '', '��ͼ�����ֶ������ ���������ͷ�', True, cid=1107)
def mapGameFubenMultiplyEx():
    pass


@config(Bool, 'false', '�Ƿ���Ѫս������', True, cid=1108)
def enableGSXY():
    pass


@config(Bool, 'false', '�Ƿ�ʹ����һ����װ���', True, cid=1109)
def enableQuickReplaceEquipmentV2():
    pass


@config(Bool, 'false', '�Ƿ�������ϵͳ', True, cid=1110)
def enableCollectionSystem():
    pass


@config(Bool, 'false', '��������Ӫģʽ����ʵ��1����Ч', True, cid=1111)
def enableWingWorldCampPowerExpire():
    pass


@config(Str, '', '�������ս��ͼ����ֳǳصȼ���������', True, cid=1112)
def wingWorldWarCityMaxCountEx():
    pass


@config(Bool, 'false', '�Ƿ���ÿ�ո�����ֵ����Ż��', True, cid=1113)
def enableDailyWelfareActivityOptimize():
    pass


@config(Bool, 'false', '��¼ʱ������ӡ������(equipmentTrigger)')
def enableLogonWenYinTrigger():
    pass


@config(Bool, 'false', '����֮����������')
def enableWingSoulBossDelayConsign():
    pass


@config(Int, '0', 'Ѫս���������aoi��0����Ч��')
def enableGSXYAoIRadius():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ������������ʾ', True, cid=1114)
def enableSpriteChallengeSpBuff():
    pass


@config(Bool, 'false', '�Ƿ����ֹ�װ���������Ż�', True, cid=1115)
def enableManualEquipMaterialDiscount():
    pass


@config(Bool, 'false', '����ӳ�ʱ��ֱ�Ӵ���', True, cid=1116)
def enableFollowNotAutoTeleport():
    pass


@config(Bool, 'true', 'ģ��ķ��Ĳ�����ʱʹ��װ������', True, cid=1117)
def enableCharTempGuanYinUseEquip():
    pass


@config(Bool, 'false', '�Ƿ�������ӡ����', True, cid=1118)
def enableNewWenYinOp():
    pass


@config(Bool, 'true', 'ģ�����ӡ������ʱʹ��װ������', True, cid=1119)
def enableCharTempWenYinUseEquip():
    pass


@config(Bool, 'false', 'ս�������������Ʊ���')
def enableBattleFieldMaxNumWarn():
    pass


@config(Str, '', 'ս�������������Ʊ���')
def battleFieldWarnNumLimit():
    pass


@config(Bool, 'false', '�������Ƿ����µ�װ���л�')
def enbalePuppetNewEquip():
    pass


@config(Bool, 'false', '��������ӳ�ˢ��(ȷ����dailyReset���ˢ)')
def enbaleTreasureBoxHistoryDelayReset():
    pass


@config(Bool, 'false', '�Ƴ���������ʧ�ܣ������Ƴ���һeffectType������')
def enablePSkillExtraEffectTryRemove():
    pass


@config(Bool, 'false', '���������������Կ���', True, cid=1120)
def enableGuildGrowthExtraPropsAdd():
    pass


@config(Bool, 'true', 'նħ���Ǽ�boss', True, cid=1121)
def enableZMJStarBoss():
    pass


@config(Bool, 'true', 'ģ����������', True, cid=1122)
def enableCharTempFamousGeneral():
    pass


@config(Bool, 'true', '����л�װ��', True, cid=1123)
def enableSwitchEquipInSoul():
    pass


@config(Bool, 'false', 'ս��׷�ϵ��߽�������', True, cid=1124)
def enableCombatScoreListReward():
    pass


@config(Bool, 'false', '���ܶ�Ӣ������Լӳ�', True, cid=1125)
def enableSpriteFamiliarAdd():
    pass


@config(Bool, 'false', 'buff��src����ɾ��')
def enableRmStateBySrcDist():
    pass


@config(Bool, 'true', '�Լ�ģ�弼����ֻ�������½�2��(1,4),�������ֹ��á��ҹ���schemeNo')
def enablePubgShortSplit():
    pass


@config(Bool, 'true', '�Լ���������������schemeNo')
def enablePubgShortcutSchemeNo():
    pass


@config(Bool, 'true', '�Լ������������������½ǲ���scheme(1,4)')
def enablePubgShortcutSchemeVal():
    pass


@config(Bool, 'false', '��������', True, cid=1126)
def enableActivityCollect():
    pass


@config(Bool, 'false', '����ͨ����http', True, cid=1127)
def enableFTBHttp():
    pass


@config(Bool, 'false', '����ͨ���', True, cid=1128)
def enableFTBActivity():
    pass


@config(Bool, 'true', '��͸����/����Ч��')
def enableIgnoreShield():
    pass


@config(Bool, 'false', '����Ǯ������', True, cid=1129)
def enableResetFTBPasswd():
    pass


@config(Bool, 'true', '���λ�λֱ�Ӵ�')
def enableTeleportNoCheck():
    pass


@config(Int, '5', '����ͨ����ȡ���')
def ftbActPullInterval():
    pass


@config(Bool, 'false', '�Ƿ���ʾ�ͻ��˵ķ���ͨ�����ť', True, cid=1130)
def enableFTBActivityClient():
    pass


@config(Bool, 'true', 'dpsMonster����ͳ����Ϣ', True, cid=1131)
def enableDpsMonsterEx():
    pass


@config(Bool, 'false', '���ѽ������ʷ���ѷ������µĲر��󶳽�', True, cid=1132)
def enableConsumeUnfreezeCbg():
    pass


@config(Bool, 'false', '�Ƿ������������ְҵ��������ҵ���Ѻ�', True, cid=1133)
def enableNewSchoolTianZhao():
    pass


@config(Bool, 'false', '�Ƿ����ϴ�traceback��appdump', True, cid=1134)
def enableUploadTBToAppdump():
    pass


@config(Bool, 'true', '�Լ����ٹ�ս����ˢ')
def enablePUBGMinNumLimit():
    pass


@config(Bool, 'true', '�Լ�����ݴ�')
def enablePUBGDoubleCheckBuildGroup():
    pass


@config(Bool, 'false', '��ͼ2��', True, cid=1135)
def enableMapGameV2():
    pass


@config(Bool, 'false', '�Ƿ���Ӣ������������', True, cid=1136)
def enableSpriteChallengeUnRealRank():
    pass


@config(Bool, 'false', 'ͳ���̳�����ۼ�����')
def enableRecordMallUnbindCoin():
    pass


@config(Bool, 'false', '�Ƿ����ͱҿ�����ҵֿ۹���', True, cid=1137)
def enableMallCashCoinPay():
    pass


@config(Bool, 'false', 'Ӣ�鼼�ܲ۸��ʽ���', True, cid=1138)
def enableSpriteSkillLuckyUnlock():
    pass


@config(Bool, 'false', '�Ƿ����̳Ƿ����ѷ�����ɫר�ù�����߹���', True, cid=1139)
def enableNoHistoryConsumedBuy():
    pass


@config(Bool, 'false', '�Ƿ�����ƥ�����', True, cid=1140)
def enableNewChooseQueue():
    pass


@config(Bool, 'true', '�Ƿ�����ҹ��ɱ�����', True, cid=1141)
def enablePVPPUBGProxy():
    pass


@config(Bool, 'false', '�Ƿ���ֿ�����빦��', True, cid=1142)
def enableFriendInviteActivityOp():
    pass


@config(Bool, 'false', '�����籨�����', True, cid=1143)
def enableWingWorldWarQueueV2():
    pass


@config(Bool, 'false', '�ع���ħ', True, cid=1144)
def enableMLShaxing():
    pass


@config(Bool, 'false', '��ͼ1��', True, cid=1145)
def enableMapGameV1():
    pass


@config(Bool, 'false', 'ս���������ҽ���', True, cid=1146)
def enableBattleJinbiReward():
    pass


@config(Bool, 'false', '�ر�����߽���', True, cid=1147)
def enableCBGItem():
    pass


@config(Str, '', '��ͼ������ֵ')
def mapGameFubenDmgLimit():
    pass


@config(Bool, 'false', '�Ƿ���WWArmy��combatMsg.msg���ڷ�����')
def enableWWArmyCombatMsgTest():
    pass


@config(Bool, 'false', '�Ƿ�����������', True, cid=1148)
def enableLZSBattleField():
    pass


@config(Bool, 'false', '������׺���������', True, cid=1149)
def enableGuildDonateBlackList():
    pass


@config(Bool, 'false', 'װ���������������', True, cid=1150)
def enableMakeManualEquipWhiteList():
    pass


@config(Bool, 'false', '�Ƿ���Puppet�ķ����Ѱ·')
def enablePuppetRecast():
    pass


@config(Bool, 'false', '�Ƿ��������ر��Ӻ�', True, cid=1152)
def enableTimerDestroyConqueredEmptyFb():
    pass


@config(Bool, 'false', '�Ƿ������˱���', True, cid=1153)
def enableNewPlayerTreasureBox():
    pass


@config(Bool, 'false', '�Ƿ�����һ������Զ��������¼�')
def enableCoinMarketAutoBuyAndCancel():
    pass


@config(Bool, 'false', '�Ƿ��������ս����ս��', True, cid=1154)
def enableWingWorldWarInactive():
    pass


@config(Bool, 'false', '�Ƿ��������log��¼', True, cid=1155)
def enableGameAntiCheatingLog():
    pass


@config(Bool, 'false', '�Ƿ�����ѡ��ӡ', True, cid=1156)
def enableSubGuanYin():
    pass


@config(Bool, 'false', '�Ƿ�����ѡ��ӡ', True, cid=1157)
def enableSubWenYin():
    pass


@config(Bool, 'false', '�Ƿ���������ż���', True, cid=1158)
def enableWingWorldArmyGather():
    pass


@config(Bool, 'true', '�Ƿ������˱�����˫�˱��俪�����', True, cid=1159)
def enableNTMultiTreasureBoxOpenCheck():
    pass


@config(Bool, 'false', '����Ч�����ٻ���Ӣ��', True, cid=1160)
def enableMultiSpriteBySE():
    pass


@config(Bool, 'false', '��������')
def enableFreezeFame():
    pass


@config(Bool, 'false', '����Ԫ�������ӳ���ȥ')
def enableCoinMarketDelayFetch():
    pass


@config(Bool, 'false', '�Ķ�ֵ����', True, cid=1163)
def enableNFWHeartbeat():
    pass


@config(Bool, 'false', '�ø������񿪹�', True, cid=1164)
def enableNFNewQuestLoop():
    pass


@config(Bool, 'false', '�����������ԭ������', True, cid=1165)
def enableIncExtraVal():
    pass


@config(Str, '', '�ع��������ƿ���')
def enableDiGongEnterLimit():
    pass


@config(Bool, 'false', '����boss����', True, cid=1167)
def enableWorldBoss():
    pass


@config(Bool, 'false', '����ʵ����֤', True, cid=1168)
def enablePlatformRealNameCheck():
    pass


@config(Bool, 'false', '˫��ֲ������', True, cid=1169)
def enableDoublePlantTree():
    pass


@config(Bool, 'false', '��ϻ��������', True, cid=1170)
def enableCardSlotResonance():
    pass


@config(Bool, 'false', '����ר�������һ�', True, cid=1171)
def enableRewardCatchUp():
    pass


@config(Bool, 'false', 'ע�����β�����ʾ', True, cid=1172)
def enableHijackHide():
    pass


@config(Bool, 'false', '��������Ƶ��', True, cid=1173)
def enableChatAnonymity():
    pass


@config(Bool, 'false', '�������ƹ������', True, cid=1174)
def enableLimitStatus():
    pass


@config(Bool, 'false', '��ʱ�Լ�����', True, cid=1175)
def enableTimingPUBG():
    pass


@config(Bool, 'false', '�Ƿ�ǿ������Avatar״̬�ݴ���')
def enableSkipAvatarStatesCheck():
    pass


@config(Bool, 'true', '����ƺſ��Ը�������', True, cid=1176)
def enableTitleWithProp():
    pass


@config(Bool, 'false', '��ͼ��Ӫ����', True, cid=1177)
def enableMapGameCamp():
    pass


@config(Bool, 'false', '����������λ������', True, cid=1178)
def enableGuildRankTournament():
    pass


@config(Bool, 'false', '�Ƿ����������Ҽ���߳����')
def enableKickoutIllegalPlayersByFuxi():
    pass


@config(Bool, 'true', '����һ���л�', True, cid=1179)
def enableGuanYinOneKeyScheme():
    pass


@config(Bool, 'false', '��/˫���������Ƿ��������¹�����̭����Ϊ��������', True, cid=1180)
def enableNewMatchRuleSSC():
    pass


@config(Bool, 'true', '��ӡһ���л�', True, cid=1181)
def enableWenYinOneKeyScheme():
    pass


@config(Bool, 'true', 'װ��һ���л�', True, cid=1182)
def enableEquipOneKeyScheme():
    pass


@config(Int, '0', '��ֹ����һ���л�[��˫�����ԣ����ܵ㣬�����������飬�ü�]', True, cid=1183)
def enableOthersOneKeyScheme():
    pass


@config(Bool, 'true', '�ü�ָ��ϴ��')
def enableWashCardFixedProps():
    pass


@config(Bool, 'false', '��ӡ���߲�ѯ')
def enableWenYinOffLineQuery():
    pass


@config(Bool, 'false', '�������а񿪹�', True, cid=1184)
def enableTianZhaoTopRank():
    pass


@config(Bool, 'false', '���а�89���¼�1��', True, cid=1185)
def enableTopRankNewLv89():
    pass


@config(Bool, 'false', '��ս�����Ƿ���', True, cid=1186)
def enableLunZhanYunDian():
    pass


@config(Bool, 'false', 'װ��ֱ���Ƿ���', True, cid=1187)
def enableUpgradeManaulEquip():
    pass


@config(Bool, 'false', '�Ƿ����°湫������', True, cid=1188)
def enableNewGuildTournament():
    pass


@config(Bool, 'false', '�Ƿ���PVE������pveQuota')
def enablePveQuota():
    pass


@config(Bool, 'false', '�Ƿ���˫ʮһ��ͼ�淨', True, cid=1189)
def enableMapGameV3():
    pass


@config(Bool, 'false', '�Ƿ���Ĺ����ͼ�淨', True, cid=1190)
def enableMapGameGrave():
    pass


@config(Bool, 'false', '�Ƿ���װ����װ�ߵȼ��滻�͵ȼ�', True, cid=1191)
def enableEquipSuitReplace():
    pass


@config(Bool, 'true', '�߳�gtͬusr���', True, cid=1192)
def enableGtOneAvatarKick():
    pass


@config(Bool, 'true', 'attackOthers���ӷ�ս����Ԫ')
def enableAttackOthersNoBU():
    pass


@config(Int, '0', '���û����˹̶�ְҵ')
def enablePuppetFixedSchool():
    pass


@config(Int, '0', '���������ʱ�����Ƿ���Ҫ���� const.WING_WORLD_CAMP_PLAYER_CHECK_TIME')
def enableWingWorldCampTimerReset():
    pass


@config(Bool, 'false', '�Ƿ���89��', True, cid=1193)
def enableNewLv89():
    pass


@config(Bool, 'false', '����BOSS��ʾ')
def enableWorldBossShowTip():
    pass


@config(Bool, 'false', '�Ƿ���������ʿ��ӻ�����', True, cid=1194)
def enableTreasureBoxVisible():
    pass


@config(Bool, 'false', '�Ƿ���89�����������ԴӴ����Ϊ���', True, cid=1195)
def enableNewPropCalcByFormula():
    pass


@config(Bool, 'false', '���������л�7ְҵ', True, cid=1196)
def questSwitch7School():
    pass


@config(Bool, 'false', '���������л�8ְҵ', True, cid=1197)
def questSwitch8School():
    pass


@config(Bool, 'false', '�Ƿ����ױ�ʵ����֤', True, cid=1198)
def enableEpayActive():
    pass


@config(Bool, 'false', '�������Ծ���3���ӹ���Ҫ��')
def enableWingWorldContriLimit():
    pass


@config(Bool, 'false', '�Ƿ��ֹnpc��dawdler�Ĺ���', True, cid=1199)
def enableForbidNpcAndDawdler():
    pass


@config(Bool, 'false', '�Ƿ���ת������׷��', True, cid=1200)
def enableMigrateRewardCatchUp():
    pass


@config(Bool, 'false', 'ǿ��ˢ����ͨ�̵�', True, cid=1201)
def enableRefreshNormalPrivateShop():
    pass


@config(Bool, 'false', 'ע���˺Ź���ģ��', True, cid=1202)
def enableDelUrsStub():
    pass


@config(Bool, 'false', '��ʵ�˺�ʹ���������')
def enableRealDmgUseStaticProp():
    pass


@config(Bool, 'false', '����꿪��', True, cid=1203)
def enableHuntGhost():
    pass


@config(Bool, 'false', '����������ƿ���', True, cid=1204)
def enableHierogramLimit():
    pass


@config(Bool, 'false', '�Ƿ���fbEntityFixLvMax����', True, cid=1205)
def enableFbEntityFixLvMax():
    pass


@config(Bool, 'false', '�Ƿ������ѵ�½����������ʾ', True, cid=1206)
def enableTianZhaoLoginShowIgnore():
    pass


@config(Bool, 'false', '�Ƿ���89����Ƭʱ79����תԪ��', True, cid=1207)
def enableChangeExpToExpXiuWei():
    pass


@config(Bool, 'false', '�Ƿ�����ֱ���ȼ����㷽ʽ', True, cid=1208)
def enableStraightLvUpV2New():
    pass


@config(Bool, 'false', '�Ƿ���80��Ԫ����', True, cid=1209)
def enableExpXiuWeiWelfare():
    pass


@config(Bool, 'false', '�Ƿ�������ת��Ԫ���������������Լ�����', True, cid=1210)
def enableExpToYuanshen():
    pass


@config(Bool, 'true', '�Ƿ���ÿ����ӯ���鷢��', True, cid=1211)
def enableAssignDailyVp():
    pass


@config(Bool, 'false', '��������Ӫģʽ,��������ϵ���Ӫ��wingWorldCampStub/crossWingWorldCampStub����һ������')
def enableWWCMValFix():
    pass


@config(Str, '1101111111000', '�ر������ְҵ����', True, cid=1212)
def cbgRoleSaleSchoolLimit():
    pass


@config(Bool, 'false', '�Ƿ���װ��ĥ������¿���', True, cid=1213)
def enableNewDurability():
    pass


@config(Bool, 'false', '89�������ǿ��ħ��pveQuota����Ϊ0::#205938', True, cid=1214)
def enablePveQuotaReset():
    pass


@config(Bool, 'false', '�Ƿ�������ң����������������')
def enableXYnecklaceEnhanceSes():
    pass


@config(Bool, 'false', '�Ƿ�����831/832״̬����Ч����Ч')
def enableTZStateSpecialEffect831():
    pass


@config(Bool, 'false', '�Ƿ���ʱ�޸��������쳣����')
def enableSSCStatusFix():
    pass


@config(Bool, 'false', '�������V2', True, cid=1215)
def enableJieQiV2():
    pass


@config(Bool, 'false', '�Ƿ��������������Ե㷽��')
def enableResetAllPropSchemeForNewLv():
    pass


@config(Str, '1,0.07', '��ս���ۼ����������')
def createLzydTimeLimit():
    pass


@config(Bool, 'false', '�Ƿ�������������˰')
def enableGuildConsignProfitTax():
    pass


@config(Bool, 'false', '�Ƿ�������ֵ�齱�', True, cid=1216)
def enableLuckyLottery():
    pass


@config(Bool, 'false', '���Ѽ��ܵ㷽������')
def enableTZSchemeSkillPointReset():
    pass


@config(Bool, 'false', '�Ƿ���װ��������ϵֿ�', True, cid=1217)
def enableManualDiKou():
    pass


@config(Bool, 'false', '�Լ���ˢ��ȫ��')
def enablePUBGNewSafeArea():
    pass


@config(Bool, 'false', '����ר�������һ��Ż�', True, cid=1218)
def enableRewardCatchUpOptimize():
    pass


@config(Bool, 'false', '�Ƿ��ϱ�������ƽ̨')
def enableReportToPlatform():
    pass


@config(Bool, 'false', '����תְ����', True, cid=1219)
def enableSchoolTransferConditionItemCost():
    pass


@config(Bool, 'false', '���������λ����ս', True, cid=1220)
def enableNewGuildTournamentLiveAndInspire():
    pass


@config(Bool, 'true', '����crontab�����жϹ̶�ʱ����Ż�', True, cid=1221)
def enableCheckCrontabStrIsFixedTimeStamp():
    pass


@config(Bool, 'false', '�Ƿ���DOTA������Ӣ��', True, cid=1222)
def enableDotaFreeRandomRole():
    pass


@config(Bool, 'false', '�Ƿ���������װ���ر�����ϵͳ', True, cid=1223)
def enableEquipEnhanceSuit():
    pass


@config(Bool, 'false', '�Ƿ���showBroodLabel�Ż�-�汾2', True, cid=1224)
def enableOptimizeShowBloodLabelV2():
    pass


@config(Bool, 'false', '�Ƿ����ü����ϴ��', True, cid=1225)
def enableAutoWashCard():
    pass


@config(Bool, 'false', '�Ƿ������������������', True, cid=1226)
def enableGuildCrossSkill():
    pass


@config(Bool, 'false', '�Ƿ�����Ӱ����', True, cid=1227)
def enableWuYinSuLan():
    pass
