import enum
import random
from grid import Dir

class Language():
    def generate():
        pass
    def interpret():
        pass

class Sym(enum.Enum):
    GOAL_X          = 1
    GOAL_Y          = 2
    CURR_X          = 3
    CURR_Y          = 4
    SET_UP          = 5
    SET_RIGHT       = 6
    SET_DOWN        = 7
    SET_LEFT        = 8
    IF_THEN_ELSE    = 9
    LESS            = 10
    EQUAL           = 11
    GREATER         = 12
    PASS            = 13


class Basic_Grid(Language):
    def __init__(self):
        self.symbols = list(Sym)
        self.bool = [Sym.LESS, Sym.EQUAL, Sym.GREATER]
        self.num  = [Sym.GOAL_X, Sym.GOAL_Y, Sym.CURR_X, Sym.CURR_Y]
        self.exe  = [Sym.SET_UP, Sym.SET_DOWN, Sym.SET_LEFT, Sym.SET_RIGHT,
                     Sym.IF_THEN_ELSE]
        self.goal_x = 0
        self.goal_y = 0
        self.curr_x = 0
        self.curr_y = 0
        self.dir = Dir.UP

    def generate(self, stopping = 3):
        s = random.choice(self.exe)
        if(random.choice(range(stopping)) == 0) : s = Sym.PASS
        if   ( s == Sym.IF_THEN_ELSE):
            return (s, (random.choice(self.bool), random.choice(self.num),
                        random.choice(self.num)) , self.generate(), self.generate())
        elif (s == Sym.LESS or s == Sym.GREATER or s == Sym.EQUAL):
            return (s, random.choice(self.num), random.choice(self.num))
        elif ( s == Sym.PASS):
            return (s,)
        else:
            return(s, self.generate())

    def print_commands(self, c, indent = 0):
        margin = indent * "\t"
        if c[0] == Sym.IF_THEN_ELSE:
            clause = c[1]
            comp = ""
            if clause[0] == Sym.LESS:
                comp = " < "
            elif clause[0] == Sym.EQUAL:
                comp = " = "
            elif clause[0] == Sym.GREATER:
                comp = " > "
            print(margin + "if " + clause[1].name + comp + clause[2].name)
            self.print_commands(c[2], indent + 1)
            print(margin + "else")
            self.print_commands(c[3], indent + 1)
        else:
            print(margin + c[0].name)
            if len(c) > 1:
                self.print_commands(c[1], indent)

    def update(self, goal_x, goal_y, curr_x, curr_y):
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.curr_x = curr_x
        self.curr_y = curr_y
        self.dir = Dir.UP

    def sym_to_value(self, s):
        if s == Sym.GOAL_X:
            return(self.goal_x)
        elif s == Sym.GOAL_Y:
            return self.goal_y
        elif s == Sym.CURR_X:
            return self.curr_x
        elif s == Sym.CURR_Y:
            return self.curr_y
        else:
            raise

    def set_to(self, s):
        if s == Sym.SET_UP:
            self.dir = Dir.UP
        elif s == Sym.SET_DOWN:
            self.dir = Dir.DOWN
        elif s == Sym.SET_LEFT:
            self.dir = Dir.LEFT
        elif s == Sym.SET_RIGHT:
            self.dir = Dir.RIGHT
        elif s == Sym.PASS:
            pass
        else: raise Exception("Invalid Set")


    def execute(self, c):
        if c[0] == Sym.IF_THEN_ELSE:
            clause = c[1]
            bool_val = False
            x = self.sym_to_value(clause[1])
            y = self.sym_to_value(clause[2])
            if clause[0] == Sym.LESS:
                bool_val = x < y
            elif clause[0] == Sym.EQUAL:
                bool_val = (x == y)
            elif clause[0] == Sym.GREATER:
                bool_val = (x > y)
            else: raise Exception("Invalid Compare")

            if bool_val:
                self.execute(c[2])
            else:
                self.execute(c[3])
        else:
            self.set_to(c[0])
            if(len(c) > 1):
                self.execute(c[1])
        return(self.dir)


def main():
    grid = Basic_Grid()
    commands = grid.generate()
    print(commands)
    print()
    grid.print_commands(commands)
    grid.update(1,1,0,0)
    print()
    print(grid.execute(commands))

if __name__ == "__main__":
    main()
