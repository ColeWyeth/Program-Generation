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
    return(best, bestT)

def seed_loop(steps, agents, c, w, seed_alg):
    bestT = steps + 1
    best = c.lang.generate()
    for agent in range(agents):
        w.reset()
        c.alg = c.lang.fill_stochastic(c.alg)
        t = 0
        for i in range(steps):
            print("Time: " + str(t))
            if w.run() == 1:
                if(t < bestT):
                    bestT = t
                    best = c.alg
                break
            c.update(w.obs(c.agent))
            c.command()
            #C2.command()
            t += 1
    return(best, bestT)


def modular_learning_strategy(steps, agents, tests, constructor, modifications):
    """ Guesses randomized algorithms until one of them is sometimes successful.
        Attempts to fill_stochastic this algorithm until it succeeds deterministically
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

        if totalScore > bestScore or (totalScore == bestScore and t < bestT) :
            print("CANDIDATE SOLUTION FOUND")
            new, newT = seed_loop(steps, modifications, c, w, c.alg)
            bestScore = totalScore # Setting zero or perfect too misleading
            if newT < steps + 1: # Updates only made if correct deterministic alg found
                best = new
                bestT = newT

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
    return(best, bestT)
