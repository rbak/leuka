class AbstractUpdater(object):

    TYPES = []

    def update(self, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    def toAdd(self):
        raise NotImplementedError("Please Implement this method")

    def toRemove(self):
        raise NotImplementedError("Please Implement this method")
