#!/usr/bin/env python

import sys
from PIL import Image
import os
from multiprocessing import Pool

QA = 50
PROC = 8


def compress_img(img_path):
    print("Compressing img %s" % img_path)
    f = Image.open(img_path)
    f.save(img_path, optimize=True, quality=QA)


def is_jpg(img):
    return img.endswith(".jpg") or img.endswith(".JPG")


def compress(path):
    pool = Pool(processes=PROC)

    for folder, subfolder, files in os.walk(path):
        imgs = [os.path.join(folder, i) for i in files if is_jpg(i)]
        pool.map(compress_img, imgs)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("No path given")
        exit(1)
    compress(sys.argv[1])
