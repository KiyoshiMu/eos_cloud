import os
import shutil
import logging
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir')
    parser.add_argument('--xml_dir')
    parser.add_argument('--img_dst')
    parser.add_argument('--xml_dst')
    options = parser.parse_args(argv)
    os.makedirs(options.xml_dst, exist_ok=1)
    os.makedirs(options.img_dst, exist_ok=1)
    for f_n in os.listdir(options.xml_dir):
        name = os.path.splitext(f_n)[0]
        img_n = f'{name}.jpg'
        img_p = os.path.join(options.img_dir, img_n)
        shutil.copy(img_p, os.path.join(options.img_dst, img_n))
        shutil.copy(os.path.join(options.xml_dir, f_n), 
                    os.path.join(options.xml_dst, f_n))