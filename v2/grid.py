from base import *
import enum
import random
from standard_language import *
import training_loops

class Dir(enum.Enum):
    REST = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Ball(Element):
    num = 0
    def __init__(self, pos):
        self.posInit = pos
        self.pos = pos
        Ball.num += 1
        self.num = Ball.num
    def name(self):
        return("Ball " + str(self.num))

    def copy(self):
        return(Ball(self.pos))

    def reset(self):
        self.pos = self.posInit

class Roller(Ball):
    def __init__(self, pos):
        Ball.__init__(self, pos)
        self.dir = Dir.REST

    def update(self, newDir):
        self.dir = newDir

    def copy(self):
        copiedRoller = Roller(self.pos)
        copiedRoller.dir = self.dir
        return(copiedRoller)

    def reset(self):
        Ball.reset(self)
        self.dir = Dir.REST

class grid(World):
    def __init__(self, element_list, params):
        World.__init__(self, element_list, params)
        self.size = params[0]
        self.goal = params[1]

    def roll(self, r):
        if(r.dir == Dir.UP and r.pos[1] < self.size-1):
            r.pos = (r.pos[0], r.pos[1]+1)
        elif(r.dir == Dir.RIGHT and r.pos[0] < self.size-1):
            r.pos = (r.pos[0]+1, r.pos[1])
        elif(r.dir == Dir.DOWN and r.pos[1] > 0):
            r.pos = (r.pos[0], r.pos[1]-1)
        elif (r.dir == Dir.LEFT and r.pos[0] > 0):
            r.pos = (r.pos[0]-1, r.pos[1])

    def run(self):
        for e in self.elements:
            if isinstance(e, Roller):
                self.roll(e)

        for e in self.elements:
            print(e.name() + " : " + str(e.pos[0]) + " , " + str(e.pos[1])  )
            if e.pos[0] == self.goal[0] and e.pos[1] == self.goal[1]:
                print("Objective reached by " + e.name())
                return(1)
        print("Step Complete")
        return(0)

    def printState(self):
        for y in range(self.size):
            print(self.size*"___")
            line = ""
            for x in range(self.size):
                occupied = "  "
                if self.goal[0] == x and self.goal[1] == y:
                    occupied = "G "
                else:
                    for e in self.elements:
                        if e.pos[0] == x and e.pos[1] == y:
                            occupied = "O "
                line += "|" + occupied
            print(line + "|")
        print(self.size*"___")

    def obs(self, R):
        return([R.pos[0], R.pos[1], self.goal[0], self.goal[1]])

    def copy(self):
        copied_elements = [e.copy() for e in self.elements]
        return(grid(copied_elements, self.params))

def grid_constructor():
    R = Roller((0,0))
    w = grid([R], [5, (4,4)])
    c = Standard_Language_Controller(R, Standard_Language(4, [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT],
    ["CURR_X", "CURR_Y", "GOAL_X","GOAL_Y"], ["SET_UP", "SET_RIGHT", "SET_DOWN", "SET_LEFT"]),
    stopping = 0.5, uncert = 0)
    return(c,w)

def terminating_grid_constructor():
    R = Roller((0,0))
    w = grid([R], [5, (4,4)])
    c = Terminating_Standard_Language_Controller(R, Terminating_Standard_Language(4, [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT],
    ["CURR_X", "CURR_Y", "GOAL_X","GOAL_Y"], ["SET_UP", "SET_RIGHT", "SET_DOWN", "SET_LEFT"]),
    stopping = 0.1, increase =1, uncert = 0.25)
    return(c,w)

def main():
    #basic_training_loop(10, 500, master_grid_constructor)
    #training_loops.probabilistic_training_loop(9, 1500, 3, grid_constructor)
    training_loops.modular_learning_strategy(9, 1500, 3, terminating_grid_constructor, 10)
if __name__ == "__main__":
    main()
