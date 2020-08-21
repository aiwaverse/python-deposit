#%%
import PIL as P
import argparse
import imagehash
import subprocess
import glob
import pickle
from typing import *


def get_all_files(root_dir: str, *, rec=True) -> List[str]:
    """
    Returns all files and folders of a @root_dir
    recursive unless @rec=False
    """
    path_list = glob.glob(root_dir + "/**", recursive=True)
    image_only = filter(lambda p: p.endswith("jpg") or p.endswith("png"), path_list)
    return list(image_only)

#%%
def make_image_dict(
    files: List[str], hash=imagehash.dhash
) -> Dict[imagehash.ImageHash, List[str]]:
    images_dict: Dict[imagehash.ImageHash, List[str]] = {}
    for file_loc in files:
        img_hash = hash(P.Image.open(file_loc))
        if img_hash not in images_dict:
            images_dict[img_hash] = []
        images_dict[img_hash].append(file_loc)
    return images_dict


#%%
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A solution to dealing with large collections of possible duplicate images"
    )
    parser.add_argument(
        "--generate-hash",
        "-gh",
        dest="generate_hash",
        action="store_true",
        help="Pass this flag to only generate a database for the hashing, recommended for first run.",
    )
    parser.add_argument(
        "--databse",
        "-db",
        nargs=1,
        dest="db_path",
        help="path of the generated database",
        type=str,
    )
    parser.add_argument(
        "folder",
        nargs=1,
        help="roogst folder of the pictures",
        type=str
    )
    args = parser.parse_args()
    folder = args.folder[0]
    if args.generate_hash:
        name = folder.split("/")[-1] + "-databse.bin"
        with open(name, "wb") as bf:
            print("Starting to probe folder!")
            files = get_all_files(folder)
            print("Generating hashing...")
            image_dict = make_image_dict(files)
            print(f"Impriting hashing on file {name}")
            pickle.dump(image_dict, bf)

# %%
