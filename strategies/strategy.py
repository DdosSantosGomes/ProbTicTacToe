from abc import ABC, abstractmethod

class Strategy(ABC):
    
    @abstractmethod
    def do(self, state):
        pass
    