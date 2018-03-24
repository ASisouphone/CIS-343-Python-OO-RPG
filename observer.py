from abc import ABCMeta, abstractmethod

"""
Class to create Observer objects
"""
class Observer(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def updateObserver(self, object):
                pass
