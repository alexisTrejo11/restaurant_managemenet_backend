from abc import ABC, abstractmethod

class UseCase(ABC):
    @abstractmethod
    def execute(self, request=None):
        pass