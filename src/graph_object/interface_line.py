import abc

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from .interface_graph_object import IGraphObject

class ILine(IGraphObject):
    """
    描画するアイテムの1つ分のインターフェース  
    線分や棒グラフ, ヒートマップのインターフェースを定義する
    """

    def __init__(self,config_path: str):
        self.config_path = config_path
        self.load_config()

    @abc.abstractmethod
    def draw(self,ax: plt.Axes):
        return NotImplementedError

    def load_config(self):
        """
        configを読み込む
        """
        config_tmp = yaml.safe_load(open(self.config_path,encoding='utf-8'))
        self.config = config_tmp[list(config_tmp.keys())[0]]
    def read_csv(self):
        """
        csvを読み込む
        """
        self.df = pd.read_csv(self.config['csvpath'])

    def is_config_changed(self) -> bool:
        """
        configの中身が変更されているかどうかを確認する
        """
        config_tmp = yaml.safe_load(open(self.config_path,encoding='utf-8'))
        new_config = config_tmp[list(config_tmp.keys())[0]]
        if self.config != new_config: 
            return True
        return False
