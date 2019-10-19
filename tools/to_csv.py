import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def scale(num_str, base):
    num = float(num_str)
    if num < 0:
        return '0'
    ret = num/float(base)
    if ret > 1:
        return '1'
    return str(ret)

def xml_to_csv(path):
    label_csv = open('label_tmp.csv', 'w')
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        w = root.find('size').find('width').text
        h = root.find('size').find('height').text
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = scale(bbx.find('xmin').text, w)
            ymin = scale(bbx.find('ymin').text, h)
            xmax = scale(bbx.find('xmax').text, w)
            ymax = scale(bbx.find('ymax').text, h)
            label = member.find('name').text

            value = ('',
                    f"gs://eeeooo/tmp/{root.find('filename').text}",
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


def main():
    xml_to_csv('e:/Data/EOS/tmp_xml')


main()