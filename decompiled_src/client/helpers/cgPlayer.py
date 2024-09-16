#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/cgPlayer.o
import BigWorld
import ResMgr
import GUI
import clientcom
from callbackHelper import Functor
gmPreloadedMovie = {}
gmPreloadedBinkMovie = {}

class CGPlayer(object):
    PREFIX_PATH = 'intro/movie/'

    def __init__(self):
        self.finalize()

    @staticmethod
    def getResourceId(cgName):
        return '%s%s.movie' % (CGPlayer.PREFIX_PATH, cgName)

    def finalize(self):
        self.cgName = None
        self.movie = None
        self.movieProvider = None
        self.callback = None
        self.isPlaying = False
        self.loadCallback = None

    def makeMovie(self, provider, config = {}):
        self.movieProvider = provider
        self.movie = self.getMovieScreen()
        self.movie.texture = self.movieProvider
        if not config.get('screenRelative', True):
            self.movie.widthRelative = False
            self.movie.heightRelative = False
        if config.get('verticalAnchor', None):
            self.movie.verticalAnchor = config['verticalAnchor']
        if config.get('horizontalAnchor', None):
            self.movie.horizontalAnchor = config['horizontalAnchor']
        self.movie.position = config['position']
        self.movie.width = config['w']
        self.movie.height = config['h']
        self.movie.materialFX = 'SOLID'

    def getMovieScreen(self):
        return GUI.Simple('movie')

    def getMovieProvider(self, cgName):
        global gmPreloadedMovie
        provider = None
        fullCgName = self.getResourceId(cgName)
        if cgName in gmPreloadedMovie:
            provider = gmPreloadedMovie[cgName]
        else:
            clientcom.resetLimitFps(False)
            BigWorld.loadingWorld(False)
            provider = BigWorld.PyMovie(fullCgName, False)
        return provider

    def setPosition(self, pos):
        if self.movie:
            self.movie.position = (pos[0], pos[1], 0)

    def setSize(self, size):
        if self.movie:
            self.movie.width, self.movie.height = size

    def playMovie(self, cgName, config = {}):
        position = config.get('position', None)
        if not position:
            return
        config['position'] = (position[0], position[1], 0)
        if self.movie:
            return
        self.cgName = cgName
        fullCgName = '%s%s.movie' % (CGPlayer.PREFIX_PATH, cgName)
        movieSection = ResMgr.openSection(fullCgName)
        if movieSection is None:
            callback = config.get('callback', None)
            if callback:
                callback()
            return
        provider = self.getMovieProvider(cgName)
        if config.get('loadCallback', None):
            self.loadCallback = config.get('loadCallback', None)
        self.doRealPlayMovie(config, provider)

    def doRealPlayMovie(self, config, provider):
        if not provider.loaded:
            BigWorld.callback(0.2, Functor(self.doRealPlayMovie, config, provider))
            return
        self.makeMovie(provider, config)
        self.callback = config.get('callback', None)
        if config.get('inBackOfUI', 0):
            GUI.addRoot(self.movie, 1)
        else:
            GUI.addRoot(self.movie, 2)
        self.movieProvider.loop(config.get('loop', False))
        self.movieProvider.play(True, self.endMovieCallback)
        self.isPlaying = True
        if self.loadCallback:
            self.loadCallback()

    def endMovie(self):
        BigWorld.worldDrawEnabled(True)
        if self.movie:
            GUI.delRoot(self.movie)
        if self.movieProvider:
            self.movieProvider.play(False)
        gmPreloadedMovie.pop(self.cgName, None)
        self.finalize()

    def endMovieCallback(self):
        callback = self.callback
        self.endMovie()
        if callback:
            callback()


class UIMoviePlayer(CGPlayer):

    def __init__(self, swfPath, insName, flashWidth, flashHeight):
        super(UIMoviePlayer, self).__init__()
        self.swfPath = swfPath
        self.insName = insName
        self.flashWidth = flashWidth
        self.flashHeight = flashHeight

    def getMovieScreen(self):
        return GUI.MovieAdaptor('movie')

    def doRealPlayMovie(self, config, provider):
        if not provider.loaded:
            BigWorld.callback(1, Functor(self.doRealPlayMovie, config, provider))
            return
        self.makeMovie(provider, config)
        self.callback = config.get('callback', None)
        self.movieProvider.loop(config.get('loop', False))
        self.movieProvider.play(True, self.endMovieCallback)
        self.movie.drawToFlash(self.swfPath, self.insName, self.flashWidth, self.flashHeight)
        self.isPlaying = True

    def endMovie(self):
        self.finalize()


class CGBinkPlayer(CGPlayer):
    PREFIX_PATH = 'intro/movie/'

    def __init__(self):
        super(CGBinkPlayer, self).__init__()

    @staticmethod
    def getResourceId(cgName):
        return '%s%s_b.bik' % (CGBinkPlayer.PREFIX_PATH, cgName)

    def getMovieProvider(self, cgName):
        global gmPreloadedBinkMovie
        provider = None
        fullCgName = self.getResourceId(cgName)
        if cgName in gmPreloadedBinkMovie:
            provider = gmPreloadedBinkMovie[cgName]
        else:
            clientcom.resetLimitFps(False)
            BigWorld.loadingWorld(False)
            provider = BigWorld.PyBinkMovie(fullCgName, False)
        return provider

    def playMovie(self, cgName, config = {}):
        position = config.get('position', None)
        if not position:
            return
        config['position'] = (position[0], position[1], 0)
        if self.movie:
            return
        self.cgName = cgName
        provider = self.getMovieProvider(cgName)
        if config.get('loadCallback', None):
            self.loadCallback = config.get('loadCallback', None)
        self.doRealPlayMovie(config, provider)

    def endMovie(self):
        super(CGBinkPlayer, self).endMovie()
        gmPreloadedBinkMovie.pop(self.cgName, None)


def preloadMovie(cgName):
    if cgName not in gmPreloadedMovie:
        fullCgName = CGPlayer.getResourceId(cgName)
        provider = BigWorld.PyMovie(fullCgName, True)
        gmPreloadedMovie[cgName] = provider


def preloadBinkMovie(cgName):
    if cgName not in gmPreloadedBinkMovie:
        fullCgName = CGBinkPlayer.getResourceId(cgName)
        provider = BigWorld.PyBinkMovie(fullCgName, False)
        gmPreloadedBinkMovie[cgName] = provider
