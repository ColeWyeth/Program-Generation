class Element():
    def run(self):
        pass
    def name(self):
        return("None")

class Agent(Element):
    def update(self, data):
        pass

class Controller():
    def __init__(self, agent_list):
        self.agents = agent_list
    def command(self):
        pass

class World():
    def __init__(self, element_list = [], params = []):
        self.elements = element_list
        self.params = params
    def run(self):
        pass
