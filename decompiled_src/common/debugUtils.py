#Embedded file name: I:/bag/tmp/tw2/res/entities\common/debugUtils.o
import BigWorld
import inspect
INCEPTION_ENABLE = True

def getmembers(obj, predicate = None):
    """Return all members of an object as (name, value) pairs sorted by name.
    Optionally, only return members that satisfy a given predicate."""
    results = []
    for key in dir(obj):
        try:
            value = getattr(obj, key)
        except AttributeError:
            continue
        except TypeError:
            continue

        if not predicate or predicate(value):
            results.append((key, value))

    results.sort()
    return results


class MethodIncepter(object):

    def __init__(self, obj, needFilterMethodMap, contextNameAllowed = False):
        """needFilterMethodMap \xd0\xe8\xd2\xaa\xc0\xb9\xbd\xd8\xb5\xc4\xb7\xbd\xb7\xa8
        contextNameAllowed \xd2\xd4\xc0\xe0\xc3\xfb+\xb7\xbd\xb7\xa8\xc3\xfb\xb5\xc4\xb7\xbd\xca\xbd\xc0\xb9\xbd\xd8"""
        self.obj = obj
        self.needFilterMethodMap = needFilterMethodMap
        self.contextNameAllowed = contextNameAllowed

    def decorate(self, needFilter = True):
        """needFilter \xd0\xe8\xd2\xaa\xb9\xfd\xc2\xcb\xb5\xf4\xc4\xb3\xd0\xa9\xb7\xbd\xb7\xa8"""
        for name, fun in getmembers(self.obj, inspect.ismethod):
            if needFilter:
                if self.needFilterMethodMap.has_key(name):
                    self.operate(name, fun)
            else:
                self.operate(name, fun)

    def inception(self, name, args, kv):
        global focusMethod
        if INCEPTION_ENABLE:
            contextName = self.obj.__class__.__name__ + '.' + name
            if name in focusMethod:
                methodInception = getMethodInception(self.obj, name)
                return '--------@M.L.incepted1	' + contextName + '	' + str(args) + '	' + str(kv) + '	' + methodInception
            if contextName in focusMethod:
                methodInception = getMethodInception(self.obj, contextName)
                return '--------@M.L.incepted	' + contextName + '	' + str(args) + '	' + str(kv) + '	' + methodInception

    def operate(self, name, fn):
        """\xc0\xb9\xbd\xd8\xb7\xbd\xb7\xa8"""

        def incept(*args, **kv):
            if name in needStackMethod:
                import traceback
                print '----------------@M.L.incepted stack start----------------'
                for i in traceback.extract_stack():
                    if 'incept' not in i:
                        print '--------@M.L.incepted stack', i

                print '----------------@M.L.incepted stack end----------------'
            inception = self.inception(name, args, kv)
            if inception:
                print inception
            ret = fn(*args, **kv)
            return ret

        setattr(self.obj, name, incept)


needStackMethod = ['playActionWithFx']
focusMethod = {'doFuncByEvent': ['BigWorld.entity(self.ownerID).qinggongState', 'BigWorld.entity(self.ownerID).qinggongMgr.state'],
 'startState': ['$p.qinggongState', '$p.qinggongMgr.state'],
 'set_qinggongState': ['$p.qinggongState'],
 'movingNotifier': ['self.model.queue', 'self.fashion.playedAction'],
 'doQinggongPlayerAction': [],
 'doQinggongAction': ['$p.qinggongState'],
 'qinggongActionFailed': ['$p.qinggongState'],
 'qinggongStateFailed': ['$p.qinggongState'],
 '_real_startJump': [],
 'startFlyAccelerate': ['#开始加速', 'self.flyType', 'self.physics.velocity'],
 'startFlyDecelerate': ['#开始减速', 'self.flyType', 'self.physics.velocity'],
 'acceleratingEndNotifier': ['#加速完毕', 'self.flyType', 'self.physics.velocity'],
 'endFlyAccelerate': ['self.physics.maxTopVelocity', '$p.fashion.doingActionType()'],
 'setUpSpeedMultiplier': [],
 'checkMove': ['$p.fashion.doingActionType()',
               '$p.isGuiding',
               '$p.castSkillBusy',
               '$p.skillPlayer.castLoop',
               '$p.clientControl',
               '$p.isFalling',
               '$p.publicFlags',
               '$p.flags',
               '$p.spellingType',
               '$p.isPathfinding'],
 'checkLockMoveActionWing': [],
 'updateVelocity': ['$p.qinggongState',
                    '$p.jumpState',
                    'self.upwardMagnitude',
                    'self.upSpeedMultiplier',
                    'self.speedMultiplier',
                    'self.forwardMagnitude',
                    'self.backwardMagnitude',
                    'self.rightwardMagnitude',
                    'self.leftwardMagnitude',
                    'self.isInAccelerating()',
                    'self.isInDecelerating()',
                    '$p.physics.keepJumpVelocity',
                    '$p.isJumping',
                    '$p.physics.jumping'],
 'doShake': [],
 'playDieAction': [],
 'useSkillByKeyDown': ['self.isChargeKeyDown'],
 'checkSkill': [],
 'checkSkillCanUse': ['self.publicFlags',
                      'self.isGuiding',
                      'self.isForceMove',
                      'self.fashion.doingActionType()',
                      'self.bsState',
                      'self.spellingType'],
 'afterCheckSkillCanUse': ['self.spellingType',
                           'self.isUseQingGong',
                           'self.skillPlayer.skillID',
                           'self.isDashing',
                           'self.isJumping'],
 'useskill': ['$p.physics.isSliding', '$p.isWaitSkillReturn', '$p.publicFlags'],
 'startSpell': [],
 'skillStart': [],
 'skillResult': [],
 'guideSkillResult': [],
 'startSpell': [],
 'stopCast': [],
 'stopSpell': [],
 'endSpell': [],
 'stopSpellHelper': [],
 'flyPeriod': [],
 'guideSkillResultPosition': [],
 'castSkill': [],
 'leaveDash': [],
 'doAction': ['$p.inMoving()'],
 'playSingleAction': ['$p.inMoving()'],
 'playAction': ['$p.inMoving()'],
 'playActionWithFx': ['$p.inMoving()'],
 'playActionSequence': ['$p.inMoving()'],
 'playActionSequence2': ['$p.inMoving()'],
 'stopAction': [],
 'stopActionByName': [],
 'stopModelAction': [],
 'beginForceMoveWithCallback': [],
 'jumpEnd': [],
 'resetFly': []}
periodTimer = None
enableTimer = None

def beginPeriodTimer():
    global periodTimer
    if not enableTimer:
        return
    p = BigWorld.player()
    print '----------------beginPeriodTimer', p.physics.velocity
    periodTimer = BigWorld.callback(0.1, beginPeriodTimer)


def getMethodInception(self, methodName):
    inception = '['
    contextAttrs = focusMethod.get(methodName, [])
    if contextAttrs:
        try:
            for attr in contextAttrs:
                attr = attr.replace('$p', 'BigWorld.player()')
                if attr.startswith('#'):
                    inception = inception + str(attr[1:]) + ', '
                else:
                    inception = inception + attr.split('.')[-1] + ':' + str(eval(attr)) + ', '

        except Exception as e:
            print '-----incepted error, methodName:', methodName, e

    inception = inception + ']'
    return inception


if BigWorld.component in 'client':
    from impl.impQuest import ImpQuest
    from impl.impChat import ImpChat
    from impl.impTeam import ImpTeam
    from impl.impArena import ImpArena
    from impl.impItem import ImpItem
    from impl.impTrade import ImpTrade
    from impl.impFuben import ImpFuben
    from impl.impAction import ImpAction
    from impl.impProperty import ImpProperty
    from impl.impSwim import ImpSwim
    from impl.impRide import ImpRide
    from impl.impBianshen import ImpBianshen
    from impl.impTutorial import ImpTutorial
    from impl.impSignIn import ImpSignIn
    from impl.impQieCuo import ImpQieCuo
    from impl.impFriend import ImpFriend
    from impl.impTop import ImpTop
    from impl.impBattleField import ImpBattleField
    from impl.impShengSiChang import ImpShengSiChang
    from impl.impAchievement import ImpAchievement
    from impl.impActivities import ImpActivities
    from impl.impMultiLine import ImpMultiLine
    from impl.impStorage import ImpStorage
    from impl.impFishing import ImpFishing
    from impl.impBooth import ImpBooth
    from impl.impRune import ImpRune
    from impl.impMail import ImpMail
    from impl.impQte import ImpQte
    from impl.impEmote import ImpEmote
    from impl.impDelegate import ImpDelegate
    from impl.impConsign import ImpConsign
    from impl.impExplore import ImpExplore
    from impl.impGuild import ImpGuild
    from impl.impPlayerCombat import ImpPlayerCombat
    from impl.impPlayerUI import ImpPlayerUI
    from impl.impPlayerRideFly import ImpPlayerRideFly
    from impl.impPlayerProperty import ImpPlayerProperty
    from impl.impPlayerItem import ImpPlayerItem
    from impl.impPlayerNpc import ImpPlayerNpc
    from impl.impPlayerDebug import ImpPlayerDebug
    from impl.impPlayerSwim import ImpPlayerSwim
    from impl.impPlayerTeam import ImpPlayerTeam
    from impl.impPlayerBooth import ImpPlayerBooth
    from impl.impPlayerSight import ImpPlayerSight
    from impl.impReport import ImpReport
    from iCombatUnit import IAvatarCombatUnit
    from iCombatUnit import IMonsterCombatUnit
    from iCombatUnit import ICombatUnit
    from iClient import IClient
    from iDisplay import IDisplay
    from iPickable import IPickable
    from Avatar import Avatar
    from Avatar import PlayerAvatar
    from Monster import Monster

    def getAvatarMethod():
        methodMap = {}
        modules = (ImpSwim,
         ImpRide,
         ImpQuest,
         ImpChat,
         ImpTeam,
         ImpItem,
         ImpTrade,
         ImpFuben,
         ImpBattleField,
         ImpShengSiChang,
         ImpProperty,
         ImpAction,
         ImpArena,
         ImpTutorial,
         ImpReport,
         ImpBianshen,
         ImpAchievement,
         ImpActivities,
         ImpSignIn,
         ImpQieCuo,
         ImpTop,
         ImpMultiLine,
         ImpFriend,
         ImpStorage,
         ImpBooth,
         ImpFishing,
         ImpRune,
         ImpMail,
         ImpQte,
         ImpDelegate,
         ImpEmote,
         ImpConsign,
         ImpExplore,
         ImpGuild,
         Avatar,
         IAvatarCombatUnit,
         ICombatUnit,
         IClient,
         IDisplay,
         IPickable,
         ImpPlayerSwim,
         ImpPlayerCombat,
         ImpPlayerRideFly,
         ImpPlayerProperty)
        for module in modules:
            for name, fun in inspect.getmembers(module, inspect.ismethod):
                methodMap[name] = name

        return methodMap


    def getClientPlayerMethod():
        methodMap = {}
        modules = (PlayerAvatar,
         ImpPlayerSwim,
         ImpPlayerCombat,
         ImpPlayerRideFly,
         ImpPlayerProperty,
         ImpPlayerNpc,
         ImpPlayerItem,
         ImpPlayerDebug,
         ImpPlayerUI,
         ImpPlayerTeam,
         ImpPlayerBooth,
         ImpPlayerSight)
        for module in modules:
            for name, fun in inspect.getmembers(module, inspect.ismethod):
                methodMap[name] = name

        avatarMap = getAvatarMethod()
        methodMap.update(avatarMap)
        return methodMap


    def getMonsterMethod():
        methodMap = {}
        modules = (Monster,
         IMonsterCombatUnit,
         ICombatUnit,
         IClient,
         IDisplay,
         IPickable)
        for module in modules:
            for name, fun in inspect.getmembers(module, inspect.ismethod):
                methodMap[name] = name

        return methodMap


    def inceptPlayer():
        methodMap = getClientPlayerMethod()
        MethodIncepter(BigWorld.player(), methodMap).decorate()
        MethodIncepter(BigWorld.player().qinggongMgr, {}).decorate(False)
        MethodIncepter(BigWorld.player().ap, {}).decorate(False)
        MethodIncepter(BigWorld.player().fashion, {}).decorate(False)
        MethodIncepter(BigWorld.player().jumpActionMgr, {}).decorate(False)
        MethodIncepter(BigWorld.player().stateMachine, {}).decorate(False)
        MethodIncepter(BigWorld.player().am, {}).decorate(False)
        MethodIncepter(BigWorld.player().physics, {}).decorate(False)
        MethodIncepter(BigWorld.player().clientStateEffect, {}).decorate(False)
        MethodIncepter(BigWorld.player().modelServer, {}).decorate(False)
        MethodIncepter(BigWorld.player().skillPlayer, {}).decorate(False)
        MethodIncepter(BigWorld.player().modelServer.leftWeaponModel, {}).decorate(False)
        MethodIncepter(BigWorld.player().modelServer.rightWeaponModel, {}).decorate(False)
        import gameglobal
        MethodIncepter(gameglobal.rds.ui, {}).decorate(False)
        for attr in gameglobal.rds.ui.__dict__.values():
            if attr and attr.__class__.__name__.endswith('Proxy'):
                MethodIncepter(attr, {}, True).decorate(False)

        from helpers import navigator
        MethodIncepter(navigator.getNav(), {}).decorate(False)
        print '-------player incepted'


    def inceptAvatar(eid):
        avatar = BigWorld.entities.get(eid, None)
        if avatar:
            methodMap = getAvatarMethod()
            MethodIncepter(avatar, methodMap).decorate()
            MethodIncepter(avatar.modelServer, {}).decorate(False)
            MethodIncepter(avatar.skillPlayer, {}).decorate(False)
            print '-----', eid, 'incepted'


    def inceptAllAvatars():
        ent = BigWorld.entities.items()
        methodMap = getAvatarMethod()
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                MethodIncepter(e, methodMap).decorate()
                MethodIncepter(e.modelServer, {}).decorate(False)
                MethodIncepter(e.skillPlayer, {}).decorate(False)
                print '-----', id, 'incepted'


    def inceptMonster(mid):
        monster = BigWorld.entities.get(mid, None)
        if monster:
            methodMap = getMonsterMethod()
            MethodIncepter(monster, methodMap).decorate()
            MethodIncepter(BigWorld.player().skillPlayer, {}).decorate(False)
            print '-----', mid, 'incepted'


    def inceptAllMonster():
        ent = BigWorld.entities.items()
        methodMap = getMonsterMethod()
        for id, e in ent:
            if e.__class__.__name__ == 'Monster':
                MethodIncepter(e, methodMap).decorate()


    inceptPlayer()
if BigWorld.component in ('base', 'cell'):
    focusMethod = {'startQinggongAction': [],
     'startQinggongState': [],
     '_qe_enterZaiju': [],
     'switchWeaponState': [],
     'enterZaiju': [],
     '_isOnZaijuOrBianyao': [],
     '_checkZaijuPrecondition': [],
     '_inWingFly': [],
     'inFuben': [],
     '_pin': [],
     '_unpin': [],
     'enterRide': [],
     '_cancel_WEAPON_IN_HAND_ST': [],
     '_realEnterRide': [],
     'checkStatus_cancel': [],
     '_AvatarOnTimer_TIMER_RUSH_END_DOWN_WEAPON_IN_HAND': [],
     'selfInjure': [],
     'otherDamage': [],
     'qinggongData': [],
     'getQingGongData': [],
     'qingGongSkillLevelUp': [],
     'isQingGongSkillLearned': [],
     '_checkQingGongSkillUpdateCommon': [],
     'reduceQingGongSkillUpdateCost': []}
    from iCell import ICell
    from impl.impQuest import ImpQuest
    from impl.impQuestLoop import ImpQuestLoop
    from impl.impCombat import ImpCombat
    from impl.impMotion import ImpMotion
    from impl.impGeneral import ImpGeneral
    from impl.impTimer import ImpTimer
    from impl.impCheck import ImpCheck
    from impl.impChat import ImpChat
    from impl.impFuben import ImpFuben
    from impl.impTeam import ImpTeam
    from impl.impItem import ImpItem
    from impl.impGroup import ImpGroup
    from impl.impTrade import ImpTrade
    from impl.impEngine import ImpEngine
    from impl.impPick import ImpPick
    from impl.impAdmin import ImpAdmin
    from impl.impTroop import ImpTroop
    from impl.impBeast import ImpBeast
    from impl.impBattleField import ImpBattleField
    from impl.impShengSiChang import ImpShengSiChang
    from impl.impGlobal import ImpGlobal
    from impl.impQinggong import ImpQinggong
    from impl.impAction import ImpAction
    from impl.impTest import ImpTest
    from impl.impShop import ImpShop
    from impl.impProperty import ImpProperty
    from impl.impArena import ImpArena
    from impl.impTop import ImpTop
    from impl.impCombatRecord import ImpCombatRecord
    from impl.impSwim import ImpSwim
    from impl.impRide import ImpRide
    from impl.impInv import ImpInv
    from impl.impBianshen import ImpBianshen
    from impl.impMaterialBag import ImpMaterialBag
    from impl.impSpriteMaterialBag import ImpSpriteMaterialBag
    from impl.impFashionBag import ImpFashionBag
    from impl.impCart import ImpCart
    from impl.impAchievement import ImpAchievement
    from impl.impWingFly import ImpWingFly
    from impl.impActivities import ImpActivities
    from impl.impStats import ImpStats
    from impl.impPk import ImpPk
    from impl.impFishing import ImpFishing
    from impl.impTempBag import ImpTempBag
    from impl.impMultiLine import ImpMultiLine
    from impl.impQieCuo import ImpQieCuo
    from impl.impFriend import ImpFriend
    from impl.impStorage import ImpStorage
    from impl.impBooth import ImpBooth
    from impl.impRune import ImpRune
    from impl.impJiGuan import ImpJiGuan
    from impl.impWushuang import ImpWushuang
    from impl.impDaZuo import ImpDaZuo
    from impl.impMail import ImpMail
    from impl.impClimb import ImpClimb
    from impl.impDelegate import ImpDelegate
    from impl.impReport import ImpReport
    from impl.impQte import ImpQte
    from impl.impEmote import ImpEmote
    from impl.impConsign import ImpConsign
    from impl.impGuild import ImpGuild
    from impl.impExplore import ImpExplore
    from impl.impSight import ImpSight
    from iSession import ISession
    from iCombatUnit import ICombatUnit
    from iAbstractCombatUnit import IAbstractCombatUnit
    from iCamp import ICamp
    from iDisplay import IDisplay
    from iTimer import ITimer
    import Monster
    from iAICombatUnit import IAICombatUnit
    from iCell import ICell
    from iRoute import IRoute
    from iDistributeAI import IDistributeAI
    from iScriptAction import IScriptAction
    from iWorldEvent import IWorldEvent
    from iMonsterCommon import IMonsterCommon
    from iPlaceable import IPlaceable
    from iRelive import IRelive
    from iCombatUnit import ICombatUnit

    def getAvatarCellMethod():
        methodMap = {}
        modules = (ISession,
         ImpQuest,
         ImpQuestLoop,
         ImpMotion,
         ImpCombat,
         ImpGeneral,
         ImpTimer,
         ImpCheck,
         ImpChat,
         ImpTeam,
         ImpFuben,
         ImpItem,
         ImpGroup,
         ImpTrade,
         ImpEngine,
         ImpPick,
         ImpMaterialBag,
         ImpSpriteMaterialBag,
         ImpFashionBag,
         ImpAdmin,
         ImpTroop,
         ImpBeast,
         ImpBattleField,
         ImpShengSiChang,
         ImpGlobal,
         ImpAction,
         ImpQinggong,
         ImpCart,
         ImpAchievement,
         ImpReport,
         ImpTest,
         ImpShop,
         ImpProperty,
         ImpArena,
         ImpTop,
         ImpCombatRecord,
         ImpSwim,
         ImpRide,
         ImpInv,
         ImpBianshen,
         ImpAchievement,
         ImpWingFly,
         ImpPk,
         ImpActivities,
         ImpStats,
         ImpFishing,
         ImpTempBag,
         ImpMultiLine,
         ImpQieCuo,
         ImpFriend,
         ImpStorage,
         ImpBooth,
         ImpRune,
         ImpJiGuan,
         ImpWushuang,
         ImpDaZuo,
         ImpMail,
         ImpClimb,
         ImpQte,
         ImpDelegate,
         ImpEmote,
         ImpConsign,
         ImpGuild,
         ImpExplore,
         ImpSight,
         ICombatUnit,
         IAbstractCombatUnit,
         ICamp,
         IDisplay,
         ITimer)
        for module in modules:
            for name, fun in inspect.getmembers(module, inspect.ismethod):
                methodMap[name] = name

        return methodMap


    def getMonsterMethod():
        methodMap = {}
        modules = (Monster,
         IAICombatUnit,
         ICell,
         IRoute,
         IDistributeAI,
         IScriptAction,
         IWorldEvent,
         IMonsterCommon,
         IPlaceable,
         IRelive,
         ICombatUnit)
        for module in modules:
            for name, fun in inspect.getmembers(module, inspect.ismethod):
                methodMap[name] = name

        return methodMap


    def inceptPlayer(playerId):
        avatar = BigWorld.entities.get(playerId, None)
        if avatar:
            methodMap = getAvatarCellMethod()
            MethodIncepter(avatar, methodMap).decorate()
            print '------playerId:', playerId, 'incepted'


    def inceptMonster(mid):
        monster = BigWorld.entities.get(mid, None)
        if monster:
            methodMap = getMonsterMethod()
            MethodIncepter(monster, methodMap).decorate()
            print '-----', mid, 'incepted'
