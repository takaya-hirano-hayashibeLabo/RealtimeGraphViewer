import os
from pathlib import Path
import yaml
import matplotlib.pyplot as plt
from .graph_object.canvas import Canvas
from .graph_object.line import Line
from .graph_object.heatmap import Heatmap

from .graph_object.interface_line import ILine

class GraphViewer:
    """
    グラフの中のオブジェクトの増減を管理するクラス
    描画については関与しない(canvasのshowを呼び出すのみ)
    """

    def __init__(self,config_root:str):
        self.config_root=Path(config_root)

        self.canvas:Canvas
        self.__init_canvas()

        self.lines:list[ILine]=[]
        self.__init_lines()

        self.config_paths:list[Path]=self.__load_line_config_paths()


    def step_view(self, fps:int):
        """
        1ループあたりのビュー更新
        これをやるだけで良い
        """

        dt=1/fps

        # グラフの増減(=configの増減)があったら, グラフのリストを更新(インスタンスのこと. 描画とは無関係)
        is_add_remove_lines=self.__is_add_remove_lines()
        if is_add_remove_lines: self.__add_remove_lines()


        # 中身の変更 or グラフの数の増減 があればビューを更新
        if self.__is_changed_config_contents() or is_add_remove_lines: 
            self.canvas.show(self.lines,dt)

        else: plt.pause(dt) #なければ表示するだけ


    def __add_remove_lines(self):
        """
        新たなグラフをメンバリストに追加したり、グラフを削除したりする
        描画とは全くの無関係
        """

        new_config_paths=self.__load_line_config_paths()

        is_add=len(new_config_paths)>len(self.config_paths)
        is_delete=len(new_config_paths)<len(self.config_paths)

        self.config_paths=new_config_paths #configpathリストを更新

        if is_add:
            print("add lines")
            self.__add_new_lines(new_config_paths)

        if is_delete:
            print("delete lines")
            deleted_line_config_paths=self.__find_deleted_lines(self.config_paths)
            self.__delete_lines(deleted_line_config_paths)


    def __is_add_remove_lines(self):
        """
        root内のコンフィグパス自体が変わったかどうか
        (=グラフが増えたり消えたりしたかどうか)
        """
        new_line_config_paths=self.__load_line_config_paths()
        if new_line_config_paths==self.config_paths: return False
        else: return True


    def __is_changed_config_contents(self):
        """
        オブジェクトが変わったかどうか
        (=configが書き換えられたかどうか)
        """
        if self.canvas.is_config_changed(): return True
        for line in self.lines:
            if line.is_config_changed(): return True
        return False

    def __init_canvas(self):
        self.canvas=Canvas(self.config_root / "canvas.yml")

    def __load_line_config_paths(self):
        """
        キーが`line`のymlファイルのパスリストを返す
        """
        line_config_paths=[]

        conf_files=os.listdir(self.config_root)

        for conf_file in conf_files:
            conf_path=self.config_root / conf_file
            config_key=list(yaml.safe_load(open(conf_path,encoding='utf-8')).keys())[0]
            if config_key!="canvas": #canvasは別で管理している
                line_config_paths.append(conf_path)
        
        return line_config_paths
    
    def __init_lines(self):
        line_config_paths=self.__load_line_config_paths()
        self.__add_new_lines(line_config_paths)


    def __is_new_line_config(self,line_config:Path):
        """
        与えられたconfgipathが新しいものか判別する
        """
        for line in self.lines:
            if line.config_path==line_config:
                return False
        return True
        
    def __find_deleted_lines(self,line_config_paths:list[Path]):
        """
        与えられたconfigpathリストのうち, メンバリストに存在しないものを返す
        (=削除されたインスタンスを見つける)
        """
        deleted_line_config_paths=[]
        for line in self.lines:
            if line.config_path not in line_config_paths:
                deleted_line_config_paths.append(line.config_path)

        return deleted_line_config_paths

    def __delete_lines(self,deleted_line_config_paths:list[Path]):
        for deleted_line_config_path in deleted_line_config_paths:
            for line in self.lines:
                if line.config_path==deleted_line_config_path:
                    self.lines.remove(line)
                    break

    def __add_new_lines(self,line_config_paths:list[Path]):
        """
        IGraphObjectの種類が増えると関数が肥大化するなあぁ...
        open-closedの原則を守れない
        ただ, こればっかしは仕方ないと思います
        """

        for line_config_path in line_config_paths:
            if self.__is_new_line_config(line_config_path):

                config_key=list(yaml.safe_load(open(line_config_path,encoding='utf-8')).keys())[0]
                print(config_key)
                if config_key=="line":
                    self.lines.append(Line(line_config_path))
                elif config_key=="heatmap":
                    self.lines.append(Heatmap(line_config_path))

