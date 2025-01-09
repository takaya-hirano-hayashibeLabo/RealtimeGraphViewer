from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
import sys
sys.path.append(str(ROOT_DIR))

import argparse
import shutil
import os

from src.graph_viewer import GraphViewer


def copy_config(config_root:Path,new_config_path:Path):
    for root, dirs, files in os.walk(config_root):
            for file in files:
                if file.endswith('.yml'):
                    src_file = Path(root) / file
                    dest_file = new_config_path / src_file.relative_to(config_root)
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dest_file)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--template",type=str,default=str(ROOT_DIR / "src/configs/line"),help="元のconfig. 前のコピーしたいときはこれを指定")
    parser.add_argument("--saveto",type=str,default=None,help="今回のconfigの保存先")
    parser.add_argument("--fps",type=int,default=4,help="描画のFPS")
    args=parser.parse_args()


    config_root=Path(args.template)

    if args.saveto is None:
        new_config_path=Path(args.template)
    else: 
        new_config_path=Path(args.saveto)
    if not new_config_path.exists(): os.makedirs(new_config_path)

    if config_root!=new_config_path:
        copy_config(config_root,new_config_path)

    fps=args.fps
    viewer=GraphViewer(new_config_path)

    while True:
        try:
            viewer.step_view(fps)
        except Exception as e:
            print(e)


if __name__=="__main__":
    main()

