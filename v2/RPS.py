from base import *
import random
import enum
from standard_language import *
import training_loops

class hand(enum.Enum):
    SCISSORS = 0
    ROCK     = 1
    PAPER    = 2

class Player(Agent):
    def __init__(self):
        self.choice = -1 # Not set
    def update(self, choice):
        self.choice = choice

class RPS(World):
    def __init__(self, element_list, params = [1,[hand.SCISSORS, hand.ROCK, hand.PAPER]]):
        World.__init__(self, element_list, params)
        self.player = self.elements[0]
        self.num = self.params[0] + 1 # Counting one free victory
        self.initNum =  self.num
        self.choices = self.params[1]
        self.select = -1

    def run(self):
        print("Num remaining: " + str(self.num))
        if self.num == 0:
            print("Victory achieved")
            return 1
        else:
            if self.select == -1:
                self.num -= 1 # Hasn't been set yet, so free victory
            elif (self.select + 1) % len(self.choices) == self.choices.index(self.player.choice):
                print("Correct Guess: " + self.player.choice.name)
                self.num -= 1
            else:
                print("Wrong Guess: " + self.player.choice.name)
            self.select = random.choice(range(len(self.choices)))
            print(self.choices[self.select].name + " selected")
            return(0)
    def obs(self, a):
        return([self.select,])

    def reset(self):
        self.num = self.initNum

def rps_constructor(rounds):
    p = Player()
    lang = Standard_Language(1, [hand.SCISSORS, hand.ROCK, hand.PAPER],
    ["ENEMY_CHOICE",], ["SET_SCISSORS","SET_ROCK","SET_PAPER"])
    c = Standard_Language_Controller(p, lang, stopping = 0.5, uncert = 0)
    enemy = RPS([p,], [rounds, [hand.SCISSORS, hand.ROCK, hand.PAPER]])
    return(c, enemy)


def main():
    #basic_training_loop(10, 500, master_grid_constructor)
    rounds = 5
    training_loops.probabilistic_training_loop(rounds+2, 13000, 5, lambda : rps_constructor(rounds))

if __name__ == "__main__":
    main()
