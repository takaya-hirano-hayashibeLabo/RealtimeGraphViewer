import matplotlib.pyplot as plt
import pandas as pd
import yaml
import numpy as np
from matplotlib.colors import SymLogNorm,LogNorm

from .interface_line import ILine

class Heatmap(ILine):
    """
    ヒートマップのを描画するクラス
    """

    def draw(self,ax: plt.Axes):
        self.load_config()
        self.read_csv()

        im=self.__plot_heatmap(ax)

        if self.config["colorbar"]["visible"]:
            self.__set_colorbar(im)
    
    def __plot_heatmap(self,ax:plt.Axes):
        """
        ヒートマップを描画する
        """
        values=self.__get_values()
        val_min,val_max=self.__get_value_range()
        im=ax.imshow(
            values,aspect='auto',
            cmap=self.config["cmap"],
            interpolation='nearest',
            norm=self.__get_color_norm(),
            vmin=val_min,vmax=val_max
        )

        return im

    def __get_values(self):
        values=self.df.values
        if self.config["is_transposed"]:
            values=values.T
        return values

    def __get_color_norm(self):
        color_norm_key=self.config["colorbar"]["ticks"]["norm"]
        if color_norm_key=="linear":
            return None
        elif color_norm_key=="log":
            return LogNorm()
        elif color_norm_key=="symlog":
            return SymLogNorm()


    def __set_colorbar(self,im):
        """
        カラーバーを設定する
        """
        cbar=plt.colorbar(im)
        ticksize=self.config["colorbar"]["ticks"]["fontsize"]
        cbar.ax.tick_params(labelsize=ticksize)

        # カラーバーのラベルを設定
        label = self.config["colorbar"]["label"]["text"]
        labelsize=self.config["colorbar"]["label"]["fontsize"]
        cbar.set_label(label, fontsize=labelsize)


    def __get_value_range(self):
        """
        ヒートマップの値の範囲を取得する
        """
        try: val_min=self.config["colorbar"]["ticks"]["limit"]["vmin"]
        except: val_min=None

        try: val_max=self.config["colorbar"]["ticks"]["limit"]["vmax"]
        except: val_max=None

        return val_min,val_max
