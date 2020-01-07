class Element():
    def name(self):
        return("None")
    def reset(self):
        pass

class Agent(Element):
    def update(self, choice):
        pass


class Controller():
    def __init__(self, agent):
        self.agent = agent
    def command(self):
        pass

class World():
    def __init__(self, element_list = [], params = []):
        self.elements = element_list
        self.params = params
    def run(self):
        pass
    def obs(self, agent):
        return([])
    def reset(self):
        for e in self.elements:
            e.reset()

class Language():
    def generate():
        pass
    def execute():
        pass

class Language_Controller(Controller):
    def __init__(self, agent, lang):
        self.agent = agent
        self.lang = lang
        self.alg = lang.generate()

    def update(self, observations):
        self.lang.update(observations)

    def command(self):
        self.agent.update(self.lang.execute(self.alg))

def loop(c, w, steps):
    for i in range(steps):
        if(w.run() == 1):
            print("Objective achieved")
            return(1)
        c.update(w.obs(c.agent))
        c.command()
    return(0)
