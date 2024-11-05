import abc

class IGraphObject(abc.ABC):

    def __init__(self,config_path:str):
        self.config_path=config_path

    @abc.abstractmethod
    def load_config(self):
        pass

    @abc.abstractmethod
    def is_config_changed(self) -> bool:
        pass

