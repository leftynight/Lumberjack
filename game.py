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
        self.image, self.rect = _load_image(imgpath, 105, 400)#locals.HEIGHT)
        #self.sound = pygame.mixer.Sound(join( ... ))

class treeBlock(Sprite):
    def __init__(self, x, y, inp):
        Sprite.__init__(self)
        self.type = inp
        if  self.type == 0:
            imgpath = join('games', 'Lumberjack', 'images', 'tree_right.png')
        elif self.type == 2:
            imgpath = join('games', 'Lumberjack', 'images', 'tree_left.png')
            x -= 157
        elif self.type == 1:
            imgpath = join('games', 'Lumberjack', 'images', 'tree_norm.png')
        self.image, self.rect = _load_image(imgpath, x, y)

    def update(self):
        self.rect = self.rect.move(0, 140)
        
##### MICROGAME CLASS ##########################################################
LEFT_POSITION = 325
# TODO: rename this class to your game's name...
class LumberjackGame(Microgame):
    def __init__(self):
        # TODO: Initialization code here
        Microgame.__init__(self)
        self.jack = Man()
        self.count = 0
        self.mycount = pygame.font.SysFont("arial", 50, bold = True)
        self.left, self.left_rect = _load_image(join("games","Lumberjack","images","timberman_normalleft.png"), 105, 400)
        self.left_chop, self.leftc_rect = _load_image(join("games","Lumberjack","images","timberman_chopleft.png"), 130, 450)
        self.right, self.right_rect = _load_image(join("games","Lumberjack","images","timberman_normalright.png"), 500, 400)
        self.right_chop, self.rightc_rect = _load_image(join("games","Lumberjack","images","timberman_chopright.png"), 375, 450)
        self.stump = load(join("games","Lumberjack","images","stump.png"))
        self.sprites = Group(self.jack)
        self.background = load(join("games","Lumberjack","images","forest.png"))
        self.tree = Group(treeBlock(LEFT_POSITION, 550, 1))
  
    def start(self):
        # TODO: Startup code here
        music.load(join("games","Lumberjack","music","tree_song.ogg"))
        music.play()
        self.generateTree()

    def stop(self):
        # TODO: Clean-up code here
        music.stop()

    def generateTree(self):
        _ , min_y = self.tree.sprites()[len(self.tree.sprites()) - 1].rect.topleft
        cur_tree = 0
        for n in range(0, (len(self.tree.sprites()) - 1)):
            _ , y = self.tree.sprites()[n].rect.topleft
            if y < min_y:
                min_y = y
                cur_tree = n
        if min_y > 0 and min_y <= 550:
            tree_type = self.tree.sprites()[cur_tree].type
            if tree_type == 2:
                self.tree.add(treeBlock(LEFT_POSITION, (min_y - 140), randint(1,2)))
            elif tree_type == 0:
                self.tree.add(treeBlock(LEFT_POSITION, (min_y - 140), randint(0,1))) 
            else:
                self.tree.add(treeBlock(LEFT_POSITION, (min_y - 140), randint(0,2)))

    def updateTree(self, side):
        max_y = locals.HEIGHT
        cur_tree = 0
        for n in range(0, (len(self.tree.sprites()))):
            _ , y = self.tree.sprites()[n].rect.topleft
            if 550 == y:
                max_y = y
                cur_tree = n
        print max_y, self.tree.sprites()[cur_tree].type 
        if self.tree.sprites()[cur_tree].type == side:
            self.lose()
        else:
            self.tree.remove(self.tree.sprites()[cur_tree])
            #self.tree.update()
            for each in self.tree:
                each.update()

    def update(self, events):
        # TODO: Update code here
        self.sprites.update()
        self.generateTree()

        #Process user input
        sound_chop = pygame.mixer.Sound(join("games","Lumberjack","music","axe_chop.wav"))
        if self.jack.image == self.left_chop:
            self.jack.image = self.left
            self.jack.rect = self.left_rect
        elif self.jack.image == self.right_chop:
            self.jack.image = self.right
            self.jack.rect = self.right_rect
        for event in events:
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.count += 1
                sound_chop.play()
                self.jack.image = self.left_chop
                self.jack.rect = self.leftc_rect
                self.updateTree(2)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.count += 1
                sound_chop.play()
                self.jack.image = self.right_chop
                self.jack.rect = self.rightc_rect
                self.updateTree(0)

    def render(self, surface):
        # TODO: Rendering code here
        surface.fill(Color(255, 255, 255))
        surface.blit(self.background, (0, 0), area = None, special_flags = 0)
        self.tree.draw(surface)
        surface.blit(self.stump, (318, 690), area = None, special_flags = 0)
        self.sprites.draw(surface)
        label = self.mycount.render(str(self.count), 1, (255, 255, 255))
        if self.count <= 9:
            surface.blit(label, (398, 200))
        else:
            surface.blit(label, (385, 200))

    def get_timelimit(self):
        # TODO: Return the time limit of this game (in seconds, 0 <= s <= 15)
        #raise NotImplementedError("get_timelimit")
        return 15
