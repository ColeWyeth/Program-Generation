class Element():
    def run(self):
        pass
    def name(self):
        return("None")

class Agent(Element):
    def update(self, data):
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
