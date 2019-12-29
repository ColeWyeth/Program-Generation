from world import *
import enum
import random
from grid import *
from language import *

class Algorithm_Control_Scheme(Controller):
    def __init__(self, agent_list, lang):
        Controller.__init__(self, agent_list)
        self.alg = lang.generate()
        self.lang = lang

    def update(self, goal_x, goal_y, curr_x, curr_y):
        self.lang.update(goal_x, goal_y, curr_x, curr_y)

    def command(self):
        self.agents[0].dir = self.lang.execute(self.alg)


# A very basic kind of program learning is achieved 
def main():
    steps = 10
    agents = 100
    bestT = steps + 1
    best = (Sym.PASS,)
    size = 5

    for agent in range(agents):
        R = Roller((0,0))
        #R2 = Roller((0,0))
        grid1 = grid([R], [5, (4, 4)])

        lang = Basic_Grid()
        C1 = Algorithm_Control_Scheme([R], lang)
        lang.print_commands(C1.alg)

        #C2 = RandomControl([R2])
        t = 0
        for i in range(steps):
            print("Time: " + str(t))
            if grid1.run() == 1:
                if(t < bestT):
                    best = C1.alg
                    bestT = t
                break
            C1.update(grid1.goal[0], grid1.goal[1], R.pos[0], R.pos[1])
            C1.command()
            #C2.command()
            t += 1

    helper_lang = Basic_Grid()
    print("Best time: " + str(bestT))
    print()
    print("Best algorithm: ")
    print()
    helper_lang.print_commands(best)


if __name__ == "__main__":
    main()
