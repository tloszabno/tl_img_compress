#!/usr/bin/env python

import sys
from PIL import Image
import os
from multiprocessing import Pool
from multiprocessing import cpu_count

concurrency_level = cpu_count()  # as many as concurrency_levelessors
default_jpg_quality = 80

result = ""


def fix_orientation(img):
    if hasattr(img, '_getexif'):
        orientation = 0x0112
        exif = img._getexif()
        if exif is not None:
            orientation = exif[orientation]
            rotations = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotations:
                img = img.transpose(rotations[orientation])
    return img


def compress_img(compress_cmd):
    (img_path, jpg_quality) = compress_cmd

    print("Compressing img %s" % img_path)
    try:
        f = Image.open(img_path)
        f = fix_orientation(f)
        f.save(img_path, optimize=True, quality=jpg_quality)
    except Exception as e:
        print(e)
        global result
        result += str(e) + "\n"


def is_jpg(img):
    return img.endswith(".jpg") or img.endswith(".JPG")


def compress(path, quality, recursive=False):
    pool = Pool(processes=concurrency_level)
    dir_iteraror = os.walk(path)
    if not recursive:
        dir_iteraror = [next(dir_iteraror)]  # only first el as list

    for folder, _, files in dir_iteraror:
        imgs = [(os.path.join(folder, i), quality) for i in files if is_jpg(i)]
        pool.map(compress_img, imgs)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error. Should be: ./%s PATH [-qN] [-r]" % sys.argv[0])
        print("-r - Recursive")
        print("-qN - jpg quality, eg -q50")
        exit(1)

    quality = default_jpg_quality
    recursive = False
    for arg in sys.argv[2:]:
        if arg.startswith('-q'):
            quality = int(arg[2:])
        if arg == '-r':
            recursive = True
    print("Starting recursive=%s quality=%s" % (str(recursive), str(quality)))
    compress(sys.argv[1], quality, recursive)
    print("END")
    print(result)
