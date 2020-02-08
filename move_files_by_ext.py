"""Move files by extension

This script allows the user to move all files with a certain extension 
from a folder recursively to a new folder.

If the source folder is `/data/foo` and the extension is `jpg`, the script
will search all the .jpg files recursively inside /data/foo folder and 
subfolders and it will copy the found files in a new folder called
`/data/foo_jpg/`

If some file already exist in the new folder, it will be renamed in the 
destiny adding the sufix `_hhmmss` being hh the current hour, mm - minutes
and ss - seconds
"""
import os
import ntpath
import time
import argparse

from pathlib import Path
from shutil import copy2


if __name__ == "__main__":

    # argument parsing
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('origin_folder', type=str, help='Path to the folder to be inspected')
    parser.add_argument('--ext', type=str, help='Extension of the files to be extracted. Default jpg',
                        default='jpg')

    args = parser.parse_args()

    dir_path = args.origin_folder
    extension = args.ext

    # searching matching files
    dest_path = f'{dir_path}_{extension}/'
    to_be_copied = list(Path(dir_path).rglob(f"*.{extension}"))
    print(f'{len(to_be_copied)} files found. Copying to folder {dest_path}')


    # creating target directory if it doesn't exist
    try:
        os.mkdir(dest_path)
    except FileExistsError:
        print(f"Directory {dest_path} already exists - using this dir and adding new files")

    # copying files
    renamed_files = 0
    for origin_file in to_be_copied:

        file_name = ntpath.basename(origin_file)

        # if the file already exists, rename with the timestamp
        if ntpath.exists(f'{dest_path}{file_name}'):
            dest_file = f'{dest_path}{file_name}_{time.strftime("%H%M%S")}'
            renamed_files += 1
        else:
            dest_file = dest_path

        copy2(origin_file, dest_file)

    # showing results
    print(f'{len(to_be_copied)} files copied. {renamed_files} duplicated filenames - renamed')