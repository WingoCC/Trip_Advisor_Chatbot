from abc import ABCMeta, abstractmethod


class AbstractStatus(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def make_response(self):
        pass
