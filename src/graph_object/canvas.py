import matplotlib.pyplot as plt
from copy import deepcopy
import yaml
import seaborn as sns
# sns.set(style="darkgrid")
from matplotlib import rcParams
rcParams['text.usetex'] = True
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
        self.__set_seaborn_style()
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
        self.__set_axscale()
        self.__set_ticks_bar()
        self.__set_ticks_label()
        self.__set_legend()
        self.__adjust_margins()

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
        self.__remove_axes_frame()
        for line in lines:
            line.draw(self.ax)

        self.__set_canvas_params(self.config)

        # plt.tight_layout()

        plt.pause(dt)

    def __set_xylim(self):
        if self.config["limit"]["xmin"] is not None and self.config["limit"]["xmax"] is not None:
            self.ax.set_xlim(self.config["limit"]["xmin"], self.config["limit"]["xmax"])
        if self.config["limit"]["ymin"] is not None and self.config["limit"]["ymax"] is not None:
            self.ax.set_ylim(self.config["limit"]["ymin"], self.config["limit"]["ymax"])


    def __get_ticks_value(self,axis:str="x"):
        """
        メモリの軸の数値の設定
        :param axis: "x" or "y"
        """
        if axis=="x":
            xtick_max = self.ax.get_xlim()[1]
            xtick_min = self.ax.get_xlim()[0]
            step=(xtick_max-xtick_min)/self.config["ticks"]["xwidth"]
            xbias = self.config["ticks"]["xbias"]
            xticks = np.arange(xtick_min, xtick_max, step) + xbias
            return xticks
        elif axis=="y":
            ytick_max = self.ax.get_ylim()[1]
            ytick_min = self.ax.get_ylim()[0]   
            step=(ytick_max-ytick_min)/self.config["ticks"]["ywidth"]
            ybias = self.config["ticks"]["ybias"]
            yticks = np.arange(ytick_min, ytick_max, step) + ybias
            return yticks


    def __ticks_value2label(self,ticks:list[float]):
        if self.config["ticks"]["num_type"] == "decimal":
            labels=[
                f"{(val):.{self.config['ticks']['num_decimal_places']}f}" for val in ticks
            ]
            return labels
        elif self.config["ticks"]["num_type"] == "scientific":
            labels = []
            for val in ticks:
                exponent = int(np.floor(np.log10(abs(val)))) if val != 0 else 0
                base = val / 10**exponent
                labels.append(f"${base:.1f} \\times 10^{{{exponent}}}$")
            return labels

    def __set_ticks_bar(self):
        """
        メモリの軸の数値の設定
        """
        if self.config["limit"]["xmax"] is not None and self.config["limit"]["xmin"] is not None: 
            xticks = self.__get_ticks_value(axis="x")
            self.ax.set_xticks(xticks)

        if self.config["limit"]["ymax"] is not None and self.config["limit"]["ymin"] is not None: 
            yticks = self.__get_ticks_value(axis="y")
            self.ax.set_yticks(yticks)

    def __set_ticks_label(self):
        """
        メモリの軸の数値のラベルの設定
        """
        if not self.config["ticks"]["visible"]["xlabel"]:
            self.ax.set_xticklabels([])
        else:
            if self.config["limit"]["xmax"] is not None and self.config["limit"]["xmin"] is not None: 
                xticks = self.__get_ticks_value(axis="x")
                ticks_labels=self.__ticks_value2label(xticks)
                self.ax.set_xticklabels(ticks_labels,fontsize=self.config["ticks"]["fontsize"])  
            else:
                self.ax.tick_params(axis='x',labelsize=self.config["ticks"]["fontsize"])  


        if not self.config["ticks"]["visible"]["ylabel"]:
            self.ax.set_yticklabels([])
        else:
            if self.config["limit"]["ymax"] is not None and self.config["limit"]["ymin"] is not None: 
                yticks = self.__get_ticks_value(axis="y")
                ticks_labels=self.__ticks_value2label(yticks)
                self.ax.set_yticklabels(ticks_labels,fontsize=self.config["ticks"]["fontsize"])
            else:
                self.ax.tick_params(axis='y',labelsize=self.config["ticks"]["fontsize"])

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
        if self.config["legend"]["visible"]:
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend(
                    fontsize=self.config['legend']['fontsize'],
                    loc='upper center',  # Change location to upper center
                    bbox_to_anchor=tuple(self.config['legend']['bbox_to_anchor']),  # Adjust position above the plot
                    ncol=self.config['legend']['ncol']  # Optional: Adjust number of columns in the legend
                )


    def __adjust_margins(self):
        """
        グラフの余白を調整する
        """
        margins = self.config.get("margin", {})
        left = self.__cm2inch(margins.get("left", 0))
        right = self.__cm2inch(margins.get("right", 0))
        top = self.__cm2inch(margins.get("top", 0))
        bottom = self.__cm2inch(margins.get("bottom", 0))

        # 負の値が入ったら、余白をその分だけ減らす
        self.figure.subplots_adjust(
            left=max(0, self.figure.subplotpars.left + left / self.figure.get_figwidth()),
            right=min(1, self.figure.subplotpars.right - right / self.figure.get_figwidth()),
            top=min(1, self.figure.subplotpars.top - top / self.figure.get_figheight()),
            bottom=max(0, self.figure.subplotpars.bottom + bottom / self.figure.get_figheight())
        )

    
    def __set_seaborn_style(self):
        try:
            style=self.config["seaborn_style"]
            sns.set(style=style)
        except Exception as e:
            print(e)
            sns.set(style="darkgrid")

    def __remove_axes_frame(self):
        """
        グラフの枠を消す
        """
        try:
            if not self.config["frame_visible"]:
                for spine in self.ax.spines.values():
                    spine.set_visible(False)
                # Remove the ticks
                self.ax.tick_params(left=False, bottom=False, labelleft=True, labelbottom=True)
            
            elif self.config["frame_visible"]:
                for spine in self.ax.spines.values():
                    spine.set_visible(True)
                self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        except Exception as e:
            print(e)