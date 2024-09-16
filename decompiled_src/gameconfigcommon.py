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

    @config(Int, str(gameconst.ONLINE_MASS_MAX), '系统最大在线人数')
    def maxOnline():
        pass


@config(Int, '0', '客户端登录版本号限制')
def clientVersionThreshold():
    pass


@config(Bool, 'false', '是否开启客户端登录版本号检查')
def clientVersionCheck():
    pass


@config(Int, str(int(time.time())), '服务器第一次启动时间', True, cid=1)
def serverOpenTime():
    pass


@config(Int, '0', '竞技场只使用指定地图')
def disableArenaMap():
    pass


@config(Int, '0', '设置3V3竞技场开启人数')
def arena3v3Num():
    pass


@config(Int, '0', '设置战场回收人数')
def bfRecycleNum():
    pass


@config(Int, '0', '设置战场关闭时间')
def bfDurationTime():
    pass


@config(Int, '0', '设置竞技场持续时间')
def arenaDurationTime():
    pass


@config(Int, '0', '设置战场人数上限')
def bfMaxNum():
    pass


@config(Int, '0', '随机组队成队人数')
def groupMatchNum():
    pass


@config(Int, '120', 'entityController句柄超限报警阈值')
def entityControllerLimitCount():
    pass


@config(Bool, 'true', '是否开启cc', True, cid=2)
def isCCVersion():
    pass


@config(Int, '800', '城战单据点容纳人数上限')
def clanWarFortMaxPlayer():
    pass


@config(Int, '3500', '城战总人数报警上限')
def clanWarWarningPlayerNum():
    pass


@config(Bool, 'true', '是否开启特效称号', True, cid=3)
def enableEffectTitle():
    pass


@config(Bool, 'true', '是否开启降低CPU的优化手段')
def enableReduceCPUOverHead():
    pass


@config(Bool, 'false', '是否开启装备喂养', True, cid=4)
def enableFeedEquip():
    pass


@config(Bool, 'true', '是否开启avatar创生客户端结算', True, cid=5)
def enableMFClientCalc():
    pass


@config(Bool, 'true', '是否开启普通技能的客户端结算', True, cid=6)
def enableSkillClientCalc():
    pass


@config(Bool, 'false', '开启所有允许技能均走客户端结算的逻辑(有结算延时的直接忽略延时)', True, cid=7)
def forceSkillClientCalc():
    pass


@config(Bool, 'true', '是否自动使用qte技能', True, cid=8)
def enableAutoUseQteSkills():
    pass


@config(Bool, 'true', '是否竞技场季后赛淘汰赛固定分组')
def enableArenaPlayoffsFinalHardGroup():
    pass


@config(Bool, 'false', '是否启用竞技场固定30s准备时间')
def enableArenaPlayoffsQuickReady():
    pass


@config(Bool, 'true', '是否确保战场的SpaceNo先销毁后pop')
def enableBFSpaceNoPopOrder():
    pass


@config(Bool, 'false', '是否开启风险监控')
def enableRiskControl():
    pass


@config(Bool, 'false', '是否开启投放监控报警到popo')
def enableRiskControlProcess():
    pass


@config(Bool, 'true', '是否开启全局投放修正')
def enableGlobalGenerationControl():
    pass


@config(Float, '1.0', '当负载达到多少时，直接禁止玩家释放技能')
def useSkillLoadLimit():
    pass


@config(Int, '0', '强制设置服务器的负载等级')
def forceLoadLv():
    pass


@config(Bool, 'false', '副本内是否也受loadLv的影响')
def enableGlobalLoadCheck():
    pass


@config(Bool, 'true', '是否开启短信提醒')
def enablePhoneMessageSend():
    pass


@config(Bool, 'true', '是否开启声望等级奖励')
def enableFameBonus():
    pass


@config(Bool, 'true', '是否开启声望升级奖励')
def enableFameLvUpBonus():
    pass


@config(Bool, 'true', '是否开启公会珍宝坊', True, cid=9)
def enableGuildShop():
    pass


@config(Bool, 'true', '是否开启众里寻他')
def enableGuildMatch():
    pass


@config(Bool, 'true', '是否开启生活技能装备耐久度消耗', True, cid=10)
def enableLifeDura():
    pass


@config(Bool, 'false', '是否关闭商城', True, cid=11)
def offMall():
    pass


@config(Bool, 'false', '是否关闭元宝充值', True, cid=12)
def offCharge():
    pass


@config(Bool, 'false', '是否关闭充值返还', True, cid=13)
def offCoinRefund():
    pass


@config(Bool, 'false', '是否关闭元宝寄售', True, cid=14)
def offCoinMarket():
    pass


@config(Bool, 'true', '是否开启失魂修理', True, cid=15)
def enableShiHunRepair():
    pass


@config(Bool, 'true', '是否开启好友自定义头像', True, cid=16)
def enableCustomRadio():
    pass


@config(Bool, 'false', '是否关闭安全模式', True, cid=17)
def offSafeMode():
    pass


@config(Bool, 'false', '是否开启易信', True, cid=18)
def enableYixin():
    pass


@config(Bool, 'false', '是否开启积分奖励功能', True, cid=19)
def enableAchieveScore():
    pass


@config(Bool, 'false', '是否开启天谕大目标/修行手册', True, cid=20)
def enableGuideGoal():
    pass


@config(Bool, 'true', '是否开启竞技场模式', True, cid=21)
def enableArenaMode():
    pass


@config(Bool, 'true', '是否开启竞技场报名', True, cid=22)
def enableArenaApply():
    pass


@config(Bool, 'true', '是否PVP传送限制', True, cid=23)
def enableDuelLimit():
    pass


@config(Bool, 'true', '是否开启交易模式', True, cid=24)
def enableTradeMode():
    pass


@config(Bool, 'true', '是否开启玩家自定义公会战旗功能', True, cid=25)
def enableUserDefGuildCrest():
    pass


@config(Bool, 'true', '是否开启境界功能', True, cid=26)
def enableJingJie():
    pass


@config(Bool, 'true', '是否开启自动突破境界功能', True, cid=27)
def enableAutoBreakJingJie():
    pass


@config(Bool, 'true', '是否启用回购标签', True, cid=28)
def enableBuyBackTab():
    pass


@config(Bool, 'true', '是否允许可配任务为不显示', True, cid=29)
def enableNoDiaplayQuests():
    pass


@config(Bool, 'true', '是否开启公会活动', True, cid=30)
def enableGuildActivity():
    pass


@config(Bool, 'true', '是否开启NOS服务', True, cid=31)
def enableNOSService():
    pass


@config(Bool, 'true', '是否开启空战技能', True, cid=32)
def enableAirSkill():
    pass


@config(Bool, 'false', '是否允许城市登录过滤', True, cid=33)
def enableLoginCityFilter():
    pass


@config(Bool, 'false', '是否开启馈灵六社跟浮动市场', True, cid=34)
def enableKuilingOrg():
    pass


@config(Bool, 'true', '突破境界时是否检查元神', True, cid=35)
def enableYSCheck():
    pass


@config(Bool, 'true', '是否开启公会面板公会建设Tab页', True, cid=36)
def enableGuildBuildingTab():
    pass


@config(Bool, 'false', '是否开启公会面板公会建筑远程使用', True, cid=37)
def enableRemoteGuildBuilding():
    pass


@config(Bool, 'true', '是否开启VIP服务', True, cid=38)
def enableVip():
    pass


@config(Bool, 'true', '是否开启副本实体数目警报', False)
def enableFubenAlert():
    pass


@config(Bool, 'true', '是否开启竞技场重复延迟匹配', False)
def enableArenaDupDelay():
    pass


@config(Bool, 'true', '是否开启AvatarPeek的代理', False)
def enableAvatarPeekProxy():
    pass


@config(Bool, 'false', '是否支持贵重物品处理', True, cid=39)
def enableValuableTrade():
    pass


@config(Bool, 'true', '是否可以领取双倍经验', True, cid=40)
def enableExpBonus():
    pass


@config(Bool, 'false', '是否可以喂养神格碎片', True, cid=41)
def enableAddRuneEquipExp():
    pass


@config(Bool, 'false', '是否可以洗练神格碎片', True, cid=42)
def enableRuneEquipXiLian():
    pass


@config(Bool, 'false', '是否可以重铸神力碎片', True, cid=43)
def enableReforgRune():
    pass


@config(Bool, 'false', '是否可以升阶神格碎片', True, cid=44)
def enableRuneEquipOrderUp():
    pass


@config(Bool, 'true', '是否打开神格系统:Hierogram or Rune', True, cid=45)
def enableHierogramOrRune():
    pass


@config(Bool, 'true', '是否使用新神格系统:Hierogram', True, cid=46)
def enableHierogram():
    pass


@config(Bool, 'false', '是否打开登录时查找物品重复uuid的功能(smj)')
def enableFindDuplicatedUUID():
    pass


@config(Bool, 'false', '是否打开消除物品重复uuid的功能，需要enableFindDuplicatedUUID打开(smj)')
def enableModifyDuplicatedUUID():
    pass


@config(Bool, 'false', '是否打开APP相册手动扩容', True, cid=47)
def enableAppAlbumManualVol():
    pass


@config(Bool, 'false', '是否打开秘闻频道', True, cid=48)
def enableSecretChannel():
    pass


@config(Bool, 'true', '是否打开基于负载重心的新负载均衡策略优化', True, cid=49)
def enableNewBalanceBarycenter():
    pass


@config(Bool, 'false', '是否全地图开启基于负载重心的新负载均衡策略优化', False)
def enableAllNewBalanceBarycenter():
    pass


@config(Bool, 'false', '是否打开高负载时的自动PythonProfile', False)
def enableAutoPythonProfileHighLoad():
    pass


@config(Bool, 'false', '是否打开states下发的发布订阅优化', False)
def enablePubSubStates():
    pass


@config(Bool, 'true', '是否打开客户端发布订阅列表的维护', True, cid=691)
def enablePubSubOperationClient():
    pass


@config(Bool, 'false', '是否打开服务端发布订阅列表的维护', False)
def enablePubSubOperation():
    pass


@config(Bool, 'false', '是否对未成年玩家消费进行每日限额')
def enableLimitTeenCoinConsume():
    pass


@config(Bool, 'true', '是否开启APP消息推送功能', True, cid=50)
def enableAppMsg():
    pass


@config(Bool, 'true', '报警消息，是否发送到popo')
def criticalMsgToPopo():
    pass


@config(Bool, 'true', '客户端的异常信息，是否发送到popo')
def clientExceptionToPopo():
    pass


@config(Bool, 'false', '是否限制只能同时创建一个角色', True, cid=51)
def oneCharacterLimit():
    pass


@config(Bool, 'false', '是否开启状态的一致性检查')
def stateConsistentCheck():
    pass


@config(Bool, 'false', '是否开启资源读取数据收集', True, cid=52)
def enableMiniClient():
    pass


@config(Bool, 'true', '是否开启挖宝功能', True, cid=53)
def enableWabao():
    pass


@config(Bool, 'true', '是否检查激活账号对应的服务器ID')
def checkActivatedAccountServerId():
    pass


@config(Bool, 'true', '是否开启TopSpeed检查')
def enableTopSpeedCheck():
    pass


@config(Bool, 'false', '是否允许发送易信图片', True, cid=54)
def enableYixinImage():
    pass


@config(Bool, 'true', '是否进行玩家任务状态修复', True, cid=55)
def enableQuestRepair():
    pass


@config(Bool, 'false', '是否开启拉新功能', True, cid=56)
def enableInviteMate():
    pass


@config(Bool, 'true', '是否开启人拉人功能', True, cid=57)
def enableFriendInvite():
    pass


@config(Bool, 'false', '是否开启邀请单人队伍的功能', True, cid=58)
def enableIgnoreTgtGroup():
    pass


@config(Bool, 'false', '账号登陆时是否检查激活验证')
def checkAccountLoginPermission():
    pass


@config(Bool, 'false', '是否开启被邀请者的拉新功能', False)
def enableInviteMateIter():
    pass


@config(Bool, 'true', '是否开启拉新查封禁功能')
def enableInviteAccountBanCheck():
    pass


@config(Bool, 'true', '是否使能平衡战场职业匹配')
def enableBFBalanceSchool():
    pass


@config(Bool, 'false', '是否使能战场匹配log')
def enableBFMatchLog():
    pass


@config(Bool, 'true', '是否使能竞技场分数均衡')
def enableArenaReBalance():
    pass


@config(Bool, 'false', '是否使能竞技场分数均衡log')
def enableArenaReBalanceLog():
    pass


@config(Bool, 'true', '允许易信服务端回查玩家信息')
def enableYixinQuery():
    pass


@config(Bool, 'false', '是否开启敌我状态的double check', True, cid=59)
def enableRelationCheck():
    pass


@config(Bool, 'false', '是否开启结拜系统', True, cid=60)
def enablePartner():
    pass


@config(Bool, 'true', '是否启用canInsertItemsEx', True, cid=61)
def enableCanInsertItemsEx():
    pass


@config(Bool, 'true', '是否启用城战数据 统计', True, cid=62)
def enableClanWarStats():
    pass


@config(Bool, 'true', '是否允许商城物品续期', True, cid=63)
def enableMallItemRenewal():
    pass


@config(Bool, 'true', '是否可以批量使用物品')
def enableBatchUseItem():
    pass


@config(Bool, 'true', '是否启用传送CD检测')
def enableTeleportCheck():
    pass


@config(Bool, 'true', '是否开启流通锁', True, cid=64)
def enableInventoryLock():
    pass


@config(Bool, 'true', '是否开启语义识别', True, cid=65)
def enableSemantics():
    pass


@config(Bool, 'true', '是否开启结契仪式', True, cid=66)
def enableContract():
    pass


@config(Bool, 'false', '是否开启结契周年奖励', True, cid=67)
def enableIntimacyYearlyReward():
    pass


@config(Bool, 'false', '是否开启结契周年奖励补偿', True, cid=68)
def enableIntimacyYearlyCompensate():
    pass


@config(Bool, 'true', '是否开启结契之誓', True, cid=69)
def enableIntimacyRegister():
    pass


@config(Bool, 'false', '是否开启结契之誓奖励领取', False)
def enableIntimacyRegisterReward():
    pass


@config(Bool, 'true', '是否启用服务端的负载记录')
def enableServerLoadCheck():
    pass


@config(Bool, 'true', '是否启用服务器负载Mongo日志', False)
def enableServerLoadDataMongo():
    pass


@config(Float, '0.95', '服务端卡顿记录的负载阈值')
def serverLoadCheckThreshold():
    pass


@config(Float, '5.0', '同步战场中玩家位置的时间间隔', True, cid=70)
def battlefieldPosRefreshInterval():
    pass


@config(Bool, 'false', '是否开启授业系统', True, cid=71)
def enableApprentice():
    pass


@config(Bool, 'true', '是否开启新授业系统', True, cid=72)
def enableNewApprentice():
    pass


@config(Bool, 'false', '是否开启防沉迷', True, cid=73)
def enableAntiIndulgence():
    pass


@config(Bool, 'false', '是否开启防沉迷登录限制')
def enableAntiIndulgenceLogin():
    pass


@config(Bool, 'false', '是否开启防沉迷登录限制(客户端)', True, cid=74)
def enableAntiIndulgenceLoginClient():
    pass


@config(Bool, 'true', '允许接入杭研NOS审核平台')
def enableHYNOSExamineAPI():
    pass


@config(Bool, 'true', '是否开启群战不广播avatarConfig的优化手段')
def enablePubAvatarConfig():
    pass


@config(Bool, 'true', '是否开启群战不广播aspect的优化手段')
def enablePubAspect():
    pass


@config(Bool, 'true', '是否打开每个进程自己的entity个数报警')
def enableEntityWarning():
    pass


@config(Bool, 'false', '是否追踪Avatar切Cell并打印日志')
def enableTraceCellSwitch():
    pass


@config(Bool, 'true', '是否开启元宝寄售', True, cid=75)
def enableCoinConsign():
    pass


@config(Bool, 'false', '是否开启本服的跨服拍卖行功能', True, cid=76)
def enableCrossConsign():
    pass


@config(Bool, 'true', '是否开启跨服拍卖中心服的服务', True, cid=77)
def enableCrossConsignCenter():
    pass


@config(Bool, 'true', '运营允许玩家发起新的跨服拍卖请求', True, cid=78)
def enableNewCrossConsignReq():
    pass


@config(Bool, 'false', '跨服拍卖行高级搜索', True, cid=79)
def enableCrossConsignFilterSearch():
    pass


@config(Bool, 'true', '是否开启无界之地战场', True, cid=80)
def enableFortBf():
    pass


@config(Bool, 'false', '是否开启钩肥战场', True, cid=81)
def enableHookBf():
    pass


@config(Bool, 'true', '是否开启战场团排延迟匹配', False)
def enableGroupApplyDelayMatch():
    pass


@config(Bool, 'false', '是否开启npc变怪优化', True, cid=82)
def enableRobModel():
    pass


@config(Bool, 'false', '是否开启npc变主角怪优化', True, cid=83)
def enableRobAvatarModel():
    pass


@config(Bool, 'true', '是否开启ccbox', True, cid=84)
def enableCCBox():
    pass


@config(Bool, 'true', '是否开启新战场', True, cid=85)
def enableFlagBf():
    pass


@config(Bool, 'false', '是否开启双旦战场', True, cid=86)
def enableHuntBf():
    pass


@config(Bool, 'false', '是否开启dota战场', True, cid=87)
def enableDotaBf():
    pass


@config(Bool, 'true', '是否使能战场、竞技场时间检查', True, cid=88)
def enableDuelTimeCheck():
    pass


@config(Bool, 'true', '是否开启光环结算上限配置')
def enableAuraCalcNumConfig():
    pass


@config(Bool, 'false', '是否记录用户的战场数据归档', True, cid=89)
def enableRecordBattleFieldData():
    pass


@config(Bool, 'true', '是否关闭公共续期道具的时间显示', True, cid=90)
def enableCommonResumeHide():
    pass


@config(Bool, 'true', '是否开放新公会功能', True, cid=91)
def enableNewGuild():
    pass


@config(Bool, 'true', '是否开启工会圆桌功能', True, cid=92)
def enableGuildRoundTable():
    pass


@config(Bool, 'false', '是否开放选人界面顶号功能', True, cid=93)
def enableLoginPassedPhaseRelog():
    pass


@config(Bool, 'true', '是否开放城战期间祖龙之怒的buff功能')
def enableClanWarCalcMultiply():
    pass


@config(Bool, 'true', '是否开放新的玉木峰贡献分统计功能')
def enableNewYmfScore():
    pass


@config(Bool, 'true', '开启NPC物品回收功能', True, cid=94)
def enableItemRecall():
    pass


@config(Bool, 'false', '是否开启网络延迟统计', False)
def sendLatencyInfo():
    pass


@config(Bool, 'true', '是否开启藏宝阁', True, cid=95)
def enableCBG():
    pass


@config(Bool, 'false', '是否开启藏宝阁联运账号跳转', True, cid=96)
def enableCBGOpenURLSkip():
    pass


@config(Bool, 'false', '是否开启藏宝阁角色交易', True, cid=695)
def enableCBGRole():
    pass


@config(Bool, 'true', '开启交易黑名单')
def enableBlackListCheck():
    pass


@config(Bool, 'true', '开启代打机器检查')
def enableBlackMachineCheck():
    pass


@config(Bool, 'true', '开启创建角色', True, cid=97)
def enableCreateRole():
    pass


@config(Bool, 'true', '开启roll点的检查')
def enableRollCheck():
    pass


@config(Bool, 'true', '是否开启云垂王者榜', True, cid=98)
def enableYunchuiTopRank():
    pass


@config(Bool, 'true', '是否开启队伍排行榜', True, cid=99)
def enableGroupFubenRank():
    pass


@config(Bool, 'True', '是否开启新生活技能面板', True, cid=100)
def enableNewLifeSkill():
    pass


@config(Bool, 'true', '是否开启物品log全服电视广播', False)
def enableItemLogBroadcast():
    pass


@config(Bool, 'true', '是否记录快捷支付客户端log', True, cid=101)
def enableEasyPayLog():
    pass


@config(Bool, 'true', '是否支持支付宝充值', True, cid=102)
def enableAlipay():
    pass


@config(Bool, 'true', '是否开启战场天降令功能', True, cid=103)
def enableTJL():
    pass


@config(Bool, 'true', '允许速度共享', True, cid=104)
def enableRideWingShareSpeed():
    pass


@config(Bool, 'true', '是否支持绑定手机将军令功能', True, cid=105)
def enableBindingProperty():
    pass


@config(Bool, 'true', '是否使能确认就位', True, cid=106)
def enableGroupPrepare():
    pass


@config(Bool, 'true', '是否支持快速开商城宝箱')
def enableAutoOpenMallBoxItem():
    pass


@config(Bool, 'true', '是否开启队列上限的功能')
def enableMaxQueueCheck():
    pass


@config(Bool, 'true', '是否开启驱魔系统', True, cid=107)
def enableQumo():
    pass


@config(Bool, 'true', '是否公会挑战', True, cid=108)
def enableGuildChallenge():
    pass


@config(Bool, 'true', '是否开启闲人撒钱/撒物品功能', False)
def enableDawdlerReward():
    pass


@config(Bool, 'true', '是否decode error异常检测', False)
def enableCheckDecodeError():
    pass


@config(Bool, 'false', '是否在console中打印mongo日志', False)
def enableConsoleLog():
    pass


@config(Bool, 'true', '是否开启交易监控', True, cid=109)
def enableTradeWatch():
    pass


@config(Bool, 'true', '是否开启弹幕', True, cid=110)
def enableBarrage():
    pass


@config(Bool, 'true', '是否开启亲密度功能', True, cid=111)
def enableIntimacy():
    pass


@config(Bool, 'true', '是否开启亲密度成就触发功能', True, cid=112)
def enableIntimacyTrigger():
    pass


@config(Int, '0', '大世界默认加载的cell数量', False)
def defaultBigWorldMinCellNum():
    pass


@config(Bool, 'false', '是否开启客户端性能日志', True, cid=113)
def enableLogClientPerformance():
    pass


@config(Bool, 'false', '是否高延迟时推送uu', True, cid=114)
def enablePushUU():
    pass


@config(Bool, 'true', '是否开启公会云币工资', True, cid=115)
def enableGuildPayCash():
    pass


@config(Bool, 'true', '是否开启公会天币工资', True, cid=116)
def enableGuildPayCoin():
    pass


@config(Bool, 'false', '怪物掉落的宝石是否需要设置归属', True, cid=117)
def enableGemOwner():
    pass


@config(Bool, 'true', '是否允许VIP网吧特权', True, cid=118)
def enableVipBar():
    pass


@config(Bool, 'true', '是否开启许愿系统', True, cid=119)
def enableWish():
    pass


@config(Bool, 'true', '是否打开proxyDist', True, cid=120)
def enableProxyDist():
    pass


@config(Bool, 'true', '公会敌对模式', True, cid=121)
def enableGuildEnemy():
    pass


@config(Bool, 'true', '开放排队美女zhibo', True, cid=122)
def enableCCliveBroadcast():
    pass


@config(Bool, 'true', '是否开启飞船移动平台前置检测', False)
def enableMPMutex():
    pass


@config(Bool, 'true', '是否开启往AdminStub发送', False)
def enableSendToAdmin():
    pass


@config(Bool, 'true', '是否开启跨服竞技场', True, cid=123)
def enableCrossServerArena():
    pass


@config(Bool, 'false', '是否是仅仅提供预约的服务器', True, cid=124)
def isReservationOnlyServer():
    pass


@config(Bool, 'true', '是否开启服务器进度', True, cid=125)
def enableServerProgress():
    pass


@config(Bool, 'true', '是否可以领取序列号激活奖励', True, cid=126)
def enableApplyActivationCodeReward():
    pass


@config(Bool, 'false', '是否兑换考拉优惠券', True, cid=127)
def enableKaola():
    pass


@config(Bool, 'true', '是否开放材料包', True, cid=128)
def enableMaterialBag():
    pass


@config(Bool, 'true', '是否开启自定义IME', True, cid=129)
def enableCustomIme():
    pass


@config(Bool, 'true', '是否开启公会无双心得修炼', True, cid=130)
def enableGuildWSPractice():
    pass


@config(Bool, 'false', '是否开启公会无双道行修炼', True, cid=131)
def enableGuildWSDaoheng():
    pass


@config(Bool, 'false', '是否开启无双悟道多方案', True, cid=132)
def enableWSSchemes():
    pass


@config(Bool, 'true', '是否开启无双悟道多方案快捷键', True, cid=133)
def enableWSSchemeHotKeys():
    pass


@config(Bool, 'false', '是否开启生死场和副本数值平衡模式', True, cid=134)
def enableRebalance():
    pass


@config(Bool, 'false', '是否开启判定珍品神器', True, cid=135)
def enableCalcRarityMiracle():
    pass


@config(Bool, 'false', '是否要将跨服拍卖数据同步到App的API', True, cid=136)
def enableSyncCrossConsignToApp():
    pass


@config(Bool, 'true', '是否进行伪排队', False)
def enableReCalcQueuePlace():
    pass


@config(Bool, 'true', '是否爆满通知', False)
def enableServerLoadedNotify():
    pass


@config(Int, '0', '服务器爆满偏移量', False)
def serverLoadedOffset():
    pass


@config(Bool, 'false', '是否使用跨服竞技场基础代码', False)
def enableCrossArenaBasic():
    pass


@config(Bool, 'true', '是否使用按时间缓存的log', False)
def enableDeadlineCachedLog():
    pass


@config(Int, str(5 * 60), 'log缓存时间', False)
def deadlineCachedLogExpireTime():
    pass


@config(Bool, 'false', '是否开启旧的历练任务', True, cid=137)
def oldLilian():
    pass


@config(Bool, 'true', '是否开启新的历练任务', True, cid=138)
def newLilian():
    pass


@config(Bool, 'true', '是否开启弑神进阶', True, cid=139)
def enableShishenCascade():
    pass


@config(Bool, 'true', '是否开启同步器防外挂', True, cid=140)
def enableNepSync():
    pass


@config(Bool, 'true', '是否开启服务器等级差经验加成', True, cid=141)
def enableServerExpAdd():
    pass


@config(Bool, 'false', '是否开启打印客户端的log信息，比如gm_client_info， ', True, cid=142)
def enablePrintClientLog():
    pass


@config(Bool, 'false', '是否开启推广员系统', True, cid=143)
def enableGsSystem():
    pass


@config(Bool, 'false', '是否开启新服福利', True, cid=144)
def enableOpenServerBonus():
    pass


@config(Bool, 'true', '是否开启新服福利的悟性瓶功能', True, cid=145)
def enableOpenServerBonusVpStorage():
    pass


@config(Bool, 'false', '是否开启UI的GC控制', True, cid=146)
def enableUIGCControl():
    pass


@config(Bool, 'false', '启用cc自更新', True, cid=147)
def enableCCSelfUpdate():
    pass


@config(Bool, 'true', '重点推荐页未完成条目强推送', True, cid=148)
def enableIncompleteItemsNotify():
    pass


@config(Bool, 'true', '是否开启VIP 7天体验包赠送增值包', True, cid=149)
def enableTrialVipGift():
    pass


@config(Bool, 'true', '是否允许连续物品使用logmerge')
def enableContinuousItemLogMerge():
    pass


@config(Bool, 'true', '是否开启地宫申请自动组队功能', True, cid=150)
def enableDiGongQuickJoinGroup():
    pass


@config(Bool, 'true', '是否开启国战申请自动组队功能', True, cid=151)
def enableWorldWarQuickJoinGroup():
    pass


@config(Bool, 'false', '是否开启cc闪烁', True, cid=152)
def enableCCShine():
    pass


@config(Bool, 'false', '是否开启段位奖励领取', True, cid=153)
def enableDuanWeiAward():
    pass


@config(Bool, 'false', '是否开启公会挑战拒战功能', True, cid=154)
def enableRejectGuildChallenge():
    pass


@config(Bool, 'true', '开启声望日志合并')
def enableFameLogMerge():
    pass


@config(Bool, 'false', '开启结契对数的通知', True, cid=155)
def enableNotifyBuildIntimacyCnt():
    pass


@config(Bool, 'true', '开启活动奖励补偿领取')
def enableActivityReward():
    pass


@config(Bool, 'true', '开启NOS服务的CDN配置', True, cid=156)
def enableNOSCDNDeploy():
    pass


@config(Bool, 'false', '是否游戏退出弹窗', True, cid=157)
def enableForceOpenUrl():
    pass


@config(Bool, 'true', '是否动态修复驱魔等级')
def enableQumoRepair():
    pass


@config(Bool, 'true', '王者之路我要变强tab页', True, cid=158)
def enablePlayRecommStrongerTab():
    pass


@config(Bool, 'true', '是否开启公会奖励工资', True, cid=159)
def enableGuildRewardSalary():
    pass


@config(Bool, 'true', '是否开启经验修为', True, cid=160)
def enableExpXiuWei():
    pass


@config(Bool, 'true', '是否开启跨服战场', True, cid=161)
def enableCrossServerBF():
    pass


@config(Bool, 'true', '是否开启跨服喇叭', True, cid=162)
def enableCrossServerLaba():
    pass


@config(Bool, 'false', '是否开启跨服国战喇叭', True, cid=163)
def enableWorldWarLaba():
    pass


@config(Bool, 'true', '开启复合商店返回实例')
def enableCompositeShopReturnInstance():
    pass


@config(Bool, 'false', '是否开启（元灵）悬饰', True, cid=164)
def enableYuanLing():
    pass


@config(Bool, 'false', '是否开启隐藏头盔', True, cid=165)
def enableHideFashionHead():
    pass


@config(Bool, 'false', '是否开启公会狩猎活动', True, cid=166)
def enableGuildActivityHunt():
    pass


@config(Bool, 'false', '是否开启物品重复UUID扫描')
def enableItemScan():
    pass


@config(Bool, 'true', '是否开启新的排行榜', True, cid=167)
def enableNewArenaRank():
    pass


@config(Bool, 'true', '一级学会所有轻功', True, cid=168)
def learnAllQingGongIgnoreLv():
    pass


@config(Bool, 'false', '防外挂增加移动到位置的记录', True, cid=169)
def recordMoveToPosition():
    pass


@config(Bool, 'true', '开启公会光源', True, cid=170)
def enableGuildLight():
    pass


@config(Int, '17', '设置商城开启等级, 受控于 offMall开关', True, cid=171)
def mallUseableMinLv():
    pass


@config(Int, '100', 'MDB的开启概率', True, cid=172)
def memoryDBRate():
    pass


@config(Bool, 'false', '是否允许deep其它玩家', True, cid=173)
def enableAvatarPeekAnother():
    pass


@config(Bool, 'false', '是否可以转服', True, cid=174)
def enableMigrateOut():
    pass


@config(Bool, 'false', '其他服务器玩家是否可以转到此服', True, cid=175)
def enableMigrateIn():
    pass


@config(Bool, 'false', '是否允许免费转服', True, cid=176)
def enableFreeMigrate():
    pass


@config(Bool, 'true', '装备前缀属性置换', True, cid=177)
def enableExchangeEquipPreProp():
    pass


@config(Bool, 'true', '装备属性转移', True, cid=178)
def enableTransferEquipProps():
    pass


@config(Bool, 'false', '是否开启GM指令广播优化')
def enableGmCommandBroadCastOptimization():
    pass


@config(Bool, 'true', '是否开启跑商功能', True, cid=179)
def enableGuildBusiness():
    pass


@config(Bool, 'true', '是否开启跑商委托功能', True, cid=180)
def enableGuildDgtBusiness():
    pass


@config(Bool, 'true', '全屏试衣间', True, cid=181)
def enableFullScreenFittingRoom():
    pass


@config(Bool, 'true', '是否开启师徒推荐', True, cid=182)
def enableApprenticePool():
    pass


@config(Bool, 'true', '是否开启物品转绑', True, cid=183)
def enableBindItemConvert():
    pass


@config(Bool, 'true', '是否开启战场双人报名', True, cid=184)
def enableBFDoubleApply():
    pass


@config(Bool, 'true', '是否开启相机分享功能', True, cid=185)
def enableCameraShare():
    pass


@config(Bool, 'true', '是否开启角色抓拍功能功能', True, cid=186)
def enableCharSnapshot():
    pass


@config(Bool, 'true', '是否开启zoomIn', True, cid=187)
def enableCameraZoomIn():
    pass


@config(Bool, 'true', '是否开启世界答题', False)
def enableWorldPuzzle():
    pass


@config(Bool, 'true', '是否在动作模式准星状态下穿透所有UI', True, cid=188)
def disableUIInActionMode():
    pass


@config(Str, '', '哪些活动奖励类型需要隐藏,英文逗号分隔', True, cid=189)
def hideActivityRewardTypes():
    pass


@config(Str, '0,0', '双旦战场的开启人数,2方阵营,用分号隔开,前面的为守卫方', True, cid=190)
def bfHuntSideNum():
    pass


@config(Str, '', '魂界战场英雄黑名单,用英文逗号隔开', True, cid=191)
def bfDotaRoleBlackList():
    pass


@config(Bool, 'true', '允许离开副本后执行清除临时背包的副本物品')
def enableRemoveFbTempBagItems():
    pass


@config(Bool, 'true', '开启活动双倍奖励', True, cid=192)
def enableActivityStateBonus():
    pass


@config(Bool, 'true', '开启服务器活动双倍状态检查')
def enableActivityStateDoubleCheck():
    pass


@config(Bool, 'true', '开启新服签到', True, cid=193)
def enableNewServerSignIn():
    pass


@config(Int, '49', '新手服最高玩家等级', True, cid=194)
def noviceServerMaxPlayerLv():
    pass


@config(Int, '30', '新手服最高社会等级', True, cid=195)
def noviceServerMaxSocLv():
    pass


@config(Int, '4000', '新手服最大驱魔贡献', True, cid=196)
def noviceServerMaxQuMo():
    pass


@config(Int, '30000', '新手服军阶累计最大贡献', True, cid=197)
def noviceServerMaxJunJie():
    pass


@config(Bool, 'true', '是否开启领地战')
def enableClanWar():
    pass


@config(Bool, 'true', '是否刷新世界怪')
def enableRefreshWorldMonster():
    pass


@config(Bool, 'true', '是否对32位开启内存控制', True, cid=198)
def enableNewMemoryLimit():
    pass


@config(Bool, 'true', '是否开启排行榜奖励领取推送')
def enableTopRankRewardPushNotify():
    pass


@config(Bool, 'true', '是否开启运营活动tab页', True, cid=199)
def enableOpratingActiviesTab():
    pass


@config(Bool, 'true', '是否开启帮带模式', True, cid=200)
def enableFubenHelpMode():
    pass


@config(Bool, 'true', '是否开启允许发送全服走马灯', True, cid=201)
def enableSendGlobalItemGainNotify():
    pass


@config(Bool, 'true', '是否开启允许接受全服走马灯', True, cid=202)
def enableRecvGlobalItemGainNotify():
    pass


@config(Bool, 'true', '是否支持服务器事件经验上限')
def enableServerProgressMaxExp():
    pass


@config(Bool, 'true', '是否开启公会联赛', True, cid=203)
def enableGuildTournament():
    pass


@config(Bool, 'true', '是否开启公会联赛分组模式', True, cid=204)
def enableGuildTournamentMultiGroup():
    pass


@config(Bool, 'true', '是否开启公会联赛报名', True, cid=205)
def enableGuildTournamentApply():
    pass


@config(Bool, 'false', '是否使用公会联赛测试战场', True, cid=206)
def enableGuildTournamentTestBF():
    pass


@config(Bool, 'false', '是否开启跨服公会联赛', True, cid=207)
def enableCrossGuildTournament():
    pass


@config(Bool, 'false', '是否开启竞技场季后赛排行榜候选玩家', True, cid=208)
def enableArenaPlayoffsTopRank():
    pass


@config(Bool, 'true', '是否开启竞技场季后赛(武道会)', True, cid=209)
def enableArenaPlayoffs():
    pass


@config(Bool, 'false', '是否开启竞技场季后赛押注功能', True, cid=210)
def enableArenaPlayoffsBet():
    pass


@config(Bool, 'false', '是否开启跨服擂台赛的功能', True, cid=211)
def enableArenaChallenge():
    pass


@config(Bool, 'false', '是否开启跨服擂台赛的观战功能', True, cid=212)
def enableArenaChallengeLive():
    pass


@config(Bool, 'false', '是否开启竞技场季后赛通过名字判断输赢的功能', True, cid=213)
def enableArenaPlayoffsBetTest():
    pass


@config(Bool, 'true', '是否开启竞技场季后赛竞猜兑奖功能', True, cid=214)
def enableArenaPlayoffsBetReward():
    pass


@config(Bool, 'false', '是否开启跨服公会联赛报名名额自动不足', True, cid=215)
def enableCrossGtnApplyAlter():
    pass


@config(Bool, 'true', '是否开启选人界面视频和翅膀', True, cid=216)
def enableAvatarVideoAndWing():
    pass


@config(Bool, 'true', '是否开启低于29级自动复活功能', True, cid=217)
def enableReliveAutoWithLvLess():
    pass


@config(Bool, 'true', '开启新服及活动积分', True, cid=218)
def enableActivityAchieveScore():
    pass


@config(Bool, 'true', '开启服务器配置功能', True, cid=219)
def enableCheckServerConfig():
    pass


@config(Bool, 'false', '是否开启内衣内裤的功能', True, cid=220)
def enableFashionNeiYi():
    pass


@config(Bool, 'true', '是否自动加技能点', True, cid=221)
def enableSkillLvAutoUp():
    pass


@config(Bool, 'true', '是否开启肤色校验', True, cid=222)
def enableCheckSkin():
    pass


@config(Bool, 'false', '是否开启新服签到面板', True, cid=223)
def enableNewServerSignInPanel():
    pass


@config(TimeStr, '', '宕机时间，用于副本cd自动补偿', False)
def fbReviseDowntime():
    pass


@config(Bool, 'true', '是否打开切换地图放弃任务', False)
def enableAbandonQuestWithSpaceChange():
    pass


@config(Bool, 'true', '是否开启新人直升', True, cid=224)
def enableNoviceBoost():
    pass


@config(Bool, 'true', '是否打开大世界和地宫指导', False)
def enableGroupGuide():
    pass


@config(Bool, 'true', '技能教学开关', True, cid=225)
def enableSkillGuide():
    pass


@config(Bool, 'true', '多怪物血条', True, cid=226)
def enableMonsterBlood():
    pass


@config(Bool, 'false', '双倍经验的开关', True, cid=227)
def enableDoubleExpPointInML():
    pass


@config(Bool, 'true', '活动签到开关', True, cid=228)
def enableActivityAttend():
    pass


@config(Bool, 'true', '活动积分开关', True, cid=229)
def enableActivityScore():
    pass


@config(Bool, 'true', '是否启动模型倾斜开关', True, cid=230)
def enableApplyModelRoll():
    pass


@config(Bool, 'true', '是否启动大世界玩法', True, cid=231)
def enableWorldPlayActivity():
    pass


@config(Bool, 'true', '是否开启充值活动', True, cid=232)
def enableChargeActivity():
    pass


@config(Bool, 'true', '是否开启新分线开启逻辑', True, cid=233)
def enableDiGongLineLogic():
    pass


@config(Bool, 'true', '是否开启space创建initData检测流程', False)
def enableSpaceInitDataCheck():
    pass


@config(Bool, 'true', '是否开启客服', True, cid=234)
def enableCustomerService():
    pass


@config(Bool, 'true', '是否开启vip客服', True, cid=235)
def enableCustomerVipService():
    pass


@config(Bool, 'false', '是否开启vip客服图片上传', True, cid=236)
def enableCustomerVipServiceUploadPic():
    pass


@config(Bool, 'true', '是否开启冒险手册', True, cid=237)
def enableDelegation():
    pass


@config(Int, '1', 'vip等级1', True, cid=238)
def vipServiceLevel1():
    pass


@config(Int, '6', 'vip等级2', True, cid=239)
def vipServiceLevel2():
    pass


@config(Bool, 'false', '是否对载具和关联buff的一致性进行检查', True, cid=240)
def enableDoubleCheckZaijuBuffRelation():
    pass


@config(Bool, 'true', '是否开启资料安全检查', True, cid=241)
def enableSecInfo():
    pass


@config(Bool, 'true', '是否开启公会召集', True, cid=242)
def enableGuildGather():
    pass


@config(Bool, 'true', '开启回流礼包功能', True, cid=243)
def enableFlowbackBonus():
    pass


@config(Bool, 'true', '是否卡钓鱼跟探秘的等级', False)
def enableFEManualUp():
    pass


@config(Bool, 'true', '是否开启人拉人活动', True, cid=244)
def enableFriendInviteActivity():
    pass


@config(Bool, 'true', '是否开启回流悟性机制', True, cid=245)
def enableBackflowVp():
    pass


@config(Bool, 'false', '是否开启校园行活动', True, cid=246)
def enableSchoolActivity():
    pass


@config(Bool, 'true', '是否删除角色的时间检查', False)
def enableDeleteAccountCheck():
    pass


@config(Bool, 'false', 'UI接口使用弱引用', True, cid=247)
def useWeakrefUIInterface():
    pass


@config(Bool, 'true', '是否开启背包搜索', True, cid=248)
def enableInvSearch():
    pass


@config(Bool, 'true', '启用地宫详情面板', True, cid=249)
def enableDigongDetail():
    pass


@config(Bool, 'false', '启用温泉详情面板', True, cid=250)
def enableWenQuanDetail():
    pass


@config(Bool, 'true', '启用元神瓶', True, cid=251)
def enableExpXiuWeiPool():
    pass


@config(Bool, 'true', '开启谕约平台', True, cid=252)
def enableMessageBoard():
    pass


@config(Bool, 'true', '是否启用装备套装激活功能', True, cid=253)
def enableEquipAddSuitEffect():
    pass


@config(Bool, 'true', '开启好友回流功能', True, cid=254)
def enableFriendFlowBack():
    pass


@config(Bool, 'true', '开启公会回流礼功能', True, cid=255)
def enableGuildFlowBack():
    pass


@config(Bool, 'true', '绑定战利品在规定时间内支持有分配权限的玩家可流通', True, cid=256)
def enableGroupTrade():
    pass


@config(Bool, 'true', '对装备的操作导致不能GroupTrade时，弹出二次确认', True, cid=257)
def enableLooseGroupTradeConfirm():
    pass


@config(Bool, 'true', '是否开启npc随机答题', True, cid=258)
def enableNpcPuzzle():
    pass


@config(Bool, 'false', '是否开启npc随机答题触发', True, cid=259)
def enableNpcPuzzleTrigger():
    pass


@config(Bool, 'true', '是否允许拖欠元宝')
def enableDebtCoin():
    pass


@config(Bool, 'true', '是否允许祖龙之印检查周围守方阵营')
def enableClanWarCreationGuardCheck():
    pass


@config(Bool, 'false', '是否允许大世界挑战', True, cid=260)
def enableWorldChallenge():
    pass


@config(Bool, 'true', '转服是是否检查包裹物品', True, cid=261)
def checkMigrateItem():
    pass


@config(Bool, 'True', '开启跨地宫寻路', True, cid=262)
def enableCrossDiGongNavigator():
    pass


@config(Bool, 'true', '玉木峰队友位置刷新', True, cid=263)
def enableYmfMemberPos():
    pass


@config(Bool, 'true', '开启组队信息分享', True, cid=264)
def enableTeamInfoShare():
    pass


@config(Bool, 'true', '是否开启科举功能', True, cid=265)
def enableKeju():
    pass


@config(Bool, 'true', '是否开启竞技场专用技能方案', True, cid=266)
def enableArenaSkillScheme():
    pass


@config(Bool, 'false', '是否在报名时检查竞技场技能方案', True, cid=267)
def enableCheckArenaSkillOnApply():
    pass


@config(Bool, 'true', '是否开启使用物品获取亲密度', False)
def enableAddIntimacyUseItem():
    pass


@config(Bool, 'true', '是否开启副本共战', True, cid=268)
def enableMutualBenefit():
    pass


@config(Bool, 'true', '是否开启双修', True, cid=269)
def enableShuangxiu():
    pass


@config(Bool, 'true', '开启跨服好友', True, cid=270)
def enableGlobalFriend():
    pass


@config(Bool, 'true', '启用新的f面板渲染', True, cid=271)
def enableNewFPanelRender():
    pass


@config(Bool, 'true', '是否开启天降福蛋在线奖励功能', True, cid=272)
def enableLoginReward():
    pass


@config(Bool, 'false', '是否开启苏澜学院奖励面板', True, cid=273)
def enableServerBonus():
    pass


@config(Bool, 'true', '是否开启奇人志', True, cid=274)
def enableRoleCardCollect():
    pass


@config(Bool, 'true', '是否开启风物志', True, cid=275)
def enableFengWuZhi():
    pass


@config(Bool, 'false', '时装属性转移', True, cid=276)
def enableFashionPropTrans():
    pass


@config(Bool, 'true', '是否商城广告下载', True, cid=277)
def enableRemotePic():
    pass


@config(Bool, 'true', '是否开启一些GM号只能在内网才能免排队', False)
def enableLoginFromNeteaseOnlyCheck():
    pass


@config(Bool, 'true', '摆摊自定义', True, cid=278)
def enableBoothCustom():
    pass


@config(Bool, 'true', '是否使用新副本指引', True, cid=279)
def enableNewFubenTargetGuide():
    pass


@config(Bool, 'true', '是否开启下一帧触发AI', False)
def enableTriggerNextFrame():
    pass


@config(Bool, 'true', '是否开启神语心魔录活动', True, cid=280)
def enableCollectItem():
    pass


@config(Bool, 'true', '启用战场cc，需要更新cc的资源，先提代码', True, cid=281)
def enableZhanChangCC():
    pass


@config(Bool, 'true', '是否启用多人合力开启的宝箱', False)
def enableMultiPlayerTreasureBox():
    pass


@config(Bool, 'true', '是否开启公会工作板', True, cid=282)
def enableGuildQuestBoard():
    pass


@config(Bool, 'true', '是否开启人拉人情感回流', True, cid=283)
def enableOfflineFlowback():
    pass


@config(Bool, 'false', '邀请点功能', True, cid=284)
def enableInvitePoint():
    pass


@config(Bool, 'true', '游戏内装备等数据链接网站数据库', True, cid=285)
def enableEquipGotoWeb():
    pass


@config(Bool, 'true', '是否开启新人直升等级', True, cid=286)
def enableNoviceBoostLevelUp():
    pass


@config(Bool, 'false', '是否禁止玩家登陆', True, cid=287)
def forbidEnterWorld():
    pass


@config(Bool, 'true', '是否开启计算国家战力')
def enableNationalCombatScoreCalc():
    pass


@config(Bool, 'true', '是否开启腰佩相关功能', True, cid=288)
def enableYaoPei():
    pass


@config(Bool, 'false', '是否开启全服排行榜', True, cid=289)
def enableCrossArenaRank():
    pass


@config(Bool, 'false', '是否开启世界阵营', True, cid=290)
def enableWorldCamp():
    pass


@config(Bool, 'true', '是否开启充值奖励', True, cid=291)
def enableChargeReward():
    pass


@config(Bool, 'false', '是否开启押镖功能', True, cid=292)
def enableYabiao():
    pass


@config(Bool, 'true', '是否开启装备解绑功能', True, cid=293)
def enableUnbindEquip():
    pass


@config(Bool, 'true', '是否开启职业克制修炼', True, cid=294)
def enablePvpEnhance():
    pass


@config(Bool, 'true', '是否开启铭牌系统', True, cid=295)
def enableMingpai():
    pass


@config(Bool, 'true', '是否开启豪气值系统', True, cid=296)
def enableHaoqiVal():
    pass


@config(Bool, 'true', '是否开启人品值系统', True, cid=297)
def enableRenpinVal():
    pass


@config(Bool, 'true', '是否开启结契时光', True, cid=298)
def enableIntimacyEvent():
    pass


@config(Bool, 'true', '是否开启结契时光V2', True, cid=299)
def enableIntimacyEventV2():
    pass


@config(Bool, 'true', '是否开启瑰宝阁相关功能', True, cid=300)
def enableGuiBaoGe():
    pass


@config(Bool, 'true', '是否开声望代币功能', True, cid=301)
def enableFameTransfer():
    pass


@config(Bool, 'false', '是否开启师徒加好友相关功能', False)
def enableApprenticeFriend():
    pass


@config(Bool, 'true', '是否开启离线加好友', False)
def enableOfflineAddFriend():
    pass


@config(Bool, 'true', '是否开启离线查看装备', False)
def enableOfflineWatchEquip():
    pass


@config(Bool, 'false', '是否开启跨服国战', True, cid=302)
def enableWorldWar():
    pass


@config(Bool, 'true', '是否开启跨服国战新地图', True, cid=303)
def enableWorldWarNewMap():
    pass


@config(Bool, 'false', '是否开启跨服国战胜负机制', True, cid=304)
def enableWorldWarJudge():
    pass


@config(Bool, 'true', '是否开启跨服国战升降级机制', True, cid=305)
def enableWorldWarUpgrade():
    pass


@config(Bool, 'false', '是否开启帝国边境掠夺', True, cid=306)
def enableWorldWarRob():
    pass


@config(Bool, 'false', '是否开启帝国边境决战', True, cid=307)
def enableWorldWarBattle():
    pass


@config(Bool, 'false', '是否开启帝国边境决战雇佣军', True, cid=308)
def enableWorldWarBattleHire():
    pass


@config(Bool, 'true', '是否开启帝国边境所在场景检查')
def enableWorldWarRemoveZombie():
    pass


@config(Bool, 'false', '是否开启跨服国战资源', True, cid=309)
def enableWorldWarBattleRes():
    pass


@config(Bool, 'false', '是否开启国家军队', True, cid=310)
def enableWorldWarArmy():
    pass


@config(Bool, 'false', '是否开启国家军队技能', True, cid=311)
def enableWorldWarArmySkill():
    pass


@config(Str, '', '是否开启国家军队分组(123全开)', True, cid=312)
def worldWarBattleGroup():
    pass


@config(Bool, 'false', '是否开启国战space异常报警', True, cid=313)
def enableWorldWarSpaceCheck():
    pass


@config(Bool, 'false', '是否开启跨服国战踢出非法角色')
def enableWorldWarKickDanger():
    pass


@config(Bool, 'true', '是否允许国战跨服登录')
def enableWorldWarSoulEnter():
    pass


@config(Bool, 'true', '是否开启跨服背包', True, cid=314)
def enableCrossServerBag():
    pass


@config(Bool, 'true', '是否开启时装染色自检', True, cid=315)
def enableCheckFashionDyeMaterials():
    pass


@config(Bool, 'true', '是否开启国战边境的原地复活物品消耗功能', True, cid=316)
def enableCrossBoarderReliveNow():
    pass


@config(Int, '500', '国战单边境最大人数')
def worldWarMaxPlayer():
    pass


@config(Int, '300', '国战决战单边境最大人数青龙组')
def worldWarBattleMaxPlayer():
    pass


@config(Int, '500', '国战掠夺单边境最大人数青龙组')
def worldWarRobMaxPlayer():
    pass


@config(Int, '100', '国战决战单边境最大人数白虎组')
def worldWarBattleYoungMaxPlayer():
    pass


@config(Int, '500', '国战掠夺单边境最大人数白虎组')
def worldWarRobYoungMaxPlayer():
    pass


@config(Bool, 'true', '是否开启国战决战掠夺分等级', True, cid=317)
def enableWorldWarYoungGroup():
    pass


@config(Bool, 'true', '是否开启国战军队分等级', True, cid=318)
def enableWorldWarArmyYoungGroup():
    pass


@config(Int, '150', '国战决战单边境最大雇佣人数')
def worldWarBattleMaxPlayerHire():
    pass


@config(Int, '50', '国战白虎决战单边境最大雇佣人数')
def worldWarBattleYoungMaxPlayerHire():
    pass


@config(Int, '30', '国战周边助攻人数上限')
def worldWarAssistLimit():
    pass


@config(Bool, 'true', '是否开启跨服国战IP限制', True, cid=319)
def enableWorldWarMacAddressCheck():
    pass


@config(Bool, 'false', '是否允许预付费预约', True, cid=320)
def enablePrePayCoin():
    pass


@config(Bool, 'true', '是否开启官印', True, cid=321)
def enableGuanYin():
    pass


@config(Bool, 'true', '是否开启官印第二期', True, cid=322)
def enableGuanYinSecondPhase():
    pass


@config(Bool, 'true', '是否开启官印魂技', True, cid=323)
def enableGuanYinSuperSkill():
    pass


@config(Bool, 'true', '是否开启共享坐骑翅膀属性', True, cid=324)
def enableSharedRideWingProp():
    pass


@config(Bool, 'true', '是否开启公会直升', True, cid=325)
def enableGuildNoviceBoost():
    pass


@config(Bool, 'true', '是否启用VIP队列', True, cid=326)
def enableVipQueue():
    pass


@config(Bool, 'true', '是否允许延迟踢玩家下线', True, cid=327)
def enableDelayKickAvatar():
    pass


@config(Bool, 'false', '是否支持随机任务', True, cid=328)
def enableRandomQuest():
    pass


@config(Bool, 'true', '是否可以在本服使用跨服背包内物品', True, cid=329)
def enableUseCrossInv():
    pass


@config(Bool, 'true', '是否开启怪物城战', True, cid=330)
def enableMonsterClanWar():
    pass


@config(Bool, 'true', '是否开启随机翅膀', True, cid=331)
def enableRandWingFly():
    pass


@config(Bool, 'true', '是否开启死循环日志', True, cid=332)
def enableRecursionLog():
    pass


@config(Bool, 'true', '是否开启传送前的spell动作', True, cid=333)
def enableTeleportSpell():
    pass


@config(Bool, 'false', '下线是remove不需要保留的buff', True, cid=334)
def removeStateOnOffline():
    pass


@config(Bool, 'true', '是否启用干扰玩法', True, cid=335)
def enableDisturb():
    pass


@config(Bool, 'true', '是否启用隐性干扰玩法', True, cid=336)
def enableInfect():
    pass


@config(Bool, 'true', '是否挖宝LOG', False)
def enableWabaoLog():
    pass


@config(Bool, 'true', '是否使用新年倒计时动画', True, cid=337)
def enableNewYearAni():
    pass


@config(Bool, 'true', '是否使用新年倒计时动画', False)
def enableSoulSaveShortcut():
    pass


@config(Bool, 'false', '是否开启NPC材料包入口', True, cid=338)
def enableMeterialNpc():
    pass


@config(Bool, 'false', '是否进行拼酒', True, cid=339)
def enablePinjiu():
    pass


@config(Bool, 'true', '是否商城折扣', True, cid=340)
def enableMallDiscount():
    pass


@config(Bool, 'true', '是否声望饰品支持生活属性', True, cid=341)
def enableLifeEquipEffect():
    pass


@config(Bool, 'true', '是否在cellapp超负载时自动降低服务器上限', True, cid=342)
def enableAutoReduceOnlineLimitOnCellAppOverload():
    pass


@config(Bool, 'false', '是否开启假日模式', True, cid=343)
def enableHolidayMode():
    pass


@config(Bool, 'true', '是否支持红包', True, cid=344)
def enableRedPacket():
    pass


@config(Bool, 'false', '是否开启图书图片支持', True, cid=345)
def enableBookPictureShow():
    pass


@config(Bool, 'true', '是否开启彩票', True, cid=346)
def enableLottery():
    pass


@config(Bool, 'false', '是否开启内置ie', True, cid=347)
def enableInnerIE():
    pass


@config(Bool, 'true', '是否开启资讯推送', True, cid=348)
def enablePushZixun():
    pass


@config(Bool, 'true', '是否开放新材料包', True, cid=349)
def enableNewMaterialBag():
    pass


@config(Bool, 'true', '是否外观收集积分排行', True, cid=350)
def enableAppearanceRank():
    pass


@config(Bool, 'true', '是否检查老玩家进入新手村并报警')
def doXinshoucunAvatarCheck():
    pass


@config(Bool, 'true', '是否开放亲密度技能', True, cid=351)
def enableIntimacySkill():
    pass


@config(Bool, 'true', '是否开放战场阵营检测', False)
def enableBfCampCheck():
    pass


@config(Bool, 'true', '是否开放申请单人无队玩家的新功能', False)
def enableApplyGroupWithNonGroup():
    pass


@config(Bool, 'true', '国家任务物品上缴功能', True, cid=352)
def enableWWNpcItemCommit():
    pass


@config(Bool, 'true', '是否物品使用推送', True, cid=353)
def enableItemUsePush():
    pass


@config(Bool, 'true', '是否使用新的相机url', True, cid=354)
def enableCameraNewURL():
    pass


@config(Bool, 'false', '是否开启运营活动大厅入口', True, cid=355)
def enableActivityHallIcon():
    pass


@config(Bool, 'true', '是否开启申请竞技场流程修改', True, cid=356)
def enableArenaApplyNotify():
    pass


@config(Bool, 'true', '是否开启血绽的错误报警')
def enableXiezhanReporting():
    pass


@config(Bool, 'true', '是否开放亲密度技能生死相随', True, cid=357)
def enableIntimacySkillSSXS():
    pass


@config(Bool, 'true', '怪物受击是否受伤害血量阈值影响', True, cid=358)
def enableHitActHpPercent():
    pass


@config(Bool, 'true', '是否开启镇妖比赛活动', True, cid=359)
def enableZhenyaoActivity():
    pass


@config(Bool, 'true', '是否开启无敌的doublecheck,在1号、10号以及所有的PVP地图中，doDamage时如果主角处于血战诀中则进行再一次的WUDI检查', False)
def enableXiezhanWudiDoubleCheck():
    pass


@config(Bool, 'true', '开启颜艺表情', True, cid=360)
def enableFaceEmote():
    pass


@config(Bool, 'true', '新的动作模式选择框刷新', True, cid=361)
def enableNewAimCross():
    pass


@config(Bool, 'false', '新的脚步声播放规则', True, cid=362)
def enableNewFootSound():
    pass


@config(Bool, 'false', '饰品加工', True, cid=363)
def enableMixJewelry():
    pass


@config(Bool, 'true', '开启传送后设置默认pitch值', True, cid=364)
def enableSetTeleportPitch():
    pass


@config(Bool, 'true', '是否开启伤害结算的二次确认（用于解决那些ghost数据同步不及时导致的结算错误问题）')
def enableDoDamageParamDoubleCheck():
    pass


@config(Bool, 'true', 'double check开启创生配置了单个entity只结算一次（用于解决那些ghost数据同步不及时导致的结算错误问题）')
def enableCreationCalcEntitiesDoubleCheck():
    pass


@config(Bool, 'true', '开启跨服背包物品检查报警', False)
def enableCrossInvItemWarning():
    pass


@config(Str, '<', '跨服后属性报警条件：bodyProp比较符soulProp', False)
def crossPropWarningOp():
    pass


@config(Bool, 'true', '是否开启战场举报功能', True, cid=365)
def enableBfReport():
    pass


@config(Bool, 'true', '是否启用一次性提示标记', True, cid=366)
def enablePushMessageOnceFlag():
    pass


@config(Bool, 'true', '活动列表根据星级排序', True, cid=367)
def enableActivitySortedByStar():
    pass


@config(Int, '0', '申请商人的最低等级')
def businessManMinLv():
    pass


@config(Bool, 'false', '是否启用新的奖励面板', True, cid=368)
def enableNewRewardHall():
    pass


@config(Bool, 'true', '领取更新奖励', True, cid=369)
def enableUpdateBonus():
    pass


@config(Bool, 'false', '开启开心公会排行榜', True, cid=370)
def enableGuildKindness():
    pass


@config(Bool, 'true', '启用国战任务引导', True, cid=371)
def enableWWQuestGuide():
    pass


@config(Bool, 'true', '是否启用任务完成动画', True, cid=372)
def enableCompleteQuestTip():
    pass


@config(Bool, 'true', '是否启用升级提示动画', True, cid=373)
def enableLvUpTip():
    pass


@config(Bool, 'true', '是否开启buff异常消失报警')
def enableDebugStateDisappear():
    pass


@config(Bool, 'false', '是否启用涂装', True, cid=374)
def enableTuzhuang():
    pass


@config(Bool, 'false', '是否启用幻肤', True, cid=375)
def enableHuanFu():
    pass


@config(Bool, 'true', '是否开启追随者交易', True, cid=376)
def enableTradeApprentice():
    pass


@config(Bool, 'false', '是否开启徒弟向师傅交易', True, cid=377)
def enableTradeToMentor():
    pass


@config(Bool, 'true', '是否开启随机挑战', True, cid=378)
def enableRandomChallenge():
    pass


@config(Bool, 'false', '是否开启realSense', True, cid=379)
def enableRealSense():
    pass


@config(Bool, 'false', '是否开启首次换模式的技能位置', True, cid=380)
def enableOperationShortCut():
    pass


@config(Bool, 'true', '是否开启手工装备', True, cid=381)
def enableManualEquip():
    pass


@config(Bool, 'true', '是否开启新手奖励', True, cid=382)
def enableNoviceReward():
    pass


@config(Bool, 'true', '是否开启大世界可交互第二阶段ui', True, cid=383)
def enableInteractiveObjReward():
    pass


@config(Bool, 'true', '是否开启怪物基础经验等级重算功能', True, cid=384)
def enableUseFormulaToCalcExp():
    pass


@config(Bool, 'true', '是否开启师徒值macaddress检测', False)
def enableApprenticeValMacAddresCheck():
    pass


@config(Bool, 'false', '是否检查成功进入跨服竞技场/战场', False)
def enableEnterDuelCheck():
    pass


@config(Bool, 'false', '是否开启个人空间', True, cid=385)
def enablePersonalZone():
    pass


@config(Bool, 'false', '是否开启龙炮功能', True, cid=386)
def enableBfBullet():
    pass


@config(Bool, 'true', '开启挂饰物理', True, cid=387)
def enableWearPhysics():
    pass


@config(Bool, 'false', '是否检查avatar创建', False)
def enableCheckAavatarCreate():
    pass


@config(Bool, 'false', '是否开启物品掉落来源查询', True, cid=388)
def enableItemSearchIcon():
    pass


@config(Bool, 'false', '是否开启新版物品掉落来源查询', True, cid=389)
def enableNewItemSearch():
    pass


@config(Bool, 'false', '是否开启VIP补领功能', False)
def enableVipCompensate():
    pass


@config(Bool, 'true', '是否开启业刹这个新职业，允许创建业刹号', True, cid=390)
def enableNewSchoolYeCha():
    pass


@config(Bool, 'true', '是否开启主角的Rpc错误报警')
def enableAvatarRpcErrorWarning():
    pass


@config(Bool, 'false', '是否开启男2', True, cid=391)
def enableMale2():
    pass


@config(Bool, 'true', '是否启用增量reloaddata')
def useIncrementalReloadData():
    pass


@config(Bool, 'true', '是否启用Item的Version')
def useItemVersion():
    pass


@config(Bool, 'true', '是否启用副本申请2sCD检测')
def enableEnteringFbCD():
    pass


@config(Bool, 'false', '是否开启选人界面的天气改变', True, cid=392)
def enableLoginWeather():
    pass


@config(Bool, 'false', '是否开启装备改造材料抵扣', True, cid=394)
def enableEquipDiKou():
    pass


@config(Bool, 'false', '是否开启二维码功能', True, cid=395)
def enableQRCode():
    pass


@config(Bool, 'false', '是否开启装备拆解', True, cid=396)
def enableDisassembleEquip():
    pass


@config(Bool, 'false', '是否开启活跃度', True, cid=397)
def enableActivation():
    pass


@config(Bool, 'true', '是否开启观战', True, cid=398)
def enableFightObserve():
    pass


@config(Bool, 'true', '是否战场VIP加成')
def enableBattleFieldVip():
    pass


@config(Bool, 'true', '是否开启dota战场排队时人数检查报警')
def enableDotaQueueItemNumCheck():
    pass


@config(Bool, 'true', '是否开启杀星', True, cid=399)
def enableShaxing():
    pass


@config(Bool, 'false', '是否开启新的副本进度面板', True, cid=400)
def enableNewFubenProgress():
    pass


@config(Bool, 'false', '是否TreasureBox生成物品的时候全局总控走base端')
def enableTreasureBoxGenItemLimitCalledInBase():
    pass


@config(Bool, 'false', '使用新的头像上传界面', True, cid=401)
def enableNewFigureUpload():
    pass


@config(Int, '100', '怪物统计报警阈值')
def monsterCheckMaxNum():
    pass


@config(Int, '50', '怪物统计报警范围')
def monsterCheckDist():
    pass


@config(Bool, 'false', '是否开启材料包制作', True, cid=402)
def enableMaterialBagManualLifeSkill():
    pass


@config(Bool, 'true', '是否开启公会场景中的怪物重生支持')
def enableReliveInGuildSpace():
    pass


@config(Bool, 'true', '跨服后金钱、声望、物品属性不一致后是否报警', False)
def enableCrossPropertyDiffWarning():
    pass


@config(Bool, 'true', '在邮件批量获取的时候检查活跃度', False)
def enableMailFetchCheckActivities():
    pass


@config(Bool, 'true', '是否开启家园', True, cid=403)
def enableHome():
    pass


@config(Bool, 'false', '是否开启家园仓库', True, cid=404)
def enableStorageHome():
    pass


@config(Bool, 'true', '是否开启选人界面自定义头像+内容上传', True, cid=405)
def enableUploadCharacterPhoto():
    pass


@config(Bool, 'false', '是否能创建女3业刹', True, cid=406)
def enableCreateFemale3Yecha():
    pass


@config(Bool, 'false', '是否能创建女2炎天', True, cid=407)
def enableCreateFemale2Yantian():
    pass


@config(Str, '', '禁用咨询tab，多个tabIndex用逗号隔开', True, cid=408)
def disableZixunTab():
    pass


@config(Bool, 'false', '是否开启福袋', True, cid=409)
def enableFuDaiProxy():
    pass


@config(Bool, 'true', '是否开启聊天框指令', True, cid=410)
def enableChatCommand():
    pass


@config(Bool, 'false', '是否开启备选装备栏', True, cid=411)
def enableSubEquipment():
    pass


@config(Bool, 'true', '是否开启装备属性共享', True, cid=412)
def enableShareEquipProp():
    pass


@config(Bool, 'false', '是否开启双人生死场', True, cid=413)
def enableTeamShengSiChang():
    pass


@config(Bool, 'false', '是否开启双人生死场假数据测试', True, cid=414)
def enableTeamShengSiChangFakeMan():
    pass


@config(Bool, 'false', '是否开启奇人奖励', True, cid=415)
def enableQiRenReward():
    pass


@config(Bool, 'false', '开启宝箱但不检查临时包裹')
def enableQuickOpenBox():
    pass


@config(Bool, 'true', '是否开启金钱log全服电视广播', False)
def enableCashLogBroadcast():
    pass


@config(Bool, 'true', '是否开启声望log全服电视广播', False)
def enableFameLogBroadcast():
    pass


@config(Bool, 'true', '是否开启GroupStub存盘优化')
def enableGroupStubShard():
    pass


@config(Bool, 'false', '开启新师徒出师修正')
def enableApprenticeGraduateRevise():
    pass


@config(Bool, 'false', '是否使用新的refreshscript')
def enableRefreshScriptNew():
    pass


@config(Bool, 'false', '是否开启快速refreshscript')
def enableQuickRefresh():
    pass


@config(Bool, 'true', '是否开启竞技场位置检测功能')
def enableArenaPositionCheck():
    pass


@config(Bool, 'true', '是否开启竞技场季后赛观战功能', True, cid=416)
def enableArenaPlayoffsLive():
    pass


@config(Bool, 'true', '是否开启GCGO')
def enableGcGo():
    pass


@config(Bool, 'false', '是否开启70_79等级段季后赛功能')
def enableArenaPlayoffsStatue():
    pass


@config(Bool, 'true', '是否可交互物件检测功能')
def enableInteractiveCheckPlayer():
    pass


@config(Bool, 'false', '是否开启装备改造精炼tab', True, cid=417)
def enableEquipChangeEnhance():
    pass


@config(Bool, 'false', '是否开启装备改造重铸tab', True, cid=418)
def enableEquipChangeReforge():
    pass


@config(Bool, 'true', '是否开启dota的doubleCheck报警')
def enableDotaDoubleCheckReport():
    pass


@config(Bool, 'false', '是否开启装备改造段位tab', True, cid=419)
def enableEquipChangeStar():
    pass


@config(Bool, 'false', '是否开启装备改造套装tab', True, cid=420)
def enableEquipChangeSuit():
    pass


@config(Bool, 'false', '是否开启装备改造纹印tab', True, cid=421)
def enableEquipChangeGem():
    pass


@config(Bool, 'false', '是否开启免费精炼觉醒重铸', True, cid=422)
def enableFreeJuexingRebuild():
    pass


@config(Bool, 'true', '是否开启退出同步Avatar形象到APP', True, cid=423)
def enableLogoutCharSnapshot():
    pass


@config(Bool, 'false', '是否开启七夕愿榜', True, cid=424)
def enableFestivalWishMadeView():
    pass


@config(Bool, 'false', '是否开启掠影谷四圣令自动使用功能', True, cid=425)
def enableAutoUseBattleFieldShopItem():
    pass


@config(Bool, 'false', '是否开启客户端的数据包完整性检查', True, cid=426)
def enableClientPackageCheck():
    pass


@config(Bool, 'false', '是否开启云垂商会', True, cid=427)
def enableYunChuiShop():
    pass


@config(Bool, 'false', '是否开启随身云垂商会', True, cid=428)
def enablePrivateYunChuiShop():
    pass


@config(Bool, 'false', '是否开启在特定地图死亡复活无双影响')
def enableWsResetOnDieOrRelive():
    pass


@config(Bool, 'false', '是否开启公会跑男', True, cid=430)
def enableGuildRunMan():
    pass


@config(Bool, 'false', '是否开启家园房间重排')
def enableRearrangementRoom():
    pass


@config(Bool, 'true', '是否开启开宝箱全部队员发奖励')
def enableGiveAllTeamMemberReward():
    pass


@config(Bool, 'false', '是否开启首充奖励', True, cid=431)
def enableFirstChargeReward():
    pass


@config(Bool, 'true', '是否开启部分怪物结算数值压制人')
def enableMonsterDmgReductionVSAvatar():
    pass


@config(Bool, 'false', '是否开启充值等级奖励', True, cid=432)
def enableChargeLvReward():
    pass


@config(Bool, 'true', '是否开启装备透明材质染色', True, cid=433)
def enableEquipTransparenceDye():
    pass


@config(Bool, 'true', '是否开启新公会引导', True, cid=434)
def enableGuildTutorialNew():
    pass


@config(Bool, 'true', '是否开启新公会引导奖励邮件提醒', True, cid=435)
def enableGuildTutorialMail():
    pass


@config(Bool, 'true', '是否开启精灵系统', True, cid=436)
def enableHelpSystem():
    pass


@config(Bool, 'false', '是否开启家园结契', True, cid=437)
def enableHomeIntimacy():
    pass


@config(Bool, 'false', '是否开启活动开启前广播', False)
def enableActivityPreNotify():
    pass


@config(Bool, 'true', '是否开启俸禄中心', True, cid=438)
def enableAward():
    pass


@config(Bool, 'false', '是否开启运营顶栏', True, cid=439)
def enableRewardGiftActivityIcons():
    pass


@config(Bool, 'false', '是否开启特惠活动', True, cid=440)
def enableActivitySale():
    pass


@config(Bool, 'false', '是否开启新手期付费', True, cid=441)
def enableNewbiePay():
    pass


@config(Int, str(int(time.time())), '新手期付费功能开启时间', True, cid=442)
def getNewbiePayEnableTime():
    pass


@config(Bool, 'false', '是否开启福利活动', True, cid=443)
def enableWelfare():
    pass


@config(Bool, 'true', '是否开启个人空间APP数据互通', True, cid=444)
def enablePersonalZoneInterface():
    pass


@config(Bool, 'false', '是否开启搭讪加好友通知APP端', False)
def enableAddFriendPostMsg2App():
    pass


@config(Bool, 'false', '是否开启个人空间APP语音互通', True, cid=445)
def enablePersonalZoneAudio():
    pass


@config(Bool, 'true', '是否开启区域事件', True, cid=446)
def enableWorldArea():
    pass


@config(Bool, 'true', 'enable GM ip address check?', True, cid=447)
def enableCheckGmIP():
    pass


@config(Bool, 'true', 'enable exception log?', True, cid=448)
def enableExceptionLog():
    pass


@config(Bool, 'false', '是否打开新的属性计算，只能用于性能测试')
def enableNewPropCalc():
    pass


@config(Bool, 'false', '是否只用新的属性计算')
def enableOnlyNewPropCalc():
    pass


@config(Bool, 'true', '是否在旧属性计算中查找属性Diff')
def enableInnerPropCheck():
    pass


@config(Bool, 'false', '是否定时器校验新旧属性计算结果Diff')
def enableTimerPropCheck():
    pass


@config(Float, '0.3', '是否定时器校验新旧属性计算结果Diff的概率')
def probTimerPropCheck():
    pass


@config(Bool, 'false', '中秋节登录loading图', True, cid=449)
def enableZhongQiuLoadingPic():
    pass


@config(Bool, 'false', '是否开启弹劾统帅', True, cid=450)
def enableWWArmyImpeach():
    pass


@config(Bool, 'true', '是否开启stream msgpack优化')
def enableServerStartCheck():
    pass


@config(Bool, 'true', '是否开启公会强盗入侵', True, cid=451)
def enableGuildRobber():
    pass


@config(Bool, 'false', 'enable kick the inactive players', True, cid=452)
def enableKickInactivePlayer():
    pass


@config(Bool, 'true', '是否活动推送改为弹王者之路', True, cid=453)
def enablePlayRecommPush():
    pass


@config(Bool, 'false', '是否支持预览家具', True, cid=454)
def enablePreviewHomeFurniture():
    pass


@config(Bool, 'true', 'enable mail cash', True, cid=455)
def enableMailCash():
    pass


@config(Bool, 'true', '是否发送通知类的GM邮件', True, cid=456)
def enableIngameGMMail():
    pass


@config(Bool, 'true', 'enable homosexual intimacy', True, cid=457)
def enableHomosexualIntimacy():
    pass


@config(Bool, 'true', 'enable festival event', True, cid=458)
def enableFestivalEvent():
    pass


@config(Bool, 'true', '背包仓库中是否使用优化后的道具排序方式', False)
def enableOptimizedItemSortFunc():
    pass


@config(Bool, 'false', '试衣间扩建', True, cid=459)
def enableFittingRoomLvUp():
    pass


@config(Bool, 'false', '房间扩建', True, cid=460)
def enableEnlargeHomeRoom():
    pass


@config(Bool, 'True', '是否开启国战公会联赛', True, cid=461)
def enableWWGuildTournament():
    pass


@config(Bool, 'true', '是否开启亡命岛', True, cid=462)
def enableWMD():
    pass


@config(Bool, 'false', '开启方向键移动家具', True, cid=463)
def enableKeyBoardMoveFurniture():
    pass


@config(Bool, 'false', '开启转职', True, cid=464)
def enableSchoolTransfer():
    pass


@config(Bool, 'true', '开启转职状态检测', True, cid=465)
def enableSchoolTransferStatusCheck():
    pass


@config(Bool, 'true', '开启转职条件判断', True, cid=466)
def enableSchoolTransferConditionCheck():
    pass


@config(Bool, 'false', '开启随身活动商店', True, cid=467)
def enablePrivateShop():
    pass


@config(Bool, 'false', '开启技能抵扣', True, cid=468)
def enableSkillDiKou():
    pass


@config(Bool, 'true', '是否开启云垂排行榜工会成员奖励模式', True, cid=469)
def enableYunChuiRankGuildMemberAward():
    pass


@config(Int, str(int(time.time())), '云垂新奖励模式第一次启用时间', True, cid=470)
def clanWarFirstOpenTimeAfterNewReward():
    pass


@config(Bool, 'false', '开启空间语音', True, cid=471)
def enablePersonalZoneVoice():
    pass


@config(Bool, 'true', '是否开启领地战排行榜公会成员参战奖励', True, cid=472)
def enableClanWarTopGuildMemberAward():
    pass


@config(Bool, 'true', '是否开启任务接取时quests和questData校验', False)
def enableQuestsAndQuestDataCheck():
    pass


@config(Bool, 'false', '是否开启怪物入战随机喊话', True, cid=473)
def enableMonsterTalkInCombat():
    pass


@config(Bool, 'false', '是否开启组队强制填写详细功能', True, cid=474)
def enableGroupDetailForcely():
    pass


@config(Bool, 'true', '是否外网是否已开', False)
def enableCheckOuterNet():
    pass


@config(Bool, 'true', '是否开启新阵营敌对规则', True, cid=475)
def enableNewCampRelation():
    pass


@config(Bool, 'false', '结契对象是否可以摆放avatar家具', True, cid=476)
def enableFittingRoomIntimacy():
    pass


@config(Int, '0', '开启商城网页', True, cid=477)
def enableShowMallWeb():
    pass


@config(Bool, 'false', '扫码支付开关', True, cid=478)
def enableQrcodeRecharge():
    pass


@config(Bool, 'false', '开启家具pitch旋转', True, cid=479)
def enableFurnitureRotatePitch():
    pass


@config(Bool, 'false', '是否开启公会联赛战场团长变更功能', True, cid=480)
def enableChangeLeaderInFortBattleField():
    pass


@config(Bool, 'false', '是否计算祝福力诅咒力')
def enableCalcBlessAndCurse():
    pass


@config(Bool, 'false', '开启createfuben指令忽略进本检查', True, cid=481)
def enableCreateFubenIgnoreCheck():
    pass


@config(Float, str(2.0), '新服开服时间之后开外网时间', False)
def newServerOpenOuterNetDelay():
    pass


@config(Int, str(200), '新服开外网时间之前最大人数上限', False)
def newServerMassLimitBeforeOpenOuterNet():
    pass


@config(Bool, 'true', '是否新服前两小时人数上限设置', False)
def enableNewServerMassLimitBeforeOpenOuterNet():
    pass


@config(Bool, 'false', '家园互动喊话', True, cid=482)
def enableInteractiveHomeChat():
    pass


@config(Bool, 'false', '可交互物件公主抱', True, cid=483)
def enableInteractiveCoupleEmote():
    pass


@config(Bool, 'false', '新版拍卖行', True, cid=484)
def enableTabAuction():
    pass


@config(Bool, 'false', '是否面板开关GC', True, cid=485)
def enableCtrlWidgetGC():
    pass


@config(Bool, 'true', '是否开启时装包续期', True, cid=486)
def enableFashionBagRenew():
    pass


@config(Bool, 'false', '是否开启直升', False)
def enableStraightLvUp():
    pass


@config(Bool, 'false', '是否开启app/微信绑定奖励功能', True, cid=487)
def enableBindReward():
    pass


@config(Bool, 'false', '是否开启buffer动态属性计算的功能', True, cid=488)
def enableBufferPropQuery():
    pass


@config(Bool, 'true', '是否支持公会联盟', True, cid=489)
def enableClan():
    pass


@config(Bool, 'false', '是否开启装备蕴灵', True, cid=490)
def enableEquipSoul():
    pass


@config(Bool, 'true', '是否开启装备蕴灵激活特效', True, cid=491)
def enableEquipSoulFlyEffect():
    pass


@config(Bool, 'false', '是否开启装备蕴灵多方案', True, cid=492)
def enableEquipSoulSchemes():
    pass


@config(Bool, 'false', '是否开始聊天链接', True, cid=493)
def enableChatLink():
    pass


@config(Bool, 'false', '是否开启直升突破', True, cid=494)
def enableLevelBreakthrough():
    pass


@config(Bool, 'true', '是否开启新角色novice异常报错', False)
def enableSendNewAvatarNoviceError():
    pass


@config(Bool, 'false', '是否开启强制设置novice为true', False)
def enableSetNoviceTrue():
    pass


@config(Bool, 'false', '是否缓存UI界面', True, cid=495)
def enableCacheUI():
    pass


@config(Bool, 'false', '是否打开训练场业刹职业', True, cid=496)
def enableTrainingAreaYeCha():
    pass


@config(Str, '1111111111000', '设置转职转出职业限制', True, cid=497)
def schoolTransferOutLimit():
    pass


@config(Str, '1111111111000', '设置转职转入职业限制', True, cid=498)
def schoolTransferInLimit():
    pass


@config(Bool, 'true', '是否打开捏脸预览', True, cid=499)
def enableCharacterSharePreview():
    pass


@config(Bool, 'false', '是否开启stream优化')
def enableStreamOptimization():
    pass


@config(Bool, 'false', '是否开启stream优化检查')
def enableStreamCheckAlways():
    pass


@config(Bool, 'false', '是否开启stream msgpack优化')
def enableStreamMsgPack():
    pass


@config(Bool, 'false', '是否开启常用函数优化')
def enableFrequentCache():
    pass


@config(Bool, 'false', '是否开启常用函数优化检查')
def enableFrequentCacheCheck():
    pass


@config(Bool, 'false', '是否开启新战场弱者保护机制')
def enableBFNewStaticProtect():
    pass


@config(Bool, 'true', '是否开启国战掠夺传送服务端可达检测')
def enableTeleportServerCheck():
    pass


@config(Bool, 'true', '是否开启左手武器挂接到右手上的cue事件', True, cid=500)
def enableAttachWeaponCue():
    pass


@config(Bool, 'false', '是否开启技能距离过远走进优化', True, cid=501)
def enableSkillDistAutoOpt():
    pass


@config(Int, str(0), 'CPU空跑循环数（建议数10000的倍数）')
def dummyCPULoopCount():
    pass


@config(Bool, 'true', '是否跨服后加容错检查', False)
def enableCrossServerSpaceCheck():
    pass


@config(Bool, 'true', '是否开启转职后竞技场技能点重算')
def enableArenaSkillPointReCalc():
    pass


@config(Bool, 'true', '启用新的GfxValue方法', True, cid=502)
def enableNewGfxValue():
    pass


@config(Bool, 'true', '是否开启副本圆桌功能', False)
def enableFubenRoundTable():
    pass


@config(Bool, 'false', '是否开启家园测试地图', False)
def debugHomeMap():
    pass


@config(Bool, 'false', '是否使用新右键菜单', True, cid=503)
def enableNewMenu():
    pass


@config(Bool, 'false', '是否开启pvp追赶系统', True, cid=504)
def enablePursuePvp():
    pass


@config(Bool, 'false', '是否开启护身符追赶系统', True, cid=505)
def enablePursueYaopei():
    pass


@config(Bool, 'false', '是否开启房屋权限设置功能', True, cid=506)
def enableHomePermissionSet():
    pass


@config(Bool, 'false', '是否开启hotKey冲突处理', False)
def enableHotKeyCheckConflict():
    pass


@config(Bool, 'true', '是否开启Avatar登录下发优化', True, cid=507)
def enableSendAvatarDataOptimization():
    pass


@config(Bool, 'true', '是否开启Avatar登录物品数据优化', True, cid=508)
def enableSendAvatarDataNoChangeToItem():
    pass


@config(Bool, 'false', '开启方块优化', True, cid=509)
def enableCubeOptimization():
    pass


@config(Int, '1500', '开启方块优化', True, cid=510)
def homeCubeMaxNum():
    pass


@config(Int, '2', '军需战一周开放多少次,才上传军需分')
def worldWarRobMaxWeeklyOpen():
    pass


@config(Int, '0', '结契的亲密度等级下限:为0时读表，大于0时生效')
def acIntimacyMinLv():
    pass


@config(Bool, 'false', '是否开启任务材料包扣除', True, cid=511)
def enableQuestMaterialBag():
    pass


@config(Bool, 'false', '是否开启区域事件怪物强度调整')
def enableAreaEventMonsterPowerSet():
    pass


@config(Bool, 'false', '是否开启怪物红圈叠加调整机制')
def enableMonsterOverlapChange():
    pass


@config(Bool, 'false', '是否开启复合商店普通售出', True, cid=512)
def enableSellNormalToCompositeShop():
    pass


@config(Bool, 'true', '是否开启Boss入战分部件检测')
def enableBossVirtualMonsterCheck():
    pass


@config(Bool, 'false', '是否开启UI统计Log', True, cid=513)
def enableUIStatistisc():
    pass


@config(Bool, 'false', '是否可以退房', True, cid=514)
def enableRemoveHome():
    pass


@config(Bool, 'false', '是否启用战场的dummyCheck', False)
def enableBfDummyCheck():
    pass


@config(Bool, 'false', '结契对象昵称的设置开关', True, cid=515)
def enableIntimacyTgtNickName():
    pass


@config(Bool, 'true', '技能宏开关', True, cid=516)
def enableSkillMacro():
    pass


@config(Bool, 'false', '联运相关LOG是否开启', True, cid=517)
def enableLianYunStatistisc():
    pass


@config(Bool, 'true', '检查队列的负载长度是否开启', True, cid=518)
def enableCheckTaskLoad():
    pass


@config(Bool, 'false', '是否开启Boss强度调整')
def enableBossPowerSet():
    pass


@config(Bool, 'true', '跨服好友服务器事件检查是否开启', True, cid=519)
def enableGlobalFriendServerProgressCheck():
    pass


@config(Bool, 'false', '组队跟随', True, cid=520)
def enableGroupFollow():
    pass


@config(Bool, 'false', '组队跟随操作开放', True, cid=521)
def enableTempGroupFollow():
    pass


@config(Bool, 'false', '是否开启组队跟随自动战斗', True, cid=522)
def enableGroupFollowAutoAttack():
    pass


@config(Int, '5', '跨服拍卖行自动刷新间隔', True, cid=523)
def xConsignClientAutoRefresh():
    pass


@config(Bool, 'true', '是否开启国战活动负载记录')
def enableCheckWorldWarLoad():
    pass


@config(Bool, 'false', '是否缓存物品tip', True, cid=524)
def enableCacheTip():
    pass


@config(Bool, 'false', '是否开启载具技能栏第二版', True, cid=525)
def enableZaijuV2():
    pass


@config(Bool, 'false', '是否开启问卷功能', True, cid=526)
def enableQuestion():
    pass


@config(Bool, 'false', '是否开启上周上榜人上线通知功能', False)
def enableNotifyLogOnTopDataBack():
    pass


@config(Bool, 'false', '是否开启新手七天时装功能', True, cid=527)
def enableXinshouSevenDay():
    pass


@config(Bool, 'false', '是否开启轻功自动寻路', True, cid=528)
def enableQingGongPathFinding():
    pass


@config(Bool, 'false', '是否开启排行榜富贵值', True, cid=529)
def enableRankingHomeWealth():
    pass


@config(Bool, 'false', '是否开启mongolog的schema检查功能')
def enableMongoLogSchemaCheck():
    pass


@config(Bool, 'true', '是否开启同一时间进本数过多报警')
def enableAlarmOfEnterFubenTooMany():
    pass


@config(Int, '8', '设置进本次数报警阀值')
def enterFubenTooManyAlarmCount():
    pass


@config(Bool, 'true', '是否开启同一时间WriteToDB过多报警')
def enableAlarmOfWriteToDBTooMany():
    pass


@config(Int, '5', '设置CellApp内WriteToDB一秒内次数报警阀值')
def enterWriteToDBTooManyAlarmCount():
    pass


@config(Bool, 'true', '是否开启区域事件调试')
def enableDebugWorldAreaManager():
    pass


@config(Bool, 'true', '是否开启忽略TPOS的优化', True, cid=530)
def enableNeedIgnoreTpos():
    pass


@config(Bool, 'false', '是否开启战灵开关', True, cid=531)
def enableSummonedSprite():
    pass


@config(Bool, 'true', '是否开启任务获得战灵的功能', False)
def enableGetSummonedSpriteByQuest():
    pass


@config(Bool, 'true', '是否允许战灵相关统计类Mongo日志')
def enableSpriteStatLog():
    pass


@config(Bool, 'false', '是否开启玩法外观评价', True, cid=532)
def enableEvaluate():
    pass


@config(Bool, 'false', '是否开启组队头顶标识', True, cid=533)
def enableTeamIdentity():
    pass


@config(Int, '28345', '设置区域事件怪物调试Id')
def debugWorldAreaMonserCharType():
    pass


@config(Bool, 'false', '是否开启系统消息好友', True, cid=534)
def enableSystemMessage():
    pass


@config(Bool, 'true', '是否开启金钱日常玩法', True, cid=535)
def enableWorldQuestLoopRefresh():
    pass


@config(Bool, 'false', '是否开启拍卖行一口价限制', True, cid=536)
def enableConsignMaxFixedPrice():
    pass


@config(Bool, 'true', '是否开启离线好友消息推送', True, cid=537)
def enableOfflineFriendNotifyMsg():
    pass


@config(Bool, 'true', '是否随机取名', True, cid=538)
def enableRandomName():
    pass


@config(Bool, 'false', '是否开启随机loading图', True, cid=539)
def enableRandomLoadingPic():
    pass


@config(Bool, 'true', '是否可以访问跨服家园', True, cid=540)
def enableCrossServerHome():
    pass


@config(Bool, 'true', '是否在做hotfix和runscript之前检查一下文件是否符合python语法', True, cid=541)
def enableCheckRunscriptFileErrors():
    pass


@config(Bool, 'false', '是否开启荣誉面板V2', True, cid=542)
def enableHonorV2():
    pass


@config(Bool, 'false', '是否开启门派声望', True, cid=543)
def enableSchoolFame():
    pass


@config(Bool, 'true', '是否开启小游戏', True, cid=544)
def enableMiniGame():
    pass


@config(Bool, 'true', '是否开启好友推荐', True, cid=545)
def enableRecommendFriend():
    pass


@config(Int, '0', '好友推荐测试服务器ID')
def recommendFriendTestHostId():
    pass


@config(Int, '0', '好友推荐测试玩家GBID')
def recommendFriendTestGbId():
    pass


@config(Bool, 'true', '是否开启兴奋点功能开启检测', True, cid=546)
def enableExcitementFeatureCheck():
    pass


@config(Int, '40', '好友推荐在线数目上限')
def recommendFriendOnlineMaxNum():
    pass


@config(Bool, 'false', '是否开启低等级免费转职', True, cid=547)
def enableLowLvFreeSchoolTransfer():
    pass


@config(Bool, 'true', '是否开启当被动技能用到属性前置状态时的报警')
def warnOnPSkillPreconditionAttrUsed():
    pass


@config(Bool, 'true', '是否开启跨服个人空间', True, cid=548)
def enableCrossServerZone():
    pass


@config(Bool, 'false', '是否开启玩家在配置地图的复活基础时间动态可调整', True, cid=549)
def enableCalcAvatarReliveIntervalDynamicAdjust():
    pass


@config(Bool, 'true', '是否开启兴奋点功能客户端UI', True, cid=550)
def enableExcitementClientShow():
    pass


@config(Bool, 'true', '是否开启跨服双人坐骑', True, cid=551)
def enableCrossRideTogether():
    pass


@config(Bool, 'true', '是否开启跨服备选装备栏', True, cid=552)
def enableCrossSubEquipment():
    pass


@config(Bool, 'true', '是否开启跨服使用公会技能', True, cid=553)
def enableCrossUseGuildMemberSkill():
    pass


@config(Bool, 'false', '是否开启轻功翅膀教学视频图标推送', True, cid=554)
def enableQinggongWingTutorialIcon():
    pass


@config(Bool, 'false', '是否开启Cython优化')
def enableCythonSkillObject():
    pass


@config(Bool, 'false', '是否开启UIProfile', True, cid=555)
def enableUIProfile():
    pass


@config(Int, '10', '每帧同时更新姓名版的数量', True, cid=556)
def enableToplogoTotalOptimize():
    pass


@config(Bool, 'true', '是否开启公会答题', True, cid=557)
def enableGuildPuzzle():
    pass


@config(Bool, 'false', '是否开启特效加载优化', True, cid=558)
def enableEffectLoadOptimize():
    pass


@config(Bool, 'false', '开启新师徒迭代', True, cid=559)
def enableApprenticeOptimize20174():
    pass


@config(Bool, 'false', '是否开启US师徒推荐', True, cid=560)
def enableUSRecommendApprentice():
    pass


@config(Int, '0', '师徒推荐测试服务器ID')
def recommendApprenticeTestHostId():
    pass


@config(Int, '0', '师徒推荐测试玩家GBID')
def recommendApprenticeTestGbId():
    pass


@config(Bool, 'false', '语音录制上传翻译', True, cid=561)
def enableSoundRecord():
    pass


@config(Bool, 'false', 'App语音录制上传翻译', True, cid=562)
def enableSoundRecordFromApp():
    pass


@config(Bool, 'true', '是否开启可交互组件任务', True, cid=563)
def enableQuestInteractive():
    pass


@config(Bool, 'false', '是否开启一条龙', True, cid=564)
def enableQuestLoopChain():
    pass


@config(Int, '1497484800', '一条龙开启时间', True, cid=565)
def questLoopChainStartTime():
    pass


@config(Bool, 'true', '是否开启无尽挑战', True, cid=566)
def enableEndlessChallenge():
    pass


@config(Bool, 'true', '是否开启npc双人答题', True, cid=567)
def enableNpcPairPuzzle():
    pass


@config(Bool, 'false', '是否开启驱魔优化', True, cid=568)
def enableQumoOptimize():
    pass


@config(Bool, 'false', '是否开启日常任务无尽循环模式', True, cid=569)
def enableEndlessLoopMode():
    pass


@config(Bool, 'false', '是否增加首轮Bonus物品奖励', True, cid=570)
def enableFirstLoopBonusReward():
    pass


@config(Bool, 'true', '是否开启魂界战场主角呼救')
def enableAvatarCallHelpOnDotaBattle():
    pass


@config(Bool, 'false', '是否开启toplogo优化', True, cid=571)
def enableTopLogoOptimize():
    pass


@config(Bool, 'false', '是否开启toplogo优化(toplogo的重用机制)', True, cid=572)
def enableTopLogoSuperOptimize():
    pass


@config(Int, '-1', '使资讯某个tab页置顶', True, cid=573)
def setZixunTabTop():
    pass


@config(Bool, 'true', '是否开启开箱记录查询功能', True, cid=574)
def enableBoxItemHistory():
    pass


@config(Bool, 'false', '是否开启PNG个人头像', True, cid=575)
def enablePNGProfileIcon():
    pass


@config(Bool, 'false', '是否开启个人空间战场数据', True, cid=576)
def enablePersonalSpaceBfData():
    pass


@config(Int, '1499011200', '公会联赛赛季开始时间', True, cid=577)
def gtnSeasonStartTime():
    pass


@config(Bool, 'false', '开启内存环引用检查')
def enableDestroyEntityCheck():
    pass


@config(Bool, 'true', '是否开启公会联赛赛季', True, cid=578)
def enableGuildTournamentSeason():
    pass


@config(Bool, 'true', '是否开启门派委托系统', True, cid=579)
def enableOpenSchoolEntrust():
    pass


@config(Bool, 'false', '是否开启师徒小目标', True, cid=580)
def enableApprenticeTarget():
    pass


@config(Bool, 'true', '应用新的视频选项', True, cid=581)
def enableNewVideoConfig():
    pass


@config(Str, '', '国战军队候选开启指定分组,特殊处理使用, 默认应该为空字符串')
def worldWarVoteGroupType():
    pass


@config(Bool, 'true', '是否开启副本新首杀机制', True, cid=582)
def enableFirstKill():
    pass


@config(Bool, 'true', '是否开启MultiCellFubenManager拆分到不同的base上')
def enableSplitFbMgr():
    pass


@config(Bool, 'false', '是否开启家园宝箱功能')
def enableHomeTreasureBox():
    pass


@config(Str, '123.58.167.166:8181', 'deeppeek外服角色的gtAdmin的IP:PORT', True, cid=583)
def deeppeekAddress():
    pass


@config(Bool, 'true', '是否开启Npc加载lod', True, cid=584)
def enableHideNpc():
    pass


@config(Bool, 'false', '是否开启小地图位置拟合', True, cid=585)
def enableDotaHeroTweenPos():
    pass


@config(Bool, 'false', '是否开启翅膀坐骑饱食度', True, cid=586)
def enableRideWingDurability():
    pass


@config(Bool, 'true', '是否开启新时装转换功能', True, cid=587)
def enableFashionExhange():
    pass


@config(Int, '150', '表现类可见NPC数量', True, cid=588)
def getNpcModelMaxCnt():
    pass


@config(Bool, 'false', '在主角创建的时候，对cellData使用copy而不是deepcopy')
def useCopyOnAvatarCellDataCreate():
    pass


@config(Bool, 'false', '组队更随，队员跟随队长寻路', True, cid=589)
def enableGroupFollowHeaderPath():
    pass


@config(Bool, 'false', '是否开启自动任务', True, cid=590)
def enableAutoQuest():
    pass


@config(Bool, 'true', '精确计算HOT,DOT持续结算buff的持续时间', True, cid=591)
def enableAccurateDotTime():
    pass


@config(Bool, 'true', '是否开启运维礼包功能', True, cid=592)
def enableGmFLowbackBonus():
    pass


@config(Bool, 'true', '是否开启家园清理', True, cid=593)
def enableClearDeadHome():
    pass


@config(Bool, 'false', '是否可以直接关闭实名认证弹窗', True, cid=594)
def enableForceCloseRealNameWnd():
    pass


@config(Bool, 'false', '是否开启动作内存的新统计', True, cid=595)
def enableNewAnimationMemoryLimit():
    pass


@config(Bool, 'false', '是否结伴玩家装备展示功能', True, cid=596)
def enablePartnerEquipment():
    pass


@config(Bool, 'true', '是否允许一次性使用多个物品（堆叠在一起）', True, cid=597)
def enableUseMultipleItems():
    pass


@config(Bool, 'true', '是否自动修复特定错误的任务', False)
def enableAutoFixSomeQuest():
    pass


@config(Bool, 'true', '是否开启 不显示的实体的toplogo不创建', True, cid=598)
def enableNotCreateTopLogoForHide():
    pass


@config(Bool, 'true', '是否控制多开党玩家的活跃度获取', False)
def enableActivationSameMacLimit():
    pass


@config(Bool, 'false', '是否开启redis连接', True, cid=599)
def enableRedisConnection():
    pass


@config(Bool, 'false', '是否开启至尊回归新功能', True, cid=600)
def enableZhiZunHuiGui():
    pass


@config(Bool, 'false', '是否开启redis访问接口', True, cid=601)
def enableRedisOperation():
    pass


@config(Bool, 'true', '是否启用家园founder自定义数据表', True, cid=602)
def enableCustomHomeFounderDataTable():
    pass


@config(Bool, 'false', '是否仅启用家园founder自定义数据表，开关修改后下次启动founder将直接使用game_表', True, cid=603)
def enableOnlyCustomHomeFounderDataTable():
    pass


@config(Bool, 'false', '是否使用天谕2UI', True, cid=604)
def enableUIVersion2():
    pass


@config(Bool, 'true', '是否开启公会任务优化', True, cid=605)
def enableGuildQuestOptimize():
    pass


@config(Bool, 'true', '是否开启会长自动退位', True, cid=606)
def enableGuildLeaderAutoResign():
    pass


@config(Bool, 'true', '是否开启会长自动退位客户端面板', True, cid=607)
def enableClientGuildLeaderAutoResign():
    pass


@config(Bool, 'true', '是否开启国战弱势服BUFF', True, cid=608)
def enableWorldWarYoungServerBuff():
    pass


@config(Bool, 'true', '是否开启战场弱势服BUFF', True, cid=609)
def enableBattleFieldYoungServerBuff():
    pass


@config(Bool, 'true', '是否开启下线记录副本log')
def enableGenFubenLogOnLogOff():
    pass


@config(Bool, 'false', '是否开启trap光环', True, cid=610)
def enableTrapAura():
    pass


@config(Bool, 'true', '是否开启连接多个hub', False)
def enableMultipleHubs():
    pass


@config(Bool, 'false', '是否在商店中显示任务道具', True, cid=611)
def enableQuestFlagInShop():
    pass


@config(Bool, 'false', '是否开启名人堂', True, cid=612)
def enableHallOfFame():
    pass


@config(Bool, 'true', '是否开启魂界log', True, cid=613)
def enablePrintBfDotaLog():
    pass


@config(Bool, 'false', '是否开启hotfix/run_script/refreshData的popo报警', True, cid=614)
def enablePopoReportOnServerHotfix():
    pass


@config(Bool, 'true', '是否开启大数据引导', True, cid=615)
def enableCareerGuilde():
    pass


@config(Bool, 'false', '是否开启吟唱和引导的flag', True, cid=616)
def enableSpellAndGuideFlag():
    pass


@config(Int, str(int(time.time())), '开启会长自动退位时间', True, cid=617)
def guildLeaderAutoResignEnableTime():
    pass


@config(Bool, 'false', '是否开启个人空间换肤功能', True, cid=618)
def enablePersonalZoneSkin():
    pass


@config(Bool, 'true', '是否开启百凤宴', True, cid=619)
def enableChickenFood():
    pass


@config(Bool, 'false', '是否开启组队邀请开关', True, cid=620)
def enableTeamInvite():
    pass


@config(Bool, 'false', '是否开启公会鉴星', True, cid=621)
def enableGuildMassAstrology():
    pass


@config(Bool, 'false', '是否开启US好友标签查询', True, cid=622)
def enableFriendTag():
    pass


@config(Bool, 'false', '是否开启萌妹团活动', True, cid=623)
def enableMissTianyu():
    pass


@config(Int, '1504767540', '萌妹团活动截止时间', True, cid=624)
def missTianyuEndtime():
    pass


@config(Bool, 'false', '是否开启名人堂榜单全部功能', True, cid=625)
def enableHallOfFameAll():
    pass


@config(Bool, 'false', '是否开启从面板领取补偿奖励', True, cid=626)
def enalbeGetCompensationFromGUI():
    pass


@config(Bool, 'true', '开启400*400大头像上传', True, cid=629)
def enableBigHeadSnapShot():
    pass


@config(Bool, 'false', '是否开启血蓝池', True, cid=630)
def enableHpMpPool():
    pass


@config(Bool, 'false', '是否开启在分解装备时预先剥离')
def enablePeelBeforeDisassembleEquip():
    pass


@config(Bool, 'false', '是否开启拾取时的任务检查', False)
def enableQuestCheckOnPickItem():
    pass


@config(Bool, 'false', '是否开启白虎雇佣军', True, cid=631)
def enableWorldWarBattleYoungHire():
    pass


@config(Bool, 'false', '是否开启二次确认面板的消耗物品时自动云垂积分抵扣', True, cid=632)
def enableYunChuiScoreDikou():
    pass


@config(Bool, 'false', '是否开启二次确认面板的消耗物品时自动天币抵扣', True, cid=633)
def enableCoinDikou():
    pass


@config(Bool, 'true', '是否开启公会鉴星', True, cid=634)
def enableGuildIdentifyStar():
    pass


@config(Bool, 'true', '是否开启新手引导分享功能', True, cid=635)
def enableSkillHierogramShare():
    pass


@config(Bool, 'false', '是否开启按规则收集玩家的客户端性能数据', True, cid=636)
def enableClientPerformanceFilter():
    pass


@config(Bool, 'true', 'states数据延迟一帧生效', True, cid=637)
def enableStatesNextFrame():
    pass


@config(int, '-1', '是否开启gatherInput缓存', True, cid=638)
def enableGatherInputCache():
    pass


@config(Bool, 'false', '是否开启名人堂历届数据和雕像', True, cid=639)
def enableHofHistoryAndStatue():
    pass


@config(Bool, 'false', '是否在高负载场景同步锁定目标的信息', True, cid=641)
def enableTargetLockedUpdateInHighLoadScene():
    pass


@config(Bool, 'false', '是否显示名人堂按钮', True, cid=642)
def enableHideHallOfFameBtn():
    pass


@config(Bool, 'false', '是否开启禁止点击名人堂特定榜单按钮', True, cid=643)
def enableHallOfFameDisableTabBtn():
    pass


@config(Int, '0', '同一帧同一个gfxValue调用次数阈值，超过报警', True, cid=644)
def gfxValueLimitCall():
    pass


@config(Bool, 'false', '是否开启hp和mp广播优化', True, cid=645)
def enableHpMpOptimization():
    pass


@config(Bool, 'false', '是否开启脱战再次寻路功能', True, cid=646)
def enableRestartPathFindAfterCombat():
    pass


@config(Bool, 'true', '是否把新服特惠活动改为新手特惠活动', True, cid=647)
def enableNewPlayerActivity():
    pass


@config(Float, '0.0', '是否记录load图时间的概率', True, cid=648)
def propOfLogLoadSpaceTime():
    pass


@config(Bool, 'false', '是否开启物品祈福功能', True, cid=649)
def enableUseItemWish():
    pass


@config(Int, '500000', 'PVP输出超阈值报警')
def pvpHurtPopoThreshold():
    pass


@config(Bool, 'true', '撒喜糖功能')
def enableMarriageShareCandy():
    pass


@config(Bool, 'true', '是否开启周活跃度功能', True, cid=650)
def enableWeekActivation():
    pass


@config(Bool, 'false', '是否开启小地图标记', True, cid=651)
def enableBfDotaMapMark():
    pass


@config(Bool, 'false', '是否开启新成就系统', True, cid=652)
def enableNewAchievement():
    pass


@config(Bool, 'false', '是否开启大宝图限时回馈活动', True, cid=653)
def enableItemUseFeedback():
    pass


@config(Bool, 'false', '是否开启好友IM优化', True, cid=654)
def enableIMOptimize():
    pass


@config(Int, str(50), '邀请者等级', True, cid=655)
def inviterLevel():
    pass


@config(Bool, 'false', '是否开启首席门派大弟子雕像实时刷新功能', True, cid=656)
def enableRefreshShoolTopOneNpcModel():
    pass


@config(Bool, 'false', '是否开启新手累计签到奖励', True, cid=657)
def enableNoviceCheckInReward():
    pass


@config(Bool, 'false', '是否开启公会传承', True, cid=658)
def enableGuildInherit():
    pass


@config(Bool, 'true', '是否开启公会拍卖行', True, cid=659)
def enableGuildConsign():
    pass


@config(Bool, 'true', '是否开启世界拍卖行', True, cid=672)
def enableWorldConsign():
    pass


@config(Bool, 'true', '是否公会和世界拍卖行预检查')
def enableWorldConsignPreOrder():
    pass


@config(Bool, 'false', '是否开启新职业', True, cid=660)
def enableNewSchoolSummon():
    pass


@config(Bool, 'false', '是否开启王者对决英雄展示', True, cid=661)
def enableBfDotaHeros():
    pass


@config(Bool, 'false', '是否开启特效键盘', True, cid=662)
def enableKeyboardEffect():
    pass


@config(Bool, 'false', '是否启用系统计算开启时间', True, cid=663)
def enableArenaPlayoffsTimeCalc():
    pass


@config(Bool, 'true', '是否放宽对副本单Avatar的buff个数限制', True, cid=664)
def enableHighStateLimitInFuben():
    pass


@config(Bool, 'false', '是否开启七日登录奖励', True, cid=665)
def enableNoviceCheckInRewardOld():
    pass


@config(Bool, 'true', '是否进行婚礼', True, cid=666)
def enableMarriage():
    pass


@config(Bool, 'true', '是否开启浮动商店', True, cid=667)
def enableDynamicShop():
    pass


@config(Bool, 'true', '是否开启周活跃度特权购买', True, cid=668)
def enableWeekPrivilegeBuy():
    pass


@config(Bool, 'true', '是否开启天币直接购买云垂积分', True, cid=669)
def enableBuyYunChuiCreditThroughCoin():
    pass


@config(Bool, 'false', '是否开启CEF超时报警', True, cid=670)
def enableCEFOverTimeWarning():
    pass


@config(Bool, 'true', '是否允许上传自定义图片', True, cid=671)
def enableNOSCustom():
    pass


@config(Bool, 'false', '是否预开启CEF', True, cid=673)
def enablePreOpenCEF():
    pass


@config(Bool, 'false', '魂界战场AoI无限大', True, cid=674)
def bfDotaAoIInfinity():
    pass


@config(Bool, 'false', '是否开启百凤宴公会排名', True, cid=675)
def enableGuildChickenMeal():
    pass


@config(Bool, 'true', '是否开启钓鱼大赛公会排名', True, cid=676)
def enableGuildFishActivity():
    pass


@config(Bool, 'true', '是否开启四方之乱公会排名', True, cid=677)
def enableGuildMonsterClanWar():
    pass


@config(Bool, 'true', '是否开启使用复活玩家技能也算参与领地战', True, cid=678)
def enableRelivePlayerIsAttendCw():
    pass


@config(Bool, 'false', '是否启用个人宝箱伪随机投放', True, cid=679)
def enableBoxProbabilityAdjustment():
    pass


@config(Bool, 'true', '是否队伍广播获取珍贵物品', True, cid=680)
def enableGetItemTeamBroadcast():
    pass


@config(Bool, 'false', '开启as抛错上传', True, cid=681)
def enableReportASError():
    pass


@config(Bool, 'false', '开启回流组功能', True, cid=682)
def enableFlowbackGroup():
    pass


@config(Bool, 'true', '是否开启特惠活动-宝箱展示及购买', True, cid=683)
def enablePreferentialActivity():
    pass


@config(Bool, 'true', '开启公会签到', True, cid=684)
def enableGuildSignIn():
    pass


@config(Bool, 'true', '开启公会红包', True, cid=685)
def enableGuildRedPacket():
    pass


@config(Bool, 'true', '是否开启王者之路精品活动', True, cid=686)
def enableOperationActivity():
    pass


@config(Bool, 'true', '是否开启任务临时buffID检查', True, cid=687)
def enableQuestTempStateId():
    pass


@config(Bool, 'false', '开启公会聊天职位显示', True, cid=688)
def enableShowGuildPrivilegesInChat():
    pass


@config(Bool, 'false', '是否开启随身商店天币计费日志')
def enablePrivateShopMallBuyLog():
    pass


@config(Bool, 'true', '是否开启订婚', True, cid=689)
def enableEngage():
    pass


@config(Bool, 'false', '是否开启工会频道优化')
def enableGuildChatOpt():
    pass


@config(Bool, 'true', '是否开启每日福利超值礼包活动', True, cid=690)
def enableDailyWelfareActivity():
    pass


@config(Bool, 'true', '商城是否支持只扣非绑天币', cid=691)
def enableBuyMallItemOnlyUnbindCoin():
    pass


@config(Bool, 'true', '是否压缩家园roomData')
def enableZipRoomData():
    pass


@config(Bool, 'true', '是否开启可交互物件使用状态检查')
def enableUseInteractiveObjectStateCheck():
    pass


@config(Bool, 'true', '是否开启公会烤火', True, cid=692)
def enableGuildBonfire():
    pass


@config(Bool, 'false', '是否开启天谕2推送', True, cid=693)
def enablePushMessageV2():
    pass


@config(Bool, 'false', '是否开启战场今日活动', True, cid=694)
def enableBfTodayActivity():
    pass


@config(Bool, 'true', '是否开启公会玉木峰排行榜', True, cid=696)
def enableGuildYMF():
    pass


@config(Bool, 'true', '是否开启本服公会联赛观战和鼓舞机制', True, cid=697)
def enableGuildTournamentLiveAndInspire():
    pass


@config(Bool, 'true', '是否开启结婚预约系统', True, cid=698)
def enableMarriageSubscribe():
    pass


@config(Bool, 'true', '是否开启公会随身商店', True, cid=699)
def enableGuildCompositeShop():
    pass


@config(Bool, 'false', '是否开启翼世界', True, cid=700)
def enableWingWorld():
    pass


@config(Bool, 'false', '是否准备开启从国战过度到翼世界')
def enableWorldWarToWingWorld():
    pass


@config(Bool, 'false', '是否开启技能修炼剥离', True, cid=701)
def enableRemoveSkillEnhance():
    pass


@config(Bool, 'true', '是否开启公会碎星屿排行榜、公会排行榜奖励', True, cid=702)
def enableGuildSXY():
    pass


@config(Bool, 'true', '是否开启公会威望排行榜', True, cid=703)
def enableGuildPrestigeTopRank():
    pass


@config(Bool, 'true', '是否开启领地战产出到公会拍卖', True, cid=704)
def enableClanWarOutputToGuildConsign():
    pass


@config(Bool, 'true', '是否开启随身复合商店公会全局限量', True, cid=705)
def enablePrivateShopGuildLimit():
    pass


@config(Bool, 'false', '是否开启翼世界开门', True, cid=706)
def enableWingWorldOpenDoor():
    pass


@config(Bool, 'false', '是否开启英灵屏蔽功能', True, cid=707)
def enableSummonedWarSpriteDisabledFun():
    pass


@config(Bool, 'false', '是否开启众里寻他优化', True, cid=708)
def enableGuildMatchOptimize():
    pass


@config(Bool, 'false', '禁止C_ui字体的使用', True, cid=709)
def disableCUIFont():
    pass


@config(Bool, 'false', '是否开启战灵的战斗统计', True, cid=710)
def enableSpriteCombatStats():
    pass


@config(Bool, 'true', '是否开启玩家周活跃度达成加公会威望', True, cid=711)
def enableAddPrestigeByWeekActivation():
    pass


@config(Int, str(0), '战灵模型最大数', True, cid=712)
def maxSpriteModelCnt():
    pass


@config(Bool, 'false', '是否开启公会宝贝', True, cid=713)
def enableGuildLady():
    pass


@config(Bool, 'false', '是否开启王者对决单Cell限制', False)
def enableSingleCellMobaDotaSpace():
    pass


@config(Bool, 'false', '是否开启深度学习数据应用', True, cid=715)
def enableDeepLearningDataApply():
    pass


@config(Bool, 'true', '是否开启本服公会联赛第二轮周排名奖励发放公会拍卖', False)
def enableGtRoundTowRewardOnGconsignSale():
    pass


@config(Bool, 'true', '开启公会联赛观战传送检测', False)
def enableGtLiveTeleportCheck():
    pass


@config(Bool, 'false', '开启进副本扣道具先判断服务器事件', False, 716)
def enableFbRequireItemByMileStoneId():
    pass


@config(Bool, 'true', '检查是否关闭gmFollow', True, cid=717)
def enableCheckGmFollow():
    pass


@config(Bool, 'false', '是否开启魂界Avatar可见性检测', True, cid=718)
def enableDotaAvatarVisibleCheck():
    pass


@config(Bool, 'false', '是否开启竞技场新匹配规则', False, cid=720)
def enableArenaNewMatchRules():
    pass


@config(Bool, 'false', '是否开启天羽演武', True, cid=721)
def enableSkyWingChallenge():
    pass


@config(Bool, 'false', '是否开启多语言聊天', True, cid=722)
def enableChatMultiLanguage():
    pass


@config(Bool, 'false', '开启奖励找回', True, cid=723)
def enableRewardRecovery():
    pass


@config(Bool, 'false', '是否开启奖励找回单服或全服开启时间开关', True, cid=724)
def enableRewardRecoveryForServerOpTime():
    pass


@config(Bool, 'false', '是否开启门派委托优化功能', True, cid=725)
def enableSchoolEntrustOptimize():
    pass


@config(Bool, 'false', '开启客户端奖励找回入口', True, cid=726)
def enableRewardRecoveryClient():
    pass


@config(Bool, 'true', '开启公会随身商店自动刷新', True, cid=727)
def enableGuildPrivateShopAutoRefresh():
    pass


@config(Bool, 'false', '开启公会天币捐献', True, cid=728)
def enableGuildDonateWithCoin():
    pass


@config(Bool, 'false', '是否开启公会联赛练兵之战', True, cid=729)
def enableGuildTournamentTraining():
    pass


@config(Bool, 'false', '是否开放英灵材料包', True, cid=730)
def enableSpriteMaterialBag():
    pass


@config(Bool, 'false', '是否开放公会NPC传功', True, cid=731)
def enableGuildInheritByNpc():
    pass


@config(Bool, 'false', '是否开启充值循环奖励', True, cid=732)
def enableChargeRewardLoop():
    pass


@config(Bool, 'false', '是否开启周随机活动奖励', True, cid=733)
def activitiesWeeklyReward():
    pass


@config(Bool, 'true', '是否开放卡牌系统', True, cid=734)
def enableCardSys():
    pass


@config(Bool, 'false', '是否开启修正王者对决模型可见性', True, cid=735)
def enableFixDotaModelVisible():
    pass


@config(Int, '0', '服务器最近一次合服的时间', True, cid=736)
def serverLatestMergeTime():
    pass


@config(Bool, 'true', '是否开启神兽活动', True, cid=737)
def enableExchangeMysteryAnimal():
    pass


@config(Bool, 'false', '是否启用新Esc面板', True, cid=738)
def enableSystemSettingV2():
    pass


@config(Bool, 'false', '是否开启任务定时器检测', True, cid=739)
def enableQuestTimerCheck():
    pass


@config(Bool, 'false', '是否开启新服争霸活动', True, cid=740)
def enableNewServerTopRankAct():
    pass


@config(Str, '', '奖励找回黑名单,根据奖励类型过滤,用英文逗号隔开', True, cid=741)
def rewardRecoveryBlackList():
    pass


@config(Bool, 'false', '是否打开扩展聊天窗', True, cid=742)
def enableExtendChatBox():
    pass


@config(Bool, 'false', '是否开启公会合并', True, cid=743)
def enableGuildMerger():
    pass


@config(Bool, 'false', '是否开启英灵亲密度转移', True, cid=744)
def enableSummonedWarSpriteFamiliar():
    pass


@config(Bool, 'false', '是否开启彩票兑换', True, cid=745)
def enableLotteryExchange():
    pass


@config(Bool, 'false', '是否开启凝聚宝盒', True, cid=746)
def enableExchangeMysteryBox():
    pass


@config(Bool, 'false', '是否开启录像')
def enableAnnalRecord():
    pass


@config(Bool, 'false', '是否开启录像回放')
def enableAnnalReplay():
    pass


@config(Int, '10', '录像快照间隔')
def annalSnapshotInterval():
    pass


@config(Bool, 'false', '是否开启新服争争霸十大公会活动)', True, cid=750)
def enableNewServerGuildPrestige():
    pass


@config(Bool, 'false', '是否开启击杀惩戒使', True, cid=751)
def enableKillFallenRedGuard():
    pass


@config(Bool, 'true', '是否开启击杀惩戒使强制PK')
def enableKillFallenRedGuardPK():
    pass


@config(Bool, 'false', '开启好友召回活动', True, cid=752)
def enableFriendRecall():
    pass


@config(Float, '0.3', '优化瞬移后接位移技能，位置计算不对的问题', True, cid=753)
def teleportMoveDelayTime():
    pass


@config(Bool, 'false', '是否开启生命链接', True, cid=754)
def enableLifeLink():
    pass


@config(Bool, 'false', '开启预购团购系统', True, cid=755)
def enableGroupPurchase():
    pass


@config(Bool, 'false', '是否开启翼世界军队', True, cid=756)
def enableWingWorldArmy():
    pass


@config(Bool, 'false', '开启魂界模型预加载', True, cid=757)
def enableDotaZaijuPreLoad():
    pass


@config(Bool, 'false', '是否开启英灵闲聊', True, cid=758)
def enableSummonedWarSpriteChat():
    pass


@config(Bool, 'false', '开启奖励找回新规则功能', True, cid=759)
def enableRewardRecoveryNew():
    pass


@config(Bool, 'false', '开启结婚技能', True, cid=760)
def enableMarriageSkill():
    pass


@config(Bool, 'false', '是否开启公会威望旗帜功能（苏澜主城）', cid=761)
def enablePrestigeFlag():
    pass


@config(Bool, 'false', '开启不计算5分钟战场', False)
def enableIgnoreBFDotaCalc():
    pass


@config(Float, '3.2', '魂界观战修复距离', cid=762)
def enableDotaFollowFix():
    pass


@config(Bool, 'false', '是否开启副本队伍搭配二次确认', cid=763)
def enableFbTeamSchoolDoubleCheck():
    pass


@config(Bool, 'false', '是否开启好友回归V2', True, cid=764)
def enableSummonFriendV2():
    pass


@config(Bool, 'true', '是否开启远古号角', True, cid=765)
def enableYuanguLaba():
    pass


@config(Bool, 'true', '是否开启杀星本怪物提前入战报警', cid=766)
def enableShaXingEnterCombatEarlyReport():
    pass


@config(Bool, 'true', '是否开启自选奖池抽奖功能', cid=767)
def enableActivitySaleLottery():
    pass


@config(Bool, 'false', '是否启用F11隐藏功能', True, cid=769)
def enableF11Hide():
    pass


@config(Bool, 'true', '是否启用角色创建对更名表检查')
def enableCreateCharacterIsInRenameList():
    pass


@config(Int, '0', '输出指定id实体的技能debug信息到info日志')
def debugSkillCalcEntId():
    pass


@config(Bool, 'false', '战场补位职业平衡')
def enableBFJumpQueueRebalance():
    pass


@config(Bool, 'false', '翼世界脚本动画推送开关', True, cid=770)
def enableWingWorldAnimPush():
    pass


@config(Bool, 'false', '开启奖池抽奖活动', True, cid=771)
def enableRandomLottery():
    pass


@config(Bool, 'false', '查看人物英灵开关', True, cid=772)
def enableSummonedSpriteOther():
    pass


@config(Bool, 'true', '是否打开技能宏入口', True, cid=773)
def enableOpenSkillMacroEntry():
    pass


@config(Bool, 'false', '是否开启翼世界心魔', True, cid=774)
def enableWingWorldXinMo():
    pass


@config(Str, '2,200', '设置天羽演武开本窗口')
def skyWingFbWindowsArgs():
    pass


@config(Bool, 'false', '是否开启妖精奇谭多倍抵扣', True, cid=775)
def enableYaojingqitanCustomCost():
    pass


@config(Int, '3000', '设置天羽演武副本同时存在数量限制')
def skyWingFbExistLimit():
    pass


@config(Bool, 'false', '开启奖池抽奖活动-优化逻辑开关', True, cid=777)
def enableRandomLotteryOptimize():
    pass


@config(Bool, 'false', '盛世婚礼开关', True, cid=778)
def enableMarriageGreat():
    pass


@config(Bool, 'false', '允许结婚扩展宾客', True, cid=779)
def enableMarriageGuestExtend():
    pass


@config(Str, '1,10', '设置天羽演武副本销毁窗口')
def skyWingFbDestoryArgs():
    pass


@config(Bool, 'false', '是否开启英灵探险', True, cid=781)
def enableExploreSprite():
    pass


@config(Bool, 'true', '开启宝箱奖励图标显示', True, cid=782)
def enableItemBoxRewardShow():
    pass


@config(Bool, 'true', '是否开启在本服globalMailBox消息直达')
def enableGlobalMailBoxMsgOptimize():
    pass


@config(Bool, 'false', '是否开启云垂百晓试（百万冲顶）', True, cid=783)
def enableQuizzes():
    pass


@config(Bool, 'true', '翼世界城市状态检查报警开关(外网开，内网测试服关)', True, cid=784)
def enableWingWorldCheckCityWarning():
    pass


@config(Bool, 'false', '是否开启技能宏奖励', True, cid=785)
def enableSkillMacroTopReward():
    pass


@config(Bool, 'false', '自动录像功能', True, cid=786)
def enableAutoTakeVideo():
    pass


@config(Bool, 'false', '普通婚礼客户端开关', True, cid=787)
def enableNormalMarriage():
    pass


@config(Bool, 'false', '是否开启NpcV2', True, cid=788)
def enableNpcV2():
    pass


@config(Bool, 'false', '运营顶栏直播武道会跨服联赛入口显示', True, cid=789)
def enableLiveStreamingIcon():
    pass


@config(Int, '500', '翼世界城战地图进入人数限制', True, cid=790)
def wingWorldWarCityMaxCount():
    pass


@config(Bool, 'false', '开启节日免做功能', True, cid=791)
def enableAvoidDoingActivity():
    pass


@config(Bool, 'false', '翼世界押镖', True, cid=792)
def enableWingWorldYabiao():
    pass


@config(Bool, 'false', '是否开启英灵驯养', True, cid=793)
def enableTrainingSprite():
    pass


@config(Bool, 'false', '考拉虚拟道具线上售卖')
def enableKoalaOrder():
    pass


@config(Int, '5', '考拉订单请求间隔')
def koalaOrderQueryInterval():
    pass


@config(Int, '50', '考拉订单一次请求的最大数目')
def koalaOrderQueryLimit():
    pass


@config(Bool, 'false', '开启称号迭代功能', True, cid=794)
def enablePropTitle():
    pass


@config(Bool, 'false', '是否开启英灵技能转移', True, cid=795)
def enableSpriteSkillTransfer():
    pass


@config(Bool, 'false', '是否开启超稀有英灵转移', True, cid=796)
def enableSpriteRareTransfer():
    pass


@config(Bool, 'false', '是否开启蛋蛋英灵进阶', True, cid=797)
def enableSpriteUpgrade():
    pass


@config(Bool, 'false', '开启装备觉醒的serverConfig', True, cid=798)
def enableEquipJuexingServerConfig():
    pass


@config(Bool, 'false', '开启通用版本海盗排行榜', True, cid=799)
def enableNewWmdRankListConfig():
    pass


@config(Bool, 'true', '是否开启翼世界万灵之主', True, cid=800)
def enableWingWorldSoulBoss():
    pass


@config(Bool, 'false', '是否开启翼世界公会职位迭代', True, cid=801)
def enableWingWorldGuildRoleOptimization():
    pass


@config(Bool, 'true', '是否开启异常结算报警')
def enableErrorCombatCalcValueAlert():
    pass


@config(Bool, 'false', '是否开启英灵修炼', True, cid=802)
def enableSpriteGrowth():
    pass


@config(Bool, 'false', '是否开启翼世界英灵资源采集')
def enableWingWorldSpriteResCollect():
    pass


@config(Bool, 'false', '是否开启统计英灵轮回出现组合天赋的次数')
def enableRecordBonusOccurrences():
    pass


@config(Bool, 'false', '是否开启英灵祈福轮回', True, cid=804)
def enableSpritePrayLunhui():
    pass


@config(Bool, 'false', '时代1的城战开关', True, cid=805)
def enableWingWarGroup1():
    pass


@config(Bool, 'false', '时代2的城战开关', True, cid=806)
def enableWingWarGroup2():
    pass


@config(Bool, 'false', '时代3的城战开关', True, cid=807)
def enableWingWarGroup3():
    pass


@config(Bool, 'false', '是否开启魂界战场创生服务端结算', True, cid=808)
def enableBFDotaCreationServerCalc():
    pass


@config(Bool, 'false', '是否开启翼世界专用技能方案', True, cid=809)
def enableWingWorldSkillScheme():
    pass


@config(Int, '0', '(已废弃，使用新开关enableWingCityDeclareList1)翼世界开放城池限制,禁止宣战的城市Id起始', True, cid=810)
def wingWorldCityDisableDeclareStart():
    pass


@config(Int, '0', '(已废弃，使用新开关enableWingCityDeclareList1)翼世界开放城池限制,禁止宣战的城市Id结束', True, cid=811)
def wingWorldCityDisableDeclareEnd():
    pass


@config(Bool, 'false', '是否开启英灵自动出战', True, cid=812)
def enableSpriteAutoCallOut():
    pass


@config(Bool, 'false', '是否开启职业专精修炼次数上限', True, cid=813)
def enablePvpEnhanceMaxCostNum():
    pass


@config(Bool, 'false', '是否开启英灵技能镶嵌', True, cid=814)
def enableSpriteSkillBeset():
    pass


@config(Bool, 'false', '是否支持跨服公会拍卖推送', True, cid=815)
def enableGuildAuctionCrossPush():
    pass


@config(Bool, 'false', '是否开启传送聊天框置顶', True, cid=816)
def enableChatTopWhenLoading():
    pass


@config(Bool, 'false', '允许轻功回复速度共享', True, cid=817)
def enableRideWingShareEpRegen():
    pass


@config(Bool, 'false', '是否开启条件属性')
def enableConditionalProp():
    pass


@config(Bool, 'false', '是否开启新版活动签到功能', True, cid=818)
def enableNewActivitySignin():
    pass


@config(Bool, 'false', '是否开启统计每日签到累计次数')
def enableRecordDailySignIn():
    pass


@config(Bool, 'false', '是否准备开启开启翼世界', True, cid=819)
def enableWingWorldReady():
    pass


@config(Bool, 'false', '是否禁止欧洲IP登录')
def enableForbidIpOfEurope():
    pass


@config(Bool, 'true', '是否开启cc语音', True, cid=820)
def enableCCSpeak():
    pass


@config(Bool, 'false', '是否使用新的英灵洗练规则表')
def enableNewSpriteRerandRuleData():
    pass


@config(Bool, 'false', '是否暂停公会合并报名')
def enablePauseApplyGuildMerger():
    pass


@config(Bool, 'false', '是否使用新增道行增长类型')
def enableNewAddDaoHengType():
    pass


@config(Bool, 'false', '是否禁止普通用户登陆翼世界')
def enableWingWorldForbidLogin():
    pass


@config(Bool, 'false', '是否开启竞拍模式物品白名单功能', True, cid=821)
def enableAuctionItemWhiteList():
    pass


@config(Bool, 'false', '是否开启妙音这个新职业，允许创建妙音号', True, cid=822)
def enableNewSchoolMiaoyin():
    pass


@config(Bool, 'false', '是否开启王者对决举报功能', True, cid=823)
def enableDotaBFVote():
    pass


@config(Bool, 'false', '是否显示玩家血条数字', True, cid=824)
def enablePlayerHpTxtVisible():
    pass


@config(Bool, 'true', '是否开启众里寻他第二次优化', True, cid=825)
def enableGuildMatchOptimizeSecond():
    pass


@config(Bool, 'true', '是否开启翼世界熔炉', True, cid=826)
def enableWingWorldForge():
    pass


@config(Bool, 'true', '是否开启翼世界城战载具建造', True, cid=827)
def enableWingWorldCarrierBuild():
    pass


@config(Bool, 'true', '跨服切换幻匣数据是否允许带回')
def enableCrossSetCardEquipSlot():
    pass


@config(Str, '', '翼世界时代1开启宣战的城池，以逗号做风格，比如1,2,3', True, cid=829)
def enableWingCityDeclareList1():
    pass


@config(Str, '', '翼世界时代2开启宣战的城池，以逗号做风格，比如1,2,3', True, cid=830)
def enableWingCityDeclareList2():
    pass


@config(Str, '', '翼世界时代3开启宣战的城池，以逗号做风格，比如1,2,3', True, cid=831)
def enableWingCityDeclareList3():
    pass


@config(Bool, 'true', '是否允许幻鉴同时装备在多个幻匣', True, cid=832)
def enableCardEquipInMutiSlots():
    pass


@config(Bool, 'false', '是否开启新夺旗战场（红石堡争夺战）', True, cid=833)
def enableNewFlagBF():
    pass


@config(Bool, 'false', '是否开启新夺旗战场跨服匹配', True, cid=1031)
def enableNewFlagBFCrossMatch():
    pass


@config(Bool, 'false', '是否开启王者对决禁止相同设备进入')
def enableDotaCheckMac():
    pass


@config(Bool, 'false', '内服藏宝阁角色交易跳过网站请求')
def cbgRolePassHttpReq():
    pass


@config(Bool, 'false', '内服藏宝阁角色交易跳过条件检查', True, cid=899)
def cbgRolePassConditions():
    pass


@config(Bool, 'false', '藏宝阁角色交易通知和反馈信息开关')
def enableCBGRoleMsg():
    pass


@config(Bool, 'false', '开启玩家模板')
def enableCharTemp():
    pass


@config(Bool, 'false', '是否开启比武招亲', True, cid=834)
def enableFightForLove():
    pass


@config(Bool, 'true', '是否开启平衡竞技场', True, cid=835)
def enableBalanceArena():
    pass


@config(Int, '60', '王者对决举报时间间隔')
def dotaBattleFieldReportInterval():
    pass


@config(Bool, 'true', '是否允许修改模板', True, cid=836)
def enableChangeCharTemp():
    pass


@config(Bool, 'true', '模板是否定时加假数据')
def enabelFakeCharTempData():
    pass


@config(Bool, 'false', ' 是否开启定时玩家数值日志监控')
def enableMonitorRoleValLog():
    pass


@config(Bool, 'false', '开启翻牌活动', True, cid=900)
def enableRandomTurnOverCard():
    pass


@config(Bool, 'false', '是否只允许白名单玩家使用角色交易', True, cid=837)
def enableCBGRoleWhiteList():
    pass


@config(Bool, 'false', '是否默认必须指定好友才能上架角色', True, cid=901)
def enableCBGRoleDefaultFriendTarget():
    pass


@config(Bool, 'false', '是否必须不指定好友才能上架角色', True, cid=902)
def enableCBGRoleNotFriendTarget():
    pass


@config(Bool, 'false', '是否开启网易游戏会员权益', True, cid=838)
def enableNeteaseGameMembershipRights():
    pass


@config(Bool, 'true', '是否开启平衡竞技场段位奖励领取', True, cid=839)
def enableDuanWeiAwardBalance():
    pass


@config(Bool, 'false', '是否可以领取竞技场周奖励', True, cid=840)
def enableArenaWeeklyAward():
    pass


@config(Bool, 'false', '是否可以领取平衡竞技场周奖励', True, cid=841)
def enableArenaWeeklyAwardBalance():
    pass


@config(Bool, 'true', '是否可以提交模板', True, cid=842)
def enableCommitCharTemp():
    pass


@config(Bool, 'false', '是否开启藏宝阁角色交易运营奖励')
def enableCBGRoleAward():
    pass


@config(Bool, 'false', '是否开启门派首席玩法', True, cid=843)
def enableSchoolTopMatch():
    pass


@config(Str, '2,50', '设置红石堡战场开本窗口')
def newFlagBFWindowsArgs():
    pass


@config(Bool, 'false', '是否开启云币售卖机器人')
def enableBuyCoinRobot():
    pass


@config(Bool, 'false', '是否开启一键配装', True, cid=844)
def enableOneKeyConfig():
    pass


@config(Bool, 'false', '是否开启全屏烟花', True, cid=846)
def enableFullScreenFireworks():
    pass


@config(Bool, 'false', '是否允许在竞技场准备地宫(701)跨服组队', cid=845)
def enableGroupOnBalanceReadyRoom():
    pass


@config(Bool, 'false', '幻匣切换功能', True, cid=847)
def enableChangeCardSuit():
    pass


@config(Bool, 'false', '是否开启英灵槽位扩展', True, cid=848)
def enableExpandSpriteSlot():
    pass


@config(Bool, 'false', '是否往合作服同步所有模板数据(非当前模板)', True, cid=849)
def syncAllCharTempInfoToHezuofu():
    pass


@config(Bool, 'false', '是否披风时装槽位', True, cid=850)
def enableFashionCapeSlot():
    pass


@config(Bool, 'true', '是否允许玩家保存，使用模板方案', True, cid=851)
def enableCharTempScheme():
    pass


@config(Bool, 'false', '是否开启使用指定道具进行精炼觉醒', True, cid=852)
def enableReforgeEquipJuexingWithItem():
    pass


@config(Bool, 'false', '是否开启双人竞技场', True, cid=853)
def enableDoubleArena():
    pass


@config(Bool, 'false', '是否跳过双人竞技场成立战队职业检查')
def enableDoubleArenaSchoolCheck():
    pass


@config(Bool, 'false', '是否开启英灵修炼回退', True, cid=854)
def enableRecoverSpriteGrowth():
    pass


@config(Bool, 'true', '是否开启历史消费返还活动', True, cid=855)
def enableHistoryConsumed():
    pass


@config(Bool, 'false', '是否开启技能外观', True, cid=912)
def enableSkillAppearance():
    pass


@config(Bool, 'false', '是否开启庆典期活动玩法', True, cid=913)
def enableWingCelebrationActivity():
    pass


@config(Str, '', '是否开启新服活动（0寻灵经验 1新服福利 2月光珍匣 3十大公会 4战力达人 5等级达人 6谕世巅峰 7副本竞速 8副本首杀 9秘市商人 10鸿运当头 11最终修行），比如1,2,3', True, cid=914)
def enableNewServerActivity():
    pass


@config(Bool, 'false', '是否开启帝翼神王传', True, cid=915)
def enableWingWorldHistoryBook():
    pass


@config(Bool, 'false', '是否修复被移除服务器列表角色数目显示移除', True, cid=916)
def enableFixOldRoleNumError():
    pass


@config(Bool, 'false', '是否开启藏宝阁二期数据')
def enableSecondStageDataCBG():
    pass


@config(Bool, 'false', '是否开启幻鉴指定洗炼', True, cid=917)
def enableCardSpecialChange():
    pass


@config(Bool, 'false', '是否开启竞技场积分赛', True, cid=918)
def enableArenaScore():
    pass


@config(Bool, 'false', '是否开启新服宝箱额外奖励组', True, cid=919)
def enableTreasureBoxExtraBonus():
    pass


@config(Bool, 'false', '是否开启竞技场临时被动技能调整', True, cid=920)
def enableArenaTempPskills():
    pass


@config(Bool, 'false', '是否开启查看详细斗魂按钮', True, cid=921)
def enableSummonedWarSpriteEffect():
    pass


@config(Bool, 'false', '是否开启新平衡竞技场结算界面', True, cid=922)
def enableBalanceArenaFinalResult():
    pass


@config(Bool, 'false', '是否启用新camera', True, cid=923)
def enableNewCamera():
    pass


@config(Bool, 'false', '是否开启客户端log打印局部变量', True, cid=924)
def enableClientLogPrintLoacalVars():
    pass


@config(Bool, 'true', '破鉴是否返还映鉴之心', True, cid=925)
def enableCardReturnBossItem():
    pass


@config(Bool, 'false', '是否开启翼世界扩展小地图', True, cid=926)
def enableWingWorldMap():
    pass


@config(Bool, 'false', '是否开启把CronStr转成list格式', True, cid=927)
def enableParseCronStr2List():
    pass


@config(Bool, 'false', '是否开启蕴灵功能最后一页', True, cid=928)
def enableEquipSoulNewest():
    pass


@config(Bool, 'false', '是否开启精炼觉醒强化功能', True, cid=929)
def enableEquipChangeJuexingStrength():
    pass


@config(Bool, 'false', '是否开启门派首席测试入口', True, cid=930)
def enableSchoolTopTestFuben():
    pass


@config(Bool, 'false', '是否允许跨战区申请战场', True, cid=931)
def enableUpBFRegion():
    pass


@config(Bool, 'false', '是否开启跨服领地战', True, cid=932)
def enableCrossClanWar():
    pass


@config(Bool, 'true', '积分赛申请时是否帮玩家自动组队', True, cid=933)
def enableAutoBuildArenaScoreTeam():
    pass


@config(Bool, 'true', '是否使用公式配置计算竞技场积分', True, cid=934)
def enableFormulaValue():
    pass


@config(Bool, 'false', '客户端双人竞技场是否开启战报', True, cid=935)
def enableDoubleArenaZhanBao():
    pass


@config(Bool, 'false', '是否开启伏羲通宝功能', True, cid=936)
def enableFTB():
    pass


@config(Bool, 'true', '客户端双人竞技场16强是否开启战报', True, cid=937)
def enableDoubleArena16QiangZhanBao():
    pass


@config(Bool, 'false', '客户端是否隐藏竞技场tab页', True, cid=938)
def hidePvpArenaPanel():
    pass


@config(Bool, 'false', '是否开启双人竞技场观战功能', True, cid=939)
def enableDoubleArenaAnnal():
    pass


@config(Bool, 'false', '是否开启平衡竞技场断线重登功能', True, cid=940)
def enableBalanceReLogon():
    pass


@config(Bool, 'true', 'npc3d头像优化', True, cid=941)
def enableLargePhotoSize():
    pass


@config(Bool, 'true', '是否开启平衡竞技场禁止相同设备进入')
def enableBalanceArenaCheckMac():
    pass


@config(Str, '5,1,100000,100000', '城战数据统计同步参数(1.同步间隔2.同步击杀阈值3.同步伤害阈值4.同步治疗阈值)')
def syncClanWarStatsParams():
    pass


@config(Bool, 'false', '是否开启斩魔极副本', True, cid=942)
def enableZMJFuben():
    pass


@config(Bool, 'true', '是否开断线后禁止重进平衡武道会', True, cid=943)
def enableNoRenterPlayoffs():
    pass


@config(Bool, 'false', '是否开启模型、特效和地图材质的加载统计', True, cid=944)
def enableMaterialLoadStatistics():
    pass


@config(Bool, 'false', '是否开通用推送', True, cid=945)
def enableGeneralPush():
    pass


@config(Bool, 'false', '是否开启全服彩票活动', True, cid=946)
def enableGlobalLottery():
    pass


@config(Bool, 'false', '是否开启新版重复道具报警')
def enableDuplicateItemReportV2():
    pass


@config(Bool, 'false', '是否开启挑战通行证', True, cid=947)
def enableChallengePassport():
    pass


@config(Bool, 'false', '是否显示技能外观屏蔽功能', True, cid=948)
def enableSkillAppearanceBlock():
    pass


@config(Bool, 'false', '是否开启延迟属性计算功能（将同步操作中的属性计算降到一次）')
def enableDeferredPropCalc():
    pass


@config(Bool, 'true', '开启陷入地下的检测', True, cid=949)
def enableCheckBelowTerrain():
    pass


@config(Bool, 'false', '是否开启Avatar spaceType,fbNo,fbType缓存')
def enableCacheSpaceType():
    pass


@config(Bool, 'false', '是否开启全服寻灵杀怪双倍经验', True, cid=950)
def enableGlobalExpBonus():
    pass


@config(Bool, 'true', '是否开启特效LRU缓存', True, cid=951)
def enableLRUCache():
    pass


@config(Bool, 'false', '是否开启远征号角', True, cid=952)
def enableCrossClanWarLaba():
    pass


@config(Bool, 'false', '是否开启跨服领地战关系判断', True, cid=953)
def enableCrossClanWarRelation():
    pass


@config(Bool, 'false', '是否开启公会副本', True, cid=954)
def enableGuildFuben():
    pass


@config(Bool, 'false', '是否开启衣柜系统(新时装外观)', True, cid=955)
def enableWardrobe():
    pass


@config(Bool, 'false', '是否开启5v5武道会', True, cid=957)
def enablePlayoffs5V5():
    pass


@config(Bool, 'false', '是否开启新版表情面板', True, cid=958)
def enableNewEmotionPanel():
    pass


@config(Bool, 'false', '是否开启领地战精英挑战', True, cid=959)
def enableClanWarChallenge():
    pass


@config(Bool, 'false', '是否开启衣柜系统，时装柜套装选项（注意不是衣柜搭配开关）', True, cid=960)
def enableWardrobeSuitShow():
    pass


@config(Bool, 'false', '是否开启武道会竞选福袋', True, cid=961)
def enablePlayoffsVoteLuckyBag():
    pass


@config(Bool, 'false', '是否开启飞升', True, cid=962)
def enableFlyUp():
    pass


@config(Bool, 'false', '是否开启衣柜系统多套染色方案功能', True, cid=963)
def enableWardrobeMultiDyeScheme():
    pass


@config(Bool, 'false', '是否使用均匀分布的findRandomNeighbourPoint')
def enableSquareFindRandomNeighbourPoint():
    pass


@config(Bool, 'false', '是否允许领地战、亡命岛区域使用战灵')
def enableSummonedSpriteInCWAndWMD():
    pass


@config(Bool, 'false', '是否启用行为树组件')
def enableBehaviorStub():
    pass


@config(Bool, 'false', '是否开启根据人数自动选择方向AI')
def enableSelectDirectionByEnemyNum():
    pass


@config(Bool, 'false', '是否开启衣柜系统自定义搭配功能', True, cid=964)
def enableWardrobeScheme():
    pass


@config(Bool, 'false', '是否启用PUPPET')
def enablePuppet():
    pass


@config(Int, '500', 'PUPPET同时存在数量限制')
def puppetNumLimit():
    pass


@config(Bool, 'false', '是否限制仅以本服数据创建PUPPET')
def enableOnlyLocalPuppet():
    pass


@config(Str, '', '禁止从这些服务器获得PUPPET原型玩家数据')
def puppetExcludeHosts():
    pass


@config(Bool, 'false', '是否开启新的战场连杀统计')
def enableBattleFieldNewStats():
    pass


@config(Bool, 'false', '是否开启本服、跨服均可打领地战')
def enableClanWarInSelfAndCross():
    pass


@config(Bool, 'false', '开启神格背包', True, cid=965)
def enableHierogramBag():
    pass


@config(Bool, 'false', '开启新神格（2019.3版本)', True, cid=966)
def enableNewHierogram():
    pass


@config(Bool, 'false', '老神格转新神格(2019.03版的新神格)', True, cid=967)
def enableTransToNewHierogram():
    pass


@config(Bool, 'false', '新神格(2019.03版的新神格)转老神格', True, cid=968)
def enableTransBackOldHierogram():
    pass


@config(Bool, 'false', '是否开启领地战全服争霸', True, cid=969)
def enableGlobalClanWar():
    pass


@config(Bool, 'false', '是否开启争霸服接收号角、蛋蛋推送、滚屏公告等', True, cid=970)
def enableReceiveMsgInRegionServer():
    pass


@config(Bool, 'false', '是否开启跨服领地战预热活动', True, cid=971)
def enableCrossClanWarPreActivity():
    pass


@config(Bool, 'false', '转职竞技场积分<=1200限制', True, cid=972)
def enableTransSchoolArenaScoreLimit():
    pass


@config(Bool, 'false', '公会副本私服人数不做判断')
def enableGuildFubenNoCheck():
    pass


@config(Bool, 'false', '是否开启装备改造-神格', True, cid=973)
def enableEquipChangeRune():
    pass


@config(Bool, 'false', '是否开启私服不检测领地战时间')
def enableClanWarNoCheck():
    pass


@config(Bool, 'false', '竞技场组排超时玩家是否和单排玩家匹配')
def enableHybridSoloTeam():
    pass


@config(Bool, 'false', '队员在组队跟随状态自动传送', True, cid=974)
def enableAutoTeleportInFollow():
    pass


@config(Bool, 'false', '团队跟随', True, cid=975)
def enableNewGroupFollow():
    pass


@config(Bool, 'false', '组队跟随召唤队员功能', True, cid=976)
def enableCallTeamMember():
    pass


@config(Bool, 'false', '私服内飞升无视战区检查')
def enableIgnoreFlyUpGroupCheck():
    pass


@config(Bool, 'true', '跨服的时候显示玩家公会图标', True, cid=977)
def enableCrossServerGuildIcon():
    pass


@config(Bool, 'false', '是否3v3竞技场不能出现3灵珑阵营')
def enable3v3SoloLingLongLimit():
    pass


@config(Bool, 'false', '是否开启时装柜退回背包功能', True, cid=978)
def enableWardrobeReturn():
    pass


@config(Bool, 'false', '是否开启新服通行证(区别于正常通行证)', True, cid=979)
def enableNewServerChallengePassport():
    pass


@config(Bool, 'false', '是否开启斩魔极协战功能', True, cid=980)
def enableZMJAssist():
    pass


@config(Bool, 'false', '是否开启时装包放入更多的材料', True, cid=981)
def enablePutMoreItCategoryIntoFashionBag():
    pass


@config(Bool, 'false', '是否开启伏羲通宝拍卖', True, cid=982)
def enableFtbPaimai():
    pass


@config(Bool, 'false', '是否开启旧神格兑换转换道具', True, cid=983)
def enableExchangeHierogram():
    pass


@config(Bool, 'false', '是否开启随机染色', True, cid=984)
def enableRandomDye():
    pass


@config(Bool, 'false', '是否开启装备改造纹印-合成', True, cid=985)
def enableEquipChangeGemLvUp():
    pass


@config(Bool, 'false', '是否开启SQL注入检测')
def enableCheckSqlInjectionCodes():
    pass


@config(Bool, 'false', '是否开启公会精英副本(五灵秘境.挑战)的排名拍卖奖励', True, cid=986)
def enableGuildFubenTopReward():
    pass


@config(Bool, 'false', '是否开启人物修炼评分各卷满级成就添加功能', False, cid=987)
def enableGuildGrowthVolumnMaxAchieveCheck():
    pass


@config(Bool, 'false', '是否开启公会副本观战', True, cid=988)
def enableGuildFubenObserve():
    pass


@config(Bool, 'false', '是否开启公会仙药制作', True, cid=989)
def enableGuildPotionProduct():
    pass


@config(Bool, 'false', '是否开启翼世界之战排队机制', True, cid=990)
def enableWingWorldWarQueue():
    pass


@config(Bool, 'false', '是否开启公会挑战优化')
def enableGuildChallengeEx():
    pass


@config(Int, '-1', '公会副本观战人数')
def guildFubenObserveNum():
    pass


@config(Bool, 'false', '是否开启战场机器人', True, cid=991)
def enableBattleFieldPuppet():
    pass


@config(Bool, 'false', '是否开启公会天空之王排行榜', True, cid=992)
def enableGuildNewFlag():
    pass


@config(Bool, 'false', '是否开启翼世界风物志', True, cid=993)
def enableWingWorldFengWuZhi():
    pass


@config(Bool, 'false', '是否开启传功延迟开放和服务器经验加成限制', True, cid=994)
def enableServerExpAddLimit():
    pass


@config(Bool, 'false', '是否使用伏羲通宝拍卖测试用url', True, cid=995)
def enableFtbAuctionTestUrl():
    pass


@config(Bool, 'false', '是否开启人物修炼评分奖励', True, cid=996)
def enableGuildGrowthScoreReward():
    pass


@config(Bool, 'false', '是否开启使用物品开启公会拍卖')
def enableUseItemStartGuildConsign():
    pass


@config(Bool, 'false', '钓鱼异常是否增加鱼群数量')
def enableAddFishGroupNumWhenFail():
    pass


@config(Bool, 'true', '钓鱼状态多次检查(拉杆, 吃饵)')
def enableFishMultiCheck():
    pass


@config(Bool, 'false', '公会副本自动踢出其它公会玩家', True, cid=997)
def enableGuildFubenKickMember():
    pass


@config(Bool, 'false', '公会副本调度优化，不修改僵尸公会的状态')
def enableScheduleActiveGuildFuben():
    pass


@config(Bool, 'false', '是否开启头像框功能', True, cid=999)
def enablePhotoBorder():
    pass


@config(Bool, 'false', '是否开启朋友圈', True, cid=1000)
def enablePYQ():
    pass


@config(Bool, 'false', '是否开启跨服战场技能页', True, cid=1001)
def enableCrossBFSkillScheme():
    pass


@config(Bool, 'false', '是否开启王者对决匹配约束优化')
def enableDotaBFGenHybirdLimitOpt():
    pass


@config(Bool, 'false', '是否开启领地战优化', True, cid=1002)
def enableClanWarOptimization():
    pass


@config(Bool, 'false', '是否开启副本免死丹', True, cid=1006)
def enableFbAvoidDieItem():
    pass


@config(Bool, 'false', '是否开启传送到gm活动服务器', True, cid=1003)
def enableTransToGmServer():
    pass


@config(Bool, 'false', '是否开启高级神格重铸', True, cid=1004)
def enableRuneSuperExchange():
    pass


@config(Bool, 'false', '是否隐藏商城的网易会员界面', True, cid=1005)
def hideNeteaseGameMembershipMall():
    pass


@config(Bool, 'false', '是否开启战场再平衡（跨服和本服）', True, cid=1007)
def enableCrossBattleFieldRebalance():
    pass


@config(Bool, 'false', '是否开启运营屏蔽词库SDK接入', True, cid=1008)
def enableEnvSDK():
    pass


@config(Bool, 'false', '是否开启服务器等级差经验加成(新模式）', True, cid=1009)
def enableServerExpAddNew():
    pass


@config(Bool, 'false', '是否开启轮回领域副本', True, cid=1010)
def enableTeamEndless():
    pass


@config(Bool, 'false', '是否开启无消耗斗魂回退', True, cid=1011)
def enableFreeRecoverSpriteGrowth():
    pass


@config(Bool, 'false', '是否开启幻鉴槽扩展', True, cid=1012)
def enableCardSlotExtend():
    pass


@config(Bool, 'true', '是否用经验等级判断指导模式', True, cid=1013)
def enableGuideModeWithXiuweiLv():
    pass


@config(Bool, 'true', '是否允许使用经验丹', True, cid=1014)
def enableBuffExp():
    pass


@config(Bool, 'false', '是否加强拉进副本的检查')
def enableEnterTeleportEnhanceCheck():
    pass


@config(Bool, 'false', '是否开启buff监控功能', True, cid=1015)
def enableBuffListener():
    pass


@config(Bool, 'false', '是否开启伏羲钱包', True, cid=1016)
def enableFtbWallet():
    pass


@config(Bool, 'true', '配置掉落的configName[1]', True, cid=1017)
def enableConfigNameOneForBonus():
    pass


@config(Bool, 'false', '是否开启经验追赶引导', True, cid=1018)
def enableExpPursueGuide():
    pass


@config(Bool, 'false', '是否统计战力所属类型')
def enableStatsCombatScoreType():
    pass


@config(Bool, 'false', '武道会晋级红包')
def enableArenaPlayoffsRedPacket():
    pass


@config(Bool, 'false', '个人空间迭代版开关', True, cid=1019)
def enablePersonalZoneV2():
    pass


@config(Bool, 'false', '是否逆袭记录玩家属性')
def enablePropLogOnWeakerProtect():
    pass


@config(Bool, 'false', '遇强则强，遇弱则弱修改')
def enableAtkAndDefAdjust():
    pass


@config(Bool, 'false', '是否开启领地战优化_战绩', True, cid=1020)
def enableClanWarOptimizationRecord():
    pass


@config(Bool, 'false', '是否开启领地战优化_事件', True, cid=1021)
def enableClanWarOptimizationEvent():
    pass


@config(Bool, 'false', '是否开启领地战优化_技能', True, cid=1022)
def enableClanWarOptimizationSkill():
    pass


@config(Bool, 'true', '是否开启showBroodLabel优化', True, cid=1023)
def enableOptimizeShowBroodLabel():
    pass


@config(Bool, 'false', '是否开启朋友圈二期', True, cid=1024)
def enableNewPYQ():
    pass


@config(Bool, 'false', '是否开启苍穹之帜战场', True, cid=1025)
def enableCqzzBf():
    pass


@config(Bool, 'false', '是否开启赛跑战场', True, cid=1026)
def enableRaceBattleField():
    pass


@config(Bool, 'false', '是否开启多人聊天', True, cid=1027)
def enableChatGroup():
    pass


@config(Bool, 'false', '英灵传送前检查目标点是否在地图范围内')
def enableSpriteTeleportCheck():
    pass


@config(Bool, 'false', '是否开启新萌妹团活动', True, cid=1028)
def enableNewMissTianyu():
    pass


@config(Bool, 'false', '是否开启付费解锁英灵传记', True, cid=1029)
def enableUnlockSpriteBioInMoney():
    pass


@config(Bool, 'false', '开启卡牌抽卡活动', True, cid=1030)
def enableRandomCardDraw():
    pass


@config(Bool, 'false', '是否开启被动技能的固定属性转移')
def enablePskillPropTransferProp():
    pass


@config(Bool, 'false', '是否开启灵视效果', True, cid=1032)
def enableLingShi():
    pass


@config(Bool, 'false', '是否开启运营屏蔽词库SDK log(需要开启enableEnvSDK)', True, cid=1033)
def enableEnvSDKLog():
    pass


@config(Bool, 'true', '是否开启强制玩家改名(非法名字)', True, cid=1034)
def enableForceRoleRename():
    pass


@config(Bool, 'false', '付费取件支持天币', True, cid=1035)
def enablePayMailCoin():
    pass


@config(Bool, 'false', '是否开启朋友圈话题', True, cid=1036)
def enablePYQTopic():
    pass


@config(Bool, 'false', '官印三期(符纹，徽章独立)', True, cid=1037)
def enableGuanYinThirdPhase():
    pass


@config(Bool, 'false', '同一mac地址地宫打印警告')
def enableSameMacAddressWarning():
    pass


@config(Bool, 'false', '是否开启特殊推荐入口', True, cid=1038)
def enableActivityGuide():
    pass


@config(Bool, 'false', '是否开启技能修炼积分系统(修炼书系统调整)', True, cid=1039)
def enableSkillXiuLianScore():
    pass


@config(Bool, 'false', '竞技场周任务计算场次需要最低治疗、伤害要求', True, cid=1040)
def enableBalanceArenaWeekCntLimit():
    pass


@config(Bool, 'false', '是否开启通行证补发奖励')
def enableNewServerReissueBonus():
    pass


@config(Bool, 'false', '是否开启纹印从装备剥离', True, cid=1041)
def enableSplitWenYinFromEquip():
    pass


@config(Bool, 'false', '是否开启创生按距离销毁')
def enableCreationDestroyByDistance():
    pass


@config(Bool, 'false', '幻鉴洗练多方案', True, cid=1042)
def enableCardWashScheme():
    pass


@config(Bool, 'false', '是否允许试玩开启外网环境', True, cid=1043)
def enableShiwanPublicServerPYQ():
    pass


@config(Bool, 'false', '人物修炼卷轴属性等级回退', True, cid=1044)
def enableGuildGrowthRegress():
    pass


@config(Bool, 'false', '是否开启战场声望奖励', True, cid=1045)
def enableBattleFieldFame():
    pass


@config(Bool, 'false', '是否新的伏羲钱包接口', True, cid=1046)
def enableFtbWalletV2():
    pass


@config(Bool, 'false', '是否使用新的伏羲通宝挖矿接口', True, cid=1047)
def enableFtbV2():
    pass


@config(Bool, 'false', '是否启用副职业', True, cid=1048)
def enableSecondSchool():
    pass


@config(Bool, 'false', '是否开启hot类buff层数改变时刷新状态hijack数据')
def enableRefreshHijackOnHotStateAddLayer():
    pass


@config(Bool, 'false', '是否开启dot类buff层数改变时刷新状态hijack数据')
def enableRefreshHijackOnDotStateAddLayer():
    pass


@config(Bool, 'false', '是否开启被动技能属性扩展', True, cid=1049)
def enablePskillExtraAttr():
    pass


@config(Bool, 'false', '是否自动清除公会联赛赛季积分')
def enableAutoClearGTNScore():
    pass


@config(Bool, 'false', '翼世界传送是否加等级限制')
def enableWingWorldTeleportLvCheck():
    pass


@config(Bool, 'false', '翼世界传送是加等级报警')
def enableWingWorldTeleportLvWaring():
    pass


@config(Str, '0, 0', '技能延时报警与统计（上行阈值、上行+下行阈值，为0则不统计）', True, cid=1050)
def skillDelayCastStatParams():
    pass


@config(Bool, 'false', '幻匣副职业方案开启', True, cid=1051)
def enableSecondSchoolCardSlotScheme():
    pass


@config(Bool, 'false', '幻鉴洗练副职业方案开启', True, cid=1052)
def enableSecondSchoolCardWashScheme():
    pass


@config(Bool, 'false', '武道会应援', True, cid=1053)
def enableArenaPlayoffsAid():
    pass


@config(Bool, 'false', '武道会单轮押注', True, cid=1054)
def enableArenaPlayoffsBetOne():
    pass


@config(Bool, 'false', '限制玩家生成内容', True, cid=1055)
def enableUGCLimit():
    pass


@config(Bool, 'false', '强制限制玩家生成内容(临时开用,需要记得及时关掉)', True, cid=1056)
def enableUGCForceLimit():
    pass


@config(Int, '0', '翼世界之战独立aoi(0不生效)')
def enableWingWarAoIRadius():
    pass


@config(Bool, 'false', '是否开启武道会单个押注', True, cid=1057)
def enablePlayoffsBetDayNew():
    pass


@config(Bool, 'false', '是否自动生效低等级的纹印', True, cid=1058)
def enableLessLvWenYin():
    pass


@config(Bool, 'false', '是否开启翼世界之战清空背包优化')
def enableClearInvInWingWar():
    pass


@config(Bool, 'false', '5v5武道会禁止断线重连')
def enableNoRenter5v5Playoffs():
    pass


@config(Bool, 'false', '是否开启打印机器人行为树log')
def enablePuppetPrintLog():
    pass


@config(Bool, 'false', '是否开启本源神格锁定', True, cid=1059)
def enableBenYuanHirogramLock():
    pass


@config(Bool, 'false', '是否开启徽章神格锁定', True, cid=1060)
def enableGuanYinLock():
    pass


@config(Bool, 'false', '水晶保卫战', True, cid=1061)
def enableHandInItem():
    pass


@config(Bool, 'false', '是否开启水晶大作战（可配置的材料收集活动）推送', True, cid=1062)
def enableCollectItemMessagePush():
    pass


@config(Bool, 'false', '是否开启头顶聊天室', True, cid=1063)
def enableTopChatRoom():
    pass


@config(Bool, 'false', '是否开启网易会员礼包v2')
def enableMembershipGiftV2():
    pass


@config(Bool, 'true', '进本前检查所在场景，公会驻地和地宫要先回大世界')
def enableCheckSceneBeforeFuben():
    pass


@config(Bool, 'false', '是否开启暗杀系统', True, cid=1064)
def enableAssassination():
    pass


@config(Bool, 'true', '是否支持跨服加道行')
def enableAddDaoHengInCross():
    pass


@config(Bool, 'true', '是否支持跨服加无双心得')
def enableAddWSProficiencyInCross():
    pass


@config(Bool, 'true', '是否开启武道会战队特权(人气战队入围小组赛)', True, cid=1065)
def enablePlayoffsTeamPrivilege():
    pass


@config(Int, '-1', '设置武道会赛季(不再按配置的赛季算)', True, cid=1066)
def arenaPlayoffsSeason():
    pass


@config(Bool, 'false', '翼世界国战使用阵营', True, cid=1067)
def enableWingWorldWarCamp():
    pass


@config(Bool, 'false', '翼世界国战阵营报名', True, cid=1068)
def enableWingWorldWarCampSignUp():
    pass


@config(Bool, 'false', '是否开启新战场匹配机制')
def enableNewBattleFieldMatch():
    pass


@config(Bool, 'false', '是否开启战场大乱斗模式', True, cid=1069)
def enableBattleFieldChaosMode():
    pass


@config(Bool, 'false', '翼世界城池吞噬', True, cid=1070)
def enableWingWorldSwallow():
    pass


@config(Str, '', '翼世界时代1被吞噬的城池，以逗号做风格，比如1,2,3', True, cid=1071)
def enableWingCitySwallowList1():
    pass


@config(Str, '', '翼世界时代2被吞噬的城池，以逗号做风格，比如1,2,3', True, cid=1072)
def enableWingCitySwallowList2():
    pass


@config(Str, '', '翼世界时代3被吞噬的城池，以逗号做风格，比如1,2,3', True, cid=1073)
def enableWingCitySwallowList3():
    pass


@config(Bool, 'false', '是否开启动作特效外观', True, cid=1074)
def enableActAppearance():
    pass


@config(Bool, 'false', '是否开启直升2.0', True, cid=1075)
def enableStraightLvUpV2():
    pass


@config(Bool, 'false', '翼世界城池宣战新联通性判断', True, cid=1076)
def enableWingWorldDeclareNewLink():
    pass


@config(Bool, 'false', '翼世界国战使用阵营模式', True, cid=1077)
def enableWingWorldWarCampMode():
    pass


@config(Bool, 'true', '翼世界阵营喇叭', True, cid=1078)
def enableWingWorldCampLaba():
    pass


@config(Bool, 'false', '开启百宝袋奖池抽奖活动', True, cid=1079)
def enableRandomItemsLottery():
    pass


@config(Bool, 'false', '是否开启竞猜', True, cid=1080)
def enableBet():
    pass


@config(Bool, 'false', '是否使用机器人异常状态检测')
def enablePuppetInvalidCheck():
    pass


@config(Bool, 'false', '实名认证开关', True, cid=1081)
def enableRealNameCheck():
    pass


@config(Bool, 'false', 'gt同一urs只能有一个', True, cid=1082)
def enableGtOneAvatar():
    pass


@config(Bool, 'false', '实名游戏时间限制', True, cid=1083)
def enableRealNameGameLimit():
    pass


@config(Bool, 'false', '实名制充值限制', True, cid=1084)
def enableRealNameChargeLimit():
    pass


@config(Bool, 'false', '战场玩法匹配限制多开', True, cid=1085)
def enableFubenMultiLimit():
    pass


@config(Bool, 'false', '发开启公会拍卖按贡献分配', True, cid=1086)
def enableGConsigntmentProfitByWeight():
    pass


@config(Bool, 'false', '是否开启打图玩法', True, cid=1087)
def enableMapGame():
    pass


@config(Bool, 'false', '是否开启百宝袋推送', True, cid=1088)
def enableRandomTreasureBagMainMessagePush():
    pass


@config(Bool, 'false', '是否开启百宝袋活动', True, cid=1089)
def enableRandomTreasureBagMain():
    pass


@config(Bool, 'false', '战场匹配最低战力分组')
def enableGroupByCombatScoreInBF():
    pass


@config(Bool, 'false', '是否开启悬赏暗杀-雇主收到暗杀成功的推送', True, cid=1090)
def enableAssEmployerPush():
    pass


@config(Bool, 'false', '是否开启公会权限重置')
def enableInitGuildPrivilege():
    pass


@config(Bool, 'false', '是否开启天币付费邮件物品白名单')
def enableCoinPayMailItemWhiteList():
    pass


@config(Bool, 'false', '是否开启领地战公会拍卖按贡献分红')
def enableClanWarConsignProfitByContribute():
    pass


@config(Bool, 'false', '是否开启元宝寄售上架')
def enableCoinConsignPlace():
    pass


@config(Int, '10000', '打图副本怪额外乘数 10000表示100%', True, cid=1091)
def mapGameFubenMultiply():
    pass


@config(Bool, 'false', '被动技能给英灵加被动/属性', True, cid=1092)
def enablePSkillExtraEffect():
    pass


@config(Bool, 'false', '幻鉴装备时做套装检查', True, cid=1093)
def enableCheckCardSuitOnFix():
    pass


@config(Bool, 'false', '飞火渠道是否进行实名')
def enableFeihuoRealName():
    pass


@config(Bool, 'false', '是否开启领地战押镖', True, cid=1094)
def enableClanWarCourier():
    pass


@config(Bool, 'false', '打图玩法,私服本身作为中心服, 如果配置了中心服，会有中心服会失效')
def enableMapGameDebugMode():
    pass


@config(Bool, 'false', '是否开启英灵亲密度优化', True, cid=1095)
def enableSpriteFamiV2():
    pass


@config(Bool, 'true', '发邮件时,超过堆叠自动拆分')
def enableAutoSplitMail():
    pass


@config(Bool, 'true', '数据延迟更新到中心服')
def enableMapGameDelayUpdate():
    pass


@config(Bool, 'false', '是否开启天币邮件物品交易限制', True, cid=1096)
def enableCoinMailHandoverCheck():
    pass


@config(Bool, 'false', '是否开启翼世界新赛季军队', True, cid=1097)
def enableWingWorldCampArmy():
    pass


@config(Bool, 'false', '是否开启NPC好感度', True, cid=1098)
def enableNpcFavor():
    pass


@config(Bool, 'false', '英灵亲密转移春节开关', True, cid=1099)
def enableSpriteFamiTransferInFestival():
    pass


@config(Bool, 'false', '打图奖励是否可以领取', True, cid=1100)
def enableMapGameReward():
    pass


@config(Bool, 'false', '翼世界阵营不计一周未登录的玩家实力', True, cid=1101)
def enableWWCIgnoreInActivePower():
    pass


@config(Bool, 'false', '是否开启英灵爬塔', True, cid=1102)
def enableSpriteChallenge():
    pass


@config(Bool, 'false', '是否开启城战', True, cid=1103)
def enableOpenWingWorldWar():
    pass


@config(Bool, 'false', '是否开启军阶追赶', True, cid=1104)
def enablePursueJunJie():
    pass


@config(Bool, 'false', '是否开启手工装提炼', True, cid=1105)
def enableRefineManualEquipment():
    pass


@config(Bool, 'false', '出战英灵亲密获取调整')
def enableSpriteAddFamiV2():
    pass


@config(Bool, 'false', '是否开启熔炉工会拍卖优化')
def enableSendForgeGConsignRightNow():
    pass


@config(Bool, 'false', '是否使用计费序列号业务新域名')
def enableNewNetBarRewardHost():
    pass


@config(Bool, 'false', '是否开启吃鸡战场', True, cid=1106)
def enablePUBG():
    pass


@config(Str, '', '打图副本怪额外乘数 按格子类型分', True, cid=1107)
def mapGameFubenMultiplyEx():
    pass


@config(Bool, 'false', '是否开启血战碎星屿', True, cid=1108)
def enableGSXY():
    pass


@config(Bool, 'false', '是否使用新一键换装面板', True, cid=1109)
def enableQuickReplaceEquipmentV2():
    pass


@config(Bool, 'false', '是否开启见闻系统', True, cid=1110)
def enableCollectionSystem():
    pass


@config(Bool, 'false', '翼世界阵营模式个人实力1周有效', True, cid=1111)
def enableWingWorldCampPowerExpire():
    pass


@config(Str, '', '翼世界城战地图进入分城池等级人数限制', True, cid=1112)
def wingWorldWarCityMaxCountEx():
    pass


@config(Bool, 'false', '是否开启每日福利超值礼包优化活动', True, cid=1113)
def enableDailyWelfareActivityOptimize():
    pass


@config(Bool, 'false', '登录时触发纹印触发器(equipmentTrigger)')
def enableLogonWenYinTrigger():
    pass


@config(Bool, 'false', '万灵之主立即拍卖')
def enableWingSoulBossDelayConsign():
    pass


@config(Int, '0', '血战碎星屿独立aoi（0不生效）')
def enableGSXYAoIRadius():
    pass


@config(Bool, 'false', '是否开启英灵爬塔增益显示', True, cid=1114)
def enableSpriteChallengeSpBuff():
    pass


@config(Bool, 'false', '是否开启手工装制作材料优惠', True, cid=1115)
def enableManualEquipMaterialDiscount():
    pass


@config(Bool, 'false', '跟随队长时不直接传送', True, cid=1116)
def enableFollowNotAutoTeleport():
    pass


@config(Bool, 'true', '模板的符文不存在时使用装备生成', True, cid=1117)
def enableCharTempGuanYinUseEquip():
    pass


@config(Bool, 'false', '是否开启新纹印操作', True, cid=1118)
def enableNewWenYinOp():
    pass


@config(Bool, 'true', '模板的纹印不存在时使用装备生成', True, cid=1119)
def enableCharTempWenYinUseEquip():
    pass


@config(Bool, 'false', '战场人数超过限制报警')
def enableBattleFieldMaxNumWarn():
    pass


@config(Str, '', '战场人数超过限制报警')
def battleFieldWarnNumLimit():
    pass


@config(Bool, 'false', '机器人是否开启新的装备切换')
def enbalePuppetNewEquip():
    pass


@config(Bool, 'false', '宝箱次数延迟刷新(确保在dailyReset后才刷)')
def enbaleTreasureBoxHistoryDelayReset():
    pass


@config(Bool, 'false', '移除额外属性失败，尝试移除另一effectType的属性')
def enablePSkillExtraEffectTryRemove():
    pass


@config(Bool, 'false', '人物修炼附赠属性开关', True, cid=1120)
def enableGuildGrowthExtraPropsAdd():
    pass


@config(Bool, 'true', '斩魔极星级boss', True, cid=1121)
def enableZMJStarBoss():
    pass


@config(Bool, 'true', '模板名将方案', True, cid=1122)
def enableCharTempFamousGeneral():
    pass


@config(Bool, 'true', '跨服切换装备', True, cid=1123)
def enableSwitchEquipInSoul():
    pass


@config(Bool, 'false', '战力追赶道具奖励开关', True, cid=1124)
def enableCombatScoreListReward():
    pass


@config(Bool, 'false', '亲密度英灵对属性加成', True, cid=1125)
def enableSpriteFamiliarAdd():
    pass


@config(Bool, 'false', 'buff随src距离删除')
def enableRmStateBySrcDist():
    pass


@config(Bool, 'true', '吃鸡模板技能栏只保存右下角2块(1,4),其它部分公用。且共用schemeNo')
def enablePubgShortSplit():
    pass


@config(Bool, 'true', '吃鸡技能栏单独保存schemeNo')
def enablePubgShortcutSchemeNo():
    pass


@config(Bool, 'true', '吃鸡技能栏单独保存右下角部分scheme(1,4)')
def enablePubgShortcutSchemeVal():
    pass


@config(Bool, 'false', '集结活动开关', True, cid=1126)
def enableActivityCollect():
    pass


@config(Bool, 'false', '伏羲通宝用http', True, cid=1127)
def enableFTBHttp():
    pass


@config(Bool, 'false', '伏羲通宝活动', True, cid=1128)
def enableFTBActivity():
    pass


@config(Bool, 'true', '穿透护盾/吸收效果')
def enableIgnoreShield():
    pass


@config(Bool, 'false', '重置钱包密码', True, cid=1129)
def enableResetFTBPasswd():
    pass


@config(Bool, 'true', '移形换位直接传')
def enableTeleportNoCheck():
    pass


@config(Int, '5', '伏羲通宝拉取间隔')
def ftbActPullInterval():
    pass


@config(Bool, 'false', '是否显示客户端的伏羲通宝活动按钮', True, cid=1130)
def enableFTBActivityClient():
    pass


@config(Bool, 'true', 'dpsMonster额外统计信息', True, cid=1131)
def enableDpsMonsterEx():
    pass


@config(Bool, 'false', '消费解除因历史消费返还导致的藏宝阁冻结', True, cid=1132)
def enableConsumeUnfreezeCbg():
    pass


@config(Bool, 'false', '是否开启天昭这个新职业，允许创建业天昭号', True, cid=1133)
def enableNewSchoolTianZhao():
    pass


@config(Bool, 'false', '是否开启上传traceback到appdump', True, cid=1134)
def enableUploadTBToAppdump():
    pass


@config(Bool, 'true', '吃鸡人少关战场防刷')
def enablePUBGMinNumLimit():
    pass


@config(Bool, 'true', '吃鸡组队容错')
def enablePUBGDoubleCheckBuildGroup():
    pass


@config(Bool, 'false', '打图2期', True, cid=1135)
def enableMapGameV2():
    pass


@config(Bool, 'false', '是否开启英灵爬塔假排名', True, cid=1136)
def enableSpriteChallengeUnRealRank():
    pass


@config(Bool, 'false', '统计商城天币累计消费')
def enableRecordMallUnbindCoin():
    pass


@config(Bool, 'false', '是否开启谕币可以天币抵扣功能', True, cid=1137)
def enableMallCashCoinPay():
    pass


@config(Bool, 'false', '英灵技能槽概率解锁', True, cid=1138)
def enableSpriteSkillLuckyUnlock():
    pass


@config(Bool, 'false', '是否开启商城非消费返还角色专用购买道具功能', True, cid=1139)
def enableNoHistoryConsumedBuy():
    pass


@config(Bool, 'false', '是否开启新匹配规则', True, cid=1140)
def enableNewChooseQueue():
    pass


@config(Bool, 'true', '是否开启雾夜逃杀新面板', True, cid=1141)
def enablePVPPUBGProxy():
    pass


@config(Bool, 'false', '是否开启挚友邀请功能', True, cid=1142)
def enableFriendInviteActivityOp():
    pass


@config(Bool, 'false', '翼世界报名组队', True, cid=1143)
def enableWingWorldWarQueueV2():
    pass


@config(Bool, 'false', '地宫心魔', True, cid=1144)
def enableMLShaxing():
    pass


@config(Bool, 'false', '打图1期', True, cid=1145)
def enableMapGameV1():
    pass


@config(Bool, 'false', '战场金堇花币奖励', True, cid=1146)
def enableBattleJinbiReward():
    pass


@config(Bool, 'false', '藏宝阁道具交易', True, cid=1147)
def enableCBGItem():
    pass


@config(Str, '', '打图副本阈值')
def mapGameFubenDmgLimit():
    pass


@config(Bool, 'false', '是否开启WWArmy的combatMsg.msg的内服测试')
def enableWWArmyCombatMsgTest():
    pass


@config(Bool, 'false', '是否开启赛龙舟赛', True, cid=1148)
def enableLZSBattleField():
    pass


@config(Bool, 'false', '工会捐献黑名单功能', True, cid=1149)
def enableGuildDonateBlackList():
    pass


@config(Bool, 'false', '装备打造白名单功能', True, cid=1150)
def enableMakeManualEquipWhiteList():
    pass


@config(Bool, 'false', '是否开启Puppet的服务端寻路')
def enablePuppetRecast():
    pass


@config(Bool, 'false', '是否开启副本关闭延后', True, cid=1152)
def enableTimerDestroyConqueredEmptyFb():
    pass


@config(Bool, 'false', '是否开启新人宝箱', True, cid=1153)
def enableNewPlayerTreasureBox():
    pass


@config(Bool, 'false', '是否开启天币机器人自动购买与下架')
def enableCoinMarketAutoBuyAndCancel():
    pass


@config(Bool, 'false', '是否开翼世界城战消极战斗', True, cid=1154)
def enableWingWorldWarInactive():
    pass


@config(Bool, 'false', '是否开启反外挂log记录', True, cid=1155)
def enableGameAntiCheatingLog():
    pass


@config(Bool, 'false', '是否开启备选官印', True, cid=1156)
def enableSubGuanYin():
    pass


@config(Bool, 'false', '是否开启备选纹印', True, cid=1157)
def enableSubWenYin():
    pass


@config(Bool, 'false', '是否开翼世界军团集结', True, cid=1158)
def enableWingWorldArmyGather():
    pass


@config(Bool, 'true', '是否开启新人宝箱获得双人宝箱开启检测', True, cid=1159)
def enableNTMultiTreasureBoxOpenCheck():
    pass


@config(Bool, 'false', '特殊效果，召唤多英灵', True, cid=1160)
def enableMultiSpriteBySE():
    pass


@config(Bool, 'false', '声望冻结')
def enableFreezeFame():
    pass


@config(Bool, 'false', '启用元宝交易延迟拉去')
def enableCoinMarketDelayFetch():
    pass


@config(Bool, 'false', '心动值开关', True, cid=1163)
def enableNFWHeartbeat():
    pass


@config(Bool, 'false', '好感新任务开关', True, cid=1164)
def enableNFNewQuestLoop():
    pass


@config(Bool, 'false', '额外参数动作原件开关', True, cid=1165)
def enableIncExtraVal():
    pass


@config(Str, '', '地宫进入限制开关')
def enableDiGongEnterLimit():
    pass


@config(Bool, 'false', '世界boss开关', True, cid=1167)
def enableWorldBoss():
    pass


@config(Bool, 'false', '渠道实名认证', True, cid=1168)
def enablePlatformRealNameCheck():
    pass


@config(Bool, 'false', '双人植树开关', True, cid=1169)
def enableDoublePlantTree():
    pass


@config(Bool, 'false', '幻匣共鸣开关', True, cid=1170)
def enableCardSlotResonance():
    pass


@config(Bool, 'false', '落后服专属奖励找回', True, cid=1171)
def enableRewardCatchUp():
    pass


@config(Bool, 'false', '注入屏蔽部分显示', True, cid=1172)
def enableHijackHide():
    pass


@config(Bool, 'false', '允许匿名频道', True, cid=1173)
def enableChatAnonymity():
    pass


@config(Bool, 'false', '特殊活动限制公会操作', True, cid=1174)
def enableLimitStatus():
    pass


@config(Bool, 'false', '定时吃鸡开关', True, cid=1175)
def enableTimingPUBG():
    pass


@config(Bool, 'false', '是否强制跳过Avatar状态容错检查')
def enableSkipAvatarStatesCheck():
    pass


@config(Bool, 'true', '允许称号可以附加属性', True, cid=1176)
def enableTitleWithProp():
    pass


@config(Bool, 'false', '打图阵营开关', True, cid=1177)
def enableMapGameCamp():
    pass


@config(Bool, 'false', '公会联赛段位赛开关', True, cid=1178)
def enableGuildRankTournament():
    pass


@config(Bool, 'false', '是否允许伏羲外挂检测踢除玩家')
def enableKickoutIllegalPlayersByFuxi():
    pass


@config(Bool, 'true', '符文一键切换', True, cid=1179)
def enableGuanYinOneKeyScheme():
    pass


@config(Bool, 'false', '单/双人生死场是否开启新赛事规则（淘汰赛变为晋级赛）', True, cid=1180)
def enableNewMatchRuleSSC():
    pass


@config(Bool, 'true', '纹印一键切换', True, cid=1181)
def enableWenYinOneKeyScheme():
    pass


@config(Bool, 'true', '装备一键切换', True, cid=1182)
def enableEquipOneKeyScheme():
    pass


@config(Int, '0', '禁止其它一键切换[无双，属性，技能点，技能栏，蕴灵，幻鉴]', True, cid=1183)
def enableOthersOneKeyScheme():
    pass


@config(Bool, 'true', '幻鉴指定洗练')
def enableWashCardFixedProps():
    pass


@config(Bool, 'false', '文印离线查询')
def enableWenYinOffLineQuery():
    pass


@config(Bool, 'false', '天昭排行榜开关', True, cid=1184)
def enableTianZhaoTopRank():
    pass


@config(Bool, 'false', '排行榜89级新加1类', True, cid=1185)
def enableTopRankNewLv89():
    pass


@config(Bool, 'false', '论战云巅是否开启', True, cid=1186)
def enableLunZhanYunDian():
    pass


@config(Bool, 'false', '装备直升是否开启', True, cid=1187)
def enableUpgradeManaulEquip():
    pass


@config(Bool, 'false', '是否开启新版公会联赛', True, cid=1188)
def enableNewGuildTournament():
    pass


@config(Bool, 'false', '是否开启PVE新属性pveQuota')
def enablePveQuota():
    pass


@config(Bool, 'false', '是否开启双十一打图玩法', True, cid=1189)
def enableMapGameV3():
    pass


@config(Bool, 'false', '是否开启墓碑打图玩法', True, cid=1190)
def enableMapGameGrave():
    pass


@config(Bool, 'false', '是否开启装备套装高等级替换低等级', True, cid=1191)
def enableEquipSuitReplace():
    pass


@config(Bool, 'true', '踢出gt同usr玩家', True, cid=1192)
def enableGtOneAvatarKick():
    pass


@config(Bool, 'true', 'attackOthers忽视非战斗单元')
def enableAttackOthersNoBU():
    pass


@config(Int, '0', '设置机器人固定职业')
def enablePuppetFixedSchool():
    pass


@config(Int, '0', '翼世界根据时间检查是否需要重置 const.WING_WORLD_CAMP_PLAYER_CHECK_TIME')
def enableWingWorldCampTimerReset():
    pass


@config(Bool, 'false', '是否开启89级', True, cid=1193)
def enableNewLv89():
    pass


@config(Bool, 'false', '世界BOSS提示')
def enableWorldBossShowTip():
    pass


@config(Bool, 'false', '是否开启宝箱概率可视化功能', True, cid=1194)
def enableTreasureBoxVisible():
    pass


@config(Bool, 'false', '是否开启89级部分老属性从代码改为配表', True, cid=1195)
def enableNewPropCalcByFormula():
    pass


@config(Bool, 'false', '门派任务切换7职业', True, cid=1196)
def questSwitch7School():
    pass


@config(Bool, 'false', '门派任务切换8职业', True, cid=1197)
def questSwitch8School():
    pass


@config(Bool, 'false', '是否开启易宝实名认证', True, cid=1198)
def enableEpayActive():
    pass


@config(Bool, 'false', '翼世界活跃玩家3分钟贡献要求')
def enableWingWorldContriLimit():
    pass


@config(Bool, 'false', '是否禁止npc和dawdler的功能', True, cid=1199)
def enableForbidNpcAndDawdler():
    pass


@config(Bool, 'false', '是否开启转服奖励追赶', True, cid=1200)
def enableMigrateRewardCatchUp():
    pass


@config(Bool, 'false', '强制刷新普通商店', True, cid=1201)
def enableRefreshNormalPrivateShop():
    pass


@config(Bool, 'false', '注销账号管理模块', True, cid=1202)
def enableDelUrsStub():
    pass


@config(Bool, 'false', '真实伤害使用面板属性')
def enableRealDmgUseStaticProp():
    pass


@config(Bool, 'false', '魂界封魂开关', True, cid=1203)
def enableHuntGhost():
    pass


@config(Bool, 'false', '神格数量限制开关', True, cid=1204)
def enableHierogramLimit():
    pass


@config(Bool, 'false', '是否开启fbEntityFixLvMax修正', True, cid=1205)
def enableFbEntityFixLvMax():
    pass


@config(Bool, 'false', '是否开启天昭登陆界面跳过演示', True, cid=1206)
def enableTianZhaoLoginShowIgnore():
    pass


@config(Bool, 'false', '是否开启89资料片时79经验转元神', True, cid=1207)
def enableChangeExpToExpXiuWei():
    pass


@config(Bool, 'false', '是否开启新直升等级计算方式', True, cid=1208)
def enableStraightLvUpV2New():
    pass


@config(Bool, 'false', '是否开启80级元神福利', True, cid=1209)
def enableExpXiuWeiWelfare():
    pass


@config(Bool, 'false', '是否开启经验转换元神适用于任务奖励以及传功', True, cid=1210)
def enableExpToYuanshen():
    pass


@config(Bool, 'true', '是否开启每日修盈经验发放', True, cid=1211)
def enableAssignDailyVp():
    pass


@config(Bool, 'false', '翼世界阵营模式,用玩家身上的阵营在wingWorldCampStub/crossWingWorldCampStub生成一份数据')
def enableWWCMValFix():
    pass


@config(Str, '1101111111000', '藏宝阁寄售职业限制', True, cid=1212)
def cbgRoleSaleSchoolLimit():
    pass


@config(Bool, 'false', '是否开启装备磨损计算新开关', True, cid=1213)
def enableNewDurability():
    pass


@config(Bool, 'false', '89级任务怪强制魔性pveQuota重置为0::#205938', True, cid=1214)
def enablePveQuotaReset():
    pass


@config(Bool, 'false', '是否允许逍遥项链进化橙字属性')
def enableXYnecklaceEnhanceSes():
    pass


@config(Bool, 'false', '是否允许831/832状态特殊效果生效')
def enableTZStateSpecialEffect831():
    pass


@config(Bool, 'false', '是否临时修复生死场异常开关')
def enableSSCStatusFix():
    pass


@config(Bool, 'false', '结契面板V2', True, cid=1215)
def enableJieQiV2():
    pass


@config(Bool, 'false', '是否开启重置所有属性点方案')
def enableResetAllPropSchemeForNewLv():
    pass


@config(Str, '1,0.07', '论战云巅间隔创建副本')
def createLzydTimeLimit():
    pass


@config(Bool, 'false', '是否开启公会拍卖收税')
def enableGuildConsignProfitTax():
    pass


@config(Bool, 'false', '是否开启幸运值抽奖活动', True, cid=1216)
def enableLuckyLottery():
    pass


@config(Bool, 'false', '天昭技能点方案重置')
def enableTZSchemeSkillPointReset():
    pass


@config(Bool, 'false', '是否开启装备改造材料抵扣', True, cid=1217)
def enableManualDiKou():
    pass


@config(Bool, 'false', '吃鸡新刷安全区')
def enablePUBGNewSafeArea():
    pass


@config(Bool, 'false', '落后服专属奖励找回优化', True, cid=1218)
def enableRewardCatchUpOptimize():
    pass


@config(Bool, 'false', '是否上报到测试平台')
def enableReportToPlatform():
    pass


@config(Bool, 'false', '开启转职消耗', True, cid=1219)
def enableSchoolTransferConditionItemCost():
    pass


@config(Bool, 'false', '开启跨服段位赛观战', True, cid=1220)
def enableNewGuildTournamentLiveAndInspire():
    pass


@config(Bool, 'true', '开启crontab优先判断固定时间戳优化', True, cid=1221)
def enableCheckCrontabStrIsFixedTimeStamp():
    pass


@config(Bool, 'false', '是否开启DOTA免费随机英雄', True, cid=1222)
def enableDotaFreeRandomRole():
    pass


@config(Bool, 'false', '是否开启精炼套装并关闭蕴灵系统', True, cid=1223)
def enableEquipEnhanceSuit():
    pass


@config(Bool, 'false', '是否开启showBroodLabel优化-版本2', True, cid=1224)
def enableOptimizeShowBloodLabelV2():
    pass


@config(Bool, 'false', '是否开启幻鉴多次洗练', True, cid=1225)
def enableAutoWashCard():
    pass


@config(Bool, 'false', '是否开启跨服公会联赛技能', True, cid=1226)
def enableGuildCrossSkill():
    pass


@config(Bool, 'false', '是否开启雾影苏澜', True, cid=1227)
def enableWuYinSuLan():
    pass
