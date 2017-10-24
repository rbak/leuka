from action import Action


class Fix(Action):
    def __init__(self, name, config_dir):
        self.name = name
        super(Fix, self).__init__(name, config_dir)

    def run(self, **kwargs):
        return self.actionmod.run(**kwargs)

    def tell(self, **kwargs):
        self.actionmod.tell(**kwargs)
