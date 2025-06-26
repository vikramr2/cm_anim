import scenes.graph_load
import sys

if __name__ == "__main__":
    scene = scenes.graph_load.TSVToGraphAnimation(tsv_file_path=sys.argv[1])
    scene.construct()
