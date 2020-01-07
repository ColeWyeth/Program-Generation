# Generalized training loops

def probabilistic_training_loop(steps, agents, tests, constructor):
    """ Constructor must return a
        language controller and a world
    """
    bestT = steps + 1
    c, w = constructor() # for a random starting algorithm
    best = c.lang.generate()
    bestScore = 0

    for agent in range(agents):
        c, w = constructor()

        totalScore = 0
        for test in range(tests):
            w.reset()

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

        if totalScore > bestScore or (totalScore == bestScore and len(c.alg) < len(best)) :
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
