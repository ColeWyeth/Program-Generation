from world import *
import enum
import random

# Next step is to add another layer of abstraction to controllers
# So that they actually have a language out of which to build strategies
# And they must also receive input from the outside world
# For instance, they could actually receive the objective (x, y)
# and learn the algorith right x times, up y times
# So worlds could vary between runs 
class Dir(enum.Enum):
    REST = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Ball(Element):
    num = 0
    def __init__(self, pos):
        self.pos = pos
        Ball.num += 1
        self.num = Ball.num
    def name(self):
        return("Ball " + str(self.num))

class Roller(Ball):
    def __init__(self, pos):
        Ball.__init__(self, pos)
        self.dir = Dir.REST

    def update(self, newDir):
        self.dir = newDir

    def run(self):
        if(self.dir == Dir.UP):
            self.pos = (self.pos[0], self.pos[1]+1)
        elif(self.dir == Dir.RIGHT):
            self.pos = (self.pos[0]+1, self.pos[1])
        elif(self.dir == Dir.DOWN):
            self.pos = (self.pos[0], self.pos[1]-1)
        elif self.dir == Dir.LEFT:
            self.pos = (self.pos[0]-1, self.pos[1])

class ControlScheme(Controller):
    def __init__(self, agent_list, dirList):
        Controller.__init__(self, agent_list)
        self.commands = dirList
        self.next = 0

    def command(self):
        curr = self.commands[self.next]
        self.next += 1
        for a in self.agents:
            a.update(curr)

class RandomControl(Controller):
    def command(self):
        curr = random.choice([Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT])
        for a in self.agents: # First clear lesson:
            a.update(curr)    # This can be part of the abstract type

class grid(World):
    def __init__(self, element_list, params):
        World.__init__(self, element_list, params)
        self.size = params[0]
        self.goal = params[1]
    def run(self):
        for e in self.elements:
            e.run()
            # All these tedious checks could be eliminated
            # (or made cleaner; these should only be checked
            # during moves)
            # if world itself ran updates on elements
            # probably the elements would need to pass some
            # information to world, particularly agents
            if e.pos[0] < 0:
                e.pos = (0, e.pos[1])
            if e.pos[0] >= self.size:
                e.pos = (self.size-1, e.pos[1])
            if e.pos[1] < 0:
                e.pos = (e.pos[0], 0)
            if e.pos[1] >= self.size:
                e.pos = (e.pos[0], self.size-1)

        for e in self.elements:
            print(e.name() + " : " + str(e.pos[0]) + " , " + str(e.pos[1])  )
            if e.pos[0] == self.goal[0] and e.pos[1] == self.goal[1]:
                print("Objective reached by " + e.name())
                return(1)
        print("Step Complete")
        return(0)

def main():
    generations = 5
    members = 400
    steps = 10
    DNA = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT]
    for g in range(generations):
        best = [Dir.UP for i in range(steps)]
        bestT = steps + 1
        for epoch in range(members):
            R = Roller((0,0))
            #R2 = Roller((0,0))
            grid1 = grid([Ball((1,1)), Ball((0,1)), R], [5, (4,3)])

            strat = [random.choice(DNA) for i in range(steps)]
            C1 = ControlScheme([R], strat)
            #C2 = RandomControl([R2])
            t = 0
            for i in range(steps):
                print("Time: " + str(t))
                if grid1.run() == 1:
                    if(t < bestT):
                        best = strat
                        bestT = t
                    break
                C1.command()
                #C2.command()
                t += 1
        DNA = best

    # And we have a kind of learning!!!
    c = 0
    for d in best:
        c += 1
        print(str(c) + ": "+ str(d))
    print("Best time: " + str(bestT))

if __name__ == "__main__":
    main()
