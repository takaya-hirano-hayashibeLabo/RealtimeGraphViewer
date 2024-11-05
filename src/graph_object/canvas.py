import matplotlib.pyplot as plt
from copy import deepcopy
import yaml
import seaborn as sns
sns.set(style="darkgrid")
from matplotlib import rcParams
import numpy as np

from .interface_graph_object import IGraphObject
from .interface_line import ILine

class Canvas(IGraphObject):

    def __init__(self, config_path: str):
        self.config_path = config_path
        
        self.figure, self.ax = plt.subplots(1,1,figsize=(1,1)) #適当に初期化
        self.config = None

    def load_config(self):
        self.config = yaml.safe_load(open(self.config_path,encoding='utf-8'))["canvas"]

    def __init_canvas(self,config: dict):
        # Example of using the configuration
        rcParams['font.family'] = config['fontstyle']['family']
        self.figure, self.ax = plt.subplots(1,1,figsize=(
            self.__cm2inch(config['figsize']['width']), 
            self.__cm2inch(config['figsize']['height'])
        ),dpi=100)

    def __set_canvas_params(self,config: dict):

        self.figure.suptitle(config['title']['text'], fontsize=config['title']['fontsize'])
        self.ax.set_xlabel(config['label']['xlabel'], fontsize=config['label']['fontsize'])
        self.ax.set_ylabel(config['label']['ylabel'], fontsize=config['label']['fontsize'])
        self.__set_grid()
        self.__set_xylim()
        self.__set_xyticks()
        self.__set_axscale()
        self.__set_legend()
        self.__set_colorbar()
    def __cm2inch(self,cm):
        return cm / 2.54
    
    def is_config_changed(self) -> bool:
        new_config = yaml.safe_load(open(self.config_path,encoding='utf-8'))["canvas"]
        if self.config != new_config: 
            return True
        return False

    def show(self, lines: list[ILine], dt: float):
        print(lines)

        plt.close()

        self.load_config()
        self.__init_canvas(self.config)

        for line in lines:
            line.draw(self.ax)

        self.__set_canvas_params(self.config)

        plt.tight_layout()

        plt.pause(dt)

    def __set_xylim(self):
        if self.config["limit"]["xmin"] is not None and self.config["limit"]["xmax"] is not None:
            self.ax.set_xlim(self.config["limit"]["xmin"], self.config["limit"]["xmax"])
        if self.config["limit"]["ymin"] is not None and self.config["limit"]["ymax"] is not None:
            self.ax.set_ylim(self.config["limit"]["ymin"], self.config["limit"]["ymax"])


    def __set_xyticks(self):
        """
        目盛りの設定
        """

        if self.config["limit"]["xmax"] is not None and self.config["limit"]["xmin"] is not None: 
            xtick_max = self.ax.get_xlim()[1]
            xtick_min = self.ax.get_xlim()[0]
            step=(xtick_max-xtick_min)/self.config["ticks"]["xwidth"]
            xbias = self.config["ticks"]["xbias"]
            xticks = np.arange(xtick_min, xtick_max, step) + xbias
            self.ax.set_xticks(xticks)

            ticks_labels=[
                f"{(val):.{self.config['ticks']['num_decimal_places']}f}" for val in xticks
            ]
            self.ax.set_xticklabels(ticks_labels,fontsize=self.config["ticks"]["fontsize"])         

        if self.config["limit"]["ymax"] is not None and self.config["limit"]["ymin"] is not None: 
            ytick_max = self.ax.get_ylim()[1]
            ytick_min = self.ax.get_ylim()[0]
            step=(ytick_max-ytick_min)/self.config["ticks"]["ywidth"]
            ybias = self.config["ticks"]["ybias"]
            yticks = np.arange(ytick_min, ytick_max, step) + ybias
            self.ax.set_yticks(yticks)

            ticks_labels=[
                f"{(val):.{self.config['ticks']['num_decimal_places']}f}" for val in yticks
            ]
            self.ax.set_yticklabels(ticks_labels,fontsize=self.config["ticks"]["fontsize"])


    def __set_axscale(self):
        """
        対数軸とかの設定をする
        """
        if self.config["axscale"]["x"] == "log":
            self.ax.set_xscale("log")
        if self.config["axscale"]["y"] == "log":
            self.ax.set_yscale("log")


    def __set_grid(self):
        self.ax.grid(alpha=self.config["grid"]["alpha"])


    def __set_legend(self):
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend(fontsize=self.config['legend']['fontsize'])

    def __set_colorbar(self):
        """
        1つ目のimshowのカラーバーを設定する
        """
        if len(self.ax.images) > 0:
            cbar=plt.colorbar(self.ax.images[0], ax=self.ax,orientation='vertical')
            cbar.ax.tick_params(labelsize=self.config["ticks"]["fontsize"])
