#%%
import argparse
import glob
import imagehash
import os
import pickle
import subprocess
from PIL import Image
from send2trash import send2trash
from typing import *


#%%
def process_dupes_manually(images: List[Image.Image]) -> Image.Image:
    """
    Given a list of @images, will ask the user for one
    This is to used when automatically processing was not able to determinate a match
    """
    print("The program was unable to automatically choose a duplicate.")
    print("Please choose one of below:")
    while True:
        code = 1
        for image in images:
            print(f"{code}: {image.filename}")
            code += 1
        print(f"Press {code} to show each image, or 0 to skip")
        code = int(input())
        if code == 0:
            return None
        if code <= len(images):
            return images[code - 1]
        else:
            for image in images:
                image.show()


#%%
def process_dupes_sizes(paths: List[str]) -> List[Image.Image]:
    """
    Given a list of @paths, returns a list only with the largest size
    if multiple elements have the same size, returns multiple elements
    otherwise it's a singleton list
    """
    img_list = []
    for path in paths:
        img_list.append(Image.open(path))
    largest_s = max(img_list, key=lambda i: i.size)
    images_with_the_same_size = list(
        filter(lambda s: s.size == largest_s.size, img_list)
    )
    return images_with_the_same_size


#%%
def process_dupes_priority(
    images: List[Image.Image], priority_list: List[str]
) -> List[Image.Image]:
    """
    Given a list of @paths (images) and a @priority_list of folder names
    returns the paths on the largest priority
    the highest number, the bigger the priority
    """
    priority_list.reverse()
    priority_dict = {
        key: priority_list.index(key)
        for (key, _) in dict().fromkeys(priority_list).items()
    }
    prioritized_paths = []
    for image in images:
        found = -1
        path = os.path.dirname(os.path.abspath(image.filename))
        for folder, value in priority_dict.items():
            if folder in path:
                found = value
        prioritized_paths.append((image, found))
    prioritized_paths.sort(key=lambda p: p[1])
    largest_priority = prioritized_paths[0][1]
    prioritized_paths = [t[0] for t in prioritized_paths if t[1] == largest_priority]
    return prioritized_paths


#%%
def process_dupes_formats(images: List[Image.Image]) -> List[Image.Image]:
    """
    returns a list of pngs, or, if empty, returns the original list
    """
    pngs = list(filter(lambda i: i.filename.endswith("png"), images))
    if not pngs:
        return images
    return pngs


#%%
def filter_image_dictionary(
    dic: Dict[imagehash.ImageHash, List[str]], priority_list: List[str]
) -> None:
    for image, paths in dic:
        if len(paths) > 1:  # then we have duplicates
            largests = process_dupes_sizes(paths)
            pick = largests[0]
            if len(largests) > 1:  # couldn't determine by just size
                formatted = process_dupes_formats(largests)
                pick = formatted[0]
                if len(formatted) > 1:  # couldn't determine by format
                    prioritized = process_dupes_priority(formatted, priority_list)
                    pick = prioritized[0]
                    if len(prioritized) > 1:  # couldn't determine by priority
                        pick = process_dupes_manually(prioritized)
            delete_others(pick, paths)


#%%
def delete_others(pick: Image.Image, others: List[str]) -> None:
    """
    Given an image and a list of paths to other images
    sends the other to trash
    """
    if pick:
        for other in others:
            if pick.filename not in other:
                send2trash(other)


#%%
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
    """
    Given a list of @files@ and a @hash@ function, returns 
    a dictionary file, using the hashed image as key, and
    the path as value
    """
    images_dict: Dict[imagehash.ImageHash, List[str]] = {}
    for file_loc in files:
        with Image.open(file_loc) as img:
            img_hash = hash(img)
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
        "--folder", "-f", nargs="?", help="root folder of the pictures, if empty, assumed to be current folder", type=str, default="."
    )
    parser.add_argument(
        "--priority-list",
        "-pl",
        dest="priority_list",
        nargs="*",
        default=[],
        help="Priority list for folders, images on a higher priority list will be chosen instead of lower priority ones, if a folder is not on the list, it's assumed to have the lowest priority.",
    )
    args = parser.parse_args()
    folder = args.folder
    print(folder)
    print(args.priority_list)
