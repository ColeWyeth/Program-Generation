import enum
import random
from language import Language
from world import Controller

class Sym(enum.Enum):
    ONE             = 1
    OBS_POS         = 2
    RAND_INT        = 3
    RAND_BOOL       = 4
    SET_CHOICE      = 5
    PLUS            = 6
    NEG_ONE         = 7
    MULT            = 8
    IF_THEN_ELSE    = 9
    LESS            = 10
    EQUAL           = 11
    GREATER         = 12
    PASS            = 13
    AND             = 14
    OR              = 15
    NEG_BOOL        = 16
    REPEAT          = 17
    ZERO            = 18

class Master_Language(Language):
    def __init__(self, obs_num, choice_list, obs_names = [], set_names = []):
        self.obs_num = obs_num
        self.obs = [0 for i in range(obs_num)]
        self.obs_names = obs_names
        self.choice_list = choice_list
        self.set_names = set_names

        self.symbols = list(Sym)
        self.bool_int_comp = [Sym.LESS, Sym.EQUAL, Sym.GREATER]
        self.int_bin_op   = [Sym.PLUS, Sym.MULT]
        self.int_val  = [Sym.ONE, Sym.NEG_ONE, Sym.ZERO] + self.obs_num * [Sym.OBS_POS]
        self.bool_op   = [Sym.AND, Sym.OR]

        self.num  = [(Sym.OBS_POS, i) for i in range(obs_num)]
        self.exe  = [Sym.IF_THEN_ELSE, Sym.SET_CHOICE]
        self.choice = self.choice_list[0]

    def int_generate(self, term_prob = 0.75, uncert = 0.25):
        """ High term_prob makes termination more likely.
            High uncert includes more probabilistic behavior
        """

        term = (random.random() < term_prob) # Whether we will terminate recursion
        if term:
            guess = (random.random() < uncert) # Whether to act probabilistically
            if guess:
                s = Sym.RAND_INT
            else:
                s = random.choice(self.int_val)
            if s == Sym.OBS_POS: # In this case we must choose an observation channel
                return (s, random.choice(range(self.obs_num)))
            else:
                return (s,)
        else:
            s = random.choice(self.int_bin_op)
            return (s, self.int_generate(term_prob, uncert), self.int_generate(term_prob, uncert))

    def int_exp_to_str(self, int_exp):
        """ Pretty printing for integer expressions (returns string) """
        x = int_exp[0]
        if x in self.int_bin_op:
            comp = ""
            if x == Sym.PLUS:
                comp = " + "
            elif x == Sym.MULT:
                comp = " * "
            return("(" + self.int_exp_to_str(int_exp[1]) + comp + self.int_exp_to_str(int_exp[2]) + ")")

        elif x == Sym.OBS_POS:
            if len(self.obs_names) == self.obs_num:
                return(self.obs_names[int_exp[1]])
            else:
                return("Obs[" + str(int_exp[1]) + "]")

        elif x == Sym.ZERO:
            return("0")
        elif x == Sym.ONE:
            return("1")
        elif x == Sym.NEG_ONE:
            return("-1")
        elif x == Sym.RAND_INT:
            return("RAND_INT")

    def int_eval(self, int_exp):
        x = int_exp[0]
        if x in self.int_bin_op:
            if x == Sym.PLUS:
                return(self.int_eval(int_exp[1]) + self.int_eval(int_exp[2]))
            elif x == Sym.MULT:
                return(self.int_eval(int_exp[1]) * self.int_eval(int_exp[2]))

        elif x == Sym.OBS_POS:
            return(self.obs[int_exp[1]])

        elif x == Sym.ZERO:
            return(0)
        elif x == Sym.ONE:
            return(1)
        elif x == Sym.NEG_ONE:
            return(-1)
        elif x == Sym.RAND_INT:
            return(random.choice([0,1]))

    def bool_generate(self, term_prob = 0.75, uncert = 0.25):

        term = (random.random() < term_prob)
        if term:
            if (random.random() < uncert):
                return((Sym.RAND_BOOL,))
            else:
                s = random.choice(self.bool_int_comp)
                return(s, self.int_generate(term_prob, uncert), self.int_generate(term_prob, uncert))
        else:
            s = random.choice(self.bool_op)
            return (s, self.bool_generate(term_prob, uncert), self.bool_generate(term_prob, uncert))

    def bool_exp_to_str(self, bool_exp):
        x = bool_exp[0]
        if x in self.bool_op:
            comp = ""
            if x == Sym.OR:
                comp = " or "
            elif x == Sym.AND:
                comp = " and "
            return("(" + self.bool_exp_to_str(bool_exp[1]) + comp + self.bool_exp_to_str(bool_exp[2]) + ")")

        elif x in self.bool_int_comp:
            comp = ""
            if x == Sym.LESS:
                comp = " < "
            elif x == Sym.EQUAL:
                comp = " = "
            elif x == Sym.GREATER:
                comp = " > "
            return("(" + self.int_exp_to_str(bool_exp[1]) + comp + self.int_exp_to_str(bool_exp[2]) + ")")

        elif x == Sym.RAND_BOOL:
            return("RAND_BOOL")

    def bool_eval(self, bool_exp):
        x = bool_exp[0]
        if x in self.bool_op:
            if x == Sym.OR:
                return(self.bool_eval(bool_exp[1]) or self.bool_eval(bool_exp[2]))
            elif x == Sym.AND:
                return(self.bool_eval(bool_exp[1]) and self.bool_eval(bool_exp[2]))

        elif x in self.bool_int_comp:
            if x == Sym.LESS:
                return(self.int_eval(bool_exp[1]) < self.int_eval(bool_exp[2]))
            elif x == Sym.EQUAL:
                return(self.int_eval(bool_exp[1]) == self.int_eval(bool_exp[2]))
            elif x == Sym.GREATER:
                return(self.int_eval(bool_exp[1]) > self.int_eval(bool_exp[2]))

        elif x == Sym.RAND_BOOL:
            return(random.choice([True, False]))

    def generate(self, stopping = 0.75, uncert = 0.25):
        s = random.choice(self.exe)
        if(random.random() < stopping) : s = Sym.PASS
        if   ( s == Sym.IF_THEN_ELSE):
            return (s, self.bool_generate(uncert = uncert), self.generate(stopping, uncert), self.generate(stopping, uncert))
        elif ( s == Sym.PASS):
            return (s,)
        else:
            return(s, random.choice(range(len(self.choice_list))), self.generate(stopping, uncert))

    def print_commands(self, c, indent = 0):
        """ Pretty printing for algorithms """
        margin = indent * "\t"
        if c[0] == Sym.IF_THEN_ELSE:
            clause = c[1]
            print(margin + "if " + self.bool_exp_to_str(clause))
            self.print_commands(c[2], indent + 1)
            print(margin + "else")
            self.print_commands(c[3], indent + 1)
        elif c[0] == Sym.SET_CHOICE:
            if len(self.set_names) == len(self.choice_list):
                print(margin + self.set_names[c[1]])
            else:
                print(margin + "SET " + str(c[1]))
            if len(c) > 2:
                self.print_commands(c[2], indent)
        else:
            print(margin + "PASS")

    def update(self, new_obs):
        self.obs = new_obs                # Set observations for cycle
        self.choice = self.choice_list[0] # Reset to default choice

    def set_to(self, num):
        self.choice = self.choice_list[num]

    def execute(self, c):
        if c[0] == Sym.IF_THEN_ELSE:
            if self.bool_eval(c[1]):
                self.execute(c[2])
            else:
                self.execute(c[3])
        elif c[0] == Sym.PASS:
            pass
        elif c[0] == Sym.SET_CHOICE:
            self.set_to(c[1])
            if(len(c) > 2):
                self.execute(c[2])
        return(self.choice)

class Master_Language_Control(Controller):
    def __init__(self, agent, lang, stopping = 0.75, uncert = 0.25):
        self.agent = agent
        self.lang = lang
        self.uncert = uncert
        self.alg = lang.generate(stopping = stopping, uncert = uncert)

    def update(self, observations):
        self.lang.update(observations)

    def command(self):
        self.agent.update(self.lang.execute(self.alg))


def main():
    ml = Master_Language(4, ["UP","DOWN","LEFT","RIGHT"], ["CURR_X","CURR_Y","GOAL_X", "GOAL_Y"],
    ["SET_UP","SET_DOWN", "SET_LEFT", "SET_RIGHT"])
    exp = ml.generate(stopping = 0.5, uncert = 0.05)
    ml.update([1,2,3,4])
    # print(exp)
    # print()
    # print("Prints as: \n")
    # print(ml.int_exp_to_str(exp) + "\n")
    # print("Evaluates to: ")
    # print(str(ml.int_eval(exp)) + "\n")
    print("An expression: \n")
    print(exp)
    print()
    print("Prints as: \n")
    ml.print_commands(exp)
    print("Evaluates to: \n")
    print(ml.execute(exp))

if __name__ == "__main__":
    main()
