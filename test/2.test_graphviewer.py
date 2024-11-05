from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
import sys
sys.path.append(str(ROOT_DIR))


from src.graph_viewer import GraphViewer

FPS=4
CONFIG_ROOT=ROOT_DIR / "src/configs"

viewer=GraphViewer(CONFIG_ROOT)

while True:

    try:
        viewer.step_view(FPS)

    except Exception as e:
        pass

