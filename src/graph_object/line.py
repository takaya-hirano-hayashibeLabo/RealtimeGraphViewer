import matplotlib.pyplot as plt
import pandas as pd
import yaml
import numpy as np

from .interface_graph_object import IGraphObject

class Line(IGraphObject):
    def __init__(self,config_path: str):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        self.config = yaml.safe_load(open(self.config_path,encoding='utf-8'))["line"]

    def __read_csv(self):
        self.df = pd.read_csv(self.config['csvpath'])

    def draw(self,ax: plt.Axes):
        self.load_config()

        self.__read_csv()

        self.__plot_line(ax)
        self.__draw_std(ax)

    def __plot_line(self, ax: plt.Axes):
        x,y=self.__get_xy()
        ax.plot(x, y, 
                marker=self.config['marker']['style'], 
                markersize=self.config['marker']['size'], 
                linestyle=self.config['linestyle']['style'], 
                linewidth=self.config['linestyle']['width'], 
                color=np.array(self.config['color'])/255,
                label=self.config['label']['text']
            )
        
    def __draw_std(self, ax: plt.Axes):
        if self.config["stdcol"] is not None:
            x,y=self.__get_xy()
            std = self.__get_std()
            ax.fill_between(
                x, y-std, y+std, alpha=0.5,
                color=np.array(self.config['color'])/255
            )

    def __get_xy(self):
        
        xcol_key=str(self.config["xcol"])
        if not xcol_key.isdecimal():
            x = self.df[xcol_key]
        else:
            x = self.df.iloc[:,int(xcol_key)]

        ycol_key=str(self.config["ycol"])
        if not ycol_key.isdecimal():
            y = self.df[ycol_key]
        else:
            y = self.df.iloc[:,int(ycol_key)]

        return x.values, y.values
    
    def __get_std(self):
        stdcol_key=str(self.config["stdcol"])
        if not stdcol_key.isdecimal():
            std = self.df[stdcol_key]
        else:
            std = self.df.iloc[:,int(stdcol_key)]
        return std.values

    def is_config_changed(self) -> bool:
        new_config = yaml.safe_load(open(self.config_path,encoding='utf-8'))["line"]
        if self.config != new_config: 
            return True
        return False
