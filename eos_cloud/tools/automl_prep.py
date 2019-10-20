import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
import random
import shutil

random.seed(42)

def _scale(num_str, base):
    return str(float(num_str)/float(base))

def _fs_split(xml_train, xml_test, dst):
    def _copy(xml_f, _dst):
        tree = ET.parse(xml_f)
        root = tree.getroot()
        img_p = root.find('path').text
        shutil.copy(img_p, os.path.join(_dst, 'imgs',os.path.basename(img_p)))
        shutil.copy(xml_f, os.path.join(_dst, 'xmls',os.path.basename(xml_f)))
    os.makedirs(os.path.join(dst, 'train', 'imgs'), exist_ok=1)
    os.makedirs(os.path.join(dst, 'train', 'xmls'), exist_ok=1)
    os.makedirs(os.path.join(dst, 'test', 'imgs'), exist_ok=1)
    os.makedirs(os.path.join(dst, 'test', 'xmls'), exist_ok=1)
    for xml_f in xml_train:
        train_dst = os.path.join(dst, 'train')
        _copy(xml_f, train_dst)
    for xml_f in xml_test:
        test_dst = os.path.join(dst, 'test')
        _copy(xml_f, test_dst)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_dir')
    parser.add_argument('--dst')
    options = parser.parse_args(argv)
    os.makedirs(options.dst, exist_ok=1)
    label_csv = open(os.path.join(options.dst, 'labels.csv'), 'w')
    xml_fs = glob.glob(f'{options.xml_dir}/*.xml')
    random.shuffle(xml_fs)
    split_line = round(0.9 * len(xml_fs))
    xml_train = xml_fs[:split_line]
    xml_test = xml_fs[split_line:]
    _fs_split(xml_train, xml_test, options.dst)
    for xml_f in xml_train:
        tree = ET.parse(xml_f)
        root = tree.getroot()
        w = root.find('size').find('width').text
        h = root.find('size').find('height').text
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = _scale(bbx.find('xmin').text, w)
            ymin = _scale(bbx.find('ymin').text, h)
            xmax = _scale(bbx.find('xmax').text, w)
            ymax = _scale(bbx.find('ymax').text, h)
            label = member.find('name').text

            value = ('',
                    f"gs://eeeooo/imgs/{root.find('filename').text}",
                     label,
                     xmin,
                     ymin,
                     '',
                     '',
                     xmax,
                     ymax,
                     '',
                     '',
                     )
            label_csv.write(','.join(value))
            label_csv.write('\n')
    label_csv.close()

if __name__ == "__main__":
    main()