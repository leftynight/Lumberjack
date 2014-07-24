# Pygame imports
import pygame, pygame.mixer
from pygame import Surface
from pygame.image import load
from pygame.locals import *
from pygame.mixer import music
from pygame.rect import Rect
from pygame.sprite import Group, Sprite

# Path imports
from os.path import join

# Random imports
from random import randint, choice

# Microgame-specific imports
import locals
from microgame import Microgame

##### LOADER-REQUIRED FUNCTIONS ################################################

def make_game():
    # TODO: Return a new instance of your Microgame class.
    #raise NotImplementedError("make_game")
    return LumberjackGame()

def title():
    # TODO: Return the title of the game.
    #raise NotImplementedError("title")
    return "Lumberjack"

def thumbnail():
    # TODO: Return a (relative path) to the thumbnail image file for your game.
    #raise NotImplementedError("thumbnail")
    return join('games','Lumberjack',"images",'thumbnail.png')

def hint():
    # TODO: Return the hint string for your game.
    #raise NotImplementedError("hint")
    return "Chop down the tree!"

################################################################################

def _load_image(name, x, y):
    '''
    Loads an image file, returning the surface and rectangle corresponding to
    that image at the given location.
    '''
    try:
        image = load(name)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, msg:
        print 'Cannot load image: {}'.format(name)
        raise SystemExit, msg
    rect = image.get_rect().move(x, y)
    return image, rect

##### MODEL CLASSES ############################################################

# TODO: put your Sprite classes here
class Man(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        postion = 0 #0 = left, 1 = right
        imgpath = join('games', 'Lumberjack',"images", "timberman_normalleft.png")
        self.image, self.rect = _load_image(imgpath, 150, 400)#locals.HEIGHT)
        #self.sound = pygame.mixer.Sound(join( ... ))

# class treeBlock(Sprite):
#     def __init__(self, x, y, type):
#         Sprite.__init__(self)
#         if  self.type == 0:
#             imgpath = join('games', 'Lumberjack', 'tree_right.png')

#         elif self.type == 1:
#             imgpath = join('games', 'Lumberjack', 'tree_left.png')
#             x -= 75
#         else:
#             imgpath = join('games', 'Lumberjack', 'tree_center.png')

#         self.image, self.rect = _load_image(imgpath, x, y)

#     #def update(self, event):
#         #self.sound.play()
        
# class tree(Sprite):
#     def __init(self):
#         Sprite.__init__(self)
#         createTree(100, locals.HEIGHT)

#     def createTree(x,y):
#         self.Tree = []
#         x, y = tree.rect.topleft
#         while y > 0:
#             self.agrigate.add(treeBlock(x-75, y), randint(0,4))


##### MICROGAME CLASS ##########################################################

# TODO: rename this class to your game's name...
class LumberjackGame(Microgame):
    def __init__(self):
        # TODO: Initialization code here
        Microgame.__init__(self)
        self.jack = Man()
        self.left, _ = _load_image(join("games","Lumberjack","images","timberman_normalleft.png"), 150, 400)
        self.left_chop, _ = _load_image(join("games","Lumberjack","images","timberman_chopleft.png"), 150, 400)
        self.right, _ = _load_image(join("games","Lumberjack","images","timberman_normalright.png"), 150, 400)
        self.right_chop, _ = _load_image(join("games","Lumberjack","images","timberman_chopright.png"), 150, 400)
        #self.tree = tree()
        self.sprites = Group(self.jack)
        self.background = load(join("games","Lumberjack","images","forest.png"))
        
    def start(self):
        # TODO: Startup code here
        music.load(join("games","Lumberjack","music","tree_song.ogg"))
        music.play()

    def stop(self):
        # TODO: Clean-up code here
        music.stop()

    def update(self, events):
        # TODO: Update code here
        self.sprites.update()

        #Process user input
        sound_chop = pygame.mixer.Sound(join("games","Lumberjack","music","axe_chop.wav"))
        for event in events:
            if event.type == KEYDOWN and event.key == K_LEFT:
                sound_chop.play()
                self.jack.image = self.left_chop
                self.jack.rect = (150, 450)
            elif event.type == KEYUP and event.key == K_LEFT:
                self.jack.image = self.left
                self.jack.rect = (150, 400)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                sound_chop.play()
                self.jack.image = self.right_chop
                self.jack.rect = (400, 450)
            elif event.type == KEYUP and event.key == K_RIGHT:
                self.jack.image = self.right
                self.jack.rect = (500, 400)

    def render(self, surface):
        # TODO: Rendering code here
        surface.fill(Color(255, 255, 255))
        surface.blit(self.background, (0, 0), area = None, special_flags = 0)
        self.sprites.draw(surface)

    def get_timelimit(self):
        # TODO: Return the time limit of this game (in seconds, 0 <= s <= 15)
        #raise NotImplementedError("get_timelimit")
        return 15
