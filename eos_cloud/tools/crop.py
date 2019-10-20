import cv2
import os
import glob
from collections import defaultdict
import argparse
import logging
import xml.etree.ElementTree as ET

from eos_cloud.tools import Metadata

OBS = Metadata.OBS
XMLBASE = Metadata.XMLBASE

def get_dst_img_n(img_p, num):
    return f'{os.path.splitext(os.path.basename(img_p))[0]}_{num}.jpg'

def croping(xml_dir, xml_dst, img_dir, img_dst):
    for f_n in os.listdir(xml_dir):
        xml_p = os.path.join(xml_dir, f_n)
        name = _crop_xml(xml_p, xml_dst, img_dst)
        try:
            img_p = glob.glob(f"{img_dir}/**/{name}*",
                            recursive=True)[0]
        except IndexError:
            logging.warning('%s loss', name)
        else:
            _crop_img(img_p, img_dst)
            pass

def _crop_img(img_p, img_dst):
    img = cv2.imread(img_p)
    cv2.imwrite(os.path.join(img_dst, get_dst_img_n(img_p, 0)), img[:720, :960])
    cv2.imwrite(os.path.join(img_dst, get_dst_img_n(img_p, 1)), img[:720, 960:])
    cv2.imwrite(os.path.join(img_dst, get_dst_img_n(img_p, 2)), img[720:, :960])
    cv2.imwrite(os.path.join(img_dst, get_dst_img_n(img_p, 3)), img[720:, 960:])

def _limit(value, upbar):
    if value < 0:
        return 0
    if value > upbar:
        return upbar
    return value

def _crop_xml(xml_p, xml_dst, img_dst):
    tree = ET.parse(xml_p)
    root = tree.getroot()
    xml_content = defaultdict(list)
    name = root.find('filename').text
    name = name.replace('_label.jpg', '').replace('_label.tif', '')
    for member in root.findall('object'):
        bbx = member.find('bndbox')
        xmin = int(bbx.find('xmin').text)
        ymin = int(bbx.find('ymin').text)
        xmax = int(bbx.find('xmax').text)
        ymax = int(bbx.find('ymax').text)
        if xmin >= 940: # 20 pixle as boundary pad
            xmin -= 960
            xmax -= 960
            if ymin >= 700:
                ymin -= 720
                ymax -= 720
                crop_fn = f'{name}_3'
            else:
                crop_fn = f'{name}_1'
        else:
            if ymin >= 700:
                ymin -= 720
                ymax -= 720
                crop_fn = f'{name}_2'
            else:
                crop_fn = f'{name}_0'
        xmin = _limit(xmin, 959)
        xmax = _limit(xmax, 959)
        ymin = _limit(ymin, 719)
        ymax = _limit(ymax, 719)
        xml_content[crop_fn].append(OBS.format(xmin, ymin, xmax, ymax))
    if len(xml_content) != 4:
        logging.warning('Expact 4 parts in %s, %d Parts found', name, len(xml_content))

    for crop_fn, v in xml_content.items():
        path = os.path.join(img_dst, f'{crop_fn}.jpg')
        _xml_n = f'{crop_fn}.xml'
        with open(os.path.join(xml_dst, _xml_n), 'w') as _xml:
            _xml.write(XMLBASE.format(f'{crop_fn}.jpg', path, 960, 720, ''.join(v)))

    return name

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir')
    parser.add_argument('--img_dst')
    parser.add_argument('--xml_dir')
    parser.add_argument('--xml_dst')
    options = parser.parse_args(argv)
    os.makedirs(options.xml_dst, exist_ok=1)
    os.makedirs(options.img_dst, exist_ok=1)
    croping(options.xml_dir, options.xml_dst, options.img_dir, options.img_dst)

if __name__ == "__main__":
    main()