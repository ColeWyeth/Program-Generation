from world import *
from grid import *
from language import *
from master_language import *

def basic_training_loop(steps, agents, constructor):
    """ Constructor must return controller, world
        The controller must be an algorithm generator
        The world must have an obs function over agents
    """
    bestT = steps + 1
    c, w = constructor() # for a random starting algorithm
    best = c.lang

    for agent in range(agents):
        c, w = constructor()

        t = 0
        for i in range(steps):
            print("Time: " + str(t))
            if w.run() == 1:
                if(t < bestT):
                    best = c.alg
                    bestT = t
                break
            c.update(w.obs(c.agent))
            c.command()
            #C2.command()
            t += 1

    helper_lang = c.lang
    print("Best time: " + str(bestT))
    print()
    print("Best algorithm: ")
    print()
    helper_lang.print_commands(best)

def probabilistic_training_loop(steps, agents, tests, constructor):
    """ Constructor must return controller, world
        The controller must be an algorithm generator
        The world must have an obs function over agents
    """
    bestT = steps + 1
    c, w = constructor() # for a random starting algorithm
    best = c.lang.generate()
    bestScore = 0

    for agent in range(agents):
        c, w = constructor()

        totalScore = 0
        for test in range(tests):
            c.agent.pos = (0,0)
            c.agent.dir = Dir.REST
            score = 0
            t = 0
            for i in range(steps):
                print("Time: " + str(t))
                if w.run() == 1:
                    if(t < bestT):
                        bestT = t
                    score += 1 # arbitrary reward
                    break
                c.update(w.obs(c.agent))
                c.command()
                #C2.command()
                t += 1

            totalScore += score

        if totalScore > bestScore:
            bestScore = totalScore
            best = c.alg

    if bestT == steps + 1:
        print("No Solution Found!")
        return()
    helper_lang = c.lang
    print("Best time: " + str(bestT))
    print()
    print("Best score: " + str(bestScore) + "\n")
    print("Best algorithm: ")
    print()
    helper_lang.print_commands(best)

def master_grid_constructor():
    R = Roller((0,0))
    w = grid([R], [5, (4,4)])
    c = Master_Language_Control(R, Master_Language(4, [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT],
    ["CURR_X", "CURR_Y", "GOAL_X","GOAL_Y"], ["SET_UP", "SET_RIGHT", "SET_DOWN", "SET_LEFT"]), uncert = 0)
    return(c,w)

def main():
    #basic_training_loop(10, 500, master_grid_constructor)
    probabilistic_training_loop(9, 500, 8, master_grid_constructor)

if __name__ == "__main__":
    main()
