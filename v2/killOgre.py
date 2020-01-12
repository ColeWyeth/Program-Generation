from base import *
import random
import enum
from standard_language import *
import training_loops
import sys, pygame

class Action(enum.Enum):
    RIGHT = 0
    LEFT  = 1
    SWORD = 2
    REST  = 3

class Monster(Element):
    def __init__(self, x, imageName, name = "None"):
        self.x = x
        self.xInit = x
        self.imageName = imageName
        self.name = name
        self.range = range
        self.dead = False

    def getRange(self):
        pass

    def reset(self):
        self.x = self.xInit

class Ogre(Monster):
    num = 0
    def __init__(self, x):
        name = "Ogre " + str(Ogre.num)
        Ogre.num += 1
        Monster.__init__(self, x, "Ogre.jpg", name)
        self.health = 1

    def getRange(self):
        return(50)

    def reset(self):
        Monster.reset(self)
        self.health = 1
        self.dead = False

class Hero(Agent):
    def __init__(self, x, imageName, name = "Hero"):
        self.x = x
        self.xInit = x
        self.imageName = imageName
        self.name = name
        self.health = 1
        self.dead = False
        self.action = Action.LEFT

    def getRange(self):
        return(100)

    def reset(self):
        self.x = self.xInit
        self.health = 1
        self.dead = False
        self.action = Action.LEFT

    def update(self, action):
        self.action = action

class Adventure(World):
    def __init__(self, element_list, params):
        World.__init__(self, element_list, params)
        self.animate = self.params[0] # Typically not during training
        self.w, self.h    = self.params[1] # of window

        if self.animate:
            self.rects = []
            self.images = []
            pygame.init()
            self.black = 0, 0, 0
            self.screen = pygame.display.set_mode((self.w, self.h))
            for e in self.elements:
                image = pygame.image.load(e.imageName)
                we, he = image.get_size()
                image = pygame.transform.smoothscale(image, (self.w//5, self.h//5 ))
                imageRect = image.get_rect()
                self.rects += [imageRect,]
                self.images += [image,]


    def run(self, manageQuit = True):
        allDead = True
        for e in self.elements:
            if e.dead:
                continue
            if isinstance(e, Hero):
                if e.action == Action.RIGHT and e.x < self.w - 10:
                    e.x += 3
                elif e.action == Action.LEFT and e.x > 10:
                    e.x -= 3
                elif e.action == Action.SWORD:
                    # Heroes attack monsters
                    for m in self.elements:
                        if isinstance(m, Monster):
                            if abs(m.x - e.x) < e.getRange():
                                m.health -= 1



            if isinstance(e, Monster):
                if e.dead == False:
                    allDead = False

                # e.x -= 1 # If we want monsters to charge
                # Monsters attack heroes
                for h in self.elements:
                    if isinstance(h, Hero):
                        if abs(e.x - h.x) < e.getRange():
                            h.health -= 1
            # Stuff dies
            if e.health < 1:
                e.dead = True

        if self.animate:
            self.screen.fill(self.black)
            if manageQuit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()

            for i in range(len(self.elements)):
                self.rects[i].left = self.elements[i].x # Set position properly
                if self.elements[i].dead == False:
                    self.screen.blit(self.images[i], self.rects[i])

            pygame.display.flip()
            pygame.time.wait(5)


        if allDead:
            return(1)

    def obs(self, A):
        min = self.w
        for e in self.elements:
            if (e.x-A.x) < min and e.x -A.x > 0:
                min = e.x - A.x

        return([A.getRange(), min])

class User(Controller):
    def command(self):
        s = input("Command (R, L, S, or X to quit): ")
        c = Action.RIGHT
        if "L" == s:
            c = Action.LEFT
        elif "S" == s:
            c = Action.SWORD
        elif "X" == s:
            return(1)

        self.agent.update(c)

class UserKeyboard(Controller):
    def command(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.agent.action = Action.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.agent.action = Action.LEFT
                elif event.key == pygame.K_UP:
                    self.agent.action = Action.SWORD

            if event.type == pygame.KEYUP:
                self.agent.action = Action.REST
            pygame.time.wait(10)
            if event.type == pygame.QUIT: sys.exit()

def adventureConstructor():
    h  = Hero(0, "tanith.jpg", "Tanith Low")
    o  = Ogre(250)
    aw = Adventure([h,o], [False, (300, 300)])
    lang = Terminating_Standard_Language(2, [Action.LEFT, Action.RIGHT, Action.SWORD, Action.REST],
    ["RANGE", "NEXT_ENEMY"], ["SET_LEFT", "SET_RIGHT", "SET_SWORD", "SET_REST"])
    c  = Terminating_Standard_Language_Controller(h, lang, stopping = 0.1, increase = 1, uncert = 0.25)
    return(c,aw)
def main():
    # lang = Terminating_Standard_Language(2, [Action.LEFT, Action.RIGHT, Action.SWORD, Action.REST],
    # ["RANGE", "NEXT_ENEMY"], ["SET_LEFT", "SET_RIGHT", "SET_SWORD", "SET_REST"])
    # lang.print_commands(lang.generate(0.001, 1, 0))

    training_loops.modular_learning_strategy(150, 50, 3, adventureConstructor, 100)

    # h  = Hero(0, "tanith.jpg", "Tanith Low")
    # o  = Ogre(256)
    # aw = Adventure([h,o], [True, (500, 500)])
    # c = UserKeyboard(h)
    # while 1:
    #     c.command()
    #     if aw.run(False) == 1:
    #         print("Victory!")
    #         break
    #     if c.command() == 1:
    #         break

if __name__ == "__main__":
    main()
