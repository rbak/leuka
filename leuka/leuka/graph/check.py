from action import Action


class Check(Action):
    def __init__(self, name, config_dir, cost, confidence, states):
        self.name = name
        super(Check, self).__init__(name, config_dir)
        self.cost = cost
        self.confidence = confidence
        self.states = states

    def run(self, **kwargs):
        return self.actionmod.run(**kwargs)
