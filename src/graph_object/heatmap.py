import matplotlib.pyplot as plt
import pandas as pd
import yaml
import numpy as np

from .interface_line import ILine

class Heatmap(ILine):
    """
    ヒートマップのを描画するクラス
    """

    def draw(self,ax: plt.Axes):
        self.load_config()
        self.read_csv()

        self.__plot_heatmap(ax)
        self.__plot_boundary(ax)
    
    def __plot_heatmap(self,ax:plt.Axes):
        """
        ヒートマップを描画する
        """
        values=self.__get_values()
        y=self.__get_y()
        ax.imshow(
            values.reshape(1,-1),aspect='auto',
            cmap=self.config["cmap"],
            extent=[0,len(values),y-0.5,y+0.5],
            interpolation='nearest'
        )

    def __plot_boundary(self,ax:plt.Axes):
        """
        ヒートマップの枠線を描画する
        """
        values=self.__get_values()
        y=self.__get_y()
        color=self.config["boundary"]["color"]
        linewidth=self.config["boundary"]["linewidth"]
        ax.plot([0,len(values)],[y-0.5,y-0.5],color=color,linewidth=linewidth)
        ax.plot([0,len(values)],[y+0.5,y+0.5],color=color,linewidth=linewidth)

    def __get_values(self):
        valuecol_key=str(self.config["valuecol"])
        if not valuecol_key.isdecimal():
            values = self.df[valuecol_key]
        else:
            values = self.df.iloc[:,int(valuecol_key)]
        return values.values


    def __get_y(self):
        y=int(self.config["y"])
        return y

