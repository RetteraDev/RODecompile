#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerDebug.o
from gamestrings import gameStrings
import BigWorld
import ResMgr
import Math
import keys
import const
import gameglobal
import gamelog
import clientcom
from sfx import sfx
from guis import topLogo
from fbStatistics import FubenStats

class ImpPlayerDebug(object):

    def adminOnClient(self, command):
        keyword = command.strip(' ').split()[0]
        args = command.strip(' ').split()[1:]
        keyword = keyword[1:].lower()
        gamelog.debug('adminOnClient:', repr(keyword), repr(args), len(args))
        if keyword == 'speed' and len(args) == 1 and gameglobal.rds.isSinglePlayer:
            self.ap.runFwdSpeed = float(args[0])
            return True
        elif keyword == 'fpslimit' and len(args) == 1:
            BigWorld.limitForegroundFPS(int(args[0]))
            return True
        elif keyword == 'bosshate':
            stats = gameglobal.rds.ui.fubenStat.fbStatDict.get(self.gbId, FubenStats())
            self.chatToGm('{}'.format(stats.getStats(FubenStats.K_BOSS_HATE)))
            return True
        elif keyword == 'npcvisible':
            gameglobal.GM_NPC_VISIBLE_ALL = int(args[0])
            gameglobal.GM_NPC_VISIBLE_TAG = {}
            self.hideNpcNearby(False)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_39, '')
            return True
        elif keyword == 'npcvisibletag':
            tag = args[0]
            value = int(args[1])
            if tag == 'null':
                tag = ''
            if value > 0:
                value = 1
            elif value < 0:
                value = -1
            gameglobal.GM_NPC_VISIBLE_TAG[tag] = value
            self.hideNpcNearby(False)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_39, '')
            return True
        else:
            if keyword == 'testuimem':
                try:
                    if hasattr(gameglobal.rds.ui, args[0]):
                        module = getattr(gameglobal.rds.ui, args[0])
                        module.runTestCase('testUIMem', [args[1:]])
                    else:
                        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_62, '')
                except:
                    gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_64, '')

            else:
                if keyword == 'showtoplogo':
                    gameglobal.rds.showDebugTopLogo = True
                    ents = BigWorld.entities.values()
                    for ent in ents:
                        if getattr(ent, 'topLogo', None) == None:
                            ent.topLog = topLogo.TopLogo(ent.id)
                        if not ent.targetCaps:
                            ent.targetCaps = [keys.CAP_CAN_USE]

                    return True
                if keyword == 'npchighlight':
                    gameglobal.GM_NPC_HIGHLIGHT_ALL = int(args[0])
                    clientcom.highlightNpcNearby()
                    gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_78 % keyword, '')
                    return True
                if keyword == 'showtemplates':
                    school = int(args[0])
                    gameglobal.rds.ui.balanceArenaTemplate.show(school)
                    gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, gameStrings.TEXT_IMPPLAYERDEBUG_78 % keyword, '')
                    return True
            return False

    def reloadEffect(self):
        sfx.gEffectMgr.effectCache.reloadAll()
        ResMgr.purgeAll()

    def testSound(self):
        modelName = 'char/21001/21001.model'
        scale = 1.0
        scaleMatrix = Math.Matrix()
        scaleMatrix.setScale((scale, scale, scale))
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = self.matrix
        model = BigWorld.PyModelObstacle(modelName, mp, True)
        self.addModel(model)
        aniName = 'cut_tree'
        model.animation(aniName, 1.0, False)
