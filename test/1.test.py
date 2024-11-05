from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
import sys
sys.path.append(str(ROOT_DIR))
import yaml
import time


from src.graph_object.canvas import Canvas
from src.graph_object.line import Line
from src.graph_object.interface_graph_object import IGraphObject


def is_config_changed(objects: list[IGraphObject]):
    for obj in objects:
        if obj.is_config_changed():
            return True
    return False


FPS=4

line = Line(ROOT_DIR / 'src/configs/line/line.yml')
canvas = Canvas(ROOT_DIR / 'src/configs/line/canvas.yml')
objects=[line,canvas]
canvas.show([line],dt=1/FPS)
while True:
    start_time = time.time()

    try:

        if is_config_changed(objects):
            print("config changed")
            canvas.show([line],dt=1/FPS)

    except Exception as e:
        pass

