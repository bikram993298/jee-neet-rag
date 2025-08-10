import faiss
import argparse
import shutil
from pathlib import Path

def export_faiss(index_path, output_dir):
    index = faiss.read_index(index_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy(index_path, Path(output_dir) / Path(index_path).name)
    print(f"Exported FAISS index to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index_path", type=str, required=True, help="Path to FAISS index file")
    parser.add_argument("--output_dir", type=str, required=True, help="Destination directory")
    args = parser.parse_args()

    export_faiss(args.index_path, args.output_dir)
