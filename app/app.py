from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
import sys
sys.path.append(str(ROOT_DIR))

import argparse
import shutil
import os

from src.graph_viewer import GraphViewer


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config_root",type=str,default=str(ROOT_DIR / "src/configs/line"),help="元のconfig. 前のコピーしたいときはこれを指定")
    parser.add_argument("--saveto",type=str,default=str(ROOT_DIR / "history/data/configs"),help="今回のconfigの保存先")
    parser.add_argument("--fps",type=int,default=4,help="描画のFPS")
    args=parser.parse_args()


    config_root=Path(args.config_root)
    new_config_path=Path(args.saveto)
    if not new_config_path.exists(): os.makedirs(new_config_path)

    if config_root!=new_config_path:
        shutil.copytree(config_root,new_config_path,dirs_exist_ok=True)

    fps=args.fps
    viewer=GraphViewer(new_config_path)

    while True:
        try:
            viewer.step_view(fps)
        except Exception as e:
            pass


if __name__=="__main__":
    main()

