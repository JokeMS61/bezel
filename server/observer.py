from abc import ABCMeta, abstractmethod
 
class Observer(object):
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    def notify(self):
        pass

    def getName (self):
        pass

    def setName (self):
        pass
